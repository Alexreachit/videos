# TikTok-Serie "Bis zum Erdkern" – Tag 4 (Aufbau von Alex freigegeben 2026-11-19).
# Zahlen (Alex): 750 Follower = 750 Arbeiter; Tag-3-Video: 49 Likes, 2 Shares -> 49*1 + 2*5 = 59 Schaufeln je Arbeiter.
# 749 Arbeiter * 59 * 0,1 m = 4.419,1 m; Blakes Diamantschaufel 59 * 1,0 m = 59 m -> heute 4.478,1 m (4,5 km).
# Gesamt: 81.656,5 + 4.478,1 = 86.134,6 m (86,1 km); Rest 6.370 - 86,13 = 6.283,9 km.
# Neuester Follower: fosa. Top-Kommentar: Lena (pinker Helm, nur fuer sie).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 4: Wir sind jetzt 750 Arbeiter!", dict(type="intro", mood="bright"), "Tag vier: Wir sind jetzt siebenhundertfünfzig Arbeiter!")
A("Unser neuester Arbeiter: fosa! Willkommen am Loch!", dict(type="newest", mood="bright"), "Unser neuester Arbeiter: Fosa! Willkommen am Loch!")
A("49 Likes und 2 Shares: 59 Schaufeln pro Arbeiter.", dict(type="calc"), "Neunundvierzig Likes und zwei Shares: neunundfünfzig Schaufeln pro Arbeiter.")
A("Und Blakes Diamantschaufel gräbt heute zum ersten Mal mit: zehnmal so tief!", dict(type="blake", mood="bright"))
A("Gestern 80,9 Kilometer, heute nur 4,5. Mehr Likes, mehr Tiefe!", dict(type="desc"), "Gestern achtzig Komma neun Kilometer, heute nur vier Komma fünf. Mehr Likes, mehr Tiefe!")
A("Lena wollte einen pinken Helm. Bitteschön, Lena!", dict(type="lena", mood="bright"))
A("Bis zum Erdkern fehlen noch über 6.283 Kilometer.", dict(type="earth", mood="calm"), "Bis zum Erdkern fehlen noch über sechstausendzweihundertdreiundachtzig Kilometer.")
A("Der beste Kommentar bekommt jeden Tag ein Upgrade.", dict(type="rule"))
A("Was brauchen wir als Nächstes? Schreib es in die Kommentare!", dict(type="comment"))
P = dict(title="TikTok-Serie Bis zum Erdkern – Tag 4 (Deutsch)", _sources="Zahlen von Alex; Erdradius ~6.370 km (Britannica).",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:Alexander - Deep TV Narrator (erd06/voice)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="cinematic", bpm=100, gain=0.12, ambience=0.0, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print(' <break time="1.0s" /> '.join((l.get("say") or l["text"]) for l in L))
