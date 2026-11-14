# TikTok-Serie "Squarehead Island" – Folge 4 (Tag 4). Zahlen von Alex (2026-11-14, Screenshots Tag 3):
# 11 neue Follower -> 33 Bürger, 26 Likes = 260 € (Kasse 320 -> 580), Abstimmung Tag 3: Brunnen (Alex), Brunnen kostet 300 € ("egal wie viel") -> 280 €.
# Kommentare: Redbl0ssom Ärztin, ♣ grüner Jogginganzug + Friseurin, Kuno_2010 Surfschule, Lucas. Burgerbude (ohne Markenname), Germany Trophy Hunters Pilot.
# Story von Alex freigegeben. Stimme: ElevenLabs "DiMario - Energetic and Fun" (wie Tag 2) – voice/ via build_voice.py.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 4 auf Squarehead Island!", dict(type="map", mood="bright"), "Tag vier auf Squarehead Island!")
A("Die Regeln: Folgen macht dich zum Bürger, jedes Like bringt 10 Euro, und im Kommentar darfst du dir was wünschen!", dict(type="regeln"), "Die Regeln: Folgen macht dich zum Bürger, jedes Like bringt zehn Euro, und im Kommentar darfst du dir was wünschen!")
A("Ihr habt entschieden: Wir bauen einen Brunnen!", dict(type="vote", mood="bright"))
A("11 neue Bürger! Wir sind jetzt 33.", dict(type="crowd", mood="bright"), "Elf neue Bürger! Wir sind jetzt dreiunddreißig.")
A("Eure 26 Likes bringen 260 Euro. Macht 580 Euro in der Kasse!", dict(type="money"), "Eure sechsundzwanzig Likes bringen zweihundertsechzig Euro. Macht fünfhundertachtzig Euro in der Kasse!")
A("Hier ist unser Brunnen! Er kostet 300 Euro, bleiben 280 in der Kasse.", dict(type="build"), "Hier ist unser Brunnen! Er kostet dreihundert Euro, bleiben zweihundertachtzig in der Kasse.")
A("Redbl0ssom wird unsere Ärztin!", dict(type="arzt"), "Red Blossom wird unsere Ärztin!")
A("Die Kleeblatt-Bürgerin kriegt ihren grünen Jogginganzug und wird Friseurin!", dict(type="friseur"))
A("Kuno eröffnet seine Surfschule am Strand!", dict(type="surf", mood="bright"))
A("Lucas bekommt eine eigene Burgerbude!", dict(type="burger"))
A("Und Germany Trophy Hunters wird Pilot. Nur ein Flugzeug fehlt noch.", dict(type="pilot"), "Und Germany Trophy Hunters wird Pilot. Nur ein Flugzeug fehlt noch.")
A("Bauen wir einen Flugplatz für unseren Piloten?", dict(type="flug"))
A("Oder eine Praxis für unsere Ärztin?", dict(type="praxis"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Squarehead Island – Tag 4 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 33 Bürger, 26 Likes, Abstimmung Brunnen.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:DiMario - Energetic and Fun (sh04/voice, build_voice.py)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=150, gain=0.13, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print('\n'.join((l.get("say") or l["text"]) + ' <break time="1.0s" />' for l in L))
