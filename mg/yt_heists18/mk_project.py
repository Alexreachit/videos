# YouTube 18 (lang, 16:9): "6 Heists So Bold They Look Fake (One Is Still Unsolved)"
# Stil: neue Referenz R-mWVMM-LAs -> gl3d-Toon-3D-Welt + 2D-Rundkopf-Figuren (samrig/MG_SAM wie ys_bridge), Story mit Figuren in Aktion,
# viele Einstellungen; Countdown #6 -> #1, Hook = #1 (Gardner, leere Rahmen) ab Sekunde 0.
# Echte Personen nur als gesichtslose/generische Figuren (keine Portraets).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SOURCES = """Sources (checked 2026-11-19):
- Guinness World Records news 19 Mar 2026 "Missing: Have you seen this painting? The greatest art robbery remains unsolved": 18 Mar 1990,
  two men dressed as police buzzed in, two guards tied up and taken to the basement, ~80 minutes (motion-sensor logs), 13 works incl. Vermeer
  "The Concert" and Rembrandt "Storm on the Sea of Galilee", valued ~$500 million, reward $10,000,000, Dutch Room frames hang empty, never seen again.
- A&E "The Unsolved Heist at Isabella Stewart Gardner Museum" (2025/2026): early hours 18 Mar 1990, fake officers claimed a disturbance, guard let
  them in against policy, guards duct-taped/handcuffed in basement, left 2:45 a.m., 13 works, $10M reward, empty frames still hang,
  FBI 2015 named two suspects (both dead), nothing recovered.
- Wikipedia "Antwerp diamond heist": 15-16 Feb 2003, Leonardo Notarbartolo rented an office in the Antwerp Diamond Center (>2 years prep),
  vault: combination lock, infrared heat detectors, seismic sensor, Doppler radar, magnetic field; hairspray on thermal sensor, polystyrene
  shield, tape on light sensor; 109 of 189 boxes; >$100 million; trash dumped near E19 motorway, found by landowner next morning;
  DNA from a partially eaten salami sandwich; Notarbartolo 10 years; most diamonds never recovered.
- Wikipedia "Vincenzo Peruggia": 21 Aug 1911 (Monday, closed day), former Louvre worker, white smock, lifted it off the wall, removed frame,
  a plumber let him out; discovered next day; Picasso questioned/Apollinaire arrested; hid it in a trunk in his apartment for two years;
  12 Dec 1913 arrested in Florence after offering it to dealer Alfredo Geri (Uffizi director Poggi verified); served about seven months;
  crowds came to stare at the empty space on the wall.
- Smithsonian Magazine "The Theft That Made the 'Mona Lisa' a Masterpiece" (title -> "many say the theft made it famous").
- Louvre 2025: ABC News timeline 21 Oct 2025 (about 7 minutes, truck with ladder) - see mg/ys_louvre.
- Wikipedia "Hatton Garden safe deposit burglary": Easter weekend April 2015, down a lift shaft, Hilti drill through 50 cm vault wall,
  alarm went off 3 Apr 00:21 but police did not respond; up to GBP 14 million; six elderly men, ringleader Brian Reader 76 at arrest;
  caught via cars/CCTV, Flying Squad; sentences ~6-7 years; only GBP 4.3m recovered.
- Wikipedia "Dresden Green Vault burglary": 25 Nov 2019 ~4 a.m. fire at a power box on Augustus Bridge cut street lights; window bars cut;
  display case smashed with an axe; 21 pieces with >4,300 diamonds; at least EUR 113 million; Audi later found burned in an underground car park;
  Dec 2022 31 items returned (Berlin), 16 May 2023 five members of the Remmo clan convicted; some pieces still missing (artnet 2023).
- Wikipedia "Great Train Robbery (1963)" + "Ronnie Biggs": 8 Aug 1963 just after 3 a.m., Royal Mail train, glove over the green light +
  battery for the red light, 15 men, driver Jack Mills hit over the head, GBP 2.6 million (~GBP 48-50 million today), Leatherslade Farm,
  Monopoly with real money + fingerprints, sentences up to 30 years; Biggs escaped Wandsworth 1965 by rope ladder, ~36 years a fugitive,
  returned 2001; bulk of the money never recovered."""
L = []
def A(t, shot, ui=None, **k):
    spec = dict(shot=shot); spec.update(k)
    if ui: spec["ui"] = ui
    L.append(dict(text=t, spec=spec))
# ---- Hook (Gardner-Teaser, stumm verstaendlich: leere Rahmen + "$500 MILLION - STILL MISSING") ----
A("Two police officers rang the bell of a museum in Boston, in the middle of the night. Eighty minutes later, half a billion dollars of art was gone.", "g_hook_door", "hook500")
A("Thirteen works, including a Rembrandt and a Vermeer. And to this day, not a single one has been found.", "g_hook_frames", "missing")
A("That's number one on this list. But first, five other heists so bold they almost look fake.", "count_wall", "list")
A("And watch closely. Because almost every one of these crews made one tiny mistake.", "magnifier", "mistake")
# ---- #6 Great Train Robbery ----
A("Number six. England, August 8th, 1963. Just after three in the morning, a Royal Mail train is rolling through the dark.", "t_train_night", "n6", cut=True, mood="tense")
A("It's carrying sacks of used banknotes. Millions of them.", "t_sacks", "sacks")
A("Up ahead, a signal turns red. So the driver stops the train.", "t_signal", "red")
A("But the signal was a trick. The gang had covered the green light with a glove, and powered the red light with a battery.", "t_glove", "glove")
A("Fifteen men stormed the train. The driver, Jack Mills, was hit over the head.", "t_storm", "fifteen")
A("They unloaded more than two-and-a-half million pounds. Today, that's close to fifty million.", "t_unload", "gbp26")
A("Then they hid at a farmhouse. And while they waited, they played Monopoly. With the real money.", "t_monopoly", "monopoly")
A("That was the mistake. Police found the farm, and fingerprints all over the game.", "t_prints", "prints")
A("The leaders got thirty years in prison. One of them, Ronnie Biggs, escaped over the wall on a rope ladder, and stayed on the run for about thirty-six years.", "t_biggs", "yrs30")
A("And most of the money was never found.", "t_empty", "notfound")
# ---- #5 Mona Lisa ----
A("Number five. Paris, August 21st, 1911. It's a Monday, and the Louvre is closed.", "m_louvre", "n5", cut=True, mood="calm")
A("A man in a white worker's smock walks in through the staff entrance. Nobody looks twice. He used to work here.", "m_smock", "smock")
A("His name is Vincenzo Peruggia. He walks up to the Mona Lisa, lifts it off the wall, and takes it out of its frame.", "m_lift", "lift")
A("At a locked door, a plumber even lets him out, thinking he's staff.", "m_plumber", "plumber")
A("Nobody notices the painting is gone until the next day.", "m_empty_wall", "nextday")
A("Police even question Pablo Picasso. And crowds come to the Louvre just to stare at the empty space on the wall.", "m_crowd", "crowd")
A("For two years, the Mona Lisa sits in a trunk in Peruggia's apartment.", "m_trunk", "yrs2")
A("Then he takes it to Florence and offers it to an art dealer. The dealer calls in the museum director, and police arrest Peruggia at his hotel.", "m_florence", "arrest")
A("He served only about seven months. And many say the theft is what made the Mona Lisa the most famous painting in the world.", "m_famous", "famous")
A("And the Louvre? In 2025, thieves robbed it again. With a ladder truck, in about seven minutes.", "m_louvre2025", "l2025")
# ---- #4 Hatton Garden ----
A("Number four. London, Easter weekend, 2015.", "h_street", "n4", cut=True, mood="tense")
A("Hatton Garden is London's jewelry district. And under one building sits a vault full of safe deposit boxes.", "h_vault", "vault")
A("The thieves climb down an elevator shaft. Then they use an industrial drill to bore through a vault wall half a meter thick.", "h_drill", "wall50")
A("The alarm goes off. But no police come.", "h_alarm", "alarm")
A("They walk out with loot worth up to fourteen million pounds.", "h_loot", "gbp14")
A("And the gang? Mostly pensioners. Their ringleader was seventy-six years old.", "h_grandpas", "age76")
A("Their mistake: they used their own cars. Cameras picked them up, and the police tracked them for weeks.", "h_cars", "cars")
A("Most of them got six to seven years. And millions of pounds' worth of the loot is still missing.", "h_prison", "missing4")
# ---- #3 Dresden ----
A("Number three. Dresden, Germany, November 25th, 2019. Around four in the morning.", "d_city", "n3", cut=True)
A("A fire breaks out in a power box on a bridge. The streetlights go dark.", "d_fire", "dark")
A("Two men cut through the iron bars of a window and climb into the Green Vault, a royal treasure chamber from the 1700s.", "d_window", "window")
A("They smash a display case with an axe.", "d_axe", "axe")
A("And grab jewelry set with more than four thousand diamonds. Worth more than one hundred and thirteen million euros.", "d_jewels", "eur113")
A("Their getaway car was later found burned in an underground garage.", "d_car", "burned")
A("But police tracked down the gang, members of a Berlin crime family.", "d_police", "clan")
A("In 2022, most of the jewels came back as part of a deal. And in 2023, five men were convicted.", "d_return", "back")
A("But some pieces are still missing today.", "d_missing", "missing3")
# ---- #2 Antwerp ----
A("Number two. Antwerp, Belgium. The diamond capital of the world. February 2003.", "a_city", "n2", cut=True, mood="tense")
A("A man named Leonardo Notarbartolo rents an office in the Antwerp Diamond Center. For over two years, he plays the part of a diamond trader.", "a_office", "yrs2b")
A("Below the building sits a vault with a combination lock, heat sensors, a seismic sensor, radar, and a magnetic field.", "a_vault", "layers")
A("His crew beat them one by one. Hairspray on the heat sensor. A foam shield in front of the infrared. Tape over the light sensor.", "a_beat", "beat")
A("Over one weekend, they opened one hundred and nine of one hundred and eighty-nine safe deposit boxes.", "a_boxes", "boxes109")
A("The haul was worth more than one hundred million dollars. People called it the heist of the century.", "a_haul", "usd100")
A("Then, on the way out, they dumped their trash in a forest next to the highway.", "a_forest", "trash")
A("The landowner found it the next morning. Inside was a half-eaten salami sandwich.", "a_sandwich", "sandwich")
A("The DNA on it helped convict the gang. Notarbartolo got ten years.", "a_dna", "dna10")
A("But most of the diamonds were never found.", "a_never", "never2")
# ---- #1 Gardner ----
A("And number one. Boston, March 18th, 1990. The early hours of the morning.", "g_street", "n1", cut=True, mood="tense")
A("Two men in police uniforms ring the bell at the Isabella Stewart Gardner Museum. They say they're responding to a disturbance.", "g_bell", "uniform")
A("The guard breaks the rules, and lets them in.", "g_letin", "rules")
A("Minutes later, both guards are tied up in the basement.", "g_basement", "tied")
A("For about eighty minutes, the thieves walk through the museum.", "g_walk", "min80")
A("They take thirteen works. Rembrandt's Storm on the Sea of Galilee. Vermeer's The Concert.", "g_take", "works13")
A("Together, worth around five hundred million dollars. The biggest art theft in history.", "g_value", "usd500")
A("The museum offers a reward of ten million dollars. It has never been paid.", "g_reward", "reward10")
A("The FBI later named two suspects. Both are dead.", "g_fbi", "fbi")
A("And today, the empty frames still hang on the wall. Waiting for the paintings to come home.", "g_frames_end", "frames", mood="calm")
# ---- Outro ----
A("So, which heist was the boldest? Tell me in the comments. And subscribe to Roundhead Stories for more true money stories.", "outro", "end", mood="bright")
P = dict(title="YouTube 18: 6 Heists So Bold They Look Fake (One Is Still Unsolved)", _sources=SOURCES, size=[1920, 1080], fps=30,
         scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+4%", lead=0.3, gap=0.42, tail=3.0, crf=21,
         music=dict(style="suspense", bpm=96, gain=0.13, duck_ratio=2), sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
