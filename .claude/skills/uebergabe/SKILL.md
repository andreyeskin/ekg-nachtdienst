---
name: uebergabe
description: Einen Arbeitsblock von „Nachtdienst" sauber abschließen und an den nächsten Chat übergeben — prüfen, committen, pushen, docs/STAND.md nachziehen (Fertig, Offen, Nächster Auftrag) und eine Startnachricht schreiben, mit der ein neuer Chat ohne Vorwissen weiterarbeitet. Laden, wenn ein Block fertig ist, das Thema wechselt, der Chat lang oder schon zusammengefasst ist, oder wenn der Nutzer „Übergabe", „neuer Chat", „abschließen", „передача", „новый чат" sagt.
---

# Übergabe an den nächsten Chat

Ziel: Der neue Chat braucht **nur die Startnachricht**. Alles Wissen steht danach im Repository, nichts
mehr nur im alten Chat. Regeln dazu stehen in CLAUDE.md („Tokensparen"); dieser Skill ist der Ablauf.

## 1. Aufräumen

- Laufende Hintergrund-Agenten und -Befehle stoppen oder ihr Ergebnis abwarten und einarbeiten.
- `git status --short`: Halbfertiges entweder fertig machen oder bewusst zurücklassen und unter „Offen" in
  STAND.md beschreiben (Datei, was fehlt). Arbeitskopien unter `.claude/worktrees/` nur entfernen, wenn ihr
  Branch gemergt oder verworfen ist.

## 2. Prüfen (nur wenn Spielcode, Texte oder Bilder geändert wurden)

```
python3 gen/kunst.py && python3 tools/baue.py && node tools/durchlauf.mjs "$PWD/bau/nachtdienst.html" "$PWD/bau/durchlauf" 2>&1 | grep -E "FEHL|bestanden"
```

Erwartet: „Alle Prüfungen bestanden." Rote Zeilen nicht verschweigen: beheben oder unter „Offen" eintragen.
Prototypen haben eigene Prüfungen (`node prototyp/fall1/pruefe.mjs`, `node prototyp/bewegung/schuss.mjs …`).

## 3. Committen und pushen

Ein Commit je Teilschritt, deutsche Betreffzeile im Stil der vorhandenen („Bereich: was"), dann
`git push`. Nichts aus dem Lehrbuch (Trappe) und nichts aus `ISABEL/` ins Repository.

## 4. docs/STAND.md nachziehen

Kopfzeile: `# Stand und Übergabe — <TT.MM.JJJJ>` mit heutigem Datum.

1. **Fertig** — neuen Abschnitt `## Fertig (<Datum>): <Block in wenigen Worten>` **oben** einfügen
   (neueste zuerst). Je Ergebnis ein Punkt: was, wo (Dateipfad), wie man es aufruft oder prüft. Keine
   Erzählung des Wegs, keine Wiederholung dessen, was in den verlinkten Dateien steht.
2. **Offen** — bekannte Mängel, offene Fragen an den Nutzer (wörtlich, nummeriert), halbfertige Dateien.
   Erledigtes aus älteren „Offen"-Listen streichen.
3. **Nächster Auftrag** — den alten Abschnitt ersetzen, nicht einen zweiten anlegen. Ein Arbeitsblock,
   der in einen Chat passt. Bei mehreren Möglichkeiten die empfohlene zuerst, die anderen in einer Zeile.
4. **Länge** — STAND.md bleibt Einstieg, kein Archiv. Über etwa 300 Zeilen: ältere „Fertig"-Abschnitte
   auf zwei, drei Zeilen kürzen; Einzelheiten stehen in den Fachdokumenten (KRANKENHAUS, REDESIGN_FALL1 …).

## 5. Startnachricht schreiben

Unter „Nächster Auftrag" als `### Startnachricht` im Codeblock. Muster:

```
Arbeite lokal auf meinem Mac im Repository andreyeskin/ekg-nachtdienst, Branch claude/stil-ligne-claire.
Lies docs/STAND.md (Abschnitt „Nächster Auftrag"), dann <nur die nötigen Dateien, mit Abschnitt>.
<Bilder nur nennen, wenn nötig, „verkleinert ansehen">
Auftrag: <ein Satz>
1. …
2. …
Prüfung: <Befehl oder Prüfweg>. <Modellwahl nach CLAUDE.md, z. B. 3D als Subagent auf Fable>.
Commit nach jedem Teilschritt, pushen, STAND.md nachziehen. Antworte mir auf Russisch.
```

Prüffragen vor dem Abschicken: Versteht ein Chat ohne Vorwissen jeden Begriff? Sind alle Dateien mit Pfad
und Abschnitt genannt, aber keine auf Vorrat? Ist klar, wann der Block fertig ist? Stehen offene Fragen,
die zuerst geklärt werden müssen, ausdrücklich drin?

## 6. Abschließen

- STAND.md committen („STAND: <Block> fertig, nächster Auftrag mit Startnachricht") und pushen.
- Dem Nutzer auf Russisch antworten: was fertig ist (zwei, drei Sätze), was offen ist, dann die
  Startnachricht im Codeblock zum Kopieren und der **Token-Tipp**: neuen Chat öffnen, Nachricht einfügen;
  den alten Chat kann er schließen oder archivieren (archivieren nur auf seinen Wunsch). Im alten Chat
  nichts Neues mehr anfangen.
