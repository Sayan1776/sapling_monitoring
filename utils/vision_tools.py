import cv2
import numpy as np

def detect_pits_op1(image):
    """Detects 45cm pits using circular hough transform."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Param2 is sensitivity; lower detects more circles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                               param1=50, param2=25, minRadius=10, maxRadius=30)
    return circles

def is_alive(patch, threshold=35):
    """Calculates Excess Green Index (ExG) to detect sapling survival."""
    r, g, b = cv2.split(patch.astype(np.float32))
    exg = 2*g - r - b
    exg_norm = (exg - exg.min()) / (exg.max() - exg.min() + 1e-6)
    green_mask = exg_norm > 0.3
    
    # Mask out the background
    green_mask = np.where(exg > threshold, 1, 0)
    survival_ratio = np.sum(green_mask) / green_mask.size
    
    # If more than 5% of the pit area is green, it's a surviving sapling
    return survival_ratio > 0.05, survival_ratio