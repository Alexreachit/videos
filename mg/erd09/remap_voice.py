# Echte ElevenLabs-Stimme (tmpv/voice 00..06 = Zeilen 0,2..7) einsetzen, Bilder je Zeile linear auf die geschaetzten Zeitfenster abbilden (kein Neurendern).
# Quelle der Bild-Zeitachse: anchors_tt.json + voice_est/durs.json (Stand des Renders).
import json, os, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
LEAD, GAP, TAIL, FPS = .05, .12, 1.4, 30
if not os.path.exists("voice_est"): shutil.copytree("voice", "voice_est")
Do = json.load(open("voice_est/durs.json")); Wo = json.load(open("voice_est/words.json"))
dn = json.load(open("tmpv/voice/durs.json")); wn = json.load(open("tmpv/voice/words.json"))
NEW = {0: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}
D, W = [], []
for i in range(len(Do)):
    if i in NEW:
        shutil.copy(f"tmpv/voice/{NEW[i]:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(dn[NEW[i]]); W.append(wn[NEW[i]])
    else:
        D.append(Do[i]); W.append(Wo[i])
json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
def starts(d):
    s = []; t = LEAD
    for x in d: s.append(t); t += x + GAP
    return s, t - GAP
So, eo = starts(Do); Sn, en = starts(D)
KO = [0] + So + [eo + TAIL]; KN = [0] + Sn + [en + TAIL]
def pw(t, A, B):   # stueckweise linear A->B
    for k in range(len(A) - 1):
        if t <= A[k + 1] or k == len(A) - 2:
            return B[k] + (t - A[k]) * (B[k + 1] - B[k]) / (A[k + 1] - A[k])
old = json.load(open("anchors_tt.json")); TTo = old["TT"]; NFo = TTo["nf"]
NF = int(math.ceil((en + TAIL) * FPS))
MAP = [min(NFo - 1, max(0, int(round(pw(f / FPS, KN, KO) * FPS)))) for f in range(NF)]
TT = dict(TTo); TT["nf"] = NF   # depth bleibt nach alter Bildnummer (Overlay liest TT.depth[MAP[f]])
for k in ("space", "zoomEnd", "back", "d0", "d1", "follow", "up"): TT[k] = round(pw(TTo[k], KO, KN), 4)
head = open("head.html").read(); body = open("overlay.js").read()
open("scene.html", "w").write(head + "const ANCH = " + json.dumps(old["ANCH"], separators=(",", ":")) + ";\nconst TT = " + json.dumps(TT) + ";\nconst MAP = " + json.dumps(MAP, separators=(",", ":")) + ";\n" + body)
print("Dauer alt", round(eo + TAIL, 2), "neu", round(en + TAIL, 2), "NF", NFo, "->", NF)
for i in range(len(D)): print(i, round(So[i], 2), "->", round(Sn[i], 2), round(Do[i], 2), "->", round(D[i], 2))
print({k: (round(TTo[k], 2), TT[k]) for k in ("d0", "d1", "space", "zoomEnd", "back", "up")})
