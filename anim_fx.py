#!/usr/bin/env python3
"""Erzeugt wiederholbare Overlay-Schleifen (mit Transparenz) fuer die Film-Animation:
  dust.mov  - sanft schwebende Staubpartikel / Lichtflocken
  coins.mov - fallende, sich drehende Muenzen (fuer Geld-Szenen)
Alles kostenlos mit numpy + Pillow, kein Download noetig."""
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1920, 1080, 30


def _pipe(path: Path, nframes: int, frame_fn):
    p = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", str(path)],
        stdin=subprocess.PIPE)
    for f in range(nframes):
        p.stdin.write(frame_fn(f).tobytes())
    p.stdin.close()
    p.wait()


def make_dust(path: Path, seconds=10):
    rnd = random.Random(7)
    n = int(seconds * FPS)
    parts = []
    for _ in range(70):
        r = rnd.choice([3, 4, 5, 7, 10])
        spr = Image.new("RGBA", (r * 6, r * 6), (0, 0, 0, 0))
        ImageDraw.Draw(spr).ellipse([r * 2, r * 2, r * 4, r * 4], fill=(255, 250, 235, rnd.randint(70, 150)))
        spr = spr.filter(ImageFilter.GaussianBlur(r * 0.5))
        parts.append(dict(spr=spr, x=rnd.uniform(0, W), y=rnd.uniform(0, H),
                          vx=rnd.uniform(-10, 14), vy=rnd.uniform(-22, -6),
                          ph=rnd.uniform(0, 6.28), cycles=rnd.choice([1, 2])))

    def frame(f):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        t = f / n
        for q in parts:
            # Position ist periodisch -> nahtlose Schleife
            x = (q["x"] + q["vx"] * seconds * t + 25 * math.sin(2 * math.pi * q["cycles"] * t + q["ph"])) % W
            y = (q["y"] + q["vy"] * seconds * t) % H
            img.alpha_composite(q["spr"], (int(x) - q["spr"].width // 2 if 0 <= x < W else 0,
                                           int(y) - q["spr"].height // 2 if 0 <= y < H else 0)) \
                if 0 < x < W - q["spr"].width and 0 < y < H - q["spr"].height else None
        return np.asarray(img)
    _pipe(path, n, frame)


def _coin(w):
    s = 64
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 1, s - 2, s - 2], fill=(120, 80, 10, 255))
    d.ellipse([5, 5, s - 6, s - 6], fill=(244, 196, 48, 255))
    d.ellipse([14, 14, s - 15, s - 15], outline=(190, 140, 20, 255), width=3)
    d.rectangle([s // 2 - 3, 20, s // 2 + 2, s - 21], fill=(190, 140, 20, 255))
    return img.resize((max(4, int(s * w)), s), Image.LANCZOS)


def make_coins(path: Path, seconds=8):
    rnd = random.Random(11)
    n = int(seconds * FPS)
    sizes = [0.9, 0.7, 0.45, 0.2]
    coins = []
    for _ in range(26):
        sc = rnd.choice([0.5, 0.7, 0.9])
        coins.append(dict(x=rnd.uniform(40, W - 80), y0=rnd.uniform(0, H + 200), sc=sc,
                          speed=int(H + 300) / seconds * rnd.choice([1, 2]) * rnd.uniform(0.8, 1.0),
                          spin=rnd.choice([1, 2, 3]), ph=rnd.uniform(0, 6.28)))
    cache = {}

    def frame(f):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        t = f / n
        for c in coins:
            y = (c["y0"] + c["speed"] * seconds * t) % (H + 200) - 100
            w = abs(math.cos(2 * math.pi * c["spin"] * t + c["ph"]))
            key = (c["sc"], int(w * 12))
            if key not in cache:
                spr = _coin(max(0.08, int(w * 12) / 12))
                cache[key] = spr.resize((max(3, int(spr.width * c["sc"])), max(3, int(spr.height * c["sc"]))), Image.LANCZOS)
            spr = cache[key]
            x = int(c["x"] + 18 * math.sin(2 * math.pi * t + c["ph"]))
            img.alpha_composite(spr, (min(max(x, 0), W - spr.width), min(max(int(y), 0), H - spr.height)))
        return np.asarray(img)
    _pipe(path, n, frame)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    make_dust(out / "dust.mov")
    make_coins(out / "coins.mov")
