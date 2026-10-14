"""Animation Stufe 2: Tiefen-Parallax (2,5D), Lippensynchronisation und sanfte Kamera.
Nur freie Werkzeuge: OpenCV/numpy plus ein kleines freies Tiefenmodell (Depth Anything V2 Small)."""
import hashlib
import math
import os
import subprocess
from pathlib import Path

import cv2
import numpy as np

import anim_char
from anim_char import W, H, Rig, cream_mask

_PIPE = None
LIPSYNC = bool(os.environ.get("ANIM2_LIPSYNC"))   # Erzaehler-Stil: Figuren sprechen nicht, standardmaessig aus


def _depth_model():
    global _PIPE
    if _PIPE is None:
        from transformers import pipeline
        _PIPE = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=-1)
    return _PIPE


def depth_map(img_bgr, cache_dir: Path, key: str):
    """Tiefe 0..1 (1 = nah) in Bildgroesse W x H, zwischengespeichert."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    f = cache_dir / (hashlib.md5(key.encode()).hexdigest() + ".npy")
    if f.exists():
        return np.load(f)
    if os.environ.get("ANIM2_FAKE_DEPTH"):      # nur fuer lokale Geometrie-Tests
        g = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
        d = cv2.GaussianBlur(g, (0, 0), 25)
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        d = 0.5 * d + 0.5 * yy
    else:
        from PIL import Image
        rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        out = _depth_model()(Image.fromarray(rgb))["predicted_depth"]
        d = out.squeeze().cpu().numpy().astype(np.float32)
        d = cv2.resize(d, (W, H), interpolation=cv2.INTER_CUBIC)
    lo, hi = np.percentile(d, 2), np.percentile(d, 98)
    d = np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)
    d = cv2.bilateralFilter(d, 9, 0.1, 15)      # Kanten behalten, Flaechen glaetten
    d = cv2.GaussianBlur(d, (0, 0), 4)
    np.save(f, d)
    return d


def envelope(wav: Path, fps=30):
    """Lautstaerke pro Videobild (0..1) aus der Sprachdatei."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    hop = 16000 // fps
    n = len(a) // hop
    if n == 0:
        return np.zeros(1, np.float32)
    rms = np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(axis=1))
    ref = np.percentile(rms, 95) + 1e-6
    e = np.clip(rms / ref, 0, 1)
    k = np.array([0.25, 0.5, 0.25], np.float32)
    return np.convolve(e, k, mode="same")


class Anim2Rig(Rig):
    def __init__(self, path, wav, seed=0, workdir=Path("work"), fps=30):
        super().__init__(path, seed)
        self.fps = fps
        self.seed = seed
        self.env = envelope(Path(wav), fps)
        self.depth = depth_map(self.src, Path(workdir) / "depth", f"{Path(path).resolve()}:{os.path.getmtime(path)}")
        self.speaker = None
        heads = [p for p in self.parts if p.kind == "head" and p.eyes]
        if heads:
            self.speaker = max(heads, key=lambda p: p.area)
            x, y, w, h = self.speaker.box
            ex = np.mean([e[0] for e in self.speaker.eyes])
            ey = np.mean([e[1] for e in self.speaker.eyes])
            
            m = (self.speaker.mask > 0) & (cream_mask(self.src) > 0)
            self.cream_col = tuple(int(v) for v in np.median(self.src[m], axis=0))
        if self.speaker is None:
            self._fallback_speaker()
        if self.speaker is not None:
            self._locate_mouth()
        gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        self.gx, self.gy = gx, gy

    def _locate_mouth(self):
        """Den gezeichneten Mund (dunkle Linie im unteren Kopfdrittel) suchen."""
        x, y, w, h = self.speaker.box
        mask = getattr(self.speaker, "mask", None)
        if mask is None:
            mask = getattr(self, "fb_mask", None)
        gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        dark = (gray < 95).astype(np.uint8) * 255
        if mask is not None:
            dark &= cv2.erode(mask, np.ones((9, 9), np.uint8))
        reg = np.zeros_like(dark)
        reg[int(y + 0.50 * h):int(y + 0.85 * h), int(x + 0.15 * w):int(x + 0.85 * w)] = 255
        dark &= reg
        n, lab, st, cent = cv2.connectedComponentsWithStats(dark, 8)
        best = None
        for i in range(1, n):
            bx, by, bw, bh, a = st[i]
            if bw < 0.08 * w or bw < 1.3 * bh or a < 12:
                continue
            if best is None or a > best[0]:
                best = (a, bx + bw / 2.0, by + bh / 2.0, bw, bh)
        if best is None:
            self.mouth_xy = (int(x + w / 2), int(y + 0.64 * h))
            self.smile_w = 0.22 * w
        else:
            self.mouth_xy = (int(best[1]), int(best[2]))
            self.smile_w = float(best[3])

    def _fallback_speaker(self):
        """Kopf ohne erkannte Augen: groesste runde cremefarbene Flaeche nehmen."""
        m = cream_mask(self.src)
        closed = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(closed, 8)
        best = None
        for i in range(1, n):
            x, y, w, h, a = stats[i]
            if a < 9000 or w > W * 0.5 or h > H * 0.8:
                continue
            fill = a / float(w * h)
            if not (0.66 < fill < 0.92 and 0.72 < w / float(h) < 1.35):
                continue
            if best is None or a > best[4]:
                best = (x, y, w, h, a)
        if best is None:
            return
        x, y, w, h, a = best
        sp = type("Sp", (), {})()
        sp.box = (x, y, w, h)
        sp.area = a
        self.speaker = sp
        self.fb_mask = (lab == (np.argmax(stats[1:, 4] == a) + 1)).astype(np.uint8) * 255
        mm = (lab == (np.argmax(stats[1:, 4] == a) + 1)) & (m > 0)
        col = self.src[mm]
        self.cream_col = tuple(int(v) for v in np.median(col, axis=0)) if len(col) else (200, 225, 240)

    def _speak(self, t):
        if not LIPSYNC or self.speaker is None:
            return None
        i = min(len(self.env) - 1, int(t * self.fps))
        o = float(self.env[i])
        if o < 0.12:
            return None
        base = self.blink_img if (self.blink_state(t) and self.blinking_parts) else self.src
        img = base.copy()
        x, y, w, h = self.speaker.box
        mx, my = self.mouth_xy
        sw = self.smile_w
        cv2.ellipse(img, (mx, my), (int(0.75 * sw), int(0.38 * sw)), 0, 0, 360, self.cream_col, -1, cv2.LINE_AA)
        ow = int(0.28 * sw * (0.8 + 0.5 * o))
        oh = max(2, int(0.26 * sw * (0.25 + 0.95 * o)))
        cv2.ellipse(img, (mx, my), (ow, oh), 0, 0, 360, (28, 24, 40), -1, cv2.LINE_AA)
        cv2.ellipse(img, (mx, my), (ow, oh), 0, 0, 360, (20, 20, 20), max(2, int(0.012 * h)), cv2.LINE_AA)
        return img

    def frame(self, t, cam):
        img = self.compose(t, self._speak(t))
        z, cx, cy = cam
        # Kamerafahrt rueckwaerts: Ausgabepixel -> Quellpixel
        sx = (self.gx - (W / 2 - z * cx)) / z
        sy = (self.gy - (H / 2 - z * cy)) / z
        d = cv2.remap(self.depth, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ph = self.seed * 1.7
        ax = 26.0 * math.sin(2 * math.pi * t / 7.5 + ph)
        ay = 9.0 * math.sin(2 * math.pi * t / 10.0 + ph + 1.0)
        near = d - 0.45
        mapx = (sx - near * ax).astype(np.float32)
        mapy = (sy - near * ay).astype(np.float32)
        return cv2.remap(img, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
