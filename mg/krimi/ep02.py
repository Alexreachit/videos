# Nebelstein Folge 2 – "Der Schluessel". Baut alle Sets, Kameras (Schnitte per Marker), Animationen; rendert Stills oder Frame-Bereich.
# blender -b --factory-startup -P mg/krimi/ep02.py -- <OUT> stills=1,60,200   |  frames=0-120
import bpy, sys, os, math, json, random
from mathutils import Vector, Euler
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nb_lib as L
from nb_lib import mat, hexc, sphere, rbox, cylr, cone, torus, tube, text, empty, kf, meta

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/out"]
OUT = ARGS[0]; os.makedirs(OUT, exist_ok=True)
OPT = dict(a.split("=", 1) for a in ARGS[1:] if "=" in a)
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
T = json.load(open(os.path.join(HERE, "ep02_timing.json")))
FPS = T["fps"]; SEG = T["segments"]; DUR = T["duration"]
F = lambda t: int(round(t * FPS))
S.render.fps = FPS; S.frame_start = 0; S.frame_end = F(DUR) - 1
# Schnittpunkte: Shot i beginnt kurz vor Satz i
CUT = [0] + [F(SEG[i]["start"]) - 5 for i in range(1, len(SEG))] + [F(DUR)]
def segf(i, frac): return F(SEG[i]["start"] + frac * (SEG[i]["end"] - SEG[i]["start"]))

# ===================================================== STADT (Strasse, Turm, Platz)
street = mat("street", "#3a4256"); cob = L.cobble_mat()
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 22, 0)); o = bpy.context.active_object; o.scale = (6.4, 70, 1); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(cob)
for sx in (-1, 1):
    rbox((sx * 3.6, 22, .08), (1.2, 70, .16), mat("curb", "#7d8496", .7), bev=.3)
rnd = random.Random(7)
WALLS = ["#e8d2b0", "#cfe0e8", "#f0c9b8", "#d9e6c9", "#e6d8f0", "#f4e3a8", "#c9d6f0"]
ROOFS = ["#a8443a", "#3e5a8a", "#5b4a7a", "#8a5a34", "#2f6b62"]
for sx in (-1, 1):
    y = -4
    i = 0
    while y < 38:
        w = rnd.uniform(3.0, 3.8); h = rnd.uniform(3.6, 6.2)
        L.house((sx * (4.2 + w * 0 + 2.0), y + w / 2, 0), w, 4.0, h, WALLS[(i * 3 + (sx > 0)) % len(WALLS)], ROOFS[(i + (sx > 0) * 2) % len(ROOFS)],
                rotz=(math.pi / 2 if sx < 0 else -math.pi / 2), seed=i * 13 + sx)
        y += w + .05; i += 1
for y in range(0, 40, 7):
    for sx in (-1, 1): L.streetlamp((sx * 3.3, y + (3.5 if sx > 0 else 0), 0), energy=70)
# Uhrturm
TW = Vector((0, 44, 0))
L.P[0] = None
rbox(TW + Vector((0, 0, 7)), (3.4, 3.4, 14), mat("tower", "#b9a68a", .8), bev=.05)
rbox(TW + Vector((0, 0, 14.3)), (3.8, 3.8, .6), mat("towertrim", "#8a7a64", .7), bev=.3)
cone(TW + Vector((0, 0, 16.4)), 2.7, .05, 3.8, mat("roof#3e5a8a", "#3e5a8a", .6), verts=4, rot=(0, 0, math.pi / 4))
CF = TW + Vector((0, -1.75, 11))
cylr(CF, 1.25, .12, mat("clockrim", "#d9b45a", .3, metal=.9), rot=(math.pi / 2, 0, 0))
cylr(CF + Vector((0, -.05, 0)), 1.12, .06, mat("clockface", "#fff4dc", .5, emis="#ffe9b8", es=2.5), rot=(math.pi / 2, 0, 0), bev=0)
for k in range(12):
    a = k / 12 * 2 * math.pi
    rbox(CF + Vector((math.sin(a) * .95, -.1, math.cos(a) * .95)), (.06, .02, .16 if k % 3 == 0 else .09), mat("ink", "#232030", .5), rot=(0, a, 0), bev=.3)
HANDS = {}
for nm, ln, wd in (("min", .85, .06), ("hour", .55, .09), ("sec", .9, .02)):
    pv = empty("hand_" + nm, CF + Vector((0, -.14 - .02 * len(HANDS), 0)))
    L.P[0] = pv
    rbox(pv.location + Vector((0, 0, ln / 2 - .08)), (wd, .02, ln), mat("hand" + nm, "#c23a2e" if nm == "sec" else "#232030", .4), bev=.3)
    L.P[0] = None; HANDS[nm] = pv
sphere(CF + Vector((0, -.2, 0)), .07, (1, .5, 1), mat("gold", "#e9b84d", .25, metal=1), seg=16)

# ===================================================== UHRMACHER-LADEN (Innenraum, x=100)
R0 = Vector((100, 0, 0))
wood = mat("wood", "#7a4e2e", .55); wood2 = mat("wood2", "#8c5a34", .55)
for i in range(12): rbox(R0 + Vector((-3 + i * .5 + .25, 0, -.05)), (.48, 7, .1), wood if i % 2 else wood2, bev=.2)
rbox(R0 + Vector((0, 3.1, 1.9)), (6.2, .2, 3.8), mat("wallpaper", "#2f5d55", .8), bev=0)
rbox(R0 + Vector((-3.1, 0, 1.9)), (.2, 6.2, 3.8), mat("wallpaper", "#2f5d55", .8), bev=0)
rbox(R0 + Vector((3.1, 0, 1.9)), (.2, 6.2, 3.8), mat("wallpaper", "#2f5d55", .8), bev=0)
rbox(R0 + Vector((0, 3.0, .45)), (6.2, .1, .9), mat("panel", "#5a3a26", .6), bev=.2)
# Uhrenwand: alle Uhren stehen auf 0:13
crnd = random.Random(3); CLK = []
for r in range(3):
    for c in range(6):
        x = -2.5 + c * 1.0 + crnd.uniform(-.1, .1); z = 1.4 + r * .75 + crnd.uniform(-.05, .05); rad = crnd.uniform(.2, .32)
        p = R0 + Vector((x, 2.95, z))
        col = ["#b0703a", "#d9b45a", "#6a3d24", "#c9c2b0", "#3e5a8a"][(r * 6 + c) % 5]
        if (r + c) % 3 == 0: rbox(p, (rad * 2.1, .14, rad * 2.4), mat("cb" + col, col, .5), bev=.3)
        else: cylr(p, rad + .05, .14, mat("cb" + col, col, .45, metal=.3), rot=(math.pi / 2, 0, 0))
        cylr(p + Vector((0, -.08, 0)), rad, .03, mat("clockface", "#fff4dc", .5, emis="#ffe9b8", es=2.5), rot=(math.pi / 2, 0, 0), bev=0)
        for nm, ln, ang in (("m", .8, 78), ("h", .5, 6.5)):
            a = math.radians(ang)
            rbox(p + Vector((math.sin(a) * rad * ln / 2, -.11, math.cos(a) * rad * ln / 2)), (.025, .01, rad * ln), mat("ink", "#232030", .5), rot=(0, a, 0), bev=.3)
        CLK.append(p)
# Standuhr
GC = R0 + Vector((2.3, 2.6, 0))
rbox(GC + Vector((0, 0, 1.2)), (.8, .5, 2.4), mat("gcwood", "#5a3220", .45, coat=.4), bev=.15)
cylr(GC + Vector((0, -.26, 1.9)), .28, .04, mat("clockface", "#fff4dc", .5), rot=(math.pi / 2, 0, 0), bev=0)
cylr(GC + Vector((0, -.28, 1.0)), .12, .02, mat("gold", "#e9b84d", .25, metal=1), rot=(math.pi / 2, 0, 0))
# Werkbank mit Taschenuhr
WB = R0 + Vector((-1.6, 1.9, 0))
rbox(WB + Vector((0, 0, .85)), (2.2, .9, .1), wood, bev=.3)
for sx in (-1, 1):
    for sy in (-1, 1): rbox(WB + Vector((sx * 1.0, sy * .35, .42)), (.08, .08, .84), wood, bev=.3)
PW = WB + Vector((.35, -.15, .93))
cylr(PW, .12, .035, mat("gold", "#e9b84d", .25, metal=1), bev=.4)
cylr(PW + Vector((0, 0, .02)), .1, .01, mat("clockface", "#fff4dc", .5, emis="#ffe9b8", es=1.5), bev=0)
torus(PW + Vector((0, .135, 0)), .03, .008, mat("gold", "#e9b84d", .25, metal=1), rot=(math.pi / 2, 0, 0))
for ln, ang, wd in ((.08, 78, .01), (.05, 6.5, .014)):
    a = math.radians(ang); rbox(PW + Vector((math.sin(a) * ln / 2, math.cos(a) * ln / 2, .03)), (wd, ln, .005), mat("ink", "#232030", .5), rot=(0, 0, -a), bev=0)
for i in range(5): cylr(WB + Vector((-.6 + i * .12, .2, .92)), .012, .1, mat("tool", "#9aa3b0", .3, metal=.9), rot=(math.pi / 2, 0, i * .4), bev=0, verts=8)
lampw = mat("deskglow", "#ffd99a", .3, emis="#ffc56a", es=8)
cylr(WB + Vector((-.8, .2, 1.25)), .14, .1, lampw); cylr(WB + Vector((-.8, .2, 1.05)), .015, .4, mat("pole", "#232a36", .4, metal=.6), bev=0)
dl = bpy.data.lights.new("desk", "POINT"); dl.energy = 40; dl.color = (1, .8, .5); dlo = bpy.data.objects.new("desk", dl); L.link(dlo); dlo.location = WB + Vector((-.8, .1, 1.15))
# Tuer rechts mit Schluessel von innen
DR = R0 + Vector((3.0, -.8, 0))
rbox(DR + Vector((0, 0, 1.1)), (.1, 1.0, 2.2), mat("door", "#5a3a2a", .5), bev=.2)
rbox(DR + Vector((-.06, .3, 1.05)), (.04, .1, .16), mat("gold", "#e9b84d", .25, metal=1), bev=.3)
KEY = DR + Vector((-.14, .3, 1.05))
L.P[0] = empty("key", KEY)
cylr(KEY, .01, .12, mat("keym", "#c9a24a", .3, metal=.9), rot=(0, math.pi / 2, 0), bev=0, verts=12)
torus(KEY + Vector((-.09, 0, 0)), .035, .01, mat("keym", "#c9a24a", .3, metal=.9), rot=(0, math.pi / 2, 0))
L.P[0] = None
# Fenster links mit Rabe auf der Fensterbank
WN = R0 + Vector((-3.0, -.5, 1.6))
rbox(WN, (.12, 1.3, 1.3), mat("frame", "#3a2e2a", .6), bev=.2)
rbox(WN + Vector((.02, 0, 0)), (.1, 1.15, 1.15), mat("night", "#2a4a7a", .3, emis="#3d6aa8", es=1.6), bev=0)
rbox(WN + Vector((.25, 0, -.68)), (.5, 1.4, .08), wood, bev=.3)
RAV = L.raven(WN + Vector((.25, 0, -.64)), rotz=-math.pi / 2, scale=1.6)
# Kreide-Umriss auf dem Boden (nicht blutig)
chalk = mat("chalk", "#ffffff", .9, emis="#ffffff", es=1.2)
C0 = R0 + Vector((.3, .2, .012))
pts = [(0, .95), (.18, .9), (.22, .72), (.15, .62), (.45, .55), (.62, .28), (.55, .24), (.3, .42), (.22, .1), (.35, -.4), (.42, -.85), (.28, -.88),
       (.12, -.45), (0, -.15), (-.12, -.45), (-.3, -.9), (-.44, -.86), (-.35, -.4), (-.22, .12), (-.32, .45), (-.6, .34), (-.65, .4), (-.45, .6), (-.15, .62), (-.22, .72), (-.18, .9), (0, .95)]
tube([C0 + Vector((x * 1.2, y * 1.2, 0)) for x, y in pts], .018, chalk)
# Licht im Laden
moon = bpy.data.lights.new("moon", "AREA"); moon.energy = 300; moon.size = 1.2; moon.color = (.55, .7, 1)
mo = bpy.data.objects.new("moon", moon); L.link(mo); mo.location = WN + Vector((.4, 0, .2)); mo.rotation_euler = (0, -math.pi / 2, 0)
amb = bpy.data.lights.new("shopamb", "AREA"); amb.energy = 420; amb.size = 5; amb.color = (.75, .85, 1)
ao = bpy.data.objects.new("shopamb", amb); L.link(ao); ao.location = R0 + Vector((0, -1, 3.6))
def arealight(name, pos, tgt, energy, size, col):
    l = bpy.data.lights.new(name, "AREA"); l.energy = energy; l.size = size; l.color = col
    o = bpy.data.objects.new(name, l); L.link(o); o.location = Vector(pos); d = Vector(tgt) - Vector(pos); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
arealight("towerkey", (2, 36, 6), CF, 900, 4, (.75, .85, 1))
arealight("theokey", (-1.2, 10.6, 2.6), (.6, 13.8, 1.1), 260, 2.5, (1, .9, .78))
arealight("theorim", (2.2, 17.5, 2.6), (.6, 14, 1.2), 380, 2, (.6, .8, 1))
arealight("squarekey", (0, 26.5, 3.2), (0, 31, 1), 650, 4, (1, .85, .65))
arealight("resrim", (0, 28, 4), (0, 25, 1), 120, 3, (.6, .75, 1))
# ===================================================== WELT, NEBEL, LICHT
W = bpy.data.worlds.new("w"); S.world = W; W.use_nodes = True
bg = W.node_tree.nodes["Background"]; bg.inputs[0].default_value = hexc("#2f5288"); bg.inputs[1].default_value = 1.0
moonS = bpy.data.lights.new("moonsun", "SUN"); moonS.energy = 1.4; moonS.color = (.6, .72, 1); moonS.angle = .2
ms = bpy.data.objects.new("moonsun", moonS); L.link(ms); ms.rotation_euler = (math.radians(55), 0, math.radians(200))
S.view_layers[0].use_pass_mist = True
W.mist_settings.falloff = 'QUADRATIC'
def mist(frame, start, depth):
    W.mist_settings.start = start; W.mist_settings.depth = depth
    W.mist_settings.keyframe_insert("start", frame=frame); W.mist_settings.keyframe_insert("depth", frame=frame)
# Kompositor: Nebel aus Mist-Pass + Glow
S.use_nodes = True; nt = S.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
rl = nt.nodes.new("CompositorNodeRLayers"); comp = nt.nodes.new("CompositorNodeComposite")
mix = nt.nodes.new("CompositorNodeMixRGB"); mix.blend_type = 'MIX'; mix.inputs[2].default_value = hexc("#9fb4d8")
mv = nt.nodes.new("CompositorNodeMath"); mv.operation = 'MULTIPLY'; mv.inputs[1].default_value = .85
nt.links.new(rl.outputs["Mist"], mv.inputs[0]); nt.links.new(mv.outputs[0], mix.inputs[0]); nt.links.new(rl.outputs["Image"], mix.inputs[1])
gl = nt.nodes.new("CompositorNodeGlare"); gl.glare_type = 'FOG_GLOW'; gl.threshold = .9; gl.size = 7; gl.mix = -.55
nt.links.new(mix.outputs[0], gl.inputs[0])
vig = nt.nodes.new("CompositorNodeEllipseMask"); vig.width = .95; vig.height = .7
blur = nt.nodes.new("CompositorNodeBlur"); blur.size_x = 200; blur.size_y = 200; blur.use_relative = False
nt.links.new(vig.outputs[0], blur.inputs[0])
vm = nt.nodes.new("CompositorNodeMixRGB"); vm.blend_type = 'MULTIPLY'; vm.inputs[0].default_value = 1
inv = nt.nodes.new("CompositorNodeMixRGB"); inv.blend_type = 'MIX'; inv.inputs[1].default_value = hexc("#6f7f9c"); inv.inputs[2].default_value = (1, 1, 1, 1)
nt.links.new(blur.outputs[0], inv.inputs[0]); nt.links.new(gl.outputs[0], vm.inputs[1]); nt.links.new(inv.outputs[0], vm.inputs[2])
nt.links.new(vm.outputs[0], comp.inputs[0])

# ===================================================== NEU IN FOLGE 2: Schluesselbrett, Kratzer, Fingerabdruecke, tickende Standuhr
L.P[0] = None
# Kratzer am Schluessel (leuchten auf, wenn der Assistent sie entdeckt)
SCR = mat("scratch", "#ffffff", .2, emis="#bff6ff", es=0)
for k, (dx, dz, a) in enumerate(((-.02, .004, .3), (.0, -.003, -.25), (.025, .002, .5))):
    rbox(KEY + Vector((dx, -.0105, dz)), (.022, .002, .0016), SCR, rot=(0, a, 0), bev=0)
# Schluesselbrett an der rechten Wand, ein Haken leer
KB = R0 + Vector((2.96, .75, 1.55))
rbox(KB, (.04, .95, .32), mat("kbwood", "#6a4026", .5, coat=.3), bev=.2)
keym = mat("keym", "#c9a24a", .3, metal=.9)
for k in range(5):
    hy = -.36 + k * .18
    cylr(KB + Vector((-.05, hy, .06)), .008, .08, mat("tool", "#9aa3b0", .3, metal=.9), rot=(0, math.pi / 2, 0), bev=0, verts=8)
    if k == 2:   # leer: heller Staubrand, wo der Schluessel hing
        rbox(KB + Vector((-.022, hy, -.05)), (.004, .05, .17), mat("dustmark", "#d9c9a8", .9), bev=.3)
        continue
    torus(KB + Vector((-.06, hy, .02)), .025, .006, keym, rot=(0, math.pi / 2, 0))
    cylr(KB + Vector((-.06, hy, -.06)), .007, .13, keym, bev=0, verts=10)
    rbox(KB + Vector((-.06, hy + .015, -.11)), (.01, .02, .025), keym, bev=.2)
# Standuhr bekommt echte Zeiger (steht auf 0:13) + Ziffernstriche
GCF = GC + Vector((0, -.29, 1.9))
for k in range(12):
    a = k / 12 * 2 * math.pi
    rbox(GCF + Vector((math.sin(a) * .23, -.005, math.cos(a) * .23)), (.012, .006, .04 if k % 3 == 0 else .025), mat("ink", "#232030", .5), rot=(0, a, 0), bev=0)
GH = {}
for nm, ln, wd, ang in (("min", .21, .014, 78), ("hour", .14, .02, 6.5), ("sec", .22, .006, 0)):
    pv = empty("gch_" + nm, GCF + Vector((0, -.012 - .004 * len(GH), 0))); L.P[0] = pv
    rbox(pv.location + Vector((0, 0, ln / 2 - .02)), (wd, .004, ln), mat("hand" + nm, "#c23a2e" if nm == "sec" else "#232030", .4), bev=0)
    L.P[0] = None; pv.rotation_euler = (0, math.radians(ang), 0); GH[nm] = pv
# Fingerabdruecke auf dem Glas der Standuhr (konzentrische Ringe, leuchten im blauen Licht)
FP = mat("fingerprint", "#f6efdc", .5, emis="#5ee7ff", es=0)
for (cx, cz, rt) in ((-.085, .07, .3), (.075, -.06, -.4)):
    for j in range(7):
        torus(GCF + Vector((cx, -.03, cz)), .008 + j * .0085, .0016, FP, rot=(math.pi / 2, rt, 0), scl=(1, 1.35, 1))
# Staubwolke beim Bestaeuben
DUST = []; drnd = random.Random(11)
dm = mat("dust", "#f2efe6", .9, emis="#ffffff", es=.6)
for k in range(36):
    s = sphere(GCF + Vector((drnd.uniform(-.05, .05), -.06, drnd.uniform(-.05, .05))), drnd.uniform(.004, .009), (1, 1, 1), dm, seg=8)
    DUST.append((s, Vector((drnd.uniform(-.35, .35), drnd.uniform(-.25, -.05), drnd.uniform(-.25, .3)))))
# blaues Laternenlicht an der Uhr
BL = bpy.data.lights.new("bluelamp", "POINT"); BL.energy = 0; BL.color = (.45, .9, 1); BL.shadow_soft_size = .05
blo = bpy.data.objects.new("bluelamp", BL); L.link(blo); blo.location = GCF + Vector((-.25, -.45, -.1))

# ===================================================== FIGUREN
def assistant(loc, rotz=0.0, sign=None):
    a = L.build_resident((0, 0, 0), coat="#2f8a6a", hat="#26303f", hatkind=1, rotz=0, sign=sign)
    L.P[0] = a["root"]
    gm = mat("magn", "#c9a24a", .3, metal=.9)
    cylr((.3, -.1, .58), .018, .2, mat("magh", "#5a3a26", .5), rot=(.4, 0, 0), bev=0, verts=10)
    torus((.3, -.15, .74), .07, .012, gm, rot=(math.pi / 2, 0, 0))
    cylr((.3, -.15, .74), .062, .005, mat("magglass", "#cfefff", .05, emis="#bfefff", es=.4), rot=(math.pi / 2, 0, 0), bev=0)
    torus((0, -.02, 1.02), .2, .045, mat("ascarf", "#e6c14a", .7, sheen=.5), scl=(1, .9, 1))   # gelber Schal = Erkennungszeichen
    L.P[0] = None
    a["root"].location = loc; a["root"].rotation_euler = (0, 0, rotz)
    return a
SQ = 30.5
NEW = [("LUCA_2006", -1.8, "#a8743e", 0), ("LIAN MX #7", -.6, "#3e6aa8", 2), ("BÜRGER NR. 4", .6, "#c25a4a", 3)]
RESN = [L.build_resident((x, SQ, 0), coat=c, hatkind=hk, rotz=0, sign=nm) for nm, x, c, hk in NEW]
AS1 = assistant((1.8, SQ, 0), sign="MTB+GAMING")
TH1 = L.build_theo(loc=(3.45, 29.35, 0), rotz=-1.2)
TH2 = L.build_theo(loc=R0 + Vector((.15, -.55, 0)), rotz=0)
AS2 = assistant(R0 + Vector((.95, -.5, 0)), rotz=-.55)
arealight("shopkey2", R0 + Vector((-.6, -2.4, 2.2)), R0 + Vector((.4, -.5, 1.2)), 140, 2, (1, .88, .72))


# ===================================================== KAMERAS + ANIMATION (Folge 2)
def camera(name, lens=28):
    c = bpy.data.cameras.new(name); c.lens = lens; c.sensor_width = 24; c.clip_end = 300
    o = bpy.data.objects.new(name, c); L.link(o); return o
def look(o, pos, tgt, frame):
    o.location = Vector(pos); d = Vector(tgt) - Vector(pos); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    o.keyframe_insert("location", frame=frame); o.keyframe_insert("rotation_euler", frame=frame)
cams = []
def shot(i, cam):
    m = S.timeline_markers.new("s%d" % i, frame=CUT[i]); m.camera = cam; cams.append(cam)
def place(obj, frame, loc, rotz=None):
    obj.location = Vector(loc); obj.keyframe_insert("location", frame=frame)
    if rotz is not None: obj.rotation_euler = (0, 0, rotz); obj.keyframe_insert("rotation_euler", frame=frame)
def jump(obj, frame, old, new, rz_old=None, rz_new=None):
    place(obj, frame - 1, old, rz_old); place(obj, frame, new, rz_new)
def popin(root, frame):
    kf(root, "scale", 0, Vector((.001, .001, .001))); kf(root, "scale", frame, Vector((.001, .001, .001)))
    kf(root, "scale", frame + 6, Vector((1.12, 1.12, 1.12))); kf(root, "scale", frame + 11, Vector((1, 1, 1)))
GLOW = L.emis_input(TH1["glow"])
def lantern(frame, v):
    GLOW.default_value = v; GLOW.keyframe_insert("default_value", frame=frame)
    for th in (TH1, TH2): th["lamp"].energy = v * .9; th["lamp"].keyframe_insert("energy", frame=frame)
lantern(0, 20)
def walk_wobble(th, f0, f1):
    R = th["root"]
    for fr in range(f0, f1 + 1, 2):
        ph = (fr - f0) / FPS * 2 * math.pi * 1.6
        th["lantern"].rotation_euler = (math.sin(ph) * .25, math.sin(ph + 1) * .1, 0); th["lantern"].keyframe_insert("rotation_euler", frame=fr)
        th["head"].rotation_euler = (0, 0, math.sin(ph * .25) * .12); th["head"].keyframe_insert("rotation_euler", frame=fr)

# 0 Titel: Strasse im Nebel Richtung Uhrturm
c0 = camera("c0", 22); look(c0, (0, -3, 1.7), (0, 40, 6), CUT[0]); look(c0, (0, 2.5, 1.9), (0, 40, 7.2), CUT[1]); shot(0, c0); mist(CUT[0], 4, 38)
# 1 Rueckblick: Uhrenwand -> Kreide-Umriss -> Tuer mit Schluessel
c1 = camera("c1", 24); a0, a1 = CUT[1], CUT[2]
look(c1, R0 + Vector((-.3, -2.6, 2.6)), R0 + Vector((0, 3, 2.1)), a0)
look(c1, R0 + Vector((-.2, -2.4, 2.9)), C0, segf(1, .45))
look(c1, R0 + Vector((.6, -2.0, 2.2)), KEY, a1); shot(1, c1); mist(a0, 30, 200)
# 2 Platz: vier neue Bewohner tauchen auf, MTB+GAMING geht zu Theo
c2 = camera("c2", 18); b0, b1 = CUT[2], CUT[3]
look(c2, (0, 24.6, 1.9), (0, SQ, 1.0), b0); look(c2, (0, 25.3, 1.8), (0, SQ, 1.0), segf(2, .5))
look(c2, (2.2, 26.0, 1.6), (2.9, 29.6, 1.05), segf(2, .7)); look(c2, (3.0, 26.5, 1.5), (3.0, 29.5, 1.0), b1); shot(2, c2); mist(b0, 4, 22)
for k, r in enumerate(RESN + [AS1]): popin(r["root"], segf(2, .12 + k * .08))
aw0, aw1 = segf(2, .66), segf(2, .9)
place(AS1["root"], aw0, (1.8, SQ, 0), 0); place(AS1["root"], aw0 + 6, (1.9, SQ - .3, .08), 1.0); place(AS1["root"], aw1, (2.6, 29.6, 0), 1.0)
# 3 Schluessel (Makro), dann Schluesselbrett mit leerem Haken
c3 = camera("c3", 60); d0, d1 = CUT[3], CUT[4]; dm = segf(3, .58)
look(c3, KEY + Vector((-.5, -.42, .08)), KEY, d0); look(c3, KEY + Vector((-.3, -.24, .04)), KEY + Vector((.02, 0, 0)), dm - 1)
look(c3, KB + Vector((-2.4, -.7, .15)), KB + Vector((0, .0, -.03)), dm); look(c3, KB + Vector((-1.9, -.5, .1)), KB + Vector((0, .0, -.03)), d1)
shot(3, c3); mist(d0, 30, 200)
SE = L.emis_input(SCR); SE.default_value = 0; SE.keyframe_insert("default_value", frame=segf(3, .28)); SE.default_value = 9; SE.keyframe_insert("default_value", frame=segf(3, .34))
# 4 Standuhr: Staub, blaues Licht, Fingerabdruecke leuchten auf
c4 = camera("c4", 45); e0, e1 = CUT[4], CUT[5]
look(c4, GCF + Vector((-.3, -1.05, -.05)), GCF, e0); look(c4, GCF + Vector((-.12, -.62, 0)), GCF, e1); shot(4, c4); mist(e0, 30, 200)
p0, p1 = segf(4, .02), segf(4, .32)
for s, dv in DUST:
    base = s.location.copy(); kf(s, "scale", 0, Vector((.001,) * 3)); kf(s, "scale", p0, Vector((.001,) * 3)); kf(s, "scale", p0 + 3, Vector((1,) * 3)); kf(s, "scale", p1, Vector((.001,) * 3))
    kf(s, "location", p0, base); kf(s, "location", p1, base + dv)
BL.energy = 0; BL.keyframe_insert("energy", frame=segf(4, .25)); BL.energy = 30; BL.keyframe_insert("energy", frame=segf(4, .33))
FE = L.emis_input(FP); FE.default_value = 0; FE.keyframe_insert("default_value", frame=segf(4, .34)); FE.default_value = 8; FE.keyframe_insert("default_value", frame=segf(4, .46))
BL.energy = 0; BL.keyframe_insert("energy", frame=e1 + 2)
# 5 Fluestern: Assistent beugt sich zu Theo
c5 = camera("c5", 24); g0, g1 = CUT[5], CUT[6]
look(c5, R0 + Vector((.5, -2.9, 1.4)), R0 + Vector((.5, -.5, 1.15)), g0); look(c5, R0 + Vector((.5, -2.45, 1.35)), R0 + Vector((.5, -.5, 1.15)), g1); shot(5, c5); mist(g0, 30, 200)
H2 = AS2["head"]; kf(H2, "rotation_euler", g0, Vector((0, 0, 0))); kf(H2, "rotation_euler", segf(5, .15), Vector((0, -.3, -.3)))
place(AS2["root"], g0, R0 + Vector((.95, -.5, 0)), -.55); place(AS2["root"], segf(5, .15), R0 + Vector((.78, -.45, 0)), -.9)
kf(TH2["head"], "rotation_euler", segf(5, .3), Vector((0, 0, 0))); kf(TH2["head"], "rotation_euler", segf(5, .5), Vector((0, 0, -.45)))
for lid in TH2["lids"]:
    kf(lid, "scale", segf(5, .55), .02, 2); kf(lid, "scale", segf(5, .55) + 2, 1.25, 2); kf(lid, "scale", segf(5, .55) + 5, .02, 2)
# 6 Theo geht an den Neuen vorbei – nur bei Lian flackert die Laterne kurz
c6 = camera("c6", 20); h0, h1 = CUT[6], CUT[7]
LIAN_X = -.6; tpass = segf(6, .55)
X0, X1 = -3.2, 1.4
jump(TH1["root"], h0, (3.45, 29.35, 0), (X0, 29.45, 0), -1.2, math.pi / 2)
place(TH1["root"], tpass, (LIAN_X, 29.45, 0)); place(TH1["root"], h1, (X1, 29.45, 0))
walk_wobble(TH1, h0, h1)
def theo_x(fr):
    if fr <= tpass: return X0 + (LIAN_X - X0) * (fr - h0) / max(1, tpass - h0)
    return LIAN_X + (X1 - LIAN_X) * (fr - tpass) / max(1, h1 - tpass)
for fr in range(h0, h1 + 1, 6):
    tx = theo_x(fr); look(c6, (tx - .3, 25.7, 1.55), (tx + .3, 30.0, 1.0), fr)
    for k, (nm, x, c, hk) in enumerate(NEW):
        kf(RESN[k]["head"], "rotation_euler", fr, Vector((0, 0, max(-.8, min(.8, math.atan2(tx - x, 1.2))))))
shot(6, c6); mist(h0, 5, 22)
jump(AS1["root"], h0, (2.6, 29.6, 0), (2.9, 28.6, 0), 1.0, 1.4)
lantern(tpass - 4, 20); r2 = random.Random(5); fr = tpass - 2
while fr < tpass + 14:
    lantern(fr, r2.choice([2, 35, 6, 30, 1])); fr += r2.choice([2, 3])
lantern(tpass + 15, 20)
# 7 Dunkler Laden: Standuhr tickt wieder los, dann geht die Laterne aus
c7 = camera("c7", 30); i0, i1 = CUT[7], CUT[8]
look(c7, R0 + Vector((-.5, -2.7, 1.6)), GCF, i0); look(c7, GC + Vector((-.35, -1.25, 1.85)), GCF, i1); shot(7, c7); mist(i0, 30, 200)
amb.energy = 420; amb.keyframe_insert("energy", frame=i0 - 1); amb.energy = 90; amb.keyframe_insert("energy", frame=i0)
amb.energy = 420; amb.keyframe_insert("energy", frame=i1)
dl.energy = 40; dl.keyframe_insert("energy", frame=i0 - 1); dl.energy = 0; dl.keyframe_insert("energy", frame=i0); dl.energy = 40; dl.keyframe_insert("energy", frame=i1)
tick0 = segf(7, .3); sec = GH["sec"]; n = 0
kf(sec, "rotation_euler", tick0 - 1, 0.0, 1)
for fr in range(tick0, i1, FPS // 2):
    n += 1; kf(sec, "rotation_euler", fr, math.radians(6 * n), 1)
for fc in sec.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation = 'BACK'; kp.back = 2.5
mj = segf(7, .85); mh = GH["min"]; kf(mh, "rotation_euler", mj - 1, math.radians(78), 1); kf(mh, "rotation_euler", mj + 2, math.radians(84), 1)
lantern(i1 - 12, 20); lantern(i1 - 9, 3); lantern(i1 - 7, 14); lantern(i1 - 4, 0)
# 8 Abstimmung: die drei Neuen auf dem Platz, Theo + Assistent davor
c8 = camera("c8", 18); k0, k1 = CUT[8], CUT[9]
look(c8, (.1, 24.5, 2.0), (.1, SQ - .5, 1.0), k0); look(c8, (.1, 25.3, 1.75), (.1, SQ - .5, 1.0), k1); shot(8, c8); mist(k0, 6, 26)
lantern(k0, 20)
jump(TH1["root"], k0, (X1, 29.45, 0), (1.25, 28.4, 0), math.pi / 2, math.pi * .85)
jump(AS1["root"], k0, (2.9, 28.6, 0), (2.0, 28.2, 0), 1.4, math.pi * .9)
for k, r in enumerate(RESN):
    for fr in range(k0, k1 + 1, 5): kf(r["root"], "location", fr, Vector((r["root"].location.x, SQ, abs(math.sin((fr - k0) / FPS * 4 + k * 1.3)) * .05)))
    kf(r["head"], "rotation_euler", k0, Vector((0, 0, 0)))
def hide(root, frame, hidden):
    for o in [root] + list(root.children_recursive):
        o.hide_render = hidden; o.keyframe_insert("hide_render", frame=frame)
for r in (TH2["root"], AS2["root"]):
    hide(r, 0, True); hide(r, CUT[5], False); hide(r, CUT[6], True); hide(r, CUT[7], False); hide(r, CUT[8], True)
# Interpolation
for c in cams:
    for fc in c.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
for o in (TH1["root"], AS1["root"], AS2["root"]):
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
for fc in W.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
for m in (GLOW,):
    pass

# ===================================================== RENDER
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'
S.cycles.samples = int(OPT.get("samples", 14)); S.cycles.use_denoising = True; S.cycles.adaptive_threshold = .05
try: S.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
S.cycles.max_bounces = 4; S.cycles.diffuse_bounces = 2; S.cycles.glossy_bounces = 2; S.cycles.transmission_bounces = 2; S.cycles.caustics_reflective = False; S.cycles.caustics_refractive = False
S.render.use_persistent_data = True
S.render.use_motion_blur = True; S.render.motion_blur_shutter = .45
S.view_settings.view_transform = 'AgX'; S.view_settings.exposure = 1.0
try: S.view_settings.look = 'AgX - Punchy'
except Exception: pass
S.render.resolution_x = 1080; S.render.resolution_y = 1920; S.render.resolution_percentage = int(OPT.get("pct", 100))
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGB'
if "stills" in OPT:
    for f in [int(x) for x in OPT["stills"].split(",")]:
        S.frame_set(f); S.render.filepath = os.path.join(OUT, "ep02_still_%04d.png" % f); bpy.ops.render.render(write_still=True); print("STILL", f)
elif "frames" in OPT:
    a, b = [int(x) for x in OPT["frames"].split("-")]
    S.frame_start = a; S.frame_end = min(b, F(DUR) - 1); S.render.filepath = os.path.join(OUT, "f_"); bpy.ops.render.render(animation=True); print("FRAMES", a, b)
print("CUTS", CUT, "END", F(DUR))

