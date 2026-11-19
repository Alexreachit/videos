// ===================== Set ANT: Antwerpen 2003 (Diamantenviertel, Buero, Tresor, Wald an der Autobahn) =====================
const AX = 2000;
const AC = [AX, 0, 0], AO = [AX, 0, -80], AV = [AX, -12, -6], AF = [AX, 0, 90];
(function antwerp() {
  const S = 'ANT';
  mk(S, merge([at(G.box(160, .4, 60, '#6a6e80', { base: true }), [AX, -.4, 10]), at(G.box(160, .3, 8, '#3a3f55', { base: true }), [AX, 0, 8])]), { outline: false, cast: false });
  // Diamond Center: moderner Block + Nachbarhaeuser
  const B = [at(G.box(18, 14, 10, '#c9ccd4', { base: true }), [AX, 0, -8])];
  for (let r = 0; r < 4; r++) for (let c = -3; c <= 3; c++) B.push(at(G.box(1.8, 2, .2, '#3a5a8a', { base: true }), [AX + c * 2.4, 2 + r * 3, -2.9]));
  [-20, -12, 12, 20].forEach((x, k) => B.push(at(G.box(7, 9 + (k % 2) * 3, 8, ['#d8c8a8', '#b8a07a', '#c9b896', '#a8b0c0'][k], { base: true }), [AX + x, 0, -7])));
  mk(S, merge(B).vary(.03, 17));
  // Buero
  mk(S, merge([at(G.box(12, .3, 9, '#8a7a6a', { base: true }), [AO[0], -.3, AO[2]]), at(G.box(12, 5, .3, '#d8d0c0', { base: true }), [AO[0], 0, AO[2] - 4.5]),
    at(G.box(.3, 5, 9, '#c8c0b0', { base: true }), [AO[0] - 6, 0, AO[2]]), at(G.box(2.4, 1.6, .1, '#9fd3f0', { base: true }), [AO[0] + 2, 2, AO[2] - 4.34]),
    at(G.box(3, .12, 1.4, '#6b4226', { base: true }), [AO[0], 1.0, AO[2] - 1.5]), at(G.box(2.8, 1.0, 1.2, '#5a3a20', { base: true }), [AO[0], 0, AO[2] - 1.5])]), { outline: false });
  // Tresor: Wand mit Schliessfaechern + runde Tresortuer
  mk(S, merge([at(G.box(14, .3, 12, '#5a5e6a', { base: true }), [AV[0], AV[1] - .3, AV[2]]), at(G.box(14, 5, .4, '#8a8e9a', { base: true }), [AV[0], AV[1], AV[2] - 5]),
    at(G.box(.4, 5, 12, '#9a9eaa', { base: true }), [AV[0] - 7, AV[1], AV[2]]), at(G.box(.4, 5, 12, '#9a9eaa', { base: true }), [AV[0] + 7, AV[1], AV[2]]),
    at(G.box(14, .3, 12, '#4a4e5a', { base: true }), [AV[0], AV[1] + 5, AV[2]]), at(G.box(5, 5, .5, '#7a7e8a', { base: true }), [AV[0], AV[1], AV[2] + 6])]), { outline: false });
  // Wald + Autobahn (Daemmerung)
  mk(S, G.box(200, .4, 60, '#4a7a3a', { base: true }), { pos: [AF[0], -.4, AF[2]], outline: false, cast: false });
  mk(S, merge([at(G.box(200, .2, 10, '#4a4e5a', { base: true }), [AF[0], 0, AF[2] + 8]), at(G.box(200, .22, .3, '#e8e8ee', { base: true }), [AF[0], 0, AF[2] + 8])]), { outline: false });
  const T = []; for (let k = 0; k < 60; k++) { const x = AF[0] - 40 + (k % 15) * 5.4 + G.hash(k) * 2, z = AF[2] - 2 - Math.floor(k / 15) * 4 - G.hash(k, 2) * 2;
    T.push(at(G.cyl(.25, .2, 3, 8, '#5a3a26'), [x, 0, z]), at(G.cyl(1.8, .1, 4.5, 8, k % 2 ? '#2f6a3a' : '#3a7a44'), [x, 2.4, z])) }
  mk(S, merge(T));
})();
const BOXW_A = texPlane('ANT', 12, 4.4, boxesTex, { pos: [AV[0], AV[1] + 2.4, AV[2] - 4.78] });
const OPEN_A = [...Array(24)].map((_, k) => mk('ANT', G.box(.5, .5, .05, '#d8dbe2'), { pos: [AV[0] - 5.4 + (k % 12) * .98, AV[1] + 1.4 + Math.floor(k / 12) * 1.6 + (k % 3) * .3, AV[2] - 4.5], rot: [0, -1.2, 0] }));
const VDOOR = mk('ANT', merge([at(G.cyl(2, 2, .6, 28, '#a8acb8'), [0, 0, 0], [PI / 2, 0, 0]), at(G.cyl(.5, .5, .3, 16, '#6a6e7a'), [0, 0, .4], [PI / 2, 0, 0]), ...[0, 1, 2, 3].map(k => at(G.box(1.6, .12, .12, '#4a4e5a'), [0, 0, .55], [0, 0, k * PI / 4]))]), { pos: [AV[0], AV[1] + 2.4, AV[2] + 5.7], spec: .6 });
const SENS = [[-2.6, 4.2, 'heat'], [2.6, 4.2, 'ir'], [-2.6, .8, 'light']].map(([x, y]) => mk('ANT', merge([at(G.box(.6, .4, .3, '#e8e8ee'), [0, 0, 0]), at(G.ico(.12, 1, '#ff3030'), [0, 0, .18])]), { pos: [AV[0] + x, AV[1] + y, AV[2] + 5.6] }));
const DIAS = [...Array(14)].map((_, k) => mk('ANT', G.ico(.09 + (k % 3) * .03, 1, '#bfefff'), { pos: [AV[0] - .7 + (k % 7) * .22, AV[1] + .1 + Math.floor(k / 7) * .12, AV[2] - 1 + G.hash(k) * .4], spec: 1, emis: .25 }));
const ACAR = mk('ANT', merge([at(G.box(4.2, 1.0, 1.9, '#5a6a8a', { base: true }), [0, .35, 0]), at(G.box(2.4, .8, 1.7, '#4a5a7a', { base: true }), [-.3, 1.35, 0]), ...[[-1.4, .9], [1.4, .9], [-1.4, -.9], [1.4, -.9]].map(([x, z]) => at(G.cyl(.38, .38, .25, 12, '#1b1b22'), [x, .38, z + (z > 0 ? 0 : -.25)], [PI / 2, 0, 0]))]), { pos: [AF[0], 0, AF[2] + 6] });
const BAGS = [...Array(4)].map((_, k) => mk('ANT', G.ico(.3, 2, '#2a2a33', 0, 1, .8).smooth(), { pos: [AF[0] - 2.4 + k * .6, .22, AF[2] + 1.6 + (k % 2) * .4] }));
const SANDW = mk('ANT', merge([at(G.box(.9, .12, .5, '#e8b866'), [0, 0, 0]), at(G.box(.86, .06, .48, '#d64545'), [0, .09, 0]), at(G.box(.9, .12, .5, '#e8b866'), [0, .18, 0])]), { pos: [AF[0] - .4, .4, AF[2] + 2.6], rot: [0, .4, 0] });
CHAP.push({ line: 'n2', n: 2, title: 'THE ANTWERP DIAMOND HEIST', year: '2003', place: '🇧🇪 Antwerp' });
let AN_I0 = 0;
function anUpd(t, i) { const k = i - AN_I0; OPEN_A.forEach((m, j) => m.vis = (k == 4 && t > Lt(i).start + .3 + j * .12) || k == 5);
  DIAS.forEach((m, j) => { m.vis = k == 5 || (k == 9 && t < wt(i, /never/) + j * .06); m.rot = [0, t + j, 0] });
  SENS.forEach((m, j) => m.vis = k == 2 || k == 3);
  ACAR.vis = k == 6; ACAR.pos = [k == 6 ? lerp(AF[0] - 30, AF[0] + 1, ez(cl((t - Lt(i).start) / 2.4, 0, 1))) : AF[0], 0, AF[2] + 6];
  BAGS.forEach((m, j) => { m.vis = (k == 6 && t > wt(i, /dumped/) + j * .2) || k == 7 }); SANDW.vis = k == 7 }
SHOT.a_city = { set: 'ANT', light: 'dusk',
  cam: i => { AN_I0 = i; return { a: { pos: [AX - 18, 6, 28], at: [AX, 6, -6], fov: 52 }, b: { pos: [AX - 8, 3, 18], at: [AX, 5, -6], fov: 50 } } },
  upd: anUpd,
  ui: (t, i) => pillAt(960, 200, t, Math.max(wt(i, /diamond/) - .1, Lt(i).start + 2.7), nextStart(i), '💎 DIAMOND CAPITAL OF THE WORLD', '#2a8fd6', '#fff', 52) + pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📅 FEBRUARY 2003', '#232838', '#fff', 44),
  sfx: i => [{ k: 'shimmer', t: wt(i, /diamond/) }] };
SHOT.a_office = { set: 'ANT', light: 'indoorWarm',
  cam: i => ({ a: { pos: [AO[0] + 3, 2.2, AO[2] + 4], at: [AO[0], 1.4, AO[2] - 1.5], fov: 46 }, b: { pos: [AO[0] + 1.6, 1.9, AO[2] + 2.6], at: [AO[0], 1.4, AO[2] - 1.5], fov: 44 } }),
  figs: (t, i) => fig([AO[0] - .2, 0, AO[2] - .5], 'suit', { mouth: 'grin', blink: bl(t, 0), look: [4, 2], prop: PROP.magnifier, hR: [180, 120], armL: [.3, .3] }),
  ui: (t, i) => { const a = wt(i, /two/); return pillAt(960, 200, t, wt(i, /notarbartolo/i) - .1, wt(i, /two/) - .2, 'LEONARDO NOTARBARTOLO', '#232838', '#fff', 54) + counter(960, 200, t, a - .1, nextStart(i), a, a + 1.4, 0, 2, v => '🎭 PLAYING A TRADER: ' + (v > 1.95 ? '2+ YEARS' : Math.round(v * 12) + ' MONTHS'), '#ffd166', OL, 52) },
  sfx: i => [{ k: 'pop', t: wt(i, /notarbartolo/i) }, { k: 'tick', t: wt(i, /two/) }] };
const LAYERS = [['🔢', 'COMBINATION LOCK', /combination/], ['🌡️', 'HEAT SENSORS', /heat/], ['📳', 'SEISMIC SENSOR', /seismic/], ['📡', 'RADAR', /radar/], ['🧲', 'MAGNETIC FIELD', /magnetic/]];
SHOT.a_vault = { set: 'ANT', light: 'vault',
  cam: i => ({ a: { pos: [AV[0] + 1.5, AV[1] + 2.6, AV[2] + 14], at: [AV[0], AV[1] + 2.4, AV[2] + 5.7], fov: 46 }, b: { pos: [AV[0] + .8, AV[1] + 2.5, AV[2] + 11.5], at: [AV[0], AV[1] + 2.4, AV[2] + 5.7], fov: 44 } }),
  upd: anUpd,
  ui: (t, i) => { let h = ''; LAYERS.forEach(([ic, tx, re], k) => { const a = wt(i, re) - .1; if (t > a) h += `<div style="position:absolute;left:${k % 2 ? 1380 : 120}px;top:${170 + k * 120}px;transform:scale(${pop(t, a)});transform-origin:${k % 2 ? 'right' : 'left'};z-index:2200">${PILL(ic + ' ' + tx, '#232838', '#fff', 40)}</div>` }); return h },
  sfx: i => LAYERS.map(([, , re]) => ({ k: 'pop', t: wt(i, re) })) };
const BEAT = [['💨 HAIRSPRAY → HEAT SENSOR', /hairspray/i], ['🧊 FOAM SHIELD → INFRARED', /foam/], ['🩹 TAPE → LIGHT SENSOR', /tape/i]];
SHOT.a_beat = { set: 'ANT', light: 'vault',
  cam: i => ({ a: { pos: [AV[0] - 1, AV[1] + 3, AV[2] + 11], at: [AV[0] - 1, AV[1] + 2.6, AV[2] + 5.7], fov: 48 }, b: { pos: [AV[0] - .6, AV[1] + 2.9, AV[2] + 10], at: [AV[0] - .6, AV[1] + 2.6, AV[2] + 5.7], fov: 46 } }),
  upd: anUpd,
  figs: (t, i) => { const s = wt(i, /hairspray/i); return fig([AV[0] - 2.2, AV[1], AV[2] + 7.4], 'mask', { mouth: 'grin', blink: bl(t, 0), look: [-3, -5], prop: t > s - .3 && t < s + 1.4 ? PROP.spray : '', hR: t > s - .3 && t < s + 1.4 ? [150, 30] : null, armL: [.2, .2] }) },
  ui: (t, i) => { let h = ''; BEAT.forEach(([tx, re], k) => { const a = wt(i, re) - .1; if (t > a) h += `<div style="position:absolute;left:960px;top:${180 + k * 110}px;transform:translate(-50%,0) scale(${pop(t, a)});z-index:2200">${PILL('✅ ' + tx, '#35a862', '#fff', 46)}</div>` }); return h },
  sfx: i => BEAT.map(([, re]) => ({ k: 'ding', t: wt(i, re) })) };
SHOT.a_boxes = { set: 'ANT', light: 'vault',
  cam: i => ({ a: { pos: [AV[0] + 3, AV[1] + 2.6, AV[2] + 4], at: [AV[0], AV[1] + 2.2, AV[2] - 4.6], fov: 52 }, b: { pos: [AV[0] + 1, AV[1] + 2.4, AV[2] + 2.6], at: [AV[0], AV[1] + 2.2, AV[2] - 4.6], fov: 50 } }),
  upd: anUpd,
  figs: (t, i) => { let h = ''; [-3, 0, 3].forEach((dx, k) => h += fig([AV[0] + dx, AV[1], AV[2] - 2.6 + (k % 2) * .5], k % 2 ? 'mask' : 'thief', { mouth: 'grin', blink: bl(t, k), look: [0, -3], hR: [180, 80 + 20 * Math.sin(t * 6 + k)] })); return h },
  ui: (t, i) => { const a = Lt(i).start + .3, b = wt(i, /nine/) + .3; return counter(960, 200, t, a, nextStart(i), a, b, 0, 109, v => '🔓 ' + Math.round(v) + ' OF 189 BOXES', '#232838', '#fff', 64) },
  sfx: i => [...Array(12)].map((_, j) => ({ k: 'click', t: Lt(i).start + .3 + j * .3 })) };
SHOT.a_haul = { set: 'ANT', light: 'vault',
  cam: i => ({ a: { pos: [AV[0] + .6, AV[1] + 2.2, AV[2] + 3.2], at: [AV[0], AV[1] + .2, AV[2] - .8], fov: 44 }, b: { pos: [AV[0] + .3, AV[1] + 1.8, AV[2] + 2.4], at: [AV[0], AV[1] + .2, AV[2] - .8], fov: 42 } }),
  upd: anUpd,
  ui: (t, i) => { const a = Lt(i).start + .2, b = wt(i, /dollars/); return counter(960, 200, t, a, nextStart(i), a, b, 0, 100, v => '💎 $' + Math.round(v) + ' MILLION+', '#35a862', '#fff', 72) + bigText(960, 360, t, wt(i, /century/) - .2, nextStart(i), '"HEIST OF THE CENTURY"', 84, '#ffd166', -3) },
  sfx: i => [{ k: 'cash', t: wt(i, /dollars/) }, { k: 'shimmer', t: wt(i, /century/) }] };
SHOT.a_forest = { set: 'ANT', light: 'dusk',
  cam: i => ({ a: { pos: [AF[0] + 8, 3, AF[2] + 14], at: [AF[0], 1, AF[2] + 3], fov: 50 }, b: { pos: [AF[0] + 6, 2.6, AF[2] + 12], at: [AF[0], 1, AF[2] + 3], fov: 48 } }),
  upd: anUpd,
  figs: (t, i) => { const d = wt(i, /dumped/) - .4; if (t < d) return ''; return fig([AF[0] - 2.2, 0, AF[2] + 8.4], 'thief', { mouth: 'grin', blink: bl(t, 0), look: [-5, 0], propL: Math.floor((t - d) * 2) % 2 ? PROP.bag : '', hL: [20, 150 + 30 * Math.sin(t * 6)] }) },
  ui: (t, i) => pillAt(960, 200, t, wt(i, /trash/) - .1, nextStart(i), '🗑️ TRASH IN THE FOREST', '#232838', '#fff', 54) + stampAt(1450, 320, t, wt(i, /forest/), 'MISTAKE', '#e0303a', 90, 8),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: 1.0 }, { k: 'thud', t: wt(i, /dumped/), g: .5 }, { k: 'impact', t: wt(i, /forest/), g: .5 }] };
SHOT.a_sandwich = { set: 'ANT', light: 'day',
  cam: i => { const s = wt(i, /inside/i) - .2; return [
    { t0: Lt(i).start, a: { pos: [AF[0] + 5, 2.4, AF[2] + 9], at: [AF[0], 1, AF[2] + 2], fov: 48 }, b: { pos: [AF[0] + 4, 2.2, AF[2] + 8], at: [AF[0], 1, AF[2] + 2], fov: 46 } },
    { t0: s, a: { pos: [AF[0] - .2, 2.0, AF[2] + 5.4], at: [AF[0] - .6, .45, AF[2] + 2.4], fov: 40 }, b: { pos: [AF[0] - .2, 1.8, AF[2] + 4.9], at: [AF[0] - .6, .45, AF[2] + 2.4], fov: 38 } }] },
  upd: anUpd,
  figs: (t, i) => t > wt(i, /inside/i) - .2 ? '' : fig([AF[0] + 1.6, 0, AF[2] + 3.2], 'old', { hat: HAT.cap, mouth: 'o', blink: bl(t, 0), look: [-5, 3], sweat: true }),
  ui: (t, i) => labelAt([AF[0] + 1.6, 2.1, AF[2] + 3.2], PILL('🧑‍🌾 LANDOWNER', '#4f8a3c', '#fff', 40), t, wt(i, /landowner/) - .1, wt(i, /inside/i) - .2) + bigText(960, 200, t, wt(i, /salami/) - .1, nextStart(i), '🥪 HALF-EATEN SALAMI SANDWICH', 76),
  sfx: i => [{ k: 'pop', t: wt(i, /landowner/) }, { k: 'ding', t: wt(i, /salami/) }] };
SHOT.a_dna = { set: 'ANT', light: 'day',
  cam: i => ({ a: { pos: [AF[0] - .2, 1.8, AF[2] + 4.9], at: [AF[0] - .6, .45, AF[2] + 2.4], fov: 38 }, b: { pos: [AF[0] - .2, 1.6, AF[2] + 4.5], at: [AF[0] - .6, .45, AF[2] + 2.4], fov: 36 } }),
  upd: (t, i) => { anUpd(t, i); SANDW.vis = true },
  ui: (t, i) => { let h = ''; const a = wt(i, /dna/i) - .1; if (t > a) { let p = ''; for (let k = 0; k < 14; k++) { const y = k * 22, x1 = 60 + 50 * Math.sin(k * .6 + t * 3), x2 = 60 - 50 * Math.sin(k * .6 + t * 3); p += `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="#ffd166" stroke-width="6"/><circle cx="${x1}" cy="${y}" r="9" fill="#2fd0ff"/><circle cx="${x2}" cy="${y}" r="9" fill="#ff5d9a"/>` }
      h += `<div style="position:absolute;left:260px;top:280px;transform:scale(${2 * pop(t, a)});transform-origin:0 0;z-index:2200"><svg width="120" height="300">${p}</svg></div>` + pillAt(360, 200, t, a, nextStart(i), '🧬 DNA', '#2a8fd6', '#fff', 50) }
    h += stampAt(1400, 400, t, wt(i, /ten/) - .05, '10 YEARS', '#e0303a', 100, 8); return h },
  sfx: i => [{ k: 'ding', t: wt(i, /dna/i) }, { k: 'impact', t: wt(i, /ten/) }] };
SHOT.a_never = { set: 'ANT', light: 'vault',
  cam: i => ({ a: { pos: [AV[0] + .4, AV[1] + 1.4, AV[2] + 1.8], at: [AV[0] + .1, AV[1] + .1, AV[2] - .8], fov: 44 }, b: { pos: [AV[0] + .2, AV[1] + 1.6, AV[2] + 2.4], at: [AV[0] + .1, AV[1] + .1, AV[2] - .8], fov: 46 } }),
  upd: anUpd,
  ui: (t, i) => bigText(960, 220, t, wt(i, /never/) - .1, nextStart(i), 'NEVER FOUND', 130, '#ff5d5d', -4),
  sfx: i => [{ k: 'impact', t: wt(i, /never/) }] };
