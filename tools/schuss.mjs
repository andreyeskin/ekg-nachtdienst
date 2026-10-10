/* Ein Bildschirmfoto einer Datei: node tools/schuss.mjs <datei> <ziel.png> [breite] [hoehe] */
import { starteBrowser } from "./browser.mjs";
const [, , datei, ziel, breite, hoehe] = process.argv;
const b = await starteBrowser();
const p = await b.newPage({ viewport: { width: +(breite || 1340), height: +(hoehe || 900) }, deviceScaleFactor: 2 });
await p.goto(datei.startsWith("http") ? datei : "file://" + datei);
await p.waitForTimeout(600);
await p.screenshot({ path: ziel, fullPage: !hoehe });
await b.close();
console.log("geschrieben:", ziel);
