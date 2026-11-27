// ===================== #1 Set KIT: Haus bei Compiegne / Kueche mit Kochplatte / Louvre =====================
const KX = 3600, KK = [KX, 0, 0], KH = [KX, 0, 90], KL = [KX, 0, -90];
LOOK.granny = { sw: '#8a7ab0', swd: '#7a6aa0', pa: '#5a4a6a', hat: `<path d="M40,64 Q30,4 100,2 Q170,4 160,64 Q150,26 100,24 Q50,26 40,64Z" fill="#e8e8ee" stroke="${OL}" stroke-width="5"/><circle cx="100" cy="8" r="20" fill="#e8e8ee" stroke="${OL}" stroke-width="5"/>`, mid: `<path d="M70,160 Q100,190 130,160 L134,240 L66,240Z" fill="#f2d0e0" stroke="${OL}" stroke-width="3"/>` };
LOOK.wolf = { sw: '#2a6a6a', swd: '#205a5a', pa: '#2c3044', hat: `<path d="M44,70 Q26,0 100,-4 Q174,0 156,70 Q150,26 100,22 Q50,26 44,70Z" fill="#3a2a22" stroke="${OL}" stroke-width="5"/>` };
LOOK.visitor = { sw: '#e07a5a', swd: '#c8644a', pa: '#3a3f55', hat: HAT.cap };
(function kit() {
  const S = 'KIT';
  // Kueche (offen): Fliesenboden, Wand, Arbeitsplatte mit Kochplatte, Fenster, Tisch
  mk(S, merge([at(G.box(14, .3, 10, '#c9b8a0', { base: true, top: '#d8c8b0' }), [KX, -.3, 0]), at(G.box(14, 5, .3, '#f0e2c4', { base: true }), [KX, 0, -4]), at(G.box(.3, 5, 10, '#e8d8b8', { base: true }), [KX - 7, 0, 0]),
    at(G.box(5, .95, 1.1, '#8a6a46', { base: true }), [KX, 0, -3.3]), at(G.box(5.1, .1, 1.2, '#e8e0d0', { base: true }), [KX, .95, -3.3]),
    at(G.box(.9, .04, .6, '#2a2a33', { base: true }), [KX, 1.05, -3.3]), ...[-.22, .22].map(x => at(G.cyl(.16, .16, .015, 16, '#c0303a'), [KX + x, 1.09, -3.3])),
    at(G.box(1.6, 1.4, .1, '#bfe0f6', { base: true }), [KX - 3.4, 1.6, -3.84]), at(G.box(1.7, .1, .14, '#f4efe2', { base: true }), [KX - 3.4, 1.55, -3.8]),
    at(G.box(1.6, .5, .5, '#a07a4a', { base: true }), [KX + 3.2, 2.6, -3.6]), ...[...Array(6)].map((_, k) => at(G.box(.18, .26, .18, ['#e07a5a', '#60a5fa', '#f2b21c'][k % 3], { base: true }), [KX + 2.6 + k * .24, 1.05, -3.4])),
    at(G.box(2, .08, 1.2, '#a8784a', { base: true }), [KX + .4, .85, -.4]), ...[[-.9, -.5], [.9, -.5], [-.9, .5], [.9, .5]].map(([a, b]) => at(G.box(.08, .85, .08, '#7a5226', { base: true }), [KX + .4 + a, 0, -.4 + b]))]), { outline: false });
  mk(S, G.cyl(.15, .15, .2, 14, '#9aa0ac'), { pos: [KX + .22, 1.1, -3.3] });
  // Haus von aussen (1960er, Garten, Zaun, Verkaufsschild)
  mk(S, G.box(160, .4, 80, '#7aa05a', { base: true }), { pos: [KX, -.4, KH[2]], outline: false, cast: false });
  mk(S, merge([at(G.box(9, 4.2, 7, '#f0e8d8', { base: true }), [KX, 0, KH[2] - 6]), at(G.cyl(6.6, 0, 2.6, 4, '#7a4a3a', { rot: .785 }), [KX, 4.2, KH[2] - 6]),
    at(G.box(1.2, 2.2, .1, '#5a7a9a', { base: true }), [KX, 0, KH[2] - 2.45]), ...[-2.8, 2.8].map(x => at(G.box(1.4, 1.2, .1, '#3a5a7a', { base: true }), [KX + x, 1.4, KH[2] - 2.45])),
    ...[...Array(14)].map((_, k) => at(G.box(.1, .9, .1, '#f4efe2', { base: true }), [KX - 7 + k * 1.08, 0, KH[2] + 2])), at(G.box(14, .08, .06, '#f4efe2', { base: true }), [KX, .7, KH[2] + 2]),
    at(G.box(.1, 1.6, .1, '#8a5a32', { base: true }), [KX + 4, 0, KH[2] + 1.4]), at(G.box(1.4, .8, .06, '#e0303a', { base: true }), [KX + 4, 1.3, KH[2] + 1.44]),
    ...leafy(KX - 9, KH[2] - 4, 1.1), ...leafy(KX + 9, KH[2] - 3, 1)]).vary(.02, 6));
  // Louvre-Saal
  mk(S, merge([at(G.box(16, .3, 12, '#a87a4a', { base: true, top: '#b88a5a' }), [KL[0], -.3, KL[2]]), at(G.box(16, 7, .3, '#8a3a3a', { base: true }), [KL[0], 0, KL[2] - 5]), at(G.box(.3, 7, 12, '#7a3434', { base: true }), [KL[0] - 8, 0, KL[2]]),
    at(G.box(16, .4, .4, '#e8c060', { base: true }), [KL[0], 6.4, KL[2] - 4.8]), at(G.box(3, .45, .9, '#5a3a2a', { base: true }), [KL[0], 0, KL[2] + 1]),
    ...[-5.4, 5.4].map(x => at(G.box(2.4, 1.8, .1, ['#3a5a3a', '#5a4a2a'][x > 0 ? 1 : 0], { base: true }), [KL[0] + x, 1.6, KL[2] - 4.8]))]), { outline: false });
})();
const KPIC = texPlane('KIT', .26, .34, paintIcon, { pos: [KX, 1.7, -3.82] });
const KFRAME = mk('KIT', G.box(.32, .4, .03, '#c9a23c', { base: false }), { pos: [KX, 1.7, -3.84] });
const KSTEAM = [0, 1, 2, 3].map(k => mk('KIT', G.ico(.06, 1, '#ffffff'), { pos: [KX + .22, 1.3, -3.3], alpha: .3, emis: .7, outline: false, cast: false, recv: false }));
const KLOUV = texPlane('KIT', .52, .68, paintIcon, { pos: [KL[0], 1.9, KL[2] - 4.82] });
const KLFR = mk('KIT', G.box(.66, .82, .05, '#c9a23c', { base: false }), { pos: [KL[0], 1.9, KL[2] - 4.86] });
CHAP.push({ line: 'n1', n: 1, title: 'THE KITCHEN PAINTING', year: '2019', place: '🇫🇷 Near Paris' });
function kUpd(t, i) { KSTEAM.forEach((m, k) => { const u = (t * .4 + k / 4) % 1; m.pos = [KX + .22 + Math.sin(t + k) * .04, 1.24 + u * .22, -3.3]; m.alpha = .3 * (1 - u); const s = .35 + u * .4; m.scl = [s, s, s] }) }
const granny = (t, o = {}) => fig([KX - .8, 0, -2.4], 'granny', Object.assign({ mouth: 'smile', blink: bl(t, 0), look: [3, 1] }, o));
// Hook: Kamera beginnt nah am kleinen Bild ueber der Kochplatte und faehrt zurueck
SHOT.h_kitchen = { set: 'KIT', light: 'indoorWarm',
  cam: i => [{ t0: 0, a: cm([KX + .3, 1.72, -2.5], [KX, 1.62, -3.82], 40), b: cm([KX + 1.6, 2.1, .2], [KX - .2, 1.4, -3.4], 46) }],
  upd: kUpd,
  figs: (t, i) => granny(t, { hR: [175, 190] }),
  ui: (t, i) => labelAt([KX, 2.0, -3.8], PILL('🖼️ TINY PAINTING', '#ffd166', OL, 40), t, wt(i, /tiny/) - .1, wt(i, /worthless/) - .2) + stampAt(1460, 560, t, wt(i, /worthless/) - .05, '"WORTHLESS"', '#e0303a', 80, -6),
  sfx: i => [{ k: 'pop', t: wt(i, /tiny/) }, { k: 'impact', t: wt(i, /worthless/), g: .4 }] };
SHOT.h_sold = { set: 'AUC', light: 'indoorWarm',
  cam: i => cut2(i, /months/, ...CAM_POD, ...CAM_AUD),
  upd: (t, i) => aucUpd(t, i, 2),
  figs: (t, i) => t < wt(i, /months/) - .15 ? fig([AX - .9, 0, -4.2], 'expert', { mouth: 'o', blink: bl(t, 0), look: [3, 0], prop: PROP.magnifier, hR: [200, 110] }) : audience(t, i, 1),
  ui: (t, i) => counter(960, 600, t, wt(i, /sold/) - .1, nextStart(i), wt(i, /sold/), wt(i, /euros/), 0, 24e6, v => '€' + Math.round(v).toLocaleString('en-US'), '#35a862', '#fff', 92) + stampAt(1460, 780, t, wt(i, /euros/) + .1, 'SOLD!', '#e0303a', 110, -8),
  sfx: i => [{ k: 'ding', t: wt(i, /closer/) }, { k: 'tick', t: wt(i, /sold/) }, { k: 'impact', t: wt(i, /euros/) }, { k: 'cash', t: wt(i, /euros/) + .2 }] };
SHOT.k_house = { set: 'KIT', light: 'day',
  cam: i => mv(cm([KX + 9, 4, KH[2] + 12], [KX, 2.2, KH[2] - 4], 50), cm([KX + 5, 3, KH[2] + 8], [KX, 2, KH[2] - 4], 48)),
  upd: kUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🏠 NEAR COMPIÈGNE, NORTH OF PARIS', '#232838', '#fff', 44) + labelAt([KX + 4, 1.8, KH[2] + 1.5], PILL('FOR SALE', '#e0303a', '#fff', 34), t, Lt(i).start + 1, nextStart(i)),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.k_value = { set: 'KIT', light: 'indoorWarm',
  cam: i => mv(cm([KX + 3.6, 2.6, 4], [KX, 1.3, -1.8], 48), cm([KX + 2.6, 2.3, 3], [KX, 1.3, -1.8], 46)),
  upd: kUpd,
  figs: (t, i) => granny(t, { talk: 0 }) + fig([KX + 2.2, 0, -1], 'wolf', { mouth: 'smile', blink: bl(t, 2), look: [-3, 1], hR: [180, 140] }),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /nineties/) - .1, nextStart(i), '👵 IN HER NINETIES', '#232838', '#fff', 52) + pillAt(960, 280, t, wt(i, /auctioneer/) - .1, nextStart(i), '🔨 AN AUCTIONEER VALUES EVERYTHING', '#2a8fd6', '#fff', 46),
  sfx: i => [{ k: 'pop', t: wt(i, /nineties/) }, { k: 'pop', t: wt(i, /auctioneer/) }] };
SHOT.k_tiny = { set: 'KIT', light: 'indoorWarm',
  cam: i => mv(cm([KX + .6, 1.7, -2.2], [KX, 1.45, -3.6], 40), cm([KX + .25, 1.68, -2.8], [KX, 1.6, -3.8], 36)),
  upd: kUpd,
  ui: (t, i) => labelAt([KX, 1.92, -3.8], PILL('26 × 20 CM', '#ffd166', OL, 40), t, wt(i, /tiny/) - .1, nextStart(i)) + pillAt(960, 160, t, wt(i, /hot/) - .1, nextStart(i), '🍳 ABOVE THE HOT PLATE', '#e0303a', '#fff', 52) +
    pillAt(960, 860, t, wt(i, /smaller/i) - .1, nextStart(i), '📄 SMALLER THAN A SHEET OF PAPER', '#232838', '#fff', 46),
  sfx: i => [{ k: 'pop', t: wt(i, /tiny/) }, { k: 'swish', t: wt(i, /smaller/i) }] };
SHOT.k_icon = { set: 'KIT', light: 'indoorWarm',
  cam: i => mv(cm([KX + 1.4, 2, -.4], [KX - .4, 1.4, -3.2], 44), cm([KX + 1.1, 1.9, -.9], [KX - .4, 1.45, -3.2], 42)),
  upd: kUpd,
  figs: (t, i) => granny(t, { mouth: 'smile', look: [4, 0], hR: [170, 60], hL: [30, 60] }),
  ui: (t, i) => pillAt(1300, 300, t, wt(i, /icon/) - .1, nextStart(i), '"JUST AN OLD ICON"', '#232838', '#fff', 50) + pillAt(1300, 420, t, wt(i, /nothing/i) - .1, nextStart(i), '🤷 NOTHING SPECIAL', '#9aa0ac', '#fff', 46),
  sfx: i => [{ k: 'pop', t: wt(i, /icon/) }, { k: 'pop', t: wt(i, /nothing/i) }] };
SHOT.k_spot = { set: 'KIT', light: 'indoorWarm',
  cam: i => cut2(i, /italian/i, cm([KX + 2.6, 2.2, .2], [KX + .3, 1.4, -3.2], 46), cm([KX + 2.3, 2.1, -.3], [KX + .3, 1.45, -3.2], 44), cm([KX + .3, 1.75, -2.6], [KX, 1.68, -3.8], 36), cm([KX + .2, 1.72, -3], [KX, 1.7, -3.8], 32)),
  upd: kUpd,
  figs: (t, i) => t > wt(i, /italian/i) - .15 ? '' : fig([KX + .9, 0, -2.6], 'wolf', { mouth: 'o', blink: bl(t, 2), look: [-4, -1], prop: PROP.magnifier, hR: [170, 70] }),
  ui: (t, i) => stampAt(1450, 300, t, wt(i, /italian/i) - .05, '🇮🇹 EARLY ITALIAN?', '#2a5ad6', 70, -6) + pillAt(960, 860, t, wt(i, /three/) - .1, nextStart(i), 'FIRST GUESS: €300,000–400,000', '#35a862', '#fff', 50),
  sfx: i => [{ k: 'ding', t: wt(i, /recognizes/) }, { k: 'impact', t: wt(i, /italian/i), g: .5 }, { k: 'cash', t: wt(i, /three/) }] };
SHOT.k_expert = { set: 'KIT', light: 'indoorWarm',
  cam: i => mv(cm([KX + 3, 2.2, 1.4], [KX + .6, 1.4, -2.6], 46), cm([KX + 2.4, 2, .6], [KX + .6, 1.4, -2.6], 44)),
  upd: kUpd,
  figs: (t, i) => fig([KX + 1.2, 0, -2.2], 'expert', { mouth: 'hmm', blink: bl(t, 0), look: [-4, -1], prop: PROP.magnifier, hR: [180, 80] }) + fig([KX + 2.4, 0, -1.4], 'wolf', { mouth: 'smile', blink: bl(t, 2), look: [-4, 1] }),
  ui: (t, i) => stampAt(1300, 300, t, wt(i, /same/) - .05, 'SAME EXPERT AS #2 👀', '#e0303a', 64, -5),
  sfx: i => [{ k: 'impact', t: wt(i, /same/), g: .5 }] };
SHOT.k_scan = { set: 'KIT', light: 'indoorDark',
  cam: i => mv(cm([KX + .1, 1.72, -3.0], [KX, 1.7, -3.82], 36), cm([KX + .05, 1.71, -3.2], [KX, 1.7, -3.82], 32)),
  upd: kUpd,
  ui: (t, i) => { const a = wt(i, /infrared/) - .2; let h = pillAt(960, 140, t, a, nextStart(i), '🔬 INFRARED SCAN', '#8a3ad6', '#fff', 54);
    if (t > a) { const y = 200 + ((t - a) * 260) % 700; h += `<div style="position:absolute;left:0;right:0;top:0;bottom:0;background:#8a3ad633;z-index:1500"></div><div style="position:absolute;left:0;right:0;top:${y}px;height:10px;background:#d6a0ff;box-shadow:0 0 30px #c080ff;z-index:1600"></div>` }
    return h + pillAt(960, 860, t, wt(i, /compares/) - .1, nextStart(i), '🔍 COMPARED TO OTHER WORKS', '#232838', '#fff', 46) },
  sfx: i => [{ k: 'beep', t: wt(i, /infrared/), f: 900 }, { k: 'swish', t: wt(i, /compares/) }] };
SHOT.k_cimabue = { set: 'KIT', light: 'indoorWarm',
  cam: i => mv(cm([KX + .35, 1.75, -2.6], [KX, 1.68, -3.82], 38), cm([KX + .2, 1.72, -2.9], [KX, 1.7, -3.82], 34)),
  upd: kUpd,
  ui: (t, i) => bigText(960, 200, t, wt(i, /cimabue/i) - .1, nextStart(i), 'CIMABUE', 140, '#ffd166', -3) + stampAt(1500, 470, t, wt(i, /1280/) - .05, '≈ 1280', '#2a5ad6', 100, -6) +
    pillAt(960, 860, t, wt(i, /handful/) - .1, nextStart(i), '✋ ONLY A HANDFUL SURVIVE', '#232838', '#fff', 50),
  sfx: i => [{ k: 'impact', t: wt(i, /cimabue/i) }, { k: 'pop', t: wt(i, /1280/) }, { k: 'ding', t: wt(i, /handful/) }] };
SHOT.k_auction = { set: 'AUC', light: 'indoorWarm',
  cam: i => mv(...CAM_AUD),
  upd: (t, i) => aucUpd(t, i, 2),
  figs: (t, i) => audience(t, i, t > wt(i, /bids/) - .2),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /october/i) - .1, nextStart(i), '📅 OCTOBER 2019 · SENLIS', '#232838', '#fff', 52) + pillAt(960, 280, t, wt(i, /eight/) - .1, nextStart(i), '👥 ~800 PEOPLE', '#2a8fd6', '#fff', 50) +
    counter(960, 830, t, wt(i, /bids/) - .1, nextStart(i), wt(i, /bids/), nextStart(i) + 1, 4e6, 15e6, v => '€' + Math.round(v / 1e5) / 10 + ' MILLION…', '#35a862', '#fff', 64),
  sfx: i => [{ k: 'pop', t: wt(i, /eight/) }, { k: 'tick', t: wt(i, /bids/) }, { k: 'tick', t: wt(i, /bids/) + .4 }, { k: 'tick', t: wt(i, /bids/) + .8 }] };
SHOT.k_sold = { set: 'AUC', light: 'indoorWarm',
  cam: i => cut2(i, /painting/, ...CAM_POD, cm([AX + .3, 1.9, -3.6], [AX, 1.68, -4.86], 40), cm([AX + .2, 1.8, -3.9], [AX, 1.68, -4.86], 36)),
  upd: (t, i) => aucUpd(t, i, 2),
  figs: (t, i) => t < wt(i, /painting/) - .15 ? auctioneer(t, i) : '',
  ui: (t, i) => counter(960, 170, t, Lt(i).start + .05, nextStart(i), Lt(i).start + .1, wt(i, /euros/), 15e6, 24e6, v => '€' + Math.round(v).toLocaleString('en-US'), '#35a862', '#fff', 90) +
    stampAt(1460, 400, t, wt(i, /euros/), 'SOLD!', '#e0303a', 120, -8, wt(i, /painting/) - .15) + pillAt(960, 860, t, wt(i, /stove/) - .1, nextStart(i), '🍳 IT HUNG OVER THE STOVE', '#ffd166', OL, 54),
  sfx: i => [{ k: 'impact', t: wt(i, /euros/) }, { k: 'cash', t: wt(i, /euros/) + .2 }, { k: 'pop', t: wt(i, /stove/) }] };
SHOT.k_louvre = { set: 'KIT', light: 'indoorWarm',
  cam: i => cut2(i, /louvre/i, cm([AX + 0, 0, 0], [AX, 0, -1], 40), cm([AX, 0, 0], [AX, 0, -1], 40), cm([KL[0] + 2.4, 2.2, KL[2] + 2.6], [KL[0], 1.8, KL[2] - 4.6], 44), cm([KL[0] + 1.2, 2, KL[2] + 1.2], [KL[0], 1.85, KL[2] - 4.6], 40)),
  upd: kUpd,
  figs: (t, i) => t < wt(i, /louvre/i) - .15 ? '' : fig([KL[0] - 1.6, 0, KL[2] - 1.4], 'visitor', { mouth: 'o', blink: bl(t, 0), look: [3, -2] }) + fig([KL[0] + 1.8, 0, KL[2] - 1], 'lady', { mouth: 'smile', blink: bl(t, 1), look: [-3, -2] }),
  ui: (t, i) => (t < wt(i, /louvre/i) - .15 ? `<div style="position:absolute;inset:0;background:#2a3044;z-index:1400"></div>` + stampAt(960, 420, t, wt(i, /blocked/) - .05, '🇫🇷 EXPORT BLOCKED', '#2a5ad6', 100, -5) : '') +
    pillAt(960, 160, t, wt(i, /louvre/i) - .1, nextStart(i), '🏛️ THE LOUVRE · 2023', '#232838', '#fff', 56),
  sfx: i => [{ k: 'impact', t: wt(i, /blocked/), g: .5 }, { k: 'ding', t: wt(i, /louvre/i) }] };
SHOT.k_grandma = { set: 'KIT', light: 'indoorWarm',
  cam: i => mv(cm([KX + 2.4, 2.2, .8], [KX + .3, 1.45, -3], 46), cm([KX + 1.8, 2, 0], [KX + .3, 1.5, -3], 44)),
  upd: kUpd,
  figs: (t, i) => fig([KX + 1.4, 0, -2.2], 'sam', { mouth: 'grin', talk: tk(t, i) * .6, blink: bl(t, 0), look: [-4, -2], prop: PROP.magnifier, hR: [170, 70] }),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /grandma/) - .1, nextStart(i), "👵 CHECK GRANDMA'S KITCHEN!", '#ffd166', OL, 54),
  sfx: i => [{ k: 'pop', t: wt(i, /grandma/) }] };
