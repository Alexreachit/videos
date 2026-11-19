# Short "He Sold the Brooklyn Bridge" (Brooklyn-Bridge-Betrug) -> project.json
# Erster Test im neuen Animationsstil nach Alex' Referenz R-mWVMM-LAs: 3D-Toon-Welt (gl3d) + 2D-Rundkopf-Figuren (samrig), Story mit Figuren,
# Untertitel 1–2 Woerter.
# Sources (checked 2026-11-19):
# Wikipedia "George C. Parker": con man whose most notable scams involved the Brooklyn Bridge; "producing convincing forged documents"
#   to back his claim he owned it; marks were often "unwary immigrants"; the scam "continued on for several years"; victims tried to
#   recoup their money by establishing a toll, "until the city's police moved in to stop them setting up toll booths upon the bridge"
#   (citing Gabriel Cohen, "For You, Half Price", New York Times, 27 Nov 2005); 17 Dec 1928 mandatory life term at Sing Sing; died there 1937.
# CrimeReads / Dean Jobb (15 Apr 2024, "The Man Who Sold the Brooklyn Bridge"): the seller (real name probably John McCarthy, many aliases
#   incl. Parker) sold the bridge "over and over" (Kilgalen, 1928); pitched "the very fine return" from tolls; real bridge tolls then:
#   10 cents per wagon; one victim, a visitor from Indiana, agreed to "$1,000 cash and $4,000 more" in instalments; life sentence 1928, Sing Sing.
# Brownstoner (28 Jun 2016): several con men sold the bridge; bridge completed 1883.
# Identity of the seller is disputed -> video says only "a con man".
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never buy a bridge from a stranger.", dict(type="hero"))
A("In New York, one con man sold the Brooklyn Bridge. Not once. Over and over again.", dict(type="sold"))
A("He picked people who were new in town.", dict(type="dock"))
A("And showed them forged papers saying he owned the bridge.", dict(type="deed"))
A("His pitch: charge a toll on every wagon, and get rich.", dict(type="toll"))
A("One buyer paid a thousand dollars in cash, and promised four thousand more.", dict(type="cash"))
A("Some buyers even started building toll booths, until the police chased them off.", dict(type="police", cut=True))
A("In 1928, the con man got life in Sing Sing prison.", dict(type="prison"))
A("Would you have bought it?", dict(type="end", choice=True))
P = dict(title="Short: He Sold the Brooklyn Bridge (bridge con, test new 3D+2D style)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.1, tail=0.4, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.5, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
