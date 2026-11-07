// ===================== YT14 Ponzi – 3D-Welt (gl3d Toon) =====================
const W = 1920, H = 1080, G = GL3D, {cl, ez, ei, bo, el, lerp} = MG;
const $ = id => document.getElementById(id);
const OL = '#232838', SKIN = '#f7e4b5', DARK = '#262a40';
const w = G.World($('cv'), W, H, 2);
w.toon = true; w.rim = .34; w.outline = .0016;
w.fog = G.hex('#dff3ff'); w.fogN = 70; w.fogF = 210; w.sky = G.hex('#d6efff'); w.gnd = G.hex('#c9b591');
w.sun = G.v.norm([.45, .8, -.38]); w.shadowSize = 30;
const SETX = { ST: 0, HB: -220, DN: -110, BK: 110, PR: 220, DK: 330, PY: 440, MN: 550, VT: 660, SW: 770, RIO: 880, STU: 990, CT: 1100 };
const SETM = {}; let CUR = null;
function mk(set, g, o = {}) {
  const m = w.mesh(g, o); (SETM[set] || (SETM[set] = [])).push(m); m._v = o.vis ?? true; return m;
}
const cp = G.m4.compose;
function tex(wd, ht, fn) { const c = document.createElement('canvas'); c.width = wd; c.height = ht; fn(c.getContext('2d'), wd, ht); return w.texture(c) }
const TEXQ = []; // Texturen erst nach dem Laden der Schriften bauen
function texMesh(set, wd, ht, fn, o) { const m = mk(set, G.plane(wd, ht, 1, 1, '#ffffff'), Object.assign({ outline: false, cast: false }, o)); TEXQ.push(() => m.tex = fn()); return m }
function txt(x, s, X, Y, font, col, o = {}) {
  x.font = font; x.textAlign = o.al || 'center'; x.textBaseline = 'middle';
  if (o.stroke) { x.lineWidth = o.stroke; x.strokeStyle = o.sc || OL; x.lineJoin = 'round'; x.strokeText(s, X, Y) }
  x.fillStyle = col; x.fillText(s, X, Y);
}
// ---------- Figuren ----------
const PCOL = ['#d64545', '#2fa36b', '#e09a2b', '#7a55c7', '#2a8fd6', '#e05d9a', '#3c4a63', '#c7a32f', '#1f9e9e', '#8a5a3c'];
function person(set, col, o = {}) {
  const sk = o.dark ? DARK : SKIN, leg = o.dark ? '#1c1f30' : (o.leg || '#5a3d2a');
  const g = new G.Geo();
  g.add(G.cyl(.09, .08, .5, 8, leg), cp([-.11, 0, 0])).add(G.cyl(.09, .08, .5, 8, leg), cp([.11, 0, 0]));
  g.add(G.cyl(.27, .23, .55, 18, col).smooth(), cp([0, .45, 0]));
  if (o.tie) g.add(G.box(.07, .3, .02, o.tie, { base: true }), cp([0, .66, .245]));
  const hg = new G.Geo().add(G.ico(.33, 3, sk).smooth(), cp([0, .3, 0]));
  if (!o.dark) hg.add(G.ico(.042, 2, OL), cp([-.1, .34, .3])).add(G.ico(.042, 2, OL), cp([.1, .34, .3])).add(G.box(.13, .025, .02, OL), cp([0, .2, .315]));
  if (o.hat == 'fedora') hg.add(G.cyl(.46, .46, .035, 24, o.hatc || DARK).smooth(), cp([0, .5, 0])).add(G.cyl(.27, .24, .3, 20, o.hatc || DARK).smooth(), cp([0, .52, 0])).add(G.cyl(.275, .275, .06, 20, '#55597a'), cp([0, .53, 0]));
  if (o.hat == 'cap') hg.add(G.cyl(.31, .3, .16, 20, o.hatc || '#2c3e70').smooth(), cp([0, .5, 0])).add(G.box(.34, .03, .2, '#1b1f33', { base: true }), cp([0, .5, .3]));
  if (o.hat == 'boater') hg.add(G.cyl(.44, .44, .03, 24, '#f2d58a').smooth(), cp([0, .5, 0])).add(G.cyl(.26, .26, .18, 20, '#f2d58a').smooth(), cp([0, .52, 0])).add(G.cyl(.265, .265, .05, 20, '#2b2f45'), cp([0, .57, 0]));
  if (o.hat == 'bun') hg.add(G.ico(.16, 2, o.hatc || '#6b4226').smooth(), cp([0, .62, -.12]));
  const s = o.s || 1;
  const body = mk(set, g, { pos: o.pos || [0, 0, 0], rot: [0, o.yaw || 0, 0], scl: [s, s, s] });
  const head = mk(set, hg, { parent: body, pos: [0, .97, 0] });
  const arm = c => new G.Geo().add(G.cyl(.075, .065, .4, 12, c).smooth(), cp([0, -.4, 0])).add(G.ico(.085, 2, sk).smooth(), cp([0, -.45, 0]));
  const aL = mk(set, arm(col), { parent: body, pos: [-.27, .92, 0], rot: [0, 0, -.12] });
  const aR = mk(set, arm(col), { parent: body, pos: [.27, .92, 0], rot: [0, 0, .12] });
  return { m: body, head, aL, aR, s, base: [...(o.pos || [0, 0, 0])], yaw: o.yaw || 0, ph: G.hash(body.n || 1, (o.pos || [0])[0]) * 6.28 + Math.random() * 0 };
}
function pose(p, t, k = 'idle', amt = 1) {
  const ph = p.ph; let hop = 0, aL = -.12 - .04 * Math.sin(t * 2 + ph), aR = .12 + .04 * Math.sin(t * 2 + ph), ax = 0, axR = 0, hx = 0, hy = .12 * Math.sin(t * .7 + ph);
  if (k == 'cheer') { hop = Math.max(0, Math.sin(t * 7 + ph)) * .25 * amt; const wv = Math.sin(t * 10 + ph) * .35; aL = -2.5 - wv; aR = 2.5 + wv }
  if (k == 'wave') { aR = 2.4 + Math.sin(t * 9 + ph) * .4 }
  if (k == 'scared') { aL = -1.5; aR = 1.5; ax = -1.2; axR = -1.2; hx = -.15; hop = Math.abs(Math.sin(t * 22 + ph)) * .03 }
  if (k == 'sad') { hx = .35; aL = -.05; aR = .05; hy = 0 }
  if (k == 'angry') { const sh = Math.sin(t * 13 + ph); aL = -2.4 - sh * .3; aR = .3; hop = Math.abs(sh) * .06 }
  if (k == 'give') { axR = -1.2; aR = .25 }
  if (k == 'walk') { const f = Math.sin(t * 8 + ph); ax = f * .6; axR = -f * .6; hop = Math.abs(f) * .05 }
  if (k == 'push') { ax = -1.5; axR = -1.5; aL = -.2; aR = .2; hop = Math.abs(Math.sin(t * 12 + ph)) * .08 }
  if (k == 'fall') { }
  p.m.pos = [p.base[0], p.base[1] + hop, p.base[2]]; p.m.rot = [0, p.yaw, .04 * Math.sin(t * 1.3 + ph)];
  p.head.rot = [hx, hy, 0]; p.aL.rot = [ax, 0, aL]; p.aR.rot = [axR, 0, aR];
}
// Ponzi: gesichtslose Silhouette mit Hut (keine Darstellung der realen Person)
const PZ = {};
function mkPonzi(set, pos, yaw) { const p = person(set, '#2f3350', { dark: true, hat: 'fedora', s: 1.08, pos, yaw }); p.m.emis = 0; return p }
// ---------- Bausteine ----------
const BRICK = ['#c4573e', '#b4634a', '#d0794f', '#a8513f', '#c98a5a', '#9c5a48', '#d9a066'];
function facadeTex(col, rows, cols, o = {}) {
  return () => tex(512, 512, (x, wd, ht) => {
    x.fillStyle = col; x.fillRect(0, 0, wd, ht);
    x.fillStyle = '#00000018'; for (let r = 0; r < 64; r++) for (let c = 0; c < 18; c++) if ((r * 7 + c * 3) % 5 == 0) x.fillRect(c * 32 + (r % 2) * 16, r * 8, 28, 6);
    const ww = wd / cols, hh = (ht - (o.shop ? 150 : 40)) / rows;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const X = c * ww + ww * .22, Y = 30 + r * hh + hh * .14, WW = ww * .56, HH = hh * .66;
      x.fillStyle = '#efe6d2'; x.fillRect(X - 7, Y - 7, WW + 14, HH + 14);
      x.fillStyle = (r + c) % 3 ? '#7fb6d9' : '#a8d4ee'; x.fillRect(X, Y, WW, HH);
      x.fillStyle = '#ffffff66'; x.beginPath(); x.moveTo(X, Y + HH * .6); x.lineTo(X + WW * .5, Y); x.lineTo(X + WW * .75, Y); x.lineTo(X, Y + HH); x.fill();
      x.fillStyle = '#efe6d2'; x.fillRect(X + WW / 2 - 3, Y, 6, HH); x.fillRect(X, Y + HH / 2 - 3, WW, 6);
    }
    if (o.shop) { x.fillStyle = o.shop; x.fillRect(0, ht - 150, wd, 150); x.fillStyle = '#a8d4ee'; x.fillRect(40, ht - 120, 150, 110); x.fillRect(wd - 190, ht - 120, 150, 110); x.fillStyle = '#5a3a22'; x.fillRect(wd / 2 - 50, ht - 135, 100, 135); x.fillStyle = '#ffd166'; x.beginPath(); x.arc(wd / 2 + 30, ht - 65, 6, 0, 7); x.fill() }
    x.fillStyle = '#00000022'; x.fillRect(0, 0, wd, 10);
  });
}
function building(set, x, z, bw, bh, bd, col, o = {}) {
  const yaw = o.yaw || 0, g = new G.Geo().add(G.box(bw, bh, bd, col, { base: true })).add(G.box(bw + .4, .35, bd + .4, '#e9dfc9', { base: true }), cp([0, bh, 0]));
  if (o.roof) g.add(G.box(bw * .3, 1.2, bd * .3, '#7a4a3a', { base: true }), cp([bw * .25, bh + .35, 0]));
  const b = mk(set, g, { pos: [x, 0, z], rot: [0, yaw, 0] });
  const f = texMesh(set, bw * .98, bh * .98, facadeTex(col, o.rows || 3, o.cols || 3, { shop: o.shop }), { parent: b, pos: [0, bh / 2, bd / 2 + .02] });
  return b;
}
function signMesh(set, parent, pos, sw, sh, lines, bg, fg, o = {}) {
  return texMesh(set, sw, sh, () => tex(1024, Math.round(1024 * sh / sw), (x, wd, ht) => {
    x.fillStyle = bg; x.fillRect(0, 0, wd, ht); x.strokeStyle = o.border || '#ffd166'; x.lineWidth = 14; x.strokeRect(12, 12, wd - 24, ht - 24);
    lines.forEach((l, i) => txt(x, l[0], wd / 2, ht * (lines.length == 1 ? .54 : (i + .7) / (lines.length + .4)), l[1] || `900 ${Math.round(ht * .42)}px IB, P, Arial`, fg));
  }), Object.assign({ parent, pos, emis: o.emis || 0 }, o.mo || {}));
}
function lamp(set, x, z) { mk(set, G.cyl(.08, .06, 3.6, 8, '#2b2f45').add(G.box(.5, .08, .08, '#2b2f45'), cp([.2, 3.5, 0])), { pos: [x, 0, z] }); mk(set, G.ico(.2, 2, '#fff1b8').smooth(), { pos: [x + .42, 3.32, z], emis: .9, outline: false }) }
function car(set, x, z, yaw, col = '#232838') {
  const g = new G.Geo().add(G.box(2.6, .55, 1.3, col, { base: true }), cp([0, .45, 0])).add(G.box(1.2, .75, 1.2, col, { base: true }), cp([-.45, 1.0, 0]))
    .add(G.box(1.0, .5, 1.24, '#a8d4ee', { base: true }), cp([-.45, 1.12, 0])).add(G.box(.9, .45, 1.1, col, { base: true }), cp([.9, .95, 0]))
    .add(G.box(.08, .4, .9, '#d8d8d8', { base: true }), cp([1.33, .55, 0]));
  [[-.85, .7], [.85, .7], [-.85, -.7], [.85, -.7]].forEach(([dx, dz]) => g.add(G.cyl(.36, .36, .2, 16, '#14161f', { cap: '#c9c9c9' }).smooth(), cp([dx, .36, dz - (dz > 0 ? .1 : -.1)], [Math.PI / 2, 0, 0])));
  return mk(set, g, { pos: [x, 0, z], rot: [0, yaw, 0] });
}
function tree(set, x, z, s = 1) { mk(set, G.cyl(.18 * s, .14 * s, 1.6 * s, 8, '#8a5a3c'), { pos: [x, 0, z] }); mk(set, G.ico(1.1 * s, 2, '#5fb24c', .12, x * 3 + z, .9).smooth(), { pos: [x, 2.2 * s, z] }) }
function ground(set, x, z, sx, sz, col, y = 0) { return mk(set, G.box(sx, .2, sz, col, { base: true }).vary(.03, x + z), { pos: [x, y - .2, z], cast: false, outline: false }) }
function room(set, x, z, rw, rd, rh, wall, floor, o = {}) {
  ground(set, x, z, rw, rd, floor);
  mk(set, G.box(rw, rh, .3, wall, { base: true }), { pos: [x, 0, z + rd / 2], cast: false });
  mk(set, G.box(.3, rh, rd, o.wall2 || wall, { base: true }), { pos: [x - rw / 2, 0, z], cast: false });
  mk(set, G.box(.3, rh, rd, o.wall2 || wall, { base: true }), { pos: [x + rw / 2, 0, z], cast: false });
}
