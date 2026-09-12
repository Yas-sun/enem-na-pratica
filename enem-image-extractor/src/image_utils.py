"""
Image processing utilities for question extraction.
"""

import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional
from pathlib import Path


def preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
    """
    Preprocess image for better OCR results.
    
    - Convert to grayscale
    - Apply adaptive thresholding
    - Remove noise
    """
    # Convert to grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Remove noise with median blur
    denoised = cv2.medianBlur(binary, 3)
    
    return denoised


def detect_text_regions(img: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Detect text regions in an image.
    
    Returns list of (x, y, width, height) bounding boxes.
    """
    # Preprocess
    processed = preprocess_for_ocr(img)
    
    # Find contours
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by size and position
    regions = []
    img_h, img_w = img.shape[:2]
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter: text lines are typically wider than tall
        aspect = w / h if h > 0 else 0
        if aspect > 0.5 and w > 20 and h > 5:
            regions.append((x, y, w, h))
    
    return regions


def detect_images_in_region(img: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Detect embedded images (figures, tables) in a region.
    
    Returns list of (x, y, width, height) bounding boxes.
    """
    # Convert to grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Dilate to connect edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by size
    regions = []
    img_h, img_w = img.shape[:2]
    min_size = min(img_h, img_w) * 0.05  # At least 5% of image
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        if w > min_size and h > min_size:
            # Check if it's likely an image (not text)
            aspect = w / h if h > 0 else 0
            if 0.2 < aspect < 5.0:
                regions.append((x, y, w, h))
    
    return regions


def split_columns(img: np.ndarray) -> List[np.ndarray]:
    """
    Split a page image into columns (for two-column layouts).
    
    Returns list of column images.
    """
    # Convert to grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Project vertically
    projection = np.sum(gray < 128, axis=0)
    
    # Find gaps (low projection values)
    threshold = np.mean(projection) * 0.1
    gaps = []
    
    in_gap = False
    gap_start = 0
    
    for x, val in enumerate(projection):
        if val < threshold and not in_gap:
            in_gap = True
            gap_start = x
        elif val >= threshold and in_gap:
            in_gap = False
            gap_width = x - gap_start
            if gap_width > 20:  # Significant gap
                gaps.append((gap_start, x))
    
    # Split by gaps
    if gaps:
        columns = []
        prev_end = 0
        
        for gap_start, gap_end in gaps:
            columns.append(img[:, prev_end:gap_start])
            prev_end = gap_end
        
        columns.append(img[:, prev_end:])
        return columns
    
    return [img]


def crop_with_padding(img: np.ndarray, x: int, y: int, w: int, h: int,
                      padding: int = 10) -> np.ndarray:
    """
    Crop image with padding, clamping to image bounds.
    """
    img_h, img_w = img.shape[:2]
    
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(img_w, x + w + padding)
    y2 = min(img_h, y + h + padding)
    
    return img[y1:y2, x1:x2]


def resize_to_height(img: np.ndarray, target_height: int) -> np.ndarray:
    """Resize image to target height, maintaining aspect ratio."""
    h, w = img.shape[:2]
    scale = target_height / h
    new_w = int(w * scale)
    return cv2.resize(img, (new_w, target_height))


def normalize_brightness(img: np.ndarray) -> np.ndarray:
    """Normalize image brightness for consistent appearance."""
    # Convert to LAB color space
    if len(img.shape) == 3:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
    else:
        l_channel = img
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l_channel)
    
    # Merge back
    if len(img.shape) == 3:
        lab[:, :, 0] = l_eq
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        return l_eq


def save_image(img: np.ndarray, path: Path, quality: int = 95):
    """
    Save image to disk.
    
    Args:
        img: Image array (BGR or grayscale)
        path: Output path
        quality: JPEG quality (if saving as JPEG)
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert BGR to RGB for PIL
    if len(img.shape) == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    pil_img = Image.fromarray(img_rgb)
    
    # Save based on extension
    if path.suffix.lower() in ['.jpg', '.jpeg']:
        pil_img.save(str(path), 'JPEG', quality=quality)
    else:
        pil_img.save(str(path), 'PNG')
