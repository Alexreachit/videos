# Short "He Hijacked a Plane and Vanished" (D. B. Cooper, 1971) -> project.json
# Stil: 3D-Toon-Welt (gl3d) + 2D-Rundkopf-Figuren (samrig) wie ys_bridge (Referenz R-mWVMM-LAs).
# Sources (checked 2026-11-22):
# FBI "A Byte Out of History: D.B. Cooper" (24 Nov 2006, update 12 Jul 2016): Nov 24, 1971, Northwest Orient Flight 305 Portland -> Seattle;
#   man calling himself "Dan Cooper", mid-forties, business suit, black tie, white shirt; handed the stewardess a note saying he had a bomb
#   in his briefcase; attache case with "a mass of wires and red colored sticks"; demanded $200,000 in twenty-dollar bills and four parachutes;
#   in Seattle the 36 passengers were exchanged for the money and parachutes; a little after 8 p.m. he jumped out of the back of the plane
#   with the money; 1980: a young boy found $5,800 in rotting $20 bills matching the ransom serial numbers; fate "remains a mystery";
#   2016: FBI redirected resources away from the case.
# History.com "Hijacker parachutes into thunderstorm" (This Day in History, Nov 24): Northwest Orient 727; 8:13 p.m. over the Lewis River,
#   SW Washington, 10,000 ft, thunderstorm, winds >100 mph; 8-year-old boy found the money on the north bank of the Columbia River (1980);
#   never identified.
# Wikipedia "D. B. Cooper hijacking": rest of the ransom never recovered; hijacker never identified; aft airstair of the 727.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why the FBI never found this man.", dict(type="hero"))
A("In 1971, a quiet man in a suit boarded a flight to Seattle.", dict(type="cabin"))
A("He handed the flight attendant a note. He had a bomb.", dict(type="note"))
A("He wanted two hundred thousand dollars, and four parachutes.", dict(type="demand"))
A("In Seattle, he swapped the passengers for the money.", dict(type="runway"))
A("Then, at night, in a storm, he jumped out of the back of the plane.", dict(type="jump", cut=True))
A("Nine years later, a boy found five thousand eight hundred dollars of it by a river.", dict(type="river"))
A("The rest was never found. And neither was he.", dict(type="gone"))
A("Would you have jumped?", dict(type="end", choice=True))
P = dict(title="Short: D. B. Cooper (hijacker who vanished, 3D+2D style)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.1, tail=0.4, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.5, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
