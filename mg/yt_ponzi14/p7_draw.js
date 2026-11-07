// ===================== Draw =====================
window.ready = false;
Promise.all(['900 40px IB', '700 40px P', '900 40px "Cinzel Decorative"'].map(f => document.fonts.load(f))).then(() => { TEXQ.forEach(f => f()); window.ready = true }).catch(() => { TEXQ.forEach(f => f()); window.ready = true });
window.setTimeline = tl => { MG.TL = tl; CHAP = []; tl.lines.forEach((l, i) => { const k = (l.spec || {}).ui; if (CH[k]) CHAP.push({ t: l.start, k: CH[k] }) }) };
let lastSet = null;
window.draw = function (t) {
  const c = camAt(t), sh = SPEC(c.i).shot;
  // Sets ein-/ausblenden
  for (const s in SETM) { const on = s == c.set; for (const m of SETM[s]) m.vis = on ? m._v : false }
  w.cam.pos = c.pos; w.cam.at = c.at; w.cam.fov = c.fov;
  w.shadowCenter = [c.at[0], 0, c.at[2]]; w.shadowSize = Math.min(48, 12 + Math.hypot(...G.v.sub(c.pos, c.at)) * .9);
  const L = LIGHTS[SHOT_LIGHT[sh]] || DAY; for (const k of ['sunCol', 'sky', 'gnd', 'fog']) w[k] = L[k];
  $('stage').style.background = L.bg;
  if (ANIM[c.set]) ANIM[c.set](t, sh, c.i, c.rt);
  w.render(t);
  // Hintergrund-Unschaerfe, wenn eine grosse Karte/Zeitung im Bild ist
  const blurOn = /^map_|^newspaper/.test(sh) || ['compare', 'mexico', 'deport', 'inflation', 'shout', 'title', 'example'].includes(SPEC(c.i).ui);
  $('cv').style.filter = blurOn ? 'blur(5px) saturate(.85) brightness(1.05)' : 'none';
  let fx = '';
  if (sh == 'sam_shout') fx += `<div style="position:absolute;inset:0;background:#ffd166;opacity:.35"></div>`;
  // kurzer Weissblitz bei Kapitelwechsel
  for (const ch of CHAP) { const f = cl(t, ch.t - .45, ch.t - .1); if (f > 0 && f < 1) fx += `<div style="position:absolute;inset:0;background:#fff;opacity:${Math.sin(f * Math.PI) * .9}"></div>` }
  fx += `<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 62%,#0b163344 100%)"></div>`;
  $('fx').innerHTML = fx;
  $('ui').innerHTML = ui(t) + MG.captions(t, { y: 975, size: 52, maxWords: 4, stageW: 1920, w: 1500, upper: true, hl: '#ffd166' }).replace(/'Arial Black',Arial/, 'IB,Arial');
};
window.sfxEvents = function () {
  const E = [], n = NL();
  let prevSet = null;
  for (let i = 0; i < n; i++) {
    const l = Lt(i), sp = SPEC(i), set = (SH[sp.shot] || SH.title)[0], k = sp.ui;
    if (set != prevSet) E.push({ k: 'whoosh', t: l.start - .35, d: .6, g: .7 }); prevSet = set;
    if (CH[k]) E.push({ k: 'impact', t: l.start - .05 }, { k: 'swish', t: l.start + .1, d: .5 });
    const W = (re, d = 0) => wt(i, re, d);
    switch (k) {
      case 'promise': E.push({ k: 'chime', t: W(/fifty/i) }, { k: 'ding', t: W(/days/i) }); break;
      case 'compare': E.push({ k: 'swish', t: l.start + .3, d: .8 }, { k: 'impact', t: W(/year/i, -.05) }); break;
      case 'perday': case 'perday2': for (let j = 0; j < 10; j++) E.push({ k: 'cash', t: W(/two/i) + j * .15 }); break;
      case 'title': E.push({ k: 'impact', t: W(/ponzi/i, -.15) }, { k: 'shimmer', t: W(/famous/i) }); break;
      case 'cash250': E.push({ k: 'coin', t: W(/two/i) }, { k: 'coin', t: W(/two/i) + .15 }); break;
      case 'fired': E.push({ k: 'pop', t: W(/washed/i) }, { k: 'pop', t: W(/waited/i) }, { k: 'thud', t: W(/fired/i, -.4) }, { k: 'impact', t: W(/fired/i) }); break;
      case 'sixpct': E.push({ k: 'chime', t: l.start + .3 }, { k: 'ding', t: W(/double/i) }); break;
      case 'flow1': case 'flow2': case 'trick': E.push({ k: 'swish', t: W(/new|next/i, -.3), d: .6 }); break;
      case 'mexico': E.push({ k: 'impact', t: l.start + .3 }, { k: 'whoosh', t: W(/mexico/i, -.3), d: 1 }); break;
      case 'check': E.push({ k: 'paper', t: W(/check/i, -.3) }, { k: 'impact', t: W(/fifty/i, .2) }, { k: 'thud', t: W(/prison/i) }); break;
      case 'atlanta': E.push({ k: 'thud', t: l.start + .3 }); break;
      case 'letter': E.push({ k: 'paper', t: l.start + .1 }, { k: 'pop', t: W(/international/i, -.2) }); break;
      case 'irc_how': E.push({ k: 'pop', t: W(/buy/i, -.1) }, { k: 'pop', t: W(/mail/i, -.1) }, { k: 'pop', t: W(/trades/i, -.1) }); break;
      case 'inflation': E.push({ k: 'impact', t: W(/exploded/i, -.1) }, { k: 'ding', t: W(/cheap/i, -.1) }); break;
      case 'arb': E.push({ k: 'pop', t: W(/buy/i) }, { k: 'pop', t: W(/trade/i) }, { k: 'cash', t: W(/pocket/i) }); break;
      case 'pct400': E.push({ k: 'chime', t: W(/legal/i) }, { k: 'impact', t: W(/four/i) }); break;
      case 'catch': E.push({ k: 'error', t: W(/catch/i) }, { k: 'impact', t: W(/mountains/i, -.1) }); break;
      case 'paid': for (let j = 0; j < 4; j++) E.push({ k: 'coin', t: W(/paid/i) + j * .12 }); break;
      case 'example': [W(/hundred/i, -.2), W(/fifty/i, -.2), wtN(i, /fifteen/i, 1, -.2), wtN(i, /fifteen/i, 2, -.2)].forEach(x => E.push({ k: 'pop', t: x })); break;
      case 'grow': E.push({ k: 'pop', t: l.start + .7 }, { k: 'pop', t: W(/round/i) }, { k: 'impact', t: W(/grow/i, -.1) }); break;
      case 'shout': E.push({ k: 'impact', t: l.start - .1 }, { k: 'bell', t: W(/subscribe/i) }, { k: 'pop', t: W(/free/i) }); break;
      case 'hanover': E.push({ k: 'impact', t: W(/controlling/i) }, { k: 'error', t: W(/refused/i) }); break;
      case 'rich': E.push({ k: 'shimmer', t: W(/millionaire/i, -.2) }); break;
      case 'ch5': case 'mcmasters': case 'forgery': case 'pulitzer': E.push({ k: 'paper', t: (k == 'ch5' ? W(/july/i, -.3) : l.start + .1) }, { k: 'swish', t: (k == 'ch5' ? W(/july/i, -.3) : l.start + .1), d: .7 }, { k: 'impact', t: (k == 'ch5' ? W(/july/i, .4) : l.start + .8) }); break;
      case 'barron': E.push({ k: 'pop', t: W(/clarence/i) }, { k: 'tick', t: W(/math/i) }); break;
      case 'c160m': for (let j = 0; j < 12; j++) E.push({ k: 'tick', t: W(/hundred/i, -.3) + j * .15 }); break;
      case 'c27k': E.push({ k: 'error', t: W(/circulation/i) }, { k: 'impact', t: W(/circulation/i, .05) }); break;
      case 'run2m': for (let j = 0; j < 8; j++) E.push({ k: 'cash', t: W(/two/i) + j * .17 }); break;
      case 'aug12': E.push({ k: 'impact', t: W(/turned/i) }); break;
      case 'audit': E.push({ k: 'impact', t: W(/millions/i) }); break;
      case 'seized': E.push({ k: 'impact', t: W(/seized/i) }, { k: 'thud', t: W(/seized/i, .1) }); break;
      case 'counts': E.push({ k: 'impact', t: W(/eighty/i) }, { k: 'thud', t: W(/guilty/i) }); break;
      case 'state': E.push({ k: 'thud', t: W(/massachusetts/i) }); break;
      case 'florida': E.push({ k: 'chime', t: W(/two/i) }); break;
      case 'again': E.push({ k: 'impact', t: W(/caught/i) }, { k: 'thud', t: W(/caught/i, .15) }); break;
      case 'deport': E.push({ k: 'whoosh', t: W(/deported/i), d: 1 }, { k: 'whoosh', t: W(/moved/i), d: 1 }); break;
      case 'dollars75': E.push({ k: 'coin', t: W(/seventy/i) }); break;
      case 'madoff': E.push({ k: 'impact', t: W(/madoff/i) }); break;
      case 'spot1': case 'spot2': case 'spot3': E.push({ k: 'pop', t: l.start + .05 }, { k: 'ding', t: l.start + .2 }); break;
      case 'end': E.push({ k: 'bell', t: W(/subscribe/i) }); break;
    }
    if (sp.shot == 'ship') { E.push({ k: 'wave', t: l.start, d: 4, g: .5 }, { k: 'gull', t: l.start + 1 }) }
    if (sp.shot == 'pyr_crash' || sp.shot == 'crash_teaser') { E.push({ k: 'impact', t: l.start + .3 }); for (let j = 0; j < 8; j++) E.push({ k: 'thud', t: l.start + .5 + j * .18, g: .6 }) }
    if (sp.shot == 'arrest') E.push({ k: 'tap', t: l.start + .4 }, { k: 'tap', t: l.start + .9 }, { k: 'tap', t: l.start + 1.4 });
    if (sp.shot == 'court') E.push({ k: 'tap', t: l.start + .3 }, { k: 'tap', t: l.start + .5 });
  }
  return E.filter(e => e.t >= 0);
};
