# Short "The Great Brink's Robbery" (Boston, 1950) -> project.json
# Stil: 3D-Toon-Welt (gl3d) + 2D-Rundkopf-Figuren (samrig) wie ys_bridge/ys_cooper (Referenz R-mWVMM-LAs).
# Sources (checked 2026-11-24):
# FBI "A Byte Out of History: The Brink's Robbery" (fbi.gov/news/stories/2007/february/brinks_020907): Jan 17, 1950, Brinks Inc. in Boston;
#   "more than $1.2 million in cash and another $1.5 million in checks and other securities"; O'Keefe "bitter", did not get his "fair share",
#   after "several unsuccessful attempts on his life" told "the full story of the 11-man job" to FBI agents; Oct 5, 1956 jury: guilty.
# FBI artifact "Brinks Robbery Cap": "chauffeur's caps, gloves, masks, pea coats" + rubber-soled shoes; months casing the building;
#   >$2.7 million in cash, checks, money orders, securities; O'Keefe confessed January 1956; state grand jury indicted 11 men Jan 11, 1956.
# Wikipedia "Great Brink's Robbery": 11 men; entered 7:10 pm with copied keys (removed each lock, had a key made, returned it), left ~7:30
#   (~20 min); $1,218,211.29 cash + $1,557,183.83 checks/securities; rubber Halloween masks, chauffeur caps, pea coats; largest robbery
#   in U.S. history at the time; hitman shot O'Keefe (survived), he talked Jan 1956; arrests "just five days before the statute of
#   limitations was to run out"; eight got life imprisonment.
# Smithsonian Magazine (2025) + History.com (This Day in History, Jan 17): Halloween masks, chauffeur's caps, peacoats; ~20 min (Smithsonian);
#   copied keys; indictments "just days before Massachusetts' six-year statute of limitations expired"; eight life sentences (History.com).
# Not used (sources disagree): exact amount ever recovered.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never cheat your partners in crime.", dict(shot="hero"))
A("In 1950, eleven men planned to rob the Brink's vault in Boston.", dict(shot="roof"))
A("For months, they secretly copied the key to every door.", dict(shot="keys"))
A("Then, in Halloween masks, they walked right in.", dict(shot="enter"))
A("In about twenty minutes, they took over a million dollars in cash.", dict(shot="vault", cut=True))
A("But one of them, Specs, felt cheated out of his share.", dict(shot="split"))
A("When the gang sent a hitman, he told the FBI everything.", dict(shot="fbi"))
A("Days before time ran out, they were charged. Eight got life.", dict(shot="prison"))
A("Would you have kept quiet?", dict(shot="end", choice=True))
P = dict(title="Short: Great Brink's Robbery 1950 (3D+2D style)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.1, tail=0.4, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.5, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
