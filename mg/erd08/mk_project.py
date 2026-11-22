# TikTok-Serie "Bis zum Erdkern" – Tag 6 (Aufbau von Alex freigegeben 2026-11-22).
# Zahlen (Alex, Tag-5-Video): 42 Likes, 16 Shares -> 42 + 16*5 = 122 Schaufeln je Arbeiter. Follower: 758 + 12 neue = 770 (angenommen).
# 769 * 122 * 0,1 m = 9.381,8 m; Blake 122 * 1,0 m = 122 m -> heute 9.503,8 m (9,5 km). Gesamt 93.881,3 + 9.503,8 = 103.385,1 m (103,4 km).
# Rest 6.370 - 103,39 = 6.266,6 km. Neuester Follower: Tutorials. Top-Kommentar: Karlstumbles fragt, wo er steht -> wird gezeigt + Namensschild.
# Stimme: neue Zeilen aus ElevenLabs 2026-11-22; Regeln- und Kommentarzeile aus Tag 5 (erd07/voice 01, 08), um Credits zu sparen.
import json, os, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open("tmpv/project.json"))["lines"]; P5 = json.load(open("../erd07/project.json"))
d5 = json.load(open("../erd07/voice/durs.json")); w5 = json.load(open("../erd07/voice/words.json"))
dn = json.load(open("tmpv/voice/durs.json")); wn = json.load(open("tmpv/voice/words.json"))
order = [("n", 0), ("5", 1), ("n", 1), ("n", 2), ("n", 3), ("n", 4), ("n", 5), ("n", 6), ("5", 8)]
specs = ["intro", "rules", "count", "newest", "calc", "karl", "desc", "earth", "comment"]
os.makedirs("voice", exist_ok=True); L, D, W = [], [], []
for i, ((src, k), sp) in enumerate(zip(order, specs)):
    if src == "n": shutil.copy(f"tmpv/voice/{k:02d}.mp3", f"voice/{i:02d}.mp3"); L.append(dict(T[k], spec=dict(type=sp))); D.append(dn[k]); W.append(wn[k])
    else: shutil.copy(f"../erd07/voice/{k:02d}.mp3", f"voice/{i:02d}.mp3"); L.append(dict(P5["lines"][k], spec=dict(type=sp))); D.append(d5[k]); W.append(w5[k])
json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
P = dict(P5, title="TikTok-Serie Bis zum Erdkern – Tag 6 (Deutsch)", voice="elevenlabs:Alexander - Deep TV Narrator (erd08/voice)", lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
for l, d in zip(L, D): print(round(d, 2), l["text"])
