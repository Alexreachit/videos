// ===================== Gemeinsame Objekte + Texturen =====================
// Gemaelde-Texturen (stilisiert, keine Kopien): Ikone auf Goldgrund (Cimabue), dunkles Barockbild (Caravaggio), triste Landschaft (Flohmarkt), Unabhaengigkeitserklaerung
function paintIcon() { return tex(512, 660, (x, wd, ht) => {
  const g = x.createLinearGradient(0, 0, wd, ht); g.addColorStop(0, '#f6d26a'); g.addColorStop(.5, '#d9a93a'); g.addColorStop(1, '#f0c450'); x.fillStyle = g; x.fillRect(0, 0, wd, ht);
  x.fillStyle = '#5a3a22'; x.fillRect(0, ht * .78, wd, ht * .22);
  // Mittelfigur mit Heiligenschein + blauem Mantel
  x.fillStyle = '#ffe9a0'; x.beginPath(); x.arc(wd / 2, ht * .3, 70, 0, 7); x.fill(); x.strokeStyle = '#a8741a'; x.lineWidth = 6; x.stroke();
  x.fillStyle = '#f1d2b0'; x.beginPath(); x.arc(wd / 2, ht * .3, 40, 0, 7); x.fill();
  x.fillStyle = '#2a4aa0'; x.beginPath(); x.moveTo(wd / 2 - 70, ht * .82); x.quadraticCurveTo(wd / 2, ht * .32, wd / 2 + 70, ht * .82); x.fill();
  x.fillStyle = '#b8323a'; x.beginPath(); x.moveTo(wd / 2 - 30, ht * .8); x.quadraticCurveTo(wd / 2, ht * .45, wd / 2 + 30, ht * .8); x.fill();
  // Seitenfiguren
  [[.16, '#7a3a8a'], [.3, '#3a7a5a'], [.7, '#9a5a2a'], [.84, '#4a5a8a']].forEach(([u, c], k) => { const cx = wd * u, cy = ht * (.42 + (k % 2) * .05);
    x.fillStyle = '#e8c8a0'; x.beginPath(); x.arc(cx, cy, 24, 0, 7); x.fill(); x.fillStyle = c; x.beginPath(); x.moveTo(cx - 40, ht * .8); x.quadraticCurveTo(cx, cy, cx + 40, ht * .8); x.fill() });
  x.strokeStyle = '#8a5a1a'; x.lineWidth = 18; x.strokeRect(9, 9, wd - 18, ht - 18);
}) }
function paintBaroque() { return tex(800, 640, (x, wd, ht) => {
  const g = x.createRadialGradient(wd * .45, ht * .4, 40, wd * .5, ht * .5, 600); g.addColorStop(0, '#9a6a40'); g.addColorStop(1, '#2a1a10'); x.fillStyle = g; x.fillRect(0, 0, wd, ht);
  x.fillStyle = '#8a1a1a'; x.beginPath(); x.moveTo(0, 0); x.lineTo(wd * .6, 0); x.quadraticCurveTo(wd * .3, ht * .2, wd * .1, ht * .45); x.lineTo(0, ht * .5); x.fill();
  [[.32, .38, '#f2d8b8'], [.58, .34, '#e8c4a0'], [.74, .42, '#c9a07a']].forEach(([u, v, c]) => { x.fillStyle = c; x.beginPath(); x.arc(wd * u, ht * v, 46, 0, 7); x.fill() });
  x.fillStyle = '#e8e0d0'; x.beginPath(); x.moveTo(wd * .48, ht * .45); x.quadraticCurveTo(wd * .6, ht * .7, wd * .52, ht); x.lineTo(wd * .78, ht); x.quadraticCurveTo(wd * .7, ht * .6, wd * .66, ht * .45); x.fill();
  x.fillStyle = '#3a2a1e'; x.fillRect(wd * .2, ht * .55, wd * .22, ht * .45);
  x.fillStyle = '#ffffff10'; for (let k = 0; k < 400; k++) x.fillRect(G.hash(k) * wd, G.hash(k, 1) * ht, 3, 3);
}) }
function paintLand() { return tex(640, 480, (x, wd, ht) => {
  x.fillStyle = '#9aa6a0'; x.fillRect(0, 0, wd, ht * .55); x.fillStyle = '#6a7458'; x.fillRect(0, ht * .55, wd, ht * .45);
  x.fillStyle = '#5a5a4a'; x.beginPath(); x.moveTo(0, ht * .6); x.quadraticCurveTo(wd * .3, ht * .35, wd * .6, ht * .58); x.quadraticCurveTo(wd * .8, ht * .45, wd, ht * .6); x.lineTo(wd, ht); x.lineTo(0, ht); x.fill();
  x.fillStyle = '#7a5a40'; x.fillRect(wd * .62, ht * .5, 70, 50); x.fillStyle = '#5a3a2a'; x.beginPath(); x.moveTo(wd * .6, ht * .5); x.lineTo(wd * .62 + 35, ht * .4); x.lineTo(wd * .62 + 80, ht * .5); x.fill();
  x.fillStyle = '#3e4a34'; [.15, .22, .85].forEach(u => { x.beginPath(); x.arc(wd * u, ht * .55, 34, 0, 7); x.fill() });
}) }
function paintDecl() { return tex(600, 760, (x, wd, ht) => {
  x.fillStyle = '#efe2c0'; x.fillRect(0, 0, wd, ht); x.fillStyle = '#e0cfa4'; for (let k = 0; k < 3; k++) x.fillRect(0, ht * (k + 1) / 4 - 2, wd, 4);
  x.fillStyle = '#2a2420'; x.textAlign = 'center'; x.font = '900 34px IB,Arial'; x.fillText('IN CONGRESS, JULY 4, 1776.', wd / 2, 64);
  x.font = '900 40px IB,Arial'; x.fillText('A DECLARATION', wd / 2, 124); x.font = '700 22px P,Arial'; x.fillText('BY THE REPRESENTATIVES OF THE', wd / 2, 160);
  x.font = '900 30px IB,Arial'; x.fillText('UNITED STATES OF AMERICA,', wd / 2, 200);
  x.fillStyle = '#4a4038'; for (let k = 0; k < 2; k++) for (let r = 0; r < 26; r++) x.fillRect(30 + k * 280, 236 + r * 19, 250 - G.hash(r, k) * 50, 7);
}) }
// Gold-Requisiten
const ringGeo = () => merge([at(G.cyl(.075, .075, .035, 20, '#f0c040', { open: true }), [0, 0, 0], [PI / 2, 0, 0]), at(G.cyl(.06, .06, .036, 20, '#d8a830', { open: true }), [0, 0, 0], [PI / 2, 0, 0]),
  at(G.ico(.06, 1, '#eaf6ff', 0, 1, .8), [0, .1, 0])]);
const coinPile = (n, r, seed = 0, col = '#ffcc44') => merge([...Array(n)].map((_, k) => { const a = G.hash(k, seed) * 6.28, d = Math.sqrt(G.hash(k, seed + 1)) * r;
  return at(G.cyl(.06, .06, .02, 10, k % 7 ? col : '#d8dde6'), [Math.cos(a) * d, .01 + (r - d) * .5 * G.hash(k, seed + 2), Math.sin(a) * d], [G.hash(k, 4) * .6, 0, G.hash(k, 5) * .6]) }));
const canGeo = () => merge([at(G.cyl(.16, .16, .36, 14, '#8a4a26'), [0, 0, 0]), at(G.cyl(.17, .17, .04, 14, '#6a3a1e'), [0, .34, 0])]);
const hammerGeo = () => merge([at(G.cyl(.03, .03, .55, 8, '#a0703a'), [0, 0, 0], [0, 0, PI / 2]), at(G.box(.08, .1, .2, '#7a7f8c', { base: true }), [.28, -.05, 0])]);
LOOK.auctioneer = { sw: '#2a2f45', swd: '#20243a', pa: '#20243a', mid: MID.tie };
LOOK.lady = { sw: '#c0508a', swd: '#a03a70', pa: '#3a3f55', hat: `<path d="M44,60 Q30,0 100,-2 Q170,0 156,60 Q150,30 100,26 Q50,30 44,60Z" fill="#7a4a2a" stroke="${OL}" stroke-width="5"/>` };
LOOK.bidder = { sw: '#4a6a8a', swd: '#3a5a78', pa: '#2c3044', mid: MID.tie };
LOOK.bidder2 = { sw: '#8a4a5a', swd: '#723a4a', pa: '#2c3044' };
LOOK.bidder3 = { sw: '#5a7a4a', swd: '#4a6a3a', pa: '#3a3f55', hat: HAT.grey };
LOOK.expert = { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', mid: MID.tie, hat: `<circle cx="78" cy="96" r="20" fill="none" stroke="${OL}" stroke-width="6"/><circle cx="124" cy="96" r="20" fill="none" stroke="${OL}" stroke-width="6"/><path d="M98,96 L104,96" stroke="${OL}" stroke-width="6"/>` };
PROP.gavel = a => `<g transform="rotate(${a})"><rect x="-5" y="-46" width="10" height="52" rx="4" fill="#8a5a32" stroke="${OL}" stroke-width="4"/><rect x="-22" y="-62" width="44" height="22" rx="7" fill="#6a3a1e" stroke="${OL}" stroke-width="5"/></g>`;
PROP.paddle = n => `<g transform="translate(-4,-10)"><rect x="-4" y="-6" width="8" height="40" fill="#8a5a32" stroke="${OL}" stroke-width="3"/><circle cx="0" cy="-30" r="26" fill="#fff" stroke="${OL}" stroke-width="5"/><text x="0" y="-21" text-anchor="middle" font-family="IB,Arial" font-weight="900" font-size="26" fill="${OL}">${n}</text></g>`;
// ===================== Set AUC: Auktionssaal (Sotheby's/Senlis) + Los-Tisch fuer Liste/Outro =====================
const AX = -600, AU = [AX, 0, 0];
(function auc() {
  const S = 'AUC';
  mk(S, merge([at(G.box(26, .3, 24, '#6a4630', { base: true, top: '#7a5236' }), [AX, -.3, 0]), at(G.box(26, 10, .4, '#7a2a34', { base: true }), [AX, 0, -8]),
    at(G.box(.4, 10, 24, '#6e2630', { base: true }), [AX - 13, 0, 0]), at(G.box(.4, 10, 24, '#6e2630', { base: true }), [AX + 13, 0, 0]),
    at(G.box(26, .5, .5, '#e8c060', { base: true }), [AX, 6.6, -7.7]), at(G.box(26, .1, .3, '#e8c060', { base: true }), [AX, 1.2, -7.75]),
    ...[-10, -5, 5, 10].map(x => at(G.box(.9, 10, .6, '#5a1e26', { base: true }), [AX + x, 0, -7.6])),
    at(G.box(6, .05, 14, '#3a2a5a', { base: true }), [AX, 0, 3]),
    // Podium + Staffelei
    at(G.box(1.5, 1.3, 1, '#4a3020', { base: true }), [AX - 4.6, 0, -4]), at(G.box(1.6, .1, 1.1, '#e8c060', { base: true }), [AX - 4.6, 1.3, -4]),
    at(G.box(.08, 2.4, .08, '#6a4428', { base: true }), [AX - .6, 0, -5]), at(G.box(.08, 2.4, .08, '#6a4428', { base: true }), [AX + .6, 0, -5]), at(G.box(1.5, .08, .25, '#6a4428', { base: true }), [AX, 1.2, -4.95]),
    // Bildschirm
    at(G.box(5.4, 3, .15, '#14182a', { base: true }), [AX + 6, 2.6, -7.7])]), { outline: false });
  // Stuhlreihen (Publikum schaut nach -z)
  const C = []; for (let r = 0; r < 4; r++) for (let k = 0; k < 8; k++) { const x = AX - 4.9 + k * 1.4, z = r * 1.7;
    C.push(at(G.box(.7, .08, .6, '#b8323a', { base: true }), [x, .55, z]), at(G.box(.7, .8, .08, '#9a2a30', { base: true }), [x, .6, z + .3]), at(G.box(.06, .55, .06, '#e8c060', { base: true }), [x - .3, 0, z - .25]), at(G.box(.06, .55, .06, '#e8c060', { base: true }), [x + .3, 0, z - .25])) }
  mk(S, merge(C));
  // Kronleuchter
  [-5, 5].forEach(x => { mk(S, merge([at(G.cyl(.04, .04, 1.4, 6, '#c9a23c'), [AX + x, 7.2, 1]), at(G.cyl(.9, .3, .3, 14, '#e8c060'), [AX + x, 7, 1])]), { outline: false });
    mk(S, merge([0, 1, 2, 3, 4, 5].map(k => at(G.ico(.12, 1, '#fff2c0'), [AX + x + Math.cos(k) * .75, 7.3, 1 + Math.sin(k) * .75]))), { emis: 1, outline: false, cast: false }) });
  // Los-Tisch (Liste)
})();
const LOTT = mk('AUC', merge([at(G.box(10, .12, 1.4, '#f4efe2', { base: true }), [0, 1.0, 0]), at(G.box(9.8, 1.0, 1.3, '#2a3a5a', { base: true }), [0, 0, 0])]), { pos: [AX, 0, -2], outline: false });
// 6 Lose: Ring, Rahmen-Gemaelde, Dose, Hammer, grosses Gemaelde, kleine Ikone
const LOTX = [-3.9, -2.35, -.8, .8, 2.35, 3.9].map(x => AX + x);
const LOTS = [
  mk('AUC', merge([at(G.box(.4, .3, .4, '#2a2a3a', { base: true }), [0, 0, 0]), at(G.box(.42, .05, .42, '#f4efe2', { base: true }), [0, .3, 0])]), { pos: [LOTX[0], 1.12, -2] }),
  mk('AUC', G.box(.9, .7, .08, '#b88a3a', { base: true }), { pos: [LOTX[1], 1.12, -2.2], rot: [-.25, 0, 0] }),
  mk('AUC', canGeo(), { pos: [LOTX[2], 1.12, -2] }),
  mk('AUC', hammerGeo(), { pos: [LOTX[3], 1.2, -2], rot: [0, .6, 0] }),
  mk('AUC', G.box(1.2, .95, .06, '#3a2a1e', { base: true }), { pos: [LOTX[4], 1.12, -2.3], rot: [-.2, 0, 0] }),
  mk('AUC', G.box(.4, .52, .05, '#a8741a', { base: true }), { pos: [LOTX[5], 1.12, -2.1], rot: [-.2, 0, 0] })];
const LRING = mk('AUC', ringGeo(), { pos: [LOTX[0], 1.5, -2], spec: 1, emis: .15, outline: false });
const LTEX = [[1, .78, .6, paintLand, -2.16], [4, 1.08, .84, paintBaroque, -2.26], [5, .34, .44, paintIcon, -2.07]].map(([j, wd, ht, f, z]) => texPlane('AUC', wd, ht, f, { pos: [LOTX[j], 1.12 + ht / 2 + .05, z + .05], rot: [-.2, 0, 0] }));
// Exponat auf der Staffelei (wechselt): 0=Ring-Kissen, 1=Erklaerung, 2=Ikone
const EAS = [mk('AUC', merge([at(G.box(.7, .5, .5, '#2a2a3a', { base: true }), [0, 0, 0]), at(G.box(.72, .06, .52, '#b8323a', { base: true }), [0, .5, 0])]), { pos: [AX, 1.25, -4.95] }),
  texPlane('AUC', .9, 1.14, paintDecl, { pos: [AX, 1.9, -4.86], rot: [-.08, 0, 0] }),
  texPlane('AUC', .5, .64, paintIcon, { pos: [AX, 1.66, -4.86], rot: [-.08, 0, 0] })];
const ERING = mk('AUC', ringGeo(), { pos: [AX, 1.95, -4.95], spec: 1, emis: .2, outline: false, scl: [1.6, 1.6, 1.6] });
const EFRAME = mk('AUC', G.box(.66, .8, .04, '#c9a23c', { base: true }), { pos: [AX, 1.25, -4.9], outline: true });
function aucUpd(t, i, ex = -1, lots = false) {
  LOTT.vis = lots; LOTS.forEach(m => m.vis = lots); LRING.vis = lots; LTEX.forEach(m => m.vis = lots); LRING.rot = [0, t * .8, 0];
  EAS.forEach((m, j) => m.vis = j == ex); ERING.vis = ex == 0; ERING.rot = [.3, t * .7, 0]; EFRAME.vis = ex == 2;
}
// Publikum (sitzend, Beine abgeschnitten) – nur, wenn die Kamera zum Publikum schaut
const AUD = [[0, 1, 'bidder'], [0, 3, 'lady'], [0, 6, 'bidder2'], [1, 0, 'bidder3'], [1, 2, 'bidder'], [1, 4, 'bidder2'], [1, 7, 'lady'], [2, 1, 'bidder3'], [2, 3, 'bidder2'], [2, 5, 'bidder'], [3, 2, 'lady'], [3, 6, 'bidder3']];
function seatFig(p, who, o) { const h = fig(p, who, o); return h ? h.replace('<div style="position:absolute;', '<div style="position:absolute;clip-path:inset(0 0 33% 0);') : '' }
function audience(t, i, paddles = 0) {
  let h = ''; AUD.forEach(([r, k, who], j) => { const up = paddles && j % 3 == (Math.floor(t * 1.5) % 3);
    h += seatFig([AX - 4.9 + k * 1.4, .02, r * 1.7 - .05], who, { mouth: up ? 'o' : 'smile', blink: bl(t, j), look: [0, -3], hR: up ? [175, 30] : null, prop: up ? PROP.paddle(10 + j * 7) : null }) });
  return h;
}
function screenPrice(t, t0, t1, html, col = '#ffd166') { return labelAt([AX + 6, 1.4, -7.55], `<div style="width:520px;height:270px;display:flex;align-items:center;justify-content:center;font:900 76px/1 IB,Arial;color:${col};text-shadow:0 0 18px ${col}88">${html}</div>`, t, t0, t1) }
const auctioneer = (t, i, k = 0) => fig([AX - 4.6, .15, -4.4], 'auctioneer', { mouth: 'grin', talk: tk(t, i) * .3, blink: bl(t, k), look: [4, 0], prop: PROP.gavel(-30 + 40 * Math.max(0, Math.sin(t * 5)) ** 8), hR: [190, 110] });
// Kameras im Saal
const CAM_AUD = [cm([AX + 2.6, 3.2, -4.2], [AX - .4, 1.1, 3.5], 52), cm([AX + 1.6, 3, -3.8], [AX - .4, 1.1, 3.5], 50)];     // vom Podium auf das Publikum
const CAM_POD = [cm([AX + 1.2, 3.2, 6.4], [AX + .6, 2.2, -5], 58), cm([AX + 1, 3, 5.2], [AX + .6, 2.2, -5], 56)];  // aus dem Saal auf Podium + Staffelei
// ---------- Liste / Outro ----------
const LOTN = [['💍', 'A £10 RING', 6], ['🖼️', 'A $4 PAINTING', 5], ['🥫', 'A RUSTY CAN', 4], ['🔨', 'A LOST HAMMER', 3], ['🏚️', 'A LEAKY ATTIC', 2], ['🍳', 'THE KITCHEN', 1]];
function lotUI(t, ts, hi = 0) {
  let h = ''; LOTN.forEach(([ic, tx, n], j) => { const a = ts[j]; if (a == null || t < a) return; const q = w.project([LOTX[j], 2.35 + (j == 4 ? .3 : 0), -2]); if (!q.vis) return;
    h += `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%) scale(${pop(t, a)});transform-origin:50% 100%;z-index:2100">${PILL(ic + ' #' + n, n == hi ? '#ffd166' : '#232838', n == hi ? OL : '#fff', 38)}</div>` });
  return h;
}
SHOT.list = { set: 'AUC', light: 'indoorWarm',
  cam: i => mv(cm([AX, 4.2, 5.4], [AX, 1.4, -2], 50), cm([AX, 3.6, 4.4], [AX, 1.4, -2], 48)),
  upd: (t, i) => aucUpd(t, i, -1, true),
  figs: (t, i) => fig([AX + 5.6, 0, -1.2], 'sam', { mouth: 'o', talk: tk(t, i) * .7, blink: bl(t, 0), look: [-5, 2], hR: [200, 100] }),
  ui: (t, i) => lotUI(t, [5, 4, 3, 2, 1, 0].map(k => wt(i, /five/) + k * .2), 1) + bigText(960, 150, t, wt(i, /number/) - .1, nextStart(i), '#1 = THE KITCHEN', 80, '#ffd166'),
  sfx: i => [{ k: 'impact', t: wt(i, /number/), g: .5 }, ...[0, 1, 2, 3, 4, 5].map(j => ({ k: 'pop', t: wt(i, /five/) + j * .2 }))] };
SHOT.list2 = { set: 'AUC', light: 'indoorWarm',
  cam: i => { const tt = [/ring/, /four/, /rusty/, /hammer/, /leaky/].map(r => wt(i, r) - .1), C = [];
    tt.forEach((x, j) => { const p = [LOTX[j], 1.4, -2]; C.push({ t0: j ? x : Lt(i).start, a: cm(X(p, .3, .9, 2.6), X(p, 0, .1, 0), 40), b: cm(X(p, -.2, .8, 2.2), X(p, 0, .1, 0), 38) }) });
    return C },
  upd: (t, i) => aucUpd(t, i, -1, true),
  ui: (t, i) => { const R = [/ring/, /four/, /rusty/, /hammer/, /leaky/]; let k = 0; R.forEach((r, j) => { if (t >= wt(i, r) - .1) k = j });
    return pillAt(960, 200, t, wt(i, R[k]) - .05, nextStart(i), LOTN[k][0] + ' ' + LOTN[k][1], '#232838', '#fff', 60) },
  sfx: i => [/ring/, /four/, /rusty/, /hammer/, /leaky/].map(r => ({ k: 'pop', t: wt(i, r) })) };
SHOT.outro = { set: 'AUC', light: 'indoorWarm',
  cam: i => mv(cm([AX + 1, 4.4, 6.4], [AX + .6, 1.6, -2], 52), cm([AX + 1, 4, 5.6], [AX + .6, 1.6, -2], 50)),
  upd: (t, i) => aucUpd(t, i, -1, true),
  figs: (t, i) => fig([AX + 5.6, 0, -1.2], 'sam', { mouth: 'grin', talk: tk(t, i) * .8, blink: bl(t, 0), look: [-5, 2], hR: [214, 90 + 10 * Math.sin(t * 4)] }),
  ui: (t, i) => lotUI(t, [0, 1, 2, 3, 4, 5].map(k => Lt(i).start + .1 + k * .08)) + bigText(960, 150, t, Lt(i).start + .2, 1e9, 'WHICH FIND WOULD YOU PICK? 💬', 78) + pillAt(960, 270, t, wt(i, /subscribe/) - .1, 1e9, '🔔 SUBSCRIBE', '#e0303a', '#fff', 60),
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'ding', t: wt(i, /subscribe/) }] };
