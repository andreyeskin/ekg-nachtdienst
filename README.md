# Nachtdienst — EKG-Lernspiel

Interaktives Lernspiel zum EKG: eine Schicht, ein Patient, echte Kurven.
Alle EKG-Streifen stammen aus offenen, frei lizenzierten Datenbanken und werden auf
echtem Millimeterpapier gezeichnet (25/50 mm/s, 10 mm/mV, Eichzacke).

## Ordner

```
engine/   EKG-Modell, Messung aus Experten-Annotationen, SVG-Rendering (Python)
web/      EKG-Renderer fürs Spiel (Canvas, Millimeterpapier, Messzirkel, Monitor-Modus)
data/     aufbereitete Aufnahmen (LUDB-Auszug) und Auswahl-Index für PTB-XL
art/      Stilstudien und Szenen-Entwürfe
tools/    Hilfsskripte (PTB-XL-Auswahl, Screenshot-Renderer)
docs/     ART_BIBLE.md (Bildregeln) und GAME_DESIGN.md (Spielkonzept)
```

## Daten besorgen

Die Rohdatenbanken liegen bewusst nicht im Repository.

```bash
# LUDB (14 MB) — 200 Aufnahmen mit manuell markierten P/QRS/T-Grenzen
#   https://physionet.org/content/ludb/1.0.1/

# PTB-XL (nur 100-Hz-Teil, ca. 600 MB) — 21 799 Aufnahmen mit Befunden
aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/records100/ records100/
aws s3 cp   --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ptbxl_database.csv .
aws s3 cp   --no-sign-request s3://physionet-open/ptb-xl/1.0.3/scp_statements.csv .

python3 tools/ptbxl_auswahl.py /pfad/zu/ptb-xl   # zieht die Fälle für das Spiel heraus
```

## Stand

- EKG-Engine fertig: Laden, Messen, Rendern auf Millimeterpapier, Export fürs Web.
- Browser-Renderer fertig: Papier- und Monitormodus, laufende Kurve, Messzirkel.
- 458 Aufnahmen aus PTB-XL ausgewählt, darunter 14× AV-Block II° und 16× AV-Block III°.
- Stil entschieden (siehe docs/ART_BIBLE.md), Szenen-Entwürfe in art/.
- Als Nächstes: Szenen-Engine (Räume, Figuren, Dialoge, Inventar) und Kapitel 1.

## Rechtliches

Siehe ATTRIBUTION.md. Keine Inhalte aus urheberrechtlich geschützten Lehrbüchern.
Lernsoftware — kein Medizinprodukt, nicht für klinische Entscheidungen.
