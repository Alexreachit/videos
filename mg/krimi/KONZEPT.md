# Kommentar-Krimi "Nebelstein" (neuer TikTok-Kanal, Alex 2026-11-07)

Komplett eigenes Format, NICHT vergleichbar mit Roundhead Stories / Roundhead Island. Alles selbst erfunden (Figuren, Orte, Musik) – kein Copyright-Risiko.

## Idee
- Kleinstadt Nebelstein, immer Nebel, leicht mystisch. Ein Mord passiert (nicht blutig: Kreide-Umriss, stehengebliebene Uhren …).
- Hauptfigur: Kommissar Theo (ockerfarbener Trenchcoat, dunkler Hut mit Petrol-Band, Petrol-Schal, braune Locken, große braune Augen)
  mit einer Laterne, deren blaues Licht flackert, wenn ein Hinweis in der Nähe ist (mystisches Element).
- Mitmachen: Folgen + Kommentar "Ich bin dabei" -> man wird Bewohner von Nebelstein (eigene 3D-Figur mit Namensschild) und kann Verdächtiger werden.
  Nur Namen von Leuten, die selbst darum bitten; keine Profilbilder.
- Jede Folge endet mit einer Abstimmung (wen befragen / wo suchen); der Top-Kommentar entscheidet. Am Ende eines Falls tippt die Community den Täter –
  liegt sie falsch, entkommt er und schlägt wieder zu.

## Technik
- Echte 3D-Figuren in Blender (Workflow .github/workflows/blender.yml, Blender 4.2, Cycles CPU). Start: mg/blender_queue.txt = "krimi/<skript>.py [preview]".
- Figur Theo: mg/krimi/char_theo.py (Metaball-Formen, weiche Studio-Beleuchtung, AgX Punchy). Ergebnis renders/krimi/ (Ansichten, theo.blend, theo.glb).
- Stimme: ElevenLabs Gratis-Plan (Alex legt Konto an und loggt sich im Browser der App ein; keine kommerzielle Nutzung, "elevenlabs.io" in Titel/Beschreibung).
  Kandidaten (Deutsch, Erzähler): Leon Stern (Fiction/Fantasy), Robert Ranger ("cool storyteller"), Alexander (tiefer TV-Erzähler).

## Folge 1 (2026-11-07)
- Fertig: renders/ep01/ep01_silent.mp4 (Blender, 20 Runner, ~4 h) + compose.py -> Nebelstein_Folge1.mp4 (52,9 s). Wartet auf Alex' OK.
