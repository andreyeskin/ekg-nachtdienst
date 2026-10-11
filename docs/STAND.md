# Stand und Übergabe — Pause am 11.10.2026

Diese Datei ist der Einstieg für die nächste Sitzung. Alles Genannte liegt auf dem Branch
`claude/stil-ligne-claire` und ist gepusht. Prüfung des Stands: `python3 gen/kunst.py &&
python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"`
→ „Alle Prüfungen bestanden." (280 Prüfungen).

## Fertig

- **Räume** Aufnahme und Monitorzimmer: Fenster mit Jalousie, eigene Raumfarben, logische Möbel,
  laufende EKG-Kurven auf EKG-Wagen und Bettmonitoren (vom Code aus `data/`, nie gemalt).
- **Figuren** Marlene, Herr K., Dr. Falk neu gezeichnet (Blender-Blockout → FLUX.1 Kontext über fal.ai),
  zweistufige Pipeline in `gen/blender/figuren_zeichnen.py` (Quellbilder in `art/figuren_quelle/`).
- **Fachabgleich** mit dem Lehrbuch (`docs/FACHREGELN.md`, `docs/QUELLEN.md`), Herzschema mit Faszikeln.
- **Oberfläche als Spiel**: Vollbild-Bühne, Titelbildschirm, HUD, Pausenmenü mit Info & Quellen (`web/huelle.js`).
- **Konzept, zweite Fassung** (`docs/KONZEPT.md`): ein Patient je Fall, Klinikalltag statt Detektivspiel,
  Rotation statt einer Schicht; Fallakten `docs/faelle/{lehrsaal,aufnahme_baum,monitor}.md`
  (Herr Baum mit vollständiger Synkopen-DD inkl. TIA), Umbauplan `docs/UMBAU.md`.
- **Skills** für die Arbeit an Inhalten: `.claude/skills/dialoge/` und `.claude/skills/fallakte/`.

## Halb fertig: Lehrsaal

Raum fertig (`gen/blender/szene_lehrsaal.py`, `art/szenen/lehrsaal/`), Figuren Dr. Wieser und Jonas samt
Porträts als **ungeprüfter Zwischenstand** eingebettet; noch keine Spiellogik. Vor dem Weiterbauen prüfen:

- Jonas' Elektroden nach Ampel-Regel (FACHREGELN, Lektion 2): rechter Arm rot, linker Arm gelb,
  linkes Bein grün, rechtes Bein schwarz — Rot und Schwarz auf derselben Körperseite. Elektroden auf
  Haut (Hosenbeine hoch), nicht auf Kleidung; flach liegend, Beine gestreckt und nicht übereinander;
  T-Shirt hochgeschoben (Brustwand frei), jede Klemme mit Kabel zum Wagen. (`gen/blender/klemmen_setzen.py`
  war dafür in Arbeit.)
- Dr. Wieser: Akzent Kobaltblau `#2F5DA8` und blaues EKG-Lineal fehlen im Porträt; graue Haare mit 41 bewusst?

## Offene Entscheidungen des Nutzers (Empfehlung in Klammern)

1. Rotation über mehrere Dienste statt einer Schicht (ja)
2. Epilog für Herrn Baum als Erzählung in einem späteren Dienst (ja)
3. Reizleitungs-Rätsel wandert in den Lehrsaal (ja)
4. Dr. Falk in der Aufnahme und Frau Lindner zunächst nur als Porträt-Dialog (ja)
5. Lagetyp erst nach dem 12-Kanal-Export (ja; `data/` enthält bisher nur Ableitung II)
6. Namen und Alter der neuen Figuren: Wieser 41, Jonas 24, Lindner 76 (übernehmen)

## Nächste Schritte (nach Freigabe, Reihenfolge aus `docs/UMBAU.md` §1)

1. Lehrsaal-Figuren prüfen und korrigieren, dann den Lehrsaal-Fall bauen (`docs/faelle/lehrsaal.md`);
   parallel 12-Kanal-Export aller LUDB-Ableitungen (UMBAU §5).
2. Kapitel 1 und 2 auf das neue Konzept: Tüten-Station raus, Anamnese mit Medikationsplan,
   Monitorzimmer mit Frau Lindner (UMBAU §2a–2c).
3. Architektur-Umbau: eine Datei je Fall, Texte über IDs, Motor getrennt (KONZEPT §6).

## Bekannte offene Punkte

- Aufnahme um 09:20 zeigt noch das Sonnenaufgangslicht (zweite Lichtfassung fehlt).
- Thermoskanne: ART_BIBLE §5 sagt Magenta, §2 verbietet Magenta im Raum; gerendert ist Rost.
- Rund 157 ältere Sätze ohne en/ru-Übersetzung.
- Neulade-Prüfung im Durchlauf scheitert selten sporadisch (Chromium über `file://`); Abhilfe: Durchlauf über `http://127.0.0.1`.
- Falks Kaffeefleck und Zirkel in der Brusttasche fehlen.

## Arbeitsweise (vom Nutzer festgelegt)

- Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
- Jeder Agent in eigenem git worktree, Commit nach jedem Teilschritt (Limits können abbrechen).
- Lehrbuch (Trappe, EKG-Kurs) nur aus dem Drive-Ordner „EKG-Kurs Texte (privat, nur für Claude-Sitzungen)",
  Inhaltsverzeichnis `00_INHALT.txt`; nie ins Repository, nur eigene Worte mit Lektionsnummer.
- Bildgenerator fal.ai ist über den Proxy der Cloud-Umgebung angebunden (`gen/blender/malen.py`).

## Startnachricht für eine neue Sitzung

```
Arbeite im Repository andreyeskin/ekg-nachtdienst auf dem Branch claude/stil-ligne-claire.
Lies zuerst docs/STAND.md, dann docs/KONZEPT.md, docs/UMBAU.md, docs/ART_BIBLE.md, docs/FACHREGELN.md
und die Skills unter .claude/skills/. Prüfe den Build:
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
Komplexe Aufgaben (3D-Szenen, Medizin-Abgleich) als Subagent auf Fable, Routine auf Opus/Sonnet.
```
