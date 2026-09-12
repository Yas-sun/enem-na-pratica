"""
Download and parse official ENEM gabaritos from Mundo Educação.
"""

import requests
import fitz  # PyMuPDF
import re
import json
from pathlib import Path


# Gabarito URLs from Mundo Educação (Caderno 1 Azul - CD1)
GABARITO_URLS = {
    2009: {
        "D1": "http://download.inep.gov.br/educacao_basica/enem/downloads/2009/gabaritodia1.pdf",
        "D2": "http://download.inep.gov.br/educacao_basica/enem/downloads/2009/gabaritodia2.pdf"
    },
    2010: {
        "D1": "http://download.inep.gov.br/educacao_basica/enem/provas/2010/AZUL_Sabado_GAB.pdf",
        "D2": "http://download.inep.gov.br/educacao_basica/enem/provas/2010/AZUL_Domingo_GAB.pdf"
    },
    2011: {
        "D1": "http://download.inep.gov.br/educacao_basica/enem/gabaritos/2011/01_AZUL_GABARITO.pdf",
        "D2": "http://download.inep.gov.br/educacao_basica/enem/gabaritos/2011/07_AZUL_GABARITO.pdf"
    },
    2012: {
        "D1": "http://download.inep.gov.br/educacao_basica/enem/gabaritos/2012/dia1_azul.pdf",
        "D2": "http://download.inep.gov.br/educacao_basica/enem/gabaritos/2012/dia2_azul.pdf"
    },
    2013: {
        "D1": "https://vestibular.mundoeducacao.uol.com.br/baixar/52b139a480e1e002f6ad85ca0185fb5b.pdf",
        "D2": "https://vestibular.mundoeducacao.uol.com.br/baixar/01c45be7886682f4cc0e419b2b317bdb.pdf"
    },
    2014: {
        "D1": "https://vestibular.mundoeducacao.uol.com.br/baixar/d24d92df048f5e90d21b54923a30b033.pdf",
        "D2": "https://vestibular.mundoeducacao.uol.com.br/baixar/5fffe453d3a9b7dce5349c99668d9f18.pdf"
    },
    2015: {
        "D1": "https://vestibular.mundoeducacao.uol.com.br/baixar/85425a4729997b421e26a9ff37e4e19b.pdf",
        "D2": "https://vestibular.mundoeducacao.uol.com.br/baixar/435dc91d1b37becd170d7e9bf37dda33.pdf"
    },
    2016: {
        "D1": "https://vestibular.mundoeducacao.uol.com.br/baixar/a8c660f4f485a0641ff417d5c54a2e35.pdf",
        "D2": "https://vestibular.mundoeducacao.uol.com.br/baixar/90d51308b6694baa987a2331450b8f52.pdf"
    },
    2017: {
        "D1": "https://vestibular.mundoeducacao.uol.com.br/baixar/aa489690c316964079f40831ac00c4d9.pdf",
        "D2": "https://vestibular.mundoeducacao.uol.com.br/baixar/42057bcbb4e9c24c81a0d1cbcf99f1d0.pdf"
    },
    2018: {
        "D1": "https://vestibular.mundoeducacao.uol.com.br/baixar/84c5e603f87c4d223cdc06ca340ff979.pdf",
        "D2": "https://vestibular.mundoeducacao.uol.com.br/baixar/71123fa1ac7466ab0422d94fa1e430ec.pdf"
    },
    2019: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2019/11/gabarito-1-dia-caderno-1-azul-aplicacao-regular.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2019/11/gabarito-2-dia-caderno-7-azul-aplicacao-regular.pdf"
    },
    2020: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2021/01/gabarito-azul-1-dia-atualizado.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2021/01/2-dia-caderno7-azul-gabarito.pdf"
    },
    2021: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2021/12/gabarito-azul.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2021/12/gabarito-azul-d2.pdf"
    },
    2022: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2022/11/1-dia-gabarito-caderno-1-azul-enem-2022.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2022/11/2-dia-gabarito-caderno-7-azul-enem-2022.pdf"
    },
    2023: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2023/11/gabarito-1-dia-azul-enem-2023.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2023/11/gabarito-2-dia-azul-enem-2023.pdf"
    },
    2024: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2024/11/gabarito-1-dia-azul-enem-2024.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2024/11/gabarito-2-dia-azul-enem-2024.pdf"
    },
    2025: {
        "D1": "https://static.mundoeducacao.uol.com.br/vestibular/2025/11/gabarito-azul-dia-1-enem-2025.pdf",
        "D2": "https://static.mundoeducacao.uol.com.br/vestibular/2025/11/enem-2025-2-dia-caderno-azul-gabarito.pdf"
    }
}


class GabaritoParser:
    """Parse gabarito PDFs to extract answers."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_pdf(self, url: str, filename: str) -> Path:
        """Download PDF from URL."""
        filepath = self.output_dir / filename
        if filepath.exists():
            print(f"  Already exists: {filename}")
            return filepath
        
        print(f"  Downloading: {filename}")
        try:
            response = self.session.get(url, timeout=30, verify=False)
            response.raise_for_status()
            filepath.write_bytes(response.content)
            return filepath
        except Exception as e:
            print(f"  Error downloading {filename}: {e}")
            return None
    
    def parse_gabarito_pdf(self, pdf_path: Path, day: str) -> dict:
        """Parse gabarito PDF to extract answers."""
        if not pdf_path or not pdf_path.exists():
            return {}
        
        doc = fitz.open(str(pdf_path))
        gabarito = {}
        
        for page in doc:
            text = page.get_text()
            
            # D1: questions 1-90, D2: questions 91-180
            # Try multiple regex patterns
            
            # Pattern 1: "91\nD" (number on separate line)
            matches = re.findall(r'(\d{1,3})\n([A-E])', text)
            for num, resp in matches:
                num = int(num)
                if 1 <= num <= 180:
                    gabarito[num] = resp
            
            # Pattern 2: "91 D" or "91-D" (same line)
            matches = re.findall(r'(\d{1,3})\s*[-.\s]\s*([A-E])', text)
            for num, resp in matches:
                num = int(num)
                if 1 <= num <= 180:
                    gabarito[num] = resp
            
            # Pattern 3: "Questão 91: D"
            matches = re.findall(r'[Qq]ues[t]ão\s+(\d{1,3})\s*[-:\s]+\s*([A-E])', text)
            for num, resp in matches:
                num = int(num)
                if 1 <= num <= 180:
                    gabarito[num] = resp
        
        doc.close()
        
        # Filter based on day
        if day == "D1":
            return {k: v for k, v in gabarito.items() if 1 <= k <= 90}
        else:  # D2
            return {k: v for k, v in gabarito.items() if 91 <= k <= 180}
    
    def download_all(self) -> dict:
        """Download all gabaritos."""
        all_gabaritos = {}
        
        for year, days in GABARITO_URLS.items():
            print(f"\n{'='*50}")
            print(f"{year}")
            print(f"{'='*50}")
            
            for day, url in days.items():
                print(f"\n{day}:")
                filename = f"{year}_GB_{day}_CD1.pdf"
                pdf_path = self.download_pdf(url, filename)
                
                if pdf_path:
                    gabarito = self.parse_gabarito_pdf(pdf_path, day)
                    key = f"{year}_{day}"
                    all_gabaritos[key] = gabarito
                    print(f"  Found {len(gabarito)} answers")
        
        return all_gabaritos


def main():
    """Main function."""
    output_dir = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\gabaritos_oficiais")
    
    parser = GabaritoParser(output_dir)
    
    print("Downloading official ENEM gabaritos...")
    gabaritos = parser.download_all()
    
    # Save gabaritos to JSON
    output_file = output_dir / "gabaritos_oficiais.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gabaritos, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(gabaritos)} gabaritos to {output_file}")
    
    # Print summary
    for key, gab in sorted(gabaritos.items()):
        print(f"{key}: {len(gab)} answers")


if __name__ == "__main__":
    main()
