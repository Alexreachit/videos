# Kommentar-Krimi "Nebelstein" – Hauptfigur Kommissar Theo (eigene Figur, keine Vorlage).
# Moderner 3D-Cartoon-Look: grosse Kopf-Proportionen, runde Formen (Subdivision), weiche Studio-Beleuchtung,
# Haut mit Subsurface, Stoffe mit Sheen. Ergebnis: Ansichten von vorne / 3/4 / Seite / hinten + Portrait + GLB.
# Lauf: blender -b --factory-startup -P mg/krimi/char_theo.py -- <OUT>
import bpy, math, sys, os
from mathutils import Vector

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/out"
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
        b.inputs["Subsurface Radius"].default_value = (1.0, .45, .3)
        b.inputs["Subsurface Scale"].default_value = .03
    if sheen: b.inputs["Sheen Weight"].default_value = sheen
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = .15
    if emis:
        b.inputs["Emission Color"].default_value = hexc(emis); b.inputs["Emission Strength"].default_value = es
    MATS[name] = m; return m

ROOT = bpy.data.objects.new("Theo", None); sc.collection.objects.link(ROOT)
def fin(o, m, sub=2, smooth=True, parent=ROOT):
    o.data.materials.append(m)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if sub:
        s = o.modifiers.new("sub", "SUBSURF"); s.levels = sub; s.render_levels = sub
    if parent: o.parent = parent
    return o
def sphere(loc, r, scl=(1, 1, 1), m=None, sub=1, rot=(0, 0, 0), seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2, rotation=rot)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m, sub)
def cyl(loc, r1, r2, depth, m, scl=(1, 1, 1), rot=(0, 0, 0), sub=2, verts=32):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m, sub)
def torus(loc, R, r, m, rot=(0, 0, 0), scl=(1, 1, 1), sub=1):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=48, minor_segments=16)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m, sub)
def cube(loc, s, m, rot=(0, 0, 0), sub=2, bevel=.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object; o.scale = s
    if bevel:
        bv = o.modifiers.new("bev", "BEVEL"); bv.width = bevel; bv.segments = 3
    return fin(o, m, sub)
def tube(pts, r, m, parent=ROOT):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new("tube", cu); sc.collection.objects.link(o); o.data.materials.append(m); o.parent = parent; return o

SKIN = mat("skin", "#f3c39f", .45, sss=.25)
COAT = mat("coat", "#d29a35", .6, sheen=.4)
COATD = mat("coatd", "#a8741f", .6, sheen=.3)
SCARF = mat("scarf", "#1c7a83", .7, sheen=.6)
HAT = mat("hat", "#2e3140", .55, sheen=.5)
BAND = mat("band", "#1c7a83", .5)
PANTS = mat("pants", "#3a4256", .7, sheen=.3)
BOOT = mat("boot", "#5b3622", .35, coat=.4)
WHITE = mat("eyew", "#fbfbfb", .15, coat=.6)
IRIS = mat("iris", "#5a3a1e", .2, coat=.8)
PUPIL = mat("pupil", "#0d0f14", .1, coat=.8)
SHINE = mat("shine", "#ffffff", .1, emis="#ffffff", es=4)
HAIR = mat("hair", "#3b2416", .5, sheen=.3)
BROW = mat("brow", "#2f1c10", .6)
MOUTH = mat("mouth", "#7b2f2a", .4)
GOLD = mat("gold", "#e3b24a", .25, metal=1)
LAMPM = mat("lampmetal", "#3a3f4a", .35, metal=.8)
GLOW = mat("glow", "#7ff3ff", .1, emis="#5ee7ff", es=18)
BLUSH = mat("blush", "#ff8a7a", .6)

# ---------- Beine + Stiefel
for sx in (-1, 1):
    cyl((sx * .1, 0, .27), .072, .066, .34, PANTS)
    cube((sx * .105, -.035, .065), (.15, .24, .12), BOOT, sub=2)
# ---------- Mantel (Trenchcoat): Rock + Oberkoerper
cyl((0, 0, .53), .30, .225, .34, COAT, scl=(1, .82, 1))
cyl((0, 0, .82), .225, .20, .30, COAT, scl=(1, .82, 1))
sphere((0, 0, .96), .205, (1, .8, .55), COAT)                    # Schultern rund
torus((0, 0, .66), .232, .03, COATD, scl=(1, .82, 1))            # Guertel
cube((0, -.192, .66), (.07, .03, .06), GOLD, sub=1)              # Schnalle
for sx in (-1, 1):                                               # Knoepfe
    for z in (.78, .88):
        sphere((sx * .07, -.168, z), .018, (1, .6, 1), COATD)
# Kragen (hochgeklappt)
cyl((0, 0, 1.03), .16, .19, .1, COATD, scl=(1, .85, 1))
# ---------- Schal
torus((0, 0, 1.06), .13, .05, SCARF, scl=(1, .9, 1))
cube((.06, -.15, .93), (.075, .03, .2), SCARF, rot=(0.15, 0, -.12), sub=2)
for i in range(3): cube((.075 + .018 * (i - 1), -.17, .825), (.012, .02, .03), SCARF, sub=1)
# ---------- Arme (Mantelaermel) + Haende
cyl((-.27, -.01, .84), .07, .06, .3, COAT, rot=(0, .28, 0))
cyl((.27, -.07, .82), .07, .06, .3, COAT, rot=(.45, -.28, 0))
torus((-.312, -.01, .70), .058, .016, COATD, rot=(0, .28, 0))
torus((.305, -.13, .69), .058, .016, COATD, rot=(.45, -.28, 0))
sphere((-.322, -.01, .64), .058, (1, .9, 1.1), SKIN)
sphere((.315, -.16, .64), .058, (1, 1, 1), SKIN)
# ---------- Laterne (mystisches blaues Licht) in der rechten Hand
L0 = Vector((.33, -.2, .44))
tube([L0 + Vector((0, 0, .2)), L0 + Vector((0, -.02, .25)), L0 + Vector((0, 0, .17))], .007, LAMPM)
cyl(L0 + Vector((0, 0, .155)), .06, .03, .04, LAMPM, sub=1)
gl = cyl(L0 + Vector((0, 0, .085)), .05, .05, .1, GLOW, sub=0); gl.visible_shadow = False
for a in range(4):
    ang = a * math.pi / 2 + .4
    cyl(L0 + Vector((math.cos(ang) * .052, math.sin(ang) * .052, .085)), .007, .007, .11, LAMPM, sub=0, verts=8)
cyl(L0 + Vector((0, 0, .025)), .065, .065, .025, LAMPM, sub=1)
lamp = bpy.data.lights.new("lantern", "POINT"); lamp.energy = 25; lamp.color = (.45, .9, 1); lamp.shadow_soft_size = .05
lo = bpy.data.objects.new("lantern", lamp); lo.location = L0 + Vector((0, 0, .085)); lo.parent = ROOT; sc.collection.objects.link(lo)
# ---------- Kopf
HZ = 1.36; HR = .29; HS = (1.0, .93, .95)
sphere((0, 0, HZ), HR, HS, SKIN, sub=1, seg=48)
def onhead(x, z, off=0.0):  # Punkt auf der Kopfvorderseite (Ellipsoid)
    dx, dz = x / (HR * HS[0]), (z - HZ) / (HR * HS[2])
    y = -HR * HS[1] * math.sqrt(max(0, 1 - dx * dx - dz * dz))
    return Vector((x, y - off, z))
for sx in (-1, 1):
    sphere((sx * .285, 0, HZ - .01), .055, (.45, .8, 1), SKIN)                      # Ohren
    e = onhead(sx * .105, HZ + .01, -.03)
    sphere(e, .068, (1, .55, 1.18), WHITE, sub=1)                                   # Augapfel
    sphere(e + Vector((sx * -.006, -.032, -.006)), .041, (1, .45, 1.1), IRIS, sub=1)
    sphere(e + Vector((sx * -.006, -.05, -.006)), .022, (1, .4, 1.1), PUPIL, sub=1)
    sphere(e + Vector((sx * .012, -.058, .025)), .011, (1, .5, 1), SHINE, sub=0)
    b = onhead(sx * .11, HZ + .115, -.005)                                          # Augenbrauen (leicht skeptisch)
    tube([b + Vector((-sx * .045, 0, -.005 + (.012 if sx > 0 else 0))), b, b + Vector((sx * .045, .006, (.012 if sx < 0 else -.002)))], .014, BROW)
    sphere(onhead(sx * .17, HZ - .07, -.005), .035, (1, .3, .7), BLUSH, sub=1)    # Wangen
sphere(onhead(0, HZ - .045, .01), .036, (1, .9, .85), SKIN)                      # Nase
m0 = onhead(-.055, HZ - .13, .004); m1 = onhead(.005, HZ - .14, .006); m2 = onhead(.06, HZ - .118, .004)
tube([m0, m1, m2], .009, MOUTH)                                                   # schiefes Grinsen
# Haare: Strähnen unter dem Hut (Stirn + Nacken)
for i, (x, z, s) in enumerate([(-.17, HZ + .13, .07), (-.08, HZ + .17, .075), (.02, HZ + .175, .07), (.12, HZ + .15, .07), (.2, HZ + .1, .06),
                               (-.22, HZ + .05, .06), (.24, HZ + .04, .055)]):
    p = onhead(x, z, -.03)
    sphere(p, s, (1.1, .7, .8), HAIR, rot=(0, (i - 3) * .25, 0))
for i in range(7):
    a = math.pi * (.15 + .7 * i / 6)
    sphere((math.cos(a) * .25, math.sin(a) * .2, HZ - .02 + .03 * (i % 2)), .075, (1, 1, .9), HAIR)
# ---------- Hut (Fedora)
HT = HZ + .2
brim = cyl((0, 0, HT), .4, .4, .025, HAT, scl=(1, .95, 1), rot=(-.08, 0, 0), sub=2)
cyl((0, -.01, HT + .11), .235, .205, .2, HAT, rot=(-.08, 0, 0))
sphere((0, -.015, HT + .2), .205, (1, .95, .32), HAT, rot=(-.08, 0, 0))
torus((0, -.004, HT + .045), .232, .03, BAND, rot=(-.08, 0, 0))

# ---------- Studio: Boden-Hohlkehle, Licht, Kamera
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
fl = bpy.context.active_object; fl.data.materials.append(mat("floor", "#cfd9e6", .9))
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 6, 5), rotation=(math.pi / 2, 0, 0))
bpy.context.active_object.data.materials.append(mat("wall", "#c7d3e3", .9))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = hexc("#dbe6f3"); w.node_tree.nodes["Background"].inputs[1].default_value = .55
def area(name, loc, rot, size, energy, col):
    l = bpy.data.lights.new(name, "AREA"); l.size = size; l.energy = energy; l.color = col
    o = bpy.data.objects.new(name, l); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o); return o
def aim(o, target=Vector((0, 0, .9))):
    d = target - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
k = area("key", Vector((-2.2, -3.0, 3.2)), (0, 0, 0), 2.5, 650, (1, .93, .84)); aim(k)
f = area("fill", Vector((3.0, -2.5, 1.6)), (0, 0, 0), 3.0, 220, (.82, .9, 1)); aim(f)
r = area("rim", Vector((1.8, 2.6, 2.6)), (0, 0, 0), 1.6, 700, (.7, .88, 1)); aim(r, Vector((0, 0, 1.2)))

cam = bpy.data.cameras.new("cam"); cam.lens = 70
co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 160; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.render.resolution_x = 1080; sc.render.resolution_y = 1350; sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
sc.render.image_settings.file_format = 'PNG'

def shot(name, ang, dist=5.6, h=1.05, target=Vector((0, 0, .95)), lens=70):
    cam.lens = lens
    co.location = Vector((math.sin(ang) * dist, -math.cos(ang) * dist, h)); aim(co, target)
    sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True); print("RENDER", name)
shot("theo_front", 0)
shot("theo_34", math.radians(35))
shot("theo_side", math.radians(90))
shot("theo_back", math.radians(180))
sc.render.resolution_x = 1080; sc.render.resolution_y = 1080
shot("theo_portrait", math.radians(20), dist=2.6, h=1.45, target=Vector((0, 0, 1.38)), lens=85)
# Modell fuer spaetere Animation sichern
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "theo.blend"))
try:
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "theo.glb"), export_format='GLB')
except Exception as ex:
    print("GLB-Export fehlgeschlagen", ex)
print("FERTIG")
