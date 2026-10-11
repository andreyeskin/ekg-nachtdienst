# Lehrplan — das ganze Buch als Krankenhaus

**Ziel:** Wer „Nachtdienst" durchgespielt hat und danach den EKG-Kurs aufschlägt,
findet nichts Neues darin. Nicht, weil das Buch im Spiel steht — sondern weil
alles, was es verlangt, im Spiel an echten Patienten geübt und geprüft wurde.

Das Buch ist der **Lehrplan**, nicht der Inhalt. Es sagt, was man können muss.
Was das Spiel behauptet, stammt aus offenen Quellen (`QUELLEN.md`); was es zeigt,
stammt aus offenen Datenbanken. Kein Satz und kein Bild aus dem Buch wandert ins
Produkt.

---

## 1. Der Bogen: acht Stufen, vom Blatt Papier zum fertigen Befund

| Stufe | Was man danach kann | Lektionen |
|---|---|---|
| 1 · Das Papier lesen | Zacken benennen, Ableitungen zuordnen, in mm messen | 1, 2 |
| 2 · Die Zacken prüfen | P, PQ, QRS, ST, T einzeln beurteilen | 3, 4 |
| 3 · Die Achse | Lagetyp bestimmen und deuten | 5, 6 |
| 4 · Takt und Tempo | Rhythmus und Frequenz, Sinus und seine Varianten | 7, 8 |
| 5 · Die Leitung | SA-Block, AV-Block, Ersatzrhythmen | 9, 10, 11 |
| 6 · Der Muskel | Vorhöfe, Schenkel, Faszikel, R-Progression, Hypertrophie | 12, 13, 14, 15, 18 |
| 7 · Die Durchblutung | ST/T, Infarkt, Lokalisation, QT | 16, 17, 19, 20 |
| 8 · Das schnelle Herz und der Rest | Tachykardien, Flimmern, Spezialfälle, Schrittmacher, Monitor | 21–33 |
| Abschluss | Systematisch befunden, fünf Schritte, jedes EKG | 34 (dazu 35–38: Rhythmus-Tricks, Technik, Artefakte, typische Fehler) |

Jede Stufe endet erst, wenn der Spieler sie an echten Aufnahmen **gezeigt** hat.
Gelesen zu haben reicht nirgends.

---

## 2. Das Haus: wo man was lernt

Das Krankenhaus ist keine Kulisse, sondern die Gliederung des Stoffes. Jede
Abteilung hat die Patienten, an denen genau ihr Stoff sichtbar wird.

```
                     ┌─ Lehrsaal (Einschulung) ─┐
                     │                           │
   Aufnahme ─── Monitorzimmer ─── Station ─── Intensiv
       │              │               │            │
   Ambulanz      Befundraum       Archiv      Herzkatheter
       │                              │
   Rhythmusambulanz ──────────────────┘
```

Jeder Fall hat seinen eigenen Patienten und gehört zu einer Lektion oder Diagnose; die Akten liegen
unter `docs/faelle/`, der Fallkatalog mit Aufnahme-Nummern in `docs/KONZEPT.md` §5.

| Abteilung | Stoff | Kernpatienten | Nebenpatienten |
|---|---|---|---|
| **Lehrsaal** | 1, 2, 3, 4, 5, 6, 7 (8: Varianten) | Jonas Prem, Tutor als Freiwilliger (Normal-EKG, LUDB 142) | anonymisierte Kursstreifen (Sinusarrhythmie 158, Sinusbradykardie 160) |
| **Aufnahme** | 8, 10 (I°); Synkope nach ESC | Herr Baum (Synkope; Sinusrhythmus langsam, AV-Block I°, LUDB 39) | AV-Block I° (134, 78, 107, 77) |
| **Monitorzimmer** | 31, 25, 7 | Frau Lindner (Herzstolpern; Vorhofflimmern am Monitor, LUDB 96); Herr Baum als Rückblick in einem anderen Bett | Monitorstreifen (173, 110, 129, 38) |
| **Station** | 12, 13, 14, 15, 18 | Frau mit Luftnot (Schenkelblock) | Hypertrophien, Vorhofbefunde |
| **Herzkatheter / Chest Pain** | 16, 19, 20 | Der Mann mit dem Druck auf der Brust | Infarkte aller Lokalisationen |
| **Intensiv** | 17, 23, 26, 30 | Patient nach Reanimation | Elektrolyte, Schrittmacher, VES |
| **Rhythmusambulanz** | 24, 25, 27, 28 | Junge Frau mit Herzrasen | Flimmern, Flattern, WPW |
| **Innere / Pulmologie** | 21, 22, 32 | Der Kurzatmige nach der Reise | Perikarditis, Dextrokardie |
| **Befundraum** | 34 | — | **alle** Aufnahmen aus der Datenbank |

Der **Befundraum** ist der Motor für die Menge: Dort liegt jede Aufnahme der
Datenbank als Fall bereit, und das Spiel prüft den Befund gegen die Diagnose,
die in der Datenbank steht. Damit skaliert die Zahl der Patienten auf hunderte,
ohne dass jeder einzeln geschrieben werden muss.

---

## 3. Patienten: zwei Sorten

**Kernpatient** — ein Mensch mit Namen, Geschichte, Zimmer und mehreren Szenen.
Trägt **eine** Lektion oder Diagnose (nie eine ganze Stufe, `KONZEPT.md` §1). Etwa zehn bis
fünfzehn im ganzen Spiel. Teuer zu bauen.

**Nebenpatient** — eine echte Aufnahme, drei Zeilen Vorgeschichte, eine Aufgabe,
eine Rückmeldung. Liegt im Bett, in der Ambulanz, im Archiv. Billig zu bauen,
beliebig viele. Aus den **458 ausgewählten PTB-XL-Aufnahmen** werden so
mindestens hundert Patienten, jeder mit echter Kurve und geprüfter Diagnose.

Die Mischung ist der Punkt: Die Kernpatienten erzählen, die Nebenpatienten
trainieren. Wer nur die Geschichte spielt, lernt zu wenig; wer nur Streifen
befundet, hält nicht durch.

---

## 4. Deckung: was die Daten hergeben

Gezählt am 10.10.2026 aus den Dateien selbst, nicht geschätzt. Drei Quellen:

| Quelle | Aufnahmen | Lizenz | Besonderheit |
|---|---|---|---|
| **LUDB** | 199 | ODC-By | **Wellen-Annotation durch Kardiologen** — die einzige Quelle, an der gemessen werden darf |
| **PTB-XL** (Auswahl) | 458 | CC BY 4.0 | SCP-Codes, Befundtext, Alter, Achse |
| **Chapman-Shaoxing / Ningbo** | 1359 | CC BY 4.0 | 86 verschiedene Diagnosen, SNOMED-codiert |
| **gesamt** | **2016** | | |

| Lektion | Thema | LUDB | PTB-XL | Chapman | gesamt | Stand |
|---|---|---:|---:|---:|---:|---|
| 1–7 | Grundlagen, Normalbefund | 142 | 286 | 121 | 549 | ok |
| 8 | Sinus und Varianten | 39 | 116 | 672 | 827 | ok |
| 9 | SA-Block, Sick Sinus | 0 | 0 | 42 | 42 | ok |
| 10 | AV-Block I–III | 0 | 73 | 180 | 253 | ok |
| 11 | AV-junktional, Ersatzrhythmen | 0 | 0 | 200 | 200 | ok |
| 12 | Vorhofleitung | 0 | 49 | 118 | 167 | ok |
| 13 | Schenkelblöcke | 0 | 121 | 252 | 373 | ok |
| 14 | Hemiblöcke | 0 | 57 | 41 | 98 | ok |
| 15 | R-Progression, Rotation | 0 | 0 | 108 | 108 | ok |
| 16 | ST und T | 0 | 154 | 985 | 1139 | ok |
| 17 | QT-Zeit, langes QT | an jeder LUDB-Aufnahme messbar | 0 | 65 | 65 | ok |
| 18 | Hypertrophie | 0 | 73 | 225 | 298 | ok |
| 19–20 | Infarkt und Lokalisation | 0 | 101 | 67 | 168 | ok |
| 21 | **Lungenembolie** | 0 | 0 | 0 | **0** | **Lücke** |
| 22 | **Peri-/Myokarditis** | 0 | 0 | 0 | **0** | **Lücke** |
| 23 | **Elektrolytstörungen** | 0 | 0 | 0 | **0** | **Lücke** |
| 24 | SVES, SVT, WPW | 0 | 103 | 413 | 516 | ok |
| 25 | Vorhofflimmern und -flattern | 18 | 67 | 300 | 385 | ok |
| 26 | Ventrikuläre Störungen | 0 | 53 | 224 | 277 | ok |
| 27 | Brugada | 0 | 0 | 5 | 5 | dünn |
| 28 | Short-QT-Syndrom (Titel laut Verweis in Lektion 38; noch nicht gelesen) | – | – | – | – | offen |
| 29 | **ARVD/C** | 0 | 0 | 0 | **0** | **Lücke** |
| 30 | Schrittmacher | 0 | 15 | 67 | 82 | ok |
| 31 | Monitor-EKG | alle | | | alle | ok |
| 32 | **Situs inversus / Dextrokardie** | 0 | 0 | 0 | **0** | **Lücke** |
| 34 | Systematische Befundung | alle | | | alle | ok |

Die Lektionsnummern folgen dem Inhaltsverzeichnis der Kapitel-PDFs (Stand 10.10.2026): 29 ARVD/C,
30 Schrittmacher, 31 Monitor-EKG, 32 Situs inversus, 33 Kinder und Jugendliche, 34 systematische
Befundung, 35–38 Rhythmus-Tricks, Technik, Artefakte, typische Fehler. Eine frühere Fassung dieser
Tabelle zählte ab 28 um eins zu niedrig.

### Was daraus folgt

**26 von 33 aufgeführten Lektionen sind mit echten Aufnahmen gedeckt.** Fünf Lücken bleiben,
eine Lektion ist dünn, eine (28) noch ungelesen.

**Die wichtigste Zahl steht nicht in der Spalte „gesamt", sondern in der Spalte
„LUDB": 199.** Nur diese Aufnahmen tragen eine Wellen-Annotation von
Kardiologen, und nur an ihnen darf der Zirkel prüfen, ob *richtig* gemessen
wurde — also ob der Spieler wirklich den P-Beginn erwischt hat und nicht
zufällig eine gleich lange Strecke daneben. Alle übrigen 1817 Aufnahmen sind
zum **Ansehen, Vergleichen und Befunden** da, nicht zum Messen. Darum stehen
sie im Export auf `messbar: false`.

Das ist kein Mangel, sondern die ehrliche Grenze offener Daten: Wer messen
lehren will, braucht jemanden, der vorher von Hand markiert hat, wo die Welle
anfängt. Das haben 199 Aufnahmen.

**Nachtrag 11.10.2026:** `data/ekg_daten.json` enthält von diesen 199 Aufnahmen bisher **nur
Ableitung II** (250 Hz, 10 s). Damit sind Lagetyp (Lektion 5, 6), Hemiblock (14), R-Progression
(15) und Hypertrophie (18) noch nicht am echten Streifen prüfbar, obwohl LUDB alle zwölf
Ableitungen samt Annotation hat. Der Export (`gen/export_spiel.py`) ist der erste Datenauftrag in
`docs/UMBAU.md`; bis dahin stehen diese Lektionen im Fallkatalog als Lücke.

### Die fünf Lücken

Lungenembolie, Peri-/Myokarditis, Elektrolytstörungen, ARVD/C und Dextrokardie
fehlen in allen drei Datenbanken — sie kommen in der SNOMED-Codeliste der
Challenge 2021 überhaupt nicht vor. Vorgehen, in dieser Reihenfolge:

1. **PTB Diagnostic Database** (ODC-By, 549 Aufnahmen) prüfen: sie führt
   Myokarditis als Diagnose auf Patientenebene. Damit wäre Lektion 22 gedeckt.
2. **Volle PTB-XL** (21 799 Aufnahmen statt der 458 der Auswahl) nach
   Dextrokardie durchsuchen; der Befundtext ist frei durchsuchbar.
3. **Als Schema zeigen, nicht als Aufnahme.** Wo keine echte Kurve zu bekommen
   ist, wird ein gerechnetes Schema gezeigt und ausdrücklich so beschriftet:
   „Schema, keine Aufnahme." Gemessen wird daran nie. Eine gezeichnete Kurve,
   die sich als Aufnahme ausgibt, kommt nicht ins Spiel — dieselbe Regel wie in
   der Art Bible.

Für Lungenembolie, ARVD/C und Elektrolyte ist Weg 3 der wahrscheinliche: Diese
Muster sind in offenen Sammlungen kaum sauber annotiert zu bekommen.

---

## 5. Bedienung — gleich wichtig wie der Inhalt

Ein Lernspiel, das man erst bedienen lernen muss, lehrt zuerst sich selbst und
erst dann das EKG. Deshalb gelten diese Regeln für jeden neuen Bildschirm:

1. **Eine Geste für alles: antippen.** Gezogen wird nur dort, wo es die Sache
   selbst verlangt — beim Zirkel, weil Messen Ziehen ist. Keine versteckten
   Gesten, kein Doppeltippen, kein langes Drücken, kein Wischen.
2. **Was anklickbar ist, ist sichtbar.** Beim Überfahren mit der Maus durch
   Umrandung und Namen; auf dem iPad über „Was geht hier?", das alle Felder
   kurz aufleuchten lässt. Niemand soll Pixel suchen.
3. **Immer vier Dinge im Blick:** wo bin ich (Ort), wie spät ist es (Uhr), was
   habe ich (Befundmappe), was ist offen (Stand). Immer an derselben Stelle,
   in jedem Bildschirm.
4. **Zurück ist immer oben rechts.** Immer dasselbe Wort, immer dieselbe Stelle.
   Jeder Bildschirm hat einen sichtbaren Ausgang; es gibt keine Sackgasse und
   nichts, was man „wegklicken" muss.
5. **Fingergröße.** Jede Schaltfläche mindestens 44 × 44 px, jedes anklickbare
   Feld im Bild groß genug für einen Daumen. Der Apple Pencil darf genauer sein,
   muss es aber nie.
6. **Tastatur gleichwertig.** Ziffern wählen Antworten, Leertaste und Eingabe
   führen weiter, `h` zeigt die Felder, `s` den Stand, Escape schließt.
7. **Nichts blinkt, nichts drängt.** Kein Zeitdruck außer dort, wo er zur Sache
   gehört (Ampelspiel am Monitor), und auch dort ohne Strafe.
8. **Jede Rückmeldung sagt warum.** „Falsch" allein ist verboten. Immer: was war
   gemeint, woran erkennt man es, wo steht es im Streifen.
9. **Gleiche Dinge sehen gleich aus.** Eine Messaufgabe sieht überall gleich aus,
   egal in welcher Abteilung. Wer eine kann, kann alle.
10. **Lesbar.** Fließtext mindestens 16 px, Zahlen in der Monospace-Schrift,
    Kontrast auch bei Sonne auf dem iPad.

Diese Liste wird bei jeder neuen Oberfläche durchgegangen, bevor sie
eingecheckt wird.

---

## 5a. Ton

Eigene Datei: `docs/TON.md`. Das Wichtigste daraus: Der Monitorton wird aus den
echten R-Zacken der Aufnahme gerechnet, nicht abgespielt — man hört die
Bradykardie und die Pause. Stimmen werden nachgeladen, nie eingebettet, und
erst aufgenommen, wenn der Text einer Abteilung endgültig ist. Alles muss stumm
funktionieren.

## 6. Reihenfolge des Baus

Nicht nach Lektionsnummern, sondern nach dem, was den größten Teil des Stoffes
auf einmal nutzbar macht:

Die Reihenfolge des Umbaus steht in `docs/UMBAU.md` (Lehrsaal → Kapitel 1/2 auf das neue Konzept →
Architektur). Danach:

1. **Befundungs-Trainer (Lektion 34).** Weil er aus jeder Aufnahme der
   Datenbank sofort einen Patienten macht. Fünf Schritte, feste Reihenfolge,
   Prüfung gegen die Diagnose der Datenbank.
2. **Lehrsaal (1–7).** Die Grundlagen, die alles andere voraussetzt. Viele kurze
   Übungen am Freiwilligen (`docs/faelle/lehrsaal.md`).
3. **Aufnahme und Monitorzimmer auf dem neuen Konzept (8, 10 I°, 31, 25).** Herr Baum als
   abgeschlossener Synkopen-Fall; Frau Lindner mit Vorhofflimmern am Monitor. AV-Block II/III
   bekommen später eigene Patienten (PTB-XL, nur Ansehen).
4. **Station (12–15, 18).** Schenkelblöcke und Hypertrophie — viel Stoff, gute
   Datenlage.
5. **Herzkatheter (16, 19, 20).** Infarkt.
6. **Rhythmusambulanz (24–26).** Tachykardien.
7. **Intensiv (17, 23, 30).** Spezialfälle mit Schemata, wo Daten fehlen.
8. **Innere (21, 22, 27, 29, 32).** Der Rest, zuletzt, weil die Datenlage dünn ist.

---

## 7. Was in jeder Abteilung gleich aufgebaut ist

Damit es nicht achtmal neu erfunden wird:

- **Ein Raum** mit vier Ebenen, Hotspots, Uhr, Befundmappe.
- **Ein Kernpatient** mit Dialogbaum und zwei bis vier Befunden zum Sammeln.
- **Zwei bis vier Nebenpatienten** aus der Datenbank, je eine Aufgabe.
- **Ein neues Werkzeug** pro Abteilung (Zirkel, Lineal, Lupe, Leiterdiagramm,
  Sokolow-Rechner …), das danach überall verfügbar bleibt.
- **Eine Figur**, die korrigiert, ohne zu belehren.
- **Kein Game Over.** Falsche Schlüsse kosten Zeit und erzeugen eine Szene.
