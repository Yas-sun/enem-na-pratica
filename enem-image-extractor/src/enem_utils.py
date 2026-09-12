"""
ENEM-specific utilities for question extraction.

Handles ENEM exam structure, question numbering, and layout patterns.
"""

from typing import Dict, List, Tuple
from pathlib import Path
import re


# ENEM exam structure by year
ENEM_STRUCTURE = {
    # 2009-2016: Old format
    "old": {
        "D1": {
            "areas": {
                "humanas": (1, 45),      # Ciências Humanas e suas Tecnologias
                "natureza": (46, 90)     # Ciências da Natureza e suas Tecnologias
            }
        },
        "D2": {
            "areas": {
                "linguagens": (91, 135),  # Linguagens, Códigos e suas Tecnologias
                "matematica": (136, 180)  # Matemática e suas Tecnologias
            }
        }
    },
    # 2017+: New format
    "new": {
        "D1": {
            "areas": {
                "linguagens": (1, 45),    # Linguagens, Códigos e suas Tecnologias
                "humanas": (46, 90)       # Ciências Humanas e suas Tecnologias
            }
        },
        "D2": {
            "areas": {
                "natureza": (91, 135),    # Ciências da Natureza e suas Tecnologias
                "matematica": (136, 180)  # Matemática e suas Tecnologias
            }
        }
    }
}

# PDF naming conventions by year
PDF_NAMING = {
    # 2014-2019: /educacao_basica/enem/provas/{year}/
    "old_site": {
        "D1": "{year}_PV_impresso_D1_CD1.pdf",
        "D2": "{year}_PV_impresso_D2_CD5.pdf"  # or CD7
    },
    # 2020+: /enem/provas_e_gabaritos/
    "new_site": {
        "D1": "{year}_PV_impresso_D1_CD1.pdf",
        "D2": "{year}_PV_impresso_D2_CD7.pdf"
    }
}


def get_enem_format(year: int) -> str:
    """Return 'old' or 'new' format based on year."""
    return "old" if year <= 2016 else "new"


def get_question_range(year: int, day: str) -> Tuple[int, int]:
    """Get question number range for a given year and day."""
    fmt = get_enem_format(year)
    areas = ENEM_STRUCTURE[fmt][day]["areas"]
    
    all_ranges = list(areas.values())
    return (all_ranges[0][0], all_ranges[-1][1])


def get_areas_for_page(year: int, day: str, page_num: int, 
                       total_pages: int) -> List[str]:
    """
    Determine which areas are covered on a specific page.
    
    Returns list of area names (e.g., ['humanas', 'natureza']).
    """
    fmt = get_enem_format(year)
    areas = ENEM_STRUCTURE[fmt][day]["areas"]
    
    q_start, q_end = get_question_range(year, day)
    questions_per_page = (q_end - q_start + 1) / total_pages
    
    page_q_start = q_start + int(page_num * questions_per_page)
    page_q_end = q_start + int((page_num + 1) * questions_per_page)
    
    page_areas = []
    for area_name, (area_start, area_end) in areas.items():
        # Check if this area overlaps with the page's question range
        if page_q_start <= area_end and page_q_end >= area_start:
            page_areas.append(area_name)
    
    return page_areas


def get_pdf_filename(year: int, day: str) -> str:
    """Get the standard PDF filename for ENEM."""
    if year >= 2020:
        pattern = PDF_NAMING["new_site"]
    else:
        pattern = PDF_NAMING["old_site"]
    
    return pattern[day].format(year=year)


def parse_question_number(text: str) -> int:
    """
    Extract question number from text.
    
    Handles formats like:
    - "1." or "1)"
    - "Questão 1"
    - "QUESTÃO 1"
    - "01" (with leading zero)
    """
    patterns = [
        r'(\d{1,3})\.\s',
        r'(\d{1,3})\)',
        r'[Qq]uestão\s+(\d{1,3})',
        r'QUESTÃO\s+(\d{1,3})',
        r'^(\d{1,3})$',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 180:
                return num
    
    return 0


def get_output_path(base_dir: Path, year: int, day: str, q_num: int) -> Path:
    """
    Get the output path for a question image.
    
    Returns: {base_dir}/{year}/{day}/Q{q_num}.png
    """
    return base_dir / str(year) / day / f"Q{q_num}.png"


def validate_question_number(q_num: int, year: int, day: str) -> bool:
    """Check if a question number is valid for the given year and day."""
    q_start, q_end = get_question_range(year, day)
    return q_start <= q_num <= q_end
