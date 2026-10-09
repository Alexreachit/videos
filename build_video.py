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
VOICES = {"de": "de-DE-FlorianMultilingualNeural", "en": "en-US-AndrewMultilingualNeural"}
VOICE_RATE = "-4%"            # etwas langsamer sprechen
VOICE_PITCH = "+0Hz"
VOICE = VOICES["de"]
LANG = "de"
PHASE_NUMBERS = {"eins": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7,
                 "acht": 8, "neun": 9, "zehn": 10, "one": 1, "two": 2, "three": 3, "four": 4,
                 "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
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
        sys.exit(f"{SCRIPT.name} fehlt.")
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
    """Erzeugt die Sprache und liefert die gemessenen Wortzeiten [(Wort, Start, Ende)]."""
    import edge_tts

    async def go():
        try:
            comm = edge_tts.Communicate(text, VOICE, rate=VOICE_RATE, pitch=VOICE_PITCH,
                                        boundary="WordBoundary")
        except TypeError:  # ältere Version: WordBoundary ist dort Standard
            comm = edge_tts.Communicate(text, VOICE, rate=VOICE_RATE, pitch=VOICE_PITCH)
        bounds = []
        with open(mp3, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    st = chunk["offset"] / 1e7
                    bounds.append((chunk["text"], st, st + chunk["duration"] / 1e7))
        return bounds
    return asyncio.run(go())


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


def make_speech(text: str, i: int, dry_run: bool):
    """Liefert (WAV-Datei 44,1 kHz mono, gemessene Wortzeiten oder [])."""
    raw = WORK / f"speech_{i:02d}"
    wav = WORK / f"speech_{i:02d}.wav"
    if dry_run:
        # Stille, deren Länge zur Wortzahl passt (ca. 2,6 Wörter pro Sekunde)
        secs = max(1.5, len(text.split()) / 2.6)
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
             "anullsrc=r=44100:cl=mono", "-t", f"{secs:.2f}", str(wav)])
        return wav, []
    bounds = []
    try:
        mp3 = raw.with_suffix(".mp3")
        bounds = tts_edge(text, mp3)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
             "-ar", "44100", "-ac", "1", str(wav)])
    except Exception as e:  # edge-tts kann auf Servern geblockt sein
        print(f"edge-tts ging bei Szene {i} nicht ({e}). Nehme Piper.")
        tmp = raw.with_suffix(".piper.wav")
        tts_piper(text, tmp)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp),
             "-ar", "44100", "-ac", "1", str(wav)])
    return wav, bounds


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


def norm(w: str) -> str:
    return re.sub(r"\W", "", w).lower()


def measured_times(words, bounds):
    """Ordnet die gemessenen Wortzeiten den Wörtern des Skripts zu (über Zeichenpositionen)."""
    if not bounds:
        return None
    b_lens = [len(norm(t)) for t, _, _ in bounds]
    s_lens = [len(norm(w)) for w in words]
    if abs(sum(b_lens) - sum(s_lens)) > 0.15 * max(1, sum(s_lens)):
        return None
    b_start, pos = [], 0
    for n in b_lens:
        b_start.append(pos)
        pos += n

    def at(char_pos):
        idx = 0
        for k, st in enumerate(b_start):
            if st <= char_pos:
                idx = k
        return idx
    times, pos = [], 0
    for n in s_lens:
        first = at(min(pos, max(0, sum(b_lens) - 1)))
        last = at(min(pos + max(n, 1) - 1, max(0, sum(b_lens) - 1)))
        times.append((bounds[first][1], bounds[last][2]))
        pos += n
    return times


def phase_title(text: str):
    m = re.match(r"^\s*Phase\s+(\w+)\s*:\s*(.+?)\s*$", text, re.IGNORECASE)
    if not m or m.group(1).lower() not in PHASE_NUMBERS:
        return None
    return PHASE_NUMBERS[m.group(1).lower()], m.group(2).rstrip(".")


def subtitle_events(text: str, start: float, speech_len: float, bounds=None):
    words = text.split()
    rel = measured_times(words, bounds)
    if rel is None:
        weights = word_weights(words)
        total = sum(weights)
        rel, t = [], 0.0
        for w in weights:
            d = speech_len * w / total
            rel.append((t, t + d))
            t += d
    times = [(start + a, start + b) for a, b in rel]
    # Lücken zwischen Wörtern schließen, damit nichts flackert
    for k in range(len(times) - 1):
        times[k] = (times[k][0], max(times[k][1], times[k + 1][0]))
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


def title_events(num: int, title: str, start: float, length: float):
    t = escape_ass(title).upper()
    return [(start, start + length,
             "{\\an5\\pos(960,450)\\fs150\\c%s\\fad(300,300)}PHASE %d" % (COLOR_HIGHLIGHT, num)),
            (start, start + length,
             "{\\an5\\pos(960,620)\\fs82\\fad(300,300)}%s" % t)]


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
    ap.add_argument("--lang", choices=["de", "en"], default="de",
                    help="Sprache: de = script.txt, en = script_en.txt")
    ap.add_argument("--voice", default="", help="Stimme überschreiben, z. B. de-DE-KatjaNeural")
    args = ap.parse_args()

    global VOICE, SCRIPT, LANG
    LANG = args.lang
    VOICE = args.voice or VOICES[LANG]
    if LANG == "en":
        SCRIPT = ROOT / "script_en.txt"
    print(f"Sprache: {LANG}, Stimme: {VOICE}")

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
    phase_scenes = set()
    t = 0.0
    for i, text in enumerate(scenes, start=1):
        print(f"Szene {i}/{len(scenes)}: {text[:60]}")
        wav, bounds = make_speech(text, i, args.dry_run)
        speech_len = duration_of(wav)
        scene_len = speech_len + PAD_SECONDS
        padded = WORK / f"scene_{i:02d}.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
             "-af", f"apad=pad_dur={PAD_SECONDS}", "-ar", "44100", "-ac", "1",
             str(padded)])
        phase = phase_title(text)
        if phase:   # Titelkarte statt Wort-für-Wort-Untertitel
            events += title_events(phase[0], phase[1], t, scene_len)
            phase_scenes.add(i - 1)
        else:
            events += subtitle_events(text, t, speech_len, bounds)
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
                     f"zoompan={zp}:d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
                     + ("eq=brightness=-0.28:saturation=0.85," if n in phase_scenes else "")
                     + "format=yuv420p"),
             "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             str(clip)])
        clips.append(clip)
    img_list = WORK / "images.txt"
    img_list.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))

    vf = f"format=yuv420p,subtitles=work/subs.ass"
    out = OUT / ("test.mp4" if args.dry_run else ("vorschau.mp4" if args.scenes else "video.mp4"))
    if LANG == "en" and not args.dry_run:
        out = out.with_name(out.stem + "_en.mp4")
    print("Baue Video ...")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(img_list), "-i", str(WORK / "audio.wav"),
         "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
         str(out)], cwd=ROOT)
    print(f"Fertig: {out}  ({t:.0f} Sekunden)")


if __name__ == "__main__":
    main()
