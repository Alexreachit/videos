# Lehren aus Video 1-3 + Genre-Daten (13.10.2026)

## Fehler, die nicht mehr passieren duerfen (Checkliste vor jedem Render)
1. Phase-Titel-Szenen NIE mit "Schild/Namensschild/Tuerschild" prompten - Gemini schreibt dann Text ins Bild.
2. Figur-Groesse konsistent: nie "small in the background"; immer "knees up, large in the foreground" (Ausnahme: bewusst gesetzte Weitwinkel max. 2x pro Video).
3. Kopf-Orientierung: nie Rueckenansicht + Gesicht; immer "facing the viewer" oder echte Profilansicht.
4. Keine Symbole/Icons/"Leiter aus Icons" prompten (werden zu Kauderwelsch).
5. Nach der Bildgenerierung IMMER Kontaktbogen aller Szenen pruefen (Kopf, Groesse, Text, Haende) BEVOR gerendert wird. Render dauert ~45 Min.
6. Gemini-Skript: __run3(from,to) arbeitet mit Q3-INDEX (0-basiert) [from,to); done-Keys = Index. Nicht mit Szenennummer verwechseln.
7. Nie zwei Treiber-Schleifen parallel auf demselben Tab.
8. Hängt der Tab (Screenshot-Timeout): Seite neu laden, v3code evaluieren, __show neu definieren.
9. edge-tts: neuer Endpunkt-Patch in build_video.py (Andrew). Andrew pruefen (F0 ~110 Hz, Hüllkurven-Korrelation mit Test-Render).

## Genre-Daten (YouTube-Suche 13.10.2026, Aufrufe/Alter)
- POVrank (etablierter Kanal): 25-Min-Videos, 85k-660k Aufrufe in 1-2 Monaten (Nordkorea-Armee 659k, Mafia 320k, KP China 317k, KGB 277k, Aegypten 281k, Gefaengnis 213k, Yakuza 299k, Azteken 185k in 2 Wochen).
- Kuerzere Hits (9-16 Min): Hypothetically Mafia 2,9M, Life Outline Kartell 7M, Drewno Illuminati 1,9M, POV Tales CIA Black Ops 1,7M, Unknown Frequencies WW2 1,1M, Strangely Ironic FBI Most Wanted 1M, POVBiz Goldman Sachs 380k.
- Nachahmer (gleiche Themen: Navy SEAL, Roman Legion, Mongolen, Vatican, Pilot, F1, Hospital, Wall Street): fast alle unter 5.000 Aufrufe, viele unter 100. Thema allein reicht NICHT; Hook, Thumbnail, Qualitaet und Kanal-Reputation entscheiden.
- Wenig/nichts gefunden (Luecken): Kreuzfahrtschiff, Fussballclub, Titanic (nur Mini-Kanaele).

## Entscheidung Laenge
- Video 3 ca. 8 Min (Alex). Ab Video 4 mindestens 12 Min (Alex).
- Pacing: Video 3 = 1208 Woerter -> 7:35 (ca. 160 W/Min). 12 Min = ca. 1950 Woerter. Bei ~65 Bildern -> ca. 30 Woerter pro Bild (2 Saetze pro Szene), Kamerafahrten halten es lebendig.
