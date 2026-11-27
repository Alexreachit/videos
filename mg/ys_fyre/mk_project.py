# Short "Fyre Festival" (Bahamas, April 2017) -> project.json
# Stil: 3D-Toon-Welt (gl3d) + 2D-Rundkopf-Figuren (samrig) wie ys_brinks/ys_brinksmat (Referenz R-mWVMM-LAs).
# Sources (checked 2026-11-27):
# Wikipedia "Fyre Festival" (en.wikipedia.org/wiki/Fyre_Festival): dates April 28-30 / May 5-7 2017 (cancelled), Exuma, The Bahamas;
#   promoted by posts from Kendall Jenner, Bella Hadid, Hailey Baldwin, Emily Ratajkowski and other models/influencers;
#   advertised "gourmet meals and luxury villas"; day tickets $500-$1,500, VIP packages "including airfare and luxury tent
#   accommodation for $12,000"; guests found "scattered disaster relief tents with dirt floors", some mattresses "soaking wet";
#   "cheese sandwiches served in foam containers"; "In the early morning, it was announced that the festival would be postponed,
#   and the attendees would be returned to Miami"; March 2018 McFarland pleaded guilty to wire fraud; October 2018 sentenced to
#   six years in prison (and ordered to forfeit $26 million).
# CBS News Philadelphia "Fyre Festival: When A $12,000 Luxury Festival In Paradise Turns Into Chaos" (2017).
# VICE News 2017: attendees "stranded on an island in disaster relief tents".
# NBC News / NPR (Oct 11, 2018): Fyre Festival organizer Billy McFarland sentenced to 6 years on fraud charges.
# Not used: exact number of guests, likes/followers, investor totals.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never buy a festival ticket from an Instagram ad.", dict(shot="hero"))
A("In 2017, famous models promoted Fyre Festival, a luxury party in the Bahamas.", dict(shot="phone"))
A("It promised luxury villas and gourmet meals.", dict(shot="promise"))
A("VIP packages with flights cost twelve thousand dollars.", dict(shot="price"))
A("But when the guests arrived, they found disaster-relief tents and soaking-wet mattresses.", dict(shot="tents"))
A("And dinner was a cheese sandwich in a foam box!", dict(shot="sandwich", cut=True))
A("By the next morning, the festival was called off, and guests were sent back to Miami.", dict(shot="airport"))
A("Its founder pleaded guilty to fraud and got six years in prison.", dict(shot="prison"))
A("Would you have bought a ticket?", dict(shot="end", choice=True))
P = dict(title="Short: Fyre Festival 2017 (3D+2D style)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.1, tail=0.4, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.5, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
