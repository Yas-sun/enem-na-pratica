"""
Advanced question detector using multiple detection strategies.
"""

import cv2
import numpy as np
from PIL import Image
from typing import List, Dict, Tuple, Optional
import re


class QuestionDetector:
    """
    Detect question boundaries using multiple strategies:
    1. Horizontal line detection
    2. OCR-based question number detection
    3. Visual pattern matching
    """
    
    def __init__(self, min_question_height: int = 100, 
                 max_question_height: int = 800):
        self.min_height = min_question_height
        self.max_height = max_question_height
    
    def detect_by_lines(self, gray: np.ndarray) -> List[int]:
        """
        Detect horizontal lines that separate questions.
        
        Returns sorted list of y-coordinates.
        """
        # Detect horizontal lines using morphological operations
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
        lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Find contours
        contours, _ = cv2.findContours(lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Extract y-coordinates
        line_positions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter: line must be reasonably long
            if w > gray.shape[1] * 0.25:
                line_positions.append(y)
        
        return sorted(set(line_positions))
    
    def detect_by_numbers(self, gray: np.ndarray) -> List[Dict]:
        """
        Detect question numbers using OCR.
        
        Returns list of dicts with question number and position.
        """
        try:
            import pytesseract
            from pytesseract import Output
            
            # OCR with detailed output
            data = pytesseract.image_to_data(
                gray, 
                output_type=Output.DICT, 
                lang='por',
                config='--psm 6'  # Assume uniform block of text
            )
            
            questions = []
            for i, text in enumerate(data['text']):
                text = text.strip()
                
                # Match question number patterns
                patterns = [
                    (r'^(\d{1,3})\.$', 1),      # "1."
                    (r'^(\d{1,3})\)$', 1),      # "1)"
                    (r'^(\d{1,3})\s*[-–]$', 1), # "1 -"
                    (r'[Qq]uestão\s+(\d{1,3})', 1),
                    (r'QUESTÃO\s+(\d{1,3})', 1),
                ]
                
                for pattern, group in patterns:
                    match = re.search(pattern, text)
                    if match:
                        q_num = int(match.group(group))
                        if 1 <= q_num <= 180:
                            questions.append({
                                'number': q_num,
                                'x': data['left'][i],
                                'y': data['top'][i],
                                'w': data['width'][i],
                                'h': data['height'][i]
                            })
                            break
            
            return questions
            
        except ImportError:
            return []
    
    def detect_by_visual_patterns(self, gray: np.ndarray) -> List[Dict]:
        """
        Detect questions by visual patterns (bullet points, numbers in circles).
        
        Returns list of dicts with detected position.
        """
        # Template matching for common question markers
        # This is a simplified version - could be enhanced with ML
        
        # Look for circular markers (often used for question numbers)
        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
            param1=50, param2=30, minRadius=10, maxRadius=30
        )
        
        results = []
        if circles is not None:
            for circle in circles[0]:
                x, y, r = circle
                results.append({
                    'x': int(x - r),
                    'y': int(y - r),
                    'w': int(2 * r),
                    'h': int(2 * r)
                })
        
        return results
    
    def segment_page(self, gray: np.ndarray, page_num: int,
                     year: int, day: str) -> List[Dict]:
        """
        Segment page into individual questions.
        
        Returns list of dicts with question number and bounding box.
        """
        h, w = gray.shape[:2]
        
        # Strategy 1: Use horizontal lines
        line_positions = self.detect_by_lines(gray)
        
        if len(line_positions) >= 2:
            # Create regions between lines
            regions = []
            prev_y = 0
            
            for y in line_positions:
                if y - prev_y >= self.min_height:
                    regions.append({
                        'y_start': prev_y,
                        'y_end': y,
                        'x_start': 0,
                        'x_end': w
                    })
                    prev_y = y
            
            # Add last region
            if h - prev_y >= self.min_height:
                regions.append({
                    'y_start': prev_y,
                    'y_end': h,
                    'x_start': 0,
                    'x_end': w
                })
            
            return regions
        
        # Strategy 2: Use OCR-detected numbers
        q_numbers = self.detect_by_numbers(gray)
        
        if q_numbers:
            # Sort by position
            q_numbers.sort(key=lambda q: (q['y'], q['x']))
            
            regions = []
            for i, q in enumerate(q_numbers):
                # Estimate region based on next question
                if i + 1 < len(q_numbers):
                    y_end = q_numbers[i + 1]['y']
                else:
                    y_end = h
                
                regions.append({
                    'number': q['number'],
                    'y_start': q['y'],
                    'y_end': min(y_end, q['y'] + self.max_height),
                    'x_start': 0,
                    'x_end': w
                })
            
            return regions
        
        # Strategy 3: Fixed segmentation (fallback)
        num_questions = 15  # Typical for ENEM
        q_height = h // num_questions
        
        regions = []
        for i in range(num_questions):
            regions.append({
                'number': i + 1,  # Will be adjusted by caller
                'y_start': i * q_height,
                'y_end': (i + 1) * q_height,
                'x_start': 0,
                'x_end': w
            })
        
        return regions


class QuestionCropper:
    """Crop question images from page based on detected regions."""
    
    def __init__(self, padding: int = 10, min_size: int = 50):
        self.padding = padding
        self.min_size = min_size
    
    def crop_region(self, img: np.ndarray, region: Dict) -> Optional[np.ndarray]:
        """
        Crop a region from the image.
        
        Args:
            img: Full page image (BGR or grayscale)
            region: Dict with x_start, y_start, x_end, y_end
        
        Returns:
            Cropped image or None if too small
        """
        h, w = img.shape[:2]
        
        # Get coordinates with padding
        x1 = max(0, region['x_start'] - self.padding)
        y1 = max(0, region['y_start'] - self.padding)
        x2 = min(w, region['x_end'] + self.padding)
        y2 = min(h, region['y_end'] + self.padding)
        
        # Check minimum size
        if (x2 - x1) < self.min_size or (y2 - y1) < self.min_size:
            return None
        
        # Crop
        crop = img[y1:y2, x1:x2]
        
        # Remove white borders
        crop = self._remove_borders(crop)
        
        return crop
    
    def _remove_borders(self, img: np.ndarray) -> np.ndarray:
        """Remove white borders from cropped image."""
        # Convert to grayscale for analysis
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Threshold
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get bounding box of all content
            all_points = np.vstack(contours)
            x, y, w, h = cv2.boundingRect(all_points)
            
            # Crop to content
            return img[y:y+h, x:x+w]
        
        return img
    
    def crop_with_aspect_ratio(self, img: np.ndarray, region: Dict,
                                target_aspect: float = 0.75) -> np.ndarray:
        """
        Crop region and adjust to target aspect ratio.
        
        Useful for making question images consistent size.
        """
        crop = self.crop_region(img, region)
        if crop is None:
            return None
        
        h, w = crop.shape[:2]
        current_aspect = w / h
        
        if current_aspect > target_aspect:
            # Too wide, crop width
            new_w = int(h * target_aspect)
            start_x = (w - new_w) // 2
            crop = crop[:, start_x:start_x + new_w]
        else:
            # Too tall, crop height
            new_h = int(w / target_aspect)
            start_y = (h - new_h) // 2
            crop = crop[start_y:start_y + new_h, :]
        
        return crop
