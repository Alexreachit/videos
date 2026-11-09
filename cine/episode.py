"""Episoden-/Szenenmodell. Eine Episode ist eine YAML-Datei unter episodes/."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REQUIRED_SCENE_FIELDS = ("id", "beat", "duration", "environment", "time_of_day", "lighting", "weather",
                         "camera", "movement", "objects", "zombies", "action", "mood", "sound", "continuity")


@dataclass
class SoundCue:
    t: float          # Sekunde innerhalb der Szene
    kind: str         # heartbeat | breath | footsteps | growl | impact | click | door | drone | stinger | metal | scream | glass
    gain_db: float = 0.0
    dur: float | None = None
    note: str = ""


@dataclass
class Scene:
    id: str
    beat: str
    duration: float
    environment: str
    time_of_day: str
    lighting: str
    weather: str
    camera: str
    movement: str
    objects: list[str]
    zombies: str
    action: str
    mood: str
    sound: str
    continuity: str
    cues: list[SoundCue] = field(default_factory=list)
    transition_in: str = "cut"   # cut | whip | dip | flash
    chain_from_previous: bool = True  # letzter Frame der Vorszene als Startbild
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Episode:
    id: str
    title: str
    logline: str
    style: dict[str, Any]
    protagonist: dict[str, Any]
    zombie_design: dict[str, Any]
    scenes: list[Scene]
    settings: dict[str, Any] = field(default_factory=dict)
    references: list[dict[str, Any]] = field(default_factory=list)
    source: Path | None = None

    @property
    def total_duration(self) -> float:
        return round(sum(s.duration for s in self.scenes), 2)

    def scene(self, sid: str) -> Scene:
        for s in self.scenes:
            if s.id == sid:
                return s
        raise KeyError(f"Szene {sid!r} nicht in Episode {self.id}")


class EpisodeError(ValueError):
    pass


def load_episode(path: str | Path) -> Episode:
    path = Path(path)
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    scenes = []
    for i, sd in enumerate(d.get("scenes", []), 1):
        missing = [f for f in REQUIRED_SCENE_FIELDS if f not in sd]
        if missing:
            raise EpisodeError(f"Szene {sd.get('id', i)}: Felder fehlen: {', '.join(missing)}")
        cues = [SoundCue(**c) for c in sd.get("cues", [])]
        for c in cues:
            if not 0 <= c.t <= float(sd["duration"]):
                raise EpisodeError(f"Szene {sd['id']}: Sound-Cue {c.kind} bei {c.t}s liegt außerhalb der Szene")
        known = set(REQUIRED_SCENE_FIELDS) | {"cues", "transition_in", "chain_from_previous"}
        scenes.append(Scene(
            **{k: sd[k] for k in REQUIRED_SCENE_FIELDS if k not in ("objects",)},
            objects=list(sd["objects"]), cues=cues,
            transition_in=sd.get("transition_in", "cut"),
            chain_from_previous=sd.get("chain_from_previous", i > 1),
            extra={k: v for k, v in sd.items() if k not in known},
        ))
    if not scenes:
        raise EpisodeError("Episode hat keine Szenen")
    ids = [s.id for s in scenes]
    if len(set(ids)) != len(ids):
        raise EpisodeError("Szenen-IDs sind nicht eindeutig")
    for s in scenes:
        if not 3 <= float(s.duration) <= 15:
            raise EpisodeError(f"Szene {s.id}: Dauer {s.duration}s – Videomodelle können 3–15 s pro Clip")
    return Episode(id=d["id"], title=d["title"], logline=d.get("logline", ""), style=d.get("style", {}),
                   protagonist=d.get("protagonist", {}), zombie_design=d.get("zombie_design", {}),
                   scenes=scenes, settings=d.get("settings", {}), references=d.get("references", []), source=path)
