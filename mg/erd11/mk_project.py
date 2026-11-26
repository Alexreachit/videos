# TikTok-Serie "Bis zum Erdkern" – Tag 9 (Aufbau von Alex freigegeben 2026-11-26: rmin wird Bohrmeister, Turbo).
# Zahlen (Alex, Tag-8-Video): 37 Likes, 13 Shares -> 37 + 13*5 = 102 Schaufeln je Arbeiter. Follower 831 + 14 = 845. Neuester Follower: Levin.
# 843 * 102 * 0,1 m = 8.598,6 m; Blake 102 m; Emilio 102 m; Bohrer mit Turbo (Bohrmeister rmin) 2 * 3.000 = 6.000 m
# -> heute 14.802,6 m (14,8 km). Gesamt 118.937,4 + 14.802,6 = 133.740,0 m (133,7 km). Rest 6.370 - 133,74 = 6.236,3 km.
import json, os, shutil, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P5 = json.load(open("../erd07/project.json"))
NEW = [("Tag 9: Wir graben ein Loch bis zum Erdkern!", "Tag neun: Wir graben ein Loch bis zum Erdkern!", "intro"),
       None,
       ("Wir sind jetzt 845 Arbeiter!", "Wir sind jetzt achthundertfünfundvierzig Arbeiter!", "count"),
       ("Neu dabei: Levin! Willkommen am Loch!", None, "newest"),
       ("37 Likes, 13 Shares: 102 Schaufeln!", "Siebenunddreißig Likes, dreizehn Shares: hundertzwei Schaufeln!", "calc"),
       ("rmin hat geschrieben: hab geliket! Dafür wird er unser Bohrmeister!", "Ermin hat geschrieben: hab gelaikt! Dafür wird er unser Bohrmeister!", "drill"),
       ("Er schaltet den Turbo ein: Der Bohrer bohrt heute doppelt so tief!", None, "turbo"),
       ("Heute 14,8 Kilometer. Jetzt sind wir fast 134 Kilometer tief!", "Heute vierzehn Komma acht Kilometer. Jetzt sind wir fast hundertvierunddreißig Kilometer tief!", "desc"),
       ("Noch über 6.230 Kilometer!", "Noch über sechstausendzweihundertdreißig Kilometer!", "earth"),
       None]
L = []
for i, n in enumerate(NEW):
    if n is None:
        k = 1 if i == 1 else 8; L.append(dict(P5["lines"][k], spec=dict(type="rules" if i == 1 else "comment"))); continue
    txt, say, sp = n; L.append(dict(text=txt, spec=dict(type=sp), **({"say": say} if say else {})))
json.dump(dict(P5, title="TikTok-Serie Bis zum Erdkern – Tag 9 (Deutsch)", voice="elevenlabs:Alexander - Deep TV Narrator (erd11/voice; Zeilen 1+9 aus erd07)", lines=L), open("project.json", "w"), indent=1, ensure_ascii=False)
NI = [i for i, n in enumerate(NEW) if n]
os.makedirs("tmpv", exist_ok=True); shutil.copy("build_voice.py", "tmpv/build_voice.py")
json.dump({"lines": [L[i] for i in NI]}, open("tmpv/project.json", "w"), ensure_ascii=False)
if len(sys.argv) > 1 and sys.argv[1] == "assemble":   # nach build_voice: voice/ zusammensetzen
    os.makedirs("voice", exist_ok=True); dn = json.load(open("tmpv/voice/durs.json")); wn = json.load(open("tmpv/voice/words.json"))
    d5 = json.load(open("../erd07/voice/durs.json")); w5 = json.load(open("../erd07/voice/words.json")); D, W = [], []
    for i, n in enumerate(NEW):
        if n is None: k = 1 if i == 1 else 8; shutil.copy(f"../erd07/voice/{k:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(d5[k]); W.append(w5[k])
        else: j = NI.index(i); shutil.copy(f"tmpv/voice/{j:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(dn[j]); W.append(wn[j])
    json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
    for l, d in zip(L, D): print(round(d, 2), l["text"])
else:
    print(' <break time="1s"/> '.join(L[i].get("say", L[i]["text"]) for i in NI))
