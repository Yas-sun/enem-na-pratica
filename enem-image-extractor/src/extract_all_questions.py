"""
Extract all ENEM questions from PDFs and update dados.js.
"""

import fitz
import re
import json
from pathlib import Path
from typing import Dict, List, Optional


# ENEM question ranges by area (D1: 1-90, D2: 91-180)
ENEM_RANGES = {
    'linguagens': {'D1': (1, 45), 'D2': (91, 135)},
    'humanas': {'D1': (46, 90), 'D2': (136, 180)},
    'natureza': {'D2': (91, 135)},
    'matematica': {'D2': (136, 180)}
}


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from PDF."""
    doc = fitz.open(str(pdf_path))
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text


def extract_questions_from_text(text: str, year: int, day: str) -> List[Dict]:
    """Extract questions from text."""
    questions = []
    
    # Find all question blocks
    pattern = re.compile(
        r'Questão\s+(\d{1,3})\s*\n(.*?)(?=Questão\s+\d{1,3}\s*\n|ENEM\d{4}|$)',
        re.DOTALL
    )
    
    for match in pattern.finditer(text):
        q_num = int(match.group(1))
        q_text = match.group(2).strip()
        
        if 1 <= q_num <= 180:
            question = parse_question(q_num, q_text, year, day)
            if question:
                questions.append(question)
    
    return questions


def parse_question(q_num: int, text: str, year: int, day: str) -> Optional[Dict]:
    """Parse question text to extract components."""
    # Remove footnotes and page markers
    text = re.sub(r'\*\d+.*?\*', '', text)
    text = re.sub(r'ENEM\d{4}', '', text)
    text = re.sub(r'CADerno.*?AZUL', '', text, flags=re.IGNORECASE)
    text = re.sub(r'LINGUAGENS.*?AZUL', '', text, flags=re.IGNORECASE)
    text = re.sub(r'CIÊNCIAS.*?AZUL', '', text, flags=re.IGNORECASE)
    text = re.sub(r'MATEMÁTICA.*?AZUL', '', text, flags=re.IGNORECASE)
    
    # Split into lines
    lines = text.split('\n')
    
    # Find where options start
    options_start = -1
    for i, line in enumerate(lines):
        if re.match(r'^[A-E]\s+', line):
            options_start = i
            break
    
    if options_start == -1:
        return None
    
    # Extract context (everything before options)
    context_lines = lines[:options_start]
    context = '\n'.join(context_lines).strip()
    
    # Extract options
    options = []
    for line in lines[options_start:]:
        match = re.match(r'^([A-E])\s+(.*)', line)
        if match:
            options.append(match.group(2).strip())
    
    # Ensure we have 5 options
    while len(options) < 5:
        options.append('')
    
    # Determine question number range
    if 1 <= q_num <= 90:
        q_range = f"{q_num:02d}"
    else:
        q_range = f"{q_num:03d}"
    
    return {
        'id': f"{'L' if day == 'D1' and q_num <= 45 else 'H' if day == 'D1' and q_num <= 90 else 'N' if day == 'D2' and q_num <= 135 else 'M'}{year}_{q_range}",
        'ano': year,
        'numero': q_num,
        'texto': context,
        'opcoes': options[:5]
    }


def main():
    """Main function."""
    pdf_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\pdfs")
    
    # Test with 2025 D1
    pdf_path = pdf_base / "2025" / "2025_PV_impresso_D1_CD1.pdf"
    
    print(f"Processing {pdf_path.name}...")
    text = extract_text_from_pdf(pdf_path)
    questions = extract_questions_from_text(text, 2025, "D1")
    
    print(f"Extracted {len(questions)} questions")
    
    # Show first 5 questions
    for q in questions[:5]:
        print(f"\nQ{q['numero']:03d}:")
        print(f"  ID: {q['id']}")
        print(f"  Text: {q['texto'][:100]}...")
        print(f"  Options: {q['opcoes']}")


if __name__ == "__main__":
    main()
