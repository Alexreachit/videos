# Short/TikTok "Why you should never bet against the internet" (GameStop short squeeze, Jan 2021) -> project.json
# Sources (checked 2026-10-31): Wikipedia "GameStop short squeeze":
#   GME at $17.25 at the start of January 2021; intraday all-time high $483.00 on Jan 28, 2021 (pre-market briefly >$500);
#   ~140% of the public float sold short as of Jan 22, 2021; r/wallstreetbets grew to 6 million users by Jan 29;
#   short sellers' losses reported at $6 billion on Jan 26; Melvin Capital: Citadel & partners $2B + Point72 $750M = $2.75B,
#   fund down 53% in January.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never bet against the internet.", dict(type="hero"))
A("In January twenty twenty-one, hedge funds bet that GameStop's stock would crash.", dict(type="bets"))
A("They had shorted about a hundred forty percent of its tradable shares.", dict(type="short"))
A("Then a Reddit forum with millions of members started buying.", dict(type="reddit"))
A("The stock exploded from seventeen dollars to over four hundred eighty.", dict(type="explode", cut=True))
A("Short sellers lost billions. One hedge fund needed a two point seven five billion dollar rescue.", dict(type="loss"))
A("Would you have bought GameStop?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never bet against the internet (GameStop)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
