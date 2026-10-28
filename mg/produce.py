"""Motion-Graphics-Produktion: Skriptzeilen -> Stimme (Andrew) -> Timeline -> Frames -> Ton-Mix -> MP4.
Aufruf: python mg/produce.py tt01 [--fake-tts] [--workers 4]
Die Szene (scene.html) bekommt die Timeline per window.setTimeline() und zeichnet per window.draw(t).
Soundeffekte kommen aus window.sfxEvents(); Musikbett und Mix werden hier erzeugt (alles selbst synthetisiert, frei)."""
import asyncio, json, os, subprocess, sys, time, wave, shutil, math
from pathlib import Path
from multiprocessing import Pool
import numpy as np

HERE = Path(__file__).parent
SR = 44100


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)

def voice_gain(path, target=-16.0, tp=-1.5):
    """Feste Verstaerkung pro Zeile (statt dynamischem loudnorm, das bei kurzen Saetzen den Anfang pumpen laesst)."""
    try:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
        I, P = float(j["input_i"]), float(j["input_tp"])
        if I < -70: return 0.0
        return round(min(target - I, tp - P), 2)
    except Exception:
        return 0.0



def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def tts_andrew(text, mp3, voice, rate, tries=40, pitch="+0Hz", volume="+0%"):
    """Nur Andrew (kein Ersatz). Wiederholt, bis der Dienst erreichbar ist; wechselt den Endpunkt.
    Liefert die Wortzeiten [(Wort, Start, Ende)] relativ zum Zeilenanfang (fuer Untertitel mit Wort-Hervorhebung)."""
    import edge_tts
    import edge_tts.communicate as ec
    orig = getattr(ec, "WSS_URL", None)
    last = None
    for k in range(tries):
        try:
            from edge_tts.constants import TRUSTED_CLIENT_TOKEN as tok
            if orig:
                ec.WSS_URL = orig if k % 2 == 0 else ("wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
                                                      "?Ocp-Apim-Subscription-Key=" + tok)
        except Exception:
            pass
        bounds = []

        async def go():
            try:
                comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume, boundary="WordBoundary")
            except TypeError:
                comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
            with open(mp3, "wb") as f:
                async for ch in comm.stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        st = ch["offset"] / 1e7
                        bounds.append((ch["text"], st, st + ch["duration"] / 1e7))
        try:
            asyncio.run(go())
            if Path(mp3).exists() and Path(mp3).stat().st_size > 2000:
                return bounds
        except Exception as e:
            last = e
            print(f"TTS Versuch {k+1} fehlgeschlagen: {e}", flush=True)
        time.sleep(min(60, 5 + k * 3))
    raise RuntimeError(f"Andrew nicht erreichbar: {last}")


def fake_tts(text, mp3):
    d = max(1.0, len(text.split()) / 2.9)
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{d:.2f}", "-q:a", "9", str(mp3)])
    ws = text.split(); step = d / max(1, len(ws))
    return [(w, i * step, (i + 1) * step) for i, w in enumerate(ws)]


def render_range(args):
    proj, a, b, size, fps, out = args
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": size[0], "height": size[1]})
        pg.goto("file://" + str((HERE / proj / "scene.html").resolve()))
        pg.evaluate("tl=>window.setTimeline(tl)", json.load(open(out / "timeline.json")))
        pg.wait_for_function("window.ready===undefined||window.ready===true", timeout=120000)
        for i in range(a, b):
            pg.evaluate(f"draw({i/fps})")
            pg.screenshot(path=str(out / "fr" / f"{i:05d}.jpg"), type="jpeg", quality=90)
        br.close()


# ---------- Ton ----------

MUSIC = {}
CHORDS = {"minor": [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)],      # Am F C G
          "major": [(48, 52, 55), (55, 59, 62), (57, 60, 64), (53, 57, 60)],      # C G Am F
          "tense": [(57, 60, 64), (57, 60, 65), (53, 57, 60), (52, 56, 59)]}      # Am Am(b6) F E


def music_soft(dur, cfg, prog=None, seed=11, mel=.55):
    """Ruhiges Hintergrundbett fuer Erklaervideos (lo-fi/ambient): weiches E-Piano, Sub-Bass, sanftes Pluck, keine Drums."""
    bpm = cfg.get("bpm", 76); beat = 60 / bpm; bar = beat * 4; n = int(SR * dur); y = np.zeros(n); tt = np.arange(n) / SR
    rng = np.random.default_rng(seed); mid = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = prog or [(60, 64, 67, 71), (57, 60, 64, 67), (53, 57, 60, 64), (55, 59, 62, 65)]   # Cmaj7 Am7 Fmaj7 G7
    def put(sig, t0, g=1.0):
        i = int(t0 * SR); m = min(len(sig), n - i)
        if m > 0 and i >= 0: y[i:i+m] += sig[:m] * g
    def ep(f, l):   # E-Piano: Sinus + leichter Oberton, weicher Anschlag, langes Ausklingen
        t = np.arange(int(l * SR)) / SR
        env = np.minimum(t / .03, 1) * np.exp(-t * 1.1)
        return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2*f*t)*np.exp(-t*3) + .08*np.sin(2*np.pi*3*f*t)*np.exp(-t*5)) * env * (1 + .15*np.sin(2*np.pi*4.5*t))
    nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar; ch = prog[b % 4]
        for k, m in enumerate(ch):   # Akkord leicht gebrochen
            put(ep(mid(m), bar + 1.5), t0 + k * .035, .085)
        put(ep(mid(ch[0]), beat * 2), t0 + beat * 2.5, .05)
        t = np.arange(int(bar * SR)) / SR   # Sub-Bass
        put(np.sin(2*np.pi*mid(ch[0]-24)*t) * np.minimum(t/.08, 1) * np.minimum((bar-t)/.3, 1) * .16, t0)
        if b >= 2:   # dezente Melodie-Tupfer
            for k in range(8):
                if rng.random() < mel: continue
                m = ch[rng.integers(0, 4)] + 12; l3 = .6; e3 = np.exp(-np.arange(int(l3*SR))/SR * 6)
                put(np.sin(2*np.pi*mid(m)*np.arange(int(l3*SR))/SR) * e3 * .03, t0 + k * beat / 2)
    fade = np.minimum(tt / 3.0, 1) * np.clip((dur - tt) / 3.0, 0, 1)
    return y * fade



def music_tense(dur, cfg):
    """Dramatischere Variante (A-Moll): dunkles Streicher-Pad, pulsierender Bass, leiser Herzschlag, Ostinato. Bleibt leise."""
    bpm = cfg.get("bpm", 76); beat = 60 / bpm; bar = beat * 4; n = int(SR * dur); y = np.zeros(n); tt = np.arange(n) / SR
    mid = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [(57, 60, 64), (53, 57, 60), (50, 53, 57), (52, 56, 59)]   # Am F Dm E
    def put(sig, t0, g=1.0):
        i = int(t0 * SR); m = min(len(sig), n - i)
        if m > 0 and i >= 0: y[i:i+m] += sig[:m] * g
    def lp(x, k):
        c = np.cumsum(np.insert(x, 0, 0)); z = (c[k:] - c[:-k]) / k
        return np.concatenate([np.zeros(k - 1), z])
    def saw(f, l):
        t = np.arange(int(l * SR)) / SR
        return sum(np.sin(2*np.pi*f*h*t) / h for h in range(1, 6))
    nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar; ch = prog[b % 4]; l = bar + .6; t = np.arange(int(l * SR)) / SR
        env = np.minimum(t / .9, 1) * np.minimum((l - t) / .6, 1)
        pad = sum(lp(saw(mid(m), l) + saw(mid(m) * 1.004, l), 40) for m in ch) * env * .035
        put(pad, t0)
        for k in range(8):   # pulsierender Bass in Achteln
            l2 = beat / 2 * .95; t2 = np.arange(int(l2 * SR)) / SR
            put(np.sin(2*np.pi*mid(ch[0]-24)*t2) * np.exp(-t2 * 7) * np.minimum(t2/.01, 1) * (.13 if k % 2 == 0 else .08), t0 + k * beat / 2)
        for k in (0, 2):   # leiser Herzschlag
            l3 = .35; t3 = np.arange(int(l3 * SR)) / SR; f = 60 * np.exp(-t3 * 6) + 38
            put(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t3 * 9) * .16, t0 + k * beat)
        for k in range(8):   # Ostinato oben
            m = (ch[0] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 12)[k % 4]; l4 = .5; t4 = np.arange(int(l4 * SR)) / SR
            put(np.sin(2*np.pi*mid(m)*t4) * np.exp(-t4 * 7) * .022, t0 + k * beat / 2)
    fade = np.minimum(tt / 3.0, 1) * np.clip((dur - tt) / 3.0, 0, 1)
    return y * fade


def music_adaptive(dur, cfg):
    """Musik folgt der Stimmung der Zeilen (spec.mood: calm/tense/bright) mit weichen Ueberblendungen (~4 s)."""
    n = int(SR * dur); spans = cfg.get("_moods", [])
    beds = {"calm": lambda: music_soft(dur, cfg),
            "tense": lambda: music_tense(dur, cfg),
            "bright": lambda: music_soft(dur, cfg, prog=[(60, 64, 67, 72), (55, 59, 62, 67), (57, 60, 64, 69), (53, 57, 60, 65)], seed=5, mel=.3)}
    gains = {"calm": 1.0, "tense": 1.65, "bright": 1.0}
    lab = np.zeros(n, dtype=np.int8); keys = list(beds)
    for a, b, m in spans:
        lab[int(a * SR):int(b * SR)] = keys.index(m) if m in keys else 0
    w = int(SR * cfg.get("xfade", 4.0)); y = np.zeros(n)
    for i, k in enumerate(keys):
        e = (lab == i).astype(np.float32)
        if not e.any(): continue
        c = np.cumsum(np.insert(e, 0, 0)); half = w // 2
        lo = np.clip(np.arange(n) - half, 0, n); hi = np.clip(np.arange(n) + half, 0, n)
        e = ((c[hi] - c[lo]) / np.maximum(hi - lo, 1)).astype(np.float32)
        y += beds[k]() * e * gains[k]
    return y


def music_tt(dur, cfg):
    """TikTok-Beat (selbst erzeugt): leiser Kick/Shaker/Bass-Groove + Pluck-Arpeggio. Stimmung je Abschnitt (spec.mood:
    tense/calm/bright, schnelle Ueberblendung), an Abschnitts-Wechseln (spec.cut) kurzer Musik-Stopp + tiefer Bass-Hit.
    Kein Fade-in/-out, damit der Loop nahtlos bleibt."""
    bpm = cfg.get("bpm", 96); beat = 60 / bpm; bar = beat * 4; n = int(SR * dur); tt = np.arange(n) / SR
    mid = lambda m: 440 * 2 ** ((m - 69) / 12); rng = np.random.default_rng(3)
    def mk(): return np.zeros(n)
    def put(y, sig, t0, g=1.0):
        i = int(t0 * SR); m = min(len(sig), n - i)
        if m > 0 and i >= 0: y[i:i+m] += sig[:m] * g
    nb = int(dur / bar) + 2
    drums = mk()
    for b in range(nb):
        t0 = b * bar
        for k in (0, 2.5):   # weicher Kick
            l = .3; t = np.arange(int(l * SR)) / SR; f = 50 + 70 * np.exp(-t * 30)
            put(drums, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11), t0 + k * beat, .32)
        for k in (1, 3):     # leiser Snap
            l = .12; nz = rng.standard_normal(int(l * SR)); ta = np.arange(len(nz)) / SR; nz = np.diff(nz, prepend=0) * np.exp(-ta * 40) * np.minimum(ta / .003, 1)
            put(drums, nz, t0 + k * beat, .03)
        for k in range(8):   # Shaker in Achteln
            l = .06; nz = np.diff(rng.standard_normal(int(l * SR)), prepend=0); ta = np.arange(len(nz)) / SR; e = np.exp(-ta * 70) * np.minimum(ta / .004, 1)
            put(drums, nz * e, t0 + k * beat / 2, .022 if k % 2 else .014)
    PROG = {"tense": [(57, 60, 64), (57, 60, 64), (53, 57, 60), (52, 56, 59)],     # Am Am F E
            "calm":  [(60, 64, 67), (57, 60, 64), (53, 57, 60), (55, 59, 62)],     # C Am F G
            "bright": [(60, 64, 67), (55, 59, 62), (57, 60, 64), (53, 57, 60)]}    # C G Am F
    def bed(prog, bright):
        y = mk()
        for b in range(nb):
            t0 = b * bar; ch = prog[b % 4]
            for k in range(8):   # Bass in Achteln
                l = beat / 2 * .9; t = np.arange(int(l * SR)) / SR
                put(y, (np.sin(2*np.pi*mid(ch[0]-24)*t) + .3*np.sin(2*np.pi*mid(ch[0]-12)*t)) * np.exp(-t * 5) * np.minimum(t / .005, 1), t0 + k * beat / 2, .16 if k % 2 == 0 else .1)
            pat = [0, 1, 2, 1, 2, 0, 1, 2] if not bright else [0, 2, 1, 2, 0, 2, 1, 2]
            for k in range(8):   # Pluck-Arpeggio (Marimba-artig)
                m = ch[pat[k]] + (24 if bright and k % 4 == 3 else 12); l = .35; t = np.arange(int(l * SR)) / SR
                put(y, (np.sin(2*np.pi*mid(m)*t) + .25*np.sin(2*np.pi*4*mid(m)*t)*np.exp(-t*30)) * np.exp(-t * 9), t0 + k * beat / 2, .05)
            if not bright:   # dunkles Pad bei tense
                l = bar + .2; t = np.arange(int(l * SR)) / SR; env = np.minimum(t / .4, 1) * np.minimum((l - t) / .3, 1)
                put(y, sum(np.sin(2*np.pi*mid(m)*t) + .3*np.sin(2*np.pi*2*mid(m)*t) for m in ch) * env * .02, t0)
        return y
    spans = cfg.get("_moods", []); keys = ["tense", "calm", "bright"]
    lab = np.full(n, 1, dtype=np.int8)
    for a, b2, m in spans: lab[int(a * SR):int(b2 * SR)] = keys.index(m) if m in keys else 1
    w = int(SR * cfg.get("xfade", .6)); out = drums.copy()
    for i, k in enumerate(keys):
        e = (lab == i).astype(np.float32)
        if not e.any(): continue
        c = np.cumsum(np.insert(e, 0, 0)); half = w // 2; idx = np.arange(n)
        lo = np.clip(idx - half, 0, n); hi = np.clip(idx + half, 0, n); e = (c[hi] - c[lo]) / np.maximum(hi - lo, 1)
        out += bed(PROG[k], k == "bright") * e
    for tc in cfg.get("_cuts", []):   # Stopp vor dem Abschnitt + Bass-Hit beim Einsatz
        a, b2 = tc - .45, tc
        g = np.ones(n); i0, i1 = int(max(a, 0) * SR), int(min(b2, dur) * SR)
        if i1 > i0:
            ramp = np.linspace(0, 1, i1 - i0); g[i0:i1] = np.where(ramp < .15, 1 - ramp / .15, 0)
            out *= g
        l = 1.2; t = np.arange(int(l * SR)) / SR; f = 38 + 50 * np.exp(-t * 18)
        put(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2), tc, .55)
    return out

def music_ttdark(dur, cfg):
    """Erwachsener TikTok-Beat (selbst erzeugt): moderner Lo-Fi/Trap-Groove in Moll – 808-Bass mit Glide, Clap auf 2/4,
    Hi-Hats in Sechzehnteln mit kleinen Rolls, warmes gefiltertes Pad, sparsame tiefe Rhodes-Toene. Keine Marimba/Pluck-Melodie.
    Eine Stimmung durchgehend (kein Kinder-Dur), spec.cut = kurzer Stopp + 808-Hit. Kein Fade, Loop bleibt nahtlos."""
    bpm = cfg.get("bpm", 140); beat = 60 / bpm; bar = beat * 4; n = int(SR * dur)
    mid = lambda m: 440 * 2 ** ((m - 69) / 12); rng = np.random.default_rng(11)
    out = np.zeros(n)
    def put(sig, t0, g=1.0):
        i = int(t0 * SR); m = min(len(sig), n - i)
        if m > 0 and i >= 0: out[i:i+m] += sig[:m] * g
    def lp(x, a=.08):   # einfacher Tiefpass (warm)
        y = np.zeros_like(x); acc = 0.0
        for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
        return y
    # Halftime-Trap: 1 Akkord pro Takt, Am – F – C – G (i–VI–III–VII), tief und warm
    PROG = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
    nb = int(dur / bar) + 2
    # Pad einmal pro Akkord vorberechnen
    padc = {}
    for ch in PROG:
        l = bar + .25; t = np.arange(int(l * SR)) / SR
        sig = sum(np.sin(2*np.pi*mid(m)*t*(1+d)) + .45*np.sin(2*np.pi*2*mid(m)*t*(1-d)) for m in ch for d in (-.003, .003))
        env = np.minimum(t / .25, 1) * np.minimum((l - t) / .25, 1)
        padc[ch] = lp(sig * env, .06)
    for b in range(nb):
        t0 = b * bar; ch = PROG[b % 4]
        put(padc[ch], t0, .018)
        # 808: Grundton, lang, mit Pitch-Glide beim Einsatz
        for k, ln in ((0, 1.5), (2.5, .9)):
            l = ln * beat; t = np.arange(int(l * SR)) / SR; f0 = mid(ch[0] - 24)
            f = f0 * (1 + .9 * np.exp(-t * 40)); ph = 2*np.pi*np.cumsum(f)/SR
            sig = np.tanh(2.2*np.sin(ph)) * np.exp(-t * 1.6) * np.minimum(t / .004, 1) * np.minimum((l - t) / .02, 1)
            put(sig, t0 + k * beat, .2)
        # Kick unter dem 808
        for k in (0, 2.5):
            l = .22; t = np.arange(int(l * SR)) / SR; f = 45 + 110 * np.exp(-t * 35)
            put(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t * 14), t0 + k * beat, .3)
        # Clap auf 2 und 4 (Halftime: Schlag 3)
        for k in (2,):
            l = .25; nz = rng.standard_normal(int(l * SR)); ta = np.arange(len(nz)) / SR
            env = (np.exp(-ta * 22) + .6*np.exp(-np.maximum(ta-.012,0)*60)*(ta>.012)) * np.minimum(ta/.002,1)
            put(np.diff(nz, prepend=0) * env, t0 + k * beat, .045)
        # Hi-Hats in Sechzehnteln, jeden 2. Takt ein Roll
        for k in range(16):
            l = .035; nz = np.diff(np.diff(rng.standard_normal(int(l * SR)), prepend=0), prepend=0); ta = np.arange(len(nz)) / SR
            put(nz * np.exp(-ta * 140), t0 + k * beat / 4, .010 if k % 2 else .016)
        if b % 2 == 1:
            for r in range(6):
                l = .02; nz = np.diff(np.diff(rng.standard_normal(int(l * SR)), prepend=0), prepend=0); ta = np.arange(len(nz)) / SR
                put(nz * np.exp(-ta * 200), t0 + 3.5 * beat + r * beat / 12, .008 + r * .0015)
        # sparsame tiefe Rhodes-Toene (nur Grundton/Terz, leise, dunkel)
        for k, m in ((0, ch[1] - 12), (1.5, ch[2] - 12)):
            l = 1.2; t = np.arange(int(l * SR)) / SR
            sig = (np.sin(2*np.pi*mid(m)*t) + .35*np.sin(2*np.pi*2*mid(m)*t)*np.exp(-t*6)) * np.exp(-t * 2.5) * np.minimum(t / .01, 1)
            put(sig, t0 + k * beat, .03)
    for tc in cfg.get("_cuts", []):
        a, b2 = tc - .4, tc; g = np.ones(n); i0, i1 = int(max(a, 0) * SR), int(min(b2, dur) * SR)
        if i1 > i0:
            ramp = np.linspace(0, 1, i1 - i0); g[i0:i1] = np.where(ramp < .15, 1 - ramp / .15, 0); out *= g
        l = 1.4; t = np.arange(int(l * SR)) / SR; f = mid(33) * (1 + .8 * np.exp(-t * 30))
        put(np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)) * np.exp(-t * 2), tc, .32)
    return out

def music_bed(dur, cfg):
    """Selbst synthetisiertes Musikbett: Pad-Akkorde, Bass, Kick/Hi-Hat, Pluck-Arpeggio. Frei von Rechten."""
    if cfg.get("style") == "ttdark": return music_ttdark(dur, cfg)
    if cfg.get("style") == "tt": return music_tt(dur, cfg)
    if cfg.get("style") == "adaptive": return music_adaptive(dur, cfg)
    if cfg.get("style") == "soft": return music_soft(dur, cfg)
    bpm = cfg.get("bpm", 100); mood = cfg.get("mood", "minor"); energy = cfg.get("energy", .7)
    n = int(SR * dur); y = np.zeros(n); tt = np.arange(n) / SR; beat = 60 / bpm; bar = beat * 4
    rng = np.random.default_rng(7)
    mid = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = CHORDS.get(mood, CHORDS["minor"])

    def put(sig, t0, g=1.0):
        i = int(t0 * SR); m = min(len(sig), n - i)
        if m > 0 and i >= 0: y[i:i+m] += sig[:m] * g

    def osc(f, l, kind="saw"):
        t = np.arange(int(l * SR)) / SR
        if kind == "sine": return np.sin(2 * np.pi * f * t)
        return sum(np.sin(2 * np.pi * f * h * t) / h * (1 if h < 4 else .5) for h in range(1, 7))

    def lowpass(x, k):
        c = np.cumsum(np.insert(x, 0, 0)); z = (c[k:] - c[:-k]) / k
        return np.concatenate([np.zeros(k - 1), z])

    nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar; ch = prog[b % len(prog)]
        # Pad
        l = bar + .3; env = np.minimum(np.arange(int(l*SR))/SR/.6, 1) * np.minimum((l - np.arange(int(l*SR))/SR)/.5, 1)
        pad = sum(lowpass(osc(mid(m), l) * .5 + osc(mid(m) * 1.003, l) * .5, 30) for m in ch) * env * .10
        put(pad, t0)
        # Bass (Grundton, Achtel-Puls)
        for k in range(8):
            l2 = beat / 2 * .9; e2 = np.exp(-np.arange(int(l2*SR))/SR * 6)
            put(osc(mid(ch[0] - 24), l2, "sine") * e2 * .32 * energy, t0 + k * beat / 2)
        # Pluck-Arpeggio (16tel, ab Takt 2)
        if b >= 1:
            for k in range(16):
                if rng.random() < .25: continue
                m = ch[k % 3] + 12 * (1 + (k // 3) % 2); l3 = .35; e3 = np.exp(-np.arange(int(l3*SR))/SR * 14)
                put(osc(mid(m), l3, "sine") * e3 * .07 * energy, t0 + k * beat / 4)
        # Drums (ab Takt 2): Kick 1+3, Snare-artig 2+4 (leise), Hats auf Achteln
        if b >= 1 and energy > .3:
            for k in range(4):
                tk = t0 + k * beat
                if k % 2 == 0:
                    lk = .3; tq = np.arange(int(lk*SR))/SR; f = 45 + 90 * np.exp(-tq * 30)
                    put(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tq * 9) * .55 * energy, tk)
                else:
                    ls = .2; nz = rng.normal(0, 1, int(ls*SR)); nz = nz - lowpass(nz, 6)
                    put(nz * np.exp(-np.arange(len(nz))/SR * 22) * .10 * energy, tk)
                for hh in (0, .5):
                    lh = .05; nz = rng.normal(0, 1, int(lh*SR)); nz = nz - lowpass(nz, 3)
                    put(nz * np.exp(-np.arange(len(nz))/SR * 80) * .05 * energy, tk + hh * beat)
    fade = np.minimum(tt / 1.5, 1) * np.clip((dur - tt) / 2.0, 0, 1)
    return y * fade


def synth(events, dur, music=True):
    n = int(SR * dur)
    rng = np.random.default_rng(3)
    L = np.zeros(n); R = np.zeros(n)
    tt = np.arange(n) / SR

    def add(sig, t0, pan=0.0, g=1.0):
        i = int(t0 * SR); m = min(len(sig), n - i)
        if m <= 0 or i < 0: return
        L[i:i+m] += sig[:m] * g * (1 - max(0, pan)); R[i:i+m] += sig[:m] * g * (1 + min(0, pan))

    def env(l, a=.005, r=None):
        t = np.arange(int(l * SR)) / SR; r = r or l
        return np.minimum(t / a, 1) * np.exp(-t * (5 / r))

    def lp(x, k):
        c = np.cumsum(np.insert(x, 0, 0)); y = (c[k:] - c[:-k]) / k
        return np.concatenate([np.zeros(k - 1), y])

    def tone(f, l, g=1, a=.005, r=None, harm=(1,)):
        t = np.arange(int(l * SR)) / SR
        return sum(np.sin(2 * np.pi * f * h * t) / h for h in harm) * env(l, a, r) * g

    music_arr = music_bed(dur, MUSIC) if music else np.zeros(n)
    VARY = bool(MUSIC.get("_vary"))
    base_tone, base_add = tone, add
    for idx, e in enumerate(events):
        k, t = e["k"], e["t"]
        if VARY:  # jede Instanz klingt etwas anders (Tonhoehe, Pegel, Stereo) -> weniger monoton
            vr = np.random.default_rng(1000 + idx)
            pf = float(vr.uniform(.82, 1.22)); gf = float(vr.uniform(.6, 1.0)); pn = float(vr.uniform(-.45, .45)); var = int(vr.integers(0, 3))
            tone = lambda f, l, g=1, a=.005, r=None, harm=(1,), _b=base_tone, _p=pf: _b(f * _p, l, g, a, r, harm)
            add = lambda sig, t0, pan=None, g=1.0, _b=base_add, _g=gf, _n=pn: _b(sig, t0, _n if pan is None else pan * .5 + _n * .5, g * _g)
            if k == "pop" and var == 1: k = "blip"
            elif k == "pop" and var == 2: k = "bubble"
            elif k == "swish" and var == 2: k = "brush"
            elif k == "tick" and var == 1: k = "click"
            elif k == "ding" and var == 1: k = "bell"
            elif k == "whoosh" and var == 2: k = "air"
        else:
            tone, add = base_tone, base_add
        if k == "whoosh":
            d = e.get("d", 1.6); w = rng.normal(0, 1, int(d*SR)); x = np.convolve(w, np.ones(40)/40, "same")
            add(x * np.sin(np.linspace(0, np.pi, len(x)))**2 * .5, t, .3)
        elif k == "tap":
            add(tone(90, .25, 1.0, .002, .1), t); add(np.diff(lp(rng.normal(0, 1, int(.03*SR)), 2), prepend=0) * .9, t)
        elif k == "beep":
            add(tone(e.get("f", 1568), .1, .5, .003, .1), t)
        elif k == "chime":
            for i, f in enumerate((880, 1108.7, 1318.5, 1760)): add(tone(f, .9, .35, .004, .5, (1, 2, 3)), t + i*.07)
        elif k == "riser":
            rl = e.get("d", 1.7); tq = np.arange(int(rl*SR)) / SR; f = 200 * np.exp(tq/rl*np.log(1800/200))
            add(np.sin(np.cumsum(2*np.pi*f/SR)) * (tq/rl)**2 * .25, t)
            nz = rng.normal(0, 1, int(rl*SR)); nz = nz - lp(nz, 30); add(nz * (tq/rl)**3 * .35, t)
        elif k == "impact":
            add(tone(55, 1.2, 1.0, .002, .5), t); add(lp(rng.normal(0, 1, int(.5*SR)), 8) * env(.5, .001, .2) * .8, t)
        elif k == "shimmer":
            add(tone(3136, .6, .2, .002, .4, (1, 2)), t)
        elif k == "pop":
            tq = np.arange(int(.25*SR)) / SR; f = 700*np.exp(-tq*9) + 200
            add(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tq*14) * .9, t)
            for i, ff in enumerate((1568, 2349)): add(tone(ff, .5, .25, .003, .3), t + .05 + i*.06)
        elif k == "tick":
            add(tone(e.get("f", 2400), .04, .35, .001, .02), t)
        elif k == "cash":
            add(np.diff(lp(rng.normal(0, 1, int(.06*SR)), 2), prepend=0) * .8, t)
            for i, f in enumerate((2093, 2637)): add(tone(f, .7, .35, .002, .4, (1, 2, 3)), t + .06 + i * .09)
        elif k == "error":
            for i in range(2): add(tone(180, .16, .5, .003, .14, (1, 3, 5)), t + i * .19)
        elif k == "thud":
            add(tone(70, .5, 1.0, .002, .2), t); add(lp(rng.normal(0, 1, int(.12*SR)), 20) * env(.12, .001, .05) * .9, t)
        elif k == "swish":
            d = e.get("d", .45); w = rng.normal(0, 1, int(d*SR)); x = w - lp(w, 12)
            add(x * np.sin(np.linspace(0, np.pi, len(x)))**3 * .35, t, e.get("pan", 0))
        elif k == "type":
            for i in range(int(e.get("n", 8))): add(np.diff(lp(rng.normal(0, 1, int(.012*SR)), 2), prepend=0) * .5, t + i * .07 + rng.random() * .02)
        elif k == "heartbeat":
            for i in range(int(e.get("n", 2))): add(tone(55, .25, 1, .003, .1), t + i * .8); add(tone(50, .25, .7, .003, .1), t + i * .8 + .22)
        elif k == "blip":
            tq = np.arange(int(.12*SR)) / SR; f = 900 + 900 * tq / .12
            add(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tq*25) * .5, t)
        elif k == "bubble":
            tq = np.arange(int(.18*SR)) / SR; f = 300 + 1400 * (tq / .18) ** 1.5
            add(np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*tq/.18) * .45, t)
        elif k == "brush":
            d = e.get("d", .4) * 1.3; w = rng.normal(0, 1, int(d*SR)); x = lp(w, 4) - lp(w, 40)
            add(x * np.sin(np.linspace(0, np.pi, len(x)))**2 * .6, t)
        elif k == "click":
            add(np.diff(lp(rng.normal(0, 1, int(.01*SR)), 2), prepend=0) * .7, t); add(tone(1200, .03, .25, .001, .015), t)
        elif k == "bell":
            for i, f in enumerate((1046.5, 1568)): add(tone(f, 1.4, .28, .002, .9, (1, 2.76, 5.4)), t + i*.08)
        elif k == "air":
            d = e.get("d", 1.0); w = rng.normal(0, 1, int(d*SR)); x = lp(w, 90)
            add(x * np.sin(np.linspace(0, np.pi, len(x)))**1.5 * 1.6, t)
        elif k == "coin":
            for i in range(int(e.get("n", 3))): add(tone(2600 + 300 * (i % 2), .25, .25, .001, .12, (1, 2.4)), t + i * .09)
        elif k == "paper":
            d = .3; w = rng.normal(0, 1, int(d*SR)); x = w - lp(w, 3)
            add(x * np.exp(-np.arange(len(x))/SR*12) * .35, t)
        elif k == "ding":
            for i, f in enumerate((1318.5, 1760, 2637)): add(tone(f, 1.2, .3, .003, .7, (1, 2)), t + i*.05)
    return L, R, music_arr


def wavwrite(path, L, R):
    m = max(np.abs(L).max(), np.abs(R).max(), 1e-9); a = (np.stack([L, R], 1) / m * .8 * 32767).astype(np.int16)
    w = wave.open(str(path), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes()); w.close()


def main():
    proj = sys.argv[1]
    fake = "--fake-tts" in sys.argv
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    cfg = json.load(open(HERE / proj / "project.json", encoding="utf-8"))
    out = Path("output") / ("mg_" + proj); shutil.rmtree(out, ignore_errors=True)
    (out / "fr").mkdir(parents=True); (out / "voice").mkdir()
    size, fps = cfg["size"], cfg["fps"]
    mcfg = cfg.get("music", {})
    MUSIC.update(mcfg if isinstance(mcfg, dict) else {})
    MUSIC["_off"] = mcfg is False
    MUSIC["_vary"] = bool(cfg.get("sfx_vary", mcfg is False))
    # 1) Stimme
    t = cfg.get("lead", 0.3); lines = []
    for i, ln in enumerate(cfg["lines"]):
        mp3 = out / "voice" / f"{i:02d}.mp3"
        if fake: words = fake_tts(ln["text"], mp3)
        else: words = tts_andrew(ln["text"], mp3, cfg["voice"], ln.get("rate", cfg["rate"]), pitch=ln.get("pitch", "+0Hz"), volume=ln.get("volume", "+0%"))  # Emotion je Zeile: rate/pitch/volume
        d = dur_of(mp3)
        start = max(t + ln.get("pause", 0), ln.get("min_start", 0))  # pause = dramatische Pause vor der Zeile
        lines.append({"text": ln["text"], "start": round(start, 3), "end": round(start + d, 3), "file": str(mp3),
                      "spec": ln.get("spec"), "words": [[w, round(a, 3), round(b, 3)] for w, a, b in words]})
        t = start + d + cfg.get("gap", .3)
        print(f"Zeile {i}: {start:.2f}-{start+d:.2f}  {ln['text']}", flush=True)
    total = round(lines[-1]["end"] + cfg.get("tail", 1.5), 2)
    mood = "calm"; MUSIC["_moods"] = []
    for j, l in enumerate(lines):   # Stimmung gilt bis zur naechsten Zeile
        mood = (l.get("spec") or {}).get("mood", mood)
        MUSIC["_moods"].append((l["start"], lines[j+1]["start"] if j + 1 < len(lines) else total, mood))
    MUSIC["_cuts"] = [l["start"] for l in lines if (l.get("spec") or {}).get("cut")]
    tl = {"lines": [{k: v for k, v in l.items() if k != "file"} for l in lines], "dur": total}
    if "--limit" in sys.argv:  # nur die ersten N Sekunden rendern (Test)
        lim = float(sys.argv[sys.argv.index("--limit") + 1]); total = min(total, lim); tl["dur"] = total
    json.dump(tl, open(out / "timeline.json", "w"), ensure_ascii=False)
    if "--stills" in sys.argv:  # nur Einzelbilder zu Zeitpunkten (schneller Test): --stills 1,5.5,12
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            br = p.chromium.launch(); pg = br.new_page(viewport={"width": size[0], "height": size[1]})
            pg.goto("file://" + str((HERE / proj / cfg["scene"]).resolve())); pg.evaluate("tl=>window.setTimeline(tl)", tl)
            pg.wait_for_function("window.ready===undefined||window.ready===true", timeout=120000)
            print("SFX:", pg.evaluate("window.sfxEvents()")[:40])
            for x in ts:
                pg.evaluate(f"draw({x})"); pg.screenshot(path=str(out / f"still_{x:06.2f}.jpg"), type="jpeg", quality=85)
            br.close()
        print("STILLS", out, f"Gesamtdauer {total}s"); return
    # 2) Ereignisse (SFX) aus der Szene
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": size[0], "height": size[1]})
        pg.goto("file://" + str((HERE / proj / cfg["scene"]).resolve())); pg.evaluate("tl=>window.setTimeline(tl)", tl)
        events = pg.evaluate("window.sfxEvents()"); br.close()
    # 3) Frames parallel
    nfr = int(total * fps); step = math.ceil(nfr / workers)
    jobs = [(proj, a, min(nfr, a + step), size, fps, out) for a in range(0, nfr, step)]
    t0 = time.time()
    with Pool(workers) as pool: pool.map(render_range, jobs)
    print(f"{nfr} Frames in {time.time()-t0:.0f}s", flush=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(out / "fr" / "%05d.jpg"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(cfg.get("crf", 19)), "-preset", "slow", str(out / "video.mp4")])
    # 4) Ton: SFX+Musik synthetisieren, Stimme platzieren, mischen (Musik unter der Stimme abgesenkt)
    L, R, music = synth(events, total, music=not MUSIC.get("_off"))
    wavwrite(out / "sfx.wav", L, R)
    mus = np.stack([music, music], 1); wavwrite(out / "music.wav", mus[:, 0], mus[:, 1])
    ins = []; fl = []
    for i, l in enumerate(lines):
        ins += ["-i", l["file"]]
        fl.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,volume={voice_gain(l['file'])}dB,adelay={int(l['start']*1000)}|{int(l['start']*1000)}[v{i}]")
    mix = "".join(f"[v{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0,apad=whole_dur={total}[voice]"  # apad: sonst schneidet der Mix die letzte Zeile ab
    n = len(lines)
    graph = ";".join(fl + [mix,
        f"[voice]asplit=2[vo][vsc]",
        f"[{n}:a]volume={0 if MUSIC.get('_off') else MUSIC.get('gain', 0.55)}[music]",
        f"[{n+1}:a]volume={cfg.get('sfx_gain', 0.8)}[sfx]",
        f"[music][vsc]sidechaincompress=threshold=0.03:ratio={MUSIC.get('duck_ratio', 8)}:attack=20:release=300[ducked]",
        f"[vo][ducked][sfx]amix=inputs=3:normalize=0,alimiter=limit=0.95[a]"])
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", str(out / "music.wav"), "-i", str(out / "sfx.wav"),
         "-filter_complex", graph, "-map", "[a]", "-t", f"{total}", "-c:a", "aac", "-b:a", "192k", str(out / "audio.m4a")])
    final = Path("output") / f"{proj}_final.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out / "video.mp4"), "-i", str(out / "audio.m4a"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", str(final)])
    shutil.rmtree(out / "fr", ignore_errors=True)
    print("FERTIG", final, f"{total}s", flush=True)


if __name__ == "__main__":
    main()
