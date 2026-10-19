# Stand und Übergabe — 18.10.2026

Diese Datei ist der Einstieg für die nächste Sitzung. Der Stand liegt auf dem Branch
`claude/stil-ligne-claire` (gepusht). Prüfung: `python3 gen/kunst.py && python3 tools/baue.py &&
node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"` → „Alle Prüfungen bestanden."

## Fertig (18.10.2026): Redesign-Entwurf Fall 1, Bewegungs-Prototyp, Skill `handlung`

- **`docs/REDESIGN_FALL1.md`** (Entwurf zur Freigabe, Spiel unverändert): Diagnose des Ist-Zustands; Lernziel =
  dramatische Frage „Darf Herr Baum heim?" (keine Vorwarnung + EKG nicht normal → nicht niedrig → Monitor,
  ESC-Synkope-2018 Tab. 6/7 am Postprint geprüft); Bogen in sieben Takten (Szene/Sequel) mit Frist 07:15, Wendung
  (verschwiegene Ohnmacht am Sonntag), Tochter Sabine am Telefon (Fremdanamnese), Verdachtsliste als roter Faden,
  ISBAR-Übergabe und Falks Gegenrede, Behandlungsentscheidung (Bisoprolol pausieren), Schlussgespräch, Epilog;
  alle Dialoge neu; Realismus-Prüfung (Koje statt Bank, Schichtwechsel, KPJ); Ersatz für „Drei Monitore"
  („Monitor gegen Papier", Namen an der Zentrale); Bewegungskonzept; Umbauliste; Belege; offene Entscheidungen
  (§13). Geprüft mit Skill `handlung` (§14) und durch ein Gutachten Medizin/Realismus/Dialoge (§15), beides
  eingearbeitet.
- **`prototyp/bewegung/`** (`leben.js`, `aufnahme.html`, `baue.py`, `schuss.mjs`): Leben in der Aufnahme über den
  vorhandenen Ebenen (Uhr mit Sekundenzeiger, Lidschlag, Blicke, Lichtkeil mit Staub, Fenster, Flur, Vordergrund,
  Handy, EKG-Wagen mit echter Kurve erst beim Schreiben). Bau: `python3 prototyp/bewegung/baue.py` →
  `bau/prototyp_bewegung_{de,ru}.html`; Prüfung: `node prototyp/bewegung/schuss.mjs bau/prototyp_bewegung_de.html`.
- **`prototyp/fall1/`** (spielbarer Prototyp der neuen Geschichte, nur Deutsch, alte Raumgrafik): `motor.js` (Dialoge,
  Uhr, Verdachtsliste, Mappe, Stand, Telefon, ISBAR, Gegenrede), `daten.js` (Drehbuch §3–§7 wörtlich), Zirkel und
  Streifen aus `web/`. Bau: `python3 prototyp/fall1/baue.py` → `bau/prototyp_fall1.html`; Prüfung:
  `node prototyp/fall1/pruefe.mjs` (guter Weg, Irrwege, iPad mit reduced-motion, Zufallsläufe) → „Alle Prüfungen bestanden."
- **Skill `.claude/skills/handlung/`**: Fehlbilder H1–H8, Szene/Sequel in 5–7 Takten, Entscheidungstest,
  Branch-and-Bottleneck, Enden und Epilog (nach jwynia/agent-skills, MIT).

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

Vorrang seit 18.10.2026 (Entscheidung des Nutzers, abends): **zuerst das Krankenhaus** (`docs/KRANKENHAUS.md`:
Gebäude, Abteilung, Grundriss, 3D-Modell, Einführung mit Flug). Danach die Design-Prüfung, dann nach Freigabe der
Umbau von Fall 1 nach `docs/REDESIGN_FALL1.md` §11 (seine Räume kommen dann aus dem Hausmodell); Kapitel 2 folgt
mit dem Ersatz für „Drei Monitore" (dort §9).

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
- QUELLEN §5: Tabelle 6 der ESC-Synkope-Leitlinie und das Stehversuch-Kriterium sind am 18.10.2026 am Postprint
  geprüft (Fundstellen in REDESIGN_FALL1 §12); QUELLEN §5 beim Umbau schließen.
- LUDB-Alter/Geschlecht der Aufnahme 39 mit „68, männlich" abgleichen (UMBAU §5).
- Der Schirm des EKG-Wagens zeigt Herrn Baums Kurve schon, bevor Elektroden kleben (`web/spiel.js`
  `starteSchirme`, `wagen_schirm`); Abhilfe im Redesign §8.2, im Prototyp schon gelöst.
- Spielfigur heißt im Spieltext „Famulantin", in ART_BIBLE §5 „KPJ-Student"; Redesign empfiehlt KPJ (§13).

## Arbeitsweise (vom Nutzer festgelegt)

- Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
- Jeder Agent in eigenem git worktree, Commit nach jedem Teilschritt (Limits können abbrechen).
- Lehrbuch (Trappe, EKG-Kurs) nur aus dem Drive-Ordner „EKG-Kurs Texte (privat, nur für Claude-Sitzungen)",
  Inhaltsverzeichnis `00_INHALT.txt`; nie ins Repository, nur eigene Worte mit Lektionsnummer.
- Bildgenerator fal.ai und GPT Image sind über den Proxy der Cloud-Umgebung angebunden
  (`gen/blender/malen.py`; Szenenbilder siehe `gen/blender/README.md`).
- Tokensparen und wann ein neuer Chat beginnt: siehe `CLAUDE.md` (ein Chat = ein Arbeitsblock; vor dem
  Wechsel committen, pushen, diese Datei nachziehen; alter Chat danach schließen oder archivieren).

### Lokal auf dem Mac arbeiten (Überlegung des Nutzers, 18.10.2026; beim ersten lokalen Start prüfen)

Für das 3D-Haus und die Renders lokal (Apple M4, 24 GB): Blender rechnet dort mit der GPU (Metal), die Cloud hat
nur 4 CPU-Kerne ohne GPU und installiert `bpy` in jeder neuen Sitzung neu; außerdem kann der Nutzer das Modell
selbst in Blender ansehen. Tokenpreis ist gleich, nur das Budget ist ein anderes (Cloud-Guthaben gegen Plan).
Einrichtung: Repository klonen und `claude/stil-ligne-claire` auschecken; Python in der Version, die `bpy` auf PyPI
verlangt, dann `pip install bpy Pillow numpy`; Node 22, `npm install`, `npx playwright install chromium`; die Schlüssel
für den Bildgenerator selbst setzen (`FAL_KEY`, `OPENAI_API_KEY`, in der Cloud kamen sie über den Proxy); in Cycles
das Gerät auf Metal stellen (in `gen/blender/` bisher fest CPU, beim ersten Lauf anpassen). Dann `claude` im Ordner
starten (oder `claude remote-control`, um vom Handy aus weiterzuarbeiten) und die Startnachricht unten senden.

**Eingerichtet am 19.10.2026** (Mac des Nutzers, Apple M4 Pro, GPU 20 Kerne): Python 3.13 über Homebrew,
`.venv/` im Repository mit `bpy` 5.2.2, Pillow, numpy (für Blender-Skripte `source .venv/bin/activate` oder
`.venv/bin/python gen/blender/…`); `npm install` (playwright-core 1.64) und dessen Chromium; Blender 5.2.2 als App
zum Ansehen. Cycles wählt über `werkzeug.cycles_geraet()` die GPU (Metal), `BLENDER_GERAET=CPU` erzwingt die CPU;
der erste Metal-Render kompiliert die Kernel einmalig (≈ 2 min). Build und Durchlauf: „Alle Prüfungen bestanden."

### Startnachricht für den ersten lokalen Chat (Mac, Claude Desktop → Code, Ordner `~/ekg-nachtdienst`)

```
Du arbeitest lokal auf meinem Mac (Apple M4, 24 GB) im Repository andreyeskin/ekg-nachtdienst,
Branch claude/stil-ligne-claire. Lies zuerst docs/STAND.md (auch „Lokal auf dem Mac arbeiten"),
dann docs/KRANKENHAUS.md, docs/KONZEPT.md §1–§3, docs/ART_BIBLE.md, gen/blender/README.md und die Skills
unter .claude/skills/.
Schritt 1, Einrichtung: prüfe, was fehlt (Python-Version für bpy, bpy, Pillow, numpy, Node, npm install,
Playwright-Chromium), erkläre mir jeden Installationsschritt kurz auf Russisch und frag vor jeder Installation.
Stelle Cycles in gen/blender/ auf die GPU (Metal) um, wo es fest auf CPU steht. Dann prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
Schritt 2, Auftrag: docs/KRANKENHAUS.md (Haus und Neuausrichtung) ausarbeiten, offene Fragen zuerst mit mir
klären, Vorbild-Recherche mit Fotos (Gebäude 31, LKH-Univ. Klinikum Graz), dann Blender-Blockout des Gebäudes
und zwei Probe-Renders in niedriger Qualität (Außenansicht im Morgenlicht, ein Flur).
3D und Raumprogramm als Subagent auf Fable, Code auf Opus. Antworte mir auf Russisch.
```

## Startnachricht für eine neue Sitzung

```
Arbeite im Repository andreyeskin/ekg-nachtdienst auf dem Branch claude/stil-ligne-claire.
Lies zuerst docs/STAND.md, dann docs/KONZEPT.md, docs/UMBAU.md, docs/ART_BIBLE.md, docs/FACHREGELN.md
und die Skills unter .claude/skills/. Der Referenzfall ist web/faelle/aufnahme_baum.js. Prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
Auftrag für diesen Chat: <ein Arbeitsblock, z. B. „Nächster Auftrag" unten>
```

## Nächster Auftrag: Krankenhaus zuerst (Idee des Nutzers, 18.10.2026)

Nach dem spielbaren Prototyp von Fall 1 sagt der Nutzer: „schön, aber trotzdem unverständlich". Er will zuerst das
ganze Krankenhaus bauen (ein eigenes Gebäude, eine Abteilung, Zimmer, Flure, Lehrsaal), am Anfang erklären, was
man lernt und wie es abläuft, mit einem Flug durch die Abteilung, und ein 3D-Modell, dessen Räume das Spiel nutzt.
Festgehalten mit Bausteinen, Folgen und offenen Fragen in **`docs/KRANKENHAUS.md`**. Am Abend kamen weitere Wünsche dazu
(viel Grün, Psychiatrie-Gebäude am LKH Graz als Vorbild, Leben im Hintergrund, Format, freundlicher Ton, weniger Text
und mehr Interaktion, Mentor je Dienst, Themenliste, Unterstützung durch Kollegen); ebenfalls dort, mit Empfehlung
zum Format. Die Farbpalette (Merkzettel
unten) wird am Haus mit ausprobiert.

### Startnachricht für den Krankenhaus-Chat

```
Arbeite im Repository andreyeskin/ekg-nachtdienst auf dem Branch claude/stil-ligne-claire.
Lies zuerst docs/STAND.md, dann docs/KRANKENHAUS.md, docs/KONZEPT.md §1–§3, docs/ART_BIBLE.md, gen/blender/README.md
und die Skills unter .claude/skills/. Prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
3D und Raumprogramm als Subagent auf Fable, Code auf Opus.
Auftrag für diesen Chat: docs/KRANKENHAUS.md (Haus und Neuausrichtung) ausarbeiten, offene Fragen zuerst mit mir klären,
Vorbild-Recherche mit Fotos, dann Blender-Blockout
des Gebäudes und zwei Probe-Renders in niedriger Qualität (Außenansicht im Morgenlicht, ein Flur).
```

## Danach: Design-Prüfung und Farbpalette (neuer Chat mit den Plugins „Design" und „audit-suite")

Die Plugins waren am 18.10.2026 in der laufenden Sitzung nicht verfügbar (nach dem Start installiert). Der neue
Chat prüft **zuerst**, ob die Skills `design:*` und `audit-suite:*` in seiner Skill-Liste stehen; fehlen sie, sagt
er es dem Nutzer sofort, statt ohne sie weiterzuarbeiten. Auftrag des Nutzers (18.10.2026), wörtlich in der Sache:

1. **Plan prüfen:** `docs/REDESIGN_FALL1.md` mit `audit-suite:audit-as-ux-eng` lesen (Ablauf, Rückmeldungen, wo die
   Spielerin hängen bleibt).
2. **Bildschirme:** Titelbildschirm, Dialogfenster, Szenenbild, Kopfleiste und Mappe mit `design:design-critique` und
   `design:accessibility-review` prüfen; Grundlage Screenshots aus dem Durchlauf bei 1024×768 und 1366×1024,
   verkleinert. Wichtig: Kontrast der Palette, Schriftgröße, Tippflächen ≥ 44 px auf dem iPad, prefers-reduced-motion.
3. **Bewegung:** Leerlauf-Animationen, Übergänge und Licht (`prototyp/bewegung/`) nach `audit-suite:web-animation-design`
   und `audit-suite:make-interfaces-feel-better` (Easing, Dauer, nur transform/opacity, ruhig, nichts lenkt vom EKG
   ab); Touch und iOS Safari zusätzlich nach `audit-suite:emil-design-engineering`.
4. **Knopf- und Hinweistexte** mit `design:ux-copy`. Figurendialoge bleiben beim Skill `dialoge` mit Humanizer,
   Medizin bei `fallakte`, Bogen und Entscheidungen bei `handlung`.
5. **Farbpalette (Merkzettel des Nutzers):** mit der Palette experimentieren, sie etwas interessanter und lebendiger
   machen. Zwei bis drei Varianten am selben Bild (Aufnahme 06:40, Szenenbild, Dialogfenster, Kopfleiste)
   nebeneinander zeigen, Kontrast der UI-Texte mitprüfen. ART_BIBLE §2 bleibt verbindlich, bis der Nutzer eine
   Variante freigibt (Rost „genau ein Objekt", Phosphor nur auf Schirmen, Magenta nur im UI, Rot-Rosa und Schwarz
   nur für Papier und Kurve).

Regeln des Nutzers dazu: audit-suite ist für React/Tauri geschrieben, nur Prinzipien übernehmen, die zum
Vanilla-JS-Einzeldatei-Bau passen (React, Tailwind, Next ignorieren). Widerspricht ein Befund der ART_BIBLE oder
KONZEPT, nichts ändern, sondern dem Nutzer die Frage vorlegen. Kein `audit-suite:full-audit` (zu teuer). Befunde als
kurze Liste in `docs/REDESIGN_FALL1.md`, Abschnitt „Design-Prüfung", nicht als langer Bericht im Chat. Danach
committen und pushen.

**Danach (nach Freigabe des Entwurfs durch den Nutzer):** Umbau nach `docs/REDESIGN_FALL1.md` §11 in eigenen
Sitzungen: (a) Akte + Texte, (b) Motor (Verdachtsliste, ISBAR, Argument, `leben.js`), (c) Falldaten + Prüfungen,
(d) Kunst + Leben (Bildaufträge B1–B7), (e) Kapitel 2 ohne „Drei Monitore". Vorher die offenen Entscheidungen in
§13 beim Nutzer abholen.

### Startnachricht für den Design-Chat

```
Arbeite im Repository andreyeskin/ekg-nachtdienst auf dem Branch claude/stil-ligne-claire.
Lies zuerst docs/STAND.md (Abschnitt „Nächster Auftrag"), dann docs/REDESIGN_FALL1.md, docs/ART_BIBLE.md, docs/KONZEPT.md §1
und die Skills unter .claude/skills/. Prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
Prüfe als Erstes, ob die Skills design:* und audit-suite:* verfügbar sind; wenn nicht, sag es mir sofort.
Auftrag für diesen Chat: Design-Prüfung (Punkte 1–4) und Farbpaletten-Varianten (Punkt 5) aus „Nächster Auftrag".
```
