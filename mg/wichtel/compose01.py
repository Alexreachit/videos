# Wichtelheim – Schnitt: stummes Blender-Video + Stimme + eigene Musik/SFX (numpy, selbst erzeugt) + Untertitel/Overlays (ASS) -> MP4
# python3 compose.py <silent.mp4> <out.mp4>
import json, re, subprocess, sys, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
T = json.load(open(os.path.join(HERE, "ep01_timing.json"))); SEG = T["segments"]; DUR = T["duration"]; FPS = T["fps"]
F = lambda t: int(round(t * FPS)); CUT = [0] + [F(s["start"]) - 2 for s in SEG[1:]] + [F(DUR)]
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
       "Style: Title,Lilita One,150,&H003A3AD6,&H00FFFFFF,&H00FFFFFF,&H64000000,0,0,0,0,100,100,3,0,1,9,6,8,40,40,300,1",
       "Style: Sub,Lilita One,64,&H00FFFFFF,&H00FFFFFF,&H00241612,&H64000000,0,0,0,0,100,100,3,0,1,5,3,8,40,40,470,1",
       "Style: Box,Lilita One,62,&H00FFFFFF,&H00FFFFFF,&H00203A9C,&HE0203A9C,0,0,0,0,100,100,1,0,3,18,0,7,0,0,0,1",
       "Style: Big,Lilita One,84,&H006BD8FF,&H00FFFFFF,&H00241612,&H64000000,0,0,0,0,100,100,2,0,1,7,4,8,40,40,300,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
def ev(a, b, style, txt, layer=0): ass.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{txt}")
GOLD = r"{\c&H6BD8FF&}"; WH = r"{\c&HFFFFFF&}"
for i, ws in enumerate(WORDS):
    # Gruppen a 3 Woertern; aktuelles Wort gold + leicht groesser
    if i == 0: continue  # Titelkarte + Overlays
def boxat(t0, t1, y, txt, style="Box", pop=True):
    ev(t0, t1, style, r"{\an5\pos(540," + str(y) + r")\fad(150,200)" + (r"\t(0,120,\fscx112\fscy112)\t(120,240,\fscx100\fscy100)" if pop else "") + "}" + txt, 3)
ev(.2, SEG[0]["end"] + .3, "Big", r"{\an8\pos(540,230)\fad(150,150)\t(0,120,\fscx112\fscy112)\t(120,240,\fscx100\fscy100)}FOLGE = DU ZIEHST EIN", 3)
boxat(segt(0, .55), SEG[0]["end"] + .3, 420, "  ALS KNETFIGUR!  ")
ev(SEG[1]["start"] - .1, segt(1, .55), "Title", r"{\fad(300,300)\t(0,160,\fscx110\fscy110)\t(160,320,\fscx100\fscy100)}WICHTELHEIM", 2)
ev(SEG[1]["start"] + .3, segt(1, .55), "Sub", r"{\fad(300,300)}DAS TIKTOK-WEIHNACHTSDORF", 2)
boxat(segt(1, .78), SEG[1]["end"] + .3, 300, "  FLOCKE, DER WICHTEL  ")
boxat(segt(2, .14), SEG[2]["end"] + .3, 230, "  1 FOLLOWER = 1 DORFBEWOHNER  ")
boxat(segt(2, .4), SEG[2]["end"] + .3, 350, "  1 HERZ = 1 GOLDTALER  ")
boxat(segt(2, .7), SEG[2]["end"] + .3, 470, "  TOP-KOMMENTAR ENTSCHEIDET  ")
boxat(segt(3, .1), SEG[3]["end"] + .3, 250, "  ZIEL: DAS SCHÖNSTE WEIHNACHTSDORF  ")
ev(segt(3, .45), SEG[3]["end"] + .3, "Big", r"{\an8\pos(540,360)\fad(150,200)\t(0,120,\fscx112\fscy112)\t(120,240,\fscx100\fscy100)}NOCH 44 TAGE\NBIS HEILIGABEND", 3)
boxat(segt(4, .55), SEG[4]["end"] + .3, 250, "  BEWOHNER: 0  ")
ev(segt(4, .82), SEG[4]["end"] + .3, "Big", r"{\an8\pos(540,340)\fad(100,200)\t(0,120,\fscx115\fscy115)\t(120,260,\fscx100\fscy100)}DORFKASSE: 0 TALER", 3)
ev(SEG[5]["start"], DUR, "Big", r"{\an8\pos(540,170)\fad(200,0)}WAS BAUEN WIR ZUERST?", 3)
boxat(segt(5, .2), DUR, 330, "  A  ·  LEBKUCHEN-BÄCKEREI  ")
boxat(segt(5, .6), DUR, 450, "  B  ·  RIESIGER WEIHNACHTSBAUM  ")
ev(segt(6, .2), DUR, "Sub", r"{\an5\pos(540,580)\fad(200,0)}SCHREIB A ODER B IN DIE KOMMENTARE!", 3)
boxat(segt(6, .65), DUR, 700, "  FOLGEN = EINZIEHEN  ")
open(os.path.join(HERE, "ep01.ass"), "w", encoding="utf-8").write("\n".join(ass) + "\n")

# ---------------------------------------------------------------- Musik (eigene Komposition, G-Dur, weihnachtlich – kein bekanntes Lied)
t = np.arange(N) / SR; rng = np.random.default_rng(5)
def note(f): return 440 * 2 ** ((f - 69) / 12)
mus = np.zeros(N); BPM = 112; beat = 60 / BPM
night0, night1 = SEG[4]["start"] - .2, SEG[4]["end"] + .3
CH = [[55, 59, 62], [52, 55, 59], [48, 52, 55], [50, 54, 57]]   # G  Em  C  D
mel = [74, 76, 78, 79, 78, 76, 74, -1, 71, 74, 76, 74, 71, 69, 71, -1, 72, 74, 76, 79, 76, 74, 72, 71, 69, 71, 74, 71, 69, 67, 67, -1]
def bell(f, L, g):
    tl = np.arange(L) / SR; return g * (np.sin(2 * np.pi * f * tl) + .5 * np.sin(2 * np.pi * f * 2.76 * tl) * np.exp(-tl * 6) + .25 * np.sin(2 * np.pi * f * 5.4 * tl) * np.exp(-tl * 9)) * np.exp(-tl * 3.5)
k = 0; tt = .2
while tt < DUR - 1.2:
    bar = int(tt / (4 * beat)); ch = CH[bar % 4]; nightv = .45 if night0 < tt < night1 else 1.0
    m = mel[k % len(mel)]
    if m > 0 and not (night0 < tt < night1 and k % 2):
        n0 = int(tt * SR); L = min(int(1.4 * SR), N - n0); mus[n0:n0 + L] += bell(note(m), L, .09 * nightv)[:L]
    if k % 2 == 0:   # Bass + Akkord (Pizzicato)
        n0 = int(tt * SR); L = min(int(.45 * SR), N - n0); tl = np.arange(L) / SR
        f = note(ch[0] - 12 if (k // 2) % 2 == 0 else ch[2] - 12); mus[n0:n0 + L] += .2 * nightv * np.sin(2 * np.pi * f * tl) * np.exp(-tl * 7)
        for c in ch: mus[n0:n0 + L] += .03 * nightv * np.sin(2 * np.pi * note(c) * tl) * np.exp(-tl * 5)
    # Schlittenglocken (Achtel), nachts aus
    if not (night0 < tt < night1):
        n0 = int(tt * SR); L = min(int(.12 * SR), N - n0); tl = np.arange(L) / SR
        jing = rng.standard_normal(L) * np.exp(-tl * 45) * .06 + sum(np.sin(2 * np.pi * f * tl) for f in (5200, 6300, 7400)) * np.exp(-tl * 30) * .015
        mus[n0:n0 + L] += jing * (1.0 if k % 2 else .6)
    k += 1; tt += beat / 2
# weiches Pad (warm)
for c, g in ((43, .05), (50, .03)): mus += g * np.sin(2 * np.pi * note(c) * t) * (.6 + .4 * np.sin(2 * np.pi * t / 6))
ir_n = int(1.2 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 4); ir /= np.sqrt((ir ** 2).sum())
mus = mus * .8 + .35 * np.convolve(mus, ir)[:N] * .5
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
def pop():
    L = int(.18 * SR); tl = np.arange(L) / SR; return np.sin(2 * np.pi * (300 + 900 * np.exp(-tl * 30)) * tl) * np.exp(-tl * 22)
def coin():
    L = int(.5 * SR); tl = np.arange(L) / SR; return (np.sin(2 * np.pi * 2093 * tl) + .6 * np.sin(2 * np.pi * 3136 * tl)) * np.exp(-tl * 9)
def wind(d):
    L = int(d * SR); x = rng.standard_normal(L); y = np.zeros(L); a = 0
    for i in range(L): a += .01 * (x[i] - a); y[i] = a
    return y * 8 * np.sin(np.linspace(0, np.pi, L)) * (.6 + .4 * np.sin(np.linspace(0, 9, L)))
for c in CUT[1:-1]: add(whoosh(.5), c / FPS - .25, .3)
add(pop(), segt(0, .05) - .05, .6); add(shimmer(.8), SEG[1]["start"], .25)
for k in range(5): add(pop(), segt(2, .12 + k * .05), .4)
for k in range(7): add(coin(), segt(2, .45 + k * .04) + 4 / FPS, .25)
for k in range(6): add(pop(), segt(3, .1 + k * .07), .35)
add(shimmer(1.4), segt(3, .45), .35)
add(wind(SEG[4]["end"] - SEG[4]["start"] + .4), SEG[4]["start"] - .2, .55)
add(ding(), segt(4, .82), .25)
for frac in (.2, .6): add(ding(), segt(5, frac), .25)
add(shimmer(.8), segt(6, .65), .25)
mix = VOICE * 1.0 + mus * .32 + sfx * .5
pk = np.max(np.abs(mix)); mix = mix / max(pk, 1e-6) * .89
mix16 = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
apath = os.path.join(HERE, "ep01_mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", apath], input=mix16.tobytes(), check=True)
if len(sys.argv) > 2:
    vid, out = sys.argv[1], sys.argv[2]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", apath,
                    "-vf", f"setpts=PTS*30/{FPS},fps=30,ass={os.path.join(HERE, 'ep01.ass')}:fontsdir={FD}", "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
                    "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print("OK", out)
print("mix", apath)
