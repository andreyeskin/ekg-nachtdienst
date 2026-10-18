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

### 2.2 Warum diese Kette fachlich hält (Prüfung der Argumentation)

ESC-Synkope-2018, Tabelle 6 (geprüft 18.10.2026 an der adaptierten Wiedergabe, Original-PDF bleibt nachzulesen,
QUELLEN §5), in eigenen Worten:

1. **Niedriges Risiko** verlangt *alle* diese Dinge: eine Vorwarnung, wie sie zur Reflexsynkope gehört (oder einen
   typischen Auslöser), keine Herzkrankheit, unauffällige Untersuchung und **ein normales EKG**. Herr Baum hat weder
   Vorwarnung noch normales EKG. Er ist also nicht niedrig.
2. **Minor-Risikomerkmal** „keine Vorwarnung oder Prodrom < 10 s" zählt als hohes Risiko, **wenn** eine strukturelle
   Herzkrankheit **oder ein auffälliges EKG** dazukommt (Fußnote der Tabelle: minor Ereignis-Merkmale nur mit
   struktureller Herzkrankheit und/oder abnormem EKG). Ein AV-Block I° (PQ 228 > 200 ms) ist ein auffälliges EKG, auch
   wenn die PQ-Zeit nicht „deutlich" verlängert ist.
3. **Die Minor-EKG-Zeile** „AV-Block I° mit deutlich verlängerter PQ-Zeit" brauchen wir für die Kette **nicht**;
   228 ms zählen wir weiterhin nicht als eigenes Risikomerkmal (wie die Akte §4 heute). Das Spiel sagt nur: „nicht
   normal", nie „deutlich verlängert". ESC-Pacing-2021 §5.2.1.1 nennt als „markiert" erst ≥ 300 ms; das stützt
   die Zurückhaltung (QUELLEN §12, neu).
4. **Tabelle 7** nennt „Synkope ohne Prodrom" unter den Hochrisiko-Merkmalen, die für eine Beobachtung in einer
   Überwachungseinheit der Notaufnahme oder einer Synkopeneinheit sprechen, und „Verletzung durch die Synkope" unter
   denen, die für eine Aufnahme sprechen (Online-Volltext 18.10.2026; Spaltenzuordnung am PDF bestätigen, §12).
5. **§4.2.4.1:** Bei Hochrisiko-Merkmalen, die eine arrhythmische Synkope nahelegen, ist eine Überwachung im Haus
   (Bett oder Telemetrie) gerechtfertigt, vor allem unmittelbar nach der Synkope (Ausbeute 1,9–17,6 %).
6. **Was nicht gilt:** Zwei Ereignisse in 48 Stunden sind in Tabelle 6 kein eigenes Merkmal. Sie sind das Gegenteil
   des Low-risk-Merkmals „lange Vorgeschichte gleichartiger harmloser Ohnmachten", und Tabelle 5 nennt die lange
   Vorgeschichte (vor allem vor dem 40. Lebensjahr) als Reflex-Merkmal. Im Spiel steht deshalb: „Mit achtundsechzig
   fängt man nicht mit Kreislaufgeschichten an" (Falk), nie „zweimal = Hochrisiko". Alter ist in Tabelle 6 kein
   Merkmal; das Spiel benutzt es nur über die Vorgeschichte.
7. **Betablocker:** Er erklärt 53/min und eine zähe Überleitung (Pharmakologie, QUELLEN §3; ESC-Pacing-2021
   §3.3/Tab. 6: Betablocker als Ursache von Sinusbradykardie und AV-Block). Er erklärt keine Ohnmacht ohne
   Vorwarnung. Ob er eine kranke Leitung nur „demaskiert", weiß am Montag niemand; ESC-Pacing-2021 §5.1.1.2 sagt
   dazu nur: Bradyarrhythmien unter Medikament lassen sich durch Dosisreduktion oder Absetzen behandeln, „aber in
   vielen Fällen bleiben sie bestehen". Das genügt für die Entscheidung „heute pausieren, Monitor zeigt den Rest"
   (§7). Die Zahl aus Zeltser 2004 (56 % Rezidiv nach Absetzen) kommt nicht ins Spiel (§12, neu, nur als Hintergrund).

Die Kette ist also: *keine Vorwarnung* + *EKG nicht normal* → nicht niedrig, sondern hoch → Beobachtung am Monitor.
Alles andere (zweimal, Verletzung, 68, Betablocker) stützt, trägt aber nicht allein. Genau so argumentiert die
Spielerin bei Falk (§6), und genau so steht es in den Rückmeldungen.

### 2.3 Die dramatische Frage

**„Darf Herr Baum heim?"** Sie steht vom ersten Bild an im Raum: Herr Baum hat die Jacke schon an. Marlene sagt
im zweiten Satz, dass Falk um viertel nach sieben genau das fragen wird. Die Tochter fragt es am Telefon. Falk
fragt es, weil er die Koje braucht, und hat schon eine Antwort (Kreislauf, heim). Alles, was die Spielerin tut,
verschiebt die Antwort. Am Ende sagt **sie** es Herrn Baum, in seiner Sprache, und löst seine eigentliche Sorge.

Die Wendung: Um sieben Uhr, mitten in der Anamnese, sagt Herr Baum, was er niemandem gesagt hat. Es war nicht das
erste Mal. Damit kippt die Notiz des Nachtdienstes („vasovagal") von „plausibel" in „nicht mehr zu halten", und
die Spielerin ist die Einzige, die es weiß.

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

Dienst 1, Montag. Spielzeit 06:40 bis 07:40 (eine Stunde Spielzeit, 15–20 Minuten echte Zeit). Ein Raum.
Figuren: Schwester Marlene (Nachtdienst seit 19:00), Herr Baum, Dr. Falk (Tagdienst, ab 07:15), Sabine Baum
(Tochter, nur am Telefon), Erzähler. Off-screen: Dr. Steiner (Nachtdienst-Ärztin, seit 06:30 im Schockraum),
Andrea (Tagdienst-Pflege, ab 07:00 am Tresen), Frau Kainz (Nachbarin), die Hündin Senta.

Dramatische Frage und Lernziel sind derselbe Satz: *Darf er heim?* (§2). Jeder Takt verschiebt die Antwort.

| Takt | Art | Zeit | Ziel der Spielerin | Widerstand / Konflikt | Wendung (Szene) bzw. Reaktion → Dilemma → Entscheidung (Sequel) |
|---|---|---|---|---|---|
| **1 Haken** | Szene | 06:40–06:44 | ankommen, wissen, was zu tun ist | Marlene ist seit zwölf Stunden da und hat keine Hand frei; Herr Baum steht mit Jacke; die Notiz des Nachtdienstes hat schon eine Antwort („vasovagal") | **„Ja, aber":** Sie bekommt den Fall, aber mit Frist (Falk, 07:15, will die Koje) und mit einer fertigen Antwort, die sie prüfen muss, nicht übernehmen |
| **2 Gespräch** | Szene | 06:45–07:00 | das Ereignis verstehen, ihn zum Sitzen bringen | er will heim (Senta um acht), spielt es herunter, die Zeugin ist nicht da | **„Nein, und außerdem":** Es war nicht das erste Mal. Gestern, Haltestelle beim Friedhof. Und: „Sagen S' es der Sabine nicht." |
| **3 Ordnen** | Sequel | 07:00–07:02 | — | — | **Reaktion:** Marlene: „Das hat er mir nicht gesagt." Verdachtsliste ordnet sich um (Reflex schwächer, Rhythmus stärker, TIA/Krampf/Zucker gestrichen). **Dilemma:** Dem Oberarzt sagen, der Tochter nicht? **Entscheidung:** Was sie ihm verspricht (Flag `versprochen`), wird in Takt 5 und 7 erinnert |
| **4 Befund** | Szene | 07:02–07:10 | das EKG schreiben, Rhythmus, Frequenz, PQ | Schichtwechsel, niemand hilft; der Wagen muss zur Koje; beim Kleben leuchtet das Handy: die Tochter; er kann sich nicht rühren | **„Ja, aber":** Die Zahlen sind klar (Sinus, 53, PQ 228). Ihre Bedeutung nicht: nicht normal, aber kein Beweis. Und die Tochter: kein Zucken, „die Tabletten liegen noch am Tisch" |
| **5 Bedeutung** | Sequel | 07:10–07:14 | — | — | **Reaktion:** Karten, Vergleich PQ ↔ Medikamente, Verdachtsliste: „Herzrhythmus: nicht bewiesen, nicht ausgeschlossen". **Dilemma:** Was sage ich Falk zuerst, und was empfehle ich? **Entscheidung:** die ISBAR-Zeilen werden gewählt (Takt 6 beginnt mit dieser Wahl) |
| **6 Höhepunkt** | Szene | 07:15–07:28 | Falk überzeugen, dass er bleibt (oder: sich überzeugen lassen) | Falk hat zwölf Minuten, eine fertige Meinung (Kreislauf) und braucht die Koje; er unterbricht; jede schwache Begründung wird zerlegt | **„Ja, aber":** Er bleibt. Aber jetzt muss *sie* es ihm sagen, und die Tabletten-Frage ist ihre |
| **7 Ausklang** | Sequel + kurze Szene | 07:30–07:40 | dass er bleibt, freiwillig | er bietet an, „alles zu unterschreiben"; die Senta | **Entscheidung der Spielerin, in Laiensprache**, und die Senta gelöst (Frau Kainz). Schlussbild: Jacke über dem Sessel, Mütze bleibt auf, Marlenes Stuhl leer, die Kanne weg. Epilog in Dienst 3 |

**Branch-and-Bottleneck.** Verzweigt wird innerhalb der Takte (Reihenfolge der Fragen, Irrwege, Ton gegenüber
Herrn Baum und der Tochter, Reihenfolge der Argumente). Engpässe, an denen alle Wege zusammenlaufen:

1. Ereignis von heute geklärt (Ende Runde 1 der Anamnese).
2. Zweites Ereignis bekannt (Ende Runde 3; die Frage „schon einmal passiert?" ist Teil der Runde, nicht versteckt).
3. EKG gemessen: Rhythmus, Frequenz, PQ (QRS optional).
4. Übergabe abgeschlossen (vier ISBAR-Zeilen).
5. Falks Entscheidung: Monitor (jeder Argumentationsweg endet hier; der Weg „heim" wird widerlegt, nicht bestraft).
6. Herr Baum bleibt (jeder Weg des Schlussgesprächs endet hier; der Irrweg kostet eine Runde und einen Satz).

**Flags mit sichtbarer Folge** (mehr nicht; `web/motor/fall.js`):

| Flag | gesetzt wenn | Folge, die man sieht |
|---|---|---|
| `versprochen` | die Spielerin sagt „Das bleibt unter uns" | Falk: „Steht nicht am Bogen." Spielerin muss es trotzdem sagen; Herr Baum im Schlussgespräch: „Sie haben's ihm gesagt." / „Dem Arzt. Nicht der Sabine." |
| `tochter_beruhigt` | am Telefon „vermutlich nur der Kreislauf" | Tochter am Ende des Anrufs erleichtert; Epilog-Karte erinnert: „Der Tochter hattest du Kreislauf gesagt." |
| `tochter_verraten` | am Telefon das zweite Ereignis erzählt | Herr Baum im Schlussgespräch: „Sie hat's gewusst, wie sie angerufen hat. Von Ihnen." Kein Game Over, aber ein kühlerer Schluss |
| `heim_empfohlen` | ISBAR-Zeile R „kann heim" | Falks Gegenrede läuft in umgekehrter Rolle (§6.3); Karte Übergabe trägt beide Sätze |
| `brady_argument` | „53 ist eine Bradykardie" als Argument | Falk erinnert es bei der Tabletten-Frage: „Vorhin war 53 eine Bradykardie. Jetzt sind es zwei Etagen, die der Betablocker bremst. Entscheiden Sie sich." |
| `revers` | „Dann unterschreiben Sie einen Revers" | Marlene beim Abschied: „Revers hat er ihr angeboten. Hat's nicht gebraucht." |
| `senta_geloest` | Frau Kainz genannt | Epilog: „Die Senta hat die Frau Kainz bis zum Parkplatz gebracht." |

Warum sich das wie *eine* Geschichte anfühlt: eine Frage (heim?), eine Frist (07:15), ein Gegenspieler mit guten
Argumenten (Falk), eine Wendung, die aus dem Gespielten folgt (die Frage „schon einmal?" steht im Fragenkatalog
jeder Synkopen-Anamnese), ein Geheimnis mit Preis (die Tochter) und ein Ende, das die Spielerin selbst spricht.
Kein Hub, kein „Zurück", keine Mahnliste; was fehlt, sagt eine Figur in einem Satz.

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
| „Beim Wasserkocher, eine Minute gestanden" | Kreislauf im Stehen | spricht dagegen | nicht beim Aufstehen, kurz gestanden | Tab. 5 (OH: beim/nach dem Aufstehen) |
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
| Untersuchung: Herztöne regelmäßig, kein Geräusch | Herz-Struktur | unwahrscheinlich | kein Geräusch, keine Beschwerden; eine Ableitung sieht wenig | Tab. 6 (Major: unklares Systolikum); FACHREGELN (Grenzen einer Ableitung) |
| Untersuchung: Neurologie unauffällig | Schlaganfall / TIA | unwahrscheinlich | Bewusstsein weg, Ausfälle keine | Tab. 4, §8.1.3; Web Table 5.4 |
| Tochter: kein Zucken, Augen offen, dagelegen | Krampfanfall | unwahrscheinlich | keine Zuckungen, sofort klar, keine Zunge | §8.1.2, Tab. 10; Web Table 5.3–5.5 |
| Tochter: Augen offen | (Psychogen, Rückmeldung) | — | | §7.1.2 |
| EKG: Sinus, 53/min | Herzrhythmus | (Grund: „53 unter Betablocker: erwartbar, nicht verdächtig") | | Lektion 8; Tab. 5 („ohne negativ chronotrope Medikation") |
| EKG: PQ 228 | Herzrhythmus | **spricht dafür**, Grund „EKG nicht normal: AV-Block I°; kein Beweis" | | Lektion 3, 10; Tab. 6 (Low-risk verlangt normales EKG) |
| EKG: QRS 86 | Herzrhythmus | (Grund: „schmal: die Bremse sitzt oben") | | Lektion 4, 10 |
| Falks Entscheidung | Herzrhythmus | **nicht bewiesen, nicht ausgeschlossen** | Beweis wäre: Pause > 3 s im Wachen, Mobitz II, III°, Sinus < 40. Dafür der Monitor | §4.1.1, §4.2.4.1 |
| Falks Entscheidung | Reflex | unwahrscheinlich | keine Vorwarnung, erstes Mal mit 68, EKG nicht normal: nicht niedrig | Tab. 6 |

### 4.3 Endzustand (so sieht die Liste um 07:30 aus)

- ~~Reflex~~ unwahrscheinlich: keine Vorwarnung, erstes Mal mit 68, EKG nicht normal
- ~~Kreislauf im Stehen~~ unwahrscheinlich: Stehversuch ohne Abfall, nicht beim Aufstehen, keine neue Tablette
- **Herzrhythmus: nicht bewiesen, nicht ausgeschlossen.** Ohne Vorwarnung, zweimal, EKG nicht normal (PQ 228). Beweis bräuchte eine Pause > 3 s im Wachen, Mobitz II, III° oder Sinus < 40. Dafür der Monitor.
- ~~Herz-Struktur~~ unwahrscheinlich: nicht unter Belastung, kein Geräusch
- ~~Krampfanfall~~ unwahrscheinlich: kein Zucken, sofort klar
- ~~Schlaganfall / TIA~~ unwahrscheinlich: Bewusstsein weg, Ausfälle keine
- ~~Unterzucker~~ unwahrscheinlich: kein Diabetes, Stix 104
- ~~Sturz ohne Bewusstlosigkeit~~ unwahrscheinlich: weg, umgesunken, keine Erinnerung

Die Liste ist zugleich die Karte „Verdacht" in der Mappe (ein Eintrag je Zustandswechsel, mit Uhrzeit). Im
Epilog bekommt „Herzrhythmus" den letzten Eintrag: „Dienst 3: Pause über drei Sekunden im Wachen, ohne
Betablocker. Bewiesen."

### 4.4 Warum keine Pflichtfragen-Mahnung mehr nötig ist

Die Engpässe (§3) ersetzen die Checkliste: Runde 1 endet erst, wenn Ereignis, Vorwarnung, Dauer, Erholung und
Verletzung gefragt sind; Herr Baum schließt die Runde selbst („Mehr weiß ich nicht. Fragen S' die Sabine."). Runde
2 (Tabletten, Krankheiten, Zucker, Alkohol) und Runde 3 (schon einmal, Familie) ebenso. Was die Spielerin in
einer Runde zuerst fragt, ist frei; die Liste zeigt pro Runde höchstens fünf Fragen, keine Hubs, kein Zurück.
Optionale Fragen (Foto, Senta, „Sie haben sich beim Kleben…") stehen dazwischen und zählen nicht.

---

## 5. Die Dialoge

Konventionen: Repliken höchstens zwei Sätze, höchstens 220 Zeichen, kein Gedankenstrich; Spieleroptionen eine
Zeile (≤ 64 Zeichen). Rückmeldungen (`warum`) erscheinen nach einer Wahl als Streifen unter dem Dialog, nie im
Figurenmund; der Beleg steht in Klammern nur hier, nie im Spiel. Austriazismen bei Marlene und Herrn Baum sparsam
und konsequent: *Sackerl, Zuckerl, gell, halt, eh, Sessel, dreiviertel acht, Entschuldigen S'*. Herr Baum sagt
„Frau Doktor", obwohl er weiß, dass sie es nicht ist; Marlene duzt; Falk siezt und nennt niemanden beim Vornamen.

Stimmprofile (Skill `dialoge` §4), ergänzt um die Tochter (neu, in den Skill zu übernehmen):

| Figur | Satzbau | Wörter | Nie | Tic |
|---|---|---|---|---|
| **Sabine Baum, 44** (Tochter, Kindergartenpädagogin, am Telefon) | schnell, halbe Sätze, organisiert beim Reden („Ich kann erst um zwölf") | „Papa", Uhrzeiten, Namen von Nachbarn | Fachwörter, Vorwürfe an den Vater vor Fremden | hört nebenbei Kinder kommen; fragt zweimal, ob er bleibt |

### 5.1 Auftakt (06:40, Erzähler, Raum sichtbar, keine Figur spricht)

> **Erzähler:** 06:40. Dein erster Tag auf der Notaufnahme, zwanzig Minuten zu früh, weil du den Weg nicht kanntest. Die Nachtschicht räumt auf.
>
> **Erzähler:** Hinter dem Tresen Schwester Marlene am Telefon. In der Koje rechts ein Mann mit Schiebermütze, der die Jacke schon anhat und ein Sackerl in der Hand hält.
>
> *Knopf:* Zum Tresen.

Bewegung dazu (§10): Marlene legt auf, als die Spielerin den Tresen anklickt; Herr Baum schaut zur Uhr.

### 5.2 Marlene am Tresen (06:42, Szenenbild; sie reicht den Bogen)

Ziel: Die Spielerin weiß, wer, was, bis wann, und hat den Anker in der Hand. Marlene will übergeben und heim; sie
gibt den Patienten ab, ohne ihn fallen zu lassen.

> **Marlene:** Du bist die Famulantin? Grüß dich. Marlene. Ich bin seit gestern sieben da, also red langsam mit mir.
>
> *Spielerin:* 1 Was ist mit dem Herrn in der Koje? · 2 Wo ist der Arzt? · 3 Was soll ich machen?
>
> **Marlene** (1): Herr Baum, achtundsechzig. Heut in der Früh in der Küche umgefallen, die Tochter hat ihn gebracht. Ihm fehlt nix, sagt er. Er will heim, der Hund muss raus.
>
> **Marlene** (2): Die Steiner ist seit halb sieben im Schockraum, die Rettung hat eine Reanimation gebracht. Vorher hat sie ihn kurz gesehen und das da hingeschrieben. *(reicht den Bogen; Karte „Aufnahmebogen")*
>
> **Marlene** (3): Red mit ihm. Schau ihn an. Und schreib das EKG, ich komm nicht dazu. Um sieben kommt die Andrea, und ich geb ihr acht Leute über.
>
> *(nach allen dreien, oder wenn die Spielerin „Ich geh zu ihm" wählt)*
>
> **Marlene:** Und der Falk kommt um viertel nach sieben runter. Der fragt dich, ob der Mann heimdarf. Nicht mich. Also schau, dass du's weißt.
>
> **Marlene:** Stehversuch und Zucker hab ich gemacht, steht alles drauf. So.
>
> *Spielerin:* Danke. Ich geh zu ihm.

*Karte „Aufnahmebogen":* Triage 06:20. Puls {puls}/min, regelmäßig. Blutdruck liegend {rr_l_sys}/{rr_l_dia}, nach
1 min Stehen {rr_s1_sys}/{rr_s1_dia}, nach 3 min {rr_s3_sys}/{rr_s3_dia}, ohne Schwindel. SpO₂ {spo2} %, {temp} °C,
Blutzucker {zucker} mg/dl. Schürfung linker Ellbogen, blauer Fleck linke Hüfte. **Notiz Dr. Steiner 06:25: V. a.
vasovagale Synkope, Schellong unauffällig, EKG ausständig.** → Verdachtsliste: Reflex „spricht dafür (Notiz)",
Kreislauf im Stehen „spricht dagegen (Stehversuch)", Unterzucker „spricht dagegen (104)".

*Prüfung:* D1: Marlene hat Hauptsätze, Imperative, „So.", Zahlen in Stationsdeutsch; ohne Namen erkennbar. D2: laut
lesbar, Abbrüche („Ihm fehlt nix, sagt er."). D3: kein Erklärdump; die Notiz ist ein Zettel, keine Lehre. D4: Müdigkeit
im „red langsam mit mir" und „acht Leute über", nicht benannt. D5: jeder Wechsel bringt dem Fall etwas (Patient, Notiz,
Auftrag), zeigt die Figur (delegiert, prüft), hat Subtext („Ich geb dir den Mann, nicht die Antwort") und verschiebt die
Beziehung (sie traut es ihr zu). D6: ruhig, aber knapp, weil müde. Humanizer: kein Gedankenstrich, keine Dreierreihe
aus Adjektiven (die drei Imperative sind eine Arbeitsliste, so spricht sie), kein Aphorismus am Schluss.

### 5.3 Herr Baum, Runde 1: das Ereignis (06:45, in der Koje; er steht)

Ziel: Die vier T-LOC-Merkmale und die Umstände, ohne dass es ein Verhör ist. Herr Baum will heim und sagt es durch
die Jacke; er spielt herunter und entschuldigt sich.

> **Herr Baum:** Ah. Frau Doktor. Entschuldigen S', ich wollt grad. Die Schwester hat gesagt, ich soll warten. Aber die Senta muss um acht raus, und mir fehlt nix.
>
> *Spielerin:* 1 Famulantin, noch keine Ärztin. Setzen Sie sich, erzählen Sie. · 2 Wer ist die Senta? · 3 Ich schau zuerst auf den Bogen.
>
> **Herr Baum** (2): Die Senta. Unser Hund. Also der Hund von der Sabine, aber ausführen tu ich. Neun Jahre, Dackel mit was drin. Die wartet jetzt an der Tür.
>
> **Herr Baum** (3): Bitte, bitte. Ich hab Zeit. Also, keine Zeit, aber bitte. *(Karte „Aufnahmebogen", falls noch nicht)*
>
> **Herr Baum** (1, setzt sich auf die Liegenkante, Jacke bleibt an): In der Küche. Ich hab den Wasserkocher angestellt wie immer. Und dann lieg ich am Boden, und die Sabine schreit. Dazwischen nix. Wie wenn einer das Licht ausdreht.
>
> *Spielerin (Runde 1, Reihenfolge frei):* 1 Haben Sie vorher etwas gespürt? Übel, heiß, Schwitzen? · 2 Wie lange waren Sie weg? · 3 Und danach, gleich wieder klar? · 4 Woher ist die Schramme? · 5 Hat Ihre Tochter gesehen, ob Sie gezuckt haben?
>
> **Herr Baum** (1): Nix. Gar nix. Ich hab grad an die Senta gedacht, dass sie dann raus muss. Und dann war der Boden da.
>
> **Herr Baum** (2): Die Sabine sagt, eine halbe Minute. Sie hat den Krach gehört und ist gleich gekommen. Mir ist's wie gar nix vorgekommen.
>
> **Herr Baum** (3): Gleich. Ich hab gesagt, Sabine, mach keinen Zirkus. Sie hat trotzdem einen gemacht. Und jetzt sitz ich da.
>
> **Herr Baum** (4): Vom Tisch wahrscheinlich. Oder vom Sessel. Ich weiß es nicht, ich war ja nicht dabei, sozusagen.
>
> **Herr Baum** (5): Das fragen S' sie am besten selber, sie ruft eh an. Ich hab nix gemerkt. Gezuckt hab ich im Leben noch nie.
>
> *(wenn alle fünf gefragt sind)*
>
> **Herr Baum:** Mehr weiß ich nicht. Ich war halt weg. Fragen S' die Sabine, die hat alles gesehen, und seitdem redet sie nix anderes.

*Verdachtsliste nach Runde 1:* Sturz ohne Bewusstlosigkeit → unwahrscheinlich (weg, umgesunken, keine
Erinnerung; §4.1 der Leitlinie). Reflex → spricht dagegen (keine Vorwarnung; Tab. 5/6). Herzrhythmus → spricht
dafür (ohne Vorwarnung; Tab. 6 Minor). Kreislauf im Stehen → spricht dagegen (nicht beim Aufstehen; Tab. 5).
Krampfanfall → spricht dagegen (sofort klar; Tab. 10). Die Verletzung geht auf die Karte „Anamnese" (Tab. 7).

*Rückmeldung zu (3) „Ich schau zuerst auf den Bogen" (kein Irrweg, aber ein Hinweis):* Lesen ist richtig. Der
Bogen hat schon eine Antwort drauf. Lies sie als Frage, nicht als Befund. *(keine fachliche Aussage)*

*Prüfung:* D1: Laiensprache, Abschweifen (Senta, Sabine), Entschuldigung, Selbstironie („ich war ja nicht dabei,
sozusagen"); kein Fachwort. D2: Abbrüche („ich wollt grad."), Rhythmus wechselt. D3: Wissen kommt aus seinen
Antworten, nicht aus Vortrag. D4: Scham und Ungeduld in der Jacke, im „mir fehlt nix", im Hund; nie benannt. D5: jede
Antwort bewegt einen Eintrag der Liste und zeigt den Mann. D6: ruhig, längere Repliken erlaubt, alle unter 220.
Humanizer: keine Gedankenstriche, keine Schlusspointe außer dem, was ein 68-Jähriger wirklich sagt.

### 5.4 Runde 2: die Person und die Tabletten (06:52)

> **Herr Baum:** Fragen S' nur. Sie haben mehr Fragen als die Sabine, und die hat viele.
>
> *Spielerin (Runde 2, Reihenfolge frei):* 1 Welche Tabletten nehmen Sie? · 2 Haben Sie Zucker? Andere Krankheiten? · 3 Herzrasen, Stolpern, Druck in der Brust, Luftnot? · 4 Konnten Sie danach reden, sehen, die Arme heben? · 5 Alkohol? Schlaftabletten?
>
> **Herr Baum** (1): Drei in der Früh. Die Sabine hat den Zettel vom Hausarzt eingepackt, da im Sackerl. Die Farben kenn ich, die Namen nicht. *(reicht den Plan; Karte „Medikamente")*
>
> *Spielerin (statt 1 erscheinen):* 1a Haben Sie die heute schon genommen? · 1b Ist in letzter Zeit etwas geändert worden?
>
> **Herr Baum** (1a): Heut, nein. Heut war ja die Küche zuerst. Die liegen noch am Tisch, neben dem Kaffee, den ich auch nicht gehabt hab.
>
> **Herr Baum** (1b): Nein. Seit Jahren das Gleiche. Der Doktor Reiter sagt, so lang's passt, bleibt's.
>
> **Herr Baum** (2): Zucker nein. Den Blutdruck halt, seit zehn Jahren. Das Knie, operiert. Und das Hörgerät, aber das ist keine Krankheit, das ist das Alter.
>
> **Herr Baum** (3): Nie. Mein Herz hab ich noch nie gespürt. Beim Bergaufgehen mit der Senta werd ich halt langsamer, aber die auch.
>
> **Herr Baum** (4): Alles. Ich hab der Sabine gesagt, sie soll den Wasserkocher abdrehen, der pfeift. Also gehört hab ich, und gesehen auch.
>
> **Herr Baum** (5): Ein Bier am Sonntag, nach dem Friedhof. Schlafen tu ich wie ein Stein, ohne was.
>
> *(wenn alle gefragt sind)*
>
> **Herr Baum:** Sonst bin ich gesund. Für mein Alter, sagt der Reiter. Der ist auch nicht jünger.

*Karte „Medikamente (Medikationsplan)":* {medi1}, {medi2}, {medi3}, 1-0-0, seit Jahren unverändert; **heute
noch nicht genommen** (zuletzt gestern früh). Der Betablocker bremst Sinusknoten und AV-Knoten: Er erklärt eine
langsame Frequenz und eine zähe Überleitung, aber keine Bewusstlosigkeit ohne Vorwarnung. *(Pharmakologie, QUELLEN
§3; ESC-Pacing-2021 §3.3/Tab. 6)*

*Verdachtsliste:* Kreislauf im Stehen → spricht dagegen (keine neue Tablette; Tab. 5). Unterzucker →
unwahrscheinlich (kein Diabetes, Stix 104; Tab. 4). Herz-Struktur → spricht dagegen (nicht unter Belastung, keine
Beschwerden; Tab. 5/6). Schlaganfall/TIA → spricht dagegen (reden, sehen, bewegen sofort; Tab. 4). Rückmeldung zu
(5), still: Alkohol und Schlafmittel gehören zu den Nicht-Synkopen, die man abfragt; hier beides nein (Tab. 4).

*Bemerkung „Der Doktor Reiter":* Der Hausarzt hat einen Namen, weil Patienten ihre Hausärzte beim Namen nennen; er
kommt sonst nicht vor und braucht kein Porträt.

*Prüfung:* D1: derselbe Mann (Sackerl, Reiter, Senta). D3: der Medikationsplan ist Alltag, kein Fund (KONZEPT §1.3).
D5: „Heut, nein" bringt dem Fall die Tabletten-Frage von Takt 6 und zeigt, wie der Morgen war. Humanizer: ok.

### 5.5 Runde 3: die Vorgeschichte, die Wendung (06:57)

Ziel: Die Pflichtfrage „schon einmal passiert?" fördert das zweite Ereignis zutage. Herr Baum will, dass es nicht
„was" wird; die Spielerin muss entscheiden, was sie verspricht.

> *Spielerin (Runde 3):* 1 Ist in Ihrer Familie jemand jung und plötzlich gestorben? · 2 Ist das schon einmal passiert?
>
> **Herr Baum** (1): Der Vater mit achtzig, Schlaganfall. Die Mutter einundneunzig. Jung, nein. Bei uns stirbt man alt, wenn's geht.
>
> **Herr Baum** (2, schaut auf das Sackerl, Pause): Frau Doktor. Sagen S' es der Sabine nicht.
>
> *Spielerin:* 1 Was soll ich ihr nicht sagen? · 2 Das bleibt unter uns. · 3 Dem Arzt sag ich alles. Der Tochter nur, wenn Sie wollen.
>
> **Herr Baum** (nach 1, 2 oder 3): Gestern. An der Haltestelle beim Friedhof. Der Bus ist nicht gekommen, und ich auf einmal auch nicht mehr. Eine Frau hat mir aufgeholfen und ein Zuckerl gegeben.
>
> **Herr Baum:** Ich hab gesagt, der Kreislauf. Und bin heimgefahren wie nix. Die Sabine hat genug mit der Lena und dem Kindergarten. Bitte.
>
> *(nach 1 erscheinen 2 und 3 noch einmal)*
>
> **Herr Baum** (nach 2, Flag `versprochen`): Danke. Sie sind eine Gute.
>
> **Herr Baum** (nach 3): Der Arzt ist der Arzt. Aber die Sabine, die macht sonst noch mehr Zirkus. Und die Lena kriegt's mit.
>
> *Spielerin (Nachfragen, erscheinen nach der Erzählung):* 1 Gestern vorher etwas gespürt? · 2 Wie lange sind Sie dort gestanden? · 3 Haben Sie sich gestern verletzt?
>
> **Herr Baum** (1): Auch nix. Gestanden, auf den Bus geschaut. Und dann die Frau mit dem Zuckerl. Vor der Kirche, alle haben geschaut.
>
> **Herr Baum** (2): Eine Viertelstunde sicher. Sonntag fährt er nur jede Stunde, und ich war zu früh, wie immer.
>
> **Herr Baum** (3): Nein. Die Frau hat gesagt, ich bin umgesunken wie ein nasser Sack, langsam. Der Ellbogen, das ist von heut.
>
> *(wenn alles gefragt ist)*
>
> **Herr Baum:** So. Jetzt wissen Sie's. Und ich darf trotzdem heim, gell?
>
> *Spielerin:* Erst schau ich Sie an. Dann das EKG.

*Rückmeldung zu „Das bleibt unter uns" (`warum`):* Versprich nur, was du halten kannst. Was er dir sagt, gehört in
die Akte und zum Oberarzt, sonst entscheidet der mit der halben Geschichte. Die Tochter erfährt es nur von ihm oder
mit seinem Einverständnis. Das sagst du ihm besser jetzt als später. *(keine fachliche Aussage; Verschwiegenheit
gegenüber Dritten: ÄrzteG 1998 §54, gilt sinngemäß für Studierende im Rahmen der Famulatur; §12, neu, zu prüfen)*

*Rückmeldung zu „Dem Arzt sag ich alles. Der Tochter nur, wenn Sie wollen":* Richtig: Die Akte ist nicht die
Familie. Er entscheidet, was die Tochter erfährt; du entscheidest nicht, was der Oberarzt erfährt. *(wie oben)*

*Verdachtsliste:* Herzrhythmus → spricht dafür, Grund „zweimal in zwei Tagen, beide ohne Vorwarnung, das erste Mal
mit 68" (Tab. 5: lange Vorgeschichte vor 40 als Reflex-Merkmal; Tab. 6 Low-risk: lange gleichartige Vorgeschichte).
Reflex → Grund ergänzt: „eine Viertelstunde Stehen spräche dafür, die fehlende Vorwarnung dagegen" (Tab. 6 Low-risk:
nach langem Stehen). Familie: kein Zustandswechsel, Grund „niemand jung und plötzlich" (Tab. 6 Minor).

*Prüfung:* D1: die Pause vor „Frau Doktor" ist Handlung (Blick auf das Sackerl), kein Erzähler-Tag. D4: Scham in
„vor der Kirche, alle haben geschaut" und im „Bitte", nicht benannt. D5: der Wechsel bringt dem Fall das zweite
Ereignis, zeigt den Mann (er schützt die Tochter, nicht sich), hat Subtext („wenn man's sagt, ist es was") und stellt
die Beziehung auf die Probe (was sie verspricht). Die Wahl besteht den Test aus Skill `handlung` §3: unterscheidbar,
Folge sichtbar (Falk, Schluss), korrigierbar, ärztlich (Vertraulichkeit gegen Dokumentationspflicht). Humanizer:
„wie ein nasser Sack" ist seine Zeugin, nicht die Autorin; keine Gedankenstriche.

### 5.6 Untersuchung und Marlene erfährt es (07:00)

> *Spielerin:* Darf ich Sie kurz anschauen? Herz, Lunge, Nerven.
>
> **Herr Baum:** Bitte. Die Jacke lass ich an, gell? Es zieht da herinnen.

*Befundzeilen (bestehende Mechanik, Karte „Untersuchung"):* Puls am Handgelenk langsam, regelmäßig. Herztöne
regelmäßig, langsam, kein Geräusch. Lunge frei, keine Beinödeme. Schürfung linker Ellbogen, blauer Fleck linke Hüfte.
Sprache klar, Gesicht symmetrisch, Arme und Beine seitengleich kräftig, kein Doppeltsehen, Finger-Nase sicher.
→ Herz-Struktur unwahrscheinlich (kein Geräusch, nicht unter Belastung; Tab. 6 Major „unklares Systolikum"),
Schlaganfall/TIA unwahrscheinlich (Bewusstsein weg, Ausfälle keine; Tab. 4, §8.1.3).

Am Tresen (Marlene steht mit Andrea an der Übergabe, Kuli hinterm Ohr; sie dreht sich um, als die Spielerin vorbeigeht):

> **Marlene:** Und? Darf er?
>
> *Spielerin:* 1 Es war gestern schon einmal. Er hat's niemandem gesagt. · 2 Noch nicht. Ich schreib jetzt das EKG.
>
> **Marlene** (1): Was? Dem hab ich den ganzen Morgen Zuckerl angeboten, und er sagt mir nix.
>
> **Marlene:** Schreib's auf den Bogen. Mit Uhrzeit. Und sag's dem Falk als Erstes, bevor er die Notiz von der Steiner liest.
>
> **Marlene** (2): Dann mach. Der Wagen steht an der Wand, Papier ist drin. Ich übergeb.

*Prüfung:* D5: (1) bringt dem Fall die Dokumentation und Falks Reihenfolge, zeigt Marlene (gekränkt, dass er ihr nichts
gesagt hat; stolz auf die Neue, ohne es zu sagen), Subtext „du hast gefunden, was ich nicht gefunden hab", Beziehung
kippt ein Stück zur Kollegin. D1: „Zuckerl angeboten" ist Marlene, nicht Falk. Humanizer: ok.

### 5.7 Das EKG (07:02): Wagen, Kleben, Handy

Wenn die Spielerin den Wagen vor dem Ende der dritten Runde anklickt, ruft Marlene vom Tresen herüber (Meldung in
ihrer Stimme, drei Varianten je nach dem, was fehlt): *„Erst reden, dann kleben. Du weißt noch nicht, was er
nimmt."* / *„…ob das schon einmal war."* / *„…ob er sich verletzt hat."* Das ersetzt die heutige Sperrmeldung.

Der Wagen rollt zur Koje (Bewegung §10). Herr Baum legt sich hin, die Mütze bleibt auf.

> **Herr Baum:** Muss ich das Hemd aufmachen? Ja? Kalt ist das Zeug.
>
> *Spielerin:* 1 Zehn Sekunden ganz ruhig liegen. Nicht reden. · 2 Haben Sie das schon einmal gehabt, ein EKG?
>
> **Herr Baum** (2): Beim Reiter, vor Jahren. Da war's in Ordnung, hat er gesagt. Damals hab ich auch noch die Elfriede gehabt.
>
> **Herr Baum** (1): Nicht reden kann ich nicht, fragen S' die Sabine. Meine Frau hat gesagt, ich red sogar im Schlaf.
>
> *(Das Handy im Sackerl leuchtet und vibriert; Bewegung §10. Herr Baum hebt den Kopf, legt ihn wieder hin.)*
>
> **Herr Baum:** Das ist die Sabine. Gehen S' ran, bitte, ich darf mich ja nicht rühren. Und ich hör eh nix mit dem Ding, wenn ich lieg.
>
> *Spielerin:* 1 Ich geh ran. · 2 Das kann warten, erst das EKG.
>
> **Herr Baum** (2): Dann ruft sie dreimal. Sie kennen sie nicht.

Wählt die Spielerin (2), kommt der Anruf nach dem Streifen noch einmal (Flag `anruf_spaeter`); nichts geht verloren,
die Reihenfolge ist ihre. Rückmeldung zu (2), still: Ein Angehöriger, der dabei war, ist die beste Zeugin, die du
kriegst; am Telefon ist sie jetzt. Beides ist vertretbar. *(ESC-Practical-2018 Web Table 5.3: Zeugenbericht)*

*Prüfung:* D4: die Elfriede (verstorbene Frau) taucht nur hier auf, einmal, als Nebensatz; das ist der „menschliche
Moment beim Kleben", ohne dass er benannt wird. D6: kurze Wechsel, weil er liegt und die Uhr läuft. Humanizer: ok.

### 5.8 Das Telefon (07:04, Sabine Baum; Dialog mit Hörer-Symbol statt Porträt)

Ziel: Fremdanamnese der Zeugin (Krampf aus, Pseudosynkope aus), die Tabletten, der Schlüssel für die Senta. Die
Tochter will wissen, ob er heimdarf, und hat fünf Minuten.

> **Sabine Baum:** Papa? Wer ist da? Ah. Entschuldigung. Ich bin im Kindergarten, ich hab fünf Minuten, bevor die Ersten kommen. Wie geht's ihm?
>
> *Spielerin:* 1 Er liegt gerade am EKG. Was haben Sie heute früh gesehen? · 2 Hat er gezuckt? Waren die Augen offen? · 3 Hat er seine Tabletten heute genommen?
>
> **Sabine Baum** (1): Einen Krach, wie wenn der Tisch umfällt. Er ist am Boden gelegen, grau im Gesicht, die Augen offen. Ich hab Papa gesagt, und er hat gleich geschaut.
>
> **Sabine Baum:** Zwanzig Sekunden vielleicht. Dreißig. Mir ist es wie eine Stunde vorgekommen.
>
> **Sabine Baum** (2): Gezuckt? Nein. Gar nichts. Er ist dagelegen wie ein Sack, das war das Schlimme. Gebissen hat er sich auch nicht, ich hab geschaut.
>
> **Sabine Baum** (3): Nein! Die liegen noch am Tisch, ich hab's gesehen, wie wir gegangen sind. Sonst nimmt er die um sieben mit dem Kaffee. Soll ich sie bringen? Ich kann erst um zwölf.
>
> *(nach allen dreien)*
>
> **Sabine Baum:** Ist das was Schlimmes? Darf er heim? Ich kann ihn erst um halb eins holen.
>
> **Sabine Baum:** Und wegen dem Hund: Die Frau Kainz nebenan hat einen Schlüssel. Ich ruf sie an, wenn er bleibt. Sagen S' ihm das, von mir glaubt er's nicht.
>
> *Spielerin:* 1 Das entscheidet der Oberarzt gleich. Ich ruf Sie an. · 2 Wahrscheinlich nur der Kreislauf. Keine Sorge. · 3 Er hat uns gesagt, dass es gestern schon einmal war.
>
> **Sabine Baum** (1): Gut. Bitte. Die Lena fragt schon.
>
> **Sabine Baum** (2, Flag `tochter_beruhigt`): Gott sei Dank. Das hab ich mir gedacht, er steht ja immer so lang beim Kocher. Dann bis zwölf.
>
> **Sabine Baum** (3, Flag `tochter_verraten`): Gestern? Was gestern? Der sagt mir nichts. Nie. Zum Friedhof will er allein, mit dem Bus, damit ich meine Ruhe hab.
>
> **Sabine Baum:** Ich muss, die Ersten kommen. Danke, Frau, ich weiß gar nicht, wie Sie heißen.

*Rückmeldung zu (2):* Zu früh. Du weißt es noch nicht, und die Tochter wird jedem erzählen, was du gesagt hast.
„Der Oberarzt entscheidet gleich" ist keine Ausrede, es ist der Stand. *(keine fachliche Aussage)*

*Rückmeldung zu (3):* Er hat dich gebeten, es ihr nicht zu sagen, und er ist bei klarem Verstand. Was die Tochter
erfährt, entscheidet er. Du hast ihm gerade das Einzige genommen, worum er gebeten hat. *(ÄrzteG §54, §12)*

*Karte „Fremdanamnese (Tochter, 07:04)":* Krach gehört, am Boden gefunden, grau, Augen offen, kein Zucken, kein
Zungenbiss, nach 20–30 s angesprochen und sofort klar. Tabletten heute nicht genommen. → Krampfanfall
unwahrscheinlich (keine Myoklonien, sofort klar, keine Zunge; §8.1.2, Tab. 10); Pseudosynkope (Rückmeldung): Augen
offen, unter einer Minute (§7.1.2, Tab. 4).

*Prüfung:* D1: Sabine spricht schnell, in halben Sätzen, mit Uhrzeiten („um zwölf", „halb eins"), organisiert („Ich ruf
sie an"); ohne Namen von Marlene und Herrn Baum unterscheidbar. D3: die Fremdanamnese kommt im Moment, in dem sie
zählt (er liegt am EKG). D4: Angst in „wie eine Stunde", nicht benannt. D5: der Anruf löst drei Dinge des Falls
(Krampf, Tabletten, Senta) und stellt die Beziehung Spielerin↔Patient auf die Probe. Humanizer: keine Gedankenstriche,
ein „Gott sei Dank" ist Figur, nicht Autorin.

### 5.9 Der Streifen (07:08): Rhythmusfrage und Zirkel

Meldung: „EKG geschrieben · 07:08". Streifen wie heute (LUDB 39, 25 mm/s für die Rhythmusfrage, 50 mm/s am Zirkel).

**Rhythmusfrage** („Erst der Rhythmus. Was führt hier?"):

| Option | richtig? | Rückmeldung (`warum`) | Beleg |
|---|---|---|---|
| Sinusrhythmus | ja | Vor jedem QRS eine P-Welle, in II positiv, die Abstände gleich. Der Sinusknoten führt. Ob er langsam ist, sagt erst die Frequenz: der Zirkel. | Lektion 8 |
| Ersatzrhythmus aus dem AV-Knoten | nein | Dann fehlte die P vor dem QRS, oder sie wäre in II negativ, im oder hinter dem QRS. Hier steht vor jedem QRS eine positive P. Langsam heißt nicht Ersatz. | Lektion 11 |
| Sinusrhythmus mit ausgefallenen Schlägen (AV-Block II°) | nein | Dann gäbe es P-Wellen, auf die kein QRS folgt, eine Lücke. Hier folgt auf jede P ein QRS, und zwischen den Komplexen liegt keine zweite P. In zehn Sekunden fällt nichts aus. | Lektion 10; Annotation LUDB 39 (6 P / 7 QRS, erster Komplex am Rand) |
| Vorhofflimmern | nein | Kein P, flimmernde Grundlinie, Abstände springen. Hier: P vor jedem QRS, Abstände gleich. | Lektion 25 |

„Kammertachykardie" entfällt (bei 53/min keine ernsthafte Irrmöglichkeit).

**Zirkel** (Mechanik unverändert; Deutungstexte neu dort, wo sie die Fallfrage berühren):

- RR → Frequenz: *„60 000 : {ms} = {hf} pro Minute. Norm 50–100: am unteren Rand. Unter Betablocker erwartbar,
  nicht verdächtig; Sinusbradykardie beginnt erst unter 50."* (Lektion 7, 8; Tab. 5 „ohne negativ chronotrope
  Medikation"). Karte „Frequenz".
- PQ: *„{ms} ms, über 200: AV-Block I°. Damit ist das EKG nicht normal. Mehr sagt es nicht: jeder Vorhofimpuls kommt
  an, keine Pause, kein ausgefallener Schlag in zehn Sekunden."* (Lektion 3, 10; §4.1.1). Karte „PQ-Zeit" mit dem
  Hinweis auf die Streuung des P-Beginns (wie heute). → Verdachtsliste: Herzrhythmus „EKG nicht normal: AV-Block
  I°; kein Beweis".
- QRS (optional): *„{ms} ms, schmal. Die Kammern laufen über das normale Leitungssystem; die Bremse sitzt oben, in
  der Überleitung."* (Lektion 4, 10). Karte „QRS".

**Vergleiche in der Mappe** (bestehende Mechanik): PQ ↔ Medikamente („Der Betablocker bremst beide Etagen: Taktgeber
und Überleitung. Die Ohnmacht erklärt er trotzdem nicht."); Rhythmus ↔ Anamnese („Zehn Sekunden Papier gegen zwei
Ohnmachten. Der Streifen war nicht dabei. Was er beweisen könnte, hat er nicht gezeigt: keine Pause, kein Block
mit ausgefallenen Schlägen."); Frequenz ↔ Aufnahmebogen (Puls 52 getastet, {hf} gemessen: dieselbe Zahl; Lektion 7).

Danach läuft die Uhr auf 07:14, und der Stand sagt in einem Satz: *„Falk kommt um viertel nach sieben. Was sagst du
ihm zuerst?"* Das ist Takt 5 (Sequel): Mappe und Verdachtsliste anschauen, nichts anklicken müssen.

---

## 6. Die Übergabe (ISBAR) und Falks Gegenrede (07:15–07:28)

Ziel des Takts: Die Spielerin bringt ihre Befunde in eine Form, die ein Oberarzt mit zwölf Minuten annimmt, und
hält seiner fertigen Meinung stand. Falk will die Koje und hat die Notiz des Nachtdienstes gelesen; er ist kein
Rätselonkel, er ist ein müder, präziser Mann, der die harmlose Erklärung bevorzugt, bis ihm jemand sagt, warum nicht.

### 6.1 Ankunft

> **Erzähler:** 07:15. Die Tür. Dr. Falk, Kaffee in der einen Hand, die Übergabeliste in der anderen. Er liest, bevor er grüßt.
>
> **Dr. Falk:** Sie sind neu. Falk. Koje drei, Herr Baum, vasovagal, steht da. Ich brauch die Koje um halb acht, die Rettung hat zwei angemeldet. Kann er heim?
>
> *Spielerin:* 1 Darf ich kurz übergeben? · 2 Nein. · 3 Ja, wahrscheinlich.
>
> **Dr. Falk** (1): Kurz. Wer, was, was Sie denken, was Sie wollen. In der Reihenfolge, wenn's geht.
>
> **Dr. Falk** (2 oder 3): Das ist eine Antwort, keine Übergabe. Wer, was, was Sie denken, was Sie wollen. Dann reden wir über ja oder nein.

Die Antwort auf „Kann er heim?" ist noch keine Entscheidung; sie wird in Zeile R gestellt. Rückmeldung zu (2)/(3),
still: Ein Oberarzt mit zwölf Minuten will zuerst den Patienten, nicht dein Urteil. ISBAR: Identifikation,
Situation, Hintergrund, Einschätzung, Empfehlung. *(Übergabe-Standard, keine fachliche Aussage; §12)*

### 6.2 Die vier Zeilen (Mechanik: je Zeile eine Wahl; die gewählte Zeile erscheint als Replik der Spielerin)

Falk unterbricht nach der ersten Zeile und zieht das EKG vor; die Reihenfolge wird I/S → A → B → R. Die Karte
„Übergabe" ordnet sie danach wieder richtig (I, S, B, A, R) und sagt, warum er umgestellt hat.

**I/S (wer, was):**

| Option (≤ 64) | Art | Falk | `warum` |
|---|---|---|---|
| Herr Baum, 68. Zweimal weg ohne Vorwarnung, gestern und heute. | richtig | Zweimal? Da steht einmal. Küche. *(Spielerin: Gestern an der Haltestelle. Er hat's niemandem gesagt.)* Hm. | Wer, Alter, was, wie oft, das Entscheidende zuerst. Das zweite Ereignis gehört in den ersten Satz, weil es die Notiz kippt. |
| Herr Baum, 68, Synkope, vermutlich vasovagal. | vage, Anker | Vermutlich steht schon da. Was ist passiert? | Du hast ihm seine eigene Notiz vorgelesen. Situation heißt: was passiert ist, nicht was jemand vermutet. |
| Ein älterer Herr, dem schwindlig geworden ist. | falsch | Schwindlig? Er lag am Boden und weiß nichts davon. Das ist nicht schwindlig. Noch einmal. | Schwindel ist kein Bewusstseinsverlust. Vier Merkmale: kurz, umgesunken, keine Reaktion, Erinnerungslücke. Alle vier da. *(§4.1)* |

Bei `versprochen`: **Dr. Falk:** Und Ihnen hat er's gesagt, weil? *(Spielerin: Weil ich gefragt hab.)* **Dr. Falk:**
Steht nicht am Bogen. Schreiben Sie's drauf.

**Falk unterbricht:** *EKG. Bevor Sie weiterreden.*

**A (Einschätzung, vorgezogen):**

| Option | Art | Falk | `warum` |
|---|---|---|---|
| Sinus, 53, PQ 228, QRS schmal. Nicht normal, kein Beweis. | richtig | Dreiundfünfzig. Zweihundertachtundzwanzig. Gut. Weiter. | Rhythmus, Frequenz, Überleitung, Kammer, und was es bedeutet: nicht normal (PQ > 200), aber nichts, was eine arrhythmische Synkope beweist. *(Lektion 10; §4.1.1)* |
| Bradykardie, 53. Das erklärt die Ohnmacht. | falsch (Flag `brady_argument`) | Dreiundfünfzig unter Betablocker ist erwartbar. Und mit dreiundfünfzig fällt niemand um. Was noch? | 53/min ist Sinusrhythmus am unteren Rand der Norm; Bradykardie erst unter 50. Unter Betablocker erwartbar; als Warnzeichen gilt erst dauerhaft unter 40 im Wachen. *(Lektion 8, 35; Tab. 6)* |
| EKG unauffällig. | falsch | Zweihundertachtundzwanzig ist nicht unauffällig. Haben Sie gemessen oder geschaut? | PQ über 200 ms ist ein AV-Block I°. Ein EKG mit AV-Block I° ist nicht normal, auch wenn es niemanden umwirft. *(Lektion 3, 10)* |
| PQ hab ich nicht gemessen. *(nur ohne Karte PQ)* | Rückweg | Dann messen Sie. Der Wagen steht da. Ich hab zwölf Minuten. | (bestehende Mechanik: Rückweg zum Wagen) |

**B (Hintergrund):**

| Option | Art | Falk | `warum` |
|---|---|---|---|
| Betablocker seit Jahren, heute nicht. Schellong negativ. | richtig | Heute nicht genommen. Merken wir uns. | *(gesprochen: Bluthochdruck seit zehn Jahren, Betablocker seit Jahren, heute nicht genommen, Stehversuch unauffällig.)* Vorerkrankung, Medikation mit Änderung (keine) und Einnahme (heute nicht), Stehversuch: das, was die Einschätzung trägt. *(Tab. 5; Web Table 5.6)* |
| Die Tochter hat's gesehen: kein Zucken, Augen offen, sofort da. | richtig (zweite B-Zeile, freiwillig) | Dann ist es kein Anfall. Das nehm ich. | Die Zeugin trennt Synkope von Anfall: keine Zuckungen, sofort klar. *(§8.1.2, Tab. 10)* |
| Er geht täglich mit dem Hund, ist fit für sein Alter. | vage | Schön für den Hund. Was nimmt er? | Belastbarkeit ist ein Befund gegen die strukturelle Herzkrankheit, aber Hintergrund heißt zuerst: Vorerkrankungen, Medikamente. |
| Drei Tabletten, welche weiß ich nicht. *(nur ohne Karte Medikamente)* | Rückweg | Dann holen Sie den Zettel. Drei Meter. | (bestehende Mechanik: Rückweg zum Patienten) |

**R (Empfehlung):**

| Option | Art | Falk | `warum` |
|---|---|---|---|
| Er bleibt. Monitor. Und das Bisoprolol heute nicht. | richtig | Monitor. Für einen Mann, der lang gestanden ist und Betablocker nimmt. Überzeugen Sie mich. | Die Empfehlung in einem Satz, mit Konsequenz. Jetzt muss sie begründet werden. |
| Er kann heim, Kontrolle beim Hausarzt. | Irrweg (Flag `heim_empfohlen`) | Das wollte ich hören. Sagen Sie mir, warum. Nicht, weil ich die Koje brauch. | Vertretbar wäre das nur bei niedrigem Risiko: Vorwarnung, normales EKG, keine Herzkrankheit. Prüf, ob du das hast. *(Tab. 6)* |
| Noch einen Stehversuch, dann sehen wir weiter. | Irrweg | Marlene hat ihn gemacht, dreimal gemessen, nichts. Was wollen Sie beim zweiten Mal sehen, was beim ersten gefehlt hat? | Der Stehversuch ist gemacht und negativ; er prüft die Orthostase, nicht das Risiko. Wiederholen beantwortet die Frage nicht. *(§4.2.2.1)* |

### 6.3 Die Gegenrede: „Überzeugen Sie mich"

> **Dr. Falk:** Lange gestanden, Betablocker, achtundsechzig. Kreislauf. Die Steiner hat's auch so gesehen. Ich brauch die Koje. Überzeugen Sie mich.

Mechanik (neu, `aufgaben.argument`): Die Spielerin wählt nacheinander Argumente; jedes ist eine Karte oder ein
Eintrag der Verdachtsliste, in einem Satz. Falk antwortet auf jedes. Er gibt nach, sobald die beiden tragenden
Argumente gefallen sind (keine Vorwarnung **und** EKG nicht normal), in beliebiger Reihenfolge; die anderen
stützen. Nach vier Argumenten ohne die beiden gibt er einen Hinweis, keinen Abbruch. Kein Game Over.

| Argument (Option) | Falk | `warum` |
|---|---|---|
| **Keine Vorwarnung. Beide Male.** | Zählt. Aber nur, wenn das EKG nicht sauber ist. Ist es sauber? | Fehlende Vorwarnung ist ein Minor-Merkmal: Es zählt als hohes Risiko nur zusammen mit einer Herzkrankheit oder einem auffälligen EKG. *(Tab. 6)* |
| **PQ 228. Das EKG ist nicht normal.** | *(wenn das erste schon fiel)* Nicht normal. Nicht gefährlich. Aber mit dem Ersten zusammen nicht mehr niedrig. *(sonst)* Nicht normal, nicht gefährlich. Allein ist das nichts. Was macht es zu etwas? | Niedriges Risiko verlangt ein normales EKG. AV-Block I° ist nicht normal. Allein ist er kein Risikomerkmal; mit „keine Vorwarnung" zusammen ist der Patient nicht mehr niedrig. *(Tab. 6; Lektion 10)* |
| Zweimal in zwei Tagen. Das erste Mal mit 68. | Mit achtundsechzig fängt man nicht mit Kreislaufgeschichten an. Das geb ich Ihnen. | Die Reflexsynkope hat meist eine lange Vorgeschichte, oft seit der Jugend. Ein erstes Mal mit 68, und gleich zweimal, ist das Gegenteil davon. *(Tab. 5, Tab. 6 Low-risk)* |
| Er hat sich verletzt. Ellbogen, Hüfte. | Die Schramme allein ist mir egal. Die Schramme bei dem Rest nicht. | Verletzung durch die Synkope spricht für Aufnahme, wenn Risikomerkmale da sind. *(Tab. 7)* |
| Stehversuch negativ, in der Küche stand er eine Minute. | Dann ist es nicht der Kreislauf im Stehen. Das nimmt mir meine Erklärung. Es gibt Ihnen noch keine. | Kein Abfall ≥ 20/10 mmHg nach drei Minuten, kein Sturz beim Aufstehen: Orthostase unwahrscheinlich. Das schließt aus, es beweist nichts. *(§4.2.2.1, Tab. 5)* |
| Die Tochter hat kein Zucken gesehen. | Das sagt, es war kein Anfall. Es sagt nicht, dass er bleiben muss. | Zeugenbericht trennt Anfall und Synkope. Für die Risikofrage ist das kein Argument. *(Tab. 10)* |
| Puls 53, das ist eine Bradykardie. | Unter Betablocker ist dreiundfünfzig erwartbar. Das ist kein Argument, das ist eine Zahl. | Sinusrhythmus 50–100 normal; Bradykardie unter 50; Warnzeichen erst dauerhaft unter 40 im Wachen, und die Leitlinie nimmt bremsende Medikamente ausdrücklich aus. *(Lektion 8; Tab. 5, Tab. 6)* |
| Der Vater hatte einen Schlaganfall. | Mit achtzig. Das ist Familie, kein Risiko. Jung und plötzlich wäre eines. | Das Familien-Merkmal heißt: plötzlicher Herztod in jungen Jahren. Ein Schlaganfall mit 80 ist keines. *(Tab. 6)* |
| Könnte es eine TIA gewesen sein? | Eine TIA nimmt etwas weg. Sprache, Kraft, ein Gesichtsfeld. Das Bewusstsein lässt sie in Ruhe. Haben Sie ihn reden und gehen lassen? *(Spielerin: Ja. Alles seitengleich.)* Dann war's keine. | TIA = fokaler Ausfall ohne Bewusstseinsverlust; vertebrobasilär nie ohne Hirnstammzeichen. Hier: Bewusstsein weg, Ausfälle keine. *(Tab. 4, §8.1.3; Web Table 5.4)* |
| *(nach vier Argumenten ohne die beiden tragenden)* | Sie haben es, Sie sagen es nur nicht. Was macht aus „keine Vorwarnung" ein Warnzeichen? Schauen Sie auf Ihr EKG. | Hinweis, keine Lösung. |

Falk gibt nach:

> **Dr. Falk:** Gut. Keine Vorwarnung und ein EKG, das nicht sauber ist. Das ist nicht niedrig. Er bleibt. Monitor, bis ich den Speicher gesehen hab.
>
> **Dr. Falk:** Die Koje kriegt die Rettung trotzdem. Oben ist ein Bett frei, ich ruf an.

*Rückmeldung (`warum`, die zentrale des Falls):* Die harmlose Erklärung trägt nicht mehr: keine Vorwarnung, EKG
nicht normal, erstes Mal mit 68, zweimal. Das Ruhe-EKG beweist nichts; beweisen würde eine Pause über drei
Sekunden im Wachen, ein Mobitz II, ein AV-Block III° oder ein Puls dauerhaft unter 40. Die sieht man nur, wenn
jemand hinschaut, während es passiert. Dafür der Monitor, jetzt, nicht nächste Woche. *(Tab. 6, §4.1.1, §4.2.4.1)*
→ Verdachtsliste: Herzrhythmus „nicht bewiesen, nicht ausgeschlossen"; Reflex durchgestrichen.

**Variante `heim_empfohlen`:** Falk fragt nach Gründen für die Entlassung; drei Optionen, alle werden widerlegt:
„Stehversuch negativ." → *Das sagt, es ist nicht der Kreislauf. Es sagt nicht, dass er heimdarf.* „Das EKG ist
fast normal." → *Fast.* „Er fühlt sich gut und will heim." → *Das hat er gestern auch. Und heute lag er in der
Küche.* Danach: **Dr. Falk:** Sie überzeugen mich nicht. Andersrum: Warum soll er bleiben? → dieselbe Argumentation
wie oben. Rückmeldung: Entlassung aus der Notaufnahme nur bei niedrigem Risiko; prüf die Liste, nicht das Gefühl
des Patienten. *(Tab. 6, §4.1.2)*

### 6.4 Die Tabletten (07:24)

> **Dr. Falk:** Die Tochter sagt, seine Tabletten liegen daheim am Tisch. Was kriegt er jetzt von uns?
>
> *Spielerin:* 1 Alle drei, wie immer. · 2 Ramipril und ASS. Bisoprolol erst nach dem Monitor. · 3 Nichts, bis alles geklärt ist.
>
> **Dr. Falk** (2): Gut. Der Blutdrucksenker bremst keinen Knoten, den kann er haben. Der Betablocker wartet. Ich schreib's auf.
>
> **Dr. Falk** (1): Mit dreiundfünfzig und einer Überleitung von zweihundertachtundzwanzig geben Sie ihm das Einzige, das beide bremst? Noch einmal.
>
> **Dr. Falk** (3): Warum soll er ohne Blutdrucksenker dastehen? Das Einzige, das bremst, ist das Bisoprolol. Das andere kann er haben.
>
> *(bei `brady_argument`, vor der Wahl)* **Dr. Falk:** Vorhin war dreiundfünfzig für Sie eine Bradykardie. Jetzt sind es zwei Etagen, die der Betablocker bremst. Entscheiden Sie sich.

*Rückmeldungen:* (2) Betablocker bremsen Sinusknoten und AV-Überleitung; bei Bradyarrhythmie unter einem solchen
Medikament ist Dosisreduktion oder Absetzen der erste Schritt, bevor man an mehr denkt. ACE-Hemmer und ASS bremsen
keinen Knoten; der Blutdruck ist 142/84, der Stehversuch unauffällig: kein Grund, sie wegzulassen. *(ESC-Pacing-2021
§3.3/Tab. 6, §5.1.1.2; Pharmakologie QUELLEN §3; Weitergabe von Ramipril/ASS ist Falks klinische Entscheidung,
keine Leitlinienaussage)* (1) Das Bisoprolol ist das einzige Mittel auf dem Plan, das Frequenz und Überleitung
bremst; es jetzt zu geben, bevor der Monitor gezeigt hat, was die Leitung ohne Bremse macht, verwischt die Frage,
die ihr gerade gestellt habt. *(ESC-Pacing-2021 §5.1.1.2)* (3) Nicht gefährlich, aber ohne Grund: Ramipril und ASS
haben mit der Ohnmacht nichts zu tun; wer ohne Grund absetzt, schafft ein neues Problem (Blutdruck). *(Pharmakologie)*

Ergebnis: Karte „Entscheidung (07:25)": Monitor; Bisoprolol heute pausiert, Ramipril und ASS gegeben; Dr. Falk.
Behandlung wird so Teil des Falls (KONZEPT §1.7), ohne Dosisänderung, ohne neue Substanz.

### 6.5 Falk am Bett (07:26)

Falk geht zur Koje (Figur bewegt sich, §10), hört kurz ab.

> **Dr. Falk:** Herr Baum. Falk. Ich hör kurz. *(Pause)* Regelmäßig, langsam, kein Geräusch. Wie die Kollegin.
>
> **Dr. Falk:** Sie bleiben heute bei uns. An einem Monitor, oben. Die Kollegin erklärt's Ihnen, sie kennt Sie besser als ich.
>
> **Herr Baum:** Aber die Senta.
>
> **Dr. Falk** (schon im Gehen, zur Spielerin): Dreiviertel acht, Besprechung. Sie kommen nach, wenn er oben ist. Hinten sitzen, nichts sagen.

*Prüfung des ganzen Takts:* D1: Falk nennt Zahlen zuerst, stellt Gegenfragen, lobt nie ohne Haken („Das geb ich
Ihnen."), kein Gedankenstrich, Pausen als kurze Sätze. D2: laut lesbar; kein Satz über 150 Zeichen. D3: Falk doziert
nicht; die Tabellenlogik steht in den Rückmeldungen. D4: Zeitdruck in „zwölf Minuten", „Koje", „Besprechung", nie
„Ich bin unter Druck". D5: jede Gegenrede bringt dem Fall ein Kriterium, zeigt Falk (prüft, nicht quält), hat Subtext
(„Ich will, dass Sie recht haben, aber ich sag's nicht") und verschiebt die Beziehung (vom Abfragen zum Streiten
auf Augenhöhe). D6: kurze Wechsel, Unterbrechungen, weil Akutlage und Uhr. Entscheidungstest (Skill `handlung` §3):
R ist ein Dilemma (heim/bleiben, beide vertretbar klingend), die Argumente sind Strategie, die Tabletten eine
echte Behandlungsentscheidung mit sichtbarer Folge (Karte, Epilog). Humanizer: „Schön für den Hund." ist trocken,
nicht aphoristisch; keine Dreierreihen außer „Lange gestanden, Betablocker, achtundsechzig", die seine
Argumentliste ist.

---

## 7. Behandlung, Schlussgespräch, Ende, Epilog

### 7.1 Schlussgespräch mit Herrn Baum (07:30)

Ziel: Er bleibt, weil er versteht, warum, und weil die Senta versorgt ist. Herr Baum will nicht „was" haben und
nicht zur Last fallen; er bietet den Revers an, bevor jemand ihn nennt.

> **Herr Baum** (sitzt wieder, Jacke an): Frau Doktor. Ich kann nicht bleiben. Die Senta sitzt daheim, die Sabine kommt erst um halb eins. Und mir fehlt nix. Ich unterschreib Ihnen alles.
>
> *Spielerin:* 1 Das ist jetzt nicht wichtig. Sie bleiben. · 2 Dann unterschreiben Sie einen Revers. · 3 Gestern und heute waren Sie weg, ohne es zu merken. · 4 Wegen der Senta: Die Frau Kainz hat den Schlüssel.
>
> **Herr Baum** (1): Für Sie nicht. *(dreht sich zum Fenster; die Optionen bleiben, (1) verschwindet)*
>
> **Herr Baum** (2, Flag `revers`): Her damit. *(Pause)* Was steht da drauf? Dass ich selber schuld bin?
>
> **Herr Baum** (4 vor 3): Die Kainz? Und wieso soll ich überhaupt bleiben? Der Doktor hat nix gesagt. Nur „die Kollegin erklärt's".
>
> **Herr Baum** (3): Ja, und? Jetzt bin ich ja da.
>
> *Spielerin:* 1 Das kann vom Herzen kommen. Ein Aussetzer. · 2 Ihr Herz schlägt langsam, die Überleitung auch.
>
> **Spielerin** (1): Das kann vom Herzen kommen. Ein Aussetzer, ein paar Sekunden. Den sieht man nur, wenn Sie am Monitor hängen, während er passiert.
>
> **Herr Baum** (1): Ein Aussetzer. *(Pause)* Und wenn's keiner ist?
>
> **Herr Baum** (2): Langsam bin ich überall. Das ist das Alter, nicht das Herz.
>
> **Spielerin:** Dann wissen wir morgen, dass es keiner war. Heute wissen wir's nicht. Deshalb der Monitor, nicht die Haltestelle.
>
> **Herr Baum:** Und die Senta?
>
> **Spielerin:** Die Frau Kainz hat den Schlüssel. Ihre Tochter ruft sie an. Das soll ich Ihnen sagen, von ihr glauben Sie's nicht.
>
> **Herr Baum** (Flag `senta_geloest`): Die Kainz. Die mag sie eh. Mehr als mich, glaub ich. *(zieht die Jacke aus, legt sie über den Sessel)* Dann bleib ich halt. Aber die Mütze bleibt auf.
>
> *(bei `versprochen`)* **Herr Baum:** Sie haben's ihm gesagt. Von gestern. *(Spielerin: Dem Arzt. Nicht der Sabine.)* Passt. Der Arzt ist der Arzt.
>
> *(bei `tochter_verraten`)* **Herr Baum:** Die Sabine hat's gewusst, wie sie angerufen hat. Von Ihnen. *(zieht die Jacke trotzdem aus)* Ich bleib. Aber nicht wegen Ihnen.

*Rückmeldungen:* (1) „Nicht wichtig" ist für ihn das Wichtigste. Wer die Sorge wegwischt, verliert den Patienten,
nicht das Argument. (2) Der Revers ist das Ende eines Gesprächs, nicht sein Ersatz. Er darf gehen, wenn er
verstanden hat, was ihr befürchtet; das hat er noch nicht gehört. *(keine fachliche Aussage)* (3) Richtig: seine
Worte („weg"), nicht deine (Synkope, Risiko). Dann der Grund in einem Bild (Aussetzer) und was der Monitor kann.
*(§4.2.4.1)* Zu „Ihr Herz schlägt langsam…": Das ist dein Befund, nicht sein Problem; er hört „Alter" und hat recht.
(4) Die Senta zuerst löst das Hindernis, aber nicht die Frage; er fragt zu Recht „wieso überhaupt".

*Prüfung:* D1: Herr Baum bleibt derselbe (Senta, Kainz, Mütze, „halt"). D4: das Einlenken ist die Jacke, nicht ein
Satz. D5: die Szene bringt dem Fall die Entscheidung in Laiensprache und zeigt, was die Spielerin verstanden hat.
Entscheidungstest: Ausdruck (wie sie es sagt) mit sichtbarer Folge (Jacke, Flags), korrigierbar, kein Game Over.
Humanizer: ok.

### 7.2 Marlenes Abschied und Schlussbild (07:35–07:40)

> **Marlene** (mit Kanne, Jacke über dem Arm, an der Koje): So. Ich geh. Herr Baum, oben haben's bessere Betten als da. Und Sie lassen die Mütze auf, ich kenn Sie.
>
> **Marlene** (zur Spielerin): Nicht schlecht für sieben Uhr früh. *(bei `revers`:)* Revers hat er dir angeboten. Hast ihn nicht gebraucht.
>
> **Erzähler:** 07:40. Der Transportdienst holt Herrn Baum ab, die Mütze auf dem Kopf, das Sackerl auf dem Bauch. Die Jacke bleibt über dem Sessel, du nimmst sie mit.
>
> **Erzähler:** Marlenes Stuhl ist leer, die Kanne ist weg. Du gehst mit nach oben, dann in die Besprechung. Hinten sitzen, nichts sagen.

Echo auf den Anfang (Skill `handlung` §4): die Jacke (angezogen → über dem Sessel → in deiner Hand), die Mütze, die
Kanne, die Uhr. Keine Zusammenfassung, keine Moral.

### 7.3 Epilog (Dienst 3, 13:20; Erzähler, ohne Porträt, ohne Kurve)

> **Erzähler:** Dienst 3, 13:20. Marlene fängt dich am Flur ab, die Kanne in der Hand. Sie hat den Speicher von Herrn Baums Monitor gesehen.
>
> **Erzähler:** In der zweiten Nacht, als von seinen Tabletten nichts mehr im Blut war, hat der Monitor eine Pause aufgezeichnet, länger als drei Sekunden. Er war wach, ihm war schwindlig, er hat geklingelt.
>
> **Erzähler:** Am Donnerstag hat er einen Zweikammer-Schrittmacher bekommen. Am Samstag ist er heim, die Mütze auf dem Kopf.
>
> **Erzähler** (bei `senta_geloest`): Die Senta hat die Frau Kainz bis zum Parkplatz gebracht. Weiter durfte sie nicht.
>
> **Erzähler** (bei `tochter_beruhigt`): Die Tochter hat dich gefragt, warum du am Montag „Kreislauf" gesagt hast. Du hast es ihr erklärt. Es hat gedauert.

*Karte „Epilog: Was der Monitor gezeigt hat":* Pause über drei Sekunden im Wachen, mit Beschwerden, ohne
bremsendes Medikament (letzte Bisoprolol-Dosis Sonntag früh, zweite Nacht rund 65 Stunden später, mehr als fünf
Halbwertszeiten): eines der Kriterien, die eine arrhythmische Synkope beweisen. Weil die Tabletten nicht mehr
beteiligt waren, war die Ursache nicht reversibel; deshalb Schrittmacher, Zweikammer, statt Abwarten.
*(ESC-Synkope-2018 §4.1.1; ESC-Pacing-2021 §5.1.1.1 (reversible Ursache ausschließen), §5.1.1.2 (unter Medikament
erst Absetzen; „in vielen Fällen bleiben sie bestehen"), §5.4 (symptomatische Asystolie > 3 s), §5.1.2/§5.2.2.1
(Zweikammer); Halbwertszeit Bisoprolol 10–12 h, Pharmakologie-Standardwissen, QUELLEN §9)*

Was sich gegenüber dem heutigen Epilog ändert: Das Bisoprolol wird nicht „auf der Kardiologie zuerst abgesetzt",
sondern war seit Montag früh pausiert (Entscheidung aus Takt 6); die Pause in der zweiten Nacht fällt deshalb
schon in die Zeit ohne Wirkstoff, und die Zeile „drei Tage ohne Betablocker, dann wieder eine Pause" entfällt.
Mechanismus der Pause (Sinusarrest oder AV-Block) wird weiterhin nicht genannt (keine annotierte Aufnahme).

---

## 8. Realismus-Prüfung der Umgebung

Maßstab: eine internistische Notaufnahme in Österreich (Graz), Montag, 06:40, Schichtwechsel, erster Tag einer
Famulantin. Was ich aus der Praxis sicher weiß, steht ohne Vermerk; was vom Haus abhängt, trägt „beim Nutzer
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
| Synkopen-Patient sitzt 25 Minuten auf der Wartebank | Nach der Triage liegt er auf einer Liege in einer Koje (Box, Behandlungsplatz) mit Vorhang, Besuchersessel, Wandarm mit Blutdruckgerät | Koje 3 statt Bank (Bildauftrag B1); er sitzt auf der Liegenkante, später liegt er |
| Kein EKG, ohne Grund | Das EKG gehört zur Erstbewertung (ESC-Synkope-2018 §4.1) und schreibt meist die Pflege bei der Triage | Grund im Text: Nachtdienst-Ärztin seit 06:30 im Schockraum, Notiz „EKG ausständig", Marlene mit acht Übergaben; die Famulantin schreibt es (Famulantinnen schreiben EKGs) |
| **Der Schirm des EKG-Wagens zeigt Herrn Baums Kurve, bevor eine Elektrode klebt** (`web/spiel.js` `starteSchirme`, `wagen_schirm`, Zeilen 554–581; Screenshot 01) | Ein Gerät ohne Patient zeigt nichts: dunkles Glas, Bereitschafts-LED; die Kurve erscheint beim Schreiben und verschwindet, wenn die Elektroden abgenommen sind | Schirm dunkel bis `ekg_geschrieben`; Kurve (LUDB 39) nur während des Schreibens, danach wieder dunkel; der Prototyp `prototyp/bewegung/leben.js` macht das schon (`ekg`/`ekg_aus`) |
| Kommt allein zu Fuß nach einer Ohnmacht im Morgengrauen | Angehörige bringen ihn; die Tochter fährt | Tochter hat ihn um 06:15 gebracht, musste zum Dienst (Kindergarten 07:00); sie ruft an |
| Kein Patientenarmband | Jeder aufgenommene Patient trägt eines (Name, Geburtsdatum; Daten setzt kein Bild, das Band ist leer) | weißes Band am linken Handgelenk in allen Posen, neben dem roten Bändchen (B2) |
| Niemand sonst da: kein Telefon, keine Rettung, keine Reinigung, kein Schichtwechsel | 06:40–07:40 ist die dichteste Stunde: Nachtdienst übergibt (Pflege 19:00–07:00, zwölf Stunden, in vielen Häusern üblich; beim Nutzer prüfen), Tagdienst kommt, Rettung bringt die Ersten, Reinigung fährt durch, Drucker läuft | Andrea (Tagdienst) ab 07:00 am Tresen, Übergabe im Hintergrund; Rettung im Flur 06:50 und 07:20; Reinigungskraft 07:05; Telefon am Tresen (06:40, 07:12); Drucker (07:16, Falks Liste) |
| Oberarzt kommt, wenn Marlene ruft | Der Oberarzt kommt zum Dienstbeginn herunter, liest die Übergabeliste, hat vor der Frühbesprechung wenige Minuten | Falk 07:15, Besprechung „dreiviertel acht" (Uhrzeit beim Nutzer prüfen), Rettung hat zwei angemeldet |
| „Tüte", „Bank", „Stuhl" | In Graz: Sackerl, Liege, Sessel | Texte; Klickfeld-Name `tuete` bleibt im Code, die Beschriftung heißt „Sackerl" |
| Strickjacke „unterm Patientenhemd" (ART_BIBLE §5) | Um 06:40 nach der Fahrt im Auto trägt er seine Kleidung; das Hemd macht er fürs EKG auf; ein Patientenhemd bekommt er oben | Posen ohne Patientenhemd (B2); ART_BIBLE §5 anpassen |
| Falk nimmt den Patienten nie wahr | Ein Oberarzt hört kurz ab und sagt dem Patienten einen Satz, bevor er geht | §6.5 |
| Triage nicht erwähnt | Österreichische Notaufnahmen triagieren (verbreitet Manchester-Triage); eine Synkope ohne Warnzeichen landet meist bei Gelb (beim Nutzer prüfen) | Bogen: „Triage 06:20"; Farbe nur im Text, nie im Bild |
| Revers kommt nicht vor | Der Revers (Entlassung gegen ärztlichen Rat) ist in Österreich der Alltagsbegriff, Patienten bieten ihn selbst an | §7.1 |
| Händedesinfektion | Spender an der Kojenwand | B1 (Requisite, keine Mechanik) |

Offen gelassen (keine Mechanik, nur Erwähnung): Dienstkleidung und Namensschild der Famulantin („kriegst du um acht
von der Verwaltung" könnte Marlene sagen; nicht nötig), Transport nach oben (Transportdienst mit Pflegeperson; die
Spielerin geht mit).

### 8.3 Bildaufträge (ohne Schrift, ohne gemalte EKGs, ohne Menschen in den Raumebenen; ART_BIBLE §6)

| Nr. | Auftrag | Technik | Aufwand |
|---|---|---|---|
| **B1** | **Aufnahme neu rendern:** links Tresen wie heute, dazu Telefon mit Hörer, kleiner Drucker, Desinfektionsspender an der Wand; Mitte Fensterfront (Sonne **nicht** rendern, sie wird SVG), Lampe am Tresen ohne eingebrannten Lichtkegel; rechts hinten Flurdurchgang als Glastür mit Seitenscheibe, mindestens 300 px breit (heute 67 px: Silhouetten sind dort unsichtbar); rechts **Koje 3**: Liege mit erhöhtem Kopfteil (Mint-Bezug), Vorhang an Deckenschiene halb zugezogen (Petrol), Besuchersessel (Holz/Petrol), Wandarm mit Blutdruckgerät, zwei Wandanschlüsse, Haken; EKG-Wagen **als eigene Ebene** `wagen.png` an der Wand zwischen Tresen und Koje, Schirm als dunkles Glas (Kurve und LED kommen aus dem Code). Rost-Objekt bleibt die Betablocker-Schachtel im Sackerl. Hitboxen: `marlene`, `tresen_telefon`, `wagen`, `koje` (Herr Baum), `tuete`, `uhr`, `pinnwand`, `ausgang`. | Blender-Pipeline (`gen/blender/`), drei Ebenen + Wagen | 1–2 Tage |
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

> **Dr. Falk:** Bett 1, Ihr Herr Baum. Der Schirm und Ihr Papier von heute früh. Was weiß der Schirm, was das Papier nicht weiß? Und umgekehrt?

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
| 07:02 Klick auf den Wagen (freigegeben) | `wagen:zur_koje`, `pose:herrk:liegt`, `elektroden:an` | Wagen rollt, Herr Baum liegt, Punkte erscheinen |
| 07:04 im Dialog „Zehn Sekunden ruhig" | `handy` (im Sackerl), danach `telefon:dialog` | Handy leuchtet und vibriert im Sackerl; Hörer-Symbol im Dialog |
| 07:05 (Zeit) | `flur:reinigung` | Reinigungswagen |
| 07:08 EKG geschrieben | `ekg` (Kurve + Papier, 10 s), dann `ekg_aus`, `elektroden:aus`, `wagen:zurueck`, `pose:herrk:sitzt` | Papier wächst, Streifen-Dialog öffnet sich, Wagen rollt zurück |
| 07:12 (Zeit) | `telefon_tresen` (Andrea hebt ab) | |
| 07:15 Falk | `tuer:auf`, `falk:tresen`, `drucker` | Tür, Falk, Liste |
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
   §5 Anamnese in drei Runden, §6 Rhythmusfrage neu, §8 Ende mit Behandlungsentscheidung (Bisoprolol pausiert),
   Epilog neu, §9 Belege um §12 hier. `docs/QUELLEN.md`: §5 (Tab. 6 am PDF, Tab. 7 Spalten), §9 anpassen, neuer §10
   für die neuen Belege. `docs/FACHREGELN.md` „Nicht aus dem EKG-Kurs": ISBAR, Verschwiegenheit (keine Medizin, aber
   Spielinhalt). Skill `dialoge` §4: Stimmprofil Sabine Baum. `docs/ART_BIBLE.md` §5: Herr Baum ohne Patientenhemd,
   Patientenarmband; §4 bleibt.
3. **Motor** (`web/motor/`), neu oder erweitert:
   - `verdacht.js`: Verdachtsliste (Einträge, Zustände, Gründe, Karte, HUD-Knopf, stille Meldung); Wirkung
     `verdacht:EINTRAG:ZUSTAND:TEXTID`.
   - `fall.js`: Aufgabentypen `sbar` (Zeilen mit Optionen, Unterbrechung, Umstellung der Reihenfolge, Karte) und
     `argument` (Argumente aus Karten/Verdacht, Antworten, Bedingung für das Nachgeben, Hinweis nach n Versuchen);
     Dialogfigur ohne Porträt mit Symbol (`figur: "tochter", symbol: "hoerer"`); Wirkungen `pose:FIGUR:NAME`,
     `leben:EREIGNIS`, `anruf:BAUM.KNOTEN` (verzögert, Flag `anruf_spaeter`); Meldungen in Figurenstimme vom
     Tresen (`melde:ID:marlene`); Runden-Logik für die Anamnese (Liste schließt, Figur spricht den Übergang).
   - `leben.js` aus dem Prototyp übernehmen und um §10.2 erweitern; Zeitereignisse aus den Falldaten
     (`leben: [{ zeit: 410, tu: "flur:rettung" }, …]`); Schalter „Bewegung" im Menü; reduced-motion.
   - Stand der Schicht: oben die dramatische Frage mit Frist, darunter höchstens drei Sätze (kein Pflichtfragen-Zähler).
   - `web/spiel.js`: Wagen-Schirm dunkel bis zum Schreiben (§8.2); Kapitel 2 Zentrale mit Namen, Aufgabe „Monitor
     gegen Papier" (§9), technischer Alarm Bett 3 (bis Kapitel 2 als Fall `monitor` migriert ist).
4. **Falldaten** `web/faelle/aufnahme_baum.js` neu in Takten (Dialogbäume `auftakt`, `marlene`, `herrk` (Runden),
   `tochter`, `falk` (ISBAR, Argument, Tabletten, Bett), `schluss`; Flags aus §3; Karten; `leben`-Ereignisse).
   Falks Auftritt wird ausgelöst, sobald `hat:ekg_geschrieben` gilt und entweder zwei der drei Kernkarten liegen oder
   die Uhr 07:15 erreicht hat (jede Messung rückt sie um zwei Minuten vor); fehlt ihm dann eine Zahl, schickt er zum
   Wagen (bestehende Mechanik).
5. **Texte** `text/de/aufnahme_baum.json` komplett neu (IDs nach Takten), dann `en`, `ru` mit denselben Schlüsseln
   (`tools/woerter.py`). Humanizer-Durchgang (`grep -c "—"` muss 0 bleiben).
6. **Kunst** B1–B7 (§8.3); `art/szenen/aufnahme/figuren/figuren.json` um Posen und Kopf-Polygone; `schirme.json`
   relativ zur Wagen-Ebene; `gen/kunst.py` für die neue Ebene.
7. **Prüfungen** `tools/durchlauf.mjs`: Runden-Engpässe (keine Frage überspringbar, kein Hub), Wendung mit allen drei
   Antworten und Folgen (`versprochen` bei Falk und im Schluss), Anruf jetzt/später, alle drei Antworten der Tochter,
   Rhythmusfrage vier Optionen, Zirkel wie heute, ISBAR alle Zeilen inkl. Rückwege, Argumente (Nachgeben nur mit den
   beiden tragenden; Hinweis nach vier), `heim_empfohlen`-Variante, Tabletten drei Optionen, `brady_argument`-Echo,
   Schlussgespräch alle Wege inkl. `revers`, Verdachtsliste-Endzustand, Epilog-Varianten, Wagen-Schirm dunkel vor dem
   Schreiben, Posen, reduced-motion (keine Animation, Zustände gesetzt), Kapitel 2 mit Namen und neuer Aufgabe,
   Textmaße (220/64), Gedankenstrich-Verbot, keine Lektionsnummern.
8. `docs/STAND.md`, `docs/UMBAU.md` nachziehen; Commit nach jedem Schritt.

Reihenfolge der Sitzungen (Tokensparen, CLAUDE.md): (a) Akte + Texte, (b) Motor, (c) Falldaten + Prüfungen,
(d) Kunst + Leben, (e) Kapitel 2.

---

## 12. Beleg-Tabelle

Bestehende Belege (FACHREGELN, QUELLEN §3, §8a, §9) gelten weiter; hier nur, was dieser Entwurf zusätzlich braucht
oder anders gewichtet. „neu, zu prüfen" = am 18.10.2026 per Websuche gefunden, vor dem Einbau am Original lesen.

| Aussage im Entwurf | Beleg | Status |
|---|---|---|
| Low-risk verlangt u. a. ein normales EKG und ein Prodrom typisch für Reflexsynkope; Minor-Ereignismerkmale (keine Vorwarnung / Prodrom < 10 s, Familie SCD jung, im Sitzen) gelten als hohes Risiko nur mit struktureller Herzkrankheit und/oder abnormem EKG; Minor-EKG-Merkmale nur, wenn die Anamnese zu einer arrhythmischen Synkope passt | ESC-Synkope-2018 Tab. 6 | bestehend (QUELLEN §8a), am 18.10.2026 an der adaptierten Wiedergabe (explorationpub.com, Table 1 „adapted from Brignole 2018") erneut gelesen; die Fußnote zur Bedingung ist dort ausdrücklich. **Original-PDF bleibt nachzulesen** (QUELLEN §5) |
| „AV-Block I° mit deutlich verlängerter PQ" steht in Tab. 5 (EKG-Merkmale, die eine arrhythmische Synkope nahelegen) | ESC-Synkope-2018 Tab. 5 | bestehend; am Online-Volltext 18.10.2026 gesehen |
| Tab. 7: „Syncope without prodrome" bei den Hochrisiko-Merkmalen, die für eine Überwachungseinheit der Notaufnahme / Synkopeneinheit sprechen; „Injury caused by syncope" bei denen, die für eine Aufnahme sprechen | ESC-Synkope-2018 Tab. 7, §4.1.2 | bestehend; Online-Volltext 18.10.2026: beide Begriffe vorhanden, **Spaltenzuordnung am PDF bestätigen** |
| §4.1.2: Low-risk braucht keine weiteren Tests in der Notaufnahme; High-risk „intensive diagnostische Abklärung, ggf. dringliche Behandlung und Aufnahme", Überwachung dort, wo reanimiert werden kann; „weder noch" → Überwachungseinheit / Synkopeneinheit; kein direkter Nachweis, dass die Aufnahme selbst das Ergebnis ändert | ESC-Synkope-2018 §4.1.2 | am Online-Volltext 18.10.2026 gelesen |
| §4.2.4.1: Überwachung im Haus (Bett oder Telemetrie) ist bei Hochrisiko-Merkmalen, die eine arrhythmische Synkope nahelegen, gerechtfertigt, vor allem unmittelbar nach der Synkope; Ausbeute 1,9–17,6 % | ESC-Synkope-2018 §4.2.4.1 | am Online-Volltext 18.10.2026 gelesen; Klasse/Level (Bildtabelle) nicht lesbar, QUELLEN §8a nennt Klasse I C aus früherer Sitzung |
| Stehversuch: abnorm ist ein progredienter, anhaltender Abfall des systolischen Drucks ≥ 20 mmHg oder des diastolischen ≥ 10 mmHg oder systolisch < 90 mmHg | ESC-Synkope-2018 §4.2.2.1 (nicht §4.2.1) | am Online-Volltext 18.10.2026 gelesen; QUELLEN §5 entsprechend schließen |
| Betablocker als Ursache von Sinusbradykardie und AV-Block; Bradyarrhythmien unter Medikament lassen sich durch Dosisreduktion oder Absetzen behandeln, „aber in vielen Fällen bleiben sie bestehen"; reversible Ursache vor einer Schrittmacherentscheidung ausschließen; DDD(R) erste Wahl bei Sinusknotenerkrankung, Zweikammer beim AV-Block | ESC-Pacing-2021 §3.3/Tab. 6, §5.1.1.2, §5.2.1.4, §5.1.2, §5.2.2.1 | §5.1.1.2 und §5.2.1.4 am 18.10.2026 am Online-Volltext gelesen; Rest bestehend (QUELLEN §9) |
| „Markiert" verlängert ist eine PQ-Zeit erst ab etwa 300 ms (Schrittmacher nur bei klarem Symptombezug) | ESC-Pacing-2021 §5.2.1.1 | **neu, zu prüfen**; im Spiel nur als Begründung, warum 228 ms „nicht normal", aber nicht „deutlich verlängert" heißt |
| AV-Block unter bremsenden Medikamenten: nach Absetzen Rezidiv in 56 % binnen drei Wochen, nur 15 % echte medikamentöse Ursache (Zeltser 2004, n = 169); Deutung „drug-revealed" | Review PMC12246518 (2025), dort zitiert: Zeltser D et al., J Am Coll Cardiol 2004 | **neu, nur Hintergrund**, kommt nicht ins Spiel; stützt, dass die Pause im Epilog nach Auswaschen zum Schrittmacher führt |
| Bisoprolol-Halbwertszeit 10–12 h; nach rund 65 h (zweite Nacht) mehr als fünf Halbwertszeiten | Pharmakologie-Standardwissen (QUELLEN §9) | bestehend, Rechnung neu |
| Ramipril und ASS weitergeben | klinische Entscheidung des Oberarztes im Spiel; keine Leitlinienaussage | keine Behauptung; ärztliche Freigabe des Nutzers |
| Arrhythmie-Monitoring bei Synkope mit vermuteter kardialer Ursache mindestens 24 h bzw. bis zur Klärung (Klasse I, Level B); Alarmmanagement (Grenzen patientenbezogen anpassen) | AHA-2017 Praxisstandards ECG-Monitoring (Sandau KE et al., Circulation 2017;136:e273, doi:10.1161/CIR.0000000000000527) | **neu, zu prüfen**; Volltext am 18.10.2026 nicht abrufbar (403), Inhalt nur aus Sekundärquellen; vor dem Einbau der Alarmgrenze lesen (§9.2) |
| ISBAR (Identifikation, Situation, Hintergrund, Einschätzung, Empfehlung) als Übergabestandard | Kommunikationsstandard, keine medizinische Aussage; optional WHO Patient Safety Solutions 2007 („Communication During Patient Hand-Overs") | **neu, optional** |
| Verschwiegenheit: Was der Patient sagt, geht nicht ohne sein Einverständnis an Angehörige; Studierende in der Famulatur sind gebunden | ÄrzteG 1998 §54 (Österreich), sinngemäß | **neu, zu prüfen** (Reichweite für Studierende); keine medizinische Aussage |
| Pflege-Nachtdienst 19:00–07:00; Frühbesprechung dreiviertel acht; Triage nach Manchester, Synkope ohne Warnzeichen Gelb | Hausüblichkeit | **beim Nutzer prüfen**, keine Quelle nötig |
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
| Rückmeldung zur Verschwiegenheit (ÄrzteG §54) im Spiel | **Ja**, in einem Satz ohne Paragraph im Spieltext; Reichweite für Studierende vom Nutzer bestätigen. |
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
- **H3 Frist ohne Zähne** · §3 Takt 1 „Frist (Falk, 07:15)", §11.4 Falk erst nach `hat:ekg_geschrieben` · Vor dem
  EKG kostet nichts Zeit, also drückt die Frist nie. · Mittel: jede Frage und jede Handlung rückt die Uhr um eine
  Minute vor; um 07:15 kommt Falk in jedem Fall. Ist das EKG noch nicht geschrieben, wartet er am Tresen
  („Schreiben Sie. Ich les solang.") und die Übergabe beginnt danach mit weniger Zeit.
- **H7 Fehlendes Sequel** · 5.6 Marlene „dreht sich um, als die Spielerin vorbeigeht" · Takt 3 (Reaktion,
  Dokumentation, „sag's dem Falk als Erstes") hängt an einem Weg, den man nicht gehen muss. · Mittel: fester Engpass
  nach der Untersuchung. Marlene schiebt den Wagen selbst an die Koje („Da. Ich übergeb.") und fragt dabei
  „Und? Darf er?".
- **H5 doppelte Entscheidung** · 6.2 R „Er bleibt. Monitor. Und das Bisoprolol heute nicht." und 6.4 Tabletten ·
  Dieselbe Behandlungswahl fällt zweimal; die zweite ist dann keine Wahl mehr. · Mittel: R ohne Bisoprolol („Er
  bleibt. Monitor."); die Tabletten bleiben allein in 6.4.
- **IF5 / atemlose Szene** · §6 Takt 6: ISBAR mit 3–4 Wahlen, Gegenrede mit bis zu acht Argumenten, Tabletten,
  Bett, in einem Stück · Zwölf Minuten Menü ohne Atempause; der Höhepunkt wird zur Abfrage. · Mittel: ein stummer
  Handlungstakt nach der A-Zeile. Falk legt seinen Messingzirkel an den Streifen und misst selbst nach („Zweihundertzwanzig,
  zweihundertdreißig. Ja."). Das gibt der Messung der Spielerin ihre Bestätigung von außen und setzt Falks Gegenstand
  ein (ART_BIBLE §5).
- **Wendung überbewertet** · §2.3 „kippt die Notiz … in nicht mehr zu halten" · Fachlich kippt die Notiz erst
  mit dem EKG (keine Vorwarnung + nicht normal, §2.2); das zweite Ereignis stützt nur, und die Viertelstunde Stehen
  spricht sogar für Reflex. Erzählt man die Wendung als Kipppunkt, lernt die Spielerin „zweimal = gefährlich". ·
  Mittel: §2.3 und Falks Reaktion („Hm.") als Einsatzerhöhung formulieren (die Notiz kannte nur die halbe Geschichte);
  der fachliche Kipppunkt bleibt die PQ-Zeit in Takt 4.
- **E5 Pointe am Schluss** · 7.1 Spielerin: „Deshalb der Monitor, nicht die Haltestelle." · Die Spielerin spricht
  die Lehre als Pointe aus. · Mittel: den Satz streichen; „Heute wissen wir's nicht." reicht, dann die Senta.
- **Flag ohne Tabelle** · 5.7 `anruf_spaeter` · fehlt in der Flag-Tabelle §3. · Mittel: eintragen (Folge: Sabine
  ruft nach dem Streifen, „Ich hab dreimal angerufen.").

Kein Befund zu H1, H2, H4, H6, H8 und zu Ende/Epilog (eine Folge, belegt, Verdachtsliste schließt mit
„Bewiesen.", kein Lebenslauf).
