# Short "Why you should never panic over your bank statement" (PayPal $92 quadrillion error, 2013) -> project.json
# Sources (checked 2026-11-10):
# CNN 17 Jul 2013 "PayPal accidentally credits man $92 quadrillion": Pennsylvania PR executive Chris Reynolds opened his June PayPal
#   e-mail statement, balance $92,233,720,368,547,800; logged in online -> balance $0; would have been "more than a million times richer"
#   than Carlos Slim ($67 billion); PayPal: "This is obviously an error", offered to donate to a cause of his choice; Reynolds: would have
#   "paid down the national debt".
# Christian Science Monitor 17 Jul 2013: Chris Reynolds (56) from Media, Pa.; first thought he OWED $92 quadrillion ("5,411 times the
#   national debt") until friends pointed out it said credit; PayPal apologized and offered a donation to a nonprofit of his choice;
#   maybe buy the Philadelphia Phillies.
# Guinness World Records "Largest accidental banking credit": June 2013, $92,233,720,368,547,800, ~1.2 million times richer than
#   Carlos Slim (world's richest man per Forbes); error rectified moments later.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never panic over your bank statement.", dict(type="hero"))
A("In twenty thirteen, Chris Reynolds opened his PayPal statement.", dict(type="mail"))
A("His balance said ninety-two quadrillion dollars.", dict(type="count", cut=True))
A("That's over a million times richer than the richest man alive.", dict(type="compare"))
A("At first, he thought he owed it.", dict(type="panic"))
A("Then he logged in, and the balance was zero.", dict(type="zero"))
A("PayPal apologized, and offered to donate to a charity of his choice.", dict(type="sorry"))
A("What would you have bought first?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never panic over your bank statement (PayPal $92 quadrillion)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
