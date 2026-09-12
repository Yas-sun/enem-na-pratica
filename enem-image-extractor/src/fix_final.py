"""
Final fix: Use keywords + context to set area, disciplina, subtopico.
Area is determined by content keywords (not question number).
"""

import json
import re
from pathlib import Path


DISC_TO_AREA = {
    'fisica': 'natureza', 'quimica': 'natureza', 'biologia': 'natureza',
    'historia': 'humanas', 'geografia': 'humanas', 'sociologia': 'humanas', 'filosofia': 'humanas',
    'portugues': 'linguagens', 'ingles': 'linguagens', 'espanhol': 'linguagens',
    'literatura': 'linguagens', 'artes': 'linguagens',
    'algebra': 'matematica', 'geometria': 'matematica',
    'estatistica': 'matematica', 'probabilidade': 'matematica',
}

# Very specific keywords - each discipline has UNIQUE keywords
DISCIPLINE_KEYWORDS = {
    'fisica': [
        'calorimetria', 'equilíbrio térmico', 'garrafa térmica',
        'termodinâmica', 'entropia', 'máquina térmica',
        'cinemática', 'dinâmica', 'estática',
        'eletromagnetismo', 'campo elétrico', 'campo magnético',
        'circuito elétrico', 'resistência elétrica',
        'óptica', 'reflexão', 'refração', 'espelho', 'lente',
        'ondas', 'frequência', 'amplitude',
        'gravitação', 'queda livre', 'velocidade', 'aceleração',
        'força', 'newton', 'massa', 'peso',
        'energia cinética', 'energia potencial', 'energia mecânica',
        'trabalho de uma força', 'potência', 'joule', 'watt',
        'volt', 'ampere', 'ohm',
        'relatividade', 'quântica', 'física moderna',
        'radioatividade', 'fissão', 'fusão',
        'semicondutor', 'transistor', 'diodo',
        'referencial inercial', 'referencial não inercial',
        'grandeza escalar', 'grandeza vetorial',
        'processo isotérmico', 'processo adiabático',
        'processo isobárico', 'processo isocórico',
        'calor sensível', 'calor latente',
        'carga elétrica', 'lei de coulomb',
        'potencial elétrico', 'capacitância',
        'transformador', 'gerador',
        'efeito fotoelétrico', 'efeito doppler',
        'dualidade onda-partícula',
        'mecânica', 'hidrostática', 'empuxo', 'arquimedes',
        'velocidade média', 'velocidade instantânea',
        'sentido do movimento', 'referencial',
        'sistema de unidades', 'unidade de medida',
    ],
    'historia': [
        'revolução francesa', 'declaração dos direitos', 'bastilha',
        'liberdade igualdade fraternidade',
        'revolução industrial', 'mecanização',
        'regime militar', 'ditadura militar', 'ai-5',
        'estado novo', 'getúlio vargas',
        'república velha', 'café com leite', 'coronelismo',
        'política dos governadores', 'primeira república',
        'guerra fria', 'bloco soviético', 'urss',
        'capitalismo', 'socialismo', 'comunismo',
        'fascismo', 'nazismo', 'liberalismo',
        'imperialismo', 'colonialismo', 'descolonização',
        'abolicionismo', 'escravidão', 'trabalho escravo',
        'reforma protestante', 'contrarreforma', 'inquisição',
        'expansão marítima', 'navegação', 'descobrimentos',
        'capitanias hereditárias', 'administração colonial',
        'revolução inglesa', 'revolução americana',
        'guerra de independência', 'constituição',
        'plebiscito', 'referendo',
        'tiradentes', 'inconfidência mineira',
        'revolução de 30',
        'segunda guerra mundial', 'primeira guerra mundial',
        'queda do muro', 'revolução de 1989',
        'revolução cubana', 'revolução mexicana',
        'independência do brasil', 'dom pedro',
    ],
    'geografia': [
        'cartografia', 'escala cartográfica', 'projeção cartográfica',
        'fuso horário', 'linha do equador', 'meridiano', 'paralelo',
        'placa tectônica', 'bacia hidrográfica',
        'zoneamento ecológico', 'reserva legal',
        'unidade de conservação', 'parque nacional',
        'desertificação', 'degradação ambiental',
        'globalização', 'mundialização',
        'reforma agrária', 'latifúndio', 'minifúndio',
        'questão agrária', 'questão ambiental',
        'bioma', 'cerrado', 'caatinga', 'mata atlântica', 'amazônia',
        'semiárido', 'litoral', 'interior',
        'fronteira', 'divisa', 'limite',
        'clima', 'temperatura', 'chuva', 'seca',
        'região', 'nordeste', 'sudeste', 'sul', 'norte', 'centro-oeste',
        'população', 'migração', 'imigração',
        'urbanização', 'metrópole', 'cidade',
        'meio ambiente', 'desmatamento', 'poluição',
        'energia', 'petróleo', 'biocombustível',
        'transporte', 'ferrovia', 'porto', 'aeroporto',
        'mapa', 'escala', 'coordenada',
        'bloco econômico', 'mercosul', 'onu', 'fmi', 'omc',
        'desenvolvimento sustentável', 'sustentabilidade',
        'preservação', 'conservação',
        'agricultura', 'pecuária', 'mineração',
        'indústria', 'comércio', 'serviços',
        'relevo', 'planície', 'planalto', 'montanha',
        'vegetação', 'floresta',
        'demografia', 'natalidade', 'mortalidade',
    ],
    'quimica': [
        'tabela periódica', 'liga iônica', 'ligação covalente', 'liga metálica',
        'eletrólise', 'eletrodo',
        'estequiometria', 'mol', 'massa molar',
        'hidrocarboneto', 'composto orgânico',
        'grupo funcional',
        'redox', 'oxidação', 'redução',
        'galvanoplastia', 'corrosão',
        'destilação', 'cristalização', 'filtração',
        'titulação', 'molaridade', 'molalidade', 'normalidade', 'diluição',
        'massa atômica', 'massa molecular',
        'número de avogadro',
        'gas ideal', 'equação de estado',
        'entalpia', 'energia de ativação',
        'velocidade de reação', 'equilíbrio químico',
        'constante de equilíbrio', 'ph', 'indicador ácido',
        'eletroquímica', 'pilha galvânica', 'bateria', 'cela eletroquímica',
        'ácido', 'base', 'sal',
        'reagente', 'produto', 'reactante',
        'combustão',
        'proteína', 'carboidrato', 'lipídio',
        'fermentação',
    ],
    'biologia': [
        'mitose', 'meiose', 'divisão celular',
        'cromossomo', 'gene', 'dna', 'rna',
        'engenharia genética', 'transgênico',
        'clonagem', 'biotecnologia', 'ogm',
        'seleção natural', 'darwin', 'evolução', 'adaptação', 'especiação',
        'fotossíntese', 'respiração celular', 'fermentação',
        'citologia', 'biologia celular', 'organela',
        'membrana plasmática', 'núcleo celular', 'citoplasma', 'ribossomo', 'mitocôndria',
        'sistema digestório', 'sistema respiratório', 'sistema circulatório',
        'sistema nervoso', 'sistema endócrino', 'sistema imunológico',
        'sistema reprodutor', 'sistema esquelético', 'sistema muscular',
        'anatomia', 'histologia', 'embriologia',
        'genética molecular', 'biologia molecular',
        'ecologia', 'ecossistema', 'cadeia alimentar',
        'biodiversidade', 'conservação', 'extinção',
        'bioma', 'cerrado', 'amazônia', 'mata atlântica',
        'desmatamento', 'degradação', 'preservação',
        'população', 'comunidade', 'bióceno',
        'fator ecológico', 'fator limitante',
        'sucessão ecológica', 'pirâmide ecológica',
        'teia alimentar', 'fluxo de energia',
        'ciclo do carbono', 'ciclo da água', 'ciclo do nitrogênio',
        'fixação de nitrogênio', 'bactéria nitrogenada',
        'mutação', 'alelo', 'genótipo', 'fenótipo',
        'homozigoto', 'heterozigoto', 'dominante', 'recessivo',
        'diabetes', 'câncer', 'aids', 'malária',
        'antibiótico', 'vacina', 'imunidade',
        'hemograma', 'hemácias', 'leucócitos', 'plaquetas', 'hemoglobina', 'anticorpo', 'antígeno',
        'bactéria', 'vírus', 'fungo', 'protista',
        'planta', 'animal', 'vertebrado', 'invertebrado',
    ],
    'sociologia': [
        'movimento dos sem terra', 'mst', 'mtst',
        'organização não governamental', 'ong',
        'pastoral da terra', 'defesa dos direitos',
        'conscientização', 'direitos trabalhistas', 'direitos sociais',
        'política pública', 'participação cidadã', 'democracia participativa',
        'movimento operário', 'movimento estudantil',
        'movimento feminista', 'movimento negro',
        'movimento ambientalista',
        'inclusão social', 'exclusão social',
        'mobilidade social', 'estratificação social',
        'desigualdade social', 'desigualdade de renda',
        'hegemonia cultural', 'indústria cultural',
        'globalização cultural', 'universalização',
        'assistência social', 'política de saúde',
        'política educacional', 'política habitacional',
        'serviço público', 'seguridade social',
        'norma social', 'controle social',
        'sociabilidade', 'interação social',
        'ideologia', 'hegemonia', 'dominação', 'resistência',
        'qualidade de vida', 'bem-estar social',
        'consumismo', 'consumidor', 'consumidorismo',
        'trabalhador', 'assalariado', 'exploração',
        'opressão', 'marginalização', 'exclusão', 'desigualdade', 'pobreza', 'riqueza',
    ],
    'filosofia': [
        'cogito ergo sum', 'materialismo histórico', 'alienação',
        'sociedade civil', 'estado democrático',
        'contratualismo', 'soberania popular',
        'direito natural', 'direito positivo',
        'utilitarismo', 'deontologia', 'virtude',
        'epistemologia', 'metafísica', 'ontologia', 'cosmologia',
        'filosofia da linguagem', 'linguagem', 'signo',
        'filosofia da mente', 'consciência', 'intencionalidade',
        'filosofia da ciência', 'paradigma', 'falsificação',
        'filosofia da história', 'historicidade',
        'fenomenologia', 'hermenêutica', 'deconstructivismo',
        'pós-modernidade', 'pós-estruturalismo',
        'escolástica', 'tomismo', 'neoplatonismo',
        'estoicismo', 'epicurismo', 'cinismo',
        'racionalismo', 'empirismo', 'idealismo',
        'pragmatismo', 'neopositivismo',
        'marxismo', 'anarquismo', 'liberalismo',
        'comunitarismo', 'cosmopolitismo',
        'bioética', 'eutanásia', 'aborto', 'pena de morte',
        'justiça social', 'direitos humanos',
        'sócrates', 'platão', 'aristóteles',
        'descartes', 'kant', 'hegel', 'marx', 'nietzsche',
        'sartre', 'foucault', 'existencialismo',
        'nihilismo', 'absurdo', 'angústia',
        'ser', 'nada', 'essência', 'existência',
        'método', 'dialética',
        'verdade', 'conhecimento', 'ciência',
        'lógica', 'raciocínio', 'argumentação',
        'pensamento', 'pensador', 'filósofo', 'filosofia',
        'ética', 'moral', 'bem', 'mal', 'justo',
        'política', 'estado', 'governo', 'poder',
        'liberdade', 'igualdade', 'justiça',
        'existencialismo', 'razão', 'racionalidade',
    ],
    'portugues': [
        'voz ativa', 'voz passiva', 'voz reflexiva',
        'tempo verbal', 'modo indicativo', 'modo subjuntivo', 'condicional', 'imperativo',
        'ponto e vírgula', 'dois pontos', 'ponto final',
        'vírgula', 'ponto de interrogação', 'ponto de exclamação',
        'crase', 'acentuação', 'ortografia',
        'concordância', 'regência',
        'coordenação', 'subordinação', 'oração absoluta',
        'sujeito simples', 'sujeito composto',
        'predicado simples', 'predicado composto',
        'objeto direto', 'objeto indireto',
        'objeto prepositivo', 'complemento nominal', 'adjunto adnominal',
        'advérbio', 'locução adverbial', 'locução prepositiva',
        'oração subordinada',
        'período simples', 'período composto',
        'norma culta', 'gramática', 'regra gramatical',
        'linguagem formal', 'linguagem informal',
        'variação linguística', 'gíria', 'calão',
        'semântica', 'sintaxe', 'morfologia',
        'fonologia', 'fonética',
        'denotação', 'conotação',
        'metáfora', 'hipérbole', 'ironia', 'comparação',
        'personificação', 'metonímia', 'sinédoque',
        'antítese', 'paradoxo', 'símile',
        'prosopopeia', 'apóstrofe', 'eufemismo',
        'catacrese',
        'figura de linguagem', 'figura de sentido',
        'redação', 'produção textual',
        'redação dissertativa', 'redação narrativa', 'redação descritiva',
        'tese', 'argumento', 'contra-argumento',
        'introdução', 'desenvolvimento', 'conclusão',
        'coesão', 'coerência', 'coerência textual',
        'texto', 'leitura', 'interpretação', 'compreensão',
        'verbo', 'sujeito', 'predicado', 'objeto', 'oração', 'período',
        'palavra', 'vocabulário', 'significado', 'significado',
        'sinônimo', 'antônimo', 'polissemia', 'homônimo',
        'prefixo', 'sufixo', 'radical',
        'gênero textual', 'tipo textual',
        'crônica', 'poema', 'conto', 'novela',
        'romantismo', 'realismo', 'modernismo', 'barroco',
        'editorial', 'crítica', 'notícia', 'reportagem',
        'charge', 'cartaz', 'anúncio',
        'linguagem', 'comunicação', 'discurso',
        'tom', 'estilo', 'artifício',
        'retórica', 'persuasão',
    ],
    'algebra': [
        'equação do 1º grau', 'equação do 2º grau',
        'sistema linear', 'sistema de equações',
        'matriz', 'determinante', 'inversa',
        'logaritmo', 'potenciação', 'radiciação',
        'progressão aritmética', 'razão da pa',
        'progressão geométrica', 'razão da pg',
        'juros simples', 'juros compostos',
        'regra de três', 'regra de três simples', 'regra de três composta',
        'produtos notáveis', 'quadrado perfeito',
        'soma de cubos', 'diferença de cubos',
        'fatoração', 'mmc', 'mdc',
        'expressão algébrica', 'monômio', 'polinômio',
        'coeficiente', 'grau do polinômio',
        'função afim', 'função do 1º grau',
        'função quadrática', 'função do 2º grau',
        'função exponencial', 'função logarítmica',
        'função trigonométrica',
        'inequação', 'sistema de inequações',
        'proporção', 'proporcionalidade direta', 'proporcionalidade inversa',
        'porcentagem', 'desconto', 'acréscimo',
        'juros', 'capital', 'taxa', 'tempo',
        'equação', 'incógnita', 'solução', 'igualdade',
        'função', 'gráfico', 'domínio', 'imagem',
        'variável', 'constante',
    ],
    'geometria': [
        'pitágoras', 'teorema de pitágoras',
        'triângulo retângulo', 'hipotenusa', 'cateto',
        'semelhança de triângulos', 'congruência de triângulos',
        'teorema de tales',
        'trigonometria', 'seno', 'cosseno', 'tângente',
        'plano cartesiano', 'coordenada', 'vetor',
        'geometria analítica',
        'sólido geométrico', 'poliedro',
        'cubo', 'esfera', 'cilindro', 'cone', 'pirâmide',
        'volume', 'área de superfície',
        'ângulo', 'grau', 'radiano',
        'mediatriz', 'bissetriz', 'altura', 'mediana',
        'baricentro', 'incentro', 'circuncentro', 'ortocentro',
        'circunscrita', 'inscrita',
        'translação', 'rotação', 'reflexão', 'dilatação', 'simetria',
        'quadrilátero', 'trapézio', 'losango',
        'retângulo', 'quadrado',
        'polígono', 'diagonal', 'lado', 'vértice',
        'ponto', 'reta', 'plano',
    ],
    'estatistica': [
        'estatística', 'estatístico',
        'população', 'amostra', 'censo',
        'pesquisa', 'coleta de dados',
        'tabela de frequência', 'distribuição de frequência',
        'histograma', 'polígono de frequência', 'ogive',
        'box plot', 'diagrama de caule e folhas',
        'média', 'mediana', 'moda',
        'desvio padrão', 'variância', 'amplitude',
        'amplitude total', 'amplitude interquartil',
        'medidas de tendência central',
        'medidas de dispersão',
        'percentil', 'quartil', 'decil',
        'correlação', 'regressão',
        'coeficiente de correlação', 'linha de regressão',
        'frequência absoluta', 'frequência relativa', 'frequência percentual',
    ],
    'probabilidade': [
        'probabilidade', 'probabilística',
        'evento', 'espaço amostral', 'resultado',
        'evento certo', 'evento impossível', 'evento aleatório',
        'evento independente', 'evento dependente',
        'permutação', 'arranjo', 'combinação',
        'árvore de decisão', 'tabela de frequência',
        'probabilidade clássica', 'probabilidade frequencista',
        'probabilidade condicional', 'probabilidade conjunta',
        'teorema de bayes', 'distribuição binomial',
        'distribuição normal',
        'lógica combinatória', 'regra do produto', 'regra da soma',
        'moeda', 'dado', 'baralho', 'loteria', 'mega-sena',
        'quina', 'lotofácil',
    ],
}


def detect_discipline(texto):
    """Detect discipline using weighted keyword matching."""
    if not texto:
        return None
    
    tl = texto.lower()
    
    best_disc = None
    best_score = 0
    
    for disc, keywords in DISCIPLINE_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw.lower() in tl:
                score += 1
        
        if score > best_score:
            best_score = score
            best_disc = disc
    
    if best_score >= 3:
        return best_disc
    return None


SUBTOPIC_KEYWORDS = {
    'historia': {
        'Brasil Colônia': [('colônia', 3), ('colonial', 3), ('capitanias', 5)],
        'Brasil Império': [('império', 3), ('dom pedro', 5), ('independência', 3)],
        'República Velha': [('república', 2), ('café com leite', 8)],
        'Era Vargas': [('vargas', 3), ('estado novo', 5), ('getúlio', 5)],
        'Regime Militar': [('militar', 3), ('ditadura', 3), ('ai-5', 8)],
        'Guerras Mundiais': [('primeira guerra', 8), ('segunda guerra', 8)],
        'Guerra Fria': [('guerra fria', 10), ('urss', 5)],
        'Pré-História': [('pré-história', 8), ('neolítico', 8), ('paleolítico', 8)],
        'Civilizações Antigas': [('egito', 5), ('mesopotâmia', 8)],
        'Idade Média': [('medieval', 8), ('feudalismo', 8)],
        'Revolução Francesa': [('revolução francesa', 10), ('bastilha', 8)],
        'Revolução Industrial': [('revolução industrial', 10)],
        'Abolicionismo': [('escravo', 3), ('escravidão', 5), ('abolicionismo', 8), ('trabalho escravo', 8)],
        'Direitos Humanos': [('direitos humanos', 10)],
        'Redemocratização': [('democracia', 3), ('eleições', 3)],
        'Idade Contemporânea': [('contemporânea', 5), ('século xx', 5)],
    },
    'geografia': {
        'Geografia do Brasil': [('brasil', 2), ('nordeste', 3), ('sudeste', 3)],
        'Geografia Mundial': [('mundo', 2), ('europa', 3), ('américa', 3)],
        'Cartografia': [('mapa', 3), ('cartografia', 8), ('coordenada', 5)],
        'Climatologia': [('clima', 5), ('temperatura', 3), ('chuva', 5)],
        'Urbanização': [('urbanização', 8), ('cidade', 3)],
        'Meio Ambiente': [('meio ambiente', 8), ('desmatamento', 5), ('poluição', 3)],
        'Demografia': [('população', 5), ('natalidade', 8)],
        'Globalização': [('globalização', 8), ('mundialização', 8)],
        'Questão Agrária': [('reforma agrária', 10), ('latifúndio', 8)],
        'Migração': [('migração', 8), ('imigração', 8)],
    },
    'sociologia': {
        'Sociologia Geral': [('sociedade', 5), ('social', 2), ('classe', 2)],
        'Cidadania': [('cidadão', 5), ('cidadania', 8), ('direito', 2), ('conscientização', 5)],
        'Cultura': [('cultura', 5), ('tradição', 3)],
        'Estratificação Social': [('estratificação', 8), ('desigualdade', 5)],
        'Trabalho': [('trabalho', 2), ('emprego', 3), ('desemprego', 5)],
        'Educação': [('educação', 5), ('escola', 3), ('ensino', 3)],
        'Violência': [('violência', 5), ('crime', 3)],
        'Mídia': [('mídia', 8), ('comunicação', 3)],
        'Movimentos Sociais': [('movimento', 3), ('protesto', 5), ('greve', 5)],
    },
    'filosofia': {
        'Filosofia Antiga': [('sócrates', 10), ('platão', 10), ('aristóteles', 10)],
        'Filosofia Moderna': [('descartes', 10), ('kant', 10), ('hegel', 10)],
        'Ética': [('ética', 8), ('moral', 5)],
        'Política': [('política', 5), ('estado', 2), ('governo', 2), ('poder', 2)],
        'Epistemologia': [('conhecimento', 5), ('verdade', 5)],
        'Existencialismo': [('existencialismo', 10), ('angústia', 5)],
    },
    'fisica': {
        'Termodinâmica': [('temperatura', 5), ('calor', 5), ('garrafa térmica', 15), ('equilíbrio térmico', 10), ('calorimetria', 10)],
        'Mecânica': [('força', 5), ('newton', 8), ('massa', 3), ('aceleração', 5)],
        'Cinemática': [('cinemática', 10), ('deslocamento', 5), ('velocidade', 3)],
        'Eletromagnetismo': [('elétric', 5), ('magnét', 5), ('carga', 3), ('circuito', 5)],
        'Óptica': [('óptica', 8), ('luz', 5), ('reflexão', 3)],
        'Gravitação': [('gravidade', 5), ('queda livre', 10)],
        'Ondas': [('onda', 5), ('frequência', 3)],
        'Trabalho e Energia': [('trabalho', 2), ('energia', 3)],
    },
    'quimica': {
        'Química Geral': [('átomo', 5), ('molécula', 5), ('tabela periódica', 8)],
        'Soluções': [('solução', 5), ('solute', 8), ('concentração', 5)],
        'Reações Químicas': [('reação', 5), ('combinação', 3)],
        'Química Orgânica': [('orgânico', 5), ('hidrocarboneto', 8)],
        'Eletroquímica': [('eletrólise', 10), ('pilha', 8)],
        'Acidoses e Bases': [('ácido', 5), ('base', 3), ('ph', 8)],
        'Estequiometria': [('estequiometria', 10)],
    },
    'biologia': {
        'Citologia': [('célula', 5), ('membrana', 3), ('organela', 8)],
        'Genética': [('gene', 5), ('dna', 8), ('hereditariedade', 8)],
        'Ecologia': [('ecologia', 8), ('ecossistema', 8), ('biodiversidade', 8)],
        'Evolução': [('evolução', 5), ('seleção natural', 10)],
        'Fisiologia': [('fisiologia', 8), ('sistema', 3)],
        'Botânica': [('planta', 5), ('fotossíntese', 8)],
        'Zoologia': [('animal', 5), ('vertebrado', 8)],
    },
    'algebra': {
        'Equações': [('equação', 8), ('incógnita', 8)],
        'Funções': [('função', 8), ('gráfico', 3)],
        'Porcentagem': [('porcento', 8), ('porcentagem', 8)],
        'Proporcionalidade': [('proporcional', 8)],
        'Regra de Três': [('regra de três', 10)],
        'Progressão Aritmética': [('pa', 5), ('progressão aritmética', 10)],
        'Progressão Geométrica': [('pg', 5), ('progressão geométrica', 10)],
    },
    'geometria': {
        'Geometria Plana': [('triângulo', 5), ('quadrilátero', 5), ('círculo', 5), ('área', 3)],
        'Geometria Espacial': [('volume', 5), ('cilindro', 5)],
        'Trigonometria': [('seno', 8), ('cosseno', 8)],
        'Pitágoras': [('pitágoras', 10), ('hipotenusa', 10)],
    },
    'estatistica': {
        'Estatística': [('estatística', 8), ('média', 5), ('mediana', 5)],
        'Gráficos': [('gráfico', 5), ('histograma', 8)],
        'Amostragem': [('amostra', 8), ('pesquisa', 3)],
    },
    'probabilidade': {
        'Probabilidade': [('probabilidade', 10), ('chance', 8), ('sorteio', 8)],
        'Espaço Amostral': [('espaço amostral', 10)],
        'Permutação': [('permutação', 10)],
    },
    'portugues': {
        'Interpretação de Texto': [('texto', 3), ('interpretação', 5), ('leitura', 3)],
        'Vozes Verbais': [('verbo', 5), ('conjungação', 8), ('tempo verbal', 8)],
        'Morfologia': [('prefixo', 8), ('sufixo', 8), ('morfologia', 10)],
        'Sintaxe': [('sintaxe', 8), ('sujeito', 5), ('predicado', 5)],
        'Semântica': [('sinônimo', 8), ('polissemia', 10)],
        'Pontuação': [('ponto', 3), ('vírgula', 8)],
        'Coesão': [('coesão', 8), ('conjunção', 5)],
        'Gêneros Textuais': [('gênero', 5), ('crônica', 8), ('poema', 5)],
        'Figuras de Linguagem': [('metáfora', 8)],
        'Norma Culta': [('norma culta', 10), ('gramática', 5)],
    },
}


def get_subtopico(discipline, texto):
    if not texto or not discipline:
        return ''
    
    tl = texto.lower()
    subtopics = SUBTOPIC_KEYWORDS.get(discipline, {})
    
    best_sub = None
    best_score = 0
    
    for sub, signals in subtopics.items():
        score = 0
        for kw, wt in signals:
            if kw.lower() in tl:
                score += wt
        if score > best_score:
            best_score = score
            best_sub = sub
    
    if best_sub and best_score >= 3:
        return best_sub
    
    defaults = {
        'historia': 'Idade Contemporânea', 'geografia': 'Geografia do Brasil',
        'sociologia': 'Sociologia Geral', 'filosofia': 'Filosofia Moderna',
        'fisica': 'Mecânica', 'quimica': 'Química Geral', 'biologia': 'Citologia',
        'algebra': 'Equações', 'geometria': 'Geometria Plana',
        'estatistica': 'Estatística', 'probabilidade': 'Probabilidade',
        'portugues': 'Interpretação de Texto',
        'ingles': 'Texto Informativo', 'espanhol': 'Texto Informativo',
        'literatura': 'Análise Literária', 'artes': 'Artes Visuais',
    }
    return defaults.get(discipline, 'Geral')


def main():
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    area_fixed = 0
    disc_fixed = 0
    sub_fixed = 0
    
    for question in q:
        texto = question.get('texto', '')
        if not texto:
            continue
        
        correct_disc = detect_discipline(texto)
        if not correct_disc:
            continue
        
        correct_area = DISC_TO_AREA.get(correct_disc, '')
        if not correct_area:
            continue
        
        if question.get('area') != correct_area:
            question['area'] = correct_area
            area_fixed += 1
        
        if question.get('disciplina') != correct_disc:
            question['disciplina'] = correct_disc
            disc_fixed += 1
        
        correct_sub = get_subtopico(correct_disc, texto)
        if correct_sub and question.get('subtopico') != correct_sub:
            question['subtopico'] = correct_sub
            sub_fixed += 1
    
    print(f"Fixed: {area_fixed} areas, {disc_fixed} disciplines, {sub_fixed} subtopics")
    
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")


if __name__ == "__main__":
    main()
