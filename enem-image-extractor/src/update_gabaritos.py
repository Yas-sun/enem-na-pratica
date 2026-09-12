"""Update dados.js with official gabaritos."""

import json
import re
from pathlib import Path


def main():
    # Load gabaritos
    gab_file = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\gabaritos_oficiais\gabaritos_oficiais.json")
    gabaritos = json.loads(gab_file.read_text())
    
    # Load dados.js
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    # Update gabaritos
    updated = 0
    for question in q:
        year = question.get('ano')
        q_num = question.get('numero', 0)
        
        # Determine day
        if 1 <= q_num <= 90:
            day = 'D1'
            gab_key = f'{year}_D1'
        else:
            day = 'D2'
            gab_key = f'{year}_D2'
        
        # Get gabarito
        if gab_key in gabaritos:
            gab = gabaritos[gab_key].get(str(q_num))
            if gab:
                question['gabarito'] = gab
                updated += 1
    
    print(f'Updated {updated} gabaritos')
    
    # Write back
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print('Updated dados.js')


if __name__ == "__main__":
    main()
