#!/usr/bin/env python3
"""
Baut aus script.txt und bilder/01.png, 02.png, ... ein fertiges Video.

Ablauf:
  1. Jede Zeile in script.txt ist eine Szene.
  2. Pro Szene wird eine Sprecherstimme erzeugt (edge-tts, Ersatz: Piper).
  3. Die Szenendauer richtet sich nach der Sprechdauer.
  4. Untertitel erscheinen Wort für Wort, das aktuelle Wort ist farbig.
  5. ffmpeg setzt Bilder, Ton und Untertitel zu output/video.mp4 zusammen.

Aufruf:
  python build_video.py              # echtes Video
  python build_video.py --dry-run    # Test mit stiller Tonspur und Platzhalterbildern
"""
import argparse
import asyncio
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "script.txt"
IMAGES = ROOT / "bilder"
WORK = ROOT / "work"
OUT = ROOT / "output"

WIDTH, HEIGHT, FPS = 1920, 1080, 30
PAD_SECONDS = 0.35          # kurze Pause nach jeder Szene
VOICE = "de-DE-ConradNeural"  # andere Stimmen: de-DE-KatjaNeural, de-DE-KillianNeural
VOICE_RATE = "-5%"            # etwas langsamer sprechen
WORDS_PER_CHUNK = 7           # so viele Wörter stehen max. gleichzeitig im Bild
SUB_FONT = "DejaVu Sans"
SUB_SIZE = 84
# ASS-Farben sind BGR: &H00BBGGRR. Aktuelles Wort in Türkis.
COLOR_HIGHLIGHT = "&H00C5D14F&"
COLOR_NORMAL = "&H00FFFFFF&"

PIPER_MODEL = "de_DE-thorsten-medium"
PIPER_URL = ("https://huggingface.co/rhasspy/piper-voices/resolve/main/"
             "de/de_DE/thorsten/medium/" + PIPER_MODEL)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def duration_of(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def read_scenes():
    if not SCRIPT.exists():
        sys.exit("script.txt fehlt.")
    scenes = [l.strip() for l in SCRIPT.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.strip().startswith("#")]
    if not scenes:
        sys.exit("script.txt ist leer.")
    return scenes


def find_image(i: int):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = IMAGES / f"{i:02d}.{ext}"
        if p.exists():
            return p
    return None


# ---------- Sprache ----------

def tts_edge(text: str, mp3: Path):
    import edge_tts

    async def go():
        await edge_tts.Communicate(text, VOICE, rate=VOICE_RATE).save(str(mp3))
    asyncio.run(go())


def ensure_piper_model() -> Path:
    model_dir = WORK / "piper"
    model_dir.mkdir(parents=True, exist_ok=True)
    for suffix in (".onnx", ".onnx.json"):
        target = model_dir / (PIPER_MODEL + suffix)
        if not target.exists():
            print(f"Lade Piper-Stimme {target.name} ...")
            urllib.request.urlretrieve(PIPER_URL + suffix, target)
    return model_dir / (PIPER_MODEL + ".onnx")


def tts_piper(text: str, wav: Path):
    model = ensure_piper_model()
    run([sys.executable, "-m", "piper", "-m", str(model), "-f", str(wav)],
        input=text.encode("utf-8"))


def make_speech(text: str, i: int, dry_run: bool) -> Path:
    """Liefert eine WAV-Datei (44,1 kHz mono) mit der gesprochenen Szene."""
    raw = WORK / f"speech_{i:02d}"
    wav = WORK / f"speech_{i:02d}.wav"
    if dry_run:
        # Stille, deren Länge zur Wortzahl passt (ca. 2,6 Wörter pro Sekunde)
        secs = max(1.5, len(text.split()) / 2.6)
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
             "anullsrc=r=44100:cl=mono", "-t", f"{secs:.2f}", str(wav)])
        return wav
    try:
        mp3 = raw.with_suffix(".mp3")
        tts_edge(text, mp3)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
             "-ar", "44100", "-ac", "1", str(wav)])
    except Exception as e:  # edge-tts kann auf Servern geblockt sein
        print(f"edge-tts ging bei Szene {i} nicht ({e}). Nehme Piper.")
        tmp = raw.with_suffix(".piper.wav")
        tts_piper(text, tmp)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp),
             "-ar", "44100", "-ac", "1", str(wav)])
    return wav


# ---------- Untertitel ----------

def ass_time(t: float) -> str:
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def word_weights(words):
    """Längere Wörter und Satzzeichen brauchen mehr Zeit."""
    ws = []
    for w in words:
        weight = len(re.sub(r"\W", "", w)) + 2
        if w.endswith((",", ";", ":")):
            weight += 3
        if w.endswith((".", "!", "?")):
            weight += 5
        ws.append(weight)
    return ws


def escape_ass(s: str) -> str:
    return s.replace("\\", "").replace("{", "(").replace("}", ")")


def subtitle_events(text: str, start: float, speech_len: float):
    words = text.split()
    weights = word_weights(words)
    total = sum(weights)
    times, t = [], start
    for w in weights:
        d = speech_len * w / total
        times.append((t, t + d))
        t += d
    events = []
    for c0 in range(0, len(words), WORDS_PER_CHUNK):
        chunk = list(range(c0, min(c0 + WORDS_PER_CHUNK, len(words))))
        for pos, wi in enumerate(chunk):
            parts = []
            for j in chunk[:pos + 1]:
                w = escape_ass(words[j]).upper()
                if j == wi:
                    parts.append("{\\c%s}%s{\\c%s}" % (COLOR_HIGHLIGHT, w, COLOR_NORMAL))
                else:
                    parts.append(w)
            # letztes Wort des Blocks bleibt bis zum Blockende stehen
            end = times[wi][1] if pos < len(chunk) - 1 else times[wi][1] + 0.15
            events.append((times[wi][0], end, " ".join(parts)))
    return events


def write_ass(path: Path, events):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{SUB_FONT},{SUB_SIZE},{COLOR_NORMAL},{COLOR_NORMAL},&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,6,2,2,160,160,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Main,,0,0,0,,{txt}"
             for a, b, txt in events]
    path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


# ---------- Hauptprogramm ----------

def placeholder_image(i: int, path: Path):
    colors = ["2d3a4a", "4a3a2d", "2d4a3a", "4a2d3a", "3a4a2d", "3a2d4a"]
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
         f"color=c=0x{colors[i % len(colors)]}:s={WIDTH}x{HEIGHT}",
         "-frames:v", "1", str(path)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Test ohne Stimme: stille Tonspur, fehlende Bilder werden ersetzt")
    ap.add_argument("--scenes", type=int, default=0,
                    help="nur die ersten N Szenen bauen (Vorschau), 0 = alle")
    args = ap.parse_args()

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    OUT.mkdir(exist_ok=True)

    scenes = read_scenes()
    if args.scenes:
        scenes = scenes[:args.scenes]
    print(f"{len(scenes)} Szenen gefunden.")

    # Bilder prüfen
    images = []
    missing = []
    for i in range(1, len(scenes) + 1):
        img = find_image(i)
        if img is None:
            if args.dry_run:
                img = WORK / f"placeholder_{i:02d}.png"
                placeholder_image(i, img)
            else:
                missing.append(f"{i:02d}")
                continue
        images.append(img)
    if missing:
        sys.exit("Es fehlen Bilder für die Szenen: " + ", ".join(missing) +
                 "\nLege sie als bilder/01.png, bilder/02.png ... ab.")

    # Sprache, Dauer, Untertitel
    events, wavs, durations = [], [], []
    t = 0.0
    for i, text in enumerate(scenes, start=1):
        print(f"Szene {i}/{len(scenes)}: {text[:60]}")
        wav = make_speech(text, i, args.dry_run)
        speech_len = duration_of(wav)
        scene_len = speech_len + PAD_SECONDS
        padded = WORK / f"scene_{i:02d}.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
             "-af", f"apad=pad_dur={PAD_SECONDS}", "-ar", "44100", "-ac", "1",
             str(padded)])
        events += subtitle_events(text, t, speech_len)
        wavs.append(padded)
        durations.append(scene_len)
        t += scene_len

    write_ass(WORK / "subs.ass", events)

    # Listen für ffmpeg
    audio_list = WORK / "audio.txt"
    audio_list.write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(audio_list), "-c", "copy", str(WORK / "audio.wav")])

    # Jede Szene wird zu einem kurzen Clip mit sanftem Zoom bzw. Schwenk
    # (abwechselnd, damit das Video lebendig wirkt)
    clips = []
    for n, (img, d) in enumerate(zip(images, durations)):
        frames = max(2, int(round(d * FPS)))
        mode = n % 4
        if mode == 0:    # langsam hineinzoomen
            zp = f"z='1+0.10*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        elif mode == 1:  # langsam herauszoomen
            zp = f"z='1.10-0.10*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        elif mode == 2:  # Schwenk von links nach rechts
            zp = f"z='1.08':x='(iw-iw/zoom)*on/{frames}':y='ih/2-(ih/zoom/2)'"
        else:            # Schwenk von rechts nach links
            zp = f"z='1.08':x='(iw-iw/zoom)*(1-on/{frames})':y='ih/2-(ih/zoom/2)'"
        clip = WORK / f"clip_{n + 1:02d}.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(img),
             "-vf", (f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
                     f"zoompan={zp}:d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p"),
             "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             str(clip)])
        clips.append(clip)
    img_list = WORK / "images.txt"
    img_list.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))

    vf = f"format=yuv420p,subtitles=work/subs.ass"
    out = OUT / ("test.mp4" if args.dry_run else ("vorschau.mp4" if args.scenes else "video.mp4"))
    print("Baue Video ...")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(img_list), "-i", str(WORK / "audio.wav"),
         "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
         str(out)], cwd=ROOT)
    print(f"Fertig: {out}  ({t:.0f} Sekunden)")


if __name__ == "__main__":
    main()
