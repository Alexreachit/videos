# Gemeinsame Rechnungen fuer Blender-Szene (scene.py) und HTML-Overlay (anchors.py): Timeline, Kamera, Arbeiter-Posen.
# Reines Python (kein bpy/mathutils), damit es lokal und in Blender gleich rechnet.
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
W, H = 1080, 1920
LENS, SENSOR = 30.0, 36.0            # Sensor vertikal angepasst
_D = json.load(open(os.path.join(HERE, "voice", "durs.json")))
LEAD, GAP, TAIL = .05, .12, 1.4
ST = []; t = LEAD
for d in _D: ST.append((t, t + d)); t += d + GAP
DUR = ST[-1][1] + TAIL
NF = int(math.ceil(DUR * FPS))
_WORDS = json.load(open(os.path.join(HERE, "voice", "words.json")))
def wt(i, word):
    for w in _WORDS[i]:
        if w[0].lower().startswith(word.lower()): return ST[i][0] + w[1]
    return ST[i][0]
# Schnittpunkte (Tag 2)
T_DESC0 = ST[3][0] + .2                 # Abstieg in den Schacht
T_DESC1 = ST[3][1] - .1                 # unten angekommen (804 m)
T_SPACE = ST[5][0] - .05                # Schnitt ins All
T_ZOOM_END = T_SPACE + 1.9
T_BACK = ST[6][0] - .05                 # zurueck an die Oberflaeche
T_FOLLOW = wt(6, "arbeiter")           # Geister-Arbeiter (+1)
T_RISE = T_DESC0                        # (fuer Tiefenschaerfe: ab hier keine)
T_SCOOP = 0.0
DEPTH = 804.1                           # Gesamttiefe nach Tag 2 (0,1 m Tag 1 + 804 m)
PIT_R = 2.6                             # Schacht-Radius
# ---------------------------------------------------------------- kleine Vektor-Helfer
def add(a, b): return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
def sub(a, b): return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
def mul(a, s): return [a[0] * s, a[1] * s, a[2] * s]
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def norm(a): l = math.sqrt(dot(a, a)) or 1; return mul(a, 1 / l)
def lerp(a, b, u): return a + (b - a) * u
def vlerp(a, b, u): return [lerp(a[i], b[i], u) for i in range(3)]
def cl(x, a=0., b=1.): return max(a, min(b, x))
def ease(u): u = cl(u); return u * u * (3 - 2 * u)
def rot_y(v, a): c, s = math.cos(a), math.sin(a); return [c * v[0] + s * v[2], v[1], -s * v[0] + c * v[2]]
def rot_z(v, a): c, s = math.cos(a), math.sin(a); return [c * v[0] - s * v[1], s * v[0] + c * v[1], v[2]]

# ---------------------------------------------------------------- Erde (im All, weit weg vom Boden)
G = [0., 0., -4000.]; R = 10.
PIN = add(G, [0, 0, R])                # Grabstelle (Deutschland nach oben gedreht)
CUT_DIR = norm([1, -1, 1])             # ausgeschnittenes Achtel (x>0, y<0, z>0)
def face_pt(r, ang=math.radians(48)):  # Punkt auf der Schnittflaeche y=0 (x>0, z>0), Radius r
    return add(G, [r * math.cos(ang), 0, r * math.sin(ang)])
R_CRUST, R_MANTLE, R_OUTER, R_INNER = R, R * (1 - 2900 / 6370), R * (1 - 5100 / 6370), 0
CRUST_VIS = .22                        # Kruste zur Sichtbarkeit dicker (echt: 40 km = 0,06)
ANCH_EARTH = {"crust": face_pt(R - CRUST_VIS / 2, math.radians(70)), "mantle": face_pt((R_MANTLE + R - CRUST_VIS) / 2, math.radians(62)),
              "outer": face_pt((R_OUTER + R_MANTLE) / 2, math.radians(52)), "inner": face_pt(R_OUTER * .45, math.radians(40)), "pin": PIN, "center": G}

# ---------------------------------------------------------------- Arbeiter (schaut in +X, Loch bei 0,0)
CHEF_ROOT = [.55, -3.75, 0.]; CHEF_YAW = math.pi / 2
GHOST_ROOT = [-.95, -3.85, 0.]; GHOST_YAW = math.pi / 2
HIP = .95
def dig_pose(t, ph=0.0, active=True):
    """bend (Vorbeugen, rad), twist (Drehung zum Haufen), sa (Schaufelwinkel relativ zum Oberkoerper), scoop (0..1 Erde auf Schaufel)"""
    if not active: return dict(bend=.12, twist=0., sa=-.35, scoop=0., p=0.)
    p = ((t + ph) / 1.15) % 1.0
    K = [(0.0, .30, 0.00, -1.05), (.32, .78, 0.00, -1.15), (.55, .45, 0.25, -1.75), (.78, .38, 0.85, -1.95), (1.0, .30, 0.00, -1.05)]
    for k in range(len(K) - 1):
        a, b = K[k], K[k + 1]
        if a[0] <= p <= b[0]:
            u = ease((p - a[0]) / (b[0] - a[0])); break
    bend, twist, sa = lerp(a[1], b[1], u), lerp(a[2], b[2], u), lerp(a[3], b[3], u)
    scoop = 1.0 if .36 < p < .74 else 0.0
    return dict(bend=bend, twist=twist, sa=sa, scoop=scoop, p=p)
SHOULDER_L, SHOULDER_R = [.0, .21, .55], [.0, -.21, .55]
GRIP_O = [.30, -.02, .30]             # obere Hand (Schaufel-Ursprung) im Oberkoerper-Raum
HANDLE = 1.15
def spine_to_world(root, yaw, pose, v):
    """Punkt im Oberkoerper-Raum -> Welt"""
    w = rot_y(v, pose["bend"]); w = rot_z(w, pose["twist"]); w = [w[0], w[1], w[2] + HIP]; w = rot_z(w, yaw); return add(root, w)
def shovel_dir(pose): return rot_y([0, 0, -1], pose["sa"])            # Stiel-Richtung im Oberkoerper-Raum
def grips(pose):
    d = shovel_dir(pose); return GRIP_O, add(GRIP_O, mul(d, .48)), add(GRIP_O, mul(d, HANDLE))   # obere Hand, untere Hand, Blatt
def elbow(s, h, hint, l1=.31, l2=.31):
    d = sub(h, s); L = math.sqrt(dot(d, d)); L2 = min(L, l1 + l2 - .005); u = norm(d)
    a = (l1 * l1 - l2 * l2 + L2 * L2) / (2 * L2); hh = math.sqrt(max(0., l1 * l1 - a * a))
    n = norm(sub(hint, mul(u, dot(hint, u)))); return add(add(s, mul(u, a)), mul(n, hh))
def head_world(root, yaw, pose): return spine_to_world(root, yaw, pose, [.04, 0, .80])

# ---------------------------------------------------------------- Kamera
def cam_z(t):
    """Kamerahoehe im Schacht (Abstieg 0 -> -DEPTH)"""
    u = cl((t - T_DESC0) / (T_DESC1 - T_DESC0)); e = u * u * (3 - 2 * u)
    return lerp(4.5, -DEPTH + 3.0, e)
def depth_at(t):
    if t < T_DESC0: return 0.1
    return cl(-(cam_z(t) - 4.5) / (DEPTH + 1.5) * DEPTH, 0.1, DEPTH)
def cam_at(t):
    """(Position, Ziel) in Welt"""
    sm = lambda a, b: ease((t - a) / (b - a))
    if t < ST[1][0]:                     # Luftbild: Menge um den Schacht
        u = sm(0, ST[1][0]); h = lerp(24., 9., u); a = lerp(-.6, -.15, u)
        return [math.sin(a) * lerp(14, 11, u), -math.cos(a) * lerp(14, 11, u), h], [0, 0, 0]
    if t < ST[2][0]:                     # tief: Chef vorn, Menge hinten
        u = sm(ST[1][0], ST[2][0]); return vlerp([3.6, -8.6, 1.5], [3.0, -7.6, 1.45], u), vlerp([.4, -2.6, 1.0], [.3, -2.4, 1.05], u)
    if t < ST[3][0]:                     # langsam um die Menge
        u = sm(ST[2][0], ST[3][0]); a = lerp(-.35, .5, u)
        return [math.sin(a) * 10.5, -math.cos(a) * 10.5, lerp(3.2, 4.2, u)], [0, 0, .4]
    if t < T_DESC0:
        u = sm(ST[3][0], T_DESC0); return vlerp([math.sin(.5) * 10.5, -math.cos(.5) * 10.5, 4.2], [.2, -.4, 4.5], u), vlerp([0, 0, .4], [0, 0, -30], u)
    if t < T_DESC1:
        z = cam_z(t); return [.2, -.4, z], [0, 0, z - 40]
    if t < T_SPACE:                      # unten: Blick nach oben zum Himmel
        u = sm(T_DESC1, T_DESC1 + .9); z = -DEPTH + 3.0
        return [.2, -.4, z], vlerp([0, 0, z - 40], [0, .02, 0], u)
    if t < T_BACK:
        u = ease((t - T_SPACE) / (T_ZOOM_END - T_SPACE)); u = 1 - (1 - u) ** 1.6
        dist = math.exp(lerp(math.log(.9), math.log(35.5), u))
        tgt = vlerp(PIN, G, ease(u))
        d0, d1 = norm([-.3, .5, 1.0]), norm([18, -26, 16])
        dirn = norm(vlerp(d0, d1, ease(u)))
        drift = max(0., t - T_ZOOM_END) * .12
        return add(tgt, mul(dirn, dist - drift)), tgt
    u = sm(T_BACK, DUR)
    return vlerp([1.6, -7.8, 1.5], [1.2, -7.0, 1.42], u), vlerp([-.2, -3.0, 1.0], [-.2, -3.0, 1.0], u)

def project(cam, tgt, X):
    f = norm(sub(tgt, cam)); r = norm(cross(f, [0, 0, 1])); up = cross(r, f)
    d = sub(X, cam); zc = dot(d, f)
    if zc < .01: return None
    k = LENS / SENSOR * H
    return [W / 2 + dot(d, r) / zc * k, H / 2 - dot(d, up) / zc * k]
