# TikTok-Serie "Roundhead Island" – Folge 8 (Tag 8). Zahlen von Alex (2026-11-13, Screenshots Tag 7): 36 Likes = 360 € (Kasse 860 -> 1220),
# 7 neue Follower -> 167 Einwohner, Umfrage: Krankenhaus 78 % / Polizeistation 22 % (18 Stimmen). Kommentare: Hoppy Pilot (Eurofighter -> erfundener Kampfjet,
# kein Markenname), Christos Schuhladen, Damian_MTB Zirkus, Mex Polizist. Story von Alex freigegeben, neue Frage: Polizeistation oder Flugplatz.
# Nachtrag Alex 13.11.: Krankenhaus kostet 1000 € (Kasse 1220 -> 220), Polizei/Flugplatz je 720 € = 50 Likes noetig, Ueberraschung bei 200 Einwohnern.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Einer will Kampfjet-Pilot werden. Abheben!", dict(type="hook", mood="bright"))
A("Tag 8 auf Roundhead Island!", dict(type="map", mood="bright"), say="Tag acht auf Roundhead Island!", say_map={"acht": "8"})
A("Die Regeln: Folgen macht dich zum Einwohner, jedes Herz bringt 10 Euro, und im Kommentar darfst du dir was wünschen!", dict(type="regeln"), say="Die Regeln: Folgen macht dich zum Einwohner, jedes Herz bringt zehn Euro, und im Kommentar darfst du dir was wünschen!", say_map={"zehn": "10"})
A("Ihr habt entschieden: Wir bauen ein Krankenhaus!", dict(type="vote", mood="bright"))
A("7 neue Bürger! Wir sind jetzt 167 Einwohner.", dict(type="crowd"), say="Sieben neue Bürger! Wir sind jetzt hundertsiebenundsechzig Einwohner.", say_map={"sieben": "7", "hundertsiebenundsechzig": "167"})
A("Eure 36 Herzen bringen 360 Euro.", dict(type="money"), say="Eure sechsunddreißig Herzen bringen dreihundertsechzig Euro.", say_map={"sechsunddreißig": "36", "dreihundertsechzig": "360"})
A("Jetzt sind 1220 Euro in der Kasse!", dict(type="money2"), say="Jetzt sind tausendzweihundertzwanzig Euro in der Kasse!", say_map={"tausendzweihundertzwanzig": "1220"})
A("Und da steht es: unser Krankenhaus!", dict(type="build", mood="bright"))
A("Das Krankenhaus hat 1000 Euro gekostet. Bleiben 220 Euro in der Kasse.", dict(type="kosten", mood="calm"), say="Das Krankenhaus hat tausend Euro gekostet. Bleiben zweihundertzwanzig Euro in der Kasse.", say_map={"tausend": "1000", "zweihundertzwanzig": "220"})
A("Christos bekommt seinen Schuhladen!", dict(type="shoe"))
A("Damian holt einen Zirkus auf die Insel!", dict(type="circus", mood="bright"))
A("Und Mex wird unser erster Polizist. Nur eine Wache hat er noch nicht.", dict(type="mex"))
A("Bauen wir jetzt eine Polizeistation für Mex?", dict(type="polizei"))
A("Oder einen Flugplatz für unseren Piloten?", dict(type="flug"))
A("Beide kosten 720 Euro. Dafür brauchen wir 50 Herzen!", dict(type="ziel"), say="Beide kosten siebenhundertzwanzig Euro. Dafür brauchen wir fünfzig Herzen!", say_map={"siebenhundertzwanzig": "720", "fünfzig": "50"})
A("Und bei 200 Einwohnern wartet eine riesige Überraschung!", dict(type="surprise", mood="bright"), say="Und bei zweihundert Einwohnern wartet eine riesige Überraschung!", say_map={"zweihundert": "200"})
A("Stimmt in der Umfrage ab!", dict(type="poll", mood="bright"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 8 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: Umfrage Krankenhaus 78 %, 36 Likes, 167 Einwohner.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
