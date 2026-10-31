# Short "Why you should never buy something that's too good to be true" (Victor Lustig sells the Eiffel Tower, 1925) -> project.json
# Sources (checked 2026-10-31):
# Smithsonian Magazine, "The Smoothest Con Man That Ever Lived" (2012): 1925 Paris; Lustig contacted the city's big scrap-metal
#   dealers; mark Andre Poisson paid cash plus a bribe; Lustig fled; returned later to repeat the scheme, fled to the US when police were tipped off.
# Wikipedia "Victor Lustig": posed as Deputy Director-General of the Ministry of Posts and Telegraphs, forged government stationery,
#   meeting in an expensive hotel; claimed upkeep was too costly and the tower would be sold for scrap; Poisson too ashamed to go to the police;
#   second attempt later in 1925 -> police informed, Lustig fled to the US. (Amount paid varies by source, therefore no figure in the video.)
# toureiffel.paris "15 essential things to know about the Eiffel Tower": metal structure ~7,300 t; originally planned for 20 years.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never buy something that's too good to be true. A man once bought the Eiffel Tower.", dict(type="hero"))
A("In nineteen twenty-five, con man Victor Lustig posed as a French government official.", dict(type="official"))
A("He told scrap dealers the tower would be torn down for its seven thousand tons of iron.", dict(type="iron"))
A("One dealer paid him, plus a secret bribe.", dict(type="bribe"))
A("Then Lustig vanished with the money.", dict(type="vanish", cut=True))
A("The buyer was too embarrassed to call the police, so Lustig came back to try again.", dict(type="shame"))
A("Would you have fallen for it?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never buy something that's too good to be true (Eiffel Tower scam)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
