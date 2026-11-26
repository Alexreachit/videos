# Short "Brink's-Mat robbery" (Heathrow, 26 Nov 1983) -> project.json
# Stil: 3D-Toon-Welt (gl3d) + 2D-Rundkopf-Figuren (samrig) wie ys_bridge/ys_cooper/ys_brinks (Referenz R-mWVMM-LAs).
# Sources (checked 2026-11-26):
# Wikipedia "Brink's-Mat robbery" (en.wikipedia.org/wiki/Brink%27s-Mat_robbery): 26 November 1983, Unit 7, Heathrow International
#   Trading Estate; six robbers; guard Anthony Black complicit, gave them impressions of the key to the main door + security details;
#   robbers poured petrol over the staff and threatened them with a lit match unless they revealed the vault combinations;
#   robbers expected around GBP 1 million in (Spanish peseta) cash; found three tonnes of gold bullion in 6,800 bars (+ diamonds,
#   traveller's cheques), total GBP 26 million; Black confessed (Dec 1983) and identified his brother-in-law Brian Robinson;
#   Robinson + Micky McAvoy arrested ten days after the robbery, sentenced to 25 years; much of the gold never recovered
#   (about half smelted and recast back into the market); "According to the BBC, some have claimed that anyone wearing gold
#   jewellery bought in the UK after 1983 is probably wearing Brink's-Mat [gold]".
# World History Encyclopedia "The Brink's-Mat Robbery" (worldhistory.org/article/2778): six armed robbers, inside guard Tony Black
#   (brother-in-law in the gang), guards tied up + petrol poured on them, GBP 26 million gold, "vast majority of the stolen gold was
#   never recovered", gold melted down and recast.
# CBC archive (cbc.ca/1.5359437, 1983): "three tons of pure gold", guards threatened with being set on fire; two men 25 years each.
# Not used (sources disagree / unclear): exact time of entry, how long it took, exact amount recovered.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never hire your brother-in-law for a heist.", dict(shot="hero"))
A("In 1983, six robbers raided a warehouse at Heathrow Airport.", dict(shot="airport"))
A("An inside guard had copied the key for them.", dict(shot="key"))
A("They poured petrol on the staff and demanded the vault codes.", dict(shot="petrol"))
A("They came for cash, but found three tonnes of gold. Twenty-six million pounds!", dict(shot="gold", cut=True))
A("Police soon suspected the guard. He named his brother-in-law.", dict(shot="police"))
A("Two got twenty-five years. Most of the gold was never found.", dict(shot="prison"))
A("Some say if you bought gold jewelry in Britain after 1983, you may be wearing it.", dict(shot="jewel"))
A("Would you still wear it?", dict(shot="end", choice=True))
P = dict(title="Short: Brink's-Mat robbery 1983 (3D+2D style)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.1, tail=0.4, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.5, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
