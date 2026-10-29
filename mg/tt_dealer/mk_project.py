# TikTok "Why you should never tell a car dealer how you're paying" -> project.json
# Sources (checked 2026-10-29):
# WardsAuto (27.04.2026) on Q1 2026 Presidio-NCM Average Dealership Performance Benchmark (4,000+ US franchised dealers):
#   F&I income per retail unit $1,727; new-vehicle gross profit per vehicle $1,781 -> "almost as much".
# American Banker: dealer markup on the bank's buy rate "often ranges from 2 to 2.5 percentage points" (dealer participation).
# Own calculations (standard annuity): $40,000 at 7%: 60 months -> $792/mo, $7,523 interest; 84 months -> $604/mo, $10,711 interest (+$3,188).
#   $40,000 over 60 months at 6% vs 8%: total interest $6,399 vs $8,663 -> +$2,265.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never tell a car dealer how you're paying.", dict(type="hero"))
A("Dealers make almost as much on financing and add-ons as on the car itself.", dict(type="profit"))
A("Ask for low monthly payments, and they can just stretch the loan, so you pay thousands more.", dict(type="stretch"))
A("They can also add about two percentage points to your rate.", dict(type="rate", cut=True))
A("On forty thousand dollars, that's over two thousand extra.", dict(type="extra"))
A("So negotiate the price first, and bring a loan offer from your own bank.", dict(type="tips"))
A("Did you know this trick?", dict(type="hero", choice=True))
P = dict(title="TikTok: Why you should never tell a car dealer how you're paying",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
