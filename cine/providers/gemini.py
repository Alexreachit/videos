"""Kostenpflichtig: KI-Bildprüfung über die Gemini API (generateContent).

Bekommt ein Kontaktblatt (mehrere Einzelbilder eines Clips) und eine Checkliste
und liefert eine Bewertung als JSON. API-Schlüssel: GEMINI_API_KEY.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from ..cost import vision_cost
from ..util import TransientError, retry
from .base import VisionProvider

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


@retry(times=3)
def _post(url: str, body: dict) -> dict:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY fehlt (GitHub Secret oder .env)")
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code in (429, 500, 503):
            raise TransientError(f"HTTP {e.code}") from e
        raise RuntimeError(f"Gemini HTTP {e.code}: {e.read().decode(errors='ignore')[:300]}") from e


class GeminiVision(VisionProvider):
    name = "gemini"
    paid = True

    def review(self, scene_id: str, contact_sheet: Path, checklist: list[str]):
        model = self.ctx.cfg["models"]["gemini"]["vision"]
        usd = vision_cost(self.ctx.cfg, 1)
        what = f"KI-Prüfung {scene_id}"
        self.ctx.guard.charge(usd, what)
        prompt = (
            "Du prüfst Einzelbilder (links oben nach rechts unten, zeitlich geordnet) eines KI-generierten "
            "First-Person-Zombie-Thriller-Clips. Bewerte streng. Antworte NUR als JSON: "
            '{"score": 0-100, "issues": ["..."], "checks": {"<kriterium>": true/false}}. Kriterien:\n- '
            + "\n- ".join(checklist))
        body = {"contents": [{"parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(contact_sheet.read_bytes()).decode()}},
        ]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}}
        try:
            res = _post(API.format(model=model), body)
        finally:
            self.ctx.guard.commit(usd, what)
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(text)
        data["score"] = max(0, min(100, int(data.get("score", 0))))
        data["usd"] = usd
        return data
