# Raum „Lehrsaal" — Einschulungstag, 08:10

Stand: 25.10.2026. Raumbeschreibung für den Bau in Blender nach `docs/ART_BIBLE.md` (§2 Farben, §3 Licht,
§5 Figuren, §7 Logik). Der Raum trägt die Lektionen 1–7 (`docs/faelle/lehrsaal.md`) und die Kurswoche aus
`docs/MECHANIK.md` §4; was hier steht, ist baubar, ohne die Fallakte gelesen zu haben.

**Neu am 25.10.2026 (Entscheid des Nutzers):** Der Lehrsaal ist kein Seminarraum für vier mehr, sondern ein Saal
**14,4 × 7 m im Westende des EG** von Haus Föhrenhang, gebaut als Ausbau in Hauskoordinaten
(`gen/blender/szene_lehrsaal.py`, Hülle aus `haus_blockout.py`; KRANKENHAUS „Ein Haus, aus Bausteinen"). Vorbild
war ein Foto des Nutzers: langer Saal, Fenster an einer Längsseite und an der Stirn, Tischreihen, Holzdecke. Daraus
übernommen: Fensterfront links, Stirnwand mit **Leinwand zwischen zwei Fenstern**, zwei Türen rechts, Lattendecke
mit Lichtbändern, zwei Ringleuchten, Stehleuchten, Vorhänge. Nicht übernommen: die roten Stühle (Rost gehört genau
einem Objekt), sie sind **Petrol**. Probe: `docs/haus/probe_lehrsaal.jpg`. §4, §5 und die Figurenplätze gelten
inhaltlich weiter; ihre Ebenen (`schirme.json`, `hitboxes.json`) entstehen, sobald Hausräume durch die
Ebenen-Pipeline laufen (bis dahin bleiben die alten Ebenen in `art/szenen/lehrsaal/`, `ebenen.py lehrsaal` läuft
nicht mehr).

## 1. Zweck

Der EKG-Kurs der Fakultät, ein Lehrsaal mit 30 Plätzen und einer Untersuchungsliege vorn. Hier lernt die Spielerin, bevor sie
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
| **Projektionsfläche** (Leinwand, 2,4 × 1,5 m, Unterkante 1,0 m) an der Stirnwand zwischen den Giebelfenstern | dem Saal | der Code zeichnet darauf: das 12-Kanal-Blatt, einzelne Ableitungen groß, Millimeterpapier mit Eichzacke, Cabrera-Kreis | Hintergrund (Schirmfläche `projektion`) |
| **Beamer** an der Decke (kleiner Kasten, Linse zur Leinwand) | dem Saal | sichtbare Lichtquelle (§3.2) für die Projektion | Hintergrund |
| **Whiteboard** (2,0 × 1,2 m, Unterkante 0,9 m), leer, Marker in der Ablage, ein Schwamm | Dr. Wieser | sie zeichnet darauf — aber nur im Code (SVG), **keine Schrift im Bild** | Hintergrund |
| **Dozententisch** (Holz, 1,6 × 0,75 m, rechts vor der Leinwand) mit der **Schachtel Lineale** (Papier-Karton, offen, blaue Lineale darin), einem Zirkel, einem Stapel leerer EKG-Blätter | Dr. Wieser | Werkzeuge der Lektionen 3, 4, 7; die Schachtel ist die Klickzone für „Lineal nehmen" | Mittelgrund |
| **Tischreihen**: fünf Reihen zu zwei Klapptischen (Holz, 1,8 × 0,5 m, T-Gestell Tinte), je drei Stühle (Petrol-Polster, Tinte-Gestell), Mittelgang; auf manchen Plätzen Block und Stift, Wasserflaschen, Jacken über Lehnen, Taschen | dem Kurs, die Kleinigkeiten den Mitstudierenden | der Kurs ist voll (Kurswoche, Abstimmung, Mitstudentin, MECHANIK §4); ein freier Platz ist der der Spielerin | Mittelgrund |
| **Lattendecke** (Holz, Latten 0,6 m längs des Saals), Lichtbänder quer, zwei Ringleuchten, Stehleuchten zwischen den Fenstern (alle aus) | dem Haus | Altbau, neu ausgebaut; die Latten führen den Blick zur Leinwand | Hintergrund |
| **Vorhänge** (Mint, gerafft) an jeder Fenstergruppe, Pflanzen auf drei Fensterbänken | dem Haus, die Pflanzen dem Sekretariat | Ruhe, Leben im Raum (die Vorlagen des Nutzers: Fenster und Kleinigkeiten tragen die Stimmung) | Hintergrund |
| **Stuhl neben der Liege** mit Dr. Wiesers Stethoskop über der Lehne und ihrer Jacke | Dr. Wieser | zeigt, dass sie nicht sitzt | Mittelgrund |
| **Wanduhr** (rund, Zeiger als SVG aus `hitboxes.json`, Zone `uhr`) | dem Haus | Spielzeit; Ebene Hintergrund wie überall (§7.3) | Hintergrund |
| **Fenster**: links vier Achsen zur Südostseite (zwei Paare in der Nische, zwei einzelne), vorn zwei Giebelfenster | dem Haus | Lichtquelle (Morgensonne von links), draußen Park und Hof im Spätherbst | Hintergrund |
| **Kleiderhaken** an der Rückwand mit einem Kapuzenpulli (noch nicht gebaut, hinter der Kamera) | der Spielfigur | ihr Kapuzenpulli unter dem Kittel (ART_BIBLE §5) hängt hier, weil sie heute den Kittel bekommen hat | – |
| **Zwei Türen** rechts in den Flur (vorn x 3,9 für die Lehrenden, hinten x 9,8), Holzzarge | dem Haus | Ausgang; Zone `ausgang` an der hinteren Tür; freier Boden davor (§7.1) | Hintergrund |

Nicht im Raum: Monitore an der Wand, Infusionsständer, Betten — alles, was „medizinisch aussieht" und
hier niemandem gehört (§2, Regel 4). Kein Poster mit EKG-Kurve (Text und Kurven sind verboten im Bild).

## 4. Flächen, auf die der Code zeichnet (`schirme.json`)

| Name | Ebene | Größe im Raum | Inhalt aus dem Code |
|---|---|---|---|
| `projektion` | hintergrund | 2,4 × 1,5 m, frontal zur Kamera, exaktes Rechteck im Bild (wie der große Schirm im Monitorzimmer: Rückwand bei y = 0, keine Kameraneigung) | Millimeterpapier `#FFF8F4` mit Eichzacke; je nach Aufgabe: eine Ableitung groß (50 mm/s), das 12-Kanal-Blatt, der Cabrera-Kreis, die Wellen-Markierungen. Standbild oder laufend, je Aufgabe. Dies ist der Hauptschirm des Raums. |
| `wagen_schirm` | mittelgrund | wie `wagen_schirm` in der Aufnahme | laufende Ableitung II des Freiwilligen (Monitorstil Phosphor), Frequenz aus den Daten |
| `whiteboard` | hintergrund | 1,2 × 1,1 m an der Flurwand, schräg im Bild (vier Ecken in `schirme.json`) | nur SVG-Zeichnungen aus dem Code (Einthoven-Dreieck, Herzschema aus `gen/kunst.py`); im Render leer |

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
| `ausgang` | zur Aufnahme — frei erst, wenn die Pflichtaufgaben der Lektionen 1–7 gezeigt sind (Fallakte) | Pfeil am rechten Bildrand (die Türen liegen außerhalb des Bilds) |

Zonen überlappen nicht (§7.6): `jonas` und `liege` getrennt wie `herrk` und `tuete` in der Aufnahme
(`getrennt` in `aufbau()`).

## 6. Tageszeit, Licht, Farben

- **Einschulungstag und Kurswoche, 08:10, Spätherbst** (ART_BIBLE §4). Sonne Anfang November bei 47° N: Azimut 126°,
  Höhe 9°. Sie steht fast senkrecht vor der Südostfront: **lange Lichtbahnen von links** über Tische, Stuhllehnen und
  die Flurwand (dort als Fensterbilder bis gut 2 m Höhe). Deckenleuchten aus, Beamer an. Die Giebelfenster (Südwest)
  bekommen keine Sonne: vorn kühles Licht, links warmes, wie in den Vorlagen des Nutzers.
- **Farben „Morgen"** (eigenes Design dieses Raums, vom Nutzer am 25.10.2026 aus drei Proben gewählt; Vorlagen:
  Lofi-Zimmer im Morgenlicht, Ligne claire, Foto des Saals; ART_BIBLE §2 nur als Ausgangspunkt). Im Skript `PALETTE`,
  Namen `ls_…`; die Stimmung macht das Licht an der Kamera: **Sonne Pfirsich** `#FFD9A3` (Anteil 0,6), **alles ohne
  Sonne ein Viertel zum kühlen Blau** `#6F7FB0` (`schattenfarbe`, `schatten` 0,24) statt nur dunkler.

| Wand | Sockel | Boden | Decke | Möbel | Akzente |
|---|---|---|---|---|---|
| warmes Papier `#F6E8CF` | Salbei `#A8C2B4` (bis 0,8 m, unter der Brüstung, Holzleiste) | Parkett Honig-Eiche `#C99260` | Holzlatten `#A9774E`, dunkler als der Boden (rahmt das Bild oben) | Tische helles Holz `#D2A673`, Stühle Petrol `#2E5E6B`, Gestelle Tinte, Liege mit Salbei-Bezug | Vorhänge Pfirsich `#EBC3A6`, Lampenschirme und Töpfe Terrakotta `#C2683F`, Pflanzen Tannengrün `#2F5A45`, Jacken Oliv `#8E9F6B` und Koralle `#E39A86`, Taschen Blau `#3F5F8C` und Pflaume `#7A4E6E` |

  Erste Fassung (bis 25.10.2026): Papier, Mint, Linoleum `#C9BDA2`, Schatten nur dunkler Richtung Petrol — dem Nutzer
  zu blass. Rot bleibt der Elektrodenklemme am rechten Arm des Freiwilligen (Figur); Terrakotta an Lampen und Töpfen ist
  bewusst wärmer und matter.

  Draußen: der echte Blick aus dem Haus (Park, Linden im Herbstlaub), flach und ohne Linie; Scheiben und Gardinen
  sind im Innenrender aus. Später als Fensterblick-Tafel (KRANKENHAUS „Bausteine" Punkt 4). Leinwand `#FFF8F4` (wie
  EKG-Papier, die Kurve kommt aus dem Code). Kobaltblau nur an Dr. Wieser und in der Linealschachtel; Senfgelb nur
  an Jonas (deshalb Jacken Oliv, nicht Senf); Pflanzen Tannengrün (Laub ist nur außen). Himmel `#9EC3E0` → `#F2D2B0`
  (Blau oben, Pfirsich am Horizont), sichtbar erst mit der Fensterblick-Tafel.

## 7. Kamera und Ebenen

- **Die Spielerin sitzt an der ersten Bank** (Wunsch des Nutzers, 25.10.2026), Gangplatz im linken Block: Kamera
  (5,75 / 2,85 / 1,25), Blick frontal zur Stirnwand (`gier` 180), Ziel (0,45 / 3,3 / 0,4), 18 mm, Bild 1600 × 900,
  Objektivverschiebung statt Drehung (die Leinwand bleibt ein exaktes Rechteck). Im Bild: Leinwand mit Uhr darüber in
  der Mitte, links Liege und Wagen vor dem linken Giebelfenster, rechts Dozententisch, am rechten Bildrand das Whiteboard an der Flurwand, unten
  die eigene Bank mit den Werkzeugen der Spielerin (Block mit Bleistift, EKG-Streifen quer, Zirkel offen; Wunsch des
  Nutzers: „dort liegen die nötigen Instrumente"). Das Lineal kommt erst aus der Schachtel (`lineale`). Die Türen liegen rechts außerhalb: `ausgang` ist ein Pfeil am rechten Bildrand.
  Render: `python3 gen/blender/haus_blockout.py render lehrsaal`. Der frühere Blick von hinten längs des Saals (14,05 /
  3,6 / 1,55, 24 mm) zeigte den ganzen Raum, aber Liege, Whiteboard und Uhr nur klein; dafür sind die Tischreihen
  gebaut, der Saal ist derselbe.
- **Kein angeschnittener dunkler Vordergrund** (§3.3): deshalb kein Stuhl der Dozentin (sie steht) und kein dunkler
  Tritt an der Liege; die eigene Bank ist hell (Holz, Papier) und trägt nur die Werkzeuge.
- **Ebenen** (§3.4): Hintergrund (Hülle, Fenster, Decke, Leinwand, Whiteboard, Uhr, Türen, Vorhänge, Beamer);
  Mittelgrund (Liege, Wagen, Tische, Stühle, Schachtel); Figuren (Dr. Wieser, Jonas, Mitstudierende,
  Spielerinnenschatten). Die Trennung kommt mit der Ebenen-Pipeline für Hausräume.
- **Bewegung** (§7.5): Dr. Wieser atmet und dreht alle paar Sekunden das Lineal (zwei Posen, Wechsel per CSS);
  Jonas atmet sichtbar (Brustkorb); die Kurve auf dem Wagenschirm läuft; die Lichtbahnen wandern nicht.

## 8. Maße (ART_BIBLE §7.4)

Hauskoordinaten (KRANKENHAUS §2), Werte in `gen/blender/szene_lehrsaal.py` oben.

| Ding | Maß |
|---|---|
| Raum | x 0 … 14,4, y 0 … 7 (EG, Achsen 1–4), dazu Nische des Eckrisalits x 0 … 7,2, y −1 … 0; lichte Flächen: Stirn x 0,45, Fenster y −0,55 (Nische) bzw. 0,45, Flur y 6,925, Rückwand x 14,325; Höhe 3,4 |
| Fenster | Südost: Paare x 0,65 … 1,65 / 1,95 … 2,95 und 4,25 … 5,25 / 5,55 … 6,55 (Nische), einzeln x 8,3 … 9,7 und 11,9 … 13,3; Giebel y 0,4 … 1,8 und 4,6 … 6,0; alle z 0,9 … 3,1 |
| Türen | Flurwand y 7, Mitte x 3,9 und x 9,8, je 1,0 × 2,1 |
| Leinwand | 2,4 × 1,5 m, Mitte y 3,2, Unterkante z 1,0, an der Stirnwand |
| Whiteboard | Flurwand ganz vorn im Eck (Wunsch des Nutzers), x 0,55 … 1,75, z 0,95 … 2,05; von der ersten Bank schräg am rechten Bildrand. Wanduhr Ø 0,42 über der Leinwand, Mitte z 2,97 |
| Dozententisch | 1,2 × 0,6 m (Pult, vom Nutzer verkleinert), Mitte (2,1 / 4,9), quer zum Saal |
| Liege | 1,95 × 0,65 m, quer vor dem linken Giebelfenster: x 0,85 … 1,5, y 0,35 … 2,3, Liegefläche 0,75 m (unter der Brüstung), Kopfteil 0,5 m um 20° hochgestellt mit Kissen (liest sich als Liege), Kopfende zur Fensterwand, Füße zur Leinwand, kein Tritt, kein Hocker, keine Papierrolle (die Ecke wirkte voll, Nutzer 25.10.2026); der Freiwillige zeigt der Klasse seine rechte Seite |
| EKG-Wagen | Mitte (1,9 / 0,02), schräg vor dem Kopfende, im Bild mit Abstand links der Liege; Schirm 0,36 × 0,24 um 38° zur ersten Bank gedreht |
| Tischreihen | Tischmitten x 5,0 / 6,2 / 7,4 / 8,6 / 9,8; Blöcke y 1,35 … 3,15 und 4,05 … 5,85; Tisch 0,5 tief, 0,74 hoch; Stühle 0,55 hinter der Tischmitte |
| Decke | Latten z 3,31 … 3,36, Lichtbänder darunter, Ringleuchten Ø 1,1 m auf z 2,75 bei x 7,8 |
| Figuren | Dr. Wieser 1,72 m, Jonas 1,80 m liegend (Kopf zur Fensterwand); Plätze werden mit der Ebenen-Pipeline neu gesetzt (Vorschlag: Wieser zwischen Liege und Leinwand auf dem freien Boden, nicht vor der Leinwand) |

Alles steht auf dem Boden, Wege frei: Fenstergang 0,9 m, Mittelgang 0,9 m, Flurgang 1,1 m; vorn 2,6 m zwischen
Leinwand und erster Reihe.

## 9. Was dieser Raum nicht braucht

Keine Pinnwand mit Zetteln (Text im Bild), keine Patientenakte, keine zweite Liege, kein Monitor an der
Wand. Keine Requisite, die eine Kardiologin nicht zur Entscheidung bräuchte (§2, Regel 4) — die
Entscheidung hier heißt: messen oder schätzen.
