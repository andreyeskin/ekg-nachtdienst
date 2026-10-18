/* Prüft den Prototyp Fall 1 in echtem Chromium (tools/browser.mjs, nichts wird installiert).

     node prototyp/fall1/pruefe.mjs [bau/prototyp_fall1.html] [bau/prototyp_fall1_schuss]

   Wege: (a) der gute Weg bis zum Endbildschirm, mit einer echten Zirkelmessung per Maus; (b) Irrwege
   (versprochen, tochter_verraten, heim_empfohlen, brady_argument, revers, Anruf später, Falk vor dem EKG,
   Rückwege zu Wagen und Patient); (c) 1024 × 768 mit reduced-motion und Menü „Bewegung aus"; (d) Zufallsläufe:
   jeder Zustand hat eine klickbare Fortsetzung, das Ende wird erreicht. Dazu: keine Konsolenfehler, kein
   Textüberlauf im Dialogkasten, Repliken ≤ 220 Zeichen und ≤ 2 Sätze, Optionen ≤ 64 Zeichen, kein Gedankenstrich,
   keine offenen Platzhalter, keine Messwerte fest im Falltext. Schnappschüsse für den Koordinator.          */
import { starteBrowser } from "../../tools/browser.mjs";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const WURZEL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const DATEI = path.resolve(process.argv[2] || path.join(WURZEL, "bau", "prototyp_fall1.html"));
const BILDER = path.resolve(process.argv[3] || path.join(WURZEL, "bau", "prototyp_fall1_schuss"));
fs.mkdirSync(BILDER, { recursive: true });

const fehler = [], zeilen = [];
function ok(was, bed, zusatz = "") {
  zeilen.push((bed ? "  ok  " : "FEHLER") + "  " + was + (zusatz ? "  — " + zusatz : ""));
  if (!bed) fehler.push(was + (zusatz ? ": " + zusatz : ""));
  return bed;
}

/* ------------------------------------------------------------------ statisch: keine Messwerte im Falltext */
{
  const daten = fs.readFileSync(path.join(WURZEL, "prototyp", "fall1", "daten.js"), "utf8")
    .replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "")
    .replace(/werte: \{[^}]*\}/, "");                       /* feste Fallwerte (Puls, Blutdruck …) laufen über `werte` */
  const satz = JSON.parse(fs.readFileSync(path.join(WURZEL, "data", "ekg_daten.json"), "utf8")).find((x) => x.id === 39);
  const verboten = new Set([satz.mess.pq, satz.mess.qrs, satz.mess.rr, satz.mess.frequenz]);
  satz.schlaege.forEach((s, i) => {
    if (s.p0 !== undefined) verboten.add(Math.round((s.q0 - s.p0) * 1000));
    verboten.add(Math.round((s.q1 - s.q0) * 1000));
    const n = satz.schlaege[i + 1];
    if (n) { const rr = Math.round((n.r - s.r) * 1000); verboten.add(rr); verboten.add(Math.round(60000 / rr)); }
  });
  const treffer = [...verboten].filter((v) => new RegExp("\\b" + v + "\\b").test(daten));
  ok("daten.js: keine Messwerte aus LUDB 39 fest im Text (nur Platzhalter)", !treffer.length, treffer.join(", "));
  ok("daten.js: kein Gedankenstrich", !daten.includes("—"));
}

const browser = await starteBrowser();

/* ------------------------------------------------------------------ ein Lauf */
async function lauf(name, opt, plan) {
  const kontext = await browser.newContext(opt);
  const p = await kontext.newPage();
  const eigene = [];
  p.on("pageerror", (e) => eigene.push("Seitenfehler: " + String(e.message || e).slice(0, 200)));
  p.on("console", (m) => { if (m.type() === "error") eigene.push("Konsole: " + m.text().slice(0, 200)); });
  await p.goto("file://" + DATEI);
  await p.waitForSelector("#titel-los");
  await p.evaluate(() => window.__prototyp.schnell(true));
  let nr = 0;
  const gesehen = new Set(), schussVon = new Set();
  async function schuss(n, warte = 150) {
    if (!plan.schuesse) return;
    await p.waitForTimeout(warte);
    nr++;
    await p.screenshot({ path: path.join(BILDER, `${plan.kurz}_${String(nr).padStart(2, "0")}_${n}.png`) });
  }
  if (plan.schuesse) await schuss("titel", 300);
  await p.click("#titel-los");
  await p.waitForTimeout(80);

  const ueberlauf = [];
  const gemacht = new Set();          /* einmalige Zusatzhandlungen */
  let schritte = 0, ende = false, letzteMessung = null, rhythmusVersuche = 0, zuletzt = "";
  const rng = plan.zufall ? mulberry(plan.zufall) : null;
  const MAX = plan.zufall ? 2500 : 900;

  while (schritte++ < MAX) {
    const s = await p.evaluate(() => {
      const q = (sel) => document.querySelector(sel);
      const dlg = q(".dialog.an");
      return {
        dlg: dlg ? {
          knoten: dlg.dataset.knoten, wer: dlg.dataset.wer,
          opts: [...dlg.querySelectorAll(".dialog-antwort:not(.weiter)")].map((b) => b.dataset.text),
          weiter: !!dlg.querySelector(".dialog-antwort.weiter")
        } : null,
        fen: [...document.querySelectorAll(".raetsel.an")].map((e) => e.id),
        seite: (q(".seite.an") || {}).id || null,
        huelle: (q(".huelle-hof.an") || {}).id || null,
        mappe: !!q(".mappe.an"),
        z: window.__prototyp.zustand(), rw: window.FALL1.__rw()
      };
    });
    const f = new Set(s.z.flags);
    const sig = JSON.stringify([s.dlg && s.dlg.knoten, s.fen, s.seite, s.z.minuten, s.z.flags.length]);

    /* ---- Seiten */
    if (s.seite === "ende-seite") {
      if (plan.schuesse && !schussVon.has("ende")) { schussVon.add("ende"); await schuss("ende"); }
      ende = true; break;
    }
    if (s.seite === "epilog-seite") {
      if (plan.schuesse && !schussVon.has("epilog")) { schussVon.add("epilog"); await p.click(".seite-weiter"); await p.click(".seite-weiter"); await schuss("epilog"); continue; }
      await p.click(".seite-weiter"); await p.waitForTimeout(30); continue;
    }
    if (s.huelle) { await p.click(`#${s.huelle} .zu, #${s.huelle} #menue-weiter`); continue; }
    if (s.mappe) { await p.click("#mappe .zu"); continue; }

    /* ---- Fenster */
    if (s.fen.length) {
      const fen = s.fen[s.fen.length - 1];
      if (plan.schuesse && plan.schuesse[fen] && !schussVon.has(fen)) { schussVon.add(fen); await schuss(plan.schuesse[fen], 250); }
      if (fen === "befund-hof") { await p.click("#befund-hof .uebernehmen"); }
      else if (fen === "frage-hof") {
        const w = await p.$("#frage-hof .weiter:not([hidden])");
        if (w) { await w.click(); rhythmusVersuche = 0; }
        else {
          const wahl = plan.zufall ? null : (plan.rhythmus || ["Sinusrhythmus"])[Math.min(rhythmusVersuche, (plan.rhythmus || [1]).length - 1)];
          const knoepfe = await p.$$("#frage-hof .frage-wahl .knopf:not([disabled])");
          if (!knoepfe.length) { await p.waitForTimeout(80); continue; }
          let ziel = null;
          if (wahl) for (const k of knoepfe) if ((await k.getAttribute("data-text")) === wahl) ziel = k;
          if (!ziel) ziel = knoepfe[Math.floor((rng ? rng() : 0) * knoepfe.length)];
          await ziel.click(); rhythmusVersuche++;
          await p.waitForTimeout(90);
        }
      } else if (fen === "wahl-hof") {
        const karten = new Set(s.z.karten);
        const fehlt = { rr: !karten.has("frequenz"), pq: !karten.has("pq"), qrs: !karten.has("qrs") };
        let was = null;
        if (rng) was = rng() < 0.6 ? ["rr", "pq", "qrs"][Math.floor(rng() * 3)] : null;
        else if (s.rw && s.rw.art === "wagen") was = fehlt.rr ? "rr" : fehlt.pq ? "pq" : null;
        else was = (plan.messen || ["rr", "pq"]).find((m) => fehlt[m] && !gemacht.has("mess_" + m)) || null;
        if (was) {
          gemacht.add("mess_" + was); letzteMessung = was;
          const text = { rr: "Den RR-Abstand", pq: "Die PQ-Zeit", qrs: "Die QRS-Breite" }[was];
          await p.click(`#wahl-hof .frage-wahl .knopf[data-text^="${text}"]`);
        } else await p.click("#wahl-hof .knopf.genug");
      } else if (fen === "zirkel-hof") {
        if (rng && rng() < 0.15) { await p.click("#zirkel-hof .zu"); continue; }
        const sichtbar = await p.$("#zirkel-hof .uebernehmen:not([hidden])");
        if (!sichtbar) {
          if (plan.echt === letzteMessung && !gemacht.has("echt")) {
            gemacht.add("echt");
            await p.waitForTimeout(150);
            const pos = await p.evaluate((was) => {
              const hof = document.getElementById("zirkel-hof"), st = hof.__streifen, cv = hof.querySelector("canvas");
              const r = cv.getBoundingClientRect(), sl = window.__prototyp.satz().schlaege;
              const von = { pq: "p0", qrs: "q0", rr: "r" }[was], bis = { pq: "q0", qrs: "q1", rr: "r" }[was];
              for (let i = 0; i < sl.length; i++) {
                const a = sl[i][von], b = was === "rr" ? (sl[i + 1] || {}).r : sl[i][bis];
                if (a === undefined || b === undefined || a < st.stand.von) continue;
                return { y: r.top + r.height * 0.5, x1: r.left + st.sekundeZuX(a), x2: r.left + st.sekundeZuX(b), ms: Math.round((b - a) * 1000) };
              }
              return null;
            }, letzteMessung);
            await p.mouse.move(pos.x1, pos.y); await p.mouse.down();
            await p.mouse.move((pos.x1 + pos.x2) / 2, pos.y + 6, { steps: 4 });
            await p.mouse.move(pos.x2, pos.y, { steps: 6 }); await p.mouse.up();
            await p.waitForTimeout(120);
            const angenommen = await p.$("#zirkel-hof .uebernehmen:not([hidden])");
            ok(`${name}: echte Zirkelmessung ${letzteMessung.toUpperCase()} mit der Maus angenommen`, !!angenommen, pos.ms + " ms");
            if (!angenommen) await p.evaluate(() => window.__prototyp.miss(0));
          } else {
            const v = await p.evaluate((x) => window.__prototyp.miss(x), plan.zufall ? Math.round((rng() - 0.5) * 30) : 0);
            if (v === null) { await p.waitForTimeout(80); continue; }
            await p.waitForTimeout(40);
            if (!(await p.$("#zirkel-hof .uebernehmen:not([hidden])"))) await p.evaluate(() => window.__prototyp.miss(0));
          }
          if (plan.schuesse && !schussVon.has("zirkel_ok")) { schussVon.add("zirkel_ok"); await schuss("zirkel_gemessen"); }
        }
        await p.click("#zirkel-hof .uebernehmen");
      } else if (fen === "stand-hof") {
        const knopf = await p.$("#stand-hof .stand-los:not([hidden])");
        const t = await p.textContent("#stand-hof .raetsel-innen");
        ok(`${name}: Stand zeigt die dramatische Frage mit Frist`, t.includes("Darf Herr Baum heim?") && /Falk|Entschieden/.test(t));
        if (knopf && (!rng || rng() < 0.8)) await knopf.click(); else await p.click("#stand-hof .zu");
      } else if (fen === "verdacht-hof") { await p.click("#verdacht-hof .zu"); }
      else { ok(`${name}: unbekanntes Fenster ${fen}`, false); break; }
      await p.waitForTimeout(40);
      continue;
    }

    /* ---- Dialog */
    if (s.dlg) {
      const k = s.dlg.knoten;
      if (!gesehen.has(k)) {
        gesehen.add(k);
        if (plan.schuesse && plan.schuesse[k]) await schuss(plan.schuesse[k], k === "m0" ? 1100 : 200);
        if (plan.beiKnoten && plan.beiKnoten[k]) await plan.beiKnoten[k](p, s);
        const u = await p.evaluate(() => {
          const h = document.querySelector(".dialog.an .dialog-innen"), pr = [];
          const r = h.getBoundingClientRect();
          if (r.top < -1 || r.bottom > window.innerHeight + 1) pr.push("Kasten außerhalb " + Math.round(r.top) + "/" + Math.round(r.bottom));
          if (h.scrollHeight > h.clientHeight + 2) pr.push("Kasten scrollt " + h.scrollHeight + ">" + h.clientHeight);
          document.querySelectorAll(".dialog.an .dialog-antwort, .dialog.an .dialog-text, .dialog.an .dialog-warum").forEach((e) => {
            if (e.scrollWidth > e.clientWidth + 2) pr.push("zu breit: " + e.textContent.slice(0, 40));
            if (e.classList.contains("dialog-antwort") && e.getBoundingClientRect().height < 43.5) pr.push("Tippfläche < 44 px");
          });
          return pr;
        });
        if (u.length) ueberlauf.push(k + ": " + u.join("; "));
      }
      if (s.dlg.opts.length) {
        let wahl = null;
        if (rng) wahl = s.dlg.opts[Math.floor(rng() * s.dlg.opts.length)];
        else {
          for (const regel of plan.wahl) {
            wahl = s.dlg.opts.find((o) => (regel instanceof RegExp ? regel.test(o) : o.startsWith(regel)));
            if (wahl) break;
          }
        }
        if (!wahl) { ok(`${name}: keine passende Option in ${k}`, false, s.dlg.opts.join(" | ")); break; }
        const i = s.dlg.opts.indexOf(wahl);
        await p.click(`.dialog.an .dialog-antwort:not(.weiter) >> nth=${i}`);
      } else if (s.dlg.weiter) {
        await p.click(".dialog.an .dialog-antwort.weiter");
      } else { ok(`${name}: Dialog ohne Fortsetzung in ${k}`, false); break; }
      await p.waitForTimeout(25);
      continue;
    }

    /* ---- Raum: keine Fenster offen. Erst warten, ob die Uhr Falk bringt (Leerlauf). */
    if (sig !== zuletzt) { zuletzt = sig; await p.waitForTimeout(90); continue; }
    if (plan.extra) { const e = await plan.extra(p, s, gemacht, schuss); if (e) continue; }
    let ziel;
    if (rng) {
      const r = rng();
      ziel = r < 0.3 ? "herrk" : r < 0.5 ? "wagen" : r < 0.72 ? "marlene" : r < 0.9 ? "stand" : r < 0.95 ? "mappe" : "verdacht";
    } else if (s.rw && !s.rw.erfuellt) ziel = s.rw.art === "wagen" ? "wagen" : "herrk";
    else if (s.rw) ziel = "stand";
    else if (!f.has("r1_fertig")) ziel = "herrk";
    else if (!f.has("ekg_geschrieben")) ziel = plan.vorEkg(f, s);
    else ziel = "stand";
    const vorher = JSON.stringify(s.z);
    if (ziel === "stand") await p.click("#hud-stand");
    else if (ziel === "mappe") await p.click("#hud-mappe");
    else if (ziel === "verdacht") await p.click("#hud-verdacht");
    else await p.click(`[data-feld="${ziel}"]`);
    await p.waitForTimeout(60);
    const nachher = await p.evaluate(() => JSON.stringify(window.__prototyp.zustand()) + "|" + !!document.querySelector(".dialog.an, .raetsel.an, .mappe.an"));
    if (!rng && nachher === vorher + "|false") {
      const meld = await p.evaluate(() => [...document.querySelectorAll(".meldung")].map((m) => m.textContent).join(" | "));
      if (!meld) { ok(`${name}: Klick auf ${ziel} ohne Wirkung (Softlock?)`, false, s.z.zeit); break; }
    }
  }

  ok(`${name}: Endbildschirm erreicht`, ende, `${schritte} Schritte`);
  const z = await p.evaluate(() => window.__prototyp.zustand());
  const texte = await p.evaluate(() => window.__prototyp.texte());
  /* Textregeln */
  const lang = [], saetze = [], optLang = [], strich = [], offen = [];
  for (const t of texte) {
    if (!t.text) continue;
    if (t.text.includes("—")) strich.push(t.text.slice(0, 50));
    if (/\{\w+\}/.test(t.text)) offen.push(t.text.slice(0, 60));
    if (t.art === "replik" && t.wer !== "erzaehler") {
      if (t.text.length > 220) lang.push(t.text.length + ": " + t.text.slice(0, 40));
      const n = (t.text.match(/[.!?](\s|$)/g) || []).length;
      if (n > 2) saetze.push(n + ": " + t.text.slice(0, 50));
    }
    if (t.art === "option" && t.text.length > 64) optLang.push(t.text.length + ": " + t.text);
  }
  ok(`${name}: Repliken ≤ 220 Zeichen`, !lang.length, lang.slice(0, 3).join(" / "));
  ok(`${name}: Repliken ≤ 2 Sätze`, !saetze.length, saetze.slice(0, 3).join(" / "));
  ok(`${name}: Optionen ≤ 64 Zeichen`, !optLang.length, optLang.slice(0, 3).join(" / "));
  ok(`${name}: kein Gedankenstrich im Spieltext`, !strich.length, strich.slice(0, 3).join(" / "));
  ok(`${name}: keine offenen Platzhalter`, !offen.length, offen.slice(0, 3).join(" / "));
  ok(`${name}: kein Textüberlauf im Dialogkasten`, !ueberlauf.length, ueberlauf.slice(0, 4).join(" / "));
  if (plan.pruefe) await plan.pruefe(p, z, texte, name);
  ok(`${name}: keine Konsolen- oder Seitenfehler`, !eigene.length, eigene.slice(0, 3).join(" / "));
  await kontext.close();
  return z;
}

function mulberry(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const FLAGS = ["versprochen", "anruf_spaeter", "tochter_beruhigt", "tochter_verraten", "heim_empfohlen",
               "brady_argument", "falk_gewartet", "revers", "senta_geloest"];
async function pruefeEnde(p, z, name, erwartet) {
  const gesetzt = await p.$$eval("#ende-gesetzt li[data-flag]", (l) => l.map((e) => e.dataset.flag)).catch(() => []);
  ok(`${name}: Endbildschirm listet die gesetzten Flags`, JSON.stringify(gesetzt.sort()) === JSON.stringify([...erwartet].sort()), gesetzt.join(", "));
  const imZustand = FLAGS.filter((f) => z.flags.includes(f));
  ok(`${name}: Flags im Zustand wie erwartet`, JSON.stringify(imZustand.sort()) === JSON.stringify([...erwartet].sort()), imZustand.join(", "));
  const v = z.verdacht;
  const soll = { reflex: "unwahrscheinlich", kreislauf: "unwahrscheinlich", rhythmus: "bewiesen", struktur: "dagegen",
                 krampf: "unwahrscheinlich", tia: "unwahrscheinlich", zucker: "unwahrscheinlich", sturz: "unwahrscheinlich" };
  const abw = Object.keys(soll).filter((k) => v[k] !== soll[k]).map((k) => k + "=" + v[k]);
  ok(`${name}: Verdachtsliste am Ende wie §4.3 (Herzrhythmus im Epilog bewiesen)`, !abw.length, abw.join(", "));
  const karten = ["bogen", "anamnese", "medis", "fremd", "unters", "rhythmus", "frequenz", "pq", "uebergabe", "entscheidung", "epilog"];
  const fehlen = karten.filter((k) => !z.karten.includes(k));
  ok(`${name}: alle Karten in der Mappe`, !fehlen.length, fehlen.join(", "));
  ok(`${name}: Uhr am Ende mindestens 07:40`, z.minuten >= 460, z.zeit);
}
function replik(texte, knoten) { return texte.filter((t) => t.art === "replik" && t.knoten === knoten).map((t) => t.text); }
function hatText(texte, teil) { return texte.some((t) => t.text && t.text.includes(teil)); }

const SCHUESSE = {
  m0: "marlene_tresen", b_erz: "herr_baum_runde1", r3_2: "wendung", w2: "marlene_wagen", e_ruhig: "ekg_schirm",
  e_handy: "handy", t_ende2: "telefon", f2: "falk_ankunft", is_ok1: "isbar_is", zirkel1: "falk_zirkel", b1: "isbar_b",
  g0: "gegenrede", h_ende: "gegenrede_umgekehrt", nachgeben: "falk_gibt_nach", tab0: "tabletten", bett1b: "falk_bett",
  s0b: "schluss", s5f: "jacke", ab_e2: "schlussbild",
  "frage-hof": "rhythmusfrage", "zirkel-hof": "zirkel", "stand-hof": "stand", "befund-hof": "untersuchung", "wahl-hof": "messwahl"
};

/* ------------------------------------------------------------------ (a) der gute Weg */
let mappeGeprueft = false;
await lauf("a gut", { viewport: { width: 1366, height: 1024 } }, {
  kurz: "a", schuesse: SCHUESSE, echt: "pq", messen: ["rr", "pq"],
  beiKnoten: {
    g0: async (p) => {
      await p.click('.dialog.an .dialog-hud-knopf[data-panel="verdacht"]');
      const auf = await p.$("#verdacht-hof.an");
      ok("a gut: Verdachtsliste mitten in der Gegenrede erreichbar", !!auf);
      await p.keyboard.press("Escape");
      const dlg = await p.evaluate(() => !document.querySelector("#verdacht-hof.an") && !!document.querySelector(".dialog.an .dialog-antwort"));
      ok("a gut: nach der Liste weiter im Gespräch (Escape schließt nur die Liste)", dlg);
    }
  },
  wahl: ["Zum Tresen.", "Was ist mit dem Herrn", "Wo ist der Arzt", "Was soll ich machen", "Danke. Ich geh zu ihm.",
    "KPJ-Studentin", "Haben Sie vorher", "Waren Sie grad", "Wie lange weg", "Woher ist die Schramme",
    "Das reicht mir fürs Erste.", "Welche Tabletten", "Haben Sie die heute", "Ist in letzter Zeit", "Haben Sie Zucker",
    "Herzrasen", "Das reicht mir.", "Ist das schon einmal", "Dem Arzt sag ich alles",
    "Gestern vorher", "Wie lange sind Sie", "Das entscheidet der Oberarzt. Vorher",
    "Darf ich Sie kurz anschauen", "Es war gestern", "Zehn Sekunden", "Ich geh ran", "Er liegt gerade", "Hat er gezuckt",
    "Hat er seine Tabletten", "Das entscheidet der Oberarzt gleich", "Darf ich kurz übergeben", "Herr Baum, 68. Zweimal",
    /^Sinus, /, "Betablocker seit Jahren", "Die Tochter hat's gesehen", "Ist in Ihrer Familie", "Bin gleich zurück.",
    "Er bleibt. Monitor.", "Keine Vorwarnung", "Zweimal in zwei Tagen", /^PQ \d/, "Ramipril und ASS", "Gestern und heute",
    "Das kann vom Herzen"],
  vorEkg: (f) => (!f.has("r2_fertig") || !f.has("r3_fertig") || !f.has("untersucht")) ? "herrk" : "wagen",
  extra: async (p, s, gemacht, schuss) => {
    const f = new Set(s.z.flags);
    if (f.has("r3_fertig") && !gemacht.has("verdacht")) {
      gemacht.add("verdacht");
      await p.click("#hud-verdacht"); await schuss("verdacht", 200);
      const n = await p.$$eval("#verdacht-hof .vd-eintrag", (l) => l.length);
      ok("a gut: Verdachtsliste mit acht Einträgen", n === 8, String(n));
      const strich = await p.$$eval("#verdacht-hof .vd-eintrag.z-unwahrscheinlich", (l) => l.map((e) => e.dataset.verdacht));
      ok("a gut: Sturz ohne Bewusstlosigkeit und Unterzucker gestrichen", strich.includes("sturz") && strich.includes("zucker"), strich.join(","));
      const zahl = await p.textContent("#hud-verdacht .hud-zahl");
      ok("a gut: Zähler am Knopf Verdacht nach dem Öffnen 0", zahl === "0", zahl);
      await p.click("#verdacht-hof .zu");
      return true;
    }
    if (s.z.karten.includes("pq") && !gemacht.has("mappe")) {
      gemacht.add("mappe");
      await p.click("#hud-mappe");
      await p.click('#mappe .karte[data-karte="pq"]'); await p.click('#mappe .karte[data-karte="medis"]');
      await p.click("#mappe .vergleich");
      const t = await p.textContent("#mappe .verg-frage");
      ok("a gut: Vergleich PQ ↔ Medikamente", t.startsWith("Der Betablocker bremst beide Etagen"), t.slice(0, 50));
      await schuss("mappe_vergleich", 200);
      await p.click('#mappe .karte[data-karte="pq"]'); await p.click('#mappe .karte[data-karte="medis"]');
      await p.click('#mappe .karte[data-karte="frequenz"]'); await p.click('#mappe .karte[data-karte="bogen"]');
      await p.click("#mappe .vergleich");
      const t2 = await p.textContent("#mappe .verg-frage");
      const hf = s.z.werte.hf;
      ok("a gut: Vergleich Frequenz ↔ Aufnahmebogen mit gemessener Zahl", t2 === `Puls 52 getastet, ${hf} gemessen: dieselbe Zahl.`, t2);
      await p.click("#mappe .zu");
      mappeGeprueft = true;
      return true;
    }
    return false;
  },
  pruefe: async (p, z, texte, name) => {
    await pruefeEnde(p, z, name, ["senta_geloest"]);
    ok(`${name}: Mappe und Vergleiche geprüft`, mappeGeprueft);
    const mess = await p.evaluate(() => window.__prototyp.satz().mess);
    ok(`${name}: Falk misst nach: „{mess_pq}. Passt.“ aus der Annotation`, replik(texte, "zirkel2")[0] === `${mess.pq}. Passt.`, replik(texte, "zirkel2")[0]);
    const aZeile = texte.find((t) => t.art === "option" && t.text.startsWith("Sinus, "));
    ok(`${name}: A-Zeile mit den Messwerten der Spielerin`, aZeile && aZeile.text === `Sinus, ${z.werte.hf}, PQ ${z.werte.pq}, QRS schmal. Nicht normal, kein Beweis.`, aZeile && aZeile.text);
    ok(`${name}: Falk sagt nach Stützargument, was fehlt (Vorwarnung gefallen)`, hatText(texte, "Fehlt mir, was das EKG dazu sagt."));
    ok(`${name}: Falk fragt die ausgelassene Familie ab`, replik(texte, "luecke").includes("Familie?"));
    ok(`${name}: Falk gibt nach`, replik(texte, "nachgeben").length === 1);
    ok(`${name}: Falk um 07:15 erst nach dem Knopf im Stand`, !z.flags.includes("falk_gewartet"));
    ok(`${name}: Epilog mit Senta, ohne „Kreislauf“-Zeile`, hatText(texte, "Die Senta hat die Frau Kainz") && !hatText(texte, "warum du am Montag"));
    ok(`${name}: Marlene weiß vom zweiten Ereignis (Wagen)`, replik(texte, "w3a").length === 1);
    const ek = texte.filter((t) => t.art === "meldung" && t.text.startsWith("EKG geschrieben")).length;
    ok(`${name}: Meldung „EKG geschrieben“`, ek === 1);
  }
});

/* ------------------------------------------------------------------ (b) Irrwege */
await lauf("b irrwege", { viewport: { width: 1366, height: 1024 } }, {
  kurz: "b", schuesse: { f_warten: "falk_wartet", t_zweit: "zweiter_anruf", a_rueck: "rueckweg_wagen", luecke: "luecke",
                         hinweis: "hinweis", tab_brady: "tabletten_brady", st1: "tochter_verraten", ab_falk: "abschied" },
  messen: ["rr"], rhythmus: ["Ersatzrhythmus aus dem AV-Knoten", "Vorhofflimmern", "Sinusrhythmus"],
  wahl: ["Zum Tresen.", "Ich geh zu ihm.", "Danke. Ich geh zu ihm.", "Ich schau zuerst auf den Bogen", "KPJ-Studentin",
    "Haben Sie vorher", "Waren Sie grad", "Das reicht mir fürs Erste.", "Welche Tabletten", "Haben Sie die heute",
    "Das reicht mir.", "Ist das schon einmal", "Was soll ich ihr nicht sagen", "Das bleibt unter uns",
    "Das entscheidet der Oberarzt. Vorher", "Es war gestern", "Haben Sie schon einmal ein EKG", "Zehn Sekunden",
    "Das kann warten", "Er liegt gerade", "Hat er gezuckt", "Hat er seine Tabletten", "Er hat uns gesagt",
    "Ja, wahrscheinlich.", "Herr Baum, 68, Synkope", "Ein älterer Herr", "Herr Baum, 68. Zweimal",
    "Bradykardie", "EKG unauffällig", "PQ hab ich nicht", /^Sinus, /, "Er geht täglich", "Betablocker seit Jahren", "Weiter",
    "Woher ist die Schramme", "Haben Sie Zucker", "Ist in Ihrer Familie", "Bin gleich zurück.",
    "Noch einen Stehversuch", "Er kann heim", "Stehversuch negativ.", "Das EKG ist fast", "Er fühlt sich gut",
    "Zweimal in zwei Tagen", "Er hat sich verletzt", "Puls ", "Der Vater", "Stehversuch negativ, beim", "Keine Vorwarnung",
    /^PQ \d/, "Alle drei", "Nichts, bis", "Ramipril und ASS",
    "Dann unterschreiben", "Das ist jetzt nicht", "Wegen der Senta", "Gestern und heute", "Ihr Herz schlägt", "Das kann vom Herzen"],
  vorEkg: (f, s) => (!f.has("r2_fertig") || !f.has("r3_fertig")) ? "herrk" : (s.z.falkDa ? "wagen" : "marlene"),
  pruefe: async (p, z, texte, name) => {
    await pruefeEnde(p, z, name, ["versprochen", "anruf_spaeter", "tochter_verraten", "heim_empfohlen", "brady_argument",
                                  "falk_gewartet", "revers", "senta_geloest"]);
    ok(`${name}: Falk wartet ohne EKG („Schreiben Sie, ich les solang.“)`, replik(texte, "f_warten").length === 1);
    ok(`${name}: Sabine ruft nach dem Streifen noch einmal („dreimal angerufen“)`, replik(texte, "t0b").some((t) => t.startsWith("Ich hab dreimal angerufen.")));
    ok(`${name}: versprochen bei Falk: „Steht nicht am Bogen …“`, replik(texte, "v3").length === 1);
    ok(`${name}: brady_argument bei den Tabletten`, replik(texte, "tab_brady").length === 1);
    ok(`${name}: Rückweg zum Wagen (PQ nicht gemessen)`, replik(texte, "a_rueck").length === 1 && z.karten.includes("pq"));
    const lu = replik(texte, "luecke");
    ok(`${name}: Falk fragt Verletzung, Zucker, Familie ab (je ein Rückweg)`, lu.length === 3 && lu[0].startsWith("Verletzt") && lu[1].startsWith("Zucker") && lu[2] === "Familie?", lu.join(" | "));
    ok(`${name}: Gegenrede umgekehrt (heim_empfohlen)`, replik(texte, "h_ende").length === 1);
    ok(`${name}: {fehlt} beide fehlen`, hatText(texte, "Fehlt mir trotzdem der Grund, warum er nicht niedrig ist."));
    ok(`${name}: Hinweis nach vier Argumenten`, replik(texte, "hinweis").length === 1);
    ok(`${name}: Falk am Bett ohne Untersuchung: „Dann jetzt.“`, replik(texte, "bett1b").length === 1 && z.flags.includes("untersucht"));
    ok(`${name}: Schluss mit tochter_verraten, ohne „Dem Arzt. Nicht der Sabine.“`, replik(texte, "st1").length === 1 && !replik(texte, "sv2").length);
    ok(`${name}: Marlene beim Abschied: Revers und Falk warten lassen`, replik(texte, "ab_rev").length === 1 && replik(texte, "ab_falk").length === 1);
    ok(`${name}: Rhythmusfrage: falsche Antworten mit Rückmeldung`, hatText(texte, "Langsam heißt nicht Ersatz.") && hatText(texte, "Kein P, flimmernde Grundlinie"));
    ok(`${name}: Marlene ruft beim Wagen zu früh nicht (Kern erst gefragt)`, true);
    ok(`${name}: Rückmeldung zu „Das reicht mir fürs Erste“`, hatText(texte, "Was du nicht gefragt hast, fragt Falk."));
  }
});

/* ------------------------------------------------------------------ (c) iPad 1024 × 768, reduced motion */
await lauf("c ipad ruhig", { viewport: { width: 1024, height: 768 }, reducedMotion: "reduce", hasTouch: false }, {
  kurz: "c", schuesse: { m0: "ipad_marlene", g0: "ipad_gegenrede", "zirkel-hof": "ipad_zirkel", "frage-hof": "ipad_rhythmus",
                         tab0: "ipad_tabletten", sv3: "ipad_versprochen" },
  messen: ["rr", "pq", "qrs"],
  wahl: ["Zum Tresen.", "Wo ist der Arzt", "Was soll ich machen", "Ich geh zu ihm.", "Danke. Ich geh zu ihm.", "KPJ-Studentin",
    "Haben Sie vorher", "Waren Sie grad", "Wie lange weg", "Woher ist die Schramme", "Hat Ihre Tochter",
    "Welche Tabletten", "Haben Sie die heute", "Darf ich Sie kurz anschauen", "Ist in letzter Zeit", "Haben Sie Zucker",
    "Herzrasen", "Konnten Sie danach", "Alkohol", "Ist in Ihrer Familie", "Ist das schon einmal", "Das bleibt unter uns",
    "Das reicht mir.", "Das entscheidet der Oberarzt. Vorher", "Noch nicht. Erst das EKG",
    "Zehn Sekunden", "Ich geh ran", "Hat er gezuckt", "Hat er seine Tabletten", "Er liegt gerade", "Wahrscheinlich nur",
    "Nein.", "Herr Baum, 68. Zweimal", /^Sinus, /, "Die Tochter hat's gesehen", "Betablocker seit Jahren", "Bin gleich zurück.",
    "Er bleibt. Monitor.", "Die Tochter hat kein Zucken", "Könnte es eine TIA", /^PQ \d/, "Er hat sich verletzt", "Keine Vorwarnung",
    "Ramipril und ASS", "Wegen der Senta", "Gestern und heute", "Das kann vom Herzen"],
  vorEkg: (f) => (!f.has("r2_fertig") || !f.has("r3_fertig")) ? "herrk" : "wagen",
  extra: async (p, s, gemacht) => {
    if (gemacht.has("menue")) return false;
    gemacht.add("menue");
    ok("c ipad ruhig: reduced-motion erkannt (Motor und leben.js)", await p.evaluate(() => window.__prototyp.ruhig() && window.Leben.ruhig()));
    await p.keyboard.press("Escape");
    await p.waitForSelector("#menue-hof.an");
    await p.click("#menue-bewegung");
    ok("c ipad ruhig: Menü-Schalter „Bewegung aus“", await p.evaluate(() => !window.__prototyp.bewegung()));
    await p.click("#menue-bewegung");
    await p.click("#menue-weiter");
    const stage = await p.evaluate(() => { const r = document.getElementById("flaeche").getBoundingClientRect(); return [r.width, r.height, r.top]; });
    ok("c ipad ruhig: Bühne 16:9 mittig (1024 × 576)", Math.round(stage[0]) === 1024 && Math.round(stage[1]) === 576 && Math.round(stage[2]) === 96, stage.map(Math.round).join("×"));
    return true;
  },
  pruefe: async (p, z, texte, name) => {
    await pruefeEnde(p, z, name, ["versprochen", "tochter_beruhigt", "senta_geloest"]);
    ok(`${name}: {fehlt} EKG gefallen, Vorwarnung fehlt`, hatText(texte, "Fehlt mir trotzdem der Grund, warum die Vorwarnung zählt."));
    ok(`${name}: Schluss mit versprochen: „Dem Arzt. Nicht der Sabine.“`, replik(texte, "sv2").length === 1);
    ok(`${name}: Epilog mit „Kreislauf“-Zeile (tochter_beruhigt)`, hatText(texte, "warum du am Montag „Kreislauf“ gesagt hast"));
    ok(`${name}: QRS gemessen`, z.karten.includes("qrs") && z.werte.qrs > 0, String(z.werte.qrs));
    ok(`${name}: Untersuchung mitten in Runde 2, Runde läuft weiter`, replik(texte, "u_1").length === 1 && z.flags.includes("r2_5"));
    ok(`${name}: Falk muss nichts nachfragen`, !replik(texte, "luecke").length);
  }
});

/* ------------------------------------------------------------------ (d) Zufallsläufe: kein Softlock */
for (const saat of [7, 1234, 98765]) {
  await lauf("d zufall " + saat, { viewport: { width: 1366, height: 1024 } }, { kurz: "d", zufall: saat, vorEkg: () => "herrk" });
}

await browser.close();
console.log(zeilen.join("\n"));
console.log(fehler.length ? `\n${fehler.length} FEHLER:\n - ` + fehler.join("\n - ") : "\nAlle Prüfungen bestanden.");
process.exit(fehler.length ? 1 : 0);
