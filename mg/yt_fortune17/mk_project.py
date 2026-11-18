# YouTube 17 (long form, 16:9): "They Said No to a Fortune: 6 Deals That Changed History" -> project.json
# Sources (checked 2026-11-18):
# Hook/#1 Excite & Google: TechCrunch 29 Sep 2010 "When Google Wanted To Sell To Excite For Under $1 Million — And They Passed"
#    (Vinod Khosla at Disrupt: early 1999, Page & Brin asked $1M, Khosla talked them down to $750,000, Excite CEO George Bell
#    still said no); Fortune 29 Sep 2010 "Excite passed up buying Google for $750,000 in 1999"; CNN Money 28 Sep 2001 /
#    Wikipedia "@Home Network" (Excite@Home filed for bankruptcy Sept 2001); FourWeekMBA ticker hub 16 Nov 2026
#    (Alphabet ~ $3.6 trillion at 13 Nov 2026 close).
# #6 Decca & Beatles: Wikipedia "The Beatles' Decca audition" (1 Jan 1962, Decca Studios West Hampstead, 15 songs, Decca signed
#    Brian Poole and the Tremeloes instead, partly because they were closer to London; "guitar groups are on the way out"
#    attributed by Brian Epstein, Dick Rowe denied it); Wikipedia "Dick Rowe" (later signed the Rolling Stones after a tip
#    from George Harrison).
# #5 Kodak: NYT via Business Insider "This man invented the digital camera in 1975 ..." (Steve Sasson, 100x100 pixels b/w,
#    23 seconds to record to cassette tape, "no one would ever want to look at their pictures on a television set");
#    PetaPixel 21 Sep 2017 (8-pound camera, 0.01 megapixel, Sasson was 24; Kodak filed for bankruptcy 2012).
# #4 Blockbuster & Netflix: Marketplace 2020 (Hastings: offered Netflix for $50M in 2000, ~9,000 stores, Netflix lost $57M);
#    NZ Herald / Marc Randolph (Antioco "struggling not to laugh"); Wikipedia "Blockbuster LLC" (bankrupt 2010).
# #3 Yahoo & Microsoft: CIO Insight / HeraldNet 1 Feb 2008 (Microsoft bids $44.6 billion for Yahoo); Supercar Blondie 2025
#    (Yahoo board: offer "substantially undervalued" Yahoo); Axios 4 May 2021 (Verizon acquired Yahoo for $4.48B in 2017;
#    Yahoo + AOL sold to Apollo for $5B in 2021).
# #2 Facebook & Yahoo: Business Insider (excerpt "An Ugly Truth", Frenkel & Kang): Yahoo offer June 2006, $1 billion;
#    Zuckerberg turned it down; much of the management team / staff left afterwards; Zuckerberg quote about staff quitting.
#    finhacker.cz: Meta market cap $1.601 trillion on 16 Nov 2026.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
def B(scene, els, **k): return dict(type="beat", scene=scene, els=els, **k)
def O(k, x, y, w, at=0, **o): return dict(e="obj", k=k, x=x, y=y, w=w, at=at, **o)
def T(txt, x, y, size=64, at=0, **o): return dict(e="tx", txt=txt, x=x, y=y, size=size, at=at, **o)
def P(txt, x, y, size=36, at=0, **o): return dict(e="pill", txt=txt, x=x, y=y, size=size, at=at, **o)
def ST(txt, x, y, at=0, **o): return dict(e="stamp", txt=txt, x=x, y=y, at=at, **o)
def CT(x, y, to, at=0, end=.8, **o): return dict(e="count", x=x, y=y, to=to, at=at, end=end, **o)
def CD(x, y, w, big, small, at=0, **o): return dict(e="card", x=x, y=y, w=w, big=big, small=small, at=at, **o)
def DEAL(x, y, press, at=0, **o): return dict(e="deal", x=x, y=y, press=press, at=at, **o)
def TN(then, now, at=0, end=.8, **o): return dict(e="thennow", then=then, now=now, at=at, end=end, **o)
N1 = [1, 0]
END = [99, 0]

# ---------------- INTRO (hook readable from frame 0, also muted)
A("In nineteen ninety-nine, Google was for sale, for seven hundred fifty thousand dollars. And the buyer said no.",
  B("intro", [dict(e="title", a="GOOGLE FOR $750,000?", b="…and the buyer said NO", at=-1, out=[2, 0]),
              dict(e="check", x=640, y=620, w=720, to="Google", amt="$750,000", at=-1, out=N1),
              ST("DECLINED", 640, 640, .55, col="red", sz=100, out=N1), O("samyell", 1400, 640, 440, -1, out=N1)],
    bg="sky", mood="tense"))
A("Today, Google's parent company is worth more than three trillion dollars.",
  B("intro", [TN("$750K", "$3.6 TRILLION", .1, .8, out=N1)]))
A("It's not the only time someone said no to a fortune. A record label turned down the Beatles. Blockbuster laughed at Netflix.",
  B("intro", [dict(e="vinyl", x=520, y=600, r=230, label="DECCA?", at=.03, out=N1), dict(e="env", x=1380, y=600, w=520, at=.45, out=N1),
              ST("NO", 520, 600, .3, col="red", sz=90, out=N1), ST("NO", 1380, 600, .8, col="red", sz=90, out=N1)]))
A("These are six times someone said no to a fortune, counted down to the most expensive no in history.",
  B("intro", [T("THEY SAID NO TO A FORTUNE", 960, 300, 86, 0, col="gold", out=[2, .99]), dict(e="ladder", n=6, at=.2, out=[2, .99])]))
A("And one of them wasn't a mistake at all. Stay to the end, and you'll see why.",
  B("intro", [dict(e="ladderhi", x=1290, green=True, txt="not a mistake?", at=.1, out=N1)]))

# ---------------- #6 DECCA / BEATLES
A("Number six. London, New Year's Day, nineteen sixty-two.",
  dict(type="map", cam=[-3, 54, 2.4], cam2=[-0.19, 51.55, 9], chap=6, chapsub="THE BAND NOBODY WANTED",
       pins=[dict(at=[-0.19, 51.55], label="Decca Studios", col="gold", delay=.45)]))
A("A young band from Liverpool drives down through the snow for an audition at Decca, one of the biggest record labels in Britain.",
  B("decca", [dict(e="van", x=520, y=640, at=0, out=N1), CD(1340, 330, 620, "Decca Records", "audition · 1 January 1962", .4, col="ink", out=N1)],
    bg="sky", mood="calm"))
A("They play fifteen songs in about an hour. Their name is the Beatles.",
  B("decca", [dict(e="vinyl", x=560, y=600, r=240, label="15 SONGS", at=0, out=[2, 0]), CT(1340, 440, 15, .1, .45, suf=" songs", size=120, col="gold", out=N1),
              P("🎸 The Beatles", 1340, 620, 56, .7, bg="blue", out=N1)]))
A("A few weeks later, the answer comes back. No. Decca signs another band instead, partly because they lived closer to London.",
  B("decca", [DEAL(1340, 560, .35, at=0, out=N1), P("✍️ signed instead: Brian Poole and the Tremeloes", 960, 300, 40, .7, out=N1)]))
A("According to the Beatles' manager, Brian Epstein, he was told that guitar groups were on their way out.",
  B("decca", [dict(e="letter", x=1340, y=290, w=700, head="DECCA RECORDS · LONDON", body="“Guitar groups are on their way out, Mr. Epstein.”", at=.05, out=N1),
              O("samthink", 520, 640, 380, .1, out=N1)]))
A("The executive who got the blame, Dick Rowe, always denied saying it. But the decision stuck to him for the rest of his life.",
  B("decca", [CD(1340, 320, 640, "Dick Rowe", "always denied the quote", .1, col="ink", out=N1), ST("BLAMED", 1340, 640, .6, col="red", sz=80, out=N1)]))
A("A few months later, the Beatles signed with a different label, and went on to become the best-selling band in music history.",
  B("decca", [dict(e="vinyl", x=560, y=600, r=240, label="BEATLES", gold=True, at=.03, out=N1), P("🏆 best-selling band in history", 1340, 520, 48, .6, bg="gold", out=N1)]))
A("Rowe did get one thing right afterwards. On a tip from George Harrison, he signed another guitar band: the Rolling Stones.",
  B("decca", [dict(e="vinyl", x=560, y=600, r=220, label="DECCA", at=0, out=N1), P("💡 tip from George Harrison", 1340, 400, 46, .3, out=N1),
              ST("SIGNED", 1340, 600, .8, col="green", sz=90, out=N1)]))
A("Lesson one: experts can be wrong about what people will love.",
  B("decca", [O("samthink", 520, 620, 460, 0, out=N1), CD(1300, 380, 760, "Lesson #1", "Experts can be wrong about what people will love.", .2, col="gold", out=N1)]))

# ---------------- #5 KODAK
A("Number five. Rochester, New York, nineteen seventy-five.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-77.61, 43.16, 8], chap=5, chapsub="THE CAMERA THEY HID",
       pins=[dict(at=[-77.61, 43.16], label="Kodak", col="gold", delay=.45)]))
A("Kodak ruled photography. It made money on almost every roll of film people bought.",
  B("kodak", [dict(e="film", x=560, y=600, at=0, out=N1), P("🎞️ film = Kodak's money machine", 1340, 420, 46, .4, out=N1)], bg="sky", mood="calm"))
A("Then a twenty-four-year-old engineer named Steve Sasson built something strange: a camera with no film at all.",
  B("kodak", [dict(e="camera", x=620, y=600, w=520, at=0, out=[3, 0]), CD(1340, 330, 620, "Steve Sasson", "Kodak engineer · age 24", .35, col="ink", out=N1),
              ST("NO FILM", 1340, 640, .8, col="red", sz=80, out=N1)]))
A("It weighed about eight pounds, and took black-and-white pictures of just a hundred by a hundred pixels.",
  B("kodak", [dict(e="camera", x=620, y=600, w=520, at=0, out=N1), dict(e="pixels", x=1340, y=560, w=420, at=.35, end=.85, out=N1),
              P("100 × 100 pixels", 1340, 830, 44, .7, out=N1)]))
A("Each photo took twenty-three seconds to save, onto a cassette tape.",
  B("kodak", [dict(e="camera", x=620, y=600, w=520, rec=True, at=0, out=N1), CT(1340, 460, 23, .1, .8, suf=" sec", size=140, col="gold", out=N1),
              P("📼 saved to cassette tape", 1340, 620, 44, .6, out=N1)]))
A("Sasson showed it to Kodak's managers. They were convinced nobody would ever want to look at their photos on a TV screen.",
  B("kodak", [O("samthink", 520, 640, 380, 0, out=N1), dict(e="letter", x=1340, y=300, w=700, head="KODAK MANAGEMENT · 1975",
              body="“No one would ever want to look at their pictures on a television set.”", at=.15, out=N1)]))
A("And a camera without film threatened the film business that paid for everything. So Kodak didn't push it.",
  B("kodak", [DEAL(1340, 560, .45, at=0, txt="DIGITAL?", out=N1), dict(e="film", x=560, y=600, at=0, out=N1)]))
A("Others did. Digital cameras took over, and then phones put a camera in almost every pocket.",
  B("kodak", [dict(e="camera", x=560, y=600, w=420, at=0, out=N1), O("phone", 1340, 600, 420, .55, out=N1), P("📷 → 📱", 960, 300, 60, .4, out=N1)]))
A("In twenty twelve, Kodak, the company that invented the digital camera, filed for bankruptcy.",
  B("kodak", [dict(e="chart", kind="crash", x=300, y=300, w=1320, h=520, at=0, end=.6, out=N1), ST("BANKRUPT", 960, 560, .65, col="red", sz=110, out=N1)], cut=True, mood="tense"))
A("Lesson two: if you don't replace your own product, someone else will.",
  B("kodak", [O("samsad", 520, 620, 460, 0, out=N1), CD(1300, 380, 760, "Lesson #2", "If you don't replace your own product, someone else will.", .2, col="gold", out=N1)]))

# ---------------- #4 BLOCKBUSTER
A("Number four. Dallas, Texas, the year two thousand.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-96.8, 32.78, 8], chap=4, chapsub="THE DEAL THEY LAUGHED AT",
       pins=[dict(at=[-96.8, 32.78], label="Blockbuster HQ", col="gold", delay=.45)]))
A("Blockbuster was the king of movie nights, with almost nine thousand stores.",
  B("bb", [dict(e="store", x=600, y=620, at=0, out=N1), CT(1340, 460, 9000, .2, .8, size=140, col="gold", out=N1), P("🏬 stores worldwide", 1340, 620, 46, .5, out=N1)],
    bg="sky", mood="calm"))
A("Netflix was a small startup that mailed DVDs in red envelopes. That year, it lost fifty-seven million dollars.",
  B("bb", [dict(e="env", x=600, y=600, w=560, at=0, out=N1), CT(1340, 460, 57, .4, .85, pre="-$", suf="M", size=140, col="red", out=N1), P("lost in 2000", 1340, 620, 44, .7, out=N1)]))
A("So its founders flew to Dallas, and offered to sell Netflix to Blockbuster, for fifty million dollars.",
  B("bb", [O("jet", 560, 560, 420, 0, out=N1), dict(e="check", x=1340, y=560, w=620, to="Netflix", amt="$50,000,000", at=.45, out=N1)]))
A("According to Netflix co-founder Marc Randolph, Blockbuster's CEO was struggling not to laugh.",
  B("bb", [O("samyell", 520, 620, 420, 0, out=N1), dict(e="letter", x=1340, y=320, w=680, head="DALLAS · 2000", body="Blockbuster's CEO was “struggling not to laugh.” — Marc Randolph", at=.1, out=N1)]))
A("The answer was no. Ten years later, Blockbuster filed for bankruptcy.",
  B("bb", [DEAL(960, 420, .2, at=0, out=N1), dict(e="store", x=760, y=790, w=440, closed=True, at=.55, out=N1),
           ST("BANKRUPT 2010", 1340, 800, .85, col="red", sz=70, out=N1)]))
A("Today, just one Blockbuster store is left, in Bend, Oregon. And Netflix is worth roughly two hundred fifty billion dollars.",
  B("bb", [P("📍 last store: Bend, Oregon", 960, 280, 46, .05, out=N1), TN("$50M", "$250 BILLION", .2, .85, out=N1)]))
A("Lesson three: the small idea you laugh at today might be the one that replaces you.",
  B("bb", [O("samthink", 520, 620, 460, 0, out=N1), CD(1300, 380, 760, "Lesson #3", "The small idea you laugh at might replace you.", .2, col="gold", out=N1)]))

# ---------------- #3 YAHOO / MICROSOFT
A("Number three. Sunnyvale, California, February twenty oh-eight.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-122.04, 37.37, 8], chap=3, chapsub="THE $44.6 BILLION NO",
       pins=[dict(at=[-122.04, 37.37], label="Yahoo", col="gold", delay=.4), dict(at=[-122.12, 47.67], label="Microsoft", col="red", delay=.6)]))
A("Microsoft wanted to catch up with Google in search. So it made Yahoo an offer of forty-four point six billion dollars.",
  B("yahoo", [dict(e="search", x=960, y=300, w=1100, q="how to catch up with google", at=0, end=.45, out=N1),
              dict(e="check", x=960, y=680, w=760, to="Yahoo", amt="$44,600,000,000", at=.5, out=N1)], bg="sky", mood="tense"))
A("Yahoo's board said the offer substantially undervalued the company. Even when Microsoft raised it, Yahoo still wanted more.",
  B("yahoo", [DEAL(960, 560, .3, at=0, out=N1), P("“substantially undervalues Yahoo”", 960, 300, 46, .05, out=N1)]))
A("A few months later, Microsoft walked away.",
  B("yahoo", [O("jet", 960, 560, 380, 0, out=N1), P("👋 Microsoft withdraws", 960, 300, 50, .3, bg="red", out=N1)]))
A("Then the financial crisis hit, Google kept growing, and Yahoo slowly faded.",
  B("yahoo", [dict(e="chart", kind="crash", x=300, y=300, w=1320, h=520, at=0, end=.95, out=N1)]))
A("In twenty seventeen, Verizon bought Yahoo's main business for about four and a half billion dollars. Roughly a tenth of Microsoft's offer.",
  B("yahoo", [dict(e="bars", x=380, y=360, w=1100, end=.8, rows=[["Microsoft's offer (2008)", 44.6, "green"], ["Verizon deal (2017)", 4.5, "red"]], at=.1, out=N1),
              P("≈ 1/10", 1580, 720, 60, .8, bg="red", out=N1)], cut=True))
A("Lesson four: holding out for a better offer only works if you keep getting stronger.",
  B("yahoo", [O("samsad", 520, 620, 460, 0, out=N1), CD(1300, 380, 760, "Lesson #4", "Holding out only works if you keep getting stronger.", .2, col="gold", out=N1)]))

# ---------------- #2 FACEBOOK (the good no)
A("Number two is the twist. Palo Alto, twenty oh-six.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-122.14, 37.44, 8], chap=2, chapsub="THE NO THAT WAS RIGHT",
       pins=[dict(at=[-122.14, 37.44], label="Facebook", col="green", delay=.45)]))
A("Facebook was two years old. Yahoo offered to buy it, for one billion dollars.",
  B("fb", [O("laptop", 560, 600, 460, 0, out=N1), dict(e="check", x=1340, y=560, w=640, to="Facebook", amt="$1,000,000,000", at=.4, out=N1)], bg="sky", mood="calm"))
A("Its founder, Mark Zuckerberg, was twenty-two. One billion dollars, at twenty-two.",
  B("fb", [CD(1340, 320, 620, "Mark Zuckerberg", "founder · age 22", .05, col="ink", out=N1), T("$1 BILLION", 1340, 620, 110, .45, col="green", out=N1),
           O("samthink", 520, 620, 400, 0, out=N1)]))
A("He said no. According to the book An Ugly Truth, he told his advisers he wouldn't know what to do with the money, and would probably just build another Facebook.",
  B("fb", [DEAL(960, 360, .15, at=0, out=N1), dict(e="letter", x=960, y=640, w=900, head="ACCORDING TO “AN UGLY TRUTH”", body="He wouldn't know what to do with the money – he'd probably just build another Facebook.", at=.45, out=N1)]))
A("Many people in the company thought he was crazy. Zuckerberg later said that after he turned it down, huge numbers of people quit.",
  B("fb", [dict(e="people", x=960, y=700, n=10, at=0, out=N1), P("🚪 many quit", 960, 340, 56, .5, bg="red", out=N1)]))
A("Today, Facebook's parent company Meta is worth around one point six trillion dollars.",
  B("fb", [TN("$1B", "$1.6 TRILLION", .2, .85, out=N1)], mood="bright"))
A("So saying no isn't always the mistake. It depends on whether you believe in what you're building, and whether you're right.",
  B("fb", [O("samhappy", 520, 620, 460, 0, out=N1), CD(1300, 380, 760, "Lesson #5", "A no is only right if you believe in it – and you're right.", .3, col="gold", out=N1)]))

# ---------------- #1 EXCITE / GOOGLE
A("And number one. Silicon Valley, early nineteen ninety-nine.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-122.2, 37.45, 8], chap=1, chapsub="THE MOST EXPENSIVE NO",
       pins=[dict(at=[-122.24, 37.49], label="Excite", col="gold", delay=.4), dict(at=[-122.14, 37.43], label="Google", col="green", delay=.6, dy=1)]))
A("Back then, the hot search engine wasn't Google. It was Excite, a big, popular web portal.",
  B("exc", [dict(e="search", x=960, y=300, w=1100, q="best search engine 1999", at=0, end=.4, out=N1), CD(960, 520, 640, "Excite", "one of the web's biggest portals", .5, col="ink", out=N1)],
    bg="sky", mood="tense"))
A("Google was a tiny startup, run by two Stanford students, Larry Page and Sergey Brin. And they were ready to sell.",
  B("exc", [O("laptop", 560, 600, 420, 0, out=N1), CD(1340, 330, 640, "Larry Page & Sergey Brin", "founders of a tiny startup", .3, col="ink", out=N1),
            P("🏷️ for sale", 1340, 640, 56, .75, bg="red", out=N1)]))
A("According to investor Vinod Khosla, the founders asked one million dollars. Excite's CEO, George Bell, said no.",
  B("exc", [dict(e="check", x=960, y=560, w=720, to="Google", amt="$1,000,000", at=0, out=N1), ST("NO", 1260, 520, .8, col="red", sz=90, out=N1)]))
A("So Khosla talked the price down. Seven hundred fifty thousand dollars.",
  B("exc", [dict(e="check", x=960, y=560, w=720, to="Google", amt="$750,000", at=0, out=N1), CT(960, 860, 750000, .3, .85, from_=1000000, pre="$", size=90, col="gold", out=N1)]))
A("And George Bell still said no.",
  B("exc", [DEAL(960, 560, .3, at=0, out=N1)], cut=True))
A("Two years later, Excite's parent company went bankrupt.",
  B("exc", [dict(e="chart", kind="crash", x=300, y=300, w=1320, h=520, at=0, end=.7, out=N1), ST("BANKRUPT 2001", 960, 560, .7, col="red", sz=100, out=N1)]))
A("And Google became one of the most valuable companies on Earth. Today, its parent company Alphabet is worth around three point six trillion dollars.",
  B("exc", [TN("$750K", "$3.6 TRILLION", .05, .75, out=N1)], mood="bright"))
A("That's almost five million times the price Excite turned down.",
  B("exc", [CT(960, 460, 5000000, .05, .6, from_=1000, suf="×", size=160, col="gold", out=N1), P("what $750,000 turned into", 960, 640, 46, .6, out=N1)]))

# ---------------- OUTRO
A("So what do all these stories have in common? Every no looked smart at the time.",
  B("outro", [O("samthink", 480, 620, 480, 0, out=N1), T("every NO looked smart at the time", 1260, 420, 62, .2, col="gold", out=N1)], bg="sky", mood="calm"))
A("Guitar bands, digital cameras, DVDs by mail, a website for students, and a tiny search engine.",
  B("outro", [dict(e="vinyl", x=300, y=480, r=120, label="", at=.02, out=N1), dict(e="camera", x=640, y=480, w=260, at=.18, out=N1),
              dict(e="env", x=980, y=480, w=280, at=.38, out=N1), O("laptop", 1310, 480, 260, .6, out=N1), dict(e="search", x=960, y=780, w=900, q="google", at=.8, end=.98, out=N1)]))
A("The people who said no weren't stupid. They just measured the future by the present.",
  B("outro", [CD(960, 380, 900, "They measured the future by the present.", "that's the real mistake", .05, col="ink", out=N1)]))
A("Which no would you have said? Tell me in the comments. And if you like true money stories, subscribe.",
  B("outro", [O("samhappy", 560, 600, 560, 0, out=END), CD(1300, 300, 720, "Which no would you have said?", "tell me in the comments 👇", .05, col="ink", out=END),
              P("🔔 Subscribe for more true money stories", 1300, 640, 44, .55, bg="red", out=END)]))

P_ = dict(title="YouTube 17: They Said No to a Fortune",
          _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
          size=[1920, 1080], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+0%",
          lead=0.6, gap=0.48, tail=3.0, crf=21, music=dict(style="ttdark", bpm=140, gain=0.15, duck_ratio=2),
          sfx_vary=True, sfx_gain=0.4, lines=L)
json.dump(P_, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
