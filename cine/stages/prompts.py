"""Schritt: Szenen-Prompts bauen (versioniert).

Jeder Prompt enthält Umgebung, Tageszeit, Licht, Wetter, Kamera, Bewegung,
sichtbare Objekte, Zombies, Handlung, Stimmung, Ton und Anschluss an die
Vorszene – plus die festen Regeln der Episode (POV, Hände, Zombie-Design,
Look). Jede Änderung am Text ergibt einen neuen Hash -> nur diese Szene
wird neu generiert.
"""
from __future__ import annotations

from ..episode import Episode, Scene
from ..util import sha

PROMPT_VERSION = 4   # erhöhen, wenn sich die Prompt-Vorlage ändert

POV_RULES = (
    "Strict first-person POV: the camera IS the eyes of the protagonist. Never show the protagonist from outside, "
    "no third-person shots, no cuts, no camera teleporting, one continuous handheld take. "
    "Natural head motion: subtle sway, breathing bob, quick glances, realistic motion blur on fast turns."
)

NEGATIVE = (
    "third-person view, over-the-shoulder shot, protagonist's face visible, mirror selfie, cut, scene change, "
    "text, subtitles, watermark, logo, cartoon, CGI look, video game HUD, crosshair, extra fingers, deformed hands, "
    "floating objects, morphing faces, changing clothes, sudden daylight, slow-motion, music video look, "
    "zombies running like athletes in unison, comedic tone"
)


def _c(x) -> str:
    """Whitespace glätten, Schlusspunkt entfernen (der Satzbau setzt ihn selbst)."""
    return " ".join(str(x).split()).rstrip(". ")


def scene_prompt(ep: Episode, s: Scene, prev: Scene | None, uses_refs: bool, uses_first_frame: bool) -> str:
    st = {k: _c(v) for k, v in ep.style.items()}
    pr = {k: _c(v) for k, v in ep.protagonist.items()}
    zd = {k: _c(v) for k, v in ep.zombie_design.items()}
    s = Scene(**{**s.__dict__, **{k: _c(getattr(s, k)) for k in ("environment", "time_of_day", "lighting", "weather",
                                                                 "camera", "movement", "zombies", "action", "mood",
                                                                 "sound", "continuity")}})
    lines = [
        f"{st.get('look', 'Photorealistic cinematic horror')}. {POV_RULES}",
        f"Scene: {s.environment}. Time: {s.time_of_day}. Weather: {s.weather}.",
        f"Lighting: {s.lighting}.",
        f"Camera: {s.camera}. Movement: {s.movement}.",
        f"Visible: {', '.join(s.objects)}.",
        f"Protagonist (only hands/forearms may be visible): {pr.get('hands', '')}. Holding: {pr.get('carry', '')}.",
        f"Zombies: {s.zombies}. Zombie look: {zd.get('look', '')}. Zombie motion: {zd.get('motion', '')}.",
        f"Action: {s.action}.",
        f"Mood: {s.mood}.",
        f"Audio: {s.sound}. {st.get('audio_rules', 'No music, no dialogue, diegetic sound only')}.",
    ]
    if prev is not None and s.chain_from_previous:
        lines.append(f"Continuity: {s.continuity}." + (" The video starts exactly on the provided start frame."
                                                      if uses_first_frame else ""))
    else:
        lines.append(f"Continuity: {s.continuity}.")
    if uses_refs:
        lines.append("Keep hands, sleeves, gloves and flashlight identical to the reference images.")
    lines.append(f"Film look: {st.get('grade', '')}. {st.get('lens', '')}.")
    return "\n".join(l.strip() for l in lines if l.strip())


def build_all(ep: Episode, video_provider) -> dict[str, dict]:
    out = {}
    prev = None
    for s in ep.scenes:
        chained = bool(prev and s.chain_from_previous and video_provider.supports_first_frame)
        refs = (not chained) and video_provider.supports_references and bool(ep.references)
        text = scene_prompt(ep, s, prev, refs, chained)
        neg = NEGATIVE + (", " + _c(ep.style["negative_extra"]) if ep.style.get("negative_extra") else "")
        out[s.id] = {"prompt": text, "negative": neg, "version": PROMPT_VERSION,
                     "uses_first_frame": chained, "uses_refs": refs,
                     "hash": sha([PROMPT_VERSION, text, neg, chained, refs])}
        prev = s
    return out
