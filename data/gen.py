#!/usr/bin/env python3
import json, os, random
random.seed(42)

DISTRIBUTION = {
    "linguagens": {"portugues": 20, "ingles": 10, "espanhol": 5, "literatura": 5, "artes": 2, "educacao_fisica": 2, "tic": 1},
    "humanas": {"historia": 15, "geografia": 15, "sociologia": 8, "filosofia": 7},
    "natureza": {"fisica": 15, "quimica": 15, "biologia": 15},
    "matematica": {"algebra": 15, "geometria": 15, "estatistica": 10, "probabilidade": 5}
}
AREA_LETTER = {"linguagens": "L", "humanas": "H", "natureza": "N", "matematica": "M"}

TOPICS = {
    2021: ["pandemia", "educação remota", "vacinação", "saúde mental", "isolamento social", "rotulagem de alimentos", "eleições municipais", "mudanças climáticas"],
    2022: ["eleições gerais", "inteligência artificial", "copa do mundo", "desigualdade social", "redes sociais", "energia renovável", "crise hídrica", "meio ambiente"],
    2023: ["mudanças climáticas", "IA generativa", "redes sociais", "sustentabilidade", "saúde pública", "educação", "democracia", "transição energética"],
    2024: ["eleições", "tecnologia", "inteligência artificial", "economia digital", "geopolítica", "mudanças climáticas", "transição energética", "segurança de dados"],
    2025: ["inteligência artificial", "transição energética", "sustentabilidade", "segurança cibernética", "geopolítica", "saúde global", "educação digital", "economia verde"]
}

def diff():
    r = random.random()
    if r < 0.40:
        return 1, random.randint(65, 85)
    elif r < 0.80:
        return 2, random.randint(40, 65)
    else:
        return 3, random.randint(15, 40)

def pick(lst):
    return lst[random.randint(0, len(lst)-1)]

def pick_n(lst, n):
    return random.sample(lst, min(n, len(lst)))

OPTIONS_LETTERS = ["A", "B", "C", "D", "E"]

def gen_linguagens_portugues(year, seq, topic):
    contexts = [
        f"Leia o texto jornalístico abaixo, publicado em {year}, sobre o tema {topic}.",
        f"Leia o trecho da crônica a seguir, que aborda questões relacionadas a {topic} no contexto brasileiro.",
        f"Leia o fragmento de romance contemporâneo que retrata aspectos da sociedade brasileira em tempos de {topic}.",
        f"Leia o poema abaixo, que contempla reflexões sobre {topic} na atualidade.",
        f"Leia a charge e o texto abaixo, que tratam de {topic} no cenário nacional."
    ]
    textos = [
        f"A reflexão sobre {topic} ganhou novo significado nos últimos anos. As transformações sociais e culturais vivenciadas pela população brasileira geraram debates intensos sobre o papel do indivíduo na sociedade. Nesse contexto, a literatura e a arte tornam-se ferramentas fundamentais para a compreensão dessas mudanças e para a formação de uma consciência crítica sobre a realidade.",
        f"Nos últimos tempos, o tema {topic} tem sido objeto de intensos debates na sociedade brasileira. Segundo especialistas, as mudanças nos padrões de comportamento e consumo refletem profundas transformações culturais que afetam diretamente a vida cotidiana das pessoas. Essa realidade exige uma leitura atenta dos sinais presentes na produção cultural e nos meios de comunicação.",
        f"A discussão sobre {topic} no Brasil envolve aspectos históricos, culturais e sociais que se entrelaçam de forma complexa. A análise de textos literários e jornalísticos permite ao leitor desenvolver habilidades de interpretação e argumentação, compétencias essenciais para a compreensão crítica da realidade nacional e para o exercício pleno da cidadania.",
        f"O debate contemporâneo sobre {topic} revela tensões entre tradição e modernidade. As novas gerações brasileiras enfrentam desafios inéditos que exigem repensar conceitos e valores historicamente estabelecidos. Essa reflexão pode ser encontrada em diversos gêneros textuais, desde a crônica até o ensaio acadêmico, cada um à sua maneira contribuindo para o aprofundamento da discussão.",
        f"Em tempos de {topic}, a importância da leitura e da interpretação de texto torna-se ainda mais evidente. A capacidade de compreender, analisar e avaliar informações é fundamental para a formação de cidadãos críticos e participativos. Textos de diferentes gêneros oferecem subsídios valiosos para essa reflexão, convidando o leitor a ir além da simples decodificação das palavras."
    ]
    perguntas = [
        "A respeito do texto, assinale a alternativa que apresenta uma interpretação correta.",
        "Considere as ideias expressas no texto acima. Assinale a alternativa que melhor sintetiza a mensagem do autor.",
        "Com base na leitura do texto, é CORRETO afirmar que",
        "No trecho apresentado, a expressão sublinhada pode ser interpretada como",
        "Sobre o texto, assinale a alternativa que apresenta a ideia central."
    ]
    alternativas = [
        [
            "A) O autor defende que o tema não merece atenção da sociedade.",
            "B) O texto apresenta uma visão otimista e desproblematizada do tema.",
            "C) O autor busca demonstrar a complexidade e a relevância do tema na sociedade atual.",
            "D) O texto propõe uma solução definitiva para os problemas apresentados.",
            "E) A obra ignora completamente as transformações culturais recentes."
        ],
        [
            "A) O autor demonstra total concordância com as mudanças sociais ocorridas.",
            "B) O texto sugere que as transformações sociais devem ser ignoradas pela população.",
            "C) O autor reflete sobre os impactos das transformações sociais de forma crítica e ponderada.",
            "D) O texto apresenta apenas aspectos positivos das mudanças culturais.",
            "E) O autor se limita a descrever os fatos sem emitir qualquer tipo de juízo."
        ],
        [
            "A) A literatura é irrelevante para a compreensão dos fenômenos sociais contemporâneos.",
            "B) As mudanças culturais são exclusivas da realidade brasileira.",
            "C) A interpretação de textos contribui para a formação de uma consciência crítica sobre a realidade.",
            "D) O debate público sobre temas sociais é desnecessário em uma democracia.",
            "E) As novas gerações são incapazes de compreender as transformações culturais."
        ],
        [
            "A) A expressão indica rejeição total ao progresso tecnológico.",
            "B) A expressão revela a tensão entre o que é tradicional e o que é novo na sociedade.",
            "C) A expressão apresenta uma solução para os problemas sociais.",
            "D) A expressão indica indiferença do autor diante das mudanças.",
            "E) A expressão demonstra apoio incondicional às inovações."
        ],
        [
            "A) O tema abordado é restrito a um público acadêmico.",
            "B) O autor não apresenta argumentos para sustentar suas ideias.",
            "C) O texto evidencia a importância da reflexão crítica sobre questões contemporâneas.",
            "D) A mensagem do texto é contraditória e confusa.",
            "E) O autor ignora o contexto histórico e cultural do tema."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_linguagens_ingles(year, seq, topic):
    contexts = [
        f"Read the following text about {topic}, published in an international news outlet in {year}.",
        f"Read the excerpt from an English article discussing {topic} and its global implications.",
        f"Read the passage below about {topic} from an academic publication.",
    ]
    textos = [
        f"The discussion around {topic} has gained significant momentum in recent years. Experts from various fields have been analyzing the long-term effects of these changes on societies worldwide. In particular, researchers have noted that young people are at the forefront of adapting to new realities, often leading the way in finding innovative solutions to complex problems. This phenomenon raises important questions about the role of education and technology in shaping the future.",
        f"Global conversations about {topic} have intensified as more data becomes available. Studies indicate that the challenges we face require collaborative efforts between governments, the private sector, and civil society. The complexity of these issues demands a multidisciplinary approach that considers economic, social, and environmental factors. As we move forward, it is essential that policies are evidence-based and inclusive.",
        f"In recent years, the topic of {topic} has become a central point of discussion in international forums. According to leading experts, the choices made today will have lasting consequences for future generations. The balance between economic growth and environmental protection remains one of the most pressing challenges of our time. Finding sustainable solutions requires innovation, cooperation, and a willingness to rethink traditional approaches.",
    ]
    perguntas = [
        "According to the text, which of the following statements is correct?",
        "Based on the passage, what can be inferred about the author's main argument?",
        "The word 'momentum' in the first paragraph is closest in meaning to",
        "What is the main idea presented in the text?",
        "According to the passage, what is essential for addressing the challenges discussed?"
    ]
    alternativas = [
        [
            "A) The author argues that the topic is irrelevant to modern society.",
            "B) The text suggests that young people are passive observers of change.",
            "C) The passage highlights the importance of collaboration and innovation in addressing global challenges.",
            "D) The author believes that traditional approaches are always superior.",
            "E) The text claims that technology alone can solve all problems."
        ],
        [
            "A) The author is completely opposed to any form of change.",
            "B) The main argument is that economic growth should always take priority over other concerns.",
            "C) The author advocates for a balanced and evidence-based approach to complex challenges.",
            "D) The text suggests that governments should act alone without input from other sectors.",
            "E) The author believes that the challenges discussed are exaggerated."
        ],
        [
            "A) Speed and physical movement",
            "B) Strength and power",
            "C) Impetus or driving force",
            "D) Confusion and disorder",
            "E) Silence and stillness"
        ],
        [
            "A) Technology is the only solution to global problems.",
            "B) Complex challenges require multifaceted and collaborative approaches.",
            "C) Economic growth is impossible without environmental destruction.",
            "D) Young people are unwilling to participate in solving global issues.",
            "E) International cooperation has proven to be ineffective."
        ],
        [
            "A) Isolating each country to develop independent solutions.",
            "B) Ignoring scientific evidence in favor of political interests.",
            "C) Innovation, cooperation, and a willingness to rethink traditional approaches.",
            "D) Eliminating all technological advancements to return to simpler times.",
            "E) Focusing exclusively on short-term economic gains."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_linguagens_espanhol(year, seq, topic):
    contexts = [
        f"Lee el siguiente texto en español sobre {topic}, publicado en un medio internacional en {year}.",
        f"Lee el fragmento del artículo en español a continuación, que aborda {topic}.",
        f"Lee el siguiente párrafo en español que reflexiona sobre {topic}.",
    ]
    textos = [
        f"El tema de {topic} ha cobrado especial relevancia en los últimos años. Diversos estudios señalan que los cambios sociales y culturales experimentados por las sociedades contemporáneas plantean interrogantes importantes sobre el papel del individuo en la construcción del futuro. En este contexto, la reflexión crítica se convierte en una herramienta indispensable para comprender las transformaciones del mundo actual.",
        f"En los últimos tiempos, {topic} ha sido objeto de debates apasionados en diversos ámbitos de la sociedad. Los expertos coinciden en señalar que las nuevas generaciones enfrentan desafíos sin precedentes que requieren respuestas innovadoras y creativas. La capacidad de adaptación y la flexibilidad se presentan como competencias fundamentales para navegar en un mundo en constante transformación.",
        f"La discusión sobre {topic} en el mundo hispanohablante refleja una preocupación creciente por los desafíos que enfrenta la humanidad. Las comunidades científicas y académicas han señalado la urgencia de tomar medidas concretas para abordar estos problemas. La colaboración internacional y el intercambio de conocimientos se presentan como vías prometedoras para encontrar soluciones efectivas.",
    ]
    perguntas = [
        "Según el texto, ¿cuál de las siguientes afirmaciones es correcta?",
        "Con base en la lectura, se puede inferir que",
        "La expresión 'herramienta indispensable' en el primer párrafo puede interpretarse como",
        "¿Cuál es la idea central del texto?",
        "De acuerdo con el pasaje, ¿qué es fundamental para enfrentar los desafíos descritos?"
    ]
    alternativas = [
        [
            "A) El autor considera que el tema carece de importancia para la sociedad.",
            "B) El texto presenta una visión pesimista y desalentadora del futuro.",
            "C) El autor subraya la importancia de la reflexión crítica para comprender las transformaciones actuales.",
            "D) El texto propone eliminar todos los avances tecnológicos.",
            "E) El autor afirma que las nuevas generaciones son incapaces de adaptarse."
        ],
        [
            "A) El tema tratado es exclusivo de los países hispanohablantes.",
            "B) Los cambios sociales no afectan la vida cotidiana de las personas.",
            "C) Las nuevas generaciones enfrentan desafíos que requieren respuestas innovadoras.",
            "D) La reflexión crítica no tiene ningún valor práctico.",
            "E) Los expertos no tienen opiniones formadas sobre el tema."
        ],
        [
            "A) Un objeto físico用来cortar materiales.",
            "B) Un medio irrelevante para la comprensión del mundo.",
            "C) Un recurso esencial y necesariopara entender y actuar sobre la realidad.",
            "D) Una herramienta exclusiva de los científicos.",
            "E) Un concepto sin relación con la vida cotidiana."
        ],
        [
            "A) El texto defiende el aislamiento de cada nación.",
            "B) La idea central es que los desafíos actuales requieren respuestas colaborativas e innovadoras.",
            "C) El autor sugiere que la tecnología es el único camino.",
            "D) El texto propone volver a un pasado sin cambios.",
            "E) La idea principal es que no existen problemas importantes."
        ],
        [
            "A) Ignorar los avances científicos y tecnológicos.",
            "B) Actuar de manera individual sin consultar a otros países.",
            "C) La colaboración internacional y el intercambio de conocimientos.",
            "D) Eliminar toda forma de educación formal.",
            "E) Esperar pasivamente a que los problemas se resuelvan solos."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_linguagens_literatura(year, seq, topic):
    contexts = [
        f"Leia o trecho de obra literária brasileira que aborda reflexões sobre {topic}.",
        f"Leia o fragmento de poema que contempla temas como {topic} e a condição humana.",
        f"Leia o conto a seguir, que utiliza {topic} como pano de fundo para sua narrativa.",
    ]
    textos = [
        f"A literatura brasileira sempre esteve em diálogo com as transformações da sociedade. Em tempos de {topic}, os escritores encontram na palavra artística um instrumento poderoso para questionar, denunciar e propor novas formas de compreender o mundo. A poesia e a prosa contemporâneas refletem a complexidade da experiência humana em meio a mudanças aceleradas.",
        f"As grandes obras da literatura nacional retratam as contradições e os anseios do povo brasileiro. O tema {topic} aparece de diversas formas na produção literária, desde a crônica cotidiana até o romance épico. A capacidade da literatura de captar as nuances da realidade a torna uma aliada fundamental na formação de leitores críticos e conscientes.",
        f"A tradição literária brasileira offers um rico acervo de textos que exploram as múltiplas facetas da experiência humana. Em {topic}, os autores contemporâneos dialogam com a tradição ao mesmo tempo em que inovam formas de expressão, criando obras que ressoam com as inquietações da sociedade atual.",
    ]
    perguntas = [
        "Sobre o trecho literário apresentado, é CORRETO afirmar que",
        "A obra em questão utiliza {topic} como tema para",
        "No fragmento, a linguagem empregada pelo autor sugere",
        "A literatura, conforme apresentada no texto, funciona como",
        "O autor do trecho busca, por meio de sua obra,"
    ]
    alternativas = [
        [
            "A) A literatura brasileira é desprovida de relevância social.",
            "B) O autor utiliza a arte como forma de reflexão sobre a realidade.",
            "C) As obras literárias não têm qualquer influência na formação do leitor.",
            "D) A poesia contemporânea é incapaz de abordar temas relevantes.",
            "E) O texto literário deve sempre ser interpretado de forma literal."
        ],
        [
            "A) Distrair o leitor de problemas sociais urgentes.",
            "B) Explorar as contradições e complexidades da condição humana.",
            "C) Promover uma visão simplificada da realidade.",
            "D) Eliminar qualquer possibilidade de interpretação múltipla.",
            "E) Reproduzir fielmente apenas fatos históricos."
        ],
        [
            "A) Total desinteresse pelas questões sociais.",
            "B) Engajamento político de forma direta e explícita.",
            "C) Uma sensibilidade apurada para captar as nuances da realidade.",
            "D) Rejeição a qualquer forma de inovação estilística.",
            "E) Indiferença diante das transformações culturais."
        ],
        [
            "A) Um obstáculo à compreensão da realidade.",
            "B) Um instrumento de alienação cultural.",
            "C) Um espelho que reflete e permite compreender a sociedade.",
            "D) Uma forma de entretenimento desprovida de sentido.",
            "E) Um meio de propagar apenas ideias conservadoras."
        ],
        [
            "A) Reproduzir fielmente a realidade sem qualquer crítica.",
            "B) Oferecer ao leitor uma nova perspectiva para compreender o mundo.",
            "C) Eliminar qualquer possibilidade de questionamento.",
            "D) Distanciar completamente o leitor da sociedade.",
            "E) Impor uma única forma de interpretação."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_linguagens_artes(year, seq, topic):
    contexts = [
        f"Leia o texto abaixo sobre expressões artísticas e {topic}.",
        f"Leia o trecho que aborda a relação entre {topic} e as artes visuais.",
    ]
    textos = [
        f"As artes visuais no Brasil contemporâneo dialogam profundamente com as transformações culturais e sociais. {topic.title()} tem sido uma constante na produção artística nacional, onde artistas utilizam diversas linguagens para expressar suas visões de mundo. A pintura, a escultura, o cinema e as artes digitais convergem para criar experiências que desafiam a percepção do público e estimulam o pensamento crítico.",
        f"A relação entre {topic} e a expressão artística é objeto de estudo de diversas áreas do conhecimento. Nas galerias e museus brasileiros, obras que abordam temas contemporâneos têm atraído cada vez mais público, evidenciando o papel das artes como veículo de comunicação e transformação social. A arte contemporânea brasileira destaca-se pela sua capacidade de incorporar novas tecnologias e formulair novas estéticas."
    ]
    perguntas = [
        "Sobre as artes visuais e seu diálogo com o tema, é CORRETO afirmar que",
        "O texto sugere que a arte contemporânea brasileira caracteriza-se por"
    ]
    alternativas = [
        [
            "A) As artes visuais são irrelevantes para a compreensão cultural.",
            "B) A produção artística brasileira não dialoga com temas contemporâneos.",
            "C) As artes funcionam como veículo de comunicação e reflexão sobre a realidade.",
            "D) A arte deve ser restrita a elites intelectuais.",
            "E) As novas tecnologias prejudicam a produção artística."
        ],
        [
            "A) Rejeitar qualquer forma de inovação tecnológica.",
            "B) Isolar-se das transformações sociais e culturais.",
            "C) Incorporar novas tecnologias e criar estéticas inovadoras.",
            "D) Reproduzir apenas temas clássicos e tradicionais.",
            "E) Evitar qualquer tipo de diálogo com o público."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_linguagens_edfisica(year, seq, topic):
    contexts = [
        f"Leia o texto abaixo sobre a importância da educação física no contexto de {topic}.",
        f"Leia o trecho que discute a relação entre atividade física e {topic}.",
    ]
    textos = [
        f"A educação física tem desempenhado um papel fundamental na promoção da saúde e do bem-estar da população brasileira. Em tempos de {topic}, a prática de atividades físicas ganhou novos significados, passando a ser reconhecida como instrumento importante para a melhoria da qualidade de vida. Estudos demonstram que a atividade física regular contribui para a prevenção de diversas doenças e para a melhoria da saúde mental.",
        f"O esporte e a atividade física são instrumentos poderosos de inclusão social e promoção da cidadania. No contexto de {topic}, programas de educação física escolar têm se mostrado eficazes no combate ao sedentarismo e na formação de hábitos saudáveis. A prática esportiva also favorece o desenvolvimento de competências sociais como trabalho em equipe, disciplina e respeito ao próximo."
    ]
    perguntas = [
        "Sobre o texto, é CORRETO afirmar que",
        "A educação física, conforme apresentada, contribui para"
    ]
    alternativas = [
        [
            "A) A atividade física é prejudicial à saúde mental.",
            "B) A educação física não tem qualquer relevância social.",
            "C) A prática regular de exercícios contribui para a melhoria da qualidade de vida.",
            "D) O esporte é exclusivo para atletas profissionais.",
            "E) A educação física deve ser eliminada do currículo escolar."
        ],
        [
            "A) Aumentar o sedentarismo na população.",
            "B) Excluir indivíduos da sociedade.",
            "C) Promover inclusão social e formação de hábitos saudáveis.",
            "D) Reduzir a expectativa de vida.",
            "E) Diminuir o desempenho acadêmico dos alunos."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_linguagens_tic(year, seq, topic):
    contexts = [
        f"Leia o texto abaixo sobre tecnologia da informação e comunicação no contexto de {topic}.",
    ]
    textos = [
        f"As tecnologias da informação e comunicação (TICs) transformaram profundamente a sociedade brasileira nos últimos anos. No contexto de {topic}, ferramentas digitais têm sido utilizadas para ampliar o acesso à informação, melhorar processos educacionais e fortalecer a cidadania. O letramento digital tornou-se uma competência essencial para a participação ativa na sociedade do conhecimento. Segundo pesquisadores, o uso responsável das TICs pode contribuir significativamente para a redução das desigualdades sociais."
    ]
    perguntas = [
        "Com base no texto, é CORRETO afirmar que"
    ]
    alternativas = [
        [
            "A) As TICs são prejudicais para a sociedade.",
            "B) O letramento digital não é importante na sociedade atual.",
            "C) As tecnologias digitais podem contribuir para a redução de desigualdades quando bem utilizadas.",
            "D) A tecnologia deve ser evitada por todos os cidadãos.",
            "E) As TICs não têm qualquer impacto na educação."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_humanas_historia(year, seq, topic):
    contexts = [
        f"Leia o trecho abaixo que aborda aspectos históricos relacionados a {topic}.",
        f"Leia o texto historiográfico sobre {topic} e seus desdobramentos na sociedade brasileira.",
        f"Leia o fragmento de obra acadêmica que analisa {topic} no contexto nacional.",
    ]
    textos = [
        f"A história do Brasil é marcada por processos sociais complexos que moldaram a identidade nacional. {topic.title()} representam momentos significativos nessa trajetória, evidenciando as tensões entre diferentes grupos sociais e as transformações políticas e econômicas que se seguiram. A análise histórica permite compreender como passado e presente se articulam na construção da realidade contemporânea.",
        f"O estudo da história do Brasil revela uma rica teia de acontecimentos que influenciaram diretamente a formação da sociedade brasileira. No que se refere a {topic}, é possível identificar continuidades e rupturas que marcam as relações de poder, as dinâmicas culturais e as estruturas econômicas. A perspectiva historiográfica contemporânea valoriza a diversidade de vozes e experiências que compõem o mosaico da história nacional.",
        f"Os processos históricos que envolvem {topic} são fundamentais para a compreensão da sociedade brasileira atual. A relação entre passado e presente revela como as estruturas sociais, econômicas e culturais foram se constituindo ao longo do tempo. A historiografia brasileira tem se renovado ao incorporar novas perspectivas teóricas e metodológicas, ampliando a compreensão sobre os mais variados aspectos da experiência histórica nacional.",
    ]
    perguntas = [
        "Sobre o tema histórico apresentado, é CORRETO afirmar que",
        "A análise histórica apresentada permite concluir que",
        "No que se refere ao tema abordado, a historiografia contemporânea",
    ]
    alternativas = [
        [
            "A) A história do Brasil é um processo linear e sem contradições.",
            "B) Os processos históricos são determinados exclusivamente por fatores econômicos.",
            "C) A compreensão do passado é fundamental para interpretar o presente.",
            "D) A história não tem relevância para a compreensão da sociedade atual.",
            "E) Os fatos históricos devem ser interpretados de forma isolada."
        ],
        [
            "A) O passado não tem qualquer influência sobre o presente.",
            "B) As estruturas sociais são imutáveis ao longo do tempo.",
            "C) As transformações históricas são resultado de múltiplos fatores interrelacionados.",
            "D) A única causa das mudanças históricas é a ação de líderes individuais.",
            "E) O estudo da história é inútil para a compreensão da realidade."
        ],
        [
            "A) Rejeita todas as novas perspectivas teóricas.",
            "B) Mantém-se estática desde o século XIX.",
            "C) Valoriza a diversidade de vozes e experiências históricas.",
            "D) Considera apenas a perspectiva das elites governantes.",
            "E) Ignora completamente os aspectos culturais da história."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_humanas_geografia(year, seq, topic):
    contexts = [
        f"Leia o texto geográfico abaixo sobre {topic} e suas implicações territoriais.",
        f"Leia o trecho que analisa as relações espaciais e {topic} no contexto brasileiro.",
        f"Leia o fragmento que aborda questões geográficas relacionadas a {topic}.",
    ]
    textos = [
        f"A geografia brasileira revela uma grande diversidade de paisagens e processos territoriais que refletem as desigualdades sociais e econômicas do país. {topic.title()} são fatores que influenciam diretamente a organização do espaço geográfico e a distribuição da população. A análise geográfica permite compreender como fatores naturais e antrópicos interagem na construção do território brasileiro.",
        f"Os processos de urbanização e ocupação do território brasileiro são marcados por intensas contradições. No que se refere a {topic}, é possível observar como as dinâmicas socioespaciais produzem tanto oportunidades quanto desafios para a população. A geografia crítica tem se destacado ao analisar as relações de poder que se expressam na organização do espaço e nas disparidades regionais.",
        f"O estudo da geografia do Brasil permite compreender as múltiplas dimensões que caracterizam o território nacional. {topic.title()} representam desafios significativos para o planejamento territorial e para a promoção do desenvolvimento sustentável. A relação entre homem e meio ambiente é mediada por processos sociais, econômicos e políticos que determinam a forma como o espaço é apropriado e transformado."
    ]
    perguntas = [
        "Sobre a questão geográfica apresentada, é CORRETO afirmar que",
        "A análise geográfica permite concluir que",
        "No que se refere ao tema territorial abordado,"
    ]
    alternativas = [
        [
            "A) O território brasileiro é homogêneo em todos os aspectos.",
            "B) A geografia não tem qualquer relevância para o planejamento urbano.",
            "C) As desigualdades sociais se expressam na organização do espaço geográfico.",
            "D) Os fatores naturais determinam isoladamente a organização do território.",
            "E) A população brasileira distribui-se uniformemente pelo país."
        ],
        [
            "A) A relação entre sociedade e espaço é desprezível.",
            "B) Os processos territoriais são exclusivamente naturais.",
            "C) As dinâmicas socioespaciais são resultado de múltiplos fatores.",
            "D) O planejamento territorial é desnecessário.",
            "E) As disparidades regionais não existem no Brasil."
        ],
        [
            "A) As desigualdades regionais estão diminuindo progressivamente.",
            "B) O planejamento territorial não afeta a vida da população.",
            "C) Os desafios territoriais exigem abordagens integradas e sustentáveis.",
            "D) O meio ambiente não é afetado pelas atividades humanas.",
            "E) A organização do espaço é determinada apenas pelo clima."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_humanas_sociologia(year, seq, topic):
    contexts = [
        f"Leia o texto sociológico que aborda {topic} na sociedade brasileira.",
        f"Leia o trecho que analisa as relações sociais no contexto de {topic}.",
    ]
    textos = [
        f"A sociologia brasileira tem se debruçado sobre as múltiplas dimensões da vida social contemporânea. {topic.title()} representam fenômenos sociais que afetam diretamente as relações interpessoais e a organização coletiva. A análise sociológica permite compreender como estruturas sociais, culturais e econômicas se entrelaçam para produzir as desigualdades e as possibilidades de transformação social.",
        f"Os processos de mudança social no Brasil são marcados por tensões e contradições que refletem a complexidade da sociedade brasileira. No que se refere a {topic}, a sociologia oferece ferramentas conceituais para analisar as relações de poder, os processos de exclusão e inclusão social, e as dinâmicas culturais que caracterizam o cenário nacional. A compreensão desses fenômenos é fundamental para o exercício da cidadania plena.",
    ]
    perguntas = [
        "Sobre a questão sociológica apresentada, é CORRETO afirmar que",
        "A análise sociológica permite compreender que"
    ]
    alternativas = [
        [
            "A) A sociedade brasileira é composta por grupos sociais homogêneos.",
            "B) As relações sociais são determinadas exclusivamente pela economia.",
            "C) A sociologia oferece instrumentos para compreender as desigualdades e transformações sociais.",
            "D) As mudanças sociais são impossíveis em uma democracia.",
            "E) A organização social não é influenciada por fatores culturais."
        ],
        [
            "A) As desigualdades sociais são naturais e inevitáveis.",
            "B) A exclusão social não tem consequências para a sociedade.",
            "C) As relações de poder se expressam em diversas esferas da vida social.",
            "D) A cidadania plena é incompatível com a diversidade cultural.",
            "E) As transformações sociais são determinadas exclusivamente pelo Estado."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_humanas_filosofia(year, seq, topic):
    contexts = [
        f"Leia o texto filosófico que reflete sobre {topic} e suas implicações éticas.",
        f"Leia o trecho que aborda questões filosóficas relacionadas a {topic}.",
    ]
    textos = [
        f"A reflexão filosófica sobre {topic} convida o leitor a repensar seus valores e concepções de mundo. O pensamento filosófico, desde a Antiguidade até os dias atuais, tem se voltado para as grandes questões que assombram a humanidade: justiça, liberdade, igualdade, dignidade. No contexto brasileiro, a filosofia pode contribuir para a formação de cidadãos mais críticos e conscientes de sua posição na sociedade.",
        f"O diálogo entre filosofia e {topic} revela a relevância do pensamento crítico na construção de uma sociedade mais justa. As grandes questões éticas e políticas que permeiam o debate contemporâneo encontram na tradição filosófica um acervo de reflexões que podem iluminar os caminhos para a superação dos desafios atuais. A filosofia não se limita ao mundo acadêmico, mas interpela cada cidadão a refletir sobre seu papel no mundo.",
    ]
    perguntas = [
        "Sobre a reflexão filosófica apresentada, é CORRETO afirmar que",
        "A filosofia, conforme descrita no texto, contribui para"
    ]
    alternativas = [
        [
            "A) A filosofia é irrelevante para a vida cotidiana.",
            "B) O pensamento crítico é desnecessário em uma democracia.",
            "C) A reflexão filosófica contribui para a formação de cidadãos críticos e conscientes.",
            "D) As grandes questões éticas não têm relação com a sociedade atual.",
            "E) A filosofia deve ser restrita aos acadêmicos."
        ],
        [
            "A) Aumentar a passividade dos cidadãos.",
            "B) Eliminar qualquer forma de questionamento.",
            "C) Promover o pensamento crítico e a reflexão sobre valores e concepções de mundo.",
            "D) Manter as desigualdades sociais inalteradas.",
            "E) Impor uma única forma de pensar."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_natureza_fisica(year, seq, topic):
    contexts = [
        f"Leia o texto científico abaixo que aborda conceitos de física relacionados a {topic}.",
        f"Leia o trecho de artigo científico sobre aplicações da física no contexto de {topic}.",
        f"Leia o fragmento que discute princípios físicos e suas relações com {topic}.",
    ]
    textos = [
        f"A física é uma ciência que busca compreender as leis fundamentais que regem o universo. No contexto de {topic}, os princípios físicos desempenham papel essencial para o desenvolvimento tecnológico e científico. As equações e modelos físicos permitem descrever fenômenos naturais com precisão, desde o movimento dos corpos até o comportamento das partículas subatômicas. A compreensão desses conceitos é fundamental para a formação de profissionais capacitados para enfrentar os desafios científicos do século XXI.",
        f"Os avanços recentes na área de {topic} têm demonstrado a importância da física para a compreensão e transformação do mundo. Os conceitos de energia, força, movimento e onda são essenciais para o desenvolvimento de tecnologias que impactam diretamente a vida cotidiana. A pesquisa científica em física continua a revelar novos fenômenos e a aprimorar nossos conhecimentos sobre o funcionamento da natureza.",
    ]
    perguntas = [
        "Sobre os conceitos físicos apresentados, é CORRETO afirmar que",
        "A física, conforme descrita no texto, é fundamental para",
    ]
    alternativas = [
        [
            "A) A física não tem aplicação prática no mundo contemporâneo.",
            "B) Os princípios físicos são obsoletos e devem ser descartados.",
            "C) As leis da física permitem descrever fenômenos naturais com precisão.",
            "D) A pesquisa em física é desnecessária nos dias atuais.",
            "E) Os modelos físicos são sempre imprecisos e inúteis."
        ],
        [
            "A) Atrapalhar o desenvolvimento tecnológico.",
            "B) Impedir a compreensão do mundo natural.",
            "C) O desenvolvimento de tecnologias e a compreensão dos fenômenos naturais.",
            "D) Limitar o progresso científico.",
            "E) Tornar a ciência inacessível ao público geral."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_natureza_quimica(year, seq, topic):
    contexts = [
        f"Leia o texto sobre conceitos químicos e suas aplicações no contexto de {topic}.",
        f"Leia o trecho de artigo científico que aborda a química e {topic}.",
    ]
    textos = [
        f"A química é a ciência que estuda a composição, estrutura e transformação da matéria. No contexto de {topic}, os princípios químicos são fundamentais para o desenvolvimento de novos materiais, medicamentos e processos industriais sustentáveis. A compreensão das reações químicas e das propriedades dos elementos é essencial para a inovação tecnológica e para a busca de soluções para problemas ambientais e de saúde pública.",
        f"Os avanços na área de química têm proporcionado descobertas significativas que impactam diretamente a vida da população. No que se refere a {topic}, pesquisadores desenvolvem novos compostos e processos que contribuem para a melhoria da qualidade de vida. A química sustentável, em particular, tem se destacado ao propor alternativas menos agressivas ao meio ambiente para a produção de bens e serviços.",
    ]
    perguntas = [
        "Sobre os conceitos químicos apresentados, é CORRETO afirmar que",
        "A química, conforme descrita, contribui para"
    ]
    alteternativas = [
        [
            "A) A química não tem qualquer aplicação prática.",
            "B) Os princípios químicos são irrelevantes para o desenvolvimento tecnológico.",
            "C) A compreensão das reações químicas é essencial para a inovação e sustentabilidade.",
            "D) A pesquisa em química é prejudicial ao meio ambiente.",
            "E) A química sustentável é uma área sem futuro."
        ],
        [
            "A) Aumentar a poluição ambiental.",
            "B) Degrada a qualidade de vida da população.",
            "C) O desenvolvimento de soluções sustentáveis e a melhoria da qualidade de vida.",
            "D) Limitar o progresso científico.",
            "E) Tornar os processos industriais mais poluentes."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alteternativas))

def gen_natureza_biologia(year, seq, topic):
    contexts = [
        f"Leia o texto biológico que aborda questões relacionadas a {topic}.",
        f"Leia o trecho de artigo científico sobre {topic} e suas implicações para a biologia.",
        f"Leia o fragmento que discute conceitos biológicos no contexto de {topic}.",
    ]
    textos = [
        f"A biologia estuda os seres vivos e seus processos vitais, oferecendo subsídios para a compreensão da vida em todas as suas manifestações. No contexto de {topic}, os conhecimentos biológicos são fundamentais para o desenvolvimento de estratégias de conservação da biodiversidade, produção de alimentos e combate a doenças. A pesquisa científica na área da biologia continua a revelar novos mecanismos e processos que擴充am nosso entendimento sobre o funcionamento dos organismos vivos.",
        f"A compreensão dos processos biológicos é essencial para o enfrentamento dos desafios contemporâneos. No que se refere a {topic}, a biologia oferece ferramentas para a conservação ambiental, o desenvolvimento de biotecnologias e a busca por soluções para problemas de saúde pública. A integração entre biologia e outras áreas do conhecimento tem gerado avanços significativos em áreas como medicina, agricultura e preservação ambiental.",
    ]
    perguntas = [
        "Sobre os conceitos biológicos apresentados, é CORRETO afirmar que",
        "A biologia, conforme descrita no texto, é essencial para"
    ]
    alternativas = [
        [
            "A) A biologia não tem relevância para os problemas atuais.",
            "B) O estudo dos seres vivos é desnecessário nos dias atuais.",
            "C) Os conhecimentos biológicos são fundamentais para a conservação e o desenvolvimento sustentável.",
            "D) A biologia é uma ciência estagnada sem novas descobertas.",
            "E) A pesquisa biológica é prejudicial ao meio ambiente."
        ],
        [
            "A) Aumentar os problemas ambientais.",
            "B) Degrada a biodiversidade.",
            "C) A conservação ambiental, o desenvolvimento de biotecnologias e a saúde pública.",
            "D) Limitar o desenvolvimento agrícola.",
            "E) Tornar a pesquisa científica inacessível."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_mat_algebra(year, seq, topic):
    d, tx = diff()
    contexts = [
        f"Em uma situação do cotidiano relacionada a {topic}, é necessário utilizar conceitos de álgebra para resolver o problema apresentado.",
        f"Considere o problema abaixo, que envolve o uso de equações e expressões algébricas no contexto de {topic}.",
    ]
    textos = [
        f"Um pesquisador está analisando dados sobre {topic} e precisa建立 um modelo matemático para representar a relação entre duas grandezas. Ele observou que, ao aumentar uma variável em 5 unidades, outra variável aumenta proporcionalmente. A partir desses dados, é possível estabelecer uma equação que descreva essa relação e utilize-a para fazer previsões sobre comportamentos futuros.",
        f"Em um estudo sobre {topic}, foram coletados dados que podem ser representados por uma função do primeiro grau. A relação entre a variável independente e a variável dependente segue um padrão linear que permite calcular valores desconhecidos. A álgebra fornece as ferramentas necessárias para resolver esse tipo de problema de forma precisa e eficiente.",
    ]
    perguntas = [
        "Com base na situação apresentada, é CORRETO afirmar que a equação que representa a relação descrita é do tipo",
        "Considere o problema. O valor de x que satisfaz a equação apresentada é",
        "A respeito do problema, a expressão que melhor representa a situação é",
    ]
    alternativas = [
        [
            "A) Exponencial, pois as variáveis crescem de forma desproporcional.",
            "B) Do segundo grau, pois envolve uma multiplicação de variáveis.",
            "C) Do primeiro grau, pois a taxa de variação entre as variáveis é constante.",
            "D) Logarítmica, pois envolve potências.",
            "E) Não é possível determinar o tipo de equação com os dados fornecidos."
        ],
        [
            "A) x = -3, pois satisfaz a equação quando substituído.",
            "B) x = 0, pois qualquer equação tem zero como solução.",
            "C) x = 5, pois o enunciado menciona o número 5.",
            "D) x = 10, pois é o dobro de 5.",
            "E) A equação não possui solução real."
        ],
        [
            "A) y = 3x + 2, pois apresenta relação linear com coeficiente angular positivo.",
            "B) y = x² - 1, pois envolve uma potência.",
            "C) y = 2/x, pois indica relação inversamente proporcional.",
            "D) y = log(x), pois envolve escala logarítmica.",
            "E) y = e^x, pois apresenta crescimento exponencial."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_mat_geometria(year, seq, topic):
    contexts = [
        f"Considere uma situação prática envolvid几何a no contexto de {topic}.",
        f"Em um problema de geometria aplicada a {topic}, determine a resposta correta.",
    ]
    textos = [
        f"Um arquiteto está projetando um espaço que envolve conceitos geométricos fundamentais. No contexto de {topic}, é necessário calcular áreas, perímetros e volumes para garantir a eficiência do projeto. A geometria plana e espacial oferece as ferramentas matemáticas necessárias para resolver problemas como esse, que envolvem formas, medidas e relações entre figuras.",
        f"Em uma atividade de planejamento urbano relacionada a {topic}, os profissionais precisam utilizar conceitos de geometria para dimensionar espaços e calcular áreas de terrenos. A compreensão das propriedades geométricas das figuras é essencial para tomar decisões precisas e eficientes. A geometria analítica complementa esses cálculos ao permitir a representação de figuras em um sistema de coordenadas.",
    ]
    perguntas = [
        "A respeito do problema geométrico, é CORRETO afirmar que",
        "Considere a situação descrita. O cálculo solicitado pode ser resolvido utilizando",
    ]
    alternativas = [
        [
            "A) A geometria não tem aplicação em projetos arquitetônicos.",
            "B) O cálculo de áreas e perímetros é desnecessário no planejamento.",
            "C) Os conceitos geométricos são essenciais para o dimensionamento preciso de espaços.",
            "D) A geometria plana não se aplica a situações tridimensionais.",
            "E) As figuras geométricas não têm propriedades mensuráveis."
        ],
        [
            "A) Apenas operações aritméticas básicas.",
            "B) Somente fórmulas de estatística.",
            "C) Fórmulas de área, perímetro e volume, além de relações trigonométricas.",
            "D) Apenas cálculo diferencial.",
            "E) Não é possível resolver o problema com os dados fornecidos."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_mat_estatistica(year, seq, topic):
    contexts = [
        f"Considere os dados estatísticos apresentados sobre {topic}.",
        f"Em um estudo que analisa informações sobre {topic}, é necessário interpretar os dados fornecidos.",
    ]
    textos = [
        f"Um instituto de pesquisa coletou dados sobre {topic} em diversas regiões do Brasil. A análise estatística desses dados permite identificar tendências, medir dispersões e tomar decisões baseadas em evidências. Conceitos como média, mediana, desvio-padrão e coeficiente de variação são essenciais para a interpretação correta dos resultados obtidos.",
        f"Em um levantamento sobre {topic}, foram obtidos dados que podem ser analisados por meio de ferramentas estatísticas. A interpretação correta desses dados é fundamental para a formulação de políticas públicas e para a compreensão dos fenômenos sociais. A estatística descritiva oferece recursos para resumir e apresentar os dados de forma clara e objetiva.",
    ]
    perguntas = [
        "Com base nos dados estatísticos apresentados, é CORRETO afirmar que",
        "A respeito da análise estatística, o indicador que melhor representa a tendência central dos dados é",
    ]
    alternativas = [
        [
            "A) A estatística não tem aplicação na análise de dados sociais.",
            "B) Os dados estatísticos são sempre imprecisos e pouco confiáveis.",
            "C) A análise estatística permite identificar tendências e tomar decisões baseadas em evidências.",
            "D) A média é sempre o melhor indicador para qualquer tipo de dado.",
            "E) A estatística é irrelevante para a formulação de políticas públicas."
        ],
        [
            "A) A média, pois sempre representa fielmente todos os dados.",
            "B) A moda, pois indica o valor mais frequente.",
            "C) A mediana, pois é menos sensível a valores extremos.",
            "D) O desvio-padrão, pois mede a dispersão dos dados.",
            "E) O coeficiente de variação, pois indica a relação entre média e desvio."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

def gen_mat_probabilidade(year, seq, topic):
    contexts = [
        f"Considere a situação abaixo envolvendo cálculo de probabilidades no contexto de {topic}.",
        f"Em um experimento relacionado a {topic}, é necessário calcular a probabilidade de um evento ocorrer.",
    ]
    textos = [
        f"Um pesquisador está estudando {topic} e deseja calcular a probabilidade de determinados eventos ocorrerem. Para isso, ele utiliza conceitos fundamentais de teoria das probabilidades, como espaço amostral, eventos elementares e eventos independentes. A compreensão desses conceitos permite ao pesquisador fazer previsões razoáveis sobre fenômenos incertos.",
        f"Em um estudo sobre {topic}, foram observados eventos cuja ocorrência pode ser modelada por meio de probabilidades. A análise de dados permite estimar a chance de eventos específicos acontecerem, auxiliando na tomada de decisões. Os conceitos de probabilidade condicional e probabilidade conjunta são particularmente importantes nesse tipo de análise.",
    ]
    perguntas = [
        "Sobre o cálculo de probabilidades apresentado, é CORRETO afirmar que",
        "Considere o experimento descrito. A probabilidade do evento ocorrer é",
    ]
    alternativas = [
        [
            "A) A teoria das probabilidades não tem aplicação prática.",
            "B) Probabilidades sempre indicam certeza absoluta sobre o resultado.",
            "C) A análise probabilística permite estimar chances de eventos incertos.",
            "D) Eventos independentes sempre influenciam uns aos outros.",
            "E) A probabilidade é sempre igual a 50% para qualquer evento."
        ],
        [
            "A) 100%, pois todo evento irá ocorrer em algum momento.",
            "B) 0%, pois eventos incertos nunca acontecem.",
            "C) Um valor entre 0 e 1, calculado com base nos dados disponíveis.",
            "D) Apenas 50%, pois há duas possibilidades: ocorre ou não ocorre.",
            "E) Não é possível calcular probabilidades sem dados."
        ]
    ]
    return (pick(contexts), pick(textos), pick(perguntas), pick(alternativas))

GEN_FUNC = {
    "portugues": gen_linguagens_portugues,
    "ingles": gen_linguagens_ingles,
    "espanhol": gen_linguagens_espanhol,
    "literatura": gen_linguagens_literatura,
    "artes": gen_linguagens_artes,
    "educacao_fisica": gen_linguagens_edfisica,
    "tic": gen_linguagens_tic,
    "historia": gen_humanas_historia,
    "geografia": gen_humanas_geografia,
    "sociologia": gen_humanas_sociologia,
    "filosofia": gen_humanas_filosofia,
    "fisica": gen_natureza_fisica,
    "quimica": gen_natureza_quimica,
    "biologia": gen_natureza_biologia,
    "algebra": gen_mat_algebra,
    "geometria": gen_mat_geometria,
    "estatistica": gen_mat_estatistica,
    "probabilidade": gen_mat_probabilidade,
}

def generate_year(year):
    questions = []
    seq = 1
    topics = TOPICS[year]
    for area, discs in DISTRIBUTION.items():
        letter = AREA_LETTER[area]
        for disc, count in discs.items():
            gen = GEN_FUNC[disc]
            for i in range(count):
                d, tx = diff()
                topic = pick(topics)
                contexto, texto, pergunta, opcoes = gen(year, seq, topic)
                # Fix pergunta templates that may contain {topic}
                pergunta = pergunta.replace("{topic}", topic)
                for idx in range(len(opcoes)):
                    opcoes[idx] = opcoes[idx].replace("{topic}", topic)
                q = {
                    "id": f"{letter}{year}_{seq:02d}",
                    "ano": year,
                    "area": area,
                    "disciplina": disc,
                    "contexto": contexto,
                    "texto": texto,
                    "pergunta": pergunta,
                    "opcoes": opcoes,
                    "gabarito": random.choice(["A", "B", "C", "D", "E"]),
                    "dificuldade": d,
                    "taxaAcerto": tx
                }
                questions.append(q)
                seq += 1
    return questions

os.makedirs("data", exist_ok=True)
for year in [2021, 2022, 2023, 2024, 2025]:
    qs = generate_year(year)
    path = f"data/{year}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
    print(f"{path}: {len(qs)} questions written")
print("All files generated successfully!")
