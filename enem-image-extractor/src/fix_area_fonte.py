"""Fix area based on fonte field, then re-run content-based discipline detection."""

import json
import re
from pathlib import Path


def get_area_from_fonte(fonte):
    """Extract correct area from fonte field."""
    if 'Natureza' in fonte:
        return 'natureza'
    elif 'Humanas' in fonte:
        return 'humanas'
    elif 'Linguagens' in fonte or 'Línguas' in fonte:
        return 'linguagens'
    elif 'Matematica' in fonte or 'Matemática' in fonte:
        return 'matematica'
    return None


def main():
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    area_fixed = 0
    for question in q:
        fonte = question.get('fonte', '')
        correct_area = get_area_from_fonte(fonte)
        if correct_area and question.get('area') != correct_area:
            question['area'] = correct_area
            area_fixed += 1
    
    print(f"Fixed {area_fixed} areas from fonte")
    
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")


if __name__ == "__main__":
    main()
