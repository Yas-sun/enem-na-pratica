const TRI = {
  calculateScore(questions, answers) {
    if (!questions || questions.length === 0) return 0;

    let score = 0;
    let totalWeight = 0;

    questions.forEach((q, i) => {
      const userAnswer = answers[q.id];
      const isCorrect = userAnswer === q.gabarito;
      const difficulty = q.dificuldade || 1;
      const disc = q.triDisc || 0.7;
      const acertoAcaso = q.triAcertoAcaso || 0.2;

      let weight;
      if (difficulty === 1) weight = 1.0;
      else if (difficulty === 2) weight = 1.5;
      else weight = 2.0;

      totalWeight += weight;

      if (isCorrect) {
        const coherenceBonus = disc * (1 - acertoAcaso);
        score += weight * coherenceBonus;
      } else if (userAnswer) {
        score -= weight * 0.05;
      }
    });

    if (totalWeight === 0) return 0;

    const normalizedScore = (score / totalWeight) * 1000;
    return Math.max(0, Math.min(1000, Math.round(normalizedScore)));
  },

  calculateAreaScore(area, questions, answers) {
    const areaQuestions = questions.filter(q => q.area === area);
    return this.calculateScore(areaQuestions, answers);
  },

  calculateAllScores(questions, answers) {
    const areas = ['linguagens', 'humanas', 'natureza', 'matematica'];
    const scores = {};

    areas.forEach(area => {
      scores[area] = this.calculateAreaScore(area, questions, answers);
    });

    scores.media = Math.round(
      Object.values(scores).reduce((a, b) => a + b, 0) / areas.length
    );

    return scores;
  },

  getAccuracy(questions, answers) {
    if (!questions || questions.length === 0) return { correct: 0, total: 0, percentage: 0 };

    let correct = 0;
    let answered = 0;

    questions.forEach(q => {
      if (answers[q.id]) {
        answered++;
        if (answers[q.id] === q.gabarito) correct++;
      }
    });

    return {
      correct,
      total: questions.length,
      answered,
      percentage: questions.length > 0 ? Math.round((correct / questions.length) * 100) : 0
    };
  },

  getAreaAccuracy(area, questions, answers) {
    const areaQuestions = questions.filter(q => q.area === area);
    return this.getAccuracy(areaQuestions, answers);
  },

  analyzePattern(questions, answers) {
    let easyCorrect = 0, easyTotal = 0;
    let mediumCorrect = 0, mediumTotal = 0;
    let hardCorrect = 0, hardTotal = 0;

    questions.forEach(q => {
      const userAnswer = answers[q.id];
      const isCorrect = userAnswer === q.gabarito;

      if (q.dificuldade === 1) {
        easyTotal++;
        if (isCorrect) easyCorrect++;
      } else if (q.dificuldade === 2) {
        mediumTotal++;
        if (isCorrect) mediumCorrect++;
      } else {
        hardTotal++;
        if (isCorrect) hardCorrect++;
      }
    });

    return {
      easy: { correct: easyCorrect, total: easyTotal },
      medium: { correct: mediumCorrect, total: mediumTotal },
      hard: { correct: hardCorrect, total: hardTotal }
    };
  },

  getDifficultyLabel(dificuldade) {
    const labels = { 1: 'Fácil', 2: 'Médio', 3: 'Difícil' };
    return labels[dificuldade] || 'Médio';
  },

  getDifficultyBadgeClass(dificuldade) {
    const classes = { 1: 'badge-easy', 2: 'badge-medium', 3: 'badge-hard' };
    return classes[dificuldade] || 'badge-medium';
  }
};
