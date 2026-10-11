# Bildaufträge — was genau bei Recraft bestellt wird

Zwei Schritte. Der erste ist der wichtigere.

## Schritt 1 · Einen eigenen Stil anlegen

Recraft kann aus Beispielbildern einen Stil lernen („Stil erstellen"). Genau
das brauchen wir, denn das Problem ist nicht ein schönes Bild, sondern **sechs
Bilder, die zusammengehören**. Ohne eigenen Stil sehen sie aus wie sechs
verschiedene Stockbilder.

Als Vorlagen dienen die Risograph-Studien aus `art/A_riso_*.png`. Der Stil
bekommt den Namen **„Nachtdienst Riso"**, und alles Weitere wird nur noch in
diesem Stil bestellt.

## Schritt 2 · Die sechs Räume

Jeder Auftrag hat denselben Bau:

```
<Stil> · <Raum, Blickwinkel> · <Licht> · <Farben> · <Verbote>
```

Die letzte Zeile steht in **jedem** Auftrag, wörtlich:

> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

Keine Schrift, weil jeder Text im Spiel vom Code gesetzt wird — gemalte
Buchstaben sind das sicherste Erkennungszeichen für ein KI-Bild. Keine
EKG-Kurven, weil alle Kurven aus echten Aufnahmen kommen; eine gemalte Zacke
ist medizinisch falsch. Keine Menschen, weil die Figuren eigene Ebenen sind und
sich bewegen müssen.

---

### 1 · Aufnahme — 06:40, Sonnenaufgang

> hand-inked risograph print, visible halftone dots, paper grain, slight
> misregistration · hospital admissions room seen from inside, three-quarter
> view, reception counter on the left, row of waiting chairs on the right ·
> low morning sun through venetian blinds, long warm light shafts across the
> floor, one bright pool of light on the right, deep shadow on the left ·
> dark doorframe cutting into the left edge of the frame, out of focus ·
> cream paper #F4E6D2, petrol ink #10212B, amber #E8A33D ·
> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

### 2 · Monitorzimmer — 09:15, kühler Vormittag

> hand-inked risograph print, visible halftone dots, paper grain · hospital
> monitoring room, wall of screens of different sizes mounted at different
> heights, long desk below, swivel chair · flat cool daylight from a window on
> the left, screens pale in the daylight, no strong shadows · back of a chair
> cutting into the bottom-left corner, very dark · cream paper #F4E6D2, petrol
> ink #10212B, phosphor green #39E58C only on screens ·
> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

### 3 · Station — 13:30, Mittag

> hand-inked risograph print, visible halftone dots, paper grain · hospital ward
> corridor with three open patient room doors, linoleum floor, handrail along
> the wall · flat midday light from a window at the far end, dust in the air,
> short hard shadows · a laundry cart in the near foreground, dark and slightly
> blurred · cream paper #F4E6D2, petrol ink #10212B, amber #E8A33D ·
> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

### 4 · Intensivstation — 18:50, Abendrot

> hand-inked risograph print, visible halftone dots, paper grain · intensive
> care bay, one bed with equipment around it, ventilator, infusion stands,
> cables ordered and taut · low evening sun through a large window, long red-
> amber shadows stretching across the floor, the bed in the light · infusion
> stand in the near foreground, almost black · cream paper #F4E6D2, petrol ink
> #10212B, amber #E8A33D, phosphor green #39E58C only on screens ·
> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

### 5 · Aufwachraum — 22:10, Nacht, Lampeninseln

> hand-inked risograph print, visible halftone dots, paper grain · hospital
> recovery room at night, two empty beds, a nurses' desk with a single lamp ·
> no daylight at all, one warm lamp pool over the desk, a second faint pool at
> the far end, everything between them dark · a curtain rail and half-drawn
> curtain in the near foreground · cream paper #F4E6D2, petrol ink #10212B,
> amber #E8A33D ·
> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

### 6 · Ambulanz / Finale — 02:14, tiefe Nacht, Regen

> hand-inked risograph print, visible halftone dots, paper grain · hospital
> emergency entrance seen from inside, large glass doors, wet reflections on
> the floor · deep night, rain on the glass, cold light from outside, a single
> warm lamp inside, strong contrast · a wheelchair in the near foreground, very
> dark, cutting into the lower right · cream paper #F4E6D2, petrol ink #10212B,
> amber #E8A33D ·
> no text, no letters, no numbers, no signage, no ECG traces or waveforms on any
> screen, no people, 16:9

---

## Woran ein Bild gemessen wird, bevor es ins Spiel kommt

Durchgehen, bevor etwas übernommen wird. Fällt ein Punkt durch, wird das Bild
neu gemacht, nicht die Regel geändert.

1. **Gestufte Tonwerte**: Boden und Möbel dunkler als die Wand, helle Insel dort,
   wo das Wichtige liegt. Kein angeschnittener dunkler Vordergrund.
2. **Die Lichtquelle ist im Bild** — Fenster, Lampe, Tür. Kein Licht aus dem Nichts.
3. **Keine Schrift**, nirgends, auch nicht verschwommen im Hintergrund.
4. **Keine gemalte EKG-Kurve**, kein Zackenmuster auf irgendeinem Schirm.
5. **Höchstens ein Magenta-Objekt** — und nur, wenn es die Geschichte weitertreibt.
6. **Keine Requisite ohne Besitzer.** Jedes Ding gehört jemandem oder hat einen Grund.
7. **16:9**, weil die Bühne 1600 × 900 ist.

## Danach

Das fertige Bild wird in drei Ebenen zerlegt (Hintergrund, Mittelgrund, Figuren),
damit die Parallaxe funktioniert. Figuren kommen **nicht** aus
Recraft: sie bleiben gezeichnet, weil dieselbe Person in sechs Bildern sechs
verschiedene Menschen würde — das ist der sicherste Weg, dass ein Spiel nach
Maschine aussieht.
