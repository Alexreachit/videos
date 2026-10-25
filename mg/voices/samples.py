# Runde 2: weitere kostenlose Edge-Stimmen auf Deutsch (gleicher Text) -> output/voices/*.mp3
import asyncio, edge_tts, os
TEXT = ("Haus kaufen oder in einen ETF investieren? Nach dreißig Jahren hat einer von beiden "
        "über siebenhunderttausend Euro mehr. Und das Ergebnis wird dich überraschen.")
async def main():
    os.makedirs("output/voices", exist_ok=True)
    allv = await edge_tts.list_voices()
    names = sorted(v["ShortName"] for v in allv)
    print("DE voices:", [n for n in names if n.startswith("de-")])
    print("Multilingual:", [n for n in names if "Multilingual" in n])
    want = [n for n in names if "Multilingual" in n and n not in (
        "en-US-AndrewMultilingualNeural", "de-DE-FlorianMultilingualNeural", "de-DE-SeraphinaMultilingualNeural")]
    want += ["de-DE-BerndNeural", "de-DE-ChristophNeural", "de-DE-KasperNeural", "de-DE-KlausNeural", "de-DE-RalfNeural"]
    for v in want:
        try:
            await edge_tts.Communicate(TEXT, v, rate="+5%").save(f"output/voices/r2_{v}.mp3"); print("ok", v)
        except Exception as e:
            print("FAIL", v, type(e).__name__)
asyncio.run(main())
