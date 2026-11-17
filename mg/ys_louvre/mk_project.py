# Short "They robbed the Louvre in 7 minutes" (Louvre jewel heist, 19 Oct 2025) -> project.json
# Sources (checked 2026-11-17):
# ABC News "The Louvre heist: A timeline of how it happened" (21 Oct 2025): Sunday 19 Oct 2025; "Seven minutes is all it took";
#   truck with extendable ladder / basket lift on the Seine side; two thieves dressed as construction workers cut a window of the
#   Apollo Gallery with an angle grinder; "four masked thieves stole eight pieces of jewelry ... valued at $102 million";
#   escaped on two motorbikes; dropped the crown of Empress Eugenie ("adorned with over a thousand diamonds"), recovered damaged.
# AFP via Express Tribune / Kuwait Times (20 Oct 2026, one year later): "eight irreplaceable items", "an estimated $100 million";
#   all four men arrested within 10 days, "the four main suspects are in jail awaiting trial"; jewels "remain listed as missing
#   in Interpol's database of stolen artworks"; French crown jewels worth 88 million euros.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Seven minutes. That's all it took to rob the Louvre.", dict(type="hero"))
A("In October twenty twenty-five, a truck with a ladder lift parked right below a window.", dict(type="climb"))
A("Two men in work vests rode it up and cut through the glass.", dict(type="climb"))
A("Inside, they grabbed eight pieces of the French crown jewels.", dict(type="grab"))
A("Worth about one hundred million dollars.", dict(type="value", cut=True))
A("On the way out, they dropped a crown with over a thousand diamonds.", dict(type="drop"))
A("Four suspects were arrested. But one year later, the jewels are still missing.", dict(type="missing"))
A("Where do you think they are?", dict(type="hero", choice=True))
P = dict(title="Short: They robbed the Louvre in 7 minutes (Louvre jewel heist 2025)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
