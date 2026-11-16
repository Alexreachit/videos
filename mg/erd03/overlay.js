// ======================= BIS ZUM ERDKERN – Tag 1 (realistisch): Overlays ueber Blender-Bildern =======================
const Lt = i => MG.L(i);
function wt(i, re) { const l = Lt(i); if (!l.words) return l.start; for (const x of l.words) if (re.test(x[0])) return l.start + x[1]; return l.start }
const pop = (t, t0, d = .35) => bo(cl(t, t0, t0 + d)), fade = (t, t0, t1) => 1 - ez(cl(t, t0, t1));
const SH = (r = 4, c = 'rgba(0,0,0,.85)') => `0 0 ${r}px ${c},0 ${r / 2}px ${r * 2}px ${c}`;
const ORANGE = '#ff8a1e', GREEN = '#3ee08f', RED = '#ff4a3d';
const fr = t => Math.max(0, Math.min(TT.nf - 1, Math.round(t * TT.fps)));
const anc = (k, t) => ANCH[k][fr(t)];
const isGround = t => t < TT.space || t >= TT.back;
let lastBg = -1;
async function setBg(t) {
  const f = fr(t); if (f === lastBg) return; lastBg = f;
  const im = $('bg'); im.src = 'bg/' + String(f).padStart(5, '0') + '.jpg'; try { await im.decode() } catch (e) { }
}
function tagAt(p, html, s) { if (!p || s <= .01) return ''; return `<div style="position:absolute;left:${p[0]}px;top:${p[1]}px;transform:translate(-50%,-100%) scale(${s});transform-origin:50% 100%">${html}</div>` }
function dayTag(t) {
  const s = pop(t, .05, .4) * fade(t, Lt(1).start + .3, Lt(1).start + .6); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;transform:translateX(-50%) scale(${s});padding:18px 44px 22px;text-align:center">
    <div style="font-size:40px;letter-spacing:6px;color:${ORANGE}">BIS ZUM ERDKERN</div><div style="font-size:128px;line-height:1">TAG 1</div></div>`;
}
function hud(t) {
  if (!isGround(t)) return '';
  const hideR = 1 - pop(t, Lt(3).start - .2, .25) * fade(t, TT.rise - .3, TT.rise); if (hideR <= .01) return '';
  const s = pop(t, .35, .4) * hideR; const d = t > TT.scoop ? .1 : 0, bump = t > TT.scoop && t < TT.scoop + .4 ? 1 + .22 * Math.sin((t - TT.scoop) / .4 * Math.PI) : 1;
  return `<div class="glass" style="right:34px;top:${t < Lt(1).start + .6 ? 470 : 190}px;transform:scale(${s * bump});transform-origin:100% 0;padding:14px 28px 16px;text-align:right">
      <div class="sub" style="font-size:28px">TIEFE</div><div style="font-size:84px;line-height:1">${d.toFixed(1).replace('.', ',')} m</div>
      <div class="sub" style="font-size:26px;margin-top:4px">Ziel: 6.370 km</div></div>
    <div class="glass" style="left:34px;top:${t < Lt(1).start + .6 ? 470 : 190}px;transform:scale(${pop(t, Lt(1).start + .3, .4) * hideR});transform-origin:0 0;padding:14px 28px 16px">
      <div class="sub" style="font-size:28px">ARBEITER</div><div style="font-size:84px;line-height:1">👷 1</div></div>`;
}
function rulesCard(t) {
  const t0 = Lt(3).start - .05, t1 = TT.rise - .1, s = pop(t, t0, .35) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  const R = [['❤️', 'LIKE', 'jeder Arbeiter schaufelt 1×', /like/i], ['↗️', 'SHARE', 'jeder Arbeiter schaufelt 5×', /share/i]];
  return `<div class="glass" style="left:50%;top:190px;width:880px;transform:translateX(-50%) scale(${s});padding:20px 32px 24px">` +
    R.map(([e, a, b, re]) => { const p = pop(t, wt(3, re) - .3, .35); return `<div style="display:flex;align-items:center;gap:24px;margin-top:10px;transform:scale(${.6 + .4 * p});opacity:${.2 + .8 * Math.min(1, p)}">
      <div style="width:100px;height:100px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 56px/100px IB,Arial;text-align:center">${e}</div>
      <div><div style="font-size:54px">${a}</div><div class="sub">${b}</div></div></div>` }).join('') +
    `<div style="margin-top:14px;text-align:center;font:800 36px P,Arial;color:${ORANGE}">1 Schaufel = 10 cm</div></div>`;
}
function workerTags(t) {
  let h = '';
  if (t > Lt(1).start && t < TT.rise - .1) h += tagAt(anc('chef', t), `<div class="tag" style="font-size:36px;background:${ORANGE}">ICH · CHEF</div>`, pop(t, Lt(1).start) * fade(t, TT.rise - .3, TT.rise - .1));
  if (t > TT.follow && t < TT.rise - .1) h += tagAt(anc('ghost', t), `<div class="lbl" style="position:relative;font-size:104px;color:${GREEN};text-shadow:${SH(8)}">+1</div>`, pop(t, TT.follow, .45) * fade(t, TT.rise - .3, TT.rise - .1));
  if (t > wt(7, /folg/i) - .2) { const g = anc('ghost', t); if (g) h += tagAt([g[0] - 150, g[1] + 120], `<div class="lbl" style="position:relative;font-size:92px;color:${GREEN};text-shadow:${SH(8)}">DU?</div>`, pop(t, wt(7, /folg/i) - .2, .45)) }
  return h;
}
// ---- Erde: Pin, Linie zur Mitte, Schicht-Beschriftungen
function earthUI(t) {
  if (isGround(t)) return '';
  const pin = anc('pin', t), cen = anc('center', t); let h = '';
  const sp = pop(t, TT.space + .25, .4);
  if (pin && sp > .01) h += `<div style="position:absolute;left:${pin[0]}px;top:${pin[1]}px;transform:translate(-50%,-50%) scale(${sp})"><div style="width:30px;height:30px;border-radius:50%;background:${RED};border:5px solid #fff;box-shadow:0 0 24px ${RED}"></div></div>`
    + `<div class="lbl" style="left:${pin[0] - 26}px;top:${pin[1] - 22}px;transform:translate(-100%,-100%) scale(${sp});transform-origin:100% 100%;font-size:48px;color:#fff;text-shadow:${SH(6)}">WIR ⬇</div>`;
  const l5 = Lt(5).start, dl = cl((t - TT.zoomEnd + .1) / .9, 0, 1);
  if (pin && cen && dl > 0) { const x = lerp(pin[0], cen[0], dl), y = lerp(pin[1], cen[1], dl);
    h += `<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><line x1="${pin[0]}" y1="${pin[1]}" x2="${x}" y2="${y}" stroke="#fff" stroke-width="7" stroke-dasharray="18 12" stroke-linecap="round"/></svg>`;
    if (dl >= 1) h += `<div class="glass" style="left:${(pin[0] + cen[0]) / 2 - 30}px;top:${(pin[1] + cen[1]) / 2}px;transform:translate(-100%,-50%) scale(${pop(t, TT.zoomEnd + .8)});transform-origin:100% 50%;padding:8px 22px;font-size:46px;color:${ORANGE}">6.370 km</div>`; }
  const L = [['crust', 'KRUSTE', 'bis ~40 km tief', '#e8d8c8', 0], ['mantle', 'MANTEL', 'bis ~2.900 km', '#ff9a4a', .35], ['outer', 'ÄUSSERER KERN', 'bis ~5.100 km', '#ffc34a', .7], ['inner', 'INNERER KERN', 'bis zur Mitte', '#fff2a8', 1.05]];
  for (const [k, a, b, c, dt] of L) {
    const p = anc(k, t), s = pop(t, TT.zoomEnd + .15 + dt, .35); if (!p || s <= .01) continue;
    const lx = 760, ly = p[1] + (k === 'crust' ? -30 : k === 'mantle' ? 30 : k === 'outer' ? 80 : 170);
    h += `<svg width="1080" height="1920" style="position:absolute;left:0;top:0;opacity:${Math.min(1, s)}"><polyline points="${p[0]},${p[1]} ${lx - 20},${ly} ${lx},${ly}" fill="none" stroke="#fff" stroke-width="4"/><circle cx="${p[0]}" cy="${p[1]}" r="9" fill="#fff"/></svg>`;
    h += `<div class="glass" style="left:${lx}px;top:${ly}px;transform:translateY(-50%) scale(${s});transform-origin:0 50%;padding:8px 20px 10px"><div style="font-size:38px;color:${c}">${a}</div><div class="sub" style="font-size:28px">${b}</div></div>`;
  }
  const no = cl((t - TT.zoomEnd - 1.4) / .5, 0, 1); if (no > 0) h += `<div class="lbl" style="left:0;width:1080px;top:1720px;font:700 26px P,Arial;color:rgba(255,255,255,.6);opacity:${no}">Kruste zur Sichtbarkeit dicker gezeichnet · Erdbild: NASA</div>`;
  return h;
}
function kmTitle(t) {
  const s = pop(t, Lt(5).start - .05, .4) * fade(t, Lt(6).start - .1, Lt(6).start + .15); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;transform:translateX(-50%) scale(${s});padding:14px 44px 18px;text-align:center"><div class="sub">bis zum Erdmittelpunkt</div><div style="font-size:120px;line-height:1;color:${ORANGE};white-space:nowrap">6.370 km</div></div>`;
}
function bigNumber(t) {
  const t0 = wt(6, /64|millionen/i) - .25, t1 = TT.back - .1, s = pop(t, t0, .4) * fade(t, t1, t1 + .15); if (t < Lt(6).start || s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;width:900px;transform:translateX(-50%) scale(${s});padding:18px 30px 22px;text-align:center">
    <div class="sub">6.370 km ÷ 10 cm =</div><div style="font-size:112px;line-height:1.05;color:${ORANGE}">63.700.000×</div><div style="font-size:48px">SCHAUFELN</div></div>`;
}
function followTag(t) {
  const t0 = wt(7, /folg/i) - .1, t1 = Lt(8).start - .1, s = pop(t, t0, .4) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  return `<div class="tag" style="left:50%;top:1180px;transform:translateX(-50%) scale(${s});font-size:66px;background:#18b864;padding:10px 34px">➕ FOLGEN = ARBEITER</div>`;
}
function commentCard(t) {
  const t0 = Lt(8).start + .2, s = pop(t, t0, .45); if (t < t0) return '';
  const txt = 'Schreib es in die Kommentare', n = Math.floor(cl((t - Lt(9).start + .1) / 1.2, 0, 1) * txt.length);
  return `<div class="glass" style="left:50%;top:1110px;width:880px;transform:translateX(-50%) scale(${s});padding:20px 26px;display:flex;align-items:center;gap:22px">
    <div style="width:96px;height:96px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 56px/96px IB,Arial;text-align:center">⛏️</div>
    <div><div class="sub">Welches Werkzeug brauchen wir?</div><div style="font:800 44px P,Arial">${txt.slice(0, n)}<span style="opacity:${Math.sin(t * 10) > 0 ? 1 : 0}">|</span></div></div></div>`;
}
function flash(t) {
  let a = 1 - Math.abs(t - TT.back) / .18;
  if (t > TT.space - .45 && t < TT.space) a = Math.max(a, ez((t - TT.space + .45) / .45)); if (t >= TT.space) a = Math.max(a, 1 - (t - TT.space) / .22);
  return a > 0 ? `<div style="position:absolute;inset:0;background:#fff;opacity:${Math.min(1, Math.max(0, a)) * .92}"></div>` : '';
}
window.setTimeline = tl => { MG.TL = tl };
window.draw = async function (t) {
  await setBg(t);
  $('ov').innerHTML = workerTags(t) + earthUI(t);
  let ui = dayTag(t) + hud(t) + rulesCard(t) + kmTitle(t) + bigNumber(t) + followTag(t) + commentCard(t);
  ui += MG.captions(t, { y: 1500, size: 80, maxWords: 3, hl: '#ffb347', upper: true, stageW: 1080 }).replace(/'Arial Black',Arial/, 'IB,Arial');
  $('ui').innerHTML = ui; $('fx').innerHTML = flash(t);
};
window.sfxEvents = function () {
  const E = [], L = Lt;
  E.push({ k: 'whoosh', t: .05, d: 1.0 }, { k: 'chime', t: .3 });
  for (let x = .5; x < TT.rise; x += 1.15) E.push({ k: 'thud', t: x, g: .28 });
  E.push({ k: 'bell', t: TT.scoop });
  E.push({ k: 'pop', t: TT.follow }, { k: 'chime', t: TT.follow + .15 });
  E.push({ k: 'swish', t: L(3).start, d: .4 }, { k: 'pop', t: wt(3, /like/i) - .3 }, { k: 'pop', t: wt(3, /share/i) - .3 });
  E.push({ k: 'whoosh', t: TT.rise, d: 1.6 }, { k: 'impact', t: TT.space }, { k: 'whoosh', t: TT.space + .1, d: 1.8 });
  [0, .35, .7, 1.05].forEach(d => E.push({ k: 'tick', t: TT.zoomEnd + .15 + d }));
  E.push({ k: 'error', t: wt(6, /64|millionen/i) - .25 });
  E.push({ k: 'impact', t: TT.back }, { k: 'pop', t: wt(7, /folg/i) }, { k: 'swish', t: L(8).start, d: .4 }, { k: 'type', t: L(9).start, n: 12 });
  return E;
};
</script></body></html>
