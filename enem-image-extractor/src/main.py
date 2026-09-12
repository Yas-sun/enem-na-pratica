"""
ENEM PDF to Question Images Extractor

Main entry point for extracting individual question images from ENEM exam PDFs.
"""

import fitz  # pymupdf
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import json
import argparse
import sys
from typing import Dict, List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from detector import QuestionDetector, QuestionCropper
from enem_utils import (
    get_question_range, get_areas_for_page, 
    get_output_path, validate_question_number
)
from image_utils import normalize_brightness, save_image


class ENEMExtractor:
    """
    Extract question images from ENEM PDFs.
    
    This class orchestrates the extraction process:
    1. Render PDF pages to images
    2. Detect question boundaries
    3. Crop individual question images
    4. Save to disk with proper naming
    """
    
    def __init__(self, dpi: int = 300, min_question_size: int = 100):
        """
        Initialize extractor.
        
        Args:
            dpi: PDF rendering resolution (higher = better quality, slower)
            min_question_size: Minimum dimension for question images
        """
        self.dpi = dpi
        self.detector = QuestionDetector(min_question_height=min_question_size)
        self.cropper = QuestionCropper(padding=15, min_size=min_question_size)
    
    def render_page(self, page) -> np.ndarray:
        """Render PDF page to numpy array (BGR format)."""
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to numpy array
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        
        # Convert to BGR for OpenCV
        if pix.n == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif pix.n == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return img
    
    def extract_questions_from_page(self, img: np.ndarray, page_num: int,
                                     year: int, day: str) -> List[Dict]:
        """
        Extract question images from a single page.
        
        Returns list of dicts with question number and image.
        """
        # Convert to grayscale for detection
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Detect question regions
        regions = self.detector.segment_page(gray, page_num, year, day)
        
        # Determine question range for this page
        q_start, q_end = get_question_range(year, day)
        total_questions = q_end - q_start + 1
        
        # Crop each region
        questions = []
        for i, region in enumerate(regions):
            # Calculate question number based on page and position
            # ENEM D1: Q1-90, D2: Q91-180
            # Each page has ~6 questions
            questions_per_page = 6
            
            q_num = q_start + (page_num * questions_per_page) + i
            
            # Validate question number
            if not validate_question_number(q_num, year, day):
                continue
            
            # Crop the region
            crop = self.cropper.crop_region(img, region)
            
            if crop is not None and crop.shape[0] > 0 and crop.shape[1] > 0:
                # Filter out invalid images (backgrounds, logos, etc.)
                if not self.is_valid_question_image(crop):
                    continue
                
                # Normalize brightness
                crop = normalize_brightness(crop)
                
                questions.append({
                    'number': q_num,
                    'image': crop,
                    'page': page_num,
                    'region': region
                })
        
        return questions
    
    def process_pdf(self, pdf_path: Path, year: int, day: str) -> Dict:
        """
        Process a single PDF file.
        
        Args:
            pdf_path: Path to PDF file
            year: ENEM year
            day: "D1" or "D2"
        
        Returns:
            Dict with extraction results
        """
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print(f"Year: {year}, Day: {day}")
        print(f"{'='*60}")
        
        doc = fitz.open(str(pdf_path))
        
        results = {
            'year': year,
            'day': day,
            'pdf_path': str(pdf_path),
            'total_pages': len(doc),
            'questions': {}
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            print(f"\nPage {page_num + 1}/{len(doc)}...")
            
            # Render page
            img = self.render_page(page)
            
            # Extract questions
            questions = self.extract_questions_from_page(img, page_num, year, day)
            
            print(f"  Found {len(questions)} questions")
            
            # Store results
            for q in questions:
                q_num = q['number']
                if q_num not in results['questions']:
                    results['questions'][q_num] = q
                    print(f"    Q{q_num}: {q['image'].shape[1]}x{q['image'].shape[0]}")
        
        doc.close()
        
        print(f"\nTotal questions extracted: {len(results['questions'])}")
        return results
    
    def is_valid_question_image(self, img: np.ndarray) -> bool:
        """
        Check if an image is a valid question (not a background pattern).
        
        Returns True if the image appears to be a real question.
        """
        # Check 1: Minimum size
        h, w = img.shape[:2]
        if h < 50 or w < 50:
            return False
        
        # Check 2: Color variance (allow more variance)
        if len(img.shape) == 3:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h_std = np.std(hsv[:, :, 0])
            s_std = np.std(hsv[:, :, 1])
            v_std = np.std(hsv[:, :, 2])
        else:
            v_std = np.std(img)
            h_std = s_std = 0
        
        # If all channels have very low variance, it's likely a uniform pattern
        if h_std < 3 and s_std < 5 and v_std < 5:
            return False
        
        # Check 3: Edge density (more lenient)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        if edge_density < 0.01:  # Less than 1% edges
            return False
        
        # Check 4: Aspect ratio (very lenient for questions)
        aspect = w / h
        if aspect < 0.2 or aspect > 15.0:
            return False
        
        return True
    
    def save_results(self, results: Dict, output_dir: Path) -> int:
        """
        Save extracted question images to disk.
        
        Returns number of images saved.
        """
        year = results['year']
        day = results['day']
        
        saved = 0
        for q_num, data in sorted(results['questions'].items()):
            output_path = get_output_path(output_dir, year, day, q_num)
            save_image(data['image'], output_path)
            saved += 1
        
        print(f"\nSaved {saved} images to {output_dir / str(year) / day}")
        return saved
    
    def process_directory(self, pdf_dir: Path, output_dir: Path,
                          years: Optional[List[int]] = None) -> int:
        """
        Process all PDFs in a directory.
        
        Args:
            pdf_dir: Directory containing PDF files
            output_dir: Output directory for images
            years: Optional list of years to process (None = all)
        
        Returns:
            Total number of questions extracted
        """
        import re
        
        total = 0
        
        # Find all PDF files
        pdf_files = list(pdf_dir.rglob("*.pdf"))
        print(f"\nFound {len(pdf_files)} PDF files")
        
        for pdf_path in sorted(pdf_files):
            # Extract year and day from filename
            match = re.search(r'(\d{4}).*?(D[12])', pdf_path.name)
            
            if match:
                year = int(match.group(1))
                day = match.group(2)
                
                # Filter by year if specified
                if years and year not in years:
                    continue
                
                results = self.process_pdf(pdf_path, year, day)
                saved = self.save_results(results, output_dir)
                total += saved
        
        print(f"\n{'='*60}")
        print(f"Total: {total} question images extracted")
        print(f"{'='*60}")
        
        return total


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract question images from ENEM exam PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from single PDF
  python main.py /path/to/2024_PV_impresso_D1_CD1.pdf --year 2024 --day D1
  
  # Extract from all PDFs in directory
  python main.py /path/to/pdfs/ --output ./output
  
  # Extract only specific years
  python main.py /path/to/pdfs/ --years 2024 2025
        """
    )
    
    parser.add_argument("input", help="PDF file or directory containing PDFs")
    parser.add_argument("--output", "-o", default="output", 
                        help="Output directory (default: output)")
    parser.add_argument("--year", type=int, help="ENEM year (for single PDF)")
    parser.add_argument("--day", choices=["D1", "D2"], help="Exam day (for single PDF)")
    parser.add_argument("--years", type=int, nargs="+", 
                        help="Process only these years")
    parser.add_argument("--dpi", type=int, default=300,
                        help="PDF rendering DPI (default: 300)")
    parser.add_argument("--min-size", type=int, default=100,
                        help="Minimum question image size (default: 100)")
    
    args = parser.parse_args()
    
    # Create extractor
    extractor = ENEMExtractor(dpi=args.dpi, min_question_size=args.min_size)
    output_dir = Path(args.output)
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Process single PDF
        year = args.year
        day = args.day
        
        # Try to extract from filename if not provided
        if not year or not day:
            import re
            match = re.search(r'(\d{4}).*?(D[12])', input_path.name)
            if match:
                year = year or int(match.group(1))
                day = day or match.group(2)
            else:
                print("Error: Could not determine year and day from filename")
                print("Please provide --year and --day arguments")
                sys.exit(1)
        
        results = extractor.process_pdf(input_path, year, day)
        extractor.save_results(results, output_dir)
        
    elif input_path.is_dir():
        # Process directory
        extractor.process_directory(input_path, output_dir, args.years)
        
    else:
        print(f"Error: {input_path} not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
