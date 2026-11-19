// ===================== Set LOU: Mona Lisa 1911 (Louvre aussen/innen, Treppe, Wohnung, Florenz) + Louvre 2025 =====================
const LX = 800;
const LE = [LX, 0, 0], LS = [LX, 0, -80], LT = [LX + 40, 0, -80], LA = [LX, 0, 80], LF = [LX, 0, 160], L25 = [LX + 80, 0, 0];
(function louvre() {
  const S = 'LOU', ST = '#e9dcc0', ST2 = '#d6c6a4', ROOF = '#4a5a72';
  mk(S, G.box(500, .4, 500, '#c9bfa8', { base: true }), { pos: [LX, -.4, 0], outline: false, cast: false });
  // Palast-Fassade (lang, mit Mansarddach), Hof davor
  const F = [at(G.box(60, 10, 3, ST, { base: true }), [LE[0], 0, LE[2] - 6]), at(G.box(60.4, .5, 3.4, ST2, { base: true }), [LE[0], 10, LE[2] - 6]),
    at(G.box(60, 3.2, 2.2, ROOF, { base: true }), [LE[0], 10.4, LE[2] - 6.3]), at(G.box(10, 14, 4, ST, { base: true }), [LE[0], 0, LE[2] - 6]), at(G.box(10.4, 4, 3.6, ROOF, { base: true }), [LE[0], 14, LE[2] - 6.2])];
  for (let k = -12; k <= 12; k++) if (Math.abs(k) > 1) F.push(at(G.box(1.2, 2.6, .3, '#3a4458', { base: true }), [LE[0] + k * 2.3, 1.8, LE[2] - 4.4]), at(G.box(1.2, 2.6, .3, '#3a4458', { base: true }), [LE[0] + k * 2.3, 6.2, LE[2] - 4.4]));
  F.push(at(G.box(2.4, 4, .3, '#5a3a26', { base: true }), [LE[0], 0, LE[2] - 4.3]), at(G.box(1.3, 2.4, .3, '#5a3a26', { base: true }), [LE[0] + 9, 0, LE[2] - 4.3]));
  mk(S, merge(F).vary(.03, 9));
  // Baeume im Hof
  [-14, -8, 8, 14].forEach((x, k) => mk(S, merge([at(G.cyl(.2, .16, 2.4, 8, '#5a3a26'), [LE[0] + x, 0, LE[2] + 4]), at(G.ico(1.4, 2, '#5aa05a'), [LE[0] + x, 3.2, LE[2] + 4])]).smooth()));
  // Salon (innen): rote Waende, Parkett, Oberlicht
  mk(S, merge([at(G.box(24, .3, 14, '#9a6a3e', { base: true, top: '#b07a48' }), [LS[0], -.3, LS[2]]), at(G.box(24, 8, .4, '#9a3a34', { base: true }), [LS[0], 0, LS[2] - 7]),
    at(G.box(.4, 8, 14, '#8a3430', { base: true }), [LS[0] - 12, 0, LS[2]]), at(G.box(.4, 8, 14, '#8a3430', { base: true }), [LS[0] + 12, 0, LS[2]]),
    at(G.box(24, .3, .5, '#c9a23c', { base: true }), [LS[0], 6.4, LS[2] - 6.75]), at(G.box(24, .4, 14, '#efe6d0', { base: true }), [LS[0], 8, LS[2]])]), { outline: false });
  // Treppenhaus mit Tuer
  mk(S, merge([at(G.box(10, .3, 8, '#8a8070', { base: true }), [LT[0], -.3, LT[2]]), at(G.box(10, 6, .4, '#cfc4ac', { base: true }), [LT[0], 0, LT[2] - 4]),
    ...[...Array(6)].map((_, k) => at(G.box(3, .3 + k * .3, .5, '#a89c84', { base: true }), [LT[0] - 3.5, 0, LT[2] - 3.5 + k * .5])),
    at(G.box(1.6, 2.8, .2, '#5a3a26', { base: true }), [LT[0] + 1.5, 0, LT[2] - 3.75]), at(G.box(.2, .2, .2, '#c9a23c', { base: true }), [LT[0] + 2.0, 1.3, LT[2] - 3.6])]), { outline: false });
  // Wohnung (Paris): Bett, Tisch, Fenster
  mk(S, merge([at(G.box(10, .3, 8, '#8a6a4a', { base: true }), [LA[0], -.3, LA[2]]), at(G.box(10, 5, .3, '#b8b0a0', { base: true }), [LA[0], 0, LA[2] - 4]),
    at(G.box(.3, 5, 8, '#a8a090', { base: true }), [LA[0] - 5, 0, LA[2]]), at(G.box(1.4, 1.6, .1, '#9fd3f0', { base: true }), [LA[0] + 2, 2, LA[2] - 3.84]),
    at(G.box(3, .6, 1.6, '#e8e0d0', { base: true }), [LA[0] - 3.2, 0, LA[2] - 2.6])]), { outline: false });
  // Florenz: Strasse, Hotel, Kuppel im Hintergrund
  mk(S, merge([at(G.box(30, 7, 2, '#e8c89a', { base: true }), [LF[0] - 4, 0, LF[2] - 5]), at(G.box(30, .6, 2.4, '#b8784a', { base: true }), [LF[0] - 4, 7, LF[2] - 5]),
    ...[-3, -1, 1, 3].map(k => at(G.box(1.1, 1.8, .2, '#3a4458', { base: true }), [LF[0] + k * 2.6, 3.6, LF[2] - 3.95])), at(G.box(1.8, 2.8, .2, '#5a3a26', { base: true }), [LF[0] - 6, 0, LF[2] - 3.95]),
    at(G.box(5, .9, .2, '#2a4a7a', { base: true }), [LF[0] - 6, 3, LF[2] - 3.9]),
    at(G.cyl(7, 7, 12, 16, '#e8d8c0'), [LF[0] + 20, 0, LF[2] - 34]), at(G.ico(7, 3, '#c8603a', 0, 1, 1.15), [LF[0] + 20, 12, LF[2] - 34]), at(G.cyl(1.1, .8, 2.6, 10, '#e8d8c0'), [LF[0] + 20, 19.5, LF[2] - 34])]).smooth(), {});
  // Louvre 2025: Glaspyramide + Fassade (Tag)
  mk(S, merge([at(G.box(40, 9, 3, ST, { base: true }), [L25[0], 0, L25[2] - 14]), at(G.box(40, 2.6, 2.4, ROOF, { base: true }), [L25[0], 9, L25[2] - 14.3]),
    ...[-7, -5, -3, -1, 1, 3, 5, 7].map(k => at(G.box(1.2, 2.4, .3, '#3a4458', { base: true }), [L25[0] + k * 2.3, 5.2, L25[2] - 12.4]))]));
  mk(S, G.cyl(4.6, .01, 4.4, 4, '#9fd3f0'), { pos: [L25[0] - 8, 0, L25[2] - 2], rot: [0, PI / 4, 0], alpha: .7, spec: .8, emis: .15 });
})();
// Gemaelde: Portrait-Textur (stilisierte Dame vor Landschaft, Gemeinfreiheit), Mona-Lisa-Rahmen
function ladyTex() { return tex(360, 520, (x) => {
  const g = x.createLinearGradient(0, 0, 0, 520); g.addColorStop(0, '#8aa08a'); g.addColorStop(.5, '#b8a870'); g.addColorStop(1, '#5a4a2a'); x.fillStyle = g; x.fillRect(0, 0, 360, 520);
  x.fillStyle = '#6a7a5a'; x.beginPath(); x.moveTo(0, 200); x.quadraticCurveTo(80, 150, 140, 210); x.lineTo(0, 260); x.fill(); x.beginPath(); x.moveTo(360, 180); x.quadraticCurveTo(290, 150, 230, 220); x.lineTo(360, 260); x.fill();
  x.fillStyle = '#2a2018'; x.beginPath(); x.ellipse(180, 470, 150, 190, 0, PI, 0); x.fill(); x.beginPath(); x.ellipse(180, 165, 78, 110, 0, 0, 7); x.fill();
  x.fillStyle = '#d8b07a'; x.beginPath(); x.ellipse(180, 175, 52, 70, 0, 0, 7); x.fill(); x.fillRect(150, 230, 60, 60); x.beginPath(); x.ellipse(180, 320, 70, 30, 0, 0, PI); x.fill();
  x.fillStyle = '#d8b07a'; x.beginPath(); x.ellipse(170, 470, 70, 24, -.15, 0, 7); x.fill();
  x.strokeStyle = '#5a3a20'; x.lineWidth = 4; x.beginPath(); x.arc(180, 192, 18, .3, PI - .3); x.stroke(); x.fillStyle = '#3a2a1a'; x.fillRect(158, 160, 10, 6); x.fillRect(192, 160, 10, 6) }) }
const ML_W = .9, ML_H = 1.3, ML_P = [LS[0], 2.6, LS[2] - 6.75];
const ML_FRAME = mk('LOU', merge([at(G.box(ML_W + .44, .22, .2, '#c9a23c'), [0, ML_H / 2 + .11, 0]), at(G.box(ML_W + .44, .22, .2, '#c9a23c'), [0, -ML_H / 2 - .11, 0]), at(G.box(.22, ML_H, .2, '#c9a23c'), [-ML_W / 2 - .11, 0, 0]), at(G.box(.22, ML_H, .2, '#c9a23c'), [ML_W / 2 + .11, 0, 0])]), { pos: ML_P, spec: .5 });
const ML = texPlane('LOU', ML_W, ML_H, ladyTex, { pos: X(ML_P, 0, 0, .03) });
const HOOKS = mk('LOU', merge([[-.3, .8], [.3, .8], [-.3, -.8], [.3, -.8]].map(([x, y]) => at(G.box(.08, .14, .1, '#3a3a44'), [x, y, .05]))), { pos: ML_P });
// weitere Bilder an der Wand (generisch)
[[-8, 3.4, 3.2, 2.4, 'storm'], [-4.2, 3.0, 2.0, 2.6, 'pair'], [4.4, 3.0, 2.4, 2.0, 'music'], [8.2, 3.4, 2.6, 2.2, 'storm']].forEach(([dx, y, wd, ht, k]) => frame3('LOU', [LS[0] + dx, y, LS[2] - 6.75], wd, ht, k));
// Truhe in der Wohnung (Deckel klappt)
const TRUNK = [LA[0] + 1, 0, LA[2] - 1];
mk('LOU', merge([at(G.box(2, .9, 1.1, '#7a4a2a', { base: true }), TRUNK), at(G.box(2.04, .12, 1.14, '#3a2a1a', { base: true }), X(TRUNK, 0, .4, 0)), at(G.box(.2, .2, .1, '#c9a23c', { base: true }), X(TRUNK, 0, .6, .56))]));
const LIDG = new G.Geo().add(G.box(2.04, .2, 1.14, '#8a5a32', { base: true }), G.m4.compose([0, 0, .57]));
const LIDM = mk('LOU', LIDG, { pos: X(TRUNK, 0, .9, -.57) });
const ML_IN = texPlane('LOU', ML_W * .9, ML_H * .9, ladyTex, { pos: X(TRUNK, 0, .93, 0), rot: [-PI / 2, 0, 0] });
// Leiterwagen 2025
const TRUCK25 = mk('LOU', merge([at(G.box(5, 2.4, 2.4, '#e8e8ee', { base: true }), [0, .6, 0]), at(G.box(1.8, 2, 2.3, '#c0303a', { base: true }), [3.4, .6, 0]), ...[[-1.6, 1.2], [1.6, 1.2], [3.4, 1.2], [-1.6, -1.2], [1.6, -1.2], [3.4, -1.2]].map(([x, z]) => at(G.cyl(.5, .5, .3, 12, '#1b1b22'), [x, .5, z + (z > 0 ? 0 : -.3)], [PI / 2, 0, 0]))]), { pos: [L25[0] + 6, 0, L25[2] - 9] });
const LADDER25 = mk('LOU', merge([at(G.box(.12, 5, .12, '#c9ccd4'), [-.4, 2.5, 0]), at(G.box(.12, 5, .12, '#c9ccd4'), [.4, 2.5, 0]), ...[...Array(10)].map((_, k) => at(G.box(.8, .06, .08, '#8a8e9a'), [0, .3 + k * .5, 0]))]), { pos: [L25[0] + 4.6, 3, L25[2] - 9], outline: false });
const PROP_LADY = `<g transform="translate(-34,-90)"><rect x="0" y="0" width="68" height="94" rx="3" fill="#a8a070" stroke="#8a6a3a" stroke-width="5"/><ellipse cx="34" cy="94" rx="30" ry="40" fill="#2a2018"/><ellipse cx="34" cy="34" rx="16" ry="22" fill="#2a2018"/><ellipse cx="34" cy="36" rx="11" ry="15" fill="#d8b07a"/><rect x="0" y="0" width="68" height="94" rx="3" fill="none" stroke="${OL}" stroke-width="3"/></g>`;
// ---------- Kapitel #5 ----------
CHAP.push({ line: 'n5', n: 5, title: 'THE MONA LISA', year: '1911', place: '🇫🇷 Paris' });
let ML_I0 = 0;
function mlUpd(t, i) {
  const k = i - ML_I0, lift = wt(ML_I0 + 2, /lifts/) - .1, fr = wt(ML_I0 + 2, /frame/) - .2;
  ML.vis = k < 2 || (k == 2 && t < lift) || k >= 8; ML_FRAME.vis = k < 2 || (k == 2 && t < fr) || k >= 8;
  LIDM.rot = [k == 6 ? -ez(cl(t, Lt(i).start + .4, Lt(i).start + 1.4)) * 1.7 : 0, 0, 0]; ML_IN.vis = k == 6;
}
SHOT.m_louvre = { set: 'LOU', light: 'day',
  cam: i => { ML_I0 = i; return { a: { pos: [LE[0] + 16, 3, LE[2] + 22], at: [LE[0], 6, LE[2] - 6], fov: 50 }, b: { pos: [LE[0] + 6, 2.2, LE[2] + 12], at: [LE[0], 3, LE[2] - 6], fov: 46 } } },
  upd: mlUpd,
  ui: (t, i) => labelAt([LE[0], 4.6, LE[2] - 4], PILL('🚫 CLOSED – MONDAY', '#e0303a', '#fff', 44), t, wt(i, /closed/) - .1, nextStart(i)) + pillAt(960, 930 - 110, t, Lt(i).start + 2.8, nextStart(i), '📅 21 AUG 1911', '#232838', '#fff', 44),
  sfx: i => [{ k: 'pop', t: wt(i, /closed/) }] };
SHOT.m_smock = { set: 'LOU', light: 'day',
  cam: i => ({ a: { pos: [LE[0] + 9, 1.8, LE[2] + 4], at: [LE[0] + 9, 1.6, LE[2] - 4], fov: 46 }, b: { pos: [LE[0] + 9, 1.6, LE[2] + 2.4], at: [LE[0] + 9, 1.4, LE[2] - 4], fov: 44 } }),
  upd: mlUpd,
  figs: (t, i) => { const u = cl((t - Lt(i).start) / 3, 0, 1); return fig([lerp(LE[0] + 4, LE[0] + 8.6, ez(u)), 0, lerp(LE[2] + .5, LE[2] - 3.8, ez(cl(u * 1.4 - .4, 0, 1)))], 'smock', Object.assign({ mouth: 'hmm', blink: bl(t, 0), look: [4, 0] }, u < 1 ? walk(t) : {})) +
    fig([LE[0] + 11.2, 0, LE[2] - 2.6], 'guard', { mouth: 'smile', blink: bl(t, 1), look: [-5, 0], armL: [.15, .1] }) },
  ui: (t, i) => pillAt(960, 200, t, wt(i, /worker/) - .1, nextStart(i), '👕 WHITE SMOCK = STAFF', '#f2f2ea', OL, 50) + pillAt(960, 300, t, wt(i, /used/) - .1, nextStart(i), 'FORMER LOUVRE WORKER', '#2a8fd6', '#fff', 46),
  sfx: i => [{ k: 'pop', t: wt(i, /worker/) }, { k: 'ding', t: wt(i, /used/) }] };
SHOT.m_lift = { set: 'LOU', light: 'indoorWarm',
  cam: i => { const l = wt(i, /lifts/) - .3; return [
    { t0: Lt(i).start, a: { pos: [LS[0] + 5, 2.6, LS[2] + 3], at: [LS[0], 2.2, LS[2] - 6.75], fov: 48 }, b: { pos: [LS[0] + 3, 2.4, LS[2] + 1], at: [LS[0], 2.2, LS[2] - 6.75], fov: 46 } },
    { t0: l, a: { pos: [LS[0] + 1.2, 2.2, LS[2] - .6], at: [LS[0] - .4, 1.8, LS[2] - 6.6], fov: 44 }, b: { pos: [LS[0] + 1.0, 2.1, LS[2] - 1.2], at: [LS[0] - .4, 1.8, LS[2] - 6.6], fov: 42 } }] },
  upd: mlUpd,
  figs: (t, i) => { const l = wt(i, /lifts/) - .1, u = cl((t - Lt(i).start) / 3.4, 0, 1), has = t > l;
    return fig([lerp(LS[0] + 6, LS[0] - .9, ez(u)), 0, LS[2] - 5.6], 'smock', Object.assign({ mouth: has ? 'grin' : 'hmm', blink: bl(t, 0), look: [-5, -3], prop: has ? PROP_LADY : '', hR: has ? [200, 150] : null, hL: has ? [70, 150] : null }, u < 1 ? walk(t) : {})) },
  ui: (t, i) => pillAt(960, 200, t, wt(i, /vincenzo/i) - .1, wt(i, /lifts/) - .3, 'VINCENZO PERUGGIA', '#232838', '#fff', 54) + stampAt(1300, 300, t, wt(i, /frame/) - .05, 'NO FRAME', '#e0303a', 90, 6),
  sfx: i => [{ k: 'pop', t: wt(i, /vincenzo/i) }, { k: 'swish', t: wt(i, /lifts/), d: .4 }, { k: 'thud', t: wt(i, /frame/), g: .6 }] };
SHOT.m_plumber = { set: 'LOU', light: 'indoorWarm',
  cam: i => ({ a: { pos: [LT[0] + 1, 2.0, LT[2] + 4], at: [LT[0] + .8, 1.5, LT[2] - 3.5], fov: 48 }, b: { pos: [LT[0] + .8, 1.9, LT[2] + 3], at: [LT[0] + .8, 1.4, LT[2] - 3.5], fov: 46 } }),
  figs: (t, i) => { const o = wt(i, /lets/) - .1; return fig([LT[0] - .4, 0, LT[2] - 2.6], 'smock', { mouth: 'grin', blink: bl(t, 0), look: [5, 0], propL: PROP_LADY, hL: [56, 190], sweat: true }) +
    fig([LT[0] + 2.4, 0, LT[2] - 2.4], 'driver', { sw: '#2a5ab0', swd: '#1f4a90', pa: '#2a5ab0', hat: HAT.cap, mouth: 'smile', talk: tk(t, i) * 0, blink: bl(t, 1), look: [-5, 0], hR: t > o ? [214, 150] : null }) },
  ui: (t, i) => labelAt([LT[0] + 2.4, 2.2, LT[2] - 2.4], PILL('🔧 PLUMBER', '#2a5ab0', '#fff', 40), t, wt(i, /plumber/) - .1, nextStart(i)) + labelAt([LT[0] + 1.5, 3.0, LT[2] - 3.7], `<div style="font:900 64px IB;color:#ffd166;text-shadow:${shadowTxt(OL, 5)}">🔓 CLICK</div>`, t, wt(i, /lets/), nextStart(i)),
  sfx: i => [{ k: 'pop', t: wt(i, /plumber/) }, { k: 'click', t: wt(i, /lets/) + .1 }] };
SHOT.m_empty_wall = { set: 'LOU', light: 'indoorWarm',
  cam: i => ({ a: { pos: [LS[0], 2.4, LS[2] - 1.5], at: [LS[0], 2.4, LS[2] - 6.75], fov: 46 }, b: { pos: [LS[0], 2.5, LS[2] - 3.2], at: [LS[0], 2.5, LS[2] - 6.75], fov: 44 } }),
  upd: mlUpd,
  ui: (t, i) => pillAt(960, 200, t, wt(i, /next/) - .1, nextStart(i), '🕐 NEXT DAY: IT\'S GONE', '#e0303a', '#fff', 56) + labelAt(X(ML_P, 0, .2, .1), `<div style="font:900 200px IB;color:#ffd166;text-shadow:${shadowTxt(OL, 8)}">?</div>`, t, Lt(i).start + .3, nextStart(i)),
  sfx: i => [{ k: 'impact', t: wt(i, /next/), g: .5 }] };
SHOT.m_crowd = { set: 'LOU', light: 'indoorWarm',
  cam: i => { const c = wt(i, /crowds/) - .2; return [
    { t0: Lt(i).start, a: { pos: [LS[0] - 6, 2.0, LS[2] + 2], at: [LS[0] - 6, 1.6, LS[2] - 3], fov: 44 }, b: { pos: [LS[0] - 6, 1.9, LS[2] + 1], at: [LS[0] - 6, 1.5, LS[2] - 3], fov: 42 } },
    { t0: c, a: { pos: [LS[0], 3.4, LS[2] + 6.5], at: [LS[0], 2.2, LS[2] - 6.75], fov: 50 }, b: { pos: [LS[0], 3.0, LS[2] + 4.5], at: [LS[0], 2.2, LS[2] - 6.75], fov: 50 } }] },
  upd: mlUpd,
  figs: (t, i) => { const c = wt(i, /crowds/) - .2; let h = '';
    if (t < c) { h += fig([LS[0] - 7, 0, LS[2] - 3], 'sam', { sw: '#e8e8ee', swd: '#c9ccd4', pa: '#3a3a46', mid: `<rect x="56" y="170" width="88" height="8" fill="#2a5ab0"/><rect x="54" y="194" width="92" height="8" fill="#2a5ab0"/><rect x="54" y="218" width="92" height="8" fill="#2a5ab0"/>`, hat: '', mouth: 'o', blink: bl(t, 0), look: [5, 0], sweat: true });
      h += fig([LS[0] - 5, 0, LS[2] - 3], 'cop', { sw: '#2a2a44', swd: '#1e1e33', mouth: 'hmm', talk: .4 * Math.abs(Math.sin(t * 7)), blink: bl(t, 1), look: [-5, 0], hR: [210, 130] }) }
    else for (let k = 0; k < 12; k++) { const x = LS[0] - 5 + (k % 6) * 2 + G.hash(k) * .6, z = LS[2] - 2.6 + Math.floor(k / 6) * 1.6; h += fig([x, 0, z], 'sam', { sw: ['#7a4f8a', '#4f8a3c', '#b5803f', '#3f7fb5', '#8a3c3c', '#5e6a7a'][k % 6], hat: k % 3 ? '' : HAT.cap, mouth: k % 2 ? 'o' : 'hmm', blink: bl(t, k), look: [lerp(-4, 4, (k % 6) / 5) * -1, -4], bob: Math.sin(t * 2 + k) * 2 }, 1.7) }
    return h },
  ui: (t, i) => pillAt(960, 200, t, wt(i, /picasso/i) - .1, wt(i, /crowds/) - .2, '🎨 SUSPECT: PABLO PICASSO', '#232838', '#fff', 54) + pillAt(960, 200, t, wt(i, /empty/) - .1, nextStart(i), 'CROWDS CAME TO SEE… NOTHING', '#ffd166', OL, 52),
  sfx: i => [{ k: 'pop', t: wt(i, /picasso/i) }, { k: 'whoosh', t: wt(i, /crowds/) - .3, d: .5 }, { k: 'ding', t: wt(i, /empty/) }] };
SHOT.m_trunk = { set: 'LOU', light: 'indoorWarm',
  cam: i => ({ a: { pos: X(TRUNK, 3.6, 3.0, 4.4), at: X(TRUNK, 0, .6, 0), fov: 46 }, b: { pos: X(TRUNK, 1.8, 2.6, 2.6), at: X(TRUNK, 0, .7, 0), fov: 44 } }),
  upd: mlUpd,
  figs: (t, i) => fig(X(TRUNK, -1.9, 0, .4), 'smock', { sw: '#5a6a8a', swd: '#4a5a7a', mouth: 'grin', blink: bl(t, 0), look: [5, 3] }),
  ui: (t, i) => { const a = wt(i, /two/), b = a + 1.4; return counter(960, 200, t, a - .1, nextStart(i), a, b, 0, 2, v => '⏳ ' + (v < 1.95 ? (v * 12).toFixed(0) + ' MONTHS' : '2 YEARS'), '#232838', '#fff', 64) + labelAt(X(TRUNK, 0, 1.1, 0), PILL('🧳 TRUNK', '#7a4a2a', '#fff', 40), t, wt(i, /trunk/) - .1, nextStart(i)) },
  sfx: i => [{ k: 'tick', t: wt(i, /two/) }, { k: 'pop', t: wt(i, /trunk/) }] };
SHOT.m_florence = { set: 'LOU', light: 'day',
  cam: i => { const p = wt(i, /police/) - .2; return [
    { t0: Lt(i).start, a: { pos: [LF[0] - 6, 3, LF[2] + 14], at: [LF[0] + 10, 8, LF[2] - 20], fov: 54 }, b: { pos: [LF[0] - 4, 2, LF[2] + 7], at: [LF[0] - 4, 1.8, LF[2] - 3], fov: 46 } },
    { t0: p, a: { pos: [LF[0] - 6, 2.0, LF[2] + 5], at: [LF[0] - 6, 1.5, LF[2] - 3], fov: 46 }, b: { pos: [LF[0] - 6, 1.9, LF[2] + 4], at: [LF[0] - 6, 1.4, LF[2] - 3], fov: 44 } }] },
  figs: (t, i) => { const p = wt(i, /police/) - .2; let h = '';
    if (t < p) { h += fig([LF[0] - 5.2, 0, LF[2] - 2.6], 'smock', { sw: '#5a6a8a', swd: '#4a5a7a', mouth: 'grin', talk: .3 * Math.abs(Math.sin(t * 6)), blink: bl(t, 0), look: [5, 0], prop: PROP_LADY, hR: [190, 150], hL: [80, 150] });
      h += fig([LF[0] - 3.0, 0, LF[2] - 2.6], 'suit', { mouth: 'o', blink: bl(t, 1), look: [-5, 0], hR: [214, 120] }) }
    else { h += fig([LF[0] - 6.8, 0, LF[2] - 2.4], 'smock', { sw: '#5a6a8a', swd: '#4a5a7a', mouth: 'o', blink: bl(t, 0), look: [4, 0], sweat: true, armL: [2.6, .2], armR: [2.6, .2] });
      h += fig([LF[0] - 5.2, 0, LF[2] - 2.2], 'cop', { sw: '#2a2a44', swd: '#1e1e33', mouth: 'hmm', blink: bl(t, 2), look: [-5, 0], hL: [30, 140] });
      h += fig([LF[0] - 8.4, 0, LF[2] - 2.2], 'cop', { sw: '#2a2a44', swd: '#1e1e33', mouth: 'hmm', blink: bl(t, 3), look: [5, 0], hR: [170, 140] }) }
    return h },
  ui: (t, i) => { let h = pillAt(960, 200, t, wt(i, /florence/i) - .1, wt(i, /police/) - .2, '🇮🇹 FLORENCE · DEC 1913', '#2fa36b', '#fff', 50);
    h += labelAt([LF[0] - 3.0, 2.2, LF[2] - 2.6], PILL('ART DEALER', '#232838', '#fff', 38), t, wt(i, /dealer/) - .1, wt(i, /police/) - .2);
    h += stampAt(1320, 320, t, wt(i, /arrest/) - .05, 'ARRESTED', '#e0303a', 100, -8); return h },
  sfx: i => [{ k: 'pop', t: wt(i, /florence/i) }, { k: 'whoosh', t: wt(i, /police/) - .3, d: .5 }, { k: 'impact', t: wt(i, /arrest/) }] };
SHOT.m_famous = { set: 'LOU', light: 'indoorWarm',
  cam: i => ({ a: { pos: [LS[0], 2.6, LS[2] + 1], at: [LS[0], 2.4, LS[2] - 6.75], fov: 50 }, b: { pos: [LS[0], 2.6, LS[2] - 2.6], at: [LS[0], 2.6, LS[2] - 6.75], fov: 46 } }),
  upd: mlUpd,
  figs: (t, i) => { let h = ''; for (let k = 0; k < 6; k++) h += fig([LS[0] - 3 + k * 1.2, 0, LS[2] - 3.4 - (k % 2) * .6], 'sam', { sw: ['#7a4f8a', '#4f8a3c', '#b5803f', '#3f7fb5', '#8a3c3c', '#5e6a7a'][k], hat: '', mouth: 'o', blink: bl(t, k), look: [0, -5] }, 1.6); return h },
  ui: (t, i) => stampAt(1380, 280, t, wt(i, /seven/) - .05, '7 MONTHS', '#e0303a', 90, 8, wt(i, /many/) - .1) + bigText(960, 180, t, wt(i, /famous/) - .1, nextStart(i), 'THE MOST <span style="color:#ffd166">FAMOUS</span> PAINTING', 88),
  sfx: i => [{ k: 'impact', t: wt(i, /seven/), g: .5 }, { k: 'ding', t: wt(i, /famous/) }] };
SHOT.m_louvre2025 = { set: 'LOU', light: 'day',
  cam: i => ({ a: { pos: [L25[0] - 6, 4, L25[2] + 14], at: [L25[0] + 4, 5, L25[2] - 12], fov: 52 }, b: { pos: [L25[0] - 2, 3.4, L25[2] + 10], at: [L25[0] + 6, 5.5, L25[2] - 12], fov: 50 } }),
  upd: (t, i) => { const l = ez(cl((t - wt(i, /ladder/) + .2) / 1.4, 0, 1)); LADDER25.rot = [lerp(-1.45, -.8, l), 0, 0]; LADDER25.scl = [1, lerp(.35, 1, l), 1] },
  ui: (t, i) => pillAt(960, 200, t, wt(i, /2025/) - .1, nextStart(i), '📅 2025: AGAIN!', '#e0303a', '#fff', 56) + counter(960, 310, t, wt(i, /seven/) - .1, nextStart(i), wt(i, /seven/), wt(i, /minutes/) + .2, 0, 7, v => '⏱ ' + Math.max(1, Math.round(v)) + ' MIN', '#232838', '#fff', 60),
  sfx: i => [{ k: 'impact', t: wt(i, /2025/), g: .5 }, { k: 'swish', t: wt(i, /ladder/), d: .6 }, { k: 'tick', t: wt(i, /seven/) }] };
