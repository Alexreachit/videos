# 2026-11-05: Nur die Stimme fuer ein Projekt erzeugen (Andrew + Wortzeiten), damit Frames woanders gerendert werden koennen.
# Ergebnis: renders/voices/<projekt>/NN.mp3 + words.json  -> lokal: produce.py <projekt> --voice-from <ordner>
import json, os, sys
sys.path.insert(0, "mg"); import produce
PROJ = "ri02"
cfg = json.load(open(f"mg/{PROJ}/project.json", encoding="utf-8"))
out = f"output/voices/{PROJ}"; os.makedirs(out, exist_ok=True)
W = []
for i, ln in enumerate(cfg["lines"]):
    mp3 = f"{out}/{i:02d}.mp3"
    words = produce.tts_andrew(ln["text"], mp3, cfg["voice"], ln.get("rate", cfg["rate"]))
    W.append([[w, a, b] for w, a, b in words]); print(i, ln["text"], flush=True)
json.dump(W, open(f"{out}/words.json", "w"), ensure_ascii=False)
