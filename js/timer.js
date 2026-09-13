const Timer = {
  interval: null,
  startTime: null,
  elapsed: 0,
  duration: 0,
  isPaused: false,
  onComplete: null,
  onTick: null,

  start(durationMinutes, onTick, onComplete) {
    this.stop();
    this.duration = durationMinutes * 60;
    this.elapsed = 0;
    this.startTime = Date.now();
    this.isPaused = false;
    this.onTick = onTick;
    this.onComplete = onComplete;

    this._tick();
    this.interval = setInterval(() => this._tick(), 1000);
  },

  _tick() {
    if (this.isPaused) return;

    this.elapsed = Math.floor((Date.now() - this.startTime) / 1000);
    const remaining = Math.max(0, this.duration - this.elapsed);

    if (this.onTick) {
      this.onTick(this.formatTime(remaining), remaining, this.duration);
    }

    if (remaining <= 0) {
      this.stop();
      if (this.onComplete) this.onComplete();
    }
  },

  pause() {
    this.isPaused = true;
    this._pauseTime = Date.now();
  },

  resume() {
    if (!this.isPaused) return;
    const pauseDuration = Date.now() - this._pauseTime;
    this.startTime += pauseDuration;
    this.isPaused = false;
  },

  toggle() {
    if (this.isPaused) this.resume();
    else this.pause();
  },

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
    this.isPaused = false;
  },

  getElapsed() {
    return this.elapsed;
  },

  getRemaining() {
    return Math.max(0, this.duration - this.elapsed);
  },

  formatTime(seconds) {
    if (seconds === undefined) seconds = this.getRemaining();
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;

    if (h > 0) {
      return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  },

  getTimerClass(remaining, total) {
    const percentage = (remaining / total) * 100;
    if (percentage <= 10) return 'danger';
    if (percentage <= 25) return 'warning';
    return '';
  }
};
