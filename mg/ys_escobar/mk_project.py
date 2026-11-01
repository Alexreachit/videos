# Short/TikTok "Why you should never hide your cash in the walls" (Pablo Escobar's cartel cash) -> project.json
# Sources (checked 2026-11-01):
# Business Insider (via AP), "Legendary drug lord Pablo Escobar lost $2.1 billion in cash each year": Roberto Escobar (Pablo's brother,
#   the cartel's chief accountant) wrote in "The Accountant's Story" that they wrote off 10% of the money each year due to rodents,
#   water damage or loss; estimated ~$2.1 billion per year; cash stashed in farm fields, dilapidated warehouses and inside walls of
#   cartel members' homes; ~$2,500 a month spent on rubber bands.
# Britannica "Pablo Escobar: 8 interesting facts": cartel reportedly took in an estimated $420 million a week at its peak;
#   much of the cash kept in warehouses and fields; ~10% ($2.1bn) lost each year per his brother (rats, elements, lost).
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never hide your cash in the walls.", dict(type="hero"))
A("Pablo Escobar's cartel had so much cash, it hid it inside walls and fields.", dict(type="hide"))
A("They spent about twenty-five hundred dollars a month just on rubber bands.", dict(type="bands"))
A("His brother said rats, water and losses wiped out ten percent a year.", dict(type="rats"))
A("An estimated two point one billion dollars a year.", dict(type="loss", cut=True))
A("WAIT!!! FOLLOW for more stories like this!!!", dict(type="samyell"), rate="+22%", volume="+50%",
  afx="acompressor=threshold=-22dB:ratio=4:attack=4:release=80:makeup=4,volume=3dB")
A("Anyway. They just wrote it off.", dict(type="writeoff"))
A("Where would you hide a billion dollars?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never hide your cash in the walls (Escobar's rats)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
