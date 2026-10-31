# Short/TikTok "Why you should never keep all your crypto on one exchange" (Binance hack, 29 Oct 2026) -> project.json
# Sources (checked 2026-10-31):
# Al Jazeera 30 Oct 2026 "Binance says $6.3bn stolen in biggest crypto heist in history": ~$6.3bn stolen, ~$3bn frozen,
#   deposits+withdrawals suspended, Binance: user funds safe, will cover all losses; initial investigation: engineer's compromised laptop;
#   bitcoin -~5% below $77,000; TRM: high confidence North Korea's TraderTraitor (linked to Lazarus).
# TRM Labs blog: USD 6.36bn moved out across ten blockchains on Oct 29, 2026, most within ~20 minutes from 20:05 UTC;
#   largest crypto theft on record; Bybit Feb 2025 ~USD 1.5bn -> roughly four times larger; ~USD 2.7bn frozen as of Oct 30 00:30 UTC.
# TechCrunch 29 Oct 2026: withdrawals suspended; "user funds are completely safe".
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = []
def A(t, s, **k): L.append(dict(text=t, spec=s, **k))
A("Why you should never keep all your crypto on one exchange.", dict(type="hero"))
A("On October twenty-ninth, hackers broke into Binance, the world's biggest crypto exchange.", dict(type="breakin"))
A("Early findings point to one engineer's hacked laptop.", dict(type="laptop"))
A("Within about twenty minutes, six point three billion dollars were drained.", dict(type="drain", cut=True))
A("WAIT!!! FOLLOW for more stories like this!!!", dict(type="samyell"), rate="+22%", volume="+50%",
  afx="acompressor=threshold=-22dB:ratio=4:attack=4:release=80:makeup=4,volume=3dB")
A("Anyway. It's the biggest crypto theft ever, about four times the old record.", dict(type="record"))
A("Experts suspect North Korean hackers, and Binance froze all withdrawals.", dict(type="suspect"))
A("Would your crypto be safe?", dict(type="hero", choice=True))
P = dict(title="Short: Why you should never keep all your crypto on one exchange (Binance hack 2026)",
         _sources=open(__file__).read().split("import json")[0].replace("# ", "").strip(),
         size=[1080, 1920], fps=30, scene="scene.html", voice="en-US-AndrewMultilingualNeural", rate="+16%",
         lead=0.05, gap=0.08, tail=0.1, crf=20, music=dict(style="suspense", bpm=140, gain=0.24, duck_ratio=2),
         sfx_vary=True, sfx_gain=0.45, lines=L)
json.dump(P, open("project.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lines", sum(len(l["text"].split()) for l in L), "words")
