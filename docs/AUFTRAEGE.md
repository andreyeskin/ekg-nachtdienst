# Aufträge für Cloud-Sitzungen

Eine Cloud-Sitzung kennt dieses Gespräch nicht. Sie kennt nur dieses Repository.
Deshalb steht hier alles, was sie wissen muss — fertig zum Kopieren, ein Auftrag
pro Sitzung.

**So benutzt du diese Datei:** Neue Sitzung auf claude.ai/code öffnen, den
Vorspann plus **einen** Auftrag hineinkopieren, fertig werden lassen, Ergebnis
im Browser ansehen. Dann die nächste Sitzung.

---

## Vorspann — kommt vor jeden Auftrag

```
Arbeite im Repository EKG-Spiel. Lies zuerst, in dieser Reihenfolge:
  docs/GAME_DESIGN.md     — was für ein Spiel das ist
  docs/ART_BIBLE.md       — wie jedes Bild auszusehen hat
  docs/TASKS.md           — die Aufgabe, an der du arbeitest
  web/spiel.js            — wie Kapitel 1 gebaut ist; alles Neue folgt diesem Muster

Erfinde nichts neu. Es gibt bereits:
  web/ekg.js              — EKG auf Millimeterpapier, Messen, Monitorlauf
  web/szene.js            — Räume, vier Ebenen, Parallaxe, Hotspots
  web/dialog.js           — Gespräche mit Bedingungen
  web/mappe.js            — Befundmappe mit Kartenvergleich
  web/raetsel_zirkel.js   — Messrätsel gegen die Experten-Annotation
  gen/kunst.py            — alle Bilder; sie werden gezeichnet, nicht generiert
  data/ekg_daten.json     — echte Aufnahmen samt Lage jeder einzelnen Welle

Regeln, die nicht verhandelbar sind:
  - Kein Framework, keine CDN-Verweise, kein Netzzugriff zur Laufzeit.
  - Deutsch in allem, was der Spieler sieht; deutsche Namen im Code.
  - Jede EKG-Kurve kommt aus data/, niemals aus erfundenen Zahlen.
  - Jede geprüfte Zahl kommt aus den Annotationen (Feld „schlaege"), nie aus dem Kopf.
  - Kein Text in Bildern. Text setzt immer der Code.
  - Medizinisch muss es stimmen. Im Zweifel die Behauptung weglassen,
    nicht raten. Lieber eine Aussage weniger als eine falsche.

Vor dem Commit, immer:
  python3 gen/kunst.py          (wenn du gen/kunst.py geändert hast)
  python3 tools/baue.py
  node tools/durchlauf.mjs      — muss ohne Fehler durchlaufen
Erweitere tools/durchlauf.mjs um Prüfungen für das, was du gebaut hast.
Sieh dir mindestens einen Screenshot aus bau/durchlauf/ wirklich an.
Dann committen und pushen, eine Zeile Beschreibung auf Deutsch.
```

---

## Auftrag 1 · Rätsel „Reizleitung bauen"

```
Baue Aufgabe 5 aus docs/TASKS.md: web/raetsel_reizleitung.js.

Ein schematisches Herz als eigenes SVG (Vorhöfe, Kammern, Septum) — gerechnet
in Python in gen/kunst.py, nicht von Hand gemalt, Stil wie die übrigen Bilder.
Fünf Bauteile werden hineingezogen: Sinusknoten, AV-Knoten, His-Bündel,
Tawara-Schenkel, Purkinje-Fasern.

Nach jedem Setzen läuft eine Erregungswelle animiert durch das, was gebaut
wurde, und darunter entsteht die passende Kurve. Diese Kurve wird NICHT
gezeichnet, sondern aus echten Aufnahmen ausgewählt:
  - vollständig und richtig       → ein Datensatz mit "Sinus rhythm."
  - ohne Sinusknoten              → ein Datensatz mit "Atrial fibrillation."
                                    (kein Taktgeber im Vorhof, keine P-Wellen)
  - Schenkel fehlt oder falsch    → ein Datensatz mit QRS > 120 ms
                                    (z. B. id 24, kompletter Linksschenkelblock)
  - AV-Knoten an falscher Stelle  → ein Datensatz mit PQ > 200 ms (z. B. id 39)
Die Zuordnung steht als Tabelle im Code, mit einer Zeile Begründung je Fall.

Fertig, wenn mindestens drei Fehlaufbauten je ein medizinisch sinnvolles
falsches EKG erzeugen und der Zusammenhang im Text erklärt wird.
```

## Auftrag 2 · Kapitel 2: Monitorzimmer, 09:15

```
Baue das Monitorzimmer zu einem echten Kapitel aus. Der Raum, Dr. Falk und
die laufende Kurve stehen schon (siehe web/spiel.js, Funktion starteMonitor).

Inhalt:
  - Drei Schirme zeigen drei verschiedene echte Aufnahmen. Der Spieler soll
    sagen, welcher davon zu Herrn Baum gehört, und begründen, woran er es sieht.
  - Mini-Spiel „Ampel am Monitor" aus docs/GAME_DESIGN.md: eine Situation,
    drei Handlungen (beobachten · Arzt rufen · Pacer vorbereiten), Zeitdruck
    von etwa zehn Sekunden. Keine Strafe bei Fehlentscheidung — stattdessen
    eine Szene, in der Dr. Falk trocken korrigiert.
  - Ein Befund mehr für die Mappe, der sich mit dem Aufnahme-EKG vergleichen
    lässt (Feld „vergleich" in der Karte, siehe b-pq in web/spiel.js).

Medizinisch: Herr Baum hat Sinusbradykardie mit AV-Block I°. Am Monitor wird
beobachtet, weil eine verzögerte Überleitung plötzlich ausfallen kann. Behaupte
NICHT, dass im Monitor schon ein höhergradiger Block zu sehen ist — dafür haben
wir (noch) keine Aufnahme. Das Kapitel endet offen.

Fertig, wenn das Kapitel ohne Sackgasse durchspielbar ist und mindestens zwei
Wege zum Ziel führen.
```

## Auftrag 3 · Veröffentlichung

```
Baue Aufgabe 7 aus docs/TASKS.md.

  - tools/baue.py schreibt zusätzlich nach docs/ (GitHub Pages) statt nur bau/.
  - Manifest und Service Worker, damit die Seite installierbar ist und offline
    läuft. Der Service Worker cacht genau eine Datei — das Spiel ist eine Datei.
  - Ein Symbol als SVG, im Stil der Art Bible, ohne Schrift.
  - README ergänzen: wie man es lokal baut, wie man es aufruft.

Fertig, wenn die Seite über GitHub Pages erreichbar ist, im Flugmodus noch
läuft und auf dem iPad „Zum Home-Bildschirm" ein eigenes Symbol bekommt.
```

## Auftrag 4 · Mehr Aufnahmen, mehr Wiederspielwert

```
Zurzeit liegen 41 Aufnahmen in data/ekg_daten.json, alle aus der LUDB.
Die Auswahl in tools/baue.py nimmt davon nur wenige mit.

  - gen/export_spiel.py so erweitern, dass es auch PTB-XL verarbeiten kann
    (CC BY 4.0; die Auswahlliste liegt in data/ptbxl_auswahl.json). PTB-XL hat
    keine Wellen-Annotation — solche Aufnahmen dürfen deshalb NICHT für
    Messrätsel verwendet werden, nur zum Ansehen und Vergleichen. Das Feld
    "messbar": false in jeden solchen Datensatz schreiben, und
    web/raetsel_zirkel.js lehnt sie ab.
  - Das Spiel zieht bei jedem neuen Durchlauf eine andere Aufnahme derselben
    Diagnosegruppe (siehe docs/GAME_DESIGN.md, Abschnitt 5). Alle Texte, die
    eine Zahl nennen, müssen die Zahl aus den Daten holen — nicht aus dem Code.

Fertig, wenn zwei Durchläufe nacheinander andere Kurven zeigen und alle
geprüften Zahlen weiterhin stimmen.
```

---

## Was NICHT in die Cloud gehört

- **Das Lehrbuch.** Trappe/Schuster ist lizenziert. Kein Kapitel, kein PDF, kein
  Zitat in dieses Repository — auch nicht in ein privates. Fachliche Abgleiche
  mit dem Buch passieren dort, wo das Buch liegt.
- **Bilder aus Recraft**, solange sie nicht heruntergeladen und geprüft sind.
- **Alles, was einen Browser mit Anmeldung braucht** (Moodle, Recraft):
  geht nur in einer Sitzung mit angebundenem Rechner.
