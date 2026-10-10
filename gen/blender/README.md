# Blender-Pipeline für die Szenen

Stil: **ligne claire** — flache Lokalfarben, eine gleichmäßige Tuschelinie, keine Schraffur,
Licht nur als harte Sonnenstreifen durch die Jalousie. Palette: Sand, Petrol, Rost, Mint.

Ablauf (CPU, kein GPU nötig; `pip install bpy Pillow numpy`):

```bash
cd gen/blender
for m in flat lines mask flatbg linesbg sun sunbg; do python3 ebenen_aufnahme.py $m; done
python3 komposit.py --layers      # schreibt art/szenen/aufnahme/{hintergrund,mittelgrund,vorschau}.png
python3 ../kunst.py               # bettet die PNG-Ebenen in bau/kunst.json ein
python3 ../../tools/baue.py
```

* `szene_aufnahme.py` — Geometrie, Kamera, Licht; markiert jedes Objekt mit Ebene (bg/mid) und Klickzone.
* `ebenen_aufnahme.py` — Render-Durchgänge: `flat` (Lokalfarbe), `lines` (Freestyle), `sun` (nur Sonne),
  `amb` (nur Streulicht, optional), `mask` (Maske Mittelgrund), jeweils auch `*bg` ohne Mittelgrund.
  Schreibt außerdem `art/szenen/aufnahme/hitboxes.json` — Klickzonen aus den 3D-Objekten.
* `komposit.py` — setzt Farbe × Licht × Linie zusammen; Ebenen mit Alpha für die Parallaxe.
* `malen.py` — optionaler Feinschliff über fal.ai (Flux Kontext), Schlüssel aus `FAL_KEY`.

Zwischenergebnisse liegen in `bau/blender/` (nicht im Repository), Ergebnisse in `art/szenen/`.
