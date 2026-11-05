# Nur die Stimme (Andrew + Wortzeiten) fuer ein Projekt: python mg/tts_only.py <projekt> <ordner>
# -> <ordner>/NN.mp3 + words.json ; danach: produce.py <projekt> --voice-from <ordner>
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import produce
P, out = sys.argv[1], sys.argv[2]
cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), P, "project.json"), encoding="utf-8"))
os.makedirs(out, exist_ok=True); W = []
for i, ln in enumerate(cfg["lines"]):
    words = produce.tts_andrew(ln["text"], f"{out}/{i:02d}.mp3", cfg["voice"], ln.get("rate", cfg["rate"]),
                               pitch=ln.get("pitch", "+0Hz"), volume=ln.get("volume", "+0%"))
    W.append([[w, a, b] for w, a, b in words]); print(i, ln["text"], flush=True)
json.dump(W, open(f"{out}/words.json", "w"), ensure_ascii=False)
