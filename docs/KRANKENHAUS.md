# Krankenhaus zuerst und Neuausrichtung — Wünsche des Nutzers (18.10.2026)

Status: **Konzept ausgearbeitet (19.10.2026), Blockout offen.** Die Entscheidungen des Nutzers (Abschnitt
„Antworten des Nutzers" und Leitsatz „Denken statt Gehen") gelten; das Konzept steht in den Abschnitten ab
„Vorbild Gebäude 31" (Maße, Grundrisse, Flug, Mentoren). Nichts davon ist gebaut; der Blender-Blockout ist der
nächste Schritt (Abschnitt „Nächster Schritt" am Ende).

## Anlass (Wortlaut des Nutzers, sinngemäß übersetzt)

Nach dem spielbaren Prototyp von Fall 1: „Das ist alles schön, aber trotzdem unverständlich. Ich will zuerst das
Krankenhaus als Ganzes bauen: Patientenzimmer, Flure, den Lehrsaal, überhaupt eine bestimmte Abteilung, ein eigenes
Gebäude, in dem alle Ereignisse spielen. Gleich am Anfang erklären, was wir lernen und wie es ablaufen wird, und
dazu einen Flug machen: hier ist die Abteilung, hier die Zimmer. Und natürlich ein 3D-Modell des Krankenhauses,
dessen Räume wir dann im Spiel verwenden."

## Was das lösen soll

- **Orientierung:** Die Spielerin weiß von der ersten Minute an, wo sie ist, was sie hier lernt und wie das Spiel
  abläuft. Heute beginnt das Spiel mitten in der Aufnahme, ohne Rahmen; das ist ein Teil des „unverständlich".
- **Ein Ort für alles:** Alle Kapitel spielen in einem Haus. Wege werden räumlich nachvollziehbar (Aufnahme im
  Erdgeschoss → Herr Baum fährt „nach oben" → Monitorzimmer), Figuren treffen sich wieder.
- **Ein Modell, viele Räume:** Ein 3D-Gesamtmodell liefert alle Raumbilder mit gleichem Maßstab, gleichem Licht und
  gleichem Stil (ART_BIBLE, ligne claire). Die heutigen Einzelszenen (`gen/blender/szene_aufnahme.py`,
  `szene_monitor.py`, `szene_lehrsaal.py`) werden Räume dieses Hauses.

## Bausteine (Vorschlag des Koordinators, alles zu entscheiden)

1. **Das Haus.** Ein fiktives Krankenhaus (kein echtes Haus, kein Logo, kein echter Name), ein eigenes Gebäude der
   Inneren Medizin mit Kardiologie. Die Räume aus KONZEPT §3 bekommen einen Ort, z. B.:
   - Erdgeschoss: Eingang, Rettungszufahrt, Notaufnahme/Aufnahme (Kapitel 1);
   - 1. Stock: kardiologische Station mit Patientenzimmern (Kapitel 3) und Monitorzimmer/Überwachung (Kapitel 2),
     Stationsstützpunkt, Dienstzimmer;
   - 2. Stock: Intensivstation (Kapitel 4), Herzkatheterlabor und Chest Pain Unit (Kapitel 5);
   - Ambulanzbereich: Rhythmusambulanz (Kapitel 6);
   - Lehrsaal (Kapitel 0), Befundraum/Arztzimmer (Finale), Aufenthaltsraum oder Cafeteria (nur Atmosphäre).
2. **3D-Modell** in der Blender-Pipeline (`gen/blender/`): zuerst ein Blockout des ganzen Gebäudes mit Grundriss
   je Stock, Fluren, Treppenhaus und Lift; jeder Spielraum ist eine Kamera im selben Modell. Grundrisslogik nach
   einem echten österreichischen Haus (der Nutzer ist die Quelle), aber ohne Wiedererkennbarkeit.
3. **Einführung mit Flug.** Spielbeginn: das Haus von außen im Morgenlicht → Eingang → Flur → Station → Zimmer.
   Dazu in wenigen Sätzen: **was** wir lernen (EKG lesen an echten Aufnahmen), **wie** es abläuft (eine Rotation
   über mehrere Dienste, jeder Fall ein Patient, messen mit dem Zirkel, Befundmappe, Verdachtsliste) und **wo**
   (dieses Haus). Der Flug endet im Lehrsaal am Einschulungstag (KONZEPT §3, Kapitel 0, Dr. Wieser).
   Technik, nach Größe der Einzeldatei: (a) Kamerafahrt als Folge weniger Standbilder mit Überblendung und
   Parallaxe (klein, einzeldateitauglich); (b) echtes Video nur in der gehosteten Fassung (TON.md §3);
   (c) dazu ein **Querschnitt des Hauses** (Puppenhaus-Schnitt), der im Spiel bleibt.
4. **Lageplan im Spiel.** Der Querschnitt als Knopf „Haus" in der Kopfleiste: wo bin ich, welche Räume sind offen,
   welcher Dienst ist heute. Er macht die Kapitelfolge sichtbar.

## Folgen für den Bestand

- **Reihenfolge:** Haus-Konzept und Gebäudemodell kommen vor dem Umbau von Fall 1. Der neue Aufnahme-Render (B1 in
  `docs/REDESIGN_FALL1.md` §8.3: Koje, Glastür, Wagen als eigene Ebene) entsteht dann als Raum dieses Hauses.
- **Gilt weiter:** KONZEPT §1 (Grundsätze) und §2 (Rotation über mehrere Dienste); ART_BIBLE §4 (Tageszeiten) für
  das ganze Haus; der Redesign-Entwurf von Fall 1 als Inhalt der Aufnahme.
- **Farbpalette** (Merkzettel in STAND.md) am Haus mit ausprobieren: Außenansicht, Flur, Zimmer.
- **Lehrsaal** (halb fertig) wird ein Raum im Haus; der Einschulungstag knüpft an den Flug an.

## Offene Fragen an den Nutzer

1. Welche Abteilung genau (Innere Medizin mit Kardiologie und eigener Notaufnahme, oder eine reine Kardiologie)?
2. Name des Hauses (fiktiv) und Stadt (Graz als Kulisse, aber ohne echtes Krankenhaus)?
3. Flug: Bildfolge in der Einzeldatei oder Video in der gehosteten Fassung; Länge etwa 30 bis 60 Sekunden?
4. Wer führt ein: Erzähler, Dr. Wieser oder Marlene?
5. Wie viel vom Haus ist begehbar: nur die Spielräume oder auch Flure zum Hin- und Hergehen?

## Zweite Nachricht des Nutzers (18.10.2026, abends): Wünsche zur Neuausrichtung

Sinngemäß übersetzt und geordnet; alles verbindliche Wünsche, die Ausarbeitung entscheidet das Wie.

1. **Ort:** im Hintergrund eine hübsche europäische Stadt; im Krankenhaus und draußen **viel Grün**.
2. **Alles stimmig:** ein Haus, ein Stil, eine Palette, passende Wege, Zeiten und Namen. Als Vorbild Bilder echter
   Krankenhäuser. Der Nutzer mag besonders das **Gebäude der Psychiatrie am LKH Graz**: finden, als Vorbild für das
   3D-Modell nehmen, deutlich verändert (kein Name, kein Logo, nicht wiedererkennbar als echtes Haus).
   Welches Gebäude gemeint ist, ist noch zu bestätigen. Kandidaten aus einer ersten Suche: (a) Universitätsklinik
   für Psychiatrie am LKH-Univ. Klinikum Graz, Auenbruggerplatz (im Lageplan Gebäude 31); (b) LKH Graz II, Standort
   Süd, Pavillonanlage im Park; (c) Erweiterung der Kinder- und Jugendpsychiatrie am LKH Graz II Süd (Holzbau,
   fünf „Häuser" um einen „Dorfplatz"). Nutzer um Bestätigung oder ein Foto bitten.
   **Bestätigt vom Nutzer (18.10.2026): (a), Gebäude 31 (Psychiatrie) am LKH-Univ. Klinikum Graz, Auenbruggerplatz.**
   Fotos und Ansichten im nächsten Chat suchen; Vorbild für Bauform, Fassade, Grün, nicht für Grundriss oder Namen.
3. **Leben im Hintergrund:** man soll spüren, dass das Haus lebt. Viele Ärztinnen und Ärzte mit ihren eigenen
   Aufgaben, Patienten liegen in den Zimmern, gehen über den Flur. (Prototyp `prototyp/bewegung/` ist der Anfang.)
4. **Format:** Der Nutzer fragt, ob das Spiel mehr 3D werden soll oder ob das heutige Format passt (Empfehlung unten).
5. **Ton der Figuren:** Heute wirken die Figuren passiv-aggressiv, die Repliken sind unklar. Das soll weg: keine
   Rätselsätze, keine Spitzen, nichts Unverständliches. Kolleginnen und Mentoren sind freundlich und unterstützend.
6. **Weniger Text, mehr Interaktion:** so klar wie möglich, weniger lesen, mehr tun, z. B. **Elektroden kleben**.
7. **Mentor statt Torwächter:** Heute muss man für jede Frage an den Patienten erst zu einer Ärztin oder zum
   Arzt, die einen weiterschicken. Stattdessen ein echter Mentor je Tag: „Heute lernen wir Dr. X kennen, sie ist auf
   Y spezialisiert, und das lernen wir heute."
8. **Das Haus** möglichst detailreich, schön und verständlich zeigen.
9. **Interesse und Dynamik** im Spiel.
10. **Themenliste mit Fortschritt:** sichtbar, welche Themen es gibt und wie weit man ist.
11. **Viele Entscheidungen und Fragen**, aber immer mit spürbarer **Unterstützung der Kolleginnen und Kollegen**.

## Empfehlung des Koordinators zum Format

**Das heutige Format behalten und um 3D aus einem echten Modell erweitern** (Web, eine Datei, iPad, offline).
- Das Haus wird ein vollständiges 3D-Modell in Blender. Daraus kommen alle Raumbilder (vorgerendert, ligne claire),
  der Flug am Anfang und **Kamerafahrten zwischen den Räumen** (Flur entlang, Lift, Tür auf). Das gibt das
  3D-Gefühl, ohne dass Figuren in Echtzeit animiert werden müssen.
- Ein **begehbarer Querschnitt** des Hauses (statisches Modell, z. B. mit three.js, ohne Figuren) für Einführung und
  Lageplan ist machbar und klein.
- Leben im Hintergrund als 2D-Ebenen über den Renders (Silhouetten, kurze Bildfolgen, Licht), wie im Prototyp.
- Echtes Echtzeit-3D mit frei begehbaren Räumen und animierten Figuren wäre ein anderes Projekt: Figuren müssten
  geriggt und animiert werden, das Spiel würde groß, auf dem iPad langsamer, und ohne Animatoren wirken Figuren
  steif. Nur sinnvoll, wenn freies Herumgehen selbst ein Ziel ist.

**Stand der Entscheidung (18.10.2026):** Der Nutzer ist unsicher („keine Erfahrung") und fragt, ob das Format als
Quest funktioniert. Antwort: ja, es ist das klassische Point-and-Click-Adventure (gerenderte Räume, Klickfelder,
Gespräche, Rätsel als Nahaufnahmen); Messen mit Zirkel und Pencil braucht ohnehin ein ruhiges 2D-Bild. Die Wahl ist
umkehrbar, weil das Hausmodell in beiden Fällen dasselbe ist. Deshalb **Entscheidung durch Probe**: nach dem
Blockout (a) einen Flur als statisches 3D zum Selbstgehen im Browser (three.js, ohne Figuren) und (b) denselben Flur
als vorgerenderten Raum mit Leben-Ebenen bauen; der Nutzer probiert beide auf dem iPad und entscheidet dann.
Modell so anlegen, dass es auch als glTF exportierbar ist.

**Leitsatz des Nutzers (18.10.2026):** „Die Zeit geht ins Denken, nicht ins Gehen durch Flure." Damit ist das Format
**Quest im 3D-Haus** (Variante b) die Vorgabe: Räume vorgerendert aus dem Modell, Wege als kurze Kamerafahrten statt
selbst gelaufen, Leben als Ebenen. Die Probe mit Variante (a) entfällt, außer der Nutzer will sie ausdrücklich. Der
Leitsatz gilt auch für alles andere: keine Laufwege, kein Hin- und Herschicken, kein Suchen; jede Minute Spielzeit
soll eine Denk- oder Handentscheidung sein.

**Godot erwogen (19.10.2026, Frage des Nutzers nach einem Beitrag „Claude Code + Godot über MCP"):** jetzt nicht.
Godot lohnt sich für Echtzeit-3D, Animation und native Apps; das Format „Quest im 3D-Haus" braucht das nicht. Ein
Wechsel hieße alles neu bauen (Dialogmotor, EKG-Papier mit Zirkel und Pencil, Prüfungen, Texte über IDs), und der
Web-Export ist für eine Offline-Einzeldatei auf dem iPad schwer. Wieder prüfen, wenn eine App im App Store,
frei begehbares 3D oder viel Figurenanimation gewünscht wird; das Hausmodell (glTF) ließe sich dann übernehmen.

## Was das am Bestand ändert (zur Ausarbeitung)

- **KONZEPT §3:** Jeder Dienst bekommt **einen Mentor mit Fachgebiet und Tagesthema**, der sich vorstellt und
  begleitet. Falk, Wieser und Marlene werden darin eingeordnet; neue Mentorinnen für Infarkt, Rhythmusambulanz,
  Intensiv.
- **Skill `dialoge` §4 (Stimmprofile):** freundlich und klar statt schroff. „Kein Lob ohne Einschränkung" (Falk) und
  „nie Unsicherheit zugeben" (Marlene) erzeugen das Passiv-Aggressive und werden ersetzt. Widerspruch bleibt als
  Lehrmittel, aber offen und kollegial („Ich halt jetzt bewusst dagegen, damit du deine Gründe sortierst.").
- **Fall 1 (`docs/REDESIGN_FALL1.md`):** Inhalt und Medizin bleiben; Text kürzen; Torwächter-Wege (zum Wagen
  geschickt, erst Marlene fragen) durch freie Arbeit mit Mentor an der Seite ersetzen; Falk als Mentor statt
  Gegenspieler; mehr Handgriffe.
- **Interaktionen statt Lesen** (jede mit Beleg über `fallakte`): Elektroden kleben (Ampel-Regel), Puls tasten und
  zählen, Blutdruck im Stehversuch ablesen, das EKG-Gerät bedienen (Papiervorschub 25/50 mm/s), Wellen antippen,
  Zirkel, Medikationsplan durchsehen (welche Tablette bremst den AV-Knoten), Verdachtsliste selbst ordnen,
  ISBAR-Karten in die Reihenfolge ziehen, Monitoralarm quittieren und Elektrode wieder ankleben.
- **Themenliste:** `docs/LEHRPLAN.md` als Lernpfad im Spiel (Themen, erledigt/offen, wo im Haus).
- **Unterstützung:** ein Knopf „Kollegin fragen" (Marlene, Jonas) gibt einen Hinweis ohne Strafe; Rückmeldungen
  ermutigen und erklären.

## Offene Fragen an den Nutzer (Ergänzung)

6. ~~Welches Gebäude der Psychiatrie in Graz ist gemeint?~~ Beantwortet: Gebäude 31, LKH-Univ. Klinikum Graz.
7. ~~Format~~ Entschieden: Quest im 3D-Haus (Leitsatz „Denken statt Gehen", siehe oben).
8. Mentoren: eine Person je Dienst (neue Figuren) oder wenige feste Mentoren, die wechseln?

**Antworten des Nutzers (19.10.2026):**
1. Abteilung: **Innere Medizin mit Kardiologie und eigener Notaufnahme** (alle Kapitel 0–8 in einem Haus).
2. Ort: **fiktive Stadt** nach dem Vorbild Graz (österreichisch, Hügel, Dächer, viel Grün), ohne erkennbare
   Wahrzeichen; Name des Hauses und der Stadt erfunden (Vorschlag in der Ausarbeitung).
3. Flug: **Bildfolge in der Einzeldatei, etwa 40 Sekunden** (8–10 Renders, Überblendung, Parallaxe, überspringbar).
4. und 8. Mentoren **gemischt**: feste Figuren (Wieser, Falk, Marlene) und neue für Infarkt, Rhythmusambulanz,
   Intensiv; **Dr. Wieser führt ein** (Stimme zum Flug).
5. Begehbar: nur die Spielräume; Wege als kurze Kamerafahrten (folgt aus dem Leitsatz „Denken statt Gehen").

## Vorbild Gebäude 31 (Recherche 19.10.2026)

**Identifikation: sicher.** Drei unabhängige Quellen zeigen dasselbe Haus: der amtliche Lageplan des Klinikums
führt „31 Psychiatrie" (Planquadrat N 17, Eingang 31/1 „Stationen, Seminarraum"; 31/3 „Ambulanz" in M 16);
OpenStreetMap hat den Grundriss als Gebäude „Psychiatrie", Auenbruggerplatz 31, offizieller Name
„Universitätsklinik für Psychiatrie"; Wikipedia nennt die frühere Klinik für Lungenkrankheiten, heute Psychiatrie,
„im Stil eines Lungensanatoriums" auf der Anhöhe im Leechwald hinter dem Hauptgelände.

**Unsicher: die Fassade.** Ein frei zugängliches Foto der Fassade von Gebäude 31 habe ich nicht gefunden (Commons,
KAGes-Seiten, Architekturdatenbanken, Pressefotos zeigen andere Häuser des Klinikums oder das LKH Graz II). Was unten
über Geschosse, Fenster und Putz steht, ist aus Luftbild, Grundriss und Bautyp (Sanatoriumspavillon um 1912)
abgeleitet, nicht aus einem Foto. Ein Handyfoto des Nutzers von der Talseite würde das bestätigen (offene Frage 1).

### Links (keine Bilder im Repository, nur eigene Beschreibung)

| Nr. | Link | Was darauf zu sehen ist |
|---|---|---|
| 1 | https://uniklinikumgraz.at/fileadmin/media/lkh-univ-klinikum-graz/Lageplan.pdf | Amtlicher Lageplan: „31 Psychiatrie" am Nordostrand des Geländes neben 36 Ausbildungszentrum, 32 Strahlentherapie, 34 Kinderklinik; Eingänge 31/1 (Stationen, Seminarraum, N 17) und 31/3 (Ambulanz, M 16) |
| 2 | https://www.openstreetmap.org/way/361495611 | Grundriss als Polygon (75 Punkte): langgestreckter Riegel von Südwest nach Nordost, Längsachse etwa 36° (Nord über Ost), rund 105 m lang, 50 m breit samt Kopfbau, 2 130 m² Grundfläche; viele kleine Vor- und Rücksprünge (Erker, Risalite) an der Südostseite |
| 3 | https://nominatim.openstreetmap.org/search?q=Auenbruggerplatz+31+Graz&format=json&polygon_geojson=1 | Dieselbe Fläche mit Koordinaten (47,0858 N, 15,4661 O), Katastralgemeinde Geidorf |
| 4 | https://www.bing.com/maps?cp=47.0858~15.4661&lvl=19.3&style=a | Luftbild: zwei Altbaukörper hintereinander mit roten Ziegel-Walmdächern und Quergiebeln (kreuzförmige Dachfiguren), dazwischen ein niedriger Verbindungsteil; am Südwestende ein weiß verputzter Flachdach-Anbau mit Lüftungsaufbauten; Ringstraße mit Parkplätzen auf der Talseite (Ost), geschlossener Wald im Westen und Norden |
| 5 | https://de.wikipedia.org/wiki/LKH-Universitätsklinikum_Graz | Geschichte: 29 Gebäude im Secessionsstil (1904–1912), Pavillons ost-west-orientiert; die Lungenklinik (heute Psychiatrie) mit größerem Abstand auf der Anhöhe im Leechwald, im Stil eines Lungensanatoriums |
| 6 | https://de.wikipedia.org/wiki/Liste_der_denkmalgeschützten_Objekte_in_Graz/Geidorf | Denkmaleintrag des Ensembles: Jugendstil 1904–1912 nach Plänen des Landesbauamts unter Karl Hupfer, Ornament August Herz, Pavillonsystem mit Flachdächern (Haupttrakte) |
| 7 | https://commons.wikimedia.org/wiki/File:LKH_Graz_Hauptgebäude.jpg | Hauptgebäude des Ensembles: heller Putz, vier Geschosse, strenges Fensterraster, Attika statt Dachüberstand, Lisenen. Stilreferenz für Putz und Fensterrhythmus, nicht für das Dach |
| 8 | https://commons.wikimedia.org/wiki/File:Leechwald_05.jpg | Tor im Zaun zwischen Leechwald und Klinikgelände, 47 m von Gebäude 31: zwei Steinpfeiler mit Reliefmedaillons, kleines Ziegeldach über dem Tor, Holzlattenzaun, Schnee. Vorbild für unser „Waldtor" |
| 9 | https://commons.wikimedia.org/wiki/File:Übersicht_Med_Uni_Graz.jpg | Luftbild des Campus: weiße Pavillons, dichte Neubauten, am oberen Bildrand der Wald, in dem Gebäude 31 liegt |
| 10 | https://www.mapillary.com/app/?lat=47.0856&lng=15.4664&z=17.5 | Straßenfotos (Oktober 2015) entlang des Auenbruggerplatzes östlich des Hauses: Allee, Wiesenhang, der zum Haus ansteigt, Haus selbst hinter Bäumen verdeckt; gegenüber ein Neubau mit auskragendem Glasgeschoss (Ausbildungszentrum) |
| 11 | https://www.uniklinikumgraz.at/psychiatrie | Klinikseite: Auenbruggerplatz 31, 131 Mitarbeitende, 769 stationäre Aufnahmen im Jahr. Ein kleines Haus, keine Großklinik; das passt zu unserem Maßstab |

### Was wir übernehmen

| Merkmal | Vorbild | Im Spiel |
|---|---|---|
| Lage | Anhöhe am Waldrand, abseits des Hauptgeländes, Wald im Rücken, Wiese zur Talseite | Hangterrasse über der Stadt, Wald (Buchen, Föhren) hinter dem Haus, Park und Wiese davor |
| Bauform | langer Riegel mit Kopfbau, Längsachse schräg zum Hang | Riegel 61,2 m plus Kopfbau 24 m, Längsachse Südwest–Nordost |
| Dach | Ziegel-Walmdächer mit Quergiebeln | ein Walmdach mit einem Quergiebel über dem Mittelrisalit |
| Fassade | heller Putz, regelmäßiges Fensterraster (Campus-Stil) | Putz in Sand, Fensterachsen alle 3,6 m, Rahmen Petrol |
| Anbau | Flachdachbau an einem Ende | Flachdachbau am Nordostende: Notaufnahme mit Rettungsvorfahrt |
| Erschließung | Ringstraße mit Vorfahrt auf der Talseite | Klinikstraße im Osten, Vorfahrt am Kopfbau, Parkweg zum Eingang |
| Grün | Wald, Wiese, Zaun mit Tor zum Wald | Park, Garten im Gebäudewinkel, Dachgarten auf dem Kopfbau, „Waldtor" |
| Maßstab | kleines Haus mit Stationen, Ambulanz, Seminarraum | ein Haus für alle Kapitel 0–8 |

### Was wir bewusst ändern (damit es nicht wiedererkennbar ist)

1. **Spiegelung:** Kopfbau und Anbau liegen am Nordost- statt am Südwestende.
2. **Ein Körper statt zwei:** ein durchgehender Riegel mit Mittelrisalit und Portal, kein zweiter Pavillon.
3. **Drei Vollgeschosse** mit Sockel, Treppenhausrisalit an der Rückseite, Dachgarten auf dem Anbau.
4. **Kleiner:** 61 m statt 105 m; Grundrisse frei nach österreichischen Richtwerten, nicht nach dem Original.
5. **Anderer Anbau:** Flachbau mit Holzlamellen und Vordach für die Rettung, keine Lüftungsaufbauten.
6. **Kein Jugendstil-Ornament**, keine Lisenen, keine Reliefs; Farben nach ART_BIBLE §2; keine Schrift und kein
   Logo am Haus (ART_BIBLE §6; der Name steht nur in der Oberfläche).
7. **Andere Umgebung:** kein Großcampus, dafür Park, Stadt-Kulisse im Tal und ein eigener Garten.

## Nächster Schritt (eigener Chat)

Fable (3D und Raumprogramm, CLAUDE.md „Modellwahl"): diese Datei zu einem Konzept ausarbeiten (Vorbild-Recherche mit Fotos,
Format, Mentoren je Dienst, Ton, Interaktionen, Themenliste, Raumprogramm,
Grundriss je Stock, Wege der Kapitel, Einführungstext, Drehbuch des Flugs, Lageplan), dann ein Blender-Blockout
des Gebäudes und zwei Probe-Renders in niedriger Qualität (Außenansicht im Morgenlicht, ein Flur). Erst nach
Freigabe durch den Nutzer werden Räume ausgebaut.
