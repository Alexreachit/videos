// ===================== Set DRE: Dresden 2019 (Schloss + Bruecke Nacht, Gruenes Gewoelbe innen, Garage) =====================
const DX = 1600;
const DC = [DX, 0, 0], DB = [DX + 26, 0, 14], DW = [DX - 4, 0, -2.6], DV = [DX, 0, -80], DG = [DX, 0, 80];
(function dresden() {
  const S = 'DRE', SAND = '#d8c8a8', SAND2 = '#bba98a', COP = '#5aa08a';
  mk(S, G.box(400, .4, 400, '#3a3f55', { base: true }), { pos: [DX, -.4, 0], outline: false, cast: false });
  // Fluss
  mk(S, G.box(400, .1, 30, '#2a4a7a', { base: true }), { pos: [DX, -.05, 30], outline: false, cast: false, spec: .5 });
  // Schloss (Barock): Hauptbau + Turm mit gruenem Kupferdach
  const F = [at(G.box(34, 12, 8, SAND, { base: true }), [DX, 0, -7]), at(G.box(34.4, 3.4, 8.4, COP, { base: true }), [DX, 12, -7]), at(G.box(34.6, .5, 8.6, SAND2, { base: true }), [DX, 11.8, -7]),
    at(G.box(5, 26, 5, SAND, { base: true }), [DX + 12, 0, -9]), at(G.cyl(3.2, .2, 8, 8, COP), [DX + 12, 26, -9]), at(G.ico(1.6, 2, COP), [DX + 12, 27.5, -9])];
  for (let k = -6; k <= 6; k++) if (k != -1) for (let r = 0; r < 3; r++) F.push(at(G.box(1.2, 2.2, .3, '#2a2a3a', { base: true }), [DX + k * 2.5, 1.4 + r * 3.4, -2.9]));
  mk(S, merge(F).vary(.03, 13));
  // Fenster mit Gitter (wird aufgeschnitten)
  mk(S, G.box(1.4, 2.2, .2, '#ffcf7a', { base: true }), { pos: [DW[0], 1.4, -2.95], emis: .4, outline: false, cast: false });
  // Bruecke (Steinboegen) + Laternen
  const B = [at(G.box(10, 1, 50, SAND2, { base: true }), [DB[0], 2.6, DB[2] + 10])];
  for (let k = 0; k < 4; k++) B.push(at(G.box(9, 2.6, 3, SAND2, { base: true }), [DB[0], 0, DB[2] + k * 12 + 2]));
  mk(S, merge(B));
  // Strassenlaternen am Schloss (gehen aus)
  [-12, -4, 4].forEach(dx => mk(S, merge([at(G.cyl(.1, .1, 4.6, 8, '#22252e'), [DX + dx, 0, 2])])));
  // Gruenes Gewoelbe innen: gruene Waende, Spiegel/Gold, Vitrinen
  mk(S, merge([at(G.box(20, .3, 14, '#5a3a2a', { base: true, top: '#6a4a32' }), [DV[0], -.3, DV[2]]), at(G.box(20, 7, .4, '#2f6a52', { base: true }), [DV[0], 0, DV[2] - 7]),
    at(G.box(.4, 7, 14, '#2a5e48', { base: true }), [DV[0] - 10, 0, DV[2]]), at(G.box(.4, 7, 14, '#2a5e48', { base: true }), [DV[0] + 10, 0, DV[2]]),
    at(G.box(20, .3, .6, '#c9a23c', { base: true }), [DV[0], 5.2, DV[2] - 6.7]), at(G.box(20, .3, .6, '#c9a23c', { base: true }), [DV[0], .9, DV[2] - 6.7]),
    at(G.box(20, .4, 14, '#1f3a30', { base: true }), [DV[0], 7, DV[2]]),
    at(G.box(3.2, 1.0, 1.6, '#3a2a1e', { base: true }), [DV[0], 0, DV[2] - 2])]), { outline: false });
  // Tiefgarage
  mk(S, merge([at(G.box(30, .3, 16, '#6a6a72', { base: true }), [DG[0], -.3, DG[2]]), at(G.box(30, .3, 16, '#4a4a52', { base: true }), [DG[0], 3.4, DG[2]]),
    ...[-10, 0, 10].map(x => at(G.box(.8, 3.4, .8, '#8a8a92', { base: true }), [DG[0] + x, 0, DG[2] - 3])), at(G.box(30, 3.4, .3, '#5a5a62', { base: true }), [DG[0], 0, DG[2] - 8])]), { outline: false });
})();
const LAMPS_D = [-12, -4, 4].map(dx => mk('DRE', G.box(.5, .5, .5, '#ffe7a0', { base: true }), { pos: [DX + dx, 4.6, 2], emis: 1, outline: false, cast: false }));
const DWIN = mk('DRE', G.box(1.4, 2.2, .2, '#ffcf7a', { base: true }), { pos: [DW[0], 1.4, -2.95], emis: .6, outline: false, cast: false });
const BARS_D = mk('DRE', merge([...Array(5)].map((_, k) => at(G.cyl(.05, .05, 2.4, 6, '#2a2a33'), [-.56 + k * .28, 0, 0])).concat([at(G.box(1.5, .08, .08, '#2a2a33'), [0, 1.0, 0])])), { pos: [DW[0], 1.3, -2.75] });
// Stromkasten mit Feuer (auf der Bruecke)
const PBOX = [DB[0] - 3.4, 3.6, DB[2] + 2];
mk('DRE', merge([at(G.box(1, 1.6, .7, '#7a7e8a', { base: true }), PBOX), at(G.box(.6, .3, .05, '#ffd166', { base: true }), X(PBOX, 0, 1.1, .36))]));
const FIRE = [0, 1, 2, 3].map(k => mk('DRE', G.ico(.35 - k * .05, 2, k % 2 ? '#ffb030' : '#ff6020', 0, 1, 1.6), { pos: X(PBOX, -.2 + k * .14, 1.8 + k * .2, .1), emis: 1, outline: false, cast: false }));
// Vitrine mit Schmuck (Glas zerspringt)
const VIT = X(DV, 0, 1.0, -2);
const GLASS = mk('DRE', G.box(3.0, 1.4, 1.4, '#bfe6ff', { base: true }), { pos: VIT, alpha: .3, spec: .9, outline: false, cast: false });
const JEWELS = [...Array(9)].map((_, k) => mk('DRE', k % 3 == 0 ? G.ico(.18, 1, '#9fe3ff') : merge([at(G.cyl(.18, .18, .05, 14, '#ffd166'), [0, 0, 0]), at(G.ico(.08, 1, ['#e0303a', '#35e08a', '#9fe3ff'][k % 3]), [0, .06, 0])]), { pos: X(VIT, -1.1 + (k % 5) * .55, .2, -.3 + Math.floor(k / 5) * .55), spec: .9, emis: .2 }));
const SHARDS = [...Array(10)].map((_, k) => mk('DRE', G.box(.25, .02, .2, '#dff4ff'), { pos: VIT, alpha: .6, outline: false, cast: false }));
const AUDI = mk('DRE', merge([at(G.box(4.4, 1.0, 1.9, '#4a4a50', { base: true }), [0, .35, 0]), at(G.box(2.6, .8, 1.7, '#3a3a40', { base: true }), [-.2, 1.35, 0]),
  ...[[-1.5, .9], [1.5, .9], [-1.5, -.9], [1.5, -.9]].map(([x, z]) => at(G.cyl(.38, .38, .25, 12, '#111'), [x, .38, z + (z > 0 ? 0 : -.25)], [PI / 2, 0, 0]))]), { pos: X(DG, 0, 0, 0) });
const SMOKE = [...Array(6)].map((_, k) => mk('DRE', G.ico(.8, 2, '#5a5a62'), { pos: X(DG, 0, 2, 0), alpha: .45, outline: false, cast: false }));
CHAP.push({ line: 'n3', n: 3, title: 'THE GREEN VAULT', year: '2019', place: '🇩🇪 Dresden' });
let DR_I0 = 0;
function drUpd(t, i) { const k = i - DR_I0, fire = k > 1 || (k == 1 && t > wt(i, /fire/) - .1), dark = k > 1 || (k == 1 && t > wt(i, /dark/) - .2);
  FIRE.forEach((m, j) => { m.vis = fire && k <= 2; m.scl = [1, 1 + .25 * Math.sin(t * 9 + j * 2), 1] });
  LAMPS_D.forEach(m => m.vis = !dark); DWIN.vis = k >= 2;
  const cut = k > 2 || (k == 2 && t > wt(i, /bars/));
  BARS_D.vis = !cut; const sm = k == 4 && t > wt(i, /smash/) || k > 4 ? 1 : 0;
  const ax = DR_I0 + 3, hit = wt(ax, /smash/) + .25; const broken = k > 3 || (k == 3 && t > hit);
  GLASS.vis = !broken || k >= 7; SHARDS.forEach((m, j) => { const u = k == 3 ? cl((t - hit) / .8, 0, 1) : 0; m.vis = k == 3 && t > hit; const a = j * 2.4; m.pos = X(VIT, Math.cos(a) * u * 2.4, .7 + u * (1.2 - u * 1.8), Math.sin(a) * u * 1.6 + u); m.rot = [u * 6 + j, u * 4, j] });
  const gone = k == 4 && t > wt(i, /grab/) ? 1 : 0;
  JEWELS.forEach((m, j) => { const tj = wt(DR_I0 + 4, /grab/) + j * .35; const u = k == 4 ? ez(cl((t - tj) / .6, 0, 1)) : (k > 4 && k < 7 ? 1 : 0);
    m.vis = (k <= 4 || k >= 7) && !(k == 4 && u >= 1) && !(k == 8 && j == 4); m.pos = X(VIT, lerp(-1.1 + (j % 5) * .55, 2.0, u), .2 + Math.sin(u * PI) * 1.2 - u * .4, lerp(-.3 + Math.floor(j / 5) * .55, .9, u)); m.rot = [0, t * (k >= 7 ? .6 : 0) + j, 0] });
  AUDI.vis = k == 5; SMOKE.forEach((m, j) => { const p = ((t * .35 + j / 6) % 1); m.vis = k == 5; m.pos = X(DG, -.5 + j * .2, 1.6 + p * 2.2, 0); m.scl = [.5 + p, .5 + p, .5 + p] }) }
SHOT.d_city = { set: 'DRE', light: 'night',
  cam: i => { DR_I0 = i; return { a: { pos: [DX + 34, 12, 48], at: [DX + 4, 8, -6], fov: 52 }, b: { pos: [DX + 26, 7, 36], at: [DX + 2, 6, -6], fov: 50 } } },
  upd: drUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📅 25 NOV 2019 · ~4:00 AM', '#232838', '#fff', 44) };
SHOT.d_fire = { set: 'DRE', light: 'night',
  cam: i => { const d = wt(i, /streetlights/) - .3; return [
    { t0: Lt(i).start, a: { pos: X(PBOX, 4, 1.6, 5), at: X(PBOX, 0, 1.4, 0), fov: 44 }, b: { pos: X(PBOX, 3, 1.4, 4), at: X(PBOX, 0, 1.4, 0), fov: 42 } },
    { t0: d, a: { pos: [DX - 4, 3, 16], at: [DX - 4, 3, 0], fov: 50 }, b: { pos: [DX - 4, 2.8, 14], at: [DX - 4, 3, 0], fov: 50 } }] },
  upd: drUpd,
  ui: (t, i) => bigText(1300, 300, t, wt(i, /fire/), wt(i, /streetlights/) - .3, '🔥 FIRE!', 110, '#ff9a3a', -6) + (t > wt(i, /dark/) - .2 ? `<div style="position:absolute;inset:0;background:#000;opacity:${.35 * ez(cl(t, wt(i, /dark/) - .2, wt(i, /dark/) + .3))};z-index:1500"></div>` : '') + pillAt(960, 200, t, wt(i, /dark/), nextStart(i), '💡 LIGHTS OUT', '#232838', '#fff', 56),
  sfx: i => [{ k: 'impact', t: wt(i, /fire/), g: .5 }, { k: 'thud', t: wt(i, /dark/), g: .6 }] };
SHOT.d_window = { set: 'DRE', light: 'night',
  cam: i => ({ a: { pos: [DW[0] + 3, 2.2, 5], at: [DW[0], 1.8, -2.8], fov: 44 }, b: { pos: [DW[0] + 2, 2.0, 3.8], at: [DW[0], 1.8, -2.8], fov: 42 } }),
  upd: drUpd,
  figs: (t, i) => { const c = wt(i, /climb/) - .1, u = cl((t - c) / 1.6, 0, 1); return fig([DW[0] + .9 - u * .9, 0, -1.6 - u * .9], 'mask', { mouth: 'grin', blink: bl(t, 0), look: [-5, -2], hR: t < c ? [200 + 20 * Math.sin(t * 12), 110] : [160, 60], prop: t < c ? `<g transform="rotate(-30)"><rect x="-4" y="-50" width="8" height="56" fill="#c9ccd4" stroke="${OL}" stroke-width="4"/></g>` : '' }) +
    fig([DW[0] + 2.2, 0, -1.4], 'mask', { mouth: 'hmm', blink: bl(t, 1), look: [-4, 0], armL: [.2, .2] }) },
  ui: (t, i) => stampAt(1350, 300, t, wt(i, /bars/), 'CUT!', '#e0303a', 100, 8, wt(i, /climb/)) + pillAt(960, 200, t, wt(i, /green/i) - .1, nextStart(i), '👑 GREEN VAULT · ROYAL TREASURE · 1700s', '#2f6a52', '#fff', 46),
  sfx: i => [{ k: 'swish', t: wt(i, /cut/), d: .3 }, { k: 'impact', t: wt(i, /bars/), g: .5 }, { k: 'pop', t: wt(i, /green/i) }] };
SHOT.d_axe = { set: 'DRE', light: 'indoorWarm',
  cam: i => ({ a: { pos: X(VIT, 3.6, 1.6, 4), at: X(VIT, 0, .7, 0), fov: 44 }, b: { pos: X(VIT, 2.8, 1.4, 3.2), at: X(VIT, 0, .7, 0), fov: 42 } }),
  upd: drUpd,
  figs: (t, i) => { const h = wt(i, /smash/) + .25, sw = t < h ? lerp(-40, -150, ez(cl(t, h - .9, h - .3))) + 160 * ez(cl(t, h - .3, h)) : 10; return fig(X(VIT, -2.2, -1.0, .6), 'mask', { mouth: 'grin', blink: bl(t, 0), look: [5, 0], prop: PROP.axe(sw), hR: [196, 120], hL: [170, 140] }) },
  ui: (t, i) => bigText(1300, 320, t, wt(i, /smash/) + .25, nextStart(i), 'CRASH!', 120, '#9fe3ff', -8) + labelAt(X(VIT, 0, 1.8, 0), PILL('🪓 AXE', '#232838', '#fff', 44), t, wt(i, /axe/) - .1, nextStart(i)),
  sfx: i => [{ k: 'swish', t: wt(i, /smash/), d: .3 }, { k: 'impact', t: wt(i, /smash/) + .25 }, { k: 'shimmer', t: wt(i, /smash/) + .3 }] };
SHOT.d_jewels = { set: 'DRE', light: 'indoorWarm',
  cam: i => ({ a: { pos: X(VIT, .4, 1.7, 5.2), at: X(VIT, .6, .3, .3), fov: 46 }, b: { pos: X(VIT, .6, 1.5, 4.6), at: X(VIT, .8, .3, .3), fov: 44 } }),
  upd: drUpd,
  figs: (t, i) => fig(X(VIT, 2.2, -1.0, .9), 'mask', { mouth: 'grin', blink: bl(t, 0), look: [-5, 0], propL: PROP.bag, hL: [40, 200] }),
  ui: (t, i) => { const a = wt(i, /four/), b = wt(i, /euros/); return counter(960, 190, t, a - .1, nextStart(i), a, a + 1, 0, 4300, v => '💎 ' + MG.fmt(Math.round(v / 10) * 10, 0) + '+ DIAMONDS', '#2a8fd6', '#fff', 62) + counter(960, 300, t, b - .6, nextStart(i), b - .6, b + .2, 0, 113, v => 'WORTH €' + Math.round(v) + '+ MILLION', '#35a862', '#fff', 62) },
  sfx: i => [...Array(9)].map((_, j) => ({ k: 'pop', t: wt(i, /grab/) + j * .35 + .5 })).concat([{ k: 'cash', t: wt(i, /euros/) }]) };
SHOT.d_car = { set: 'DRE', light: 'vault',
  cam: i => ({ a: { pos: X(DG, 6, 2.2, 6), at: X(DG, 0, .8, 0), fov: 46 }, b: { pos: X(DG, 4.6, 1.8, 5), at: X(DG, 0, .8, 0), fov: 44 } }),
  upd: drUpd,
  ui: (t, i) => pillAt(960, 200, t, wt(i, /burned/) - .1, nextStart(i), '🔥 GETAWAY CAR: BURNED', '#e0303a', '#fff', 56) + labelAt(X(DG, 0, 2.4, 0), `<div style="font:900 90px IB;color:#ff9a3a;text-shadow:${shadowTxt(OL, 5)}">🔥</div>`, t, Lt(i).start + .2, nextStart(i)),
  sfx: i => [{ k: 'impact', t: wt(i, /burned/), g: .5 }] };
SHOT.d_police = { set: 'DRE', light: 'night',
  cam: i => ({ a: { pos: [DX - 2, 2.4, 12], at: [DX - 2, 1.6, 0], fov: 48 }, b: { pos: [DX - 2, 2.2, 10], at: [DX - 2, 1.6, 0], fov: 46 } }),
  upd: drUpd,
  figs: (t, i) => { let h = ''; [-4.5, -3, 1.5, 3].forEach((dx, k) => h += fig([DX - 2 + dx, 0, 2.4 + (k % 2) * .4], 'cop', { sw: '#2a5a3a', swd: '#1e4a2e', pa: '#2a2e3a', hat: HAT.cop.replace('#1b2f6b', '#2a5a3a'), mouth: 'hmm', blink: bl(t, k), look: [dx > 0 ? -5 : 5, 0] }));
    [-1, 0].forEach((dx, k) => h += fig([DX - 2 + dx * 1.3 + .6, 0, 1.6], 'thief', { mouth: 'sad', blink: bl(t, k + 5), look: [0, 3], armL: [.05, .05], armR: [.05, .05], sweat: true })); return h },
  ui: (t, i) => { let h = pillAt(960, 200, t, wt(i, /family/) - .3, nextStart(i), '👨‍👦 BERLIN CRIME FAMILY', '#232838', '#fff', 56);
    if (Math.floor(t * 3) % 2 == 0) h += `<div style="position:absolute;inset:0;background:radial-gradient(circle at 15% 30%,#3a7aff55,transparent 40%);z-index:1500"></div>`; else h += `<div style="position:absolute;inset:0;background:radial-gradient(circle at 85% 30%,#3a7aff55,transparent 40%);z-index:1500"></div>`; return h },
  sfx: i => [{ k: 'beep', t: Lt(i).start + .3, f: 900 }, { k: 'pop', t: wt(i, /family/) }] };
SHOT.d_return = { set: 'DRE', light: 'indoorWarm',
  cam: i => ({ a: { pos: X(VIT, 0, 1.6, 4.4), at: X(VIT, 0, .6, 0), fov: 44 }, b: { pos: X(VIT, 0, 1.4, 3.4), at: X(VIT, 0, .6, 0), fov: 42 } }),
  upd: drUpd,
  ui: (t, i) => stampAt(620, 300, t, wt(i, /back/) - .05, '2022: RETURNED', '#35a862', 70, -6) + stampAt(1300, 420, t, wt(i, /convicted/) - .05, '2023: 5 CONVICTED', '#e0303a', 70, 6),
  sfx: i => [{ k: 'ding', t: wt(i, /back/) }, { k: 'impact', t: wt(i, /convicted/) }] };
SHOT.d_missing = { set: 'DRE', light: 'indoorWarm',
  cam: i => ({ a: { pos: X(VIT, .5, 1.3, 2.4), at: X(VIT, .1, .4, 0), fov: 40 }, b: { pos: X(VIT, .3, 1.1, 1.8), at: X(VIT, .1, .4, 0), fov: 38 } }),
  upd: drUpd,
  ui: (t, i) => labelAt(X(VIT, -1.1 + 4 % 5 * .55, .6, -.3), `<div style="font:900 120px IB;color:#ffd166;text-shadow:${shadowTxt(OL, 6)}">?</div>`, t, Lt(i).start + .2, nextStart(i)) + bigText(960, 200, t, wt(i, /missing/) - .1, nextStart(i), 'STILL MISSING', 110, '#ff5d5d', -4),
  sfx: i => [{ k: 'impact', t: wt(i, /missing/) }] };
