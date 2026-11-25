// ===================== Set OAK: Oak Island, Nova Scotia (Insel im Meer + Schnittbild der Grube) =====================
const OX = 500, OI = [OX, 0, 0];          // Insel-Mitte (Grube bei OI)
const OC = [OX, 0, -120];                   // Schnittbild (Ameisenfarm-Blick), Schacht-Mitte, Oberflaeche y=0
LOOK.teen = { sw: '#8a3a2a', swd: '#702e22', pa: '#4a3a2a', hat: HAT.cap };
LOOK.fdr = { sw: '#3a3f55', swd: '#2c3044', pa: '#2c3044', mid: MID.tie, hat: `<path d="M46,40 Q46,10 100,8 Q154,10 154,40Z" fill="#e8d8a0" stroke="${OL}" stroke-width="6"/><path d="M22,44 Q100,30 178,44 Q178,54 100,52 Q22,54 22,44Z" fill="#d8c890" stroke="${OL}" stroke-width="5"/><rect x="48" y="30" width="104" height="10" fill="#3a3f55"/>` };
LOOK.miner = { sw: '#6a5a4a', swd: '#57483a', pa: '#3e3a36', hat: `<path d="M38,50 Q38,4 100,2 Q162,4 162,50Z" fill="#f2b21c" stroke="${OL}" stroke-width="6"/><rect x="30" y="44" width="140" height="12" rx="5" fill="#e0a010" stroke="${OL}" stroke-width="4"/><circle cx="100" cy="24" r="9" fill="#fff6c0" stroke="${OL}" stroke-width="3"/>` };
LOOK.crew = { sw: '#2a2a33', swd: '#1e1e28', pa: '#3a3f55', hat: HAT.cap };
PROP.pick = `<g transform="rotate(-30)"><rect x="-5" y="-70" width="10" height="100" rx="4" fill="#a0703a" stroke="${OL}" stroke-width="4"/><path d="M-46,-62 Q0,-90 46,-62 L40,-56 Q0,-76 -40,-56Z" fill="#9aa0ac" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/></g>`;
PROP.cam = `<g transform="translate(-40,-40)"><rect x="0" y="10" width="70" height="44" rx="6" fill="#2a2a33" stroke="${OL}" stroke-width="5"/><circle cx="76" cy="32" r="16" fill="#4a4e5a" stroke="${OL}" stroke-width="5"/><circle cx="20" cy="4" r="12" fill="#2a2a33" stroke="${OL}" stroke-width="4"/><circle cx="48" cy="4" r="12" fill="#2a2a33" stroke="${OL}" stroke-width="4"/><circle cx="12" cy="22" r="4" fill="#e0303a"/></g>`;
(function oak() {
  const S = 'OAK';
  seaGrid(S, OX, 0, 220, 2.2, '#2a8fc0', { pos: [0, -.6, 0] });
  mk(S, G.cyl(26, 25, 1.4, 40, '#5f9a48'), { pos: [OX, -1.4, 0], outline: false, terrain: 0 });
  mk(S, G.cyl(29, 28, 1.4, 40, '#e8d4a0'), { pos: [OX, -1.6, 0], outline: false, cast: false });
  const T = []; for (let k = 0; k < 46; k++) { const a = k * 2.39, r = 8 + G.hash(k) * 15, x = OX + Math.cos(a) * r, z = Math.sin(a) * r * .8; if (z > -2 && x > OX - 6) continue; T.push(...tree(x, z, .8 + G.hash(k, 4) * .5, k % 3 ? '#2f5a34' : '#3a6a3a')) }
  mk(S, merge(T));
  // die alte Eiche + Grube (Mulde)
  mk(S, merge([at(G.cyl(.7, .5, 5, 10, '#5a3a26'), [OX - 2.6, 0, -1]), at(G.cyl(.25, .2, 3.4, 8, '#5a3a26'), [OX - 2.6, 4, -1], [0, 0, -1.1]), at(G.ico(3.2, 2, '#4a8a3c', .1, 2), [OX - 3, 7, -1]), at(G.ico(2.4, 2, '#3f7a34', .1, 3), [OX - .6, 6.4, -.6]), at(G.ico(2.2, 2, '#4f9440', .1, 6), [OX - 5, 6, -.4])]).smooth());
  mk(S, merge([at(G.cyl(1.8, 1.4, .12, 20, '#5a4430'), [OX, 0, 0])]), { outline: false, cast: false });
  // Flaschenzug am Ast
  mk(S, merge([at(G.cyl(.02, .02, 2.6, 4, '#c9b48a'), [OX - .2, 2.9, 0]), at(G.cyl(.2, .2, .2, 10, '#6a4a2e'), [OX - .2, 5.4, 0], [PI / 2, 0, 0])]), { outline: false });
  // ---------- Schnittbild ----------
  const D = 22, SH = 1.6, dirt = '#7a5634', dirt2 = '#6a4a2e', top = '#5f9a48';
  mk(S, merge([at(G.box(30, D, 30, dirt, { base: true, top }), [OC[0] - 15 - SH, -D, OC[2] - 15 + SH]), at(G.box(30, D, 30, dirt2, { base: true, top }), [OC[0] + 15 + SH, -D, OC[2] - 15 + SH]),
    at(G.box(2 * SH, D, 30, dirt2, { base: true, top }), [OC[0], -D, OC[2] - 15 - SH])]).vary(.04, 8), { outline: false });
  // Erdschichten-Streifen auf der Schnittflaeche
  const ST = []; for (let k = 1; k < 7; k++) [-1, 1].forEach(sg => ST.push(at(G.box(28, .25, .05, k % 2 ? '#8a6440' : '#5e4228', { base: true }), [OC[0] + sg * (14 + SH), -k * 3.1, OC[2] + SH + .03])));
  mk(S, merge(ST), { outline: false, cast: false });
  // Steine in der Erde
  mk(S, merge([...Array(20)].map((_, k) => at(G.ico(.3 + G.hash(k) * .4, 1, '#8a8478', .2, k), [OC[0] + (k % 2 ? 1 : -1) * (3 + G.hash(k, 2) * 12), -1 - G.hash(k, 3) * 19, OC[2] + SH + .05]))), { outline: false });
  // Hintergrund oben: Baeume, Eiche
  const T2 = []; for (let k = 0; k < 16; k++) T2.push(...tree(OC[0] - 22 + k * 3, OC[2] - 6 - (k % 3) * 3, .9, '#2f5a34'));
  T2.push(...leafy(OC[0] - 4, OC[2] - 3, 1.3, '#4a8a3c')); mk(S, merge(T2));
})();
// Baumstamm-Lagen im Schacht (alle ~10 Fuss)
const OLOGS = [1, 2, 3, 4].map(k => mk('OAK', merge([...Array(5)].map((_, j) => at(G.cyl(.28, .28, 3.2, 10, '#8a5a32'), [-1.6, 0, -1.2 + j * .6], [0, 0, -PI / 2]))), { pos: [OC[0], -k * 3.3, OC[2]] }));
const OSTONE = mk('OAK', G.box(1.4, .9, .3, '#8a8478'), { pos: [OC[0], -15.6, OC[2] + .4] });
function stoneTex() { return tex(512, 330, (x, wd, ht) => { x.fillStyle = '#8a8478'; x.fillRect(0, 0, wd, ht); x.strokeStyle = '#3a3830'; x.lineWidth = 9; x.lineCap = 'round';
  const sym = ['M0,0 L30,40', 'M0,40 L30,0', 'M0,20 L30,20 M15,0 L15,40', 'M0,0 L30,0 L15,40Z', 'M0,40 Q15,-10 30,40', 'M0,0 L0,40 L30,40', 'M15,0 A15,15 0 1 0 15.1,0', 'M0,20 L30,0 L30,40Z'];
  for (let r = 0; r < 3; r++) for (let c = 0; c < 8; c++) { x.save(); x.translate(40 + c * 56, 50 + r * 100); x.stroke(new Path2D(sym[(c * 3 + r) % 8])); x.restore() } }) }
const OSTONE_T = texPlane('OAK', 1.3, .84, stoneTex, { pos: [OC[0], -15.15, OC[2] + .56] });
const OWATER = mk('OAK', G.box(3.2, 1, 3.2, '#2a8fd6', { base: true }), { pos: [OC[0], -22, OC[2]], alpha: .62, emis: .2, outline: false, cast: false });
const OGAS = mk('OAK', G.ico(1.4, 2, '#9ad04a', .3, 7), { pos: [OC[0], -18, OC[2]], alpha: .35, emis: .5, outline: false, cast: false, recv: false });
const OLADDER = mk('OAK', merge([at(G.box(.06, 20, .06, '#c9b48a'), [-.35, -10, 0]), at(G.box(.06, 20, .06, '#c9b48a'), [.35, -10, 0]), ...[...Array(30)].map((_, k) => at(G.box(.7, .05, .05, '#c9b48a'), [0, -.4 - k * .65, 0]))]), { pos: [OC[0] + 1.2, 0, OC[2] - 1.2], outline: false });
const OTVCAM = mk('OAK', merge([at(G.cyl(.05, .05, 1.5, 6, '#2a2a33'), [-.3, 0, 0], [0, 0, .2]), at(G.cyl(.05, .05, 1.5, 6, '#2a2a33'), [.3, 0, 0], [0, 0, -.2]), at(G.box(.6, .45, .9, '#2a2a33'), [0, 1.6, 0]), at(G.cyl(.15, .15, .4, 10, '#4a4e5a'), [0, 1.6, .6], [PI / 2, 0, 0])]), { pos: [OI[0] + 3.6, 0, OI[2] + 2.4], rot: [0, -.9, 0] });
CHAP.push({ line: 'n5', n: 5, title: 'THE OAK ISLAND MONEY PIT', year: '1795', place: '🇨🇦 Nova Scotia' });
let OA_I0 = 0;
function oaUpd(t, i) {
  const k = i - OA_I0;
  OLOGS.forEach((m, j) => m.vis = k != 2 || t > Lt(i).start + .8 + j * ((Lt(i).end - Lt(i).start - 1.2) / 4));
  OSTONE.vis = OSTONE_T.vis = k == 3 || k == 4;
  const fl = k == 4 ? ez(cl((t - wt(i, /flooded/) + .3) / 2.4, 0, 1)) : (k == 6 ? .25 : 0);
  OWATER.vis = fl > 0; OWATER.scl = [1, Math.max(.01, fl * 16), 1]; OWATER.pos = [OC[0], -22, OC[2]];
  OGAS.vis = k == 6 && t > wt(i, /gas/) - .4; OGAS.scl = [1 + .1 * Math.sin(t * 3), 1.6, 1]; OGAS.alpha = .3 + .08 * Math.sin(t * 4);
  OLADDER.vis = k >= 2 && k <= 6; OTVCAM.vis = k == 8;
}
const cutCam = (y, z = 15, fov = 46) => cm([OC[0] + 1.5, y + 1, OC[2] + z], [OC[0], y, OC[2]], fov);
SHOT.o_island = { set: 'OAK', light: 'day',
  cam: i => { OA_I0 = i; return mv(cm([OX + 46, 22, 50], [OX, 0, 0], 46), cm([OX + 30, 14, 34], [OX, 1, 0], 46)) },
  upd: oaUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📍 NOVA SCOTIA, CANADA', '#232838', '#fff', 44),
  sfx: i => [{ k: 'wave', t: Lt(i).start + .2 }, { k: 'gull', t: Lt(i).start + 1.4 }] };
SHOT.o_dip = { set: 'OAK', light: 'day',
  cam: i => mv(cm([OX + 4, 2.4, 7.5], [OX - .6, 1.6, 0], 48), cm([OX + 3, 2.1, 6.2], [OX - .6, 1.4, 0], 46)),
  upd: oaUpd,
  figs: (t, i) => fig([OX + 1.6, 0, 1.4], 'teen', { mouth: 'o', talk: 0, blink: bl(t, 0), look: [-5, 4], hR: [200, 110], tilt: -.08 }),
  ui: (t, i) => pillAt(960, 170, t, wt(i, /1795/) - .1, nextStart(i), '📜 THE STORY GOES… 1795', '#8a6a3a', '#fff', 52) + labelAt([OX, .4, 0], PILL('🕳️ A STRANGE DIP', '#232838', '#fff', 40), t, wt(i, /dip/) - .1, nextStart(i)),
  sfx: i => [{ k: 'pop', t: wt(i, /dip/) }, { k: 'gull', t: Lt(i).start + .5 }] };
SHOT.o_logs = { set: 'OAK', light: 'day',
  cam: i => mv(cutCam(-2, 18, 50), cutCam(-8, 16, 50)),
  upd: oaUpd,
  figs: (t, i) => { const u = cl((t - Lt(i).start) / (nextStart(i) - Lt(i).start), 0, 1), y = -u * 13.5; return fig([OC[0] - .4, y, OC[2] + .6], 'teen', { mouth: 'grin', blink: bl(t, 0), look: [2, 5], prop: PROP.shovel, hR: [180, 150 + 25 * Math.sin(t * 6)] }, 1.75) },
  ui: (t, i) => { let h = ''; const dt = (Lt(i).end - Lt(i).start - 1.2) / 4; OLOGS.forEach((m, j) => { const a = Lt(i).start + .8 + j * dt; h += labelAt(X(m.pos, 3.6, .3, 0), PILL('🪵 ' + (j + 1) * 10 + ' FT', '#8a5a32', '#fff', 38), t, a, nextStart(i)) }); return h },
  sfx: i => { const dt = (Lt(i).end - Lt(i).start - 1.2) / 4; return [0, 1, 2, 3].map(j => ({ k: 'thud', t: Lt(i).start + .8 + j * dt, g: .5 })) } };
SHOT.o_stone = { set: 'OAK', light: 'day',
  cam: i => mv(cm([OC[0] + .4, -14.6, OC[2] + 4.2], [OC[0], -15.2, OC[2] + .4], 40), cm([OC[0] + .2, -14.9, OC[2] + 3.2], [OC[0], -15.2, OC[2] + .4], 38)),
  upd: oaUpd,
  ui: (t, i) => bigText(960, 190, t, wt(i, /ten/) - .1, nextStart(i), '"10 FEET BELOW: <span style="color:#ffd166">£2,000,000</span>"', 72) + pillAt(960, 320, t, wt(i, /claimed/) - .1, nextStart(i), '⚠️ CLAIMED – NEVER PROVEN', '#232838', '#fff', 42),
  sfx: i => [{ k: 'shimmer', t: wt(i, /stone/) }, { k: 'cash', t: wt(i, /million/) }] };
SHOT.o_flood = { set: 'OAK', light: 'day',
  cam: i => mv(cutCam(-12, 22, 52), cutCam(-10, 20, 52)),
  upd: oaUpd,
  figs: (t, i) => { const a = wt(i, /flooded/); const y = t < a ? -14 : lerp(-14, -1, ez(cl((t - a) / 1.6, 0, 1))); return fig([OC[0] + .9, y, OC[2] - .6], 'teen', Object.assign(walk(t, 12), { mouth: 'o', blink: bl(t, 0), look: [0, -6], sweat: true, hR: [190, 40], hL: [10, 40] })) },
  ui: (t, i) => stampAt(1400, 300, t, wt(i, /water/) - .05, 'FLOODED!', '#2a8fd6', 100, 6),
  sfx: i => [{ k: 'splash', t: wt(i, /flooded/) }, { k: 'wave', t: wt(i, /water/) }] };
SHOT.o_fdr = { set: 'OAK', light: 'day',
  cam: i => mv(cm([OX + 6, 2.6, 9], [OX, 1.4, 0], 50), cm([OX + 4.8, 2.4, 7.6], [OX, 1.4, 0], 48)),
  upd: oaUpd,
  figs: (t, i) => { const a = wt(i, /roosevelt/i) - .3; let h = fig([OX - 1.6, 0, 1.4], 'miner', { mouth: 'grin', blink: bl(t, 1), look: [3, 2], prop: PROP.pick, hR: [180, 140 + 20 * Math.sin(t * 5)] });
    if (t > a) h += fig([OX + 1.8, 0, 2], 'fdr', { mouth: 'smile', blink: bl(t, 0), look: [-4, 0], prop: PROP.cash, hR: [200, 140] }); return h },
  ui: (t, i) => counter(960, 160, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, wt(i, /years/), 1795, 2026, v => '⏳ ' + Math.round(v), '#232838', '#fff', 64) + labelAt([OX + 1.8, 2.2, 2], PILL('FRANKLIN D. ROOSEVELT · 1909', '#2a8fd6', '#fff', 36), t, wt(i, /roosevelt/i) - .1, nextStart(i)),
  sfx: i => [{ k: 'tick', t: Lt(i).start + .3 }, { k: 'pop', t: wt(i, /roosevelt/i) }, { k: 'cash', t: wt(i, /invested/) }] };
SHOT.o_deaths = { set: 'OAK', light: 'indoorDark',
  cam: i => mv(cutCam(-14, 18, 50), cutCam(-16, 15, 48)),
  upd: oaUpd,
  ui: (t, i) => { let h = counter(960, 170, t, wt(i, /six/i) - .1, nextStart(i), wt(i, /six/i), wt(i, /died/), 0, 6, v => '⚠️ ' + Math.round(v) + ' DEATHS', '#e0303a', '#fff', 70);
    h += pillAt(960, 300, t, wt(i, /1965/) - .1, nextStart(i), '☠️ 1965: TOXIC GAS IN THE SHAFT', '#232838', '#fff', 46); return h },
  sfx: i => [{ k: 'impact', t: wt(i, /died/), g: .5 }, { k: 'heartbeat', t: wt(i, /gas/), n: 2 }] };
SHOT.o_science = { set: 'OAK', light: 'day',
  cam: i => cut2(i, /stone/, cutCam(-10, 24, 52), cutCam(-9, 22, 52), cm([OC[0] + .2, -14.9, OC[2] + 3.6], [OC[0], -15.2, OC[2] + .4], 40), cm([OC[0] + .2, -14.9, OC[2] + 3.0], [OC[0], -15.2, OC[2] + .4], 38)),
  upd: (t, i) => { oaUpd(t, i); OWATER.vis = t < wt(i, /stone/) - .15; OWATER.scl = [1, 6 + 2 * Math.sin(t * 2), 1]; OSTONE.vis = false; OSTONE_T.vis = false },
  ui: (t, i) => pillAt(960, 170, t, wt(i, /natural/) - .1, wt(i, /stone/) - .2, '🌊 NATURAL FLOODING (STUDY, 1995)', '#2a8fd6', '#fff', 50) + stampAt(960, 470, t, wt(i, /lost/) - .05, 'LOST', '#e0303a', 130, -6) + bigText(960, 300, t, wt(i, /stone/) - .1, nextStart(i), '?', 220, '#ffd166'),
  sfx: i => [{ k: 'ding', t: wt(i, /natural/) }, { k: 'impact', t: wt(i, /lost/), g: .5 }] };
SHOT.o_tv = { set: 'OAK', light: 'day',
  cam: i => mv(cm([OX + 7, 3, 8], [OX + 1, 1.4, 0], 50), cm([OX + 5.6, 2.6, 6.6], [OX + 1, 1.4, 0], 48)),
  upd: oaUpd,
  figs: (t, i) => fig([OX - 1.4, 0, 1.2], 'miner', { mouth: 'sad', blink: bl(t, 0), look: [3, 4], prop: PROP.shovel, hR: [180, 190] }) + fig([OX + 2.4, 0, 3.4], 'crew', { mouth: 'grin', blink: bl(t, 1), look: [-5, 0], prop: PROP.cam, hR: [150, 60], hL: [50, 70] }),
  ui: (t, i) => stampAt(960, 230, t, wt(i, /no/) - .05, 'NO TREASURE', '#e0303a', 100, -5) + pillAt(1440, 420, t, wt(i, /tv/i) - .1, nextStart(i), '📺 ON TV SINCE 2014', '#e0303a', '#fff', 50),
  sfx: i => [{ k: 'impact', t: wt(i, /no/), g: .5 }, { k: 'ding', t: wt(i, /tv/i) }] };
