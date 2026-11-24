// ===================== Set BOS: Boston 1950 (Strasse Nacht, Dach, Tresorraum, Versteck, FBI-Buero, Gefaengnis) =====================
const S = 'BOS';
const VR = [0, 0, -60], SH = [60, 0, 0], FB = [100, 0, 0], PR = [140, 0, 0], AL = [-60, 0, 0];
const DOOR = [3, 0, 0];          // Personaltuer (Fassade z=0)
(function street() {
  const BR = '#9a5a44', BR2 = '#86503c';
  mk(S, merge([at(G.box(200, .4, 60, '#3a3f55', { base: true }), [0, -.4, 10]), at(G.box(200, .25, 2.4, '#6a6e80', { base: true }), [0, 0, 1.2]), at(G.box(200, .25, 2.4, '#6a6e80', { base: true }), [0, 0, 20.8])]), { outline: false });
  // Brink's-Gebaeude (3 Etagen)
  const F = [at(G.box(22, 12, 10, BR, { base: true }), [0, 0, -5]), at(G.box(22.4, .5, 10.4, '#d8d0c0', { base: true }), [0, 12, -5]), at(G.box(22.2, .3, .4, '#d8d0c0', { base: true }), [0, 4.2, .1]), at(G.box(22.2, .3, .4, '#d8d0c0', { base: true }), [0, 8.1, .1])];
  F.push(at(G.box(4.4, 3.8, .3, '#3d5a4a', { base: true }), [-5, 0, .05]));                  // Garagentor
  for (let k = 0; k < 6; k++) F.push(at(G.box(4.2, .08, .05, '#2c4236', { base: true }), [-5, .5 + k * .6, .22]));
  F.push(at(G.box(1.5, 2.7, .25, '#5a3a2a', { base: true }), [DOOR[0], 0, .05]), at(G.box(1.8, .3, .5, '#d8d0c0', { base: true }), [DOOR[0], 2.7, .1]));
  for (let fl = 0; fl < 2; fl++) for (let k = 0; k < 8; k++) F.push(at(G.box(1.3, 2.0, .2, '#2a2a3a', { base: true }), [-8.8 + k * 2.5, 5.0 + fl * 3.9, .02]));
  F.push(at(G.box(1.2, 1.4, .2, '#2a2a3a', { base: true }), [7.5, 1.4, .02]), at(G.box(1.2, 1.4, .2, '#2a2a3a', { base: true }), [9.5, 1.4, .02]));
  mk(S, merge(F).vary(.03, 5));
  // beleuchtete Fenster (2. Etage = Geldraum)
  const WL = []; for (let k = 0; k < 8; k++) if (k % 3 != 1) WL.push(at(G.box(1.1, 1.8, .1, '#ffe2a0', { base: true }), [-8.8 + k * 2.5, 5.1, .14]));
  WL.push(at(G.box(.12, .12, .05, '#ffd166'), [DOOR[0] + .5, 1.2, .2]));
  mk(S, merge(WL), { emis: .45, outline: false, cast: false });
  // Nachbarhaeuser + gegenueberliegende Zeile (mit Flachdach fuer die Beobachter)
  const N = [];
  [[-17, 9, '#7a5a6a'], [-28, 13, BR2], [17, 10, '#6a6a80'], [28, 8, BR]].forEach(([x, h, c]) => { N.push(at(G.box(11.6, h, 10, c, { base: true }), [x, 0, -5]));
    for (let r = 0; r < Math.floor(h / 3.4); r++) for (let k = 0; k < 4; k++) N.push(at(G.box(1.2, 1.7, .2, '#2a2a3a', { base: true }), [x - 4.2 + k * 2.8, 1.6 + r * 3.4, .02])) });
  for (let k = -3; k <= 3; k++) { const x = k * 12, h = 10 + (k == 0 ? 0 : (k % 2) * 2.5); N.push(at(G.box(11.8, h, 8, k % 2 ? '#6a4a40' : '#7d5f4c', { base: true }), [x, 0, 26]), at(G.box(11.8, .6, .4, '#5a3e34', { base: true }), [x, h, 22.2])) }
  mk(S, merge(N).vary(.04, 9));
  // Laternen
  [-12, 0, 12].forEach(dx => { mk(S, merge([at(G.cyl(.1, .1, 4.6, 8, '#22252e'), [dx, 0, 2.2])])); mk(S, G.box(.5, .5, .5, '#ffe7a0', { base: true }), { pos: [dx, 4.6, 2.2], emis: 1, outline: false, cast: false }) });
  // Mond
  mk(S, G.ico(6, 3, '#f4efd8'), { pos: [-40, 70, -150], emis: 1, outline: false, cast: false, recv: false });
  // ---- Tresorraum (2. Etage, hier separat bei z=-60) ----
  const V = [at(G.box(16, .3, 13, '#6a5e52', { base: true }), [VR[0], -.3, VR[2]]), at(G.box(16, 5, .4, '#8a8e9a', { base: true }), [VR[0], 0, VR[2] - 6.5]),
    at(G.box(.4, 5, 13, '#9a9eaa', { base: true }), [VR[0] - 8, 0, VR[2]]), at(G.box(.4, 5, 13, '#9a9eaa', { base: true }), [VR[0] + 8, 0, VR[2]])];
  V.push(at(G.cyl(2.3, 2.3, .6, 28, '#b8bcc8'), [VR[0] + 2.4, 2.5, VR[2] - 6.3], [PI / 2, 0, 0]), at(G.cyl(1.9, 1.9, .2, 28, '#9aa0ae'), [VR[0] + 2.4, 2.5, VR[2] - 5.7], [PI / 2, 0, 0]),
    at(G.cyl(.35, .35, .5, 16, '#ffd166'), [VR[0] + 2.4, 2.5, VR[2] - 5.6], [PI / 2, 0, 0]));
  for (let k = 0; k < 3; k++) V.push(at(G.box(2.6, .14, .14, '#ffd166'), [VR[0] + 2.4, 2.5, VR[2] - 5.3], [0, 0, k * PI / 3]));
  // Zaehltische mit Geldstapeln
  [-3.2, 3.4].forEach((x, j) => { V.push(at(G.box(3.4, .12, 1.5, '#8a6a4a', { base: true }), [VR[0] + x, 1.0, VR[2] - 1.5]), at(G.box(.12, 1.0, .12, '#5a4632', { base: true }), [VR[0] + x - 1.5, 0, VR[2] - 2.1]), at(G.box(.12, 1.0, .12, '#5a4632', { base: true }), [VR[0] + x + 1.5, 0, VR[2] - .9]),
    at(G.box(.12, 1.0, .12, '#5a4632', { base: true }), [VR[0] + x + 1.5, 0, VR[2] - 2.1]), at(G.box(.12, 1.0, .12, '#5a4632', { base: true }), [VR[0] + x - 1.5, 0, VR[2] - .9]));
    for (let k = 0; k < 6; k++) V.push(at(G.box(.42, .16 + (k % 3) * .1, .24, '#5fb06a', { base: true }), [VR[0] + x - 1.2 + k * .48, 1.12, VR[2] - 1.5 + (k % 2) * .3])) });
  // Regal mit Geldsaecken
  V.push(at(G.box(4, .12, 1, '#6a5038', { base: true }), [VR[0] - 4.5, 1.6, VR[2] - 5.8]), at(G.box(4, .12, 1, '#6a5038', { base: true }), [VR[0] - 4.5, 3.0, VR[2] - 5.8]));
  for (let k = 0; k < 6; k++) V.push(at(G.ico(.4, 2, '#cdb98a'), [VR[0] - 6 + (k % 3) * 1.3, 2.05 + Math.floor(k / 3) * 1.4, VR[2] - 5.7], [0, 0, 0], [1, 1.1, .8]));
  mk(S, merge(V).vary(.02, 13));
  mk(S, merge([-4, 0, 4].map(x => at(G.box(1.6, .08, .5, '#fff6dc'), [VR[0] + x, 4.9, VR[2]]))), { emis: 1, outline: false, cast: false });
  // ---- Versteck (Tisch mit Beute) ----
  const SV = [at(G.box(20, .3, 14, '#5a4a3e', { base: true }), [SH[0], -.3, SH[2]]), at(G.box(20, 6, .4, '#7a6a5a', { base: true }), [SH[0], 0, SH[2] - 4]),
    at(G.box(4.6, .14, 2, '#8a6038', { base: true }), [SH[0], 1.0, SH[2]]), ...[[-2.1, -.8], [2.1, -.8], [-2.1, .8], [2.1, .8]].map(([x, z]) => at(G.box(.14, 1.0, .14, '#5a4028', { base: true }), [SH[0] + x, 0, SH[2] + z])),
    at(G.box(1.6, 1.3, .1, '#3a4a6a', { base: true }), [SH[0] - 4, 2.2, SH[2] - 3.75])];
  mk(S, merge(SV).vary(.03, 17));
  mk(S, merge([at(G.cyl(.04, .04, 2.2, 6, '#22252e'), [SH[0], 3.4, SH[2]]), at(G.cyl(.7, .25, .5, 16, '#3f6a4a'), [SH[0], 3.0, SH[2]])]), { cast: false });
  mk(S, G.ico(.22, 2, '#fff2c0'), { pos: [SH[0], 2.95, SH[2]], emis: 1, outline: false, cast: false });
  // ---- FBI-Buero ----
  const FV = [at(G.box(16, .3, 12, '#6a5a4a', { base: true }), [FB[0], -.3, FB[2]]), at(G.box(16, 6, .4, '#c9c0a8', { base: true }), [FB[0], 0, FB[2] - 4]),
    at(G.box(3.4, .14, 1.6, '#6a4a30', { base: true }), [FB[0] - 1.2, 1.0, FB[2] - 1.0]), at(G.box(3.2, 1.0, .1, '#5a3e26', { base: true }), [FB[0] - 1.2, 0, FB[2] - .25]),
    at(G.box(1.1, 2.2, .9, '#7a8090', { base: true }), [FB[0] + 3.4, 0, FB[2] - 3.3]), ...[0, 1, 2].map(k => at(G.box(.9, .05, .05, '#4a4e5a'), [FB[0] + 3.4, .6 + k * .7, FB[2] - 2.83])),
    at(G.box(2.4, 1.6, .1, '#2a3a5a', { base: true }), [FB[0] - 1.2, 2.4, FB[2] - 3.75]), at(G.box(.5, .36, .7, '#e8e4d8', { base: true }), [FB[0] - 2.2, 1.14, FB[2] - 1.0])];
  for (let k = 0; k < 6; k++) FV.push(at(G.box(2.4, .06, .05, '#9aa8c8'), [FB[0] - 1.2, 2.6 + k * .24, FB[2] - 3.68]));
  mk(S, merge(FV).vary(.03, 19));
  mk(S, G.box(.4, .26, .4, '#f0c040', { base: true }), { pos: [FB[0] - .2, 1.6, FB[2] - 1.2], emis: .6, outline: false, cast: false });
  mk(S, merge([at(G.cyl(.04, .04, .5, 6, '#2a2e3a'), [FB[0] - .2, 1.14, FB[2] - 1.2])]), { cast: false });
  // ---- Gefaengnis ----
  mk(S, merge([at(G.box(20, .3, 12, '#5a5e6a', { base: true }), [PR[0], -.3, PR[2]]), at(G.box(20, 6, .4, '#8a8e98', { base: true }), [PR[0], 0, PR[2] - 3]),
    at(G.box(12, .5, .8, '#6a6e78', { base: true }), [PR[0], 0, PR[2] - 2.4]), at(G.box(1.2, .9, .1, '#2a2e3a', { base: true }), [PR[0] - 3, 3.6, PR[2] - 2.75])]).vary(.03, 23), { outline: false });
  // ---- dunkle Gasse (Auftragsmoerder) ----
  mk(S, merge([at(G.box(30, .3, 20, '#2e3346', { base: true }), [AL[0], -.3, AL[2]]), at(G.box(30, 9, .4, '#5a3e36', { base: true }), [AL[0], 0, AL[2] - 3]),
    at(G.box(1.4, 1.2, 1, '#3a4a3a', { base: true }), [AL[0] + 3.4, 0, AL[2] - 2.2]), at(G.box(.9, 1.3, .9, '#4a4a52', { base: true }), [AL[0] - 3.6, 0, AL[2] - 2.2])]).vary(.03, 29), { outline: false });
  mk(S, G.box(.4, .4, .3, '#ffe7a0', { base: true }), { pos: [AL[0] + .6, 3.6, AL[2] - 2.75], emis: 1, outline: false, cast: false });
})();
// Fluchtwagen (gruener Pritschen-LKW, 1949er Stil)
const TRUCK = mk(S, merge([
  at(G.box(2.0, 1.4, 2.1, '#3f7a4a', { base: true }), [2.4, .65, 0]), at(G.box(1.2, .9, 2.0, '#3f7a4a', { base: true }), [3.9, .65, 0]), at(G.box(1.2, .55, 1.6, '#2a3a5a', { base: true }), [2.5, 1.35, 0]),
  at(G.box(5.0, .24, 2.3, '#5a4632', { base: true }), [-1.1, .75, 0]), ...[-3.4, -2.0, -.6, .6].flatMap(x => [at(G.box(.12, 1.0, .12, '#6a5038', { base: true }), [x, .95, 1.1]), at(G.box(.12, 1.0, .12, '#6a5038', { base: true }), [x, .95, -1.1])]),
  at(G.box(4.9, .12, .1, '#6a5038'), [-1.1, 1.7, 1.12]), at(G.box(4.9, .12, .1, '#6a5038'), [-1.1, 1.7, -1.12]),
  ...[[3.4, 1.05], [3.4, -1.05], [-2.4, 1.05], [-2.4, -1.05]].map(([x, z]) => at(G.cyl(.48, .48, .3, 14, '#1b1b22', { cap: '#777' }), [x, .48, z + (z > 0 ? 0 : -.3)], [PI / 2, 0, 0])),
  at(G.box(.1, .3, .3, '#ffe7a0'), [4.52, 1.0, .7]), at(G.box(.1, .3, .3, '#ffe7a0'), [4.52, 1.0, -.7])]).vary(.03, 31), { pos: [12.5, 0, 6.5] });
const TSACKS = [...Array(4)].map((_, k) => mk(S, G.ico(.42, 2, '#cdb98a'), { pos: [12.5 - 3.2 + k * .8, 1.15, 6.5 + (k % 2 ? .4 : -.4)], scl: [.6, .5, .55], vis: false, emis: .25 }));
TSACKS.forEach(m => m._auto = false);
// ---------- Figuren-Looks fuer diesen Fall ----------
const MASKC = ['#f0c27a', '#e8a0a0', '#b8d68a', '#9ac4e8', '#e8d070', '#d0a8e0', '#f0b090'];
const MASK = c => `<ellipse cx="100" cy="90" rx="58" ry="56" fill="${c}" stroke="${OL}" stroke-width="5"/><ellipse cx="84" cy="86" rx="11" ry="9" fill="#14141a"/><ellipse cx="118" cy="86" rx="11" ry="9" fill="#14141a"/>` +
  `<ellipse cx="66" cy="108" rx="10" ry="6" fill="#e0505a" opacity=".55"/><ellipse cx="136" cy="108" rx="10" ry="6" fill="#e0505a" opacity=".55"/><path d="M74,114 Q100,140 128,114 Q100,126 74,114Z" fill="#fff" stroke="${OL}" stroke-width="4" stroke-linejoin="round"/>` +
  `<path d="M66,70 Q84,62 96,70 M106,70 Q118,62 136,70" stroke="${OL}" stroke-width="0" fill="none"/>`;
const PEA = `<circle cx="88" cy="182" r="5" fill="#c9ccd4" stroke="${OL}" stroke-width="2"/><circle cx="112" cy="182" r="5" fill="#c9ccd4" stroke="${OL}" stroke-width="2"/><circle cx="88" cy="206" r="5" fill="#c9ccd4" stroke="${OL}" stroke-width="2"/><circle cx="112" cy="206" r="5" fill="#c9ccd4" stroke="${OL}" stroke-width="2"/><path d="M76,150 L100,172 L124,150" stroke="#0e1424" stroke-width="5" fill="none"/>`;
const GLASSES = `<circle cx="84" cy="86" r="15" fill="#bfe6ff55" stroke="${OL}" stroke-width="5"/><circle cx="118" cy="86" r="15" fill="#bfe6ff55" stroke="${OL}" stroke-width="5"/><path d="M99,86 L103,86" stroke="${OL}" stroke-width="5"/>`;
const FEDORA = `<path d="M46,48 Q42,4 100,2 Q158,4 154,48Z" fill="#3a3e4a" stroke="${OL}" stroke-width="6"/><path d="M28,48 Q100,34 172,48 Q174,60 100,58 Q26,60 28,48Z" fill="#2a2e38" stroke="${OL}" stroke-width="5"/><rect x="50" y="36" width="100" height="10" fill="#c0303a"/>`;
const HAIRS = [`<path d="M40,60 Q44,14 100,16 Q156,14 160,60 Q140,34 100,36 Q60,34 40,60Z" fill="#5a3a24" stroke="${OL}" stroke-width="5"/>`, `<path d="M42,56 Q56,22 100,22 Q144,22 158,56 Q124,40 100,42 Q76,40 42,56Z" fill="#2a2a30" stroke="${OL}" stroke-width="5"/>`,
  `<path d="M44,50 Q60,24 100,24 Q140,24 156,50 Q120,38 100,40 Q80,38 44,50Z" fill="#8a6a3a" stroke="${OL}" stroke-width="5"/>`];
Object.assign(LOOK, {
  rob: k => ({ sw: '#1f2a4a', swd: '#162038', pa: '#2a2a33', hat: MASK(MASKC[k % MASKC.length]) + HAT.driver, mid: PEA }),
  gang: k => ({ sw: ['#1f2a4a', '#4a3a2e', '#2e4a3a', '#4a2e3a'][k % 4], swd: '#1a1e2c', pa: '#2a2a33', hat: k == 1 ? FEDORA : HAIRS[k % 3] }),
  specs: { sw: '#5a4a3a', swd: '#44382c', pa: '#2a2a33', hat: HAIRS[1] + GLASSES },
  clerk: k => ({ sw: '#e8e4d8', swd: '#c8c4b8', pa: '#3a3e4a', hat: HAIRS[k % 3], mid: MID.tie }),
  agent: { sw: '#4a4f5e', swd: '#383c48', pa: '#3a3e4a', hat: FEDORA, mid: MID.tie },
  hitman: { sw: '#16181f', swd: '#0e1016', pa: '#16181f', hat: FEDORA },
});
// LOOK-Eintraege koennen Funktionen sein (Variante k)
const L_ = (who, k) => { const v = LOOK[who]; return typeof v == 'function' ? v(k) : v };
function figk(p, who, k, o = {}, H3 = 1.75, clipY = null) { const look = L_(who, k); const sv = LOOK.__tmp; LOOK.__tmp = look; const h = fig(p, '__tmp', o, H3, clipY); LOOK.__tmp = sv; return h }
const P_SACK = `<g transform="translate(-34,-14)"><path d="M10,6 Q34,-8 58,6 L66,60 Q34,74 2,60 Z" fill="#cdb98a" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/><path d="M14,8 Q34,18 54,8" fill="none" stroke="${OL}" stroke-width="4"/><text x="34" y="52" text-anchor="middle" font-family="IB,Arial" font-weight="900" font-size="28" fill="#2f6e3c">$</text></g>`;
const P_EMPTY = `<g transform="translate(-26,-6) rotate(14)"><path d="M10,0 L42,0 L48,40 Q26,48 4,40Z" fill="#d8c8a0" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/><path d="M14,4 Q26,22 40,4" fill="none" stroke="${OL}" stroke-width="3"/></g>`;
const P_SCREW = `<g transform="rotate(-30)"><rect x="-6" y="-40" width="12" height="30" rx="5" fill="#e0303a" stroke="${OL}" stroke-width="4"/><rect x="-2" y="-12" width="4" height="34" fill="#c9ccd4" stroke="${OL}" stroke-width="2"/></g>`;
const P_PAD = `<g transform="translate(-22,-30) rotate(-6)"><rect x="0" y="0" width="44" height="56" rx="4" fill="#fffdf2" stroke="${OL}" stroke-width="4"/><path d="M8,14 L36,14 M8,24 L34,24 M8,34 L30,34 M8,44 L26,44" stroke="#7a86b8" stroke-width="3"/></g>`;
const P_CASH = PROP.cash;
// ---------- Kamera-Positionen ----------
const HERO_A = { pos: [6.6, 2.0, 13.8], at: [5.0, 1.6, 2.8], fov: 46 }, HERO_B = { pos: [6.0, 1.6, 10.6], at: [4.9, 1.4, 3.0], fov: 44 };
const gangOut = (t, n = 5) => {   // Maskierte kommen mit Saecken aus der Tuer zum LKW
  let h = ''; for (let k = 0; k < n; k++) { const u = ((t * .16 + k / n) % 1), x = lerp(DOOR[0], 7.6, u), z = lerp(1.2, 5.6, u) + (k % 2) * .4;
    h += figk([x, 0, z], 'rob', k, Object.assign({ mouth: 'grin', blink: 0, look: [5, 2], propL: P_SACK, hL: [44, 226], hR: k % 2 ? [176, 150] : null, prop: k % 2 ? P_SACK : '' }, walk(t + k * .37, 8))) }
  return h };
SHOT.hero = { set: S, light: 'night', cam: i => ({ a: HERO_A, b: HERO_B }),
  upd: (t, i) => { TSACKS.forEach((m, k) => m.vis = true) },
  figs: (t, i) => gangOut(t),
  sfx: i => [{ k: 'pop', t: .2 }] };
SHOT.roof = { set: S, light: 'night',
  cam: i => ({ a: { pos: [1.4, 12.5, 30.5], at: [.6, 7.4, -1], fov: 46 }, b: { pos: [1.2, 12.1, 29.2], at: [.5, 7.1, -1], fov: 44 } }),
  figs: (t, i) => { let h = ''; [[.0, 23.2], [1.0, 23.7], [2.0, 23.2]].forEach(([x, z], k) => h += figk([x, 10, z], 'gang', k, { mouth: k == 1 ? 'hmm' : 'smile', talk: k == 1 ? tk(t, i) * .4 : 0, blink: bl(t, k), look: [-5, -3], prop: k == 2 ? PROP.magnifier : '', hR: k == 2 ? [150, 70] : null })); return h },
  ui: (t, i) => { let h = pillAt(540, 250, t, Lt(i).start + .1, nextStart(i), '📍 BOSTON · JANUARY 1950', '#232838', '#fff', 50);
    const a = wt(i, /eleven/) - .1; if (t > a) { let heads = ''; for (let k = 0; k < 11; k++) heads += `<div style="display:inline-block;margin:0 3px;transform:scale(${pop(t, a + k * .05, .25)})"><svg width="62" height="62" viewBox="0 0 60 60"><circle cx="30" cy="30" r="25" fill="#fff" stroke="${OL}" stroke-width="5"/><circle cx="23" cy="29" r="3.5" fill="${OL}"/><circle cx="37" cy="29" r="3.5" fill="${OL}"/></svg></div>`;
      h += `<div style="position:absolute;left:0;right:0;top:330px;text-align:center;z-index:2200">${heads}<div style="margin-top:6px;transform:scale(${pop(t, a + .4)})">${PILL('11 MEN', '#e0303a', '#fff', 60)}</div></div>` }
    h += pillAt(540, 640, t, wt(i, /brink/i) - .15, nextStart(i), "🏦 BRINK'S VAULT", '#ffd166', OL, 56);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, ...[0, 3, 6, 9].map(k => ({ k: 'pop', t: wt(i, /eleven/) + k * .05 })), { k: 'ding', t: wt(i, /brink/i) }] };
SHOT.keys = { set: S, light: 'night',
  cam: i => ({ a: { pos: [DOOR[0] + 1.2, 1.6, 6.0], at: [DOOR[0] - .3, 1.3, 0], fov: 42 }, b: { pos: [DOOR[0] + 1.0, 1.5, 5.0], at: [DOOR[0] - .25, 1.2, 0], fov: 40 } }),
  figs: (t, i) => figk([DOOR[0] - .55, 0, 1.0], 'gang', 0, { mouth: 'hmm', blink: bl(t, 0), look: [6, 2], hR: [196 + 8 * Math.sin(t * 14), 140], prop: P_SCREW, sweat: false }, 1.75),
  ui: (t, i) => {
    let h = pillAt(540, 250, t, wt(i, /months/) - .1, nextStart(i), '🗓 FOR MONTHS', '#232838', '#fff', 54);
    const a = wt(i, /copied/) - .1, b = wt(i, /every/) - .1;
    if (t > a) { const n = t > b ? 1 + Math.min(5, Math.floor((t - b) / .14)) : 1;
      let keys = ''; for (let k = 0; k < n; k++) keys += `<div style="display:inline-block;margin:0 -6px;transform:rotate(${-20 + k * 8}deg) scale(${pop(t, k == 0 ? a : b + (k - 1) * .14, .3)})"><svg width="170" height="300" viewBox="0 0 80 150"><circle cx="40" cy="30" r="24" fill="#ffd166" stroke="${OL}" stroke-width="6"/><circle cx="40" cy="30" r="9" fill="#fff6dc" stroke="${OL}" stroke-width="5"/><path d="M34,52 L46,52 L46,140 L60,140 L60,128 L52,128 L52,118 L62,118 L62,104 L46,104" fill="#ffd166" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/></svg></div>`;
      h += `<div style="position:absolute;left:0;right:0;top:360px;text-align:center;z-index:2200">${keys}</div>` }
    h += pillAt(540, 720, t, b + .2, nextStart(i), '🔑 EVERY DOOR', '#ffd166', OL, 58);
    return h },
  sfx: i => [{ k: 'pop', t: wt(i, /months/) }, { k: 'click', t: wt(i, /copied/) }, ...[0, 1, 2, 3, 4].map(k => ({ k: 'tick', t: wt(i, /every/) + k * .14, f: 1800 }))] };
SHOT.enter = { set: S, light: 'night',
  cam: i => ({ a: { pos: [DOOR[0] - 4.2, 1.1, 8.6], at: [DOOR[0] - .6, 1.5, 1], fov: 46 }, b: { pos: [DOOR[0] - 3.0, 1.3, 7.0], at: [DOOR[0] - .4, 1.5, .5], fov: 44 } }),
  figs: (t, i) => { let h = ''; const t0 = Lt(i).start, T = nextStart(i) - t0;
    for (let k = 0; k < 5; k++) { const u = ez(cl((t - t0 - k * .3) / (T * .9), 0, 1)), x = lerp(DOOR[0] - 4.5 - k * 1.0, DOOR[0] - .2 - k * .55, u), z = lerp(5.0 + (k % 2) * .6, 1.2 + k * .35, u);
      h += figk([x, 0, z], 'rob', k, Object.assign({ mouth: 'grin', blink: 0, look: [5, 1] }, u < 1 ? walk(t + k * .4, 8) : {})) }
    return h },
  ui: (t, i) => { const a = wt(i, /masks/) - .15; let h = pillAt(540, 250, t, Lt(i).start + .1, nextStart(i), '🕖 7:10 PM', '#232838', '#fff', 56);
    h += pillAt(540, 380, t, a, nextStart(i), '🎃 HALLOWEEN MASKS', '#ff8a3d', '#fff', 54) + pillAt(540, 490, t, a + .45, nextStart(i), "🧢 CHAUFFEUR'S CAPS + PEA COATS", '#3f7fb5', '#fff', 42);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'pop', t: wt(i, /masks/) - .15 }, { k: 'pop', t: wt(i, /masks/) + .3 }, { k: 'thud', t: wt(i, /walked/), g: .4 }] };
SHOT.vault = { set: S, light: 'vault',
  cam: i => ({ a: { pos: [VR[0] + .4, 2.6, VR[2] + 8.0], at: [VR[0], 1.7, VR[2] - 3], fov: 50 }, b: { pos: [VR[0], 2.3, VR[2] + 6.6], at: [VR[0], 1.6, VR[2] - 3], fov: 48 } }),
  figs: (t, i) => { let h = '';
    for (let k = 0; k < 3; k++) h += figk([VR[0] - 2.7 + k * .95, 0, VR[2] - 4.3 + (k % 2) * .3], 'clerk', k, { mouth: 'o', talk: 0, blink: bl(t, k), sweat: k % 2 == 0, look: [4, 0], hL: [30, 40 + 6 * Math.sin(t * 7 + k)], hR: [170, 40 + 6 * Math.sin(t * 7 + k + 1)] }, 1.7);
    [[-1.2, .6], [1.0, .9], [1.3, -2.6]].forEach(([dx, dz], k) => { const s = Math.abs(Math.sin(t * 6 + k));
      h += figk([VR[0] + dx, 0, VR[2] + dz], 'rob', k + 1, { mouth: 'grin', blink: 0, look: [k < 2 ? 5 : -5, 3], propL: P_SACK, hL: [60, 210], hR: [150 + 20 * s, 150 - 40 * s], prop: s > .5 ? P_CASH : '' }) });
    return h },
  ui: (t, i) => { const a = wt(i, /million/) - .3, v = lerp(0, 1218211, ez(cl(t, a - .4, a + .6)));
    let h = pillAt(540, 250, t, Lt(i).start + .1, nextStart(i), '⏱ ~20 MINUTES', '#232838', '#fff', 56);
    if (t > a - .4) h += pillAt(540, 400, t, a - .4, nextStart(i), MG.fmt(Math.round(v), 0, '$'), '#35a862', '#fff', 104) + pillAt(540, 530, t, a + .5, nextStart(i), '💵 IN CASH', '#ffd166', OL, 50);
    h += pillAt(540, 650, t, wt(i, /cash/) + .2, nextStart(i), '+ $1.5M IN CHECKS', '#3f7fb5', '#fff', 46);
    h += stampAt(540, 1180, t, wt(i, /cash/) + .55, 'BIGGEST U.S. ROBBERY', '#e0303a', 68, -6);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'cash', t: wt(i, /million/) + .4 }, { k: 'pop', t: wt(i, /cash/) + .2 }, { k: 'impact', t: wt(i, /cash/) + .55, g: .6 }] };
SHOT.split = { set: S, light: 'indoorWarm',
  cam: i => ({ a: { pos: [SH[0] + 1.0, 2.4, SH[2] + 9.4], at: [SH[0] + .3, 1.4, SH[2]], fov: 44 }, b: { pos: [SH[0] + 1.4, 2.0, SH[2] + 7.6], at: [SH[0] + .6, 1.3, SH[2]], fov: 42 } }),
  figs: (t, i) => { let h = ''; const sp = wt(i, /specs/i) - .1, ch = wt(i, /cheated/) - .1;
    [[-2.0, -.9], [-.7, -1.2], [.6, -1.2]].forEach(([dx, dz], k) => h += figk([SH[0] + dx, 0, SH[2] + dz], 'gang', k + 1, { mouth: 'grin', talk: .25 + .2 * Math.sin(t * 5 + k), blink: bl(t, k), look: [k - 1, 3], prop: P_CASH, hR: [180, 120 + 10 * Math.sin(t * 4 + k)], propL: P_SACK, hL: [44, 226] }));
    h += fig([SH[0] + 1.85, 0, SH[2] + .5], 'specs', { mouth: t > ch ? 'sad' : 'hmm', blink: bl(t, 3), sweat: t > ch, look: [-6, 2], propL: t > ch ? P_EMPTY : '', hL: t > ch ? [40, 150] : null, tilt: t > ch ? -.08 : 0 });
    return h },
  upd: (t, i) => {},
  ui: (t, i) => { let h = labelAt([SH[0] + 1.85, 2.25, SH[2] + .5], PILL('"SPECS"', '#232838', '#fff', 50), t, wt(i, /specs/i) - .15, nextStart(i));
    const ch = wt(i, /cheated/) - .1; h += pillAt(540, 260, t, ch, nextStart(i), 'HIS SHARE: $0?', '#e0303a', '#fff', 70);
    const piles = [...Array(10)].map((_, k) => `<div style="display:inline-block;margin:0 4px;transform:scale(${pop(t, Lt(i).start + .2 + k * .06, .25)})">${k == 9 && t > ch ? '<div style="width:62px;height:40px;border:5px dashed #e0303a;border-radius:6px"></div>' : '<div style="width:62px;height:40px;background:#5fb06a;border:5px solid ' + OL + ';border-radius:6px"></div>'}</div>`).join('');
    h += `<div style="position:absolute;left:0;right:0;top:420px;text-align:center;z-index:2200">${piles}</div>`.replace('top:420px','top:380px');
    return h },
  sfx: i => [{ k: 'cash', t: Lt(i).start + .3 }, { k: 'ding', t: wt(i, /specs/i) }, { k: 'error', t: wt(i, /cheated/) }] };
SHOT.fbi = { set: S, light: (t, i) => t < wt(i, /told/) - .15 ? 'night' : 'indoorWarm',
  cam: i => { const c = wt(i, /told/) - .15; return [
    { t0: Lt(i).start, a: { pos: [AL[0] + .4, 1.7, AL[2] + 7.0], at: [AL[0] + .2, 1.4, AL[2]], fov: 44 }, b: { pos: [AL[0] + .3, 1.5, AL[2] + 5.8], at: [AL[0] + .2, 1.3, AL[2]], fov: 42 } },
    { t0: c, a: { pos: [FB[0] - .8, 2.0, FB[2] + 7.2], at: [FB[0] - .8, 1.4, FB[2] - 1], fov: 44 }, b: { pos: [FB[0] - .8, 1.8, FB[2] + 6.2], at: [FB[0] - .8, 1.3, FB[2] - 1], fov: 42 }}] },
  figs: (t, i) => { const c = wt(i, /told/) - .15; let h = '';
    if (t < c) { const u = ez(cl((t - Lt(i).start) / (c - Lt(i).start), 0, 1));
      h += fig([AL[0] - .7, 0, AL[2] + .4], 'specs', Object.assign({ mouth: t > wt(i, /hitman/) ? 'o' : 'hmm', blink: bl(t, 0), sweat: t > wt(i, /hitman/), look: [5, 0] }, walk(t, 7)));
      h += fig([lerp(AL[0] + 2.2, AL[0] + .9, u), 0, AL[2] - 1.0], 'hitman', Object.assign({ mouth: 'hmm', blink: 0, look: [-6, 1] }, u < 1 ? walk(t, 6) : {})) }
    else { h += fig([FB[0] - 1.9, 0, FB[2] + .6], 'specs', { mouth: 'hmm', talk: .5 + .4 * Math.sin(t * 9), blink: bl(t, 1), look: [5, 0], hR: [176, 150 + 14 * Math.sin(t * 6)] });
      h += fig([FB[0] + .3, 0, FB[2] - 1.6], 'agent', { mouth: 'smile', blink: bl(t, 2), look: [-6, 2], prop: P_PAD, hR: [160, 160], hL: [70, 170] }) }
    return h },
  ui: (t, i) => { const c = wt(i, /told/) - .15; let h = '';
    h += stampAt(540, 380, t, wt(i, /hitman/) - .05, 'HITMAN!', '#e0303a', 110, -7, c);
    h += pillAt(540, 280, t, c + .05, nextStart(i), '🕵 FBI', '#232838', '#fff', 70) + pillAt(540, 410, t, wt(i, /everything/) - .1, nextStart(i), '🗣 "THE FULL STORY"', '#ffd166', OL, 52);
    return h },
  sfx: i => [{ k: 'impact', t: wt(i, /hitman/), g: .6 }, { k: 'pop', t: wt(i, /told/) }, { k: 'type', t: wt(i, /everything/), n: 8 }] };
SHOT.prison = { set: S, light: (t, i) => t < wt(i, /eight/i) - .15 ? 'indoorWarm' : 'vault',
  cam: i => { const c = wt(i, /eight/i) - .15; return [
    { t0: Lt(i).start, a: { pos: [FB[0] - .8, 1.8, FB[2] + 6.2], at: [FB[0] - .8, 1.3, FB[2] - 1], fov: 42 }, b: { pos: [FB[0] - .8, 2.2, FB[2] + 7.6], at: [FB[0] - .8, 1.5, FB[2] - 1], fov: 46 } },
    { t0: c, a: { pos: [PR[0], 1.8, PR[2] + 7.4], at: [PR[0], 1.1, PR[2] - 1], fov: 48 }, b: { pos: [PR[0], 1.6, PR[2] + 6.6], at: [PR[0], 1.0, PR[2] - 1], fov: 46 } }] },
  figs: (t, i) => { const c = wt(i, /eight/i) - .15; let h = '';
    if (t < c) { [[-1.9, .6, 'agent'], [.3, -1.6, 'agent']].forEach(([dx, dz, who], k) => h += fig([FB[0] + dx, 0, FB[2] + dz], who, { mouth: 'grin', blink: bl(t, k), look: [k ? -5 : 5, 2], prop: k ? P_PAD : '', hR: k ? [160, 160] : [190, 60] })); return h }
    for (let k = 0; k < 8; k++) h += figk([PR[0] - 3.15 + k * .9, 0, PR[2] - 1.2 + (k % 2) * .5], 'gang', k, { sw: '#d0d0d0', swd: '#9a9a9a', pa: '#9a9a9a', mid: MID.stripes, mouth: 'sad', blink: bl(t, k), look: [0, 3], hat: HAIRS[k % 3] }, 1.65);
    return h },
  ui: (t, i) => { const c = wt(i, /eight/i) - .15; let h = '';
    if (t < c) { const a = Lt(i).start + .05, d = Math.min(9, Math.max(5, 9 - Math.floor((t - wt(i, /days/) + .1) / .22)));
      h += pillAt(540, 260, t, a, c, '🗓 JANUARY 1956', '#232838', '#fff', 56);
      h += `<div style="position:absolute;left:50%;top:360px;transform:translate(-50%,0) scale(${pop(t, a + .2)});width:520px;background:#fff;border:8px solid ${OL};border-radius:28px;box-shadow:0 12px 0 #2328384d;text-align:center;overflow:hidden;z-index:2200">
        <div style="background:#e0303a;color:#fff;font:900 46px/1.6 IB,Arial;text-shadow:${shadowTxt(OL, 3)}">⏳ 6-YEAR DEADLINE</div><div style="font:900 150px/1.1 IB,Arial;color:${OL}">${d}</div><div style="font:900 44px/1.4 IB,Arial;color:${OL}">DAYS LEFT</div></div>`;
      h += stampAt(540, 1060, t, wt(i, /charged/) - .05, 'CHARGED', '#e0303a', 100, -6, c);
      return h }
    for (let k = 0; k < 7; k++) h += `<div style="position:absolute;left:${110 + k * 140}px;top:0;width:28px;height:1290px;background:linear-gradient(90deg,#2a2a33,#6a6a76 45%,#2a2a33);border:4px solid ${OL};border-top:0;border-radius:0 0 14px 14px;z-index:1500"></div>`;
    h += `<div style="position:absolute;left:0;right:0;top:330px;height:26px;background:linear-gradient(#2a2a33,#6a6a76 45%,#2a2a33);border:4px solid ${OL};z-index:1500"></div>`;
    h += stampAt(540, 230, t, wt(i, /life/) - .05, '8 × LIFE', '#e0303a', 120, -6);
    return h },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .05 }, ...[1, 2, 3, 4].map(k => ({ k: 'tick', t: wt(i, /days/) - .1 + k * .22, f: 1500 })), { k: 'impact', t: wt(i, /charged/), g: .5 }, { k: 'thud', t: wt(i, /eight/i) - .1, g: .6 }, { k: 'impact', t: wt(i, /life/), g: .7 }] };
SHOT.end = { set: S, light: 'night', cam: i => ({ a: HERO_B, b: HERO_A }),
  upd: (t, i) => { TSACKS.forEach((m, k) => m.vis = true) },
  figs: (t, i) => gangOut(t),
  ui: (t, i) => { const t0 = Lt(i).start, k = pop(t, t0 + .1, .4);
    const btn = (txt, bg, d) => `<div style="flex:1;text-align:center;font:900 64px/1 IB,Arial;color:#fff;background:${bg};border:7px solid ${OL};border-radius:26px;padding:22px 0;text-shadow:${shadowTxt(OL, 3)};transform:scale(${pop(t, t0 + d, .3)})">${txt}</div>`;
    const o = fade(t, MG.TL.dur - .35, MG.TL.dur - .05);
    return `<div style="position:absolute;left:90px;right:90px;top:250px;opacity:${o};transform:scale(${k});background:#fff;border:8px solid ${OL};border-radius:34px;box-shadow:0 14px 0 #2328384d;padding:30px 34px;text-align:center;z-index:2200">
    <div style="font:900 62px/1.1 IB,Arial;color:${OL}">Would you have kept quiet? 🤐</div>
    <div style="display:flex;gap:30px;margin-top:26px">${btn('YES', '#35a862', .35)}${btn('NO', '#e0303a', .5)}</div></div>` },
  sfx: i => [{ k: 'pop', t: Lt(i).start + .1 }, { k: 'pop', t: Lt(i).start + .45 }, { k: 'pop', t: Lt(i).start + .6 }] };
