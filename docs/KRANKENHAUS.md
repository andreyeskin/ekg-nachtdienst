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

## Konzept (19.10.2026): Haus, Räume, Wege, Flug

Gilt für den Blender-Blockout (`gen/blender/`). Alle Maße in Metern, Achsmaße (Wandmitten); Außenwände 0,45 m,
Innenwände 0,15 m liegen innerhalb der Rechtecke. Medizinische Inhalte stehen hier nicht, nur Raumfunktionen.

### 1. Name des Hauses und der Stadt

| | Vorschlag | Prüfung (Suche 19.10.2026) |
|---|---|---|
| Haus, erster Vorschlag | Klinikum Hollerberg (Holler = Holunder; der Hang heißt im Spiel Hollerberg) | kein Krankenhaus dieses Namens gefunden |
| Haus, Alternative | Landeskrankenhaus Annabrunn | kein Treffer |
| **Haus, gewählt (19.10.2026)** | **Haus Föhrenhang** | kein Treffer |
| **Stadt, empfohlen** | **Annabrunn** (Hügel, Fluss, Dächer, nach dem Vorbild Graz, ohne Wahrzeichen) | nur ein Weiler in Bayern und eine Kapelle bei Leibnitz, keine Stadt |
| Stadt, Alternativen | Gradenfeld, Leonsbach | keine Treffer |

Im Spieltext: „Klinikum Hollerberg, Innere Medizin mit Kardiologie und Notaufnahme, Annabrunn". Am Haus selbst
keine Schrift (ART_BIBLE §6).

### 2. Das Haus in Zahlen

| Teil | Maß |
|---|---|
| Lokale Koordinaten | Ursprung: Südwestecke des Altbaus am Erdgeschossboden. **+x** läuft entlang des Riegels nach Nordost, **+y** quer nach Nordwest (Waldseite), **+z** nach oben. Der **Nordpfeil** zeigt in der Ebene auf (0,71 / 0,71), also diagonal zwischen +x und +y |
| Trakt A (Altbau) | x 0 … 61,2, y 0 … 16; drei Vollgeschosse; Mittelrisalit an der Südostseite x 25,2 … 36,0, y −3 … 0 (alle Geschosse, Quergiebel); Treppenhausrisalit an der Nordwestseite x 25,2 … 30,6, y 16 … 19 |
| Trakt N (Neubau) | x 61,2 … 85,2, y −6 … 18; zwei Geschosse, Flachdach mit Dachgarten; Vordach x 85,2 … 91,2, y −6 … 4, Unterkante z 3,6 |
| Geschosse | EG z 0, 1. OG z 4,0, 2. OG z 8,0 (Geschosshöhe 4,0 in beiden Trakten; Raumhöhe Altbau 3,4 wie in `docs/raeume/lehrsaal.md`, Neubau 3,0 plus Installationsraum) |
| Dach Altbau | Walmdach 30°, Traufe z 12,0, First z 16,6 (Firstlinie y 8), Dachüberstand 0,6; Quergiebel über dem Mittelrisalit (Sattel 30°, First z 16,6); Treppenhausrisalit mit kleinem Walm; drei Kamine auf dem First bei x 12, 30,6, 48 |
| Sockel | 0,6 m sichtbar an der Südostseite (Gelände dort z −0,6), an der Nordwestseite Gelände z 0 |
| Fensterachsen Altbau | 17 Achsen zu 3,6 m: Achse k deckt x 3,6·(k−1) … 3,6·k; Fenstermitte x = 3,6·k − 1,8 |
| Fenster Altbau | 1,4 breit, 2,2 hoch, Brüstung 0,9 (z Geschoss + 0,9 … + 3,1), Rahmen Petrol, Laibung 0,3 tief |
| Flur Altbau | y 7,0 … 10,0 (3,0 m) in allen Geschossen, x 0 … 61,2; Stirnfenster bei x 0 (y 7 … 10); Brandschutztür bei x 61,2 |
| Flur Neubau | y 7,0 … 10,0, x 61,2 … 85,2 (im EG ab x 66 in die Aufnahme geöffnet) |
| Treppen und Lifte | S1 Haupttreppe x 25,2 … 30,6, y 10 … 19 (alle Geschosse); L1 zwei Lifte (Betten 2,8 × 2,5 und Personen 1,6 × 2,0) x 30,6 … 36,0, y 10 … 13,5; S2 Fluchttreppe x 54 … 57,6, y 10 … 16; L2 Bettenlift x 57,6 … 61,2, y 10 … 13,5 (verbindet Notaufnahme, Herzkatheter und Intensiv); S3 Fluchttreppe Neubau x 61,2 … 66, y 14 … 18 |
| Türen | Zimmertüren 1,0 × 2,1 (Patientenzimmer 1,25 breit), Flurtüren zweiflügelig 1,8 × 2,1, Portal 3,0 × 3,2 mit Oberlicht, Rettungstor Schiebetür 3,0 × 2,8 |

### 3. Raumprogramm

Tageszeiten nach ART_BIBLE §4, Farben nach ART_BIBLE §2 (die drei beschriebenen Räume unverändert; die übrigen sind
Vorschläge, Rost-Objekt je Raum bleibt bei der Fallakte).

| Raum | Trakt, Geschoss | Maße (m) | Kapitel | Dienst, Zeit | Hauptkombination (Wand / Sockel / Boden) |
|---|---|---|---|---|---|
| Lehrsaal | A, EG | 10,8 × 7,0 | 0 | Einschulungstag 08:10 | Papier / Mint / Linoleum warm |
| Aufnahme (Notaufnahme: Tresen, Kojen 1–3, EKG-Wagen) | N, EG | 19,2 × 16,0 | 1 | Dienst 1, 06:40 | Sand / Mint / Linoleum warm |
| Monitorzimmer (Überwachung, 4 Betten, Zentrale am Fenster) | A, 1. OG | 10,8 × 6,0 | 2 | Dienst 1, 09:15 | Mint hell / Sand / Linoleum kühl |
| Patientenzimmer 104 (2 Betten) | A, 1. OG | 3,6 × 7,0 | 3 | Dienst 2, 13:30 | Sand / Mint / Linoleum warm; Vorhänge Mint |
| Intensiv, Box 6 (2 Plätze) und Zentrale | A, 2. OG | 7,2 × 6,0 und 7,2 × 6,0 | 4 | Dienst 3, 18:50 | Mint hell / Petrol / Linoleum kühl |
| Chest Pain Unit (4 Plätze, Stützpunkt) und Herzkatheterlabor | N, 1. OG | 19,2 × 8,0 und 8,4 × 7,0 | 5 | Dienst 4, 10:00 | Papier / Petrol / Linoleum kühl; hartes Kunstlicht |
| Rhythmusambulanz, Untersuchungsraum (EKG, Ergometrie) | A, EG | 7,2 × 7,0 | 6 | Dienst 5, 15:00 | Sand / Holz / Linoleum warm |
| Aufwachraum / Überwachung Innere (4 Betten) | A, 2. OG | 10,8 × 7,0 | 7 | Dienst 6, 22:10 | Mint hell / Sand / Linoleum kühl; nur Lampeninseln |
| Befundraum (Arztzimmer Oberarzt, im Erker) | A, 2. OG | 5,4 × 10,0 | 8 | Nachtdienst 02:14 | Papier / Holz / Linoleum warm; Regen am Erkerfenster |
| Eingangshalle mit Portier | A, EG | 10,8 × 13,0 | Flug, Wege | morgens | Sand / Mint / Linoleum warm |
| Rettungsvorfahrt mit Vordach, Triage-Schleuse | N, EG, außen | 6,0 × 10,0 und 15,2 × 4,0 | Flug, 1, 5 | 06:40, 10:00 | Papier / Petrol; Holzlamellen |
| Flure | A und N, alle | 3,0 breit | Wege | je Kapitel | Altbau Sand / Mint; Neubau Papier / Petrol |
| Treppenhaus S1 | A, Risalit NW | 5,4 × 9,0 | Wege | je Kapitel | Sand / Holz (Handlauf) |
| Lifte L1, L2 | A | 2,8 × 2,5 | Wege | je Kapitel | Petrol / Tinte (Glas) |
| Stützpunkt Station 1 (im Erker) | A, 1. OG | 5,4 × 10,0 | 2, 3 | Dienst 1 und 2 | Sand / Holz |
| Dienstzimmer Ärzte (Station 1; Nachtdienst neben dem Befundraum) | A, 1. und 2. OG | 5,4 × 7,0 | 3, 8 | tags, nachts | Papier / Holz |
| Cafeteria / Aufenthalt mit Terrasse | A, EG | 14,4 × 6,0 | Atmosphäre | mittags, Kapitel 3 | Papier / Holz / Linoleum warm |
| Garten im Gebäudewinkel | außen | 25 × 18 | Atmosphäre, Flug | morgens | Grün, Holzbank, Kastanie |
| Dachgarten Trakt N | N, Dach z 8 | 24 × 24 | Atmosphäre, 4 | abends | Grün, Hochbeete |
| Umkleide Studierende (Spind der Spielerin) | A, EG | 3,6 × 6,0 | 1 (Auftakt) | 06:35 | Sand / Petrol (Spinde) |
| Schockraum, Dienstzimmer Notaufnahme, Wartebereich | N, EG | 8,8 × 8,0 u. a. | Kulisse | 06:40 | Papier / Petrol |
| Patientenzimmer 101–118, 201–207 (Kulisse, Leben) | A, 1. und 2. OG | 3,6 × 7,0 bzw. 3,6 × 6,0 | Leben | je Kapitel | wie 104 |

Sonnenprüfung der Zeiten: Südostfassade (y = 0) bekommt die Morgensonne (06:40, 08:10, 09:15), um 13:30 streift
sie flach (Kapitel 3), abends ist sie im Schatten; das Abendrot (18:50, Kapitel 4) kommt durch die
Nordwestfenster der Intensivbox 6, deshalb liegt sie auf der Waldseite. Die Notaufnahme hat ihre Fensterfront nach
Nordost (x = 85,2): Sonnenaufgang schräg durch die Scheiben, wie ART_BIBLE §4 für Kapitel 1 verlangt.

### 4. Grundrisse je Geschoss

Rechtecke als (x0, y0, x1, y1). Türen: Wand und Lage. Fenster: Achsen nach §2. „Spiel" markiert Räume mit Kamera.

#### Erdgeschoss (z 0)

| Raum | x0 | y0 | x1 | y1 | Tür | Fenster |
|---|---|---|---|---|---|---|
| Lehrsaal (Spiel) | 0 | 0 | 10,8 | 7 | Flurwand y 7 bei x 9,8 | SE Achsen 1–3 (die „Rückwand" aus `lehrsaal.md` ist die Südostfassade) |
| Garderobe / Nebenraum Lehre | 10,8 | 0 | 14,4 | 7 | y 7 bei x 12,6 | SE Achse 4 |
| Ambulanz Innere, Vorbefund (Kulisse) | 14,4 | 0 | 21,6 | 7 | y 7 bei x 16 | SE Achsen 5–6 |
| Portier | 21,6 | 0 | 25,2 | 7 | offen zur Halle (x 25,2, Fenster mit Tresen) | SE Achse 7 |
| Eingangshalle (Spiel: Flug) | 25,2 | −3 | 36 | 10 | Portal y −3, x 29,1 … 32,1; Windfang y −3 … −0,5; nach beiden Seiten in den Flur offen | Risalit SE: Portal Achse 9, Fenster Achsen 8 und 10 (hoch, 1,4 × 2,8) |
| Rhythmusambulanz, Anmeldung und Warten | 36 | 0 | 39,6 | 7 | y 7 bei x 37,8 (Glastür) | SE Achse 11 |
| Rhythmusambulanz, Untersuchung (Spiel) | 39,6 | 0 | 46,8 | 7 | y 7 bei x 41; Verbindungstür zum Arztzimmer x 46,8 | SE Achsen 12–13 |
| Rhythmusambulanz, Arztzimmer | 46,8 | 0 | 50,4 | 7 | y 7 bei x 48 | SE Achse 14 |
| Holter / Ergometrie (Kulisse) | 50,4 | 0 | 54 | 7 | y 7 | SE Achse 15 |
| Sanitär Besucher | 54 | 0 | 57,6 | 7 | y 7 | SE Achse 16 (Milchglas) |
| Lager | 57,6 | 0 | 61,2 | 7 | y 7 | SE Achse 17 |
| Sekretariat Lehre / Verwaltung | 0 | 10 | 7,2 | 16 | y 10 bei x 2 | NW Achsen 1–2 |
| Umkleide Studierende | 7,2 | 10 | 10,8 | 16 | y 10 bei x 9 | NW Achse 3 |
| Technik / Lager | 10,8 | 10 | 18 | 16 | y 10 | NW Achsen 4–5 |
| Sozialraum | 18 | 10 | 25,2 | 16 | y 10 bei x 20 | NW Achsen 6–7 |
| Treppenhaus S1 | 25,2 | 10 | 30,6 | 19 | zur Halle y 10 (zweiflügelig) | Risalit NW: zwei hohe Fenster 1,2 × 4,0 bei x 28, z 2 … 6 und 6 … 10 |
| Lifte L1 | 30,6 | 10 | 36 | 13,5 | Türen y 10 zur Halle | keine (Blindfeld NW) |
| Technik Lift / Lager | 30,6 | 13,5 | 36 | 16 | von S1 | keine |
| Cafeteria / Aufenthalt | 36 | 10 | 50,4 | 16 | y 10 bei x 40 (Glastür); Terrassentür y 16 bei x 45 | NW Achsen 11–14 |
| Küche / Ausgabe | 50,4 | 10 | 54 | 16 | zur Cafeteria x 50,4 | NW Achse 15 |
| Fluchttreppe S2 | 54 | 10 | 57,6 | 16 | y 10 | NW Achse 16 |
| Bettenlift L2 | 57,6 | 10 | 61,2 | 13,5 | y 10 | keine |
| Flur EG | 0 | 7 | 61,2 | 10 | Brandschutztür x 61,2 | Stirnfenster x 0 |
| Trakt N: Flurfortsetzung | 61,2 | 7 | 66 | 10 | Glastür x 66 in die Aufnahme (mindestens 1,8 breit, Seitenscheibe) | keine |
| Wartebereich Notaufnahme | 61,2 | 10 | 66 | 14 | offen zum Flur | NW Band |
| Fluchttreppe S3 | 61,2 | 14 | 66 | 18 | y 14 | NW Band |
| Vorraum Schockraum | 61,2 | 2 | 66 | 7 | offen zum Flur | keine |
| Schockraum | 61,2 | −6 | 70 | 2 | Schiebetür y 2 (zur Aufnahme, x 67), Tür x 70 (zur Triage) | SE Oberlichter z 2,2 … 3,0 |
| **Aufnahme (Spiel)** | 66 | −2 | 85,2 | 14 | Glastür x 66 (Flur, links hinten vom Tresen aus), Glastür y −2 bei x 76 … 78 (Triage, hier gehen Rettung und Reinigung vorbei), Schiebetür zum Schockraum | NE Fensterfront x 85,2, y 2 … 12, z 0 … 3,0 (Jalousien); Holzlamellen außen |
| darin: Tresen | 67 | 10 | 72 | 13 | | Holz, 1,05 hoch, Lampe, Telefon, kleiner Drucker |
| darin: Monitorkojen 1 und 2 | 72 | 10 | 78,6 | 14 | Vorhänge an Deckenschiene | außerhalb des Bildes (links hinter dem Tresen) |
| darin: Koje 3, ohne Monitor | 80 | −2 | 85,2 | 2 | Vorhang halb zu | rechts hinten im Bild; Liege, Besuchersessel, Wandarm mit Blutdruckgerät |
| darin: EKG-Wagen (eigene Ebene) | 78 | 9 | 78,6 | 9,5 | | zwischen Tresen und Koje an der NW-Wand |
| Triage / Rettungsschleuse | 70 | −6 | 85,2 | −2 | Rettungstor x 85,2 (y −5 … −2), Glastür y −2 | NE Seitenlicht |
| Dienstzimmer Notaufnahme | 66 | 14 | 72 | 18 | y 14 | NW Band |
| Medikamente / Arbeitsraum | 72 | 14 | 79 | 18 | y 14 | NW Band |
| Sanitär / Umkleide | 79 | 14 | 85,2 | 18 | y 14 | NW Band |
| Vorfahrt Rettung (außen) | 85,2 | −6 | 91,2 | 4 | Vordach z 3,6 auf zwei Petrol-Stützen | |

```
EG   (1 Zeichen ≈ 1,8 m in x; Zeilen ≈ 2 m in y; NW oben, SE unten)
y19        ┌S1┐                                   Garten ──┐
y16 ┌Sekr┬Umkl┬Tech┬Sozial┬S1 ┬L1┬Lg┬Cafeteria/Aufenth┬Kü┬S2┬L2┐┬Wart┬S3───┬DienstNA┬Medik┬Sanit┐
y10 ├────┴────┴────┴──────┴───┴──┴──┴─────────────────┴──┴──┴──┤│    │     ├────────┴─────┴─────┤
     Flur ───────────────────────── Halle ──────────────────────▶ Glastür ▶  AUFNAHME  Kojen 1-2  │
y7  ├────┬────┬──────┬──┬ Halle ┬Warte┬Rhythmus┬Arzt┬Holt┬WC┬Lg┤│Vorr│     Tresen         Wagen   │ x85,2
y0  │Lehr│Gard│Ambul │Po│       │     │ambulanz│    │    │  │  ││Schock-│ Bank      Koje 3  Fenster│NE
    └────┴────┴──────┴──┤Portal ├─────┴────────┴────┴────┴──┴──┘│raum   ├──────┬──────────────┤
y-3                     └───────┘  Vorplatz                      └───────┤Triage│ Rettung ▶ Tor│ Vorfahrt
y-6                                                                      └──────┴──────────────┘ + Vordach
    x0        x10,8        x25,2    x36       x46,8        x61,2      x66        x78     x85,2  x91,2
```

#### 1. Obergeschoss (z 4,0): Station 1 (Kardiologie), Herzkatheter und Chest Pain Unit

| Raum | x0 | y0 | x1 | y1 | Tür | Fenster |
|---|---|---|---|---|---|---|
| Patientenzimmer 101–106 (je 2 Betten, Nasszelle 1,8 × 2,0 an der Flurwand) | 3,6·(k−1) | 0 | 3,6·k | 7 für k = 1 … 6 | y 7, je Zimmer bei x = 3,6·k − 0,7 (1,25 breit) | SE Achse k |
| **Patientenzimmer 104 (Spiel, Kapitel 3)** | 10,8 | 0 | 14,4 | 7 | y 7 bei x 13,7 | SE Achse 4; Betten quer zur Fensterwand, Fensterbett ist der Fall |
| Patientenzimmer 107 (1 Bett) | 21,6 | 0 | 25,2 | 7 | y 7 | SE Achse 7 |
| Stützpunkt Station 1 (im Erker) | 25,2 | −3 | 30,6 | 7 | offen zum Flur (Tresen an y 7) | Risalit SE Achse 8 und Erkerfenster |
| Dienstzimmer Ärzte Station 1 | 30,6 | 0 | 36 | 7 | y 7 bei x 34 | Risalit SE Achsen 9–10 |
| Patientenzimmer 108–112 | 36 | 0 | 54 | 7 | y 7 je Achse 11–15 | SE Achsen 11–15 |
| Bad / Sanitär Station | 54 | 0 | 57,6 | 7 | y 7 | SE Achse 16 (Milchglas) |
| Lager / unrein | 57,6 | 0 | 61,2 | 7 | y 7 | SE Achse 17 |
| Patientenzimmer 113–116 | 0 | 10 | 14,4 | 16 | y 10 je Achse 1–4 | NW Achsen 1–4 |
| Pflegearbeitsraum rein | 14,4 | 10 | 18 | 16 | y 10 | NW Achse 5 |
| Pflegearbeitsraum unrein | 18 | 10 | 21,6 | 16 | y 10 | NW Achse 6 |
| Wäsche / Lager | 21,6 | 10 | 25,2 | 16 | y 10 | NW Achse 7 |
| S1, L1, Lager | wie EG | | | | | |
| **Monitorzimmer (Spiel, Kapitel 2)** | 36 | 10 | 46,8 | 16 | y 10 bei x 37,5 (Glastür mit Seitenscheibe, vom Flur einsehbar) | NW Achsen 11–13 (kühles Nordwestlicht); vier Betten mit Kopf an der NW-Wand, Zentrale mit Monitorwand an der Wand x 46,8, Papier-Tisch auf Petrol-Blöcken, Holz-Aktenschrank |
| Patientenzimmer 117–118 | 46,8 | 10 | 54 | 16 | y 10 | NW Achsen 14–15 |
| S2, L2 | wie EG | | | | | |
| Flur 1. OG | 0 | 7 | 85,2 | 10 | Brandschutztür x 61,2 (Glas) | Stirnfenster x 0; am Ende x 85,2 ein Fenster nach NE |
| Trakt N: Technik | 61,2 | −6 | 66 | 7 | vom Flur | keine |
| Herzkatheterlabor, Untersuchungsraum (Spiel: Kulisse Kapitel 5) | 66 | −6 | 74,4 | 1 | Schleuse y 1 (Schiebetür) | keine (Lamellenwand SE) |
| Schaltraum | 74,4 | −6 | 78 | 1 | zur Schleuse | Bleiglasfenster zum Labor x 74,4 |
| Vorbereitung / Schleuse | 66 | 1 | 78 | 7 | y 7 (zweiflügelig) | keine |
| Arztzimmer Herzkatheter | 78 | −6 | 85,2 | 0 | y 0 | NE Band |
| Befundung / Umkleide | 78 | 0 | 85,2 | 7 | y 7 | NE Band |
| Warten / Angehörige | 61,2 | 10 | 66 | 14 | offen | NW Band |
| S3 | 61,2 | 14 | 66 | 18 | | |
| **Chest Pain Unit (Spiel, Kapitel 5)** | 66 | 10 | 85,2 | 18 | y 10 bei x 68 (Glastür) | NW Band y 18 (x 66 … 85,2, z 5,0 … 6,6); vier Plätze mit Monitor, Stützpunkt bei x 66 … 70 |

```
1. OG
y19        ┌S1┐                                   
y16 ┌113┬114┬115┬116┬rein┬unr┬Wä┬S1 ┬L1┬Lg┬ MONITORZIMMER ┬117┬118┬S2┬L2┐┬Wart┬S3──┬ CHEST PAIN UNIT (4 Plätze)┐
y10 ├───┴───┴───┴───┴────┴───┴──┴───┴──┴──┴───────────────┴───┴───┴──┴──┤│    │    ├───────────────────────────┤
     Flur ─────────────────────── Stützpunkt ──────────────────────────▶ Glas ▶ Flur ───────────────── Fenster NE
y7  ├101┬102┬103┬104┬105┬106┬107┬Stütz┬Dienstz┬108┬109┬110┬111┬112┬Bad┬Lg┤│Tech│Vorbereitung/Schleuse┬Befund│
y0  │   │   │ * │   │   │   │   │punkt│ Ärzte │   │   │   │   │   │   │  ││    ├────────┬───────┬────┤      │
    └───┴───┴───┴───┴───┴───┴───┤Erker├───────┴───┴───┴───┴───┴───┴───┴──┘│    │  HKL   │Schalt │Arzt│      │
y-3                             └─────┘                                   └────┴────────┴───────┴────┴──────┘ y-6
    x0          x10,8 (*104)    x25,2  x36                       x61,2  x66      x74,4   x78     x85,2
```

#### 2. Obergeschoss (z 8,0): Intensiv, Innere mit Aufwachraum, Befundraum

| Raum | x0 | y0 | x1 | y1 | Tür | Fenster |
|---|---|---|---|---|---|---|
| Patientenzimmer 201–203 (Innere, Kulisse) | 0 | 0 | 10,8 | 7 | y 7 je Achse 1–3 | SE Achsen 1–3 |
| **Aufwachraum / Überwachung Innere (Spiel, Kapitel 7)** | 10,8 | 0 | 21,6 | 7 | y 7 bei x 12 (zweiflügelig, Glas) | SE Achsen 4–6; nachts dunkel, nur Lampeninseln über den Betten |
| Stützpunkt Innere | 21,6 | 0 | 25,2 | 7 | offen zum Flur | SE Achse 7 |
| **Befundraum, Arztzimmer Oberarzt (Spiel, Kapitel 8)** | 25,2 | −3 | 30,6 | 7 | y 7 bei x 29 | Risalit SE Achse 8 und Erkerfenster (drei Scheiben, Blick auf die Stadt bei Nacht, Regen) |
| Dienstzimmer Nachtdienst | 30,6 | 0 | 36 | 7 | y 7 bei x 34; Verbindungstür zum Befundraum | Risalit SE Achsen 9–10 |
| Intensiv, Boxen 1–5 (je 1 Platz, Glaswände zum Flur) | 36 | 0 | 54 | 7 | Schiebetüren y 7 je Achse 11–15 | SE Achsen 11–15 |
| Sanitär / Technik Intensiv | 54 | 0 | 57,6 | 7 | y 7 | SE Achse 16 |
| Entsorgung | 57,6 | 0 | 61,2 | 7 | y 7 | SE Achse 17 |
| Patientenzimmer 204–207 (Innere, Kulisse) | 0 | 10 | 14,4 | 16 | y 10 je Achse 1–4 | NW Achsen 1–4 |
| Pflegearbeitsraum | 14,4 | 10 | 18 | 16 | y 10 | NW Achse 5 |
| Lager | 18 | 10 | 21,6 | 16 | y 10 | NW Achse 6 |
| Arztzimmer Innere | 21,6 | 10 | 25,2 | 16 | y 10 | NW Achse 7 |
| S1, L1, Lager | wie EG | | | | | |
| Intensiv, Zentrale (Spiel: Blick aus Box 6) | 36 | 10 | 43,2 | 16 | offen zum Intensivflur | NW Achsen 11–12 |
| **Intensiv, Box 6 (2 Plätze; Spiel, Kapitel 4)** | 43,2 | 10 | 50,4 | 16 | Schiebetür y 10 bei x 45 (Glas) | NW Achsen 13–14: Abendrot durch die Bäume, lange Schatten über die Betten |
| Angehörigenraum | 50,4 | 10 | 54 | 16 | y 10 | NW Achse 15 |
| S2, L2 | wie EG | | | | | |
| Flur 2. OG | 0 | 7 | 61,2 | 10 | Intensivschleuse: zweiflügelige Glastür quer im Flur bei x 36; Tür zum Dachgarten x 61,2 | Stirnfenster x 0 |
| Dachgarten Trakt N (außen, z 8) | 61,2 | −6 | 85,2 | 18 | vom Flurende | Attika 1,1 m, Hochbeete, zwei Bänke, zwei Felsenbirnen in Kübeln |

```
2. OG
y19        ┌S1┐                                   
y16 ┌204┬205┬206┬207┬Pfl┬Lg┬Arzt┬S1 ┬L1┬Lg┬ Zentrale ┬ BOX 6 (*)┬Angeh┬S2┬L2┐
y10 ├───┴───┴───┴───┴───┴──┴────┴───┴──┴──┴──────────┴──────────┴─────┴──┴──┤   Dachgarten Trakt N
     Flur ───────────────────────────────────┤Schleuse├ Intensivflur ─────▶ Tür ▶ (z 8, Attika, Hochbeete)
y7  ├201┬202┬203┬ AUFWACHRAUM ┬Stütz┬BEFUND┬Dienstz┬B1┬B2┬B3┬B4┬B5┬San┬Ent┤
y0  │   │   │   │ Innere (4)  │Inn. │ RAUM │Nacht  │  │  │  │  │  │   │   │
    └───┴───┴───┴─────────────┴─────┤Erker ├───────┴──┴──┴──┴──┴──┴───┴───┘
y-3                                 └──────┘
    x0          x10,8        x21,6  x25,2  x36                      x61,2
```

### 5. Umgebung

| Element | Lage (lokal) | Beschreibung |
|---|---|---|
| Gelände | Terrasse 40 m um das Haus eben (z −0,6 an der SE-Seite); ab y −40 fällt der Hang nach Südost mit 6 % zum Parkweg und zur Klinikstraße; hinter dem Haus (y > 35) steigt der Waldhang mit 10 % | Hangterrasse über der Stadt, wie das Vorbild auf der Anhöhe |
| Vorplatz | x 20 … 41, y −3 … −20 | Pflaster in Papier, zwei Linden (Kronen Ø 9 m bei x 23 und x 38, y −12), Bänke, Fahrradständer; keine Beschilderung mit Text |
| Parkweg | von (30, −20) in zwei Kehren nach (60, −70) zur Haltestelle | Kies, Laternen alle 15 m, Hecken |
| Klinikstraße | x 100 … 106, y −80 … 40 (läuft im Spiel „von Süd nach Nord" entlang der Talseite) | Allee aus sechs Platanen, Bushaltestelle bei (103, −60), Zufahrt zur Vorfahrt bei y −6 … 4 |
| Rettungszufahrt | von der Klinikstraße nach (91, −1) unter das Vordach | Asphalt, Abstellfläche für zwei Rettungswagen x 91 … 100 |
| Parkplatz Personal | x 70 … 100, y 20 … 40 | hinter dem Neubau, von Hecken verdeckt |
| Garten im Gebäudewinkel | x 36 … 61, y 16 … 34 | Cafeteria-Terrasse y 16 … 20, Rasen, eine Kastanie (Ø 12 m bei 50 / 27), zwei Holzbänke, Rosenbeet in Rost nur im Finale-Epilog (Rost-Regel: ein Objekt pro Bild) |
| Waldtor | (48, 34) | zwei Putzpfeiler mit kleinem Ziegeldach, Holzlattentor, Weg in den Wald; frei nach Link 8 |
| Wald | y > 35, und x < −20 | Buchen und Föhren als Silhouettenbänder in Petrol und Papier (ART_BIBLE §2), drei Tiefenebenen |
| Stadt-Kulisse | jenseits y −120, Blick nach Südost und Süd | Flusstal, Dächer in Papier und Sand, zwei Kirchtürme (einer mit Zwiebelhaube), Hügel links und rechts; nur Bänder, keine Wahrzeichen |
| Sonne am Morgen | Azimut etwa 80° (Ostnordost), Höhe 6–8° um 06:40 Anfang April oder Anfang September (REDESIGN §8.1); in lokalen Koordinaten kommt das Licht aus Richtung (0,82 / −0,57), also von der Südost-Seite und vom Nordost-Ende | Die Südostfassade und die Glasfront der Notaufnahme liegen im Morgenlicht; die Linden werfen lange Schatten über den Vorplatz nach Nordwest. Blender-Sonne: Richtung des Lichts (−0,82 / 0,57 / −0,14), Farbe Morgenlicht `#F8E7BF` |

### 6. Wege der Kapitel (Kamerafahrten, 4–8 s, keine Laufwege)

| Kapitel | Start → Ziel | Kamerafahrt |
|---|---|---|
| 0 | Flug (§7) → Lehrsaal | letzte Einstellung des Flugs: durch die Lehrsaaltür, Übergang in die Spielkamera |
| 1 | Umkleide (Spind, 06:35) → Flur EG → Glastür → Aufnahme | Fahrt den EG-Flur entlang nach Nordost, Glastür geht auf, Schnitt auf die Aufnahme-Kamera |
| 1 → 2 | Aufnahme → Bettenlift L2 → Flur 1. OG → Monitorzimmer (Herr Baum fährt „nach oben") | Trage rollt durch die Glastür, Lift: Türen zu, Ziffer 1 leuchtet, Türen auf; Fahrt den Flur entlang bis zur Glastür des Monitorzimmers |
| 2 → Ende Dienst 1 | Monitorzimmer → Treppenhaus S1 → Vorplatz (Mittag) | Treppe abwärts, Portal, Vorplatz im Mittagslicht; Erzähler: Tageswechsel in einem Satz |
| 3 | Außenansicht mittags → Halle → L1 → Stützpunkt → Zimmer 104 | Haus von außen (13:30), Schnitt Halle, Lift, Fahrt am Stützpunkt vorbei nach Südwest, Zimmertür 104 |
| 4 | Außenansicht abends → L1 → Flur 2. OG → Intensivschleuse → Box 6 | Abendrot an der Fassade, Lift, Schleuse öffnet, Schwenk in die Box |
| 5 | Vorfahrt (Rettung kommt) → Triage → L2 → Flur 1. OG Neubau → Chest Pain Unit, dann Blick ins Herzkatheterlabor | Rettungswagen unter dem Vordach, Tor, Lift nach oben, Glastür CPU; später Schleuse zum Labor (Kulisse) |
| 6 | Halle → Flur EG nach Nordost → Rhythmusambulanz Warten → Untersuchung | Nachmittagslicht in der Halle, Flur, Glastür, Schwenk in den Untersuchungsraum |
| 7 | Außenansicht nachts (Fensterinseln) → L1 → Flur 2. OG (dunkel) → Aufwachraum | Nacht, nur Lampen, Lift, dunkler Flur, Glastür |
| 8 | Flur 2. OG (02:14) → Befundraum im Erker; Chefvisite: Befundraum → Flur → Rückblick der Räume im Querschnitt | Regen am Stirnfenster, Tür zum Befundraum; Finale als Folge von Standbildern aller Kapitel im Lageplan |

### 7. Drehbuch des Flugs (Einschulungstag, 07:55, etwa 40 s, überspringbar)

Bildfolge aus neun Renders mit Überblendung (0,6 s) und Parallaxe (drei Ebenen, 3–5 % Drift). Stimme: Dr. Wieser,
freundlich, kurz, duzt. Jede Zeile höchstens zwei Sätze (Stimmprofil in `docs/raeume/lehrsaal.md`). Die Sätze sind
Platzhalter für den Skill `dialoge`, Inhalt verbindlich: was, wie, wo.

| Nr. | Zeit | Kamera (lokal, Blick) | Bewegung | Dr. Wieser |
|---|---|---|---|---|
| 1 | 0–5 s | hoch über dem Tal, (120, −260, 60), Blick auf Stadt und Hang, das Haus rechts oben am Waldrand | langsames Heranfahren | „Guten Morgen. Das ist Annabrunn, und das Haus am Waldrand ist unseres: das Klinikum Hollerberg." |
| 2 | 5–10 s | Außenansicht wie Probe-Render (a), §9 | Drift nach rechts, Linden im Vordergrund wandern | „Innere Medizin mit Kardiologie. Hier lernst du in den nächsten Wochen, EKGs zu lesen, an echten Aufnahmen." |
| 3 | 10–14 s | Vorplatz vor dem Portal (30,6, −12, 1,6), Blick +y durch das Portal in die Halle | Fahrt durch das Portal | „Eine Rotation: mehrere Dienste, jeder Dienst ein Patient und eine Frage, die du beantwortest." |
| 4 | 14–18 s | Aufnahme, Spielkamera (§9, Raumkamera 1) | Überblendung, Jalousienlicht wandert | „Unten die Notaufnahme. Dein erster Dienst beginnt hier, morgen vor sieben." |
| 5 | 18–23 s | Flur 1. OG wie Probe-Render (b), dann Monitorzimmer | Fahrt den Flur entlang, Schnitt in das Monitorzimmer | „Erster Stock: die Station und das Überwachungszimmer. Wer hier liegt, hängt am Monitor, und du liest mit." |
| 6 | 23–27 s | Intensiv Box 6, dann Herzkatheterlabor durch die Schleuse | zwei kurze Standbilder | „Oben die Intensivstation, drüben das Herzkatheterlabor. Dort wird es später ernst." |
| 7 | 27–32 s | Nahaufnahme Schreibtisch im Lehrsaal: Zirkel, blaues Lineal, Befundmappe, Verdachtsliste als Zettel | leichtes Zoomen, die Mappe klappt auf (Oberfläche blendet ein) | „Deine Werkzeuge: Zirkel und Lineal zum Messen, die Mappe für deine Befunde, die Verdachtsliste zum Sortieren." |
| 8 | 32–36 s | Querschnitt des Hauses (§8), Räume leuchten in Kapitelfolge auf | Räume blenden nacheinander ein | „Der Knopf ‚Haus' zeigt dir jederzeit, wo du bist und was heute dran ist." |
| 9 | 36–40 s | Lehrsaaltür vom Flur (9,8, 8,5, 1,55), Blick −y, Tür geht auf, Jonas auf der Liege | Fahrt durch die Tür, Übergang in die Spielkamera des Lehrsaals | „Aber zuerst: Papier, Zacken, Zirkel. Komm rein." |

Technik: neun PNG-Paare (Hintergrund, Mittelgrund) aus demselben Blender-Modell, Einbettung über `gen/kunst.py`;
Tonspur entfällt in der Einzeldatei (Text als Untertitel in Dr. Wiesers Farbe), in der gehosteten Fassung Sprache
(TON.md §3). Ein Knopf „Überspringen" ab Sekunde 2.

### 8. Lageplan im Spiel (Knopf „Haus")

- **Was er zeigt:** einen Puppenhaus-Schnitt längs der x-Achse, Blick von Südost: drei Geschosse des Altbaus und
  zwei des Neubaus nebeneinander, Dach und Vordach als Umriss; jeder Spielraum eine Kachel an seinem Ort
  (Lehrsaal unten links, Aufnahme unten rechts, Monitorzimmer und Zimmer 104 in der Mitte, CPU rechts oben,
  Intensiv und Befundraum oben). Kopfzeile: „Dienst 1 · 06:40", Mentor des Tages als Porträt-Medaillon
  daneben. Rechts die Themenliste aus `docs/LEHRPLAN.md` (erledigt, heute, offen).
- **Zustände der Kacheln:** aktuell (Rahmen Rost, der einzige Rost im Bild), erledigt (Mint-Fläche mit Haken),
  heute offen (Papier mit Tinte-Linie), später (Sand ohne Linie). Antippen zeigt einen Satz (Raum, Dienst, Thema)
  und schließt wieder; kein Gehen, kein Laden (Leitsatz „Denken statt Gehen"). Nur wenn ein Kapitel ausdrücklich
  eine Wahl anbietet, ist eine zweite Kachel antippbar.
- **Aussehen:** ligne claire, Flächen Sand und Papier, Linie Tinte, kleine Figuren als Silhouetten, die sich
  zwischen Räumen bewegen (Leben); 1600 × 900 als Überlagerung, auf dem iPad quer bildfüllend. Dasselbe Bild dient
  als Einstellung 8 des Flugs und als Rückblick im Finale.

### 9. Probe-Renders für den Blockout und Raumkameras

| | Kamera (lokal) | Ziel | Brennweite, Sensor | Zeit, Licht | Warum |
|---|---|---|---|---|---|
| **(a) Außenansicht im Morgenlicht** | (−30, −62, 3,0) auf dem Parkweg, Blick nach Nordost | (34, 2, 7) | 35 mm, 36 mm Sensor, Objektivverschiebung statt Neigung (Vertikalen bleiben senkrecht), Bild 1600 × 900 | Dienst 1, 06:40, Sonne Azimut 80°, Höhe 7°, Farbe `#F8E7BF`; Himmel als drei Bänder (`#F8E7BF` → `#F6DCA4` → `#F3CD8C`) | zeigt Südostfassade mit Risalit und Portal, rechts den Neubau mit Vordach, dahinter den Wald, vorn die Linden; prüft Kubatur, Dach und Palette am Haus |
| **(b) Flur** | 1. OG, (24, 8,5, 1,55), Blick +x (Nordost) den Stationsflur entlang | (61, 8,5, 1,55) | 24 mm, keine Neigung | Dienst 1, 09:15, kühles Vormittagslicht; Sonne (Azimut 120°, Höhe 35°) fällt durch die offenen Zimmertüren rechts als Streifen auf den Boden; Fenster am Flurende | der meistgenutzte Weg (Kapitel 1→2, 3, Lift nach 4); links Lifttüren, Monitorzimmer-Glastür und Fenster der Zentrale, rechts Zimmertüren 108–112, Stützpunkt-Tresen am Bildrand ohne dunklen Anschnitt (ART_BIBLE §3.3); prüft Flurbreite, Türrhythmus, Sockelfarbe und ob Silhouetten (Leben) lesbar sind |

Raumkameras (alle Dreiviertelansicht, Verschiebung statt Neigung, 1600 × 900, Vorschlag für den Blockout):

| Raum | Kamera | Blick | Brennweite |
|---|---|---|---|
| 1 Aufnahme | (70, 4, 1,55) | +x auf Fensterfront, Tresen links, Koje 3 rechts | 28 mm |
| 2 Monitorzimmer | (38, 10,8, 1,55) | +y … +x diagonal auf Betten und Zentrale | 28 mm |
| 3 Zimmer 104 | (13,8, 6,6, 1,5) | −y zum Fenster, Fensterbett rechts | 28 mm |
| 4 Intensiv Box 6 | (45, 10,6, 1,55) | +y zum Fenster (Abendrot) | 28 mm |
| 5 Chest Pain Unit | (69, 10,8, 1,55) | +x entlang der Plätze, Fensterband links | 28 mm |
| 6 Rhythmusambulanz | (41, 6,6, 1,55) | −y zum Fenster, Liege links, Ergometer rechts | 28 mm |
| 7 Aufwachraum | (12, 6,6, 1,55) | −y, Lampeninseln | 28 mm |
| 8 Befundraum | (27, 6,5, 1,5) | −y in den Erker, Regen am Glas | 28 mm |
| 0 Lehrsaal | nach `docs/raeume/lehrsaal.md` §7, gedreht: Rückwand = Südostfassade | | 28 mm |

### 10. Mentoren je Dienst

Feste Figuren bleiben (ART_BIBLE §5, `lehrsaal.md`); drei neue Figuren nur als Vorschlag mit Fachgebiet und
Tagesthema. Stimmprofile und Dialoge später mit dem Skill `dialoge`; Fachinhalt je Fall über `fallakte`.

| Dienst | Kapitel | Mentor | Fachgebiet | Tagesthema (ein Satz) |
|---|---|---|---|---|
| Einschulungstag | 0 | Dr. Nora Wieser, 41 | Innere Medizin, EKG-Kurs | Messen statt schätzen: Papier, Zacken, Zirkel, Lagetyp. |
| Dienst 1 | 1 | Schwester Marlene, 54 (Pflege Notaufnahme); Dr. Falk kommt um 07:15 dazu | Notaufnahme | Erst der Patient, dann der Streifen: eine Synkope und ihr erstes EKG. |
| Dienst 1 | 2 | Oberarzt Dr. Falk, 61 | Kardiologie | Monitor gegen Papier: was der Monitor zeigt und was nur der Streifen beweist. |
| Dienst 2 | 3 | Schwester Marlene (Station 1, springt ein) | Station | Luftnot am Bett: der Streifen, der breit geworden ist. |
| Dienst 3 | 4 | **neu: Dr. Ruth Haidinger, 47** | Intensivmedizin (Innere) | Wenn ein Gerät den Takt gibt: Schrittmacher und lange QT auf der Intensivstation. |
| Dienst 4 | 5 | **neu: Dr. Stefan Pichler, 44** | Interventionelle Kardiologie, Herzkatheter | Druck auf der Brust: Minuten zählen und die Hebung erkennen. |
| Dienst 5 | 6 | **neu: Dr. Aylin Demir, 36** | Rhythmologie, Rhythmusambulanz | Herzrasen bei jungen Menschen: schmal oder breit, regelmäßig oder nicht. |
| Dienst 6 | 7 | Schwester Marlene (Überwachung Innere) | Innere Medizin | Nacht, vier Betten, vier Streifen: Sonderfälle mit Schema. |
| Nachtdienst | 8 | Oberarzt Dr. Falk | Chefvisite, Befundraum | Alles zusammen: drei Fragen, drei Belege, dann darf die Spielerin heim. |

Stützpersonen ohne Mentorenrolle: Jonas Prem (Tutor, Knopf „Kollegin fragen"), Portier, Andrea (Tagdienst
Notaufnahme, nur Silhouette).

## Offene Fragen an den Nutzer (nach der Ausarbeitung, 19.10.2026)

1. **Ein Foto von Gebäude 31** von der Talseite (Handy reicht, nicht ins Repository): Geschosszahl, Fensterform
   und Putzfarbe sind bisher aus dem Luftbild abgeleitet. Ohne Foto bauen wir nach §2 (drei Geschosse).
2. **Namen freigeben:** Klinikum Hollerberg in Annabrunn (oder eine der Alternativen in §1).
3. **Dachfarbe:** ein eigener Ziegelton in ART_BIBLE §2 (Vorschlag „Ziegel" `#C9795A`, gedeckt, nur außen) oder
   das Dach in Holz `#C99A5B`? Rost bleibt dem einen Objekt pro Bild vorbehalten.
4. **Neubau als Flachbau** mit Holzlamellen und Dachgarten für Notaufnahme und Herzkatheter: einverstanden, oder
   soll alles im Altbau liegen (dann entfällt die Rettungsvorfahrt am Kopfbau)?
5. **Raumfunktionen prüfen (Arztblick):** Monitorzimmer als Vier-Bett-Überwachung der Station, Aufwachraum als
   Überwachungszimmer der Inneren im 2. OG, Chest Pain Unit neben dem Herzkatheterlabor, Intensiv direkt darüber
   am Bettenlift. Außerdem die drei Mentorennamen (§10).

**Antworten des Nutzers (19.10.2026, nach der Ausarbeitung):**
1. Foto: keines; gebaut wird nach §2 (drei Geschosse, Walmdach, heller Putz).
2. Name: **Haus Föhrenhang** (statt Klinikum Hollerberg; der Hang heißt im Spiel Föhrenhang); Stadt bleibt
   vorerst Annabrunn.
3. Dach: **Ziegel `#C9795A`**, in ART_BIBLE §2 eingetragen (nur außen).
4. **Altbau plus Neubau** (Flachbau mit Holzlamellen und Dachgarten) wie in §2.
5. Mentorennamen und Raumfunktionen: **später** (bei der Arbeit an den Figuren); der Blockout folgt der Lage aus §3/§4.

## Nächster Schritt (eigener Chat)

Blender-Blockout nach §2 bis §5 (Skript in `gen/blender/`, z. B. `haus_blockout.py`: Hülle, Geschosse, Flure, Räume
als Quader aus den Tabellen, Treppen, Lifte, Dach, Gelände, Bäume als Platzhalter; glTF-Export mitdenken), dann die
beiden Probe-Renders nach §9 in niedriger Qualität. Erst nach Freigabe durch den Nutzer werden Räume ausgebaut
(Aufnahme B1 aus `docs/REDESIGN_FALL1.md` §8.3 als erster Raum des Hauses, danach Lehrsaal und Monitorzimmer
in das Haus übernehmen).
