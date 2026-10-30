# TikTok/Short "Why you should never buy something just because everyone else is" (Tulip mania 1637) -> project.json
# Sources (checked 2026-10-30):
# History.com, Dave Roos "There Never Was a Real Tulip Fever" (on Anne Goldgar, "Tulipmania", 2007):
#   prices spiked Dec 1636 - Feb 1637; Switzer bulb rose 12-fold; most expensive recorded sale 5,000 guilders
#   = "the going rate for a nice house in 1637"; 300 guilders = what a skilled craftsman earned in a year; Haarlem centre of the trade.
# Wikipedia "Tulip mania": collapse by end of first week of February 1637; first sign Feb 3 in Haarlem, auction found no buyers;
#   fall "faster and more dramatic than the rise"; contracts traded without bulbs changing hands ("windhandel").
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never buy something just because everyone else is.", dict(type="hero"))
A("In the sixteen-thirties, tulips became the hottest thing to trade in Holland.", dict(type="holland"))
A("Within weeks, one bulb got twelve times more expensive.", dict(type="rise"))
A("The priciest one sold for five thousand guilders. That's the price of a nice house.", dict(type="house"))
A("A craftsman earned about three hundred a year.", dict(type="wage"))
A("Then in February, a Haarlem auction found no buyers, and prices crashed.", dict(type="crash", cut=True))
A("Would you have bought a tulip?", dict(type="hero", choice=True))
P = dict(title="TikTok: Why you should never buy something just because everyone else is (Tulip mania)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
