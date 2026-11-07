# Nebelstein Folge 1 – "Der Uhrmacher". Baut alle Sets, Kameras (Schnitte per Marker), Animationen; rendert Stills oder Frame-Bereich.
# blender -b --factory-startup -P mg/krimi/ep01.py -- <OUT> stills=1,60,200   |  frames=0-120
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
T = json.load(open(os.path.join(HERE, "ep01_timing.json")))
FPS = T["fps"]; SEG = T["segments"]; DUR = T["duration"]
F = lambda t: int(round(t * FPS))
S.render.fps = FPS; S.frame_start = 0; S.frame_end = F(DUR) - 1
# Schnittpunkte: Shot i beginnt kurz vor Satz i
CUT = [0] + [F(SEG[i]["start"]) - 5 for i in range(1, len(SEG))] + [F(DUR)]
def segf(i, frac): return F(SEG[i]["start"] + frac * (SEG[i]["end"] - SEG[i]["start"]))

# ===================================================== STADT (Strasse, Turm, Platz)
street = mat("street", "#3a4256"); cob = L.cobble_mat()
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 22, 0)); o = bpy.context.active_object; o.scale = (6.4, 70, 1); o.data.materials.append(cob)
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

# ===================================================== FIGUREN
TH = L.build_theo(loc=(.6, 14, 0), rotz=0)
RES = []
for i, (x, y, c, hk) in enumerate([(-1.6, 24, "#7a5cc4", 0), (-.6, 25.2, "#3f8f6a", 1), (.5, 24.4, "#c25a4a", 2), (1.5, 25.4, "#3e6aa8", 3), (2.4, 24.2, "#a8743e", 0)]):
    RES.append(L.build_resident((x, y, 0), coat=c, hatkind=hk, rotz=0, dark=True))
SIGN = []
for i, (x, y, c, hk, rz) in enumerate([(-1.7, 31, "#7a5cc4", 0, .35), (-.6, 30.2, "#3f8f6a", 1, .15), (.6, 30.4, "#c25a4a", 2, -.1), (1.7, 31.2, "#3e6aa8", 3, -.35)]):
    SIGN.append(L.build_resident((x, y, 0), coat=c, hatkind=hk, rotz=rz, sign="DEIN NAME?"))

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

# ===================================================== KAMERAS + ANIMATION
def camera(name, lens=28):
    c = bpy.data.cameras.new(name); c.lens = lens; c.sensor_width = 24; c.clip_end = 300
    o = bpy.data.objects.new(name, c); L.link(o); return o
def look(o, frm, pos, tgt, frame):
    o.location = Vector(pos); d = Vector(tgt) - Vector(pos); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    o.keyframe_insert("location", frame=frame); o.keyframe_insert("rotation_euler", frame=frame)
cams = []
def shot(i, cam):
    m = S.timeline_markers.new("s%d" % i, frame=CUT[i]); m.camera = cam; cams.append(cam)
a0, a1 = CUT[0], CUT[1]
# 1 Strasse: Fahrt in den Nebel Richtung Uhrturm
c1 = camera("c1", 22); look(c1, 0, (0, -3, 1.7), (0, 40, 6), a0); look(c1, 0, (0, 3.5, 2.0), (0, 40, 7.5), a1); shot(0, c1); mist(a0, 4, 38)
# 2 Uhrturm: Zeiger laufen bis 0:13 und bleiben stehen
c2 = camera("c2", 26); b0, b1 = CUT[1], CUT[2]
look(c2, 0, (1.5, 33, 7.0), CF, b0); look(c2, 0, (.4, 37.5, 9.8), CF, b1); shot(1, c2); mist(b0, 3, 60)
stop = segf(1, .72)
for nm, a_from, a_to in (("min", 60, 78), ("hour", 5, 6.5)):
    pv = HANDS[nm]; kf(pv, "rotation_euler", b0, math.radians(a_from), 1); kf(pv, "rotation_euler", stop, math.radians(a_to), 1)
sec = HANDS["sec"]
for k, fr in enumerate(range(b0, stop, FPS // 2)): kf(sec, "rotation_euler", fr, math.radians(k * 6), 1)
kf(sec, "rotation_euler", stop, math.radians(((stop - b0) // (FPS // 2)) * 6 + 6), 1)
for fc in (sec.animation_data.action.fcurves):
    for kp in fc.keyframe_points: kp.interpolation = 'BACK'; kp.back = 2.5
# kurzer Ruck der Kamera beim Stehenbleiben
look(c2, 0, (.62, 36.7, 9.3), CF, stop); look(c2, 0, (.56, 36.75, 9.36), CF + Vector((0, 0, .06)), stop + 2); look(c2, 0, (.4, 37.5, 9.8), CF, b1)
# 3 Laden: von der Uhrenwand runter zum Kreide-Umriss, dann zur Tuer
c3 = camera("c3", 24); c0, c1f = CUT[2], CUT[3]
look(c3, 0, R0 + Vector((-.3, -2.6, 2.6)), R0 + Vector((0, 3, 2.1)), c0)
look(c3, 0, R0 + Vector((-.2, -2.4, 2.9)), C0 + Vector((0, 0, 0)), segf(2, .52))
look(c3, 0, R0 + Vector((.6, -2.0, 2.2)), KEY, c1f); shot(2, c3); mist(c0, 30, 200)
# 4 Theo kommt durch den Nebel, Laterne flackert
c4 = camera("c4", 40); d0, d1 = CUT[3], CUT[4]
R = TH["root"]; kf(R, "location", d0, Vector((.6, 15.5, 0))); kf(R, "location", d1, Vector((.6, 12.6, 0)))
for fc in R.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
for fr in range(d0, d1 + 1, 2):
    ph = (fr - d0) / FPS * 2 * math.pi * 1.6
    kf(R, "rotation_euler", fr, math.sin(ph) * .05, 1); kf(R, "rotation_euler", fr, math.sin(ph * .5) * .04, 2)
    TH["lantern"].rotation_euler = (math.sin(ph) * .25, math.sin(ph + 1) * .1, 0); TH["lantern"].keyframe_insert("rotation_euler", frame=fr)
    TH["head"].rotation_euler = (0, 0, math.sin(ph * .25) * .12); TH["head"].keyframe_insert("rotation_euler", frame=fr)
look(c4, 0, (1.0, 12.4, 1.25), (.6, 15.5, 1.15), d0); look(c4, 0, (1.0, 9.8, 1.25), (.6, 12.6, 1.2), d1); shot(3, c4); mist(d0, 2.5, 22)
flick0 = segf(3, .36); G = L.emis_input(TH["glow"])
G.default_value = 20; G.keyframe_insert("default_value", frame=d0); TH["lamp"].energy = 18; TH["lamp"].keyframe_insert("energy", frame=d0)
fr = flick0; r2 = random.Random(5)
while fr < d1:
    v = r2.choice([2, 35, 8, 28, 1, 40, 12]); G.default_value = v; G.keyframe_insert("default_value", frame=fr)
    TH["lamp"].energy = v * .9; TH["lamp"].keyframe_insert("energy", frame=fr); fr += r2.choice([2, 3, 4])
for lid in TH["lids"]:
    for f0 in (d0 + 20, segf(3, .8)):
        kf(lid, "scale", f0, .02, 2); kf(lid, "scale", f0 + 2, 1.25, 2); kf(lid, "scale", f0 + 5, .02, 2)
# 5 Silhouetten im Nebel, Augen leuchten auf
c5 = camera("c5", 32); e0, e1 = CUT[4], CUT[5]
look(c5, 0, (.4, 17.5, 1.3), (.4, 25, 1.0), e0); look(c5, 0, (.5, 21.4, 1.2), (.5, 24.4, 1.15), e1); shot(4, c5); mist(e0, 1.5, 14)
eyes_on = segf(4, .55)
for k, r in enumerate(RES):
    for ey in r["eyes"]:
        kf(ey, "scale", e0, Vector((0.001, .001, .001))); kf(ey, "scale", eyes_on + k * 2, Vector((0.001, .001, .001))); kf(ey, "scale", eyes_on + k * 2 + 4, Vector((1, .5, 1)))
# 6 Platz: Bewohner mit Schildern "DEIN NAME?" – Kamera kreist
c6 = camera("c6", 30); g0, g1 = CUT[5], CUT[6]
for k in range(5):
    t = k / 4; ang = math.radians(-25 + 50 * t)
    look(c6, 0, (math.sin(ang) * 5.2, 30.8 - math.cos(ang) * 5.2, 1.6 - .2 * t), (0, 30.8, .95), g0 + int((g1 - g0) * t))
shot(5, c6); mist(g0, 6, 30)
for k, r in enumerate(SIGN):
    for fr in range(g0, g1 + 1, 6): kf(r["root"], "location", fr, Vector((r["root"].location.x, r["root"].location.y, abs(math.sin((fr - g0) / FPS * 5 + k)) * .06)))
# 7 Hinweise: Taschenuhr -> Rabe -> Schluessel -> Totale
c7 = camera("c7", 35); h0, h1 = CUT[6], CUT[7]
look(c7, 0, PW + Vector((.0, -.9, .5)), PW, h0)
look(c7, 0, PW + Vector((.05, -.75, .4)), PW, segf(6, .30))
look(c7, 0, WN + Vector((1.7, -.6, -.2)), RAV.location + Vector((0, 0, .3)), segf(6, .40))
look(c7, 0, WN + Vector((1.5, -.5, -.25)), RAV.location + Vector((0, 0, .3)), segf(6, .52))
look(c7, 0, KEY + Vector((-1.1, -.6, .15)), KEY, segf(6, .60))
look(c7, 0, KEY + Vector((-1.0, -.45, .1)), KEY, segf(6, .72))
look(c7, 0, R0 + Vector((.2, -3.0, 2.3)), R0 + Vector((-.4, 1.2, 1.0)), segf(6, .82))
look(c7, 0, R0 + Vector((.2, -3.3, 2.4)), R0 + Vector((-.4, 1.2, 1.0)), h1)
shot(6, c7); mist(h0, 30, 200)
for c in cams:
    if c.animation_data:
        for fc in c.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if kp.interpolation != 'BACK': kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
for fc in W.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
# Rabe dreht den Kopf
kf(RAV, "rotation_euler", h0, -math.pi / 2, 2); kf(RAV, "rotation_euler", segf(6, .45), -math.pi / 2 + .5, 2)

# ===================================================== RENDER
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'
S.cycles.samples = int(OPT.get("samples", 28)); S.cycles.use_denoising = True
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
        S.frame_set(f); S.render.filepath = os.path.join(OUT, "still_%04d.png" % f); bpy.ops.render.render(write_still=True); print("STILL", f)
elif "frames" in OPT:
    a, b = [int(x) for x in OPT["frames"].split("-")]
    S.frame_start = a; S.frame_end = min(b, F(DUR) - 1); S.render.filepath = os.path.join(OUT, "f_"); bpy.ops.render.render(animation=True); print("FRAMES", a, b)
print("CUTS", CUT, "END", F(DUR))
