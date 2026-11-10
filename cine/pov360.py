"""POV-360-Videos (Machart wie die Referenz @humanlabbzz) – komplett kostenlos.

Bausteine:
  * Schauplätze = 360°-Panoramen (gratis mit Gemini erzeugt, 2:1)
  * virtuelle Kopf-Kamera mit Fischaugen-Look (cine/pano.py)
  * Overlays: Untertitel, Handy-Benachrichtigung, "TEIL 1"-Marke, Abstimmungs-Endkarte
  * Ton: Geräusche exakt auf Zeitpunkte (cine/providers/procedural_audio.py)
  * Sichtprüfung: Kontaktblätter + Schlüsselbilder, die Claude selbst ansieht

Aufruf:  python -m cine.pov360 episodes/pov_zombie_ep01.yaml [--preview]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile

from .config import REPO
from .pano import Key, PanoCamera, camera_at, fix_seam, head_motion
from .providers.procedural_audio import DEFAULT_DUR, GENERATORS, SR, drone

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT_R, size)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------- Overlays
def draw_subtitle(d: ImageDraw.ImageDraw, w: int, h: int, text: str, color=(255, 255, 255), y_rel: float = 0.44):
    f = font(int(w * 0.052))
    words, lines, line = text.split(), [], ""
    for wd in words:
        c = (line + " " + wd).strip()
        if d.textlength(c, font=f) > w * 0.82:
            lines.append(line)
            line = wd
        else:
            line = c
    lines.append(line)
    y = int(h * y_rel)   # pro Einstellung wählbar (sub_y), damit nichts Wichtiges verdeckt wird
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((w - tw) / 2, y), ln, font=f, fill=color, stroke_width=max(3, w // 160), stroke_fill=(0, 0, 0))
        y += int(f.size * 1.2)


def draw_notification(d: ImageDraw.ImageDraw, w: int, h: int, sender: str, text: str, app="NACHRICHTEN",
                      clock="23:47", slide: float = 1.0):
    m = int(w * 0.03)
    bh = int(h * 0.105)
    y0 = int(h * 0.065 - (1 - slide) * (bh + h * 0.08))
    d.rounded_rectangle([m, y0, w - m, y0 + bh], radius=int(w * 0.03), fill=(246, 246, 248), outline=(210, 210, 215))
    fs, fb = font(int(w * 0.027)), font(int(w * 0.036))
    d.rounded_rectangle([m * 2, y0 + m * 0.7, m * 2 + w * 0.03, y0 + m * 0.7 + w * 0.03], radius=4, fill=(52, 199, 89))
    d.text((m * 2 + w * 0.045, y0 + m * 0.65), app, font=fs, fill=(110, 110, 115))
    d.text((w - m * 2 - d.textlength(clock, font=fs), y0 + m * 0.65), clock, font=fs, fill=(200, 60, 60))
    d.text((m * 2, y0 + bh * 0.38), sender, font=fb, fill=(20, 20, 20))
    d.text((m * 2, y0 + bh * 0.64), text[:46], font=font(int(w * 0.033), False), fill=(30, 30, 30))


def load_hands(path: Path, W: int, H: int) -> Image.Image:
    """Hände/Ärmel/Handy vor Grün (Gemini) freistellen -> RGBA in Videogröße."""
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Hände-Bild fehlt: {path}")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(hsv, (40, 90, 70), (85, 255, 255))
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    alpha = 255 - green
    alpha = cv2.GaussianBlur(cv2.erode(alpha, np.ones((3, 3), np.uint8)), (3, 3), 0)
    # grünen Farbsaum an den Kanten entfernen
    b, g, r = cv2.split(img)
    g = np.minimum(g, np.maximum(b, r).astype(np.int16) + 20).clip(0, 255).astype(np.uint8)
    rgba = cv2.merge([r, g, b, alpha])
    pil = Image.fromarray(rgba, "RGBA")
    scale = W / pil.width
    pil = pil.resize((W, int(pil.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(pil, (0, H - pil.height))
    return canvas


def place_hands(img: Image.Image, hands: Image.Image, t: float, lt: float, walk: float, raise_: float):
    """Hände mit Atem-/Lauf-Bewegung; raise_ 0..1 hebt das Handy ins Bild."""
    import math
    dy = 6 * math.sin(t * 1.3) + walk * 14 * abs(math.sin(t * 2 * math.pi * 0.95))
    dx = 4 * math.sin(t * 0.8) + walk * 6 * math.sin(t * 2 * math.pi * 0.95)
    off = int((1 - raise_) * img.height * 0.32)
    img.alpha_composite(hands, (int(dx), int(dy) + off))


def draw_badge(d: ImageDraw.ImageDraw, w: int, h: int, label: str):
    f = font(int(w * 0.026))
    tw = d.textlength(label, font=f)
    x0, y0 = (w - tw) / 2 - 12, int(h * 0.012)
    d.rounded_rectangle([x0, y0, x0 + tw + 24, y0 + f.size + 12], radius=8, fill=(40, 40, 40, 200))
    d.text((x0 + 12, y0 + 5), label, font=f, fill=(255, 255, 255))


def draw_choice(img: Image.Image, question: str, options: list[str], u: float):
    w, h = img.size
    shade = Image.new("RGBA", img.size, (0, 0, 0, int(140 * min(1, u * 3))))
    img.alpha_composite(shade)
    d = ImageDraw.Draw(img)
    fq = font(int(w * 0.062))
    y = int(h * 0.30)
    for ln in question.split("\n"):
        tw = d.textlength(ln, font=fq)
        d.text(((w - tw) / 2, y), ln, font=fq, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
        y += int(fq.size * 1.15)
    cols = [(32, 120, 230), (220, 50, 50), (40, 160, 90)]
    fo, fs = font(int(w * 0.042)), font(int(w * 0.03))
    bw, bh = w * 0.72, h * 0.065
    y += int(h * 0.04)
    for i, op in enumerate(options):
        k = min(1, max(0, (u - 0.15 - i * 0.12) * 5))
        if k > 0:
            x0 = (w - bw) / 2 + (1 - k) * w * (-1 if i % 2 == 0 else 1)
            d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=int(bh / 2), fill=cols[i % 3])
            tw = d.textlength(op, font=fo)
            d.text((x0 + (bw - tw) / 2, y + (bh - fo.size) / 2 - 2), op, font=fo, fill=(255, 255, 255))
        y += bh
        if i < len(options) - 1:
            gap = int(bh * 0.9)
            if k > 0:
                d.text(((w - d.textlength("ODER", font=fs)) / 2, y + (gap - fs.size) / 2), "ODER", font=fs,
                       fill=(255, 220, 90), stroke_width=2, stroke_fill=(0, 0, 0))
            y += gap
    if u > 0.5:
        fr = font(int(w * 0.03), False)
        t = "Schreib es in die Kommentare"
        d.text(((w - d.textlength(t, font=fr)) / 2, y + h * 0.025), t, font=fr, fill=(255, 255, 255),
               stroke_width=2, stroke_fill=(0, 0, 0))


# ---------------------------------------------------------------- Grading
def grade(frame: np.ndarray, kind: str, t: float, flicker: float = 0.0) -> np.ndarray:
    f = frame.astype(np.float32)
    if kind == "night":
        # Schatten anheben, Mitten aufhellen – Cartoon-Linien bleiben, Bild wird nicht matschig
        f = 255 * (f / 255) ** 0.78
        mean = f.mean()
        f = (f - mean) * 1.12 + mean + 6
    if flicker:
        f *= 1 - flicker * (0.5 + 0.5 * np.sign(np.sin(t * 37) * np.sin(t * 11.3)))
    h, w = f.shape[:2]
    yy, xx = np.ogrid[:h, :w]
    vig = 1 - 0.35 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 1.6)) ** 2)
    f *= vig[..., None].clip(0.45, 1)
    return f.clip(0, 255).astype(np.uint8)


# ---------------------------------------------------------------- Renderer
def load_episode(path: Path) -> dict:
    ep = yaml.safe_load(path.read_text(encoding="utf-8"))
    t = 0.0
    for s in ep["shots"]:
        s["start"] = t
        t += float(s["duration"])
    ep["total"] = t + float(ep.get("end_card", {}).get("duration", 0))
    return ep


def render(ep_path: Path, out_dir: Path, preview: bool = False) -> Path:
    ep = load_episode(ep_path)
    W, H = (288, 512) if preview else (int(ep.get("width", 720)), int(ep.get("height", 1280)))
    fps = 12 if preview else int(ep.get("fps", 30))
    out_dir.mkdir(parents=True, exist_ok=True)
    video = out_dir / ("preview.mp4" if preview else f"{ep['id']}.mp4")
    base = ep_path.parent
    cams: dict[str, PanoCamera] = {}

    def cam_for(p: str) -> PanoCamera:
        if p not in cams:
            path = (base / p) if not Path(p).is_absolute() else Path(p)
            img = cv2.imread(str(path))
            if img is None:
                raise FileNotFoundError(f"Panorama fehlt: {path}")
            if img.shape[1] < 4096:   # weichere, sauberere Linien beim Heranzoomen
                img = cv2.resize(img, (4096, 2048), interpolation=cv2.INTER_LANCZOS4)
            cams[p] = PanoCamera(fix_seam(img, 32), W, H)
        return cams[p]

    hands = load_hands(base / ep["hands"], W, H) if ep.get("hands") else None
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "20", "-pix_fmt", "yuv420p", str(out_dir / "_video.mp4")], stdin=subprocess.PIPE)
    n = int(round(ep["total"] * fps))
    last = None
    last_with_hands = None
    for i in range(n):
        t = i / fps
        shot = next((s for s in ep["shots"] if s["start"] <= t < s["start"] + s["duration"]), None)
        if shot is not None:
            lt = t - shot["start"]
            keys = [Key(*k) if isinstance(k, list) else Key(**k) for k in shot["camera"]]
            yaw, pitch, fov = camera_at(keys, lt)
            jy, jp = head_motion(t, float(shot.get("walk", 0)), seed=hash(shot["pano"]) % 7)
            frame = cam_for(shot["pano"]).render(yaw + jy, pitch + jp, fov)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = grade(frame, ep.get("grade", "night"), t, float(shot.get("flicker", 0)) if
                          any(a <= lt < b for a, b in shot.get("flicker_at", [])) else 0.0)
            if lt < 0.25 and shot.get("transition") == "blink":   # Augenzwinkern statt hartem Schnitt
                k = 1 - lt / 0.25
                frame = (frame * (1 - k)).astype(np.uint8)
            last = frame
        else:
            frame = last
        img = Image.fromarray(frame).convert("RGBA")
        if hands is not None and shot is not None:
            lt = t - shot["start"]
            r = shot.get("hands", 1.0)
            if isinstance(r, list):   # [[t, wert], …] linear interpoliert
                r = float(np.interp(lt, [a for a, _ in r], [b for _, b in r]))
            if r > 0.01:
                place_hands(img, hands, t, lt, float(shot.get("walk", 0)), float(r))
            last_with_hands = img.copy()
        elif shot is None and hands is not None and last_with_hands is not None:
            img = last_with_hands.copy()
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        if shot is not None:
            lt = t - shot["start"]
            for nt in shot.get("notify", []):
                if nt["t"] <= lt < nt.get("until", nt["t"] + 3):
                    draw_notification(d, W, H, nt["from"], nt["text"], clock=ep.get("clock", "23:47"),
                                      slide=min(1, (lt - nt["t"]) / 0.25))
            for st in shot.get("subs", []):
                if st[0] <= lt < st[1]:
                    draw_subtitle(d, W, H, st[2], tuple(st[3]) if len(st) > 3 else (255, 255, 255), float(st[4]) if len(st) > 4 else float(shot.get('sub_y', 0.44)))
        if ep.get("badge"):
            draw_badge(d, W, H, ep["badge"])
        img.alpha_composite(layer)
        ec = ep.get("end_card")
        if shot is None and ec:
            draw_choice(img, ec["question"], ec["options"], (t - ep["shots"][-1]["start"] - ep["shots"][-1]["duration"]) / ec["duration"])
        proc.stdin.write(np.asarray(img.convert("RGB")).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("ffmpeg (Video) fehlgeschlagen")

    audio = build_audio(ep, out_dir)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out_dir / "_video.mp4", "-i", audio,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-2",
                    "-shortest", "-movflags", "+faststart", video], check=True)
    return video


def build_audio(ep: dict, out_dir: Path) -> Path:
    total = ep["total"]
    buf = np.zeros(int(total * SR) + SR, np.float32)
    rng = np.random.default_rng(7)

    def place(x, at, gain_db):
        i = int(at * SR)
        x = x / (np.abs(x).max() + 1e-9) * 10 ** (gain_db / 20)
        m = min(len(x), len(buf) - i)
        if m > 0:
            buf[i:i + m] += x[:m]

    for s in ep["shots"]:
        place(drone(s["duration"] + 0.5, rng, s.get("ambience", "dread")) * 0.6, s["start"], -18)
        for c in s.get("sfx", []):
            kind, at = c[0], c[1]
            gain = c[2] if len(c) > 2 else -6
            dur = c[3] if len(c) > 3 else DEFAULT_DUR[kind]
            place(GENERATORS[kind](dur, rng), s["start"] + at, gain)
    if ep.get("end_card"):
        place(GENERATORS["stinger"](2.5, rng), ep["total"] - ep["end_card"]["duration"], -6)
    buf = buf[: int(total * SR)]
    buf /= max(1.0, np.abs(buf).max() / 0.9)
    p = out_dir / "_audio.wav"
    wavfile.write(p, SR, (buf * 32767).astype(np.int16))
    return p


# ---------------------------------------------------------------- Sichtprüfung
def review_sheets(video: Path, out_dir: Path, every: float = 1.0, cols: int = 6) -> list[Path]:
    """Kontaktblätter mit Zeitstempel – diese Bilder werden vor jeder Abgabe angesehen."""
    sheets = []
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                video], capture_output=True, text=True).stdout or 0)
    per = cols * 3
    for k in range(int(np.ceil(dur / every / per))):
        p = out_dir / f"review_{k + 1:02d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(k * per * every), "-t", str(per * every),
                        "-i", video, "-vf", f"fps=1/{every},scale=200:-1,drawtext=fontfile={FONT_B}:"
                        f"text='%{{pts\\:hms}}':x=4:y=h-th-4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.7,"
                        f"setpts=PTS+{k * per * every}/TB,tile={cols}x3", "-frames:v", "1", p], check=True)
        sheets.append(p)
    return sheets


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    ep_path = Path(a.episode).resolve()
    out = Path(a.out) if a.out else REPO / "productions" / ep_path.stem
    v = render(ep_path, out, a.preview)
    sheets = review_sheets(v, out)
    print(v)
    print("Sichtprüfung:", *sheets, sep="\n  ")


if __name__ == "__main__":
    sys.exit(main())
