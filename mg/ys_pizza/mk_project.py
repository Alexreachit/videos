# Short "Why you should never pay for pizza with Bitcoin" (Bitcoin Pizza Day 2010) -> project.json
# Sources (checked 2026-11-16):
# CoinDesk "What Is Bitcoin Pizza Day?" (B. George, 2022, upd. 2024): Floridian programmer Laszlo Hanyecz offered 10,000 BTC on
#   Bitcointalk (18 May 2010) for two large pizzas; 22 May 2010 a 19-year-old, Jeremy Sturdivant ("jercos"), took the deal;
#   pizzas made by Papa John's; the 10,000 BTC were worth about $41 at the time.
# BTC price: Fortune "Current price of Bitcoin" 13 Nov 2026; aktualita.co 15 Nov 2026 (~$62,000-65,000); cryptonomist 16 Nov 2026
#   -> 10,000 BTC = ~$620-650 million -> "over six hundred million dollars", "over three hundred million per pizza".
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never pay for pizza with Bitcoin.", dict(type="hero"))
A("In twenty ten, a programmer in Florida offered ten thousand Bitcoin for two pizzas.", dict(type="offer"))
A("Back then, all of it was worth about forty dollars.", dict(type="cheap"))
A("A nineteen-year-old took the deal and sent him two large pizzas.", dict(type="deal"))
A("The pizzas got eaten. The Bitcoin was gone.", dict(type="eaten"))
A("Today, those ten thousand Bitcoin are worth over six hundred million dollars.", dict(type="boom", cut=True))
A("That's over three hundred million dollars per pizza.", dict(type="slice"))
A("Would you have taken the pizza?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never pay for pizza with Bitcoin (Bitcoin Pizza Day)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
