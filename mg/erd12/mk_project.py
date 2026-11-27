# TikTok-Serie "Bis zum Erdkern" – Tag 10 (Aufbau von Alex freigegeben 2026-11-27: Baldi bekommt Riesenbohrer; Regeln kuerzer).
# Zahlen (Alex, Tag-9-Video): 31 Likes, 12 Shares -> 31 + 12*5 = 91 Schaufeln je Arbeiter. Follower 845 + 24 = 869. Neuester Follower: london14.
# 867 * 91 * 0,1 m = 7.889,7 m; Blake 91 m; Emilio 91 m; Riesenbohrer (Baldi) 10.000 m
# -> heute 18.071,7 m (18,1 km). Gesamt 133.740,0 + 18.071,7 = 151.811,7 m (151,8 km). Rest 6.370 - 151,81 = 6.218,2 km.
import json, os, shutil, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P5 = json.load(open("../erd07/project.json"))
NEW = [("Tag 10: Wir graben ein Loch bis zum Erdkern!", "Tag zehn: Wir graben ein Loch bis zum Erdkern!", "intro"),
       ("Folgen: Arbeiter. Like: Schaufel. Share: fünf Schaufeln!", None, "rules"),
       ("Wir sind jetzt 869 Arbeiter!", "Wir sind jetzt achthundertneunundsechzig Arbeiter!", "count"),
       ("Neu dabei: london14! Willkommen am Loch!", "Neu dabei: London vierzehn! Willkommen am Loch!", "newest"),
       ("31 Likes, 12 Shares: 91 Schaufeln!", "Einunddreißig Likes, zwölf Shares: einundneunzig Schaufeln!", "calc"),
       ("Baldi sagt: Ich arbeite nicht kostenlos! Sein Lohn: ein Riesenbohrer!", None, "drill"),
       ("Bohrmeister rmin wirft ihn an: Er bohrt heute 10 Kilometer!", "Bohrmeister Ermin wirft ihn an: Er bohrt heute zehn Kilometer!", "turbo"),
       ("Heute 18,1 Kilometer. Jetzt sind wir über 150 Kilometer tief!", "Heute achtzehn Komma eins Kilometer. Jetzt sind wir über hundertfünfzig Kilometer tief!", "desc"),
       ("Noch über 6.210 Kilometer!", "Noch über sechstausendzweihundertzehn Kilometer!", "earth"),
       None]
L = []
for i, n in enumerate(NEW):
    if n is None:
        k = 8; L.append(dict(P5["lines"][k], spec=dict(type="comment"))); continue
    txt, say, sp = n; L.append(dict(text=txt, spec=dict(type=sp), **({"say": say} if say else {})))
json.dump(dict(P5, title="TikTok-Serie Bis zum Erdkern – Tag 10 (Deutsch)", voice="elevenlabs:Alexander - Deep TV Narrator (erd12/voice; Zeile 9 aus erd07)", lines=L), open("project.json", "w"), indent=1, ensure_ascii=False)
NI = [i for i, n in enumerate(NEW) if n]
os.makedirs("tmpv", exist_ok=True); shutil.copy("build_voice.py", "tmpv/build_voice.py")
json.dump({"lines": [L[i] for i in NI]}, open("tmpv/project.json", "w"), ensure_ascii=False)
if len(sys.argv) > 1 and sys.argv[1] == "assemble":   # nach build_voice: voice/ zusammensetzen
    os.makedirs("voice", exist_ok=True); dn = json.load(open("tmpv/voice/durs.json")); wn = json.load(open("tmpv/voice/words.json"))
    d5 = json.load(open("../erd07/voice/durs.json")); w5 = json.load(open("../erd07/voice/words.json")); D, W = [], []
    for i, n in enumerate(NEW):
        if n is None: k = 8; shutil.copy(f"../erd07/voice/{k:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(d5[k]); W.append(w5[k])
        else: j = NI.index(i); shutil.copy(f"tmpv/voice/{j:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(dn[j]); W.append(wn[j])
    json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
    for l, d in zip(L, D): print(round(d, 2), l["text"])
else:
    print(' <break time="1s"/> '.join(L[i].get("say", L[i]["text"]) for i in NI))
