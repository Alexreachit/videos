# YouTube 13 (long form, 16:9): "Every Trick Your Supermarket Uses on You" -> project.json
# Sources (checked 2026-11-05):
# Hook 76%: Supermarket News 8 May 2012 "POPAI: 76% of Decisions Made In-Store" (POPAI 2012 Shopper Engagement Study).
# #1 Cart: Tasting Table "Grocery Carts Have Gotten Bigger So You'll Buy More Things" – marketing consultant Martin Lindstrom told Today
#    that when cart size doubled (2009-2011) people bought 40% more (consultant claim, attributed as such).
# #2 Produce/bakery at entrance: The Daily Meal (citing National Geographic, Mental Floss): produce up front "sets the tone", lighting;
#    Mental Floss: stores stage baked goods near the entrance.
# #3 Music: Milliman 1982, Journal of Marketing (via Pipedown / HubSpot): slow-tempo music -> 38.2% higher sales volume than fast tempo;
#    no statistically significant difference between no music and slow music.
# #4 Milk: NPR Planet Money 1 Aug 2014 (Kestenbaum): BJ's dairy buyer Rob Olsen calls it "building the basket"; Pollan: walk past goods;
#    Russ Roberts/Olsen: trucks deliver to the back, big cold room, cold chain -> verdict: both. Mental Floss same.
# #5 Eye level / slotting: CNN Business via KVIA 21 May 2022: brands pay "slotting fees"; best spots are eye level, end caps, checkout.
#    Supermarket News 24 Nov 2003 on FTC report: slotting fees for a national launch from a little under $1M to more than $2M.
# #6 End caps: University of South Carolina Moore School 2019 (Ferguson): endcap display without discount raises sales ~60%.
# #7 Price endings: Chicago Booth Review "Yours for only $19.99" (Anderson & Simester): catalog item at $44, $49, $54 -
#    demand almost identical at $44 and $54, significantly higher at $49.
# #8 Quantity surcharge: Victoria University of Wellington news Sept 2026 (Banerjee/Feld): ~3,000 prices, 40 products, 38 supermarkets,
#    26% had a quantity surcharge; cheese 1kg $1.90/100g vs 700g $1.71/100g; other countries 10-30%.
# #9 Shrinkflation: BLS Beyond the Numbers Vol.12 No.2 (Feb 2023): most size changes household paper products (716, 2015-21), snacks (509);
#    overall CPI effect very small (~0.01%/yr).
# #10 Checkout: CNN via KVIA 2022: shoppers spent $6 billion in checkout areas last year (IRI); top UK chains removed candy from checkouts.
# Beat them: PNAS 2015 Xu, Schwarz, Wyer "Hunger promotes acquisition of nonfood objects" (EurekAlert 17 Feb 2015): hungry participants
#    took ~70% more binder clips; hungrier department-store shoppers spent 64% more.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
def B(scene, els, **k): return dict(type="beat", scene=scene, els=els, **k)
def O(k, x, y, w, at=0, **o): return dict(e="obj", k=k, x=x, y=y, w=w, at=at, **o)
def T(txt, x, y, size=64, at=0, **o): return dict(e="tx", txt=txt, x=x, y=y, size=size, at=at, **o)
def KT(txt, x, y, size=90, at=0, **o): return dict(e="kt", txt=txt, x=x, y=y, size=size, at=at, **o)
def P(txt, x, y, size=36, at=0, **o): return dict(e="pill", txt=txt, x=x, y=y, size=size, at=at, **o)
def ST(txt, x, y, at=0, **o): return dict(e="stamp", txt=txt, x=x, y=y, at=at, **o)
def CT(x, y, to, at=0, end=.8, **o): return dict(e="count", x=x, y=y, to=to, at=at, end=end, **o)
def CD(x, y, w, big, small, at=0, **o): return dict(e="card", x=x, y=y, w=w, big=big, small=small, at=at, **o)
def E(kind, at=0, **o): return dict(e=kind, at=at, **o)
N1 = [1, 0]; N2 = [2, 0]; END = [99, 0]

# ================= INTRO
A("You walk into a supermarket to buy one thing. Milk.",
  B("intro", [E("doors", 0, out=N1), O("samhappy", 960, 640, 520, .15, out=N1), O("milk", 1420, 420, 220, .7, out=N1),
              P("shopping list: 🥛 milk", 1420, 640, 40, .75, out=N1)], bg="store", mood="calm"))
A("Twenty minutes later, you walk out with a full cart, and you're not even sure how it happened.",
  B("intro", [O("samcart", 760, 640, 640, 0, out=N1), E("clock", .05, x=1420, y=330, out=N1), E("receipt", .45, x=1420, y=560, mode="long", out=N1)], cut=True))
A("That's not an accident. In one big industry study, seventy-six percent of buying decisions were made inside the store.",
  B("intro", [O("samthink", 520, 640, 520, 0, out=N1), CT(1300, 420, 76, .5, .8, suf="%", size=170, col="gold", out=N1),
              P("of buying decisions made IN the store", 1300, 600, 40, .7, out=N1), P("POPAI shopper study · 2012", 1300, 700, 30, .8, dot="gold", out=N1)]))
A("Supermarkets know that. So every step of your trip, from the cart to the checkout, has been planned.",
  B("intro", [E("plan", 0, route=1, end=.9, out=N1)]))
A("Today, we'll walk through a supermarket together, station by station, and I'll show you ten tricks hiding in plain sight.",
  B("intro", [E("plan", -1, route=1, stations=1, out=N1), P("10 tricks · 5 stations", 960, 110, 44, .6, bg="red", out=N1)]))
A("Some are sneaky. Some are actually fair. And at the end, I'll show you four simple ways to beat them.",
  B("intro", [O("samhappy", 520, 640, 520, 0, out=N1), P("😈 sneaky", 1300, 360, 48, .05, out=N1), P("🤝 actually fair", 1300, 500, 48, .3, out=N1),
              P("🛡️ 4 ways to beat them", 1300, 640, 48, .65, bg="green", out=N1)]))

# ================= STATION 1: ENTRANCE
A("Station one. The entrance. And trick number one starts before you even walk in. The cart.",
  B("entrance", [E("station", 0, n=1, name="THE ENTRANCE", out=[0, .45]), E("trick", .55, n=1, name="THE CART", out=[0, .99]),
                 O("cart", 960, 600, 520, .75, out=N1)], bg="store", mood="calm", trick=1, st=1))
A("Shopping carts have gotten bigger over the years. And a big, empty cart quietly tells you: fill me up.",
  B("entrance", [E("cartgrow", 0, x=960, y=600, end=.5, out=N1), KT("fill me up.", 960, 170, 96, .7, col="gold", out=N1)]))
A("Marketing consultant Martin Lindstrom has said that when cart sizes doubled, shoppers bought about forty percent more.",
  B("entrance", [O("samcart", 600, 620, 560, 0, out=N1), P("2× bigger cart", 1340, 360, 48, .45, dot="gold", out=N1),
                 CT(1340, 530, 40, .65, .9, pre="+", suf="%", size=160, col="green", out=N1), P("bought (his claim)", 1340, 680, 36, .85, out=N1)]))
A("It's one consultant's claim, not a lab study. But the idea is simple: an empty space feels like a job that isn't finished.",
  B("entrance", [O("cart", 600, 600, 520, 0, out=N1), P("⚠️ claim · not a study", 1340, 360, 40, .05, bg="red", out=N1),
                 CD(1340, 470, 640, "empty = unfinished", "your brain wants to fill it", .55, col="ink", out=N1)]))
A("Trick number two. Walk in, and what's the first thing you see? Fruit and vegetables.",
  B("entrance2", [E("trick", 0, n=2, name="FRESH FIRST", out=[0, .99]), E("produce", .6, out=N2)], bg="store"))
A("Bright colors, careful lighting, everything stacked like a market stall.",
  B("entrance2", [E("spot", 0, out=N1), P("🎨 bright colors", 1600, 250, 38, .05, out=N1), P("💡 spotlights", 1600, 360, 38, .3, out=N1),
                  P("🧺 market-stall look", 1600, 470, 38, .55, out=N1)]))
A("It sets the tone for the whole trip: this place is fresh, colorful, and worth slowing down for.",
  B("entrance2", [O("samhappy", 420, 660, 460, 0, out=N1), KT("fresh · colorful · slow down", 1220, 200, 70, .2, col="gold", out=N1),
                  E("produce", -1, mini=1, out=N1)]))
A("And many stores put the bakery close to the door, so one of the first things you smell is fresh bread.",
  B("entrance2", [E("bread", 0, x=1200, y=600, out=N1), E("smell", .3, x=1200, y=430, out=N1), O("samhappy", 480, 640, 460, .1, out=N1)]))
A("Trick number three is something you've probably never noticed. The music.",
  B("music", [E("trick", 0, n=3, name="THE MUSIC", out=[0, .99]), O("speaker", 960, 560, 480, .5, out=N1)], bg="sky", mood="calm"))
A("In nineteen eighty-two, a researcher named Ronald Milliman tested background music in a supermarket.",
  B("music", [O("speaker", 560, 560, 420, 0, out=N2), P("📚 Journal of Marketing · 1982", 1320, 380, 40, .3, out=N1),
              CD(1320, 470, 600, "Milliman", "music test in a real supermarket", .5, col="ink", out=N1)]))
A("On some days, the store played fast music. On other days, slow music.",
  B("music", [E("notes", 0, x=1150, y=520, mode="both", out=N1)]))
A("With slow music, sales were thirty-eight percent higher.",
  B("music", [E("notes", -1, x=1150, y=520, mode="slow", out=N1), CT(1150, 860, 38.2, .2, .7, pre="+", suf="% sales", dec=1, size=110, col="green", out=N1)], cut=True))
A("The idea: slower music, slower steps, more time in front of the shelves.",
  B("music", [O("samcart", 1320, 620, 520, 0, slow=1, out=N1), P("🐢 slower steps", 560, 760, 44, .3, out=N1)]))
A("But here's the twist. The same study found no clear difference between slow music and no music at all.",
  B("music2", [O("samthink", 480, 640, 500, 0, out=N1), E("vs", .1, a="🐢 slow music", b="🔇 no music", out=N1), ST("NO CLEAR DIFFERENCE", 1260, 760, .7, col="gold", sz=56, out=N1)], bg="sky"))
A("So maybe the real trick is simply not playing fast music.",
  B("music2", [ST("NO FAST MUSIC", 1260, 520, .2, col="red", sz=80, rot=-5, out=N1), O("speaker", 480, 600, 380, 0, out=N1)]))
A("But the biggest trick of all is built into the floor plan itself. And it's waiting at the very back.",
  B("music2", [E("plan", 0, route=2, end=.95, hl="back", out=N1)], mood="tense"))

# ================= STATION 2: BACK WALL
A("Station two. The back wall. Trick number four. The milk.",
  B("back", [E("station", 0, n=2, name="THE BACK WALL", out=[0, .5]), E("trick", .5, n=4, name="THE MILK", out=[0, .99])], bg="aisle", mood="tense", trick=4, st=2, dolly=1))
A("Almost everyone needs milk, eggs, or butter. So where are they? Usually at the very back of the store.",
  B("back", [E("dairyglow", .35, out=N1), P("🥛 milk · 🥚 eggs · 🧈 butter", 960, 150, 44, .05, out=N1), KT("the very back.", 960, 880, 80, .7, col="gold", out=N1)]))
A("To get there, you walk past aisle after aisle of other stuff.",
  B("back2", [E("plan", 0, route=3, end=.95, items=1, out=N1)], bg="sky"))
A("A dairy buyer told NPR the industry even has a name for this. Building the basket.",
  B("back2", [O("cart", 560, 620, 460, 0, out=N1), E("fill", .25, x=560, y=560, out=N1), KT("BUILDING THE BASKET", 1300, 470, 84, .55, col="gold", out=N1),
              P("dairy buyer · NPR 2014", 1300, 600, 34, .75, dot="gold", out=N1)]))
A("The longer your walk, the more chances to grab something you never planned to buy.",
  B("back2", [E("receipt", 0, x=1320, y=520, mode="long", out=N1), O("samcart", 560, 640, 540, 0, out=N1)]))
A("But to be fair, there's a boring reason too. Delivery trucks unload at the back, and the big cold rooms are right there.",
  B("back3", [O("truck", 520, 620, 560, .05, drive=1, out=N1), E("coldroom", .4, x=1360, y=560, out=N1), P("🤝 fair point", 960, 150, 44, .1, bg="green", out=N1)], bg="sky", mood="calm"))
A("Milk has to stay cold the whole way, from the truck, to the cold room, to the fridge. Keeping that trip short just makes sense.",
  B("back3", [E("chain", 0, out=N1)]))
A("So it's probably both. Convenient for the store, and very good for sales.",
  B("back3", [CD(600, 380, 640, "logistics ✓", "trucks + cold rooms", .05, col="green", out=N1), CD(1320, 380, 640, "sales ✓", "you walk past everything", .4, col="red", out=N1),
              T("+", 960, 500, 140, .3, col="gold", out=N1)]))

# ================= STATION 3: AISLES
A("Station three. The aisles. Trick number five. Look straight ahead at any shelf.",
  B("aisles", [E("station", 0, n=3, name="THE AISLES", out=[0, .5]), E("trick", .45, n=5, name="EYE LEVEL", out=[0, .99]),
               E("shelf", .7, out=N1)], bg="sky", mood="tense", trick=5, st=3))
A("The products right at eye level are the ones you're most likely to grab. And that spot is not free.",
  B("aisles", [E("shelf", -1, eye=.05, out=N1), ST("NOT FREE", 1500, 760, .75, col="red", sz=64, out=N1)]))
A("Brands pay supermarkets so-called slotting fees, to get onto the shelves, and into the best spots.",
  B("aisles", [E("shelf", -1, eye=-1, pay=.2, out=N1), P("💸 slotting fees", 1730, 300, 44, .1, bg="red", out=N1)]))
A("In two thousand three, a report by the US Federal Trade Commission found that getting one new product onto shelves nationwide could cost from under one million, to over two million dollars.",
  B("aisles2", [CD(560, 300, 640, "FTC report · 2003", "slotting fees for one national launch", .05, col="ink", out=N1),
                E("range", .45, x=980, y=520, w=820, lo=1, hi=2, max=2.4, lab="M", out=N1), O("cash", 560, 700, 360, .3, out=N1)], bg="sky"))
A("So next time, look above and below eye level too. The best spot isn't always the best deal.",
  B("aisles2", [E("shelf", 0, eye=-1, look=.1, out=N1)]))
A("Trick number six is waiting at the end of every aisle. Those big displays are called end caps.",
  B("aisles3", [E("trick", 0, n=6, name="END CAPS", out=[0, .99]), E("endcap", .5, x=1160, y=600, out=N2), O("samthink", 480, 650, 460, .55, out=N2)], bg="aisle", dolly=1))
A("They look like special offers. But researchers at the University of South Carolina estimated that just putting a product on an end cap raises its sales by about sixty percent, even with no discount at all.",
  B("aisles3", [P("looks like a deal…", 1220, 120, 40, .05, out=N1), CT(1630, 500, 60, .5, .78, pre="+", suf="%", size=150, col="green", out=N1),
                P("sales", 1630, 620, 40, .7, out=N1), ST("NO DISCOUNT", 1630, 760, .85, col="red", sz=54, rot=6, out=N1)]))
A("Sixty percent more sales, without the price changing by a single cent.",
  B("aisles4", [E("bars", 0, x=520, y=330, w=1000, rows=[["normal shelf", 100, "blue"], ["end cap", 160, "green"]], end=.55, out=N1), P("same price 🏷️", 1520, 820, 44, .6, bg="red", out=N1)], bg="sky"))
A("Okay. So far, the tricks were about where things are. The next three are about the numbers on the price tag.",
  B("aisles4", [E("receipt", 0, x=600, y=520, mode="tricks", upto=6, out=N1), O("tag", 1400, 560, 420, .55, out=N1)], mood="tense"))
A("And one of them is probably happening right now, in your own kitchen.",
  B("aisles4", [E("kitchen", 0, out=N1), ST("?!", 1500, 300, .6, col="red", sz=110, out=N1)]))

# ================= STATION 4: PRICE TAG
A("Station four. The price tag. Trick number seven. Why does so much cost four ninety-nine, instead of five dollars?",
  B("price", [E("station", 0, n=4, name="THE PRICE TAG", out=[0, .4]), E("trick", .4, n=7, name="THE 9 ENDING", out=[0, .99]),
              E("bigtag", .55, x=960, y=560, a="$4.99", b="$5.00", out=N1)], bg="sky", mood="calm", trick=7, st=4))
A("Two marketing professors tested this with a clothing catalog. The same item was offered at forty-four dollars, forty-nine dollars, and fifty-four dollars.",
  B("price", [E("tags3", 0, out=N1)]))
A("At forty-four and fifty-four, demand was almost the same. But at forty-nine, it sold significantly more.",
  B("price", [E("tags3", -1, bars=.05, out=N1)], cut=True))
A("A higher price, and more sales. Just because it ended in a nine.",
  B("price2", [O("samyell", 520, 640, 520, 0, out=N1), KT("higher price → more sales", 1300, 420, 70, .1, col="gold", out=N1), T("…9", 1300, 600, 160, .55, col="red", out=N1)], bg="sky"))
A("Trick number eight. The big pack is always the better deal, right?",
  B("bulk", [E("trick", 0, n=8, name="THE BIG PACK", out=[0, .99]), E("packs", .45, out=N2)], bg="sky", mood="tense"))
A("Not always. This year, a researcher in New Zealand checked around three thousand prices, in thirty-eight supermarkets.",
  B("bulk2", [E("nz", 0, out=N1), CT(1320, 420, 3000, .4, .65, suf=" prices", size=100, col="gold", out=N1), P("38 supermarkets · 2026", 1320, 560, 40, .7, out=N1)], bg="sky"))
A("About one in four products cost more per gram in the bigger pack.",
  B("bulk2", [E("grid", 0, n=4, bad=1, x=960, y=480, out=N1), P("26% · bigger pack = pricier per gram", 960, 820, 44, .6, bg="red", out=N1)], cut=True))
A("In one example, a big block of cheese cost more per hundred grams than a smaller block of the same brand.",
  B("bulk3", [E("packs", 0, cheese=1, out=N1)], bg="sky"))
A("Studies in other countries have found the same thing in roughly ten to thirty percent of cases. So check the small price per kilo, or per ounce, on the shelf label.",
  B("bulk3", [E("unitlabel", 0, out=N1), P("other countries: 10–30%", 1440, 220, 40, .05, out=N1)]))
A("Trick number nine. The pack looks the same. The price looks the same. But there's less inside.",
  B("shrink", [E("trick", 0, n=9, name="THE SHRINKING PACK", out=[0, .99]), E("shrink", .4, out=N2)], bg="sky", mood="tense"))
A("It's called shrinkflation.",
  B("shrink", [KT("SHRINKFLATION", 960, 150, 110, .05, col="red", out=N1)], cut=True))
A("The US Bureau of Labor Statistics tracks it. Household paper products, like paper towels, had the most size changes, followed by snacks like chips.",
  B("shrink2", [E("bars", .15, x=420, y=330, w=1080, rows=[["🧻 household paper", 716, "red"], ["🍟 snacks", 509, "gold"]], end=.85, out=N1),
                P("size changes recorded · 2015–2021 (BLS)", 960, 230, 36, .05, out=N1)], bg="sky"))
A("To be fair, the government's analysis found it barely moves overall inflation. But for the products it hits, you're simply paying more for less.",
  B("shrink2", [P("🤝 overall inflation: tiny effect", 960, 260, 44, .05, bg="green", out=N1), E("shrink", .4, mini=1, out=N1), ST("MORE FOR LESS", 1460, 640, .75, col="red", sz=60, out=N1)]))
A("You've made it through the whole store. Your cart is full. But there's one last trap, and it's the one you can't walk around.",
  B("shrink3", [O("samcart", 560, 640, 560, 0, out=N1), E("receipt", .2, x=1340, y=520, mode="tricks", upto=9, out=N1)], bg="sky", mood="tense"))

# ================= STATION 5: CHECKOUT
A("Station five. The checkout. Trick number ten.",
  B("checkout", [E("station", 0, n=5, name="THE CHECKOUT", out=[0, .55]), E("trick", .55, n=10, name="THE LINE", out=[0, .99])], bg="sky", mood="tense", trick=10, st=5))
A("You're waiting in line. You're bored, maybe a bit tired. And right next to you: candy, drinks, snacks. Small stuff you can grab with one hand.",
  B("checkout", [E("belt", 0, out=N2), O("samthink", 300, 660, 440, .1, out=N1), E("grab", .7, out=N1)]))
A("According to the market research firm IRI, shoppers in the US spent about six billion dollars in one year, just in checkout areas.",
  B("checkout", [CT(1480, 220, 6, .4, .75, pre="$", suf=" BILLION", size=110, col="gold", out=N1), P("in one year · checkout areas (IRI)", 1480, 330, 34, .7, out=N1)], cut=True))
A("Some big supermarket chains in the UK have even removed candy from their checkouts completely.",
  B("checkout2", [E("uk", 0, out=N1)], bg="sky"))

# ================= BEAT THEM
A("So how do you beat a store that was designed to make you spend more? Here are four simple moves.",
  B("beat", [O("samyell", 960, 640, 520, 0, out=N1), KT("4 ways to beat them", 960, 170, 90, .4, col="gold", out=N1)], bg="sky", mood="bright", trick=0, st=6))
A("One: bring a list, and stick to it.",
  B("beat2", [E("tips", 0, upto=1, out=N1)], bg="sky"))
A("Two: if you only need a few things, take a basket instead of a cart.",
  B("beat2", [E("tips", -1, upto=2, out=N1)]))
A("Three: look up, look down, and check the unit price before you grab the big pack.",
  B("beat2", [E("tips", -1, upto=3, out=N1)]))
A("And four, the easiest one: don't shop hungry.",
  B("beat2", [E("tips", -1, upto=4, out=N1)]))
A("In a study published in twenty fifteen, hungry people asked for about seventy percent more binder clips. Not food. Binder clips.",
  B("beat3", [E("clips", 0, x=1320, y=560, end=.6, out=N1), O("samthink", 480, 640, 480, 0, out=N1), CT(1320, 220, 70, .3, .6, pre="+", suf="%", size=120, col="red", out=N1)], bg="sky"))
A("And shoppers leaving a department store who were hungrier had spent sixty-four percent more.",
  B("beat3", [O("samsad", 480, 640, 480, 0, out=N1), CT(1320, 460, 64, .3, .7, pre="+", suf="% spent", size=130, col="red", out=N1), P("PNAS · 2015", 1320, 620, 36, .6, dot="gold", out=N1)]))

# ================= OUTRO
A("Supermarkets aren't evil. Some of these tricks are just good business, and some, like the cold rooms at the back, are simply logistics.",
  B("outro", [O("samhappy", 520, 640, 500, 0, out=N1), E("receipt", .2, x=1320, y=520, mode="tricks", upto=10, out=N1)], bg="store", mood="calm", trick=0, st=0))
A("But once you've seen them, you can't unsee them.",
  B("outro", [KT("you can't unsee them.", 960, 520, 100, .1, col="gold", out=N1)]))
A("So, which trick has gotten you the most? The milk at the back, the nine-ninety-nine prices, or the candy at the checkout? Tell me in the comments.",
  B("outro", [E("poll", 0, out=END), O("samthink", 330, 680, 380, 0, out=END)]))
A("And if you want more stories about where your money really goes, subscribe.",
  B("outro", [P("🔔 Subscribe for more money stories", 960, 120, 48, .2, bg="red", out=END)]))

P_ = dict(title="YouTube 13: Every Trick Your Supermarket Uses on You",
          _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
          size=[1920, 1080], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+4%",
          lead=0.5, gap=0.4, tail=3.0, crf=21, music=dict(style="ttdark", bpm=140, gain=0.13, duck_ratio=2),
          sfx_vary=True, sfx_gain=0.4, lines=L)
json.dump(P_, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
