# Erdkern Tag 2 + Extra-Szene "neuester Follower" (Alessio) nach Zeile 1 – ohne Neurendern:
# Hintergrund = alte Blender-Bilder (erd04/bg), fuer die neue Szene Ping-Pong der letzten Bilder vor dem Einschub.
import json, os, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__)); OLD = os.path.join(HERE, "..", "erd04")
old = json.load(open(os.path.join(HERE, "anchors_old.json"))); A, T = old["ANCH"], old["TT"]
dold = json.load(open(os.path.join(HERE, "voice_old", "durs.json"))); dnew = json.load(open(os.path.join(HERE, "voice", "durs.json")))
assert len(dnew) == len(dold) + 1
GAP, LEAD = .12, .05
ins_t = LEAD + sum(d + GAP for d in dold[:2])            # Start der alten Zeile 2 = Start der neuen Szene
D = dnew[2] + GAP                                        # Verschiebung aller spaeteren Zeiten
N = int(round(D * 30)); F0 = int(round(ins_t * 30))
NF_OLD = T["nf"]
MAP = list(range(F0))
half = N // 2
seg = list(range(F0 - 1, F0 - 1 - half, -1)) + list(range(F0 - 1 - (N - half) + 1, F0))   # zurueck, dann wieder vor
seg = seg[:N]
MAP += seg + list(range(F0, NF_OLD))
NF = len(MAP)
bg = os.path.join(HERE, "bg"); shutil.rmtree(bg, ignore_errors=True); os.makedirs(bg)
for i, o in enumerate(MAP): os.link(os.path.join(OLD, "bg", "%05d.jpg" % o), os.path.join(bg, "%05d.jpg" % i))
TT = dict(T); TT["nf"] = NF
for k in ("space", "zoomEnd", "back", "d0", "d1", "follow"): TT[k] = T[k] + D
head = open(os.path.join(HERE, "head.html")).read(); body = open(os.path.join(HERE, "overlay.js")).read()
open(os.path.join(HERE, "scene.html"), "w").write(head + "const ANCH = " + json.dumps(A, separators=(",", ":")) + ";\nconst TT = " + json.dumps(TT) + ";\nconst MAP = " + json.dumps(MAP, separators=(",", ":")) + ";\n" + body)
print("Einschub bei", round(ins_t, 2), "s, Bild", F0, "Dauer", round(D, 2), "s =", N, "Bilder; gesamt", NF)
