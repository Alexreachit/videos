# Short/TikTok "Why you should never ignore an error email" (Knight Capital, 1 Aug 2012) -> project.json
# Sources (checked 2026-10-29):
# SEC Press Release 2013-222 (16 Oct 2013) "SEC Charges Knight Capital With Violations of Market Access Rule":
#   1 Aug 2012, ~45 minutes after open; one of eight servers did not get the new code (old "Power Peg" code);
#   more than 4 million orders while trying to fill 212 customer orders; 397 million shares; loss of more than $460 million;
#   97 automated emails referencing "Power Peg disabled" sent to Knight staff before the 9:30 a.m. open, not acted on.
# Wikipedia "Knight Capital Group": largest US equities trader (~17.3% NYSE / 16.9% NASDAQ share);
#   stock fell over 70% within two days; ~$400 million rescue investment (Jefferies-led group) on 5-6 Aug 2012.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never ignore an error email. One cost four hundred sixty million dollars.", dict(type="hero"))
A("In twenty twelve, Knight Capital was a giant of US stock trading.", dict(type="tower"))
A("But one of its eight servers missed a software update.", dict(type="servers"))
A("Before the market opened, it sent ninety-seven warning emails. Nobody acted.", dict(type="emails"))
A("Then that server fired four million orders in forty-five minutes.", dict(type="orders", cut=True))
A("Knight's stock crashed over seventy percent, and it needed a rescue.", dict(type="crash"))
A("Would you have read those emails?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never ignore an error email (Knight Capital)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="ttdark", bpm=140, gain=0.22, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.42, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
