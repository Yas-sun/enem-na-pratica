"""
Update dados.js with correct subtopic hierarchy based on SUBTOPICOS_OFICIAIS.
"""

import json
import re
import unicodedata
from pathlib import Path

# Official ENEM subtopics from subtopicos.js (SUBTOPICOS_OFICIAIS)
SUBTOPICOS_OFICIAIS = {
    "portugues": ["Interpretação de Texto", "Gramática Normativa", "Ortografia", "Pontuação", "Classes Gramaticais", "Sintaxe", "Semântica", "Concordância Verbal", "Regência Verbal", "Crase", "Vozes Verbais", "Coesão Textual", "Figuras de Linguagem"],
    "ingles": ["Interpretação de Texto em Inglês", "Vocabulário em Contexto", "Estruturas Gramaticais"],
    "espanhol": ["Interpretação de Texto em Espanhol", "Vocabulário em Contexto", "Estruturas Gramaticais"],
    "artes": ["Linguagens Artísticas", "Artes Visuais", "Música", "Teatro", "Dança", "História da Arte"],
    "literatura": ["Literatura Medieval", "Literatura Clássica", "Literatura Barroca", "Literatura Arcádica", "Literatura Romântica", "Literatura Realista", "Literatura Parnasiana", "Literatura Simbolista", "Literatura Moderna", "Literatura Contemporânea", "Movimentos Literários"],
    "historia": ["Pré-História", "Civilizações Antigas", "Idade Média", "Idade Moderna", "Descobrimentos e Colonização", "Brasil Colônia", "Iluminismo", "Revolução Industrial", "Independência do Brasil", "Brasil Imperial", "Abolição da Escravatura", "República Velha", "Revolução de 1930", "Era Vargas", "Estado Novo", "Redemocratização", "Regime Militar", "Contemporaneidade", "Movimentos Sociais", "Direitos Humanos"],
    "geografia": ["Espaço Geográfico", "Globalização", "Migrações e Urbanização", "Geografia do Brasil", "Regiões Brasileiras", "Relevo e Clima", "Hidrografia", "Vegetação", "População Brasileira", "Atividades Econômicas", "Agricultura e Pecuária", "Industrialização", "Geopolítica", "Meio Ambiente", "Desenvolvimento Sustentável", "Questões Sociais"],
    "sociologia": ["Cultura e Identidade", "Socialização e Grupos Sociais", "Estratificação Social", "Movimentos Sociais", "Cidadania e Democracia", "Educação", "Religião", "Comunicação e Opinião Pública", "Violência e Cidadania"],
    "filosofia": ["Origens do Pensamento Filosófico", "Filosofia Antiga", "Filosofia Medieval", "Filosofia Moderna", "Filosofia Contemporânea", "Ética", "Política", "Direitos Humanos", "Cidadania", "Liberdade e Igualdade"],
    "fisica": ["Cinemática", "Dinâmica", "Estática", "Gravitação Universal", "Trabalho e Energia", "Máquinas Simples", "Termodinâmica", "Calorimetria", "Ondulatória", "Óptica", "Eletricidade", "Eletrostática", "Eletrodinâmica", "Magnetismo", "Eletromagnetismo", "Física Moderna", "Relatividade", "Física Nuclear"],
    "quimica": ["Matéria e Mudanças", "Modelo Atômico", "Tabela Periódica", "Ligações Químicas", "Nomenclatura", "Reações Químicas", "Estequiometria", "Soluções", "Cinética Química", "Equilíbrio Químico", "Acidez e Alcalinidade", "Eletroquímica", "Química Orgânica", "Química Ambiental", "Química dos Alimentos", "Bioquímica"],
    "biologia": ["Bioquímica", "Citologia", "Genética", "Evolução", "Ecologia", "Biodiversidade", "Fisiologia Humana", "Sistema Nervoso", "Sistema Endócrino", "Sistema Reprodutor", "Sistema Circulatório", "Sistema Respiratório", "Sistema Digestório", "Sistema Excretor", "Sistema Imunológico", "Biotecnologia", "Saúde e Doenças", "Meio Ambiente"],
    "algebra": ["Números Naturais", "Números Inteiros", "Números Racionais", "Números Reais", "Conjuntos Numéricos", "Porcentagem", "Juros Simples e Compostos", "Proporção e Razão", "Equações do 1º Grau", "Equações do 2º Grau", "Sistemas Lineares", "Inequações", "Funções do 1º Grau", "Funções do 2º Grau", "Funções Polinomiais", "Funções Racionais", "Funções Exponenciais", "Funções Logarítmicas", "Progressão Aritmética", "Progressão Geométrica", "Princípios de Contagem", "Logaritmos"],
    "geometria": ["Geometria Plana", "Triângulos", "Quadriláteros", "Polígonos", "Circunferência e Círculo", "Área e Perímetro", "Geometria Espacial", "Prismas", "Pirâmides", "Corpos de Revolução", "Trigonometria", "Relações Trigonométricas", "Lei dos Senos", "Lei dos Cossenos", "Vetores", "Matrizes", "Plano Cartesiano", "Retas e Planos"],
    "estatistica": ["Estatística Descritiva", "Média Aritmética", "Mediana", "Moda", "Amplitude", "Desvio Padrão", "Gráficos", "Tabelas de Frequência", "Análise de Dados", "Fontes de Dados"],
    "probabilidade": ["Probabilidade", "Probabilidade Simples", "Probabilidade Composta", "Evento Independente", "Evento Dependente", "Espaço Amostral", "Árvore de Probabilidade"]
}

# Keyword mapping for each subtopic (only official subtopics)
SUBTOPIC_KEYWORDS = {
    "portugues": {
        "Interpretação de Texto": ["interpretação", "texto", "leitura", "compreensão", "interpretar"],
        "Gramática Normativa": ["gramática", "norma culta"],
        "Ortografia": ["ortografia"],
        "Pontuação": ["pontuação", "vírgula", "ponto final", "ponto e vírgula", "dois pontos"],
        "Classes Gramaticais": ["classe gramatical", "substantivo", "verbo", "adjetivo", "advérbio", "pronome", "preposição", "conjunção", "interjeição"],
        "Sintaxe": ["sintaxe", "sujeito", "predicado", "objeto", "oração"],
        "Semântica": ["semântica", "significado", "sinônimo", "antônimo", "polissemia", "homônimo"],
        "Concordância Verbal": ["concordância verbal", "concordância"],
        "Regência Verbal": ["regência", "regência verbal"],
        "Crase": ["crase"],
        "Vozes Verbais": ["voz ativa", "voz passiva", "voz reflexiva", "verbal"],
        "Coesão Textual": ["coesão", "coesão textual", "articulador", "conjunção coordenativa", "conjunção subordinativa"],
        "Figuras de Linguagem": ["figura de linguagem", "metáfora", "comparação", "hipérbole", "ironia", "símile", "personificação", "metonímia", "sinédoque", "antítese", "eufemismo"]
    },
    "historia": {
        "Pré-História": ["prè-história", "paleolítico", "neolítico", "pré-história"],
        "Civilizações Antigas": ["egito", "mesopotâmia", "roma", "grécia", "civilização antiga"],
        "Idade Média": ["idade média", "medieval", "feudalismo", "monarquia", "feudo"],
        "Idade Moderna": ["idade moderna", "absolutismo", "iluminismo", "mercantilismo"],
        "Descobrimentos e Colonização": ["descobrimentos", "navegação", "expansão marítima", "colonização"],
        "Brasil Colônia": ["colônia", "colonial", "capitanias", "porto seguro"],
        "Iluminismo": ["iluminismo", "enciclopédia", "voltaire", "rousseau"],
        "Revolução Industrial": ["revolução industrial", "mecanização", "fabricação", "fábrica"],
        "Independência do Brasil": ["independência do brasil", "dom pedro", "grito do ipiranga"],
        "Brasil Imperial": ["império", "dom pedro", "brasil imperial"],
        "Abolição da Escravatura": ["abolicionismo", "escravidão", "escravos", "lei áurea"],
        "República Velha": ["república velha", "café com leite", "coronelismo"],
        "Revolução de 1930": ["revolução de 1930", "getúlio vargas"],
        "Era Vargas": ["vargas", "estado novo", "getúlio"],
        "Estado Novo": ["estado novo", "vargas"],
        "Redemocratização": ["redemocratização", "abertura", "constituinte", "88"],
        "Regime Militar": ["regime militar", "ditadura militar", "ai-5", "militar"],
        "Contemporaneidade": ["contemporâneo", "contemporânea", "século xx", "globalização"],
        "Movimentos Sociais": ["movimento social", "greve", "protesto", "manifestação"],
        "Direitos Humanos": ["direitos humanos", "declaração universal", "onu"]
    },
    "geografia": {
        "Espaço Geográfico": ["espaço geográfico", "região", "lugar", "país"],
        "Globalização": ["globalização", "mundialização", "internacional"],
        "Migrações e Urbanização": ["migração", "imigração", "urbanização", "metrópole", "cidade"],
        "Geografia do Brasil": ["geografia do brasil", "brasil", "região brasileira"],
        "Regiões Brasileiras": ["nordeste", "sudeste", "sul", "norte", "centro-oeste", "região"],
        "Relevo e Clima": ["relevo", "clima", "temperatura", "chuva", "plano", "planalto", "serra"],
        "Hidrografia": ["hidrografia", "rio", "bacia", "lago", "águas"],
        "Vegetação": ["vegetação", "floresta", "bioma", "cerrado", "amazônia", "caatinga"],
        "População Brasileira": ["população", "demografia", "natalidade", "mortalidade"],
        "Atividades Econômicas": ["atividade econômica", "economia", "produção"],
        "Agricultura e Pecuária": ["agricultura", "pecuária", "lavoura", "gado", "colheita"],
        "Industrialização": ["industrialização", "indústria", "fábrica", "manufatura"],
        "Geopolítica": ["geopolítica", "poder", "conflito", "soberania"],
        "Meio Ambiente": ["meio ambiente", "desmatamento", "poluição", "sustentabilidade"],
        "Desenvolvimento Sustentável": ["desenvolvimento sustentável", "preservação", "conservação"],
        "Questões Sociais": ["questão social", "desigualdade", "pobreza", "exclusão"]
    },
    "sociologia": {
        "Cultura e Identidade": ["cultura", "identidade", "tradição", "social"],
        "Socialização e Grupos Sociais": ["socialização", "grupo social", "interação"],
        "Estratificação Social": ["estratificação", "classe social", "desigualdade", "renda"],
        "Movimentos Sociais": ["movimento social", "greve", "protesto", "manifestação", "mst"],
        "Cidadania e Democracia": ["cidadania", "cidadão", "democracia", "participação", "constituição"],
        "Educação": ["educação", "escola", "ensino", "aprendizagem"],
        "Religião": ["religião", "fé", "crença"],
        "Comunicação e Opinião Pública": ["mídia", "comunicação", "jornal", "opinião pública", "imprensa"],
        "Violência e Cidadania": ["violência", "crime", "segurança", "cidadania"]
    },
    "filosofia": {
        "Origens do Pensamento Filosófico": ["sócrates", "platão", "filosofia antiga"],
        "Filosofia Antiga": ["sócrates", "platão", "aristóteles", "estoicismo", "epicurismo"],
        "Filosofia Medieval": ["filosofia medieval", "escolástica", "tomismo", "agostinho", "tomás de aquino"],
        "Filosofia Moderna": ["descartes", "kant", "hegel", "racionalismo", "empirismo"],
        "Filosofia Contemporânea": ["sartre", "foucault", "existencialismo", "pós-modernidade", "heidegger"],
        "Ética": ["ética", "moral", "bom", "mal", "justo"],
        "Política": ["política", "estado", "governo", "poder", "soberania"],
        "Direitos Humanos": ["direitos humanos", "liberdade", "igualdade"],
        "Cidadania": ["cidadania", "cidadão", "democracia"],
        "Liberdade e Igualdade": ["liberdade", "igualdade", "direitos"]
    },
    "fisica": {
        "Cinemática": ["cinemática", "deslocamento", "velocidade", "aceleração", "trajetória"],
        "Dinâmica": ["dinâmica", "força", "newton", "lei", "massa", "atrito"],
        "Estática": ["estática", "equilíbrio", "repouso", "equilíbrio de forças"],
        "Gravitação Universal": ["gravitação", "gravidade", "queda livre", "newton"],
        "Trabalho e Energia": ["trabalho", "energia", "potência", "calor"],
        "Máquinas Simples": ["máquina simples", "alavanca", "pólio", "roldana"],
        "Termodinâmica": ["termodinâmica", "temperatura", "calor", "entropia", "processo isotérmico", "processo adiabático", "calorimetria", "equilíbrio térmico"],
        "Calorimetria": ["calorimetria", "calor sensível", "calor latente"],
        "Ondulatória": ["onda", "frequência", "amplitude", "reflexão", "refração"],
        "Óptica": ["óptica", "luz", "reflexão", "refração", "lente", "espelho"],
        "Eletricidade": ["eletricidade", "carga", "campo elétrico", "potencial"],
        "Eletrostática": ["eletrostática", "carga", "force eletrostática"],
        "Eletrodinâmica": ["eletrodinâmica", "corrente", "tensão", "resistência"],
        "Magnetismo": ["magnetismo", "campo magnético", "ímã"],
        "Eletromagnetismo": ["eletromagnetismo", "elétric", "magnét", "indução"],
        "Física Moderna": ["física moderna", "quântica", "relatividade", "efeito fotoelétrico"],
        "Relatividade": ["relatividade", "einstein", "espaço-tempo"],
        "Física Nuclear": ["nuclear", "radioatividade", "fissão", "fusão"]
    },
    "quimica": {
        "Matéria e Mudanças": ["matéria", "substância", "mistura", "composto"],
        "Modelo Atômico": ["átomo", "modelo atômico", "próton", "elétron", "nêutron"],
        "Tabela Periódica": ["tabela periódica", "período", "grupo", "elemento químico"],
        "Ligações Químicas": ["ligação", "iônica", "covalente", "metálica"],
        "Nomenclatura": ["nomenclatura", "nome químico"],
        "Reações Químicas": ["reação", "química", "produto", "reactant", "combustão"],
        "Estequiometria": ["estequiometria", "mol", "massa molar", "rendimento"],
        "Soluções": ["solução", "soluto", "solvente", "concentração"],
        "Cinética Química": ["cinética", "velocidade de reação"],
        "Equilíbrio Químico": ["equilíbrio químico", "constante de equilíbrio"],
        "Acidez e Alcalinidade": ["ph", "ácido", "base", "neutralização"],
        "Eletroquímica": ["eletroquímica", "eletrólise", "pilha", "bateria"],
        "Química Orgânica": ["orgânico", "hidrocarboneto", "composto orgânico"],
        "Química Ambiental": ["química ambiental", "poluição", "meio ambiente"],
        "Química dos Alimentos": ["alimento", "nutrição", "carboidrato", "lipídio", "proteína"],
        "Bioquímica": ["bioquímica", "enzima", "metabolismo"]
    },
    "biologia": {
        "Bioquímica": ["bioquímica", "proteína", "enzima", "carboidrato", "lipídio"],
        "Citologia": ["célula", "citologia", "organela", "membrana plasmática"],
        "Genética": ["genética", "dna", "gene", "hereditariedade", "cromossomo"],
        "Evolução": ["evolução", "seleção natural", "adaptação", "darwin"],
        "Ecologia": ["ecologia", "ecossistema", "biodiversidade", "cadeia alimentar"],
        "Biodiversidade": ["biodiversidade", "espécie", "extinção"],
        "Fisiologia Humana": ["fisiologia", "sistema digestório", "sistema respiratório", "sistema circulatório"],
        "Sistema Nervoso": ["sistema nervoso", "neurônio", "sinapse"],
        "Sistema Endócrino": ["sistema endócrino", "hormônio"],
        "Sistema Reprodutor": ["sistema reprodutor", "reprodução"],
        "Sistema Circulatório": ["sistema circulatório", "sangue", "hemoglobina"],
        "Sistema Respiratório": ["sistema respiratório", "pulmão", "respiração"],
        "Sistema Digestório": ["sistema digestório", "digestão", "absorção"],
        "Sistema Excretor": ["sistema excretor", "rins", "urina"],
        "Sistema Imunológico": ["sistema imunológico", "anticorpo", "vacina", "imunidade"],
        "Biotecnologia": ["biotecnologia", "engenharia genética", "ogm", "clonagem"],
        "Saúde e Doenças": ["saúde", "doença", "câncer", "aids", "malária"],
        "Meio Ambiente": ["meio ambiente", "conservação", "desmatamento"]
    },
    "algebra": {
        "Números Naturais": ["número natural", "natural", "números"],
        "Números Inteiros": ["número inteiro", "inteiro"],
        "Números Racionais": ["número racional", "racional"],
        "Números Reais": ["número real", "real"],
        "Conjuntos Numéricos": ["conjunto", "conjunto numérico", "intervalo"],
        "Porcentagem": ["porcentagem", "porcento", "percentual"],
        "Juros Simples e Compostos": ["juros", "capital", "taxa", "tempo"],
        "Proporção e Razão": ["proporção", "razão", "proporcional"],
        "Equações do 1º Grau": ["equação do 1º grau", "equação do primeiro grau", "incógnita"],
        "Equações do 2º Grau": ["equação do 2º grau", "equação do segundo grau"],
        "Sistemas Lineares": ["sistema linear", "sistema de equações"],
        "Inequações": ["inequação", "inequação"],
        "Funções do 1º Grau": ["função do 1º grau", "função afim"],
        "Funções do 2º Grau": ["função do 2º grau", "função quadrática"],
        "Funções Polinomiais": ["função polinomial", "polinômio"],
        "Funções Racionais": ["função racional"],
        "Funções Exponenciais": ["função exponencial", "expoente"],
        "Funções Logarítmicas": ["função logarítmica", "logaritmo"],
        "Progressão Aritmética": ["progressão aritmética", "pa"],
        "Progressão Geométrica": ["progressão geométrica", "pg"],
        "Princípios de Contagem": ["princípio fundamental", "contagem", "combinatória"],
        "Logaritmos": ["logaritmo", "log"]
    },
    "geometria": {
        "Geometria Plana": ["geometria plana", "triângulo", "quadrilátero", "círculo", "área"],
        "Triângulos": ["triângulo", "retângulo", "pitágoras", "semelhança"],
        "Quadriláteros": ["quadrilátero", "paralelogramo", "retângulo", "quadrado"],
        "Polígonos": ["polígono", "vértice", "lado"],
        "Circunferência e Círculo": ["circunferência", "círculo", "diâmetro", "raio"],
        "Área e Perímetro": ["área", "perímetro"],
        "Geometria Espacial": ["geometria espacial", "volume", "sólido", "cubo", "esfera", "cilindro"],
        "Prismas": ["prisma", "volume"],
        "Pirâmides": ["pirâmide", "volume"],
        "Corpos de Revolução": ["corpo de revolução", "cone", "esfera"],
        "Trigonometria": ["trigonometria", "seno", "cosseno", "tangente", "ângulo"],
        "Relações Trigonométricas": ["lei dos senos", "lei dos cossenos", "relação trigonométrica"],
        "Lei dos Senos": ["lei dos senos"],
        "Lei dos Cossenos": ["lei dos cossenos"],
        "Vetores": ["vetor", "vetorial"],
        "Matrizes": ["matriz", "determinante"],
        "Plano Cartesiano": ["plano cartesiano", "coordenada"],
        "Retas e Planos": ["reta", "plano", "parallelismo"]
    },
    "estatistica": {
        "Estatística Descritiva": ["estatística descritiva", "média", "mediana", "moda"],
        "Média Aritmética": ["média", "aritmética"],
        "Mediana": ["mediana"],
        "Moda": ["moda"],
        "Amplitude": ["amplitude"],
        "Desvio Padrão": ["desvio padrão", "variância"],
        "Gráficos": ["gráfico", "histograma", "tabela"],
        "Tabelas de Frequência": ["tabela de frequência", "frequência"],
        "Análise de Dados": ["análise de dados", "interpretação de dados"],
        "Fontes de Dados": ["fonte", "censo", "pesquisa", "amostra"]
    },
    "probabilidade": {
        "Probabilidade": ["probabilidade", "chance", "evento"],
        "Probabilidade Simples": ["probabilidade simples"],
        "Probabilidade Composta": ["probabilidade composta", "condicional"],
        "Evento Independente": ["evento independente"],
        "Evento Dependente": ["evento dependente"],
        "Espaço Amostral": ["espaço amostral"],
        "Árvore de Probabilidade": ["árvore de probabilidade", "permutação", "arranjo", "combinação"]
    }
}


def get_subtopic_for_question(question):
    """Determine the correct subtopic based on official subtopics and keywords."""
    disc = question.get('disciplina', '')
    texto = unicodedata.normalize('NFC', question.get('texto', '').lower())
    pergunta = unicodedata.normalize('NFC', question.get('pergunta', '').lower())
    combined = texto + ' ' + pergunta
    
    subtopics = SUBTOPICOS_OFICIAIS.get(disc, [])
    if not subtopics:
        return ''
    
    keywords = SUBTOPIC_KEYWORDS.get(disc, {})
    
    # Check keywords for each subtopic
    for sub, words in keywords.items():
        if sub in subtopics:
            for word in words:
                if word.lower() in combined:
                    return sub
    
    # Default: return first subtopic in the official list
    return subtopics[0] if subtopics else ''


def main():
    d = Path(r"C:\Users\ffxtr\OneDrive\Documentos\opencode\enem-na-pratica\js\dados.js")
    c = d.read_text(encoding='utf-8')
    m = re.search(r'window\.BANCO_QUESTIONS\s*=\s*(\[.*?\]);', c, re.DOTALL)
    q = json.loads(m.group(1))
    
    updated = 0
    for question in q:
        new_sub = get_subtopic_for_question(question)
        if new_sub and new_sub != question.get('subtopico'):
            question['subtopico'] = new_sub
            updated += 1
    
    print(f"Updated {updated} subtopicos")
    
    new_json = json.dumps(q, ensure_ascii=False, separators=(',', ':'))
    new_content = c[:m.start()] + 'window.BANCO_QUESTIONS = ' + new_json + ';' + c[m.end():]
    d.write_text(new_content, encoding='utf-8')
    print("Updated dados.js")


if __name__ == "__main__":
    main()
