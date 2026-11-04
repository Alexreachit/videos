# Short/TikTok "Why the milk is always at the very back of the supermarket" (supermarket tricks) -> project.json
# Sources (checked 2026-11-04):
# Mental Floss "Why Grocery Stores Put Dairy in the Back": layout makes shoppers walk past other products ("building the basket");
#   counterpoint Michael Pollan (NPR 2014): cold chain / delivery trucks unload at the back, so coolers sit there.
# CNN via KVIA (21 May 2022) "Why stores always put candy and soda near the cash register": shoppers spent $6 billion in checkout
#   areas in a year (IRI); brands pay stores "slotting fees" for the best spots incl. eye-level shelves, end caps, checkout.
# HubSpot "music psychology marketing" on Milliman (1982, Journal of Marketing): supermarket, 9 weeks, slow (60 BPM) vs fast (108 BPM)
#   music -> customers spent 38% more with slow music.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why the milk is always at the very back of the supermarket.", dict(type="hero"))
A("To reach it, you walk past dozens of other products. It's called building the basket.", dict(type="map"))
A("Eye level? Brands pay to be there.", dict(type="eyelevel"))
A("And shoppers spend about six billion dollars a year just at the checkout.", dict(type="checkout"))
A("In one study, slow music made shoppers spend thirty-eight percent more.", dict(type="music", cut=True))
A("To be fair, the coolers are also near the delivery doors.", dict(type="fair"))
A("Did you notice any of these tricks?", dict(type="hero", choice=True))
P = dict(title="Short: Why the milk is always at the back of the supermarket",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
