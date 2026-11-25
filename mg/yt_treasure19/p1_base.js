// ===================== YT19 Lost Treasures – Basis (gl3d Toon + 2D-Figuren) =====================
const W = 1920, H = 1080, G = GL3D, {cl, ez, ei, bo, lerp} = MG;
const $ = id => document.getElementById(id);
const OL = '#232838', PI = Math.PI;
const shadowTxt = (c = OL, r = 5) => MG.outline(r).replace(/#000/g, c);
const w = G.World($('cv'), W, H, 1.5);
w.toon = true; w.rim = .34; w.outline = .0017;
const at = (g, p, r = [0, 0, 0], s = [1, 1, 1]) => [g, G.m4.compose(p, r, s)];
function merge(list) { const g = new G.Geo(); list.forEach(([a, m]) => g.add(a, m)); return g }
// ---------- Sets: jedes Set an eigenem Ort, nur das aktive ist sichtbar ----------
const SETS = {};
function mk(set, geo, o = {}) { const m = w.mesh(geo, o); (SETS[set] || (SETS[set] = [])).push(m); m._v = o.vis ?? true; return m }
function showSet(name) { for (const k in SETS) SETS[k].forEach(m => { if (k != name) m.vis = false; else if (m._auto !== false) m.vis = m._v }) }
function tex(wd, ht, fn) { const c = document.createElement('canvas'); c.width = wd; c.height = ht; fn(c.getContext('2d'), wd, ht); return w.texture(c) }
const TEXQ = [];
function texPlane(set, wd, ht, fn, o = {}) { const m = mk(set, G.plane(wd, ht, 1, 1, '#ffffff'), Object.assign({ outline: false, cast: false }, o)); TEXQ.push(() => m.tex = fn()); return m }
// Licht-Stimmungen
const LIGHT = {
  deep: { sun: [.2, .95, .2], sunCol: '#a8e4ff', sky: '#3a8ac0', gnd: '#1a3a5a', fog: '#0b2a48', fogN: 10, fogF: 60, shCol: '#1a3a70', bg: 'linear-gradient(#0d3a66 0%,#082646 60%,#051a33 100%)' },
  amber: { sun: [.3, .85, .45], sunCol: '#ffe2a8', sky: '#ffd9a0', gnd: '#8a5a2a', fog: '#6a4426', fogN: 60, fogF: 200, shCol: '#a0603a', bg: '#4a2e1a' },
  storm: { sun: [.6, .5, .4], sunCol: '#ffc890', sky: '#c9a8a0', gnd: '#5a5a6a', fog: '#8a7a86', fogN: 60, fogF: 260, shCol: '#6a5a8a', bg: 'linear-gradient(#3a3a5a 0%,#8a6a7a 45%,#f0a070 75%,#f6c890 100%)' },
  night: { sun: [.4, .7, .5], sunCol: '#9fb2ec', sky: '#2c3a6e', gnd: '#202640', fog: '#1d2748', fogN: 40, fogF: 160, shCol: '#3a3f78', bg: 'radial-gradient(ellipse at 70% 20%,#3d4f8f 0%,#1d2748 55%,#141a33 100%)' },
  indoorWarm: { sun: [.3, .85, .45], sunCol: '#ffe6c0', sky: '#f3dcc0', gnd: '#7a5a44', fog: '#4a3a34', fogN: 60, fogF: 200, shCol: '#8a6a8a', bg: '#3a2c2a' },
  indoorDark: { sun: [.3, .85, .45], sunCol: '#b6c0e6', sky: '#6a74a0', gnd: '#2a2c40', fog: '#22263a', fogN: 40, fogF: 140, shCol: '#454a80', bg: '#1c2033' },
  day: { sun: [.55, .75, .35], sunCol: '#fff1d6', sky: '#cfe9ff', gnd: '#b9a27a', fog: '#cfe6f6', fogN: 70, fogF: 260, shCol: '#8c9be0', bg: 'linear-gradient(#7fb6ea 0%,#bfe0f8 55%,#e8f3fb 100%)' },
  vault: { sun: [.3, .85, .45], sunCol: '#eef2ff', sky: '#c4cce6', gnd: '#5a5e70', fog: '#3a4058', fogN: 50, fogF: 160, shCol: '#7a84b8', bg: '#2a3044' },
  dusk: { sun: [.62, .45, .4], sunCol: '#ffd9a8', sky: '#f2c9a0', gnd: '#8a7a66', fog: '#e8c4a4', fogN: 60, fogF: 240, shCol: '#7f86c8', bg: 'linear-gradient(#5a7fc6 0%,#b9b6d6 40%,#f6cfa0 70%,#f3b27a 100%)' },
};
function setLight(k) { const L = LIGHT[k]; w.sun = G.v.norm(L.sun); w.sunCol = G.hex(L.sunCol); w.sky = G.hex(L.sky); w.gnd = G.hex(L.gnd); w.fog = G.hex(L.fog); w.fogN = L.fogN; w.fogF = L.fogF; w.shCol = G.hex(L.shCol); $('bg').style.background = L.bg }
// ---------- Figuren (2D-SVG, wie ys_bridge) ----------
const HAT = {
  cap: `<path d="M38,50 Q38,8 100,6 Q162,8 162,50 Q100,40 38,50Z" fill="#8a6a4a" stroke="${OL}" stroke-width="6"/><path d="M128,44 Q176,40 188,56 Q150,62 124,54Z" fill="#6e523a" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/>`,
  cop: `<path d="M36,44 L42,4 Q100,-10 158,4 L164,44 Z" fill="#1b2f6b" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/><circle cx="100" cy="24" r="10" fill="#ffd166" stroke="${OL}" stroke-width="4"/><path d="M40,42 Q100,60 160,42 L156,52 Q100,70 44,52Z" fill="#11131c" stroke="${OL}" stroke-width="4"/>`,
  beanie: `<path d="M40,52 Q36,2 100,0 Q164,2 160,52 Q100,42 40,52Z" fill="#2a2a33" stroke="${OL}" stroke-width="6"/><rect x="40" y="40" width="120" height="16" rx="6" fill="#3a3a46" stroke="${OL}" stroke-width="5"/>`,
  balaclava: `<path d="M38,96 Q30,10 100,14 Q170,10 162,96 Q164,150 100,152 Q36,150 38,96Z" fill="#23232c" stroke="${OL}" stroke-width="6"/><rect x="62" y="70" width="78" height="30" rx="14" fill="#f7e4b5" stroke="${OL}" stroke-width="4"/>`,
  driver: `<path d="M40,48 Q40,12 100,10 Q160,12 160,48 Z" fill="#2c3550" stroke="${OL}" stroke-width="6"/><path d="M36,44 L164,44 L170,56 L30,56Z" fill="#1b2236" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/>`,
  guard: `<path d="M38,46 Q40,8 100,6 Q160,8 162,46 Z" fill="#5a6070" stroke="${OL}" stroke-width="6"/><path d="M34,42 Q100,60 166,42 L162,54 Q100,70 38,54Z" fill="#2a2e3a" stroke="${OL}" stroke-width="4"/>`,
  detective: `<path d="M46,48 Q42,2 100,0 Q158,2 154,48Z" fill="#a07a4a" stroke="${OL}" stroke-width="6"/><path d="M30,48 Q100,34 170,48 Q172,60 100,58 Q28,60 30,48Z" fill="#8a6438" stroke="${OL}" stroke-width="5"/>`,
  grey: `<path d="M50,40 Q60,14 100,16 Q140,14 150,40 Q130,28 100,30 Q70,28 50,40Z" fill="#e8e8ee" stroke="${OL}" stroke-width="5"/>`,
};
const MID = {
  tie: `<path d="M84,150 L100,176 L116,150Z" fill="#fff" stroke="${OL}" stroke-width="3"/><path d="M100,160 L92,176 L100,214 L108,176Z" fill="#c0303a" stroke="${OL}" stroke-width="3"/>`,
  buttons: `<circle cx="100" cy="178" r="5" fill="#ffd166" stroke="${OL}" stroke-width="2"/><circle cx="100" cy="200" r="5" fill="#ffd166" stroke="${OL}" stroke-width="2"/><circle cx="100" cy="222" r="5" fill="#ffd166" stroke="${OL}" stroke-width="2"/>`,
  badge: `<path d="M112,168 l10,0 l4,8 l-4,8 l-10,0 l-4,-8z" fill="#ffd166" stroke="${OL}" stroke-width="3"/>`,
  stripes: `<rect x="56" y="176" width="88" height="10" fill="#555"/><rect x="54" y="206" width="92" height="10" fill="#555"/>`,
};
const SWEAT = `<path d="M160,40 Q172,62 160,70 Q148,62 160,40Z" fill="#8fd3ff" stroke="${OL}" stroke-width="4"/>`;
const LOOK = {
  sam: { hat: HAT.cap },
  thief: { sw: '#2b2b36', swd: '#1e1e28', pa: '#2f2f3a', hat: HAT.beanie },
  mask: { sw: '#2b2b36', swd: '#1e1e28', pa: '#2f2f3a', hat: HAT.balaclava },
  cop: { sw: '#22408e', swd: '#183070', pa: '#1a2a55', hat: HAT.cop, mid: MID.buttons },
  fakecop: { sw: '#22408e', swd: '#183070', pa: '#1a2a55', hat: HAT.cop, mid: MID.buttons },
  guard: { sw: '#6a7080', swd: '#555a68', pa: '#3a3e4a', hat: HAT.guard, mid: MID.badge },
  driver: { sw: '#2c3550', swd: '#1f273d', pa: '#2a3045', hat: HAT.driver },
  smock: { sw: '#f2f2ea', swd: '#d6d6cc', pa: '#5a4a3a' },
  suit: { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', mid: MID.tie },
  old: { sw: '#6b5a4a', swd: '#57483a', pa: '#3e3a36', hat: HAT.grey },
  prisoner: { sw: '#d0d0d0', swd: '#9a9a9a', pa: '#9a9a9a', mid: MID.stripes },
  det: { sw: '#a07a4a', swd: '#8a6438', pa: '#5e4a36', hat: HAT.detective },
};
// p: Fusspunkt in 3D, H3: Figurenhoehe in Welt-Einheiten
function fig(p, who, o = {}, H3 = 1.75) {
  const q = w.project(p); if (!q.vis) return '';
  const s = q.s * H3 / 350 * 240;
  const oo = Object.assign({}, LOOK[who] || {}, o);
  if (o.sweat) oo.hat = (oo.hat || '') + SWEAT;
  return `<div style="position:absolute;left:${(q.x - s / 240 * 120).toFixed(1)}px;top:${(q.y - s / 240 * 342).toFixed(1)}px;width:${s.toFixed(1)}px;z-index:${Math.round(1000 - q.z)}">${MG_SAM.svg(Object.assign(oo, { w: s }))}</div>`;
}
const walk = (t, sp = 9) => ({ legL: .35 * Math.sin(t * sp), legR: -.35 * Math.sin(t * sp), bob: Math.abs(Math.sin(t * sp)) * 6 });
const tk = (t, i) => MG_SAM.talk(t, MG.L(i)), bl = (t, k) => MG_SAM.blink(t + k);
// Requisiten (SVG in der Hand)
const PROP = {
  sack: `<g transform="translate(-30,-10)"><path d="M6,0 Q30,-10 54,0 L60,56 Q30,66 0,56Z" fill="#c9b48a" stroke="${OL}" stroke-width="5"/><path d="M14,8 Q30,2 46,8" stroke="${OL}" stroke-width="4" fill="none"/><text x="30" y="42" text-anchor="middle" font-family="IB,Arial" font-weight="900" font-size="20" fill="#7a5a2a">£</text></g>`,
  cash: `<g transform="translate(-34,-22) rotate(-10)"><rect x="0" y="0" width="68" height="40" rx="5" fill="#5fb06a" stroke="${OL}" stroke-width="5"/><rect x="28" y="0" width="12" height="40" fill="#f4efe2" stroke="${OL}" stroke-width="3"/></g>`,
  glove: `<g transform="translate(-20,-26)"><path d="M6,40 L4,14 Q4,6 10,6 L12,26 L14,2 Q20,-2 22,4 L22,24 L26,4 Q32,0 34,6 L32,26 L38,10 Q44,8 44,14 L38,44 Q30,54 14,52Z" fill="#6b4a2e" stroke="${OL}" stroke-width="4"/></g>`,
  cosh: a => `<g transform="rotate(${a})"><rect x="-6" y="-62" width="12" height="70" rx="6" fill="#3a3a44" stroke="${OL}" stroke-width="4"/></g>`,
  magnifier: `<g transform="translate(-4,-6) rotate(-20)"><rect x="-6" y="0" width="12" height="46" rx="5" fill="#8a5a32" stroke="${OL}" stroke-width="4"/><circle cx="0" cy="-28" r="30" fill="#bfe6ff88" stroke="${OL}" stroke-width="7"/><circle cx="-8" cy="-36" r="8" fill="#fff" opacity=".7"/></g>`,
  drill: `<g transform="translate(-10,-20)"><rect x="0" y="0" width="70" height="34" rx="8" fill="#e0303a" stroke="${OL}" stroke-width="5"/><rect x="66" y="10" width="44" height="12" fill="#c9ccd4" stroke="${OL}" stroke-width="4"/><rect x="14" y="30" width="18" height="34" rx="5" fill="#2a2a33" stroke="${OL}" stroke-width="4"/></g>`,
  axe: a => `<g transform="rotate(${a})"><rect x="-5" y="-80" width="10" height="90" rx="4" fill="#a0703a" stroke="${OL}" stroke-width="4"/><path d="M4,-82 L34,-92 Q42,-70 34,-50 L4,-58Z" fill="#c9ccd4" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/></g>`,
  painting: `<g transform="translate(-50,-80)"><rect x="0" y="0" width="100" height="80" rx="3" fill="#2e4a6a" stroke="#c9a23c" stroke-width="9"/><path d="M14,58 Q40,30 60,50 Q76,30 88,58Z" fill="#e8d8a8"/></g>`,
  bag: `<g transform="translate(-34,-6)"><path d="M4,10 Q34,-4 64,10 L68,58 Q34,68 0,58Z" fill="#2a2a33" stroke="${OL}" stroke-width="5"/><path d="M20,10 Q34,-14 48,10" stroke="${OL}" stroke-width="5" fill="none"/></g>`,
  sandwich: `<g transform="translate(-30,-16)"><path d="M0,20 Q30,0 60,20 L60,30 Q30,22 0,30Z" fill="#e8b866" stroke="${OL}" stroke-width="4"/><rect x="2" y="26" width="56" height="6" fill="#d64545"/><path d="M0,34 Q30,28 60,34 L58,42 Q30,48 2,42Z" fill="#e8b866" stroke="${OL}" stroke-width="4"/></g>`,
  spray: `<g transform="translate(-10,-40)"><rect x="0" y="10" width="22" height="46" rx="5" fill="#d35fa0" stroke="${OL}" stroke-width="4"/><rect x="5" y="0" width="12" height="12" fill="#c9ccd4" stroke="${OL}" stroke-width="3"/></g>`,
};
// ---------- UI-Helfer ----------
const pop = (t, t0, d = .35) => bo(cl(t, t0, t0 + d));
const fade = (t, t0, t1) => 1 - ez(cl(t, t0, t1));
function stampAt(x, y, t, t0, txt, col, size = 110, rot = -8, t1 = 1e9) {
  if (t < t0 || t > t1) return '';
  return `<div style="position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%) rotate(${rot}deg) scale(${lerp(2.4, 1, ez(cl(t, t0, t0 + .15))) * fade(t, t1 - .2, t1)});border:11px solid ${col};border-radius:22px;padding:2px 30px;color:${col};background:#ffffffe0;font:900 ${size}px/1.0 IB,Arial;white-space:nowrap;z-index:2000">${txt}</div>`;
}
const PILL = (txt, bg, col = '#fff', fs = 44) => `<div class="pill" style="position:relative;display:inline-block;font-size:${fs}px;color:${col};background:${bg};${col == '#fff' ? 'text-shadow:' + shadowTxt(OL, 3) : ''}">${txt}</div>`;
function pillAt(x, y, t, t0, t1, txt, bg, col = '#fff', fs = 44) {
  if (t < t0 || t > t1) return '';
  return `<div style="position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%) scale(${pop(t, t0) * fade(t, t1 - .2, t1)});z-index:2200">${PILL(txt, bg, col, fs)}</div>`;
}
function labelAt(p, html, t, t0, t1) {
  if (t < t0 || t > t1) return ''; const q = w.project(p); if (!q.vis) return '';
  const k = pop(t, t0, .4) * fade(t, t1 - .2, t1);
  return `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%) scale(${k});transform-origin:50% 100%;z-index:2100">${html}</div>`;
}
function bigText(x, y, t, t0, t1, html, size = 120, col = '#fff', rot = 0) {
  if (t < t0 || t > t1) return '';
  return `<div style="position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%) rotate(${rot}deg) scale(${pop(t, t0, .4) * fade(t, t1 - .2, t1)});font:900 ${size}px/1.02 IB,Arial;color:${col};text-align:center;white-space:nowrap;text-shadow:${shadowTxt(OL, 7)},0 10px 22px #0007;z-index:2300">${html}</div>`;
}
// Zaehler: v0->v1 zwischen ta..tb
function counter(x, y, t, t0, t1, ta, tb, v0, v1, fmt, bg = '#35a862', col = '#fff', fs = 70) {
  if (t < t0 || t > t1) return '';
  const v = lerp(v0, v1, ez(cl(t, ta, tb)));
  return pillAt(x, y, t, t0, t1, fmt(v), bg, col, fs);
}
// ---------- Timeline ----------
const Lt = i => MG.L(i);
const NL = () => MG.TL.lines.length;
const SPEC = i => MG.TL.lines[i].spec || {};
function wt(i, re, end) { const l = Lt(i); if (!l.words) return l.start; for (const x of l.words) if (re.test(x[0])) return l.start + (end ? x[2] : x[1]); return l.start + (l.end - l.start) * .4 }
const nextStart = i => i + 1 < NL() ? Lt(i + 1).start : MG.TL.dur + 1;
function lineAt(t) { let k = 0; for (let i = 0; i < NL(); i++) if (t >= Lt(i).start - .001) k = i; return k }
const X = (p, dx, dy, dz) => [p[0] + dx, p[1] + dy, p[2] + dz];
// SHOT-Registry: SHOT[name] = { set, light, cam(i)->[{t0,a,b}] oder {a,b}, upd(t,i,u), figs(t,i,u)->html, ui(t,i,u)->html, sfx(i)->[] }
const SHOT = {};
function camOf(i) {
  const s = SHOT[SPEC(i).shot]; if (!s) return [{ t0: Lt(i).start, a: { pos: [0, 5, 20], at: [0, 1, 0], fov: 45 }, b: { pos: [0, 5, 20], at: [0, 1, 0], fov: 45 } }];
  let c = s.cam(i); if (!Array.isArray(c)) c = [Object.assign({ t0: Lt(i).start }, c)];
  return c;
}
let CAMS = null;
function camAt(t) {
  const i = lineAt(t), c = CAMS[i]; let k = 0; c.forEach((x, j) => { if (t >= x.t0 - .001) k = j });
  const s = c[k], t1 = k + 1 < c.length ? c[k + 1].t0 : nextStart(i), u = ei(cl(t, s.t0, t1));
  return { pos: G.v.lerp(s.a.pos, s.b.pos, u), at: G.v.lerp(s.a.at, s.b.at, u), fov: lerp(s.a.fov, s.b.fov, u) };
}
function cutTimes() { const r = []; for (let i = 1; i < NL(); i++) r.push(Lt(i).start); CAMS.forEach(c => c.slice(1).forEach(x => r.push(x.t0))); return r }
// Kapitel-Karte (#6 ... #1) + kleines Kapitel-Label oben links
const CHAP = [];   // {i, n, title, year, place}
function chapterUI(t) {
  let h = ''; let cur = null; CHAP.forEach(c => { if (t >= Lt(c.i).start) cur = c });
  if (!cur) return '';
  const t0 = Lt(cur.i).start, big = t < t0 + 2.6;
  if (big) {
    const k = pop(t, t0 + .05, .45), o = fade(t, t0 + 2.3, t0 + 2.6);
    h += `<div style="position:absolute;left:0;right:0;top:120px;text-align:center;opacity:${o};z-index:2400">
      <div style="display:inline-block;transform:scale(${k}) rotate(-3deg);font:900 230px/1 IB,Arial;color:#ffd166;text-shadow:${shadowTxt(OL, 10)},0 16px 30px #0008">#${cur.n}</div>
      <div style="margin-top:8px;transform:scale(${pop(t, t0 + .35, .4)});font:900 78px/1.05 IB,Arial;color:#fff;text-shadow:${shadowTxt(OL, 7)}">${cur.title}</div></div>`;
  } else {
    const k = ez(cl(t, t0 + 2.4, t0 + 2.8));
    h += `<div style="position:absolute;left:40px;top:34px;opacity:${k};z-index:2400;display:flex;gap:14px;align-items:center">
      <div style="font:900 64px/1 IB,Arial;color:#ffd166;text-shadow:${shadowTxt(OL, 5)}">#${cur.n}</div>
      ${PILL(cur.place + ' · ' + cur.year, '#232838cc', '#fff', 34)}</div>`;
  }
  return h;
}
