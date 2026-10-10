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
  Raumfugen), `loch()`, `platzhalter()` (unsichtbare Fläche nur für eine Klickzone, z. B. Platz einer Figur),
  `platte()` (eine Fläche ohne Dicke: eine Kontur statt zweier Striche), die gemeinsamen Bausteine
  `fenster()` (Blendrahmen in der Laibung, Pfosten/Kämpfer, Flügelrahmen, Griff, Fensterbank), `jalousie()`
  (Kasten, Lamellen einzeln mit Kontur, Leiterbänder, Unterschiene, Schnur) und `himmel_baender()` (flacher
  Himmel aus Farbbändern), sowie `schirmflaeche()` (Bildschirmfläche, die das Spiel mit einer Kurve belegt).
* `ebenen.py` — Render-Durchgänge für jeden Raum:
  `flat` (Lokalfarbe, Stufen nach Flächenrichtung), `lines` (Freestyle, doppelt aufgelöst), `linesmid`
  (nur Mittelgrund), `mask`, `sun` (nur Sonne), `ao` (Umgebungsverdeckung), `kontakt` (Schatten von oben
  unter Möbeln), jeweils `*bg` ohne Mittelgrund. Schreibt `art/szenen/<raum>/hitboxes.json` und
  `schirme.json` (vier Bildecken je Schirmfläche, Ebene). `BLENDER_THREADS=2` begrenzt die Kerne, wenn
  nebenher anderes rendert.
* `komposit.py` — Farbe × Kontaktschatten × Sonne × Linie; Ebenen mit Alpha für die Parallaxe.
  Je Raum einstellbar (`EINSTELLUNG`): Lichtfarbe, Weichheit, AO-Schwelle, Kontaktschatten an/aus.
* `malen.py` — optionaler Feinschliff über fal.ai (Flux Kontext), Schlüssel aus `FAL_KEY`.
* `figuren.py` — Marlene, Herr K. und Dr. Falk als Grundkörper (Art Bible §5), mit Haltungen und Kopf-Leerobjekt.
* `ebenen_figuren.py` — Figuren durch dieselben Durchgänge (Fläche, Linie, Sonne), Raumobjekte als Holdout:
  `raum` schreibt `art/szenen/aufnahme/figuren/{marlene,herrk}.png`, `monitor` schreibt
  `art/szenen/monitor/figuren/falk.png`, jeweils mit `figuren.json` (Bühnenposition, Atem-Klasse), und
  vereinigt die Klickzone der Figur in `hitboxes.json`; `portraits` schreibt `art/portraits/*.png` (400×440);
  `probe` stellt alle drei auf eine neutrale Bühne (`bau/blender/figuren/probe.png`, Silhouettentest).
  Licht und Sonnenschwelle kommen aus `komposit.EINSTELLUNG` des Raums.

Figuren immer NACH den Raum-Durchgängen rendern (`ebenen.py <raum> flat` schreibt `hitboxes.json` neu):

```bash
python3 gen/blender/ebenen_figuren.py raum && python3 gen/blender/ebenen_figuren.py monitor
python3 gen/blender/ebenen_figuren.py portraits
```

Die Uhrzeiger setzt `gen/kunst.py` aus der Klickzone `uhr` als SVG über das Hintergrundbild (gleiche Ebene
wie das Zifferblatt, sonst wandern sie in der Parallaxe); das Spiel dreht sie nach der Spielzeit.
`kunst.py` bettet `hitboxes.json` (→ `kunst.szenen.<raum>.zonen`, daraus baut `spiel.js` die Klickfelder) und
`schirme.json` (→ `.schirme`, Leinwände mit laufenden Kurven in der Ebene des Schirms) mit ein — Zahlen werden
nirgends abgeschrieben.

Draußen vor den Fenstern (Himmel, Nachbarflügel, Bäume) liegt niedrig genug, dass es nie im Weg der Sonne steht:
`ebenen_figuren.py raum` lässt alle Raumobjekte die Sonne der Figuren abschatten, unabhängig von `SONNE_AUS`.

Regeln, die aus Fehlern stammen:
* Raum nicht aus sich durchdringenden Kisten bauen — die Fugen bekommen sonst keine oder flackernde Linien.
* Keine Geometrie hinter der Kamera (`raum_huelle(..., tiefe)` endet davor) — Freestyle zeichnet sonst lose Striche.
* Kein Dithering im Render: das Komposit verstärkt die Tusche, aus ±1 Rauschen würde Korn.
* Der Mittelgrund nimmt nur seine eigenen Linien mit (`linesmid`), sonst wandern Striche des Hintergrunds
  in der Parallaxe mit.

Zwischenergebnisse liegen in `bau/blender/<raum>/` (nicht im Repository), Ergebnisse in `art/szenen/<raum>/`.

## Porträts: Feinschliff über fal.ai (Flux Kontext)

Die Brustbilder in `art/portraits/` entstehen aus dem 3D-Blockout (`ebenen_figuren.py portraits`) und einem
Kontext-Durchlauf mit den Stilphrasen in `stil/` (weiche Variante, Seed 11), danach auf 400×440 gebracht und
auf 160 Farben quantisiert (RGB, Alpha getrennt). Schlüssel kommt aus `FAL_KEY` oder dem Proxy der Cloud-Umgebung:

```bash
python3 gen/blender/malen.py kontext --image art/portraits/marlene.png --style gen/blender/stil/portrait_marlene.txt \
        --seed 11 --size portrait_4_3 --out bau/blender/figuren/marlene_weich.png
```

Vor dem Übernehmen gegen docs/ART_BIBLE.md §5 prüfen (Dutt mit Lesebrille, Kuli, Thermoskanne; Schiebermütze,
Hörgerät; Brille an der Kette, Zirkel, Stethoskop) — Kontext lässt gern ein Detail weg, dann neuer Seed.
`stil/szene_ligne_claire.txt` ist die Phrase für ganze Räume (nur als Vergleich; Räume bleiben reine Blender-Ausgabe).
