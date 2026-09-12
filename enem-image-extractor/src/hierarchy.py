"""
Correct ENEM subtopic hierarchy.
Each subtopic belongs to exactly one discipline, which belongs to one area.
"""

# Correct hierarchy: area > disciplina > subtopicos
ENEM_HIERARCHY = {
    'linguagens': {
        'portugues': [
            'Interpretação de Texto', 'Gêneros Textuais', 'Vozes Verbais',
            'Morfologia', 'Sintaxe', 'Semântica', 'Pontuação', 'Coesão',
            'Tom Textual', 'Tipologia Textual', 'Norma Culta', 'Regência',
            'Concordância', 'Ortografia', 'Acentuação', 'Crítica Literária',
            'Análise Sintática', 'Período Simples', 'Período Composto',
            'Funções da Linguagem', 'Elementos de Comunicação', 'Texto Informativo',
            'Texto Argumentativo', 'Texto Narrativo', 'Texto Descritivo',
            'Instrucional', 'Editorial', 'Crônica', 'Poema', 'Fábula',
            'Reportagem', 'Notícia', 'Charge', 'Cartaz', 'Anúncio'
        ],
        'ingles': [
            'Vocabulário Inglês', 'Gramática Inglesa',
            'Expressões Idiomáticas', 'Texto Argumentativo', 'Texto Informativo',
            'Connectors', 'Verb Tenses', 'Conditionals', 'Passive Voice',
            'Reported Speech', 'Relative Clauses', 'Phrasal Verbs'
        ],
        'espanhol': [
            'Vocabulário Espanhol', 'Gramática Espanhola',
            'Expresiones Idiomáticas', 'Texto Argumentativo', 'Texto Informativo',
            'Pretérito', 'Subjuntivo', 'Objetos Directos', 'Pronombres'
        ],
        'literatura': [
            'Movimentos Literários', 'Análise Literária', 'Figuras de Linguagem',
            'Metáfora', 'Comparação', 'Hipérbole', 'Ironia', 'Antítese',
            'Paradoxo', 'Símile', 'Personificação', 'Metonímia',
            'Sinédoque', 'Eufemismo', 'Catacrese', 'Prosopopeia',
            'Lirismo', 'Narrativa', 'Descritiva', 'Monólogo', 'Diálogo',
            'Romantismo', 'Realismo', 'Naturalismo', 'Modernismo',
            'Parnasianismo', 'Simbolismo', 'Concretismo', 'Tropicalismo',
            'Literatura Barroca', 'Literatura Clássica', 'Literatura Contemporânea'
        ],
        'artes': [
            'Artes Visuais', 'Música', 'Teatro', 'Dança', 'Cinema',
            'Fotografia', 'Arquitetura', 'Design', 'Grafite', 'Street Art',
            'Arte Digital', 'Instalação', 'Performance', 'Escultura',
            'Pintura', 'Desenho', 'Gravura', 'Xilogravura', 'Serigrafia',
            'Arte Primitiva', 'Arte Sacra', 'Arte Moderna', 'Arte Contemporânea',
            'Cubismo', 'Surrealismo', 'Impressionismo', 'Expressionismo',
            'Pop Art', 'Arte Abstrata', 'Arte Conceitual'
        ]
    },
    'humanas': {
        'historia': [
            'Pré-História', 'Civilizações Antigas', 'Idade Média', 'Idade Moderna',
            'Idade Contemporânea', 'Revolução Francesa', 'Revolução Industrial',
            'Brasil Colônia', 'Brasil Império', 'República Velha',
            'Era Vargas', 'Regime Militar', 'Redemocratização',
            'Guerras Mundiais', 'Guerra Fria',
            'Direitos Humanos', 'Abolicionismo',
            'Imigração', 'Industrialização',
            'Formação do Estado Nacional', 'Descolonização',
            'Fascismo', 'Nazismo', 'Comunismo', 'Liberalismo'
        ],
        'geografia': [
            'Geografia do Brasil', 'Geografia Mundial', 'Cartografia',
            'Climatologia', 'Geomorfologia', 'Hidrografia', 'Biogeografia',
            'Demografia', 'Urbanização', 'Migração', 'Globalização',
            'Meio Ambiente', 'Desenvolvimento Sustentável', 'Questão Agrária',
            'Reforma Agrária', 'Agricultura', 'Pecuária', 'Mineração',
            'Indústria', 'Comércio', 'Transportes', 'Energia',
            'Blocos Econômicos', 'Mercosul', 'ONU', 'FMI',
            'Questão Ambiental', 'Mudanças Climáticas', 'Desmatamento',
            'Poluição', 'Recursos Hídricos', 'Solo', 'Vegetação',
            'Relevo', 'Clima', 'Fuso Horário', 'Placas Tectônicas'
        ],
        'sociologia': [
            'Sociologia Geral', 'Classes Sociais',
            'Cultura', 'Identidade', 'Estratificação Social', 'Desigualdade',
            'Cidadania', 'Estado', 'Sociedade', 'Economia',
            'Religião', 'Educação', 'Família', 'Trabalho', 'Violência',
            'Mídia', 'Comunicação', 'Tecnologia', 'Meio Ambiente',
            'Gênero', 'Raça', 'Etnia', 'Classe', 'Poder', 'Instituição',
            'Socialização', 'Controle Social', 'Mudança Social'
        ],
        'filosofia': [
            'Filosofia Antiga', 'Filosofia Medieval', 'Filosofia Moderna',
            'Filosofia Contemporânea', 'Ética', 'Política', 'Estética',
            'Epistemologia', 'Metafísica', 'Lógica', 'Filosofia da Linguagem',
            'Filosofia da Mente', 'Filosofia da Ciência', 'Filosofia da História',
            'Sócrates', 'Platão', 'Aristóteles', 'Descartes', 'Kant',
            'Hegel', 'Marx', 'Nietzsche', 'Sartre', 'Foucault',
            'Existencialismo', 'Racionalismo', 'Empirismo', 'Idealismo',
            'Materialismo', 'Utilitarismo', 'Deontologia', 'Virtude',
            'Liberdade', 'Igualdade', 'Justiça', 'Verdade', 'Beleza'
        ]
    },
    'natureza': {
        'fisica': [
            'Mecânica', 'Cinemática', 'Dinâmica', 'Estática', 'Trabalho e Energia',
            'Termodinâmica', 'Calor', 'Temperatura', 'Entropia',
            'Eletromagnetismo', 'Carga Elétrica', 'Campo Elétrico',
            'Campo Magnético', 'Circuitos', 'Ondas', 'Óptica',
            'Acústica', 'Nuclear', 'Física Moderna', 'Relatividade',
            'Quântica', 'Semicondutores', 'Supercondutividade',
            'Gravitação', 'Leis de Newton', 'Princípio de Arquimedes',
            'Pressão', 'Velocidade', 'Aceleração', 'Força', 'Massa',
            'Energia Cinética', 'Energia Potencial', 'Conservação'
        ],
        'quimica': [
            'Química Geral', 'Ligações Químicas', 'Estrutura Atômica',
            'Tabela Periódica', 'Reações Químicas', 'Estequiometria',
            'Soluções', 'Acidoses e Bases', 'pH', 'Eletroquímica',
            'Termoquímica', 'Cinética Química', 'Equilíbrio Químico',
            'Química Orgânica', 'Hidrocarbonetos', 'Funções Orgânicas',
            'Alcoóis', 'Fenóis', 'Éteres', 'Aldeídos', 'Cetonas',
            'Ácidos Carboxílicos', 'Ésteres', 'Aminas', 'Amidas',
            'Química Inorgânica', 'Metais', 'Não-Metais', 'Gases',
            'Química Ambiental', 'Poluição', 'Reciclagem', 'Combustíveis',
            'Química dos Alimentos', 'Aditivos', 'Conservantes',
            'Química Farmacêutica', 'Medicamentos', 'Vacinas'
        ],
        'biologia': [
            'Citologia', 'Biologia Celular', 'Membrana Plasmática',
            'Organelas', 'Divisão Celular', 'Mitose', 'Meiose',
            'Genética', 'Hereditariedade', 'DNA', 'RNA', 'Genética Molecular',
            'Engenharia Genética', 'Biotecnologia', 'OGM', 'Clonagem',
            'Ecologia', 'Ecossistemas', 'Cadeias Alimentares', 'Fluxo de Energia',
            'Ciclo do Carbono', 'Ciclo da Água', 'Biodiversidade',
            'Conservação', 'Desmatamento', 'Mudanças Climáticas',
            'Evolução', 'Seleção Natural', 'Adaptação', 'Especiação',
            'Fisiologia', 'Sistema Digestório', 'Sistema Respiratório',
            'Sistema Circulatório', 'Sistema Nervoso', 'Sistema Endócrino',
            'Sistema Reprodutor', 'Sistema Imunológico', 'Sistema Excretor',
            'Anatomia', 'Histologia', 'Embriologia', 'Microbiologia',
            'Vírus', 'Bactérias', 'Fungos', 'Plantas', 'Animais',
            'Invertebrados', 'Vertebrados', 'Metabolismo', 'Fotossíntese',
            'Respiração Celular', 'Fermentação', 'Bioma', 'Cerrado', 'Amazônia'
        ]
    },
    'matematica': {
        'algebra': [
            'Equações', 'Equações do 1º Grau', 'Equações do 2º Grau',
            'Sistemas Lineares', 'Inequações', 'Funções', 'Função Afim',
            'Função Quadrática', 'Função Exponencial', 'Função Logarítmica',
            'Função Trigonométrica', 'Progressão Aritmética', 'Progressão Geométrica',
            'Matrizes', 'Determinantes', 'Logaritmos', 'Potenciação',
            'Radiciação', 'Expressões Algébricas', 'Fatoração',
            'Polinômios', 'Raízes', 'Produtos Notáveis', 'MMC', 'MDC',
            'Proporcionalidade', 'Regra de Três', 'Porcentagem',
            'Juros Simples', 'Juros Compostos', 'Anuidades'
        ],
        'geometria': [
            'Geometria Plana', 'Geometria Espacial', 'Trigonometria',
            'Ângulos', 'Triângulos', 'Quadriláteros', 'Polígonos',
            'Círculo', 'Circunferência', 'Área', 'Perímetro', 'Volume',
            'Área de Superfície', 'Pitágoras', 'Semelhança de Triângulos',
            'Congruência de Triângulos', 'Transformações Geométricas',
            'Translação', 'Rotação', 'Reflexão', 'Dilatação',
            'Coordenadas Cartesianas', 'Vetores', 'Geometria Analítica',
            'Reta', 'Plano', 'Espaço', 'Mediatriz', 'Bissetriz',
            'Altura', 'Bissetriz', 'Centroide', 'Incentro', 'Circuncentro'
        ],
        'estatistica': [
            'Estatística', 'Tabelas', 'Gráficos', 'Medidas de Tendência Central',
            'Média', 'Mediana', 'Moda', 'Medidas de Dispersão',
            'Desvio Padrão', 'Variância', 'Amplitude', 'Quartis',
            'Percentis', 'Box Plot', 'Histograma', 'Polígono de Frequência',
            'Gráfico de Barras', 'Gráfico de Pizza', 'Gráfico de Linha',
            'Amostragem', 'Censo', 'Pesquisa', 'Interpretação de Dados',
            'Análise Estatística', 'Experimento',
            'Espaço Amostral', 'Evento', 'Área sob a Curva'
        ],
        'probabilidade': [
            'Probabilidade', 'Probabilidade Clássica', 'Probabilidade Frequencista',
            'Espaço Amostral', 'Evento', 'Evento Certeza', 'Evento Impossível',
            'Evento Independente', 'Evento Excludente', 'Probabilidade Condicional',
            'Teorema de Bayes', 'Distribuição Binomial', 'Distribuição Normal',
            'Permutação', 'Arranjo', 'Combinação', 'Princípio Fundamental',
            'Regra do Produto', 'Regra da Soma', 'Árvore de Decisão',
            'Tabela de Frequência', 'Experimento Aleatório', 'Sorteio',
            'Loteria', 'Jogo de Dados', 'Baralho', 'Moeda'
        ]
    }
}


def get_correct_hierarchy():
    """Get the correct hierarchy for validation."""
    return ENEM_HIERARCHY


if __name__ == "__main__":
    # Print hierarchy
    for area, disciplinas in ENEM_HIERARCHY.items():
        print(f"\n{area.upper()}:")
        for disc, subtopicos in disciplinas.items():
            print(f"  {disc}: {len(subtopicos)} subtopicos")
