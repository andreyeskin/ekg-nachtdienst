# Quellen und Belege

Dieses Spiel behauptet nichts, was nicht belegt ist. Hier steht, woher jede
Zahl und jede fachliche Aussage kommt — und ebenso, was wir **nicht** behaupten,
weil die Datenlage es nicht hergibt.

Alles hier ist offen lizenziert oder öffentlich zugänglich. Das Lehrbuch
(Trappe/Schuster, *EKG-Kurs für Isabel*) ist **keine** Quelle dieses Produkts:
es dient privat zum Gegenlesen, sein Inhalt wandert nicht ins Spiel.

Stand der Prüfung: 10.10.2026. Die Spalte „geprüft gegen" nennt, was an dem Tag
tatsächlich gelesen wurde, nicht was erinnert wurde.

---

## 1. Woher die Kurven kommen

| | |
|---|---|
| **LUDB** | Kalyakulina AI, Yusipov II, Moskalenko VA, Nikolskiy AV, Kosonogov KA, Osipov GV, Zolotykh NYu, Ivanchenko MV. *LUDB: A New Open-Access Validation Tool for Electrocardiogram Delineation Algorithms.* IEEE Access 2020;8:186181–186190. doi:10.1109/ACCESS.2020.3029211 |
| Datensatz | Kalyakulina A et al. *Lobachevsky University Electrocardiography Database* (v1.0.1). PhysioNet. doi:10.13026/eegm-h675 |
| Lizenz | Open Data Commons Attribution License v1.0 (ODC-By) — Namensnennung genügt, kommerzielle Nutzung erlaubt |
| Umfang | 200 Aufnahmen, je 10 s, 500 Hz, 12 Ableitungen |
| Annotation | Kardiologen haben **Grenzen und Gipfel** von P, QRS und T in jeder Ableitung einzeln markiert: 16 797 P-Wellen, 21 966 QRS-Komplexe, 19 666 T-Wellen |

**Das ist der Kern des Spiels.** Wenn der Zirkel sagt „deine PQ-Zeit ist 40 ms zu
kurz", dann vergleicht er nicht mit einem Mittelwert, sondern mit der von Hand
gesetzten Marke eines Kardiologen an genau diesem Schlag.

| | |
|---|---|
| **PTB-XL** | Wagner P, Strodthoff N, Bousseljot R-D, Kreiseler D, Lunze FI, Samek W, Schaeffter T. *PTB-XL: A Large Publicly Available ECG Dataset.* Scientific Data 2020;7:154. doi:10.1038/s41597-020-0495-6 |
| Datensatz | PhysioNet v1.0.3. doi:10.13026/kfzx-aw45 |
| Lizenz | CC BY 4.0 |
| Umfang | 21 799 Aufnahmen von 18 869 Patienten, 10 s, 500 Hz (und 100 Hz) |
| Befundung | SCP-ECG-Aussagen, 71 Stück, in fünf Oberklassen |

**Wichtige Einschränkung:** PTB-XL hat **keine** Wellen-Annotation. Aufnahmen
von dort dürfen deshalb gezeigt und verglichen, aber **nie zum Messen benutzt**
werden. Im Datensatz steht dafür `"messbar": false`.

---

## 2. Fachliche Quellen

| Kürzel | Quelle | geprüft gegen |
|---|---|---|
| **ESC-Synkope-2018** | Brignole M, et al. *2018 ESC Guidelines for the diagnosis and management of syncope.* Eur Heart J 2018;39(21):1883–1948. doi:10.1093/eurheartj/ehy037 | Volltext-PDF, Abschnitt 4.1.1, Tabellen 5 und 7 |
| **ESC-Pacing-2021** | Glikson M, Nielsen JC, Kronborg MB, et al. *2021 ESC Guidelines on cardiac pacing and cardiac resynchronization therapy.* Eur Heart J 2021;42:3427–3520 | Zusammenfassung des American College of Cardiology |
| **AHA-EKG-2007-I** | Kligfield P, Gettes LS, Bailey JJ, et al. *Recommendations for the standardization and interpretation of the electrocardiogram, Part I: The electrocardiogram and its technology.* Circulation 2007;115(10). doi:10.1161/CIRCULATIONAHA.106.180200 | Bibliografischer Nachweis |
| **Chou** | Surawicz B, Knilans TK. *Chou's Electrocardiography in Clinical Practice.* 6. Auflage | noch nicht am Original geprüft |

---

## 3. Belegtabelle Kapitel 1

| Aussage im Spiel | Beleg | Anmerkung |
|---|---|---|
| Die Aufnahme zeigt Sinusrhythmus | LUDB-Datensatz 39, Kommentarfeld „Sinus bradycardia" + eigene Prüfung: vor jedem QRS eine annotierte P-Welle | |
| Frequenz 53/min (RR ≈ 1130 ms) | LUDB 39, Median der RR-Abstände aus den QRS-Marken | Die im Spiel angezeigte Zahl wird aus dem **vom Spieler gemessenen** Schlag gerechnet, nicht fest eingetragen |
| Bradykardie = unter 60/min | allgemeiner Standard, ESC-Synkope-2018 nennt 40–50/min als „mild inappropriate sinus bradycardia" | |
| PQ-Zeit normal 120–200 ms | Chou; Schwelle 200 ms auch in ESC-Pacing-2021 | Untergrenze 120 ms noch am Original zu prüfen |
| PQ über 200 ms = AV-Block I. Grades | ESC-Pacing-2021; Definition: jede P-Welle wird übergeleitet, aber verzögert | |
| LUDB 39 hat PQ 214–258 ms (Median 228) | eigene Messung aus den Annotationen, Schlag für Schlag | Die Streuung ist echt: der P-Beginn ist die am schwersten zu setzende Marke |
| QRS schmal (82–92 ms) | LUDB 39, Annotation | spricht gegen eine Blockierung unterhalb des AV-Knotens |
| Synkope ohne Vorwarnung ist ein Warnzeichen | ESC-Synkope-2018, Tabelle 7: „Syncope without prodrome" unter den Hochrisikomerkmalen; Abschnitt 4.1.1: ein typisches, langsam einsetzendes Prodrom (Blässe, Schwitzen, Übelkeit) spricht **für** eine Reflexsynkope | **Vorsicht:** Die Leitlinie sagt *nicht*, dass fehlendes Prodrom kardiale Synkope beweist. Sie sagt: es macht die harmlose Erklärung unwahrscheinlicher und zählt als Risikomerkmal. Der Dialog im Spiel ist entsprechend formuliert |
| AV-Block I. Grades mit deutlich verlängerter PQ-Zeit passt zu arrhythmischer Synkope | ESC-Synkope-2018, Tabelle 5 (Merkmale, die eine Diagnose *nahelegen*, nicht beweisen) | Deshalb sagt Dr. Falk ausdrücklich, dass das noch nicht die Ursache ist |
| Betablocker bremsen Sinusknoten und AV-Überleitung | Pharmakologie, Standardwissen | |
| Eine langsame Frequenz ist nur dann verdächtig, wenn kein bremsendes Medikament im Spiel ist | ESC-Synkope-2018, Tabelle 5: Das Kriterium nennt ausdrücklich „with no negatively chronotropic drugs" | Deshalb ist Bisoprolol in der Tüte kein Beiwerk, sondern ein Argument |
| Beweisend für arrhythmische Synkope wären: Sinusbradykardie dauerhaft unter 40/min, Pausen über 3 s im Wachzustand, Mobitz II, AV-Block III° | ESC-Synkope-2018, Abschnitt 4.1.1, Klasse I, Evidenzgrad C | **Nichts davon liegt bei Herrn Baum vor.** Genau deshalb endet Kapitel 1 mit Beobachtung und nicht mit einer Diagnose |

---

## 4. Was das Spiel bewusst nicht behauptet

- **Nicht**, dass Herr Baums Synkopen durch den AV-Block I° erklärt sind. Sie sind
  es nach Datenlage nicht; der Block ist ein Hinweis auf eine angeschlagene
  Leitung, mehr nicht.
- **Nicht**, dass am Monitor bereits ein höhergradiger Block zu sehen ist. Dafür
  gibt es in unseren Daten keine Aufnahme mit Annotation, und eine gemalte Kurve
  kommt nicht in Frage.
- **Nicht**, dass die Bradykardie allein gefährlich ist. Unter Betablocker ist
  sie erwartbar.
- Keine Dosierungen, keine Therapieempfehlungen, keine Anweisungen zur
  Behandlung. Das Spiel übt Befunden, nicht Behandeln.

## 5. Offen

- Untergrenze der PQ-Norm (120 ms) am Primärtext belegen.
- Für Kapitel 2 und folgende: Aufnahmen mit AV-Block II°/III° **mit**
  Wellen-Annotation finden. PTB-XL hat die Diagnosen, aber keine Marken; LUDB
  hat die Marken, aber keine höhergradigen Blöcke. Solange diese Lücke besteht,
  wird in diesen Kapiteln verglichen und beobachtet, nicht gemessen.
- Fachliche Durchsicht durch einen Kardiologen vor einer Veröffentlichung, die
  über den eigenen Gebrauch hinausgeht.

---

## 6. Regel für alle, die hier weiterarbeiten

Eine Zahl ohne Beleg wird nicht geschrieben. Lieber eine Aussage weniger als
eine, die niemand nachschlagen kann. Wer eine neue Behauptung einbaut, trägt
sie in die Belegtabelle ein — in derselben Sitzung, nicht später.
