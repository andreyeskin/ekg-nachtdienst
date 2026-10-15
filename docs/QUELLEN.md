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
| **ESC-Synkope-2018** | Brignole M, et al. *2018 ESC Guidelines for the diagnosis and management of syncope.* Eur Heart J 2018;39(21):1883–1948. doi:10.1093/eurheartj/ehy037 | Volltext-PDF, Abschnitt 4.1.1, Tabellen 5 und 7 (10.10.2026); am 11.10.2026 am Online-Volltext (academic.oup.com) zusätzlich: §3.1, §3.2.1/Tab. 3, §3.2.2/Tab. 4, §4.1, §4.1.1/Tab. 5, §4.2.4.x, §6.1.1, §7.1.2, §8.1.2/Tab. 10, §8.1.3, §10 (Schlüsselbotschaften). Tabelle 6 nur über eine adaptierte Wiedergabe (siehe §5) |
| **ESC-Practical-2018** | Brignole M, et al. *Practical Instructions for the 2018 ESC Guidelines for the diagnosis and management of syncope.* Eur Heart J 2018;39(21):e43–e80. doi:10.1093/eurheartj/ehy071 | Online-Volltext 11.10.2026: Web Table 4 (vier T-LOC-Merkmale), Web Tables 5.1–5.6 (Anamnese: vor, Beginn, während/Zeugen, andere Aspekte, danach, Vorerkrankungen — darunter „kürzlicher Beginn oder Wechsel einer Medikation", Familienanamnese, Herzkrankheit, Diabetes), §1.3, §2.1.2, §2.3.1, §2.3.3 |
| **ESC-AF-2020** | Hindricks G, Potpara T, et al. *2020 ESC Guidelines for the diagnosis and management of atrial fibrillation.* Eur Heart J 2021;42(5):373–498. doi:10.1093/eurheartj/ehaa612 | nur Inhaltsverzeichnis und Abkürzungen am Online-Volltext (11.10.2026): §3.1 Definition (Tab. 3), §3.2 Diagnosekriterien, §8.1 Symptome (Tab. 6 EHRA), Fig. 3 Risikofaktoren, Fig. 5 4S-AF, §10.3.1 Alkohol, §11.1 Instabilität, §11.10 endokrin — Wortlaut der Kriterien noch nicht gelesen (§5) |
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
| Beweisend für arrhythmische Synkope wären: Sinusbradykardie dauerhaft unter 40/min, Pausen über 3 s im Wachzustand, Mobitz II, AV-Block III° | ESC-Synkope-2018, Abschnitt 4.1.1, Klasse I, Evidenzgrad C | **Nichts davon liegt bei Herrn Baum vor.** Genau deshalb endet Kapitel 1 mit Beobachtung und nicht mit einer Diagnose. Der Epilog (Erzählung, Dienst 3) sagt, der Monitor habe in der zweiten Nacht eine Pause über drei Sekunden aufgezeichnet, er sei wach gewesen — genau dieses Kriterium; keine Kurve, keine Diagnose, keine Therapie |
| TIA = fokaler Ausfall (Sprache, Kraft, Gesichtsfeld) ohne Bewusstseinsverlust; vertebrobasiläre TIA nie ohne Herdzeichen (Doppelbilder, Ataxie); Synkope ist das Gegenteil | ESC-Synkope-2018 Tabelle 4, §8.1.3; ESC-Practical-2018 Web Table 5.4 | Marlenes und Falks Antwort auf „Ist das nicht eine TIA?"; die Kurzuntersuchung (Sprache, Gesicht, Kraft seitengleich, Doppeltsehen, Finger-Nase) ist die orientierende Neurologie dazu |
| Krampfanfall gegen Synkope: Zuckungen, seitlicher Zungenbiss, langsames Wiederklarwerden sprechen für einen Anfall | ESC-Synkope-2018 §8.1.2, Tabelle 10 | Marlene: „kein Zucken, Zunge heil, nachher gleich klar" |
| Hypoglykämie: kein Diabetes, Blutzucker-Stix normal, Verlauf zu kurz | ESC-Synkope-2018 Tabelle 4; ESC-Practical-2018 Web Table 5.6 | Marlene: Stix-Wert aus den Falldaten (104 mg/dl), „er hat keinen Zucker" |
| Orthostatische Synkope: beim oder nach dem Aufstehen, Beginn oder Wechsel blutdrucksenkender Mittel; Stehblutdruck bei allen Patienten | ESC-Synkope-2018 Tabelle 5, Schlüsselbotschaft 3 | Marlene und Falk: Stehversuch ohne Abfall (142/84 → 134/80 nach 3 min), Sturz nach zehn Minuten Stehen, Medikation seit Jahren unverändert. Das Zahlenkriterium (≥ 20/10 mmHg) wird im Spiel nicht genannt (offen, §5) |
| QRS schmal (60–100 ms): die Kammern werden über das normale Leitungssystem erregt; die Verzögerung des AV-Blocks I° liegt im AV-Knoten, oberhalb der Schenkel | Lehrbuch Lektion 4, 10 (FACHREGELN) | Karte „QRS-Breite" und Vergleich QRS ↔ PQ; Falk: „langsam und lang, und schmal" |
| Getasteter Puls (52) und am Papier gemessene Frequenz sind bei 1:1-Überleitung dieselbe Größe | Lehrbuch Lektion 7 (FACHREGELN) | Vergleich Aufnahmebogen ↔ Frequenz |

---

## 4. Was das Spiel bewusst nicht behauptet

- **Nicht**, dass Herr Baums Synkopen durch den AV-Block I° erklärt sind. Sie sind
  es nach Datenlage nicht; der Block ist ein Hinweis auf eine angeschlagene
  Leitung, mehr nicht.
- **Nicht**, dass am Monitor bereits ein höhergradiger Block zu sehen ist. Dafür
  gibt es in unseren Daten keine Aufnahme mit Annotation, und eine gemalte Kurve
  kommt nicht in Frage. Der Epilog (seit 13.10.2026) **erzählt** eine Pause über
  drei Sekunden im Wachen, zeigt aber keine Kurve und stellt keine Diagnose.
- **Nicht**, dass die Bradykardie allein gefährlich ist. Unter Betablocker ist
  sie erwartbar.
- **Behandlung gehört dazu** (Entscheidung des Nutzers, 15.10.2026; die frühere Regel „Das Spiel übt
  Befunden, nicht Behandeln" ist aufgehoben): Therapie, Medikamente mit Dosierung, Eingriffe und
  Behandlungsentscheidungen der Spielerin sind erlaubt. Es gilt dieselbe Regel wie für jede fachliche
  Aussage: nur mit Beleg (Lektion in FACHREGELN.md oder Leitlinie mit Abschnitt in der Belegtabelle).
  Beispiel: Herr Baum, Epilog (§9).

## 5. Offen

- **ESC-Synkope-2018, Tabelle 6** (Risikomerkmale Major/Minor/Low-risk) wurde am 11.10.2026 nur
  über eine adaptierte Wiedergabe gegengeprüft (Tabelle 1 in *Exploration of Cardiology*,
  explorationpub.com/Journals/Tables/1012114/t1, „adapted from Brignole 2018"); der Online-Volltext
  liefert die Tabelle nicht als Text. Vor der Veröffentlichung am PDF der Leitlinie nachprüfen —
  insbesondere die Minor-EKG-Zeile „AV-Block I° mit deutlich verlängerter PQ-Zeit".
- **ESC-Synkope-2018, §4.2.1** (Stehversuch: Kriterium für orthostatische Hypotonie — Abfall des
  systolischen Drucks ≥ 20 mmHg oder des diastolischen ≥ 10 mmHg oder systolisch < 90 mmHg innerhalb
  von 3 min) ist aus dem Gedächtnis zitiert; die Zeile in `docs/faelle/aufnahme_baum.md` §4 trägt den
  Vermerk. Am Original prüfen.
- **ESC-AF-2020**: Wortlaut und Klasse der Diagnosekriterien (§3.2: 12-Kanal-EKG oder Einkanalstreifen
  ≥ 30 s mit unregelmäßigen RR ohne erkennbare P-Wellen), das Kriterium „hämodynamische Instabilität"
  (§11.1) und die Risikofaktorenliste (Fig. 3, §10.3.1, §11.10) am Volltext lesen, bevor die
  Monitor-Dialoge gebaut werden.
- **LUDB-Alter und -Geschlecht** der Aufnahmen 39, 96, 142 (und Ersatz) aus der Rohdatenbank
  nachtragen; die Figuren (68 m, 76 w, 24 m) daran anpassen.
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
stehen nicht im EKG-Kurs. Sie dürfen ins Spiel; vorher Beleg aus ESC-Pacing-2021 / ERC-Leitlinie
hier eintragen.

---

## 8. Belegtabelle Fallakten (11.10.2026)

Jede Zeile gehört zu einer Aussage in `docs/faelle/*.md`; der Spieler sieht nie die Quelle, nur das
Merkmal. Lehrbuchbelege stehen in `FACHREGELN.md` (eigene Worte, Lektionsnummer) und werden hier nicht
wiederholt.

### 8a. Herr Baum (`aufnahme_baum.md`)

| Aussage | Beleg | Anmerkung |
|---|---|---|
| T-LOC hat vier Merkmale: kurze Dauer, Verlust der Haltungskontrolle, keine Reaktion, Amnesie; alle vier → T-LOC sicher | ESC-Synkope-2018 §4.1; ESC-Practical-2018 Web Table 4 | |
| Synkope = T-LOC durch globale Hirnminderdurchblutung, rascher Beginn, kurz, spontane vollständige Erholung; Klassen reflektorisch / orthostatisch / kardial | ESC-Synkope-2018 §3.1, §3.2.1, Tabelle 3 | |
| Bedingungen, die als Synkope fehlgedeutet werden: generalisierte Anfälle, komplex-partielle/Absencen, psychogene Pseudosynkope, Sturz ohne T-LOC, Kataplexie, intrazerebrale/Subarachnoidalblutung, vertebrobasiläre TIA, Karotis-TIA, Subclavian-Steal, metabolisch (Hypoglykämie, Hypoxie, Hyperventilation), Intoxikation, Herzstillstand, Koma | ESC-Synkope-2018 §3.2.2, Tabelle 4 | |
| Vertebrobasiläre TIA: immer fokale Zeichen, meist ohne Bewusstseinsverlust, wenn doch, länger; Karotis-TIA: Bewusstsein erhalten; „TIA = fokales Defizit ohne LOC, Synkope das Gegenteil"; Parese, Ataxie, Hirnstammzeichen → vertebrobasilär | ESC-Synkope-2018 Tabelle 4, §8.1.3; ESC-Practical-2018 Web Table 5.4 | Grundlage der Option „Ist das nicht eine TIA?" |
| Epileptischer Anfall vs. Synkope: Myoklonien < 10, asynchron, asymmetrisch vs. 20–100 synchron; Zungenbiss Spitze/selten vs. seitlich; Wiederklarwerden 10–30 s vs. Minuten; Verwirrtheit danach; Inkontinenz, Augen offen, Müdigkeit, blaues Gesicht von begrenztem Nutzen | ESC-Synkope-2018 §8.1.2, Tabelle 10; ESC-Practical-2018 Web Tables 5.3–5.5 (Bewegungen ab Beginn → Epilepsie, nach LOC → Synkope; Dauer < 30 s Synkope, > 1 min Anfall; „sofort klar" → Synkope) | |
| Psychogene Pseudosynkope: scheinbare Bewusstlosigkeit Minuten bis Stunden, hohe Frequenz bis mehrmals täglich; Augen meist geschlossen | ESC-Synkope-2018 Tabelle 4, §7.1.1–7.1.2; ESC-Practical-2018 Web Table 5.4 | |
| Hypoglykämie: metabolische Störung, die als Synkope fehlgedeutet wird; Verlauf zu lang für T-LOC | ESC-Synkope-2018 Tabelle 4; ESC-Practical-2018 Web Table 5.6 (Diabetes) | |
| Merkmale der Erstbewertung: Reflex (lange Vorgeschichte, v. a. vor 40; Auslöser Anblick/Geräusch/Geruch/Schmerz; langes Stehen; Mahlzeit; Hitze/Gedränge; Prodrom Blässe/Schwitzen/Übelkeit; Kopfdrehung/Karotisdruck; kein Herzleiden); OH (beim/nach dem Aufstehen, langes Stehen, nach Belastung, postprandial, zeitlicher Zusammenhang mit Beginn/Dosisänderung vasodepressiver Mittel oder Diuretika, autonome Neuropathie/Parkinson); kardial (unter Belastung/im Liegen, plötzliches Herzrasen davor, Familie, strukturelle/koronare Herzkrankheit, EKG: bifaszikulärer Block, QRS ≥ 0,12 s, Mobitz I oder AV-Block I° mit deutlich verlängerter PQ, nsVT, Präexzitation, QT, frühe Repolarisation, Brugada, ARVC, LVH/HCM; asymptomatische Sinusbradykardie 40–50 „ohne negativ chronotrope Medikation") | ESC-Synkope-2018 §4.1.1, Tabelle 5 | am Online-Volltext gelesen 11.10.2026 |
| Medikamentös induzierte OH ist die häufigste OH-Form (Vasodilatatoren, Diuretika, Phenothiazine, Antidepressiva); Synkope wahrscheinlicher/schwerer unter blutdrucksenkender Medikation | ESC-Synkope-2018 Tabelle 3 | |
| Medikamentenanamnese: „kürzlicher Beginn oder Wechsel einer Medikation" als Anamnesefrage (OH, Reflex, langes QT); Hypertonie → OH durch Medikation; Familienanamnese plötzlicher Tod < 40; Herzkrankheit; frühere Ohnmachten; Verletzungen | ESC-Practical-2018 Web Table 5.6 (Vorerkrankungen), §2.3.1, §2.3.3 | Beleg dafür, dass die Medikamentenfrage Pflichtteil der Synkopen-Anamnese ist (KONZEPT §1.3) |
| Polypharmazie, kardiovaskuläre, psychotrope und dopaminerge Mittel erhöhen Synkopen- und Sturzrisiko; negativ dromotrope und chronotrope Mittel beim älteren Patienten sorgfältig bewerten | ESC-Synkope-2018 §6.1.1 | Bisoprolol |
| Bei allen Patienten: vollständige Anamnese, körperliche Untersuchung einschließlich Stehblutdruck, Standard-EKG; bei Verdacht auf arrhythmische Synkope sofortige EKG-Überwachung bei Hochrisiko | ESC-Synkope-2018 §10 Schlüsselbotschaften 3 und 4; §4.1.1 | |
| Hochrisiko → Überwachung dort, wo Reanimation möglich ist; In-Hospital-Monitoring bei Hochrisikomerkmalen, v. a. unmittelbar nach der Synkope (Ausbeute 1,9–17,6 %) | ESC-Synkope-2018 §4.1.2, §4.2.4.1 | Klasse/Level nicht aus dem Online-Text lesbar |
| Risikomerkmale Major (neuer Brustschmerz/Atemnot/Bauch-/Kopfschmerz; unter Belastung/im Liegen; Herzrasen unmittelbar davor; schwere strukturelle/koronare Herzkrankheit; systolisch < 90; Blutung; Bradykardie < 40 wach; unklares Systolikum; EKG: Ischämie, Mobitz II, III°, langsames VHF < 40, Sinusbradykardie < 40 / SA-Block / Pausen > 3 s wach, Schenkelblock/IVCD/Hypertrophie/Q, VT, Gerätefehlfunktion, Brugada Typ 1, QTc > 460) und Minor (ohne Vorwarnung oder Prodrom < 10 s; Familie SCD jung; im Sitzen; EKG: Mobitz I / AV-Block I° deutlich verlängert, Sinusbradykardie oder langsames VHF 40–50, paroxysmale SVT/VHF, Präexzitation, kurzes QT, atypisches Brugada, rechtspräkordiale T-Negativierung/Epsilon); Minor zählen nur mit struktureller Herzkrankheit oder auffälligem EKG | ESC-Synkope-2018 Tabelle 6 — gegengeprüft über adaptierte Wiedergabe (§5) | Herr Baum: Minor „ohne Prodrom" + auffälliges EKG |
| Synkope ohne Prodrom, Verletzung durch die Synkope → eher Beobachtung/Aufnahme | ESC-Synkope-2018 Tabelle 7 | |

### 8b. Frau Lindner (`monitor.md`)

| Aussage | Beleg | Anmerkung |
|---|---|---|
| Vorhofflimmern: Diagnose am 12-Kanal-EKG oder Einkanalstreifen ≥ 30 s (unregelmäßige RR, keine erkennbaren P-Wellen) | ESC-AF-2020 §3.1 (Tab. 3), §3.2 | Wortlaut/Klasse am Original zu prüfen (§5) |
| Symptomlast (EHRA-Skala) und 4S-AF (Schlaganfallrisiko, Symptomschwere, Flimmerlast, Substrat) als Charakterisierung | ESC-AF-2020 §8.1 (Tab. 6), Fig. 5 | begründet die Fragen „Beschwerden?", „seit wann?" |
| Risikofaktoren/Komorbiditäten: Hypertonie, Alkohol, Schilddrüse u. a. | ESC-AF-2020 Fig. 3, §10.3.1, §11.10 | das Spiel notiert nur, behauptet keine Ursache |
| Hämodynamische Instabilität als Kriterium für dringliches Handeln | ESC-AF-2020 §11.1 | nur das Kriterium; am Original zu prüfen |
| Monitor erkennt tachykardes/bradykardes VHF sicher; jede Auffälligkeit → 12-Kanal-EKG | Lehrbuch Lektion 31 (FACHREGELN) | |
| mittlere Frequenz: Komplexe in 6 s × 10 | Lehrbuch Lektion 7 (FACHREGELN) | gegen `schlaege` im gezeigten Fenster geprüft |

### 8c. Lehrsaal (`lehrsaal.md`)

Alle Aussagen stammen aus dem Lehrbuch (Lektionen 1–8, 17, 34–38) und stehen in `FACHREGELN.md`.
Offene Quellen für die Veröffentlichung: Elektrodenpositionen und Ableitungsgruppen nach
AHA-EKG-2007-I (Kligfield 2007, bibliografisch nachgewiesen in §2; Stelle noch zu lesen); Ampel-Regel
der Kabelfarben entspricht IEC 60601-2-25 (Farbcode Europa) — noch nicht am Original geprüft.

## 9. Behandlung im Epilog von Herrn Baum (15.10.2026)

| Aussage im Spiel | Beleg | Anmerkung |
|---|---|---|
| Zuerst wird das Bisoprolol abgesetzt; machen die Tabletten die Pausen, braucht es keinen Schrittmacher | ESC-Pacing-2021 (Glikson M et al., Eur Heart J 2021;42:3427–3520, doi:10.1093/eurheartj/ehab364) §5.1.1.1: bei reversiblen Ursachen ist deren Korrektur nötig, ein permanenter Schrittmacher nicht indiziert; §5.1.1.2: Bradyarrhythmien unter Medikamenten lassen sich durch Dosisreduktion oder Absetzen statt Schrittmacher behandeln; §3.3/Tab. 6: Betablocker als Ursache von Sinusbradykardie und AV-Block | Volltext am 15.10.2026 gelesen (academic.oup.com), Klassen/Evidenzgrade stehen in Bildtabellen und wurden nicht übernommen |
| Erneute Pause im Wachen ohne Betablocker → Schrittmacher | ESC-Pacing-2021 §5.1.1.1: Schrittmacher bei Sinusknotenerkrankung nur, wenn die Bradykardie symptomatisch ist; §5.4 / Abb. 7: symptomatische Asystolie > 3 s (Sinusarrest, AV-Block oder beides) | Mechanismus der Pause wird im Spiel nicht genannt (keine annotierte Aufnahme) |
| Zweikammer-Schrittmacher | ESC-Pacing-2021 §5.1.2: DDD(R) ist bei Sinusknotenerkrankung der Modus erster Wahl; beim AV-Block ebenfalls ein Zweikammersystem üblich | Keine Programmierangaben im Spiel |
| Drei Tage ohne Betablocker | Erzählte Zeitspanne; Bisoprolol hat eine Halbwertszeit von etwa 10–12 h, nach drei Tagen ist die Wirkung abgeklungen | Pharmakologie, Standardwissen |

