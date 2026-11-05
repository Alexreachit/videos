// GL3D: kleine deterministische WebGL2-Engine fuer Low-Poly-3D-Welten (Roundhead Island u. a.).
// Flat Shading ueber Ableitungen (keine Normalen noetig), Sonnen-Schatten (Shadow Map + PCF), Himmel-/Boden-Licht,
// Nebel zum Horizont, Wasser-Wellen im Vertex-Shader, Schaum-Ring, optionale Canvas-Texturen, Transparenz (Hologramme).
// Alles aus t berechnet -> parallel renderbar. Nutzung: siehe mg/ri01/scene.html.
(function () {
  const G = {};
  // ---------- Mathe (Spalten-Matrizen wie WebGL) ----------
  const m4 = {
    id: () => [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1],
    mul(a, b) { const o = new Array(16); for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) { let s = 0; for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k]; o[c * 4 + r] = s } return o },
    persp(fov, asp, n, f) { const t = 1 / Math.tan(fov / 2); return [t / asp,0,0,0, 0,t,0,0, 0,0,(f + n) / (n - f),-1, 0,0,2 * f * n / (n - f),0] },
    ortho(l, r, b, t, n, f) { return [2/(r-l),0,0,0, 0,2/(t-b),0,0, 0,0,-2/(f-n),0, -(r+l)/(r-l),-(t+b)/(t-b),-(f+n)/(f-n),1] },
    look(e, c, u = [0, 1, 0]) {
      let z = norm(sub(e, c)), x = norm(cross(u, z)), y = cross(z, x);
      return [x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0, -dot(x,e),-dot(y,e),-dot(z,e),1];
    },
    // T * Ry * Rx * Rz * S
    compose(p = [0,0,0], r = [0,0,0], s = [1,1,1]) {
      const [rx, ry, rz] = r, cx = Math.cos(rx), sx = Math.sin(rx), cy = Math.cos(ry), sy = Math.sin(ry), cz = Math.cos(rz), sz = Math.sin(rz);
      const Ry = [cy,0,-sy,0, 0,1,0,0, sy,0,cy,0, 0,0,0,1], Rx = [1,0,0,0, 0,cx,sx,0, 0,-sx,cx,0, 0,0,0,1], Rz = [cz,sz,0,0, -sz,cz,0,0, 0,0,1,0, 0,0,0,1];
      const a = m4.mul(m4.mul(Ry, Rx), Rz);
      const S = Array.isArray(s) ? s : [s, s, s];
      for (let i = 0; i < 3; i++) { a[i] *= S[0]; a[4 + i] *= S[1]; a[8 + i] *= S[2] }
      a[12] = p[0]; a[13] = p[1]; a[14] = p[2]; return a;
    },
    xf(m, v) { const x = v[0], y = v[1], z = v[2]; const w = m[3]*x + m[7]*y + m[11]*z + m[15]; return [(m[0]*x + m[4]*y + m[8]*z + m[12]) / w, (m[1]*x + m[5]*y + m[9]*z + m[13]) / w, (m[2]*x + m[6]*y + m[10]*z + m[14]) / w, w] }
  };
  const sub = (a, b) => [a[0]-b[0], a[1]-b[1], a[2]-b[2]], dot = (a, b) => a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
  const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
  const norm = a => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0]/l, a[1]/l, a[2]/l] };
  G.m4 = m4; G.v = { sub, dot, cross, norm, lerp: (a, b, t) => a.map((x, i) => x + (b[i] - x) * t) };
  G.hex = h => { const n = parseInt(h.replace('#', ''), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255] };
  const hash = (a, b = 0, c = 0) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x) };
  G.hash = hash;

  // ---------- Geometrie-Bauer: Dreiecks-Listen {p:[], c:[], uv:[]} ----------
  function Geo() { this.p = []; this.c = []; this.uv = []; this.n = [] }
  Geo.prototype.tri = function (a, b, c, col, ua, ub, uc) {
    this.p.push(...a, ...b, ...c); this.c.push(...col, ...col, ...col);
    const fn = norm(cross(sub(b, a), sub(c, a))); this.n.push(...fn, ...fn, ...fn);
    this.uv.push(...(ua || [0, 0]), ...(ub || [0, 0]), ...(uc || [0, 0])); return this;
  };
  Geo.prototype.quad = function (a, b, c, d, col, uvs) { this.tri(a, b, c, col, uvs && uvs[0], uvs && uvs[1], uvs && uvs[2]); return this.tri(a, c, d, col, uvs && uvs[0], uvs && uvs[2], uvs && uvs[3]) };
  Geo.prototype.add = function (g, m) {
    for (let i = 0; i < g.p.length; i += 3) { const v = m ? m4.xf(m, [g.p[i], g.p[i+1], g.p[i+2]]) : [g.p[i], g.p[i+1], g.p[i+2]]; this.p.push(v[0], v[1], v[2]);
      let nx = g.n[i], ny = g.n[i+1], nz = g.n[i+2]; if (m) { const a = m[0]*nx + m[4]*ny + m[8]*nz, b = m[1]*nx + m[5]*ny + m[9]*nz, c = m[2]*nx + m[6]*ny + m[10]*nz; const q = norm([a, b, c]); nx = q[0]; ny = q[1]; nz = q[2] } this.n.push(nx, ny, nz) }
    this.c.push(...g.c); this.uv.push(...g.uv); return this;
  };
  // Farbe je Dreieck leicht variieren (wirkt lebendiger)
  Geo.prototype.vary = function (amt = .06, seed = 1) {
    for (let i = 0; i < this.c.length; i += 9) { const k = 1 + (hash(i, seed) - .5) * 2 * amt; for (let j = 0; j < 9; j++) this.c[i + j] = Math.min(1, this.c[i + j] * k) } return this;
  };
  Geo.prototype.smooth = function (q = 1000) {
    const acc = {}, key = i => Math.round(this.p[i] * q) + ',' + Math.round(this.p[i+1] * q) + ',' + Math.round(this.p[i+2] * q);
    for (let i = 0; i < this.p.length; i += 3) { const k = key(i); const a = acc[k] || (acc[k] = [0, 0, 0]); a[0] += this.n[i]; a[1] += this.n[i+1]; a[2] += this.n[i+2] }
    for (let i = 0; i < this.p.length; i += 3) { const a = norm(acc[key(i)]); this.n[i] = a[0]; this.n[i+1] = a[1]; this.n[i+2] = a[2] }
    this.smoothed = true; return this;
  };
  G.Geo = Geo;
  const C = c => typeof c === 'string' ? G.hex(c) : c;

  G.box = (w, h, d, col, o = {}) => {
    const g = new Geo(), x = w / 2, z = d / 2, y0 = o.base ? 0 : -h / 2, y1 = y0 + h, k = C(col), top = o.top ? C(o.top) : k;
    const P = [[-x,y0,-z],[x,y0,-z],[x,y1,-z],[-x,y1,-z],[-x,y0,z],[x,y0,z],[x,y1,z],[-x,y1,z]];
    const F = [[4,5,6,7],[1,0,3,2],[5,1,2,6],[0,4,7,3],[7,6,2,3],[0,1,5,4]];
    F.forEach((f, i) => g.quad(P[f[0]], P[f[1]], P[f[2]], P[f[3]], i == 4 ? top : k, i == 0 && o.uvFront ? [[0,1],[1,1],[1,0],[0,0]] : null));
    return g;
  };
  // Zylinder/Kegel (rTop=0 -> Kegel), Basis auf y=0
  G.cyl = (rb, rt, h, seg, col, o = {}) => {
    const g = new Geo(), k = C(col), cap = o.cap ? C(o.cap) : k;
    for (let i = 0; i < seg; i++) {
      const a0 = i / seg * 6.2832 + (o.rot || 0), a1 = (i + 1) / seg * 6.2832 + (o.rot || 0);
      const b0 = [Math.cos(a0) * rb, 0, Math.sin(a0) * rb], b1 = [Math.cos(a1) * rb, 0, Math.sin(a1) * rb];
      const t0 = [Math.cos(a0) * rt, h, Math.sin(a0) * rt], t1 = [Math.cos(a1) * rt, h, Math.sin(a1) * rt];
      if (rt > 0) g.quad(b0, t0, t1, b1, k); else g.tri(b0, [0, h, 0], b1, k);
      if (rt > 0) g.tri([0, h, 0], t1, t0, cap);
      if (!o.open) g.tri([0, 0, 0], b0, b1, k);
    }
    return g;
  };
  // Ikosaeder-Kugel, jit = Zufallsverformung (Felsen, Wolken, Kokosnuss)
  G.ico = (r, det, col, jit = 0, seed = 1, sy = 1) => {
    const t = (1 + Math.sqrt(5)) / 2;
    let V = [[-1,t,0],[1,t,0],[-1,-t,0],[1,-t,0],[0,-1,t],[0,1,t],[0,-1,-t],[0,1,-t],[t,0,-1],[t,0,1],[-t,0,-1],[-t,0,1]].map(norm);
    let F = [[0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],[1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],[3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],[4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]];
    for (let d = 0; d < det; d++) {
      const cache = {}, mid = (a, b) => { const key = a < b ? a + '_' + b : b + '_' + a; if (cache[key] == null) { V.push(norm(V[a].map((x, i) => (x + V[b][i]) / 2))); cache[key] = V.length - 1 } return cache[key] };
      const NF = []; F.forEach(([a, b, c]) => { const ab = mid(a, b), bc = mid(b, c), ca = mid(c, a); NF.push([a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]) }); F = NF;
    }
    const P = V.map((v, i) => { const k = r * (1 + (hash(i, seed) - .5) * 2 * jit); return [v[0] * k, v[1] * k * sy, v[2] * k] });
    const g = new Geo(), k = C(col); F.forEach(f => g.tri(P[f[0]], P[f[1]], P[f[2]], k)); return g;
  };
  // flaches Rechteck (fuer Texturen: Flagge, Schild), in XY-Ebene, Mitte links (ax=0) oder zentriert
  G.plane = (w, h, nx, ny, col, o = {}) => {
    const g = new Geo(), k = C(col), x0 = o.left ? 0 : -w / 2;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const u0 = i / nx, u1 = (i + 1) / nx, v0 = j / ny, v1 = (j + 1) / ny;
      const P = (u, v) => [x0 + u * w, (v - .5) * h, 0];
      g.quad(P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1), k, [[u0, 1 - v0], [u1, 1 - v0], [u1, 1 - v1], [u0, 1 - v1]]);
    }
    return g;
  };
  // Palmblatt: gebogener Streifen mit Mittelfalte
  G.leaf = (len, wid, droop, col, seg = 6) => {
    const g = new Geo(), k = C(col), k2 = k.map(x => x * .82);
    for (let i = 0; i < seg; i++) {
      const f = (s) => { const u = s / seg, w = wid * Math.sin(Math.PI * Math.min(1, u * 1.15 + .08)) * (1 - u * .3); return { x: u * len, y: -droop * u * u * len + .25 * u * len * (1 - u), w } };
      const a = f(i), b = f(i + 1);
      const ca = [a.x, a.y + .05, 0], cb = [b.x, b.y + .05, 0];
      g.quad(ca, cb, [b.x, b.y - .06 * b.w, b.w], [a.x, a.y - .06 * a.w, a.w], k);
      g.quad(ca, [a.x, a.y - .06 * a.w, -a.w], [b.x, b.y - .06 * b.w, -b.w], cb, k2);
    }
    return g;
  };

  // ---------- Renderer ----------
  const VS = `#version 300 es
in vec3 aP; in vec3 aC; in vec2 aU; in vec3 aN;
uniform mat4 uM,uVP,uLVP; uniform float uT,uWave;
out vec3 vW; out vec3 vC; out vec4 vL; out vec2 vU; out vec3 vN;
void main(){ vec4 w=uM*vec4(aP,1.); vN=normalize(mat3(uM)*aN);
 if(uWave>0.){ float x=w.x,z=w.z;
   w.y+=uWave*(sin(x*.33+uT*1.7)*.5+sin(z*.41-uT*1.25)*.45+sin((x-z)*.9+uT*2.3)*.18+sin(x*1.7+z*1.3+uT*3.1)*.06);
   float dx=uWave*(cos(x*.33+uT*1.7)*.165+cos((x-z)*.9+uT*2.3)*.162+cos(x*1.7+z*1.3+uT*3.1)*.102);
   float dz=uWave*(cos(z*.41-uT*1.25)*.1845-cos((x-z)*.9+uT*2.3)*.162+cos(x*1.7+z*1.3+uT*3.1)*.078);
   vN=normalize(vec3(-dx,1.,-dz)); }
 vW=w.xyz; vC=aC; vU=aU; vL=uLVP*w; gl_Position=uVP*w; }`;
  const FS = `#version 300 es
precision highp float; precision highp sampler2DShadow;
in vec3 vW; in vec3 vC; in vec4 vL; in vec2 vU; in vec3 vN;
uniform vec3 uSun,uSunCol,uSky,uGnd,uFog,uCam,uTint; uniform float uFogN,uFogF,uAlpha,uEmis,uTintA,uFoamR,uT,uUseTex,uShade,uRecv,uSmooth,uTerrain,uWater,uSpec;
uniform sampler2DShadow uSh; uniform sampler2D uTex;
out vec4 o;
float shadow(){ vec3 p=vL.xyz/vL.w*.5+.5; if(p.x<0.||p.x>1.||p.y<0.||p.y>1.||p.z>1.) return 1.; float s=0.; vec2 tx=vec2(1./2048.);
 for(int x=-1;x<=1;x++) for(int y=-1;y<=1;y++) s+=texture(uSh,vec3(p.xy+vec2(x,y)*tx*2.2,p.z-.0015)); return s/9.; }
float h21(vec2 p){ p=fract(p*vec2(123.34,456.21)); p+=dot(p,p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i=floor(p),f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h21(i),h21(i+vec2(1,0)),f.x),mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x),f.y); }
float fbm(vec2 p){ float a=.5,s=0.; for(int i=0;i<3;i++){ s+=a*vn(p); p*=2.03; a*=.5; } return s; }
void main(){
 vec3 nf=normalize(cross(dFdx(vW),dFdy(vW))); vec3 n=uSmooth>.5?normalize(vN):nf; if(dot(nf,uCam-vW)<0.){ nf=-nf; if(uSmooth<.5) n=-n; }
 vec3 col=vC; if(uUseTex>.5){ vec4 tx=texture(uTex,vU); if(tx.a<.05) discard; col=mix(col,tx.rgb,tx.a);}
 if(uTerrain>.5){ float y=vW.y, nz=fbm(vW.xz*.35), nz2=fbm(vW.xz*2.2), sl=1.-n.y;
   vec3 g1=vec3(.36,.68,.27), g2=vec3(.47,.76,.30), g3=vec3(.30,.58,.22);
   vec3 grass=mix(mix(g1,g2,smoothstep(.35,.7,nz)),g3,smoothstep(.55,.85,nz2)*.5);
   grass*=.94+.12*vn(vW.xz*5.);
   vec3 sand=mix(vec3(.93,.83,.6),vec3(.97,.89,.68),nz2)*(.95+.08*vn(vW.xz*14.));
   vec3 wet=vec3(.78,.66,.45);
   float gs=smoothstep(.5+.25*nz,.85+.25*nz,y);
   col=mix(mix(wet,sand,smoothstep(-.15,.25,y)),grass,gs);
   col=mix(col,col*.82,smoothstep(.25,.6,sl)); }
 col=mix(col,uTint,uTintA);
 float sh=uRecv>.5?shadow():1.;
 float d=max(dot(n,uSun),0.);
 vec3 amb=mix(uGnd,uSky,n.y*.5+.5);
 vec3 c=col*(amb*.62+uSunCol*d*mix(.35,1.,sh)*.72);
 vec3 V=normalize(uCam-vW), Hh=normalize(V+uSun);
 if(uSpec>0.) c+=uSunCol*pow(max(dot(n,Hh),0.),40.)*uSpec*sh;
 if(uWater>.5){ float fr=pow(1.-max(dot(n,V),0.),3.); c=mix(c,uSky*1.05,fr*.55); c+=uSunCol*pow(max(dot(n,Hh),0.),180.)*1.4*sh; }
 c=mix(col,c,uShade)+col*uEmis;
 if(uFoamR>0.){ float r=length(vW.xz);
   float shallow=smoothstep(uFoamR+9.,uFoamR+.5,r); c=mix(c,c*vec3(.75,1.25,1.12)+vec3(.05,.12,.1),shallow*.85);
   float ring=uFoamR+.35+.25*sin(uT*1.4+atan(vW.z,vW.x)*5.);
   float f=smoothstep(.55,0.,abs(r-ring))+smoothstep(uFoamR+.2,uFoamR-.3,r); c=mix(c,vec3(.97,.99,1.),clamp(f,0.,1.)*.85); }
 float fg=smoothstep(uFogN,uFogF,length(vW-uCam)); c=mix(c,uFog,fg);
 o=vec4(c,uAlpha); }`;
  const SVS = `#version 300 es
in vec3 aP; uniform mat4 uM,uLVP; void main(){ gl_Position=uLVP*uM*vec4(aP,1.); }`;
  const SFS = `#version 300 es
precision mediump float; out vec4 o; void main(){ o=vec4(1.); }`;

  function prog(gl, vs, fs) {
    const p = gl.createProgram();
    [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]].forEach(([t, s]) => { const sh = gl.createShader(t); gl.shaderSource(sh, s); gl.compileShader(sh); if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh)); gl.attachShader(p, sh) });
    gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    const U = {}; const n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS); for (let i = 0; i < n; i++) { const nm = gl.getActiveUniform(p, i).name; U[nm] = gl.getUniformLocation(p, nm) }
    return { p, U };
  }

  G.World = function (canvas, W, H, SS = 1) {
    const gl = canvas.getContext('webgl2', { antialias: SS < 1.3, alpha: true, premultipliedAlpha: false, preserveDrawingBuffer: true });
    if (!gl) throw new Error('kein WebGL2');
    canvas.width = Math.round(W * SS); canvas.height = Math.round(H * SS);
    const P = prog(gl, VS, FS), S = prog(gl, SVS, SFS);
    // Shadow map
    const SM = 2048, stex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, stex);
    gl.texStorage2D(gl.TEXTURE_2D, 1, gl.DEPTH_COMPONENT24, SM, SM);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_COMPARE_MODE, gl.COMPARE_REF_TO_TEXTURE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_COMPARE_FUNC, gl.LEQUAL);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    const fb = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fb); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.TEXTURE_2D, stex, 0); gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    const white = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, white); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([255, 255, 255, 255]));

    const w = {
      gl, W, H, objs: [],
      cam: { pos: [0, 5, 10], at: [0, 0, 0], fov: 50, roll: 0 },
      sun: norm([.45, .8, .35]), sunCol: G.hex('#fff1d6'), sky: G.hex('#cfe9ff'), gnd: G.hex('#b9a27a'), fog: G.hex('#bfe3f7'), fogN: 60, fogF: 220,
      shadowCenter: [0, 0, 0], shadowSize: 30, t: 0,
    };
    w.mesh = function (geo, o = {}) {
      const vao = gl.createVertexArray(); gl.bindVertexArray(vao);
      const mk = (arr, loc, n, dyn) => { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(arr), dyn ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, n, gl.FLOAT, false, 0, 0); return b };
      const lp = gl.getAttribLocation(P.p, 'aP'), lc = gl.getAttribLocation(P.p, 'aC'), lu = gl.getAttribLocation(P.p, 'aU'), ln = gl.getAttribLocation(P.p, 'aN');
      const bp = mk(geo.p, lp, 3, o.dynamic); mk(geo.c, lc, 3); mk(geo.uv, lu, 2); const bn = mk(geo.n.length ? geo.n : new Array(geo.p.length).fill(0), ln, 3, o.dynamic);
      gl.bindVertexArray(null);
      const ob = Object.assign({ vao, bp, bn, smooth: !!geo.smoothed, terrain: 0, water: 0, spec: 0, n: geo.p.length / 3, pos: [0, 0, 0], rot: [0, 0, 0], scl: [1, 1, 1], vis: true, alpha: 1, emis: 0, tint: [1, 1, 1], tintA: 0, wave: 0, foam: 0, cast: true, recv: true, shade: 1, tex: null, parent: null }, o);
      w.objs.push(ob); return ob;
    };
    w.update = function (ob, geo) { gl.bindBuffer(gl.ARRAY_BUFFER, ob.bp); gl.bufferSubData(gl.ARRAY_BUFFER, 0, new Float32Array(geo.p)); if (geo.n.length) { gl.bindBuffer(gl.ARRAY_BUFFER, ob.bn); gl.bufferSubData(gl.ARRAY_BUFFER, 0, new Float32Array(geo.n)) } };
    w.texture = function (cv) { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv); gl.generateMipmap(gl.TEXTURE_2D); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); return t };
    w.matrix = function (ob) { const l = m4.compose(ob.pos, ob.rot, ob.scl); return ob.parent ? m4.mul(w.matrix(ob.parent), l) : l };
    w.vp = function () {
      const c = w.cam, V = m4.look(c.pos, c.at, [Math.sin(c.roll || 0), Math.cos(c.roll || 0), 0]);
      return m4.mul(m4.persp(c.fov * Math.PI / 180, W / H, .1, 600), V);
    };
    // Weltpunkt -> Bildschirm {x,y,depth,scale(px pro Welteinheit)}
    w.project = function (p) {
      const VP = w.vp(), q = m4.xf(VP, p), f = 1 / Math.tan(w.cam.fov * Math.PI / 360);
      return { x: (q[0] * .5 + .5) * W, y: (1 - (q[1] * .5 + .5)) * H, z: q[3], s: f * H / 2 / q[3], vis: q[3] > .1 };
    };
    w.render = function (t) {
      w.t = t;
      const L = w.sun, sc = w.shadowCenter, R = w.shadowSize;
      const LV = m4.look([sc[0] + L[0] * 60, sc[1] + L[1] * 60, sc[2] + L[2] * 60], sc, [0, 1, 0]);
      const LVP = m4.mul(m4.ortho(-R, R, -R, R, 1, 160), LV);
      const list = w.objs.filter(o => o.vis && (!o.parent || o.parent.vis !== false) && o.alpha > .003);
      // Schatten-Pass
      gl.bindFramebuffer(gl.FRAMEBUFFER, fb); gl.viewport(0, 0, SM, SM); gl.clear(gl.DEPTH_BUFFER_BIT); gl.enable(gl.DEPTH_TEST); gl.disable(gl.BLEND);
      gl.useProgram(S.p); gl.uniformMatrix4fv(S.U.uLVP, false, LVP);
      gl.enable(gl.POLYGON_OFFSET_FILL); gl.polygonOffset(2, 4);
      for (const o of list) if (o.cast && o.alpha >= 1) { gl.uniformMatrix4fv(S.U.uM, false, w.matrix(o)); gl.bindVertexArray(o.vao); gl.drawArrays(gl.TRIANGLES, 0, o.n) }
      gl.disable(gl.POLYGON_OFFSET_FILL);
      // Haupt-Pass
      gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, canvas.width, canvas.height); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.useProgram(P.p); const U = P.U;
      gl.uniformMatrix4fv(U.uVP, false, w.vp()); gl.uniformMatrix4fv(U.uLVP, false, LVP);
      gl.uniform3fv(U.uSun, L); gl.uniform3fv(U.uSunCol, w.sunCol); gl.uniform3fv(U.uSky, w.sky); gl.uniform3fv(U.uGnd, w.gnd); gl.uniform3fv(U.uFog, w.fog); gl.uniform3fv(U.uCam, w.cam.pos);
      gl.uniform1f(U.uFogN, w.fogN); gl.uniform1f(U.uFogF, w.fogF); gl.uniform1f(U.uT, t);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, stex); gl.uniform1i(U.uSh, 0);
      gl.uniform1i(U.uTex, 1);
      const draw = o => {
        gl.uniformMatrix4fv(U.uM, false, w.matrix(o)); gl.uniform1f(U.uWave, o.wave); gl.uniform1f(U.uFoamR, o.foam);
        gl.uniform1f(U.uAlpha, o.alpha); gl.uniform1f(U.uEmis, o.emis); gl.uniform3fv(U.uTint, o.tint); gl.uniform1f(U.uTintA, o.tintA);
        gl.uniform1f(U.uShade, o.shade); gl.uniform1f(U.uRecv, o.recv ? 1 : 0);
        gl.uniform1f(U.uSmooth, (o.smooth || o.wave > 0) ? 1 : 0); gl.uniform1f(U.uTerrain, o.terrain); gl.uniform1f(U.uWater, o.water || (o.wave > 0 ? 1 : 0)); gl.uniform1f(U.uSpec, o.spec);
        gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, o.tex || white); gl.uniform1f(U.uUseTex, o.tex ? 1 : 0);
        gl.bindVertexArray(o.vao); gl.drawArrays(gl.TRIANGLES, 0, o.n);
      };
      gl.disable(gl.BLEND); gl.depthMask(true);
      for (const o of list) if (o.alpha >= 1) draw(o);
      gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false);
      for (const o of list) if (o.alpha < 1) { if (o.additive) gl.blendFunc(gl.SRC_ALPHA, gl.ONE); else gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); draw(o) }
      gl.depthMask(true); gl.disable(gl.BLEND);
    };
    return w;
  };
  window.GL3D = G;
})();
