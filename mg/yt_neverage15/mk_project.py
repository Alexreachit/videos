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
Version 2 (Alex, 11.11.): Fokus auf Gefuehl "erst cool, dann Probleme" statt Geschichte. Fakten nur noch: Sonne (Phys.org).
Fiction: the character does not age (hypothetical). Identity changes, Mars in the year 3000 etc. are clearly framed as imagination ("maybe")."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, shot, era, chip=None, **k): L.append(dict(text=t, spec=dict(shot=shot, era=era, chip=chip, **k)))
# ---------- AKT 1: "Ich lebe fuer immer!" ----------
A("Imagine you wake up one morning, and your body has simply... stopped aging.", "wake", "wonder", "DAY 1 · AGE 25")
A("No wrinkles. No gray hair. No back pain. Ever.", "mirror", "wonder", "DAY 1 · AGE 25")
A("At first, this is the best thing that has ever happened to you. You're basically a superhero.", "hype", "wonder", "DAY 1 · AGE 25")
A("This is your life if you never aged.", "title", "title")
A("The first thing you notice is that the pressure is gone. No more, I'm getting too old for this. No ticking clock. Ever.", "nopressure", "modern", "YEAR 1 · AGE 25", cut=True)
A("You sleep in. You take a year off. Nobody can tell you that you're wasting your life, because you literally can't.", "sleepin", "modern", "YEAR 1 · AGE 25")
A("So you learn everything. French. Then Spanish. Then Japanese.", "learn", "modern", "YEAR 2 · AGE 25")
A("You learn the piano, the guitar, and how to cook pretty much anything. You read every book you ever wanted to read.", "skills", "modern", "YEAR 4 · AGE 25")
A("You travel to every single country on Earth. Not on some rushed two-week vacation. You live in each one for a while.", "travel", "modern", "YEAR 6 · AGE 25")
A("You take every risk. Start a business, fail, start another one. Who cares? You can try again a hundred times.", "risks", "modern", "YEAR 7 · AGE 25")
A("Want to be a doctor, a pilot and a chef? Easy. Just become all of them, one after another.", "careers", "modern", "YEAR 8 · AGE 25")
A("You even put a little money into the stock market and just leave it there. When you have decades to wait, compound interest becomes your best friend.", "invest", "modern", "YEAR 8 · AGE 25")
A("Your friends are jealous. What's your secret, they ask. And you just smile.", "envy", "modern", "YEAR 9 · AGE 25")
A("Life is perfect. You feel like you've beaten the game.", "king", "modern", "YEAR 9 · AGE 25")
# ---------- AKT 2: Die ersten Risse ----------
A("But then, slowly, the problems start.", "problems", "lounge", "YEAR 10 · LOOKS 25", cut=True)
A("Ten years later, your friends start to notice. They have their first wrinkles and their first gray hairs. You look exactly the same.", "tenyears", "lounge", "YEAR 10 · LOOKS 25")
A("At first they joke about it. Then they stop joking. People start whispering behind your back.", "whisper", "lounge", "YEAR 12 · LOOKS 25")
A("Your best friend turns forty and throws a huge party. And you still get asked for your ID at the door.", "party40", "lounge", "YEAR 15 · LOOKS 25")
A("So you start lying. Botox. Great genes. A really strict skincare routine. And every lie needs another lie.", "lies", "lounge", "YEAR 14 · LOOKS 25")
A("Then your parents get old. You sit next to them in the hospital, and the nurse thinks you're their grandson.", "parents", "sad", "YEAR 25 · LOOKS 25", mood="dark")
A("At the funeral, people who have known you your whole life don't recognize you. They think you're some distant relative.", "funeral", "sad", "YEAR 27 · LOOKS 25")
A("Love gets complicated too. You fall in love, but every year, your partner gets a little older, and you don't.", "dating", "sad", "YEAR 30 · LOOKS 25")
A("After twenty years, a waiter asks if she's your mom. Every time it happens, it hurts a little more.", "motherson", "sad", "YEAR 45 · LOOKS 25")
A("Even normal life stops working. Your ID says you're fifty, but your face says twenty-five. Banks, doctors, employers. Everyone gets suspicious.", "paperwork", "lounge", "YEAR 50 · LOOKS 25")
A("Try explaining to a doctor why your scans look twenty-five, when your file says you should be sixty.", "doctor", "lounge", "YEAR 60 · LOOKS 25")
A("You start avoiding cameras. Every old photo of you is evidence. One picture from the past could expose everything.", "photos", "lounge", "YEAR 50 · LOOKS 25")
# ---------- AKT 3: Einsamkeit ----------
A("So you do the only thing you can. You pack one suitcase, leave in the middle of the night, and start over in a new city with a new name.", "move", "sad", "YEAR 52 · LOOKS 25", cut=True)
A("No goodbyes. No explanations. Your friends just wake up one day, and you're gone.", "burn", "sad", "YEAR 52 · LOOKS 25")
A("And from far away, you watch the people you left behind get old, get sick, and die. And you're not allowed to be there.", "faraway", "sad", "YEAR 70 · LOOKS 25")
A("And you have to do it again every ten or fifteen years. New city. New friends. New life. Again and again.", "moves", "sad", "YEAR 100 · LOOKS 25")
A("After a while, you stop letting people in. What's the point of making friends if you'll have to leave them anyway?", "walls", "sad", "YEAR 110 · LOOKS 25")
A("You learn to fake it. You pretend to be tired. You pretend your back hurts. You even paint on a few wrinkles.", "fake", "sad", "YEAR 115 · LOOKS 25")
A("Every conversation is a test. Where did you grow up? Who are your parents? Why do you remember things nobody your age should know?", "story", "sad", "YEAR 120 · LOOKS 25")
A("And then something even worse shows up. Boredom. You've seen every kind of movie, heard every kind of song, had every kind of argument.", "bored", "space", "YEAR 150 · LOOKS 25")
A("Nothing surprises you anymore. And without surprises, even happiness starts to feel flat.", "flat", "space", "YEAR 160 · LOOKS 25")
A("Your memories start to blur. One day you realize you can't remember the face of your first love anymore. Or your mother's voice.", "forget", "space", "YEAR 180 · LOOKS 25", mood="dark")
A("And hiding gets harder and harder. Cameras everywhere. Face recognition. Digital records of everything.", "scan", "synth", "YEAR 200 · LOOKS 25")
A("You know exactly what would happen if anyone found out. You wouldn't be a celebrity. You'd be a science experiment.", "lab", "synth", "YEAR 200 · LOOKS 25")
A("So you carry the biggest secret in the world, completely alone. There's literally nobody you can tell.", "secret", "synth", "YEAR 220 · LOOKS 25")
# ---------- AKT 4: Ende ----------
A("Decades turn into centuries. Everyone you ever loved is gone. Only you remain.", "gone", "cosmic", "YEAR 500 · LOOKS 25", cut=True)
A("Sure, that little investment has turned into a fortune by now. But there's nobody left to spend it with.", "fortune", "cosmic", "YEAR 500 · LOOKS 25")
A("And you start to envy them. The people who got old. They got a whole story, with a beginning, a middle, and an end.", "envyold", "cosmic", "YEAR 500 · LOOKS 25")
A("In roughly a billion years, scientists expect the Sun to be so bright that Earth becomes too hot for life.", "hotearth", "cosmic", "~1 BILLION YEARS")
A("And in about five billion years, the Sun swells into a red giant.", "redgiant", "cosmic", "~5 BILLION YEARS")
A("And you? You're still twenty-five.", "alone", "cosmic", "AGE 25")
# ---------- OUTRO ----------
A("Maybe getting older isn't a bug. Maybe it's exactly what makes our time so valuable. Every birthday, every goodbye, every moment matters, because it doesn't last forever.", "meaning", "wonder", None, cut=True)
A("So, would you still take the deal? Living forever, but watching everyone you love leave?", "deal", "wonder", None)
A("Tell me in the comments. And if you want more what-if stories like this, subscribe.", "outro", "wonder", None)
P_ = dict(title="YouTube 15: Your Life If You Never Aged (v2)", _sources=SOURCES,
          size=[1920, 1080], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="-4%",
          lead=0.8, gap=0.55, tail=3.0, crf=20, music=dict(style="eras", gain=0.16, duck_ratio=2),
          sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P_, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
