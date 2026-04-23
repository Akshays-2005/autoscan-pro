"""
Image processing pipeline using OpenCV.
Steps follow the exact spec:
 1. grayscale
 2. Gaussian blur (5,5)
 3. Canny edges (50,150)
 4. external contours
 5. largest contour
 6. approxPolyDP (0.02 * perimeter)
 7. if 4 points -> reorder -> perspective warp 500x700
 8. grayscale + threshold(150,255, BINARY)
"""
import cv2
import numpy as np


def reorder_points(pts: np.ndarray) -> np.ndarray:
    pts = pts.reshape(4, 2)
    ordered = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)
    ordered[0] = pts[np.argmin(s)]   # top-left
    ordered[2] = pts[np.argmax(s)]   # bottom-right
    ordered[1] = pts[np.argmin(d)]   # top-right
    ordered[3] = pts[np.argmax(d)]   # bottom-left
    return ordered


def scan_document(img: np.ndarray, width: int = 500, height: int = 700):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(largest, True)
    approx = cv2.approxPolyDP(largest, 0.02 * perimeter, True)

    if len(approx) != 4:
        return None

    ordered = reorder_points(approx)
    dst = np.array(
        [[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32
    )
    M = cv2.getPerspectiveTransform(ordered, dst)
    warped = cv2.warpPerspective(img, M, (width, height))

    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(warped_gray, 150, 255, cv2.THRESH_BINARY)
    return thresh
