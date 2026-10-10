# Spielkonzept — „Nachtdienst"

Lernspiel zum EKG. Eine Schicht, ein Patient, viele Wege. Der Spieler lernt, weil er
Entscheidungen treffen muss, nicht weil er Text liest.

## 1. Die Grundidee

Du bist KPJ-Student in deiner ersten eigenständigen Schicht. **Herr Konrad Baum, 68**, kommt
morgens zu Fuß in die Aufnahme: zweimal kurz bewusstlos geworden, beide Male im Stehen, keine
Vorwarnung. Niemand weiß warum. Bis zum Ende der Schicht sollst du sagen können, was sein Herz
macht — und es belegen.

Der Fall ist medizinisch echt aufgebaut: Synkopen bei intermittierender Überleitungsstörung.
Die Beweiskette führt über Rhythmus → Überleitung → Pausen → Lokalisation des Blocks.

## 2. Struktur: ein Rückgrat, viele Abzweigungen

Linear ist nur die **Zeit** (die Schicht läuft von 06:40 bis 02:14) und das **Ziel** (die
Diagnose). Alles dazwischen ist offen.

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
der Anamnese, ein altes EKG aus dem Archiv. Jeder Befund ist eine Karte mit echtem Bild aus der
Engine. Zwei Karten lassen sich **nebeneinanderlegen und vergleichen** — das ist der zentrale
Denkvorgang beim EKG und damit die zentrale Spielmechanik.

## 4. Mini-Spiele: raus aus dem Flur, rein in den Körper

Sie starten aus der Situation heraus, nicht aus einem Menü. Jedes dauert ein bis drei Minuten.

| Auslöser | Mini-Spiel | Was man dabei lernt |
|---|---|---|
| Du misst zum ersten Mal | **Zirkel** — PQ, QRS, QT am echten Streifen abgreifen; die Experten­markierung aus der Datenbank prüft auf die Millisekunde | Messen statt schätzen |
| Marlene zeigt dir das Schema | **Reizleitung bauen** — Sinusknoten, AV-Knoten, His, Schenkel in ein Herz setzen und den Impuls laufen lassen; falsch gesetzt = falsches EKG unten im Streifen | Anatomie → Kurve |
| Herr K. wird blass | **Ampelspiel am Monitor** — innerhalb von Sekunden entscheiden: beobachten, Arzt rufen, Pacer | Dringlichkeit |
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
