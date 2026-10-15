/* Durchlauf durch Kapitel 1 (Fall aufnahme_baum, Fallmotor) und Kapitel 2 in echtem Chromium.
   jsdom reicht hier nicht: Canvas, Zeigerereignisse, Layout und Animation
   sind genau das, was schiefgeht.

   Aufruf: node tools/durchlauf.mjs [spiel.html] [bilderordner]
   Ohne Angaben: bau/nachtdienst.html und bau/durchlauf/ in diesem Repository. */
import { starteBrowser } from "./browser.mjs";
import fs from "fs";
import { fileURLToPath } from "url";

const BAU = fileURLToPath(new URL("../bau/", import.meta.url));
const DATEI = process.argv[2] || BAU + "nachtdienst.html";
const BILDER = process.argv[3] || BAU + "durchlauf";
fs.mkdirSync(BILDER, { recursive: true });

const fehler = [], warnungen = [];
let n = 0;
const schritte = [];

function ok(was, bedingung, zusatz = "") {
  schritte.push((bedingung ? "  ok  " : "FEHLER") + "  " + was + (zusatz ? "  — " + zusatz : ""));
  if (!bedingung) fehler.push(was + (zusatz ? ": " + zusatz : ""));
}

const browser = await starteBrowser();
const seite = await browser.newPage({ viewport: { width: 1340, height: 900 }, deviceScaleFactor: 1 });
/* Der Durchlauf prüft die deutschen Sätze — Sprache vor dem Laden festlegen. */
await seite.addInitScript(() => {
  try {
    window.__spracheBeimStart = !!window.localStorage.getItem("nachtdienst-sprache");
    window.__ursprung = window.origin;
    if (!window.__spracheBeimStart) {
      window.localStorage.setItem("nachtdienst-sprache", "de");
    }
    /* Still vermerken, was beim Dokumentstart im Speicher lag — damit ein verlorener Spielstand beim
       Neuladen (selten beobachtet) sich im Fehlertext selbst erklärt. */
    window.__speicherBeimStart = (window.localStorage.getItem("nachtdienst-1") || "").length;
  } catch (e) {}
});
seite.on("console", (m) => { if (m.type() === "error") fehler.push("Konsole: " + m.text().slice(0, 160)); });
seite.on("pageerror", (e) => fehler.push("Seitenfehler: " + String(e).slice(0, 200)));

/* Bricht ein Schritt ab (Zeitüberschreitung o. ä.), trotzdem alles Bisherige
   ausgeben und ein Bild vom Zustand machen — sonst sieht man nur den Stapel. */
let abgebrochen = false;
function abbruch(e) {
  if (abgebrochen) return;
  abgebrochen = true;
  console.log(schritte.join("\n"));
  if (fehler.length) console.log("\nBIS DAHIN GESAMMELT:\n - " + fehler.join("\n - "));
  console.log("\nABBRUCH: " + String((e && e.message) || e).split("\n")[0]);
  seite.screenshot({ path: `${BILDER}/abbruch.png` }).catch(() => {}).finally(() => process.exit(1));
}
process.on("uncaughtException", abbruch);
process.on("unhandledRejection", abbruch);

async function schuss(name) {
  n++;
  await seite.screenshot({ path: `${BILDER}/${String(n).padStart(2, "0")}_${name}.png` });
}
const warte = (ms) => seite.waitForTimeout(ms);

/* Nach jedem Laden steht der Titelbildschirm da: „Weiterspielen“, wenn es einen Spielstand gibt, sonst nur
   „Neues Spiel“. Fehlt der Spielstand unerwartet, startet so ein neues Spiel — die Prüfungen danach sagen es. */
async function vomTitel(p = seite) {
  await p.locator("#titel").waitFor({ state: "visible", timeout: 5000 });
  const weiter = p.locator("#titel-weiter");
  if (await weiter.count()) await weiter.click();
  else await p.locator("#titel-neu").click();
}
async function neuLaden() { await seite.reload(); await vomTitel(); }
/* Was außer der Bühne sichtbar im Dokument steht (Spielfenster wie Dialog und Meldungen ausgenommen):
   Kopfzeile, Fußzeile, Seitenleiste dürfen nicht dabei sein. */
const webseitenReste = () => seite.evaluate(() => {
  const sichtbar = (e) => { const r = e.getBoundingClientRect(); return getComputedStyle(e).display !== "none" && r.width > 0 && r.height > 0; };
  return [...document.querySelectorAll("header, footer, aside, nav, select, .kopf, .fuss, .rahmen")].filter(sichtbar)
    .concat([...document.body.children].filter((e) => e.tagName !== "SCRIPT" && e.id !== "flaeche" && sichtbar(e) &&
      !e.classList.contains("dialog") && !e.classList.contains("meldungen") && !e.classList.contains("szenenbild")))
    .map((e) => e.tagName + "#" + e.id + "." + e.className);
});

/* ---------------------------------------------------------- Hilfen */
async function dialogDurch(maxKlicks = 14, p = seite) {
  for (let i = 0; i < maxKlicks; i++) {
    if (!(await p.locator(".dialog.an").count())) return;
    await p.locator(".dialog-text").click();          // Tippen überspringen
    await p.waitForTimeout(140);
    /* War der Text schon fertig, hat dieser Klick bei einem Endknopf-Knoten bereits „weiter“ ausgelöst. */
    if (!(await p.locator(".dialog.an").count())) return;
    const w = p.locator(".dialog-antwort.weiter");
    if (await w.count()) { await w.first().click(); await p.waitForTimeout(280); continue; }
    const a = p.locator(".dialog-antwort");
    if ((await a.count()) === 1) { await a.first().click(); await p.waitForTimeout(280); continue; }
    return;                                               // echte Wahl: nicht raten
  }
}
async function dialogLesen(p = seite) {
  if (!(await p.locator(".dialog-antworten.an").count())) {   /* tippt noch */
    await p.locator(".dialog-text").click();
    await p.waitForTimeout(120);
  }
  return (await p.locator(".dialog-text").textContent()) || "";
}
/* Klickt einen Dialog bis zum Ende durch und sammelt Texte und Knöpfe. */
async function dialogDurchLesen(max = 16) {
  const texte = [];
  for (let i = 0; i < max; i++) {
    if (!(await seite.locator(".dialog.an").count())) break;
    texte.push(await dialogLesen());
    const w = seite.locator(".dialog-antwort.weiter");
    if (await w.count()) {
      texte.push("[" + ((await w.first().textContent()) || "").trim() + "]");
      await w.first().click(); await warte(300); continue;
    }
    const a = seite.locator(".dialog-antwort");
    if ((await a.count()) === 1) {
      texte.push("[" + ((await a.first().textContent()) || "").trim() + "]");
      await a.first().click(); await warte(300); continue;
    }
    break;
  }
  return texte.join(" | ");
}
/* Den Endknopf eines Knotens tippen (z. B. „Danke, Marlene.“) und dem nächsten Dialog Zeit geben, sich zu öffnen. */
async function endeKnopf(p = seite) {
  if (!(await p.locator(".dialog-antworten.an").count())) { await p.locator(".dialog-text").click(); await p.waitForTimeout(120); }
  await p.locator(".dialog-antwort.weiter").first().click(); await p.waitForTimeout(450);
}
/* Antwort im laufenden Dialog wählen (Text muss enthalten sein) */
async function antworte(teil, p = seite) {
  await p.locator(".dialog-text").click();
  await p.waitForTimeout(120);
  const knopf = p.locator(".dialog-antwort", { hasText: teil });
  if (!(await knopf.count())) return false;
  await knopf.first().click();
  await p.waitForTimeout(320);
  return true;
}
const antworten = () => seite.locator(".dialog-antwort").allTextContents();
const feld = (id) => seite.locator(`.feld[data-feld="${id}"]`);
const zustand = () => seite.evaluate(() => JSON.parse(JSON.stringify(window.Spiel.zustand)));
const speicher = () => seite.evaluate(() => window.localStorage.getItem("nachtdienst-1"));
const fallHat = (m) => seite.evaluate((x) => window.Fall.hat("aufnahme_baum", x), m);
const letzteMeldung = async () => ((await seite.locator(".meldung").last().textContent()) || "").trim();
const standOffen = async () => (await seite.locator("#stand-hof .offen li").allTextContents()).join(" | ");
async function standLesen() {
  await seite.locator("#hud-stand").click(); await warte(350);
  const aus = { hat: (await seite.locator("#stand-hof .hat li").allTextContents()).join(" | "),
                offen: await standOffen(),
                fuss: (await seite.locator("#stand-hof .stand-fuss").textContent()) || "",
                zeile: (await seite.locator("#stand-hof .stand-zeile").textContent()) || "" };
  return aus;
}
async function standZu() { await seite.locator("#stand-hof .zu").click(); await warte(250); }
/* Alle sichtbaren Knöpfe eines Fensters mindestens 44 × 44 px? */
async function fingergross(wurzel, p = seite) {
  return p.evaluate((sel) => {
    const zuKlein = [];
    document.querySelectorAll(sel + " button").forEach((b) => {
      const r = b.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;              /* versteckt */
      if (r.width < 44 || r.height < 44) zuKlein.push((b.textContent || "").trim().slice(0, 24) + " " +
                                                       Math.round(r.width) + "×" + Math.round(r.height));
    });
    return zuKlein;
  }, wurzel);
}
/* Nichts blinkt: keine CSS-Animation in den neuen Fenstern. */
async function ohneBlinken(wurzel, p = seite) {
  return p.evaluate((sel) => {
    const an = [];
    document.querySelectorAll(sel + ", " + sel + " *").forEach((el) => {
      const n = getComputedStyle(el).animationName;
      if (n && n !== "none") an.push(el.className + ":" + n);
    });
    return an;
  }, wurzel);
}
const rueckText = async (sel) => ((await seite.locator(sel + " .rueck").textContent()) || "").trim();
/* Zieht den Zirkel über eine echte Strecke aus der Annotation (echte Maus). */
async function messe(vonSek, bisSek, p = seite) {
  const geo = await p.evaluate(() => {
    const hof = document.getElementById("zirkel-hof");
    const lw = hof.querySelector("canvas");
    const r = lw.getBoundingClientRect();
    return { x: r.left, y: r.top, h: r.height, s: hof.__streifen.stand.von };
  });
  const xv = await p.evaluate((s) => document.getElementById("zirkel-hof").__streifen.sekundeZuX(s), vonSek);
  const xb = await p.evaluate((s) => document.getElementById("zirkel-hof").__streifen.sekundeZuX(s), bisSek);
  const y = geo.y + geo.h / 2;
  await p.mouse.move(geo.x + xv, y);
  await p.mouse.down();
  await p.mouse.move(geo.x + (xv + xb) / 2, y, { steps: 4 });
  await p.mouse.move(geo.x + xb, y, { steps: 4 });
  await p.mouse.up();
  await p.waitForTimeout(350);
}

await seite.goto("file://" + DATEI);
await warte(700);

/* ---------------------------------------------------------- 0 Titelbildschirm */
ok("Titelbildschirm erscheint beim Start", await seite.locator("#titel").isVisible());
ok("Titel: Spieltitel vom Code gesetzt", ((await seite.locator("#titel .titel-name").textContent()) || "").trim() === "Nachtdienst");
ok("Titel: Hintergrund ist die Aufnahme (drei Ebenen als Bilder, unscharf)",
   (await seite.locator("#titel .titel-ebenen img").count()) === 3 &&
   /blur/.test(await seite.evaluate(() => getComputedStyle(document.querySelector("#titel .titel-ebenen")).filter)));
ok("Titel: Kurve aus der echten Aufnahme (Herr Baum, data/)", await seite.evaluate(() => {
  const l = document.querySelector("#titel .titel-kurve polyline");
  return !!l && l.getAttribute("points").split(" ").length > 500;
}));
ok("Titel: ohne Spielstand kein „Weiterspielen“", (await seite.locator("#titel-weiter").count()) === 0);
ok("Titel: Neues Spiel, Sprache, Info & Quellen",
   await seite.locator("#titel-neu").isVisible() && await seite.locator("#titel-sprache").isVisible() &&
   await seite.locator("#titel-info").isVisible());
let zuKleinT = await fingergross("#titel");
ok("Titel: Knöpfe fingergroß", !zuKleinT.length, zuKleinT.join(", "));
ok("Titel: das Spiel läuft noch nicht (kein Dialog, keine Szene)",
   (await seite.locator(".dialog.an").count()) === 0 && await seite.evaluate(() => !window.Szene.aktueller()));
await seite.screenshot({ path: `${BILDER}/00_titel.png` });
await seite.locator("#titel-sprache").click();
await warte(200);
ok("Titel: Sprache bietet Deutsch, English, Русский",
   (await seite.locator("#sprache-hof.an .knopf.sprache").allTextContents()).join("|") === "Deutsch|English|Русский");
await seite.keyboard.press("Escape");
await warte(200);
ok("Titel: Escape schließt die Sprachwahl, der Titel bleibt",
   (await seite.locator("#sprache-hof.an").count()) === 0 && await seite.locator("#titel").isVisible());
await seite.locator("#titel-info").click();
await warte(200);
ok("Titel: Info & Quellen erreichbar", await seite.locator("#info-hof.an").isVisible());
await seite.locator("#info-hof .zu").click();
await warte(200);
await seite.locator("#titel-neu").click();
await warte(900);
ok("„Neues Spiel“ startet: Titel weg, Szene steht",
   !(await seite.locator("#titel").isVisible()) && await seite.evaluate(() => window.Szene.aktueller() === "aufnahme"));
ok("Beim ersten Tippen Vollbild angefordert (wo es das gibt)",
   await seite.evaluate(() => !!(document.fullscreenElement || document.webkitFullscreenElement)));

/* ---------------------------------------------------------- 0a Texte über IDs: jede ID in allen Sprachen, ohne Gedankenstrich, in Bildschirmmaß */
const texte = await seite.evaluate(() => {
  const T = window.TEXTE, de = Object.keys(T.de || {});
  const fehltEn = de.filter((k) => !T.en[k]), fehltRu = de.filter((k) => !T.ru[k]);
  const platzhalter = (s) => (s.match(/\{\w+\}/g) || []).sort().join(",");
  const falsch = de.filter((k) => (T.en[k] && platzhalter(T.en[k]) !== platzhalter(T.de[k])) || (T.ru[k] && platzhalter(T.ru[k]) !== platzhalter(T.de[k])));
  const striche = de.filter((k) => /—/.test(T.de[k]) || /—/.test(T.en[k] || "") || /—/.test(T.ru[k] || ""));
  const repliken = de.filter((k) => /^baum\.(marlene|herrk|falk|auftakt|epilog)\./.test(k) && !/\.(a|f)\./.test(k));
  const lang = repliken.filter((k) => T.de[k].length > 230).map((k) => k + ":" + T.de[k].length);
  const optionen = de.filter((k) => /^baum\.(marlene|herrk|falk)\.(a|f)\./.test(k));
  const langeOptionen = optionen.filter((k) => T.de[k].length > 64).map((k) => k + ":" + T.de[k].length);
  const lektion = de.filter((k) => /Lektion|ESC-|Tabelle \d|§/.test(T.de[k]));
  return { n: de.length, fehltEn, fehltRu, falsch, striche, lang, langeOptionen, lektion, nRepliken: repliken.length };
});
ok("Texte über IDs: Englisch und Russisch vollständig (" + texte.n + " IDs)", !texte.fehltEn.length && !texte.fehltRu.length,
   texte.fehltEn.concat(texte.fehltRu).slice(0, 5).join(", "));
ok("Texte über IDs: dieselben Platzhalter in allen Sprachen", !texte.falsch.length, texte.falsch.slice(0, 5).join(", "));
ok("Humanizer: kein Gedankenstrich in den Texten des Falls (de/en/ru)", !texte.striche.length, texte.striche.slice(0, 5).join(", "));
ok("Bildschirmmaß: jede Replik des Falls höchstens 230 Zeichen (" + texte.nRepliken + " Repliken)", !texte.lang.length, texte.lang.join(", "));
ok("Bildschirmmaß: jede Spielerantwort höchstens eine Zeile (64 Zeichen)", !texte.langeOptionen.length, texte.langeOptionen.join(", "));
ok("Keine Lektionsnummern und keine Quellenangaben im Spieltext", !texte.lektion.length, texte.lektion.join(", "));
ok("Keine Tüten-Station mehr: kein Klickfeld, kein Export, kein Tüten-Verweis in Spieltexten",
   (await feld("tuete").count()) === 0 && await seite.evaluate(() => !window.Spiel.__tuete &&
     !Object.values(window.TEXTE.de).some((t) => /Tüte/.test(t) && !/Tüte in der einen Hand|Plastiktüte|Tüte darunter/.test(t))));

/* ---------------------------------------------------------- 1 Auftakt */
ok("Seite lebt", await seite.locator("#buehne").isVisible());
/* Gerenderte Räume haben keinen Vordergrund (nichts steht vor der Kamera); Hintergrund, Mittelgrund und
   Figuren müssen gezeichnet sein. */
for (const n of ["hintergrund", "mittelgrund", "figuren"])
  ok("Ebene " + n + " gezeichnet", (await seite.locator("#buehne .ebene-" + n + " svg").count()) === 1);
ok("Uhrzeiger in der Hintergrund-Ebene", (await seite.locator("#buehne .ebene-hintergrund svg #uhr-std").count()) === 1);
ok("Hotspots vorhanden (Marlene, Herr Baum, Wagen, Uhr, Pinnwand, Flur)", (await seite.locator(".feld").count()) === 6);
ok("Auftakt-Dialog erscheint", await seite.locator(".dialog.an").isVisible());
/* Die Erzählstimme hat kein Porträt und keinen Namen — sie beschreibt Marlene, statt Marlene zu sein. */
ok("Auftakt: Erzähler ohne Porträt und ohne Namensschild", await seite.evaluate(() => {
  const d = document.querySelector(".dialog.an");
  return d.classList.contains("ohne-bild") && !d.querySelector(".dialog-bild svg") &&
         !d.querySelector(".dialog-name").textContent.trim();
}));
ok("Auftakt: 06:40, Marlene hinter dem Tresen, Herr Baum mit Tüte", /06:40/.test(await dialogLesen()) && /Marlene/.test(await dialogLesen()));
/* Bildschirme: auf dem EKG-Wagen läuft Herrn Baums Aufnahme aus data/ (Leinwand in der Mittelgrund-Ebene),
   Marlenes Verwaltungs-PC zeigt keine Kurve — in der Aufnahme gibt es genau diese eine Leinwand. */
const schirme1 = await seite.evaluate(() => window.Spiel.__schirme());
ok("EKG-Wagen: laufende Kurve aus data/", schirme1.length === 1 && schirme1[0].name === "wagen_schirm" &&
   schirme1[0].satz === 39 && schirme1[0].laeuft, JSON.stringify(schirme1));
ok("EKG-Wagen: Leinwand in der Mittelgrund-Ebene",
   (await seite.locator("#buehne .ebene-mittelgrund .schirm-lauf[data-schirm=wagen_schirm] canvas").count()) === 1);
ok("Marlenes PC zeigt kein EKG", (await seite.locator("#buehne .schirm-lauf").count()) === 1);
await schuss("auftakt");
let reste = await webseitenReste();
ok("Keine Kopf-, Fuß- oder Seitenleiste neben der Bühne", !reste.length, reste.join(", "));
await seite.keyboard.press("Escape");
await warte(200);
ok("Escape bei offenem Dialog: kein Menü, der Dialog bleibt",
   (await seite.locator("#menue-hof.an").count()) === 0 && (await seite.locator(".dialog.an").count()) === 1);
await dialogDurch();
ok("Auftakt beendet", (await seite.locator(".dialog.an").count()) === 0);
ok("Nach dem Auftakt leuchten die Klickfelder einmal von selbst auf",
   await seite.evaluate(() => document.querySelector(".felder").classList.contains("zeigen")));

/* -------------------------------------------- 1a HUD und Pausenmenü */
const hud = await seite.evaluate(() => {
  const b = document.getElementById("buehne").getBoundingClientRect();
  return [...document.querySelectorAll("#hud button")].map((k) => {
    const r = k.getBoundingClientRect();
    return { id: k.id, b: Math.round(r.width), h: Math.round(r.height),
             drin: r.left >= b.left && r.right <= b.right && r.top >= b.top && r.bottom <= b.bottom };
  });
});
ok("HUD: Hinweis, Stand, Befundmappe und Menü als Knöpfe",
   ["hud-hinweis", "hud-stand", "hud-mappe", "hud-menue"].every((id) => hud.some((k) => k.id === id)), hud.map((k) => k.id).join(","));
ok("HUD: alle Knöpfe mindestens 44 × 44 px", hud.every((k) => k.b >= 44 && k.h >= 44), hud.map((k) => k.id + " " + k.b + "×" + k.h).join(", "));
ok("HUD: liegt über der Bühne", hud.every((k) => k.drin));
ok("HUD: Symbole zeichnet der Code (SVG, kein Bild)",
   (await seite.locator("#hud button svg path").count()) >= 4 && (await seite.locator("#hud img").count()) === 0);
ok("HUD: jeder Knopf hat Text oder Tooltip", await seite.evaluate(() =>
  [...document.querySelectorAll("#hud button")].every((k) => k.title && k.getAttribute("aria-label"))));
ok("HUD: Uhr zeigt die Spielzeit, dazu der Raum",
   ((await seite.locator("#hud-zeit").textContent()) || "") === "06:40" && ((await seite.locator("#hud-ort").textContent()) || "") === "Aufnahme");
ok("HUD: Mappe zählt", ((await seite.locator("#hud-mappe .hud-zahl").textContent()) || "") === "0");
const ebenenLage = () => seite.evaluate(() => document.querySelector("#buehne .ebene-figuren").style.transform);
const ebenenLage1 = await ebenenLage();
await warte(400);
ok("Parallaxe läuft in der Vollbild-Bühne weiter", !!ebenenLage1 && ebenenLage1 !== (await ebenenLage()), ebenenLage1);
let blinktHud = await ohneBlinken("#hud");
ok("HUD: nichts blinkt", !blinktHud.length, blinktHud.join(", "));
await warte(2600);                                      /* Klickfelder wieder ruhig */
await schuss("hud");
await seite.locator("#hud-menue").click();
await warte(250);
ok("≡ öffnet das Menü", await seite.locator("#menue-hof.an").isVisible());
const menueText = (await seite.locator("#menue-hof").textContent()) || "";
ok("Menü: Fortsetzen · Neues Spiel · Sprache · Vollbild · Info & Quellen",
   ["Fortsetzen", "Neues Spiel", "Sprache", "Deutsch", "English", "Русский", "Vollbild", "Info & Quellen"].every((t) => menueText.includes(t)),
   menueText.slice(0, 160));
ok("Menü: Vollbild steht auf „an“", await seite.evaluate(() =>
  document.querySelector("#menue-vollbild").getAttribute("aria-pressed") === "true"));
let zuKleinM = await fingergross("#menue-hof");
ok("Menü: Knöpfe fingergroß", !zuKleinM.length, zuKleinM.join(", "));
let blinktM = await ohneBlinken("#menue-hof");
ok("Menü: nichts blinkt", !blinktM.length, blinktM.join(", "));
await schuss("menue");
await seite.keyboard.press("s");
await warte(200);
ok("Solange das Menü offen ist, erreichen Tasten das Spiel nicht (S öffnet keinen Stand)",
   (await seite.locator("#stand-hof.an").count()) === 0);
await seite.locator("#menue-neu").click();
await warte(200);
ok("Neues Spiel fragt erst nach", await seite.locator("#frage-neu-hof.an").isVisible() &&
   /von vorn/.test((await seite.locator("#frage-neu-hof").textContent()) || ""));
await seite.locator("#frage-nein").click();
await warte(200);
ok("Abbrechen: Rückfrage zu, Menü offen, Spielstand bleibt",
   (await seite.locator("#frage-neu-hof.an").count()) === 0 && await seite.locator("#menue-hof.an").isVisible() &&
   await seite.evaluate(() => !!window.localStorage.getItem("nachtdienst-1")));
await seite.locator("#menue-info").click();
await warte(250);
ok("Info & Quellen öffnet aus dem Menü", await seite.locator("#info-hof.an").isVisible());
const quellen = await seite.locator("#info-hof .info-quelle").allTextContents();
ok("Info: drei Datenquellen, jede mit Lizenz",
   quellen.length === 3 && /LUDB/.test(quellen[0]) && /ODC-By 1\.0/.test(quellen[0]) &&
   /PTB-XL/.test(quellen[1]) && /CC BY 4\.0/.test(quellen[1]) &&
   /Chapman-Shaoxing/.test(quellen[2]) && /Ningbo/.test(quellen[2]) && /CC BY 4\.0/.test(quellen[2]), quellen.join(" | ").slice(0, 200));
ok("Info: Namensnennung je Quelle (Autoren, PhysioNet)",
   /Kalyakulina/.test(quellen[0]) && /Wagner/.test(quellen[1]) && /Zheng/.test(quellen[2]) && quellen.every((q) => /PhysioNet/.test(q)));
const infoText = (await seite.locator("#info-hof").textContent()) || "";
ok("Info: Lernspiel, kein Medizinprodukt", /Lernspiel zum EKG/.test(infoText) && /Kein Medizinprodukt/.test(infoText));
let zuKleinI = await fingergross("#info-hof");
ok("Info: Knöpfe fingergroß", !zuKleinI.length, zuKleinI.join(", "));
await schuss("info");
await seite.keyboard.press("Escape");
await warte(200);
ok("Escape schließt Info & Quellen, das Menü bleibt",
   (await seite.locator("#info-hof.an").count()) === 0 && await seite.locator("#menue-hof.an").isVisible());
await seite.keyboard.press("Escape");
await warte(200);
ok("Escape schließt das Menü", (await seite.locator("#menue-hof.an").count()) === 0);
await seite.keyboard.press("Escape");
await warte(200);
ok("Escape öffnet das Menü, wenn nichts anderes offen ist", await seite.locator("#menue-hof.an").isVisible());
await seite.locator("#menue-weiter").click();
await warte(200);
ok("„Fortsetzen“ schließt das Menü, die Bühne ist wieder bedienbar",
   (await seite.locator("#menue-hof.an").count()) === 0 && await seite.evaluate(() => !document.getElementById("flaeche").hasAttribute("inert")));

/* -------------------------------------------- 1b Stand ganz am Anfang */
let st = await standLesen();
ok("Stand öffnet sich", await seite.locator("#stand-hof.an").isVisible());
ok("Stand nennt am Anfang offene Punkte (Marlene zuerst, EKG)", /Marlene/.test(st.offen) && /EKG/.test(st.offen), st.offen.slice(0, 120));
ok("Stand verrät die Lösung nicht", !st.offen.match(/228|Block|Bisoprolol|AV-/), st.offen.slice(0, 120));
ok("Stand: Kapitel 1 · Aufnahme", /Kapitel 1/.test(st.zeile) && /Aufnahme/.test(st.zeile), st.zeile);
await schuss("stand_anfang");
await standZu();
const standLeer = await speicher();

/* ---------------------------------------------------------- 1c Klinische Reihenfolge: kein EKG vor der Anamnese */
await feld("wagen").click();
await warte(400);
ok("Wagen vor der Anamnese: kein EKG, Meldung nennt die Reihenfolge (Anamnese, Untersuchung, dann EKG)",
   (await seite.locator("#frage-hof.an").count()) === 0 && /Anamnese/.test(await letzteMeldung()) && /Untersuchung/.test(await letzteMeldung()),
   await letzteMeldung());

/* ---------------------------------------------------------- 2 Marlene im Szenenbild */
await feld("marlene").click();
await warte(900);
ok("Erstes Gespräch mit Marlene: Szenenbild erscheint bildschirmfüllend", await seite.evaluate(() => {
  const s = document.querySelector(".szenenbild.an"), b = document.getElementById("buehne").getBoundingClientRect();
  if (!s) return false;
  const r = s.getBoundingClientRect();
  return window.Szenenbild.offen() && Math.abs(r.width - b.width) <= 1 && Math.abs(r.height - b.height) <= 1 &&
         parseFloat(getComputedStyle(s).opacity) > 0.9;
}));
ok("Szenenbild: Bild aus kunst.json (JPEG, komprimiert, unter 300 kB)", await seite.evaluate(() => {
  const src = (document.querySelector(".szenenbild img") || {}).src || "";
  return /^data:image\/jpeg;base64,/.test(src) && src.length * 3 / 4 < 300 * 1024;
}));
ok("Szenenbild: ruhige Einblendung (Übergang, keine Animation)", await seite.evaluate(() => {
  const s = getComputedStyle(document.querySelector(".szenenbild"));
  return /opacity/.test(s.transitionProperty) && parseFloat(s.transitionDuration) >= 0.5 && s.animationName === "none";
}));
ok("Marlene spricht über dem Szenenbild, das Bild bleibt sichtbar", await seite.locator(".dialog.an").isVisible() &&
   await seite.evaluate(() => +getComputedStyle(document.querySelector(".dialog.an")).zIndex > +getComputedStyle(document.querySelector(".szenenbild")).zIndex));
const gruss = await dialogLesen();
ok("Erstbegrüßung, nicht die Wiederholung", gruss.includes("Famulantin") && /ohne Vorwarnung/.test(gruss), gruss.slice(0, 60));
ok("Porträt im Dialog", (await seite.locator(".dialog-bild svg").count()) === 1);
await schuss("szenenbild_marlene");
ok("Frage nach den Vitalzeichen", await antworte("Was hast du bisher"));
const werte = await dialogLesen();
const FALLWERTE = await seite.evaluate(() => window.FAELLE.aufnahme_baum.werte);
ok("Marlene nennt Puls, Blutdruck liegend und nach drei Minuten Stehen, Zucker — aus den Werten des Falls, nicht aus Literalen",
   werte.includes("Puls " + FALLWERTE.puls) && werte.includes(FALLWERTE.rr_l_sys + " zu " + FALLWERTE.rr_l_dia) &&
   werte.includes(FALLWERTE.rr_s3_sys + " zu " + FALLWERTE.rr_s3_dia) && werte.includes("Zucker " + FALLWERTE.zucker), werte.slice(0, 120));
ok("Frage, was zu fragen ist", await antworte("Was soll ich ihn fragen"));
ok("Marlene sagt nichts vor (D3: kein Erklärdump)", /nichts vor/.test(await dialogLesen()));
ok("Zum Patienten", await antworte("Dann frag ich ihn"));
ok("Marlene reicht den Aufnahmebogen — Bild und Logik stimmen überein", /Aufnahmebogen/.test(await dialogLesen()) &&
   await seite.evaluate(() => window.Mappe.hat("b-bogen")) && await seite.evaluate(() => window.Szenenbild.aktuelles() === "aufnahme_tresen"));
await dialogDurch();
await warte(900);
ok("Nach dem Gesprächsabschnitt blendet das Szenenbild aus, der Raum ist wieder da",
   !(await seite.evaluate(() => window.Szenenbild.offen())) && (await seite.locator(".szenenbild.an").count()) === 0 &&
   await seite.evaluate(() => document.querySelector(".felder").classList.contains("zeigen")));
const karteBogen = await seite.evaluate(() => { const b = window.Spiel.zustand.befunde.find((x) => x.id === "b-bogen"); return b ? window.T(b.text, b.vars) : ""; });
ok("Aufnahmebogen-Karte: Vitalzeichen, Stehversuch, Blutzucker, Schürfung, Vorerkrankungen",
   karteBogen.includes(FALLWERTE.rr_l_sys + "/" + FALLWERTE.rr_l_dia) && karteBogen.includes(FALLWERTE.rr_s3_sys + "/" + FALLWERTE.rr_s3_dia) &&
   karteBogen.includes("Blutzucker " + FALLWERTE.zucker) && /Schürfung/.test(karteBogen) && /Bluthochdruck/.test(karteBogen), karteBogen.slice(0, 120));
await warte(2600);
await schuss("raum_nach_szenenbild");
await feld("marlene").click();
await warte(450);
ok("Zweites Gespräch: kein Szenenbild mehr, Marlene im Raum", !(await seite.evaluate(() => window.Szenenbild.offen())) && /schlauer/.test(await dialogLesen()));
ok("Vor der Anamnese keine Expertenfragen (sie brauchen den Fall erst)", !(await antworten()).join(" ").includes("Fragen"));
await antworte("Später");
const standBogen = await speicher();

/* ---------------------------------------------------------- 3 Anamnese bei Herrn Baum */
st = await standLesen();
ok("Stand nach dem Bogen: Aufnahmebogen gezählt, Herr Baum noch nicht befragt",
   /Aufnahmebogen/.test(st.hat) && /Herrn Baum selbst/.test(st.offen), st.offen.slice(0, 120));
await standZu();
await feld("herrk").click();
await warte(450);
const kGruss = await dialogLesen();
ok("Herr Baum entschuldigt sich (Laiensprache, Tochter)", /Entschuldigen Sie/.test(kGruss) && /Tochter/.test(kGruss), kGruss.slice(0, 60));
let opt = await antworten();
ok("Anamnese-Menü: Ereignis, Medikamente, Vorerkrankungen, Untersuchen", /was passiert ist/.test(opt.join(" ")) && /Medikamente/.test(opt.join(" ")) &&
   /Krankheiten/.test(opt.join(" ")) && /untersuchen/.test(opt.join(" ")), opt.join(" / "));
ok("Frage nach dem Ereignis", await antworte("was passiert ist"));
const ereignis = await dialogLesen();
ok("Herr Baum: Haltestelle, kein Schwindel, kein Herzklopfen, „Licht ausgemacht“ (T-LOC ohne Prodrom, Laiensprache)",
   /Haltestelle/.test(ereignis) && /kein Schwindel/.test(ereignis) && /Licht/.test(ereignis) && !/Synkope|Prodrom/.test(ereignis), ereignis.slice(0, 80));
await schuss("anamnese");
opt = await antworten();
ok("Nach dem Ereignis die Fragen zum Moment: Vorwarnung, Situation, Dauer, Erholung",
   /gespürt/.test(opt.join(" ")) && /gerade gemacht/.test(opt.join(" ")) && /Wie lange/.test(opt.join(" ")) && /danach/.test(opt.join(" ")), opt.join(" / "));
ok("Prodrom", await antworte("vorher etwas gespürt"));
ok("Antwort Prodrom: nichts gespürt, Blässe erst nachher", /Nix/.test(await dialogLesen()) && /nachher/.test(await dialogLesen()));
ok("Gestellte Frage verschwindet aus der Liste", !(await antworten()).join(" ").includes("gespürt"));
ok("Situation", await antworte("gerade gemacht"));
ok("Antwort Situation: Stehen, Bus, Wasserkocher", /Gestanden/.test(await dialogLesen()) && /Wasserkocher/.test(await dialogLesen()));
ok("Dauer", await antworte("Wie lange"));
ok("Antwort Dauer: halbe Minute", /halbe Minute/.test(await dialogLesen()));
ok("Erholung", await antworte("danach"));
ok("Antwort Erholung: sofort wieder gut, frühstücken", /Sofort/.test(await dialogLesen()) && /frühstücken/.test(await dialogLesen()));
ok("Weitere Fragen zum Moment", await antworte("Andere Fragen"));
opt = await antworten();
ok("Zeugin, Verletzung, Zungenbiss, Herzrasen, Brustschmerz, Neurologie als Fragen",
   /gezuckt/.test(opt.join(" ")) && /Schramme/.test(opt.join(" ")) && /Zunge/.test(opt.join(" ")) && /Herzrasen/.test(opt.join(" ")) &&
   /Brust/.test(opt.join(" ")) && /Arme heben/.test(opt.join(" ")), opt.join(" / "));
ok("Zeugin", await antworte("gezuckt"));
ok("Antwort Zeugin: umgesunken, kein Zucken gesagt, zweites Mal allein", /umgesunken/.test(await dialogLesen()) && /allein/.test(await dialogLesen()));
ok("Verletzung", await antworte("Schramme"));
ok("Antwort Verletzung: Regal, Erinnerungslücke", /Regal/.test(await dialogLesen()) && /nicht mehr genau/.test(await dialogLesen()));
ok("Neurologie (optional)", await antworte("Arme heben"));
ok("Antwort Neurologie: Name gewusst, alles gesehen", /Namen|heiß/.test(await dialogLesen()) && /Gesehen/.test(await dialogLesen()));
await antworte("Zurück");
ok("„Zurück“ führt zum Anamnese-Menü, „Ich komme gleich wieder“ schließt", /Frau Doktor/.test(await dialogLesen()) && await antworte("gleich wieder") &&
   (await seite.locator(".dialog.an").count()) === 0);
st = await standLesen();
ok("Stand mahnt die fehlenden Pflichtfragen an: Medikamente, Vorerkrankungen, Familie",
   /fehlt noch/.test(st.offen) && /Medikamente/.test(st.offen) && /Vorerkrankungen/.test(st.offen) && /Familie/.test(st.offen) &&
   !/Vorwarnung|Dauer|Zeugin/.test(st.offen), st.offen.slice(0, 200));
ok("Stand: Herrn Baums Schilderung gezählt", /Schilderung/.test(st.hat));
await schuss("stand_pflicht");
await standZu();
await feld("herrk").click();
await warte(450);
ok("Wiederholte Begrüßung kurz", /Frau Doktor/.test(await dialogLesen()));
ok("Foto-Frage ohne Tüten-Bedingung", await antworte("Foto"));
ok("Lena und das Bändchen (Mensch, nicht Fall)", /Lena/.test(await dialogLesen()) && /Bändchen/.test(await dialogLesen()));
await antworte("Schön");
ok("Medikamente als Anamnesefrage", await antworte("Medikamente"));
const medis = await dialogLesen();
ok("Herr Baum reicht den Medikationsplan in Laiensprache (Zettel vom Hausarzt, Farben statt Namen)",
   /Zettel vom Hausarzt/.test(medis) && /Farben/.test(medis) && !/Bisoprolol|Tüte/.test(medis), medis.slice(0, 100));
const karteMedis = await seite.evaluate(() => { const b = window.Spiel.zustand.befunde.find((x) => x.id === "b-medis"); return b ? { titel: window.T(b.titel, b.vars), text: window.T(b.text, b.vars) } : null; });
ok("Medikationsplan erscheint in der Mappe (Karte entsteht im Gespräch, nicht in der Tüte)",
   !!karteMedis && /Medikationsplan/.test(karteMedis.titel) && /Bisoprolol 5 mg/.test(karteMedis.text) && /Betablocker/.test(karteMedis.text) &&
   /nicht verdächtig/.test(karteMedis.text) && !/Tüte/.test(karteMedis.text), JSON.stringify(karteMedis).slice(0, 120));
ok("Folgefrage nach Änderung", await antworte("neu dazugekommen"));
ok("Antwort: nichts geändert (Orthostase durch neue Medikation unwahrscheinlich)", /Nein/.test(await dialogLesen()) && /bleibt's/.test(await dialogLesen()));
ok("Diabetes", await antworte("Zucker"));
ok("Antwort: kein Zucker, Schwester hat gestochen", /keinen/.test(await dialogLesen()) && /gestochen/.test(await dialogLesen()));
await antworte("Zurück");
ok("Vorerkrankungen", await antworte("Krankheiten"));
ok("Antwort: Blutdruck, Knie, Hörgerät", /Blutdruck/.test(await dialogLesen()) && /Knie/.test(await dialogLesen()));
ok("Früher schon einmal?", await antworte("früher"));
ok("Antwort: nie", /Nie/.test(await dialogLesen()));
ok("Familie", await antworte("Familie"));
ok("Antwort Familie: Vater Schlaganfall mit achtzig, niemand jung", /Schlaganfall/.test(await dialogLesen()) && /Jung, nein/.test(await dialogLesen()));
ok("Alle Pflichtfragen gestellt: Anamnese-Karte entsteht von selbst",
   (await seite.evaluate(() => window.Fall.fehlendePflicht("aufnahme_baum"))).length === 0 && await seite.evaluate(() => window.Mappe.hat("b-anamnese")));
await antworte("Zurück");
ok("Kurzuntersuchung als Menüpunkt", await antworte("untersuchen"));
ok("Herr Baum: Jacke ausziehen?", /Jacke/.test(await dialogLesen()));
await dialogDurch();
await warte(300);
ok("Befundzeilen-Fenster: vier Zeilen, kein Rätsel, „In die Mappe“", (await seite.locator("#befund-hof.an").count()) === 1 &&
   (await seite.locator("#befund-hof .befund-zeilen li").count()) === 4 && (await seite.locator("#befund-hof .frage-wahl").count()) === 0);
const zeilen = (await seite.locator("#befund-hof .befund-zeilen li").allTextContents()).join(" ");
ok("Befundzeilen: Herztöne, Lunge, Sprache/Gesicht/Kraft, Doppeltsehen/Finger-Nase (orientierende Neurologie gegen TIA)",
   /Herztöne/.test(zeilen) && /Lunge/.test(zeilen) && /symmetrisch/.test(zeilen) && /Finger-Nase/.test(zeilen), zeilen.slice(0, 120));
let zuKleinB = await fingergross("#befund-hof");
ok("Befundzeilen: Knöpfe fingergroß", !zuKleinB.length, zuKleinB.join(", "));
await schuss("untersuchung");
await seite.keyboard.press("Enter");
await warte(400);
ok("Untersuchung als Karte in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-untersuchung")));
st = await standLesen();
ok("Stand: keine Pflichtfrage mehr offen, keine Untersuchung mehr offen, EKG steht an",
   !/fehlt noch|Untersucht hast/.test(st.offen) && /EKG/.test(st.offen), st.offen.slice(0, 160));
await standZu();
const standAnamnese = await speicher();

/* ---------------------------------------------------------- 4 Expertenfragen an Marlene */
await feld("marlene").click();
await warte(450);
ok("Nach der Anamnese bietet Marlene die Fragen an", await antworte("Fragen"));
opt = await antworten();
ok("Expertenfragen: Vorwarnung, TIA, Krampf, Unterzucker, Orthostase", /Vorwarnung/.test(opt.join(" ")) && /TIA/.test(opt.join(" ")) &&
   /gekrampft/.test(opt.join(" ")) && /Unterzucker/.test(opt.join(" ")) && /Stehen/.test(opt.join(" ")), opt.join(" / "));
ok("„Ist das nicht eine TIA?“", await antworte("TIA"));
const tia = await dialogLesen();
ok("TIA-Antwort: fokaler Ausfall fehlt, Bewusstsein war weg (ESC: TIA ohne LOC, Synkope das Gegenteil) — in Marlenes Stimme",
   /ausgefallen/.test(tia) && /Namen/.test(tia) && /Weg war er/.test(tia) && !/Leitlinie|ESC|Tabelle/.test(tia), tia.slice(0, 120));
await schuss("tia");
ok("Nachfrage Hirnstamm", await antworte("Hirnstamm"));
ok("Hirnstamm-TIA nie ohne Herdzeichen: doppelt sehen, schwanken; „schau selber nach“", /doppelt/.test(await dialogLesen()) && /selber nach/.test(await dialogLesen()));
ok("„Hat er gekrampft?“", await antworte("gekrampft"));
ok("Krampf-Antwort: kein Zucken, Zunge heil, gleich klar", /Zucken/.test(await dialogLesen()) && /Zunge/.test(await dialogLesen()) && /klar/.test(await dialogLesen()));
ok("„Unterzucker?“", await antworte("Unterzucker"));
ok("Zucker-Antwort nennt den Stix-Wert aus den Falldaten und: kein Diabetes", (await dialogLesen()).includes(String(FALLWERTE.zucker)) && /keinen Zucker/.test(await dialogLesen()));
ok("Orthostase", await antworte("Druck im Stehen"));
const ortho = await dialogLesen();
ok("Orthostase-Antwort: Stehversuch aus den Falldaten, kein Abfall, nicht beim Aufstehen",
   ortho.includes(FALLWERTE.rr_s3_sys + " zu " + FALLWERTE.rr_s3_dia) && /Kein Abfall/.test(ortho) && /Aufstehen/.test(ortho), ortho.slice(0, 120));
ok("Nachfrage ohne Vorwarnung", await antworte("Vorwarnung"));
ok("Vorwarnung: der gewöhnliche Weg fehlt; beweist nichts, aber Warnzeichen", /fehlt/.test(await dialogLesen()) && /Warnzeichen/.test(await dialogLesen()));
ok("Nachfrage nach dem Beweiswert", await antworte("Beweist das etwas"));
const streng = await dialogLesen();
ok("Antwort nennt die harten Kriterien, nicht nur ein Gefühl (Puls unter 40, Pause über 3 s, plötzlicher Ausfall)",
   /unter vierzig/.test(streng) && /drei Sekunden/.test(streng) && /plötzlich/.test(streng), streng.slice(0, 80));
ok("Alle Expertenfragen gestellt: nur noch „Das war's“", (await antworten()).length === 1);
await antworte("Das war");
ok("Marlene: Sticker-Frage (warmer Raum, kein Fall)", await antworte("Katze"));
ok("Sticker: Patientin 2009", /2009/.test(await dialogLesen()));
await antworte("Zurück");
await antworte("Später");

/* ---------------------------------------------------------- 5 EKG schreiben */
const wagen = feld("wagen");
await wagen.click();
await warte(500);
ok("Rhythmusfrage erscheint", await seite.locator("#frage-hof.an").isVisible());
ok("EKG geschrieben: Meldung mit Uhrzeit", /EKG geschrieben/.test(await letzteMeldung()) && await fallHat("ekg_geschrieben"));
ok("EKG in der Frage gezeichnet", (await seite.locator("#frage-hof canvas").count()) === 1);
await schuss("rhythmusfrage");
/* Die Antworten sind bloße Diagnosen; die Kriterien tragen die Rückmeldungen (Fachabgleich, Lektion 8, 25, 26). */
ok("Rhythmusfrage: Antworten ohne Spickzettel (keine Kriterien im Antworttext)",
   (await seite.locator("#frage-hof .wahl").allTextContents()).every((t) => !/P-Welle|regelmäßig|breite|schnell/.test(t)));
await seite.locator("#frage-hof .wahl", { hasText: "Vorhofflimmern" }).click();
await warte(300);
const rFlimmern = (await seite.locator("#frage-hof .rueck").textContent()) || "";
ok("Falsch „Vorhofflimmern“: beide Kriterien genannt und am Streifen widerlegt",
   /keine P-Wellen/.test(rFlimmern) && /unregelmäßig/.test(rFlimmern) && /vor jedem QRS eine P-Welle/.test(rFlimmern),
   rFlimmern.slice(0, 100));
await warte(2300);                                            /* Knöpfe wieder frei */
await seite.locator("#frage-hof .wahl", { hasText: "Kammertachykardie" }).click();
await warte(300);
const rVt = (await seite.locator("#frage-hof .rueck").textContent()) || "";
ok("Falsch „Kammertachykardie“: breite Komplexe ab 120 ms und Frequenz über 100 — hier schmal und langsam",
   /120 ms/.test(rVt) && /über 100/.test(rVt) && /schmal/.test(rVt), rVt.slice(0, 100));
await warte(2300);
await seite.locator("#frage-hof .wahl", { hasText: "Sinusrhythmus" }).click();
await warte(300);
const rSinus = (await seite.locator("#frage-hof .rueck").textContent()) || "";
ok("Richtig „Sinusrhythmus“: P vor jedem QRS, normal geformt, gleiche Abstände; Frequenz bleibt dem Zirkel",
   /Vor jedem QRS eine P-Welle/.test(rSinus) && /normal geformt/.test(rSinus) && /Abstände bleiben gleich/.test(rSinus) &&
   /Zirkel/.test(rSinus), rSinus.slice(0, 120));
await warte(3000);
ok("Nichts schließt sich von allein: Fenster nach 3 s noch offen, „Weiter“ sichtbar",
   (await seite.locator("#frage-hof.an").count()) === 1 && await seite.locator("#frage-hof .weiter").isVisible());
ok("Kein Befund, bevor „Weiter“ getippt ist", !(await seite.evaluate(() => window.Mappe.hat("b-rhythmus"))));
await seite.keyboard.press("Enter");                          /* Eingabe führt weiter */
await warte(400);
ok("Befund Rhythmus in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-rhythmus")));
const standRhythmus = await speicher();

/* ---------------------------------------------------------- 6 Zirkel: RR */
await wagen.click();
await warte(400);
ok("Messwahl erscheint: RR, PQ, QRS", await seite.locator("#wahl-hof.an").isVisible() && (await seite.locator("#wahl-hof .wahl").count()) === 3);
await seite.locator("#wahl-hof .wahl", { hasText: "RR-Abstand" }).click();
await warte(600);
ok("Zirkel offen", await seite.locator("#zirkel-hof.an").isVisible());
await schuss("zirkel_rr");

const wahrheit = await seite.evaluate(() => {
  const s = window.Spiel.satz(39).schlaege;
  return { r1: s[2].r, r2: s[3].r, p0: s[3].p0, q0: s[3].q0, q1: s[3].q1 };
});
await messe(wahrheit.r1, wahrheit.r2);
ok("RR richtig gemessen", await seite.locator("#zirkel-hof .rueck.gut").isVisible(),
   (await seite.locator("#zirkel-hof .rueck").textContent() || "").slice(0, 110));
await schuss("zirkel_rr_richtig");
await seite.locator("#zirkel-hof .uebernehmen").click();
await warte(400);
ok("Befund Frequenz in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-frequenz")));
/* Lehrbuch Lektion 8: Norm 50–100/min, Sinusbradykardie erst unter 50 — nirgends mehr „unter 60“. */
const karteHf = await seite.evaluate(() => { const b = window.Spiel.zustand.befunde.find((x) => x.id === "b-frequenz"); return window.T(b.text, b.vars); });
ok("Frequenz-Karte: Norm 50–100, Grenze der Sinusbradykardie bei 50, Zahl aus der Messung",
   /50–100/.test(karteHf) && /unter 50/.test(karteHf) && !/60–100|unter 60/.test(karteHf) &&
   karteHf.includes(String(await seite.evaluate(() => window.Spiel.zustand.werte.rr))), karteHf.slice(-90));
ok("Nach dem zweiten Kernbefund der Hinweis auf Marlene", /Marlene/.test(await letzteMeldung()), await letzteMeldung());

/* ---------------------------------------------------------- 7 Zirkel: PQ, erst falsch */
await wagen.click(); await warte(400);
await seite.locator("#wahl-hof .wahl", { hasText: "PQ-Zeit" }).click();
await warte(600);
await messe(wahrheit.q0, wahrheit.q1);                     /* QRS statt PQ gemessen */
const meckern = (await seite.locator("#zirkel-hof .rueck").textContent()) || "";
ok("Falsche Strecke wird erkannt", /andere Strecke|zu spät|zu früh/.test(meckern), meckern.slice(0, 110));
await schuss("zirkel_pq_falsch");
await seite.locator("#zirkel-hof .nochmal").click();
await warte(250);
await messe(wahrheit.p0, wahrheit.q0);
ok("PQ richtig gemessen", await seite.locator("#zirkel-hof .rueck.gut").isVisible(),
   (await seite.locator("#zirkel-hof .rueck").textContent() || "").slice(0, 110));
ok("PQ-Deutung: Norm 120–200, AV-Block I. Grades", /120–200/.test(await rueckText("#zirkel-hof")) && /AV-Block I\. Grades/.test(await rueckText("#zirkel-hof")));
await schuss("zirkel_pq_richtig");
await seite.locator("#zirkel-hof .uebernehmen").click();
await warte(400);
ok("Befund PQ in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-pq")));

/* ---------------------------------------------------------- 7a Zirkel: QRS (optional, dritte Zahl) */
await wagen.click(); await warte(400);
ok("Messwahl: RR und PQ als erledigt markiert, QRS offen",
   (await seite.locator("#wahl-hof .wahl.erledigt").count()) === 2 && (await seite.locator("#wahl-hof .wahl:not(.erledigt)", { hasText: "QRS" }).count()) === 1);
await seite.locator("#wahl-hof .wahl", { hasText: "QRS" }).click();
await warte(600);
await messe(wahrheit.q0, wahrheit.q1);
ok("QRS richtig gemessen, Deutung: schmal (Norm 60–100)", await seite.locator("#zirkel-hof .rueck.gut").isVisible() && /60–100/.test(await rueckText("#zirkel-hof")) && /schmal/.test(await rueckText("#zirkel-hof")),
   (await rueckText("#zirkel-hof")).slice(0, 110));
await seite.locator("#zirkel-hof .uebernehmen").click();
await warte(400);
ok("Befund QRS in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-qrs")));
ok("Messwerte im Zustand: rr, hf, pq, qrs", await seite.evaluate(() => { const w = window.Spiel.zustand.werte; return w.rr > 0 && w.hf > 0 && w.pq > 0 && w.qrs > 0; }));

/* ---------------------------------------------------------- 8 Mappe und Vergleich */
await seite.locator("#hud-mappe").click();
await warte(600);
ok("Mappe offen mit acht Karten", (await seite.locator(".mappe .karte").count()) === 8, String(await seite.locator(".mappe .karte").count()));
ok("EKG auf den Karten", (await seite.locator(".mappe .karte-ekg").count()) >= 3);
const kartenTitel = await seite.locator(".mappe .karte h3").allTextContents();
ok("Karten: Aufnahmebogen, Medikationsplan, Anamnese, Untersuchung, Rhythmus, Frequenz, PQ, QRS",
   /Aufnahmebogen/.test(kartenTitel[0]) && /Medikationsplan/.test(kartenTitel.join(" ")) && /Anamnese/.test(kartenTitel.join(" ")) &&
   /Kurzuntersuchung/.test(kartenTitel.join(" ")) && /Rhythmus/.test(kartenTitel.join(" ")) && /Frequenz/.test(kartenTitel.join(" ")) &&
   /PQ-Zeit/.test(kartenTitel.join(" ")) && /QRS/.test(kartenTitel.join(" ")), kartenTitel.join(" | "));
await schuss("mappe");
const iPq = kartenTitel.findIndex((t) => /^PQ-Zeit/.test(t)), iHf = kartenTitel.findIndex((t) => /^Frequenz/.test(t)), iMed = kartenTitel.findIndex((t) => /Medik/.test(t));
await seite.locator(".mappe .karte").nth(iHf).click();
await seite.locator(".mappe .karte").nth(iPq).click();
await warte(200);
ok("Vergleichen freigeschaltet", await seite.locator(".mappe .vergleich").isEnabled());
await seite.locator(".mappe .vergleich").click();
await warte(700);
ok("Zwei Karten nebeneinander", (await seite.locator(".mappe-vergleich.an canvas").count()) === 2);
ok("Vergleich PQ ↔ Frequenz: zwei Etagen", /Zwei Etagen/.test((await seite.locator(".mappe-vergleich .verg-frage").textContent()) || ""));
await schuss("vergleich");
await seite.locator(".mappe .karte").nth(iPq).click();
await seite.locator(".mappe .karte").nth(iMed).click();
await seite.locator(".mappe .vergleich").click();
await warte(500);
const vglMed = (await seite.locator(".mappe-vergleich .verg-frage").textContent()) || "";
ok("Vergleich Medikationsplan ↔ Frequenz: Betablocker erklärt die gemessene Frequenz, mit der Zahl aus der Messung",
   /Betablocker/.test(vglMed) && vglMed.includes(String(await seite.evaluate(() => window.Spiel.zustand.werte.hf))), vglMed.slice(0, 120));
await seite.keyboard.press("Escape");                      /* Escape schließt die Mappe — und öffnet nicht das Menü */
await warte(300);
ok("Escape schließt die Befundmappe, kein Menü",
   (await seite.locator(".mappe.an").count()) === 0 && (await seite.locator("#menue-hof.an").count()) === 0);
ok("HUD: Mappe zählt acht Befunde", ((await seite.locator("#hud-mappe .hud-zahl").textContent()) || "") === "8");
const standMappe = await speicher();

/* ---------------------------------------------------------- 9 Flur gesperrt, Bericht an Marlene, Übergabe an Dr. Falk */
await seite.locator("#buehne .felder polygon.ausgang").first().click();
await warte(400);
ok("Flur vor dem Bericht an Marlene gesperrt", await seite.evaluate(() => window.Szene.aktueller() === "aufnahme"));
ok("Sperrmeldung sagt, wer anmeldet (Marlene ruft Dr. Falk)", /Marlene/.test(await letzteMeldung()) && /Falk/.test(await letzteMeldung()), await letzteMeldung());
await feld("marlene").click();
await warte(450);
await seite.locator(".dialog-text").click();
await warte(150);
ok("Antwort erscheint erst mit Befund",
   (await seite.locator(".dialog-antwort", { hasText: "Ich hab gemessen" }).count()) === 1);
const gemessen = await seite.evaluate(() => window.Spiel.zustand.werte.pq);
const hfGemessen = await seite.evaluate(() => window.Spiel.zustand.werte.hf);
const berichtKnopf = (await seite.locator(".dialog-antwort", { hasText: "Ich hab gemessen" }).textContent()) || "";
ok("Dialog nennt die selbst gemessenen Werte",
   berichtKnopf.includes(String(gemessen)) && berichtKnopf.includes(String(hfGemessen)), "gemessen: " + hfGemessen + " / " + gemessen);
await seite.locator(".dialog-antwort", { hasText: "Ich hab gemessen" }).click();
await warte(400);
const bericht = await dialogLesen();
ok("Marlene: über zweihundert, lässt keinen umfallen, ruft Dr. Falk herunter, der will Zahlen",
   /zweihundert/.test(bericht) && /umfallen/.test(bericht) && /Falk/.test(bericht) && /Zahlen/.test(bericht), bericht.slice(-100));
await endeKnopf();
ok("Erzähler ohne Porträt: Dr. Falk kommt an den Tresen, den Aufnahmebogen in der Hand",
   (await seite.locator(".dialog.an.ohne-bild").count()) === 1 && /Dr\. Falk am Tresen/.test(await dialogLesen()) && /Aufnahmebogen/.test(await dialogLesen()));
await seite.locator(".dialog-antwort.weiter").click();
await warte(350);
ok("Dr. Falk als Porträt-Dialog in der Aufnahme: nur Zahlen", (await seite.locator(".dialog-bild svg").count()) === 1 &&
   /Falk/.test((await seite.locator(".dialog-name").textContent()) || "") && /gemessen haben/.test(await dialogLesen()));
await schuss("falk_tresen");
opt = await antworten();
ok("Beste Antwort nur mit beiden Befunden — hier mit allen drei Zahlen",
   (await seite.locator(".dialog-antwort", { hasText: "Sinusrhythmus," }).count()) === 1 && opt[0].includes("QRS " + (await seite.evaluate(() => window.Spiel.zustand.werte.qrs))), opt.join(" / "));
ok("Umweg über die Anamnese: Falk will Zahlen", await antworte("ohne Vorwarnung umgekippt") && /Zahlen/.test(await dialogLesen()));
await seite.locator(".dialog-antwort", { hasText: "Sinusrhythmus," }).click();
await warte(400);
ok("Falk: langsam, lang, schmal — fragt nach dem Medikament, das beides bremst",
   /schmal/.test(await dialogLesen()) && /Nimmt er etwas/.test(await dialogLesen()) && (await seite.locator(".dialog-antwort", { hasText: "Bisoprolol" }).count()) === 1 &&
   (await seite.locator(".dialog-antwort", { hasText: "Das weiß ich nicht" }).count()) === 0);
await antworte("Bisoprolol");
ok("Falk: Tabletten erklären die Zahlen, nicht den Boden", /Tabletten die Zahlen/.test(await dialogLesen()) && /Boden/.test(await dialogLesen()));
opt = await antworten();
ok("Expertenfragen an Falk: TIA, Orthostase, Entscheidung", /TIA/.test(opt.join(" ")) && /Kreislauf/.test(opt.join(" ")) && /Nach Hause/.test(opt.join(" ")), opt.join(" / "));
ok("„Ist das nicht eine TIA?“ bei Falk", await antworte("TIA"));
const fTia = await dialogLesen();
ok("Falk: TIA nimmt Sprache oder Kraft, lässt das Bewusstsein in Ruhe; bei ihm umgekehrt (dieselbe Aussage wie Marlene, andere Stimme)",
   /Bewusstsein/.test(fTia) && /umgekehrt/.test(fTia) && !/Leitlinie|ESC/.test(fTia), fTia.slice(0, 120));
await seite.locator(".dialog-antwort.weiter").click();
await warte(300);
ok("Falk: Hirnstamm nie ohne Herdzeichen, fragt nach Gang und Armen", /Herdzeichen/.test(await dialogLesen()) && /Arme/.test(await dialogLesen()));
await antworte("seitengleich");
ok("Falk: keine TIA", /keine TIA/.test(await dialogLesen()));
await antworte("Kreislauf");
const fOrtho = await dialogLesen();
ok("Falk: Stehversuch aus den Falldaten, nach zehn Minuten Stehen, nicht beim Aufstehen",
   fOrtho.includes(FALLWERTE.rr_l_sys + " zu " + FALLWERTE.rr_l_dia) && /zehn Minuten/.test(fOrtho) && /Aufstehen/.test(fOrtho), fOrtho.slice(0, 120));
await antworte("Nach Hause");
const ent1 = await dialogLesen();
ok("Entscheidung: keine Vorwarnung, zweimal, EKG nicht sauber → nicht heimschicken, Monitor",
   /Keine Vorwarnung/.test(ent1) && /zweimal/.test(ent1) && /nicht heimzuschicken/.test(ent1) && /Monitor/.test(ent1), ent1.slice(0, 120));
await schuss("entscheidung");
await seite.locator(".dialog-antwort.weiter").click(); await warte(300);
const ent2 = await dialogLesen();
await seite.locator(".dialog-antwort.weiter").click(); await warte(300);
const ent3 = await dialogLesen();
const ent = ent2 + " | " + ent3;
ok("Einordnung: Beweis wäre Pause oder Block mit plötzlich ausfallenden Schlägen; sieht man nur am Monitor; entschieden wird am Bett",
   /Weil ich es nicht weiß/.test(ent2) && /plötzlich Schläge ausfallen/.test(ent2) && /Monitor/.test(ent3) && /am Bett/.test(ent3), ent.slice(0, 200));
ok("Übergabe endet mit „Verstanden.“", ((await seite.locator(".dialog-antwort.weiter").textContent()) || "").trim() === "Verstanden.");
await seite.locator(".dialog-antwort.weiter").click();
ok("Keine Therapie, keine Dosis, kein Pacer in der Übergabe", !/Pacer|Dosis|\bmg\b|Schrittmacher|Atropin/.test(ent + ent1 + fTia + fOrtho));
await warte(400);
ok("Klares Ende des Falls: Erzähler, Herr Baum geht nach oben, Marlene schenkt Kaffee nach (D4: Verhalten statt Gefühl)",
   (await seite.locator(".dialog.an.ohne-bild").count()) === 1 && /nach oben/.test(await dialogLesen()) && /Kaffee/.test(await dialogLesen()));
await dialogDurch();
await warte(300);
ok("Fall beendet: Marke fall_ende, Herr Baum und Tüte nicht mehr im Raum, Wagen bleibt",
   await fallHat("fall_ende") && (await feld("herrk").count()) === 0 && (await feld("wagen").count()) === 1 &&
   await seite.evaluate(() => ["#fig-herrk", "#fig-tuete"].every((s) => { const f = document.querySelector(s); return !!f && getComputedStyle(f).display === "none"; })));
await schuss("ende_kapitel1");
st = await standLesen();
ok("Stand am Ende von Kapitel 1: Falks Entscheidung, Flur offen, nichts von einer Tüte",
   /Entscheidung/.test(st.hat) && /Flur/.test(st.offen) && !/Tüte/.test(st.hat + st.offen), st.offen.slice(0, 120));
ok("Stand ohne tote Fäden aus der Aufnahme", !/Mit Herrn Baum selbst|Marlene weiß|Frag ihn|fehlt noch/.test(st.offen), st.offen.slice(0, 160));
await standZu();
await feld("marlene").click();
await warte(450);
const grussUnten = await dialogLesen();
ok("Marlene nach der Verlegung: er liegt oben — ohne Tüten-Verweis", /oben/.test(grussUnten) && !/Tüte/.test(grussUnten), grussUnten);
await antworte("Später");
/* Nur Herr Baum geht: Die Kurve auf dem Wagen läuft weiter — der Streifen von heute früh liegt ja noch dort. */
const schirmeUnten = await seite.evaluate(() => window.Spiel.__schirme());
ok("Auf dem EKG-Wagen läuft weiter die Kurve von heute früh",
   schirmeUnten.some((s) => s.name === "wagen_schirm" && s.satz === 39 && s.laeuft) &&
   (await seite.locator("#buehne .ebene-mittelgrund .schirm-lauf[data-schirm=wagen_schirm] canvas").isVisible()), JSON.stringify(schirmeUnten));
const standEnde = await speicher();

/* ---------------------------------------------------------- 10 Raumwechsel */
const ausgang = seite.locator("#buehne .felder polygon.ausgang").first();
await ausgang.click();
await warte(1100);
ok("Im Monitorzimmer", await seite.evaluate(() => window.Szene.aktueller() === "monitor"));
ok("Monitorkurve läuft (großer Schirm, Papier)", (await seite.locator("#buehne .ebene-hintergrund .schirm-lauf[data-schirm=gross] canvas").count()) === 1);
/* Bettmonitore: drei Leinwände, je eine der drei Aufnahmen der Zentrale, in Bettenfolge, alle laufend */
const schirme2 = await seite.evaluate(() => window.Spiel.__schirme());
const bettenJetzt = await seite.evaluate(() => window.Spiel.__betten().map((b) => b.id));
const kleine = schirme2.filter((s) => /^bett_\d$/.test(s.name)).sort((a, b) => a.name < b.name ? -1 : 1);
ok("Bettmonitore: drei laufende Kurven in Bettenfolge",
   kleine.length === 3 && kleine.every((s, i) => s.laeuft && s.satz === bettenJetzt[i]) &&
   new Set(kleine.map((s) => s.satz)).size === 3, JSON.stringify(kleine) + " Betten " + bettenJetzt.join(","));
ok("Keine Leinwand der Aufnahme mehr aktiv", schirme2.every((s) => s.name !== "wagen_schirm"));
await warte(1600);
ok("Kapitelwechsel: der Erzähler erklärt die zweieinhalb Stunden, ohne Porträt",
   (await seite.locator(".dialog.an.ohne-bild").count()) === 1 && /Zweieinhalb Stunden/.test(await dialogLesen()));
await schuss("monitorzimmer");
await seite.locator(".dialog-antwort.weiter").click();
await warte(350);
ok("Dr. Falk spricht an — kein zweites Verhör, er hat die Zahlen schon", (await seite.locator(".dialog-bild svg").count()) === 1 &&
   /beobachtet/.test(await dialogLesen()) && !/gemessen haben/.test(await dialogLesen()));
const textFalk = await dialogDurchLesen();
ok("Falk: der Monitor ersetzt das Zwölfkanal-EKG nicht", /Zwölfkanal/.test(textFalk));
ok("Auftrag mit den drei Betten", await seite.evaluate(() => window.Spiel.hat("k2_auftrag")) && /drei Betten/.test(textFalk));
await schuss("nach_falk");

/* ---------------------------------------------------------- 11 Neu laden */
const gespeichert = await seite.evaluate(() => {
  try { const g = JSON.parse(window.localStorage.getItem("nachtdienst-1") || "null"); return g ? g.raum + "/" + g.befunde.length : "leer"; }
  catch (e) { return "kaputt: " + e; }
});
ok("Zustand vor dem Neuladen gespeichert (Raum/Befunde)", gespeichert === "monitor/8", gespeichert);
await seite.reload();
await seite.locator("#titel").waitFor({ state: "visible", timeout: 5000 });
const titelStand = (await seite.locator("#titel .titel-stand").count())
  ? ((await seite.locator("#titel .titel-stand").textContent()) || "") : "";
ok("Nach dem Neuladen: Titel bietet „Weiterspielen“ mit dem gespeicherten Stand",
   (await seite.locator("#titel-weiter").count()) === 1 && /09:\d\d/.test(titelStand) && /\b8\b/.test(titelStand), titelStand);
ok("Vor „Weiterspielen“ läuft nichts (kein Dialog, keine Szene)",
   (await seite.locator(".dialog.an").count()) === 0 && await seite.evaluate(() => !window.Szene.aktueller()));
await vomTitel();
await warte(1200);
const nachLaden = await seite.evaluate(() => ({
  raum: window.Szene && window.Szene.aktueller(),
  befunde: window.Spiel && window.Spiel.zustand.befunde.length,
  dialogOffen: document.querySelectorAll(".dialog.an").length,
  dialog: ((document.querySelector(".dialog.an .dialog-text") || {}).textContent || "").slice(0, 60),
  zeichenBeimStart: window.__speicherBeimStart,
  spracheBeimStart: window.__spracheBeimStart,
  ursprung: window.__ursprung,
  fallEnde: window.Fall.hat("aufnahme_baum", "fall_ende"),
  betten: (window.Spiel.zustand.werte.betten || []).join(","),
  speicher: (() => { try { const g = JSON.parse(window.localStorage.getItem("nachtdienst-1") || "null"); return g ? g.raum + "/" + g.befunde.length : "leer"; } catch (e) { return "kaputt"; } })()
}));
/* Beobachtet (selten): Chromium reicht dem neu geladenen Dokument einen ganz leeren file://-Speicher — auch ohne den
   Sprachschlüssel, den nur dieser Durchlauf setzt und nichts löscht. Dann hat der Browser verworfen, nicht das Spiel. */
const browserVerwarf = nachLaden.zeichenBeimStart === 0 && nachLaden.spracheBeimStart === false;
ok("Zustand übersteht Neuladen", nachLaden.raum === "monitor",
   JSON.stringify(nachLaden) + (browserVerwarf
     ? " — Browser lieferte beim Neuladen einen leeren file://-Speicher (auch ohne Sprachschlüssel); vorher war gespeichert: " + gespeichert
     : ""));
ok("Befunde noch da", nachLaden.befunde === 8, String(nachLaden.befunde));
ok("Marken des Falls überstehen das Neuladen (Z.faelle)", nachLaden.fallEnde === true);
ok("Kein Auftakt bei Fortsetzung", nachLaden.dialogOffen === 0, nachLaden.dialog);
await schuss("nach_neuladen");

/* --------------------------------------------------- 11b Hotspots zeigen */
await seite.locator("#hud-hinweis").click();
await warte(300);
ok("Hotspot-Hilfe schaltet sich ein", await seite.evaluate(
  () => document.querySelector(".felder").classList.contains("zeigen")));
await schuss("hotspots_gezeigt");

/* ================================================== Kapitel 2: Monitorzimmer
   Vier Wege durch dasselbe Kapitel, alle bis zum Epilog:
     A  Tastatur · erst zwei falsche Betten · Begründung PQ · Ampel: Arzt rufen
     B  großer Monitor · Begründung Frequenz · Ampel weggeklickt, über Dr. Falk
        wieder geholt · Zeit läuft ab
     C  Neubetreten nach dem Fund · Ampel: Pacer
     D  Neubetreten · Ampel weggeklickt, über den großen Monitor · Beobachten   */
await warte(2600);                                         /* Hotspot-Hilfe aus */

const K2 = await seite.evaluate(() => window.Spiel.KAPITEL2_EKG);
const MESS = await seite.evaluate((k) => ({
  baum: window.Spiel.satz(k.baum).mess, flimmern: window.Spiel.satz(k.flimmern).mess,
  schnell: window.Spiel.satz(k.schnell).mess
}), K2);
/* Wo liegt welches Bett? Die Folge wird je Schicht gemischt. */
async function bettIndex() {
  await seite.evaluate(() => { window.Spiel.__betten(); });
  const b = (await zustand()).werte.betten;
  return { baum: b.indexOf(K2.baum), flimmern: b.indexOf(K2.flimmern), schnell: b.indexOf(K2.schnell) };
}

ok("K2: Falk hat den Auftrag gegeben", await seite.evaluate(() => window.Spiel.hat("k2_auftrag")));
ok("K2: Neues Feld an der Monitorwand", (await feld("wand").count()) === 1);
st = await standLesen();
ok("K2: Stand nennt den Auftrag", /drei Schirme/.test(st.offen), st.offen.slice(0, 140));
ok("K2: Stand verrät weder Bett noch Merkmal",
   !/Bett \d|Vorhofflimmern|PQ \d|\b228\b/.test(st.offen), st.offen.slice(0, 140));
ok("K2: Kapitel 2 im Stand", /Kapitel 2/.test(st.zeile));
await standZu();
const vorZentrale = await speicher();

/* ------------------------------------------------------------ Weg A */
await feld("wand").click();
await warte(700);
ok("A: Zentrale öffnet sich", await seite.locator("#schirme-hof.an").isVisible());
ok("A: drei Schirme mit Kurve", (await seite.locator("#schirme-hof .schirm canvas").count()) === 3);
const auftragZentrale = (await seite.locator("#schirme-hof .raetsel-auftrag").textContent()) || "";
ok("A: Kästchengröße mit Papiervorschub genannt (5 mm bei 25 mm/s = 200 ms)",
   /5 mm/.test(auftragZentrale) && /25 mm\/s/.test(auftragZentrale) && /200 ms/.test(auftragZentrale), auftragZentrale.slice(-60));
const bilder = await seite.evaluate(() => Array.from(document.querySelectorAll("#schirme-hof .schirm canvas"))
  .map((c) => c.getContext("2d").getImageData(0, 0, c.width, c.height).data.some((v, i) => i % 4 === 1 && v > 200)));
ok("A: auf jedem Schirm leuchtet eine Kurve", bilder.length === 3 && bilder.every(Boolean), JSON.stringify(bilder));
ok("A: „Zurück“ oben rechts", await seite.evaluate(() => {
  const k = document.querySelector("#schirme-hof .raetsel-kopf"), z = k.querySelector(".zu");
  return z.textContent.trim() === "Zurück" && k.getBoundingClientRect().right - z.getBoundingClientRect().right < 40;
}));
let zuKlein = await fingergross("#schirme-hof");
ok("A: Knöpfe der Zentrale fingergroß", !zuKlein.length, zuKlein.join(", "));
let blinkt = await ohneBlinken("#schirme-hof");
ok("A: nichts blinkt in der Zentrale", !blinkt.length, blinkt.join(", "));
await schuss("k2_zentrale");

let idx = await bettIndex();
await seite.keyboard.press(String(idx.flimmern + 1));         /* Ziffer wählt */
await warte(250);
let r = await rueckText("#schirme-hof");
ok("A: falsches Bett (Flimmern) per Ziffer, mit Begründung",
   (await seite.locator("#schirme-hof .rueck.fast").count()) === 1 && /P-Welle/.test(r) && /Vorhofflimmern/.test(r),
   r.slice(0, 120));
await seite.locator("#schirme-hof .frage-wahl .knopf").nth(idx.schnell).click();
await warte(250);
r = await rueckText("#schirme-hof");
ok("A: falsches Bett (schnell) nennt Zahlen aus den Daten",
   r.includes(String(MESS.schnell.frequenz)) && r.includes(String(MESS.schnell.pq)), r.slice(0, 160));
await schuss("k2_zentrale_falsch");
await seite.keyboard.press(String(idx.baum + 1));
await warte(250);
ok("A: richtiges Bett erkannt", (await seite.locator("#schirme-hof .rueck.gut").count()) === 1);
await seite.keyboard.press("Enter");                         /* Enter führt weiter */
await warte(300);
ok("A: Begründungsfrage nennt das Bett",
   ((await seite.locator("#schirme-hof .schirme-frage").textContent()) || "").includes("Bett " + (idx.baum + 1)));
ok("A: sein Schirm ist hervorgehoben",
   (await seite.locator(`#schirme-hof .schirm.hervor[data-i="${idx.baum}"]`).count()) === 1);
await seite.keyboard.press("1");                             /* P-Wellen: reicht allein nicht */
await warte(250);
r = await rueckText("#schirme-hof");
ok("A: „P vor jedem QRS“ allein reicht nicht — mit Grund",
   (await seite.locator("#schirme-hof .rueck.fast").count()) === 1 && /nicht von beiden/.test(r), r.slice(0, 140));
await seite.keyboard.press("3");                             /* PQ */
await warte(250);
r = await rueckText("#schirme-hof");
ok("A: Begründung PQ angenommen, Zahlen aus den Daten",
   (await seite.locator("#schirme-hof .rueck.gut").count()) === 1 &&
   r.includes(String(MESS.baum.pq)) && r.includes(String(MESS.schnell.pq)), r.slice(0, 160));
await schuss("k2_zentrale_begruendet");
await seite.locator("#schirme-hof .weiter").click();
await warte(600);
ok("A: Befund „Monitor“ in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-monitor")));
ok("A: Dr. Falk antwortet auf die PQ-Begründung", /PQ-Zeit/.test(await dialogLesen()));
await schuss("k2_falk_pq");
const textA1 = await dialogDurchLesen();
ok("A: Falk übergibt das Bett", /Ab jetzt gehört er Ihnen/.test(textA1), textA1.slice(-120));
await warte(2400);
ok("A: Bett klingelt — Ampel öffnet sich", await seite.locator("#ampel-hof.an").isVisible());
const lage = (await seite.locator("#ampel-hof .ampel-lage").textContent()) || "";
ok("A: Lage nennt Frequenz aus den Daten", lage.includes(MESS.baum.frequenz + " pro Minute"), lage.slice(-60));
ok("A: Lage behauptet keinen höhergradigen Block",
   !/Block|Pause|fällt aus|Wenckebach|Mobitz/i.test(lage), lage.slice(0, 80));
ok("A: Das Foto von Lena steht am Bett (die Frage wurde unten gestellt)", /Foto von Lena/.test(lage));
ok("A: Monitor läuft in der Ampel", (await seite.locator("#ampel-hof canvas").count()) === 1);
ok("A: Zeit läuft erst nach „Los“", (await seite.locator("#ampel-hof .ampel-entscheidung").isHidden()));
await schuss("k2_ampel_lage");
await seite.keyboard.press("Enter");                         /* Los */
await warte(250);
const breite1 = await seite.evaluate(() => document.querySelector("#ampel-hof .ampel-balken").getBoundingClientRect().width);
await warte(1200);
const breite2 = await seite.evaluate(() => document.querySelector("#ampel-hof .ampel-balken").getBoundingClientRect().width);
ok("A: Zeitbalken schrumpft sichtbar", breite2 < breite1 - 20, Math.round(breite1) + " → " + Math.round(breite2));
ok("A: drei Handlungen", (await seite.locator("#ampel-hof .ampel-knopf").count()) === 3);
ok("A: Gelb heißt bleiben und rufen — so, wie Falk es danach lobt",
   /bleiben/.test((await seite.locator("#ampel-hof .ampel-knopf").nth(1).textContent()) || ""));
zuKlein = await fingergross("#ampel-hof");
ok("A: Ampel-Knöpfe fingergroß", !zuKlein.length, zuKlein.join(", "));
blinkt = await ohneBlinken("#ampel-hof");
ok("A: nichts blinkt in der Ampel", !blinkt.length, blinkt.join(", "));
await schuss("k2_ampel_entscheidung");
await seite.keyboard.press("2");                             /* Arzt rufen */
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("A: Falk zur richtigen Wahl", /Gerufen, und bei ihm geblieben/.test(await dialogLesen()));
await schuss("k2_ampel_falk");
const textA2 = await dialogDurchLesen(24);
ok("A: Schlussszene nennt die Frequenz aus den Daten",
   textA2.includes("Sinus, " + MESS.baum.frequenz + " pro Minute"), textA2.slice(0, 120));
ok("A: Falk bleibt in der Rolle (Pause über drei Sekunden, wach); was das Spiel über sich sagt, sagt der Erzähler",
   /Pause über drei Sekunden/.test(textA2) && textA2.indexOf("Verstanden.]") >= 0 &&
   textA2.indexOf("Verstanden.]") < textA2.indexOf("Dienst 3"), textA2.slice(-200));
ok("A: Ende und Epilog: Erzählung in einem späteren Dienst — Pause über drei Sekunden, wach; Kardiologie",
   /Dienst 3/.test(textA2) && /Pause/.test(textA2) && /drei Sekunden/.test(textA2) && /wach/.test(textA2) &&
   /Kardiologie/.test(textA2) && /Ende des spielbaren Teils/.test(textA2), textA2.slice(-300));
{
  const epi = textA2.slice(textA2.indexOf("Dienst 3"));
  ok("A: Epilog nach Leitlinie: erst der Betablocker abgesetzt, dann bei erneuter Pause der Schrittmacher",
     /Bisoprolol abgesetzt/.test(epi) && /ohne Betablocker/.test(epi) && /Zweikammer-Schrittmacher/.test(epi) &&
     epi.indexOf("abgesetzt") < epi.indexOf("Zweikammer-Schrittmacher"), epi.slice(0, 400));
  ok("A: Epilog ohne Dosisangaben", !/Dosis|\bmg\b|\d+\s*mg/.test(epi));
}
let z = await zustand();
ok("A: Ziel erreicht (Wahl: Arzt)", z.marken.k2_fertig && z.werte.ampel === "arzt", JSON.stringify(z.werte.ampel));
ok("A: neun Befunde (acht aus der Aufnahme, der Monitor)", z.befunde.length === 9, String(z.befunde.length));

st = await standLesen();
ok("A: Stand sagt, dass hier das Gebaute endet, und nennt den Epilog", /Damit endet/.test(st.fuss) && /Epilog/.test(st.fuss), st.fuss.slice(0, 80));
ok("A: Stand führt die Episode auf", /geklingelt/.test(st.hat), st.hat.slice(-100));
await schuss("k2_stand_ende");
await standZu();

/* Vergleich der neuen Karte mit dem Aufnahme-EKG */
await seite.locator("#hud-mappe").click();
await warte(600);
const titel = await seite.locator(".mappe .karte h3").allTextContents();
const iMon = titel.findIndex((t) => /^Monitor/.test(t)), iPq2 = titel.findIndex((t) => /^PQ-Zeit/.test(t));
await seite.locator(".mappe .karte").nth(iMon).click();
await seite.locator(".mappe .karte").nth(iPq2).click();
await seite.locator(".mappe .vergleich").click();
await warte(700);
const pqSpanne = await seite.evaluate((id) => {
  const w = window.Spiel.satz(id).schlaege.filter((s) => s.p0 !== undefined).map((s) => Math.round((s.q0 - s.p0) * 1000));
  return { min: Math.min(...w), max: Math.max(...w) };
}, K2.baum);
const vergleich = (await seite.locator(".mappe-vergleich .verg-frage").textContent()) || "";
ok("A: Monitorkarte lässt sich mit dem Aufnahme-EKG vergleichen",
   (await seite.locator(".mappe-vergleich.an canvas").count()) === 2 &&
   vergleich.includes(pqSpanne.min + " und " + pqSpanne.max + " ms"), vergleich.slice(0, 160));
await schuss("k2_vergleich");
await seite.locator(".mappe .zu").click();
await warte(300);

await feld("falk").click();
await warte(450);
ok("A: Falk danach, ohne neue Begrüßung", /Speicher/.test(await dialogLesen()));
await dialogDurchLesen();
await feld("wand").click();
await warte(600);
ok("A: Monitorwand danach als Rückschau mit Befund je Schirm",
   (await seite.locator("#schirme-hof.an.rueckschau .schirm-unter").count()) === 3);
await schuss("k2_rueckschau");
await seite.keyboard.press("Escape");
await warte(300);
ok("A: Escape schließt die Rückschau", (await seite.locator("#schirme-hof.an").count()) === 0);
/* Der große Monitor nach dem Fund: 53/min ist nach Lektion 8 Sinusrhythmus am unteren Rand, keine Bradykardie. */
await feld("schirm").click();
await warte(300);
const meldungSchirm = await letzteMeldung();
ok("A: großer Monitor nennt Sinusrhythmus, langsam — nicht „Sinusbradykardie“ bei " + MESS.baum.frequenz + "/min",
   /Sinusrhythmus/.test(meldungSchirm) && !/Sinusbradykardie/.test(meldungSchirm) &&
   meldungSchirm.includes(MESS.baum.frequenz + "/min"), meldungSchirm.slice(0, 90));

/* ------------------------------------------------------------ Weg B */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), vorZentrale);
await neuLaden();
await warte(2000);
ok("B: wieder vor der Zentrale", !(await zustand()).marken.k2_bett && (await seite.locator(".dialog.an").count()) === 0);
await feld("schirm").click();                                /* der große Monitor führt auch hin */
await warte(700);
ok("B: großer Monitor öffnet die Zentrale", await seite.locator("#schirme-hof.an").isVisible());
idx = await bettIndex();
await seite.locator("#schirme-hof .frage-wahl .knopf").nth(idx.baum).click();
await warte(250);
await seite.locator("#schirme-hof .weiter").click();
await warte(300);
await seite.locator("#schirme-hof .frage-wahl .knopf", { hasText: "Frequenz" }).click();
await warte(250);
r = await rueckText("#schirme-hof");
ok("B: Begründung Frequenz angenommen, Zahlen aus den Daten",
   (await seite.locator("#schirme-hof .rueck.gut").count()) === 1 &&
   r.includes(String(MESS.baum.frequenz)) && r.includes(String(MESS.schnell.frequenz)) &&
   r.includes(String(MESS.flimmern.frequenz)), r.slice(0, 160));
await seite.locator("#schirme-hof .weiter").click();
await warte(600);
ok("B: Falk antwortet auf die Frequenz-Begründung", /Die Frequenz/.test(await dialogLesen()));
const nachFund = await speicher();
await dialogDurchLesen();
await warte(2400);
ok("B: Ampel öffnet sich", await seite.locator("#ampel-hof.an").isVisible());
await seite.locator("#ampel-hof .zu").click();               /* weggeklickt: keine Sackgasse */
await warte(400);
ok("B: „Zurück“ schließt die Ampel", (await seite.locator("#ampel-hof.an").count()) === 0);
st = await standLesen();
ok("B: Stand erinnert an die Klingel", /hat geklingelt/.test(st.offen), st.offen.slice(-90));
await standZu();
await feld("falk").click();
await warte(450);
ok("B: Falk schickt zum Bett", /klingelt/.test(await dialogLesen()));
await seite.locator(".dialog-antwort", { hasText: "Ich geh" }).click();
await warte(900);
ok("B: Ampel über Dr. Falk wieder da", await seite.locator("#ampel-hof.an").isVisible());
await seite.locator("#ampel-hof .ampel-los").click();
await seite.locator("#ampel-hof .rueck.fast").waitFor({ timeout: 13000 });   /* niemand entscheidet */
ok("B: Zeit abgelaufen, mit Satz statt Strafe",
   /Zeit ist um/.test(await rueckText("#ampel-hof")), await rueckText("#ampel-hof"));
await schuss("k2_ampel_zeit");
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("B: Falk korrigiert trocken", /Zehn Sekunden/.test(await dialogLesen()));
const textB = await dialogDurchLesen(24);
z = await zustand();
ok("B: Ziel erreicht (Zeit abgelaufen), Epilog am Ende", z.marken.k2_fertig && z.werte.ampel === "zeit" &&
   /Ende des spielbaren Teils/.test(textB) && /Kardiologie/.test(textB), z.werte.ampel);
ok("B: Karte nennt die Frequenz als Merkmal",
   /Erkannt an der Frequenz/.test(z.befunde.find((b) => b.id === "b-monitor").text));

/* ------------------------------------------------------------ Weg C */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), nachFund);
await neuLaden();
await warte(2600);
ok("C: beim Betreten klingelt das Bett (wieder)", await seite.locator("#ampel-hof.an").isVisible());
await seite.locator("#ampel-hof .ampel-los").click();
await warte(300);
await seite.locator("#ampel-hof .ampel-knopf", { hasText: "Pacer" }).click();
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("C: Falk korrigiert den Pacer", /Gelb, nicht Rot/.test(await dialogLesen()));
await schuss("k2_ampel_pacer");
await dialogDurchLesen(24);
z = await zustand();
ok("C: Ziel erreicht (Pacer)", z.marken.k2_fertig && z.werte.ampel === "pacer", z.werte.ampel);

/* ------------------------------------------------------------ Weg D */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), nachFund);
await neuLaden();
await warte(2600);
await seite.keyboard.press("Escape");                        /* Escape schließt auch die Ampel */
await warte(300);
ok("D: Escape schließt die Ampel", (await seite.locator("#ampel-hof.an").count()) === 0);
await feld("schirm").click();
await warte(500);
ok("D: großer Monitor holt die Ampel zurück", await seite.locator("#ampel-hof.an").isVisible());
await seite.keyboard.press(" ");                             /* Leertaste: Los */
await warte(250);
await seite.keyboard.press("1");                             /* Beobachten */
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("D: Falk korrigiert das bloße Beobachten", /Gelb, nicht Grün/.test(await dialogLesen()));
await dialogDurchLesen(24);
z = await zustand();
ok("D: Ziel erreicht (Beobachten)", z.marken.k2_fertig && z.werte.ampel === "beobachten", z.werte.ampel);
ok("Kapitel 2: vier Wege, alle bis zum Epilog", true);

/* ------------------------------------------------- 12 Drei Sprachen */
for (const [kurz, probe] of [["en", "Findings"], ["ru", "Папка находок"]]) {
  await seite.evaluate((k) => { window.localStorage.setItem("nachtdienst-sprache", k); }, kurz);
  await seite.reload();
  await seite.locator("#titel").waitFor({ state: "visible", timeout: 5000 });
  const titelKnopf = (await seite.locator("#titel-weiter").count())
    ? ((await seite.locator("#titel-weiter").textContent()) || "").trim() : "(kein „Weiterspielen“)";
  ok("Sprache " + kurz + ": Titel übersetzt", titelKnopf === { en: "Continue", ru: "Продолжить" }[kurz], titelKnopf);
  await vomTitel();
  await warte(900);
  const kopf = (await seite.locator("#hud-mappe").textContent()) || "";
  ok("Sprache " + kurz + " schaltet um", kopf.includes(probe), kopf.trim());
  /* Karten aus dem Fall tragen IDs: Sie erscheinen in der Sprache des Spielers — mit den gemessenen Zahlen. */
  await seite.locator("#hud-mappe").click(); await warte(400);
  const kartenSp = await seite.locator(".mappe .karte h3").allTextContents();
  ok("Sprache " + kurz + ": Karten des Falls übersetzt, Zahlen bleiben",
     kartenSp.some((t) => t.includes({ en: "Admission sheet", ru: "Лист приёма" }[kurz])) &&
     kartenSp.some((t) => /(Rate|Частота): \d+\/(min|мин)/.test(t)), kartenSp.join(" | "));
  await seite.locator(".mappe .zu").click(); await warte(200);
  await schuss("sprache_" + kurz);
}
await seite.evaluate(() => { window.localStorage.setItem("nachtdienst-sprache", "de"); });
await neuLaden();
await warte(900);

/* ------------------------------------------------- 12b Sprache aus dem Menü
   Der Wechsel lädt neu; danach geht es ohne Titel weiter, mit offenem Menü in der neuen Sprache. */
const vorWechsel = await zustand();
await seite.locator("#hud-menue").click();
await warte(250);
await Promise.all([seite.waitForEvent("load"), seite.locator('#menue-hof .knopf.sprache[data-sprache="en"]').click()]);
await warte(900);
ok("Menü-Sprachwechsel: kein Titel, das Menü ist wieder offen",
   !(await seite.locator("#titel").isVisible()) && await seite.locator("#menue-hof.an").isVisible());
const menueEn = (await seite.locator("#menue-hof").textContent()) || "";
ok("Menü-Sprachwechsel: Menü und HUD auf Englisch",
   /Resume/.test(menueEn) && /About & sources/.test(menueEn) &&
   ((await seite.locator("#hud-mappe").textContent()) || "").includes("Findings") &&
   await seite.evaluate(() => document.documentElement.lang === "en" && window.localStorage.getItem("nachtdienst-sprache") === "en"),
   menueEn.slice(0, 120));
ok("Menü-Sprachwechsel: English ist markiert",
   (await seite.locator('#menue-hof .knopf.sprache[aria-pressed="true"]').textContent()) === "English");
const nachWechsel = await zustand();
ok("Menü-Sprachwechsel: Spielstand bleibt (Raum, Zeit, Befunde)",
   nachWechsel.raum === vorWechsel.raum && nachWechsel.zeit === vorWechsel.zeit && nachWechsel.befunde.length === vorWechsel.befunde.length,
   vorWechsel.raum + "/" + vorWechsel.befunde.length + " → " + nachWechsel.raum + "/" + nachWechsel.befunde.length);
await schuss("menue_englisch");
await seite.locator("#menue-info").click();
await warte(250);
const infoEn = (await seite.locator("#info-hof").textContent()) || "";
ok("Info auf Englisch, Quellen unverändert", /Not a medical device/.test(infoEn) && /ODC-By 1\.0/.test(infoEn) && /CC BY 4\.0/.test(infoEn));
await seite.locator("#info-hof .zu").click();
await warte(200);
await Promise.all([seite.waitForEvent("load"), seite.locator('#menue-hof .knopf.sprache[data-sprache="de"]').click()]);
await warte(900);
ok("Menü-Sprachwechsel zurück auf Deutsch", /Fortsetzen/.test((await seite.locator("#menue-hof").textContent()) || "") &&
   ((await seite.locator("#hud-mappe").textContent()) || "").includes("Befundmappe"));
await seite.locator("#menue-weiter").click();
await warte(300);
ok("Nach dem Sprachwechsel geht das Spiel weiter", (await seite.locator("#menue-hof.an").count()) === 0 &&
   await seite.evaluate(() => window.Szene.aktueller()) === vorWechsel.raum);

/* ---------------------------------------------------------- 13 Zurück, Sperre */
await seite.evaluate(() => { window.localStorage.clear(); });
await neuLaden();
await warte(1200);
await dialogDurch();
const gesperrt = seite.locator("#buehne .felder polygon.ausgang").first();
await gesperrt.click();
await warte(400);
ok("Ausgang ohne Befunde gesperrt", await seite.evaluate(() => window.Szene.aktueller() === "aufnahme"));
ok("Begründung als Meldung", (await seite.locator(".meldung").count()) >= 1);
await schuss("gesperrt");

/* ------------------------------------------------- 14 Übergabe nur mit beiden Zahlen: die Rückwege
   R1  Nur die Frequenz gemessen → Marlene ruft Falk, warnt aber → Falk schickt zum Wagen zurück, kein Ende →
       PQ nachgemessen → Hinweis → über Marlene zu Falk → Falk nimmt an → Monitor.
   R2  Nur die PQ-Zeit → Marlene mahnt die Frequenz an → Falk fragt nach der Frequenz → zurück.
   R3  Medikamente nie gefragt → Falk: „Das weiß ich nicht“ → zum Patienten → Plan → zurück zu Falk.          */
async function zirkel(was, von, bis) {
  await wagen.click(); await warte(400);
  await seite.locator("#wahl-hof .wahl", { hasText: was }).click(); await warte(600);
  await messe(von, bis);
  await seite.locator("#zirkel-hof .uebernehmen").click(); await warte(400);
}
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), standRhythmus);
await neuLaden(); await warte(1200);
ok("R1: Ausgang vor der Anamnese-Übergabe: Herr Baum sitzt noch da", (await feld("herrk").count()) === 1);
await zirkel("RR-Abstand", wahrheit.r1, wahrheit.r2);
ok("R1: nach der zweiten Karte der Hinweis auf Marlene", /Marlene/.test(await letzteMeldung()), await letzteMeldung());
await feld("marlene").click(); await warte(450);
ok("R1: Bericht mit der Frequenz allein", await antworte("Ich hab gemessen"));
const warnung = await dialogLesen();
ok("R1: Marlene ruft Falk, warnt aber vor seiner Frage nach der Überleitung",
   /ruf den Falk/.test(warnung) && /Überleitung/.test(warnung), warnung.slice(-90));
await endeKnopf();
await seite.locator(".dialog-antwort.weiter").click(); await warte(350);        /* Erzähler → Falk */
ok("R1: ohne PQ gibt es nur die halbe Antwort",
   (await seite.locator(".dialog-antwort", { hasText: "Sinusrhythmus," }).count()) === 0 && await antworte("Der Puls ist langsam"));
ok("R1: Falk fragt nach der Überleitung", /Vorhof bis zur Kammer/.test(await dialogLesen()));
await antworte("nicht gemessen");
const zurueck = await dialogLesen();
ok("R1: Falk schickt zum Wagen zurück — kein Ende, kein Monitor", /Wagen/.test(zurueck) && !/Monitor/.test(zurueck), zurueck.slice(0, 90));
await dialogDurch();
ok("R1: kein Fallende ohne beide Zahlen", !(await fallHat("fall_ende")) && await fallHat("falk_schickt_zurueck"));
await schuss("rueckweg_falk");
await seite.locator("#buehne .felder polygon.ausgang").first().click(); await warte(300);
ok("R1: der Flur bleibt zu, die Meldung nennt Dr. Falk", await seite.evaluate(() => window.Szene.aktueller() === "aufnahme") && /Falk/.test(await letzteMeldung()), await letzteMeldung());
st = await standLesen();
ok("R1: Stand nennt beide Zahlen und den Tresen", /zwei Zahlen/.test(st.offen) && /Tresen/.test(st.offen), st.offen.slice(0, 160));
await standZu();
await feld("marlene").click(); await warte(450);
ok("R1: Marlene weiß, dass Falk wartet, und bietet den Weg zu ihm", /Falk/.test(await dialogLesen()) && (await antworten()).some((t) => /Zu Dr\. Falk/.test(t)));
await antworte("Später");
await zirkel("PQ-Zeit", wahrheit.p0, wahrheit.q0);
ok("R1: nach der fehlenden Zahl der Hinweis auf Falk", /Falk/.test(await letzteMeldung()), await letzteMeldung());
await feld("marlene").click(); await warte(450);
await antworte("Zu Dr. Falk"); await warte(400);
ok("R1: Falk beim Wiederkommen: „Haben Sie, was fehlt?“", /Haben Sie, was fehlt/.test(await dialogLesen()));
ok("R1: jetzt die ganze Antwort", await antworte("Sinusrhythmus,"));
await antworte("Bisoprolol");
await antworte("Nach Hause");
await dialogDurch(); await warte(400); await dialogDurch();
ok("R1: Übergabe mit beiden Zahlen → Ende des Falls, Flur offen", await fallHat("fall_ende") && (await feld("herrk").count()) === 0);

/* Nur die PQ-Zeit: Falk fragt nach der Frequenz. */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), standRhythmus);
await neuLaden(); await warte(1200);
await zirkel("PQ-Zeit", wahrheit.p0, wahrheit.q0);
await feld("marlene").click(); await warte(450);
await antworte("Ich hab gemessen");
const berichtPq = await dialogLesen();
ok("R2: Marlene mit PQ ohne Frequenz mahnt die Frequenz an", /Miss die Frequenz/.test(berichtPq), berichtPq.slice(-90));
await endeKnopf();
await seite.locator(".dialog-antwort.weiter").click(); await warte(350);
ok("R2: mit der PQ-Zeit allein lässt sich die Zahl nennen", await antworte("Sinusrhythmus, PQ"));
ok("R2: Falk fragt nach der Frequenz", /wie langsam/.test(await dialogLesen()));
await antworte("Hol ich nach");
await dialogDurch();
ok("R2: zurück zum Wagen, kein Ende", !(await fallHat("fall_ende")));

/* Medikamente nie gefragt: Falk schickt zum Patienten, nicht zur Tüte. */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), standBogen);
await neuLaden(); await warte(1200);
await feld("herrk").click(); await warte(450);
await antworte("was passiert ist"); await antworte("Zurück"); await antworte("untersuchen"); await dialogDurch(); await warte(300);
await seite.keyboard.press("Enter"); await warte(300);
ok("R3: Wagen frei mit Ereignis und Untersuchung, ohne Medikamente", !(await seite.evaluate(() => window.Mappe.hat("b-medis"))));
await wagen.click(); await warte(500);
await seite.locator("#frage-hof .wahl", { hasText: "Sinusrhythmus" }).click(); await warte(300);
await seite.locator("#frage-hof .weiter").click(); await warte(400);
await zirkel("RR-Abstand", wahrheit.r1, wahrheit.r2);
await zirkel("PQ-Zeit", wahrheit.p0, wahrheit.q0);
st = await standLesen();
ok("R3: Stand mahnt die Medikamente als Pflichtfrage, nicht die Tüte", /Medikamente/.test(st.offen) && !/Tüte/.test(st.offen), st.offen.slice(0, 160));
await standZu();
await feld("marlene").click(); await warte(450);
await antworte("Ich hab gemessen"); await endeKnopf();
await seite.locator(".dialog-antwort.weiter").click(); await warte(350);
await antworte("Sinusrhythmus,");
ok("R3: ohne Medikationsplan nur „Das weiß ich nicht“", (await seite.locator(".dialog-antwort", { hasText: "Bisoprolol" }).count()) === 0 && await antworte("Das weiß ich nicht"));
const halbe = await dialogLesen();
ok("R3: Falk schickt zum Patienten (drei Meter), nicht in eine Tüte", /Fragen Sie ihn/.test(halbe) && /drei Meter/.test(halbe) && !/Tüte|Aufnahmebogen/.test(halbe), halbe);
await dialogDurch();
st = await standLesen();
ok("R3: Stand: Dr. Falk will wissen, was Herr Baum einnimmt", /Falk will wissen/.test(st.offen), st.offen.slice(0, 160));
await standZu();
await feld("herrk").click(); await warte(450);
await antworte("Medikamente");
ok("R3: Medikationsplan jetzt in der Mappe, Hinweis auf Falk", await seite.evaluate(() => window.Mappe.hat("b-medis")) && /Falk/.test(await letzteMeldung()));
await antworte("Zurück"); await antworte("gleich wieder");
await feld("marlene").click(); await warte(450);
await antworte("Zu Dr. Falk"); await warte(400);
await antworte("Sinusrhythmus,");
ok("R3: jetzt Bisoprolol", await antworte("Bisoprolol") && /Tabletten die Zahlen/.test(await dialogLesen()));
await antworte("Nach Hause"); await dialogDurch(); await warte(400); await dialogDurch();
ok("R3: Ende des Falls auch auf diesem Weg", await fallHat("fall_ende"));

/* ------------------------------------------------- 15 Rätsel „Reizleitung bauen" (Modul; wandert in den Lehrsaal)
   Das Rätsel hängt nicht mehr an Marlene (Entscheidung: Lehrsaal, KONZEPT §7). Es bleibt gebaut und geprüft — hier
   direkt gestartet, damit nichts davon leise kaputtgeht. */
await seite.evaluate(() => { window.localStorage.clear(); });
await neuLaden(); await warte(1200); await dialogDurch();
await seite.evaluate(() => window.Reizleitung.starte({ satz: window.Spiel.satz,
  anmerkungen: { 39: "Den kennst du: Das ist der Streifen von Herrn Baum. Sein AV-Knoten sitzt am richtigen Platz, er leitet nur langsamer." },
  fertig: function () { window.__rlFertig = true; } }));
await warte(500);
const rl = (sel) => seite.locator("#reizleitung-hof " + sel);
ok("Reizleitung offen", await seite.locator("#reizleitung-hof.an").isVisible());
ok("Herzschema aus kunst.json", (await rl(".rl-herz svg.schema-herz").count()) === 1);
ok("Kein Text im Herzbild", (await rl("svg.schema-herz text").count()) === 0);
ok("Fünf Bauteile, sieben Plätze",
   (await rl(".rl-teil").count()) === 5 && (await rl(".rl-platz").count()) === 7);
const kleinste = await seite.evaluate(() => {
  const hof = document.getElementById("reizleitung-hof");
  const masse = [...hof.querySelectorAll("button:not([hidden]), .rl-platz .rl-treffer")].map((e) => {
    const r = e.getBoundingClientRect(); return Math.min(r.width, r.height);
  });
  return Math.round(Math.min(...masse));
});
ok("Alles Antippbare mindestens 44 px", kleinste >= 44, kleinste + " px");
const tabelle = await seite.evaluate(() => window.Reizleitung.__pruefeTabelle());
ok("Fall-Tabelle passt zu den Daten (Rhythmus, PQ, QRS je Aufnahme)",
   tabelle.length >= 5 && tabelle.every((z) => z.da && z.passt),
   tabelle.map((z) => z.fall + ":" + z.aufnahme + (z.passt ? "" : "!")).join(" "));
ok("Jede Zeile der Fall-Tabelle nennt ihre Lehrbuchlektion (im Code, nicht im Spieltext)",
   await seite.evaluate(() => Object.keys(window.Reizleitung.FAELLE).every((k) => typeof window.Reizleitung.FAELLE[k].lektion === "string")));
/* Lehrbuch Lektion 1 und 14: der linke Schenkel teilt sich in zwei Faszikel — rechts, Stamm, hinten, vorn. */
const bahnen = await seite.evaluate(() => window.KUNST.schemata.herz_geo.teile.schenkel.bahnen.length);
ok("Herzschema: linker Schenkel in zwei Faszikel geteilt (vier Schenkelbahnen)", bahnen === 4, String(bahnen));
await schuss("reizleitung_leer");

/* Setzt ein Bauteil (Ziffer oder Antippen) und wartet, bis Welle und Streifen durch sind. */
async function setzeTeil(teil, platz, mitTaste) {
  if (mitTaste) await seite.keyboard.press(String(["sinus", "av", "his", "schenkel", "purkinje"].indexOf(teil) + 1));
  else await rl(`.rl-teil[data-teil="${teil}"]`).click();
  await rl(`.rl-platz[data-platz="${platz}"]`).click();
  await seite.waitForSelector('#reizleitung-hof .rl-herz[data-bereit="ja"]', { timeout: 15000 });
  await warte(200);
  return seite.evaluate(() => {
    const hof = document.getElementById("reizleitung-hof"), z = window.Reizleitung.zustand();
    const sp = hof.__streifen && hof.__streifen.stand.zirkel;
    return { fall: z.fall, aufnahme: z.aufnahme,
             ms: sp ? Math.round((sp.ende - sp.start) * 1000) : null,
             unter: hof.querySelector(".rl-unterschrift").textContent,
             rueck: hof.querySelector(".rl-rueck").textContent,
             streifen: !hof.querySelector(".rl-streifen").classList.contains("ohne") };
  });
}

/* Richtiger Aufbau, Schritt für Schritt — jeder Zwischenstand hat seine eigene echte Kurve. */
let rlSt = await setzeTeil("sinus", "sinus", true);
ok("Nur Sinusknoten: kompletter Block, Schrittmacher-Aufnahme 74",
   rlSt.fall === "block" && rlSt.aufnahme === 74 && /AV-Block III/.test(rlSt.rueck), rlSt.fall + "/" + rlSt.aufnahme);
ok("Block: Ersatzfrequenzen nach Lage des Blocks (40–60 schmal, 30–40 breit) und Schrittmacher benannt",
   /40–60/.test(rlSt.rueck) && /30–40/.test(rlSt.rueck) && /Schrittmacher/.test(rlSt.rueck) && /schenkelblockartig/.test(rlSt.rueck));
rlSt = await setzeTeil("av", "av", true);
ok("Ohne His-Bündel weiterhin Block", rlSt.fall === "block" && rlSt.aufnahme === 74, rlSt.fall + "/" + rlSt.aufnahme);
rlSt = await setzeTeil("his", "his");
ok("Ohne Schenkel: breiter QRS, Aufnahme 24 (Linksschenkelblock)",
   rlSt.fall === "schenkel" && rlSt.aufnahme === 24 && rlSt.ms >= 120 && /Linksschenkelblock/.test(rlSt.unter),
   rlSt.fall + "/" + rlSt.aufnahme + "/" + rlSt.ms + " ms");
/* Die Datenbank nennt Nr. 24 „Sinusbradykardie“ (51/min); das Spiel ordnet das Etikett an seiner Grenze (50) ein. */
ok("Datenbank-Etikett „Sinusbradykardie“ bei 51/min wird eingeordnet, nicht übernommen",
   /Sinusbradykardie/.test(rlSt.unter) && /unter 50/.test(rlSt.rueck) && /nicht zum Modell/.test(rlSt.rueck), rlSt.rueck.slice(-140));
await schuss("reizleitung_ohne_schenkel");
rlSt = await setzeTeil("schenkel", "schenkel");
ok("Ohne Purkinje: nächstliegende Aufnahme 59, ehrlich benannt",
   rlSt.fall === "purkinje" && rlSt.aufnahme === 59 && /Am nächsten kommt/.test(rlSt.rueck), rlSt.fall + "/" + rlSt.aufnahme);
rlSt = await setzeTeil("purkinje", "purkinje");
ok("Vollständig und richtig: Sinusrhythmus, Aufnahme 119",
   rlSt.fall === "richtig" && rlSt.aufnahme === 119 && /LUDB Nr\. 119/.test(rlSt.unter) && /Sinusrhythmus/.test(rlSt.unter),
   rlSt.unter.slice(0, 90));
ok("Markierte PQ-Zeit im Normbereich", rlSt.ms >= 120 && rlSt.ms <= 200, rlSt.ms + " ms");
ok("Lernziel im Text: richtige Anatomie, normales EKG", /Richtige Anatomie, normales EKG/.test(rlSt.rueck));
ok("Kein Lehrbuchverweis im Spieltext (Lektionsnummern bleiben in Code und docs)", !/Lektion/.test(rlSt.rueck), rlSt.rueck.slice(0, 80));
ok("Alle vier Schenkelbahnen gezeichnet (rechts, Stamm, zwei Faszikel)",
   (await rl('.rl-teil-bild[data-teil="schenkel"] path.rl-strang').count()) === 4);
ok("Abschluss-Knopf erscheint", await rl(".rl-fertig").isVisible());
await schuss("reizleitung_richtig");

/* Fehlaufbau 1: AV-Knoten in den linken Vorhof — PQ über 200 ms (Herrn Baums Streifen). */
rlSt = await setzeTeil("av", "linker_vorhof");
ok("AV-Knoten falsch: PQ > 200 ms, Aufnahme 39",
   rlSt.fall === "av_umweg" && rlSt.aufnahme === 39 && rlSt.ms > 200 && /PQ über 200 ms/.test(rlSt.rueck),
   rlSt.fall + "/" + rlSt.aufnahme + "/" + rlSt.ms + " ms");
ok("Rückmeldung sagt, warum (und was im echten Herzen passiert)",
   /Umweg/.test(rlSt.rueck) && /AV-Block I\. Grades/.test(rlSt.rueck) && /Herrn Baum/.test(rlSt.rueck));
await schuss("reizleitung_av_falsch");
await setzeTeil("av", "av");

/* Fehlaufbau 2: Sinusknoten heraus — Knotenersatzrhythmus (Lektion 11), keine annotierte Aufnahme, kein Streifen. */
await rl('.rl-teil[data-teil="sinus"]').click();
await rl(".rl-raus").click();
await seite.waitForSelector('#reizleitung-hof .rl-herz[data-bereit="ja"]', { timeout: 15000 });
rlSt = await seite.evaluate(() => ({ ...window.Reizleitung.zustand(),
  rueck: document.querySelector("#reizleitung-hof .rl-rueck").textContent,
  unter: document.querySelector("#reizleitung-hof .rl-unterschrift").textContent }));
ok("Ohne Sinusknoten: Ersatzzentrum im AV-Übergang, kein Streifen (Lektion 11)",
   rlSt.fall === "ohne_sinus" && rlSt.aufnahme === null && /Ersatz/.test(rlSt.rueck) && /kein Streifen/.test(rlSt.rueck),
   rlSt.fall + "/" + rlSt.aufnahme);
await schuss("reizleitung_ohne_sinus");
await setzeTeil("sinus", "sinus");

/* Fehlaufbau 3: Schenkel auf den Klappenring — breiter QRS. */
rlSt = await setzeTeil("schenkel", "klappenring");
ok("Schenkel falsch: QRS > 120 ms, Aufnahme 24", rlSt.fall === "schenkel" && rlSt.aufnahme === 24 && rlSt.ms > 120,
   rlSt.fall + "/" + rlSt.aufnahme + "/" + rlSt.ms + " ms");

await seite.keyboard.press("Escape");
await warte(300);
ok("Escape schließt das Rätsel", (await seite.locator("#reizleitung-hof.an").count()) === 0);
ok("Bühne danach wieder bedienbar",
   await seite.evaluate(() => !document.getElementById("buehne").classList.contains("stumm")));

/* ------------------------------------------------- 16 Vollbild-Bühne: mehrere Größen, Hochformat
   Je Größe ein frischer Browserkontext (eigener Speicher): Titel, „Neues Spiel“, dann messen. Die Bühne ist das
   größte 16:9-Rechteck im Fenster, mittig; der Rest ist Tinte. Abweichung höchstens 1 px. */
async function frischeSeite(b, h, sprache = "de", stand = null, dpr = 1) {
  const ctx = await browser.newContext({ viewport: { width: b, height: h }, deviceScaleFactor: dpr });
  const p = await ctx.newPage();
  const tag = b + "×" + h + (sprache !== "de" ? " " + sprache : "") + (dpr !== 1 ? " @" + dpr + "x" : "");
  p.on("console", (m) => { if (m.type() === "error") fehler.push("Konsole (" + tag + "): " + m.text().slice(0, 160)); });
  p.on("pageerror", (e) => fehler.push("Seitenfehler (" + tag + "): " + String(e).slice(0, 200)));
  await p.addInitScript(({ sp, st }) => { try {
    window.localStorage.setItem("nachtdienst-sprache", sp);
    if (st) window.localStorage.setItem("nachtdienst-1", st);
  } catch (e) {} }, { sp: sprache, st: stand });
  await p.goto("file://" + DATEI);
  await p.waitForTimeout(600);
  return { ctx, p, tag };
}
for (const [b, h] of [[1340, 900], [1024, 768], [1366, 1024], [1920, 1080]]) {
  const { ctx, p, tag } = await frischeSeite(b, h);
  ok(tag + ": Titelbildschirm, kein Hochformat-Hinweis",
     await p.locator("#titel").isVisible() && !(await p.locator("#quer-hinweis").isVisible()));
  const bildT = await p.evaluate(() => { const r = document.querySelector("#titel .titel-bild").getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; });
  await p.locator("#titel-neu").click();
  await p.waitForTimeout(900);
  const m = await p.evaluate(() => {
    const r = document.getElementById("buehne").getBoundingClientRect();
    const e = document.scrollingElement;
    const knoepfe = [...document.querySelectorAll("#hud button")].map((k) => { const q = k.getBoundingClientRect();
      return Math.min(q.width, q.height) >= 44 && q.left >= r.left && q.right <= r.right && q.top >= r.top && q.bottom <= r.bottom; });
    return { l: r.left, t: r.top, w: r.width, h: r.height, sw: e.scrollWidth, sh: e.scrollHeight,
             grund: getComputedStyle(document.body).backgroundColor, html: getComputedStyle(document.documentElement).backgroundColor,
             rand: getComputedStyle(document.getElementById("buehne")).borderTopWidth, knoepfe };
  });
  const sollB = Math.min(b, h * 16 / 9), sollH = Math.min(h, b * 9 / 16);
  const nah = (x, y) => Math.abs(x - y) <= 1;
  ok(tag + ": Bühne füllt das Fenster in 16:9, Letterbox mittig (≤ 1 px)",
     nah(m.w, sollB) && nah(m.h, sollH) && nah(m.l, (b - sollB) / 2) && nah(m.t, (h - sollH) / 2) && (nah(m.w, b) || nah(m.h, h)),
     [m.l, m.t, m.w, m.h].map((x) => Math.round(x * 10) / 10).join(", ") + " soll " + [sollB, sollH].map(Math.round).join("×"));
  ok(tag + ": Titelbild liegt genau auf der Bühne",
     nah(bildT[0], m.l) && nah(bildT[1], m.t) && nah(bildT[2], m.w) && nah(bildT[3], m.h), bildT.map(Math.round).join(","));
  ok(tag + ": kein Scrollen", m.sw <= b && m.sh <= h, m.sw + "×" + m.sh);
  ok(tag + ": Letterbox in Tinte #1E2A30, kein Bühnenrahmen",
     m.grund === "rgb(30, 42, 48)" && m.html === "rgb(30, 42, 48)" && m.rand === "0px", m.grund + " / " + m.rand);
  ok(tag + ": HUD-Knöpfe ≥ 44 px, über der Bühne", m.knoepfe.length === 4 && m.knoepfe.every(Boolean), JSON.stringify(m.knoepfe));
  const resteP = await p.evaluate(() => [...document.body.children].filter((e) => e.tagName !== "SCRIPT" && e.id !== "flaeche" &&
    getComputedStyle(e).display !== "none" && e.getBoundingClientRect().height > 0 &&
    !e.classList.contains("dialog") && !e.classList.contains("meldungen") && !e.classList.contains("szenenbild")).map((e) => e.id || e.className));
  ok(tag + ": außer der Bühne nichts sichtbar (keine Fuß- oder Seitenleiste)", !resteP.length, resteP.join(", "));
  if (b === 1366) {
    await dialogDurch(8, p);
    await p.waitForTimeout(2600);
    await p.screenshot({ path: `${BILDER}/ipad_quer.png` });
    /* Das Szenenbild deckt genau die Bühne — auch auf dem iPad-Maß. */
    await p.locator('.feld[data-feld="marlene"]').click();
    await p.waitForTimeout(1000);
    const sb = await p.evaluate(() => { const s = document.querySelector(".szenenbild.an"), b = document.getElementById("buehne").getBoundingClientRect();
      if (!s) return null; const r = s.getBoundingClientRect(); return [r.left - b.left, r.top - b.top, r.width - b.width, r.height - b.height].map(Math.round); });
    ok(tag + ": Szenenbild deckt genau die Bühne", !!sb && sb.every((x) => Math.abs(x) <= 1), JSON.stringify(sb));
    await p.screenshot({ path: `${BILDER}/ipad_szenenbild.png` });
  }
  await ctx.close();
}
{
  const { ctx, p, tag } = await frischeSeite(768, 1024);
  const quer = p.locator("#quer-hinweis");
  ok(tag + " (Hochformat): ruhiger Hinweis „Bitte quer halten“ mit Symbol",
     await quer.isVisible() && /Bitte quer halten/.test((await quer.textContent()) || "") &&
     (await p.locator("#quer-hinweis svg").count()) === 1 && !(await ohneBlinken("#quer-hinweis", p)).length);
  await p.screenshot({ path: `${BILDER}/hochformat.png` });
  await p.setViewportSize({ width: 1024, height: 768 });
  await p.waitForTimeout(300);
  ok("Gedreht auf 1024×768: Hinweis weg, Titel da", !(await quer.isVisible()) && await p.locator("#titel").isVisible());
  await ctx.close();
}

/* ------------------------------------------------- 17 Textüberlauf: de/en/ru bei 1024×768 und 1366×1024
   Kein Text in Knöpfen, Dialogantworten, HUD, Menü, Stand oder Fenstern über seinen Kasten; die Dialogkarte
   bleibt im Fenster. Gemessen wird scrollWidth/scrollHeight gegen clientWidth/clientHeight (abgeschnitten)
   und die Lage der Kästen gegen den Fensterrand. */
const ueberlauf = (p, wo) => p.evaluate((wo) => {
  const aus = [], vw = window.innerWidth, vh = window.innerHeight;
  const sichtbar = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden"; };
  const sel = "button, .dialog-antwort, .dialog-text, .dialog-name, .hud-uhr, .hud-zeit, .hud-ort, .stand-liste li, .stand-zeile, " +
              ".raetsel-kopf h2, .raetsel-auftrag, .rueck, .befund-zeilen li, .karte h3, .karte p, .menue-ort, .schalter, .huelle-kopf h2";
  document.querySelectorAll(sel).forEach((e) => {
    if (!sichtbar(e)) return;
    if (e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1)
      aus.push(wo + ": " + (e.className || e.tagName) + " „" + (e.textContent || "").trim().slice(0, 30) + "“ " +
               e.scrollWidth + ">" + e.clientWidth + " / " + e.scrollHeight + ">" + e.clientHeight);
  });
  document.querySelectorAll(".dialog-innen, .raetsel-innen, .huelle-karte, #hud").forEach((e) => {
    if (!sichtbar(e)) return;
    const r = e.getBoundingClientRect();
    if (r.left < -1 || r.top < -1 || r.right > vw + 1 || r.bottom > vh + 1)
      aus.push(wo + ": Kasten " + (e.className || e.id) + " ragt aus dem Fenster (" + [r.left, r.top, r.right, r.bottom].map(Math.round).join(",") + ")");
  });
  /* HUD: linke und rechte Gruppe dürfen sich nicht überlappen */
  const g = document.querySelectorAll("#hud .hud-gruppe");
  if (g.length === 2) { const a = g[0].getBoundingClientRect(), b = g[1].getBoundingClientRect(); if (a.right > b.left) aus.push(wo + ": HUD-Gruppen überlappen"); }
  return aus;
}, wo);
for (const sprache of ["de", "en", "ru"]) {
  for (const [b, h] of [[1024, 768], [1366, 1024]]) {
    const { ctx, p, tag } = await frischeSeite(b, h, sprache, standMappe);
    const funde = [];
    await vomTitel(p); await p.waitForTimeout(1000);
    funde.push(...await ueberlauf(p, "HUD"));
    await p.locator("#hud-menue").click(); await p.waitForTimeout(250);
    funde.push(...await ueberlauf(p, "Menü"));
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);
    await p.locator("#hud-stand").click(); await p.waitForTimeout(300);
    funde.push(...await ueberlauf(p, "Stand"));
    await p.locator("#stand-hof .zu").click(); await p.waitForTimeout(200);
    await p.locator("#hud-mappe").click(); await p.waitForTimeout(500);
    funde.push(...await ueberlauf(p, "Mappe"));
    await p.locator(".mappe .zu").click(); await p.waitForTimeout(200);
    /* Herr Baum: das längste Antwortmenü (sechs Zeilen) */
    await p.locator('.feld[data-feld="herrk"]').click(); await p.waitForTimeout(400);
    await p.locator(".dialog-text").click(); await p.waitForTimeout(150);
    funde.push(...await ueberlauf(p, "Dialog Herr Baum"));
    const nAntw = await p.locator(".dialog-antwort").count();
    if (sprache === "de" && b === 1024) await p.screenshot({ path: `${BILDER}/ueberlauf_herrk_${b}.png` });
    await p.locator(".dialog-antwort").last().click(); await p.waitForTimeout(300);
    /* Marlene: Bericht mit Zahlen, dann Dr. Falk mit den langen Zahlenantworten */
    await p.locator('.feld[data-feld="marlene"]').click(); await p.waitForTimeout(400);
    await p.locator(".dialog-text").click(); await p.waitForTimeout(150);
    funde.push(...await ueberlauf(p, "Dialog Marlene"));
    await p.locator(".dialog-antwort").first().click(); await p.waitForTimeout(300);
    await p.locator(".dialog-text").click(); await p.waitForTimeout(150);
    funde.push(...await ueberlauf(p, "Dialog Marlene Bericht"));
    await dialogDurch(2, p); await p.waitForTimeout(400);
    if (await p.locator(".dialog-antwort.weiter").count()) { await p.locator(".dialog-antwort.weiter").click(); await p.waitForTimeout(350); }
    await p.locator(".dialog-text").click(); await p.waitForTimeout(150);
    funde.push(...await ueberlauf(p, "Dialog Falk"));
    if (b === 1024) await p.screenshot({ path: `${BILDER}/ueberlauf_falk_${sprache}_${b}.png` });
    await p.locator(".dialog-antwort").last().click(); await p.waitForTimeout(300);     /* Umweg Anamnese */
    await p.locator(".dialog-antwort").first().click(); await p.waitForTimeout(300);
    await p.locator(".dialog-text").click(); await p.waitForTimeout(150);
    funde.push(...await ueberlauf(p, "Dialog Falk gut"));
    await p.locator(".dialog-antwort").first().click(); await p.waitForTimeout(300);
    await p.locator(".dialog-text").click(); await p.waitForTimeout(150);
    funde.push(...await ueberlauf(p, "Dialog Falk Tabletten"));
    /* Fenster: Messwahl, Zirkel (Knöpfe), Frage */
    await p.locator(".dialog-antwort").first().click(); await p.waitForTimeout(300);
    await dialogDurch(3, p);
    while (await p.locator(".dialog.an").count()) { await p.locator(".dialog-text").click(); await p.waitForTimeout(120);
      const a = p.locator(".dialog-antwort"); if (await a.count()) { await a.last().click(); await p.waitForTimeout(250); } else break; }
    await p.locator('.feld[data-feld="wagen"]').click(); await p.waitForTimeout(400);
    funde.push(...await ueberlauf(p, "Messwahl"));
    await p.locator("#wahl-hof .wahl").first().click(); await p.waitForTimeout(500);
    funde.push(...await ueberlauf(p, "Zirkel"));
    await p.locator("#zirkel-hof .loesung").click(); await p.waitForTimeout(200);
    funde.push(...await ueberlauf(p, "Zirkel Lösung"));
    await p.locator("#zirkel-hof .zu").click(); await p.waitForTimeout(200);
    ok(tag + ": kein Textüberlauf in HUD, Menü, Stand, Mappe, Dialogen und Fenstern (" + nAntw + " Antworten im längsten Menü)",
       !funde.length, funde.slice(0, 4).join(" | "));
    await ctx.close();
  }
}

/* ------------------------------------------------- 18 Zirkel maßstabstreu: 1024×768, 1366×1024, 1920×1080 (Retina, 2×)
   Dieselbe Strecke (PQ bzw. RR, aus der Annotation) ergibt auf jedem Bildschirm dieselben Millisekunden (±2 ms)
   und dieselbe Bewertung. Gemessen mit Zeigerereignissen auf Bruchteile von Pixeln (so weiß man, dass Maßstab
   und Rückrechnung stimmen) und mit der echten Maus (Bewertung). Das Fenster ist auf 1100 px gedeckelt, deshalb
   teilen sich 1366 und 1920 die Leinwandbreite; der dritte Maßstab kommt bei 1920 über das Gerätepixelverhältnis 2. */
const zirkelMessung = async (p, aufgabe, von, bis) => {
  await p.locator('.feld[data-feld="wagen"]').click(); await p.waitForTimeout(400);
  await p.locator("#wahl-hof .wahl", { hasText: aufgabe }).click(); await p.waitForTimeout(600);
  const fein = await p.evaluate(({ von, bis }) => {
    const hof = document.getElementById("zirkel-hof"), lw = hof.querySelector("canvas"), s = hof.__streifen;
    const r = lw.getBoundingClientRect(), y = r.top + r.height / 2;
    const ev = (typ, x) => lw.dispatchEvent(new PointerEvent(typ, { clientX: x, clientY: y, pointerId: 1, isPrimary: true, bubbles: true, cancelable: true, pointerType: "mouse" }));
    ev("pointerdown", r.left + s.sekundeZuX(von));
    ev("pointermove", r.left + s.sekundeZuX((von + bis) / 2));
    ev("pointermove", r.left + s.sekundeZuX(bis));
    ev("pointerup", r.left + s.sekundeZuX(bis));
    return { ms: +hof.querySelector(".wert").textContent, gut: hof.querySelector(".rueck").classList.contains("gut"),
             pxProMm: Math.round(s.sekundeZuX(1) - s.sekundeZuX(0)) / s.stand.mmProS, breite: Math.round(r.width),
             dpr: window.devicePixelRatio, backing: lw.width };
  }, { von, bis });
  await p.locator("#zirkel-hof .nochmal").click(); await p.waitForTimeout(200);
  await messe(von, bis, p);
  const maus = await p.evaluate(() => { const hof = document.getElementById("zirkel-hof");
    return { ms: +hof.querySelector(".wert").textContent, gut: hof.querySelector(".rueck").classList.contains("gut") }; });
  await p.locator("#zirkel-hof .zu").click(); await p.waitForTimeout(200);
  return { fein, maus };
};
const massstab = {};
for (const [b, h, dpr] of [[1024, 768, 1], [1366, 1024, 1], [1920, 1080, 2]]) {
  const { ctx, p, tag } = await frischeSeite(b, h, "de", standRhythmus, dpr);
  await vomTitel(p); await p.waitForTimeout(1000);
  massstab[tag] = { pq: await zirkelMessung(p, "PQ-Zeit", wahrheit.p0, wahrheit.q0), rr: await zirkelMessung(p, "RR-Abstand", wahrheit.r1, wahrheit.r2) };
  await ctx.close();
}
const tags = Object.keys(massstab);
for (const was of ["pq", "rr"]) {
  const werte = tags.map((t) => massstab[t][was].fein.ms), soll = Math.round(({ pq: wahrheit.q0 - wahrheit.p0, rr: wahrheit.r2 - wahrheit.r1 })[was] * 1000);
  ok("Zirkel maßstabstreu (" + was.toUpperCase() + "): " + tags.join(", ") + " ergeben dieselben Millisekunden (±2 ms) — und die der Annotation",
     werte.every((w) => Math.abs(w - werte[0]) <= 2 && Math.abs(w - soll) <= 2), werte.join("/") + " soll " + soll + " · px/mm " + tags.map((t) => massstab[t][was].fein.pxProMm.toFixed(2)).join("/"));
  ok("Zirkel maßstabstreu (" + was.toUpperCase() + "): dieselbe Bewertung auf allen drei Bildschirmen (fein und mit der Maus)",
     tags.every((t) => massstab[t][was].fein.gut && massstab[t][was].maus.gut), tags.map((t) => t + ":" + massstab[t][was].maus.ms + (massstab[t][was].maus.gut ? "✓" : "✗")).join(" "));
}
ok("Zirkel: drei verschiedene Maßstäbe geprüft (Leinwandbreite oder Gerätepixel verschieden, Retina mit doppeltem Speicher)",
   new Set(tags.map((t) => massstab[t].pq.fein.breite + "@" + massstab[t].pq.fein.dpr)).size === 3 &&
   tags.some((t) => massstab[t].pq.fein.dpr === 2 && massstab[t].pq.fein.backing === massstab[t].pq.fein.breite * 2),
   tags.map((t) => massstab[t].pq.fein.breite + "@" + massstab[t].pq.fein.dpr + "→" + massstab[t].pq.fein.backing).join(" / "));

await browser.close();

console.log(schritte.join("\n"));
console.log("\n" + (fehler.length ? "FEHLER (" + fehler.length + "):\n - " + fehler.join("\n - ")
                                  : "Alle Prüfungen bestanden."));
process.exit(fehler.length ? 1 : 0);
