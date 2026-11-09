"""Kostenpflichtig: ElevenLabs Sound Effects API (Text -> Geräusch).

Doku: https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
Für kommerzielle Nutzung ist mindestens der Starter-Plan nötig. Schlüssel: ELEVENLABS_API_KEY.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from ..cost import sfx_cost
from ..util import TransientError, retry, run
from .base import AudioProvider
from .procedural_audio import ProceduralSfx

DESCRIPTIONS = {
    "heartbeat": "close, muffled human heartbeat, fast, tense, cinematic",
    "breath": "panicked heavy human breathing close to the microphone, first person",
    "footsteps": "running footsteps on wet concrete, first person, close",
    "growl": "raspy wet zombie growl, close, horror film",
    "impact": "heavy body slamming against a metal door, horror impact",
    "click": "flashlight button click",
    "door": "heavy steel stairwell door creaking open",
    "drone": "low dark horror ambience drone",
    "stinger": "cinematic horror stinger hit with reverb tail",
    "metal": "metal shopping cart rolling and crashing on concrete",
    "scream": "distant human scream echoing in a concrete garage",
    "glass": "car window glass cracking under impact",
}


@retry(times=3)
def _post(body: dict, out: Path) -> None:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY fehlt")
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation", method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            out.write_bytes(r.read())
    except urllib.error.HTTPError as e:
        if e.code in (429, 500, 503):
            raise TransientError(f"HTTP {e.code}") from e
        raise RuntimeError(f"ElevenLabs HTTP {e.code}: {e.read().decode(errors='ignore')[:300]}") from e


class ElevenLabsSfx(AudioProvider):
    name = "elevenlabs"
    paid = True

    def sfx(self, kind, duration, out: Path, note="", seed=0):
        duration = max(0.5, min(30.0, duration))
        usd = sfx_cost(self.ctx.cfg, duration)
        what = f"SFX {kind} {duration:.1f}s"
        self.ctx.guard.charge(usd, what)
        mp3 = out.with_suffix(".mp3")
        try:
            _post({"text": f"{DESCRIPTIONS.get(kind, kind)}. {note}".strip(), "duration_seconds": duration,
                   "prompt_influence": 0.5}, mp3)
        finally:
            self.ctx.guard.commit(usd, what)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "48000", out])
        return {"provider": "elevenlabs", "usd": usd}

    def ambience(self, mood, duration, out, seed=0):
        # Ambience lokal (kostenlos) – lange Flächen über die API wären teurer und schlechter loopbar.
        return ProceduralSfx(self.ctx).ambience(mood, duration, out, seed)
