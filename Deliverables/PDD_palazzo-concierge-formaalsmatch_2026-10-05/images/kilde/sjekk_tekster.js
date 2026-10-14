// Holder det gjesten ser i rammene, mot korpuset og mot reglene i kontrakten.
// Skriptet ser det som står i tilstander.js: svarene i hvert steg, det skissen legger på,
// og hvilken merkelapp og hvilke advarsler rammen ender med. Det ser ikke pikslene i bildene.
// Bruk: node sjekk_tekster.js [<en annen tilstander.js>]
"use strict";
const fs = require("fs");
const path = require("path");
const { RAMMER, BILDER } = require(process.argv[2] ? path.resolve(process.argv[2]) : "./tilstander.js");
// Linjene om allergener, skrevet av fra koden på nett og ikke hentet fra filen som kontrolleres
// (PalazzoScaffold/Sources/App/Controllers/PalazzoCommunaleProjection.swift, linje 17–19). Den fjerde er ny i forslaget.
const LINJER = {
  enRett: "Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller.",
  flere: "Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller.",
  kort: "Spør personalet om allergener før du bestiller.",
  personal: "Merkingen dekker ikke spor eller krysskontakt. Si fra til personalet før du bestiller."
};
// Den ene rammen som viser sidens merkelapp med vilje (tilleggsbildet om merkelappen).
const MED_SIDENS_MERKELAPP = ["merkelapp-som-i-dag"];
const KORPUS = "/mnt/user-data/uploads/PalazzoScaffold/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json";
const K = JSON.parse(fs.readFileSync(KORPUS, "utf8"));
const ALG = Object.fromEntries(K.allergens.map((a) => [a.code, a.name_nb]));
const retter = K.menu_items, drikke = K.beverage_items;

const tall = {};
const si = (slag, ok, tekst) => {
  tall[slag] = tall[slag] || { sjekket: 0, feil: 0 };
  tall[slag].sjekket++;
  if (!ok) { tall[slag].feil++; console.log("FEIL [" + slag + "]:", tekst); }
};

// Ord conciergen ikke skal bruke om en rett. «sikker» fanger også «sikkert» og «sikkerhet».
const FORBUDT = [/\btryg[gt]/i, /\bsikker/i, /\bgarant/i, /\buten risiko\b/i, /\bufarlig/i];
const harForbudt = (t) => FORBUDT.some((m) => m.test(t));
// En påstand om at en rett er uten noe. «kan ikke si at … er uten …» er det motsatte, og er lov.
const UTEN = [/\ber uten\b/i, /\binneholder ikke\b/i, /\bfri for\b/i, /(gluten|laktose|nøtte|melke|egge?|allergen)fri/i];
const sierUten = (t) => t.split(/(?<=[.!?])\s+|\n+/).some((setning) => UTEN.some((m) => m.test(setning)) && !/kan ikke si at/i.test(setning));
// Et tilbud sagt med ord, uten knapper. «Jeg foreslår derfor ingen rett» og «foreslår helst andre retter» er ikke tilbud.
const TILBUD = [/\bVil du ha\b/, /\banbefaler\b/i, /\bprøv\b/i, /\bpasser (godt |fint )?(for|til) deg\b/i, /\bdu kan (ta|spise|velge|bestille)\b/i, /\bjeg foreslår (?!derfor ingen|helst andre)/i];
const harTilbud = (t) => TILBUD.some((m) => m.test(t));
const NAVN = retter.map((x) => x.name).concat(drikke.map((x) => x.name));

// Det sidens eget skript setter som merkelapp (palazzo-communale.js, linje 79 og 91–104).
const MERKELAPP = { high: "høy sikkerhet", medium: "middels sikkerhet", low: "lav sikkerhet" };
function sidensMerkelapp(k) {
  const kontrollert = k.status === "answered" && k.needs_human_review !== true && k.citations.length > 0 && String(k.last_verified || "").trim() !== "";
  return kontrollert ? (MERKELAPP[k.confidence] || "kontrollert") : "må bekreftes";
}
function synligMerkelapp(r) {
  const s = r.skisse;
  if (s.kind === "receipt" || s.kind === "ask-model" || s.kind === "strip-only" || s.hideBadge) return null;
  if (s.badge !== undefined) return s.badge;
  return sidensMerkelapp(r.steg[r.steg.length - 1].svar);
}
function skissetekster(s) {
  const ut = [];
  for (const n of ["understood", "note", "notedHelp", "modelMark", "modelNote", "badge", "eyebrow", "title", "intro", "keepLink", "question", "questionLabel"]) if (typeof s[n] === "string") ut.push([n, s[n]]);
  (s.actions || []).forEach((a) => ut.push(["knapp", a.label]));
  (s.noted || []).forEach((n) => ut.push(["notert", n.text]));
  if (s.keep) {
    ut.push(["behold", s.keep.title], ["behold", s.keep.text]);
    s.keep.items.forEach((i) => { ut.push(["behold", i.text]); if (i.small) ut.push(["behold", i.small]); });
    s.keep.actions.forEach((a) => ut.push(["behold-knapp", a.label]));
  }
  return ut;
}
const blokkMed = (svar, navn) => svar.split("\n\n").filter((b) => b.includes(navn));

for (const [navn, r] of Object.entries(RAMMER)) {
  const s = r.skisse;
  const synlige = r.steg.map((st) => st.svar.answer).filter((a) => a !== "…");
  const siste = r.steg[r.steg.length - 1].svar;
  const visesSvar = s.kind !== "strip-only" && siste.answer !== "…";

  // 1 Ordene: hvert svar i hvert steg, og alt skissen legger på.
  synlige.forEach((a, i) => si("ord i svar", !harForbudt(a), navn + ", svar " + (i + 1) + ": har et ord conciergen ikke skal bruke"));
  skissetekster(s).forEach(([hva, t]) => si("ord i det skissen legger på", !harForbudt(t), navn + ", " + hva + ": «" + t + "»"));

  // 2 Merkelappen rammen ender med. Rammen som viser sidens merkelapp med vilje, er unntatt og telles for seg.
  const merke = synligMerkelapp(r);
  if (MED_SIDENS_MERKELAPP.includes(navn)) si("merkelapp vist med vilje", s.viserSidensMerkelapp === true && merke !== null && /sikkerhet/.test(merke), navn + ": skulle vist sidens merkelapp, viser «" + merke + "»");
  else si("merkelapp", s.viserSidensMerkelapp !== true && (merke === null || !harForbudt(merke)), navn + ": merkelappen «" + merke + "» står på svaret" + (s.viserSidensMerkelapp ? " (unntaket gjelder bare " + MED_SIDENS_MERKELAPP.join(", ") + ")" : ""));

  for (const a of synlige) {
    // 2b Ingen påstand om at en rett er uten noe.
    si("ingen «er uten»", !sierUten(a), navn + ": et svar sier at noe er uten, ikke inneholder eller er fritt for noe");
    // 2c Hvert avsnitt med «Beskrivelse:» eller «Merket med:» begynner med et navn fra korpuset, og et tilbud nevner et.
    for (const b of a.split("\n\n")) {
      if (/Beskrivelse: |Merket med: /.test(b)) si("navn fra korpuset", retter.some((x) => b.startsWith(x.name)), navn + ": avsnittet begynner ikke med et rettnavn fra korpuset: «" + b.slice(0, 50) + "»");
      if (/^Vi har /.test(b) && /Vil du ha/.test(b)) si("navn fra korpuset", NAVN.some((x) => b.startsWith("Vi har " + x)), navn + ": tilbudet nevner ikke et navn fra korpuset: «" + b.slice(0, 50) + "»");
      if (/ \((hovedrett|dessert|forrett|pastarett|pizza)\): /.test(b)) si("navn fra korpuset", retter.some((x) => b.startsWith(x.name + " (")), navn + ": avsnittet begynner ikke med et rettnavn fra korpuset: «" + b.slice(0, 50) + "»");
    }
    // 3 Beskrivelsene og merkingen, rett for rett, i samme avsnitt som navnet.
    for (const rett of retter) {
      if (!a.includes(rett.name)) continue;
      const blokker = blokkMed(a, rett.name);
      const bareNavn = /^Notert: du vil ha /.test(a);
      const ordrett = blokker.some((b) => b.includes(rett.name + ": " + rett.description_nb) || b.includes("Beskrivelse: " + rett.description_nb) || b.includes(rett.name + " (hovedrett): " + rett.description_nb) || b.includes(rett.name + " (dessert): " + rett.description_nb));
      si("beskrivelse ordrett fra korpuset", ordrett || bareNavn, navn + ": «" + rett.name + "» står uten beskrivelsen ordrett i samme avsnitt");
      for (const b of blokker) {
        const mm = b.match(/Merket med: ([^\n]*)\./);
        if (!mm) continue;
        const venter = rett.allergen_codes.map((c) => ALG[c]).join(", ");
        si("merking lik korpuset", mm[1] === venter, navn + ": merkingen for «" + rett.name + "» er «" + mm[1] + "», korpuset sier «" + venter + "»");
        const sierUbekreftet = /merkingen er ikke bekreftet/.test(b);
        si("bekreftet eller ikke, som i korpuset", sierUbekreftet === (rett.human_verified_allergens !== true), navn + ": «" + rett.name + "»: svaret og korpuset er uenige om merkingen er bekreftet");
      }
    }
    // 4 Drikke som nevnes, er uten alkohol.
    for (const d of drikke) if (a.includes(d.name)) si("drikke uten alkohol", d.category === "non_alcoholic", navn + ": drikken «" + d.name + "» er ikke uten alkohol i korpuset");
  }

  // 5 Linjen om allergener: en ramme som ender med et svar som nevner en rett eller en drikk,
  //   viser den, og i den formen koden på nett bruker (én rett, flere, eller uten beskrivelse).
  if (visesSvar) {
    const a = siste.answer;
    const nevnte = retter.filter((x) => a.includes(x.name));
    const nevnteDrikke = drikke.filter((x) => a.includes(x.name));
    if (nevnte.length + nevnteDrikke.length > 0) {
      const medBeskrivelse = nevnte.filter((x) => a.includes(x.description_nb)).length;
      const w = siste.warnings || [];
      let ventet;
      if (w.includes(LINJER.personal)) ventet = LINJER.personal;          // listene etter «tåler ikke»
      else if (medBeskrivelse === 1) ventet = LINJER.enRett;
      else if (medBeskrivelse > 1) ventet = LINJER.flere;
      else ventet = LINJER.kort;
      si("linjen om allergener vises", s.hideWarning !== true && w[0] === ventet, navn + ": venter «" + ventet + "» først blant advarslene, og at de vises. Har: " + JSON.stringify(w) + (s.hideWarning ? " (skjult)" : ""));
    }
  }

  // 5b «Liker ikke» trekker ned, det stenger ikke (F5): kvitteringen lover ikke å holde noe ute.
  r.steg.forEach((st) => {
    if (/liker ikke/i.test(st.si || "") && /^Notert:/.test(st.svar.answer)) {
      si("«liker ikke» stenger ikke", !/foreslår (jeg )?ikke|tilbyr (jeg )?ikke|ingen retter/i.test(st.svar.answer), navn + ": kvitteringen lover å holde retter ute: «" + st.svar.answer + "»");
    }
  });

  // 6 Regel 2: etter «tåler ikke» tilbys ingen rett.
  const taalerIkke = (s.noted || []).some((n) => /^tåler ikke /.test(n.text)) || r.steg.some((st) => /tåler ikke/i.test(st.si || ""));
  if (taalerIkke) {
    si("ingen tilbud etter «tåler ikke»", s.kind !== "offer" && !(s.actions || []).some((x) => /^Ja/.test(x.label)), navn + ": rammen har et tilbud");
    synlige.forEach((a) => si("ingen tilbud etter «tåler ikke»", !harTilbud(a), navn + ": et svar tilbyr noe («Vil du ha», «anbefaler», «prøv», «passer for deg», «du kan ta», «jeg foreslår …»)"));
  }
}

// 7 Faste kontroller av korpuset bak ordlyden og listene.
const kat = (n) => retter.find((r) => r.name === n).category;
si("kategori og lister", kat("Carpaccio di polpo") === "antipasti", "Carpaccio di polpo er ikke antipasti");
si("kategori og lister", kat("Agnello arrosto con salsa di pistacchio di Brontë") === "secondi", "Agnello er ikke secondi");
si("kategori og lister", kat("Formaggi misti") === "dolce", "Formaggi misti er ikke dolce");
si("kategori og lister", kat('Pizza Tartufo "Umami"') === "pizze", "Pizza Tartufo er ikke pizze");
si("kategori og lister", kat("Torta di mascarpone e pistacchi") === "dolce", "Torta er ikke dolce");
const medKat = (k) => retter.filter((r) => r.category === k).map((r) => r.name);
const iSvar = (ramme, k) => medKat(k).every((n) => RAMMER[ramme].steg.slice(-1)[0].svar.answer.includes(n));
si("kategori og lister", iSvar("liste-etter-noetter", "dolce") && medKat("dolce").length === 3, "dessertlisten har ikke alle de tre dessertene");
si("kategori og lister", iSvar("unngaar-selleri", "antipasti") && medKat("antipasti").length === 5, "forrettlisten har ikke alle de fem forrettene");
si("kategori og lister", iSvar("unngaar-kjoett", "pizze") && medKat("pizze").length === 5, "pizzalisten har ikke alle de fem pizzaene");
const pist = retter.filter((r) => /pistas[ji]/i.test(r.description_nb)).map((r) => r.name);
si("kategori og lister", pist.length === 2 && pist.every((n) => RAMMER["forteller"].steg[0].svar.answer.includes(n)), "pistasj: korpuset har " + pist.length + " retter (" + pist.join("; ") + ")");
const sel = retter.filter((r) => r.category === "antipasti" && (/selleri/i.test(r.description_nb) || r.allergen_codes.includes("SE")));
si("kategori og lister", sel.length === 1 && sel[0].name === "Carpaccio di polpo" && !sel[0].allergen_codes.includes("SE"), "selleri: " + sel.map((r) => r.name + " " + r.allergen_codes).join("; "));
const n = retter.filter((r) => r.category === "dolce" && r.allergen_codes.includes("N")).map((r) => r.name);
si("kategori og lister", n.length === 1 && n[0] === "Torta di mascarpone e pistacchi", "nøtter blant dessertene: " + n.join("; "));
const kj = retter.filter((r) => r.category === "pizze" && /salami|nduja|skinke|pølse|bacon|kjøtt/i.test(r.description_nb)).map((r) => r.name);
si("kategori og lister", kj.length === 2 && kj.includes("Pizza Vulcano") && kj.includes('Pizza Tartufo "Umami"'), "pizzaer med kjøttvarer i beskrivelsen: " + kj.join("; "));

// 8 Hver ramme er med i et bilde, og hvert bilde peker på rammer som finnes.
const brukt = new Set(BILDER.flatMap((b) => (b.kolonner || b.rader).flat().map((c) => c.ramme)));
for (const navn of Object.keys(RAMMER)) si("rammer og bilder", brukt.has(navn), navn + " er ikke med i noe bilde");
for (const navn of brukt) si("rammer og bilder", !!RAMMER[navn], "et bilde peker på rammen " + navn + ", som ikke finnes");

let sjekket = 0, feil = 0;
for (const [slag, t] of Object.entries(tall)) { console.log(String(t.sjekket).padStart(4), "kontroller,", t.feil, "feil:", slag); sjekket += t.sjekket; feil += t.feil; }
console.log("I alt", sjekket, "kontroller,", feil, "feil.", Object.keys(RAMMER).length, "rammer,", BILDER.length, "bilder.");
process.exit(feil ? 1 : 0);
