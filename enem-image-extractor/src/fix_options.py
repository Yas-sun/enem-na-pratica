"""
Fix questions with missing or image-based options.
Re-extracts from PDFs.
"""

import fitz
import re
import json
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from PDF."""
    doc = fitz.open(str(pdf_path))
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text


def extract_question_options(text: str, q_num: int) -> list:
    """Extract options for a specific question."""
    # Find question block
    pattern = re.compile(
        rf'Questão\s+{q_num:02d}\s*\n(.*?)(?=Questão\s+\d{{1,3}}\s*\n|ENEM\d{{4}}|$)',
        re.DOTALL
    )
    
    match = pattern.search(text)
    if not match:
        # Try without leading zero
        pattern = re.compile(
            rf'Questão\s+{q_num}\s*\n(.*?)(?=Questão\s+\d{{1,3}}\s*\n|ENEM\d{{4}}|$)',
            re.DOTALL
        )
        match = pattern.search(text)
    
    if not match:
        return []
    
    q_text = match.group(1)
    
    # Find options
    options = []
    lines = q_text.split('\n')
    
    for line in lines:
        # Match option pattern: "A text" or "A\ttext"
        opt_match = re.match(r'^([A-E])\s+(.*)', line)
        if opt_match:
            options.append(opt_match.group(2).strip())
    
    # Ensure 5 options
    while len(options) < 5:
        options.append('')
    
    return options[:5]


def main():
    """Main function."""
    pdf_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\pdfs")
    
    # Load dados.js
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    # Find problematic questions
    fixed = 0
    for question in q:
        opts = question.get('opcoes', [])
        
        # Check if options need fixing
        needs_fix = (
            any(not opt for opt in opts) or  # Empty options
            any('images/' in str(opt) or '.png' in str(opt) for opt in opts)  # Image paths
        )
        
        if not needs_fix:
            continue
        
        year = question.get('ano')
        q_num = question.get('numero')
        
        # Determine PDF path
        if 1 <= q_num <= 90:
            day = 'D1'
            caderno = 'CD1'
        else:
            day = 'D2'
            caderno = 'CD7'
        
        pdf_path = pdf_base / str(year) / f"{year}_PV_impresso_{day}_{caderno}.pdf"
        
        if not pdf_path.exists():
            continue
        
        # Extract text and get options
        text = extract_text_from_pdf(pdf_path)
        new_opts = extract_question_options(text, q_num)
        
        if new_opts and any(new_opts):
            question['opcoes'] = new_opts
            fixed += 1
            print(f'Fixed {year} Q{q_num}: {new_opts}')
    
    print(f'\nTotal fixed: {fixed}')
    
    # Write back
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print('Updated dados.js')


if __name__ == "__main__":
    main()
