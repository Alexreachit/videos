# TikTok-Serie "Roundhead Island" – Folge 9 (Tag 9). Zahlen von Alex (2026-11-14, Screenshots Tag 8): 24 Likes = 240 € (Kasse 220 -> 460),
# 4 neue Follower -> 171 Einwohner, Umfrage: Polizei Revier 71 % / Flugplatz 29 % (7 Stimmen). Polizeistation kostet 720 € -> es fehlen 260 € (26 Herzen).
# Kommentare: Simon Security Chef, 😴 Architekt (Benedih unlesbar -> weggelassen). Neue Umfrage: Polizeichef Mex oder Simon. Regeln am Anfang (Alex 13.11.).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Tag 9 auf Roundhead Island!", dict(type="map", mood="bright"), say="Tag neun auf Roundhead Island!", say_map={"neun": "9"})
A("Die Regeln: Folgen macht dich zum Einwohner, jedes Herz bringt 10 Euro, und im Kommentar darfst du dir was wünschen!", dict(type="regeln"), say="Die Regeln: Folgen macht dich zum Einwohner, jedes Herz bringt zehn Euro, und im Kommentar darfst du dir was wünschen!", say_map={"zehn": "10"})
A("Ihr habt entschieden: Wir bauen die Polizeistation!", dict(type="vote", mood="bright"))
A("4 neue Bürger! Wir sind jetzt 171 Einwohner.", dict(type="crowd"), say="Vier neue Bürger! Wir sind jetzt hunderteinundsiebzig Einwohner.", say_map={"vier": "4", "hunderteinundsiebzig": "171"})
A("Eure 24 Herzen bringen 240 Euro. Macht 460 Euro.", dict(type="money"), say="Eure vierundzwanzig Herzen bringen zweihundertvierzig Euro. Macht vierhundertsechzig Euro.", say_map={"vierundzwanzig": "24", "zweihundertvierzig": "240", "vierhundertsechzig": "460"})
A("Aber die Polizeistation kostet 720 Euro. Es fehlen noch 260!", dict(type="gap", mood="calm"), say="Aber die Polizeistation kostet siebenhundertzwanzig Euro. Es fehlen noch zweihundertsechzig!", say_map={"siebenhundertzwanzig": "720", "zweihundertsechzig": "260"})
A("Die Baustelle steht schon!", dict(type="site", mood="bright"))
A("Unser neuer Architekt plant alles!", dict(type="arch"))
A("Simon wird Sicherheitschef und bewacht die Baustelle.", dict(type="security"))
A("Mit 26 Herzen ist die Wache fertig!", dict(type="ziel"), say="Mit sechsundzwanzig Herzen ist die Wache fertig!", say_map={"sechsundzwanzig": "26"})
A("Und bei 200 Einwohnern wartet die Überraschung. Nur noch 29!", dict(type="surprise", mood="bright"), say="Und bei zweihundert Einwohnern wartet die Überraschung. Nur noch neunundzwanzig!", say_map={"zweihundert": "200", "neunundzwanzig": "29"})
A("Wer wird Polizeichef: Mex oder Simon?", dict(type="chef"))
A("Stimmt in der Umfrage ab!", dict(type="poll", mood="bright"))
P = dict(title="TikTok-Serie Roundhead Island – Tag 9 (Deutsch)",
         _sources="Fiktive Community-Serie (keine Faktenbehauptungen). Zahlen von Alex: Umfrage Polizei 71 %, 24 Likes, 171 Einwohner.",
         size=[1080, 1920], fps=60, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=18, music=dict(style="playful", bpm=150, gain=0.11, ambience=0.02, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
