"""
Fix disciplina + subtopico based on content keywords.
Uses DISC_TO_AREA mapping and SUBTOPIC_KEYWORDS from update_subtopicos.py.
"""

import json
import re
import unicodedata
from pathlib import Path


DISC_TO_AREA = {
    'fisica': 'natureza', 'quimica': 'natureza', 'biologia': 'natureza',
    'historia': 'humanas', 'geografia': 'humanas', 'sociologia': 'humanas', 'filosofia': 'humanas',
    'portugues': 'linguagens', 'ingles': 'linguagens', 'espanhol': 'linguagens',
    'literatura': 'linguagens', 'artes': 'linguagens',
    'algebra': 'matematica', 'geometria': 'matematica',
    'estatistica': 'matematica', 'probabilidade': 'matematica',
}


DISC_KEYWORDS = {
    'fisica': {
        'specific': ['calorimetria', 'equilíbrio térmico', 'termodinâmica',
                      'cinemática', 'dinâmica', 'estática',
                      'eletromagnetismo', 'campo elétrico', 'campo magnético',
                      'circuito elétrico', 'resistência elétrica',
                      'óptica', 'gravitação', 'queda livre',
                      'lei de ohm', 'lei de newton', 'princípio de arquimedes',
                      'mecânica', 'hidrostática', 'empuxo',
                      'processo isotérmico', 'processo adiabático',
                      'calor sensível', 'calor latente',
                      'efeito fotoelétrico', 'efeito doppler',
                      'dualidade onda-partícula', 'radioatividade'],
        'generic': ['velocidade média', 'grandeza escalar', 'grandeza vetorial',
                     'newton', 'joule', 'volt', 'ampere', 'ohm', 'watt', 'hertz'],
    },
    'quimica': {
        'specific': ['tabela periódica', 'liga iônica', 'ligação covalente',
                      'liga metálica', 'eletrólise', 'eletrodo',
                      'estequiometria', 'massa molar', 'número de avogadro',
                      'hidrocarboneto', 'composto orgânico', 'grupo funcional',
                      'redox', 'titulação', 'molaridade',
                      'equilíbrio químico', 'constante de equilíbrio',
                      'eletroquímica', 'pilha galvânica'],
        'generic': ['átomo', 'molécula', 'elemento químico', 'composto químico',
                     'solução aquosa', 'ácido', 'base', 'ph', 'neutralização',
                     'reação química', 'combustão', 'oxidação', 'redução'],
    },
    'biologia': {
        'specific': ['citologia', 'biologia celular', 'genética molecular',
                      'biologia molecular', 'mitose', 'meiose',
                      'ecologia', 'ecossistema', 'biodiversidade',
                      'seleção natural', 'fotossíntese', 'respiração celular',
                      'sistema digestório', 'sistema respiratório',
                      'sistema circulatório', 'sistema nervoso',
                      'sistema imunológico', 'transgênico', 'clonagem',
                      'engenharia genética', 'biotecnologia'],
        'generic': ['célula', 'dna', 'gene', 'cromossomo', 'proteína', 'enzima',
                     'bactéria', 'vírus', 'fungo', 'planta', 'animal',
                     'evolução', 'adaptação', 'metabolismo'],
    },
    'historia': {
        'specific': ['revolução francesa', 'regime militar', 'ditadura militar',
                      'estado novo', 'getúlio vargas', 'república velha',
                      'guerra fria', 'abolicionismo', 'escravatura',
                      'expansão marítima', 'capitanias hereditárias',
                      'tiradentes', 'inconfidência mineira',
                      'segunda guerra mundial', 'primeira guerra mundial',
                      'revolução industrial', 'dom pedro'],
        'generic': ['guerra', 'revolução', 'império', 'colônia', 'república',
                     'ditadura', 'escravidão', 'escravo', 'fazenda',
                     'batalha', 'tratado', 'século', 'período',
                     'história', 'histórico'],
    },
    'geografia': {
        'specific': ['cartografia', 'escala cartográfica', 'fuso horário',
                      'placa tectônica', 'bacia hidrográfica',
                      'zoneamento ecológico', 'unidade de conservação',
                      'desertificação', 'reforma agrária', 'bioma',
                      'cerrado', 'caatinga', 'mata atlântica', 'amazônia'],
        'generic': ['clima', 'relevo', 'população', 'migração', 'urbanização',
                     'meio ambiente', 'desmatamento', 'poluição',
                     'energia', 'petróleo', 'agricultura', 'pecuária',
                     'indústria', 'comércio', 'globalização'],
    },
    'sociologia': {
        'specific': ['movimento dos sem terra', 'mst', 'mtst',
                      'organização não governamental', 'ong',
                      'participação cidadã', 'democracia participativa',
                      'movimento operário', 'movimento estudantil',
                      'movimento feminista', 'movimento negro',
                      'inclusão social', 'exclusão social',
                      'estratificação social', 'hegemonia cultural',
                      'indústria cultural', 'assistência social'],
        'generic': ['desigualdade', 'cidadão', 'cidadania', 'classe social',
                     'identidade', 'tradição', 'escola', 'ensino',
                     'emprego', 'desemprego', 'crime', 'segurança',
                     'mídia', 'movimento social', 'protesto', 'greve',
                     'família', 'religião', 'gênero', 'consumismo'],
    },
    'filosofia': {
        'specific': ['sócrates', 'platão', 'aristóteles', 'descartes', 'kant',
                      'hegel', 'sartre', 'foucault', 'existencialismo'],
        'generic': ['filosofia', 'filosófico', 'ética', 'moral',
                     'conhecimento', 'verdade', 'liberdade', 'igualdade',
                     'justiça', 'razão', 'pensamento'],
    },
    'portugues': {
        'specific': ['voz ativa', 'voz passiva', 'concordância verbal',
                      'regência verbal', 'crase', 'ponto e vírgula',
                      'sintaxe', 'morfologia', 'semântica',
                      'norma culta', 'gramática'],
        'generic': ['texto', 'interpretação', 'leitura', 'compreensão',
                     'verbo', 'sujeito', 'predicado', 'oração',
                     'sinônimo', 'antônimo', 'metáfora', 'ironia',
                     'coesão', 'coerência'],
    },
    'ingles': {
        'specific': ['english', 'vocabulary', 'grammar', 'reading comprehension'],
        'generic': ['inglês', 'english', 'text in english'],
    },
    'espanhol': {
        'specific': ['español', 'vocabulario', 'gramática', 'comprensión'],
        'generic': ['espanhol', 'español', 'texto en español'],
    },
    'literatura': {
        'specific': ['romantismo', 'realismo', 'modernismo', 'barroco',
                      'arcadismo', 'parnasianismo', 'simbolismo',
                      'literalismo', 'contemporâneo'],
        'generic': ['literatura', 'poema', 'poesia', 'conto', 'novela',
                     'crônica', 'autor', 'obra'],
    },
    'artes': {
        'specific': ['arte visual', 'música', 'teatro', 'dança',
                      'pintura', 'escultura', 'fotografia'],
        'generic': ['arte', 'artístico', 'artística', 'cultura visual'],
    },
    'algebra': {
        'specific': ['equação do 1º grau', 'equação do 2º grau',
                      'sistema linear', 'progressão aritmética',
                      'progressão geométrica', 'juros simples',
                      'juros compostos', 'regra de três',
                      'função afim', 'função quadrática',
                      'função exponencial', 'função logarítmica'],
        'generic': ['equação', 'incógnita', 'função', 'porcentagem',
                     'razão', 'proporção', 'logaritmo'],
    },
    'geometria': {
        'specific': ['teorema de pitágoras', 'trigonometria',
                      'geometria analítica', 'plano cartesiano',
                      'semelhança de triângulos', 'congruência de triângulos',
                      'lei dos senos', 'lei dos cossenos'],
        'generic': ['triângulo', 'quadrilátero', 'círculo', 'circunferência',
                     'área', 'perímetro', 'volume', 'ângulo',
                     'polígono', 'poliedro', 'vértice'],
    },
    'estatistica': {
        'specific': ['estatística descritiva', 'estatística inferencial',
                      'tabela de frequência', 'medidas de tendência central',
                      'medidas de dispersão', 'correlação', 'regressão'],
        'generic': ['média', 'mediana', 'moda', 'desvio padrão',
                     'histograma', 'amostra', 'pesquisa', 'dados'],
    },
    'probabilidade': {
        'specific': ['evento independente', 'evento dependente',
                      'permutação', 'arranjo', 'combinação',
                      'distribuição binomial', 'distribuição normal'],
        'generic': ['probabilidade', 'chance', 'evento', 'espaço amostral',
                     'moeda', 'dado', 'sorteio'],
    },
}


def detect_discipline(texto):
    """Detect discipline using weighted scoring. Returns (disc, score)."""
    if not texto:
        return None, 0
    
    tl = texto.lower()
    best_disc = None
    best_score = 0
    
    for disc, data in DISC_KEYWORDS.items():
        score = 0
        for kw in data.get('specific', []):
            if kw.lower() in tl:
                score += 3
        for kw in data.get('generic', []):
            if kw.lower() in tl:
                score += 1
        
        if score > best_score:
            best_score = score
            best_disc = disc
    
    if best_score >= 5:
        return best_disc, best_score
    return None, 0


def main():
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    disc_fixed = 0
    area_fixed = 0
    
    for question in q:
        texto = question.get('texto', '')
        if not texto:
            continue
        
        new_disc, score = detect_discipline(texto)
        if not new_disc:
            continue
        
        old_disc = question.get('disciplina', '')
        if new_disc != old_disc:
            question['disciplina'] = new_disc
            question['area'] = DISC_TO_AREA.get(new_disc, '')
            disc_fixed += 1
    
    print(f"Fixed {disc_fixed} disciplines")
    
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")


if __name__ == "__main__":
    main()
