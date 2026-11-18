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
# Schnittpunkte (Tag 3)
DEPTH0 = 804.1                          # Tiefe vor Tag 3
DEPTH = 81656.5                         # Tiefe nach Tag 3 (804,1 m + 80.852,4 m)
KOLA, CRUST = 12262., 40000.
T_DESC0 = wt(4, "runter") + .25
T_KOLA = wt(4, "bohrloch")
T_CRUST = wt(5, "erdkruste")
T_DESC1 = ST[6][0] + .45
T_VEIN = ST[7][0] - .1                  # Kamera dreht zur Diamanten-Ader
T_BLAKE = ST[9][0] - .05                # Schnitt nach oben zu Blake
T_SPACE = ST[10][0] - .05
T_ZOOM_END = T_SPACE + 1.9
T_BACK = ST[11][0] - .05
T_FOLLOW = 999.
T_RISE = T_DESC0
T_SCOOP = 0.0
PIT_R = 2.6
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
BLAKE_ROOT = GHOST_ROOT; BLAKE_YAW = GHOST_YAW
# Menge: 664 Instanzen (+ Chef + Blake = 666), deterministisch, damit Overlay-Anker passen
import random as _r
_rnd = _r.Random(23); POS = []
for r_, sp_ in [(3.75 + .9 * k, .88 + .01 * k) for k in range(14)]:
    n_ = int(2 * math.pi * r_ / sp_)
    for j in range(n_):
        a_ = (j + .5 * (k_ := 0)) / n_ * 2 * math.pi + _rnd.uniform(-.05, .05); rr_ = r_ + _rnd.uniform(-.15, .15)
        x_, y_ = math.cos(a_) * rr_, math.sin(a_) * rr_; yaw_ = math.atan2(-y_, -x_) + _rnd.uniform(-.12, .12); sc_ = _rnd.uniform(.93, 1.06)
        if y_ < -2.4 and abs(x_ - .3) < 2.9: continue
        if y_ < 0 and abs(x_ - .3) < 3.6 and rr_ > 6: continue
        POS.append((x_, y_, yaw_, sc_))
POS = POS[:664]

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
def _dep(t):
    """Absolute Kameratiefe im Schacht (m) waehrend des Abstiegs, log-interpoliert ueber die Meilensteine"""
    K = [(T_DESC0, 1.0), (T_KOLA, KOLA), (T_CRUST, CRUST), (T_DESC1, DEPTH + 2.9)]
    if t <= K[0][0]: return 0.
    if t >= K[-1][0]: return DEPTH + 2.9
    for (ta, da), (tb, db) in zip(K, K[1:]):
        if ta <= t <= tb:
            u = (t - ta) / (tb - ta)
            if ta == K[0][0]: u = u ** 1.6                      # anfahren
            if tb == K[-1][0]: u = 1 - (1 - u) ** 2             # abbremsen
            return math.exp(lerp(math.log(da), math.log(db), u))
def cam_z(t): return 4.5 - _dep(t)
def depth_at(t):
    if t < T_DESC0: return DEPTH0
    if t < T_BLAKE: return min(max(_dep(t), .1), DEPTH)
    return DEPTH
ZB = 4.5 - DEPTH - 2.9                                         # = -DEPTH + 1.6                                               # Kamerahoehe unten
def cam_at(t):
    sm = lambda a, b: ease((t - a) / (b - a))
    if t < ST[1][0]:                     # Luftbild: 666 Arbeiter
        u = sm(0, ST[1][0]); h = lerp(34., 15., u); a = lerp(-.7, -.2, u)
        return [math.sin(a) * lerp(22, 16, u), -math.cos(a) * lerp(22, 16, u), h], [0, 0, 0]
    if t < ST[2][0]:                     # tief: Chef vorn, Menge hinten
        u = sm(ST[1][0], ST[2][0]); return vlerp([3.6, -8.6, 2.4], [3.0, -7.6, 2.3], u), vlerp([.4, -2.6, .55], [.3, -2.4, .6], u)
    if t < ST[3][0]:                     # langsam um die Menge
        u = sm(ST[2][0], ST[3][0]); a = lerp(-.4, .45, u)
        return [math.sin(a) * 19., -math.cos(a) * 19., lerp(7.5, 9.0, u)], [0, 0, 0]
    if t < ST[4][0]:                     # Freddy
        u = sm(ST[3][0], ST[4][0]); return vlerp([2.6, -8.2, 1.6], [2.3, -7.7, 1.6], u), [.4, 1.5, 1.2]
    if t < T_DESC0:
        u = sm(ST[4][0], T_DESC0); return vlerp([2.3, -7.7, 1.6], [.2, -.4, 4.5], u), vlerp([.4, 1.5, 1.2], [0, 0, -30], u)
    if t < T_DESC1:
        z = cam_z(t); return [.2, -.4, z], [0, 0, z - 40]
    if t < T_BLAKE:                      # unten: zur Diamanten-Ader drehen
        u = sm(T_DESC1 + .3, T_DESC1 + 2.0); z = ZB
        p = vlerp([.2, -.4, z], [0., -1.9, z + .3], u)
        tg = vlerp([0, 0, z - 40], [0., 2.5, z - .2], u)
        push = max(0., t - T_DESC1 - 2.0) * .06
        return add(p, [0, push, 0]), tg
    if t < T_SPACE:                      # Blake mit Diamantschaufel
        u = sm(T_BLAKE, T_SPACE); return vlerp([-.55, -.4, 1.75], [-.45, -.65, 1.7], u), vlerp([-.85, -3.1, .85], [-.85, -3.15, .85], u)
    if t < T_BACK:
        u = ease((t - T_SPACE) / (T_ZOOM_END - T_SPACE)); u = 1 - (1 - u) ** 1.6
        dist = math.exp(lerp(math.log(.9), math.log(35.5), u))
        tgt = vlerp(PIN, G, ease(u))
        d0, d1 = norm([-.3, .5, 1.0]), norm([18, -26, 16])
        dirn = norm(vlerp(d0, d1, ease(u)))
        drift = max(0., t - T_ZOOM_END) * .12
        return add(tgt, mul(dirn, dist - drift)), tgt
    u = sm(T_BACK, DUR)
    return vlerp([1.4, -8.0, 2.4], [1.0, -7.2, 2.3], u), vlerp([-.25, -3.1, .6], [-.25, -3.1, .6], u)

def project(cam, tgt, X):
    f = norm(sub(tgt, cam)); r = norm(cross(f, [0, 0, 1])); up = cross(r, f)
    d = sub(X, cam); zc = dot(d, f)
    if zc < .01: return None
    k = LENS / SENSOR * H
    return [W / 2 + dot(d, r) / zc * k, H / 2 - dot(d, up) / zc * k]
