# YouTube Short / TikTok: Felicity Ace – the ship that sank with 4,000 luxury cars -> project.json
# Sources (checked 2026-10-28):
# FreightWaves (01.03.2022) & gCaptain (01.03.2022): fire broke out Wed 16 Feb 2022 ~90 nm SW of the Azores; ~4,000 VW Group vehicles
#   (Audi, Bentley, Lamborghini, Porsche); route Emden (Germany) -> Davisville, Rhode Island (US); all 22 crew evacuated safely;
#   cargo valued at $401 million (Bloomberg); ship towed toward the Azores, sank Tue 1 Mar 2022 ~220 nm off the Azores;
#   lithium-ion batteries of EVs on board reportedly complicated firefighting.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("This ship sank with four thousand luxury cars on board.", dict(type="hero"))
A("In February twenty twenty-two, the Felicity Ace left Germany for the United States.", dict(type="map", stage=1))
A("It was carrying Porsches, Bentleys and Lamborghinis worth about four hundred million dollars.", dict(type="cargo"))
A("But near the Azores, a fire broke out.", dict(type="map", stage=2, cut=True))
A("All twenty-two crew members were rescued, but the ship kept burning for days.", dict(type="burn"))
A("Then, while it was being towed, it sank into the Atlantic.", dict(type="sink"))
A("Would you still ship your dream car across the ocean?", dict(type="hero", choice=True))
P = dict(title="Short: Felicity Ace – sank with 4,000 luxury cars (map + Gemini objects)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
