"""
ENEM Image Extractor - ONLY embedded images (caue-paiva approach).
No page rendering. Only extract images that are actually embedded in the PDF.
"""

import fitz
import io
from pathlib import Path
from PIL import Image
import re
import json
from typing import Dict, List


class ENEMImageExtractor:
    """
    Extract ONLY embedded images from ENEM PDFs using caue-paiva approach.
    
    Uses page.get_images() + extract_image(xref) to get original embedded images.
    Does NOT render pages or crop - only extracts what's actually in the PDF.
    """
    
    def get_question_numbers(self, page: fitz.Page) -> List[int]:
        """Extract question numbers from page text."""
        text = page.get_text()
        numbers = set()
        
        for pattern in [r'Questão\s+(\d{1,3})', r'QUESTÃO\s+(\d{1,3})']:
            matches = re.findall(pattern, text, re.MULTILINE)
            for m in matches:
                num = int(m)
                if 1 <= num <= 180:
                    numbers.add(num)
        
        return sorted(numbers)
    
    def extract_embedded_images(self, doc: fitz.Document, page: fitz.Page, 
                                    page_num: int, q_numbers: List[int]) -> Dict[int, Image.Image]:
        """
        Extract ONLY embedded images from a page using caue-paiva approach.
        
        Associates each image to the question ABOVE it (last question before image).
        """
        images = page.get_images()
        
        if not images:
            return {}
        
        result = {}
        
        # Get question positions
        text = page.get_text()
        q_positions = {}
        for match in re.finditer(r'Questão\s+(\d{1,3})', text):
            q_num = int(match.group(1))
            if 1 <= q_num <= 180:
                q_rects = page.search_for(f"Questão {q_num}")
                if q_rects:
                    q_positions[q_num] = q_rects[0].y0
        
        if not q_positions:
            return {}
        
        for img_idx, img_tuple in enumerate(images):
            xref = img_tuple[0]
            
            try:
                # Extract image bytes from PDF (caue-paiva method)
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Create Pixmap from bytes
                pix = fitz.Pixmap(image_bytes)
                
                # Handle alpha
                if pix.alpha:
                    try:
                        pix = fitz.Pixmap(pix, 0)
                    except ValueError:
                        continue
                
                # Convert CMYK to RGB
                if pix.n == 4:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix = pix1
                
                # Get image position on page
                rects = page.get_image_rects(xref)
                if not rects:
                    continue
                
                y_pos = rects[0].y0
                
                # Find the LAST question ABOVE the image (question whose y < image y)
                above_questions = {q: y for q, y in q_positions.items() if y < y_pos}
                
                if not above_questions:
                    continue
                
                # Get the question with the largest y (closest above)
                target_q = max(above_questions.keys(), key=lambda q: above_questions[q])
                
                # Convert to PIL Image
                img_data = pix.tobytes("png")
                pil_img = Image.open(io.BytesIO(img_data))
                if pil_img.mode != 'RGBA':
                    pil_img = pil_img.convert('RGBA')
                result[target_q] = pil_img
                    
            except Exception:
                continue
        
        return result
    
    def process_pdf(self, pdf_path: Path, year: int, day: str) -> Dict[int, Image.Image]:
        """
        Process a PDF and extract ONLY embedded images.
        
        Returns dict: {question_number: PIL_Image}
        """
        print(f"\nProcessing {pdf_path.name}...")
        
        doc = fitz.open(str(pdf_path))
        
        all_images = {}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            q_numbers = self.get_question_numbers(page)
            
            if not q_numbers:
                continue
            
            # Extract ONLY embedded images (no rendering)
            embedded = self.extract_embedded_images(doc, page, page_num, q_numbers)
            
            if embedded:
                print(f"  Page {page_num + 1}: {len(embedded)} images - Q{sorted(embedded.keys())}")
                all_images.update(embedded)
        
        doc.close()
        
        print(f"  Total: {len(all_images)} images")
        return all_images
    
    def save_images(self, images: Dict[int, Image.Image], output_dir: Path):
        """Save images as Q{number}.png, resized to 605x530."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved = 0
        
        for q_num in sorted(images.keys()):
            img = images[q_num]
            filename = f"Q{q_num:03d}.png"
            filepath = output_dir / filename
            
            # Resize to 605x530
            img = img.resize((605, 530), Image.LANCZOS)
            
            img.save(str(filepath), 'PNG')
            saved += 1
        
        print(f"  Saved {saved} images to {output_dir}")
        return saved


def main():
    """Extract images from all ENEM PDFs that have embedded images."""
    pdf_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\pdfs")
    img_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\images")
    
    # Process all PDFs
    for year_dir in sorted(pdf_base.iterdir()):
        if not year_dir.is_dir():
            continue
        
        year = year_dir.name
        
        for pdf_file in sorted(year_dir.glob("*.pdf")):
            match = re.search(r'(\d{4}).*?(D[12])', pdf_file.name)
            if not match:
                continue
            
            day = match.group(2)
            
            print(f"\n{'='*50}")
            print(f"{year} {day}")
            print(f"{'='*50}")
            
            extractor = ENEMImageExtractor()
            images = extractor.process_pdf(pdf_file, int(year), day)
            
            if images:
                out_dir = img_base / f"{year}_{day}"
                extractor.save_images(images, out_dir)


if __name__ == "__main__":
    main()
