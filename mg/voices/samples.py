# Runde 3: Andrew mit mehr Emotion – Textgestaltung + Tempo/Tonhöhe je Satzteil
import asyncio, edge_tts, os, subprocess
V = "en-US-AndrewMultilingualNeural"
os.makedirs("output/voices", exist_ok=True)
async def say(txt, out, rate="+10%", pitch="+0Hz", volume="+0%"):
    await edge_tts.Communicate(txt, V, rate=rate, pitch=pitch, volume=volume).save(out)
def join(parts, out, gaps):
    # Teile mit kurzen Pausen zusammenfügen
    lst = []
    for i, p in enumerate(parts):
        lst.append(f"file '{os.path.abspath(p)}'")
        if i < len(gaps):
            sil = f"output/voices/_sil{i}.mp3"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(gaps[i]), "-q:a", "9", sil], check=True)
            lst.append(f"file '{os.path.abspath(sil)}'")
    open("output/voices/_list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "output/voices/_list.txt", "-ar", "24000", "-ac", "1", out], check=True)
async def main():
    # A: wie bisher
    await say("Should you buy a house, or invest in an ETF? In thirty years, one of them makes you seven hundred fifty thousand dollars more.", "output/voices/e1_A_bisher.mp3")
    # B: gleicher Inhalt, für Emotion geschrieben (kurze Sätze, Fragen, Ausrufe, Gedankenstriche)
    await say("Buy a house... or invest in an ETF? Thirty years later, one of them is ahead by seven hundred fifty THOUSAND dollars. And it's not the one you think!", "output/voices/e2_B_text.mp3")
    # C: B + Tempo/Tonhöhe je Satzteil (Frage höher+schneller, Zahl langsamer+tiefer, Pointe schneller+höher)
    p = ["output/voices/_c1.mp3", "output/voices/_c2.mp3", "output/voices/_c3.mp3"]
    await say("Buy a house... or invest in an ETF?", p[0], rate="+14%", pitch="+6Hz")
    await say("Thirty years later, one of them is ahead by seven hundred fifty thousand dollars.", p[1], rate="+2%", pitch="-4Hz")
    await say("And it's not the one you think!", p[2], rate="+16%", pitch="+8Hz", volume="+10%")
    join(p, "output/voices/e3_C_text_plus_betonung.mp3", [0.25, 0.35])
    # D: dramatische Stelle aus dem Video (Wendung)
    p = ["output/voices/_d1.mp3", "output/voices/_d2.mp3", "output/voices/_d3.mp3"]
    await say("But here's the catch.", p[0], rate="+0%", pitch="-6Hz")
    await say("That only works at ten percent a year.", p[1], rate="+8%", pitch="+0Hz")
    await say("At eight percent? The house wins!", p[2], rate="+14%", pitch="+8Hz", volume="+10%")
    join(p, "output/voices/e4_D_wendung.mp3", [0.45, 0.3])
asyncio.run(main())
for f in os.listdir("output/voices"):
    if f.startswith("_"): os.remove(os.path.join("output/voices", f))
