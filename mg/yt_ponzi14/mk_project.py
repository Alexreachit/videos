# YouTube 14 (lang, 16:9, 3D-Toon): "The Man Who Invented the Ponzi Scheme" – Charles Ponzi 1903–1949.
# Ponzi selbst wird NICHT gezeichnet (nur gesichtslose Silhouette mit Hut). Sam = Gastgeber.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SOURCES = """Sources (checked 2026-11-07):
- Wikipedia "Charles Ponzi": born 3 Mar 1882 Lugo, Italy; 15 Nov 1903 Boston with $2.50 after gambling on the voyage; dishwasher/waiter, fired for
  theft + short-changing; 1907 Montreal, Banco Zarossi paid 6% (double), funded by new deposits, failed, Zarossi fled to Mexico; forged check $423.58,
  prison in Canada; Atlanta prison for smuggling immigrants; 1919 School Street office; IRCs cheap in Italy after WWI inflation, exchanged for US stamps,
  legal in principle, claimed >400% net; Hanover Trust manager refused loan, later Ponzi bought controlling interest; 50% in 45 days or 100% in 90 days,
  banks ~5%/yr; up to $250,000/day; Lexington mansion; mother brought first class; Barron: 160 million IRCs needed, ~27,000 in circulation; paid out
  $2M in three days; McMasters 2 Aug 1920; bank seized 11 Aug; 86 mail-fraud counts; pleaded guilty, 5 yrs federal, released after ~3.5 yrs; state
  trials; Florida swampland 200% in 60 days; deported 7 Oct 1934; died Rio 1949 charity ward, estate $75; losses ~$20M, <30 cents per dollar.
- Mental Floss "Charles Ponzi scheme facts": $2.50 arrival; letter from Spain with reply coupon; 160 million needed vs 27,000; $20M.
- New England Historical Society: 50%/45 days or 100%/90 days; up to $250,000 a day; $2M in three days; McMasters "robbing Peter to pay Paul";
  arrested Aug 12, 1920 on 86 counts; Florida 200% in 60 days; died in charity hospital Rio.
- WGBH (2014) "This week in history: the Boston Post takes down Charles Ponzi": first Post story 24 Jul 1920; Barron consultant; 11 Aug forgery story;
  surrendered 12 Aug; losses $20M, <30 cents on the dollar; Lexington mansion.
- Mass Moments "Ponzi Scheme Begins to Unravel": Post series won the paper its first Pulitzer Prize.
- IBTimes UK: buried with the $75 he had saved for his funeral; up to $250,000 a day.
- History.com "How did the Ponzi scheme get its name?": Madoff pleaded guilty 2009, $65 billion swindle; Ponzi deported 1934, died in poverty in Brazil 1949.
- Boston Globe 2014/2023: Ponzi's former Lexington house for sale.
Example with 10 investors x $100 is an illustration (labeled as example)."""
L = []
def A(t, shot, ui=None, **k):
    spec = dict(shot=shot); spec.update(k)
    if ui: spec["ui"] = ui
    L.append(dict(text=t, spec=spec, **({"rate": k.pop("rate")} if "rate" in k else {})))
# ---- Hook ----
A("In the summer of 1920, thousands of people in Boston lined up in the street to hand their savings to one man.", "street_wide", "date1920")
A("He promised them fifty percent profit in just forty-five days.", "office_door", "promise")
A("Banks were paying about five percent. Per year.", "bank_compare", "compare")
A("At his peak, he was taking in up to two hundred and fifty thousand dollars a day.", "money_rain", "perday")
A("And a few weeks later, it all came crashing down.", "crash_teaser", None, mood="dark")
A("His name was Charles Ponzi. And this is how one man turned postage stamps into the most famous scam in history.", "title", "title")
# ---- Kapitel 1 ----
A("Ponzi was born in Italy in 1882.", "map_italy", "ch1", cut=True)
A("In November 1903, he stepped off a ship in Boston with just two dollars and fifty cents in his pocket. He had gambled away the rest on the way over.", "ship", "cash250")
A("He washed dishes. He waited tables. And he got fired for short-changing customers and for stealing.", "diner", "fired")
A("In 1907, he moved to Montreal and got a job at a small bank run by a man named Luigi Zarossi.", "bank_ext", "montreal")
A("The bank paid six percent interest on deposits, double the normal rate. Customers loved it.", "bank_queue", "sixpct")
A("But the interest wasn't coming from profits. It was paid with money from new deposits.", "bank_flow", "flow1")
A("The bank collapsed, and Zarossi fled to Mexico with a large part of the customers' money.", "bank_crash", "mexico", mood="dark")
A("Ponzi was watching. And he took notes.", "silhouette_close")
A("Soon after, he forged a check for four hundred and twenty-three dollars and fifty-eight cents, and went to prison in Canada.", "prison", "check")
A("After that came a second prison term in Atlanta, for helping to smuggle immigrants into the United States.", "prison2", "atlanta")
# ---- Kapitel 2 ----
A("By 1919, Ponzi was back in Boston, with a small office on School Street.", "office_ext", "ch2", cut=True, mood="calm")
A("One day, a letter arrived from Spain. Inside was something called an international reply coupon.", "desk_letter", "letter")
A("The idea was simple. You buy a coupon in one country and mail it abroad, and the receiver trades it for a local stamp to send a reply.", "desk_coupon", "irc_how")
A("But after the First World War, prices in Europe had exploded. In Italy, the coupons had become cheap.", "map_europe", "inflation")
A("Buy coupons cheap in Italy, trade them for more valuable stamps in America, and pocket the difference.", "desk_arb", "arb")
A("On paper, this was legal. Ponzi claimed it could make a profit of over four hundred percent.", "desk_arb2", "pct400")
A("But there was a catch. Each coupon traded for a stamp worth just a few cents. To make real money, you would need mountains of them.", "coupon_mountain", "catch")
A("Ponzi didn't care. He didn't need the stamps to work. He just needed people to believe they did.", "silhouette_close2")
# ---- Kapitel 3 ----
A("He founded the Securities Exchange Company, and made a simple promise: fifty percent profit in forty-five days, or double your money in ninety.", "office_sign", "ch3", cut=True)
A("His first investors were friends and neighbors. And to their surprise, they actually got paid.", "first_inv", "paid")
A("But that money wasn't coming from stamps. It came from the next investors.", "flow2", "flow2")
A("That's the whole trick. Old investors get paid with new investors' money. As long as more comes in than goes out, everything looks perfect.", "pyr_1", "trick")
A("Imagine ten people put in a hundred dollars each. Forty-five days later, they want one hundred and fifty back. That's fifteen hundred dollars. So you need fifteen new people just to pay the first ten.", "pyr_2", "example")
A("And those fifteen will soon want their money too. Every round, the pyramid has to grow.", "pyr_3", "grow")
A("And the happy investors did his marketing for him. They told everyone they knew.", "word_mouth")
A("Wait! If you're enjoying this, hit subscribe. It's free. Unlike Ponzi's company.", "sam_shout", "shout", rate="+22%", volume="+25%")
# ---- Kapitel 4 ----
A("By the summer of 1920, Boston had Ponzi fever. Crowds lined up outside his office on School Street.", "street_crowd", "ch4", cut=True, mood="bright")
A("At his peak, he was taking in up to two hundred and fifty thousand dollars a day.", "money_room", "perday2")
A("He bought a mansion in Lexington, and brought his mother over from Italy, first class.", "mansion", "mansion")
A("He even bought a controlling stake in the Hanover Trust bank. The same bank whose manager had refused to lend him money.", "hanover", "hanover")
A("The man who arrived with two dollars and fifty cents was now living like a millionaire.", "mansion_night", "rich")
# ---- Kapitel 5 ----
A("But one newspaper started asking questions. On July 24th, 1920, the Boston Post put Ponzi on its front page.", "newspaper", "ch5", cut=True, mood="dark")
A("The Post brought in Clarence Barron, a famous financial journalist. And he did some simple math.", "math_desk", "barron")
A("To cover all the money people had invested, Ponzi would need around one hundred and sixty million reply coupons.", "coupon_math", "c160m")
A("But only about twenty-seven thousand were actually in circulation.", "coupon_math2", "c27k")
A("Investors panicked and rushed to get their money back. Ponzi paid out two million dollars in just three days.", "bank_run", "run2m")
A("On August 2nd, his own former publicist, William McMasters, went public. Ponzi was deep in debt, robbing Peter to pay Paul.", "newspaper2", "mcmasters")
A("On August 11th, the Post revealed his old forgery conviction from Montreal.", "newspaper3", "forgery")
A("The next day, Charles Ponzi turned himself in to federal authorities.", "arrest", "aug12")
A("Auditors found that his company owed millions of dollars more than it had.", "audit", "audit")
# ---- Kapitel 6 ----
A("Investors lost about twenty million dollars. Many got back less than thirty cents for every dollar.", "pyr_crash", "ch6", cut=True)
A("The state seized his bank, Hanover Trust.", "hanover_closed", "seized")
A("Ponzi faced eighty-six counts of mail fraud. He pleaded guilty to one, and went to federal prison.", "prison", "counts")
A("After about three and a half years, he was out. But Massachusetts put him on trial again.", "court", "state")
A("Out on bail, he went to Florida and started selling swampland, promising two hundred percent in sixty days.", "swamp", "florida")
A("He was caught again, and spent years more behind bars.", "prison2", "again")
A("In 1934, he was deported to Italy. Later, he moved to Brazil.", "map_brazil", "deport")
A("In 1949, Charles Ponzi died in a charity hospital in Rio de Janeiro. He left behind about seventy-five dollars.", "rio", "dollars75", mood="calm")
A("And the Boston Post? It won the Pulitzer Prize for exposing him.", "newspaper_prize", "pulitzer")
# ---- Outro ----
A("A hundred years later, the trick still works. In 2009, Bernie Madoff pleaded guilty to a Ponzi scheme worth about sixty-five billion dollars.", "pyr_big", "madoff", cut=True)
A("So here is how to spot one.", "sam_studio", "spot")
A("One: high returns that are almost guaranteed.", "sam_studio", "spot1")
A("Two: a secret strategy that nobody can really explain.", "sam_studio", "spot2")
A("Three: you get paid with money from people who join after you.", "sam_studio", "spot3")
A("Because in a Ponzi scheme, the last people in always pay for the first.", "pyr_end")
A("Subscribe to Roundhead Stories for more money stories like this one.", "sam_end", "end", mood="bright")
# Lautstaerke/Tempo fuer Sams Ruf: gleiche Stimme, kein Pitch
for l in L:
    if l["spec"].get("volume"): l["volume"] = l["spec"].pop("volume")
    if l["spec"].get("rate"): l["rate"] = l["spec"].pop("rate")
    if l["spec"].get("shot") == "sam_shout": l["afx"] = "volume=4dB"  # Normalisierung je Zeile -> Ruf danach 4 dB lauter
P = dict(title="YouTube 14: The Man Who Invented the Ponzi Scheme", _sources=SOURCES, size=[1920, 1080], fps=30, scene="scene.html",
         voice="en-US-AndrewMultilingualNeural", rate="+4%", lead=0.5, gap=0.42, tail=3.0, crf=21,
         music=dict(style="suspense", bpm=96, gain=0.13, duck_ratio=2), sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
