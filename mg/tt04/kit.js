// Kleines Szenen-Kit fuer die Hidden-Price-Folgen (laedt nach ../lib/core.js).
// Alles deterministisch aus t berechnet.
(function () {
  const K = {}, M = window.MG;
  const F = "'Arial Black',Arial,Helvetica,sans-serif", FB = "Arial,Helvetica,sans-serif";
  K.F = F; K.FB = FB;
  const cl = M.cl, ez = M.ez, ei = M.ei, bo = M.bo;
  K.S = i => M.L(i).start; K.E = i => M.L(i).end;
  // absolute Zeit eines Wortes in Zeile i (erstes Wort, das mit w beginnt); Fallback: Anteil f der Zeile
  K.W = (i, w, f = .5) => {
    const l = M.L(i); const ws = l.words || [];
    for (const x of ws) if (x[0].toLowerCase().replace(/[^a-z0-9$]/g, '').startsWith(w)) return l.start + x[1];
    return l.start + (l.end - l.start) * f;
  };
  K.ph = (t, a, d = .6) => ez(cl(t, a, a + d));
  K.pb = (t, a, d = .6) => bo(cl(t, a, a + d));
  // Text (fett), o: {a,o,ls,st,sw,f,w}
  K.t = (x, y, s, sz, c, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.a || 'middle'}" font-family="${o.w ? FB : F}" font-weight="${o.w || 900}" font-size="${sz}" fill="${c}"${o.ls ? ` letter-spacing="${o.ls}"` : ''}${o.o != null ? ` opacity="${o.o}"` : ''}${o.f ? ` filter="${o.f}"` : ''}${o.st ? ` stroke="${o.st}" stroke-width="${o.sw || 10}" stroke-linejoin="round" paint-order="stroke"` : ''}>${s}</text>`;
  K.g = (tr, inner, o = 1) => o <= 0.001 ? '' : `<g transform="${tr}"${o < 1 ? ` opacity="${o.toFixed(3)}"` : ''}>${inner}</g>`;
  K.at = (x, y, s, inner, o = 1) => K.g(`translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${Math.max(0.0001, s).toFixed(4)})`, inner, o);
  // isometrischer Block: Vorderseite (x,y,w,h), Tiefe d nach rechts oben
  K.box = (x, y, w, h, d, c, c2, c3, extra = '') => {
    if (h <= 0.5) return '';
    const dy = d * .55;
    return `<g>${extra}<path d="M${x},${y} L${x + d},${y - dy} L${x + w + d},${y - dy} L${x + w},${y} Z" fill="${c2}"/>` +
      `<path d="M${x + w},${y} L${x + w + d},${y - dy} L${x + w + d},${y + h - dy} L${x + w},${y + h} Z" fill="${c3}"/>` +
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"/>` +
      `<rect x="${x}" y="${y}" width="${w}" height="${Math.min(h, 6)}" fill="#ffffff" opacity=".22"/></g>`;
  };
  // Farbe aufhellen/abdunkeln (#rrggbb, f -1..1)
  K.sh = (hex, f) => {
    const n = parseInt(hex.slice(1), 16); let r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    const m = v => Math.round(f >= 0 ? v + (255 - v) * f : v * (1 + f));
    return '#' + [m(r), m(g), m(b)].map(v => v.toString(16).padStart(2, '0')).join('');
  };
  K.chip = (x, y, s, c, sz = 34, bg = '#00000088') => {
    if (typeof c == 'number') { const q = c; c = sz; sz = q }
    const w = s.length * sz * .66 + sz * 1.2;
    return `<g transform="translate(${x},${y})"><rect x="${-w / 2}" y="${-sz * .95}" width="${w}" height="${sz * 1.5}" rx="${sz * .75}" fill="${bg}" stroke="${c}" stroke-width="3"/>${K.t(0, sz * .1, s, sz, c, { ls: 2 })}</g>`;
  };
  K.count = (a, b, p, d = 0, pre = '$') => M.fmt(M.lerp(a, b, p), d, pre);

  // ---- Szenen mit Uebergaengen ----
  // fx: push (seitlich), zoom (rein), dolly (zurueck), rise (von unten), flash (weisser Blitz + Zoom)
  K.scenes = [];
  K.add = (a, fx, f, opt = {}) => K.scenes.push(Object.assign({ a, fx, f }, opt));
  K.TD = .55;
  K.st = k => k == 0 ? -10 : K.S(K.scenes[k].a) - .3;
  K.camX = t => { let x = 0; K.scenes.forEach((s, k) => { if (k && s.fx == 'push') x += ei(cl(t, K.st(k), K.st(k) + K.TD)) }); return x };
  function tf(fx, q, dir) { // dir 1 = rein, -1 = raus; q 0..1 Fortschritt des Uebergangs
    const C = 'translate(540,820)', U = 'translate(-540,-820)';
    if (fx == 'push') { const x = dir > 0 ? (1 - q) * 1150 : -q * 1150, s = 1 - .08 * Math.sin(Math.PI * q); return [`translate(${x.toFixed(1)},0) ${C} scale(${s.toFixed(4)}) ${U}`, 1] }
    if (fx == 'rise') { const y = dir > 0 ? (1 - q) * 1400 : -q * 900; return [`translate(0,${y.toFixed(1)})`, dir > 0 ? 1 : 1 - q * .8] }
    if (fx == 'zoom' || fx == 'flash') { const s = dir > 0 ? .55 + .45 * q : 1 + 1.4 * q; return [`${C} scale(${s.toFixed(4)}) ${U}`, dir > 0 ? Math.min(1, q * 1.6) : 1 - q] }
    if (fx == 'dolly') { const s = dir > 0 ? 1.9 - .9 * q : 1 - .45 * q; return [`${C} scale(${s.toFixed(4)}) ${U}`, dir > 0 ? Math.min(1, q * 1.4) : 1 - q] }
    return ['', dir > 0 ? q : 1 - q];
  }
  K.render = t => {
    let out = ''; const n = K.scenes.length;
    for (let k = 0; k < n; k++) {
      const s0 = K.st(k), s1 = k + 1 < n ? K.st(k + 1) : 1e9;
      if (t < s0 || t > s1 + K.TD) continue;
      const sc = K.scenes[k];
      if (sc.html) continue; // HTML-Szenen zeichnen sich selbst
      let tr = '', op = 1;
      const qi = ei(cl(t, s0, s0 + K.TD)), qo = ei(cl(t, s1, s1 + K.TD));
      if (k > 0 && qi < 1) { const r = tf(sc.fx, qi, 1); tr = r[0]; op = r[1] }
      if (qo > 0) { const r = tf(K.scenes[k + 1].fx, qo, -1); tr = r[0] + ' ' + tr; op *= r[1] }
      if (op <= .001) continue;
      out += `<g transform="${tr}" opacity="${op.toFixed(3)}">${sc.f(t)}</g>`;
    }
    return out;
  };
  // Sichtbarkeit/Transform einer HTML-Szene k (fuer Intro)
  K.vis = (t, k) => { const n = K.scenes.length, s1 = k + 1 < n ? K.st(k + 1) : 1e9; return { q: ei(cl(t, s1, s1 + K.TD)), fx: k + 1 < n ? K.scenes[k + 1].fx : '' } };
  K.flash = t => { let f = 0; K.scenes.forEach((s, k) => { if (k && s.fx == 'flash') { const a = K.st(k); f = Math.max(f, Math.sin(Math.PI * cl(t, a - .05, a + .45)) * .9) } }); return f };
  K.sfx = () => {
    const e = [];
    K.scenes.forEach((s, k) => {
      if (k) {
        const a = K.st(k);
        if (s.fx == 'push') e.push({ k: 'swish', t: a, d: .5, pan: .4 });
        else if (s.fx == 'flash') { e.push({ k: 'riser', t: a - 1.0, d: 1.0 }); e.push({ k: 'impact', t: a + .15 }) }
        else if (s.fx == 'rise') e.push({ k: 'whoosh', t: a, d: .6 });
        else e.push({ k: 'whoosh', t: a, d: .7 });
      }
      if (s.sfx) e.push(...s.sfx());
    });
    return e.filter(x => x.t >= 0).sort((a, b) => a.t - b.t);
  };
  window.K = K;
})();
