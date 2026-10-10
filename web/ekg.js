/* EKG-Renderer fürs Spiel: echtes Millimeterpapier auf Canvas.
   Der Maßstab ist physikalisch definiert — mm/s (Papiervorschub) und mm/mV
   (Verstärkung). Ein „mm" auf dem Schirm = pxProMm Pixel; alles folgt daraus.
   Wer ein Fenster angibt (von/dauer), bekommt pxProMm automatisch so, dass
   genau dieses Fenster in die Leinwand passt.                                */
(function (global) {
  "use strict";

  var FARBE = {
    papier: "#FFF8F4", fein: "#F0C2B0", grob: "#DB8A6E",
    kurve: "#17181A", kurveMonitor: "#39E58C", papierMonitor: "#07130F",
    zirkel: "#C2185B", loesung: "#0E7C6B"
  };
  var VORLAUF_MM = 12;                      /* Platz für die Eichzacke */

  function Streifen(leinwand, opt) {
    opt = opt || {};
    var ctx = leinwand.getContext("2d");
    var S = {
      werte: opt.werte || [],               /* mV */
      fs: opt.fs || 250,
      mmProS: opt.mmProS || 25,
      mmProMv: opt.mmProMv || 10,
      pxProMm: opt.pxProMm || 0,            /* 0 = aus dem Fenster rechnen */
      monitor: !!opt.monitor,
      kalibrierung: opt.kalibrierung !== false,
      raster: opt.raster !== false,
      von: opt.von || 0,                    /* Fensteranfang in Sekunden */
      dauer: opt.dauer || 0,                /* 0 = so viel wie hineinpasst */
      zirkel: null,                         /* {start, ende} in Sekunden */
      loesung: null,                        /* {start, ende} in Sekunden */
      marken: null                          /* [{s, farbe}] senkrechte Hilfslinien */
    };

    function groesse() {
      var b = leinwand.clientWidth || leinwand.width || 600;
      var h = leinwand.clientHeight || leinwand.height || 160;
      var dpr = global.devicePixelRatio || 1;
      if (leinwand.width !== Math.round(b * dpr) || leinwand.height !== Math.round(h * dpr)) {
        leinwand.width = Math.round(b * dpr);
        leinwand.height = Math.round(h * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { b: b, h: h };
    }

    function massstab(b) {
      if (S.pxProMm > 0) return S.pxProMm;
      var vorlauf = S.kalibrierung ? VORLAUF_MM : 2;
      var dauer = S.dauer || (S.werte.length / S.fs - S.von);
      if (!(dauer > 0)) return 4;
      return Math.max(0.8, (b - 8) / (vorlauf + dauer * S.mmProS));
    }

    function vorlaufPx(mm) { return (S.kalibrierung ? VORLAUF_MM : 2) * mm; }

    function raster(b, h, mm) {
      ctx.fillStyle = S.monitor ? FARBE.papierMonitor : FARBE.papier;
      ctx.fillRect(0, 0, b, h);
      if (!S.raster) return;
      var i, n;
      if (S.monitor) {
        ctx.strokeStyle = "rgba(57,229,140,.14)"; ctx.lineWidth = 1;
        for (n = Math.ceil(b / (mm * 5)), i = 0; i <= n; i++) {
          ctx.beginPath(); ctx.moveTo(i * mm * 5 + .5, 0); ctx.lineTo(i * mm * 5 + .5, h); ctx.stroke();
        }
        for (n = Math.ceil(h / (mm * 5)), i = 0; i <= n; i++) {
          ctx.beginPath(); ctx.moveTo(0, i * mm * 5 + .5); ctx.lineTo(b, i * mm * 5 + .5); ctx.stroke();
        }
        return;
      }
      var spalten = Math.ceil(b / mm), zeilen = Math.ceil(h / mm);
      if (spalten > 4000 || zeilen > 4000) return;          /* Schutz gegen Unsinn */
      for (i = 0; i <= spalten; i++) {
        ctx.strokeStyle = (i % 5 === 0) ? FARBE.grob : FARBE.fein;
        ctx.lineWidth = (i % 5 === 0) ? 1 : 0.5;
        ctx.beginPath(); ctx.moveTo(i * mm + .5, 0); ctx.lineTo(i * mm + .5, h); ctx.stroke();
      }
      for (i = 0; i <= zeilen; i++) {
        ctx.strokeStyle = (i % 5 === 0) ? FARBE.grob : FARBE.fein;
        ctx.lineWidth = (i % 5 === 0) ? 1 : 0.5;
        ctx.beginPath(); ctx.moveTo(0, i * mm + .5); ctx.lineTo(b, i * mm + .5); ctx.stroke();
      }
    }

    var letzteMm = 4, letzteB = 600;

    function zeichne() {
      var g = groesse(), b = g.b, h = g.h;
      if (!ctx || !(b > 10) || !(h > 10)) return;           /* versteckte Leinwand */
      var mm = massstab(b);
      letzteMm = mm; letzteB = b;
      raster(b, h, mm);
      var y0 = h / 2, vl = vorlaufPx(mm);

      if (S.kalibrierung && !S.monitor) {                    /* 1-mV-Eichzacke */
        ctx.strokeStyle = FARBE.kurve;
        ctx.lineWidth = Math.max(1, 0.3 * mm);
        ctx.lineJoin = "round";
        ctx.beginPath();
        ctx.moveTo(1.5 * mm, y0); ctx.lineTo(3.5 * mm, y0);
        ctx.lineTo(3.5 * mm, y0 - S.mmProMv * mm); ctx.lineTo(8.5 * mm, y0 - S.mmProMv * mm);
        ctx.lineTo(8.5 * mm, y0); ctx.lineTo(VORLAUF_MM * mm - 1, y0);
        ctx.stroke();
      }

      var i0 = Math.max(0, Math.round(S.von * S.fs));
      var dauer = S.dauer || (b - vl) / (S.mmProS * mm);
      var i1 = Math.min(S.werte.length, i0 + Math.ceil(dauer * S.fs) + 2);
      ctx.strokeStyle = S.monitor ? FARBE.kurveMonitor : FARBE.kurve;
      ctx.lineWidth = Math.max(1.1, (S.monitor ? 0.42 : 0.3) * mm);
      ctx.lineJoin = "round"; ctx.lineCap = "round";
      if (S.monitor) { ctx.shadowColor = "rgba(57,229,140,.55)"; ctx.shadowBlur = 7; }
      ctx.beginPath();
      for (var i = i0; i < i1; i++) {
        var x = vl + (i - i0) / S.fs * S.mmProS * mm;
        var y = y0 - S.werte[i] * S.mmProMv * mm;
        if (i === i0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      if (S.marken) {
        S.marken.forEach(function (m) {
          var x = sekundeZuX(m.s);
          if (x < 0 || x > b) return;
          ctx.strokeStyle = m.farbe || FARBE.loesung;
          ctx.lineWidth = 1.4; ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.moveTo(x, 6); ctx.lineTo(x, h - 6); ctx.stroke();
          ctx.setLineDash([]);
        });
      }
      if (S.loesung) spanne(S.loesung, FARBE.loesung, h, mm, "Lösung", true);
      if (S.zirkel) spanne(S.zirkel, FARBE.zirkel, h, mm, null, false);
    }

    function spanne(sp, farbe, h, mm, beschriftung, unten) {
      var xa = sekundeZuX(sp.start), xb = sekundeZuX(sp.ende);
      var links = Math.min(xa, xb), breite = Math.abs(xb - xa);
      ctx.fillStyle = farbe; ctx.globalAlpha = 0.12;
      ctx.fillRect(links, 0, breite, h);
      ctx.globalAlpha = 1;
      ctx.strokeStyle = farbe; ctx.lineWidth = 2;
      [xa, xb].forEach(function (xx) {
        ctx.beginPath(); ctx.moveTo(xx, 0); ctx.lineTo(xx, h); ctx.stroke();
      });
      var ms = Math.round(Math.abs(sp.ende - sp.start) * 1000);
      ctx.fillStyle = farbe;
      ctx.font = "600 " + Math.max(11, Math.round(3.0 * mm)) + "px ui-monospace, Menlo, monospace";
      ctx.textAlign = "center";
      ctx.fillText((beschriftung ? beschriftung + " " : "") + ms + " ms",
                   (xa + xb) / 2, unten ? h - 2.5 * mm : Math.max(12, 3.6 * mm));
    }

    function sekundeZuX(s) { return vorlaufPx(letzteMm) + (s - S.von) * S.mmProS * letzteMm; }
    function xZuSekunde(x) { return S.von + (x - vorlaufPx(letzteMm)) / (S.mmProS * letzteMm); }

    /* Messen mit Finger, Pencil oder Maus */
    function messbar(beiMessung, beiZug) {
      var zieht = false;
      function pos(e) {
        var r = leinwand.getBoundingClientRect();
        var cx = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0].clientX) || 0;
        return xZuSekunde(cx - r.left);
      }
      leinwand.style.touchAction = "none";
      leinwand.addEventListener("pointerdown", function (e) {
        e.preventDefault(); zieht = true;
        var s = pos(e); S.zirkel = { start: s, ende: s }; zeichne();
        try { leinwand.setPointerCapture(e.pointerId); } catch (x) {}
      });
      leinwand.addEventListener("pointermove", function (e) {
        if (!zieht) return;
        S.zirkel.ende = pos(e); zeichne();
        if (beiZug) beiZug(Math.round(Math.abs(S.zirkel.ende - S.zirkel.start) * 1000));
      });
      function los(e) {
        if (!zieht) return;
        zieht = false; S.zirkel.ende = pos(e); zeichne();
        if (beiMessung) {
          beiMessung(Math.round(Math.abs(S.zirkel.ende - S.zirkel.start) * 1000),
                     Math.min(S.zirkel.start, S.zirkel.ende),
                     Math.max(S.zirkel.start, S.zirkel.ende));
        }
      }
      leinwand.addEventListener("pointerup", los);
      leinwand.addEventListener("pointercancel", los);
    }

    /* Monitor-Modus: die Kurve läuft durch */
    var laeuft = null;
    function starteLauf(tempo) {
      stoppeLauf();
      var t0 = null, start = S.von, dauerGesamt = S.werte.length / S.fs;
      function tick(t) {
        if (t0 === null) t0 = t;
        S.von = start + (t - t0) / 1000 * (tempo || 1);
        if (S.von > dauerGesamt - (S.dauer || 4)) { start = 0; t0 = t; S.von = 0; }
        zeichne();
        laeuft = global.requestAnimationFrame(tick);
      }
      laeuft = global.requestAnimationFrame(tick);
    }
    function stoppeLauf() {
      if (laeuft) global.cancelAnimationFrame(laeuft);
      laeuft = null;
    }

    return {
      zeichne: zeichne, messbar: messbar, starteLauf: starteLauf, stoppeLauf: stoppeLauf,
      setze: function (o) { for (var k in o) if (o.hasOwnProperty(k)) S[k] = o[k]; zeichne(); },
      stand: S, sekundeZuX: sekundeZuX, xZuSekunde: xZuSekunde, laeuftGerade: function () { return !!laeuft; }
    };
  }

  global.EKG = { Streifen: Streifen, FARBE: FARBE, VORLAUF_MM: VORLAUF_MM };
})(window);
