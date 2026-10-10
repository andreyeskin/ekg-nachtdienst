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
| 8 · Das schnelle Herz und der Rest | Tachykardien, Flimmern, Spezialfälle, Schrittmacher | 21–31 |
| Abschluss | Systematisch befunden, fünf Schritte, jedes EKG | 32 |

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

| Abteilung | Stoff | Kernpatienten | Nebenpatienten |
|---|---|---|---|
| **Lehrsaal** | 1, 2, 3, 4, 5, 6, 7 | — (Übungen am Gerät) | Normalbefunde |
| **Aufnahme** | 8, 9, 10, 11 | Herr Baum (Synkope) | Brady-/Tachykardien |
| **Monitorzimmer** | 30, 9, 10 | Herr Baum, Teil 2 | Monitorstreifen |
| **Station** | 12, 13, 14, 15, 18 | Frau mit Luftnot (Schenkelblock) | Hypertrophien, Vorhofbefunde |
| **Herzkatheter / Chest Pain** | 16, 19, 20 | Der Mann mit dem Druck auf der Brust | Infarkte aller Lokalisationen |
| **Intensiv** | 17, 23, 26, 29 | Patient nach Reanimation | Elektrolyte, Schrittmacher, VES |
| **Rhythmusambulanz** | 24, 25, 27, 28 | Junge Frau mit Herzrasen | Flimmern, Flattern, WPW |
| **Innere / Pulmologie** | 21, 22, 31 | Der Kurzatmige nach der Reise | Perikarditis, Dextrokardie |
| **Befundraum** | 32 | — | **alle** Aufnahmen aus der Datenbank |

Der **Befundraum** ist der Motor für die Menge: Dort liegt jede Aufnahme der
Datenbank als Fall bereit, und das Spiel prüft den Befund gegen die Diagnose,
die in der Datenbank steht. Damit skaliert die Zahl der Patienten auf hunderte,
ohne dass jeder einzeln geschrieben werden muss.

---

## 3. Patienten: zwei Sorten

**Kernpatient** — ein Mensch mit Namen, Geschichte, Zimmer und mehreren Szenen.
Trägt eine Stufe. Etwa acht bis zehn im ganzen Spiel. Teuer zu bauen.

**Nebenpatient** — eine echte Aufnahme, drei Zeilen Vorgeschichte, eine Aufgabe,
eine Rückmeldung. Liegt im Bett, in der Ambulanz, im Archiv. Billig zu bauen,
beliebig viele. Aus den **458 ausgewählten PTB-XL-Aufnahmen** werden so
mindestens hundert Patienten, jeder mit echter Kurve und geprüfter Diagnose.

Die Mischung ist der Punkt: Die Kernpatienten erzählen, die Nebenpatienten
trainieren. Wer nur die Geschichte spielt, lernt zu wenig; wer nur Streifen
befundet, hält nicht durch.

---

## 4. Deckung: was die Daten hergeben

Geprüft gegen `data/ekg_daten.json` (41 Aufnahmen LUDB, mit Wellen-Annotation)
und `data/ptbxl_auswahl.json` (458 Aufnahmen PTB-XL, mit Diagnosen).

| Lektion | Thema | Daten vorhanden | Messbar? |
|---|---|---|---|
| 1–7 | Grundlagen | Normalbefunde: 40 SR + 89 NORM | ja (LUDB) |
| 8 | Sinusrhythmus und Varianten | SBRAD 30, STACH 30, SARRH 29 | ja |
| 9 | SA-Block, Sick Sinus | **fehlt** | — |
| 10 | AV-Block I–III | 1AVB 30, **2AVB 14, 3AVB 16** | teils |
| 11 | AV-junktionaler Rhythmus | in 3AVB enthalten | teils |
| 12 | Vorhofleitungsstörungen | RAO/RAE 15, LAO/LAE 14 | ja (LUDB-P-Dauer) |
| 13 | Schenkelblöcke | CRBBB 19, CLBBB 15, IRBBB 33, IVCD 23 | ja (QRS-Breite) |
| 14 | Hemiblöcke | LAFB 13; **LPFB fehlt** | ja (Achse) |
| 15 | R-Progression, S-Persistenz | in Infarkt- und Hypertrophiefällen | ja |
| 16 | ST/T | NST_ 42, STD_ 35, NDT 31, ISC_ 46 | ja |
| 17 | QT, langes QT | QT messbar (LUDB); **pathologisch fehlt** | ja/— |
| 18 | Hypertrophie | LVH 50, RVH 23 | ja (Sokolow) |
| 19–20 | Infarkt, Lokalisation | ASMI 49, IMI 35 u. a. | ja |
| 21 | Lungenembolie | **fehlt** | — |
| 22 | Peri-/Myokarditis | **fehlt** | — |
| 23 | Elektrolyte | **fehlt** | — |
| 24 | SVES, SVT, WPW | PAC 32, SVTAC 27, PSVT 24, WPW 20 | ja |
| 25 | Vorhofflimmern, -flattern | AFIB 40, AFLT 27 | ja |
| 26 | Ventrikuläre Störungen | PVC 53; **VT/Kammerflimmern fehlt** | teils |
| 27 | Brugada | **fehlt** | — |
| 28 | ARVD/C | **fehlt** | — |
| 29 | Schrittmacher | PACE 15 | ja |
| 30 | Monitor-EKG | jede Aufnahme im Monitormodus | ja |
| 31 | Situs inversus | **im Auszug nicht; in der Volldatenbank suchen** | — |
| 32 | Systematische Befundung | alle | ja |

**Sieben Lücken.** So wird damit umgegangen, in dieser Reihenfolge:

1. **In der Volldatenbank suchen.** Die ausgewählten 458 sind ein Auszug; PTB-XL
   hat 21 799 Aufnahmen und 71 Diagnose-Codes. Für Situs inversus, VT und
   seltenere Muster lohnt die Suche in `ptbxl_database.csv`.
2. **Andere offene Quellen prüfen.** Es gibt weitere frei lizenzierte
   EKG-Sammlungen; jede Aufnahme, die ins Spiel soll, muss eine Lizenz haben,
   die Weitergabe und Verkauf erlaubt.
3. **Als Schema zeigen, nicht als Aufnahme.** Wo keine echte Kurve zu bekommen
   ist (Brugada, ARVD, Elektrolytstörungen), wird ein **gerechnetes Schema**
   gezeigt und ausdrücklich so beschriftet: „Schema, keine Aufnahme." Gemessen
   wird daran nie. Eine gezeichnete Kurve, die sich als Aufnahme ausgibt, kommt
   nicht ins Spiel — das ist dieselbe Regel wie in der Art Bible.

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

1. **Befundungs-Trainer (Lektion 32).** Zuerst, weil er aus jeder Aufnahme der
   Datenbank sofort einen Patienten macht. Fünf Schritte, feste Reihenfolge,
   Prüfung gegen die Diagnose der Datenbank.
2. **Lehrsaal (1–7).** Die Grundlagen, die alles andere voraussetzt. Viele kurze
   Übungen, aus dem bestehenden Kurs übernehmbar.
3. **Aufnahme und Monitorzimmer fertig (8–11, 30).** Herr Baum zu Ende erzählen,
   jetzt mit echten AV-Block-II/III-Aufnahmen aus PTB-XL.
4. **Station (12–15, 18).** Schenkelblöcke und Hypertrophie — viel Stoff, gute
   Datenlage.
5. **Herzkatheter (16, 19, 20).** Infarkt.
6. **Rhythmusambulanz (24–26).** Tachykardien.
7. **Intensiv (17, 23, 29).** Spezialfälle mit Schemata, wo Daten fehlen.
8. **Innere (21, 22, 27, 28, 31).** Der Rest, zuletzt, weil die Datenlage dünn ist.

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
