# TikTok-Serie "Bis zum Erdkern" – Tag 8 (Aufbau von Alex freigegeben 2026-11-25).
# Zahlen (Alex, Tag-7-Video): 52 Likes, 5 Shares -> 52 + 5*5 = 77 Schaufeln je Arbeiter. Follower 793 + 38 = 831. Neuester Follower: Jason.
# 829 * 77 * 0,1 m = 6.383,3 m; Blake 77 * 1 m = 77 m; Emilio (Diamantschaufel, 10x) 77 * 1 m = 77 m; Bohrer (Wunsch der Community) 3.000 m
# -> heute 9.537,3 m (9,5 km). Gesamt 109.400,1 + 9.537,3 = 118.937,4 m (118,9 km). Rest 6.370 - 118,94 = 6.251,1 km.
import json, os, shutil, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P5 = json.load(open("../erd07/project.json"))
NEW = [("Tag 8: Wir graben ein Loch bis zum Erdkern!", "Tag acht: Wir graben ein Loch bis zum Erdkern!", "intro"),
       None,
       ("Wir sind jetzt 831 Arbeiter!", "Wir sind jetzt achthunderteinunddreißig Arbeiter!", "count"),
       ("Neu dabei: Jason! Willkommen am Loch!", None, "newest"),
       ("52 Likes, 5 Shares: 77 Schaufeln!", "Zweiundfünfzig Likes, fünf Shares: siebenundsiebzig Schaufeln!", "calc"),
       ("Ihr habt euch einen Bohrer gewünscht. Hier ist er!", None, "drill"),
       ("Und Emilio gräbt mit der Diamantschaufel zehnmal so tief!", None, "emilio"),
       ("Heute 9,5 Kilometer. Jetzt sind wir fast 119 Kilometer tief!", "Heute neuneinhalb Kilometer. Jetzt sind wir fast hundertneunzehn Kilometer tief!", "desc"),
       ("Noch über 6.250 Kilometer!", "Noch über sechstausendzweihundertfünfzig Kilometer!", "earth"),
       None]
L = []
for i, n in enumerate(NEW):
    if n is None:
        k = 1 if i == 1 else 8; L.append(dict(P5["lines"][k], spec=dict(type="rules" if i == 1 else "comment"))); continue
    txt, say, sp = n; L.append(dict(text=txt, spec=dict(type=sp), **({"say": say} if say else {})))
json.dump(dict(P5, title="TikTok-Serie Bis zum Erdkern – Tag 8 (Deutsch)", voice="elevenlabs:Alexander - Deep TV Narrator (erd10/voice; Zeilen 1+9 aus erd07)", lines=L), open("project.json", "w"), indent=1, ensure_ascii=False)
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
