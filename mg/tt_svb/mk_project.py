# TikTok "$42 billion left one bank in one day" (Silicon Valley Bank, March 2023) -> project.json
# Sources (checked 2026-10-26/27, same as YT 11):
# Fed Vice Chair Barr, Senate testimony 28.03.2023 (via CNBC): $42B withdrawn on March 9, ~$100B scheduled for March 10 -> $142B of ~$175B deposits = 81%.
# Wikipedia "Collapse of Silicon Valley Bank" (call report data): HQ Santa Clara, CA; ~86% of deposits uninsured; $1.8B loss on securities sale announced March 8 (evening);
#   closed by California DFPI / FDIC receivership on the morning of March 10 (<2 days later); 3rd-largest US bank failure.
# FDIC / Treasury / Fed joint statement 12.03.2023: systemic risk exception, all depositors fully protected.
# FDIC: $250,000 per depositor, per insured bank, per ownership category.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
SC = [-121.96, 37.35]
A("Why you should never keep all your money in one bank.",
  dict(type="hero", title=["WHY YOU SHOULD NEVER", "KEEP ALL YOUR MONEY", "IN ONE BANK"], mood="tense"))
A("In twenty twenty-three, forty-two billion dollars left Silicon Valley Bank in one day.",
  dict(type="map", cam=[-98, 39, 2.0], cam2=[-121.5, 37.0, 10], pins=[dict(at=SC, label="Silicon Valley Bank", col="red", delay=.3)]))
A("It started with a one-point-eight-billion-dollar loss.",
  dict(type="loss"))
A("Founders panicked in group chats and pulled everything out.",
  dict(type="panic"))
A("Less than two days later, the bank was shut down.",
  dict(type="closed", cut=True))
A("And eighty-six percent of the money wasn't insured.",
  dict(type="pie"))
A("Only a last-minute government rescue saved them.",
  dict(type="rescue"))
A("Would you have pulled your money out?",
  dict(type="hero", choice=True))
P = dict(title="TikTok: $42 billion left one bank in one day (SVB, Sam + detailed coded scenes)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=22, music=dict(style="tt", bpm=96, gain=0.2, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
