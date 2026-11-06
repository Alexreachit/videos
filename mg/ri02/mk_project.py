# TikTok-Serie "Roundhead Island" – Folge 2 (Tag 2). Story von Alex freigegeben 2026-11-06:
# Rückblick Tag 1 -> Community hat Hafen gewählt -> 108 Follower = 108 Einwohner, 86 Likes = 860 € (+20 € = 880 €)
# -> reicht nur für kleinen Steg + Boot -> Maskottchen Benluca (Kommentar) -> nichts zu essen (Dönermann-Wunsch aus Kommentaren)
# -> Abstimmung: mit dem Boot fischen oder Nachbarinseln ausrauben. Fiktive Story, keine Faktenbehauptungen.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag zwei auf Roundhead Island!", dict(type="day", mood="bright"))
A("Rückblick: Gestern habe ich mein eigenes Land gegründet.", dict(type="recap", mood="calm"))
A("Unser Ziel: das reichste Land der Welt.", dict(type="goal"))
A("Jeder Follower wird ein Einwohner. Startkapital: zwanzig Euro und eine Kokosnuss.", dict(type="recap2"))
A("Dann habt ihr abgestimmt: Wir bauen einen Hafen!", dict(type="vote"))
A("Und jetzt sind wir schon hundertacht Einwohner!", dict(type="crowd", mood="bright"))
A("Eure Likes bringen achthundertsechzig Euro!", dict(type="money"))
A("Für einen großen Hafen reicht das nicht...", dict(type="bigharbor", mood="calm"))
A("Aber für einen kleinen Steg und ein Boot!", dict(type="pier", mood="bright"))
A("Und wir haben ein Maskottchen: Ben Luca, die Krabbe!", dict(type="mascot"))
A("Nur ein Problem: Wir haben nichts zu essen.", dict(type="hunger", mood="calm"))
A("Viele wollen einen Dönermann... aber wir haben nur eine Kokosnuss.", dict(type="doner"))
A("Also: Fahren wir mit dem Boot fischen?", dict(type="fish", mood="bright"))
A("Oder rauben wir die Nachbarinseln aus?", dict(type="raid"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 2 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 108 Follower, 86 Likes auf Tag 1.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
