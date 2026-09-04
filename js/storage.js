const Storage = {
  KEYS: {
    SETTINGS: 'enem_settings',
    LAST_RESULT: 'enem_last_result',
    HISTORY: 'enem_history',
    FREQUENCY: 'enem_freq'
  },

  get(key) {
    try { const d = localStorage.getItem(key); return d ? JSON.parse(d) : null; }
    catch { return null; }
  },

  set(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); }
    catch (e) { console.warn('Storage error:', e); }
  },

  remove(key) { localStorage.removeItem(key); },

  getSettings() {
    return this.get(this.KEYS.SETTINGS) || {
      timerEnabled: true, timerMinutes: 30,
      theme: 'dark', showExplanation: true
    };
  },

  saveSettings(s) { this.set(this.KEYS.SETTINGS, s); },

  getLastResult() { return this.get(this.KEYS.LAST_RESULT); },
  saveLastResult(r) { this.set(this.KEYS.LAST_RESULT, r); },

  getHistory() { return this.get(this.KEYS.HISTORY) || []; },

  addToHistory(result) {
    const h = this.getHistory();
    h.unshift({ ...result, date: new Date().toISOString() });
    if (h.length > 100) h.pop();
    this.set(this.KEYS.HISTORY, h);
  },

  getFrequency() { return this.get(this.KEYS.FREQUENCY) || {}; },
  saveFrequency(f) { this.set(this.KEYS.FREQUENCY, f); },

  clearAll() {
    Object.values(this.KEYS).forEach(k => this.remove(k));
  }
};
