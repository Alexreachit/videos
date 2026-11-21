# TikTok-Serie "Bis zum Erdkern" – Tag 5 (Aufbau von Alex freigegeben 2026-11-21).
# Zahlen (Alex, Tag-4-Video): 36 Likes, 13 Shares -> 36*1 + 13*5 = 101 Schaufeln je Arbeiter. Follower: 750 + 8 neue = 758 (angenommen).
# 757 Arbeiter * 101 * 0,1 m = 7.645,7 m; Blakes Diamantschaufel 101 * 1,0 m = 101 m -> heute 7.746,7 m (7,7 km).
# Gesamt: 86.134,6 + 7.746,7 = 93.881,3 m (93,9 km); Rest 6.370 - 93,88 = 6.276,1 km. Neuester Follower: Ben. Kein Top-Kommentar.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 5: Wir graben ein Loch bis zum Erdkern!", dict(type="intro", mood="bright"), "Tag fünf: Wir graben ein Loch bis zum Erdkern!")
A("Die Regeln: Folgen macht dich zum Arbeiter, jedes Like ist eine Schaufel, jeder Share sogar fünf!", dict(type="rules"))
A("Wir sind jetzt 758 Arbeiter!", dict(type="count", mood="bright"), "Wir sind jetzt siebenhundertachtundfünfzig Arbeiter!")
A("Unser neuester Arbeiter: Ben! Willkommen am Loch!", dict(type="newest", mood="bright"))
A("36 Likes und 13 Shares: 101 Schaufeln pro Arbeiter!", dict(type="calc"), "Sechsunddreißig Likes und dreizehn Shares: hunderteins Schaufeln pro Arbeiter!")
A("Gestern 4,5 Kilometer, heute 7,7. Fast doppelt so tief!", dict(type="desc"), "Gestern vier Komma fünf Kilometer, heute sieben Komma sieben. Fast doppelt so tief!")
A("Wir sind jetzt fast 100 Kilometer tief!", dict(type="bottom", mood="bright"), "Wir sind jetzt fast hundert Kilometer tief!")
A("Bis zum Erdkern fehlen noch über 6.276 Kilometer.", dict(type="earth", mood="calm"), "Bis zum Erdkern fehlen noch über sechstausendzweihundertsechsundsiebzig Kilometer.")
A("Was brauchen wir als Nächstes? Schreib es in die Kommentare!", dict(type="comment"))
P = dict(title="TikTok-Serie Bis zum Erdkern – Tag 5 (Deutsch)", _sources="Zahlen von Alex; Erdradius ~6.370 km (Britannica).",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:Alexander - Deep TV Narrator (erd07/voice)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="cinematic", bpm=100, gain=0.12, ambience=0.0, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print(' <break time="1.0s" /> '.join((l.get("say") or l["text"]) for l in L))
