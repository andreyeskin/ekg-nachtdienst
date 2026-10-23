# Nachtdienst — Hinweise für jede Sitzung

EKG-Lernspiel (Vanilla HTML/JS, ein Bau-Ergebnis `bau/nachtdienst.html`). Arbeitsbranch:
`claude/stil-ligne-claire`. Einstieg und aktueller Stand: `docs/STAND.md` (zuerst lesen, sonst nichts
auf Vorrat). Bau und Prüfung:

```
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf"
```

- Lehrbuch (Trappe, EKG-Kurs) nur aus dem Drive-Ordner „EKG-Kurs Texte (privat, nur für Claude-Sitzungen)";
  nie ins Repository, nur eigene Worte mit Lektionsnummer.
- Neue Fälle und Dialoge nur mit den Skills `fallakte` und `dialoge` (`.claude/skills/`).
- Commit nach jedem Teilschritt, dann pushen. Chatwechsel mit dem Skill `uebergabe`.
- Agenten (`.claude/agents/`): `spieltester` nach Änderungen am Spiel, `medizin-gutachter` vor jeder Freigabe
  eines Falls, `uebersetzer` für en/ru. Hooks in `.claude/settings.json` prüfen Texte nach jeder Bearbeitung.

## Tokensparen (der Nutzer will dazu immer beraten werden)

**Ein Chat = ein Arbeitsblock.** Am Ende einer Antwort einen kurzen **Token-Tipp** geben, wenn einer passt,
und ausdrücklich zu einem neuen Chat raten, sobald einer dieser Punkte zutrifft:

- ein Block ist fertig und gepusht (z. B. ein Fall, eine Szene, ein Redesign-Entwurf);
- das Thema wechselt (vom Bild zur Medizin, vom Fall 1 zum Fall 2);
- der Chat ist lang oder wurde schon zusammengefasst („This session is being continued …");
- Antworten werden langsam, vergessen Absprachen oder wiederholen Fehler.

**Vor dem Wechsel:** alles committen und pushen, `docs/STAND.md` nachziehen (Fertig, Offen, Nächster
Auftrag), die Startnachricht dort aktuell halten. Dann braucht der neue Chat nur diese Nachricht.

**Mit dem alten Chat:** Hintergrund-Agenten stoppen; danach kann er geschlossen oder archiviert werden,
es geht nichts verloren, weil alles im Repository steht. Archivieren nur auf Wunsch des Nutzers.
Nicht im alten Chat „noch schnell" etwas Neues anfangen.

**Modellwahl:** Fable nur für 3D-Szenen, Medizin-Abgleich und Falldesign; Opus für Koordination und
Code; Sonnet für Routine (Übersetzungen, Prüfungen ergänzen, Aufräumen); Haiku für rein Mechanisches.

**Im Chat sparsam:**
- Dateien gezielt lesen (grep, Ausschnitte), nicht ganz; große Dateien (`malen.py`, ART_BIBLE) nur abschnittsweise.
- Bilder und Screenshots nur ansehen, wenn sie für die Entscheidung nötig sind; verkleinert.
- Testausgaben filtern (`| tail`, `grep -E "FEHL|bestanden"`), nie ganze Logs.
- Agenten kurze, genaue Aufträge mit Dateiliste geben; Ergebnisse in Dateien schreiben lassen statt langer Berichte.
- Bildgenerierung: erst niedrige Qualität testen; fal/Flux für kleine Änderungen, GPT Image für Szenen mit Figuren.
