// Gemeinsame Helfer fuer alle Motion-Graphics-Szenen (mg/<projekt>/scene.html laedt ../lib/core.js).
// Vertrag der Szene: window.setTimeline(tl), window.draw(t), window.sfxEvents(), optional window.ready.
(function () {
  const M = {};
  M.cl = (t, a, b) => Math.max(0, Math.min(1, (t - a) / (b - a)));
  M.ez = t => t <= 0 ? 0 : t >= 1 ? 1 : 1 - Math.pow(1 - t, 3);            // ease-out
  M.ei = t => t <= 0 ? 0 : t >= 1 ? 1 : t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; // ease-in-out
  M.bo = t => { t = Math.max(0, Math.min(1, t)); const c = 1.9; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2) }; // overshoot
  M.el = t => { t = Math.max(0, Math.min(1, t)); if (t == 0 || t == 1) return t; return Math.pow(2, -10 * t) * Math.sin((t * 10 - .75) * 2.0944) + 1 }; // elastic
  M.lerp = (a, b, t) => a + (b - a) * t;
  M.$ = id => document.getElementById(id);
  M.NS = 'http://www.w3.org/2000/svg';
  M.TL = null;
  M.L = i => M.TL ? M.TL.lines[(i + M.TL.lines.length) % M.TL.lines.length] : { start: i * 3, end: i * 3 + 2.5, words: [], text: '' };
  M.cur = t => { if (!M.TL) return 0; let k = 0; M.TL.lines.forEach((l, i) => { if (t >= l.start - .25) k = i }); return k };
  // Zahl hochzaehlen (fuer Zaehler-Animationen)
  M.fmt = (v, d = 0, pre = '', suf = '') => pre + Number(v).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }) + suf;
  // Deterministisches Rauschen
  M.rnd = s => { const x = Math.sin(s * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x) };

  // ---- Untertitel mit Wort-Hervorhebung (Karaoke) ----
  // opts: {y, w, size, maxWords, color, hl, bg, x, upper}
  M.captions = function (t, o = {}) {
    if (!M.TL) return '';
    const W = o.w || 960, X = o.x == null ? (o.stageW || 1080) / 2 : o.x, Y = o.y || 1450, S = o.size || 64, MW = o.maxWords || 4;
    for (const l of M.TL.lines) {
      if (t < l.start - .05 || t > l.end + .35) continue;
      const ws = (l.words && l.words.length) ? l.words : l.text.split(' ').map((w, i, a) => [w, i * (l.end - l.start) / a.length, (i + 1) * (l.end - l.start) / a.length]);
      const rt = t - l.start;
      // Woerter in Gruppen von MW teilen, Gruppe des aktuellen Worts zeigen
      let gi = 0; ws.forEach((w, i) => { if (rt >= w[1] - .02) gi = Math.floor(i / MW) });
      const grp = ws.slice(gi * MW, gi * MW + MW), g0 = grp[0][1];
      const pin = M.ez(M.cl(rt, g0 - .05, g0 + .12)), out = 1 - M.ez(M.cl(t, l.end + .15, l.end + .35));
      let h = '';
      grp.forEach((w, j) => {
        const nx = j + 1 < grp.length ? grp[j + 1][1] : w[2] + .3, on = rt >= w[1] - .02, act = on && rt < nx - .02, pop = act ? M.bo(M.cl(rt, w[1] - .02, w[1] + .14)) : 1;
        const txt = (o.upper ? w[0].toUpperCase() : w[0]).replace(/</g, '&lt;');
        h += `<span style="display:inline-block;margin:0 .14em;transform:scale(${act ? .9 + .14 * pop : 1});color:${act ? (o.hl || '#ffd166') : (o.color || '#ffffff')};opacity:${on ? 1 : .55}">${txt}</span>`;
      });
      return `<div style="position:absolute;left:${X - W / 2}px;width:${W}px;top:${Y}px;text-align:center;font:900 ${S}px/1.15 'Arial Black',Arial,Helvetica,sans-serif;letter-spacing:-.5px;text-shadow:${M.outline(Math.max(3, Math.round(S / 14)))},0 ${S / 10}px ${S / 4}px #000c;opacity:${pin * out};transform:translateY(${(1 - pin) * 20}px) scale(${.92 + .08 * pin})">${h}</div>`;
    }
    return '';
  };

  M.outline = r => { const a = []; for (let k = 0; k < 16; k++) { const q = k / 16 * 6.2832; a.push(`${(Math.cos(q) * r).toFixed(1)}px ${(Math.sin(q) * r).toFixed(1)}px 0 #000`) } return a.join(',') };
  // ---- Filmkorn + Vignette (einmal einfuegen, pro Frame M.grainTick(t)) ----
  M.finish = function (stage, w, h, grain = .08, vig = '#000a', vigStart = 50) {
    const v = document.createElement('div');
    v.style.cssText = `position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent ${vigStart}%,${vig} 100%);z-index:90`;
    stage.appendChild(v);
    const g = document.createElementNS(M.NS, 'svg');
    g.setAttribute('width', w + 80); g.setAttribute('height', h + 80);
    g.style.cssText = `position:absolute;left:-40px;top:-40px;opacity:${grain};mix-blend-mode:overlay;pointer-events:none;z-index:91`;
    g.innerHTML = `<filter id=mgnz><feTurbulence id=mgtb type=fractalNoise baseFrequency=".9" numOctaves=2 seed=1 /></filter><rect width=100% height=100% filter="url(#mgnz)"/>`;
    stage.appendChild(g);
  };
  M.grainTick = t => { const e = document.getElementById('mgtb'); if (e) e.setAttribute('seed', 1 + Math.floor(t * 30) % 40) };

  // ---- Bild vorladen (fuer Szenen mit Gemini-Bildern) ----
  M.preload = function (srcs) {
    window.ready = false; let n = srcs.length; if (!n) { window.ready = true; return }
    srcs.forEach(s => { const i = new Image(); i.onload = i.onerror = () => { if (--n == 0) window.ready = true }; i.src = s });
  };
  window.MG = M;
})();
