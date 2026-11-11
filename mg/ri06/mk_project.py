# TikTok-Serie "Roundhead Island" – Folge 6 (Tag 6). Zahlen von Alex (2026-11-11, Screenshots): Abstimmung Tag 5: Handeln 72 % / Eckkoepfe attackieren 28 % (18 Stimmen),
# 28 Likes = 280 € (Kasse 270 -> 550), 10 neue Follower -> 151 Einwohner. Kommentare: @Juless!! will Munition sein, @In_Verse will ein Eckkopf sein, deezy will ein Panzer sein.
# Story (von Alex freigegeben, Frage geaendert): Hook Kanonen-Flug, Karte, Handel Kokosnuesse <-> Melonen, Wuensche, Abstimmung Rathaus vs. 10 Haeuser.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Ein Bürger wollte Munition sein. Wunsch erfüllt!", dict(type="hook", mood="bright"))
A("Tag 6 auf Roundhead Island!", dict(type="map", mood="bright"), say="Tag sechs auf Roundhead Island!", say_map={"sechs": "6"})
A("Ihr habt entschieden: 72 Prozent für Handeln!", dict(type="vote", mood="bright"), say="Ihr habt entschieden: zweiundsiebzig Prozent für Handeln!", say_map={"zweiundsiebzig": "72"})
A("10 neue Bürger! Wir sind jetzt 151 Einwohner.", dict(type="crowd"), say="Zehn neue Bürger! Wir sind jetzt hunderteinundfünfzig Einwohner.", say_map={"zehn": "10", "hunderteinundfünfzig": "151"})
A("Eure 28 Herzen bringen 280 Euro.", dict(type="money"), say="Eure achtundzwanzig Herzen bringen zweihundertachtzig Euro.", say_map={"achtundzwanzig": "28", "zweihundertachtzig": "280"})
A("Jetzt sind 550 Euro in der Kasse!", dict(type="money2"), say="Jetzt sind fünfhundertfünfzig Euro in der Kasse!", say_map={"fünfhundertfünfzig": "550"})
A("Und der fliegende Bürger hatte Kokosnüsse dabei.", dict(type="coco", mood="calm"))
A("Zurück kommt ein Boot voller Melonen!", dict(type="boat", mood="bright"))
A("Ein anderer wollte ein Eckkopf sein. Jetzt ist er unser Botschafter drüben!", dict(type="eckkopf"), say="Ein anderer wollte ein Eck-Kopf sein. Jetzt ist er unser Botschafter drüben!", say_map={"eck-kopf": "Eckkopf"})
A("Und wer ein Panzer sein wollte: Hier ist unser Schildkröten-Panzer!", dict(type="panzer", mood="bright"))
A("Mit 550 Euro bauen wir jetzt etwas Großes.", dict(type="plan", mood="calm"), say="Mit fünfhundertfünfzig Euro bauen wir jetzt etwas Großes.", say_map={"fünfhundertfünfzig": "550"})
A("Ein Rathaus für den Bürgermeister?", dict(type="rathaus"))
A("Oder 10 Häuser für die Bürger?", dict(type="haeuser"), say="Oder zehn Häuser für die Bürger?", say_map={"zehn": "10"})
A("Stimmt in der Umfrage ab!", dict(type="poll", mood="bright"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 6 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: Abstimmung Handeln 72 %, 28 Likes, 151 Einwohner.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%", lang="de-DE",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
