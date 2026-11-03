# Short/TikTok "Why you should never laugh at a small idea" (Blockbuster vs. Netflix) -> project.json
# Sources (checked 2026-11-03):
# Marketplace (8 Sep 2020, interview Reed Hastings, "No Rules Rules"): in 2000 Hastings + Marc Randolph proposed that Blockbuster buy
#   Netflix for $50 million; CEO John Antioco turned it down; Blockbuster then ~$6 billion revenue and nearly 9,000 stores,
#   Netflix ~100 employees, ~300,000 subscribers, lost $57 million that year.
# NZ Herald / Marc Randolph ("That Will Never Work"): Antioco was "struggling not to laugh" at the $50M offer.
# Wikipedia "Blockbuster LLC": peak 9,094 stores (2004); filed for bankruptcy protection 2010 (Sept 2010); one franchise store left (Bend, Oregon).
# Netflix market cap: Nasdaq ~$256 billion (2 Nov 2026), CompaniesMarketCap ~$260 billion (Nov 2026), StockAnalysis $270B (23 Oct 2026)
#   -> "about two hundred fifty billion dollars".
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never laugh at a small idea.", dict(type="hero"))
A("In two thousand, Netflix offered to sell itself to Blockbuster for fifty million dollars.", dict(type="offer"))
A("Blockbuster had nearly nine thousand stores.", dict(type="giant"))
A("Netflix mailed DVDs in red envelopes, and lost fifty-seven million that year.", dict(type="tiny"))
A("Blockbuster's CEO said no, and could barely keep from laughing.", dict(type="laugh"))
A("In twenty ten, Blockbuster went bankrupt.", dict(type="bust"))
A("Today, Netflix is worth about two hundred fifty billion dollars.", dict(type="boom", cut=True))
A("Would you have laughed too?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never laugh at a small idea (Blockbuster vs Netflix)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
