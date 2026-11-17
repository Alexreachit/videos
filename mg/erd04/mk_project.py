# TikTok-Serie "Bis zum Erdkern" – Tag 2 (Story von Alex freigegeben 2026-11-17).
# Zahlen von Alex: 201 Follower = 201 Arbeiter, 35 Likes, 1 Share. Regeln: Like = jeder Arbeiter 1 Schaufel, Share = 5, 1 Schaufel = 10 cm.
# Rechnung: (35*1 + 1*5) = 40 Schaufeln je Arbeiter; 201 * 40 * 0,1 m = 804 m (+0,1 m von Tag 1 = 804,1 m). Rest: 6.370 km - 0,804 km = 6.369,2 km.
# Fakten: Burj Khalifa 828 m (Guinness World Records / CTBUH); Erdmitte ~6.370 km (Britannica).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 2: Wir graben ein Loch bis zum Erdkern!", dict(type="intro", mood="bright"), "Tag zwei: Wir graben ein Loch bis zum Erdkern!")
A("Gestern war ich allein. Heute sind wir schon 201!", dict(type="crowd", mood="bright"), "Gestern war ich allein. Heute sind wir schon zweihunderteins!")
A("Ihr habt 35 Likes und einen Share dagelassen. Das sind 40 Schaufeln pro Arbeiter.", dict(type="calc"), "Ihr habt fünfunddreißig Likes und einen Share dagelassen. Das sind vierzig Schaufeln pro Arbeiter.")
A("201 mal 40 Schaufeln mal 10 Zentimeter: Wir sind 804 Meter tiefer!", dict(type="shaft", mood="bright"), "Zweihunderteins mal vierzig Schaufeln mal zehn Zentimeter: Wir sind achthundertvier Meter tiefer!")
A("Das ist fast so tief, wie das höchste Gebäude der Welt hoch ist.", dict(type="compare"))
A("Auf der Erde sieht man davon noch nichts. Es fehlen noch über 6.369 Kilometer.", dict(type="earth", mood="calm"), "Auf der Erde sieht man davon noch nichts. Es fehlen noch über sechstausenddreihundertneunundsechzig Kilometer.")
A("Folg mir und werde Arbeiter. Jedes Like und jeder Share bringt uns tiefer!", dict(type="follow", mood="bright"))
A("Was finden wir da unten wohl als Erstes?", dict(type="comment"))
A("Schreib es in die Kommentare!", dict(type="comment2"))
P = dict(title="TikTok-Serie Bis zum Erdkern – Tag 2 realistisch (Deutsch)", _sources="Guinness World Records: Burj Khalifa 828 m. Britannica: Erdmittelpunkt ~6.370 km. Zahlen von Alex: 201 Follower, 35 Likes, 1 Share.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:Alexander - Deep TV Narrator (erd04/voice, build_voice.py)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="cinematic", bpm=96, gain=0.12, ambience=0.0, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print(' <break time="1.0s" /> '.join((l.get("say") or l["text"]) for l in L))
