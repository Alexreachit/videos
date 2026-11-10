# Nur die Stimme (Andrew + Wortzeiten) fuer ein Projekt: python mg/tts_only.py <projekt> <ordner>
# -> <ordner>/NN.mp3 + words.json ; danach: produce.py <projekt> --voice-from <ordner>
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import produce
P, out = sys.argv[1], sys.argv[2]
cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), P, "project.json"), encoding="utf-8"))
os.makedirs(out, exist_ok=True); W = []
pre = os.path.join(os.path.dirname(os.path.abspath(__file__)), P, "voice")   # fertige Stimme (z. B. ElevenLabs, build_voice.py) im Projekt -> nur kopieren
if os.path.exists(os.path.join(pre, "words.json")):
    import shutil
    for f in os.listdir(pre): shutil.copy(os.path.join(pre, f), out)
    print("Stimme aus", pre, "uebernommen"); sys.exit(0)
for i, ln in enumerate(cfg["lines"]):
    words = produce.tts_andrew(ln.get("say", ln["text"]), f"{out}/{i:02d}.mp3", cfg["voice"], ln.get("rate", cfg["rate"]),   # "say" = Aussprache (Zahlen als Woerter)
                               pitch=ln.get("pitch", "+0Hz"), volume=ln.get("volume", "+0%"), lang=cfg.get("lang"))
    W.append([[w, a, b] for w, a, b in words]); print(i, ln["text"], flush=True)
json.dump(W, open(f"{out}/words.json", "w"), ensure_ascii=False)
