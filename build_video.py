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
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anim_char
import cv2


class PlainRig:
    """Nur Kamerafahrt (Zoom/Schwenk), keine Figurenverformung."""
    def __init__(self, path):
        src = cv2.imread(str(path))
        up = cv2.resize(src, (anim_char.W, anim_char.H), interpolation=cv2.INTER_LANCZOS4)
        blur = cv2.GaussianBlur(up, (0, 0), 1.4)
        self.src = cv2.addWeighted(up, 1.6, blur, -0.6, 0)   # leichtes Nachschaerfen gegen Weichheit

    def frame(self, t, cam):
        z, cx, cy = cam
        W, H = anim_char.W, anim_char.H
        M = anim_char.np.float32([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]])
        return cv2.warpAffine(self.src, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "script.txt"
IMAGES = ROOT / "bilder"
WORK = ROOT / "work"
OUT = ROOT / "output"

WIDTH, HEIGHT, FPS = 1920, 1080, 30
PAD_SECONDS = 0.55          # kurze Pause nach jeder Szene
SHOT_SECONDS = 4.2          # Ziel-Takt für Bildausschnitt-Wechsel (Retention-Empfehlung 3-5 s)
VOICES = {"de": "de-DE-FlorianMultilingualNeural", "en": "en-US-AndrewMultilingualNeural"}
VOICE_RATE = "-4%"            # etwas langsamer sprechen
VOICE_PITCH = "+0Hz"
VOICE = VOICES["de"]
LANG = "de"
PIPER_USED = 0
KOKORO_USED = 0
EDGE_DEAD = False
KOKORO_BASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
PHASE_NUMBERS = {"eins": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7,
                 "acht": 8, "neun": 9, "zehn": 10, "one": 1, "two": 2, "three": 3, "four": 4,
                 "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
WORDS_PER_CHUNK = 7           # so viele Wörter stehen max. gleichzeitig im Bild
SUB_FONT = "DejaVu Sans"
SUB_SIZE = 62
# ASS-Farben sind BGR: &H00BBGGRR. Aktuelles Wort in Türkis.
COLOR_HIGHLIGHT = "&H00C5D14F&"
COLOR_NORMAL = "&H00FFFFFF&"

PIPER_MODELS = {
    "de": ("de_DE-thorsten-medium", "de/de_DE/thorsten/medium/"),
    "en": ("en_US-ryan-high", "en/en_US/ryan/high/"),
}
PIPER_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"


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
    # Seit 10.10.2026 nutzt Microsoft einen neuen Endpunkt (alter liefert 403).
    # Der Token ist der öffentliche Client-Token der edge-tts-Bibliothek (kein Geheimnis).
    try:
        import edge_tts.communicate as _ec
        from edge_tts.constants import TRUSTED_CLIENT_TOKEN as _tok
        _ec.WSS_URL = ("wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
                       "?Ocp-Apim-Subscription-Key=" + _tok)
    except Exception:
        pass

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
    name, sub = PIPER_MODELS.get(LANG, PIPER_MODELS["en"])
    for suffix in (".onnx", ".onnx.json"):
        target = model_dir / (name + suffix)
        if not target.exists():
            print(f"Lade Piper-Stimme {target.name} ...")
            urllib.request.urlretrieve(PIPER_BASE + sub + name + suffix, target)
    return model_dir / (name + ".onnx")


_KOKORO = None


def tts_kokoro(text: str, wav: Path):
    """Natuerliche englische Ersatzstimme (Kokoro, laeuft ohne Internet-Dienst)."""
    global _KOKORO
    import soundfile as sf
    if _KOKORO is None:
        from kokoro_onnx import Kokoro
        d = WORK / "kokoro"
        d.mkdir(parents=True, exist_ok=True)
        for n in ("kokoro-v1.0.int8.onnx", "voices-v1.0.bin"):
            if not (d / n).exists():
                print(f"Lade {n} ...")
                urllib.request.urlretrieve(KOKORO_BASE + n, d / n)
        _KOKORO = Kokoro(str(d / "kokoro-v1.0.int8.onnx"), str(d / "voices-v1.0.bin"))
    samples, sr = _KOKORO.create(text, voice="am_michael", speed=0.97, lang="en-us")
    sf.write(str(wav), samples, sr)


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
    # Nur Andrew (edge-tts). Keine Ersatzstimme: ist er gesperrt, wird gewartet
    # und weiter probiert; klappt es bis zum Zeitlimit nicht, bricht der Lauf ab.
    mp3 = raw.with_suffix(".mp3")
    t0 = time.time()
    attempt = 0
    while True:
        attempt += 1
        try:
            bounds = tts_edge(text, mp3)
            break
        except Exception as e:
            print(f"edge-tts Versuch {attempt} bei Szene {i} fehlgeschlagen: {e}")
            if time.time() - t0 > 4.5 * 3600:
                raise RuntimeError("Andrew dauerhaft nicht erreichbar - Abbruch, kein Ersatzstimmen-Video")
            time.sleep(min(60, 5 + 5 * attempt))
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
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
            # letztes Wort des Blocks bleibt kurz stehen, aber nie in den nächsten Block hinein
            if pos < len(chunk) - 1:
                end = times[wi][1]
            else:
                nxt = times[chunk[-1] + 1][0] if chunk[-1] + 1 < len(words) else None
                end = times[wi][1] + 0.15
                if nxt is not None:
                    end = min(end, nxt)
            events.append((times[wi][0], max(end, times[wi][0] + 0.05), " ".join(parts)))
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
Style: Main,{SUB_FONT},{SUB_SIZE},{COLOR_NORMAL},{COLOR_NORMAL},&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,4,1,2,160,160,95,1

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
    ap.add_argument("--project", default="",
                    help="Unterordner mit script.txt und bilder/ (z. B. video2); leer = Hauptordner")
    ap.add_argument("--fx", action="store_true", help="Staub- und Muenzen-Overlay einschalten (Standard: aus)")
    ap.add_argument("--rig", action="store_true", help="Figurenanimation (Kopfnicken, Blinzeln) einschalten (Standard: aus)")
    ap.add_argument("--static", action="store_true",
                    help="alte Variante ohne Film-Animation (nur Zoom/Schwenk)")
    args = ap.parse_args()

    global VOICE, SCRIPT, LANG, IMAGES
    LANG = args.lang
    VOICE = args.voice or VOICES[LANG]
    proj = ROOT / args.project if args.project else ROOT
    SCRIPT = proj / ("script_en.txt" if LANG == "en" else "script.txt")
    IMAGES = proj / "bilder"
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

    # Jede Szene wird zu einem Clip mit Kamerafahrt (weich ein-/ausgeblendet), leichtem
    # Atmen/Wippen, schwebendem Staub und bei Geld-Szenen fallenden Muenzen.
    fx_dir = WORK / "fx"
    use_fx = bool(args.fx) and not args.static   # Staub/Muenzen nur noch mit --fx
    if use_fx:
        import anim_fx
        fx_dir.mkdir(parents=True, exist_ok=True)
        anim_fx.make_dust(fx_dir / "dust.mov")
        anim_fx.make_coins(fx_dir / "coins.mov")
    money_re = re.compile(r"money|euro|€|\$|salary|paid|pay\b|cost|expens|price|cash|coin|invest|saving|"
                          r"rich|million|income|debt|loan|Geld|Gehalt|bezahl|kost|teuer|Preis|Münz|"
                          r"investier|spar|reich|Million|Einkommen|Schulden|Kredit", re.I)
    clips = []
    for n, (img, d) in enumerate(zip(images, durations)):
        frames = max(2, int(round(d * FPS)))
        F = frames
        mode = n % 8
        Wd, Hd = WIDTH, HEIGHT

        # Bildwechsel-Takt: lange Szenen werden in Teilschnitte (ca. alle SHOT_SECONDS s) zerlegt,
        # jeder mit anderem Bildausschnitt/Kamera. Das bricht das Bild oft genug, ohne neue Bilder.
        segs = 1 if n in phase_scenes else max(1, int(round(d / SHOT_SECONDS)))
        def one(prog, mode):
            e = prog * prog * (3 - 2 * prog)
            if mode == 0:   z, fx, fy = 1.00 + 0.12 * e, 0.5, 0.5
            elif mode == 1: z, fx, fy = 1.12 - 0.12 * e, 0.5, 0.5
            elif mode == 2: z, fx, fy = 1.10, e, 0.5
            elif mode == 3: z, fx, fy = 1.10, 1 - e, 0.5
            elif mode == 4: z, fx, fy = 1.02 + 0.10 * e, 0.3 + 0.4 * e, 0.7 - 0.5 * e
            elif mode == 5: z, fx, fy = 1.10, 0.5, e
            elif mode == 6: z, fx, fy = 1.02 + 0.10 * e, 0.7 - 0.4 * e, 0.3 + 0.4 * e
            elif mode == 7: z, fx, fy = 1.10, 0.5, 1 - e
            elif mode == 8:  z, fx, fy = 1.14 + 0.04 * e, 0.15 + 0.1 * e, 0.4   # Nahaufnahme links
            elif mode == 9:  z, fx, fy = 1.14 + 0.04 * e, 0.85 - 0.1 * e, 0.4   # Nahaufnahme rechts
            elif mode == 10: z, fx, fy = 1.17 - 0.04 * e, 0.5, 0.25 + 0.1 * e   # Nahaufnahme oben/Mitte
            else:            z, fx, fy = 1.14 + 0.05 * e, 0.5, 0.6               # Nahaufnahme unten/Mitte
            hw, hh = Wd / 2 / z, Hd / 2 / z
            return z, hw + fx * (Wd - 2 * hw), hh + fy * (Hd - 2 * hh)

        def camera(prog, mode=mode, segs=segs, n=n):
            if segs == 1:
                return one(prog, mode)
            k = min(segs - 1, int(prog * segs))
            p = prog * segs - k
            # erster Teilschnitt: Weitwinkel (Original-Kamera), danach wechselnde Nahaufnahmen
            m = mode if k == 0 else 8 + ((n * 3 + k * 5) % 4)
            return one(min(1.0, p), m)
        phase = n in phase_scenes
        clip = WORK / f"clip_{n + 1:02d}.mp4"
        grade = ",eq=brightness=-0.28:saturation=0.85" if phase else ""
        tail = (f"fade=t=in:st=0:d=0.18,fade=t=out:st={max(0.0, d - 0.18):.3f}:d=0.18,format=yuv420p")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
               "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-"]
        use_coins = use_fx and (not phase) and bool(money_re.search(scenes[n]))
        if not use_fx:
            fg = f"[0:v]format=yuv420p{grade},{tail}[v]"
        else:
            cmd += ["-stream_loop", "-1", "-i", str(fx_dir / "dust.mov")]
            if use_coins:
                cmd += ["-stream_loop", "-1", "-i", str(fx_dir / "coins.mov")]
            fg = f"[0:v]format=yuv420p{grade}[b];[b][1:v]overlay=shortest=1[o]"
            last = "o"
            if use_coins:
                fg += ";[o][2:v]overlay=shortest=1[o2]"
                last = "o2"
            fg += f";[{last}]{tail}[v]"
        cmd += ["-filter_complex", fg, "-map", "[v]", "-frames:v", str(frames),
                "-c:v", "libx264", "-preset", "fast", "-crf", "14", str(clip)]
        rig = anim_char.Rig(img, seed=n) if args.rig else PlainRig(img)
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for f in range(frames):
            pr.stdin.write(rig.frame(f / FPS, camera(f / max(1, frames - 1))).tobytes())
        pr.stdin.close()
        if pr.wait() != 0:
            sys.exit("ffmpeg-Fehler bei Szene %d" % (n + 1))
        clips.append(clip)
    img_list = WORK / "images.txt"
    img_list.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))

    vf = f"format=yuv420p,subtitles=work/subs.ass"
    base = args.project or "video"
    out = OUT / ("test.mp4" if args.dry_run else (f"vorschau_{base}.mp4" if args.scenes else f"{base}.mp4"))
    if LANG == "en" and not args.dry_run:
        out = out.with_name(out.stem + "_en.mp4")
    if KOKORO_USED and not PIPER_USED and not args.dry_run:
        out = out.with_name(out.stem + "_KOKORO.mp4")
    if PIPER_USED and not args.dry_run:
        out = out.with_name(out.stem + f"_ERSATZSTIMME{PIPER_USED}.mp4")
    print("Baue Video ...")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(img_list), "-i", str(WORK / "audio.wav"),
         "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "16",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
         str(out)], cwd=ROOT)
    print(f"Fertig: {out}  ({t:.0f} Sekunden)")


if __name__ == "__main__":
    main()
