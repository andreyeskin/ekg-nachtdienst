# Raum „Lehrsaal" — Einschulungstag, 08:10

Stand: 11.10.2026. Raumbeschreibung für den Bau in Blender (`gen/blender/szene_lehrsaal.py`) nach
`docs/ART_BIBLE.md` (§2 Farben, §3 Licht, §5 Figuren, §7 Logik). Der Raum trägt die Lektionen 1–7
(`docs/faelle/lehrsaal.md`); was hier steht, ist baubar, ohne die Fallakte gelesen zu haben.

## 1. Zweck

Der EKG-Kurs der Fakultät, ein Seminarraum mit Untersuchungsliege. Hier lernt die Spielerin, bevor sie
einen Patienten sieht: Papier und Eichzacke, die zwölf Ableitungen und wo die Elektroden hingehören,
die Zacken und ihre Namen, Messen mit Zirkel und Lineal, Lagetyp, Rhythmus und Frequenz. Es gibt keinen
Kranken in diesem Raum. Auf der Liege liegt ein Kommilitone mit einem normalen EKG; alles Pathologische
kommt später, auf Station.

Zeitrahmen (Entscheidung in `docs/KONZEPT.md` §2): Das Spiel ist eine **Rotation** über mehrere
Dienste. Der Lehrsaal ist der **Einschulungstag** vor dem ersten Dienst, Vormittag, 08:10. Danach erst
beginnt der Frühdienst in der Aufnahme (06:40, nächster Tag).

## 2. Wer da ist

### Dr. Nora Wieser, 41 — Internistin, hält den EKG-Kurs seit acht Jahren

„Erklärt nie zwei Dinge auf einmal und keines länger als zwei Sätze."

Die fünf Punkte (ART_BIBLE §5):

1. **Silhouette**: schmal, immer halb gedreht, ein Fuß auf dem Tritt der Liege; der Oberkörper zeigt zur
   Projektionsfläche, der Kopf zur Spielerin. Daumennagelgroß: ein schräger Strich mit Fußstütze.
2. **Formfamilie**: schmale Ovale (Kopf, Rumpf, Ärmel), Gegenakzent ein harter Winkel — der Ellbogen des
   Arms, der das Lineal hält.
3. **Gegenstand**: ein **kurzes EKG-Lineal aus blauem Kunststoff** (Kardiometer), das sie zwischen zwei
   Fingern dreht und mit dem sie zweimal auf die Tischkante klopft, bevor sie etwas Wichtiges sagt. Eine
   **Schachtel mit zwanzig gleichen Linealen** steht auf dem Seminartisch; eines davon bekommt die
   Spielerin — und hat es später in der Kitteltasche (ART_BIBLE §5, Spielfigur: „das EKG-Lineal aus dem
   Kurs").
4. **Akzentfarbe**: **Kobaltblau** `#2F5DA8` (Lineal, Sneaker). Kommt in keinem Raum sonst vor.
5. **Haltung**: nie sitzend, nie frontal; mitten in der Bewegung zwischen Liege und Projektionsfläche.

Details: kurzes graues Haar mit einer dunklen Strähne, Kittel offen über einem dunklen Rollkragen, keine
Brille, Stethoskop nicht umgehängt, sondern über der Stuhllehne (sie braucht es hier nicht). Ausdrücke
(drei bis vier): neutral-wach; Brauen hoch („und?"); schmales Lächeln; Lippen zusammengepresst beim Messen.
Porträt (Brustbild) nach demselben Weg wie die anderen (`gen/blender/figuren_zeichnen.py`), Stilphrase
`stil/portrait_wieser.txt`.

**Stimmprofil** (Skill `dialoge`, §4 — verbindlich, bevor sie spricht):

| Figur | Satzbau | Wörter | Nie | Tic / Gegenstand |
|---|---|---|---|---|
| **Dr. Wieser** (Lehrperson, 41) | kurz, oft Doppelpunkt-Bau („Erst das Papier: welche Geschwindigkeit?"); gibt Fragen zurück („Und woran siehst du das?"); zählt Kriterien an den Fingern | duzt Studierende, Alltagsbilder (Kabel, Bremse, Taktgeber), sagt „noch nicht" statt „falsch" | Vortrag länger als zwei Sätze; Zahlen aus dem Kopf — sie misst vor allen; Lob ohne Frage danach; Fachbegriff ohne das Bild dazu | blaues Lineal, klopft zweimal, bevor es wichtig wird |

Was sie will und nicht sagt: dass die Spielerin **ohne sie** messen kann, bevor der erste Dienst
beginnt. Deshalb gibt sie Fragen zurück, statt zu antworten, und deshalb verteilt sie Lineale.

### Jonas Prem, 24 — Medizinstudent, Tutor im Kurs, liegt auf der Liege

„Legt sich jedes Semester hin, weil sein EKG langweilig ist. Das ist sein Stolz."

1. **Silhouette**: liegend, lang, ein Knie leicht angezogen, ein Arm hinter dem Kopf — bis Dr. Wieser
   ihn bittet, still zu liegen (Muskelartefakte, Lektion 37: dann beide Arme neben dem Körper).
2. **Formfamilie**: lange Rechtecke, Gegenakzent runder Kopf mit Kopfhörern.
3. **Gegenstand**: **Kopfhörer um den Hals**, Kabel in der Hosentasche; er muss sie zum EKG abnehmen.
4. **Akzentfarbe**: **Senfgelb** `#D9A441` (Socken; die Schuhe stehen unter der Liege).
5. **Haltung**: entspannt liegend, redet mit der Decke; T-Shirt hochgeschoben, Elektroden an Armen und
   Beinen schon geklebt, Brustwandelektroden noch nicht (das ist eine Aufgabe).

Stimmprofil: Patient-Zeile aus `dialoge` §4, aber kein Kranker — er redet wie ein Tutor, der die Antworten
kennt und sie nicht sagt („Das darf ich dir nicht verraten, ich bin heute Patient."). Sagt nie einen
Fachbegriff, solange er auf der Liege liegt; das ist sein Spiel.

### Die Spielfigur

Wie überall nur Hände, Schatten, Spiegelbild (ART_BIBLE §5). Hier zum ersten Mal mit dem Lineal in der
Hand — die Schachtel ist der Ursprung.

## 3. Gegenstände — jeder mit Besitzer und Grund (ART_BIBLE §7.2)

| Gegenstand | Wem er gehört | Warum er da ist | Ebene |
|---|---|---|---|
| **Untersuchungsliege** mit Papierrolle, Tritt, Mint-Bezug | dem Kurs | Jonas liegt darauf; Elektroden kleben, EKG schreiben | Mittelgrund |
| **EKG-Wagen** (gleiches Bauteil wie in der Aufnahme: Gehäuse Petrol, Schirm Tinte, Papierfach, Kabelbaum mit zehn Elektrodenkabeln, Saugelektroden-Satz) | der Fakultät | das eine Gerät, an dem gemessen wird; sein Schirm zeigt die laufende Ableitung II | Mittelgrund |
| **Elektrodenkabel** am Wagen: vier Extremitätenklemmen — rot, gelb, grün, schwarz — und sechs Brustwand-Saugelektroden | zum Wagen | Lektion 2, Ampel-Regel; **die rote Klemme ist das Rost-Objekt des Raums** (`#B5552D`), weil sie die erste Aufgabe anstößt (rechter Arm) | Mittelgrund |
| **Projektionsfläche** (Leinwand, 2,4 × 1,5 m, Unterkante 1,10 m) an der Rückwand | dem Seminarraum | der Code zeichnet darauf: das 12-Kanal-Blatt, einzelne Ableitungen groß, Millimeterpapier mit Eichzacke, Cabrera-Kreis | Hintergrund (Schirmfläche `projektion`) |
| **Beamer** an der Decke (kleiner Kasten, Linse zur Leinwand) | dem Seminarraum | sichtbare Lichtquelle (§3.2) für die Projektion | Hintergrund |
| **Whiteboard** (2,0 × 1,2 m, Unterkante 0,9 m), leer, Marker in der Ablage, ein Schwamm | Dr. Wieser | sie zeichnet darauf — aber nur im Code (SVG), **keine Schrift im Bild** | Hintergrund |
| **Seminartisch** (Holz, 1,8 × 0,8 m, 0,75 m hoch) mit der **Schachtel Lineale** (Papier-Karton, offen, blaue Lineale darin), einem Zirkel, einem Stapel leerer EKG-Blätter | Dr. Wieser | Werkzeuge der Lektionen 3, 4, 7; die Schachtel ist die Klickzone für „Lineal nehmen" | Mittelgrund |
| **Vier Stühle** (Petrol-Polster, Tinte-Gestell) an der Tischseite zur Kamera, einer herausgezogen | dem Kurs | der Platz der Spielerin; der herausgezogene Stuhl ist ihr Schatten im Bild | Mittelgrund |
| **Stuhl neben der Liege** mit Dr. Wiesers Stethoskop über der Lehne und ihrer Jacke | Dr. Wieser | zeigt, dass sie nicht sitzt | Mittelgrund |
| **Wanduhr** (rund, Zeiger als SVG aus `hitboxes.json`, Zone `uhr`) | dem Haus | Spielzeit; Ebene Hintergrund wie überall (§7.3) | Hintergrund |
| **Fenster** (zwei hohe Flügel, Jalousie halb oben) rechts | dem Haus | Lichtquelle; draußen Hofseite, Vormittag | Hintergrund |
| **Kleiderhaken** an der Tür mit einem Kapuzenpulli | der Spielfigur | ihr Kapuzenpulli unter dem Kittel (ART_BIBLE §5) hängt hier, weil sie heute den Kittel bekommen hat | Hintergrund |
| **Tür** links, offen in den Flur | dem Haus | Ausgang; Zone `ausgang`; freier Boden davor (§7.1) | Hintergrund |

Nicht im Raum: Monitore an der Wand, Infusionsständer, Betten — alles, was „medizinisch aussieht" und
hier niemandem gehört (§2, Regel 4). Kein Poster mit EKG-Kurve (Text und Kurven sind verboten im Bild).

## 4. Flächen, auf die der Code zeichnet (`schirme.json`)

| Name | Ebene | Größe im Raum | Inhalt aus dem Code |
|---|---|---|---|
| `projektion` | hintergrund | 2,4 × 1,5 m, frontal zur Kamera, exaktes Rechteck im Bild (wie der große Schirm im Monitorzimmer: Rückwand bei y = 0, keine Kameraneigung) | Millimeterpapier `#FFF8F4` mit Eichzacke; je nach Aufgabe: eine Ableitung groß (50 mm/s), das 12-Kanal-Blatt, der Cabrera-Kreis, die Wellen-Markierungen. Standbild oder laufend, je Aufgabe. Dies ist der Hauptschirm des Raums. |
| `wagen_schirm` | mittelgrund | wie `wagen_schirm` in der Aufnahme | laufende Ableitung II des Freiwilligen (Monitorstil Phosphor), Frequenz aus den Daten |
| `whiteboard` | hintergrund | 2,0 × 1,2 m | nur SVG-Zeichnungen aus dem Code (Einthoven-Dreieck, Herzschema aus `gen/kunst.py`); im Render leer |

Alle Kurven kommen aus `data/ekg_daten.json` (ART_BIBLE §6): der Freiwillige ist LUDB-Aufnahme **142**
(Sinusrhythmus ohne Nebendiagnose, 74/min, PQ 130 ms, QRS 84 ms, QT 356 ms); Ersatz für den
Wiederspielwert: 198, 149. Nur **Ableitung II** liegt im Export — für die 12-Kanal-Projektion und den
Lagetyp (Lektion 5/6) muss `gen/export_spiel.py` die übrigen Ableitungen nachliefern (Datenlücke,
siehe `docs/UMBAU.md` §5). Bis dahin zeigt die Projektion nur Ableitung II und sagt das.

## 5. Klickzonen (`hitboxes.json`)

| Zone | Was passiert | Mindestgröße |
|---|---|---|
| `wieser` | Gespräch (Einstieg jeder Aufgabe) | Figur, ≥ 44 CSS-px |
| `jonas` | Gespräch; „still liegen" für das Artefakt-Beispiel | Figur |
| `liege` (ohne Figur) | Elektroden-Aufgabe (Lektion 2): Klemmen und Saugelektroden setzen | ganze Liegefläche |
| `wagen` | EKG schreiben, danach Streifen; Zirkel-Aufgaben | Gehäuse |
| `projektion` | öffnet die große Ansicht (Papier, Ableitungen, Lagetyp, Zacken benennen) | Leinwand |
| `whiteboard` | Herzschema / Einthoven-Dreieck (Rätsel „Reizleitung bauen" wandert hierher) | Tafel |
| `lineale` | Lineal nehmen (einmalig; danach „erledigt") | Schachtel |
| `uhr` | Uhrzeit-Meldung | Zifferblatt |
| `ausgang` | zur Aufnahme — frei erst, wenn die Pflichtaufgaben der Lektionen 1–7 gezeigt sind (Fallakte) | Tür |

Zonen überlappen nicht (§7.6): `jonas` und `liege` getrennt wie `herrk` und `tuete` in der Aufnahme
(`getrennt` in `aufbau()`).

## 6. Tageszeit, Licht, Farben

- **Einschulungstag, 08:10, Vormittag.** Neues Blatt in ART_BIBLE §4 (Rotation): die Tabelle bekommt die
  Zeile „0 Lehrsaal · Einschulungstag 08:10 · Vormittag, neutrales Tageslicht, Beamer an".
- **Licht**: Tageslicht von rechts durch die hohen Fenster (hart, als zwei helle Parallelogramme auf
  Boden und Liege — die Lichtinsel liegt auf Jonas und dem Wagen); Beamerkegel schwach von der Decke auf
  die Leinwand; Deckenleuchten aus (es ist hell genug). Keine langen Morgenschatten wie in der Aufnahme —
  die Sonne steht schon höher; Schatten kurz.
- **Farben** (ART_BIBLE §2, eigene Verteilung je Raum):

| Wand | Sockel | Boden | Möbel | Rost (das eine Objekt) |
|---|---|---|---|---|
| Papier `#F7F1E4` | Mint `#BFD9CF` (bis 0,95 m, Holzleiste) | Linoleum warm `#C9BDA2` | Holz-Tisch, Petrol-Stühle und -Wagen, Liege mit Mint-Bezug, Gestelle Tinte | **rote Elektrodenklemme** am rechten Arm des Freiwilligen |

  Himmel draußen: flache Bänder `#EAF1F0` → `#DCE9EA`, Hofbaum in Petrol/Papier-Silhouette. Leinwand
  `#FFF8F4` (wie EKG-Papier, die Kurve kommt aus dem Code). Kobaltblau nur an Dr. Wieser und in der
  Linealschachtel; Senfgelb nur an Jonas.

## 7. Kamera und Ebenen

- **Dreiviertelansicht**: Kamera rechts der Mitte (wie Monitorzimmer), Blick entlang +y ohne Neigung,
  Objektivverschiebung statt Kippung — so bleibt die Rückwand frontal und die Projektionsfläche ein
  exaktes Rechteck, auf das der Code zeichnet. Vorschlag: Kamera (0,9 / −7,6 / 1,55), Brennweite 28 mm,
  Sensor 36 mm horizontal, Bild 1600 × 900. Tiefe aus Liege und Tisch, die schräg zur Rückwand stehen
  (Liege 20° gedreht, Kopfende zur Rückwand).
- **Kein angeschnittener dunkler Vordergrund** (§3.3). Der herausgezogene Stuhl bleibt ganz im Bild,
  hell, unten rechts, nicht angeschnitten.
- **Drei Ebenen** (§3.4): Hintergrund (Raumhülle, Fenster, Leinwand, Whiteboard, Uhr, Tür, Beamer);
  Mittelgrund (Liege, Wagen, Tisch, Stühle, Schachtel); Figuren (Dr. Wieser, Jonas, Spielerinnenschatten).
  Der Mittelgrund nimmt nur seine eigenen Linien mit (`linesmid`).
- **Bewegung** (§7.5): Dr. Wieser atmet und dreht alle paar Sekunden das Lineal (zwei Posen, Wechsel
  per CSS); Jonas atmet sichtbar (Brustkorb); die Kurve auf dem Wagenschirm läuft; Jalousieschatten
  wandern nicht (eine Stunde ist zu kurz).

## 8. Maße (ART_BIBLE §7.4)

| Ding | Maß |
|---|---|
| Raumhülle | X0 = −5,4 m, X1 = 4,4 m, Höhe 3,4 m, Tiefe 7,0 m (Rückwand y = 0, nichts hinter der Kamera) |
| Tür | 0,95 × 2,10 m, links (x ≈ −4,9 … −3,95), Zarge Holz |
| Fenster | zwei Flügel, x ≈ 1,6 … 4,0, z 1,0 … 2,9 (hohe Seminarfenster) |
| Leinwand | 2,4 × 1,5 m, Mitte x = −1,2, Unterkante z = 1,10 |
| Whiteboard | 2,0 × 1,2 m, Mitte x = 2,6 (rechts neben der Leinwand, links vom Fenster: x 1,6 … 3,6 geht nicht — Whiteboard deshalb an die rechte Seitenwand, y 1,0 … 3,0, Unterkante 0,9 m) |
| Liege | 1,95 × 0,65 m, Liegefläche 0,75 m hoch, Tritt 0,25 m; Position Mitte (0,6 / 2,4), 20° gedreht, Kopfende zur Rückwand |
| EKG-Wagen | 0,55 × 0,5 m Grundfläche, Arbeitsfläche 0,95 m, Schirm 0,9 … 1,2 m; neben der Liege am Fußende, Schirm zur Kamera |
| Seminartisch | 1,8 × 0,8 m, 0,75 m hoch, Mitte (−2,6 / 3,2), parallel zur Rückwand |
| Stühle | Sitz 0,47 m, Lehne 0,9 m; vier Stück, einer um 0,4 m herausgezogen |
| Wanduhr | Ø 0,32 m, Mitte z = 2,6, x = −3,6 (über der Tür-Seite, Hintergrund) |
| Figuren | Dr. Wieser 1,72 m, stehend zwischen Liege und Leinwand, Fuß auf dem Tritt: `PLATZ["wieser"] = dict(ort=(−0,4, 1,6, 0), drehung=35, haltung="tritt")`; Jonas 1,80 m liegend: `PLATZ["jonas"] = dict(ort=(0,6, 2,4, 0,75), drehung=20, haltung="liegen")` |

Alles steht auf dem Boden (Füße auf der Bodenlinie), Wege frei: zwischen Tür und Liege 1,2 m Gang,
zwischen Tisch und Liege 1,0 m.

## 9. Was dieser Raum nicht braucht

Keine Pinnwand mit Zetteln (Text im Bild), keine Patientenakte, keine zweite Liege, kein Monitor an der
Wand. Keine Requisite, die eine Kardiologin nicht zur Entscheidung bräuchte (§2, Regel 4) — die
Entscheidung hier heißt: messen oder schätzen.
