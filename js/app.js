const App = {
  allQuestions: [],
  currentQuestions: [],
  currentAnswers: {},
  mode: null,
  sessionConfig: null,
  questionFrequency: {},

  async init() {
    this.loadTheme();
    this.loadFrequency();
    const page = this.getPage();
    if (page === 'index') await this.initIndex();
    else if (page === 'questoes') await this.initQuestoes();
    else if (page === 'simulado') await this.initSimulado();
    else if (page === 'resultado') this.initResultado();
  },

  getPage() {
    const p = window.location.pathname;
    if (p.includes('questoes')) return 'questoes';
    if (p.includes('simulado')) return 'simulado';
    if (p.includes('resultado')) return 'resultado';
    return 'index';
  },

  // ===== JSON LOADER =====
  async loadAllQuestions() {
    if (this.allQuestions.length > 0) return this.allQuestions;
    // Modo offline: banco embutido em js/dados.js (funciona sem servidor, via file://)
    if (typeof window !== 'undefined' && window.BANCO_QUESTIONS) {
      this.allQuestions = window.BANCO_QUESTIONS;
      return this.allQuestions;
    }
    const years = [];
    for (let y = 2009; y <= 2025; y++) years.push(y);

    const results = await Promise.all(
      years.map(y =>
        fetch(`data/${y}.json`).then(r => r.ok ? r.json() : []).catch(() => [])
      )
    );
    this.allQuestions = results.flat();

    // Deduplicate by id
    const seen = new Set();
    this.allQuestions = this.allQuestions.filter(q => {
      if (seen.has(q.id)) return false;
      seen.add(q.id);
      return true;
    });

    return this.allQuestions;
  },

  // ===== SMART RANDOMIZATION =====
  loadFrequency() {
    try { this.questionFrequency = JSON.parse(localStorage.getItem('enem_freq') || '{}'); }
    catch { this.questionFrequency = {}; }
  },

  saveFrequency() {
    try { localStorage.setItem('enem_freq', JSON.stringify(this.questionFrequency)); } catch {}
  },

  recordUsage(ids) {
    ids.forEach(id => { this.questionFrequency[id] = (this.questionFrequency[id] || 0) + 1; });
    this.saveFrequency();
  },

  smartShuffle(questions, count) {
    const scored = questions.map(q => {
      const freq = this.questionFrequency[q.id] || 0;
      const r = Math.random() * 0.4;
      return { question: q, score: freq * 0.6 + r };
    });
    scored.sort((a, b) => a.score - b.score);
    return scored.slice(0, count).map(s => s.question);
  },

  // ===== THEME =====
  loadTheme() {
    const s = Storage.getSettings();
    if (s.theme === 'light') document.body.classList.add('light');
    this.updateThemeIcon();
  },

  toggleTheme() {
    document.body.classList.toggle('light');
    const s = Storage.getSettings();
    s.theme = document.body.classList.contains('light') ? 'light' : 'dark';
    Storage.saveSettings(s);
    this.updateThemeIcon();
  },

  updateThemeIcon() {
    const b = document.getElementById('theme-toggle');
    if (b) b.textContent = document.body.classList.contains('light') ? '🌙' : '☀';
  },

  // ===== CHIP TOGGLE =====
  toggleChip(el) {
    el.classList.toggle('selected');
    // If it's an area chip, update disciplinas
    if (el.dataset.area) {
      this.updateDisciplinas();
    } else if (el.dataset.disc) {
      this.updateSubtopicos();
    }
  },

  esc(str) {
    if (str === null || str === undefined) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  },

  renderImagemHtml(imagem) {
    if (!imagem) return '';
    const list = Array.isArray(imagem) ? imagem : [imagem];
    return list.map(img => {
      if (/^https?:\/\//i.test(img) || /^data:image/i.test(img)) {
        return `<div class="question-image"><img src="${this.esc(img)}" alt="Imagem da questão" onerror="this.closest('.question-image').style.display='none';"></div>`;
      }
      if (/^\[Imagem:/i.test(img)) {
        return `<div class="question-image question-image-placeholder"><span>${this.esc(img)}</span></div>`;
      }
      return `<div class="question-image"><img src="${this.esc(img)}" alt="Imagem da questão" onerror="this.closest('.question-image').style.display='none';"></div>`;
    }).join('');
  },

  // ===== INDEX =====
  async initIndex() {
    await this.loadAllQuestions();
    this.renderHistory();
    this.renderIndexStats();
    this.renderBankStats();
  },

  renderBankStats() {
    const qs = this.allQuestions;
    const editions = new Set(qs.map(q => q.ano)).size;
    const areas = new Set(qs.map(q => q.area)).size;
    const images = qs.filter(q => q.imagem).length;
    const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
    set('stat-editions', editions);
    set('stat-areas', areas);
    set('stat-questions', qs.length);
    set('stat-images', images);
  },

  renderIndexStats() {
    const history = Storage.getHistory();
    const el = document.getElementById('index-stats');
    if (!el || history.length === 0) return;
    const totalQ = history.reduce((s, h) => s + (h.accuracy?.total || 0), 0);
    const totalC = history.reduce((s, h) => s + (h.accuracy?.correct || 0), 0);
    const avg = history.length > 0 ? Math.round(history.reduce((s, h) => s + (h.scores?.media || 0), 0) / history.length) : 0;
    el.innerHTML = `
      <div class="score-item blue"><div class="score-value">${history.length}</div><div class="score-label">Sessões</div></div>
      <div class="score-item green"><div class="score-value">${totalQ}</div><div class="score-label">Questões</div></div>
      <div class="score-item purple"><div class="score-value">${totalC}</div><div class="score-label">Acertos</div></div>
      <div class="score-item yellow"><div class="score-value">${avg}</div><div class="score-label">Média TRI</div></div>
    `;
    el.classList.remove('hidden');
  },

  renderHistory() {
    const history = Storage.getHistory();
    const el = document.getElementById('history-list');
    if (!el) return;
    if (history.length === 0) {
      el.innerHTML = '<p class="text-muted text-sm text-center" style="padding:2rem;">Nenhum registro ainda.</p>';
      return;
    }
    el.innerHTML = history.slice(0, 10).map((h, i) => {
      const d = new Date(h.date);
      const date = d.toLocaleDateString('pt-BR');
      const time = d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
      const type = h.type === 'simulado' ? 'Simulado' : 'Questões';
      const pct = h.accuracy?.percentage || 0;
      return `
        <div class="history-item" onclick="App.showHistoryDetail(${i})">
          <div class="history-header">
            <div class="flex items-center gap-2">
              <span class="badge badge-default">${type}</span>
              <span class="text-sm" style="font-weight:500;">${date} ${time}</span>
            </div>
            <span class="badge ${pct>=70?'badge-success':pct>=40?'badge-warning':'badge-destructive'}">${pct}%</span>
          </div>
          <div class="history-scores">
            <span class="history-score"><strong>${h.accuracy?.correct||0}</strong>/${h.accuracy?.total||0} acertos</span>
            <span class="history-score">TRI: <strong>${h.scores?.media||0}</strong></span>
          </div>
        </div>`;
    }).join('');
  },

  showHistoryDetail(i) {
    const h = Storage.getHistory()[i];
    if (!h) return;
    const modal = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');
    let areaHtml = '';
    if (h.type === 'simulado' && h.scores) {
      const areas = ['linguagens','humanas','natureza','matematica'];
      areaHtml = `<div class="separator"></div><h3 class="text-sm" style="font-weight:600;margin-bottom:0.75rem;">Notas por Área</h3>
        <div style="display:flex;flex-direction:column;gap:0.5rem;">
        ${areas.map(a=>`<div class="chart-bar"><span class="chart-label">${(AREA_NAMES[a]||a).split(' e ')[0]}</span><div class="chart-track"><div class="chart-fill" style="width:${(h.scores[a]||0)/10}%;background:var(--info);"></div></div><span class="chart-value">${h.scores[a]||0}</span></div>`).join('')}
        </div>`;
    }
    content.innerHTML = `<h2>Detalhes da Sessão</h2>
      <div class="text-sm text-muted mb-3">${new Date(h.date).toLocaleDateString('pt-BR')} às ${new Date(h.date).toLocaleTimeString('pt-BR')}</div>
      <div class="score-grid mb-3">
        <div class="score-item purple"><div class="score-value">${h.scores?.media||0}</div><div class="score-label">TRI</div></div>
        <div class="score-item green"><div class="score-value">${h.accuracy?.correct||0}</div><div class="score-label">Acertos</div></div>
        <div class="score-item red"><div class="score-value">${(h.accuracy?.total||0)-(h.accuracy?.correct||0)}</div><div class="score-label">Erros</div></div>
        <div class="score-item blue"><div class="score-value">${h.accuracy?.percentage||0}%</div><div class="score-label">%</div></div>
      </div>${areaHtml}
      <div class="separator"></div>
      <div class="modal-actions"><button class="btn btn-outline btn-sm" onclick="document.getElementById('modal-overlay').classList.remove('active')">Fechar</button></div>`;
    modal.classList.add('active');
  },

  // ===== QUESTÕES =====
  async initQuestoes() {
    await this.loadAllQuestions();
    document.getElementById('btn-start').addEventListener('click', () => this.startPractice());
    this.updateDisciplinas();
  },

  getSelectedAreas() {
    return Array.from(document.querySelectorAll('#area-chips .form-chip.selected')).map(c => c.dataset.area);
  },

  updateDisciplinas() {
    const areas = this.getSelectedAreas();
    const container = document.getElementById('disciplina-chips');
    if (!container) return;

    // Preserve current selections
    const prevSelected = new Set(
      Array.from(container.querySelectorAll('.form-chip.selected')).map(c => c.dataset.disc)
    );

    let discList = [];
    if (areas.length === 0) {
      discList = Object.entries(DISCIPLINAS).flatMap(([a, ds]) =>
        ds.map(d => ({ area: a, id: d, name: DISCIPLINA_NAMES[d] }))
      );
    } else {
      discList = areas.flatMap(a =>
        (DISCIPLINAS[a] || []).map(d => ({ area: a, id: d, name: DISCIPLINA_NAMES[d] }))
      );
    }

    container.innerHTML = discList.map(d => {
      const wasSelected = prevSelected.has(d.id) ? ' selected' : '';
      return `<div class="form-chip${wasSelected}" data-disc="${d.id}" onclick="App.toggleChip(this)"><span>${d.name}</span></div>`;
    }).join('');

    this.updateSubtopicos();
  },

  getSelectedDisciplinas() {
    return Array.from(document.querySelectorAll('#disciplina-chips .form-chip.selected')).map(c => c.dataset.disc);
  },

  getSelectedSubtopicos() {
    return Array.from(document.querySelectorAll('#subtopico-chips .form-chip.selected')).map(c => c.dataset.sub);
  },

  updateSubtopicos() {
    const container = document.getElementById('subtopico-chips');
    if (!container) return;

    const areas = this.getSelectedAreas();
    const disciplinas = this.getSelectedDisciplinas();

    const prevSelected = new Set(
      Array.from(container.querySelectorAll('.form-chip.selected')).map(c => c.dataset.sub)
    );

    let pool = this.allQuestions;
    if (areas.length > 0) pool = pool.filter(q => areas.includes(q.area));
    if (disciplinas.length > 0) pool = pool.filter(q => disciplinas.includes(q.disciplina));

    const subs = [...new Set(pool.map(q => q.subtopico).filter(Boolean))].sort((a, b) => a.localeCompare(b, 'pt-BR'));

    if (subs.length === 0 || (areas.length === 0 && disciplinas.length === 0)) {
      container.innerHTML = '<p class="form-hint">Selecione uma área ou disciplina para ver as sub-matérias (ex.: Álgebra → Função de 2º grau).</p>';
      return;
    }

    container.innerHTML = subs.map(s => {
      const wasSelected = prevSelected.has(s) ? ' selected' : '';
      return `<div class="form-chip${wasSelected}" data-sub="${s}" onclick="App.toggleChip(this)"><span>${this.esc(s)}</span></div>`;
    }).join('');
  },

  async startPractice() {
    const areas = this.getSelectedAreas();
    const disciplinas = this.getSelectedDisciplinas();
    const subtopicos = this.getSelectedSubtopicos();
    let num = parseInt(document.getElementById('num-questions').value) || 10;
    num = Math.max(1, Math.min(180, num));

    let pool = [...this.allQuestions];
    if (areas.length > 0) pool = pool.filter(q => areas.includes(q.area));
    if (disciplinas.length > 0) pool = pool.filter(q => disciplinas.includes(q.disciplina));
    if (subtopicos.length > 0) pool = pool.filter(q => subtopicos.includes(q.subtopico));

    if (pool.length === 0) {
      this.showToast('Nenhuma questão encontrada com esses filtros.');
      return;
    }

    this.currentQuestions = this.smartShuffle(pool, num);
    this.currentAnswers = {};
    this.mode = 'questoes';
    this.sessionConfig = { areas, disciplinas, subtopicos, num };
    this.recordUsage(this.currentQuestions.map(q => q.id));

    document.getElementById('setup-screen').classList.add('hidden');
    document.getElementById('questions-screen').classList.remove('hidden');
    this.renderScrollQuestions();
    this.startTimerIfEnabled();
  },

  // ===== SIMULADO =====
  async initSimulado() {
    await this.loadAllQuestions();
    document.getElementById('btn-start').addEventListener('click', () => this.startSimulado());
    document.querySelectorAll('.simulado-type-card').forEach(card => {
      card.addEventListener('click', () => {
        document.querySelectorAll('.simulado-type-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        document.getElementById('simulado-type').value = card.dataset.type;
      });
    });
  },

  async startSimulado() {
    const type = document.getElementById('simulado-type').value;
    const cap = { completo: 180, dia1: 90, dia2: 90 }[type] || 180;
    let pool = [];
    if (type === 'dia1') pool = this.allQuestions.filter(q => q.area === 'linguagens' || q.area === 'humanas');
    else if (type === 'dia2') pool = this.allQuestions.filter(q => q.area === 'natureza' || q.area === 'matematica');
    else pool = [...this.allQuestions];

    this.currentQuestions = this.smartShuffle(pool, Math.min(cap, pool.length));
    this.currentAnswers = {};
    this.mode = 'simulado';
    this.sessionConfig = { type };
    this.recordUsage(this.currentQuestions.map(q => q.id));

    document.getElementById('setup-screen').classList.add('hidden');
    document.getElementById('questions-screen').classList.remove('hidden');
    this.renderScrollQuestions();
    this.startTimerIfEnabled();
  },

  // ===== TIMER =====
  startTimerIfEnabled() {
    const cb = document.getElementById('timer-enabled');
    if (cb && !cb.checked) return;
    const min = parseInt(document.getElementById('timer-minutes')?.value) || 30;
    const bar = document.getElementById('timer-bar');
    const disp = document.getElementById('timer-display');
    const pause = document.getElementById('timer-pause');
    if (!bar) return;
    bar.classList.remove('hidden');
    Timer.start(min, (fmt, rem, tot) => {
      disp.textContent = fmt;
      disp.className = 'timer-display ' + Timer.getTimerClass(rem, tot);
    }, () => { this.showToast('Tempo esgotado!'); this.finishSession(); });
    if (pause) pause.onclick = () => { Timer.toggle(); pause.textContent = Timer.isPaused ? '▶' : '⏸'; };
  },

  // ===== SCROLLABLE QUESTIONS =====
  renderScrollQuestions() {
    const container = document.getElementById('questions-list');
    if (!container) return;
    container.innerHTML = this.currentQuestions.map((q, i) => {
      const ctx = q.contexto || '';
      const txt = q.texto || q.enunciado || '';
      const pergunta = q.pergunta || '';
      const opcoes = q.opcoes || [];
      const fonte = q.fonte || (q.ano ? `ENEM ${q.ano}` : 'Questão própria');
      return `
        <div class="question-block" id="q-${i}" data-idx="${i}">
          <div class="question-block-header">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="badge badge-purple">${(AREA_NAMES[q.area]||q.area).split(' e ')[0]}</span>
              <span class="badge badge-info">${DISCIPLINA_NAMES[q.disciplina]||q.disciplina}</span>
              ${q.subtopico?`<span class="badge badge-warning">${this.esc(q.subtopico)}</span>`:''}
              <span class="badge ${q.dificuldade===1?'badge-success':q.dificuldade===2?'badge-warning':'badge-destructive'}">
                ${q.dificuldade===1?'Fácil':q.dificuldade===2?'Médio':'Difícil'}</span>
              <span class="badge badge-default fonte-badge" title="Origem da questão">${this.esc(fonte)}</span>
            </div>
            <span class="text-xs text-muted">${i+1}/${this.currentQuestions.length}</span>
          </div>
          <div class="question-block-body">
            ${ctx?`<div class="question-context">${this.esc(ctx)}</div>`:''}
            ${txt?`<div class="question-text">${this.esc(txt)}</div>`:''}
            ${this.renderImagemHtml(q.imagem)}
            ${q.referencia?`<div class="question-reference">${this.esc(q.referencia)}</div>`:''}
            ${pergunta?`<div class="question-prompt">${this.esc(pergunta)}</div>`:''}
            <div class="options-list">
              ${opcoes.map((opt, oi) => {
                const letter = String.fromCharCode(65+oi);
                return `<div class="option-item" data-q="${q.id}" data-letter="${letter}" onclick="App.selectOption('${q.id}','${letter}',this)">
                  <span class="option-letter">${letter}</span><span>${this.esc(opt)}</span></div>`;
              }).join('')}
            </div>
          </div>
        </div>`;
    }).join('');
    this.renderFloatingNav();
    this.updateProgress();
  },

  renderFloatingNav() {
    const nav = document.getElementById('floating-nav');
    if (!nav) return;
    nav.classList.remove('hidden');
    nav.innerHTML = `
      <button class="btn btn-ghost btn-icon btn-sm" onclick="App.goToQ(0)" title="Início">⟨⟨</button>
      <button class="btn btn-ghost btn-icon btn-sm" onclick="App.goPrev()" title="Anterior">⟨</button>
      <span class="text-xs text-muted font-mono" id="nav-counter">0/${this.currentQuestions.length}</span>
      <button class="btn btn-ghost btn-icon btn-sm" onclick="App.goNext()" title="Próxima">⟩</button>
      <button class="btn btn-ghost btn-icon btn-sm" onclick="App.goToQ(${this.currentQuestions.length-1})" title="Fim">⟩⟩</button>
      <div style="width:1px;height:20px;background:var(--border);margin:0 0.25rem;"></div>
      <button class="btn btn-primary btn-sm" onclick="App.finishSession()">Finalizar</button>`;
  },

  goToQ(idx) {
    const el = document.getElementById(`q-${idx}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  },

  goNext() {
    const c = this.getCurrentIdx();
    if (c < this.currentQuestions.length - 1) this.goToQ(c + 1);
  },

  goPrev() {
    const c = this.getCurrentIdx();
    if (c > 0) this.goToQ(c - 1);
  },

  getCurrentIdx() {
    const c = document.getElementById('nav-counter');
    return c ? parseInt(c.textContent.split('/')[0]) || 0 : 0;
  },

  selectOption(qid, letter, el) {
    this.currentAnswers[qid] = letter;
    const block = el.closest('.question-block');
    block.querySelectorAll('.option-item').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    this.updateProgress();
  },

  updateProgress() {
    const answered = this.currentQuestions.filter(q => this.currentAnswers[q.id]).length;
    const total = this.currentQuestions.length;
    const track = document.getElementById('progress-track');
    if (track) {
      track.innerHTML = this.currentQuestions.map(q =>
        `<div class="progress-pip ${this.currentAnswers[q.id]?'answered':''}"></div>`
      ).join('');
    }
    const c = document.getElementById('nav-counter');
    if (c) c.textContent = `${answered}/${total}`;
    const s = document.getElementById('answer-stats');
    if (s) s.textContent = `${answered} de ${total} respondidas`;
  },

  // ===== FINISH =====
  finishSession() {
    const unanswered = this.currentQuestions.filter(q => !this.currentAnswers[q.id]).length;
    if (unanswered > 0 && !confirm(`${unanswered} questão(ões) sem resposta. Finalizar?`)) return;
    Timer.stop();
    const scores = TRI.calculateAllScores(this.currentQuestions, this.currentAnswers);
    const accuracy = TRI.getAccuracy(this.currentQuestions, this.currentAnswers);
    const pattern = TRI.analyzePattern(this.currentQuestions, this.currentAnswers);
    const result = {
      type: this.mode, config: this.sessionConfig,
      questions: this.currentQuestions, answers: this.currentAnswers,
      scores, accuracy, pattern,
      totalQuestions: this.currentQuestions.length,
      timeElapsed: Timer.getElapsed()
    };
    Storage.saveLastResult(result);
    Storage.addToHistory(result);
    window.location.href = 'resultado.html';
  },

  // ===== RESULTADO =====
  initResultado() {
    const result = Storage.getLastResult();
    if (!result) {
      document.getElementById('result-content').innerHTML = `
        <div class="text-center" style="padding:3rem;">
          <h2 style="font-size:1.25rem;font-weight:600;">Nenhum resultado</h2>
          <p class="text-muted text-sm mt-1">Faça um simulado primeiro.</p>
          <a href="index.html" class="btn btn-primary mt-3">Início</a></div>`;
      return;
    }
    this._result = result;
    this.detailFilter = 'all';
    this.renderResult(result);
  },

  renderResult(r) {
    const { scores, accuracy, pattern, questions, answers, type } = r;
    document.getElementById('res-notation').textContent = scores.media || 0;
    document.getElementById('res-total').textContent = accuracy.total;
    document.getElementById('res-correct').textContent = accuracy.correct;
    document.getElementById('res-wrong').textContent = accuracy.total - accuracy.correct;
    document.getElementById('res-percentage').textContent = (accuracy.percentage||0) + '%';

    if (type === 'simulado') {
      const el = document.getElementById('area-scores');
      if (el) {
        el.innerHTML = ['linguagens','humanas','natureza','matematica'].map(a =>
          `<div class="score-item blue"><div class="score-value">${scores[a]||0}</div><div class="score-label">${(AREA_NAMES[a]||'').split(' e ')[0]}</div></div>`
        ).join('');
        el.classList.remove('hidden');
      }
    }

    if (pattern) {
      const pct = p => p.total > 0 ? Math.round((p.correct/p.total)*100) : 0;
      document.getElementById('difficulty-analysis').innerHTML = `
        <div class="score-item green"><div class="score-value">${pct(pattern.easy)}%</div><div class="score-label">Fáceis ${pattern.easy.correct}/${pattern.easy.total}</div></div>
        <div class="score-item yellow"><div class="score-value">${pct(pattern.medium)}%</div><div class="score-label">Médias ${pattern.medium.correct}/${pattern.medium.total}</div></div>
        <div class="score-item red"><div class="score-value">${pct(pattern.hard)}%</div><div class="score-label">Difíceis ${pattern.hard.correct}/${pattern.hard.total}</div></div>`;
    }

    document.getElementById('gabarito-grid').innerHTML = questions.map((q, i) => {
      const ua = answers[q.id];
      const ok = ua === q.gabarito;
      return `<div class="gabarito-pip${ua?(ok?' correct':' incorrect'):''}" title="Q${i+1}: ${ua||'-'} → ${q.gabarito}" onclick="App.showQuestionDetail(${i})" style="cursor:pointer;">${i+1}</div>`;
    }).join('');

    this.renderDetails();
  },

  filterDetails(filter) {
    this.detailFilter = filter;
    const btns = document.querySelectorAll('#detail-filters .btn');
    btns.forEach(b => b.classList.toggle('btn-primary', b.dataset.filter === filter));
    btns.forEach(b => b.classList.toggle('btn-secondary', b.dataset.filter !== filter));
    this.renderDetails();
  },

  renderDetails() {
    const r = this._result;
    if (!r) return;
    const { questions, answers } = r;
    const filter = this.detailFilter;
    const el = document.getElementById('question-details');
    if (!el) return;

    const items = questions.map((q, i) => {
      const ua = answers[q.id];
      const ok = ua === q.gabarito;
      if (filter === 'correct' && !ok) return null;
      if (filter === 'wrong' && (ok || !ua)) return null;
      const txt = (q.texto || q.enunciado || '').substring(0, 160);
      const fonte = q.fonte || (q.ano ? `ENEM ${q.ano}` : 'Questão própria');
      return `<div class="card mb-2" style="border-left:3px solid ${ok?'var(--success)':'var(--destructive)'};">
        <div class="card-content" style="padding:1rem 1.25rem;">
          <div class="flex justify-between items-center mb-2 flex-wrap gap-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-xs text-muted">Q${i+1}</span>
              <span class="badge badge-info">${DISCIPLINA_NAMES[q.disciplina]||q.disciplina}</span>
              ${q.subtopico?`<span class="badge badge-warning">${this.esc(q.subtopico)}</span>`:''}
              <span class="badge badge-default">${this.esc(fonte)}</span>
            </div>
            <span class="badge ${ok?'badge-success':'badge-destructive'}">${ok?'✓ Acertou':'✗ Errou'}</span>
          </div>
          <p class="text-sm text-muted mb-2" style="line-height:1.6;">${this.esc(txt)}${txt.length>=160?'...':''}</p>
          <div class="text-xs flex items-center justify-between flex-wrap gap-1">
            <div>
              <span class="text-muted">Sua:</span>
              <span style="color:${ok?'var(--success)':'var(--destructive)'};font-weight:600;"> ${ua||'—'}</span>
              ${!ok?`<span class="text-muted" style="margin-left:0.5rem;">Gab:</span> <span style="color:var(--success);font-weight:600;">${q.gabarito}</span>`:''}
            </div>
            <button class="btn btn-outline btn-sm" onclick="App.showQuestionDetail(${i})">Ver questão completa</button>
          </div>
        </div></div>`;
    }).filter(Boolean);

    el.innerHTML = items.length > 0
      ? items.join('')
      : '<p class="text-muted text-sm text-center" style="padding:2rem;">Nenhuma questão com esse filtro.</p>';
  },

  showQuestionDetail(i) {
    const r = this._result;
    if (!r || !r.questions[i]) return;
    const q = r.questions[i];
    const ua = r.answers[q.id];
    const ok = ua === q.gabarito;
    const fonte = q.fonte || (q.ano ? `ENEM ${q.ano}` : 'Questão própria');
    const ctx = q.contexto || '';
    const txt = q.texto || q.enunciado || '';
    const pergunta = q.pergunta || '';

    const opts = (q.opcoes || []).map((opt, oi) => {
      const letter = String.fromCharCode(65+oi);
      const isGab = letter === q.gabarito;
      const isUser = ua === letter && !isGab;
      let cls = 'detail-option';
      if (isGab) cls += ' correct-option';
      else if (isUser) cls += ' user-wrong';
      const tags = [];
      if (isGab) tags.push('Gabarito');
      if (ua === letter) tags.push('Sua resposta');
      return `<div class="${cls}">
        <span class="option-letter">${letter}</span>
        <div style="flex:1;">
          <div>${this.esc(opt)}</div>
          ${tags.length?`<div class="text-xs" style="margin-top:0.25rem;font-weight:600;color:${isGab?'var(--success)':'var(--destructive)'};">${tags.join(' · ')}</div>`:''}
        </div>
      </div>`;
    }).join('');

    const modal = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');
    content.innerHTML = `
      <div class="flex items-center justify-between mb-2 flex-wrap gap-1">
        <h2 style="font-size:1.1rem;font-weight:700;margin:0;">Questão ${i+1}</h2>
        <span class="badge ${ok?'badge-success':'badge-destructive'}">${ok?'✓ Acertou':'✗ Errou'}</span>
      </div>
      <div class="flex items-center gap-2 flex-wrap mb-3">
        <span class="badge badge-info">${DISCIPLINA_NAMES[q.disciplina]||q.disciplina}</span>
        ${q.subtopico?`<span class="badge badge-warning">${this.esc(q.subtopico)}</span>`:''}
        <span class="badge badge-default">${this.esc(fonte)}</span>
      </div>
      ${ctx?`<div class="question-context">${this.esc(ctx)}</div>`:''}
      ${txt?`<div class="question-text">${this.esc(txt)}</div>`:''}
      ${this.renderImagemHtml(q.imagem)}
      ${q.referencia?`<div class="question-reference">${this.esc(q.referencia)}</div>`:''}
      ${pergunta?`<div class="question-prompt">${this.esc(pergunta)}</div>`:''}
      <div class="detail-options">${opts}</div>
      <div class="separator" style="margin:1rem 0;"></div>
      <div class="text-xs text-muted">
        Sua resposta: <strong style="color:${ok?'var(--success)':'var(--destructive)'};">${ua||'—'}</strong>
        · Gabarito: <strong style="color:var(--success);">${q.gabarito}</strong>
      </div>
      <div class="modal-actions mt-3">
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('modal-overlay').classList.remove('active')">Fechar</button>
      </div>`;
    modal.classList.add('active');
  },

  showToast(msg) {
    const old = document.querySelector('.toast');
    if (old) old.remove();
    const t = document.createElement('div');
    t.className = 'toast';
    t.style.cssText = `position:fixed;bottom:5rem;left:50%;transform:translateX(-50%);background:var(--foreground);color:var(--background);padding:.625rem 1rem;border-radius:var(--radius);font-size:.85rem;font-weight:500;z-index:300;box-shadow:0 4px 16px rgba(0,0,0,.3);`;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
