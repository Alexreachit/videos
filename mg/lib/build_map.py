# Erzeugt mg/lib/mapdata.js: Weltkarte + US-Bundesstaaten als SVG-Pfade (Web-Mercator, Weltbreite 2000 Einheiten)
import json, math, glob, os, random
W = 2000.0
def P(lon, lat):
    lat = max(-80, min(84, lat)); x = (lon + 180) / 360 * W
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * W
    return x, y
def rings(geom):
    t = geom["type"]; c = geom["coordinates"]
    if t == "Polygon": return [c]
    if t == "MultiPolygon": return c
    return []
def path(geom, tol=0.6):
    out = []
    for poly in rings(geom):
        for ring in poly:
            pts = [P(*p[:2]) for p in ring]; s = []; last = None
            for x, y in pts:
                if last is None or abs(x - last[0]) + abs(y - last[1]) > tol: s.append((x, y)); last = (x, y)
            if len(s) < 3: continue
            out.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in s) + "Z")
    return "".join(out)
world = json.load(open("wgj/countries.geo.json"))
W_PATHS = {}
for f in world["features"]:
    iso = f.get("id"); 
    if iso == "ATA": continue
    W_PATHS[iso] = path(f["geometry"], 0.8)
US = {}
for fn in glob.glob("wgj/countries/USA/*.geo.json"):
    st = os.path.basename(fn).split(".")[0]; g = json.load(open(fn))
    feats = g["features"] if g.get("type") == "FeatureCollection" else [g]
    US[st] = "".join(path(ft["geometry"], 0.25) for ft in feats)
# 9000 Zufallspunkte in den 48 Festlandstaaten (Gewichtung nach Fläche via Rejection Sampling)
polys = []
for fn in glob.glob("wgj/countries/USA/*.geo.json"):
    st = os.path.basename(fn).split(".")[0]
    if st in ("AK", "HI"): continue
    g = json.load(open(fn)); feats = g["features"] if g.get("type") == "FeatureCollection" else [g]
    for ft in feats:
        for poly in rings(ft["geometry"]): polys.append(poly[0])
def inside(x, y, ring):
    c = False; j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][:2]; xj, yj = ring[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi: c = not c
        j = i
    return c
bbs = [(min(p[0] for p in r), min(p[1] for p in r), max(p[0] for p in r), max(p[1] for p in r)) for r in polys]
random.seed(7); dots = []
while len(dots) < 18000:
    lon = random.uniform(-125, -67); lat = random.uniform(25, 49.5)
    for r, b in zip(polys, bbs):
        if b[0] <= lon <= b[2] and b[1] <= lat <= b[3] and inside(lon, lat, r):
            x, y = P(lon, lat); dots.append(round(x, 1)); dots.append(round(y, 1)); break
js = ("// Automatisch erzeugt (build_map.py) – Kartendaten: johan/world.geo.json (Public Domain / Natural Earth)\n"
      "const MAP_W=2000;\nfunction MAPP(lon,lat){lat=Math.max(-80,Math.min(84,lat));const x=(lon+180)/360*MAP_W;"
      "const r=lat*Math.PI/180;const y=(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*MAP_W;return [x,y]}\n"
      "const WORLD=" + json.dumps(W_PATHS, separators=(",", ":")) + ";\nconst USST=" + json.dumps(US, separators=(",", ":")) +
      ";\nconst US_DOTS=" + json.dumps(dots, separators=(",", ":")) + ";\n")
open("../repo/mg/lib/mapdata.js", "w").write(js)
print(len(W_PATHS), "countries", len(US), "states", len(dots)//2, "dots", round(len(js)/1e6, 2), "MB")
