# Spielkonzept — „Nachtdienst"

Lernspiel zum EKG. Eine Rotation, viele Patienten, echte Kurven. Der Spieler lernt, weil er
Entscheidungen treffen muss, nicht weil er Text liest.

**Zweite Fassung (11.10.2026):** Die Grundsätze, der Zeitrahmen, der Ablauf und der Fallkatalog stehen in
`docs/KONZEPT.md`; dieses Blatt behält die Mechaniken, die warmen Räume, die Anspielungen und die
technischen Grundsätze. Wo beide Blätter sich widersprächen, gilt `KONZEPT.md`.

## 1. Die Grundidee

Du bist Famulantin/KPJ-Studentin in deiner ersten Rotation. Jeder Dienst hat seine Abteilung und
seine eigenen Patienten, und jeder Patient trägt genau eine Lektion oder Diagnose (`KONZEPT.md` §1).
Es beginnt im Lehrsaal (Einschulung, Lektionen 1–7) und führt über Aufnahme, Monitorzimmer, Station,
Intensiv, Herzkatheter und Rhythmusambulanz bis zum Nachtdienst im Befundraum. Was dich durch alle
Dienste trägt, sind die Menschen des Hauses — Marlene, Dr. Falk, Dr. Wieser — und deine Befundmappe.

Der erste Patient, **Herr Konrad Baum, 68**, kommt am ersten Frühdienst zu Fuß in die Aufnahme:
zweimal kurz bewusstlos geworden, beide Male im Stehen, keine Vorwarnung. Sein Fall ist die
Synkopen-Abklärung mit einem EKG, das Sinusrhythmus, langsam, und einen AV-Block I° zeigt — und
nicht mehr (`docs/faelle/aufnahme_baum.md`).

## 2. Struktur: ein Rückgrat, viele Abzweigungen

Linear sind nur die **Zeit** (innerhalb eines Dienstes läuft die Uhr weiter; die Dienste folgen
aufeinander) und das **Ziel** jedes Falls (der Befund). Alles dazwischen ist offen.

```
          ┌── Monitorzimmer ──┐        ┌── Intensiv ──┐
Aufnahme ─┤                   ├─ Station ─┤            ├─ Finale: Chefvisite
          └── Labor/Archiv ───┘        └── Aufwachraum ┘
```

**Regeln der Nichtlinearität**
- Jeder Raum ist jederzeit betretbar, sobald er freigeschaltet ist. Reihenfolge frei.
- Für den nächsten Abschnitt braucht man **zwei von drei** Beweisstücken — nie alle.
  Wer anders denkt, geht einen anderen Weg und bekommt eine andere Szene.
- Jede Figur reagiert darauf, was du schon weißt. Fragst du Marlene nach der Pause, bevor du
  sie gemessen hast, antwortet sie anders als danach.
- Es gibt **kein Game Over**. Falsche Schlüsse kosten Zeit (die Uhr springt) und erzeugen eine
  Szene, in der jemand dich korrigiert — meist Dr. Falk, trocken und ohne Belehrung.

## 3. Inventar als Wissen

Gesammelt werden keine Schlüssel, sondern **Befunde**: ein Streifen, eine Messung, ein Satz aus
der Anamnese, ein altes EKG aus dem Archiv. Befunde entstehen im normalen klinischen Ablauf
(Anamnese, Aufnahmebogen, Vitalzeichen, Untersuchung, EKG) — nie durch das Finden eines versteckten
Gegenstands (`KONZEPT.md` §1.3). Jeder Befund ist eine Karte mit echtem Bild aus der
Engine. Zwei Karten lassen sich **nebeneinanderlegen und vergleichen** — das ist der zentrale
Denkvorgang beim EKG und damit die zentrale Spielmechanik.

## 4. Mini-Spiele: raus aus dem Flur, rein in den Körper

Sie starten aus der Situation heraus, nicht aus einem Menü. Jedes dauert ein bis drei Minuten.

| Auslöser | Mini-Spiel | Was man dabei lernt |
|---|---|---|
| Du misst zum ersten Mal | **Zirkel** — PQ, QRS, QT am echten Streifen abgreifen; die Experten­markierung aus der Datenbank prüft auf die Millisekunde | Messen statt schätzen |
| Dr. Wieser zeigt das Whiteboard (Lehrsaal) | **Reizleitung bauen** — Sinusknoten, AV-Knoten, His, Schenkel in ein Herz setzen und den Impuls laufen lassen; falsch gesetzt = falsches EKG unten im Streifen | Anatomie → Kurve |
| Der Monitor von Frau Lindner alarmiert | **Ampelspiel am Monitor** — innerhalb von Sekunden entscheiden: beobachten · bleiben, Arzt rufen, 12-Kanal-EKG · Notfallteam | Dringlichkeit, Grenzen des Monitors |
| Kein Patient, nur Elektroden | **Elektroden kleben** (Lehrsaal) — vier Klemmen nach der Ampel-Regel, sechs Brustwandelektroden an ihren Platz | Ableitungen |
| Nachtruhe, Archiv | **Karten vergleichen** — altes EKG gegen neues, Unterschied finden | Verlaufsbeurteilung |
| Dr. Falk erklärt den Block | **Leiterdiagramm legen** — Linien im A-AV-V-Diagramm so setzen, dass sie zum Streifen passen | Mechanismus |
| Finale | **Chefvisite** — drei Fragen, Antworten müssen mit deinen Befunden belegt werden | Argumentieren |

## 5. Was den Spieler bei der Stange hält

- **Jeder Raum hat ein Geheimnis**, das nichts mit dem Fall zu tun hat: Marlenes Katzensticker,
  Falks nie angezündete Zigarette, die Zeichnung am Schrank. Wer fragt, bekommt eine kleine Szene.
- **Die Uhr** oben rechts läuft weiter. Nicht als Stress, sondern als Erzählung: Licht und
  Geräusche verändern sich, Figuren werden müder.
- **Kein Fortschrittsbalken.** Stattdessen die Befundmappe, die sichtbar dicker wird.
- **Wiederspielwert**: Die Engine zieht die Streifen jedes Mal aus einem anderen echten Datensatz
  derselben Diagnosegruppe. Der Fall bleibt, die Kurven sind neu.

## 5a. Räume, die nichts beibringen

Ein Haus, in dem jeder Raum eine Aufgabe hat, ist kein Haus, sondern ein
Fragebogen mit Tapete. Deshalb gibt es **warme Räume**: Orte, an denen man
nichts lernt, nichts sammelt und nichts freischaltet.

- **Teeküche.** Der Automat macht nur noch halbe Tassen, seit jemand im Februar
  etwas hineingeschüttet hat. Im Kühlschrank steht eine Dose mit einem Zettel
  drauf. An der Tür hängt eine Dankeskarte von Angehörigen, ohne Namen.
- **Hinterausgang.** Dr. Falks nie angezündete Zigarette. Kalte Luft. Er sagt
  genau einen Satz, der nichts mit Herzen zu tun hat.
- **Lager.** Ein EKG-Gerät aus den Achtzigern, in dem noch Papier steckt. Ein
  Rollstuhl mit einem Aufkleber, den ein Kind daraufgeklebt hat.
- **Treppenhaus.** Die Abkürzung, die alle nehmen. Ein Fenster, an dem man
  sieht, wie die Tageszeit weitergeht.
- **Stilles Zimmer.** Nichts passiert. Genau darum geht es.

**Regeln, damit sie warm bleiben:**

1. **Nie Pflicht.** Kein Fortschritt hängt daran, kein Befund liegt dort.
2. **Nie in der Liste.** Der „Stand der Schicht" erwähnt sie nicht. Wer sie
   findet, findet sie.
3. **Nie belohnt.** Keine Punkte, keine Abzeichen. Die Szene ist die Belohnung.
4. **Sie kosten Zeit** — und das ist richtig so. Wer sich fünf Minuten hinsetzt,
   hat fünf Minuten weniger. Niemand bestraft einen dafür.
5. **Sie verändern sich mit der Schicht.** Morgens riecht die Teeküche nach
   Kaffee, nachts steht die Kanne kalt da. Die Tassen auf Marlenes Tisch werden
   mehr. Falks Zigarette wandert zwischen Ohr und Hand.
6. **Wer zweimal kommt, bekommt mehr.** Figuren erzählen beim zweiten Mal etwas,
   das sie beim ersten Mal nicht erzählt haben — nichts Dramatisches, eher
   warum jemand immer dieselbe Tasse nimmt.

## 5b. Anspielungen — auf uns selbst, nicht auf andere

Kleine Wiedererkennungen machen eine Welt lebendig. Sie kommen aber **aus
unserer eigenen Welt**, nicht aus fremden Filmen, Serien oder Spielen: deren
Namen und Figuren sind geschützt, und ein geborgter Witz altert schlecht.

Was funktioniert:
- **Dinge kehren wieder.** Der verblasste Katzensticker auf Marlenes
  Namensschild. Das rote Fadenbändchen der Enkelin, das später in einem ganz
  anderen Kapitel auf einer Kinderzeichnung auftaucht.
- **Figuren erinnern sich.** Wer Herrn Baum nach dem Foto gefragt hat, wird beim
  nächsten Treffen gefragt, ob er noch weiß, wie das Mädchen heißt.
- **Das Haus altert.** Der schiefe Bilderrahmen im Flur hängt im letzten Kapitel
  immer noch schief.
- **Ein Insiderwitz pro Abteilung**, aus dem Fach selbst: die Kaffeekasse, die
  jemand mit einem EKG-Lineal bewacht; der Spruch über Ableitung aVR, den jede
  Station anders erzählt.

Was nicht: Zitate aus Serien, Namen aus anderen Spielen, nachgebaute Figuren,
Markennamen auf Geräten.

## 6. Technische Grundsätze

- Eine Webseite, später PWA. Kein Spiel-Framework: SVG und Canvas reichen und bleiben leicht.
- **Alle EKG-Kurven kommen aus echten Aufnahmen** (LUDB, PTB-XL) und werden auf echtem
  Millimeterpapier gezeichnet: 25 oder 50 mm/s, 10 mm/mV, Eichzacke.
- Jede Messaufgabe hat eine **geprüfte Wahrheit** aus den Experten-Annotationen der Datenbank.
- Fortschritt lokal; in Moodle über SCORM, wenn gewünscht.
- Text ausschließlich aus dem Code, nie im Bild.

## 7. Offen — beim nächsten Mal besprechen

- Anatomie-Quellen für das Herz-Mini-Spiel (Andrey und Claude entscheiden gemeinsam).
- Vertonung: Umgebungsgeräusche und Stimmen, voraussichtlich ElevenLabs.
- Umfang Kapitel 2 bis 6: wie viele Räume wirklich gebaut werden.
