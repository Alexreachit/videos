# Bis zum Erdkern – Tag 2 (201 Arbeiter, 804 m Schacht), realistische Umgebung (Cycles). Texturen: Poly Haven (CC0), Erde: NASA Blue Marble (gemeinfrei).
# blender -b --factory-startup -P mg/erd03/scene.py -- <OUT> stills=30,200 [samples=32 pct=100 grass=40000] | frames=a-b
import bpy, bmesh, sys, os, math, random
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
env = wt.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(os.path.join(TEX, OPT.get("hdri", "field.hdr")))
wmap = wt.nodes.new("ShaderNodeMapping"); wtc = wt.nodes.new("ShaderNodeTexCoord"); wmap.inputs["Rotation"].default_value = (0, 0, math.radians(float(OPT.get("hrot", 0))))
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

sun = bpy.data.lights.new("sun", "SUN"); sun.energy = float(OPT.get("sun", 1.6)); sun.angle = math.radians(10); sun.color = (1., .96, .9)
so = bpy.data.objects.new("sun", sun); link(so); so.rotation_mode = 'QUATERNION'; so.rotation_quaternion = Vector((-.45, -.6, .66)).normalized().to_track_quat('Z', 'Y')

# ======================================================= BODEN mit Loch
GRASS, gnt, gb, gmp, gD = texmat("grass", "aerial_grass_rock", scale=.45, bump=1.2, tint="#d8ffd0")
DIRT, *_ = texmat("dirt", "brown_mud_02", scale=.8, bump=1.4)
# Gras/Erde-Mischung im selben Material (Maske: Abstand zum Loch + Rauschen)
def ground_mat():
    m, nt, b, mp, D = texmat("ground", "aerial_grass_rock", scale=.3, bump=1.1, tint="#e6ffd8")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    D2 = img(nt, "brown_mud_02_diff.jpg"); mp2 = nt.nodes.new("ShaderNodeMapping"); mp2.inputs["Scale"].default_value = (.9, .9, .9); nt.links.new(geo.outputs["Position"], mp2.inputs["Vector"]); nt.links.new(mp2.outputs["Vector"], D2.inputs["Vector"])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sep.inputs[0])
    # Abstand zum Loch (0,0) und zum Erdhaufen
    vl = nt.nodes.new("ShaderNodeVectorMath"); vl.operation = 'LENGTH'
    cxy = nt.nodes.new("ShaderNodeCombineXYZ"); nt.links.new(sep.outputs[0], cxy.inputs[0]); nt.links.new(sep.outputs[1], cxy.inputs[1]); nt.links.new(cxy.outputs[0], vl.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.5; nz.inputs["Detail"].default_value = 8; nt.links.new(geo.outputs["Position"], nz.inputs["Vector"])
    ad = nt.nodes.new("ShaderNodeMath"); ad.operation = 'MULTIPLY_ADD'; ad.inputs[1].default_value = .45; nt.links.new(nz.outputs["Fac"], ad.inputs[0]); nt.links.new(vl.outputs["Value"], ad.inputs[2])
    rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["From Min"].default_value = SH.PIT_R + 1.5; rr.inputs["From Max"].default_value = SH.PIT_R + .9; nt.links.new(ad.outputs[0], rr.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; nt.links.new(rr.outputs["Result"], mx.inputs["Factor"])
    link_from = b.inputs["Base Color"].links[0].from_socket
    mz = nt.nodes.new("ShaderNodeTexNoise"); mz.inputs["Scale"].default_value = .18; mz.inputs["Detail"].default_value = 4; nt.links.new(geo.outputs["Position"], mz.inputs["Vector"])
    mzr = nt.nodes.new("ShaderNodeMapRange"); mzr.inputs["From Min"].default_value = .3; mzr.inputs["From Max"].default_value = .7; mzr.inputs["To Min"].default_value = .62; mzr.inputs["To Max"].default_value = 1.15; nt.links.new(mz.outputs["Fac"], mzr.inputs["Value"])
    mv = nt.nodes.new("ShaderNodeMix"); mv.data_type = 'RGBA'; mv.blend_type = 'MULTIPLY'; mv.inputs["Factor"].default_value = 1.
    nt.links.new(link_from, mv.inputs[6]); cmb = nt.nodes.new("ShaderNodeCombineXYZ"); [nt.links.new(mzr.outputs["Result"], cmb.inputs[i]) for i in range(3)]; nt.links.new(cmb.outputs[0], mv.inputs[7])
    link_from = mv.outputs[2]; nt.links.new(link_from, mx.inputs[6]); nt.links.new(D2.outputs["Color"], mx.inputs[7]); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    return m, rr
GROUND, GMASK = ground_mat()
cl_ = lambda x: max(0., min(1., x))
# feines Gitter um das Loch (mit Mulde), dazu grosse Flaeche bis zum Horizont
bpy.ops.mesh.primitive_grid_add(x_subdivisions=400, y_subdivisions=400, size=38, location=(0, 0, 0)); gr = bpy.context.active_object; gr.name = "near"
import bmesh
bm = bmesh.new(); bm.from_mesh(gr.data)
for v in bm.verts:
    x, y = v.co.x, v.co.y; d = math.hypot(x, y)
    z = .025 * math.sin(x * 1.7 + 1) * math.cos(y * 1.3) + .012 * math.sin(x * 7.1) * math.sin(y * 6.3)
    if d < SH.PIT_R + 1.3: z += .16 * math.sin(cl_((d - SH.PIT_R) / 1.3) * math.pi) ** .8      # Erdwall am Rand
    edge = max(0., (max(abs(x), abs(y)) - 17) / 2); z -= edge * .02
    v.co.z = z
bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < SH.PIT_R - .02], context='VERTS')
for v in bm.verts:                                   # gezackten Lochrand auf exakten Kreis ziehen
    d = math.hypot(v.co.x, v.co.y)
    if v.is_boundary and d < SH.PIT_R + .3: v.co.x *= SH.PIT_R / d; v.co.y *= SH.PIT_R / d; v.co.z = 0.
bm.to_mesh(gr.data); bm.free()
smooth(gr); gr.data.materials.append(GROUND)
# Ferne Flaeche als Rahmen um das nahe Gitter (Mitte offen -> das Loch bleibt wirklich offen)
for cx, cy, sx, sy in ((0, 51.5, 85, 33.5), (0, -51.5, 85, 33.5), (51.5, 0, 33.5, 18), (-51.5, 0, 33.5, 18)):
    prim("plane", (cx, cy, -.03), (sx, sy, 1), m=GROUND, size=2)
# Haufen bekommt Erd-Material (eigene Kappe)
HEAPS = {"chef": (2.0, -3.2, .12), "ghost": (-2.3, -3.3, .12)}
for k_, (hx, hy, hz) in HEAPS.items():
    heap = prim("uv_sphere", (hx, hy, -.05), (.55, .5, .28), m=DIRT, segments=40, ring_count=20); smooth(heap)
    hd_ = heap.modifiers.new("d", "DISPLACE"); tx = bpy.data.textures.new("clods" + k_, "CLOUDS"); tx.noise_scale = .09; tx.noise_depth = 4; hd_.texture = tx; hd_.strength = .14
# Steine verstreut
ROCK, *_ = texmat("rock", "gray_rocks", scale=1.6, worldcoords=False, bump=1.5)
for k in range(26):
    a = rnd.random() * 6.283; d = 17.5 + rnd.random() * 6                    # vor der Kamera frei lassen
    r = .04 + rnd.random() * .14
    st = prim("ico_sphere", (math.cos(a) * d, math.sin(a) * d, -r * .3), (r * (1 + rnd.random()), r, r * .7), (rnd.random(), rnd.random(), rnd.random()), m=ROCK, subdivisions=3)
    dm = st.modifiers.new("d", "DISPLACE"); t2 = bpy.data.textures.new("rk%d" % k, "VORONOI"); t2.noise_scale = .3; dm.texture = t2; dm.strength = r * .35
# Gras-Halme (Partikel) auf dem nahen Gitter, nicht im Loch/Haufen
if int(OPT.get("grass", 45000)) > 0:
    vg = gr.vertex_groups.new(name="dens")
    for v in gr.data.vertices:
        x, y = v.co.x, v.co.y; d = math.hypot(x, y); hd = math.hypot(x - .12, y - 1.18)
        wv = cl_((d - SH.PIT_R - 1.0) / .6)
        vg.add([v.index], wv, 'REPLACE')
    ps = gr.modifiers.new("gras", "PARTICLE_SYSTEM").particle_system; pst = ps.settings
    pst.type = 'HAIR'; pst.count = int(OPT.get("grass", 70000)); pst.use_advanced_hair = False; pst.hair_length = .09
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
for k, (x, y) in enumerate(()):
    s = .9 + rnd.random() * .6; z = 0
    tr = prim("cylinder", (x, y, 2.2 * s), (.22 * s, .22 * s, 2.2 * s), m=BARK, vertices=12)
    for j in range(6):
        b = prim("ico_sphere", (x + rnd.uniform(-1.4, 1.4) * s, y + rnd.uniform(-1.2, 1.2) * s, (4.6 + rnd.uniform(-.5, 1.6)) * s), (1.6 * s, 1.6 * s, 1.4 * s), m=LEAF, subdivisions=3)
        dm = b.modifiers.new("d", "DISPLACE"); t3 = bpy.data.textures.new("lf%d_%d" % (k, j), "CLOUDS"); t3.noise_scale = .5; dm.texture = t3; dm.strength = .6; smooth(b)
# Schild "BIS ZUM ERDKERN"
WOOD = pbr("wood", "#8a5a34", .7); PAINT = pbr("paint", "#f4f1e8", .5)
SX, SY = 3.6, -4.9
for dx in (-.75, .75): prim("cylinder", (SX + dx, SY, .75), (.05, .05, .75), m=WOOD, vertices=10)
board = prim("cube", (SX, SY, 1.25), (.95, .04, .36), m=WOOD); bevel(board, .015)
for row, (txt, z) in enumerate((("BIS ZUM", 1.39), ("ERDKERN", 1.08))):
    bpy.ops.object.text_add(location=(SX, SY - .045, z), rotation=(math.pi / 2, 0, 0)); tx_ = bpy.context.active_object; tx_.data.body = txt; tx_.data.align_x = 'CENTER'; tx_.data.size = .26; tx_.data.extrude = .006; tx_.data.materials.append(PAINT)
# Schubkarre-Ersatz: Eimer + Spitzhacke am Rand
MET = pbr("metal", "#8c9196", .35, metal=1.); prim("cylinder", (-2.6, -4.6, .16), (.17, .17, .16), m=MET, vertices=24)

# ======================================================= ARBEITER (stilisiert, realistische Materialien, ohne Gesicht)
SKIN = pbr("skin", "#c99a78", .55, sss=.2); VEST = pbr("vest", "#ff6a14", .6); STRIPE = pbr("stripe", "#d9dde0", .25, metal=.6)
SHIRT = pbr("shirt", "#2c4f86", .8); PANTS = pbr("pants", "#2f3540", .85); BOOT = pbr("boot", "#3a2a1c", .6); HAT = pbr("hat", "#ffcc1a", .28, coat=.6)
GLAS = pbr("glas", "#101418", .08, metal=.4); HANDLE_M = pbr("handle", "#9b6b3c", .6)
def ghost_mat():
    m, nt, b = newmat("ghost"); nodes = nt.nodes; nodes.remove(b)
    lw = nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = .35
    em = nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = hexc("#bcd4ff"); em.inputs["Strength"].default_value = .9
    tr = nodes.new("ShaderNodeBsdfTransparent"); mx = nodes.new("ShaderNodeMixShader")
    mp = nodes.new("ShaderNodeMapRange"); mp.inputs["To Min"].default_value = .06; mp.inputs["To Max"].default_value = .75; nt.links.new(lw.outputs["Facing"], mp.inputs["Value"])
    nt.links.new(mp.outputs["Result"], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], nt.nodes["Material Output"].inputs["Surface"]); return m
GHOSTM = ghost_mat()
def cyl_between(name, m, r=.05):
    o = prim("cylinder", m=m, vertices=16, radius=r, depth=1.0); smooth(o); o.name = name
    o.data.transform(Matrix.Translation((0, 0, .5)))            # Ursprung an einem Ende, Laenge 1 in +Z
    o.rotation_mode = 'QUATERNION'; return o
def diamond_mat():
    m, nt, b = newmat("diamond"); b.inputs["Base Color"].default_value = hexc("#a8ecff"); b.inputs["Roughness"].default_value = .0
    b.inputs["Transmission Weight"].default_value = 1.; b.inputs["IOR"].default_value = 2.42
    b.inputs["Emission Color"].default_value = hexc("#2fc4ff"); b.inputs["Emission Strength"].default_value = .9
    return m
DIAM = diamond_mat()
def build_worker(name, ghost=False, shirt=None, blade=None, hat=None):
    M = (lambda m: GHOSTM) if ghost else (lambda m: (shirt if (shirt is not None and m is SHIRT) else (hat if (hat is not None and m is HAT) else m)))
    root = empty(name + "_root"); spine = empty(name + "_spine"); spine.parent = root; spine.location = (0, 0, SH.HIP); spine.rotation_mode = 'XYZ'
    parts = []
    def P(o, par=spine): o.parent = par; parts.append(o); return o
    # Beine (fest)
    for y in (.11, -.11):
        lg = prim("cylinder", (0, y * 1.15, .48), (.068, .068, .46), m=M(PANTS), vertices=16); smooth(lg); P(lg, root)
        bt = prim("cube", (.05, y * 1.15, .06), (.13, .058, .06), m=M(BOOT)); bevel(bt, .03); P(bt, root)
    hip = prim("cube", (0, 0, SH.HIP - .02), (.12, .2, .1), m=M(PANTS)); bevel(hip, .05); P(hip, root)
    # Oberkoerper (im Spine-Raum, Spine bei Huefthoehe)
    to = prim("cube", (0, 0, .31), (.15, .22, .31), m=M(SHIRT)); bevel(to, .09, 4); P(to)
    ve = prim("cube", (.005, 0, .3), (.158, .228, .26), m=M(VEST)); bevel(ve, .08, 4); P(ve)
    for z in (.2, .34): s_ = prim("cube", (.006, 0, z), (.16, .23, .018), m=M(STRIPE)); bevel(s_, .01); P(s_)
    nk = prim("cylinder", (.01, 0, .66), (.055, .055, .05), m=M(SKIN)); P(nk)
    hd = prim("uv_sphere", (.04, 0, .80), (.118, .112, .138), m=M(SKIN), segments=32, ring_count=16); smooth(hd); P(hd)
    gl = prim("cube", (.145, 0, .82), (.02, .112, .03), m=M(GLAS)); bevel(gl, .012); P(gl)
    ht = prim("uv_sphere", (.04, 0, .87), (.138, .132, .1), m=M(HAT), segments=32, ring_count=16); smooth(ht); P(ht)
    br = prim("cylinder", (.065, 0, .875), (.175, .155, .008), m=M(HAT), vertices=32); P(br)
    # Arme (je Ober-/Unterarm + Hand), Schaufel
    arms = {}
    for side in "LR":
        ua = cyl_between(name + "ua" + side, M(SHIRT), .055); fa = cyl_between(name + "fa" + side, M(SHIRT), .047)
        hn = prim("uv_sphere", m=M(SKIN), segments=16, ring_count=8, radius=.045); smooth(hn)
        for o in (ua, fa, hn): P(o)
        arms[side] = (ua, fa, hn)
    sh = empty(name + "_shovel"); sh.parent = spine; sh.location = SH.GRIP_O; sh.rotation_mode = 'XYZ'
    hdl = prim("cylinder", (0, 0, -SH.HANDLE / 2), (.018, .018, SH.HANDLE / 2), m=M(HANDLE_M), vertices=12); hdl.parent = sh
    tgrip = prim("cube", (0, 0, .03), (.02, .07, .02), m=M(HANDLE_M)); tgrip.parent = sh
    bl = prim("cube", (0, 0, -SH.HANDLE - .12), (.012 if blade is None else .02, .12, .15), m=(blade or M(MET))); bevel(bl, .01 if blade is None else .006); bl.parent = sh
    bm = bl.modifiers.new("cv", "SIMPLE_DEFORM"); bm.deform_method = 'BEND'; bm.angle = math.radians(25); bm.deform_axis = 'Y'
    clod = prim("uv_sphere", (.03, 0, -SH.HANDLE - .1), (.07, .1, .06), m=M(DIRT), segments=16, ring_count=8); clod.parent = sh
    if ghost:
        for o in [root, spine, sh] + parts + [hdl, tgrip, bl, clod]:
            if o.type == 'MESH': o.visible_shadow = False
    return dict(root=root, spine=spine, arms=arms, shovel=sh, clod=clod, parts=parts + [hdl, tgrip, bl, clod])
CHEF = build_worker("chef"); GH = build_worker("blake", shirt=pbr("blake_shirt", "#1fa3b8", .75), blade=DIAM)
SPARK = []
for o in GH["parts"]:
    if o.type == 'MESH' and DIAM in [ms.material for ms in o.material_slots]:
        sp_ = bpy.data.lights.new("blake_sparkle", "POINT"); sp_.energy = 6; sp_.color = (.75, .92, 1.); sp_.shadow_soft_size = .02
        so_ = bpy.data.objects.new("blake_sparkle", sp_); link(so_); so_.parent = o; so_.location = (.25, 0, .05); SPARK.append(sp_)
for sp_ in SPARK:
    for f, v in ((0, 0.), (1, 15.), (F(SH.T_SPACE) - 1, 15.), (F(SH.T_SPACE), 0.), (F(SH.T_BACK) - 1, 0.), (F(SH.T_BACK), 15.)):
        sp_.energy = v; sp_.keyframe_insert("energy", frame=f)
CHEF["root"].location = SH.CHEF_ROOT; CHEF["root"].rotation_euler = (0, 0, SH.CHEF_YAW)
GH["root"].location = SH.BLAKE_ROOT; GH["root"].rotation_euler = (0, 0, SH.BLAKE_YAW)
LE = build_worker("lena", hat=pbr("pink_helmet", "#ff4fb3", .3))
LE["root"].location = SH.LENA_ROOT; LE["root"].rotation_euler = (0, 0, SH.LENA_YAW)
# fliegende Erdklumpen (je Arbeiter einer)
FLY = {k: prim("uv_sphere", m=DIRT, segments=16, ring_count=8, radius=.06) for k in ("chef", "ghost")}


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
    chef_active = gv and not (SH.T_DESC0 - .5 < t < SH.T_UP)
    le_vis = gv and t >= SH.T_UP - .05                     # Lena erscheint erst mit ihrem pinken Helm
    pose_worker(LE, t, .3, le_vis, False, f, le_vis)
    for o in LE["parts"]:
        if o.type == 'MESH' and o is not LE.get("clod"): o.hide_render = not le_vis; o.keyframe_insert("hide_render", frame=f)
    pose_worker(CHEF, t, 0., chef_active, False, f, gv)
    gh_vis = gv
    pose_worker(GH, t, .55, gh_vis, True, f, gh_vis)
    for o in GH["parts"]:
        if o.type == 'MESH' and o is not GH["clod"]: o.hide_render = not gh_vis; o.keyframe_insert("hide_render", frame=f)
    # Klumpen fliegt nach dem Schwung zum Haufen
    for key, W, ph, act, mir, root, yaw in (("chef", CHEF, 0., chef_active, False, SH.CHEF_ROOT, SH.CHEF_YAW), ("ghost", GH, .55, gh_vis, True, SH.BLAKE_ROOT, SH.BLAKE_YAW)):
        o = FLY[key]; p = SH.dig_pose(t, ph, act); show = act and .74 <= p["p"] < .98
        if show:
            t0 = t - (p["p"] - .74) * 1.15; p0 = SH.dig_pose(t0, ph, True)
            if mir: p0 = dict(p0, twist=-p0["twist"])
            a = SH.spine_to_world(root, yaw, p0, SH.grips(p0)[2]); u = (p["p"] - .74) / .24
            o.location = ballistic(a, HEAPS[key], u, .35)
        o.hide_render = not show; o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("location", frame=f)
for o in bpy.data.objects:
    ad = o.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if fc.data_path == "hide_render":
                for k in fc.keyframe_points: k.interpolation = 'CONSTANT'

# ======================================================= SCHACHT (804 m) mit Lampenringen
SROCK, *_ = texmat("shaftrock", "dry_riverbed_rock", scale=.35, worldcoords=False, bump=1.6)
SSOIL, *_ = texmat("shaftsoil", "brown_mud_02", scale=.6, worldcoords=False, bump=1.3)
def tube(r, z0, z1, m, name):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=z0 - z1, end_fill_type='NOTHING', location=(0, 0, (z0 + z1) / 2)); o = bpy.context.active_object; o.name = name
    o.data.materials.append(m); smooth(o)
    bm2 = bmesh.new(); bm2.from_mesh(o.data); bmesh.ops.reverse_faces(bm2, faces=bm2.faces[:]); bm2.to_mesh(o.data); bm2.free()
    return o
MANTLE, mnt, mb, *_ = texmat("mantle", "dry_riverbed_rock", scale=.35, worldcoords=False, bump=1.6, tint="#b8604a")
mb.inputs["Emission Color"].default_value = hexc("#ff3a08"); mb.inputs["Emission Strength"].default_value = .22
def depth_dark(m):
    """Wand wird nach unten schnell dunkel (von oben wirkt das Loch tief); beim Abstieg animiert auf hell"""
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; src = b.inputs["Base Color"].links[0].from_socket
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -.65; mr.inputs["From Max"].default_value = .05; mr.inputs["To Max"].default_value = 1.
    nt.links.new(sp.outputs[2], mr.inputs["Value"])
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.3; nt.links.new(mr.outputs["Result"], pw.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs["Factor"].default_value = 1.
    nt.links.new(src, mx.inputs[6]); cb = nt.nodes.new("ShaderNodeCombineXYZ"); [nt.links.new(pw.outputs[0], cb.inputs[i]) for i in range(3)]; nt.links.new(cb.outputs[0], mx.inputs[7])
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    tm = mr.inputs["To Min"]
    for f, v in ((0, 0.), (F(SH.T_DESC0) - 1, 0.), (F(SH.T_DESC0), 1.), (F(SH.T_UP) - 1, 1.), (F(SH.T_UP), 0.)):
        tm.default_value = v; tm.keyframe_insert("default_value", frame=f)
depth_dark(SSOIL); depth_dark(SROCK)
before_shaft = set(bpy.data.objects)
ROPE = pbr("rope2", "#c9a36a", .8)
for a_ in (math.radians(78), math.radians(104)):          # Seile haengen in die Tiefe
    x_, y_ = math.cos(a_) * (SH.PIT_R - .12), math.sin(a_) * (SH.PIT_R - .12)
    prim("cylinder", (x_, y_, -24.), (.016, .016, 25.), m=ROPE, vertices=8)
tube(SH.PIT_R, .05, -3.0, SSOIL, "soil"); tube(SH.PIT_R, -2.95, -SH.CRUST, SROCK, "rock"); tube(SH.PIT_R, -SH.CRUST + .05, -SH.DEPTH - 2, MANTLE, "mantle")
prim("cylinder", (0, 0, -SH.DEPTH - .3), (SH.PIT_R + .2, SH.PIT_R + .2, .3), m=MANTLE, vertices=48)
LAMPM = pbr("lamp", "#ffcf8a", .4, emis="#ffc27a", es=18.)
bpy.ops.mesh.primitive_torus_add(major_radius=SH.PIT_R - .1, minor_radius=.035, major_segments=32, minor_segments=6, location=(0, 0, -6)); lr = bpy.context.active_object; lr.data.materials.append(LAMPM); lr.visible_shadow = False
ar = lr.modifiers.new("arr", "ARRAY"); ar.use_relative_offset = False; ar.use_constant_offset = True; ar.constant_offset_displace = (0, 0, -20); ar.count = int((SH.DEPTH - 10) // 20)
for k, (xx, zz) in enumerate(((.5, SH.ZB + .9), (-.6, SH.ZB + .5))):            # Arbeitslicht unten
    vl_ = bpy.data.lights.new("work%d" % k, "POINT"); vl_.energy = 30; vl_.color = (1., .93, .82); vl_.shadow_soft_size = .1
    vo_ = bpy.data.objects.new("work%d" % k, vl_); link(vo_); vo_.location = (xx, 1.0, zz)
for o in set(bpy.data.objects) - before_shaft:          # Schacht im All ausblenden (reicht sonst durch die Erde)
    for f, v in ((0, False), (F(SH.T_SPACE), True), (F(SH.T_BACK), False)):
        o.hide_render = v; o.keyframe_insert("hide_render", frame=f)
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'

# Gelaender am Rand (Holzpfosten + Seil)
for k in range(28):
    a_ = k / 28 * 6.283; r_ = SH.PIT_R + .35
    prim("cylinder", (math.cos(a_) * r_, math.sin(a_) * r_, .55), (.04, .04, .55), m=WOOD, vertices=8)
bpy.ops.mesh.primitive_torus_add(major_radius=SH.PIT_R + .35, minor_radius=.018, major_segments=96, minor_segments=6, location=(0, 0, 1.0)); rope = bpy.context.active_object; rope.data.materials.append(pbr("rope", "#d84a2a", .7))

# ======================================================= MENGE: 200 Arbeiter (4 animierte Varianten, als Instanzen)
def shirt_rand():
    m, nt, b = newmat("shirt_rand"); oi = nt.nodes.new("ShaderNodeObjectInfo"); cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.interpolation = 'CONSTANT'
    cols = ["#2c4f86", "#3d6b3a", "#7a2f2f", "#4a4f57", "#2f6f80", "#5a3f7a"]
    cr.color_ramp.elements[0].color = hexc(cols[0]); cr.color_ramp.elements[1].position = .99; cr.color_ramp.elements[1].color = hexc(cols[-1])
    for i_, c in enumerate(cols[1:-1]): e = cr.color_ramp.elements.new((i_ + 1) / len(cols)); e.color = hexc(c)
    nt.links.new(oi.outputs["Random"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = .8
    return m
SHR = shirt_rand(); VARS = []
for vk in range(4):
    before = set(bpy.data.objects)
    Wv = build_worker("v%d" % vk, shirt=SHR)
    new = [o for o in bpy.data.objects if o not in before]
    col = bpy.data.collections.new("V%d" % vk)
    for o in new:
        col.objects.link(o)
        for c in list(o.users_collection):
            if c is not col: c.objects.unlink(o)
    VARS.append((Wv, col))
for f in range(SH.NF):
    t = f / FPS; on = t < SH.T_DESC0 + .5 or t >= SH.T_DESC1 - 1.
    for vk, (Wv, col) in enumerate(VARS):
        pose_worker(Wv, t, vk * .29, on, False, f, on)
print("MENGE", len(SH.POS))
for i_, (x_, y_, yaw_, s_) in enumerate(SH.POS):
    e = bpy.data.objects.new("crew%d" % i_, None); e.instance_type = 'COLLECTION'; e.instance_collection = VARS[i_ % 4][1]; link(e)
    e.location = (x_, y_, 0); e.rotation_euler = (0, 0, yaw_); e.scale = (s_, s_, s_)

BOT = [(-1.1, .8, .99), (1.15, .75, 2.15), (-.42, 1.65, math.pi / 2), (.45, 1.7, math.pi / 2)]
for i_, (x_, y_, yaw_) in enumerate(BOT):
    e = bpy.data.objects.new("bot%d" % i_, None); e.instance_type = 'COLLECTION'; e.instance_collection = VARS[(i_ + 1) % 4][1]; link(e)
    e.location = (x_, y_, -SH.DEPTH); e.rotation_euler = (0, 0, yaw_)
    for f, v in ((0, False), (F(SH.T_SPACE), True), (F(SH.T_BACK), False)):
        e.hide_render = v; e.keyframe_insert("hide_render", frame=f)

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
cd.dof.use_dof = True; cd.dof.aperture_fstop = float(OPT.get("fstop", 2.8))
hl = bpy.data.lights.new("headlamp", "POINT"); hl.energy = 0; hl.shadow_soft_size = .3; hl.color = (1, .9, .78); hlo = bpy.data.objects.new("headlamp", hl); link(hlo); hlo.parent = cam
for f, v in ((0, 0.), (F(SH.T_DESC0) - 1, 0.), (F(SH.T_DESC0), 220.), (F(SH.T_UP) - 1, 220.), (F(SH.T_UP), 0.)):
    hl.energy = v; hl.keyframe_insert("energy", frame=f)
for f in range(SH.NF):
    t = f / FPS; p, tg = SH.cam_at(t)
    cam.location = p; cam.rotation_quaternion = (Vector(tg) - Vector(p)).to_track_quat('-Z', 'Y'); cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_quaternion", frame=f)
    ground = t < SH.T_SPACE or t >= SH.T_BACK
    fd = (Vector(tg) - Vector(p)).length if ground else 1e4
    if SH.T_DESC0 <= t < SH.T_VEIN: fd = 1e4
    if SH.T_DESC1 <= t < SH.T_BLAKE: fd = 3.4 if t >= SH.T_DESC1 + 1.6 else max(1., p[2] + SH.DEPTH)
    cd.dof.focus_distance = fd; cd.dof.keyframe_insert("focus_distance", frame=f)
# Bewegungsunschaerfe nur beim Abstieg (Verschluss animiert)
S.render.use_motion_blur = True; S.render.motion_blur_position = 'CENTER'
for f, v in ((0, 0.), (F(SH.T_DESC0) + 6, 0.), (F(SH.T_DESC0) + 12, .15), (F(SH.T_DESC1) - 6, .15), (F(SH.T_DESC1), 0.)):
    S.render.motion_blur_shutter = v
    try: S.render.keyframe_insert("motion_blur_shutter", frame=f)
    except Exception as ex: print("MB-KEY", ex)

# ======================================================= RENDER + Dunst (Mist) nur am Boden
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'
S.cycles.samples = int(OPT.get("samples", 40)); S.cycles.use_denoising = True; S.cycles.adaptive_threshold = .03
try: S.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
S.cycles.max_bounces = 5; S.cycles.diffuse_bounces = 2; S.cycles.glossy_bounces = 2; S.cycles.transmission_bounces = 6; S.cycles.transparent_max_bounces = 8
S.render.use_persistent_data = True
S.view_settings.view_transform = 'AgX'; S.view_settings.exposure = float(OPT.get("exp", 0.0))
try: S.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
vl = S.view_layers[0]; vl.use_pass_mist = True; WD.mist_settings.start = 12; WD.mist_settings.depth = 260; WD.mist_settings.falloff = 'QUADRATIC'
S.use_nodes = True; ct = S.node_tree; ct.nodes.clear()
rl = ct.nodes.new("CompositorNodeRLayers"); cm = ct.nodes.new("CompositorNodeMixRGB"); cm.inputs[2].default_value = (.78, .86, .95, 1)
mm = ct.nodes.new("CompositorNodeMath"); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = 0.
ct.links.new(rl.outputs["Mist"], mm.inputs[0]); ct.links.new(mm.outputs[0], cm.inputs[0]); ct.links.new(rl.outputs["Image"], cm.inputs[1])
co = ct.nodes.new("CompositorNodeComposite"); ct.links.new(cm.outputs[0], co.inputs["Image"])
for f, v in ((0, 0.), ):
    mm.inputs[1].default_value = v; mm.inputs[1].keyframe_insert("default_value", frame=f)
S.render.resolution_x = SH.W; S.render.resolution_y = SH.H; S.render.resolution_percentage = int(OPT.get("pct", 100))
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGB'
print("TIMES desc", SH.T_DESC0, SH.T_DESC1, "up", SH.T_UP, "space", SH.T_SPACE, "back", SH.T_BACK, "NF", SH.NF)
if "stills" in OPT:
    for f in [int(x) for x in OPT["stills"].split(",")]:
        S.frame_set(f); S.render.filepath = os.path.join(OUT, "still_%04d.png" % f); bpy.ops.render.render(write_still=True); print("STILL", f)
elif "frames" in OPT:
    a, b = [int(x) for x in OPT["frames"].split("-")]
    S.frame_start = a; S.frame_end = min(b, SH.NF - 1); S.render.filepath = os.path.join(OUT, "f_"); bpy.ops.render.render(animation=True); print("FRAMES", a, b)
