"""Kostenlose Platzhalter-Provider.

Sie erzeugen keine echten Zombie-Szenen, sondern synthetische POV-Clips
(Taschenlampenkegel, Kopfbewegung, Lauf-Wackeln, Szenentext), damit die gesamte
Pipeline – Verkettung, Ton, Schnitt, Grading, QC, Export – ohne Kosten getestet
werden kann.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .base import ClipRequest, ImageProvider, VideoProvider


def _font(size: int):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _label(img: Image.Image, lines: list[str]) -> Image.Image:
    d = ImageDraw.Draw(img)
    w, h = img.size
    f = _font(max(14, w // 26))
    y = h // 12
    for ln in lines:
        d.text((w // 20 + 2, y + 2), ln, font=f, fill=(0, 0, 0))
        d.text((w // 20, y), ln, font=f, fill=(235, 235, 235))
        y += int(f.size * 1.35) if hasattr(f, "size") else 18
    return img


class MockImage(ImageProvider):
    name = "mock"

    def generate(self, ref_id, prompt, out: Path, inputs=None):
        w, h = self.ctx.width, self.ctx.height
        rng = np.random.default_rng(abs(hash(ref_id)) % 2**32)
        yy, xx = np.mgrid[0:h, 0:w]
        base = (30 + 25 * np.sin(xx / w * 3 + rng.random() * 6) + 20 * (yy / h)).astype(np.float32)
        rgb = np.stack([base * 0.8, base * 0.95, base * 1.1], -1).clip(0, 255).astype(np.uint8)
        img = _label(Image.fromarray(rgb), ["MOCK-REFERENZ", ref_id, prompt[:40]])
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, quality=92)
        return {"provider": "mock", "usd": 0.0}


class MockVideo(VideoProvider):
    name = "mock"
    supports_first_frame = True
    supports_references = True

    def generate(self, req: ClipRequest, out: Path):
        w, h = self.ctx.width, self.ctx.height
        fps = int(self.ctx.cfg["render"]["fps"])
        n = int(round(req.duration * fps))
        rng = np.random.default_rng((abs(hash(req.scene_id)) + req.attempt * 7919) % 2**32)
        start = None
        if req.first_frame and Path(req.first_frame).exists():
            start = np.asarray(Image.open(req.first_frame).convert("RGB").resize((w, h)), dtype=np.float32)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        tint = np.array([0.75, 0.9, 1.0], np.float32) * (0.8 + 0.4 * rng.random())
        text = _label(Image.new("RGB", (w, h)), ["MOCK POV-CLIP", f"Szene {req.scene_id}", f"Versuch {req.attempt}"])
        text = np.asarray(text, dtype=np.float32)
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
               "-r", str(fps), "-i", "-", "-f", "lavfi", "-t", str(req.duration), "-i",
               "anoisesrc=color=brown:amplitude=0.05:sample_rate=48000",
               "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "128k", str(out)]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        phase = rng.random() * 6
        for i in range(n):
            t = i / fps
            # POV: Gehbewegung (vertikal), Umsehen (horizontal), Taschenlampenkegel
            cx = w / 2 + w * 0.18 * np.sin(t * 0.9 + phase) + 6 * np.sin(t * 13)
            cy = h * 0.55 + h * 0.03 * np.sin(t * 7.5) + 4 * np.sin(t * 17)
            r = min(w, h) * 0.33
            d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)
            cone = np.exp(-d2 * 1.6)[..., None]
            grain = rng.normal(0, 6, (h, w, 1)).astype(np.float32)
            floor = 18 + 30 * (yy / h)[..., None] + 10 * np.sin((xx + t * 80) / 37)[..., None]
            frame = floor * tint * (0.35 + 1.6 * cone) + grain
            if start is not None and t < 0.6:  # Anschluss an die Vorszene
                a = 1 - t / 0.6
                frame = frame * (1 - a) + start * a
            frame = np.maximum(frame, text)
            p.stdin.write(frame.clip(0, 255).astype(np.uint8).tobytes())
        p.stdin.close()
        err = p.stderr.read().decode(errors="ignore")
        if p.wait() != 0:
            raise RuntimeError(f"Mock-Clip fehlgeschlagen: {err[-500:]}")
        return {"provider": "mock", "model": "procedural-pov", "usd": 0.0, "native_audio": False}
