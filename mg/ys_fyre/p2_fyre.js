// ===================== Set FY: Fyre Festival 2017 (Camp mit Zelten, Versprechen-Villa, Flughafen, Gefaengnis) =====================
const S = 'FY';
LIGHT.sunny = { sun: [.55, .78, .35], sunCol: '#fff4dc', sky: '#cfeaff', gnd: '#e8d2a0', fog: '#bfe3fa', fogN: 80, fogF: 300, shCol: '#7f95e0', bg: 'linear-gradient(#3f8fe0 0%,#7cc0f4 45%,#c8ecff 100%)' };
LIGHT.gold = { sun: [.7, .4, .35], sunCol: '#ffd9a0', sky: '#ffd6b0', gnd: '#e8c08a', fog: '#ffcf9c', fogN: 80, fogF: 300, shCol: '#8a7ad0', bg: 'linear-gradient(#5a6fd0 0%,#c48ac8 35%,#ffb27a 70%,#ffd9a0 100%)' };
LIGHT.grey = { sun: [.45, .8, .4], sunCol: '#eef2f6', sky: '#c6d4e2', gnd: '#c8b894', fog: '#c2d0de', fogN: 60, fogF: 220, shCol: '#7c88b8', bg: 'linear-gradient(#7d93b4 0%,#a9bcd2 50%,#d6e0ea 100%)' };
LIGHT.cell = { sun: [.3, .85, .45], sunCol: '#eef2ff', sky: '#c4cce6', gnd: '#5a5e70', fog: '#3a4058', fogN: 50, fogF: 160, shCol: '#7a84b8', bg: '#2a3044' };
const VL = [0, 0, -150], AP = [150, 0, 0], PR = [-150, 0, 0];
const TB = [2.4, 0, 3.2];          // Klapptisch mit Styropor-Box
(function world() {
  // Meer ueberall
  const g = new G.Geo(), NR = 40, NS = 90, k = G.hex('#1d9bd3');
  const P = (i, j) => { const r = 2 + 420 * Math.pow(i / NR, 2.0), a = (j + (i % 2) * .5) / NS * 6.2832; return [Math.cos(a) * r, -.45, Math.sin(a) * r] };
  for (let i = 0; i < NR; i++) for (let j = 0; j < NS; j++) { const a = P(i, j), b = P(i, j + 1), c = P(i + 1, j + 1), d = P(i + 1, j); g.tri(a, b, c, k); g.tri(a, c, d, k) }
  mk(S, g, { wave: .22, foam: 0, cast: false, recv: true });
  // Inseln (Sand), Oberkante y=0
  mk(S, G.box(90, .6, 46, '#f1dba6', { base: true }), { pos: [0, -.6, 9], outline: false });
  mk(S, G.box(60, .6, 34, '#f4e0ae', { base: true }), { pos: [VL[0], -.6, VL[2] + 8], outline: false });
  mk(S, G.box(70, .6, 50, '#c9c2b0', { base: true }), { pos: [AP[0], -.6, AP[2] + 8], outline: false });
  mk(S, G.box(30, .6, 34, '#5a5e6a', { base: true }), { pos: [PR[0], -.6, PR[2] + 8], outline: false });
})();
function palm(x, z, hgt, lean, yaw, seed) {
  const g = new G.Geo(), seg = 8; let px = 0, py = 0;
  for (let i = 0; i < seg; i++) {
    const u = i / seg, r0 = .28 - .1 * u, r1 = .28 - .1 * (u + 1 / seg), sh = hgt / seg;
    const c = G.cyl(r0, r1 * 1.12, sh * 1.02, 10, i % 2 ? '#a4744a' : '#94683f', { rot: i * .4, open: true }).smooth();
    const bx = lean * u * u * hgt * .35, bx1 = lean * (u + 1 / seg) * (u + 1 / seg) * hgt * .35;
    g.add(c, G.m4.compose([bx, i * sh, 0], [0, 0, -(bx1 - bx) / sh], 1)); px = bx1; py = (i + 1) * sh;
  }
  for (let i = 0; i < 8; i++) { const lf = G.leaf(2.6 + .5 * G.hash(i, seed), .42, .55 + .2 * G.hash(seed, i), i % 2 ? '#3fae49' : '#55c457'); g.add(lf, G.m4.compose([px, py, 0], [0, i / 8 * 6.2832 + seed, -.25 + .25 * G.hash(i * 3, seed)], 1)) }
  for (let i = 0; i < 3; i++) g.add(G.ico(.2, 2, '#6b4426', .06, i).smooth(), G.m4.compose([px + Math.cos(i * 2.1) * .25, py - .25, Math.sin(i * 2.1) * .25]));
  return mk(S, g, { pos: [x, -.05, z], rot: [0, yaw, 0] });
}
// ---------- Camp (Realitaet) ----------
const TENTS = [];
(function camp() {
  [[-13, -11, 5.4], [-7, -12.5, 6], [9, -12, 5.2], [15, -10.5, 6.2], [-18, -4, 4.8], [19, -3, 5], [-21, 8, 5.6], [22, 9, 5]].forEach(([x, z, h], k) => palm(x, z, h, 1 + (k % 3) * .15, k * 1.3, k + 1));
  const T = [];
  const tent = (x, z, r = 0) => { const m = G.m4.compose([x, 0, z], [0, r, 0], [1, 1, 1]);
    T.push([G.box(3.0, 1.5, 3.0, '#e6eaee', { base: true }), m], [G.cyl(2.15, 0, 1.25, 4, '#d4dae2', { rot: PI / 4 }), G.m4.compose([x, 1.5, z], [0, r, 0], [1, 1, 1])],
      [G.box(.9, 1.2, .06, '#5a6474', { base: true }), G.m4.mul(m, G.m4.compose([0, 0, 1.52]))], [G.box(3.04, .12, 3.04, '#9aa6b6', { base: true }), G.m4.mul(m, G.m4.compose([0, 1.25, 0]))]) };
  for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) { const x = -8.5 + c * 3.6 + (r % 2) * 1.5, z = -2.5 - r * 4.0; tent(x, z, (G.hash(r, c) - .5) * .25); TENTS.push([x, z]) }
  mk(S, merge(T).vary(.03, 5));
  // nasse Matratzen
  const M = [[-3.4, .4, .2], [-1.2, 1.4, -.3], [5.2, .8, .5], [7.2, 2.2, .1]].map(([x, z, r]) => at(G.box(1.9, .22, .95, '#7fa6d4', { base: true, top: '#6f97c8' }), [x, 0, z], [0, r, 0]));
  M.push(at(G.box(1.9, .22, .95, '#7fa6d4', { base: true }), [-6.0, .45, .6], [1.15, .3, 0]));
  mk(S, merge(M));
  mk(S, merge([[-3.2, .5], [-1.0, 1.5], [5.4, .9], [7.0, 2.3]].map(([x, z], k) => at(G.ico(.36, 1, '#4f7fb6'), [x + .2, .23, z], [0, k, 0], [1.2, .08, .8]))), { outline: false, cast: false });
  // Pfuetzen
  mk(S, merge([[1.6, 5.2, .8], [-4.6, 3.6, .6], [6.4, 4.8, .7]].map(([x, z, s]) => at(G.ico(s, 2, '#9fb4c4'), [x, .01, z], [0, 0, 0], [1.4, .01, .7]))), { outline: false, cast: false, spec: 1 });
  // Kisten/Muell
  mk(S, merge([[-9, 1.2], [-8.2, 1.9], [10.2, .4], [11, 1.4]].map(([x, z], k) => at(G.box(.9, .7, .8, k % 2 ? '#c49a62' : '#b48a56', { base: true }), [x, 0, z], [0, k * .5, 0]))).vary(.04, 9));
  // Klapptisch + Styropor-Boxen
  mk(S, merge([at(G.box(2.2, .08, 1.1, '#d8d8d2', { base: true }), [TB[0], .88, TB[2]]), ...[[-1, -.45], [1, -.45], [-1, .45], [1, .45]].map(([x, z]) => at(G.box(.06, .88, .06, '#6a6e78', { base: true }), [TB[0] + x, 0, TB[2] + z]))]));
  mk(S, merge([at(G.box(.62, .2, .62, '#f6f6f2', { base: true }), [TB[0] + .7, .96, TB[2] - .1]), at(G.box(.62, .2, .62, '#f6f6f2', { base: true }), [TB[0] + .72, 1.16, TB[2] - .1], [0, .2, 0])]));
})();
// Sandwich-Box (Hauptobjekt, Deckel klappt auf)
const BOXP = [TB[0] - .35, .96, TB[2]];
const BOX = mk(S, merge([at(G.box(.9, .26, .9, '#fbfbf7', { base: true }), [0, 0, 0]), at(G.box(.8, .04, .8, '#ececE4', { base: true }), [0, .25, 0])]), { pos: BOXP });
const SAND = mk(S, merge([at(G.box(.62, .1, .62, '#f3dcaa', { base: true, top: '#ead09a' }), [0, .0, 0]), at(G.box(.66, .035, .66, '#ffcf3a', { base: true }), [0, .1, 0], [0, PI / 4, 0]),
  at(G.box(.62, .1, .62, '#f3dcaa', { base: true, top: '#e2c286' }), [0, .135, 0])]).smooth(), { pos: [BOXP[0], BOXP[1] + .29, BOXP[2]] });
const LETT = mk(S, merge([[-.26, -.2], [.2, .26], [.3, -.16]].map(([x, z], k) => at(G.ico(.14, 1, '#5fc451'), [x, .12, z], [0, k, 0], [1.3, .12, .8]))), { pos: [BOXP[0], BOXP[1] + .28, BOXP[2]], outline: false });
// Deckel: Scharnier-Kante bei z=0
const LIDG = mk(S, merge([at(G.box(.9, .2, .9, '#f4f4ee', { base: true }), [0, 0, .45])]), { pos: [BOXP[0], BOXP[1] + .26, BOXP[2] - .45] });
function lidOpen(a) { LIDG.rot = [-a, 0, 0] }
// ---------- Villa (Versprechen) ----------
(function villa() {
  [[-12, -8, 5.6], [-8.5, -10, 4.6], [10, -9, 6], [14, -6, 5], [-15, 2, 5.2], [16, 3, 4.6]].forEach(([x, z, h], k) => palm(VL[0] + x, VL[2] + z, h, 1.1, k * 1.7, k + 20));
  const V = [at(G.box(10, 3.4, 6, '#fbf7f0', { base: true }), [VL[0], 0, VL[2] - 4]), at(G.box(11.4, .35, 7.4, '#e8dcc8', { base: true }), [VL[0], 3.4, VL[2] - 3.6]),
    at(G.box(5, 2.4, 4.4, '#fbf7f0', { base: true }), [VL[0] + 1.5, 3.75, VL[2] - 4.4]), at(G.box(6.0, .3, 5.4, '#e8dcc8', { base: true }), [VL[0] + 1.5, 6.15, VL[2] - 4.2]),
    at(G.box(13, .25, 4, '#d9c7a6', { base: true }), [VL[0], 0, VL[2] + 1.0])];
  // Liegen
  [-4.2, -2.2, 3.2, 5.2].forEach(x => V.push(at(G.box(.8, .3, 2.0, '#ffffff', { base: true }), [VL[0] + x, .25, VL[2] + 4.6]), at(G.box(.8, .1, .7, '#ff8a6a', { base: true }), [VL[0] + x, .55, VL[2] + 3.9], [.5, 0, 0])));
  mk(S, merge(V).vary(.01, 3));
  mk(S, merge([[-3, 1.5, -.95], [0, 1.5, -.95], [3, 1.5, -.95]].map(([x, y]) => at(G.box(2.2, 2.2, .1, '#ffd98a', { base: true }), [VL[0] + x, .4, VL[2] - .95])).concat([at(G.box(3.2, 1.6, .1, '#ffd98a', { base: true }), [VL[0] + 1.5, 4.2, VL[2] - 2.15])])), { emis: .9, outline: false, cast: false });
  // Pool
  mk(S, G.box(8, .1, 2.6, '#2fc4e8', { base: true }), { pos: [VL[0], .02, VL[2] + 2.0], spec: 1, emis: .25, outline: false });
  // Sonnenschirme
  [-3.2, 4.2].forEach((x, k) => { mk(S, G.cyl(.05, .05, 2.4, 8, '#ddd'), { pos: [VL[0] + x, 0, VL[2] + 5.6], cast: false }); mk(S, G.cyl(1.4, 0, .6, 12, k ? '#ff5d7a' : '#ffd166'), { pos: [VL[0] + x, 2.2, VL[2] + 5.6] }) });
  // Gourmet-Tisch mit Cloche
  mk(S, merge([at(G.cyl(.9, .9, .08, 20, '#ffffff'), [VL[0] - 6.5, .9, VL[2] + 3.0]), at(G.cyl(.08, .08, .9, 8, '#c9ccd4'), [VL[0] - 6.5, 0, VL[2] + 3.0]),
    at(G.cyl(.5, .5, .03, 20, '#f2f2f2'), [VL[0] - 6.5, .98, VL[2] + 3.0])]));
  mk(S, G.ico(.42, 2, '#d8dce6', 0, 1, .8).smooth(), { pos: [VL[0] - 6.5, 1.0, VL[2] + 3.0], spec: 1, scl: [1, 1, 1] });
  // Yacht
  mk(S, merge([at(G.box(6, .9, 1.8, '#ffffff', { base: true }), [0, 0, 0]), at(G.box(3, .8, 1.4, '#eef2f6', { base: true }), [-.6, .9, 0]), at(G.box(2.6, .3, 1.42, '#2a3a5a'), [-.6, 1.3, 0])]).vary(.01, 4), { pos: [VL[0] + 14, -.1, VL[2] - 22], rot: [0, .3, 0] });
})();
// ---------- Flughafen ----------
(function airport() {
  [[-16, -8, 5], [16, -9, 5.4], [-20, 4, 4.6]].forEach(([x, z, h], k) => palm(AP[0] + x, AP[2] + z, h, 1, k * 2.1, k + 40));
  const A = [at(G.box(22, 4.4, 7, '#f2e6cc', { base: true }), [AP[0], 0, AP[2] - 6]), at(G.box(23, .4, 8.4, '#c0603a', { base: true }), [AP[0], 4.4, AP[2] - 5.6]),
    at(G.box(6, 3.0, .1, '#2a4a6a', { base: true }), [AP[0], 0, AP[2] - 2.45])];
  [-10, -6, 6, 10].forEach(x => A.push(at(G.box(.3, 4.4, .3, '#e0d2b4', { base: true }), [AP[0] + x, 0, AP[2] - 2.3])));
  mk(S, merge(A).vary(.02, 8));
  texPlane(S, 5.2, 1.0, () => tex(520, 100, (c, wd, ht) => { c.fillStyle = '#232838'; c.fillRect(0, 0, wd, ht); c.fillStyle = '#ffd166'; c.font = '900 64px IB,Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('DEPARTURES', wd / 2, ht / 2 + 4) }), { pos: [AP[0], 3.7, AP[2] - 2.38] });
  // Koffer-Stapel
  mk(S, merge([[-4, 2], [-3.4, 2.6], [3.8, 1.6], [4.6, 2.4], [5.2, 1.8]].map(([x, z], k) => at(G.box(.7, .9, .35, ['#e0303a', '#3f7fb5', '#ffd166', '#35a862', '#d35fa0'][k], { base: true }), [AP[0] + x, 0, AP[2] + z], [0, k * .6, 0]))));
})();
// ---------- Gefaengnis ----------
mk(S, merge([at(G.box(20, 6, .4, '#8a8e98', { base: true }), [PR[0], 0, PR[2] - 3]), at(G.box(8, .5, .8, '#6a6e78', { base: true }), [PR[0], 0, PR[2] - 2.4]),
  at(G.box(1.2, .9, .1, '#2a2e3a', { base: true }), [PR[0] - 2, 3.6, PR[2] - 2.75])]).vary(.03, 23), { outline: false });
// Flugzeug (generisch, keine Airline)
const PLANE = (function () {
  const WH = '#eef1f5', BL = '#ff8a3d', GR = '#aab3c2';
  const root = mk(S, merge([
    at(G.cyl(1.9, 1.9, 34, 22, WH), [-17, 0, 0], [0, 0, -PI / 2]), at(G.cyl(1.9, .3, 5.5, 22, WH), [17, 0, 0], [0, 0, -PI / 2]), at(G.cyl(1.9, .7, 6, 22, WH), [-17, 0, 0], [0, 0, PI / 2]),
    at(G.box(33, .4, 3.88, BL), [0, .2, 0]), at(G.box(2.2, .55, 2.9, '#1d2a44'), [18.2, .5, 0], [0, 0, -.25]),
    at(G.box(5, .3, 30, GR), [-1, -1.2, 0]), at(G.box(4.4, 6.2, .36, BL, { base: true }), [-20.6, .8, 0], [0, 0, .45]), at(G.box(2.6, .26, 10, GR), [-22.4, .8, 0]),
    at(G.cyl(1.0, 1.0, 3.4, 16, GR), [.6, -2.4, 7], [0, 0, PI / 2]), at(G.cyl(1.0, 1.0, 3.4, 16, GR), [.6, -2.4, -7], [0, 0, PI / 2])]).vary(.02, 3), { pos: [0, 30, -20], cast: false });
  return root;
})();
function planeAt(t, x0, y0, z0, sp = 9, dy = -.08, yaw = 0) { const d = t * sp; PLANE.pos = [x0 + d * Math.cos(yaw), y0 + d * dy, z0 - d * Math.sin(yaw)]; PLANE.rot = [0, yaw, dy * .8] }
// ---------- Figuren-Looks ----------
const HAIRS = [`<path d="M40,60 Q44,14 100,16 Q156,14 160,60 Q140,34 100,36 Q60,34 40,60Z" fill="#5a3a24" stroke="${OL}" stroke-width="5"/>`, `<path d="M42,56 Q56,22 100,22 Q144,22 158,56 Q124,40 100,42 Q76,40 42,56Z" fill="#2a2a30" stroke="${OL}" stroke-width="5"/>`,
  `<path d="M44,50 Q60,24 100,24 Q140,24 156,50 Q120,38 100,40 Q80,38 44,50Z" fill="#8a6a3a" stroke="${OL}" stroke-width="5"/>`,
  `<path d="M38,70 Q30,10 100,12 Q170,10 162,70 L164,130 Q150,100 150,60 Q100,44 50,60 Q50,100 36,130Z" fill="#c9843a" stroke="${OL}" stroke-width="5"/>`,
  `<path d="M38,70 Q30,10 100,12 Q170,10 162,70 L166,150 Q150,110 150,60 Q100,44 50,60 Q50,110 34,150Z" fill="#2a2228" stroke="${OL}" stroke-width="5"/>`];
const SHADES = `<path d="M62,80 L96,80 Q96,100 80,100 Q64,100 62,80Z M104,80 L138,80 Q136,100 120,100 Q104,100 104,80Z" fill="#232838" stroke="${OL}" stroke-width="3"/><path d="M96,83 L104,83" stroke="${OL}" stroke-width="4"/><path d="M68,84 L76,84" stroke="#fff" stroke-width="3" opacity=".6"/>`;
const FLOWERS = `<circle cx="74" cy="182" r="7" fill="#ffd166"/><circle cx="122" cy="196" r="7" fill="#fff"/><circle cx="96" cy="216" r="7" fill="#ff5d7a"/><circle cx="130" cy="172" r="6" fill="#ffd166"/>`;
const LANY = `<path d="M80,152 L100,200 L120,152" stroke="#ff8a3d" stroke-width="6" fill="none"/><rect x="88" y="196" width="24" height="30" rx="4" fill="#fff" stroke="${OL}" stroke-width="3"/><rect x="92" y="202" width="16" height="6" fill="#ff8a3d"/>`;
const STRIPES = `<rect x="56" y="176" width="88" height="10" fill="#555"/><rect x="54" y="206" width="92" height="10" fill="#555"/>`;
const GUESTC = ['#3fb6c8', '#ff7a8a', '#ffd166', '#8ad06a', '#b58ae0', '#ff9a4a'];
Object.assign(LOOK, {
  guest: k => ({ sw: GUESTC[k % 6], swd: '#00000022', pa: ['#f2efe6', '#3a4a6a', '#d6c6a0'][k % 3], hat: HAIRS[k % 5] + (k % 3 == 1 ? SHADES : ''), mid: FLOWERS + LANY }),
  model: k => ({ sw: ['#ffffff', '#ff5d7a', '#ffd166'][k % 3], swd: '#e8e0e8', pa: ['#f6e6c8', '#ffffff', '#3fb6c8'][k % 3], hat: HAIRS[[3, 4, 0][k % 3]] + SHADES }),
  founder: { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', hat: HAIRS[1], mid: MID.tie },
  convict: { sw: '#d0d0d0', swd: '#9a9a9a', pa: '#9a9a9a', hat: HAIRS[1], mid: STRIPES },
});
const L_ = (who, k) => { const v = LOOK[who]; return typeof v == 'function' ? v(k) : v };
function figk(p, who, k, o = {}, H3 = 1.75, clipY = null) { const look = L_(who, k); const sv = LOOK.__tmp; LOOK.__tmp = look; const h = fig(p, '__tmp', o, H3, clipY); LOOK.__tmp = sv; return h }
const P_BOX = `<g transform="translate(-34,-30)"><path d="M0,30 L68,30 L62,58 L6,58Z" fill="#fbfbf7" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/><path d="M8,30 Q34,14 60,30" fill="#f3dcaa" stroke="${OL}" stroke-width="4"/><path d="M10,28 L58,28 L54,34 L14,34Z" fill="#ffcf3a" stroke="${OL}" stroke-width="3"/><path d="M0,30 L10,-4 L66,-4 L68,30" fill="#f4f4ee" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/></g>`;
const P_CASE = c => `<g transform="translate(-26,-4)"><rect x="0" y="10" width="52" height="64" rx="8" fill="${c}" stroke="${OL}" stroke-width="5"/><path d="M16,10 L16,0 L36,0 L36,10" stroke="${OL}" stroke-width="5" fill="none"/></g>`;
const P_PHONE = `<g transform="translate(-14,-40) rotate(-8)"><rect x="0" y="0" width="30" height="54" rx="6" fill="#232838" stroke="${OL}" stroke-width="3"/><rect x="4" y="6" width="22" height="22" fill="#ff8a3d"/></g>`;
// ---------- Shots ----------
const HERO_A = { pos: [-.4, 2.0, 9.4], at: [.6, 1.5, -2], fov: 52 }, HERO_B = { pos: [0, 1.9, 8.2], at: [.6, 1.5, -2], fov: 50 };
const heroFigs = (t, sad = true) => {
  let h = '';
  for (let k = 0; k < 4; k++) { const x = [-4.4, 3.4, -2.2, 5.6][k], z = [-.8, -1.2, -1.8, .2][k];
    h += figk([x, 0, z], 'guest', k + 1, { mouth: k % 2 ? 'o' : 'sad', blink: bl(t, k), look: [k % 2 ? -4 : 4, 0], sweat: k == 1, prop: k == 2 ? P_CASE('#3f7fb5') : '', hR: k == 0 ? [170, 60 + 8 * Math.sin(t * 3 + k)] : null }) }
  h += figk([.5, 0, 1.4], 'guest', 0, { mouth: 'sad', blink: bl(t, 7), look: [0, 2], sweat: true, prop: P_BOX, hR: [150, 150], tilt: .06 * Math.sin(t * 1.5) });
  return h };
SHOT.hero = { set: S, light: 'grey', cam: i => ({ a: HERO_A, b: HERO_B }), figs: (t, i) => heroFigs(t), sfx: i => [{ k: 'pop', t: .2 }] };
SHOT.phone = { set: S, light: 'sunny',
  cam: i => ({ a: { pos: [VL[0] - 2, 2.2, VL[2] + 16], at: [VL[0], 2.6, VL[2] - 2], fov: 50 }, b: { pos: [VL[0] + 1.5, 2.0, VL[2] + 13], at: [VL[0], 2.4, VL[2] - 2], fov: 48 } }),
  figs: (t, i) => { let h = ''; for (let k = 0; k < 3; k++) { const s = Math.sin(t * 6 + k * 2); h += figk([VL[0] - 3 + k * 3, 0, VL[2] + 4.2 + (k % 2) * .6], 'model', k, { mouth: 'grin', blink: 0, look: [0, 1], bob: Math.abs(s) * 8, hR: [190, 40 + 20 * s], hL: [10, 60 - 20 * s], prop: k == 1 ? P_PHONE : '' }) } return h },
  ui: (t, i) => { const t0 = Lt(i).start, a = t0 + .15, f = wt(i, /fyre/i) - .1; let h = '';
    h += pillAt(540, 230, t, t0 + .05, nextStart(i), '📍 BAHAMAS · 2017', '#232838', '#fff', 50);
    if (t > a) { const k = pop(t, a, .4), y = lerp(1400, 330, ez(cl(t, a, a + .45)));
      let heads = ''; for (let n = 0; n < 3; n++) heads += `<svg width="78" height="78" viewBox="0 0 60 60" style="margin:0 3px;transform:scale(${pop(t, wt(i, /models/) - .1 + n * .08, .25)})"><circle cx="30" cy="30" r="25" fill="#f7e4b5" stroke="${OL}" stroke-width="4"/><path d="M14,26 L27,26 Q27,34 20,34 Q14,34 14,26Z M33,26 L46,26 Q46,34 40,34 Q33,34 33,26Z" fill="${OL}"/><path d="M22,42 Q30,47 38,42" stroke="${OL}" stroke-width="3" fill="none"/></svg>`;
      const hr = wt(i, /luxury/) - .1, likes = t > hr ? Math.floor(lerp(0, 999, ez(cl(t, hr, hr + 1.2)))) : 0;
      h += `<div style="position:absolute;left:250px;top:${y}px;width:580px;height:880px;background:#fff;border:10px solid ${OL};border-radius:60px;box-shadow:0 18px 0 #2328384d;overflow:hidden;z-index:2200">
        <div style="padding:26px 26px 10px;display:flex;align-items:center;gap:6px">${heads}<span style="margin-left:10px;font:900 34px IB,Arial;color:${OL}">TOP MODELS</span></div>
        <div style="margin:10px 26px;height:528px;background:linear-gradient(135deg,#ff9a3d,#ff6a1a);border:5px solid ${OL};border-radius:18px;transform:scale(${pop(t, a + .3, .4)})"></div>
        <div style="padding:6px 30px;font:900 46px IB,Arial;color:#e0303a">♥ <span style="color:${OL};font-size:40px">${likes ? MG.fmt(likes, 0, '') + 'K' : ''}</span></div>
        <div style="padding:0 30px;font:700 34px P,Arial;color:${OL};opacity:${cl((t - f) * 4, 0, 1)}">Fyre Festival 🌴</div></div>` }
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, { k: 'whoosh', t: Lt(i).start + .15, d: .5 }, { k: 'pop', t: wt(i, /models/) }, { k: 'ding', t: wt(i, /luxury/) }, { k: 'wave', t: Lt(i).start + .3 }] };
SHOT.promise = { set: S, light: 'gold',
  cam: i => { const c = wt(i, /gourmet/) - .1; return [
    { t0: Lt(i).start, a: { pos: [VL[0] + 6, 4.5, VL[2] + 18], at: [VL[0], 2.6, VL[2] - 3], fov: 50 }, b: { pos: [VL[0] + 3, 3.0, VL[2] + 12], at: [VL[0], 2.4, VL[2] - 3], fov: 48 } },
    { t0: c, a: { pos: [VL[0] - 5.4, 2.6, VL[2] + 7.6], at: [VL[0] - 7.0, 1.0, VL[2] + 2.8], fov: 44 }, b: { pos: [VL[0] - 5.6, 2.4, VL[2] + 6.8], at: [VL[0] - 7.0, 1.0, VL[2] + 2.8], fov: 42 } }] },
  upd: (t, i) => {},
  figs: (t, i) => { const c = wt(i, /gourmet/) - .1; if (t > c) return figk([VL[0] - 8.3, 0, VL[2] + 2.2], 'guest', 3, { mouth: 'grin', blink: bl(t, 2), look: [5, 2], hR: [176, 110] }, 1.75);
    let h = ''; for (let k = 0; k < 3; k++) h += figk([VL[0] - 3.4 + k * 3.2, .25, VL[2] + 4.6 + (k % 2) * .3], 'model', k + 1, { mouth: 'smile', blink: bl(t, k), look: [0, -1] }); return h },
  ui: (t, i) => { let h = '';
    h += pillAt(540, 360, t, wt(i, /villas/) - .2, nextStart(i), '🏝 LUXURY VILLAS', '#ffd166', OL, 54);
    h += pillAt(540, 240, t, wt(i, /promised/) - .1, nextStart(i), '✨ THE PROMISE', '#232838', '#fff', 56);
    h += pillAt(540, 480, t, wt(i, /gourmet/) - .05, nextStart(i), '🍽 GOURMET MEALS', '#35a862', '#fff', 54);
    return h },
  sfx: i => [{ k: 'shimmer', t: wt(i, /promised/) }, { k: 'swish', t: wt(i, /gourmet/) - .1, d: .4 }, { k: 'ding', t: wt(i, /gourmet/) }, { k: 'pop', t: wt(i, /villas/) }] };
SHOT.price = { set: S, light: 'sunny',
  cam: i => ({ a: { pos: [-4, 3, 40], at: [-4, 12, -10], fov: 52 }, b: { pos: [-3, 2.6, 36], at: [-2, 10, -10], fov: 50 } }),
  upd: (t, i) => planeAt(t - Lt(i).start, -52, 22, -20, 15, -.06, 0),
  ui: (t, i) => { const t0 = Lt(i).start, a = wt(i, /twelve/) - .3; let h = '';
    const k = pop(t, t0 + .1, .4);
    h += `<div style="position:absolute;left:130px;right:130px;top:250px;transform:scale(${k}) rotate(-3deg);background:#fff6e6;border:9px solid ${OL};border-radius:30px;box-shadow:0 14px 0 #2328384d;padding:26px 30px;text-align:center;z-index:2200">
      <div style="font:900 46px IB,Arial;color:#ff6a1a">🎟 VIP PACKAGE</div><div style="font:700 36px P,Arial;color:${OL};margin-top:6px">✈ FLIGHTS · 🏝 STAY · 🎵 MUSIC</div>
      <div style="border-top:5px dashed ${OL};margin:18px 0 10px"></div>
      <div style="font:900 120px/1 IB,Arial;color:#35a862;text-shadow:${shadowTxt(OL, 5)}">${MG.fmt(Math.round(lerp(0, 12000, ez(cl(t, a, a + .9)))), 0, '$')}</div></div>`;
    return h },
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .1, d: 1.4 }, { k: 'pop', t: Lt(i).start + .1 }, { k: 'cash', t: wt(i, /twelve/) + .6 }] };
SHOT.tents = { set: S, light: 'grey',
  cam: i => { const c = wt(i, /mattress/) - .2; return [
    { t0: Lt(i).start, a: { pos: [0, 7, 16], at: [0, 1.0, -6], fov: 52 }, b: { pos: [0, 4.2, 11], at: [0, 1.2, -5], fov: 50 } },
    { t0: c, a: { pos: [-1.0, 2.8, 6.8], at: [-2.6, .6, .4], fov: 46 }, b: { pos: [-1.2, 2.5, 5.9], at: [-2.6, .6, .4], fov: 44 } }] },
  figs: (t, i) => { const c = wt(i, /mattress/) - .2, t0 = Lt(i).start, f = wt(i, /found/) - .1; let h = '';
    if (t < c) { for (let k = 0; k < 5; k++) { const u = ez(cl((t - t0 - k * .1) / 1.6, 0, 1)), x = -4 + k * 2;
        h += figk([x, 0, lerp(9, 3.2 + (k % 2), u)], 'guest', k, Object.assign({ mouth: t > f ? 'o' : 'grin', blink: bl(t, k), look: [0, -2], prop: P_CASE(['#e0303a', '#3f7fb5', '#ffd166', '#35a862', '#d35fa0'][k]), hR: [170, 160], sweat: t > f }, u < 1 ? walk(t + k * .3, 8) : {})) } return h }
    return figk([-1.6, 0, 1.6], 'guest', 2, { mouth: 'o', blink: bl(t, 3), look: [-6, 4], sweat: true, hR: [190, 70 + 8 * Math.sin(t * 8)] }) },
  ui: (t, i) => { const c = wt(i, /mattress/) - .2; let h = '';
    h += pillAt(540, 240, t, wt(i, /found/) - .05, c, '⛺ DISASTER-RELIEF TENTS', '#e0303a', '#fff', 52);
    h += pillAt(540, 240, t, c, nextStart(i), '💧 SOAKING-WET MATTRESSES', '#3f7fb5', '#fff', 50);
    return h },
  sfx: i => [{ k: 'error', t: wt(i, /found/) }, { k: 'pop', t: wt(i, /found/) + .1 }, { k: 'thud', t: wt(i, /mattress/), g: .5 }] };
SHOT.sandwich = { set: S, light: 'grey',
  cam: i => ({ a: { pos: [BOXP[0] + .1, 2.9, BOXP[2] + 2.9], at: [BOXP[0], 1.05, BOXP[2] - .1], fov: 40 }, b: { pos: [BOXP[0] + .1, 2.5, BOXP[2] + 2.2], at: [BOXP[0], 1.08, BOXP[2] - .1], fov: 38 } }),
  upd: (t, i) => { lidOpen(1.95 * bo(cl(t, wt(i, /cheese/) - .45, wt(i, /cheese/) + .05))) },
  ui: (t, i) => { const a = wt(i, /cheese/) - .1; let h = '';
    h += pillAt(540, 240, t, Lt(i).start + .05, nextStart(i), '🍽 DINNER', '#232838', '#fff', 60);
    if (t > a) h += bigText(540, 420, t, a, nextStart(i), '$12,000 → 🥪', 112, '#ffd166', -4);
    h += stampAt(540, 1180, t, wt(i, /foam/) - .05, 'FOAM BOX', '#e0303a', 80, 6);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, { k: 'click', t: wt(i, /cheese/) - .45 }, { k: 'impact', t: wt(i, /cheese/), g: .6 }, { k: 'pop', t: wt(i, /foam/) }] };
SHOT.airport = { set: S, light: 'sunny',
  cam: i => ({ a: { pos: [AP[0] - 1, 2.6, AP[2] + 13], at: [AP[0], 2.2, AP[2] - 3], fov: 50 }, b: { pos: [AP[0] + 1, 2.2, AP[2] + 10.5], at: [AP[0], 2.0, AP[2] - 3], fov: 48 } }),
  figs: (t, i) => { let h = ''; for (let k = 0; k < 7; k++) { const x = AP[0] - 5 + k * 1.6 + (k % 2) * .3, z = AP[2] + .6 + (k % 3) * 1.1;
      h += figk([x, 0, z], 'guest', k, { mouth: k % 2 ? 'sad' : 'hmm', blink: bl(t, k), look: [0, -1], sweat: k % 3 == 0, prop: P_CASE(['#e0303a', '#3f7fb5', '#ffd166', '#35a862', '#d35fa0', '#ff8a3d', '#8a6a4a'][k]), hR: [176, 170] }) } return h },
  ui: (t, i) => { let h = '';
    h += stampAt(540, 280, t, wt(i, /called/) - .05, 'CANCELLED', '#e0303a', 120, -6);
    h += pillAt(540, 470, t, wt(i, /miami/i) - .2, nextStart(i), '✈ BACK TO MIAMI', '#232838', '#fff', 60);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, { k: 'impact', t: wt(i, /called/), g: .6 }, { k: 'ding', t: wt(i, /miami/i) }] };
SHOT.prison = { set: S, light: 'cell',
  cam: i => ({ a: { pos: [PR[0], 1.8, PR[2] + 6.0], at: [PR[0], 1.2, PR[2] - 1], fov: 44 }, b: { pos: [PR[0], 1.6, PR[2] + 5.0], at: [PR[0], 1.1, PR[2] - 1], fov: 42 } }),
  figs: (t, i) => fig([PR[0], 0, PR[2] - .9], 'convict', { mouth: 'sad', blink: bl(t, 2), look: [0, 3] }, 1.7),
  ui: (t, i) => { let h = '';
    for (let k = 0; k < 7; k++) h += `<div style="position:absolute;left:${110 + k * 140}px;top:0;width:28px;height:1290px;background:linear-gradient(90deg,#2a2a33,#6a6a76 45%,#2a2a33);border:4px solid ${OL};border-top:0;border-radius:0 0 14px 14px;z-index:1500"></div>`;
    h += pillAt(540, 250, t, wt(i, /founder/) - .1, nextStart(i), '👔 THE FOUNDER', '#232838', '#fff', 56);
    h += stampAt(540, 400, t, wt(i, /fraud/) - .1, 'GUILTY: FRAUD', '#e0303a', 90, -5);
    h += stampAt(540, 580, t, wt(i, /six/) - .1, '6 YEARS', '#e0303a', 120, 4);
    return h },
  sfx: i => [{ k: 'thud', t: Lt(i).start + .05, g: .6 }, { k: 'impact', t: wt(i, /fraud/), g: .6 }, { k: 'impact', t: wt(i, /six/), g: .6 }] };
SHOT.end = { set: S, light: 'grey', cam: i => ({ a: HERO_B, b: HERO_A }), figs: (t, i) => heroFigs(t),
  ui: (t, i) => { const t0 = Lt(i).start, k = pop(t, t0 + .1, .4);
    const btn = (txt, bg, d) => `<div style="flex:1;text-align:center;font:900 64px/1 IB,Arial;color:#fff;background:${bg};border:7px solid ${OL};border-radius:26px;padding:22px 0;text-shadow:${shadowTxt(OL, 3)};transform:scale(${pop(t, t0 + d, .3)})">${txt}</div>`;
    const o = fade(t, MG.TL.dur - .35, MG.TL.dur - .05);
    return `<div style="position:absolute;left:90px;right:90px;top:250px;opacity:${o};transform:scale(${k});background:#fff;border:8px solid ${OL};border-radius:34px;box-shadow:0 14px 0 #2328384d;padding:30px 34px;text-align:center;z-index:2200">
    <div style="font:900 60px/1.1 IB,Arial;color:${OL}">Would you have bought a ticket? 🎟</div>
    <div style="display:flex;gap:30px;margin-top:26px">${btn('YES', '#35a862', .35)}${btn('NO', '#e0303a', .5)}</div></div>` },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'pop', t: Lt(i).start + .45 }, { k: 'pop', t: Lt(i).start + .6 }] };
