"""
Verify image-question association for ENEM PDFs.
"""

import fitz
import re
from pathlib import Path
from PIL import Image


def verify_images(pdf_path: Path, images_dir: Path):
    """Verify if images are associated with correct questions."""
    print(f"\n{'='*60}")
    print(f"Verifying: {pdf_path.name}")
    print(f"{'='*60}")
    
    doc = fitz.open(str(pdf_path))
    
    # Get all images in directory
    extracted = {}
    if images_dir.exists():
        for f in images_dir.glob('Q*.png'):
            match = re.match(r'Q(\d+)\.png', f.name)
            if match:
                q_num = int(match.group(1))
                extracted[q_num] = f
    
    print(f"Extracted images: {len(extracted)}")
    
    # For each page, check if images match questions
    issues = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # Find question numbers on this page
        q_matches = re.findall(r'Questão\s+(\d{1,3})', text)
        if not q_matches:
            continue
        
        questions = [int(q) for q in q_matches]
        
        # Find images on this page
        imgs = page.get_images()
        if not imgs:
            continue
        
        # Check each image
        for img in imgs:
            xref = img[0]
            rects = page.get_image_rects(xref)
            if not rects:
                continue
            
            y_pos = rects[0].y0
            
            # Find closest question
            closest_q = None
            min_dist = float('inf')
            
            for q in questions:
                q_rects = page.search_for(f'Questão {q:02d}')
                if not q_rects:
                    q_rects = page.search_for(f'Questão {q}')
                
                if q_rects:
                    q_y = q_rects[0].y0
                    dist = y_pos - q_y
                    if dist > 0 and dist < min_dist:
                        min_dist = dist
                        closest_q = q
            
            if closest_q:
                # Check if image exists for this question
                if closest_q not in extracted:
                    issues.append(f"Page {page_num+1}: Q{closest_q:03d} has image in PDF but not extracted")
    
    doc.close()
    
    if issues:
        print(f"\nISSUES ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nAll images correctly associated!")
    
    return issues


def main():
    """Main function."""
    pdf_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\pdfs")
    img_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\images")
    
    all_issues = []
    
    # Verify 2025 D1
    pdf_path = pdf_base / "2025" / "2025_PV_impresso_D1_CD1.pdf"
    img_dir = img_base / "2025_D1"
    issues = verify_images(pdf_path, img_dir)
    all_issues.extend(issues)
    
    # Verify 2025 D2
    pdf_path = pdf_base / "2025" / "2025_PV_impresso_D2_CD7.pdf"
    img_dir = img_base / "2025_D2"
    issues = verify_images(pdf_path, img_dir)
    all_issues.extend(issues)
    
    print(f"\n{'='*60}")
    print(f"TOTAL ISSUES: {len(all_issues)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
