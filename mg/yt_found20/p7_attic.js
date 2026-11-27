// ===================== #2 Set ATTIC: Toulouse (rosa Backstein) / Dachboden mit Leck =====================
const CX = 3000, CA = [CX, 0, 0], CT = [CX, 0, 90];
LOOK.frauct = { sw: '#5a3a6a', swd: '#4a2e5a', pa: '#2c3044', mid: MID.tie };
LOOK.owner = { sw: '#d8c8a8', swd: '#c0b090', pa: '#4a5a7a', hat: HAT.grey };
PROP.torch = `<g transform="rotate(-70)"><rect x="-6" y="-10" width="12" height="34" rx="4" fill="#2a2a33" stroke="${OL}" stroke-width="3"/><path d="M-9,-10 L9,-10 L40,-110 L-40,-110Z" fill="#fff6c0" opacity=".35"/></g>`;
(function attic() {
  const S = 'ATTIC';
  // Dachboden: Holzboden, schraege Dachflaechen, Balken, Kram
  mk(S, merge([at(G.box(14, .3, 10, '#7a5a3a', { base: true, top: '#8a6a46' }), [CX, -.3, 0]), at(G.box(14, 5, .3, '#b07a5a', { base: true }), [CX, 0, -5]),
    at(G.box(14, .2, 9, '#6a4a32', { base: true }), [CX, 3.7, -.6], [-.25, 0, 0]), at(G.box(.3, 5, 10, '#a06a4a', { base: true }), [CX - 7, 0, 0]),
    ...[-5, -2.5, 0, 2.5, 5].map(x => at(G.box(.25, .25, 9, '#5a3a22', { base: true }), [CX + x, 3.5, -.6], [-.25, 0, 0])), at(G.box(14, .3, .3, '#5a3a22', { base: true }), [CX, 2.5, -4.6])]), { outline: false });
  const J = []; [[-5, -3.6, 1.2, .8], [-3.6, -3.8, .9, 1.2], [-5.2, -2.2, .8, .6], [4.2, -3.6, 1.4, .9], [5.4, -3.4, .8, 1.4], [3.8, -2, .7, .5]].forEach(([x, z, s, h], k) =>
    J.push(at(G.box(s, h, s * .8, ['#a07a4a', '#8a6a4a', '#c9b48a'][k % 3], { base: true }), [CX + x, 0, z], [0, k * .3, 0])));
  J.push(at(G.cyl(.4, .35, .9, 12, '#6a7a8a'), [CX + 2.6, 0, -3.8]), at(G.box(1.2, .9, .6, '#5a3a22', { base: true }), [CX - 2, 0, -4.2]));
  mk(S, merge(J));
  // Eimer unter dem Leck
  mk(S, G.cyl(.25, .2, .4, 12, '#9aa0ac', { open: true }), { pos: [CX + 1.4, 0, -1.2] });
  // Toulouse: Strasse mit rosa Backsteinhaeusern
  mk(S, G.box(160, .4, 80, '#b8a890', { base: true }), { pos: [CX, -.4, CT[2]], outline: false, cast: false });
  const Hh = []; for (let k = 0; k < 9; k++) { const x = CX - 20 + k * 5, hh = 6 + (k % 3) * 1.6;
    Hh.push(at(G.box(4.8, hh, 5, ['#d98a6a', '#e0a07a', '#c97a5a'][k % 3], { base: true }), [x, 0, CT[2] - 6]), at(G.cyl(3.6, 0, 1.8, 4, '#a0503a', { rot: .785 }), [x, hh, CT[2] - 6]));
    for (let r = 0; r < 2; r++) for (let j = 0; j < 2; j++) Hh.push(at(G.box(.9, 1.3, .1, '#3a5a7a', { base: true }), [x - 1.1 + j * 2.2, 1.6 + r * 2.6, CT[2] - 3.46])) }
  Hh.push(at(G.box(1.2, 2.2, .1, '#5a3a22', { base: true }), [CX, 0, CT[2] - 3.45]));
  mk(S, merge(Hh).vary(.03, 5));
})();
const CPIC = texPlane('ATTIC', 2.2, 1.76, paintBaroque, { pos: [CX - .2, 1.15, -3.3], rot: [-.18, 0, 0] });
const CFR = mk('ATTIC', G.box(2.36, 1.9, .06, '#3a2a1e', { base: false }), { pos: [CX - .2, 1.15, -3.34], rot: [-.18, 0, 0] });
const CDROPS = [0, 1, 2].map(k => mk('ATTIC', G.ico(.05, 1, '#8fd3ff'), { pos: [CX + 1.4, 3, -1.2], emis: .4, outline: false, cast: false }));
const CSHEET = mk('ATTIC', G.box(2.5, 2.0, .2, '#e8e4dc', { base: false }), { pos: [CX - .2, 1.15, -3.2], rot: [-.18, 0, 0] });
CHAP.push({ line: 'n2', n: 2, title: 'THE LEAKY ATTIC', year: '2014', place: '🇫🇷 Toulouse' });
function cUpd(t, i, sheet = false) {
  CPIC.vis = !sheet; CFR.vis = true; CSHEET.vis = sheet;
  CDROPS.forEach((m, k) => { const u = ((t * .9 + k / 3) % 1); m.pos = [CX + 1.4, 3 - u * 2.7, -1.2]; m.scl = [1, 1.5, 1] });
}
SHOT.c_house = { set: 'ATTIC', light: 'day',
  cam: i => mv(cm([CX + 8, 5, CT[2] + 12], [CX, 3, CT[2] - 4], 50), cm([CX + 4, 3.4, CT[2] + 7], [CX, 2.4, CT[2] - 4], 48)),
  upd: (t, i) => cUpd(t, i),
  figs: (t, i) => fig([CX + 4 - (t - Lt(i).start) * .9, 0, CT[2] - 1.6], 'frauct', Object.assign(walk(t, 6), { mouth: 'smile', blink: bl(t, 0), look: [-3, 2] })),
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🌸 TOULOUSE · "LA VILLE ROSE"', '#232838', '#fff', 44),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.c_attic = { set: 'ATTIC', light: 'indoorDark',
  cam: i => mv(cm([CX + 4.6, 2.6, 4.4], [CX, 1.4, -2.4], 50), cm([CX + 3.4, 2.4, 3.4], [CX, 1.4, -2.4], 48)),
  upd: (t, i) => cUpd(t, i),
  figs: (t, i) => fig([CX + 2.6, 0, .2], 'frauct', { mouth: 'o', blink: bl(t, 0), look: [-4, 1], prop: PROP.torch, hR: [190, 80] }) + fig([CX + 3.8, 0, 1], 'owner', { mouth: 'smile', talk: tk(t, i) * .4, blink: bl(t, 1), look: [-4, 1] }),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /auctioneer/) - .1, nextStart(i), '🔨 A LOCAL AUCTIONEER', '#232838', '#fff', 52) + pillAt(1420, 300, t, wt(i, /leaking/) - .1, nextStart(i), '💧 LEAKY ROOF', '#2a8fd6', '#fff', 48),
  sfx: i => [{ k: 'thud', t: Lt(i).start + .3 }, { k: 'pop', t: wt(i, /leaking/) }] };
SHOT.c_canvas = { set: 'ATTIC', light: 'indoorWarm',
  cam: i => mv(cm([CX + .4, 1.8, 1.2], [CX - .2, 1.2, -3.3], 46), cm([CX + .2, 1.6, .4], [CX - .2, 1.2, -3.3], 42)),
  upd: (t, i) => cUpd(t, i),
  ui: (t, i) => pillAt(960, 140, t, wt(i, /huge/) - .1, nextStart(i), '🖼️ A HUGE, OLD PAINTING', '#232838', '#fff', 54) + pillAt(960, 800, t, wt(i, /cutting/) - .1, nextStart(i), '⚔️ JUDITH & HOLOFERNES', '#8a1a1a', '#fff', 46),
  sfx: i => [{ k: 'shimmer', t: wt(i, /huge/) }, { k: 'impact', t: wt(i, /head/), g: .4 }] };
SHOT.c_expert = { set: 'ATTIC', light: 'indoorWarm',
  cam: i => cut2(i, /caravaggio/i, cm([CX + 2.6, 2.2, 2.4], [CX - .2, 1.3, -3], 46), cm([CX + 2, 2, 1.8], [CX - .2, 1.3, -3], 44), cm([CX - .2, 1.5, -.6], [CX - .2, 1.2, -3.3], 46), cm([CX - .2, 1.4, -1.2], [CX - .2, 1.2, -3.3], 44)),
  upd: (t, i) => cUpd(t, i),
  figs: (t, i) => t > wt(i, /caravaggio/i) - .15 ? '' : fig([CX + 1.5, 0, -1.6], 'expert', { mouth: 'hmm', blink: bl(t, 0), look: [-5, 1], prop: PROP.magnifier, hR: [200, 110] }),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /paris/i) - .1, wt(i, /caravaggio/i) - .2, '🇫🇷 AN EXPERT FROM PARIS', '#232838', '#fff', 52) + bigText(960, 200, t, wt(i, /caravaggio/i) - .1, nextStart(i), 'CARAVAGGIO?!', 120, '#ffd166', -4) +
    pillAt(960, 340, t, wt(i, /famous/) - .1, nextStart(i), '⭐ ONE OF THE MOST FAMOUS PAINTERS', '#232838', '#fff', 46),
  sfx: i => [{ k: 'ding', t: wt(i, /studies/) }, { k: 'impact', t: wt(i, /caravaggio/i) }] };
SHOT.c_estimate = { set: 'ATTIC', light: 'indoorWarm',
  cam: i => mv(cm([CX + 1.6, 1.6, .8], [CX - .2, 1.2, -3.3], 44), cm([CX + 1.2, 1.5, .2], [CX - .2, 1.2, -3.3], 42)),
  upd: (t, i) => cUpd(t, i),
  ui: (t, i) => stampAt(1450, 250, t, wt(i, /bans/) - .05, '🇫🇷 STAYS IN FRANCE', '#2a5ad6', 64, -6) + pillAt(1450, 400, t, wt(i, /years/) - .1, nextStart(i), '🔬 TESTS FOR 2+ YEARS', '#232838', '#fff', 46) +
    counter(960, 820, t, wt(i, /estimates/i) - .1, nextStart(i), wt(i, /estimates/i), wt(i, /euros/), 0, 150, v => 'UP TO €' + Math.round(v) + ' MILLION', '#35a862', '#fff', 72),
  sfx: i => [{ k: 'impact', t: wt(i, /bans/), g: .5 }, { k: 'tick', t: wt(i, /years/) }, { k: 'cash', t: wt(i, /euros/) }] };
SHOT.c_cancel = { set: 'AUC', light: 'indoorDark',
  cam: i => mv(...CAM_POD),
  upd: (t, i) => aucUpd(t, i, -1),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /june/i) - .1, nextStart(i), '📅 AUCTION: JUNE 2019', '#232838', '#fff', 54) + screenPrice(t, wt(i, /june/i), nextStart(i), '€100–150M?', '#ffd166') +
    stampAt(1000, 520, t, wt(i, /off/) - .05, 'CANCELLED', '#e0303a', 120, -8),
  sfx: i => [{ k: 'tick', t: wt(i, /june/i) }, { k: 'impact', t: wt(i, /off/) }] };
SHOT.c_secret = { set: 'ATTIC', light: 'indoorDark',
  cam: i => mv(cm([CX + 2.4, 2, 2.6], [CX - .2, 1.2, -3.2], 46), cm([CX + 1.8, 1.9, 1.8], [CX - .2, 1.2, -3.2], 44)),
  upd: (t, i) => cUpd(t, i, t > wt(i, /secret/) - .1),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /private/) - .1, nextStart(i), '🕴️ A PRIVATE COLLECTOR', '#232838', '#fff', 52) + stampAt(1450, 340, t, wt(i, /secret/) - .05, 'PRICE: SECRET 🤫', '#e0303a', 72, -6) +
    pillAt(960, 820, t, wt(i, /doubt/) - .1, nextStart(i), '🤔 REAL CARAVAGGIO? SOME DOUBT IT', '#ffd166', OL, 48),
  sfx: i => [{ k: 'cash', t: wt(i, /bought/) }, { k: 'impact', t: wt(i, /secret/), g: .5 }, { k: 'pop', t: wt(i, /doubt/) }] };
