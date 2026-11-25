// ===================== Set AMB: Katharinenpalast + Bernsteinzimmer + Koenigsberg =====================
const AX2 = 2000, AP = [AX2, 0, 0], AR = [AX2, 0, -90], AK = [AX2, 0, 90];
LOOK.king = { sw: '#2a3a6a', swd: '#203058', pa: '#e8e0d0', hat: CROWN, mid: MID.buttons };
LOOK.peter = { sw: '#2a6a3a', swd: '#20582e', pa: '#e8e0d0', hat: CROWN, mid: MID.buttons };
(function amber() {
  const S = 'AMB';
  // Palast aussen: lange blau-weisse Fassade, goldene Kuppeln
  mk(S, G.box(200, .4, 120, '#7aa85a', { base: true }), { pos: [AX2, -.4, 0], outline: false, cast: false });
  const F = [at(G.box(60, 9, 6, '#4a8ad6', { base: true }), [AX2, 0, -12]), at(G.box(60.6, .6, 6.4, '#f2f2f8', { base: true }), [AX2, 9, -12]), at(G.box(60.6, .5, 6.4, '#f2f2f8', { base: true }), [AX2, 4.2, -12])];
  for (let k = -14; k <= 14; k++) { F.push(at(G.box(.5, 9, .5, '#f2f2f8', { base: true }), [AX2 + k * 2.1, 0, -8.8])); if (k % 2) F.push(at(G.box(1.1, 2, .1, '#e8f4ff', { base: true }), [AX2 + k * 2.1 + 1.05, 1.2, -8.92]), at(G.box(1.1, 2, .1, '#e8f4ff', { base: true }), [AX2 + k * 2.1 + 1.05, 5.6, -8.92])) }
  [-24, -12, 0, 12, 24].forEach(x => F.push(at(G.cyl(1.4, 1.4, 1.6, 14, '#f2f2f8'), [AX2 + x, 9.5, -12])));
  mk(S, merge(F).vary(.02, 2));
  mk(S, merge([-24, -12, 0, 12, 24].map(x => at(G.ico(1.6, 2, '#ffcc44', 0, 1, 1.1), [AX2 + x, 11.8, -12])).concat([-24, -12, 0, 12, 24].map(x => at(G.cyl(.4, 0, 2.4, 10, '#ffcc44'), [AX2 + x, 13, -12])))), { spec: 1, emis: .15 });
  // Bernsteinzimmer innen (Waende = Textur)
  mk(S, merge([at(G.box(16, .3, 12, '#6a3a1a', { base: true, top: '#8a5228' }), [AR[0], -.3, AR[2]]), at(G.box(16, .5, 12, '#f2e2b8', { base: true }), [AR[0], 7, AR[2]])]), { outline: false });
  mk(S, merge([at(G.ico(.45, 2, '#fff2c0'), [0, 0, 0]), ...[0, 1, 2, 3, 4, 5].map(k => at(G.ico(.18, 1, '#fff2c0'), [Math.cos(k) * .8, -.3, Math.sin(k) * .8]))]), { pos: [AR[0], 6.3, AR[2]], emis: 1, outline: false, cast: false });
  mk(S, G.box(16, 7, .2, '#cfc2a8', { base: true }), { pos: [AR[0], 0, AR[2] - 6.2], outline: false });
  // Koenigsberg: Burg aus Backstein
  mk(S, G.box(200, .4, 80, '#6a7a5a', { base: true }), { pos: [AK[0], -.4, AK[2]], outline: false, cast: false });
  mk(S, merge([at(G.box(26, 8, 8, '#a8583a', { base: true }), [AK[0], 0, AK[2] - 10]), at(G.box(5, 18, 5, '#9a4e32', { base: true }), [AK[0] + 8, 0, AK[2] - 10]), at(G.cyl(3.4, 0, 5, 4, '#3a4a5a', { rot: PI / 4 }), [AK[0] + 8, 18, AK[2] - 10]),
    ...[...Array(12)].map((_, k) => at(G.box(1, 1, 8.4, '#a8583a', { base: true }), [AK[0] - 12 + k * 2.2, 8, AK[2] - 10]))]).vary(.04, 6));
  const HH = []; for (let k = 0; k < 12; k++) { const x = AK[0] - 30 + k * 5.2, z = AK[2] - 26 - (k % 2) * 4; HH.push(at(G.box(4, 4 + (k % 3), 4, ['#c8b098', '#b89878', '#d8c0a0'][k % 3], { base: true }), [x, 0, z]), at(G.cyl(3, .05, 2, 4, '#7a3a2a', { rot: PI / 4 }), [x, 4 + (k % 3), z])) }
  mk(S, merge(HH));
})();
function amberTex() { return tex(1024, 512, (x, wd, ht) => {
  x.fillStyle = '#8a4a14'; x.fillRect(0, 0, wd, ht);
  for (let k = 0; k < 900; k++) { const px = G.hash(k) * wd, py = G.hash(k, 2) * ht, r = 8 + G.hash(k, 3) * 22; const c = ['#e8962a', '#f0b040', '#c86a18', '#ffcc66', '#d47a1c'][k % 5];
    x.fillStyle = c; x.beginPath(); for (let j = 0; j < 6; j++) { const a = j / 6 * 6.283 + k; x.lineTo(px + Math.cos(a) * r * (.7 + G.hash(k, j) * .5), py + Math.sin(a) * r * (.7 + G.hash(k, j + 9) * .5)) } x.fill() }
  x.strokeStyle = '#ffd166'; x.lineWidth = 14; for (let c = 0; c < 4; c++) { x.strokeRect(20 + c * 252, 30, 220, ht - 60); x.strokeStyle = '#ffd166' }
  x.fillStyle = '#ffe8a0'; for (let c = 0; c < 4; c++) { x.beginPath(); x.ellipse(130 + c * 252, 160, 50, 64, 0, 0, 7); x.fill(); x.fillStyle = '#c8e8ff'; x.beginPath(); x.ellipse(130 + c * 252, 160, 38, 52, 0, 0, 7); x.fill(); x.fillStyle = '#ffe8a0' }
}) }
const AWALLS = [[AR[0], 3.5, AR[2] - 6, 0], [AR[0] - 8, 3.5, AR[2], PI / 2], [AR[0] + 8, 3.5, AR[2], -PI / 2]].map(([x, y, z, r]) => texPlane('AMB', r ? 12 : 16, 7, amberTex, { pos: [x, y, z], rot: [0, r, 0], spec: .5 }));
// 12 Paneele, die abgenommen werden (Rueckwand vorn)
const APAN = [...Array(6)].map((_, k) => texPlane('AMB', 2.4, 3, amberTex, { pos: [AR[0] - 6 + k * 2.4, 2, AR[2] - 5.9] }));
const ACRATES = [...Array(9)].map((_, k) => mk('AMB', merge([at(G.box(1.6, 1.1, 1.1, '#a07a4a', { base: true }), [0, 0, 0]), at(G.box(1.64, .12, 1.14, '#7a5a32', { base: true }), [0, .55, 0])]), { pos: [0, 0, 0] }));
const ATRUCK = mk('AMB', merge([at(G.box(6, 2.8, 2.6, '#4e5440', { base: true }), [-1, .8, 0]), at(G.box(2.2, 2.0, 2.4, '#40463a', { base: true }), [3.2, .8, 0]), at(G.box(1.8, .8, .1, '#9fd3f0', { base: true }), [3.3, 2.0, 1.22]),
  ...[[-3, 1.2], [1, 1.2], [3.2, 1.2], [-3, -1.5], [1, -1.5], [3.2, -1.5]].map(([x, z]) => at(G.cyl(.5, .5, .3, 12, '#1b1b22'), [x, .5, z], [PI / 2, 0, 0]))]), { pos: [AK[0] - 20, 0, AK[2] + 2] });
const AFIRE = [...Array(7)].map((_, k) => mk('AMB', G.ico(1.2 + G.hash(k) * 1.2, 2, k % 2 ? '#ff8a2a' : '#ffcc44', .3, k), { pos: [AK[0] - 10 + k * 3.4, 8 + G.hash(k, 4) * 3, AK[2] - 9], emis: 1, outline: false, cast: false }));
const ASMOKE = [...Array(6)].map((_, k) => mk('AMB', G.ico(2.4, 2, '#3a3a44', .2, k), { pos: [AK[0] - 8 + k * 3.2, 14, AK[2] - 10], alpha: .5, outline: false, cast: false, recv: false }));
CHAP.push({ line: 'n2', n: 2, title: 'THE AMBER ROOM', year: '1941', place: '🇷🇺 near St. Petersburg' });
let AM_I0 = 0;
function amUpd(t, i) {
  const k = i - AM_I0;
  APAN.forEach((m, j) => { m.vis = k <= 3 || k == 8; m.pos = [AR[0] - 6 + j * 2.4, 2, AR[2] - 5.9]; m.rot = [0, 0, 0];
    if (k == 3) { const a = wt(i, /apart/) - 1.2 + j * .35, u = ez(cl((t - a) / .8, 0, 1)); m.pos = [AR[0] - 6 + j * 2.4, 2 - u * .6, AR[2] - 5.9 + u * 3]; m.rot = [-u * 1.3, 0, 0]; m.vis = u < .98 } });
  AWALLS[0].vis = k < 3 || k == 8 || (k == 3 && t < wt(i, /apart/) - 1.2); ACRATES.forEach((m, j) => { m.vis = false });
  if (k == 3) ACRATES.forEach((m, j) => { m.vis = t > wt(i, /apart/) - .6 + j * .2; m.pos = [AR[0] - 4.8 + (j % 3) * 1.8, 0, AR[2] + 1 + Math.floor(j / 3) * 1.4] });
  if (k == 4) { const u = ez(cl((t - wt(i, /ship/)) / 3, 0, 1)); ATRUCK.pos = [lerp(AK[0] - 34, AK[0] - 6, u), 0, AK[2] + 2]; ACRATES.forEach((m, j) => { m.vis = true; m.pos = X(ATRUCK.pos, -3.2 + (j % 3) * 1.6, 1.6 + Math.floor(j / 3) * .5 * 0, j < 3 ? -.6 : j < 6 ? .6 : 0); m.pos[1] = 1.6 + Math.floor(j / 6) * 1.1 }) }
  ATRUCK.vis = k == 4;
  AFIRE.forEach((m, j) => { m.vis = (k == 5 && t > wt(i, /bombed/) - .2) || k == 6; m.scl = [1 + .15 * Math.sin(t * 8 + j), 1 + .25 * Math.sin(t * 6 + j * 2), 1] });
  ASMOKE.forEach((m, j) => { m.vis = (k == 5 && t > wt(i, /ruins/) - .4) || k == 6; m.pos = [AK[0] - 8 + j * 3.2, 14 + ((t * .8 + j) % 5), AK[2] - 10] });
}
SHOT.a_palace = { set: 'AMB', light: 'day',
  cam: i => { AM_I0 = i; return mv(cm([AX2 + 30, 6, 30], [AX2, 6, -12], 52), cm([AX2 + 16, 4, 18], [AX2, 6, -12], 50)) },
  upd: amUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📍 CATHERINE PALACE · 1941', '#232838', '#fff', 44),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .3, d: 1.2 }, { k: 'bell', t: Lt(i).start + 1.5 }] };
SHOT.a_room = { set: 'AMB', light: 'amber',
  cam: i => mv(cm([AR[0] + 5, 2.4, AR[2] + 5.4], [AR[0] - 2, 2.8, AR[2] - 5], 58), cm([AR[0] - 3, 2.2, AR[2] + 4.6], [AR[0] + 3, 3, AR[2] - 5], 58)),
  upd: amUpd,
  figs: (t, i) => fig([AR[0] + .6, 0, AR[2] + .6], 'sam', { hat: '', mouth: 'o', blink: bl(t, 0), look: [0, -5], hR: [200, 100], hL: [0, 100] }),
  ui: (t, i) => counter(960, 170, t, wt(i, /six/) - .1, nextStart(i), wt(i, /six/), wt(i, /tons/), 0, 6, v => '🟧 ' + Math.round(v) + ' TONS OF AMBER', '#e8962a', '#fff', 66) + bigText(960, 320, t, wt(i, /eighth/) - .1, nextStart(i), '"8TH WONDER OF THE WORLD"', 70, '#ffd166', -3),
  sfx: i => [{ k: 'shimmer', t: wt(i, /amber/) }, { k: 'ding', t: wt(i, /eighth/) }] };
SHOT.a_gift = { set: 'AMB', light: 'amber',
  cam: i => mv(cm([AR[0] + 1, 2.2, AR[2] + 6], [AR[0], 1.8, AR[2] - 2], 52), cm([AR[0] + .6, 2.1, AR[2] + 5], [AR[0], 1.8, AR[2] - 2], 50)),
  upd: amUpd,
  figs: (t, i) => fig([AR[0] - 1.8, 0, AR[2]], 'king', { mouth: 'smile', blink: bl(t, 0), look: [5, 0], hR: [210, 140] }) + fig([AR[0] + 1.8, 0, AR[2]], 'peter', { mouth: 'grin', blink: bl(t, 1), look: [-5, 0], hL: [-10, 140] }),
  ui: (t, i) => labelAt([AR[0] - 1.8, 2.1, AR[2]], PILL('KING OF PRUSSIA', '#2a3a6a', '#fff', 36), t, wt(i, /prussia/i) - .1, nextStart(i)) + labelAt([AR[0] + 1.8, 2.1, AR[2]], PILL('PETER THE GREAT', '#2a6a3a', '#fff', 36), t, wt(i, /peter/i) - .1, nextStart(i)) + pillAt(960, 170, t, wt(i, /gift/) - .1, nextStart(i), '🎁 A ROYAL GIFT · 1716', '#232838', '#fff', 52),
  sfx: i => [{ k: 'pop', t: wt(i, /prussia/i) }, { k: 'pop', t: wt(i, /peter/i) }] };
SHOT.a_tear = { set: 'AMB', light: 'indoorDark',
  cam: i => mv(cm([AR[0] + 2, 2.6, AR[2] + 6], [AR[0] - 1, 1.8, AR[2] - 5], 56), cm([AR[0] + 1.4, 2.4, AR[2] + 4.6], [AR[0] - 1, 1.8, AR[2] - 5], 54)),
  upd: amUpd,
  figs: (t, i) => { let h = ''; [-4, -1, 2].forEach((dx, k) => h += fig([AR[0] + dx, 0, AR[2] - 3.6], 'soldier', { mouth: 'hmm', blink: bl(t, k), look: [0, -4], hR: [190, 40 + 20 * Math.sin(t * 5 + k)], hL: [10, 40 + 20 * Math.sin(t * 5 + k + 1)] })); return h },
  ui: (t, i) => pillAt(960, 170, t, wt(i, /invades/) - .1, nextStart(i), '⚔️ JUNE 1941: GERMANY INVADES', '#232838', '#fff', 50) + counter(960, 300, t, wt(i, /thirty/) - .1, nextStart(i), wt(i, /thirty/), wt(i, /hours/) + .8, 0, 36, v => '⏱️ ' + Math.round(v) + ' HOURS', '#e0303a', '#fff', 70),
  sfx: i => [{ k: 'impact', t: wt(i, /invades/), g: .5 }, ...[0, 1, 2, 3, 4, 5].map(j => ({ k: 'hammer', t: wt(i, /apart/) - 1.2 + j * .35 }))] };
SHOT.a_crates = { set: 'AMB', light: 'dusk',
  cam: i => mv(cm([AK[0] - 6, 4, AK[2] + 16], [AK[0] - 6, 3, AK[2] - 4], 52), cm([AK[0] - 2, 4.4, AK[2] + 18], [AK[0] - 2, 5, AK[2] - 8], 52)),
  upd: amUpd,
  ui: (t, i) => counter(960, 170, t, wt(i, /twenty/) - .1, nextStart(i), wt(i, /twenty/), wt(i, /crates/), 0, 27, v => '📦 ' + Math.round(v) + ' CRATES', '#a07a4a', '#fff', 64) + pillAt(960, 930 - 110, t, wt(i, /castle/) - .1, nextStart(i), '🏰 KÖNIGSBERG CASTLE', '#232838', '#fff', 46),
  sfx: i => [{ k: 'thud', t: Lt(i).start + .3, g: .5 }, { k: 'whoosh', t: wt(i, /ship/), d: 1.4 }] };
SHOT.a_bomb = { set: 'AMB', light: 'night',
  cam: i => mv(cm([AK[0] + 4, 6, AK[2] + 26], [AK[0], 8, AK[2] - 10], 54), cm([AK[0] + 2, 5, AK[2] + 20], [AK[0], 8, AK[2] - 10], 52)),
  upd: amUpd,
  ui: (t, i) => stampAt(960, 300, t, wt(i, /cold/) - .05, 'TRAIL LOST', '#e0303a', 100, -5),
  sfx: i => [{ k: 'impact', t: wt(i, /bombed/) }, { k: 'impact', t: wt(i, /bombed/) + .5, g: .5 }, { k: 'thud', t: wt(i, /ruins/), g: .6 }, { k: 'air', t: wt(i, /cold/), d: 1 }] };
SHOT.a_theories = { set: 'AMB', light: 'night',
  cam: i => mv(cm([AK[0] - 8, 3, AK[2] + 18], [AK[0], 7, AK[2] - 10], 54), cm([AK[0] - 5, 3, AK[2] + 15], [AK[0], 7, AK[2] - 10], 52)),
  upd: amUpd,
  ui: (t, i) => { const C3 = [[/destroyed/, '💥', 'DESTROYED?'], [/hidden/, '🕳️', 'HIDDEN?'], [/sunk/, '🌊', 'SUNK?']]; let h = '';
    C3.forEach(([re, ic, tx], k) => { const a = wt(i, re) - .1; if (t > a) h += `<div style="position:absolute;left:${420 + k * 540}px;top:330px;transform:translate(-50%,-50%) rotate(${(k - 1) * 4}deg) scale(${pop(t, a)});width:400px;padding:26px 0;background:#f6ecd2;border:9px solid ${OL};border-radius:18px;text-align:center;box-shadow:0 14px 0 #0006;z-index:2200"><div style="font-size:110px">${ic}</div><div style="font:900 54px IB;color:${OL}">${tx}</div></div>` });
    return h + bigText(960, 640 - 40, t, wt(i, /nobody/i) - .1, nextStart(i), 'NOBODY KNOWS', 90, '#ffd166', -2) },
  sfx: i => [{ k: 'pop', t: wt(i, /destroyed/) }, { k: 'pop', t: wt(i, /hidden/) }, { k: 'pop', t: wt(i, /sunk/) }] };
SHOT.a_copy = { set: 'AMB', light: 'amber',
  cam: i => mv(cm([AR[0] - 4, 2.6, AR[2] + 5], [AR[0] + 2, 3, AR[2] - 5], 58), cm([AR[0] + 4, 2.4, AR[2] + 5], [AR[0] - 2, 3, AR[2] - 5], 58)),
  upd: amUpd,
  ui: (t, i) => counter(700, 170, t, wt(i, /twenty/) - .1, nextStart(i), wt(i, /twenty/), wt(i, /years/), 0, 25, v => '🛠️ ' + Math.round(v) + ' YEARS', '#232838', '#fff', 56) + counter(1240, 170, t, wt(i, /eleven/) - .1, nextStart(i), wt(i, /eleven/), wt(i, /dollars/), 0, 11, v => '$' + Math.round(v) + ' MILLION', '#35a862', '#fff', 56) +
    pillAt(960, 300, t, wt(i, /copy/) - .1, nextStart(i), 'REPLICA · 2003', '#e8962a', '#fff', 50) + stampAt(960, 470, t, wt(i, /never/) - .05, 'ORIGINAL: NEVER FOUND', '#e0303a', 74, -4),
  sfx: i => [{ k: 'tick', t: wt(i, /twenty/) }, { k: 'cash', t: wt(i, /dollars/) }, { k: 'impact', t: wt(i, /never/), g: .5 }] };
