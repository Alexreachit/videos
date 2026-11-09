"""Hilfsfunktionen: Logging, Retry, ffmpeg-Aufrufe, Hashes, atomares Schreiben."""
from __future__ import annotations

import functools
import hashlib
import json
import logging
import os
import random
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

log = logging.getLogger("cine")


def setup_logging(logfile: Path | None = None, level: int = logging.INFO) -> None:
    root = logging.getLogger("cine")
    root.setLevel(level)
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler) for h in root.handlers):
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%H:%M:%S"))
        root.addHandler(sh)
    if logfile:
        logfile.parent.mkdir(parents=True, exist_ok=True)
        if not any(isinstance(h, logging.FileHandler) and Path(h.baseFilename) == logfile.resolve() for h in root.handlers):
            fh = logging.FileHandler(logfile, encoding="utf-8")
            fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
            root.addHandler(fh)


class TransientError(Exception):
    """Fehler, bei dem ein erneuter Versuch sinnvoll ist (Netz, 5xx, Rate-Limit)."""


def retry(times: int = 4, base: float = 2.0, cap: float = 60.0, on: tuple = (TransientError,)):
    def deco(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            for attempt in range(1, times + 1):
                try:
                    return fn(*a, **kw)
                except on as e:  # noqa: PERF203
                    if attempt == times:
                        raise
                    wait = min(cap, base ** attempt) * (0.7 + 0.6 * random.random())
                    log.warning("%s fehlgeschlagen (%s), Versuch %d/%d in %.0fs", fn.__name__, e, attempt, times, wait)
                    time.sleep(wait)
        return wrapper
    return deco


def sha(obj: Any, n: int = 10) -> str:
    data = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()[:n]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    log.debug("$ %s", " ".join(map(str, cmd)))
    p = subprocess.run(list(map(str, cmd)), capture_output=True, text=True, **kw)
    if p.returncode != 0:
        raise RuntimeError(f"Befehl fehlgeschlagen ({p.returncode}): {' '.join(map(str, cmd[:6]))} …\n{p.stderr[-1500:]}")
    return p


def ffprobe(path: Path) -> dict:
    p = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path])
    return json.loads(p.stdout)


def media_info(path: Path) -> dict:
    j = ffprobe(path)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    info = {"duration": float(j["format"].get("duration", 0) or 0), "has_audio": a is not None}
    if v:
        num, den = (v.get("avg_frame_rate") or "0/1").split("/")
        info.update(width=int(v["width"]), height=int(v["height"]),
                    fps=(float(num) / float(den)) if float(den) else 0.0, vcodec=v.get("codec_name"))
    return info
