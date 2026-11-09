"""Schritt: Qualitätskontrolle pro Clip und für das fertige Video.

Automatisch messbar (zuverlässig): Dauer, Auflösung, Seitenverhältnis, Bildrate,
Schwarzbilder, eingefrorene Bilder, Unschärfe, Flackern, harte Schnitte innerhalb
eines Clips (= Bruch der durchgehenden POV-Einstellung), Tonspur, Übersteuerung.

Nicht zuverlässig messbar ohne KI-Sichtprüfung: ob die Perspektive wirklich
First Person bleibt, verformte Hände, unlogische Bewegungen, Realismus. Diese
Punkte prüft optional ein Vision-Modell (kostenpflichtig) anhand eines
Kontaktblatts – sonst landen sie als "manuell prüfen" im Bericht.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from ..util import media_info, run

VISION_CHECKLIST = [
    "Durchgehend First-Person-Perspektive, kein Außenblick auf die Hauptperson",
    "Keine verformten oder zusätzlichen Finger an sichtbaren Händen",
    "Hände/Ärmel/Handschuhe passen zur Beschreibung",
    "Zombies bewegen sich glaubwürdig (ruckartig, schwer, nicht synchron)",
    "Keine schwebenden oder verschmelzenden Objekte",
    "Fotorealistisch, kein Cartoon-/Spiele-Look",
    "Kein eingeblendeter Text, kein Wasserzeichen",
    "Umgebung bleibt innerhalb des Clips konsistent",
]


def sample_frames(path: Path, every_s: float = 1 / 6, max_w: int = 320):
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    step = max(1, int(round(fps * every_s)))
    frames, i = [], 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if i % step == 0:
            h, w = f.shape[:2]
            s = max_w / w
            frames.append(cv2.resize(f, (max_w, int(h * s))))
        i += 1
    cap.release()
    return frames


def contact_sheet(path: Path, out: Path, n: int = 9) -> Path:
    fr = sample_frames(path, every_s=0.25, max_w=360)
    if not fr:
        raise RuntimeError(f"Keine Frames in {path}")
    idx = np.linspace(0, len(fr) - 1, n).astype(int)
    tiles = [fr[i] for i in idx]
    cols = 3
    rows = [np.hstack(tiles[r * cols:(r + 1) * cols]) for r in range(int(np.ceil(n / cols)))]
    sheet = np.vstack(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), sheet, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return out


def measure(path: Path, cut_threshold: float = 0.55) -> dict:
    fr = sample_frames(path)
    if len(fr) < 2:
        return {"frames": len(fr)}
    gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr]
    lum = np.array([g.mean() for g in gray])
    sharp = np.array([cv2.Laplacian(g, cv2.CV_64F).var() for g in gray])
    diffs = np.array([np.abs(gray[i].astype(np.int16) - gray[i - 1]).mean() for i in range(1, len(gray))])
    hists = []
    for f in fr:
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        h = cv2.calcHist([hsv], [0, 1], None, [24, 16], [0, 180, 0, 256])
        hists.append(cv2.normalize(h, h).flatten())
    corr = np.array([cv2.compareHist(hists[i - 1], hists[i], cv2.HISTCMP_CORREL) for i in range(1, len(hists))])
    cuts = [round((i + 1) / 6, 2) for i, c in enumerate(corr) if (1 - c) > cut_threshold and diffs[i] > 18]
    return {
        "frames": len(fr),
        "black_ratio": float((lum < 6).mean()),
        "freeze_ratio": float((diffs < 0.35).mean()),
        "sharpness": float(np.median(sharp)),
        "flicker": float(np.std(np.diff(lum))) if len(lum) > 2 else 0.0,
        "mean_luma": float(lum.mean()),
        "internal_cuts": cuts,
    }


def audio_levels(path: Path) -> dict:
    p = run(["ffmpeg", "-hide_banner", "-i", path, "-af", "volumedetect", "-vn", "-f", "null", "-"])
    out = {}
    for line in p.stderr.splitlines():
        if "mean_volume" in line:
            out["mean_db"] = float(line.split(":")[1].split()[0])
        if "max_volume" in line:
            out["max_db"] = float(line.split(":")[1].split()[0])
    return out


def check_clip(path: Path, duration: float, width: int, height: int, qcfg: dict) -> dict:
    info = media_info(path)
    m = measure(path, qcfg["cut_threshold"])
    score, issues, checks = 100, [], {}

    def flag(name: str, ok: bool, penalty: int, msg: str):
        nonlocal score
        checks[name] = ok
        if not ok:
            score -= penalty
            issues.append(msg)

    flag("dauer", info["duration"] >= duration - 0.5, 25,
         f"Clip zu kurz: {info['duration']:.1f}s statt {duration:.1f}s")
    same_aspect = abs(info.get("width", 1) / max(1, info.get("height", 1)) - width / height) < 0.03
    flag("seitenverhaeltnis", same_aspect, 20, f"Falsches Format {info.get('width')}x{info.get('height')}")
    flag("aufloesung", min(info.get("width", 0), info.get("height", 0)) >= min(width, height) * 0.66, 10,
         "Auflösung deutlich zu niedrig")
    flag("schwarzbilder", m.get("black_ratio", 1) <= qcfg["max_black_ratio"], 25,
         f"{m.get('black_ratio', 1):.0%} fast schwarze Bilder")
    flag("eingefroren", m.get("freeze_ratio", 1) <= qcfg["max_freeze_ratio"], 25,
         f"{m.get('freeze_ratio', 1):.0%} der Zeit kaum Bewegung (Standbild-Effekt)")
    flag("schaerfe", m.get("sharpness", 0) >= qcfg["min_sharpness"], 10,
         f"Bild sehr unscharf (Schärfe {m.get('sharpness', 0):.1f})")
    flag("pov_ohne_schnitt", len(m.get("internal_cuts", [])) <= qcfg["max_internal_cuts"], 30,
         f"Harte Schnitte im Clip bei {m.get('internal_cuts')} s – POV-Einstellung bricht")
    flag("flackern", m.get("flicker", 0) < 9, 10, f"Starkes Helligkeitsflackern ({m.get('flicker', 0):.1f})")
    return {"score": max(0, score), "issues": issues, "checks": checks, "metrics": m, "info": info,
            "manuell_pruefen": [c for c in VISION_CHECKLIST]}


def apply_vision(result: dict, vision: dict) -> dict:
    result = dict(result)
    result["vision"] = vision
    result["score"] = int(round(min(result["score"], 0.4 * result["score"] + 0.6 * vision["score"])))
    result["issues"] = result["issues"] + [f"KI-Prüfung: {i}" for i in vision.get("issues", [])]
    result["manuell_pruefen"] = []
    return result


def check_final(path: Path, expected: float, width: int, height: int, scene_bounds: list[float]) -> dict:
    info = media_info(path)
    lv = audio_levels(path) if info.get("has_audio") else {}
    issues = []
    if abs(info["duration"] - expected) > 0.6:
        issues.append(f"Gesamtdauer {info['duration']:.1f}s statt {expected:.1f}s")
    if (info.get("width"), info.get("height")) != (width, height):
        issues.append(f"Ausgabeformat {info.get('width')}x{info.get('height')} statt {width}x{height}")
    if not info.get("has_audio"):
        issues.append("Keine Tonspur")
    if lv.get("max_db", -99) > -0.5:
        issues.append(f"Ton übersteuert (Spitze {lv['max_db']} dB)")
    if lv and lv.get("mean_db", -99) < -40:
        issues.append(f"Ton sehr leise (Mittel {lv['mean_db']} dB)")
    score = max(0, 100 - 20 * len(issues))
    return {"score": score, "issues": issues, "info": info, "audio": lv, "scene_bounds": scene_bounds}
