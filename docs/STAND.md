# Stand und Übergabe — 13.10.2026

Diese Datei ist der Einstieg für die nächste Sitzung. Der Stand liegt auf dem Branch `arbeit/episode`
(Worktree, nicht gepusht). Prüfung: `python3 gen/kunst.py && python3 tools/baue.py &&
node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"` → „Alle Prüfungen bestanden."

## Fertig (13.10.2026): Referenzfall Herr Baum im neuen Fallschema

- **Fallschema und Motor** (KONZEPT §6): `web/motor/fall.js` spielt Fälle aus reinen Datenobjekten;
  `web/motor/fenster.js` (Frage, Auswahl, Befundzeilen), `web/motor/szenenbild.js` (bildschirmfüllende
  Nahaufnahme mit ruhiger Einblendung). `web/spiel.js` enthält nur noch Start, Kopfleiste, Kapitel 2.
- **Fall `aufnahme_baum`** (`web/faelle/aufnahme_baum.js`, Akte `docs/faelle/aufnahme_baum.md` §8a): Szenenbild am
  Tresen (Marlene reicht den Aufnahmebogen), Anamnese mit zehn Pflichtfragen und Vertiefung, Medikationsplan
  im Gespräch, Kurzuntersuchung als Befundzeilen, Expertenfragen bei Marlene und Dr. Falk (TIA, Krampf,
  Unterzucker, Orthostase), EKG mit Zirkel (RR, PQ, optional QRS), Übergabe an Dr. Falk am Tresen
  (Porträt-Dialog, nur mit beiden Zahlen; Rückwege zum Wagen und zum Patienten), Entscheidung Monitor,
  Erzähler-Ende, Epilog als Erzählung (Dienst 3). Tüten-Station und Reizleitung bei Marlene sind raus.
- **Texte über IDs**: `text/de/aufnahme_baum.json` ist die Quelle, `text/en/…` und `text/ru/…` tragen dieselben
  Schlüssel (240 IDs, vollständig). `T(id, vars)` in `web/sprache.js` nimmt IDs und, übergangsweise, die alten
  deutschen Sätze. Karten der Mappe speichern ID + Platzhalterwerte und übersetzen sich beim Sprachwechsel.
- **Prüfungen** (`tools/durchlauf.mjs`): alle Wege des Falls (Pflichtfragen → Mahnung, TIA, Medikationsplan,
  Übergabe nur mit beiden Zahlen, drei Rückwege, Ende und Epilog, Szenenbild, keine Tüte), Textüberlauf
  de/en/ru bei 1024×768 und 1366×1024, Zirkel maßstabstreu bei 1024×768/1366×1024/1920×1080 (±2 ms),
  ID-Vollständigkeit, Gedankenstrich-Verbot und Bildschirmmaß der Repliken; Kapitel 2 (vier Wege), Sprachen,
  Hülle, Reizleitungs-Modul wie bisher. `tools/woerter.py` prüft zusätzlich die IDs (fehlend, verwaist,
  Platzhalter) und räumt mit `--aufraeumen` verwaiste alte Sätze weg.
- Leinwände (Zirkel, Frage, Karten) haben jetzt feste CSS-Höhen; vorher skalierte der Browser sie mit der
  Breite hoch, und der Zirkel passte auf kein iPad ohne Scrollen.

## So legt man den nächsten Fall an (Muster: Herr Baum)

1. **Akte** `docs/faelle/<id>.md` nach dem Skill `fallakte` (DD-Tabelle mit Expertenfragen, Belege in
   FACHREGELN/QUELLEN), erst dann Dialoge nach dem Skill `dialoge` (inkl. Humanizer-Durchgang).
2. **Datendatei** `web/faelle/<id>.js`: `window.FAELLE.<id> = { id, kuerzel, aufnahme: { haupt }, werte,
   pflicht, kern, regeln, dialoge, karten, aufgaben, raum, stand, epilog }`. Bedingungen und Wirkungen sind
   Strings (Liste im Kopf von `web/motor/fall.js`); Texte sind IDs `<kuerzel>.<baum>.<knoten>`; Zahlen nur als
   Platzhalter aus `werte` (feste Fallwerte) oder aus den Messungen (`hf`, `rr`, `pq`, `qrs`).
   Dialogknoten: `{ text | [{wenn, text}], tu, nach, antworten: [{text, zu, wenn, tu, baum}], weiter, ende }`.
   Aufgaben: `frage` (Streifen + Antworten), `wahl`, `zirkel` (rr/pq/qrs/qt mit Deutungsregeln),
   `befundzeilen`. Räume: Felder mit `bei: [{wenn, tu}]`, Ausgänge mit `wenn` und `gesperrt`.
3. **Texte** `text/de/<id>.json`, dann `text/en/<id>.json` und `text/ru/<id>.json` mit denselben Schlüsseln
   (`python3 tools/woerter.py` meldet Lücken; der Bau bricht bei fehlender Übersetzung ab).
4. **Einhängen**: Datei in `tools/baue.py` (SKRIPTE) und `web/index.html` eintragen; in `web/spiel.js`
   `Fall.lade(global.FAELLE.<id>)` und die Dialogbäume zusammenführen (für mehrere Fälle: Kapitelfolge dort).
   Ein Szenenbild kommt über `SZENENBILDER` in `gen/kunst.py` (PNG → JPEG ≤ 300 kB) und wird im Fall mit
   `szenenbild:<name>>baum.knoten` aufgerufen.
5. **Prüfungen** in `tools/durchlauf.mjs` für jeden Weg des Falls ergänzen; dann bauen und laufen lassen.

## Halb fertig: Lehrsaal

Raum fertig (`gen/blender/szene_lehrsaal.py`, `art/szenen/lehrsaal/`), Figuren Dr. Wieser und Jonas samt
Porträts als **ungeprüfter Zwischenstand** eingebettet; noch keine Spiellogik. Vor dem Weiterbauen prüfen:

- Jonas' Elektroden nach Ampel-Regel (FACHREGELN, Lektion 2): rechter Arm rot, linker Arm gelb,
  linkes Bein grün, rechtes Bein schwarz — Rot und Schwarz auf derselben Körperseite. Elektroden auf
  Haut (Hosenbeine hoch), nicht auf Kleidung; flach liegend, Beine gestreckt und nicht übereinander;
  T-Shirt hochgeschoben (Brustwand frei), jede Klemme mit Kabel zum Wagen. (`gen/blender/klemmen_setzen.py`
  war dafür in Arbeit.)
- Dr. Wieser: Akzent Kobaltblau `#2F5DA8` und blaues EKG-Lineal fehlen im Porträt; graue Haare mit 41 bewusst?
- Das Reizleitungs-Rätsel (`web/raetsel_reizleitung.js`) wartet hier auf seinen Einstieg (Dr. Wieser,
  Whiteboard); der Durchlauf startet es bis dahin direkt.

## Entscheidungen des Nutzers (13.10.2026, umgesetzt)

Rotation über mehrere Dienste · Epilog für Herrn Baum als Erzählung · Reizleitung in den Lehrsaal · Dr. Falk
in der Aufnahme als Porträt-Dialog · Lagetyp erst nach dem 12-Kanal-Export · erst ein Fall komplett, dann
die übrigen nach diesem Muster.

## Nächste Schritte (Reihenfolge aus `docs/UMBAU.md` §1)

1. Kapitel 2 als Fall `monitor` nach dem Muster (Frau Lindner, `docs/faelle/monitor.md`): dann wandert der
   Epilog von Herrn Baum an den Anfang von Dienst 3, Herrn Baums Präsynkope und der „Speicher" entfallen,
   `web/spiel.js` schrumpft auf Start und Kapitelfolge.
2. Lehrsaal-Fall (`docs/faelle/lehrsaal.md`) mit Reizleitung, Zacken antippen, Elektroden kleben; parallel
   12-Kanal-Export (UMBAU §5).
3. Ersatzaufnahmen (Wiederspielwert): `aufnahme.ersatz` steht in den Falldaten, der Motor zieht noch immer
   `haupt`; Textvarianten je Ersatz fehlen.

## Bekannte offene Punkte

- Aufnahme um 09:20 zeigt noch das Sonnenaufgangslicht (zweite Lichtfassung fehlt).
- Thermoskanne: ART_BIBLE §5 sagt Magenta, §2 verbietet Magenta im Raum; gerendert ist Rost.
- Rund 150 ältere Sätze (Reizleitung, Kapitel 2, Hülle) ohne en/ru-Übersetzung; sie wandern mit der
  Migration der jeweiligen Kapitel auf IDs.
- Neulade-Prüfung im Durchlauf scheitert selten sporadisch (Chromium über `file://`); Abhilfe: Durchlauf über
  `http://127.0.0.1`.
- Falks Kaffeefleck und Zirkel in der Brusttasche fehlen.
- QUELLEN §5: Tabelle 6 der ESC-Synkope-Leitlinie und das Stehversuch-Kriterium am Original nachprüfen.
- LUDB-Alter/Geschlecht der Aufnahme 39 mit „68, männlich" abgleichen (UMBAU §5).

## Arbeitsweise (vom Nutzer festgelegt)

- Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
- Jeder Agent in eigenem git worktree, Commit nach jedem Teilschritt (Limits können abbrechen).
- Lehrbuch (Trappe, EKG-Kurs) nur aus dem Drive-Ordner „EKG-Kurs Texte (privat, nur für Claude-Sitzungen)",
  Inhaltsverzeichnis `00_INHALT.txt`; nie ins Repository, nur eigene Worte mit Lektionsnummer.
- Bildgenerator fal.ai und GPT Image sind über den Proxy der Cloud-Umgebung angebunden
  (`gen/blender/malen.py`; Szenenbilder siehe `gen/blender/README.md`).

## Startnachricht für eine neue Sitzung

```
Arbeite im Repository andreyeskin/ekg-nachtdienst auf dem Branch arbeit/episode.
Lies zuerst docs/STAND.md, dann docs/KONZEPT.md, docs/UMBAU.md, docs/ART_BIBLE.md, docs/FACHREGELN.md
und die Skills unter .claude/skills/. Der Referenzfall ist web/faelle/aufnahme_baum.js. Prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
```
