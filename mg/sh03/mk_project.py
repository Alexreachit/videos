# TikTok-Serie "Squarehead Island" – Folge 3 (Tag 3). Zahlen von Alex (2026-11-12, Screenshots Tag 2):
# 7 neue Follower -> 22 Einwohner, 14 Likes = 140 € (+170 € = 310 €), Abstimmung: Melonenfeld (einziger Abstimmungskommentar).
# Kommentare: TAMINO Doenermann, Henry Gurkenladen, Elias Goldkette/Cappy/blauer Pulli, Кристиан Uschanka, Jk777 Bodyguard.
# Story von Alex freigegeben. Stimme: ElevenLabs "DiMario - Energetic and Fun", voice/ via build_voice.py.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 3 auf Squarehead Island!", dict(type="map", mood="bright"), "Tag drei auf Squarehead Island!")
A("Ihr habt entschieden: Wir pflanzen ein Melonenfeld!", dict(type="feld", mood="bright"))
A("Wir sind jetzt 22 Einwohner!", dict(type="crowd", mood="bright"), "Wir sind jetzt zweiundzwanzig Einwohner!")
A("Eure Likes bringen 140 Euro. Macht 310 Euro in der Kasse!", dict(type="money"), "Eure Likes bringen hundertvierzig Euro. Macht dreihundertzehn Euro in der Kasse!")
A("Tamino will Dönermann werden: Hier ist deine Dönerbude!", dict(type="doener"))
A("Henry bekommt seinen Gurkenladen, direkt daneben!", dict(type="gurken"))
A("Elias kriegt Goldkette, Cappy und einen blauen Pulli!", dict(type="elias", mood="bright"))
A("Kristian bekommt seine Uschanka. Auf der Insel ist es zwar warm, aber egal!", dict(type="uschanka"))
A("Und Jk777 ist ab heute Bodyguard vom Vize-Bürgermeister!", dict(type="bodyguard"), "Und Jott Ka sieben sieben sieben ist ab heute Bodyguard vom Vize-Bürgermeister!")
A("Die erste Melone ist reif. Aber wohin mit der ganzen Ernte?", dict(type="reif", mood="calm"))
A("Bauen wir einen Markt für Melonen, Döner und Gurken?", dict(type="markt", mood="bright"))
A("Oder einen Brunnen, damit das Feld nie austrocknet?", dict(type="brunnen"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Squarehead Island – Tag 3 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 22 Einwohner, 14 Likes, Abstimmung Melonenfeld.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:DiMario - Energetic and Fun (sh03/voice, build_voice.py)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=150, gain=0.13, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print('\n'.join((l.get("say") or l["text"]) + ' <break time="1.0s" />' for l in L))
