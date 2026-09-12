"""
ENEM PDF Image Extractor

Extracts individual question images from ENEM exam PDFs using:
- PyMuPDF for PDF rendering
- OpenCV for image processing and contour detection
- Tesseract OCR for text detection (optional)
"""

import fitz  # pymupdf
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import re
import json
import argparse
from typing import List, Tuple, Optional, Dict


class ENEMImageExtractor:
    """Extract question images from ENEM PDFs."""
    
    # ENEM structure: ~15 questions per page in printed version
    QUESTIONS_PER_PAGE = 15
    
    # Minimum image dimensions to keep (filter out logos/icons)
    MIN_WIDTH = 150
    MIN_HEIGHT = 100
    
    # Maximum aspect ratio (width/height) to filter out banners
    MAX_ASPECT_RATIO = 4.0
    
    def __init__(self, dpi: int = 300):
        """
        Initialize extractor.
        
        Args:
            dpi: Resolution for PDF rendering (higher = better quality, slower)
        """
        self.dpi = dpi
    
    def render_page_to_image(self, page) -> np.ndarray:
        """Render a PDF page to a numpy array (OpenCV format)."""
        # Render at specified DPI
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to numpy array
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        
        # Convert RGB to BGR for OpenCV
        if pix.n == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        
        return img
    
    def detect_question_regions(self, page_img: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect question regions in a page image.
        
        Returns list of (x, y, width, height) bounding boxes.
        """
        # Convert to grayscale
        if len(page_img.shape) == 3:
            gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = page_img
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and position
        regions = []
        page_h, page_w = page_img.shape[:2]
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by minimum size
            if w < self.MIN_WIDTH or h < self.MIN_HEIGHT:
                continue
            
            # Filter by aspect ratio
            aspect = w / h if h > 0 else 0
            if aspect > self.MAX_ASPECT_RATIO:
                continue
            
            # Filter out very small or very large regions
            area_ratio = (w * h) / (page_w * page_h)
            if area_ratio < 0.005 or area_ratio > 0.5:
                continue
            
            regions.append((x, y, w, h))
        
        # Sort by position (top to bottom, left to right)
        regions.sort(key=lambda r: (r[1], r[0]))
        
        return regions
    
    def detect_question_by_text(self, page_img: np.ndarray, page_num: int, 
                                 year: int, day: str) -> List[Dict]:
        """
        Detect questions by finding question numbers in text.
        
        Returns list of dicts with question info and bounding boxes.
        """
        # Convert to grayscale
        if len(page_img.shape) == 3:
            gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = page_img
        
        # Use pytesseract to find text regions
        try:
            import pytesseract
            from pytesseract import Output
            
            # Get detailed OCR data
            data = pytesseract.image_to_data(gray, output_type=Output.DICT, 
                                              lang='por')
            
            # Find question number patterns
            questions = []
            for i, text in enumerate(data['text']):
                # Match patterns like "1.", "1)", "Questão 1", "QUESTÃO 1"
                match = re.match(r'^(\d{1,3})[.\)]?$', text.strip())
                if match:
                    q_num = int(match.group(1))
                    if 1 <= q_num <= 180:  # Valid ENEM question range
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        
                        # Expand bounding box to include full question
                        # Typically extends to next question or page bottom
                        expanded_box = self._expand_question_box(
                            x, y, w, h, page_img.shape, q_num
                        )
                        
                        questions.append({
                            'number': q_num,
                            'box': expanded_box,
                            'text': text
                        })
            
            return questions
            
        except ImportError:
            print("pytesseract not available, using contour-based detection")
            return []
    
    def _expand_question_box(self, x: int, y: int, w: int, h: int,
                              page_shape: Tuple, q_num: int) -> Tuple[int, int, int, int]:
        """Expand bounding box to cover full question area."""
        page_h, page_w = page_shape[:2]
        
        # Expand width to cover most of the page
        new_x = max(0, x - 20)
        new_w = min(page_w - new_x, w + 40)
        
        # Height will be determined by spacing between questions
        # For now, use a reasonable default
        new_h = max(h * 3, 200)  # At least 3x the number height
        
        return (new_x, y, new_w, new_h)
    
    def extract_questions_from_page(self, page, year: int, day: str, 
                                     page_num: int) -> List[Dict]:
        """
        Extract question images from a single PDF page.
        
        Returns list of dicts with question number and image data.
        """
        # Render page to image
        page_img = self.render_page_to_image(page)
        
        # Detect question regions
        regions = self.detect_question_regions(page_img)
        
        # If no regions found, try text-based detection
        if not regions:
            questions = self.detect_question_by_text(page_img, page_num, year, day)
            if questions:
                regions = [q['box'] for q in questions]
        
        # Extract images for each region
        extracted = []
        for i, (x, y, w, h) in enumerate(regions):
            # Crop the region
            crop = page_img[y:y+h, x:x+w]
            
            # Filter out small/noisy crops
            if crop.shape[0] < self.MIN_HEIGHT or crop.shape[1] < self.MIN_WIDTH:
                continue
            
            # Convert to PIL Image
            crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(crop_rgb)
            
            extracted.append({
                'image': pil_image,
                'box': (x, y, w, h),
                'page': page_num
            })
        
        return extracted
    
    def extract_from_pdf(self, pdf_path: Path, year: int, day: str) -> Dict:
        """
        Extract all question images from a PDF.
        
        Args:
            pdf_path: Path to PDF file
            year: ENEM year
            day: "D1" or "D2"
        
        Returns:
            Dict with extraction results
        """
        doc = fitz.open(str(pdf_path))
        
        results = {
            'year': year,
            'day': day,
            'pdf_path': str(pdf_path),
            'total_pages': len(doc),
            'questions': []
        }
        
        # Determine question range for this day
        if day == "D1":
            q_start, q_end = 1, 90
        else:  # D2
            q_start, q_end = 91, 180
        
        # Calculate questions per page
        questions_per_page = (q_end - q_start + 1) / len(doc)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract questions from this page
            extracted = self.extract_questions_from_page(page, year, day, page_num)
            
            # Assign question numbers based on page
            base_q = q_start + int(page_num * questions_per_page)
            
            for i, item in enumerate(extracted):
                q_num = base_q + i
                if q_start <= q_num <= q_end:
                    item['question_number'] = q_num
                    results['questions'].append(item)
        
        doc.close()
        return results
    
    def save_questions(self, results: Dict, output_dir: Path):
        """Save extracted question images to disk."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for item in results['questions']:
            q_num = item['question_number']
            img = item['image']
            
            filename = f"Q{q_num}.png"
            filepath = output_dir / filename
            
            img.save(str(filepath), 'PNG')
            print(f"  Saved Q{q_num}.png ({img.width}x{img.height})")
    
    def process_pdf(self, pdf_path: Path, year: int, day: str, 
                    output_dir: Path) -> int:
        """
        Process a single PDF and save extracted images.
        
        Returns number of questions extracted.
        """
        print(f"\nProcessing {pdf_path.name}...")
        
        results = self.extract_from_pdf(pdf_path, year, day)
        
        # Create output directory for this PDF
        pdf_output = output_dir / str(year) / day
        self.save_questions(results, pdf_output)
        
        print(f"  Extracted {len(results['questions'])} question images")
        return len(results['questions'])


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract question images from ENEM PDFs"
    )
    parser.add_argument("--pdf", type=str, help="Path to PDF file")
    parser.add_argument("--year", type=int, help="ENEM year")
    parser.add_argument("--day", type=str, choices=["D1", "D2"], help="Exam day")
    parser.add_argument("--pdf-dir", type=str, help="Directory with PDFs")
    parser.add_argument("--output", type=str, default="output", 
                        help="Output directory")
    parser.add_argument("--dpi", type=int, default=300, 
                        help="PDF rendering DPI (default: 300)")
    
    args = parser.parse_args()
    
    extractor = ENEMImageExtractor(dpi=args.dpi)
    output_dir = Path(args.output)
    
    if args.pdf:
        # Process single PDF
        pdf_path = Path(args.pdf)
        year = args.year or int(re.search(r'(\d{4})', pdf_path.name).group(1))
        day = args.day or ("D1" if "D1" in pdf_path.name else "D2")
        
        extractor.process_pdf(pdf_path, year, day, output_dir)
        
    elif args.pdf_dir:
        # Process all PDFs in directory
        pdf_dir = Path(args.pdf_dir)
        total = 0
        
        for pdf_path in sorted(pdf_dir.rglob("*.pdf")):
            # Extract year and day from filename
            match = re.search(r'(\d{4}).*?(D[12])', pdf_path.name)
            if match:
                year = int(match.group(1))
                day = match.group(2)
                total += extractor.process_pdf(pdf_path, year, day, output_dir)
        
        print(f"\nTotal: {total} question images extracted")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
