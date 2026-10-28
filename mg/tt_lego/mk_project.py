# TikTok "Why you should never throw away your old LEGO" -> project.json
# Sources (checked 2026-10-28):
# HSE University news "LEGO sets: a more profitable investment than gold" + working paper Dobrynskaya & Kishilova (HSE, 2020):
#   2,322 new, unopened sets released 1987-2015; secondary-market prices of retired sets grow ~10-11% per year; beat gold, stocks, bonds;
#   resale prices usually start rising 2-3 years after a set is retired.
# Mental Floss (study coverage): 2007 Millennium Falcon set, originally $499.99, sold for nearly $4,000 in 2016.
# (No LEGO logo or Star Wars ship drawn – generic bricks/boxes only.)
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never throw away your old LEGO.",
  dict(type="hero", mood="bright"))
A("A study of over two thousand sets found something crazy.",
  dict(type="study"))
A("Unopened LEGO grew about eleven percent per year.",
  dict(type="grow"))
A("That beat stocks, bonds, and even gold.",
  dict(type="race"))
A("This set cost five hundred dollars in two thousand seven.",
  dict(type="price"))
A("Nine years later, people paid almost four thousand.",
  dict(type="price"))
A("Just keep the box sealed, because prices usually rise after a set is retired.",
  dict(type="sealed"))
A("Would you open it, or keep it sealed?",
  dict(type="hero", choice=True))
P = dict(title="TikTok: Why you should never throw away your old LEGO (Sam + detailed coded scenes)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=22, music=dict(style="tt", bpm=100, gain=0.2, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
