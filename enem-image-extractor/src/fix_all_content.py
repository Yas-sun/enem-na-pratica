"""
Fix ALL metadata using ONLY content analysis (keywords + context).
Ignores question number completely for area/discipline/subtopic.
"""

import json
import re
from pathlib import Path


# ============================================================
# DISCIPLINE DETECTION BY CONTENT
# ============================================================

DISCIPLINE_KEYWORDS = {
    # NATUREZA
    'fisica': [
        ('força', 2), ('newton', 5), ('aceleração', 3), ('velocidade', 2),
        ('energia', 2), ('trabalho', 1), ('potência', 2), ('joule', 5),
        ('temperatura', 2), ('calor', 3), ('calorimetria', 10),
        ('equilíbrio térmico', 10), ('garrafa térmica', 15),
        ('água fria', 8), ('água quente', 8), ('misturadas', 3),
        ('circuito', 3), ('resistência', 2), ('corrente', 2), ('tensão', 2),
        ('campo elétrico', 5), ('campo magnético', 5), ('eletromagnetismo', 8),
        ('luz', 2), ('reflexão', 2), ('refração', 2), ('espelho', 3), ('lente', 3),
        ('onda', 2), ('frequência', 2), ('amplitude', 2),
        ('pressão', 2), ('fluido', 3), ('líquido', 2), ('densidade', 2),
        ('gravidade', 3), ('gravitacional', 5), ('queda livre', 5),
        ('cinemática', 8), ('dinâmica', 5), ('estática', 5),
        ('entropia', 8), ('termodinâmica', 8), ('máquina térmica', 10),
        ('lei de ohm', 10), ('arquimedes', 10), ('empuxo', 8),
        ('referencial', 3), ('deslocamento', 2), ('trajetória', 2),
        ('m/s', 5), ('m/s²', 8), ('newton', 5),
        ('watt', 5), ('joule', 5), ('volt', 5), ('ampere', 5),
        ('ohm', 5), ('pascal', 5), ('hertz', 5),
        ('movimento', 1), ('repouso', 2), ('oscilação', 5),
        ('ressonância', 8), ('interferência', 5), ('difração', 5),
        ('polarização', 5), ('espectro', 3),
        ('partícula', 2), ('fóton', 5), ('elétron', 3), ('próton', 3), ('nêutron', 3),
        ('núcleo', 2), ('radioatividade', 8), ('meia-vida', 8),
        ('fissão', 5), ('fusão', 5), ('reator', 3),
        ('semicondutor', 5), ('diodo', 5), ('transistor', 5),
        ('relatividade', 8), ('espaço-tempo', 8),
        ('quântica', 8), ('incerteza', 5), ('dualidade', 5),
        ('propagação', 3), ('meio elástico', 8), ('movimento ondulatório', 10),
        ('velocidade de propagação', 10), ('distância percorrida', 5),
        ('grandeza escalar', 8), ('grandeza vetorial', 8),
        ('sentido', 2), ('magnitude', 3), ('módulo', 3),
        ('referencial inercial', 10), ('referencial não inercial', 10),
        ('lei de newton', 10), ('princípio da inércia', 10),
        ('ação e reação', 10), ('terceira lei', 8),
        ('segunda lei', 8), ('primeira lei', 5),
        ('energia cinética', 10), ('energia potencial', 10),
        ('energia mecânica', 10), ('trabalho de uma força', 10),
        ('potência mecânica', 10), ('watts', 5),
        ('calor sensível', 10), ('calor latente', 10),
        ('capacidade térmica', 10), ('calorimetria', 10),
        ('primeira lei da termodinâmica', 10),
        ('processo isotérmico', 10), ('processo adiabático', 10),
        ('processo isobárico', 10), ('processo isocórico', 10),
        ('carga elétrica', 10), ('lei de coulomb', 10),
        ('campo eletrostático', 10), ('potencial elétrico', 10),
        ('capacitância', 10), ('corrente elétrica', 10),
        ('lei de ohm', 10), ('resistores em série', 10),
        ('resistores em paralelo', 10), ('potência elétrica', 10),
        ('força magnetizante', 10), ('indutância', 10),
        ('transformador', 8), ('gerador', 5),
        (' lei dos senos', 10), (' lei dos cossenos', 10),
        ('princípio de superposição', 10),
        ('ecolho', 5), ('sonar', 5), ('ultrassom', 5),
        ('radiação', 3), ('absorção', 2), ('emissão', 3),
        ('corpo negro', 8), ('lei de stefan-boltzmann', 10),
        ('lei de planck', 10), ('efeito fotoelétrico', 10),
        ('efeito doppler', 10),
    ],
    'quimica': [
        ('átomo', 3), ('molécula', 3), ('elemento', 2), ('liga metálica', 5),
        ('tabela periódica', 8), ('ligação iônica', 8), ('ligação covalente', 8),
        ('reação química', 5), ('combinação', 2), ('decomposição', 2), ('dupla troca', 8),
        ('solução', 3), ('solute', 5), ('solvente', 5), ('concentração', 3),
        ('ácido', 3), ('base', 2), ('ph', 5), ('neutralização', 8),
        ('eletrólise', 8), ('pilha', 5), ('bateria', 3), ('eletrodo', 5),
        ('estequiometria', 10), ('mol', 5), ('massa molar', 8),
        ('orgânico', 3), ('carbono', 2), ('hidrocarboneto', 5),
        ('polímero', 5), ('plástico', 3), ('biodiesel', 5),
        ('combustível', 2), ('etanol', 3), ('gasolina', 3),
        ('proteína', 3), ('carboidrato', 3), ('lipídio', 3), ('vitamina', 3),
        ('fermentação', 3), ('destilação', 5), ('cristalização', 5),
        ('diluição', 5), ('titulação', 8),
        ('molaridade', 8), ('molalidade', 8), ('normalidade', 8),
        ('redox', 8), ('oxidação', 5), ('redução', 5),
        ('corrosão', 5), ('galvanização', 8),
        (' compound', 3), ('compound', 3), ('mixture', 3),
        ('solution', 3), ('solute', 3), ('solvent', 3),
        ('acid', 3), ('base', 2), ('salt', 3),
        ('reaction', 3), ('product', 2), ('reactant', 3),
        ('periodic table', 8), ('chemical bond', 8),
        ('covalent bond', 8), ('ionic bond', 8),
        ('oxidation', 5), ('reduction', 5), ('redox', 8),
        ('electrolysis', 8), ('electrode', 5),
        ('organic chemistry', 10), ('hydrocarbon', 8),
        ('polymer', 5), ('monomer', 5),
        ('functional group', 8), ('alkane', 5), ('alkene', 5), ('alkyne', 5),
        ('alcohol', 3), ('aldehyde', 5), ('ketone', 5), ('carboxylic acid', 8),
        ('ester', 5), ('amine', 5), ('amide', 5),
    ],
    'biologia': [
        ('célula', 3), ('membrana', 2), ('organela', 5), ('citoplasma', 5),
        ('dna', 5), ('rna', 5), ('gene', 3), ('cromossomo', 5), ('hereditariedade', 5),
        ('mitose', 8), ('meiose', 8), ('divisão celular', 8),
        ('ecologia', 5), ('ecossistema', 5), ('cadeia alimentar', 8), ('biodiversidade', 5),
        ('evolução', 3), ('seleção natural', 8), ('adaptação', 3), ('darwin', 5),
        ('fotossíntese', 8), ('respiração celular', 8), ('fermentação', 3),
        ('sistema digestório', 5), ('sistema respiratório', 5), ('sistema circulatório', 5),
        ('sistema nervoso', 5), ('sistema endócrino', 5), ('sistema imunológico', 5),
        ('bactéria', 3), ('vírus', 3), ('fungo', 3), ('protista', 3),
        ('planta', 2), ('animal', 2), ('vertebrado', 3), ('invertebrado', 3),
        ('bioma', 5), ('cerrado', 3), ('amazônia', 3), ('mata atlântica', 3),
        ('desmatamento', 3), ('conservação', 2), ('extinção', 3),
        ('transgênico', 5), ('clonagem', 5), ('engenharia genética', 8),
        ('proteína', 3), ('enzima', 5), ('metabolismo', 5),
        ('digestão', 3), ('absorção', 2), ('excreção', 3),
        ('fotossintese', 8), ('quimiossíntese', 8),
        ('predador', 3), ('presa', 2), ('parasita', 3), ('simbiose', 5),
        ('mutualismo', 5), ('comensalismo', 5), ('competição', 2),
        ('população', 2), ('comunidade', 2), ('biótopo', 5), ('biocenose', 5),
        ('fator ecológico', 8), ('fator limitante', 8),
        ('sucessão ecológica', 8), ('pirâmide ecológica', 8),
        ('teia alimentar', 8), ('fluxo de energia', 8),
        ('ciclo do carbono', 8), ('ciclo da água', 8), ('ciclo do nitrogênio', 8),
        ('fixação de nitrogênio', 10), ('bactéria nitrogenada', 10),
        ('alelo', 5), ('genótipo', 5), ('fenótipo', 5),
        ('dominante', 3), ('recessivo', 3), ('heterozigoto', 5), ('homozigoto', 5),
        ('cruzamento', 3), ('herança', 3), ('alelos', 5),
        ('diabetes', 3), ('hipertensão', 3), ('câncer', 3), ('aids', 3),
        ('antibiótico', 3), ('vacina', 3), ('imunidade', 3),
        ('hemograma', 5), ('hemácias', 5), ('leucócitos', 5), ('plaquetas', 5),
        ('hemoglobina', 5), ('anticorpo', 5), ('antígeno', 5),
        ('cell', 3), ('membrane', 3), ('organelle', 5), ('cytoplasm', 5),
        ('dna', 5), ('rna', 5), ('gene', 3), ('chromosome', 5),
        ('mitosis', 8), ('meiosis', 8), ('cell division', 8),
        ('ecology', 5), ('ecosystem', 5), ('food chain', 8), ('biodiversity', 5),
        ('evolution', 3), ('natural selection', 8), ('adaptation', 3), ('darwin', 5),
        ('photosynthesis', 8), ('cellular respiration', 8),
        ('digestive system', 5), ('respiratory system', 5), ('circulatory system', 5),
        ('nervous system', 5), ('endocrine system', 5), ('immune system', 5),
        ('bacteria', 3), ('virus', 3), ('fungus', 3),
        ('plant', 2), ('animal', 2), ('vertebrate', 3), ('invertebrate', 3),
    ],
    
    # HUMANAS
    'historia': [
        ('guerra', 2), ('revolução', 2), ('império', 2), ('colônia', 2), ('república', 2),
        ('independência', 2), ('ditadura', 2), ('golpe', 2), ('eleições', 2),
        ('escravidão', 3), ('escravo', 3), ('abolicionismo', 5),
        ('dom pedro', 5), ('getúlio', 5), ('vargas', 3),
        ('primeira guerra', 8), ('segunda guerra', 8), ('guerra fria', 8),
        ('nazismo', 5), ('fascismo', 5), ('comunismo', 3), ('liberalismo', 3),
        ('medieval', 5), ('renascimento', 5), ('descobrimentos', 5),
        ('iluminismo', 5), ('absolutismo', 5), ('feudalismo', 5),
        ('estado nacional', 5), ('soberania', 3), ('nação', 2),
        ('século xvi', 5), ('século xvii', 5), ('século xviii', 5), ('século xix', 5),
        ('século xx', 3), ('século xxi', 3),
        ('ditadura militar', 8), ('regime militar', 8), ('ai-5', 10),
        ('redemocratização', 5), ('constituição', 3),
        ('trabalho escravo', 8), ('fazenda', 2), ('fazendeiro', 3),
        ('bloqueio', 2), ('fiscalização', 2), ('organizações não governamentais', 5),
        ('conflito', 2), ('batalha', 3), ('tratado', 3), ('aliança', 2),
        ('imperialismo', 5), ('colonialismo', 5), ('descolonização', 5),
        ('guerra civil', 5), ('revolta', 3), ('insurreição', 5),
        ('monarquia', 3), ('democracia', 2),
        ('mercantilismo', 5), ('capitalismo', 3),
        ('igreja', 2), ('católica', 2), ('protestante', 3), ('reforma protestante', 8),
        ('contrarreforma', 8), ('inquisição', 5),
        ('expansão marítima', 8), ('navegação', 3),
        ('capitanias hereditárias', 8), ('administração colonial', 8),
        ('sociedade colonial', 5),
        ('mineração', 2), ('ouro', 1), ('diamante', 2),
        ('escravatura', 5), ('tráfico de escravos', 8),
        ('inconfidência', 8), ('conjuração', 5), ('inconfidentes', 8),
        ('tiradentes', 8), ('marquês de pombal', 8),
        ('revolução francesa', 10), ('bastilha', 8), ('declaração dos direitos', 8),
        ('liberdade', 2), ('igualdade', 2), ('fraternidade', 5),
        ('napoleão', 5), ('império francês', 5),
        ('revolução industrial', 10), ('mecanização', 5), ('fábrica', 3),
        ('proletariado', 5), ('burguesia', 3),
        ('abolição', 5), ('lei áurea', 8), ('princesa Isabel', 8),
        ('república velha', 8), ('café com leite', 8), ('coronelismo', 8),
        ('política dos governadores', 10), ('estado novo', 8), ('getúlio vargas', 8),
        ('justiça do trabalho', 8), ('consolidação das leis', 8), ('clt', 8),
        ('primeira república', 8),
        ('1930', 3), ('1937', 3), ('1945', 3), ('1964', 3), ('1985', 3),
        ('1822', 3), ('1889', 3), ('1888', 3), ('1500', 3),
        ('pedro i', 5), ('pedro ii', 5), ('deodoro', 5), ('floriano', 5),
        ('conflitos', 2), ('violência', 1), ('período', 1),
        ('histórico', 2), ('século', 2), ('ano', 1),
        ('brasil', 1), ('europa', 2), ('américa', 2), ('áfrica', 2),
        (' guerra ', 2), (' revolução ', 2), (' império ', 2),
        (' colônia ', 2), (' república ', 2), (' ditadura ', 2),
    ],
    'geografia': [
        ('região', 2), ('nordeste', 3), ('sudeste', 3), ('centro-oeste', 3), ('norte', 2),
        ('clima', 3), ('chuva', 3), ('seca', 2), ('inundaç', 2),
        ('relevo', 3), ('montanha', 2), ('planície', 3), ('planalto', 3),
        ('vegetação', 3), ('floresta', 2), ('cerrado', 3), ('caatinga', 3), ('mata atlântica', 3),
        ('população', 2), ('migração', 3), ('imigração', 3), ('urbanização', 2),
        ('globalização', 3), ('bloco econômico', 5), ('mercosul', 5),
        ('meio ambiente', 3), ('desmatamento', 3), ('poluição', 2),
        ('reforma agrária', 5), ('latifúndio', 5), ('minifúndio', 5),
        ('energia', 1), ('petróleo', 3), ('biocombustível', 5),
        ('transporte', 2), ('ferrovia', 3), ('porto', 2), ('aeroporto', 2),
        ('mapa', 2), ('escala', 2), ('cartografia', 5), ('coordenadas', 3),
        ('fuso horário', 8), ('meridiano', 5), ('paralelo', 3),
        ('placa tectônica', 8), ('terremoto', 5), ('vulcão', 5),
        ('questão agrária', 8), ('questão ambiental', 8),
        ('amazônia', 3), ('semiárido', 5), ('litoral', 3), ('interior', 2),
        ('fronteira', 3), ('divisa', 2), ('limite', 2),
        ('bacia hidrográfica', 8), ('rio', 1), ('lago', 1), ('oceano', 2),
        ('mar', 1), ('golfo', 2), ('baía', 2),
        ('ilha', 2), ('península', 3), ('continente', 2),
        ('hemisfério', 3), ('trópico', 3), ('câncer', 2), ('capricórnio', 3),
        ('linha do equador', 5), ('polo', 2),
        ('zoneamento ecológico', 8), ('área de preservação', 8), ('reserva legal', 8),
        ('unidade de conservação', 8), ('parque nacional', 5),
        ('desertificação', 5), ('erosão', 3), ('degradação', 3),
        ('contaminação', 3), ('desequilíbrio', 2),
        ('agropecuária', 3), ('agricultura', 2), ('pecuária', 2),
        ('mineração', 2), ('indústria', 2), ('comércio', 2),
        ('serviços', 1), ('setor terciário', 5), ('setor secundário', 5), ('setor primário', 5),
        ('brasil', 1), ('américa', 2), ('europa', 2), ('áfrica', 2), ('ásia', 2),
        ('onu', 3), ('fmi', 3), ('banco mundial', 5), ('omc', 5),
        ('desenvolvimento sustentável', 8), ('equilíbrio ambiental', 5),
        ('sustentabilidade', 3), ('preservação', 2), ('conservação', 2),
        ('temperatura', 1), ('chuva', 2), ('seca', 2),
        ('região', 2), ('território', 3), ('espacial', 3),
    ],
    'sociologia': [
        ('sociedade', 3), ('social', 2), ('classe', 2), ('desigualdade', 3),
        ('cidadão', 3), ('cidadania', 5), ('direito', 2), ('dever', 2),
        ('cultura', 2), ('identidade', 2), ('tradição', 2),
        ('educação', 2), ('escola', 2), ('ensino', 2),
        ('trabalho', 1), ('emprego', 2), ('desemprego', 3),
        ('violência', 2), ('crime', 2), ('segurança', 2),
        ('mídia', 3), ('comunicação', 2), ('jornal', 2),
        ('movimento social', 8), ('protesto', 5), ('greve', 5),
        ('família', 2), ('religião', 2), ('gênero', 3),
        ('consumismo', 5), ('consumidor', 3),
        ('conscientização', 5), ('direitos sociais', 8), ('direitos trabalhistas', 8),
        ('ministério público', 5), ('ação judicial', 5),
        ('organização não governamental', 8), ('ong', 5),
        ('pastoral', 5), ('defesa dos direitos', 5),
        ('trabalhador', 2), ('assalariado', 3), ('exploração', 2),
        ('opressão', 3), ('marginalização', 5), ('exclusão', 3),
        ('inclusão social', 8), ('política social', 8),
        ('assistência social', 8), ('política pública', 5),
        ('participação cidadã', 8), ('democracia participativa', 8),
        ('movimento operário', 8), ('movimento estudantil', 8),
        ('movimento feminista', 8), ('movimento negro', 8),
        ('movimento ambientalista', 8), ('movimento dos sem terra', 10),
        ('mst', 8), ('mtst', 8),
        ('sociabilidade', 5), ('interação social', 8),
        ('norma social', 8), ('controle social', 8),
        ('estratificação', 5), ('mobilidade social', 8),
        ('etnia', 3), ('raça', 2), ('preconceito', 3), ('discriminação', 3),
        ('multiculturalismo', 5), ('diversidade', 2),
        ('globalização cultural', 8), ('universalização', 5),
        ('indústria cultural', 8), ('hegemonia cultural', 8),
        ('ideologia', 3), ('poder', 1), ('dominação', 2),
        ('hegemonia', 3), ('resistência', 2),
        ('qualidade de vida', 8), ('bem-estar social', 8),
        ('serviço público', 5), ('política de saúde', 5),
        ('política educacional', 5), ('política habitacional', 5),
    ],
    'filosofia': [
        ('filosofia', 5), ('filósofo', 5), ('sócrates', 8), ('platão', 8), ('aristóteles', 8),
        ('descartes', 8), ('kant', 8), ('hegel', 8), ('marx', 5), ('nietzsche', 8),
        ('existencialismo', 8), ('racionalismo', 8), ('empirismo', 8),
        ('ética', 5), ('moral', 3), ('bem', 1), ('mal', 1), ('justo', 2),
        ('política', 2), ('estado', 1), ('governo', 1), ('poder', 1),
        ('verdade', 3), ('conhecimento', 3), ('realidade', 2),
        ('liberdade', 2), ('igualdade', 2), ('justiça', 2),
        ('cogito ergo sum', 10), ('method', 3),
        ('dialética', 8), ('materialismo histórico', 10), ('alienação', 5),
        ('sociedade civil', 5), ('estado democrático', 5),
        ('contratualismo', 8), ('soberania popular', 8),
        ('direito natural', 8), ('direito positivo', 8),
        ('utilitarismo', 8), ('deontologia', 8), ('virtude', 5),
        ('estética', 5), ('beleza', 2), ('sublime', 3),
        ('epistemologia', 8), ('ciência', 2), ('método', 3),
        ('metafísica', 8), ('ontologia', 8), ('cosmologia', 5),
        ('filosofia da linguagem', 10), ('linguagem', 2), ('signo', 5),
        ('filosofia da mente', 10), ('consciência', 3), ('intencionalidade', 5),
        ('filosofia da ciência', 10), ('paradigma', 5), ('falsificação', 5),
        ('filosofia da história', 10), ('progresso', 2), ('historicidade', 5),
        ('fenomenologia', 8), ('hermenêutica', 8), ('deconstructivismo', 8),
        ('pós-modernidade', 5), ('pós-estruturalismo', 8),
        ('escolástica', 8), ('tomismo', 8), ('neoplatonismo', 8),
        ('estoicismo', 8), ('epicurismo', 8), ('cinismo', 5),
        ('iluminismo', 5), ('idealismo', 5),
        ('pragmatismo', 5), ('neopositivismo', 8),
        ('marxismo', 5), ('anarquismo', 5), ('liberalismo', 3),
        ('comunitarismo', 5), ('cosmopolitismo', 5),
        ('bioética', 8), ('eutanásia', 5), ('aborto', 3), ('pena de morte', 5),
        ('justiça social', 5), ('direitos humanos', 5),
        ('cidadania', 3), ('democracia', 2), ('soberania', 2),
    ],
    
    # LINGUAGENS
    'portugues': [
        ('verbo', 3), ('conjugação', 5), ('tempo verbal', 5),
        ('sujeito', 2), ('predicado', 3), ('objeto direto', 5), ('objeto indireto', 5),
        ('oração', 3), ('período', 2),
        ('ponto e vírgula', 5), ('vírgula', 3), ('dois pontos', 3), ('ponto final', 3),
        ('sinônimo', 5), ('antônimo', 5), ('polissemia', 8), ('hipônimo', 8),
        ('metáfora', 5), ('hipérbole', 5), ('ironia', 5), ('comparação', 3),
        ('gênero textual', 8), ('crônica', 5), ('poema', 3), ('conto', 3), ('novela', 3),
        ('romantismo', 5), ('realismo', 5), ('modernismo', 5), ('barroco', 5),
        ('regência', 8), ('concordância', 8), ('crase', 8), ('acentuação', 5),
        ('coordenação', 3), ('subordinação', 5), ('oração absoluta', 8),
        ('sujeito simples', 8), ('sujeito composto', 8), ('predicado simples', 8),
        ('voz ativa', 8), ('voz passiva', 8), ('voz reflexiva', 8),
        ('aspecto verbal', 8), ('modo indicativo', 8), ('modo subjuntivo', 8),
        ('artigo', 3), ('demonstrativo', 5), ('indefinido', 5), ('numeral', 3),
        ('adjetivo', 3), ('advérbio', 3), ('preposição', 3), ('conjunção', 3),
        ('locução adverbial', 8), ('locução prepositiva', 8),
        ('texto', 1), ('trecho', 2), ('fragmento', 2),
        ('leitura', 2), ('interpretação', 2), ('compreensão', 2),
        ('argumentação', 3), ('narrativa', 2), ('descritiva', 2),
        ('informativo', 2), ('editorial', 3), ('crítica', 2),
        ('norma culta', 8), ('gramática', 3), ('regra', 2),
        ('linguagem formal', 8), ('linguagem informal', 5),
        ('variação linguística', 8), ('gíria', 5), ('calão', 5),
        ('semântica', 8), ('sintaxe', 8), ('morfologia', 8),
        ('fonologia', 8), ('fonética', 5),
        ('discurso', 3), ('interlocutor', 5), ('propósito', 3),
        ('tom', 2), ('sarcasmo', 5), ('humor', 2),
        ('ambiguidade', 5), ('equívoco', 5),
        ('denotação', 8), ('conotação', 8),
        ('figuras de linguagem', 8), ('figuras de sentido', 8),
        ('metonímia', 5), ('sinédoque', 5), ('antítese', 5),
        ('paradoxo', 5), ('símile', 5),
        ('prosopopeia', 8), ('apóstrofe', 5), ('eufemismo', 5),
        ('catacrese', 8), ('personificação', 5),
        ('soneto', 5), ('ode', 5), ('elegia', 5), ('lira', 5), ('balada', 5),
        ('canção', 3), ('epopeia', 5), ('sátira', 5),
        ('monólogo', 5), ('diálogo', 3), ('monologo', 5),
        ('estrofe', 5), ('verso', 3), ('rima', 3), ('métrica', 5),
        ('redação', 2), ('produção textual', 8), ('redação dissertativa', 8),
        ('tese', 3), ('argumento', 2), ('contra-argumento', 5),
        ('introdução', 2), ('desenvolvimento', 2), ('conclusão', 2),
        ('repertório', 5), ('exemplo', 1),
    ],
    'ingles': [
        ('verb to be', 10), ('present simple', 8), ('past simple', 8),
        ('present continuous', 8), ('future tense', 8), ('present perfect', 8),
        ('past continuous', 8), ('adjective', 3), ('adverb', 3),
        ('pronoun', 5), ('preposition', 3),
        ('although', 5), ('because', 3), ('while', 3), ('during', 3),
        ('before', 2), ('after', 2), ('if clause', 8), ('conditional', 8),
        ('passive voice', 10), ('reported speech', 10),
        ('relative clause', 8), ('phrasal verb', 8),
        ('text', 1), ('article', 2), ('passage', 2),
        ('according to', 5), ('based on', 3),
        ('the author', 3), ('the writer', 3),
        ('main idea', 5), ('main purpose', 5),
        ('inference', 5), ('imply', 5), ('suggest', 3),
    ],
    'espanhol': [
        ('verbo ser', 10), ('verbo estar', 10), ('verbo haber', 10),
        ('pretérito', 8), ('subjuntivo', 8), ('imperativo', 8),
        ('futuro', 5), ('condicional', 5),
        ('pronombre', 5), ('artículo', 5), ('preposición', 5), ('conjunción', 5),
        ('texto', 1), ('artículo', 2), ('pasaje', 2),
        ('según', 5), ('de acuerdo con', 5),
        ('la idea principal', 8), ('el propósito', 8),
    ],
    'literatura': [
        ('personagem', 5), ('enredo', 5), ('narrador', 5), ('foco narrativo', 8),
        ('tema', 2), ('motivo', 3), ('figura linguagem', 5),
        ('romantismo', 5), ('realismo', 5), ('naturalismo', 8), ('modernismo', 5),
        ('parnasianismo', 8), ('simbolismo', 8), ('concretismo', 8),
        ('soneto', 5), ('ode', 5), ('elegia', 5), ('lira', 5), ('balada', 5),
        ('monólogo', 5), ('diálogo', 3),
        ('literário', 3), ('obra', 2), ('livro', 2), ('poesia', 3), ('prosa', 3),
        ('metáfora', 3), ('simbolismo', 3), ('alegoria', 5),
        ('arquétipo', 8), ('mito', 3), ('arquétipo literário', 10),
    ],
    'artes': [
        ('pintura', 5), ('escultura', 5), ('arte', 2), ('quadro', 3),
        ('música', 3), ('teatro', 3), ('cinema', 3), ('dança', 3), ('fotografia', 3),
        ('impressionismo', 8), ('cubismo', 8), ('surrealismo', 8), ('expressionismo', 8),
        ('grafite', 5), ('street art', 5), ('arte digital', 5),
        ('artista', 3), ('obra de arte', 5),
        ('cultura visual', 8), ('linguagem visual', 8),
        ('cor', 2), ('forma', 2), ('composição', 3), ('perspectiva', 3),
        ('simetria', 3), ('equilíbrio', 2), ('ritmo', 2),
        ('linhas', 2), ('volumes', 2), ('textura', 3),
        ('contexto histórico', 3), ('movimento artístico', 8),
        ('vanguarda', 5), ('anguarda', 5),
        ('arte contemporânea', 8), ('arte moderna', 5), ('arte barroca', 5),
        ('renascimento', 3), ('arte renascentista', 8),
    ],
    
    # MATEMÁTICA
    'algebra': [
        ('equação', 5), ('incógnita', 5), ('solução', 2), ('igualdade', 3),
        ('função', 3), ('gráfico', 2), ('domínio', 3), ('imagem', 2),
        ('porcento', 5), ('porcentagem', 5), ('desconto', 3), ('acréscimo', 3),
        ('razão', 3), ('proporção', 5), ('proporcional', 5),
        ('progressão aritmética', 10), ('razão da pa', 10),
        ('progressão geométrica', 10), ('razão da pg', 10),
        ('juros simples', 8), ('juros compostos', 8),
        ('sistema linear', 8), ('matriz', 5), ('determinante', 8),
        ('logaritmo', 8), ('potenciação', 5), ('radiciação', 5),
        ('expressão algébrica', 8), ('monômio', 8), ('polinômio', 8),
        ('coeficiente', 5), ('grau', 3),
        ('MMC', 5), ('MDC', 5), ('fatoração', 8),
        ('produtos notáveis', 10), ('quadrado perfeito', 8),
        ('proporcionalidade direta', 10), ('proporcionalidade inversa', 10),
        ('regra de três simples', 10), ('regra de três composta', 10),
        ('grandezas proporcionais', 10),
    ],
    'geometria': [
        ('triângulo', 3), ('quadrilátero', 3), ('círculo', 3), ('circunferência', 3),
        ('área', 2), ('perímetro', 3), ('volume', 2),
        ('pitágoras', 8), ('hipotenusa', 8), ('cateto', 5),
        ('seno', 5), ('cosseno', 5), ('tangente', 5), ('ângulo', 3),
        ('semelhança', 5), ('congruência', 5),
        ('plano cartesiano', 8), ('coordenada', 5),
        ('polígono', 5), ('poliedro', 5), ('cubo', 3), ('esfera', 3), ('cilindro', 3),
        ('pirâmide', 3), ('cone', 3), ('paralelepípedo', 5),
        ('diagonal', 3), ('lado', 2), ('vértice', 3),
        ('teorema', 8), ('propriedade', 3),
        ('trapézio', 5), ('losango', 5), ('retângulo', 3), ('quadrado', 2),
        ('paralelogramo', 5),
        ('mediana', 5), ('bissetriz', 5), ('altura', 3), ('base', 2),
        ('baricentro', 8), ('incentro', 8), ('circuncentro', 8), ('ortocentro', 8),
        ('circunscrita', 8), ('inscrita', 8),
        ('lei dos cossenos', 10), ('lei dos senos', 10),
        ('razão trigonométrica', 10), ('arco seno', 8), ('arco cosseno', 8),
        ('arco tangente', 8),
        ('transformação geométrica', 10), ('translação', 8), ('rotação', 5),
        ('reflexão', 3), ('dilatação', 5),
    ],
    'estatistica': [
        ('média', 5), ('mediana', 5), ('moda', 5),
        ('gráfico', 3), ('tabela', 2), ('histograma', 8),
        ('desvio padrão', 10), ('variância', 8), ('amplitude', 5),
        ('pesquisa', 2), ('amostra', 5), ('censo', 5),
        ('estatística', 5), ('dados', 2), ('informação', 2),
        ('frequência', 3), ('absoluta', 2), ('relativa', 2),
        ('percentual', 3), ('proporção', 2),
        ('amplitude total', 8), ('amplitude interquartil', 10),
        ('medidas de tendência central', 10), ('medidas de dispersão', 10),
        ('Box Plot', 10), ('diagrama', 5),
        ('interpretar', 2), ('analisar', 2),
        ('tabela de dados', 8), ('gráfico de barras', 8),
        ('gráfico de pizza', 8), ('gráfico de linhas', 8),
        ('gráfico de colunas', 8), ('gráfico de setores', 8),
    ],
    'probabilidade': [
        ('probabilidade', 8), ('chance', 5), ('evento', 3), ('sorteio', 5),
        ('espaço amostral', 10), ('resultado possível', 8),
        ('evento certo', 10), ('evento impossível', 10),
        ('dependente', 5), ('independente', 5),
        ('permutação', 8), ('arranjo', 8), ('combinação', 8),
        ('árvore de decisão', 10), ('tabela de frequência', 8),
        ('experimento aleatório', 10), ('experiência', 3),
        ('ocorrência', 3), ('possibilidade', 3),
        ('um décimo', 5), ('um terço', 3), ('metade', 3),
        ('dois terços', 3), ('um quarto', 3),
        ('número de casos favoráveis', 10),
        ('número de casos possíveis', 10),
        ('casos favoráveis', 10), ('casos possíveis', 10),
        ('moeda', 3), ('dado', 2), ('baralho', 3),
        ('loteria', 5), ('mega-sena', 5), ('quina', 3),
    ],
}

# Discipline to area mapping
DISC_TO_AREA = {
    'fisica': 'natureza', 'quimica': 'natureza', 'biologia': 'natureza',
    'historia': 'humanas', 'geografia': 'humanas', 'sociologia': 'humanas', 'filosofia': 'humanas',
    'portugues': 'linguagens', 'ingles': 'linguagens', 'espanhol': 'linguagens',
    'literatura': 'linguagens', 'artes': 'linguagens',
    'algebra': 'matematica', 'geometria': 'matematica',
    'estatistica': 'matematica', 'probabilidade': 'matematica',
}


def detect_discipline(texto):
    """Detect discipline based on question text content using weighted scoring."""
    if not texto:
        return None, 0
    
    texto_lower = texto.lower()
    
    scores = {}
    for disc, signals in DISCIPLINE_KEYWORDS.items():
        score = 0
        for keyword, weight in signals:
            if keyword.lower() in texto_lower:
                score += weight
        scores[disc] = score
    
    if not scores:
        return None, 0
    
    best = max(scores, key=scores.get)
    if scores[best] >= 5:
        return best, scores[best]
    
    return None, 0


# ============================================================
# SUBTOPIC DETECTION
# ============================================================

SUBTOPIC_KEYWORDS = {
    'historia': {
        'Brasil Colônia': [('colônia', 3), ('colonial', 3), ('capitanias', 5), ('portugueses', 2), ('brasil colonial', 5)],
        'Brasil Império': [('império', 3), ('dom pedro', 5), ('independência', 3), ('imperial', 3), ('brasil império', 5)],
        'República Velha': [('república', 2), ('oligárquica', 5), ('café com leite', 8), ('república velha', 8)],
        'Era Vargas': [('vargas', 3), ('estado novo', 5), ('getúlio', 5), ('era vargas', 8)],
        'Regime Militar': [('militar', 3), ('ditadura', 3), ('golpe', 3), ('ai-5', 8), ('regime militar', 8)],
        'Guerras Mundiais': [('primeira guerra', 8), ('segunda guerra', 8), ('guerra mundial', 8), ('1914', 5), ('1939', 5)],
        'Guerra Fria': [('guerra fria', 10), ('urss', 5), ('bloco soviético', 8), ('bloco ocidental', 8)],
        'Pré-História': [('pré-história', 8), ('neolítico', 8), ('paleolítico', 8)],
        'Civilizações Antigas': [('egito', 5), ('mesopotâmia', 8), ('roma', 3), ('grécia', 3)],
        'Idade Média': [('medieval', 8), ('feudalismo', 8), ('feudal', 5)],
        'Revolução Francesa': [('revolução francesa', 10), ('liberdade igualdade fraternidade', 10)],
        'Revolução Industrial': [('revolução industrial', 10), ('mecanização', 8)],
        'Direitos Humanos': [('direitos humanos', 10), ('direito', 2), ('liberdade', 2)],
        'Abolicionismo': [('escravo', 3), ('escravidão', 5), ('abolicionismo', 8), ('trabalho escravo', 8), ('fazenda', 2)],
        'Redemocratização': [('democracia', 3), ('eleições', 3), ('plebiscito', 5), ('constituição', 3)],
        'Formação do Estado Nacional': [('estado nacional', 8), ('nação', 3), ('soberania', 5)],
        'Descolonização': [('descolonização', 10), ('independência', 3), ('colônia', 2)],
        'Idade Moderna': [('moderna', 3), ('renascimento', 5), ('descobrimentos', 5)],
        'Idade Contemporânea': [('contemporânea', 5), ('globalização', 3), ('mundialização', 5), ('século xx', 5), ('século xix', 5)],
    },
    'geografia': {
        'Geografia do Brasil': [('brasil', 2), ('região', 2), ('nordeste', 3), ('sudeste', 3), ('norte', 2), ('centro-oeste', 3)],
        'Geografia Mundial': [('mundo', 2), ('europa', 3), ('américa', 3), ('áfrica', 3), ('ásia', 3)],
        'Cartografia': [('mapa', 3), ('cartografia', 8), ('escala', 3), ('projeção', 5), ('coordenada', 5)],
        'Climatologia': [('clima', 5), ('temperatura', 3), ('chuva', 5), ('seca', 3)],
        'Urbanização': [('urbanização', 8), ('cidade', 3), ('migração', 3), ('metrópole', 5)],
        'Meio Ambiente': [('meio ambiente', 8), ('desmatamento', 5), ('poluição', 3), ('sustentável', 5)],
        'Demografia': [('população', 5), ('natalidade', 8), ('mortalidade', 8), ('crescimento', 3)],
        'Globalização': [('globalização', 8), ('mundialização', 8), ('internacional', 3)],
        'Questão Agrária': [('agrária', 8), ('reforma agrária', 10), ('latifúndio', 8)],
        'Migração': [('migração', 8), ('migrante', 8), ('imigração', 8), ('emigração', 8)],
    },
    'sociologia': {
        'Sociologia Geral': [('sociedade', 5), ('social', 2), ('classe', 2), ('estrutura', 2)],
        'Cidadania': [('cidadão', 5), ('cidadania', 8), ('direito', 2), ('dever', 2), ('conscientização', 5)],
        'Cultura': [('cultura', 5), ('tradição', 3), ('costume', 3), ('identidade cultural', 8)],
        'Estratificação Social': [('estratificação', 8), ('desigualdade', 5), ('renda', 3)],
        'Trabalho': [('trabalho', 2), ('emprego', 3), ('desemprego', 5), ('assalariado', 5), ('trabalhador', 3)],
        'Educação': [('educação', 5), ('escola', 3), ('ensino', 3), ('aprendizagem', 5)],
        'Violência': [('violência', 5), ('crime', 3), ('segurança', 3), ('punição', 3)],
        'Mídia': [('mídia', 8), ('comunicação', 3), ('jornal', 3), ('televisão', 3)],
        'Movimentos Sociais': [('movimento', 3), ('protesto', 5), ('luta', 3), ('greve', 5)],
        'Classe Social': [('classe', 3), ('burguesia', 5), ('proletariado', 5), ('elite', 3)],
    },
    'filosofia': {
        'Filosofia Antiga': [('sócrates', 10), ('platão', 10), ('aristóteles', 10)],
        'Filosofia Moderna': [('descartes', 10), ('kant', 10), ('hegel', 10)],
        'Ética': [('ética', 8), ('moral', 5), ('bem', 2), ('mal', 2), ('justo', 3)],
        'Política': [('política', 5), ('estado', 2), ('governo', 2), ('poder', 2)],
        'Epistemologia': [('conhecimento', 5), ('verdade', 5), ('ciência', 3)],
        'Existencialismo': [('existencialismo', 10), ('existência', 5), ('angústia', 5)],
    },
    'fisica': {
        'Mecânica': [('força', 5), ('newton', 8), ('lei', 2), ('massa', 3), ('aceleração', 5)],
        'Cinemática': [('cinemática', 10), ('deslocamento', 5), ('trajetória', 5), ('velocidade', 3)],
        'Dinâmica': [('dinâmica', 8), ('newton', 5), ('lei', 2), ('força', 3)],
        'Termodinâmica': [('temperatura', 5), ('calor', 5), ('energia', 3), ('entropia', 8), ('garrafa', 5), ('água', 2), ('equilíbrio térmico', 10), ('calorimetria', 10)],
        'Eletromagnetismo': [('elétric', 5), ('magnét', 5), ('carga', 3), ('campo', 2), ('circuito', 5), ('corrente', 3), ('tensão', 3)],
        'Óptica': [('óptica', 8), ('luz', 5), ('reflexão', 3), ('refração', 3), ('espelho', 5), ('lente', 5)],
        'Hidrostática': [('pressão', 3), ('fluido', 5), ('líquido', 3), ('volume', 2), ('densidade', 3), ('arquimedes', 10), ('empuxo', 8)],
        'Gravitação': [('gravidade', 5), ('gravitacional', 8), ('queda livre', 10)],
        'Ondas': [('onda', 5), ('frequência', 3), ('amplitude', 3), ('sonora', 5)],
        'Trabalho e Energia': [('trabalho', 2), ('energia', 3), ('potência', 5), ('joule', 8)],
    },
    'quimica': {
        'Química Geral': [('átomo', 5), ('molécula', 5), ('elemento', 3), ('liga', 3), ('tabela periódica', 8)],
        'Reações Químicas': [('reação', 5), ('química', 2), ('combinação', 3), ('decomposição', 3)],
        'Soluções': [('solução', 5), ('solute', 8), ('solvente', 8), ('concentração', 5)],
        'Química Orgânica': [('orgânico', 5), ('carbono', 3), ('hidrocarboneto', 8)],
        'Eletroquímica': [('eletrólise', 10), ('pilha', 8), ('bateria', 5), ('eletrodo', 8)],
        'Acidoses e Bases': [('ácido', 5), ('base', 3), ('ph', 8), ('neutralização', 10)],
        'Estequiometria': [('estequiometria', 10), ('mol', 8), ('massa molar', 10)],
    },
    'biologia': {
        'Citologia': [('célula', 5), ('membrana', 3), ('organela', 8), ('citoplasma', 8)],
        'Genética': [('gene', 5), ('dna', 8), ('hereditariedade', 8), ('cromossomo', 8)],
        'Ecologia': [('ecologia', 8), ('ecossistema', 8), ('biodiversidade', 8), ('cadeia alimentar', 10)],
        'Evolução': [('evolução', 5), ('seleção natural', 10), ('adaptação', 5)],
        'Fisiologia': [('fisiologia', 8), ('sistema', 3), ('órgão', 3), ('função', 2)],
        'Biologia Celular': [('celular', 5), ('célula', 3), ('divisão', 3), ('mitose', 8), ('meiose', 8)],
        'Microbiologia': [('bactéria', 5), ('vírus', 5), ('microorganismo', 8)],
        'Botânica': [('planta', 5), ('fotossíntese', 8), ('flor', 3), ('folha', 3)],
        'Zoologia': [('animal', 5), ('vertebrado', 8), ('invertebrado', 8)],
    },
    'algebra': {
        'Equações': [('equação', 8), ('incógnita', 8), ('solução', 3), ('igualdade', 5)],
        'Funções': [('função', 8), ('gráfico', 3), ('domínio', 5), ('imagem', 3)],
        'Porcentagem': [('porcento', 8), ('porcentagem', 8), ('80%', 5), ('20%', 5)],
        'Proporcionalidade': [('proporcional', 8), ('razão', 3), ('razão entre', 5)],
        'Regra de Três': [('regra de três', 10), ('proporcional', 5)],
        'Progressão Aritmética': [('pa', 5), ('progressão aritmética', 10), ('razão', 3)],
        'Progressão Geométrica': [('pg', 5), ('progressão geométrica', 10)],
    },
    'geometria': {
        'Geometria Plana': [('triângulo', 5), ('quadrilátero', 5), ('círculo', 5), ('área', 3), ('perímetro', 5)],
        'Geometria Espacial': [('volume', 5), ('sólido', 5), ('cubo', 3), ('esfera', 3), ('cilindro', 5)],
        'Trigonometria': [('seno', 8), ('cosseno', 8), ('tangente', 8), ('ângulo', 5)],
        'Ângulos': [('ângulo', 5), ('graus', 3), ('radiano', 8)],
        'Pitágoras': [('pitágoras', 10), ('hipotenusa', 10), ('cateto', 8)],
        'Semelhança de Triângulos': [('semelhança', 8), ('semelhante', 5), ('proporção', 3)],
    },
    'estatistica': {
        'Estatística': [('estatística', 8), ('média', 5), ('mediana', 5), ('moda', 5), ('desvio', 5)],
        'Gráficos': [('gráfico', 5), ('tabela', 3), ('barras', 5), ('pizza', 5), ('histograma', 8)],
        'Medidas de Tendência Central': [('média', 5), ('mediana', 5), ('moda', 5)],
        'Amostragem': [('amostra', 8), ('amostragem', 10), ('pesquisa', 3)],
        'Interpretação de Dados': [('dados', 3), ('tabela', 2), ('gráfico', 2), ('número', 2)],
    },
    'probabilidade': {
        'Probabilidade': [('probabilidade', 10), ('chance', 8), ('evento', 5), ('sorteio', 8), ('possibilidade', 5)],
        'Espaço Amostral': [('espaço amostral', 10), ('resultado', 3), ('possível', 3)],
        'Evento': [('evento', 5), ('acontecimento', 5), ('ocorrência', 5)],
        'Permutação': [('permutação', 10), ('arranjo', 10), ('combinação', 10), ('ordem', 3)],
    },
    'portugues': {
        'Interpretação de Texto': [('texto', 3), ('interpretação', 5), ('leitura', 3), ('compreensão', 3)],
        'Vozes Verbais': [('verbo', 5), ('verbal', 5), ('conjugação', 8), ('tempo verbal', 8)],
        'Morfologia': [('prefixo', 8), ('sufixo', 8), ('radical', 8), ('morfologia', 10)],
        'Sintaxe': [('sintaxe', 8), ('sujeito', 5), ('predicado', 5), ('objeto', 3)],
        'Semântica': [('sinônimo', 8), ('antônimo', 8), ('polissemia', 10), ('significado', 3)],
        'Pontuação': [('vírgula', 8), ('ponto', 3), ('ponto e vírgula', 8)],
        'Coesão': [('coesão', 8), ('conjunção', 5), ('articulador', 8)],
        'Gêneros Textuais': [('gênero', 5), ('crônica', 8), ('poema', 5), ('notícia', 5), ('editorial', 8)],
        'Figuras de Linguagem': [('metáfora', 8), ('comparação', 5), ('hipérbole', 8), ('ironia', 5)],
        'Movimentos Literários': [('romantismo', 8), ('realismo', 8), ('modernismo', 8)],
        'Norma Culta': [('norma culta', 10), ('gramática', 5), ('regra', 3)],
    },
    'ingles': {
        'Vocabulário Inglês': [('word', 5), ('vocabulary', 8), ('meaning', 5)],
        'Gramática Inglesa': [('verb', 5), ('tense', 8), ('adjective', 5)],
        'Texto Informativo': [('text', 3), ('article', 5), ('passage', 5)],
    },
    'espanhol': {
        'Vocabulário Espanhol': [('palabra', 5), ('vocabulario', 8), ('significado', 5)],
        'Gramática Espanhola': [('verbo', 5), ('tiempo', 5), ('adjetivo', 5)],
    },
    'literatura': {
        'Movimentos Literários': [('romantismo', 8), ('realismo', 8), ('modernismo', 8), ('barroco', 8)],
        'Análise Literária': [('personagem', 8), ('enredo', 8), ('narrador', 8), ('tema', 3)],
        'Figuras de Linguagem': [('metáfora', 8), ('comparação', 5), ('hipérbole', 8)],
    },
    'artes': {
        'Artes Visuais': [('pintura', 8), ('escultura', 8), ('arte', 3), ('quadro', 5)],
        'Música': [('música', 8), ('melodia', 8), ('ritmo', 5), ('canção', 5)],
        'Teatro': [('teatro', 8), ('peça', 5), ('ator', 3), ('cena', 5)],
        'Cinema': [('cinema', 8), ('filme', 5), ('diretor', 5), ('ator', 3)],
    },
}


def get_subtopico(discipline, texto):
    """Get subtopic based on discipline and question text using weighted scoring."""
    if not texto or not discipline:
        return ''
    
    texto_lower = texto.lower()
    discipline_topics = SUBTOPIC_KEYWORDS.get(discipline, {})
    
    best_sub = None
    best_score = 0
    
    for subtopico, signals in discipline_topics.items():
        score = 0
        for keyword, weight in signals:
            if keyword.lower() in texto_lower:
                score += weight
        if score > best_score:
            best_score = score
            best_sub = subtopico
    
    if best_sub and best_score >= 3:
        return best_sub
    
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
        texto = question.get('texto', '')
        
        # Detect discipline from content
        correct_disc, score = detect_discipline(texto)
        
        if correct_disc:
            # Set area based on detected discipline
            correct_area = DISC_TO_AREA.get(correct_disc, '')
            if correct_area and question.get('area') != correct_area:
                question['area'] = correct_area
                area_fixed += 1
            
            # Set discipline
            if question.get('disciplina') != correct_disc:
                question['disciplina'] = correct_disc
                disc_fixed += 1
            
            # Set subtopic
            correct_sub = get_subtopico(correct_disc, texto)
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
