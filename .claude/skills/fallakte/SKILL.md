---
name: fallakte
description: Einen Patientenfall für „Nachtdienst" fachlich wie ein erfahrener Arzt durcharbeiten — Leitsymptom, Differenzialdiagnosen samt der Fragen, die jede Ärztin sofort stellen würde (z. B. „Ist das nicht eine TIA?"), Rolle und Grenzen des EKG, passende echte Aufnahme, Belege. Immer laden, bevor ein neuer Fall, ein neues Kapitel oder neue Fachinhalte gebaut oder ein bestehender Fall überarbeitet wird.
license: Projektinhalt
---

# Fallakte — ein Fall, wie ihn ein Arzt durchdenkt

Jeder Fall im Spiel gehört zu **einer Lektion oder einer Diagnose** und hat **seinen eigenen Patienten**.
Bevor ein Satz Dialog entsteht, liegt die Fallakte unter `docs/faelle/<id>.md` vor und ist gegen das
Lehrbuch (Kapitel-PDFs im Drive des Nutzers, nie ins Repository) und docs/QUELLEN.md geprüft.

## 1. Aufbau der Fallakte (alle Abschnitte Pflicht)

1. **Lernziel** — was die Spielerin danach am EKG kann (ein Satz, prüfbar), Lektion(en).
2. **Aufnahme** — Datensatz aus `data/` (LUDB mit Wellen-Annotation, wenn gemessen wird; PTB-XL nur
   zum Ansehen, `"messbar": false`). Etikett der Datenbank, eigene Nachrechnung der Kernzahlen,
   Abweichungen vom Lehrbuch (FACHREGELN „Datenbank-Etiketten").
3. **Patient** — Alter, Situation, ein persönlicher Gegenstand, Laiensprache; nichts, was der Aufnahme
   widerspricht (Alter/Geschlecht aus der Datenbank, wo vorhanden).
4. **Leitsymptom und Differenzialdiagnosen** — Tabelle: Diagnose · spricht dafür · spricht dagegen ·
   welche Frage/Untersuchung trennt · Rolle des EKG. Immer mit den **„Must-not-miss"**-Diagnosen.
   Hier gehören die Fragen hin, die jede Ärztin reflexhaft stellt — und die das Spiel deshalb als
   Antwortoption anbieten muss. Beispiel Synkope: echter Bewusstseinsverlust oder nicht? Synkope
   (reflektorisch, orthostatisch, kardial) gegen nicht-synkopale Ursachen (Krampfanfall, psychogen,
   TIA/Schlaganfall, Hypoglykämie, Intoxikation) — mit Beleg, warum etwas wahrscheinlich ist oder nicht.
5. **Anamnese-Fragen** — was die Spielerin fragen kann und was der Patient (in Laiensprache) antwortet;
   welche Antwort welche DD stützt oder schwächt.
6. **EKG-Aufgabe** — was gemessen oder erkannt wird, Toleranzen, häufigste Fehler und deren Rückmeldung.
7. **Was das EKG sagt — und was nicht.** Grenzen ausdrücklich (z. B. ein normales Ruhe-EKG schließt
   eine rhythmogene Synkope nicht aus).
8. **Ende des Falls und Behandlung** — was mit dem Patienten geschieht, einschließlich Therapie (Medikamente
   mit Dosierung, Eingriffe); Behandlungsentscheidungen dürfen Aufgaben der Spielerin sein. Jede Aussage
   belegt (Leitlinie mit Abschnitt, QUELLEN §4).
9. **Belege** — je Aussage: Lektion (eigene Worte) bzw. offene Quelle (Leitlinie mit Abschnitt/Tabelle).
   Was nicht belegt ist, kommt nicht ins Spiel.

## 2. Regeln

- **Ein Patient, ein Lernziel.** Kein Patient trägt Stoff, den seine Aufnahme nicht zeigt.
- **Eindeutigkeit:** Die richtige Antwort muss aus Aufnahme und Anamnese **zwingend** folgen; jede
  falsche Option muss mit einem konkreten Merkmal widerlegbar sein. Fangfragen, die je nach Quelle
  richtig oder falsch sind, sind verboten (z. B. „Sinusbradykardie" bei 53/min).
- **Experten-Reflex:** Lies die Akte als Oberärztin. Welche Frage würdest du als Erstes stellen?
  Steht sie als Option drin, mit belegter Antwort? Wenn nicht: nachtragen.
- **Zahlen nur aus den Daten** (Annotation „schlaege"/„mess"), nie aus dem Kopf.
- **Lehrbuch nie zitieren.** In Akte und Code nur eigene Worte und Lektionsnummern.
- Danach Dialoge mit dem Skill `dialoge` schreiben.

## 3. Abnahme

Eine Akte ist fertig, wenn (a) jede DD-Zeile belegt ist, (b) jede Spieleroption eine belegte
Rückmeldung hat, (c) die Kernzahlen aus den Daten nachgerechnet sind, (d) docs/FACHREGELN.md und
docs/QUELLEN.md nachgezogen sind.
