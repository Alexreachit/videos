# TikTok-Serie "Squarehead Island" – Folge 1 (Tag 1). Community-Serie nach Vorlage FC Asche (Alex 2026-11-05):
# 1 Follow = 1 Buerger, Top-Kommentar entscheidet, was als Naechstes gebaut wird. Fiktive Story, keine Fakten-Behauptungen.
# Neu: echte 3D-Welt (mg/lib/gl3d.js, WebGL) + animierter Sam (mg/lib/samrig.js).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag eins: Ich habe gerade mein eigenes Land gegründet.", dict(type="fly", mood="calm"))
A("Willkommen auf Squarehead Island!", dict(type="sign"))
A("Einwohner: genau einer. Ich.", dict(type="pop"))
A("Aber jeder neue Follower wird ein Bürger.", dict(type="follow"))
A("Unser Ziel: das reichste Land der Welt.", dict(type="goal", mood="bright"))
A("Aber schau dich um. Keine Häuser, keine Bank, nicht mal eine Straße.", dict(type="empty", mood="calm"))
A("Folg jetzt, und du bekommst Reisepass Nummer eins.", dict(type="passport"))
A("Unsere Staatskasse: zwanzig Euro... und eine Melone.", dict(type="treasury"))
A("Und für jeden Like kommen zehn Euro in die Kasse!", dict(type="likes"))
A("Also, was bauen wir zuerst? Ein Feld oder ein Haus?", dict(type="choice"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Squarehead Island – Tag 1 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen).",
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=150, gain=0.13, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
