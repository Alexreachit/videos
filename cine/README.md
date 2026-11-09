# Kino-Pipeline (cine) – POV-Zombie-Videos

Aus einer Episode-Datei (`episodes/*.yaml`) entsteht automatisch ein fertiges Video:
Szenenplan → Prompts → Referenzbilder → Clips (verkettet) → Prüfung → gezielte Neugenerierung
→ Sounddesign → Schnitt, Farbe, Ton → Endkontrolle → Video + Bericht + Dashboard.

**Kostenpflichtiges startet nie ohne deine Freigabe.** Details zur Technik-Wahl: [TECHNOLOGIE.md](TECHNOLOGIE.md).

## Drei Wege

| Weg | Kosten | Was du tust |
|---|---|---|
| **Testlauf** (`mock`) | 0 € | nichts – prüft Ton, Schnitt, Timing, Prüfungen mit Platzhalter-Bildern |
| **Gratis** (`manual`) | 0 € | Clips nach fertigen Prompt-Karten selbst erzeugen (z. B. Google Vids) und ablegen |
| **Vollautomatisch** (`replicate`) | ca. 4–7 $ pro 60 s | Kosten freigeben, warten |

## Auf GitHub (empfohlen)

1. Einmalig: *Settings → Secrets and variables → Actions* → `REPLICATE_API_TOKEN` anlegen
   (nur für den bezahlten Weg; optional `ELEVENLABS_API_KEY`, `GEMINI_API_KEY`).
2. *Actions → Kino-Pipeline – Produktion → Run workflow*:
   - `kosten_schaetzen` → in der Zusammenfassung stehen Anbieter, Clips, Auflösung, Dauer,
     Kosten, Kosten pro Neugenerierung und der **Freigabe-Code**.
   - `produktion` mit `freigabe_code` und `max_usd` → läuft. Ohne gültigen Code stoppt der Lauf vor
     dem ersten bezahlten Aufruf.
   - `testlauf_kostenlos` → komplettes Platzhalter-Video in wenigen Minuten.
   - `szene_neu` + `szene: s04` → nur diese Szene neu (braucht Freigabe-Code, falls kostenpflichtig).
3. Fertiges Video: im Lauf unten unter **Artifacts** (enthält Video, Thumbnail, Bericht, Dashboard,
   Kontaktblätter jeder Szene).

Zwischenstände werden im GitHub-Cache gesichert: Bricht ein Lauf ab, macht der nächste dort weiter –
fertige Clips werden nicht erneut bezahlt.

## Lokal

```bash
pip install -r cine/requirements.txt     # plus ffmpeg
cp .env.example .env                       # nur für bezahlte Anbieter ausfüllen

python -m cine plan     episodes/zombie_ep01.yaml                  # Szenenplan + Prompts
python -m cine run      episodes/zombie_ep01.yaml --video mock     # kostenloser Testlauf
python -m cine run      episodes/zombie_ep01.yaml --video manual   # Gratis-Weg (s. u.)
python -m cine estimate episodes/zombie_ep01.yaml --video replicate
python -m cine approve  episodes/zombie_ep01.yaml --video replicate --code ABC123 --max-usd 7
python -m cine run      episodes/zombie_ep01.yaml --video replicate
python -m cine redo     episodes/zombie_ep01.yaml --video replicate --scene s04
python -m cine serve                                               # Dashboard: http://localhost:8765
```

Alles einer Produktion liegt in `productions/<episode>_<anbieter>/`:

| Ordner/Datei | Inhalt |
|---|---|
| `plan.md`, `prompts/` | Szenenplan mit Zeiten, Prompt je Szene, Prompt-Historie |
| `estimate.md`, `approval.json` | Kostenschätzung, Freigabe |
| `attempts/`, `clips/` | alle Versuche, übernommene Clips |
| `qc/` | Kontaktblatt je Versuch (9 Einzelbilder) |
| `audio/` | Effekte, Atmosphäre, Zeitleiste aller Sound-Cues |
| `output/` | **fertiges Video**, Thumbnail, `bericht.md` |
| `handoff/`, `inbox/` | Gratis-Weg: Prompt-Karten raus, deine Clips rein |
| `dashboard.html`, `log.txt` | Statusseite, Protokoll |

## Gratis-Weg im Detail

1. `python -m cine run episodes/zombie_ep01.yaml --video manual`
2. In `handoff/s01.md` steht der komplette Prompt. Clip erzeugen, als `inbox/s01.mp4` speichern.
3. Erneut starten → s01 wird geprüft, das letzte Bild wird zum Startbild für s02
   (`handoff/s02_startbild.jpg` – beim Erzeugen als Startbild hochladen). Das hält Hände,
   Umgebung und Licht über die Szenen konsistent.
4. Nach der letzten Szene schneidet, vertont und rendert die Pipeline automatisch.

## Neue Episode

`episodes/zombie_ep01.yaml` kopieren und anpassen. Pro Szene Pflicht: `environment, time_of_day,
lighting, weather, camera, movement, objects, zombies, action, mood, sound, continuity` plus Dauer
(3–15 s). Sound-Cues (`cues`) legen Geräusche sekundengenau auf die Handlung. Fehlt etwas, bricht
`plan` mit einer klaren Meldung ab. Format/Auflösung je Episode unter `settings.render`.

## Qualitätskontrolle

Automatisch pro Clip: Dauer, Format, Auflösung, Schwarzbilder, eingefrorene Bilder, Unschärfe,
Flackern und **harte Schnitte im Clip** (= POV-Bruch). Unter 70 Punkten wird die Szene neu generiert
(max. 3 Versuche, nur im freigegebenen Budget); der beste Versuch wird übernommen. Endkontrolle:
Gesamtlänge, Format, Tonspur, Übersteuerung, Lautstärke.

Nicht zuverlässig automatisch messbar: echte First-Person-Wirkung, verformte Hände, Realismus.
Mit `--vision gemini` bewertet ein KI-Modell die Kontaktblätter (kostenpflichtig, ca. 0,01 $/Szene),
sonst stehen diese Punkte als Checkliste im Bericht.

## Anbieter wechseln

Alle Modelle stehen in `cine/config/default.yaml` (`models`, `prices`). Ein neues Modell = neuer
Provider unter `cine/providers/` (Unterklasse von `VideoProvider` mit `generate()`), Eintrag in
`cine/providers/__init__.py`, Preis in `default.yaml`. Der Rest bleibt unverändert.

## Fehlerbehebung

| Meldung | Lösung |
|---|---|
| `wartet auf Freigabe` | `estimate` ansehen, mit dem Code `approve` ausführen |
| `Plan hat sich seit der Freigabe geändert` | Episode/Einstellungen geändert → neu schätzen und freigeben |
| `Budget überschreiten` | höheres `--max-usd` freigeben oder Szenen einzeln neu machen |
| `REPLICATE_API_TOKEN fehlt` | Secret anlegen bzw. `.env` ausfüllen |
| `wartet auf Clips` | Gratis-Weg: Clip aus `handoff/` erzeugen und in `inbox/` ablegen |
| Szene sieht schlecht aus, Score aber ok | `redo --scene sXX`; ggf. Prompt in der Episode schärfen |

Tests (kostenlos, offline): `python -m pytest -q tests/`
