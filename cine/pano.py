"""360°-POV-Renderer (Machart wie @humanlabbzz-Referenz).

Prinzip: Ein Schauplatz ist EIN 360°-Panoramabild (equirectangular, 2:1). Eine
virtuelle Kamera mit sehr weitem Bildwinkel (stereografische Projektion =
der typische "Fischaugen"-Look mit gebogenen Decken) dreht sich darin wie ein
Kopf: umsehen, runter auf die Hände, hoch zur Decke, zu einer Figur. Dazu kleine
Atem-/Gehbewegungen. Alles läuft lokal mit numpy/OpenCV – kostenlos.

Kamera-Keyframes: (t, yaw, pitch, fov) in Grad. yaw 0 = Bildmitte des Panoramas,
positiv nach rechts; pitch positiv nach oben; fov = horizontaler Bildwinkel.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class Key:
    t: float
    yaw: float
    pitch: float = 0.0
    fov: float = 120.0
    ease: str = "inout"   # inout | linear | snap (schneller Blickwechsel)


def _ease(u: float, kind: str) -> float:
    u = min(1.0, max(0.0, u))
    if kind == "linear":
        return u
    if kind == "snap":       # schneller Kopfruck mit weichem Auslaufen
        return 1 - (1 - u) ** 4
    return u * u * (3 - 2 * u)


def camera_at(keys: list[Key], t: float) -> tuple[float, float, float]:
    if t <= keys[0].t:
        k = keys[0]
        return k.yaw, k.pitch, k.fov
    for a, b in zip(keys, keys[1:]):
        if t <= b.t:
            u = _ease((t - a.t) / max(1e-6, b.t - a.t), b.ease)
            dy = (b.yaw - a.yaw + 180) % 360 - 180          # kürzester Weg
            return a.yaw + dy * u, a.pitch + (b.pitch - a.pitch) * u, a.fov + (b.fov - a.fov) * u
    k = keys[-1]
    return k.yaw, k.pitch, k.fov


def head_motion(t: float, walk: float = 0.0, seed: float = 0.0) -> tuple[float, float]:
    """Natürliches Mikrowackeln (Atmen) + optional Gehen (walk 0..1)."""
    y = 0.6 * math.sin(t * 0.7 + seed) + 0.25 * math.sin(t * 1.9 + seed * 2)
    p = 0.5 * math.sin(t * 1.1 + seed * 3) + 0.2 * math.sin(t * 2.7)
    if walk:
        y += walk * 1.2 * math.sin(t * 2 * math.pi * 0.95)
        p += walk * 1.6 * abs(math.sin(t * 2 * math.pi * 0.95))
    return y, p


class PanoCamera:
    """Rendert Ansichten aus einem Panorama. Rays werden einmal pro Größe vorberechnet."""

    def __init__(self, pano: np.ndarray, out_w: int, out_h: int):
        if abs(pano.shape[1] / pano.shape[0] - 2) > 0.05:
            pano = cv2.resize(pano, (pano.shape[0] * 2, pano.shape[0]), interpolation=cv2.INTER_CUBIC)
        # Naht entschärfen: Ränder überlappend einbetten, damit remap über yaw=±180 interpoliert
        self.pad = 8
        self.pano = cv2.copyMakeBorder(pano, 0, 0, self.pad, self.pad, cv2.BORDER_WRAP)
        self.ph, self.pw = pano.shape[:2]
        self.w, self.h = out_w, out_h
        xs = (np.arange(out_w) + 0.5) / out_w * 2 - 1
        ys = (np.arange(out_h) + 0.5) / out_h * 2 - 1
        self.u, self.v = np.meshgrid(xs, ys * out_h / out_w)

    def render(self, yaw: float, pitch: float, fov: float) -> np.ndarray:
        # Stereografische Projektion: r = 2 tan(theta/2); fov bezieht sich auf die Bildbreite
        k = 2 * math.tan(math.radians(fov) / 4)
        x, y = self.u * k, -self.v * k
        r2 = x * x + y * y
        # Strahl in Kamerakoordinaten (z nach vorne)
        dz = (4 - r2) / (4 + r2)
        dx = 4 * x / (4 + r2)
        dy = 4 * y / (4 + r2)
        cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
        cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        # Pitch um x-Achse, dann Yaw um y-Achse
        y1 = dy * cp + dz * sp
        z1 = -dy * sp + dz * cp
        x2 = dx * cy + z1 * sy
        z2 = -dx * sy + z1 * cy
        lon = np.arctan2(x2, z2)
        lat = np.arcsin(np.clip(y1, -1, 1))
        mx = ((lon / (2 * math.pi) + 0.5) * self.pw + self.pad).astype(np.float32)
        my = ((0.5 - lat / math.pi) * self.ph).astype(np.float32)
        return cv2.remap(self.pano, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


def fix_seam(pano: np.ndarray, width: int = 24) -> np.ndarray:
    """KI-Panoramen haben oft eine sichtbare Naht links/rechts – sanft überblenden."""
    p = pano.astype(np.float32)
    left, right = p[:, :width].copy(), p[:, -width:].copy()
    a = np.linspace(0, 1, width)[None, :, None]
    mix = (left + right) / 2
    p[:, :width] = left * a + mix * (1 - a)
    p[:, -width:] = right * (1 - a) + mix * a
    return p.clip(0, 255).astype(np.uint8)
