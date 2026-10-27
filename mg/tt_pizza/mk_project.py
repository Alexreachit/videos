# TikTok "10,000 bitcoin for two pizzas" (Bitcoin Pizza Day) -> project.json
# Sources (checked 2026-10-27):
# Nasdaq "Happy Bitcoin Pizza Day": 22 May 2010, Florida programmer Laszlo Hanyecz paid 10,000 BTC for two Papa John's pizzas, worth ~$41 then;
#   widely regarded as the first real-world purchase with bitcoin; celebrated yearly on 22 May as Bitcoin Pizza Day.
# BTC-Echo "10.000 Bitcoin fuer zwei Pizzen – was wurde aus Laszlo Hanyecz?": Jacksonville, Florida; request posted in a bitcoin forum, accepted 22 May 2010.
# BitcoinTalk thread "Pizza for bitcoins?" (18 May 2010): "a couple of pizzas.. like maybe 2 large ones".
# Price: CoinGecko via Analytics Insight 27.10.2026: 1 BTC = $79,769.40 -> 10,000 BTC = $797.7M (~"about eight hundred million"); 797.7M / 41 = 19.5 million times.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("This man paid almost eight hundred million dollars for two pizzas.",
  dict(type="hero", title=["$798 MILLION", "FOR TWO PIZZAS"], mood="tense"), rate="+12%")
A("In May twenty-ten, a programmer in Florida posted an offer on a bitcoin forum.",
  dict(type="map", cam=[-96, 38, 2.2], cam2=[-81.7, 29.5, 9], pins=[dict(at=[-81.66, 30.33], label="Florida, USA", col="red", delay=.45)], post=True))
A("Ten thousand bitcoin for two large pizzas. Back then, that was about forty-one dollars.",
  dict(type="deal"))
A("Four days later, someone took the deal, and two Papa John's pizzas arrived at his door.",
  dict(type="deliver", chips=["May 22, 2010", "Paid: 10,000 BTC"]))
A("It's seen as the first time anyone bought real goods with bitcoin.",
  dict(type="receipt", mood="calm"))
A("But here's the crazy part. Today, those ten thousand bitcoin are worth about eight hundred million dollars.",
  dict(type="chart", mood="tense", cut=True))
A("That's more than nineteen million times what he paid.",
  dict(type="money"))
A("And every year on May twenty-second, people celebrate it as Bitcoin Pizza Day.",
  dict(type="party"))
A("Would you have kept the bitcoin, or eaten the pizza? Tell me below, and remember:",
  dict(type="hero", choice=True))
P = dict(title="TikTok: 10,000 bitcoin for two pizzas (map + Sam + detailed coded scenes + chart)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+10%",
         lead=0.1, gap=0.2, tail=0.1, crf=22, music=dict(style="tt", bpm=96, gain=0.2, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
