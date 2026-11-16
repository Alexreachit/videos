# Bis zum Erdkern – Tag 1, realistische Umgebung (Cycles). Texturen: Poly Haven (CC0), Erde: NASA Blue Marble (gemeinfrei).
# blender -b --factory-startup -P mg/erd03/scene.py -- <OUT> stills=30,200 [samples=32 pct=100 grass=40000] | frames=a-b
import bpy, sys, os, math, random
from mathutils import Vector, Matrix, Quaternion
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shared as SH
TEX = os.path.join(HERE, "..", "erd", "tex")
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/out"]
OUT = ARGS[0]; os.makedirs(OUT, exist_ok=True)
OPT = dict(a.split("=", 1) for a in ARGS[1:] if "=" in a)
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene; FPS = SH.FPS
S.render.fps = FPS; S.frame_start = 0; S.frame_end = SH.NF - 1
F = lambda t: int(round(t * FPS))
rnd = random.Random(7)

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple([(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c] + [a])
def link(o): S.collection.objects.link(o); return o
def newmat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; return m, m.node_tree, m.node_tree.nodes["Principled BSDF"]
def pbr(name, col, rough=.5, metal=0., sss=0., coat=0., emis=None, es=0.):
    m, nt, b = newmat(name); b.inputs["Base Color"].default_value = hexc(col); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if sss: b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1., .4, .25); b.inputs["Subsurface Scale"].default_value = .02
    if coat: b.inputs["Coat Weight"].default_value = coat
    if emis: b.inputs["Emission Color"].default_value = hexc(emis); b.inputs["Emission Strength"].default_value = es
    return m
def img(nt, name, colorspace="sRGB"):
    n = nt.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(os.path.join(TEX, name)); n.image.colorspace_settings.name = colorspace; return n
def texmat(name, key, scale=.4, tint=None, bump=1.0, worldcoords=True, rough_mul=1.0):
    """PBR-Material aus Poly-Haven-Satz (diff/nor_gl/rough), Projektion ueber Welt-XY (Draufsicht) oder Box"""
    m, nt, b = newmat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (scale, scale, scale)
    if worldcoords:
        geo = nt.nodes.new("ShaderNodeNewGeometry"); nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])
    else: nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    D = img(nt, f"{key}_diff.jpg"); N = img(nt, f"{key}_nor_gl.jpg", "Non-Color"); Rr = img(nt, f"{key}_rough.jpg", "Non-Color")
    for n in (D, N, Rr):
        n.projection = 'BOX' if not worldcoords else 'FLAT'; n.projection_blend = .3; nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    if tint:
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs["Factor"].default_value = 1.
        nt.links.new(D.outputs["Color"], mx.inputs[6]); mx.inputs[7].default_value = hexc(tint); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    else: nt.links.new(D.outputs["Color"], b.inputs["Base Color"])
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = bump; nt.links.new(N.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    if rough_mul != 1.0:
        mm = nt.nodes.new("ShaderNodeMath"); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = rough_mul; nt.links.new(Rr.outputs["Color"], mm.inputs[0]); nt.links.new(mm.outputs[0], b.inputs["Roughness"])
    else: nt.links.new(Rr.outputs["Color"], b.inputs["Roughness"])
    return m, nt, b, mp, D

def prim(kind, loc=(0, 0, 0), scl=(1, 1, 1), rot=(0, 0, 0), m=None, **kw):
    getattr(bpy.ops.mesh, "primitive_" + kind + "_add")(location=loc, rotation=rot, **kw); o = bpy.context.active_object; o.scale = scl
    if m: o.data.materials.append(m)
    return o
def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
    return o
def bevel(o, w=.02, seg=3):
    b = o.modifiers.new("bev", "BEVEL"); b.width = w; b.segments = seg; b.limit_method = 'ANGLE'; return o
def parent(o, p): o.parent = p; o.matrix_parent_inverse = p.matrix_world.inverted(); return o
def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); link(e); e.location = loc; return e

# ======================================================= WELT: HDRI-Himmel <-> Sternenhimmel (All)
WD = bpy.data.worlds.new("w"); S.world = WD; WD.use_nodes = True; wt = WD.node_tree; wt.nodes.clear()
env = wt.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(os.path.join(TEX, "sky.hdr"))
wmap = wt.nodes.new("ShaderNodeMapping"); wtc = wt.nodes.new("ShaderNodeTexCoord"); wmap.inputs["Rotation"].default_value = (0, 0, math.radians(110))
wt.links.new(wtc.outputs["Generated"], wmap.inputs["Vector"]); wt.links.new(wmap.outputs["Vector"], env.inputs["Vector"])
bg1 = wt.nodes.new("ShaderNodeBackground"); bg1.inputs["Strength"].default_value = 1.0; wt.links.new(env.outputs["Color"], bg1.inputs["Color"])
vor = wt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 420; vor.feature = 'F1'
wt.links.new(wtc.outputs["Generated"], vor.inputs["Vector"])
ramp = wt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
ramp.color_ramp.elements[1].position = .035; ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
wt.links.new(vor.outputs["Distance"], ramp.inputs["Fac"])
mx0 = wt.nodes.new("ShaderNodeMix"); mx0.data_type = 'RGBA'; mx0.inputs["Factor"].default_value = 1.0; mx0.inputs[6].default_value = hexc("#020511"); wt.links.new(ramp.outputs["Color"], mx0.inputs[7])
bg2 = wt.nodes.new("ShaderNodeBackground"); bg2.inputs["Strength"].default_value = 1.2; wt.links.new(mx0.outputs[2], bg2.inputs["Color"])
wmix = wt.nodes.new("ShaderNodeMixShader"); wt.links.new(bg1.outputs[0], wmix.inputs[1]); wt.links.new(bg2.outputs[0], wmix.inputs[2])
wout = wt.nodes.new("ShaderNodeOutputWorld"); wt.links.new(wmix.outputs[0], wout.inputs["Surface"])
def wkey(f, v): wmix.inputs[0].default_value = v; wmix.inputs[0].keyframe_insert("default_value", frame=f)
wkey(0, 0.); wkey(F(SH.T_SPACE) - 1, 0.); wkey(F(SH.T_SPACE), 1.); wkey(F(SH.T_BACK) - 1, 1.); wkey(F(SH.T_BACK), 0.)
for fc in WD.node_tree.animation_data.action.fcurves:
    for k in fc.keyframe_points: k.interpolation = 'CONSTANT'

sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 3.2; sun.angle = math.radians(1.2); sun.color = (1., .96, .9)
so = bpy.data.objects.new("sun", sun); link(so); so.rotation_mode = 'QUATERNION'; so.rotation_quaternion = Vector((-.45, -.6, .66)).normalized().to_track_quat('Z', 'Y')

# ======================================================= BODEN mit Loch
GRASS, gnt, gb, gmp, gD = texmat("grass", "aerial_grass_rock", scale=.45, bump=1.2, tint="#d8ffd0")
DIRT, *_ = texmat("dirt", "brown_mud_02", scale=.8, bump=1.4)
# Gras/Erde-Mischung im selben Material (Maske: Abstand zum Loch + Rauschen)
def ground_mat():
    m, nt, b, mp, D = texmat("ground", "aerial_grass_rock", scale=.45, bump=1.1, tint="#e6ffd8")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    D2 = img(nt, "brown_mud_02_diff.jpg"); mp2 = nt.nodes.new("ShaderNodeMapping"); mp2.inputs["Scale"].default_value = (.9, .9, .9); nt.links.new(geo.outputs["Position"], mp2.inputs["Vector"]); nt.links.new(mp2.outputs["Vector"], D2.inputs["Vector"])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sep.inputs[0])
    # Abstand zum Loch (0,0) und zum Erdhaufen
    vl = nt.nodes.new("ShaderNodeVectorMath"); vl.operation = 'LENGTH'
    cxy = nt.nodes.new("ShaderNodeCombineXYZ"); nt.links.new(sep.outputs[0], cxy.inputs[0]); nt.links.new(sep.outputs[1], cxy.inputs[1]); nt.links.new(cxy.outputs[0], vl.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.5; nz.inputs["Detail"].default_value = 8; nt.links.new(geo.outputs["Position"], nz.inputs["Vector"])
    ad = nt.nodes.new("ShaderNodeMath"); ad.operation = 'MULTIPLY_ADD'; ad.inputs[1].default_value = .45; nt.links.new(nz.outputs["Fac"], ad.inputs[0]); nt.links.new(vl.outputs["Value"], ad.inputs[2])
    rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["From Min"].default_value = .95; rr.inputs["From Max"].default_value = .78; nt.links.new(ad.outputs[0], rr.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; nt.links.new(rr.outputs["Result"], mx.inputs["Factor"])
    link_from = b.inputs["Base Color"].links[0].from_socket; nt.links.new(link_from, mx.inputs[6]); nt.links.new(D2.outputs["Color"], mx.inputs[7]); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    return m, rr
GROUND, GMASK = ground_mat()
# feines Gitter um das Loch (mit Mulde), dazu grosse Flaeche bis zum Horizont
bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=220, size=22, location=(0, 0, 0)); gr = bpy.context.active_object; gr.name = "near"
for v in gr.data.vertices:
    x, y = v.co.x, v.co.y; d = math.hypot(x, y)
    z = .025 * math.sin(x * 1.7 + 1) * math.cos(y * 1.3) + .012 * math.sin(x * 7.1) * math.sin(y * 6.3)
    if d < .62: z -= .2 * (math.cos(d / .62 * math.pi) * .5 + .5) ** 1.2         # Loch
    hd = math.hypot(x - .12, y - 1.18)
    if hd < .75: z += .3 * (math.cos(hd / .75 * math.pi) * .5 + .5) ** 1.4        # Erdhaufen
    edge = max(0., (max(abs(x), abs(y)) - 9) / 2); z -= edge * .03
    v.co.z = z
smooth(gr); gr.data.materials.append(GROUND)
far = prim("plane", (0, 0, -.06), (1, 1, 1), m=GROUND, size=900)
# sanfte Huegel weit hinten
for x, y, s, h in ((-60, 140, 70, 9), (40, 170, 90, 14), (130, 120, 60, 8), (-150, 110, 80, 11), (0, 230, 120, 18)):
    hl = prim("uv_sphere", (x, y, -h * .2), (s, s * .7, h), m=GROUND, segments=48, ring_count=24); smooth(hl)
# Haufen bekommt Erd-Material (eigene Kappe)
heap = prim("uv_sphere", (.12, 1.18, -.12), (.62, .55, .34), m=DIRT, segments=40, ring_count=20); smooth(heap)
hd_ = heap.modifiers.new("d", "DISPLACE"); tx = bpy.data.textures.new("clods", "CLOUDS"); tx.noise_scale = .12; hd_.texture = tx; hd_.strength = .08
# Steine verstreut
ROCK, *_ = texmat("rock", "gray_rocks", scale=1.6, worldcoords=False, bump=1.5)
for k in range(26):
    a = rnd.random() * 6.283; d = 1.3 + rnd.random() * 7
    if 4.2 < a < 5.3 and d < 4.5: continue                    # vor der Kamera frei lassen
    r = .04 + rnd.random() * .14
    st = prim("ico_sphere", (math.cos(a) * d, math.sin(a) * d, -r * .3), (r * (1 + rnd.random()), r, r * .7), (rnd.random(), rnd.random(), rnd.random()), m=ROCK, subdivisions=3)
    dm = st.modifiers.new("d", "DISPLACE"); t2 = bpy.data.textures.new("rk%d" % k, "VORONOI"); t2.noise_scale = .3; dm.texture = t2; dm.strength = r * .35
# Gras-Halme (Partikel) auf dem nahen Gitter, nicht im Loch/Haufen
if int(OPT.get("grass", 45000)) > 0:
    vg = gr.vertex_groups.new(name="dens")
    for v in gr.data.vertices:
        x, y = v.co.x, v.co.y; d = math.hypot(x, y); hd = math.hypot(x - .12, y - 1.18)
        wv = cl = max(0., min(1., (d - .8) / .5)) * max(0., min(1., (hd - .85) / .4))
        vg.add([v.index], wv, 'REPLACE')
    ps = gr.modifiers.new("gras", "PARTICLE_SYSTEM").particle_system; pst = ps.settings
    pst.type = 'HAIR'; pst.count = int(OPT.get("grass", 45000)); pst.use_advanced_hair = False; pst.hair_length = .09
    pst.child_type = 'INTERPOLATED'; pst.rendered_child_count = 6; pst.child_length = 1.0; pst.child_length_threshold = .3
    pst.roughness_2 = .04; pst.roughness_endpoint = .05
    pst.root_radius = .9; pst.tip_radius = .0; pst.radius_scale = .004
    ps.vertex_group_density = "dens"
    HM, hnt, hb = newmat("halm"); hi = hnt.nodes.new("ShaderNodeHairInfo"); hr = hnt.nodes.new("ShaderNodeValToRGB")
    hr.color_ramp.elements[0].color = hexc("#2c4a18"); hr.color_ramp.elements[1].color = hexc("#9cbf55"); hnt.links.new(hi.outputs["Intercept"], hr.inputs["Fac"]); hnt.links.new(hr.outputs["Color"], hb.inputs["Base Color"])
    hb.inputs["Roughness"].default_value = .55; hb.inputs["Subsurface Weight"].default_value = .1
    gr.data.materials.append(HM); pst.material = 2
# Baeume in der Ferne (Stamm + Blattwerk-Kugeln)
BARK = pbr("bark", "#4a3424", .85); LEAF = pbr("leaf", "#3d6b22", .7, sss=.15)
for k, (x, y) in enumerate(((-14, 22), (-9, 30), (11, 26), (17, 34), (-22, 40), (25, 21), (5, 44), (-30, 28), (30, 46), (-4, 52))):
    s = .9 + rnd.random() * .6; z = 0
    tr = prim("cylinder", (x, y, 2.2 * s), (.22 * s, .22 * s, 2.2 * s), m=BARK, vertices=12)
    for j in range(6):
        b = prim("ico_sphere", (x + rnd.uniform(-1.4, 1.4) * s, y + rnd.uniform(-1.2, 1.2) * s, (4.6 + rnd.uniform(-.5, 1.6)) * s), (1.6 * s, 1.6 * s, 1.4 * s), m=LEAF, subdivisions=3)
        dm = b.modifiers.new("d", "DISPLACE"); t3 = bpy.data.textures.new("lf%d_%d" % (k, j), "CLOUDS"); t3.noise_scale = .5; dm.texture = t3; dm.strength = .6; smooth(b)
# Schild "BIS ZUM ERDKERN"
WOOD = pbr("wood", "#8a5a34", .7); PAINT = pbr("paint", "#f4f1e8", .5)
for dx in (-.75, .75): prim("cylinder", (2.2 + dx, 1.9, .75), (.05, .05, .75), m=WOOD, vertices=10)
board = prim("cube", (2.2, 1.9, 1.25), (.95, .04, .36), m=WOOD); bevel(board, .015)
for row, (txt, z) in enumerate((("BIS ZUM", 1.39), ("ERDKERN", 1.08))):
    bpy.ops.object.text_add(location=(2.2, 1.855, z), rotation=(math.pi / 2, 0, 0)); tx_ = bpy.context.active_object; tx_.data.body = txt; tx_.data.align_x = 'CENTER'; tx_.data.size = .26; tx_.data.extrude = .006; tx_.data.materials.append(PAINT)
# Schubkarre-Ersatz: Eimer + Spitzhacke am Rand
MET = pbr("metal", "#8c9196", .35, metal=1.); prim("cylinder", (-1.6, .9, .16), (.17, .17, .16), m=MET, vertices=24)

# ======================================================= ARBEITER (stilisiert, realistische Materialien, ohne Gesicht)
SKIN = pbr("skin", "#c99a78", .55, sss=.2); VEST = pbr("vest", "#ff6a14", .6); STRIPE = pbr("stripe", "#d9dde0", .25, metal=.6)
SHIRT = pbr("shirt", "#2c4f86", .8); PANTS = pbr("pants", "#2f3540", .85); BOOT = pbr("boot", "#3a2a1c", .6); HAT = pbr("hat", "#ffcc1a", .28, coat=.6)
GLAS = pbr("glas", "#101418", .08, metal=.4); HANDLE_M = pbr("handle", "#9b6b3c", .6)
def ghost_mat():
    m, nt, b = newmat("ghost"); b.inputs["Base Color"].default_value = hexc("#dfe8ff"); b.inputs["Alpha"].default_value = .38
    b.inputs["Emission Color"].default_value = hexc("#cfe0ff"); b.inputs["Emission Strength"].default_value = .25; b.inputs["Roughness"].default_value = .3
    m.blend_method = 'BLEND' if hasattr(m, "blend_method") else None; return m
GHOSTM = ghost_mat()
def cyl_between(name, m, r=.05):
    o = prim("cylinder", m=m, vertices=16, radius=r, depth=1.0); smooth(o); o.name = name
    o.data.transform(Matrix.Translation((0, 0, .5)))            # Ursprung an einem Ende, Laenge 1 in +Z
    o.rotation_mode = 'QUATERNION'; return o
def build_worker(name, ghost=False):
    M = (lambda m: GHOSTM) if ghost else (lambda m: m)
    root = empty(name + "_root"); spine = empty(name + "_spine"); spine.parent = root; spine.location = (0, 0, SH.HIP); spine.rotation_mode = 'XYZ'
    parts = []
    def P(o, par=spine): o.parent = par; parts.append(o); return o
    # Beine (fest)
    for y in (.11, -.11):
        lg = prim("cylinder", (0, y, .48), (.075, .075, .46), m=M(PANTS), vertices=16); smooth(lg); P(lg, root)
        bt = prim("cube", (.05, y, .06), (.14, .065, .06), m=M(BOOT)); bevel(bt, .03); P(bt, root)
    hip = prim("cube", (0, 0, SH.HIP - .02), (.12, .17, .09), m=M(PANTS)); bevel(hip, .05); P(hip, root)
    # Oberkoerper (im Spine-Raum, Spine bei Huefthoehe)
    to = prim("cube", (0, 0, .3), (.13, .2, .3), m=M(SHIRT)); bevel(to, .09, 4); P(to)
    ve = prim("cube", (.005, 0, .3), (.137, .207, .25), m=M(VEST)); bevel(ve, .08, 4); P(ve)
    for z in (.2, .34): s_ = prim("cube", (.006, 0, z), (.139, .209, .018), m=M(STRIPE)); bevel(s_, .01); P(s_)
    nk = prim("cylinder", (.01, 0, .64), (.05, .05, .05), m=M(SKIN)); P(nk)
    hd = prim("uv_sphere", (.04, 0, .78), (.105, .1, .125), m=M(SKIN), segments=32, ring_count=16); smooth(hd); P(hd)
    gl = prim("cube", (.13, 0, .8), (.02, .1, .028), m=M(GLAS)); bevel(gl, .012); P(gl)
    ht = prim("uv_sphere", (.04, 0, .84), (.125, .12, .095), m=M(HAT), segments=32, ring_count=16); smooth(ht); P(ht)
    br = prim("cylinder", (.06, 0, .845), (.16, .14, .008), m=M(HAT), vertices=32); P(br)
    # Arme (je Ober-/Unterarm + Hand), Schaufel
    arms = {}
    for side in "LR":
        ua = cyl_between(name + "ua" + side, M(SHIRT), .048); fa = cyl_between(name + "fa" + side, M(SHIRT), .042)
        hn = prim("uv_sphere", m=M(SKIN), segments=16, ring_count=8, radius=.045); smooth(hn)
        for o in (ua, fa, hn): P(o)
        arms[side] = (ua, fa, hn)
    sh = empty(name + "_shovel"); sh.parent = spine; sh.location = SH.GRIP_O; sh.rotation_mode = 'XYZ'
    hdl = prim("cylinder", (0, 0, -SH.HANDLE / 2), (.018, .018, SH.HANDLE / 2), m=M(HANDLE_M), vertices=12); hdl.parent = sh
    tgrip = prim("cube", (0, 0, .03), (.02, .07, .02), m=M(HANDLE_M)); tgrip.parent = sh
    bl = prim("cube", (0, 0, -SH.HANDLE - .12), (.012, .12, .15), m=M(MET)); bevel(bl, .01); bl.parent = sh
    bm = bl.modifiers.new("cv", "SIMPLE_DEFORM"); bm.deform_method = 'BEND'; bm.angle = math.radians(25); bm.deform_axis = 'Y'
    clod = prim("uv_sphere", (.03, 0, -SH.HANDLE - .1), (.07, .1, .06), m=M(DIRT), segments=16, ring_count=8); clod.parent = sh
    if ghost:
        for o in [root, spine, sh] + parts + [hdl, tgrip, bl, clod]:
            if o.type == 'MESH': o.visible_shadow = False
    return dict(root=root, spine=spine, arms=arms, shovel=sh, clod=clod, parts=parts + [hdl, tgrip, bl, clod])
CHEF = build_worker("chef"); GH = build_worker("ghost", ghost=True)
CHEF["root"].location = SH.CHEF_ROOT; CHEF["root"].rotation_euler = (0, 0, SH.CHEF_YAW)
GH["root"].location = SH.GHOST_ROOT; GH["root"].rotation_euler = (0, 0, SH.GHOST_YAW)
# fliegende Erdklumpen (je Arbeiter einer)
FLY = {k: prim("uv_sphere", m=DIRT, segments=16, ring_count=8, radius=.06) for k in ("chef", "ghost")}
HEAP_T = (.15, 1.1, .32)

def pose_worker(W, t, ph, active, mirror, f, vis):
    p = SH.dig_pose(t, ph, active)
    if mirror: p = dict(p, twist=-p["twist"])
    sp = W["spine"]; sp.rotation_euler = (0, p["bend"], p["twist"]); sp.keyframe_insert("rotation_euler", frame=f)
    W["shovel"].rotation_euler = (0, p["sa"], 0); W["shovel"].keyframe_insert("rotation_euler", frame=f)
    gu, gl_, blade = SH.grips(p)
    for side, sh_, hand in (("R", SH.SHOULDER_R, gu), ("L", SH.SHOULDER_L, gl_)):
        ua, fa, hn = W["arms"][side]
        el = SH.elbow(sh_, hand, [-.2, (-.6 if side == "R" else .6), -.8])
        for o, a, b in ((ua, sh_, el), (fa, el, hand)):
            d = Vector(b) - Vector(a); o.location = a; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); o.scale = (1, 1, d.length)
            o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_quaternion", frame=f); o.keyframe_insert("scale", frame=f)
        hn.location = hand; hn.keyframe_insert("location", frame=f)
    W["clod"].hide_render = not (p["scoop"] > 0 and active and vis); W["clod"].keyframe_insert("hide_render", frame=f)
    return p
def ballistic(a, b, u, h=.6): return [a[i] + (b[i] - a[i]) * u for i in range(2)] + [a[2] + (b[2] - a[2]) * u + h * 4 * u * (1 - u)]
ground_vis = lambda t: t < SH.T_SPACE or t >= SH.T_BACK
for f in range(SH.NF):
    t = f / FPS; gv = ground_vis(t)
    chef_active = t > .15 and not (SH.ST[2][0] + .1 < t < SH.ST[3][0] - .2) and gv
    pose_worker(CHEF, t, 0., chef_active, False, f, gv)
    gh_vis = (t > SH.T_FOLLOW - .05 and t < SH.T_RISE + .3) or t >= SH.T_BACK
    pose_worker(GH, t, .55, gh_vis and t > SH.T_FOLLOW + .5, True, f, gh_vis)
    for o in GH["parts"]:
        if o.type == 'MESH' and o is not GH["clod"]: o.hide_render = not gh_vis; o.keyframe_insert("hide_render", frame=f)
    # Klumpen fliegt nach dem Schwung zum Haufen
    for key, W, ph, act, mir, root, yaw in (("chef", CHEF, 0., chef_active, False, SH.CHEF_ROOT, SH.CHEF_YAW), ("ghost", GH, .55, gh_vis and t > SH.T_FOLLOW + .5, True, SH.GHOST_ROOT, SH.GHOST_YAW)):
        o = FLY[key]; p = SH.dig_pose(t, ph, act); show = act and .74 <= p["p"] < .98
        if show:
            t0 = t - (p["p"] - .74) * 1.15; p0 = SH.dig_pose(t0, ph, True)
            if mir: p0 = dict(p0, twist=-p0["twist"])
            a = SH.spine_to_world(root, yaw, p0, SH.grips(p0)[2]); u = (p["p"] - .74) / .24
            o.location = ballistic(a, HEAP_T, u, .35)
        o.hide_render = not show; o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("location", frame=f)
for o in bpy.data.objects:
    ad = o.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if fc.data_path == "hide_render":
                for k in fc.keyframe_points: k.interpolation = 'CONSTANT'

# ======================================================= ERDE (aufgeschnitten)
def earth_mat():
    m, nt, b = newmat("earth"); nodes = nt.nodes
    tc = nodes.new("ShaderNodeTexCoord"); sep = nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sep.inputs[0])
    at = nodes.new("ShaderNodeMath"); at.operation = 'ARCTAN2'; nt.links.new(sep.outputs[1], at.inputs[0]); nt.links.new(sep.outputs[0], at.inputs[1])
    ln = nodes.new("ShaderNodeVectorMath"); ln.operation = 'LENGTH'; nt.links.new(tc.outputs["Object"], ln.inputs[0])
    dv = nodes.new("ShaderNodeMath"); dv.operation = 'DIVIDE'; nt.links.new(sep.outputs[2], dv.inputs[0]); nt.links.new(ln.outputs["Value"], dv.inputs[1])
    asn = nodes.new("ShaderNodeMath"); asn.operation = 'ARCSINE'; nt.links.new(dv.outputs[0], asn.inputs[0])
    u = nodes.new("ShaderNodeMath"); u.operation = 'MULTIPLY_ADD'; u.inputs[1].default_value = 1 / (2 * math.pi); u.inputs[2].default_value = .5; nt.links.new(at.outputs[0], u.inputs[0])
    v = nodes.new("ShaderNodeMath"); v.operation = 'MULTIPLY_ADD'; v.inputs[1].default_value = 1 / math.pi; v.inputs[2].default_value = .5; nt.links.new(asn.outputs[0], v.inputs[0])
    uv = nodes.new("ShaderNodeCombineXYZ"); nt.links.new(u.outputs[0], uv.inputs[0]); nt.links.new(v.outputs[0], uv.inputs[1])
    E = img(nt, "earth.jpg"); E.extension = 'REPEAT'; E.interpolation = 'Cubic'; nt.links.new(uv.outputs[0], E.inputs["Vector"])
    nt.links.new(E.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = .55
    # Ozeane leicht glaenzend (blau-Anteil)
    # Innenleben nach Radius
    rr = nodes.new("ShaderNodeMath"); rr.operation = 'DIVIDE'; rr.inputs[1].default_value = SH.R; nt.links.new(ln.outputs["Value"], rr.inputs[0])
    nz = nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.6; nz.inputs["Detail"].default_value = 9; nz.inputs["Distortion"].default_value = .8; nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nz2 = nodes.new("ShaderNodeMath"); nz2.operation = 'MULTIPLY_ADD'; nz2.inputs[1].default_value = .045; nz2.inputs[2].default_value = -.022; nt.links.new(nz.outputs["Fac"], nz2.inputs[0])
    rn = nodes.new("ShaderNodeMath"); rn.operation = 'ADD'; nt.links.new(rr.outputs[0], rn.inputs[0]); nt.links.new(nz2.outputs[0], rn.inputs[1])
    cr = nodes.new("ShaderNodeValToRGB"); cre = cr.color_ramp; cre.interpolation = 'LINEAR'
    stops = [(0.0, "#fffbe0"), (.17, "#ffe680"), (.195, "#ffb43a"), (.42, "#ff8a1e"), (.52, "#e8541a"), (.545, "#c33a12"), (.80, "#a3290e"), (.965, "#7a1d0a"), (.975, "#5a4030"), (1.0, "#6b5442")]
    cre.elements[0].position, cre.elements[0].color = stops[0][0], hexc(stops[0][1]); cre.elements[1].position, cre.elements[1].color = stops[-1][0], hexc(stops[-1][1])
    for p_, c in stops[1:-1]: e = cre.elements.new(p_); e.color = hexc(c)
    nt.links.new(rn.outputs[0], cr.inputs["Fac"])
    # Glut-Staerke (Kern hell, Kruste nicht)
    gr_ = nodes.new("ShaderNodeMapRange"); gr_.inputs["From Min"].default_value = .975; gr_.inputs["From Max"].default_value = .0; gr_.inputs["To Min"].default_value = 0; gr_.inputs["To Max"].default_value = 3.0
    nt.links.new(rr.outputs[0], gr_.inputs["Value"])
    inner = nodes.new("ShaderNodeEmission"); nt.links.new(cr.outputs["Color"], inner.inputs["Color"]); nt.links.new(gr_.outputs["Result"], inner.inputs["Strength"])
    innerd = nodes.new("ShaderNodeBsdfDiffuse"); nt.links.new(cr.outputs["Color"], innerd.inputs["Color"])
    ia = nodes.new("ShaderNodeAddShader"); nt.links.new(inner.outputs[0], ia.inputs[0]); nt.links.new(innerd.outputs[0], ia.inputs[1])
    # Schale (Oberflaeche) vs. Schnittflaeche: Radius > R - 0.03
    th = nodes.new("ShaderNodeMath"); th.operation = 'GREATER_THAN'; th.inputs[1].default_value = SH.R - .03; nt.links.new(ln.outputs["Value"], th.inputs[0])
    out = nt.nodes["Material Output"]; mix = nodes.new("ShaderNodeMixShader"); nt.links.new(th.outputs[0], mix.inputs[0])
    nt.links.new(ia.outputs[0], mix.inputs[1]); nt.links.new(b.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m
EARTH = earth_mat()
earth = prim("uv_sphere", tuple(SH.G), m=EARTH, segments=160, ring_count=80, radius=SH.R); smooth(earth); earth.name = "earth"
# Deutschland (51 N, 11 O) nach oben drehen: Objekt-Richtung (lat, lon) -> +Z
lat, lon = math.radians(51), math.radians(11)
vdir = Vector((math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)))
q = vdir.rotation_difference(Vector((0, 0, 1)))
q = Quaternion((0, 0, 1), math.radians(float(OPT.get("spin", 200)))) @ q            # um die Hochachse drehen, damit Europa/Afrika sichtbar sind
earth.rotation_mode = 'QUATERNION'; earth.rotation_quaternion = q
cut = prim("cube", (SH.G[0] + SH.R, SH.G[1] - SH.R, SH.G[2] + SH.R), (SH.R, SH.R, SH.R)); cut.hide_render = True; cut.display_type = 'WIRE'
bo = earth.modifiers.new("cut", "BOOLEAN"); bo.object = cut; bo.operation = 'DIFFERENCE'; bo.solver = 'EXACT'
# Atmosphaere (Rand-Leuchten)
def atmo_mat():
    m, nt, b = newmat("atmo"); nodes = nt.nodes; nodes.remove(b)
    lw = nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = .12
    pw = nodes.new("ShaderNodeMath"); pw.operation = 'POWER'; pw.inputs[1].default_value = 5.0; nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    em = nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = hexc("#6fb8ff"); em.inputs["Strength"].default_value = 3.0
    tr = nodes.new("ShaderNodeBsdfTransparent"); mx = nodes.new("ShaderNodeMixShader"); nt.links.new(pw.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], nt.nodes["Material Output"].inputs["Surface"]); return m
atmo = prim("uv_sphere", tuple(SH.G), m=atmo_mat(), segments=96, ring_count=48, radius=SH.R * 1.03); smooth(atmo)
for o in (earth, atmo): o.visible_shadow = False

# ======================================================= KAMERA (ein Objekt, Bild fuer Bild)
cd = bpy.data.cameras.new("cam"); cd.lens = SH.LENS; cd.sensor_fit = 'VERTICAL'; cd.sensor_height = SH.SENSOR; cd.clip_start = .03; cd.clip_end = 5000
cam = bpy.data.objects.new("cam", cd); link(cam); S.camera = cam; cam.rotation_mode = 'QUATERNION'
cd.dof.use_dof = True; cd.dof.aperture_fstop = float(OPT.get("fstop", 5.6))
for f in range(SH.NF):
    t = f / FPS; p, tg = SH.cam_at(t)
    cam.location = p; cam.rotation_quaternion = (Vector(tg) - Vector(p)).to_track_quat('-Z', 'Y'); cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_quaternion", frame=f)
    ground = t < SH.T_SPACE or t >= SH.T_BACK
    fd = (Vector(tg) - Vector(p)).length if ground else 1e4
    cd.dof.focus_distance = fd if t < SH.T_RISE or t >= SH.T_BACK else 1e4; cd.dof.keyframe_insert("focus_distance", frame=f)

# ======================================================= RENDER + Dunst (Mist) nur am Boden
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'
S.cycles.samples = int(OPT.get("samples", 40)); S.cycles.use_denoising = True; S.cycles.adaptive_threshold = .03
try: S.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
S.cycles.max_bounces = 5; S.cycles.diffuse_bounces = 2; S.cycles.glossy_bounces = 2; S.cycles.transmission_bounces = 2; S.cycles.transparent_max_bounces = 8
S.render.use_persistent_data = True
S.view_settings.view_transform = 'AgX'; S.view_settings.exposure = float(OPT.get("exp", 0.0))
try: S.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
vl = S.view_layers[0]; vl.use_pass_mist = True; WD.mist_settings.start = 12; WD.mist_settings.depth = 260; WD.mist_settings.falloff = 'QUADRATIC'
S.use_nodes = True; ct = S.node_tree; ct.nodes.clear()
rl = ct.nodes.new("CompositorNodeRLayers"); cm = ct.nodes.new("CompositorNodeMixRGB"); cm.inputs[2].default_value = (.78, .86, .95, 1)
mm = ct.nodes.new("CompositorNodeMath"); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = .55
ct.links.new(rl.outputs["Mist"], mm.inputs[0]); ct.links.new(mm.outputs[0], cm.inputs[0]); ct.links.new(rl.outputs["Image"], cm.inputs[1])
co = ct.nodes.new("CompositorNodeComposite"); ct.links.new(cm.outputs[0], co.inputs["Image"])
for f, v in ((0, .55), (F(SH.T_SPACE) - 1, .55), (F(SH.T_SPACE), 0.), (F(SH.T_BACK) - 1, 0.), (F(SH.T_BACK), .55)):
    mm.inputs[1].default_value = v; mm.inputs[1].keyframe_insert("default_value", frame=f)
S.render.resolution_x = SH.W; S.render.resolution_y = SH.H; S.render.resolution_percentage = int(OPT.get("pct", 100))
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGB'
print("TIMES space", SH.T_SPACE, "back", SH.T_BACK, "NF", SH.NF)
if "stills" in OPT:
    for f in [int(x) for x in OPT["stills"].split(",")]:
        S.frame_set(f); S.render.filepath = os.path.join(OUT, "still_%04d.png" % f); bpy.ops.render.render(write_still=True); print("STILL", f)
elif "frames" in OPT:
    a, b = [int(x) for x in OPT["frames"].split("-")]
    S.frame_start = a; S.frame_end = min(b, SH.NF - 1); S.render.filepath = os.path.join(OUT, "f_"); bpy.ops.render.render(animation=True); print("FRAMES", a, b)
