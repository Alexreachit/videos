// ======================= BIS ZUM ERDKERN – Tag 2 (realistisch): Overlays ueber Blender-Bildern =======================
const Lt = i => MG.L(i);
function wt(i, re) { const l = Lt(i); if (!l.words) return l.start; for (const x of l.words) if (re.test(x[0])) return l.start + x[1]; return l.start }
const pop = (t, t0, d = .35) => bo(cl(t, t0, t0 + d)), fade = (t, t0, t1) => 1 - ez(cl(t, t0, t1));
const SH = (r = 4, c = 'rgba(0,0,0,.85)') => `0 0 ${r}px ${c},0 ${r / 2}px ${r * 2}px ${c}`;
const ORANGE = '#ff8a1e', GREEN = '#3ee08f', RED = '#ff4a3d';
const fr = t => Math.max(0, Math.min(TT.nf - 1, Math.round(t * TT.fps)));
const anc = (k, t) => ANCH[k][fr(t)];
const inSpace = t => t >= TT.space && t < TT.back;
const fmtDepth = d => d >= 100 ? Math.round(d).toLocaleString('de-DE') + ' m' : d.toFixed(1).replace('.', ',') + ' m';
let lastBg = -1;
async function setBg(t) {
  const f = fr(t); if (f === lastBg) return; lastBg = f;
  const im = $('bg'); im.src = 'bg/' + String(f).padStart(5, '0') + '.jpg'; try { await im.decode() } catch (e) { }
}
function tagAt(p, html, s) { if (!p || s <= .01) return ''; return `<div style="position:absolute;left:${p[0]}px;top:${p[1]}px;transform:translate(-50%,-100%) scale(${s});transform-origin:50% 100%">${html}</div>` }
function dayTag(t) {
  const s = pop(t, .05, .4) * fade(t, Lt(1).start - .2, Lt(1).start + .1); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;transform:translateX(-50%) scale(${s});padding:18px 44px 22px;text-align:center">
    <div style="font-size:40px;letter-spacing:6px;color:${ORANGE}">BIS ZUM ERDKERN</div><div style="font-size:128px;line-height:1">TAG 2</div></div>`;
}
// Arbeiter- und Tiefen-Anzeige
function hud(t) {
  if (inSpace(t)) return '';
  const hide = (t > Lt(2).start - .15 && t < Lt(3).start + .1) || (t > Lt(3).start - .15 && t < TT.d0 + .1) || (t > TT.d1 + .5 && t < TT.space);
  const tn = wt(1, /201/) - .2, n = Math.round(lerp(1, 201, ez(cl((t - tn) / 1.1, 0, 1)))), bumpN = t > tn + 1 && t < tn + 1.4 ? 1 + .2 * Math.sin((t - tn - 1) / .4 * Math.PI) : 1;
  const d = TT.depth[fr(t)], s = pop(t, Lt(1).start - .2, .4) * (hide ? 0 : 1); if (s <= .01) return '';
  const desc = t > TT.d0 && t < TT.d1 + .6;
  return `<div class="glass" style="left:34px;top:190px;transform:scale(${s * (desc ? 0 : 1) * bumpN});transform-origin:0 0;padding:14px 28px 16px">
      <div class="sub" style="font-size:28px">ARBEITER</div><div style="font-size:84px;line-height:1">👷 ${n}</div></div>
    <div class="glass" style="${desc ? 'left:50%;transform:translateX(-50%) scale(' + s * 1.35 + ');transform-origin:50% 0' : 'right:34px;transform:scale(' + s + ');transform-origin:100% 0'};top:190px;padding:14px 28px 16px;text-align:${desc ? 'center' : 'right'}">
      <div class="sub" style="font-size:28px">TIEFE</div><div style="font-size:84px;line-height:1;color:${desc ? ORANGE : '#fff'}">${fmtDepth(d)}</div>
      <div class="sub" style="font-size:26px;margin-top:4px">Ziel: 6.370 km</div></div>`;
}
function calcCard(t) {
  const t0 = Lt(2).start - .05, t1 = Lt(3).start - .15, s = pop(t, t0, .35) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  const r = (re, html) => { const p = pop(t, wt(2, re) - .25, .35); return `<div style="display:flex;align-items:center;gap:22px;margin-top:12px;opacity:${.15 + .85 * Math.min(1, p)};transform:scale(${.7 + .3 * p});transform-origin:0 50%">${html}</div>` };
  const ic = e => `<div style="width:92px;height:92px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 52px/92px IB,Arial;text-align:center">${e}</div>`;
  const tot = pop(t, wt(2, /40|vierzig/) - .2, .4);
  return `<div class="glass" style="left:50%;top:190px;width:900px;transform:translateX(-50%) scale(${s});padding:20px 34px 26px">` +
    r(/likes/i, ic('❤️') + `<div style="font-size:56px">35 Likes <span class="sub" style="font-size:40px">× 1 =</span> 35</div>`) +
    r(/share/i, ic('↗️') + `<div style="font-size:56px">1 Share <span class="sub" style="font-size:40px">× 5 =</span> 5</div>`) +
    `<div style="height:3px;background:rgba(255,255,255,.3);margin:18px 0 10px"></div>
     <div style="text-align:center;transform:scale(${.6 + .4 * tot});opacity:${Math.min(1, tot)}"><div style="font-size:96px;line-height:1;color:${ORANGE}">40 Schaufeln</div><div class="sub">pro Arbeiter</div></div></div>`;
}
function mathCard(t) {
  const t0 = Lt(3).start - .05, t1 = TT.d0 + .4, s = pop(t, t0, .35) * fade(t, t1, t1 + .25); if (s <= .01) return '';
  return `<div class="glass" style="left:50%;top:190px;width:900px;transform:translateX(-50%) scale(${s});padding:20px 30px 24px;text-align:center">
    <div style="font-size:60px">201 × 40 × 10 cm</div><div style="font-size:120px;line-height:1.05;color:${ORANGE}">= 804 m</div></div>`;
}
function arrivedTag(t) {
  const s = pop(t, TT.d1 - .1, .4) * fade(t, Lt(4).start - .2, Lt(4).start + .1); if (s <= .01) return '';
  return `<div class="tag" style="left:50%;top:1150px;transform:translateX(-50%) scale(${s});font-size:64px;background:#18b864;padding:10px 34px">✅ 804 m TIEFER!</div>`;
}
// Vergleich: Schacht 804 m vs. hoechstes Gebaeude 828 m
function compareCard(t) {
  const t0 = Lt(4).start - .05, t1 = TT.space - .3, s = pop(t, t0, .4) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  const g = ez(cl((t - t0 - .2) / 1.2, 0, 1)), PX = .62, gy = 820, hB = 828 * PX * g, hS = 804 * PX * g;
  const tower = `<path d="M${-38},0 L${-38},${-hB * .55} L${-24},${-hB * .55} L${-24},${-hB * .78} L${-12},${-hB * .78} L${-12},${-hB * .92} L${-3},${-hB * .92} L0,${-hB} L3,${-hB * .92} L12,${-hB * .92} L12,${-hB * .78} L24,${-hB * .78} L24,${-hB * .55} L38,${-hB * .55} L38,0 Z" fill="#b9c6d6" stroke="#fff" stroke-width="3"/>`;
  return `<div class="glass" style="left:50%;top:180px;width:920px;height:1180px;transform:translateX(-50%) scale(${s});transform-origin:50% 0;padding:0;overflow:hidden">
    <svg width="920" height="1180" viewBox="0 0 920 1180">
      <rect x="0" y="0" width="920" height="${gy}" fill="rgba(120,170,230,.10)"/><rect x="0" y="${gy}" width="920" height="${1180 - gy}" fill="rgba(110,75,45,.55)"/>
      <line x1="0" y1="${gy}" x2="920" y2="${gy}" stroke="#7ac05a" stroke-width="8"/>
      <g transform="translate(250,${gy})">${tower}</g>
      <rect x="610" y="${gy}" width="70" height="${hS}" fill="#140e0a" stroke="${ORANGE}" stroke-width="4"/>
      <text x="250" y="${gy - hB - 22}" text-anchor="middle" font-family="IB,Arial" font-weight="900" font-size="54" fill="#fff" opacity="${g}">828 m</text>
      <text x="645" y="${gy + hS + 60}" text-anchor="middle" font-family="IB,Arial" font-weight="900" font-size="54" fill="${ORANGE}" opacity="${g}">804 m</text>
      <text x="250" y="${gy + 60}" text-anchor="middle" font-family="P,Arial" font-weight="700" font-size="32" fill="#fff">höchstes Gebäude</text>
      <text x="250" y="${gy + 100}" text-anchor="middle" font-family="P,Arial" font-weight="700" font-size="32" fill="#fff">der Welt</text>
      <text x="645" y="${gy - 30}" text-anchor="middle" font-family="P,Arial" font-weight="700" font-size="34" fill="#fff">unser Loch</text>
    </svg></div>
    <div class="lbl" style="left:0;width:1080px;top:1380px;font:700 24px P,Arial;color:rgba(255,255,255,.6);opacity:${s}">Burj Khalifa, 828 m (Guinness World Records) · Grafik vereinfacht</div>`;
}
function earthUI(t) {
  if (!inSpace(t)) return '';
  const pin = anc('pin', t), cen = anc('center', t); let h = '';
  const sp = pop(t, TT.space + .25, .4);
  if (pin && sp > .01) h += `<div style="position:absolute;left:${pin[0]}px;top:${pin[1]}px;transform:translate(-50%,-50%) scale(${sp})"><div style="width:30px;height:30px;border-radius:50%;background:${RED};border:5px solid #fff;box-shadow:0 0 24px ${RED}"></div></div>`
    + `<div class="glass" style="left:${pin[0] - 30}px;top:${pin[1] - 20}px;transform:translate(-100%,-100%) scale(${sp});transform-origin:100% 100%;padding:8px 20px 10px;text-align:right"><div style="font-size:40px">WIR</div><div class="sub" style="font-size:28px">804 m tief</div></div>`;
  const dl = cl((t - TT.zoomEnd + .1) / .9, 0, 1);
  if (pin && cen && dl > 0) { const x = lerp(pin[0], cen[0], dl), y = lerp(pin[1], cen[1], dl);
    h += `<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><line x1="${pin[0]}" y1="${pin[1]}" x2="${x}" y2="${y}" stroke="#fff" stroke-width="7" stroke-dasharray="18 12" stroke-linecap="round"/><circle cx="${pin[0]}" cy="${pin[1]}" r="4" fill="${ORANGE}"/></svg>`; }
  const no = cl((t - TT.zoomEnd - .8) / .5, 0, 1); if (no > 0) h += `<div class="lbl" style="left:0;width:1080px;top:1720px;font:700 26px P,Arial;color:rgba(255,255,255,.6);opacity:${no}">Erdbild: NASA · 804 m sind auf dem Bild kleiner als ein Pixel</div>`;
  return h;
}
function restCard(t) {
  const s = pop(t, wt(5, /fehlen/i) - .2, .4) * fade(t, TT.back - .15, TT.back); if (s <= .01 || !inSpace(t)) return '';
  return `<div class="glass" style="left:50%;top:190px;transform:translateX(-50%) scale(${s});padding:14px 44px 18px;text-align:center"><div class="sub">es fehlen noch über</div><div style="font-size:120px;line-height:1;color:${ORANGE};white-space:nowrap">6.369 km</div></div>`;
}
function workerTags(t) {
  let h = '';
  if (t > Lt(1).start && t < Lt(2).start - .1) h += tagAt(anc('chef', t), `<div class="tag" style="font-size:36px;background:${ORANGE}">ICH · CHEF</div>`, pop(t, Lt(1).start + .1) * fade(t, Lt(2).start - .3, Lt(2).start - .1));
  if (t > TT.follow - .05) { const g = anc('ghost', t); if (g) h += tagAt(g, `<div class="lbl" style="position:relative;font-size:96px;color:${GREEN};text-shadow:${SH(8)}">${t < Lt(7).start ? '+1' : 'DU?'}</div>`, pop(t, TT.follow - .05, .45)); }
  return h;
}
function followTag(t) {
  const t0 = wt(6, /folg/i) - .1, t1 = Lt(7).start - .1, s = pop(t, t0, .4) * fade(t, t1, t1 + .2); if (s <= .01) return '';
  return `<div class="tag" style="left:50%;top:1180px;transform:translateX(-50%) scale(${s});font-size:66px;background:#18b864;padding:10px 34px">➕ FOLGEN = ARBEITER</div>`;
}
function commentCard(t) {
  const t0 = Lt(7).start + .2, s = pop(t, t0, .45); if (t < t0) return '';
  const txt = 'Schreib es in die Kommentare', n = Math.floor(cl((t - Lt(8).start + .1) / 1.2, 0, 1) * txt.length);
  return `<div class="glass" style="left:50%;top:1110px;width:880px;transform:translateX(-50%) scale(${s});padding:20px 26px;display:flex;align-items:center;gap:22px">
    <div style="width:96px;height:96px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 56px/96px IB,Arial;text-align:center">🔦</div>
    <div><div class="sub">Was finden wir da unten als Erstes?</div><div style="font:800 44px P,Arial">${txt.slice(0, n)}<span style="opacity:${Math.sin(t * 10) > 0 ? 1 : 0}">|</span></div></div></div>`;
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
  let ui = dayTag(t) + hud(t) + calcCard(t) + mathCard(t) + arrivedTag(t) + compareCard(t) + restCard(t) + followTag(t) + commentCard(t);
  ui += MG.captions(t, { y: 1500, size: 80, maxWords: 3, hl: '#ffb347', upper: true, stageW: 1080 }).replace(/'Arial Black',Arial/, 'IB,Arial');
  $('ui').innerHTML = ui; $('fx').innerHTML = flash(t);
};
window.sfxEvents = function () {
  const E = [], L = Lt;
  E.push({ k: 'whoosh', t: .05, d: 1.4 }, { k: 'chime', t: .3 });
  for (let x = .5; x < TT.d0; x += .55) E.push({ k: 'thud', t: x, g: .22 });
  const tn = wt(1, /201/) - .2; for (let k = 0; k < 10; k++) E.push({ k: 'pop', t: tn + k * .11, g: .4 }); E.push({ k: 'bell', t: tn + 1.1 });
  E.push({ k: 'swish', t: L(2).start, d: .4 }, { k: 'pop', t: wt(2, /likes/i) - .25 }, { k: 'pop', t: wt(2, /share/i) - .25 }, { k: 'chime', t: wt(2, /40|vierzig/) - .2 });
  E.push({ k: 'swish', t: L(3).start, d: .4 }, { k: 'impact', t: wt(3, /804/) - .1 });
  E.push({ k: 'whoosh', t: TT.d0, d: TT.d1 - TT.d0 }, { k: 'impact', t: TT.d1 - .05 }, { k: 'bell', t: TT.d1 + .1 });
  E.push({ k: 'swish', t: L(4).start, d: .5 }, { k: 'tick', t: L(4).start + .6 });
  E.push({ k: 'impact', t: TT.space }, { k: 'whoosh', t: TT.space + .1, d: 1.8 }, { k: 'error', t: wt(5, /fehlen/i) - .2 });
  E.push({ k: 'impact', t: TT.back }, { k: 'pop', t: TT.follow - .05 }, { k: 'chime', t: TT.follow + .1 }, { k: 'pop', t: wt(6, /folg/i) });
  E.push({ k: 'swish', t: L(7).start, d: .4 }, { k: 'type', t: L(8).start, n: 12 });
  return E;
};
</script></body></html>
