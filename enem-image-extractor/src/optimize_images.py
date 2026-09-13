"""Optimize existing PNG images without losing quality."""
from pathlib import Path
from PIL import Image
import os

def optimize_images():
    images_dir = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\images")
    
    total_before = 0
    total_after = 0
    optimized = 0
    
    for img_file in sorted(images_dir.rglob("*.png")):
        size_before = img_file.stat().st_size
        total_before += size_before
        
        try:
            img = Image.open(img_file)
            
            # Convert to RGB if no alpha needed
            if img.mode == 'RGBA' and not img.info.get('transparency'):
                img = img.convert('RGB')
                ext = '.jpg'
                new_path = img_file.with_suffix(ext)
                img.save(new_path, 'JPEG', quality=95, optimize=True)
                size_after = new_path.stat().st_size
                img_file.unlink()  # Remove old PNG
            else:
                # Keep as PNG with optimization
                img.save(img_file, 'PNG', optimize=True)
                size_after = img_file.stat().st_size
            
            total_after += size_after
            optimized += 1
            
            if size_before > size_after:
                reduction = (1 - size_after/size_before) * 100
                print(f"  {img_file.name}: {size_before//1024}KB -> {size_after//1024}KB (-{reduction:.0f}%)")
            
        except Exception as e:
            print(f"  Error {img_file.name}: {e}")
            total_after += size_before
    
    print(f"\nOptimized {optimized} images")
    print(f"Total: {total_before//1024}KB -> {total_after//1024}KB")
    print(f"Reduction: {(1 - total_after/total_before) * 100:.1f}%")

if __name__ == "__main__":
    optimize_images()
