"""
Batch extract embedded images from ALL ENEM PDFs using caue-paiva approach.
Only extracts images that are actually embedded in the PDF.
"""

import fitz
import io
from pathlib import Path
from PIL import Image
import re
import json
from typing import Dict, List


class ENEMImageExtractor:
    """Extract ONLY embedded images from ENEM PDFs."""
    
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
    
    def extract_embedded_images(self, doc: fitz.Document, page: fitz.Page, 
                                    q_numbers: List[int]) -> Dict[int, Image.Image]:
        """Extract ONLY embedded images using caue-paiva approach with y-position matching."""
        images = page.get_images()
        
        if not images:
            return {}
        
        result = {}
        
        for img_tuple in images:
            xref = img_tuple[0]
            
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                pix = fitz.Pixmap(image_bytes)
                
                if pix.alpha:
                    try:
                        pix = fitz.Pixmap(pix, 0)
                    except ValueError:
                        continue
                
                if pix.n == 4:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix = pix1
                
                # Get image position on page
                rects = page.get_image_rects(xref)
                if not rects:
                    continue
                
                y_pos = rects[0].y0
                
                # Find question positions using search_for
                q_positions = {}
                for q_num in q_numbers:
                    q_rects = page.search_for(f"Questão {q_num}")
                    if q_rects:
                        q_positions[q_num] = q_rects[0].y0
                    else:
                        q_rects = page.search_for(f"Questão {q_num:02d}")
                        if q_rects:
                            q_positions[q_num] = q_rects[0].y0
                
                if not q_positions:
                    continue
                
                # Find closest question
                closest_q = min(q_positions.keys(), key=lambda q: abs(q_positions[q] - y_pos))
                
                # Only associate if image is below question text
                if y_pos > q_positions[closest_q]:
                    img_data = pix.tobytes("png")
                    pil_img = Image.open(io.BytesIO(img_data))
                    if pil_img.mode != 'RGBA':
                        pil_img = pil_img.convert('RGBA')
                    result[closest_q] = pil_img
                    
            except Exception:
                continue
        
        return result
    
    def process_pdf(self, pdf_path: Path, year: int, day: str) -> Dict[int, Image.Image]:
        """Process a PDF and extract ONLY embedded images."""
        print(f"Processing {pdf_path.name}...")
        
        doc = fitz.open(str(pdf_path))
        all_images = {}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            q_numbers = self.get_question_numbers(page)
            
            if not q_numbers:
                continue
            
            embedded = self.extract_embedded_images(doc, page, q_numbers)
            
            if embedded:
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
            
            img = img.resize((605, 530), Image.LANCZOS)
            img.save(str(filepath), 'PNG')
            saved += 1
        
        print(f"  Saved {saved} images")
        return saved


def main():
    """Process all ENEM PDFs."""
    pdf_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\pdfs")
    output_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\images")
    
    total_images = 0
    
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
                out_dir = output_base / f"{year}_{day}"
                saved = extractor.save_images(images, out_dir)
                total_images += saved
    
    print(f"\nTotal: {total_images} images extracted")


if __name__ == "__main__":
    main()
