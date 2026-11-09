# Wichtelheim Folge 1 – "Ein leeres Tal". Knete-Look (Stop-Motion, 12 fps). Baut Tal, Wichtel Flocke, Bewohner, Kasse, Traumdorf, Abstimmungs-Modelle.
# blender -b --factory-startup -P mg/wichtel/ep01.py -- <OUT> stills=10,60  |  frames=0-120
import bpy, sys, os, math, json, random
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nb_lib as L
from nb_lib import hexc, sphere, rbox, cylr, cone, torus, text, empty, kf

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/out"]
OUT = ARGS[0]; os.makedirs(OUT, exist_ok=True)
OPT = dict(a.split("=", 1) for a in ARGS[1:] if "=" in a)
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
T = json.load(open(os.path.join(HERE, "ep01_timing.json")))
FPS = T["fps"]; SEG = T["segments"]; DUR = T["duration"]
F = lambda t: int(round(t * FPS))
S.render.fps = FPS; S.frame_start = 0; S.frame_end = F(DUR) - 1
CUT = [0] + [F(SEG[i]["start"]) - 2 for i in range(1, len(SEG))] + [F(DUR)]
def segf(i, frac): return F(SEG[i]["start"] + frac * (SEG[i]["end"] - SEG[i]["start"]))
rnd = random.Random(3)

# ===================================================== KNETE-MATERIAL
CLAYM = {}
def clay(name, col, rough=.62, sss=.08, emis=None, es=0):
    if name in CLAYM: return CLAYM[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(col); b.inputs["Roughness"].default_value = rough
    b.inputs["Sheen Weight"].default_value = .25
    if sss: b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1.0, .5, .3); b.inputs["Subsurface Scale"].default_value = .03
    if emis: b.inputs["Emission Color"].default_value = hexc(emis); b.inputs["Emission Strength"].default_value = es
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 22; nz.inputs["Detail"].default_value = 6
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 7; vo.feature = 'DISTANCE_TO_EDGE'
    b1 = nt.nodes.new("ShaderNodeBump"); b1.inputs["Strength"].default_value = .32; b1.inputs["Distance"].default_value = .02
    b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = .18; b2.inputs["Distance"].default_value = .02
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"]); nt.links.new(tc.outputs["Object"], vo.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], b1.inputs["Height"]); nt.links.new(vo.outputs["Distance"], b2.inputs["Height"])
    nt.links.new(b1.outputs["Normal"], b2.inputs["Normal"]); nt.links.new(b2.outputs["Normal"], b.inputs["Normal"])
    CLAYM[name] = m; return m
TEXCL = bpy.data.textures.new("lumps", "CLOUDS"); TEXCL.noise_scale = .35
def lumpy(o, amt=.015):
    d = o.modifiers.new("lump", "DISPLACE"); d.texture = TEXCL; d.strength = amt; d.mid_level = .5; d.texture_coords = 'OBJECT'
    return o
def C(fn, *a, l=.022, **k):
    o = fn(*a, **k); return lumpy(o, l) if o is not None and o.type == 'MESH' else o

# ===================================================== TAL
SNOW = clay("snow", "#f4f7fd", .7, .15)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=120, y_subdivisions=120, size=80, location=(0, 10, 0)); g = bpy.context.active_object
for v in g.data.vertices:
    x, y = v.co.x, v.co.y + 10; d = math.hypot(x, y - 6)
    v.co.z = max(0, (d - 9) * .08) ** 1.6 * 1.2 + .12 * math.sin(x * .6) * math.cos(y * .5)
g.data.materials.append(SNOW); L.smooth(g); lumpy(g, .05)
def gz(x, y): d = math.hypot(x, y - 6); return max(0, (d - 9) * .08) ** 1.6 * 1.2 + .12 * math.sin(x * .6) * math.cos(y * .5)
for x, y, s in ((-14, 30, 9), (6, 34, 11), (22, 28, 8), (-26, 22, 7), (28, 14, 6)):
    sphere((x, y, -1), s, (1.3, 1, .55), SNOW, seg=48)
TRK = clay("trunk", "#7a4a2c"); PINE = [clay("pine1", "#2f7a4a"), clay("pine2", "#3b8a52")]
def pine(x, y, s=1.0):
    z0 = gz(x, y) - .05; r0 = empty("pine", (0, 0, 0)); L.P[0] = r0
    C(cylr, (x, y, .25 * s), .12 * s, .5 * s, TRK, verts=12, bev=0)
    for k in range(3):
        C(cone, (x, y, (.55 + k * .55) * s), (.85 - k * .22) * s, .02, .9 * s, PINE[k % 2], verts=24)
        C(cone, (x, y, (.72 + k * .55) * s), (.55 - k * .16) * s, .02, .45 * s, SNOW, verts=24)
    L.P[0] = None; r0.location.z = z0
for k in range(22):
    a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(7.5, 16)
    x, y = math.cos(a) * r, 6 + math.sin(a) * r
    if y < 1.5 and abs(x) < 6: continue
    pine(x, y, rnd.uniform(.9, 1.6))
# Ortsschild
WOOD = clay("wood", "#a8703f"); INK = clay("ink", "#3a2418", .5)
C(cylr, (-3.2, 3.2, .7), .07, 1.4, WOOD, verts=10, bev=0)
C(rbox, (-3.2, 3.15, 1.35), (1.5, .1, .45), WOOD, bev=.4)
text("WICHTELHEIM", (-3.2, 3.09, 1.35), .17, INK, extrude=.02)

# ===================================================== FIGUREN (Cartoon-Stil: grosser runder Kopf, Kulleraugen, Jacke mit Streifen, duenne Arme)
import bmesh
SKIN = clay("skin", "#f3c39c", .55, .25); EYEW = clay("eyew", "#fbfbf8", .35, .05); EYE = clay("eye", "#16141a", .3, 0)
CHEEK = clay("cheek", "#f08a8a", .6, .2); MOUTH = clay("mouth", "#6e1f28", .5, 0); TONG = clay("tongue", "#ea6f78", .5, .1)
PANT = clay("pant", "#26232c", .6); SHOE = clay("shoe", "#18171c", .5); FUR = clay("fur", "#fbfbf6", .85, .1)
HAIRC = ["#6b3b1e", "#e2b65a", "#2a1d17", "#a8441f"]
def half_sphere(loc, r, scl, m):
    o = sphere(loc, r, scl, m, seg=32); bm = bmesh.new(); bm.from_mesh(o.data)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_outer=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    if edges: bmesh.ops.holes_fill(bm, edges=edges)
    bm.to_mesh(o.data); bm.free(); L.smooth(o); return o
def face(hc, r, brow="#4a2a18", ears="round", stache=None):
    for sx in (-1, 1):
        C(sphere, hc + Vector((sx * r * .37, -r * .9, r * .12)), r * .2, (1, .55, 1.25), EYEW, l=.006)
        sphere(hc + Vector((sx * r * .33, -r * 1.0, r * .07)), r * .09, (1, .5, 1.05), EYE, seg=20)
        sphere(hc + Vector((sx * r * .3, -r * 1.045, r * .13)), r * .028, (1, .5, 1), EYEW, seg=12)
        C(rbox, hc + Vector((sx * r * .38, -r * .88, r * .46)), (r * .26, r * .07, r * .075), clay("brow" + brow, brow, .7), rot=(0, sx * .22, 0), bev=.8, l=.006)
        C(sphere, hc + Vector((sx * r * .62, -r * .74, -r * .16)), r * .14, (1, .4, .8), CHEEK, l=.005)
        if ears == "elf": C(cone, hc + Vector((sx * r * 1.08, .0, r * .1)), r * .16, r * .02, r * .5, SKIN, rot=(0, sx * 1.2, 0), verts=16)
        else: C(sphere, hc + Vector((sx * r * .98, 0, -r * .02)), r * .17, (.5, 1, 1.2), SKIN)
    C(sphere, hc + Vector((0, -r * .99, -r * .1)), r * .1, (1.1, .9, .9), SKIN, l=.005)
    half_sphere(hc + Vector((0, -r * .86, -r * .3)), r * .28, (1, .4, .75), MOUTH)
    sphere(hc + Vector((0, -r * .88, -r * .44)), r * .11, (1.3, .45, .55), TONG, seg=20)
    if stache:
        for sx in (-1, 1): C(sphere, hc + Vector((sx * r * .15, -r * 1.0, -r * .2)), r * .14, (1.4, .55, .6), clay("st" + stache, stache, .8), rot=(0, -sx * .25, 0), l=.006)
def toon(name, jc, trim, s=1.0, collar=None):
    root = empty(name, (0, 0, 0)); inner = empty(name + "_in", (0, 0, 0), root); L.P[0] = inner
    JC = clay("jc" + jc, jc, .62); TR = clay("tr" + trim, trim, .6)
    for sx in (-1, 1):
        C(cylr, (sx * .09, 0, .15), .045, .28, PANT, verts=12, bev=0, l=.008)
        C(sphere, (sx * .1, -.04, .045), .08, (1, 1.5, .6), SHOE, l=.01)
    C(rbox, (0, 0, .44), (.46, .32, .42), JC, bev=.25, l=.015)
    for z in (.33, .42): C(rbox, (0, -.163, z), (.47, .014, .035), TR, bev=.4, l=.004)
    C(rbox, (0, -.166, .44), (.022, .01, .4), clay("zip", "#3a3540", .4), bev=.3, l=.003)
    C(torus, (0, .02, .65), .15, .055, clay("co" + (collar or trim), collar or trim, .7), scl=(1.15, 1, 1))
    arms = []
    for sx in (-1, 1):
        sh = empty(name + "_arm%d" % sx, (sx * .25, 0, .6), inner); L.P[0] = sh
        C(cylr, (sx * .26, 0, .45), .042, .3, JC, verts=14, bev=0, l=.008)
        C(sphere, (sx * .26, 0, .27), .062, (1, 1, 1), SKIN, l=.008)
        arms.append(sh); L.P[0] = inner
    head = empty(name + "_head", (0, 0, .66), inner); L.P[0] = head
    hc = Vector((0, 0, .96)); r = .3
    C(sphere, hc, r, (1, .96, .95), SKIN, l=.012)
    return dict(root=root, inner=inner, head=head, arms=arms, hc=hc, r=r, s=s)
def toon_end(d, loc):
    L.P[0] = None; d["inner"].scale = (d["s"],) * 3; d["root"].location = loc; bpy.context.view_layer.update()
def flocke(loc):
    d = toon("flocke", "#d22a26", "#fbfbf6", 1.0, collar="#1f8a48"); hc, r = d["hc"], d["r"]
    face(hc, r, brow="#e9e4da", ears="elf", stache="#f6f2ea")
    RED = clay("red", "#d22a26", .6)
    hat = C(cone, hc + Vector((0, 0, .59)), .25, .02, .8, RED, verts=32)
    bd = hat.modifiers.new("bend", "SIMPLE_DEFORM"); bd.deform_method = 'BEND'; bd.angle = -1.0; bd.deform_axis = 'X'
    C(torus, hc + Vector((0, 0, .19)), .24, .06, FUR)
    C(sphere, hc + Vector((0, .36, .84)), .08, (1, 1, 1), FUR)
    L.P[0] = d["inner"]; C(rbox, (.13, -.17, .5), (.1, .03, .28), clay("scarf", "#1f8a48", .65), bev=.5)
    C(rbox, (0, -.163, .25), (.47, .02, .06), FUR, bev=.5, l=.006)
    toon_end(d, loc); return dict(root=d["root"], head=d["head"], arms=d["arms"])
COLS = ["#2f6fd0", "#f08a20", "#7f3fd0", "#16a58a", "#ea3f6a", "#4fa83a", "#d84a2a", "#3a4fd0"]
def villager(loc, k):
    d = toon("v%d" % k, COLS[k % len(COLS)], "#fbfbf6" if k % 2 else "#f2c23a", .82); hc, r = d["hc"], d["r"]
    hcol = HAIRC[k % len(HAIRC)]; H = clay("hair" + hcol, hcol, .75)
    face(hc, r, brow=hcol if k % 4 != 1 else "#4a2a18", stache=(hcol if k % 3 == 0 else None))
    v = k % 4
    if v == 0:   # Haarbueschel wie Referenz
        for a, b, c, rr in ((0, -.12, .96, .1), (-.1, -.04, .98, .09), (.1, -.06, .97, .09), (0, .08, 1.0, .1)):
            C(sphere, hc + Vector((a * r * 2.5, b * r * 2.5, (c - .66) * r * 2.7)), rr * 1.0, (1, 1, .7), H)
    elif v == 1:  # Muetze mit Bommel
        bc = clay("vh%d" % k, COLS[(k + 3) % len(COLS)])
        C(sphere, hc + Vector((0, .01, .165)), r * 1.0, (1.0, 1.0, .72), bc); C(torus, hc + Vector((0, 0, .16)), .26, .05, FUR)
        C(sphere, hc + Vector((0, 0, .4)), .07, (1, 1, 1), FUR)
    elif v == 2:  # Ohrenschuetzer + Dutt
        C(sphere, hc + Vector((0, .05, r * .55)), r * .88, (1, 1, .55), H); C(sphere, hc + Vector((0, .12, r * 1.0)), .1, (1, 1, 1), H)
        mc = clay("muff%d" % k, COLS[(k + 2) % len(COLS)], .9)
        C(torus, hc, r * 1.02, .018, mc, rot=(0, math.pi / 2, 0))
        for sx in (-1, 1): C(sphere, hc + Vector((sx * r * 1.0, 0, 0)), .085, (.7, 1, 1), mc)
    else:        # Locken
        for j in range(9):
            a = j / 9 * 2 * math.pi; C(sphere, hc + Vector((math.cos(a) * r * .62, math.sin(a) * r * .62 + .04, r * .62)), .1, (1, 1, .85), H)
        C(sphere, hc + Vector((0, .04, r * .8)), .14, (1, 1, .7), H)
    toon_end(d, loc); return d["root"]
def popin(o, fr, s=1.0):
    kf(o, "scale", 0, Vector((.001,) * 3)); kf(o, "scale", fr, Vector((.001,) * 3)); kf(o, "scale", fr + 2, Vector((s * 1.18,) * 3)); kf(o, "scale", fr + 4, Vector((s,) * 3))
def popout(o, fr, s=1.0):
    kf(o, "scale", fr, Vector((s,) * 3)); kf(o, "scale", fr + 3, Vector((.001,) * 3))

FL = flocke((-6, 1.0, 0))
# Schlitten
SLED = empty("sled", (0, 0, 0)); L.P[0] = SLED
for sx in (-1, 1): C(rbox, (sx * .28, 0, .05), (.06, 1.1, .06), clay("runner", "#b8372e"), bev=.6)
for k in range(5): C(rbox, (0, -.4 + k * .2, .17), (.7, .14, .05), WOOD, bev=.4)
L.P[0] = None; SLED.location = (-6, 1.6, 0)
# Bewohner (Regeln: "jeder Follower")
VIL = [villager((1.2 + k * .65, 2.2 + (k % 2) * .45, 0), k) for k in range(5)]
# Dorfkasse + Goldtaler
CHEST = empty("chest", (0, 0, 0)); L.P[0] = CHEST
C(rbox, (0, 0, .22), (.8, .55, .44), clay("chestw", "#8a5a34"), bev=.3); C(rbox, (0, -.28, .22), (.82, .04, .1), clay("band", "#e0b83a", .4), bev=.3)
text("DORFKASSE", (0, -.29, .26), .085, clay("chlab", "#fbe9b0", .5), extrude=.01)
L.P[0] = None; CHEST.location = (-.3, 2.0, 0)
GOLD = clay("gold", "#f2c23a", .35, 0)
COINS = [cylr((-.3 + rnd.uniform(-.2, .2), 2.0, 2.2), .1, .03, GOLD, rot=(math.pi / 2, 0, 0), verts=20, bev=0) for k in range(7)]
# Traumdorf (Ziel bis Heiligabend)
WARM = clay("win", "#ffd27a", .4, 0, emis="#ffb74a", es=6)
DREAM = []
def house(x, y, col, roof, w=1.0, h=.9):
    r = empty("h", (0, 0, 0)); L.P[0] = r
    C(rbox, (0, 0, h / 2), (w, w * .9, h), clay("hw" + col, col), bev=.15)
    C(cone, (0, 0, h + .3), w * .82, .02, .6, clay("hr" + roof, roof), verts=4, rot=(0, 0, math.pi / 4))
    C(rbox, (0, -w * .46, h * .45), (w * .26, .04, w * .26), WARM, bev=.3); C(rbox, (0, -w * .47, h * .18), (w * .2, .04, h * .36), clay("door", "#6b3e22"), bev=.3)
    L.P[0] = None; r.location = (x, y, 0); DREAM.append(r)
for x, y, c, rf in ((-3.0, 7.5, "#e8b06a", "#b8372e"), (-1.4, 9, "#f2d9b0", "#2f6b62"), (1.6, 9, "#d9a06a", "#7a3a8a"), (3.2, 7.5, "#f0c48a", "#b8372e"), (0, 11.5, "#e8c08a", "#3e5a8a")):
    house(x, y, c, rf)
TR = empty("dtree", (0, 0, 0)); L.P[0] = TR
C(cylr, (0, 0, .3), .15, .6, TRK, verts=12, bev=0)
for k in range(4): C(cone, (0, 0, .7 + k * .7), 1.3 - k * .27, .02, 1.1, PINE[k % 2], verts=28)
C(sphere, (0, 0, 3.35), .18, (1, 1, 1), clay("star", "#ffd84a", .3, 0, emis="#ffcf3a", es=8))
for k in range(26):
    a = k * 2.4; z = .8 + (k / 26) * 2.4; r = (1.25 - (z - .7) * .36)
    sphere((math.cos(a) * r, math.sin(a) * r, z), .07, (1, 1, 1), clay("bulb%d" % (k % 4), ["#ff5a4a", "#ffd84a", "#5ab8ff", "#7ee08a"][k % 4], .3, 0, emis=["#ff5a4a", "#ffd84a", "#5ab8ff", "#7ee08a"][k % 4], es=5))
L.P[0] = None; TR.location = (0, 8.5, 0); DREAM.append(TR)
# Abstimmungs-Modelle auf Sockeln: A Lebkuchen-Baeckerei, B Weihnachtsbaum
PED = clay("ped", "#e9e2d6", .6)
def pedestal(x, lab):
    r = empty("ped" + lab, (0, 0, 0)); L.P[0] = r
    C(cylr, (0, 0, .25), .55, .5, PED, verts=32, bev=.2)
    text(lab, (0, -.56, .26), .26, clay("lab" + lab, "#d22a26", .5), extrude=.03)
    L.P[0] = None; r.location = (x, 3.4, 0); return r
PEDS = [pedestal(-1.1, "A"), pedestal(1.1, "B")]
GB = empty("gb", (0, 0, 0)); L.P[0] = GB
GING = clay("ging", "#b8743a", .6); ICE = clay("icing", "#fbfbf6", .5, .1)
C(rbox, (0, 0, .25), (.55, .5, .5), GING, bev=.2); C(cone, (0, 0, .62), .5, .02, .35, GING, verts=4, rot=(0, 0, math.pi / 4))
for z in (.02, .5): C(rbox, (0, -.255, z), (.56, .03, .05), ICE, bev=.5)
for k, c in enumerate(("#ff5a4a", "#7ee08a", "#5ab8ff")): sphere((-.15 + k * .15, -.27, .35), .045, (1, .6, 1), clay("candy%d" % k, c, .3))
C(rbox, (0, -.26, .14), (.12, .03, .22), clay("door", "#6b3e22"), bev=.3)
L.P[0] = None; GB.location = (-1.1, 3.4, .5)
MT = empty("mt", (0, 0, 0)); L.P[0] = MT
C(cylr, (0, 0, .08), .06, .16, TRK, verts=10, bev=0)
for k in range(3): C(cone, (0, 0, .22 + k * .22), .4 - k * .09, .02, .35, PINE[k % 2], verts=20)
C(sphere, (0, 0, .92), .07, (1, 1, 1), clay("star", "#ffd84a"))
for k in range(9): sphere((math.cos(k * 2.2) * (.32 - k * .025), math.sin(k * 2.2) * (.32 - k * .025), .25 + k * .07), .03, (1, 1, 1), clay("bulb%d" % (k % 4), "#ff5a4a"))
L.P[0] = None; MT.location = (1.1, 3.4, .5)

# ===================================================== SCHNEEFALL (Partikel)
bpy.ops.mesh.primitive_plane_add(size=26, location=(0, 6, 9)); em = bpy.context.active_object; em.name = "snowemit"
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=.035, location=(0, 0, -50)); flake = bpy.context.active_object; flake.data.materials.append(clay("flake", "#ffffff", .8, 0, emis="#ffffff", es=.6))
ps = em.modifiers.new("snow", "PARTICLE_SYSTEM").particle_system.settings
ps.count = 2600; ps.frame_start = -200; ps.frame_end = F(DUR); ps.lifetime = 200; ps.normal_factor = -.6; ps.factor_random = .2
ps.effector_weights.gravity = .02; ps.brownian_factor = .25; ps.render_type = 'OBJECT'; ps.instance_object = flake; ps.particle_size = 1; ps.size_random = .6
em.show_instancer_for_render = False

# ===================================================== LICHT + WELT
W = bpy.data.worlds.new("w"); S.world = W; W.use_nodes = True; BG = W.node_tree.nodes["Background"]
BG.inputs[0].default_value = hexc("#8fbfea"); BG.inputs[1].default_value = .75
sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 4.2; sun.angle = math.radians(14); sun.color = (1, .95, .88)
so = bpy.data.objects.new("sun", sun); L.link(so); so.rotation_euler = (math.radians(52), 0, math.radians(-35))
def area(name, loc, tgt, e, size, col):
    l = bpy.data.lights.new(name, "AREA"); l.energy = e; l.size = size; l.color = col
    o = bpy.data.objects.new(name, l); L.link(o); o.location = Vector(loc); d = Vector(tgt) - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return l
fill = area("fill", (-4, -6, 5), (0, 3, .5), 350, 8, (.85, .92, 1))
lamp = bpy.data.lights.new("lantern", "POINT"); lamp.energy = 0; lamp.color = (1, .7, .4); lamp.shadow_soft_size = .3
lo = bpy.data.objects.new("lantern", lamp); L.link(lo); lo.location = (.6, 1.4, 1.2)
def night(fr0, fr1):
    for fr, v in ((fr0 - 1, 0), (fr0 + 6, 1), (fr1, 1)):
        BG.inputs[0].default_value = [a + (b - a) * v for a, b in zip(hexc("#8fbfea"), hexc("#1d2a52"))]; BG.inputs[0].keyframe_insert("default_value", frame=fr)
        BG.inputs[1].default_value = .75 - .45 * v; BG.inputs[1].keyframe_insert("default_value", frame=fr)
        sun.energy = 4.2 - 4.0 * v; sun.keyframe_insert("energy", frame=fr); sun.color = (1 - .45 * v, .95 - .3 * v, .88 + .1 * v); sun.keyframe_insert("color", frame=fr)
        fill.energy = 350 - 180 * v; fill.keyframe_insert("energy", frame=fr)

# ===================================================== KAMERAS (Schnitte per Marker)
FOC = {}
def camera(name, lens=30, focus=None):
    c = bpy.data.cameras.new(name); c.lens = lens; c.sensor_width = 24; c.clip_end = 200
    if focus is not None:
        c.dof.use_dof = True; c.dof.aperture_fstop = 2.2; fo = empty(name + "_f", focus); c.dof.focus_object = fo; FOC[name] = fo
    o = bpy.data.objects.new(name, c); L.link(o); return o
def look(o, pos, tgt, frame):
    o.location = Vector(pos); d = Vector(tgt) - Vector(pos); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    o.keyframe_insert("location", frame=frame); o.keyframe_insert("rotation_euler", frame=frame)
def shot(i, cam):
    m = S.timeline_markers.new("s%d" % i, frame=CUT[i]); m.camera = cam
def wobble(obj, idx, f0, f1, amp, spd, base=0.0, step=1):
    for fr in range(f0, f1 + 1, step): kf(obj, "rotation_euler", fr, base + amp * math.sin((fr - f0) / FPS * spd), idx)

# 0 Hook: ein Bewohner ploppt direkt vor der Kamera aus dem Schnee
HV = villager((0, -1.2, 0), 9)
c0 = camera("c0", 40, (0, -1.2, .6)); look(c0, (.35, -3.6, .75), (0, -1.2, .6), CUT[0]); look(c0, (.25, -3.2, .72), (0, -1.2, .62), CUT[1]); shot(0, c0)
popin(HV, segf(0, .05)); wobble(HV, 2, segf(0, .1), CUT[1], .25, 7)
L.P[0] = HV; text("DU?", (0, -1.2 - .16, .45), .09, clay("du", "#d22a26", .5), extrude=.015); L.P[0] = None
popout(HV, CUT[1] - 1)
# 1 Leeres Tal, Flocke kommt mit dem Schlitten
c1 = camera("c1", 26, (0, 1.3, .5)); a0, a1 = CUT[1], CUT[2]
look(c1, (2.5, -7, 3.2), (-.5, 4, .6), a0); look(c1, (1.4, -5.6, 2.2), (-.2, 2.5, .6), a1); shot(1, c1)
arr = segf(1, .55)
for o, dx in ((FL["root"], 0), (SLED, 0)):
    kf(o, "location", a0, Vector((-7.5, 1.0 + (.6 if o is SLED else 0), 0))); kf(o, "location", arr, Vector((-.6 + dx, 1.0 + (.6 if o is SLED else 0), 0)))
kf(FL["root"], "location", arr + 4, Vector((0, .9, 0)))
wobble(FL["root"], 1, a0, arr, .08, 14)
# 2 Regeln: Bewohner ploppen auf, Taler fallen in die Kasse
c2 = camera("c2", 20, (1.6, 2.1, .5)); b0, b1 = CUT[2], CUT[3]
look(c2, (1.6, -3.0, 1.6), (1.6, 2.1, .55), b0); look(c2, (1.6, -2.6, 1.5), (1.6, 2.1, .55), b1); shot(2, c2)
for k, v in enumerate(VIL): popin(v, segf(2, .12 + k * .05)); wobble(v, 2, segf(2, .15 + k * .05), b1, .18, 5 + k)
popin(CHEST, segf(2, .38))
for k, cn in enumerate(COINS):
    t0 = segf(2, .45 + k * .04); kf(cn, "location", 0, Vector((cn.location.x, 2.0, 2.4))); kf(cn, "location", t0, Vector((cn.location.x, 2.0, 2.4)))
    kf(cn, "location", t0 + 4, Vector((cn.location.x, 2.0, .3))); kf(cn, "rotation_euler", t0, 0.0, 2); kf(cn, "rotation_euler", t0 + 4, 6.0, 2)
    kf(cn, "scale", 0, Vector((.001,) * 3)); kf(cn, "scale", t0 - 1, Vector((.001,) * 3)); kf(cn, "scale", t0, Vector((1,) * 3)); kf(cn, "scale", t0 + 4, Vector((1,) * 3)); kf(cn, "scale", t0 + 5, Vector((.001,) * 3))
for k, cn in enumerate(COINS): kf(cn, "location", 0, Vector((cn.location.x, 2.0, 2.4)))
# 3 Ziel: Traumdorf erscheint, verschwindet wieder
c3 = camera("c3", 24, (0, 8.5, 1.2)); d0, d1 = CUT[3], CUT[4]
look(c3, (0, -1.5, 3.4), (0, 8.5, 1.1), d0); look(c3, (0, .2, 3.0), (0, 8.5, 1.3), d1); shot(3, c3)
for k, o in enumerate(DREAM): popin(o, segf(3, .1 + k * .07)); popout(o, d1 - 2)
for v in VIL: popout(v, d0)
# 4 Nacht + Kaelte: Flocke zittert, Kasse leer
c4 = camera("c4", 34, (-.1, 1.4, .6)); e0, e1 = CUT[4], CUT[5]
look(c4, (.9, -2.4, 1.1), (-.1, 1.3, .6), e0); look(c4, (.6, -1.8, .95), (-.1, 1.3, .62), e1); shot(4, c4)
night(e0, e1)
kf(FL["root"], "location", e0, Vector((0, .9, 0)))
for fr in range(segf(4, .3), e1, 1): kf(FL["root"], "location", fr, Vector(((.02 if fr % 2 else -.02), .9, 0)))
for a in FL["arms"]: kf(a, "rotation_euler", segf(4, .28), 0.0, 1); kf(a, "rotation_euler", segf(4, .32), (-1.3 if a.location.x < 0 else 1.3), 1)
kf(CHEST, "location", e0, Vector((-.3, 2.0, 0))); kf(CHEST, "location", e0 + 1, Vector((.9, 1.9, 0)))
# 5 Abstimmung: Modelle A/B, Flocke dazwischen
c5 = camera("c5", 26, (0, 3.2, .7)); g0, g1 = CUT[5], CUT[6]
look(c5, (0, -1.6, 1.7), (0, 3.2, .75), g0); look(c5, (0, -1.1, 1.6), (0, 3.2, .78), g1); shot(5, c5)
kf(FL["root"], "location", g0, Vector((0, 2.6, 0)))
kf(SLED, "location", g0 - 1, Vector((-.6, 1.6, 0))); kf(SLED, "location", g0, Vector((-4.5, 3.5, 0))); kf(CHEST, "location", g0 - 1, Vector((.9, 1.9, 0))); kf(CHEST, "location", g0, Vector((3.5, 3.6, 0)))
popin(GB, segf(5, .12)); popin(MT, segf(5, .55)); popin(PEDS[0], segf(5, .08)); popin(PEDS[1], segf(5, .5))
wobble(FL["head"], 2, segf(5, .1), segf(5, .5), .0, 1, .45); wobble(FL["head"], 2, segf(5, .55), g1, .0, 1, -.45)
kf(GB, "rotation_euler", 0, 0.0, 2); kf(GB, "rotation_euler", g1, .8, 2); kf(MT, "rotation_euler", 0, 0.0, 2); kf(MT, "rotation_euler", g1, -.8, 2)
lamp.energy = 0; lamp.keyframe_insert("energy", frame=g0 - 1); lamp.energy = 60; lamp.keyframe_insert("energy", frame=g0)
# 6 Schluss: Flocke winkt, Kamera faehrt zurueck
c6 = camera("c6", 26, (0, 2.6, .6)); h0, h1 = CUT[6], CUT[7]
look(c6, (0, -.6, 1.2), (0, 2.6, .7), h0); look(c6, (0, -4.0, 2.6), (0, 3.0, .7), h1); shot(6, c6)
wobble(FL["arms"][1], 1, h0, h1, .5, 9, -2.4)
# Grundhaltung Kopf
kf(FL["head"], "rotation_euler", 0, 0.0, 2)

# ===================================================== RENDER
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'
S.cycles.samples = int(OPT.get("samples", 24)); S.cycles.use_denoising = True; S.cycles.adaptive_threshold = .05
try: S.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
S.cycles.max_bounces = 4; S.cycles.diffuse_bounces = 2; S.cycles.glossy_bounces = 1; S.cycles.transmission_bounces = 1
S.render.use_persistent_data = True
S.view_settings.view_transform = 'AgX'; S.view_settings.exposure = .4
try: S.view_settings.look = 'AgX - Punchy'
except Exception: pass
S.render.resolution_x = 1080; S.render.resolution_y = 1920; S.render.resolution_percentage = int(OPT.get("pct", 100))
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGB'
if "stills" in OPT:
    for f in [int(x) for x in OPT["stills"].split(",")]:
        S.frame_set(f); S.render.filepath = os.path.join(OUT, "w01_still_%04d.png" % f); bpy.ops.render.render(write_still=True); print("STILL", f)
elif "frames" in OPT:
    a, b = [int(x) for x in OPT["frames"].split("-")]
    S.frame_start = a; S.frame_end = min(b, F(DUR) - 1); S.render.filepath = os.path.join(OUT, "f_"); bpy.ops.render.render(animation=True); print("FRAMES", a, b)
print("CUTS", CUT, "END", F(DUR))
