"""
ENEM PDF Image Extractor v2 - Uses text extraction for accurate numbering.
"""

import fitz  # pymupdf
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import re
import json
from typing import Dict, List, Tuple


class ENEMExtractorV2:
    """
    Extract question images from ENEM PDFs with accurate numbering.
    
    Uses text extraction to determine question numbers, then renders
    and crops the corresponding regions.
    """
    
    def __init__(self, dpi: int = 300):
        self.dpi = dpi
    
    def extract_question_map(self, pdf_path: Path) -> Dict[int, List[int]]:
        """
        Extract mapping of page numbers to question numbers.
        
        Returns dict: {page_num: [question_numbers]}
        """
        doc = fitz.open(str(pdf_path))
        
        page_questions = {}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Find question numbers
            patterns = [
                r'Questão\s+(\d{1,3})',
                r'QUESTÃO\s+(\d{1,3})',
                r'^(\d{1,3})\.\s',
                r'^(\d{1,3})\)\s',
            ]
            
            found = set()
            for pattern in patterns:
                matches = re.findall(pattern, text, re.MULTILINE)
                for match in matches:
                    num = int(match)
                    if 1 <= num <= 180:
                        found.add(num)
            
            if found:
                page_questions[page_num] = sorted(found)
        
        doc.close()
        return page_questions
    
    def render_page(self, page) -> np.ndarray:
        """Render PDF page to numpy array."""
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        
        if pix.n == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif pix.n == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return img
    
    def detect_question_regions(self, gray: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect question regions using horizontal line detection.
        
        Returns list of (x, y, width, height) bounding boxes.
        """
        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
        lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Find contours
        contours, _ = cv2.findContours(lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get line positions
        line_positions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > gray.shape[1] * 0.25:
                line_positions.append(y)
        
        line_positions.sort()
        
        # Create regions between lines
        regions = []
        prev_y = 0
        
        for y in line_positions:
            if y - prev_y > 50:  # Minimum region height
                regions.append((0, prev_y, gray.shape[1], y - prev_y))
            prev_y = y
        
        # Add last region
        if gray.shape[0] - prev_y > 50:
            regions.append((0, prev_y, gray.shape[1], gray.shape[0] - prev_y))
        
        return regions
    
    def has_image_in_bottom(self, crop: np.ndarray, threshold: float = 0.1) -> bool:
        """
        Check if question crop has an image in the bottom portion.
        
        Args:
            crop: Question image (BGR)
            threshold: Minimum ratio of non-white pixels to consider as image
        
        Returns:
            True if image detected in bottom
        """
        h, w = crop.shape[:2]
        
        # Bottom 40% of the question
        bottom_start = int(h * 0.6)
        bottom = crop[bottom_start:, :]
        
        # Convert to grayscale
        if len(bottom.shape) == 3:
            gray = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)
        else:
            gray = bottom
        
        # Threshold to find non-white pixels
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Count non-white pixels
        non_white_ratio = np.sum(binary > 0) / binary.size
        
        return non_white_ratio > threshold
    
    def extract_questions_from_page(self, img: np.ndarray, 
                                     question_numbers: List[int]) -> List[Dict]:
        """
        Extract question images from a page.
        
        Args:
            img: Page image (BGR)
            question_numbers: List of question numbers on this page
        
        Returns:
            List of dicts with question number and image
        """
        # Convert to grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Detect regions
        regions = self.detect_question_regions(gray)
        
        # If regions don't match question count, use simple equal splitting
        if len(regions) != len(question_numbers):
            # Split page evenly based on question count
            h, w = gray.shape
            regions = []
            region_height = h // len(question_numbers)
            
            for i, q_num in enumerate(question_numbers):
                y_start = i * region_height
                y_end = (i + 1) * region_height if i < len(question_numbers) - 1 else h
                regions.append((0, y_start, w, y_end - y_start))
        
        # Match regions to question numbers
        questions = []
        
        for i, region in enumerate(regions):
            x, y, w, h = region
            
            # Get question number
            if i < len(question_numbers):
                q_num = question_numbers[i]
            else:
                continue
            
            # Crop the region
            crop = img[y:y+h, x:x+w]
            
            # Filter small crops
            if crop.shape[0] < 30 or crop.shape[1] < 30:
                continue
            
            # Check if has image in bottom
            has_image = self.has_image_in_bottom(crop)
            
            questions.append({
                'number': q_num,
                'image': crop,
                'box': (x, y, w, h),
                'has_image': has_image
            })
        
        return questions
    
    def process_pdf(self, pdf_path: Path, year: int, day: str) -> Dict:
        """
        Process a PDF and extract question images.
        
        Returns dict with extraction results.
        """
        print(f"\nProcessing {pdf_path.name}...")
        
        # Get question map
        page_questions = self.extract_question_map(pdf_path)
        print(f"  Found questions on {len(page_questions)} pages")
        
        # Open PDF
        doc = fitz.open(str(pdf_path))
        
        results = {
            'year': year,
            'day': day,
            'pdf_path': str(pdf_path),
            'questions': {}
        }
        
        for page_num in range(len(doc)):
            if page_num not in page_questions:
                continue
            
            page = doc[page_num]
            question_numbers = page_questions[page_num]
            
            # Render page
            img = self.render_page(page)
            
            # Extract questions
            questions = self.extract_questions_from_page(img, question_numbers)
            
            print(f"  Page {page_num + 1}: {len(questions)} questions")
            
            # Store results
            for q in questions:
                q_num = q['number']
                if q_num not in results['questions']:
                    results['questions'][q_num] = q
        
        doc.close()
        
        print(f"  Total: {len(results['questions'])} questions")
        return results
    
    def save_results(self, results: Dict, output_dir: Path) -> int:
        """Save extracted question images that have images."""
        year = results['year']
        day = results['day']
        
        out_path = output_dir / str(year) / day
        out_path.mkdir(parents=True, exist_ok=True)
        
        saved = 0
        skipped = 0
        
        for q_num, data in sorted(results['questions'].items()):
            # Only save if question has image
            if not data.get('has_image', False):
                skipped += 1
                continue
            
            filename = f"Q{q_num:03d}.png"
            filepath = out_path / filename
            
            # Convert to PIL and save
            img_rgb = cv2.cvtColor(data['image'], cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            pil_img.save(str(filepath), 'PNG')
            
            saved += 1
        
        print(f"  Saved {saved} images, skipped {skipped} (no image)")
        return saved


def main():
    """Extract images from all ENEM PDFs."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ENEM Image Extractor v2")
    parser.add_argument("pdf_path", help="PDF file or directory")
    parser.add_argument("--year", type=int, help="ENEM year")
    parser.add_argument("--day", choices=["D1", "D2"], help="Exam day")
    parser.add_argument("--output", "-o", default="output_v2", help="Output directory")
    
    args = parser.parse_args()
    
    extractor = ENEMExtractorV2(dpi=300)
    output_dir = Path(args.output)
    
    pdf_path = Path(args.pdf_path)
    
    if pdf_path.is_file():
        year = args.year or int(re.search(r'(\d{4})', pdf_path.name).group(1))
        day = args.day or ("D1" if "D1" in pdf_path.name else "D2")
        
        results = extractor.process_pdf(pdf_path, year, day)
        extractor.save_results(results, output_dir)
    
    elif pdf_path.is_dir():
        total = 0
        for pdf_file in sorted(pdf_path.rglob("*.pdf")):
            match = re.search(r'(\d{4}).*?(D[12])', pdf_file.name)
            if match:
                year = int(match.group(1))
                day = match.group(2)
                
                results = extractor.process_pdf(pdf_file, year, day)
                saved = extractor.save_results(results, output_dir)
                total += saved
        
        print(f"\nTotal: {total} questions extracted")


if __name__ == "__main__":
    main()
