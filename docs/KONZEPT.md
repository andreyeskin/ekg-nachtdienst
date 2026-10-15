# Konzept — „Nachtdienst", zweite Fassung

Stand: 11.10.2026. Dieses Blatt ersetzt die Grundidee „eine Schicht, ein Patient" aus `GAME_DESIGN.md`
§1–2. Was dort über Mechaniken, warme Räume, Anspielungen und Technik steht, gilt weiter;
`LEHRPLAN.md` bleibt die Gliederung des Stoffes. Grund für die zweite Fassung: die Rückmeldung des
Nutzers (Arzt) — Inhalt und Dialoge müssen maximal logisch sein; ein Patient, der den ganzen Stoff
trägt, ist Unsinn; Informationen kommen aus dem Klinikalltag, nicht aus versteckten Gegenständen.

---

## 1. Grundsätze

1. **Ein Fall, ein Patient, ein Lernziel.** Jeder Fall gehört zu genau einer Lektion oder Diagnose und hat
   seinen eigenen Patienten mit eigener Aufnahme aus `data/`. Kein Patient trägt Stoff, den seine Aufnahme
   nicht zeigt. Jeder Fall hat eine Akte unter `docs/faelle/<id>.md` nach dem Skill `fallakte`, bevor ein
   Satz Dialog entsteht.
2. **Kontinuität tragen die festen Figuren, das Haus und die Spielfigur** — Marlene, Dr. Falk, Dr. Wieser,
   die Räume, die Befundmappe, das Lineal aus dem Kurs. Patienten kommen und gehen, wie im Dienst. Ein
   Patient darf wiederkehren (Herr Baum liegt im Monitorzimmer), aber er ist dann Kulisse oder Rückblick,
   nicht Träger eines neuen Lernziels.
3. **Klinikalltag statt Detektivspiel.** Informationen kommen über den normalen klinischen Ablauf:
   Anamnese (einschließlich Medikamentenanamnese), Aufnahmebogen bzw. Pflegeanamnese, mitgebrachter
   Medikationsplan oder Arztbrief, Vitalzeichen, körperliche Untersuchung, Vorbefunde und Labor, soweit
   belegt. **Kein Fortschritt und keine Pointe hängt an einem Klickfeld, das man nur zufällig findet.**
   Niemand verweist nachträglich auf etwas, das die Spielerin nicht verpassen konnte und trotzdem verpasst
   hat. Gegenstände im Raum gehören jemandem (ART_BIBLE §7) und dürfen Atmosphäre sein — Rätselstation
   sind sie nicht. Die Anamnese folgt der Reihenfolge, in der eine Ärztin wirklich fragt; Pflichtinhalte
   werden nicht übersprungen; optionale Fragen sind echte Vertiefungen, keine versteckten Schlüssel.
4. **Eindeutigkeit.** Die richtige Antwort folgt zwingend aus Aufnahme und Anamnese; jede falsche Option
   ist mit einem konkreten Merkmal widerlegbar; Fangfragen, die je nach Quelle richtig oder falsch sind,
   sind verboten. Die Fragen, die eine Ärztin reflexhaft stellt („Ist das nicht eine TIA?"), stehen als
   Antwortoption da und bekommen eine belegte Antwort im Ton der Figur (Skill `fallakte`, Experten-Reflex).
5. **Die Lehre steht im Feedback, nicht im Gespräch.** Figuren reden wie Menschen (Skill `dialoge`);
   Begründungen, Normwerte und Kriterien stehen in der Rückmeldung einer Wahl und auf den Karten der Mappe.
6. **Echte Kurven, belegte Sätze.** Unverändert: alle Kurven aus `data/`, alle Zahlen aus der Annotation,
   jede fachliche Aussage in `FACHREGELN.md` (Lehrbuch, eigene Worte) oder `QUELLEN.md` (offene Quelle mit
   Stelle). Lektionsnummern nie im Spieltext.
7. **Behandlung gehört zum Fall** (Entscheidung des Nutzers, 15.10.2026; keine Einschränkung mehr): Jeder Fall
   endet mit dem, was mit dem Patienten geschieht. Therapie, Medikamente mit Dosierung, Eingriffe und
   Behandlungsentscheidungen der Spielerin sind erlaubt, jede Aussage mit Beleg (QUELLEN §4).

---

## 2. Zeitrahmen: eine Rotation, nicht eine Schicht

**Entscheidung:** Das Spiel läuft über **mehrere Dienste einer Famulatur/KPJ-Rotation**, beginnend mit
einem Einschulungstag im Lehrsaal. Der Titel „Nachtdienst" wird im letzten Kapitel eingelöst: Die
Abschlussprüfung (Befundraum, Chefvisite) ist ein Nachtdienst, in dem alles zusammenkommt.

Warum nicht eine Schicht:
- Mit Grundsatz 1 hat jede Abteilung eigene Patienten. Dass eine Famulantin an einem Tag einen
  Schenkelblock auf Station, einen Infarkt im Herzkatheter, ein WPW in der Rhythmusambulanz und einen
  Schrittmacher auf der Intensivstation befundet und am selben Abend die Chefvisite besteht, ist genau
  die Unlogik, die der Nutzer beanstandet. Eine Rotation über Wochen ist der Alltag.
- Der Lehrsaal liegt sinnvoll **vor** dem ersten Dienst, nicht mitten in der Schicht.
- Die Uhr bleibt als Erzählmittel (Licht, Müdigkeit, Geräusche); sie bekommt nur ein zweites Wort:
  **„Dienst 1 · 06:40"** statt nur „06:40". Innerhalb eines Kapitels läuft die Zeit wie bisher weiter.

Was bleibt: Kapitel 1 und 2 liegen weiter in **einem** Frühdienst (06:40 Aufnahme → 09:15 Monitorzimmer),
weil Herrn Baums Weg nach oben und sein Bett an der Monitorwand die Kontinuität zwischen beiden Räumen
sind. Jedes weitere Kapitel ist ein eigener Dienst.

**ART_BIBLE §4** wird minimal angepasst: die Tabelle bekommt eine Spalte „Dienst" und die Zeile
„0 Lehrsaal · Einschulungstag 08:10 · Vormittag, neutrales Tageslicht, Beamer an"; die Zeiten der
übrigen Kapitel bleiben, jedes Kapitel ab 3 steht an einem eigenen Tag. Die Nacht mit Regen bleibt dem
Finale vorbehalten.

---

## 3. Ablauf

| Kapitel | Dienst, Zeit | Raum | Fall (eigener Patient) | Lektionen | Feste Figur |
|---|---|---|---|---|---|
| 0 | Einschulungstag, 08:10 | Lehrsaal | Jonas Prem, 24, Tutor als Freiwilliger (Normal-EKG) + anonymisierte Kursstreifen | 1–7, 8 (Varianten) | Dr. Wieser |
| 1 | Dienst 1, 06:40 | Aufnahme | Herr Konrad Baum, 68 — Synkope; Sinusrhythmus langsam, AV-Block I° | 8, 10 (I°); Synkope: ESC | Marlene |
| 2 | Dienst 1, 09:15 | Monitorzimmer | Frau Gerda Lindner, 76 — Herzstolpern; Vorhofflimmern am Monitor. Herr Baum liegt in einem anderen Bett (Rückblick: „Welches Bett ist er?") | 31, 25, 7 (mittlere Frequenz) | Dr. Falk |
| 3 | Dienst 2, 13:30 | Station | Frau mit Luftnot — Schenkelblock (LUDB 24 LSB / 23 RSB) | 13 (später 12, 14, 15, 18) | Marlene |
| 4 | Dienst 3, 18:50 | Intensiv | Schrittmacherpatient (LUDB 74/34/90/111) und Patient mit langer QT-Zeit (LUDB 29, QTc 553 ms) | 30, 17 | Dr. Falk |
| 5 | Dienst 4, 10:00 | Herzkatheter / Chest Pain | Mann mit Druck auf der Brust — Infarkt (PTB-XL, nur Ansehen) | 16, 19, 20 | neu |
| 6 | Dienst 5, 15:00 | Rhythmusambulanz | Junge Frau mit Herzrasen (PTB-XL SVT/WPW, nur Ansehen); Vorhofflattern (LUDB 35/52/103) | 24, 25 | neu |
| 7 | Dienst 6, 22:10 | Innere / Aufwachraum | Spezialfälle mit Schema, wo Daten fehlen | 21–23, 27, 29, 32 | Marlene |
| 8 | Nachtdienst, 02:14 | Befundraum, Chefvisite | alle Aufnahmen der Datenbank; drei Fragen mit Belegen | 34 (35–38) | Dr. Falk |

Innerhalb eines Kapitels bleibt alles, was `GAME_DESIGN.md` §2 sagt: Räume frei betretbar, zwei von drei
Beweisstücken, Figuren reagieren auf den Stand, kein Game Over. Zwischen Kapiteln erzählt der Erzähler
den Tageswechsel in einem Satz.

---

## 4. Was aus den bestehenden Kapiteln 1 und 2 wird

**Bleibt (gut, nicht anfassen):** die Räume Aufnahme und Monitorzimmer, Marlene, Dr. Falk, Herr Baum
mit Tüte und Foto als Figur, die Mechaniken Zirkel, Mappe-Vergleich, Reizleitung bauen, Drei Schirme
(Zentrale), Ampel, Stand der Schicht, die Bedienregeln aus LEHRPLAN §5.

**Kapitel 1 — Herr Baum** bleibt der Fall „Synkope mit Sinusrhythmus langsam + AV-Block I°"
(`docs/faelle/aufnahme_baum.md`). Änderungen:
- Die Anamnese wird vollständig und expertenhaft: echter Bewusstseinsverlust ja/nein; die
  Differenzialdiagnosen als Fragen der Spielerin (reflektorisch, orthostatisch, kardial; Krampfanfall,
  psychogen, TIA/Schlaganfall, Hypoglykämie, Intoxikation, Sturz ohne Bewusstseinsverlust) mit belegten
  Antworten; Risikomerkmale; was das EKG beiträgt und was nicht.
- **Die Tüte ist keine Rätselstation mehr.** Die Medikamente erfragt die Spielerin als
  selbstverständliche Anamnesefrage; Herr Baum antwortet in Laiensprache und reicht den Medikationsplan,
  den die Tochter in die Tüte gelegt hat. Die Tüte bleibt sein Gegenstand im Raum (ART_BIBLE §5), ohne
  Klickzone, die Fortschritt trägt. Falks „Nächstes Mal schauen Sie in die Tüte" und Marlenes Satz
  „Die Tüte ist mit ihm hoch" entfallen (UMBAU §2).
- Blutdruck im Liegen und Stehen (Pflegeanamnese), Blutzucker-Stix, kurze körperliche Untersuchung durch
  Dr. Falk gehören zum Ablauf — als Befundzeilen auf dem Aufnahmebogen, nicht als Rätsel.
- Das Kapitel endet klar: AV-Block I° und langsame Frequenz unter Betablocker erklären die Zahlen, nicht
  die Ohnmacht; fehlendes Prodrom plus auffälliges EKG sind nach ESC Risikomerkmale; deshalb Monitor.
  Was der Monitor später zeigt, ist nicht mehr dieser Fall.
- Das Rätsel „Reizleitung bauen" wandert in den Lehrsaal (Lektion 1, Whiteboard bei Dr. Wieser). Marlene
  behält ihre Katze, ihre Thermoskanne und den Fall.

**Kapitel 2 — Monitorzimmer** bekommt einen eigenen Patienten und ein eigenes Lernziel
(`docs/faelle/monitor.md`): Frau Lindner, 76, seit der Nacht am Monitor wegen Herzstolperns; am Schirm
Vorhofflimmern (LUDB 96). Lernziel: am Monitor Rhythmus und Frequenz beurteilen (Vorhofflimmern erkennen:
keine P-Welle, absolut unregelmäßig; mittlere Frequenz aus sechs Sekunden), und wissen, was der Monitor
nicht kann (keine Feinanalyse; jede Auffälligkeit → 12-Kanal-EKG). Herr Baum liegt in einem der drei
Betten — die Zentrale-Aufgabe „Welches Bett ist Herr Baum, woran siehst du es?" bleibt als Rückblick,
weil sie die am Morgen gemessenen Zahlen noch einmal arbeiten lässt. Die Ampel gehört Frau Lindner:
Monitoralarm, sie ist wach — bleiben, Arzt rufen, 12-Kanal-EKG schreiben (Gelb). Herrn Baums
Präsynkope am Bett und der „Speicher" entfallen aus Kapitel 2; ob Herr Baum später einen Epilog bekommt,
entscheidet der Nutzer (§7).

---

## 5. Fallkatalog

Geprüft am 11.10.2026 gegen `data/ekg_daten.json` (199 LUDB-Aufnahmen, nur Ableitung II, 250 Hz, 10 s,
Wellen-Annotation) und `data/ptbxl_auswahl.json` (458 Einträge, nur Index — keine Signale im Repository,
`messbar: false`). Zahlen sind Mediane aus der Annotation; „Ersatz" nennt Aufnahmen derselben Gruppe für
den Wiederspielwert.

| Lektion | Diagnose / Lernziel | Patient (Kurzprofil) | Aufnahme-ID(s) LUDB | Raum | Mechanik | Stand |
|---|---|---|---|---|---|---|
| 1 | Zacken benennen, Reizleitung | Jonas Prem, 24, Tutor, Kopfhörer, „langweiliges EKG" | **142** (SR, 74/min, P 84 ms, PQ 130, QRS 84, QT 356); Ersatz 198, 149 | Lehrsaal | Wellen antippen (neu), Reizleitung bauen (Whiteboard) | ok |
| 2 | Ableitungen, Elektroden, Papier, Eichzacke | Jonas | 142 | Lehrsaal | Elektroden kleben (neu, ohne Daten); Papier-Frage | **Lücke**: nur Ableitung II exportiert — 12-Kanal-Blatt erst nach Export |
| 3 | P-Welle, PQ-Zeit messen | Jonas | 142 (P 84, PQ 130) | Lehrsaal | Zirkel `p` (neu), `pq` | ok |
| 4 | QRS, ST/T, QT messen | Jonas | 142 (QRS 84, QT 356, QTc 397) | Lehrsaal | Zirkel `qrs`, `qt` | ok |
| 5–6 | Lagetyp | Jonas | 142 — braucht I, II, III, aVR, aVL, aVF | Lehrsaal | Cabrera-Wahl an der Projektion (neu) | **Lücke** (Export); Übergang: Schema, als Schema beschriftet |
| 7 | Rhythmus (fünf Fragen), Frequenz (Kästchen, Lineal, Zirkel) | Jonas | 142 | Lehrsaal | Kästchen-Regel gegen Zirkel | ok |
| 8 | Sinusrhythmus und Varianten | anonymisierte Kursstreifen (kein Patient) | Sinusarrhythmie **158** (PP 790–1052, Δ 262 ms), Ersatz 63; Sinusbradykardie **160** (44/min), Ersatz 47, 1, 41 | Lehrsaal | Drei Streifen vergleichen | Sinustachykardie > 100/min: **Lücke** in LUDB (Maximum 99/min, Nr. 92); PTB-XL STACH nur Ansehen |
| 8 + 10 (I°) | Synkope; Sinusrhythmus langsam, AV-Block I° | Herr Konrad Baum, 68, Schiebermütze, Tüte, Foto der Enkelin | **39** (53/min, PQ 228, QRS 86); Ersatz 134 (50/min, PQ 244), 78 (62/min, PQ 226), 107 (PQ 214), 77 (PQ 212) | Aufnahme | Anamnese mit DD-Optionen, EKG schreiben, Zirkel RR/PQ, Mappe | ok |
| 9 | SA-Block, kranker Sinusknoten | — | 175 („Sinoatrial blockade, undefined": PP 762–1022 ms, kein klares Vielfaches) | später (Rhythmusambulanz) | Ansehen mit Vorbehalt | **dünn** |
| 10 (II°, III°) | Mobitz, Wenckebach, totaler Block | eigener Patient später | LUDB III° nur mit Kammerschrittmacher (34, 74, 90, 111, keine P-Marken); PTB-XL 2AVB 14 / 3AVB 16 (Ansehen) | Station / Intensiv | Vergleichen, nicht messen | **Lücke** mit Annotation |
| 11 | AV-junktionaler Rhythmus | — | 0 in LUDB | — | — | **Lücke** |
| 31 (+ 25, 7) | Monitor-EKG; Vorhofflimmern erkennen; mittlere Frequenz | Frau Gerda Lindner, 76, Herzstolpern seit der Nacht, Strickzeug am Bett | **96** (VHF, 90/min im Mittel, QRS 74–88, RR 470–1096); Ersatz 173 (82/min), 110 (90/min, ein aberranter Komplex), 129 (60/min), 38 (113/min, ein breiter Komplex) | Monitorzimmer | Drei Schirme, Ampel, 6-s-Zählung, Mappe-Vergleich mit Baum-Streifen | ok |
| 12 | Vorhofleitung (P-sinistroatriale) | eigener Patient | „Left atrial hypertrophy" 102× (P > 100 ms), z. B. 13 (P 158), 102 (P 142) | Station | Zirkel `p` | ok (nur II) |
| 13 | Schenkelblock | Frau mit Luftnot | **24** (LSB, QRS 160, 51/min), **23** (RSB, QRS 153); inkomplett 29× RSB, 6× LSB | Station | Zirkel `qrs`, Vergleich M-Form | ok (II) |
| 14 | Hemiblock | eigener Patient | LAH 16× (21, 26, 46, 55, 65, 84, 138, 164 …) — Lagetyp braucht Extremitätenableitungen | Station | — | **Lücke** (Export) |
| 15, 18 | R-Progression, Hypertrophie (Sokolow) | — | braucht V1–V6 | Station | — | **Lücke** (Export) |
| 16, 19, 20 | ST/T, Infarkt, Lokalisation | Mann mit Druck auf der Brust | LUDB 0; PTB-XL 101 (Ansehen) | Herzkatheter | Vergleichen | nur Ansehen |
| 17 | lange QT-Zeit | eigener Patient (Intensiv) | **29** (QT 531, QTc 553); 61 (QTc 521), 116 (508) | Intensiv | Zirkel `qt` + Bazett | ok |
| 24, 26 | SVT, WPW, VES/VT | junge Frau mit Herzrasen | LUDB 0; PTB-XL SVTAC 23, WPW 20, PSVT 15, PVC 8 (Ansehen) | Rhythmusambulanz | Vergleichen | nur Ansehen |
| 25 | Vorhofflimmern / -flattern (12-Kanal) | eigener Patient | VHF schmal: 96, 110, 173, 129, 88, 112; Flattern 35 (141/min), 52 (65/min), 103 (93/min) — ohne P-Marken | Rhythmusambulanz | Vergleichen, 6-s-Zählung | ok |
| 30 | Schrittmacher-EKG | eigener Patient | **74**, 34 (VVI, III°), 90, 111 (bipolar), 45 (AAI + VVI), 93 (biventrikulär) | Intensiv | Zirkel `qrs`, Spike finden | ok |
| 21, 22, 23, 27, 29, 32, 33 | Lungenembolie, Peri-/Myokarditis, Elektrolyte, Brugada, ARVD/C, Situs inversus, Kinder | — | 0 (LEHRPLAN §4) | Innere | Schema, als Schema beschriftet | **Lücke** |
| 34 | systematische Befundung, fünf Schritte | alle Aufnahmen | alle | Befundraum | Fünf-Schritte-Formular | ok |
| 35–38 | Rhythmus-Tricks, Technik, Artefakte, Fehler | Jonas (Muskelartefakt) | LUDB enthält keine Artefakt-Aufnahme; PTB-XL führt Artefakt-Felder (baseline_drift, static_noise, burst_noise, electrodes_problems) | Lehrsaal | Ansehen | **Lücke** (Export aus PTB-XL) |

**Lesart:** 15 Zeilen ok, 4 nur Ansehen, 1 dünn, 7 Lücken. Die größte Lücke ist nicht fachlich, sondern
technisch: **der Export enthält nur Ableitung II.** Mit allen zwölf Ableitungen aus LUDB (die Annotation
liegt dort je Ableitung vor) werden Lagetyp, Hemiblock, R-Progression und Hypertrophie messbar — vier
Zeilen auf einmal. Das ist der erste Datenauftrag in `UMBAU.md`.

---

## 6. Architektur für den Umbau (Bewertung des Vorschlags)

Der Koordinator schlägt vor: eine Datei je Fall mit Dialogdaten, Bedingungen und Texten mit festen IDs;
Übersetzungen über IDs statt über den deutschen Wortlaut; Motor-Code getrennt von Fällen.

**Bewertung: richtig, mit drei Konkretisierungen.**

1. **Eine Datei je Fall, aber als reines Datenobjekt.** `web/faelle/<id>.js` exportiert ein Objekt
   `{ id, lektionen, raum, patient, aufnahme: { haupt, ersatz: [...] }, marken: [...], befunde: {...},
   dialoge: { <figur>: { <knoten>: ... } }, aufgaben: [...] }`. Bedingungen stehen als kleine Ausdrücke in
   Strings (`"hat:ekg_geschrieben"`, `"befund:b-pq"`, `"nicht:befund:b-medis"`, `"alle:[...]"`), nicht als
   Funktionen — sie sind dann speicherbar, in `tools/durchlauf.mjs` aufzählbar und für Übersetzer lesbar.
   Nur berechnete Texte (Zahlen aus der Aufnahme) bleiben Vorlagen mit Platzhaltern (`{hf}`, `{pq}`), die
   der Motor aus `aufnahme.mess` oder aus der Messung der Spielerin füllt — nie aus Literalen.
2. **Texte über IDs.** `text/de/<fall>.json` ist die Quelle (`baum.marlene.fall.text`,
   `baum.frage.tia.warum`), `text/en/...` und `text/ru/...` tragen dieselben Schlüssel. `T(id, vars)`
   ersetzt `T(deutscherSatz)`. Übergang: `sprache.js` akzeptiert beides, bis die alten Sätze migriert sind;
   `tools/woerter.py` prüft, dass jeder Schlüssel in allen Sprachen existiert, und der Durchlauf schlägt
   fehl, wenn eine ID im Spiel ohne Text bleibt. Vorteil gegenüber dem Wortlaut-Schlüssel: Ein
   korrigiertes Komma im Deutschen bricht keine Übersetzung mehr, und Fall-Texte lassen sich fallweise
   prüfen.
3. **Motor getrennt.** `web/motor/` (szene, dialog, mappe, stand, zirkel, schirme, ampel, sprache, ekg)
   kennt keinen Patienten. Neu: `web/motor/fall.js` lädt Fallobjekte, registriert ihre Räume und
   Klickzonen, wertet Bedingungen aus und hält den Zustand je Fall (`Z.faelle[id]`). `spiel.js` schrumpft
   auf Start, Kopfleiste und Kapitelfolge. Ein neuer Fall ist dann eine Akte, eine Datendatei und drei
   Textdateien — kein Eingriff in den Motor.

Risiko: Überbau für drei Fälle. Gegenmittel: Herr Baum wird zuerst migriert (Referenzfall, prüft, ob das
Schema alles trägt, was `spiel.js` heute kann), der Lehrsaal als erster nativ gebauter Fall. Erst danach
Kapitel 2. Reihenfolge und Arbeitspakete: `UMBAU.md`.

---

## 7. Offene Entscheidungen für den Nutzer

| Frage | Empfehlung |
|---|---|
| Rotation über mehrere Dienste (§2) oder eine Schicht behalten? | Rotation. Nur sie macht Grundsatz 1 logisch. |
| Bekommt Herr Baum einen Epilog (Marlene erzählt am Dienst 3, was der Monitor-Speicher zeigte; optional ein PTB-XL-Standbild „AV-Block II°, Mobitz" mit `messbar: false`)? | Ja, als Erzählung ohne neues Lernziel — die Spielerin soll erfahren, was aus ihm wurde; ein Standbild nur, wenn es als „andere Aufnahme, gleiche Diagnose" beschriftet ist. |
| Lagetyp im Lehrsaal erst nach dem 12-Kanal-Export bauen oder vorläufig als Schema? | Export zuerst (ein Datenauftrag, deckt vier Lektionen). Kein Schema für Stoff, den die Daten hergeben. |
| Vorname und Alter der neuen Figuren (Dr. Nora Wieser 41, Jonas Prem 24, Frau Gerda Lindner 76) | Vorschlag übernehmen; LUDB-Alter/Geschlecht der Aufnahmen 142 und 96 vor dem Bau aus der Rohdatenbank nachtragen (im Export fehlt beides) und die Figuren daran anpassen. |
| Reizleitung bauen: in den Lehrsaal (Lektion 1) oder bei Marlene lassen? | Lehrsaal. Marlene behält den Fall, nicht den Unterricht. |
| Textschlüssel: Migration in einem Zug oder fallweise? | Fallweise, mit Übergangsfunktion (§6.2). |
