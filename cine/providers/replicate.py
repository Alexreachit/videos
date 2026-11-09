"""Kostenpflichtig: Replicate-API (eine REST-Schnittstelle für viele Modelle).

Doku: https://replicate.com/docs/reference/http
Jeder Aufruf geht vorher durch den CostGuard. API-Schlüssel: REPLICATE_API_TOKEN.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from ..cost import image_cost, video_cost
from ..util import TransientError, log, retry
from .base import ClipRequest, ImageProvider, VideoProvider

API = "https://api.replicate.com/v1"

# Eingabefelder je Modell. Gemini Omni: `image` (Startbild) und `reference_images`
# schließen sich gegenseitig aus (laut Modellseite).
INPUT_MAP = {
    "google/gemini-omni-1.2-flash": {"first_frame": "image", "refs": "reference_images", "exclusive": True,
                                     "duration": "duration", "resolution": "resolution",
                                     "aspect": "aspect_ratio", "negative": None, "max_refs": 6},
    "_default": {"first_frame": "start_image", "refs": None, "exclusive": True, "duration": "duration",
                 "resolution": None, "aspect": "aspect_ratio", "negative": "negative_prompt", "max_refs": 0},
}


def _token() -> str:
    t = os.environ.get("REPLICATE_API_TOKEN")
    if not t:
        raise RuntimeError("REPLICATE_API_TOKEN fehlt (GitHub Secret oder .env)")
    return t


def _data_uri(p: Path) -> str:
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(Path(p).read_bytes()).decode()}"


@retry(times=4)
def _http(method: str, url: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="ignore")[:400]
        if e.code in (429, 500, 502, 503, 504):
            raise TransientError(f"HTTP {e.code}: {msg}") from e
        raise RuntimeError(f"Replicate HTTP {e.code}: {msg}") from e
    except urllib.error.URLError as e:
        raise TransientError(str(e)) from e


@retry(times=4)
def _download(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=300) as r, open(out, "wb") as f:
            f.write(r.read())
    except urllib.error.URLError as e:
        raise TransientError(str(e)) from e


def run_prediction(model: str, inp: dict, timeout_s: int = 1500) -> dict:
    pred = _http("POST", f"{API}/models/{model}/predictions", {"input": inp})
    url = pred["urls"]["get"]
    t0 = time.time()
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        if time.time() - t0 > timeout_s:
            raise TimeoutError(f"{model}: keine Antwort nach {timeout_s}s (ID {pred.get('id')})")
        time.sleep(5)
        pred = _http("GET", url)
    if pred["status"] != "succeeded":
        raise RuntimeError(f"{model}: {pred['status']} – {pred.get('error')}")
    return pred


def _first_url(output) -> str:
    if isinstance(output, str):
        return output
    if isinstance(output, list) and output:
        return output[0]
    if isinstance(output, dict):
        return next(iter(output.values()))
    raise RuntimeError(f"Unerwartete Ausgabe: {output!r}")


class ReplicateVideo(VideoProvider):
    name = "replicate"
    paid = True
    native_audio = True
    supports_first_frame = True
    supports_references = True

    def generate(self, req: ClipRequest, out: Path):
        cfg = self.ctx.cfg
        model = cfg["models"]["replicate"]["video"]
        m = INPUT_MAP.get(model, INPUT_MAP["_default"])
        secs = int(round(req.duration))
        usd = video_cost(cfg, secs)
        what = f"Clip {req.scene_id} (Versuch {req.attempt}, {secs}s, {model})"
        self.ctx.guard.charge(usd, what)  # bricht ab, falls nicht freigegeben
        inp = {"prompt": req.prompt}
        if m["duration"]:
            inp[m["duration"]] = secs
        if m["resolution"]:
            inp[m["resolution"]] = cfg["render"]["resolution"]
        if m["aspect"]:
            inp[m["aspect"]] = cfg["render"]["aspect"]
        if m["negative"] and req.negative:
            inp[m["negative"]] = req.negative
        if req.first_frame and m["first_frame"]:
            inp[m["first_frame"]] = _data_uri(req.first_frame)
        elif req.reference_images and m["refs"]:
            inp[m["refs"]] = [_data_uri(p) for p in req.reference_images[: m["max_refs"]]]
        if req.seed is not None:
            inp["seed"] = req.seed
        log.info("Replicate: %s", what)
        try:
            pred = run_prediction(model, inp)
        finally:
            # konservativ: jeder angenommene Auftrag wird als Ausgabe verbucht
            self.ctx.guard.commit(usd, what)
        _download(_first_url(pred["output"]), out)
        return {"provider": "replicate", "model": model, "usd": usd, "prediction": pred.get("id"),
                "native_audio": True, "inputs": sorted(k for k in inp if k != "prompt")}


class ReplicateImage(ImageProvider):
    name = "replicate"
    paid = True

    def generate(self, ref_id, prompt, out: Path, inputs=None):
        cfg = self.ctx.cfg
        model = cfg["models"]["replicate"]["image"]
        usd = image_cost(cfg, 1)
        what = f"Referenzbild {ref_id} ({model})"
        self.ctx.guard.charge(usd, what)
        inp = {"prompt": prompt, "aspect_ratio": cfg["render"]["aspect"], "output_format": "png"}
        if inputs:
            inp["image_input"] = [_data_uri(p) for p in inputs]
        try:
            pred = run_prediction(model, inp, timeout_s=600)
        finally:
            self.ctx.guard.commit(usd, what)
        _download(_first_url(pred["output"]), out)
        return {"provider": "replicate", "model": model, "usd": usd, "prediction": pred.get("id")}
