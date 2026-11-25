// ===================== Set FEN: Santa Fe + Rocky Mountains (Kiste mit Gold) =====================
const FX = 1000, FT = [FX, 0, 0], FS = [FX, 0, -90], FM = [FX, 0, 200];   // Stadt / Arbeitszimmer / Berge
LOOK.dealer = { sw: '#e8e0d0', swd: '#cfc6b4', pa: '#4a5a7a', hat: `<path d="M46,44 Q46,6 100,4 Q154,6 154,44Z" fill="#d8c8a8" stroke="${OL}" stroke-width="6"/><path d="M14,46 Q100,30 186,46 Q186,58 100,56 Q14,58 14,46Z" fill="#c8b490" stroke="${OL}" stroke-width="5"/><rect x="48" y="32" width="104" height="10" fill="#6a4a2e"/>`, mid: `<path d="M80,154 L100,170 L120,154" stroke="#2a8fd6" stroke-width="7" fill="none"/>` };
LOOK.student = { sw: '#2a5ab0', swd: '#204890', pa: '#3a3f55', hat: HAT.beanie };
LOOK.hiker = { sw: '#d64545', swd: '#b43636', pa: '#4a5a3a', hat: HAT.cap };
LOOK.hiker2 = { sw: '#f2b21c', swd: '#d49a10', pa: '#3a3f55', hat: HAT.beanie };
(function fenn() {
  const S = 'FEN';
  // Santa Fe: Wueste + Adobe-Haeuser
  mk(S, G.box(160, .4, 80, '#d8b888', { base: true }), { pos: [FX, -.4, 0], outline: false, cast: false });
  const A = []; for (let k = 0; k < 16; k++) { const x = FX - 26 + (k % 8) * 7 + G.hash(k) * 2, z = -6 - Math.floor(k / 8) * 9 - G.hash(k, 2) * 2, hh = 2.6 + (k % 3) * 1.2;
    A.push(at(G.box(5, hh, 4.6, ['#d9a676', '#c98f5f', '#e0b488'][k % 3], { base: true }), [x, 0, z]), at(G.box(5.2, .3, 4.8, '#b97a4a', { base: true }), [x, hh, z]), at(G.box(1, 1.4, .1, '#4a7ab0', { base: true }), [x - 1, .2, z + 2.32]), at(G.box(.9, .9, .1, '#2a3a5a', { base: true }), [x + 1.2, 1.4, z + 2.32]));
    for (let j = 0; j < 4; j++) A.push(at(G.cyl(.1, .1, .8, 6, '#6a4a2e'), [x - 1.8 + j * 1.2, hh - .4, z + 2.3], [PI / 2, 0, 0])) }
  mk(S, merge(A).vary(.03, 4));
  const C = []; for (let k = 0; k < 10; k++) { const x = FX - 30 + k * 6.6, z = 6 + (k % 3) * 2; C.push(at(G.cyl(.3, .3, 1.6, 8, '#4f8a3c'), [x, 0, z]), at(G.cyl(.16, .16, .7, 6, '#4f8a3c'), [x + .4, .8, z], [0, 0, -1])) }
  mk(S, merge(C));
  // Arbeitszimmer
  mk(S, merge([at(G.box(12, .3, 9, '#7a5a3a', { base: true }), [FS[0], -.3, FS[2]]), at(G.box(12, 5, .3, '#e0c8a0', { base: true }), [FS[0], 0, FS[2] - 4.5]),
    at(G.box(.3, 5, 9, '#d4b890', { base: true }), [FS[0] - 6, 0, FS[2]]), at(G.box(3.4, .14, 1.6, '#6b4226', { base: true }), [FS[0], 1.0, FS[2] - 1.5]), at(G.box(3.2, 1.0, 1.4, '#5a3a20', { base: true }), [FS[0], 0, FS[2] - 1.5]),
    at(G.box(5, .1, 3, '#a03a2a', { base: true }), [FS[0], 0, FS[2] + 1]), at(G.box(1.6, 1.2, .1, '#2a4a6a', { base: true }), [FS[0] - 3, 2.2, FS[2] - 4.34]), at(G.box(1.6, 1.2, .1, '#8a3a2a', { base: true }), [FS[0] + 2.6, 2.4, FS[2] - 4.34])]), { outline: false });
  // Rocky Mountains: Gipfel mit Schnee, Wald, Fluss
  mk(S, G.box(260, .4, 140, '#5f8a48', { base: true }), { pos: [FM[0], -.4, FM[2]], outline: false, cast: false });
  const P = []; [[-40, -40, 22, 30], [0, -52, 28, 40], [42, -44, 24, 32], [-80, -60, 26, 36], [82, -62, 30, 42]].forEach(([x, z, r, h], k) => { P.push(at(G.cyl(r, 0, h, 7, k % 2 ? '#7a7f8c' : '#8a8f9c', { rot: k }), [FM[0] + x, -1, FM[2] + z]), at(G.cyl(r * .32, 0, h * .32, 7, '#f4f6fb', { rot: k }), [FM[0] + x, h * .68 - 1, FM[2] + z])) });
  mk(S, merge(P), { cast: false });
  const T = []; for (let k = 0; k < 80; k++) { const x = FM[0] - 50 + (k % 20) * 5 + G.hash(k) * 3, z = FM[2] - 8 - Math.floor(k / 20) * 5 - G.hash(k, 2) * 3; T.push(...tree(x, z, .9 + G.hash(k, 3) * .6, k % 3 ? '#2a5030' : '#356038')) }
  mk(S, merge(T));
  // Felsen am Fluss
  mk(S, merge([...Array(14)].map((_, k) => at(G.ico(.5 + G.hash(k) * .9, 1, '#8a8478', .25, k), [FM[0] - 14 + k * 2.2, 0, FM[2] + 4.2 + (k % 2) * 3.2]))).smooth());
})();
const FRIVER = seaGrid('FEN', FM[0], FM[2] + 5.8, 90, 1, '#3a9ad6', { wave: .08, pos: [0, .08, 0] }, 2.6);
// Kiste (Bronze) mit Deckel + Goldinhalt
const FCH = mk('FEN', merge([at(G.box(.9, .5, .7, '#a8743a', { base: true }), [0, 0, 0]), at(G.box(.94, .08, .74, '#7a5226', { base: true }), [0, .22, 0])]), { pos: [FS[0] - .6, 1.14, FS[2] - 1.5], spec: .6 });
const FLID = mk('FEN', merge([at(G.box(.94, .14, .74, '#b8844a', { base: true }), [0, 0, .37]), at(G.box(.12, .16, .14, '#ffd166', { base: true }), [0, -.06, .74])]), { parent: FCH, pos: [0, .5, -.37], spec: .6 });
const FGOLD = mk('FEN', merge([...Array(16)].map((_, k) => at(G.cyl(.1, .1, .03, 12, k % 4 ? '#ffcc44' : '#e84a6a'), [-.3 + (k % 4) * .2, .52 + Math.floor(k / 8) * .05, -.2 + (Math.floor(k / 4) % 2) * .3], [.3 * (k % 3), 0, .2]))), { parent: FCH, emis: .3, spec: 1, outline: false });
CHAP.push({ line: 'n4', n: 4, title: "FORREST FENN'S TREASURE", year: '2010', place: '🇺🇸 Rocky Mountains' });
let FE_I0 = 0;
function feUpd(t, i) {
  const k = i - FE_I0; FCH.vis = k >= 1 && k <= 2 || k == 6; FGOLD.vis = FCH.vis;
  if (k == 1) { FCH.pos = [FS[0] - .6, 1.14, FS[2] - 1.5]; FCH.rot = [0, .3, 0]; FLID.rot = [-1.6, 0, 0] }
  if (k == 2) { FCH.pos = [FM[0] + 3, 0, FM[2] + 1]; FCH.rot = [0, -.4, 0]; FLID.rot = [0, 0, 0] }
  if (k == 6) { FCH.pos = [FM[0] - 1, 0, FM[2] + 8]; FCH.rot = [0, .5, 0]; FLID.rot = [-1.4 * ez(cl((t - wt(i, /found/)) / .6, 0, 1)), 0, 0] }
}
SHOT.f_town = { set: 'FEN', light: 'day',
  cam: i => { FE_I0 = i; return mv(cm([FX + 14, 7, 22], [FX - 2, 2, -8], 50), cm([FX + 8, 5, 16], [FX - 2, 2, -8], 48)) },
  upd: feUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📍 SANTA FE, NEW MEXICO', '#232838', '#fff', 44),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .3, d: 1.2 }] };
SHOT.f_chest = { set: 'FEN', light: 'indoorWarm',
  cam: i => cut2(i, /gold/, cm([FS[0] + 3, 2.2, FS[2] + 4.4], [FS[0] - .3, 1.4, FS[2] - 1.5], 48), cm([FS[0] + 2.4, 2.1, FS[2] + 3.6], [FS[0] - .3, 1.4, FS[2] - 1.5], 46),
    cm([FS[0] - .5, 2.9, FS[2] - .3], [FS[0] - .6, 1.4, FS[2] - 1.5], 40), cm([FS[0] - .5, 2.7, FS[2] - .5], [FS[0] - .6, 1.4, FS[2] - 1.5], 38)),
  upd: feUpd,
  figs: (t, i) => t > wt(i, /gold/) - .15 ? '' : fig([FS[0] + 1.3, 0, FS[2] - .5], 'dealer', { mouth: 'grin', talk: 0, blink: bl(t, 0), look: [-5, 3], hR: [150, 150] }),
  ui: (t, i) => labelAt([FS[0] + 1.3, 2.2, FS[2] - .5], PILL('🎨 ART DEALER, AGE 80', '#232838', '#fff', 38), t, wt(i, /dealer/) - .1, wt(i, /gold/) - .2) +
    pillAt(960, 180, t, wt(i, /million/) - .1, nextStart(i), '💰 $1 MILLION+', '#35a862', '#fff', 72),
  sfx: i => [{ k: 'coin', t: wt(i, /gold/) }, { k: 'shimmer', t: wt(i, /gems/) }, { k: 'cash', t: wt(i, /dollars/) }] };
SHOT.f_hide = { set: 'FEN', light: 'dusk',
  cam: i => mv(cm([FM[0] + 16, 8, FM[2] + 22], [FM[0], 8, FM[2] - 30], 52), cm([FM[0] + 8, 3, FM[2] + 9], [FM[0] + 3, .6, FM[2] + 1], 46)),
  upd: feUpd,
  figs: (t, i) => fig([FM[0] + 4.6, 0, FM[2] + 1.8], 'dealer', { mouth: 'grin', blink: bl(t, 0), look: [-5, 4], hR: [170, 200], lean: .15 }),
  ui: (t, i) => bigText(960, 190, t, wt(i, /rocky/i) - .1, nextStart(i), '🏔️ SOMEWHERE IN THE ROCKIES', 80),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: 1.4 }, { k: 'thud', t: nextStart(i) - .6, g: .4 }] };
SHOT.f_poem = { set: 'FEN', light: 'indoorWarm',
  cam: i => mv(cm([FS[0] + .5, 2.6, FS[2] + 2], [FS[0], 1.1, FS[2] - 1.5], 44), cm([FS[0] + .3, 2.4, FS[2] + 1.2], [FS[0], 1.1, FS[2] - 1.5], 42)),
  upd: feUpd,
  ui: (t, i) => { const a = Lt(i).start + .1; if (t < a) return ''; let ln = ''; const n = Math.round(24 * ez(cl((t - a) / 2.4, 0, 1)));
    for (let k = 0; k < n; k++) ln += `<div style="height:9px;margin:5px 0;width:${60 + 30 * G.hash(k)}%;background:#5a4a3a;border-radius:5px${[2, 5, 8, 11, 13, 16, 18, 20, 22].includes(k) && t > wt(i, /nine/) ? ';background:#e0a010;box-shadow:0 0 10px #ffd166' : ''}"></div>`;
    return `<div style="position:absolute;left:960px;top:150px;transform:translate(-50%,0) rotate(-2deg) scale(${pop(t, a)});width:420px;padding:28px 34px;background:#f6ecd2;border:9px solid ${OL};border-radius:10px;box-shadow:0 16px 0 #0005;z-index:2200">
      <div style="font:900 40px IB;color:${OL};text-align:center;margin-bottom:8px">📜 THE POEM</div>${ln}</div>` + pillAt(1460, 300, t, wt(i, /twenty/) - .1, nextStart(i), '24 LINES', '#232838', '#fff', 46) + pillAt(1460, 420, t, wt(i, /nine/) - .1, nextStart(i), '🔑 9 CLUES', '#ffd166', OL, 50) },
  sfx: i => [{ k: 'paper', t: Lt(i).start + .1 }, { k: 'ding', t: wt(i, /nine/) }] };
SHOT.f_search = { set: 'FEN', light: 'day',
  cam: i => mv(cm([FM[0] + 10, 4, FM[2] + 18], [FM[0], 1.2, FM[2] + 5], 52), cm([FM[0] + 6, 3.2, FM[2] + 15], [FM[0] - 1, 1.2, FM[2] + 5], 50)),
  upd: feUpd,
  figs: (t, i) => { let h = ''; const L4 = [['hiker', [-6, 0, 2], PROP.shovel, 0], ['hiker2', [-2, -.4, 6], PROP.detector, 1], ['student', [2, 0, 2.6], PROP.map, 0], ['hunter', [5, -.4, 6.4], '', 1]];
    L4.forEach(([who, p, pr, wade], k) => h += fig([FM[0] + p[0] + Math.sin(t * .6 + k) * .4, p[1], FM[2] + p[2]], who, Object.assign(walk(t + k, 7), { mouth: 'grin', blink: bl(t, k), look: [k % 2 ? -4 : 4, 3], prop: pr, hR: pr ? [180, 150] : [200, 100], legsOff: !!wade })));
    return h },
  ui: (t, i) => counter(960, 170, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, wt(i, /looking/), 0, 1000, v => '🔎 ' + (v > 990 ? 'THOUSANDS' : Math.round(v)) + ' OF SEARCHERS', '#232838', '#fff', 60),
  sfx: i => [{ k: 'splash', t: wt(i, /waded/) }, { k: 'thud', t: wt(i, /dug/), g: .4 }] };
SHOT.f_danger = { set: 'FEN', light: 'dusk',
  cam: i => mv(cm([FM[0] + 2, 2, FM[2] + 13], [FM[0] - 2, 1, FM[2] + 5], 48), cm([FM[0] + 1, 1.6, FM[2] + 11], [FM[0] - 2, 1, FM[2] + 5], 46)),
  upd: feUpd,
  figs: (t, i) => fig([FM[0] - 3, -.5, FM[2] + 6], 'hiker', { mouth: 'o', blink: bl(t, 0), look: [0, -4], sweat: true, legsOff: true, hR: [200, 60], hL: [0, 60], tilt: .1 * Math.sin(t * 3) }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /dangerous/) - .1, nextStart(i), '⚠️ DANGEROUS', '#e0303a', '#fff', 56) + counter(960, 300, t, wt(i, /five/) - .1, nextStart(i), wt(i, /five/), wt(i, /died/), 0, 5, v => 'AT LEAST ' + Math.round(v) + ' DIED', '#232838', '#fff', 64),
  sfx: i => [{ k: 'splash', t: Lt(i).start + .4 }, { k: 'impact', t: wt(i, /died/), g: .5 }] };
SHOT.f_found = { set: 'FEN', light: 'day',
  cam: i => cut2(i, /found/, cm([FM[0] + 4, 2, FM[2] + 15], [FM[0] - 1, 1, FM[2] + 7], 48), cm([FM[0] + 3, 2, FM[2] + 14], [FM[0] - 1, 1, FM[2] + 7], 46),
    cm([FM[0] + .6, 1.4, FM[2] + 10.6], [FM[0] - 1, .4, FM[2] + 8], 42), cm([FM[0] + .4, 1.3, FM[2] + 10.2], [FM[0] - 1, .4, FM[2] + 8], 40)),
  upd: feUpd,
  figs: (t, i) => { const f = wt(i, /found/) - .15; return t < f ? fig([FM[0] - .2, 0, FM[2] + 9], 'student', Object.assign(walk(t, 7), { mouth: 'smile', blink: bl(t, 0), look: [-3, 3], prop: PROP.map, hR: [170, 130] })) : fig([FM[0] + .2, 0, FM[2] + 8.6], 'student', { mouth: 'grin', talk: .6, blink: bl(t, 0), look: [-3, 4], hR: [210, 60], hL: [-10, 60] }) },
  ui: (t, i) => counter(960, 160, t, Lt(i).start + .1, wt(i, /found/), Lt(i).start + .2, wt(i, /2020/), 2010, 2020, v => '📅 ' + Math.round(v), '#232838', '#fff', 64) + labelAt([FM[0] + .2, 2.1, FM[2] + 8.6], PILL('🩺 MEDICAL STUDENT, 32', '#2a5ab0', '#fff', 38), t, wt(i, /student/) - .1, nextStart(i)) + stampAt(480, 330, t, wt(i, /found/), 'FOUND!', '#35a862', 110, -6),
  sfx: i => [{ k: 'tick', t: Lt(i).start + .3 }, { k: 'impact', t: wt(i, /found/), g: .6 }, { k: 'shimmer', t: wt(i, /found/) + .3 }] };
SHOT.f_wyoming = { set: 'FEN', light: 'dusk',
  cam: i => mv(cm([FM[0] + 22, 14, FM[2] + 30], [FM[0], 6, FM[2] - 10], 52), cm([FM[0] + 18, 10, FM[2] + 26], [FM[0], 5, FM[2] - 10], 50)),
  upd: feUpd,
  ui: (t, i) => bigText(960, 200, t, wt(i, /wyoming/i) - .1, nextStart(i), '📍 WYOMING', 110, '#ffd166', -3) + pillAt(960, 360, t, wt(i, /confirmed/) - .1, nextStart(i), '✅ CONFIRMED BY FENN', '#35a862', '#fff', 48) +
    pillAt(960, 470, t, wt(i, /ninety/) - .1, nextStart(i), '🕊️ FENN DIED IN SEPT 2020, AGE 90', '#232838', '#fff', 44),
  sfx: i => [{ k: 'impact', t: wt(i, /wyoming/i), g: .5 }, { k: 'ding', t: wt(i, /confirmed/) }, { k: 'bell', t: wt(i, /ninety/) }] };
