"""Kostenloser Weg über Web-Oberflächen mit Gratis-Kontingent.

Das System schreibt pro Szene eine Prompt-Karte (handoff/<szene>.md) samt Startbild
und Referenzbildern. Du erzeugst den Clip z. B. in Google Vids oder Google Flow
(Gratis-Kontingent) und legst ihn als inbox/<szene>.mp4 ab. Der nächste Lauf
übernimmt ihn automatisch und macht mit Ton, Schnitt und Prüfung weiter.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from .base import ClipRequest, ImageProvider, NeedsManualInput, VideoProvider


def _card(path: Path, title: str, body: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([f"# {title}", ""] + body) + "\n", encoding="utf-8")


class ManualVideo(VideoProvider):
    name = "manual"
    supports_first_frame = True
    supports_references = True
    native_audio = True  # Gratis-Webtools (Vids/Flow) liefern meist Ton mit

    def generate(self, req: ClipRequest, out: Path):
        prod = self.ctx.prod
        inbox = prod.sub("inbox")
        found = next((inbox / f"{req.scene_id}{ext}" for ext in (".mp4", ".mov", ".webm")
                      if (inbox / f"{req.scene_id}{ext}").exists()), None)
        if found:
            out.parent.mkdir(parents=True, exist_ok=True)
            if found.suffix == ".mp4":
                shutil.copy2(found, out)
            else:
                from ..util import run
                run(["ffmpeg", "-y", "-loglevel", "error", "-i", found, "-c:v", "libx264", "-crf", "18",
                     "-c:a", "aac", out])
            return {"provider": "manual", "source": str(found.name), "usd": 0.0, "native_audio": True}
        hand = prod.sub("handoff")
        files = []
        if req.first_frame and Path(req.first_frame).exists():
            dst = hand / f"{req.scene_id}_startbild{Path(req.first_frame).suffix}"
            shutil.copy2(req.first_frame, dst)
            files.append(f"- Startbild: `{dst.name}` (als erstes Bild / Start-Frame hochladen)")
        for i, r in enumerate(req.reference_images):
            if Path(r).exists():
                dst = hand / f"{req.scene_id}_ref{i}{Path(r).suffix}"
                shutil.copy2(r, dst)
                files.append(f"- Referenz {i}: `{dst.name}` (als Charakter-/Stil-Referenz)")
        _card(hand / f"{req.scene_id}.md", f"Szene {req.scene_id} – Clip erzeugen", [
            f"**Dauer:** {req.duration:.0f} s · **Format:** {self.ctx.cfg['render']['aspect']}"
            f" · **Auflösung:** {self.ctx.cfg['render']['resolution']}", "",
            "**Prompt (komplett kopieren):**", "", "```", req.prompt, "```", "",
            "**Vermeiden:**", "", "```", req.negative, "```", "",
            *(["**Dateien:**", *files, ""] if files else []),
            f"**Ablage:** fertigen Clip als `inbox/{req.scene_id}.mp4` speichern, dann Pipeline erneut starten.",
        ])
        raise NeedsManualInput(f"Szene {req.scene_id}: wartet auf inbox/{req.scene_id}.mp4",
                               [hand / f"{req.scene_id}.md"])


class ManualImage(ImageProvider):
    name = "manual"

    def generate(self, ref_id, prompt, out: Path, inputs=None):
        inbox = self.ctx.prod.sub("inbox")
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            f = inbox / f"{ref_id}{ext}"
            if f.exists():
                from PIL import Image
                out.parent.mkdir(parents=True, exist_ok=True)
                Image.open(f).convert("RGB").save(out, quality=95)
                return {"provider": "manual", "source": f.name, "usd": 0.0}
        hand = self.ctx.prod.sub("handoff")
        _card(hand / f"{ref_id}.md", f"Referenzbild {ref_id}", [
            "**Prompt (z. B. in Gemini):**", "", "```", prompt, "```", "",
            f"**Ablage:** als `inbox/{ref_id}.png` speichern."])
        raise NeedsManualInput(f"Referenz {ref_id}: wartet auf inbox/{ref_id}.png", [hand / f"{ref_id}.md"])
