// ===================== Set NAZ: Polen, Berge bei Walbrzych (Gleis, Tunnel, Schatzsucher, Bagger) =====================
const NX = 0, NT = [NX + 6, 0, -14];   // Tunnelportal
PROP.shovel = `<g transform="rotate(20)"><rect x="-5" y="-70" width="10" height="96" rx="4" fill="#a0703a" stroke="${OL}" stroke-width="4"/><path d="M-18,24 L18,24 L14,58 Q0,70 -14,58Z" fill="#9aa0ac" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/></g>`;
PROP.detector = `<g transform="rotate(30)"><rect x="-4" y="-40" width="8" height="110" rx="4" fill="#3a3a44" stroke="${OL}" stroke-width="4"/><ellipse cx="0" cy="76" rx="30" ry="10" fill="#ffd166" stroke="${OL}" stroke-width="5"/><rect x="-14" y="-30" width="28" height="18" rx="4" fill="#2fa36b" stroke="${OL}" stroke-width="4"/></g>`;
PROP.tablet = `<g transform="translate(-34,-30)"><rect x="0" y="0" width="68" height="50" rx="6" fill="#232838" stroke="${OL}" stroke-width="5"/><rect x="6" y="6" width="56" height="38" rx="3" fill="#35e08a"/><path d="M10,30 L24,18 L36,28 L56,12" stroke="#0a3a20" stroke-width="4" fill="none"/></g>`;
PROP.map = `<g transform="translate(-40,-30) rotate(-6)"><rect x="0" y="0" width="80" height="56" fill="#f3e2b8" stroke="${OL}" stroke-width="5"/><path d="M10,40 Q30,10 50,30 T74,16" stroke="#c0303a" stroke-width="4" stroke-dasharray="6 5" fill="none"/><text x="62" y="46" font-family="IB" font-weight="900" font-size="20" fill="#c0303a">X</text></g>`;
LOOK.hunter = { sw: '#4f7a3c', swd: '#3e632e', pa: '#5a4a3a', hat: HAT.beanie };
LOOK.hunter2 = { sw: '#c96a2a', swd: '#a8561f', pa: '#3a3f55', hat: HAT.cap };
LOOK.sci = { sw: '#f2f2ea', swd: '#d6d6cc', pa: '#3a3f55' };
LOOK.soldier = { sw: '#5a6048', swd: '#484d3a', pa: '#4a4e3a', hat: `<path d="M34,52 Q34,0 100,0 Q166,0 166,52 L176,60 L24,60Z" fill="#4e5440" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/>` };
(function naz() {
  const S = 'NAZ';
  mk(S, G.box(300, .4, 300, '#5a8a44', { base: true }), { pos: [NX, -.4, 0], outline: false, cast: false });
  // Berge (gruene Kuppen + Wald)
  const M = []; [[-30, -40, 22], [10, -74, 26], [44, -38, 20], [-60, -60, 30], [70, -64, 34]].forEach(([x, z, r], k) => M.push(at(G.ico(r, 3, k % 2 ? '#4a7a3c' : '#557f42', .06, k, .55), [NX + x, -2, z])));
  mk(S, merge(M).smooth(), { cast: false, outline: false });
  // Huegel mit Tunnel direkt hinter dem Gleisende
  const T = []; for (let k = 0; k < 70; k++) { const a = k * 2.4, r = 16 + G.hash(k) * 40, x = NX + Math.cos(a) * r, z = -24 + Math.sin(a) * r * .5 - 10; if (Math.abs(x - NX - 6) < 5 && z > -20) continue; T.push(...tree(x, z, .9 + G.hash(k, 2) * .6, k % 3 ? '#2f5a34' : '#3a6a3a')) }
  mk(S, merge(T), { cast: true });
  // Gleis (Damm) Richtung Tunnel
  const R = [at(G.box(4, .4, 60, '#7a7466', { base: true }), [NT[0], 0, NT[2] + 26]), at(G.box(.12, .14, 60, '#a8acb8', { base: true }), [NT[0] - .72, .4, NT[2] + 26]), at(G.box(.12, .14, 60, '#a8acb8', { base: true }), [NT[0] + .72, .4, NT[2] + 26])];
  for (let z = -4; z < 56; z += 1.1) R.push(at(G.box(2.2, .1, .3, '#4a3a2a', { base: true }), [NT[0], .34, NT[2] + z]));
  mk(S, merge(R), { outline: false, cast: false });
  // Tunnelportal (Steinbogen) + schwarzes Loch
  mk(S, merge([at(G.box(8, 6.5, 2, '#8a8478', { base: true }), [NT[0], 0, NT[2] - 1]), at(G.box(8.6, .6, 2.2, '#77716a', { base: true }), [NT[0], 6.5, NT[2] - 1])]).vary(.05, 3));
  mk(S, merge([at(G.box(4.2, 4.2, .2, '#08080c', { base: true }), [NT[0], 0, NT[2] + .02]), at(G.cyl(2.1, 2.1, .2, 18, '#08080c'), [NT[0], 4.2, NT[2] + .02], [PI / 2, 0, 0])]), { outline: false, cast: false });
  // Stadt in der Ferne (Kleinstadt)
  const H2 = []; for (let k = 0; k < 14; k++) { const x = NX - 40 + k * 3.2, z = 20 + (k % 3) * 3; H2.push(at(G.box(2.6, 2.2 + (k % 4) * .6, 2.6, ['#e8d8b8', '#d8a878', '#c9b8a0', '#f0e0c8'][k % 4], { base: true }), [x, 0, z]), at(G.cyl(2, .05, 1.4, 4, '#b04a3a', { rot: PI / 4 }), [x, 2.2 + (k % 4) * .6, z])) }
  mk(S, merge(H2));
})();
// Zug (dunkel, Kisten mit Gold sichtbar auf offenem Wagen)
const NTRAIN = mk('NAZ', merge([at(G.box(2.6, 2.8, 9, '#3a3d44', { base: true }), [0, .4, 0]), at(G.cyl(.9, .9, 6, 14, '#2c2f36'), [0, 2.2, .5], [PI / 2, 0, 0]), at(G.cyl(.35, .4, 1.4, 10, '#2c2f36'), [0, 3.1, -2.6]),
  ...[-3, -1, 1, 3].map(z => at(G.cyl(.55, .55, 2.8, 12, '#1b1b22'), [-1.4, .55, z], [0, 0, PI / 2])),
  at(G.box(2.6, 1.2, 9, '#4a4e3a', { base: true }), [0, .4, 10]), ...[-3, -1, 1, 3].map(z => at(G.cyl(.5, .5, 2.8, 12, '#1b1b22'), [-1.4, .5, z + 10], [0, 0, PI / 2]))]), { pos: [NT[0], .4, 40] });
const NGOLD = mk('NAZ', merge([...Array(8)].map((_, k) => at(G.box(.9, .4, .5, '#ffcc44', { base: true }), [-.5 + (k % 2) * 1, 1.6 + Math.floor(k / 4) * .42, 7.5 + (Math.floor(k / 2) % 2) * 3]))), { parent: NTRAIN, emis: .35, spec: 1, outline: false });
// Radar-Hologramm (Tunnel + Zug) im Huegel
const NHILL = mk('NAZ', G.ico(14, 3, '#4f8040', .05, 9, .6).smooth(), { pos: [NT[0], -1, NT[2] - 10], outline: false });
const NHOLO_T = mk('NAZ', G.box(4.4, 4.4, 30, '#7fd0ff'), { pos: [NT[0], 2.2, NT[2] - 18], alpha: .4, emis: 1, outline: false, cast: false, recv: false });
const NHOLO_TR = mk('NAZ', merge([at(G.box(2.4, 2.6, 8, '#ffd166'), [0, 0, -5]), at(G.box(2.4, 2.0, 8, '#ffd166'), [0, -.3, 4])]), { pos: [NT[0], 1.8, NT[2] - 18], alpha: .4, emis: 1, outline: false, cast: false, recv: false });
// Bagger + 3 Gruben
const PITS = [[-6, 6], [0, 9], [6, 5]].map(([x, z]) => [NT[0] + 14 + x, 0, NT[2] + 14 + z]);
const PITM = PITS.map(p => mk('NAZ', merge([at(G.cyl(2, 1.6, .2, 18, '#3a2a1e'), [0, 0, 0]), at(G.ico(1.2, 2, '#6a4a2e', .2, 3, .5), [2.8, 0, 0]), at(G.ico(.9, 2, '#7a5634', .2, 4, .5), [2.6, 0, 1.4])]).smooth(), { pos: X(p, 0, .01, 0) }));
const EXC = mk('NAZ', merge([at(G.box(3.2, .9, 4, '#2a2a33', { base: true }), [0, 0, 0]), at(G.box(2.8, 1.6, 2.8, '#f2b21c', { base: true }), [0, .9, -.2]), at(G.box(1.3, 1.2, 1.3, '#f2b21c', { base: true }), [.6, 2.5, .3]), at(G.box(1.1, .9, .1, '#9fd3f0', { base: true }), [.6, 2.7, .96])]), { pos: X(PITS[1], -4.5, 0, -1), rot: [0, .6, 0] });
const EXA = mk('NAZ', merge([at(G.box(.5, .5, 4.4, '#f2b21c'), [0, 0, 2.2]), at(G.box(.45, .45, 3, '#e0a010'), [0, -1.4, 4.4], [.9, 0, 0]), at(G.box(1.1, .8, .9, '#3a3a44'), [0, -2.6, 5.4])]), { parent: EXC, pos: [-.6, 2.2, .6] });
CHAP.push({ line: 'n6', n: 6, title: 'THE NAZI GOLD TRAIN', year: '2015', place: '🇵🇱 Poland' });
let NA_I0 = 0;
function naUpd(t, i) {
  const k = i - NA_I0; NHILL.alpha = (k == 3 || (k == 5 && t > wt(i, /verdict/) - .15)) ? .3 : 1; NTRAIN.vis = k == 1; NHOLO_T.vis = k == 3 || k == 5; NHOLO_TR.vis = k == 3 || (k == 5 && t < wt(i, /train/) - .1);
  NHOLO_TR.alpha = k == 5 ? .4 * (1 - cl((t - wt(i, /^no\b/i)) * 2, 0, 1)) + .05 : .75 + .2 * Math.sin(t * 6);
  if (k == 1) { const a = Lt(i).start + 1.2, u = ez(cl((t - a) / 6, 0, 1)); NTRAIN.pos = [NT[0], .4, lerp(NT[2] + 20, NT[2] - 16, u)] }
  PITM.forEach((m, j) => m.vis = k == 7 || (k == 6 && t > Lt(i).start + 1 + j * 1.2)); PITM.forEach((m, j) => m.scl = [k == 6 ? ez(cl((t - Lt(i).start - 1 - j * 1.2) / .8, 0, 1)) : 1, 1, k == 6 ? ez(cl((t - Lt(i).start - 1 - j * 1.2) / .8, 0, 1)) : 1]);
  EXC.vis = k == 6 || k == 7; EXA.rot = [k == 6 ? .25 * Math.sin(t * 2.2) - .1 : -.2, 0, 0];
}
SHOT.n_hills = { set: 'NAZ', light: 'day',
  cam: i => { NA_I0 = i; return mv(cm([NX - 30, 16, 50], [NX, 4, -20], 50), cm([NX - 18, 10, 36], [NX + 4, 3, -14], 48)) },
  upd: naUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📍 WAŁBRZYCH, POLAND · AUGUST 2015', '#232838', '#fff', 44),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .3, d: 1.2 }] };
SHOT.n_legend = { set: 'NAZ', light: 'dusk',
  cam: i => mv(cm([NT[0] + 9, 4, NT[2] + 30], [NT[0], 2.4, NT[2] + 10], 48), cm([NT[0] + 7, 3.4, NT[2] + 14], [NT[0], 2.4, NT[2] - 2], 46)),
  upd: naUpd,
  ui: (t, i) => pillAt(960, 160, t, Lt(i).start + .1, nextStart(i), '📜 LEGEND · 1945', '#8a6a3a', '#fff', 50) + bigText(960, 330, t, wt(i, /never/) - .1, nextStart(i), 'NEVER SEEN AGAIN', 96, '#ffd166', -3),
  sfx: i => [{ k: 'thud', t: Lt(i).start + 1.4, g: .5 }, { k: 'whoosh', t: wt(i, /tunnel/), d: 1.2 }, { k: 'impact', t: wt(i, /never/), g: .5 }] };
SHOT.n_hunters = { set: 'NAZ', light: 'day',
  cam: i => mv(cm([NT[0] + 3, 2.4, NT[2] + 12], [NT[0] - .5, 1.6, NT[2] + 4], 46), cm([NT[0] + 2.4, 2.2, NT[2] + 10], [NT[0] - .5, 1.6, NT[2] + 4], 44)),
  upd: naUpd,
  figs: (t, i) => fig([NT[0] - 2.4, 0, NT[2] + 5.4], 'hunter', { mouth: 'grin', talk: tk(t, i) * .6, blink: bl(t, 0), look: [4, 0], prop: PROP.map, hR: [170, 130] }) + fig([NT[0] + 1.4, 0, NT[2] + 5], 'hunter2', { mouth: 'grin', blink: bl(t, 2), look: [-4, 0], hR: [205, 70], hL: [-10, 70] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /two/) - .1, nextStart(i), '🕵️ TWO TREASURE HUNTERS', '#232838', '#fff', 52) + stampAt(1460, 400, t, wt(i, /found/) - .05, '"WE FOUND IT!"', '#35a862', 70, 6),
  sfx: i => [{ k: 'pop', t: wt(i, /two/) }, { k: 'ding', t: wt(i, /found/) }] };
SHOT.n_radar = { set: 'NAZ', light: 'dusk',
  cam: i => mv(cm([NT[0] + 6, 28, NT[2] + 16], [NT[0], 0, NT[2] - 16], 50), cm([NT[0] + 4, 24, NT[2] + 12], [NT[0], 0, NT[2] - 17], 48)),
  upd: naUpd,
  ui: (t, i) => { const a = wt(i, /radar/) - .2; let h = '';
    if (t > a) h += `<div style="position:absolute;left:330px;top:250px;transform:translate(-50%,0) scale(${pop(t, a)});width:440px;height:300px;border:10px solid ${OL};border-radius:18px;background:repeating-linear-gradient(90deg,#3a2a6a 0 6px,#2a2a5a 6px 12px);overflow:hidden;box-shadow:0 14px 0 #0005;z-index:2200">
      <div style="position:absolute;left:70px;top:120px;width:300px;height:60px;border-radius:30px;background:radial-gradient(ellipse,#ffe14a 0%,#ff8a2a 60%,transparent 75%)"></div><div style="position:absolute;left:0;right:0;bottom:8px;text-align:center;font:900 34px IB;color:#fff">GROUND RADAR</div></div>`;
    h += counter(1450, 230, t, wt(i, /ninety/) - .2, nextStart(i), wt(i, /ninety/) - .1, wt(i, /percent/), 0, 99, v => Math.round(v) + '% SURE', '#35a862', '#fff', 84);
    return h },
  sfx: i => [{ k: 'blip', t: wt(i, /radar/) }, { k: 'tick', t: wt(i, /ninety/) }, { k: 'ding', t: wt(i, /percent/) }] };
SHOT.n_rush = { set: 'NAZ', light: 'day',
  cam: i => mv(cm([NX - 14, 5, 46], [NX - 10, 2, 24], 50), cm([NX - 10, 4, 42], [NX - 8, 2, 24], 48)),
  upd: naUpd,
  figs: (t, i) => { let h = ''; for (let k = 0; k < 7; k++) { const u = ((t - Lt(i).start) * .9 + k * 1.7) % 12; h += fig([NX - 20 + u * 1.6, 0, 31 + (k % 3) * 1.4], k % 2 ? 'hunter' : 'hunter2', Object.assign(walk(t + k, 8), { mouth: 'grin', blink: bl(t, k), look: [4, 0], prop: k % 3 == 0 ? PROP.detector : k % 3 == 1 ? PROP.shovel : '', hR: k % 3 < 2 ? [180, 160] : null })) } return h },
  ui: (t, i) => pillAt(960, 170, t, wt(i, /news/) - .1, nextStart(i), '📰 WORLD NEWS: NAZI GOLD TRAIN FOUND?', '#e0303a', '#fff', 52),
  sfx: i => [{ k: 'paper', t: wt(i, /news/) }, { k: 'whoosh', t: wt(i, /poured/), d: .8 }] };
SHOT.n_scan = { set: 'NAZ', light: 'dusk',
  cam: i => cut2(i, /verdict/, cm([NT[0] + 7, 3, NT[2] + 12], [NT[0] - 2, 2, NT[2] - 2], 48), cm([NT[0] + 6, 3, NT[2] + 10], [NT[0] - 2, 2, NT[2] - 2], 46), cm([NT[0] + 6, 28, NT[2] + 16], [NT[0], 0, NT[2] - 16], 50), cm([NT[0] + 4, 25, NT[2] + 13], [NT[0], 0, NT[2] - 17], 48)),
  upd: naUpd,
  figs: (t, i) => t > wt(i, /verdict/) - .15 ? '' : fig([NT[0] - 3, 0, NT[2] + 5], 'sci', { mouth: 'hmm', blink: bl(t, 0), look: [3, -2], prop: PROP.tablet, hR: [170, 120] }) + fig([NT[0] + 1, 0, NT[2] + 4.6], 'sci', { mouth: 'hmm', blink: bl(t, 1), look: [-3, -2], prop: PROP.detector, hR: [180, 160] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /krakow/i) - .1, wt(i, /verdict/) - .2, '🔬 SCIENTISTS FROM KRAKÓW', '#2a8fd6', '#fff', 52) + pillAt(700, 200, t, wt(i, /tunnel/) - .1, nextStart(i), '✅ TUNNEL? MAYBE', '#35a862', '#fff', 50) + stampAt(1300, 420, t, wt(i, /train/) - .05, 'NO TRAIN', '#e0303a', 110, -6),
  sfx: i => [{ k: 'blip', t: wt(i, /scanned/) }, { k: 'ding', t: wt(i, /tunnel/) }, { k: 'impact', t: wt(i, /train/) }] };
SHOT.n_dig = { set: 'NAZ', light: 'day',
  cam: i => mv(cm([PITS[1][0] + 4, 7, PITS[1][2] + 18], [PITS[1][0] - 2, 1.5, PITS[1][2]], 50), cm([PITS[1][0] + 2, 6, PITS[1][2] + 14], [PITS[1][0] - 2, 1.5, PITS[1][2]], 48)),
  upd: naUpd,
  figs: (t, i) => fig([PITS[0][0] + 2, 0, PITS[0][2] + 4], 'hunter', { mouth: 'grin', blink: bl(t, 0), look: [3, 0], prop: PROP.shovel, hR: [180, 150 + 20 * Math.sin(t * 5)] }) + fig([PITS[2][0] - 1, 0, PITS[2][2] + 4], 'hunter2', { mouth: 'grin', blink: bl(t, 1), look: [-3, 2], hR: [200, 110], hL: [0, 110] }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /excavators/) - .1, nextStart(i), '🚜 SUMMER 2016: THE BIG DIG', '#f2b21c', OL, 52),
  sfx: i => [{ k: 'thud', t: Lt(i).start + 1, g: .6 }, { k: 'thud', t: Lt(i).start + 2.2, g: .6 }, { k: 'thud', t: Lt(i).start + 3.4, g: .6 }] };
SHOT.n_holes = { set: 'NAZ', light: 'day',
  cam: i => mv(cm([PITS[1][0] + 1, 14, PITS[1][2] + 10], [PITS[1][0], 0, PITS[1][2]], 50), cm([PITS[1][0] + 1, 11, PITS[1][2] + 8], [PITS[1][0], 0, PITS[1][2]], 50)),
  upd: naUpd,
  figs: (t, i) => fig([PITS[1][0] + 2.6, 0, PITS[1][2] + 2.4], 'hunter', { mouth: 'sad', blink: bl(t, 0), look: [-3, 5], sweat: true, prop: PROP.shovel, hR: [170, 200] }),
  ui: (t, i) => stampAt(560, 300, t, wt(i, /train/) - .05, 'NO TRAIN', '#e0303a', 80, -8) + stampAt(1360, 300, t, wt(i, /tunnel/) - .05, 'NO TUNNEL', '#e0303a', 80, 6) +
    counter(960, 760 - 40, t, wt(i, /three/) - .1, nextStart(i), wt(i, /cost/), wt(i, /dollars/), 0, 37000, v => '💸 $' + Math.round(v).toLocaleString('en-US'), '#232838', '#fff', 70),
  sfx: i => [{ k: 'error', t: wt(i, /train/) }, { k: 'error', t: wt(i, /tunnel/) }, { k: 'cash', t: wt(i, /dollars/) }] };
