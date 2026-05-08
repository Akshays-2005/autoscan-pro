import cv2
import numpy as np


def reorder_points(pts):
    pts = pts.reshape((4, 2))
    ordered = np.zeros((4, 2), dtype=np.float32)

    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)

    ordered[0] = pts[np.argmin(s)]  # top-left
    ordered[1] = pts[np.argmin(d)]  # top-right
    ordered[2] = pts[np.argmax(s)]  # bottom-right
    ordered[3] = pts[np.argmax(d)]  # bottom-left

    return ordered


def is_document_contour(contour, img_area):
    area = cv2.contourArea(contour)

    # Reject very tiny contours
    if area < 0.05 * img_area:
        return False

    x, y, w, h = cv2.boundingRect(contour)

    aspect_ratio = w / float(h)

    # Reject extreme shapes
    if aspect_ratio < 0.5 or aspect_ratio > 2.5:
        return False

    return True


def scan_document(img):
    """
    Automatic Document Alignment Pipeline

    Steps:
    1. Grayscale conversion
    2. Contrast enhancement
    3. Blur
    4. Edge detection
    5. Contour detection
    6. Perspective correction
    7. Return aligned color image
    """

    img_area = img.shape[0] * img.shape[1]

    # ---------------------------------------------------
    # 1. Convert to grayscale
    # ---------------------------------------------------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ---------------------------------------------------
    # 2. Improve contrast using CLAHE
    # ---------------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))

    gray = clahe.apply(gray)

    # ---------------------------------------------------
    # 3. Blur image
    # ---------------------------------------------------
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # ---------------------------------------------------
    # 4. Edge detection
    # ---------------------------------------------------
    edges = cv2.Canny(blur, 20, 100)

    kernel = np.ones((3, 3), np.uint8)

    # Strengthen edges
    edges = cv2.dilate(edges, kernel, iterations=2)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Close broken edges
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    # ---------------------------------------------------
    # 5. Find contours
    # ---------------------------------------------------
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Sort by largest area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    doc_contour = None

    # ---------------------------------------------------
    # Try detecting main document
    # ---------------------------------------------------
    for cnt in contours:

        if not is_document_contour(cnt, img_area):
            continue

        peri = cv2.arcLength(cnt, True)

        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        # Accept imperfect contours
        # Best case → exact 4 corners
        if len(approx) == 4:
            doc_contour = approx
            break

        # Fallback → imperfect contour
        elif len(approx) > 4:

            rect = cv2.minAreaRect(cnt)

            box = cv2.boxPoints(rect)

            box = np.intp(box)

            doc_contour = box.reshape(4, 1, 2)

            break

    # ---------------------------------------------------
    # Fallback for smaller documents/cards
    # ---------------------------------------------------
    if doc_contour is None:

        for cnt in contours[:5]:

            peri = cv2.arcLength(cnt, True)

            approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)

            # Best case → exact 4 corners
            if len(approx) == 4:
                doc_contour = approx
                break

            # Fallback → imperfect contour
            elif len(approx) > 4:

                rect = cv2.minAreaRect(cnt)

                box = cv2.boxPoints(rect)

                box = np.intp(box)

                doc_contour = box.reshape(4, 1, 2)

                break

    # ---------------------------------------------------
    # If no document detected
    # ---------------------------------------------------
    if doc_contour is None:
        return None

    # ---------------------------------------------------
    # 6. Reorder points
    # ---------------------------------------------------
    ordered = reorder_points(doc_contour)

    pts = ordered.reshape(4, 2)

    # Compute width
    width_top = np.linalg.norm(pts[0] - pts[1])
    width_bottom = np.linalg.norm(pts[3] - pts[2])

    width = int(max(width_top, width_bottom))

    # Compute height
    height_left = np.linalg.norm(pts[0] - pts[3])
    height_right = np.linalg.norm(pts[1] - pts[2])

    height = int(max(height_left, height_right))

    # Prevent invalid warp size
    width = max(width, 300)
    height = max(height, 300)

    if width < 50 or height < 50:
        return None

    # ---------------------------------------------------
    # Destination coordinates
    # ---------------------------------------------------
    dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

    # ---------------------------------------------------
    # 7. Perspective transform
    # ---------------------------------------------------
    matrix = cv2.getPerspectiveTransform(ordered, dst)

    warped = cv2.warpPerspective(img, matrix, (width, height))

    # ---------------------------------------------------
    # Optional enhancement
    # ---------------------------------------------------
    warped = cv2.detailEnhance(warped, sigma_s=10, sigma_r=0.15)

    # ---------------------------------------------------
    # Return aligned COLOR image
    # ---------------------------------------------------
    return warped
