#!/usr/bin/env python3
"""
Erzeugt die Bilder für alle Szenen automatisch über einen kostenlosen Bilddienst
(Pollinations, ohne Konto). Existierende Bilder werden übersprungen, so kann man
die Arbeit auf mehrere Tage verteilen.

  python generate_images.py              # alle fehlenden Bilder
  python generate_images.py --max 35     # höchstens 35 neue Bilder in diesem Lauf
  python generate_images.py --only 5 12  # nur diese Szenen (neu erzeugen)

Eingaben:  stil.txt (Stil-Block), prompts.txt (eine Zeile pro Szene)
Ausgabe:   bilder/01.jpg, bilder/02.jpg, ...
"""
import argparse
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "bilder"
BASE_URL = "https://gen.pollinations.ai/image/"
API_KEY = os.environ.get("POLLINATIONS_KEY", "").strip()
WIDTH, HEIGHT = 1280, 720
SEED = 42                # gleicher Startwert für alle Bilder hilft der Figurenkonsistenz
MODEL = os.environ.get("POLLINATIONS_MODEL", "").strip()  # leer = Standardmodell des Dienstes
PAUSE_SECONDS = 4        # Pause zwischen zwei Bildern, schont den Gratis-Dienst
MAX_TRIES = 4
MAX_FAILS_IN_A_ROW = 3   # danach Abbruch: Limit erreicht, morgen weitermachen


def read_lines(name: str):
    path = ROOT / name
    if not path.exists():
        sys.exit(f"{name} fehlt.")
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")]


def existing_image(i: int):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = IMAGES / f"{i:02d}.{ext}"
        if p.exists() and p.stat().st_size > 5000:
            return p
    return None


class OutOfBudget(Exception):
    """Konto/Key hat kein Guthaben mehr (HTTP 402) oder der Key ist ungültig."""


def fetch(prompt: str) -> bytes:
    params = {"width": WIDTH, "height": HEIGHT, "seed": SEED, "nologo": "true"}
    if MODEL:
        params["model"] = MODEL
    url = BASE_URL + urllib.parse.quote(prompt, safe="") + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "User-Agent": "video-pipeline/1.0",
        "Authorization": f"Bearer {API_KEY}",
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            ctype = resp.headers.get("Content-Type", "")
            data = resp.read()
    except urllib.error.HTTPError as e:
        if e.code in (401, 402, 403):
            raise OutOfBudget(f"HTTP {e.code}: Key ungültig oder Guthaben aufgebraucht") from e
        raise
    if not ctype.startswith("image/") or len(data) < 5000:
        raise RuntimeError(f"Keine gültige Bildantwort (Typ {ctype!r}, {len(data)} Bytes)")
    return data


def looks_like_same_fallback(sizes):
    """Drei Bilder in Folge mit fast gleicher Dateigröße sind sehr verdächtig:
    Der Dienst liefert dann meist ein Ersatzbild statt der Szene."""
    if len(sizes) < 3:
        return False
    a, b, c = sizes[-3:]
    return max(a, b, c) - min(a, b, c) < 0.005 * max(a, b, c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=0, help="höchstens so viele neue Bilder (0 = alle)")
    ap.add_argument("--only", type=int, nargs="*", help="nur diese Szenennummern (überschreibt vorhandene)")
    args = ap.parse_args()

    if not API_KEY:
        sys.exit("Der Key fehlt. Lege ihn bei GitHub unter Settings, Secrets and variables, "
                 "Actions als POLLINATIONS_KEY an.")

    style = " ".join(read_lines("stil.txt")) if (ROOT / "stil.txt").exists() else ""
    prompts = read_lines("prompts.txt")
    scenes = read_lines("script.txt")
    if len(prompts) != len(scenes):
        sys.exit(f"prompts.txt hat {len(prompts)} Zeilen, script.txt hat {len(scenes)}. Das muss gleich sein.")

    IMAGES.mkdir(exist_ok=True)
    wanted = args.only if args.only else range(1, len(prompts) + 1)
    todo = [i for i in wanted if args.only or existing_image(i) is None]
    print(f"{len(prompts) - len([i for i in range(1, len(prompts) + 1) if existing_image(i) is None])} "
          f"von {len(prompts)} Bildern sind schon da, {len(todo)} fehlen.")
    if args.max:
        todo = todo[:args.max]

    made = fails_in_row = 0
    sizes = []
    for i in todo:
        prompt = f"{style} Scene: {prompts[i - 1]}".strip()
        ok = False
        for attempt in range(1, MAX_TRIES + 1):
            try:
                data = fetch(prompt)
                (IMAGES / f"{i:02d}.jpg").write_bytes(data)
                ok = True
                break
            except OutOfBudget as e:
                print(f"Stopp: {e}. Bereits erzeugte Bilder bleiben erhalten, mache morgen weiter.")
                todo = []
                break
            except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
                wait = 10 * attempt
                print(f"  Szene {i}, Versuch {attempt}/{MAX_TRIES} fehlgeschlagen: {e}. Warte {wait}s.")
                time.sleep(wait)
        if not todo:
            break
        if ok:
            made += 1
            fails_in_row = 0
            sizes.append((IMAGES / f"{i:02d}.jpg").stat().st_size)
            print(f"Szene {i:02d} fertig ({made})")
            if looks_like_same_fallback(sizes):
                print("Achtung: Die letzten drei Bilder sind fast gleich groß. Vermutlich liefert der "
                      "Dienst ein Ersatzbild. Ich höre auf. Prüfe die Bilder, bevor du weitermachst.")
                break
        else:
            fails_in_row += 1
            print(f"Szene {i:02d} aufgegeben.")
            if fails_in_row >= MAX_FAILS_IN_A_ROW:
                print("Mehrere Fehler hintereinander, vermutlich Tageslimit oder Dienst down. "
                      "Ich höre auf. Starte den Workflow später noch einmal, er macht dort weiter.")
                break
        time.sleep(PAUSE_SECONDS)

    left = [i for i in range(1, len(prompts) + 1) if existing_image(i) is None]
    print(f"Neu erzeugt: {made}. Noch fehlend: {len(left)}" + (f" ({left})" if left else ""))


if __name__ == "__main__":
    main()
