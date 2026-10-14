#!/usr/bin/env python3
"""Baut Shorts (1080x1920) aus einer Spec-Datei (shorts/*.txt) und den Bildern eines Projekts.
Stimme: wie build_video.py (nur Andrew, bei Sperre wird gewartet)."""
import argparse, shutil, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_video as bv

W, H, FPS = 1080, 1920, 30
PAD = 0.35
BOX_Y, BOX_H = 560, 608          # Bildbereich (Bild in voller Breite, 16:9)


def parse(spec: Path):
    shorts, cur = [], None
    for line in spec.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("==="):
            name, hook = [x.strip() for x in line[3:].split("|", 1)]
            cur = {"name": name, "hook": hook, "scenes": []}
            shorts.append(cur)
        else:
            n, text = [x.strip() for x in line.split("|", 1)]
            cur["scenes"].append((int(n), text))
    return shorts


def write_ass(path: Path, events, hook: str):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,86,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,6,2,8,70,70,1260,1
Style: Hook,DejaVu Sans,92,&H0028D7FF&,&H0028D7FF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,7,2,8,60,60,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 0,{bv.ass_time(a)},{bv.ass_time(b)},Cap,,0,0,0,,{t}" for a, b, t in events]
    return_end = max(b for _, b, _ in events)
    lines.append(f"Dialogue: 1,{bv.ass_time(0)},{bv.ass_time(return_end)},Hook,,0,0,0,,{bv.escape_ass(hook)}")
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def make_bg(img):
    bg = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA) if False else None
    s = max(W / img.shape[1], H / img.shape[0])
    big = cv2.resize(img, (int(img.shape[1] * s) + 1, int(img.shape[0] * s) + 1), interpolation=cv2.INTER_AREA)
    x0 = (big.shape[1] - W) // 2
    y0 = (big.shape[0] - H) // 2
    bg = big[y0:y0 + H, x0:x0 + W]
    bg = cv2.GaussianBlur(bg, (0, 0), 28)
    return (bg * 0.45).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    bv.LANG = "en"
    bv.VOICE = bv.VOICES["en"]
    bv.WORDS_PER_CHUNK = 4
    bv.IMAGES = bv.ROOT / a.project / "bilder"
    bv.OUT.mkdir(exist_ok=True)
    for sh in parse(bv.ROOT / a.spec):
        if a.only and sh["name"] != a.only:
            continue
        if bv.WORK.exists():
            shutil.rmtree(bv.WORK)
        bv.WORK.mkdir(parents=True)
        events, wavs, durs, imgs = [], [], [], []
        t = 0.0
        for i, (num, text) in enumerate(sh["scenes"], start=1):
            wav, bounds = bv.make_speech(text, i, a.dry_run)
            sp = bv.duration_of(wav)
            pad = PAD
            padded = bv.WORK / f"s_{i:02d}.wav"
            bv.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", f"apad=pad_dur={pad}",
                    "-ar", "44100", "-ac", "1", str(padded)])
            events += bv.subtitle_events(text, t, sp, bounds)
            wavs.append(padded); durs.append(sp + pad); t += sp + pad
            p = bv.find_image(num)
            if p is None:
                sys.exit(f"Bild {num} fehlt")
            imgs.append(p)
        write_ass(bv.WORK / "subs.ass", events, sh["hook"])
        (bv.WORK / "audio.txt").write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
        bv.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i",
                str(bv.WORK / "audio.txt"), "-c", "copy", str(bv.WORK / "audio.wav")])
        out = bv.OUT / f"{sh['name']}_en.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-i", str(bv.WORK / "audio.wav"),
               "-vf", "subtitles=work/subs.ass,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
               "-crf", "17", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE, cwd=bv.ROOT)
        for k, (p, d) in enumerate(zip(imgs, durs)):
            src = cv2.imread(str(p))
            bg = make_bg(src)
            fg = cv2.resize(src, (W, BOX_H), interpolation=cv2.INTER_LANCZOS4)
            n = max(2, int(round(d * FPS)))
            for f in range(n):
                prog = f / (n - 1)
                z = 1.0 + 0.07 * (prog if k % 2 == 0 else 1 - prog)
                M = np.float32([[z, 0, W / 2 - z * W / 2], [0, z, BOX_H / 2 - z * BOX_H / 2]])
                box = cv2.warpAffine(fg, M, (W, BOX_H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
                fr = bg.copy()
                fr[BOX_Y:BOX_Y + BOX_H] = box
                # leichter Fade am Szenenanfang
                if f < 4:
                    fr = cv2.addWeighted(fr, 0.6 + 0.1 * f, bg, 0.4 - 0.1 * f, 0)
                pr.stdin.write(fr.tobytes())
        pr.stdin.close()
        if pr.wait() != 0:
            sys.exit("ffmpeg-Fehler")
        print(f"Fertig: {out} ({t:.1f} s)")


if __name__ == "__main__":
    main()
