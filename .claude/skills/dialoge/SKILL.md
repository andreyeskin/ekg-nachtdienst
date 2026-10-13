---
name: dialoge
description: Dialoge für „Nachtdienst" schreiben, prüfen und überarbeiten — Figurenstimmen, Subtext, Anamnese-Gespräche, Spielerantworten mit echten Entscheidungen. Immer laden, bevor ein Dialog in web/ oder in einer Fallakte geschrieben oder geändert wird, und wenn Dialoge „hölzern", „belehrend" oder „seltsam" wirken.
license: MIT (Diagnose-Teil nach jwynia/agent-skills „dialogue", MIT); Rest Projektinhalt
---

# Dialoge in „Nachtdienst"

Ein Dialog im Spiel muss drei Dinge gleichzeitig leisten: **lehren**, **eine Figur zeigen**,
**die Lage verändern**. Ein Satz, der nur Wissen liefert, ist ein Lehrbuchsatz im Kostüm — er wird
umgeschrieben. Grundlage: der Diagnose-Ansatz aus jwynia/agent-skills („dialogue", MIT;
https://github.com/jwynia/agent-skills, skills/creative/fiction/character/dialogue), angepasst an ein
medizinisches Lernspiel.

## 1. Die drei Schichten jeder Zeile

| Schicht | Frage |
|---|---|
| **Text** | Klingt das nach genau dieser Person? Laut lesbar? Kurz genug für den Bildschirm? |
| **Subtext** | Was meint sie, ohne es zu sagen? Was will sie, worum sie nicht direkt bittet? |
| **Kontext** | Wer hat hier Macht? Was ist vorher passiert? Was steht für wen auf dem Spiel? |

Die meisten schwachen Dialoge scheitern am Subtext (alle sagen genau, was sie meinen) oder am Text
(alle klingen gleich).

## 2. Die sechs Fehlbilder (prüfen, benennen, beheben)

- **D1 Gleiche Stimmen.** Namen abdecken — erkennt man noch, wer spricht? Sonst: Stimmprofil (§4) schärfen.
- **D2 Hölzern.** Vollständige Schulsätze, keine Abbrüche, kein Rhythmus. Laut lesen; was man nicht sagen kann, neu schreiben.
- **D3 Erklärdump.** „Wie Sie wissen …", eine Figur fragt nur, damit die andere doziert. Wissen muss
  **entdeckt** werden: am Streifen, in der Tüte, in einer Antwort, die nicht passt.
- **D4 Auf die Nase.** Gefühle werden benannt („Ich mache mir Sorgen"). Stattdessen Verhalten: Herr Baum
  entschuldigt sich zum dritten Mal; Marlene schenkt Kaffee nach, ohne zu fragen.
- **D5 Nur eine Funktion.** Doppelt-Test: Jeder Wechsel beantwortet mindestens drei von vier Fragen —
  Was bringt er dem Fall? Was zeigt er über die Figur? Was ist der Subtext? Wie verschiebt er die Beziehung?
- **D6 Falsches Tempo.** In der Akutlage kurze Wechsel, Unterbrechungen; in der Ruhe längere Sätze, Pausen.

Weitere Muster, die sofort raus müssen: **der Philosoph** (Figur spricht das Lernziel oder die Moral
aus), **der Gerichtsschreiber** (Füllwörter ohne Inhalt), **das Tennismatch** (alle Repliken gleich lang,
niemand dominiert, niemand unterbricht), **der Erzähler-Tag** („sagte sie besorgt") — Gefühle zeigt die
Handlung, nicht ein Adverb.

## 3. Was in einem Lernspiel anders ist

1. **Der Spieler stellt die Fragen, die ein Arzt stellen würde.** Antwortoptionen sind echte
   Denkwege — auch die naheliegend falschen (z. B. bei einer Synkope: „Könnte das eine TIA sein?",
   „Hat er gekrampft?", „Hat er gegessen?"). Jede bekommt eine fachlich belegte, knappe Antwort im
   Ton der Figur. Keine Option ist nur Dekoration; keine falsche Option ist albern.
2. **Wissen kommt aus Widerspruch, nicht aus Vortrag.** Falk widerspricht, Marlene korrigiert, der
   Patient erinnert sich falsch, die Tochter sagt etwas anderes. Die Spielerin entscheidet, wem sie glaubt,
   und prüft es am EKG.
3. **Patienten sprechen Laiensprache** — ungenau, ausweichend, manchmal falsch („Mir wurde schwarz vor
   Augen", nicht „Ich hatte eine Synkope"). Fachbegriffe sagen nur Profis, und auch die nicht ständig.
4. **Die Lehre steht im Feedback, nicht im Gespräch.** Wer eine Option wählt, bekommt die Begründung
   als Rückmeldung (`warum`); das Gespräch selbst bleibt Gespräch.
5. **Bildschirmmaß:** eine Replik höchstens zwei Sätze, etwa 220 Zeichen; Spielerantworten höchstens
   eine Zeile. Lange Inhalte teilen, nie quetschen.
6. **Jede medizinische Aussage** muss in docs/FACHREGELN.md (Lehrbuch, eigene Worte) oder
   docs/QUELLEN.md stehen — vor dem Einbau, nicht danach. Im Zweifel weglassen.
7. **Keine Lektionsnummern, keine Quellenangaben im Spieltext.** Die gehören in Code-Kommentare.
8. **Kein Meta-Text** in Figurenmund („Hier endet der gebaute Teil" sagt nur der Erzähler).

## 4. Stimmprofile (verbindlich; neue Figuren bekommen eins, bevor sie sprechen)

| Figur | Satzbau | Wörter | Nie | Tic / Gegenstand |
|---|---|---|---|---|
| **Marlene** (Pflege, 54) | kurz, Hauptsätze, Imperativ | Stationsdeutsch, duzt Studierende | Fachvortrag, Unsicherheit zugeben | Thermoskanne, „So." |
| **Dr. Falk** (Oberarzt, 61) | langsam, Pausen (—), Gegenfragen | präzise Zahlen, siezt | Lob ohne Einschränkung, Eile | Zirkel, fragt zuerst nach Zahlen |
| **Patient** | Laiensprache, Entschuldigungen, Abschweifen | Alltag, Angehörige | Fachbegriffe | ein persönlicher Gegenstand |
| **Erzähler** | Präsens, sachlich, ohne Porträt | Ort, Zeit, Handlung | Wertungen, Lehrsätze | — |

## 5. Arbeitsablauf

1. Ziel des Gesprächs in einem Satz: Was muss die Spielerin danach wissen oder entschieden haben?
2. Was will jede Figur in diesem Gespräch — und was davon sagt sie nicht?
3. Rohfassung schreiben; dann D1–D6 und die Muster aus §2 durchgehen; jede Zeile laut lesen.
4. Spielerantworten prüfen: Bildet die Liste die echten ärztlichen Denkwege ab, inklusive der
   plausiblen Irrwege? Ist jede Rückmeldung belegt (§3.6)?
5. Übersetzungen (text/en.json, text/ru.json) im selben Schritt nachziehen; tools/durchlauf.mjs um
   Prüfungen für neue Wege ergänzen.

## 6. Letzter Durchgang: Humanizer (Pflicht vor jedem Commit von Spieltext)

Wenn verfügbar, den Skill `anthropic-skills:humanizer` auf die geänderten Texte anwenden; sonst diese
Liste von Hand durchgehen (Erkennungszeichen maschinell geschriebener Texte, auf Deutsch übertragen):

- **Gedankenstriche (—)**: höchstens einer pro Replik, besser keiner. Ersetzen durch Punkt, Komma,
  Doppelpunkt oder einen neuen Satz. Pausen in Falks Sprechweise lieber durch kurze Sätze zeigen.
- **Dreierreihen** („ruhig, klar und präzise"): eine oder zwei Angaben reichen.
- **„Nicht nur …, sondern auch …"**, „Es geht nicht um X, es geht um Y": umschreiben.
- **Füll- und Gewichtswörter**: „durchaus", „zudem", „darüber hinaus", „letztlich", „im Grunde",
  „spannend", „entscheidend", „wichtig zu beachten": streichen.
- **Aphorismen zum Schluss einer Replik** („Und genau darum geht es."): weg; Figuren ziehen keine Moral.
- **Gleich gebaute Sätze hintereinander** (gleiche Länge, gleiche Struktur): Rhythmus brechen.
- **Übertriebene Höflichkeit oder Bestätigung** („Gute Frage!", „Genau!"): nur, wenn es zur Figur passt.
- **Vage Zuschreibungen** („Studien zeigen", „man sagt"): konkret werden oder weglassen.

Zählprobe vor dem Commit: `grep -c "—"` über die geänderten Texte. Steigt die Zahl, nachbessern.

## 7. Was dieser Skill nicht tut

Er entscheidet keine medizinischen Inhalte — dafür gibt es `fallakte` und docs/FACHREGELN.md. Er
ersetzt nicht die Durchsicht durch eine Ärztin oder einen Arzt vor einer Veröffentlichung.
