// ===================== Kapitel #1: Gardner Museum 1990 (Set GAR) + Outro =====================
const GB = [0, 0, -130];   // Keller
mk('GAR', merge([at(G.box(10, .3, 8, '#5a5a62', { base: true }), [GB[0], -.3, GB[2]]), at(G.box(10, 4, .3, '#7a7068', { base: true }), [GB[0], 0, GB[2] - 4]),
  at(G.box(.3, 4, 8, '#6a6058', { base: true }), [GB[0] - 5, 0, GB[2]]), at(G.box(10, .3, 8, '#3a3a40', { base: true }), [GB[0], 4, GB[2]]),
  at(G.cyl(.15, .15, 10, 10, '#8a6a4a'), [GB[0], 3.4, GB[2] - 3.6], [0, 0, PI / 2]), at(G.cyl(.1, .1, 4, 10, '#8a8e9a'), [GB[0] - 1.6, 0, GB[2] - 2.2]), at(G.cyl(.1, .1, 4, 10, '#8a8e9a'), [GB[0] + 1.6, 0, GB[2] - 2.2])]), { outline: false });
mk('GAR', G.ico(.2, 2, '#fff2c0'), { pos: [GB[0], 3.7, GB[2]], emis: 1, outline: false, cast: false });
// Tuer (dreht sich auf)
const GDOOR = mk('GAR', new G.Geo().add(G.box(2.5, 3.3, .12, '#5a3824', { base: true }), G.m4.compose([1.25, 0, 0])), { pos: [-1.25, 0, .36] });
CHAP.push({ line: 'n1', n: 1, title: 'THE GARDNER MUSEUM HEIST', year: '1990', place: '🇺🇸 Boston' });
let GA_I0 = 0;
function gaUpd(t, i) { const k = i - GA_I0, open = k == 2 ? ez(cl(t, wt(i, /lets/) - .4, wt(i, /lets/) + .4)) : (k > 2 ? 1 : 0);
  GDOOR.rot = [0, open * 1.6, 0];
  const gone1 = k > 5 || (k == 5 && t > wt(i, /rembrandt/i) - .1), gone2 = k > 5 || (k == 5 && t > wt(i, /vermeer/i) - .1), gone3 = k > 5;
  FR_STORM.pl.vis = !gone1; FR_MUSIC.pl.vis = !gone2; FR_PAIR.pl.vis = !gone3 }
const FAKECOPS = (t, extra = {}) => fig([-.8, 0, 1.6], 'fakecop', Object.assign({ mouth: 'hmm', blink: bl(t, 0), look: [2, -2] }, extra)) + fig([.9, 0, 2.0], 'fakecop', { mouth: 'hmm', blink: bl(t, 1.3), look: [-3, -2], armL: [.15, .1], armR: [.15, .1] });
SHOT.g_street = { set: 'GAR', light: 'night',
  cam: i => { GA_I0 = i; return { a: { pos: [14, 8, 26], at: [0, 4, 0], fov: 50 }, b: { pos: [8, 4.4, 16], at: [0, 3, 0], fov: 48 } } },
  upd: gaUpd,
  ui: (t, i) => pillAt(960, 930 - 110, t, Lt(i).start + 2.7, nextStart(i), '📅 18 MARCH 1990 · NIGHT', '#232838', '#fff', 44) };
SHOT.g_bell = { set: 'GAR', light: 'night',
  cam: i => ({ a: { pos: [4.4, 2.4, 8], at: [0, 1.6, 0], fov: 44 }, b: { pos: [3.2, 2.0, 6.4], at: [0, 1.6, 0], fov: 42 } }),
  upd: gaUpd,
  figs: (t, i) => { const r = wt(i, /bell/) - .1; return FAKECOPS(t, { hR: t > r && t < r + .7 ? [210, 96] : null, mouth: t > wt(i, /say/) ? 'smile' : 'hmm', talk: t > wt(i, /say/) ? tk(t, i) : 0 }) },
  ui: (t, i) => labelAt([0, 3.9, .5], `<div style="font:900 80px IB;color:#ffd166;text-shadow:${shadowTxt(OL, 6)};transform:rotate(-6deg)">DING DONG!</div>`, t, wt(i, /bell/), wt(i, /bell/) + 1.4) + pillAt(960, 200, t, wt(i, /police/) - .1, nextStart(i), '👮 "POLICE" – BUT FAKE', '#e0303a', '#fff', 54) + pillAt(960, 310, t, wt(i, /disturbance/) - .1, nextStart(i), '💬 "WE GOT A DISTURBANCE CALL"', '#fff', OL, 44),
  sfx: i => [{ k: 'bell', t: wt(i, /bell/) }, { k: 'pop', t: wt(i, /police/) }, { k: 'pop', t: wt(i, /disturbance/) }] };
SHOT.g_letin = { set: 'GAR', light: 'night',
  cam: i => ({ a: { pos: [3.2, 2.0, 6.4], at: [0, 1.6, 0], fov: 42 }, b: { pos: [2.6, 1.9, 5.6], at: [-.2, 1.6, 0], fov: 40 } }),
  upd: gaUpd,
  figs: (t, i) => FAKECOPS(t, { mouth: 'grin' }) + (t > wt(i, /lets/) - .2 ? fig([-.3, 0, -.2], 'guard', { mouth: 'smile', blink: bl(t, 2), look: [3, 2], hR: [210, 150] }, 1.7) : ''),
  ui: (t, i) => stampAt(1400, 300, t, wt(i, /rules/) - .05, 'AGAINST THE RULES', '#e0303a', 70, 8),
  sfx: i => [{ k: 'impact', t: wt(i, /rules/), g: .5 }, { k: 'click', t: wt(i, /lets/) }] };
SHOT.g_basement = { set: 'GAR', light: 'indoorDark',
  cam: i => ({ a: { pos: [GB[0], 1.8, GB[2] + 4], at: [GB[0], 1.2, GB[2] - 2.2], fov: 46 }, b: { pos: [GB[0], 1.7, GB[2] + 3], at: [GB[0], 1.2, GB[2] - 2.2], fov: 44 } }),
  figs: (t, i) => { const rope = `<path d="M50,170 Q100,184 150,170 M50,200 Q100,214 150,200 M56,230 Q100,244 144,230" stroke="#b8863a" stroke-width="12" fill="none"/><circle cx="100" cy="206" r="10" fill="#b8863a" stroke="${OL}" stroke-width="3"/>`; let h = '';
    [-1.6, 1.6].forEach((dx, k) => h += fig([GB[0] + dx, 0, GB[2] - 1.9], 'guard', { mouth: 'o', blink: bl(t, k), look: [k ? -4 : 4, 2], armL: [.05, .05], armR: [.05, .05], front: rope, sweat: true, tilt: Math.sin(t * 3 + k) * .05 })); return h },
  ui: (t, i) => stampAt(960, 280, t, wt(i, /tied/) - .05, 'TIED UP', '#e0303a', 110, -6) + pillAt(960, 160, t, wt(i, /basement/) - .1, nextStart(i), '⬇️ BASEMENT', '#232838', '#fff', 46),
  sfx: i => [{ k: 'impact', t: wt(i, /tied/) }, { k: 'pop', t: wt(i, /basement/) }] };
SHOT.g_walk = { set: 'GAR', light: 'indoorDark',
  cam: i => ({ a: { pos: [GI[0] - 6, 3.0, GI[2] + 5.5], at: [GI[0], 2.2, GI[2] - 4], fov: 52 }, b: { pos: [GI[0] - 2, 2.8, GI[2] + 5], at: [GI[0] + 2, 2.2, GI[2] - 4], fov: 50 } }),
  upd: gaUpd,
  figs: (t, i) => { let h = ''; [0, 1].forEach(k => { const u = cl((t - Lt(i).start - k * .4) / 4, 0, 1); h += fig([lerp(GI[0] - 7, GI[0] + 1 + k * 1.6, ez(u)), 0, GI[2] - 2.6 + k * 1.2], 'fakecop', Object.assign({ mouth: 'grin', blink: bl(t, k), look: [5, -2], prop: `<g transform="rotate(-70)"><rect x="-8" y="-40" width="16" height="40" rx="4" fill="#3a3a44" stroke="${OL}" stroke-width="4"/></g>`, hR: [214, 130] }, u < 1 ? walk(t + k) : {})) }); return h },
  ui: (t, i) => { const a = Lt(i).start + .2, b = wt(i, /minutes/) + .2; return counter(960, 200, t, a, nextStart(i), a, b, 0, 80, v => '⏱ ' + Math.round(v) + ' MINUTES', '#232838', '#fff', 64) + `<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 60% 45%,transparent 25%,#0008 70%);z-index:1500"></div>` },
  sfx: i => [{ k: 'tick', t: Lt(i).start + .3 }, { k: 'ding', t: wt(i, /minutes/) }] };
SHOT.g_take = { set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0] - 1, 3.2, GI[2] + 2.4], at: [GI[0], 3.0, GI[2] - 6.75], fov: 54 }, b: { pos: [GI[0], 3.1, GI[2] + 1.4], at: [GI[0], 3.0, GI[2] - 6.75], fov: 52 } }),
  upd: gaUpd,
  ui: (t, i) => { let h = counter(960, 160, t, Lt(i).start + .1, nextStart(i), Lt(i).start + .2, wt(i, /works/), 0, 13, v => '🖼️ ' + Math.round(v) + ' WORKS', '#232838', '#fff', 60);
    const q1 = w.project(X(FR_STORM.p, 0, -1.8, 0)), q2 = w.project(X(FR_MUSIC.p, 0, -1.5, 0));
    if (t > wt(i, /rembrandt/i) - .1) h += `<div style="position:absolute;left:${q1.x}px;top:${q1.y}px;transform:translate(-50%,0) scale(${pop(t, wt(i, /rembrandt/i) - .1)});z-index:2200">${PILL('REMBRANDT', '#c9a23c', OL, 40)}</div>`;
    if (t > wt(i, /vermeer/i) - .1) h += `<div style="position:absolute;left:${q2.x}px;top:${q2.y}px;transform:translate(-50%,0) scale(${pop(t, wt(i, /vermeer/i) - .1)});z-index:2200">${PILL('VERMEER', '#c9a23c', OL, 40)}</div>`;
    return h },
  sfx: i => [{ k: 'swish', t: wt(i, /rembrandt/i), d: .4 }, { k: 'swish', t: wt(i, /vermeer/i), d: .4 }] };
SHOT.g_value = { set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0], 3.1, GI[2] + 1.4], at: [GI[0], 3.0, GI[2] - 6.75], fov: 52 }, b: { pos: [GI[0], 3.0, GI[2] - .4], at: [GI[0], 3.0, GI[2] - 6.75], fov: 50 } }),
  upd: gaUpd,
  ui: (t, i) => { const a = Lt(i).start + .2, b = wt(i, /dollars/); return counter(960, 230, t, a, nextStart(i), a, b, 0, 500, v => '$' + Math.round(v) + ' MILLION', '#35a862', '#fff', 96) + bigText(960, 400, t, wt(i, /biggest/) - .1, nextStart(i), 'BIGGEST ART THEFT IN HISTORY', 70, '#ffd166', -3) },
  sfx: i => [{ k: 'cash', t: wt(i, /dollars/) }, { k: 'impact', t: wt(i, /biggest/), g: .6 }] };
SHOT.g_reward = { set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0] + 2, 3.0, GI[2] + 3], at: [GI[0], 2.8, GI[2] - 6.75], fov: 50 }, b: { pos: [GI[0] + 1, 3.0, GI[2] + 2], at: [GI[0], 2.8, GI[2] - 6.75], fov: 50 } }),
  upd: gaUpd,
  ui: (t, i) => { const a = wt(i, /reward/) - .2; if (t < a) return ''; return `<div style="position:absolute;left:960px;top:460px;transform:translate(-50%,-50%) rotate(-3deg) scale(${pop(t, a, .45)});width:620px;background:#f3e6c4;border:10px solid ${OL};border-radius:14px;padding:24px 20px;text-align:center;box-shadow:0 18px 0 #0005;z-index:2200">
      <div style="font:900 84px/1 IB;color:#c0303a">REWARD</div><div style="font:900 88px/1.1 IB;color:${OL}">$10,000,000</div><div style="font:700 34px/1.2 P;color:${OL}">for information leading to the recovery of the art</div></div>` +
      stampAt(1450, 700, t, wt(i, /never/) - .05, 'NEVER PAID', '#e0303a', 80, 10) },
  sfx: i => [{ k: 'cash', t: wt(i, /reward/) }, { k: 'impact', t: wt(i, /never/), g: .5 }] };
SHOT.g_fbi = { set: 'GAR', light: 'indoorDark',
  cam: i => ({ a: { pos: [GI[0], 1.8, GI[2] + 2.6], at: [GI[0], 1.3, GI[2] - 2], fov: 46 }, b: { pos: [GI[0], 1.7, GI[2] + 1.8], at: [GI[0], 1.3, GI[2] - 2], fov: 44 } }),
  upd: gaUpd,
  figs: (t, i) => { const a = wt(i, /two/) - .1; if (t < a) return ''; return [-1, 1].map((dx, k) => fig([GI[0] + dx, 0, GI[2] - 2], 'thief', { ghost: true, ghostA: .7 * ez(cl(t, a + k * .2, a + .5 + k * .2)), hat: '' })).join('') },
  ui: (t, i) => pillAt(960, 180, t, wt(i, /fbi/i) - .1, nextStart(i), '🕵️ FBI: TWO SUSPECTS', '#232838', '#fff', 56) + stampAt(960, 420, t, wt(i, /dead/) - .05, 'BOTH DEAD', '#e0303a', 110, -6),
  sfx: i => [{ k: 'pop', t: wt(i, /fbi/i) }, { k: 'impact', t: wt(i, /dead/) }] };
SHOT.g_frames_end = { set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0] - 3, 3.0, GI[2] + 2.6], at: [GI[0] - 3, 3.1, GI[2] - 6.75], fov: 50 }, b: { pos: [GI[0] - 4.6, 3.3, GI[2] - 2.6], at: [GI[0] - 5, 3.3, GI[2] - 6.75], fov: 44 } }),
  upd: gaUpd,
  ui: (t, i) => bigText(960, 180, t, wt(i, /empty/) - .1, nextStart(i), 'STILL EMPTY', 110, '#fff', -2),
  sfx: i => [{ k: 'ding', t: wt(i, /empty/) }] };
SHOT.outro = { set: 'GAR', light: 'indoorWarm',
  cam: i => ({ a: { pos: [GI[0] + 3.6, 2.4, GI[2] + 2.4], at: [GI[0] + 10.75, 2.6, GI[2] - .4], fov: 54 }, b: { pos: [GI[0] + 4.4, 2.2, GI[2] + 1.6], at: [GI[0] + 10.75, 2.4, GI[2] - .4], fov: 52 } }),
  upd: gaUpd,
  figs: (t, i) => fig([GI[0] + 8, 0, GI[2] + 1.6], 'sam', { mouth: 'grin', talk: tk(t, i) * .8, blink: bl(t, 0), look: [-5, 0], hR: [214, 90 + 10 * Math.sin(t * 4)] }),
  ui: (t, i) => { let h = ''; CASES.forEach((c, j) => { const q = w.project(X(c.p, -.1, 1.05, 0)); if (q.vis) h += `<div style="position:absolute;left:${q.x}px;top:${q.y}px;transform:translate(-50%,-100%);font:900 56px IB;color:${j == 5 ? '#ffd166' : '#fff'};text-shadow:${shadowTxt(OL, 5)};z-index:2100">#${6 - j}</div>` });
    h += bigText(960, 150, t, Lt(i).start + .1, 1e9, 'WHICH WAS THE BOLDEST? 💬', 84);
    h += pillAt(960, 270, t, wt(i, /subscribe/) - .1, 1e9, '🔔 SUBSCRIBE', '#e0303a', '#fff', 60); return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'ding', t: wt(i, /subscribe/) }] };
