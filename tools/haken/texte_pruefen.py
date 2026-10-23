# -*- coding: utf-8 -*-
"""Hook nach jeder Bearbeitung (PostToolUse auf Edit|Write|MultiEdit).

Liest die Hook-Daten von stdin und prüft nur, wenn eine Datei unter text/ oder web/ geändert wurde:
  · Sprachdatei text/<de|en|ru>/<fall>.json: gültiges JSON, kein Gedankenstrich, deutsche Repliken
    höchstens 230 Zeichen (Bildschirmmaß, wie tools/durchlauf.mjs; Karten und Antwortknoten ausgenommen);
  · IDs wie tools/woerter.py: jede ID im Code hat einen deutschen Text, jede deutsche ID hat en und ru
    mit denselben Platzhaltern, keine ID in en/ru ohne deutsches Gegenstück.
Mängel gehen auf stderr mit Ausgang 2, dann sieht Claude sie sofort. Sonst still, Ausgang 0.

Von Hand:  echo '{"tool_input":{"file_path":"text/de/aufnahme_baum.json"}}' | python3 tools/haken/texte_pruefen.py
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WURZEL, "tools"))

MAX_REPLIK = 230
KEINE_REPLIK = re.compile(r'\.(karte|a|f)\.')
ZEIGEN = 8


def geaenderte_datei():
    try:
        daten = json.load(sys.stdin)
    except ValueError:
        return None
    eingabe = daten.get("tool_input") or {}
    pfad = eingabe.get("file_path") or (daten.get("tool_response") or {}).get("filePath")
    if not pfad:
        return None
    return os.path.relpath(os.path.abspath(os.path.join(WURZEL, pfad)), WURZEL)


def pruefe_sprachdatei(pfad, maengel):
    m = re.match(r'text/(de|en|ru)/[^/]+\.json$', pfad)
    if not m:
        return True
    try:
        with open(os.path.join(WURZEL, pfad), encoding="utf-8") as f:
            tisch = json.load(f)
    except ValueError as e:
        maengel.append(f"{pfad}: kein gültiges JSON ({e})")
        return False
    striche = [k for k, v in tisch.items() if isinstance(v, str) and "—" in v]
    if striche:
        maengel.append(f"{pfad}: Gedankenstrich in {len(striche)} Texten: " + ", ".join(striche[:ZEIGEN]))
    if m.group(1) == "de":
        lang = [f"{k} ({len(v)})" for k, v in tisch.items()
                if isinstance(v, str) and len(v) > MAX_REPLIK and not KEINE_REPLIK.search(k)]
        if lang:
            maengel.append(f"Repliken über {MAX_REPLIK} Zeichen: " + ", ".join(lang[:ZEIGEN]))
    return True


def pruefe_ids(maengel):
    import woerter
    de = woerter.lies_ids("de")
    benutzt = woerter.ids_im_code()
    ohne_text = sorted(benutzt - set(de))
    if ohne_text:
        maengel.append(f"{len(ohne_text)} IDs im Code ohne deutschen Text: " + ", ".join(ohne_text[:ZEIGEN]))
    for sprache in ("en", "ru"):
        tisch = woerter.lies_ids(sprache)
        fehlt = [k for k in de if not tisch.get(k)]
        extra = [k for k in tisch if k not in de]
        falsch = [k for k in de if tisch.get(k) and
                  set(re.findall(r'\{\w+\}', de[k])) != set(re.findall(r'\{\w+\}', tisch[k]))]
        if fehlt:
            maengel.append(f"{sprache}: {len(fehlt)} IDs fehlen: " + ", ".join(fehlt[:ZEIGEN]))
        if extra:
            maengel.append(f"{sprache}: {len(extra)} IDs ohne deutsches Gegenstück: " + ", ".join(extra[:ZEIGEN]))
        if falsch:
            maengel.append(f"{sprache}: {len(falsch)} IDs mit anderen Platzhaltern: " + ", ".join(falsch[:ZEIGEN]))


def main():
    pfad = geaenderte_datei()
    if not pfad or not re.match(r'(text|web)/', pfad):
        return 0
    maengel = []
    if pruefe_sprachdatei(pfad, maengel):
        pruefe_ids(maengel)
    if not maengel:
        return 0
    print("Textprüfung nach " + pfad + ":\n  · " + "\n  · ".join(maengel), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
