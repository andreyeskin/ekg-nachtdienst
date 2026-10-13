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

## Szenenbilder: Nahaufnahmen für Gesprächsanfänge

Ein Szenenbild ist eine illustrierte Nahaufnahme ohne Klickzonen (Vorlage: `art/referenz/chatgpt_aufnahme_marlene.png` —
Marlene reicht der Spielerin die Mappe über den Tresen). Das Bild aus dem Generator war im Licht falsch: Sonne im Fenster
hinter Marlene, Jalousiestreifen aber von links auf Wand und Tresen, Gesicht frontal hell. Deshalb teilt die Pipeline die
Arbeit: **Blender rechnet das Licht, der Bildgenerator malt nur.**

1. `szenenbild.py` baut dieselbe Szene (Raum, `sonne_stellen()`, Figuren-Blockouts aus `figuren.py`) aus einer eigenen Kamera
   (`EINSTELLUNG[raum][einstellung]`: Ort in Augenhöhe, Gier, Neigung, Brennweite, Haltungen und Orte der Figuren) und rendert
   16:9 (1920×1080) die Durchgänge Fläche (mit Stufen nach Flächenrichtung wie `ebenen.py`), Linie (Freestyle, doppelt
   aufgelöst, Gesichtsteile ohne Kontur), Tiefe, Figurenmaske, Kontaktschatten, Sonne und Lampe (nur der Spot im Lampenkopf).
   Das Komposit ist das Ligne-claire-Komposit der Räume plus Lampeninsel: `art/szenenbilder/<raum>_<einstellung>/vorlage.png`,
   dazu die Lichtmasken aus Blender `sonne.png`, `lampe.png` sowie `tiefe.png`, `maske.png`.
2. `malen.py` schickt die Vorlage mit der Stilphrase `stil/szenenbild.txt` zum Generator — fal Kontext (`kontext`, mit
   `--referenz` als max/multi mit Stilreferenz) oder OpenAI GPT Image (`openai`: Vorlage + Porträts + Stilreferenz als
   Eingabebilder, `POST /v1/images/edits`, Standardmodell `gpt-image-2.5-sunburst`). Die Stilphrase beschreibt den Stil des
   Referenzbilds und das Licht ausdrücklich (Sonne tief hinter dem Fenster der Rückwand zur Kamera, Streifen auf dem Boden zum
   Betrachter, Gegenlicht, Lampe als warme Insel, „keep all light and shadow exactly as in the input") und verbietet Text,
   gemalte EKG-Kurven, Uhrzeiger.
3. `licht_pruefen.py` misst, ob das Licht im gemalten Bild dort liegt, wo Blender es hat (Korrelation der hellen Flächen mit der
   Sonnenmaske, Kontrast, Versatz, Streifenrichtung, Fremdlicht) und schreibt ein Vergleichsbild.

```bash
BLENDER_THREADS=2 python3 gen/blender/szenenbild.py aufnahme tresen            # ≈ 2,5 min -> art/szenenbilder/aufnahme_tresen/
python3 gen/blender/szenenbild.py aufnahme tresen --komposit                   # nur neu zusammensetzen
BLENDER_THREADS=2 python3 gen/blender/szenenbild.py aufnahme tresen --probe --kamera -2.5,-2.5,1.58 --gier 40 --brennweite 30
                                                                               # Kamera ausprobieren (klein, 10 s); --licht tönt dazu die Sonne gelb (+5 s)
python3 gen/blender/malen.py kontext --image art/szenenbilder/aufnahme_tresen/vorlage.png \
        --style gen/blender/stil/szenenbild.txt --aspect 16:9 --seed 7 --out bau/blender/szenenbilder/aufnahme_tresen/kontext_s7.png
python3 gen/blender/malen.py openai --image art/szenenbilder/aufnahme_tresen/vorlage.png \
        --portrait art/portraits/marlene.png --portrait art/portraits/herr_k.png \
        --referenz art/referenz/chatgpt_aufnahme_marlene.png [--dry-run]       # Schlüssel vom Proxy (Secret api.openai.com, /v1/images/) oder OPENAI_API_KEY; Ergebnis + JSON nach art/szenenbilder/aufnahme_tresen/
python3 gen/blender/licht_pruefen.py <ergebnis.png> art/szenenbilder/aufnahme_tresen/sonne.png --lampe art/szenenbilder/aufnahme_tresen/lampe.png
```

Einstellung `aufnahme/tresen` (zweite Fassung, nach dem Vorbild `art/referenz/chatgpt_aufnahme_marlene.png`): Ich-Perspektive über
den Tresen mit 30 mm, Marlene groß links, hinter ihr das Fenster mit der tiefen Sonne, rechts klein Herr K. auf der Bank, der
EKG-Wagen daneben. Die Raumgeometrie setzt Grenzen: der Tresen (x −4,1…−1,7) liegt ganz links vom Fenster (x −1,25…1,45), und die
Gelenklampe steht am rechten Tresenende. Von einer Kamera rechts der Lampe liegt das Fenster immer rechts neben Marlene; von einer
Kamera links der Lampe hängt der Lampenarm vor ihrem Gesicht — das Fenster lässt sich also nicht vollständig hinter sie bringen.
Kompromiss: die Spielerin steht links vor dem Tresen (−2,5/−2,5, Augenhöhe 1,58 m), schaut mit 40° Gier schräg nach rechts an der
Lampe vorbei (Lampenkopf am linken Bildrand); Marlene steht am äußersten rechten Tresenende (−1,66/−0,45, linke Schulter über der
Wange), so beginnt das Fenster an ihrer linken Schulter, die Sonnenscheibe (`sonne_im_fenster` −0,7/1,52) steht dicht neben ihr.
Herr K. sitzt für dieses Bild auf dem ersten Sitz (1,1/−0,75, dem Fenster nächstes Bankende), nur so passt er mit 30 mm ganz ins
Bild; Tüte und EKG-Wagen werden über `objekte` (Klickzonen-Gruppen aus `szene_aufnahme.HIT`, Versatz in Metern) mitverschoben —
der Wagen unter das rechte Fensterende, die Tüte neben seinen Sitz. Haltung `reicht_mappe`: der linke Arm gestreckt zur Kamera,
Hand 0,6 m vor dem Körper in Schulterhöhe, die Mappe an der hinteren Kante gehalten und um 40° zur Kamera geneigt, ihre Vorderkante
knapp über der Ablage; die Kanne steht (`kanne_welt`, Raumkoordinaten) auf der Ablage vor der Lampenklemme. Was Blender für diese
Kamera ergibt: die Sonne (`sonne_stellen`, nach links-vorn) erreicht hinter dem Tresen weder Marlenes Haar noch ihre Schultern (die
beleuchtete Zone beginnt bei x ≈ −1,45, ihre linke Schulter endet bei −1,42); Streifen liegen auf dem rechten Ende der Ablage, auf
Fensterbank, Wagen und auf Herrn K. (Mütze, Schulter); die Streifen auf dem Boden liegen 2,5–3,3 m vor der Rückwand, also hinter
der Kamera. Ein Gegenlicht-Saum an Marlene steht daher nicht in `sonne.png`; die Stilphrase verlangt Säume nur, wo die Vorlage sie
zeigt. Freestyle ließ aus dieser Nahkamera in einem schmalen Band Kanten hinter der Tresenplatte durch (Hinterkante der
Arbeitsfläche, Marlenes Beine — Striche auf der Ablage; in der ersten Fassung dasselbe mit der Kanne auf der Arbeitsfläche):
Fase, Dicke und Lage der Platte änderten daran nichts, erst die fein unterteilte Platte (Subdivision „simple", Stufe 4, in
`aufbau`) hält die Sichtbarkeitsprüfung dicht. Die Kanne steht trotzdem auf der Ablage der Sichtblende, wie im Vorbild.

Nicht im Bild: Klickzonen, Uhrzeiger (bleiben SVG), Kurven auf Schirmen, Text. Die Szenenbilder werden später eingebunden; die
Spiellogik kennt sie noch nicht.

### Probe mit fal.ai am 11.10.2026 (sechs Aufrufe, Vorlage `aufnahme_tresen`)

| Aufruf | Endpunkt, Eingaben | Licht (`licht_pruefen.py`, 4 Kriterien) | Figuren, Stil |
|---|---|---|---|
| Vorlage selbst | — | RICHTIG 4/4: Kontrast 0,57, Versatz 1 %, Richtung 7°, Fremdlicht 0 ‰ | Blockout |
| Referenz (ChatGPT) | — | FALSCH 1/4: Kontrast 0,06, Versatz 4 %, Fremdlicht 42 ‰ (Streifen auf Wand und Tresen, wo Blender keine hat) | der Anlass |
| 1 kontext, s7 | Vorlage + Stilphrase | TEILWEISE 3/4: Kontrast 0,51, Richtung 4°, Fremdlicht 6 ‰; Versatz 4,6 % (Glanz unter der Fensterbank) | hält Aufbau und Licht, malt aber plastisch wie ein 3D-Render; Mannequin-Gesicht, Dutt ohne Brille, Hand mit Fingern, Kanne rost, Mütze, Tüte als Blase, keine Schrift |
| 2 kontext/max/multi | Vorlage + Referenzbild | FALSCH 1/4 | malt das Referenzbild nach, verwirft die Vorlage (Herr K. fehlt, Licht wie im Original falsch) |
| 3 kontext, s11 | Vorlage + Stilphrase + „hand-drawn, not 3D" | FALSCH 2/4: Kontrast 0,27 | wie 1, dunkler |
| 4 kontext/max/multi | Vorlage + Porträts | kein Bild (fal: downstream_service_unavailable) | — |
| 5 kontext/max/multi, s7 | Vorlage + Porträts Marlene, Herr K. | FALSCH 1/4: Kontrast 0,05, Fremdlicht 32 ‰ | echte Ligne claire, Marlenes Gesicht/Dutt/Lesebrille/Kuli aus dem Porträt, Mütze; aber Mappe, Lampeninsel und Streifen weg, Hände ohne Finger, Kritzelschrift auf dem Namensschild |
| 6 kontext/max, s7 | Vorlage + Stilphrase | TEILWEISE 3/4: Kontrast 0,10, Versatz 1,9 %, Fremdlicht 8 ‰ | fast eine Kopie der Vorlage, Streifen auf dem Wagen verblasst |

Lehre: Flux Kontext kann Licht halten (einbildig) oder Personen treffen (multi mit Porträts), nicht beides in einem Bild. Für
den GPT-Lauf mit Schlüssel heißt das: Vorlage + Porträts + Stilreferenz in einem Aufruf und prüfen, ob `licht_pruefen.py`
den Kontrast der Vorlage (0,57) annähernd hält; wenn nicht, zweistufig — Szene einbildig fürs Licht, Figuren wie im Spiel
getrennt gezeichnet und über `maske.png` eingesetzt. Bilder und Prüfungen der Probe liegen nicht im Repository
(`bau/blender/szenenbilder/aufnahme_tresen/kontext_*.png` + `.json`).

### GPT Image zur zweiten Einstellung am 13.10.2026 (drei Aufrufe, Vorlage `aufnahme_tresen`, 30 mm)

Aufruf wie oben (`malen.py openai`, Vorlage + Porträts Marlene, Herr K. + Referenzbild), dazu `--prompt` mit einer kurzen
Szenenbeschreibung (Marlene am Tresenende reicht die Mappe, Kanne vor der Lampe, Fenster hinter ihrer linken Schulter, Herr K.
auf der Bank mit Tüte, Wagen unter dem Fenster; Schild leer; dünner warmer Saum an Haar und Schulter). Die Lichtprüfung ist für
diese Einstellung streng: die Sonnenmaske ist dünn (Fensterbank, Wagen, drei Streifen am rechten Ende der Ablage, Herrn K.s
Mütze und Schulter), und schon die Vorlage selbst kommt nur auf 1/4 (Kontrast 0,13, Versatz 7 %: die cremefarbene Ablage zeigt
die Tönung kaum). Figuren treffen in allen drei Läufen die Porträts (Dutt mit Lesebrille, Kanne rost, Mütze, Schnurrbart,
Strickjacke, Hausschuhe, Tüte mit Schachteln, Uhr ohne Zeiger, Schirme dunkel, Hände mit Fingern, keine Schrift außer wo
vermerkt); der Kuli steckt wie im Porträt in der Brusttasche, nicht hinterm Ohr.

| Aufruf | Prompt-Zusatz | Licht (`licht_pruefen.py`) | Befund |
|---|---|---|---|
| 1 (19:03) | Szenenbeschreibung | FALSCH 2/4: Kontrast −0,34, Versatz 5,9 %, Richtung 17°, Fremdlicht 5 ‰ | Komposition wie die Vorlage, Lampeninsel da, aber **keine** Sonnenstreifen (Ablage, Fensterbank, Wagen, Herr K. alle flach); Schild leer |
| 2 (19:05) | + Streifen einzeln benannt (Ablage, Fensterbank, Wagen, Mütze/Schulter), Gesicht im Halbschatten, Saum | TEILWEISE 3/4: Kontrast 0,60, Richtung 6°, Fremdlicht 3,9 ‰; Versatz 7,2 % | Streifen auf Ablage (aber unter der Mappe statt am rechten Ende) und Fensterbank, Wagen und Herr K. weiter flach, zarter Saum am Dutt; **Schild mit Schriftlinien** (§6) |
| 3 (19:06) | + Schild „absolut leer", Streifen rechts neben der Mappe | FALSCH 2/4: Kontrast 0,10, Richtung 10°, Fremdlicht 5,1 ‰; Versatz 7,6 % | Schild leer, Streifen am rechten Ablagenende und auf der Fensterbank, aber blass; Wagen und Herr K. flach; Saum zart — **bestes Ergebnis** (kein Ausschlusskriterium) |

Offen: GPT malt die Streifen blass und nie auf Wagen oder Herrn K.; der Versatz bleibt bei 7 %, weil die gemalten Streifen auf
der Ablage weiter links liegen als Blenders. Marlenes Gesicht bleibt frontal hell statt im Halbschatten, der Gegenlicht-Saum
ist nur angedeutet (Blenders Sonne erreicht sie nicht, siehe oben).
