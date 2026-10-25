# Erzeugt deutsche Hörproben verschiedener Edge-Stimmen (gleicher Text) -> output/voices/*.mp3
import asyncio, edge_tts, os
TEXT = ("Haus kaufen oder in einen ETF investieren? Nach dreißig Jahren hat einer von beiden "
        "über siebenhunderttausend Euro mehr. Und das Ergebnis wird dich überraschen.")
VOICES = ["de-DE-ConradNeural", "de-DE-KillianNeural", "de-DE-FlorianMultilingualNeural",
          "en-US-AndrewMultilingualNeural", "de-AT-JonasNeural", "de-CH-JanNeural",
          "de-DE-SeraphinaMultilingualNeural", "de-DE-KatjaNeural", "de-DE-AmalaNeural"]
async def main():
    os.makedirs("output/voices", exist_ok=True)
    for v in VOICES:
        try:
            await edge_tts.Communicate(TEXT, v, rate="+10%").save(f"output/voices/{v}.mp3")
            print("ok", v)
        except Exception as e:
            print("FAIL", v, e)
asyncio.run(main())
