# Beispielvideo neues TikTok-Format "Bis zum Erdkern" (Idee Alex 2026-11-15). Fakten: Britannica (Mantel bis ~2.900 km, innerer Kern ab ~5.100 km,
# Erdmitte ~6.370 km), Wikipedia Kola-Bohrung 12.262 m (1989). Beispiel-Arbeiter/Namen sind Platzhalter.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag 1: Wir graben bis zum Erdkern!", dict(type="intro", mood="bright"), say="Tag eins: Wir graben bis zum Erdkern!", say_map={"eins:": "1:"})
A("Die Regeln: Folgen macht dich zum Arbeiter, jedes Herz gräbt einen Meter, und in der Umfrage entscheidest du mit!", dict(type="regeln"))
A("Unsere ersten 5 Arbeiter legen los!", dict(type="dig", mood="bright"), say="Unsere ersten fünf Arbeiter legen los!", say_map={"fünf": "5"})
A("Bis zur Erdmitte sind es rund 6370 Kilometer.", dict(type="earth"), say="Bis zur Erdmitte sind es rund sechstausenddreihundertsiebzig Kilometer.", say_map={"sechstausenddreihundertsiebzig": "6370"})
A("Der Weltrekord liegt bei 12262 Metern. Den wollen wir knacken!", dict(type="record", mood="bright"), say="Der Weltrekord liegt bei zwölftausendzweihundertzweiundsechzig Metern. Den wollen wir knacken!", say_map={"zwölftausendzweihundertzweiundsechzig": "12262"})
A("Was kaufen wir zuerst: einen Presslufthammer oder einen Bagger? Stimmt ab!", dict(type="vote", mood="bright"))
P = dict(title="TikTok-Format Bis zum Erdkern – Beispiel (Deutsch)", _sources="Britannica Earth's layers; Wikipedia Kola Superdeep Borehole.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.2, crf=20, music=dict(style="playful", bpm=140, gain=0.11, ambience=0.0, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
