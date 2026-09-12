"""
Fix ALL metadata using ONLY content analysis (keywords + context).
Ignores question number completely.
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


# Keywords with weights - very specific to each discipline
DISCIPLINE_KEYWORDS = {
    'fisica': {
        'termos': [
            'calorimetria', 'equilíbrio térmico', 'garrafa térmica',
            'termodinâmica', 'entropia', 'máquina térmica',
            'calorimetria', 'lei de ohm', 'lei de newton',
            'princípio de arquimedes', 'empuxo', 'pressão',
            'cinemática', 'dinâmica', 'estática',
            'eletromagnetismo', 'campo elétrico', 'campo magnético',
            'circuito elétrico', 'resistência elétrica',
            'óptica', 'reflexão', 'refração',
            'ondas', 'frequência', 'amplitude',
            'gravitação', 'queda livre', 'velocidade',
            'aceleração', 'força', 'newton', 'massa',
            'energia', 'trabalho', 'potência', 'joule',
            'volt', 'ampere', 'ohm', 'watt',
            'relatividade', 'quântica', 'física moderna',
            'radioatividade', 'fissão', 'fusão',
            'semicondutor', 'transistor', 'diodo',
            'movimento ondulatório', 'velocidade de propagação',
            'referencial inercial', 'referencial não inercial',
            'grandeza escalar', 'grandeza vetorial',
            'processo isotérmico', 'processo adiabático',
            'processo isobárico', 'processo isocórico',
            'calor sensível', 'calor latente',
            'carga elétrica', 'lei de coulomb',
            'potencial elétrico', 'capacitância',
            'corrente alternada', 'corrente contínua',
            'transformador', 'gerador',
            'efeito fotoelétrico', 'efeito doppler',
            'dualidade onda-partícula',
        ],
        'temas': [
            'temperatura', 'calor', 'pressão', 'volume',
            'densidade', 'fluido', 'gás', 'líquido',
            'força', 'massa', 'energia', 'trabalho',
            'potência', 'movimento', 'velocidade',
            'aceleração', 'deslocamento', 'trajetória',
            'resistência', 'corrente', 'tensão', 'voltagem',
            'circuito', 'campo', 'onda', 'luz',
            'espelho', 'lente', 'prisma',
        ],
    },
    'historia': {
        'termos': [
            'revolução francesa', 'declaração dos direitos',
            'bastilha', 'liberdade igualdade fraternidade',
            'revolução industrial', 'mecanização',
            'regime militar', 'ditadura militar', 'ai-5',
            'estado novo', 'getúlio vargas',
            'república velha', 'café com leite', 'coronelismo',
            'política dos governadores',
            'primeira república',
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
            '1930', '1937', '1945', '1964', '1985',
            '1822', '1889', '1888', '1500',
            'tiradentes', 'inconfidência mineira',
            'conjunção mineira',
            'revolução de 30', 'estado novo',
            'segunda guerra mundial', 'primeira guerra mundial',
            'guerra do golfo', 'guerra do vietnã',
            'queda do muro', 'revolução de 1989',
            'revolução cubana', 'revolução mexicana',
            'independência do brasil', 'dom pedro',
        ],
        'temas': [
            'guerra', 'revolução', 'império', 'colônia',
            'república', 'ditadura', 'golpe', 'eleições',
            'escravidão', 'escravo', 'fazenda',
            'bloqueio', 'fiscalização',
            'conflito', 'batalha', 'tratado',
            'século', 'período', 'era',
            'história', 'brasil', 'europa', 'américa',
            'poder', 'política', 'governo', 'estado',
            'nação', 'soberania',
            'economia', 'mercado', 'comércio',
            'sociedade', 'povo', 'povoação',
        ],
    },
    'geografia': {
        'termos': [
            'cartografia', 'escala cartográfica', 'projeção cartográfica',
            'fuso horário', 'linha do equador',
            'paralelo', 'meridiano de greenwich',
            'placa tectônica', 'bacia hidrográfica',
            'zoneamento ecológico', 'reserva legal',
            'unidade de conservação', 'parque nacional',
            'desertificação', 'degradação ambiental',
            'contaminação', 'desequilíbrio ambiental',
            'globalização', 'mundialização',
            'reforma agrária', 'latifúndio', 'minifúndio',
            'questão agrária', 'questão ambiental',
            'bacia oceânica', 'planície', 'planalto',
            'relevo', 'vegetação', 'bioma',
            'cerrado', 'caatinga', 'mata atlântica', 'amazônia',
            'semiárido', 'litoral', 'interior',
            'fronteira', 'divisa', 'limite',
        ],
        'temas': [
            'clima', 'temperatura', 'chuva', 'seca',
            'região', 'nordeste', 'sudeste', 'sul',
            'norte', 'centro-oeste',
            'população', 'migração', 'imigração',
            'urbanização', 'metrópole', 'cidade',
            'meio ambiente', 'desmatamento', 'poluição',
            'energia', 'petróleo', 'biocombustível',
            'transporte', 'ferrovia', 'porto',
            'mapa', 'escala', 'coordenada',
            'bloco econômico', 'mercosul', 'onu',
            'desenvolvimento sustentável',
            'sustentabilidade', 'preservação', 'conservação',
            'agricultura', 'pecuária', 'mineração',
            'indústria', 'comércio', 'serviços',
        ],
    },
    'quimica': {
        'termos': [
            'tabela periódica', 'liga iônica', 'ligação covalente',
            'liga metálica', 'eletrólise', 'eletrodo',
            'estequiometria', 'mol', 'massa molar',
            'hidrocarboneto', 'composto orgânico',
            'grupo funcional', 'alcool', 'aldehyde',
            'ácido carboxílico', 'éster', 'amina',
            'amida', 'química orgânica',
            'redox', 'oxidação', 'redução',
            'galvanoplastia', 'corrosão',
            'destilação', 'cristalização', 'filtração',
            'titulação', 'molaridade', 'molalidade',
            'normalidade', 'diluição',
            'compostos iônicos', 'compostos moleculares',
            'massa atômica', 'massa molecular',
            'número de avogadro',
            'gás ideal', 'equação de estado',
            'termodinâmica química', 'entalpia',
            'energia de ativação', 'velocidade de reação',
            'equilíbrio químico', 'constante de equilíbrio',
            'ph', 'indicador ácido',
            'eletroquímica', 'pilha galvânica',
            'bateria', 'cela eletroquímica',
        ],
        'temas': [
            'átomo', 'molécula', 'elemento', 'composto',
            'mistura', 'solução', 'solute', 'solvente',
            'concentração', 'diluição', 'saturação',
            'ácido', 'base', 'ph', 'neutralização',
            'reação', 'produto', 'reactante',
            'combustível', 'etanol', 'gasolina',
            'polímero', 'plástico', 'biodiesel',
            'combustão', 'oxidação', 'redução',
            'proteína', 'carboidrato', 'lipídio',
            'fermentação', 'destilação',
        ],
    },
    'biologia': {
        'termos': [
            'mitose', 'meiose', 'divisão celular',
            'cromossomo', 'gene', 'dna', 'rna',
            'engenharia genética', 'transgênico',
            'clonagem', 'biotecnologia', 'ogm',
            'seleção natural', 'darwin', 'evolução',
            'adaptação', 'especiação', 'fossil',
            'fotossíntese', 'respiração celular', 'fermentação',
            'citologia', 'biologia celular', 'organela',
            'membrana plasmática', 'núcleo celular',
            'citoplasma', 'ribossomo', 'mitocôndria',
            'sistema digestório', 'sistema respiratório',
            'sistema circulatório', 'sistema nervoso',
            'sistema endócrino', 'sistema imunológico',
            'sistema reprodutor', 'sistema esquelético',
            'sistema muscular', 'sistema urinário',
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
            'ciclo do carbono', 'ciclo da água',
            'ciclo do nitrogênio', 'fixação de nitrogênio',
            'bactéria nitrogenada', 'rhizóbio',
            'mutação', 'alelo', 'genótipo', 'fenótipo',
            'homozigoto', 'heterozigoto',
            'dominante', 'recessivo',
            'diabetes', 'câncer', 'aids', 'malária',
            'antibiótico', 'vacina', 'imunidade',
            'hemograma', 'hemácias', 'leucócitos',
            'plaquetas', 'hemoglobina', 'anticorpo', 'antígeno',
        ],
        'temas': [
            'célula', 'membrana', 'organela', 'organito',
            'dna', 'gene', 'cromossomo', 'hereditariedade',
            'evolução', 'seleção natural', 'adaptação',
            'fotossíntese', 'respiração', 'fermentação',
            'ecologia', 'ecossistema', 'biodiversidade',
            'bactéria', 'vírus', 'fungo',
            'planta', 'animal', 'vertebrado', 'invertebrado',
            'bioma', 'ecossistema',
            'proteína', 'enzima', 'metabolismo',
            'digestão', 'absorção', 'excreção',
            'imunidade', 'defesa', 'anticorpo',
        ],
    },
    'sociologia': {
        'termos': [
            'movimento dos sem terra', 'mst',
            'organização não governamental', 'ong',
            'pastoral da terra', 'defesa dos direitos',
            'conscientização', 'direitos trabalhistas',
            'direitos sociais', 'política pública',
            'participação cidadã', 'democracia participativa',
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
            'sistema previdenciário',
            'norma social', 'controle social',
            'sociabilidade', 'interação social',
            'poder', 'dominação', 'resistência',
            'ideologia', 'hegemonia',
            'qualidade de vida', 'bem-estar social',
            'mst', 'mtst',
        ],
        'temas': [
            'sociedade', 'social', 'classe', 'estrutura',
            'cidadão', 'cidadania', 'direito', 'dever',
            'cultura', 'identidade', 'tradição',
            'educação', 'escola', 'ensino',
            'trabalho', 'emprego', 'desemprego',
            'violência', 'crime', 'segurança',
            'mídia', 'comunicação', 'jornal',
            'movimento social', 'protesto', 'greve',
            'família', 'religião', 'gênero',
            'consumismo', 'consumidor',
            'exploração', 'opressão', 'marginalização',
            'exclusão', 'desigualdade', 'pobreza',
            'riqueza', 'renda', 'salário',
            'política', 'governo', 'estado',
            'poder', 'autoridade', 'legitimidade',
            'participação', 'cidadania', 'democracia',
        ],
    },
    'filosofia': {
        'termos': [
            'cogito ergo sum', 'materialismo histórico',
            'alienação', 'sociedade civil', 'estado democrático',
            'contratualismo', 'soberania popular',
            'direito natural', 'direito positivo',
            'utilitarismo', 'deontologia', 'virtude',
            'epistemologia', 'metafísica', 'ontologia',
            'cosmologia', 'filosofia da linguagem',
            'linguagem', 'signo',
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
            'cidadania', 'democracia', 'soberania',
            'sócrates', 'platão', 'aristóteles',
            'descartes', 'kant', 'hegel', 'marx', 'nietzsche',
            'sartre', 'foucault', 'existencialismo',
            'racionalismo', 'empirismo', 'materialismo',
            'idealismo', 'utilitarismo', 'deontologia',
            'existencialismo', 'nihilismo',
            'absurdo', 'angústia', 'alienação',
            'ser', 'nada', 'essência', 'existência',
            'método', 'dialética', 'sociologia',
            'verdade', 'conhecimento', 'ciência',
        ],
        'temas': [
            'filosofia', 'filósofo', 'sócrates', 'platão',
            'descartes', 'kant', 'hegel', 'marx', 'nietzsche',
            'ética', 'moral', 'bem', 'mal', 'justo',
            'política', 'estado', 'governo', 'poder',
            'verdade', 'conhecimento', 'realidade',
            'liberdade', 'igualdade', 'justiça',
            'existência', 'consciência', 'metafísica',
            'epistemologia', 'estética', 'beleza',
            'lógica', 'raciocínio', 'argumentação',
            'ideia', 'conceito', 'noção',
            'sentido', 'significado', 'interpretação',
            'crítica', 'análise', 'reflexão',
            'pensamento', 'pensador',
        ],
    },
    'portugues': {
        'termos': [
            'voz ativa', 'voz passiva', 'voz reflexiva',
            'tempo verbal', 'modo indicativo', 'modo subjuntivo',
            'condicional', 'imperativo', 'jussivo',
            'ponto e vírgula', 'dois pontos', 'ponto final',
            'vírgula', 'ponto de interrogação', 'ponto de exclamação',
            'crase', 'acentuação', 'ortografia',
            'concordância', 'regência', 'crase',
            'coordenação', 'subordinação', 'oração absoluta',
            'sujeito simples', 'sujeito composto',
            'predicado simples', 'predicado composto',
            'objeto direto', 'objeto indireto',
            'objeto prepositivo', 'complemento nominal',
            'adjunto adnominal', 'advérbio', 'locução adverbial',
            'locução prepositiva', 'oração subordinada',
            'período simples', 'período composto',
            'norma culta', 'gramática', 'regra gramatical',
            'linguagem formal', 'linguagem informal',
            'variação linguística', 'gíria', 'calão',
            'semântica', 'sintaxe', 'morfologia',
            'fonologia', 'fonética', 'fonologia',
            'denotação', 'conotação',
            'metáfora', 'hipérbole', 'ironia', 'comparação',
            'personificação', 'metonímia', 'sinédoque',
            'antítese', 'paradoxo', 'símile',
            'prosopopeia', 'apóstrofe', 'eufemismo',
            'catacrese', 'antítese',
            'figura de linguagem', 'figura de sentido',
            'redação', 'produção textual',
            'redação dissertativa', 'redação narrativa',
            'redação descritiva', 'texto argumentativo',
            'tese', 'argumento', 'contra-argumento',
            'introdução', 'desenvolvimento', 'conclusão',
            'coesão', 'coerência', 'coerência textual',
        ],
        'temas': [
            'texto', 'leitura', 'interpretação', 'compreensão',
            'verbo', 'sujeito', 'predicado',
            'objeto', 'oração', 'período',
            'palavra', 'vocabulário', 'significado',
            'sinônimo', 'antônimo', 'polissemia', 'homônimo',
            'prefixo', 'sufixo', 'radical', 'radicalidade',
            'género textual', 'gênero', 'tipo textual',
            'crônica', 'poema', 'conto', 'novela',
            'romantismo', 'realismo', 'modernismo', 'barroco',
            'editorial', 'crítica', 'notícia', 'reportagem',
            'charge', 'cartaz', 'anúncio',
            'norma culta', 'gramática', 'regra',
            'linguagem', 'comunicação', 'discurso',
            'tom', 'estilo', 'artifício',
            'retórica', 'argumento', 'persuasão',
        ],
    },
    'algebra': {
        'termos': [
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
            'proporção', 'proporcionalidade direta',
            'proporcionalidade inversa',
            'grandeza diretamente proporcional',
            'grandeza inversamente proporcional',
            'porcentagem', 'desconto', 'acréscimo',
            'juros', 'capital', 'taxa', 'tempo',
        ],
        'temas': [
            'equação', 'incógnita', 'solução', 'igualdade',
            'função', 'gráfico', 'domínio', 'imagem',
            'porcento', 'porcentagem', 'proporção',
            'razão', 'proporcional', 'regra de três',
            'juros', 'capital', 'taxa',
            'sistema', 'matriz', 'determinante',
            'logaritmo', 'potência', 'raiz',
            'expressão', 'monômio', 'polinômio',
            'coeficiente', 'constante',
            'variável', 'incógnita',
            'gráfico', 'tabela', 'representação',
        ],
    },
    'geometria': {
        'termos': [
            'pitágoras', 'teorema de pitágoras',
            'triângulo retângulo', 'hipotenusa', 'cateto',
            'semelhança de triângulos', 'congruência de triângulos',
            'teorema de tales',
            'relação métrica do triângulo retângulo',
            'trigonometria', 'seno', 'cosseno', 'tangente',
            'plano cartesiano', 'coordenada', 'vetor',
            'geometria analítica', 'equação da reta',
            'equação da circunferência',
            'equação da parábola', 'equação da elipse',
            'equação da hipérbole',
            'sólido geométrico', 'poliedro',
            'cubo', 'esfera', 'cilindro', 'cone', 'pirâmide',
            'volume', 'área de superfície',
            'ponto', 'reta', 'plano', 'ângulo',
            'mediatriz', 'bissetriz', 'altura', 'mediana',
            'baricentro', 'incentro', 'circuncentro', 'ortocentro',
            'circunscrita', 'inscrita',
            'transformação geométrica', 'translação', 'rotação',
            'reflexão', 'dilatação', 'simetria',
            'quadrilátero', 'trapézio', 'losango',
            'retângulo', 'quadrado', 'parallelogram',
            'polígono', 'poliedro',
            'diagonal', 'lado', 'vértice', 'aresta',
        ],
        'temas': [
            'triângulo', 'quadrilátero', 'círculo',
            'circunferência', 'área', 'perímetro',
            'volume', 'sólido', 'poliedro',
            'ângulo', 'grau', 'radiano',
            'pitágoras', 'hipotenusa', 'cateto',
            'seno', 'cosseno', 'tangente',
            'plano', 'espacio', 'coordenada',
            'semelhança', 'congruência',
            'simetria', 'translação', 'rotação',
            'reflexão', 'dilatação',
            'polígono', 'lados', 'vértices',
            'diagonal', 'base', 'altura',
        ],
    },
    'estatistica': {
        'termos': [
            'estatística', 'estatístico', 'estatística descritiva',
            'estatística inferencial',
            'população', 'amostra', 'censo',
            'pesquisa', 'coleta de dados',
            'tabela de frequência', 'distribuição de frequência',
            'histograma', 'polígono de frequência',
            'ogive', 'box plot', 'diagrama de caule e folhas',
            'média', 'mediana', 'moda',
            'desvio padrão', 'variância', 'amplitude',
            'amplitude total', 'amplitude interquartil',
            'medidas de tendência central',
            'medidas de dispersão',
            'percentil', 'quartil', 'decil',
            'correlação', 'regressão',
            'coeficiente de correlação', 'linha de regressão',
            'probabilidade', 'evento', 'espaço amostral',
            'experimento aleatório',
            'resultado', 'caso favorável', 'caso possível',
            'frequência absoluta', 'frequência relativa',
            'frequência percentual',
        ],
        'temas': [
            'média', 'mediana', 'moda',
            'gráfico', 'tabela', 'histograma',
            'desvio padrão', 'variância', 'amplitude',
            'pesquisa', 'amostra', 'censo',
            'dados', 'informação', 'estatística',
            'frequência', 'percentual', 'proporção',
            'amostra', 'população',
            'box plot', 'histograma',
            'interpretação', 'análise', 'comparação',
            'medida', 'cálculo', 'cálculo estatístico',
        ],
    },
    'probabilidade': {
        'termos': [
            'probabilidade', 'probabilística',
            'evento', 'espaço amostral', 'resultado',
            'evento certo', 'evento impossível',
            'evento aleatório', 'experimento aleatório',
            'evento determinado', 'evento aleatório',
            'evento independente', 'evento dependente',
            'permutação', 'arranjo', 'combinação',
            'árvore de decisão', 'tabela de frequência',
            'experimento aleatório', 'experiência aleatória',
            'caso favorável', 'caso possível',
            'probabilidade clássica', 'probabilidade frequencista',
            'probabilidade subjetiva',
            'evento composto', 'evento simples',
            'probabilidade condicional', 'probabilidade conjunta',
            'teorema de bayes', 'distribuição binomial',
            'distribuição normal', 'distribuição uniforme',
            'lógica combinatória', 'regra do produto', 'regra da soma',
            'moeda', 'dado', 'baralho', 'loteria',
            'mega-sena', 'quina', 'lotofácil', 'dia de sorte',
        ],
        'temas': [
            'probabilidade', 'chance', 'evento',
            'espaço amostral', 'resultado possível',
            'sorteio', 'experiência', 'experimento',
            'moeda', 'dado', 'baralho',
            'loteria', 'jogo', 'azar',
            'certeza', 'incerteza', 'impossível',
            'possível', 'provável', 'improvável',
            'número de casos', 'frequência',
            'porcentagem', 'proporção',
            'permutação', 'arranjo', 'combinação',
            'contagem', 'enumeração',
            'resultado', 'outcome', 'evento',
        ],
    },
}


def detect_discipline(texto):
    """Detect discipline using weighted keyword matching."""
    if not texto:
        return None
    
    tl = texto.lower()
    
    best_disc = None
    best_score = 0
    
    for disc, data in DISCIPLINE_KEYWORDS.items():
        score = 0
        for kw in data.get('termos', []):
            if kw.lower() in tl:
                score += 3
        for kw in data.get('temas', []):
            if kw.lower() in tl:
                score += 1
        
        if score > best_score:
            best_score = score
            best_disc = disc
    
    if best_score >= 5:
        return best_disc
    return None


def get_subtopico(discipline, texto):
    """Get subtopic based on discipline keywords."""
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


# Subtopic keywords
SUBTOPIC_KEYWORDS = {
    'historia': {
        'Brasil Colônia': [('colônia', 3), ('colonial', 3), ('capitanias', 5), ('brasil colonial', 5)],
        'Brasil Império': [('império', 3), ('dom pedro', 5), ('independência', 3), ('brasil império', 5)],
        'República Velha': [('república', 2), ('café com leite', 8), ('república velha', 8)],
        'Era Vargas': [('vargas', 3), ('estado novo', 5), ('getúlio', 5)],
        'Regime Militar': [('militar', 3), ('ditadura', 3), ('ai-5', 8), ('regime militar', 8)],
        'Guerras Mundiais': [('primeira guerra', 8), ('segunda guerra', 8), ('guerra fria', 8)],
        'Guerra Fria': [('guerra fria', 10), ('urss', 5), ('bloco soviético', 8)],
        'Pré-História': [('pré-história', 8), ('neolítico', 8), ('paleolítico', 8)],
        'Civilizações Antigas': [('egito', 5), ('mesopotâmia', 8), ('roma', 3)],
        'Idade Média': [('medieval', 8), ('feudalismo', 8)],
        'Revolução Francesa': [('revolução francesa', 10), ('bastilha', 8)],
        'Revolução Industrial': [('revolução industrial', 10), ('mecanização', 8)],
        'Abolicionismo': [('escravo', 3), ('escravidão', 5), ('abolicionismo', 8), ('trabalho escravo', 8)],
        'Direitos Humanos': [('direitos humanos', 10), ('liberdade', 2)],
        'Redemocratização': [('democracia', 3), ('eleições', 3), ('constituição', 3)],
        'Idade Contemporânea': [('contemporânea', 5), ('século xx', 5), ('globalização', 3)],
    },
    'geografia': {
        'Geografia do Brasil': [('brasil', 2), ('nordeste', 3), ('sudeste', 3), ('norte', 2)],
        'Geografia Mundial': [('mundo', 2), ('europa', 3), ('américa', 3), ('áfrica', 3)],
        'Cartografia': [('mapa', 3), ('cartografia', 8), ('escala', 3), ('coordenada', 5)],
        'Climatologia': [('clima', 5), ('temperatura', 3), ('chuva', 5), ('seca', 3)],
        'Urbanização': [('urbanização', 8), ('cidade', 3), ('metrópole', 5)],
        'Meio Ambiente': [('meio ambiente', 8), ('desmatamento', 5), ('poluição', 3)],
        'Demografia': [('população', 5), ('natalidade', 8), ('mortalidade', 8)],
        'Globalização': [('globalização', 8), ('mundialização', 8)],
        'Questão Agrária': [('reforma agrária', 10), ('latifúndio', 8)],
        'Migração': [('migração', 8), ('imigração', 8)],
    },
    'sociologia': {
        'Sociologia Geral': [('sociedade', 5), ('social', 2), ('classe', 2)],
        'Cidadania': [('cidadão', 5), ('cidadania', 8), ('direito', 2), ('conscientização', 5)],
        'Cultura': [('cultura', 5), ('tradição', 3), ('identidade cultural', 8)],
        'Estratificação Social': [('estratificação', 8), ('desigualdade', 5)],
        'Trabalho': [('trabalho', 2), ('emprego', 3), ('desemprego', 5), ('trabalhador', 3)],
        'Educação': [('educação', 5), ('escola', 3), ('ensino', 3)],
        'Violência': [('violência', 5), ('crime', 3)],
        'Mídia': [('mídia', 8), ('comunicação', 3), ('jornal', 3)],
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
        'Termodinâmica': [('temperatura', 5), ('calor', 5), ('garrafa térmica', 15), ('equilíbrio térmico', 10), ('calorimetria', 10), ('entropia', 8)],
        'Mecânica': [('força', 5), ('newton', 8), ('massa', 3), ('aceleração', 5)],
        'Cinemática': [('cinemática', 10), ('deslocamento', 5), ('velocidade', 3)],
        'Eletromagnetismo': [('elétric', 5), ('magnét', 5), ('carga', 3), ('circuito', 5)],
        'Óptica': [('óptica', 8), ('luz', 5), ('reflexão', 3), ('refração', 3)],
        'Gravitação': [('gravidade', 5), ('queda livre', 10)],
        'Ondas': [('onda', 5), ('frequência', 3), ('amplitude', 3)],
        'Trabalho e Energia': [('trabalho', 2), ('energia', 3), ('joule', 8)],
    },
    'quimica': {
        'Química Geral': [('átomo', 5), ('molécula', 5), ('tabela periódica', 8)],
        'Soluções': [('solução', 5), ('solute', 8), ('solvente', 8), ('concentração', 5)],
        'Reações Químicas': [('reação', 5), ('combinação', 3), ('decomposição', 3)],
        'Química Orgânica': [('orgânico', 5), ('carbono', 3), ('hidrocarboneto', 8)],
        'Eletroquímica': [('eletrólise', 10), ('pilha', 8), ('eletrodo', 8)],
        'Acidoses e Bases': [('ácido', 5), ('base', 3), ('ph', 8)],
        'Estequiometria': [('estequiometria', 10), ('mol', 8)],
    },
    'biologia': {
        'Citologia': [('célula', 5), ('membrana', 3), ('organela', 8), ('citoplasma', 8)],
        'Genética': [('gene', 5), ('dna', 8), ('hereditariedade', 8)],
        'Ecologia': [('ecologia', 8), ('ecossistema', 8), ('biodiversidade', 8), ('cadeia alimentar', 10)],
        'Evolução': [('evolução', 5), ('seleção natural', 10)],
        'Fisiologia': [('fisiologia', 8), ('sistema', 3)],
        'Botânica': [('planta', 5), ('fotossíntese', 8)],
        'Zoologia': [('animal', 5), ('vertebrado', 8), ('invertebrado', 8)],
    },
    'algebra': {
        'Equações': [('equação', 8), ('incógnita', 8), ('solução', 3)],
        'Funções': [('função', 8), ('gráfico', 3)],
        'Porcentagem': [('porcento', 8), ('porcentagem', 8)],
        'Proporcionalidade': [('proporcional', 8), ('razão', 3)],
        'Regra de Três': [('regra de três', 10)],
        'Progressão Aritmética': [('pa', 5), ('progressão aritmética', 10)],
        'Progressão Geométrica': [('pg', 5), ('progressão geométrica', 10)],
    },
    'geometria': {
        'Geometria Plana': [('triângulo', 5), ('quadrilátero', 5), ('círculo', 5), ('área', 3)],
        'Geometria Espacial': [('volume', 5), ('sólido', 5), ('cilindro', 5)],
        'Trigonometria': [('seno', 8), ('cosseno', 8), ('tangente', 8)],
        'Pitágoras': [('pitágoras', 10), ('hipotenusa', 10)],
    },
    'estatistica': {
        'Estatística': [('estatística', 8), ('média', 5), ('mediana', 5), ('moda', 5)],
        'Gráficos': [('gráfico', 5), ('histograma', 8)],
        'Medidas de Tendência Central': [('média', 5), ('mediana', 5), ('moda', 5)],
        'Amostragem': [('amostra', 8), ('amostragem', 10)],
    },
    'probabilidade': {
        'Probabilidade': [('probabilidade', 10), ('chance', 8), ('sorteio', 8)],
        'Espaço Amostral': [('espaço amostral', 10)],
        'Permutação': [('permutação', 10), ('arranjo', 10)],
    },
    'portugues': {
        'Interpretação de Texto': [('texto', 3), ('interpretação', 5), ('leitura', 3), ('compreensão', 3)],
        'Vozes Verbais': [('verbo', 5), ('conjugação', 8), ('tempo verbal', 8)],
        'Morfologia': [('prefixo', 8), ('sufixo', 8), ('morfologia', 10)],
        'Sintaxe': [('sintaxe', 8), ('sujeito', 5), ('predicado', 5)],
        'Semântica': [('sinônimo', 8), ('polissemia', 10)],
        'Pontuação': [('ponto', 3), ('vírgula', 8), ('ponto e vírgula', 8)],
        'Coesão': [('coesão', 8), ('conjunção', 5)],
        'Gêneros Textuais': [('gênero', 5), ('crônica', 8), ('poema', 5), ('editorial', 8)],
        'Figuras de Linguagem': [('metáfora', 8), ('comparação', 5)],
        'Movimentos Literários': [('romantismo', 8), ('realismo', 8)],
        'Norma Culta': [('norma culta', 10), ('gramática', 5)],
    },
    'ingles': {
        'Texto Informativo': [('text', 3), ('article', 5), ('passage', 5)],
        'Gramática Inglesa': [('verb', 5), ('tense', 8)],
    },
    'espanhol': {
        'Texto Informativo': [('texto', 3)],
    },
    'literatura': {
        'Movimentos Literários': [('romantismo', 8), ('realismo', 8), ('modernismo', 8)],
        'Análise Literária': [('personagem', 8), ('enredo', 8), ('narrador', 8)],
        'Figuras de Linguagem': [('metáfora', 8)],
    },
    'artes': {
        'Artes Visuais': [('pintura', 8), ('escultura', 8), ('arte', 3)],
        'Música': [('música', 8), ('ritmo', 5)],
        'Teatro': [('teatro', 8), ('peça', 5)],
        'Cinema': [('cinema', 8), ('filme', 5)],
    },
}


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
