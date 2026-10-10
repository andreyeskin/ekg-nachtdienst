# Blender-Pipeline für die Szenen

Stil: **ligne claire** — flache Lokalfarben, eine gleichmäßige Tuschelinie, keine Schraffur,
Licht nur als harte Formen (Sonnenfleck durchs Fenster). Palette: docs/ART_BIBLE.md.

Ablauf je Raum (CPU, kein GPU nötig; `pip install bpy Pillow numpy`), aus der Wurzel des Repositorys:

```bash
python3 gen/blender/ebenen.py monitor alle         # alle Durchgänge nach bau/blender/monitor/, Klickzonen
python3 gen/blender/komposit.py monitor --layers   # art/szenen/monitor/{hintergrund,mittelgrund,vorschau}.png
python3 gen/kunst.py && python3 tools/baue.py      # PNG-Ebenen ins Spiel
```

Einzelne Durchgänge: `python3 gen/blender/ebenen.py aufnahme lines` usw. (Liste: `ebenen.py` ohne Argumente).

* `szene_<raum>.py` — Geometrie, Kamera, Licht und die Einstellungen des Raums: `PALETTE`, `HIMMEL`,
  `OHNE_LINIE`, `OHNE_SCHATTIERUNG`, `SONNE_AUS`, `sonne_stellen()` (Schnittstelle in `werkzeug.py`).
  Jedes Objekt trägt eine Ebene (hinten/mitte) und optional eine Klickzone.
* `werkzeug.py` — Materialien, Grundkörper, `raum_huelle()` (Raum als ein Netz: saubere Linien an allen
  Raumfugen), `loch()`, `platzhalter()` (unsichtbare Fläche nur für eine Klickzone, z. B. Platz einer Figur).
* `ebenen.py` — Render-Durchgänge für jeden Raum:
  `flat` (Lokalfarbe, Stufen nach Flächenrichtung), `lines` (Freestyle, doppelt aufgelöst), `linesmid`
  (nur Mittelgrund), `mask`, `sun` (nur Sonne), `ao` (Umgebungsverdeckung), `kontakt` (Schatten von oben
  unter Möbeln), jeweils `*bg` ohne Mittelgrund. Schreibt `art/szenen/<raum>/hitboxes.json`.
* `komposit.py` — Farbe × Kontaktschatten × Sonne × Linie; Ebenen mit Alpha für die Parallaxe.
  Je Raum einstellbar (`EINSTELLUNG`): Lichtfarbe, Weichheit, AO-Schwelle, Kontaktschatten an/aus.
* `malen.py` — optionaler Feinschliff über fal.ai (Flux Kontext), Schlüssel aus `FAL_KEY`.

Regeln, die aus Fehlern stammen:
* Raum nicht aus sich durchdringenden Kisten bauen — die Fugen bekommen sonst keine oder flackernde Linien.
* Keine Geometrie hinter der Kamera (`raum_huelle(..., tiefe)` endet davor) — Freestyle zeichnet sonst lose Striche.
* Kein Dithering im Render: das Komposit verstärkt die Tusche, aus ±1 Rauschen würde Korn.
* Der Mittelgrund nimmt nur seine eigenen Linien mit (`linesmid`), sonst wandern Striche des Hintergrunds
  in der Parallaxe mit.

Zwischenergebnisse liegen in `bau/blender/<raum>/` (nicht im Repository), Ergebnisse in `art/szenen/<raum>/`.
