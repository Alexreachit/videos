# YT 11 – "What Happens When Your Bank Collapses?" -> project.json
# Sources (checked 2026-10-26):
# Fed Vice Chair Barr testimony via CNBC 28.03.2023: SVB $42B withdrawn Mar 9, $100B scheduled Mar 10 = $142B ≈ 81% of $175B deposits.
# Wikipedia "Collapse of Silicon Valley Bank" (call report data): HQ Santa Clara CA, $209B assets, 3rd-largest US bank failure; uninsured 86.4%;
#   $1.8B loss on securities sale, $2.25B raise announced Mar 8; systemic risk exception Mar 12 (SVB + Signature), funded by special assessment on banks.
# Federal Reserve: reserve requirement ratios 0% effective March 26, 2020.
# FDIC (fdic.gov/90years): ~9,000 banks suspended operations 1930–1933. FDIC "what we do": $250,000 per depositor, per insured bank, per ownership category;
#   "Since the start of FDIC insurance on January 1, 1934, no depositor has lost a penny of insured funds."
# FDIC "payment to depositors": usually transfer to acquiring bank (immediate access) or check, payments usually begin within a few days.
# UK Treasury Committee report (2008): Northern Rock run 14 Sep 2007 = "first bank run in the United Kingdom since Victorian times".
# Bank of England 18.11.2025: FSCS limit £120,000 from 1 Dec 2025 (was £85,000). EU Directive 2014/49/EU: €100,000.
# Snopes/FDIC: First Republic failed May 1 2023, $229.1B assets, 2nd-largest US failure after WaMu ($307B, 2008), bought by JPMorgan. HQ San Francisco.
# CNBC 10.03.2023: Roku ~$487M at SVB (~26% of $1.9B cash). CNBC 11.03.2023: Circle $3.3B reserves at SVB, USDC fell below 87 cents.
# Wikipedia "Acquisition of Credit Suisse by UBS": announced 19 Mar 2023, CHF 3B, founded 1856 (167 yrs), CHF 16B AT1 written down to zero, SNB >CHF 100B liquidity.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
SF = [-121.96, 37.35]   # Santa Clara, CA
# ---- HOOK
A("On March ninth, twenty twenty-three, customers pulled forty-two billion dollars out of one single bank. In one day.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-121.96, 37.35, 6.5], pins=[dict(at=SF, label="Silicon Valley Bank", col="red")], counter=dict(to=42, pre="−$", suf="B", label="withdrawn on March 9"), title=["$42 BILLION", "OUT OF ONE BANK – IN ONE DAY"], mood="tense"), rate="+8%")
A("The next morning, another hundred billion was lined up to leave. And by lunchtime, the bank was gone.",
  dict(type="map", cam=[-121.96, 37.35, 6.5], pins=[dict(at=SF, label="Silicon Valley Bank", col="red", closed=True)], counter=dict(from_=42, to=142, pre="−$", suf="B", label="lined up to leave")), rate="+10%", pitch="+3Hz")
A("So what actually happens to your money when your bank collapses? And could it happen to your bank, too?",
  dict(type="img", img=1, chips=["Your money?", "Your bank?"]), pause=0.15)
# ---- HOW BANKS WORK
A("To understand that, you first need to know one slightly uncomfortable secret about banks.", dict(type="img", img=2, mood="calm"))
A("When you put a thousand dollars into your account, the bank doesn't just keep it in a vault.", dict(type="bank", step="deposit"))
A("It lends most of it out to people buying homes and cars, or invests it in things like government bonds.", dict(type="bank", step="lend"))
A("In the US, banks don't even have to keep a minimum share in reserve anymore. Since March twenty twenty, that requirement is zero percent.", dict(type="bank", step="zero"))
A("And that works perfectly well, as long as not everyone wants their money back on the same day.", dict(type="bank", step="run"))
# ---- HISTORY
A("When they do, it's called a bank run. And history shows how brutal that can get.", dict(type="img", img=3, mood="tense"))
A("Between nineteen thirty and nineteen thirty-three, around nine thousand American banks shut their doors.",
  dict(type="map", cam=[-97, 38.5, 3.2], view="us", dots=True, counter=dict(to=9000, label="banks suspended, 1930–1933", pre="", suf="")))
A("Millions of families lost their savings, because back then, nothing protected their deposits.", dict(type="map", cam=[-97, 38.5, 3.2], view="us", dots=True, fade=True))
A("And it's not just history. In two thousand seven, people lined up outside Northern Rock in Britain. It was the first bank run in the UK since Victorian times.",
  dict(type="map", cam=[-1.6, 54.97, 9], pins=[dict(at=[-1.61, 54.98], label="Northern Rock · 2007", col="red")], photo=8, hl=["GBR"]))
# ---- PROTECTION
A("So in nineteen thirty-three, the US created the FDIC. Its deposit insurance started on January first, nineteen thirty-four.", dict(type="shield", step="fdic", mood="calm"))
A("Today, it covers two hundred fifty thousand dollars per person, per bank, per account type.", dict(type="shield", step="limit"))
A("And since nineteen thirty-four, no depositor has lost a single penny of insured money.", dict(type="shield", step="zero"), rate="+6%", pitch="-2Hz")
A("Other countries do the same. The European Union protects one hundred thousand euros, and the UK, one hundred twenty thousand pounds.",
  dict(type="map", cam=[-40, 45, 1.25], pins=[dict(at=[-98, 39], label="USA · $250,000", col="green"), dict(at=[16, 47.5], label="EU · €100,000", col="green", dy=-0.6), dict(at=[-2, 53.5], label="UK · £120,000", col="green", dy=1.3)], hl=["USA", "GBR", "EU"]))
# ---- SVB
A("So why did Silicon Valley Bank still turn into a disaster?", dict(type="map", cam=[-121.96, 37.35, 6.5], pins=[dict(at=SF, label="Silicon Valley Bank", col="red")], mood="tense"), pause=0.2)
A("Its customers were mostly startups and tech companies, with accounts far above the limit. About eighty-six percent of its deposits were not insured.", dict(type="pie", v=86.4))
A("The bank had put a huge part of that money into long-term bonds. Then interest rates shot up, and those bonds lost value.", dict(type="bond"))
A("Selling them now would mean locking in those losses. Keeping them meant the bank had less cash on hand than it looked.", dict(type="bond", step=2))
A("On March eighth, the bank admitted that it had sold bonds at a one point eight billion dollar loss, and that it needed to raise new money.", dict(type="loss"))
A("Founders warned each other in group chats and on social media. Within hours, everyone tried to get out at once.",
  dict(type="map", cam=[-98, 39, 1.25], view="us", spread=True))
A("In just two days, customers tried to pull out about eighty-one percent of all deposits. And this time, nobody had to stand in line. They just tapped a button.", dict(type="bar81"))
A("On March tenth, regulators shut it down. It was the third-largest bank failure in American history.", dict(type="map", cam=[-121.96, 37.35, 6.5], pins=[dict(at=SF, label="Silicon Valley Bank", col="red", closed=True)]), pitch="-3Hz")
# ---- AFTER
A("And suddenly, real companies had their cash stuck inside. The streaming company Roku had about four hundred eighty-seven million dollars there. That was a quarter of all its cash.", dict(type="stuck", step=1))
A("The crypto company Circle had three point three billion dollars stuck. Its digital dollar, which is supposed to be worth exactly one dollar, fell below eighty-seven cents.", dict(type="stuck", step=2))
A("Then came the weekend that saved everyone.", dict(type="img", img=5, mood="bright", cut=True), pause=0.25)
A("On March twelfth, the government decided that all depositors would get their money back, even above the limit. And it was paid for with a special fee on other banks.", dict(type="rescue"))
A("But the fear kept spreading. Signature Bank in New York fell that same weekend, and in May, First Republic in San Francisco collapsed too.",
  dict(type="map", cam=[-98, 39, 1.25], view="us", pins=[dict(at=SF, label="Silicon Valley Bank", col="red", closed=True), dict(at=[-74.0, 40.71], label="Signature Bank", col="red", closed=True), dict(at=[-122.42, 37.77], label="First Republic", col="red", closed=True, dy=1, delay=0.55)], mood="tense"))
A("With two hundred twenty-nine billion dollars in assets, First Republic became the second-largest bank failure ever in the US.", dict(type="rank"))
A("And then, the fear jumped across the Atlantic.", dict(type="map", cam=[-40, 45, 1.25], arc=dict(a=[-98, 39], b=[8.54, 47.37]), pins=[dict(at=[8.54, 47.37], label="Zurich", col="gold")]))
A("Credit Suisse, a hundred sixty-seven year old Swiss bank, had to be rescued. On March nineteenth, its rival UBS bought it for just three billion Swiss francs.",
  dict(type="map", cam=[8.4, 46.8, 14], hl=["CHE"], pins=[dict(at=[8.54, 47.37], label="Credit Suisse · since 1856", col="red", closed=True)], counter=dict(to=3, pre="CHF ", suf="B", label="sale price to UBS")))
A("And some investors lost everything. Sixteen billion francs in special bonds were written down to zero.", dict(type="at1"))
# ---- WHAT HAPPENS TO YOU
A("So, what happens to your money if your bank fails?", dict(type="img", img=7, mood="calm"), pause=0.2)
A("If you're under the limit, usually almost nothing. Most of the time, a healthy bank takes over your account, and you can use your money right away.", dict(type="transfer"))
A("If no bank steps in, the FDIC sends you a check, and payments usually begin within a few days.", dict(type="check"))
A("Only the money above the limit is at risk. You become a creditor of the failed bank, and you might get some of it back, or not.", dict(type="above"))
A("So here's what you can do. First, keep your savings under the limit at each bank. If you have more, spread it across several banks.", dict(type="tips", n=1, img=6, mood="bright"))
A("Second, make sure your bank is actually insured. Some apps look like banks, but they aren't banks themselves.", dict(type="tips", n=2, img=6))
A("And third, don't panic. Bank runs are what kill banks. Your insured money is safe, even when the headlines look scary.", dict(type="tips", n=3, img=6))
A("Would you have pulled your money out of Silicon Valley Bank? Tell me in the comments.", dict(type="img", img=4, chips=["Yes", "No"]))
A("And subscribe for more money explained simply.", dict(type="outro", mood="calm"))
cfg = {"title": "YouTube 11: What Happens When Your Bank Collapses?", "size": [1920, 1080], "fps": 30, "scene": "scene.html",
       "voice": "en-US-AndrewMultilingualNeural", "rate": "+10%", "lead": 0.6, "gap": 0.4, "tail": 3.0, "crf": 21,
       "music": {"style": "adaptive", "bpm": 76, "gain": 0.3}, "sfx_vary": True, "sfx_gain": 0.42, "lines": L}
json.dump(cfg, open("project.json", "w"), ensure_ascii=False, indent=1)
w = sum(len(l["text"].split()) for l in L); print(len(L), "lines", w, "words ~", round(w / 165, 1), "min")
