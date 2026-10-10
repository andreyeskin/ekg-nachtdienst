#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTB-XL → kleine Auswahl für den EKG-Kurs / das Spiel.

Was das Skript tut
------------------
Liest die PTB-XL-Metadaten, sucht pro Rhythmus-/Überleitungsbefund eine Handvoll
Aufnahmen heraus (die Befunde aus Lektion 7–12) und kopiert NUR diese Datensätze
in einen neuen Ordner (100-Hz-Version, klein). Am Ende liegt ein ZIP bereit,
das man problemlos in den Chat hochladen kann.

Vorbereitung
------------
1. PTB-XL laden (kein Account nötig, CC BY 4.0):
     https://physionet.org/content/ptb-xl/1.0.3/
   Entweder das ZIP (1,7 GB) oder:
     wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/
2. Python-Pakete:
     pip install pandas
3. Starten (Pfad = Ordner mit ptbxl_database.csv):
     python3 ptbxl_auswahl.py /pfad/zu/ptb-xl-1.0.3

Ergebnis: ptbxl_auswahl/ + ptbxl_auswahl.zip  (ca. 20–60 MB)
"""
import ast
import os
import shutil
import sys
import zipfile

import pandas as pd

# SCP-Codes von PTB-XL → unsere Themen (Lektionen 7–12)
GRUPPEN = {
    "SR":     ("Sinusrhythmus (Referenz/Normalfall)", 30),
    "SBRAD":  ("Sinusbradykardie", 20),
    "STACH":  ("Sinustachykardie", 20),
    "SARRH":  ("Sinusarrhythmie", 20),
    "1AVB":   ("AV-Block I°", 25),
    "2AVB":   ("AV-Block II°", 25),
    "3AVB":   ("AV-Block III° (totaler AV-Block)", 25),
    "SVARR":  ("supraventrikuläre Arrhythmie", 10),
    "PACE":   ("Schrittmacher (zum Abgrenzen)", 8),
    "AFIB":   ("Vorhofflimmern (für später)", 15),
    "AFLT":   ("Vorhofflattern (für später)", 10),
    "LVH":    ("Linkshypertrophie — P-sinistroatriale wahrscheinlich", 15),
    "RVH":    ("Rechtshypertrophie — P-dextroatriale wahrscheinlich", 15),
}
ABTASTUNG = "records100"          # 100 Hz reicht für Darstellung und ist klein


def main(wurzel):
    meta_pfad = os.path.join(wurzel, "ptbxl_database.csv")
    if not os.path.isfile(meta_pfad):
        sys.exit(f"ptbxl_database.csv nicht gefunden in {wurzel}")
    df = pd.read_csv(meta_pfad, index_col="ecg_id")
    df["scp_codes"] = df["scp_codes"].apply(ast.literal_eval)

    ziel = os.path.join(os.getcwd(), "ptbxl_auswahl")
    os.makedirs(ziel, exist_ok=True)
    zeilen, fehlend = [], 0

    for code, (titel, anzahl) in GRUPPEN.items():
        treffer = df[df["scp_codes"].apply(lambda d: code in d)]
        # sichere Fälle zuerst: hohe Wahrscheinlichkeit, von Kardiologen validiert
        treffer = treffer.assign(sicherheit=treffer["scp_codes"].apply(lambda d: d.get(code, 0)))
        treffer = treffer[treffer["validated_by_human"] == True] if "validated_by_human" in treffer else treffer
        treffer = treffer.sort_values("sicherheit", ascending=False).head(anzahl)
        for ecg_id, zeile in treffer.iterrows():
            basis = zeile["filename_lr"] if "filename_lr" in zeile else None
            if not basis:
                continue
            quelle = os.path.join(wurzel, basis)
            if not (os.path.isfile(quelle + ".hea") and os.path.isfile(quelle + ".dat")):
                fehlend += 1
                continue
            unterordner = os.path.join(ziel, ABTASTUNG)
            os.makedirs(unterordner, exist_ok=True)
            for endung in (".hea", ".dat"):
                shutil.copy2(quelle + endung, os.path.join(unterordner, os.path.basename(basis) + endung))
            zeilen.append({
                "ecg_id": ecg_id, "gruppe": code, "beschreibung": titel,
                "datei": os.path.basename(basis), "alter": zeile.get("age"), "geschlecht": zeile.get("sex"),
                "herzachse": zeile.get("heart_axis"), "bericht": str(zeile.get("report"))[:200],
                "scp": str(zeile["scp_codes"]),
            })
        print(f"{code:6s} {titel:45s} {len(treffer):3d} Aufnahmen")

    aus = pd.DataFrame(zeilen)
    aus.to_csv(os.path.join(ziel, "auswahl.csv"), index=False)
    for extra in ("scp_statements.csv",):
        p = os.path.join(wurzel, extra)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(ziel, extra))
    with open(os.path.join(ziel, "QUELLE.txt"), "w", encoding="utf-8") as f:
        f.write("Auszug aus PTB-XL 1.0.3 (Wagner et al., PhysioNet), Lizenz CC BY 4.0.\n"
                "https://physionet.org/content/ptb-xl/1.0.3/\n")

    zip_pfad = os.path.join(os.getcwd(), "ptbxl_auswahl.zip")
    with zipfile.ZipFile(zip_pfad, "w", zipfile.ZIP_DEFLATED) as z:
        for ordner, _, dateien in os.walk(ziel):
            for d in dateien:
                voll = os.path.join(ordner, d)
                z.write(voll, os.path.relpath(voll, os.path.dirname(ziel)))
    mb = os.path.getsize(zip_pfad) / 1e6
    print(f"\nFertig: {len(aus)} Aufnahmen · {zip_pfad} ({mb:.1f} MB)"
          + (f" · {fehlend} Dateien fehlten" if fehlend else ""))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
