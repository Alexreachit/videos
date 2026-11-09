"""Schnittstellen aller Anbieter. Neue Modelle = neue Unterklasse, sonst nichts."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Ctx:
    """Was ein Provider braucht: Konfiguration, Produktion, Kostenwächter."""
    cfg: dict
    prod: Any          # cine.state.Production
    guard: Any         # cine.cost.CostGuard
    width: int
    height: int


@dataclass
class ClipRequest:
    scene_id: str
    prompt: str
    negative: str
    duration: float
    first_frame: Path | None = None
    reference_images: list[Path] = field(default_factory=list)
    seed: int | None = None
    attempt: int = 1


class NeedsManualInput(RuntimeError):
    """Der Schritt wartet auf eine Datei, die der Nutzer ablegen soll (kostenloser Weg)."""

    def __init__(self, msg: str, paths: list[Path]):
        super().__init__(msg)
        self.paths = paths


class VideoProvider(ABC):
    name = "base"
    paid = False
    native_audio = False
    supports_first_frame = False
    supports_references = False

    def __init__(self, ctx: Ctx):
        self.ctx = ctx

    @abstractmethod
    def generate(self, req: ClipRequest, out: Path) -> dict[str, Any]:
        """Erzeugt einen Clip nach `out` (mp4). Rückgabe: Metadaten (Modell, Kosten, Seed …)."""


class ImageProvider(ABC):
    name = "base"
    paid = False

    def __init__(self, ctx: Ctx):
        self.ctx = ctx

    @abstractmethod
    def generate(self, ref_id: str, prompt: str, out: Path, inputs: list[Path] | None = None) -> dict[str, Any]:
        ...


class AudioProvider(ABC):
    name = "base"
    paid = False

    def __init__(self, ctx: Ctx):
        self.ctx = ctx

    @abstractmethod
    def sfx(self, kind: str, duration: float, out: Path, note: str = "", seed: int = 0) -> dict[str, Any]:
        """Einzelnes Geräusch als WAV (48 kHz, mono)."""

    @abstractmethod
    def ambience(self, mood: str, duration: float, out: Path, seed: int = 0) -> dict[str, Any]:
        """Atmosphäre/Drone unter der Szene."""


class VisionProvider(ABC):
    name = "base"
    paid = True

    def __init__(self, ctx: Ctx):
        self.ctx = ctx

    @abstractmethod
    def review(self, scene_id: str, contact_sheet: Path, checklist: list[str]) -> dict[str, Any]:
        """Bewertet ein Kontaktblatt eines Clips: {'score': 0-100, 'issues': [...]}"""
