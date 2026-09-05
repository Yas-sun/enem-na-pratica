// Gera js/dados.js com todo o banco de questoes embutido (funciona sem servidor, file://)
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const all = [];
for (let y = 2009; y <= 2025; y++) {
  const p = path.join(ROOT, 'data', y + '.json');
  const q = JSON.parse(fs.readFileSync(p, 'utf8'));
  all.push(...q);
}

const out = '/* Gerado por tools/build_bundle.js — nao editar manualmente. */\n' +
  'window.BANCO_QUESTIONS = ' + JSON.stringify(all) + ';\n';
fs.writeFileSync(path.join(ROOT, 'js', 'dados.js'), out, 'utf8');
console.log('questoes no bundle:', all.length);
console.log('tamanho (MB):', (Buffer.byteLength(out) / 1e6).toFixed(1));