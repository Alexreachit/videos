"""Checkpoints: jede Produktion hat einen Ordner productions/<id>/ mit state.json.

Jeder Schritt (global oder pro Szene) wird mit Status, Eingabe-Hash und Ergebnis
gespeichert. Bricht ein Lauf ab, setzt der nächste Lauf genau dort wieder an.
Ändert sich die Eingabe eines Schritts (z. B. ein Prompt), wird nur dieser
Schritt und alles, was davon abhängt, neu gemacht.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .config import REPO
from .util import read_json, write_json

PRODUCTIONS = REPO / "productions"

STAGES = ["plan", "prompts", "references", "clips", "qc_clips", "audio", "edit", "qc_final", "export"]


class Production:
    def __init__(self, pid: str, base: Path | None = None):
        self.id = pid
        self.dir = (base or PRODUCTIONS) / pid
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "state.json"
        self.data: dict[str, Any] = read_json(self.path, None) or {
            "id": pid, "created": time.time(), "status": "neu", "steps": {}, "scenes": {}, "spend_usd": 0.0,
            "events": [],
        }

    # --- Ordner ---------------------------------------------------------------
    def sub(self, name: str) -> Path:
        p = self.dir / name
        p.mkdir(parents=True, exist_ok=True)
        return p

    # --- Speichern -----------------------------------------------------------
    def save(self) -> None:
        self.data["updated"] = time.time()
        write_json(self.path, self.data)

    def event(self, msg: str, level: str = "info") -> None:
        self.data["events"] = (self.data.get("events", []) + [{"ts": time.time(), "level": level, "msg": msg}])[-200:]
        self.save()

    def set_status(self, status: str, current: str | None = None) -> None:
        self.data["status"] = status
        if current is not None:
            self.data["current"] = current
        self.save()

    # --- Schritte -----------------------------------------------------------
    def _slot(self, step: str, scene: str | None) -> dict:
        if scene is None:
            return self.data["steps"].setdefault(step, {})
        return self.data["scenes"].setdefault(scene, {}).setdefault(step, {})

    def is_done(self, step: str, input_hash: str, scene: str | None = None) -> bool:
        s = self._slot(step, scene)
        return s.get("status") == "done" and s.get("input") == input_hash

    def get(self, step: str, scene: str | None = None) -> dict:
        return self._slot(step, scene)

    def mark(self, step: str, status: str, scene: str | None = None, input_hash: str | None = None, **result) -> None:
        s = self._slot(step, scene)
        s["status"] = status
        s["ts"] = time.time()
        if input_hash is not None:
            s["input"] = input_hash
        s.update(result)
        self.save()

    def invalidate_scene(self, scene: str, from_step: str = "clips") -> None:
        """Szene gezielt neu machen: Schritt und alle nachfolgenden Szenen-Schritte löschen."""
        sc = self.data["scenes"].get(scene, {})
        idx = STAGES.index(from_step)
        for st in STAGES[idx:]:
            sc.pop(st, None)
        # Gesamtschritte danach müssen auch neu
        for st in ("audio", "edit", "qc_final", "export"):
            self.data["steps"].pop(st, None)
        self.save()

    def add_spend(self, usd: float, what: str) -> None:
        self.data["spend_usd"] = round(self.data.get("spend_usd", 0.0) + usd, 4)
        self.data.setdefault("spend_log", []).append({"ts": time.time(), "usd": round(usd, 4), "what": what})
        self.save()
