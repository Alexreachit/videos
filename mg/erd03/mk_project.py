# TikTok-Serie "Bis zum Erdkern" – Tag 1 (Story von Alex freigegeben 2026-11-16).
# Regeln (Alex): 1 Follower = 1 Arbeiter am Loch, 1 Like = jeder Arbeiter schaufelt 1x, 1 Share = jeder 5x; Start mit 1 Person (Alex = "Chef", Cartoon).
# 1 Schaufel = 10 cm (Vorschlag, von Alex angenommen). 6.370 km / 0,1 m = 63.700.000 Schaufeln.
# Fakten: Britannica (Erdmitte ~6.370 km, Kontinentalkruste ~40 km, Mantel bis ~2.900 km, innerer Kern ab ~5.100 km).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag 1: Wir graben ein Loch bis zum Erdkern!", dict(type="intro", mood="bright"), say="Tag eins: Wir graben ein Loch bis zum Erdkern!", say_map={"eins": "1", "eins:": "1:"})
A("Noch grabe ich ganz allein.", dict(type="alone", mood="calm"))
A("Jeder Follower wird ein neuer Arbeiter am Loch.", dict(type="ghost"))
A("Jedes Like: Jeder Arbeiter schaufelt einmal. Jeder Share: fünfmal!", dict(type="rules"))
A("Und so weit ist es bis zum Erdkern:", dict(type="zoom"))
A("6.370 Kilometer!", dict(type="earth", mood="bright"), say="Sechstausenddreihundertsiebzig Kilometer!", say_map={"sechstausenddreihundertsiebzig": "6.370"})
A("Mit 10 Zentimetern pro Schaufel sind das fast 64 Millionen Mal schaufeln.", dict(type="number"), say="Mit zehn Zentimetern pro Schaufel sind das fast vierundsechzig Millionen Mal schaufeln.", say_map={"zehn": "10", "vierundsechzig": "64"})
A("Also folg mir, damit ich nicht allein graben muss!", dict(type="follow", mood="bright"))
A("Welches Werkzeug brauchen wir?", dict(type="comment"))
P = dict(title="TikTok-Serie Bis zum Erdkern – Tag 1 realistisch (Deutsch)", _sources="Britannica: Earth's layers (crust ~40 km continental, mantle to ~2,900 km, inner core from ~5,100 km, centre ~6,370 km).",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:Alexander - Deep TV Narrator (erd03/voice, build_voice.py)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=140, gain=0.11, ambience=0.0, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
