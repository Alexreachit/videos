# YouTube 20 (lang, 16:9): "6 People Who Found a Fortune by Accident"
# Stil wie yt_treasure19/yt_heists18: gl3d-Toon-3D-Welt + 2D-Rundkopf-Figuren, Countdown #6 -> #1, Hook = #1 (Cimabue in der Kueche) ab Sekunde 0.
# Echte Personen nur als generische Figuren (keine Portraets).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SOURCES = """Sources (checked 2026-11-27):
- Cimabue "The Mocking of Christ": Wikipedia "The Mocking of Christ (Cimabue)" (house near Compiegne, 2019, hung above the hotplate, owner in her nineties,
  thought it an old religious icon of little value, 25.8 x 20.3 cm, c. 1280, auctioneer Philomene Wolf noticed it, Eric Turquin attributed it, sold 27 Oct 2019 at
  Acteon Senlis, EUR 24 million with fees, export ban, acquired by the Louvre Nov 2023); Irish Times 27 Oct 2019 ("hung for decades above a cooking hotplate",
  "simply an old icon from Russia", 26 x 20 cm, over EUR 24 million); The Art Newspaper 6 Nov 2023 (Louvre, EUR 24.1m).
- Caravaggio "Judith Beheading Holofernes" (Toulouse): The Art Newspaper 1 Mar 2019 timeline (April 2014 auctioneer Marc Labarbe called to a house in Toulouse,
  Eric Turquin, national treasure, 30-month export ban); artnet News June 2019 ("dark, cluttered, leaky attic", estimate EUR 100-150 million, auction 27 June 2019
  cancelled at the eleventh hour, sold privately, buyer and price confidential, some experts doubt the attribution); Wikipedia (undisclosed amount).
- Hoxne Hoard: Wikipedia "Hoxne Hoard" (16 Nov 1992, farmer Peter Whatling lost a hammer, friend Eric Lawes with metal detector, notified police without digging
  further, archaeologists excavated next day, 14,865 Roman coins: 569 gold, 14,272 silver, 24 bronze, ~200 items of tableware and jewellery, buried after AD 407,
  valued GBP 1.75 million paid to Lawes and shared with Whatling, hammer also recovered and given to the British Museum); Smithsonian Magazine 2017.
- Saddle Ridge Hoard: Wikipedia "Saddle Ridge Hoard" (Feb 2013, couple "John and Mary" walking their dog on their property in Northern California, rusty can
  poking out of the ground, 8 cans, 1,427 gold coins dated 1847-1894, face value $27,980, hid them in an old cooler under a woodpile, Mint-theft theory ruled out);
  NPR 26 Feb 2014 (Sierra Nevada property, Kagin's: about $10 million).
- Declaration of Independence (Adamstown): Snopes; Philadelphia Inquirer (1991, reprint 2009: bought a painting for $4 because he liked the frame, folded document
  between painting and backing); History.com (1989, Adamstown, Pennsylvania, printed by John Dunlap); Christian Science Monitor 3 Jul 2000 (sold 1991 for $2.42 million,
  2000 for about $8.1 million to TV producer Norman Lear and a partner).
- "Tenner" diamond: Sotheby's editorial (late 1980s, car boot sale in Isleworth, West London, haggled from GBP 12 to GBP 10, thought it was costume jewellery,
  wore it regularly, appraised in 2017, cushion-cut 26.27 carats, 19th century); ITV News 7 Jun 2017 (estimate GBP 250,000-350,000, sold at Sotheby's London for GBP 656,750)."""
L = []
def A(t, shot, ui=None, **k):
    spec = dict(shot=shot); spec.update(k)
    if ui: spec["ui"] = ui
    L.append(dict(text=t, spec=spec))
# ---- Hook: Cimabue in der Kueche (stumm verstaendlich: "€24 MILLION / IN HER KITCHEN") ----
A("For decades, this tiny painting hung above a hot plate in an old woman's kitchen. She thought it was worthless.", "h_kitchen", "hook")
A("Then someone took a closer look. A few months later, it sold for twenty-four million euros.", "h_sold", "sold")
A("That's number one on this list. But first, five other people who found a fortune completely by accident.", "list", "list")
A("A ring from a car boot sale. A four-dollar painting. A rusty can. A lost hammer. And a leaky attic.", "list2", "teaser")
# ---- #6 Tenner diamond ----
A("Number six. West London, the late 1980s.", "r_boot", "n6", cut=True, mood="calm")
A("A woman is browsing a car boot sale. That's like a flea market, out of the trunks of cars.", "r_browse", "boot")
A("In a box of cheap costume jewelry, she spots a big, sparkly ring. The seller wants twelve pounds. She haggles him down to ten.", "r_haggle", "gbp10")
A("She thinks it's glass. So she just wears it. For about thirty years.", "r_wear", "yrs30")
A("Then, in 2017, she finally asks a jeweler to take a look.", "r_jeweler", "jeweler")
A("It's not glass. It's a real diamond, over twenty-six carats, from the eighteen-hundreds.", "r_real", "ct26")
A("Sotheby's expected up to three hundred and fifty thousand pounds.", "r_estimate", "est")
A("It sold for six hundred and fifty-six thousand pounds. Not bad for a tenner.", "r_sold", "gbp656k")
# ---- #5 Declaration ----
A("Number five. Adamstown, Pennsylvania, 1989.", "d_market", "n5", cut=True, mood="calm")
A("A man at a flea market buys an old painting for four dollars. He doesn't care about the picture. He just wants the frame.", "d_buy", "usd4")
A("At home, he takes it apart. The old frame falls to pieces.", "d_break", "break")
A("And hidden behind the painting, he finds a folded piece of paper.", "d_paper", "paper")
A("It's a copy of the Declaration of Independence. Not a souvenir. One of the very first printings, from July 1776.", "d_decl", "y1776")
A("Only a couple of dozen copies of that printing were known to still exist.", "d_rare", "rare")
A("In 1991, it sold at auction for two point four million dollars.", "d_sold", "usd242")
A("And nine years later, it sold again. This time for more than eight million.", "d_resold", "usd8m")
# ---- #4 Saddle Ridge ----
A("Number four. Northern California, 2013.", "s_hill", "n4", cut=True, mood="bright")
A("A couple is walking their dog on their own land.", "s_walk", "walk")
A("Then, they notice an old rusty can, sticking out of the ground.", "s_can", "can")
A("They dig it out. Inside: gold coins.", "s_open", "gold")
A("They keep digging. In the end, they find eight cans, with fourteen hundred and twenty-seven gold coins.", "s_cans", "coins1427")
A("The coins are from 1847 to 1894, most of them minted in San Francisco. Their face value: about twenty-eight thousand dollars.", "s_dates", "face")
A("But to collectors, they're worth around ten million.", "s_value", "usd10m")
A("Some people guessed they were stolen from the San Francisco Mint in 1901. But the Mint said it found no link.", "s_mint", "mint")
A("At first, the couple hid them in an old cooler, under a pile of firewood.", "s_cooler", "cooler")
A("And who buried them? To this day, nobody knows.", "s_mystery", "mystery")
# ---- #3 Hoxne ----
A("Number three. Suffolk, England, November 1992.", "x_field", "n3", cut=True, mood="calm")
A("A farmer loses his hammer somewhere in a field. So he asks a friend for help.", "x_hammer", "hammer")
A("His friend has a metal detector. He got it as a retirement present.", "x_detector", "detector")
A("The detector beeps. But it's not the hammer. It's coins. Silver coins. Gold coins. Spoons. Jewelry.", "x_beep", "beep")
A("And here's the smart part. He stops digging, and calls the police.", "x_stop", "police")
A("The next day, archaeologists dig out the whole find.", "x_dig", "dig")
A("Almost fifteen thousand Roman coins, plus about two hundred silver and gold objects. Buried around sixteen hundred years ago.", "x_count", "coins15k")
A("It's now in the British Museum. The reward: one point seven five million pounds, shared with the farmer.", "x_reward", "gbp175m")
A("Oh, and the hammer? They found that too. It's in the British Museum as well.", "x_hammer2", "hammer2", mood="bright")
# ---- #2 Caravaggio ----
A("Number two. Toulouse, France, 2014.", "c_house", "n2", cut=True, mood="tense")
A("A family calls a local auctioneer to look at something in their attic. It's dark, cluttered, and the roof is leaking.", "c_attic", "attic")
A("Leaning against a wall is a huge, old painting. A woman is cutting off a man's head.", "c_canvas", "canvas")
A("An expert from Paris studies it, and makes a bold claim. He thinks it was painted by Caravaggio, one of the most famous painters of all time.", "c_expert", "expert")
A("France bans the painting from leaving the country for more than two years, while experts examine it. Estimates go up to one hundred and fifty million euros.", "c_estimate", "eur150m")
A("An auction is set for June 2019. But just days before, it's suddenly called off.", "c_cancel", "cancel")
A("A private collector bought it. The price is a secret. And some experts still doubt it's a real Caravaggio.", "c_secret", "secret")
# ---- #1 Cimabue ----
A("And number one. A small town north of Paris, 2019.", "k_house", "n1", cut=True, mood="calm")
A("A woman in her nineties is selling her house. An auctioneer comes by to value everything inside.", "k_value", "nineties")
A("In the kitchen, above the hot plate, hangs a tiny painting on wood. Smaller than a sheet of paper.", "k_tiny", "tiny")
A("The family thinks it's an old religious icon. Nothing special.", "k_icon", "icon")
A("But the auctioneer recognizes it right away. It looks like early Italian art. Maybe worth three or four hundred thousand euros.", "k_spot", "spot")
A("And the expert who checks it? The same man from the Caravaggio story.", "k_expert", "same")
A("His team scans it with infrared light, and compares it to other works.", "k_scan", "scan")
A("The verdict: it's by Cimabue, a master from around 1280. Only a handful of his paintings still exist.", "k_cimabue", "y1280")
A("In October 2019, about eight hundred people pack into the auction room. The bids keep climbing.", "k_auction", "auction", mood="tense")
A("Twenty-four million euros. For a painting that hung over the stove.", "k_sold", "eur24m")
A("France blocked the buyer from taking it abroad. In 2023, the Louvre bought it.", "k_louvre", "louvre", mood="bright")
A("So maybe go and check what's hanging in your grandma's kitchen.", "k_grandma", "grandma")
# ---- Outro ----
A("Which find would you most like to make? Tell me in the comments. And subscribe to Roundhead Stories for more true money stories.", "outro", "end")
P = dict(title="YouTube 20: 6 People Who Found a Fortune by Accident", _sources=SOURCES, size=[1920, 1080], fps=30,
         scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+4%", lead=0.3, gap=0.42, tail=3.0, crf=21,
         music=dict(style="suspense", bpm=96, gain=0.13, duck_ratio=2), sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
