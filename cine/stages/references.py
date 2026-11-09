"""Schritt: Referenzbilder (Hände/Ausrüstung, Zombie-Typen, Schauplatz) als visuelle Anker."""
from __future__ import annotations

from pathlib import Path

from ..episode import Episode
from ..providers.base import NeedsManualInput
from ..util import log, sha


def run_references(ep: Episode, prod, image_provider) -> tuple[dict[str, Path], list[Path]]:
    refs: dict[str, Path] = {}
    waiting: list[Path] = []
    folder = prod.sub("references")
    for r in ep.references:
        rid = r["id"]
        out = folder / f"{rid}.jpg"
        h = sha([r["prompt"], image_provider.name])
        if prod.is_done("references", h, scene=f"ref:{rid}") and out.exists():
            refs[rid] = out
            continue
        try:
            meta = image_provider.generate(rid, r["prompt"], out)
            prod.mark("references", "done", scene=f"ref:{rid}", input_hash=h, file=str(out.relative_to(prod.dir)),
                      **{k: v for k, v in meta.items() if k in ("provider", "model", "usd")})
            refs[rid] = out
            log.info("Referenz %s fertig", rid)
        except NeedsManualInput as e:
            prod.mark("references", "wartet", scene=f"ref:{rid}", input_hash=h, note=str(e))
            waiting += e.paths
    return refs, waiting


def refs_for_scene(ep: Episode, scene_id: str, refs: dict[str, Path]) -> list[Path]:
    out = []
    for r in ep.references:
        use = r.get("use_in", "all")
        if (use == "all" or scene_id in use) and r["id"] in refs:
            out.append(refs[r["id"]])
    return out
