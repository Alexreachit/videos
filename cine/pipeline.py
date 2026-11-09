"""Orchestrierung der gesamten Produktion mit Checkpoints und Wiederaufnahme."""
from __future__ import annotations

import time
from pathlib import Path

from . import cost
from .config import dimensions, load_config, load_env_file
from .dashboard import write_dashboards
from .episode import Episode, load_episode
from .providers import get_image, get_sfx, get_video, get_vision
from .providers.base import Ctx
from .stages import audio, clips, edit, prompts, qc, references
from .state import Production
from .util import log, read_json, setup_logging, sha, write_json


def production_id(ep: Episode, cfg: dict) -> str:
    return f"{ep.id}_{cfg['providers']['video']}"


def write_plan(ep: Episode, prod: Production, cfg: dict) -> dict:
    t = 0.0
    scenes = []
    for s in ep.scenes:
        scenes.append({"id": s.id, "beat": s.beat, "start": round(t, 2), "end": round(t + s.duration, 2),
                       "duration": s.duration, "action": s.action, "transition_in": s.transition_in,
                       "cues": [{"t": c.t, "art": c.kind} for c in s.cues]})
        t += s.duration
    plan = {"episode": ep.id, "title": ep.title, "logline": ep.logline, "dauer_s": ep.total_duration,
            "providers": cfg["providers"], "render": cfg["render"], "scenes": scenes}
    write_json(prod.dir / "plan.json", plan)
    md = [f"# {ep.title}", "", ep.logline, "", "| Szene | Zeit | Beat | Inhalt |", "|---|---|---|---|"]
    md += [f"| {s['id']} | {s['start']:.0f}–{s['end']:.0f} s | {s['beat']} | {s['action']} |" for s in scenes]
    (prod.dir / "plan.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return plan


def save_prompts(prod: Production, ps: dict) -> None:
    folder = prod.sub("prompts")
    hist = read_json(folder / "history.json", {}) or {}
    for sid, p in ps.items():
        (folder / f"{sid}.txt").write_text(p["prompt"] + "\n\nNEGATIVE: " + p["negative"] + "\n", encoding="utf-8")
        h = hist.setdefault(sid, [])
        if not h or h[-1]["hash"] != p["hash"]:
            h.append({"hash": p["hash"], "version": p["version"], "ts": time.time(), "prompt": p["prompt"]})
    write_json(folder / "history.json", hist)
    write_json(folder / "prompts.json", ps)


def write_report(ep: Episode, prod: Production, final_qc: dict, cfg: dict) -> Path:
    st = prod.data
    lines = [f"# Produktionsbericht: {ep.title}", "", f"Produktion `{prod.id}` · Video-Anbieter **{cfg['providers']['video']}**"
             f" · {cfg['render']['resolution']} {cfg['render']['aspect']} · {ep.total_duration:.0f} s", "",
             f"**Gesamt-QC:** {final_qc['score']}/100 " + ("✓" if not final_qc["issues"] else "– " + "; ".join(final_qc["issues"])),
             f"**Kosten:** {st.get('spend_usd', 0):.2f} USD", "", "## Szenen", "",
             "| Szene | Score | Versuche | Hinweise |", "|---|---:|---:|---|"]
    uncertain = set()
    for s in ep.scenes:
        q = st["scenes"].get(s.id, {}).get("qc_clips", {})
        lines.append(f"| {s.id} | {q.get('score', '–')} | {q.get('attempt', '–')} | {'; '.join(q.get('issues', [])) or 'ok'} |")
        uncertain.update(q.get("manuell_pruefen", []))
    if cfg["providers"]["video"] == "mock":
        lines += ["", "> Testlauf mit Platzhalter-Clips: Ton, Schnitt, Timing und Prüfungen sind echt, die Bilder nicht."]
    if uncertain:
        lines += ["", "## Bitte selbst ansehen", "", "Automatisch nicht sicher prüfbar (keine KI-Sichtprüfung aktiv):", ""]
        lines += [f"- [ ] {u}" for u in sorted(uncertain)]
    p = prod.dir / "output" / "bericht.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def run_production(episode_path: str | Path, overrides: dict | None = None, pid: str | None = None,
                   only_scenes: set[str] | None = None, base: Path | None = None) -> dict:
    load_env_file()
    ep = load_episode(episode_path)
    cfg = load_config(ep.settings, overrides)
    prod = Production(pid or production_id(ep, cfg), base=base)
    setup_logging(prod.dir / "log.txt")
    w, h = dimensions(cfg)
    try:
        write_plan(ep, prod, cfg)
        est = cost.estimate(ep, cfg)
        cost.save_estimate(prod, est)
        guard = cost.CostGuard(prod, est["plan_hash"])
        if est["kostenpflichtig"] and guard.remaining() <= 0:
            prod.set_status("wartet auf Freigabe", current=f"Schätzung {est['basis_usd']:.2f} USD, Code {est['code']}")
            prod.event(f"Kostenpflichtiger Lauf – wartet auf Freigabe (Code {est['code']}, ca. {est['mit_reserve_usd']:.2f} USD)", "warn")
            return {"status": "wartet auf Freigabe", "estimate": est, "production": prod.id, "dir": str(prod.dir)}

        ctx = Ctx(cfg=cfg, prod=prod, guard=guard, width=w, height=h)
        video = get_video(cfg["providers"]["video"], ctx)
        image = get_image(cfg["providers"]["image"], ctx)
        sfx = get_sfx(cfg["providers"]["sfx"], ctx)
        vision = get_vision(cfg["providers"]["vision_qc"], ctx)

        prod.set_status("läuft", current="Prompts")
        ps = prompts.build_all(ep, video)
        save_prompts(prod, ps)
        prod.mark("prompts", "done", input_hash=sha({k: v["hash"] for k, v in ps.items()}))

        prod.set_status("läuft", current="Referenzbilder")
        refs, waiting_refs = references.run_references(ep, prod, image)

        prod.set_status("läuft", current="Videoclips")
        cres = clips.run_clips(ep, prod, ctx, video, vision, ps, refs, only=only_scenes)
        if cres["waiting"] or cres["failed"] or waiting_refs:
            status = "gestoppt" if cres["failed"] else "wartet auf Clips"
            prod.set_status(status, current=f"{len(cres['ready'])}/{len(ep.scenes)} Szenen fertig")
            if cres["handoff"] or waiting_refs:
                prod.event(f"Prompt-Karten liegen in handoff/ – {len(cres['handoff']) + len(waiting_refs)} Dateien")
            return {"status": status, "production": prod.id, "dir": str(prod.dir), "clips": cres,
                    "estimate": est, "waiting_refs": [str(p) for p in waiting_refs]}

        prod.set_status("läuft", current="Sounddesign")
        a = audio.run_audio(ep, prod, sfx)
        write_json(prod.dir / "audio" / "timeline.json", a["timeline"])
        prod.mark("audio", "done", cues=a["cues"])

        prod.set_status("läuft", current="Schnitt und Rendering")
        native = {s.id: bool(prod.get("clips", scene=s.id).get("native_audio")) for s in ep.scenes}
        final = edit.run_edit(ep, prod, ctx, native)
        prod.mark("edit", "done", file=str(final.relative_to(prod.dir)))

        prod.set_status("läuft", current="Endkontrolle")
        fq = qc.check_final(final, ep.total_duration, w, h, audio.scene_offsets(ep))
        prod.mark("qc_final", "done", score=fq["score"], issues=fq["issues"], audio=fq["audio"])
        report = write_report(ep, prod, fq, cfg)
        prod.mark("export", "done", file=str(final.relative_to(prod.dir)), report=str(report.relative_to(prod.dir)))
        prod.set_status("fertig", current=f"{final.name} · QC {fq['score']}")
        prod.event(f"Fertig: {final.name} (QC {fq['score']}, {prod.data.get('spend_usd', 0):.2f} USD)")
        return {"status": "fertig", "production": prod.id, "dir": str(prod.dir), "video": str(final),
                "qc": fq, "estimate": est}
    except Exception as e:
        log.exception("Produktion abgebrochen")
        prod.set_status("fehler", current=str(e)[:300])
        prod.event(f"Fehler: {e}", "error")
        raise
    finally:
        write_dashboards(prod.dir.parent)


def redo_scene(episode_path: str | Path, scene: str, overrides: dict | None = None, pid: str | None = None,
               base: Path | None = None) -> dict:
    ep = load_episode(episode_path)
    ep.scene(scene)
    cfg = load_config(ep.settings, overrides)
    prod = Production(pid or production_id(ep, cfg), base=base)
    prod.invalidate_scene(scene)
    (prod.dir / "clips" / f"{scene}.mp4").unlink(missing_ok=True)
    rejected = prod.sub("inbox/verworfen")
    for f in (prod.dir / "inbox").glob(f"{scene}.*"):   # Gratis-Weg: alten Clip beiseitelegen
        f.rename(rejected / f"{f.stem}_{int(time.time())}{f.suffix}")
    prod.event(f"Szene {scene} wird neu generiert")
    return run_production(episode_path, overrides, prod.id, only_scenes={scene}, base=base)
