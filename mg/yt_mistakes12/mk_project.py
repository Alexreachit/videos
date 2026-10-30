# YouTube 12 (long form, 16:9): "The Most Expensive Mistakes in History" -> project.json
# Sources (checked 2026-10-30):
# #7 Mars Climate Orbiter: Deseret News 1 Oct 1999 "Metric miscalculation becomes cosmic blunder" ($125M orbiter, vanished Sept 23,
#    Lockheed Martin Astronautics sent data in pounds of force, JPL assumed newtons); 19FortyFive (2026): flew 416 million miles. 1 lbf = 4.448 N.
# #6 Mizuho / J-Com: InvestmentNews ("$121M award..."): Dec 8, 2005, sold 610,000 shares at 1 yen instead of 1 share at 610,000 yen,
#    loss 40.7bn yen, court: TSE 70% to blame, 10.7bn yen (~$121M); Finextra: TSE glitch, cancel failed; BBC via TU Delft page: order
#    41 times the outstanding shares. ~40bn yen ~ $340M at 2005 rates (Gamestar: $335M).
# #5 Knight Capital: SEC press release 2013-222 (see ys_knight).
# #4 James Howells: Decrypt (2025): drive with keys to 8,000 BTC thrown out by former partner in 2013, appeal lost 2025;
#    The Register (11 Feb 2025): Newport landfill, ~100,000 t area, wants to buy the site, council plans to close/cap it;
#    Decrypt 2021: offered council a share. BTC ~ $79,769 (CoinGecko 27 Oct 2026) -> 8,000 BTC ~ $638M.
# #3 Citibank / Revlon: Insurance Journal / Reuters 12 Sep 2022: Aug 11, 2020, meant to pay $7.8M interest, paid off $894M loan due 2023,
#    ~$500M not returned by 10 asset managers, Feb 2021 Judge Furman ruled for lenders, 2nd Circuit reversed 3-0 (Sept 2022).
# #2 Samsung Securities: Business Standard 11 Apr 2018: dividend 1,000 won/share became 1,000 shares/share, 2.8bn shares
#    (>30x issued shares), 111.8 trillion won ($104.8bn), 16 staff sold 5 million shares (~$186.9M); BloombergQuint: CEO resigned.
# #1 Ronald Wayne: Fortune 12 Dec 2025: 10% stake, cashed out 12 days after Apple's inception for $800, later $1,500 to forfeit any claim,
#    Apple ~ $4 trillion, stake "could now be worth between $75 billion and $360 billion"; Outlook Business: "no regrets".
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
def B(scene, els, **k): return dict(type="beat", scene=scene, els=els, **k)
# element helpers (at/end = fraction of the line; out=[lines later, frac])
def O(k, x, y, w, at=0, **o): return dict(e="obj", k=k, x=x, y=y, w=w, at=at, **o)
def T(txt, x, y, size=64, at=0, **o): return dict(e="tx", txt=txt, x=x, y=y, size=size, at=at, **o)
def P(txt, x, y, size=36, at=0, **o): return dict(e="pill", txt=txt, x=x, y=y, size=size, at=at, **o)
def ST(txt, x, y, at=0, **o): return dict(e="stamp", txt=txt, x=x, y=y, at=at, **o)
def CT(x, y, to, at=0, end=.8, **o): return dict(e="count", x=x, y=y, to=to, at=at, end=end, **o)
def CD(x, y, w, big, small, at=0, **o): return dict(e="card", x=x, y=y, w=w, big=big, small=small, at=at, **o)
END = [99, 0]

# ---------------- INTRO
A("In twenty twelve, one company lost four hundred sixty million dollars in forty-five minutes.",
  B("intro", [dict(e="title", at=-1), O("server", 560, 600, 380, 0, out=[1, 0]),
              CT(1300, 560, 460, .45, .85, pre="−$", suf="M", size=130, col="red", out=[1, 0]), P("in 45 minutes", 1300, 700, 40, .8, dot="red", out=[1, 0])],
    bg="sky", mood="tense"))
A("In twenty twenty, a bank accidentally sent out nearly nine hundred million dollars.",
  B("intro", [O("bank", 560, 620, 400, 0, out=[1, 0]), dict(e="fly", k="cash", fx=640, fy=600, tx=1500, ty=380, w=150, at=.3, end=.8, n=6, out=[1, 0]),
              CT(1300, 560, 894, .4, .85, pre="$", suf="M", size=130, col="red", out=[1, 0]), P("sent by mistake", 1300, 700, 40, .8, dot="red", out=[1, 0])]))
A("And one man gave up a piece of Apple for just eight hundred dollars.",
  B("intro", [O("samthink", 560, 640, 460, 0, out=[1, 0]), O("contract", 1300, 600, 320, .2, out=[1, 0]), ST("$800", 1300, 780, .7, col="red", sz=90, out=[1, 0])]))
A("Some of these mistakes nearly destroyed a company. Others became famous lessons that banks and engineers still learn from today.",
  B("intro", [O("samthink", 560, 640, 460, 0, out=[1, 0]), P("📉 nearly destroyed companies", 1320, 450, 44, .1, out=[1, 0]), P("📚 still taught today", 1320, 600, 44, .55, out=[1, 0])]))
A("These are some of the most expensive mistakes in history.",
  B("intro", [dict(e="ladder", at=0, out=[2, .99])]))
A("Some were typos. Some were software bugs. And one was simply a bad decision.",
  B("intro", [P("⌨️ typos", 470, 860, 40, .05, out=[1, .99]), P("🐛 software bugs", 960, 860, 40, .3, out=[1, .99]), P("🤦 one bad decision", 1470, 860, 40, .65, out=[1, .99])]))
A("We'll count them down, from number seven to number one. And number one is so big, it barely feels real.",
  B("intro", [dict(e="ladderhi", at=.55, out=[1, 0])]))

# ---------------- #7 MARS
A("Number seven. In nineteen ninety-nine, NASA's Mars Climate Orbiter had flown four hundred sixteen million miles to reach Mars.",
  B("mars", [dict(e="chap", n=7, sub="THE WRONG UNITS", at=0, out=[0, .45]), O("mars", 1420, 560, 600, .1, out=[2, 0]),
             dict(e="probe", at=.35, out=[2, 0]), P("416 million miles", 560, 820, 40, .6, dot="gold", out=[1, 0])], bg="space", mood="calm"))
A("On September twenty-third, it was supposed to swing into orbit. Instead, it flew far too close to the planet, and was never heard from again.",
  B("mars", [dict(e="orbit", x=1420, y=560, rx=420, ry=170, at=0, out=[1, 0]), P("planned orbit", 1420, 260, 36, .1, dot="green", out=[1, 0]),
             ST("SIGNAL LOST", 960, 200, .82, col="red", sz=76, out=[1, 0])]))
A("The reason? Lockheed Martin, which built the spacecraft, sent its thruster data in pounds of force. NASA's navigation team assumed the numbers were in newtons.",
  B("mars", [CD(520, 330, 620, "pound-force", "LOCKHEED MARTIN · spacecraft builder", .15, col="red", out=[1, .99]),
             CD(1400, 330, 620, "newtons", "NASA navigation team", .62, col="green", out=[1, .99]), T("≠", 960, 420, 180, .7, col="gold", out=[1, .99])]))
A("One pound of force is about four and a half newtons. So every correction was off by more than four times, and nobody noticed.",
  B("mars", [T("1 lbf ≈ 4.45 N", 960, 700, 96, .05, out=[1, 0]), CT(960, 840, 4.45, .45, .75, pre="off by ×", dec=2, size=70, col="red", out=[1, 0])]))
A("And because the numbers didn't look obviously wrong, the error kept growing quietly, mile after mile.",
  B("mars", [O("probe", 960, 560, 360, 0, out=[1, 0]), dict(e="drift", at=.1, end=.9, out=[1, 0])]))
A("A hundred and twenty-five million dollar spacecraft, lost because two teams used different units.",
  B("mars", [O("probe", 600, 520, 520, 0, gray=1, rot=-14, out=[1, 0]), CT(1320, 480, 125, .05, .5, pre="$", suf="M", size=140, col="red", out=[1, 0]),
             ST("LOST", 1320, 660, .6, col="red", sz=90, out=[1, 0])]))
A("Lesson one: the most dangerous errors are the ones that look completely normal.",
  B("mars", [O("samthink", 520, 620, 480, 0, out=[1, 0]), CD(1260, 380, 760, "Lesson #1", "The worst errors look completely normal", .2, col="gold", out=[1, 0])]))
A("But at least that one was in space. Number six happened with a single keyboard.",
  B("mars", [O("keyboard", 1260, 600, 420, .3, out=END)]))

# ---------------- #6 MIZUHO
A("Number six. Tokyo, December eighth, two thousand five.",
  dict(type="map", cam=[138, 37, 3.2], cam2=[139.69, 35.69, 7], chap=6, chapsub="THE SWAPPED NUMBERS",
       pins=[dict(at=[139.69, 35.69], label="Tokyo Stock Exchange", col="red", delay=.45)]))
A("A trader at Mizuho Securities wanted to sell one share of a new company called J-Com, for six hundred ten thousand yen.",
  B("mizuho", [O("keyboard", 520, 600, 520, 0, out=[1, 0]), dict(e="ticket", x=1320, y=520, a="SELL  1 share", b="at ¥610,000", ok=True, at=.35, out=[1, 0])], bg="sky", mood="tense"))
A("Instead, the numbers got swapped. The order said: sell six hundred ten thousand shares, for one yen each.",
  B("mizuho", [O("keyboard", 520, 600, 520, 0, glow=True, out=[1, 0]), dict(e="ticket", x=1320, y=520, a="SELL  610,000 shares", b="at ¥1 each", ok=False, at=.3, out=[1, 0])]))
A("In finance, this is called a fat-finger error. Someone hits the wrong key, or types the right numbers into the wrong box.",
  B("mizuho", [O("keyboard", 520, 600, 520, 0, glow=True, out=[1, 0]), T("FAT-FINGER ERROR", 1320, 460, 84, .1, col="gold", out=[1, 0]), P("wrong key · wrong box", 1320, 600, 44, .5, out=[1, 0])]))
A("And J-Com didn't even have that many shares. The order was forty-one times bigger than all the shares that existed.",
  B("mizuho", [O("certs", 330, 560, 340, 0, out=[1, 0]),
               dict(e="bars", x=620, y=380, w=1150, rows=[["all J-Com shares", 1, "blue"], ["the order", 41, "red"]], at=.2, end=.75, out=[1, 0]),
               P("41× more than existed", 1200, 760, 44, .78, bg="red", out=[1, 0])]))
A("Mizuho tried to cancel it right away, but a glitch at the Tokyo Stock Exchange kept the cancel from going through.",
  B("mizuho", [dict(e="button", x=760, y=520, txt="CANCEL", at=.1, press=.35, out=[1, 0]), O("server", 1360, 540, 360, .4, out=[1, 0]),
               ST("ERROR", 1360, 760, .7, col="red", sz=80, out=[1, 0])]))
A("The damage: about forty billion yen, more than three hundred million dollars, from one swapped number.",
  B("mizuho", [O("burn", 560, 560, 460, 0, out=[1, 0]), CT(1320, 460, 40, .05, .4, pre="−¥", suf="B", size=140, col="red", out=[1, 0]),
               P("≈ $340 million", 1320, 620, 52, .5, bg="red", out=[1, 0])]))
A("Years later, a court said the exchange was mostly to blame, and ordered it to pay around a hundred and twenty million dollars. It still left a huge hole.",
  B("mizuho", [O("scales", 560, 560, 460, 0, out=END), P("court: exchange 70% to blame", 1320, 380, 40, .25, dot="gold", out=END),
               CT(1320, 540, 121, .45, .7, pre="+$", suf="M", size=110, col="green", out=END), P("still a huge loss", 1320, 700, 40, .8, bg="red", out=END)]))
A("Since then, trading systems have added more automatic checks to block orders that are clearly impossible. But as number five shows, software can fail in other ways.",
  B("mizuho", [P("✅ more automatic checks", 1320, 860, 40, .1, dot="green", out=END)]))

# ---------------- #5 KNIGHT
A("Number five. August first, twenty twelve. Knight Capital was one of the biggest stock traders in America.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-74.07, 40.72, 7], chap=5, chapsub="THE FORGOTTEN SERVER",
       pins=[dict(at=[-74.07, 40.72], label="Knight Capital · Jersey City", col="red", delay=.55)]))
A("That morning, it installed new trading software on its eight servers. But on one of them, the update never arrived.",
  B("knight", [dict(e="servers", at=0, bad=.6, out=[1, 0]), P("1 of 8 missed the update", 960, 160, 44, .7, bg="red", out=[1, 0])], bg="sky", mood="tense"))
A("Before the market opened, the system sent ninety-seven warning emails. Nobody acted on them.",
  B("knight", [O("laptop", 640, 600, 560, 0, out=[1, 0]), O("mail", 1300, 420, 280, .1, out=[1, 0]), CT(1300, 640, 97, .15, .6, suf=" emails", size=110, col="red", out=[1, 0]),
               ST("IGNORED", 960, 820, .8, col="red", sz=86, out=[1, 0])]))
A("At nine thirty, the market opened, and that one server woke up old code that hadn't been used in years.",
  B("knight", [O("monitor", 640, 580, 560, 0, out=[1, 0]), P("⏰ 9:30 AM · market opens", 1320, 400, 44, .05, out=[1, 0]), P("old code · unused for years", 1320, 560, 40, .6, bg="red", out=[1, 0])]))
A("In forty-five minutes, it fired off more than four million orders.",
  B("knight", [O("monitor", 640, 580, 560, 0, out=[1, 0]), dict(e="orders", at=.05, out=[1, 0]), CT(1320, 420, 4000000, .1, .8, size=110, col="gold", out=[1, 0]),
               P("orders", 1320, 540, 44, .1, out=[1, 0]), O("watch", 1320, 720, 220, .2, out=[1, 0])], cut=True))
A("By the time it was stopped, Knight had lost four hundred sixty million dollars.",
  B("knight", [O("burn", 560, 580, 480, 0, out=[1, 0]), CT(1320, 520, 460, .2, .8, pre="−$", suf="M", size=150, col="red", out=[1, 0])]))
A("That's more than ten million dollars, every single minute.",
  B("knight", [CT(1320, 480, 10.2, .1, .7, pre="$", suf="M / minute", dec=1, size=110, col="red", out=[1, 0]), O("watch", 560, 560, 360, 0, out=[1, 0])]))
A("Its stock crashed more than seventy percent, and days later it needed a four hundred million dollar rescue just to survive.",
  B("knight", [dict(e="chart", kind="crash", x=200, y=260, w=1100, h=560, at=0, end=.45, out=END), CT(1550, 400, 70, .2, .45, pre="−", suf="%", size=130, col="red", out=END),
               P("🛟 $400M rescue", 1550, 620, 48, .7, bg="green", out=END)]))
A("A year later, Knight was taken over by a rival, and the company disappeared as an independent firm.",
  B("knight", [ST("TAKEN OVER · 2013", 1550, 820, .3, col="red", sz=48, out=END)]))

# ---------------- #4 HOWELLS
A("Number four. A city called Newport, in Wales.",
  dict(type="map", cam=[-3, 54, 2.2], cam2=[-2.99, 51.58, 7], chap=4, chapsub="THE HARD DRIVE IN THE TRASH",
       pins=[dict(at=[-2.99, 51.58], label="Newport, Wales", col="red", delay=.5)]))
A("In the early days of bitcoin, a computer engineer named James Howells collected around eight thousand bitcoin, back when they were worth almost nothing.",
  B("howells", [O("hdd", 560, 560, 420, 0, out=[1, .55]), dict(e="btc", x=1320, y=560, at=.3, end=.75, out=[2, 0]), CT(1320, 820, 8000, .3, .75, suf=" BTC", size=70, col="gold", out=[2, 0])],
    bg="sky", mood="calm"))
A("In twenty thirteen, an old hard drive holding the keys to those coins was thrown out with the trash, and it ended up in the local landfill.",
  B("howells", [O("landfill", 560, 600, 620, .45, out=END), dict(e="fly", k="hdd", fx=560, fy=560, tx=560, ty=560, w=200, at=.35, end=.65, n=1, drop=True, out=[1, 0]),
                P("2013", 560, 220, 48, 0, dot="gold", out=[1, 0])]))
A("Today, those eight thousand bitcoin would be worth more than six hundred million dollars.",
  B("howells", [CT(1320, 480, 600, .2, .8, pre="$", suf="M+", size=140, col="green", out=[1, 0]), P("1 BTC ≈ $80,000 (Oct 2026)", 1320, 640, 38, .5, out=[1, 0])]))
A("And the drive isn't sitting on top. He believes it's buried somewhere in an area holding around a hundred thousand tonnes of waste.",
  B("howells", [CT(1320, 480, 100000, .45, .8, suf=" tonnes", size=110, col="gold", out=[1, 0]), P("somewhere in here", 560, 260, 40, .3, dot="red", out=[1, 0])]))
A("For over ten years, he tried to get permission to dig. He offered the city a share of the money. He even talked about buying the whole landfill.",
  B("howells", [P("⛏️ asked to dig", 1320, 340, 44, .05, out=[1, 0]), P("🤝 offered the city a share", 1320, 490, 44, .35, out=[1, 0]), P("🏷️ wanted to buy the landfill", 1320, 640, 44, .7, out=[1, 0])]))
A("But in twenty twenty-five, the courts said no. And the city plans to close the site for good.",
  B("howells", [O("gavel", 1320, 480, 320, 0, out=END), ST("CASE REJECTED", 1320, 680, .2, col="red", sz=64, out=END), ST("SITE CLOSING", 560, 260, .75, col="red", sz=64, rot=6, out=END)]))
A("Still, at least that money was never really in someone else's hands. Number three is about a bank that sent away almost a billion dollars by accident.",
  B("howells", [O("bank", 1320, 820, 260, .5, out=END)]))

# ---------------- #3 CITI
A("Number three. New York, August eleventh, twenty twenty.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-74.0, 40.71, 7], chap=3, chapsub="THE $900 MILLION OOPS",
       pins=[dict(at=[-74.0, 40.71], label="Citibank · New York", col="red", delay=.5)]))
A("Citibank was supposed to send a routine interest payment for the cosmetics company Revlon. About seven point eight million dollars.",
  B("citi", [O("bank", 560, 580, 440, 0, out=[1, 0]), CD(1320, 400, 600, "$7.8M", "interest payment · planned", .45, col="green", out=[1, 0])], bg="sky", mood="tense"))
A("Instead, after a mix-up in how the payment was entered, it paid back Revlon's entire loan. Nearly nine hundred million dollars, years before it was due.",
  B("citi", [O("bank", 560, 580, 440, 0, out=[1, 0]), dict(e="fly", k="cash", fx=640, fy=560, tx=1700, ty=300, w=140, at=.35, end=.85, n=10, out=[1, 0]),
             CT(1320, 520, 894, .35, .75, pre="$", suf="M", size=140, col="red", from_=7.8, out=[1, 0]), P("loan wasn't due until 2023", 1320, 680, 40, .8, dot="red", out=[1, 0])]))
A("That's more than a hundred times bigger than the payment it was supposed to make.",
  B("citi", [dict(e="bars", x=520, y=380, w=1150, rows=[["planned: $7.8M", 7.8, "green"], ["sent: $894M", 894, "red"]], at=.1, end=.7, out=[1, 0]),
             P("114× too much", 1100, 800, 48, .75, bg="red", out=[1, 0])]))
A("Some lenders sent the money back. But others kept about five hundred million dollars, and basically said: thanks, that's ours now.",
  B("citi", [dict(e="people", x=560, y=640, n=10, at=.3, out=[2, 0]), CT(1320, 480, 500, .35, .65, pre="$", suf="M", size=130, col="red", out=[1, 0]),
             P("kept by 10 asset managers", 1320, 640, 40, .5, out=[1, 0]), P('💬 "Thanks, that\'s ours now."', 560, 300, 40, .8, out=[1, 0])]))
A("And in twenty twenty-one, a judge actually agreed with them.",
  B("citi", [O("scales", 1320, 520, 420, 0, rot=-8, out=[1, 0]), ST("LENDERS WIN · 2021", 1320, 780, .45, col="red", sz=56, out=[1, 0])]))
A("Citibank appealed. In twenty twenty-two, a higher court reversed the ruling, and said Citi had the right to get its money back.",
  B("citi", [O("gavel", 560, 520, 340, 0, out=END), ST("REVERSED · 2022", 1320, 260, .35, col="green", sz=64, out=END),
             dict(e="fly", k="cash", fx=1750, fy=420, tx=1320, ty=700, w=130, at=.6, end=.95, n=8, out=END)]))
A("Two years of court fights, all because of a few clicks. It became a famous lesson about how payment screens and approvals are designed.",
  B("citi", [P("lesson: design + double approvals", 1320, 800, 40, .5, dot="gold", out=END)]))

# ---------------- #2 SAMSUNG
A("Number two. Seoul, South Korea, April twenty eighteen.",
  dict(type="map", cam=[127.5, 36.5, 3.5], cam2=[126.98, 37.57, 7], chap=2, chapsub="THE GHOST SHARES",
       pins=[dict(at=[126.98, 37.57], label="Samsung Securities · Seoul", col="red", delay=.5)]))
A("Samsung Securities wanted to pay its employees a dividend of one thousand won per share. That's less than one dollar.",
  B("samsung", [O("certs", 560, 580, 420, 0, out=[1, 0]), CD(1320, 380, 640, "₩1,000", "dividend per share · less than $1", .3, col="green", out=[1, 0])], bg="sky"))
A("But an employee entered one thousand shares, instead of one thousand won.",
  B("samsung", [O("keyboard", 560, 600, 520, 0, glow=True, out=[1, 0]), CD(1320, 380, 640, "1,000 SHARES", "per share · instead of ₩1,000", .3, col="red", out=[1, 0])]))
A("In seconds, about two point eight billion new shares appeared out of thin air. More than thirty times all the shares that really existed.",
  B("samsung", [dict(e="ghosts", x=560, y=600, at=.05, end=.6, out=[1, .99]), CT(1320, 440, 2.8, .1, .5, suf="B shares", dec=1, size=120, col="gold", out=[1, .99]),
                P(">30× all real shares", 1320, 600, 44, .6, bg="red", out=[1, .99])]))
A("On paper, they were worth around a hundred and five billion dollars.",
  B("samsung", [CT(1320, 760, 105, .2, .8, pre="$", suf="B", size=130, col="red", out=[1, 0])]))
A("These were ghost shares. But sixteen employees sold about five million of them anyway, worth around a hundred and eighty-seven million dollars.",
  B("samsung", [dict(e="people", x=560, y=640, n=16, at=.3, out=[2, 0]), CT(1320, 440, 5, .4, .65, suf="M shares sold", size=96, col="gold", out=[1, 0]),
                P("≈ $187 million", 1320, 600, 48, .8, bg="red", out=[1, 0])]))
A("The company's CEO later resigned.",
  B("samsung", [ST("CEO RESIGNED", 1320, 480, .15, col="red", sz=80, out=END)]))
A("South Korea's regulators stepped in, and even years later, courts were still ordering Samsung Securities to pay compensation to investors.",
  B("samsung", [O("scales", 560, 560, 420, .1, out=END), P("⚖️ compensation ordered · even in 2026", 1320, 680, 40, .5, out=END)]))
A("A hundred and five billion dollars on paper is huge. But the number one mistake on this list wasn't a typo at all.",
  B("samsung", [P("no typo · no bug", 1320, 820, 40, .6, bg="red", out=END)]))

# ---------------- #1 WAYNE
A("And number one. California, nineteen seventy-six.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-122.1, 37.38, 6], chap=1, chapsub="THE $800 DECISION",
       pins=[dict(at=[-122.1, 37.38], label="California · 1976", col="gold", delay=.5)]))
A("Steve Jobs and Steve Wozniak were starting a new computer company called Apple. They brought in a third partner, Ronald Wayne, and gave him ten percent.",
  B("wayne", [O("garage", 560, 560, 560, 0, out=[4, 0]), dict(e="pie", x=1360, y=520, r=220, at=.5, end=.85, out=[4, 0])], bg="sky", mood="calm"))
A("Back then, Apple was just a tiny startup, and nobody knew if it would survive.",
  B("wayne", [P("tiny startup · no guarantee", 1360, 860, 40, .2, out=[1, 0])]))
A("But just twelve days later, Wayne gave up his share. For eight hundred dollars.",
  B("wayne", [P("12 days later", 1760, 180, 40, .05, dot="red", out=[1, 0]), ST("SOLD FOR $800", 1360, 840, .6, col="red", sz=72, out=[2, 0])]))
A("Why? He later said he felt like he was standing in the shadow of giants.",
  B("wayne", [P('💬 "standing in the shadow of giants"', 960, 170, 44, .3, out=[1, 0])]))
A("Later, he took another fifteen hundred dollars to drop any claim to the company.",
  B("wayne", [O("contract", 560, 560, 380, 0, out=[1, 0]), P("+$1,500 · no more claims", 1360, 420, 48, .4, out=[1, 0])]))
A("Today, Apple is worth around four trillion dollars.",
  B("wayne", [CT(960, 440, 4, .1, .7, pre="$", suf=" TRILLION", size=150, col="gold", out=[1, 0]), P("Apple today (approx.)", 960, 620, 40, .3, out=[1, 0])]))
A("Even after all the new shares Apple created over the years, his ten percent could be worth somewhere between seventy-five and three hundred sixty billion dollars.",
  B("wayne", [dict(e="range", x=260, y=520, w=1400, lo=75, hi=360, max=400, at=.5, end=.9, out=[1, 0]), T("his 10% today (estimate)", 960, 300, 60, .1, out=[1, 0])]))
A("And the wildest part? He says he has no regrets.",
  B("wayne", [O("samhappy", 560, 620, 480, 0, out=END), ST("NO REGRETS", 1320, 480, .5, col="green", sz=90, out=END)]))

# ---------------- OUTRO
A("So what do all these mistakes have in common? Most of them weren't made by stupid people.",
  B("outro", [O("samthink", 480, 620, 480, 0, out=[1, 0]), T("What do they have in common?", 1260, 300, 64, .05, out=[1, 0])], bg="sky", mood="calm"))
A("They were made by smart people, in a hurry, trusting a number they never double-checked.",
  B("outro", [P("smart people", 1260, 460, 44, .1, out=[1, 0]), P("in a hurry", 1260, 580, 44, .3, out=[1, 0]), P("no double-check", 1260, 700, 44, .6, bg="red", out=[1, 0])]))
A("A unit nobody converted. A number typed the wrong way round. Ninety-seven emails nobody read.",
  B("outro", [CD(400, 300, 480, "lbf ≠ N", "a unit nobody converted", .05, col="red", out=[1, 0]), CD(960, 300, 480, "610,000 ⇄ 1", "numbers swapped", .35, col="red", out=[1, 0]),
              CD(1520, 300, 480, "97 emails", "nobody read", .7, col="red", out=[1, 0])]))
A("So next time you send money, sign something, or hit confirm, take five extra seconds. It might be the cheapest insurance you'll ever get.",
  B("outro", [dict(e="button", x=640, y=520, txt="CONFIRM", at=.05, press=None, out=[1, 0]), CT(1320, 480, 5, .3, .6, suf=" seconds", size=120, col="green", out=[1, 0]),
              P("the cheapest insurance", 1320, 640, 44, .7, dot="green", out=[1, 0])]))
A("Because as you just saw, the biggest losses rarely come from one huge decision. They come from tiny moments that nobody took seriously.",
  B("outro", [T("tiny moments → huge losses", 960, 480, 80, .3, col="gold", out=[1, 0])]))
A("Which of these mistakes shocked you the most? Tell me in the comments. And if you want more stories like this, subscribe.",
  B("outro", [O("samhappy", 560, 600, 560, 0, out=END), CD(1300, 300, 720, "Which one shocked you?", "tell me in the comments 👇", .05, col="ink", out=END),
              P("🔔 Subscribe for more money stories", 1300, 640, 44, .55, bg="red", out=END)]))

P_ = dict(title="YouTube 12: The Most Expensive Mistakes in History",
          _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
          size=[1920, 1080], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+0%",
          lead=0.6, gap=0.48, tail=3.0, crf=21, music=dict(style="ttdark", bpm=140, gain=0.15, duck_ratio=2),
          sfx_vary=True, sfx_gain=0.4, lines=L)
json.dump(P_, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
