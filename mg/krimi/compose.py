# Nebelstein – Schnitt: stummes Blender-Video + Stimme + eigene Musik/SFX (numpy, selbst erzeugt) + Untertitel/Overlays (ASS) -> MP4
# python3 compose.py <silent.mp4> <out.mp4>
import json, re, subprocess, sys, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
T = json.load(open(os.path.join(HERE, "ep01_timing.json"))); SEG = T["segments"]; DUR = T["duration"]; FPS = T["fps"]
F = lambda t: int(round(t * FPS)); CUT = [0] + [F(s["start"]) - 5 for s in SEG[1:]] + [F(DUR)]
def segt(i, frac): return SEG[i]["start"] + frac * (SEG[i]["end"] - SEG[i]["start"])
raw = open(os.path.join(HERE, "ep01_script.txt"), encoding="utf-8").read()
TEXTS = [re.sub(r"\s+", " ", t).strip() for t in re.split(r'<break[^>]*/>', raw)]
assert len(TEXTS) == len(SEG), (len(TEXTS), len(SEG))

def wav_read(p):
    a = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(a, np.float32).copy()
VOICE = wav_read(os.path.join(HERE, "ep01_voice_cut.wav")); N = int((DUR + .5) * SR)
VOICE = np.pad(VOICE, (0, max(0, N - len(VOICE))))[:N]

# ---------------------------------------------------------------- Wort-Timings (Silben-proportional, an Sprechpausen ausgerichtet)
env = np.convolve(np.abs(VOICE), np.ones(480) / 480, mode="same"); speech = env > 0.012
def words_for(i):
    s0, s1 = SEG[i]["start"], SEG[i]["end"]; ws = TEXTS[i].replace("„", "").replace("“", "").split()
    def wt(w):
        v = len(re.findall(r"[aeiouäöüyAEIOUÄÖÜ]+", w)) or 1; p = 2.2 if w[-1] in ".?!…" else (1.0 if w[-1] in ",:" else 0)
        return v, p
    tot = sum(a + b for a, b in (wt(w) for w in ws)); t = s0; out = []
    for w in ws:
        a, b = wt(w); d = (s1 - s0) * a / tot; out.append((w, t, t + d)); t += d + (s1 - s0) * b / tot
    return out
WORDS = [words_for(i) for i in range(len(SEG))]

# ---------------------------------------------------------------- ASS-Untertitel + Overlays
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h}:{m:02d}:{s:05.2f}"
FD = os.path.join(HERE, "fonts")
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
       "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Lilita One,84,&H00FFFFFF,&H00FFFFFF,&H00301A14,&H96000000,0,0,0,0,100,100,1,0,1,7,4,2,60,60,560,1",
       "Style: Title,Cinzel Decorative Black,118,&H006BD8FF,&H00FFFFFF,&H00241612,&H64000000,0,0,0,0,100,100,4,0,1,6,6,8,40,40,330,1",
       "Style: Sub,Lilita One,58,&H00FFFFFF,&H00FFFFFF,&H00241612,&H64000000,0,0,0,0,100,100,3,0,1,5,3,8,40,40,470,1",
       "Style: Box,Lilita One,62,&H00FFFFFF,&H00FFFFFF,&H00382218,&HD0382218,0,0,0,0,100,100,1,0,3,18,0,7,0,0,0,1",
       "Style: Big,Lilita One,96,&H006BD8FF,&H00FFFFFF,&H00241612,&H64000000,0,0,0,0,100,100,2,0,1,7,4,8,40,40,300,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
def ev(a, b, style, txt, layer=0): ass.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{txt}")
GOLD = r"{\c&H6BD8FF&}"; WH = r"{\c&HFFFFFF&}"
for i, ws in enumerate(WORDS):
    # Gruppen a 3 Woertern; aktuelles Wort gold + leicht groesser
    if i == 0: continue  # Titelkarte statt Untertitel
    groups = []; g = []
    for w in ws:
        g.append(w)
        if len(g) == 3 or w[0][-1] in ".?!…": groups.append(g); g = []
    if g: groups.append(g)
    for gi, g in enumerate(groups):
        g_end = groups[gi + 1][0][1] if gi + 1 < len(groups) else g[-1][2] + .25
        for wi, (w, a, b) in enumerate(g):
            nb = g[wi + 1][1] if wi + 1 < len(g) else g_end
            parts = []
            for wj, (w2, _, _) in enumerate(g):
                w2u = w2.upper()
                parts.append((GOLD + r"{\fscx108\fscy108}" + w2u + r"{\fscx100\fscy100}" + WH) if wj == wi else w2u)
            pop = r"{\t(0,90,\fscx106\fscy106)\t(90,180,\fscx100\fscy100)}" if wi == 0 else ""
            ev(a, nb, "Cap", pop + " ".join(parts))
# Titelkarte
ev(.25, SEG[0]["end"] + .5, "Title", r"{\fad(500,400)\blur1.2}NEBELSTEIN", 2)
ev(.9, SEG[0]["end"] + .5, "Sub", r"{\fad(400,400)}FALL 1  ·  DER UHRMACHER", 2)
# Uhrzeit-Einblendung beim Stehenbleiben
stop_t = (int(round(segt(1, .72) * FPS))) / FPS
ev(stop_t, SEG[1]["end"] + .3, "Big", r"{\fad(80,300)\an8\pos(540,250)\t(0,120,\fscx115\fscy115)\t(120,260,\fscx100\fscy100)}00:13", 3)
# Laterne / Luege
ev(segt(3, .62), SEG[3]["end"] + .2, "Box", r"{\an5\pos(540,330)\fad(150,200)}  LATERNE FLACKERT = LÜGE  ", 3)
# Mitmachen
c0 = SEG[5]["start"]
ev(c0 + .1, SEG[5]["end"] + .4, "Box", r"{\an5\pos(540,300)\fad(200,200)\t(0,150,\fscx110\fscy110)\t(150,300,\fscx100\fscy100)}  1. FOLGEN  ", 3)
ev(segt(5, .22), SEG[5]["end"] + .4, "Box", r"{\an5\pos(540,420)\fad(200,200)}  2. KOMMENTIERE: »ICH BIN DABEI«  ", 3)
ev(segt(5, .55), SEG[5]["end"] + .4, "Sub", r"{\an5\pos(540,540)\fad(200,200)}= DU WOHNST IN NEBELSTEIN", 3)
# Abstimmung
v0 = SEG[6]["start"]
ev(v0 + .1, DUR, "Big", r"{\fad(200,0)\an8\pos(540,190)}WAS ZUERST?", 3)
for k, (lab, frac) in enumerate((("A  ·  DIE UHR", .30), ("B  ·  DER RABE", .42), ("C  ·  DER SCHLÜSSEL", .58))):
    ev(segt(6, frac), DUR, "Box", r"{\an5\pos(540," + str(360 + k * 120) + r")\fad(150,0)\t(0,120,\fscx112\fscy112)\t(120,240,\fscx100\fscy100)}  " + lab + "  ", 3)
ev(segt(6, .80), DUR, "Sub", r"{\an5\pos(540,760)\fad(200,0)}SCHREIB A, B ODER C IN DIE KOMMENTARE", 3)
open(os.path.join(HERE, "ep01.ass"), "w", encoding="utf-8").write("\n".join(ass) + "\n")

# ---------------------------------------------------------------- Musik (eigene Komposition, d-Moll, mysterioes)
t = np.arange(N) / SR; rng = np.random.default_rng(3)
def note(f): return 440 * 2 ** ((f - 69) / 12)
def adsr(n, a=.01, r=.3):
    e = np.ones(n); ka = max(1, int(a * SR)); kr = max(1, int(r * SR)); e[:ka] = np.linspace(0, 1, ka); e[-kr:] *= np.linspace(1, 0, kr); return e
mus = np.zeros(N)
# Drone (D2 + A2, leicht verstimmt, langsam atmend)
for f, g in ((note(38), .16), (note(45), .09), (note(50), .05)):
    for det in (-.6, .6): mus += g * np.sin(2 * np.pi * (f + det) * t + rng.random() * 6)
mus *= .55 + .45 * np.sin(2 * np.pi * t / 7.5) ** 2
# Spieluhr-Melodie
BPM = 72; beat = 60 / BPM
mel = [74, 77, 81, 79, 77, 76, 74, 69, 70, 74, 77, 76, 74, 73, 74, -1]
box = np.zeros(N); k = 0; tt = .4
while tt < DUR - 1:
    m = mel[k % len(mel)]
    if m > 0:
        n0 = int(tt * SR); L = int(2.2 * SR); L = min(L, N - n0); tl = np.arange(L) / SR; f = note(m)
        tone = (np.sin(2 * np.pi * f * tl) + .35 * np.sin(2 * np.pi * f * 2.01 * tl) + .12 * np.sin(2 * np.pi * f * 3.98 * tl)) * np.exp(-tl * 3.2)
        box[n0:n0 + L] += .11 * tone
    k += 1; tt += beat / 2
# Hall fuer die Spieluhr
ir_n = int(1.6 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 3.5); ir /= np.sqrt((ir ** 2).sum())
box = box * .7 + .45 * np.convolve(box, ir)[:N] * .5
mus += box
# Pizzicato-Puls ab Theo (Spannung)
for tt in np.arange(SEG[3]["start"], SEG[6]["end"], beat):
    n0 = int(tt * SR); L = int(.35 * SR); tl = np.arange(L) / SR; f = note(38 if int(tt / beat) % 2 == 0 else 45)
    seg = np.sin(2 * np.pi * f * tl) * np.exp(-tl * 12) * .22
    mus[n0:n0 + L] += seg[:max(0, min(L, N - n0))]
def boom(at, g=.9, f0=55):
    n0 = int(at * SR); L = int(2.5 * SR); tl = np.arange(L) / SR
    s = (np.sin(2 * np.pi * (f0 * np.exp(-tl * 1.2)) * tl) * np.exp(-tl * 1.8) + .3 * rng.standard_normal(L) * np.exp(-tl * 14)) * g
    end = min(N, n0 + L); mus[n0:end] += s[:end - n0]
boom(stop_t); boom(SEG[2]["start"] + 3.0, .7); boom(SEG[4]["end"] - .2, .8, 48)
# Musik-Pause kurz nach dem Stehenbleiben (Stille-Effekt)
gate = np.ones(N); a = int((stop_t + .05) * SR); b = int((stop_t + 1.1) * SR); gate[a:b] = np.linspace(.15, 1, b - a) ** 2
mus *= gate
# Ducking unter der Stimme
venv = np.convolve(np.abs(VOICE), np.ones(4800) / 4800, mode="same"); duck = 1 - .55 * np.clip(venv / .05, 0, 1)
mus *= duck
fade = np.ones(N); fade[:int(.5 * SR)] = np.linspace(0, 1, int(.5 * SR)); fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR)); mus *= fade

# ---------------------------------------------------------------- Soundeffekte
sfx = np.zeros(N)
def add(sig, at, g=1.0):
    n0 = int(at * SR)
    if n0 >= N: return
    end = min(N, n0 + len(sig)); sfx[n0:end] += g * sig[:end - n0]
def tick(f=2600):
    L = int(.05 * SR); tl = np.arange(L) / SR; return (np.sin(2 * np.pi * f * tl) * .6 + rng.standard_normal(L) * .4) * np.exp(-tl * 160)
def whoosh(d=.6):
    L = int(d * SR); x = rng.standard_normal(L); y = np.zeros(L); a = 0
    cut = np.linspace(.02, .25, L) * np.sin(np.linspace(0, np.pi, L))
    for i in range(L): a += cut[i] * (x[i] - a); y[i] = a
    return y * np.sin(np.linspace(0, np.pi, L)) * 1.2
def shimmer(d=1.2):
    L = int(d * SR); tl = np.arange(L) / SR; s = sum(np.sin(2 * np.pi * f * tl) for f in (1760, 2217, 2637, 3520)) / 4
    return s * np.exp(-tl * 2.5) * np.minimum(1, tl * 20)
def crackle(d):
    L = int(d * SR); s = rng.standard_normal(L) * (rng.random(L) > .985) * 1.0; hum = .15 * np.sin(2 * np.pi * 100 * np.arange(L) / SR)
    return (s + hum * (rng.random(L) > .5)) * .6
def ding():
    L = int(.9 * SR); tl = np.arange(L) / SR; return (np.sin(2 * np.pi * 1318 * tl) + .4 * np.sin(2 * np.pi * 2637 * tl)) * np.exp(-tl * 5)
for c in CUT[1:-1]: add(whoosh(.55), c / FPS - .3, .35)
b0 = CUT[1] / FPS
for tt in np.arange(b0, stop_t, .5): add(tick(), tt, .5)
add(tick(1800), stop_t, .9)
add(crackle(SEG[3]["end"] - segt(3, .36)), segt(3, .36), .25)
add(shimmer(), segt(4, .55), .35)
for frac in (.30, .42, .58): add(ding(), segt(6, frac), .25)
add(tick(2200), SEG[2]["start"] + .2, .0)

mix = VOICE * 1.0 + mus * .32 + sfx * .5
pk = np.max(np.abs(mix)); mix = mix / max(pk, 1e-6) * .89
mix16 = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
apath = os.path.join(HERE, "ep01_mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", apath], input=mix16.tobytes(), check=True)
if len(sys.argv) > 2:
    vid, out = sys.argv[1], sys.argv[2]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", apath,
                    "-vf", f"ass={os.path.join(HERE, 'ep01.ass')}:fontsdir={FD}", "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
                    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print("OK", out)
print("mix", apath)
