"""Schritt: Sounddesign – Geräusche exakt auf die Bild-Ereignisse gelegt.

Jede Szene hat Sound-Cues mit Zeitpunkt (Sekunde innerhalb der Szene). Die Cues
werden in die Gesamt-Zeitleiste umgerechnet (Szenen-Startzeit + t), einzeln
erzeugt (Cache), gemischt und als Stems gespeichert:
  audio/sfx.wav        – Effekte (Schritte, Herzschlag, Growls, Impacts …)
  audio/ambience.wav   – Atmosphäre (Drone je nach Stimmung der Szene)
Der Originalton der Videomodelle (falls vorhanden) kommt im Schnitt dazu.
"""
from __future__ import annotations

import numpy as np
from scipy.io import wavfile

from ..episode import Episode
from ..providers.procedural_audio import DEFAULT_DUR, SR, write_wav
from ..util import log, sha

MOOD_BY_BEAT = {"hook": "panic", "orientation": "dread", "threat": "dread", "escalation": "panic",
                "flight": "panic", "twist": "eerie", "cliffhanger": "eerie"}


def scene_offsets(ep: Episode) -> list[float]:
    offs, t = [], 0.0
    for s in ep.scenes:
        offs.append(round(t, 3))
        t += s.duration
    return offs


def _load(path) -> np.ndarray:
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / 32768.0
    return x.mean(axis=1) if x.ndim > 1 else x


def _place(buf: np.ndarray, x: np.ndarray, at: float, gain_db: float) -> None:
    i = int(at * SR)
    if i >= len(buf):
        return
    n = min(len(x), len(buf) - i)
    fade = min(n, int(0.01 * SR))
    x = x[:n].copy()
    if fade:
        x[-fade:] *= np.linspace(1, 0, fade)
    buf[i:i + n] += x * (10 ** (gain_db / 20))


def run_audio(ep: Episode, prod, sfx_provider) -> dict:
    total = ep.total_duration
    n = int(total * SR) + SR
    sfx = np.zeros(n, np.float32)
    amb = np.zeros(n, np.float32)
    cache = prod.sub("audio/cache")
    timeline = []
    for s, off in zip(ep.scenes, scene_offsets(ep)):
        mood = s.extra.get("ambience", MOOD_BY_BEAT.get(s.beat, "dread"))
        ah = sha(["amb", mood, s.duration, s.id, sfx_provider.name])
        af = cache / f"amb_{ah}.wav"
        if not af.exists():
            sfx_provider.ambience(mood, s.duration + 0.5, af, seed=int(ah[:6], 16))
        _place(amb, _load(af), off, 0.0)
        for k, c in enumerate(s.cues):
            d = c.dur or DEFAULT_DUR.get(c.kind, 1.5)
            d = min(d, s.duration - c.t + 0.8)  # Geräusche dürfen leicht in die nächste Szene klingen
            h = sha([c.kind, round(d, 2), c.note, s.id, k, sfx_provider.name])
            f = cache / f"{c.kind}_{h}.wav"
            if not f.exists():
                sfx_provider.sfx(c.kind, d, f, note=c.note, seed=int(h[:6], 16))
            _place(sfx, _load(f), off + c.t, c.gain_db)
            timeline.append({"t": round(off + c.t, 2), "szene": s.id, "art": c.kind, "dauer": round(d, 2),
                             "gain_db": c.gain_db, "notiz": c.note})
    peak = max(np.abs(sfx).max(), 1e-6)
    if peak > 0.95:
        sfx *= 0.95 / peak
    out = prod.sub("audio")
    write_wav(out / "sfx.wav", sfx[: int(total * SR)], peak=min(0.95, float(np.abs(sfx).max()) or 0.5))
    write_wav(out / "ambience.wav", amb[: int(total * SR)], peak=0.6)
    log.info("Sounddesign: %d Cues auf %.1fs Zeitleiste", len(timeline), total)
    return {"cues": len(timeline), "timeline": timeline}
