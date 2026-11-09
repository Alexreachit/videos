"""Konfiguration laden: default.yaml + Episoden-Settings + Umgebungsvariablen."""
from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "default.yaml"
REPO = ROOT.parent


def deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_env_file(path: Path | None = None) -> None:
    """Liest eine lokale .env (falls vorhanden) – überschreibt nichts Bestehendes."""
    path = path or REPO / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_config(episode_settings: dict | None = None, overrides: dict | None = None) -> dict[str, Any]:
    cfg = yaml.safe_load(DEFAULT_CONFIG.read_text(encoding="utf-8"))
    cfg = deep_merge(cfg, episode_settings or {})
    cfg = deep_merge(cfg, overrides or {})
    # Anbieter per Umgebungsvariable umstellbar (z. B. in GitHub Actions)
    for step in ("image", "video", "sfx", "vision_qc"):
        env = os.environ.get(f"CINE_{step.upper()}_PROVIDER")
        if env:
            cfg["providers"][step] = env
    return cfg


def dimensions(cfg: dict) -> tuple[int, int]:
    res = cfg["render"]["resolution"]
    short = {"360p": 360, "480p": 480, "720p": 720, "1080p": 1080}[res]
    long_ = {360: 640, 480: 854, 720: 1280, 1080: 1920}[short]
    if cfg["render"]["aspect"] == "9:16":
        return short, long_
    return long_, short
