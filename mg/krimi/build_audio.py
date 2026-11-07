# Baut ep01_voice_cut.wav + ep01_timing.json aus den ElevenLabs-Aufnahmen (Teile wiederverwenden, interne Pausen kuerzen)
import json, subprocess, numpy as np
SR = 48000
def load(p):
    a = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(a, np.float32).copy()
A = load("ep01_voice.mp3"); B = load("ep01_voice_b.mp3")
CLIPS = [(A, 0.0, 3.915), (A, 5.106, 11.546), (A, 12.775, 18.986), (A, 20.30, 26.46),   # Saetze 1-4 aus der ersten Aufnahme
         (B, 0.0, 4.93), (B, 5.87, 15.90), (B, 16.86, 30.955)]                            # Saetze 5-7 neu gesprochen
FIXED = [0.6, 5.065, 12.055, 18.816, 25.527]   # Starts 1-5 bleiben gleich -> Schnitte 1-5 bleiben gleich
def cap_pauses(x, maxp=.36, keep=.30):
    env = np.convolve(np.abs(x), np.ones(240) / 240, mode="same"); quiet = env < .006
    out = []; i = 0; n = len(x)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if (j - i) / SR > maxp and i > SR * .2 and j < n - SR * .2:
                k = int(keep * SR); out.append(x[i:i + k // 2]); out.append(x[j - k // 2:j])
            else: out.append(x[i:j])
            i = j
        else:
            j = i
            while j < n and not quiet[j]: j += 1
            out.append(x[i:j]); i = j
    return np.concatenate(out)
segs = []; parts = []; t = 0
for k, (src, a, b) in enumerate(CLIPS):
    clip = cap_pauses(src[int(a * SR):int(b * SR)])
    start = FIXED[k] if k < len(FIXED) else t + .5
    segs.append(dict(i=k, start=round(start, 3), end=round(start + len(clip) / SR, 3))); parts.append((start, clip)); t = start + len(clip) / SR
DUR = round(t + 1.6, 3); out = np.zeros(int(DUR * SR) + SR)
for s, c in parts: n0 = int(s * SR); out[n0:n0 + len(c)] += c
out = out[:int(DUR * SR)]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "ep01_voice_cut.wav"], input=out.astype(np.float32).tobytes(), check=True)
json.dump(dict(fps=30, duration=DUR, segments=segs), open("ep01_timing.json", "w"), indent=1)
print(segs, DUR)
