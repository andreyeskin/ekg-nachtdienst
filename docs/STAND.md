# Stand und Übergabe — 26.10.2026

Diese Datei ist der Einstieg für die nächste Sitzung. Der Stand liegt auf dem Branch
`claude/stil-ligne-claire` (gepusht). Prüfung: `python3 gen/kunst.py && python3 tools/baue.py &&
node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"` → „Alle Prüfungen bestanden."

## Fertig (25./26.10.2026): Lehrsaal gestaltet — Saal im Haus, Farbdesign „Morgen", Spielkamera an der ersten Bank

Vom Nutzer angenommen (26.10.2026). Probe `docs/haus/probe_lehrsaal.jpg`, Aufruf:
`.venv/bin/python gen/blender/haus_blockout.py bauen && .venv/bin/python gen/blender/haus_blockout.py render lehrsaal` (≈ 25 s).

- **Saal im Haus:** Westende des EG, 14,4 × 7 m, `gen/blender/szene_lehrsaal.py` als Ausbau in Hauskoordinaten
  (`PALETTE`, `KAMERA`, `ausbau(h)`, eingebunden über `AUSBAUTEN` in `haus_blockout.py`). Nur Netze aus Punktlisten, keine
  `bpy.ops` (9:44 min statt 11 s). Kamera-Schlüssel `ausbau`, `ohne_scheiben`, `sonne_staerke`, neu `schattenfarbe`
  (Komposit) und `gier` (feste Blickrichtung, Ziel per Verschiebung in x und y).
- **Eigenes Farbdesign „Morgen"** (aus drei Proben gewählt; Vorlagen Lofi-Zimmer, Ligne claire, Foto): Sonne Pfirsich,
  alles ohne Sonne 24 % zum kühlen Blau `#6F7FB0`, Parkett, helle Lattendecke, Stühle Petrol, Akzente Pfirsich,
  Terrakotta, Tannengrün, Oliv, Koralle. **Jeder Raum bekommt sein eigenes Design**; ART_BIBLE §2 ist nur Ausgangspunkt.
  Werte in `docs/raeume/lehrsaal.md` §6.
- **Spielkamera: die Spielerin sitzt an der ersten Bank** (5,75 / 2,85 / 1,25, Blick frontal zur Stirnwand, 18 mm).
  Im Bild: Leinwand mit Uhr darüber in der Mitte; links Liege quer vor dem Giebelfenster (Kopfteil hoch, Kopf zur
  Fensterwand) und EKG-Wagen frei daneben, Schirm zur Bank gedreht; rechts kleiner Dozententisch (Linealschachtel,
  Laptop) und das Whiteboard an der Flurwand im Eck; unten die eigene Bank mit Block, EKG-Streifen und Zirkel
  (`werkzeug()`). Türen außerhalb: der Ausgang wird ein Pfeil am rechten Bildrand. Maße `lehrsaal.md` §7, §8.

## Fertig (25.10.2026): Figuren mit Haltung und lesbare Schrift in der Außenansicht (a) (Auftrag B, dritter Teil)

- `haus_blockout.py`: `HALTUNGEN` und `figur` (Röhrengerüst, Mantel, Gegenstand, Haar, Dutt, Mütze); sieben Figuren, davon
  zwei vorn auf dem Parkweg (älterer Herr mit Gehstock, Besucherin mit Tasche). `schrift` setzt Text aus Schriftdateien:
  „HAUS FÖHRENHANG" auf der Giebelwand, Wegweiser am Parkweg („↑ Haupteingang", „Notaufnahme →"), „H" an der Haltestelle.
- Entschieden: farbige Mäntel und Hautton draußen bleiben (ART_BIBLE §2, Entscheid 25.10.2026).

## Fertig (25.10.2026): Natur, Himmel und Ferne der Außenansicht (a) (Auftrag B, zweiter Teil)

Astwerk, Kronen, kahle Bäume, Stadt in Gassen, Himmel in fünf Stufen, Linien ab 90 m dünner. Einzelheiten KRANKENHAUS
„Natur, Himmel und Ferne"; Renders `docs/haus/stil_tag.jpg`, `stil_blau.jpg`, `probe_aussen.jpg`.

## Fertig (25.10.2026): Fassade und Hof der Außenansicht (a) ausdetailliert (Auftrag B, erster Teil)

Altbaufenster, Gesimse, Portal, Loggia, Hof mit Autos und Figuren, Spätherbst. Einzelheiten KRANKENHAUS „Fassade
ausdetailliert (25.10.2026)". Offene Fragen an den Nutzer: Gardinen lassen oder nur Rollläden? Kahlen Baum rechts
behalten? Fensterband hinter den Lamellen von Trakt N 1. OG bestätigen?

## Fertig (25.10.2026): Mechanik und Struktur, dritte Fassung (Entwurf, wartet auf Freigabe)

- Nutzer will Geschichte und Mechanik neu: zuerst die Mechanik; Belohnungen; drei Teile (Kurswoche im Lehrsaal mit
  Modellen, Noten und Prüfung · Ambulanz mit Patienten, Mentorbericht und Patientenreaktion · Station und Reanimation).
- **`docs/MECHANIK.md`** (nur Konzept, Spiel unverändert): dramatische Frage des ganzen Spiels „Wird man dir die Nacht
  anvertrauen?"; Kernschleife auf vier Ebenen; Befundsatz nach Lektion 34 als gemeinsame Mechanik; Belohnung =
  Logbuch mit Vertrauensstufen (EPA), Noten nur im Kurs, Mentorbericht (Mini-CEX), Patientenreaktion, Verlauf,
  Befundatlas, Werkzeuge, „Routine wird kurz"; keine Punkte, Serien, Ranglisten. Teil 1 vier Lehrtage, Prüfung als
  OSCE; Teil 2 fünf Ambulanztage (A1 = Herr Baum unverändert); Teil 3 Station, Intensiv, Reanimation, Finale
  Nachtdienst. Bestand-Tabelle (§10), Vorbilder (§11), Datenaufträge (§12), **14 offene Fragen (§13)**; Gutachten
  Medizin eingearbeitet (§14, voll in `docs/MECHANIK_GUTACHTEN.md`: „nach Änderungen freigeben", vier Muss-Punkte
  umgesetzt, u. a. Nachtdienst nur mitgehen, weil KPJ nie einzige ärztliche Ebene ist).
- Ersetzt nach Freigabe KONZEPT §2–§3 und GAME_DESIGN §2, §5; bis dahin gelten diese.

## Fertig (25.10.2026): Außenstil Tag und Blaue Stunde

`render aussen --stil tag|blau` (`TAG_PALETTE`, `STILE` in `haus_blockout.py`), beide angenommen, je für ihre Tageszeit
(ART_BIBLE §2, §4). Jahreszeit Spätherbst. Vorlagen des Nutzers nur lokal in `vorlagen/` (in `.gitignore`).

## Fertig (23.10.2026): Werkzeuge für Claude-Sitzungen

Hooks in `.claude/settings.json` (Textprüfung, Erinnerung an Commits), Skill `uebergabe`, Agenten `spieltester`,
`medizin-gutachter`, `uebersetzer` (`.claude/agents/`, Berichte in `bau/berichte/`).

## Fertig (23.10.2026): Außenansicht (a) zweite Überarbeitung

Talbiegung, Eckrisalite, Parkweg mit Laternen, Hecken, warme Fenster, Rettungswagen; Geisterschatten behoben. Vom Nutzer
freigegeben. Einzelheiten: KRANKENHAUS „Zweite Überarbeitung (23.10.2026)".

## Fertig (23.10.2026): Blockout nach Rückmeldung überarbeitet

Außengrün (ART_BIBLE §2), Bäume, Fensterpaare, Flur als Rasternetz, Kamera (b). Einzelheiten: KRANKENHAUS
„Überarbeitung nach Rückmeldung (23.10.2026)".

## Fertig (19.10.2026): Haus-Konzept und Blockout „Haus Föhrenhang"

`docs/KRANKENHAUS.md` (Raumprogramm, Grundrisse, Flug, Lageplan) und `gen/blender/haus_blockout.py` (`bauen`, `render`,
`grundriss`; Aufrufe in `gen/blender/README.md`). Lokal auf dem Mac eingerichtet (unten).

## Fertig (18.10.2026): Redesign-Entwurf Fall 1, Bewegungs-Prototyp, Skill `handlung`

`docs/REDESIGN_FALL1.md` (Entwurf zur Freigabe; „Darf Herr Baum heim?", sieben Takte, Gutachten eingearbeitet);
`prototyp/bewegung/` und `prototyp/fall1/` (Bau und Prüfung dort, `baue.py`, `pruefe.mjs`); Skill `.claude/skills/handlung/`.

## Fertig (13.10.2026): Referenzfall Herr Baum im neuen Fallschema

Motor `web/motor/` (fall, fenster, szenenbild), Fall `web/faelle/aufnahme_baum.js`, Akte `docs/faelle/aufnahme_baum.md`,
Texte über IDs in `text/{de,en,ru}/aufnahme_baum.json`, Prüfungen in `tools/durchlauf.mjs` und `tools/woerter.py`.

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

Seit 25./26.10.2026 als Saal im Haus neu gebaut und gestaltet (siehe „Fertig" oben); die folgenden Punkte gelten für die
Figuren weiter (Jonas liegt jetzt quer vor dem Giebelfenster, rechte Seite zur Klasse).
Alter Stand: Raum (`art/szenen/lehrsaal/`), Figuren Dr. Wieser und Jonas samt
Porträts als **ungeprüfter Zwischenstand** eingebettet; noch keine Spiellogik. Vor dem Weiterbauen prüfen:

- Jonas' Elektroden nach Ampel-Regel (FACHREGELN, Lektion 2): rechter Arm rot, linker Arm gelb,
  linkes Bein grün, rechtes Bein schwarz — Rot und Schwarz auf derselben Körperseite. Elektroden auf
  Haut (Hosenbeine hoch), nicht auf Kleidung; flach liegend, Beine gestreckt und nicht übereinander;
  T-Shirt hochgeschoben (Brustwand frei), jede Klemme mit Kabel zum Wagen. (`gen/blender/klemmen_setzen.py`
  war dafür in Arbeit.)
- Dr. Wieser: Akzent Kobaltblau `#2F5DA8` und blaues EKG-Lineal fehlen im Porträt; graue Haare mit 41 bewusst?
- Das Reizleitungs-Rätsel (`web/raetsel_reizleitung.js`) wartet hier auf seinen Einstieg (Whiteboard an der Flurwand,
  rechter Bildrand); der Durchlauf startet es bis dahin direkt.

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
- Spätherbst (25.10.2026, ART_BIBLE §4): Aufnahme braucht eine Fassung 06:40 im Kunstlicht mit Blauer Stunde vor dem
  Fenster; der Sonnenstreifen kommt erst gegen 07:10. Außen: Laub, tiefe Sonne (Tag-Stil höchstens etwa 25°).
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

## Startnachricht für eine neue Sitzung

```
Arbeite im Repository andreyeskin/ekg-nachtdienst auf dem Branch claude/stil-ligne-claire.
Lies zuerst docs/STAND.md, dann docs/KONZEPT.md, docs/UMBAU.md, docs/ART_BIBLE.md, docs/FACHREGELN.md
und die Skills unter .claude/skills/. Der Referenzfall ist web/faelle/aufnahme_baum.js. Prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
Auftrag für diesen Chat: <ein Arbeitsblock, z. B. „Nächster Auftrag" unten>
```

## Weiterer Auftrag (wartet auf den Nutzer): Mechanik freigeben

Der Nutzer beantwortet die offenen Fragen in `docs/MECHANIK.md` §13 (F1–F14, je eine Entscheidung mit Empfehlung).
Danach im selben Chat: Antworten in MECHANIK §13 eintragen, KONZEPT §2–§3, GAME_DESIGN §2/§5 und LEHRPLAN §2/§6 auf
MECHANIK verweisen lassen, committen, pushen. Folgeauftrag (eigener Chat): senkrechter Schnitt (MECHANIK §15.2:
Lehrtag 3 mit Testat, Prüfungsstation 3, Herr Baum mit Mentorbericht und Logbuch). Auftrag B (Fassade) läuft
unabhängig davon.

### Startnachricht

```
Arbeite lokal auf meinem Mac im Repository andreyeskin/ekg-nachtdienst, Branch claude/stil-ligne-claire.
Lies docs/STAND.md (Abschnitt „Weiterer Auftrag … Mechanik freigeben") und docs/MECHANIK.md ganz, dazu docs/KONZEPT.md §1–§3 und
docs/REDESIGN_FALL1.md §2–§3 nur bei Bedarf.
Auftrag: Geh mit mir die offenen Fragen in MECHANIK §13 einzeln durch (eine Frage je Nachricht, kurz, mit
Empfehlung), trag die Antworten ein und zieh KONZEPT, GAME_DESIGN und LEHRPLAN nach. Kein Code.
Koordination auf Opus. Commit nach jedem Teilschritt, pushen, STAND.md nachziehen. Antworte mir auf Russisch.
```

## Nächster Auftrag (ab 26.10.2026): Lehrsaal ins Spiel — Fensterblick, Ebenen, Zonen, Figuren, Raum

Der Saal ist gestaltet und angenommen („Fertig" oben, Probe `docs/haus/probe_lehrsaal.jpg`). Jetzt soll er im Spiel
erscheinen, statt der alten Seminarraum-Ebenen in `art/szenen/lehrsaal/`.

**Zuerst den Nutzer fragen:** Wie kommt man ins Spiel in den Lehrsaal, solange der Fall (Dialoge Wieser, Jonas;
`docs/UMBAU.md` §2d) noch fehlt? Vorschlag: Raum registrieren und über einen Prüfweg erreichbar machen (z. B.
`?raum=lehrsaal` oder ein Eintrag im Menü), Ausgang führt zur Aufnahme; das neue Spiel beginnt weiter in der Aufnahme.
Und: soll die eigene Bank (Zirkel, Streifen) eine eigene Klickzone `bank` bekommen?

1. **Fensterblick als Tafel** (KRANKENHAUS „Ein Haus, aus Bausteinen", Punkt 4): Fassade Südwest EG (beide Giebelfenster
   neben der Leinwand) und Südost EG (Nischenfenster links) einmal von außen rendern, gleiche Tageszeit und Farben wie der
   Saal (Himmel `#9EC3E0` → `#F2D2B0`), als flache Tafel hinter die Öffnungen; Kronen dicht davor ausdünnen.
2. **Ebenen-Pipeline für Hausräume**, eine Pipeline: `hintergrund.png`, `mittelgrund.png` (eigene Linien),
   `hitboxes.json`, `schirme.json` nach `art/szenen/lehrsaal/`. Ebenen und Zonen nach `lehrsaal.md` §4, §5, §7
   (Mittelgrund: Liege, Wagen, Bänke samt eigener Bank, Schachtel). Fallen: das Komposit braucht dieselbe kühle
   Schattenstufe (`schattenfarbe`, `schatten`) und das Pfirsichlicht wie `haus_blockout.komposit`, sonst wird der Saal
   wieder blass; der Wagenschirm ist um 38° gedreht, `schirme()` in `ebenen.py` nimmt den achsparallelen Kasten an und
   muss die echten Eckpunkte der Vorderseite nehmen; `ausgang` hat kein Objekt (Pfeil am rechten Bildrand).
3. **Figuren** Dr. Wieser und Jonas neu setzen (`figuren.py` `PLATZ`, Hauskoordinaten): Jonas liegend auf der Liege
   (x 0,85 … 1,5, y 0,35 … 2,3, Kopf bei y 0,35 auf dem 20°-Kopfteil, rechte Seite nach +x), Wieser stehend auf dem
   freien Boden zwischen Liege und Leinwand, nicht vor der Leinwand. Dann `figuren_zeichnen.py einsetzen lehrsaal`
   (ohne fal, Quellbilder in `art/figuren_quelle/`). Elektroden-Punkte unter „Halb fertig: Lehrsaal".
4. **Raum im Spiel** nach der Antwort des Nutzers: `web/spiel.js` registriert bisher nur `monitor`; Felder aus den Zonen,
   Schirme laufen über `starteSchirme`. Neue Spielertexte nur mit Skill `dialoge`, en/ru über den Agenten `uebersetzer`.

Fertig, wenn das gebaute Spiel den neuen Saal mit allen Zonen und Schirmflächen zeigt, der Durchlauf „Alle Prüfungen
bestanden." meldet und der Agent `spieltester` den Lehrsaal ohne Stocken bedient. Offen aus Auftrag B (nicht in diesem
Block): Fragen unter „Fassade und Hof" oben. Offen am Saal: die Sonne macht nur kleine Flecken (große Lichtbahnen wären
eine Lichtfrage).

### Startnachricht

```
Arbeite lokal auf meinem Mac im Repository andreyeskin/ekg-nachtdienst, Branch claude/stil-ligne-claire
(.venv mit bpy 5.2.2, Blender-Skripte mit .venv/bin/python, Cycles auf Metal).
Lies docs/STAND.md (Abschnitte „Nächster Auftrag" und „Halb fertig: Lehrsaal"), dann docs/raeume/lehrsaal.md §4–§8,
gen/blender/README.md (Ablauf je Raum oben und „Lehrsaal … Ausbau im Haus"), gen/blender/szene_lehrsaal.py,
gen/blender/ebenen.py, gen/blender/komposit.py und in gen/blender/haus_blockout.py nur KAMERAS, AUSBAUTEN,
kamera_stellen(), durchgang() und komposit(). docs/haus/probe_lehrsaal.jpg verkleinert ansehen.
Auftrag: den gestalteten Lehrsaal ins Spiel bringen. Zuerst mir die zwei Fragen aus „Nächster Auftrag" stellen.
1. Fensterblick als Tafel hinter den Fenstern (Südwest EG, Südost EG).
2. Ebenen-Pipeline für Hausräume (eine Pipeline): hintergrund, mittelgrund, hitboxes.json, schirme.json nach
   art/szenen/lehrsaal/, mit kühler Schattenstufe wie im Haus-Komposit und gedrehtem Wagenschirm.
3. Dr. Wieser und Jonas neu setzen (figuren.py PLATZ, figuren_zeichnen.py einsetzen lehrsaal, ohne fal).
4. Raum lehrsaal in web/spiel.js registrieren, wie ich es auf die Frage beantworte.
Prüfung: python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html"
"$PWD/bau/durchlauf", danach der Agent spieltester für den Lehrsaal. Alles auf Opus (Detailarbeit an einer
bestehenden Szene). Commit nach jedem Teilschritt, pushen, STAND.md nachziehen. Antworte mir auf Russisch.
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
