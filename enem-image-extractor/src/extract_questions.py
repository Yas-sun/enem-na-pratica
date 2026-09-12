"""
ENEM Question Extractor - Extract all questions from PDFs.
Extracts text, options, and metadata for all questions.
"""

import fitz
import re
import json
from pathlib import Path
from typing import Dict, List, Optional


class ENEMQuestionExtractor:
    """Extract questions from ENEM PDFs."""
    
    def extract_questions_from_page(self, page: fitz.Page) -> List[Dict]:
        """Extract all questions from a single page."""
        text = page.get_text()
        questions = []
        
        # Find all question blocks
        # Pattern: "Questão XX" followed by text and options
        question_pattern = re.compile(
            r'Questão\s+(\d{1,3})\s*\n(.*?)(?=Questão\s+\d{1,3}\s*\n|$)',
            re.DOTALL
        )
        
        for match in question_pattern.finditer(text):
            q_num = int(match.group(1))
            q_text = match.group(2).strip()
            
            if 1 <= q_num <= 180:
                question = self.parse_question_text(q_num, q_text)
                if question:
                    questions.append(question)
        
        return questions
    
    def parse_question_text(self, q_num: int, text: str) -> Optional[Dict]:
        """Parse question text to extract components."""
        # Remove footnotes and page markers
        text = re.sub(r'\*\d+.*?\*', '', text)
        text = re.sub(r'ENEM\d{4}', '', text)
        text = re.sub(r'CADerno.*?AZUL', '', text, flags=re.IGNORECASE)
        
        # Try to find options (A, B, C, D, E)
        options_match = re.search(
            r'([A-E])\s+(.*?)(?=[A-E]\s+|$)',
            text,
            re.DOTALL
        )
        
        if not options_match:
            return None
        
        # Split text into context and question
        parts = text.split('\n')
        
        # Find where options start
        options_start = -1
        for i, part in enumerate(parts):
            if re.match(r'^[A-E]\s+', part):
                options_start = i
                break
        
        if options_start == -1:
            return None
        
        # Extract context (everything before options)
        context_parts = parts[:options_start]
        context = '\n'.join(context_parts).strip()
        
        # Extract options
        options = []
        for part in parts[options_start:]:
            match = re.match(r'^([A-E])\s+(.*)', part)
            if match:
                options.append(match.group(2).strip())
        
        # Ensure we have 5 options
        while len(options) < 5:
            options.append('')
        
        return {
            'numero': q_num,
            'texto': context,
            'opcoes': options[:5]
        }


def main():
    """Main function."""
    pdf_base = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\pdfs")
    
    # Test with 2025 D1
    pdf_path = pdf_base / "2025" / "2025_PV_impresso_D1_CD1.pdf"
    
    doc = fitz.open(str(pdf_path))
    extractor = ENEMQuestionExtractor()
    
    all_questions = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        questions = extractor.extract_questions_from_page(page)
        all_questions.extend(questions)
    
    doc.close()
    
    print(f"Extracted {len(all_questions)} questions")
    for q in all_questions[:5]:
        print(f"\nQ{q['numero']:03d}:")
        print(f"  Text: {q['texto'][:100]}...")
        print(f"  Options: {q['opcoes']}")


if __name__ == "__main__":
    main()
