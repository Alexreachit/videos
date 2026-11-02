# Short/TikTok "Why you should never flex your money on Instagram" (Ray Hushpuppi) -> project.json
# Sources (checked 2026-11-02):
# NBC News / Al Jazeera 8 Nov 2022: Ramon Abbas "Ray Hushpuppi", 2M+ Instagram followers, posts of private jets, ultra-expensive cars,
#   high-end clothes & watches; sentenced to 135 months (11+ years); admitted conspiring to launder over $300 million in 18 months
#   (much of the intended loss did not materialize); $1.7M restitution; arrested in Dubai in 2020.
# Quartz (2020) "How the FBI used Instagram and Snapchat to track down an alleged conman in Dubai": FBI matched his Instagram posts to
#   passport photos and used Instagram/Snapchat/Apple records to confirm identity and his Dubai residence (Palazzo Versace);
#   Dubai Police operation "Fox Hunt 2": six raids, twelve suspects, more than $40 million in cash seized.
# Wikipedia "Hushpuppi": arrested June 2020; >150M dirhams (~$40M) cash and 13 luxury cars seized; Gucci/Fendi/Louis Vuitton bags in posts.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never flex your money on Instagram.", dict(type="hero"))
A("Ray Hushpuppi showed two million followers private jets, luxury cars and designer bags.", dict(type="flex"))
A("But the FBI used his own posts to confirm who he was, and where he lived.", dict(type="fbi"))
A("In twenty twenty, Dubai police raided his crew and seized over forty million dollars in cash.", dict(type="raid", cut=True))
A("He admitted conspiring to launder over three hundred million dollars.", dict(type="launder"))
A("And got more than eleven years in prison.", dict(type="prison"))
A("Would you flex your money online?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never flex your money on Instagram (Hushpuppi)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
