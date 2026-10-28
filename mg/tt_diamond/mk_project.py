# TikTok "Why you should never buy a diamond ring" -> project.json
# Sources (checked 2026-10-28):
# American RadioWorks "With This Ring" / Marketing Society "A tagline is forever": "A diamond is forever" written 1947 by Frances Gerety (N.W. Ayer) for De Beers;
#   the campaign made the diamond engagement ring the standard in the US.
# Marketplace (22.02.2013) "Diamonds are not a jewel of an investment": owner of a $10,000 ring – best offer "35 percent of what I paid".
# TheStreet via Yahoo Finance (02.04.2026) "Price of diamonds crashes to lowest level this century": natural 1-carat avg ~$6,000 (2021) -> ~$4,200 (2025) ≈ -30%;
#   lab-grown diamonds cost 73-83% less than natural (BriteCo). Lab-grown = same carbon crystal as natural (chemically identical).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never buy a diamond ring.", dict(type="hero"))
A("In nineteen forty-seven, an ad agency gave De Beers four words: a diamond is forever.", dict(type="ad"))
A("That slogan made a diamond ring the must-have for every engagement.", dict(type="must"))
A("But try selling one. One owner was offered just thirty-five percent of what he paid.", dict(type="resell"))
A("And natural diamond prices fell about thirty percent since twenty twenty-one.", dict(type="crash", cut=True))
A("Lab-grown diamonds are chemically the same, and cost up to eighty percent less.", dict(type="lab"))
A("Would you still buy a natural diamond?", dict(type="hero", choice=True))
P = dict(title="TikTok: Why you should never buy a diamond ring (Sam + Gemini objects + code animation)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=22, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
