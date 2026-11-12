# TikTok-Serie "Roundhead Island" – Folge 7 (Tag 7). Zahlen von Alex (2026-11-12, Screenshots Tag 6): 31 Likes = 310 € (Kasse 550 -> 860),
# 9 neue Follower -> 160 Einwohner, Umfrage: 10 Haeuser (von Alex bestaetigt). Kommentare: furz "wo bin ich", In_Verse Poststation auf der Eckkopf-Insel,
# River_the_person will Lehrer sein, R will ein Stein sein. Story von Alex freigegeben, neue Frage: Polizeistation oder Krankenhaus (Hafen gibt es schon, Alex 12.11.).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Einer wollte ein Stein sein. Wunsch erfüllt!", dict(type="hook", mood="bright"))
A("Tag 7 auf Roundhead Island!", dict(type="map", mood="bright"), say="Tag sieben auf Roundhead Island!", say_map={"sieben": "7"})
A("Ihr habt entschieden: 10 Häuser für die Bürger!", dict(type="vote", mood="bright"), say="Ihr habt entschieden: zehn Häuser für die Bürger!", say_map={"zehn": "10"})
A("9 neue Bürger! Wir sind jetzt 160 Einwohner.", dict(type="crowd"), say="Neun neue Bürger! Wir sind jetzt hundertsechzig Einwohner.", say_map={"neun": "9", "hundertsechzig": "160"})
A("Eure 31 Herzen bringen 310 Euro.", dict(type="money"), say="Eure einunddreißig Herzen bringen dreihundertzehn Euro.", say_map={"einunddreißig": "31", "dreihundertzehn": "310"})
A("Jetzt sind 860 Euro in der Kasse!", dict(type="money2"), say="Jetzt sind achthundertsechzig Euro in der Kasse!", say_map={"achthundertsechzig": "860"})
A("Also bauen wir: 10 Häuser!", dict(type="build", mood="bright"), say="Also bauen wir: zehn Häuser!", say_map={"zehn": "10"})
A("Und die Bürger ziehen sofort ein.", dict(type="movein"))
A("Ein Bürger macht drüben eine Poststation auf.", dict(type="post", mood="calm"))
A("Und schon fliegt der erste Brief zu uns!", dict(type="letter", mood="bright"))
A("Ein anderer wollte Lehrer sein: Hier ist unsere Schule!", dict(type="school"))
A("Und wer sich sucht: Hier bist du!", dict(type="find", mood="bright"))
A("Wir haben jetzt Häuser, eine Schule und eine Post.", dict(type="overview", mood="calm"))
A("Aber keine Polizei und kein Krankenhaus.", dict(type="missing"))
A("Bauen wir eine Polizeistation?", dict(type="polizei"))
A("Oder ein Krankenhaus für alle?", dict(type="krankenhaus"))
A("Stimmt in der Umfrage ab!", dict(type="poll", mood="bright"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 7 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: Umfrage 10 Haeuser, 31 Likes, 160 Einwohner.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%", lang="de-DE",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
