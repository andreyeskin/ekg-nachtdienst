/* Rätsel „Reizleitung bauen": fünf Bauteile ins Herz setzen, die Erregung
   laufen sehen und darunter die Kurve, die dazu passt.

   Die Kurve wird NIE gezeichnet. Sie wird aus echten Aufnahmen ausgewählt
   (Tabelle FAELLE, je Zeile eine LUDB-Nummer und eine Zeile Begründung).
   Gibt es für einen Bauzustand keine passende Aufnahme, wird die nächstliegende
   gezeigt und das dazugesagt — oder gar keine.

   Bedienung (docs/LEHRPLAN.md, Abschnitt 5): nur antippen — erst ein Bauteil,
   dann einen Platz im Herzen. Ziffern 1–5 wählen ein Bauteil, Tab und Eingabe
   setzen es auf einen Platz, Entf nimmt es heraus, Escape schließt.

   Das Bild (Herz, Plätze, Bahnen) kommt aus gen/kunst.py → KUNST.schemata.   */
(function (global) {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";

  var TEILE = [
    { id: "sinus", nr: 1, name: "Sinusknoten",
      platz: "oben im rechten Vorhof, wo die obere Hohlvene mündet" },
    { id: "av", nr: 2, name: "AV-Knoten",
      platz: "unten in der Vorhofscheidewand, direkt über der Klappenebene" },
    { id: "his", nr: 3, name: "His-Bündel",
      platz: "durch die Klappenebene hindurch, oben auf der Kammerscheidewand" },
    { id: "schenkel", nr: 4, name: "Tawara-Schenkel",
      platz: "rechts und links an der Kammerscheidewand entlang nach unten" },
    { id: "purkinje", nr: 5, name: "Purkinje-Fasern",
      platz: "als feines Netz unter der Innenschicht beider Kammern, von der Herzspitze aufwärts" }
  ];

  /* ------------------------------------------------------------------
     Die Zuordnung: Bauzustand → echte Aufnahme (LUDB, Ableitung II).
     `passt` prüft gegen die Daten, dass die Aufnahme zeigt, was die Zeile
     behauptet — tools/durchlauf.mjs ruft das für jede Zeile auf.          */
  var FAELLE = {
    /* Normale Anatomie → normale Leitung: P vor jedem QRS, PQ 120–200 ms, QRS < 120 ms. */
    richtig: {
      aufnahme: 119, zeige: "pq",
      begruendung: "Richtige Anatomie, normale Leitung: Sinusrhythmus, PQ 120–200 ms, QRS unter 120 ms.",
      passt: function (r) {
        return r.rhythmus === "Sinus rhythm." && !r.diagnose.length &&
               r.mess.pq >= 120 && r.mess.pq <= 200 && r.mess.qrs < 120;
      }
    },
    /* Kein Taktgeber im Vorhof → keine P-Welle. Echter Ersatzrhythmus fehlt in den Daten;
       nächstliegend: Vorhofflimmern (auch ohne P-Welle, aber unregelmäßig). */
    ohne_sinus: {
      aufnahme: 96, zeige: "r", naechstliegend: true,
      begruendung: "Kein Taktgeber im Vorhof → keine P-Welle; nächstliegende Aufnahme: Vorhofflimmern.",
      passt: function (r) { return r.rhythmus === "Atrial fibrillation." && r.mess.pq === null && r.mess.qrs < 120; }
    },
    /* Keine P-Welle und Kammer über den Muskel → Vorhofflimmern mit Linksschenkelblock. */
    ohne_sinus_breit: {
      aufnahme: 44, zeige: "qrs", naechstliegend: true,
      begruendung: "Keine P-Welle und breiter QRS → Vorhofflimmern mit komplettem Linksschenkelblock (QRS > 120 ms).",
      passt: function (r) {
        return r.rhythmus === "Atrial fibrillation." && r.mess.qrs > 120 &&
               r.diagnose.indexOf("Complete left bundle branch block.") >= 0;
      }
    },
    /* Kein Weg durch die Klappenebene → kompletter AV-Block. Unbehandelt liegt keiner vor;
       nächstliegend: AV-Block III° mit Kammerschrittmacher (breiter QRS aus dem Muskel). */
    block: {
      aufnahme: 74, zeige: "qrs", naechstliegend: true,
      begruendung: "Keine Verbindung Vorhof → Kammer → kompletter AV-Block; nächstliegende Aufnahme: AV-Block III. Grades mit Kammerschrittmacher.",
      passt: function (r) { return r.diagnose.indexOf("III degree AV-block.") >= 0 && r.mess.qrs > 120; }
    },
    /* Überleitung über Umweg → PQ > 200 ms (wie beim AV-Block I. Grades). */
    av_umweg: {
      aufnahme: 39, zeige: "pq",
      begruendung: "Verzögerte Überleitung Vorhof → Kammer → PQ über 200 ms (AV-Block I. Grades).",
      passt: function (r) { return r.mess.pq > 200 && r.mess.qrs < 120; }
    },
    /* Umweg plus Kammer über den Muskel → PQ > 200 ms und QRS > 120 ms in einer Aufnahme. */
    av_umweg_breit: {
      aufnahme: 23, zeige: "pq", marken: "qrs",
      begruendung: "Verzögerte Überleitung und Kammer über den Muskel → PQ über 200 ms und QRS über 120 ms.",
      passt: function (r) { return r.mess.pq > 200 && r.mess.qrs > 120; }
    },
    /* Schenkel fehlt oder falsch → Kammer über den Muskel → QRS > 120 ms (Linksschenkelblock). */
    schenkel: {
      aufnahme: 24, zeige: "qrs",
      begruendung: "Schenkel leitet nicht → Kammer Zelle für Zelle über den Muskel → QRS über 120 ms (kompletter Linksschenkelblock).",
      passt: function (r) {
        return r.mess.qrs > 120 && r.mess.pq <= 200 &&
               r.diagnose.indexOf("Complete left bundle branch block.") >= 0;
      }
    },
    /* Purkinje-Netz fehlt → langsame Ausbreitung in der Kammer ohne Schenkelblock-Muster.
       Ein Herz ohne Purkinje-Fasern gibt es nicht; nächstliegend: unspezifische Leitungsverzögerung. */
    purkinje: {
      aufnahme: 59, zeige: "qrs", naechstliegend: true,
      begruendung: "Langsame Ausbreitung in der Kammer → QRS über 120 ms; nächstliegende Aufnahme: unspezifische intraventrikuläre Leitungsverzögerung.",
      passt: function (r) {
        return r.mess.qrs > 120 && r.mess.pq <= 200 &&
               r.diagnose.indexOf("Non-specific intravintricular conduction delay.") >= 0;
      }
    },
    /* Kein Takt und kein Durchgang → nur ein Kammer-Ersatzrhythmus. Keine Aufnahme → kein Streifen. */
    still: {
      aufnahme: null,
      begruendung: "Keine passende echte Aufnahme → kein Streifen. Erfunden wird nichts.",
      passt: function () { return true; }
    }
  };

  /* Befundnamen der Datenbank, deutsch. Was hier fehlt, erscheint im Original. */
  var BEFUND = {
    "Sinus rhythm.": "Sinusrhythmus",
    "Sinus bradycardia.": "Sinusbradykardie",
    "Atrial fibrillation.": "Vorhofflimmern",
    "Left ventricular hypertrophy.": "linksventrikuläre Hypertrophie",
    "Left atrial hypertrophy.": "linksatriale Hypertrophie",
    "Complete left bundle branch block.": "kompletter Linksschenkelblock",
    "Complete right bundle branch block.": "kompletter Rechtsschenkelblock",
    "Non-specific intravintricular conduction delay.": "unspezifische intraventrikuläre Leitungsverzögerung",
    "III degree AV-block.": "AV-Block III. Grades",
    "UNIpolar ventricular pacing.": "Kammerschrittmacher (unipolar)"
  };

  var hof = null, herzBox = null, auflage = null, streifen = null, S = null, geo = null;
  var bau = {}, gewaehlt = null, letzter = null, lauf = 0, streifenLauf = 0;
  var ruhig = !!(global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches);

  function teil(id) { for (var i = 0; i < TEILE.length; i++) if (TEILE[i].id === id) return TEILE[i]; return null; }
  function el(name, attr) {
    var e = document.createElementNS(NS, name);
    for (var k in attr) if (attr.hasOwnProperty(k)) e.setAttribute(k, attr[k]);
    return e;
  }
  function leer() { var b = {}; TEILE.forEach(function (t) { b[t.id] = null; }); return b; }
  function teilAuf(platz) { for (var k in bau) if (bau[k] === platz) return k; return null; }

  /* ------------------------------------------------------------------ Bewerten */
  function bewerte(b) {
    var z = { gesetzt: 0 };
    TEILE.forEach(function (t) {
      if (b[t.id]) z.gesetzt++;
      z[t.id] = !b[t.id] ? "fehlt" : (b[t.id] === t.id ? "richtig" : "falsch");
    });
    if (z.av === "falsch") {
      /* Ein AV-Knoten im Vorhof, aber am falschen Platz: Umweg. Unterhalb des Vorhofs: abgeschnitten. */
      var p = geo && geo.plaetze[b.av];
      z.av = (p && p.etage === "vorhof") ? "umweg" : "abgeschnitten";
    }
    z.leitung = z.his !== "richtig" ? "block"
              : z.av === "richtig" ? "normal"
              : z.av === "umweg" ? "umweg" : "block";
    z.kammer = z.schenkel !== "richtig" ? "schenkel" : z.purkinje !== "richtig" ? "purkinje" : "schmal";
    z.ersatz = null;

    if (!z.gesetzt) z.fall = "leer";
    else if (z.sinus === "richtig") {
      if (z.leitung === "block") z.fall = "block";
      else if (z.leitung === "umweg") z.fall = z.kammer === "schmal" ? "av_umweg" : "av_umweg_breit";
      else z.fall = z.kammer === "schmal" ? "richtig" : z.kammer;
    } else if (z.his === "richtig") {
      /* Ohne Sinusknoten übernimmt ein Ersatzzentrum im Übergang zur Kammer. */
      z.ersatz = z.av === "richtig" ? "av" : "his";
      z.fall = z.kammer === "schmal" ? "ohne_sinus" : "ohne_sinus_breit";
    } else z.fall = "still";
    return z;
  }

  /* ------------------------------------------------------------------ Texte */
  function satzSinus(z) {
    return z.sinus === "fehlt"
      ? T("Es fehlt der Sinusknoten, der Taktgeber oben im rechten Vorhof.")
      : T("Der Sinusknoten sitzt nicht an seinem Platz: oben im rechten Vorhof, wo die obere Hohlvene mündet. "
        + "Ein Taktgeber an anderer Stelle ist kein Sinusknoten mehr — im Modell gibt er dort keinen Takt.");
  }

  function saetzeDurchgang(z) {
    var s = [];
    if (z.av === "fehlt") s.push(T("Ohne AV-Knoten führt kein Weg vom Vorhof zum His-Bündel."));
    if (z.av === "abgeschnitten") {
      s.push(T("Der AV-Knoten sitzt nicht im Vorhof, sondern in oder unter der Klappenebene — dort nimmt er vom Vorhof "
             + "nichts auf. Sein Platz ist unten in der Vorhofscheidewand, direkt über der Klappenebene."));
    }
    if (z.av === "umweg") s.push(T("Der AV-Knoten sitzt nicht unten in der Vorhofscheidewand."));
    if (z.his === "fehlt") s.push(T("Ohne His-Bündel kommt die Erregung nicht durch die Klappenebene."));
    if (z.his === "falsch") {
      s.push(T("Das His-Bündel sitzt nicht dort, wo es die Klappenebene durchbricht: direkt unter dem AV-Knoten, "
             + "oben auf der Kammerscheidewand."));
    }
    return s.join(" ");
  }

  function satzKammer(z) {
    if (z.kammer === "schenkel") {
      return (z.schenkel === "fehlt"
        ? T("Ohne Tawara-Schenkel fehlt der schnelle Weg an der Kammerscheidewand hinunter.")
        : T("Die Tawara-Schenkel gehören rechts und links an die Kammerscheidewand; an dieser Stelle leiten sie nichts weiter."))
        + " " + T("Die Kammern werden über den Muskel erregt, Zelle für Zelle. Das dauert: Der QRS-Komplex wird breit, über 120 ms.");
    }
    if (z.kammer === "purkinje") {
      return (z.purkinje === "fehlt"
        ? T("Die Schenkel bringen die Erregung bis zur Herzspitze. Ohne Purkinje-Fasern fehlt das feine Netz, das sie von "
          + "dort in beide Kammerwände verteilt.")
        : T("Die Purkinje-Fasern gehören als feines Netz unter die Innenschicht beider Kammern, von der Herzspitze aufwärts — "
          + "nicht an diese Stelle."))
        + " " + T("Den Rest erledigt der Muskel, Zelle für Zelle. Der QRS-Komplex wird breiter.");
    }
    return "";
  }

  function erklaere(z, m) {
    var e = { titel: "", text: "", wo: "", echt: "" };
    var ort = z.ersatz === "av" ? T("im AV-Knoten") : T("im His-Bündel");
    switch (z.fall) {
      case "leer":
        e.titel = T("Noch nichts gebaut.");
        e.text = T("Tipp ein Bauteil an, dann seinen Platz im Herzen. Die gestrichelten Kreise sind mögliche Plätze — nicht jeder ist richtig.");
        break;
      case "richtig":
        e.titel = T("Richtig gebaut: Sinusrhythmus.");
        e.text = T("Der Sinusknoten gibt den Takt. Die Erregung läuft über beide Vorhöfe — das ist die P-Welle. Im AV-Knoten "
               + "wartet sie kurz, damit sich die Vorhöfe zusammenziehen, bevor die Kammern an der Reihe sind — das ist die "
               + "PQ-Zeit. Dann schießt sie durch His-Bündel, Tawara-Schenkel und Purkinje-Fasern und erregt beide Kammern "
               + "fast gleichzeitig: ein schmaler QRS-Komplex.");
        e.wo = T("Markiert: die PQ-Zeit eines Schlags, {ms} ms — vom Beginn der P-Welle bis zum Beginn des QRS.", { ms: m.ms });
        e.echt = T("Richtige Anatomie, normales EKG. Das ist der ganze Zusammenhang.");
        break;
      case "ohne_sinus":
        e.titel = T("Keine P-Welle.");
        e.text = satzSinus(z) + " " + T("Die Vorhöfe bekommen keinen geordneten Anstoß, also gibt es keine P-Welle. Den Takt "
               + "übernimmt ein langsameres Ersatzzentrum im Übergang zur Kammer, {ort}. Von dort leiten His-Bündel, Schenkel und "
               + "Purkinje-Fasern wie gewohnt: Der QRS-Komplex bleibt schmal.", { ort: ort });
        e.wo = T("Gestrichelt: jede R-Zacke. Vor keinem Kammerkomplex steht eine P-Welle, und die Abstände sind ungleich.");
        e.echt = T("Eine Aufnahme eines solchen Ersatzrhythmus liegt uns nicht vor. Gezeigt wird die nächstliegende echte "
               + "Aufnahme: Vorhofflimmern. Gemeinsam ist beiden: keine P-Welle, schmaler QRS. Der Unterschied: Vorhofflimmern "
               + "ist unregelmäßig, ein Ersatzrhythmus regelmäßig und langsam.");
        break;
      case "ohne_sinus_breit":
        e.titel = T("Keine P-Welle, breiter QRS.");
        e.text = satzSinus(z) + " " + T("Ohne geordneten Anstoß im Vorhof gibt es keine P-Welle; den Takt übernimmt ein "
               + "Ersatzzentrum {ort}.", { ort: ort }) + " " + satzKammer(z);
        e.wo = T("Markiert: ein Kammerkomplex, {ms} ms breit (Norm unter 120 ms). Davor steht keine P-Welle.", { ms: m.ms });
        e.echt = T("Eine Aufnahme mit Ersatzrhythmus und breitem QRS liegt uns nicht vor. Am nächsten kommt diese: "
               + "Vorhofflimmern (keine P-Welle) mit Linksschenkelblock (QRS über 120 ms).");
        break;
      case "block":
        e.titel = T("Nichts kommt in der Kammer an.");
        e.text = T("Der Sinusknoten feuert, die Vorhöfe werden erregt — das gäbe die P-Welle.") + " " + saetzeDurchgang(z) + " "
               + T("Die Klappenebene ist Bindegewebe und leitet nicht; das His-Bündel ist der einzige Durchgang. Vorhöfe und "
               + "Kammern sind elektrisch getrennt: ein kompletter AV-Block (III. Grades).");
        e.wo = T("Markiert: ein Kammerkomplex, {ms} ms breit. Er ist breit, weil der Schrittmacher im Kammermuskel zündet und "
               + "die Erregung von dort Zelle für Zelle läuft, nicht über die Leitungsbahn.", { ms: m.ms });
        e.echt = T("Unbehandelt springt in der Kammer nur ein langsamer Ersatzrhythmus ein — oder keiner. Eine Aufnahme davon "
               + "ohne Schrittmacher liegt uns nicht vor. Gezeigt wird ein Patient mit AV-Block III. Grades, dessen Kammern "
               + "ein Schrittmacher anregt.");
        break;
      case "still":
        e.titel = T("Kein Takt, kein Durchgang.");
        e.text = satzSinus(z) + " " + saetzeDurchgang(z) + " " + T("Im Vorhof gibt niemand den Takt, und durch die Klappenebene "
               + "führt kein Weg. Übrig bliebe ein sehr langsamer Ersatzrhythmus aus der Kammer selbst.");
        e.echt = T("Eine echte Aufnahme davon liegt uns nicht vor — deshalb hier kein Streifen. Gemalte Kurven gibt es in diesem Spiel nicht.");
        break;
      case "av_umweg":
      case "av_umweg_breit":
        e.titel = z.fall === "av_umweg" ? T("Die Überleitung dauert zu lang.") : T("Zwei Fehler, zwei Zeichen.");
        e.text = T("Der AV-Knoten sitzt nicht unten in der Vorhofscheidewand, direkt über dem His-Bündel. Im Modell muss die "
               + "Erregung deshalb einen Umweg durch den Vorhofmuskel nehmen, bevor sie die Kammer erreicht. Die Zeit vom "
               + "Beginn der P-Welle bis zum QRS wird länger: PQ über 200 ms.");
        if (z.fall === "av_umweg") {
          e.wo = T("Markiert: die PQ-Zeit eines Schlags, {ms} ms (Norm 120–200 ms).", { ms: m.ms });
          e.echt = T("Im echten Herzen sitzt der AV-Knoten immer am selben Platz. Dort wird die PQ-Zeit länger, wenn der "
                 + "AV-Knoten selbst langsamer leitet: AV-Block I. Grades — wie in dieser Aufnahme.");
        } else {
          e.text += " " + satzKammer(z);
          e.wo = T("Markiert: die PQ-Zeit eines Schlags, {ms} ms. Gestrichelt: Anfang und Ende seines QRS-Komplexes, {qrs} ms.",
                   { ms: m.ms, qrs: m.qrs });
          e.echt = T("Gezeigt wird eine echte Aufnahme mit beidem: PQ über 200 ms und ein breiter QRS. In ihr leitet der rechte "
                 + "Schenkel nicht (kompletter Rechtsschenkelblock); das Prinzip ist dasselbe.");
        }
        break;
      case "schenkel":
        e.titel = T("Breiter Kammerkomplex.");
        e.text = T("Die Erregung kommt über AV-Knoten und His-Bündel bis oben in die Kammerscheidewand.") + " " + satzKammer(z);
        e.wo = T("Markiert: ein Kammerkomplex, {ms} ms breit (Norm unter 120 ms).", { ms: m.ms });
        e.echt = T("So sieht es aus, wenn ein Schenkel ausfällt: In dieser Aufnahme leitet der linke Schenkel nicht (kompletter "
               + "Linksschenkelblock). Die linke Kammer wird über den Muskel erregt, spät und langsam.");
        break;
      case "purkinje":
        e.titel = T("Breiter Kammerkomplex — trotz Schenkel.");
        e.text = satzKammer(z);
        e.wo = T("Markiert: ein Kammerkomplex, {ms} ms breit (Norm unter 120 ms).", { ms: m.ms });
        e.echt = T("Ein Herz ganz ohne Purkinje-Fasern gibt es nicht. Am nächsten kommt eine Leitungsverzögerung in der Kammer, "
               + "die keinem einzelnen Schenkel zuzuordnen ist (unspezifische intraventrikuläre Leitungsverzögerung) — wie in dieser Aufnahme.");
        break;
    }
    /* Was dieser Streifen nicht zeigen kann, wird gesagt statt verschwiegen. */
    if ((z.fall === "ohne_sinus" || z.fall === "ohne_sinus_breit") && z.av !== "richtig") {
      e.echt += " " + T("Ob der AV-Knoten richtig sitzt, verrät dieser Streifen nicht: Ohne P-Welle gibt es keine PQ-Zeit.");
    }
    if (z.fall === "block" && z.kammer !== "schmal") {
      e.echt += " " + T("Ob unterhalb der Klappenebene alles stimmt, verrät dieser Streifen nicht — es kommt ja nichts an.");
    }
    if (m.satz && m.satz.rhythmus === "Sinus bradycardia." && m.satz.mess.frequenz) {
      e.echt += " " + T("Dass dieser Patient langsam ist ({hf}/min, Sinusbradykardie), gehört zu ihm, nicht zum Modell.",
                        { hf: m.satz.mess.frequenz });
    }
    if (m.satz && S && S.anmerkungen && S.anmerkungen[m.satz.id]) e.echt += " " + T(S.anmerkungen[m.satz.id]);
    return e;
  }

  /* ------------------------------------------------------------------ Streifen */
  function fenster(r, fall) {
    var sl = r.schlaege || [], fs = r.sig.fs, gesamt = r.sig.werte.length / fs;
    var dauer = Math.min(6, gesamt), w = null, a, b;
    if (fall.zeige === "pq" || fall.zeige === "qrs") {
      /* Der Schlag, dessen Strecke dem Median am nächsten liegt — bevorzugt einer, der
         im Fenster vorn stehen kann (ein Schlag davor, viele danach). */
      var soll = fall.zeige === "pq" ? r.mess.pq : r.mess.qrs;
      for (var runde = 0; runde < 2 && !w; runde++) {
        for (var i = 1; i < sl.length; i++) {               /* nicht der allererste Schlag */
          a = fall.zeige === "pq" ? sl[i].p0 : sl[i].q0;
          b = fall.zeige === "pq" ? sl[i].q0 : sl[i].q1;
          if (a === undefined || b === undefined) continue;
          if (runde === 0 && (a < 1.0 || a > gesamt - dauer + 2.0)) continue;
          var d = Math.abs((b - a) * 1000 - soll);
          if (!w || d < w.d) w = { d: d, a: a, b: b, i: i };
        }
      }
    }
    var anker = w ? w.a - 1.4 : ((sl[0] ? sl[0].q0 : 0.5) - 0.4);
    var von = Math.max(0, Math.min(gesamt - dauer, anker));
    var f = { von: von, dauer: dauer, zirkel: null, marken: null, ms: null, qrs: null };
    if (w) {
      f.zirkel = { start: w.a, ende: w.b };
      f.ms = Math.round((w.b - w.a) * 1000);
      if (fall.marken === "qrs" && sl[w.i].q1 !== undefined) {
        f.marken = [{ s: sl[w.i].q0 }, { s: sl[w.i].q1 }];
        f.qrs = Math.round((sl[w.i].q1 - sl[w.i].q0) * 1000);
      }
    }
    if (fall.zeige === "r") {
      f.marken = sl.filter(function (s) { return s.r >= von && s.r <= von + dauer; })
                   .map(function (s) { return { s: s.r }; });
    }
    return f;
  }

  function unterschrift(r) {
    var befunde = [r.rhythmus].concat(r.diagnose || []).filter(Boolean)
      .map(function (b) { return T(BEFUND[b] || b); });
    var zahlen = [];
    if (r.mess.pq) zahlen.push(T("PQ {ms} ms", { ms: r.mess.pq }));
    if (r.mess.qrs) zahlen.push(T("QRS {ms} ms", { ms: r.mess.qrs }));
    if (r.mess.frequenz) zahlen.push(T("{hf}/min", { hf: r.mess.frequenz }));
    return '<span class="rl-quelle">' + T("Echte Aufnahme · LUDB Nr. {id} · Ableitung {lead} · 25 mm/s",
             { id: r.id, lead: String(r.sig.lead || "II").toUpperCase() }) + '</span>' +
           '<span class="rl-befund">' + befunde.join(" · ") + '</span>' +
           '<span class="rl-zahlen">' + zahlen.join(" · ") + " " + T("(Median aller Schläge)") + '</span>';
  }

  function zeigeStreifen(r, f) {
    var box = hof.querySelector(".rl-streifen");
    var lw = box.querySelector("canvas");
    box.classList.remove("ohne");
    box.querySelector(".rl-unterschrift").innerHTML = unterschrift(r);
    box.querySelector(".rl-hinweis").textContent = "";
    if (!streifen) { streifen = global.EKG.Streifen(lw, { werte: [], fs: 250 }); hof.__streifen = streifen; }
    var b = lw.clientWidth || 900;
    var px = Math.max(0.8, (b - 8) / ((global.EKG.VORLAUF_MM || 12) + f.dauer * 25));
    var basis = { werte: r.sig.werte, fs: r.sig.fs, mmProS: 25, mmProMv: 10, von: f.von,
                  zirkel: null, loesung: null, marken: null };
    var mein = ++streifenLauf;
    function ende() {
      basis.dauer = f.dauer; basis.pxProMm = 0; basis.zirkel = f.zirkel; basis.marken = f.marken;
      streifen.setze(basis);
      hof.querySelector(".rl-herz").setAttribute("data-bereit", "ja");
    }
    if (ruhig) { ende(); return; }
    /* Der Streifen entsteht von links nach rechts — einmal, ohne Wiederholung. */
    basis.pxProMm = px; basis.dauer = 0.02;
    streifen.setze(basis);
    animiere(900, function () { return mein === streifenLauf; }, function (p) {
      if (p >= 1) { ende(); return; }
      streifen.setze({ dauer: Math.max(0.02, f.dauer * p) });
    });
  }

  function keinStreifen(text) {
    var box = hof.querySelector(".rl-streifen");
    box.classList.add("ohne");
    box.querySelector(".rl-unterschrift").innerHTML = "";
    box.querySelector(".rl-hinweis").textContent = text;
    hof.querySelector(".rl-herz").setAttribute("data-bereit", "ja");
  }

  /* ------------------------------------------------------------------ Welle */
  /* gilt: Zahl (gehört zur Welle `lauf`) oder Funktion, die sagt, ob das Bild noch aktuell ist. */
  function animiere(ms, gilt, schritt) {
    var aktuell = typeof gilt === "function" ? gilt : function () { return gilt === lauf; };
    if (ruhig || ms <= 0) { schritt(1); return; }
    var t0 = null;
    function f(t) {
      if (!aktuell()) return;
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / ms);
      schritt(p);
      if (p < 1) global.requestAnimationFrame(f);
    }
    global.requestAnimationFrame(f);
  }

  function kurve(a, b) {
    var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return "M" + a[0] + "," + a[1] + " Q" + (mx - dy * 0.18).toFixed(1) + "," + (my + dx * 0.18).toFixed(1) +
           " " + b[0] + "," + b[1];
  }

  function platzPunkt(p) { var q = geo.plaetze[p]; return [q.x, q.y]; }

  function schritt(s, mein) {
    var welle = auflage.querySelector(".rl-welle");
    if (s.art === "bahn") {
      var pf = el("path", { d: s.d, "class": "rl-w-bahn" });
      welle.appendChild(pf);
      var lang = pf.getTotalLength();
      pf.style.strokeDasharray = lang + " " + lang;
      pf.style.strokeDashoffset = lang;
      animiere(s.ms, mein, function (p) { pf.style.strokeDashoffset = lang * (1 - p); });
    } else if (s.art === "zellen") {
      /* Muskel leitet von Zelle zu Zelle: Punkt für Punkt, langsam. */
      var mess = el("path", { d: s.d });
      welle.appendChild(mess);
      var l = mess.getTotalLength(), orte = [], punkte = [];
      for (var x = 0; x <= l; x += 9) orte.push(mess.getPointAtLength(x));
      welle.removeChild(mess);
      orte.forEach(function (q) {
        var c = el("circle", { cx: q.x.toFixed(1), cy: q.y.toFixed(1), r: 2.8, "class": "rl-w-zelle" });
        c.style.opacity = 0;
        welle.appendChild(c);
        punkte.push(c);
      });
      animiere(s.ms, mein, function (p) {
        var bis = Math.round(p * punkte.length);
        for (var i = 0; i < bis; i++) punkte[i].style.opacity = 1;
      });
    } else if (s.art === "flaeche") {
      var fl = auflage.querySelector(".rl-flaeche.rl-" + s.wo);
      fl.style.transition = "opacity " + (ruhig ? 0 : Math.round(s.ms * 0.8)) + "ms linear";
      fl.style.opacity = 0.3;
      global.setTimeout(function () {
        if (mein !== lauf) return;
        fl.style.transition = "opacity " + (ruhig ? 0 : 900) + "ms linear";
        fl.style.opacity = 0;
      }, ruhig ? 0 : s.ms + 350);
    } else if (s.art === "ring") {
      var ring = el("circle", { cx: s.p[0], cy: s.p[1], r: 6, "class": "rl-w-ring" });
      welle.appendChild(ring);
      animiere(s.ms, mein, function (p) {
        ring.setAttribute("r", (6 + 16 * p).toFixed(1));
        ring.style.opacity = String(1 - 0.8 * p);
      });
    } else if (s.art === "sperre") {
      welle.appendChild(el("line", { x1: s.p[0] - 22, y1: s.p[1], x2: s.p[0] + 22, y2: s.p[1], "class": "rl-w-sperre" }));
    }
  }

  function zeitplan(z) {
    var G = geo, P = G.punkte, W = G.wege, his = G.teile.his.bahnen[0], plan = [];
    function alle(liste, art, ms) { return liste.map(function (d) { return { art: art, d: d, ms: ms }; }); }
    function kammer() {
      var schenkel = G.teile.schenkel.bahnen;
      if (z.kammer === "schenkel") {
        return [alle(schenkel, "zellen", 1100).concat([{ art: "flaeche", wo: "kammer", ms: 1500 }]),
                alle(W.purkinje, "zellen", 900)];
      }
      if (z.kammer === "purkinje") {
        return [alle(schenkel, "bahn", 260),
                alle(W.purkinje, "zellen", 1000).concat([{ art: "flaeche", wo: "kammer", ms: 1000 }])];
      }
      return [alle(schenkel, "bahn", 260),
              alle(W.purkinje, "bahn", 280).concat([{ art: "flaeche", wo: "kammer", ms: 300 }])];
    }
    if (z.fall === "leer" || z.fall === "still") return plan;
    if (z.sinus === "richtig") {
      var avOrt = z.av === "umweg" ? platzPunkt(bau.av) : P.av;
      plan.push({ art: "ring", p: P.sinus, ms: 300 });
      plan.push([{ art: "zellen", d: W.vorhof_links, ms: 560 }, { art: "zellen", d: W.vorhof_unten, ms: 560 },
                 { art: "zellen", d: z.av === "umweg" ? kurve(P.sinus, avOrt) : W.vorhof_av, ms: 560 },
                 { art: "flaeche", wo: "vorhof", ms: 560 }]);
      if (z.av === "richtig" || z.av === "umweg") plan.push({ art: "ring", p: avOrt, ms: 420 });
      if (z.av === "umweg") plan.push({ art: "zellen", d: kurve(avOrt, P.his_anfang), ms: 1000 });
      if (z.leitung === "block") { plan.push({ art: "sperre", p: P.sperre, ms: 300 }); return plan; }
      plan.push({ art: "bahn", d: his, ms: 240 });
      return plan.concat(kammer());
    }
    /* Ersatzzentrum: Die Vorhöfe bleiben still, der Takt beginnt am Übergang. */
    plan.push({ art: "ring", p: z.ersatz === "av" ? P.av : P.his_anfang, ms: 520 });
    plan.push({ art: "bahn", d: his, ms: 240 });
    return plan.concat(kammer());
  }

  function spiele(plan, fertig) {
    var mein = ++lauf, i = 0;
    var welle = auflage.querySelector(".rl-welle");
    while (welle.firstChild) welle.removeChild(welle.firstChild);
    welle.style.transition = "none"; welle.style.opacity = 1;
    Array.prototype.forEach.call(auflage.querySelectorAll(".rl-flaeche"), function (f) {
      f.style.transition = "none"; f.style.opacity = 0;
    });
    (function weiter() {
      if (mein !== lauf) return;
      if (i >= plan.length) {
        /* Die Spur bleibt blass stehen: Man sieht danach noch, welchen Weg die Erregung nahm. */
        global.setTimeout(function () {
          if (mein !== lauf) return;
          welle.style.transition = ruhig ? "none" : "opacity 1.2s linear";
          welle.style.opacity = 0.35;
        }, ruhig ? 0 : 900);
        if (fertig) fertig();
        return;
      }
      var gruppe = [].concat(plan[i++]), lang = 0;
      gruppe.forEach(function (s) { lang = Math.max(lang, s.ms || 0); schritt(s, mein); });
      global.setTimeout(weiter, ruhig ? 0 : lang);
    })();
  }

  /* ------------------------------------------------------------------ Zeichnen */
  function zeichneTeile() {
    var g = auflage.querySelector(".rl-teile");
    while (g.firstChild) g.removeChild(g.firstChild);
    TEILE.forEach(function (t) {
      var p = bau[t.id];
      if (!p) return;
      var form = geo.teile[t.id];
      var gruppe = el("g", { "class": "rl-teil-bild" + (gewaehlt === t.id ? " gewaehlt" : ""), "data-teil": t.id });
      if (p === t.id && form.ellipse) {
        var e = form.ellipse;
        gruppe.appendChild(el("ellipse", { cx: e[0], cy: e[1], rx: e[2], ry: e[3],
                                           transform: "rotate(" + e[4] + " " + e[0] + " " + e[1] + ")", "class": "rl-knoten" }));
      } else if (p === t.id) {
        form.bahnen.forEach(function (d) {
          gruppe.appendChild(el("path", { d: d, "class": "rl-strang-rand" + (form.fein ? " fein" : "") }));
        });
        form.bahnen.forEach(function (d) {
          gruppe.appendChild(el("path", { d: d, "class": "rl-strang" + (form.fein ? " fein" : "") }));
        });
      } else {
        var q = geo.plaetze[p];
        gruppe.appendChild(el("circle", { cx: q.x, cy: q.y, r: 17, "class": "rl-marke" }));
        var tx = el("text", { x: q.x, y: q.y + 6, "class": "rl-marke-nr", "text-anchor": "middle" });
        tx.textContent = String(t.nr);
        gruppe.appendChild(tx);
      }
      g.appendChild(gruppe);
    });
  }

  function zeigeAuswahl() {
    Array.prototype.forEach.call(hof.querySelectorAll(".rl-teil"), function (k) {
      var id = k.getAttribute("data-teil");
      k.classList.toggle("gewaehlt", gewaehlt === id);
      k.setAttribute("aria-pressed", gewaehlt === id ? "true" : "false");
      k.classList.toggle("gesetzt", !!bau[id]);
      k.querySelector(".wo").textContent = bau[id] ? T("gesetzt") : T("im Kasten");
    });
    hof.querySelector(".rl-herz").classList.toggle("bereit", !!gewaehlt);
    hof.querySelector(".rl-raus").disabled = !(gewaehlt && bau[gewaehlt]);
    zeichneTeile();
  }

  function status(text) { hof.querySelector(".rl-status").textContent = text || ""; }

  function rueckmeldung(z, e, fall) {
    var r = hof.querySelector(".rl-rueck");
    r.className = "rueck rl-rueck" + (z.fall === "richtig" ? " gut" : z.fall === "leer" ? "" : " fast");
    var html = "<strong>" + e.titel + "</strong> " + e.text;
    if (e.wo) html += '<span class="rl-wo">' + e.wo + "</span>";
    if (e.echt) html += '<span class="rl-echt">' + e.echt + "</span>";
    if (fall && fall.begruendung && z.fall !== "leer") {
      html += '<span class="rl-grund">' + T("Warum diese Aufnahme: {grund}", { grund: T(fall.begruendung) }) + "</span>";
    }
    r.innerHTML = html;
    hof.querySelector(".rl-fertig").hidden = z.fall !== "richtig";
  }

  /* ------------------------------------------------------------------ Ablauf */
  function nachDemSetzen(notiz) {
    zeigeAuswahl();
    var z = bewerte(bau), fall = FAELLE[z.fall] || null;
    letzter = z;
    var herz = hof.querySelector(".rl-herz");
    herz.setAttribute("data-fall", z.fall);
    herz.setAttribute("data-bereit", "nein");
    status((notiz ? notiz + " " : "") + T("{n} von 5 Bauteilen gesetzt.", { n: z.gesetzt }));
    hof.querySelector(".rl-rueck").className = "rueck rl-rueck";
    hof.querySelector(".rl-rueck").innerHTML = z.gesetzt ? "<em>" + T("Die Erregung läuft …") + "</em>" : "";
    hof.querySelector(".rl-fertig").hidden = true;
    streifenLauf++;                                   /* alter Streifen hört auf zu wachsen */
    spiele(zeitplan(z), function () { zeigeFolge(z, fall); });
  }

  function zeigeFolge(z, fall) {
    var r = fall && fall.aufnahme ? S.satz(fall.aufnahme) : null;
    var herz = hof.querySelector(".rl-herz");
    herz.setAttribute("data-aufnahme", r ? String(r.id) : "");
    if (z.fall === "leer") {
      keinStreifen(T("Noch keine Kurve. Sie entsteht, sobald etwas gebaut ist."));
      rueckmeldung(z, erklaere(z, {}), fall);
      return;
    }
    if (fall && fall.aufnahme && !r) {
      /* Fehlt die Aufnahme im Bündel, wird nichts erfunden. */
      if (global.console) global.console.warn("Reizleitung: Aufnahme " + fall.aufnahme + " fehlt im Bündel.");
      keinStreifen(T("Die passende Aufnahme (LUDB Nr. {id}) ist in dieser Ausgabe nicht enthalten.", { id: fall.aufnahme }));
      rueckmeldung(z, erklaere(z, {}), fall);
      return;
    }
    if (!r) {
      keinStreifen(T("Kein Streifen: Für diesen Aufbau liegt keine echte Aufnahme vor."));
      rueckmeldung(z, erklaere(z, {}), fall);
      return;
    }
    var f = fenster(r, fall);
    zeigeStreifen(r, f);
    rueckmeldung(z, erklaere(z, { ms: f.ms, qrs: f.qrs, satz: r }), fall);
  }

  function waehle(id) {
    if (!teil(id)) return;
    gewaehlt = gewaehlt === id ? null : id;
    zeigeAuswahl();
    if (gewaehlt) {
      status(bau[id]
        ? T("{name} ist gewählt. Tipp einen anderen Platz an — oder „Herausnehmen“.", { name: T(teil(id).name) })
        : T("{name} ist gewählt. Jetzt den Platz im Herzen antippen.", { name: T(teil(id).name) }));
    }
  }

  function tippePlatz(platz) {
    var da = teilAuf(platz);
    if (!gewaehlt) {
      if (da) { waehle(da); return; }
      status(T("Erst ein Bauteil wählen — rechts antippen oder Ziffer 1 bis 5."));
      return;
    }
    if (da === gewaehlt) { gewaehlt = null; zeigeAuswahl(); status(""); return; }
    var notiz = "";
    if (da) { bau[da] = null; notiz = T("{name} liegt wieder im Kasten.", { name: T(teil(da).name) }); }
    bau[gewaehlt] = platz;
    gewaehlt = null;
    nachDemSetzen(notiz);
  }

  function herausnehmen() {
    if (!gewaehlt || !bau[gewaehlt]) return;
    var name = T(teil(gewaehlt).name);
    bau[gewaehlt] = null;
    gewaehlt = null;
    nachDemSetzen(T("{name} herausgenommen.", { name: name }));
  }

  function allesZurueck() {
    bau = leer(); gewaehlt = null;
    nachDemSetzen("");
  }

  /* ------------------------------------------------------------------ Aufbau */
  function baueAuflage() {
    var svg = el("svg", { viewBox: geo.viewBox, "class": "rl-auflage", preserveAspectRatio: "xMidYMid meet" });
    var defs = el("defs", {}), clip = el("clipPath", { id: "rl-umriss" });
    clip.appendChild(el("path", { d: geo.flaechen.umriss }));
    defs.appendChild(clip);
    svg.appendChild(defs);
    var vb = geo.viewBox.split(/\s+/).map(Number), band = geo.flaechen.band;
    var fl = el("g", { "clip-path": "url(#rl-umriss)" });
    fl.appendChild(el("rect", { x: 0, y: 0, width: vb[2], height: band[0], "class": "rl-flaeche rl-vorhof" }));
    fl.appendChild(el("rect", { x: 0, y: band[1], width: vb[2], height: vb[3] - band[1], "class": "rl-flaeche rl-kammer" }));
    svg.appendChild(fl);
    svg.appendChild(el("g", { "class": "rl-teile" }));
    svg.appendChild(el("g", { "class": "rl-welle" }));
    var pl = el("g", { "class": "rl-plaetze" });
    /* Reihenfolge nur für die Tastatur: von oben nach unten, ohne Namen — der Platz ist die Frage. */
    var reihe = Object.keys(geo.plaetze).sort(function (a, b) {
      return (geo.plaetze[a].y - geo.plaetze[b].y) || (geo.plaetze[a].x - geo.plaetze[b].x);
    });
    reihe.forEach(function (id, i) {
      var q = geo.plaetze[id];
      var g = el("g", { "class": "rl-platz", "data-platz": id, tabindex: "0", role: "button",
                        "aria-label": T("Platz {n} von {alle}", { n: i + 1, alle: reihe.length }) });
      g.appendChild(el("circle", { cx: q.x, cy: q.y, r: 35, "class": "rl-treffer" }));   /* ≥ 44 px bei 420 px Breite */
      g.appendChild(el("circle", { cx: q.x, cy: q.y, r: 27, "class": "rl-ring" }));
      g.addEventListener("click", function () { tippePlatz(id); });
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); tippePlatz(id); }
      });
      pl.appendChild(g);
    });
    svg.appendChild(pl);
    return svg;
  }

  function bau_() {
    hof = document.createElement("div");
    hof.className = "raetsel";
    hof.id = "reizleitung-hof";
    var knoepfe = TEILE.map(function (t) {
      return '<button class="knopf rl-teil" type="button" data-teil="' + t.id + '" aria-pressed="false">' +
             '<span class="nr">' + t.nr + '</span><span class="name">' + T(t.name) + '</span>' +
             '<span class="wo"></span></button>';
    }).join("");
    hof.innerHTML =
      '<div class="raetsel-innen">' +
      '  <div class="raetsel-kopf"><h2></h2><button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
      '  <p class="raetsel-auftrag"></p>' +
      '  <div class="rl-werkbank">' +
      '    <div class="rl-herz" data-fall="leer" data-bereit="ja"></div>' +
      '    <div class="rl-seite">' +
      '      <div class="rl-kasten" role="group">' + knoepfe + '</div>' +
      '      <div class="rl-aktionen">' +
      '        <button class="knopf rl-raus" type="button" disabled>' + T("Herausnehmen") + '</button>' +
      '        <button class="knopf rl-welle-knopf" type="button">' + T("Welle nochmal") + '</button>' +
      '        <button class="knopf rl-neu" type="button">' + T("Alles zurück") + '</button>' +
      '        <button class="knopf haupt rl-fertig" type="button" hidden>' + T("Verstanden") + '</button>' +
      '      </div>' +
      '      <p class="rl-status" aria-live="polite"></p>' +
      '    </div>' +
      '  </div>' +
      '  <div class="rl-streifen ohne">' +
      '    <div class="rl-unterschrift"></div>' +
      '    <div class="raetsel-papier"><canvas height="170"></canvas></div>' +
      '    <p class="rl-hinweis"></p>' +
      '  </div>' +
      '  <div class="rueck rl-rueck" aria-live="polite"></div>' +
      '</div>';
    document.body.appendChild(hof);
    hof.querySelector(".zu").addEventListener("click", schliesse);
    Array.prototype.forEach.call(hof.querySelectorAll(".rl-teil"), function (k) {
      k.addEventListener("click", function () { waehle(k.getAttribute("data-teil")); });
    });
    hof.querySelector(".rl-raus").addEventListener("click", herausnehmen);
    hof.querySelector(".rl-neu").addEventListener("click", allesZurueck);
    /* Noch einmal dasselbe: Welle und Streifen, ohne am Bau etwas zu ändern. */
    hof.querySelector(".rl-welle-knopf").addEventListener("click", function () { nachDemSetzen(""); });
    hof.querySelector(".rl-fertig").addEventListener("click", function () {
      var f = S && S.fertig;
      schliesse();
      if (f) f({ fall: letzter && letzter.fall });
    });
    document.addEventListener("keydown", function (e) {
      if (!hof.classList.contains("an")) return;
      if (e.key === "Escape") { e.preventDefault(); schliesse(); return; }
      if (/^[1-5]$/.test(e.key) && !e.altKey && !e.ctrlKey && !e.metaKey) {
        e.preventDefault(); waehle(TEILE[+e.key - 1].id); return;
      }
      if (e.key === "Delete" || e.key === "Backspace") { e.preventDefault(); herausnehmen(); }
    });
  }

  function starte(opt) {
    opt = opt || {};
    var schema = opt.schema || (global.KUNST && global.KUNST.schemata);
    if (!schema || !schema.herz || !schema.herz_geo) {
      if (global.console) global.console.warn("Reizleitung: Schema fehlt (gen/kunst.py → schemata).");
      return false;
    }
    if (!hof) bau_();
    S = opt;
    S.satz = opt.satz || (global.Spiel && global.Spiel.satz) || function () { return null; };
    geo = schema.herz_geo;
    herzBox = hof.querySelector(".rl-herz");
    herzBox.innerHTML = schema.herz;
    auflage = baueAuflage();
    herzBox.appendChild(auflage);
    hof.querySelector("h2").textContent = T(opt.titel || "Reizleitung bauen");
    hof.querySelector(".raetsel-auftrag").innerHTML =
      T(opt.auftrag || "Setz die fünf Bauteile ins Herz: erst ein Bauteil antippen, dann seinen Platz. Nach jedem Setzen läuft "
        + "die Erregung durch das, was gebaut ist — und darunter erscheint die echte Kurve, die dazu passt.") +
      " <em>" + T("Ziel: Richtige Anatomie ergibt ein normales EKG.") + "</em>";
    bau = leer(); gewaehlt = null; letzter = null; lauf++;
    hof.classList.add("an");
    if (global.Szene) global.Szene.sperre(true);
    nachDemSetzen("");
    var erster = hof.querySelector(".rl-teil");
    if (erster && erster.focus) { try { erster.focus({ preventScroll: true }); } catch (x) { erster.focus(); } }
    return true;
  }

  function schliesse() {
    lauf++; streifenLauf++;
    if (hof) hof.classList.remove("an");
    if (global.Szene) { global.Szene.sperre(false); global.Szene.aktualisiere(); }
  }

  /* Für den Durchlauf: Stimmt jede Zeile der Tabelle mit den Daten überein? */
  function pruefeTabelle(satz) {
    satz = satz || (S && S.satz) || (global.Spiel && global.Spiel.satz);
    return Object.keys(FAELLE).map(function (k) {
      var f = FAELLE[k], r = f.aufnahme ? satz(f.aufnahme) : null;
      return { fall: k, aufnahme: f.aufnahme, da: !f.aufnahme || !!r, passt: !f.aufnahme || (!!r && f.passt(r)) };
    });
  }

  global.Reizleitung = {
    starte: starte, schliesse: schliesse, TEILE: TEILE, FAELLE: FAELLE,
    bewerte: function (b) { return bewerte(b || bau); },
    zustand: function () {
      var b = {}; for (var k in bau) b[k] = bau[k];
      return { bau: b, fall: letzter && letzter.fall,
               aufnahme: hof ? +(hof.querySelector(".rl-herz").getAttribute("data-aufnahme") || 0) || null : null };
    },
    __waehle: waehle, __tippePlatz: tippePlatz, __pruefeTabelle: pruefeTabelle
  };
})(window);
