# Nebelstein – TikTok-Profilbild: Theo (Brustbild) vor Vollmond + Uhrturm-Silhouette im Nebel. Varianten: mit/ohne Rabe.
import bpy, sys, os, math
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nb_lib as L
from nb_lib import mat, hexc, sphere, rbox, cylr, cone, empty
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/out"]
OUT = ARGS[0]; os.makedirs(OUT, exist_ok=True)
S = bpy.context.scene

def build(raven):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    S = bpy.context.scene; L.MATS.clear(); L.WIN = None
    TH = L.build_theo(loc=(0, 0, 0), rotz=math.radians(-12))
    TH["head"].rotation_euler = (math.radians(-4), math.radians(-5), math.radians(14))
    if raven:
        rv = L.raven((-.22, .04, 1.01), rotz=-math.pi / 2 + .5, scale=.75)
    # Hintergrund: Mond + Uhrturm-Silhouette + Nebelbank
    moon = mat("moonm", "#fff3d6", .5, emis="#ffe9c2", es=3.5)
    L.P[0] = None
    sphere((.55, 4.5, 1.95), .95, (1, .2, 1), moon, seg=64)
    sil = mat("sil", "#1b2a47", .9)
    rbox((-.9, 4.0, 1.0), (.5, .3, 2.4), sil, bev=.05); cone((-.9, 4.0, 2.42), .38, .02, .5, sil, verts=4, rot=(0, 0, math.pi / 4))
    cylr((-.9, 3.84, 1.75), .14, .02, mat("cf", "#ffd98a", .5, emis="#ffcf6b", es=3), rot=(math.pi / 2, 0, 0), bev=0)
    for x, w, h in ((-1.6, .6, 1.1), (1.5, .7, 1.3), (2.2, .6, .9), (-2.3, .7, 1.4)):
        rbox((x, 4.2, h / 2), (w, .3, h), sil, bev=.05)
    W = bpy.data.worlds.new("w"); S.world = W; W.use_nodes = True
    W.node_tree.nodes["Background"].inputs[0].default_value = hexc("#2c4f86"); W.node_tree.nodes["Background"].inputs[1].default_value = .9
    def area(name, loc, tgt, e, size, col):
        l = bpy.data.lights.new(name, "AREA"); l.energy = e; l.size = size; l.color = col
        o = bpy.data.objects.new(name, l); L.link(o); o.location = Vector(loc); d = Vector(tgt) - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    area("key", (-1.6, -2.4, 2.4), (0, 0, 1.25), 260, 2.5, (1, .9, .78))
    area("fill", (1.8, -2.0, 1.4), (0, 0, 1.2), 70, 3, (.7, .82, 1))
    area("rim", (1.3, 1.6, 2.0), (0, 0, 1.3), 420, 1.5, (.45, .8, 1))
    area("rim2", (-1.4, 1.5, 1.8), (0, 0, 1.3), 220, 1.5, (.5, .85, 1))
    S.view_layers[0].use_pass_mist = True; W.mist_settings.start = 2.5; W.mist_settings.depth = 4; W.mist_settings.falloff = 'LINEAR'
    S.use_nodes = True; nt = S.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new("CompositorNodeRLayers"); comp = nt.nodes.new("CompositorNodeComposite")
    mix = nt.nodes.new("CompositorNodeMixRGB"); mix.inputs[2].default_value = hexc("#5f7fb4")
    mv = nt.nodes.new("CompositorNodeMath"); mv.operation = 'MULTIPLY'; mv.inputs[1].default_value = .55
    nt.links.new(rl.outputs["Mist"], mv.inputs[0]); nt.links.new(mv.outputs[0], mix.inputs[0]); nt.links.new(rl.outputs["Image"], mix.inputs[1])
    gl = nt.nodes.new("CompositorNodeGlare"); gl.glare_type = 'FOG_GLOW'; gl.threshold = .85; gl.size = 8; gl.mix = -.4
    nt.links.new(mix.outputs[0], gl.inputs[0]); nt.links.new(gl.outputs[0], comp.inputs[0])
    c = bpy.data.cameras.new("cam"); c.lens = 85; co = bpy.data.objects.new("cam", c); L.link(co); S.camera = co
    co.location = Vector((.45, -2.75, 1.42)); d = Vector((0, 0, 1.36)) - co.location; co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = 128; S.cycles.use_denoising = True
    S.view_settings.view_transform = 'AgX'; S.view_settings.exposure = .6
    try: S.view_settings.look = 'AgX - Punchy'
    except Exception: pass
    S.render.resolution_x = 1080; S.render.resolution_y = 1080
    S.render.filepath = os.path.join(OUT, "profil_%s.png" % ("rabe" if raven else "theo")); bpy.ops.render.render(write_still=True); print("RENDER", raven)

build(True)
build(False)
