# Quellen und Lizenzen

## EKG-Daten

**LUDB — Lobachevsky University Electrocardiography Database v1.0.1**
200 Aufnahmen, 12 Ableitungen, 500 Hz, mit von Kardiologen markierten P-, QRS- und T-Grenzen.
Lizenz: Open Data Commons Attribution License v1.0.
Kalyakulina A., Yusipov I., Moskalenko V. et al., PhysioNet.
https://physionet.org/content/ludb/1.0.1/

**PTB-XL v1.0.3**
21 799 Aufnahmen, 12 Ableitungen, 100/500 Hz, mit ärztlichen Befunden (SCP-Codes).
Lizenz: Creative Commons Attribution 4.0 (CC BY 4.0).
Wagner P., Strodthoff N., Bousseljot R.-D. et al., PhysioNet.
https://physionet.org/content/ptb-xl/1.0.3/

**Chapman-Shaoxing/Ningbo — A large scale 12-lead electrocardiogram database for arrhythmia study v1.0.0**
12 Ableitungen, je 10 s, mit ärztlichen Diagnosen (SNOMED-codiert), ohne Wellen-Annotation.
Lizenz: Creative Commons Attribution 4.0 (CC BY 4.0).
Zheng J., Guo H., Chu H., PhysioNet. Originalarbeit: Zheng J. et al. (2020), Optimal Multi-Stage
Arrhythmia Classification Approach, Scientific Reports 10.
https://physionet.org/content/ecg-arrhythmia/1.0.0/
(Export vorbereitet in gen/export_chapman.py; derzeit stammen alle Kurven im Spiel aus LUDB.)

PhysioNet allgemein: Goldberger A. et al. (2000), Circulation 101(23):e215–e220.

## Grafik

Räume werden in Blender aus Code gerendert (gen/blender/, ligne claire). Figuren und Porträts
entstehen als 3D-Blockout in Blender und werden mit FLUX.1 Kontext (Black Forest Labs, über fal.ai)
nachgezeichnet und anschließend geprüft; die geprüften Quellbilder liegen in art/figuren_quelle/.
Die frühen Stilstudien in art/ (A_–D_) entstanden mit Recraft und werden im Spiel nicht verwendet.
Alle EKG-Kurven und medizinischen Darstellungen stammen nicht aus Bildmodellen, sondern aus der
Engine dieses Projekts.

## Nicht enthalten

Keine Abbildungen, Tabellen oder Textpassagen aus Lehrbüchern. Fachliche Normwerte sind
Allgemeinwissen der Medizin und werden eigenständig formuliert.

## Hinweis

Lernsoftware für Ausbildungszwecke. Kein Medizinprodukt, keine Grundlage für
Behandlungsentscheidungen.
