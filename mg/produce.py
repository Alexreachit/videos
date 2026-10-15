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


def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def tts_andrew(text, mp3, voice, rate, tries=40):
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
                comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
            except TypeError:
                comm = edge_tts.Communicate(text, voice, rate=rate)
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


def music_bed(dur, cfg):
    """Selbst synthetisiertes Musikbett: Pad-Akkorde, Bass, Kick/Hi-Hat, Pluck-Arpeggio. Frei von Rechten."""
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
    for e in events:
        k, t = e["k"], e["t"]
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
    MUSIC.update(cfg.get("music", {}))
    # 1) Stimme
    t = cfg.get("lead", 0.3); lines = []
    for i, ln in enumerate(cfg["lines"]):
        mp3 = out / "voice" / f"{i:02d}.mp3"
        if fake: words = fake_tts(ln["text"], mp3)
        else: words = tts_andrew(ln["text"], mp3, cfg["voice"], cfg["rate"])
        d = dur_of(mp3)
        start = max(t, ln.get("min_start", 0))
        lines.append({"text": ln["text"], "start": round(start, 3), "end": round(start + d, 3), "file": str(mp3),
                      "spec": ln.get("spec"), "words": [[w, round(a, 3), round(b, 3)] for w, a, b in words]})
        t = start + d + cfg.get("gap", .3)
        print(f"Zeile {i}: {start:.2f}-{start+d:.2f}  {ln['text']}", flush=True)
    total = round(lines[-1]["end"] + cfg.get("tail", 1.5), 2)
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
    L, R, music = synth(events, total)
    wavwrite(out / "sfx.wav", L, R)
    mus = np.stack([music, music], 1); wavwrite(out / "music.wav", mus[:, 0], mus[:, 1])
    ins = []; fl = []
    for i, l in enumerate(lines):
        ins += ["-i", l["file"]]
        fl.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=7,adelay={int(l['start']*1000)}|{int(l['start']*1000)}[v{i}]")
    mix = "".join(f"[v{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0[voice]"
    n = len(lines)
    graph = ";".join(fl + [mix,
        f"[voice]asplit=2[vo][vsc]",
        f"[{n}:a]volume=0.55[music]",
        f"[{n+1}:a]volume=0.8[sfx]",
        f"[music][vsc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[ducked]",
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
