# TikTok-Serie "Roundhead Island" – Folge 3 (Tag 3). Zahlen von Alex (2026-11-07): +20 Follower (108 -> 128),
# 76 % fuer "Nachbarinsel ausrauben", 50 neue Likes = 500 € (Kasse 80 -> 580). Story: naechtlicher Raubzug, 1000 € Gold,
# Nachbarn wollen Rache -> Abstimmung Mauer vs. Frieden. Fiktive Story, keine Faktenbehauptungen.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag drei auf Roundhead Island!", dict(type="day", mood="bright"))
A("Gestern habt ihr entschieden: fischen oder die Nachbarinsel ausrauben?", dict(type="recap", mood="calm"))
A("76 Prozent sagen: Ausrauben!", dict(type="vote", mood="bright"))
A("Und wir sind jetzt 128 Einwohner!", dict(type="crowd"))
A("Eure 50 Likes bringen 500 Euro!", dict(type="money"))
A("Also schleichen wir heute Nacht mit dem Boot rüber.", dict(type="night", mood="calm"))
A("Benluca, die Krabbe, spioniert vorne am Strand.", dict(type="spy"))
A("Und da: eine riesige Schatzkiste!", dict(type="chest", mood="bright"))
A("Wir schnappen sie und rudern so schnell wir können zurück!", dict(type="escape"))
A("Darin: 1000 Euro in Gold!", dict(type="gold"))
A("Doch dann geht auf der Nachbarinsel das Licht an...", dict(type="lights", mood="calm"))
A("Die Nachbarn haben uns gesehen. Und sie wollen Rache!", dict(type="revenge"))
A("Also: Bauen wir eine riesige Mauer?", dict(type="wall", mood="bright"))
A("Oder schließen wir Frieden und geben das Gold zurück?", dict(type="peace"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 3 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 128 Follower, 76 % Ausrauben, 50 Likes auf Tag 2.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
