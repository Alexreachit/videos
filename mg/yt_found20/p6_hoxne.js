// ===================== #3 Set FIELD: Acker in Suffolk 1992 / British Museum =====================
const HX = 2400, HF = [HX, 0, 0], HM = [HX, 0, -90];
LOOK.farmer = { sw: '#4a6a3a', swd: '#3a5a2e', pa: '#3a3f55', hat: HAT.cap };
LOOK.eric = { sw: '#b8744a', swd: '#9a5e3a', pa: '#4a4a3a', hat: HAT.grey };
LOOK.arch = { sw: '#f2b21c', swd: '#d49a10', pa: '#4a5a3a', hat: `<path d="M38,50 Q38,8 100,6 Q162,8 162,50 Q100,40 38,50Z" fill="#f4efe2" stroke="${OL}" stroke-width="6"/><path d="M20,50 Q100,36 180,50 Q180,60 100,58 Q20,60 20,50Z" fill="#e8e0c8" stroke="${OL}" stroke-width="5"/>` };
LOOK.ukcop = { sw: '#1b2236', swd: '#141a2a', pa: '#1b2236', hat: `<path d="M50,52 Q46,-20 100,-24 Q154,-20 150,52Z" fill="#1b2236" stroke="${OL}" stroke-width="6"/><circle cx="100" cy="20" r="10" fill="#c9ccd4" stroke="${OL}" stroke-width="3"/>`, mid: `<rect x="56" y="170" width="88" height="22" fill="#e8f060" stroke="${OL}" stroke-width="3"/>` };
LOOK.curator = { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', mid: MID.tie };
PROP.detector = a => `<g transform="rotate(${a})"><rect x="-4" y="-10" width="8" height="110" rx="3" fill="#5a5e6a" stroke="${OL}" stroke-width="3"/><rect x="-12" y="4" width="24" height="16" rx="4" fill="#2a2a33" stroke="${OL}" stroke-width="3"/><ellipse cx="0" cy="104" rx="30" ry="10" fill="#e0303a" stroke="${OL}" stroke-width="4"/></g>`;
PROP.phone = `<g transform="translate(-10,-26)"><rect x="0" y="0" width="22" height="40" rx="5" fill="#2a2a33" stroke="${OL}" stroke-width="4"/><rect x="4" y="5" width="14" height="22" fill="#60a5fa"/></g>`;
PROP.trowel = `<g transform="rotate(30)"><rect x="-4" y="-34" width="8" height="30" rx="3" fill="#8a5a32" stroke="${OL}" stroke-width="3"/><path d="M-12,-4 L12,-4 L0,30Z" fill="#c9ccd4" stroke="${OL}" stroke-width="4"/></g>`;
(function field() {
  const S = 'FIELD';
  mk(S, G.box(200, .4, 140, '#7a8a4a', { base: true }), { pos: [HX, -.4, 0], outline: false, cast: false });
  // gepfluegter Acker: Furchen
  mk(S, merge([...Array(40)].map((_, k) => at(G.box(60, .14, .45, k % 2 ? '#7a5a3a' : '#8a6a46', { base: true }), [HX, 0, -18 + k * .9]))), { outline: false, cast: false });
  // Hecken + Bauernhof
  mk(S, merge([...Array(20)].map((_, k) => at(G.ico(1.4 + G.hash(k) * .6, 2, '#3a6a3a', .1, k), [HX - 30 + k * 3.2, .8, -20]))).smooth(), { cast: false });
  mk(S, merge([at(G.box(7, 3.4, 5, '#e8d8c0', { base: true }), [HX - 14, 0, -26]), at(G.cyl(5, 0, 2.4, 4, '#6a3a2a', { rot: .785 }), [HX - 14, 3.4, -26]), at(G.box(9, 4, 6, '#a03a2a', { base: true }), [HX - 2, 0, -28]), at(G.cyl(.6, .6, 9, 10, '#c9ccd4'), [HX + 4, 0, -26])]));
  // Polizeiauto (UK, Streifen)
  mk(S, merge([at(G.box(3.8, .8, 1.7, '#f4f6fb', { base: true }), [0, .35, 0]), at(G.box(2.2, .7, 1.56, '#f4f6fb', { base: true }), [-.2, 1.15, 0]), at(G.box(2.0, .5, 1.58, '#a8d8f0', { base: true }), [-.2, 1.2, 0]),
    at(G.box(3.82, .22, 1.72, '#2a5ad6', { base: true }), [0, .62, 0]), at(G.box(.5, .16, .3, '#2a8fff', { base: true }), [-.2, 1.85, 0]),
    ...[[-1.2, .86], [1.2, .86], [-1.2, -.86], [1.2, -.86]].map(([a, b]) => at(G.cyl(.34, .34, .24, 14, '#22242c'), [a, .34, b], [PI / 2, 0, 0]))]), { pos: [HX + 7, 0, -5], rot: [0, .5, 0] });
  // British Museum: Saal mit Saeulen + Vitrine
  mk(S, merge([at(G.box(16, .3, 12, '#d8d0c0', { base: true }), [HM[0], -.3, HM[2]]), at(G.box(16, 7, .3, '#e8e0d0', { base: true }), [HM[0], 0, HM[2] - 6]), at(G.box(.3, 7, 12, '#ded6c6', { base: true }), [HM[0] - 8, 0, HM[2]]),
    ...[-6, -2, 2, 6].map(x => at(G.cyl(.4, .4, 7, 14, '#f2ece0'), [HM[0] + x, 0, HM[2] - 5.4])),
    at(G.box(3.2, 1.0, 1.6, '#3a3f55', { base: true }), [HM[0], 0, HM[2] - 1.4]), at(G.box(1.4, 1.0, 1.0, '#3a3f55', { base: true }), [HM[0] + 3.4, 0, HM[2] - 1.4])]), { outline: false });
  mk(S, merge([at(G.box(3.2, 1.2, 1.6, '#d8f0ff'), [HM[0], 1.6, HM[2] - 1.4]), at(G.box(1.4, 1.0, 1.0, '#d8f0ff'), [HM[0] + 3.4, 1.5, HM[2] - 1.4])]), { alpha: .16, spec: 1, outline: false, cast: false, recv: false });
  mk(S, merge([at(coinPile(60, .7, 7, "#e8eaf0"), [0, 0, 0]), ...[...Array(8)].map((_, k) => at(G.box(.06, .02, .4, '#d8dde6', { base: true }), [-1.2 + k * .34, .02, .45], [0, .3, 0]))]), { pos: [HM[0], 1.02, HM[2] - 1.5], spec: 1, emis: .15, outline: false });
  mk(S, coinPile(25, .4, 9), { pos: [HM[0] + .9, 1.02, HM[2] - 1.3], spec: 1, emis: .2, outline: false });
})();
const HHAM = mk('FIELD', hammerGeo(), { pos: [HM[0] + 3.4, 1.06, HM[2] - 1.4], rot: [0, .4, 0], scl: [1.4, 1.4, 1.4] });
const HHOLE = mk('FIELD', G.cyl(.7, .7, .04, 18, '#4a3020'), { pos: [HX + 1, .15, 0], outline: false, cast: false });
const HFIND = mk('FIELD', merge([at(coinPile(40, .5, 11, "#e8eaf0"), [0, 0, 0]), at(coinPile(14, .35, 12), [0, 0, 0]), ...[0, 1, 2].map(k => at(G.box(.06, .02, .4, '#d8dde6', { base: true }), [-.2 + k * .2, .06, .1], [0, .5 * k, 0]))]), { pos: [HX + 1, .17, 0], spec: 1, emis: .2, outline: false });
const HBLOCK = mk('FIELD', merge([at(G.box(1.4, .8, 1.2, '#6a4a2e', { base: true }), [0, 0, 0]), at(G.box(1.5, .06, 1.3, '#c9ccd4', { base: true }), [0, -.06, 0])]), { pos: [HX + 1, 0, 0] });
const HTAPE = mk('FIELD', merge([[-2, -2], [2, -2], [2, 2], [-2, 2]].map(([a, b]) => at(G.cyl(.04, .04, 1, 6, '#e8e8ee'), [a, 0, b]))), { pos: [HX + 1, 0, 0] });
CHAP.push({ line: 'n3', n: 3, title: 'THE LOST HAMMER', year: '1992', place: '🇬🇧 Suffolk, England' });
function hUpd(t, i, mode) {
  HHOLE.vis = false; HFIND.vis = false; HBLOCK.vis = false; HTAPE.vis = false;
  if (mode == 'find') { const a = wt(i, /coins/) - .3; HHOLE.vis = t > a; HFIND.vis = t > a; HFIND.scl = [1, ez(cl((t - a) / .5, 0, 1)) + .01, 1] }
  if (mode == 'found') { HHOLE.vis = true; HFIND.vis = true; HTAPE.vis = true }
  if (mode == 'block') { HTAPE.vis = true; HBLOCK.vis = true; const u = ez(cl((t - wt(i, /whole/) + .3) / 1.2, 0, 1)); HBLOCK.pos = [HX + 1, u * .9, 0] }
}
const detSweep = t => PROP.detector(-20 + 22 * Math.sin(t * 2.4));
SHOT.x_field = { set: 'FIELD', light: 'day',
  cam: i => mv(cm([HX + 14, 7, 14], [HX, 1, -2], 50), cm([HX + 9, 5, 10], [HX, 1, -1.5], 48)),
  upd: (t, i) => hUpd(t, i, ''),
  figs: (t, i) => fig([HX - 1.5 + (t - Lt(i).start) * .4, 0, .4], 'farmer', Object.assign(walk(t, 5), { mouth: 'hmm', blink: bl(t, 0), look: [2, 4] })),
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🌾 A FIELD IN SUFFOLK', '#232838', '#fff', 44),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.x_hammer = { set: 'FIELD', light: 'day',
  cam: i => mv(cm([HX + 1.4, 2.4, 5.6], [HX - .4, 1.2, 0], 46), cm([HX + .9, 2.2, 4.6], [HX - .4, 1.2, 0], 44)),
  upd: (t, i) => hUpd(t, i, ''),
  figs: (t, i) => fig([HX - .8, 0, .4], 'farmer', { mouth: 'sad', blink: bl(t, 0), look: [Math.sin(t * 2) * 5, 4], hR: [170, 40], hL: [30, 40], sweat: true }) +
    (t > wt(i, /friend/) - .1 ? fig([HX + 2.4 - Math.max(0, 1 - (t - wt(i, /friend/)) * .7) * 2, 0, .8], 'eric', Object.assign(walk(t, 6), { mouth: 'smile', blink: bl(t, 2), look: [-4, 2] })) : ''),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /hammer/) - .1, nextStart(i), '🔨 LOST: ONE HAMMER', '#e0303a', '#fff', 58),
  sfx: i => [{ k: 'error', t: wt(i, /hammer/), g: .4 }, { k: 'pop', t: wt(i, /friend/) }] };
SHOT.x_detector = { set: 'FIELD', light: 'day',
  cam: i => mv(cm([HX + 3, 2, 4.2], [HX + 1.6, 1.2, .4], 44), cm([HX + 2.6, 1.9, 3.4], [HX + 1.6, 1.2, .4], 40)),
  upd: (t, i) => hUpd(t, i, ''),
  figs: (t, i) => fig([HX + 1.8, 0, .6], 'eric', { mouth: 'grin', talk: 0, blink: bl(t, 2), look: [2, 2], prop: detSweep(t), hR: [170, 140] }) + fig([HX - .4, 0, .2], 'farmer', { mouth: 'smile', blink: bl(t, 0), look: [4, 2] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /detector/) - .1, nextStart(i), '📡 A METAL DETECTOR', '#232838', '#fff', 56) + pillAt(960, 290, t, wt(i, /retirement/) - .1, nextStart(i), '🎁 A RETIREMENT PRESENT', '#35a862', '#fff', 50),
  sfx: i => [{ k: 'pop', t: wt(i, /detector/) }, { k: 'ding', t: wt(i, /retirement/) }] };
SHOT.x_beep = { set: 'FIELD', light: 'day',
  cam: i => cut2(i, /coins/, cm([HX + 3.6, 2, 3.6], [HX + 1.2, .7, 0], 44), cm([HX + 3.2, 1.8, 3], [HX + 1.2, .7, 0], 42), cm([HX + 1.9, 1.3, 1.3], [HX + 1, .15, 0], 38), cm([HX + 1.7, 1.1, 1], [HX + 1, .15, 0], 34)),
  upd: (t, i) => hUpd(t, i, 'find'),
  figs: (t, i) => t > wt(i, /coins/) - .15 ? '' : fig([HX + 1.6, 0, .9], 'eric', { mouth: 'o', blink: bl(t, 2), look: [-2, 4], prop: PROP.detector(-30), hR: [160, 150] }),
  ui: (t, i) => { const P4 = [[/silver/i, '🪙 SILVER', '#9aa0ac'], [/gold/i, '🪙 GOLD', '#e8a800'], [/spoons/i, '🥄 SPOONS', '#2a8fd6'], [/jewelry/i, '💍 JEWELRY', '#c0508a']];
    return P4.map(([re, tx, bg], k) => pillAt(330 + k * 420, 170, t, wt(i, re) - .1, nextStart(i), tx, bg, '#fff', 52)).join('') + stampAt(1450, 420, t, wt(i, /beeps/) - .05, 'BEEP!', '#e0303a', 100, -8, wt(i, /coins/) - .2) },
  sfx: i => [{ k: 'beep', t: wt(i, /beeps/), f: 1200 }, { k: 'beep', t: wt(i, /beeps/) + .18, f: 1200 }, { k: 'shimmer', t: wt(i, /coins/) }, ...[/silver/i, /gold/i, /spoons/i, /jewelry/i].map(r => ({ k: 'pop', t: wt(i, r) }))] };
SHOT.x_stop = { set: 'FIELD', light: 'day',
  cam: i => cut2(i, /calls/, cm([HX + 4.2, 2.4, 5], [HX + 1.4, 1, 0], 46), cm([HX + 3.8, 2.3, 4.4], [HX + 1.4, 1, 0], 44), cm([HX + 4, 3, 7], [HX + 4.4, 1, -3], 48), cm([HX + 3.4, 2.8, 6], [HX + 4.4, 1, -3], 46)),
  upd: (t, i) => hUpd(t, i, 'found'),
  figs: (t, i) => t < wt(i, /calls/) - .15 ? fig([HX + 2.1, 0, .7], 'eric', { mouth: 'hmm', blink: bl(t, 2), look: [-3, 3], hR: [190, 60], hL: [10, 60] }) :
    fig([HX + 2.1, 0, .9], 'eric', { mouth: 'smile', talk: .4 * Math.abs(Math.sin(t * 9)), blink: bl(t, 2), look: [2, 1], prop: PROP.phone, hR: [150, 70] }) + fig([HX + 5.8, 0, -3.2], 'ukcop', { mouth: 'o', blink: bl(t, 4), look: [-4, 2] }),
  ui: (t, i) => stampAt(1400, 300, t, wt(i, /stops/) - .05, '✋ STOP DIGGING', '#e0303a', 90, -6, wt(i, /calls/) - .15) + pillAt(960, 170, t, wt(i, /police/) - .1, nextStart(i), '🚓 CALLS THE POLICE', '#2a5ad6', '#fff', 56),
  sfx: i => [{ k: 'impact', t: wt(i, /stops/), g: .5 }, { k: 'ding', t: wt(i, /police/) }] };
SHOT.x_dig = { set: 'FIELD', light: 'day',
  cam: i => mv(cm([HX + 4.4, 3, 5.6], [HX + 1, .8, 0], 46), cm([HX + 3.6, 2.6, 4.4], [HX + 1, .9, 0], 44)),
  upd: (t, i) => hUpd(t, i, 'block'),
  figs: (t, i) => [[-.9, .2, 0], [2.4, .1, 1], [-1.8, 1.4, 2]].map(([dx, dz, k]) => fig([HX + 1 + dx, 0, dz], 'arch', { mouth: 'smile', blink: bl(t, k), look: [dx < 0 ? 4 : -4, 3], prop: k == 1 ? PROP.trowel : null, hR: [170, 120] })).join(''),
  ui: (t, i) => pillAt(960, 170, t, Lt(i).start + .1, nextStart(i), '📅 THE NEXT DAY: ARCHAEOLOGISTS', '#232838', '#fff', 54),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: .8 }, { k: 'thud', t: wt(i, /whole/) }] };
SHOT.x_count = { set: 'FIELD', light: 'day',
  cam: i => mv(cm([HX + 1.9, 1.2, 1.4], [HX + 1, .3, 0], 38), cm([HX + 1.6, 1.0, 1], [HX + 1, .25, 0], 34)),
  upd: (t, i) => hUpd(t, i, 'found'),
  ui: (t, i) => counter(960, 160, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, wt(i, /coins/), 0, 14865, v => Math.round(v).toLocaleString('en-US') + ' ROMAN COINS', '#e8a800', OL, 72) +
    pillAt(960, 290, t, wt(i, /objects/) - .1, nextStart(i), '+ ~200 SILVER & GOLD OBJECTS', '#232838', '#fff', 52) + stampAt(1500, 760, t, wt(i, /sixteen/) - .05, '≈ 1,600 YEARS OLD', '#2a5ad6', 64, -6),
  sfx: i => [{ k: 'cash', t: wt(i, /coins/) }, { k: 'pop', t: wt(i, /objects/) }, { k: 'impact', t: wt(i, /sixteen/), g: .5 }] };
SHOT.x_reward = { set: 'FIELD', light: 'vault',
  cam: i => mv(cm([HM[0] + 3, 3, HM[2] + 5.4], [HM[0] + .6, 1.4, HM[2] - 2], 48), cm([HM[0] + 2, 2.6, HM[2] + 4], [HM[0] + .4, 1.4, HM[2] - 2], 46)),
  upd: (t, i) => hUpd(t, i, ''),
  figs: (t, i) => fig([HM[0] - 2.4, 0, HM[2] - .6], 'curator', { mouth: 'smile', blink: bl(t, 0), look: [4, 1] }),
  ui: (t, i) => pillAt(960, 150, t, wt(i, /british/i) - .1, nextStart(i), '🏛️ BRITISH MUSEUM', '#232838', '#fff', 56) +
    counter(960, 280, t, wt(i, /reward/) - .1, nextStart(i), wt(i, /reward/), wt(i, /pounds/), 0, 1.75, v => '💷 £' + v.toFixed(2) + ' MILLION', '#35a862', '#fff', 76) + pillAt(960, 420, t, wt(i, /shared/) - .1, nextStart(i), '🤝 SHARED WITH THE FARMER', '#ffd166', OL, 50),
  sfx: i => [{ k: 'ding', t: wt(i, /british/i) }, { k: 'cash', t: wt(i, /pounds/) }, { k: 'pop', t: wt(i, /shared/) }] };
SHOT.x_hammer2 = { set: 'FIELD', light: 'vault',
  cam: i => mv(cm([HM[0] + 4.4, 2, HM[2] + 1.4], [HM[0] + 3.4, 1.2, HM[2] - 1.4], 40), cm([HM[0] + 4, 1.9, HM[2] + .8], [HM[0] + 3.4, 1.2, HM[2] - 1.4], 36)),
  upd: (t, i) => { hUpd(t, i, ''); HHAM.rot = [0, .4 + Math.sin(t) * .2, 0] },
  ui: (t, i) => stampAt(960, 230, t, wt(i, /too/) - .05, '🔨 FOUND IT!', '#35a862', 110, -6) + pillAt(960, 800, t, wt(i, /museum/i) - .1, nextStart(i), 'ON DISPLAY TOO 😄', '#ffd166', OL, 54),
  sfx: i => [{ k: 'ding', t: wt(i, /too/) }, { k: 'pop', t: wt(i, /museum/i) }] };
