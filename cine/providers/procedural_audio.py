"""Kostenlos: lokal synthetisierte Horror-Geräusche (numpy/scipy, keine Lizenzfragen).

Klanglich nicht auf dem Niveau einer professionellen Library, aber exakt
timebar, beliebig oft erzeugbar und rechtlich unproblematisch. Für die
finale Qualität kann pro Geräusch auf ElevenLabs oder eigene CC0-Dateien
(cine/assets/sfx/<art>*.wav) umgestellt werden – eigene Dateien haben Vorrang.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy import signal
from scipy.io import wavfile

from ..config import ROOT
from .base import AudioProvider

SR = 48000
LIBRARY = ROOT / "assets" / "sfx"


def _t(d):
    return np.arange(int(SR * d)) / SR


def _bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def _lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, fs=SR, output="sos"), x)


def _hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, btype="high", fs=SR, output="sos"), x)


def _env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))


def _reverb(x, rng, size=1.2, mix=0.35):
    n = int(SR * size)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * size / 5))
    ir = _lp(ir, 5000)
    wet = signal.fftconvolve(x, ir)[: len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return (1 - mix) * x + mix * wet * np.max(np.abs(x))


def _norm(x, peak=0.9):
    return x / (np.max(np.abs(x)) + 1e-9) * peak


def heartbeat(d, rng, bpm=None):
    bpm = bpm or rng.uniform(105, 135)
    out = np.zeros(int(SR * d))
    beat = 60 / bpm
    for start in np.arange(0, d, beat):
        for off, g in ((0, 1.0), (0.17, 0.7)):
            i = int((start + off) * SR)
            n = int(0.18 * SR)
            if i + n >= len(out):
                continue
            tt = np.arange(n) / SR
            thump = np.sin(2 * np.pi * (55 - 20 * tt) * tt) * _env(n, 0.004, 0.05)
            thump += 0.3 * _lp(rng.normal(0, 1, n), 120) * _env(n, 0.002, 0.03)
            out[i:i + n] += g * thump
    return _lp(out, 180)


def breath(d, rng):
    out = np.zeros(int(SR * d))
    t = 0.0
    while t < d:
        for phase, dur, g in (("in", rng.uniform(0.35, 0.55), 0.6), ("out", rng.uniform(0.3, 0.5), 1.0)):
            n = int(dur * SR)
            i = int(t * SR)
            if i + n > len(out):
                n = len(out) - i
                if n <= 16:
                    return out
                dur = n / SR
            e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
            nz = _bp(rng.normal(0, 1, n), 400 if phase == "in" else 250, 2600 if phase == "in" else 1800)
            out[i:i + n] += g * nz * e
            t += dur + rng.uniform(0.02, 0.08)
    return out


def footsteps(d, rng, rate=None):
    rate = rate or rng.uniform(2.6, 3.4)  # Laufen
    out = np.zeros(int(SR * d))
    for k, start in enumerate(np.arange(0.05, d, 1 / rate)):
        start += rng.uniform(-0.03, 0.03)
        i = int(start * SR)
        n = int(0.16 * SR)
        if i + n >= len(out) or i < 0:
            continue
        nz = rng.normal(0, 1, n)
        hit = _lp(nz, 900) * _env(n, 0.002, 0.03) + 0.5 * _bp(nz, 1500, 5000) * _env(n, 0.001, 0.012)
        hit += 0.6 * np.sin(2 * np.pi * 70 * np.arange(n) / SR) * _env(n, 0.002, 0.04)
        out[i:i + n] += hit * (1.0 if k % 2 else 0.85)
    return _reverb(out, rng, 0.8, 0.25)


def growl(d, rng):
    t = _t(d)
    f0 = rng.uniform(70, 100) * (1 + 0.15 * np.sin(2 * np.pi * rng.uniform(0.4, 1.2) * t)) \
        + rng.normal(0, 4, len(t)).cumsum() / SR * 30
    phase = 2 * np.pi * np.cumsum(f0) / SR
    src = signal.sawtooth(phase) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * rng.uniform(25, 38) * t)))
    src += 0.6 * rng.normal(0, 1, len(t))
    voc = sum(g * _bp(src, f * 0.85, f * 1.15) for f, g in ((450, 1.0), (1100, 0.6), (2400, 0.25)))
    env = np.sin(np.linspace(0, np.pi, len(t))) ** 0.6 * (0.7 + 0.3 * np.sin(2 * np.pi * 3 * t))
    return _reverb(voc * env, rng, 0.9, 0.3)


def impact(d, rng):
    n = int(SR * d)
    tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (80 * np.exp(-tt * 6) + 32) * tt) * _env(n, 0.002, 0.45)
    crack = _hp(rng.normal(0, 1, n), 800) * _env(n, 0.001, 0.05)
    return _reverb(boom + 0.5 * crack, rng, 1.5, 0.35)


def click(d, rng):
    n = int(SR * max(d, 0.08))
    nz = _bp(rng.normal(0, 1, n), 2500, 9000) * _env(n, 0.0005, 0.006)
    i2 = int(0.035 * SR)
    nz[i2:] += 0.6 * _bp(rng.normal(0, 1, n - i2), 1800, 7000) * _env(n - i2, 0.0005, 0.005)
    return nz


def door(d, rng):
    t = _t(d)
    f = 180 + 120 * np.sin(2 * np.pi * 0.35 * t + rng.random()) + 40 * rng.normal(0, 1, len(t)).cumsum() / SR
    creak = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * (np.sin(2 * np.pi * 9 * t) > 0))
    creak = _bp(creak, 400, 3000) * np.sin(np.linspace(0, np.pi, len(t))) ** 0.5
    out = 0.5 * creak
    tail = impact(min(0.8, d * 0.3), rng)
    out[-len(tail):] += tail * 0.8
    return _reverb(out, rng, 1.3, 0.3)


def drone(d, rng, mood="dread"):
    t = _t(d)
    base = {"dread": 41.2, "panic": 49.0, "eerie": 36.7}.get(mood, 41.2)
    x = sum(np.sin(2 * np.pi * base * m * (1 + rng.uniform(-0.004, 0.004)) * t + rng.random() * 6) * g
            for m, g in ((1, 1), (1.5, 0.35), (2.01, 0.3), (2.98, 0.12)))
    air = _bp(rng.normal(0, 1, len(t)), 200, 900) * 0.25 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t))
    if mood == "panic":
        x *= 0.8 + 0.2 * np.sin(2 * np.pi * 6 * t)
    fade = np.minimum(1, np.minimum(t / 1.5, (d - t) / 1.5).clip(0, None) + 1e-3)
    return (x + air) * fade


def stinger(d, rng):
    t = _t(d)
    cluster = sum(np.sin(2 * np.pi * f * t) for f in (311, 330, 466, 493, 622)) / 5
    cluster = cluster * _env(len(t), 0.01, d / 3) + 0.3 * _hp(rng.normal(0, 1, len(t)), 3000) * _env(len(t), 0.005, 0.15)
    out = cluster * 0.7
    out[: int(SR * min(d, 1.0))] += impact(min(d, 1.0), rng)
    return _reverb(out, rng, 2.0, 0.45)


def metal(d, rng):
    n = int(SR * d)
    tt = np.arange(n) / SR
    parts = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, k in
                ((rng.uniform(380, 420), 3), (1047, 5), (1720, 7), (2890, 9)))
    rattle = _bp(rng.normal(0, 1, n), 2000, 8000) * (np.sin(2 * np.pi * 14 * tt) > 0.3) * np.exp(-tt * 2)
    return _reverb(parts * 0.4 + rattle * 0.5, rng, 1.2, 0.35)


def scream(d, rng):
    t = _t(d)
    f0 = rng.uniform(620, 820) * (1 + 0.04 * np.sin(2 * np.pi * 6 * t)) * (1 - 0.15 * t / d)
    src = signal.sawtooth(2 * np.pi * np.cumsum(f0) / SR, 0.5)
    v = _bp(src, 900, 3200) * np.sin(np.linspace(0, np.pi, len(t))) ** 0.8
    return _lp(_reverb(v, rng, 2.2, 0.7), 3500) * 0.5   # weit weg


def glass(d, rng):
    n = int(SR * d)
    out = np.zeros(n)
    for _ in range(int(40 * d)):
        i = rng.integers(0, max(1, n - 2000))
        m = rng.integers(200, 1800)
        out[i:i + m] += _hp(rng.normal(0, 1, m), 3500) * _env(m, 0.0003, 0.004) * rng.uniform(0.2, 1)
    return _reverb(out + 0.5 * impact(d, rng) * np.exp(-np.arange(n) / SR * 8), rng, 1.0, 0.3)


GENERATORS = {"heartbeat": heartbeat, "breath": breath, "footsteps": footsteps, "growl": growl, "impact": impact,
              "click": click, "door": door, "stinger": stinger, "metal": metal, "scream": scream, "glass": glass}
DEFAULT_DUR = {"heartbeat": 4.0, "breath": 3.0, "footsteps": 3.0, "growl": 2.2, "impact": 1.6, "click": 0.12,
               "door": 2.5, "stinger": 2.5, "metal": 1.8, "scream": 2.0, "glass": 1.2}


def write_wav(path: Path, x: np.ndarray, peak: float = 0.9) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(path, SR, (_norm(x, peak) * 32767).astype(np.int16))


def _from_library(kind: str, d: float, rng) -> np.ndarray | None:
    files = sorted(LIBRARY.glob(f"{kind}*.wav")) if LIBRARY.exists() else []
    if not files:
        return None
    sr, x = wavfile.read(files[int(rng.integers(0, len(files)))])
    x = x.astype(np.float32)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        x = signal.resample_poly(x, SR, sr)
    n = int(d * SR)
    return np.pad(x, (0, max(0, n - len(x))))[:n]


class ProceduralSfx(AudioProvider):
    name = "procedural"

    def sfx(self, kind, duration, out: Path, note="", seed=0):
        if kind not in GENERATORS:
            raise ValueError(f"Unbekanntes Geräusch: {kind} (bekannt: {', '.join(GENERATORS)})")
        d = duration or DEFAULT_DUR[kind]
        rng = np.random.default_rng(seed)
        lib = _from_library(kind, d, rng)
        x = lib if lib is not None else GENERATORS[kind](d, rng)
        write_wav(out, x)
        return {"provider": "library" if lib is not None else "procedural", "usd": 0.0}

    def ambience(self, mood, duration, out: Path, seed=0):
        rng = np.random.default_rng(seed)
        write_wav(out, drone(duration, rng, mood), 0.6)
        return {"provider": "procedural", "usd": 0.0}
