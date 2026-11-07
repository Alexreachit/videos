// ---- PY: die Pyramide ----
const PY = {};
(function () {
  const S = 'PY', X = SETX.PY;
  ground(S, X, 0, 120, 90, '#f3e3b5');
  const back = new G.Geo(); for (let i = 0; i < 9; i++) back.add(G.box(14, 30, .5, i % 2 ? '#7cc6ff' : '#6bb8f5', { base: true }), cp([-63 + i * 14, 0, 0]));
  mk(S, back, { pos: [X, 0, 14], cast: false, outline: false });
  PY.N = [10, 15, 23, 34]; PY.tiers = []; PY.ppl = [];
  const TC = ['#ffd166', '#ffb347', '#ff8f6b', '#ef6f8f'];
  PY.N.forEach((n, k) => {
    const y = (3 - k) * .9, z = -k * 1.5, sp = .78, wd = n * sp + .8;
    const pl = mk(S, G.box(wd, .9, 1.5, TC[k], { base: true, top: '#fff3d6' }), { pos: [X, y - .9 + .0, z] });
    // Plattform reicht bis zum Boden
    const leg = mk(S, G.box(wd, Math.max(.01, y - .9 + .001), 1.5, TC[k], { base: true }), { pos: [X, 0, z], vis: y - .9 > .05 });
    PY.tiers.push({ pl, leg, y, z, k });
    for (let i = 0; i < n; i++) { const x = X + (i - (n - 1) / 2) * sp; const p = person(S, PCOL[(i * 3 + k) % PCOL.length], { pos: [x, y, z], yaw: Math.PI + (G.hash(i, k) - .5) * .3, s: .78, hat: ['cap', null, 'bun', 'boater', null, 'fedora'][(i + k) % 6] }); p.k = k; p.i = i; PY.ppl.push(p) }
  });
  PY.ped = mk(S, G.box(1.6, 3.6, 1.5, '#232838', { base: true, top: '#ffd166' }), { pos: [X, 0, 1.6] });
  PY.ponzi = mkPonzi(S, [X, 3.6, 1.6], Math.PI);
  PY.coins = []; const cg = G.cyl(.18, .18, .05, 16, '#ffc94a').smooth(); for (let i = 0; i < 40; i++) PY.coins.push(mk(S, cg, { emis: .25, cast: false }));
})();
// ---- MN: Villa in Lexington ----
const MN = {};
(function () {
  const S = 'MN', X = SETX.MN;
  ground(S, X, 0, 120, 90, '#7cc65f');
  ground(S, X, -4, 3, 22, '#e3d6bb', .03); ground(S, X + 7, -3, 10, 5, '#e3d6bb', .03);
  const h = new G.Geo().add(G.box(14, 6.4, 8, '#f3dc8e', { base: true })).add(G.cyl(10.2, 0, 3.2, 4, '#9a4b3a', { rot: Math.PI / 4 }), cp([0, 6.4, 0], [0, 0, 0], [1, 1, .62]))
    .add(G.box(4.4, 4.2, 2, '#f3dc8e', { base: true }), cp([0, 0, 4.4])).add(G.cyl(3.4, 0, 1.6, 4, '#9a4b3a', { rot: Math.PI / 4 }), cp([0, 4.2, 4.4], [0, 0, 0], [.9, 1, .7]))
    .add(G.box(1.2, 2.4, .2, '#ffffff', { base: true }), cp([0, 0, 5.42])).add(G.box(.9, 2, .1, '#5a3a22', { base: true }), cp([0, 0, 5.5]))
    .add(G.box(1.2, 1.6, 1.2, '#b9b0a0', { base: true }), cp([4.5, 7.2, -1]));
  MN.house = mk(S, h, { pos: [X, 0, 8], rot: [0, Math.PI, 0] });
  const wins = texMesh(S, 13.6, 6, facadeTex('#f3dc8e', 2, 5), { parent: MN.house, pos: [0, 3.1, 4.03] });
  MN.lit = []; for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) { if (c == 1 || c == 2) { if (r == 0) continue } MN.lit.push(mk(S, G.box(1.2, 1.4, .05, '#ffe08a', { base: true }), { parent: MN.house, pos: [-5 + c * 3.33 + (c > 1 ? 0 : 0), .9 + r * 3, 4.06], emis: 1, vis: false, cast: false, outline: false })) }
  [[-11, 2, 1.3], [11, 3, 1.2], [-14, 10, 1.6], [15, 9, 1.5], [-7, -6, .9], [8, -8, 1]].forEach(([dx, dz, s]) => tree(S, X + dx, dz, s));
  for (let i = 0; i < 10; i++) mk(S, G.ico(.55, 2, '#4f9f45', .15, i, .8).smooth(), { pos: [X - 6.5 + (i % 5) * 1.0 + (i > 4 ? 9 : 0), .4, 3.2] });
  MN.car = car(S, X + 6, -3, Math.PI * .92, '#7a1f2b');
  MN.ponzi = mkPonzi(S, [X + 3.6, 0, -2.4], -.6);
  MN.mom = person(S, '#7a55c7', { pos: [X + 4.6, 0, -1.6], yaw: -1.4, hat: 'bun', hatc: '#d9d9d9', s: .9 });
  MN.coins = []; const cg = G.cyl(.25, .25, .06, 16, '#ffc94a').smooth(); for (let i = 0; i < 26; i++) MN.coins.push(mk(S, cg, { emis: .3, cast: false }));
})();
// ---- VT: Geldraum ----
const VT = {};
(function () {
  const S = 'VT', X = SETX.VT;
  room(S, X, 0, 14, 12, 7, '#e9d6a6', '#c9a46a', { wall2: '#e0c993' });
  mk(S, G.cyl(2.4, 2.4, .5, 32, '#9aa3b5').smooth().add(G.cyl(.5, .5, .7, 16, '#5d6680').smooth(), cp([0, .3, 0])), { pos: [X + 3.5, 3, 5.6], rot: [Math.PI / 2, 0, 0] });
  // Geldstapel: viele Buendel, Anzahl sichtbar per Fortschritt
  VT.bricks = []; const bg = G.box(.9, .32, .45, '#6fbf73', { base: true }).add(G.box(.18, .33, .46, '#f4efe2', { base: true }), cp([0, 0, 0]));
  for (let i = 0; i < 150; i++) { const col = i % 30, layer = Math.floor(i / 30); const px = X - 5.2 + (col % 10) * .95 + (layer % 2) * .1 + layer * .25, pz = 1.2 + Math.floor(col / 10) * .5 + layer * .2;
    VT.bricks.push(mk(S, bg, { pos: [px, layer * .33, pz], rot: [0, (G.hash(i, 2) - .5) * .2, 0], vis: false })) }
  VT.bills = []; const bl = G.box(.55, .02, .26, '#7bc47f', { base: true }); for (let i = 0; i < 60; i++) VT.bills.push(mk(S, bl, { cast: false, outline: false }));
  VT.ponzi = mkPonzi(S, [X + 1.8, 0, 1.4], -.5);
})();
// ---- SW: Florida-Sumpf ----
const SW = {};
(function () {
  const S = 'SW', X = SETX.SW;
  ground(S, X, 0, 120, 90, '#7a9a4f');
  const g = new G.Geo(), k = G.hex('#4f7a5a'); for (let i = 0; i < 40; i++) for (let j = 0; j < 30; j++) { const P = (a, b) => [X - 30 + a * 1.5, .05, -14 + b * 1.2]; g.quad(P(i, j), P(i, j + 1), P(i + 1, j + 1), P(i + 1, j), k) }
  mk(S, g, { wave: .05, cast: false, water: 1, spec: .3, pos: [0, 0, 0] });
  for (let i = 0; i < 14; i++) mk(S, G.ico(1.6, 2, '#86a85a', .2, i, .25).smooth(), { pos: [X - 20 + G.hash(i, 1) * 40, 0, -8 + G.hash(i, 2) * 26] });
  const reeds = new G.Geo(); for (let i = 0; i < 120; i++) reeds.add(G.cyl(.04, .01, 1.2 + G.hash(i, 3), 4, i % 2 ? '#5b7f36' : '#6f9a40'), cp([(G.hash(i, 4) - .5) * 40, 0, (G.hash(i, 5) - .5) * 26], [(G.hash(i, 6) - .5) * .4, 0, (G.hash(i, 7) - .5) * .4]));
  mk(S, reeds, { pos: [X, 0, 0], cast: false });
  [[-8, 6], [9, 7], [-14, 2], [14, -3], [3, 10]].forEach(([dx, dz]) => { mk(S, G.cyl(.4, .2, 5, 8, '#7a5a3c'), { pos: [X + dx, 0, dz] }); mk(S, G.ico(1.8, 2, '#4f7a3a', .2, dx, .5).smooth(), { pos: [X + dx, 5, dz] }) });
  SW.sign = mk(S, G.cyl(.1, .1, 3, 6, '#7a5a3c').add(G.cyl(.1, .1, 3, 6, '#7a5a3c'), cp([2.6, 0, 0])), { pos: [X - 1.3, 0, 2] });
  signMesh(S, null, [X, 2.3, 1.85], 3.4, 1.7, [['LAND FOR SALE!', '900 92px IB, P, Arial'], ['200% IN 60 DAYS', '900 80px IB, P, Arial']], '#ffd166', '#232838', { border: '#232838', mo: { rot: [0, Math.PI, 0] } });
  SW.ponzi = mkPonzi(S, [X + 2.4, 0, 1.2], Math.PI + .3);
  SW.gator = mk(S, new G.Geo().add(G.box(2.4, .3, .6, '#3f6a3a', { base: true })).add(G.ico(.12, 1, '#f4efe2'), cp([.9, .32, .2])).add(G.ico(.12, 1, '#f4efe2'), cp([.9, .32, -.2])).add(G.ico(.05, 1, OL), cp([.98, .36, .2])).add(G.ico(.05, 1, OL), cp([.98, .36, -.2])), { pos: [X - 4, -.12, -3], rot: [0, -.4, 0] });
  SW.buyers = [person(S, '#2a8fd6', { pos: [X + 4.2, 0, -.4], yaw: Math.PI * 1.2, hat: 'boater' }), person(S, '#e09a2b', { pos: [X + 5.3, 0, .2], yaw: Math.PI * 1.25, hat: 'bun' })];
})();
// ---- RIO: Krankenhauszimmer mit Blick aufs Meer ----
const RIO = {};
(function () {
  const S = 'RIO', X = SETX.RIO;
  ground(S, X, 0, 12, 10, '#e9e4da');
  mk(S, G.box(.3, 5, 10, '#dfe9e6', { base: true }), { pos: [X - 6, 0, 0] }); mk(S, G.box(.3, 5, 10, '#dfe9e6', { base: true }), { pos: [X + 6, 0, 0] });
  // Rueckwand mit grossem Fenster (vier Teile)
  mk(S, G.box(12, 1.2, .3, '#dfe9e6', { base: true }), { pos: [X, 0, 5] }); mk(S, G.box(12, 1, .3, '#dfe9e6', { base: true }), { pos: [X, 4, 5] });
  mk(S, G.box(3, 5, .3, '#dfe9e6', { base: true }), { pos: [X - 4.5, 0, 5] }); mk(S, G.box(3, 5, .3, '#dfe9e6', { base: true }), { pos: [X + 4.5, 0, 5] });
  mk(S, G.box(.12, 2.8, .32, '#ffffff', { base: true }), { pos: [X, 1.2, 5] });
  const sea = new G.Geo(), k = G.hex('#2b9fd8'); for (let i = 0; i < 30; i++) for (let j = 0; j < 20; j++) { const P = (a, b) => [X - 60 + a * 4, -1, 8 + b * 4]; sea.quad(P(i, j), P(i, j + 1), P(i + 1, j + 1), P(i + 1, j), k) } mk(S, sea, { wave: .1, cast: false, water: 1 });
  mk(S, G.ico(9, 3, '#5f9a4f', .15, 3, 1.6).smooth(), { pos: [X + 10, -2, 60], cast: false }); mk(S, G.ico(6, 3, '#6aa857', .1, 5, 1.2).smooth(), { pos: [X - 14, -2, 52], cast: false }); mk(S, G.ico(12, 3, '#4f8a45', .12, 7, .7).smooth(), { pos: [X - 30, -2, 70], cast: false });
  mk(S, G.box(2.4, .6, 4.6, '#d9d9d9', { base: true }).add(G.box(2.3, .3, 4.5, '#ffffff', { base: true }), cp([0, .6, 0])).add(G.box(2.4, 1.4, .15, '#c9ced8', { base: true }), cp([0, 0, 2.3])).add(G.box(1.4, .25, .9, '#ffffff', { base: true }), cp([0, .9, 1.6])), { pos: [X - 2, 0, 1.2] });
  RIO.hat = mk(S, G.cyl(.46, .46, .035, 24, DARK).smooth().add(G.cyl(.27, .24, .3, 20, DARK).smooth(), cp([0, .02, 0])).add(G.cyl(.275, .275, .06, 20, '#55597a'), cp([0, .03, 0])), { pos: [X - 1.8, .92, 0], rot: [0, .4, .05] });
  mk(S, G.box(1, 1, 1, '#c9a46a', { base: true }), { pos: [X + .6, 0, 2.6] });
  RIO.coins = []; const cg = G.cyl(.14, .14, .04, 14, '#ffc94a').smooth(); for (let i = 0; i < 6; i++) RIO.coins.push(mk(S, cg, { pos: [X + .45 + (i % 3) * .18, 1.02 + Math.floor(i / 3) * .045, 2.5 + (i % 2) * .15] }));
})();
// ---- STU: Studio fuer Sam ----
const STU = {};
(function () {
  const S = 'STU', X = SETX.STU;
  ground(S, X, 0, 60, 40, '#ffe7a8');
  const bg = new G.Geo(); for (let i = 0; i < 24; i++) { const a0 = Math.PI * (.15 + .7 * i / 24), a1 = Math.PI * (.15 + .7 * (i + 1) / 24); const P = (a, y) => [Math.cos(a) * -16, y, Math.sin(a) * 16 - 4]; bg.quad(P(a0, 0), P(a0, 14), P(a1, 14), P(a1, 0), G.hex(i % 2 ? '#7cc6ff' : '#69b9f8')) }
  mk(S, bg, { pos: [X, 0, 0], cast: false, outline: false, recv: false });
  for (let i = 0; i < 10; i++) mk(S, G.ico(.4 + G.hash(i, 1) * .6, 2, ['#ffd166', '#ff8f6b', '#7ee08a', '#ffffff'][i % 4]).smooth(), { pos: [X - 9 + i * 2, 2 + G.hash(i, 2) * 6, 8 + G.hash(i, 3) * 2], emis: .3, cast: false });
  STU.ped = mk(S, G.ico(2.4, 3, '#ffffff', 0, 1, .14).smooth(), { pos: [X, 0, 0], outline: false, vis: false });
})();
// ---- CT: Gericht ----
const CT = {};
(function () {
  const S = 'CT', X = SETX.CT;
  room(S, X, 0, 16, 12, 7, '#d9b98a', '#8a5a3c', { wall2: '#cfae7f' });
  mk(S, G.box(6, 2.4, 1.6, '#6b4226', { base: true }).add(G.box(6.4, .2, 1.9, '#5a3418', { base: true }), cp([0, 2.4, 0])), { pos: [X, 0, 3.6] });
  CT.judge = person(S, '#232838', { pos: [X, .9, 4.6], yaw: Math.PI, hat: 'bun', hatc: '#f4efe2', leg: '#232838' });
  CT.gavel = mk(S, G.cyl(.04, .04, .7, 6, '#5a3418').add(G.cyl(.14, .14, .4, 10, '#5a3418').smooth(), cp([-.2, .7, 0], [0, 0, Math.PI / 2])), { pos: [X + .8, 2.6, 3.2] });
  for (let i = 0; i < 2; i++) mk(S, G.box(5, 1, .8, '#6b4226', { base: true }), { pos: [X + (i ? 4 : -4), 0, -2.5] });
  CT.ponzi = mkPonzi(S, [X, 0, 1.2], 0);
  signMesh(S, null, [X, 5.3, 5.82], 4, 1, [['COURT']], '#5a3418', '#ffd166', { mo: { rot: [0, Math.PI, 0] } });
  CT.cops = [person(S, '#2c3e70', { pos: [X - 1.4, 0, .8], yaw: .3, hat: 'cap', hatc: '#1d2a52', leg: '#1d2a52' }), person(S, '#2c3e70', { pos: [X + 1.4, 0, .8], yaw: -.3, hat: 'cap', hatc: '#1d2a52', leg: '#1d2a52' })];
})();
