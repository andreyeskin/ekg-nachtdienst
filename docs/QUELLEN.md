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
| Norm der Sinusfrequenz 50–100/min; Sinusbradykardie = unter 50/min; 53/min heißt im Spiel „Sinusrhythmus, langsam" | Lehrbuch Lektion 8 als Prüfmaßstab (§7); ESC-Synkope-2018 nennt als Warnzeichen erst dauerhaft < 40/min und als „mild inappropriate sinus bradycardia" 40–50/min | Viele offene Quellen setzen die Grenze bei 60/min, und LUDB etikettiert Nr. 39 (53/min) als „Sinus bradycardia". Das Spiel folgt dem Lehrbuch und sagt das Etikett dazu, wo es neben einer Kurve steht. Früher stand hier „Bradykardie = unter 60/min" — das widersprach §7 und ist gestrichen |
| PQ-Zeit normal 120–200 ms | Chou; Schwelle 200 ms auch in ESC-Pacing-2021; beide Grenzen gegen Lehrbuch Lektion 3 geprüft | Für die Veröffentlichung bleibt Chou am Original zu prüfen (§5) |
| PQ über 200 ms = AV-Block I. Grades | ESC-Pacing-2021; Definition: jede P-Welle wird übergeleitet, aber verzögert | |
| LUDB 39 hat PQ 214–258 ms (Median 228) | eigene Messung aus den Annotationen, Schlag für Schlag | Die Streuung ist echt: der P-Beginn ist die am schwersten zu setzende Marke. Die LUDB-Befundliste für Nr. 39 nennt **keinen** AV-Block I° (nur linksatriale und linksventrikuläre Hypertrophie); die Einstufung im Spiel folgt allein der Regel PQ > 200 ms, gerechnet aus den annotierten P- und QRS-Anfängen. Die P-Welle ist mit 137 ms (Median) verbreitert; dasselbe gilt für Nr. 23 (PQ 210 ms, Rätsel Reizleitung) |
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

- Untergrenze der PQ-Norm (120 ms): gegen das Lehrbuch geprüft (Lektion 3); für die
  Veröffentlichung noch an einer offenen Quelle (Chou, AHA-Empfehlungen) belegen.
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


---

## 7. Abgleich mit dem Lehrbuch und ergänzende offene Quellen (10.10.2026, zweiter Durchgang)

Das Lehrbuch (EKG-Kurs, Thieme 2024, 38 Lektionen) ist der **Prüfmaßstab**: Jede fachliche
Aussage im Spiel wird gegen die passende Lektion gelesen (Ergebnis in `FACHREGELN.md`, in eigenen
Worten, ohne Zitate). Es bleibt keine zitierte Quelle des Produkts, und Lektionsnummern stehen
nicht in Texten, die der Spieler sieht; wo eine Aussage belegt werden muss, steht hier eine
offene Quelle.

| Kürzel | Quelle | wofür | Lizenz / Hinweis |
|---|---|---|---|
| **OpenStax-A&P-19.2** | OpenStax, *Anatomy and Physiology 2e*, 19.2 „Cardiac Muscle and Electrical Activity". https://openstax.org/books/anatomy-and-physiology-2e/pages/19-2-cardiac-muscle-and-electrical-activity | Lage von Sinusknoten, AV-Knoten, His-Bündel, Schenkeln (linker Schenkel mit zwei Faszikeln), Purkinje-Fasern; Ersatzfrequenzen (AV-Knoten 40–60/min, His-Bündel 30–40/min, tiefer langsamer); AV-Verzögerung ca. 100 ms | CC BY-NC-SA 4.0 — nur als Faktenquelle, kein Text übernommen. Das Spiel nennt Ersatzfrequenzen nur nach Lage des Blocks, wie das Lehrbuch (Lektion 10) |
| **Lehrbuch L1/L14** | Lektionen 1 und 14 | linker Schenkel teilt sich in zwei Faszikel | Herzschema im Rätsel „Reizleitung" zeigt Stamm und zwei Faszikel (umgesetzt) |
| **Lehrbuch L2/L36** | Lektionen 2 und 36 | 50 mm/s in Deutschland üblich, 25 mm/s angloamerikanisch; 1 mm = 20 ms bei 50 mm/s; Eichung 10 mm = 1 mV; Leitungszeiten in II messen | Zirkel-Kopfzeile nennt Geschwindigkeit, Eichung, Ableitung; Zentrale nennt „5 mm bei 25 mm/s = 200 ms" |
| **Lehrbuch L7** | Lektion 7 | Frequenz aus Kästchen (300 bzw. 150 geteilt durch 10-mm-Quadrate); bei Flimmern mittlere Frequenz | Spiel rechnet 60 000 : RR; Flimmer-Schirm sagt „im Mittel etwa" |
| **Lehrbuch L8** | EKG-Kurs, Lektion 8 | Frequenzgrenzen: Norm 50–100/min, Sinusbradykardie < 50/min | Entscheidung: Das Spiel folgt dem Lehrbuch. Viele andere Quellen setzen 60/min; die Datenbank LUDB etikettiert Aufnahme 39 (53/min) als „Sinus bradycardia". Das Spiel nennt deshalb 53/min „Sinusrhythmus, langsam" und die Grenze 50 — auch am großen Monitor (korrigiert) |
| **Lehrbuch L3/L10** | Lektionen 3 und 10 | PQ 120–200 ms; AV-Block I° > 200 ms, Verzögerung im AV-Knoten; AV-Block III° mit Ersatzzentrum am Übergang (40–60/min, schmal) oder in der Kammer (30–40/min, breit); Mobitz II blockiert plötzlich | im Spiel so umgesetzt; „ein Block, bei dem plötzlich Schläge ausfallen" |
| **Lehrbuch L11** | Lektion 11 | AV-junktionaler Ersatzrhythmus bei Ausfall des Sinusimpulses | Rätsel „Reizleitung": Fall „ohne Sinusknoten" zeigt keinen Vorhofflimmer-Streifen mehr |
| **Lehrbuch L13** | Lektion 13 | kompletter Schenkelblock QRS ≥ 120 ms; Myokardschädigung plump, nicht M-förmig | im Rätsel so benannt (Nr. 24 bzw. Nr. 59) |
| **Lehrbuch L25** | Lektion 25 | Vorhofflimmern: keine P, absolute Arrhythmie, Frequenz als Mittel | Schirm „Vorhofflimmern" (Nr. 96) |
| **Lehrbuch L30** | Lektion 30 | Schrittmacher-EKG: Spike, schenkelblockartig breiter QRS | Aufnahme 74 (AV-Block III° mit Kammerschrittmacher) wird als solche benannt |
| **Lehrbuch L31** | Lektion 31 | Monitor-EKG: Rhythmus und Frequenz, keine Feinanalyse | Schirme zeigen Ableitung II echter Aufnahmen als Standbild; Zahlen als Median benannt |
| **Lehrbuch L35/L38** | Lektionen 35 und 38 | Bradykardie < 50; Sinusbradykardie unter Betablocker und bei Sportlern; PQ von P-Anfang bis Q-Anfang | stützt Dr. Falks und Marlenes Sätze; Zirkel-Regeln |

**Datenbank-Etiketten, die vom Lehrbuch abweichen** (dokumentiert, nicht korrigiert): „Sinus
bradycardia" bei 50–59/min (Nr. 39, 24, 59, 134); „Sinus tachycardia" bei Nr. 114 (Median
91/min); kein „I degree AV block" bei Nr. 39 (PQ 228) und Nr. 23 (PQ 210), dafür bei Nr. 61 (PQ
189). Das Spiel zeigt die Etiketten als Datenbankbefund und ordnet sie nach Lehrbuch ein.

**Noch zu belegen (offen):** Therapie-Entscheidungen am Monitor (Beobachten · Arzt rufen · Pacer)
stehen nicht im EKG-Kurs. Das Spiel behauptet dazu keine Kriterien mehr; falls später doch,
Beleg aus ESC-Pacing-2021 / ERC-Leitlinie hier eintragen.
