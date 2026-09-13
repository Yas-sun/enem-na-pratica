"""Update image paths in dados.js to match actual file extensions."""
import json
import re
from pathlib import Path

def main():
    root = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode")
    dados_path = root / "js" / "dados.js"
    images_dir = root / "images"
    
    # Build map of actual image files
    actual_files = {}
    for img_file in images_dir.rglob("*"):
        if img_file.suffix.lower() in ('.png', '.jpg', '.jpeg'):
            # Get relative path from root
            rel = img_file.relative_to(root)
            actual_files[str(rel).replace("\\", "/")] = True
    
    # Read dados.js
    content = dados_path.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', content, re.DOTALL)
    questions = json.loads(m.group(1))
    
    updated = 0
    for q in questions:
        img = q.get('imagem', '')
        if not img:
            continue
        
        # Check if file exists
        img_path = root / img
        if not img_path.exists():
            # Try .jpg if .png doesn't exist
            if img.endswith('.png'):
                jpg_path = img_path.with_suffix('.jpg')
                if jpg_path.exists():
                    q['imagem'] = img.replace('.png', '.jpg')
                    updated += 1
            # Try .png if .jpg doesn't exist
            elif img.endswith('.jpg'):
                png_path = img_path.with_suffix('.png')
                if png_path.exists():
                    q['imagem'] = img.replace('.jpg', '.png')
                    updated += 1
    
    print(f"Updated {updated} image paths")
    
    # Write back
    new_json = json.dumps(questions, ensure_ascii=False, separators=(',', ':'))
    new_content = content[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + content[m.end():]
    dados_path.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")

if __name__ == "__main__":
    main()
