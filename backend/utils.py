import cv2
import numpy as np


def reorder_points(pts):
    pts = pts.reshape((4, 2))
    ordered = np.zeros((4, 2), dtype=np.float32)

    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)

    ordered[0] = pts[np.argmin(s)]   # top-left
    ordered[2] = pts[np.argmax(s)]   # bottom-right
    ordered[1] = pts[np.argmin(d)]   # top-right
    ordered[3] = pts[np.argmax(d)]   # bottom-left

    return ordered


def scan_document(img):

    img_area = img.shape[0] * img.shape[1]

    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Improve contrast
    gray = cv2.equalizeHist(gray)

    # 2. Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Edge detection
    edges = cv2.Canny(blur, 30, 120)

    kernel = np.ones((3, 3))
    edges = cv2.dilate(edges, kernel, iterations=2)
    edges = cv2.erode(edges, kernel, iterations=1)

    # 4. Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    doc_contour = None

    # Try large contours
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area < 0.1 * img_area:
            continue

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        if len(approx) == 4:
            doc_contour = approx
            break

    # Fallback for small objects
    if doc_contour is None:
        for cnt in contours[:5]:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)

            if len(approx) == 4:
                doc_contour = approx
                break

    if doc_contour is None:
        return None

    # Reorder
    ordered = reorder_points(doc_contour)

    pts = doc_contour.reshape(4, 2)

    w1 = np.linalg.norm(pts[0] - pts[1])
    w2 = np.linalg.norm(pts[2] - pts[3])
    h1 = np.linalg.norm(pts[0] - pts[3])
    h2 = np.linalg.norm(pts[1] - pts[2])

    width = int(max(w1, w2))
    height = int(max(h1, h2))

    width = max(width, 300)
    height = max(height, 300)

    dst = np.array(
        [[0, 0], [width, 0], [width, height], [0, height]],
        dtype=np.float32
    )

    # Perspective transform
    M = cv2.getPerspectiveTransform(ordered, dst)
    warped = cv2.warpPerspective(img, M, (width, height))

    # 8. Scan effect
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    # 🔥 noise reduction
    warped_gray = cv2.bilateralFilter(warped_gray, 9, 75, 75)

    # 🔥 HYBRID THRESHOLD (FIXES YOUR ISSUE)
    _, thresh1 = cv2.threshold(
        warped_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    thresh2 = cv2.adaptiveThreshold(
        warped_gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    thresh = cv2.bitwise_and(thresh1, thresh2)

    return thresh