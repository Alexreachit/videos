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
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "bilder"
BASE_URL = "https://image.pollinations.ai/prompt/"
WIDTH, HEIGHT = 1280, 720
SEED = 42                # gleicher Startwert für alle Bilder hilft der Figurenkonsistenz
MODEL = "flux"
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


def fetch(prompt: str) -> bytes:
    query = urllib.parse.urlencode({
        "width": WIDTH, "height": HEIGHT, "seed": SEED,
        "model": MODEL, "nologo": "true", "safe": "true",
    })
    url = BASE_URL + urllib.parse.quote(prompt, safe="") + "?" + query
    req = urllib.request.Request(url, headers={"User-Agent": "video-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        ctype = resp.headers.get("Content-Type", "")
        data = resp.read()
    if not ctype.startswith("image/") or len(data) < 5000:
        raise RuntimeError(f"Keine gültige Bildantwort (Typ {ctype!r}, {len(data)} Bytes)")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=0, help="höchstens so viele neue Bilder (0 = alle)")
    ap.add_argument("--only", type=int, nargs="*", help="nur diese Szenennummern (überschreibt vorhandene)")
    args = ap.parse_args()

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
    for i in todo:
        prompt = f"{style} Scene: {prompts[i - 1]}".strip()
        ok = False
        for attempt in range(1, MAX_TRIES + 1):
            try:
                data = fetch(prompt)
                (IMAGES / f"{i:02d}.jpg").write_bytes(data)
                ok = True
                break
            except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
                wait = 10 * attempt
                print(f"  Szene {i}, Versuch {attempt}/{MAX_TRIES} fehlgeschlagen: {e}. Warte {wait}s.")
                time.sleep(wait)
        if ok:
            made += 1
            fails_in_row = 0
            print(f"Szene {i:02d} fertig ({made}/{len(todo)})")
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
