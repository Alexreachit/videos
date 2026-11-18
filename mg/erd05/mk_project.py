# TikTok-Serie "Bis zum Erdkern" – Tag 3 (Aufbau von Alex freigegeben 2026-11-18).
# Zahlen (Alex, inkl. seiner Schaetzung +10 Follower/+15 Likes): 465 neue Follower -> 201+465 = 666 Arbeiter, 594 Likes, 124 Shares.
# 594*1 + 124*5 = 1.214 Schaufeln je Arbeiter; 666*1.214*0,1 m = 80.852,4 m (80,9 km). Gesamt: 0,1 + 804 + 80.852,4 = 81.656,5 m (81,7 km); Rest 6.370 - 81,66 = 6.288,3 km.
# Neuester Follower: Freddy_Mtb.69. Top-Kommentar: Blake (Diamanten / Diamantschaufel, 10x so tief wie normal, gilt ab Tag 4).
# Fakten: Kola-Bohrung 12.262 m (Wikipedia); Kontinentalkruste ~40 km (Britannica); Diamanten entstehen 150-700 km tief, Kimberlit-Magma bringt sie nach oben (GIA, Gems & Gemology Sommer 2019).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, say=None): L.append(dict(text=t, spec=s, **({"say": say} if say else {})))
A("Tag 3: Ihr seid komplett eskaliert!", dict(type="intro", mood="bright"), "Tag drei: Ihr seid komplett eskaliert!")
A("Wir sind jetzt 666 Arbeiter!", dict(type="crowd", mood="bright"), "Wir sind jetzt sechshundertsechsundsechzig Arbeiter!")
A("594 Likes und 124 Shares: Das sind 1.214 Schaufeln pro Arbeiter!", dict(type="calc"), "Fünfhundertvierundneunzig Likes und hundertvierundzwanzig Shares: Das sind tausendzweihundertvierzehn Schaufeln pro Arbeiter!")
A("Unser neuester Arbeiter: Freddy! Willkommen am Loch!", dict(type="newest", mood="bright"))
A("Und jetzt geht's runter! Wir sind tiefer als das tiefste Bohrloch der Welt!", dict(type="desc1"))
A("Wir sind durch die Erdkruste durch!", dict(type="desc2", mood="bright"))
A("80,9 Kilometer an einem Tag!", dict(type="desc3", mood="bright"), "Achtzig Komma neun Kilometer an einem Tag!")
A("Und Blake hatte recht: Diamanten!", dict(type="diamonds", mood="bright"))
A("Kimberlit-Gestein bringt sie aus über 150 Kilometern Tiefe nach oben.", dict(type="fact"), "Kimberlitgestein bringt sie aus über hundertfünfzig Kilometern Tiefe nach oben.")
A("Blakes Diamantschaufel gräbt zehnmal so tief wie eine normale!", dict(type="blake", mood="bright"))
A("Bis zum Erdkern fehlen noch über 6.288 Kilometer.", dict(type="earth", mood="calm"), "Bis zum Erdkern fehlen noch über sechstausendzweihundertachtundachtzig Kilometer.")
A("Der beste Kommentar bekommt jeden Tag ein Upgrade.", dict(type="rule"))
A("Was brauchen wir als Nächstes? Schreib es in die Kommentare!", dict(type="comment"))
P = dict(title="TikTok-Serie Bis zum Erdkern – Tag 3 (Deutsch)", _sources="Wikipedia (Kola-Bohrung 12.262 m), Britannica (Kruste ~40 km, Erdmitte ~6.370 km), GIA Gems & Gemology Summer 2019 (Diamanten 150-700 km, Kimberlit). Zahlen von Alex.",
         size=[1080, 1920], fps=30, scene="scene.html", voice="elevenlabs:Alexander - Deep TV Narrator (erd05/voice)", rate="+16%",
         lead=0.05, gap=0.12, tail=1.4, crf=20, music=dict(style="cinematic", bpm=100, gain=0.12, ambience=0.0, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.55, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines")
print(' <break time="0.8s" /> '.join((l.get("say") or l["text"]) for l in L))
