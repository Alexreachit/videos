# Folge 2: Hook am Anfang ("Folge dem Kanal ... Nebelstein") – Stimme aus dem Schluss wiederverwendet (keine neuen ElevenLabs-Zeichen)
import json, subprocess, sys, numpy as np
SR = 48000; FPS = 30
T = json.load(open("ep02_timing.json")); s8 = T["segments"][8]
CTA0 = s8["start"] + 9.45; CTA1 = s8["end"] + .05
VID0 = 12.3; HL = 4.6        # Ausschnitt: neue Bewohner tauchen auf
def load(p, a=None, b=None):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
    return x if a is None else x[int(a * SR):int(b * SR)]
cta = load("ep02_voice_cut.wav", CTA0, CTA1)
N = int(HL * SR); t = np.arange(N) / SR; out = np.zeros(N)
out[int(.35 * SR):int(.35 * SR) + len(cta)] += cta * 1.05
drone = (np.sin(2 * np.pi * 55 * t) * .5 + np.sin(2 * np.pi * 82.4 * t) * .3 + np.sin(2 * np.pi * 110 * t) * .15) * .05 * np.minimum(1, t / .4) * np.minimum(1, (HL - t) / .3)
boom = np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 8)) * t) * np.exp(-t * 3.2) * .35
out += drone + boom
for k, tp in enumerate((.5, .8, 1.1, 1.4)):   # leise "pop"-Shimmer fuer die auftauchenden Figuren
    n0 = int(tp * SR); tt = np.arange(int(.5 * SR)) / SR; out[n0:n0 + len(tt)] += np.sin(2 * np.pi * (1500 + 300 * k) * tt) * np.exp(-tt * 9) * .05
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "hook_a.wav"], input=out.astype(np.float64).tobytes(), check=True)
cl = len(cta) / SR
def ts(s): return "%d:%02d:%02d.%02d" % (s // 3600, s % 3600 // 60, int(s % 60), int(round((s % 1) * 100)) % 100)
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
       "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Big,Lilita One,104,&H006BD8FF,&H000000FF,&H00201010,&H64000000,0,0,0,0,100,100,2,0,1,7,3,8,40,40,0,1",
       "Style: Box,Lilita One,66,&H00FFFFFF,&H000000FF,&H00382820,&HD0201010,0,0,0,0,100,100,1,0,3,14,0,5,40,40,0,1", "",
       "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
pop = r"\t(0,120,\fscx112\fscy112)\t(120,240,\fscx100\fscy100)"
ass.append(f"Dialogue: 3,{ts(.3)},{ts(HL)},Big,,0,0,0,,{{\\an8\\pos(540,230)\\fad(150,150){pop}}}FOLGE DEM KANAL")
ass.append(f"Dialogue: 3,{ts(.35 + cl * .45)},{ts(HL)},Box,,0,0,0,,{{\\an5\\pos(540,430)\\fad(150,150){pop}}}  = DU ZIEHST NACH NEBELSTEIN  ")
ass.append(f"Dialogue: 3,{ts(.35 + cl * .8)},{ts(HL)},Box,,0,0,0,,{{\\an5\\pos(540,560)\\fad(150,150){pop}\\c&H6BD8FF&}}  UND SPIELST MIT  ")
open("hook.ass", "w", encoding="utf-8").write("\n".join(ass) + "\n")
src, final, out_p = sys.argv[1], sys.argv[2], sys.argv[3]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(VID0), "-t", str(HL), "-i", src, "-i", "hook_a.wav",
                "-vf", "subtitles=hook.ass:fontsdir=fonts,fade=t=out:st=%.2f:d=0.25:color=white" % (HL - .25), "-r", "30",
                "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-15:TP=-1.5:LRA=7", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1", "hook.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "hook.mp4", "-i", final, "-filter_complex",
                "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_p], check=True)
print("OK", out_p)
