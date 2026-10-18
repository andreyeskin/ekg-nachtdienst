/* Leben im Raum (Prototyp, 18.10.2026, docs/REDESIGN_FALL1.md §10).
   Kleine Bewegungen über den gerenderten Ebenen einer Szene: Uhr mit Sekundenzeiger, Lidschlag,
   Kopf- und Blickwechsel der Figuren, Lichtkeil mit Staub, Leben vor dem Fenster, Leute im Flur,
   ein Vorbeigehender im unscharfen Vordergrund, der EKG-Wagen. Nichts davon trägt Spielinhalt;
   alles bleibt stumm verständlich. prefers-reduced-motion: nur Uhr und Zustände, keine Bewegung.

     Leben.starte(svg, cfg, bilder)   baut die Überlagerungen (cfg: Raumbeschreibung, bilder: Name → URL)
     Leben.zeit(minuten)              Spielzeit (Minuten seit Mitternacht): Zeiger, Licht, Ungeduld
     Leben.ereignis(name)             Story-Momente: "handy", "vorbei", "uhr_blick", "ekg", "ekg_aus"
     Leben.bewegung(an)               alles an/aus (Schalter im Menü)

   Koordinaten: 1600 × 900 wie die Ebenen (art/szenen/<raum>/*.png). Kurven auf Geräteschirmen nur aus
   data/ (ART_BIBLE §6): cfg.wagen.ekg = { werte, fs, frequenz } aus data/ekg_daten.json.            */
(function (global) {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var LINIE = "#1E2A30", PHOSPHOR = "#39E58C", GLAS = "#1E2A30";
  var svg = null, cfg = null, defs = null, uhr = null, figuren = {}, takte = [], an = true, ruhig = false;
  var spielzeit = 6 * 60 + 40, t0 = 0, jetzt = 0, wagen = null, licht = null, staub = [];

  function el(name, attr, eltern) {
    var e = document.createElementNS(NS, name);
    for (var k in attr) if (attr.hasOwnProperty(k)) e.setAttribute(k, attr[k]);
    if (eltern) eltern.appendChild(e);
    return e;
  }
  function zufall(a, b) { return a + Math.random() * (b - a); }
  function weich(aktuell, ziel, dt, k) { return aktuell + (ziel - aktuell) * Math.min(1, dt * k); }
  function punkte(liste) { return liste.map(function (p) { return p[0] + "," + p[1]; }).join(" "); }

  /* Ein Takt ist eine Aufgabe pro Bild: fn(t, dt) gibt false zurück, wenn sie fertig ist. */
  function takt(fn) { takte.push(fn); }

  /* ------------------------------------------------------------------ Uhr */
  function baueUhr(ebene, u) {
    var g = el("g", { "class": "leben-uhr" }, ebene);
    function zeiger(laenge, breite, farbe, schwanz) {
      return el("line", { x1: u.cx, y1: u.cy + (schwanz || 0), x2: u.cx, y2: u.cy - laenge, stroke: farbe,
        "stroke-width": breite, "stroke-linecap": "round" }, g);
    }
    uhr = {
      std: zeiger(u.r * 0.52, 5, LINIE), min: zeiger(u.r * 0.8, 3, LINIE),
      sek: zeiger(u.r * 0.86, 1.4, "#A8432F", u.r * 0.18), u: u
    };
    el("circle", { cx: u.cx, cy: u.cy, r: 3, fill: LINIE }, g);
    takt(function (t) {
      var d = new Date(), s = d.getSeconds(), ms = d.getMilliseconds();
      /* Sprung mit kurzem Nachfedern, wie eine Bahnhofsuhr */
      var feder = ms < 160 ? Math.sin(ms / 160 * Math.PI) * 1.8 : 0;
      var winkel = ruhig || !an ? s * 6 : s * 6 + feder;
      uhr.sek.setAttribute("transform", "rotate(" + winkel.toFixed(2) + " " + u.cx + " " + u.cy + ")");
      return true;
    });
    stelleUhr();
  }
  function stelleUhr() {
    if (!uhr) return;
    var h = (spielzeit / 60) % 12, m = spielzeit % 60, u = uhr.u;
    uhr.std.setAttribute("transform", "rotate(" + (h * 30).toFixed(2) + " " + u.cx + " " + u.cy + ")");
    uhr.min.setAttribute("transform", "rotate(" + (m * 6).toFixed(2) + " " + u.cx + " " + u.cy + ")");
  }

  /* ------------------------------------------------------------------ Figuren: Atem, Kopf, Lidschlag */
  function clip(id, d, regel) {
    var c = el("clipPath", { id: id }, defs);
    el("path", { d: d, "clip-rule": regel || "nonzero" }, c);
    return "url(#" + id + ")";
  }
  function pfad(liste) { return "M" + liste.map(function (p) { return p[0] + " " + p[1]; }).join(" L") + " Z"; }

  function baueFigur(ebene, name, f, url) {
    var aussen = el("g", { "class": "leben-figur", "data-figur": name, transform: "translate(" + f.x + " " + f.y + ")" }, ebene);
    var rumpf = el("g", {}, aussen);
    var ohneKopf = clip("loch-" + name, "M-40 -40 H" + (f.b + 40) + " V" + (f.h + 40) + " H-40 Z " + pfad(f.kopf.loch), "evenodd");
    el("image", { href: url, x: 0, y: 0, width: f.b, height: f.h, "clip-path": ohneKopf }, rumpf);
    var kopf = el("g", {}, rumpf);
    el("image", { href: url, x: 0, y: 0, width: f.b, height: f.h, "clip-path": clip("kopf-" + name, pfad(f.kopf.kopf)) }, kopf);
    var lider = el("g", { "class": "lider", style: "display:none" }, kopf);
    f.augen.forEach(function (a) {
      el("ellipse", { cx: a[0], cy: a[1], rx: a[2], ry: a[3], fill: f.haut }, lider);
      el("path", { d: "M" + (a[0] - a[2]) + " " + (a[1] + 0.3) + " Q" + a[0] + " " + (a[1] + a[3] * 0.9) + " " +
        (a[0] + a[2]) + " " + (a[1] + 0.3), fill: "none", stroke: LINIE, "stroke-width": 1, "stroke-linecap": "round" }, lider);
    });
    var zusatz = el("g", {}, aussen);           /* Vibrieren, Zeichen neben der Figur */
    var F = {
      def: f, aussen: aussen, rumpf: rumpf, kopf: kopf, lider: lider, zusatz: zusatz,
      r: 0, dy: 0, ziel: f.blicke[f.ruhe], pose: f.ruhe, bisPose: 0, bisLid: zufall(1, 4), lidZu: 0,
      zittern: 0, tippen: false
    };
    figuren[name] = F;
    takt(function (t, dt) { bewegeFigur(F, t, dt); return true; });
    return F;
  }

  function setzePose(F, pose, dauer) {
    F.pose = pose; F.ziel = F.def.blicke[pose]; F.bisPose = jetzt + dauer;
    F.tippen = !!F.ziel.tippt;
  }
  function naechstePose(F) {
    var plan = F.def.plan(F.pose, spielzeit);                 /* [pose, dauer] */
    setzePose(F, plan[0], plan[1]);
  }

  function bewegeFigur(F, t, dt) {
    var f = F.def;
    if (an && !ruhig && t > F.bisPose) naechstePose(F);
    var ziel = (an && !ruhig) ? F.ziel : f.blicke[f.ruhe];
    F.r = weich(F.r, ziel.r, dt, ziel.schnell ? 9 : 4.5);
    F.dy = weich(F.dy, ziel.y, dt, ziel.schnell ? 9 : 4.5);
    var tipp = (an && !ruhig && F.tippen) ? Math.sin(t * 17) * 0.35 : 0;
    F.kopf.setAttribute("transform", "rotate(" + F.r.toFixed(2) + " " + f.kopf.dreh[0] + " " + f.kopf.dreh[1] +
      ") translate(0 " + (F.dy + tipp).toFixed(2) + ")");
    var atem = (an && !ruhig) ? Math.sin(t / f.atem.periode * Math.PI * 2) * f.atem.hub : 0;
    var zx = 0;
    if (F.zittern > t) { zx = Math.sin(t * 160) * 0.9 * ((Math.floor((F.zittern - t) / 0.55) % 2) ? 0 : 1); }
    F.rumpf.setAttribute("transform", "translate(" + zx.toFixed(2) + " " + atem.toFixed(2) + ")");
    /* Lidschlag: 120 ms, manchmal doppelt */
    if (an && !ruhig) {
      if (t > F.bisLid) {
        F.lidZu = t + 0.12;
        F.bisLid = t + (Math.random() < 0.15 ? 0.32 : zufall(2.4, 6.2));
      }
      F.lider.style.display = t < F.lidZu ? "" : "none";
    } else F.lider.style.display = "none";
  }

  /* ------------------------------------------------------------------ Licht: Keil durchs Fenster, Staub, Tagesfarbe */
  function baueLicht(ebene, k) {
    var verlauf = el("linearGradient", { id: "leben-keil", x1: "0", y1: "0", x2: "0", y2: "1" }, defs);
    el("stop", { offset: "0", "stop-color": "#FFE2A8", "stop-opacity": "0.9" }, verlauf);
    el("stop", { offset: "1", "stop-color": "#FFD08A", "stop-opacity": "0.15" }, verlauf);
    var g = el("g", { "class": "leben-licht", style: "mix-blend-mode:screen" }, ebene);
    var keil = el("polygon", { points: punkte(k.keil), fill: "url(#leben-keil)", opacity: "0.12" }, g);
    var staubClip = clip("leben-staubraum", pfad(k.keil));
    var sg = el("g", { "clip-path": staubClip }, g);
    var minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
    k.keil.forEach(function (p) { minx = Math.min(minx, p[0]); maxx = Math.max(maxx, p[0]); miny = Math.min(miny, p[1]); maxy = Math.max(maxy, p[1]); });
    for (var i = 0; i < 34; i++) {
      var s = { x: zufall(minx, maxx), y: zufall(miny, maxy), r: zufall(1.1, 2.6), ph: zufall(0, 6.3), v: zufall(2, 6) };
      s.el = el("circle", { cx: s.x, cy: s.y, r: s.r, fill: "#FFF1CF" }, sg);
      staub.push(s);
    }
    licht = { keil: keil, wolke: 1, wolkeZiel: 1, bisWolke: 4, box: [minx, maxx, miny, maxy] };
    takt(function (t, dt) {
      if (!an || ruhig) { keil.setAttribute("opacity", (0.12 * sonne()).toFixed(3)); sg.style.display = "none"; return true; }
      sg.style.display = "";
      if (t > licht.bisWolke) { licht.wolkeZiel = Math.random() < 0.3 ? zufall(0.45, 0.7) : 1; licht.bisWolke = t + zufall(5, 12); }
      licht.wolke = weich(licht.wolke, licht.wolkeZiel, dt, 0.5);
      var staerke = sonne() * licht.wolke;
      keil.setAttribute("opacity", (0.14 * staerke).toFixed(3));
      staub.forEach(function (s) {
        s.y -= s.v * dt * 0.6; s.x += Math.sin(t * 0.4 + s.ph) * dt * 4;
        if (s.y < licht.box[2]) { s.y = licht.box[3]; s.x = zufall(licht.box[0], licht.box[1]); }
        s.el.setAttribute("cx", s.x.toFixed(1)); s.el.setAttribute("cy", s.y.toFixed(1));
        s.el.setAttribute("opacity", (staerke * (0.35 + 0.35 * Math.sin(t * 1.3 + s.ph))).toFixed(2));
      });
      return true;
    });
  }
  /* 06:40 tiefe Sonne, voller Keil; gegen 07:50 steht sie höher, der Keil wird blass. */
  function sonne() { return Math.max(0.25, Math.min(1, 1 - (spielzeit - 400) / 95)); }

  function baueStimmung(ebene) {
    var r = el("rect", { x: -50, y: -50, width: 1700, height: 1000, fill: "#FF9F45", opacity: "0.12",
      style: "mix-blend-mode:soft-light;pointer-events:none" }, ebene);
    takt(function () { r.setAttribute("opacity", (0.16 * sonne()).toFixed(3)); return true; });
  }

  /* ------------------------------------------------------------------ Fenster: Vögel, Spaziergänger mit Hund */
  function baueFenster(ebene, fe) {
    var d = fe.scheiben.map(function (s) { return "M" + s[0] + " " + s[1] + " h" + s[2] + " v" + s[3] + " h" + (-s[2]) + " Z"; }).join(" ");
    var g = el("g", { "clip-path": clip("leben-glas", d) }, ebene);
    var links = fe.scheiben[0][0], rechts = fe.scheiben[fe.scheiben.length - 1][0] + fe.scheiben[fe.scheiben.length - 1][2];
    var oben = fe.scheiben[0][1];
    var bisVogel = zufall(3, 8), bisGeher = zufall(6, 14);

    function voegel() {
      var schwarm = el("g", {}, g), n = 2 + Math.floor(Math.random() * 3), rueck = Math.random() < 0.5;
      var vs = [];
      for (var i = 0; i < n; i++) vs.push({ dx: i * zufall(14, 22), dy: zufall(-6, 6), ph: zufall(0, 6), p: el("path", { fill: "none", stroke: LINIE, "stroke-width": 1.3, "stroke-linecap": "round" }, schwarm) });
      var y0 = oben + zufall(8, 34), start = jetzt, dauer = zufall(4.5, 7);
      takt(function (t) {
        var a = (t - start) / dauer; if (a > 1) { schwarm.remove(); return false; }
        var x = rueck ? rechts + 40 - a * (rechts - links + 120) : links - 80 + a * (rechts - links + 120);
        vs.forEach(function (v) {
          var f = Math.sin(t * 13 + v.ph), xx = x + (rueck ? v.dx : -v.dx), yy = y0 + v.dy + Math.sin(t * 2 + v.ph) * 2;
          v.p.setAttribute("d", "M" + (xx - 6) + " " + (yy - 2 * f) + " Q" + (xx - 3) + " " + (yy - 3 - f) + " " + xx + " " + yy +
            " Q" + (xx + 3) + " " + (yy - 3 - f) + " " + (xx + 6) + " " + (yy - 2 * f));
        });
        return true;
      });
    }

    /* Ein Mann mit Hund geht draußen vorbei: um 06:40 ist das der erste, der Gassi geht. */
    function geher() {
      var k = el("g", {}, g), rueck = Math.random() < 0.6, start = jetzt, dauer = zufall(16, 22), boden = fe.boden;
      var bein1 = el("line", { stroke: "#4A3A2C", "stroke-width": 2.2, "stroke-linecap": "round" }, k);
      var bein2 = el("line", { stroke: "#4A3A2C", "stroke-width": 2.2, "stroke-linecap": "round" }, k);
      var mantel = el("path", { fill: "#7A5136", stroke: LINIE, "stroke-width": 0.8 }, k);
      var kopf = el("circle", { r: 3.4, fill: "#E2B48A", stroke: LINIE, "stroke-width": 0.8 }, k);
      var muetze = el("path", { fill: "#3D4B52" }, k);
      var leine = el("path", { fill: "none", stroke: LINIE, "stroke-width": 0.7 }, k);
      var hund = el("ellipse", { rx: 6.5, ry: 3, fill: "#3B2B20" }, k);
      var hkopf = el("circle", { r: 2.4, fill: "#3B2B20" }, k);
      var hb = [0, 1, 2, 3].map(function () { return el("line", { stroke: "#3B2B20", "stroke-width": 1.4, "stroke-linecap": "round" }, k); });
      takt(function (t) {
        var a = (t - start) / dauer; if (a > 1) { k.remove(); return false; }
        var dir = rueck ? -1 : 1, x = rueck ? rechts + 30 - a * (rechts - links + 60) : links - 30 + a * (rechts - links + 60);
        var ph = t * 7.5, hub = Math.abs(Math.sin(ph)) * 0.8, y = boden - 12 - hub;
        bein1.setAttribute("x1", x); bein1.setAttribute("y1", y); bein1.setAttribute("x2", x + Math.sin(ph) * 3.2); bein1.setAttribute("y2", boden - 1);
        bein2.setAttribute("x1", x); bein2.setAttribute("y1", y); bein2.setAttribute("x2", x - Math.sin(ph) * 3.2); bein2.setAttribute("y2", boden - 1);
        mantel.setAttribute("d", "M" + (x - 4) + " " + (y + 1) + " L" + (x - 3.4) + " " + (y - 14) + " Q" + x + " " + (y - 16.5) + " " + (x + 3.4) + " " + (y - 14) + " L" + (x + 4) + " " + (y + 1) + " Z");
        kopf.setAttribute("cx", x + dir * 0.6); kopf.setAttribute("cy", y - 18.5);
        muetze.setAttribute("d", "M" + (x - 3.6) + " " + (y - 19.5) + " Q" + x + " " + (y - 24) + " " + (x + 3.6) + " " + (y - 19.5) + " Z");
        var hx = x + dir * 15, hy = boden - 5 - Math.abs(Math.sin(ph * 1.6)) * 0.7;
        hund.setAttribute("cx", hx); hund.setAttribute("cy", hy);
        hkopf.setAttribute("cx", hx + dir * 6.5); hkopf.setAttribute("cy", hy - 2.2);
        leine.setAttribute("d", "M" + (x + dir * 3) + " " + (y - 7) + " Q" + (x + dir * 9) + " " + (y - 2) + " " + (hx + dir * 5) + " " + (hy - 2.5));
        hb.forEach(function (b, i) {
          var bx = hx + (i < 2 ? -4 : 4), sw = Math.sin(ph * 1.6 + (i % 2) * Math.PI) * 2;
          b.setAttribute("x1", bx); b.setAttribute("y1", hy + 1.5); b.setAttribute("x2", bx + sw); b.setAttribute("y2", boden - 0.5);
        });
        return true;
      });
    }
    takt(function (t) {
      if (!an || ruhig) return true;
      if (t > bisVogel) { voegel(); bisVogel = t + zufall(14, 32); }
      if (t > bisGeher) { geher(); bisGeher = t + zufall(40, 75); }
      return true;
    });
  }

  /* ------------------------------------------------------------------ Flur: jemand geht im Durchgang vorbei */
  function baueFlur(ebene, fl) {
    var g = el("g", { "clip-path": clip("leben-flur", "M" + fl.x + " " + fl.y + " h" + fl.b + " v" + fl.h + " h" + (-fl.b) + " Z") }, ebene);
    var bis = zufall(5, 12);
    function vorbei() {
      var p = el("path", { fill: "#3E565E", opacity: "0.95" }, g), start = jetzt, dauer = zufall(0.9, 1.4), rueck = Math.random() < 0.5;
      var oben = fl.y + fl.h * zufall(0.12, 0.2);
      takt(function (t) {
        var a = (t - start) / dauer; if (a > 1) { p.remove(); return false; }
        var x = rueck ? fl.x + fl.b + 40 - a * (fl.b + 80) : fl.x - 40 + a * (fl.b + 80);
        var hub = Math.abs(Math.sin(t * 9)) * 3;
        p.setAttribute("d", "M" + (x - 8) + " " + (oben + hub) + " a8 9 0 1 1 16 0 a8 9 0 1 1 -16 0 Z M" + (x - 22) + " " + (oben + 26 + hub) +
          " Q" + x + " " + (oben + 12 + hub) + " " + (x + 22) + " " + (oben + 26 + hub) + " L" + (x + 20) + " " + (fl.y + fl.h) + " L" + (x - 20) + " " + (fl.y + fl.h) + " Z");
        return true;
      });
    }
    takt(function (t) { if (an && !ruhig && t > bis) { vorbei(); bis = t + zufall(12, 30); } return true; });
  }

  /* ------------------------------------------------------------------ Vordergrund: jemand geht unscharf durchs Bild */
  function vordergrundGeher(ebene) {
    if (!an || ruhig) return;
    var unschaerfe = el("filter", { id: "leben-unscharf-" + Math.floor(jetzt * 1000), x: "-30%", y: "-30%", width: "160%", height: "160%" }, defs);
    el("feGaussianBlur", { stdDeviation: 7 }, unschaerfe);
    var rueck = Math.random() < 0.5, g = el("g", { filter: "url(#" + unschaerfe.id + ")", opacity: "0.93" }, ebene);
    var k = el("g", {}, g);
    function glied(farbe, laenge, breite, haut) {
      var gg = el("g", {}, k);
      el("path", { d: "M" + (-breite / 2) + " 0 L" + (breite / 2) + " 0 L" + (breite * 0.4) + " " + laenge + " L" + (-breite * 0.4) + " " + laenge + " Z", fill: farbe }, gg);
      if (haut) el("ellipse", { cx: 0, cy: laenge, rx: breite * 0.42, ry: breite * 0.5, fill: haut }, gg);
      return gg;
    }
    var beinH = glied("#1B3A42", 340, 54), armH = glied("#21474F", 270, 30, "#9E7558");
    el("path", { d: "M-60 -620 C-66 -480 -58 -400 -50 -330 L54 -330 C60 -420 64 -520 56 -620 Q0 -646 -60 -620 Z", fill: "#2B5662" }, k);
    el("rect", { x: -15, y: -660, width: 30, height: 48, fill: "#B8876A" }, k);
    el("ellipse", { cx: 8, cy: -708, rx: 46, ry: 54, fill: "#C4936F" }, k);
    el("path", { d: "M-40 -716 Q-44 -770 8 -766 Q50 -762 52 -728 Q26 -748 -2 -740 Q-24 -734 -30 -700 Z", fill: "#2A2420" }, k);
    el("ellipse", { cx: -40, cy: -714, rx: 16, ry: 20, fill: "#2A2420" }, k);   /* Zopf, Gesicht im Profil nach vorn */
    var beinV = glied("#244B54", 340, 56), armV = glied("#2B5662", 270, 32, "#B8876A");
    var start = jetzt, dauer = 2.6, s = 1.18;
    takt(function (t) {
      var a = (t - start) / dauer; if (a > 1) { g.remove(); unschaerfe.remove(); return false; }
      var x = rueck ? 1900 - a * 2200 : -300 + a * 2200, ph = (t - start) * Math.PI * 2 * 1.7;
      var hub = -Math.abs(Math.sin(ph)) * 16, sw = Math.sin(ph);
      k.setAttribute("transform", "translate(" + x.toFixed(1) + " " + (1090 + hub).toFixed(1) + ") scale(" + (rueck ? -s : s) + " " + s + ")");
      beinH.setAttribute("transform", "translate(0 -340) rotate(" + (-22 * sw).toFixed(1) + ")");
      beinV.setAttribute("transform", "translate(0 -340) rotate(" + (22 * sw).toFixed(1) + ")");
      armH.setAttribute("transform", "translate(-6 -605) rotate(" + (18 * sw).toFixed(1) + ")");
      armV.setAttribute("transform", "translate(6 -605) rotate(" + (-18 * sw).toFixed(1) + ")");
      return true;
    });
  }

  /* ------------------------------------------------------------------ EKG-Wagen: Bereitschaft, Schreiben, Papier */
  function baueWagen(ebene, w) {
    var g = el("g", { "class": "leben-wagen" }, ebene);
    var s = w.schirm;
    var glas = el("rect", { x: s[0], y: s[1], width: s[2], height: s[3], fill: GLAS, opacity: "0" }, g);
    var kurve = el("polyline", { fill: "none", stroke: PHOSPHOR, "stroke-width": 1.3, "stroke-linejoin": "round", opacity: "0" }, g);
    var hf = el("text", { x: s[0] + s[2] - 4, y: s[1] + 11, "text-anchor": "end", fill: PHOSPHOR, "font-size": 10,
      "font-family": "ui-monospace, Menlo, monospace", opacity: "0" }, g);
    var abl = el("text", { x: s[0] + 4, y: s[1] + 11, fill: PHOSPHOR, "font-size": 8, "font-family": "ui-monospace, Menlo, monospace", opacity: "0" }, g);
    abl.textContent = "II";
    var led = el("circle", { cx: w.led[0], cy: w.led[1], r: 2.3, fill: "#E8A33D" }, g);
    var p = w.papier;
    var papier = el("rect", { x: p[0], y: p[1], width: p[2], height: p[3], fill: "#F3EDE0", stroke: LINIE, "stroke-width": 1.2 }, g);
    papier.style.display = "none";
    wagen = { laeuft: false, seit: 0, papierH: p[3], glas: glas, kurve: kurve, hf: hf, abl: abl, led: led, papier: papier, def: w };
    var breite = s[2] - 6, fenster = 3.2;
    takt(function (t, dt) {
      if (!wagen.laeuft) {                    /* Bereitschaft: Bernstein-LED atmet, Schirm dunkel */
        led.setAttribute("fill", "#E8A33D");
        led.setAttribute("opacity", (an && !ruhig ? 0.45 + 0.45 * Math.sin(t * 2.2) : 0.7).toFixed(2));
        return true;
      }
      led.setAttribute("fill", PHOSPHOR); led.setAttribute("opacity", "0.95");
      var e = w.ekg, lauf = t - wagen.seit;
      if (e && e.werte && e.werte.length) {
        /* Sweep wie am Monitor: links neue Daten bis zum Schreibkopf, rechts der vorige Durchlauf, dazwischen eine Lücke */
        var dauerGesamt = e.werte.length / e.fs, kopf = (lauf % fenster) / fenster, runde = Math.floor(lauf / fenster);
        var pts = [], schritte = Math.round(breite * 1.5);
        for (var i = 0; i <= schritte; i++) {
          var a = i / schritte;
          if (Math.abs(a - kopf) < 0.05 && a > kopf) continue;
          var r = a <= kopf ? runde : runde - 1;
          if (r < 0) continue;
          var zeitpunkt = ((r * fenster + a * fenster) % dauerGesamt);
          var v = e.werte[Math.floor(zeitpunkt * e.fs)] || 0;
          pts.push((s[0] + 3 + a * breite).toFixed(1) + "," + (s[1] + s[3] * 0.7 - v * s[3] * 0.5).toFixed(1));
        }
        kurve.setAttribute("points", pts.join(" "));
      }
      if (lauf < 11) {                         /* zehn Sekunden schreiben: das Papier wächst */
        wagen.papierH = p[3] + Math.min(1, lauf / 10) * (w.papierMax - p[3]);
        papier.setAttribute("height", wagen.papierH.toFixed(1));
      }
      return true;
    });
  }
  function ekgAn(ja) {
    if (!wagen) return;
    wagen.laeuft = ja; wagen.seit = jetzt;
    [wagen.glas, wagen.kurve, wagen.hf, wagen.abl].forEach(function (e) { e.setAttribute("opacity", ja ? (e === wagen.glas ? "1" : "0.95") : "0"); });
    if (ja && wagen.def.ekg) wagen.hf.textContent = String(wagen.def.ekg.frequenz);
    wagen.papier.style.display = ja || wagen.papierH > wagen.def.papier[3] ? "" : "none";
    if (!ja) wagen.kurve.setAttribute("points", "");
  }

  /* ------------------------------------------------------------------ Handy vibriert (die Tochter ruft an) */
  function handy() {
    var F = figuren[cfg.handy.figur]; if (!F) return;
    var h = cfg.handy, start = jetzt;
    F.zittern = jetzt + 3.3;
    setzePose(F, h.pose, 3.6);
    var w = el("g", { fill: "none", stroke: LINIE, "stroke-width": 1.6, "stroke-linecap": "round" }, F.zusatz);
    [0, 1].forEach(function (i) {
      el("path", { d: "M" + (h.x - 6 - i * 6) + " " + (h.y - 7 - i * 3) + " Q" + (h.x - 11 - i * 6) + " " + h.y + " " + (h.x - 6 - i * 6) + " " + (h.y + 7 + i * 3) }, w);
    });
    takt(function (t) {
      var a = t - start; if (a > 3.4) { w.remove(); return false; }
      w.setAttribute("opacity", (Math.floor(a / 0.55) % 2 ? 0 : 0.85).toFixed(2));
      return true;
    });
  }

  /* ------------------------------------------------------------------ Schleife */
  var letztes = 0;
  function schleife(ms) {
    var t = ms / 1000;
    if (!t0) { t0 = t; letztes = t; }
    var dt = Math.min(0.1, t - letztes); letztes = t; jetzt = t;
    takte = takte.filter(function (fn) { return fn(t, dt) !== false; });
    global.requestAnimationFrame(schleife);
  }

  var bisVorbei = 0;
  function starte(wurzel, raum, bilder) {
    svg = wurzel; cfg = raum;
    ruhig = global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches;
    defs = svg.querySelector("defs") || el("defs", {}, svg);
    var ebene = function (n) { return svg.querySelector('[data-ebene="' + n + '"]'); };
    if (raum.fenster) baueFenster(ebene("hintergrund"), raum.fenster);
    if (raum.flur) baueFlur(ebene("hintergrund"), raum.flur);
    if (raum.uhr) baueUhr(ebene("hintergrund"), raum.uhr);
    if (raum.wagen) baueWagen(ebene("mittelgrund"), raum.wagen);
    Object.keys(raum.figuren || {}).forEach(function (n) { baueFigur(ebene("figuren"), n, raum.figuren[n], bilder[n]); });
    if (raum.licht) baueLicht(ebene("licht"), raum.licht);
    baueStimmung(ebene("stimmung"));
    bisVorbei = zufall(14, 26);
    takt(function (t) {
      if (an && !ruhig && t > bisVorbei) { vordergrundGeher(ebene("vordergrund")); bisVorbei = t + zufall(45, 90); }
      return true;
    });
    global.requestAnimationFrame(schleife);
  }

  global.Leben = {
    starte: starte,
    zeit: function (min) { spielzeit = min; stelleUhr(); },
    ereignis: function (name) {
      if (name === "handy") handy();
      else if (name === "vorbei") { var r = an; an = true; vordergrundGeher(svg.querySelector('[data-ebene="vordergrund"]')); an = r; }
      else if (name === "uhr_blick" && cfg.uhrBlick) setzePose(figuren[cfg.uhrBlick.figur], cfg.uhrBlick.pose, 2.2);
      else if (name === "ekg") ekgAn(true);
      else if (name === "ekg_aus") ekgAn(false);
    },
    bewegung: function (ja) { an = !!ja; },
    ruhig: function () { return ruhig; }
  };
})(window);
