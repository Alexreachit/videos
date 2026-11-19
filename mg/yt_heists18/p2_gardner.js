// ===================== Set GAR: Museum in Boston (aussen Nacht + Galerie innen) =====================
const GA = [0, 0, 0];          // Fassade / Strasse
const GI = [0, 0, -80];         // Galerie innen (Mitte des Bodens)
(function gardner() {
  const S = 'GAR', FAC = '#e8c6a2', FAC2 = '#d4ad88';
  // Strasse + Gehweg
  mk(S, merge([at(G.box(80, .4, 30, '#3a3f55', { base: true }), [0, -.4, 14]), at(G.box(80, .25, 4, '#6a6e80', { base: true }), [0, 0, 2])]), { outline: false });
  // Fassade (Palazzo) mit Bogenfenstern
  const L = [at(G.box(26, 12, 1.2, FAC, { base: true }), [0, 0, -.6]), at(G.box(26.6, .5, 1.6, FAC2, { base: true }), [0, 12, -.6]), at(G.box(26.6, .4, 1.5, FAC2, { base: true }), [0, 4.2, -.5])];
  for (let k = -3; k <= 3; k++) if (k) { const x = k * 3.4; L.push(at(G.box(1.6, 2.4, .3, '#2a2438', { base: true }), [x, 1.4, .05]), at(G.box(1.6, 2.6, .3, '#2a2438', { base: true }), [x, 6.4, .05])) }
  mk(S, merge(L).vary(.03, 7));
  // warme Fenster (leuchten)
  const WL = []; for (let k = -3; k <= 3; k++) if (k && Math.abs(k) != 2) WL.push(at(G.box(1.3, 2.1, .1, '#ffcf7a', { base: true }), [k * 3.4, 6.6, .22]));
  mk(S, merge(WL), { emis: .9, outline: false, cast: false });
  // Eingang: Tuer + Vordach + Lampe
  mk(S, merge([at(G.box(2.6, 3.4, .4, '#4a2e22', { base: true }), [0, 0, .1]), at(G.box(.12, 3.4, .5, '#2a1a12', { base: true }), [0, 0, .12]),
    at(G.box(3.6, .3, 1.6, FAC2, { base: true }), [0, 3.6, .6]), at(G.box(.4, .4, .2, '#c9a23c', { base: true }), [1.6, 1.6, .38])]));
  mk(S, G.ico(.25, 2, '#fff2c0'), { pos: [0, 3.3, 1.1], emis: 1, outline: false, cast: false });
  // Strassenlaterne
  mk(S, merge([at(G.cyl(.12, .1, 5.2, 10, '#22252e'), [5.5, 0, 3.2]), at(G.box(.7, .8, .7, '#22252e', { base: true }), [5.5, 5.1, 3.2])]));
  mk(S, G.box(.5, .55, .5, '#ffe7a0', { base: true }), { pos: [5.5, 5.2, 3.2], emis: 1, outline: false, cast: false });
  // Baeume (dunkel) links/rechts
  [-11, 11].forEach((x, k) => mk(S, merge([at(G.cyl(.25, .2, 3, 8, '#3a2a22'), [x, 0, 3]), at(G.ico(1.8, 2, '#2c4a3c'), [x, 4, 3]), at(G.ico(1.3, 2, '#35574a'), [x + .8, 4.8, 3.3])]).smooth(), { cast: true }));
  // ---------- Galerie innen ----------
  const WALL = '#3f6150', WALL2 = '#355445', FLOOR = '#8a5a3a';
  mk(S, merge([at(G.box(22, .3, 14, FLOOR, { base: true, top: '#9a6a46' }), [GI[0], -.3, GI[2]]),
    at(G.box(22, 7, .4, WALL, { base: true }), [GI[0], 0, GI[2] - 7]), at(G.box(.4, 7, 14, WALL2, { base: true }), [GI[0] - 11, 0, GI[2]]), at(G.box(.4, 7, 14, WALL2, { base: true }), [GI[0] + 11, 0, GI[2]]),
    at(G.box(22, .35, .5, '#5a3a26', { base: true }), [GI[0], 0, GI[2] - 6.75]), at(G.box(22, .3, .5, '#c9a23c', { base: true }), [GI[0], 5.6, GI[2] - 6.75]),
    at(G.box(22, .5, 14, '#2a2026', { base: true }), [GI[0], 7, GI[2]])]), { outline: false });
  // Holzbalken an der Decke
  mk(S, merge([...Array(6)].map((_, k) => at(G.box(.4, .4, 14, '#5a3a26', { base: true }), [GI[0] - 9 + k * 3.6, 6.6, GI[2]]))), { outline: false });
  // Bank in der Mitte, Teppich
  mk(S, merge([at(G.box(8, .05, 5, '#8a2a30', { base: true }), [GI[0], 0, GI[2] - 1]), at(G.box(3, .5, .9, '#6b4226', { base: true }), [GI[0], 0, GI[2] + 1.5])]), { outline: false });
})();
// Gemaelde-Texturen (generische, selbst gezeichnete Motive – keine Reproduktionen)
function paintTex(kind) {
  return tex(512, kind == 'storm' ? 640 : 512, (x, wd, ht) => {
    if (kind == 'storm') {
      const g = x.createLinearGradient(0, 0, 0, ht); g.addColorStop(0, '#2b3242'); g.addColorStop(.45, '#7a7a62'); g.addColorStop(1, '#203a34'); x.fillStyle = g; x.fillRect(0, 0, wd, ht);
      x.fillStyle = '#e8d8a8'; x.beginPath(); x.ellipse(380, 120, 150, 70, -.3, 0, 7); x.fill();
      x.fillStyle = '#1c2e2a'; for (let k = 0; k < 5; k++) { x.beginPath(); x.moveTo(0, 430 + k * 40); for (let s = 0; s <= 512; s += 32) x.quadraticCurveTo(s + 16, 400 + k * 40 - 30 * Math.sin(s * .02 + k), s + 32, 430 + k * 40); x.lineTo(512, 640); x.lineTo(0, 640); x.fill() }
      x.save(); x.translate(250, 400); x.rotate(-.35); x.fillStyle = '#4a2e1e'; x.beginPath(); x.moveTo(-150, 0); x.lineTo(150, -20); x.lineTo(110, 50); x.lineTo(-110, 60); x.fill();
      x.fillStyle = '#3a2618'; x.fillRect(-6, -250, 12, 250); x.fillStyle = '#d8ccaa'; x.beginPath(); x.moveTo(6, -240); x.lineTo(150, -60); x.lineTo(6, -40); x.fill(); x.restore();
      x.strokeStyle = '#f2ead0aa'; x.lineWidth = 6; for (let k = 0; k < 8; k++) { x.beginPath(); x.arc(100 + k * 50, 470 + (k % 2) * 30, 30, PI, PI * 1.8); x.stroke() }
    } else if (kind == 'music') {
      x.fillStyle = '#5a4a3a'; x.fillRect(0, 0, wd, ht); x.fillStyle = '#8a7a62'; x.fillRect(0, 0, wd, 300);
      x.fillStyle = '#2a2a2a'; for (let k = 0; k < 8; k++) { x.fillRect(k * 64, 330, 32, 32); x.fillRect(k * 64 + 32, 362, 32, 32) }
      x.fillStyle = '#3a2a1e'; x.fillRect(60, 250, 220, 90); x.fillStyle = '#f0e6c8'; x.fillRect(70, 255, 200, 20);
      const p = (cx, col) => { x.fillStyle = col; x.beginPath(); x.ellipse(cx, 300, 40, 70, 0, 0, 7); x.fill(); x.fillStyle = '#f0d8b8'; x.beginPath(); x.arc(cx, 210, 22, 0, 7); x.fill() };
      p(170, '#e8e0c0'); p(310, '#7a3a2a'); p(420, '#3a4a6a');
    } else {
      x.fillStyle = '#2a2622'; x.fillRect(0, 0, wd, ht);
      const p = (cx) => { x.fillStyle = '#111'; x.beginPath(); x.ellipse(cx, 380, 80, 150, 0, 0, 7); x.fill(); x.fillStyle = '#fff'; x.fillRect(cx - 40, 250, 80, 18); x.fillStyle = '#e8c8a8'; x.beginPath(); x.arc(cx, 210, 36, 0, 7); x.fill() };
      p(170); p(350);
    }
  });
}
const FRAMES = [];
function frame3(set, p, wd, ht, kind, o = {}) {
  const b = .22, col = '#c9a23c';
  const f = mk(set, merge([at(G.box(wd + 2 * b, b, .18, col), [0, ht / 2 + b / 2, 0]), at(G.box(wd + 2 * b, b, .18, col), [0, -ht / 2 - b / 2, 0]),
    at(G.box(b, ht, .18, col), [-wd / 2 - b / 2, 0, 0]), at(G.box(b, ht, .18, col), [wd / 2 + b / 2, 0, 0])]), { pos: p, rot: o.rot || [0, 0, 0], spec: .5 });
  const pl = texPlane(set, wd, ht, () => kind == 'empty' ? null : (o.texFn ? o.texFn() : paintTex(kind)), { pos: X(p, 0, 0, .02), rot: o.rot || [0, 0, 0] });
  if (kind == 'empty') pl.vis = pl._v = false;
  const fr = { f, pl, p, kind }; FRAMES.push(fr); return fr;
}
// Hauptwand: drei Rahmen (Sturm, Musik, Paar)
const FR_STORM = frame3('GAR', [GI[0] - 5, 3.4, GI[2] - 6.75], 2.4, 3.0, 'storm');
const FR_MUSIC = frame3('GAR', [GI[0] + .2, 3.2, GI[2] - 6.75], 2.2, 2.2, 'music');
const FR_PAIR = frame3('GAR', [GI[0] + 5.2, 3.2, GI[2] - 6.75], 2.0, 2.4, 'pair');
// Seitenwand (rechts): Galerie der 6 Faelle (Countdown-Wand)
const CASE_ICON = ['train', 'lady', 'drill', 'crown', 'diamond', 'empty'];
function iconTex(k) {
  return tex(400, 400, (x) => {
    const g = x.createLinearGradient(0, 0, 0, 400); g.addColorStop(0, '#f6efe0'); g.addColorStop(1, '#e2d4b8'); x.fillStyle = g; x.fillRect(0, 0, 400, 400);
    x.lineWidth = 12; x.strokeStyle = OL; x.lineJoin = 'round';
    if (k == 'train') { x.fillStyle = '#3f7a4a'; x.fillRect(60, 160, 260, 120); x.strokeRect(60, 160, 260, 120); x.fillStyle = '#ffe9a0'; x.fillRect(250, 185, 50, 45); x.strokeRect(250, 185, 50, 45);
      x.fillStyle = OL; [110, 190, 270].forEach(c => { x.beginPath(); x.arc(c, 290, 28, 0, 7); x.fill() }); x.fillRect(30, 320, 340, 12) }
    if (k == 'lady') { x.fillStyle = '#5a6a4a'; x.fillRect(80, 40, 240, 320); x.fillStyle = '#3a2a1e'; x.beginPath(); x.ellipse(200, 300, 100, 110, 0, PI, 0); x.fill(); x.fillStyle = '#e8c890'; x.beginPath(); x.ellipse(200, 170, 50, 64, 0, 0, 7); x.fill(); x.fillStyle = '#3a2a1e'; x.beginPath(); x.ellipse(200, 140, 62, 50, 0, PI, 0); x.fill(); x.strokeRect(80, 40, 240, 320) }
    if (k == 'drill') { x.fillStyle = '#e0303a'; x.fillRect(70, 150, 180, 80); x.strokeRect(70, 150, 180, 80); x.fillStyle = '#c9ccd4'; x.fillRect(250, 175, 100, 30); x.strokeRect(250, 175, 100, 30); x.fillStyle = OL; x.fillRect(110, 230, 50, 90) }
    if (k == 'crown') { x.fillStyle = '#ffd166'; x.beginPath(); x.moveTo(80, 300); x.lineTo(70, 130); x.lineTo(140, 200); x.lineTo(200, 100); x.lineTo(260, 200); x.lineTo(330, 130); x.lineTo(320, 300); x.closePath(); x.fill(); x.stroke();
      x.fillStyle = '#4fc3f7'; [130, 200, 270].forEach(c => { x.beginPath(); x.arc(c, 260, 18, 0, 7); x.fill(); x.stroke() }) }
    if (k == 'diamond') { x.fillStyle = '#9fe3ff'; x.beginPath(); x.moveTo(80, 160); x.lineTo(140, 90); x.lineTo(260, 90); x.lineTo(320, 160); x.lineTo(200, 330); x.closePath(); x.fill(); x.stroke(); x.beginPath(); x.moveTo(80, 160); x.lineTo(320, 160); x.moveTo(140, 90); x.lineTo(200, 330); x.lineTo(260, 90); x.stroke() }
    if (k == 'empty') { x.fillStyle = '#3f6150'; x.fillRect(0, 0, 400, 400); x.fillStyle = '#ffd166'; x.font = '900 220px Arial'; x.textAlign = 'center'; x.fillText('?', 200, 280) }
  });
}
const CASES = CASE_ICON.map((k, j) => frame3('GAR', [GI[0] + 10.75, 3.1, GI[2] - 5 + j * 1.9], 1.4, 1.4, k, { rot: [0, -PI / 2, 0], texFn: () => iconTex(k) }));
// Waechter-Pult + Keller (fuer Kapitel 1)
mk('GAR', merge([at(G.box(2.2, 1.1, 1, '#6b4226', { base: true }), [GI[0] - 8, 0, GI[2] + 4]), at(G.box(.9, .5, .6, '#2a2a33', { base: true }), [GI[0] - 8.3, 1.1, GI[2] + 4])]));
const DOORP = [0, 0, 1.4];   // vor der Tuer
// ---------- Shots: Hook (Zeilen 0-3) ----------
SHOT.g_hook_door = {
  set: 'GAR', light: (t, i) => t > wt(i, /eighty/i) - .1 ? 'indoorWarm' : 'night',
  cam: i => { const t2 = wt(i, /eighty/i) - .1; return [
    { t0: Lt(i).start, a: { pos: [6, 2.6, 11], at: [0, 2.0, 0], fov: 44 }, b: { pos: [2.6, 1.9, 6.4], at: [0, 1.6, 0], fov: 40 } },
    { t0: t2, a: { pos: [GI[0], 3.0, GI[2] + 4], at: [GI[0], 3.0, GI[2] - 6.75], fov: 52 }, b: { pos: [GI[0], 3.1, GI[2] + 2.2], at: [GI[0], 3.1, GI[2] - 6.75], fov: 50 } }] },
  upd: (t, i) => { const empty = t > wt(i, /eighty/i) - .1; [FR_STORM, FR_MUSIC, FR_PAIR].forEach(f => f.pl.vis = !empty) },
  figs: (t, i) => {
    if (t > wt(i, /eighty/i) - .1) return '';
    const ring = wt(i, /bell/) - .1, hR = t > ring && t < ring + .6 ? [210, 96] : null;
    return fig([-.8, 0, 1.6], 'fakecop', { mouth: 'hmm', blink: bl(t, 0), look: [2, -2], hR, armL: [.2, .15] }) +
      fig([.9, 0, 2.0], 'fakecop', { mouth: 'hmm', blink: bl(t, 1.3), look: [-3, -2], armL: [.15, .1], armR: [.15, .1] });
  },
  ui: (t, i) => { const tb = wt(i, /bell/); let h = '';
    if (t > tb && t < tb + 1.4) h += labelAt([0, 3.6, .5], `<div style="font:900 90px IB;color:#ffd166;text-shadow:${shadowTxt(OL, 6)};transform:rotate(-6deg)">DING DONG!</div>`, t, tb, tb + 1.4);
    const te = wt(i, /eighty/i); h += pillAt(960, 760, t, te, nextStart(i), '⏱ 80 MINUTES LATER', '#232838', '#fff', 46);
    h += stampAt(960, 500, t, wt(i, /gone/) - .05, 'GONE', '#e0303a', 150, -8);
    return h },
  sfx: i => [{ k: 'bell', t: wt(i, /bell/) }, { k: 'whoosh', t: wt(i, /eighty/i) - .2, d: .5 }, { k: 'impact', t: wt(i, /gone/) }],
};
SHOT.g_hook_frames = {
  set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [FR_STORM.p[0] + 1, 3.2, GI[2] + .5], at: [FR_STORM.p[0], 3.2, GI[2] - 6.75], fov: 46 }, b: { pos: [FR_PAIR.p[0] - .6, 3.2, GI[2] + .8], at: [FR_PAIR.p[0], 3.2, GI[2] - 6.75], fov: 46 } }),
  upd: (t, i) => { [FR_STORM, FR_MUSIC, FR_PAIR].forEach(f => f.pl.vis = false) },
  ui: (t, i) => { let h = counter(960, 300, t, Lt(i).start, nextStart(i), wt(i, /thirteen/i) - .2, wt(i, /thirteen/i) + .7, 0, 13, v => Math.round(v) + ' WORKS STOLEN', '#232838', '#fff', 64);
    h += stampAt(960, 600, t, wt(i, /single/) - .05, 'STILL MISSING', '#e0303a', 120, -6);
    return h },
  sfx: i => [{ k: 'pop', t: wt(i, /thirteen/i) }, { k: 'impact', t: wt(i, /single/) }],
};
SHOT.count_wall = {
  set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0] + 4.5, 3.0, GI[2] - 6.2], at: [GI[0] + 10.75, 3.0, GI[2] - 3.2], fov: 50 }, b: { pos: [GI[0] + 4.8, 3.0, GI[2] + 3.4], at: [GI[0] + 10.75, 3.0, GI[2] + .6], fov: 50 } }),
  upd: (t, i) => { [FR_STORM, FR_MUSIC, FR_PAIR].forEach(f => f.pl.vis = false) },
  ui: (t, i) => { let h = ''; const a = wt(i, /number/), b = wt(i, /five/);
    CASES.forEach((c, j) => { const q = w.project(X(c.p, -.1, 1.05, 0)); if (!q.vis) return; const n = 6 - j, t0 = j == 5 ? a : b + j * .18;
      if (t > t0) h += `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%) scale(${pop(t, t0)});font:900 64px IB;color:${n == 1 ? '#ffd166' : '#fff'};text-shadow:${shadowTxt(OL, 5)};z-index:2100">#${n}</div>` });
    h += bigText(960, 170, t, wt(i, /bold/) - .1, nextStart(i), 'SO BOLD THEY LOOK <span style="color:#ffd166">FAKE</span>', 84);
    return h },
  sfx: i => [{ k: 'ding', t: wt(i, /number/) }, ...[0, 1, 2, 3, 4].map(j => ({ k: 'pop', t: wt(i, /five/) + j * .18 }))],
};
SHOT.magnifier = {
  set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0] - 2.2, 1.6, GI[2] + 1.6], at: [GI[0] - 2.2, 1.25, GI[2] - 2], fov: 40 }, b: { pos: [GI[0] - 2.2, 1.45, GI[2] + .4], at: [GI[0] - 2.2, 1.2, GI[2] - 2], fov: 38 } }),
  figs: (t, i) => { const lk = Math.sin(t * 1.6) * 4; return fig([GI[0] - 2.2, 0, GI[2] - 2], 'det', { mouth: t > wt(i, /tiny/) ? 'o' : 'hmm', blink: bl(t, .4), look: [lk, 3], prop: PROP.magnifier, hR: [176 + lk * 3, 112], armL: [.25, .2] }) },
  ui: (t, i) => pillAt(960, 200, t, wt(i, /tiny/) - .1, nextStart(i), '🔍 ONE TINY MISTAKE', '#ffd166', OL, 60),
  sfx: i => [{ k: 'ding', t: wt(i, /tiny/) }],
};
