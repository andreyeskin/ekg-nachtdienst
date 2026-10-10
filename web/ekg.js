/* EKG-Renderer fürs Spiel: echtes Millimeterpapier auf Canvas.
   Maßstab ist physikalisch definiert — mm/s (Papiervorschub) und mm/mV (Verstärkung).
   Ein "mm" auf dem Schirm = pxProMm Pixel; alles andere folgt daraus.          */
(function (global) {
  "use strict";

  var FARBE = {
    papier: "#FFF8F4", fein: "#F2C4B2", grob: "#DD8A6E",
    kurve: "#17181A", kurveMonitor: "#39E58C", papierMonitor: "#0A1512",
    zirkel: "#B01267", ziel: "#0E6B66"
  };

  function Streifen(leinwand, opt) {
    opt = opt || {};
    var ctx = leinwand.getContext("2d");
    var S = {
      werte: opt.werte || [],          /* mV */
      fs: opt.fs || 250,
      mmProS: opt.mmProS || 25,
      mmProMv: opt.mmProMv || 10,
      pxProMm: opt.pxProMm || 4,
      monitor: !!opt.monitor,          /* dunkler Monitor statt Papier */
      kalibrierung: opt.kalibrierung !== false,
      versatz: 0,                      /* Scroll-Position in Sekunden */
      zirkel: null                     /* {start, ende} in Sekunden */
    };

    function groesse() {
      var b = leinwand.clientWidth || 600, h = leinwand.clientHeight || 160;
      var dpr = global.devicePixelRatio || 1;
      if (leinwand.width !== Math.round(b * dpr) || leinwand.height !== Math.round(h * dpr)) {
        leinwand.width = Math.round(b * dpr);
        leinwand.height = Math.round(h * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { b: b, h: h };
    }

    function raster(b, h) {
      var mm = S.pxProMm, i, n;
      ctx.fillStyle = S.monitor ? FARBE.papierMonitor : FARBE.papier;
      ctx.fillRect(0, 0, b, h);
      if (S.monitor) {
        ctx.strokeStyle = "rgba(57,229,140,.13)"; ctx.lineWidth = 1;
        for (n = Math.ceil(b / (mm * 5)), i = 0; i <= n; i++) {
          ctx.beginPath(); ctx.moveTo(i * mm * 5 + .5, 0); ctx.lineTo(i * mm * 5 + .5, h); ctx.stroke();
        }
        for (n = Math.ceil(h / (mm * 5)), i = 0; i <= n; i++) {
          ctx.beginPath(); ctx.moveTo(0, i * mm * 5 + .5); ctx.lineTo(b, i * mm * 5 + .5); ctx.stroke();
        }
        return;
      }
      var spalten = Math.ceil(b / mm), zeilen = Math.ceil(h / mm);
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

    function zeichne() {
      var g = groesse(), b = g.b, h = g.h;
      raster(b, h);
      var pxProS = S.mmProS * S.pxProMm;
      var y0 = h / 2;
      var x = 0, i0 = Math.floor(S.versatz * S.fs), i, wert;
      if (S.kalibrierung && S.versatz === 0 && !S.monitor) {
        var k = S.pxProMm;
        ctx.strokeStyle = FARBE.kurve; ctx.lineWidth = Math.max(1, 0.3 * S.pxProMm);
        ctx.beginPath();
        ctx.moveTo(2 * k, y0); ctx.lineTo(4 * k, y0);
        ctx.lineTo(4 * k, y0 - S.mmProMv * k); ctx.lineTo(9 * k, y0 - S.mmProMv * k);
        ctx.lineTo(9 * k, y0); ctx.lineTo(12 * k, y0);
        ctx.stroke();
        x = 12 * k;
      }
      ctx.strokeStyle = S.monitor ? FARBE.kurveMonitor : FARBE.kurve;
      ctx.lineWidth = Math.max(1, (S.monitor ? 0.45 : 0.3) * S.pxProMm);
      ctx.lineJoin = "round"; ctx.lineCap = "round";
      if (S.monitor) { ctx.shadowColor = "rgba(57,229,140,.6)"; ctx.shadowBlur = 6; }
      ctx.beginPath();
      var erster = true;
      for (i = 0; x <= b && i0 + i < S.werte.length; i++) {
        wert = S.werte[(i0 + i) % S.werte.length];
        x = (S.kalibrierung && S.versatz === 0 && !S.monitor ? 12 * S.pxProMm : 0) + i / S.fs * pxProS;
        var y = y0 - wert * S.mmProMv * S.pxProMm;
        if (erster) { ctx.moveTo(x, y); erster = false; } else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      if (S.zirkel) {                                   /* Messzirkel */
        var xa = sekundeZuX(S.zirkel.start), xb = sekundeZuX(S.zirkel.ende);
        ctx.fillStyle = "rgba(176,18,103,.12)";
        ctx.fillRect(Math.min(xa, xb), 0, Math.abs(xb - xa), h);
        ctx.strokeStyle = FARBE.zirkel; ctx.lineWidth = 2;
        [xa, xb].forEach(function (xx) {
          ctx.beginPath(); ctx.moveTo(xx, 0); ctx.lineTo(xx, h); ctx.stroke();
        });
        var ms = Math.round(Math.abs(S.zirkel.ende - S.zirkel.start) * 1000);
        ctx.fillStyle = FARBE.zirkel;
        ctx.font = "600 " + Math.round(3.2 * S.pxProMm) + "px ui-monospace, Menlo, monospace";
        ctx.textAlign = "center";
        ctx.fillText(ms + " ms", (xa + xb) / 2, 4 * S.pxProMm);
      }
    }

    function sekundeZuX(s) {
      var vorlauf = (S.kalibrierung && S.versatz === 0 && !S.monitor) ? 12 * S.pxProMm : 0;
      return vorlauf + (s - S.versatz) * S.mmProS * S.pxProMm;
    }
    function xZuSekunde(x) {
      var vorlauf = (S.kalibrierung && S.versatz === 0 && !S.monitor) ? 12 * S.pxProMm : 0;
      return S.versatz + (x - vorlauf) / (S.mmProS * S.pxProMm);
    }

    /* Messen mit Finger, Pencil oder Maus */
    function messbar(beiMessung) {
      var zieht = false;
      function pos(e) {
        var r = leinwand.getBoundingClientRect();
        return xZuSekunde((e.clientX !== undefined ? e.clientX : e.touches[0].clientX) - r.left);
      }
      leinwand.addEventListener("pointerdown", function (e) {
        e.preventDefault(); zieht = true;
        var s = pos(e); S.zirkel = { start: s, ende: s }; zeichne();
        try { leinwand.setPointerCapture(e.pointerId); } catch (x) {}
      });
      leinwand.addEventListener("pointermove", function (e) {
        if (!zieht) return;
        S.zirkel.ende = pos(e); zeichne();
      });
      leinwand.addEventListener("pointerup", function (e) {
        if (!zieht) return;
        zieht = false; S.zirkel.ende = pos(e); zeichne();
        if (beiMessung) beiMessung(Math.round(Math.abs(S.zirkel.ende - S.zirkel.start) * 1000),
                                   Math.min(S.zirkel.start, S.zirkel.ende));
      });
    }

    /* Monitor-Modus: Kurve läuft durch */
    var laeuft = null;
    function starteLauf(tempo) {
      stoppeLauf();
      var t0 = performance.now(), start = S.versatz;
      function tick(t) {
        S.versatz = start + (t - t0) / 1000 * (tempo || 1);
        var dauer = S.werte.length / S.fs;
        if (S.versatz > dauer - 4) { start -= (dauer - 4); t0 = t; S.versatz = 0; }
        zeichne();
        laeuft = requestAnimationFrame(tick);
      }
      laeuft = requestAnimationFrame(tick);
    }
    function stoppeLauf() { if (laeuft) cancelAnimationFrame(laeuft); laeuft = null; }

    return {
      zeichne: zeichne, messbar: messbar, starteLauf: starteLauf, stoppeLauf: stoppeLauf,
      setze: function (o) { for (var k in o) if (o.hasOwnProperty(k)) S[k] = o[k]; zeichne(); },
      stand: S, sekundeZuX: sekundeZuX, xZuSekunde: xZuSekunde
    };
  }

  global.EKG = { Streifen: Streifen, FARBE: FARBE };
})(window);
