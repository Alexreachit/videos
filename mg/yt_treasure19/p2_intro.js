// ===================== Helfer fuer kompakte Shots =====================
const cm = (pos, at, fov = 48) => ({ pos, at, fov });
const mv = (a, b) => ({ a, b });                  // Kamerafahrt a->b ueber die Zeile
// zweiteilige Einstellung: Schnitt beim Wort re
const cut2 = (i, re, a1, b1, a2, b2) => [{ t0: Lt(i).start, a: a1, b: b1 }, { t0: wt(i, re) - .15, a: a2, b: b2 }];
function seaGrid(set, cx, cz, size, step, col, o = {}, sz = size) {
  const g = new G.Geo(), k = G.hex(col), n = Math.round(size / step), m = Math.round(sz / step);
  for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) { const x0 = cx - size / 2 + i * step, z0 = cz - sz / 2 + j * step, x1 = x0 + step, z1 = z0 + step;
    g.tri([x0, 0, z0], [x0, 0, z1], [x1, 0, z1], k); g.tri([x0, 0, z0], [x1, 0, z1], [x1, 0, z0], k) }
  return mk(set, g, Object.assign({ wave: .22, cast: false, recv: true, outline: false }, o));
}
const tree = (x, z, s = 1, c = '#2f6a3a', k = 0) => [at(G.cyl(.25 * s, .2 * s, 2.4 * s, 8, '#5a3a26'), [x, 0, z]), at(G.cyl(1.7 * s, .08, 4.2 * s, 9, c), [x, 2 * s, z]), at(G.cyl(1.3 * s, .06, 3.2 * s, 9, c), [x, 3.6 * s, z])];
const leafy = (x, z, s = 1, c = '#3a7a3a') => [at(G.cyl(.3 * s, .24 * s, 3 * s, 8, '#5a3a26'), [x, 0, z]), at(G.ico(1.9 * s, 2, c), [x, 3.8 * s, z]), at(G.ico(1.4 * s, 2, c), [x + .9 * s, 4.4 * s, z + .3 * s])];
// ===================== Set INT: Schreibtisch mit Schatzkarte (Hook-Liste + Outro) =====================
const IX = -600, ID = [IX, 0, 0];
(function intro() {
  const S = 'INT';
  mk(S, merge([at(G.box(30, .3, 20, '#4a3428', { base: true }), [IX, -.3, 0]), at(G.box(30, 9, .4, '#5a4436', { base: true }), [IX, 0, -7]),
    at(G.box(10, .3, 6, '#7a4a2a', { base: true, top: '#8a5632' }), [IX, 1.5, 0]), ...[[-4.6, -2.6], [4.6, -2.6], [-4.6, 2.6], [4.6, 2.6]].map(([x, z]) => at(G.box(.35, 1.5, .35, '#5a3420', { base: true }), [IX + x, 0, z]))]), { outline: false });
  // Regal mit Buechern hinten
  const B = [at(G.box(8, 5, .8, '#4a2e1e', { base: true }), [IX - 6, 0, -6.4])];
  for (let r = 0; r < 4; r++) for (let k = 0; k < 14; k++) B.push(at(G.box(.4, .9 + G.hash(k, r) * .3, .6, ['#8a2a2a', '#2a5a8a', '#c9a23c', '#3a6a3a', '#6a3a7a'][(k + r) % 5], { base: true }), [IX - 9 + k * .48, .2 + r * 1.2, -6.2]));
  mk(S, merge(B), { outline: false });
  // Lampe
  mk(S, merge([at(G.cyl(.4, .3, .15, 12, '#2a2a33'), [IX + 3.6, 1.8, -1.8]), at(G.cyl(.05, .05, 1.6, 6, '#2a2a33'), [IX + 3.6, 1.8, -1.8]), at(G.cyl(.7, .25, .6, 14, '#2f7a4a', { open: true }), [IX + 3.6, 3.1, -1.6])]));
  mk(S, G.ico(.2, 2, '#fff2c0'), { pos: [IX + 3.6, 3.05, -1.6], emis: 1, outline: false, cast: false });
  // Kompass + Lupe auf dem Tisch
  mk(S, merge([at(G.cyl(.45, .45, .12, 20, '#c9a23c'), [IX - 3.7, 1.8, 1.6]), at(G.cyl(.36, .36, .13, 20, '#f4efe2'), [IX - 3.7, 1.82, 1.6])]));
})();
// Weltkarte als Pergament (Natural Earth, mapdata.js) – Ausschnitt lon -130..45, lat 0..68
const MAPB = { lon0: -130, lon1: 45, lat0: 0, lat1: 68 };
function mapXY(lon, lat, wd, ht) { const [x0, y1] = MAPP(MAPB.lon0, MAPB.lat0), [x1, y0] = MAPP(MAPB.lon1, MAPB.lat1), [x, y] = MAPP(lon, lat); return [(x - x0) / (x1 - x0) * wd, (y - y0) / (y1 - y0) * ht] }
function mapTex() { return tex(2048, 1280, (x, wd, ht) => {
  const g = x.createRadialGradient(wd / 2, ht / 2, 200, wd / 2, ht / 2, 1300); g.addColorStop(0, '#f3e2b8'); g.addColorStop(1, '#c9a46a'); x.fillStyle = g; x.fillRect(0, 0, wd, ht);
  const [x0, y1] = MAPP(MAPB.lon0, MAPB.lat0), [x1, y0] = MAPP(MAPB.lon1, MAPB.lat1);
  x.save(); x.scale(wd / (x1 - x0), ht / (y1 - y0)); x.translate(-x0, -y0);
  for (const k in WORLD) { const p = new Path2D(WORLD[k]); x.fillStyle = '#d9c08a'; x.fill(p); x.strokeStyle = '#7a5a32'; x.lineWidth = 1.2; x.stroke(p) }
  x.restore();
  x.strokeStyle = '#a0804a55'; x.lineWidth = 3; for (let k = 1; k < 8; k++) { x.beginPath(); x.moveTo(k * wd / 8, 0); x.lineTo(k * wd / 8, ht); x.stroke() } for (let k = 1; k < 5; k++) { x.beginPath(); x.moveTo(0, k * ht / 5); x.lineTo(wd, k * ht / 5); x.stroke() }
  x.strokeStyle = '#6a4a22'; x.lineWidth = 16; x.strokeRect(8, 8, wd - 16, ht - 16);
}) }
const MAPW = 8, MAPH = 5;
texPlane('INT', MAPW, MAPH, mapTex, { pos: [IX, 1.82, 0], rot: [-PI / 2, 0, 0] });
// 6 Schaetze: lon/lat -> 3D-Punkt auf der Karte
const TRS = [
  { n: 6, ic: '🚂', name: 'NAZI GOLD TRAIN', lon: 16.3, lat: 50.8 },
  { n: 5, ic: '🏝️', name: 'OAK ISLAND', lon: -64.3, lat: 44.5 },
  { n: 4, ic: '🧰', name: "FENN'S CHEST", lon: -108, lat: 43.5 },
  { n: 3, ic: '🥚', name: 'FABERGÉ EGG', lon: 37.6, lat: 55.7 },
  { n: 2, ic: '🟧', name: 'AMBER ROOM', lon: 30.4, lat: 59.7 },
  { n: 1, ic: '⛵', name: 'SAN JOSÉ', lon: -75.5, lat: 10.4 }];
TRS.forEach(c => { const [u, v] = mapXY(c.lon, c.lat, MAPW, MAPH); c.p = [IX - MAPW / 2 + u, 1.84, -MAPH / 2 + v] });
const PINS = TRS.map(c => mk('INT', merge([at(G.cyl(.03, .03, .5, 6, '#2a2a33'), [0, 0, 0]), at(G.ico(.12, 2, c.n == 1 ? '#ffd166' : '#e0303a'), [0, .5, 0])]), { pos: c.p }));
function pinUI(t, t0, step, hi) {
  let h = ''; TRS.forEach((c, j) => { const a = t0 + j * step; if (t < a) return; const q = w.project(X(c.p, 0, .7, 0)); if (!q.vis) return;
    h += `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%) scale(${pop(t, a)});transform-origin:50% 100%;z-index:2100">${PILL(c.ic + ' #' + c.n, c.n == hi ? '#ffd166' : '#232838', c.n == hi ? OL : '#fff', 40)}</div>` });
  return h;
}
function intUpd(t, i) { PINS.forEach((m, j) => { m.vis = true; m.scl = [1, 1, 1] }) }
SHOT.count_wall = { set: 'INT', light: 'indoorWarm',
  cam: i => mv(cm([IX, 7.5, 5.2], [IX, 1.8, .2], 46), cm([IX, 6.6, 4.4], [IX, 1.8, .1], 46)),
  upd: (t, i) => { intUpd(t, i); PINS.forEach((m, j) => { const a = wt(i, /five/) + j * .22; m.vis = t > a || j == 5; m.scl = [1, j == 5 ? 1 : bo(cl(t, a, a + .3)), 1] }) },
  ui: (t, i) => pinUI(t, wt(i, /five/), .22, 1) + bigText(960, 140, t, wt(i, /number/) - .1, nextStart(i), '#1 = SAN JOSÉ', 80, '#ffd166'),
  sfx: i => [{ k: 'impact', t: wt(i, /number/), g: .5 }, ...[0, 1, 2, 3, 4].map(j => ({ k: 'pop', t: wt(i, /five/) + j * .22 }))] };
SHOT.count_wall2 = { set: 'INT', light: 'indoorWarm',
  cam: i => mv(cm([IX + 2.4, 4.4, 9.4], [IX + 1.8, 2.2, 0], 50), cm([IX + 2.2, 4, 8.4], [IX + 1.8, 2.2, 0], 48)),
  upd: intUpd,
  figs: (t, i) => fig([IX + 5.4, 0, 3.4], 'sam', { mouth: 'o', talk: tk(t, i) * .7, blink: bl(t, 0), look: [-4, 4], prop: PROP.magnifier, hR: [190, 130] }),
  ui: (t, i) => { const P3 = [[/never/, '❓ NEVER FOUND', '#232838'], [/accident/, '🍀 FOUND BY ACCIDENT', '#35a862'], [/melted/, '🔥 ALMOST MELTED', '#e0303a']];
    return P3.map(([re, tx, bg], k) => pillAt(560, 260 + k * 130, t, wt(i, re) - .1, nextStart(i), tx, bg, '#fff', 50)).join('') },
  sfx: i => [{ k: 'pop', t: wt(i, /never/) }, { k: 'ding', t: wt(i, /accident/) }, { k: 'impact', t: wt(i, /melted/), g: .5 }] };
SHOT.outro = { set: 'INT', light: 'indoorWarm',
  cam: i => mv(cm([IX + 2.4, 5, 9.4], [IX + 1.6, 2, 0], 50), cm([IX + 2.2, 4.6, 8.6], [IX + 1.6, 2, 0], 50)),
  upd: intUpd,
  figs: (t, i) => fig([IX + 5.4, 0, 3.4], 'sam', { mouth: 'grin', talk: tk(t, i) * .8, blink: bl(t, 0), look: [-5, 2], hR: [214, 90 + 10 * Math.sin(t * 4)] }),
  ui: (t, i) => pinUI(t, Lt(i).start + .1, .1, 0) + bigText(960, 150, t, Lt(i).start + .2, 1e9, 'WHICH ONE WOULD YOU HUNT? 💬', 80) + pillAt(960, 270, t, wt(i, /subscribe/) - .1, 1e9, '🔔 SUBSCRIBE', '#e0303a', '#fff', 60),
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'ding', t: wt(i, /subscribe/) }] };
