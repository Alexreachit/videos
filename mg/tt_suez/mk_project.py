# TikTok "One ship blocked $9.6B a day" (Ever Given, Suez 2021) -> project.json
# Sources (checked 2026-10-26):
# Bloomberg via Al Jazeera 25.03.2021: ~$9.6B/day of traffic held up (westbound $5.1B, eastbound $4.5B), Ever Given 400 m.
# Boskalis/SMIT via gCaptain: grounded 23 Mar 2021, refloated 29 Mar 2021 15:05, ~30,000 m3 sand dredged, 11 harbour tugs + 2 seagoing tugs.
# NZ MFAT "The Importance of the Suez Canal to Global Trade" (18.04.2021): ~12% of global trade, 30% of container traffic,
#   ~450 vessels held up, Cape of Good Hope detour adds ~9,000 km and 6-14 days.
# Empire State Building: 443 m to tip (381 m roof) -> "almost as long as ... is tall".
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
SUEZ = [32.55, 30.0]
A("This one ship blocked nine-point-six billion dollars of world trade. Every single day.",
  dict(type="map", cam=[45, 24, 1.0], cam2=[33, 29, 6.0], pins=[dict(at=SUEZ, label="Suez Canal · Egypt", col="red", delay=.45)],
       counter=dict(to=9.6, d=1, pre="$", suf="B", label="of trade blocked per day"), title=["$9.6 BILLION", "OF TRADE · EVERY DAY"], mood="tense"),
  rate="+12%", pitch="+2Hz")
A("In March twenty twenty-one, the Ever Given got stuck sideways in the Suez Canal.",
  dict(type="canal", step="stuck"), rate="+10%")
A("It's four hundred meters long. That's almost as long as the Empire State Building is tall.",
  dict(type="tower"), rate="+10%", pitch="+3Hz")
A("And about twelve percent of all world trade goes through this one canal.",
  dict(type="map", cam=[62, 26, 1.05], route="suez", pins=[dict(at=[121.5, 31.2], label="Shanghai", col="gold", delay=.1), dict(at=[4.4, 51.9], label="Rotterdam", col="gold", delay=.7, dy=-.2)], share=True, mood="calm"),
  rate="+10%")
A("Within days, around four hundred fifty ships were stuck waiting.",
  dict(type="queue"), rate="+12%", pitch="+4Hz")
A("The only other way is all the way around Africa. That's about nine thousand extra kilometers, and up to two weeks longer.",
  dict(type="map", cam=[40, 8, 0.82], route="cape", mood="tense", cut=True), rate="+10%")
A("So diggers and dredgers removed thirty thousand cubic meters of sand, and tugboats pulled for six days.",
  dict(type="canal", step="dig", mood="calm"), rate="+10%")
A("On March twenty-ninth, the ship finally broke free!",
  dict(type="canal", step="free", mood="bright", cut=True), rate="+14%", pitch="+7Hz", volume="+8%")
A("Would you have waited, or gone around Africa? Comment below, and remember:",
  dict(type="map", cam=[45, 24, 1.0], choice=True, mood="tense"), rate="+10%", pitch="+3Hz")
P = dict(title="TikTok: One ship blocked $9.6B a day (Ever Given / Suez, map + animation)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+10%",
         lead=0.1, gap=0.2, tail=0.1, crf=22, music=dict(style="tt", bpm=96, gain=0.2, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
