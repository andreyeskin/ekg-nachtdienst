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

Magenta `#C2185B` bleibt der Oberfläche vorbehalten (Zirkel, Messwerte, Signal im UI) und kommt
in keinem Raumbild vor. Rot-Rosa und reines Schwarz gehören dem Millimeterpapier und der Kurve.

### Regeln, die aus der Recherche kommen
1. Der Streifen ist das einzige hochfrequente Element am Bildschirm. Raster, Korn, Dithering
   berühren ihn nie.
2. Der Streifen ist heller als die Welt: eigenes Papier `#FFF8F4` mit Schatten, nie Sand.
3. Hinweise auf dem Streifen sind statische Farbflächen unter der Kurve. Nichts blinkt.
4. Jede Requisite besteht den Test „Würde ein Kardiologe sie zur Entscheidung brauchen?" —
   sonst bleibt sie klein, still oder weg.
5. Figuren tragen Emotion im Gesicht; Körperdetail und Realismus zählen wenig.

## 3. Licht und Tiefe

1. **Drei Helligkeitszonen pro Bild**: fast schwarzer Vordergrundrahmen → mittlerer Raum →
   eine helle Lichtinsel dort, wo das Wichtige liegt. Das Auge geht ins Licht, immer.
2. **Die Lichtquelle ist im Bild sichtbar** (Lampe, Monitor, Fenster, Notausgangsschild).
3. **Vordergrund schneidet an**: Türrahmen, Infusionsständer, Rollstuhlgriff — dunkel, knapp,
   leicht unscharf. Das erzeugt Raum und das Gefühl, selbst dort zu stehen.
4. **Vier Ebenen für Parallaxe**: Vordergrund · Figur · Mittelgrund · Hintergrund.

## 4. Tageszeiten — kein ewiger Regen

Die Geschichte läuft über **eine Schicht**, und das Licht erzählt mit:

| Kapitel | Zeit | Licht |
|---|---|---|
| 1 Aufnahme | 06:40 | Sonnenaufgang, langes warmes Licht durch die Jalousien |
| 2 Monitorzimmer | 09:15 | heller Vormittag, kühles Tageslicht, Bildschirme blass |
| 3 Station | 13:30 | Mittag, flaches Licht, Staub in der Luft |
| 4 Intensiv | 18:50 | Abendrot, lange Schatten |
| 5 Aufwachraum | 22:10 | Nacht, nur Lampeninseln |
| 6 Ambulanz / Finale | 02:14 | tiefe Nacht, Regen — jetzt ist es verdient |

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
Kittel, Bleistift hinterm Ohr, das EKG-Lineal aus dem Kurs in der Tasche.

## 6. Was ein Bild sofort disqualifiziert

- Schrift im Bild. **Jeder Text im Spiel wird vom Code gesetzt**, nie vom Bildmodell —
  das ist das eindeutigste Erkennungszeichen für KI-Bilder.
- Ein EKG, das vom Bildmodell gemalt wurde. **Alle Kurven kommen aus der Engine**, aus echten
  Aufnahmen. Gemalte Zacken sind medizinisch falsch und sofort als Fake erkennbar.
- Sechs Finger, verbogene Hände, Instrumente, die es nicht gibt, Stethoskope mit zwei Schläuchen.
- Frontalansicht ohne jede Tiefe (leichte Dreiviertelansicht oder ein Vordergrund-Element genügt).
- Mehr als ein Magenta-Objekt.
- Requisiten ohne Grund im Bild („sieht medizinisch aus") — jedes Ding gehört jemandem.
