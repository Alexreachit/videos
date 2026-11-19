# Erdkern Tag 3, Ueberarbeitung der Blake-Szene ohne Neurendern:
# Kimberlit-Zeile (Haenger bei "nach") + alte Blake-Zeile raus, neue Zeile "Damit macht sich Blake eine Diamantschaufel ..." direkt nach "Diamanten!" ueber die Blake-Bilder.
import json, os, re, shutil, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OLD = os.path.join(HERE, "..", "erd05"); os.chdir(HERE)
NEWTXT = "Damit macht sich Blake eine Diamantschaufel, die zehnmal so tief gräbt!"
SRC = "/mnt/user-data/uploads/Downloads/ElevenLabs_2026-11-19T08_00_33_Alexander - Deep TV Narrator_pvc_sp107_s30_sb54_se50_b_m2.mp3"
SR = 44100; LEAD, GAP, FPS = .05, .12, 30
# ---- Stimme
os.makedirs("voice", exist_ok=True)
dold = json.load(open(f"{OLD}/voice/durs.json")); wold = json.load(open(f"{OLD}/voice/words.json"))
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
env = np.convolve(np.abs(x), np.ones(441) / 441, mode="same"); v = np.where(env >= .006)[0]
c = x[max(0, v[0] - int(.03 * SR)):min(len(x), v[-1] + int(.08 * SR))]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-b:a", "160k", "voice/08.mp3"], input=c.astype(np.float32).tobytes(), check=True)
def runs(m):
    d = np.diff(np.concatenate([[0], m.astype(int), [0]])); return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))
words = NEWTXT.split(); wts = [max(2, len(re.sub(r"[^\wäöüÄÖÜß]", "", w))) + 1.5 for w in words]
e2 = np.convolve(np.abs(c), np.ones(441) / 441, mode="same") >= .006
for r0, r1 in runs(~e2):
    if (r1 - r0) / SR < .12: e2[r0:r1] = True
cum = np.cumsum(e2) / SR; V = cum[-1]; tot = sum(wts); acc = 0; wn = []
tm = lambda vt: float(np.searchsorted(cum, min(vt, V - 1e-4))) / SR
for w, k in zip(words, wts): t0 = tm(V * acc / tot); acc += k; t1 = tm(V * acc / tot); wn.append([w, round(t0, 3), round(t0 + (t1 - t0) * .92, 3)])
keep = [0, 1, 2, 3, 4, 5, 6, 7, None, 10, 11, 12]
D, W = [], []
for i, k in enumerate(keep):
    if k is None: D.append(round(len(c) / SR, 4)); W.append(wn)
    else: shutil.copy(f"{OLD}/voice/{k:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(dold[k]); W.append(wold[k])
json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
p = json.load(open(f"{OLD}/project.json")); L = p["lines"]
p["lines"] = [L[k] if k is not None else dict(L[9], text=NEWTXT) for k in keep]
json.dump(p, open("project.json", "w"), ensure_ascii=False, indent=1)
# ---- Bilder-Zuordnung
def starts(d):
    s = []; t = LEAD
    for x_ in d: s.append(t); t += x_ + GAP
    return s, t - GAP
So, endo = starts(dold); Sn, endn = starts(D)
TAIL = 1.4; NF_OLD = int(np.ceil((endo + TAIL) * FPS)); NF = int(np.ceil((endn + TAIL) * FPS))
old = json.load(open(f"{OLD}/anchors_tt.json")); TTo = old["TT"]
B0 = int(round(TTo["blake"] * FPS)) + 1; S0 = int(round(TTo["space"] * FPS))      # alte Blake-Bilder B0..S0-1
cut = Sn[8] - .05; sh = So[10] - Sn[9]                                              # Verschiebung der Zeit ab dem All
MAP = []
for f in range(NF):
    t = f / FPS
    if t < cut: MAP.append(min(f, NF_OLD - 1))
    elif t < Sn[9] - .05:
        k = f - int(round(cut * FPS)); n = S0 - B0
        MAP.append(B0 + k if k < n else S0 - 1 - (k - n + 1))                         # am Ende kurz zurueck (vom Blitz verdeckt)
    else: MAP.append(min(NF_OLD - 1, int(round((t + sh) * FPS))))
bg = "bg"; shutil.rmtree(bg, ignore_errors=True); os.makedirs(bg)
for f_ in os.listdir(f"{OLD}/bg"): os.link(f"{OLD}/bg/{f_}", f"{bg}/{f_}")   # alte Nummern; das Overlay waehlt per MAP
TT = dict(TTo); TT["nf"] = NF; TT["blake"] = cut
for k in ("space", "zoomEnd", "back"): TT[k] = TTo[k] - sh
head = open("head.html").read(); body = open("overlay.js").read()
open("scene.html", "w").write(head + "const ANCH = " + json.dumps(old["ANCH"], separators=(",", ":")) + ";\nconst TT = " + json.dumps(TT) + ";\nconst MAP = " + json.dumps(MAP, separators=(",", ":")) + ";\n" + body)
print("Zeilen", len(D), "Dauer", round(endn + TAIL, 2), "s, NF", NF, "| Blake-Schnitt", round(cut, 2), "Bilder", B0, S0, "| Verschiebung", round(sh, 2))
