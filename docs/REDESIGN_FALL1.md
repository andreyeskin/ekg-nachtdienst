# Redesign Fall 1 — Herr Konrad Baum, 68: „Darf er heim?"

Entwurf, 18.10.2026. Antwort auf die Rückmeldung des Nutzers („unverständlich, zerrissen, was lehrt er?").
Noch nichts gebaut: Dieses Blatt ist der Vorschlag, der vor dem Umbau freigegeben wird. Grundlage: `docs/KONZEPT.md`
§1, `docs/faelle/aufnahme_baum.md` (Akte, bleibt fachlich die Basis), die Skills `fallakte` und `dialoge`,
`docs/FACHREGELN.md`, `docs/QUELLEN.md`. Kurve unverändert: LUDB 39, Ableitung II, 10 s (Sinusrhythmus 53/min,
PQ 228 ms, QRS 86 ms). Nichts wird gemalt, nichts behauptet, was die Aufnahme nicht zeigt.

Lesehilfe: §1–§3 sind die Diagnose und der neue Bogen (zuerst lesen). §4–§7 sind das Drehbuch mit allen
Dialogen. §8–§10 sind Umgebung, Kapitel 2 und Bewegung. §11–§13 Umbau, Belege, offene Entscheidungen.

---

## 1. Diagnose des Ist-Zustands

Grundlage: Durchlauf `bau/durchlauf/01…21` und `26–28`, die Texte in `text/de/aufnahme_baum.json`, die Struktur in
`web/faelle/aufnahme_baum.js`. Die Diagnose des Koordinators ist richtig; hier mit Fundstellen und drei Ergänzungen.

### 1.1 Das Lernziel ist zweigeteilt, und der Teil mit Gewicht (die Messung) beantwortet die Fallfrage nicht

Die Akte nennt zwei Ziele (messen; Synkope abklären). Im Spiel trägt die Messung die ganze Mechanik (Zirkel, Karten,
Falks „Zahlen"), aber die Geschichte entwertet sie sofort: *„Dann erklären die Tabletten die Zahlen. Die Zahlen
erklären nicht, warum er auf dem Boden lag."* (`baum.falk.tabletten`). Die Spielerin hat zehn Minuten gemessen und
hört: Das war's nicht. Das ist eine Antiklimax. Die Entscheidung kommt dann nicht aus ihren Befunden, sondern aus
Falks Bauch: *„Nicht, weil ich weiß, was es ist. Weil ich es nicht weiß."* (`baum.falk.entscheidung2`). Und die
Auflösung kommt Tage später im Epilog, als Erzählung. Der Fall endet also dreimal: einmal mit „weiß ich nicht",
einmal mit „er geht nach oben", einmal mit „Schrittmacher". Keines dieser Enden gehört der Spielerin.

### 1.2 Keine dramatische Frage, nichts auf dem Spiel

Niemand will etwas, das die Spielerin verhindern oder erreichen müsste. Herr Baum sitzt brav (*„Da war ich halt
brav."*), Marlene hat alles schon gemessen, Falk kommt, wenn gerufen. Es gibt keinen Widerstand, keine Wendung,
keinen Zeitdruck. Die Uhr läuft, aber nichts hängt an ihr. Die Frage „Was passiert, wenn ich es falsch mache?" hat
keine Antwort, weil nichts passieren kann.

### 1.3 Zerrissen: Fenster, Hubs, Checkliste

Der Fall ist eine Folge von Modalfenstern über demselben Standbild. Die Anamnese ist ein Menübaum mit vier Hubs
(*„Andere Fragen zu dem Moment."*, *„Noch etwas zu den Tabletten."*, *„Noch etwas zu Ihnen und Ihrer Familie."*,
*„Noch einmal zu dem Moment."*) und einem „Zurück". Zehn Pflichtfragen werden im Stand der Schicht als Liste
angemahnt (*„In der Anamnese fehlt noch: die Vorwarnung, die Dauer, …"*). Das ist eine Checkliste mit
Gesprächsfassade. Dazu das Pendeln: Marlene (Szenenbild) → Herr Baum → Untersuchung → Marlene (Expertenfragen) →
Wagen → Marlene (Bericht) → Falk (Porträt) → Wagen (Rückweg) → Falk. Screenshot 19 zeigt das Ergebnis: Falk
spricht als Porträt vor dem leeren Raum, Herr Baum sitzt drei Meter entfernt auf der Bank und ist nicht beteiligt.

### 1.4 Dialoge: Pointen statt Sätze

Fast jede Replik ist ein Aphorismus oder ein Rätselsatz:
- Marlene: *„Ich sag dir nichts vor. Sonst suchst du nachher nur, was ich dir in den Kopf gesetzt hab."* (das
  Philosophen-Muster aus dem Skill `dialoge` §2: die Figur spricht ein Prinzip aus).
- Marlene doziert Leitlinie: *„Beweisen würde: ein Puls dauerhaft unter vierzig, eine Pause über drei Sekunden im
  Wachen, oder ein Block, bei dem plötzlich Schläge ausfallen."* (`baum.marlene.beweis`) und *„Es beweist nichts,
  aber es steht in jeder Liste der Warnzeichen."* (`baum.marlene.vorwarnung`). Das ist Tabelle 6 im Kittel.
- Falk: *„Bevor Sie etwas sagen: Ich will nicht hören, was Sie vermuten."* (`baum.falk.start.erst`), *„sonst läge
  die halbe Sportmannschaft auf dem Boden"* (`baum.falk.halb`), *„Nicht, weil ich weiß, was es ist. Weil ich es
  nicht weiß."* Das ist das Klischee des grantigen Mentors; niemand redet so um sieben Uhr früh.
- Herr Baum ist am besten (*„Als hätte jemand das Licht ausgemacht"*), aber auch er bekommt Pointen (*„Mit
  achtundsechzig fang ich damit an."*, *„Ich erzähl's der Tochter sowieso alles noch einmal."*).
Tennismatch-Muster: alle Repliken gleich lang, niemand unterbricht, niemand ist müde, niemand telefoniert.

### 1.5 Realismus

- Ein Synkopen-Patient sitzt in der Notaufnahme auf der Wartebank statt auf einer Liege; der Stehversuch ist seit
  06:30 gemacht, aber kein EKG, obwohl das EKG zur Erstbewertung gehört (ESC-Synkope-2018 §4.1, Schlüsselbotschaft 3)
  und in Wirklichkeit meist die Pflege gleich bei der Triage schreibt. Im heutigen Text fehlt jeder Grund dafür.
- Ein 68-Jähriger kommt nach einer Ohnmacht um sechs Uhr früh *zu Fuß* (*„weil er die Tochter nicht wecken
  wollte"*). Die Tochter, die ihn fand, kommt nicht vor.
- Die Rhythmusfrage bietet „Kammertachykardie" bei 53/min an (Screenshot 12). Das ist keine Irrmöglichkeit, das
  ist Dekoration (Skill `dialoge` §3.1: „keine falsche Option ist albern").
- Falk kommt nur, um Zahlen abzufragen, und untersucht den Patienten nicht; er spricht nie mit ihm.
- Keine anderen Patienten, kein Telefon, kein Schichtwechsel, keine Rettung, keine Reinigung. Die Aufnahme ist ein
  leeres Bühnenbild mit zwei Figuren, die atmen.

### 1.6 Kapitel 2: „Welches Bett ist Herr Baum?"

An jeder echten Zentrale steht an jedem Schirm Bett und Name. Niemand identifiziert einen Patienten an der Kurve;
wer es täte, wäre ein Sicherheitsrisiko. Falk „nimmt die Namen weg" (Screenshot 26) ist ein Rätsel, das es nur im
Spiel gibt. Es muss weg (§9).

### 1.7 Umgebung

Es bewegt sich: das Atmen der Figuren (2,5 px), die Parallaxe, die Kurve am Wagen, die Uhr. Sonst nichts. Das
Sonnenaufgangslicht steht um 07:38 noch genauso wie um 06:40 (Screenshot 20 gegen 01). Kein Mensch im Flur.

### 1.8 Drei Ergänzungen zur Diagnose des Koordinators

1. **Die richtige Antwort ist nicht erkennbar als Antwort.** Die Logik „keine Vorwarnung zählt nur mit auffälligem
   EKG; das EKG ist auffällig; also Monitor" steht nur in der Akte (§4) und in keiner Rückmeldung, die die Spielerin
   zu sehen bekommt. Sie kann den Fall durchspielen, ohne diese Kette je zu lesen.
2. **Die Spielerin entscheidet nie.** Jede Wahl ist eine Frage („Ist das nicht eine TIA?") oder ein Bericht
   („Sinusrhythmus, 53, PQ 228"). Die einzige Entscheidung des Falls (Monitor) trifft Falk; die Spielerin klickt
   „Und jetzt? Nach Hause?" und bekommt die Entscheidung erzählt.
3. **Der Epilog verrät, dass Kapitel 1 unvollständig war.** Weil die Pause erst Tage später kommt, lernt die
   Spielerin rückblickend, dass die Entscheidung am Morgen richtig war. Das ist gut gemeint, aber die Lehre
   („Monitor war richtig, obwohl der Streifen nichts bewies") muss *am Morgen* ankommen, in ihrer eigenen
   Begründung, nicht als nachgereichte Pointe.

---

## 2. Lernziel und dramatische Frage

### 2.1 Lernziel (ein Satz, prüfbar)

**Bei einer Synkope entscheiden Anamnese und EKG gemeinsam, wer heimgehen darf: Fehlt die Vorwarnung und ist das
EKG nicht normal (hier Sinusrhythmus 53/min unter Betablocker mit AV-Block I°, PQ 228 ms), bleibt der Patient am
Monitor, auch wenn das Ruhe-EKG die Ohnmacht nicht erklärt.**

Dazu die Fertigkeit, die der Fall trägt: Sinusrhythmus erkennen, Frequenz und PQ-Zeit mit dem Zirkel messen,
PQ > 200 ms als AV-Block I° einordnen (Lektion 7, 8, 10). Die Messung bekommt damit Gewicht: Sie erklärt die Ohnmacht
nicht, aber sie entscheidet, ob die harmlose Erklärung noch trägt.

### 2.2 Warum diese Kette fachlich hält (am Original geprüft, 18.10.2026)

ESC-Synkope-2018, Tabelle 6 und §4.1.2 (akzeptiertes Manuskript, Postprint der Universität Florenz; QUELLEN §5
ist damit zu schließen), in eigenen Worten:

1. **Niedriges Risiko** verlangt alle Low-risk-Merkmale, darunter ausdrücklich „normales EKG" (Nr. 11),
   „unauffällige Untersuchung" (Nr. 10) und ein Prodrom, wie es zur Reflexsynkope gehört, oder einen typischen
   Auslöser (langes Stehen zählt dazu). Herr Baum hat weder Vorwarnung noch normales EKG. Er ist also **nicht
   niedrig**.
2. **Minor-Ereignismerkmal** „keine Vorwarnung oder Prodrom < 10 s" zählt nur zusammen mit struktureller
   Herzkrankheit **oder abnormem EKG** (Fußnote der Tabelle). „Abnormes EKG" definiert die Leitlinie nicht; ein
   AV-Block I° (PQ > 200 ms) ist nach dem Kurs nicht normal (Lektion 3, 10). Das trägt „nicht niedrig", **nicht**
   „hoch": Die einzige EKG-Zeile zum AV-Block I° verlangt eine *deutlich* verlängerte PQ-Zeit und gilt nur, wenn die
   Anamnese zu einer arrhythmischen Synkope passt; 228 ms sind nicht „deutlich" (ESC-Pacing-2021 §5.2.1.1 nennt
   als „markiert" ≥ 300 ms, geprüft). Das Spiel sagt deshalb überall „nicht normal" und „nicht niedrig", nie
   „Hochrisiko".
3. **Weder niedrig noch hoch:** §4.1.2 empfiehlt Beobachtung in der Notaufnahme oder einer Synkopeneinheit statt
   Aufnahme (Klasse I B). Das ist Falks Entscheidung: **Beobachtung am Monitor, keine Entlassung.** §4.2.4.1
   (Überwachung im Haus, Bett oder Telemetrie, bei Merkmalen, die eine arrhythmische Synkope nahelegen; Ausbeute
   1,9–17,6 %; Empfehlung I C für Hochrisiko) stützt die Form der Beobachtung, nicht die Einstufung.
4. **Tabelle 7** („Synkope ohne Prodrom" → Beobachtungseinheit; „Verletzung durch die Synkope" → Aufnahme;
   Spalten am Postprint bestätigt) dient nur als Stütze: Sie setzt Hochrisiko-Merkmale voraus, die Herr Baum nicht
   hat.
5. **Was nicht gilt:** Zwei Ereignisse in zwei Tagen sind in Tabelle 6 kein Merkmal; sie sind das Gegenteil des
   Low-risk-Merkmals „lange Vorgeschichte gleichartiger harmloser Ohnmachten" (Nr. 8), und Tabelle 5 nennt die
   lange Vorgeschichte (vor allem vor 40) als Reflex-Merkmal. Alter kommt in Tabelle 6 nicht vor. Im Spiel steht
   „Mit achtundsechzig fängt man nicht mit Kreislaufgeschichten an" (Falk), nie „zweimal = gefährlich". Die
   Wendung (zweites Ereignis) erhöht den Einsatz; der fachliche Kipppunkt bleibt die PQ-Zeit in Takt 4.
6. **Orthostase:** Das Low-risk-Merkmal „beim Aufstehen aus dem Liegen oder Sitzen" (Nr. 7) und das OH-Merkmal
   „beim oder nach dem Aufstehen" (Tab. 5) werden im Gespräch ausgeschlossen, mit einer eigenen Pflichtfrage
   („Waren Sie grad erst aufgestanden?": seit sechs auf, eine Minute beim Kocher). Der Stehversuch ist negativ
   (§4.2.2.1: Abfall ≥ 20/10 mmHg oder systolisch < 90 mmHg; geprüft).
7. **Betablocker:** Er erklärt die langsame Frequenz und eine zähe Überleitung (Pharmakologie, QUELLEN §3;
   ESC-Pacing-2021 §3.3/Tab. 6), keine Ohnmacht ohne Vorwarnung. Pausieren stützt sich auf §5.1.1.1 (reversible
   Ursachen korrigieren) und Tab. 6; der Satz „in vielen Fällen bleiben sie bestehen" (§5.1.1.2) steht im Abschnitt
   zur Brady-Tachy-Form und wird nur sinngemäß herangezogen. Zeltser 2004 bleibt Hintergrund (§12).

Die Kette: *keine Vorwarnung* + *EKG nicht normal* → **nicht niedrig** → Beobachtung am Monitor statt Entlassung.
Zweimal, Verletzung und 68 stützen, tragen aber nicht allein. Genau so argumentiert die Spielerin bei Falk (§6),
und genau so steht es in den Rückmeldungen.

### 2.3 Die dramatische Frage

**„Darf Herr Baum heim?"** Sie steht vom ersten Bild an im Raum: Herr Baum hat die Jacke schon an. Marlene sagt
im zweiten Satz, dass Falk um viertel nach sieben genau das fragen wird. Die Tochter fragt es am Telefon. Falk
fragt es, weil er die Koje braucht, und hat schon eine Antwort (Kreislauf, heim). Alles, was die Spielerin tut,
verschiebt die Antwort. Am Ende sagt **sie** es Herrn Baum, in seiner Sprache, und löst seine eigentliche Sorge.

Die Wendung: Um sieben Uhr sagt Herr Baum, was er niemandem gesagt hat. Es war nicht das erste Mal. Das erhöht
den Einsatz: Die Notiz des Nachtdienstes kannte nur die halbe Geschichte, und die Spielerin ist die Einzige, die
das weiß. Fachlich kippt die Notiz erst in Takt 4, mit der PQ-Zeit; das zweite Ereignis stützt, es entscheidet nicht.

### 2.4 Was die Spielerin danach kann

1. An einem Streifen Sinusrhythmus feststellen, Frequenz und PQ messen, PQ > 200 ms als AV-Block I° benennen.
2. Sagen, warum „keine Vorwarnung" nur zusammen mit einem auffälligen EKG oder einer Herzkrankheit zählt.
3. Sagen, was ein Ruhe-EKG bei Synkope nicht beweisen kann und was es bräuchte (Pause > 3 s im Wachen, Mobitz II,
   AV-Block III°, Sinusbradykardie < 40/min).
4. Eine Übergabe nach ISBAR geben, auch wenn der Oberarzt unterbricht.
5. Einem Patienten in Laiensprache sagen, warum er bleibt, ohne zu drohen und ohne einen Revers vorzuschieben.
6. Eine Synkopen-Anamnese führen, die das zweite Ereignis findet, weil sie danach fragt.

---

## 3. Der Bogen in sieben Takten (Szene und Sequel, Skill `handlung` §2)

Dienst 1, Montag. Spielzeit 06:40 bis 07:40 (eine Stunde Spielzeit; 15–25 Minuten echte Zeit, beim ersten
Durchlauf mit Zirkel eher 25). Ein Raum. Figuren: Schwester Marlene (Nachtdienst seit 19:00), Herr Baum, Dr. Falk
(Tagdienst, ab 07:15), Sabine Baum (Tochter, nur am Telefon), Erzähler. Off-screen: Dr. Steiner (Journaldienst,
seit 06:30 im Schockraum), Andrea (Tagdienst-Pflege, ab 07:00 am Tresen), Frau Kainz (Nachbarin), die Hündin Senta.
Die Spielfigur ist KPJ-Studentin am ersten Tag ihrer Rotation (ART_BIBLE §5; Entscheidung §13).

Dramatische Frage und Lernziel sind derselbe Satz: *Darf er heim?* (§2). Jeder Takt verschiebt die Antwort.
**Die Uhr hat Zähne:** jede Frage und jede Handlung rückt sie um eine Minute vor, jede Messung um zwei; um 07:15
kommt Falk in jedem Fall.

| Takt | Art | Zeit | Ziel der Spielerin | Widerstand / Konflikt | Wendung (Szene) bzw. Reaktion → Dilemma → Entscheidung (Sequel) |
|---|---|---|---|---|---|
| **1 Haken** | Szene | 06:40–06:44 | ankommen, wissen, was zu tun ist | Marlene ist seit zwölf Stunden da und hat keine Hand frei; Herr Baum steht mit Jacke in einer Koje ohne Monitor; die Notiz des Journaldienstes hat schon eine Antwort („vasovagal") | **„Ja, aber":** Sie bekommt den Fall, aber mit Frist (Falk, 07:15, will die Koje) und mit einer fertigen Antwort, die sie prüfen muss, nicht übernehmen |
| **2 Gespräch** | Szene | 06:45–07:00 | das Ereignis verstehen, ihn zum Sitzen bringen | er will heim (Senta um acht), spielt es herunter, die Zeugin ist nicht da; die Uhr läuft mit jeder Frage | **„Nein, und außerdem":** Es war nicht das erste Mal. Gestern, Haltestelle beim Friedhof. Und: „Sagen S' es der Sabine nicht." Der Einsatz steigt; fachlich entscheidet das noch nichts |
| **3 Ordnen** | Sequel | 07:00–07:02 | — | — | **Reaktion:** Marlene schiebt den Wagen an die Koje und fragt „Und? Darf er?"; weiß die Spielerin vom zweiten Ereignis: „Das hat er mir nicht gesagt." Verdachtsliste ordnet sich um. **Dilemma:** Dem Oberarzt sagen, der Tochter nicht? **Entscheidung:** Was sie ihm verspricht (Flag `versprochen`), wird in Takt 6 und 7 erinnert |
| **4 Befund** | Szene | 07:02–07:10 | das EKG schreiben, Rhythmus, Frequenz, PQ | Schichtwechsel, niemand hilft beim Kleben; das Handy leuchtet: die Tochter; er kann sich nicht rühren | **„Ja, aber":** Die Zahlen sind klar (Sinus, {hf}, PQ {pq}). Ihre Bedeutung nicht: nicht normal, aber kein Beweis. Und die Tochter: kein Zucken, „die Tabletten liegen noch am Tisch". Hier kippt die Notiz des Journaldienstes |
| **5 Bedeutung** | Sequel | 07:10–07:14 | — | — | **Reaktion:** Karten, Vergleich PQ ↔ Medikamente, Verdachtsliste: „Herzrhythmus: nicht bewiesen, nicht ausgeschlossen". **Dilemma:** Was sage ich Falk zuerst, und was empfehle ich? **Entscheidung:** Knopf im Stand „Zum Tresen, Falk ist da" (ab `ekg_geschrieben`; stellt die Uhr auf 07:15, falls früher) |
| **6 Höhepunkt** | Szene | 07:15–07:28 | Falk überzeugen, dass er bleibt (oder: sich überzeugen lassen) | Falk hat zwölf Minuten, eine fertige Meinung (Kreislauf) und braucht die Koje; er unterbricht; jede schwache Begründung bekommt eine Gegenfrage | **„Ja, aber":** Er bleibt. Falk sagt ihm den Grund in einem Satz; Herr Baum will ihn von *ihr* noch einmal hören. Und die Tabletten-Frage ist ihre |
| **7 Ausklang** | Sequel + kurze Szene | 07:30–07:40 | dass er bleibt, freiwillig | er bietet an, „alles zu unterschreiben"; die Senta | **Entscheidung der Spielerin, in Laiensprache**, und die Senta gelöst (Frau Kainz). Schlussbild: Jacke über dem Sessel, Mütze bleibt auf, Marlenes Stuhl leer, die Kanne weg. Epilog in Dienst 3 |

**Branch-and-Bottleneck.** Verzweigt wird innerhalb der Takte (welche Fragen über den Kern hinaus, Irrwege, Ton
gegenüber Herrn Baum und der Tochter, Reihenfolge der Argumente). Engpässe, an denen alle Wege zusammenlaufen:

1. Kern der Runde 1 (Ereignis, Vorwarnung, „grad erst aufgestanden?"); danach ist der Wagen frei.
2. Marlene schiebt den Wagen an die Koje (fester Sequel, Takt 3), bevor das EKG geschrieben werden kann.
3. EKG geschrieben; Rhythmus bestimmt. Frequenz und PQ holt Falk sonst ab (Rückweg).
4. Falk um 07:15, in jedem Fall. Kern der Runden 2 und 3 (Tabletten; „schon einmal?") und alles Ausgelassene
   fragt er in der Übergabe ab und schickt zum Patienten (bestehender Rückweg); ist das EKG noch nicht
   geschrieben, wartet er („Schreiben Sie, ich les solang.", Flag `falk_gewartet`).
5. Falks Entscheidung: Monitor (jeder Argumentationsweg endet hier; der Weg „heim" wird widerlegt, nicht bestraft).
6. Herr Baum bleibt (jeder Weg des Schlussgesprächs endet hier; der Irrweg kostet eine Runde und einen Satz).

**Flags mit sichtbarer Folge** (mehr nicht; `web/motor/fall.js`):

| Flag | gesetzt wenn | Folge, die man sieht |
|---|---|---|
| `versprochen` | die Spielerin sagt „Das bleibt unter uns" | Falk: „Steht nicht am Bogen." Spielerin muss es trotzdem sagen; Herr Baum im Schlussgespräch: „Sie haben's ihm gesagt." / „Dem Arzt. Nicht der Sabine." |
| `anruf_spaeter` | „Das kann warten, erst das EKG" | Sabine ruft nach dem Streifen noch einmal: „Ich hab dreimal angerufen." |
| `tochter_beruhigt` | am Telefon „wahrscheinlich nur der Kreislauf" | Tochter am Ende des Anrufs erleichtert; Epilog: sie fragt, warum du am Montag „Kreislauf" gesagt hast |
| `tochter_verraten` | am Telefon das zweite Ereignis erzählt | Herr Baum im Schlussgespräch: „Die Sabine hat's gewusst, wie sie angerufen hat. Von Ihnen." Die Senta-Lösung schreibt er der Tochter zu, nicht der Spielerin |
| `heim_empfohlen` | ISBAR-Zeile R „kann heim" | Falks Gegenrede läuft in umgekehrter Rolle (§6.3); Karte Übergabe trägt beide Sätze |
| `brady_argument` | „Bradykardie, {hf}. Das erklärt die Ohnmacht." oder „Puls {hf}, das ist eine Bradykardie." | Falk bei der Tabletten-Frage: „Vorhin war Ihnen {hf} zu langsam. Jetzt geben Sie ihm die Bremse dazu?" |
| `falk_gewartet` | 07:15 ohne geschriebenes EKG | Falk liest am Tresen, die Übergabe beginnt später; Marlene beim Abschied: „Den Falk hast du warten lassen." |
| `revers` | „Dann unterschreiben Sie einen Revers" | Marlene beim Abschied: „Revers hat er dir angeboten." |
| `senta_geloest` | Frau Kainz genannt | Epilog: „Die Senta hat die Frau Kainz bis zum Parkplatz gebracht." |

Warum sich das wie *eine* Geschichte anfühlt: eine Frage (heim?), eine Frist, die drückt (die Uhr läuft mit jeder
Frage), ein Gegenspieler mit guten Argumenten (Falk), eine Wendung, die aus dem Gespielten folgt (die Frage „schon
einmal?" steht im Fragenkatalog jeder Synkopen-Anamnese), ein Geheimnis mit Preis (die Tochter) und ein Ende, das
die Spielerin selbst spricht. Kein Hub, kein „Zurück", keine Mahnliste; was fehlt, fragt Falk.

---

## 4. Die Verdachtsliste

Ersetzt die Pflichtfragen-Checkliste im Stand der Schicht. Sie ist der sichtbare rote Faden: jeder Befund streicht
oder verstärkt einen Eintrag, mit einem Satz Grund. Die Spielerin sieht, *wofür* sie fragt.

### 4.1 Einträge und Zustände

Acht Einträge, in Laiensprache mit Fachwort in Klammern (so steht es auch auf der Karte):

1. Reflex (vasovagal, situativ)
2. Kreislauf im Stehen (orthostatisch)
3. Herzrhythmus (Pause, Block, Rasen)
4. Herz-Struktur (Klappe, Muskel, Durchblutung)
5. Krampfanfall
6. Schlaganfall / TIA
7. Unterzucker
8. Sturz ohne Bewusstlosigkeit

Zustände: **offen** (grau) · **spricht dafür** (+, Pfeil nach oben) · **spricht dagegen** (−, Pfeil nach unten) ·
**unwahrscheinlich** (durchgestrichen, Grund bleibt lesbar) · **nicht bewiesen, nicht ausgeschlossen** (Bernstein,
nur am Ende für Herzrhythmus). Ein Eintrag kann mehrere Gründe sammeln; die Liste zeigt die letzten zwei.

Anzeige: Knopf „Verdacht" im HUD neben der Mappe (Zahl = Einträge, die sich zuletzt geändert haben); beim
Wechsel eines Eintrags eine stille Meldung unten links („Krampfanfall: unwahrscheinlich. Kein Zucken, sofort
klar."), keine Animation, die blinkt (ART_BIBLE §2). Zu Beginn sind alle acht offen; der Bogen des Nachtdienstes
setzt „Reflex: spricht dafür (Notiz Nachtdienst: V. a. vasovagal)". Das ist der Anker, und er steht sichtbar da.

### 4.2 Welcher Befund was bewirkt

| Befund (woher) | Eintrag | neuer Zustand | Grund (so steht er in der Liste) | Beleg |
|---|---|---|---|---|
| Bogen gelesen (Notiz Nachtdienst) | Reflex | spricht dafür | Notiz 06:25: V. a. vasovagal | Anker, keine fachliche Aussage |
| Bogen: Stehversuch 142/84 → 134/80, kein Schwindel | Kreislauf im Stehen | spricht dagegen | kein Abfall nach drei Minuten Stehen | ESC-Synkope-2018 §4.2.2.1 (Kriterium ≥ 20/10 mmHg oder < 90 systolisch), Schlüsselbotschaft 3 |
| Bogen: Zucker 104 | Unterzucker | spricht dagegen | 104, kein Diabetes | ESC-Synkope-2018 Tab. 4; ESC-Practical Web Table 5.6 |
| „Wie wenn einer das Licht ausdreht", am Boden, Erinnerungslücke, Tochter hat ihn angesprochen | Sturz ohne Bewusstlosigkeit | unwahrscheinlich | weg, umgesunken, keine Erinnerung | ESC-Synkope-2018 §4.1 (vier T-LOC-Merkmale), Tab. 4 |
| „Nix gespürt" (kein Prodrom) | Reflex | spricht dagegen | keine Vorwarnung | Tab. 5 (Prodrom als Reflex-Merkmal), Tab. 6 (Low-risk verlangt typisches Prodrom) |
| dito | Herzrhythmus | spricht dafür | ohne Vorwarnung | Tab. 6 (Minor: keine Vorwarnung / Prodrom < 10 s) |
| „Seit sechs auf, die Senta gefüttert, eine Minute beim Kocher" (Pflichtfrage „grad erst aufgestanden?") | Kreislauf im Stehen | spricht dagegen | nicht beim Aufstehen, kurz gestanden | Tab. 5 (OH: beim/nach dem Aufstehen), Tab. 6 Low-risk Nr. 7 (geprüft) |
| „Halbe Minute, gleich wieder klar" | Krampfanfall | spricht dagegen | sofort klar, keine Verwirrtheit | §8.1.2, Tab. 10 |
| dito | Psychogen (kein eigener Eintrag; Rückmeldung) | — | Dauer unter einer Minute | Tab. 4 |
| Schürfung, blauer Fleck, „ich war ja nicht dabei" | (kein Eintrag; Karte Anamnese: Verletzung) | — | Verletzung durch die Synkope | Tab. 7 |
| „Herz nie gespürt, kein Druck, täglich mit dem Hund, nicht bei Belastung" | Herz-Struktur | spricht dagegen | nicht unter Belastung, keine Beschwerden | Tab. 5, Tab. 6 (Major: unter Belastung, im Liegen, Herzrasen davor) |
| „Hab gesehen, gehört, der Sabine gesagt, sie soll den Kocher ausmachen" | Schlaganfall / TIA | spricht dagegen | reden, sehen, bewegen sofort wie immer | Tab. 4, §8.1.3 |
| Medikationsplan: Bisoprolol, Ramipril, ASS, seit Jahren | Kreislauf im Stehen | spricht dagegen | keine neue oder geänderte Tablette | Tab. 5 (zeitlicher Zusammenhang mit Beginn/Änderung), ESC-Practical Web Table 5.6 |
| dito | Herzrhythmus | (Hinweis auf der Karte) | Betablocker bremst Sinus- und AV-Knoten; erklärt langsame Zahlen, keine Ohnmacht | Pharmakologie (QUELLEN §3); ESC-Pacing-2021 §3.3/Tab. 6 |
| „Zucker nein", Stix | Unterzucker | unwahrscheinlich | kein Diabetes, Stix 104, Verlauf zu kurz | Tab. 4; Web Table 5.6 |
| „Ein Bier am Sonntag, schlafen ohne alles" | (Intoxikation, kein Eintrag; Rückmeldung) | — | | Tab. 4 |
| **Gestern an der Haltestelle, auch ohne Vorwarnung** | Herzrhythmus | spricht dafür | zweimal in zwei Tagen, beide Male ohne Vorwarnung, das erste Mal mit 68 | Tab. 5 (Reflex: lange Vorgeschichte, v. a. vor 40), Tab. 6 (Low-risk: lange Vorgeschichte gleichartiger Episoden) |
| dito: „eine Viertelstunde gestanden" | Reflex | (bleibt „spricht dagegen", Grund ergänzt: „langes Stehen spräche dafür, die fehlende Vorwarnung dagegen") | | Tab. 6 (Low-risk: nach langem Stehen) |
| Familie: Vater 80 Schlaganfall, Mutter 91 | Herzrhythmus | (kein Zustandswechsel; Grund: „niemand jung und plötzlich") | | Tab. 6 (Minor: plötzlicher Herztod jung in der Familie) |
| Untersuchung: Herztöne regelmäßig, kein Geräusch | Herz-Struktur | spricht dagegen (nicht gestrichen) | kein Geräusch, keine Beschwerden; Auskultation und eine Ableitung schließen bei 68 mit Bluthochdruck nichts aus, das Echo macht die Station | Tab. 6 (Major: unklares Systolikum); FACHREGELN (Grenzen einer Ableitung); ESC §4.2.3 (zu prüfen, §12) |
| Untersuchung: Neurologie unauffällig | Schlaganfall / TIA | unwahrscheinlich | Bewusstsein weg, Ausfälle keine | Tab. 4, §8.1.3; Web Table 5.4 |
| Tochter: kein Zucken, Augen offen, dagelegen | Krampfanfall | unwahrscheinlich | keine Zuckungen, sofort klar, keine Zunge | §8.1.2, Tab. 10; Web Table 5.3–5.5 |
| Tochter: Augen offen | (Psychogen, Rückmeldung) | — | | §7.1.2 |
| EKG: Sinus, {hf}/min | Herzrhythmus | (Grund: „{hf} unter Betablocker: erwartbar, nicht verdächtig") | | Lektion 8; Tab. 5 („ohne negativ chronotrope Medikation") |
| EKG: PQ {pq} | Herzrhythmus | **spricht dafür**, Grund „EKG nicht normal: AV-Block I°, PQ {pq}; kein Beweis" | | Lektion 3, 10; Tab. 6 (Low-risk verlangt normales EKG, Nr. 11, geprüft) |
| EKG: QRS 86 | Herzrhythmus | (Grund: „schmal: die Bremse sitzt oben") | | Lektion 4, 10 |
| Falks Entscheidung | Herzrhythmus | **nicht bewiesen, nicht ausgeschlossen** | Beweis wäre: Pause > 3 s im Wachen, Mobitz II, III°, Sinus < 40. Dafür der Monitor | §4.1.1, §4.2.4.1 |
| Falks Entscheidung | Reflex | unwahrscheinlich | keine Vorwarnung, erstes Mal mit 68, EKG nicht normal: nicht niedrig | Tab. 6 |

### 4.3 Endzustand (so sieht die Liste um 07:30 aus)

- ~~Reflex~~ unwahrscheinlich: keine Vorwarnung, erstes Mal mit 68, EKG nicht normal
- ~~Kreislauf im Stehen~~ unwahrscheinlich: Stehversuch ohne Abfall, nicht beim Aufstehen, keine neue Tablette
- **Herzrhythmus: nicht bewiesen, nicht ausgeschlossen.** Ohne Vorwarnung, zweimal, EKG nicht normal (PQ {pq}): nicht niedrig. Beweis bräuchte eine Pause > 3 s im Wachen, Mobitz II, III° oder Sinus < 40. Dafür der Monitor.
- Herz-Struktur: spricht dagegen (nicht unter Belastung, kein Geräusch); das Echo macht die Station morgen
- ~~Krampfanfall~~ unwahrscheinlich: kein Zucken, sofort klar
- ~~Schlaganfall / TIA~~ unwahrscheinlich: Bewusstsein weg, Ausfälle keine
- ~~Unterzucker~~ unwahrscheinlich: kein Diabetes, Stix 104
- ~~Sturz ohne Bewusstlosigkeit~~ unwahrscheinlich: weg, umgesunken, keine Erinnerung

Die Liste ist zugleich die Karte „Verdacht" in der Mappe (ein Eintrag je Zustandswechsel, mit Uhrzeit). Im
Epilog bekommt „Herzrhythmus" den letzten Eintrag: „Dienst 3: Pause über drei Sekunden im Wachen, ohne
Betablocker. Bewiesen."

### 4.4 Kern und Rest: warum keine Pflichtfragen-Mahnung mehr nötig ist

Jede Runde hat einen **Kern**, der die Runde schließt, und einen Rest, den die Spielerin fragen oder auslassen darf:

| Runde | Kern (Engpass) | Rest (auslassbar, mit Folge bei Falk) |
|---|---|---|
| 1 Ereignis | Erzählen; Vorwarnung; „grad erst aufgestanden?" | Dauer/Erholung, Schramme, Zucken (die Tochter deckt Dauer und Zucken am Telefon) |
| 2 Person, Tabletten | Tabletten (mit „heute genommen?") | Zucker/Krankheiten, Herz/Brust, Neuro, Alkohol |
| 3 Vorgeschichte | „Schon einmal passiert?" | Familie |

Sobald der Kern einer Runde steht, erscheint „Das reicht mir fürs Erste"; Herr Baum schließt die Runde mit einem
Satz. Was ausgelassen wurde, fragt Falk in der Übergabe („Verletzt hat er sich? Zucker? Familie?") und schickt
zum Patienten, drei Meter, die Uhr läuft weiter (§6.2). So ist die Wahl echt (Skill `handlung` §3: Folge
sichtbar, korrigierbar), und das EKG wartet nicht auf drei Runden: Nach dem Kern der Runde 1 ist der Wagen frei.
Die Liste zeigt pro Runde höchstens sechs Zeilen, keine Hubs, kein Zurück. Optionale menschliche Fragen (Senta,
Foto) stehen dazwischen und zählen nicht.

---

## 5. Die Dialoge

Konventionen: Repliken höchstens zwei Sätze und 220 Zeichen, kein Gedankenstrich; längere Gedanken in zwei
Klicks (zwei Repliken nacheinander); Spieleroptionen eine Zeile (≤ 64 Zeichen). Rückmeldungen (`warum`) erscheinen
nach einer Wahl als Streifen unter dem Dialog, nie im Figurenmund; der Beleg steht in Klammern nur hier, nie im
Spiel. **Messwerte stehen nur als Platzhalter** ({hf}, {pq}, {qrs}; {mess_pq} = Median aus der Annotation), weil die
Spielerin um ± 20 ms anders messen darf; feste Fallwerte (Puls 52, Blutdruck, Zucker) laufen wie bisher über
`werte`. Austriazismen bei Marlene und Herrn Baum sparsam: *Sackerl, Zuckerl, halt, eh, Sessel, dreiviertel acht,
Entschuldigen S'*, ein einziges „gell". Herr Baum sagt „Frau Doktor", obwohl er weiß, dass sie es nicht ist;
Marlene duzt; Falk siezt und nennt niemanden beim Vornamen. Die Spielfigur ist KPJ-Studentin (§13).

Stimmprofile (Skill `dialoge` §4), ergänzt um die Tochter (neu, in den Skill zu übernehmen):

| Figur | Satzbau | Wörter | Nie | Tic |
|---|---|---|---|---|
| **Sabine Baum, 44** (Tochter, Kindergartenpädagogin, am Telefon) | schnell, halbe Sätze, organisiert beim Reden („Ich kann erst um zwölf") | „Papa", Uhrzeiten, Namen von Nachbarn | Fachwörter, Vorwürfe an den Vater vor Fremden | hört nebenbei ihre Gruppe kommen; fragt zweimal, ob er bleibt |

### 5.1 Auftakt (06:40, Erzähler, Raum sichtbar, keine Figur spricht)

> **Erzähler:** 06:40. Dein erster Tag der Rotation auf der Notaufnahme, zwanzig Minuten zu früh, weil du den Weg nicht kanntest.
>
> **Erzähler:** Die Nachtschicht räumt auf, Marlene telefoniert hinter dem Tresen. In der Koje rechts ein Mann mit Schiebermütze, der die Jacke schon anhat und ein Sackerl in der Hand hält.
>
> *Knopf:* Zum Tresen.

Bewegung dazu (§10): Marlene legt auf, als die Spielerin den Tresen anklickt; Herr Baum schaut zur Uhr.

### 5.2 Marlene am Tresen (06:42, Szenenbild; sie reicht den Bogen)

Ziel: Die Spielerin weiß, wer, was, bis wann, und hat den Anker in der Hand. Marlene will übergeben und heim; sie
gibt den Patienten ab, ohne ihn fallen zu lassen.

> **Marlene:** Du bist die KPJ-lerin? Marlene, seit gestern sieben Uhr da, also red langsam mit mir.
>
> *Spielerin:* 1 Was ist mit dem Herrn in der Koje? · 2 Wo ist der Arzt? · 3 Was soll ich machen?
>
> **Marlene** (1): Herr Baum, achtundsechzig, heut in der Früh in der Küche umgefallen, die Tochter hat ihn gebracht. Ihm fehlt nix, sagt er, und der Hund muss raus.
>
> **Marlene:** Die Monitorkojen sind voll, drum ist er in der Drei.
>
> **Marlene** (2): Die Steiner hat Journal, die ist seit halb sieben im Schockraum, die Rettung hat eine Reanimation gebracht. Vorher hat sie ihn kurz gesehen und das da hingeschrieben. *(reicht den Bogen; Karte „Aufnahmebogen")*
>
> **Marlene** (3): Red mit ihm und schau ihn an. Das EKG schreibst du, ich komm nicht dazu, um sieben geb ich der Andrea acht Leute über.
>
> *(nach allen dreien, oder wenn die Spielerin „Ich geh zu ihm" wählt)*
>
> **Marlene:** Und der Falk kommt um viertel nach sieben runter und fragt dich, ob der Mann heimdarf. Nicht mich.
>
> **Marlene:** Stehversuch und Zucker hab ich gemacht, Blut ist weg, Labor kommt um acht. So.
>
> *Spielerin:* Danke. Ich geh zu ihm.

*Karte „Aufnahmebogen":* Triage 06:20. Puls {puls}/min, regelmäßig. Blutdruck liegend {rr_l_sys}/{rr_l_dia}, nach
1 min Stehen {rr_s1_sys}/{rr_s1_dia}, nach 3 min {rr_s3_sys}/{rr_s3_dia}, ohne Schwindel. SpO₂ {spo2} %, {temp} °C,
Blutzucker {zucker} mg/dl. Schürfung linker Ellbogen, blauer Fleck linke Hüfte. Labor abgenommen 06:30. **Notiz
Dr. Steiner 06:25: V. a. vasovagale Synkope, Schellong unauffällig, EKG ausständig.** → Verdachtsliste: Reflex
„spricht dafür (Notiz)", Kreislauf im Stehen „spricht dagegen (Stehversuch)", Unterzucker „spricht dagegen (104)".

*Prüfung:* D1: Marlene hat Hauptsätze, Imperative, „So.", Zahlen in Stationsdeutsch; ohne Namen erkennbar. D2: laut
lesbar, Abbrüche („Ihm fehlt nix, sagt er."). D3: kein Erklärdump; die Notiz ist ein Zettel, keine Lehre. D4: Müdigkeit
im „red langsam mit mir" und „acht Leute über", nicht benannt. D5: jeder Wechsel bringt dem Fall etwas (Patient, Notiz,
Koje ohne Monitor, Auftrag), zeigt die Figur (delegiert, prüft), hat Subtext („Ich geb dir den Mann, nicht die Antwort")
und verschiebt die Beziehung (sie traut es ihr zu). D6: ruhig, aber knapp, weil müde. Humanizer: kein Gedankenstrich,
keine Dreierreihe, kein Aphorismus am Schluss; jede Replik höchstens zwei Sätze.

### 5.3 Herr Baum, Runde 1: das Ereignis (06:45, in der Koje; er steht)

Ziel: Die vier T-LOC-Merkmale und die Umstände, ohne dass es ein Verhör ist. Kern der Runde: Erzählen, Vorwarnung,
„grad erst aufgestanden?" (Orthostase braucht eine Quelle im Gespielten). Herr Baum will heim und sagt es durch die
Jacke; er spielt herunter und entschuldigt sich.

> **Herr Baum:** Ah, Frau Doktor. Entschuldigen S', die Schwester hat gesagt, ich soll warten, aber die Senta muss um acht raus, und mir fehlt nix.
>
> *Spielerin:* 1 KPJ-Studentin, keine Ärztin. Setzen Sie sich, erzählen Sie. · 2 Wer ist die Senta? · 3 Ich schau zuerst auf den Bogen.
>
> **Herr Baum** (2): Die Senta, unser Hund, also der von der Sabine, aber ausführen tu ich. Neun Jahre, Dackel mit was drin, die wartet jetzt an der Tür.
>
> **Herr Baum** (3): Bitte, bitte, ich hab Zeit. Also keine, aber bitte. *(Karte „Aufnahmebogen", falls noch nicht)*
>
> **Herr Baum** (1, setzt sich auf die Liegenkante, Jacke bleibt an): In der Küche, ich hab den Wasserkocher angestellt wie immer. Und dann lieg ich am Boden, und die Sabine schreit, dazwischen nix, wie wenn einer das Licht ausdreht.
>
> *Spielerin (Runde 1, Reihenfolge frei):* 1 Haben Sie vorher etwas gespürt? Übel, heiß, Schwitzen? · 2 Waren Sie grad erst aufgestanden? · 3 Wie lange weg, und danach gleich klar? · 4 Woher ist die Schramme? · 5 Hat Ihre Tochter gesehen, ob Sie gezuckt haben? · 6 Das reicht mir fürs Erste. *(erscheint, sobald 1 und 2 gefragt sind)*
>
> **Herr Baum** (1): Nix, gar nix. Ich hab grad an die Senta gedacht, und dann war der Boden da.
>
> **Herr Baum** (2): Nein, seit sechs auf, die Senta gefüttert, dann der Kocher. Eine Minute hab ich dort gestanden, höchstens.
>
> **Herr Baum** (3): Eine halbe Minute, sagt die Sabine, sie hat den Krach gehört und ist gleich gekommen. Dann hab ich gesagt, Sabine, mach keinen Zirkus, und sie hat trotzdem einen gemacht.
>
> **Herr Baum** (4): Vom Tisch, glaub ich, oder vom Sessel. Die Sabine weiß es, ich nicht.
>
> **Herr Baum** (5): Das fragen S' sie selber, sie ruft eh an. Gezuckt hab ich im Leben noch nie.
>
> *(nach 6, oder wenn alles gefragt ist)*
>
> **Herr Baum:** Mehr weiß ich nicht, ich war halt weg. Fragen S' die Sabine, die hat alles gesehen.

*Verdachtsliste nach Runde 1:* Sturz ohne Bewusstlosigkeit → unwahrscheinlich (weg, umgesunken, keine
Erinnerung; §4.1 der Leitlinie). Reflex → spricht dagegen (keine Vorwarnung; Tab. 5/6). Herzrhythmus → spricht
dafür (ohne Vorwarnung; Tab. 6 Minor). Kreislauf im Stehen → spricht dagegen (seit sechs auf, nicht beim Aufstehen,
eine Minute gestanden; Tab. 5, Tab. 6 Nr. 7). Mit (3): Krampfanfall → spricht dagegen (sofort klar; Tab. 10). Mit (4):
Verletzung auf die Karte „Anamnese" (Tab. 7, nur Stütze).

*Rückmeldung zu (6), wenn etwas offen blieb (still):* Was du nicht gefragt hast, fragt Falk. Oder die Tochter sagt
es dir. *(keine fachliche Aussage)* Zu (3) „Ich schau zuerst auf den Bogen": Lesen ist richtig; der Bogen hat
schon eine Antwort drauf, lies sie als Frage, nicht als Befund.

*Prüfung:* D1: Laiensprache, Abschweifen (Senta, Sabine), Entschuldigung; kein Fachwort. D2: Abbrüche, Rhythmus
wechselt; keine Replik über zwei Sätze. D3: Wissen kommt aus seinen Antworten. D4: Scham und Ungeduld in der Jacke,
im „mir fehlt nix", im Hund; nie benannt. D5: jede Antwort bewegt einen Eintrag der Liste und zeigt den Mann. D6:
ruhig, kurze Sätze, weil er weg will. Humanizer: keine Gedankenstriche, keine Schlusspointe; „Die Sabine weiß es,
ich nicht" ist Auskunft, kein Witz.

### 5.4 Runde 2: die Person und die Tabletten (06:52)

Kern: die Tabletten (mit „heute genommen?"). Rest auslassbar.

> **Herr Baum:** Fragen S' nur. Die Sabine hat auch schon alles gefragt.
>
> *Spielerin (Runde 2, Reihenfolge frei):* 1 Welche Tabletten nehmen Sie? · 2 Haben Sie Zucker? Andere Krankheiten? · 3 Herzrasen, Stolpern, Druck in der Brust, Luftnot? · 4 Konnten Sie danach reden, sehen, die Arme heben? · 5 Alkohol? Schlaftabletten? · 6 Das reicht mir. *(erscheint nach 1)*
>
> **Herr Baum** (1): Drei in der Früh, die Sabine hat den Zettel vom Hausarzt eingepackt, da im Sackerl. Die Farben kenn ich, die Namen nicht. *(reicht den Plan; Karte „Medikamente")*
>
> *Spielerin (statt 1 erscheinen):* 1a Haben Sie die heute schon genommen? · 1b Ist in letzter Zeit etwas geändert worden?
>
> **Herr Baum** (1a): Heut nein, heut war ja die Küche zuerst. Die liegen noch am Tisch, neben dem Kaffee.
>
> **Herr Baum** (1b): Nein, seit Jahren das Gleiche. Der Doktor Reiter sagt, so lang's passt, bleibt's.
>
> **Herr Baum** (2): Zucker nein. Den Blutdruck, seit zehn Jahren, das Knie, und das Hörgerät.
>
> **Herr Baum** (3): Nie, mein Herz hab ich noch nie gespürt. Bergauf mit der Senta werd ich langsamer, aber ich komm rauf.
>
> **Herr Baum** (4): Alles. Ich hab der Sabine gesagt, sie soll den Wasserkocher abdrehen, der pfeift, also gehört und gesehen hab ich.
>
> **Herr Baum** (5): Ein Bier am Sonntag, nach dem Friedhof. Schlafen tu ich wie ein Stein, ohne was.
>
> *(nach 6, oder wenn alles gefragt ist)*
>
> **Herr Baum:** Sonst bin ich gesund. Sagt der Reiter.

*Karte „Medikamente (Medikationsplan)":* {medi1}, {medi2}, {medi3}, 1-0-0, seit Jahren unverändert; **heute
noch nicht genommen** (zuletzt gestern früh). Der Betablocker bremst Sinusknoten und AV-Knoten: Er erklärt eine
langsame Frequenz und eine zähe Überleitung, aber keine Bewusstlosigkeit ohne Vorwarnung. *(Pharmakologie, QUELLEN
§3; ESC-Pacing-2021 §3.3/Tab. 6)*

*Verdachtsliste:* Kreislauf im Stehen → spricht dagegen (keine neue Tablette; Tab. 5). Unterzucker →
unwahrscheinlich (kein Diabetes, Stix 104; Tab. 4). Herz-Struktur → spricht dagegen (nicht unter Belastung, keine
Beschwerden; Tab. 5/6). Schlaganfall/TIA → spricht dagegen (reden, sehen, bewegen sofort; Tab. 4). Rückmeldung zu
(5), still: Alkohol und Schlafmittel gehören zu den Nicht-Synkopen, die man abfragt; hier beides nein (Tab. 4).

*Prüfung:* D1: derselbe Mann (Sackerl, Reiter, Senta). D3: der Medikationsplan ist Alltag, kein Fund (KONZEPT §1.3).
D5: „Heut nein" bringt dem Fall die Tabletten-Frage von Takt 6 und zeigt, wie der Morgen war. Humanizer: die
Schlusspointen („das ist das Alter", „aber die auch", „auch nicht jünger") sind weg.

### 5.5 Runde 3: die Vorgeschichte, die Wendung (06:57)

Kern: „Ist das schon einmal passiert?" Rest: Familie. Ziel: Das zweite Ereignis kommt heraus; Herr Baum will,
dass es nicht „was" wird; die Spielerin muss entscheiden, was sie verspricht.

> *Spielerin (Runde 3):* 1 Ist in Ihrer Familie jemand jung und plötzlich gestorben? · 2 Ist das schon einmal passiert?
>
> **Herr Baum** (1): Der Vater mit achtzig, Schlaganfall, die Mutter einundneunzig. Jung ist bei uns keiner gestorben.
>
> **Herr Baum** (2, schaut auf das Sackerl): Frau Doktor. Sagen S' es der Sabine nicht.
>
> *Spielerin:* 1 Was soll ich ihr nicht sagen? · 2 Das bleibt unter uns. · 3 Dem Arzt sag ich alles. Der Tochter nur, wenn Sie wollen.
>
> **Herr Baum** (nach 1, 2 oder 3): Gestern, an der Haltestelle beim Friedhof. Der Bus ist nicht gekommen, und auf einmal lieg ich am Boden, und eine Frau redet auf mich ein.
>
> **Herr Baum:** Ich hab gesagt, der Kreislauf, und bin heimgefahren wie nix. Die Sabine hat genug mit der Lena und dem Kindergarten, bitte.
>
> *(nach 1 erscheinen 2 und 3 noch einmal)*
>
> **Herr Baum** (nach 2, Flag `versprochen`): Danke. Sie sind eine Gute.
>
> **Herr Baum** (nach 3): Der Arzt ist der Arzt. Aber die Sabine macht sonst noch mehr Zirkus, und die Lena kriegt's mit.
>
> *Spielerin (Nachfragen):* 1 Gestern vorher etwas gespürt? · 2 Wie lange sind Sie dort gestanden? · 3 Haben Sie sich gestern verletzt?
>
> **Herr Baum** (1): Auch nix, gestanden und auf den Bus geschaut. Und dann die Frau mit dem Zuckerl, vor der Kirche, alle haben geschaut.
>
> **Herr Baum** (2): Eine Viertelstunde sicher. Sonntag fährt er nur alle halbe Stunde, und ich war zu früh, wie immer.
>
> **Herr Baum** (3): Nein, die Frau hat gesagt, ich bin umgesunken wie ein nasser Sack, langsam. Der Ellbogen, das ist von heut.
>
> *(wenn die Nachfragen durch sind oder die Spielerin weitergeht)*
>
> **Herr Baum:** So, jetzt wissen Sie's. Und ich darf trotzdem heim, gell?
>
> *Spielerin:* Das entscheidet der Oberarzt. Vorher schau ich Sie an.

*Rückmeldung zu „Das bleibt unter uns" (`warum`):* Versprich nur, was du halten kannst. Was er dir sagt, gehört in
die Akte und zum Oberarzt, sonst entscheidet der mit der halben Geschichte; die Tochter erfährt es nur von ihm oder
mit seinem Einverständnis. *(keine fachliche Aussage; Verschwiegenheit: KAKuG §9 für in Krankenanstalten
beschäftigte Personen, dazu die Verschwiegenheitserklärung der Famulatur/des KPJ; Reichweite für Studierende §12)*

*Rückmeldung zu „Dem Arzt sag ich alles. Der Tochter nur, wenn Sie wollen":* Richtig: Die Akte ist nicht die
Familie. Er entscheidet, was die Tochter erfährt; du entscheidest nicht, was der Oberarzt erfährt. *(wie oben)*

*Verdachtsliste:* Herzrhythmus → spricht dafür, Grund „zweimal in zwei Tagen, beide ohne Vorwarnung, das erste Mal
mit 68" (Tab. 5: lange Vorgeschichte vor 40 als Reflex-Merkmal; Tab. 6 Low-risk Nr. 8). Reflex → Grund ergänzt:
„eine Viertelstunde Stehen spräche dafür, die fehlende Vorwarnung dagegen" (Tab. 6 Low-risk: nach langem Stehen).
Familie: kein Zustandswechsel, Grund „niemand jung und plötzlich" (Tab. 6 Minor). Die Wendung erhöht den Einsatz;
der Kipppunkt bleibt die PQ-Zeit (§2.2).

*Prüfung:* D1: die Pause vor „Frau Doktor" ist Handlung (Blick auf das Sackerl). D4: Scham in „vor der Kirche, alle
haben geschaut" und im „bitte", nicht benannt. D5: der Wechsel bringt dem Fall das zweite Ereignis, zeigt den Mann
(er schützt die Tochter, nicht sich), hat Subtext („wenn man's sagt, ist es was") und stellt die Beziehung auf die
Probe. Entscheidungstest (Skill `handlung` §3): unterscheidbar, Folge sichtbar (Falk, Schluss), korrigierbar,
ärztlich (Vertraulichkeit gegen Dokumentationspflicht). Humanizer: „wie ein nasser Sack" ist seine Zeugin, nicht die
Autorin; „ich auf einmal auch nicht mehr" ist weg.

### 5.6 Untersuchung (freiwillig, ab Runde 1) und Marlene mit dem Wagen (fester Engpass)

> *Spielerin:* Darf ich Sie kurz anschauen? Herz, Lunge, Nerven.
>
> **Herr Baum:** Bitte, die Jacke lass ich an, oder? Es zieht da herinnen.

*Befundzeilen (bestehende Mechanik, Karte „Untersuchung"):* Puls am Handgelenk langsam, regelmäßig. Herztöne
regelmäßig, langsam, kein Geräusch. Lunge frei, keine Beinödeme. Schürfung linker Ellbogen, blauer Fleck linke Hüfte.
Sprache klar, Gesicht symmetrisch, Arme und Beine seitengleich kräftig, kein Doppeltsehen, Finger-Nase sicher.
→ Herz-Struktur **spricht dagegen** (kein Geräusch, nicht unter Belastung; eine Auskultation und eine Ableitung
schließen bei 68 mit Bluthochdruck nichts aus: das Echo macht die Station, §6.5), Schlaganfall/TIA unwahrscheinlich
(Bewusstsein weg, Ausfälle keine; Tab. 4, §8.1.3). Wer nicht untersucht, hört es von Falk am Bett (§6.5).

**Marlene mit dem Wagen** (Takt 3, Sequel; ausgelöst, sobald die Spielerin nach dem Kern der Runde 1 den Wagen
anklickt): Marlene schiebt ihn selbst an die Koje (Bewegung §10), den Kuli hinterm Ohr, Andrea wartet am Tresen.

> **Marlene:** Da, ich übergeb.
>
> **Marlene:** Und? Darf er?
>
> *Spielerin:* 1 Es war gestern schon einmal. Er hat's niemandem gesagt. *(nur mit `hat:zweites_ereignis`)* · 2 Noch nicht. Erst das EKG.
>
> **Marlene** (1): Was, dem hab ich den ganzen Morgen Zuckerl angeboten, und er sagt mir nix? Schreib's auf den Bogen, mit Uhrzeit, und sag's dem Falk als Erstes.
>
> **Marlene** (2): Dann mach. Papier ist drin.

Kommt das zweite Ereignis erst nach dem EKG heraus, meldet sich Marlene vom Tresen (Meldung in ihrer Stimme):
*„Das hat er mir nicht gesagt. Schreib's auf den Bogen, mit Uhrzeit."* Klickt die Spielerin den Wagen vor dem Kern
der Runde 1, ruft Marlene herüber: *„Lass den Wagen noch. Du weißt ja nicht einmal, was passiert ist."*

*Prüfung:* D5: (1) bringt dem Fall die Dokumentation und Falks Reihenfolge, zeigt Marlene (gekränkt, dass er ihr
nichts gesagt hat; stolz auf die Neue, ohne es zu sagen), Subtext „du hast gefunden, was ich nicht gefunden hab".
Der Sequel ist jetzt ein Engpass, kein Zufall (Skill `handlung` H7). Humanizer: kein Lehrsatz mehr („Erst reden,
dann kleben" ist weg).

### 5.7 Das EKG (07:02): Kleben, Handy

Der Wagen steht an der Koje. Herr Baum legt sich hin, die Mütze bleibt auf.

> **Herr Baum:** Muss ich das Hemd aufmachen? Kalt ist das Zeug.
>
> *Spielerin:* 1 Zehn Sekunden ganz ruhig liegen. Nicht reden. · 2 Haben Sie schon einmal ein EKG gehabt?
>
> **Herr Baum** (2): Beim Reiter, vor Jahren, da war's in Ordnung. Damals hab ich auch noch die Elfriede gehabt.
>
> **Herr Baum** (1): Nicht reden kann ich nicht, fragen S' die Sabine.
>
> *(Das Handy im Sackerl leuchtet und vibriert; Bewegung §10. Herr Baum hebt den Kopf, legt ihn wieder hin.)*
>
> **Herr Baum:** Das ist die Sabine. Gehen S' ran, bitte, ich darf mich ja nicht rühren, und ich hör eh nix mit dem Ding, wenn ich lieg.
>
> *Spielerin:* 1 Ich geh ran. · 2 Das kann warten, erst das EKG.
>
> **Herr Baum** (2, Flag `anruf_spaeter`): Dann ruft sie dreimal. Sie kennen sie nicht.

Wählt die Spielerin (2), kommt der Anruf nach dem Streifen noch einmal; nichts geht verloren, die Reihenfolge ist
ihre. Rückmeldung zu (2), still: Ein Angehöriger, der dabei war, ist die beste Zeugin, die du kriegst; am Telefon
ist sie jetzt. Beides ist vertretbar. *(ESC-Practical-2018 Web Table 5.3: Zeugenbericht)*

*Prüfung:* D4: die Elfriede (verstorbene Frau) kommt genau einmal vor, als Nebensatz. D6: kurze Wechsel, weil er
liegt und die Uhr läuft. Humanizer: ok.

### 5.8 Das Telefon (07:04, Sabine Baum; Dialog mit Hörer-Symbol statt Porträt)

Ziel: Fremdanamnese der Zeugin (Krampf aus, Pseudosynkope aus), die Tabletten, der Schlüssel für die Senta. Die
Tochter will wissen, ob er heimdarf, und hat fünf Minuten.

> **Sabine Baum:** Papa, wer ist da? Ah, Entschuldigung, ich hab nur fünf Minuten, bevor meine Gruppe kommt.
>
> **Sabine Baum:** Wie geht's ihm?
>
> **Sabine Baum** (bei `anruf_spaeter` stattdessen): Ich hab dreimal angerufen. Wie geht's ihm?
>
> *Spielerin:* 1 Er liegt gerade am EKG. Was haben Sie heute früh gesehen? · 2 Hat er gezuckt? Waren die Augen offen? · 3 Hat er seine Tabletten heute genommen?
>
> **Sabine Baum** (1): Einen Krach, wie wenn der Tisch umfällt, und dann ist er am Boden gelegen, grau im Gesicht, die Augen offen. Ich hab Papa gesagt, und er hat gleich geschaut.
>
> **Sabine Baum:** Zwanzig Sekunden vielleicht, dreißig. Mir ist es wie eine Stunde vorgekommen.
>
> **Sabine Baum** (2): Gezuckt hat er nicht, er ist dagelegen wie ein Sack, das war das Schlimme. Gebissen hat er sich auch nicht, ich hab geschaut.
>
> **Sabine Baum** (3): Nein, die liegen noch am Tisch, ich hab's gesehen, wie wir gegangen sind. Sonst nimmt er die um sieben mit dem Kaffee, soll ich sie bringen, ich kann erst um zwölf?
>
> *(nach allen dreien)*
>
> **Sabine Baum:** Ist das was Schlimmes, darf er heim? Ich kann ihn erst um halb eins holen.
>
> **Sabine Baum:** Und wegen dem Hund: Die Frau Kainz nebenan hat einen Schlüssel, ich ruf sie an, wenn er bleibt. Sagen S' ihm das, von mir glaubt er's nicht.
>
> *Spielerin:* 1 Das entscheidet der Oberarzt gleich. Ich ruf Sie an. · 2 Wahrscheinlich nur der Kreislauf. Keine Sorge. · 3 Er hat uns gesagt, dass es gestern schon einmal war.
>
> **Sabine Baum** (1): Gut, bitte. Die Lena fragt schon.
>
> **Sabine Baum** (2, Flag `tochter_beruhigt`): Gott sei Dank, das hab ich mir gedacht, der Kreislauf halt. Dann bis zwölf.
>
> **Sabine Baum** (3, Flag `tochter_verraten`): Gestern, was gestern? Der sagt mir nichts, nie, und zum Friedhof will er allein, mit dem Bus, damit ich meine Ruhe hab.
>
> **Sabine Baum:** Ich muss, die Gruppe kommt. Danke, Frau, ich weiß gar nicht, wie Sie heißen.

*Rückmeldung zu (2):* Zu früh. Du weißt es noch nicht, und die Tochter wird jedem erzählen, was du gesagt hast;
„der Oberarzt entscheidet gleich" ist keine Ausrede, es ist der Stand. *(keine fachliche Aussage)*

*Rückmeldung zu (3):* Er hat dich gebeten, es ihr nicht zu sagen, und er ist bei klarem Verstand. Was die Tochter
erfährt, entscheidet er. *(KAKuG §9, Verschwiegenheitserklärung; §12)*

*Karte „Fremdanamnese (Tochter, 07:04)":* Krach gehört, am Boden gefunden, grau, Augen offen, kein Zucken, kein
Zungenbiss, nach 20–30 s angesprochen und sofort klar. Tabletten heute nicht genommen. → Krampfanfall
unwahrscheinlich (keine Myoklonien, sofort klar, keine Zunge; §8.1.2, Tab. 10); Pseudosynkope (Rückmeldung): Augen
offen, unter einer Minute (§7.1.2, Tab. 4).

*Prüfung:* D1: Sabine spricht schnell, in halben Sätzen, mit Uhrzeiten („um zwölf", „halb eins"), organisiert („Ich ruf
sie an"); ohne Namen von Marlene und Herrn Baum unterscheidbar. D3: die Fremdanamnese kommt im Moment, in dem sie
zählt (er liegt am EKG). D4: Angst in „wie eine Stunde", nicht benannt. D5: der Anruf löst drei Dinge des Falls
(Krampf, Tabletten, Senta) und stellt die Beziehung Spielerin↔Patient auf die Probe. Humanizer: keine Gedankenstriche,
jede Replik höchstens zwei Sätze.

### 5.9 Der Streifen (07:08): Rhythmusfrage und Zirkel

Meldung: „EKG geschrieben · 07:08". Streifen wie heute (LUDB 39, 25 mm/s für die Rhythmusfrage, 50 mm/s am Zirkel).
Der Schirm des Wagens zeigt die Kurve nur jetzt (§8.2).

**Rhythmusfrage** („Erst der Rhythmus. Was führt hier?"):

| Option | richtig? | Rückmeldung (`warum`) | Beleg |
|---|---|---|---|
| Sinusrhythmus | ja | Vor jedem QRS eine P-Welle, in II positiv, die Abstände gleich. Der Sinusknoten führt. Ob er langsam ist, sagt erst die Frequenz: der Zirkel. | Lektion 8 |
| Ersatzrhythmus aus dem AV-Knoten | nein | Dann fehlte die P vor dem QRS, oder sie wäre in II negativ, im oder hinter dem QRS. Hier steht vor jedem QRS eine positive P. Langsam heißt nicht Ersatz. | Lektion 11 |
| Sinusrhythmus mit ausgefallenen Schlägen (AV-Block II°) | nein | Dann gäbe es P-Wellen, auf die kein QRS folgt, eine Lücke. Hier folgt auf jede P ein QRS, und zwischen den Komplexen liegt keine zweite P. In zehn Sekunden fällt nichts aus. | Lektion 10; Annotation LUDB 39 (6 P / 7 QRS, erster Komplex am Rand) |
| Vorhofflimmern | nein | Kein P, flimmernde Grundlinie, Abstände springen. Hier: P vor jedem QRS, Abstände gleich. | Lektion 25 |

„Kammertachykardie" entfällt (bei 53/min keine ernsthafte Irrmöglichkeit).

**Zirkel** (Mechanik unverändert; Deutungstexte neu dort, wo sie die Fallfrage berühren):

- RR → Frequenz: *„60 000 : {ms} = {hf} pro Minute. Im Kurs heißt Sinusbradykardie unter 50 (so auch die
  Synkopen-Leitlinie); andere Quellen sagen 60, und der Datensatz nennt diese Kurve Sinusbradykardie. Wichtiger: unter
  Betablocker erwartbar, nicht verdächtig."* (Lektion 7, 8; Tab. 5 „ohne negativ chronotrope Medikation"; QUELLEN §3
  Quellenabhängigkeit). Karte „Frequenz".
- PQ: *„{ms} ms, über 200: AV-Block I°. Damit ist das EKG nicht normal. Mehr sagt es nicht: jeder Vorhofimpuls kommt
  an, keine Pause, kein ausgefallener Schlag in zehn Sekunden."* (Lektion 3, 10; §4.1.1). Karte „PQ-Zeit" mit dem
  Hinweis auf die Streuung des P-Beginns (wie heute). → Verdachtsliste: Herzrhythmus „EKG nicht normal: AV-Block
  I°, PQ {pq}; kein Beweis".
- QRS (optional): *„{ms} ms, schmal. Die Kammern laufen über das normale Leitungssystem; die Bremse sitzt oben, in
  der Überleitung."* (Lektion 4, 10). Karte „QRS".

**Vergleiche in der Mappe** (bestehende Mechanik): PQ ↔ Medikamente („Der Betablocker bremst beide Etagen: Taktgeber
und Überleitung. Die Ohnmacht erklärt er trotzdem nicht."); Rhythmus ↔ Anamnese („Zehn Sekunden Papier gegen zwei
Ohnmachten. Der Streifen war nicht dabei. Was er beweisen könnte, hat er nicht gezeigt: keine Pause, kein Block
mit ausgefallenen Schlägen."); Frequenz ↔ Aufnahmebogen (Puls {puls} getastet, {hf} gemessen: dieselbe Zahl; Lektion 7).

Danach sagt der Stand in einem Satz: *„Falk kommt um viertel nach sieben. Was sagst du ihm zuerst?"* und bietet den
Knopf **„Zum Tresen, Falk ist da"** (stellt die Uhr auf 07:15, falls sie früher steht). Das ist Takt 5 (Sequel):
Mappe und Verdachtsliste anschauen, dann hinübergehen. Steht die Uhr schon auf 07:15, ist Falk ohnehin da.

---

## 6. Die Übergabe (ISBAR) und Falks Gegenrede (07:15–07:28)

Ziel des Takts: Die Spielerin bringt ihre Befunde in eine Form, die ein Oberarzt mit zwölf Minuten annimmt, und
hält seiner fertigen Meinung stand. Falk will die Koje und hat die Notiz des Journaldienstes gelesen; er ist kein
Rätselonkel, er ist ein müder, präziser Mann, der die harmlose Erklärung bevorzugt, bis ihm jemand sagt, warum nicht.
Er fragt zurück, statt zu dozieren; Antithesen erlaubt er sich zwei (Übergabe, Schramme).

### 6.1 Ankunft (um 07:15 in jedem Fall)

> **Erzähler:** 07:15. Die Tür, Dr. Falk, Kaffee in der einen Hand, die Übergabeliste in der anderen; er liest, bevor er grüßt.
>
> **Dr. Falk:** Sie sind neu, Falk. Koje drei, Herr Baum, vasovagal, steht da.
>
> **Dr. Falk:** Ich brauch die Koje um halb acht, die Rettung hat zwei angemeldet. Kann er heim?
>
> *(ist das EKG noch nicht geschrieben, Flag `falk_gewartet`:)* **Dr. Falk:** Kein EKG? Schreiben Sie, ich les solang. *(Die Übergabe beginnt danach; die Uhr steht dann näher an halb acht.)*
>
> *Spielerin:* 1 Darf ich kurz übergeben? · 2 Nein. · 3 Ja, wahrscheinlich.
>
> **Dr. Falk** (1): Kurz. Wer, was, was Sie denken, was Sie wollen, in der Reihenfolge, wenn's geht.
>
> **Dr. Falk** (2 oder 3): Das ist eine Antwort, keine Übergabe. Wer, was, was Sie denken, was Sie wollen, dann reden wir über ja oder nein.

Rückmeldung zu (2)/(3), still: Ein Oberarzt mit zwölf Minuten will zuerst den Patienten, nicht dein Urteil. ISBAR:
Identifikation, Situation, Hintergrund, Einschätzung, Empfehlung. *(Übergabe-Standard, keine fachliche Aussage; §12)*

### 6.2 Die vier Zeilen (Mechanik: je Zeile eine Wahl; die gewählte Zeile erscheint als Replik der Spielerin)

Falk unterbricht nach der ersten Zeile und zieht das EKG vor; die Reihenfolge wird I/S → A → B → R. Die Karte
„Übergabe" ordnet sie danach wieder richtig (I, S, B, A, R) und sagt, warum er umgestellt hat.

**I/S (wer, was):**

| Option (≤ 64) | Art | Falk | `warum` |
|---|---|---|---|
| Herr Baum, 68. Zweimal weg ohne Vorwarnung, gestern und heute. | richtig | Zweimal? Da steht einmal, Küche. *(Spielerin: Gestern an der Haltestelle. Er hat's niemandem gesagt.)* Hm. | Wer, Alter, was, wie oft: das Entscheidende zuerst. Das zweite Ereignis gehört in den ersten Satz, weil die Notiz nur die halbe Geschichte kannte. |
| Herr Baum, 68, Synkope, vermutlich vasovagal. | vage, Anker | Vermutlich steht schon da. Was ist passiert? | Du hast ihm seine eigene Notiz vorgelesen. Situation heißt: was passiert ist, nicht was jemand vermutet. |
| Ein älterer Herr, dem schwindlig geworden ist. | falsch | Schwindlig? Er lag am Boden und weiß nichts davon, das ist nicht schwindlig, noch einmal. | Schwindel ist kein Bewusstseinsverlust. Vier Merkmale: kurz, umgesunken, keine Reaktion, Erinnerungslücke. Alle vier da. *(§4.1)* |

Bei `versprochen`: **Dr. Falk:** Und Ihnen hat er's gesagt, weil? *(Spielerin: Weil ich gefragt hab.)* **Dr. Falk:**
Steht nicht am Bogen, schreiben Sie's drauf.

**Falk unterbricht:** *EKG, bevor Sie weiterreden.*

**A (Einschätzung, vorgezogen):**

| Option | Art | Falk | `warum` |
|---|---|---|---|
| Sinus, {hf}, PQ {pq}, QRS schmal. Nicht normal, kein Beweis. | richtig | {hf}, {pq}. Gut. | Rhythmus, Frequenz, Überleitung, Kammer, und was es bedeutet: nicht normal (PQ > 200), aber nichts, was eine arrhythmische Synkope beweist. *(Lektion 10; §4.1.1)* |
| Bradykardie, {hf}. Das erklärt die Ohnmacht. | falsch in der Folgerung (Flag `brady_argument`) | {hf} unter Betablocker ist erwartbar, damit fällt niemand um. Was noch? | {hf} erklärt keine Ohnmacht und ist unter Betablocker erwartbar. Ein Warnzeichen wäre erst ein Puls dauerhaft unter 40 im Wachen, und die Leitlinie nimmt bremsende Medikamente ausdrücklich aus. Ob man {hf} Bradykardie nennt, hängt von der Quelle ab; die Folgerung ist falsch, nicht das Wort. *(Tab. 6; Tab. 5; QUELLEN §3)* |
| EKG unauffällig. | falsch | {pq} ist nicht unauffällig. Haben Sie gemessen oder geschaut? | PQ über 200 ms ist ein AV-Block I°. Ein EKG mit AV-Block I° ist nicht normal, auch wenn es niemanden umwirft. *(Lektion 3, 10)* |
| PQ hab ich nicht gemessen. *(nur ohne Karte PQ)* | Rückweg | Dann messen Sie, der Wagen steht da. Ich hab zwölf Minuten. | (bestehende Mechanik: Rückweg zum Wagen) |

**Stummer Zirkel-Takt** (nach der richtigen A-Zeile; Skill `handlung`, §14): Falk nimmt den Streifen.

> **Erzähler:** Falk zieht den Messingzirkel aus der Brusttasche und setzt ihn auf den Streifen, P-Anfang, QRS-Anfang. Drei Schläge, ohne ein Wort.
>
> **Dr. Falk:** {mess_pq}. Passt.

Die Karte „PQ-Zeit" bekommt die Zeile „von Dr. Falk nachgemessen: {mess_pq} ms (Median aller Schläge)". Das ist die
Bestätigung von außen für die Messung der Spielerin, und Falks Gegenstand (ART_BIBLE §5) kommt zum Einsatz.

**B (Hintergrund):**

| Option | Art | Falk | `warum` |
|---|---|---|---|
| Betablocker seit Jahren, heute nicht. Schellong negativ. | richtig | Heute nicht genommen. Merken wir uns. | *(gesprochen: Bluthochdruck seit zehn Jahren, Betablocker seit Jahren, heute nicht genommen, Stehversuch unauffällig.)* Vorerkrankung, Medikation mit Änderung (keine) und Einnahme (heute nicht), Stehversuch: das, was die Einschätzung trägt. *(Tab. 5; Web Table 5.6)* |
| Die Tochter hat's gesehen: kein Zucken, Augen offen, sofort da. | richtig (zweite B-Zeile, freiwillig) | Dann ist es kein Anfall. Das nehm ich. | Die Zeugin trennt Synkope von Anfall: keine Zuckungen, sofort klar. *(§8.1.2, Tab. 10)* |
| Er geht täglich mit dem Hund, ist fit für sein Alter. | vage | Schön für den Hund. Was nimmt er? | Belastbarkeit ist ein Befund gegen die strukturelle Herzkrankheit, aber Hintergrund heißt zuerst: Vorerkrankungen, Medikamente. |
| Drei Tabletten, welche weiß ich nicht. *(nur ohne Karte Medikamente)* | Rückweg | Dann holen Sie den Zettel. Drei Meter. | (bestehende Mechanik: Rückweg zum Patienten) |

**Was ausgelassen wurde, fragt Falk hier ab** (eine Lücke je Durchgang, Rückweg zum Patienten, die Uhr läuft):
*„Verletzt hat er sich? Wissen Sie nicht, dann fragen Sie ihn, drei Meter."* · *„Schon einmal gehabt? Das fragt
man als Erstes."* · *„Zucker, andere Krankheiten? Fragen Sie."* · *„Familie?"* Fehlt die Fremdanamnese (Anruf
verschoben und noch nicht nachgeholt): *„Wer hat ihn gefunden? Die Tochter, und die haben Sie nicht gefragt?"*

**R (Empfehlung):**

| Option | Art | Falk | `warum` |
|---|---|---|---|
| Er bleibt. Monitor. | richtig | Monitor, für einen Mann, der lang gestanden ist und Betablocker nimmt. Überzeugen Sie mich. | Die Empfehlung in einem Satz. Jetzt muss sie begründet werden; die Tabletten kommen danach (§6.4). |
| Er kann heim, Kontrolle beim Hausarzt. | Irrweg (Flag `heim_empfohlen`) | Das wollte ich hören. Sagen Sie mir, warum, und nicht, weil ich die Koje brauch. | Vertretbar wäre das nur bei niedrigem Risiko: Vorwarnung, normales EKG, keine Herzkrankheit. Prüf, ob du das hast. *(Tab. 6)* |
| Noch einen Stehversuch, dann sehen wir weiter. | Irrweg | Marlene hat ihn gemacht, dreimal gemessen, nichts. Was wollen Sie beim zweiten Mal sehen, was beim ersten gefehlt hat? | Der Stehversuch ist gemacht und negativ; er prüft die Orthostase, nicht das Risiko. Wiederholen beantwortet die Frage nicht. *(§4.2.2.1)* |

### 6.3 Die Gegenrede: „Überzeugen Sie mich"

> **Dr. Falk:** Lange gestanden, Betablocker, achtundsechzig, Kreislauf, die Steiner hat's auch so gesehen. Ich brauch die Koje, überzeugen Sie mich.

Mechanik (neu, `aufgaben.argument`): Die Spielerin wählt nacheinander Argumente; jedes ist eine Karte oder ein
Eintrag der Verdachtsliste, in einem Satz. Falk antwortet auf jedes und **sagt nach jedem Stützargument, was ihm
noch fehlt** (Platzhalter {fehlt}: *„Fehlt mir trotzdem der Grund, warum die Vorwarnung zählt."* wenn das
EKG-Argument fehlt; *„Fehlt mir, was das EKG dazu sagt."* wenn die Vorwarnung schon fiel; *„Fehlt mir trotzdem der
Grund, warum er nicht niedrig ist."* wenn beide fehlen). Er gibt nach, sobald die beiden tragenden Argumente
gefallen sind (keine Vorwarnung **und** EKG nicht normal), in beliebiger Reihenfolge. Kein Game Over.

| Argument (Option) | Falk | `warum` |
|---|---|---|
| **Keine Vorwarnung. Beide Male.** | *(EKG-Argument fehlt noch)* Zählt, mit dem EKG zusammen, das Sie mir vorhin gesagt haben. Sagen Sie's als Argument. *(sonst)* Zählt. Mit dem EKG zusammen ist er nicht mehr niedrig. | Fehlende Vorwarnung ist ein Minor-Merkmal: Es zählt nur zusammen mit einer Herzkrankheit oder einem nicht normalen EKG. *(Tab. 6)* |
| **PQ {pq}. Das EKG ist nicht normal.** | *(Vorwarnung fiel schon)* Nicht normal, nicht gefährlich. Mit der fehlenden Vorwarnung zusammen aber nicht mehr niedrig. *(sonst)* Nicht normal, nicht gefährlich, allein ist das nichts. Was macht es zu etwas? | Niedriges Risiko verlangt ein normales EKG. AV-Block I° ist nicht normal. Allein ist er kein Risikomerkmal; mit „keine Vorwarnung" zusammen ist der Patient nicht mehr niedrig. *(Tab. 6; Lektion 10)* |
| Zweimal in zwei Tagen. Das erste Mal mit 68. | Mit achtundsechzig fängt man nicht mit Kreislaufgeschichten an, geb ich Ihnen. {fehlt} | Die Reflexsynkope hat meist eine lange Vorgeschichte, oft seit der Jugend. Ein erstes Mal mit 68, und gleich zweimal, ist das Gegenteil davon; ein Risikomerkmal der Tabelle ist es nicht. *(Tab. 5, Tab. 6 Low-risk Nr. 8)* |
| Er hat sich verletzt. Ellbogen, Hüfte. | Die Schramme allein ist mir egal, die Schramme bei dem Rest nicht. {fehlt} | Verletzung durch die Synkope spricht für Aufnahme, wenn Risikomerkmale da sind; allein trägt sie nichts. *(Tab. 7)* |
| Stehversuch negativ, beim Kocher eine Minute gestanden. | Gut, dann ist es nicht der Kreislauf. Und was ist es dann? | Kein Abfall ≥ 20/10 mmHg nach drei Minuten, kein Sturz beim Aufstehen, nur eine Minute gestanden: Orthostase unwahrscheinlich. Das schließt aus, es beweist nichts. *(§4.2.2.1, Tab. 5, Tab. 6 Nr. 7)* |
| Die Tochter hat kein Zucken gesehen. | Kein Anfall, gut. Und warum bleibt er? | Zeugenbericht trennt Anfall und Synkope. Für die Risikofrage ist das kein Argument. *(Tab. 10)* |
| Puls {hf}, das ist eine Bradykardie. *(Flag `brady_argument`)* | Unter Betablocker ist {hf} erwartbar. Was noch? | {hf} erklärt keine Ohnmacht und ist unter Betablocker erwartbar; Warnzeichen erst dauerhaft unter 40 im Wachen, und die Leitlinie nimmt bremsende Medikamente aus. Das Wort hängt von der Quelle ab, die Folgerung ist falsch. *(Tab. 6, Tab. 5)* |
| Der Vater hatte einen Schlaganfall. | Mit achtzig. Wer ist bei Ihnen jung und plötzlich gestorben? *(Spielerin: Niemand.)* Dann weiter. | Das Familien-Merkmal heißt: plötzlicher Herztod in jungen Jahren. Ein Schlaganfall mit 80 ist keines. *(Tab. 6)* |
| Könnte es eine TIA gewesen sein? | Eine TIA nimmt etwas weg, Sprache, Kraft, ein Gesichtsfeld, das Bewusstsein lässt sie in Ruhe. Haben Sie ihn reden und gehen lassen? *(Spielerin: Ja. Alles seitengleich.)* Dann war's keine. | TIA = fokaler Ausfall ohne Bewusstseinsverlust; vertebrobasilär nie ohne Hirnstammzeichen. Hier: Bewusstsein weg, Ausfälle keine. *(Tab. 4, §8.1.3; Web Table 5.4)* |
| *(nach vier Argumenten ohne die beiden tragenden)* | Schauen Sie auf Ihre Liste. Was macht aus der fehlenden Vorwarnung ein Warnzeichen? | Hinweis, keine Lösung. |

Falk gibt nach:

> **Dr. Falk:** Gut, keine Vorwarnung und ein EKG, das nicht sauber ist, das ist nicht niedrig. Er bleibt am Monitor, bis ich den Speicher gesehen hab.
>
> **Dr. Falk:** Die Koje kriegt die Rettung trotzdem, oben ist ein Bett frei. Ich ruf an.

*Rückmeldung (`warum`, die zentrale des Falls):* Fehlende Vorwarnung zählt nur mit Herzkrankheit oder nicht normalem
EKG. Mit PQ {pq} ist er nicht mehr niedrig; das heißt Beobachtung am Monitor, nicht Entlassung. Das Ruhe-EKG beweist
nichts; beweisen würde eine Pause über drei Sekunden im Wachen, ein Mobitz II, ein AV-Block III° oder ein Puls
dauerhaft unter 40, und die sieht man nur, wenn jemand hinschaut, während es passiert. *(Tab. 6; §4.1.2: weder
niedrig noch hoch → Beobachtung in der Notaufnahme oder Synkopeneinheit statt Aufnahme, I B; §4.1.1; §4.2.4.1)*
→ Verdachtsliste: Herzrhythmus „nicht bewiesen, nicht ausgeschlossen"; Reflex durchgestrichen.

**Variante `heim_empfohlen`:** Falk fragt nach Gründen für die Entlassung; drei Optionen, alle bekommen eine
Gegenfrage: „Stehversuch negativ." → *Dann ist es nicht der Kreislauf. Darf er deshalb heim?* „Das EKG ist fast
normal." → *Fast.* „Er fühlt sich gut und will heim." → *Das hat er gestern auch, und heute lag er in der Küche.*
Danach: **Dr. Falk:** Sie überzeugen mich nicht. Andersrum: Warum soll er bleiben? → dieselbe Argumentation wie
oben. Rückmeldung: Entlassung aus der Notaufnahme nur bei niedrigem Risiko; prüf die Liste, nicht das Gefühl des
Patienten. *(Tab. 6, §4.1.2)*

### 6.4 Die Tabletten (07:24)

> **Dr. Falk:** Die Tochter sagt, seine Tabletten liegen daheim am Tisch. Was kriegt er jetzt von uns?
>
> *(bei `brady_argument`, davor)* **Dr. Falk:** Vorhin war Ihnen {hf} zu langsam. Jetzt geben Sie ihm die Bremse dazu?
>
> *Spielerin:* 1 Alle drei, wie immer. · 2 Ramipril und ASS. Bisoprolol erst nach dem Monitor. · 3 Nichts, bis alles geklärt ist.
>
> **Dr. Falk** (2): Gut, der Blutdrucksenker bremst keinen Knoten, den kann er haben. Der Betablocker wartet, ich schreib's auf.
>
> **Dr. Falk** (1): Mit {hf} und einer Überleitung von {pq} geben Sie ihm das Einzige, das beide bremst? Noch einmal.
>
> **Dr. Falk** (3): Warum soll er ohne Blutdrucksenker dastehen? Das Einzige, das bremst, ist das Bisoprolol, das andere kann er haben.

*Rückmeldungen:* (2) Betablocker bremsen Sinusknoten und AV-Überleitung; bei einer Bradyarrhythmie unter einem
solchen Medikament ist Dosisreduktion oder Absetzen der erste Schritt, bevor man an mehr denkt. ACE-Hemmer und ASS
bremsen keinen Knoten; der Blutdruck ist {rr_l_sys}/{rr_l_dia}, der Stehversuch unauffällig: kein Grund, sie
wegzulassen. *(ESC-Pacing-2021 §3.3/Tab. 6, §5.1.1.1; §5.1.1.2 sinngemäß; Pharmakologie QUELLEN §3; Weitergabe von
Ramipril/ASS ist Falks klinische Entscheidung, keine Leitlinienaussage)* (1) Das Bisoprolol ist das einzige Mittel auf
dem Plan, das Frequenz und Überleitung bremst; es jetzt zu geben, bevor der Monitor gezeigt hat, was die Leitung
ohne Bremse macht, verwischt die Frage, die ihr gerade gestellt habt. *(ESC-Pacing-2021 §5.1.1.1, Tab. 6)* (3) Nicht
gefährlich, aber ohne Grund: Ramipril und ASS haben mit der Ohnmacht nichts zu tun; wer ohne Grund absetzt, schafft
ein neues Problem. *(Pharmakologie)*

Ergebnis: Karte „Entscheidung (07:25)": Beobachtung am Monitor; Bisoprolol heute pausiert, Ramipril und ASS gegeben;
Dr. Falk. Behandlung wird so Teil des Falls (KONZEPT §1.7), ohne Dosisänderung, ohne neue Substanz.

### 6.5 Falk am Bett (07:26)

Falk geht zur Koje (Figur bewegt sich, §10), hört kurz ab.

> **Dr. Falk:** Herr Baum, Falk. Ich hör kurz.
>
> *(mit Karte „Untersuchung")* **Dr. Falk:** Regelmäßig, langsam, kein Geräusch, wie die Kollegin.
>
> *(ohne, zur Spielerin)* **Dr. Falk:** Haben Sie ihn abgehört? Dann jetzt. *(Befundzeilen, Karte „Untersuchung")*
>
> **Dr. Falk:** Ihr Herz leitet zu langsam, und Sie sind zweimal umgefallen. Das will ich über Nacht am Schirm sehen.
>
> **Dr. Falk:** Echo macht die Station morgen. Die Kollegin bleibt bei Ihnen.
>
> **Herr Baum:** Aber die Senta.
>
> **Dr. Falk** (schon im Gehen, zur Spielerin): Dreiviertel acht, Morgenbesprechung. Sie kommen nach, wenn er oben ist.

Die Aufklärung über den Verbleib ist Arztsache; Falk sagt den Grund in einem Satz. Dass Herr Baum ihn von der
Spielerin noch einmal hören will (§7.1), ist der Lernschritt, nicht der Ersatz für den Arzt. „Echo macht die
Station" ist Falks Anordnung, keine Behauptung des Spiels über eine Indikation (ESC §4.2.3, §12: zu prüfen).

*Prüfung des ganzen Takts:* D1: Falk nennt Zahlen zuerst, stellt Gegenfragen, lobt nie ohne Haken („geb ich
Ihnen"), kein Gedankenstrich, Pausen als kurze Sätze; zwei Antithesen, nicht sieben. D2: laut lesbar, keine Replik
über zwei Sätze. D3: Falk doziert nicht; die Tabellenlogik steht in den Rückmeldungen; der Normwert „Bradykardie ab
50" kommt nicht mehr aus seinem Mund. D4: Zeitdruck in „zwölf Minuten", „Koje", „Morgenbesprechung", nie „Ich bin
unter Druck". D5: jede Gegenrede bringt dem Fall ein Kriterium, zeigt Falk (prüft, nicht quält), hat Subtext („Ich
will, dass Sie recht haben, aber ich sag's nicht") und verschiebt die Beziehung (vom Abfragen zum Streiten auf
Augenhöhe); der stumme Zirkel-Takt ist die Atempause (Skill `handlung`, §14). D6: kurze Wechsel, Unterbrechungen, weil
Akutlage und Uhr. Entscheidungstest: R ist ein Dilemma, die Argumente sind Strategie, die Tabletten eine echte
Behandlungsentscheidung mit sichtbarer Folge (Karte, Epilog). Humanizer: „Schön für den Hund." ist trocken, nicht
aphoristisch.

---

## 7. Behandlung, Schlussgespräch, Ende, Epilog

### 7.1 Schlussgespräch mit Herrn Baum (07:30)

Ziel: Er bleibt, weil er versteht, warum, und weil die Senta versorgt ist. Falk hat den Grund gesagt; Herr Baum hat
ihn nicht verstanden und will ihn von der Spielerin hören. Er will nicht „was" haben und nicht zur Last fallen; er
bietet den Revers an, bevor jemand ihn nennt.

> **Herr Baum** (sitzt wieder, Jacke an): Frau Doktor, der Doktor hat was von Schirm gesagt, verstanden hab ich's nicht. Sie sagen's mir, und dann geh ich, die Senta sitzt daheim.
>
> **Herr Baum:** Ich unterschreib Ihnen alles.
>
> *Spielerin:* 1 Das ist jetzt nicht wichtig. Sie bleiben. · 2 Dann unterschreiben Sie einen Revers. · 3 Gestern und heute waren Sie weg, ohne es zu merken. · 4 Wegen der Senta: Die Frau Kainz hat den Schlüssel.
>
> **Herr Baum** (1): Für Sie nicht. *(dreht sich zum Fenster; die Optionen bleiben, (1) verschwindet)*
>
> **Herr Baum** (2, Flag `revers`): Her damit. Was steht da drauf, dass ich selber schuld bin?
>
> **Herr Baum** (4 vor 3): Die Kainz? Und wieso soll ich überhaupt bleiben, der Doktor hat was von Schirm gesagt und ist gegangen.
>
> **Herr Baum** (3): Ja, und? Jetzt bin ich ja da.
>
> *Spielerin:* 1 Das kann vom Herzen kommen. Ein Aussetzer. · 2 Ihr Herz schlägt langsam, die Überleitung auch.
>
> **Spielerin** (1): Das kann vom Herzen kommen, ein Aussetzer, ein paar Sekunden. Den sieht man nur, wenn Sie am Schirm hängen, während er passiert.
>
> **Herr Baum** (1): Ein Aussetzer. Und wenn's keiner ist?
>
> **Herr Baum** (2): Langsam bin ich überall. Das ist das Alter, nicht das Herz.
>
> **Spielerin:** Dann wissen wir morgen, dass es keiner war. Heute wissen wir's nicht, deshalb bleiben S' heut am Schirm.
>
> **Herr Baum:** Und die Senta?
>
> **Spielerin:** Die Frau Kainz hat den Schlüssel, Ihre Tochter ruft sie an. Das soll ich Ihnen sagen, von ihr glauben Sie's nicht.
>
> **Herr Baum** (Flag `senta_geloest`): Die Kainz, die mag sie eh, mehr als mich. *(zieht die Jacke aus, legt sie über den Sessel)* Dann bleib ich halt, aber die Mütze bleibt auf.
>
> *(bei `versprochen`)* **Herr Baum:** Sie haben's ihm gesagt, von gestern. *(Spielerin: Dem Arzt. Nicht der Sabine.)* Passt, der Arzt ist der Arzt.
>
> *(bei `tochter_verraten`)* **Herr Baum:** Die Sabine hat's gewusst, wie sie angerufen hat, von Ihnen. Die Kainz hat die Sabine ausgemacht, nicht Sie. *(zieht die Jacke trotzdem aus)*

*Rückmeldungen:* (1) „Nicht wichtig" ist für ihn das Wichtigste. Wer die Sorge wegwischt, verliert den Patienten,
nicht das Argument. (2) Den Revers nimmt der Arzt, nach Aufklärung. Du hast weder das eine noch das andere getan.
*(keine fachliche Aussage)* (3) Richtig: seine Worte („weg"), nicht deine (Synkope, Risiko). Dann der Grund in einem
Bild (Aussetzer) und was der Schirm kann. *(§4.2.4.1)* Zu „Ihr Herz schlägt langsam…": Das ist dein Befund, nicht sein
Problem; er hört „Alter" und hat recht. (4) Die Senta zuerst löst das Hindernis, aber nicht die Frage; er fragt zu
Recht „wieso überhaupt".

*Prüfung:* D1: Herr Baum bleibt derselbe (Senta, Kainz, Mütze, „halt"). D4: das Einlenken ist die Jacke, nicht ein
Satz. D5: die Szene bringt dem Fall die Entscheidung in Laiensprache und zeigt, was die Spielerin verstanden hat.
Entscheidungstest: Ausdruck (wie sie es sagt) mit sichtbarer Folge (Jacke, Flags), korrigierbar, kein Game Over. Die
Spielerin spricht keine Lehre mehr aus („nicht die Haltestelle" ist weg). Humanizer: ok.

### 7.2 Marlenes Abschied und Schlussbild (07:35–07:40)

> **Marlene** (mit Kanne, Jacke über dem Arm, an der Koje): So, ich geh. Herr Baum, oben haben's bessere Betten als da, und Sie lassen die Mütze auf, ich kenn Sie.
>
> **Marlene** (zur Spielerin): So. Schlaf du auch irgendwann.
>
> *(bei `revers`)* **Marlene:** Revers hat er dir angeboten. Hast ihn nicht gebraucht.
>
> *(bei `falk_gewartet`)* **Marlene:** Den Falk hast du warten lassen. Der merkt sich das, aber nicht lang.
>
> **Erzähler:** 07:40. Eine Pflegerin und der Transportdienst holen Herrn Baum ab, mit Transportmonitor, die Mütze auf dem Kopf, das Sackerl auf dem Bauch.
>
> **Erzähler:** Die Jacke bleibt über dem Sessel, du nimmst sie mit. Marlenes Stuhl ist leer, die Kanne ist weg; du gehst mit nach oben, dann zur Morgenbesprechung.

Echo auf den Anfang (Skill `handlung` §4): die Jacke (angezogen → über dem Sessel → in deiner Hand), die Mütze, die
Kanne, die Uhr. Keine Zusammenfassung, keine Moral, kein Mentorenlob.

### 7.3 Epilog (Dienst 3, eine Woche später, 18:40; Erzähler, ohne Porträt, ohne Kurve)

Zeit nach KONZEPT §3: Dienst 3 ist der Abenddienst auf der Intensivstation (18:50); der Epilog liegt davor, am Flur,
eine Woche nach Dienst 1, also nach dem Samstag der Entlassung.

> **Erzähler:** Dienst 3, eine Woche später, 18:40, auf dem Weg zur Intensivstation. Marlene fängt dich am Flur ab, die Kanne in der Hand; sie hat's von oben gehört.
>
> **Erzähler:** In der zweiten Nacht, als vom Betablocker praktisch nichts mehr da war, hat der Monitor eine Pause aufgezeichnet, länger als drei Sekunden. Er war wach, ihm war schwindlig, er hat geklingelt.
>
> **Erzähler:** Am Donnerstag hat er einen Zweikammer-Schrittmacher bekommen, am Samstag ist er heim, die Mütze auf dem Kopf.
>
> **Erzähler** (bei `senta_geloest`): Die Senta hat die Frau Kainz bis zum Parkplatz gebracht. Weiter durfte sie nicht.
>
> **Erzähler** (bei `tochter_beruhigt`): Die Tochter hat dich gefragt, warum du am Montag „Kreislauf" gesagt hast. Du hast es ihr erklärt, es hat gedauert.

*Karte „Epilog: Was der Monitor gezeigt hat":* Pause über drei Sekunden (Sinusstillstand oder Block, der Speicher
sagt's), im Wachen, mit Beschwerden, ohne bremsendes Medikament (letzte Bisoprolol-Dosis Sonntag früh, zweite Nacht
rund 65 Stunden später, mehr als fünf Halbwertszeiten, also praktisch nichts mehr da): eines der Kriterien, die
eine arrhythmische Synkope beweisen. Weil der Betablocker nicht mehr beteiligt war, war die Ursache nicht
reversibel; deshalb Schrittmacher, Zweikammer, statt Abwarten. *(ESC-Synkope-2018 §4.1.1 Nr. 5, I C; ESC-Pacing-2021
§5.1.1.1 (Schrittmacher nur bei symptomatischer Bradykardie, reversible Ursachen vorher korrigieren), §5.2.1.4
(reversible Ursache ausschließen), §5.1.2/§5.2.2.1 (Zweikammer); §5.4 nur sinngemäß, er gilt der Reflexsynkope;
Halbwertszeit Bisoprolol 10–12 h bei normaler Nierenfunktion, Pharmakologie-Standardwissen, QUELLEN §9)*

Was sich gegenüber dem heutigen Epilog ändert: Das Bisoprolol wird nicht „auf der Kardiologie zuerst abgesetzt",
sondern war seit Montag früh pausiert (Entscheidung aus Takt 6); die Pause in der zweiten Nacht fällt deshalb
schon in die Zeit ohne Wirkstoff, und die Zeile „drei Tage ohne Betablocker, dann wieder eine Pause" entfällt.
Mechanismus der Pause (Sinusarrest oder AV-Block) wird weiterhin nicht gezeigt (keine annotierte Aufnahme).

---

## 8. Realismus-Prüfung der Umgebung

Maßstab: eine internistische Notaufnahme in Österreich (Graz), Montag, 06:40, Schichtwechsel, erster Tag einer
KPJ-Studentin. Was ich aus der Praxis sicher weiß, steht ohne Vermerk; was vom Haus abhängt, trägt „beim Nutzer
prüfen". Der Nutzer (Arzt in Graz) ist hier die Quelle, nicht eine Leitlinie.

### 8.1 Was stimmt (bleibt)

- Tresen mit PC und Lampe, Wanduhr, Pinnwand (Dienstplan, Kaffeekasse), Jalousie mit Morgenlicht, EKG-Wagen mit
  Papier, Linoleum. Marlenes Kanne, Herrn Baums Sackerl mit Medikationsplan und Foto, die Schiebermütze.
- Pflegeanamnese mit Stehversuch (liegend, 1 min, 3 min) und Blutzucker-Stix durch die Pflege: Alltag.
- Sonnenaufgang 06:40: in Graz Anfang April oder Anfang September; passt zu „Sonntag, Friedhof, Bus jede Stunde".
- Falk kommt als Oberarzt des Tagdienstes herunter und ist um 09:15 (Kapitel 2) noch da: passt.

### 8.2 Was nicht stimmt (wird geändert)

| Heute | Richtig | Änderung |
|---|---|---|
| Synkopen-Patient sitzt 25 Minuten auf der Wartebank | Nach der Triage liegt er auf einer Liege in einer Koje (Box, Behandlungsplatz) mit Vorhang, Besuchersessel, Wandarm mit Blutdruckgerät; in einer internistischen Notaufnahme hat jede Koje einen Bettmonitor, und ein Synkopenpatient hängt ab Triage dran | Koje 3 statt Bank (Bildauftrag B1), **ausdrücklich ohne Monitor** (Überlaufkoje, „die Monitorkojen sind voll", Marlene §5.2): so bleibt „Monitor oder heim" scharf, und Falk braucht die Koje; er sitzt auf der Liegenkante, später liegt er |
| Kein EKG, ohne Grund | Das EKG gehört zur Erstbewertung (ESC-Synkope-2018 §4.1) und schreibt meist die Pflege bei der Triage | Grund im Text: Journaldienst-Ärztin seit 06:30 im Schockraum, Notiz „EKG ausständig", Marlene mit acht Übergaben; die KPJ-Studentin schreibt es (Studierende im KPJ schreiben EKGs); Blut ist abgenommen, Labor kommt um acht (keine Mechanik) |
| **Der Schirm des EKG-Wagens zeigt Herrn Baums Kurve, bevor eine Elektrode klebt** (`web/spiel.js` `starteSchirme`, `wagen_schirm`, Zeilen 554–581; Screenshot 01) | Ein Gerät ohne Patient zeigt nichts: dunkles Glas, Bereitschafts-LED; die Kurve erscheint beim Schreiben und verschwindet, wenn die Elektroden abgenommen sind | Schirm dunkel bis `ekg_geschrieben`; Kurve (LUDB 39) nur während des Schreibens, danach wieder dunkel; der Prototyp `prototyp/bewegung/leben.js` macht das schon (`ekg`/`ekg_aus`) |
| Kommt allein zu Fuß nach einer Ohnmacht im Morgengrauen | Angehörige bringen ihn; die Tochter fährt | Tochter hat ihn um 06:15 gebracht, musste zum Dienst (Kindergarten 07:00); sie ruft an |
| Kein Patientenarmband | Jeder aufgenommene Patient trägt eines (Name, Geburtsdatum; Daten setzt kein Bild, das Band ist leer) | weißes Band am linken Handgelenk in allen Posen, neben dem roten Bändchen (B2) |
| Niemand sonst da: kein Telefon, keine Rettung, keine Reinigung, kein Schichtwechsel | 06:40–07:40 ist die dichteste Stunde: Nachtdienst übergibt (Pflege 19:00–07:00, zwölf Stunden, in vielen Häusern üblich; beim Nutzer prüfen), Tagdienst kommt, Rettung bringt die Ersten, Reinigung fährt durch, Drucker läuft | Andrea (Tagdienst) ab 07:00 am Tresen, Übergabe im Hintergrund; Rettung im Flur 06:50 und 07:20; Reinigungskraft 07:05; Telefon am Tresen (06:40, 07:12); Drucker (07:16, Falks Liste) |
| Oberarzt kommt, wenn Marlene ruft | Der Oberarzt kommt zum Dienstbeginn herunter, liest die Übergabeliste, hat vor der Frühbesprechung wenige Minuten | Falk 07:15, Morgenbesprechung „dreiviertel acht" (Uhrzeit beim Nutzer prüfen), Rettung hat zwei angemeldet |
| „Tüte", „Bank", „Stuhl" | In Graz: Sackerl, Liege, Sessel | Texte; Klickfeld-Name `tuete` bleibt im Code, die Beschriftung heißt „Sackerl" |
| Strickjacke „unterm Patientenhemd" (ART_BIBLE §5) | Um 06:40 nach der Fahrt im Auto trägt er seine Kleidung; das Hemd macht er fürs EKG auf; ein Patientenhemd bekommt er oben | Posen ohne Patientenhemd (B2); ART_BIBLE §5 anpassen |
| Falk nimmt den Patienten nie wahr | Ein Oberarzt hört kurz ab und sagt dem Patienten einen Satz, bevor er geht | §6.5 |
| Triage nicht erwähnt | Österreichische Notaufnahmen triagieren (verbreitet Manchester-Triage); eine Synkope ohne Warnzeichen landet meist bei Gelb (beim Nutzer prüfen) | Bogen: „Triage 06:20"; Farbe nur im Text, nie im Bild |
| Revers kommt nicht vor | Der Revers (Entlassung gegen ärztlichen Rat) ist in Österreich der Alltagsbegriff, Patienten bieten ihn selbst an | §7.1 |
| Händedesinfektion | Spender an der Kojenwand | B1 (Requisite, keine Mechanik) |

Offen gelassen (keine Mechanik, nur Erwähnung): Dienstkleidung und Namensschild der KPJ-Studentin („kriegst du um acht
von der Verwaltung" könnte Marlene sagen; nicht nötig), Transport nach oben (Transportdienst mit Pflegeperson; die
Spielerin geht mit, der Transport mit Pflegebegleitung und Transportmonitor, weil der Verdacht auf eine
rhythmogene Synkope besteht).

### 8.3 Bildaufträge (ohne Schrift, ohne gemalte EKGs, ohne Menschen in den Raumebenen; ART_BIBLE §6)

| Nr. | Auftrag | Technik | Aufwand |
|---|---|---|---|
| **B1** | **Aufnahme neu rendern:** links Tresen wie heute, dazu Telefon mit Hörer, kleiner Drucker, Desinfektionsspender an der Wand; Mitte Fensterfront (Sonne **nicht** rendern, sie wird SVG), Lampe am Tresen ohne eingebrannten Lichtkegel; rechts hinten Flurdurchgang als Glastür mit Seitenscheibe, mindestens 300 px breit (heute 67 px: Silhouetten sind dort unsichtbar); rechts **Koje 3, ausdrücklich ohne Bettmonitor** (Überlaufkoje; die Monitorkojen liegen links hinter dem Tresen außerhalb des Bildes): Liege mit erhöhtem Kopfteil (Mint-Bezug), Vorhang an Deckenschiene halb zugezogen (Petrol), Besuchersessel (Holz/Petrol), Wandarm mit Blutdruckgerät, zwei Wandanschlüsse, Haken; EKG-Wagen **als eigene Ebene** `wagen.png` an der Wand zwischen Tresen und Koje, Schirm als dunkles Glas (Kurve und LED kommen aus dem Code). Rost-Objekt bleibt die Betablocker-Schachtel im Sackerl. Hitboxen: `marlene`, `tresen_telefon`, `wagen`, `koje` (Herr Baum), `tuete`, `uhr`, `pinnwand`, `ausgang`. | Blender-Pipeline (`gen/blender/`), drei Ebenen + Wagen | 1–2 Tage |
| **B2** | **Herr Baum, vier Posen** auf transparentem Grund, gleiche Figur wie `herrk.png`: (a) steht mit Jacke, Sackerl in der Hand; (b) sitzt auf der Liegenkante, Jacke an; (c) liegt mit offenem Hemd, Mütze auf (Elektroden und Kabel setzt der Code als SVG-Punkte und -Linien, damit Ampel-Regel und Lage stimmen, FACHREGELN Lektion 2); (d) sitzt ohne Jacke, Mütze auf. In allen: weißes Patientenarmband links neben dem roten Bändchen, Hörgerät, Hausschuhe. Kopf-Ausschnitt für Lidschlag/Blick (`leben.js` `kopf.loch/kopf`) je Pose vermessen. | GPT Image (Edit der bestehenden Figur, Maske), danach Ebenenprüfung | 0,5–1 Tag |
| **B3** | **Marlene, drei Zusatzbilder:** (a) Kanne am Mund; (b) Hörer am Ohr; (c) mit Jacke über dem Arm (Abschied, am Tresen vorbei). Gleiche Größe und Ankerpunkt wie `marlene.png`. | GPT Image (Edit), wie STAND.md „Prototyp: Marlene trinkt" | 0,5 Tag |
| **B4** | **Falk in der Aufnahme:** `art/szenen/monitor/figuren/falk.png` wiederverwenden (am Tresen, an der Koje; skaliert auf die Bodenlinie). Optional eine Pose „hört ab" (Stethoskop in der Hand). | vorhanden; optional GPT Image | 0–0,5 Tag |
| **B5** | **Andrea (Tagdienst):** nur als Silhouette hinter der Glasscheibe und als halb verdeckte Figur hinter dem Tresen (Rücken, Dutt, Kittel). Keine eigene Stimme, kein Porträt. | SVG-Silhouette von Hand; optional Figur per GPT Image | 0,25 Tag |
| **B6** | **Flur-Silhouetten:** drei Gruppen in Petrol: zwei Rettungssanitäter mit Trage (keine Logos, keine Kreuze), Reinigungskraft mit Wagen, Pflegeperson. Nur Umriss, 2–3 Beinstellungen für den Gang. | SVG von Hand (wie `leben.js` `baueFlur`) | 0,25 Tag |
| **B7** | **Hörer-Symbol** für den Telefon-Dialog (statt Porträt), Zirkel-/Mappen-Stil. | SVG vom Code | 0,1 Tag |

---

## 9. Ersatz für „Drei Monitore" in Kapitel 2

Abgestimmt auf `docs/faelle/monitor.md` (Frau Lindner, Vorhofflimmern, Lektion 31). Die Zentrale bleibt die
Mechanik; das Rätsel „welches Bett" entfällt. Was bleibt: die Zahlen vom Morgen werden noch einmal gebraucht.

### 9.1 Die Zentrale, realistisch

Drei Schirme mit **Bett und Namen, vom Code gesetzt** (ART_BIBLE §6: Text nur aus dem Code): „1 · Baum K." (LUDB 39,
laufend, HF 53), „2 · Lindner G." (LUDB 96, laufend, unregelmäßig, HF 90), „3 · Pichler F." (LUDB 114, laufend,
HF 91; namenloser Dritter bekommt einen Namen, sonst ist es wieder ein Rätsel). Jeder Schirm trägt Ableitung,
Frequenz und die Alarmgrenzen als kleine Zahlen (Werkseinstellung 50/120; die Zahlen setzt der Code).

Leben (§10): Bett 3 meldet um 09:16 einen **technischen Alarm** „Elektrode ab" (gelber Rahmen, Text vom Code, das
Kurvenfeld leer, kein Strich, keine gemalte Linie); eine Pflege-Silhouette geht hinüber, nach zwanzig Sekunden
läuft die Kurve wieder. Keine Aufgabe, keine Frage; es zeigt, dass nicht jeder Alarm ein Herz ist (Gerätealltag,
keine fachliche Aussage; die Artefakt-Lektionen 36/38 stützen die Einordnung).

### 9.2 Die Rückblick-Aufgabe: „Monitor gegen Papier"

> **Dr. Falk:** Bett 1, Ihr Herr Baum, der Schirm und Ihr Papier von heute früh. Was weiß der Schirm, was das Papier nicht weiß, und umgekehrt?

Frage am Standbild von Bett 1 mit der Karte „PQ-Zeit" daneben (Mappe-Vergleich):

| Option | richtig? | Rückmeldung | Beleg |
|---|---|---|---|
| Rhythmus und Frequenz, sicher. Die PQ-Zeit nur grob. | ja | Der Monitor zeigt Rhythmus und Frequenz und erkennt eine Pause, einen Block mit ausgefallenen Schlägen, eine Bradykardie sicher. Die Monitorableitung ist meist keine Standardableitung; Feinanalyse (PQ, ST, P-Form) nur mit größter Zurückhaltung. Dafür das Papier vom Morgen. | Lektion 31 |
| Alles, was das Papier zeigt, nur kleiner. | nein | Die Monitorableitung ist meist keine Standardableitung; PQ, ST-Strecke und P-Form gehören aufs 12-Kanal-EKG. Was du heute früh gemessen hast, misst kein Schirm. | Lektion 31 |
| Nichts Verlässliches, das ist nur ein Monitor. | nein | Bradykardie, Pausen, AV-Block II°/III°, Asystolie, Tachykardien, neue breite Komplexe: das erkennt der Monitor ausreichend sicher. Dafür liegt Herr Baum dran. | Lektion 31 |

Zweite Frage, die den Morgen abschließt:

> **Dr. Falk:** Und wofür hängt er dran? Was soll der Schirm heute Nacht sehen?

| Option | richtig? | Rückmeldung | Beleg |
|---|---|---|---|
| Eine Pause oder einen Block, bei dem Schläge ausfallen. | ja | Genau das, was das Ruhe-EKG nicht gezeigt hat und was eine arrhythmische Synkope beweisen würde: Pause > 3 s im Wachen, Mobitz II, III°, Puls dauerhaft unter 40. Der Monitor erkennt das sicher. | ESC-Synkope-2018 §4.1.1; Lektion 31 |
| Dass die Frequenz unter fünfzig fällt. | halb | Die Frequenzgrenze läutet bei einem, der bei 53 läuft, den ganzen Tag, ohne etwas zu beweisen. Worauf ihr wartet, ist eine Pause oder ein Block. Dafür hat der Monitor eigene Alarme. | Lektion 31 (Alarme für Frequenzgrenzen und komplexe Arrhythmien) |
| Die ST-Strecke. | nein | Feinanalyse ist Sache des 12-Kanal-EKGs, nicht des Monitors. | Lektion 31 |

Zur **individuellen Alarmgrenze** (Vorschlag des Koordinators): Falks Satz „Die Untergrenze hab ich auf
fünfundvierzig gestellt, sonst läutet er den ganzen Tag" wäre Alltag, aber ohne gelesene Quelle. Die
AHA-Praxisstandards 2017 (Sandau et al., Circulation 2017;136:e273) enthalten einen Abschnitt Alarmmanagement; der
Volltext war am 18.10.2026 nicht abrufbar (§12, neu, zu prüfen). Empfehlung: den Satz erst einbauen, wenn der
Abschnitt gelesen ist; bis dahin bleibt die Zahl weg, die zweite Frage reicht.

Danach wie in `monitor.md` §6.2 ff.: der Alarm von Bett 2 (Ampel), Frau Lindner, das Blatt. Falks Überleitung:
„Die zwei anderen gehören heute auch Ihnen. Bett 2 kennen Sie noch nicht. Das Bett kennt Sie gleich." bleibt.

---

## 10. Bewegung und Leben im Raum

Grundlage: der Prototyp `prototyp/bewegung/leben.js` (+ `aufnahme.html`, `baue.py`; `bau/prototyp_bewegung_de.html`).
Alles stumm verständlich; `prefers-reduced-motion`: nur Uhr und Zustände, keine Bewegung (so schon im Prototyp).
Kurven auf Schirmen nur aus `data/`.

### 10.1 Was der Prototyp schon kann (übernehmen in `web/motor/leben.js`)

| Bewegung | Technik im Prototyp | Bemerkung |
|---|---|---|
| Uhr mit Sekundenzeiger (Echtzeit, Nachfedern), Stunde/Minute nach Spielzeit | SVG-Zeiger in der Hintergrund-Ebene, `Leben.zeit(min)` | ersetzt die heutigen `#uhr-std/#uhr-min` |
| Lidschlag, Kopfdrehung, Blickwechsel (Marlene: tippt, schaut auf, schaut zu ihm; Herr Baum: zur Uhr, je später desto öfter) | Kopf als geclipptes zweites `<image>` derselben PNG, Posenplan je Figur | braucht je Pose die Kopf-Polygone (B2) |
| Lichtkeil mit Staub, bis 07:50 blasser; Wolken dämpfen | SVG-Polygon mit Verlauf und Partikeln, `sonne()` aus der Spielzeit | Lampe am Tresen fehlt noch |
| Vögel, Mann mit Hund vor dem Fenster | SVG, geclippt auf die Scheiben | |
| Leute im Flurdurchgang (alle 12–30 s) | Silhouetten, geclippt auf `flur` | Durchgang ist 39 px breit; nach B1 breiter |
| Unscharfe Pflegerin im Vordergrund (`vorbei`) | SVG-Figur mit Blur, über die Bühne | |
| Handy vibriert in Herrn Baums Tasche (`handy`) | Pose „tasche" + Leuchten | im Redesign liegt das Handy im Sackerl: Position ändern |
| EKG-Wagen: Bernstein-LED in Bereitschaft; beim Schreiben Kurve (LUDB 39) und Papierstreifen (`ekg`/`ekg_aus`) | Leinwand im Schirmrechteck, Papier wächst | behebt den Realismusfehler aus §8.2 |
| Schalter „Bewegung aus" | `Leben.bewegung(false)` | kommt ins Menü |

### 10.2 Was fehlt

| Bewegung | Technik | Aufwand |
|---|---|---|
| **Posen** von Herrn Baum (steht → sitzt → liegt → sitzt ohne Jacke) | `Leben.pose(figur, name)`: `href` der Figur tauschen, 150 ms Überblendung (reduced-motion: sofort); Kopf-Polygone je Pose aus `figuren.json` | 0,5 Tag Code + B2 |
| **Marlene**: Kanne trinken (alle 40–90 s, nie während sie spricht), Hörer am Ohr (06:40, 07:12), Jacke über dem Arm (Abschied), Weg zur Koje (07:35) | Bildtausch wie oben; der Weg als Translate der Figur entlang der Bodenlinie, 2 s, Beine nicht animiert (Ligne claire verträgt „gleiten" nicht gut → stattdessen Ausblenden am Tresen, Einblenden an der Koje, 400 ms) | 0,5 Tag + B3 |
| **Wagen rollt** von der Wand zur Koje (07:02) und zurück (07:10) | eigene Ebene `wagen.png` (B1); Translate 1,6 s mit leichtem Nachwippen; Räder als zwei SVG-Kreise mit Rotation; Schirm-Leinwand und Papier wandern mit (`schirme.json` relativ zur Wagen-Ebene) | 0,5 Tag |
| **Elektroden** auf Herrn Baum beim Schreiben | SVG-Punkte (rot/gelb/grün/schwarz nach Ampel-Regel, Lektion 2) und dünne Linien zum Wagen; erscheinen mit dem Klick „Zehn Sekunden ruhig" | 0,25 Tag |
| **Falk kommt** (07:15): Glastür geht auf, Falk im Durchgang, dann am Tresen; (07:26) an der Koje; (07:28) ab | Tür als eigene kleine Ebene (Clip-Reveal, 600 ms); Falk-Figur (B4) ein-/ausblenden an drei Ankerpunkten | 0,5 Tag |
| **Andrea** erscheint 07:00 hinter dem Tresen (halb verdeckt), spricht nicht; 07:35 bleibt sie allein | Silhouette/Figur einblenden | 0,25 Tag + B5 |
| **Telefon am Tresen** klingelt (06:40 beim Start, Marlene legt auf, wenn die Spielerin kommt; 07:12 Andrea hebt ab) | Hörer-Wackeln 2 Hz, 3 s, kleine Lichtfläche; stumm verständlich | 0,25 Tag |
| **Drucker** am Tresen spuckt Falks Liste (07:15), das EKG-Blatt kommt vom Wagen (07:08) | Papierstreifen-SVG wächst (wie beim Wagen) | 0,1 Tag |
| **Lampe am Tresen** geht um 07:20 aus (Andrea), Lichtkegel als SVG | Kegel-Polygon mit Verlauf, Opacity 1 → 0 in 300 ms | 0,1 Tag (B1 ohne eingebrannten Kegel) |
| **Sonne** steigt (SVG-Kreis, 06:40 → 07:50 um 40 px nach oben), Himmelsbänder hellen auf | `sonne()` erweitert | 0,1 Tag (B1 ohne Sonne) |
| **Straßenbahn/Bus** hinter den Büschen (alle 4–7 min, 6 s) | Silhouette in Petrol, Translate, geclippt auf die Scheiben | 0,2 Tag |
| **Rettung im Flur** mit Trage (06:50, 07:20), Reinigungswagen (07:05) | Silhouettengruppen (B6) im `baueFlur`-Mechanismus, aber **zeitgebunden** statt zufällig | 0,25 Tag |
| **Herr Baums Fuß wippt**, wenn er sitzt und wartet (Ungeduld, nimmt ab, sobald die Jacke aus ist) | Clip des Fußes, 1,5-px-Hub, Takt aus `ungeduld` | 0,2 Tag |
| **Jacke** über dem Sessel ab 07:32 | Teil der Pose (d) oder eigene kleine Ebene | B2 |
| **Verdachtsliste** und Mappe: Einträge ordnen sich still um (keine Blinker) | CSS-Transition 300 ms, reduced-motion: keine | 0,1 Tag |

Summe neu: rund 4 Tage Code und 2–3 Tage Kunst (B1–B7).

### 10.3 Story-Ereignisse → Bewegungen (die Kopplung)

| Spielzeit / Auslöser | Ereignis `Leben.ereignis(...)` | Was man sieht |
|---|---|---|
| 06:40 Start | `telefon_tresen`, `pose:marlene:hoerer` | Marlene telefoniert, Herr Baum steht (Pose a), schaut zur Uhr |
| Klick auf Marlene | `pose:marlene:auf` (legt auf) | Szenenbild |
| 06:45 Klick auf Herrn Baum, Option „Setzen Sie sich" | `pose:herrk:sitzt` | er setzt sich auf die Liegenkante; Fuß wippt |
| 06:50 (Zeit) | `flur:rettung` | zwei Silhouetten mit Trage von rechts nach links |
| 06:57 Wendung erzählt | `uhr_blick` aus; Blick zum Sackerl (`blicke.tasche` langsam) | er schaut weg |
| 07:00 (Zeit) | `andrea_kommt`, `pose:marlene:uebergabe` (Kuli hinterm Ohr, dreht sich zu Andrea) | Übergabe am Tresen, Marlene trinkt zwischendurch |
| 07:02 Klick auf den Wagen (frei nach dem Kern der Runde 1) | `marlene:zum_wagen`, `wagen:zur_koje` (Marlene schiebt, Figur wandert mit), `pose:herrk:liegt`, `elektroden:an` | Marlene schiebt den Wagen an die Koje und fragt „Und? Darf er?"; Herr Baum liegt, Punkte erscheinen |
| 07:04 im Dialog „Zehn Sekunden ruhig" | `handy` (im Sackerl), danach `telefon:dialog` | Handy leuchtet und vibriert im Sackerl; Hörer-Symbol im Dialog |
| 07:05 (Zeit) | `flur:reinigung` | Reinigungswagen |
| 07:08 EKG geschrieben | `ekg` (Kurve + Papier, 10 s), dann `ekg_aus`, `elektroden:aus`, `wagen:zurueck`, `pose:herrk:sitzt` | Papier wächst, Streifen-Dialog öffnet sich, Wagen rollt zurück |
| 07:12 (Zeit) | `telefon_tresen` (Andrea hebt ab) | |
| 07:15 Falk (in jedem Fall) | `tuer:auf`, `falk:tresen`, `drucker` | Tür, Falk, Liste |
| 07:17 nach der A-Zeile | `falk:zirkel` (3 s) | Falk beugt sich über den Wagen, Zirkel-Symbol wandert über den Streifen; stumm |
| 07:20 (Zeit) | `lampe:aus`, `flur:rettung` | Licht ändert sich, zweite Rettung (die angemeldete) |
| 07:26 Falk am Bett | `falk:koje` | |
| 07:28 Falk ab | `falk:ab`, `tuer:zu` | |
| 07:32 Jacke aus | `pose:herrk:ohne_jacke`; Fußwippen aus | Jacke über dem Sessel |
| 07:35 Marlene geht | `pose:marlene:jacke`, `marlene:zur_koje`, dann `marlene:ab` | Stuhl leer, Kanne weg |
| 07:40 Ende | `transport` (zwei Silhouetten mit Liege von rechts), Figur Herr Baum aus | Schlussbild |
| ständig | Lidschlag, Atem, Blicke, Licht, Vögel, Bahn, Staub | |

Reduced-motion: Posen und Zustände (Wagen an der Koje, Lampe aus, Jacke über dem Sessel, Falk da/weg) gelten
sofort; keine Translate, kein Lidschlag, kein Staub, keine Silhouetten; das Telefon zeigt nur die Lichtfläche.

---

## 11. Umbauliste (Reihenfolge)

1. **Freigabe** dieses Entwurfs durch den Nutzer; offene Entscheidungen (§13) beantworten.
2. **Akte** `docs/faelle/aufnahme_baum.md` nachziehen (Skill `fallakte`): §3 Patient (Tochter Sabine, Senta, Frau
   Kainz, Dr. Reiter, zwei Ereignisse: Sonntag Haltestelle, Montag Küche), §4 um die Risikokette aus §2.2 hier,
   §5 Anamnese in drei Runden mit Kern und Rest und der neuen Pflichtfrage „grad erst aufgestanden?", §6 Rhythmusfrage neu, §8 Ende mit Behandlungsentscheidung (Bisoprolol pausiert),
   Epilog neu, §9 Belege um §12 hier. `docs/QUELLEN.md`: §5 schließen (Tab. 6, Tab. 7, §4.2.2.1 am Postprint geprüft, Fundstelle eintragen), §9 anpassen
   (Epilog-Belege §5.1.1.1/§5.2.1.4), neuer §10 für die neuen Belege. KONZEPT §2 und ART_BIBLE §5: Spielfigur
   einheitlich KPJ-Studentin. `docs/FACHREGELN.md` „Nicht aus dem EKG-Kurs": ISBAR, Verschwiegenheit (keine Medizin, aber
   Spielinhalt). Skill `dialoge` §4: Stimmprofil Sabine Baum. `docs/ART_BIBLE.md` §5: Herr Baum ohne Patientenhemd,
   Patientenarmband; §4 bleibt.
3. **Motor** (`web/motor/`), neu oder erweitert:
   - `verdacht.js`: Verdachtsliste (Einträge, Zustände, Gründe, Karte, HUD-Knopf, stille Meldung); Wirkung
     `verdacht:EINTRAG:ZUSTAND:TEXTID`.
   - `fall.js`: Aufgabentypen `sbar` (Zeilen mit Optionen, Unterbrechung, Umstellung der Reihenfolge, Karte) und
     `argument` (Argumente aus Karten/Verdacht, Antworten, Bedingung für das Nachgeben, Hinweis nach n Versuchen);
     Dialogfigur ohne Porträt mit Symbol (`figur: "tochter", symbol: "hoerer"`); Wirkungen `pose:FIGUR:NAME`,
     `leben:EREIGNIS`, `anruf:BAUM.KNOTEN` (verzögert, Flag `anruf_spaeter`); Meldungen in Figurenstimme vom
     Tresen (`melde:ID:marlene`); Runden-Logik für die Anamnese (Kern schließt die Runde, Rest auslassbar, „Das reicht mir fürs Erste"; Falk fragt
     Ausgelassenes in B ab). Uhr: `zeit:+1` je Frage und Handlung, `+2` je Messung; Falks Auftritt zeitgesteuert
     (`leben: [{ zeit: 435, tu: "dialog:falk.ankunft" }]`), Flag `falk_gewartet` ohne EKG; Aufgabentyp `argument`
     mit Platzhalter `{fehlt}` und Nachgeben nur mit beiden tragenden Argumenten; stummer Zirkel-Takt
     (`leben:falk:zirkel`, Karte PQ ergänzt `{mess_pq}`).
   - `leben.js` aus dem Prototyp übernehmen und um §10.2 erweitern; Zeitereignisse aus den Falldaten
     (`leben: [{ zeit: 410, tu: "flur:rettung" }, …]`); Schalter „Bewegung" im Menü; reduced-motion.
   - Stand der Schicht: oben die dramatische Frage mit Frist, darunter höchstens drei Sätze (kein Pflichtfragen-Zähler);
     Knopf „Zum Tresen, Falk ist da" ab `ekg_geschrieben` (stellt die Uhr auf 07:15, falls früher; kein Softlock).
   - `web/spiel.js`: Wagen-Schirm dunkel bis zum Schreiben (§8.2); Kapitel 2 Zentrale mit Namen, Aufgabe „Monitor
     gegen Papier" (§9), technischer Alarm Bett 3 (bis Kapitel 2 als Fall `monitor` migriert ist).
4. **Falldaten** `web/faelle/aufnahme_baum.js` neu in Takten (Dialogbäume `auftakt`, `marlene`, `herrk` (Runden),
   `tochter`, `falk` (ISBAR, Argument, Tabletten, Bett), `schluss`; Flags aus §3; Karten; `leben`-Ereignisse).
   Falks Auftritt kommt um 07:15 nach der Uhr, die mit jeder Handlung läuft; ohne EKG wartet er (`falk_gewartet`),
   fehlt ihm eine Zahl, schickt er zum Wagen, fehlt eine Antwort, zum Patienten (bestehende Rückwege).
5. **Texte** `text/de/aufnahme_baum.json` komplett neu (IDs nach Takten), dann `en`, `ru` mit denselben Schlüsseln
   (`tools/woerter.py`). Humanizer-Durchgang (`grep -c "—"` muss 0 bleiben).
6. **Kunst** B1–B7 (§8.3); `art/szenen/aufnahme/figuren/figuren.json` um Posen und Kopf-Polygone; `schirme.json`
   relativ zur Wagen-Ebene; `gen/kunst.py` für die neue Ebene.
7. **Prüfungen** `tools/durchlauf.mjs`: Runden-Engpässe (keine Frage überspringbar, kein Hub), Wendung mit allen drei
   Antworten und Folgen (`versprochen` bei Falk und im Schluss), Anruf jetzt/später, alle drei Antworten der Tochter,
   Rhythmusfrage vier Optionen, Zirkel wie heute, ISBAR alle Zeilen inkl. Rückwege, Argumente (Nachgeben nur mit den
   beiden tragenden; Hinweis nach vier), `heim_empfohlen`-Variante, Tabletten drei Optionen, `brady_argument`-Echo,
   Schlussgespräch alle Wege inkl. `revers`, Verdachtsliste-Endzustand, Epilog-Varianten, Kern/Rest je Runde
   (Runde schließt nach dem Kern; Falk fragt Ausgelassenes ab), 07:15 ohne EKG (`falk_gewartet`), Stand-Knopf
   „Zum Tresen", Zirkel-Takt mit `{mess_pq}`, alle `{fehlt}`-Varianten, keine ausgeschriebenen Messwerte in
   Repliken, höchstens zwei Sätze je Replik, Wagen-Schirm dunkel vor dem
   Schreiben, Posen, reduced-motion (keine Animation, Zustände gesetzt), Kapitel 2 mit Namen und neuer Aufgabe,
   Textmaße (220/64), Gedankenstrich-Verbot, keine Lektionsnummern.
8. `docs/STAND.md`, `docs/UMBAU.md` nachziehen; Commit nach jedem Schritt.

Reihenfolge der Sitzungen (Tokensparen, CLAUDE.md): (a) Akte + Texte, (b) Motor, (c) Falldaten + Prüfungen,
(d) Kunst + Leben, (e) Kapitel 2.

---

## 12. Beleg-Tabelle

Bestehende Belege (FACHREGELN, QUELLEN §3, §8a, §9) gelten weiter; hier nur, was dieser Entwurf zusätzlich braucht
oder anders gewichtet. „geprüft" = am 18.10.2026 am Original gelesen (ESC-Synkope-2018 als akzeptiertes Manuskript,
Postprint der Universität Florenz: https://flore.unifi.it/bitstream/2158/1146550/5/2158-1146550_POSTPRINT.pdf;
ESC-Pacing-2021 am OUP-Volltext; KAKuG §9 im RIS). „neu, zu prüfen" = per Websuche gefunden, vor dem Einbau lesen.

| Aussage im Entwurf | Beleg | Status |
|---|---|---|
| Low-risk verlangt u. a. ein normales EKG und ein Prodrom typisch für Reflexsynkope; Minor-Ereignismerkmale (keine Vorwarnung / Prodrom < 10 s, Familie SCD jung, im Sitzen) gelten als hohes Risiko nur mit struktureller Herzkrankheit und/oder abnormem EKG; Minor-EKG-Merkmale nur, wenn die Anamnese zu einer arrhythmischen Synkope passt | ESC-Synkope-2018 Tab. 6 | **geprüft** am Postprint (Manuskriptzeilen 479–480): Low-risk Nr. 8 (lange Vorgeschichte gleichartiger Episoden), Nr. 10 (unauffällige Untersuchung), Nr. 11 (normales EKG); Minor „high risk only if associated with structural heart disease or abnormal ECG"; EKG-Minor Nr. 20 „1° degree AV block with markedly prolonged PR interval", „only if history consistent with arrhythmic syncope"; „abnormal ECG" nicht definiert (Fußnote a). Alter kommt nicht vor. QUELLEN §5 schließen |
| „AV-Block I° mit deutlich verlängerter PQ" steht in Tab. 5 (EKG-Merkmale, die eine arrhythmische Synkope nahelegen) | ESC-Synkope-2018 Tab. 5 | bestehend; am Online-Volltext 18.10.2026 gesehen |
| Tab. 7: „Syncope without prodrome" bei den Hochrisiko-Merkmalen, die für eine Überwachungseinheit der Notaufnahme / Synkopeneinheit sprechen; „Injury caused by syncope" bei denen, die für eine Aufnahme sprechen | ESC-Synkope-2018 Tab. 7, §4.1.2 | **geprüft** (Postprint Z. 525): Spalte 1 „Favour initial management in ED observation unit and/or fast-track to syncope unit: High-risk features AND … Syncope without prodrome"; Spalte 2 „Favour admission to hospital: High-risk features AND … Injury caused by syncope". Beide setzen Hochrisiko-Merkmale voraus: im Spiel nur als Stütze |
| §4.1.2: Low-risk braucht keine weiteren Tests in der Notaufnahme; High-risk „intensive diagnostische Abklärung, ggf. dringliche Behandlung und Aufnahme", Überwachung dort, wo reanimiert werden kann; „weder noch" → Überwachungseinheit / Synkopeneinheit; kein direkter Nachweis, dass die Aufnahme selbst das Ergebnis ändert | ESC-Synkope-2018 §4.1.2 | **geprüft** (Postprint Z. 484–494 und Empfehlungstabelle „Management of syncope in the ED": Low-risk entlassen I B; High-risk intensiv abklären I B; „neither … observed in the ED or in a syncope unit instead of being hospitalized" I B). Herr Baum: „weder noch" → Beobachtung |
| §4.2.4.1: Überwachung im Haus (Bett oder Telemetrie) ist bei Hochrisiko-Merkmalen, die eine arrhythmische Synkope nahelegen, gerechtfertigt, vor allem unmittelbar nach der Synkope; Ausbeute 1,9–17,6 % | ESC-Synkope-2018 §4.2.4.1 | **geprüft** (Postprint Z. 727–731; Empfehlung „Immediate in-hospital monitoring (in bed or by telemetry) is indicated in high-risk patients" I C). Für Herrn Baum stützt der Abschnitt die Form der Beobachtung, nicht eine Hochrisiko-Einstufung |
| Stehversuch: abnorm ist ein progredienter, anhaltender Abfall des systolischen Drucks ≥ 20 mmHg oder des diastolischen ≥ 10 mmHg oder systolisch < 90 mmHg | ESC-Synkope-2018 §4.2.2.1 (nicht §4.2.1) | **geprüft** (Postprint Z. 604); QUELLEN §5 schließen |
| Betablocker als Ursache von Sinusbradykardie und AV-Block; Bradyarrhythmien unter Medikament lassen sich durch Dosisreduktion oder Absetzen behandeln, „aber in vielen Fällen bleiben sie bestehen"; reversible Ursache vor einer Schrittmacherentscheidung ausschließen; DDD(R) erste Wahl bei Sinusknotenerkrankung, Zweikammer beim AV-Block | ESC-Pacing-2021 §3.3/Tab. 6, §5.1.1.1, §5.1.1.2, §5.2.1.4, §5.1.2, §5.2.2.1 | **geprüft** am OUP-Volltext. Vorbehalt: der Satz „in many cases bradyarrhythmias persist" (§5.1.1.2) steht im Abschnitt Brady-Tachy-Form (Medikamente zur Frequenz-/Rhythmuskontrolle), nicht allgemein zu Betablockern bei Hypertonie; das Pausieren stützt sich auf §5.1.1.1 (reversible Ursachen korrigieren) und §3.3/Tab. 6 (Betablocker), §5.1.1.2 nur sinngemäß. §5.4/Abb. 7 (3 s symptomatisch, 6 s asymptomatisch) gilt der Reflexsynkope und wird für den Epilog nur sinngemäß genannt |
| „Markiert" verlängert ist eine PQ-Zeit erst ab etwa 300 ms (Schrittmacher nur bei klarem Symptombezug) | ESC-Pacing-2021 §5.2.1.1 | **geprüft** („weak evidence to show that marked PR prolongation (i.e. ≥300 ms) … can lead to symptoms similar to pacemaker syndrome"; „In the absence of a clear correlation, a pacemaker is generally not indicated."); im Spiel nur als Begründung, warum 228 ms „nicht normal", aber nicht „deutlich verlängert" heißt |
| AV-Block unter bremsenden Medikamenten: nach Absetzen Rezidiv in 56 % binnen drei Wochen, nur 15 % echte medikamentöse Ursache (Zeltser 2004, n = 169); Deutung „drug-revealed" | Review PMC12246518 (2025), dort zitiert: Zeltser D et al., J Am Coll Cardiol 2004 | **neu, nur Hintergrund**, kommt nicht ins Spiel; stützt, dass die Pause im Epilog nach Auswaschen zum Schrittmacher führt |
| Bisoprolol-Halbwertszeit 10–12 h; nach rund 65 h (zweite Nacht) mehr als fünf Halbwertszeiten | Pharmakologie-Standardwissen (QUELLEN §9) | bestehend, Rechnung neu |
| Ramipril und ASS weitergeben | klinische Entscheidung des Oberarztes im Spiel; keine Leitlinienaussage | keine Behauptung; ärztliche Freigabe des Nutzers |
| Arrhythmie-Monitoring bei Synkope mit vermuteter kardialer Ursache mindestens 24 h bzw. bis zur Klärung (Klasse I, Level B); Alarmmanagement (Grenzen patientenbezogen anpassen) | AHA-2017 Praxisstandards ECG-Monitoring (Sandau KE et al., Circulation 2017;136:e273, doi:10.1161/CIR.0000000000000527) | **neu, zu prüfen**; Volltext am 18.10.2026 nicht abrufbar (403), Inhalt nur aus Sekundärquellen; vor dem Einbau der Alarmgrenze lesen (§9.2) |
| ISBAR (Identifikation, Situation, Hintergrund, Einschätzung, Empfehlung) als Übergabestandard | Kommunikationsstandard, keine medizinische Aussage; optional WHO Patient Safety Solutions 2007 („Communication During Patient Hand-Overs") | **neu, optional** |
| Verschwiegenheit: Was der Patient sagt, geht nicht ohne sein Einverständnis an Angehörige; Studierende sind gebunden | KAKuG §9 (RIS, **geprüft**: Verschwiegenheit für „die bei Trägern von Krankenanstalten und in Krankenanstalten beschäftigten Personen") plus Verschwiegenheitserklärung der Famulatur/des KPJ | Reichweite für Studierende regeln Landesgesetz und Erklärung, **zu prüfen**; keine medizinische Aussage; kein Paragraph im Spieltext |
| Pflege-Nachtdienst 19:00–07:00; Journaldienst; Morgenbesprechung dreiviertel acht; Triage nach Manchester, Synkope ohne Warnzeichen Gelb; Labor bei Synkope an der Triage | Hausüblichkeit | **beim Nutzer prüfen**, keine Quelle nötig |
| Echo bei Verdacht auf strukturelle Herzkrankheit (Falk: „Echo macht die Station morgen") | ESC-Synkope-2018 §4.2.3 | **neu, zu prüfen**; im Spiel nur Falks Anordnung, keine Indikationsaussage |
| Beweisend im Ruhe-/Monitor-EKG: Sinuspausen > 3 s im Wachen bzw. Mobitz II / AV-Block III° (Nr. 5, I C); die Karte sagt „Sinusstillstand oder Block, der Speicher sagt's" | ESC-Synkope-2018 §4.1.1 | **geprüft** (Postprint) |
| Bisoprolol-Halbwertszeit 10–12 h gilt bei normaler Nierenfunktion (etwa zur Hälfte renal eliminiert) | Pharmakologie-Standardwissen | nicht am Original geprüft; der Epilog sagt „praktisch nichts mehr da", nicht „nichts" |
| Rhythmusfrage: AV-junktionaler Ersatzrhythmus hat keine P vor dem QRS oder eine negative in II; AV-Block II° zeigt P ohne QRS | Lektion 11, 10 (FACHREGELN) | bestehend |
| Annotation LUDB 39: 6 P / 7 QRS, keine zweite P zwischen den Komplexen, PP ≈ RR | eigene Nachrechnung (Akte §2) | bestehend |

---

## 13. Offene Entscheidungen für den Nutzer

| Frage | Empfehlung |
|---|---|
| Marlene als Nachtdienst (seit 19:00, übergibt um 07:00, bleibt bis 07:35 wegen Herrn Baum) oder als Tagdienst ab 06:30? | **Nachtdienst.** Die Müdigkeit, die Übergabe, „red langsam mit mir" und die Frist geben dem Takt 1 seinen Widerstand. Dienstzeiten des Hauses (12-Stunden-Nacht) bestätigen. |
| Koje mit Liege statt Wartebank (neuer Render B1) | **Ja.** Ohne Liege bleibt der Fall unglaubwürdig; der Render ist ohnehin fällig (Wagen als eigene Ebene, Sonne als SVG, breiter Flurdurchgang). |
| Tochter als Figur nur am Telefon, ohne Porträt (Hörer-Symbol) | **Ja.** Sie ist die Zeugin und der Schlüssel zur Senta; ein Porträt bräuchte eine Figur, die nie im Raum ist. |
| Behandlungsentscheidung „Bisoprolol heute pausieren, Ramipril und ASS geben" als Spielerwahl mit Falk als Entscheider | **Ja**, mit ärztlicher Freigabe des Nutzers; die Belege tragen das Pausieren (ESC-Pacing-2021 §5.1.1.2), das Weitergeben der beiden anderen ist klinische Entscheidung ohne Leitlinienanspruch. Alternative: nur Bisoprolol als Frage, die anderen beiden nennt Falk. |
| Verdachtsliste mit acht Einträgen als HUD-Element (neue UI) | **Ja.** Sie ersetzt die Checkliste und macht das Lernziel sichtbar; acht Einträge passen auf ein iPad. |
| ISBAR mit Falks Umstellung (S → A → B → R) oder streng I-S-B-A-R | **Mit Umstellung.** So unterbrechen Oberärzte; die Karte stellt die Reihenfolge richtig und erklärt es. |
| Kapitel 2: Alarmgrenze „auf 45 gestellt" als Falk-Satz | **Weglassen**, bis AHA-2017 gelesen ist; die zweite Frage (§9.2) trägt den Punkt ohne Zahl. |
| Kapitel 2: technischer Alarm „Elektrode ab" an Bett 3 mit leerem Kurvenfeld | **Ja**, als Atmosphäre ohne Aufgabe; leeres Feld, keine gezeichnete Linie (ART_BIBLE §6 wird nicht berührt). |
| Rückmeldung zur Verschwiegenheit (KAKuG §9, Verschwiegenheitserklärung) im Spiel | **Ja**, in einem Satz ohne Paragraph im Spieltext; Reichweite für Studierende vom Nutzer bestätigen. |
| Spielfigur: KPJ-Studentin (ART_BIBLE §5, KONZEPT §2 „Famulatur/KPJ") statt Famulantin | **KPJ.** Nur ihr gibt ein Oberarzt unter Aufsicht die Tabletten-Frage und das Gespräch mit dem Patienten; eine Famulantin am ersten Tag wäre dabei unglaubwürdig. KONZEPT §2 und ART_BIBLE §5 entsprechend vereinheitlichen. |
| Herr Baum nennt die Spielerin „Frau Doktor", obwohl sie es nicht ist | **Beibehalten.** Patienten tun das; die Spielerin korrigiert es einmal (5.3), danach nicht mehr. |
| Posen von Herrn Baum und Marlene per GPT Image (Edit der bestehenden Figuren) oder neu in Blender | **GPT Image**, wie in STAND.md geplant (Prototyp „Marlene trinkt"); Blender nur für den Raum. |
| Ersatzaufnahmen (134, 78, 107) mit Textvarianten | **Später**, nach dem Umbau; die Platzhalter (`{hf}`, `{pq}`) bleiben dafür erhalten. |
| Katzensticker-Szene (warm, GAME_DESIGN §5) | **Behalten** als freiwillige Frage an Marlene vor 07:00; nach 07:00 hat sie keine Zeit, und das sagt sie. |
| Friedhof am Sonntag (verstorbene Frau Elfriede), ein Nebensatz beim Kleben | **Behalten**, genau ein Nebensatz; mehr wäre Rührung auf Bestellung. |
| Verletzung: Schürfung am Ellbogen und blauer Fleck an der Hüfte, bewusst keine Kopfverletzung | **So lassen.** Eine Beule am Kopf nach Bewusstlosigkeit würde die Frage nach einer Bildgebung aufwerfen, die der Fall nicht trägt und nicht belegt; die Hüfte erfüllt „Verletzung durch die Synkope" (Tab. 7) genauso. |

---

## 14. Handlung (Prüfung mit Skill `handlung`, 18.10.2026)

Urteil: Der Bogen trägt. Eine Frage („Darf er heim?"), eine Frist, ein Gegenspieler mit guten Gründen, eine
Wendung mit Saat (Friedhof in 5.4 vor der Enthüllung in 5.5), die Spielerin löst selbst, Schlussbild mit Echo
(Jacke, Mütze, Kanne). H1 und H2 aus §1 sind behoben. Offen, je ein Mittel:

- **H5 Scheinwahl** · §4.4, 5.3–5.5 „Reihenfolge frei", Runde endet erst, wenn alle fünf gefragt sind · Die
  einzige Wahl ist die Reihenfolge, und sie hat keine Folge; die Runden bleiben eine Checkliste mit fünf Knöpfen.
  · Mittel: je Runde nur der Kern als Engpass (Runde 1: Ereignis, Vorwarnung; Runde 3: „schon einmal?"), die
  übrigen Fragen dürfen ausgelassen werden („Das reicht mir fürs Erste"); was fehlt, fragt Falk in der ISBAR ab
  („Verletzt?") und schickt zum Patienten (bestehender Rückweg).
  → erledigt: §4.4 Kern und Rest je Runde, „Das reicht mir fürs Erste" in §5.3–5.5, Falk fragt Ausgelassenes in §6.2 B ab.
- **H3 Frist ohne Zähne** · §3 Takt 1 „Frist (Falk, 07:15)", §11.4 Falk erst nach `hat:ekg_geschrieben` · Vor dem
  EKG kostet nichts Zeit, also drückt die Frist nie. · Mittel: jede Frage und jede Handlung rückt die Uhr um eine
  Minute vor; um 07:15 kommt Falk in jedem Fall. Ist das EKG noch nicht geschrieben, wartet er am Tresen
  („Schreiben Sie. Ich les solang.") und die Übergabe beginnt danach mit weniger Zeit.
  → erledigt: §3 „Die Uhr hat Zähne", §6.1 Falk um 07:15 in jedem Fall mit Flag `falk_gewartet`, §11.3 Uhrregel.
- **H7 Fehlendes Sequel** · 5.6 Marlene „dreht sich um, als die Spielerin vorbeigeht" · Takt 3 (Reaktion,
  Dokumentation, „sag's dem Falk als Erstes") hängt an einem Weg, den man nicht gehen muss. · Mittel: fester Engpass
  nach der Untersuchung. Marlene schiebt den Wagen selbst an die Koje („Da. Ich übergeb.") und fragt dabei
  „Und? Darf er?".
  → erledigt: §5.6 „Marlene mit dem Wagen" als fester Engpass vor dem EKG, §10.3 um 07:02.
- **H5 doppelte Entscheidung** · 6.2 R „Er bleibt. Monitor. Und das Bisoprolol heute nicht." und 6.4 Tabletten ·
  Dieselbe Behandlungswahl fällt zweimal; die zweite ist dann keine Wahl mehr. · Mittel: R ohne Bisoprolol („Er
  bleibt. Monitor."); die Tabletten bleiben allein in 6.4.
  → erledigt: §6.2 R „Er bleibt. Monitor.", Tabletten nur in §6.4.
- **IF5 / atemlose Szene** · §6 Takt 6: ISBAR mit 3–4 Wahlen, Gegenrede mit bis zu acht Argumenten, Tabletten,
  Bett, in einem Stück · Zwölf Minuten Menü ohne Atempause; der Höhepunkt wird zur Abfrage. · Mittel: ein stummer
  Handlungstakt nach der A-Zeile. Falk legt seinen Messingzirkel an den Streifen und misst selbst nach („Zweihundertzwanzig,
  zweihundertdreißig. Ja."). Das gibt der Messung der Spielerin ihre Bestätigung von außen und setzt Falks Gegenstand
  ein (ART_BIBLE §5).
  → erledigt: §6.2 „Stummer Zirkel-Takt" nach der A-Zeile, Falk sagt {mess_pq}, Karte PQ ergänzt; §10.3 07:17.
- **Wendung überbewertet** · §2.3 „kippt die Notiz … in nicht mehr zu halten" · Fachlich kippt die Notiz erst
  mit dem EKG (keine Vorwarnung + nicht normal, §2.2); das zweite Ereignis stützt nur, und die Viertelstunde Stehen
  spricht sogar für Reflex. Erzählt man die Wendung als Kipppunkt, lernt die Spielerin „zweimal = gefährlich". ·
  Mittel: §2.3 und Falks Reaktion („Hm.") als Einsatzerhöhung formulieren (die Notiz kannte nur die halbe Geschichte);
  der fachliche Kipppunkt bleibt die PQ-Zeit in Takt 4.
  → erledigt: §2.2 Nr. 5, §2.3, §3 Takt 2 und 4, §5.5 Verdachtsliste, §6.2 `warum` („halbe Geschichte").
- **E5 Pointe am Schluss** · 7.1 Spielerin: „Deshalb der Monitor, nicht die Haltestelle." · Die Spielerin spricht
  die Lehre als Pointe aus. · Mittel: den Satz streichen; „Heute wissen wir's nicht." reicht, dann die Senta.
  → erledigt: §7.1, Spielerin ohne „nicht die Haltestelle".
- **Flag ohne Tabelle** · 5.7 `anruf_spaeter` · fehlt in der Flag-Tabelle §3. · Mittel: eintragen (Folge: Sabine
  ruft nach dem Streifen, „Ich hab dreimal angerufen.").
  → erledigt: §3 Flag-Tabelle (`anruf_spaeter`, dazu `falk_gewartet`), §5.8 Sabine.

Kein Befund zu H1, H2, H4, H6, H8 und zu Ende/Epilog (eine Folge, belegt, Verdachtsliste schließt mit
„Bewiesen.", kein Lebenslauf).

---

## 15. Prüfung Medizin, Realismus, Dialoge (18.10.2026)

Zweite Runde nach dem Gutachten (`pruefung_redesign.md`) und der Handlung-Prüfung (§14). Geändert:
- **Einstufung:** nirgends mehr „hoch"; überall „nicht niedrig → Beobachtung am Monitor" (§2.2, §6.3 `warum`,
  Verdachtsliste); Tab. 7 nur als Stütze; Tab. 6, Tab. 7, §4.1.2, §4.2.4.1, §4.2.2.1 am Postprint geprüft (§12).
- **Bradykardie-Falle entschärft:** Option bleibt, falsch ist die Folgerung („erklärt die Ohnmacht"); `warum` und
  Falks Echo ohne Normwert; Zirkel-Deutung zur Sinusbradykardie quellenoffen (§5.9).
- **Orthostase hat eine Quelle im Gespielten:** neue Pflichtfrage „Waren Sie grad erst aufgestanden?" (§5.3);
  Sabines „Kocher"-Satz angepasst.
- **Spielfigur KPJ-Studentin** (ART_BIBLE §5), Entscheidung in §13; Falk sagt dem Patienten den Grund selbst, Herr
  Baum will ihn von der Spielerin noch einmal hören (§6.5, §7.1); Revers nimmt der Arzt (`warum` §7.1); Koje 3 ohne
  Monitor (§5.2, §8.3 B1); Herz-Struktur nur „spricht dagegen", Echo morgen auf der Station (§4, §6.5); Epilog-Beleg
  auf ESC-Pacing §5.1.1.1/§5.2.1.4, Karte mit „Sinusstillstand oder Block, der Speicher sagt's" (§7.3).
- **Spielbarkeit:** Wagen nach dem Kern der Runde 1 frei; Marlene schiebt ihn an die Koje (fester Sequel); Uhr
  rückt mit jeder Handlung, Falk um 07:15 in jedem Fall, Knopf „Zum Tresen" im Stand (kein Softlock); Falk sagt
  nach Stützargumenten, was fehlt; R ohne Bisoprolol; stummer Zirkel-Takt Falks; Pointe am Schluss weg;
  `anruf_spaeter` und `falk_gewartet` in der Flag-Tabelle (§3, §5–§7, §14 „→ erledigt").
- **Dialoge:** alle Repliken höchstens zwei Sätze und 220 Zeichen, 0 Gedankenstriche; Falks Antithesen auf zwei
  reduziert; Herrn Baums Schlusspointen nach der Liste des Gutachtens ersetzt; Messwerte nur als Platzhalter
  ({hf}, {pq}, {mess_pq}); Journaldienst, Morgenbesprechung, Bus alle halbe Stunde, Transport mit Monitor und
  Pflege, „bevor meine Gruppe kommt", Elfriede einmal, ein „gell", Verschwiegenheit nach KAKuG §9.
Offen (siehe §12/§13): Echo-Indikation (ESC §4.2.3), AHA-2017 (Alarmgrenzen, 24 h), Reichweite der
Verschwiegenheit für KPJ-Studierende, Bisoprolol-Halbwertszeit bei normaler Nierenfunktion, Hausüblichkeiten in
Graz (Dienstzeiten, Triagefarbe, Morgenbesprechung), ärztliche Freigabe der Tabletten-Entscheidung.
