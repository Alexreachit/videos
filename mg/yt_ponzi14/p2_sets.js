// ===================== Sets =====================
// ---- ST: Boston, School Street ----
const ST = {};
(function () {
  const S = 'ST';
  ground(S, 0, 0, 120, 10.2, '#a39d92'); ground(S, 0, 6.6, 120, 3.2, '#ddd3c2', .14); ground(S, 0, -6.6, 120, 3.2, '#ddd3c2', .14);
  ground(S, 0, 40, 160, 60, '#cfc6b4', -.01); ground(S, 0, -40, 160, 60, '#cfc6b4', -.01);
  // Strassenmarkierung / Pflaster-Fugen
  const lines = new G.Geo(); for (let x = -58; x < 58; x += 1.6) lines.add(G.box(.05, .02, 10, '#8f897f', { base: true }), cp([x, 0, 0])); mk(S, lines, { cast: false, outline: false });
  // Nordseite (Fassaden schauen nach -z)
  const N = [[-25.5, 8, 10, 4], [-17.5, 8, 7.5, 1], [-9, 9, 11, 2], [0, 8.4, 9, 0], [9, 9, 12, 5], [17.5, 8, 8, 6], [25.5, 8, 10.5, 3]];
  N.forEach(([x, bw, bh, ci], i) => { const b = building(S, x, 12, bw - .2, bh, 8, BRICK[ci], { yaw: Math.PI, rows: Math.round(bh / 3.2), cols: 3, shop: i == 3 ? '#2f5d4a' : ['#3b6ea5', '#8a4b2a', '#6b4f8a', '', '#2f6f6a', '#9a3b3b', '#4a6a2a'][i] }); if (i == 3) ST.office = b });
  ST.sign = signMesh(S, ST.office, [0, 2.7, 4.07], 7.4, 1.0, [['SECURITIES EXCHANGE CO.']], '#1f4a3a', '#ffd166', { emis: .05 });
  ST.banner = signMesh(S, ST.office, [0, 4.9, 4.1], 6.6, 1.5, [['50% PROFIT', '900 92px IB, P, Arial'], ['IN 45 DAYS', '900 92px IB, P, Arial']], '#e8483c', '#ffffff', { border: '#ffffff' });
  // Suedseite (Fassaden schauen nach +z), Hanover Trust
  const Sd = [[-24, 9, 9, 2], [-14, 10, 12, 0], [-4, 9, 8, 5], [6, 8, 10, 3], [26, 9, 9, 1]];
  Sd.forEach(([x, bw, bh, ci], i) => building(S, x, -12, bw - .2, bh, 8, BRICK[ci], { rows: Math.round(bh / 3.2), cols: 3, shop: ['#3b6ea5', '#8a4b2a', '#2f6f6a', '#9a3b3b', '#4a6a2a'][i] }));
  const hx = 15.5, hb = mk(S, new G.Geo().add(G.box(9.6, 8, 8, '#e8e0cc', { base: true })).add(G.box(10.4, .6, 8.6, '#d9cfb5', { base: true }), cp([0, 8, 0])).add(G.box(10.4, .5, 8.8, '#d9cfb5', { base: true })), { pos: [hx, 0, -12] });
  for (let i = 0; i < 4; i++) mk(S, G.cyl(.35, .32, 6.2, 16, '#f4efe2').smooth(), { pos: [hx - 3.3 + i * 2.2, .5, -7.6] });
  mk(S, G.box(10.4, 1.2, 1.2, '#efe7d4', { base: true }), { pos: [hx, 6.7, -7.6] });
  ST.hsign = signMesh(S, null, [hx, 7.3, -6.95], 7.6, .95, [['HANOVER TRUST']], '#efe7d4', '#3a3f5c', { border: '#c8b98f' });
  ST.hdoor = mk(S, G.box(2.2, 3.2, .1, '#5a3a22', { base: true }), { pos: [hx, .5, -7.95] });
  ST.closed = mk(S, new G.Geo().add(G.box(3.2, .3, .08, '#c98c50', { base: true }), cp([0, 0, 0], [0, 0, .6])).add(G.box(3.2, .3, .08, '#c98c50', { base: true }), cp([0, 1.9, 0], [0, 0, -.6])), { pos: [hx - .1, 1.2, -7.85], vis: false });
  ST.closedSign = signMesh(S, null, [hx, 3.0, -7.78], 2.6, .8, [['CLOSED']], '#ffffff', '#e8483c', { border: '#e8483c', mo: { vis: false } });
  for (let x = -40; x <= 40; x += 8) { lamp(S, x + 2, 5.25); lamp(S, x - 2, -5.25) }
  ST.cars = [car(S, -12, 3.2, 0, '#232838'), car(S, 22, -3.4, Math.PI, '#2f5d4a'), car(S, -30, -3.4, Math.PI, '#6b2b2b')];
  // Schlange vor dem Buero (Blick Richtung Tuer = -x)
  ST.queue = []; for (let i = 0; i < 44; i++) { const row = i % 2, x = 1.6 + Math.floor(i / 2) * .95 + row * .45, z = 5.75 + row * .8;
    ST.queue.push(person(S, PCOL[i % PCOL.length], { pos: [x, .14, z], yaw: -Math.PI / 2 + (G.hash(i, 2) - .5) * .3, hat: ['fedora', 'cap', 'boater', 'bun', null][i % 5], hatc: ['#5b4636', '#3c4a63', '#6b4226', '#2b2f45'][i % 4], tie: i % 3 == 0 ? '#e8483c' : null, s: .95 + .1 * G.hash(i, 5) })) }
  ST.crowd = []; for (let i = 0; i < 30; i++) { const x = -6 + (i % 10) * 1.3 + (G.hash(i, 3) - .5) * .5, z = 1.4 + Math.floor(i / 10) * 1.25 + (G.hash(i, 4) - .5) * .4;
    ST.crowd.push(person(S, PCOL[(i + 3) % PCOL.length], { pos: [x, 0, z], yaw: (G.hash(i, 6) - .5) * .5, hat: ['cap', 'fedora', 'bun', 'boater', null][i % 5], s: .95 + .1 * G.hash(i, 8) })) }
  ST.newsboy = person(S, '#e09a2b', { pos: [-6.5, .14, 5.6], yaw: -.4, hat: 'cap', hatc: '#6b4226', s: .82 });
  ST.paper = texMesh(S, .7, .9, () => tex(256, 330, (x, wd, ht) => { x.fillStyle = '#f4eedf'; x.fillRect(0, 0, wd, ht); txt(x, 'BOSTON POST', wd / 2, 34, '900 30px IB, Arial', '#232838'); x.fillStyle = '#232838'; x.fillRect(16, 60, wd - 32, 6); txt(x, 'PONZI?', wd / 2, 110, '900 56px IB, Arial', '#c0392b'); for (let i = 0; i < 9; i++) { x.fillStyle = '#9a9384'; x.fillRect(20, 160 + i * 17, wd - 40 - (i % 3) * 30, 8) } }), { parent: ST.newsboy.aR, pos: [0, -.55, .18], rot: [-.2, 0, 0] });
  ST.cops = [person(S, '#2c3e70', { pos: [-1.2, .14, 6.0], yaw: 0, hat: 'cap', hatc: '#1d2a52', leg: '#1d2a52', vis: false }), person(S, '#2c3e70', { pos: [1.2, .14, 6.0], yaw: 0, hat: 'cap', hatc: '#1d2a52', leg: '#1d2a52' })];
  PZ.ST = mkPonzi(S, [0, .14, 7.2], 0);
  // Geldscheine (Bank-Run / Regen)
  ST.bills = []; const bg = G.box(.5, .02, .24, '#7bc47f', { base: true }); for (let i = 0; i < 30; i++) ST.bills.push(mk(S, bg, { cast: false, outline: false }));
})();
// ---- HB: Hafen 1903 ----
const HB = {};
(function () {
  const S = 'HB', X = SETX.HB;
  const g = new G.Geo(), k = G.hex('#2b9fd8'); for (let i = 0; i < 70; i++) for (let j = 0; j < 70; j++) { const P = (a, b) => [X - 100 + a * 200 / 70, -.3, -60 + b * 160 / 70]; g.quad(P(i, j), P(i, j + 1), P(i + 1, j + 1), P(i + 1, j), k) }
  mk(S, g, { wave: .18, cast: false, water: 1, spec: .4 });
  ground(S, X, 20, 200, 20, '#cfc6b4', .3); // Kai
  mk(S, G.box(30, .5, 6, '#9c6d43', { base: true }).vary(.05, 3), { pos: [X, 0, 8] });
  for (let i = 0; i < 8; i++) mk(S, G.cyl(.25, .25, 1.4, 10, '#7a5230'), { pos: [X - 13 + i * 3.7, -.9, 5.2] });
  [[-14, 9, 7, 2], [-4, 11, 9, 0], [7, 9, 6, 4], [17, 10, 8, 1]].forEach(([dx, bw, bh, ci]) => building(S, X + dx, 26, bw, bh, 8, BRICK[ci], { yaw: Math.PI, rows: 2, cols: 3 }));
  for (let i = 0; i < 6; i++) { const c = mk(S, G.box(1, 1, 1, ['#c98c50', '#8a5a3c', '#a8703f'][i % 3], { base: true }), { pos: [X - 8 + i * 1.2 + (i > 2 ? 3 : 0), .5, 9 + (i % 2) * 1.1] }) }
  const sh = new G.Geo().add(G.box(22, 3, 5, '#2b2f45', { base: true }), cp([0, 0, 0])).add(G.box(22.2, .9, 5.1, '#c0392b', { base: true }), cp([0, -.2, 0]))
    .add(G.box(14, 2.2, 4, '#f4efe2', { base: true }), cp([0, 3, 0])).add(G.box(9, 1.6, 3.4, '#f4efe2', { base: true }), cp([.5, 5.2, 0]))
    .add(G.cyl(.75, .75, 3.6, 18, '#e8483c').smooth(), cp([-2.2, 6.6, 0])).add(G.cyl(.78, .78, .9, 18, '#232838').smooth(), cp([-2.2, 9.6, 0]))
    .add(G.cyl(.75, .75, 3.6, 18, '#e8483c').smooth(), cp([2.6, 6.6, 0])).add(G.cyl(.78, .78, .9, 18, '#232838').smooth(), cp([2.6, 9.6, 0]))
    .add(G.cyl(.08, .08, 7, 6, '#5a3a22'), cp([-9, 3, 0])).add(G.cyl(.08, .08, 6, 6, '#5a3a22'), cp([8.5, 3, 0]));
  for (let i = 0; i < 9; i++) sh.add(G.cyl(.25, .25, .05, 12, '#2b2f45'), cp([-6 + i * 1.5, 4.1, -2.02], [Math.PI / 2, 0, 0]));
  for (let i = 0; i < 9; i++) sh.add(G.cyl(.25, .25, .05, 12, '#a8d4ee'), cp([-6 + i * 1.5, 4.1, -2.05], [Math.PI / 2, 0, 0]));
  HB.ship = mk(S, sh, { pos: [X + 4, -.6, 1] });
  HB.smoke = []; for (let i = 0; i < 10; i++) HB.smoke.push(mk(S, G.ico(.6, 2, '#eef1f6', .2, i).smooth(), { cast: false, outline: false }));
  HB.ponzi = mkPonzi(S, [X, .5, 8.5], Math.PI);
  HB.case = mk(S, G.box(.5, .36, .18, '#8a5a3c', { base: true }), { parent: HB.ponzi.aR, pos: [0, -.75, 0] });
  HB.crowd = []; for (let i = 0; i < 10; i++) HB.crowd.push(person(S, PCOL[i % PCOL.length], { pos: [X - 10 + i * 2.1, .5, 12 + (i % 3) * 1.2], yaw: Math.PI + (G.hash(i, 1) - .5), hat: ['cap', 'bun', 'fedora', null][i % 4] }));
})();
// ---- DN: Restaurant (Tellerwaescher) ----
const DN = {};
(function () {
  const S = 'DN', X = SETX.DN;
  room(S, X, 0, 16, 12, 6, '#f2dfbf', '#e9e1d2', { wall2: '#ead3ad' });
  const fl = new G.Geo(); for (let i = 0; i < 16; i++) for (let j = 0; j < 12; j++) if ((i + j) % 2) fl.add(G.box(1, .02, 1, '#2b2f45', { base: true }), cp([X - 7.5 + i, 0, -5.5 + j])); mk(S, fl, { cast: false, outline: false });
  mk(S, G.box(10, 1.1, 1.2, '#c0392b', { base: true }).add(G.box(10.2, .1, 1.4, '#f4efe2', { base: true }), cp([0, 1.1, 0])), { pos: [X, 0, 1] });
  for (let i = 0; i < 6; i++) mk(S, G.cyl(.06, .06, .8, 8, '#9aa3b5').add(G.cyl(.32, .32, .12, 16, '#e8483c').smooth(), cp([0, .8, 0])), { pos: [X - 4 + i * 1.6, 0, -.2] });
  mk(S, G.box(3, 1, 1, '#c9ced8', { base: true }).add(G.box(2.4, .1, .7, '#7fb6d9', { base: true }), cp([0, 1, 0])), { pos: [X + 2.5, 0, 4.5] });
  DN.plates = []; const pg = G.cyl(.32, .3, .05, 20, '#ffffff').smooth(); for (let i = 0; i < 12; i++) DN.plates.push(mk(S, pg, { pos: [X + .9, 1.12 + i * .06, 3.6] }));
  DN.ponzi = mkPonzi(S, [X + 1.6, 0, 3.7], Math.PI);
  DN.cust = [person(S, '#2a8fd6', { pos: [X - 2.4, .5, -.25], yaw: 0, s: .95 }), person(S, '#e05d9a', { pos: [X - .8, .5, -.25], yaw: 0, hat: 'bun', s: .95 })];
  DN.boss = person(S, '#f4efe2', { pos: [X - 2, 0, 3.8], yaw: Math.PI / 2, leg: '#232838', tie: '#232838', s: 1.05 });
  signMesh(S, null, [X, 4.2, 5.82], 5, 1.1, [['DINER']], '#c0392b', '#ffffff', { border: '#ffffff', mo: { rot: [0, Math.PI, 0] } });
})();
// ---- BK: Banco Zarossi, Montreal ----
const BK = {};
(function () {
  const S = 'BK', X = SETX.BK;
  ground(S, X, 0, 90, 70, '#d9d0bf'); ground(S, X, -1, 90, 7, '#a39d92', .02);
  const b = new G.Geo().add(G.box(14, 7.5, 8, '#efe7d4', { base: true })).add(G.box(15, .7, 9, '#ddd2b8', { base: true }))
    .add(G.box(15, .7, 9, '#ddd2b8', { base: true }), cp([0, 7.5, 0])).add(G.cyl(9.2, 0, 2.6, 3, '#e5dcc4', { rot: Math.PI / 2 }), cp([0, 8.2, 3.3], [Math.PI / 2, 0, 0], [1, .7, 1]));
  BK.b = mk(S, b, { pos: [X, 0, 10] });
  for (let i = 0; i < 6; i++) mk(S, G.cyl(.38, .34, 6.2, 16, '#f7f2e6').smooth(), { pos: [X - 5.5 + i * 2.2, .7, 5.6] });
  BK.sign = signMesh(S, null, [X, 7.1, 5.48], 9, 1.1, [['BANCO ZAROSSI']], '#efe7d4', '#3a3f5c', { border: '#c8b98f', mo: { rot: [0, Math.PI, 0] } });
  BK.banner = signMesh(S, null, [X, 4.4, 5.3], 4.8, 1.6, [['6%', '900 120px IB, P, Arial'], ['INTEREST!', '900 76px IB, P, Arial']], '#2fa36b', '#ffffff', { border: '#ffffff', mo: { rot: [0, Math.PI, 0] } });
  BK.door = mk(S, G.box(2.4, 3.4, .12, '#5a3a22', { base: true }), { pos: [X, .7, 5.95] });
  BK.closed = signMesh(S, null, [X, 2.4, 5.8], 2.2, .7, [['CLOSED']], '#ffffff', '#e8483c', { border: '#e8483c', mo: { vis: false, rot: [0, Math.PI, 0] } });
  [[-20, 10, 9, 1], [20, 10, 11, 4], [-31, 9, 8, 6], [31, 9, 7, 2]].forEach(([dx, bw, bh, ci]) => building(S, X + dx, 12, bw, bh, 8, BRICK[ci], { yaw: Math.PI, rows: 3, cols: 3, shop: '#3b6ea5' }));
  for (let x = -24; x <= 24; x += 8) lamp(S, X + x, 3.3);
  BK.queue = []; for (let i = 0; i < 14; i++) BK.queue.push(person(S, PCOL[(i + 5) % PCOL.length], { pos: [X - 1.2 - (i % 7) * 1.0 - (i > 6 ? .5 : 0), 0, 4.3 - (i > 6 ? .9 : 0)], yaw: Math.PI / 2 + .3 * (G.hash(i, 9) - .5) + Math.PI, hat: ['fedora', 'bun', 'cap', 'boater', null][i % 5] }));
  BK.queue.forEach(p => { p.yaw = Math.PI / 2 * 1; p.m.rot = [0, p.yaw, 0] });
  BK.car = car(S, X + 9, -1.2, 0, '#2b2f45');
  BK.bag = mk(S, G.ico(.45, 2, '#c9a35a', .1, 4, 1.1).smooth().add(G.box(.2, .25, .2, '#a8803c', { base: true }), cp([0, .38, 0])), { parent: BK.car, pos: [.9, 1.4, 0] });
  PZ.BK = mkPonzi(S, [X + 6.5, 0, 2.2], -2.4);
})();
// ---- PR: Gefaengniszelle ----
const PR = {};
(function () {
  const S = 'PR', X = SETX.PR;
  room(S, X, 0, 7, 6, 4.4, '#a7afc2', '#7d8496', { wall2: '#99a2b6' });
  const bars = new G.Geo(); for (let i = 0; i < 15; i++) bars.add(G.cyl(.05, .05, 4.4, 8, '#3a3f5c').smooth(), cp([-3.5 + i * .5, 0, 0]));
  bars.add(G.box(7, .14, .14, '#3a3f5c', { base: true }), cp([0, 2.6, 0])).add(G.box(7, .14, .14, '#3a3f5c', { base: true }), cp([0, 4.2, 0]));
  PR.bars = mk(S, bars, { pos: [X, 0, -3] });
  mk(S, G.box(2.6, .5, 1, '#8a5a3c', { base: true }), { pos: [X - 1.6, 0, 2.3] });
  mk(S, G.box(1.4, .1, .9, '#c9b98f', { base: true }), { pos: [X - 1.6, .5, 2.3] });
  const win = new G.Geo().add(G.box(1.2, 1, .05, '#cfe9ff', { base: true })); for (let i = 0; i < 4; i++) win.add(G.box(.06, 1, .08, '#3a3f5c', { base: true }), cp([-.45 + i * .3, 0, 0]));
  mk(S, win, { pos: [X + 1.2, 2.7, 2.83], emis: .8, cast: false });
  PR.ponzi = mkPonzi(S, [X - 1.6, .25, 2.2], Math.PI);
  PR.num = signMesh(S, null, [X - 1.6, 1.25, 1.9], .55, .25, [['6660']], '#ffffff', '#232838', { border: '#232838', mo: { vis: false, rot: [0, Math.PI, 0] } });
})();
// ---- DK: riesiger Schreibtisch (Briefe, Coupons, Rechnungen) ----
const DK = {};
(function () {
  const S = 'DK', X = SETX.DK;
  const top = new G.Geo(); for (let i = 0; i < 14; i++) top.add(G.box(40, .4, 1.5, i % 2 ? '#a8703f' : '#b07a48', { base: true }), cp([0, 0, -10 + i * 1.5]));
  mk(S, top, { pos: [X, -.4, 0], cast: false, outline: false });
  mk(S, G.box(40, 14, .4, '#e9f4ff', { base: true }), { pos: [X, -.4, 11], cast: false, outline: false });
  DK.lamp = mk(S, G.cyl(1.2, 1.2, .3, 20, '#2f5d4a').smooth().add(G.cyl(.12, .12, 5, 8, '#c9a35a'), cp([0, .3, 0])).add(G.cyl(1.6, .5, 1.4, 20, '#2f8a5a', { open: true }).smooth(), cp([1.2, 4.6, 0], [0, 0, -1.9])), { pos: [X + 7, 0, 6] });
  mk(S, G.ico(1.2, 1, '#fff1b8').smooth(), { pos: [X + 7.4, 4, 6], emis: 1, vis: false });
  // Globus
  DK.globe = mk(S, G.ico(1.6, 3, '#4fa9ec').smooth(), { pos: [X - 8, 3.4, 6] });
  const land = new G.Geo(); for (let i = 0; i < 14; i++) { const a = G.hash(i, 1) * 6.28, b = (G.hash(i, 2) - .5) * 2.2; land.add(G.ico(.55, 2, '#6cbf55', .2, i, .35).smooth(), cp([Math.cos(a) * Math.cos(b) * 1.45, Math.sin(b) * 1.45, Math.sin(a) * Math.cos(b) * 1.45], [0, -a, b + Math.PI / 2])) }
  DK.land = mk(S, land, { parent: DK.globe });
  mk(S, G.cyl(1, 1.1, .3, 18, '#5a3a22').add(G.cyl(.12, .12, 1.8, 8, '#c9a35a'), cp([0, .3, 0])), { pos: [X - 8, 0, 6] });
  // Briefumschlag
  DK.env = texMesh(S, 4.4, 2.8, () => tex(880, 560, (x, wd, ht) => { x.fillStyle = '#f6ecd6'; x.fillRect(0, 0, wd, ht); x.strokeStyle = '#c0392b'; x.lineWidth = 16; x.setLineDash([40, 30]); x.strokeRect(14, 14, wd - 28, ht - 28); x.setLineDash([]);
    x.fillStyle = '#e8483c'; x.fillRect(wd - 190, 50, 130, 160); x.fillStyle = '#ffd166'; x.fillRect(wd - 175, 65, 100, 130); txt(x, 'ESPAÑA', wd - 125, 130, '900 26px IB, Arial', '#c0392b');
    txt(x, 'POR AVIÓN', 160, 80, '900 40px IB, Arial', '#2a6fd6'); txt(x, 'BOSTON, MASS.', wd / 2, 320, '700 54px P, Arial', '#232838'); txt(x, 'U.S.A.', wd / 2, 400, '700 54px P, Arial', '#232838') }), { rot: [-Math.PI / 2, Math.PI, .12], pos: [X - 3, .02, -1] });
  // Coupons
  const couponTex = () => tex(640, 440, (x, wd, ht) => { x.fillStyle = '#e9f1d8'; x.fillRect(0, 0, wd, ht); x.strokeStyle = '#2f7a4a'; x.lineWidth = 12; x.strokeRect(16, 16, wd - 32, ht - 32); x.lineWidth = 3; x.strokeRect(34, 34, wd - 68, ht - 68);
    for (let i = 0; i < 14; i++) { x.beginPath(); x.arc(wd / 2, ht / 2 + 10, 40 + i * 9, 0, 7); x.strokeStyle = '#2f7a4a22'; x.stroke() }
    txt(x, 'INTERNATIONAL', wd / 2, 90, '900 50px IB, Arial', '#2f6a42'); txt(x, 'REPLY COUPON', wd / 2, 148, '900 50px IB, Arial', '#2f6a42');
    x.fillStyle = '#ffffffaa'; x.beginPath(); x.arc(wd / 2, 270, 70, 0, 7); x.fill(); txt(x, '✉', wd / 2, 272, '700 80px P, Arial', '#2f6a42'); txt(x, '= 1 STAMP', wd / 2, 385, '900 36px IB, Arial', '#2f6a42') });
  DK.coupons = []; for (let i = 0; i < 6; i++) DK.coupons.push(texMesh(S, 2.4, 1.65, couponTex, { rot: [-Math.PI / 2, Math.PI, 0], pos: [X, .05 + i * .01, 0], vis: false }));
  const stampTex = (c, lab) => () => tex(320, 400, (x, wd, ht) => { x.fillStyle = '#fffaf0'; x.fillRect(0, 0, wd, ht); for (let i = 0; i < 10; i++) { x.fillStyle = '#e9f4ff'; x.beginPath(); x.arc(i * 34 + 10, 0, 12, 0, 7); x.arc(i * 34 + 10, ht, 12, 0, 7); x.fill() } x.fillStyle = c; x.fillRect(30, 30, wd - 60, ht - 60);
    txt(x, lab, wd / 2, ht / 2 - 40, '900 64px IB, Arial', '#fff'); txt(x, 'POSTAGE', wd / 2, ht / 2 + 60, '900 40px IB, Arial', '#ffffffcc') });
  DK.stampIT = texMesh(S, 1.2, 1.5, stampTex('#2fa36b', 'ITALIA'), { rot: [-Math.PI / 2, Math.PI, 0], pos: [X - 5, .06, 1], vis: false });
  DK.stampUS = texMesh(S, 1.2, 1.5, stampTex('#2a6fd6', 'U.S.A.'), { rot: [-Math.PI / 2, Math.PI, 0], pos: [X + 5, .06, 1], vis: false });
  // Coupon-Berg (eine Geometrie, waechst per Skalierung)
  const mt = new G.Geo(); for (let i = 0; i < 260; i++) { const r = 3.2 * Math.sqrt(G.hash(i, 3)), a = G.hash(i, 4) * 6.28, h = (1 - r / 3.4) * 3.5 * G.hash(i, 5) + .1; mt.add(G.box(.9, .04, .62, i % 3 ? '#e9f1d8' : '#d7e6c1', { base: true }), cp([Math.cos(a) * r, h, Math.sin(a) * r], [(G.hash(i, 6) - .5) * .6, G.hash(i, 7) * 3, (G.hash(i, 8) - .5) * .6])) }
  DK.mount = mk(S, mt, { pos: [X, 0, 2], vis: false });
  DK.small = mk(S, G.box(.9, .4, .62, '#e9f1d8', { base: true }), { pos: [X - 6, 0, 2], vis: false });
  DK.coins = []; const cg = G.cyl(.32, .32, .07, 20, '#ffc94a').smooth(); for (let i = 0; i < 24; i++) DK.coins.push(mk(S, cg, { vis: false }));
  // Notizblock (Barron) + Kassenbuch (Audit)
  DK.pad = texMesh(S, 5, 3.4, () => tex(1000, 680, (x, wd, ht) => { x.fillStyle = '#fffdf3'; x.fillRect(0, 0, wd, ht); for (let i = 0; i < 12; i++) { x.fillStyle = '#9ec5ea'; x.fillRect(0, 80 + i * 50, wd, 3) } x.fillStyle = '#e88'; x.fillRect(90, 0, 4, ht);
    txt(x, 'COUPONS NEEDED:', 130, 150, '700 54px P, Arial', '#232838', { al: 'left' }); txt(x, '160,000,000', 130, 250, '900 96px IB, Arial', '#c0392b', { al: 'left' });
    txt(x, 'IN CIRCULATION:', 130, 400, '700 54px P, Arial', '#232838', { al: 'left' }); txt(x, '27,000', 130, 500, '900 96px IB, Arial', '#2a6fd6', { al: 'left' }) }), { rot: [-Math.PI / 2, Math.PI, -.06], pos: [X + 1, .05, -1.5], vis: false });
  DK.pencil = mk(S, G.cyl(.12, .12, 4, 6, '#ffc94a').add(G.cyl(.12, 0, .4, 6, '#f2d2a2'), cp([0, 4, 0])), { pos: [X + 4.2, .2, -2.5], rot: [0, 0, 1.45], vis: false });
  DK.ledger = texMesh(S, 5.4, 3.6, () => tex(1000, 667, (x, wd, ht) => { x.fillStyle = '#f7f0dc'; x.fillRect(0, 0, wd, ht); x.fillStyle = '#5a3a22'; x.fillRect(wd / 2 - 8, 0, 16, ht);
    txt(x, 'ASSETS', wd * .25, 70, '900 52px IB, Arial', '#2f7a4a'); txt(x, 'DEBTS', wd * .75, 70, '900 52px IB, Arial', '#c0392b');
    for (let i = 0; i < 7; i++) { x.fillStyle = '#c9bfa5'; x.fillRect(30, 130 + i * 70, wd / 2 - 60, 3); x.fillRect(wd / 2 + 30, 130 + i * 70, wd / 2 - 60, 3) }
    txt(x, '$ ? ? ?', wd * .25, 300, '900 70px IB, Arial', '#2f7a4a'); txt(x, 'MILLIONS', wd * .75, 260, '900 70px IB, Arial', '#c0392b'); txt(x, 'MORE', wd * .75, 360, '900 70px IB, Arial', '#c0392b') }), { rot: [-Math.PI / 2, Math.PI, .05], pos: [X, .05, -.5], vis: false });
  DK.ponzi = mkPonzi(S, [X - 10, 0, -6], 0); DK.ponzi.m.vis = false;
})();
