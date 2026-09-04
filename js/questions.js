const QUESTIONS = {
  linguagens: [
    // PORTUGUÊS (1-20)
    {
      id: 1, area: "linguagens", disciplina: "portugues",
      enunciado: "Leia o fragmento abaixo.\n\n\"A língua portuguesa é uma língua viva, em constante transformação. Palavras novas surgem, outras caem em desuso, e o significado dos termos pode mudar ao longo do tempo.\"\n\nA respeito do texto, assinale a alternativa que apresenta uma transformação linguística ocorrida na língua portuguesa contemporânea.",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O uso da vírgula antes do 'e' em orações coordenadas explicativas.",
        "A substituição do 'você' pelo 'tu' em todas as regiões do Brasil.",
        "A incorporação de termos da língua inglesa no vocabulário cotidiano.",
        "A uniformização da pronúncia de todas as palavras em todo o país.",
        "A proibição do uso de gírias na comunicação formal."
      ],
      gabarito: "C",
      dificuldade: 1, // fácil
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 2, area: "linguagens", disciplina: "portugues",
      enunciado: "Considere o período a seguir.\n\n\"Embora o projeto tenha sido aprovado, ainda não foi implementado devido à falta de recursos financeiros.\"\n\nA alternativa que apresenta a análise gramatical correta da oração sublinhada é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Subordinada Adjetiva Restritiva,.functions as complemento nominal.",
        "Subordinada Concessiva, introduzida pela conjunção 'embora'.",
        "Subordinada Condicional, condicionando a ação principal.",
        "Subordinada Temporal, estabelecendo relação de tempo.",
        "Coordenada Sindética Adversativa, indicando oposição."
      ],
      gabarito: "B",
      dificuldade: 2, // médio
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 3, area: "linguagens", disciplina: "portugues",
      enunciado: "Leia o poema abaixo.\n\n\"No meio do caminho tinha uma pedra\ntinha uma pedra no meio do caminho\ntinha uma pedra\ntinha uma pedra no meio do caminho tinha uma pedra.\"\n\n— Carlos Drummond de Andrade\n\nAssinale a alternativa que melhor interpreta a repetição do verso \"tinha uma pedra\".",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Indica a monotonia e a persistência de um obstáculo na vida do sujeito lírico.",
        "Demonstra a incapacidade do poeta de encontrar sinônimos para a palavra 'pedra'.",
        "Representa a tentativa de memorização da palavra por parte do leitor.",
        "Cria um efeito de musicalidade sem nenhum significado profundo.",
        "Sugere que o caminho é composto apenas por uma única pedra."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 4, area: "linguagens", disciplina: "portugues",
      enunciado: "Na frase \"Os estudantes, cansados após a prova, saíram em silêncio\", a vírgula após \"estudantes\" e após \"prova\" tem a função de:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Separar termos de uma enumeração.",
        "Isolar uma oração explicativa, explicando o estado dos estudantes.",
        "Separar sujeito do predicado.",
        "Indicar suppressão de palavras.",
        "Introduzir uma oração consecutiva."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 5, area: "linguagens", disciplina: "portugues",
      enunciado: "Leia o texto abaixo.\n\n\"A internet revolucionou a forma como nos comunicamos. No entanto, o excesso de informações pode gerar uma sobrecarga cognitiva, dificultando a capacidade de filtrar o que é relevante.\"\n\nA expressão \"sobrecarga cognitiva\", utilizada no texto, refere-se:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "À incapacidade total de processar qualquer tipo de informação.",
        "Ao acúmulo excessivo de informações que dificulta a absorção do conhecimento.",
        "À falta de acesso à internet em algumas regiões.",
        "À sobrecarga de trabalho causada pelo uso de computadores.",
        "À velocidade excessiva da transmissão de dados."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 6, area: "linguagens", disciplina: "portugues",
      enunciado: "Considere a frase: \"Quem não arrisca, não petisca.\" No contexto da frase, a locução verbal \"não petisca\" expressa:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Uma ação de roubar escondido.",
        "Uma consequência negativa para quem não arrisca.",
        "Uma recompensa que virá em breve.",
        "Um verbo no gerúndio indicando continuidade.",
        "Um substantivo abstrato."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.25
    },
    {
      id: 7, area: "linguagens", disciplina: "portugues",
      enunciado: "Na oração \"Fazia tanto frio que os rios congelaram\", a conjunção \"que\" estabelece uma relação de:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Causa, indicando a razão do frio.",
        "Consequência, indicando o resultado do frio intenso.",
        "Concessão, indicando contraste.",
        "Condicional, indicando condição.",
        "Finalidade, indicando objetivo."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 8, area: "linguagens", disciplina: "portugues",
      enunciado: "Leia o trecho: \"O governador anunciou, ontem, novas medidas para conter a crise econômica.\"\n\nA Supressão de vírgulas na frase alteraria sua compreensão da seguinte forma:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Não alteraria nada, pois as vírgulas são opcionais nesse caso.",
        "Faria com que \"ontem\" ficasse deslocado, gerando ambiguidade temporal.",
        "Transformaria \"ontem\" em vocativo.",
        "Criaria uma aposição para \"governador\".",
        "Indicaria omissão de palavras na oração."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 9, area: "linguagens", disciplina: "portugues",
      enunciado: "\"Se eu fosse você, estudaria mais.\" A frase acima apresenta uma construção no:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Presente do indicativo em ambas as orações.",
        "Futuro do presente com verbo modificado.",
        "Futuro do pretérito (condicional) no verbo principal e pretérito imperfeito do subjuntivo na oração condicional.",
        "Pretérito perfeito do indicativo em ambas as orações.",
        "Presente do subjuntivo em ambas as orações."
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 10, area: "linguagens", disciplina: "portugues",
      enunciado: "Leia o poema:\n\n\"Eu,ROTO,de,peito,aberto,\npor,dentro,de,um,caderno,\nvou,escrevendo,com,cuidado,\nversos,que,são,meu,cotidiano.\"\n\nA marcação de vírgulas entre cada palavra do poema sugere:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Um erro de pontuação que deveria ser corrigido.",
        "O ritmo truncado e a fragmentação da fala cotidiana.",
        "A necessidade de ler cada palavra pausadamente.",
        "Uma tentativa de aumentar o número de palavras no poema.",
        "A impossibilidade de usar vírgulas em poesia."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 11, area: "linguagens", disciplina: "ingles",
      enunciado: "Read the text below.\n\n\"The new environmental policy aims to reduce carbon emissions by 30% by 2030.\"\n\nWhat is the main idea of the text?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "The government will increase carbon emissions by 2030.",
        "The new policy seeks to decrease carbon emissions significantly.",
        "Environmental policies have been abandoned.",
        "Carbon emissions will remain the same until 2030.",
        "The policy only applies to small companies."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 12, area: "linguagens", disciplina: "ingles",
      enunciado: "\"If I had known about the meeting, I would have attended it.\"\n\nThe sentence above uses:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Simple present tense.",
        "Past simple tense.",
        "Third conditional (conditional perfect).",
        "First conditional.",
        "Future perfect tense."
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 13, area: "linguagens", disciplina: "espanhol",
      enunciado: "Lee el siguiente texto.\n\n\"La contaminación del aire es un problema mundial que afecta la salud de millones de personas.\"\n\nLa idea principal del texto es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "El aire está limpio en todas partes del mundo.",
        "La contaminación del aire es un problema global de salud.",
        "Solo unas pocas personas se ven afectadas por la contaminación.",
        "La contaminación solo afecta a los animales.",
        "No existe contaminación del aire en los países desarrollados."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 14, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"Si yo tuviera dinero, viajaría por todo el mundo.\" La frase anterior presenta una construcción verbal en:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Presente de indicativo en ambas las oraciones.",
        "Futuro simple con verbo modificado.",
        "Condicional compuesto con pretérito imperfecto de subjuntivo.",
        "Pretérito perfecto en ambas las oraciones.",
        "Presente de subjuntivo en ambas las oraciones."
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.6, triAcertoAcaso: 0.2
    },
    {
      id: 15, area: "linguagens", disciplina: "artes",
      enunciado: "Sobre a arte brasileira, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O Modernismo brasileiro teve como marco a Semana de Arte Moderna de 1922.",
        "A arte brasileira começou apenas no século XX.",
        "O Barroco brasileiro não teve nenhum representante importante.",
        "A arte contemporânea não existe no Brasil.",
        "O Realismo foi o primeiro movimento artístico brasileiro."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.25
    },
    {
      id: 16, area: "linguagens", disciplina: "literatura",
      enunciado: "Leia o trecho abaixo.\n\n\"Tudo o que um estudante precisa saber sobre a obra de Machado de Assis é que ele foi o maior escritor da língua portuguesa.\"\n\nA afirmação acima é problemática porque:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Machado de Assis não escreveu obras literárias.",
        "Reduz a complexidade da obra machadiana a uma única afirmação absoluta.",
        "O texto não apresenta qualquer problema.",
        "Machado de Assis escreveu apenas em espanhol.",
        "Não existem críticos literários que estudem Machado."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 17, area: "linguagens", disciplina: "educacao_fisica",
      enunciado: "A prática regular de atividade física contribui para a manutenção da saúde de diversas formas. Assinale a alternativa que apresenta um benefício comprovado da atividade física regular.",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Aumento do risco de doenças cardiovasculares.",
        "Redução do estresse e melhoria da qualidade do sono.",
        "Aumento do sedentarismo.",
        "Redução da capacidade respiratória.",
        "Aumento da pressão arterial."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.9, triAcertoAcaso: 0.2
    },
    {
      id: 18, area: "linguagens", disciplina: "portugues",
      enunciado: "\"O livro, que era da biblioteca, foi devolvido ontem.\" A oração relativa \"que era da biblioteca\" pode ser classificada como:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Subordinada Adjetiva Restritiva.",
        "Subordinada Adjetiva Explicativa.",
        "Subordinada Substantiva Subjetiva.",
        "Subordinada Adverbial Condicional.",
        "Coordenada Sindética Alternativa."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 19, area: "linguagens", disciplina: "tic",
      enunciado: "Sobre a segurança da informação no contexto digital, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Senhas fracas são tão seguras quanto senhas complexas.",
        "O phishing é uma técnica que engana o usuário para obter dados pessoais.",
        "Firewalls são desnecessários em redes domésticas.",
        "Antivírus não são importantes para a segurança digital.",
        "Dados pessoais na internet são sempre protegidos automaticamente."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 20, area: "linguagens", disciplina: "ingles",
      enunciado: "\"She has been studying English for five years.\"\n\nThe tense used in the sentence is:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Simple past.",
        "Present perfect continuous.",
        "Future simple.",
        "Past continuous.",
        "Present perfect simple."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.6, triAcertoAcaso: 0.2
    },
    // LITERATURA (21-25)
    {
      id: 21, area: "linguagens", disciplina: "literatura",
      enunciado: "Na obra \"Memórias Póstumas de Brás Cubas\", de Machado de Assis, o narrador é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Um observador onisciente que narra em terceira pessoa.",
        "O próprio Brás Cubas, narrando de além-túmulo.",
        "Um personagem secundário da história.",
        "Um narrador sem identificação com nenhum personagem.",
        "O próprio leitor, convidado a narrar."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 22, area: "linguagens", disciplina: "literatura",
      enunciado: "O movimento literário que valorizava a linguagem coloquial, a quebra de normas gramaticais e a aproximação com a fala do povo foi:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O Arcadismo.",
        "O Realismo.",
        "O Modernismo.",
        "O Parnasianismo.",
        "O Naturalismo."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 23, area: "linguagens", disciplina: "literatura",
      enunciado: "\"Sempre a胞lua meiga, e aやungada, e a estrela d'alva...\" Esse fragmento apresenta marcas do movimento literário:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Modernismo, por usar palavras estrangeiras.",
        "Arcadismo, por valorizar a natureza e a simplicidade.",
        "Parnasianismo, por buscar perfeição formal.",
        "Romantismo, por expressar sentimentalismo.",
        "Realismo, por retratar a crueza da realidade."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 24, area: "linguagens", disciplina: "literatura",
      enunciado: "Na poesia de Vinícius de Moraes, tema recorrente é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A exaltação da natureza sem nenhum viés amoroso.",
        "O amor em todas as suas formas, do platônico ao carnal.",
        "A crítica política direta ao governo.",
        "O contato com o mundo sobrenatural.",
        "A rejeição de qualquer sentimento emocional."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 25, area: "linguagens", disciplina: "literatura",
      enunciado: "\"Quem disse queEu vim para fazer poesia? Eu vim para viver.\" (Manuel Bandeira)\n\nO verso acima manifesta a estética do:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Parnasianismo, com busca de perfeição formal.",
        "Modernismo, com a valorização da vida cotidiana e anti-formalismo.",
        "Arcadismo, com o louvor à natureza.",
        "Symbolismo, com o uso de sugestões.",
        "Romantismo, com a exaltação do eu."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    // INGLÊS (26-30)
    {
      id: 26, area: "linguagens", disciplina: "ingles",
      enunciado: "\"Despite the rain, we decided to go for a walk.\"\n\nThe word \"despite\" indicates:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Cause.",
        "Concession/contrast.",
        "Time.",
        "Purpose.",
        "Result."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 27, area: "linguagens", disciplina: "ingles",
      enunciado: "\"The report _____ finished by tomorrow.\"\n\nThe correct form of the verb to complete the sentence is:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "will be",
        "is being",
        "has been",
        "was being",
        "would be"
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.6, triAcertoAcaso: 0.2
    },
    {
      id: 28, area: "linguagens", disciplina: "ingles",
      enunciado: "\"It is essential that every student _____ the exam before the deadline.\"\n\nThe correct verb form is:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "submits",
        "submit",
        "submitted",
        "submitting",
        "will submit"
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.6, triAcertoAcaso: 0.2
    },
    {
      id: 29, area: "linguagens", disciplina: "ingles",
      enunciado: "\"The company has _____ its operations to several countries.\"\n\nThe correct word to fill in the blank is:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "expand",
        "expanded",
        "expanding",
        "expands",
        "expansion"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 30, area: "linguagens", disciplina: "ingles",
      enunciado: "\"She wouldn't have failed if she _____ harder.\"\n\nThe correct form to complete the sentence is:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "studied",
        "studies",
        "had studied",
        "would study",
        "has studied"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.55, triAcertoAcaso: 0.2
    },
    // ESPANHOL (31-35)
    {
      id: 31, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"Los estudiantes ________ (estudiar) mucho para el examen.\"\n\nLa forma correcta del verbo es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "estudiam",
        "estudiarán",
        "estudiaron",
        "estudian",
        "estudiarán"
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 32, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"Si yo ________ tiempo, viajaría a España.\"\n\nLa forma correcta del verbo en la oración condicional es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "tengo",
        "tendría",
        "tuviera",
        "tendrá",
        "tendría que"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.55, triAcertoAcaso: 0.2
    },
    {
      id: 33, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"El profesor ________ a los estudiantes la lección.\"\n\nEl pronombre correcto para completar la frase es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "le",
        "lo",
        "la",
        "les",
        "se"
      ],
      gabarito: "D",
      dificuldade: 2,
      triDisc: 0.5, triAcertoAcaso: 0.2
    },
    {
      id: 34, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"Ayer ________ (llover) mucho en la ciudad.\"\n\nLa forma verbal correcta es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "llueve",
        "lloverá",
        "llovió",
        "lloviendo",
        "llovía"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 35, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"Nosotros ________ al parque todos los domingos.\"\n\nLa forma correcta del verbo es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "vamos",
        "iremos",
        "íbamos",
        "fuimos",
        "vendremos"
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    // ARTES (36-38)
    {
      id: 36, area: "linguagens", disciplina: "artes",
      enunciado: "O Cinema Novo brasileiro, movimento dos anos 1960, é conhecido por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Produzir filmes com grandes orçamentos e efeitos especiais.",
        "Retratar a realidade social brasileira com baixo custo de produção.",
        "Seguir padrões hollywoodianos de narrativa.",
        "Produzir apenas filmes de ficção científica.",
        "Usar apenas atores estrangeiros."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 37, area: "linguagens", disciplina: "artes",
      enunciado: "A arte pop art, surgida nos anos 1960, caracterizou-se por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Usar apenas tons de preto e branco.",
        "Utilizar imagens da cultura popular e de massa.",
        "Representar exclusivamente paisagens naturais.",
        "Ser criada apenas por artistas brasileiros.",
        "Rejeitar qualquer influência da publicidade."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 38, area: "linguagens", disciplina: "artes",
      enunciado: "A música popular brasileira, reconhecida mundialmente, é uma manifestação artística que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Não tem influência da cultura africana.",
        "Reflete a mistura cultural do povo brasileiro.",
        "É apenas uma forma de entretenimento sem valor artístico.",
        "Não tem nenhum vínculo com a identidade nacional.",
        "Só existe no formato de samba."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    // EDUCAÇÃO FÍSICA (39-40)
    {
      id: 39, area: "linguagens", disciplina: "educacao_fisica",
      enunciado: "O sedentarismo é considerado um fator de risco para diversas doenças crônicas. Assinale a alternativa correta sobre o sedentarismo:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Afeta apenas pessoas idosas.",
        "Contribui para o aumento do risco de doenças cardíacas e diabetes.",
        "Não tem nenhum impacto na saúde.",
        "É benfazejo para o organismo.",
        "Só afeta atletas profissionais."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 40, area: "linguagens", disciplina: "educacao_fisica",
      enunciado: "Sobre a importância do aquecimento antes da atividade física, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O aquecimento é opcional e não traz benefícios.",
        "O aquecimento prepara o corpo para o exercício e reduz o risco de lesões.",
        "O aquecimento deve ser feito apenas por atletas profissionais.",
        "O aquecimento aumenta a probabilidade de lesões musculares.",
        "O aquecimento só é necessário em esportes coletivos."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    // TIC (41-42)
    {
      id: 41, area: "linguagens", disciplina: "tic",
      enunciado: "A rede social permite a comunicação instantânea entre pessoas de diferentes países. Sobre o uso responsável da internet, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "É permitido compartilhar dados pessoais sem restrição.",
        "O cyberbullying não é um problema nas redes sociais.",
        "É importante verificar a fonte das informações antes de compartilhá-las.",
        "Todas as informações da internet são sempre verdadeiras.",
        "A privacidade não é importante na internet."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 42, area: "linguagens", disciplina: "tic",
      enunciado: "A inteligência artificial (IA) tem sido aplicada em diversas áreas. Sobre a IA, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A IA não tem aplicação prática no cotidiano.",
        "A IA pode auxiliar em tarefas como reconhecimento de voz e tradução.",
        "A IA substitui completamente o trabalho humano em todas as áreas.",
        "A IA não representa nenhum risco à sociedade.",
        "A IA é uma tecnologia do passado."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    // QUESTÕES RESTANTES (43-45)
    {
      id: 43, area: "linguagens", disciplina: "portugues",
      enunciado: "\"O governo ________ novas medidas para conter a inflação.\" A forma verbal correta para preencher a lacuna é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "anunciará",
        "anunciou",
        "anuncia",
        "anunciariam",
        "anunciando"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 44, area: "linguagens", disciplina: "ingles",
      enunciado: "\"The book _____ by J.K. Rowling is very popular.\"\n\nThe correct form of the verb is:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "write",
        "wrote",
        "written",
        "writing",
        "writes"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.6, triAcertoAcaso: 0.2
    },
    {
      id: 45, area: "linguagens", disciplina: "espanhol",
      enunciado: "\"Ellos ________ (comer) en un restaurante anoche.\"\n\nLa forma correcta del verbo es:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "comen",
        "comerán",
        "comieron",
        "comiendo",
        "comían"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.7, triAcertoAcaso: 0.2
    }
  ],

  humanas: [
    // HISTÓRIA (1-15)
    {
      id: 46, area: "humanas", disciplina: "historia",
      enunciado: "Leia o trecho abaixo.\n\n\"A Proclamação da República, em 15 de novembro de 1889, marcou o fim do Império no Brasil e o início de um novo regime político.\"\n\nSobre a Proclamação da República, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Foi um movimento popular amplamente apoiado pela população.",
        "Foi liderada pelo Marechal Deodoro da Fonseca.",
        "Ocorreu antes da abolição da escravatura.",
        "Resultou na imediata instituição do voto feminino.",
        "Estabeleceu o Brasil como uma monarquia parlamentarista."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 47, area: "humanas", disciplina: "historia",
      enunciado: "A Revolução Francesa, ocorrida em 1789, é considerada um marco na história porque:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Aboliu a escravatura na Europa.",
        "Inspirou os ideais de liberdade, igualdade e fraternidade.",
        "Iniciou a Primeira Guerra Mundial.",
        "Criou o sistema feudal europeu.",
        "Estabeleceu a monarquia absoluta na França."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 48, area: "humanas", disciplina: "historia",
      enunciado: "A Segunda Guerra Mundial (1939-1945) teve como uma de suas principais consequências:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A queda do Muro de Berlim.",
        "A criação da ONU e a divisão da Alemanha.",
        "O início da Revolução Industrial.",
        "A independência dos Estados Unidos.",
        "O fim do colonialismo europeu na Ásia."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 49, area: "humanas", disciplina: "historia",
      enunciado: "O período da ditadura militar no Brasil (1964-1985) é caracterizado por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Ampla liberdade de expressão.",
        "Perseguição política e censura.",
        "Eleições diretas para presidente.",
        "Pleno funcionamento do Congresso Nacional.",
        "Fim do AI-5."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 50, area: "humanas", disciplina: "historia",
      enunciado: "A colonização portuguesa no Brasil teve como característica principal:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A instalação de vilas comerciais sem exploração agrícola.",
        "A exploração do trabalho escravo e a exportação de matérias-primas.",
        "O contato pacífico com os povos indígenas.",
        "A construção de grandes cidades desde o início.",
        "A democratização da terra entre colonos e indígenas."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    // GEOGRAFIA (16-30)
    {
      id: 51, area: "humanas", disciplina: "geografia",
      enunciado: "Leia o gráfico abaixo que representa a distribuição populacional do Brasil por região.\n\nSobre a distribuição populacional brasileira, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A região Norte é a mais populosa do Brasil.",
        "A região Sudeste concentra a maior parte da população.",
        "A região Centro-Oeste tem a menor população do país.",
        "A distribuição populacional é homogênea em todo o território.",
        "O Nordeste possui a maior densidade demográfica."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 52, area: "humanas", disciplina: "geografia",
      enunciado: "O aquecimento global é um tema de grande relevância ambiental. Sobre suas consequências, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O aumento da temperatura global não afeta o nível do mar.",
        "O derretimento das geleiras pode causar elevação do nível dos oceanos.",
        "O aquecimento global é causado apenas por fatores naturais.",
        "As mudanças climáticas não têm impacto na biodiversidade.",
        "O aquecimento global beneficia todas as regiões do planeta."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 53, area: "humanas", disciplina: "geografia",
      enunciado: "A globalização econômica tem gerado diversos impactos sociais. Uma das consequências negativas mais apontadas é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A diminuição das desigualdades sociais.",
        "O aumento da concentração de renda em poucos países.",
        "A melhoria das condições de trabalho em todos os países.",
        "O fim da pobreza mundial.",
        "A redução do comércio internacional."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 54, area: "humanas", disciplina: "geografia",
      enunciado: "O bioma Amazônia é considerado o maior bioma do Brasil. Sobre ele, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "É composto apenas por florestas tropicais.",
        "Abrange apenas o território brasileiro.",
        "Desempenha papel fundamental na regulação do clima global.",
        "Não sofre com atividades antrópicas.",
        "Tem sua vegetação composta exclusivamente por cerrado."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 55, area: "humanas", disciplina: "geografia",
      enunciado: "A urbanização acelerada no Brasil gerou diversos problemas sociais. Um dos principais é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A diminuição da população nas cidades.",
        "A formação de favelas e assentamentos precários.",
        "A redução da poluição do ar nas grandes cidades.",
        "O aumento da área rural no país.",
        "A redução do trânsito nas capitais."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    // SOCIOLOGIA (31-38)
    {
      id: 56, area: "humanas", disciplina: "sociologia",
      enunciado: "Leia o trecho abaixo.\n\n\"A desigualdade social é um dos principais desafios do Brasil contemporâneo. Segundo dados do IBGE, a concentração de renda permanece elevada.\"\n\nSobre a desigualdade social no Brasil, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A desigualdade social é um problema apenas dos países pobres.",
        "A desigualdade social pode gerar exclusão e conflitos.",
        "A desigualdade social não tem impacto na economia.",
        "A desigualdade social diminuiu drasticamente nos últimos anos.",
        "A desigualdade social é causada apenas pela falta de educação."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 57, area: "humanas", disciplina: "sociologia",
      enunciado: "O conceito de \"cidadania\" em T.H. Marshall refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Apenas ao direito de voto.",
        "Um conjunto de direitos civis, políticos e sociais.",
        "Exclusivamente aos direitos econômicos.",
        "Apenas à obligação de pagar impostos.",
        "Um conceito exclusivamente jurídico."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 58, area: "humanas", disciplina: "sociologia",
      enunciado: "A educação é considerada um forte elemento de mobilidade social. Sobre a relação entre educação e sociedade, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A educação não tem influência na ascensão social.",
        "O acesso à educação de qualidade pode reduzir as desigualdades sociais.",
        "A educação só beneficia as classes mais abastadas.",
        "A educação não é um direito social.",
        "A educação não tem impacto na economia."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 59, area: "humanas", disciplina: "sociologia",
      enunciado: "O conceito de \"etnocentrismo\" refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Valorizar todas as culturas igualmente.",
        "Julgar outras culturas a partir dos padrões da própria cultura.",
        "Estudar todas as culturas do mundo.",
        "Rejeitar todas as culturas diferentes.",
        "Acreditar que todas as culturas são inferiores."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 60, area: "humanas", disciplina: "sociologia",
      enunciado: "A mídia tem papel fundamental na formação de opinião pública. Sobre o papel da mídia, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A mídia é sempre imparcial e objetiva.",
        "A mídia pode influenciar a percepção da realidade.",
        "A mídia não tem impacto na sociedade.",
        "A mídia é controlada exclusivamente pelo governo.",
        "A mídia não tem responsabilidade social."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    // FILOSOFIA (39-45)
    {
      id: 61, area: "humanas", disciplina: "filosofia",
      enunciado: "\"Cogito, ergo sum\" (Penso, logo existo) é uma frase atribuída a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Sócrates.",
        "Platão.",
        "René Descartes.",
        "Aristóteles.",
        "Karl Marx."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.25
    },
    {
      id: 62, area: "humanas", disciplina: "filosofia",
      enunciado: "Sobre a ética kantiana, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A moral deve ser determinada pelas consequências da ação.",
        "A boa vontade é o único bem incondicional.",
        "A ética deve se basear exclusivamente nos desejos.",
        "O imperativo categórico é opcional na moralidade.",
        "A ética kantiana valoriza apenas os resultados práticos."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 63, area: "humanas", disciplina: "filosofia",
      enunciado: "O contrato social, tema desenvolvido por Rousseau, Hobbes e Locke, refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Um acordo entre cidadãos para viver em sociedade.",
        "Um contrato de trabalho entre empregador e empregado.",
        "Um documento jurídico que regula o comércio.",
        "Um acordo internacional entre países.",
        "Uma constituição de um país."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 64, area: "humanas", disciplina: "filosofia",
      enunciado: "A dialética hegeliana apresenta como estrutura básica:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Tese, antítese e síntese.",
        "Premissa, conclusão e axioma.",
        "Hipótese, tese e verificação.",
        "Afirmação, negação e refutação.",
        "Proposição, argumento e dedução."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 65, area: "humanas", disciplina: "filosofia",
      enunciado: "A filosofia socrática é conhecida por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A aceitação de qualquer verdade sem questionamento.",
        "O método de questionamento dialético (maiêutica).",
        "A busca pela verdade apenas em textos sagrados.",
        "O conhecimento baseado exclusivamente na experiência sensorial.",
        "A negação de qualquer forma de conhecimento."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 66, area: "humanas", disciplina: "historia",
      enunciado: "O Movimento dos Trabalhadores Rurais Sem Terra (MST) tem como principal demanda:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A reforma agrária e o acesso à terra.",
        "Aumento do salário mínimo.",
        "A redução da jornada de trabalho.",
        "O fim do trabalho escravo.",
        "A privatização das terras públicas."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 67, area: "humanas", disciplina: "historia",
      enunciado: "O/forum Social Mundial é um encontro que discute alternativas ao modelo neoliberal. Sua frase de ordem é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "\"Outro mundo é possível.\"",
        "\"A revolução é inevitável.\"",
        "\"O progresso a qualquer custo.\"",
        "\"Liberdade acima de tudo.\"",
        "\"O lucro é o objetivo da sociedade.\""
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.75, triAcertoAcaso: 0.2
    },
    {
      id: 68, area: "humanas", disciplina: "geografia",
      enunciado: "A Agropecuária brasileira é um dos principais setores da economia. Sobre a agropecuária, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O Brasil não é um grande exportador de produtos agrícolas.",
        "A agropecuária tem impacto ambiental negativo quando praticada de forma irresponsável.",
        "A agropecuária não tem relação com a economia nacional.",
        "O agronegócio não afeta o meio ambiente.",
        "A agropecuária brasileira é apenas de subsistência."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 69, area: "humanas", disciplina: "geografia",
      enunciado: "A matéria \"combustíveis fósseis\" é um dos principais recursos energéticos do mundo. Sobre os combustíveis fósseis, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "São recursos renováveis e inesgotáveis.",
        "São formados a partir de resíduos orgânicos ao longo de milhões de anos.",
        "Não contribuem para a poluição do ar.",
        "São utilizados apenas em países da Europa.",
        "Não têm impacto no aquecimento global."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 70, area: "humanas", disciplina: "filosofia",
      enunciado: "O utilitarismo, filosofia de John Stuart Mill, defende que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A moralidade deve ser julgada pelo princípio da maior felicidade para o maior número.",
        "A moralidade é determinada apenas pela religião.",
        "A moralidade não deve considerar consequências.",
        "A moralidade é relativa e não pode ser julgada.",
        "A moralidade é determinada exclusivamente pelo Estado."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 71, area: "humanas", disciplina: "historia",
      enunciado: "A independência do Brasil, proclamada em 7 de setembro de 1822, teve como principal líder:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Dom Pedro I.",
        "Dom Pedro II.",
        "Tiradentes.",
        "José Bonifácio.",
        "Marquês de Pombal."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.25
    },
    {
      id: 72, area: "humanas", disciplina: "historia",
      enunciado: "A abolição da escravatura no Brasil ocorreu em 1888 com a assinatura da Lei Áurea. Quem a assinou?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Dom Pedro I.",
        "Princesa Isabel.",
        "Deodoro da Fonseca.",
        "Getúlio Vargas.",
        "Tiradentes."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.25
    },
    {
      id: 73, area: "humanas", disciplina: "geografia",
      enunciado: "O clima tropical úmido é caracterizado por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Temperaturas baixas o ano todo.",
        "Temperaturas elevadas e chuvas bem distribuídas ao longo do ano.",
        "Estações bem definidas com invernos rigorosos.",
        "Chuvas concentradas apenas no inverno.",
        "Temperaturas constantes de 10°C."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 74, area: "humanas", disciplina: "geografia",
      enunciado: "O霓neômeno das Ilhas de Calor Urbanas ocorre quando:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "As cidades ficam mais frias que as áreas rurais.",
        "As áreas urbanas apresentam temperaturas superiores às áreas rurais.",
        "O nível do mar sobe nas cidades costeiras.",
        "A poluição do ar diminui nas cidades.",
        "As chuvas são mais intensas no campo."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 75, area: "humanas", disciplina: "sociologia",
      enunciado: "O conceito de 'favelização' refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A formação de bairros de classe alta.",
        "O processo de ocupação urbana informal e precária.",
        "A diminuição da população urbana.",
        "O crescimento ordenado das cidades.",
        "A construção de moradias populares pelo governo."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 76, area: "humanas", disciplina: "filosofia",
      enunciado: "Para Platão, o mundo sensível é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O mundo das ideias perfeitas.",
        "O mundo material e mutável que percebemos pelos sentidos.",
        "O mundo divino e eterno.",
        "O mundo dos sonhos.",
        "O mundo dos mortos."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 77, area: "humanas", disciplina: "historia",
      enunciado: "A Revolução Industrial, iniciada na Inglaterra no século XVIII, transformou:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A sociedade agrária em sociedade industrial.",
        "A sociedade industrial em sociedade agrária.",
        "A economia baseada no comércio de escravos.",
        "O sistema feudal em sistema capitalista.",
        "A religião em ciência."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 78, area: "humanas", disciplina: "geografia",
      enunciado: "O mercado internacional de commodities agrícolas é dominado por países como:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Brasil, EUA, Argentina e China.",
        "Japão, Alemanha e Itália.",
        "Austrália, Nova Zelândia e Canadá.",
        "Rússia, Índia e China.",
        "México, Colômbia e Peru."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 79, area: "humanas", disciplina: "sociologia",
      enunciado: "A mobilidade social refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A capacidade de se deslocar entre cidades.",
        "A capacidade de ascender ou descendendo na escala social.",
        "A mudança de residência de uma cidade para outra.",
        "O movimento de turistas entre países.",
        "A mobilização política de um grupo social."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 80, area: "humanas", disciplina: "filosofia",
      enunciado: "A \"alegoria da caverna\" é uma metáfora filosófica proposta por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Aristóteles.",
        "Sócrates.",
        "Platão.",
        "Descartes.",
        "Nietzsche."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 81, area: "humanas", disciplina: "historia",
      enunciado: "O Estado Novo, regime autoritário no Brasil, foi implantado por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Getúlio Vargas.",
        "Juscelino Kubitschek.",
        "Jânio Quadros.",
        "Castelo Branco.",
        "Fernando Henrique Cardoso."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 82, area: "humanas", disciplina: "geografia",
      enunciado: "A monocultura é uma prática agrícola que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Cultiva apenas um tipo de plantação em larga escala.",
        "Cultiva diversos tipos de plantas na mesma área.",
        "Não tem impacto ambiental.",
        "É uma técnica sustentável.",
        "É praticada apenas em pequenas propriedades."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 83, area: "humanas", disciplina: "sociologia",
      enunciado: "O conceito de 'exclusão social' refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Um processo de marginalização que impede o acesso a direitos básicos.",
        "A separação de pessoas por motivos religiosos.",
        "O isolamento geográfico de comunidades.",
        "A exclusão de atletas de competições.",
        "A proibição de entrada em determinados locais."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 84, area: "humanas", disciplina: "filosofia",
      enunciado: "O existencialismo é uma corrente filosófica que enfatiza:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A existência precede a essência e a liberdade individual.",
        "A existência de Deus como explicação para tudo.",
        "A negação de qualquer forma de existência.",
        "A busca pela felicidade material.",
        "A aceitação passiva do destino."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 85, area: "humanas", disciplina: "historia",
      enunciado: "A ditadura militar brasileira (1964-1985) teve como marca principal:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A ampliação da democracia.",
        "A repressão política e a censura.",
        "O fortalecimento do Congresso Nacional.",
        "A garantia de eleições diretas.",
        "A liberdade de imprensa."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 86, area: "humanas", disciplina: "geografia",
      enunciado: "A energia renovável é aquela que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Se esgota com o uso.",
        "Não causa impacto ambiental.",
        "Não se esgota e é naturalmente reposta.",
        "Só pode ser usada em usinas nucleares.",
        "É encontrada apenas em países desenvolvidos."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 87, area: "humanas", disciplina: "sociologia",
      enunciado: "A globalização cultural refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A homogeneização cultural causada pela influência de grandes empresas e mídias.",
        "A valorização de todas as culturas locais.",
        "O isolamento cultural entre países.",
        "A proibição de influências estrangeiras.",
        "A criação de novas línguas."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 88, area: "humanas", disciplina: "filosofia",
      enunciado: "O método cartesiano de Descartes baseia-se em:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A dúvida como ponto de partida para o conhecimento.",
        "A aceitação de verdades absolutas sem questionamento.",
        "A observação exclusiva da natureza.",
        "A valorização da emoção sobre a razão.",
        "A negação da existência do mundo externo."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 89, area: "humanas", disciplina: "historia",
      enunciado: "O governo de Juscelino Kubitschek (1956-1961) é marcado pelo slogan:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "\"O petróleo é nosso\".",
        "\"Cinquenta anos em cinco\".",
        "\"Brasil, ame-o ou deixe-o\".",
        "\"Ordem e progresso\".",
        "\"Paz e amor\"."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 90, area: "humanas", disciplina: "geografia",
      enunciado: "O conceito de 'desenvolvimento sustentável' refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Um desenvolvimento que atende as necessidades sem comprometer as futuras gerações.",
        "Um desenvolvimento baseado apenas no crescimento econômico.",
        "A exploração indiscriminada de recursos naturais.",
        "O desenvolvimento tecnológico sem limites.",
        "A urbanização acelerada sem planejamento."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    }
  ],

  natureza: [
    // FÍSICA (1-15)
    {
      id: 91, area: "natureza", disciplina: "fisica",
      enunciado: "Um corpo em queda livre é solto de uma altura de 80 metros. Desprezando a resistência do ar e considerando g = 10 m/s², o tempo necessário para o corpo atingir o solo é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "2 segundos.",
        "4 segundos.",
        "8 segundos.",
        "16 segundos.",
        "40 segundos."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 92, area: "natureza", disciplina: "fisica",
      enunciado: "Sobre a Segunda Lei de Newton, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A força resultante sobre um corpo é igual ao produto de sua massa pela aceleração.",
        "A velocidade de um corpo é sempre constante.",
        "A força de atrito é sempre nula.",
        "A energia não pode ser transformada.",
        "A massa de um corpo não pode ser alterada."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 93, area: "natureza", disciplina: "fisica",
      enunciado: "Um automóvel percorre 240 km em 3 horas. Sua velocidade média, em km/h, é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "60 km/h.",
        "72 km/h.",
        "80 km/h.",
        "90 km/h.",
        "120 km/h."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 94, area: "natureza", disciplina: "fisica",
      enunciado: "Um objeto de massa 5 kg está sobre uma superfície horizontal. Sabendo que a aceleração da gravidade é 10 m/s², o peso desse objeto é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "0,5 N.",
        "5 N.",
        "50 N.",
        "500 N.",
        "5.000 N."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 95, area: "natureza", disciplina: "fisica",
      enunciado: "A Lei da Conservação da Energia Mecânica afirma que, na ausência de forças dissipativas, a soma da energia cinética e potencial de um sistema:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Diminui ao longo do tempo.",
        "Aumenta ao longo do tempo.",
        "Permanece constante.",
        "Depende da massa do corpo.",
        "É sempre nula."
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    // QUÍMICA (16-30)
    {
      id: 96, area: "natureza", disciplina: "quimica",
      enunciado: "Sobre a tabela periódica, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Os elementos estão organizados por massa atômica crescente.",
        "Os elementos são organizados por número atômico crescente.",
        "A tabela periódica não tem qualquer organização.",
        "Todos os elementos da tabela são metais.",
        "A tabela foi criada por Albert Einstein."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 97, area: "natureza", disciplina: "quimica",
      enunciado: "Uma reação química é considerada exotérmica quando:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Absorve calor do meio ambiente.",
        "Libera calor para o meio ambiente.",
        "Não envolve troca de energia.",
        "Ocorre apenas em altas temperaturas.",
        "Não produz nenhum produto."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 98, area: "natureza", disciplina: "quimica",
      enunciado: "O pH de uma solução é igual a 3. Essa solução é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Neutra.",
        "Ácida.",
        "Básica.",
        "Anfótera.",
        "Ampla."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.25
    },
    {
      id: 99, area: "natureza", disciplina: "quimica",
      enunciado: "Sobre a água (H₂O), é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "É um composto formado por dois átomos de hidrogênio e um de oxigênio.",
        "É um elemento químico.",
        "Não é importante para a vida.",
        "É formada por três átomos de carbono.",
        "É um gás em temperatura ambiente."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 100, area: "natureza", disciplina: "quimica",
      enunciado: "A corrosão do ferro é um processo químico que ocorre quando:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O ferro é exposto ao oxigênio e à umidade.",
        "O ferro é isolado do ar.",
        "O ferro é submetido a temperaturas extremamente baixas.",
        "O ferro é misturado com ouro.",
        "O ferro é colocado em vácuo perfeito."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    // BIOLOGIA (31-45)
    {
      id: 101, area: "natureza", disciplina: "biologia",
      enunciado: "Sobre a célula, unidade básica da vida, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "As células procariotas possuem núcleo definido.",
        "As células eucariotas possuem núcleo delimitado por membrana.",
        "Todas as células são iguais em estrutura.",
        "As células não realizam metabolismo.",
        "As células são visíveis a olho nu."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 102, area: "natureza", disciplina: "biologia",
      enunciado: "A fotossíntese é o processo pelo qual:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Os seres humanos produzem energia a partir da comida.",
        "As plantas produzem gás oxigênio e glicose a partir de luz solar.",
        "Os animais respiram oxigênio e eliminam gás carbônico.",
        "As bactérias se reproduzem por divisão binária.",
        "Os fungos se alimentam de matéria orgânica morta."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 103, area: "natureza", disciplina: "biologia",
      enunciado: "A seleção natural, conceito proposto por Charles Darwin, refere-se a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A capacidade dos organismos mais adaptados ao ambiente de sobreviver e se reproduzir.",
        "A alteração artificial de genes em laboratório.",
        "A separação artificial de espécies.",
        "O processo de extinção de todas as espécies.",
        "A domesticação de animais selvagens."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 104, area: "natureza", disciplina: "biologia",
      enunciado: "O DNA é a molécula que armazena as informações genéticas. Sua estrutura é descrita como:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Uma cadeia simples de nucleotídeos.",
        "Uma dupla hélice de nucleotídeos.",
        "Uma estrutura esférica de proteínas.",
        "Uma cadeia de aminoácidos.",
        "Um composto químico inorgânico."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 105, area: "natureza", disciplina: "biologia",
      enunciado: "As doenças cardiovasculares são uma das principais causas de morte no mundo. Sobre essas doenças, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Afetam apenas pessoas idosas.",
        "Podem ser prevenidas com hábitos saudáveis.",
        "Não têm relação com a alimentação.",
        "Só afetam homens.",
        "Não possuem tratamento médico."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 106, area: "natureza", disciplina: "fisica",
      enunciado: "A velocidadeda luz no vácuo é aproximadamente:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "300.000 km/s.",
        "300.000 m/s.",
        "300 km/s.",
        "3.000.000 km/s.",
        "30 km/s."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 107, area: "natureza", disciplina: "fisica",
      enunciado: "Um corpo de massa 10 kg move-se com aceleração constante de 2 m/s². A força resultante sobre o corpo é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "5 N.",
        "10 N.",
        "20 N.",
        "100 N.",
        "200 N."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 108, area: "natureza", disciplina: "quimica",
      enunciado: "O gás oxigênio (O₂) é essencial para:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A combustão e a respiração aeróbica.",
        "A fermentação alcoólica.",
        "A produção de ácido clorídrico.",
        "A neutralização de ácidos.",
        "A formação de sais."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 109, area: "natureza", disciplina: "quimica",
      enunciado: "O soluço da soda cáustica (NaOH) em água resulta em uma solução:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Ácida.",
        "Neutra.",
        "Básica.",
        "Anfótera.",
        "Ampla."
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 110, area: "natureza", disciplina: "biologia",
      enunciado: "A cadeia alimentar é um modelo que mostra como a energia se transfere entre os seres vivos. Nela, os produtores são:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Os organismos que se alimentam de outros seres vivos.",
        "Os organismos que produzem seu próprio alimento (plantas).",
        "Os decompositores.",
        "Os consumidores secundários.",
        "Os predadores."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 111, area: "natureza", disciplina: "fisica",
      enunciado: "A energia elétrica é uma forma de energia muito utilizada no cotidiano. A unidade de medida de energia elétrica é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Watt (W).",
        "Volt (V).",
        "Joule (J) ou Quilowatt-hora (kWh).",
        "Ampère (A).",
        "Ohm (Ω)."
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 112, area: "natureza", disciplina: "quimica",
      enunciado: "O radônio é um gás nobre radioativo. Sobre os gases nobres, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Reagem facilmente com outros elementos.",
        "Possuem camada de valência completa.",
        "São altamente reativos.",
        "Não existem na natureza.",
        "Só existem em laboratório."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 113, area: "natureza", disciplina: "biologia",
      enunciado: "A mitose é um tipo de divisão celular que resulta em:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Duas células-filhas geneticamente idênticas à célula-mãe.",
        "Quatro células-filhas com metade dos cromossomos.",
        "Apenas uma célula-filha.",
        "Células com número variável de cromossomos.",
        "Células idênticas à célula-mãe, mas com mutações."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 114, area: "natureza", disciplina: "fisica",
      enunciado: "A Primeira Lei da Termodinâmica afirma que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A energia não pode ser criada nem destruída, apenas transformada.",
        "A energia sempre se perde no meio ambiente.",
        "A entropia sempre diminui.",
        "O calor sempre flui do corpo frio para o quente.",
        "A temperatura é constante em todos os corpos."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 115, area: "natureza", disciplina: "biologia",
      enunciado: "Os antibióticos são medicamentos usados para combater infecções bacterianas. Sobre os antibióticos, é correto afirmar que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Devem ser usados indiscriminadamente.",
        "O uso inadequado pode gerar resistência bacteriana.",
        "São eficazes contra vírus.",
        "Não precisam de prescrição médica.",
        "Devem ser tomados mesmo após o fim dos sintomas."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 116, area: "natureza", disciplina: "quimica",
      enunciado: "O elemento químico oxigênio (O₂) é essencial para:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A respiração aeróbica dos seres vivos.",
        "A produção deonly ferro.",
        "A fabricação de vidro.",
        "A neutralização de ácidos.",
        "A formação de sais minerais."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 117, area: "natureza", disciplina: "biologia",
      enunciado: "A mitose é um tipo de divisão celular que resulta em:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Duas células-filhas geneticamente idênticas à célula-mãe.",
        "Quatro células-filhas com metade dos cromossomos.",
        "Apenas uma célula-filha.",
        "Células com número variável de cromossomos.",
        "Células com mutações intencionais."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 118, area: "natureza", disciplina: "fisica",
      enunciado: "A unidade de medida de força no Sistema Internacional é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Joule (J).",
        "Newton (N).",
        "Watt (W).",
        "Pascal (Pa).",
        "Ampère (A)."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 119, area: "natureza", disciplina: "quimica",
      enunciado: "A água (H₂O) é formada por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Dois átomos de hidrogênio e um de oxigênio.",
        "Um átomo de hidrogênio e dois de oxigênio.",
        "Três átomos de carbono.",
        "Dois átomos de nitrogênio.",
        "Um átomo de hélio e um de oxigênio."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 120, area: "natureza", disciplina: "biologia",
      enunciado: "O sistema circulatório é responsável por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Transportar oxigênio e nutrientes para as células.",
        "Realizar a fotossíntese.",
        "Produzir hormônios.",
        "Realizar a digestão dos alimentos.",
        "Armazenar informações genéticas."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 121, area: "natureza", disciplina: "fisica",
      enunciado: "A energia cinética de um corpo depende de:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Sua massa e sua velocidade ao quadrado.",
        "Apenas de sua massa.",
        "Apenas de sua velocidade.",
        "De sua altura.",
        "De sua temperatura."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 122, area: "natureza", disciplina: "quimica",
      enunciado: "Um ácido é uma substância que em solução aquosa:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Libera íons hidrônio (H₃O⁺).",
        "Libera íons hidróxido (OH⁻).",
        "Não libera nenhum íon.",
        "Aumenta o pH da solução.",
        "Neutraliza bases completamente."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 123, area: "natureza", disciplina: "biologia",
      enunciado: "As células nervosas (neurônios) são responsáveis por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        " transmitir impulsos elétricos e químicos no organismo.",
        "Produzir insulina.",
        "Armazenar gordura.",
        "Realizar a respiração celular.",
        "Formar os ossos."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 124, area: "natureza", disciplina: "fisica",
      enunciado: "O princípio de Arquimedes afirma que um corpo imerso em um fluido sofre uma força para cima igual a:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Seu peso próprio.",
        "O peso do fluido deslocado.",
        "O dobro de seu peso.",
        "Metade de seu volume.",
        "Zero."
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 125, area: "natureza", disciplina: "quimica",
      enunciado: "O processo de destilação é utilizado para:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Separar líquidos com pontos de ebulição diferentes.",
        "Separar sólidos insolúveis.",
        "Misturar dois líquidos.",
        "Aumentar a temperatura de uma solução.",
        "Produzir gases."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 126, area: "natureza", disciplina: "biologia",
      enunciado: "A evolução das espécies, proposta por Charles Darwin, baseia-se em:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A seleção natural e a sobrevivência dos mais adaptados.",
        "A criação divina de todas as espécies.",
        "A mutação intencional dos genes.",
        "A imutabilidade das espécies.",
        "A migração forçada dos animais."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 127, area: "natureza", disciplina: "fisica",
      enunciado: "A velocidade do som no ar é aproximadamente:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "340 m/s.",
        "3.000 m/s.",
        "30.000 m/s.",
        "300 m/s.",
        "3.000.000 m/s."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 128, area: "natureza", disciplina: "quimica",
      enunciado: "O craqueamento é um processo químico utilizado na refinaria de petróleo para:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Quebrar moléculas grandes em menores.",
        "Aumentar o tamanho das moléculas.",
        "Separar metais.",
        "Produzir plásticos.",
        "Eliminar impurezas da água."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 129, area: "natureza", disciplina: "biologia",
      enunciado: "Os seres vivos são classificados em cinco reinos. O reino Monera é composto por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Organismos procariotas como bactérias e cianobactérias.",
        "Fungos como cogumelos e leveduras.",
        "Plantas como árvores e samambaias.",
        "Animais como insetos e vertebrados.",
        "Protistas como amebas e euglenas."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 130, area: "natureza", disciplina: "fisica",
      enunciado: "A densidade de um corpo é calculada pela relação entre:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Massa e volume.",
        "Peso e altura.",
        "Velocidade e tempo.",
        "Força e área.",
        "Energia e tempo."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 131, area: "natureza", disciplina: "quimica",
      enunciado: "O pH de uma solução neutra é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "0.",
        "7.",
        "14.",
        "3.",
        "10."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 132, area: "natureza", disciplina: "biologia",
      enunciado: "O vírus da gripe é um agente patogênico que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Não possui células e depende de um hospedeiro para se reproduzir.",
        "É composto apenas por proteínas.",
        "Pode ser combatido com antibióticos.",
        "Não causa doenças em humanos.",
        "É visível ao microscópio óptico comum."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 133, area: "natureza", disciplina: "fisica",
      enunciado: "A refração da luz é o fenômeno que ocorre quando a luz:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Muda de direção ao passar de um meio para outro.",
        "É absorvida por um corpo negro.",
        "É refletida por uma superfície plana.",
        "Viaja em linha reta no vácuo.",
        "É emitida por uma estrela."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 134, area: "natureza", disciplina: "quimica",
      enunciado: "O combústão é uma reação química que:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Libera energia na forma de calor e luz.",
        "Absorve energia do meio ambiente.",
        "Não envolve oxigênio.",
        "Ocorre apenas em temperaturas baixas.",
        "Produz apenas água."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 135, area: "natureza", disciplina: "biologia",
      enunciado: "O ciclo do nitrogênio é fundamental para a vida porque:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "Permite que o nitrogênio seja incorporado aos organismos vivos.",
        "Produz oxigênio para a respiração.",
        "Aumenta a temperatura do solo.",
        "Destroi bactérias do solo.",
        "Reduz a quantidade de CO₂ na atmosfera."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    }
  ],

  matematica: [
    // ÁLGEBRA (1-15)
    {
      id: 136, area: "matematica", disciplina: "algebra",
      enunciado: "Resolva a equação: 2x + 5 = 15",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "x = 3",
        "x = 5",
        "x = 10",
        "x = 7,5",
        "x = 20"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 137, area: "matematica", disciplina: "algebra",
      enunciado: "Se f(x) = 3x² - 2x + 1, qual é o valor de f(2)?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "5",
        "9",
        "13",
        "17",
        "21"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 138, area: "matematica", disciplina: "algebra",
      enunciado: "Qual é o valor de x que satisfaz a equação: log₂(x) = 3?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "6",
        "8",
        "9",
        "16",
        "27"
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 139, area: "matematica", disciplina: "algebra",
      enunciado: "Em uma progressão aritmética (PA) o primeiro termo é 3 e a razão é 5. Qual é o quarto termo?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "12",
        "15",
        "18",
        "23",
        "20"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 140, area: "matematica", disciplina: "algebra",
      enunciado: "Uma progressão geométrica (PG) tem primeiro termo igual a 2 e razão igual a 3. Qual é o terceiro termo?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "6",
        "9",
        "18",
        "27",
        "54"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    // GEOMETRIA (16-30)
    {
      id: 141, area: "matematica", disciplina: "geometria",
      enunciado: "A área de um triângulo de base 10 cm e altura 6 cm é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "16 cm²",
        "30 cm²",
        "60 cm²",
        "160 cm²",
        "36 cm²"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 142, area: "matematica", disciplina: "geometria",
      enunciado: "O volume de um cilindro com raio da base 3 cm e altura 10 cm é (use π = 3):",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "30 cm³",
        "90 cm³",
        "270 cm³",
        "300 cm³",
        "900 cm³"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 143, area: "matematica", disciplina: "geometria",
      enunciado: "Em um triângulo retângulo, os catetos medem 3 cm e 4 cm. A hipotenusa mede:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "5 cm",
        "6 cm",
        "7 cm",
        "12 cm",
        "25 cm"
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 144, area: "matematica", disciplina: "geometria",
      enunciado: "A circunferência de um círculo de raio 5 cm é (use π = 3,14):",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "15,7 cm",
        "31,4 cm",
        "78,5 cm",
        "157 cm",
        "314 cm"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 145, area: "matematica", disciplina: "geometria",
      enunciado: "A área de um quadrado com lado de 7 cm é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "14 cm²",
        "21 cm²",
        "28 cm²",
        "49 cm²",
        "64 cm²"
      ],
      gabarito: "D",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    // ESTATÍSTICA E PROBABILIDADE (31-45)
    {
      id: 146, area: "matematica", disciplina: "estatistica",
      enunciado: "As notas de um aluno nas 5 provas foram: 6, 8, 7, 9 e 10. A média aritmética das notas é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "7",
        "7,5",
        "8",
        "8,5",
        "9"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 147, area: "matematica", disciplina: "estatistica",
      enunciado: "Em um conjunto de dados {2, 3, 5, 5, 7, 8, 10}, a moda é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "3",
        "5",
        "7",
        "8",
        "10"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 148, area: "matematica", disciplina: "probabilidade",
      enunciado: "Ao lançar um dado justo de 6 faces, a probabilidade de obter um número maior que 4 é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/6",
        "2/6 = 1/3",
        "3/6 = 1/2",
        "4/6 = 2/3",
        "5/6"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 149, area: "matematica", disciplina: "estatistica",
      enunciado: "Os valores 4, 6, 8, 10 e 12 formam uma progressão aritmética. A razão dessa PA é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1",
        "2",
        "3",
        "4",
        "6"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 150, area: "matematica", disciplina: "probabilidade",
      enunciado: "Em uma sacola com 3 bolas vermelhas e 2 bolas azuis, qual é a probabilidade de sortear uma bola vermelha?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/5",
        "2/5",
        "3/5",
        "4/5",
        "1/2"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 151, area: "matematica", disciplina: "algebra",
      enunciado: "Qual é o valor de x na equação: 3(x - 2) = 15?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "3",
        "5",
        "7",
        "9",
        "11"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 152, area: "matematica", disciplina: "algebra",
      enunciado: "Se 2^x = 32, o valor de x é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "3",
        "4",
        "5",
        "6",
        "8"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 153, area: "matematica", disciplina: "geometria",
      enunciado: "A área de um trapézio de bases 8 cm e 12 cm, e altura 5 cm, é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "25 cm²",
        "40 cm²",
        "50 cm²",
        "60 cm²",
        "100 cm²"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 154, area: "matematica", disciplina: "estatistica",
      enunciado: "Em um gráfico de barras que representa a preferência musical de 100 pessoas, 40 preferem rock, 30 sertanejo e 30 pagode. A porcentagem de pessoas que preferem rock é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "25%",
        "30%",
        "40%",
        "50%",
        "60%"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 155, area: "matematica", disciplina: "probabilidade",
      enunciado: "Ao lançar duas moedas simultaneamente, a probabilidade de obter duas caras é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/2",
        "1/3",
        "1/4",
        "2/3",
        "3/4"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 156, area: "matematica", disciplina: "algebra",
      enunciado: "A soma dos termos de uma PA com 5 termos, sendo o primeiro termo 2 e a razão 3, é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "25",
        "30",
        "35",
        "40",
        "50"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 157, area: "matematica", disciplina: "geometria",
      enunciado: "O volume de um cubo de aresta 4 cm é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "16 cm³",
        "48 cm³",
        "64 cm³",
        "128 cm³",
        "256 cm³"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 158, area: "matematica", disciplina: "estatistica",
      enunciado: "Os números 5, 7, 9, 11 e 13 formam uma PA. A média aritmética desses números é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "7",
        "8",
        "9",
        "10",
        "11"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 159, area: "matematica", disciplina: "probabilidade",
      enunciado: "Em um urna com 5 bolas numeradas de 1 a 5, qual é a probabilidade de sortear um número par?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/5",
        "2/5",
        "3/5",
        "4/5",
        "1/2"
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 160, area: "matematica", disciplina: "algebra",
      enunciado: "Se f(x) = x² - 4x + 3, qual é o valor de x para o qual f(x) = 0?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "x = 1 ou x = 3",
        "x = 1 ou x = -3",
        "x = -1 ou x = 3",
        "x = 2 ou x = 4",
        "x = 0 ou x = 3"
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 161, area: "matematica", disciplina: "geometria",
      enunciado: "A área de um círculo de raio 7 cm é (use π = 3,14):",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "153,86 cm²",
        "43,96 cm²",
        "21,98 cm²",
        "307,72 cm²",
        "154 cm²"
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 162, area: "matematica", disciplina: "estatistica",
      enunciado: "Em um conjunto de dados, a mediana é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O valor que mais se repete.",
        "O valor que divide o conjunto em duas partes iguais.",
        "A soma de todos os valores dividida pelo número de valores.",
        "O maior valor do conjunto.",
        "O menor valor do conjunto."
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 163, area: "matematica", disciplina: "probabilidade",
      enunciado: "Ao lançar um dado de 6 faces, a probabilidade de obter um número par é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/6",
        "1/3",
        "1/2",
        "2/3",
        "5/6"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 164, area: "matematica", disciplina: "algebra",
      enunciado: "A soma dos n primeiros termos de uma PA é dada por Sn = n(a₁ + an)/2. Qual é a soma dos 10 primeiros termos de uma PA com a₁ = 2 e a₁₀ = 20?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "110",
        "100",
        "90",
        "120",
        "80"
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 165, area: "matematica", disciplina: "geometria",
      enunciado: "Em um triângulo equilátero de lado 6 cm, a altura mede:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "3√3 cm.",
        "6 cm.",
        "3 cm.",
        "6√3 cm.",
        "9 cm."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 166, area: "matematica", disciplina: "algebra",
      enunciado: "Se 5^x = 125, o valor de x é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "2",
        "3",
        "4",
        "5",
        "6"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 167, area: "matematica", disciplina: "estatistica",
      enunciado: "O desvio padrão é uma medida que indica:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "A dispersão dos dados em relação à média.",
        "O valor mais frequente.",
        "O centro do conjunto de dados.",
        "A soma dos valores.",
        "A relação entre dois conjuntos."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 168, area: "matematica", disciplina: "probabilidade",
      enunciado: "Em um baralho com 52 cartas, qual é a probabilidade de sortear um Ás?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/13",
        "1/52",
        "4/13",
        "1/4",
        "1/2"
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 169, area: "matematica", disciplina: "geometria",
      enunciado: "O perímetro de um retângulo de lados 8 cm e 5 cm é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "13 cm",
        "26 cm",
        "40 cm",
        "60 cm",
        "80 cm"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 170, area: "matematica", disciplina: "algebra",
      enunciado: "A equação x² - 5x + 6 = 0 possui como raízes:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "x = 2 e x = 3.",
        "x = 1 e x = 6.",
        "x = -2 e x = -3.",
        "x = 2 e x = -3.",
        "x = 5 e x = 6."
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 171, area: "matematica", disciplina: "geometria",
      enunciado: "O ângulo interno de um triângulo equilátero mede:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "45°",
        "60°",
        "90°",
        "120°",
        "180°"
      ],
      gabarito: "B",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 172, area: "matematica", disciplina: "estatistica",
      enunciado: "Em uma pesquisa com 200 pessoas, 80 preferem música pop. A porcentagem de pessoas que preferem música pop é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "25%",
        "30%",
        "40%",
        "50%",
        "60%"
      ],
      gabarito: "C",
      dificuldade: 1,
      triDisc: 0.85, triAcertoAcaso: 0.2
    },
    {
      id: 173, area: "matematica", disciplina: "probabilidade",
      enunciado: "Ao lançar duas moedas, a probabilidade de obter pelo menos uma cara é:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/4",
        "1/2",
        "3/4",
        "1/3",
        "2/3"
      ],
      gabarito: "C",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 174, area: "matematica", disciplina: "algebra",
      enunciado: "Se f(x) = 2x + 3, qual é o valor de f⁻¹(7)?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "2",
        "3",
        "4",
        "5",
        "7"
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.65, triAcertoAcaso: 0.2
    },
    {
      id: 175, area: "matematica", disciplina: "geometria",
      enunciado: "O volume de um cone de raio da base 3 cm e altura 10 cm é (use π = 3):",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "30 cm³",
        "90 cm³",
        "270 cm³",
        "300 cm³",
        "900 cm³"
      ],
      gabarito: "B",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 176, area: "matematica", disciplina: "estatistica",
      enunciado: "A amplitude de um conjunto de dados é a diferença entre:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "O maior e o menor valor.",
        "A média e a mediana.",
        "O primeiro e o último valor.",
        "Dois valores quaisquer.",
        "A moda e a média."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 177, area: "matematica", disciplina: "probabilidade",
      enunciado: "Em um saco com 3 bolas vermelhas, 2 azuis e 1 verde, qual é a probabilidade de sortear uma bola que não seja verde?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "1/6",
        "1/3",
        "2/3",
        "5/6",
        "1/2"
      ],
      gabarito: "D",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 178, area: "matematica", disciplina: "algebra",
      enunciado: "A soma dos ângulos internos de um polígono de n lados é dada por:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "(n - 2) × 180°",
        "n × 180°",
        "(n + 2) × 180°",
        "n × 360°",
        "(n - 1) × 180°"
      ],
      gabarito: "A",
      dificuldade: 2,
      triDisc: 0.7, triAcertoAcaso: 0.2
    },
    {
      id: 179, area: "matematica", disciplina: "geometria",
      enunciado: "A diagonal de um quadrado de lado 5 cm mede:",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "5√2 cm.",
        "10 cm.",
        "5 cm.",
        "25 cm.",
        "50 cm."
      ],
      gabarito: "A",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    },
    {
      id: 180, area: "matematica", disciplina: "estatistica",
      enunciado: "Em um gráfico de pizza que representa a preferência de 300 pessoas, 45% preferem azul, 30% vermelho e 25% verde. Quantas pessoas preferem azul?",
      alternativas: ["A", "B", "C", "D", "E"],
      opcoes: [
        "75",
        "90",
        "100",
        "135",
        "150"
      ],
      gabarito: "D",
      dificuldade: 1,
      triDisc: 0.8, triAcertoAcaso: 0.2
    }
  ]
};

// Mapeamento de disciplinas por área
const DISCIPLINAS = {
  linguagens: ["portugues", "ingles", "espanhol", "artes", "literatura", "educacao_fisica", "tic"],
  humanas: ["historia", "geografia", "sociologia", "filosofia"],
  natureza: ["fisica", "quimica", "biologia"],
  matematica: ["algebra", "geometria", "estatistica", "probabilidade"]
};

const AREA_NAMES = {
  linguagens: "Linguagens, Códigos e suas Tecnologias",
  humanas: "Ciências Humanas e suas Tecnologias",
  natureza: "Ciências da Natureza e suas Tecnologias",
  matematica: "Matemática e suas Tecnologias"
};

const DISCIPLINA_NAMES = {
  portugues: "Língua Portuguesa",
  ingles: "Língua Inglesa",
  espanhol: "Língua Espanhola",
  artes: "Artes",
  literatura: "Literatura",
  educacao_fisica: "Educação Física",
  tic: "Tecnologias da Informação e Comunicação",
  historia: "História",
  geografia: "Geografia",
  sociologia: "Sociologia",
  filosofia: "Filosofia",
  fisica: "Física",
  quimica: "Química",
  biologia: "Biologia",
  algebra: "Álgebra",
  geometria: "Geometria",
  estatistica: "Estatística",
  probabilidade: "Probabilidade"
};
