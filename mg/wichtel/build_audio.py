# Folge 2: ElevenLabs-Aufnahme(n) -> ep01_voice_cut.wav + ep01_timing.json (Saetze an den <break>-Pausen trennen, interne Pausen kuerzen)
# python3 build_audio02.py ep02_voice.mp3 [weitere.mp3 ...]   (mehrere Dateien = Saetze der Reihe nach)
import json, re, subprocess, sys, numpy as np
SR = 48000
raw = open("ep01_script.txt", encoding="utf-8").read()
NSEG = len(re.split(r'<break[^>]*/>', raw))
def load(p):
    a = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(a, np.float32).copy()
def split(x, minp=.85):
    env = np.convolve(np.abs(x), np.ones(480) / 480, mode="same"); q = env < .006
    segs = []; i = 0; n = len(x); start = None; last_voice = 0
    while i < n:
        if not q[i]:
            if start is None: start = i
            last_voice = i; i += 1; continue
        j = i
        while j < n and q[j]: j += 1
        if start is not None and (j - i) / SR >= minp: segs.append((start, last_voice + 1)); start = None
        i = j
    if start is not None: segs.append((start, last_voice + 1))
    segs = [(a, b) for a, b in segs if (b - a) / SR > .25]
    while len(segs) > NSEG:   # zu viele Teile -> die beiden mit der kuerzesten Pause dazwischen zusammenlegen
        k = min(range(len(segs) - 1), key=lambda j: segs[j + 1][0] - segs[j][1]); segs[k:k + 2] = [(segs[k][0], segs[k + 1][1])]
    return [x[max(0, a - int(.03 * SR)):min(n, b + int(.08 * SR))] for a, b in segs]
def cap_pauses(x, maxp=.36, keep=.30):
    env = np.convolve(np.abs(x), np.ones(240) / 240, mode="same"); quiet = env < .006
    out = []; i = 0; n = len(x)
    while i < n:
        j = i
        if quiet[i]:
            while j < n and quiet[j]: j += 1
            if (j - i) / SR > maxp: k = int(keep * SR); out += [x[i:i + k // 2], x[j - k // 2:j]]
            else: out.append(x[i:j])
        else:
            while j < n and not quiet[j]: j += 1
            out.append(x[i:j])
        i = j
    return np.concatenate(out)
clips = []
for p in sys.argv[1:]: clips += split(load(p))
print("Saetze gefunden:", len(clips), "erwartet:", NSEG)
assert len(clips) == NSEG, [round(len(c) / SR, 2) for c in clips]
segs = []; t = .6; parts = []
for k, c in enumerate(clips):
    c = cap_pauses(c); segs.append(dict(i=k, start=round(t, 3), end=round(t + len(c) / SR, 3))); parts.append((t, c)); t += len(c) / SR + .55
DUR = round(t + 1.2, 3); out = np.zeros(int(DUR * SR) + SR)
for s, c in parts: n0 = int(s * SR); out[n0:n0 + len(c)] += c
out = out[:int(DUR * SR)]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "ep01_voice_cut.wav"], input=out.astype(np.float32).tobytes(), check=True)
json.dump(dict(fps=12, duration=DUR, segments=segs), open("ep01_timing.json", "w"), indent=1)
print(segs, DUR)
