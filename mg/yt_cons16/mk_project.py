# YouTube 16 (long form, 16:9): "History's Boldest Con Artists (One Sold the Eiffel Tower)" -> project.json
# Sources (checked 2026-11-17):
# #7 Anna Sorokin: Wikipedia "Anna Sorokin" (NYC mid-2013, posed as German heiress, fake statements EUR 60M in Swiss accounts,
#    $22M loan application City National Nov 2016, $100,000 overdraft Jan 2017, unpaid hotel bills, Marrakesh: Williams paid $62,000,
#    guilty on 8 counts 25 Apr 2019, sentenced 9 May 2019 to 4-12 years; Netflix paid $320,000 for rights, "Inventing Anna" 2022);
#    NBC News 9 May 2019 "fake German heiress ... gets up to 12 years".
# #6 Fyre Festival: Wikipedia "Fyre Festival" (Great Exuma, Bahamas, April 2017; VIP packages up to $12,000 incl. airfare;
#    Dec 2016 influencer promo with models, one celebrity paid $275,000 for one post; disaster relief tents, wet mattresses,
#    cheese sandwiches in foam containers; cancelled first weekend; SEC: raised at least $27.4M from over 100 investors;
#    Oct 2018 McFarland sentenced to 6 years, forfeit $26M); NBC New York / Engadget 11 Oct 2018 (six-year sentence).
# #5 Hitler Diaries: Wikipedia "Hitler Diaries" (Konrad Kujau forged 1981-83; Stern via reporter Gerd Heidemann paid 9.3M DM
#    = $3.7M; sixty volumes; historian Trevor-Roper authenticated, changed his mind at the press conference; forensic analysis
#    quickly confirmed fakes; 'FH' instead of 'AH' on a cover; Kujau and Heidemann spent time in prison; several editors lost jobs);
#    Britannica "Hitler Diaries"; germanhistorydocs.org "Stern presents Hitler's diaries (April 22, 1983)".
# #4 Han van Meegeren: Wikipedia "Han van Meegeren" (Supper at Emmaus accepted by Bredius Sept 1937, bought for fl. 520,000
#    (~EUR 4.6M today) by Rembrandt Society, donated to Museum Boijmans Van Beuningen Rotterdam; Christ with the Adulteress:
#    Goering traded 137 looted paintings; arrested 29 May 1945, aiding the enemy, threatened with death penalty; painted
#    "Jesus among the Doctors" Jul-Dec 1945 watched by court-appointed witnesses; collaboration charges dropped; 12 Nov 1947
#    guilty of forgery and fraud, 1 year; died 30 Dec 1947; earned 5.5-7.5M guilders ~ US$25-30M today); Britannica.
# #3 Gregor MacGregor / Poyais: Wikipedia "Gregor MacGregor" (from 1821 claimed to be Cazique of fictional Poyais on the
#    Mosquito Coast, Honduras; 1822 guidebook; Oct 1822 GBP 200,000 Poyais loan in London; ~250 emigrated 1822-23, more than half
#    died; French trial 1826, acquitted); Smithsonian/CrimeReads excerpt "Poyais".
# #2 Bernie Madoff: Wikipedia "Bernie Madoff" (former Nasdaq chairman; ~$65B missing incl. fabricated gains; 10 Dec 2008 sons
#    reported him after he called it "one big lie"; arrested 11 Dec 2008; 29 Jun 2009 150 years, the maximum; died 14 Apr 2021
#    in prison; trustee recovered ~$14.8B); HISTORY.com "Madoff arrested".
# #1 Victor Lustig: Smithsonian Magazine "The Smoothest Con Man That Ever Lived" (2012) (by 1925; posed as deputy director of
#    the Ministere de Postes et Telegraphes; letters to largest scrap dealers; Hotel de Crillon; tower to be demolished, 7,000 tons
#    of metal; Andre Poisson paid $20,000 cash + $50,000; never reported; returned for second attempt, fled; May 1935 arrested
#    in New York, $51,000 counterfeit in a Times Square locker; 20 years Alcatraz).
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
N1 = [1, 0]
END = [99, 0]

# ---------------- INTRO (hook visible & readable from frame 0, also muted)
A("In nineteen twenty-five, a man sold the Eiffel Tower. He didn't own it. And the buyer never even went to the police.",
  B("intro", [dict(e="title", a="HE SOLD THE EIFFEL TOWER", b="…and he didn't even own it", at=-1, out=[2, 0]),
              O("eiffel", 600, 610, 560, -1, out=N1), O("conman", 1320, 640, 480, -1, out=N1),
              ST("SOLD", 600, 640, .22, col="red", sz=110, out=N1), P("🚫👮 never reported", 1320, 900, 40, .8, bg="red", out=N1)],
    bg="sky", mood="tense"))
A("Other con artists sold a country that didn't exist, fake paintings to the Nazis, and a luxury festival that turned into a disaster camp.",
  B("intro", [P("🏝️ a country that didn't exist", 960, 420, 50, .05, out=N1), P("🖼️ fake paintings", 960, 560, 50, .4, out=N1),
              P("⛺ a 'luxury' festival", 960, 700, 50, .75, out=N1)]))
A("These are seven of the boldest cons in history, counted down from number seven to number one.",
  B("intro", [T("HISTORY'S BOLDEST CONS", 960, 300, 90, 0, col="gold", out=[2, .99]), dict(e="ladder", at=.2, out=[2, .99])]))
A("And number one is so bold, it sounds made up. But it really happened.",
  B("intro", [dict(e="ladderhi", at=.1, out=N1)]))

# ---------------- #7 ANNA DELVEY
A("Number seven. New York, twenty thirteen.",
  dict(type="map", cam=[-98, 39, 1.0], cam2=[-74.0, 40.72, 7], chap=7, chapsub="THE FAKE HEIRESS",
       pins=[dict(at=[-74.0, 40.72], label="New York", col="red", delay=.5)]))
A("A young woman calling herself Anna Delvey shows up in the city's art and party scene. She says she's a rich German heiress.",
  B("delvey", [O("bag", 560, 600, 440, 0, out=[2, 0]), CD(1320, 360, 620, "Anna Delvey", "“rich German heiress”", .35, col="ink", out=N1)], bg="sky", mood="calm"))
A("Her real name was Anna Sorokin. And her fortune only existed on paper.",
  B("delvey", [CD(1320, 360, 620, "Anna Sorokin", "real name", .05, col="ink", out=N1), ST("NO FORTUNE", 1320, 680, .6, col="red", sz=70, out=N1)]))
A("Her fake bank statements claimed she had sixty million euros sitting in Swiss accounts.",
  B("delvey", [O("certs", 560, 600, 460, 0, out=N1), CT(1320, 480, 60, .2, .7, pre="€", suf="M", size=150, col="green", out=N1),
               P("“in Swiss accounts”", 1320, 640, 44, .55, out=N1), ST("FAKE", 560, 600, .85, col="red", sz=90, out=N1)]))
A("With that story, she applied for a twenty-two million dollar loan to open a private art club in Manhattan.",
  B("delvey", [O("bank", 560, 600, 460, 0, out=[2, 0]), CD(1320, 340, 640, "$22M loan", "for a private members' art club", .3, col="ink", out=N1)]))
A("The loan never came through. But one bank did give her a hundred-thousand-dollar overdraft, and she spent it.",
  B("delvey", [ST("DENIED", 1320, 300, .05, col="red", sz=70, out=N1), CT(1320, 520, 100000, .4, .7, pre="$", size=120, col="gold", out=N1),
               P("overdraft", 1320, 660, 44, .5, out=N1), dict(e="fly", k="cash", fx=560, fy=600, tx=1500, ty=260, w=150, at=.75, end=.98, n=5, out=N1)]))
A("She lived in luxury hotels without paying, and a friend ended up covering a sixty-two-thousand-dollar bill from a trip to Marrakesh.",
  B("delvey", [P("🏨 unpaid hotel bills", 560, 360, 46, .05, out=N1), CT(1320, 520, 62000, .5, .85, pre="$", size=130, col="red", out=N1),
               P("✈️ Marrakesh trip · paid by a friend", 1320, 680, 40, .7, out=N1), O("samsad", 560, 660, 380, .1, out=N1)]))
A("In twenty nineteen, a jury in New York found her guilty on eight counts. She got four to twelve years in prison.",
  B("delvey", [O("gavel", 560, 600, 440, 0, out=N1), ST("GUILTY", 1320, 380, .3, col="red", sz=100, out=N1), P("⛓️ 4–12 years", 1320, 600, 56, .75, bg="red", out=N1)]))
A("And then Netflix paid her three hundred twenty thousand dollars for the rights to her story.",
  B("delvey", [O("phone", 560, 600, 400, 0, out=N1), CT(1320, 480, 320000, .4, .8, pre="$", size=130, col="green", out=N1), P("🎬 for her story", 1320, 640, 44, .7, out=N1)]))
A("The lesson: a confident story can open doors long before anyone checks the facts.",
  B("delvey", [O("samthink", 520, 620, 480, 0, out=END), CD(1260, 380, 760, "Lesson #1", "Confidence opens doors before anyone checks", .2, col="gold", out=END)]))

# ---------------- #6 FYRE
A("Number six. The Bahamas, twenty seventeen.",
  dict(type="map", cam=[-80, 28, 2.4], cam2=[-75.85, 23.55, 9], chap=6, chapsub="THE LUXURY FESTIVAL",
       pins=[dict(at=[-75.85, 23.55], label="Great Exuma, Bahamas", col="red", delay=.5)]))
A("Fyre Festival promised a luxury music weekend on a tropical island, with private jets, villas and celebrities.",
  B("fyre", [dict(e="fly", k="jet", fx=200, fy=700, tx=1700, ty=260, w=380, at=0, end=.4, n=1, out=N1),
             O("jet", 560, 600, 460, .38, out=N1), P("✈️ private jets", 1320, 380, 46, .3, out=N1), P("🏡 villas", 1320, 520, 46, .5, out=N1), P("⭐ celebrities", 1320, 660, 46, .7, out=N1)],
    bg="sky", mood="bright"))
A("Famous models posted a glossy promo video, and one celebrity was paid two hundred seventy-five thousand dollars for a single post.",
  B("fyre", [O("phone", 560, 600, 420, 0, out=N1), CT(1320, 480, 275000, .45, .85, pre="$", size=130, col="gold", out=N1), P("for ONE post", 1320, 640, 46, .75, bg="red", out=N1)]))
A("VIP packages with flights and luxury tents cost up to twelve thousand dollars.",
  B("fyre", [CD(960, 330, 700, "$12,000", "VIP package · flights + luxury tent", .1, col="green", out=N1)]))
A("But when the guests landed in April twenty seventeen, there were no villas.",
  B("fyre", [O("jet", 560, 560, 420, 0, out=N1), ST("NO VILLAS", 1320, 520, .55, col="red", sz=100, out=N1)], mood="tense"))
A("Instead, they found disaster relief tents, wet mattresses, and cheese sandwiches in foam boxes.",
  B("fyre", [dict(e="tents", x=700, y=560, at=0, out=[2, 0]), dict(e="sandwich", x=1500, y=560, w=400, at=.65, out=N1), P("🧀 cheese sandwich", 1500, 300, 40, .75, out=N1), P("wet mattresses", 700, 300, 44, .4, out=N1)]))
A("The festival was called off that very first weekend, and guests scrambled to get off the island.",
  B("fyre", [ST("CANCELLED", 1400, 480, .1, col="red", sz=100, out=N1), dict(e="fly", k="jet", fx=1200, fy=760, tx=1800, ty=200, w=300, at=.6, end=.95, n=1, out=N1)]))
A("The founder, Billy McFarland, had raised more than twenty-seven million dollars from over a hundred investors.",
  B("fyre", [O("cash", 560, 600, 440, 0, out=N1), CT(1320, 480, 27.4, .35, .75, pre="$", suf="M", dec=1, size=140, col="gold", out=N1), P("from 100+ investors", 1320, 640, 44, .75, out=N1)]))
A("In twenty eighteen, he was sentenced to six years in prison, and ordered to forfeit twenty-six million dollars.",
  B("fyre", [O("cuffs", 560, 600, 420, 0, out=N1), ST("6 YEARS", 1320, 420, .3, col="red", sz=100, out=N1), P("$26M forfeited", 1320, 640, 50, .75, bg="red", out=N1)]))
A("The lesson: when a deal is all hype and no details, slow down.",
  B("fyre", [O("samthink", 520, 620, 480, 0, out=END), CD(1260, 380, 760, "Lesson #2", "All hype, no details? Slow down.", .2, col="gold", out=END)]))

# ---------------- #5 DIARIES
A("Number five. Hamburg, Germany, nineteen eighty-three.",
  dict(type="map", cam=[10, 51, 2.2], cam2=[9.99, 53.55, 7], chap=5, chapsub="THE FAKE DIARIES",
       pins=[dict(at=[9.99, 53.55], label="Stern magazine · Hamburg", col="red", delay=.5)]))
A("Stern, one of Germany's biggest magazines, announced a sensation: sixty volumes of Adolf Hitler's secret diaries.",
  B("diaries", [dict(e="diaries", x=600, y=760, n=7, at=0, out=N1), CT(1320, 460, 60, .5, .85, suf=" volumes", size=120, col="gold", out=N1),
                P("“secret diaries”", 1320, 620, 46, .7, out=N1)], bg="sky", mood="tense"))
A("A Stern reporter had bought them in secret, for nine point three million marks. That's about three point seven million dollars.",
  B("diaries", [dict(e="diaries", x=600, y=760, n=7, at=0, out=N1), CT(1320, 460, 9.3, .2, .55, suf="M marks", dec=1, size=120, col="red", out=N1),
                P("≈ $3.7 million", 1320, 620, 50, .75, bg="red", out=N1)]))
A("A famous British historian vouched for them at first. Then, at the big press conference, he changed his mind.",
  B("diaries", [O("magnifier", 560, 600, 420, 0, out=N1), P("✅ “they're real”", 1320, 420, 50, .1, dot="green", out=N1), P("❌ changed his mind", 1320, 600, 50, .6, bg="red", out=N1)]))
A("Forensic tests quickly showed what they really were: modern fakes.",
  B("diaries", [O("magnifier", 560, 600, 420, 0, out=N1), dict(e="diaries", x=1320, y=780, n=5, at=0, out=N1), ST("FAKE", 1320, 520, .55, col="red", sz=110, out=N1)]))
A("The forger had even messed up the initials on one cover. Instead of A H, it said F H.",
  B("diaries", [dict(e="diaries", x=960, y=900, n=0, big=True, cover=.65, at=0, out=N1)]))
A("They were written by a forger named Konrad Kujau. He and the reporter both went to prison, and several editors lost their jobs.",
  B("diaries", [O("typewriter", 560, 600, 440, 0, out=N1), O("cuffs", 1320, 460, 300, .4, out=N1), P("editors lost their jobs", 1320, 680, 44, .75, bg="red", out=N1)]))
A("The lesson: when you badly want something to be true, you stop checking.",
  B("diaries", [O("samthink", 520, 620, 480, 0, out=END), CD(1260, 380, 760, "Lesson #3", "Wanting it to be true is a trap", .2, col="gold", out=END)]))

# ---------------- #4 VAN MEEGEREN
A("Number four. The Netherlands, nineteen thirty-seven.",
  dict(type="map", cam=[5, 50, 2.4], cam2=[4.48, 51.92, 8], chap=4, chapsub="THE FAKE VERMEERS",
       pins=[dict(at=[4.48, 51.92], label="Rotterdam", col="red", delay=.5)]))
A("A famous art expert announced a sensational find: a lost painting by the Dutch master Vermeer, called The Supper at Emmaus.",
  B("vermeer", [dict(e="painting", x=620, y=560, w=420, at=0, out=[2, 0]), CD(1340, 380, 640, "“a lost Vermeer”", "The Supper at Emmaus", .5, col="ink", out=N1)], bg="sky", mood="calm"))
A("It was bought for five hundred twenty thousand guilders, millions in today's money, and given to a museum in Rotterdam.",
  B("vermeer", [CT(1340, 460, 520000, .1, .5, pre="ƒ ", size=120, col="gold", out=N1), P("≈ €4.6 million today", 1340, 620, 46, .6, out=N1)]))
A("But it wasn't a Vermeer. It had been painted by a Dutch artist named Han van Meegeren.",
  B("vermeer", [dict(e="painting", x=620, y=560, w=420, at=0, out=[3, 0]), ST("FAKE", 620, 560, .2, col="red", sz=110, out=[3, 0]), CD(1340, 380, 640, "Han van Meegeren", "the painter behind it", .55, col="ink", out=N1)]))
A("During the war, another one of his fakes ended up with Hermann Göring, one of the most powerful Nazis, who traded a hundred and thirty-seven looted paintings for it.",
  B("vermeer", [CT(1340, 460, 137, .5, .85, suf=" paintings", size=110, col="red", out=N1), P("traded for one fake", 1340, 620, 46, .85, bg="red", out=N1)], mood="tense"))
A("In nineteen forty-five, van Meegeren was arrested for helping the enemy. He was even threatened with the death penalty.",
  B("vermeer", [O("cuffs", 1340, 520, 340, 0, out=N1)]))
A("So he confessed: it's not a Vermeer, it's mine. And to prove it, he painted a brand new Vermeer, while court-appointed witnesses watched.",
  B("vermeer2", [P("“It's not a Vermeer. It's mine!”", 960, 540, 60, .02, bg="red", out=[0, .42]), dict(e="painting", x=760, y=560, w=420, at=.45, end=.95, paint=1, out=N1), P("👀 witnesses watching", 1460, 400, 44, .55, out=N1), O("samthink", 1460, 680, 340, .7, out=N1)]))
A("The collaboration charges were dropped. In nineteen forty-seven, he was convicted of forgery and fraud, and sentenced to one year.",
  B("vermeer2", [O("gavel", 560, 600, 440, 0, out=N1), ST("1 YEAR", 1320, 460, .7, col="red", sz=110, out=N1)]))
A("He died just weeks later. Experts estimate his fakes had earned him the equivalent of twenty-five to thirty million dollars today.",
  B("vermeer2", [O("coins", 560, 600, 440, .3, out=N1), T("$25–30M", 1320, 480, 120, .5, col="gold", out=N1), P("in today's money", 1320, 620, 44, .7, out=N1)]))
A("The lesson: even experts can be fooled, especially by the thing they've always hoped to find.",
  B("vermeer2", [O("samthink", 520, 620, 480, 0, out=END), CD(1260, 380, 760, "Lesson #4", "Even experts get fooled", .2, col="gold", out=END)]))

# ---------------- #3 POYAIS
A("Number three. London, eighteen twenty-two.",
  dict(type="map", cam=[-2, 54, 2.4], cam2=[-0.12, 51.5, 8], chap=3, chapsub="THE COUNTRY THAT DIDN'T EXIST",
       pins=[dict(at=[-0.12, 51.5], label="London", col="red", delay=.5)]))
A("A Scottish soldier named Gregor MacGregor told high society that he was the ruler of a country called Poyais, in Central America.",
  B("poyais", [O("conman", 560, 620, 480, 0, out=[2, 0]), CD(1320, 360, 680, "Cazique of Poyais", "“ruler” of a Central American land", .4, col="ink", out=N1)], bg="sky", mood="calm"))
A("He described rich farmland, a growing capital city, and settlers getting wealthy. There was even a guidebook.",
  B("poyais", [P("🌾 rich farmland", 1320, 340, 46, .05, out=N1), P("🏙️ a capital city", 1320, 480, 46, .3, out=N1), dict(e="letter", x=1320, y=560, w=560, head="SKETCH OF THE MOSQUITO SHORE", body="…including the Territory of Poyais", at=.75, out=N1)]))
A("In London, investors bought two hundred thousand pounds' worth of Poyais government bonds.",
  B("poyais", [O("bond", 560, 600, 460, 0, out=N1), CT(1320, 480, 200000, .3, .8, pre="£", size=130, col="gold", out=N1), P("Poyais bonds · 1822", 1320, 640, 44, .7, out=N1)]))
A("And around two hundred and fifty people packed up their lives and sailed across the Atlantic to their new home.",
  dict(type="map", cam=[-45, 35, 1.3], arc=dict(a=[-0.12, 51.5], b=[-84.5, 15.8], label="≈ 250 settlers set sail"),
       pins=[dict(at=[-84.5, 15.8], label="“Poyais” · Mosquito Coast", col="gold", delay=.75)]))
A("When they arrived, there was no capital and no farms. Poyais simply didn't exist.",
  dict(type="map", cam=[-85, 15.5, 7], pins=[dict(at=[-84.5, 15.8], label="“Poyais”", col="red", delay=.1, closed=True)]))
A("Disease spread through the camps. More than half of the settlers died.",
  B("poyais2", [T("MORE THAN HALF", 960, 440, 120, .55, col="red", out=N1), P("of the settlers died", 960, 600, 50, .75, bg="red", out=N1), dict(e="people", x=960, y=910, n=10, at=.05, out=N1)], mood="tense"))
A("Later, MacGregor was put on trial for fraud in France. And he was acquitted.",
  B("poyais2", [O("scales", 560, 600, 440, 0, out=N1), ST("ACQUITTED", 1320, 480, .7, col="green", sz=90, out=N1)]))
A("The lesson: if you can't check something with your own eyes, don't bet everything on it.",
  B("poyais2", [O("samthink", 520, 620, 480, 0, out=END), CD(1260, 380, 760, "Lesson #5", "Can't check it? Don't bet everything.", .2, col="gold", out=END)]))

# ---------------- #2 MADOFF
A("Number two. New York, December twenty-oh-eight.",
  dict(type="map", cam=[-90, 40, 1.4], cam2=[-73.98, 40.76, 8], chap=2, chapsub="THE $65 BILLION LIE",
       pins=[dict(at=[-73.98, 40.76], label="Manhattan", col="red", delay=.5)]))
A("Bernie Madoff was a Wall Street legend, and a former chairman of the Nasdaq stock exchange.",
  B("madoff", [O("bank", 560, 600, 460, 0, out=N1), CD(1320, 360, 680, "Bernie Madoff", "former Nasdaq chairman", .3, col="ink", out=N1)], bg="sky", mood="calm"))
A("For decades, his clients got smooth, steady returns, year after year, no matter what the market did.",
  B("madoff", [dict(e="chart", kind="up", x=260, y=280, w=1400, h=520, at=0, end=.8, out=N1), P("📈 steady, every year", 1500, 220, 44, .5, out=N1)]))
A("But there were no real trades. Money from new investors was used to pay the old ones. A Ponzi scheme.",
  B("madoff", [O("vault", 560, 600, 440, 0, out=N1), dict(e="fly", k="cash", fx=1500, fy=300, tx=560, ty=600, w=150, at=.1, end=.6, n=5, out=N1),
               ST("PONZI SCHEME", 1320, 520, .75, col="red", sz=80, out=N1)], mood="tense"))
A("In December twenty-oh-eight, he told his sons the business was one big lie. They reported him to the authorities.",
  B("madoff", [O("samyell", 560, 620, 440, .1, out=N1), P("“one big lie”", 1320, 420, 56, .35, bg="red", out=N1), O("cuffs", 1320, 640, 280, .8, out=N1)], cut=True))
A("Client statements showed almost sixty-five billion dollars, including gains that were completely made up.",
  B("madoff", [O("burn", 560, 600, 460, 0, out=N1), CT(1320, 480, 65, .2, .7, pre="$", suf="B", size=160, col="red", out=N1), P("incl. fake gains", 1320, 650, 44, .75, out=N1)]))
A("He was sentenced to a hundred and fifty years in prison, the maximum, and died there in twenty twenty-one.",
  B("madoff", [O("gavel", 560, 600, 440, 0, out=N1), ST("150 YEARS", 1320, 460, .3, col="red", sz=100, out=N1)]))
A("A court-appointed trustee has since recovered billions of dollars for the victims.",
  B("madoff", [CT(1320, 480, 14.8, .2, .7, pre="$", suf="B", dec=1, size=140, col="green", out=N1), P("recovered for victims", 1320, 640, 44, .6, out=N1), O("coins", 560, 600, 440, 0, out=N1)]))
A("The lesson: returns that look too smooth to be true usually are.",
  B("madoff", [O("samthink", 520, 620, 480, 0, out=END), CD(1260, 380, 760, "Lesson #6", "Too smooth to be true? It usually is.", .2, col="gold", out=END)]))

# ---------------- #1 LUSTIG
A("Number one. Paris, nineteen twenty-five.",
  dict(type="map", cam=[5, 49, 2.2], cam2=[2.32, 48.87, 8], chap=1, chapsub="THE MAN WHO SOLD THE EIFFEL TOWER",
       pins=[dict(at=[2.29, 48.858], label="Eiffel Tower", col="gold", delay=.4), dict(at=[2.32, 48.867], label="Hôtel de Crillon", col="red", delay=.7, dy=1)]))
A("A con man named Victor Lustig read that the Eiffel Tower was expensive to maintain. And he had an idea.",
  B("lustig", [O("eiffel", 600, 600, 560, 0, out=[3, 0]), P("💸 costly upkeep", 1320, 380, 46, .3, out=N1), O("conman", 1320, 660, 360, .65, out=N1)], bg="sky", mood="tense"))
A("Posing as a deputy director of France's postal and telegraph ministry, he invited the biggest scrap metal dealers in Paris to a meeting at a luxury hotel.",
  B("lustig", [dict(e="letter", x=1340, y=300, w=680, head="MINISTÈRE DES POSTES ET TÉLÉGRAPHES", body="Confidential: you are invited to a meeting at the Hôtel de Crillon…", at=.1, out=N1)]))
A("His secret: the tower would be torn down, and one lucky dealer could buy its seven thousand tons of metal.",
  B("lustig", [CT(1340, 440, 7000, .45, .85, suf=" tons", size=120, col="gold", out=N1), P("🏗️ scrap metal for sale", 1340, 600, 44, .65, out=N1)]))
A("A dealer named André Poisson wanted the deal badly. He paid twenty thousand dollars in cash, plus fifty thousand more to make sure he won.",
  B("lustig2", [O("scrap", 560, 640, 520, 0, out=N1), CT(1320, 460, 70000, .3, .9, pre="$", size=130, col="green", out=N1), P("$20,000 cash + $50,000", 1320, 620, 44, .8, out=N1)]))
A("Then Lustig left Paris with the money. And Poisson was so embarrassed, he never went to the police.",
  B("lustig2", [P("💼 Lustig leaves Paris", 960, 300, 52, .02, out=[0, .5]), dict(e="fly", k="cash", fx=1320, fy=460, tx=1850, ty=200, w=160, at=.05, end=.35, n=4, out=N1), O("samsad", 560, 640, 420, .3, out=N1),
                ST("NEVER REPORTED", 1320, 520, .7, col="red", sz=76, out=N1)], cut=True))
A("Lustig even came back to Paris to try it again, but fled when he suspected the police had been tipped off.",
  B("lustig2", [O("eiffel", 560, 600, 480, 0, out=N1), P("🔁 second attempt", 1320, 400, 50, .2, out=N1), P("🏃 fled", 1320, 560, 50, .7, bg="red", out=N1)]))
A("Years later, in New York, he was caught with fifty-one thousand dollars in fake bills, and sent to Alcatraz.",
  B("lustig2", [O("cuffs", 560, 600, 420, 0, out=N1), CT(1320, 460, 51000, .3, .7, pre="$", size=120, col="red", out=N1), P("in counterfeit bills", 1320, 610, 44, .5, out=N1),
                ST("ALCATRAZ", 1320, 780, .85, col="red", sz=70, out=N1)]))

# ---------------- OUTRO
A("Every con on this list worked the same way: a story so good, that people didn't want to check it.",
  B("outro", [O("samthink", 480, 620, 480, 0, out=N1), T("a story too good to check", 1260, 420, 70, .45, col="gold", out=N1)], bg="sky", mood="calm"))
A("An heiress, a festival, lost diaries, a lost painting, a whole country, perfect returns, and the Eiffel Tower.",
  B("outro", [O("bag", 300, 440, 220, .02, out=N1), O("jet", 620, 440, 240, .14, out=N1), dict(e="diaries", x=940, y=560, n=3, at=.27, out=N1),
              dict(e="painting", x=1260, y=440, w=170, at=.42, out=N1), O("bond", 1580, 440, 220, .55, out=N1), O("vault", 700, 760, 200, .7, out=N1), O("eiffel", 1200, 760, 260, .85, out=N1)]))
A("Which one would have fooled you? Tell me in the comments. And if you like true money stories, subscribe.",
  B("outro", [O("samhappy", 560, 600, 560, 0, out=END), CD(1300, 300, 720, "Which one would fool you?", "tell me in the comments 👇", .05, col="ink", out=END),
              P("🔔 Subscribe for more true money stories", 1300, 640, 44, .55, bg="red", out=END)]))

P_ = dict(title="YouTube 16: History's Boldest Con Artists",
          _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
          size=[1920, 1080], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+0%",
          lead=0.6, gap=0.48, tail=3.0, crf=21, music=dict(style="ttdark", bpm=140, gain=0.15, duck_ratio=2),
          sfx_vary=True, sfx_gain=0.4, lines=L)
json.dump(P_, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
