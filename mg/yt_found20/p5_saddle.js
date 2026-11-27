// ===================== #4 Set HILL: Grundstueck in Nordkalifornien (Saddle Ridge) / Holzstapel mit Kuehlbox =====================
const SX = 1800, SH = [SX, 0, 0], SW = [SX, 0, -90];
LOOK.john = { sw: '#4a7ab0', swd: '#3a6aa0', pa: '#5a4a3a', hat: HAT.cap };
LOOK.mary = { sw: '#e07a5a', swd: '#c8644a', pa: '#3a3f55', hat: `<path d="M44,60 Q30,0 100,-2 Q170,0 156,60 Q150,30 100,26 Q50,30 44,60Z" fill="#c9a06a" stroke="${OL}" stroke-width="5"/>` };
function dog(p, t, o = {}) {
  const q = w.project(p); if (!q.vis) return ''; const s = q.s * .62 / 350 * 240 / 240 * 1.2, wag = Math.sin(t * 14) * 18, lg = o.walk ? Math.sin(t * 12) * 14 : 0, f = o.flip ? -1 : 1;
  return `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%) scale(${s * f},${s});transform-origin:50% 100%;z-index:${Math.round(1000 - q.z)}"><svg width="240" height="200" viewBox="0 0 240 200" style="display:block">
   <path d="M44,96 Q20,${70 - wag * .6} 14,${60 - wag}" stroke="${OL}" stroke-width="18" stroke-linecap="round" fill="none"/><path d="M44,96 Q20,${70 - wag * .6} 14,${60 - wag}" stroke="#c98a4a" stroke-width="10" stroke-linecap="round" fill="none"/>
   ${[[64, lg], [92, -lg], [140, -lg], [168, lg]].map(([x, a]) => `<path d="M${x},120 L${x + a * .4},182" stroke="${OL}" stroke-width="20" stroke-linecap="round"/><path d="M${x},120 L${x + a * .4},182" stroke="#c98a4a" stroke-width="12" stroke-linecap="round"/>`).join('')}
   <ellipse cx="116" cy="112" rx="78" ry="40" fill="#c98a4a" stroke="${OL}" stroke-width="7"/>
   <circle cx="186" cy="70" r="40" fill="#c98a4a" stroke="${OL}" stroke-width="7"/><path d="M166,40 Q150,30 154,74 Q166,72 172,50Z" fill="#8a5a2a" stroke="${OL}" stroke-width="5"/>
   <ellipse cx="218" cy="80" rx="18" ry="13" fill="#e8c8a0" stroke="${OL}" stroke-width="5"/><circle cx="230" cy="76" r="6" fill="${OL}"/><circle cx="194" cy="62" r="6" fill="${OL}"/>
   ${o.bark ? `<path d="M222,94 Q232,104 240,96" stroke="${OL}" stroke-width="5" fill="#e5767a"/>` : ''}</svg></div>`;
}
(function hill() {
  const S = 'HILL';
  mk(S, G.box(200, .4, 140, '#c9b46a', { base: true }), { pos: [SX, -.4, 0], outline: false, cast: false });
  // sanfte Huegel (goldenes Gras) + Eichen
  mk(S, merge([[-40, -50, 30, 8], [10, -60, 36, 11], [55, -48, 28, 7], [-80, -40, 26, 6], [90, -70, 40, 12]].map(([x, z, r, h]) => at(G.ico(r, 2, '#c4a85a', 0, 1, h / r), [SX + x, -1, z]))).smooth(), { cast: false, outline: false });
  const T = []; [[-14, -10], [-8, -16], [6, -12], [16, -9], [24, -18], [-22, -6], [-16, 10]].forEach(([x, z], k) => T.push(...leafy(SX + x, z, 1 + G.hash(k) * .4, k % 2 ? '#4a7a3a' : '#5a8a3a')));
  mk(S, merge(T));
  // Weg + Felsen
  mk(S, G.box(60, .04, 1.6, '#b89a6a', { base: true }), { pos: [SX, 0, 1.2], outline: false, cast: false });
  mk(S, merge([...Array(10)].map((_, k) => at(G.ico(.3 + G.hash(k) * .5, 1, '#9a9488', .25, k), [SX - 12 + k * 2.6 + G.hash(k, 2) * 1.5, 0, -2.2 - G.hash(k, 1) * 2]))).smooth());
  // Haus in der Ferne
  mk(S, merge([at(G.box(6, 3, 5, '#e8d8b8', { base: true }), [SX + 18, 0, -26]), at(G.cyl(4.6, 0, 2.2, 4, '#8a4a3a', { rot: .785 }), [SX + 18, 3, -26])]));
  // Holzstapel + Schuppen
  mk(S, G.box(60, .4, 40, '#8a9a5a', { base: true }), { pos: [SW[0], -.38, SW[2]], outline: false, cast: false });
  mk(S, merge([at(G.box(6, 3.2, 4, '#9a6a4a', { base: true }), [SW[0] - 4, 0, SW[2] - 4]), at(G.box(6.6, .3, 4.6, '#6a4a3a', { base: true }), [SW[0] - 4, 3.2, SW[2] - 4]),
    ...[...Array(24)].map((_, k) => at(G.cyl(.16, .16, 2.2, 8, k % 3 ? '#a8784a' : '#8a6038'), [SW[0] + .2 + (k % 8) * .34 + (Math.floor(k / 8) % 2) * .17, .16 + Math.floor(k / 8) * .3, SW[2] - 1.6], [PI / 2, 0, 0]))]));
})();
// Dosen: 8 Stueck; Dose 0 steckt schraeg im Boden am Weg
const SC0 = [SX + 1.2, 0, -.3];
const SCANS = [...Array(8)].map((_, k) => mk('HILL', canGeo(), { pos: [SX - 1.4 + k * .5, 0, -1.2] }));
const SLID = mk('HILL', G.cyl(.17, .17, .04, 14, '#6a3a1e'), { pos: [0, 0, 0] });
const SGOLD = mk('HILL', coinPile(70, .45, 3), { pos: [SX + 1.8, .02, -.1], spec: 1, emis: .2, outline: false });
const SCOOL = mk('HILL', merge([at(G.box(1.1, .6, .6, '#2a8fd6', { base: true }), [0, 0, 0]), at(G.box(1.14, .08, .64, '#f4efe2', { base: true }), [0, .6, 0])]), { pos: [SW[0] + 3.6, 0, SW[2] - .9] });
const SHOLES = mk('HILL', merge([...Array(8)].map((_, k) => at(G.cyl(.26, .26, .03, 12, '#5a4028'), [k * .5, 0, 0]))), { pos: [SX - 1.4, .01, -1.2], outline: false, cast: false });
CHAP.push({ line: 'n4', n: 4, title: 'THE RUSTY CAN', year: '2013', place: '🇺🇸 Northern California' });
function sUpd(t, i, mode) {
  SCANS.forEach(m => { m.vis = false; m.rot = [0, 0, 0] }); SLID.vis = false; SGOLD.vis = false; SCOOL.vis = true; SHOLES.vis = false;
  if (mode == 'one') { const c = SCANS[0]; c.vis = true; c.pos = X(SC0, 0, -.12, 0); c.rot = [.5, 0, .3] }
  if (mode == 'open') { const c = SCANS[0], u = ez(cl((t - Lt(i).start) / .8, 0, 1)); c.vis = true; c.pos = X(SC0, 0, lerp(-.12, 0, u), 0); c.rot = [lerp(.5, 0, u), 0, lerp(.3, 1.45, ez(cl((t - wt(i, /inside/i) + .4) / .4, 0, 1)))];
    SGOLD.vis = t > wt(i, /inside/i) - .1; SGOLD.scl = [1, ez(cl((t - wt(i, /inside/i)) / .5, 0, 1)) + .01, 1] }
  if (mode == 'eight') { SCANS.forEach((m, k) => { const a = wt(i, /eight/) + k * .12; m.vis = t > a || k == 0; m.pos = [SX - 1.4 + k * .5, 0, -1.2]; m.scl = [1, k ? bo(cl(t, a, a + .3)) : 1, 1] }); SGOLD.vis = true }
  if (mode == 'pile') { SCANS.forEach((m, k) => { m.vis = true; m.pos = [SX - 1.4 + k * .5, 0, -1.2] }); SGOLD.vis = true }
  if (mode == 'holes') { SHOLES.vis = true }
}
SHOT.s_hill = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX + 5, 5, 15], [SX - 4, 1, 0], 50), cm([SX + 3, 3.8, 11], [SX - 4, 1, 0], 48)),
  upd: (t, i) => sUpd(t, i, 'one'),
  figs: (t, i) => { const x = SX - 8 + (t - Lt(i).start) * .8; return fig([x, 0, 1.2], 'john', Object.assign(walk(t, 6), { mouth: 'smile', blink: bl(t, 0), look: [3, 2] })) + fig([x - 1.1, 0, 1.5], 'mary', Object.assign(walk(t + .3, 6), { mouth: 'smile', blink: bl(t, 1), look: [3, 2] })) + dog([x + 1.4, 0, 1.4], t, { walk: 1 }) },
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '🌄 SIERRA NEVADA · CALIFORNIA', '#232838', '#fff', 44),
  sfx: i => [{ k: 'bell', t: Lt(i).start + .4 }] };
SHOT.s_walk = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX - 4, 2.2, 6], [SX - 3, 1.2, 1], 46), cm([SX - 1, 2.2, 6], [SX - .4, 1.2, 1], 46)),
  upd: (t, i) => sUpd(t, i, 'one'),
  figs: (t, i) => { const u = cl((t - Lt(i).start) / (nextStart(i) - Lt(i).start), 0, 1), x = SX - 4.6 + u * 3.6; return fig([x, 0, 1.2], 'john', Object.assign(walk(t, 6), { mouth: 'smile', talk: 0, blink: bl(t, 0), look: [3, 2] })) + fig([x - 1.1, 0, 1.5], 'mary', Object.assign(walk(t + .3, 6), { mouth: 'smile', blink: bl(t, 1), look: [3, 2] })) + dog([x + 1.3, 0, 1.6], t, { walk: 1 }) },
  ui: (t, i) => pillAt(960, 170, t, wt(i, /land/) - .1, nextStart(i), '🐕 A WALK ON THEIR OWN LAND', '#232838', '#fff', 54),
  sfx: i => [{ k: 'pop', t: wt(i, /dog/) }] };
SHOT.s_can = { set: 'HILL', light: 'dusk',
  cam: i => cut2(i, /rusty/, cm([SX - 1, 2, 4.4], [SX + .6, 1, .2], 44), cm([SX - .4, 1.9, 4], [SX + .8, 1, .2], 42), cm([SX + 2.6, 1.1, 1.8], [SX + 1.2, .1, -.3], 38), cm([SX + 2.3, 1, 1.4], [SX + 1.2, .1, -.3], 36)),
  upd: (t, i) => sUpd(t, i, 'one'),
  figs: (t, i) => t > wt(i, /rusty/) - .15 ? '' : fig([SX - .2, 0, 1.2], 'john', { mouth: 'o', blink: bl(t, 0), look: [4, 4] }) + fig([SX - 1.2, 0, 1.5], 'mary', { mouth: 'o', blink: bl(t, 1), look: [4, 4] }) + dog([SX + .9, 0, 1], t, { bark: Math.sin(t * 8) > 0 }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /rusty/) - .1, nextStart(i), '🥫 AN OLD, RUSTY CAN', '#a0582a', '#fff', 56),
  sfx: i => [{ k: 'ding', t: wt(i, /notice/) }, { k: 'pop', t: wt(i, /rusty/) }] };
SHOT.s_open = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX + 2.4, 1.6, 2.2], [SX + 1.4, .2, -.2], 40), cm([SX + 2.2, 1.3, 1.6], [SX + 1.5, .2, -.2], 36)),
  upd: (t, i) => sUpd(t, i, 'open'),
  figs: (t, i) => fig([SX + .2, 0, .6], 'john', { mouth: t > wt(i, /gold/) ? 'o' : 'hmm', blink: bl(t, 0), look: [4, 4], hR: [170, 200] }),
  ui: (t, i) => stampAt(1400, 300, t, wt(i, /gold/) - .05, '🪙 GOLD!', '#e8a800', 120, -8),
  sfx: i => [{ k: 'thud', t: Lt(i).start + .3 }, { k: 'shimmer', t: wt(i, /inside/i) }, { k: 'impact', t: wt(i, /gold/) }] };
SHOT.s_cans = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX + .4, 2.6, 4.4], [SX + .2, .3, -.9], 44), cm([SX + .2, 2.4, 3.8], [SX + .2, .3, -.9], 42)),
  upd: (t, i) => sUpd(t, i, 'eight'),
  figs: (t, i) => fig([SX + 3.3, 0, -.4], 'mary', { mouth: 'grin', blink: bl(t, 1), look: [-4, 3] }) + dog([SX + 2.6, 0, .6], t, { flip: 1 }),
  ui: (t, i) => pillAt(960, 160, t, wt(i, /eight/) - .1, nextStart(i), '🥫 × 8 CANS', '#a0582a', '#fff', 60) +
    counter(960, 290, t, wt(i, /fourteen/) - .1, nextStart(i), wt(i, /fourteen/), wt(i, /coins/), 0, 1427, v => Math.round(v).toLocaleString('en-US') + ' GOLD COINS', '#e8a800', OL, 70),
  sfx: i => [...[0, 1, 2, 3, 4, 5, 6, 7].map(k => ({ k: 'pop', t: wt(i, /eight/) + k * .12 })), { k: 'cash', t: wt(i, /coins/) }] };
SHOT.s_dates = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX + 3, 1.6, 1.8], [SX + 1.6, .1, -.3], 40), cm([SX + 2.8, 1.4, 1.5], [SX + 1.6, .1, -.3], 38)),
  upd: (t, i) => sUpd(t, i, 'pile'),
  ui: (t, i) => pillAt(960, 140, t, wt(i, /1847/) - .1, nextStart(i), '📅 1847 – 1894', '#232838', '#fff', 60) + pillAt(960, 270, t, wt(i, /san/i) - .1, nextStart(i), '🏛️ SAN FRANCISCO', '#2a8fd6', '#fff', 50) +
    counter(960, 760, t, wt(i, /face/) - .1, nextStart(i), wt(i, /face/), wt(i, /dollars/), 0, 27980, v => 'FACE VALUE: $' + Math.round(v).toLocaleString('en-US'), '#35a862', '#fff', 64),
  sfx: i => [{ k: 'tick', t: wt(i, /1847/) }, { k: 'pop', t: wt(i, /san/i) }, { k: 'cash', t: wt(i, /dollars/) }] };
SHOT.s_value = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX + 1, 2.2, 4.6], [SX + .6, 1, -.4], 44), cm([SX + .8, 2, 3.6], [SX + .6, 1.1, -.4], 40)),
  upd: (t, i) => sUpd(t, i, 'pile'),
  figs: (t, i) => fig([SX - .6, 0, .2], 'john', { mouth: 'o', blink: bl(t, 0), look: [2, 1], hR: [175, 40], hL: [25, 40] }) + fig([SX + 2.9, 0, .2], 'mary', { mouth: 'o', blink: bl(t, 1), look: [-2, 1], hR: [175, 40], hL: [25, 40] }) + dog([SX + 1.3, 0, 1.2], t, { bark: Math.sin(t * 8) > 0 }),
  ui: (t, i) => counter(960, 200, t, wt(i, /collectors/) - .1, nextStart(i), wt(i, /collectors/), wt(i, /million/), 27980, 1e7, v => '~$' + Math.round(v).toLocaleString('en-US'), '#35a862', '#fff', 92),
  sfx: i => [{ k: 'tick', t: wt(i, /collectors/) }, { k: 'impact', t: wt(i, /million/) }, { k: 'cash', t: wt(i, /million/) + .2 }] };
SHOT.s_mint = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SX + 3.2, 1.7, 2], [SX + 1.6, .1, -.3], 40), cm([SX + 3, 1.6, 1.8], [SX + 1.6, .1, -.3], 38)),
  upd: (t, i) => sUpd(t, i, 'pile'),
  ui: (t, i) => { const a = wt(i, /stolen/) - .2; if (t < a) return '';
    return `<div style="position:absolute;left:960px;top:120px;transform:translate(-50%,0) scale(${pop(t, a)}) rotate(-2deg);width:860px;background:#f4efe2;border:8px solid ${OL};border-radius:12px;padding:20px 30px;box-shadow:0 14px 0 #0005;z-index:2200;text-align:center">
      <div style="font:900 30px IB;color:#6a5a4a">THEORY · 1901</div><div style="font:900 62px/1.05 IB;color:${OL}">STOLEN FROM THE<br>SAN FRANCISCO MINT?</div></div>` + stampAt(1450, 560, t, wt(i, /link/) - .05, 'NO LINK', '#e0303a', 110, -8) },
  sfx: i => [{ k: 'pop', t: wt(i, /stolen/) }, { k: 'impact', t: wt(i, /link/) }] };
SHOT.s_cooler = { set: 'HILL', light: 'dusk',
  cam: i => mv(cm([SW[0] + 4, 2.4, SW[2] + 4.4], [SW[0] + 1, .9, SW[2] - 1], 46), cm([SW[0] + 3, 2, SW[2] + 3.2], [SW[0] + 1.2, .8, SW[2] - .8], 44)),
  upd: (t, i) => sUpd(t, i, 'none'),
  figs: (t, i) => fig([SW[0] + .6, 0, SW[2] + .6], 'john', { mouth: 'hmm', blink: bl(t, 0), look: [4, 2], hR: [180, 80] }) + dog([SW[0] + 1.8, 0, SW[2] + 1.2], t, {}),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /cooler/) - .1, nextStart(i), '🧊 AN OLD COOLER', '#2a8fd6', '#fff', 56) + pillAt(960, 290, t, wt(i, /firewood/) - .1, nextStart(i), '🪵 UNDER THE FIREWOOD', '#a0582a', '#fff', 50),
  sfx: i => [{ k: 'pop', t: wt(i, /cooler/) }, { k: 'thud', t: wt(i, /firewood/) }] };
SHOT.s_mystery = { set: 'HILL', light: 'night',
  cam: i => mv(cm([SX + .2, 3.4, 5.6], [SX - .2, .2, -1.2], 46), cm([SX + .2, 2.6, 4], [SX - .2, .2, -1.2], 44)),
  upd: (t, i) => sUpd(t, i, 'holes'),
  ui: (t, i) => bigText(960, 230, t, wt(i, /buried/) - .1, nextStart(i), 'WHO BURIED THEM?', 100, '#ffd166', -3) + bigText(960, 420, t, wt(i, /nobody/) - .1, nextStart(i), '❓', 160),
  sfx: i => [{ k: 'impact', t: wt(i, /buried/), g: .5 }, { k: 'shimmer', t: wt(i, /nobody/) }] };
