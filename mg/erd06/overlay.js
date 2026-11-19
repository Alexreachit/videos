// ======================= BIS ZUM ERDKERN – Tag 4 (realistisch): Overlays ueber Blender-Bildern =======================
const Lt = i => MG.L(i);
function wt(i, re) { const l = Lt(i); if (!l.words) return l.start; for (const x of l.words) if (re.test(x[0])) return l.start + x[1]; return l.start }
const pop = (t, t0, d = .35) => bo(cl(t, t0, t0 + d)), fade = (t, t0, t1) => 1 - ez(cl(t, t0, t1));
const SH = (r = 4, c = 'rgba(0,0,0,.85)') => `0 0 ${r}px ${c},0 ${r / 2}px ${r * 2}px ${c}`;
const PINK = '#ff4fb3', ORANGE = '#ff8a1e', GREEN = '#3ee08f', RED = '#ff4a3d', GOLD = '#ffd23f', DIA = '#8fe6ff';
const fr = t => Math.max(0, Math.min(TT.nf - 1, Math.round(t * TT.fps)));
const anc = (k, t) => ANCH[k][MAP[fr(t)]];
const inSpace = t => t >= TT.space && t < TT.back;
const fmtDepth = d => d >= 10000 ? (d / 1000).toFixed(1).replace('.', ',') + ' km' : d >= 100 ? Math.round(d).toLocaleString('de-DE') + ' m' : d.toFixed(1).replace('.', ',') + ' m';
let lastBg = -1;
async function setBg(t) {
  const f = fr(t); if (f === lastBg) return; lastBg = f;
  const im = $('bg'); im.src = 'bg/' + String(MAP[f]).padStart(5, '0') + '.jpg'; try { await im.decode() } catch (e) { }
}
function tagAt(p, html, s) { if (!p || s <= .01) return ''; return `<div style="position:absolute;left:${p[0]}px;top:${p[1]}px;transform:translate(-50%,-100%) scale(${s});transform-origin:50% 100%">${html}</div>` }
function dayTag(t) {
  const s = pop(t, .05, .4) * fade(t, Lt(1).start - .2, Lt(1).start + .1); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:430px;transform:translateX(-50%) scale(${s});padding:18px 44px 22px;text-align:center">
    <div style="font-size:40px;letter-spacing:6px;color:${ORANGE}">BIS ZUM ERDKERN</div><div style="font-size:128px;line-height:1">TAG 4</div></div>`;
}
// Arbeiter- und Tiefen-Anzeige
const desc = t => t > TT.d0 && t < TT.d1 + .6;
function hud(t) {
  if (inSpace(t)) return '';
  const hide = (t > Lt(2).start - .15 && t < Lt(3).start - .1) || (t > Lt(3).start && t < TT.d0) || (t > TT.up - .05 && t < TT.back + .3);
  const tn = wt(0, /750/) - .25, n = Math.round(lerp(666, 750, ez(cl((t - tn) / 1.1, 0, 1)))), bumpN = t > tn + 1 && t < tn + 1.4 ? 1 + .2 * Math.sin((t - tn - 1) / .4 * Math.PI) : 1;
  const d = TT.depth[MAP[fr(t)]], s = pop(t, .3, .4) * (hide ? 0 : 1); if (s <= .01) return '';
  const D = desc(t);
  return `<div class="glass" style="left:34px;top:190px;transform:scale(${s * (D ? 0 : 1) * bumpN});transform-origin:0 0;padding:14px 28px 16px">
      <div class="sub" style="font-size:28px">ARBEITER</div><div style="font-size:84px;line-height:1">👷 ${n}</div></div>
    <div class="glass" style="${D ? 'left:50%;transform:translateX(-50%) scale(' + s * 1.35 + ');transform-origin:50% 0' : 'right:34px;transform:scale(' + s + ');transform-origin:100% 0'};top:190px;padding:14px 28px 16px;text-align:${D ? 'center' : 'right'};min-width:${D ? 430 : 0}px">
      <div class="sub" style="font-size:28px">TIEFE</div><div style="font-size:84px;line-height:1;color:${D ? ORANGE : '#fff'}">${fmtDepth(d)}</div>
      <div class="sub" style="font-size:26px;margin-top:4px">Ziel: 6.370 km</div></div>`;
}
function calcCard(t) {
  const t0 = Lt(2).start - .05, t1 = Lt(3).start - .15, s = pop(t, t0, .35) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  const r = (re, html) => { const p = pop(t, wt(2, re) - .25, .35); return `<div style="display:flex;align-items:center;gap:22px;margin-top:12px;opacity:${.15 + .85 * Math.min(1, p)};transform:scale(${.7 + .3 * p});transform-origin:0 50%">${html}</div>` };
  const ic = e => `<div style="width:92px;height:92px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 52px/92px IB,Arial;text-align:center">${e}</div>`;
  const tot = pop(t, wt(2, /^59/) - .2, .4);
  return `<div class="glass" style="left:50%;top:190px;width:900px;transform:translateX(-50%) scale(${s});padding:20px 34px 26px">` +
    r(/^49/, ic('❤️') + `<div style="font-size:56px">49 Likes <span class="sub" style="font-size:40px">× 1 =</span> 49</div>`) +
    r(/^2$/, ic('↗️') + `<div style="font-size:56px">2 Shares <span class="sub" style="font-size:40px">× 5 =</span> 10</div>`) +
    `<div style="height:3px;background:rgba(255,255,255,.3);margin:18px 0 10px"></div>
     <div style="text-align:center;transform:scale(${.6 + .4 * tot});opacity:${Math.min(1, tot)}"><div style="font-size:96px;line-height:1;color:${ORANGE}">59 Schaufeln</div><div class="sub">pro Arbeiter</div></div></div>`;
}
function newestFollower(t) {
  const l = Lt(1); if (t < l.start - .1 || t > Lt(2).start) return '';
  const p = anc('fosa', t); if (!p) return '';
  const s = pop(t, l.start, .45) * fade(t, Lt(2).start - .25, Lt(2).start), X = p[0], Y = p[1] + 70;
  const pulse = 1 + .08 * Math.sin(t * 9), ring = pop(t, wt(1, /fosa/i) - .25, .4), TX = 540, TY = Y + 330;
  return `<div style="position:absolute;left:${X}px;top:${Y}px;width:150px;height:240px;transform:translate(-50%,-50%) scale(${ring * pulse});border:7px solid ${GOLD};border-radius:50%;box-shadow:0 0 30px ${GOLD}, inset 0 0 20px rgba(255,210,63,.5);opacity:${Math.min(1, s)}"></div>
    <svg width="1080" height="1920" style="position:absolute;left:0;top:0;opacity:${Math.min(1, ring * s)}"><line x1="${X}" y1="${Y + 125}" x2="${TX}" y2="${TY}" stroke="${GOLD}" stroke-width="6"/></svg>
    <div class="glass" style="left:${TX}px;top:${TY}px;transform:translate(-50%,0) scale(${s});transform-origin:50% 0;padding:14px 32px 18px;text-align:center;border-color:${GOLD}">
      <div class="sub" style="font-size:28px;color:${GOLD}">NEUESTER ARBEITER</div>
      <div style="font-size:76px;line-height:1.05;margin-top:4px">fosa</div></div>`;
}
// Meilensteine beim Abstieg
function dayCard(t) {
  const t0 = wt(4, /heute/i) - .15, t1 = TT.up - .15, s = pop(t, t0, .4) * fade(t, t1, t1 + .15); if (s <= .01) return '';
  const g = pop(t, wt(4, /mehr/i) - .2, .4);
  return `<div class="glass" style="left:50%;top:560px;width:900px;transform:translateX(-50%) scale(${s});padding:20px 30px 24px;text-align:center">
    <div style="display:flex;justify-content:center;gap:50px;font-size:44px"><div><div class="sub" style="font-size:28px">gestern</div>80,9 km</div><div><div class="sub" style="font-size:28px">heute</div><span style="color:${ORANGE}">4,5 km</span></div></div>
    <div style="font-size:64px;margin-top:14px;opacity:${Math.min(1, g)};transform:scale(${.7 + .3 * g})">❤️ Mehr Likes = mehr Tiefe!</div>
    <div class="sub" style="font-size:26px;margin-top:6px">749 × 59 × 10 cm + Blake 59 × 1 m · gesamt 86,1 km</div></div>`;
}
function blakeShovel(t) {
  const t0 = Lt(3).start - .05, t1 = TT.d0 - .2, s = pop(t, t0, .4) * fade(t, t1, t1 + .15); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;width:900px;transform:translateX(-50%) scale(${s});padding:18px 30px 22px;text-align:center;border-color:${DIA}">
    <div class="sub" style="color:${DIA}">HEUTE ZUM ERSTEN MAL</div><div style="font-size:72px;line-height:1.1">💎 Blakes Diamantschaufel</div>
    <div style="display:flex;justify-content:center;gap:40px;margin-top:14px;font-size:46px;opacity:${Math.min(1, pop(t, wt(3, /zehnmal/i) - .2, .4))}">
      <div><div class="sub" style="font-size:28px">normal</div>10 cm</div><div style="color:${DIA}"><div class="sub" style="font-size:28px;color:${DIA}">Blake</div>1 m</div></div>
    <div class="sub" style="font-size:28px;margin-top:8px">pro Schaufel</div></div>`;
}
function lenaCard(t) {
  const t0 = TT.up + .05, t1 = TT.space - .3, s = pop(t, t0, .4) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;width:880px;transform:translateX(-50%) scale(${s});padding:20px 26px;display:flex;align-items:center;gap:22px;border-color:${PINK}">
    <div style="width:96px;height:96px;flex:none;border-radius:50%;background:rgba(255,79,179,.2);font:900 56px/96px IB,Arial;text-align:center">🩷</div>
    <div><div class="sub">Top-Kommentar von <b style="color:${PINK}">Lena</b></div><div style="font:800 46px P,Arial">Wunsch: pinker Helm ✔</div></div></div>`;
}
function workerTags(t) {
  let h = '';
  if (t > TT.up && t < TT.space) h += tagAt(anc('lena', t), `<div class="tag" style="font-size:44px;background:${PINK}">🩷 LENA</div>`, pop(t, wt(5, /lena/i) - .1, .4));
  if (t > TT.back) { h += tagAt(anc('blake', t), `<div class="tag" style="font-size:36px;background:#1a8fb0">💎 BLAKE</div>`, pop(t, TT.back + .3, .4));
    h += tagAt(anc('lena', t), `<div class="tag" style="font-size:36px;background:${PINK}">🩷 LENA</div>`, pop(t, TT.back + .45, .4)); }
  return h;
}
function earthUI(t) {
  if (!inSpace(t)) return '';
  const pin = anc('pin', t), cen = anc('center', t); let h = '';
  const sp = pop(t, TT.space + .25, .4);
  if (pin && sp > .01) h += `<div style="position:absolute;left:${pin[0]}px;top:${pin[1]}px;transform:translate(-50%,-50%) scale(${sp})"><div style="width:30px;height:30px;border-radius:50%;background:${RED};border:5px solid #fff;box-shadow:0 0 24px ${RED}"></div></div>`
    + `<div class="glass" style="left:${pin[0] + 34}px;top:${pin[1] + 10}px;transform:translate(0,-50%) scale(${sp});transform-origin:0 50%;padding:8px 20px 10px;text-align:left"><div style="font-size:40px">WIR</div><div class="sub" style="font-size:28px">86,1 km tief</div></div>`;
  const dl = cl((t - TT.zoomEnd + .1) / .9, 0, 1);
  if (pin && cen && dl > 0) { const x = lerp(pin[0], cen[0], dl), y = lerp(pin[1], cen[1], dl);
    h += `<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><line x1="${pin[0]}" y1="${pin[1]}" x2="${x}" y2="${y}" stroke="#fff" stroke-width="7" stroke-dasharray="18 12" stroke-linecap="round"/><circle cx="${pin[0]}" cy="${pin[1]}" r="4" fill="${ORANGE}"/></svg>`; }
  const no = cl((t - TT.zoomEnd - .8) / .5, 0, 1); if (no > 0) h += `<div class="lbl" style="left:0;width:1080px;top:1720px;font:700 26px P,Arial;color:rgba(255,255,255,.6);opacity:${no}">Erdbild: NASA · Schichten vereinfacht</div>`;
  return h;
}
function restCard(t) {
  const s = pop(t, wt(6, /fehlen/i) - .2, .4) * fade(t, TT.back - .15, TT.back); if (s <= .01 || !inSpace(t)) return '';
  return `<div class="glass" style="left:50%;top:190px;transform:translateX(-50%) scale(${s});padding:14px 44px 18px;text-align:center"><div class="sub">es fehlen noch über</div><div style="font-size:120px;line-height:1;color:${ORANGE};white-space:nowrap">6.283 km</div></div>`;
}
function upgradeCard(t) {
  const t0 = Lt(7).start - .05, t1 = Lt(8).start - .1, s = pop(t, t0, .4) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:1110px;width:880px;transform:translateX(-50%) scale(${s});padding:20px 26px;display:flex;align-items:center;gap:22px;border-color:${GOLD}">
    <div style="width:96px;height:96px;flex:none;border-radius:50%;background:rgba(255,210,63,.18);font:900 56px/96px IB,Arial;text-align:center">🏆</div>
    <div><div class="sub">jeden Tag</div><div style="font:900 56px IB,Arial">Top-Kommentar = <span style="color:${GOLD}">Upgrade</span></div></div></div>`;
}
function commentCard(t) {
  const t0 = Lt(8).start - .05, s = pop(t, t0, .45); if (t < t0) return '';
  const txt = 'Schreib es in die Kommentare', n = Math.floor(cl((t - wt(8, /schreib/i) + .1) / 1.2, 0, 1) * txt.length);
  return `<div class="glass" style="left:50%;top:1110px;width:880px;transform:translateX(-50%) scale(${s});padding:20px 26px;display:flex;align-items:center;gap:22px">
    <div style="width:96px;height:96px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 56px/96px IB,Arial;text-align:center">⛏️</div>
    <div><div class="sub">Was brauchen wir als Nächstes?</div><div style="font:800 44px P,Arial">${txt.slice(0, n)}<span style="opacity:${Math.sin(t * 10) > 0 ? 1 : 0}">|</span></div></div></div>`;
}
function flash(t) {
  let a = Math.max(1 - Math.abs(t - TT.back) / .18, 1 - Math.abs(t - TT.up) / .18, 1 - Math.abs(t - TT.d0) / .18);
  if (t > TT.space - .45 && t < TT.space) a = Math.max(a, ez((t - TT.space + .45) / .45)); if (t >= TT.space) a = Math.max(a, 1 - (t - TT.space) / .22);
  return a > 0 ? `<div style="position:absolute;inset:0;background:#fff;opacity:${Math.min(1, Math.max(0, a)) * .92}"></div>` : '';
}
window.setTimeline = tl => { MG.TL = tl };
window.draw = async function (t) {
  await setBg(t);
  $('ov').innerHTML = workerTags(t) + earthUI(t) + newestFollower(t);
  let ui = dayTag(t) + hud(t) + calcCard(t) + dayCard(t) + blakeShovel(t) + lenaCard(t) + restCard(t) + upgradeCard(t) + commentCard(t);
  ui += MG.captions(t, { y: 1500, size: 80, maxWords: 3, hl: '#ffb347', upper: true, stageW: 1080 }).replace(/'Arial Black',Arial/, 'IB,Arial');
  $('ui').innerHTML = ui; $('fx').innerHTML = flash(t);
};
window.sfxEvents = function () {
  const E = [], L = Lt;
  E.push({ k: 'whoosh', t: .05, d: 1.4 }, { k: 'chime', t: .3 });
  for (let x = .5; x < TT.d0; x += .55) E.push({ k: 'thud', t: x, g: .22 });
  const tn = wt(0, /750/) - .25; for (let k = 0; k < 8; k++) E.push({ k: 'pop', t: tn + k * .12, g: .4 }); E.push({ k: 'bell', t: tn + 1.1 });
  E.push({ k: 'pop', t: wt(1, /fosa/i) - .25 }, { k: 'chime', t: wt(1, /fosa/i) });
  E.push({ k: 'swish', t: L(2).start, d: .4 }, { k: 'pop', t: wt(2, /^49/) - .25 }, { k: 'pop', t: wt(2, /^2$/) - .25 }, { k: 'chime', t: wt(2, /^59/) - .2 });
  E.push({ k: 'chime', t: L(3).start + .1 }, { k: 'pop', t: wt(3, /zehnmal/i) - .2 });
  E.push({ k: 'impact', t: TT.d0 }, { k: 'whoosh', t: TT.d0 + .05, d: TT.d1 - TT.d0 }, { k: 'impact', t: TT.d1 - .05 }, { k: 'error', t: wt(4, /heute/i) - .1 }, { k: 'bell', t: wt(4, /mehr/i) - .1 });
  E.push({ k: 'impact', t: TT.up }, { k: 'chime', t: wt(5, /lena/i) }, { k: 'bell', t: wt(5, /bitte/i) });
  E.push({ k: 'impact', t: TT.space }, { k: 'whoosh', t: TT.space + .1, d: 1.8 }, { k: 'error', t: wt(6, /fehlen/i) - .2 });
  E.push({ k: 'impact', t: TT.back }, { k: 'bell', t: L(7).start + .1 }, { k: 'swish', t: L(8).start, d: .4 }, { k: 'type', t: wt(8, /schreib/i), n: 12 });
  return E;
};
</script></body></html>
