# YouTube 19 (lang, 16:9): "6 Lost Treasures Worth Billions (One Was Almost Melted for Scrap)"
# Stil wie yt_heists18 (Referenz R-mWVMM-LAs): gl3d-Toon-3D-Welt + 2D-Rundkopf-Figuren, Countdown #6 -> #1, Hook = #1 (San Jose) ab Sekunde 0.
# Echte Personen nur als generische Figuren (keine Portraets), Fenn/Stuef/Haendler ohne Gesichtsaehnlichkeit.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SOURCES = """Sources (checked 2026-11-25):
- San Jose: CBS News 21 Nov 2025 "Colombia recovers first treasures from San Jose shipwreck" (1708, attacked by an English fleet, sank with most of its crew,
  believed 11 million gold and silver coins + emeralds, located 2015, almost 2,000 feet deep, site is a state secret, a cannon, three coins and a porcelain cup
  among the first objects recovered; claimants Colombia, Spain, Qhara Qhara Bolivians; arbitration with US investors Sea Search Armada claiming $10 billion);
  IFLScience 9 Dec 2025 ($17 billion "commonly cited", some think overinflated, 600 m, Wager's expedition, cause of sinking never categorically proven);
  Discover Magazine 2024 (June 8 1708 near Isla de Baru, ~1 hour of fighting, 11 of ~600 aboard survived, estimated $20 billion, many claimants);
  The Art Newspaper 25 May 2026 (controversy continues).
- Amber Room: Smithsonian Magazine "A Brief History of the Amber Room" (begun 1701 in Prussia, 1716 gift to Peter the Great, Catherine Palace 1755,
  six tons of amber, "Eighth Wonder of the World", ~$142 million today, Nazis dismantled it within 36 hours in 1941, 27 crates to Koenigsberg,
  trail lost after 1944 bombing; replica completed 2003, 25 years, $11 million); History.com "The Amber Room mystery" (last seen 12 Jan 1945,
  theories: destroyed in bombing, hidden, sunk; 2020 Karlsruhe wreck held no Amber Room panels).
- Third Imperial Faberge Egg: PBS NewsHour 20 Mar 2014, JCK 20 Mar 2014, Irish Times 19 Mar 2014 (1887 gift from Alexander III to Maria Feodorovna,
  Vacheron Constantin watch inside, seized after 1917, recorded in Moscow 1922 and sold, 1964 Parke-Bernet New York ~$1,500 as a "gold watch",
  US Midwest scrap metal dealer paid ~$14,000 meaning to melt it for its gold, no buyer, googled "egg" + "Vacheron Constantin", Wartski London confirmed,
  reported value ~$33 million; one of 50 imperial eggs, several still missing).
- Fenn treasure: CBS News photo essay "The hunt for Forrest Fenn's treasure" (2010, 80-year-old art dealer, chest hidden in the Rocky Mountains,
  north of Santa Fe, gold coins, gems, jewelry worth at least $1 million, 24-line poem with nine clues in his memoir "The Thrill of the Chase",
  five men died searching); Good Morning America Dec 2020 (found June 6 2020 in Wyoming by Jack Stuef, 32, Michigan; thousands searched; Fenn died Sept 2020 aged 90);
  NPR 2021 (32-year-old medical student).
- Oak Island: Wikipedia "Oak Island mystery" (1795 discovery story = legend, Daniel McGinnis, depression in the ground; log layers about every ten feet;
  stone said to be found ~90 feet down with markings, one reading "Ten feet below are two million pounds buried", stone later lost;
  pit flooded; FDR part of Old Gold Salvage 1909; six deaths incl. four in 1965 from hydrogen sulfide fumes; Woods Hole 1995: flooding natural;
  treasure never found; The Curse of Oak Island on History since 2014); Canadian Encyclopedia "Oak Island"; History.com "History of Oak Island" (230+ years).
- Nazi gold train: NPR 15 Dec 2015 (Aug 2015 Piotr Koper and Andreas Richter, Walbrzych, deputy culture minister "99 percent convinced" from radar images;
  AGH Krakow team: "There may be a tunnel... But there is no train."); CBS News/AP 24 Aug 2016 (gold rush of hunters; dig found "no train, no tunnel",
  three pits cost 140,000 zlotys / $37,000)."""
L = []
def A(t, shot, ui=None, **k):
    spec = dict(shot=shot); spec.update(k)
    if ui: spec["ui"] = ui
    L.append(dict(text=t, spec=spec))
# ---- Hook: San Jose, stumm verstaendlich ($17 BILLION / AT THE BOTTOM OF THE SEA) ----
A("Two thousand feet below the Caribbean Sea lies a ship packed with gold, silver and emeralds. Some say it's worth seventeen billion dollars.", "s_hook", "hook")
A("It was found more than ten years ago. And yet, almost all of it is still down there.", "s_hook2", "still")
A("That's number one on this list. But first, five other lost treasures that people have hunted for years.", "count_wall", "list")
A("Some were never found. One was found by accident. And one almost got melted down for scrap.", "count_wall2", "teaser")
# ---- #6 Nazi gold train ----
A("Number six. Poland, August 2015.", "n_hills", "n6", cut=True, mood="tense")
A("For decades, a legend has gone around these mountains. In 1945, a Nazi train loaded with gold rolled into a tunnel, and was never seen again.", "n_legend", "legend")
A("Then two treasure hunters went public. They said they'd found it, buried in a hidden tunnel.", "n_hunters", "found")
A("They showed a ground radar image. And a government official said he was ninety-nine percent sure the train was real.", "n_radar", "pct99")
A("The news went around the world. Treasure hunters poured into the town.", "n_rush", "rush")
A("But then, scientists from Krakow scanned the hill. Their verdict: there may be a tunnel, but there is no train.", "n_scan", "notrain")
A("The two men dug anyway, with excavators, in the summer of 2016.", "n_dig", "dig")
A("They found no train. Not even a tunnel. Just three holes in the ground, that cost them about thirty-seven thousand dollars.", "n_holes", "usd37")
# ---- #5 Oak Island ----
A("Number five. Oak Island, Canada.", "o_island", "n5", cut=True, mood="calm")
A("The story goes that in 1795, a teenager named Daniel McGinnis found a strange dip in the ground, right next to an old oak tree.", "o_dip", "y1795")
A("He and his friends started digging. And every ten feet or so, they hit a layer of logs. As if someone had built this pit on purpose.", "o_logs", "logs")
A("Later diggers claimed they found a stone with strange markings. One reading said: ten feet below, two million pounds are buried.", "o_stone", "stone")
A("But every time they got close, the pit flooded with water.", "o_flood", "flood")
A("For more than two hundred years, people kept trying. Even a young Franklin D. Roosevelt invested in the hunt, long before he became president.", "o_fdr", "fdr")
A("Six people have died in the search. Four of them in 1965, from poisonous gas in a shaft.", "o_deaths", "deaths6")
A("Scientists now think the flooding is natural. And the stone? It's lost.", "o_science", "natural")
A("To this day, no treasure has ever been found. But there's still a TV show about the search, running since 2014.", "o_tv", "tv")
# ---- #4 Fenn treasure ----
A("Number four. Santa Fe, New Mexico, 2010.", "f_town", "n4", cut=True, mood="bright")
A("An eighty-year-old art dealer named Forrest Fenn fills a small chest with gold coins, gems and jewelry. Worth at least one million dollars.", "f_chest", "usd1m")
A("Then he hides it somewhere in the Rocky Mountains.", "f_hide", "hide")
A("The only clue: a twenty-four-line poem in his book, with nine hints.", "f_poem", "poem")
A("Thousands of people went looking. They climbed, they dug, they waded through rivers.", "f_search", "search")
A("And it got dangerous. At least five people died while searching.", "f_danger", "dead5")
A("Then, after ten years, in June 2020, a thirty-two-year-old medical student named Jack Stuef found it.", "f_found", "found2020")
A("Where? In Wyoming. Fenn confirmed it. And just a few months later, he died at the age of ninety.", "f_wyoming", "wyoming")
# ---- #3 Faberge egg ----
A("Number three. Russia, Easter 1887.", "e_palace", "n3", cut=True, mood="calm")
A("Tsar Alexander the Third gives his wife a golden egg made by Faberge. Inside is a tiny watch.", "e_gift", "gift")
A("Then came the revolution. The new Soviet government seized the royal treasures, and sold many of them abroad.", "e_revolution", "seized")
A("The egg disappeared. For decades, nobody knew where it was.", "e_lost", "photo")
A("Then, decades later, a scrap metal dealer in the American Midwest spots a gold egg at an antiques market.", "e_market", "market")
A("He pays about fourteen thousand dollars. His plan: melt it down and sell the gold.", "e_melt", "usd14k")
A("But no one would pay more than he had paid. So he typed the name on the watch into Google.", "e_google", "google")
A("He found an article about a lost Faberge egg. It looked exactly like his.", "e_article", "article")
A("Experts in London confirmed it. It was the Third Imperial Egg, reportedly worth around thirty-three million dollars.", "e_value", "usd33m")
A("He almost melted it. And there are still a few imperial eggs that nobody can find.", "e_missing", "missingeggs")
# ---- #2 Amber Room ----
A("Number two. A palace near Saint Petersburg, 1941.", "a_palace", "n2", cut=True, mood="tense")
A("Inside is a room covered in six tons of amber, with gold and mirrors. People called it the eighth wonder of the world.", "a_room", "tons6")
A("It was a gift from the king of Prussia to Peter the Great.", "a_gift", "prussia")
A("Then, the German army invades. In just thirty-six hours, soldiers take the room apart.", "a_tear", "h36")
A("They pack it into twenty-seven crates, and ship it to a castle in Konigsberg.", "a_crates", "crates27")
A("Then the city gets bombed. The castle is left in ruins. And the trail goes cold.", "a_bomb", "bombed")
A("Was it destroyed? Hidden somewhere? Sunk at the bottom of the Baltic Sea? Nobody knows.", "a_theories", "theories")
A("Divers even searched a sunken German ship. No amber.", "a_divers", "noamber")
A("Russia spent twenty-five years and eleven million dollars building a copy. But the original has never been found.", "a_copy", "copy")
# ---- #1 San Jose ----
A("And number one. The Caribbean Sea, June 1708.", "s_sea", "n1", cut=True, mood="tense")
A("A Spanish galleon called the San Jose is sailing toward Cartagena, carrying gold, silver and emeralds from the Americas.", "s_sail", "cargo")
A("Then, British warships attack.", "s_attack", "attack")
A("After about an hour of fighting, the San Jose goes down. Of around six hundred people on board, only about eleven survive.", "s_sink", "survive")
A("For three hundred years, the wreck is lost.", "s_lost", "yrs300")
A("Then, in 2015, Colombia announces it has found it. Almost two thousand feet deep.", "s_found", "found2015")
A("Cannons. Jars. Piles of coins. Some estimate up to eleven million gold and silver coins.", "s_coins", "coins11m")
A("But who owns it? Colombia says it's theirs. Spain claims it too. American investors want ten billion dollars. And Indigenous people in Bolivia say the treasure was taken from their ancestors.", "s_owners", "owners")
A("In 2025, Colombian scientists brought up the first objects. A cannon, a porcelain cup, and three coins.", "s_raise", "first3")
A("The rest is still at the bottom of the sea. And the exact spot is a state secret.", "s_secret", "secret", mood="calm")
# ---- Outro ----
A("So, which treasure would you go looking for? Tell me in the comments. And subscribe to Roundhead Stories for more true money stories.", "outro", "end", mood="bright")
P = dict(title="YouTube 19: 6 Lost Treasures Worth Billions (One Was Almost Melted for Scrap)", _sources=SOURCES, size=[1920, 1080], fps=30,
         scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+4%", lead=0.3, gap=0.42, tail=3.0, crf=21,
         music=dict(style="suspense", bpm=96, gain=0.13, duck_ratio=2), sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
