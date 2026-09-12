"""
Update data/*.json and dados.js with correct image paths.
"""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica")
images_dir = ROOT / "images"
data_dir = ROOT / "data"
dados_path = ROOT / "js" / "dados.js"

# Build image map: {(year, day, numero): image_path}
image_map = {}
for year_dir in sorted(images_dir.iterdir()):
    if not year_dir.is_dir():
        continue
    parts = year_dir.name.split('_')
    if len(parts) != 2:
        continue
    year, day = parts
    for img_file in year_dir.glob("Q*.png"):
        q_num = int(img_file.stem[1:])
        img_path = f"images/{year_dir.name}/{img_file.name}"
        image_map[(year, day, q_num)] = img_path

print(f"Found {len(image_map)} images")

# Update each data/*.json
total_updated = 0
for json_file in sorted(data_dir.glob("*.json")):
    data = json.loads(json_file.read_text(encoding='utf-8'))
    updated = 0
    for q in data:
        year = str(q.get('ano', ''))
        numero = q.get('numero', 0)
        day = 'D1' if 1 <= numero <= 90 else 'D2'
        key = (year, day, numero)
        if key in image_map:
            q['imagem'] = image_map[key]
            updated += 1
    json_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    total_updated += updated
    if updated:
        print(f"  {json_file.name}: {updated} images")

print(f"Total: {total_updated} questions updated across data/*.json")
