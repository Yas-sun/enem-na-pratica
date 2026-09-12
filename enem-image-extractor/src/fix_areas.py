"""
Fix area/discipline assignments based on ENEM structure.
D1 Q1-45: linguagens
D1 Q46-90: humanas
D2 Q91-135: natureza
D2 Q136-180: matematica
"""

import json
import re
from pathlib import Path


# Correct discipline mapping by question number
AREA_BY_NUM = {
    'linguagens': {
        'portugues': list(range(1, 31)),  # Q1-30
        'ingles': [31, 32, 33, 34, 35],   # Q31-35
        'espanhol': [36, 37, 38, 39, 40], # Q36-40
        'literatura': list(range(41, 46)), # Q41-45
    },
    'humanas': {
        'historia': list(range(46, 61)),   # Q46-60
        'geografia': list(range(61, 76)),  # Q61-75
        'filosofia': [76, 77, 78, 79, 80], # Q76-80
        'sociologia': list(range(81, 86)), # Q81-85
    },
    'natureza': {
        'fisica': list(range(91, 111)),    # Q91-110
        'quimica': list(range(111, 126)),  # Q111-125
        'biologia': list(range(126, 136)), # Q126-135
    },
    'matematica': {
        'algebra': list(range(136, 151)),  # Q136-150
        'geometria': list(range(151, 166)), # Q151-165
        'estatistica': list(range(166, 173)), # Q166-172
        'probabilidade': list(range(173, 181)), # Q173-180
    }
}


def get_correct_discipline(num, dia):
    """Get correct discipline based on ENEM structure."""
    if dia == 1:
        if 1 <= num <= 45:
            area = 'linguagens'
        elif 46 <= num <= 90:
            area = 'humanas'
        else:
            return None, None
    
    elif dia == 2:
        if 91 <= num <= 135:
            area = 'natureza'
        elif 136 <= num <= 180:
            area = 'matematica'
        else:
            return None, None
    else:
        return None, None
    
    # Find discipline within area
    for disc, nums in AREA_BY_NUM.get(area, {}).items():
        if num in nums:
            return area, disc
    
    # Default discipline for area
    defaults = {'linguagens': 'portugues', 'humanas': 'historia', 
                'natureza': 'fisica', 'matematica': 'algebra'}
    return area, defaults.get(area, '')


def main():
    """Main function."""
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    area_fixed = 0
    disc_fixed = 0
    
    for question in q:
        num = question.get('numero', 0)
        dia = question.get('dia', 1)
        
        correct_area, correct_disc = get_correct_discipline(num, dia)
        
        if correct_area and question.get('area') != correct_area:
            question['area'] = correct_area
            area_fixed += 1
        
        if correct_disc and question.get('disciplina') != correct_disc:
            question['disciplina'] = correct_disc
            disc_fixed += 1
    
    print(f"Fixed {area_fixed} areas, {disc_fixed} disciplines")
    
    # Write back
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")


if __name__ == "__main__":
    main()
