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
* `figuren.py` — Marlene, Herr K., Dr. Falk, Dr. Wieser und Jonas als Grundkörper (Art Bible §5), mit Haltungen und
  Kopf-Leerobjekt. `PLATZ` ist die EINE Stelle je Figur für Ort (Meter, Weltkoordinaten der Szene), Drehung und Haltung;
  Falk mit `ort=None` steht am Platzhalter `platz_falk` der Szene.
* `ebenen_figuren.py` — Blockout-Figuren durch dieselben Durchgänge (Fläche, Linie, Sonne), Raumobjekte als
  Holdout. `aufbau(raum)` baut Raum + Figuren (gemeinsam mit `figuren_zeichnen.py`); die Sonne kommt aus
  `szene.sonne_stellen()`, `SONNE_AUS` wirft keinen Schatten. `raum`/`monitor` schreiben nur noch eine Vorschau
  nach `bau/blender/figuren/blockout/<raum>/` (Haltung und Platz prüfen), `portraits` die Brustbild-Blockouts nach
  `bau/blender/figuren/portrait_<wer>_blockout.png`, `probe` alle drei auf eine neutrale Bühne (Silhouettentest).
* `figuren_zeichnen.py` — die Figuren im Spiel: Blockout → Flux Kontext → einsetzen (unten).

## Figuren im Raum: zwei Schritte

Die Figuren in `art/szenen/<raum>/figuren/` sind ligne-claire-Zeichnungen, die Flux Kontext aus dem Blockout
ausmalt. Der teure Schritt läuft einmal, sein geprüftes Ergebnis liegt im Repository (`art/figuren_quelle/`:
PNG in voller Auflösung mit Alpha + JSON mit Ausschnitt, Seed, Endpunkt, Prompt). Der billige Schritt setzt die
Figur in den Raum und läuft nach jeder Raumänderung erneut — ohne fal, nur Masken aus Blender (Sekunden).

**(a) Zeichnen** — nur, wenn eine Figur neu entstehen soll (Kosten ≈ 0,04–0,08 $ je Aufruf):

```bash
python3 gen/blender/figuren_zeichnen.py vorlage aufnahme          # Blockout-Ausschnitte (4× Bühnenmaßstab, grüner Grund)
python3 gen/blender/figuren_zeichnen.py malen marlene --seed 7 --portrait   # Kontext (max/multi, Porträt = dieselbe Person)
python3 gen/blender/figuren_zeichnen.py malen herrk --seed 23               # Kontext (pro), Stilphrase stil/figur_herr_k.txt
python3 gen/blender/figuren_zeichnen.py malen falk --seed 8 --bearbeiten --quelle bau/blender/figuren/ki_falk_s7p.png \
        --stil gen/blender/stil/figur_falk_zirkel.txt                       # ein Requisit nachbessern (Zirkel)
python3 gen/blender/figuren_zeichnen.py malen herrk --seed 23 --aus bau/blender/figuren/ki_herrk_s23.png --uebernehmen
```

`malen` legt `bau/blender/figuren/ki_<name>_s<seed>[p|e].png` ab, dazu `_frei.png` (Farbschlüssel auf dem grünen
Grund) und `_pruef.png` (Vorlage | Kontext | freigestellt). Erst prüfen (Art Bible §5/§6: Requisiten, Finger,
keine Schrift, ein Schlauch), dann mit `--aus … --uebernehmen` nach `art/figuren_quelle/<name>.png` übernehmen.
Stilphrasen: `stil/figur_rahmen.txt` (Rahmen: Stil, Pose halten, grüner Grund, nichts dazuerfinden) +
`stil/figur_<name>.txt` (die Person). Das Quellbild ist im eigenen, neutralen Licht — Raumlicht kommt in (b).

**(b) Einsetzen** — nach jedem Raum-Render, immer NACH `ebenen.py <raum> flat` (das schreibt `hitboxes.json` neu):

```bash
BLENDER_THREADS=2 python3 gen/blender/figuren_zeichnen.py einsetzen aufnahme
BLENDER_THREADS=2 python3 gen/blender/figuren_zeichnen.py einsetzen monitor
python3 gen/kunst.py && python3 tools/baue.py
```

Je Figur rendert das drei billige Durchgänge im Ausschnitt (Tiefe des Raums, Tiefe des Blockouts, Sonne) und
rechnet daraus: Verdeckung (Raum vor der Figur: Tresen, PC, Becher vor Marlene; für Herrn K keine, er sitzt IN
der Bank — `verdecker` in `aufbau()`), Ausrichtung am Blockout (Kopfoberkante, Fußlinie), Umgriff (nichts, was
Kontext um die Figur herum dazuerfand), Sonnenfleck und Lichtfarbe aus `komposit.EINSTELLUNG` des Raums, dann
Bühnengröße (`--skala 2` für doppelte Auflösung), 160 Farben mit eigenem Alpha, `figuren.json` (Position, Atem-
Klasse) und die Klickzone der Figur in `hitboxes.json` (vereinigt mit der bestehenden Zone, mindestens 44 CSS-px).
Vorschau: `bau/blender/figuren/<raum>_vorschau.png`; `FIGUREN_DEBUG=1` schreibt die Masken daneben.

Bewegt sich eine Figur (neuer Stuhl, anderer Platz): `figuren.PLATZ` ändern, (b) erneut ausführen. Ändert sich
die Pose, braucht es (a) neu. Der Ausschnitt in `art/figuren_quelle/<name>.json` stammt aus `vorlage` und bleibt
gültig, solange die Figur am Platz bleibt; `vorlage` überspringt Figuren mit übernommener Quelle (`--neu` erzwingt,
`--nur NAME` beschränkt).

Auch Gegenstände einer Figur gehen diesen Weg: Herrn K.s **Tüte** sind die Raumobjekte der Zone `tuete` in
`szene_aufnahme.py` (dort `PLATZHALTER`: im Raumrender unsichtbar, Klickzone bleibt). `aufbau()` führt sie als
`Raumfigur` „tuete“ (Stilphrase `stil/figur_tuete.txt`, Rahmen `figur_rahmen_ding.txt`), (b) schreibt
`figuren/tuete.png` ohne Atem-Klasse, nach Herrn K gezeichnet, Klickzone `tuete` getrennt von `herrk`
(`getrennt` in `aufbau()`). Nach einer Änderung an der Tüte: `ebenen.py aufnahme flat` (Klickzone), dann (b).
Kontext hält sich eng an die Vorlage — ein weicher Blockout (Ellipsoide, flache Schlaufen) gibt eine Tüte,
ein Kasten mit Ringen einen Kanister. Gesichter: `malen --portrait` (Vorlage + Porträt) trifft die Person;
eine nachträgliche Gesichts-Bearbeitung mit Porträt (`--bearbeiten --portrait`) komponiert das Bild neu — nicht nutzen.

Die Uhrzeiger setzt `gen/kunst.py` aus der Klickzone `uhr` als SVG über das Hintergrundbild (gleiche Ebene
wie das Zifferblatt, sonst wandern sie in der Parallaxe); das Spiel dreht sie nach der Spielzeit.
`kunst.py` bettet `hitboxes.json` (→ `kunst.szenen.<raum>.zonen`, daraus baut `spiel.js` die Klickfelder) und
`schirme.json` (→ `.schirme`, Leinwände mit laufenden Kurven in der Ebene des Schirms) mit ein — Zahlen werden
nirgends abgeschrieben.

## Lehrsaal (Einschulungstag, 08:10)

`szene_lehrsaal.py` nach `docs/raeume/lehrsaal.md`; Rückwand y = 0, Raum nach −y (die Beschreibung misst y von der
Rückwand in den Raum, die Szene negiert). Kamera 28 mm bei (0,9 / −9,0 / 2,0) statt der vorgeschlagenen −7,6 m: Tür ganz
links und Whiteboard an der rechten Seitenwand brauchen 63° Sichtwinkel. Schirmflächen `projektion` (Leinwand, exaktes
Rechteck), `whiteboard` (Seitenwand: `ebenen.py` nimmt die große Seite der dünnen Kiste, die der Kamera näher liegt —
vier Ecken, kein Rechteck) und `wagen_schirm`. Zonen `jonas` (Kopfende) und `liege` (Fußende, Elektroden-Aufgabe)
sind Platzhalter, `figuren_zeichnen.py einsetzen lehrsaal` hält sie getrennt. Die vier Extremitätenleitungen sind
Raumobjekte (Mittelgrund) und enden unter Jonas' Armen und Beinen; die Klemmen selbst gehören zur Figur (rote Klemme =
das Rost-Objekt). Der Tisch steht näher an der Rückwand als beschrieben ((−2,1 / −2,0) statt (−2,6 / −3,2)), sonst
schnitte der 28-mm-Ausschnitt die Stühle an.

```bash
BLENDER_THREADS=2 python3 gen/blender/ebenen.py lehrsaal alle && python3 gen/blender/komposit.py lehrsaal --layers
BLENDER_THREADS=2 python3 gen/blender/ebenen_figuren.py lehrsaal            # Blockout-Vorschau (Haltung, Platz)
BLENDER_THREADS=2 python3 gen/blender/ebenen_figuren.py portraits wieser jonas
python3 gen/blender/figuren_zeichnen.py portrait wieser --seed 3 --uebernehmen
python3 gen/blender/figuren_zeichnen.py vorlage lehrsaal
python3 gen/blender/figuren_zeichnen.py malen wieser --seed 7 --portrait    # Stilphrase stil/figur_wieser.txt
python3 gen/blender/figuren_zeichnen.py malen jonas --seed 7 --portrait     # liegend: Liege nicht in der Vorlage (wie Herrn K.s Stuhl)
BLENDER_THREADS=2 python3 gen/blender/figuren_zeichnen.py einsetzen lehrsaal
```

Regeln, die aus Fehlern stammen:
* Raum nicht aus sich durchdringenden Kisten bauen — die Fugen bekommen sonst keine oder flackernde Linien.
* Keine Geometrie hinter der Kamera (`raum_huelle(..., tiefe)` endet davor) — Freestyle zeichnet sonst lose Striche.
* Kein Dithering im Render: das Komposit verstärkt die Tusche, aus ±1 Rauschen würde Korn.
* Der Mittelgrund nimmt nur seine eigenen Linien mit (`linesmid`), sonst wandern Striche des Hintergrunds
  in der Parallaxe mit.

Zwischenergebnisse liegen in `bau/blender/<raum>/` (nicht im Repository), Ergebnisse in `art/szenen/<raum>/`.

## Porträts: Feinschliff über fal.ai (Flux Kontext)

Die Brustbilder in `art/portraits/` entstehen aus dem 3D-Blockout (`ebenen_figuren.py portraits` →
`bau/blender/figuren/portrait_<wer>_blockout.png`) und einem Kontext-Durchlauf mit der Stilphrase
`stil/portrait_<wer>.txt`, danach 400×440 und 160 Farben. Ein fertiges Porträt lässt sich auch gezielt umzeichnen
(`--bearbeiten`, Gesicht bleibt) — so bekam Marlene den Dutt (`stil/portrait_marlene_dutt.txt`) und den Kuli
hinterm Ohr (`stil/portrait_marlene_kuli.txt`). Schlüssel aus `FAL_KEY` oder dem Proxy der Cloud-Umgebung:

```bash
python3 gen/blender/figuren_zeichnen.py portrait marlene --seed 3                       # aus dem Blockout
python3 gen/blender/figuren_zeichnen.py portrait marlene --seed 5 --bearbeiten --stil gen/blender/stil/portrait_marlene_kuli.txt
python3 gen/blender/figuren_zeichnen.py portrait marlene --seed 5 --bearbeiten --aus bau/blender/figuren/portrait_marlene_s5.png --uebernehmen
```

Vor dem Übernehmen gegen docs/ART_BIBLE.md §5 prüfen (Dutt mit Lesebrille, Kuli, Thermoskanne; Schiebermütze,
Hörgerät; Brille an der Kette, Zirkel, Stethoskop) — Kontext lässt gern ein Detail weg, dann neuer Seed oder
eine Bearbeitung mit einer einzigen Änderung (mehrere auf einmal gehen oft schief). Die Ganzkörperfigur danach
mit `malen --portrait` gegen das neue Porträt zeichnen, damit beide dieselbe Person zeigen.
`malen.py kontext` bleibt für Räume (nur als Vergleich; Räume bleiben reine Blender-Ausgabe).
