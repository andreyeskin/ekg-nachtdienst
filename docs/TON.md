# Ton — Atmosphäre, Stimmen, und der Puls, den man hört

Ton ist in diesem Spiel kein Beiwerk. Ein EKG ist ein Rhythmus, und Rhythmus
hört man besser, als man ihn sieht. Wer eine Pause einmal **gehört** hat,
erkennt sie danach im Streifen.

## 1. Die eiserne Regel

**Alles muss stumm funktionieren.** Kein Befund, keine Aufgabe und keine
Warnung darf nur über den Ton laufen. Ton verstärkt, er trägt nie allein. Das
ist Barrierefreiheit und zugleich Alltag: gespielt wird in der Bibliothek, im
Zug, zwischen zwei Diensten.

## 2. Drei Schichten

### a) Der Puls — gerechnet, nicht aufgenommen

Der Monitorton wird **aus der echten Aufnahme erzeugt**: ein kurzer Ton pro
R-Zacke, exakt auf den Annotationen der Datenbank. Damit ist er so unregelmäßig
oder so langsam wie der Patient. Man hört die Bradykardie. Man hört die Pause.
Man hört, dass bei Vorhofflimmern kein Takt drin ist.

Gemacht wird das mit der Web Audio API, nicht mit Dateien: ein Oszillator, eine
kurze Hüllkurve, Tonhöhe nach Sättigung (hoch = gut, tiefer = schlechter, wie am
echten Monitor). Das kostet null Bytes und ist jedes Mal richtig.

Dasselbe Prinzip für das Metronom beim Frequenzschätzen und für den Ton, der
eine gemessene Strecke hörbar macht.

### b) Umgebung — leise, lang, unaufdringlich

Pro Raum eine Grundstimmung, die sich mit der Tageszeit ändert: morgens Vögel
und ein Kaffeeautomat hinter der Wand, mittags Stimmen im Flur, nachts
Lüftung und Regen. Dazu wenige Einzelgeräusche, die zu etwas gehören, das man
sieht: Tür, Rollwagen, Papierstreifen, Clogs auf Linoleum.

Nichts loopt hörbar. Lieber zwei Minuten Material mit zufälligen Einsätzen als
ein zwanzig Sekunden langer Loop, der nach dem dritten Mal nervt.

### c) Stimmen

Die Figuren sprechen. Das ist der größte Unterschied zwischen „Lernprogramm"
und „Spiel", und zugleich der teuerste Teil.

- **Marlene** — warm, trocken, kurze Sätze, Grazer Färbung. Nie belehrend.
- **Dr. Falk** — langsam, tief, Pausen zwischen den Sätzen. Spricht wenig.
- **Herr Baum** — höflich, leicht außer Atem, entschuldigt sich zu oft.
- **Erzähler** — nur zwischen den Kapiteln, sehr sparsam.

Fachbegriffe müssen stimmen: „Wenckebach", „Tawara-Schenkel", „Sokolow-Index",
„Torsade de pointes". Eine Stimme, die das falsch betont, verliert die Figur.
Deshalb gehört zu jeder Aufnahme eine Ausspracheliste.

## 3. Wie das technisch geht, ohne das Spiel zu sprengen

Das Spiel ist **eine Datei**. Stimmen für ein tagelanges Spiel sind hunderte
Megabyte. Beides zusammen geht nicht. Also:

| Fassung | Puls und Töne | Umgebung | Stimmen |
|---|---|---|---|
| **Eine Datei** (zum Weitergeben, iPad, Documents) | ja, gerechnet | kurze eingebettete Schleifen, stark komprimiert | nein |
| **Gehostete Fassung / PWA** | ja, gerechnet | ja, nachgeladen | ja, nachgeladen |
| **Moodle (SCORM)** | ja, gerechnet | ja | ja, wenn Platz |

Die Stimmen werden also **nachgeladen**, nie eingebettet. Fehlt die Verbindung,
läuft das Spiel weiter und zeigt den Text — dafür ist Regel 1 da.

Format: Opus in einer `.webm`-Hülle, ein File je Dialogknoten, benannt nach der
Knoten-ID. Dadurch kann jede Szene unabhängig vertont oder neu vertont werden.

## 4. Rechtliches — bevor der erste Ton aufgenommen wird

- **Gekaufte oder CC0-Geräusche.** Jede Aufnahme bekommt eine Zeile in
  `ATTRIBUTION.md`: Quelle, Lizenz, Datum. Keine Datei ohne diese Zeile.
- **Synthetische Stimmen** (ElevenLabs o. ä.): nur mit einem Tarif, der die
  kommerzielle Nutzung ausdrücklich erlaubt, und die Bestätigung wird
  aufgehoben. Die Lizenzbedingungen werden vor der Produktion gelesen, nicht
  danach.
- **Keine Stimme eines echten Menschen ohne schriftliche Zustimmung** — auch
  nicht nachgebaut.
- Keine Musik aus Spielen, Filmen oder Serien, in keiner Form.

## 5. Reihenfolge

1. **Puls und Rückmeldungstöne** (gerechnet). Billig, sofort nützlich, lehrt
   wirklich etwas. Kommt als Erstes.
2. **Umgebung pro Raum**, zusammen mit dem jeweiligen Raum.
3. **Stimmen** erst, wenn der Text einer Abteilung endgültig ist. Vorher ist
   jede Aufnahme Ausschuss — Texte ändern sich beim Bauen noch.

## 6. Einstellungen, die der Spieler bekommt

Drei Regler, mehr nicht: **Stimmen · Umgebung · Töne**. Jeder einzeln auf null
stellbar. Die Einstellung wird gemerkt. Dazu eine Taste, die alles sofort stumm
schaltet — für den Fall, dass jemand hereinkommt.
