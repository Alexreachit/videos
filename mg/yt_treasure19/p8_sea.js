// ===================== Set SEA: Karibik 1708 (Seeschlacht) + Wrack in 600 m Tiefe + Ostsee-Wrack =====================
const SX = 2500, SD = [SX, -60, -100], SB = [SX + 70, -60, -100];
LOOK.diver = { sw: '#2a2a33', swd: '#1e1e28', pa: '#2a2a33', hat: `<circle cx="100" cy="96" r="70" fill="#9fd3f055" stroke="${OL}" stroke-width="7"/><rect x="58" y="70" width="84" height="40" rx="18" fill="#bfe6ff88" stroke="${OL}" stroke-width="5"/><rect x="150" y="60" width="22" height="70" rx="8" fill="#f2b21c" stroke="${OL}" stroke-width="5"/>` };
function galleonGeo(hull, sail, flag, sails = true) { const G2 = [at(G.box(9, 2.2, 2.8, hull, { base: true }), [0, -.6, 0]), at(G.box(2.6, 1.6, 2.6, hull, { base: true }), [-3.6, 1.6, 0]), at(G.box(1.8, .9, 2.4, hull, { base: true }), [3.8, 1.6, 0]),
  at(G.cyl(1.4, .1, 2.6, 4, hull, { rot: PI / 4 }), [4.6, -.6, 0], [0, 0, -PI / 2]), at(G.box(9.2, .2, 3, '#e8c060', { base: true }), [0, 1.5, 0]),
  ...[-1.4, 0, 1.4].map(x => at(G.box(.4, .3, .1, '#1b1b22', { base: true }), [x, .6, 1.42])), ...[-1.4, 0, 1.4].map(x => at(G.box(.4, .3, .1, '#1b1b22', { base: true }), [x, .6, -1.42]))];
  [[-2, 8], [.8, 9.5], [3, 7]].forEach(([x, h]) => { G2.push(at(G.cyl(.12, .1, h, 8, '#5a3a26'), [x, 1.6, 0])); if (sails) [.5, .78].forEach((f, k) => G2.push(at(G.box(.12, h * .26, 2.8 - k * .7, sail, { base: true }), [x + .2, 1.6 + h * (f - .18), 0]))); G2.push(at(G.box(.04, .6, 1, flag, { base: true }), [x, 1.6 + h, .5])) });
  return merge(G2) }
(function sea() {
  const S = 'SEA';
  seaGrid(S, SX, 0, 240, 2.4, '#2a7ab0', { pos: [0, -.3, 0] });
  // Kueste in der Ferne (Cartagena)
  mk(S, merge([at(G.ico(30, 2, '#5f8a48', .1, 3, .15), [SX + 60, -3, -80]), at(G.ico(24, 2, '#6a9a50', .1, 4, .18), [SX + 20, -3, -95])]).smooth(), { outline: false, cast: false });
  // Meeresgrund
  mk(S, G.ico(60, 3, '#c9b48a', .02, 2, .08).smooth(), { pos: [SX + 30, SD[1] - 4.2, SD[2]], outline: false });
  const R = []; for (let k = 0; k < 30; k++) R.push(at(G.ico(.6 + G.hash(k) * 1.4, 1, '#8a8a7a', .3, k), [SX - 20 + G.hash(k, 1) * 40, SD[1], SD[2] - 14 + G.hash(k, 2) * 30]));
  for (let k = 0; k < 22; k++) { const cx = -16 + G.hash(k, 5) * 32, cz = -10 + G.hash(k, 6) * 18; if (Math.abs(cx) < 7 && cz > -6) continue; R.push(at(G.cyl(.08, .04, 1 + G.hash(k, 3) * 1.6, 5, ['#d65a7a', '#e8962a', '#7ad0a0'][k % 3]), [SX + cx, SD[1], SD[2] + cz])) }
  mk(S, merge(R), { outline: false });
  // Wrack San Jose: Galeone ohne Segel, schraeg im Sand
  mk(S, galleonGeo('#6a5038', '#000', '#5a4a3a', false), { pos: [SD[0] - 1, SD[1] + .2, SD[2] - 3], rot: [.22, .35, .18] });
  // Ostsee-Wrack (Dampfer, grau)
  mk(S, merge([at(G.box(12, 3, 3.2, '#7a808c', { base: true }), [0, 0, 0]), at(G.box(3, 2, 2.6, '#5a5e68', { base: true }), [1, 3, 0]), at(G.cyl(.6, .6, 2.6, 10, '#3a3e48'), [1, 5, 0])]), { pos: [SB[0], SB[1] - .4, SB[2] - 2], rot: [.2, -.3, .15] });
})();
const SJ = mk('SEA', galleonGeo('#7a4a2a', '#f4ecd8', '#e8c040'), { pos: [SX, 0, 0] });
const BR = [0, 1].map(k => mk('SEA', galleonGeo('#3a3a44', '#ecece4', '#c03030'), { pos: [SX - 30, 0, 18 + k * 8] }));
const SMOKE = [...Array(8)].map((_, k) => mk('SEA', G.ico(1.4, 2, '#e8e4dc', .25, k), { pos: [0, 0, 0], alpha: .7, outline: false, cast: false, recv: false }));
const BOOM = mk('SEA', G.ico(3, 2, '#ffb030', .35, 3), { pos: [SX, 2, 0], emis: 1, outline: false, cast: false, alpha: .9 });
// Schatz am Grund: Kanonen, Kruege, Muenzhaufen
const CAN = (p, r) => at(merge([at(G.cyl(.32, .24, 2.6, 12, '#3a5a4a'), [0, 0, 0], [0, 0, -PI / 2]), at(G.ico(.36, 1, '#3a5a4a'), [0, 0, 0])]), p, r);
mk('SEA', merge([CAN([SD[0] + 2.4, SD[1] + .3, SD[2] + 1.2], [0, .6, 0]), CAN([SD[0] - 4.6, SD[1] + .3, SD[2] + 2], [0, -.9, 0]), CAN([SD[0] + 4.6, SD[1] + .3, SD[2] - 1.4], [0, 2.2, 0]),
  ...[...Array(9)].map((_, k) => at(merge([at(G.cyl(.2, .15, .6, 12, '#b08a5a'), [0, 0, 0]), at(G.ico(.24, 2, '#b08a5a', 0, 1, 1.1), [0, .2, 0])]), [SD[0] - 2 + (k % 3) * .8 + G.hash(k) * .5, SD[1] + .2, SD[2] + 2.6 + Math.floor(k / 3) * .7], [k % 2 ? PI / 2.3 : 0, k, 0]))]), {});
const COINS = mk('SEA', merge([...Array(60)].map((_, k) => at(G.cyl(.12, .12, .04, 10, k % 5 ? '#ffcc44' : '#d8dce4'), [SD[0] + .6 + G.hash(k) * 2 - 1, SD[1] + .05 + G.hash(k, 3) * .3 * (1 - Math.abs(G.hash(k) - .5)), SD[2] + 3.4 + G.hash(k, 2) * 1.6 - .8], [G.hash(k, 4) * 1.4, k, 0])).concat(
  [...Array(6)].map((_, k) => at(G.ico(.1, 1, '#35e08a'), [SD[0] + G.hash(k, 7) * 2, SD[1] + .12, SD[2] + 3 + G.hash(k, 8)])))), { emis: .35, spec: 1, outline: false });
const ROV = mk('SEA', merge([at(G.box(1.6, 1, 1.1, '#f2b21c', { base: true }), [0, 0, 0]), at(G.box(1.7, .25, 1.2, '#2a2a33', { base: true }), [0, -.2, 0]), at(G.cyl(.18, .18, .3, 10, '#2a2a33'), [-.6, .5, .55], [PI / 2, 0, 0]), at(G.cyl(.18, .18, .3, 10, '#2a2a33'), [.6, .5, .55], [PI / 2, 0, 0]),
  at(G.box(.12, .12, .8, '#9aa0ac'), [.5, -.15, .9])]), { pos: [SD[0], SD[1] + 3, SD[2] + 8] });
const ROVL = mk('SEA', merge([at(G.ico(.12, 1, '#fff6c0'), [-.6, .5, .72]), at(G.ico(.12, 1, '#fff6c0'), [.6, .5, .72])]), { parent: ROV, emis: 1, outline: false, cast: false });
const BEAM = mk('SEA', G.cyl(2.2, .15, 9, 18, '#fff6c0', { open: true }), { parent: ROV, pos: [0, .5, .7], rot: [-PI / 2 - .35, 0, 0], alpha: .14, emis: 1, outline: false, cast: false, recv: false });
const BUBS = [...Array(10)].map((_, k) => mk('SEA', G.ico(.08 + G.hash(k) * .08, 1, '#d8f0ff'), { alpha: .6, emis: .5, outline: false, cast: false, recv: false }));
const LOOT = [mk('SEA', merge([at(G.cyl(.32, .24, 2.6, 12, '#3a5a4a'), [0, 0, 0], [0, 0, -PI / 2])]), {}), mk('SEA', merge([at(G.cyl(.18, .12, .22, 14, '#f4f4f8'), [0, 0, 0]), at(G.cyl(.185, .185, .03, 14, '#3a6ad6'), [0, .14, 0])]), {}),
  mk('SEA', merge([0, 1, 2].map(k => at(G.cyl(.13, .13, .04, 10, '#ffcc44'), [k * .3 - .3, 0, 0], [.4, 0, 0]))), { emis: .3, spec: 1 })];
CHAP.push({ line: 'n1', n: 1, title: 'THE SAN JOSÉ GALLEON', year: '1708', place: '🇨🇴 Caribbean Sea' });
let SE_I0 = 999;
const rovAt = (t, a, b, t0, t1) => G.v.lerp(a, b, ei(cl((t - t0) / (t1 - t0), 0, 1)));
function bubbles(t, p) { BUBS.forEach((m, j) => { const u = (t * .5 + j / 10) % 1; m.vis = true; m.pos = [p[0] + Math.sin(j * 3 + t) * .4, p[1] + u * 5, p[2] + Math.cos(j * 2) * .4]; m.alpha = .6 * (1 - u) }) }
function seUpd(t, i) {
  const k = i - SE_I0, sh = SPEC(i).shot;
  BR.forEach(m => m.vis = false); SMOKE.forEach(m => m.vis = false); BOOM.vis = false; SJ.vis = true; SJ.rot = [0, 0, 0]; SJ.pos = [SX + (t - (Lt(SE_I0 + 1) ? Lt(SE_I0 + 1).start : 0)) * .6, 0, 0];
  LOOT.forEach(m => m.vis = false); BUBS.forEach(m => m.vis = false); ROV.vis = true; COINS.vis = true;
  if (sh == 's_attack' || sh == 's_sink') { BR.forEach((m, j) => { m.vis = true; m.pos = [SJ.pos[0] - 10 + j * 14, 0, -13 - j * 3]; m.rot = [0, -.25, 0] });
    SMOKE.forEach((m, j) => { const ft = Lt(i).start + .6 + j * .35, u = cl((t - ft) / 2.2, 0, 1); m.vis = t > ft; const b = BR[j % 2].pos; m.pos = [b[0] + 1 + u * 1.5, 1 + u * 1.2, b[2] + 1.6 + u * 2]; m.scl = [.4 + u, .4 + u, .4 + u]; m.alpha = .75 * (1 - u * .7) }) }
  if (sh == 's_sink') { const b = wt(i, /down/) - .6, u = ez(cl((t - b) / 3.2, 0, 1)); SJ.pos = [SJ.pos[0], -u * 5, 0]; SJ.rot = [u * .5, 0, -u * .35]; BOOM.vis = t > b - .2 && t < b + .9; BOOM.pos = X(SJ.pos, 0, 2, 0); const s = ez(cl((t - b + .2) / .5, 0, 1)) * 1.4; BOOM.scl = [s, s, s]; BOOM.alpha = .9 * (1 - cl((t - b - .3) / .6, 0, 1)) }
}
const deepCam = (dx, dy, dz, ax = 0, ay = 0, az = 0, f = 50) => cm([SD[0] + dx, SD[1] + dy, SD[2] + dz], [SD[0] + ax, SD[1] + ay, SD[2] + az], f);
SHOT.s_hook = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(9, 4.5, 14, -1, 1, -1, 50), deepCam(6, 3, 10, 0, .6, 1, 46)),
  upd: (t, i) => { seUpd(t, i); ROV.pos = rovAt(t, [SD[0] - 5, SD[1] + 4, SD[2] + 4], [SD[0] - 1.5, SD[1] + 2.6, SD[2] + 5], 0, nextStart(i)); ROV.rot = [0, .9, 0]; bubbles(t, X(ROV.pos, 0, .8, 0)) },
  ui: (t, i) => pillAt(960, 330, t, wt(i, /seventeen/) - .1, nextStart(i), '💰 ~$17 BILLION?', '#35a862', '#fff', 60),
  sfx: i => [{ k: 'air', t: .2, d: 1.5 }, { k: 'shimmer', t: wt(i, /gold/) }, { k: 'cash', t: wt(i, /dollars/) }] };
SHOT.s_hook2 = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(-3, 2, 7, .6, .3, 3, 46), deepCam(-1.6, 1.4, 5.4, .6, .2, 3.4, 42)),
  upd: (t, i) => { seUpd(t, i); ROV.pos = rovAt(t, [SD[0] + 1.6, SD[1] + 2.4, SD[2] + 6.4], [SD[0] + 2.6, SD[1] + 2, SD[2] + 5.4], Lt(i).start, nextStart(i)); ROV.rot = [0, .5, 0]; bubbles(t, X(ROV.pos, 0, .8, 0)) },
  ui: (t, i) => pillAt(960, 930 - 120, t, wt(i, /found/) - .1, nextStart(i), '🔎 FOUND IN 2015', '#2a8fd6', '#fff', 56) + stampAt(1460, 330, t, wt(i, /still/) - .05, 'STILL DOWN THERE', '#e0303a', 70, 6),
  sfx: i => [{ k: 'blip', t: wt(i, /found/) }, { k: 'impact', t: wt(i, /still/), g: .5 }] };
SHOT.s_sea = { set: 'SEA', light: 'storm',
  cam: i => { SE_I0 = i; return mv(cm([SX - 30, 14, 40], [SX, 3, 0], 50), cm([SX - 18, 8, 28], [SX + 2, 3, 0], 48)) },
  upd: seUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📍 OFF CARTAGENA, COLOMBIA', '#232838', '#fff', 44),
  sfx: i => [{ k: 'wave', t: Lt(i).start + .2 }, { k: 'gull', t: Lt(i).start + 1.8 }] };
SHOT.s_sail = { set: 'SEA', light: 'storm',
  cam: i => mv(cm([SX + 10, 4, 12], [SX + 1, 3.6, 0], 50), cm([SX + 12, 3, 9], [SX + 3, 3.6, 0], 48)),
  upd: seUpd,
  ui: (t, i) => { const C = [[/gold/, '🥇 GOLD', '#ffd166', OL], [/silver/, '🥈 SILVER', '#d8dce4', OL], [/emeralds/, '💚 EMERALDS', '#35a862', '#fff']];
    return labelAt(X(SJ.pos, 0, 12, 0), PILL('🇪🇸 SAN JOSÉ', '#232838', '#fff', 44), t, wt(i, /san/i) - .1, nextStart(i)) + C.map(([re, tx, bg, col], k) => pillAt(560 + k * 400, 930 - 120, t, wt(i, re) - .1, nextStart(i), tx, bg, col, 48)).join('') },
  sfx: i => [{ k: 'pop', t: wt(i, /san/i) }, { k: 'coin', t: wt(i, /gold/) }, { k: 'coin', t: wt(i, /silver/) }, { k: 'shimmer', t: wt(i, /emeralds/) }] };
SHOT.s_attack = { set: 'SEA', light: 'storm',
  cam: i => mv(cm([SX - 6, 6, 34], [SX - 2, 3, 8], 54), cm([SX - 2, 5, 30], [SX, 3, 8], 52)),
  upd: seUpd,
  ui: (t, i) => pillAt(960, 170, t, wt(i, /british/i) - .1, nextStart(i), '🇬🇧 BRITISH WARSHIPS', '#c03030', '#fff', 54),
  sfx: i => [0, 1, 2, 3, 4].map(j => ({ k: 'impact', t: Lt(i).start + .6 + j * .35, g: .45 })) };
SHOT.s_sink = { set: 'SEA', light: 'storm',
  cam: i => mv(cm([SX + 2, 6, 26], [SX + 2, 1, 0], 52), cm([SX + 4, 4, 22], [SX + 3, 0, 0], 52)),
  upd: seUpd,
  ui: (t, i) => { const a = wt(i, /six/) - .1, b = wt(i, /eleven/) - .1; let h = pillAt(960, 170, t, wt(i, /hour/) - .1, wt(i, /down/) + .6, '⏱️ ~1 HOUR OF FIGHTING', '#232838', '#fff', 50);
    if (t > a) h += counter(960, 170, t, a, nextStart(i), a, wt(i, /board/), 0, 600, v => '👥 ~' + Math.round(v) + ' ON BOARD', '#232838', '#fff', 60);
    h += stampAt(960, 340, t, b, 'ONLY ~11 SURVIVE', '#e0303a', 84, -4); return h },
  sfx: i => [{ k: 'impact', t: wt(i, /down/) - .6 }, { k: 'splash', t: wt(i, /down/) }, { k: 'impact', t: wt(i, /eleven/), g: .5 }] };
SHOT.s_lost = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(-14, 8, 16, 0, 0, 0, 52), deepCam(-10, 5, 12, 0, 0, 0, 50)),
  upd: (t, i) => { seUpd(t, i); ROV.vis = false },
  ui: (t, i) => counter(960, 170, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, nextStart(i) - .3, 1708, 2015, v => '⏳ ' + Math.round(v), '#232838', '#fff', 70),
  sfx: i => [{ k: 'air', t: Lt(i).start + .2, d: 1.5 }, { k: 'tick', t: Lt(i).start + .3 }] };
SHOT.s_found = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(8, 8, 12, 0, 1, 0, 52), deepCam(5, 4, 9, 0, .6, 1, 48)),
  upd: (t, i) => { seUpd(t, i); ROV.pos = rovAt(t, [SD[0] + 6, SD[1] + 10, SD[2] + 6], [SD[0] + 2, SD[1] + 3, SD[2] + 5], Lt(i).start, nextStart(i)); ROV.rot = [0, .4, 0]; bubbles(t, X(ROV.pos, 0, .8, 0)) },
  ui: (t, i) => { let h = pillAt(960, 170, t, wt(i, /colombia/i) - .1, nextStart(i), '🇨🇴 2015: COLOMBIA FINDS IT', '#2a8fd6', '#fff', 52);
    const a = wt(i, /two/) - .1; if (t > a) { const d = Math.round(2000 * ez(cl((t - a) / 1.4, 0, 1)));
      h += `<div style="position:absolute;left:1700px;top:200px;transform:scale(${pop(t, a)});width:130px;height:520px;background:linear-gradient(#2a8fd6,#051a33);border:8px solid ${OL};border-radius:20px;z-index:2200"><div style="position:absolute;left:-14px;right:-14px;top:${20 + d / 2000 * 440}px;height:14px;background:#ffd166;border:4px solid ${OL};border-radius:8px"></div></div>` + pillAt(1500, 760 - 40, t, a, nextStart(i), '⬇️ ' + d.toLocaleString('en-US') + ' FT', '#232838', '#fff', 50) }
    return h },
  sfx: i => [{ k: 'blip', t: wt(i, /found/) }, { k: 'air', t: wt(i, /two/), d: 1.2 }] };
SHOT.s_coins = { set: 'SEA', light: 'deep',
  cam: i => [{ t0: Lt(i).start, ...mv(deepCam(-6, 2.6, 8, -2, .4, 0, 46), deepCam(-5, 2.2, 7, -2, .4, 0, 44)) }, { t0: wt(i, /jars/) - .15, ...mv(deepCam(-1, 1.4, 5.6, -1.2, .2, 3, 40), deepCam(-.6, 1.2, 5.2, -1, .2, 3, 38)) },
    { t0: wt(i, /coins/) - .15, ...mv(deepCam(1.6, 1.4, 5.8, .6, .1, 3.4, 40), deepCam(1.2, 1, 5, .6, .1, 3.4, 36)) }],
  upd: (t, i) => { seUpd(t, i); ROV.vis = false },
  ui: (t, i) => { const a = wt(i, /some/i) - .1; return counter(960, 170, t, a, nextStart(i), a, wt(i, /coins/, 1) + 1.4, 0, 11, v => '🪙 UP TO ' + Math.round(v) + ' MILLION COINS?', '#ffd166', OL, 60) },
  sfx: i => [{ k: 'thud', t: Lt(i).start + .2, g: .4 }, { k: 'pop', t: wt(i, /jars/) }, { k: 'coin', t: wt(i, /coins/) }, { k: 'cash', t: nextStart(i) - .6 }] };
SHOT.s_owners = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(0, 6, 13, 0, 0, 1, 54), deepCam(0, 5, 11, 0, 0, 1, 52)),
  upd: (t, i) => { seUpd(t, i); ROV.vis = false },
  ui: (t, i) => { const C4 = [[/colombia/i, '🇨🇴', 'COLOMBIA', 'IT\'S OURS'], [/spain/i, '🇪🇸', 'SPAIN', 'OURS TOO'], [/investors/, '🇺🇸', 'US INVESTORS', 'WANT $10B'], [/bolivia/i, '🇧🇴', 'QHARA QHARA', 'OUR ANCESTORS\'']]; let h = '';
    C4.forEach(([re, fl, who, say], k) => { const a = wt(i, re) - .1; if (t > a) h += `<div style="position:absolute;left:${250 + k * 473}px;top:250px;transform:translate(-50%,0) rotate(${(k % 2 ? 3 : -3)}deg) scale(${pop(t, a)});width:410px;padding:18px 0 22px;background:#fff;border:8px solid ${OL};border-radius:18px;text-align:center;box-shadow:0 12px 0 #0006;z-index:2200"><div style="font-size:90px;line-height:1.1">${fl}</div><div style="font:900 40px IB;color:${OL}">${who}</div><div style="font:700 32px P;color:#c0303a">${say}</div></div>` });
    return pillAt(960, 140, t, Lt(i).start + .1, nextStart(i), '⚖️ WHO OWNS IT?', '#232838', '#fff', 56) + h },
  sfx: i => [/colombia/i, /spain/i, /investors/, /bolivia/i].map(re => ({ k: 'pop', t: wt(i, re) })) };
SHOT.s_raise = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(5, 3.6, 10, 1, 2.6, 3.4, 48), deepCam(4.4, 4, 9, 1, 3.2, 3.4, 46)),
  upd: (t, i) => { seUpd(t, i); const a = Lt(i).start + 1, u = ez(cl((t - a) / (nextStart(i) - a), 0, 1)); ROV.pos = [SD[0] + 1, SD[1] + 1.6 + u * 2.6, SD[2] + 3.6]; ROV.rot = [0, -.5, 0]; bubbles(t, X(ROV.pos, 0, .8, 0));
    const R3 = [/cannon/, /cup/, /coins/]; LOOT.forEach((m, j) => { const s = wt(i, R3[j]) - .2; m.vis = t > s; m.pos = X(ROV.pos, -.6 + j * .6, -.5 - (j == 0 ? .3 : 0), .3) }) },
  ui: (t, i) => { const P3 = [[/cannon/, '💣 CANNON'], [/cup/, '☕ PORCELAIN CUP'], [/coins/, '🪙 3 COINS']]; return pillAt(960, 160, t, wt(i, /2025/) - .1, nextStart(i), '🤖 2025: FIRST OBJECTS RAISED', '#2a8fd6', '#fff', 52) + P3.map(([re, tx], k) => pillAt(400 + k * 560, 930 - 120, t, wt(i, re) - .1, nextStart(i), tx, '#232838', '#fff', 46)).join('') },
  sfx: i => [{ k: 'ding', t: wt(i, /cannon/) }, { k: 'ding', t: wt(i, /cup/) }, { k: 'coin', t: wt(i, /coins/) }] };
SHOT.s_secret = { set: 'SEA', light: 'deep',
  cam: i => mv(deepCam(2, 3, 9, 0, 0, 2, 46), deepCam(-4, 18, 30, 0, 0, 0, 56)),
  upd: (t, i) => { seUpd(t, i); ROV.vis = false },
  ui: (t, i) => bigText(960, 190, t, wt(i, /rest/) - .1, nextStart(i), 'STILL ON THE SEAFLOOR', 86, '#ffd166', -2) + stampAt(960, 400, t, wt(i, /secret/) - .05, '📍 TOP SECRET', '#e0303a', 96, 5),
  sfx: i => [{ k: 'air', t: Lt(i).start + .2, d: 2 }, { k: 'impact', t: wt(i, /secret/), g: .5 }] };
// Bernsteinzimmer-Kapitel: Taucher am Ostsee-Wrack
SHOT.a_divers = { set: 'SEA', light: 'deep',
  cam: i => mv(cm([SB[0] + 6, SB[1] + 3, SB[2] + 10], [SB[0], SB[1] + 1.4, SB[2] - 1], 50), cm([SB[0] + 4, SB[1] + 2.6, SB[2] + 8], [SB[0], SB[1] + 1.4, SB[2] - 1], 48)),
  upd: (t, i) => { ROV.vis = false; COINS.vis = false; bubbles(t, [SB[0] - 1.6, SB[1] + 2.4, SB[2] + 2.6]) },
  figs: (t, i) => fig([SB[0] - 1.6, SB[1] + .8 + .2 * Math.sin(t * 1.5), SB[2] + 2.6], 'diver', { mouth: 'hmm', blink: bl(t, 0), look: [4, 2], hR: [200, 120 + 20 * Math.sin(t * 2)], legL: .3 * Math.sin(t * 3), legR: -.3 * Math.sin(t * 3) }) +
    fig([SB[0] + 2, SB[1] + 1.2 + .2 * Math.sin(t * 1.3 + 1), SB[2] + 2], 'diver', { mouth: 'sad', blink: bl(t, 1), look: [-4, 3], hR: [190, 80], legL: .3 * Math.sin(t * 3 + 1), legR: -.3 * Math.sin(t * 3 + 1) }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /sunken/) - .1, nextStart(i), '🤿 2020: A SUNKEN GERMAN SHIP', '#2a8fd6', '#fff', 50) + stampAt(960, 380, t, wt(i, /amber/) - .05, 'NO AMBER', '#e0303a', 110, -5),
  sfx: i => [{ k: 'air', t: Lt(i).start + .2, d: 1.2 }, { k: 'error', t: wt(i, /amber/) }] };
