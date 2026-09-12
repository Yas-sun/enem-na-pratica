"""
Complete fix for ENEM question metadata.
Fixes area, disciplina, and subtopico based on ENEM structure.

ENEM Day 1 (D1) Q1-90:
  Q1-45: Linguagens (portugues, ingles, espanhol, literatura, artes)
  Q46-90: Humanas (historia, geografia, filosofia, sociologia)

ENEM Day 2 (D2) Q91-180:
  Q91-135: Natureza (fisica, quimica, biologia)
  Q136-180: Matematica (algebra, geometria, estatistica, probabilidade)
"""

import json
import re
from pathlib import Path


# ENEM structure: question number ranges for each discipline
DISCIPLINE_MAP = {
    # Day 1 - Linguagens
    'portugues': list(range(1, 31)),      # Q1-30
    'ingles': [31, 32, 33, 34, 35],       # Q31-35
    'espanhol': [36, 37, 38, 39, 40],     # Q36-40
    'literatura': list(range(41, 46)),     # Q41-45
    'artes': [],                           # Mixed within linguagens
    
    # Day 1 - Humanas
    'historia': list(range(46, 61)),       # Q46-60
    'geografia': list(range(61, 76)),      # Q61-75
    'filosofia': [76, 77, 78, 79, 80],    # Q76-80
    'sociologia': list(range(81, 86)),     # Q81-85
    
    # Day 2 - Natureza
    'fisica': list(range(91, 111)),        # Q91-110
    'quimica': list(range(111, 126)),      # Q111-125
    'biologia': list(range(126, 136)),     # Q126-135
    
    # Day 2 - Matematica
    'algebra': list(range(136, 151)),      # Q136-150
    'geometria': list(range(151, 166)),    # Q151-165
    'estatistica': list(range(166, 173)),  # Q166-172
    'probabilidade': list(range(173, 181)),# Q173-180
}

# Area for each discipline
AREA_MAP = {
    'portugues': 'linguagens', 'ingles': 'linguagens', 'espanhol': 'linguagens',
    'literatura': 'linguagens', 'artes': 'linguagens',
    'historia': 'humanas', 'geografia': 'humanas', 'filosofia': 'humanas',
    'sociologia': 'humanas',
    'fisica': 'natureza', 'quimica': 'natureza', 'biologia': 'natureza',
    'algebra': 'matematica', 'geometria': 'matematica',
    'estatistica': 'matematica', 'probabilidade': 'matematica',
}


def get_correct_discipline(numero, dia):
    """Get correct discipline based on question number and day."""
    if dia == 1:
        if 1 <= numero <= 45:
            area = 'linguagens'
        elif 46 <= numero <= 90:
            area = 'humanas'
        else:
            return None, None
    elif dia == 2:
        if 91 <= numero <= 135:
            area = 'natureza'
        elif 136 <= numero <= 180:
            area = 'matematica'
        else:
            return None, None
    else:
        return None, None
    
    # Find discipline within area
    for disc, nums in DISCIPLINE_MAP.items():
        if AREA_MAP.get(disc) == area and numero in nums:
            return area, disc
    
    # Default discipline for area
    defaults = {
        'linguagens': 'portugues', 'humanas': 'historia',
        'natureza': 'fisica', 'matematica': 'algebra'
    }
    return area, defaults.get(area, '')


def get_subtopico_for_discipline(discipline, texto):
    """Get appropriate subtopic based on discipline and question text."""
    texto_lower = texto.lower() if texto else ''
    
    subtopic_keywords = {
        'historia': {
            'Brasil Colônia': ['colônia', 'colonial', 'capitanias', 'portugueses'],
            'Brasil Império': ['império', 'dom pedro', 'independência', 'imperial'],
            'República Velha': ['república', 'oligárquica', 'café com leite'],
            'Era Vargas': ['vargas', 'estado novo', 'getúlio'],
            'Regime Militar': ['militar', 'ditadura', 'golpe', 'ai-5'],
            'Guerras Mundiais': ['guerra', 'mundial', '1914', '1939', 'primeira guerra', 'segunda guerra'],
            'Guerra Fria': ['guerra fria', 'urss', 'eua', 'bloco soviético'],
            'Pré-História': ['pré-história', 'neolítico', 'paleolítico'],
            'Civilizações Antigas': ['egito', 'mesopotâmia', 'roma', 'grécia'],
            'Idade Média': ['medieval', 'medieval', 'feudal'],
            'Revolução Francesa': ['revolução francesa', 'liberdade igualdade fraternidade'],
            'Revolução Industrial': ['revolução industrial', 'mecanização'],
            'Direitos Humanos': ['direitos humanos', 'direito', 'liberdade'],
            'Abolicionismo': ['escravo', 'escravidão', 'abolicionismo', 'trabalho escravo'],
            'Redemocratização': ['democracia', 'eleições', 'plebiscito'],
            'Formação do Estado Nacional': ['estado nacional', 'nação', 'soberania'],
            'Descolonização': ['descolonização', 'independência', 'colônia'],
            'Idade Moderna': ['moderna', 'renascimento', 'descobrimentos'],
            'Idade Contemporânea': ['contemporânea', 'globalização', 'mundialização'],
        },
        'geografia': {
            'Geografia do Brasil': ['brasil', 'região', 'nordeste', 'sudeste', 'norte', 'centro-oeste'],
            'Geografia Mundial': ['mundo', 'europa', 'américa', 'áfrica', 'ásia'],
            'Cartografia': ['mapa', 'cartografia', 'escala', 'projeção'],
            'Climatologia': ['clima', 'temperatura', 'chuva', 'fase'],
            'Urbanização': ['urbanização', 'cidade', 'migração', 'metrópole'],
            'Meio Ambiente': ['meio ambiente', 'desmatamento', 'poluição', 'sustentável'],
            'Demografia': ['população', 'natalidade', 'mortalidade', 'crescimento'],
            'Globalização': ['globalização', 'mundialização', 'internacional'],
            'Questão Agrária': ['agrária', 'reforma agrária', 'latifúndio'],
            'Migração': ['migração', 'migrante', 'imigração', 'emigração'],
        },
        'sociologia': {
            'Sociologia Geral': ['sociedade', 'social', 'classe', 'estrutura'],
            'Cidadania': ['cidadão', 'cidadania', 'direito', 'dever'],
            'Cultura': ['cultura', 'tradição', 'costume', 'identidade cultural'],
            'Estratificação Social': ['estratificação', 'desigualdade', 'renda'],
            'Trabalho': ['trabalho', 'emprego', 'desemprego', 'assalariado'],
            'Educação': ['educação', 'escola', 'ensino', 'aprendizagem'],
            'Violência': ['violência', 'crime', 'segurança', 'punição'],
            'Mídia': ['mídia', 'comunicação', 'jornal', 'televisão'],
            'Movimentos Sociais': ['movimento', 'protesto', 'luta', 'greve'],
            'Classe Social': ['classe', 'burguesia', 'proletariado', 'elite'],
        },
        'filosofia': {
            'Filosofia Antiga': ['sócrates', 'platão', 'aristóteles'],
            'Filosofia Moderna': ['descartes', 'kant', 'hegel'],
            'Ética': ['ética', 'moral', 'bem', 'mal', 'justo'],
            'Política': ['política', 'estado', 'governo', 'poder'],
            'Epistemologia': ['conhecimento', 'verdade', 'ciência'],
            'Existencialismo': ['existencialismo', 'existência', 'angústia'],
        },
        'fisica': {
            'Mecânica': ['força', 'movimento', 'velocidade', 'aceleração', 'newton'],
            'Cinemática': ['cinemática', 'deslocamento', 'trajetória'],
            'Dinâmica': ['dinâmica', 'newton', 'lei', 'massa'],
            'Termodinâmica': ['temperatura', 'calor', 'energia', 'entropia', 'garrafa', 'água'],
            'Eletromagnetismo': ['elétric', 'magnét', 'carga', 'campo', 'circuito'],
            'Óptica': ['óptica', 'luz', 'reflexão', 'refração', 'espelho'],
            'Hidrostática': ['pressão', 'fluido', 'líquido', 'volume', 'densidade'],
            'Gravitação': ['gravidade', 'gravitacional', 'queda livre'],
            'Ondas': ['onda', 'frequência', 'amplitude', 'sonora'],
            'Trabalho e Energia': ['trabalho', 'energia', 'potência', 'joule'],
        },
        'quimica': {
            'Química Geral': ['átomo', 'molécula', 'elemento', 'liga', 'tabela periódica'],
            'Reações Químicas': ['reação', 'química', 'combinação', 'decomposição'],
            'Soluções': ['solução', 'solute', 'solvente', 'concentração'],
            'Química Orgânica': ['orgânico', 'carbono', 'hidrocarboneto'],
            'Eletroquímica': ['eletrólise', 'pilha', 'bateria', 'eletrodo'],
            'Acidoses e Bases': ['ácido', 'base', 'ph', 'neutralização'],
            'Estequiometria': ['estequiometria', 'mol', 'massa molar'],
        },
        'biologia': {
            'Citologia': ['célula', 'membrana', 'organela', 'citoplasma'],
            'Genética': ['gene', 'dna', 'hereditariedade', 'cromossomo'],
            'Ecologia': ['ecologia', 'ecossistema', 'biodiversidade', 'cadeia alimentar'],
            'Evolução': ['evolução', 'seleção natural', 'adaptação'],
            'Fisiologia': ['fisiologia', 'sistema', 'órgão', 'função'],
            'Biologia Celular': ['celular', 'célula', 'divisão', 'mitose', 'meiose'],
            'Microbiologia': ['bactéria', 'vírus', 'microorganismo'],
            'Botânica': ['planta', 'fotossíntese', 'flor', 'folha'],
            'Zoologia': ['animal', 'vertebrado', 'invertebrado'],
        },
        'algebra': {
            'Equações': ['equação', 'incógnita', 'solução', 'igualdade'],
            'Funções': ['função', 'gráfico', 'domínio', 'imagem'],
            'Porcentagem': ['porcento', 'porcentagem', '80%', '20%'],
            'Proporcionalidade': ['proporcional', 'razão', 'razão entre'],
            'Regra de Três': ['regra de três', 'proporcional'],
            'Progressão Aritmética': ['pa', 'progressão aritmética', 'razão'],
            'Progressão Geométrica': ['pg', 'progressão geométrica'],
        },
        'geometria': {
            'Geometria Plana': ['triângulo', 'quadrilátero', 'círculo', 'área', 'perímetro'],
            'Geometria Espacial': ['volume', 'sólido', 'cubo', 'esfera', 'cilindro'],
            'Trigonometria': ['seno', 'cosseno', 'tangente', 'ângulo'],
            'Ângulos': ['ângulo', 'graus', 'radiano'],
            'Pitágoras': ['pitágoras', 'hipotenusa', 'cateto'],
            'Semelhança de Triângulos': ['semelhança', 'semelhante', 'proporção'],
        },
        'estatistica': {
            'Estatística': ['estatística', 'média', 'mediana', 'moda', 'desvio'],
            'Gráficos': ['gráfico', 'tabela', 'barras', 'pizza', 'histograma'],
            'Medidas de Tendência Central': ['média', 'mediana', 'moda'],
            'Amostragem': ['amostra', 'amostragem', 'pesquisa'],
            'Interpretação de Dados': ['dados', 'tabela', 'gráfico', 'número'],
        },
        'probabilidade': {
            'Probabilidade': ['probabilidade', 'chance', 'evento', 'sorteio', 'possibilidade'],
            'Espaço Amostral': ['espaço amostral', 'resultado', 'possível'],
            'Evento': ['evento', 'acontecimento', 'ocorrência'],
            'Permutação': ['permutação', 'arranjo', 'combinação', 'ordem'],
        },
        'portugues': {
            'Interpretação de Texto': ['texto', 'interpretação', 'leitura', 'compreensão'],
            'Vozes Verbais': ['verbo', 'verbal', 'conjugação', 'tempo verbal'],
            'Morfologia': ['prefixo', 'sufixo', 'radical', 'morfologia'],
            'Sintaxe': ['sintaxe', 'sujeito', 'predicado', 'objeto'],
            'Semântica': ['sinônimo', 'antônimo', 'polissemia', 'significado'],
            'Pontuação': ['vírgula', 'ponto', 'ponto e vírgula'],
            'Coesão': ['coesão', 'conjunção', 'articulador'],
            'Gêneros Textuais': ['gênero', 'crônica', 'poema', 'notícia', 'editorial'],
            'Figuras de Linguagem': ['metáfora', 'comparação', 'hipérbole', 'ironia'],
            'Movimentos Literários': ['romantismo', 'realismo', 'modernismo'],
            'Norma Culta': ['norma culta', 'gramática', 'regra'],
        },
        'ingles': {
            'Vocabulário Inglês': ['word', 'vocabulary', 'meaning'],
            'Gramática Inglesa': ['verb', 'tense', 'adjective'],
            'Texto Informativo': ['text', 'article', 'passage'],
        },
        'espanhol': {
            'Vocabulário Espanhol': ['palabra', 'vocabulario', 'significado'],
            'Gramática Espanhola': ['verbo', 'tiempo', 'adjetivo'],
        },
        'literatura': {
            'Movimentos Literários': ['romantismo', 'realismo', 'modernismo', 'barroco'],
            'Análise Literária': ['personagem', 'enredo', 'narrador', 'tema'],
            'Figuras de Linguagem': ['metáfora', 'comparação', 'hipérbole'],
        },
        'artes': {
            'Artes Visuais': ['pintura', 'escultura', 'arte', 'quadro'],
            'Música': ['música', 'melodia', 'ritmo', 'canção'],
            'Teatro': ['teatro', 'peça', 'ator', 'cena'],
            'Cinema': ['cinema', 'filme', 'diretor', 'ator'],
        },
    }
    
    discipline_topics = subtopic_keywords.get(discipline, {})
    
    for subtopico, keywords in discipline_topics.items():
        for keyword in keywords:
            if keyword in texto_lower:
                return subtopico
    
    # Default subtopic for discipline
    defaults = {
        'historia': 'Idade Contemporânea',
        'geografia': 'Geografia do Brasil',
        'sociologia': 'Sociologia Geral',
        'filosofia': 'Filosofia Moderna',
        'fisica': 'Mecânica',
        'quimica': 'Química Geral',
        'biologia': 'Citologia',
        'algebra': 'Equações',
        'geometria': 'Geometria Plana',
        'estatistica': 'Estatística',
        'probabilidade': 'Probabilidade',
        'portugues': 'Interpretação de Texto',
        'ingles': 'Texto Informativo',
        'espanhol': 'Texto Informativo',
        'literatura': 'Análise Literária',
        'artes': 'Artes Visuais',
    }
    return defaults.get(discipline, 'Geral')


def main():
    """Main function."""
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    area_fixed = 0
    disc_fixed = 0
    sub_fixed = 0
    
    for question in q:
        num = question.get('numero', 0)
        dia = question.get('dia', 1)
        texto = question.get('texto', '')
        
        # Fix area and discipline
        correct_area, correct_disc = get_correct_discipline(num, dia)
        
        if correct_area and question.get('area') != correct_area:
            question['area'] = correct_area
            area_fixed += 1
        
        if correct_disc and question.get('disciplina') != correct_disc:
            question['disciplina'] = correct_disc
            disc_fixed += 1
        
        # Fix subtopic
        correct_sub = get_subtopico_for_discipline(correct_disc or question.get('disciplina', ''), texto)
        if correct_sub and question.get('subtopico') != correct_sub:
            question['subtopico'] = correct_sub
            sub_fixed += 1
    
    print(f"Fixed: {area_fixed} areas, {disc_fixed} disciplines, {sub_fixed} subtopics")
    
    # Write back
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")


if __name__ == "__main__":
    main()
