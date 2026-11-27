// ===================== #6 Set BOOT: Car-Boot-Sale West London / Wohnzimmer / Juwelier =====================
const BX = 600, BB = [BX, 0, 0], BH = [BX, 0, 90], BJ = [BX, 0, -90];
LOOK.seller = { sw: '#3a6a4a', swd: '#2e5a3c', pa: '#3a3f55', hat: HAT.beanie };
LOOK.seller2 = { sw: '#d68a2a', swd: '#b8741e', pa: '#2c3044', hat: HAT.cap };
LOOK.jeweler = { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', mid: MID.tie };
PROP.ring = `<g transform="translate(0,-6)"><circle cx="0" cy="0" r="9" fill="none" stroke="#f0c040" stroke-width="5"/><path d="M-9,-14 L0,-24 L9,-14 L0,-6Z" fill="#eaf6ff" stroke="${OL}" stroke-width="3"/><circle cx="-14" cy="-26" r="3" fill="#fff"/><circle cx="14" cy="-22" r="2" fill="#fff"/></g>`;
function car(x, z, col, ry = 0, open = true) {
  const L = [at(G.box(4, .8, 1.8, col, { base: true }), [0, .35, 0]), at(G.box(2.2, .7, 1.6, col, { base: true }), [-.2, 1.15, 0]), at(G.box(2.0, .5, 1.62, '#a8d8f0', { base: true }), [-.2, 1.2, 0]),
    ...[[-1.3, .9], [1.3, .9], [-1.3, -.9], [1.3, -.9]].map(([a, b]) => at(G.cyl(.36, .36, .26, 14, '#22242c'), [a, .36, b], [PI / 2, 0, 0]))];
  if (open) L.push(at(G.box(.08, .9, 1.6, col, { base: true }), [1.95, 1.15, 0], [0, 0, -.5]));
  const g = merge(L); return [g, G.m4.compose([x, 0, z], [0, ry, 0], [1, 1, 1])];
}
(function boot() {
  const S = 'BOOT';
  mk(S, G.box(120, .4, 80, '#8a9a7a', { base: true }), { pos: [BX, -.4, 0], outline: false, cast: false });
  mk(S, G.box(40, .05, 20, '#6a7278', { base: true }), { pos: [BX, 0, 0], outline: false, cast: false });
  // Autos mit offenen Kofferraeumen + Tische
  const C = [[-9, -3, '#d64545', 0], [-3, -3.4, '#2a8fd6', 0], [3, -3, '#f2b21c', 0], [9, -3.2, '#35a862', 0], [-6, 5.4, '#e8e8ee', PI], [2, 5.6, '#8a5ab0', PI]];
  const M = []; C.forEach(([x, z, c, r]) => { M.push(car(BX + x, z, c, r)); const tz = z + (r ? -2 : 2);
    M.push(at(G.box(2.6, .1, 1.1, '#f4efe2', { base: true }), [BX + x + 1, .9, tz]), ...[[-1.2, -.45], [1.2, -.45], [-1.2, .45], [1.2, .45]].map(([a, b]) => at(G.box(.06, .9, .06, '#9aa0ac', { base: true }), [BX + x + 1 + a, 0, tz + b])));
    for (let k = 0; k < 6; k++) M.push(at(k % 3 ? G.box(.25 + G.hash(k, x) * .3, .15 + G.hash(k, z) * .35, .25, ['#c9ccd4', '#8a5a32', '#6a8acb', '#d8c8a8', '#e07a5a'][k % 5], { base: true }) : G.cyl(.12, .1, .3, 8, '#9aa0ac'), [BX + x + .1 + k * .38, 1.0, tz + (k % 2) * .3 - .15])) });
  mk(S, merge(M));
  // Baeume + Zaun hinten
  const T = []; for (let k = 0; k < 14; k++) T.push(...leafy(BX - 26 + k * 4 + G.hash(k) * 2, -14 - G.hash(k, 1) * 4, .9 + G.hash(k, 2) * .4, k % 2 ? '#3a7a3a' : '#4a8a3a'));
  mk(S, merge(T));
  // Schmuckkiste auf dem gelben Tisch
  mk(S, merge([at(G.box(.8, .14, .55, '#6a3a2a', { base: true }), [0, 0, 0]), at(G.box(.72, .04, .47, '#b8323a', { base: true }), [0, .12, 0]),
    ...[...Array(9)].map((_, k) => at(G.ico(.04, 1, ['#e0303a', '#60a5fa', '#35e08a', '#ffd166'][k % 4]), [-.3 + (k % 5) * .15, .17, -.12 + Math.floor(k / 5) * .2]))]), { pos: [BX + 3.6, 1.0, -1.0] });
  // Wohnzimmer
  mk(S, merge([at(G.box(12, .3, 9, '#8a6a4a', { base: true }), [BH[0], -.3, BH[2]]), at(G.box(12, 5, .3, '#e8d8b8', { base: true }), [BH[0], 0, BH[2] - 4.5]),
    at(G.box(.3, 5, 9, '#dcc8a4', { base: true }), [BH[0] - 6, 0, BH[2]]), at(G.box(3.4, .9, 1.2, '#5a7ab0', { base: true }), [BH[0] - 2, 0, BH[2] - 3.4]), at(G.box(3.4, 1, .3, '#4a6aa0', { base: true }), [BH[0] - 2, .6, BH[2] - 3.9]),
    at(G.box(1.2, 1.6, .1, '#f4efe2', { base: true }), [BH[0] + 2.4, 1.6, BH[2] - 4.32]), at(G.box(1.2, .3, .1, '#e0303a', { base: true }), [BH[0] + 2.4, 2.9, BH[2] - 4.32]),
    at(G.box(1.8, 1.2, .1, '#6a9ad6', { base: true }), [BH[0] - 2, 2.2, BH[2] - 4.32]), at(G.box(4, .05, 3, '#c0606a', { base: true }), [BH[0], 0, BH[2] - 1])]), { outline: false });
  // Juwelier
  mk(S, merge([at(G.box(12, .3, 9, '#3a2a22', { base: true }), [BJ[0], -.3, BJ[2]]), at(G.box(12, 5, .3, '#2a3a32', { base: true }), [BJ[0], 0, BJ[2] - 4.5]), at(G.box(.3, 5, 9, '#26342c', { base: true }), [BJ[0] - 6, 0, BJ[2]]),
    at(G.box(3, 1.0, 1.2, '#5a3a26', { base: true }), [BJ[0], 0, BJ[2] - 1.2]), at(G.box(.9, .3, .9, '#1a1a2a', { base: true }), [BJ[0], 1.0, BJ[2] - 1.2]),
    ...[-4, 4].map(x => at(G.box(2.4, 2.4, .6, '#4a3a2a', { base: true }), [BJ[0] + x, 0, BJ[2] - 4]))]), { outline: false });
})();
const BRING = mk('BOOT', ringGeo(), { pos: [BX + 3.6, 1.24, -1.0], spec: 1, emis: .2, outline: false });
const BSPARK = mk('BOOT', G.ico(.06, 1, '#ffffff'), { pos: [BX + 3.6, 1.38, -1.0], emis: 1, outline: false, cast: false });
CHAP.push({ line: 'n6', n: 6, title: 'THE £10 RING', year: 'late 1980s', place: '🇬🇧 West London' });
function rgUpd(t, i, where = 'boot') {
  BRING.vis = true; BSPARK.vis = true; BRING.scl = [1, 1, 1]; BRING.rot = [0, t * .6, 0];
  if (where == 'boot') BRING.pos = [BX + 3.6, 1.24, -1.0];
  if (where == 'jew') { BRING.pos = [BJ[0], 1.42, BJ[2] - 1.2]; BRING.scl = [1.4, 1.4, 1.4] }
  if (where == 'none') BRING.vis = false;
  BSPARK.pos = X(BRING.pos, .02, .1 * BRING.scl[0], 0); BSPARK.vis = BRING.vis; const s = .5 + 1.2 * Math.max(0, Math.sin(t * 5)) ** 6; BSPARK.scl = [s, s, s];
}
const sellers = (t, k = 0) => fig([BX + 4.6, 0, -1.6], 'seller2', { mouth: 'smile', blink: bl(t, 3), look: [-4, 2], hL: [40, 140] }) + fig([BX - 5.4, 0, -1.4], 'seller', { mouth: 'smile', blink: bl(t, 5), look: [4, 2] });
SHOT.r_boot = { set: 'BOOT', light: 'day',
  cam: i => mv(cm([BX + 12, 7, 14], [BX, 1, -1], 50), cm([BX + 8, 5.4, 11], [BX, 1, -1], 48)),
  upd: (t, i) => rgUpd(t, i),
  figs: (t, i) => sellers(t) + fig([BX - 1, 0, 1.6 - (t - Lt(i).start) * .2], 'lady', Object.assign(walk(t, 6), { mouth: 'smile', blink: bl(t, 0), look: [2, 2] })),
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🚗 CAR BOOT SALE · WEST LONDON', '#232838', '#fff', 44),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.r_browse = { set: 'BOOT', light: 'day',
  cam: i => mv(cm([BX - 4, 2.4, 6], [BX + 1, 1.3, -1], 46), cm([BX - 1, 2.3, 5.4], [BX + 2.6, 1.3, -1], 46)),
  upd: (t, i) => rgUpd(t, i),
  figs: (t, i) => { const u = cl((t - Lt(i).start) / (nextStart(i) - Lt(i).start), 0, 1); return sellers(t) + fig([BX - 2 + u * 4.4, 0, .3], 'lady', Object.assign(walk(t, 6), { mouth: 'smile', talk: 0, blink: bl(t, 0), look: [4, 3] })) },
  ui: (t, i) => pillAt(960, 170, t, wt(i, /flea/) - .1, nextStart(i), '= A FLEA MARKET 🚗🧺', '#2a8fd6', '#fff', 54),
  sfx: i => [{ k: 'pop', t: wt(i, /flea/) }] };
SHOT.r_haggle = { set: 'BOOT', light: 'day',
  cam: i => cut2(i, /seller/, cm([BX + 3.7, 2.4, .5], [BX + 3.6, 1.1, -1.0], 40), cm([BX + 3.65, 2.2, .2], [BX + 3.6, 1.1, -1.0], 36),
    cm([BX + 3.2, 2.2, 4.2], [BX + 3.6, 1.4, -1.2], 46), cm([BX + 3.4, 2.1, 3.6], [BX + 3.7, 1.4, -1.2], 44)),
  upd: (t, i) => rgUpd(t, i),
  figs: (t, i) => t < wt(i, /seller/) - .15 ? '' : fig([BX + 4.6, 0, -1.6], 'seller2', { mouth: t < wt(i, /haggles/) ? 'grin' : 'sad', talk: t < wt(i, /haggles/) ? tk(t, i) * .5 : 0, blink: bl(t, 3), look: [-4, 2], hL: [40, 140] }) +
    fig([BX + 2.4, 0, -.2], 'lady', { mouth: t > wt(i, /haggles/) ? 'grin' : 'hmm', blink: bl(t, 0), look: [4, 1], prop: PROP.ring, hR: [175, 120] }),
  ui: (t, i) => { const a = wt(i, /twelve/), b = wt(i, /haggles/); let h = pillAt(960, 170, t, wt(i, /costume/) - .1, wt(i, /seller/) - .2, '💍 COSTUME JEWELRY', '#232838', '#fff', 54);
    if (t > a - .1) h += bigText(1400, 300, t, a - .1, nextStart(i), `<span style="${t > b ? 'text-decoration:line-through;text-decoration-color:#e0303a;text-decoration-thickness:12px;opacity:.6' : ''}">£12</span>`, 130, '#fff');
    h += stampAt(1400, 470, t, wt(i, /ten/) - .05, '£10', '#35a862', 130, -8); return h },
  sfx: i => [{ k: 'shimmer', t: wt(i, /sparkly/) }, { k: 'pop', t: wt(i, /twelve/) }, { k: 'cash', t: wt(i, /ten/) }] };
SHOT.r_wear = { set: 'BOOT', light: 'indoorWarm',
  cam: i => mv(cm([BH[0] + 3, 2.6, BH[2] + 6.4], [BH[0], 1.4, BH[2] - 2], 48), cm([BH[0] + 2, 2.3, BH[2] + 4.6], [BH[0] + .4, 1.4, BH[2] - 2], 46)),
  upd: (t, i) => rgUpd(t, i, 'none'),
  figs: (t, i) => fig([BH[0] + .6, 0, BH[2] - 1], 'lady', { mouth: 'smile', blink: bl(t, 0), look: [2, 2], prop: PROP.ring, hR: [200, 100 + 8 * Math.sin(t * 3)] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /glass/) - .1, nextStart(i), '🔍 "JUST GLASS"', '#232838', '#fff', 54) +
    counter(1460, 330, t, wt(i, /wears/) - .1, nextStart(i), wt(i, /wears/), wt(i, /years/), 1988, 2017, v => '📅 ' + Math.round(v), '#2a8fd6', '#fff', 70) +
    stampAt(1460, 480, t, wt(i, /years/) - .05, '~30 YEARS', '#e0303a', 90, -6),
  sfx: i => [{ k: 'tick', t: wt(i, /wears/) }, { k: 'tick', t: wt(i, /wears/) + .5 }, { k: 'tick', t: wt(i, /wears/) + 1 }, { k: 'impact', t: wt(i, /years/), g: .4 }] };
SHOT.r_jeweler = { set: 'BOOT', light: 'indoorWarm',
  cam: i => mv(cm([BJ[0] + 2.6, 2.6, BJ[2] + 4.6], [BJ[0], 1.5, BJ[2] - 1.2], 48), cm([BJ[0] + 1.6, 2.2, BJ[2] + 3.4], [BJ[0], 1.5, BJ[2] - 1.2], 44)),
  upd: (t, i) => rgUpd(t, i, 'jew'),
  figs: (t, i) => fig([BJ[0] - 1.8, 0, BJ[2] - .6], 'jeweler', { mouth: 'hmm', blink: bl(t, 0), look: [5, 1], prop: PROP.magnifier, hR: [200, 120] }) + fig([BJ[0] + 1.9, 0, BJ[2] - .2], 'lady', { mouth: 'smile', blink: bl(t, 2), look: [-4, 1] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /2017/) - .1, nextStart(i), '📅 2017 · A JEWELER', '#232838', '#fff', 54),
  sfx: i => [{ k: 'ding', t: wt(i, /jeweler/) }] };
SHOT.r_real = { set: 'BOOT', light: 'indoorWarm',
  cam: i => mv(cm([BJ[0] + .5, 1.8, BJ[2] + .3], [BJ[0], 1.5, BJ[2] - 1.2], 36), cm([BJ[0] + .25, 1.7, BJ[2] - .2], [BJ[0], 1.5, BJ[2] - 1.2], 30)),
  upd: (t, i) => rgUpd(t, i, 'jew'),
  ui: (t, i) => stampAt(960, 250, t, wt(i, /real/) - .05, '💎 REAL DIAMOND', '#35a862', 100, -5) + pillAt(960, 760, t, wt(i, /carats/) - .1, nextStart(i), '26.27 CARATS · 1800s', '#ffd166', OL, 60),
  sfx: i => [{ k: 'error', t: wt(i, /glass/), g: .5 }, { k: 'impact', t: wt(i, /real/) }, { k: 'shimmer', t: wt(i, /carats/) }] };
SHOT.r_estimate = { set: 'AUC', light: 'indoorWarm',
  cam: i => mv(...CAM_POD),
  upd: (t, i) => aucUpd(t, i, 0),
  figs: (t, i) => auctioneer(t, i),
  ui: (t, i) => pillAt(960, 170, t, Lt(i).start + .1, nextStart(i), "🔨 SOTHEBY'S · LONDON", '#232838', '#fff', 54) + screenPrice(t, wt(i, /expected/), nextStart(i), 'EST. £350,000'),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: .8 }, { k: 'ding', t: wt(i, /pounds/) }] };
SHOT.r_sold = { set: 'AUC', light: 'indoorWarm',
  cam: i => cut2(i, /tenner/, ...CAM_AUD, ...CAM_POD),
  upd: (t, i) => aucUpd(t, i, 0),
  figs: (t, i) => t < wt(i, /tenner/) - .15 ? audience(t, i, 1) : auctioneer(t, i),
  ui: (t, i) => counter(960, 180, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, wt(i, /pounds/), 350000, 656750, v => '£' + Math.round(v).toLocaleString('en-US'), '#35a862', '#fff', 84) +
    stampAt(1450, 420, t, wt(i, /pounds/) + .1, 'SOLD!', '#e0303a', 120, -8) + bigText(960, 330, t, wt(i, /tenner/) - .1, nextStart(i), '£10 ➜ £656,750', 90, '#ffd166'),
  sfx: i => [{ k: 'tick', t: Lt(i).start + .4 }, { k: 'tick', t: Lt(i).start + .9 }, { k: 'impact', t: wt(i, /pounds/) }, { k: 'cash', t: wt(i, /pounds/) + .2 }] };
