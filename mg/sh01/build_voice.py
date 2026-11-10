# ElevenLabs-Aufnahme (alle Zeilen, getrennt durch <break 1.0s>) -> voice/NN.mp3 + words.json (Wortzeiten geschaetzt nach Silbenlaenge)
# python3 build_voice.py voice_eleven.mp3
import json, os, re, subprocess, sys, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__))); SR = 44100
lines = [l["text"] for l in json.load(open("project.json", encoding="utf-8"))["lines"]]; N = len(lines)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
env = np.convolve(np.abs(x), np.ones(441) / 441, mode="same"); q = env < .006
def runs(mask):   # (start,end) der stillen Abschnitte
    d = np.diff(np.concatenate([[0], mask.astype(int), [0]])); return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))
sil = [(a, b) for a, b in runs(q) if (b - a) / SR > .6 and a > 0 and b < len(x)]
sil = sorted(sorted(sil, key=lambda r: r[1] - r[0], reverse=True)[:N - 1])
assert len(sil) == N - 1, len(sil)
bounds = [0] + [(a + b) // 2 for a, b in sil] + [len(x)]
os.makedirs("voice", exist_ok=True); W = []; DUR = []
for i in range(N):
    c = x[bounds[i]:bounds[i + 1]]; v = np.where(env[bounds[i]:bounds[i + 1]] >= .006)[0]
    a, b = max(0, v[0] - int(.03 * SR)), min(len(c), v[-1] + int(.08 * SR)); c = c[a:b]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-b:a", "160k", f"voice/{i:02d}.mp3"], input=c.astype(np.float32).tobytes(), check=True)
    # Wortzeiten: stimmhafte Abschnitte (Pausen > .12 s trennen) proportional zur Wortlaenge fuellen
    words = lines[i].split(); wts = [max(2, len(re.sub(r"[^\wäöüÄÖÜß]", "", w))) + 1.5 for w in words]
    e2 = np.convolve(np.abs(c), np.ones(441) / 441, mode="same") >= .006   # Stille ueberspringen: Woerter nur auf stimmhafte Zeit verteilen
    for r0, r1 in runs(~e2):
        if (r1 - r0) / SR < .12: e2[r0:r1] = True
    cum = np.cumsum(e2) / SR; V = cum[-1]; tot = sum(wts); acc = 0; out = []
    tm = lambda vt: float(np.searchsorted(cum, min(vt, V - 1e-4))) / SR
    for w, k in zip(words, wts): t0 = tm(V * acc / tot); acc += k; t1 = tm(V * acc / tot); out.append([w, round(t0, 3), round(t0 + (t1 - t0) * .92, 3)])
    W.append(out); DUR.append(round(len(c) / SR, 4)); print(i, round(len(c) / SR, 2), lines[i])
json.dump(W, open("voice/words.json", "w"), ensure_ascii=False); json.dump(DUR, open("voice/durs.json", "w"))
