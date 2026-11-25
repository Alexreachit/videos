// ===================== Set EGG: Zarenpalast 1887 / Antikmarkt im Mittleren Westen / Schrottwerkstatt / Juwelier London =====================
const EX = 1500, EP = [EX, 0, 0], EM = [EX, 0, 90], EW = [EX, 0, 170], EL = [EX, 0, -90];
const CROWN = `<path d="M50,44 L56,4 L78,26 L100,0 L122,26 L144,4 L150,44Z" fill="#ffd166" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/><circle cx="100" cy="30" r="7" fill="#e0303a" stroke="${OL}" stroke-width="3"/>`;
LOOK.tsar = { sw: '#2a4a8a', swd: '#203a70', pa: '#1b2236', hat: CROWN, mid: MID.buttons };
LOOK.empress = { sw: '#e8e0f0', swd: '#d0c6e0', pa: '#c8b8e0', hat: `<path d="M64,40 L70,14 L86,30 L100,8 L114,30 L130,14 L136,40Z" fill="#f2f2f8" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/><circle cx="100" cy="26" r="6" fill="#60a5fa" stroke="${OL}" stroke-width="3"/>` };
LOOK.scrap = { sw: '#5a6a8a', swd: '#4a5a78', pa: '#3a3f55', hat: HAT.cap };
LOOK.jeweler = { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', mid: MID.tie };
LOOK.redguard = { sw: '#5a6048', swd: '#484d3a', pa: '#3a3e30', hat: `<path d="M36,50 Q36,6 100,4 Q164,6 164,50Z" fill="#6a6e5a" stroke="${OL}" stroke-width="6"/><circle cx="100" cy="28" r="9" fill="#e0303a" stroke="${OL}" stroke-width="3"/>` };
(function egg() {
  const S = 'EGG';
  // Palast-Saal
  mk(S, merge([at(G.box(22, .3, 14, '#a8743a', { base: true, top: '#c08a4a' }), [EP[0], -.3, EP[2]]), at(G.box(22, 8, .4, '#e8d8c0', { base: true }), [EP[0], 0, EP[2] - 7]),
    at(G.box(.4, 8, 14, '#e0ceb4', { base: true }), [EP[0] - 11, 0, EP[2]]), at(G.box(10, .05, 8, '#a02a3a', { base: true }), [EP[0], 0, EP[2]]),
    ...[-8, -4, 4, 8].map(x => at(G.box(.8, 8, .8, '#e8c060', { base: true }), [EP[0] + x, 0, EP[2] - 6.4])),
    ...[-6, 0, 6].map(x => at(G.box(2.4, 4, .1, '#bfe0f6', { base: true }), [EP[0] + x, 2, EP[2] - 6.76])),
    at(G.box(22, .6, .6, '#e8c060', { base: true }), [EP[0], 7.4, EP[2] - 6.6]), at(G.box(1.6, 1.1, 1.0, '#f2ead8', { base: true }), [EP[0], 0, EP[2] - 1])]), { outline: false });
  mk(S, merge([at(G.cyl(.1, .1, 1.4, 6, '#c9a23c'), [EP[0], 6.4, EP[2]]), at(G.ico(.8, 2, '#fff2c0'), [EP[0], 6, EP[2]])]), { emis: .8, outline: false, cast: false });
  // Antikmarkt (draussen, Tag)
  mk('EGGM', G.box(120, .4, 60, '#9a9a8a', { base: true }), { pos: [EM[0], -.4, EM[2]], outline: false, cast: false });
  const M = []; [[-6, 0, '#e0303a'], [0, -1, '#2a8fd6'], [6, 0, '#35a862']].forEach(([x, z, c]) => { M.push(at(G.box(3.4, .12, 1.6, '#8a6a46', { base: true }), [EM[0] + x, 1, EM[2] + z]), ...[[-1.5, -.7], [1.5, -.7], [-1.5, .7], [1.5, .7]].map(([a, b]) => at(G.box(.12, 1, .12, '#6b4226', { base: true }), [EM[0] + x + a, 0, EM[2] + z + b])),
    at(G.box(3.8, .12, 2.2, c, { base: true }), [EM[0] + x, 2.6, EM[2] + z]), ...[-1.8, 1.8].map(a => at(G.cyl(.05, .05, 2.6, 6, '#3a3a44'), [EM[0] + x + a, 0, EM[2] + z + .9]))) });
  for (let k = 0; k < 18; k++) M.push(at(k % 3 ? G.box(.3 + G.hash(k) * .3, .2 + G.hash(k, 1) * .4, .3, ['#c9ccd4', '#8a5a32', '#6a8acb', '#d8c8a8'][k % 4], { base: true }) : G.cyl(.15, .1, .4, 8, '#9aa0ac'), [EM[0] - 7.4 + (k % 6) * .55 + Math.floor(k / 6) * 6, 1.12, EM[2] + (k % 2) * .4 - .2 - (Math.floor(k / 6) == 1 ? 1 : 0)]));
  M.push(...[-14, -10, 12, 16].map((x, k) => at(G.box(3, 2 + k % 2, 3, ['#c9b896', '#a8b0c0', '#d8c8a8', '#b8a07a'][k], { base: true }), [EM[0] + x, 0, EM[2] - 6])));
  mk('EGGM', merge(M));
  // Werkstatt (Schrott + Schmelzofen)
  mk('EGGW', merge([at(G.box(14, .3, 10, '#5a5e6a', { base: true }), [EW[0], -.3, EW[2]]), at(G.box(14, 5, .3, '#7a6a5a', { base: true }), [EW[0], 0, EW[2] - 5]), at(G.box(.3, 5, 10, '#6a5a4a', { base: true }), [EW[0] - 7, 0, EW[2]]),
    at(G.box(3, .14, 1.4, '#4a4e5a', { base: true }), [EW[0] + 1.6, 1.0, EW[2] - 1.4]), at(G.box(2.8, 1.0, 1.2, '#3a3e4a', { base: true }), [EW[0] + 1.6, 0, EW[2] - 1.4])]), { outline: false });
  mk('EGGW', merge([...Array(22)].map((_, k) => at(k % 2 ? G.box(.6 + G.hash(k) * .6, .2, .5, ['#9aa0ac', '#8a6a46', '#b8744a'][k % 3]) : G.cyl(.25, .25, .7, 10, ['#9aa0ac', '#b8744a'][k % 2]), [EW[0] - 5.5 + (k % 7) * .6, .2 + Math.floor(k / 7) * .3, EW[2] - 3.8 + G.hash(k, 3) * 1.2], [0, k, .3 * (k % 3)]))), { outline: true });
  mk('EGGW', merge([at(G.cyl(.9, .8, 1.4, 16, '#3a3a44'), [EW[0] - 2.2, 0, EW[2] - 1.2]), at(G.cyl(.55, .5, .6, 14, '#5a5e6a'), [EW[0] - 2.2, 1.4, EW[2] - 1.2])]));
  // Juwelier London: dunkles Holz, Vitrine
  mk('EGGL', merge([at(G.box(12, .3, 9, '#3a2a22', { base: true }), [EL[0], -.3, EL[2]]), at(G.box(12, 5, .3, '#2a3a32', { base: true }), [EL[0], 0, EL[2] - 4.5]), at(G.box(.3, 5, 9, '#26342c', { base: true }), [EL[0] - 6, 0, EL[2]]),
    at(G.box(3, 1.0, 1.2, '#5a3a26', { base: true }), [EL[0], 0, EL[2] - 1.2]), at(G.box(.9, .5, .9, '#6a1a2a', { base: true }), [EL[0], 1.0, EL[2] - 1.2])]), { outline: false });
  mk('EGGL', G.box(1.4, 1.1, 1.2, '#d8f0ff'), { pos: [EL[0], 1.5, EL[2] - 1.2], alpha: .18, spec: 1, outline: false, cast: false, recv: false });
})();
// Das Ei (Gold, 3 Saphir-Schleifen, Staender) – Wurzel bewegt sich zwischen den Orten
function eggGeo(gold = '#f0c040') { return merge([at(G.ico(.22, 3, gold, 0, 1, 1.25), [0, .42, 0]), at(G.cyl(.06, .1, .16, 12, '#e0b030'), [0, .06, 0]), ...[0, 1, 2].map(k => at(G.cyl(.012, .012, .2, 6, '#e0b030'), [Math.cos(k * 2.1) * .12, 0, Math.sin(k * 2.1) * .12], [0, 0, .5 * (k - 1)])),
  ...[0, 1, 2].map(k => at(G.ico(.035, 1, '#3a6ad6'), [Math.cos(k * 2.1) * .21, .5, Math.sin(k * 2.1) * .21])), at(G.ico(.02, 1, '#ffffff'), [0, .7, 0])]).smooth() }
const EGG = mk('EGG', eggGeo(), { pos: [EP[0], 1.1, EP[2] - 1], spec: 1, emis: .12 });
const EGG2 = [0, 1, 2].map(k => mk('EGG', eggGeo(['#d8e8f8', '#f0c0d0', '#c0e8c8'][k]), { pos: [EP[0] - 1.6 + k * 1.6, 1.1, EP[2] - 1], spec: 1, alpha: .5, emis: .2, outline: false }));
const EFIRE = mk('EGGW', G.ico(.5, 2, '#ff8a2a', .3, 3), { pos: [EW[0] - 2.2, 2.1, EW[2] - 1.2], emis: 1, outline: false, cast: false });
const ECRATES = [0, 1, 2].map(k => mk('EGG', merge([at(G.box(1.2, .9, .9, '#a07a4a', { base: true }), [0, 0, 0]), at(G.box(1.24, .1, .94, '#7a5a32', { base: true }), [0, .4, 0])]), { pos: [EP[0] - 5 + k * 1.6, 0, EP[2] + 1.6] }));
const ELAPTOP = mk('EGGW', merge([at(G.box(1.1, .05, .75, '#c9ccd4', { base: true }), [0, 0, 0]), at(G.box(1.1, .72, .05, '#c9ccd4', { base: true }), [0, 0, -.36], [-.25, 0, 0])]), { pos: [EW[0] + 1.4, 1.14, EW[2] - 1.4] });
CHAP.push({ line: 'n3', n: 3, title: 'THE LOST FABERGÉ EGG', year: '1887', place: '🇷🇺 Russia' });
let EG_I0 = 0;
function egUpd(t, i) {
  const k = i - EG_I0; EGG.vis = true; EGG.rot = [0, t * .5, 0]; EGG.alpha = 1; EGG2.forEach(m => m.vis = false); EFIRE.vis = k == 5 || k == 4; EFIRE.scl = [1 + .08 * Math.sin(t * 9), 1 + .15 * Math.sin(t * 7), 1];
  ECRATES.forEach((m, j) => { m.vis = k == 2; m.pos = [EP[0] - 5 + j * 1.6 + (k == 2 ? (t - Lt(i).start) * 1.4 : 0), 0, EP[2] + 1.6] });
  if (k <= 3) EGG.pos = [EP[0], 1.1, EP[2] - 1];
  if (k == 2) EGG.vis = t < wt(i, /seized/) + .2;
  if (k == 3) { EGG.alpha = Math.max(.01, 1 - ez(cl((t - wt(i, /disappeared/)) / 1, 0, 1))); EGG.vis = EGG.alpha > .02 }
  if (k == 4) EGG.pos = [EM[0], 1.12, EM[2] - 1.2];
  if (k == 5 || k == 6 || k == 7) EGG.pos = [EW[0] + .5, 1.14, EW[2] - 1.3];
  if (k == 8) EGG.pos = [EL[0], 1.5, EL[2] - 1.2];
  if (k == 9) { EGG.vis = false; EGG2.forEach((m, j) => { m.vis = t > Lt(i).start + 1.2 + j * .4 && t > wt(i, /still/) - .2; m.rot = [0, t * .4, 0] }) }
}
SHOT.e_palace = { set: 'EGG', light: 'indoorWarm',
  cam: i => { EG_I0 = i; return mv(cm([EP[0] + 6, 4.2, EP[2] + 9], [EP[0], 2.4, EP[2] - 3], 50), cm([EP[0] + 3.6, 3.2, EP[2] + 6.4], [EP[0], 2, EP[2] - 2], 48)) },
  upd: egUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🥚 EASTER 1887 · ST. PETERSBURG', '#232838', '#fff', 44),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.e_gift = { set: 'EGG', light: 'indoorWarm',
  cam: i => cut2(i, /inside/i, cm([EP[0] + 2, 2.4, EP[2] + 4.4], [EP[0], 1.7, EP[2] - 1], 48), cm([EP[0] + 1.4, 2.2, EP[2] + 3.6], [EP[0], 1.6, EP[2] - 1], 46),
    cm([EP[0] + .3, 1.75, EP[2] + .2], [EP[0], 1.55, EP[2] - 1], 34), cm([EP[0] + .2, 1.7, EP[2] - .1], [EP[0], 1.55, EP[2] - 1], 32)),
  upd: egUpd,
  figs: (t, i) => t > wt(i, /inside/i) - .15 ? '' : fig([EP[0] - 1.6, 0, EP[2]], 'tsar', { mouth: 'smile', blink: bl(t, 0), look: [4, 2], hR: [190, 150] }) + fig([EP[0] + 1.5, 0, EP[2] + .2], 'empress', { mouth: 'o', blink: bl(t, 1), look: [-4, 2], hR: [170, 60], hL: [30, 60] }),
  ui: (t, i) => labelAt([EP[0], 2.2, EP[2] - 1], PILL('FABERGÉ', '#ffd166', OL, 40), t, wt(i, /faberge/i) - .1, wt(i, /inside/i) - .2) + pillAt(960, 170, t, wt(i, /watch/) - .1, nextStart(i), '⌚ A TINY WATCH INSIDE', '#232838', '#fff', 52),
  sfx: i => [{ k: 'shimmer', t: wt(i, /golden/) }, { k: 'tick', t: wt(i, /watch/) }] };
SHOT.e_revolution = { set: 'EGG', light: 'indoorDark',
  cam: i => mv(cm([EP[0] + 4, 3, EP[2] + 8], [EP[0] - 2, 1.6, EP[2]], 50), cm([EP[0] + 3, 2.6, EP[2] + 6.6], [EP[0] - 1, 1.6, EP[2]], 48)),
  upd: egUpd,
  figs: (t, i) => { let h = ''; [0, 1].forEach(k => { const x = EP[0] - 4 + k * 2.6 + (t - Lt(i).start) * 1.4; h += fig([x, 0, EP[2] + 2.8], 'redguard', Object.assign(walk(t + k, 8), { mouth: 'hmm', blink: bl(t, k), look: [5, 0], hR: [170, 120], hL: [40, 120] })) });
    const s = wt(i, /seized/); if (t > s - .3) h += fig([EP[0] + 1.4, 0, EP[2] - .2], 'redguard', { mouth: 'grin', blink: bl(t, 3), look: [-5, 3], hL: [10, 140] }); return h },
  ui: (t, i) => stampAt(1400, 300, t, wt(i, /seized/), 'SEIZED', '#e0303a', 110, 6) + pillAt(960, 170, t, wt(i, /sold/) - .1, nextStart(i), '💵 SOLD ABROAD', '#35a862', '#fff', 52),
  sfx: i => [{ k: 'impact', t: wt(i, /revolution/), g: .5 }, { k: 'impact', t: wt(i, /seized/) }, { k: 'cash', t: wt(i, /sold/) }] };
SHOT.e_lost = { set: 'EGG', light: 'indoorDark',
  cam: i => mv(cm([EP[0] + .6, 2, EP[2] + 1.8], [EP[0], 1.55, EP[2] - 1], 38), cm([EP[0] + .3, 1.9, EP[2] + 1.2], [EP[0], 1.55, EP[2] - 1], 36)),
  upd: egUpd,
  ui: (t, i) => bigText(960, 330, t, wt(i, /disappeared/) + .4, nextStart(i), '?', 260, '#ffd166') + pillAt(960, 170, t, wt(i, /decades/) - .1, nextStart(i), '⏳ LOST FOR DECADES', '#232838', '#fff', 56),
  sfx: i => [{ k: 'air', t: wt(i, /disappeared/), d: 1 }, { k: 'tick', t: wt(i, /decades/) }] };
SHOT.e_market = { set: 'EGGM', light: 'day',
  cam: i => cut2(i, /spots/, cm([EM[0] + 8, 4, EM[2] + 12], [EM[0], 1.4, EM[2]], 50), cm([EM[0] + 5, 3.4, EM[2] + 9], [EM[0], 1.4, EM[2]], 48),
    cm([EM[0] + .9, 2, EM[2] + 1.6], [EM[0], 1.3, EM[2] - 1.2], 40), cm([EM[0] + .6, 1.8, EM[2] + 1.1], [EM[0], 1.3, EM[2] - 1.2], 36)),
  upd: egUpd,
  figs: (t, i) => t > wt(i, /spots/) - .15 ? '' : fig([EM[0] + 1.6 - Math.max(0, 1.6 - (t - Lt(i).start) * .6), 0, EM[2] + 1.6], 'scrap', Object.assign(walk(t, 7), { mouth: 'o', blink: bl(t, 0), look: [-4, 3] })),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /midwest/i) - .1, wt(i, /spots/) - .2, '🇺🇸 A SCRAP METAL DEALER', '#232838', '#fff', 52) + pillAt(960, 930 - 110, t, wt(i, /decades/) - .1, wt(i, /spots/) - .2, '🛒 ANTIQUES MARKET', '#2a8fd6', '#fff', 44),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: 1 }, { k: 'shimmer', t: wt(i, /spots/) }] };
SHOT.e_melt = { set: 'EGGW', light: 'indoorWarm',
  cam: i => mv(cm([EW[0] + 1.4, 2.8, EW[2] + 4.4], [EW[0] - 1.2, 1.3, EW[2] - 1.2], 48), cm([EW[0] + .8, 2.4, EW[2] + 3.4], [EW[0] - 1.4, 1.3, EW[2] - 1.2], 46)),
  upd: egUpd,
  figs: (t, i) => fig([EW[0] + 1.4, 0, EW[2] - .2], 'scrap', { mouth: 'grin', talk: tk(t, i) * .5, blink: bl(t, 0), look: [-5, 2], hL: [20, 150] }),
  ui: (t, i) => counter(960, 170, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, wt(i, /dollars/), 0, 14000, v => '💵 PAID: $' + Math.round(v / 100) * 100 / 1000 + 'K', '#35a862', '#fff', 64) + stampAt(1400, 340, t, wt(i, /melt/) - .05, '🔥 MELT IT?', '#e0303a', 90, 6),
  sfx: i => [{ k: 'cash', t: wt(i, /dollars/) }, { k: 'impact', t: wt(i, /melt/), g: .5 }] };
SHOT.e_google = { set: 'EGGW', light: 'indoorDark',
  cam: i => mv(cm([EW[0] + 2.6, 2.1, EW[2] + 1.6], [EW[0] + 1.4, 1.5, EW[2] - 1.6], 44), cm([EW[0] + 2.2, 2, EW[2] + 1.1], [EW[0] + 1.4, 1.5, EW[2] - 1.6], 42)),
  upd: egUpd,
  figs: (t, i) => fig([EW[0] + 3.3, 0, EW[2] - 1.0], 'scrap', { mouth: 'hmm', blink: bl(t, 0), look: [-5, 4], hR: [130, 150], hL: [70, 150] }),
  ui: (t, i) => { const a = wt(i, /typed/) - .2; if (t < a) return pillAt(960, 170, t, wt(i, /no one/) - .1, nextStart(i), '❌ NO BUYER', '#e0303a', '#fff', 56);
    const q = 'egg vacheron constantin', n = Math.round(q.length * cl((t - a) / 1.6, 0, 1));
    return `<div style="position:absolute;left:960px;top:200px;transform:translate(-50%,0) scale(${pop(t, a)});width:900px;padding:22px 30px;background:#fff;border:8px solid ${OL};border-radius:60px;font:700 50px P;color:#232838;box-shadow:0 14px 0 #0005;z-index:2200">🔍 ${q.slice(0, n)}<span style="opacity:${Math.floor(t * 3) % 2}">|</span></div>` },
  sfx: i => [{ k: 'error', t: wt(i, /no one/) }, { k: 'type', t: wt(i, /typed/), n: 14 }] };
SHOT.e_article = { set: 'EGGW', light: 'indoorDark',
  cam: i => mv(cm([EW[0] + 2.2, 2, EW[2] + 1.1], [EW[0] + 1.4, 1.5, EW[2] - 1.6], 42), cm([EW[0] + 2, 1.95, EW[2] + .8], [EW[0] + 1.4, 1.5, EW[2] - 1.6], 40)),
  upd: egUpd,
  ui: (t, i) => { const a = Lt(i).start + .1; if (t < a) return '';
    return `<div style="position:absolute;left:960px;top:120px;transform:translate(-50%,0) scale(${pop(t, a)});width:860px;background:#fff;border:8px solid ${OL};border-radius:16px;overflow:hidden;box-shadow:0 14px 0 #0005;z-index:2200">
      <div style="background:#232838;color:#fff;font:900 34px IB;padding:10px 24px">📰 NEWS</div><div style="display:flex;gap:24px;padding:24px;align-items:center">
      <svg width="200" height="230" viewBox="0 0 200 230"><ellipse cx="100" cy="100" rx="70" ry="88" fill="#f0c040" stroke="${OL}" stroke-width="7"/><circle cx="60" cy="90" r="10" fill="#3a6ad6"/><circle cx="140" cy="90" r="10" fill="#3a6ad6"/><rect x="80" y="190" width="40" height="30" fill="#e0b030" stroke="${OL}" stroke-width="5"/></svg>
      <div style="font:900 52px/1.1 IB;color:${OL}">HAVE YOU SEEN THIS LOST FABERGÉ EGG?</div></div></div>` + stampAt(1500, 640, t, wt(i, /exactly/) - .05, 'MATCH!', '#35a862', 100, -6) },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'impact', t: wt(i, /exactly/), g: .5 }] };
SHOT.e_value = { set: 'EGGL', light: 'indoorWarm',
  cam: i => mv(cm([EL[0] + 2.4, 2.4, EL[2] + 3.6], [EL[0], 1.6, EL[2] - 1.2], 46), cm([EL[0] + .8, 1.9, EL[2] + 1.4], [EL[0], 1.7, EL[2] - 1.2], 40)),
  upd: egUpd,
  figs: (t, i) => fig([EL[0] - 1.8, 0, EL[2] - .4], 'jeweler', { mouth: 'o', blink: bl(t, 0), look: [5, 0], prop: PROP.magnifier, hR: [200, 120] }),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /london/i) - .1, nextStart(i), '🇬🇧 EXPERTS IN LONDON: REAL!', '#232838', '#fff', 50) + labelAt([EL[0], 2.4, EL[2] - 1.2], PILL('THE THIRD IMPERIAL EGG', '#ffd166', OL, 40), t, wt(i, /third/i) - .1, nextStart(i)) +
    counter(960, 300, t, wt(i, /worth/) - .1, nextStart(i), wt(i, /worth/), wt(i, /dollars/), 0, 33, v => '~$' + Math.round(v) + ' MILLION', '#35a862', '#fff', 84),
  sfx: i => [{ k: 'ding', t: wt(i, /confirmed/) }, { k: 'cash', t: wt(i, /dollars/) }] };
SHOT.e_missing = { set: 'EGG', light: 'indoorDark',
  cam: i => mv(cm([EP[0], 2.6, EP[2] + 4.6], [EP[0], 1.5, EP[2] - 1], 46), cm([EP[0], 2.2, EP[2] + 3.4], [EP[0], 1.5, EP[2] - 1], 44)),
  upd: (t, i) => { egUpd(t, i); if (t < wt(i, /still/) - .15) { EGG.vis = true; EGG.pos = [EP[0], 1.1, EP[2] - 1] } },
  ui: (t, i) => stampAt(1300, 300, t, wt(i, /almost/) - .05, 'ALMOST MELTED', '#e0303a', 80, -6, wt(i, /still/) - .15) + bigText(960, 200, t, wt(i, /nobody/) - .1, nextStart(i), 'STILL MISSING', 100, '#ffd166', -3),
  sfx: i => [{ k: 'impact', t: wt(i, /almost/), g: .5 }, { k: 'shimmer', t: wt(i, /nobody/) }] };
