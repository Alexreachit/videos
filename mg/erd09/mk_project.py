# TikTok-Serie "Bis zum Erdkern" – Tag 7 (Aufbau von Alex freigegeben 2026-11-23; Stimme kommt spaeter -> geschaetzte Dauern, spaeter Bild-Umzuordnung).
# Zahlen (Alex, Tag-6-Video): 45 Likes, 6 Shares -> 45 + 6*5 = 75 Schaufeln je Arbeiter. Follower 770 + 23 = 793 (angenommen).
# 792 * 75 * 0,1 m = 5.940 m; Blake 75 * 1 m = 75 m -> heute 6.015 m (6,0 km). Gesamt 103.385,1 + 6.015 = 109.400,1 m (109,4 km). Rest 6.370 - 109,40 = 6.260,6 km.
# Neuester Follower: Lukas. Top-Kommentar: Emilio "Ich habe Diamanten gefunden" -> bekommt Diamantschaufel (graebt ab Tag 8 mit 1 m).
import json, os, shutil, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P5 = json.load(open("../erd07/project.json")); d5 = json.load(open("../erd07/voice/durs.json")); w5 = json.load(open("../erd07/voice/words.json"))
NEW = [("Tag 7: Wir graben ein Loch bis zum Erdkern!", "Tag sieben: Wir graben ein Loch bis zum Erdkern!", "intro"),
       None,
       ("Wir sind jetzt 793 Arbeiter!", "Wir sind jetzt siebenhundertdreiundneunzig Arbeiter!", "count"),
       ("Neu dabei: Lukas! Willkommen am Loch!", None, "newest"),
       ("45 Likes, 6 Shares: 75 Schaufeln!", "Fünfundvierzig Likes, sechs Shares: fünfundsiebzig Schaufeln!", "calc"),
       ("Emilio hat Diamanten gefunden! Dafür bekommt er eine Diamantschaufel!", None, "emilio"),
       ("Heute 6 Kilometer. Jetzt sind wir 109 Kilometer tief!", "Heute sechs Kilometer. Jetzt sind wir hundertneun Kilometer tief!", "desc"),
       ("Noch über 6.260 Kilometer!", "Noch über sechstausendzweihundertsechzig Kilometer!", "earth"),
       None]
RATE = 15.5
os.makedirs("voice", exist_ok=True); L, D, W = [], [], []
for i, n in enumerate(NEW):
    if n is None:
        k = 1 if i == 1 else 8; shutil.copy(f"../erd07/voice/{k:02d}.mp3", f"voice/{i:02d}.mp3")
        L.append(dict(P5["lines"][k], spec=dict(type="rules" if i == 1 else "comment"))); D.append(d5[k]); W.append(w5[k]); continue
    txt, say, sp = n; s = say or txt; d = round(len(s) / RATE + .15, 3)
    ws = txt.split(); wt = [max(2, len(re.sub(r"[^\wäöüÄÖÜß]", "", w))) + 1.5 for w in ws]; tot = sum(wt); acc = 0; wl = []
    for w, k in zip(ws, wt): t0 = d * acc / tot; acc += k; wl.append([w, round(t0, 3), round(d * acc / tot * .97, 3)])
    L.append(dict(text=txt, spec=dict(type=sp), **({"say": say} if say else {}))); D.append(d); W.append(wl)
json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
json.dump(dict(P5, title="TikTok-Serie Bis zum Erdkern – Tag 7 (Deutsch)", voice="elevenlabs:Alexander - Deep TV Narrator (erd09/voice, vorlaeufig)", lines=L), open("project.json", "w"), indent=1, ensure_ascii=False)
for l, d in zip(L, D): print(round(d, 2), l["text"])
