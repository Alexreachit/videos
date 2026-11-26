// ===================== Set HX: Heathrow 1983 (Lager Unit 7, Halle innen, Gold, Polizei, Gefaengnis, Schmelze, Juwelier) =====================
const S = 'HX';
LIGHT.dawn = { sun: [.75, .38, .45], sunCol: '#ffd2a6', sky: '#f3c7aa', gnd: '#6a6470', fog: '#e9b99c', fogN: 70, fogF: 230, shCol: '#6f78c0', bg: 'linear-gradient(#2c3f7a 0%,#6a6fa8 30%,#d99aa0 58%,#ffc48a 78%,#ffd9a8 100%)' };
LIGHT.ware = { sun: [.3, .85, .45], sunCol: '#f4f6ff', sky: '#cfd6ea', gnd: '#6a6e7a', fog: '#4a5068', fogN: 50, fogF: 160, shCol: '#7a84b8', bg: '#353b52' };
LIGHT.goldL = { sun: [.35, .8, .5], sunCol: '#fff0c8', sky: '#e8d2a8', gnd: '#6a5a44', fog: '#3a3226', fogN: 40, fogF: 140, shCol: '#8a6a7a', bg: '#2e281f' };
LIGHT.shop = { sun: [.4, .8, .5], sunCol: '#fff4e0', sky: '#f6e6d0', gnd: '#9a7a5a', fog: '#e8d6c0', fogN: 60, fogF: 200, shCol: '#a08ab8', bg: '#f0dcc4' };
const IN = [0, 0, -140], GD = [60, 0, 0], PO = [100, 0, 0], PR = [140, 0, 0], SM = [-60, 0, 0], JW = [180, 0, 0];
const DOOR = [6, 0, 0];
const GOLD = '#f2c14e';
(function exterior() {
  // Boden: Gewerbegebiet (Asphalt + Grasstreifen)
  mk(S, merge([at(G.box(100, .4, 110, '#5c6170', { base: true }), [0, -.4, 5]), at(G.box(100, .06, 3, '#7a9a5a', { base: true }), [0, 0, 16]),
    at(G.box(100, .06, 40, '#6f9a58', { base: true }), [0, -.02, -30])]), { outline: false });
  for (let k = -6; k <= 6; k++) mk(S, G.box(1.6, .03, .18, '#e8e4d0', { base: true }), { pos: [k * 4.5, 0, 8], outline: false, cast: false });
  // Halle Unit 7 (Wellblech-Look)
  const F = [at(G.box(26, 8, 16, '#93a7bc', { base: true }), [0, 0, -8]), at(G.box(26.6, .6, 16.6, '#5e6e82', { base: true }), [0, 8, -8])];
  for (let k = 0; k < 26; k++) F.push(at(G.box(.12, 7.6, .06, '#7d92a8', { base: true }), [-12.6 + k * 1.0, .2, .03]));
  [-8, -2].forEach(x => { F.push(at(G.box(4.6, 4.6, .2, '#d6dbe4', { base: true }), [x, 0, .1])); for (let k = 0; k < 8; k++) F.push(at(G.box(4.4, .07, .06, '#a8b0bf'), [x, .4 + k * .55, .22])) });
  F.push(at(G.box(1.5, 2.6, .2, '#2f5a96', { base: true }), [DOOR[0], 0, .1]), at(G.box(1.9, .25, .5, '#4a5568', { base: true }), [DOOR[0], 2.7, .2]));
  F.push(at(G.box(1.8, 1.3, .15, '#2a3446', { base: true }), [9.5, 1.3, .1]));
  mk(S, merge(F).vary(.02, 5));
  mk(S, merge([at(G.box(.5, .25, .3, '#ffe7a0'), [DOOR[0], 3.3, .3]), at(G.box(.5, .25, .3, '#ffe7a0'), [-5, 5.0, .3]), at(G.box(1.6, 1.1, .08, '#ffd98a'), [9.5, 1.4, .2])]), { emis: 1, outline: false, cast: false });
  texPlane(S, 3.2, 1.3, () => tex(320, 130, (c, wd, ht) => { c.fillStyle = '#f4f1e6'; c.fillRect(0, 0, wd, ht); c.strokeStyle = '#232838'; c.lineWidth = 10; c.strokeRect(5, 5, wd - 10, ht - 10);
    c.fillStyle = '#232838'; c.font = '900 84px IB,Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('UNIT 7', wd / 2, ht / 2 + 4) }), { pos: [DOOR[0], 4.4, .2] });
  // Nachbarhallen
  [[-34, '#b0a490', 7], [32, '#8c9cb0', 6.5]].forEach(([x, c, h], j) => mk(S, merge([at(G.box(18, h, 14, c, { base: true }), [x, 0, -7]), at(G.box(18.4, .5, 14.4, '#5a6474', { base: true }), [x, h, -7])]).vary(.03, 7 + j)));
  // Zaun
  const Z = []; for (let k = -12; k <= 12; k++) if (k < 1 || k > 3) Z.push(at(G.box(.12, 2.2, .12, '#4a5060', { base: true }), [k * 2.2, 0, 14]));
  Z.push(at(G.box(26, .08, .08, '#4a5060'), [-15.4, 2.1, 14]), at(G.box(18, .08, .08, '#4a5060'), [17.6, 2.1, 14]));
  mk(S, merge(Z), { cast: false });
  // Tower + Flughafen in der Ferne
  mk(S, merge([at(G.cyl(1.4, 1.1, 22, 16, '#d8d4cc'), [-40, 0, -44]), at(G.cyl(3.4, 2.6, 3, 16, '#3a4a66'), [-40, 22, -44]), at(G.cyl(3.6, 3.6, .5, 16, '#e8e4dc'), [-40, 25, -44])]));
  mk(S, merge([...Array(10)].map((_, k) => at(G.box(.5, .2, .5, '#fff2c0'), [-45 + k * 10, .1, -40]))), { emis: 1, outline: false, cast: false });
  mk(S, merge([...Array(7)].map((_, k) => at(G.box(.4, .4, .4, '#ff5d5d'), [-45 + k * 14, 2 + (k % 3), -48]))), { emis: 1, outline: false, cast: false });
})();
// Verkehrsflugzeug (generisch, ohne Airline)
const PLANE = (function () {
  const WH = '#eef1f5', BL = '#2f5fae', GR = '#aab3c2';
  const root = mk(S, merge([
    at(G.cyl(1.9, 1.9, 34, 22, WH), [-17, 0, 0], [0, 0, -PI / 2]), at(G.cyl(1.9, .3, 5.5, 22, WH), [17, 0, 0], [0, 0, -PI / 2]), at(G.cyl(1.9, .7, 6, 22, WH), [-17, 0, 0], [0, 0, PI / 2]),
    at(G.box(33, .4, 3.88, BL), [0, .2, 0]), at(G.box(2.2, .55, 2.9, '#1d2a44'), [18.2, .5, 0], [0, 0, -.25]),
    at(G.box(5, .3, 30, GR), [-1, -1.2, 0]), at(G.box(4.4, 6.2, .36, BL, { base: true }), [-20.6, .8, 0], [0, 0, .45]), at(G.box(2.6, .26, 10, GR), [-22.4, .8, 0]),
    at(G.cyl(1.0, 1.0, 3.4, 16, GR), [.6, -2.4, 7], [0, 0, PI / 2]), at(G.cyl(1.0, 1.0, 3.4, 16, GR), [.6, -2.4, -7], [0, 0, PI / 2])]).vary(.02, 3), { pos: [0, 30, -20], cast: false });
  mk(S, merge([...Array(28)].flatMap((_, k) => [at(G.box(.34, .3, .05, '#ffe2a0'), [14 - k * 1.0, .4, 1.955]), at(G.box(.34, .3, .05, '#ffe2a0'), [14 - k * 1.0, .4, -1.955])])), { parent: root, emis: .9, outline: false, cast: false });
  mk(S, merge([at(G.box(.5, .5, .5, '#ff4040'), [-1, -1.2, 15.2]), at(G.box(.5, .5, .5, '#40ff70'), [-1, -1.2, -15.2]), at(G.box(.6, .4, .6, '#fff6d0'), [19.5, -1.4, 0])]), { parent: root, emis: 1, outline: false, cast: false });
  return root;
})();
function planeAt(t, y = 26, z = -26, sp = 9, x0 = -70) { PLANE.pos = [x0 + ((t * sp) % 160), y - ((t * sp) % 160) * .06, z]; PLANE.rot = [0, 0, -.06] }
// Fluchtwagen (weisser Kastenwagen)
const VAN = mk(S, merge([
  at(G.box(3.6, 2.2, 2.0, '#eceff3', { base: true }), [-.6, .45, 0]), at(G.box(1.4, 1.5, 1.94, '#eceff3', { base: true }), [1.9, .45, 0]), at(G.box(.08, .7, 1.7, '#2a3a5a'), [2.62, 1.45, 0], [0, 0, -.2]),
  at(G.box(3.62, .18, 2.02, '#c0303a'), [-.6, 1.3, 0]),
  ...[[1.8, .95], [1.8, -.95], [-1.6, .95], [-1.6, -.95]].map(([x, z]) => at(G.cyl(.42, .42, .26, 14, '#1b1b22', { cap: '#777' }), [x, .42, z + (z > 0 ? 0 : -.26)], [PI / 2, 0, 0])),
  at(G.box(.08, .25, .3, '#ffe7a0'), [2.62, .8, .65]), at(G.box(.08, .25, .3, '#ffe7a0'), [2.62, .8, -.65])]).vary(.02, 31), { pos: [13.4, 0, 2.6], rot: [0, -.25, 0] });
// Goldbarren-Geometrie
function bars(cx, cz, nx, nz, ny, y0 = 0, s = 1) { const B = []; for (let y = 0; y < ny; y++) for (let x = 0; x < nx - (y % 2 ? 1 : 0); x++) for (let z = 0; z < nz; z++)
  B.push(at(G.box(.46 * s, .16 * s, .22 * s, GOLD, { base: true, top: '#ffd978' }), [cx + (x - (nx - 1) / 2 + (y % 2) * .5) * .5 * s, y0 + y * .165 * s, cz + (z - (nz - 1) / 2) * .26 * s])); return B }
(function inside() {
  mk(S, G.box(20, .3, 34, '#7a7e88', { base: true }), { pos: [IN[0], -.3, IN[2] + 10], outline: false });
  mk(S, G.box(24, .3, 36, '#6e6a64', { base: true }), { pos: [GD[0], -.3, GD[2] + 10], outline: false });
  mk(S, G.box(18, .3, 32, '#5e5a54', { base: true }), { pos: [PO[0], -.3, PO[2] + 10], outline: false });
  mk(S, G.box(20, .3, 32, '#5a5e6a', { base: true }), { pos: [PR[0], -.3, PR[2] + 10], outline: false });
  mk(S, G.box(18, .3, 32, '#5a4a3a', { base: true }), { pos: [SM[0], -.3, SM[2] + 10], outline: false });
  mk(S, G.box(20, .3, 32, '#b08a64', { base: true }), { pos: [JW[0], -.3, JW[2] + 10], outline: false });
  // ---- Halle innen (Tresor + Wachen) ----
  const V = [at(G.box(20, 6, .4, '#b8bcc6', { base: true }), [IN[0], 0, IN[2] - 6.5]),
    at(G.box(.4, 6, 14, '#a8acb8', { base: true }), [IN[0] - 9, 0, IN[2]]), at(G.box(.4, 6, 14, '#a8acb8', { base: true }), [IN[0] + 9, 0, IN[2]])];
  V.push(at(G.box(6.4, 5.2, .5, '#8a8e9a', { base: true }), [IN[0] + 3, 0, IN[2] - 6.2]), at(G.cyl(2.1, 2.1, .6, 28, '#c4c8d2'), [IN[0] + 3, 2.5, IN[2] - 6.0], [PI / 2, 0, 0]),
    at(G.cyl(1.7, 1.7, .2, 28, '#a0a6b4'), [IN[0] + 3, 2.5, IN[2] - 5.6], [PI / 2, 0, 0]), at(G.cyl(.45, .45, .4, 20, '#232838'), [IN[0] + 3, 2.5, IN[2] - 5.5], [PI / 2, 0, 0]));
  for (let k = 0; k < 3; k++) V.push(at(G.box(2.4, .14, .14, '#e0e4ec'), [IN[0] + 3, 2.5, IN[2] - 5.3], [0, 0, k * PI / 3]));
  // Regale mit Kartons
  [-6.6, -3.6].forEach((x, j) => { V.push(at(G.box(2.6, .1, 1.1, '#5a6478', { base: true }), [IN[0] + x, 1.4, IN[2] - 5.6]), at(G.box(2.6, .1, 1.1, '#5a6478', { base: true }), [IN[0] + x, 2.8, IN[2] - 5.6]),
    at(G.box(.1, 3.6, .1, '#5a6478', { base: true }), [IN[0] + x - 1.25, 0, IN[2] - 5.1]), at(G.box(.1, 3.6, .1, '#5a6478', { base: true }), [IN[0] + x + 1.25, 0, IN[2] - 5.1]));
    for (let k = 0; k < 4; k++) V.push(at(G.box(.9, .7, .8, k % 2 ? '#c49a62' : '#b48a56', { base: true }), [IN[0] + x - .7 + (k % 2) * 1.4, 1.5 + Math.floor(k / 2) * 1.4, IN[2] - 5.6])) });
  mk(S, merge(V).vary(.02, 13));
  mk(S, merge([-5, 0, 5].map(x => at(G.box(2.6, .08, .4, '#f6fbff'), [IN[0] + x, 5.9, IN[2]]))), { emis: 1, outline: false, cast: false });
  // Benzin-Pfuetze
  mk(S, G.ico(1, 2, '#5f7590'), { pos: [IN[0] - 2.2, .005, IN[2] - 3.2], outline: false, cast: false, scl: [1.9, .012, .8], spec: 1 });
  // ---- Goldraum (Kartons + Barren) ----
  const D = [at(G.box(22, 6, .4, '#9a948a', { base: true }), [GD[0], 0, GD[2] - 5])];
  [-3.4, 3.4].forEach(x => D.push(at(G.box(2.4, .3, 1.8, '#a07a4a', { base: true }), [GD[0] + x, 0, GD[2] - 3.4])));
  [[-4.2, -3.6], [-2.6, -3.2], [2.6, -3.4], [4.2, -3.2]].forEach(([x, z], k) => D.push(at(G.box(1.1, .8, .9, '#c49a62', { base: true, top: '#d4aa72' }), [GD[0] + x, .3, GD[2] + z])));
  mk(S, merge(D).vary(.02, 17));
  mk(S, merge(bars(GD[0], GD[2] - 1.2, 7, 4, 5, 0, 1.1)).smooth(), { spec: .9, emis: .18 });
  mk(S, merge([...bars(GD[0] - 3.4, GD[2] - 3.4, 3, 3, 2, .3), ...bars(GD[0] + 3.4, GD[2] - 3.4, 3, 3, 2, .3)]), { spec: .9, emis: .18 });
  mk(S, merge([-4, 0, 4].map(x => at(G.box(2.4, .08, .4, '#fff2d0'), [GD[0] + x, 5.9, GD[2] - 1]))), { emis: 1, outline: false, cast: false });
  // ---- Polizei-Verhoerraum ----
  const P = [at(G.box(16, 6, .4, '#9fb3a2', { base: true }), [PO[0], 0, PO[2] - 4]),
    at(G.box(3.0, .12, 1.4, '#7a5a3a', { base: true }), [PO[0], 1.0, PO[2] - .8]), ...[[-1.3, -.3], [1.3, -.3], [-1.3, -1.3], [1.3, -1.3]].map(([x, z]) => at(G.box(.12, 1.0, .12, '#4a3a2a', { base: true }), [PO[0] + x, 0, PO[2] + z])),
    at(G.box(.5, .36, .7, '#e8e4d8', { base: true }), [PO[0] + .6, 1.12, PO[2] - .8]), at(G.box(2.2, 1.4, .1, '#2a3a4a', { base: true }), [PO[0] + 3.4, 2.2, PO[2] - 3.75])];
  mk(S, merge(P).vary(.03, 19));
  mk(S, merge([at(G.cyl(.03, .03, 2.0, 6, '#22252e'), [PO[0], 3.6, PO[2] - .8]), at(G.cyl(.6, .2, .45, 16, '#2f3a30'), [PO[0], 3.2, PO[2] - .8])]), { cast: false });
  mk(S, G.ico(.2, 2, '#fff2c0'), { pos: [PO[0], 3.15, PO[2] - .8], emis: 1, outline: false, cast: false });
  // ---- Gefaengnis ----
  mk(S, merge([at(G.box(20, 6, .4, '#8a8e98', { base: true }), [PR[0], 0, PR[2] - 3]),
    at(G.box(8, .5, .8, '#6a6e78', { base: true }), [PR[0], 0, PR[2] - 2.4]), at(G.box(1.2, .9, .1, '#2a2e3a', { base: true }), [PR[0] - 2, 3.6, PR[2] - 2.75])]).vary(.03, 23), { outline: false });
  // ---- Schmelze (Gartenhuette mit Ofen) ----
  const M2 = [at(G.box(16, 6, .4, '#7a5a40', { base: true }), [SM[0], 0, SM[2] - 3.5])];
  for (let k = 0; k < 14; k++) M2.push(at(G.box(.08, 6, .06, '#5e4430', { base: true }), [SM[0] - 7.5 + k * 1.15, 0, SM[2] - 3.28]));
  M2.push(at(G.box(2.4, 2.2, 1.8, '#4a4a52', { base: true }), [SM[0] - 1.6, 0, SM[2] - 2.2]), at(G.cyl(.5, .5, 1.6, 12, '#3a3a42'), [SM[0] - 1.6, 2.2, SM[2] - 2.6]),
    at(G.box(3.0, .14, 1.2, '#6a5038', { base: true }), [SM[0] + 2.2, 1.0, SM[2] - 1.6]), ...[[-1.3, -.5], [1.3, -.5], [-1.3, .5], [1.3, .5]].map(([x, z]) => at(G.box(.12, 1.0, .12, '#4a3828', { base: true }), [SM[0] + 2.2 + x, 0, SM[2] - 1.6 + z])));
  mk(S, merge(M2).vary(.03, 37));
  mk(S, G.box(1.2, .9, .1, '#ff7a1a', { base: true }), { pos: [SM[0] - 1.6, .5, SM[2] - 1.28], emis: 1, outline: false, cast: false });
  mk(S, G.cyl(.42, .5, .5, 18, '#ffb84a'), { pos: [SM[0] - 1.6, 2.2, SM[2] - 1.7], emis: 1, outline: false, cast: false });
  mk(S, merge(bars(SM[0] + 2.2, SM[2] - 1.6, 4, 2, 2, 1.14)), { spec: .9, emis: .2 });
  // ---- Juwelier ----
  const J = [at(G.box(18, 6, .4, '#e8d2b8', { base: true }), [JW[0], 0, JW[2] - 4]),
    at(G.box(6, 1.0, 1.2, '#7a4a3a', { base: true }), [JW[0], 0, JW[2] - 1.2]), at(G.box(6, .06, 1.2, '#cfe6f4'), [JW[0], 1.03, JW[2] - 1.2])];
  for (let k = 0; k < 3; k++) J.push(at(G.box(2.6, .1, .6, '#7a4a3a', { base: true }), [JW[0] - 3.6 + k * 3.6, 2.2, JW[2] - 3.6]));
  mk(S, merge(J).vary(.02, 41));
  const RG = []; for (let k = 0; k < 9; k++) RG.push(at(G.ico(.09, 1, GOLD), [JW[0] - 2.4 + k * .6, 1.08, JW[2] - 1.2 + (k % 2) * .25]));
  for (let k = 0; k < 12; k++) RG.push(at(G.ico(.08, 1, GOLD), [JW[0] - 4.6 + (k % 4) * .35 + Math.floor(k / 4) * 3.6, 2.32, JW[2] - 3.6]));
  mk(S, merge(RG), { spec: 1, emis: .35, outline: false });
  mk(S, merge([-3, 0, 3].map(x => at(G.box(2.0, .08, .4, '#fff6e0'), [JW[0] + x, 5.9, JW[2] - 1]))), { emis: 1, outline: false, cast: false });
})();
// ---------- Figuren-Looks ----------
const ROPE = `<path d="M56,176 Q100,190 146,176 M54,198 Q100,212 148,198" stroke="#c9a46a" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M56,176 Q100,190 146,176 M54,198 Q100,212 148,198" stroke="${OL}" stroke-width="2" fill="none" opacity=".5"/>`;
const HAIRS = [`<path d="M40,60 Q44,14 100,16 Q156,14 160,60 Q140,34 100,36 Q60,34 40,60Z" fill="#5a3a24" stroke="${OL}" stroke-width="5"/>`, `<path d="M42,56 Q56,22 100,22 Q144,22 158,56 Q124,40 100,42 Q76,40 42,56Z" fill="#2a2a30" stroke="${OL}" stroke-width="5"/>`,
  `<path d="M44,50 Q60,24 100,24 Q140,24 156,50 Q120,38 100,40 Q80,38 44,50Z" fill="#8a6a3a" stroke="${OL}" stroke-width="5"/>`,
  `<path d="M38,70 Q30,10 100,12 Q170,10 162,70 L164,130 Q150,100 150,60 Q100,44 50,60 Q50,100 36,130Z" fill="#c9843a" stroke="${OL}" stroke-width="5"/>`];
const HELMET = `<path d="M44,50 Q44,0 100,-2 Q156,0 156,50 Z" fill="#1b2f6b" stroke="${OL}" stroke-width="6"/><circle cx="100" cy="20" r="9" fill="#e8e4d8" stroke="${OL}" stroke-width="4"/><path d="M40,48 L160,48" stroke="${OL}" stroke-width="7"/>`;
Object.assign(LOOK, {
  rob: k => ({ sw: ['#2b2b36', '#3a2e2a', '#2a3440'][k % 3], swd: '#1e1e28', pa: '#2f2f3a', hat: HAT.balaclava }),
  black: { sw: '#3b4a6a', swd: '#2c3852', pa: '#2a3045', hat: HAIRS[0], mid: MID.badge },
  staff: k => ({ sw: '#3b4a6a', swd: '#2c3852', pa: '#2a3045', hat: HAIRS[(k + 1) % 3], mid: ROPE }),
  bobby: { sw: '#1b2f6b', swd: '#14234f', pa: '#1a2a55', hat: HELMET, mid: MID.buttons },
  dsuit: { sw: '#6a5a4a', swd: '#57483a', pa: '#3e3a36', hat: HAIRS[1], mid: MID.tie },
  shopper: { sw: '#d35f7a', swd: '#b04a64', pa: '#3a3e5a', hat: HAIRS[3] },
  jeweller: { sw: '#f2efe6', swd: '#d6d2c6', pa: '#3a3e4a', hat: HAT.grey, mid: MID.tie },
  prisoner: k => ({ sw: '#d0d0d0', swd: '#9a9a9a', pa: '#9a9a9a', mid: MID.stripes, hat: HAIRS[k % 3] }),
});
const L_ = (who, k) => { const v = LOOK[who]; return typeof v == 'function' ? v(k) : v };
function figk(p, who, k, o = {}, H3 = 1.75, clipY = null) { const look = L_(who, k); const sv = LOOK.__tmp; LOOK.__tmp = look; const h = fig(p, '__tmp', o, H3, clipY); LOOK.__tmp = sv; return h }
const P_BAR = `<g transform="translate(-30,-16)"><path d="M6,0 L54,0 L62,26 L-2,26Z" fill="${GOLD}" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/><path d="M10,6 L50,6" stroke="#fff3b0" stroke-width="4"/></g>`;
const P_BARS = `<g transform="translate(-36,-30)">${[0, 1, 2].map(k => `<path d="M${6 + (k % 2) * 6},${k * 20} L${58 + (k % 2) * 6},${k * 20} L${66 + (k % 2) * 6},${k * 20 + 22} L${-2 + (k % 2) * 6},${k * 20 + 22}Z" fill="${GOLD}" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/>`).join('')}</g>`;
const P_CAN = a => `<g transform="rotate(${a}) translate(-30,-40)"><rect x="0" y="10" width="54" height="62" rx="8" fill="#d83a3a" stroke="${OL}" stroke-width="5"/><rect x="34" y="0" width="14" height="16" fill="#3a3a44" stroke="${OL}" stroke-width="4"/><path d="M10,22 L44,60 M44,22 L10,60" stroke="#a82a2a" stroke-width="5"/></g>`;
const P_MATCH = `<g transform="translate(-4,-50) rotate(10)"><rect x="0" y="0" width="7" height="54" rx="3" fill="#e8c890" stroke="${OL}" stroke-width="3"/><circle cx="3.5" cy="0" r="7" fill="#c0303a" stroke="${OL}" stroke-width="3"/><path d="M3,-30 Q16,-12 4,-4 Q-10,-12 3,-30Z" fill="#ffb33a" stroke="${OL}" stroke-width="3"/><path d="M4,-18 Q9,-10 4,-6 Q-1,-10 4,-18Z" fill="#fff2a0"/></g>`;
const P_KEY = `<g transform="translate(-14,-40) rotate(-20)"><circle cx="14" cy="10" r="12" fill="#ffd166" stroke="${OL}" stroke-width="5"/><path d="M11,20 L17,20 L17,62 L25,62 L25,56 L21,56 L21,50 L26,50 L26,44 L17,44" fill="#ffd166" stroke="${OL}" stroke-width="4" stroke-linejoin="round"/></g>`;
const P_RING = `<g transform="translate(-6,-26)"><circle cx="6" cy="0" r="13" fill="none" stroke="${GOLD}" stroke-width="7"/><circle cx="6" cy="0" r="13" fill="none" stroke="${OL}" stroke-width="2"/><path d="M0,-18 L6,-26 L12,-18 L6,-12Z" fill="#bfe6ff" stroke="${OL}" stroke-width="3"/></g>`;
// ---------- Shots ----------
const HERO_A = { pos: [4.6, 1.8, 13.6], at: [8.6, 3.0, 2.4], fov: 52 }, HERO_B = { pos: [5.2, 1.6, 11.8], at: [8.6, 2.8, 2.6], fov: 50 };
const gangOut = (t, n = 4) => {
  let h = ''; for (let k = 0; k < n; k++) { const u = ((t * .17 + k / n) % 1), x = lerp(DOOR[0], 10.6, u), z = lerp(1.0, 3.4, u) + (k % 2) * .5;
    h += figk([x, 0, z], 'rob', k, Object.assign({ mouth: 'grin', blink: 0, look: [5, 2], prop: P_BARS, hR: [150, 168], hL: [60, 172], elR2: 'in' }, walk(t + k * .37, 8))) }
  return h };
SHOT.hero = { set: S, light: 'dawn', cam: i => ({ a: HERO_A, b: HERO_B }),
  upd: (t, i) => planeAt(t + 3.2, 24, -34, 8),
  figs: (t, i) => gangOut(t),
  sfx: i => [{ k: 'pop', t: .2 }] };
SHOT.airport = { set: S, light: 'dawn',
  cam: i => ({ a: { pos: [-6, 3.2, 34], at: [0, 8, -6], fov: 52 }, b: { pos: [-3.5, 2.6, 30], at: [1, 7, -6], fov: 50 } }),
  upd: (t, i) => planeAt(t - Lt(i).start, 26, -28, 10, -52),
  figs: (t, i) => { let h = ''; const t0 = Lt(i).start; for (let k = 0; k < 6; k++) { const u = ez(cl((t - t0 - k * .12) / 2.6, 0, 1));
      h += figk([lerp(-2 + k * .8, DOOR[0] - 2.2 + k * .6, u), 0, lerp(13 + (k % 2), 2.2 + (k % 2) * .8, u)], 'rob', k, Object.assign({ mouth: 'grin', blink: 0, look: [5, 1] }, u < 1 ? walk(t + k * .3, 8) : {})) } return h },
  ui: (t, i) => { let h = pillAt(540, 250, t, Lt(i).start + .05, nextStart(i), '📍 HEATHROW · NOV 26, 1983', '#232838', '#fff', 48);
    const a = wt(i, /six/) - .1; if (t > a) { let heads = ''; for (let k = 0; k < 6; k++) heads += `<div style="display:inline-block;margin:0 4px;transform:scale(${pop(t, a + k * .06, .25)})"><svg width="74" height="74" viewBox="0 0 60 60"><circle cx="30" cy="30" r="25" fill="#23232c" stroke="${OL}" stroke-width="5"/><rect x="15" y="22" width="30" height="13" rx="6" fill="#f7e4b5"/><circle cx="23" cy="28.5" r="3" fill="${OL}"/><circle cx="37" cy="28.5" r="3" fill="${OL}"/></svg></div>`;
      h += `<div style="position:absolute;left:0;right:0;top:330px;text-align:center;z-index:2200">${heads}<div style="margin-top:6px;transform:scale(${pop(t, a + .45)})">${PILL('6 ROBBERS', '#e0303a', '#fff', 60)}</div></div>` }
    h += labelAt([0, 8.8, 0], PILL('🏭 WAREHOUSE', '#ffd166', OL, 46), t, wt(i, /warehouse/) - .1, nextStart(i));
    return h },
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: 1.2 }, { k: 'pop', t: Lt(i).start + .05 }, ...[0, 2, 4].map(k => ({ k: 'pop', t: wt(i, /six/) + k * .06 })), { k: 'ding', t: wt(i, /warehouse/) }] };
SHOT.key = { set: S, light: 'dawn',
  cam: i => ({ a: { pos: [DOOR[0] + .1, 1.7, 7.6], at: [DOOR[0] + .1, 1.3, 0], fov: 42 }, b: { pos: [DOOR[0] + .1, 1.6, 6.6], at: [DOOR[0] + .1, 1.25, 0], fov: 40 } }),
  figs: (t, i) => { const a = wt(i, /copied/) - .1, g = ez(cl(t, a, a + .5));
    return fig([DOOR[0] - .6, 0, 1.0], 'black', { mouth: 'hmm', blink: bl(t, 0), look: [6, 1], sweat: true, prop: P_KEY, hR: [lerp(160, 196, g), 150] }) +
      figk([DOOR[0] + .75, 0, 1.2], 'rob', 0, { mouth: 'grin', blink: 0, look: [-6, 1], hL: [lerp(40, 10, g), 150] }) },
  ui: (t, i) => { let h = pillAt(540, 250, t, Lt(i).start + .05, nextStart(i), '🕵 INSIDE MAN', '#232838', '#fff', 60);
    h += labelAt([DOOR[0] - .6, 2.2, 1.0], PILL('GUARD', '#3f7fb5', '#fff', 44), t, wt(i, /guard/) - .1, nextStart(i));
    const a = wt(i, /copied/) - .1; if (t > a) h += `<div style="position:absolute;left:0;right:0;top:360px;text-align:center;z-index:2200;transform:scale(${pop(t, a, .35)})"><svg width="170" height="320" viewBox="0 0 80 150"><circle cx="40" cy="30" r="24" fill="#ffd166" stroke="${OL}" stroke-width="6"/><circle cx="40" cy="30" r="9" fill="#fff6dc" stroke="${OL}" stroke-width="5"/><path d="M34,52 L46,52 L46,140 L60,140 L60,128 L52,128 L52,118 L62,118 L62,104 L46,104" fill="#ffd166" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/></svg></div>` + pillAt(540, 720, t, a + .3, nextStart(i), '🔑 COPY OF THE KEY', '#ffd166', OL, 52);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, { k: 'ding', t: wt(i, /guard/) }, { k: 'click', t: wt(i, /copied/) }, { k: 'pop', t: wt(i, /copied/) + .3 }] };
SHOT.petrol = { set: S, light: 'ware',
  cam: i => { const c = wt(i, /demanded/) - .1; return [
    { t0: Lt(i).start, a: { pos: [IN[0] - 1.4, 2.4, IN[2] + 6.4], at: [IN[0] - 2.2, 1.2, IN[2] - 3], fov: 46 }, b: { pos: [IN[0] - 1.8, 2.1, IN[2] + 5.0], at: [IN[0] - 2.4, 1.1, IN[2] - 3], fov: 44 } },
    { t0: c, a: { pos: [IN[0] + 1.0, 2.0, IN[2] + 5.6], at: [IN[0] + 2.4, 2.0, IN[2] - 5.6], fov: 44 }, b: { pos: [IN[0] + 1.4, 2.1, IN[2] + 4.4], at: [IN[0] + 2.5, 2.1, IN[2] - 5.6], fov: 42 } }] },
  figs: (t, i) => { const c = wt(i, /demanded/) - .1; let h = '';
    if (t < c) { for (let k = 0; k < 3; k++) h += figk([IN[0] - 3.6 + k * .95, 0, IN[2] - 4.0 + (k % 2) * .3], 'staff', k, { mouth: 'o', talk: .3 + .2 * Math.sin(t * 9 + k), blink: bl(t, k), sweat: true, look: [3, 0], armL: [.05, .05], armR: [.05, .05] }, 1.7);
      const s = Math.sin(t * 5);
      h += figk([IN[0] - .9, 0, IN[2] - 1.6], 'rob', 0, { mouth: 'grin', blink: 0, look: [-5, 2], prop: P_CAN(-60 + 10 * s), hR: [40, 120], elR2: 'in' });
      h += figk([IN[0] + .4, 0, IN[2] - .6], 'rob', 1, { mouth: 'grin', blink: 0, look: [-5, 1], prop: P_MATCH, hR: [176, 90] }) }
    else { h += figk([IN[0] + 1.6, 0, IN[2] - 4.4], 'staff', 0, { mouth: 'o', blink: bl(t, 1), sweat: true, look: [4, -2], hR: [190, 60 + 6 * Math.sin(t * 20)], armL: [.05, .05] });
      h += figk([IN[0] + .6, 0, IN[2] - 3.2], 'rob', 2, { mouth: 'hmm', talk: .4 + .3 * Math.sin(t * 11), blink: 0, look: [4, -1], hR: [176, 120] }) }
    return h },
  ui: (t, i) => { const c = wt(i, /demanded/) - .1; let h = '';
    h += pillAt(540, 250, t, wt(i, /petrol/) - .1, c, '⛽ PETROL', '#e0303a', '#fff', 64) + pillAt(540, 370, t, wt(i, /staff/) - .05, c, '🔥 + A LIT MATCH', '#ff8a3d', '#fff', 50);
    if (t > c) { const d = Math.floor((t - c) * 7); const code = [3, 7, 1, 9, 4, 2].map((v, k) => k < Math.min(6, d) ? '?' : '–').join(' ');
      h += pillAt(540, 260, t, c, nextStart(i), '🔢 VAULT CODES', '#232838', '#fff', 60) + pillAt(540, 400, t, c + .15, nextStart(i), code, '#fff', OL, 76) }
    return h },
  sfx: i => [{ k: 'pop', t: wt(i, /petrol/) }, { k: 'swish', t: wt(i, /poured/), d: .5 }, { k: 'pop', t: wt(i, /staff/) }, { k: 'thud', t: wt(i, /demanded/), g: .5 }, ...[1, 2, 3, 4, 5].map(k => ({ k: 'tick', t: wt(i, /demanded/) + k * .14, f: 1600 }))] };
SHOT.gold = { set: S, light: (t, i) => t < wt(i, /found/) - .1 ? 'ware' : 'goldL',
  cam: i => { const c = wt(i, /found/) - .1; return [
    { t0: Lt(i).start, a: { pos: [IN[0] + 2.4, 2.2, IN[2] + 4.0], at: [IN[0] + 2.8, 2.0, IN[2] - 5.6], fov: 44 }, b: { pos: [IN[0] + 2.6, 2.2, IN[2] + 2.8], at: [IN[0] + 2.9, 2.1, IN[2] - 5.6], fov: 42 } },
    { t0: c, a: { pos: [GD[0] + .6, 3.6, GD[2] + 8.6], at: [GD[0], 1.0, GD[2] - 1.6], fov: 46 }, b: { pos: [GD[0] + .2, 2.4, GD[2] + 5.4], at: [GD[0], .9, GD[2] - 1.4], fov: 44 } }] },
  figs: (t, i) => { const c = wt(i, /found/) - .1; let h = '';
    if (t < c) return figk([IN[0] + 3.7, 0, IN[2] - 3.2], 'rob', 1, { mouth: 'hmm', blink: 0, look: [3, -2], prop: PROP.sack, hR: [170, 150] });
    [[-3.4, .6], [3.2, .9], [-1.9, -3.6]].forEach(([dx, dz], k) => h += figk([GD[0] + dx, 0, GD[2] + dz], 'rob', k, { mouth: t > wt(i, /tonnes/) ? 'o' : 'grin', talk: 0, blink: 0, look: [k == 0 ? 5 : -5, 3], prop: P_BAR, hR: [170, 110 + 14 * Math.sin(t * 6 + k)], hL: [30, 110] }));
    return h },
  ui: (t, i) => { const c = wt(i, /found/) - .1; let h = '';
    if (t < c + .2) { h += pillAt(540, 260, t, Lt(i).start + .05, c + .2, '💵 CASH?', '#35a862', '#fff', 72); h += stampAt(540, 410, t, wt(i, /but/) - .05, 'EXPECTED: ~£1M', '#232838', 62, -4, c + .2) }
    else { const a = wt(i, /tonnes/) - .2;
      h += pillAt(540, 250, t, c + .1, nextStart(i), '🥇 3 TONNES OF GOLD', '#ffd166', OL, 62);
      h += pillAt(540, 370, t, a + .3, nextStart(i), '6,800 BARS', '#232838', '#fff', 54);
      const m = wt(i, /million/) - .5, v = lerp(0, 26000000, ez(cl(t, m - .5, m + .7)));
      if (t > m - .5) h += pillAt(540, 520, t, m - .5, nextStart(i), MG.fmt(Math.round(v), 0, '£'), '#35a862', '#fff', 108) }
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, { k: 'error', t: wt(i, /but/) }, { k: 'shimmer', t: wt(i, /found/) }, { k: 'pop', t: wt(i, /tonnes/) + .1 }, { k: 'cash', t: wt(i, /million/) + .2 }] };
SHOT.police = { set: S, light: 'indoorWarm',
  cam: i => { const c = wt(i, /named/) - .15; return [
    { t0: Lt(i).start, a: { pos: [PO[0] + .4, 2.2, PO[2] + 7.4], at: [PO[0], 1.4, PO[2] - 1], fov: 44 }, b: { pos: [PO[0] + .2, 1.9, PO[2] + 6.0], at: [PO[0], 1.3, PO[2] - 1], fov: 42 } },
    { t0: c, a: { pos: [PO[0] - .9, 1.75, PO[2] + 3.6], at: [PO[0] - .9, 1.45, PO[2]], fov: 40 }, b: { pos: [PO[0] - .9, 1.7, PO[2] + 3.0], at: [PO[0] - .9, 1.45, PO[2]], fov: 38 } }] },
  figs: (t, i) => { const c = wt(i, /named/) - .15;
    return fig([PO[0] - .9, 0, PO[2] + .2], 'black', { mouth: t > c ? 'o' : 'sad', talk: t > c ? .5 + .4 * Math.sin(t * 10) : 0, blink: bl(t, 1), sweat: true, look: [5, 1], hR: t > c ? [186, 140 + 10 * Math.sin(t * 6)] : null }) +
      fig([PO[0] + 1.0, 0, PO[2] - 1.9], 'bobby', { mouth: 'hmm', talk: t < c ? tk(t, i) * .5 : 0, blink: bl(t, 2), look: [-6, 2], hR: [176, 110] }) +
      fig([PO[0] + 2.4, 0, PO[2] - 1.5], 'dsuit', { mouth: 'hmm', blink: bl(t, 3), look: [-6, 2], prop: PROP.magnifier, hR: [150, 80] }) },
  ui: (t, i) => { const c = wt(i, /named/) - .15; let h = '';
    h += pillAt(540, 250, t, Lt(i).start + .05, nextStart(i), '🚓 POLICE', '#232838', '#fff', 64);
    h += stampAt(540, 400, t, wt(i, /suspected/) - .05, 'SUSPECT', '#e0303a', 96, -6, c);
    if (t > c) { const a = wt(i, /brother/) - .2, hd = (bg, face) => `<svg width="130" height="130" viewBox="0 0 60 60"><circle cx="30" cy="30" r="25" fill="${bg}" stroke="${OL}" stroke-width="5"/>${face}</svg>`;
      const g = hd('#fff', `<circle cx="23" cy="29" r="3.5" fill="${OL}"/><circle cx="37" cy="29" r="3.5" fill="${OL}"/><path d="M14,18 Q30,4 46,18" stroke="#5a3a24" stroke-width="8" fill="none"/>`), r = hd('#23232c', `<rect x="15" y="22" width="30" height="13" rx="6" fill="#f7e4b5"/><circle cx="23" cy="28.5" r="3" fill="${OL}"/><circle cx="37" cy="28.5" r="3" fill="${OL}"/>`);
      h += `<div style="position:absolute;left:0;right:0;top:360px;text-align:center;z-index:2200;transform:scale(${pop(t, c, .35)})"><span style="display:inline-block;vertical-align:middle">${g}<br>${PILL('GUARD', '#3f7fb5', '#fff', 40)}</span>` +
        `<span style="display:inline-block;vertical-align:middle;margin:0 18px;font:900 80px IB,Arial;color:#ffd166;text-shadow:${shadowTxt(OL, 5)};transform:scale(${pop(t, a, .3)})">↔</span>` +
        `<span style="display:inline-block;vertical-align:middle;transform:scale(${pop(t, a, .3)})">${r}<br>${PILL('ROBBER', '#e0303a', '#fff', 40)}</span></div>`;
      h += pillAt(540, 720, t, a + .15, nextStart(i), '👨‍👦 BROTHER-IN-LAW', '#ffd166', OL, 54) }
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, { k: 'impact', t: wt(i, /suspected/), g: .5 }, { k: 'pop', t: wt(i, /named/) }, { k: 'ding', t: wt(i, /brother/) }] };
SHOT.prison = { set: S, light: (t, i) => t < wt(i, /most/i) - .15 ? 'vault' : 'goldL',
  cam: i => { const c = wt(i, /most/i) - .15; return [
    { t0: Lt(i).start, a: { pos: [PR[0], 1.8, PR[2] + 6.4], at: [PR[0], 1.1, PR[2] - 1], fov: 46 }, b: { pos: [PR[0], 1.6, PR[2] + 5.6], at: [PR[0], 1.0, PR[2] - 1], fov: 44 } },
    { t0: c, a: { pos: [SM[0] - .5, 3.2, SM[2] + 11.0], at: [SM[0] - .3, 1.4, SM[2] - 1.8], fov: 46 }, b: { pos: [SM[0] - .5, 2.9, SM[2] + 9.6], at: [SM[0] - .3, 1.3, SM[2] - 1.8], fov: 45 } }] },
  figs: (t, i) => { const c = wt(i, /most/i) - .15; let h = '';
    if (t < c) { for (let k = 0; k < 2; k++) h += figk([PR[0] - .7 + k * 1.4, 0, PR[2] - 1.0], 'prisoner', k, { mouth: 'sad', blink: bl(t, k), look: [0, 3] }, 1.7); return h }
    return fig([SM[0] + .3, 0, SM[2] - .4], 'smock', { mouth: 'hmm', blink: bl(t, 4), look: [-6, -1], prop: P_BAR, hR: [40 + 10 * Math.sin(t * 4), 120], elR2: 'in', hat: HAIRS[1] }) },
  ui: (t, i) => { const c = wt(i, /most/i) - .15; let h = '';
    if (t < c) { for (let k = 0; k < 7; k++) h += `<div style="position:absolute;left:${110 + k * 140}px;top:0;width:28px;height:1290px;background:linear-gradient(90deg,#2a2a33,#6a6a76 45%,#2a2a33);border:4px solid ${OL};border-top:0;border-radius:0 0 14px 14px;z-index:1500"></div>`;
      h += stampAt(540, 260, t, Lt(i).start + .15, '2 × 25 YEARS', '#e0303a', 104, -6, c); return h }
    h += pillAt(540, 250, t, c + .05, nextStart(i), '🔥 MELTED DOWN', '#ff8a3d', '#fff', 60);
    h += stampAt(540, 420, t, wt(i, /never/) - .05, 'NEVER FOUND', '#e0303a', 104, -6);
    return h },
  sfx: i => [{ k: 'thud', t: Lt(i).start + .05, g: .6 }, { k: 'impact', t: wt(i, /twenty/), g: .6 }, { k: 'whoosh', t: wt(i, /most/i) - .15, d: .4 }, { k: 'impact', t: wt(i, /never/), g: .6 }] };
SHOT.jewel = { set: S, light: 'shop',
  cam: i => ({ a: { pos: [JW[0] + 1.2, 2.2, JW[2] + 7.0], at: [JW[0] + .2, 1.3, JW[2] - 1], fov: 44 }, b: { pos: [JW[0] + .9, 1.9, JW[2] + 5.4], at: [JW[0] + .2, 1.3, JW[2] - 1], fov: 42 } }),
  figs: (t, i) => { const a = wt(i, /wearing/) - .1;
    return fig([JW[0] - .2, 0, JW[2] - 2.6], 'jeweller', { mouth: 'smile', blink: bl(t, 0), look: [2, 2], hR: [170, 140] }) +
      fig([JW[0] + 1.0, 0, JW[2] + .7], 'shopper', { mouth: t > a ? 'o' : 'smile', blink: bl(t, 1), look: [t > a ? 0 : -4, t > a ? 0 : 1], sweat: t > a, prop: P_RING, hR: [150, 150] }) },
  ui: (t, i) => { let h = pillAt(540, 250, t, wt(i, /jewelry/) - .1, nextStart(i), '💍 GOLD JEWELRY', '#ffd166', OL, 60);
    h += pillAt(540, 370, t, wt(i, /britain/i) - .1, nextStart(i), '🇬🇧 BOUGHT AFTER 1983', '#232838', '#fff', 50);
    const a = wt(i, /wearing/) - .1; if (t > a) h += bigText(540, 560, t, a, nextStart(i), "BRINK'S-MAT<br>GOLD?", 104, '#ffd166', -4);
    return h },
  sfx: i => [{ k: 'shimmer', t: wt(i, /jewelry/) }, { k: 'pop', t: wt(i, /britain/i) }, { k: 'impact', t: wt(i, /wearing/), g: .5 }] };
SHOT.end = { set: S, light: 'dawn', cam: i => ({ a: HERO_B, b: HERO_A }),
  upd: (t, i) => planeAt(t + 3.2, 24, -34, 8),
  figs: (t, i) => gangOut(t),
  ui: (t, i) => { const t0 = Lt(i).start, k = pop(t, t0 + .1, .4);
    const btn = (txt, bg, d) => `<div style="flex:1;text-align:center;font:900 64px/1 IB,Arial;color:#fff;background:${bg};border:7px solid ${OL};border-radius:26px;padding:22px 0;text-shadow:${shadowTxt(OL, 3)};transform:scale(${pop(t, t0 + d, .3)})">${txt}</div>`;
    const o = fade(t, MG.TL.dur - .35, MG.TL.dur - .05);
    return `<div style="position:absolute;left:90px;right:90px;top:250px;opacity:${o};transform:scale(${k});background:#fff;border:8px solid ${OL};border-radius:34px;box-shadow:0 14px 0 #2328384d;padding:30px 34px;text-align:center;z-index:2200">
    <div style="font:900 62px/1.1 IB,Arial;color:${OL}">Would you still wear it? 💍</div>
    <div style="display:flex;gap:30px;margin-top:26px">${btn('YES', '#35a862', .35)}${btn('NO', '#e0303a', .5)}</div></div>` },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'pop', t: Lt(i).start + .45 }, { k: 'pop', t: Lt(i).start + .6 }] };
