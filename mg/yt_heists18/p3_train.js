// ===================== Set TRN: Great Train Robbery 1963 (Nacht, Gleis, Signal, Farm, Gefaengnis) =====================
const TX = 400, RY = 1.2;              // Gleis-Hoehe (Damm)
const SIG = [TX + 18, RY, -2.2];       // Signalmast
(function train() {
  const S = 'TRN';
  mk(S, G.box(400, .4, 300, '#2f4a3a', { base: true }), { pos: [TX, -.4, 0], outline: false, cast: false });
  // Damm + Schotter + Schienen + Schwellen
  mk(S, merge([at(G.box(400, 1.0, 7, '#4a4a40', { base: true }), [TX, 0, 0]), at(G.box(400, .25, 4, '#6a665a', { base: true }), [TX, 1.0, 0])]), { outline: false });
  const R = [at(G.box(400, .14, .12, '#a8acb8', { base: true }), [TX, RY, -.72]), at(G.box(400, .14, .12, '#a8acb8', { base: true }), [TX, RY, .72])];
  for (let x = -120; x <= 120; x += 1.1) R.push(at(G.box(.3, .1, 2.2, '#4a3a2a', { base: true }), [TX + x, RY - .08, 0]));
  mk(S, merge(R), { outline: false, cast: false });
  // Telegrafenmasten + Hecken + Baeume
  const T = []; for (let k = -10; k <= 10; k++) { T.push(at(G.cyl(.08, .07, 5, 6, '#3a2a22'), [TX + k * 12, 1, 3.6]), at(G.box(.1, .1, 1.4, '#3a2a22'), [TX + k * 12, 5.6, 3.6])) }
  mk(S, merge(T), { outline: false });
  const B = []; for (let k = 0; k < 40; k++) { const x = TX - 150 + k * 7.7 + G.hash(k) * 4, z = (k % 2 ? 1 : -1) * (14 + G.hash(k, 3) * 30); B.push(at(G.ico(2 + G.hash(k, 5) * 2, 2, k % 3 ? '#23402f' : '#2c4a36'), [x, 1.6, z]), at(G.cyl(.25, .2, 2, 6, '#3a2a22'), [x, 0, z])) }
  mk(S, merge(B).smooth(), { cast: false });
  // Signal: Mast + Kopf
  mk(S, merge([at(G.cyl(.12, .1, 5, 8, '#2a2a33'), SIG), at(G.box(.9, 1.8, .5, '#1b1b22', { base: true }), X(SIG, 0, 4.2, 0)), at(G.box(.12, 4.2, .12, '#555'), X(SIG, .3, 0, .3))]));
})();
const SIG_G = mk('TRN', G.ico(.26, 2, '#35e08a'), { pos: X(SIG, 0, 5.5, .3), emis: 1, outline: false, cast: false });
const SIG_R = mk('TRN', G.ico(.26, 2, '#ff4040'), { pos: X(SIG, 0, 4.7, .3), emis: 1, outline: false, cast: false });
const SIG_GOFF = mk('TRN', G.ico(.26, 2, '#1d3a2a'), { pos: X(SIG, 0, 5.5, .3), outline: false, cast: false });
const SIG_ROFF = mk('TRN', G.ico(.26, 2, '#3a1d1d'), { pos: X(SIG, 0, 4.7, .3), outline: false, cast: false });
const GLOVE = mk('TRN', merge([at(G.ico(.32, 2, '#6b4a2e', 0, 1, .8), [0, 0, 0]), ...[0, 1, 2, 3].map(k => at(G.cyl(.06, .05, .3, 6, '#6b4a2e'), [-.15 + k * .1, .25, 0]))]).smooth(), { pos: X(SIG, 0, 5.5, .42) });
const SIGLAD = mk('TRN', merge([at(G.box(.06, 4.2, .06, '#8a6a46'), [-.3, 2.1, 0]), at(G.box(.06, 4.2, .06, '#8a6a46'), [.3, 2.1, 0]), ...[...Array(7)].map((_, k) => at(G.box(.6, .05, .05, '#8a6a46'), [0, .4 + k * .55, 0]))]), { pos: X(SIG, -1.1, -.2, .5), rot: [0, 0, -.12], outline: false });
const BATT = mk('TRN', merge([at(G.box(.5, .35, .3, '#e0a030', { base: true }), [0, 0, 0]), at(G.box(.08, .1, .08, '#222', { base: true }), [-.12, .35, 0]), at(G.box(.08, .1, .08, '#c33', { base: true }), [.12, .35, 0])]), { pos: X(SIG, -.6, 3.6, .3) });
// Zug: Lok + 2 Postwagen (Wurzel bewegt sich in x)
const TRAIN = mk('TRN', merge([at(G.box(11, 3.0, 2.7, '#3f7a4a', { base: true }), [0, .5, 0]), at(G.box(11.2, .5, 2.8, '#2a2a33', { base: true }), [0, .1, 0]),
  at(G.box(1.6, 1.0, 2.75, '#2c5a36', { base: true }), [4.6, 2.3, 0]), at(G.box(.12, .1, 2.8, '#ffd166', { base: true }), [0, 1.8, 0]),
  ...[-4.2, -2.6, 2.6, 4.2].map(x => at(G.cyl(.45, .45, 2.9, 12, '#1b1b22'), [x, .45, -1.45], [PI / 2, 0, 0])),
  at(G.box(13, 3.0, 2.7, '#7a2a2a', { base: true }), [-12.4, .5, 0]), at(G.box(13, .4, 2.8, '#2a2a33', { base: true }), [-12.4, .1, 0]),
  at(G.box(13, 3.0, 2.7, '#7a2a2a', { base: true }), [-26.0, .5, 0]), at(G.box(13, .4, 2.8, '#2a2a33', { base: true }), [-26.0, .1, 0]),
  ...[-16.6, -8.2, -30.2, -21.8].map(x => at(G.cyl(.45, .45, 2.9, 12, '#1b1b22'), [x, .45, -1.45], [PI / 2, 0, 0])),
  at(G.box(1.6, 1.4, .3, '#2a1a12', { base: true }), [-12.4, .6, 1.36])]), { pos: [TX, RY, 0] });
const TRAIN_WIN = mk('TRN', merge([at(G.box(1.4, .8, .1, '#ffe9a0', { base: true }), [4.6, 2.5, 1.38]), at(G.box(.3, .4, .1, '#ffffff', { base: true }), [5.55, 1.2, 0]),
  ...[-17, -15, -10, -8, -30, -28, -23, -21].map(x => at(G.box(1.0, .6, .1, '#ffcf7a', { base: true }), [x + 4.6 - 4.6, 2.3, 1.38]))]), { parent: TRAIN, emis: .95, outline: false, cast: false });
const HEAD = mk('TRN', G.box(.12, .5, .9, '#fff6c0'), { parent: TRAIN, pos: [5.56, 1.3, 0], emis: 1, outline: false, cast: false });
// Lastwagen + Sackhaufen
const LORRY = [TX - 12.4, 0, 8];
const LORRYM = mk('TRN', merge([at(G.box(6, 2.6, 2.6, '#4a5a3a', { base: true }), [-1, .8, 0]), at(G.box(2.2, 2.0, 2.4, '#3a4a2e', { base: true }), [3.2, .8, 0]), at(G.box(1.8, .8, .1, '#ffe9a0', { base: true }), [3.3, 2.0, 1.22]),
  ...[[-3, 1.2], [1, 1.2], [3.2, 1.2], [-3, -1.2], [1, -1.2], [3.2, -1.2]].map(([x, z]) => at(G.cyl(.5, .5, .3, 12, '#1b1b22'), [x, .5, z + (z > 0 ? 0 : -.3)], [PI / 2, 0, 0]))]), { pos: LORRY });
const SACKS = [...Array(14)].map((_, k) => mk('TRN', G.ico(.42, 2, '#c9b48a', 0, 1, .75).smooth(), { pos: [LORRY[0] - 1 + (k % 5) * .8, .3 + Math.floor(k / 5) * .5, LORRY[2] - 2.2 + (k % 2 ? .3 : -.3)], rot: [0, k, 0] }));
// Postwagen innen (bei z=-60): Saecke in Regalen
const PW = [TX, 0, -60];
mk('TRN', merge([at(G.box(12, .2, 4, '#5a4a3a', { base: true }), [PW[0], 0, PW[2]]), at(G.box(12, 3.2, .2, '#6a3a30', { base: true }), [PW[0], 0, PW[2] - 2]),
  at(G.box(12, .2, 4, '#3a2a2a', { base: true }), [PW[0], 3.2, PW[2]]), at(G.box(.2, 3.2, 4, '#5a302a', { base: true }), [PW[0] - 6, 0, PW[2]]),
  ...[0, 1, 2].map(k => at(G.box(10, .12, 1.0, '#8a6a46', { base: true }), [PW[0], .9 + k * .8, PW[2] - 1.4]))]), { outline: false });
mk('TRN', merge([...Array(30)].map((_, k) => at(G.ico(.36, 2, ['#c9b48a', '#bba67a', '#d4c296'][k % 3], 0, 1, .7), [PW[0] - 4.6 + (k % 10) * 1.0, 1.25 + Math.floor(k / 10) * .8, PW[2] - 1.4]))).smooth());
mk('TRN', G.box(.6, .3, .6, '#fff2c0'), { pos: [PW[0], 3.1, PW[2]], emis: 1, outline: false, cast: false });
// Farmhaus innen (bei z=+80)
const FM = [TX, 0, 80];
mk('TRN', merge([at(G.box(12, .2, 10, '#7a5a3a', { base: true }), [FM[0], 0, FM[2]]), at(G.box(12, 4, .3, '#c9b896', { base: true }), [FM[0], 0, FM[2] - 5]),
  at(G.box(.3, 4, 10, '#b8a684', { base: true }), [FM[0] - 6, 0, FM[2]]), at(G.box(1.2, 1.4, .1, '#24305a', { base: true }), [FM[0] + 2, 1.8, FM[2] - 4.8]),
  at(G.box(3.2, .14, 2.2, '#8a5a32', { base: true }), [FM[0], .9, FM[2]]), ...[[-1.4, -.9], [1.4, -.9], [-1.4, .9], [1.4, .9]].map(([x, z]) => at(G.box(.14, .9, .14, '#6b4226', { base: true }), [FM[0] + x, 0, FM[2] + z]))]), { outline: false });
mk('TRN', G.ico(.25, 2, '#fff2c0'), { pos: [FM[0], 3.2, FM[2]], emis: 1, outline: false, cast: false });
function boardTex() { return tex(512, 512, x => { x.fillStyle = '#d8ecd6'; x.fillRect(0, 0, 512, 512); const c = ['#8a4a2a', '#9fd3f0', '#d64f9a', '#f08a2a', '#e04040', '#f2d23a', '#2fa36b', '#2a5ab0'];
  for (let k = 0; k < 9; k++) { [[k * 56, 0], [k * 56, 456], [0, k * 56], [456, k * 56]].forEach(([a, b], s) => { x.fillStyle = '#f6f2e6'; x.fillRect(a, b, 56, 56); x.strokeStyle = OL; x.lineWidth = 3; x.strokeRect(a, b, 56, 56); x.fillStyle = c[(k + s * 2) % 8]; x.fillRect(a + 4, b + 4, 48, 14) }) }
  x.fillStyle = '#c8e0c4'; x.fillRect(80, 80, 352, 352); x.fillStyle = '#f2d23a'; x.save(); x.translate(256, 256); x.rotate(-.6); x.fillRect(-60, -30, 120, 60); x.restore() }) }
const BOARD = texPlane('TRN', 1.6, 1.6, boardTex, { pos: [FM[0], 1.05, FM[2]], rot: [-PI / 2, 0, 0] });
const NOTES = [...Array(8)].map((_, k) => mk('TRN', merge([at(G.box(.3, .05, .15, '#6a8acb', { base: true }), [0, 0, 0]), at(G.box(.05, .055, .16, '#f4efe2', { base: true }), [0, 0, 0])]), { pos: [FM[0] - .5 + (k % 4) * .33, 1.06, FM[2] + (k < 4 ? -.45 : .45)], rot: [0, .4 * (k % 3) - .4, 0] }));
// Gefaengnismauer (bei z=+160)
const PM = [TX, 0, 160];
mk('TRN', merge([at(G.box(40, 9, 1.4, '#8a7a6a', { base: true }), [PM[0], 0, PM[2]]), at(G.box(40, .6, 1.8, '#6a5a4a', { base: true }), [PM[0], 9, PM[2]]), at(G.box(3, 14, 3, '#7a6a5a', { base: true }), [PM[0] + 14, 0, PM[2] - 1])]).vary(.04, 4));
const LADDER = mk('TRN', merge([at(G.box(.06, 9.4, .06, '#c9b48a'), [-.35, 4.7, 0]), at(G.box(.06, 9.4, .06, '#c9b48a'), [.35, 4.7, 0]), ...[...Array(14)].map((_, k) => at(G.box(.7, .05, .05, '#c9b48a'), [0, .5 + k * .65, 0]))]), { pos: [PM[0] - 2, 0, PM[2] + .8], outline: false });
const SEARCH = mk('TRN', G.cyl(.1, 2.6, 18, 18, '#fff6c0'), { pos: [PM[0] + 14, 14, PM[2] - 1], alpha: .16, emis: 1, outline: false, cast: false, recv: false });
// Leere Saecke im Feld (Ende)
const EMPTY = [TX + 40, 0, 6];
mk('TRN', merge([...Array(9)].map((_, k) => at(G.ico(.5, 2, '#bba67a', 0, 1, .25), [EMPTY[0] - 3 + (k % 3) * 2.2 + G.hash(k) * .8, .1, EMPTY[2] - 2 + Math.floor(k / 3) * 1.8]))).smooth());
// ---------- Kapitel #6 ----------
CHAP.push({ line: 'n6', n: 6, title: 'THE GREAT TRAIN ROBBERY', year: '1963', place: '🇬🇧 England' });
const trainX = (t, i0) => { // faehrt mit 9 m/s, bremst 2 s lang, steht am Signal
  const tS = wt(i0 + 2, /stops/) + .3, xS = SIG[0] - 7;
  if (t >= tS) return xS; if (t < tS - 2) return xS - 9 - 9 * (tS - 2 - t); const u = t - (tS - 2); return xS - 9 + 9 * u - 9 * u * u / 4;
};
let TR_I0 = 0;
function trainUpd(t, i) { TRAIN.pos = [trainX(t, TR_I0), RY, 0]; const red = t > wt(TR_I0 + 2, /red/) - .1;
  SIG_G.vis = !red; SIG_GOFF.vis = red; SIG_R.vis = red; SIG_ROFF.vis = !red;
  GLOVE.vis = i > TR_I0 + 3 || (i == TR_I0 + 3 && t > wt(TR_I0 + 3, /glove/) - .2); BATT.vis = i > TR_I0 + 3 || (i == TR_I0 + 3 && t > wt(TR_I0 + 3, /battery/) - .2);
  LORRYM.vis = i >= TR_I0 + 5; SIGLAD.vis = i == TR_I0 + 3; SACKS.forEach(m => m.vis = false) }
SHOT.t_train_night = { set: 'TRN', light: 'night',
  cam: i => { TR_I0 = i; const xa = trainX(Lt(i).start, i), xb = trainX(nextStart(i), i); return { a: { pos: [xa + 16, 7, 16], at: [xa - 4, 2, 0], fov: 46 }, b: { pos: [xb + 9, 3.2, 11], at: [xb - 6, 2.4, 0], fov: 48 } } },
  upd: trainUpd,
  ui: (t, i) => pillAt(960, 930 - 120, t, Lt(i).start + 2.8, nextStart(i), '📅 8 AUG 1963 · 3:00 AM', '#232838', '#fff', 44),
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + 3, d: 1.2 }] };
SHOT.t_sacks = { set: 'TRN', light: 'indoorWarm',
  cam: i => ({ a: { pos: [PW[0] + 3.5, 1.9, PW[2] + 1.6], at: [PW[0] - 1, 1.5, PW[2] - 1.4], fov: 46 }, b: { pos: [PW[0] + 2, 1.8, PW[2] + 1.3], at: [PW[0] - 2, 1.5, PW[2] - 1.4], fov: 42 } }),
  figs: (t, i) => fig([PW[0] + .8, .1, PW[2] + .2], 'driver', { sw: '#5a6070', swd: '#4a5060', hat: HAT.guard, mouth: 'hmm', blink: bl(t, 2), propL: PROP.sack, hL: [40, 200], look: [-4, 0] }),
  ui: (t, i) => pillAt(960, 200, t, wt(i, /banknotes/) - .1, nextStart(i), '💷 USED BANKNOTES', '#35a862', '#fff', 58) + bigText(960, 330, t, wt(i, /millions/i) - .05, nextStart(i), 'MILLIONS', 110, '#ffd166', -4),
  sfx: i => [{ k: 'pop', t: wt(i, /banknotes/) }, { k: 'cash', t: wt(i, /millions/i) }] };
SHOT.t_signal = { set: 'TRN', light: 'night',
  cam: i => { const s = wt(i, /stops/) - .1; return [
    { t0: Lt(i).start, a: { pos: X(SIG, 2.6, 5.2, 3.2), at: X(SIG, 0, 5.0, .3), fov: 34 }, b: { pos: X(SIG, 2.0, 5.1, 2.6), at: X(SIG, 0, 5.0, .3), fov: 32 } },
    { t0: s, a: { pos: X(SIG, 7, 3.6, 13), at: X(SIG, -10, 2.2, 0), fov: 42 }, b: { pos: X(SIG, 6, 3.4, 12), at: X(SIG, -10, 2.2, 0), fov: 42 } }] },
  upd: trainUpd,
  ui: (t, i) => bigText(960, 180, t, wt(i, /red/) - .05, wt(i, /stops/) - .1, '🔴 STOP', 120, '#ff5d5d') + bigText(1300, 300, t, wt(i, /stops/) + .1, nextStart(i), 'SCREECH!', 100, '#ffd166', -6),
  sfx: i => [{ k: 'ding', t: wt(i, /red/) }, { k: 'thud', t: wt(i, /stops/) + .3, g: .7 }] };
SHOT.t_glove = { set: 'TRN', light: 'night',
  cam: i => ({ a: { pos: X(SIG, 2.6, 4.2, 6.4), at: X(SIG, -.5, 3.6, .3), fov: 44 }, b: { pos: X(SIG, 2.2, 4.2, 5.8), at: X(SIG, -.5, 3.6, .3), fov: 44 } }),
  upd: trainUpd,
  figs: (t, i) => { const g = wt(i, /glove/) - .2, u = cl(t, g - .6, g); return fig(X(SIG, -1.1, 3.4, .6), 'mask', { mouth: 'grin', blink: bl(t, 1), look: [5, -4], hR: [lerp(150, 214, u), lerp(160, 30, u)], prop: u < 1 ? PROP.glove : '', armL: [.2, .2] }, 1.7) },
  ui: (t, i) => { let h = stampAt(1450, 300, t, wt(i, /trick/) - .05, 'TRICK!', '#e0303a', 110, 8);
    h += labelAt(X(SIG, -.6, 4.05, .3), PILL('🔋 BATTERY', '#ffd166', OL, 40), t, wt(i, /battery/) - .1, nextStart(i));
    h += labelAt(X(SIG, .55, 5.9, .4), PILL('🧤 GLOVE', '#6b4a2e', '#fff', 40), t, wt(i, /glove/), nextStart(i)); return h },
  sfx: i => [{ k: 'impact', t: wt(i, /trick/), g: .5 }, { k: 'pop', t: wt(i, /glove/) }, { k: 'pop', t: wt(i, /battery/) }] };
SHOT.t_storm = { set: 'TRN', light: 'night',
  cam: i => { const h = wt(i, /driver/) - .1; return [
    { t0: Lt(i).start, a: { pos: [SIG[0] - 12, 2.8, 8.5], at: [SIG[0] - 27, 1.6, 2], fov: 50 }, b: { pos: [SIG[0] - 13, 2.6, 8], at: [SIG[0] - 26, 1.6, 2], fov: 48 } },
    { t0: h, a: { pos: [SIG[0] - 3.4, 2.6, 9], at: [SIG[0] - 3.4, 2.0, 2], fov: 44 }, b: { pos: [SIG[0] - 3.4, 2.5, 8], at: [SIG[0] - 3.4, 2.0, 2], fov: 42 } }] },
  upd: trainUpd,
  figs: (t, i) => { let h = ''; const hd = wt(i, /driver/) - .1, hit = wt(i, /hit/);
    if (t < hd) for (let k = 0; k < 8; k++) { const s = Lt(i).start + k * .18, x = lerp(SIG[0] - 40 - k * 2.6, SIG[0] - 24 + k * 1.3, ez(cl((t - s) / 2.4, 0, 1))); h += fig([x, 1.0, 2.2 + (k % 3) * .5], k % 2 ? 'mask' : 'thief', Object.assign({ mouth: 'grin', blink: bl(t, k), look: [5, 0] }, walk(t + k, 12)), 1.7) }
    else { const dx = TRAIN.pos[0] + 3.2; h += fig([dx, 1.0, 2.4], 'driver', { mouth: t > hit ? 'o' : 'hmm', blink: t > hit ? 1 : bl(t, 0), look: [-5, 2], tilt: t > hit ? .25 : 0, sweat: t > hit }, 1.5);
      h += fig([dx - 1.5, 1.0, 2.5], 'mask', { mouth: 'grin', blink: bl(t, 2), prop: PROP.cosh(t < hit ? -60 + 80 * ez(cl(t, hit - .35, hit)) : 20), hR: [200, 90], look: [6, 0] }, 1.6) }
    return h },
  ui: (t, i) => { let h = counter(960, 200, t, Lt(i).start + .2, wt(i, /driver/) - .1, wt(i, /fifteen/i) - .1, wt(i, /men/), 0, 15, v => '👥 ' + Math.round(v) + ' MEN', '#232838', '#fff', 64);
    const hit = wt(i, /hit/); if (t > hit) h += labelAt([TRAIN.pos[0] + 3.2, 3.0, 2.4], `<div style="font:900 70px IB;color:#ffd166;text-shadow:${shadowTxt(OL, 5)}">💫</div>`, t, hit, nextStart(i));
    h += pillAt(960, 200, t, wt(i, /jack/i) - .1, nextStart(i), 'DRIVER: JACK MILLS', '#3f7a4a', '#fff', 50); return h },
  sfx: i => [{ k: 'whoosh', t: Lt(i).start + .2, d: .8 }, { k: 'pop', t: wt(i, /fifteen/i) }, { k: 'impact', t: wt(i, /hit/) + .05, g: .7 }] };
SHOT.t_unload = { set: 'TRN', light: 'night',
  cam: i => ({ a: { pos: [LORRY[0] + 15, 3.6, 4.4], at: [LORRY[0], 1.6, 4.2], fov: 48 }, b: { pos: [LORRY[0] + 12, 3.2, 4.4], at: [LORRY[0], 1.6, 4.2], fov: 46 } }),
  upd: (t, i) => { trainUpd(t, i); const a = Lt(i).start, b = nextStart(i) - .5; SACKS.forEach((m, k) => m.vis = t > lerp(a, b, k / SACKS.length)) },
  figs: (t, i) => { let h = ''; for (let k = 0; k < 5; k++) { const z = 2.0 + k * 1.05, ph = (t * 2.2 + k * .5) % 1, carry = ph < .5;
    h += fig([LORRY[0] + 2.5 + (k % 2) * .5, k < 2 ? 1.0 : 0, z], k % 2 ? 'mask' : 'thief', { mouth: 'grin', blink: bl(t, k), look: [0, 2], hL: carry ? [60, 150] : [40, 236], hR: carry ? [140, 150] : [160, 236], propL: carry ? PROP.sack : '' }, 1.7) } return h },
  ui: (t, i) => { const a = Lt(i).start + .3, b = wt(i, /pounds/); let h = counter(960, 190, t, a, nextStart(i), a, b, 0, 2.6, v => '£' + v.toFixed(1) + ' MILLION', '#35a862', '#fff', 76);
    h += pillAt(960, 300, t, wt(i, /today/i) - .1, nextStart(i), 'TODAY: ≈ £50 MILLION', '#ffd166', OL, 54); return h },
  sfx: i => [{ k: 'cash', t: wt(i, /pounds/) }, { k: 'ding', t: wt(i, /today/i) }] };
SHOT.t_monopoly = { set: 'TRN', light: 'indoorWarm',
  cam: i => { const r = wt(i, /real/) - .2; return [
    { t0: Lt(i).start, a: { pos: [FM[0] + 4.5, 2.6, FM[2] + 5], at: [FM[0], 1.3, FM[2]], fov: 48 }, b: { pos: [FM[0] + 3.5, 2.4, FM[2] + 4], at: [FM[0], 1.2, FM[2]], fov: 46 } },
    { t0: r, a: { pos: [FM[0] + .2, 3.0, FM[2] + 1.0], at: [FM[0], 1.0, FM[2]], fov: 46 }, b: { pos: [FM[0] + .1, 2.6, FM[2] + .8], at: [FM[0], 1.0, FM[2]], fov: 44 } }] },
  upd: (t, i) => { NOTES.forEach((m, k) => m.vis = t > wt(i, /real/) + k * .08) },
  figs: (t, i) => { if (t > wt(i, /real/) - .2) return ''; let h = '';
    [[-2.3, .3, 'thief', 5], [2.3, .3, 'mask', -5], [-2.2, -1.3, 'thief', 4]].forEach(([dx, dz, who, lx], k) => h += fig([FM[0] + dx, 0, FM[2] + dz], who, { mouth: 'grin', talk: k == 2 ? .3 + .3 * Math.sin(t * 6) : 0, blink: bl(t, k), look: [lx, 4], hR: [150, 150], hL: [50, 150] }, 1.7));
    return h },
  ui: (t, i) => { let h = labelAt([FM[0], 1.2, FM[2]], PILL('🎲 BOARD GAME', '#232838', '#fff', 40), t, wt(i, /monopoly/i) - .1, wt(i, /real/) - .2);
    h += bigText(960, 190, t, wt(i, /real/), nextStart(i), 'WITH THE <span style="color:#35e08a">REAL</span> MONEY', 92); return h },
  sfx: i => [{ k: 'pop', t: wt(i, /monopoly/i) }, { k: 'cash', t: wt(i, /real/) + .1 }] };
SHOT.t_prints = { set: 'TRN', light: 'indoorWarm',
  cam: i => ({ a: { pos: [FM[0], 3.0, FM[2] + .6], at: [FM[0], 1.0, FM[2]], fov: 40 }, b: { pos: [FM[0], 2.4, FM[2] + .45], at: [FM[0], 1.0, FM[2]], fov: 38 } }),
  upd: (t, i) => NOTES.forEach(m => m.vis = false),
  ui: (t, i) => { let h = stampAt(960, 250, t, wt(i, /mistake/) - .05, 'MISTAKE', '#e0303a', 100, -6, wt(i, /police/) - .1);
    const f = wt(i, /fingerprints/) - .2; [[760, 520], [1080, 620], [900, 760], [1220, 470]].forEach(([x, y], k) => { if (t > f + k * .15) h += `<div style="position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%) scale(${pop(t, f + k * .15)}) rotate(${k * 37}deg);z-index:2200"><svg width="120" height="150" viewBox="0 0 120 150">${[...Array(6)].map((_, r) => `<ellipse cx="60" cy="75" rx="${12 + r * 9}" ry="${16 + r * 11}" fill="none" stroke="#2fd0ff" stroke-width="6" opacity=".85"/>`).join('')}</svg></div>` });
    h += pillAt(960, 930 - 120, t, f, nextStart(i), '🔍 FINGERPRINTS', '#2a8fd6', '#fff', 54); return h },
  sfx: i => [{ k: 'impact', t: wt(i, /mistake/), g: .6 }, ...[0, 1, 2, 3].map(k => ({ k: 'pop', t: wt(i, /fingerprints/) - .2 + k * .15 }))] };
SHOT.t_biggs = { set: 'TRN', light: 'night',
  cam: i => { const r = wt(i, /ronnie/i) - .15; return [
    { t0: Lt(i).start, a: { pos: [PM[0] + 12, 3, PM[2] + 26], at: [PM[0] + 4, 7, PM[2]], fov: 52 }, b: { pos: [PM[0] + 10, 3, PM[2] + 23], at: [PM[0] + 4, 7, PM[2]], fov: 52 } },
    { t0: r, a: { pos: [PM[0] + 4, 3.5, PM[2] + 9], at: [PM[0] - 2, 5.5, PM[2]], fov: 48 }, b: { pos: [PM[0] + 3, 4.5, PM[2] + 8], at: [PM[0] - 2, 6.5, PM[2]], fov: 48 } }] },
  upd: (t, i) => { SEARCH.rot = [0, 0, .5 + .35 * Math.sin(t * .9)] ; LADDER.vis = t > wt(i, /ronnie/i) - .15 },
  figs: (t, i) => { const r = wt(i, /ronnie/i) - .15; if (t < r) return ''; const u = cl((t - r - .4) / 3.2, 0, 1), ph = Math.sin(t * 10);
    return fig([PM[0] - 2, lerp(.2, 8.6, u), PM[2] + 1.1], 'prisoner', { mouth: 'grin', blink: bl(t, 1), look: [0, -6], hL: [70, 60 + 20 * ph], hR: [130, 60 - 20 * ph], legL: .3 * ph, legR: -.3 * ph }, 1.7) },
  ui: (t, i) => { let h = stampAt(960, 300, t, wt(i, /thirty/i) - .05, '30 YEARS', '#e0303a', 120, -6, wt(i, /ronnie/i) - .15);
    const e = wt(i, /run/); h += counter(960, 190, t, e - .1, nextStart(i), e, e + 1.6, 0, 36, v => '🏃 ON THE RUN: ' + Math.round(v) + ' YEARS', '#232838', '#fff', 60); return h },
  sfx: i => [{ k: 'impact', t: wt(i, /thirty/i) }, { k: 'whoosh', t: wt(i, /ronnie/i) - .2, d: .5 }, { k: 'tick', t: wt(i, /run/) }] };
SHOT.t_empty = { set: 'TRN', light: 'night',
  cam: i => ({ a: { pos: [EMPTY[0] + 6, 5, EMPTY[2] + 6], at: [EMPTY[0], .5, EMPTY[2]], fov: 46 }, b: { pos: [EMPTY[0] + 4, 3.6, EMPTY[2] + 5], at: [EMPTY[0], .5, EMPTY[2]], fov: 44 } }),
  ui: (t, i) => bigText(960, 200, t, wt(i, /never/) - .05, nextStart(i) + 1, 'NEVER FOUND', 130, '#ff5d5d', -4) + pillAt(960, 360, t, wt(i, /money/) - .1, nextStart(i) + 1, '💷 £ ???', '#35a862', '#fff', 64),
  sfx: i => [{ k: 'impact', t: wt(i, /never/) }] };
