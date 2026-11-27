// ===================== #5 Set FLEA: Flohmarkt Adamstown 1989 / Werkbank zu Hause =====================
const DX = 1200, DM = [DX, 0, 0], DH = [DX, 0, -90];
LOOK.analyst = { sw: '#6a8ab0', swd: '#5a7aa0', pa: '#3a3f55', mid: MID.tie };
LOOK.vendor = { sw: '#a05a3a', swd: '#8a4a2e', pa: '#3a3f55', hat: HAT.cap };
PROP.frame = `<g transform="translate(-46,-70)"><rect x="0" y="0" width="92" height="72" rx="3" fill="#8a9a80" stroke="#a87a3a" stroke-width="10"/><path d="M6,52 Q30,30 50,48 Q66,36 86,52 L86,66 L6,66Z" fill="#5a6a4a"/></g>`;
(function flea() {
  const S = 'FLEA';
  mk(S, G.box(120, .4, 80, '#a8b890', { base: true }), { pos: [DX, -.4, 0], outline: false, cast: false });
  mk(S, G.box(30, .05, 6, '#c8b490', { base: true }), { pos: [DX, 0, 1], outline: false, cast: false });
  const M = []; [[-8, -3, '#e0303a'], [-2.5, -3.4, '#2a8fd6'], [3, -3, '#f2b21c'], [8.5, -3.2, '#35a862'], [-5, 5.6, '#8a5ab0'], [3, 5.8, '#e07a5a']].forEach(([x, z, c], k) => {
    const f = z > 0 ? -1 : 1;
    M.push(at(G.box(3.6, .12, 1.4, '#8a6a46', { base: true }), [DX + x, 1, z]), ...[[-1.6, -.6], [1.6, -.6], [-1.6, .6], [1.6, .6]].map(([a, b]) => at(G.box(.12, 1, .12, '#6b4226', { base: true }), [DX + x + a, 0, z + b])),
      at(G.box(4, .12, 2.4, c, { base: true }), [DX + x, 2.8, z - f * .3]), ...[-1.9, 1.9].map(a => at(G.cyl(.05, .05, 2.8, 6, '#3a3a44'), [DX + x + a, 0, z + f * .9])), ...[-1.9, 1.9].map(a => at(G.cyl(.05, .05, 2.8, 6, '#3a3a44'), [DX + x + a, 0, z - f * 1.2])));
    for (let j = 0; j < 5; j++) M.push(at(j % 2 ? G.box(.3 + G.hash(j, k) * .3, .2 + G.hash(j, k + 1) * .4, .3, ['#c9ccd4', '#8a5a32', '#6a8acb', '#d8c8a8'][j % 4], { base: true }) : G.cyl(.15, .1, .35, 8, '#9aa0ac'), [DX + x - 1.3 + j * .6, 1.12, z]));
    // Bilder an der Rueckseite des Standes
    M.push(...[-1, 0, 1].map(j => at(G.box(.8, .65, .06, ['#6a7a5a', '#8a6a4a', '#5a6a8a'][(j + k + 3) % 3], { base: true }), [DX + x + j * 1.1, 1.5, z - f * 1.1])));
  });
  mk(S, merge(M));
  const T = []; for (let k = 0; k < 14; k++) T.push(...leafy(DX - 26 + k * 4 + G.hash(k) * 2, -12 - G.hash(k, 1) * 4, .9 + G.hash(k, 2) * .4));
  mk(S, merge(T));
  // Werkbank / Kellerraum
  mk(S, merge([at(G.box(12, .3, 9, '#6a5a4a', { base: true }), [DH[0], -.3, DH[2]]), at(G.box(12, 5, .3, '#9a8a74', { base: true }), [DH[0], 0, DH[2] - 4.5]), at(G.box(.3, 5, 9, '#8a7a64', { base: true }), [DH[0] - 6, 0, DH[2]]),
    at(G.box(3.6, .14, 1.6, '#a0703a', { base: true }), [DH[0], 1.0, DH[2] - 1.4]), at(G.box(3.4, 1.0, 1.4, '#7a5226', { base: true }), [DH[0], 0, DH[2] - 1.4]),
    at(G.box(3, 1.6, .1, '#c9b48a', { base: true }), [DH[0], 1.8, DH[2] - 4.32]), ...[-1, -.4, .3, 1].map(x => at(G.box(.08, .5, .08, '#5a5e6a', { base: true }), [DH[0] + x, 2.2, DH[2] - 4.25]))]), { outline: false });
})();
// Das 4-Dollar-Bild (Landschaft) + Rahmenleisten + gefaltetes Papier
const DP0 = [DX + 3, 1.62, -3.3];           // am Stand
const DPH = [DH[0], 1.45, DH[2] - 1.5];      // auf der Werkbank (liegt schraeg)
const DPIC = texPlane('FLEA', .72, .56, paintLand, { pos: DP0 });
const DFR = [[0, .32, .9, .08], [0, -.32, .9, .08], [-.41, 0, .08, .56], [.41, 0, .08, .56]].map(([x, y, wd, ht]) => mk('FLEA', G.box(wd, ht, .07, '#a87a3a', { base: false }), { pos: [0, 0, 0], spec: .3 }));
const DPAPER = mk('FLEA', merge([at(G.box(.34, .02, .44, '#efe2c0', { base: true }), [0, 0, 0]), at(G.box(.34, .005, .006, '#c9b48a', { base: true }), [0, .022, 0])]), { pos: DPH, outline: true });
const DDECL = texPlane('FLEA', .6, .76, paintDecl, { pos: [DH[0], 1.6, DH[2] - 1.2] });
CHAP.push({ line: 'n5', n: 5, title: 'THE $4 PAINTING', year: '1989', place: '🇺🇸 Pennsylvania' });
function dpPlace(p, tilt, burst = 0, drop = 0) {
  DPIC.pos = p; DPIC.rot = [-tilt, 0, 0];
  DFR.forEach((m, j) => { const [dx, dy] = [[0, .32], [0, -.32], [-.41, 0], [.41, 0]][j]; const b = burst;
    m.pos = [p[0] + dx * (1 + b * 1.4) + (j > 1 ? Math.sign(dx) * b * .2 : 0), p[1] + dy * Math.cos(tilt) * (1 + b * 1.2) - drop * b * .3 * (j + 1) * .5, p[2] + dy * Math.sin(tilt) + .02 + b * .2];
    m.rot = [-tilt, b * (j - 1.5) * .4, b * (j % 2 ? .6 : -.5)] });
}
function dpUpd(t, i, mode) {
  DPIC.vis = true; DFR.forEach(m => m.vis = true); DPAPER.vis = false; DDECL.vis = false;
  if (mode == 'stall') dpPlace(DP0, 0);
  if (mode == 'bench') dpPlace(DPH, .35);
  if (mode == 'break') { const a = wt(i, /falls/) - .2, u = ez(cl((t - a) / .7, 0, 1)); dpPlace(DPH, .35, u, 1) }
  if (mode == 'paper') { dpPlace(X(DPH, .9, -.1, .2), .35, 1, 1); DFR.forEach(m => m.vis = false); DPAPER.vis = true; const u = ez(cl((t - wt(i, /folded/) + .3) / .8, 0, 1)); DPAPER.pos = X(DPH, -.1, -.2 + u * .25, .15 * u); DPAPER.rot = [-.35 * (1 - u), 0, 0] }
  if (mode == 'decl') { DPIC.vis = false; DFR.forEach(m => m.vis = false); DDECL.vis = true; const u = ez(cl((t - Lt(i).start) / .9, 0, 1)); DDECL.scl = [lerp(.5, 1, u), lerp(.08, 1, u), 1]; DDECL.rot = [-.12, 0, 0] }
}
SHOT.d_market = { set: 'FLEA', light: 'day',
  cam: i => mv(cm([DX + 12, 7, 14], [DX, 1.2, -1], 50), cm([DX + 7, 5, 10], [DX + 1, 1.2, -1.5], 48)),
  upd: (t, i) => dpUpd(t, i, 'stall'),
  figs: (t, i) => fig([DX + 4.8, 0, -2.2], 'vendor', { mouth: 'smile', blink: bl(t, 2), look: [-3, 2] }) + fig([DX - 2 + (t - Lt(i).start) * .5, 0, .8], 'analyst', Object.assign(walk(t, 6), { mouth: 'smile', blink: bl(t, 0), look: [3, 2] })),
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🛒 FLEA MARKET · ADAMSTOWN, PA', '#232838', '#fff', 44),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.d_buy = { set: 'FLEA', light: 'day',
  cam: i => cut2(i, /picture/, cm([DX + 3.4, 2.2, -.4], [DX + 3, 1.55, -3.3], 40), cm([DX + 3.2, 2, -1.2], [DX + 3, 1.6, -3.3], 34),
    cm([DX + 1.6, 2.2, 2.8], [DX + 2.4, 1.5, -1], 44), cm([DX + 1.8, 2.1, 2.2], [DX + 2.4, 1.5, -1], 42)),
  upd: (t, i) => { dpUpd(t, i, 'stall'); if (t > wt(i, /picture/) - .15) { DPIC.vis = false; DFR.forEach(m => m.vis = false) } },
  figs: (t, i) => t < wt(i, /picture/) - .15 ? '' : fig([DX + 4.4, 0, -2.2], 'vendor', { mouth: 'grin', blink: bl(t, 2), look: [-4, 2] }) + fig([DX + 1.6, 0, -.6], 'analyst', { mouth: 'grin', blink: bl(t, 0), look: [4, 1], prop: PROP.frame, hR: [185, 110] }),
  ui: (t, i) => stampAt(1450, 300, t, wt(i, /dollars/) - .05, '$4', '#35a862', 140, -8) + pillAt(960, 170, t, wt(i, /frame/) - .1, nextStart(i), '🖼️ HE WANTS THE FRAME', '#232838', '#fff', 56),
  sfx: i => [{ k: 'cash', t: wt(i, /dollars/) }, { k: 'pop', t: wt(i, /frame/) }] };
SHOT.d_break = { set: 'FLEA', light: 'indoorWarm',
  cam: i => mv(cm([DH[0] + 1.4, 2.4, DH[2] + 1.6], [DH[0], 1.4, DH[2] - 1.5], 44), cm([DH[0] + .9, 2.2, DH[2] + 1], [DH[0], 1.4, DH[2] - 1.5], 40)),
  upd: (t, i) => dpUpd(t, i, 'break'),
  figs: (t, i) => fig([DH[0] - 1.6, 0, DH[2] - .7], 'analyst', { mouth: t > wt(i, /falls/) ? 'o' : 'smile', blink: bl(t, 0), look: [5, 3], hR: [190, 160] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /home/) - .1, wt(i, /falls/) - .2, '🏠 AT HOME', '#232838', '#fff', 54) + stampAt(1400, 300, t, wt(i, /pieces/) - .05, 'CRACK!', '#e0303a', 100, -6),
  sfx: i => [{ k: 'thud', t: wt(i, /falls/) }, { k: 'impact', t: wt(i, /pieces/), g: .5 }] };
SHOT.d_paper = { set: 'FLEA', light: 'indoorWarm',
  cam: i => mv(cm([DH[0] + .5, 2.2, DH[2] + .5], [DH[0] - .1, 1.3, DH[2] - 1.4], 38), cm([DH[0] + .3, 2, DH[2] + .1], [DH[0] - .1, 1.32, DH[2] - 1.4], 34)),
  upd: (t, i) => dpUpd(t, i, 'paper'),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /folded/) - .1, nextStart(i), '📄 HIDDEN BEHIND THE PICTURE', '#232838', '#fff', 54) + bigText(1450, 380, t, wt(i, /paper/) + .2, nextStart(i), '?', 220, '#ffd166'),
  sfx: i => [{ k: 'swish', t: wt(i, /folded/) }, { k: 'pop', t: wt(i, /paper/) + .2 }] };
SHOT.d_decl = { set: 'FLEA', light: 'indoorWarm',
  cam: i => mv(cm([DH[0], 1.9, DH[2] + .4], [DH[0], 1.6, DH[2] - 1.2], 44), cm([DH[0], 1.85, DH[2] + .1], [DH[0], 1.62, DH[2] - 1.2], 40)),
  upd: (t, i) => dpUpd(t, i, 'decl'),
  ui: (t, i) => pillAt(960, 120, t, wt(i, /declaration/i) - .1, nextStart(i), '📜 THE DECLARATION OF INDEPENDENCE', '#232838', '#fff', 52) +
    stampAt(1500, 360, t, wt(i, /souvenir/) - .05, '❌ SOUVENIR', '#e0303a', 70, 6, wt(i, /first/) - .1) + stampAt(1500, 380, t, wt(i, /first/) - .05, 'JULY 1776', '#35a862', 100, -6),
  sfx: i => [{ k: 'shimmer', t: Lt(i).start + .2 }, { k: 'error', t: wt(i, /souvenir/), g: .4 }, { k: 'impact', t: wt(i, /first/) }] };
SHOT.d_rare = { set: 'FLEA', light: 'indoorWarm',
  cam: i => mv(cm([DH[0] + 2.2, 2.4, DH[2] + 2.6], [DH[0], 1.6, DH[2] - 1.2], 46), cm([DH[0] + 1.6, 2.2, DH[2] + 2], [DH[0], 1.6, DH[2] - 1.2], 44)),
  upd: (t, i) => dpUpd(t, i, 'decl'),
  figs: (t, i) => fig([DH[0] - 1.4, 0, DH[2] - .4], 'analyst', { mouth: 'o', blink: bl(t, 0), look: [4, 2], sweat: true }),
  ui: (t, i) => { const a = wt(i, /dozen/) - .2; if (t < a) return ''; let g = ''; for (let k = 0; k < 24; k++) g += `<span style="display:inline-block;transform:scale(${pop(t, a + k * .04)})">📜</span>`;
    return `<div style="position:absolute;left:1150px;top:230px;width:620px;font-size:70px;line-height:1.1;z-index:2200">${g}</div>` + pillAt(1460, 120, t, a, nextStart(i), 'ONLY ~2 DOZEN KNOWN', '#ffd166', OL, 46) },
  sfx: i => [{ k: 'pop', t: wt(i, /dozen/) }, { k: 'pop', t: wt(i, /dozen/) + .4 }, { k: 'ding', t: wt(i, /exist/) }] };
SHOT.d_sold = { set: 'AUC', light: 'indoorWarm',
  cam: i => mv(...CAM_POD),
  upd: (t, i) => aucUpd(t, i, 1),
  figs: (t, i) => auctioneer(t, i),
  ui: (t, i) => pillAt(960, 170, t, Lt(i).start + .1, nextStart(i), '🔨 AUCTION · 1991', '#232838', '#fff', 54) + screenPrice(t, wt(i, /auction/) - .1, nextStart(i), `$${(lerp(4, 2420000, ez(cl(t, wt(i, /auction/), wt(i, /dollars/)))) / 1e6).toFixed(2)}M`) +
    stampAt(1450, 470, t, wt(i, /dollars/), 'SOLD!', '#e0303a', 110, -8),
  sfx: i => [{ k: 'impact', t: wt(i, /dollars/) }, { k: 'cash', t: wt(i, /dollars/) + .2 }] };
SHOT.d_resold = { set: 'AUC', light: 'indoorWarm',
  cam: i => mv(...CAM_AUD),
  upd: (t, i) => aucUpd(t, i, 1),
  figs: (t, i) => audience(t, i, 1),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /nine/) - .1, nextStart(i), '📅 2000', '#232838', '#fff', 54) +
    counter(960, 300, t, wt(i, /time/) - .1, nextStart(i), wt(i, /time/), wt(i, /million/), 2.42, 8.14, v => '$' + v.toFixed(2) + ' MILLION', '#35a862', '#fff', 84) + bigText(960, 470, t, wt(i, /million/) + .2, nextStart(i), '$4 ➜ $8,140,000', 80, '#ffd166'),
  sfx: i => [{ k: 'tick', t: wt(i, /time/) }, { k: 'impact', t: wt(i, /million/) }, { k: 'cash', t: wt(i, /million/) + .2 }] };
