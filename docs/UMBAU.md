# Umbau — Änderungsliste und Umsetzungsplan

Stand: 11.10.2026, nachgezogen 13.10.2026. Folgt aus `docs/KONZEPT.md` und den Akten unter `docs/faelle/`.
Zeilennummern in §2 beziehen sich auf `web/spiel.js` im Stand des Branches `arbeit/konzept` (1367 Zeilen)
und sind Fundstellen; seit 13.10.2026 liegt Kapitel 1 in `web/faelle/aufnahme_baum.js`.

**Erledigt am 13.10.2026 (Branch `arbeit/episode`):** Schritt 3 (Fallschema, Motor, Texte über IDs) und der
Kapitel-1-Teil von Schritt 2 (§2a vollständig, §2b vollständig). Wie der nächste Fall nach dem Muster
angelegt wird: `docs/STAND.md`.

---

## 1. Reihenfolge

1. ~~**Architektur-Umbau** (KONZEPT §6): Herr Baum als Referenzfall in das Fallschema migrieren, Texte auf
   IDs, Motor trennen.~~ Erledigt 13.10.2026 (`web/motor/`, `web/faelle/aufnahme_baum.js`, `text/<sprache>/`).
2. **Kapitel 2 als Fall `monitor`** (`docs/faelle/monitor.md`): Frau Lindner, Ampel neu belegt, Herrn Baums
   Präsynkope und „Speicher" raus, Epilog von Herrn Baum an den Anfang von Dienst 3.
3. **Lehrsaal** (Raum + Figuren liegen vor; Fall nach `docs/faelle/lehrsaal.md`) mit den neuen Mechaniken
   aus §3; Reizleitung zieht dorthin um. Parallel: Datenauftrag 12-Kanal-Export (§5).

Nach jedem Schritt: `python3 gen/kunst.py`, `python3 tools/baue.py`, `node tools/durchlauf.mjs` ohne
Fehler; Durchlauf um Prüfungen für neue Wege erweitern (§7).

---

## 2. Was in `web/` und `text/` konkret umgeschrieben wird

### 2a. Stellen, die dem Grundsatz „Klinikalltag statt Detektivspiel" widersprechen (KONZEPT §1.3)

**Stand 13.10.2026: alle Zeilen dieser Tabelle, die Kapitel 1 betreffen, sind umgesetzt** (Tüte ohne
Klickzone, Medikationsplan im Gespräch, kein Verweis auf Verpasstes, Wagen-Meldung konkret, Karte
„Medikamente (Medikationsplan)", Export `__tuete` und Durchlauf-Schritt entfernt, verwaiste Übersetzungen
gelöscht). Offen bleibt nur die Ampel-Zeile (Kapitel 2, Frau Lindner).

| Fundstelle | heute | neu |
|---|---|---|
| `tueteAnsehen()` (767–789) und Feld `tuete` (1118–1124, `sichtbar: hat("darf_tuete")`) | die Tüte ist eine Rätselstation mit Frage „Welche Schachtel geht dich etwas an?" | **entfällt.** Die Medikamentenkarte entsteht im Anamnesedialog, wenn Herr Baum den Medikationsplan reicht (Knoten `herr_k.medis` → `befund(medisKarte(...))`). Die Klickzone `tuete` bleibt in `hitboxes.json` (Figur, Kunst), bekommt aber kein `bei` mehr oder nur eine Meldung („Die Tüte, die die Tochter gepackt hat. Fragen Sie ihn."). Die Pharmakologie-Frage (Betablocker vs. ACE-Hemmer vs. ASS) wandert als Rückmeldung in die Karte oder in Falks Übergabe. |
| `herr_k.medis` (428–433): „Darf ich reinschauen?" → `darf_tuete` | Zugang zur Tüte als Belohnung | Antwort reicht den Plan: „Drei in der Früh, seit Jahren dieselben. Die Tochter hat den Zettel vom Hausarzt eingepackt — da." Neue Folgefrage „Ist in letzter Zeit etwas neu dazugekommen oder geändert worden?" (Akte §5). Marken `darf_tuete`, `k_zeigt_tuete`, `tuete_gesehen`, `tuete_erklaert` entfallen. |
| `herr_k.start`, Option „Wer ist auf dem Foto?" `wenn: hat("tuete_gesehen")` (399) | Foto nur nach der Tüte | Foto-Frage ohne Bedingung (das Foto steht sichtbar in der Tüte) oder nach der ersten Anamnesefrage. |
| `falk.gut_medis` (466–472): „Steht im Aufnahmebogen, Marlene schreibt die Schachteln immer ab … Nächstes Mal schauen Sie in die Tüte" | Ersatzweg + nachträglicher Verweis | **entfällt.** Die Medikamentenanamnese ist Pflichtfrage; fehlt sie, mahnt der Stand der Schicht („Was Herr Baum einnimmt, weißt du nicht. Frag ihn.") und Falk fragt bei der Übergabe „Nimmt er etwas, das die ersten beiden macht?" — ohne Antwortoption, solange die Karte fehlt, schickt er zurück zum Patienten, nicht zur Tüte. |
| `marlene.start` Monitor-Zweig (267–273): „Die Tüte mit seinen Tabletten ist mit ihm hoch. Das Foto steht jetzt am Bett." + `tuete_erklaert` (280) | Verweis auf Verpasstes | **entfällt.** Marlene sagt nur, dass er oben liegt. |
| `kapitelStand()` (1033–1037): „In die Plastiktüte hast du noch nicht geschaut." | Hinweis auf Klickfeld | ersetzen durch „Was Herr Baum einnimmt, weißt du nicht. Frag ihn." (ohne Zweig). |
| `medisKarte()` (197–206) | Text spricht von „der Tüte oder dem Aufnahmebogen" | Karte heißt „Medikamente (Medikationsplan)"; Text ohne Ortsbezug; Zahlen wie heute. |
| `web/stil.css` 146 (`#buehne.baum-oben #fig-tuete`), `__tuete` (1363), `Spiel.__tuete` in `tools/durchlauf.mjs` | Technik der Station | Ausblenden bleibt (die Tüte geht mit ihm hoch), Export und Durchlauf-Schritt entfernen. |
| `text/en.json`, `text/ru.json`: Einträge „Die Tüte", „Die Tüte mit seinen Tabletten …", „Dann wissen Sie die Hälfte …", „ASS 100 — der Blutverdünner.", „Ramipril — der Blutdrucksenker.", „Bisoprolol — der Betablocker." und die zugehörigen `warum`-Sätze | Übersetzungen der Station | löschen bzw. an die neuen Sätze hängen (`tools/woerter.py` meldet verwaiste Schlüssel). |
| Feld `wagen` (1125–1137): „Erst fragen, dann schreiben. Marlene weiß, worum es geht." | Sperre mit vagem Hinweis | bleibt als klinische Reihenfolge (Anamnese vor EKG), Meldung konkret: „Erst die Anamnese: Was ist passiert, Medikamente, Untersuchung. Dann das EKG." |
| `ampel_pacer` (578–583) „Pacer" als Option; `auftakt.schluss`, `falk.ende2` („Speicher … Pause über drei Sekunden"), `k2_wache`, `ampel_*` (566–605), `ampelAusloesen()` (955–982) mit Herrn Baums Präsynkope | Kapitel 2 trägt Herrn Baum weiter | **Ampel neu belegt** mit Frau Lindner (Akte §6.2: Grün beobachten · Gelb bleiben, Falk rufen, 12-Kanal-EKG · Rot Notfallteam). Herrn Baums Präsynkope und der „Speicher" entfallen aus Kapitel 2 (Epilog: Entscheidung des Nutzers). |

Weitere Stellen desselben Musters, geprüft und **unverändert** gelassen, weil sie Figur oder
Atmosphäre sind und keinen Fortschritt tragen: Katzensticker (378–383), Pinnwand (1147–1153), Wanduhr
(1138–1146), Falks Zigarette (nur GAME_DESIGN).

### 2b. Kapitel 1 — Aufnahme (Akte §5–§8) — umgesetzt 13.10.2026, siehe Akte §8a

Abweichungen von der Liste unten: Die Übergabe an Dr. Falk findet am Tresen statt (Porträt-Dialog ohne
Raumfigur, Entscheidung des Nutzers); der Wagen ist frei, sobald Ereignis und Untersuchung erledigt sind,
die Medikamente mahnen Stand und Falk; der Epilog hängt vorerst am Ende von Kapitel 2 (siehe §2c).

- Anamnese-Baum `herr_k` um die Pflichtfragen erweitern (Prodrom, Situation, Dauer, Erholung, Zeugin:
  Zuckungen/Zungenbiss/Einnässen, Verletzung, Herzrasen, Brustschmerz/Atemnot, neurologische Ausfälle,
  Medikamente + Änderung, Diabetes, Alkohol/Schlafmittel, Vorerkrankungen, frühere Ohnmachten, Familie).
  Antworten aus Akte §5; Laiensprache; je Antwort eine Marke (`a_prodrom`, `a_zeuge`, …).
- Neuer Menüpunkt am Patienten **„Untersuchen"** mit Befundzeilen (Herz, Lunge, Beine, Neurologie
  orientierend) → Karte „Untersuchung". Kein Rätsel.
- **Aufnahmebogen** als Karte (Marlene reicht ihn oder liest vor): Vitalzeichen, Stehversuch (142/84 →
  134/80 nach 3 min, ohne Beschwerden), Blutzucker 104, Schürfung, Vorerkrankungen. Ersetzt die
  „Beweis"-Knoten teilweise; Marlenes `vorwarnung`/`beweis` bleiben inhaltlich (QUELLEN §3), kürzer.
- Neue Optionen mit belegten Rückmeldungen (Akte §4/§5): „Ist das nicht eine TIA?", „Hat er gekrampft?",
  „Unterzucker?", „War das überhaupt eine Ohnmacht — oder ein Sturz?", „Kreislauf — zu niedriger
  Blutdruck im Stehen?", „Ein Krampfanfall?" — bei Marlene und/oder Falk, Antworten in beiden Stimmen.
- EKG-Aufgaben wie heute; optional Zirkel `qrs` (86 ms) als dritte Zahl.
- **Dr. Falk kommt am Ende herunter** (Untersuchung, Übergabe, Entscheidung „Monitor") — neuer
  Dialogknoten in der Aufnahme statt nur oben; Figur Falk braucht einen Platz in `szene_aufnahme.py`
  (PLATZ, Klickzone) oder die Übergabe findet an der Tür statt (Porträt-Dialog ohne Raumfigur —
  billiger, erste Wahl).
- Stand der Schicht: Pflichtfragen zählen („Drei Dinge fehlen in der Anamnese: …"), keine Tüte.
- Das Rätsel **Reizleitung** wird aus `marlene.start`/`reizleitung`/`reizleitung_danach` (612–663)
  herausgenommen und im Lehrsaal an Dr. Wieser/Whiteboard gehängt (`raetsel_reizleitung.js` bleibt).

### 2c. Kapitel 2 — Monitorzimmer (Akte `monitor.md`)

- Konstanten: `SCHIRM_FLIMMERN_EKG = 96` wird **Frau Lindners Aufnahme** (`LINDNER_EKG`), Ersatzliste
  173, 110, 129, 38 mit Textvarianten; `SCHIRM_SCHNELL_EKG = 114` bleibt als dritter, namenloser Patient.
- `zentrale()`/`bettGefunden()` bleiben (Rückblick Herr Baum); Unterschrift von Bett 96 nennt jetzt
  Frau Lindner, sobald der Alarm war.
- Neuer Dialogbaum `lindner` (Akte §5, §10), Porträt nötig (§4).
- Ampel: Lage, Optionen und drei Falk-Knoten nach Akte §6.2; `fertig` führt in die Bett-Szene.
- Neue Aufgaben: „Monitor lesen" (Frage am Standbild), „Sechs Sekunden zählen" (neue kleine Mechanik:
  Streifenfenster 6 s, Zähler, Prüfung gegen Komplexe im Fenster × 10, Toleranz ± 10), „QRS schmal oder
  breit", „12-Kanal-EKG schreiben" (Zirkel `qrs`, `rr` an zwei Schlägen), Karte und Mappe-Vergleich mit
  `b-rhythmus` von Herrn Baum.
- `auftakt.monitor`, `auftakt.schluss` neu (Erzähler ohne „Hier endet …", solange weitere Kapitel
  folgen; sonst der Satz am Ende von Kapitel 2 mit Frau Lindner).
- Kopfzeile: Dienst + Uhrzeit („Dienst 1 · 09:15"); `zeitText()` um `Z.dienst` ergänzen.

### 2d. Lehrsaal (Akte `lehrsaal.md`, Raum `docs/raeume/lehrsaal.md`)

- Raum `lehrsaal` registrieren (Felder aus §5 der Raumbeschreibung), Dialogbäume `wieser`, `jonas`,
  `auftakt.lehrsaal`.
- Neue Mechaniken (jede als eigene Datei im Stil von `raetsel_zirkel.js`, Bedienung nach LEHRPLAN §5):
  - `raetsel_wellen.js` — **Zacken antippen**: Treffer gegen p0–p1, q0–q1, t0–t1 der Annotation
    (Strecken PQ, ST, QT als Intervalle daraus).
  - `raetsel_elektroden.js` — **Elektroden kleben**: Zuordnung ohne Daten; Körperschema aus
    `gen/kunst.py` (SVG), Klemmen in Rot/Gelb/Grün/Schwarz, sechs Punkte V1–V6.
  - `raetsel_lagetyp.js` — **Cabrera-Wahl**: erst nach dem 12-Kanal-Export (§5); bis dahin nicht bauen.
  - Zirkel-Aufgabe `p` (p0→p1) in `raetsel_zirkel.js` ergänzen; Frage-Typ „Papier lesen" über `frage()`.
  - Drei Kursstreifen über `raetsel_schirme.js` (142, 158, 160).
- Schirmfläche `projektion` als großes Papier (wie `gross` im Monitorzimmer, aber 50 mm/s und Standbild
  je Aufgabe), `wagen_schirm` wie Aufnahme, `whiteboard` als SVG-Ebene.
- Reizleitung-Einstieg von Marlene zu Dr. Wieser.
- Übergang Lehrsaal → Aufnahme: Erzähler „Dienst 1, 06:40 …"; `Z.dienst = 1`.

### 2e. Texte (`text/`)

- Alle neuen Sätze zuerst Deutsch in den Akten, dann `en.json`/`ru.json` im selben Schritt (Skill
  `dialoge` §5.5). Bei der Architektur-Migration (§6): Schlüssel `fall.figur.knoten.feld` statt
  deutscher Wortlaut; `sprache.js` akzeptiert übergangsweise beides.
- `tools/woerter.py`: verwaiste und fehlende Schlüssel je Sprache melden; Durchlauf bricht bei fehlender
  ID ab.

---

## 3. Mechaniken — Bestand und Neues

| Mechanik | Datei | Stand | Einsatz |
|---|---|---|---|
| Zirkel (rr, pq, qrs, qt) | `raetsel_zirkel.js` | fertig | überall; neu `p` |
| Reizleitung bauen | `raetsel_reizleitung.js` | fertig | Lehrsaal (verschoben) |
| Drei Schirme / Zentrale | `raetsel_schirme.js` | fertig | Monitor (Rückblick), Lehrsaal (Kursstreifen) |
| Ampel | `raetsel_ampel.js` | fertig | Monitor, neu belegt |
| Mappe-Vergleich | `mappe.js` | fertig | Baum ↔ Lindner |
| Frage mit Streifen | `spiel.js frage()` | fertig | Rhythmus, Papier, Monitor lesen, QRS breit/schmal |
| Zacken antippen | neu | — | Lehrsaal L1 |
| Elektroden kleben | neu | — | Lehrsaal L2 |
| Cabrera-Wahl (Lagetyp) | neu, nach Export | — | Lehrsaal L5/6 |
| Sechs Sekunden zählen | neu (klein) | — | Monitor L7/25 |
| Untersuchen / Aufnahmebogen (Befundzeilen) | `motor/fenster.js` (`befundzeilen`) | fertig | Aufnahme, Monitor |
| Szenenbild (Nahaufnahme ohne Klickzonen) | `motor/szenenbild.js` | fertig | Gesprächsanfänge, Schlüsselmomente |
| Fallmotor (Dialoge, Felder, Aufgaben, Karten, Stand aus Daten) | `motor/fall.js` | fertig | jeder Fall |

---

## 4. Arbeitspakete Blender / Bild (ART_BIBLE §5, `gen/blender/README.md`)

| Paket | Inhalt | Blocker |
|---|---|---|
| **Lehrsaal-Raum** | `szene_lehrsaal.py` nach `docs/raeume/lehrsaal.md` (Raumhülle, Tür, Fenster, Leinwand als `schirmflaeche("projektion")`, Whiteboard, Liege, Wagen, Tisch, Stühle, Schachtel, Uhr); Durchgänge `ebenen.py lehrsaal alle`, `komposit.py lehrsaal --layers`; `hitboxes.json`/`schirme.json` mit den Zonen aus §5 | keiner — kann sofort beginnen |
| **Figur Dr. Wieser** | Grundkörper in `figuren.py` (Haltung `tritt`, Lineal als Requisit, Kobaltblau), Stilphrasen `stil/figur_wieser.txt`, `stil/portrait_wieser.txt`; Blockout → Kontext → einsetzen; Porträt 400 × 440; drei bis vier Ausdrücke | Raum-Blockout (Platz) |
| **Figur Jonas** | liegende Haltung `liegen` (neu in `figuren.py`), Kopfhörer, Senfgelb; Porträt | Liege im Raum |
| **Figur Frau Lindner** | Porträt (Pflicht für den Dialog); Raumfigur optional — im Monitorzimmer ist kein Bett im Bild; die Bett-Szene läuft wie die Ampel heute als Text + Streifen. Wenn ein Bettplatz gewünscht ist: eigener kleiner Raum „Überwachungsbett" (neue Szene) | Entscheidung des Nutzers (§6) |
| **Dr. Falk in der Aufnahme** | nur, wenn die Übergabe als Raumfigur stattfinden soll; sonst Porträt-Dialog | Entscheidung (§6) |
| **SVG aus `gen/kunst.py`** | Körperschema mit Elektrodenpunkten (Elektroden kleben), Cabrera-Kreis (Lagetyp), Einthoven-Dreieck (Whiteboard) — alles ohne Schrift im Bild, Beschriftung durch den Code | keiner |

---

## 5. Daten-Arbeitspakete (`gen/export_spiel.py`, `data/`)

1. **Alle zwölf Ableitungen aus LUDB exportieren** (Annotation liegt je Ableitung vor): Feld `sig` wird
   zu `sigs: { i, ii, iii, avr, avl, avf, v1 … v6 }`, `schlaege` je Ableitung oder mit Verweis. Deckt
   Lektion 5/6 (Lagetyp), 14 (Hemiblock), 15 (R-Progression), 18 (Hypertrophie) und das 12-Kanal-Blatt im
   Lehrsaal. Speichergröße prüfen (eine Datei, iPad).
2. **Alter und Geschlecht** je LUDB-Aufnahme exportieren (Felder `alter`, `sex`), damit Figuren und
   Aufnahmen zusammenpassen (142 Jonas, 39 Herr Baum, 96 Frau Lindner); Fallakten danach nachführen.
3. **PTB-XL-Signale** für die Gruppen, die LUDB nicht hat (STACH, 2AVB, 3AVB, Infarkt, SVT/WPW, PVC)
   mit `messbar: false` — Auftrag 4 aus `AUFTRAEGE.md`; zusätzlich die Artefakt-Felder der PTB-XL-Tabelle
   (baseline_drift, static_noise, burst_noise, electrodes_problems) für Lektion 37.
4. **Prüfen:** 175 („Sinoatrial blockade, undefined") — ob die Pause 1022 ms als SA-Block II° lesbar ist
   (Vielfaches des PP? nein: 762–1022). Bis dahin nicht verwenden.
5. Kursstreifen-Gruppen als Listen im Export (Normal: 142, 198, 149; Sinusarrhythmie: 158, 63;
   Sinusbradykardie: 160, 47, 1, 41; AV-Block I°: 39, 134, 78, 107, 77; VHF schmal: 96, 173, 110, 129,
   38), damit `spiel.js` ohne Literale zieht (GAME_DESIGN §5, Wiederspielwert).

---

## 6. Entscheidungen des Nutzers

| Entscheidung | Empfehlung |
|---|---|
| Rotation statt Schicht (KONZEPT §2) | ja |
| Epilog für Herrn Baum (Erzählung; optional PTB-XL-Standbild AV-Block II°, nur Ansehen) | ja, als Erzählung in einem späteren Dienst; Standbild nur mit Beschriftung „andere Aufnahme, gleiche Diagnose" |
| Reizleitung in den Lehrsaal | ja |
| Dr. Falk als Raumfigur in der Aufnahme oder Porträt-Dialog an der Tür | Porträt-Dialog zuerst (kein Blender-Paket); Raumfigur später, wenn der Raum ohnehin neu gerendert wird |
| Frau Lindner nur als Porträt oder mit eigenem Bettplatz-Raum | zuerst Porträt; Bettplatz als eigenes Paket, wenn die Station gebaut wird (dann für alle Patienten) |
| Lagetyp warten auf den 12-Kanal-Export oder Schema | warten; Export ist ein Datenauftrag, der vier Lektionen öffnet |
| Namen/Alter der neuen Figuren (Wieser 41, Jonas 24, Lindner 76) | übernehmen; nach Export der LUDB-Alter ggf. anpassen |
| Textschlüssel fallweise oder in einem Zug | fallweise mit Übergangsfunktion |
| Vorhofflimmer-Anamnese: Fragen nach Blutverdünner, Schilddrüse, Alkohol im Spiel lassen (nur „notiert", keine Ursache behauptet) | ja, mit Belegen aus ESC-AF-2020 in QUELLEN §8, Stellen am Original prüfen |

---

## 7. Prüfungen (`tools/durchlauf.mjs`)

- Lehrsaal: jede Pflichtaufgabe lösbar; Zacken-Treffer gegen Annotation; Elektroden-Zuordnung; drei
  Kursstreifen; Tür erst danach frei.
- Aufnahme (**umgesetzt 13.10.2026**): Medikamentenkarte entsteht im Dialog; kein Weg führt über die Tüte;
  Falk ohne Karte schickt zum Patienten; Pflichtfragen → Mahnung im Stand; TIA bei Marlene und Falk
  beantwortet; Übergabe nur mit beiden Zahlen (drei Rückwege); Ende und Epilog; Szenenbild beim ersten
  Gespräch; Untersuchung und Aufnahmebogen als Karten; alle IDs in de/en/ru, keine Gedankenstriche,
  Repliken ≤ 230 Zeichen; Textüberlauf de/en/ru bei 1024×768 und 1366×1024; Zirkel maßstabstreu bei drei
  Bildschirmgrößen (±2 ms, gleiche Bewertung).
- Monitor: Bett von Frau Lindner trägt 96 (oder Ersatz); Alarm jede Wahl → Falk-Szene; 6-s-Zählung
  gegen Komplexe im Fenster; Vergleich Baum ↔ Lindner; Therapieaussagen nur mit Beleg (QUELLEN §4).
- Allgemein: keine Lektionsnummern im Spieltext; jede Zahl im Text aus `mess`/Messung (Grep auf
  Literale wie `228`, `53` in Dialogen schlägt an).
