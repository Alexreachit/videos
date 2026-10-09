#!/usr/bin/env python3
"""Erzeugt kurze Hörproben mit mehreren kostenlosen Stimmen (edge-tts) zum Vergleichen."""
import asyncio
from pathlib import Path

import edge_tts

OUT = Path("output/stimmen")
DE = ("Zwölf Stunden später sitzt du in elf Kilometern Höhe, die Sonne geht auf, und unter dir liegen "
      "die Wolken wie ein riesiger Teppich. Klingt nach dem besten Job der Welt, oder? Aber der Weg "
      "dorthin ist länger, teurer und härter, als die meisten Leute denken.")
EN = ("Twelve hours later you are sitting eleven kilometers up, the sun is rising, and the clouds below "
      "you look like a giant carpet. Sounds like the best job in the world, right? But the road there "
      "is longer, more expensive and tougher than most people think.")
VOICES = [
    ("de", "de-DE-FlorianMultilingualNeural"), ("de", "de-DE-SeraphinaMultilingualNeural"),
    ("de", "de-DE-ConradNeural"), ("de", "de-DE-KillianNeural"), ("de", "de-DE-KatjaNeural"),
    ("de", "de-DE-AmalaNeural"),
    ("en", "en-US-AndrewMultilingualNeural"), ("en", "en-US-BrianMultilingualNeural"),
    ("en", "en-US-AvaMultilingualNeural"), ("en", "en-US-EmmaMultilingualNeural"),
    ("en", "en-US-ChristopherNeural"), ("en", "en-GB-RyanNeural"),
]


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, voice in VOICES:
        try:
            await edge_tts.Communicate(DE if lang == "de" else EN, voice, rate="-4%").save(
                str(OUT / f"{lang}_{voice}.mp3"))
            print("ok", voice)
        except Exception as e:
            print("FEHLER", voice, e)

asyncio.run(main())
