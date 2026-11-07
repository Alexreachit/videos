// ===================== UI (gleiche Bausteine wie die anderen Videos: weisse Karten, Navy-Rand, IB-Schrift) =====================
const fmt = n => Math.round(n).toLocaleString('en-US');
const card = (x, y, inner, s, o = {}) => s <= .01 ? '' : `<div class="card" style="left:${x}px;top:${y}px;transform:translate(-50%,0) rotate(${o.rot || 0}deg) scale(${s});transform-origin:50% 0;padding:${o.pad || '18px 40px'};text-align:center;${o.w ? 'width:' + o.w + 'px;' : ''}${o.bg ? 'background:' + o.bg + ';' : ''}">${inner}</div>`;
const pill = (x, y, txt, s, o = {}) => s <= .01 ? '' : `<div class="pill" style="left:${x}px;top:${y}px;transform:translate(${o.left ? '0' : '-50%'},-50%) rotate(${o.rot || 0}deg) scale(${s});transform-origin:${o.left ? '0' : '50%'} 50%;font-size:${o.size || 44}px;color:${o.col || '#fff'};background:${o.bg || '#2a6fd6'};text-shadow:${o.col == OL ? 'none' : shadowTxt(OL, 3)}">${txt}</div>`;
const stampTx = (x, y, txt, t, t0, o = {}) => { if (t < t0) return ''; const k = lerp(2.2, 1, ez(cl(t, t0, t0 + .18))); return `<div style="position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%) rotate(${o.rot ?? -8}deg) scale(${k});border:12px solid ${o.col || '#e8483c'};border-radius:22px;padding:4px 34px;color:${o.col || '#e8483c'};background:#ffffffe8;font:900 ${o.size || 110}px/1.05 IB,Arial;white-space:nowrap">${txt}</div>` };
const bigNum = (x, y, txt, s, col = '#35e08a', size = 170) => s <= .01 ? '' : `<div class="lbl" style="left:${x}px;top:${y}px;transform:translate(-50%,-50%) scale(${s});font-size:${size}px;line-height:1;color:${col};text-shadow:${shadowTxt(OL, 9)}">${txt}</div>`;
function labelAt(p, html, s) { const q = w.project(p); if (!q.vis || s <= .01) return ''; return `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%) scale(${s});transform-origin:50% 100%">${html}</div>` }
const CH = { ch1: ['CHAPTER 1', 'THE MAN WITH $2.50'], ch2: ['CHAPTER 2', 'THE STAMP TRICK'], ch3: ['CHAPTER 3', '50% IN 45 DAYS'], ch4: ['CHAPTER 4', 'PONZI FEVER'], ch5: ['CHAPTER 5', 'THE NEWSPAPER'], ch6: ['CHAPTER 6', 'THE FALL'] };
let CHAP = [];
function chapterUI(t) {
  let h = '', cur = null;
  for (const c of CHAP) if (t >= c.t - .1) cur = c;
  if (!cur) return '';
  const a = cur.t, s = pop(t, a - .05, .45), out = ez(cl(t, a + 2.3, a + 2.8));
  if (out < 1) h += `<div style="position:absolute;left:0;right:0;top:${lerp(330, 300, s)}px;text-align:center;opacity:${1 - out};transform:scale(${lerp(.9, 1, s)})">
    <div class="pill" style="position:relative;display:inline-block;font-size:44px;color:#fff;background:#e8483c;text-shadow:${shadowTxt(OL, 3)}">${cur.k[0]}</div><br>
    <div class="lbl" style="position:relative;display:inline-block;margin-top:24px;font-size:150px;line-height:1;text-shadow:${shadowTxt(OL, 10)}">${cur.k[1]}</div></div>`;
  if (t > a + 2.5 && lineAt(t) < 55) h += pill(40, 60, `<span style="opacity:.75">${cur.k[0].replace('CHAPTER ', 'CH ')}</span> · ${cur.k[1]}`, pop(t, a + 2.5, .4), { left: true, size: 30, bg: '#ffffff', col: OL });
  return h;
}
// Karten (Weltkarte aus mapdata.js)
const MAPC = {};
function mapBase(key, lon0, lon1, lat0, lat1, hi) {
  if (MAPC[key]) return MAPC[key];
  const [x0, y1] = MAPP(lon0, lat0), [x1, y0] = MAPP(lon1, lat1);
  let s = `<rect x="${x0 - 50}" y="${y0 - 50}" width="${x1 - x0 + 100}" height="${y1 - y0 + 100}" fill="#8fd0f5"/>`;
  for (const k in WORLD) s += `<path d="${WORLD[k]}" fill="${hi[k] || '#f4dca0'}" stroke="${OL}" stroke-width="1.2" stroke-linejoin="round"/>`;
  return MAPC[key] = { s, vb: `${x0} ${y0} ${x1 - x0} ${y1 - y0}`, k: (x1 - x0) / 1500 };
}
function mapCard(t, t0, key, box, hi, pins, arrows, o = {}) {
  const s = pop(t, t0, .45); if (s <= .01) return '';
  const m = mapBase(key, ...box, hi), k = m.k;
  let fg = '';
  arrows.forEach(([a, b, ta, col]) => { const A = MAPP(...a), B = MAPP(...b), C = [(A[0] + B[0]) / 2, Math.min(A[1], B[1]) - Math.hypot(B[0] - A[0], B[1] - A[1]) * .3], u = ez(cl(t, ta, ta + 1.1));
    if (u <= 0) return; const L = 2000; fg += `<path d="M${A[0]},${A[1]} Q${C[0]},${C[1]} ${B[0]},${B[1]}" fill="none" stroke="${col || '#e8483c'}" stroke-width="${7 * k}" stroke-dasharray="${18 * k} ${12 * k}" pathLength="1000" style="stroke-dashoffset:0" opacity="${u > 0 ? 1 : 0}" clip-path="none"/>`;
    const P = (v) => [(1 - v) * (1 - v) * A[0] + 2 * v * (1 - v) * C[0] + v * v * B[0], (1 - v) * (1 - v) * A[1] + 2 * v * (1 - v) * C[1] + v * v * B[1]], q = P(u);
    fg += `<circle cx="${q[0]}" cy="${q[1]}" r="${11 * k}" fill="${col || '#e8483c'}" stroke="${OL}" stroke-width="${3 * k}"/>` });
  pins.forEach(([ll, lab, tp, col]) => { const p = MAPP(...ll), v = pop(t, tp, .35); if (v <= .01) return;
    fg += `<g transform="translate(${p[0]},${p[1]}) scale(${v * k})"><circle r="14" fill="${col || '#e8483c'}" stroke="${OL}" stroke-width="5"/><g transform="translate(22,-22)"><rect x="0" y="-34" width="${lab.length * 25 + 30}" height="50" rx="14" fill="#fff" stroke="${OL}" stroke-width="5"/><text x="15" y="2" font-family="IB,Arial" font-weight="900" font-size="34" fill="${OL}">${lab}</text></g></g>` });
  return `<div style="position:absolute;left:960px;top:${o.y || 120}px;transform:translateX(-50%) rotate(${o.rot ?? -1.5}deg) scale(${s});transform-origin:50% 0;border:8px solid ${OL};border-radius:34px;overflow:hidden;box-shadow:0 14px 0 #2328384d;width:1180px;height:${o.h || 700}px">
    <svg viewBox="${m.vb}" width="1180" height="${o.h || 700}" preserveAspectRatio="xMidYMid slice">${m.s}${fg}</svg></div>`;
}
function samSVG(t, x, y, wd, o = {}) {
  const i = MG.cur(t), l = Lt(i);
  const p = Object.assign({ mouth: 'smile', talk: MG_SAM.talk(t, l) * (t < l.end + .05 ? 1 : 0), blink: MG_SAM.blink(t), armL: [.15, .1], armR: [.15, .1], w: wd }, o);
  return `<div style="position:absolute;left:${x - wd / 2}px;top:${y - wd * 365 / 240}px">${MG_SAM.svg(p)}</div>`;
}
const flagIcon = `<svg width="60" height="60" viewBox="0 0 60 60" style="vertical-align:-12px"><path d="M14 54 V6" stroke="${OL}" stroke-width="6" stroke-linecap="round"/><path d="M16 8 H48 L40 20 L48 32 H16 Z" fill="#e8483c" stroke="${OL}" stroke-width="4" stroke-linejoin="round"/></svg>`;
function newspaperCard(t, t0, head, sub, date, o = {}) {
  const u = cl(t, t0, t0 + .7), s = ez(u); if (u <= 0) return '';
  const rot = lerp(720, o.rot ?? -4, ez(u)), k = lerp(.05, 1, s);
  return `<div style="position:absolute;left:960px;top:${o.y || 470}px;transform:translate(-50%,-50%) rotate(${rot}deg) scale(${k});width:${o.w || 1000}px;background:#f4eedf;border:8px solid ${OL};border-radius:10px;box-shadow:0 18px 0 #2328384d;padding:24px 40px 30px;font-family:IB,Arial;color:${OL};text-align:center">
   <div style="font:900 30px P,Arial;display:flex;justify-content:space-between;border-bottom:5px solid ${OL};padding-bottom:6px"><span>${date}</span><span>BOSTON</span></div>
   <div style="font:900 92px/1 'Cinzel Decorative',IB,serif;margin:12px 0 10px;letter-spacing:2px">BOSTON POST</div>
   <div style="border-top:5px solid ${OL};border-bottom:2px solid ${OL};height:6px;margin-bottom:16px"></div>
   <div style="font:900 ${o.hs || 74}px/1.05 IB,Arial;color:#b8322a">${head}</div><div style="font:700 36px P,Arial;margin-top:12px;color:#4a4f66">${sub}</div>
   <div style="display:flex;gap:20px;margin-top:20px">${[0, 1, 2].map(c => `<div style="flex:1">${[0, 1, 2, 3].map(r => `<div style="height:12px;background:#b9b2a2;margin:9px 0;width:${90 - ((r + c) % 3) * 12}%"></div>`).join('')}</div>`).join('')}</div></div>`;
}
function ui(t) {
  if (!MG.TL) return '';
  let h = chapterUI(t);
  const i = lineAt(t), sp = SPEC(i), k = sp.ui, l = Lt(i), a = l.start, e = l.end, nx = nextStart(i), out = fade(t, nx - .3, nx), sh = sp.shot;
  const S = (t0, d) => pop(t, t0, d) * out;
  switch (k) {
    case 'date1920': h += pill(60, 900, 'BOSTON · SUMMER 1920', S(a + .3), { left: true, bg: '#ffffff', col: OL, size: 40 }); break;
    case 'promise': { const v = ez(cl(t, wt(i, /fifty/i, -.1), wt(i, /fifty/i, .6))); h += card(1340, 170, `<div style="font-size:46px;color:#6b7280">PONZI PROMISED</div><div style="font-size:190px;line-height:1;color:#2fa36b">${Math.round(50 * v)}%</div><div style="font-size:64px;opacity:${t > wt(i, /forty/i, -.1) ? 1 : 0}">IN 45 DAYS</div>`, S(a + .1), { rot: 3 }); break }
    case 'compare': { const g = ez(cl(t, a + .3, a + 1.2)), g2 = ez(cl(t, wt(i, /year/i, -.2), wt(i, /year/i, .5)));
      const bar = (lab, pct, col, sub) => `<div style="display:flex;align-items:center;gap:22px;margin:16px 0"><div style="width:250px;text-align:right;font-size:48px">${lab}</div><div style="flex:1;height:96px;border:6px solid ${OL};border-radius:20px;background:#eef1f6;overflow:hidden;position:relative"><div style="position:absolute;inset:0;width:${pct}%;background:${col}"></div></div><div style="width:330px;font-size:58px;text-align:left">${sub}</div></div>`;
      h += card(960, 230, `<div style="font-size:44px;color:#6b7280">RETURN</div>${bar('PONZI', 100 * g, '#2fa36b', '50% / 45 DAYS')}${bar('BANK', 10 * g, '#2a6fd6', '~5% / <span style="color:#e8483c">YEAR</span>')}`, S(a, .4), { w: 1450, rot: -1.5 });
      if (g2 > .01) h += stampTx(1500, 690, 'PER YEAR!', t, wt(i, /year/i, -.1), { size: 80 }); break }
    case 'perday': case 'perday2': { const t0 = wt(i, /two/i, -.1), v = ez(cl(t, t0, t0 + 1.6)); h += `<div class="lbl" style="left:960px;top:200px;transform:translateX(-50%) scale(${S(t0 - .2)})"><div class="pill" style="position:relative;display:inline-block;font-size:46px;color:${OL};background:#ffd166">UP TO</div>
      <div style="font-size:200px;line-height:1.05;color:#35e08a;text-shadow:${shadowTxt(OL, 10)}">$${fmt(250000 * v)}</div><div class="pill" style="position:relative;display:inline-block;font-size:64px;color:#fff;background:#e8483c;text-shadow:${shadowTxt(OL, 4)}">PER DAY</div></div>`; break }
    case 'title': { const s = S(a + .2, .6); h += `<div class="lbl" style="left:960px;top:150px;transform:translateX(-50%) scale(${s})"><div class="pill" style="position:relative;display:inline-block;font-size:44px;color:${OL};background:#ffd166">BOSTON · 1920</div><div style="font-size:${t > wt(i, /ponzi/i, -.2) ? 210 : 0}px;line-height:1.05;color:#ffd166;text-shadow:${shadowTxt(OL, 12)};transform:scale(${pop(t, wt(i, /ponzi/i, -.2), .5)})">CHARLES PONZI</div>
      <div style="font-size:${t > wt(i, /famous/i, -.3) ? 76 : 0}px;margin-top:6px;text-shadow:${shadowTxt(OL, 7)}">THE MOST FAMOUS SCAM IN HISTORY</div></div>`; break }
    case 'cash250': { const t0 = wt(i, /two/i, -.15); h += bigNum(1480, 300, '$2.50', S(t0, .5), '#35e08a', 190) + pill(1480, 450, 'NOVEMBER 1903', S(a + .3), { bg: '#2a6fd6' });
      if (t > wt(i, /gambled/i, -.1)) h += pill(1480, 560, '🎲 THE REST: GAMBLED AWAY', S(wt(i, /gambled/i, -.1)), { bg: '#e8483c', size: 38 }); break }
    case 'fired': h += pill(1400, 200, 'DISHWASHER', S(wt(i, /washed/i, -.1)), { bg: '#2a6fd6', rot: -3 }) + pill(1400, 300, 'WAITER', S(wt(i, /waited/i, -.1)), { bg: '#2fa36b', rot: 2 }) + stampTx(1400, 470, 'FIRED!', t, wt(i, /fired/i, -.05)); break;
    case 'montreal': h += pill(60, 900, 'MONTREAL · 1907', S(a + .2), { left: true, bg: '#ffffff', col: OL, size: 40 }) + (t > wt(i, /zarossi/i, -.3) ? pill(1400, 220, 'BANK OWNER: LUIGI ZAROSSI', S(wt(i, /zarossi/i, -.3)), { bg: '#2f4372', size: 40 }) : ''); break;
    case 'sixpct': h += card(1350, 160, `<div style="font-size:44px;color:#6b7280">INTEREST ON DEPOSITS</div><div style="display:flex;gap:50px;justify-content:center;align-items:flex-end;margin-top:10px"><div><div style="font-size:150px;line-height:1;color:#2fa36b">6%</div><div style="font-size:40px">ZAROSSI</div></div><div><div style="font-size:90px;line-height:1;color:#9aa3b5">3%</div><div style="font-size:40px;color:#6b7280">NORMAL</div></div></div>`, S(a + .3), { rot: 2 }) + (t > wt(i, /double/i, -.1) ? stampTx(1350, 620, '2× !', t, wt(i, /double/i, -.1), { col: '#2fa36b', size: 90 }) : ''); break;
    case 'flow1': case 'flow2': case 'trick': {
      const t1 = k == 'flow2' ? wt(i, /next/i, -.3) : wt(i, /new/i, -.3), box = (x, y, txt, col, s) => card(x, y, `<div style="font-size:52px;color:${col}">${txt}</div>`, s, { pad: '16px 34px' });
      h += box(560, 230, k == 'flow1' ? 'NEW DEPOSITS' : 'NEW INVESTORS', '#2fa36b', S(a + .2)) + box(1360, 230, k == 'flow1' ? 'OLD CUSTOMERS' : 'OLD INVESTORS', '#2a6fd6', S(t1));
      const u = cl(t, t1, t1 + .6); if (u > 0) h += `<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><path d="M780 280 L${780 + 340 * ez(u)} 280" stroke="${OL}" stroke-width="22" stroke-linecap="round"/><path d="M780 280 L${780 + 340 * ez(u)} 280" stroke="#ffd166" stroke-width="12" stroke-linecap="round"/>${u > .9 ? `<path d="M1105 250 L1150 280 L1105 310 Z" fill="#ffd166" stroke="${OL}" stroke-width="6"/>` : ''}</svg><div class="lbl" style="left:960px;top:330px;transform:translateX(-50%);font-size:40px;text-shadow:${shadowTxt(OL, 4)}">${k == 'flow1' ? 'PAYS THE INTEREST' : 'PAYS THE "PROFIT"'}</div>`;
      if (k == 'trick' && t > wt(i, /perfect/i, -.2)) h += stampTx(960, 560, 'LOOKS PERFECT', t, wt(i, /perfect/i, -.2), { col: '#2fa36b', size: 84, rot: -5 });
      break }
    case 'mexico': h += stampTx(560, 300, 'BANK FAILED', t, a + .3, { size: 90 }) + mapCard(t, wt(i, /mexico/i, -.6), 'mex', [-125, -50, 12, 56], { MEX: '#ffd166', CAN: '#f7c6a3', USA: '#f4dca0' }, [[[-73.6, 45.5], 'MONTREAL', wt(i, /mexico/i, -.5)], [[-99.1, 19.4], 'MEXICO', wt(i, /mexico/i, .5)]], [[[-73.6, 45.5], [-99.1, 19.4], wt(i, /mexico/i, -.3)]], { y: 110, h: 560, rot: 2 }).replace('left:960px', 'left:1260px').replace('width:1180px', 'width:900px').replace('width="1180"', 'width="900"'); break;
    case 'check': h += card(1300, 190, `<div style="text-align:left;font:700 34px P,Arial;color:#6b7280">PAY TO THE ORDER OF ...</div><div style="font-size:120px;line-height:1.1;color:#2a6fd6">$423.58</div><div style="text-align:right;font:italic 700 40px P,Arial;color:#6b7280">signature?</div>`, S(wt(i, /check/i, -.3)), { w: 760, rot: -3, bg: '#e9f6ee' }) + stampTx(1300, 330, 'FORGED', t, wt(i, /fifty/i, .2)) + (t > wt(i, /prison/i, -.2) ? pill(1300, 640, 'PRISON IN CANADA', S(wt(i, /prison/i, -.2)), { bg: '#3a3f5c' }) : ''); break;
    case 'atlanta': h += pill(60, 900, 'ATLANTA · SECOND PRISON TERM', S(a + .2), { left: true, bg: '#ffffff', col: OL, size: 40 }); break;
    case 'letter': h += pill(1420, 260, '✉ A LETTER FROM SPAIN', S(wt(i, /letter/i, -.2)), { bg: '#e8483c' }) + (t > wt(i, /international/i, -.2) ? pill(1420, 370, 'INTERNATIONAL REPLY COUPON', S(wt(i, /international/i, -.2)), { bg: '#2fa36b', size: 38 }) : ''); break;
    case 'irc_how': { const st = [[wt(i, /buy/i, -.1), '🛒 BUY A COUPON', 'COUNTRY A'], [wt(i, /mail/i, -.1), '✉ MAIL IT ABROAD', '→'], [wt(i, /trades/i, -.1), '🔁 TRADE FOR A STAMP', 'COUNTRY B']];
      h += st.map(([tt, a1, b1], j) => card(420 + j * 540, 150, `<div style="font-size:30px;color:#6b7280">${j + 1}</div><div style="font-size:46px">${a1}</div>`, S(tt), { rot: j % 2 ? 2 : -2, pad: '14px 30px' })).join(''); break }
    case 'inflation': h += mapCard(t, a + .1, 'eu', [-12, 35, 34, 60], { ITA: '#ffd166', ESP: '#f7c6a3' }, [[[12.5, 42], 'ITALY', wt(i, /italy/i, -.3)], [[-3.7, 40.4], 'SPAIN', a + .4]], [], { y: 80, h: 640 }) + (t > wt(i, /exploded/i, -.2) ? stampTx(1500, 260, 'PRICES ↑↑', t, wt(i, /exploded/i, -.2), { size: 80, rot: 6 }) : '') + (t > wt(i, /cheap/i, -.2) ? stampTx(960, 620, 'COUPONS: CHEAP', t, wt(i, /cheap/i, -.2), { col: '#2fa36b', size: 70, rot: -4 }) : ''); break;
    case 'arb': h += labelAt(ABS('DK', [-5, .2, 1]), pill(0, 0, 'BUY CHEAP 🇮🇹'.replace('🇮🇹', ''), 1, { bg: '#2fa36b' }).replace('position:absolute', 'position:relative'), S(wt(i, /buy/i, -.1))) + labelAt(ABS('DK', [5, .2, 1]), pill(0, 0, 'TRADE FOR MORE', 1, { bg: '#2a6fd6' }).replace('position:absolute', 'position:relative'), S(wt(i, /trade/i, -.1))) + (t > wt(i, /pocket/i, -.1) ? stampTx(960, 300, '+ PROFIT', t, wt(i, /pocket/i, -.1), { col: '#2fa36b', size: 100 }) : ''); break;
    case 'pct400': h += pill(560, 220, '✔ LEGAL (ON PAPER)', S(wt(i, /legal/i, -.2)), { bg: '#2fa36b' }) + bigNum(1300, 330, '400%+', S(wt(i, /four/i, -.1), .5), '#ffd166', 230) + (t > wt(i, /claimed/i, -.2) ? pill(1300, 470, 'HE CLAIMED', S(wt(i, /claimed/i, -.2)), { bg: '#e8483c', size: 40 }) : ''); break;
    case 'catch': h += card(1360, 150, `<div style="font-size:48px">1 COUPON</div><div style="font-size:40px;color:#6b7280">=</div><div style="font-size:48px">1 STAMP</div><div style="font-size:40px;color:#6b7280">=</div><div style="font-size:64px;color:#e8483c">A FEW CENTS</div>`, S(wt(i, /coupon/i, -.2)), { rot: 2 }) + (t > wt(i, /mountains/i, -.2) ? stampTx(560, 300, 'MOUNTAINS NEEDED', t, wt(i, /mountains/i, -.2), { size: 70 }) : ''); break;
    case 'ch3': h += t > a + 2.6 ? card(1400, 190, `<div style="font-size:40px;color:#6b7280">SECURITIES EXCHANGE CO.</div><div style="font-size:110px;line-height:1.05;color:#2fa36b">+50%</div><div style="font-size:46px">IN 45 DAYS</div><div style="font-size:34px;color:#6b7280;margin-top:8px">or +100% in 90 days</div>`, S(a + 2.6), { rot: 3 }) : ''; break;
    case 'paid': { const t0 = wt(i, /paid/i, -.2); for (let j = 0; j < 10; j += 3) h += labelAt(ABS('PY', [((j) - 4.5) * .78, 4.4, 0]), `<div class="pill" style="position:relative;font-size:40px;color:#fff;background:#2fa36b;text-shadow:${shadowTxt(OL, 3)}">+50%</div>`, S(t0 + j * .05)); h += pill(960, 160, 'FRIENDS & NEIGHBORS', S(a + .3), { bg: '#ffffff', col: OL }); break }
    case 'example': {
      const e1 = wt(i, /hundred/i, -.2), e2 = wt(i, /fifty/i, -.2), e3 = wtN(i, /fifteen/i, 1, -.2), e4 = wtN(i, /fifteen/i, 2, -.2);
      const row = (tt, a1, b1, col) => t < tt ? '' : `<div style="display:flex;justify-content:space-between;gap:30px;font-size:50px;margin:8px 0;transform:scale(${pop(t, tt, .3)});transform-origin:0 50%"><span>${a1}</span><span style="color:${col}">${b1}</span></div>`;
      h += card(1440, 110, `<div class="pill" style="position:relative;display:inline-block;font-size:30px;background:#ffd166;color:${OL};border-width:5px;padding:4px 20px">EXAMPLE</div>
        ${row(e1, '10 people × $100', '$1,000', '#2fa36b')}${row(e2, 'after 45 days: 10 × $150', '$1,500', '#e8483c')}${row(e3, 'missing money', '$1,500', '#e8483c')}${row(e4, 'new people needed', '15', '#2a6fd6')}`, S(a + .1), { w: 860, rot: 1.5, pad: '14px 36px' });
      break }
    case 'grow': { const lab = (k2, tt) => labelAt(ABS('PY', [PY.N[k2] * .39 + 1.4, PY.tiers[k2].y + 1.3, PY.tiers[k2].z]), `<div class="pill" style="position:relative;font-size:44px;color:#fff;background:#2a6fd6;text-shadow:${shadowTxt(OL, 3)}">${PY.N[k2]}</div>`, S(tt));
      h += lab(0, a) + lab(1, a + .2) + lab(2, a + .7) + lab(3, wt(i, /round/i, 0)) + (t > wt(i, /grow/i, -.2) ? stampTx(560, 220, 'MUST KEEP GROWING', t, wt(i, /grow/i, -.2), { size: 70, rot: -5 }) : ''); break }
    case 'shout': { const s = pop(t, a - .15, .3), sh2 = Math.sin(t * 40) * 6 * cl(1 - (t - a) / .5, 0, 1);
      h += `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 60%,#ffd16655,transparent 60%)"></div>`;
      h += `<div style="position:absolute;left:${960 + sh2}px;top:1180px;transform:translate(-50%,-100%) scale(${s});transform-origin:50% 100%">${MG_SAM.svg({ w: 760, mouth: 'o', talk: MG_SAM.talk(t, l), blink: 0, armL: [2.6, .3], armR: [2.6, .3] })}</div>`;
      const bs = pop(t, wt(i, /subscribe/i, -.15), .35); h += `<div style="position:absolute;left:1500px;top:330px;transform:translate(-50%,-50%) rotate(-6deg) scale(${bs * (1 + .05 * Math.sin(t * 12))});background:#e8283c;color:#fff;font:900 84px/1 IB,Arial;padding:26px 54px;border-radius:30px;border:8px solid ${OL};box-shadow:0 12px 0 #2328384d">SUBSCRIBE 🔔</div>`;
      if (t > wt(i, /free/i, -.1)) h += pill(420, 330, 'IT\'S FREE!', S(wt(i, /free/i, -.1)), { bg: '#2fa36b', rot: 5, size: 60 }); break }
    case 'perday2': break;
    case 'wordmouth': break;
    case 'mansion': h += pill(60, 900, 'LEXINGTON, MASSACHUSETTS', S(a + .2), { left: true, bg: '#ffffff', col: OL, size: 40 }) + (t > wt(i, /mother/i, -.2) ? pill(1450, 250, '🚢 MOM: FIRST CLASS', S(wt(i, /mother/i, -.2)), { bg: '#7a55c7' }) : ''); break;
    case 'hanover': h += stampTx(1300, 260, 'BOUGHT!', t, wt(i, /controlling/i, -.1), { col: '#2fa36b', size: 100 }) + (t > wt(i, /refused/i, -.3) ? pill(1300, 480, 'THEY ONCE REFUSED HIM A LOAN', S(wt(i, /refused/i, -.3)), { bg: '#e8483c', size: 38 }) : ''); break;
    case 'rich': h += `<div class="lbl" style="left:960px;top:300px;transform:translateX(-50%);font-size:150px;text-shadow:${shadowTxt(OL, 10)}"><span style="color:#35e08a;opacity:${S(a + .2)}">$2.50</span> <span style="opacity:${S(wt(i, /living/i, -.4))}">→</span> <span style="color:#ffd166;display:inline-block;transform:scale(${S(wt(i, /millionaire/i, -.2))})">MILLIONAIRE</span></div>`; break;
    case 'ch5': h += newspaperCard(t, wt(i, /july/i, -.3), 'QUESTIONS ABOUT PONZI', 'Front page · Boston Post', 'JULY 24, 1920'); break;
    case 'barron': h += pill(1380, 230, 'CLARENCE BARRON', S(wt(i, /clarence/i, -.2)), { bg: '#2f4372', size: 54 }) + pill(1380, 330, 'FINANCIAL JOURNALIST', S(wt(i, /journalist/i, -.2)), { bg: '#ffffff', col: OL, size: 36 }) + (t > wt(i, /math/i, -.2) ? stampTx(1380, 500, 'SIMPLE MATH', t, wt(i, /math/i, -.2), { col: '#2a6fd6', size: 76 }) : ''); break;
    case 'c160m': { const t0 = wt(i, /hundred/i, -.3), v = ez(cl(t, t0, t0 + 1.8)); h += `<div class="lbl" style="left:1300px;top:170px;transform:translateX(-50%) scale(${S(t0 - .2)})"><div class="pill" style="position:relative;display:inline-block;font-size:42px;color:${OL};background:#ffd166">COUPONS NEEDED</div><div style="font-size:140px;line-height:1.1;color:#ffd166;text-shadow:${shadowTxt(OL, 9)}">${fmt(160e6 * v)}</div></div>`; break }
    case 'c27k': h += `<div class="lbl" style="left:960px;top:150px;transform:translateX(-50%) scale(${S(a)})"><div class="pill" style="position:relative;display:inline-block;font-size:42px;color:#fff;background:#2a6fd6;text-shadow:${shadowTxt(OL, 3)}">IN CIRCULATION</div><div style="font-size:170px;line-height:1.1;color:#9fdcff;text-shadow:${shadowTxt(OL, 9)}">${fmt(27000 * ez(cl(t, wt(i, /twenty/i, -.2), wt(i, /thousand/i, .4))))}</div></div>` + (t > wt(i, /circulation/i, 0) ? stampTx(960, 620, 'IMPOSSIBLE', t, wt(i, /circulation/i, 0), { size: 110 }) : ''); break;
    case 'run2m': { const t0 = wt(i, /two/i, -.2), v = ez(cl(t, t0, t0 + 1.4)); h += `<div class="lbl" style="left:960px;top:150px;transform:translateX(-50%) scale(${S(t0 - .2)})"><div style="font-size:170px;line-height:1.05;color:#35e08a;text-shadow:${shadowTxt(OL, 10)}">$${fmt(2e6 * v)}</div><div class="pill" style="position:relative;display:inline-block;font-size:56px;color:#fff;background:#e8483c;text-shadow:${shadowTxt(OL, 4)}">IN 3 DAYS</div></div>`; break }
    case 'mcmasters': h += newspaperCard(t, a + .1, '"DEEP IN DEBT"', 'Former publicist William McMasters goes public', 'AUGUST 2, 1920', { y: 430 }) + (t > wt(i, /robbing/i, -.2) ? card(960, 760, `<div style="font-size:56px">“ROBBING PETER TO PAY PAUL”</div>`, S(wt(i, /robbing/i, -.2)), { rot: -2, bg: '#ffd166', pad: '10px 36px' }) : ''); break;
    case 'forgery': h += newspaperCard(t, a + .1, 'PONZI\'S PAST: FORGERY', 'Old conviction from Montreal revealed', 'AUGUST 11, 1920'); break;
    case 'aug12': h += pill(60, 900, 'AUGUST 12, 1920', S(a + .2), { left: true, bg: '#ffffff', col: OL, size: 40 }) + stampTx(1450, 300, 'SURRENDERS', t, wt(i, /turned/i, -.1), { col: '#2f4372', size: 90 }); break;
    case 'audit': h += stampTx(960, 260, 'MILLIONS IN DEBT', t, wt(i, /millions/i, -.1), { size: 100 }); break;
    case 'ch6': if (t > a + 2.6) { const t0 = wt(i, /twenty/i, -.2); h += bigNum(560, 330, '-$' + Math.round(20 * ez(cl(t, t0, t0 + 1.2))) + ' MILLION', S(t0), '#ff6b5b', 110) } if (t > wt(i, /thirty/i, -.3)) h += card(1440, 520, `<div style="font-size:42px;color:#6b7280">GOT BACK PER $1</div><div style="font-size:120px;line-height:1;color:#e8483c">&lt;30¢</div>`, S(wt(i, /thirty/i, -.3)), { rot: 3 }); break;
    case 'seized': h += stampTx(1300, 260, 'SEIZED', t, wt(i, /seized/i, -.1), { size: 130 }); break;
    case 'counts': h += bigNum(1400, 260, '86', S(wt(i, /eighty/i, -.2), .4), '#ffd166', 200) + pill(1400, 400, 'COUNTS OF MAIL FRAUD', S(wt(i, /mail/i, -.2)), { bg: '#e8483c' }) + (t > wt(i, /guilty/i, -.2) ? pill(1400, 500, 'PLEADED GUILTY TO ONE', S(wt(i, /guilty/i, -.2)), { bg: '#2f4372', size: 38 }) : ''); break;
    case 'state': h += pill(1400, 230, '~3.5 YEARS', S(wt(i, /three/i, -.2)), { bg: '#2f4372', size: 56 }) + (t > wt(i, /massachusetts/i, -.2) ? stampTx(1400, 420, 'TRIAL #2', t, wt(i, /massachusetts/i, -.2), { col: '#2a6fd6', size: 90 }) : ''); break;
    case 'florida': h += pill(60, 900, 'FLORIDA · OUT ON BAIL', S(a + .2), { left: true, bg: '#ffffff', col: OL, size: 40 }) + (t > wt(i, /two/i, -.2) ? bigNum(1450, 300, '200%', S(wt(i, /two/i, -.2), .4), '#ffd166', 160) + pill(1450, 430, 'IN 60 DAYS', S(wt(i, /sixty/i, -.2)), { bg: '#e8483c' }) : ''); break;
    case 'again': h += stampTx(1350, 300, 'CAUGHT AGAIN', t, wt(i, /caught/i, -.1), { size: 100 }); break;
    case 'deport': h += mapCard(t, a + .1, 'atl', [-100, 45, -38, 60], { ITA: '#ffd166', BRA: '#7ee08a', USA: '#f7c6a3' }, [[[-71.06, 42.36], 'BOSTON', a + .2], [[12.5, 41.9], 'ITALY 1934', wt(i, /italy/i, 0)], [[-43.2, -22.9], 'BRAZIL', wt(i, /brazil/i, 0)]], [[[-71.06, 42.36], [12.5, 41.9], wt(i, /deported/i, -.1), '#e8483c'], [[12.5, 41.9], [-43.2, -22.9], wt(i, /moved/i, -.2), '#2fa36b']], { y: 70, h: 760 }); break;
    case 'dollars75': h += pill(60, 900, 'RIO DE JANEIRO · 1949', S(a + .2), { left: true, bg: '#ffffff', col: OL, size: 40 }) + bigNum(1450, 330, '$75', S(wt(i, /seventy/i, -.2), .5), '#35e08a', 230) + (t > wt(i, /seventy/i, .3) ? pill(1450, 500, 'LEFT BEHIND', S(wt(i, /seventy/i, .3)), { bg: '#3a3f5c' }) : ''); break;
    case 'pulitzer': h += newspaperCard(t, a, 'PULITZER PRIZE', 'For exposing the Ponzi scheme', '1921', { y: 470, hs: 96 }) + (t > wt(i, /pulitzer/i, -.1) ? `<div style="position:absolute;left:1560px;top:360px;transform:translate(-50%,-50%) rotate(12deg) scale(${pop(t, wt(i, /pulitzer/i, -.1), .4)})"><svg width="260" height="300" viewBox="0 0 260 300"><path d="M90 150 L60 290 L110 260 L130 300 L150 150 Z" fill="#e8483c" stroke="${OL}" stroke-width="8"/><path d="M170 150 L200 290 L150 260 L130 300 L110 150 Z" fill="#2a6fd6" stroke="${OL}" stroke-width="8"/><circle cx="130" cy="110" r="96" fill="#ffd166" stroke="${OL}" stroke-width="10"/><circle cx="130" cy="110" r="66" fill="none" stroke="#c99a2e" stroke-width="8"/><text x="130" y="132" text-anchor="middle" font-family="IB,Arial" font-weight="900" font-size="64" fill="${OL}">1st</text></svg></div>` : ''); break;
    case 'madoff': h += card(1380, 160, `<div style="font-size:44px;color:#6b7280">2009 · BERNIE MADOFF</div><div style="font-size:140px;line-height:1.05;color:#e8483c">~$65 BILLION</div><div style="font-size:40px">PONZI SCHEME</div>`, S(wt(i, /madoff/i, -.2)), { rot: 2 }) + pill(560, 230, '100 YEARS LATER', S(a + .2), { bg: '#2a6fd6' }); break;
    case 'spot': case 'spot1': case 'spot2': case 'spot3': {
      const n = { spot: 0, spot1: 1, spot2: 2, spot3: 3 }[k], items = ['HIGH, "GUARANTEED" RETURNS', 'A SECRET STRATEGY', 'PAID WITH NEWER INVESTORS\' MONEY'];
      let rows = items.map((it, j) => { const on = j < n || (j == n - 1); if (j >= n) return ''; const s2 = j == n - 1 ? pop(t, a + .05, .4) : 1;
        return `<div style="display:flex;align-items:center;gap:22px;margin:18px 0;transform:scale(${s2});transform-origin:0 50%"><span>${flagIcon}</span><span style="font-size:52px;text-align:left">${j + 1}. ${it}</span></div>` }).join('');
      h += card(1250, 170, `<div style="font-size:62px;color:#e8483c">🚩 3 RED FLAGS</div>${rows}`, k == 'spot' ? pop(t, a + .2, .45) : 1, { w: 1080, rot: 1, pad: '24px 44px' });
      break }
    case 'end': h += `<div style="position:absolute;left:1350px;top:420px;transform:translate(-50%,-50%) rotate(-4deg) scale(${pop(t, wt(i, /subscribe/i, -.2), .4) * (1 + .04 * Math.sin(t * 8))});background:#e8283c;color:#fff;font:900 90px/1 IB,Arial;padding:28px 60px;border-radius:30px;border:8px solid ${OL};box-shadow:0 12px 0 #2328384d">SUBSCRIBE 🔔</div>` + pill(1350, 620, 'ROUNDHEAD STORIES', S(wt(i, /roundhead/i, -.2)), { bg: '#ffffff', col: OL, size: 52 }); break;
  }
  if (sh == 'word_mouth') { const Bs = ['50%!!', 'IT WORKS!', 'MY NEIGHBOR GOT PAID!', '45 DAYS!']; [2, 7, 12, 17].forEach((q, j) => { const p = ST.queue[q]; if (!p) return; h += labelAt([p.m.pos[0], 2.35, p.m.pos[2]], `<div class="card" style="position:relative;padding:8px 24px;font-size:38px;border-radius:24px">${Bs[j]}</div>`, pop(t, a + .3 + j * .45, .35) * out) }) }
  // Karten-Einstellungen
  if (sh == 'map_italy') h += pill(960, 700, '🇮🇹 BORN IN ITALY · 1882'.replace('🇮🇹 ', ''), pop(t, a + 1.0, .4) * out, { bg: '#2fa36b', size: 52 });
  // Sam im Studio
  if (sh == 'sam_studio' || sh == 'sam_end') { const n = MG.cur(t), up = SPEC(n).ui; h += samSVG(t, 470, 1000, 470, { armR: up == 'end' ? [2.5 + .3 * Math.sin(t * 9), .3] : up == 'spot' ? [1.4, -.2] : [1.1, -.1], mouth: up == 'end' ? 'grin' : 'smile', look: [4, -2] }) }
  return h;
}
