"""Schritt: Videoclips generieren – mit Verkettung, Prüfung und gezielter Neugenerierung.

Für jede Szene:
1. Startbild = letzter Frame der freigegebenen Vorszene (falls Anbieter das kann)
   -> nahtloser Anschluss, gleiche Umgebung, gleiche Hände.
2. Clip generieren (Provider), sofort prüfen (QC).
3. Score unter Schwelle -> neuer Versuch mit anderem Seed, bis max. Versuche oder
   Budget erschöpft. Jeder Versuch bleibt als Datei erhalten (attempts/).
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ..cost import PaymentNotApproved
from ..episode import Episode
from ..providers.base import ClipRequest, NeedsManualInput
from ..util import log, run, sha
from . import qc
from .references import refs_for_scene


def last_frame(clip: Path, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.25", "-i", clip, "-frames:v", "1", "-q:v", "2",
         "-update", "1", out])
    return out


def run_clips(ep: Episode, prod, ctx, video, vision, prompts: dict, refs: dict,
              only: set[str] | None = None) -> dict:
    cfg = ctx.cfg
    qcfg = cfg["qc"]
    max_attempts = int(cfg["costs"]["max_attempts_per_scene"])
    clips_dir, att_dir, fr_dir, sheet_dir = (prod.sub(n) for n in ("clips", "attempts", "frames", "qc"))
    result = {"ready": [], "waiting": [], "failed": [], "handoff": []}
    prev_clip: Path | None = None
    for s in ep.scenes:
        p = prompts[s.id]
        final = clips_dir / f"{s.id}.mp4"
        first = None
        if p["uses_first_frame"]:
            if prev_clip is None or not prev_clip.exists():
                prod.mark("clips", "wartet", scene=s.id, note="wartet auf die Vorszene (Startbild)")
                result["waiting"].append(s.id)
                prev_clip = None
                continue
            first = last_frame(prev_clip, fr_dir / f"{s.id}_start.jpg")
        scene_refs = refs_for_scene(ep, s.id, refs) if p["uses_refs"] else []
        # Hash bewusst OHNE Vorszene: wird Szene 4 neu gemacht, bleiben 5–7 erhalten.
        in_hash = sha([p["hash"], video.name, cfg["render"], [str(r.name) for r in scene_refs]])
        if final.exists() and prod.is_done("qc_clips", in_hash, scene=s.id):
            result["ready"].append(s.id)
            prev_clip = final
            continue
        if only is not None and s.id not in only and final.exists():
            result["ready"].append(s.id)
            prev_clip = final
            continue

        state = prod.get("clips", scene=s.id)
        attempt = state.get("attempt", 0) if state.get("input") == in_hash else 0
        best = None
        while attempt < max_attempts:
            attempt += 1
            out = att_dir / f"{s.id}_v{attempt}.mp4"
            req = ClipRequest(s.id, p["prompt"], p["negative"], s.duration, first, scene_refs,
                              seed=int(in_hash[:6], 16) + attempt, attempt=attempt)
            prod.set_status("läuft", current=f"Clip {s.id} (Versuch {attempt})")
            try:
                meta = video.generate(req, out)
            except NeedsManualInput as e:
                prod.mark("clips", "wartet", scene=s.id, input_hash=in_hash, attempt=attempt - 1, note=str(e))
                result["waiting"].append(s.id)
                result["handoff"] += [str(x) for x in e.paths]
                break
            except PaymentNotApproved as e:
                prod.mark("clips", "gestoppt", scene=s.id, input_hash=in_hash, attempt=attempt - 1, note=str(e))
                prod.event(f"Szene {s.id}: {e}", "warn")
                result["failed"].append(s.id)
                break
            prod.mark("clips", "generiert", scene=s.id, input_hash=in_hash, attempt=attempt, **meta)
            res = qc.check_clip(out, s.duration, ctx.width, ctx.height, qcfg)
            sheet = qc.contact_sheet(out, sheet_dir / f"{s.id}_v{attempt}.jpg")
            if vision is not None:
                try:
                    res = qc.apply_vision(res, vision.review(s.id, sheet, qc.VISION_CHECKLIST))
                except PaymentNotApproved as e:
                    res["issues"].append(f"KI-Prüfung übersprungen: {e}")
            res.update(attempt=attempt, file=str(out.relative_to(prod.dir)), sheet=str(sheet.relative_to(prod.dir)))
            log.info("Szene %s Versuch %d: QC %d %s", s.id, attempt, res["score"], "; ".join(res["issues"]) or "ok")
            if best is None or res["score"] > best[0]["score"]:
                best = (res, out)
            if res["score"] >= qcfg["min_scene_score"] or video.name in ("manual",):
                break
            prod.event(f"Szene {s.id} Versuch {attempt}: Score {res['score']} – generiere neu", "warn")
        if best is None:
            prev_clip = None
            continue
        res, out = best
        shutil.copy2(out, final)
        # Der beste Versuch wird übernommen; liegt er unter der Schwelle, wird er markiert.
        prod.mark("qc_clips", "done", scene=s.id, input_hash=in_hash,
                  below_threshold=res["score"] < qcfg["min_scene_score"], **res)
        if res["score"] < qcfg["min_scene_score"]:
            prod.event(f"Szene {s.id}: bester Versuch nur Score {res['score']} – bitte prüfen", "warn")
        result["ready"].append(s.id)
        prev_clip = final
    return result
