# TikTok-Serie "Squarehead Island" – Folge 2 (Tag 2). Zahlen von Alex (2026-11-11, Screenshots Tag 1 auf dem Nebelstein-Account):
# 14 neue Follower -> 15 Einwohner (mit Sam), 15 Likes = 150 € (+20 € Startkapital = 170 €), Abstimmung: Haus (von Alex bestaetigt).
# Kommentare: 👑-Nutzer will Buergermeister werden, Jk777 will Sonnenbrille, MTB+GAMING "wohne ich schon da", julien will in die Armee, Elias "wo bin ich".
# Story von Alex freigegeben. Stimme: ElevenLabs "DiMario - Energetic and Fun" (wie Tag 1), voice/ via build_voice.py.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 2 auf Squarehead Island!", dict(type="map", mood="bright"), "Tag zwei auf Squarehead Island!")
A("Gestern habe ich mein eigenes Land gegründet.", dict(type="recap", mood="calm"))
A("Unser Ziel: das reichste Land der Welt.", dict(type="goal"))
A("Und ihr habt entschieden: Wir bauen ein Haus!", dict(type="vote", mood="bright"))
A("Wir sind jetzt schon 15 Einwohner!", dict(type="crowd", mood="bright"), "Wir sind jetzt schon fünfzehn Einwohner!")
A("Eure Likes bringen 150 Euro. Macht 170 Euro in der Kasse!", dict(type="money"), "Eure Likes bringen hundertfünfzig Euro. Macht hundertsiebzig Euro in der Kasse!")
A("Für eine Villa reicht das nicht…", dict(type="villa", mood="calm"))
A("Aber für eine kleine Hütte! Alle Mann, wir bauen!", dict(type="build", mood="bright"))
A("Einer will Bürgermeister werden. Du wirst mein Vize-Bürgermeister!", dict(type="vize"))
A("Hier ist deine Sonnenbrille!", dict(type="brille", mood="bright"))
A("Und ja: Du wohnst schon hier!", dict(type="wohnt"))
A("Wer in die Armee will: Du bist der Erste in der Wache!", dict(type="armee"))
A("Und wer sich sucht: Hier bist du!", dict(type="elias", mood="bright"))
A("Nur ein Problem: 15 Leute, eine Hütte und nur eine Melone.", dict(type="problem", mood="calm"), "Nur ein Problem: fünfzehn Leute, eine Hütte und nur eine Melone.")
A("Also: Pflanzen wir ein Melonenfeld?", dict(type="feld", mood="bright"))
A("Oder bauen wir ein Boot zur Nachbarinsel?", dict(type="boot"))
A("Der Top-Kommentar entscheidet.", dict(type="comment"))
P = dict(title="TikTok-Serie Squarehead Island – Tag 2 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: 15 Einwohner, 15 Likes, Abstimmung Haus.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:DiMario - Energetic and Fun (sh02/voice, build_voice.py)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="playful", bpm=150, gain=0.13, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print('\n'.join((l.get("say") or l["text"]) + ' <break time="1.0s" />' for l in L))
