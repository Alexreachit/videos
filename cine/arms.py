"""POV-Arme als 2D-Gelenkmodell (Cutout-Rig) + Handy mit echtem Bildschirm.

Aus EINEM Gemini-Bild (beide Unterarme mit Händen vor Grün) werden pro Arm zwei
Teile geschnitten: Unterarm (Ärmel) und Hand (bei rechts: inkl. Handy). Die Teile
drehen sich um echte Gelenkpunkte:
  Ellbogen (unterhalb des Bildes)  -> ganzer Arm schwenkt, kommt näher (Skalierung)
  Handgelenk (an der Ärmelkante)   -> Hand kippt, folgt mit leichter Verzögerung
Posen werden zwischen Keyframes weich überblendet; dazu Atmen und Nachschwingen.

Der Handybildschirm wird perspektivisch korrekt in die Displayfläche eingesetzt
(aus = schwarz mit Spiegelung, an = Sperrbildschirm mit Uhrzeit und Nachricht).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Geometrie des Quellbilds panos/hands_phone.jpg (768x1376), von Hand am Bild vermessen
SRC_W = 768
RIG = {
    "right": {"elbow": (820, 1520), "wrist": (622, 1052),
              "cuff": ((540, 1068), (768, 1022)),          # Linie Ärmelkante (Hand liegt darüber)
              "screen": [(473, 732), (590, 733), (583, 980), (462, 975)]},   # TL TR BR BL
    "left": {"elbow": (-80, 1500), "wrist": (178, 1084),
             "cuff": ((40, 1022), (250, 1125)), "screen": None},
}

# Posen: rot = Unterarm um Ellbogen (Grad, + = im Uhrzeigersinn), wrist = Hand um Handgelenk,
# dx/dy = Verschiebung in Pixeln (Videogröße 720 breit), s = Nähe zur Kamera
POSES = {
    "right": {
        "unten":   dict(rot=16, wrist=12, dx=40, dy=330, s=1.00),   # Handy liegt tief, kaum sichtbar
        "halten":  dict(rot=4, wrist=4, dx=10, dy=120, s=1.00),     # locker in der Hand
        "lesen":   dict(rot=-10, wrist=-6, dx=-70, dy=-40, s=1.32), # Handy nah vors Gesicht
        "zeigen":  dict(rot=-24, wrist=-16, dx=-150, dy=-110, s=0.86),  # Handy jemandem hinhalten
        "weg":     dict(rot=30, wrist=20, dx=120, dy=620, s=1.00),  # aus dem Bild
    },
    "left": {
        "unten":   dict(rot=-14, wrist=-8, dx=-40, dy=360, s=1.00),
        "bereit":  dict(rot=-4, wrist=-4, dx=-10, dy=150, s=1.00),
        "abwehr":  dict(rot=2, wrist=-12, dx=10, dy=90, s=1.12),    # Hand zuckt hoch, Schutzreflex
        "greifen": dict(rot=6, wrist=4, dx=50, dy=110, s=1.05),
        "weg":     dict(rot=-30, wrist=-20, dx=-140, dy=640, s=1.00),
    },
}


def _ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


# ------------------------------------------------------------------ Bildschirm
def lock_screen(w: int, h: int, clock: str, date: str, msg: tuple[str, str] | None) -> Image.Image:
    """Sperrbildschirm wie im Referenzvideo: lila Verlauf, große Uhr, Nachrichtenkarte."""
    img = Image.new("RGB", (w, h))
    top, bot = np.array([86, 46, 140]), np.array([28, 14, 58])
    grad = (top[None, :] * (1 - np.linspace(0, 1, h)[:, None]) + bot[None, :] * np.linspace(0, 1, h)[:, None])
    img = Image.fromarray(np.repeat(grad[:, None, :], w, axis=1).astype(np.uint8))
    d = ImageDraw.Draw(img)
    fd, fc = _font(int(w * 0.07), False), _font(int(w * 0.26))
    tw = d.textlength(date, font=fd)
    d.text(((w - tw) / 2, h * 0.07), date, font=fd, fill=(230, 220, 245))
    tw = d.textlength(clock, font=fc)
    d.text(((w - tw) / 2, h * 0.11), clock, font=fc, fill=(255, 255, 255))
    if msg:
        sender, text = msg
        m = int(w * 0.06)
        y0 = int(h * 0.36)
        fs, ft = _font(int(w * 0.075)), _font(int(w * 0.082))
        words, lines, line = text.split(), [], ""
        for wd in words:
            c = (line + " " + wd).strip()
            if d.textlength(c, font=ft) > w - 4 * m:
                lines.append(line)
                line = wd
            else:
                line = c
        lines.append(line)
        lines = lines[:4]
        ch = int(fs.size * 1.6 + len(lines) * ft.size * 1.2 + m)
        d.rounded_rectangle([m, y0, w - m, y0 + ch], radius=int(w * 0.07), fill=(245, 242, 250))
        d.text((m * 2, y0 + m * 0.6), sender, font=fs, fill=(40, 30, 60))
        y = y0 + m * 0.6 + fs.size * 1.4
        for ln in lines:
            d.text((m * 2, y), ln, font=ft, fill=(20, 20, 30))
            y += ft.size * 1.2
    return img


def _screen_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return np.asarray(m, np.float32) / 255


# ------------------------------------------------------------------ Rig
@dataclass
class Part:
    rgba: np.ndarray       # Canvas-große RGBA-Ebene (float32 0..1 alpha separat)


class ArmRig:
    def __init__(self, src_path, W: int, H: int):
        img = cv2.imread(str(src_path))
        if img is None:
            raise FileNotFoundError(src_path)
        self.k = W / img.shape[1]
        img = cv2.resize(img, (W, int(img.shape[0] * self.k)), interpolation=cv2.INTER_AREA)
        self.W, self.H = W, H
        self.yoff = H - img.shape[0]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green = cv2.inRange(hsv, (45, 150, 140), (78, 255, 255))   # nur reines Chroma-Grün, Oliv-Ärmel bleibt
        alpha = (255 - green).astype(np.float32)
        alpha = cv2.GaussianBlur(cv2.erode(alpha, np.ones((3, 3), np.uint8)), (3, 3), 0) / 255
        b, g, r = cv2.split(img)
        g = np.minimum(g, np.maximum(b, r).astype(np.int16) + 20).clip(0, 255).astype(np.uint8)
        rgb = cv2.merge([r, g, b]).astype(np.float32)
        self.EXT = EXT = 800   # Ärmel laufen unten aus dem Bild weiter
        canvas = np.zeros((H + EXT, W, 4), np.float32)
        y0 = max(0, self.yoff)
        canvas[y0:H, :, :3] = rgb[y0 - self.yoff:y0 - self.yoff + (H - y0)]
        canvas[y0:H, :, 3] = alpha[y0 - self.yoff:y0 - self.yoff + (H - y0)]
        edge = canvas[H - 4:H - 3]                      # letzte Zeile nach unten fortsetzen
        canvas[H:] = np.repeat(edge, EXT, axis=0)
        self.base = canvas
        self.pts = {side: {k: self._p(v) for k, v in RIG[side].items() if k in ("elbow", "wrist")}
                    for side in RIG}
        H2 = H + EXT
        yy, xx = np.mgrid[0:H2, 0:W]
        n, lab = cv2.connectedComponents((canvas[..., 3] > 0.5).astype(np.uint8))
        # Komponenten den Armen zuordnen (größte links/rechts)
        side_of = {}
        for c in range(1, n):
            m = lab == c
            if m.sum() < 500:
                continue
            side_of[c] = "right" if xx[m].mean() > W / 2 else "left"
        self.parts = {}
        for side in ("left", "right"):
            m_arm = np.zeros((H2, W), bool)
            for c, s in side_of.items():
                if s == side:
                    m_arm |= lab == c
            m_arm = cv2.dilate(m_arm.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
            (x1, y1), (x2, y2) = (self._p(p) for p in RIG[side]["cuff"])
            line_y = y1 + (y2 - y1) * (xx - x1) / max(1e-6, (x2 - x1))
            above = yy < line_y
            hand = self.base.copy()
            hand[..., 3] *= (m_arm & above)
            fore = self.base.copy()
            fore[..., 3] *= (m_arm & ~above)
            self.parts[side] = {"hand": hand, "fore": fore}
        sq = RIG["right"]["screen"]
        self.screen_quad = np.float32([self._p(p) for p in sq])
        self._screen_cache = {}

    def _p(self, p):
        return (p[0] * self.k, p[1] * self.k + self.yoff)

    # ---- Bildschirm in die Hand-Ebene einsetzen
    def hand_with_screen(self, content: Image.Image | None, brightness: float) -> np.ndarray:
        hand = self.parts["right"]["hand"]
        if content is None or brightness <= 0.01:
            return hand
        key = (id(content), round(brightness, 2))
        if key in self._screen_cache:
            return self._screen_cache[key]
        sw, sh = content.size
        src = np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]])
        M = cv2.getPerspectiveTransform(src, self.screen_quad)
        scr = np.asarray(content, np.float32)
        size = (self.W, self.H + self.EXT)
        warped = cv2.warpPerspective(scr, M, size, flags=cv2.INTER_LINEAR)
        mask = cv2.warpPerspective(_screen_mask(sw, sh, int(sw * 0.1)), M, size)
        mask = (mask * brightness)[..., None]
        out = hand.copy()
        out[..., :3] = out[..., :3] * (1 - mask) + warped * mask
        # leichte Glasspiegelung bleibt sichtbar
        out[..., :3] = np.minimum(out[..., :3] + mask * 10, 255)
        self._screen_cache = {key: out}   # nur letzten behalten (Speicher)
        return out

    # ---- Transformation
    @staticmethod
    def _affine(rot, s, pivot, dx, dy):
        M = cv2.getRotationMatrix2D(pivot, -rot, s)
        M[0, 2] += dx
        M[1, 2] += dy
        return np.vstack([M, [0, 0, 1]])

    def _warp(self, layer, M):
        return cv2.warpAffine(layer, M[:2], (self.W, self.H), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

    def render(self, poses: dict[str, dict], hand_right: np.ndarray | None = None) -> np.ndarray:
        """poses: {'left': {...}, 'right': {...}} -> RGBA float32 (H, W, 4)"""
        out = np.zeros((self.H, self.W, 4), np.float32)
        for side in ("left", "right"):
            p = poses.get(side)
            if p is None:
                continue
            E, Wp = self.pts[side]["elbow"], self.pts[side]["wrist"]
            M1 = self._affine(p["rot"], p["s"], E, p["dx"], p["dy"])
            wx, wy, _ = M1 @ np.array([Wp[0], Wp[1], 1.0])
            M2 = self._affine(p["wrist"], 1.0, (wx, wy), 0, 0) @ M1
            hand = hand_right if (side == "right" and hand_right is not None) else self.parts[side]["hand"]
            for layer, M in ((hand, M2), (self.parts[side]["fore"], M1)):   # Ärmel liegt über dem Handgelenk
                w = self._warp(layer, M)
                a = w[..., 3:4]
                out[..., :3] = out[..., :3] * (1 - a) + w[..., :3] * a
                out[..., 3:4] = out[..., 3:4] + a * (1 - out[..., 3:4])
        out[..., :3] = out[..., :3].clip(0, 255)
        return out


# ------------------------------------------------------------------ Posen-Zeitleiste
def pose_at(track: list, side: str, t: float, breathe: float = 1.0) -> dict | None:
    """track: [[t, pose_name, dauer_übergang], …] in globaler Zeit."""
    if not track:
        return None
    lib = POSES[side]
    cur = dict(lib[track[0][1]])
    for i, k in enumerate(track):
        t0, name = k[0], k[1]
        dur = k[2] if len(k) > 2 else 0.45
        if t < t0:
            break
        prev = cur
        u = _ease((t - t0) / dur)
        tgt = lib[name]
        cur = {key: prev[key] + (tgt[key] - prev[key]) * u for key in tgt}
        # Hand folgt verzögert (Nachschwingen) -> wirkt wie ein echtes Handgelenk
        lag = _ease((t - t0 - 0.08) / dur)
        cur["wrist"] = prev["wrist"] + (tgt["wrist"] - prev["wrist"]) * lag + \
            (3.5 * math.sin(min(1, max(0, (t - t0) / dur)) * math.pi) * (1 if tgt["rot"] < prev["rot"] else -1))
        if u >= 1:
            cur = dict(tgt)
    ph = 0.0 if side == "right" else 1.7
    cur = dict(cur)
    cur["dy"] += breathe * 5 * math.sin(t * 1.25 + ph)
    cur["rot"] += breathe * 0.6 * math.sin(t * 0.9 + ph)
    cur["wrist"] += breathe * 0.8 * math.sin(t * 1.7 + ph)
    return cur
