# TikTok-Serie "Squarehead Island" – Folge 5 (Tag 5). Zahlen von Alex (2026-11-15, Screenshots Tag 4):
# 8 neue Follower -> 41 Bürger, 20 Likes = 200 € (Kasse 280 -> 480), Umfrage: Praxis 55 % / Flugplatz 45 % (11 Stimmen). Praxis kostet 400 € -> 80 €.
# Kommentare: Gaming+Motor Pizza Riha, Elias Burger-Restaurant (Marke weggelassen -> Partner in Lucas' Burgerbude), Louie King. Story von Alex freigegeben.
# Stimme: ElevenLabs "DiMario - Energetic and Fun" (wie Tag 2-4) – voice/ via build_voice.py.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 5 auf Squarehead Island!", dict(type="map", mood="bright"), "Tag fünf auf Squarehead Island!")
A("Die Regeln: Folgen macht dich zum Bürger, jedes Like bringt 10 Euro, und im Kommentar darfst du dir was wünschen!", dict(type="regeln"), "Die Regeln: Folgen macht dich zum Bürger, jedes Like bringt zehn Euro, und im Kommentar darfst du dir was wünschen!")
A("Ihr habt entschieden: Wir bauen die Praxis!", dict(type="vote", mood="bright"))
A("8 neue Bürger! Wir sind jetzt 41.", dict(type="crowd", mood="bright"), "Acht neue Bürger! Wir sind jetzt einundvierzig.")
A("Eure 20 Likes bringen 200 Euro. Macht 480 Euro in der Kasse!", dict(type="money"), "Eure zwanzig Likes bringen zweihundert Euro. Macht vierhundertachtzig Euro in der Kasse!")
A("Hier ist die Praxis! Sie kostet 400 Euro, bleiben 80 in der Kasse.", dict(type="build"), "Hier ist die Praxis! Sie kostet vierhundert Euro, bleiben achtzig in der Kasse.")
A("Gaming+Motor eröffnet seine Pizzeria: Pizza Riha!", dict(type="pizza", mood="bright"), "Gaming plus Motor eröffnet seine Pizzeria: Pizza Riha!")
A("Elias wird Partner in Lucas' Burgerbude, und die Bude wird größer!", dict(type="burger"))
A("Und Louie wird unser König!", dict(type="king", mood="bright"))
A("Der Flugplatz war knapp dran: nur 45 Prozent!", dict(type="knapp", mood="calm"), "Der Flugplatz war knapp dran: nur fünfundvierzig Prozent!")
A("Bauen wir jetzt den Flugplatz für unseren Piloten?", dict(type="flug"))
A("Oder ein Schloss für unseren König?", dict(type="schloss"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Squarehead Island – Tag 5 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 41 Bürger, 20 Likes, Umfrage Praxis 55 %.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:DiMario - Energetic and Fun (sh05/voice, build_voice.py)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=150, gain=0.13, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print('\n'.join((l.get("say") or l["text"]) + ' <break time="1.0s" />' for l in L))
