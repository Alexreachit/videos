// Schritt-Engine + SVG-Bausteine fuer "The Hidden Price" (tt08/tt09). Alles deterministisch aus t.
(function () {
  const M = window.MG, cl = M.cl, ez = M.ez, ei = M.ei, bo = M.bo, lerp = M.lerp;
  const X = {};
  X.F = "'Arial Black',Arial,Helvetica,sans-serif";
  X.TR = .55;           // Uebergangsdauer
  X.CX = 540; X.CY = 840; // Bildmitte des Visual-Bereichs (Untertitelzone 1330-1560 bleibt frei)

  // Zeitpunkt des ersten Worts in Zeile i, das auf re passt (sonst Anteil frac der Zeile)
  X.wordT = (i, re, frac = .5) => {
    const l = M.L(i); const w = (l.words || []).find(w => re.test(w[0]));
    return w ? l.start + w[1] : l.start + (l.end - l.start) * frac;
  };
  X.lineP = (t, i, a = 0, b = 1) => { const l = M.L(i); return cl(t, l.start + (l.end - l.start) * a, l.start + (l.end - l.start) * b) };

  // ---- Schritt-Engine ----
  // steps: [{a: Zeilenindex, tr: 'left'|'right'|'up'|'drop'|'zoom'|'fade'|'cut', f:(t,s,io)=>svg, sfx:()=>[]}]
  X.steps = [];
  X.compute = function () {
    const S = X.steps;
    S.forEach((s, k) => { s.t0 = k == 0 ? 0 : M.L(s.a).start - .25 });
    S.forEach((s, k) => { s.t1 = k + 1 < S.length ? S[k + 1].t0 : 1e9; s.ls = M.L(s.a).start });
  };
  function tf(type, p, dir) {
    const q = dir == 'in' ? 1 - p : p, sg = dir == 'in' ? 1 : -1; // q: 0 = ruhend
    switch (type) {
      case 'left': return { tx: sg * 1080 * q, o: 1 };
      case 'right': return { tx: -sg * 1080 * q, o: 1 };
      case 'up': return { ty: sg * 1250 * q, o: 1 };
      case 'drop': return { ty: -sg * 1250 * q, o: 1 };
      case 'zoom': return dir == 'in' ? { s: .55 + .45 * p, o: Math.min(1, p * 1.6) } : { s: 1 + 1.4 * p, o: 1 - p };
      case 'cut': return { o: dir == 'in' ? (p > .35 ? 1 : 0) : (p > .35 ? 0 : 1) };
      default: return { o: dir == 'in' ? p : 1 - p };
    }
  }
  X.render = function (t) {
    const S = X.steps; let h = '';
    for (let k = 0; k < S.length; k++) {
      const s = S[k];
      if (t < s.t0 || t > s.t1 + X.TR) continue;
      const pin = k == 0 ? 1 : ei(cl(t, s.t0, s.t0 + X.TR)), nx = S[k + 1];
      const pout = nx ? ei(cl(t, s.t1, s.t1 + X.TR)) : 0;
      const A = k == 0 ? { o: 1 } : tf(s.tr, pin, 'in'), B = nx ? tf(nx.tr, pout, 'out') : { o: 1 };
      const tx = (A.tx || 0) + (B.tx || 0), ty = (A.ty || 0) + (B.ty || 0), sc = (A.s || 1) * (B.s || 1), o = (A.o == null ? 1 : A.o) * (B.o == null ? 1 : B.o);
      if (o <= .001) continue;
      const body = s.f(t, s, { pin, pout });
      h += `<g opacity="${o.toFixed(3)}" transform="translate(${(tx + X.CX).toFixed(1)},${(ty + X.CY).toFixed(1)}) scale(${sc.toFixed(4)}) translate(${-X.CX},${-X.CY})">${body}</g>`;
    }
    return h;
  };
  X.cur = t => { let k = 0; X.steps.forEach((s, i) => { if (t >= s.t0) k = i }); return k };
  X.sfx = function () {
    const e = [];
    X.steps.forEach((s, k) => {
      if (k > 0) {
        const tt = s.t0 + .02;
        if (s.tr == 'left' || s.tr == 'right') e.push({ k: 'swish', t: tt, d: .5, pan: s.tr == 'left' ? .4 : -.4 });
        else if (s.tr == 'zoom') e.push({ k: 'whoosh', t: tt - .15, d: .8 });
        else if (s.tr == 'up' || s.tr == 'drop') e.push({ k: 'swish', t: tt, d: .55, pan: 0 });
        else e.push({ k: 'shimmer', t: tt });
      }
      if (s.sfx) s.sfx(s).forEach(x => e.push(x));
    });
    return e;
  };

  // ---- Text ----
  X.T = (x, y, str, size, fill, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.a || 'middle'}" font-family="${X.F}" font-weight="900" font-size="${size}" fill="${fill}"${o.ls != null ? ` letter-spacing="${o.ls}"` : ''}${o.op != null ? ` opacity="${o.op}"` : ''}${o.st ? ` stroke="${o.st}" stroke-width="${o.sw || 8}" paint-order="stroke" stroke-linejoin="round"` : ''}>${str}</text>`;
  // grosse Zahl mit Pop + Glow
  X.big = (x, y, str, size, fill, p, glow = true) => {
    if (p <= 0) return '';
    const s = bo(p), o = cl(p, 0, .3);
    return `<g transform="translate(${x},${y}) scale(${s.toFixed(4)})" opacity="${o}">${glow ? `<g filter="url(#blur18)" opacity=".55">${X.T(0, 0, str, size, fill)}</g>` : ''}${X.T(0, 0, str, size, fill, { st: '#05070f', sw: Math.round(size / 9) })}</g>`;
  };
  // Kopfzeile (Kicker) oben mit wachsender Linie
  X.kick = (str, p, col = '#ffd166', y = 250, size = 62) => {
    if (p <= 0) return ''; const e = ez(p), w = Math.min(820, str.length * size * .62);
    return `<g opacity="${cl(p, 0, .4)}" transform="translate(0,${(1 - e) * -30})">${X.T(540, y, str, size, '#fff', { ls: 2, st: '#05070fcc', sw: 10 })}<rect x="${540 - w / 2 * e}" y="${y + 26}" width="${w * e}" height="8" rx="4" fill="${col}"/></g>`;
  };
  X.typed = (str, p) => str.slice(0, Math.floor(str.length * cl(p, 0, 1) + .001));

  // ---- Formen ----
  X.defs = `
  <filter id="blur18" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#000" flood-opacity=".55"/></filter>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".55" stop-color="#ffc145"/><stop offset="1" stop-color="#d98a12"/></linearGradient>
  <linearGradient id="gBunF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6c27a"/><stop offset=".6" stop-color="#d98d3c"/><stop offset="1" stop-color="#a65f22"/></linearGradient>
  <linearGradient id="gBunB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e7a95c"/><stop offset="1" stop-color="#9c5a20"/></linearGradient>
  <linearGradient id="gSaus" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0674a"/><stop offset=".5" stop-color="#b23a24"/><stop offset="1" stop-color="#7a2414"/></linearGradient>
  <linearGradient id="gCard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1fb6a8"/><stop offset=".55" stop-color="#2a5cff"/><stop offset="1" stop-color="#6b3cff"/></linearGradient>
  <linearGradient id="gCardG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="#f2b33d"/><stop offset="1" stop-color="#b8740c"/></linearGradient>
  <linearGradient id="gSteel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5571"/><stop offset="1" stop-color="#1b2133"/></linearGradient>
  <linearGradient id="gPanel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2640"/><stop offset="1" stop-color="#0d1222"/></linearGradient>
  <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6ff5ad"/><stop offset="1" stop-color="#17a85c"/></linearGradient>
  <linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a8a"/><stop offset="1" stop-color="#d83a3a"/></linearGradient>
  <linearGradient id="gBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc6ff"/><stop offset="1" stop-color="#3b7be0"/></linearGradient>
  <linearGradient id="gCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6d0" stop-opacity=".55"/><stop offset="1" stop-color="#fff6d0" stop-opacity="0"/></linearGradient>
  <radialGradient id="gSpot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <pattern id="hatch" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="22" height="22" fill="#ff5d5d22"/><rect width="8" height="22" fill="#ff5d5d55"/></pattern>`;

  // Hot Dog (Mitte 0,0, Breite ~470). m = Senf-Fortschritt
  X.hotdog = (m = 1) => {
    const L = 560;
    return `<g>
    <ellipse cx="0" cy="70" rx="230" ry="22" fill="#000" opacity=".35" filter="url(#blur8)"/>
    <path d="M-205,-8 Q-212,-74 -150,-76 L150,-76 Q212,-74 205,-8 Z" fill="url(#gBunB)"/>
    <rect x="-238" y="-66" width="476" height="70" rx="35" fill="url(#gSaus)"/>
    <rect x="-205" y="-58" width="380" height="13" rx="6.5" fill="#ffffff" opacity=".28"/>
    <path d="M-205,-36 q20,-26 40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0" fill="none" stroke="#ffd23f" stroke-width="11" stroke-linecap="round" stroke-dasharray="${L}" stroke-dashoffset="${(L * (1 - m)).toFixed(1)}"/>
    <path d="M-222,-22 Q-230,58 -150,62 L150,62 Q230,58 222,-22 Q150,4 0,4 Q-150,4 -222,-22 Z" fill="url(#gBunF)"/>
    <path d="M-160,30 Q0,44 160,30" stroke="#ffffff" stroke-opacity=".18" stroke-width="8" fill="none" stroke-linecap="round"/>
  </g>`;
  };
  // Becher (Boden bei y=0, Hoehe ~330)
  X.soda = () => `<g>
    <ellipse cx="0" cy="6" rx="105" ry="16" fill="#000" opacity=".35" filter="url(#blur8)"/>
    <path d="M-100,-300 L100,-300 L80,0 L-80,0 Z" fill="#f4f6fb"/>
    <path d="M-93,-210 L93,-210 L88,-150 L-88,-150 Z" fill="#ff5d5d"/>
    <path d="M-86,-120 L86,-120 L83,-90 L-83,-90 Z" fill="#60a5fa"/>
    <path d="M-100,-300 L-60,-300 L-48,0 L-80,0 Z" fill="#000" opacity=".08"/>
    <rect x="-112" y="-322" width="224" height="28" rx="10" fill="#dfe6f2"/>
    <rect x="18" y="-450" width="18" height="140" rx="8" fill="#ff5d5d" transform="rotate(12 27 -320)"/>
  </g>`;
  // Preisschild (Mitte 0,0)
  X.tag = (txt = '$1.50', w = 380, h = 200) => `<g>
    <path d="M${-w / 2 + 50},${-h / 2} L${w / 2 - 20},${-h / 2} Q${w / 2},${-h / 2} ${w / 2},${-h / 2 + 20} L${w / 2},${h / 2 - 20} Q${w / 2},${h / 2} ${w / 2 - 20},${h / 2} L${-w / 2 + 50},${h / 2} L${-w / 2},0 Z" fill="url(#gGold)" stroke="#fff3c4" stroke-width="5"/>
    <circle cx="${-w / 2 + 48}" cy="0" r="14" fill="#2a1a00"/>
    ${X.T(30, h * .2, txt, h * .52, '#3a2300')}
  </g>`;
  // Mitgliedskarte (Mitte 0,0, 520x330), back=true -> Rueckseite mit Text
  X.card = (front = true, label = 'MEMBER', gold = false, w = 520, h = 330) => `<g>
    <rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="34" fill="url(#${gold ? 'gCardG' : 'gCard'})" stroke="#ffffff55" stroke-width="3"/>
    ${front ? `<rect x="${-w / 2 + 44}" y="${-h / 2 + 96}" width="78" height="60" rx="12" fill="url(#gGold)" stroke="#b9791a" stroke-width="3"/>
    ${X.T(-w / 2 + 44, h / 2 - 50, label, 44, gold ? '#3a2300' : '#ffffff', { a: 'start', ls: 6 })}
    <circle cx="${w / 2 - 80}" cy="${-h / 2 + 70}" r="30" fill="#ffffff44"/><circle cx="${w / 2 - 50}" cy="${-h / 2 + 70}" r="30" fill="#ffffff2a"/>` :
      `<rect x="${-w / 2}" y="${-h / 2 + 50}" width="${w}" height="60" fill="#0b0e17cc"/>`}
    <path d="M${-w / 2 + 34},${-h / 2 + 6} L${w / 2 - 34},${-h / 2 + 6}" stroke="#ffffff66" stroke-width="5" stroke-linecap="round"/>
  </g>`;
  X.house = (c = '#60a5fa', lit = 1) => `<g><path d="M-40,-6 L0,-44 L40,-6 Z" fill="${c}"/><rect x="-32" y="-8" width="64" height="48" fill="${c}" opacity=".85"/><rect x="-10" y="12" width="20" height="28" fill="#0b1020"/><rect x="-26" y="2" width="14" height="12" fill="#ffd166" opacity="${lit}"/><rect x="12" y="2" width="14" height="12" fill="#ffd166" opacity="${lit}"/></g>`;
  X.person = (c = '#dfe7ff') => `<g><circle cx="0" cy="-58" r="20" fill="${c}"/><path d="M-26,0 L-26,-22 Q-26,-38 -10,-38 L10,-38 Q26,-38 26,-22 L26,0 Z" fill="${c}"/></g>`;
  X.arrowUp = (c = '#ff5d5d', s = 1) => `<g transform="scale(${s})"><path d="M0,-34 L24,-6 L9,-6 L9,30 L-9,30 L-9,-6 L-24,-6 Z" fill="${c}" stroke="#05070f" stroke-width="4" stroke-linejoin="round"/></g>`;
  X.check = (c = '#35e08a', s = 1) => `<g transform="scale(${s})"><circle r="40" fill="${c}"/><path d="M-18,2 L-5,15 L19,-12" fill="none" stroke="#05070f" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></g>`;
  X.cross = (c = '#ff5d5d', s = 1) => `<g transform="scale(${s})"><circle r="40" fill="${c}"/><path d="M-14,-14 L14,14 M14,-14 L-14,14" stroke="#05070f" stroke-width="9" stroke-linecap="round"/></g>`;
  X.badge = (inner, c, r = 92) => `<g><circle r="${r}" fill="#0d1428" stroke="${c}" stroke-width="7"/><circle r="${r - 14}" fill="${c}" opacity=".14"/>${inner}</g>`;
  // Lichtkegel von oben
  X.cone = (x, y, w0, w1, h, o = 1) => `<path d="M${x - w0 / 2},${y} L${x + w0 / 2},${y} L${x + w1 / 2},${y + h} L${x - w1 / 2},${y + h} Z" fill="url(#gCone)" opacity="${o}"/>`;
  X.floor = (y = 1180, w = 760, c = '#ffffff') => `<ellipse cx="540" cy="${y}" rx="${w / 2}" ry="${w / 14}" fill="${c}" opacity=".06"/><ellipse cx="540" cy="${y}" rx="${w / 3}" ry="${w / 22}" fill="${c}" opacity=".06"/>`;
  // Hintergrund-Farben je Schritt, weich ueberblendet
  X.bg = function (el, t, pal) {
    const k = X.cur(t), s = X.steps[k], nx = X.steps[k + 1];
    const a = pal[k % pal.length], b = nx ? pal[(k + 1) % pal.length] : a;
    const p = nx ? ei(cl(t, s.t1 - .1, s.t1 + .6)) : 0; // Uebergang kurz vor naechstem Schritt
    const mix = (c1, c2) => { const h = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)); const A = h(c1), B = h(c2); return '#' + A.map((v, i) => Math.round(lerp(v, B[i], p)).toString(16).padStart(2, '0')).join('') };
    const c1 = mix(a[0], b[0]), c2 = mix(a[1], b[1]);
    const dx = Math.sin(t * .35) * 80, dy = Math.cos(t * .27) * 60;
    el.style.background = `radial-gradient(900px 700px at ${300 + dx}px ${620 + dy}px, ${c1}66, transparent 70%), radial-gradient(900px 800px at ${800 - dx}px ${1180 - dy}px, ${c2}55, transparent 70%), radial-gradient(130% 90% at 50% 40%, #141c34, #080b16 60%, #03050b)`;
  };
  window.X = X;
})();
