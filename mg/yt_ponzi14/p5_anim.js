// ===================== Animation je Set =====================
const shadowTxt = (c = OL, r = 5) => MG.outline(r).replace(/#000/g, c);
function pop(t, t0, d = .35) { return bo(cl(t, t0, t0 + d)) }
function fade(t, t0, t1) { return 1 - ez(cl(t, t0, t1)) }
function wtN(i, re, n, d = 0) { const l = Lt(i); let c = 0; if (l.words) for (const x of l.words) if (re.test(x[0]) && ++c == n) return l.start + x[1] + d; return wt(i, re, d) }
const frac = x => x - Math.floor(x);
const arc = (a, b, u, hgt) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u) + Math.sin(u * Math.PI) * hgt, lerp(a[2], b[2], u)];
const has = (sh, ...a) => a.includes(sh);
function vis(p, v) { p.m.vis = v; p.head.vis = v; p.aL.vis = v; p.aR.vis = v }

function animST(t, sh, i, rt) {
  const qOn = has(sh, 'street_wide', 'office_door', 'bank_compare', 'word_mouth', 'street_crowd', 'bank_run', 'newspaper', 'newspaper3', 'arrest', 'newspaper2', 'newspaper_prize');
  ST.queue.forEach((p, k) => { vis(p, qOn); if (!qOn) return;
    let ps = 'idle'; if (sh == 'street_crowd') ps = 'cheer'; if (sh == 'bank_run') ps = k % 2 ? 'angry' : 'push'; if (sh == 'word_mouth') ps = k % 3 == 0 ? 'wave' : 'idle'; if (sh == 'arrest') ps = k % 2 ? 'scared' : 'angry';
    pose(p, t, ps) });
  const cOn = has(sh, 'street_crowd', 'bank_run', 'arrest', 'newspaper2', 'newspaper_prize');
  ST.crowd.forEach((p, k) => { vis(p, cOn); if (!cOn) return; let ps = sh == 'street_crowd' ? 'cheer' : sh == 'bank_run' ? (k % 2 ? 'push' : 'angry') : sh == 'arrest' ? (k % 3 ? 'angry' : 'scared') : 'idle';
    p.yaw = sh == 'arrest' ? Math.PI * .1 * (k % 2 ? 1 : -1) : (G.hash(k, 6) - .5) * .5; pose(p, t, ps);
    if (sh == 'arrest') { p.m.pos = [p.base[0] + (p.base[0] > 0 ? 1.5 : -1.5), p.m.pos[1], p.base[2] - 1] } });
  ST.banner.vis = sh != 'office_ext';
  const pz = PZ.ST, pzOn = has(sh, 'office_door', 'office_ext', 'office_sign', 'bank_run', 'arrest');
  vis(pz, pzOn);
  if (pzOn) {
    pz.base = [0, .14, 7.2]; pz.yaw = 0;
    if (sh == 'arrest') { const u = ez(cl(rt, .3, Lt(i).end - Lt(i).start)); pz.base = [0, .14, lerp(7.4, 3.6, u)]; pose(pz, t, 'walk'); pz.aL.rot = [.3, 0, -.15]; pz.aR.rot = [.3, 0, .15]; pz.head.rot = [.35, 0, 0] }
    else pose(pz, t, sh == 'office_door' || sh == 'office_sign' ? 'wave' : sh == 'bank_run' ? 'give' : 'idle');
  }
  ST.cops.forEach((c, k) => { vis(c, sh == 'arrest'); if (sh != 'arrest') return; const u = ez(cl(rt, .3, Lt(i).end - Lt(i).start)); c.base = [k ? 1 : -1, .14, lerp(7.2, 3.4, u)]; pose(c, t, 'walk') });
  ST.closed.vis = ST.closedSign.vis = sh == 'hanover_closed';
  pose(ST.newsboy, t, has(sh, 'newspaper', 'newspaper3') ? 'wave' : 'idle');
  if (has(sh, 'newspaper', 'newspaper3')) { ST.newsboy.aR.rot = [0, 0, 2.3 + .2 * Math.sin(t * 6)]; ST.newsboy.m.pos[1] = .14 + Math.abs(Math.sin(t * 5)) * .06 }
  ST.bills.forEach((b, k) => { b.vis = sh == 'bank_run'; if (!b.vis) return; const f = frac(t * .45 + k / 30), s = [0, 2.6, 7.4], e = [(G.hash(k, 1) - .5) * 10, 0, 1 + G.hash(k, 2) * 4];
    b.pos = arc(s, e, f, 2.5); b.rot = [f * 9 + k, f * 5, f * 7] });
  ST.cars[0].pos = [-30 + frac(t / 24) * 60, 0, 3.2];
}
function animHB(t, sh, i, rt) {
  const X = SETX.HB, d = Lt(i).end - Lt(i).start, u = ez(cl(rt, 0, d * .6));
  HB.ship.pos = [X + lerp(36, 4, u), -.6 + Math.sin(t * 1.3) * .06, 1]; HB.ship.rot = [Math.sin(t * 1.1) * .01, 0, Math.sin(t * .9) * .015];
  HB.smoke.forEach((s, k) => { const f = frac(t * .35 + k / 10), fx = k % 2 ? 2.6 : -2.2; s.pos = [HB.ship.pos[0] + fx + f * 3, 9.6 + f * 5, 1 + f]; const sc = .5 + f * 1.8; s.scl = [sc, sc, sc]; s.alpha = 1 - f });
  const on = rt > d * .55; vis(HB.ponzi, on); HB.case.vis = on;
  if (on) { const v = cl(rt, d * .55, d); HB.ponzi.base = [X + lerp(2.5, -2.5, v), .5, 7.8]; HB.ponzi.yaw = -Math.PI / 2; pose(HB.ponzi, t, 'walk'); HB.ponzi.aR.rot = [0, 0, .1] }
  HB.crowd.forEach(p => pose(p, t, 'idle'));
}
function animDN(t, sh, i, rt) {
  const X = SETX.DN, tf = wt(i, /fired/i, -.4), ff = cl(t, tf, tf + .7);
  DN.plates.forEach((p, k) => { const base = [X + .9, 1.12 + k * .06, 3.6]; if (ff <= 0) { p.pos = [base[0] + Math.sin(t * 4 + k) * .01, base[1], base[2]]; p.rot = [0, 0, 0]; return }
    const v = ez(ff); p.pos = [base[0] - v * (1 + G.hash(k, 1) * 2), lerp(base[1], .03, Math.min(1, v * 1.2)) + Math.sin(v * Math.PI) * .5, base[2] - v * G.hash(k, 2) * 2]; p.rot = [v * 3 * G.hash(k, 3), 0, v * 2] });
  pose(DN.ponzi, t, t > tf ? 'sad' : 'give'); if (t <= tf) { DN.ponzi.aL.rot = [-1.1 + .2 * Math.sin(t * 9), 0, -.2]; DN.ponzi.aR.rot = [-1.1 - .2 * Math.sin(t * 9), 0, .2] }
  pose(DN.boss, t, t > wt(i, /got/i, -.2) ? 'angry' : 'idle');
  DN.cust.forEach(p => pose(p, t, t > tf ? 'scared' : 'idle'));
}
function animBK(t, sh, i, rt) {
  const X = SETX.BK, crash = sh == 'bank_crash' || sh == 'silhouette_close';
  BK.queue.forEach((p, k) => pose(p, t, crash ? (k % 2 ? 'angry' : 'scared') : sh == 'bank_queue' && t > wt(i, /loved/i, -.2) ? 'cheer' : 'idle'));
  BK.closed.vis = crash;
  const fb = crash ? ez(cl(rt, .2, 1.0)) : 0; BK.banner.pos = [X, lerp(4.4, .9, fb), lerp(5.3, 4.7, fb)]; BK.banner.rot = [lerp(0, -1.35, fb), Math.PI, lerp(0, .2, fb)];
  if (sh == 'bank_crash') { const u = ez(cl(rt, .6, Lt(i).end - Lt(i).start)); BK.car.pos = [X + lerp(9, -26, u), 0, -1.2]; BK.car.rot = [0, Math.PI, 0] } else { BK.car.pos = [X + 9, 0, -1.2]; BK.car.rot = [0, 0, 0] }
  BK.bag.vis = sh == 'bank_crash';
  vis(PZ.BK, crash); if (crash) { PZ.BK.base = [X + 6.5, 0, 2.2]; PZ.BK.yaw = sh == 'silhouette_close' ? -2.6 : -2.4; pose(PZ.BK, t, 'idle'); PZ.BK.head.rot = [0, Math.sin(t * .8) * .25, 0] }
}
function animPR(t, sh, i, rt) {
  const X = SETX.PR, p = PR.ponzi; PR.num.vis = sh == 'prison' && i < 20;
  if (sh == 'prison') { p.base = [X - .4, 0, -2.4]; p.yaw = Math.PI; pose(p, t, 'idle'); p.aL.rot = [-1.4, 0, -.3]; p.aR.rot = [-1.4, 0, .3]; p.head.rot = [.25, 0, 0]; PR.num.pos = [X - .4, 1.05, -2.72] }
  else { p.base = [X + 1.2, 0, 2.2]; p.yaw = Math.PI * .1 + Math.PI; pose(p, t, 'sad'); p.yaw = 0; p.m.rot = [0, 0, 0] }
}
function animDK(t, sh, i, rt) {
  const X = SETX.DK, d = Lt(i).end - Lt(i).start;
  DK.globe.rot = [0, t * .3, .25];
  DK.env.vis = has(sh, 'desk_letter', 'desk_coupon');
  DK.coupons.forEach(c => c.vis = false); DK.stampIT.vis = DK.stampUS.vis = false; DK.coins.forEach(c => c.vis = false);
  DK.mount.vis = DK.small.vis = DK.pad.vis = DK.pencil.vis = DK.ledger.vis = false; vis(DK.ponzi, false);
  if (sh == 'desk_letter') { DK.env.pos = [X - 3, .02 + Math.max(0, .6 - rt) * 3, -1 - Math.max(0, .6 - rt) * 4]; DK.env.rot = [-Math.PI / 2, Math.PI, .12 + Math.max(0, .6 - rt)] }
  if (sh == 'desk_coupon') { const c = DK.coupons[0], u = ez(cl(rt, .1, 1.1)); c.vis = true; c.pos = [lerp(X - 3, X - .4, u), .06 + Math.sin(u * Math.PI) * 1.4, lerp(-1, .3, u)]; c.rot = [-Math.PI / 2, Math.PI, lerp(.12, -.08, u)];
    const ts = wt(i, /stamp/i, -.2), v = pop(t, ts, .4); DK.stampUS.vis = v > .01; DK.stampUS.pos = [X + 3, .06, .2]; DK.stampUS.scl = [v, v, v]; DK.stampUS.rot = [-Math.PI / 2, Math.PI, .1] }
  if (sh == 'desk_arb' || sh == 'desk_arb2') {
    DK.stampIT.vis = DK.stampUS.vis = true; DK.stampIT.pos = [X - 5, .06, 1]; DK.stampUS.pos = [X + 5, .06, 1]; DK.stampIT.scl = DK.stampUS.scl = [1, 1, 1]; DK.stampIT.rot = [-Math.PI / 2, Math.PI, -.1]; DK.stampUS.rot = [-Math.PI / 2, Math.PI, .1];
    for (let k = 0; k < 4; k++) { const c = DK.coupons[k], f = frac(t * .4 + k / 4); c.vis = true; c.pos = arc([X - 4, .1, 1], [X + 4, .1, 1], f, 2); c.rot = [-Math.PI / 2, Math.PI, f * .6 - .3]; const sc = .55; c.scl = [sc, sc, sc] }
    const n = sh == 'desk_arb2' ? 24 : Math.min(24, Math.floor(rt * 3)); DK.coins.forEach((c, k) => { c.vis = k < n; c.pos = [X + 5.6 + (k % 3) * .7 - .7, .04 + Math.floor(k / 3) * .075, -1.2 + (k % 2) * .3] });
  }
  if (sh == 'coupon_mountain' || sh == 'silhouette_close2' || sh == 'coupon_math') {
    DK.mount.vis = true; const g = sh == 'coupon_mountain' ? lerp(.15, 1, ez(cl(rt, .6, d))) : sh == 'coupon_math' ? lerp(1, 1.7, ez(cl(rt, .3, d))) : 1; DK.mount.scl = [g, g, g];
    if (sh == 'coupon_mountain') { const c = DK.coupons[0]; c.vis = true; c.pos = [X - 5.5, .06, -2]; c.rot = [-Math.PI / 2, Math.PI, .2]; c.scl = [.6, .6, .6] }
  }
  if (sh == 'coupon_math' || sh == 'coupon_math2') { DK.small.vis = true; DK.small.pos = [SETX.DK - (sh == 'coupon_math2' ? 10 : 6.5), 0, 2]; DK.mount.vis = sh == 'coupon_math' }
  if (sh == 'silhouette_close2') { vis(DK.ponzi, true); DK.ponzi.base = [X - 1.5, 0, -.2]; DK.ponzi.yaw = Math.PI + .5; pose(DK.ponzi, t, 'idle'); DK.ponzi.head.rot = [0, Math.sin(t * .6) * .3, 0] }
  if (sh == 'math_desk') { DK.pad.vis = DK.pencil.vis = true; DK.pencil.pos = [X + 2 + Math.sin(t * 5) * 1.2, .25, -2 + Math.cos(t * 3.3) * .6] }
  if (sh == 'audit') { DK.ledger.vis = true }
}
function animPY(t, sh, i, rt) {
  const X = SETX.PY, d = Lt(i).end - Lt(i).start;
  let show = [1, 1, 1, 1];
  if (sh == 'first_inv') show = [1, 0, 0, 0];
  if (sh == 'flow2' || sh == 'pyr_1') show = [1, 1, 0, 0];
  if (sh == 'pyr_2') show = [1, pop(t, wtN(i, /fifteen/i, 2, -.1), .5), 0, 0];
  if (sh == 'pyr_3') show = [1, 1, pop(t, Lt(i).start + .5, .5), pop(t, wt(i, /round/i, -.2), .5)];
  let cu = 0; if (sh == 'crash_teaser') cu = cl(rt, .2, 1.8); if (sh == 'pyr_crash') cu = cl(rt, .2, 2.4); if (sh == 'pyr_end') cu = 1;
  PY.tiers.forEach((tr, k) => { const s = show[k], v = ez(cl((cu * 1.6 - (3 - k) * .12) / .8, 0, 1)); tr.pl.vis = s > .01; tr.leg.vis = s > .01 && tr.leg._v;
    tr.pl.scl = [1, Math.max(.01, s), 1]; tr.pl.pos = [X, (tr.y - .9) * s - v * .5 * (tr.y > 0 ? 1 : 0), tr.z]; tr.pl.rot = [0, 0, v * (k % 2 ? .18 : -.18)];
    tr.leg.scl = [1, Math.max(.01, s * (1 - v)), 1] });
  PY.ppl.forEach(p => { const s = show[p.k]; vis(p, s > .01); if (s <= .01) return; const sc = p.s * Math.max(.01, s);
    let ps = 'idle'; if (sh == 'title' || sh == 'pyr_big') ps = 'cheer'; if (sh == 'first_inv' && p.k == 0) ps = 'cheer'; if (sh == 'pyr_3' && p.k == 0) ps = 'cheer'; if (sh == 'pyr_end') ps = 'sad';
    pose(p, t, ps, .6); p.m.scl = [sc, sc, sc];
    if (cu > 0) { const v = ez(cl((cu * 1.6 - (p.k) * .15 - G.hash(p.i, p.k) * .25) / .7, 0, 1)), sgn = G.hash(p.i, 9) > .5 ? 1 : -1;
      if (v > 0) { p.m.pos = [p.base[0] + (G.hash(p.i, p.k + 3) - .5) * 3 * v, Math.max(0, lerp(p.base[1], .25, v) + Math.sin(v * Math.PI) * .8), p.base[2] - v * (1.4 + G.hash(p.i, 4) * 2.5)];
        p.m.rot = [-1.45 * v, p.yaw, sgn * .5 * v]; if (sh != 'pyr_end') { p.aL.rot = [0, 0, -2.6]; p.aR.rot = [0, 0, 2.6] } } }
  });
  const pz = PY.ponzi, vz = ez(cl((cu * 1.6) / .6, 0, 1)); vis(pz, sh != 'pyr_end'); pz.base = [X, 3.6 - vz * 3.6, 1.6 + vz * 2.5]; pz.yaw = Math.PI; pose(pz, t, cu > 0 ? 'scared' : (sh == 'first_inv' || sh == 'flow2' ? 'give' : 'wave'));
  PY.ped.vis = true;
  // Muenzen
  const routes = { first_inv: [[-1, 0]], flow2: [[1, -1], [-1, 0]], pyr_1: [[1, 0]], pyr_2: [[1, 0]], pyr_3: [[2, 1], [3, 2], [1, 0]], pyr_big: [[3, 2], [2, 1], [1, 0]], title: [[3, 2], [2, 1], [1, 0]] };
  const R = cu > 0 ? null : routes[sh];
  const head = (k, j) => { if (k < 0) return [X, 5.4, 1.6]; const n = PY.N[k], tr = PY.tiers[k]; return [X + ((j % n) - (n - 1) / 2) * .78, tr.y + 1.6, tr.z] };
  PY.coins.forEach((c, j) => { c.vis = !!R && (sh != 'pyr_2' || show[1] > .9); if (!c.vis) return; const r = R[j % R.length]; if (show[Math.max(0, r[0])] < .9 || show[Math.max(0, r[1])] < .9) { c.vis = false; return }
    const f = frac(t * .55 + j * .137); c.pos = arc(head(r[0], j * 7), head(r[1], j * 3), f, 1.2); c.rot = [f * 8, f * 4, 0] });
}
function animMN(t, sh, i, rt) {
  MN.lit.forEach(m => m.vis = sh == 'mansion_night'); MN.coins.forEach(c => c.vis = false);
  pose(MN.ponzi, t, sh == 'mansion' ? 'wave' : 'idle'); pose(MN.mom, t, sh == 'mansion' && t > wt(i, /mother/i, -.2) ? 'wave' : 'idle');
  vis(MN.mom, sh == 'mansion' && t > wt(i, /mother/i, -.4));
}
function animVT(t, sh, i, rt) {
  const d = Lt(i).end - Lt(i).start, n = sh == 'money_room' ? 150 : Math.floor(150 * ez(cl(rt, .2, d)));
  VT.bricks.forEach((b, k) => { b.vis = k < n; if (k == n - 1) { const s = bo(cl(frac(rt * 3), 0, 1)); } });
  VT.bills.forEach((b, k) => { const f = frac(t * .3 + k / 60); b.pos = [SETX.VT - 6 + G.hash(k, 1) * 12 + Math.sin(t + k) * .5, 7 - f * 7, -3 + G.hash(k, 2) * 7]; b.rot = [t * 2 + k, k, t * 3 + k] });
  VT.ponzi.base = [SETX.VT + 3.2, 0, -1.2]; VT.ponzi.yaw = -.7; pose(VT.ponzi, t, 'cheer', .5);
}
function animSW(t, sh, i, rt) { pose(SW.ponzi, t, 'wave'); SW.buyers.forEach(p => pose(p, t, 'idle')); SW.gator.pos = [SETX.SW - 4 + Math.sin(t * .3) * 1.5, -.12 + Math.sin(t * 2) * .03, -3] }
function animCT(t, sh, i, rt) { pose(CT.judge, t, 'idle'); const g = frac(t * .5); CT.gavel.rot = [0, 0, g < .15 ? -Math.sin(g / .15 * Math.PI) * .9 : 0]; pose(CT.ponzi, t, 'idle'); CT.cops.forEach(c => pose(c, t, 'idle')) }
const ANIM = { ST: animST, HB: animHB, DN: animDN, BK: animBK, PR: animPR, DK: animDK, PY: animPY, MN: animMN, VT: animVT, SW: animSW, CT: animCT };
// ---------- Licht ----------
const DAY = { sunCol: w.sunCol.slice(), sky: w.sky.slice(), gnd: w.gnd.slice(), fog: w.fog.slice(), bg: 'linear-gradient(#5fb2ee 0%,#9fdcff 45%,#e6f6ff 70%)' };
const LIGHTS = {
  night: { sunCol: [.45, .55, .9], sky: [.24, .3, .52], gnd: [.12, .14, .24], fog: G.hex('#1b2c55'), bg: 'linear-gradient(#0b1633 0%,#1c2f63 55%,#33508f 80%)' },
  dusk: { sunCol: [1.15, .78, .52], sky: [.62, .55, .62], gnd: [.42, .3, .25], fog: G.hex('#f2b58a'), bg: 'linear-gradient(#5b5f9e 0%,#f08a6b 55%,#ffd29a 85%)' },
  dim: { sunCol: [.75, .8, .95], sky: [.5, .55, .7], gnd: [.3, .3, .36], fog: G.hex('#9aa3b5'), bg: 'linear-gradient(#5d6680,#9aa3b5)' },
  warm: { sunCol: [1.1, .92, .72], sky: [.85, .8, .72], gnd: [.5, .42, .32], fog: G.hex('#ffe2b8'), bg: 'linear-gradient(#ffb36b 0%,#ffd9a0 50%,#fff1d6 80%)' },
};
const SHOT_LIGHT = { mansion_night: 'night', bank_crash: 'dusk', silhouette_close: 'dusk', prison: 'dim', prison2: 'dim', rio: 'warm', pyr_end: 'dim', crash_teaser: 'dusk', pyr_crash: 'dusk' };
