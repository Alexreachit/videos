"""Leichte Figurenanimation fuer flache Cartoon-Bilder (kein Download, nur OpenCV/numpy).
Erkennt die cremefarbenen Koepfe und Haende, bewegt sie sanft (Nicken, Neigen, Wippen)
und laesst die Augen blinzeln. Kamerafahrt (Zoom/Schwenk) wird im selben Schritt gerechnet."""
import math
import cv2
import numpy as np

W, H = 1920, 1080


def cream_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = ((h >= 12) & (h <= 34) & (s >= 20) & (s <= 110) & (v >= 190)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return m


class Part:
    pass


def find_parts(bgr):
    """Liefert Koepfe (gross) und Haende (klein) als Part-Objekte."""
    m = cream_mask(bgr)
    # Linien/Augen im Kopf schliessen, damit der Kopf eine Flaeche ist
    closed = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    n, lab, stats, cent = cv2.connectedComponentsWithStats(closed, 8)
    parts = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < 2500 or w > W * 0.6 or h > H * 0.9:
            continue
        p = Part()
        p.kind = "head" if area > 22000 else "hand"
        p.box = (x, y, w, h)
        p.area = area
        # gefuellte Maske (Loecher/Augen inklusive)
        comp = (lab == i).astype(np.uint8) * 255
        cnts, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filled = np.zeros_like(comp)
        cv2.drawContours(filled, cnts, -1, 255, -1)
        p.mask = filled
        p.r = math.sqrt(area / math.pi)
        if p.kind == "head":
            fill = cv2.countNonZero(filled) / float(w * h)
            if not (0.66 < fill < 0.9 and 0.72 < w / float(h) < 1.35):
                continue
            p.eyes = find_eyes(bgr, p)
            if not p.eyes:
                continue
            # Muetze/Kopfhoerer (dunkel) direkt am Kopf mitbewegen
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            reg = np.zeros_like(filled)
            ry0, ry1 = max(0, int(y - 0.9 * p.r)), int(y + 0.35 * h)
            rx0, rx1 = max(0, int(x - 0.15 * w)), min(W, int(x + 1.15 * w))
            reg[ry0:ry1, rx0:rx1] = 255
            cand = (((gray < 100).astype(np.uint8) * 255) & reg) | filled
            cand = cv2.morphologyEx(cand, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            n2, lab2, st2, _ = cv2.connectedComponentsWithStats(cand, 8)
            keep = np.zeros_like(filled)
            ids = set(np.unique(lab2[filled > 0])) - {0}
            for k in ids:
                keep[lab2 == k] = 255
            # nicht ueber das Kopf-Umfeld hinaus (Koerper nicht mitnehmen)
            keep[int(y + 0.55 * h):, :] = filled[int(y + 0.55 * h):, :]
            p.mask = keep
            ys, xs = np.nonzero(keep)
            p.box = (xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
        parts.append(p)
    return parts


def find_eyes(bgr, head):
    x, y, w, h = head.box
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    dark = ((gray < 90) & (head.mask > 0)).astype(np.uint8) * 255
    dark = cv2.erode(head.mask, np.ones((9, 9), np.uint8)) & dark  # Rand/Kontur ausschliessen
    n, lab, stats, cent = cv2.connectedComponentsWithStats(dark, 8)
    eyes = []
    for i in range(1, n):
        bx, by, bw, bh, a = stats[i]
        if not (0.002 * head.area < a < 0.03 * head.area):
            continue
        if not (0.65 < bw / max(bh, 1) < 1.5):
            continue
        if a / float(bw * bh) < 0.6:   # rund
            continue
        if cent[i][1] > y + 0.62 * h:  # Augen liegen in der oberen Haelfte
            continue
        eyes.append((int(cent[i][0]), int(cent[i][1]), bw, bh, (lab == i)))
    return eyes if len(eyes) in (1, 2) else []


class Rig:
    def __init__(self, path, seed=0):
        src = cv2.imread(str(path))
        self.src = cv2.resize(src, (W, H), interpolation=cv2.INTER_CUBIC)
        self.parts = find_parts(self.src)
        self.rnd = np.random.RandomState(seed)
        self.cream = None
        self.blink_img = self.src.copy()
        self.blinking_parts = 0
        for p in self.parts:
            p.ph = self.rnd.uniform(0, 6.28)
            p.f = self.rnd.uniform(0.28, 0.42)
            if p.kind == "head":
                med = np.median(self.src[(p.mask > 0) & (cream_mask(self.src) > 0)], axis=0)
                for (cx, cy, bw, bh, comp) in p.eyes:
                    dil = cv2.dilate(comp.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
                    self.blink_img[dil] = med
                    t = max(2, int(bh * 0.18))
                    cv2.line(self.blink_img, (cx - bw // 2, cy), (cx + bw // 2, cy), (30, 30, 30), t, cv2.LINE_AA)
                self.blinking_parts += 1 if p.eyes else 0
            # Region (ROI) und Gewichtsmaske
            x, y, w, h = p.box
            pad = int(p.r * 0.9)
            x0, y0 = max(0, x - pad), max(0, y - pad)
            x1, y1 = min(W, x + w + pad), min(H, y + h + pad)
            p.roi = (x0, y0, x1, y1)
            mm = p.mask[y0:y1, x0:x1]
            wgt = cv2.dilate(mm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(p.r * 0.25) * 2 + 1,) * 2))
            wgt = cv2.GaussianBlur(wgt, (0, 0), max(2, p.r * 0.22)).astype(np.float32) / 255.0
            p.w = wgt
            gx, gy = np.meshgrid(np.arange(x0, x1, dtype=np.float32), np.arange(y0, y1, dtype=np.float32))
            p.gx, p.gy = gx, gy
            p.pivot = (x + w / 2.0, y + h * 0.95)   # Hals-/Handgelenkspunkt

    def blink_state(self, t):
        # alle ~3.5 s ein Blinzeln von 0.14 s, pro Rig leicht versetzt
        per = 3.6
        k = (t + self.rnd_off) % per if hasattr(self, "rnd_off") else t % per
        return k < 0.14

    def frame(self, t, cam):
        """cam = (zoom, cx, cy) in Ausgabekoordinaten (Bildmitte des Ausschnitts)."""
        if not hasattr(self, "rnd_off"):
            self.rnd_off = 0.0
        base = self.blink_img if self.blink_state(t) and self.blinking_parts else self.src
        img = self.src.copy() if base is self.src else self.blink_img.copy()
        for p in self.parts:
            amp = 1.0 if p.kind == "head" else 0.6
            ty = amp * 0.05 * p.r * math.sin(2 * math.pi * p.f * t + p.ph)
            tx = amp * 0.02 * p.r * math.sin(2 * math.pi * p.f * 0.7 * t + p.ph + 1)
            th = amp * math.radians(3.0) * math.sin(2 * math.pi * p.f * 0.8 * t + p.ph + 2)
            x0, y0, x1, y1 = p.roi
            px, py = p.pivot
            c, s = math.cos(-th), math.sin(-th)
            rx, ry = p.gx - px - tx, p.gy - py - ty
            sx = px + c * rx - s * ry
            sy = py + s * rx + c * ry
            mx = (p.gx + p.w * (sx - p.gx)).astype(np.float32)
            my = (p.gy + p.w * (sy - p.gy)).astype(np.float32)
            roi = cv2.remap(base, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            img[y0:y1, x0:x1] = roi
        z, cx, cy = cam
        M = np.float32([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]])
        return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
