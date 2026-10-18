# Krankenhaus zuerst — Idee des Nutzers (18.10.2026)

Status: **Idee, festgehalten, noch nicht ausgearbeitet.** Ausarbeitung in einem eigenen Chat (unten „Nächster
Schritt"). Nichts davon ist gebaut.

## Anlass (Wortlaut des Nutzers, sinngemäß übersetzt)

Nach dem spielbaren Prototyp von Fall 1: „Das ist alles schön, aber trotzdem unverständlich. Ich will zuerst das
Krankenhaus als Ganzes bauen: Patientenzimmer, Flure, den Lehrsaal, überhaupt eine bestimmte Abteilung, ein eigenes
Gebäude, in dem alle Ereignisse spielen. Gleich am Anfang erklären, was wir lernen und wie es ablaufen wird, und
dazu einen Flug machen: hier ist die Abteilung, hier die Zimmer. Und natürlich ein 3D-Modell des Krankenhauses,
dessen Räume wir dann im Spiel verwenden."

## Was das lösen soll

- **Orientierung:** Die Spielerin weiß von der ersten Minute an, wo sie ist, was sie hier lernt und wie das Spiel
  abläuft. Heute beginnt das Spiel mitten in der Aufnahme, ohne Rahmen; das ist ein Teil des „unverständlich".
- **Ein Ort für alles:** Alle Kapitel spielen in einem Haus. Wege werden räumlich nachvollziehbar (Aufnahme im
  Erdgeschoss → Herr Baum fährt „nach oben" → Monitorzimmer), Figuren treffen sich wieder.
- **Ein Modell, viele Räume:** Ein 3D-Gesamtmodell liefert alle Raumbilder mit gleichem Maßstab, gleichem Licht und
  gleichem Stil (ART_BIBLE, ligne claire). Die heutigen Einzelszenen (`gen/blender/szene_aufnahme.py`,
  `szene_monitor.py`, `szene_lehrsaal.py`) werden Räume dieses Hauses.

## Bausteine (Vorschlag des Koordinators, alles zu entscheiden)

1. **Das Haus.** Ein fiktives Krankenhaus (kein echtes Haus, kein Logo, kein echter Name), ein eigenes Gebäude der
   Inneren Medizin mit Kardiologie. Die Räume aus KONZEPT §3 bekommen einen Ort, z. B.:
   - Erdgeschoss: Eingang, Rettungszufahrt, Notaufnahme/Aufnahme (Kapitel 1);
   - 1. Stock: kardiologische Station mit Patientenzimmern (Kapitel 3) und Monitorzimmer/Überwachung (Kapitel 2),
     Stationsstützpunkt, Dienstzimmer;
   - 2. Stock: Intensivstation (Kapitel 4), Herzkatheterlabor und Chest Pain Unit (Kapitel 5);
   - Ambulanzbereich: Rhythmusambulanz (Kapitel 6);
   - Lehrsaal (Kapitel 0), Befundraum/Arztzimmer (Finale), Aufenthaltsraum oder Cafeteria (nur Atmosphäre).
2. **3D-Modell** in der Blender-Pipeline (`gen/blender/`): zuerst ein Blockout des ganzen Gebäudes mit Grundriss
   je Stock, Fluren, Treppenhaus und Lift; jeder Spielraum ist eine Kamera im selben Modell. Grundrisslogik nach
   einem echten österreichischen Haus (der Nutzer ist die Quelle), aber ohne Wiedererkennbarkeit.
3. **Einführung mit Flug.** Spielbeginn: das Haus von außen im Morgenlicht → Eingang → Flur → Station → Zimmer.
   Dazu in wenigen Sätzen: **was** wir lernen (EKG lesen an echten Aufnahmen), **wie** es abläuft (eine Rotation
   über mehrere Dienste, jeder Fall ein Patient, messen mit dem Zirkel, Befundmappe, Verdachtsliste) und **wo**
   (dieses Haus). Der Flug endet im Lehrsaal am Einschulungstag (KONZEPT §3, Kapitel 0, Dr. Wieser).
   Technik, nach Größe der Einzeldatei: (a) Kamerafahrt als Folge weniger Standbilder mit Überblendung und
   Parallaxe (klein, einzeldateitauglich); (b) echtes Video nur in der gehosteten Fassung (TON.md §3);
   (c) dazu ein **Querschnitt des Hauses** (Puppenhaus-Schnitt), der im Spiel bleibt.
4. **Lageplan im Spiel.** Der Querschnitt als Knopf „Haus" in der Kopfleiste: wo bin ich, welche Räume sind offen,
   welcher Dienst ist heute. Er macht die Kapitelfolge sichtbar.

## Folgen für den Bestand

- **Reihenfolge:** Haus-Konzept und Gebäudemodell kommen vor dem Umbau von Fall 1. Der neue Aufnahme-Render (B1 in
  `docs/REDESIGN_FALL1.md` §8.3: Koje, Glastür, Wagen als eigene Ebene) entsteht dann als Raum dieses Hauses.
- **Gilt weiter:** KONZEPT §1 (Grundsätze) und §2 (Rotation über mehrere Dienste); ART_BIBLE §4 (Tageszeiten) für
  das ganze Haus; der Redesign-Entwurf von Fall 1 als Inhalt der Aufnahme.
- **Farbpalette** (Merkzettel in STAND.md) am Haus mit ausprobieren: Außenansicht, Flur, Zimmer.
- **Lehrsaal** (halb fertig) wird ein Raum im Haus; der Einschulungstag knüpft an den Flug an.

## Offene Fragen an den Nutzer

1. Welche Abteilung genau (Innere Medizin mit Kardiologie und eigener Notaufnahme, oder eine reine Kardiologie)?
2. Name des Hauses (fiktiv) und Stadt (Graz als Kulisse, aber ohne echtes Krankenhaus)?
3. Flug: Bildfolge in der Einzeldatei oder Video in der gehosteten Fassung; Länge etwa 30 bis 60 Sekunden?
4. Wer führt ein: Erzähler, Dr. Wieser oder Marlene?
5. Wie viel vom Haus ist begehbar: nur die Spielräume oder auch Flure zum Hin- und Hergehen?

## Nächster Schritt (eigener Chat)

Fable (3D und Raumprogramm, CLAUDE.md „Modellwahl"): diese Datei zu einem Konzept ausarbeiten (Raumprogramm,
Grundriss je Stock, Wege der Kapitel, Einführungstext, Drehbuch des Flugs, Lageplan), dann ein Blender-Blockout
des Gebäudes und zwei Probe-Renders in niedriger Qualität (Außenansicht im Morgenlicht, ein Flur). Erst nach
Freigabe durch den Nutzer werden Räume ausgebaut.
