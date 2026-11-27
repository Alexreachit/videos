// ===================== Draw =====================
let LASTSET = null;
window.setTimeline = tl => {
  MG.TL = tl; CAMS = [];
  for (let i = 0; i < NL(); i++) CAMS.push(camOf(i));
};
window.ready = false;
Promise.all(['900 40px IB', '700 40px P'].map(f => document.fonts.load(f))).then(() => { TEXQ.forEach(f => f()); window.ready = true }).catch(() => { TEXQ.forEach(f => f()); window.ready = true });
window.draw = function (t) {
  const i = lineAt(t), sh = SHOT[SPEC(i).shot] || { set: 'FY', light: 'grey' };
  showSet(sh.set); setLight((typeof sh.light == 'function' ? sh.light(t, i) : sh.light) || 'grey');
  const c = camAt(t); w.cam.pos = c.pos; w.cam.at = c.at; w.cam.fov = c.fov;
  w.shadowCenter = [c.at[0], 0, c.at[2]]; w.shadowSize = Math.min(60, 10 + Math.hypot(...G.v.sub(c.pos, c.at)) * .7);
  if (sh.upd) sh.upd(t, i);
  w.render(t);
  $('ov').innerHTML = sh.figs ? sh.figs(t, i) : '';
  let fx = '';
  const cuts = cutTimes(); let fl = 0; cuts.forEach(x => { const f = cl(t, x - .06, x + .16); if (f > 0 && f < 1) fl = Math.max(fl, Math.sin(f * PI) * .5) });
  if (fl > 0) fx += `<div style="position:absolute;inset:0;background:#fff;opacity:${fl}"></div>`;
  $('fx').innerHTML = fx;
  let ui = (sh.ui ? sh.ui(t, i) : '') + hookTitle(t);
  ui += MG.captions(t, { y: 1420, size: 104, maxWords: 2, hl: '#ffd166', stageW: 1080 }).replace(/'Arial Black',Arial/, 'IB,Arial');
  $('ui').innerHTML = ui;
};
// Hook-Text ab Frame 0 (stumm verstaendlich)
function hookTitle(t) {
  const t1 = Lt(1).start + .1; if (t > t1) return '';
  const o = fade(t, t1 - .25, t1);
  return `<div style="position:absolute;left:0;right:0;top:250px;text-align:center;opacity:${o};z-index:2350">
   <div style="display:inline-block;font:900 96px/1.04 IB,Arial;color:#fff;text-shadow:${shadowTxt(OL, 7)},0 12px 24px #0007">$12,000 TICKET<br><span style="font-size:76px">…FOR THIS</span><br><span style="color:#ffd166">CHEESE<br>SANDWICH?</span></div></div>`;
}
window.sfxEvents = function () {
  const E = [{ k: 'whoosh', t: .05, d: .8 }];
  cutTimes().forEach(x => E.push({ k: 'whoosh', t: x - .12, d: .45 }));
  for (let i = 0; i < NL(); i++) { const s = SHOT[SPEC(i).shot]; if (s && s.sfx) s.sfx(i).forEach(e => { if (isFinite(e.t)) E.push(e) }) }
  return E;
};
