# Aufgabenliste

Jede Aufgabe ist in sich abgeschlossen: Eine Cloud-Sitzung kann sie allein aus diesem
Repository heraus erledigen, ohne Rückfragen und ohne Zugriff auf den Rechner des Autors.

**Vor jeder Aufgabe lesen:** `docs/ART_BIBLE.md` (Bildregeln) und `docs/GAME_DESIGN.md`
(Spielkonzept). Die Regeln dort sind verbindlich.

**Grundsätze für allen Code**
- Keine Spiel-Engine, keine Frameworks, keine CDN-Links. Reines HTML, CSS, JavaScript, SVG, Canvas.
- Deutsch in allem, was der Spieler sieht; deutsche Namen im Code (wie in `web/ekg.js`).
- Jede EKG-Kurve kommt aus `data/`, niemals aus handgeschriebenen Zufallswerten.
- Text steht nie in einem Bild, immer im Code.
- Nach jeder Aufgabe: im Browser prüfen (Playwright/Chromium, Beispiel in `tools/schuss.mjs`),
  Screenshot ansehen, Konsole muss fehlerfrei sein.

---

## 1 · Szenen-Engine (Grundgerüst)

**Ziel:** `web/szene.js` — ein Raum wird aus einer Beschreibung aufgebaut und ist bedienbar.

Anforderungen:
- Eine Szene besteht aus vier Ebenen (Hintergrund, Mittelgrund, Figuren, Vordergrund), die sich
  bei Mausbewegung oder Neigung unterschiedlich schnell verschieben (Parallaxe, maximal 12 px).
- Anklickbare Bereiche (Hotspots) als SVG-Polygone mit Namen, Mauszeiger-Wechsel und dezenter
  Umrandung beim Überfahren.
- Szenenwechsel mit weichem Übergang (Abblenden, 400 ms).
- Zustand (aktueller Raum, gelöste Rätsel, Inventar) in einem einzigen Objekt, das sich
  speichern und laden lässt.
- Alles ohne Bilder lauffähig: solange keine Grafik vorhanden ist, werden farbige Flächen
  gezeichnet. So blockiert fehlende Kunst die Programmierung nicht.

**Fertig, wenn** eine Testseite zwei Räume zeigt, man zwischen ihnen wechselt, Hotspots reagieren
und der Zustand einen Neuladen übersteht.

---

## 2 · Dialogsystem

**Ziel:** `web/dialog.js` — Gespräche mit Figuren.

Anforderungen:
- Dialoge als Daten (JSON): Knoten mit Sprecher, Text, Antwortmöglichkeiten, Bedingungen
  (`wenn: hat_befund('pq_gemessen')`) und Wirkungen (`setze: ...`).
- Schreibmaschinen-Effekt, Überspringen per Klick, Name und Porträt der Figur.
- Figuren antworten unterschiedlich, je nachdem was der Spieler schon weiß (Bedingungen).
- Tastatur bedienbar, lesbar auf dem iPad.

**Fertig, wenn** ein Beispielgespräch mit Marlene läuft, in dem eine Antwort nur erscheint,
nachdem ein bestimmter Befund im Inventar liegt.

---

## 3 · Befundmappe (Inventar)

**Ziel:** `web/mappe.js` — gesammelte Befunde ansehen und vergleichen.

Anforderungen:
- Jeder Befund ist eine Karte: Titel, Zeitstempel, Bild (EKG aus der Engine) und kurzer Text.
- Zwei Karten lassen sich nebeneinanderlegen und gemeinsam betrachten (Kernmechanik).
- Karten lassen sich an Figuren zeigen; das löst im Dialogsystem Bedingungen aus.

**Fertig, wenn** drei Beispielkarten sammelbar, vergleichbar und vorzeigbar sind.

---

## 4 · Rätsel „Zirkel" (Messen)

**Ziel:** `web/raetsel_zirkel.js` auf Basis von `web/ekg.js`.

Anforderungen:
- Der Spieler zieht über den Streifen und misst eine Strecke (die Funktion `messbar` gibt es schon).
- Die Aufgabe nennt, was zu messen ist (PQ-Zeit, QRS-Breite, RR-Abstand).
- Geprüft wird gegen die Wahrheit aus `data/ekg_daten.json` (Feld `mess`), Toleranz ±20 ms.
- Rückmeldung nennt die Abweichung und zeigt die richtige Strecke eingeblendet.
- Drei Schwierigkeitsstufen über die Toleranz.

**Fertig, wenn** zehn verschiedene Aufnahmen durchspielbar sind und die Prüfung nachweislich
gegen die Expertenannotationen läuft (kleiner Test im Browser).

---

## 5 · Rätsel „Reizleitung bauen"

**Ziel:** `web/raetsel_reizleitung.js`.

Anforderungen:
- Ein schematisches Herz (eigenes SVG, keine Bildgenerierung): Vorhöfe, Kammern, Septum.
- Fünf Bauteile werden hineingezogen: Sinusknoten, AV-Knoten, His-Bündel, Tawara-Schenkel,
  Purkinje-Fasern.
- Nach jedem Setzen läuft eine Erregungswelle animiert durch das, was gebaut wurde, und darunter
  entsteht die passende Kurve: fehlt der AV-Knoten an der richtigen Stelle, sieht man es im EKG.
- Lernziel sichtbar machen: richtige Anatomie ergibt normales EKG.

**Fertig, wenn** mindestens drei Fehlaufbauten je ein medizinisch sinnvolles falsches EKG erzeugen.

---

## 6 · Kapitel 1 bauen

**Ziel:** Raum „Aufnahme", spielbar von Anfang bis Übergang.

Anforderungen aus `docs/GAME_DESIGN.md`: Marlene, Herr K., drei Befunde zum Sammeln, zwei davon
reichen für den Übergang. Licht nach Tageszeit 06:40.

**Fertig, wenn** ein Durchlauf ohne Sackgasse möglich ist und mindestens zwei Wege zum Ziel führen.

---

## 7 · Veröffentlichung

**Ziel:** GitHub Pages.

- Ein Build-Skript bündelt alles nach `docs/` oder `dist/` und die Seite läuft offline.
- Die Seite ist als PWA installierbar (Manifest, Service Worker).

---

## Offen, erst nach Absprache

- Vertonung (Umgebungsgeräusche, Stimmen).
- SCORM-Verpackung für Moodle.
- Kapitel 2 bis 6.
