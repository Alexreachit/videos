// Sam als animierbare SVG-Figur (Regeln aus characters.py: runder cremefarbener Kopf, KEINE Ohren/Brauen/Nase,
// nur Punktaugen + Strichmund, navy Pullover, braune Hose). Gelenke: Schulter/Ellbogen je Arm, Beine, Kopfneigung.
// MG_SAM.svg(o) -> SVG-String, Fusspunkt = (100, 340) im 200x350-Raster.
(function () {
  const OL = '#232838', SK = '#f7e4b5', SKD = '#e6c587', SW = '#2f4372', SWD = '#22335a', PA = '#7b4b2a', PAD = '#5e381e', SH = '#4a2c1a';
  function arm(sx, sy, side, a, b, L1 = 50, L2 = 46) {
    const ex = sx + side * Math.sin(a) * L1, ey = sy + Math.cos(a) * L1;
    const a2 = a + b, hx = ex + side * Math.sin(a2) * L2, hy = ey + Math.cos(a2) * L2;
    const p = `M${sx.toFixed(1)},${sy.toFixed(1)} L${ex.toFixed(1)},${ey.toFixed(1)} L${hx.toFixed(1)},${hy.toFixed(1)}`;
    return { svg: `<path d="${p}" fill="none" stroke="${OL}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/><path d="${p}" fill="none" stroke="${SW}" stroke-width="21" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="M${(ex + side * 3).toFixed(1)},${(ey).toFixed(1)} L${(hx).toFixed(1)},${(hy).toFixed(1)}" stroke="${SWD}" stroke-width="5" stroke-linecap="round" opacity=".35"/>` +
      `<circle cx="${hx.toFixed(1)}" cy="${hy.toFixed(1)}" r="13" fill="${SK}" stroke="${OL}" stroke-width="5"/>`, hx, hy };
  }
  // IK: Hand-Ziel (hx,hy) im Rig-Raster -> [a,b]; el=+1 Ellbogen nach aussen/unten, -1 andersrum
  function ik(sx, sy, side, hx, hy, el = 1, L1 = 50, L2 = 46) {
    const x = side * (hx - sx), y = hy - sy; let d = Math.hypot(x, y); d = Math.max(8, Math.min(L1 + L2 - .5, d));
    const ad = Math.atan2(x, y), al = Math.acos((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)), ga = Math.acos((L1 * L1 + L2 * L2 - d * d) / (2 * L1 * L2));
    const sol = e => [ad + e * al, -e * (Math.PI - ga)];
    if (el === 'in' || el === 'out' || el == null) {   // automatisch: Ellbogen nach aussen (weg von der Koerpermitte)
      const A = sol(1), B = sol(-1), ex = a => sx + side * Math.sin(a[0]) * L1;
      const pa = Math.abs(ex(A) - 100), pb = Math.abs(ex(B) - 100);
      return (el === 'in') === (pa > pb) ? B : A;
    }
    return sol(el);
  }
  function leg(x, y, a, L = 92) {
    const fx = x + Math.sin(a) * L, fy = y + Math.cos(a) * L;
    return `<path d="M${x},${y} L${fx.toFixed(1)},${fy.toFixed(1)}" stroke="${OL}" stroke-width="34" stroke-linecap="round"/><path d="M${x},${y} L${fx.toFixed(1)},${fy.toFixed(1)}" stroke="${PA}" stroke-width="25" stroke-linecap="round"/>` +
      `<path d="M${(x + 6)},${y + 8} L${(fx + 6).toFixed(1)},${(fy - 6).toFixed(1)}" stroke="${PAD}" stroke-width="6" stroke-linecap="round" opacity=".5"/>` +
      `<ellipse cx="${(fx + 7).toFixed(1)}" cy="${(fy + 6).toFixed(1)}" rx="21" ry="11" fill="${SH}" stroke="${OL}" stroke-width="5"/>`;
  }
  function mouth(kind, open, cx, cy) {
    const s = `stroke="${OL}" stroke-width="5" stroke-linecap="round" fill="none"`;
    const o = Math.max(0, Math.min(1, open || 0));
    if (o > .08 && kind !== 'o') { // sprechen / lachen: offener D-Mund
      const w = kind === 'grin' ? 17 : 13, h = 4 + 15 * o;
      return `<path d="M${cx - w},${cy - 2} Q${cx},${cy + 3} ${cx + w},${cy - 2} Q${cx + w * .6},${cy + h} ${cx},${cy + h} Q${cx - w * .6},${cy + h} ${cx - w},${cy - 2} Z" fill="#7a2a2a" stroke="${OL}" stroke-width="4.5" stroke-linejoin="round"/>` +
        `<ellipse cx="${cx}" cy="${cy + h * .72}" rx="${w * .45}" ry="${h * .22}" fill="#e5767a"/>`;
    }
    switch (kind) {
      case 'grin': return `<path d="M${cx - 17},${cy - 4} Q${cx},${cy + 14} ${cx + 17},${cy - 4}" ${s}/>`;
      case 'smile': return `<path d="M${cx - 13},${cy - 2} Q${cx},${cy + 9} ${cx + 13},${cy - 2}" ${s}/>`;
      case 'sad': return `<path d="M${cx - 11},${cy + 5} Q${cx},${cy - 5} ${cx + 11},${cy + 5}" ${s}/>`;
      case 'o': return `<ellipse cx="${cx}" cy="${cy + 3}" rx="${6 + 3 * o}" ry="${8 + 4 * o}" fill="#7a2a2a" stroke="${OL}" stroke-width="4.5"/>`;
      case 'hmm': return `<path d="M${cx - 10},${cy + 2} L${cx + 11},${cy - 2}" ${s}/>`;
      default: return `<path d="M${cx - 11},${cy + 1} L${cx + 11},${cy + 1}" ${s}/>`;
    }
  }
  // o: {armL:[a,b], armR:[a,b], legL, legR, mouth, talk(0..1), blink(0..1), look:[dx,dy], tilt(rad), bob(px), ghost, prop:{svg} in rechter Hand}
  function svg(o = {}) {
    const bob = o.bob || 0, tilt = (o.tilt || 0) * 57.3;
    const aL = o.hL ? ik(64, 160, -1, o.hL[0], o.hL[1], o.elL2 == null ? 'out' : o.elL2) : (o.armL || [.15, .15]);
    const aR = o.hR ? ik(136, 160, 1, o.hR[0], o.hR[1], o.elR2 == null ? 'out' : o.elR2) : (o.armR || [.15, .15]);
    let g = '';
    g += `<ellipse cx="100" cy="342" rx="${62 - Math.min(20, Math.abs(bob) * .4)}" ry="11" fill="#000" opacity="${o.ghost ? .08 : .22}"/>`;
    g += `<g transform="translate(0,${-bob}) rotate(${((o.lean || 0) * 57.3).toFixed(2)},100,340)">`;
    if (o.back) g += o.back;
    g += leg(84, 228, o.legL || 0) + leg(116, 228, o.legR || 0);
    // Pullover
    g += `<path d="M58,152 Q100,132 142,152 L150,236 Q100,250 50,236 Z" fill="${SW}" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/>`;
    g += `<path d="M54,224 Q100,238 146,224" stroke="${SWD}" stroke-width="7" fill="none" opacity=".7"/><path d="M80,152 Q100,166 120,152" stroke="${SWD}" stroke-width="6" fill="none"/>`;
    const L = arm(64, 160, -1, aL[0], aL[1]), R = arm(136, 160, 1, aR[0], aR[1]);
    if (o.legsOff) {}
    if (o.mid) g += o.mid;
    if (o.propL) g += `<g transform="translate(${L.hx.toFixed(1)},${L.hy.toFixed(1)})">${o.propL}</g>`;
    if (!o.lFront) g += L.svg;
    if (o.armsBack) g += R.svg;
    // Kopf
    const lx = (o.look || [0, 0])[0], ly = (o.look || [0, 0])[1];
    g += `<g transform="rotate(${tilt.toFixed(2)},100,140)">`;
    if (o.hood) g += o.hood;
    if (o.square) {   // Squarehead: eckiger Kopf mit runden Kanten
      g += `<rect x="38" y="24" width="124" height="124" rx="24" fill="${SK}" stroke="${OL}" stroke-width="6"/>`;
      g += `<path d="M41,120 Q100,134 159,120 L159,124 Q159,145 138,145 L62,145 Q41,145 41,124 Z" fill="${SKD}" opacity=".85"/>`;
    } else {
    g += `<circle cx="100" cy="86" r="64" fill="${SK}" stroke="${OL}" stroke-width="6"/>`;
    g += `<path d="M48,108 A64,64 0 0,0 150,122 A70,70 0 0,1 48,108 Z" fill="${SKD}" opacity=".85"/>`;
    }
    g += `<ellipse cx="78" cy="56" rx="16" ry="10" fill="#fff" opacity=".45" transform="rotate(-30,78,56)"/>`;
    const bl = 1 - Math.max(0, Math.min(1, o.blink || 0)) * .9;
    if (o.ghost) g += `<text x="100" y="112" text-anchor="middle" font-family="Inter,Arial" font-weight="900" font-size="78" fill="${OL}" opacity=".55">?</text>`;
    else {
      g += `<ellipse cx="${84 + lx}" cy="${86 + ly}" rx="6.5" ry="${(7.5 * bl).toFixed(2)}" fill="${OL}"/><ellipse cx="${118 + lx}" cy="${86 + ly}" rx="6.5" ry="${(7.5 * bl).toFixed(2)}" fill="${OL}"/>`;
      g += mouth(o.mouth || 'smile', o.talk, 101 + lx * .6, 112 + ly * .5);
    }
    if (o.hat) g += o.hat;
    g += `</g>`;
    if (o.prop) g += `<g transform="translate(${R.hx.toFixed(1)},${R.hy.toFixed(1)})">${o.prop}</g>`;
    if (!o.armsBack) g += R.svg;
    if (o.lFront) g += L.svg;
    if (o.front) g += o.front;
    if (o.claw) { const cl = (x, y, sd, op) => `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${sd},1) rotate(${-20 - 25 * op})"><path d="M-4,6 C-30,8 -34,-30 -10,-40 C-4,-30 -8,-18 2,-12 Z" fill="${o.claw}" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/></g>` +
      `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${sd},1) rotate(${10 + 20 * op})"><path d="M-4,4 C-26,14 -40,-10 -24,-26 C-18,-14 -10,-6 2,-4 Z" fill="${o.claw}" stroke="${OL}" stroke-width="5" stroke-linejoin="round"/></g>` +
      `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="14" fill="${o.claw}" stroke="${OL}" stroke-width="5"/>`;
      const op = o.clawOpen || 0; g += cl(L.hx, L.hy, 1, op) + cl(R.hx, R.hy, -1, op) }
    g += `</g>`;
    if (o.sw) g = g.split(SW).join(o.sw).split(SWD).join(o.swd || o.sw);
    if (o.pa) g = g.split(PA).join(o.pa);
    const ghost = o.ghost ? ` opacity="${o.ghostA == null ? .8 : o.ghostA}" style="filter:grayscale(1) brightness(1.9)"` : '';
    return `<svg viewBox="-20 -10 240 365" width="${o.w || 240}" height="${(o.w || 240) * 365 / 240}" style="overflow:visible"${ghost}>${g}</svg>`;
  }
  // Mund-Oeffnung aus Wortzeiten (Lippen-Flattern beim Sprechen)
  function talk(t, line) {
    if (!line || !line.words) return 0;
    const rt = t - line.start;
    for (const w of line.words) if (rt >= w[1] && rt <= w[2]) { const u = (rt - w[1]) / Math.max(.05, w[2] - w[1]); return Math.abs(Math.sin(u * Math.PI * Math.max(1, Math.round((w[2] - w[1]) / .13)))) }
    return 0;
  }
  const blink = t => { const p = (t + .7) % 3.3; return p < .14 ? Math.sin(p / .14 * Math.PI) : 0 };
  window.MG_SAM = { svg, talk, blink, ik };
})();
