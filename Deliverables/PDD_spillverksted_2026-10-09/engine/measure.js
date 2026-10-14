// Runs each generated game headless: errors, canvas present, reacts to input.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const LIB = { kaplay: 'http://127.0.0.1:8765/kaplay.js', phaser: 'http://127.0.0.1:8765/phaser.js' };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const out = [];
  for (const eng of ['kaplay', 'phaser']) for (const f of fs.readdirSync(path.join(__dirname, eng)).filter(x => /^\d-.*\.js$/.test(x)).sort()) {
    const code = fs.readFileSync(path.join(__dirname, eng, f), 'utf8');
    const p = await b.newPage({ viewport: { width: 640, height: 360 } });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errs.push(m.text().slice(0, 200)); });
    const html = `<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#14213d}</style><script src="${LIB[eng]}"></script></head><body><script>${code}\n</script></body></html>`;
    const tmp = path.join(__dirname, '_run.html'); fs.writeFileSync(tmp, html);
    await p.goto('file://' + tmp); await p.waitForTimeout(1500);
    const canvas = await p.locator('canvas').count();
    const a = await p.screenshot();
    await p.mouse.click(320, 180);
    for (const k of ['ArrowRight', 'ArrowRight', 'Space', 'ArrowLeft', 'ArrowUp', 'ArrowDown']) { await p.keyboard.down(k); await p.waitForTimeout(250); await p.keyboard.up(k); }
    for (let i = 0; i < 6; i++) await p.mouse.click(60 + i * 100, 80 + (i % 3) * 90);
    await p.waitForTimeout(600);
    const c = await p.screenshot({ path: path.join(__dirname, eng, f.replace('.js', '.png')) });
    out.push({ engine: eng, game: f, lines: code.split('\n').length, canvas, changed: !a.equals(c), errors: [...new Set(errs)] });
    await p.close();
  }
  await b.close();
  fs.writeFileSync(path.join(__dirname, 'result.json'), JSON.stringify(out, null, 2));
  for (const r of out) console.log(r.engine, r.game, r.lines, 'canvas', r.canvas, 'changed', r.changed, 'errors', r.errors.length ? r.errors.join(' | ').slice(0, 300) : 0);
})();
