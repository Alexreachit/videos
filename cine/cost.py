"""Kostenschätzung und Freigabe.

Regel: Kein kostenpflichtiger Aufruf ohne gültige Freigabe.
1. `python -m cine estimate <episode>` schreibt estimate.json mit einem Freigabe-Code.
2. `python -m cine approve <episode> --code <CODE> --max-usd <BETRAG>` schreibt approval.json.
3. Jeder bezahlte Provider ruft vor dem API-Aufruf CostGuard.charge() auf. Ohne passende
   Freigabe (falscher Code, Plan geändert, Budget erschöpft) bricht der Schritt ab,
   BEVOR Geld ausgegeben wird.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from .episode import Episode
from .state import Production
from .util import read_json, sha, write_json

FREE_PROVIDERS = {"mock", "manual", "procedural", "none"}


class PaymentNotApproved(RuntimeError):
    pass


def _price(cfg: dict, key: str) -> dict:
    p = cfg.get("prices", {}).get(key)
    if p is None:
        raise KeyError(f"Kein Preis für {key} in der Konfiguration hinterlegt – bitte in default.yaml ergänzen")
    return p


def price_key(cfg: dict, step: str) -> str | None:
    prov = cfg["providers"][step]
    if prov in FREE_PROVIDERS:
        return None
    if prov == "elevenlabs":
        return "elevenlabs:sfx"
    model_step = {"image": "image", "video": "video", "vision_qc": "vision"}[step]
    return f"{prov}:{cfg['models'][prov][model_step]}"


def video_cost(cfg: dict, seconds: float) -> float:
    key = price_key(cfg, "video")
    if not key:
        return 0.0
    return round(_price(cfg, key)["per_second"][cfg["render"]["resolution"]] * seconds, 4)


def image_cost(cfg: dict, n: int = 1) -> float:
    key = price_key(cfg, "image")
    return 0.0 if not key else round(_price(cfg, key)["per_image"] * n, 4)


def sfx_cost(cfg: dict, seconds: float) -> float:
    key = price_key(cfg, "sfx")
    return 0.0 if not key else round(_price(cfg, key)["per_second"] * seconds, 4)


def vision_cost(cfg: dict, calls: int = 1) -> float:
    key = price_key(cfg, "vision_qc")
    return 0.0 if not key else round(_price(cfg, key)["per_call"] * calls, 4)


def estimate(ep: Episode, cfg: dict) -> dict:
    n_scenes = len(ep.scenes)
    secs = ep.total_duration
    n_refs = len(ep.references)
    cue_secs = sum((c.dur or 1.5) for s in ep.scenes for c in s.cues)
    lines = [
        {"posten": "Referenzbilder", "anbieter": cfg["providers"]["image"], "menge": n_refs, "einheit": "Bilder",
         "usd": image_cost(cfg, n_refs)},
        {"posten": "Videoclips", "anbieter": f"{cfg['providers']['video']}"
         + (f" ({cfg['models'].get(cfg['providers']['video'], {}).get('video')})" if price_key(cfg, 'video') else ""),
         "menge": n_scenes, "einheit": f"Clips / {secs:.0f} s @ {cfg['render']['resolution']} {cfg['render']['aspect']}",
         "usd": video_cost(cfg, secs)},
        {"posten": "Soundeffekte", "anbieter": cfg["providers"]["sfx"], "menge": round(cue_secs, 1), "einheit": "s",
         "usd": sfx_cost(cfg, cue_secs)},
        {"posten": "KI-Bildprüfung", "anbieter": cfg["providers"]["vision_qc"], "menge": n_scenes, "einheit": "Prüfungen",
         "usd": vision_cost(cfg, n_scenes)},
        {"posten": "Schnitt, Grading, Upscaling, Rendering", "anbieter": "ffmpeg (lokal/GitHub)", "menge": 1,
         "einheit": "Lauf", "usd": 0.0},
    ]
    base = round(sum(l["usd"] for l in lines), 2)
    reserve = round(base * cfg["costs"]["retry_reserve"], 2)
    avg_scene = video_cost(cfg, secs / n_scenes) + vision_cost(cfg, 1)
    worst = round(base + avg_scene * n_scenes * (cfg["costs"]["max_attempts_per_scene"] - 1), 2)
    plan = {
        "episode": ep.id, "providers": cfg["providers"], "models": cfg["models"],
        "render": {k: cfg["render"][k] for k in ("aspect", "resolution", "fps")},
        "scenes": [(s.id, s.duration) for s in ep.scenes], "refs": n_refs,
    }
    est = {
        "created": time.time(), "episode": ep.id, "title": ep.title, "lines": lines,
        "basis_usd": base, "mit_reserve_usd": round(base + reserve, 2), "worst_case_usd": worst,
        "pro_neugenerierung_szene_usd": round(avg_scene, 2),
        "clips": n_scenes, "dauer_s": secs,
        "kostenpflichtig": base > 0, "plan_hash": sha(plan),
    }
    est["code"] = est["plan_hash"][:6].upper()
    return est


def format_estimate(est: dict) -> str:
    rows = ["| Posten | Anbieter | Menge | USD |", "|---|---|---|---:|"]
    for l in est["lines"]:
        rows.append(f"| {l['posten']} | {l['anbieter']} | {l['menge']} {l['einheit']} | {l['usd']:.2f} |")
    rows += [
        f"| **Summe (ein Durchgang)** | | | **{est['basis_usd']:.2f}** |",
        f"| inkl. Reserve für Neuversuche | | | {est['mit_reserve_usd']:.2f} |",
        f"| schlimmster Fall (alle Szenen max. Versuche) | | | {est['worst_case_usd']:.2f} |",
        "",
        f"Neugenerierung einer Szene: ca. {est['pro_neugenerierung_szene_usd']:.2f} USD.",
    ]
    if est["kostenpflichtig"]:
        rows.append(f"\n**Freigabe-Code: `{est['code']}`** – ohne diesen Code startet nichts Kostenpflichtiges.")
    else:
        rows.append("\nDieser Lauf ist **kostenlos** – keine Freigabe nötig.")
    return "\n".join(rows)


def approve(prod: Production, code: str, max_usd: float, by: str = "user") -> dict:
    est = read_json(prod.dir / "estimate.json")
    if not est:
        raise PaymentNotApproved("Keine Kostenschätzung vorhanden – erst `estimate` ausführen")
    if code.strip().upper() != est["code"]:
        raise PaymentNotApproved(f"Freigabe-Code passt nicht zur aktuellen Schätzung (erwartet {est['code']})")
    if max_usd <= 0:
        raise PaymentNotApproved("Budget muss größer als 0 sein")
    appr = {"code": est["code"], "plan_hash": est["plan_hash"], "max_usd": float(max_usd), "ts": time.time(), "by": by}
    write_json(prod.dir / "approval.json", appr)
    prod.event(f"Kosten freigegeben: bis {max_usd:.2f} USD (Code {est['code']})")
    return appr


@dataclass
class CostGuard:
    prod: Production
    plan_hash: str

    def remaining(self) -> float:
        appr = read_json(self.prod.dir / "approval.json")
        if not appr or appr.get("plan_hash") != self.plan_hash:
            return 0.0
        return round(appr["max_usd"] - self.prod.data.get("spend_usd", 0.0), 4)

    def check(self, usd: float, what: str) -> None:
        if usd <= 0:
            return
        appr = read_json(self.prod.dir / "approval.json")
        if not appr:
            raise PaymentNotApproved(f"{what}: kostet ca. {usd:.2f} USD, aber es gibt keine Freigabe")
        if appr.get("plan_hash") != self.plan_hash:
            raise PaymentNotApproved(f"{what}: Plan hat sich seit der Freigabe geändert – neu schätzen und freigeben")
        if usd > self.remaining() + 1e-9:
            raise PaymentNotApproved(
                f"{what}: {usd:.2f} USD würden das freigegebene Budget überschreiten (Rest {self.remaining():.2f} USD)")

    def charge(self, usd: float, what: str) -> None:
        """Vor dem API-Aufruf prüfen; nach Erfolg mit commit() verbuchen."""
        self.check(usd, what)

    def commit(self, usd: float, what: str) -> None:
        if usd > 0:
            self.prod.add_spend(usd, what)


def save_estimate(prod: Production, est: dict) -> None:
    write_json(prod.dir / "estimate.json", est)
    (prod.dir / "estimate.md").write_text(format_estimate(est), encoding="utf-8")
