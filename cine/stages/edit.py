"""Schritt: Schnitt, Übergänge, Farbkorrektur, Tonmischung, Rendering (ffmpeg).

Szenen werden exakt auf ihre geplante Dauer gebracht (längere Clips gekürzt,
kürzere mit dem letzten Bild verlängert), damit die Sound-Cues sitzen.
Übergänge passieren innerhalb der Szene (kein Überlappen), deshalb verschiebt
sich die Zeitleiste nie.
"""
from __future__ import annotations

from pathlib import Path

from ..episode import Episode
from ..util import log, media_info, run

GRADES = {
    # kühle, entsättigte Nacht mit abgesoffenen Schwarzwerten, leichte Teal-Schatten
    "horror_night": "eq=contrast=1.10:brightness=-0.015:saturation=0.78:gamma=0.97,"
                    "colorbalance=rs=-0.04:bs=0.05:rh=0.03:bh=-0.02,"
                    "curves=master='0/0 0.08/0.03 0.5/0.47 1/0.96'",
    "overcast_day": "eq=contrast=1.06:saturation=0.70,colorbalance=rs=-0.02:gs=0.01:bs=0.03,"
                    "curves=master='0/0.02 0.5/0.48 1/0.95'",
    "neutral": "null",
}


def _transition(kind: str) -> str:
    if kind == "whip":   # Reißschwenk-Gefühl: kurze horizontale Bewegungsunschärfe am Szenenanfang
        return ",boxblur=luma_radius=18:luma_power=2:chroma_radius=8:enable='lt(t,0.12)'"
    if kind == "dip":
        return ",fade=t=in:st=0:d=0.35"
    if kind == "flash":
        return ",fade=t=in:st=0:d=0.22:color=white"
    return ""


def normalize_clip(src: Path, out: Path, dur: float, w: int, h: int, fps: int, transition: str,
                   use_audio: bool) -> None:
    info = media_info(src)
    pad = max(0.0, dur - info["duration"] + 0.05)
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps}"
          f",tpad=stop_mode=clone:stop_duration={pad:.3f}" + _transition(transition) + f",trim=0:{dur:.3f},setpts=PTS-STARTPTS")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src]
    if use_audio and info["has_audio"]:
        af = f"aresample=48000,apad,atrim=0:{dur:.3f},asetpts=PTS-STARTPTS"
        cmd += ["-filter_complex", f"[0:v]{vf}[v];[0:a]{af}[a]", "-map", "[v]", "-map", "[a]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{dur:.3f}", out]
    run(cmd)


def run_edit(ep: Episode, prod, ctx, native_audio: dict[str, bool]) -> Path:
    cfg = ctx.cfg
    w, h, fps = ctx.width, ctx.height, int(cfg["render"]["fps"])
    ed = cfg["edit"]
    norm = prod.sub("edit/norm")
    parts = []
    for s in ep.scenes:
        src = prod.dir / "clips" / f"{s.id}.mp4"
        out = norm / f"{s.id}.mp4"
        normalize_clip(src, out, s.duration, w, h, fps, s.transition_in, native_audio.get(s.id, False))
        parts.append(out)
    lst = prod.dir / "edit" / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts), encoding="utf-8")
    joined = prod.dir / "edit" / "joined.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

    total = ep.total_duration
    grade = GRADES.get(ed.get("grade", "neutral"), "null")
    vchain = [grade]
    if ed.get("vignette", True):
        vchain.append("vignette=angle=PI/5")
    if ed.get("grain", 0):
        vchain.append(f"noise=alls={int(ed['grain'])}:allf=t")
    end = ep.settings.get("ending", "cut_to_black")
    if end == "cut_to_black":
        vchain.append(f"fade=t=out:st={max(0, total - 0.08):.3f}:d=0.08")
    elif end == "fade":
        vchain.append(f"fade=t=out:st={max(0, total - 1.2):.3f}:d=1.2")
    vchain.append("format=yuv420p")
    lufs = cfg["render"]["loudness_lufs"]
    fc = (f"[0:v]{','.join(vchain)}[v];"
          f"[0:a]volume={ed['native_audio_gain_db']}dB[a0];"
          f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={ed['sfx_gain_db']}dB[a1];"
          f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={ed['ambience_gain_db']}dB[a2];"
          f"[a0][a1][a2]amix=inputs=3:normalize=0:duration=first,"
          f"loudnorm=I={lufs}:TP=-2:LRA=11,alimiter=limit=0.75:level=false,atrim=0:{total:.3f}[a]")
    final = prod.sub("output") / f"{ep.id}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", joined, "-i", prod.dir / "audio" / "sfx.wav",
         "-i", prod.dir / "audio" / "ambience.wav", "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", cfg["render"]["preset"], "-crf", str(cfg["render"]["crf"]),
         "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
         "-t", f"{total:.3f}", final])
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{min(1.0, total / 2):.2f}", "-i", final,
         "-frames:v", "1", "-q:v", "3", "-update", "1", prod.dir / "output" / f"{ep.id}_thumb.jpg"])
    log.info("Rendering fertig: %s", final)
    return final
