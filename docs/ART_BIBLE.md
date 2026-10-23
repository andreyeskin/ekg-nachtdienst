# Art Bible — „Nachtdienst" (Arbeitstitel)

Stand: 10.10.2026. Dieses Dokument ist die verbindliche Regel für jedes Bild im Spiel.
Wenn ein Bild gegen eine Regel hier verstößt, wird es neu gemacht — nicht die Regel geändert.

## 1. Stilentscheid

**Gewählt (10.10.2026, nach Stilrecherche): Ligne claire.** Flache Lokalfarben, eine
gleichmäßig dünne Tuschelinie, keine Schraffur, kein Raster. Licht nur als harte, geometrische
Formen (Sonnenstreifen durch die Jalousie, Lampenkegel). Hell, klar, ruhig — der Raum ist Kulisse,
der EKG-Streifen ist das einzige Objekt mit feiner Zeichnung.

Warum dieser und kein anderer:
- Die Recherche (docs/stil-recherche-2026-10-10.md im Projekt-Repository) zeigt: Spiele, in denen
  Dokumente gelesen werden, halten die Welt ruhig und niedrigfrequent und den Beleg scharf.
  Ligne claire ist genau das: große glatte Flächen, eine Linie, nichts flimmert.
- Er lässt sich vollständig aus Code erzeugen (Blender → Flächen, Freestyle-Linie, Sonnenpass),
  bleibt deshalb über alle Räume gleich und kostet Sekunden statt Stunden.
- Er ist erwachsen (europäischer Comic, Moebius, Sable, Rollerdrome), nicht „Toon".

Verworfen: Risograph-/Gouache-/Noir-Studien aus dem Bildgenerator (sehen generiert aus, sechs
Bilder = sechs Stile), der flache Code-SVG-Look (Figuren ohne Gesicht, Krankenhaus-Mint) und
pastelliges Low-Poly (Blender-Trend, wirkt wie Vorlage).

Pipeline: `gen/blender/` (siehe README dort). Ergebnis je Raum: `art/szenen/<raum>/` mit
`hintergrund.png`, `mittelgrund.png`, `hitboxes.json` — `gen/kunst.py` bettet sie ein.

Nebenrollen: Isometrie nur für den Stationsplan; dunkler Monitor-Look (Grün auf Schwarz) nur als
Bildschirm-Inhalt, nie als Raum.

## 2. Farben

| Rolle | Farbe | Einsatz |
|---|---|---|
| Sand | `#EFE6D3` | Wände, Grundfläche |
| Papier | `#F7F1E4` | Tische, Rahmen, Zettel |
| Mint | `#BFD9CF` | zweite Fläche (Wandpaneel, Vorhänge, Bezüge) |
| Petrol | `#2C5560` | Möbel, Geräte — die dunkle Form |
| Tinte | `#1E2A30` | **die Linie**; nie reines Schwarz (das gehört der EKG-Kurve) |
| Holz | `#C99A5B` | Tresen, Rahmen, Armlehnen |
| Rost | `#B5552D` | **genau ein Objekt pro Bild** — das, was die Geschichte weitertreibt |
| Morgenlicht | `#F8E7BF` | Fenster, Sonnenstreifen; je Tageszeit abgewandelt |
| Phosphor | `#39E58C` | ausschließlich Bildschirme und Monitorkurven |
| Linoleum | `#C9BDA2` warm · `#B6BFB6` kühl | Böden: eine Stufe dunkler als die Wand, erdet den Raum (§3.1) |
| Mint hell | `#D6E4DD` | Wände des kühlen Raums (Monitorzimmer) — Mint als Fläche, nicht als Sockel |
| Glas | `#1E2A30` | Geräteschirme (EKG-Wagen, Bettmonitore): Tinte als Fläche, die Kurve kommt aus dem Code |
| Ziegel | `#C9795A` | nur außen: Dachziegel des Hauses (Entscheid des Nutzers 19.10.2026); gedeckter als Rost, zählt nicht als „das eine Objekt" |
| Wiese | `#ACB98B` | nur außen: Rasen, Wiese, Hang (Entscheid des Nutzers 23.10.2026: eigener Außen-Grünton statt Mint); warm-gedecktes Graugrün zwischen Sand und Laub, Wiesenflecken eine Stufe heller `#B9C59A` |
| Laub | `#6F8A62` | nur außen: Kronen der Laubbäume, Hecken, Büsche, vorderes Waldband (Entscheid des Nutzers 23.10.2026). Tiefenstaffelung des Walds: vorn Laub (besonnt), Mitte Petrol (Kamm im Schatten — die dunkle Form der Palette, kein Mischton mehr), hinten Papier (Dunst); Stadtdächer im Tal Linoleum warm |

Magenta `#C2185B` bleibt der Oberfläche vorbehalten (Zirkel, Messwerte, Signal im UI) und kommt
in keinem Raumbild vor. Rot-Rosa und reines Schwarz gehören dem Millimeterpapier und der Kurve.

### Je Raum eine eigene Hauptkombination (10.10.2026)
Alle Räume teilen Sand/Papier/Mint/Petrol/Tinte/Holz, aber jeder Raum hat eine eigene Verteilung,
sonst sind sie nicht zu unterscheiden:

| Raum | Wand | Sockel | Boden | Möbel | Rost (das eine Objekt) |
|---|---|---|---|---|---|
| Lehrsaal (08:10, neutral) | Papier | Mint | Linoleum warm | Holz-Seminartisch, Petrol-Stühle und -Wagen, Liege mit Mint-Bezug | rote Elektrodenklemme am rechten Arm des Freiwilligen (`docs/raeume/lehrsaal.md`) |
| Aufnahme (06:40, warm) | Sand | Mint | Linoleum warm | Holz-Tresen, Petrol-Polster der Bank, Geräte Tinte | Betablocker-Schachtel in Herrn Baums Tüte (die Tüte ist sein Gegenstand, keine Klickzone mit Fortschritt — `KONZEPT.md` §1.3) |
| Monitorzimmer (09:15, kühl) | Mint hell | Sand | Linoleum kühl | Papier-Tischplatte auf Petrol-Blöcken, Holz-Aktenschrank | Dr. Falks Zirkel |

Werkstoff-Logik: Holz für Arbeitsplatten, Tresen, Zargen, Armlehnen; Petrol für Polster und lackierte
Gehäuse; Tinte für Gestelle, Griffe und dunkles Glas; Papier für Ablagen, Rahmen, Zettel. Himmel draußen
als flache Bänder aus Morgenlicht-Abwandlungen (Aufnahme: `#F8E7BF` → `#F6DCA4` → `#F3CD8C`, Sonne `#FFF6DC`;
Monitorzimmer: `#DCE9EA` / `#E6EFEE`), Silhouetten draußen in Petrol und Papier.

### Regeln, die aus der Recherche kommen
1. Der Streifen ist das einzige hochfrequente Element am Bildschirm. Raster, Korn, Dithering
   berühren ihn nie.
2. Der Streifen ist heller als die Welt: eigenes Papier `#FFF8F4` mit Schatten, nie Sand.
3. Hinweise auf dem Streifen sind statische Farbflächen unter der Kurve. Nichts blinkt.
   Geräteschirme im Raum (EKG-Wagen, Bettmonitore) zeigen laufende Kurven aus `data/`, gezeichnet vom
   Code auf eine Leinwand in der Ebene des Schirms (`art/szenen/<raum>/schirme.json` → `spiel.js`);
   im Render bleibt die Schirmfläche eine ruhige Glasfläche. Ableitung und Frequenz setzt der Code.
4. Jede Requisite besteht den Test „Würde ein Kardiologe sie zur Entscheidung brauchen?" —
   sonst bleibt sie klein, still oder weg.
5. Figuren tragen Emotion im Gesicht; Körperdetail und Realismus zählen wenig.

## 3. Licht und Tiefe

1. **Gestufte Tonwerte**: Boden und Möbel eine Stufe dunkler als die Wand, dazu eine helle
   Lichtinsel dort, wo das Wichtige liegt. Das Auge geht ins Licht, immer.
2. **Die Lichtquelle ist im Bild sichtbar** (Lampe, Monitor, Fenster, Notausgangsschild).
3. **Kein angeschnittener dunkler Vordergrund** (Türrahmen, Ständer o. Ä. am Bildrand): der Raum
   bleibt offen und ruhig. Tiefe entsteht durch Dreiviertelansicht, Tonwerte und Parallaxe.
4. **Drei Ebenen für Parallaxe**: Figur · Mittelgrund · Hintergrund.
5. **Schatten außen** (Entscheid 23.10.2026): Gebäude, Vordächer und Fahrzeuge werfen echte, harte Schlagschatten.
   Bäume, Büsche, Hecken, Laternen und Bänke werfen **keinen** Schlagschatten (Kronenschatten zerlegen Fassaden in
   Flecken, bei tiefer Sonne liefen 20–30 m lange Streifen ohne sichtbaren Werfer durchs Bild). Sie bekommen stattdessen
   einen **Fußschatten**: eine flache, harte Form in derselben Schattenstufe wie alle anderen Schatten, knapp am Fuß, in
   Sonnenrichtung versetzt und gestreckt — so stehen sie auf dem Boden statt aufgeklebt zu wirken.

## 4. Tageszeiten — kein ewiger Regen

Die Geschichte läuft über **eine Rotation aus mehreren Diensten** (`docs/KONZEPT.md` §2), und das
Licht erzählt mit. Kapitel 1 und 2 liegen im selben Frühdienst; jedes weitere Kapitel ist ein
eigener Tag. Die Kopfzeile nennt Dienst und Uhrzeit („Dienst 1 · 06:40").

| Kapitel | Dienst | Zeit | Licht |
|---|---|---|---|
| 0 Lehrsaal | Einschulungstag | 08:10 | Vormittag, neutrales Tageslicht von rechts, Beamer an, kurze Schatten |
| 1 Aufnahme | Dienst 1 | 06:40 | Sonnenaufgang, langes warmes Licht durch die Jalousien |
| 2 Monitorzimmer | Dienst 1 | 09:15 | heller Vormittag, kühles Tageslicht, Bildschirme blass |
| 3 Station | Dienst 2 | 13:30 | Mittag, flaches Licht, Staub in der Luft |
| 4 Intensiv | Dienst 3 | 18:50 | Abendrot, lange Schatten |
| 5 Aufwachraum / Innere | Dienst 6 | 22:10 | Nacht, nur Lampeninseln |
| 6 Befundraum / Finale | Nachtdienst | 02:14 | tiefe Nacht, Regen — jetzt ist es verdient |

Herzkatheter (Dienst 4, 10:00, hartes Kunstlicht) und Rhythmusambulanz (Dienst 5, 15:00, Nachmittag)
bekommen ihre Zeile, sobald ihre Räume beschrieben sind.

## 5. Figuren

Umsetzung in ligne claire: einfache Formfamilien als 3D-Grundkörper (Blender), gerendert durch
dieselbe Pipeline wie die Räume (Fläche + Linie), Gesicht als wenige klare Formen (Augen, Brauen,
Mund) mit drei bis vier Ausdrücken. So bleibt dieselbe Person in jedem Raum dieselbe Person.

Jede Figur erfüllt alle fünf Punkte, sonst ist sie nicht fertig:

1. **Silhouette**: schwarz ausgefüllt und daumennagelgroß noch erkennbar.
2. **Formfamilie**: eine dominante Form, ein Gegenakzent.
3. **Ein Gegenstand**, der immer dabei ist und etwas über sie erzählt.
4. **Eine Akzentfarbe**, die nur ihr gehört.
5. **Haltung statt Pose**: angelehnt, in Bewegung, mitten im Satz — nie strammstehend.

### Besetzung

**Schwester Marlene, 54** — „Hält die Station seit zwanzig Jahren zusammen und kennt jeden Namen."
Runde Formfamilie, kompakte Silhouette, großer schiefer Dutt mit Lesebrille darin, Kuli hinterm Ohr.
Gegenstand: verbeulte **Magenta-Thermoskanne**, die sie nie abstellt. Akzent: Magenta.
Details: Namensschild mit verblasstem Katzensticker, hochgekrempelte Ärmel, grüne Socken in Clogs,
Lachfalten, schwere Lider. Spricht kurz, trocken, warm.

**Oberarzt Dr. Falk, 61** — „Redet langsam, weil er das alles schon gesehen hat."
Dreieckige, vertikale Formfamilie, hoher schmaler Umriss, langer Kittel mit scharfem Saum,
Hände in den Taschen. Gegenstand: **messingfarbener EKG-Zirkel**, mit dem er alles ausmisst —
im Spiel wird genau dieser Zirkel zum Messwerkzeug des Spielers. Akzent: Bernstein.
Details: Brille an der Kette, Kaffeefleck am Kittel, Stethoskop mit rissigem Schlauch.

**Herr Konrad Baum, 68, „Herr K."** — „Ist zu Fuß gekommen, weil er die Tochter nicht wecken wollte."
Weiche Rechteck-Formfamilie, gebeugter Bogen, breiter Rücken, Schiebermütze, die er nicht abnimmt.
Gegenstand: **Plastiktüte mit Tablettenschachteln und einem Foto der Enkelin**. Akzent: rotes
Faden-Armband von der Enkelin. Details: Hausschuhe, Strickjacke unterm Patientenhemd, Hörgerät.

**Die Spielfigur (KPJ-Student)** — nur als Hände, Schatten und Spiegelbild. Kapuzenpulli unterm
Kittel, Bleistift hinterm Ohr, das EKG-Lineal aus dem Kurs in der Tasche (Dr. Wieser hat es ihr am
Einschulungstag aus der Schachtel gegeben).

**Dr. Nora Wieser, 41** — Lehrperson im Lehrsaal; blaues EKG-Lineal, Akzent Kobaltblau `#2F5DA8`,
nie sitzend, ein Fuß auf dem Tritt der Liege. Alle fünf Punkte und das Stimmprofil:
`docs/raeume/lehrsaal.md` §2.

**Jonas Prem, 24** — Tutor, liegt als Freiwilliger auf der Liege; Kopfhörer um den Hals, Akzent
Senfgelb `#D9A441`. `docs/raeume/lehrsaal.md` §2.

**Frau Gerda Lindner, 76** — Patientin im Monitorzimmer (Vorhofflimmern); runde Formfamilie, sitzt
aufrecht im Bett, Strickzeug auf der Decke als Gegenstand, Akzent Flaschengrün `#3E6B4F` (Wolle).
Akte: `docs/faelle/monitor.md`. Neue Patientenfiguren gehen denselben Weg wie Herr K. (Blockout →
Kontext → einsetzen, `gen/blender/README.md`).

## 6. Was ein Bild sofort disqualifiziert

- Schrift im Bild. **Jeder Text im Spiel wird vom Code gesetzt**, nie vom Bildmodell —
  das ist das eindeutigste Erkennungszeichen für KI-Bilder.
- Ein EKG, das vom Bildmodell gemalt wurde. **Alle Kurven kommen aus der Engine**, aus echten
  Aufnahmen. Gemalte Zacken sind medizinisch falsch und sofort als Fake erkennbar.
- Sechs Finger, verbogene Hände, Instrumente, die es nicht gibt, Stethoskope mit zwei Schläuchen.
- Frontalansicht ohne jede Tiefe (leichte Dreiviertelansicht genügt).
- Mehr als ein Magenta-Objekt.
- Requisiten ohne Grund im Bild („sieht medizinisch aus") — jedes Ding gehört jemandem.

## 7. Logikprüfung — vor jedem Einchecken einer Szene

Ein Raum muss als Ort funktionieren, nicht nur als Bild. Durchgehen, bevor Ebenen ins Spiel kommen:

1. **Wege frei.** Jede Tür, jeder Durchgang und jeder Ausgang-Hotspot hat freien Boden davor.
   Kein Stuhl vor der Tür, kein Wagen im Gang.
2. **Dinge stehen, wo sie gebraucht werden.** EKG-Wagen am Patienten, Monitor dort, wo man ihn
   vom Platz aus sieht, Lampe über dem Arbeitsplatz. Jedes Ding gehört jemandem.
3. **Die Uhr geht richtig.** Zeiger werden nie ins Bild gerendert; sie sind SVG-Elemente
   (`#uhr-std`, `#uhr-min`, aus `hitboxes.json` → `gen/kunst.py`) in derselben Ebene wie das Zifferblatt
   (Hintergrund — in einer anderen Ebene wanderten sie in der Parallaxe gegen die Uhr) und folgen der Spielzeit.
   Das Licht im Raum passt zur Uhrzeit des Kapitels (Tabelle in Abschnitt 4).
4. **Maßstab stimmt.** Stuhl ≈ 0,5 m, Tresen ≈ 1,05 m hoch, Tür ≈ 2,1 m; Figuren stehen auf dem
   Boden, Füße auf der Bodenlinie, nicht davor schwebend.
5. **Es bewegt sich etwas.** Figuren atmen (`class="atmet"` auf ihrem Element), Parallaxe
   läuft, Bildschirme zeigen die laufende Kurve. Eine Szene ohne jede Bewegung ist nicht fertig.
6. **Hotspots sind erreichbar** und überlappen nicht: Tür, Figur, Gegenstand getrennt.
