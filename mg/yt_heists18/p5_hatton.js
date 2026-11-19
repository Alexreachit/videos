// ===================== Set HAT: Hatton Garden 2015 (Strasse Nacht, Schacht, Tresor) =====================
const HX = 1200;
const HS = [HX, 0, 0], HV = [HX, -12, -6], HSH = [HX + 6, -12, -6];   // Strasse, Tresorraum (unter der Erde), Aufzugsschacht
(function hatton() {
  const S = 'HAT', BR = '#9a5a44', BR2 = '#86503c';
  mk(S, merge([at(G.box(120, .4, 40, '#3a3f55', { base: true }), [HX, -.4, 14]), at(G.box(120, .3, 4, '#6a6e80', { base: true }), [HX, 0, 1]), at(G.box(120, .3, 4, '#6a6e80', { base: true }), [HX, 0, 17])]), { outline: false });
  // Haeuserzeile (Backstein) mit Schaufenstern
  const F = [];
  for (let k = -5; k <= 5; k++) { const x = HX + k * 6.2, h = 11 + (k % 3) * 1.6, c = k % 2 ? BR : BR2; F.push(at(G.box(6, h, 2, c, { base: true }), [x, 0, -2]), at(G.box(6.2, .5, 2.3, '#d8d0c0', { base: true }), [x, h, -2]));
    for (let r = 0; r < 3; r++) F.push(at(G.box(1.2, 1.8, .2, '#2a2a3a', { base: true }), [x - 1.6, 4.2 + r * 2.6, -.95]), at(G.box(1.2, 1.8, .2, '#2a2a3a', { base: true }), [x + 1.6, 4.2 + r * 2.6, -.95])) }
  mk(S, merge(F).vary(.04, 11));
  const SH = []; for (let k = -5; k <= 5; k++) SH.push(at(G.box(4.6, 2.2, .2, '#ffe6a0', { base: true }), [HX + k * 6.2, .6, -.9]));
  mk(S, merge(SH), { emis: .45, outline: false, cast: false });
  // Laternen
  [-12, 0, 12].forEach(dx => { mk(S, merge([at(G.cyl(.1, .1, 4.6, 8, '#22252e'), [HX + dx, 0, 2.6])])); mk(S, G.box(.5, .5, .5, '#ffe7a0', { base: true }), { pos: [HX + dx, 4.6, 2.6], emis: 1, outline: false, cast: false }) });
  // Tresorraum: Wand mit Schliessfaechern
  mk(S, merge([at(G.box(14, .3, 10, '#5a5e6a', { base: true }), [HV[0], HV[1] - .3, HV[2]]), at(G.box(14, 5, .4, '#8a8e9a', { base: true }), [HV[0], HV[1], HV[2] - 5]),
    at(G.box(.6, 5, 10, '#9a9eaa', { base: true }), [HV[0] + 7, HV[1], HV[2]]), at(G.box(.4, 5, 10, '#8a8e9a', { base: true }), [HV[0] - 7, HV[1], HV[2]]), at(G.box(14, .3, 10, '#4a4e5a', { base: true }), [HV[0], HV[1] + 5, HV[2]])]), { outline: false });
  // Schacht (zwischen Strasse und Tresor)
  mk(S, merge([at(G.box(.3, 12, 3, '#5a5a62', { base: true }), [HSH[0] - 1.6, HSH[1], HSH[2]]), at(G.box(.3, 12, 3, '#5a5a62', { base: true }), [HSH[0] + 1.6, HSH[1], HSH[2]]), at(G.box(3.2, 12, .3, '#4a4a52', { base: true }), [HSH[0], HSH[1], HSH[2] - 1.5])]), { outline: false });
})();
function boxesTex() { return tex(1024, 512, x => { x.fillStyle = '#7a7e8a'; x.fillRect(0, 0, 1024, 512);
  for (let r = 0; r < 8; r++) for (let c = 0; c < 16; c++) { const X0 = 8 + c * 63.5, Y0 = 8 + r * 63; x.fillStyle = (r + c) % 3 ? '#c9ccd4' : '#b8bcc6'; x.fillRect(X0, Y0, 58, 58); x.strokeStyle = '#4a4e5a'; x.lineWidth = 3; x.strokeRect(X0, Y0, 58, 58); x.fillStyle = '#4a4e5a'; x.beginPath(); x.arc(X0 + 46, Y0 + 29, 5, 0, 7); x.fill() } }) }
const BOXWALL = texPlane('HAT', 12, 4.4, boxesTex, { pos: [HV[0], HV[1] + 2.4, HV[2] - 4.78] });
// Bohrloch (schwarze Scheibe waechst) in der Seitenwand
const HOLE = mk('HAT', G.cyl(.4, .4, .02, 20, '#111118'), { pos: [HV[0] + 6.68, HV[1] + 1.2, HV[2] + 1], rot: [0, 0, PI / 2], outline: false, cast: false });
const ALARM = mk('HAT', G.ico(.3, 2, '#ff3030'), { pos: [HV[0] - 4, HV[1] + 4.4, HV[2] - 4.7], emis: 1, outline: false, cast: false });
// offene Faecher (Klappen) fuer "Beute"
const OPEN = [...Array(10)].map((_, k) => mk('HAT', G.box(.5, .5, .05, '#d8dbe2'), { pos: [HV[0] - 5 + k * 1.1, HV[1] + 1 + (k % 3) * 1.1, HV[2] - 4.5], rot: [0, -1.2, 0] }));
// Auto (Strasse)
const CAR = mk('HAT', merge([at(G.box(4.2, 1.0, 1.9, '#e8e8ee', { base: true }), [0, .35, 0]), at(G.box(2.4, .8, 1.7, '#cfd2da', { base: true }), [-.3, 1.35, 0]), at(G.box(2.2, .6, 1.72, '#3a4a6a', { base: true }), [-.3, 1.45, 0]),
  ...[[-1.4, .9], [1.4, .9], [-1.4, -.9], [1.4, -.9]].map(([x, z]) => at(G.cyl(.38, .38, .25, 12, '#1b1b22'), [x, .38, z + (z > 0 ? 0 : -.25)], [PI / 2, 0, 0]))]), { pos: [HX + 3, 0, 8] });
CHAP.push({ line: 'n4', n: 4, title: 'THE HATTON GARDEN HEIST', year: '2015', place: '🇬🇧 London' });
let HA_I0 = 0;
function haUpd(t, i) { const k = i - HA_I0; HOLE.vis = false; HOLE.scl = [1, 1, 1].map((_, j) => j == 1 ? 1 : (k == 2 ? lerp(.05, 1, ez(cl((t - wt(i, /drill/)) / 3, 0, 1))) : 1));
  ALARM.vis = k == 3 ? (Math.floor(t * 4) % 2 == 0) : false; OPEN.forEach((m, j) => m.vis = k == 4 && t > Lt(i).start + .3 + j * .2); CAR.vis = k == 6;
  CAR.pos = [k == 6 ? lerp(HX - 20, HX + 10, cl((t - Lt(i).start) / (nextStart(i) - Lt(i).start), 0, 1)) : HX, 0, 8] }
const OLDS = (t, n, z0, spread = 1.3, extra = {}) => { let h = ''; for (let k = 0; k < n; k++) h += fig([HV[0] - (n - 1) * spread / 2 + k * spread, HV[1], z0 + (k % 2) * .5], 'old', Object.assign({ sw: ['#6b5a4a', '#4a5a6b', '#5a4a6b', '#6b6b4a', '#4a6b5a'][k % 5], mouth: 'grin', blink: bl(t, k), look: [0, 2], bob: Math.sin(t * 2 + k) }, extra), 1.65); return h };
SHOT.h_street = { set: 'HAT', light: 'night',
  cam: i => { HA_I0 = i; return { a: { pos: [HX - 14, 6, 22], at: [HX, 4, -2], fov: 50 }, b: { pos: [HX - 6, 3, 14], at: [HX, 3, -2], fov: 48 } } },
  upd: haUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i) + .3, '🐣 EASTER WEEKEND · APRIL 2015', '#232838', '#fff', 44),
  sfx: i => [] };
SHOT.h_vault = { set: 'HAT', light: 'vault',
  cam: i => { const v = wt(i, /under/) - .2; return [
    { t0: Lt(i).start, a: { pos: [HX + 4, 4, 12], at: [HX, 2.4, -1], fov: 46 }, b: { pos: [HX + 2, 2.6, 8], at: [HX, 1.6, -1], fov: 44 } },
    { t0: v, a: { pos: [HV[0], HV[1] + 2.6, HV[2] + 4], at: [HV[0], HV[1] + 2.4, HV[2] - 5], fov: 54 }, b: { pos: [HV[0], HV[1] + 2.5, HV[2] + 2.6], at: [HV[0], HV[1] + 2.4, HV[2] - 5], fov: 52 } }] },
  light: (t, i) => t > wt(i, /under/) - .2 ? 'vault' : 'night',
  upd: haUpd,
  ui: (t, i) => labelAt([HX, 3.4, -.8], PILL('💎 JEWELRY DISTRICT', '#2a8fd6', '#fff', 44), t, wt(i, /jewelry/) - .1, wt(i, /under/) - .2) + pillAt(960, 200, t, wt(i, /safe/) - .1, nextStart(i), '🔐 SAFE DEPOSIT BOXES', '#232838', '#fff', 54),
  sfx: i => [{ k: 'pop', t: wt(i, /jewelry/) }, { k: 'whoosh', t: wt(i, /under/) - .3, d: .6 }, { k: 'pop', t: wt(i, /safe/) }] };
SHOT.h_drill = { set: 'HAT', light: 'vault',
  cam: i => { const d = wt(i, /drill/) - .3; return [
    { t0: Lt(i).start, a: { pos: [HSH[0], HSH[1] + 6, HSH[2] + 6], at: [HSH[0], HSH[1] + 5, HSH[2]], fov: 50 }, b: { pos: [HSH[0], HSH[1] + 3.5, HSH[2] + 5], at: [HSH[0], HSH[1] + 2.5, HSH[2]], fov: 50 } },
    { t0: d, a: { pos: [HV[0] + 1, HV[1] + 1.8, HV[2] + 6], at: [HV[0] + 6.6, HV[1] + 1.2, HV[2] + 1.2], fov: 46 }, b: { pos: [HV[0] + 1.6, HV[1] + 1.7, HV[2] + 5.4], at: [HV[0] + 6.6, HV[1] + 1.2, HV[2] + 1.2], fov: 44 } }] },
  upd: haUpd,
  figs: (t, i) => { const d = wt(i, /drill/) - .3; let h = '';
    if (t < d) { for (let k = 0; k < 2; k++) { const y = HSH[1] + lerp(10, 1, ez(cl((t - Lt(i).start - k * .5) / 3, 0, 1))); h += fig([HSH[0] - .5 + k, y, HSH[2] + .4], 'old', { mouth: 'grin', blink: bl(t, k), look: [0, -4], hL: [70, 40], hR: [130, 40] }, 1.6) } }
    else { const sh = Math.sin(t * 60) * 2; h += fig([HV[0] + 4.6, HV[1], HV[2] + 3.2], 'old', { mouth: 'grin', blink: bl(t, 2), look: [6, 0], prop: PROP.drill, hR: [214 + sh, 150], hL: [180, 160], bob: sh * .5 }, 1.65) }
    return h },
  ui: (t, i) => { let h = pillAt(960, 200, t, wt(i, /elevator/) - .1, wt(i, /drill/) - .3, '🛗 DOWN THE ELEVATOR SHAFT', '#232838', '#fff', 50);
    h += pillAt(960, 200, t, wt(i, /half/) - .1, nextStart(i), '🧱 WALL: 50 CM THICK', '#e0a030', OL, 56);
    if (t > wt(i, /drill/)) { h += bigText(1380, 380, t, wt(i, /drill/), nextStart(i), 'BRRRRR!', 90, '#ffd166', -8); const q = w.project([HV[0] + 5.9, HV[1] + 1.05, HV[2] + 3.2]), r = lerp(10, 110, ez(cl((t - wt(i, /drill/)) / 3, 0, 1)));
      h += `<div style="position:absolute;left:${q.x + 30}px;top:${q.y - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;background:radial-gradient(circle,#0a0a10 55%,#3a3a44 70%,#8a8e9a);border:5px solid ${OL};z-index:500"></div>` } return h },
  sfx: i => [{ k: 'pop', t: wt(i, /elevator/) }, { k: 'whoosh', t: wt(i, /drill/) - .4, d: .5 }, { k: 'type', t: wt(i, /drill/), n: 14 }, { k: 'pop', t: wt(i, /half/) }] };
SHOT.h_alarm = { set: 'HAT', light: 'vault',
  cam: i => { const n = wt(i, /no/) - .25; return [
    { t0: Lt(i).start, a: { pos: [HV[0] - 4, HV[1] + 3.2, HV[2] - 1], at: [HV[0] - 4, HV[1] + 4.2, HV[2] - 4.7], fov: 44 }, b: { pos: [HV[0] - 4, HV[1] + 3.4, HV[2] - 1.8], at: [HV[0] - 4, HV[1] + 4.3, HV[2] - 4.7], fov: 42 } },
    { t0: n, a: { pos: [HX + 10, 3, 20], at: [HX, 2, 2], fov: 48 }, b: { pos: [HX + 8, 2.6, 18], at: [HX, 2, 2], fov: 48 } }] },
  light: (t, i) => t > wt(i, /no/) - .25 ? 'night' : 'vault',
  upd: haUpd,
  ui: (t, i) => { let h = ''; if (t < wt(i, /no/) - .25 && Math.floor(t * 4) % 2 == 0) h += `<div style="position:absolute;inset:0;background:#ff2020;opacity:.18;z-index:1500"></div>`;
    h += bigText(960, 200, t, wt(i, /alarm/), wt(i, /no/) - .25, '🚨 ALARM!', 120, '#ff5d5d'); h += stampAt(960, 420, t, wt(i, /police/) - .05, 'NO POLICE', '#e0303a', 120, -6); return h },
  sfx: i => [{ k: 'error', t: wt(i, /alarm/) }, { k: 'error', t: wt(i, /alarm/) + .5 }, { k: 'impact', t: wt(i, /police/) }] };
SHOT.h_loot = { set: 'HAT', light: 'vault',
  cam: i => ({ a: { pos: [HV[0] + 3, HV[1] + 2.6, HV[2] + 3.5], at: [HV[0], HV[1] + 1.6, HV[2] - 4.6], fov: 50 }, b: { pos: [HV[0] + 1, HV[1] + 2.2, HV[2] + 2.4], at: [HV[0], HV[1] + 1.6, HV[2] - 4.6], fov: 48 } }),
  upd: haUpd,
  figs: (t, i) => OLDS(t, 3, HV[2] - 1.6, 2.2, { propL: PROP.bag, hL: [40, 210] }),
  ui: (t, i) => counter(960, 200, t, Lt(i).start + .2, nextStart(i), Lt(i).start + .3, wt(i, /pounds/), 0, 14, v => '💰 UP TO £' + Math.round(v) + ' MILLION', '#35a862', '#fff', 70),
  sfx: i => [...Array(10)].map((_, j) => ({ k: 'click', t: Lt(i).start + .3 + j * .2 })).concat([{ k: 'cash', t: wt(i, /pounds/) }]) };
SHOT.h_grandpas = { set: 'HAT', light: 'vault',
  cam: i => ({ a: { pos: [HV[0], HV[1] + 1.8, HV[2] + 4.5], at: [HV[0], HV[1] + 1.2, HV[2] - 1], fov: 46 }, b: { pos: [HV[0], HV[1] + 1.6, HV[2] + 3.2], at: [HV[0], HV[1] + 1.1, HV[2] - 1], fov: 44 } }),
  figs: (t, i) => OLDS(t, 4, HV[2] - 1, 1.5),
  ui: (t, i) => { const a = wt(i, /seventy/i); return pillAt(960, 200, t, wt(i, /pensioners/) - .1, nextStart(i), '👴 THE "GRANDPA GANG"', '#6b5a4a', '#fff', 56) + counter(960, 320, t, a - .1, nextStart(i), a, a + 1, 0, 76, v => 'RINGLEADER: ' + Math.round(v) + ' YEARS OLD', '#ffd166', OL, 56) },
  sfx: i => [{ k: 'pop', t: wt(i, /pensioners/) }, { k: 'ding', t: wt(i, /seventy/i) + 1 }] };
SHOT.h_cars = { set: 'HAT', light: 'night',
  cam: i => ({ a: { pos: [HX - 8, 7, 18], at: [HX - 6, 1, 8], fov: 50 }, b: { pos: [HX + 4, 7, 18], at: [HX + 4, 1, 8], fov: 50 } }),
  upd: haUpd,
  ui: (t, i) => { let h = stampAt(1450, 260, t, wt(i, /mistake/) - .05, 'MISTAKE', '#e0303a', 90, 8, wt(i, /cameras/) - .1);
    if (t > wt(i, /cameras/) - .1) { const q = w.project(X(CAR.pos, 0, 1, 0)); h += `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-50%) scale(${pop(t, wt(i, /cameras/) - .1)});width:340px;height:200px;border:8px solid #ff5d5d;border-radius:14px;z-index:2100"></div><div style="position:absolute;right:40px;top:40px;font:900 52px IB;color:#ff5d5d;text-shadow:${shadowTxt(OL, 4)};z-index:2100">● REC  CCTV</div>` }
    return h },
  sfx: i => [{ k: 'impact', t: wt(i, /mistake/), g: .5 }, { k: 'beep', t: wt(i, /cameras/), f: 1200 }] };
SHOT.h_prison = { set: 'HAT', light: 'vault',
  cam: i => ({ a: { pos: [HV[0], HV[1] + 1.8, HV[2] + 4.5], at: [HV[0], HV[1] + 1.2, HV[2] - 1], fov: 46 }, b: { pos: [HV[0], HV[1] + 1.6, HV[2] + 3.6], at: [HV[0], HV[1] + 1.1, HV[2] - 1], fov: 44 } }),
  figs: (t, i) => OLDS(t, 4, HV[2] - 1, 1.5, { sw: '#d0d0d0', swd: '#9a9a9a', pa: '#9a9a9a', mid: MID.stripes, mouth: 'sad' }),
  ui: (t, i) => { let h = ''; if (t < wt(i, /millions/) - .2) { for (let k = 0; k < 11; k++) h += `<div style="position:absolute;left:${300 + k * 132}px;top:0;width:26px;height:1080px;background:linear-gradient(90deg,#2a2a33,#5a5a66 45%,#2a2a33);border:3px solid ${OL};z-index:1900"></div>`;
      h += stampAt(960, 300, t, wt(i, /six/) - .05, '6–7 YEARS', '#e0303a', 110, -6) }
    h += pillAt(960, 200, t, wt(i, /millions/) - .1, nextStart(i), '💎 MILLIONS STILL MISSING', '#e0303a', '#fff', 58); return h },
  sfx: i => [{ k: 'impact', t: wt(i, /six/) }, { k: 'ding', t: wt(i, /millions/) }] };
