# TikTok-Serie "Roundhead Island" – Folge 10 (Tag 10). Zahlen von Alex (2026-11-15, Screenshots Tag 9): 22 Likes = 220 € (Kasse 460 -> 680),
# 5 neue Follower -> 176 Einwohner. Polizeistation 720 € -> es fehlen 40 €, die der Kinderpunsch-Stand (Wunsch Always Team Dog) verdient.
# Kommentare: KaistürmtdasFeld Soldat, Alina Inselärztin, Always Team Dog Kinderpunsch-Stand, Edition Dönerladen. Neue Umfrage: Flugplatz oder Freibad.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
CHIEF = "Mex"
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag 10 auf Roundhead Island!", dict(type="map", mood="bright"), say="Tag zehn auf Roundhead Island!", say_map={"zehn": "10"})
A("Die Regeln: Folgen macht dich zum Einwohner, jedes Herz bringt 10 Euro, und im Kommentar darfst du dir was wünschen!", dict(type="regeln"), say="Die Regeln: Folgen macht dich zum Einwohner, jedes Herz bringt zehn Euro, und im Kommentar darfst du dir was wünschen!", say_map={"zehn": "10"})
A("5 neue Bürger! Wir sind jetzt 176 Einwohner.", dict(type="crowd", mood="bright"), say="Fünf neue Bürger! Wir sind jetzt hundertsechsundsiebzig Einwohner.", say_map={"fünf": "5", "hundertsechsundsiebzig": "176"})
A("Eure 22 Herzen bringen 220 Euro. Macht 680 Euro.", dict(type="money"), say="Eure zweiundzwanzig Herzen bringen zweihundertzwanzig Euro. Macht sechshundertachtzig Euro.", say_map={"zweiundzwanzig": "22", "zweihundertzwanzig": "220", "sechshundertachtzig": "680"})
A("Für die Polizeistation fehlen nur noch 40 Euro!", dict(type="gap", mood="calm"), say="Für die Polizeistation fehlen nur noch vierzig Euro!", say_map={"vierzig": "40"})
A("Da hilft Always Team Dog: Sein Kinderpunsch-Stand verdient die 40 Euro!", dict(type="punch", mood="bright"), say="Da hilft Always Team Dog: Sein Kinderpunschstand verdient die vierzig Euro!", say_map={"vierzig": "40", "kinderpunschstand": "Kinderpunsch-Stand"})
A("Die Polizeistation ist fertig!", dict(type="station", mood="bright"))
A(f"Und unser neuer Polizeichef ist {CHIEF}!", dict(type="chief"))
A("Alina wird unsere Inselärztin im Krankenhaus.", dict(type="wish"))
A("Kai wird Soldat und bewacht den Strand.", dict(type="wish"))
A("Und Edition bekommt einen Dönerladen!", dict(type="wish", mood="bright"))
A("Bei 200 Einwohnern wartet die Überraschung. Nur noch 24!", dict(type="surprise", mood="bright"), say="Bei zweihundert Einwohnern wartet die Überraschung. Nur noch vierundzwanzig!", say_map={"zweihundert": "200", "vierundzwanzig": "24"})
A("Was bauen wir als Nächstes: Flugplatz oder Freibad?", dict(type="chef"))
A("Stimmt in der Umfrage ab!", dict(type="poll", mood="bright"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 10 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 22 Likes, 5 neue Follower, Kommentare Tag 9.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
