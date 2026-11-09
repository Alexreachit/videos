# TikTok-Serie "Roundhead Island" – Folge 4 (Tag 4). Zahlen von Alex (2026-11-09): 128 Follower (unveraendert), Abstimmung: Mauer,
# 35 Likes = 350 € (Kasse 1580 -> 1930), Mauer kostet 1500 € -> 430 €. Story: Mauerbau, Nachtangriff prallt ab, Katapult -> Abstimmung Kanone vs. Friedensbote.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag vier auf Roundhead Island!", dict(type="day", mood="bright"))
A("Gestern hieß es: Mauer oder Frieden?", dict(type="recap", mood="calm"))
A("Und die Mauer hat gewonnen!", dict(type="vote", mood="bright"))
A("Wir sind 128 Einwohner. Holt eure Freunde, jeder Follower ist ein neuer Bürger!", dict(type="crowd"))
A("Eure 35 Likes bringen 350 Euro!", dict(type="money"))
A("Die Mauer kostet 1500 Euro. Bleiben 430 Euro.", dict(type="money2"))
A("Also: Alle Mann an die Steine!", dict(type="build", mood="bright"))
A("Benluca passt auf, dass alles schön gerade wird.", dict(type="build2"))
A("Und fertig ist die große Mauer!", dict(type="done", mood="bright"))
A("In der Nacht kommen die Eckköpfe mit Fackeln.", dict(type="night", mood="calm"))
A("Und krachen direkt gegen die Mauer!", dict(type="crash"))
A("Wütend rudern sie zurück. Unsere Mauer hält!", dict(type="hold", mood="bright"))
A("Doch am Morgen schaut Sam durchs Fernglas.", dict(type="morning", mood="calm"))
A("Die Nachbarn bauen ein riesiges Katapult!", dict(type="catapult"))
A("Bauen wir eine eigene Kanone?", dict(type="cannon", mood="bright"))
A("Oder schicken wir Benluca als Friedensboten mit einem Geschenk?", dict(type="peace"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 4 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 128 Follower, Abstimmung Mauer, 35 Likes auf Tag 3.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%", lang="de-DE",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
