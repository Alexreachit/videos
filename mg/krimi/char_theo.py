# Kommentar-Krimi "Nebelstein" – Hauptfigur Kommissar Theo (eigene Figur, keine Vorlage).
# v2: organische Formen aus Metaballs (Mantel+Aermel, Hose, Haare verschmelzen weich), keine Kegel+Subdivision mehr,
# kraeftige Farben (Standard-Farbraum), freigestellt mit Schattenfaenger -> wird spaeter auf Hintergrund gesetzt.
# Lauf: blender -b --factory-startup -P mg/krimi/char_theo.py -- <OUT> [preview]
import bpy, math, sys, os
from mathutils import Vector, Quaternion

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/out"]
OUT = ARGS[0]; PREVIEW = "preview" in ARGS
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [a]

MATS = {}
def mat(name, col, rough=.55, sss=0, sheen=0, coat=0, emis=None, es=0, metal=0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(col)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (1.0, .4, .25)
        b.inputs["Subsurface Scale"].default_value = .02
    if sheen: b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Sheen Tint"].default_value = (1, 1, 1, 1)
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = .12
    if emis:
        b.inputs["Emission Color"].default_value = hexc(emis); b.inputs["Emission Strength"].default_value = es
    MATS[name] = m; return m

ROOT = bpy.data.objects.new("Theo", None); sc.collection.objects.link(ROOT)
def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
def fin(o, m, sub=0, parent=ROOT):
    o.data.materials.append(m); smooth(o)
    if sub:
        s = o.modifiers.new("sub", "SUBSURF"); s.levels = sub; s.render_levels = sub
    if parent: o.parent = parent
    return o
def sphere(loc, r, scl=(1, 1, 1), m=None, rot=(0, 0, 0), seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2, rotation=rot)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m)
def torus(loc, R, r, m, rot=(0, 0, 0), scl=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=64, minor_segments=20)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m)
def rbox(loc, s, m, rot=(0, 0, 0), bev=.2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object; o.scale = s
    bv = o.modifiers.new("bev", "BEVEL"); bv.width = bev * .5; bv.segments = 6; bv.affect = 'EDGES'
    o.data.materials.append(m); smooth(o); o.parent = ROOT
    bpy.ops.object.shade_smooth()
    return o
def cylr(loc, r, depth, m, rot=(0, 0, 0), verts=48):  # Zylinder mit gerundeten Kanten
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object
    bv = o.modifiers.new("bev", "BEVEL"); bv.width = min(r, depth) * .3; bv.segments = 5; bv.limit_method = 'ANGLE'
    o.data.materials.append(m); o.parent = ROOT; bpy.ops.object.shade_smooth(); return o
def tube(pts, r, m, parent=ROOT):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 8; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new("tube", cu); sc.collection.objects.link(o); o.data.materials.append(m); o.parent = parent; return o

# ---------- Metaball-Helfer: sichtbarer Radius ~ 0.67 * radius (threshold .6, stiffness 2)
K = 1 / .67
def meta(name, m, elems, res=.012):
    mb = bpy.data.metaballs.new(name); mb.resolution = res; mb.render_resolution = res * .6; mb.threshold = .6
    for e in elems:
        t = e[0]; el = mb.elements.new(type=t)
        if t == 'BALL':
            _, co, r = e; el.co = co; el.radius = r * K
        elif t == 'ELLIPSOID':
            _, co, r, sz = e; el.co = co; el.radius = r * K; el.size_x, el.size_y, el.size_z = sz
        elif t == 'CAPSULE':  # von a nach b, sichtbarer Radius r
            _, a, b, r = e; a = Vector(a); b = Vector(b); d = b - a
            el.co = (a + b) / 2; el.radius = r * K; el.size_x = d.length / 2
            el.rotation = Vector((1, 0, 0)).rotation_difference(d.normalized())
    o = bpy.data.objects.new(name, mb); sc.collection.objects.link(o)
    for ob in sc.objects: ob.select_set(False)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.active_object; o.data.materials.clear(); o.data.materials.append(m); smooth(o)
    sm = o.modifiers.new("smooth", "CORRECTIVE_SMOOTH"); sm.iterations = 4; sm.scale = 1
    o.parent = ROOT; return o

SKIN = mat("skin", "#f6c7a1", .42, sss=.18)
COAT = mat("coat", "#e0a43a", .62, sheen=.35)
COATD = mat("coatd", "#b77a1e", .55, sheen=.25)
SCARF = mat("scarf", "#16838d", .7, sheen=.5)
HAT = mat("hat", "#33384a", .6, sheen=.45)
BAND = mat("band", "#16838d", .5)
PANTS = mat("pants", "#3b465f", .7, sheen=.3)
BOOT = mat("boot", "#5e3721", .32, coat=.5)
WHITE = mat("eyew", "#ffffff", .12, coat=.7)
IRIS = mat("iris", "#6b4220", .2, coat=.9)
PUPIL = mat("pupil", "#0c0e13", .1, coat=.9)
SHINE = mat("shine", "#ffffff", .1, emis="#ffffff", es=6)
HAIR = mat("hair", "#432616", .45, sheen=.35)
BROW = mat("brow", "#2c190d", .6)
MOUTH = mat("mouth", "#8a3530", .4)
GOLD = mat("gold", "#e9b84d", .25, metal=1)
LAMPM = mat("lampmetal", "#3b4150", .35, metal=.8)
GLOW = mat("glow", "#8ef5ff", .1, emis="#5ee7ff", es=20)
BLUSH = mat("blush", "#ff8f80", .6)

# ---------- Proportionen (3D-Cartoon, ~2,6 Koepfe hoch)
HZ = 1.33; HR = .30; HS = (1.0, .94, .96)
# Hose + Beine
meta("Legs", PANTS, [('CAPSULE', (-.095, 0, .13), (-.1, 0, .42), .072), ('CAPSULE', (.095, 0, .13), (.1, 0, .42), .072)])
for sx in (-1, 1):
    rbox((sx * .1, -.035, .06), (.15, .25, .12), BOOT, bev=.45)
# Mantel inkl. Aermel als eine weiche Form
SH_L = (-.2, 0, .97); SH_R = (.2, 0, .97)
EL_L = (-.29, 0, .78); EL_R = (.29, -.06, .79)
WR_L = (-.31, -.02, .62); WR_R = (.29, -.19, .66)
meta("Coat", COAT, [
    ('ELLIPSOID', (0, 0, .82), .2, (1.0, .78, 1.15)),
    ('ELLIPSOID', (0, 0, .58), .26, (1.0, .8, .75)),
    ('ELLIPSOID', (0, 0, .46), .28, (1.0, .82, .45)),
    ('BALL', SH_L, .1), ('BALL', SH_R, .1),
    ('CAPSULE', SH_L, EL_L, .072), ('CAPSULE', EL_L, WR_L, .066),
    ('CAPSULE', SH_R, EL_R, .072), ('CAPSULE', EL_R, WR_R, .066),
])
torus((0, 0, .655), .222, .026, COATD, scl=(1, .8, 1))                # Guertel
rbox((0, -.183, .655), (.075, .03, .065), GOLD, bev=.3)                # Schnalle
for sx in (-1, 1):
    for z in (.76, .88): sphere((sx * .075, -.158, z), .019, (1, .55, 1), COATD, seg=24)
tube([Vector((-.03, -.165, .99)), Vector((-.07, -.17, .86)), Vector((-.05, -.19, .70))], .012, COATD)  # Mantelkante
# Hochgeklappter Kragen + Schal
torus((0, 0, 1.03), .145, .045, COATD, scl=(1, .88, 1.15))
torus((0, 0, 1.08), .13, .055, SCARF, scl=(1, .9, 1))
meta("ScarfEnd", SCARF, [('CAPSULE', (.07, -.16, 1.03), (.09, -.2, .83), .045)])
# Haende (rundliche Cartoon-Haende)
sphere(WR_L, .062, (.95, .9, 1.1), SKIN); sphere((WR_L[0] + .035, WR_L[1] - .03, WR_L[2] + .01), .025, (1, 1, 1), SKIN, seg=24)
sphere(WR_R, .062, (1, 1, 1), SKIN)
# Laterne
L0 = Vector((WR_R[0] + .02, WR_R[1] - .02, WR_R[2] - .26))
tube([Vector(WR_R) + Vector((0, 0, -.02)), L0 + Vector((0, 0, .22))], .008, LAMPM)
cylr(L0 + Vector((0, 0, .17)), .055, .035, LAMPM)
sphere(L0 + Vector((0, 0, .195)), .03, (1, 1, .6), LAMPM, seg=24)
gl = sphere(L0 + Vector((0, 0, .09)), .052, (1, 1, 1.25), GLOW); gl.visible_shadow = False
for a in range(4):
    ang = a * math.pi / 2 + .4
    cylr(L0 + Vector((math.cos(ang) * .05, math.sin(ang) * .05, .09)), .007, .13, LAMPM, verts=12)
cylr(L0 + Vector((0, 0, .015)), .06, .03, LAMPM)
lamp = bpy.data.lights.new("lantern", "POINT"); lamp.energy = 30; lamp.color = (.45, .9, 1); lamp.shadow_soft_size = .04
lo = bpy.data.objects.new("lantern", lamp); lo.location = L0 + Vector((0, 0, .09)); lo.parent = ROOT; sc.collection.objects.link(lo)
# ---------- Kopf
sphere((0, 0, HZ - .27), .07, (1, 1, 1.2), SKIN)                              # Hals
sphere((0, 0, HZ), HR, HS, SKIN, seg=64)
def onhead(x, z, off=0.0):
    dx, dz = x / (HR * HS[0]), (z - HZ) / (HR * HS[2])
    y = -HR * HS[1] * math.sqrt(max(0, 1 - dx * dx - dz * dz))
    return Vector((x, y - off, z))
for sx in (-1, 1):
    sphere((sx * .292, .01, HZ - .02), .06, (.42, .75, 1), SKIN, seg=32)       # Ohren
    e = onhead(sx * .105, HZ + .0, -.035)
    sphere(e, .07, (1, .55, 1.2), WHITE, seg=40)
    sphere(e + Vector((-sx * .004, -.034, -.008)), .045, (1, .42, 1.1), IRIS, seg=32)
    sphere(e + Vector((-sx * .004, -.052, -.008)), .025, (1, .38, 1.1), PUPIL, seg=24)
    sphere(e + Vector((sx * .014, -.06, .026)), .012, (1, .5, 1), SHINE, seg=16)
    b = onhead(sx * .112, HZ + .12, -.008)
    tube([b + Vector((-sx * .048, 0, -.004 + (.014 if sx > 0 else 0))), b, b + Vector((sx * .048, .008, (.014 if sx < 0 else -.004)))], .015, BROW)
    sphere(onhead(sx * .175, HZ - .075, -.004), .036, (1, .28, .68), BLUSH, seg=24)
sphere(onhead(0, HZ - .05, .012), .038, (1, .9, .85), SKIN, seg=32)          # Nase
tube([onhead(-.058, HZ - .135, .004), onhead(.004, HZ - .148, .006), onhead(.062, HZ - .122, .004)], .009, MOUTH)
# Haare: eine weiche Masse + Strähnen vorne
hair = [('ELLIPSOID', (0, .05, HZ + .07), .3, (1.04, 1.0, .82))]
for i, x in enumerate([-.19, -.11, -.02, .07, .16, .22]):
    p = onhead(x, HZ + .155 - abs(x) * .25, -.02)
    hair.append(('BALL', tuple(p), .062 - .004 * (i % 2)))
for sx in (-1, 1): hair.append(('BALL', (sx * .25, .02, HZ + .06), .07))
meta("Hair", HAIR, hair, res=.01)
# ---------- Hut (Fedora)
HT = HZ + .21; TILT = (-.1, 0, .06)
sphere((0, -.01, HT), .41, (1, .95, .055), HAT, rot=TILT)                    # Krempe (abgeflacht, weich)
sphere((0, -.01, HT + .1), .225, (1, .93, .62), HAT, rot=TILT)               # Krone
torus((0, -.005, HT + .045), .222, .028, BAND, rot=TILT)
sphere((0, -.035, HT + .185), .12, (1.3, .55, .18), mat("hatdent", "#2a2e3d", .6), rot=TILT)  # Delle

# ---------- Schattenfaenger-Boden, Licht, Kamera
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0)); fl = bpy.context.active_object; fl.is_shadow_catcher = True
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = hexc("#e3ecf7"); w.node_tree.nodes["Background"].inputs[1].default_value = .6
def area(name, loc, size, energy, col, target=Vector((0, 0, .95))):
    l = bpy.data.lights.new(name, "AREA"); l.size = size; l.energy = energy; l.color = col
    o = bpy.data.objects.new(name, l); o.location = loc; sc.collection.objects.link(o)
    d = target - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
area("key", Vector((-2.4, -3.0, 3.3)), 3, 700, (1, .94, .86))
area("fill", Vector((3.0, -2.6, 1.6)), 3.5, 260, (.85, .92, 1))
area("rim", Vector((1.8, 2.6, 2.8)), 2, 900, (.75, .9, 1), Vector((0, 0, 1.2)))
area("rim2", Vector((-2.2, 2.2, 2.0)), 2, 450, (1, .9, .8), Vector((0, 0, 1.0)))
cam = bpy.data.cameras.new("cam"); co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48 if PREVIEW else 160; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

def shot(name, ang, dist=5.4, h=1.0, target=Vector((0, 0, .93)), lens=70, res=(1080, 1350)):
    s = .5 if PREVIEW else 1
    sc.render.resolution_x = int(res[0] * s); sc.render.resolution_y = int(res[1] * s); cam.lens = lens
    co.location = Vector((math.sin(ang) * dist, -math.cos(ang) * dist, h)); d = target - co.location; co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True); print("RENDER", name)
shot("theo_front", 0)
shot("theo_34", math.radians(35))
shot("theo_side", math.radians(90))
shot("theo_back", math.radians(180))
shot("theo_portrait", math.radians(18), dist=2.5, h=1.42, target=Vector((0, 0, 1.36)), lens=85, res=(1080, 1080))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "theo.blend"))
try: bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "theo.glb"), export_format='GLB')
except Exception as ex: print("GLB-Export fehlgeschlagen", ex)
print("FERTIG")
