# YouTube 15 (long form, 16:9, flat 2D "what if" style): "Your Life If You Never Aged" -> project.json
# Idee von Alex (2026-11-10), Stil nach seiner Bildschirmaufnahme (flaches 2D, Bokeh, Ich-Perspektive, Icon-Blasen, Jahr/Alter-Chip). Sam = "du".
SOURCES = """Sources (checked 2026-11-10):
- CDC/NCHS blog "Life Expectancy in the U.S., 1900-2018": life expectancy at birth at the beginning of the 20th century was only 47.3 years.
- Space.com "The Wright Brothers First Heavier-than-air Flight": Dec 17, 1903, Kitty Hawk, first flight lasted 12 seconds, 120 feet.
- The Henry Ford "Ford's Model T: A Car for the Great Multitude": introduced 1908 at $850; by Oct 1922 under $300.
- CDC (archive) "History of 1918 Flu Pandemic": about 500 million people, one-third of the world's population, infected; at least 50 million deaths.
- MoneyWeek "8 July 1932: the Dow Jones Industrial Average hits rock bottom": record high 381.17 on 3 Sep 1929, closed at 41.22 on 8 Jul 1932,
  lost 89%; back to its pre-crash high in 1954.
- NASA "50 Years Ago: One Small Step, One Giant Leap": Armstrong stepped onto the Moon July 20, 1969; hundreds of millions of viewers watched.
- Guinness World Records "1973: First mobile phone call": April 3, 1973, Martin Cooper (Motorola) called Joel Engel (Bell Labs) from a Manhattan
  street, phone weighed about 2.5 pounds.
- History.com "The world's first web site": the Web became a publicly available service on August 6, 1991.
- Apple unveiled the iPhone in January 2007 (Apple newsroom, 9 Jan 2007).
- UBS Global Investment Returns Yearbook 2025 (summary edition, Dimson/Marsh/Staunton): US equities 1900-2024 annualized nominal return 9.7%;
  USD 1 invested in 1900 grew to USD 107,409 by end-2024 (nominal, dividends reinvested) -> $100 = ~$10.7 million. US inflation 2.9%/yr,
  USD 1 of 1900 = USD 37 today.
- Phys.org (2014) "Bright aging sun": rising solar output could end Earth's habitability in ~650 million years (older models); newer 3-D models
  at least 1.5 billion years -> "roughly a billion years" as a round middle; the Sun becomes a red giant in about 5 billion years.
Fiction: the character does not age (hypothetical). Identity changes, Mars in the year 3000 etc. are clearly framed as imagination ("maybe")."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, shot, era, chip=None, **k): L.append(dict(text=t, spec=dict(shot=shot, era=era, chip=chip, **k)))
# ---------- HOOK ----------
A("Imagine you're twenty-five years old. It's the year 1900. And one morning... you simply stop aging.", "wake", "wonder", "1900 · AGE 25")
A("No wrinkles. No gray hair. No back pain. Ever.", "mirror", "wonder", "1900 · AGE 25")
A("Sounds like a dream, right? But over the next hundred and twenty-five years, you're going to find out it comes with some very weird problems.", "timeline", "wonder", "1900 · AGE 25")
A("And one tiny decision you make on day one will turn you into a multi-millionaire.", "teaser", "wonder", "1900 · AGE 25")
A("This is your life if you never aged.", "title", "title")
# ---------- 1900 ----------
A("Let's start. The year is 1900. There are no airplanes, almost no cars, and the average American only lives to about forty-seven.", "street1900", "rag", "1900 · AGE 25", cut=True)
A("You, on the other hand, have all the time in the world.", "smug", "rag", "1900 · AGE 25")
A("So you do something that sounds really boring. You take one hundred dollars, put it into the American stock market, and promise yourself you'll never touch it.", "invest", "rag", "1900 · AGE 25")
A("And a hundred dollars in 1900 is real money. In today's dollars, that's roughly three thousand seven hundred.", "worth1900", "rag", "1900 · AGE 25")
A("Keep an eye on that number. We'll come back to it.", "counter", "rag", "1900 · AGE 25")
# ---------- 1903 - 1929 ----------
A("In 1903, two brothers named Wright fly an airplane for twelve seconds. You're standing right there, thinking it's a cute toy.", "wright", "rag", "1903 · REALLY 28")
A("In 1908, Ford releases the Model T for eight hundred and fifty dollars. Suddenly, everybody wants a car.", "modelt", "rag", "1908 · REALLY 33")
A("And by 1922, a brand new Model T costs less than three hundred. You buy one. Then another. You have time to collect them all.", "modelt2", "rag", "1922 · REALLY 47")
A("Then things get dark. A world war breaks out. And in 1918, a flu pandemic infects about a third of the entire planet. At least fifty million people die.", "flu", "sad", "1918 · REALLY 43", mood="dark")
A("You survive. But it teaches you something important: you don't age, but you're not invincible.", "survive", "sad", "1918 · REALLY 43")
A("Then come the Twenties. Jazz, parties, and a stock market that only seems to go up.", "twenties", "jazz", "1925 · REALLY 50")
A("Until October 1929.", "crash1", "sad", "1929 · REALLY 54", mood="dark")
A("The market crashes. From its peak, the Dow Jones loses eighty-nine percent. People who borrowed money to buy stocks lose everything.", "crash2", "sad", "1929 · REALLY 54")
A("Your little investment gets crushed too. But you have a superpower nobody else has. Time. So you just... wait.", "wait", "sad", "1932 · REALLY 57")
A("And honestly, waiting isn't so bad when you have forever. You learn French. Then Spanish. Then Japanese.", "learn", "lounge", "1935 · REALLY 60")
A("You learn the piano, the guitar, and how to cook pretty much anything. You read every book in the library. Twice.", "skills", "lounge", "1940 · REALLY 65")
A("It takes until 1954 for the Dow to get back to its old high. Twenty-five years. For everyone else, that's a huge part of their life. For you, it's a coffee break.", "recover", "lounge", "1954 · REALLY 79")
# ---------- 1940s - 1960s ----------
A("But by now, the real problems have started.", "problems", "lounge", "1954 · REALLY 79")
A("Your friends got married, had kids, and found their first gray hairs. Some of them are grandparents now.", "friends", "lounge", "1954 · REALLY 79")
A("And you? You still look twenty-five. People start whispering.", "whisper", "lounge", "1954 · REALLY 79")
A("Dating gets complicated too. Every relationship comes with an expiration date, and only you know it.", "dating", "lounge", "1954 · REALLY 79")
A("So you do what every immortal has to do. You pack one suitcase, move to a new city, and start over with a new name.", "move", "lounge", "1955 · REALLY 80")
A("You'll have to do this every twenty years or so. New city. New friends. New life. Again and again.", "moves", "lounge", "1955 · REALLY 80")
A("Every time, you need a new story. Where were you born? Who are your parents? Why do you know so much about the 1920s?", "story", "lounge", "1960 · REALLY 85")
A("In 1969, you sit in front of a TV with hundreds of millions of other people and watch a man step onto the Moon.", "moon", "space", "1969 · REALLY 94")
A("And it hits you. You're going to see things nobody alive today will ever see.", "stars", "space", "1969 · REALLY 94")
A("Think about it. The first airplane you watched flew for twelve seconds. Sixty-six years later, humans are walking on the Moon.", "plane2moon", "space", "1969 · REALLY 94")
# ---------- 1970s - 2000s ----------
A("In 1973, an engineer at Motorola makes the first call from a handheld cell phone. It weighs about two and a half pounds.", "phone", "synth", "1973 · REALLY 98")
A("And who does he call first? His rival at Bell Labs. Just to tell him that Motorola got there first.", "rival", "synth", "1973 · REALLY 98")
A("In 1991, the World Wide Web goes public. And in 2007, the iPhone shows up.", "web", "synth", "2007 · REALLY 132")
A("For most people, that's exciting. For you, it's a nightmare.", "nightmare", "synth", "2007 · REALLY 132", mood="dark")
A("Computers, databases, and later face scans make it harder and harder to just invent a new person.", "scan", "synth", "2015 · REALLY 140")
A("You can't get old. But you also can't hide anymore.", "cameras", "synth", "2015 · REALLY 140")
A("And the stock market keeps doing its thing. Crashes, panics, headlines saying it's the end of the world. You've seen this movie before. You don't sell.", "panics", "synth", "2020 · REALLY 145")
# ---------- TODAY: THE MONEY ----------
A("So here we are. It's 2025. On paper, you're a hundred and fifty years old. And you still look twenty-five.", "today", "modern", "2025 · REALLY 150", cut=True)
A("Now, remember those hundred dollars?", "remember", "modern", "2025 · REALLY 150")
A("According to the UBS Global Investment Returns Yearbook, one dollar put into American stocks in 1900 grew to about one hundred and seven thousand dollars by the end of 2024.", "yearbook", "modern", "2025 · REALLY 150")
A("Which means your hundred dollars is now worth about ten point seven million dollars.", "million", "modern", "2025 · REALLY 150")
A("Your hundred dollars from 1900 had the buying power of about three thousand seven hundred dollars today. Now it buys almost three thousand times more.", "power", "modern", "2025 · REALLY 150")
A("You never had a genius idea. You never ran a big company. You just had one thing. Time.", "lesson", "modern", "2025 · REALLY 150")
A("And that's the real secret of compound interest. The longest player wins. You're not immortal, but starting early is the closest thing to it.", "compound", "modern", "2025 · REALLY 150")
# ---------- THE FUTURE ----------
A("But let's keep going. The year 2100. Everyone you ever met is gone.", "y2100", "cosmic", "2100 · REALLY 225", cut=True)
A("You've watched every invention of the last two centuries happen live. You're basically a walking history book that nobody is allowed to read.", "historybook", "cosmic", "2100 · REALLY 225")
A("The year 3000. Maybe people live on Mars by now. You've changed your name about fifty times.", "y3000", "cosmic", "3000 · REALLY 1,125")
A("One million years from now, cities, languages, maybe even humans themselves have turned into something completely new.", "y1m", "cosmic", "1,000,000 · ???")
A("In roughly a billion years, scientists expect the Sun to be so bright that Earth becomes too hot for life.", "hotearth", "cosmic", "~1 BILLION YEARS")
A("And in about five billion years, the Sun swells into a red giant.", "redgiant", "cosmic", "~5 BILLION YEARS")
A("And you? You're still twenty-five.", "alone", "cosmic", "AGE 25")
# ---------- OUTRO ----------
A("So, would you take the deal? Millions in the bank and all the time in the world, but you outlive everyone you love?", "deal", "wonder", None, cut=True)
A("Tell me in the comments. And if you want more what-if stories like this, subscribe.", "outro", "wonder", None)
P_ = dict(title="YouTube 15: Your Life If You Never Aged", _sources=SOURCES,
          size=[1920, 1080], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+0%",
          lead=0.8, gap=0.45, tail=3.0, crf=20, music=dict(style="eras", gain=0.16, duck_ratio=2),
          sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P_, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
