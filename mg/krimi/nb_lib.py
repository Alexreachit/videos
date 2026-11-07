# Nebelstein – gemeinsame Blender-Bausteine: Materialien, Formen, Kommissar Theo (mit Kopf-/Laternen-Pivot), Bewohner, Haeuser, Laternen.
import bpy, math
from mathutils import Vector

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [a]

MATS = {}
def mat(name, col, rough=.55, sss=0, sheen=0, coat=0, emis=None, es=0, metal=0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(col); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1.0, .4, .25); b.inputs["Subsurface Scale"].default_value = .02
    if sheen: b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Sheen Tint"].default_value = (1, 1, 1, 1)
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = .12
    if emis: b.inputs["Emission Color"].default_value = hexc(emis); b.inputs["Emission Strength"].default_value = es
    MATS[name] = m; return m

def emis_input(m): return m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]

P = [None]  # aktueller Eltern-Knoten
def sc(): return bpy.context.scene
def link(o):
    if o.name not in sc().collection.objects: sc().collection.objects.link(o)
def parent(o, p=None):
    p = p or P[0]
    if p is not None:
        bpy.context.view_layer.update(); o.parent = p; o.matrix_parent_inverse = p.matrix_world.inverted()
    return o
def empty(name, loc=(0, 0, 0), par=None):
    e = bpy.data.objects.new(name, None); link(e); e.location = loc
    if par is not None: parent(e, par)
    bpy.context.view_layer.update(); return e
def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
def fin(o, m):
    o.data.materials.clear(); o.data.materials.append(m); smooth(o); return parent(o)
def sphere(loc, r, scl=(1, 1, 1), m=None, rot=(0, 0, 0), seg=40):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=max(8, seg // 2), rotation=rot)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m)
def torus(loc, R, r, m, rot=(0, 0, 0), scl=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=56, minor_segments=16)
    o = bpy.context.active_object; o.scale = scl; return fin(o, m)
def rbox(loc, s, m, rot=(0, 0, 0), bev=.2, seg=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object; o.scale = s
    bv = o.modifiers.new("bev", "BEVEL"); bv.width = bev * .5; bv.segments = seg; bv.affect = 'EDGES'
    return fin(o, m)
def cylr(loc, r, depth, m, rot=(0, 0, 0), verts=40, bev=.3):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object
    if bev:
        bv = o.modifiers.new("bev", "BEVEL"); bv.width = min(r, depth) * bev; bv.segments = 4; bv.limit_method = 'ANGLE'
    return fin(o, m)
def cone(loc, r1, r2, depth, m, rot=(0, 0, 0), verts=40):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    return fin(bpy.context.active_object, m)
def tube(pts, r, m):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new("tube", cu); link(o); o.data.materials.append(m); return parent(o)
def text(body, loc, size, m, rot=(math.pi / 2, 0, 0), extrude=.01, align='CENTER'):
    cu = bpy.data.curves.new("t", "FONT"); cu.body = body; cu.size = size; cu.extrude = extrude; cu.align_x = align; cu.align_y = 'CENTER'
    o = bpy.data.objects.new("text", cu); link(o); o.location = loc; o.rotation_euler = rot; o.data.materials.append(m); return parent(o)

K = 1 / .67
def meta(name, m, elems, res=.012):
    mb = bpy.data.metaballs.new(name); mb.resolution = res; mb.render_resolution = res * .6; mb.threshold = .6
    for e in elems:
        t = e[0]; el = mb.elements.new(type=t)
        if t == 'BALL': _, co, r = e; el.co = co; el.radius = r * K
        elif t == 'ELLIPSOID': _, co, r, sz = e; el.co = co; el.radius = r * K; el.size_x, el.size_y, el.size_z = sz
        elif t == 'CAPSULE':
            _, a, b, r = e; a = Vector(a); b = Vector(b); d = b - a
            el.co = (a + b) / 2; el.radius = r * K; el.size_x = d.length / 2; el.rotation = Vector((1, 0, 0)).rotation_difference(d.normalized())
    o = bpy.data.objects.new(name, mb); link(o)
    for ob in bpy.context.view_layer.objects: ob.select_set(False)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.active_object; o.data.materials.clear(); o.data.materials.append(m); smooth(o)
    sm = o.modifiers.new("smooth", "CORRECTIVE_SMOOTH"); sm.iterations = 4
    return parent(o)

def kf(o, path, frame, val, idx=None):
    if idx is None: setattr(o, path, val); o.keyframe_insert(path, frame=frame)
    else: getattr(o, path)[idx] = val; o.keyframe_insert(path, index=idx, frame=frame)

# =====================================================================  KOMMISSAR THEO
_uid = [0]
def build_theo(loc=(0, 0, 0), rotz=0.0):
    """Gibt dict mit root, head (Pivot), lantern (Pivot), glow-Material, lamp-Licht zurueck. Lokale Masse: Fuesse bei z=0, Blick nach -y."""
    _uid[0] += 1; u = str(_uid[0])
    SKIN = mat("skin", "#f6c7a1", .42, sss=.18); COAT = mat("coat", "#e6992a", .62, sheen=.35); COATD = mat("coatd", "#b77a1e", .55, sheen=.25)
    SCARF = mat("scarf", "#16838d", .7, sheen=.5); HAT = mat("hat", "#33384a", .6, sheen=.45); BAND = mat("band", "#16838d", .5)
    PANTS = mat("pants", "#3b465f", .7, sheen=.3); BOOT = mat("boot", "#5e3721", .32, coat=.5)
    WHITE = mat("eyew", "#ffffff", .12, coat=.7); IRIS = mat("iris", "#6b4220", .2, coat=.9); PUPIL = mat("pupil", "#0c0e13", .1, coat=.9)
    SHINE = mat("shine", "#ffffff", .1, emis="#ffffff", es=6); HAIR = mat("hair", "#432616", .45, sheen=.35); BROW = mat("brow", "#2c190d", .6)
    MOUTH = mat("mouth", "#8a3530", .4); GOLD = mat("gold", "#e9b84d", .25, metal=1); LAMPM = mat("lampmetal", "#3b4150", .35, metal=.8)
    GLOW = mat("glow", "#8ef5ff", .1, emis="#5ee7ff", es=20); BLUSH = mat("blush", "#ff8f80", .6)
    root = empty("Theo" + u); P[0] = root
    HZ = 1.33; HR = .30; HS = (1.0, .94, .96)
    meta("Legs" + u, PANTS, [('CAPSULE', (-.095, 0, .13), (-.1, 0, .42), .072), ('CAPSULE', (.095, 0, .13), (.1, 0, .42), .072)])
    for sx in (-1, 1): rbox((sx * .1, -.035, .06), (.15, .25, .12), BOOT, bev=.45)
    SH_L = (-.2, 0, .97); SH_R = (.2, 0, .97); EL_L = (-.29, 0, .78); EL_R = (.29, -.06, .79); WR_L = (-.31, -.02, .62); WR_R = (.29, -.19, .66)
    meta("Coat" + u, COAT, [('ELLIPSOID', (0, 0, .82), .2, (1.0, .78, 1.15)), ('ELLIPSOID', (0, 0, .58), .26, (1.0, .8, .75)),
        ('ELLIPSOID', (0, 0, .46), .28, (1.0, .82, .45)), ('BALL', SH_L, .1), ('BALL', SH_R, .1),
        ('CAPSULE', SH_L, EL_L, .072), ('CAPSULE', EL_L, WR_L, .066), ('CAPSULE', SH_R, EL_R, .072), ('CAPSULE', EL_R, WR_R, .066)])
    torus((0, 0, .655), .222, .026, COATD, scl=(1, .8, 1)); rbox((0, -.183, .655), (.075, .03, .065), GOLD, bev=.3)
    for sx in (-1, 1):
        for z in (.76, .88): sphere((sx * .075, -.158, z), .019, (1, .55, 1), COATD, seg=20)
    tube([Vector((-.03, -.165, .99)), Vector((-.07, -.17, .86)), Vector((-.05, -.19, .70))], .012, COATD)
    torus((0, 0, 1.03), .145, .045, COATD, scl=(1, .88, 1.15)); torus((0, 0, 1.075), .135, .068, SCARF, scl=(1, .9, 1))
    sphere((.05, -.165, 1.04), .055, (1, .7, .9), SCARF, seg=28); meta("ScarfEnd" + u, SCARF, [('CAPSULE', (.07, -.16, 1.03), (.09, -.2, .83), .045)])
    sphere(WR_L, .062, (.95, .9, 1.1), SKIN); sphere(WR_R, .062, (1, 1, 1), SKIN)
    # Laterne an Pivot (Handgelenk) -> kann schwingen
    lp = empty("LanternPivot" + u, WR_R, root); P[0] = lp
    L0 = Vector((WR_R[0] + .02, WR_R[1] - .02, WR_R[2] - .26))
    tube([Vector(WR_R) + Vector((0, 0, -.02)), L0 + Vector((0, 0, .22))], .008, LAMPM)
    cylr(L0 + Vector((0, 0, .17)), .055, .035, LAMPM); sphere(L0 + Vector((0, 0, .195)), .03, (1, 1, .6), LAMPM, seg=20)
    gl = sphere(L0 + Vector((0, 0, .09)), .052, (1, 1, 1.25), GLOW); gl.visible_shadow = False
    for a in range(4):
        ang = a * math.pi / 2 + .4; cylr(L0 + Vector((math.cos(ang) * .05, math.sin(ang) * .05, .09)), .007, .13, LAMPM, verts=10)
    cylr(L0 + Vector((0, 0, .015)), .06, .03, LAMPM)
    lamp = bpy.data.lights.new("lantern" + u, "POINT"); lamp.energy = 18; lamp.color = (.45, .9, 1); lamp.shadow_soft_size = .04
    lo = bpy.data.objects.new("lanternL" + u, lamp); link(lo); lo.location = L0 + Vector((0, 0, .09)); parent(lo)
    # Kopf an Pivot (Hals)
    hp = empty("HeadPivot" + u, (0, 0, 1.08), root); P[0] = hp
    sphere((0, 0, HZ - .27), .07, (1, 1, 1.2), SKIN); sphere((0, 0, HZ), HR, HS, SKIN, seg=56)
    def onhead(x, z, off=0.0):
        dx, dz = x / (HR * HS[0]), (z - HZ) / (HR * HS[2]); y = -HR * HS[1] * math.sqrt(max(0, 1 - dx * dx - dz * dz)); return Vector((x, y - off, z))
    lids = []
    for sx in (-1, 1):
        sphere((sx * .292, .01, HZ - .02), .06, (.42, .75, 1), SKIN, seg=28)
        e = onhead(sx * .105, HZ, -.035)
        sphere(e, .078, (1, .55, 1.2), WHITE, seg=36); sphere(e + Vector((-sx * .004, -.037, -.008)), .05, (1, .42, 1.1), IRIS, seg=28)
        sphere(e + Vector((-sx * .004, -.057, -.008)), .028, (1, .38, 1.1), PUPIL, seg=20); sphere(e + Vector((sx * .016, -.066, .028)), .013, (1, .5, 1), SHINE, seg=14)
        lid = sphere(e + Vector((0, -.004, 0)), .082, (1.02, .6, .02), SKIN, seg=36); lids.append(lid)   # Augenlid fuer Blinzeln (z-Skalierung)
        b = onhead(sx * .112, HZ + .12, -.008)
        tube([b + Vector((-sx * .048, 0, -.004 + (.014 if sx > 0 else 0))), b, b + Vector((sx * .048, .008, (.014 if sx < 0 else -.004)))], .015, BROW)
        sphere(onhead(sx * .175, HZ - .075, -.004), .036, (1, .28, .68), BLUSH, seg=20)
    sphere(onhead(0, HZ - .05, .012), .038, (1, .9, .85), SKIN, seg=28)
    tube([onhead(-.058, HZ - .135, .004), onhead(.004, HZ - .148, .006), onhead(.062, HZ - .122, .004)], .012, MOUTH)
    hair = [('ELLIPSOID', (0, .05, HZ + .07), .3, (1.04, 1.0, .82))]
    for i, x in enumerate([-.19, -.11, -.02, .07, .16, .22]): hair.append(('BALL', tuple(onhead(x, HZ + .155 - abs(x) * .25, -.02)), .062 - .004 * (i % 2)))
    for sx in (-1, 1): hair.append(('BALL', (sx * .25, .02, HZ + .06), .07))
    meta("Hair" + u, HAIR, hair, res=.01)
    HT = HZ + .21; TILT = (-.1, 0, .06)
    sphere((0, -.01, HT), .41, (1, .95, .055), HAT, rot=TILT); sphere((0, -.01, HT + .1), .225, (1, .93, .62), HAT, rot=TILT)
    torus((0, -.005, HT + .045), .222, .028, BAND, rot=TILT)
    P[0] = None
    root.location = loc; root.rotation_euler = (0, 0, rotz)
    return dict(root=root, head=hp, lantern=lp, glow=GLOW, lamp=lamp, lids=lids)

# =====================================================================  BEWOHNER (vereinfachte Figuren)
def build_resident(loc, coat="#7a5cc4", hat="#2f3a4f", skin="#f0c19a", hatkind=0, rotz=0.0, dark=False, sign=None):
    _uid[0] += 1; u = str(_uid[0])
    if dark:
        C = mat("silh", "#141a26", .9); CS = C; H = C; SK = C
    else:
        C = mat("rc" + coat, coat, .6, sheen=.35); H = mat("rh" + hat, hat, .55, sheen=.4); SK = mat("rs" + skin, skin, .45, sss=.15)
    root = empty("Res" + u); P[0] = root
    meta("RB" + u, C, [('ELLIPSOID', (0, 0, .6), .24, (1, .8, 1.25)), ('ELLIPSOID', (0, 0, .32), .26, (1, .85, .7)),
                       ('CAPSULE', (-.2, 0, .82), (-.27, -.04, .5), .065), ('CAPSULE', (.2, 0, .82), (.27, -.04, .5), .065)])
    meta("RL" + u, mat("pants", "#3b465f", .7) if not dark else C, [('CAPSULE', (-.09, 0, .05), (-.09, 0, .25), .07), ('CAPSULE', (.09, 0, .05), (.09, 0, .25), .07)])
    hp = empty("RHead" + u, (0, 0, .95), root); P[0] = hp
    sphere((0, 0, 1.18), .27, (1, .95, .96), SK, seg=40)
    eyes = []
    for sx in (-1, 1):
        if dark: eyes.append(sphere((sx * .09, -.235, 1.2), .032, (1, .5, 1), mat("eyeglow", "#ffffff", .2, emis="#dff8ff", es=25), seg=16))
        else:
            sphere((sx * .09, -.225, 1.2), .05, (1, .5, 1.2), mat("eyew", "#ffffff", .12), seg=24)
            eyes.append(sphere((sx * .09, -.25, 1.195), .028, (1, .4, 1.1), mat("pupil", "#0c0e13", .1), seg=16))
    if hatkind == 0:   # Melone
        sphere((0, 0, 1.4), .3, (1, 1, .06), H); sphere((0, 0, 1.45), .2, (1, 1, .75), H)
    elif hatkind == 1:  # Muetze
        sphere((0, 0, 1.36), .25, (1, 1, .55), H); sphere((0, 0, 1.6), .06, (1, 1, 1), mat("pom", "#f2f2f2", .8))
    elif hatkind == 2:  # Zylinder
        sphere((0, 0, 1.4), .3, (1, 1, .05), H); cylr((0, 0, 1.56), .17, .32, H)
    else:               # Haarknoten
        sphere((0, .03, 1.3), .26, (1.03, 1, .75), mat("rhair", "#5a3a22", .5)); sphere((0, .1, 1.5), .1, (1, 1, 1), mat("rhair", "#5a3a22", .5))
    if sign:
        P[0] = root
        rbox((0, -.28, .62), (.5, .04, .3), mat("sign", "#f4ead2", .7), bev=.3)
        text(sign, (0, -.305, .62), .085 if len(sign) > 9 else .1, mat("signink", "#2a2230", .6), extrude=.004)
    P[0] = None
    root.location = loc; root.rotation_euler = (0, 0, rotz)
    return dict(root=root, head=hp, eyes=eyes)

# =====================================================================  STADT
def cobble_mat():
    if "cobble" in MATS: return MATS["cobble"]
    m = bpy.data.materials.new("cobble"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 3.2
    try: vo.feature = 'DISTANCE_TO_EDGE'
    except Exception: pass
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = .02; ramp.color_ramp.elements[0].color = hexc("#1c2333")
    ramp.color_ramp.elements[1].position = .1; ramp.color_ramp.elements[1].color = hexc("#56607a")
    nt.links.new(vo.outputs["Distance"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = .6; nt.links.new(vo.outputs["Distance"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = .45
    MATS["cobble"] = m; return m

WIN = None
def house(loc, w, d, h, col, roof, rotz=0, door=True, seed=0):
    global WIN
    WIN = WIN or mat("window", "#ffcf7a", .3, emis="#ffb04a", es=6)
    root = empty("House"); P[0] = root
    rbox((0, 0, h / 2), (w, d, h), mat("wall" + col, col, .8), bev=.06)
    # Dach: zwei schraege Platten
    for s in (-1, 1):
        rbox((s * w * .26, 0, h + w * .2), (w * .62, d * 1.08, .09), mat("roof" + roof, roof, .6), rot=(0, s * -.62, 0), bev=.5)
    rbox((0, 0, h + w * .1), (w * .9, d * .98, w * .22), mat("wall" + col, col, .8), bev=.1)
    rbox((w * .25, d * .2, h + w * .45), (.25, .25, .6), mat("chim", "#7d5a4a", .8), bev=.2)
    import random; rnd = random.Random(seed)
    fr = mat("frame", "#3a2e2a", .6)
    for fl in range(max(1, int(h / 1.4))):
        for i in (-1, 1):
            z = .9 + fl * 1.3
            if z > h - .4: continue
            lit = rnd.random() > .35
            rbox((i * w * .25, -d / 2 - .02, z), (.42, .06, .55), fr, bev=.3)
            rbox((i * w * .25, -d / 2 - .05, z), (.34, .04, .46), WIN if lit else mat("windark", "#2a3550", .3), bev=.3)
    if door:
        rbox((0, -d / 2 - .03, .55), (.5, .08, 1.1), mat("door", "#5a3a2a", .5), bev=.3)
        sphere((.15, -d / 2 - .09, .55), .03, (1, 1, 1), mat("gold", "#e9b84d", .25, metal=1), seg=12)
    P[0] = None; root.location = loc; root.rotation_euler = (0, 0, rotz); return root

def streetlamp(loc, energy=60):
    root = empty("Lamp"); P[0] = root
    pole = mat("pole", "#232a36", .4, metal=.6)
    cylr((0, 0, 1.4), .05, 2.8, pole, bev=0); cylr((0, 0, .06), .14, .12, pole)
    rbox((0, 0, 2.95), (.32, .32, .4), mat("lampglass", "#ffe7a8", .2, emis="#ffcf6b", es=12), bev=.3)
    cone((0, 0, 3.25), .26, .02, .25, pole)
    l = bpy.data.lights.new("sl", "POINT"); l.energy = energy; l.color = (1, .78, .45); l.shadow_soft_size = .2
    lo = bpy.data.objects.new("slo", l); link(lo); lo.location = (0, 0, 2.95); parent(lo)
    P[0] = None; root.location = loc; return root

def raven(loc, rotz=0, scale=1.0):
    root = empty("Raven"); P[0] = root
    B = mat("raven", "#151821", .35, sheen=.5, coat=.3)
    meta("RavenBody", B, [('ELLIPSOID', (0, 0, .18), .12, (1, 1.5, 1)), ('BALL', (0, -.12, .3), .08), ('CAPSULE', (0, .12, .14), (0, .3, .06), .04)])
    cone((0, -.22, .3), .03, .0, .1, mat("beak", "#3b3f4a", .4), rot=(math.pi / 2, 0, 0))
    for sx in (-1, 1): sphere((sx * .05, -.17, .33), .016, (1, 1, 1), mat("raveneye", "#ffffff", .2, emis="#cfe9ff", es=8), seg=12)
    for sx in (-1, 1): cylr((sx * .04, 0, .03), .008, .08, mat("beak", "#3b3f4a", .4), bev=0, verts=8)
    P[0] = None; root.location = loc; root.rotation_euler = (0, 0, rotz); root.scale = (scale,) * 3; return root
