"""Provider-Registry: Name aus der Konfiguration -> Klasse."""
from __future__ import annotations

from .base import AudioProvider, ImageProvider, VideoProvider, VisionProvider


def get_video(name: str, ctx) -> VideoProvider:
    if name == "mock":
        from .mock import MockVideo
        return MockVideo(ctx)
    if name == "manual":
        from .manual import ManualVideo
        return ManualVideo(ctx)
    if name == "replicate":
        from .replicate import ReplicateVideo
        return ReplicateVideo(ctx)
    raise ValueError(f"Unbekannter Video-Provider: {name}")


def get_image(name: str, ctx) -> ImageProvider:
    if name == "mock":
        from .mock import MockImage
        return MockImage(ctx)
    if name == "manual":
        from .manual import ManualImage
        return ManualImage(ctx)
    if name == "replicate":
        from .replicate import ReplicateImage
        return ReplicateImage(ctx)
    raise ValueError(f"Unbekannter Bild-Provider: {name}")


def get_sfx(name: str, ctx) -> AudioProvider:
    if name == "procedural":
        from .procedural_audio import ProceduralSfx
        return ProceduralSfx(ctx)
    if name == "elevenlabs":
        from .elevenlabs import ElevenLabsSfx
        return ElevenLabsSfx(ctx)
    raise ValueError(f"Unbekannter Sound-Provider: {name}")


def get_vision(name: str, ctx) -> VisionProvider | None:
    if name == "none":
        return None
    if name == "gemini":
        from .gemini import GeminiVision
        return GeminiVision(ctx)
    raise ValueError(f"Unbekannter Vision-Provider: {name}")
