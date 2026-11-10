# TikTok-Serie "Roundhead Island" – Folge 5 (Tag 5). Zahlen von Alex (2026-11-10): 141 Einwohner (+13), Abstimmung Tag 4: Kanone 61 % / Frieden 39 % (36 Stimmen),
# 34 Likes = 340 € (Kasse 430 -> 770), Kanone kostet 500 € -> 270 €. Kommentare: @Mrxx will Gurken-Bewohner sein, @Always Team Dog will einen Hund.
# Story (von Alex freigegeben): Karte mit Nachbarinsel Squarehead Island, Rueckblick Katapult, Kanone gebaut, Probeschuss platscht vor Squarehead Island,
# Flaschenpost "Lasst uns handeln statt schiessen" -> Abstimmung Handel vs. Wettruesten.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag fünf auf Roundhead Island! Und gleich da drüben wohnen die Eckköpfe.", dict(type="map", mood="bright"))
A("Gestern bauten die Nachbarn ein Katapult.", dict(type="recap", mood="calm"))
A("Ihr habt abgestimmt: 61 Prozent für die Kanone!", dict(type="vote", mood="bright"), say="Ihr habt abgestimmt: einundsechzig Prozent für die Kanone!", say_map={"einundsechzig": "61"})
A("13 neue Bürger! Wir sind jetzt 141 Einwohner.", dict(type="crowd"), say="Dreizehn neue Bürger! Wir sind jetzt hunderteinundvierzig Einwohner.", say_map={"dreizehn": "13", "hunderteinundvierzig": "141"})
A("Eure 34 Herzen bringen 340 Euro!", dict(type="money"), say="Eure vierunddreißig Herzen bringen dreihundertvierzig Euro!", say_map={"vierunddreißig": "34", "dreihundertvierzig": "340"})
A("Ein neuer Bürger wollte eine Gurke sein. Wunsch erfüllt!", dict(type="gurke"))
A("Und wer sich einen Hund gewünscht hat: Hier ist er!", dict(type="hund", mood="bright"))
A("Die Kanone kostet 500 Euro. Bleiben 270 Euro.", dict(type="money2"), say="Die Kanone kostet fünfhundert Euro. Bleiben zweihundertsiebzig Euro.", say_map={"fünfhundert": "500", "zweihundertsiebzig": "270"})
A("Also: Alle Mann an die Mauer, wir bauen!", dict(type="build", mood="bright"))
A("Probeschuss! Drei, zwei, eins…", dict(type="countdown", mood="calm"))
A("Feuer!", dict(type="fire"))
A("Platsch! Knapp vor Squarehead Island.", dict(type="splash", mood="bright"))
A("Doch dann treibt eine Flaschenpost an unseren Strand.", dict(type="bottle", mood="calm"))
A("Die Eckköpfe schreiben: Lasst uns handeln statt schießen!", dict(type="letter"))
A("Also: Handeln wir mit den Eckköpfen?", dict(type="trade", mood="bright"))
A("Oder rüsten wir weiter auf, mit einer zweiten Kanone?", dict(type="arms"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 5 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 141 Einwohner, Abstimmung Kanone 61 %, 34 Likes auf Tag 4.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%", lang="de-DE",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
