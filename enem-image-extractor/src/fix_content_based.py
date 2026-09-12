"""
Fix ENEM question metadata using CONTENT-based discipline assignment.
Area is determined by question number + day (reliable).
Discipline is determined by content analysis (keyword matching).
Subtopic is determined by content + discipline.
"""

import json
import re
from pathlib import Path


# Area by question number and day (ENEM structure)
def get_area(numero, dia):
    """Get area based on question number and day."""
    if dia == 1:
        if 1 <= numero <= 45:
            return 'linguagens'
        elif 46 <= numero <= 90:
            return 'humanas'
    elif dia == 2:
        if 91 <= numero <= 135:
            return 'natureza'
        elif 136 <= numero <= 180:
            return 'matematica'
    return None


# Discipline detection by content keywords
DISCIPLINE_KEYWORDS = {
    # Linguagens
    'portugues': [
        'verbo', 'conjugação', 'tempo verbal', 'sujeito', 'predicado',
        'objeto direto', 'objeto indireto', 'oração', 'período',
        'ponto e vírgula', 'vírgula', 'dois pontos', 'ponto final',
        'sinônimo', 'antônimo', 'polissemia', 'hipônimo',
        'metáfora', 'hipérbole', 'ironia', 'comparação',
        'gênero textual', 'crônica', 'poema', 'conto', 'novela',
        'romantismo', 'realismo', 'modernismo', 'barroco',
        'regência', 'concordância', 'crase', 'acentuação',
        'coordenação', 'subordinação', 'oração absoluta',
        'sujeito simples', 'sujeito composto', 'predicado simples',
        'voz ativa', 'voz passiva', 'voz reflexiva',
        'aspecto verbai', 'modo indicativo', 'modo subjuntivo',
        'artigo', 'demonstrativo', 'indefinido', 'numeral',
        'adjetivo', 'advérbio', 'preposição', 'conjunção',
        'locução adverbial', 'locução prepositiva',
    ],
    'ingles': [
        'verb to be', 'present simple', 'past simple', 'present continuous',
        'future tense', 'present perfect', 'past continuous',
        'adjective', 'adverb', 'pronoun', 'preposition',
        'although', 'because', 'while', 'during', 'before', 'after',
        'if clause', 'conditional', 'passive voice', 'reported speech',
        'relative clause', 'phrasal verb',
    ],
    'espanhol': [
        'verbo ser', 'verbo estar', 'verbo haber', 'pretérito',
        'subjuntivo', 'imperativo', 'futuro', 'condicional',
        'pronombre', 'artículo', 'preposición', 'conjunción',
    ],
    'literatura': [
        'personagem', 'enredo', 'narrador', 'foco narrativo',
        'tema', 'motivo', 'figura linguagem', 'metáfora',
        'romantismo', 'realismo', 'naturalismo', 'modernismo',
        'parnasianismo', 'simbolismo', 'concretismo',
        'soneto', 'ode', 'elegia', 'lira', 'balada',
        'monólogo', 'diálogo', 'monologo',
    ],
    'artes': [
        'pintura', 'escultura', 'arte', 'quadro', 'música',
        'teatro', 'cinema', 'dança', 'fotografia',
        'impressionismo', 'cubismo', 'surrealismo', ' expressionismo',
        'grafite', 'street art', 'arte digital',
    ],
    
    # Humanas
    'historia': [
        'guerra', 'revolução', 'império', 'colônia', 'república',
        'independência', 'ditadura', 'golpe', 'eleições',
        'escravidão', 'escravo', 'abolicionismo',
        'dom pedro', 'getúlio', 'vargas',
        'primeira guerra', 'segunda guerra', 'guerra fria',
        'nazismo', 'fascismo', 'comunismo', 'liberalismo',
        'medieval', 'renascimento', 'descobrimentos',
        'iluminismo', 'absolutismo', 'feudalismo',
        'estado nacional', 'soberania', 'nação',
        'século xvi', 'século xvii', 'século xviii', 'século xix',
        'século xx', 'século xxi',
        'ditadura militar', 'regime militar', 'ai-5',
        'redemocratização', 'constituição',
        'trabalho escravo', 'fazenda', 'fazendeiro',
        'bloqueio', 'fiscalização', 'organizações não governamentais',
    ],
    'geografia': [
        'região', 'nordeste', 'sudeste', 'centro-oeste', 'norte',
        'clima', 'temperatura', 'chuva', 'seca', 'inundaç',
        'relevo', 'montanha', 'planície', 'planalto',
        'vegetação', 'floresta', 'cerrado', 'caatinga', 'mata atlântica',
        'população', 'migração', 'imigração', 'urbanização',
        'globalização', 'bloco econômico', 'mercocul',
        'meio ambiente', 'desmatamento', 'poluição',
        'reforma agrária', 'latifúndio', 'minifúndio',
        'energia', 'petróleo', 'biocombustível',
        'transporte', 'ferrovia', 'porto', 'aeroporto',
        'mapa', 'escala', 'cartografia', 'coordenadas',
        'fuso horário', 'meridiano', 'paralelo',
        'placa tectônica', 'terremoto', 'vulcão',
        'questão agrária', 'questão ambiental',
    ],
    'sociologia': [
        'sociedade', 'social', 'classe', 'desigualdade',
        'cidadão', 'cidadania', 'direito', 'dever',
        'cultura', 'identidade', 'tradição',
        'educação', 'escola', 'ensino',
        'trabalho', 'emprego', 'desemprego',
        'violência', 'crime', 'segurança',
        'mídia', 'comunicação', 'jornal',
        'movimento social', 'protesto', 'greve',
        'família', 'religião', 'gênero',
        'consumismo', 'consumidor',
        'conscientização', 'direitos sociais', 'direitos trabalhistas',
        'ministério público', 'ação judicial',
        'organização não governamental', 'ong',
        'pastoral', 'defesa dos direitos',
    ],
    'filosofia': [
        'filosofia', 'filósofo', 'sócrates', 'platão', 'aristóteles',
        'descartes', 'kant', 'hegel', 'marx', 'nietzsche',
        'existencialismo', 'racionalismo', 'empirismo',
        'ética', 'moral', 'bem', 'mal', 'justo',
        'política', 'estado', 'governo', 'poder',
        'verdade', 'conhecimento', 'realidade',
        'liberdade', 'igualdade', 'justiça',
        'cogito ergo sum', 'method',
    ],
    
    # Natureza
    'fisica': [
        'força', 'newton', 'lei', 'massa', 'aceleração',
        'velocidade', 'deslocamento', 'trajetória',
        'energia', 'trabalho', 'potência', 'joule',
        'temperatura', 'calor', 'calorimetria', 'equilíbrio térmico',
        'garrafa térmica', 'água fria', 'água quente',
        'circuito', 'resistência', 'corrente', 'tensão', 'voltagem',
        'campo elétrico', 'campo magnético', 'eletromagnetismo',
        'luz', 'reflexão', 'refração', 'espelho', 'lente',
        'onda', 'frequência', 'amplitude', 'sonora',
        'pressão', 'fluido', 'líquido', 'gás', 'densidade',
        'gravidade', 'gravitacional', 'queda livre',
        'cinemática', 'dinâmica', 'estática',
        'entropia', 'termodinâmica', 'máquina térmica',
        'resistência elétrica', 'lei de ohm',
        ' Semiconductor', 'diodo', 'transistor',
        'relatividade', 'quântica', 'fóton',
        'arquimedes', 'empuxo', 'flutuação',
        'velocidade média', 'velocidade instantânea',
        'sentido do movimento', 'referencial',
        'sistema de unidades', 'unidade de medida',
        'grandeza escalar', 'grandeza vetorial',
    ],
    'quimica': [
        'átomo', 'molécula', 'elemento', 'liga metálica',
        'tabela periódica', 'grupo', 'período',
        'ligação iônica', 'ligação covalente', 'ligação metálica',
        'reação química', 'combinação', 'decomposição', 'dupla troca',
        'solução', 'solute', 'solvente', 'concentração',
        'ácido', 'base', 'ph', 'neutralização',
        'eletrólise', 'pilha', 'bateria', 'eletrodo',
        'estequiometria', 'mol', 'massa molar',
        'orgânico', 'carbono', 'hidrocarboneto',
        'polímero', 'plástico', 'biodiesel',
        'combustível', 'etanol', 'gasolina',
        'poluição', 'sustentabilidade',
    ],
    'biologia': [
        'célula', 'membrana', 'organela', 'citoplasma',
        'dna', 'rna', 'gene', 'cromossomo', 'hereditariedade',
        'mitose', 'meiose', 'divisão celular',
        'ecologia', 'ecossistema', 'cadeia alimentar', 'biodiversidade',
        'evolução', 'seleção natural', 'adaptação', 'darwin',
        'fotossíntese', 'respiração celular', 'fermentação',
        'sistema digestório', 'sistema respiratório', 'sistema circulatório',
        'sistema nervoso', 'sistema endócrino', 'sistema imunológico',
        'bactéria', 'vírus', 'fungo', 'protista',
        'planta', 'animal', 'vertebrado', 'invertebrado',
        'bioma', 'cerrado', 'amazônia', 'mata atlântica',
        'desmatamento', 'conservação', 'extinção',
        'transgênico', 'clonagem', 'engenharia genética',
    ],
    
    # Matematica
    'algebra': [
        'equação', 'incógnita', 'solução', 'igualdade',
        'função', 'gráfico', 'domínio', 'imagem',
        'porcento', 'porcentagem', 'desconto', 'acréscimo',
        'razão', 'proporção', 'proporcional',
        'progressão aritmética', 'razão da pa',
        'progressão geométrica', 'razão da pg',
        'juros simples', 'juros compostos',
        'sistema linear', 'matriz', 'determinante',
        'logaritmo', 'potenciação', 'radiciação',
    ],
    'geometria': [
        'triângulo', 'quadrilátero', 'círculo', 'circunferência',
        'área', 'perímetro', 'volume',
        'pitágoras', 'hipotenusa', 'cateto',
        'seno', 'cosseno', 'tangente', 'ângulo',
        'semelhança', 'congruência',
        'plano cartesiano', 'coordenada',
        'polígono', 'poliedro', 'cubo', 'esfera', 'cilindro',
        'pirâmide', 'cone', 'paralelepípedo',
        'diagonal', 'lado', 'vértice',
    ],
    'estatistica': [
        'média', 'mediana', 'moda',
        'gráfico', 'tabela', 'histograma',
        'desvio padrão', 'variância', 'amplitude',
        'pesquisa', 'amostra', 'censo',
        'probabilidade', 'chance', 'evento',
        'espaço amostral', 'permutação', 'arranjo', 'combinação',
        'Box Plot', 'diagrama',
    ],
    'probabilidade': [
        'probabilidade', 'chance', 'evento', 'sorteio',
        'espaço amostral', 'resultado possível',
        'evento certo', 'evento impossível',
        'dependente', 'independente',
        'permutação', 'arranjo', 'combinação',
        'árvore de decisão', 'tabela de frequência',
    ],
}


def detect_discipline(texto, area):
    """Detect discipline based on question text content."""
    if not texto:
        return None
    
    texto_lower = texto.lower()
    
    # Get disciplines for this area
    area_disciplines = {
        'linguagens': ['portugues', 'ingles', 'espanhol', 'literatura', 'artes'],
        'humanas': ['historia', 'geografia', 'sociologia', 'filosofia'],
        'natureza': ['fisica', 'quimica', 'biologia'],
        'matematica': ['algebra', 'geometria', 'estatistica', 'probabilidade'],
    }
    
    disciplines = area_disciplines.get(area, [])
    
    # Score each discipline
    scores = {}
    for disc in disciplines:
        keywords = DISCIPLINE_KEYWORDS.get(disc, [])
        score = sum(1 for kw in keywords if kw.lower() in texto_lower)
        scores[disc] = score
    
    if not scores:
        return None
    
    # Return discipline with highest score
    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return best
    
    return None


# Subtopic detection
SUBTOPIC_KEYWORDS = {
    'historia': {
        'Brasil Colônia': ['colônia', 'colonial', 'capitanias', 'portugueses', 'brasil colonial'],
        'Brasil Império': ['império', 'dom pedro', 'independência', 'imperial', 'brasil império'],
        'República Velha': ['república', 'oligárquica', 'café com leite', 'república velha'],
        'Era Vargas': ['vargas', 'estado novo', 'getúlio', 'era vargas'],
        'Regime Militar': ['militar', 'ditadura', 'golpe', 'ai-5', 'regime militar'],
        'Guerras Mundiais': ['primeira guerra', 'segunda guerra', 'guerra mundial', '1914', '1939'],
        'Guerra Fria': ['guerra fria', 'urss', 'eua', 'bloco soviético', 'bloco ocidental'],
        'Pré-História': ['pré-história', 'neolítico', 'paleolítico'],
        'Civilizações Antigas': ['egito', 'mesopotâmia', 'roma', 'grécia'],
        'Idade Média': ['medieval', 'feudalismo', 'feudal'],
        'Revolução Francesa': ['revolução francesa', 'liberdade igualdade fraternidade'],
        'Revolução Industrial': ['revolução industrial', 'mecanização'],
        'Direitos Humanos': ['direitos humanos', 'direito', 'liberdade'],
        'Abolicionismo': ['escravo', 'escravidão', 'abolicionismo', 'trabalho escravo', 'fazenda'],
        'Redemocratização': ['democracia', 'eleições', 'plebiscito', 'constituição'],
        'Formação do Estado Nacional': ['estado nacional', 'nação', 'soberania'],
        'Descolonização': ['descolonização', 'independência', 'colônia'],
        'Idade Moderna': ['moderna', 'renascimento', 'descobrimentos'],
        'Idade Contemporânea': ['contemporânea', 'globalização', 'mundialização', 'século xx', 'século xix'],
    },
    'geografia': {
        'Geografia do Brasil': ['brasil', 'região', 'nordeste', 'sudeste', 'norte', 'centro-oeste'],
        'Geografia Mundial': ['mundo', 'europa', 'américa', 'áfrica', 'ásia'],
        'Cartografia': ['mapa', 'cartografia', 'escala', 'projeção', 'coordenada'],
        'Climatologia': ['clima', 'temperatura', 'chuva', 'seca'],
        'Urbanização': ['urbanização', 'cidade', 'migração', 'metrópole'],
        'Meio Ambiente': ['meio ambiente', 'desmatamento', 'poluição', 'sustentável'],
        'Demografia': ['população', 'natalidade', 'mortalidade', 'crescimento'],
        'Globalização': ['globalização', 'mundialização', 'internacional'],
        'Questão Agrária': ['agrária', 'reforma agrária', 'latifúndio'],
        'Migração': ['migração', 'migrante', 'imigração', 'emigração'],
    },
    'sociologia': {
        'Sociologia Geral': ['sociedade', 'social', 'classe', 'estrutura'],
        'Cidadania': ['cidadão', 'cidadania', 'direito', 'dever', 'conscientização'],
        'Cultura': ['cultura', 'tradição', 'costume', 'identidade cultural'],
        'Estratificação Social': ['estratificação', 'desigualdade', 'renda'],
        'Trabalho': ['trabalho', 'emprego', 'desemprego', 'assalariado', 'trabalhador'],
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
        'Mecânica': ['força', 'newton', 'lei', 'massa', 'aceleração'],
        'Cinemática': ['cinemática', 'deslocamento', 'trajetória', 'velocidade'],
        'Dinâmica': ['dinâmica', 'newton', 'lei', 'força'],
        'Termodinâmica': ['temperatura', 'calor', 'energia', 'entropia', 'garrafa', 'água', 'equilíbrio térmico', 'calorimetria'],
        'Eletromagnetismo': ['elétric', 'magnét', 'carga', 'campo', 'circuito', 'corrente', 'tensão'],
        'Óptica': ['óptica', 'luz', 'reflexão', 'refração', 'espelho', 'lente'],
        'Hidrostática': ['pressão', 'fluido', 'líquido', 'volume', 'densidade', 'arquimedes', 'empuxo'],
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


def get_subtopico(discipline, texto):
    """Get subtopic based on discipline and question text."""
    if not texto or not discipline:
        return ''
    
    texto_lower = texto.lower()
    discipline_topics = SUBTOPIC_KEYWORDS.get(discipline, {})
    
    for subtopico, keywords in discipline_topics.items():
        for keyword in keywords:
            if keyword.lower() in texto_lower:
                return subtopico
    
    # Default subtopics
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
        
        # Fix area based on number + day
        correct_area = get_area(num, dia)
        if correct_area and question.get('area') != correct_area:
            question['area'] = correct_area
            area_fixed += 1
        
        # Fix discipline based on content
        current_area = question.get('area', '')
        correct_disc = detect_discipline(texto, current_area)
        if correct_disc and question.get('disciplina') != correct_disc:
            question['disciplina'] = correct_disc
            disc_fixed += 1
        
        # Fix subtopic based on content + discipline
        current_disc = question.get('disciplina', '')
        correct_sub = get_subtopico(current_disc, texto)
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
