"""
ENEM Image Extractor v3 - Render at 300 DPI, detect lines for precise cropping.
Replicates the quality of existing images in images/2019/.
"""

import fitz
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import re
import json
from typing import Dict, List, Tuple


class ENEMImageExtractorV3:
    """
    Extract question images from ENEM PDFs by rendering pages at high DPI
    and cropping based on horizontal line detection.
    
    This replicates the quality of existing images in images/2019/.
    """
    
    def __init__(self, dpi: int = 300):
        self.dpi = dpi
    
    def render_page(self, page: fitz.Page) -> np.ndarray:
        """Render PDF page to numpy array."""
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        
        if pix.n == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif pix.n == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return img
    
    def detect_question_boundaries(self, gray: np.ndarray) -> List[int]:
        """Detect horizontal lines that separate questions."""
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
        
        contours, _ = cv2.findContours(lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        line_positions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > gray.shape[1] * 0.25:
                line_positions.append(y)
        
        return sorted(set(line_positions))
    
    def get_question_numbers(self, page: fitz.Page) -> List[int]:
        """Extract question numbers from page text."""
        text = page.get_text()
        
        numbers = set()
        
        matches = re.findall(r'Questão\s+(\d{1,3})', text, re.MULTILINE)
        for m in matches:
            num = int(m)
            if 1 <= num <= 180:
                numbers.add(num)
        
        matches = re.findall(r'QUESTÃO\s+(\d{1,3})', text, re.MULTILINE)
        for m in matches:
            num = int(m)
            if 1 <= num <= 180:
                numbers.add(num)
        
        matches = re.findall(r'Questões\s+de\s+(\d{1,3})\s+a\s+(\d{1,3})', text, re.MULTILINE)
        for start, end in matches:
            s, e = int(start), int(end)
            if 1 <= s <= 180 and 1 <= e <= 180:
                numbers.add(s)
                numbers.add(e)
        
        return sorted(numbers)
    
    def remove_white_borders(self, img: np.ndarray) -> np.ndarray:
        """Remove white borders from cropped image."""
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            all_points = np.vstack(contours)
            x, y, w, h = cv2.boundingRect(all_points)
            
            pad = 3
            x = max(0, x - pad)
            y = max(0, y - pad)
            w = min(img.shape[1] - x, w + 2 * pad)
            h = min(img.shape[0] - y, h + 2 * pad)
            
            return img[y:y+h, x:x+w]
        
        return img
    
    def extract_page_questions(self, img: np.ndarray, q_numbers: List[int]) -> Dict[int, np.ndarray]:
        """Extract question images from a rendered page."""
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        h, w = gray.shape[:2]
        
        # Detect horizontal lines
        line_positions = self.detect_question_boundaries(gray)
        
        # Create boundaries
        boundaries = [0] + line_positions + [h]
        
        # Create regions between boundaries
        regions = []
        for i in range(len(boundaries) - 1):
            y_start = boundaries[i]
            y_end = boundaries[i + 1]
            
            if y_end - y_start < 50:
                continue
            
            regions.append((y_start, y_end))
        
        # If line detection didn't produce enough regions, fall back to equal splitting
        if len(regions) < len(q_numbers):
            region_height = h // len(q_numbers)
            regions = []
            for i in range(len(q_numbers)):
                y_start = i * region_height
                y_end = (i + 1) * region_height if i < len(q_numbers) - 1 else h
                regions.append((y_start, y_end))
        
        # Match regions to question numbers
        questions = {}
        
        for i, (y_start, y_end) in enumerate(regions):
            if i < len(q_numbers):
                q_num = q_numbers[i]
            else:
                continue
            
            pad = 10
            y_start = max(0, y_start - pad)
            y_end = min(h, y_end + pad)
            
            crop = img[y_start:y_end, 0:w]
            
            if crop.shape[0] < 30 or crop.shape[1] < 30:
                continue
            
            # Remove white borders
            crop = self.remove_white_borders(crop)
            
            # Convert to RGBA
            if len(crop.shape) == 3 and crop.shape[2] == 3:
                crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGBA)
            elif len(crop.shape) == 2:
                crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2RGBA)
            
            questions[q_num] = crop
        
        return questions
    
    def process_pdf(self, pdf_path: Path, year: int, day: str) -> Dict[int, np.ndarray]:
        """Process a PDF and extract all question images."""
        print(f"\nProcessing {pdf_path.name}...")
        
        doc = fitz.open(str(pdf_path))
        
        all_questions = {}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            q_numbers = self.get_question_numbers(page)
            
            if not q_numbers:
                continue
            
            img = self.render_page(page)
            
            questions = self.extract_page_questions(img, q_numbers)
            
            if questions:
                print(f"  Page {page_num + 1}: {len(questions)} questions extracted")
                all_questions.update(questions)
        
        doc.close()
        
        print(f"  Total: {len(all_questions)} questions")
        return all_questions
    
    def save_images(self, images: Dict[int, np.ndarray], output_dir: Path, target_size: Tuple[int, int] = (605, 530)):
        """Save images as Q{number}.png, resized to target size."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved = 0
        
        for q_num in sorted(images.keys()):
            img = images[q_num]
            filename = f"Q{q_num:03d}.png"
            filepath = output_dir / filename
            
            if len(img.shape) == 3 and img.shape[2] == 4:
                pil_img = Image.fromarray(img, 'RGBA')
            elif len(img.shape) == 3 and img.shape[2] == 3:
                pil_img = Image.fromarray(img, 'RGB')
            else:
                pil_img = Image.fromarray(img)
            
            # Resize to target size
            pil_img = pil_img.resize(target_size, Image.LANCZOS)
            
            pil_img.save(str(filepath), 'PNG')
            saved += 1
        
        print(f"  Saved {saved} images")
        return saved


def main():
    """Extract images from all ENEM PDFs."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ENEM Image Extractor v3")
    parser.add_argument("pdf_path", help="PDF file or directory")
    parser.add_argument("--year", type=int, help="ENEM year")
    parser.add_argument("--day", choices=["D1", "D2"], help="Exam day")
    parser.add_argument("--output", "-o", default="output_v3", help="Output directory")
    
    args = parser.parse_args()
    
    extractor = ENEMImageExtractorV3(dpi=300)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_path = Path(args.pdf_path)
    
    if pdf_path.is_file():
        year = args.year or int(re.search(r'(\d{4})', pdf_path.name).group(1))
        day = args.day or ("D1" if "D1" in pdf_path.name else "D2")
        
        images = extractor.process_pdf(pdf_path, year, day)
        extractor.save_images(images, output_dir / str(year) / day)
    
    elif pdf_path.is_dir():
        total = 0
        
        for pdf_file in sorted(pdf_path.rglob("*.pdf")):
            match = re.search(r'(\d{4}).*?(D[12])', pdf_file.name)
            if match:
                year = int(match.group(1))
                day = match.group(2)
                
                images = extractor.process_pdf(pdf_file, year, day)
                saved = extractor.save_images(images, output_dir / str(year) / day)
                total += saved
        
        print(f"\nTotal: {total} images extracted")


if __name__ == "__main__":
    main()
