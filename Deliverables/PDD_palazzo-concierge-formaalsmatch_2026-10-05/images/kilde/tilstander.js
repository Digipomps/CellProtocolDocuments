// Tilstandene de ni bildene viser (G1-GUI, PDD_palazzo-concierge-formaalsmatch_2026-10-05).
// Tekstene om retter og drikke er kopiert fra korpuset (palazzo_seed_corpus.json), ikke skrevet av.
// Dette er en skisse: ingen programkode har laget svarene. De viser foreslått ordlyd og plassering.
"use strict";

const MENY = {
  last_verified: "2026-06-03", source_id: "src-palazzo-menu-pdf", status: "active",
  title: "Palazzo Communales meny (PDF)", url: "https://palazzocomunale.no/s/Meny-med-drikkemeny-mars.pdf"
};
// Linjene om allergener er dem koden på nett har (regel 3 i strakstiltaket,
// PalazzoScaffold/Sources/App/Controllers/PalazzoCommunaleProjection.swift, linje 17–19):
// én for én rett med beskrivelse, én for flere, og én for svar uten beskrivelse.
const LINJE_EN_RETT = "Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller.";
const LINJE_ALLERGEN = "Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller.";
const LINJE_KORT = "Spør personalet om allergener før du bestiller.";
const LINJE_DATERT = "Svaret bygger på et datert kunnskapsgrunnlag. Dagens meny, priser og tilgjengelighet må bekreftes av Palazzo.";
const LINJE_PERSONAL = "Merkingen dekker ikke spor eller krysskontakt. Si fra til personalet før du bestiller.";

function konvolutt(answer, extra = {}) {
  return Object.assign({
    schema: "haven.palazzo.communale.guest-concierge.v1", status: "answered", answer,
    citations: [MENY], citation_count: 1, citation_summary: "Kilder: Palazzo Communales meny (PDF)",
    last_verified: "2026-06-03", confidence: "high", audience: "guest", needs_human_review: false,
    warnings: [LINJE_ALLERGEN, LINJE_DATERT], route: "native", reason_code: "answered"
  }, extra);
}
function utenKilder(answer) {
  return konvolutt(answer, { citations: [], citation_count: 0, citation_summary: "", last_verified: "", warnings: [] });
}
// Én rett med beskrivelse: linjen for én rett, som på nett i dag.
function enRett(answer, extra = {}) {
  return konvolutt(answer, Object.assign({ warnings: [LINJE_EN_RETT, LINJE_DATERT] }, extra));
}
// En bom, slik eksempelet contract/eksempler/gyldig-03-bom.svar.json har den.
function bom(answer) {
  return konvolutt(answer, {
    status: "requires-review", confidence: "blocked", citations: [], citation_count: 0,
    citation_summary: "Ingen publiserbare kilder i dette svaret.", last_verified: "", warnings: [], reason_code: "match-miss"
  });
}

// Rettene, ordrett fra korpuset.
const R = {
  formaggi: "Formaggi misti: Utvalg av oster fra små utvalgte gårder i Italia med tilbehør.",
  polpo: "Carpaccio di polpo: Blekksprutcarpaccio med kokt potet, stangselleri, olivenolje og sitron.",
  agnello: "Agnello arrosto con salsa di pistacchio di Brontë: Lammecarré og lammenakke med pistasj fra Brontë, gulrot og bakt løk.",
  tartufo: "Pizza Tartufo \"Umami\": Pizza med trøffelsalami, høsttrøffel, taleggio og mozzarella.",
  arancini: "Arancini: Friterte riskroketter fylt med ragu, safran og ost, to stk."
};

const NOTERT_HJELP = "Gjelder mens du har siden åpen. Ikke lagret.";
const INTRO_NY = "Spør med egne ord, eller velg en snarvei. Det du sier om deg selv, huskes mens du har siden åpen, og lagres ikke.";
const JA_NEI = [{ label: "Ja, det vil jeg", primary: true }, { label: "Nei takk" }];
const JA_NOTE = "Et ja bestiller ikke. Du bestiller hos kelneren.";

const RAMMER = {
  // 1 ────────────────────────────────────────────────────────────────────────
  "tilbud": {
    modus: "layout", bredde: 1280,
    steg: [{ si: "Jeg liker ost", svar: enRett("Vi har " + R.formaggi + " Vil du ha det til dessert?") }],
    skisse: {
      kind: "offer", intro: INTRO_NY, understood: "du liker ost.", hideBadge: true,
      actions: JA_NEI, note: JA_NOTE,
      noted: [{ text: "liker ost" }], notedHelp: NOTERT_HJELP
    }
  },
  "tilbud-mobil": {
    modus: "card", bredde: 390,
    steg: [{ si: "Jeg liker ost", svar: enRett("Vi har " + R.formaggi + " Vil du ha det til dessert?") }],
    skisse: {
      kind: "offer", understood: "du liker ost.", hideBadge: true,
      actions: JA_NEI, note: JA_NOTE,
      noted: [{ text: "liker ost" }], notedHelp: NOTERT_HJELP
    }
  },
  // 2 ────────────────────────────────────────────────────────────────────────
  "flere-forrett": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker blekksprut", svar: enRett("Vi har " + R.polpo + " Vil du ha det til forrett?") }],
    skisse: { kind: "offer", understood: "du liker blekksprut.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideBadge: true }
  },
  "flere-hovedrett": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker lam", svar: enRett("Vi har " + R.agnello + " Vil du ha det til hovedrett?") }],
    skisse: { kind: "offer", understood: "du liker lam.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideBadge: true }
  },
  "flere-pizza": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker trøffel", svar: enRett("Vi har " + R.tartufo + " Vil du ha den?") }],
    skisse: { kind: "offer", understood: "du liker trøffel.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideBadge: true }
  },
  "flere-drikke": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker eplemost", svar: konvolutt("Vi har Eplemost. Vil du ha det å drikke?", { warnings: [LINJE_KORT, LINJE_DATERT] }) }],
    skisse: { kind: "offer", understood: "du liker eplemost.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideBadge: true }
  },
  // Tillegg: samme tilbud med merkelappen siden setter på svar i dag.
  "merkelapp-forslag": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker blekksprut", svar: enRett("Vi har " + R.polpo + " Vil du ha det til forrett?") }],
    skisse: { kind: "offer", understood: "du liker blekksprut.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideBadge: true }
  },
  "merkelapp-som-i-dag": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker blekksprut", svar: enRett("Vi har " + R.polpo + " Vil du ha det til forrett?") }],
    skisse: { kind: "offer", understood: "du liker blekksprut.", actions: JA_NEI, note: JA_NOTE, hideSources: true, viserSidensMerkelapp: true }
  },
  // 3 ────────────────────────────────────────────────────────────────────────
  "forteller": {
    modus: "card", bredde: 1280,
    steg: [{
      si: "Jeg liker pistasj", svar: konvolutt(
        "Vi har to retter med pistasj:\n\n" +
        "Agnello arrosto con salsa di pistacchio di Brontë (hovedrett): Lammecarré og lammenakke med pistasj fra Brontë, gulrot og bakt løk.\n\n" +
        "Torta di mascarpone e pistacchi (dessert): Ovnsbakt ostekake på mascarpone og pistasi fra Brontë.")
    }],
    skisse: { kind: "tell", understood: "du liker pistasj.", hideBadge: true, noted: [{ text: "liker pistasj" }], notedHelp: NOTERT_HJELP }
  },
  // 4 ────────────────────────────────────────────────────────────────────────
  "kvittering-liker-ikke": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker ikke ost", svar: utenKilder("Notert: du liker ikke ost. Jeg foreslår helst andre retter. Spør du om ost, får du svar likevel.") }],
    skisse: {
      kind: "receipt", eyebrow: "Notert", title: "Fra Palazzo concierge", hideWarning: true, hideSources: true,
      noted: [{ text: "liker ikke ost" }], notedHelp: NOTERT_HJELP
    }
  },
  "kvittering-taaler-ikke": {
    modus: "svar", bredde: 1280,
    steg: [{
      si: "Jeg tåler ikke nøtter.", svar: utenKilder(
        "Notert: du tåler ikke nøtter. Jeg foreslår derfor ingen retter selv. Spør du om retter, viser jeg merkingen og beskrivelsen fra menyen. Personalet må bekrefte før du bestiller.")
    }],
    skisse: {
      kind: "receipt", eyebrow: "Notert", hideWarning: true, hideSources: true,
      noted: [{ text: "tåler ikke nøtter", cls: "avoid" }], notedHelp: NOTERT_HJELP
    }
  },
  "liste-etter-noetter": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Jeg tåler ikke nøtter.", svar: utenKilder("Notert: du tåler ikke nøtter.") },
      {
        si: "Hva har dere til dessert?", svar: konvolutt(
          "Du har sagt at du ikke tåler nøtter. Jeg foreslår derfor ingen rett. Dette sier menyen om dessertene:\n\n" +
          "Torta di mascarpone e pistacchi er merket med nøtter.\nMerket med: hvete/gluten, melk, egg, nøtter, lupin.\nBeskrivelse: Ovnsbakt ostekake på mascarpone og pistasi fra Brontë.\n\n" +
          "Crema di limone Siciliana.\nMerket med: hvete/gluten.\nBeskrivelse: Karamellisert sitronkrem og sitronsorbet.\n\n" +
          "Formaggi misti.\nMerket med: melk.\nBeskrivelse: Utvalg av oster fra små utvalgte gårder i Italia med tilbehør.",
          { confidence: "medium", warnings: [LINJE_PERSONAL, LINJE_DATERT] })
      }
    ],
    skisse: {
      kind: "review", eyebrow: "Fra menyen", badge: "må bekreftes av personalet",
      noted: [{ text: "tåler ikke nøtter", cls: "avoid" }], notedHelp: NOTERT_HJELP
    }
  },
  // 5 ────────────────────────────────────────────────────────────────────────
  "ja": {
    modus: "card", bredde: 1280,
    steg: [
      { si: "Jeg liker ost", svar: enRett("Vi har " + R.formaggi + " Vil du ha det til dessert?") },
      { trykk: "Ja, det vil jeg", svar: konvolutt("Notert: du vil ha Formaggi misti til dessert. Jeg kan ikke bestille for deg, og kelneren ser ikke dette. Si det til kelneren når du bestiller.", { warnings: [LINJE_KORT, LINJE_DATERT] }) }
    ],
    skisse: {
      kind: "receipt", eyebrow: "Notert", questionLabel: "Ditt svar", question: "Ja, det vil jeg", hideSources: true,
      noted: [{ text: "liker ost" }, { text: "vil ha Formaggi misti til dessert", cls: "purpose" }], notedHelp: NOTERT_HJELP
    }
  },
  // 6 ────────────────────────────────────────────────────────────────────────
  "unngaar-selleri": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Jeg tåler ikke selleri.", svar: utenKilder("Notert: du tåler ikke selleri.") },
      {
        si: "Hva har dere av forretter?", svar: konvolutt(
          "Du har sagt at du ikke tåler selleri. Jeg foreslår derfor ingen rett. Dette sier menyen om forrettene:\n\n" +
          "Carpaccio di polpo: beskrivelsen nevner stangselleri. Retten er ikke merket med selleri.\nMerket med: skalldyr, hvete/gluten.\nBeskrivelse: Blekksprutcarpaccio med kokt potet, stangselleri, olivenolje og sitron.\n\n" +
          "Ostriche: merkingen er ikke bekreftet.\nMerket med: bløtdyr.\nBeskrivelse: Østers Fine De Claire, 3 eller 6 stk.\n\n" +
          "Pane di campagna focaccia e olio.\nMerket med: hvete/gluten, lupin.\nBeskrivelse: Landbrød, focaccia og olivenolje.\n\n" +
          "Arancini.\nMerket med: hvete/gluten, egg, melk, lupin.\nBeskrivelse: Friterte riskroketter fylt med ragu, safran og ost, to stk.\n\n" +
          "Vitello tonnato.\nMerket med: fisk.\nBeskrivelse: Tynne skiver kalveroastbiff med tunfiskmajones, ristet kalvebrissel og asparges.",
          { confidence: "medium", warnings: [LINJE_PERSONAL, LINJE_DATERT] })
      }
    ],
    skisse: {
      kind: "review", eyebrow: "Fra menyen", badge: "må bekreftes av personalet",
      noted: [{ text: "tåler ikke selleri", cls: "avoid" }], notedHelp: NOTERT_HJELP
    }
  },
  "unngaar-kjoett": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Jeg spiser ikke kjøtt.", svar: utenKilder("Notert: du spiser ikke kjøtt.") },
      {
        si: "Hvilke pizzaer har dere?", svar: konvolutt(
          "Du har sagt at du ikke spiser kjøtt. Disse pizzaene nevner kjøttvarer i beskrivelsen:\n\n" +
          "Pizza Vulcano: chilisalami og 'nduja.\nBeskrivelse: Piccant pizza med San Marzano tomatsaus, chilisalami, 'nduja, grønn pepper og mozzarella.\n\n" +
          "Pizza Tartufo \"Umami\": trøffelsalami.\nBeskrivelse: Pizza med trøffelsalami, høsttrøffel, taleggio og mozzarella.\n\n" +
          "De andre pizzaene:\n\n" +
          "Pizza Margherita.\nBeskrivelse: San Marzano tomatsaus, mozzarella og basilikum.\n\n" +
          "Pizza Siciliana.\nBeskrivelse: San Marzano tomatsaus, aubergine, tomat, oliven, kapers, caciocavallo og mozzarella.\n\n" +
          "Pizza Salina.\nBeskrivelse: San Marzano tomatsaus, nubia, ansjos, hvitløk og kapers.\n\n" +
          "Jeg kjenner bare beskrivelsene, og kan ikke si at en pizza er uten kjøtt. Spør personalet.",
          { confidence: "medium" })
      }
    ],
    skisse: {
      kind: "tell", eyebrow: "Fra menyen", hideBadge: true,
      noted: [{ text: "spiser ikke kjøtt", cls: "avoid" }], notedHelp: NOTERT_HJELP
    }
  },
  // 7 ────────────────────────────────────────────────────────────────────────
  "notert": {
    modus: "layout", bredde: 1280,
    steg: [
      { si: "Jeg liker pistasj", svar: konvolutt("…") },
      { si: "Jeg liker ikke ost", svar: konvolutt("…") },
      { si: "Jeg spiser ikke kjøtt.", svar: utenKilder("Notert: du spiser ikke kjøtt. Spør du om retter, sier jeg hvilke som nevner kjøttvarer i beskrivelsen.") }
    ],
    skisse: {
      kind: "receipt", eyebrow: "Notert", intro: INTRO_NY, hideWarning: true, hideSources: true,
      noted: [{ text: "liker pistasj" }, { text: "liker ikke ost" }, { text: "spiser ikke kjøtt", cls: "avoid" }],
      notedHelp: NOTERT_HJELP + " Trykk ✕ for å fjerne én ting, eller «Fjern alt»."
    }
  },
  "notert-fjernet": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Jeg spiser ikke kjøtt.", svar: utenKilder("…") },
      { trykk: "✕ på «liker ikke ost»", svar: utenKilder("Fjernet: «liker ikke ost». Jeg regner ikke lenger med det.") }
    ],
    skisse: {
      kind: "receipt", eyebrow: "Fjernet", questionLabel: "Du fjernet", question: "liker ikke ost", hideWarning: true, hideSources: true,
      noted: [{ text: "liker pistasj" }, { text: "spiser ikke kjøtt", cls: "avoid" }], notedHelp: NOTERT_HJELP
    }
  },
  "notert-tomt": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Jeg spiser ikke kjøtt.", svar: utenKilder("…") },
      { trykk: "Fjern alt", svar: utenKilder("Alt er fjernet. Jeg husker ingenting av det du har sagt om deg selv.") }
    ],
    skisse: { kind: "receipt", eyebrow: "Fjernet", questionLabel: "Du trykket", question: "Fjern alt", hideWarning: true, hideSources: true }
  },
  // 8 ────────────────────────────────────────────────────────────────────────
  "modell-spoer": {
    modus: "svar", bredde: 1280,
    steg: [{
      si: "Har dere noe sånt som risboller?", svar: bom(
        "Jeg fant ikke noe hos oss som passer til det du skrev. Skal jeg spørre en språkmodell hva du mener?\n\n" +
        "Da sendes setningen din ut av huset, til en språkmodell. Den får bare peke på noe huset har. Svaret du får, er husets eget.")
    }],
    skisse: {
      kind: "ask-model", eyebrow: "Ikke funnet", understood: "du spør om noe huset har.", hideWarning: true, hideSources: true,
      actions: [{ label: "Denne gangen", primary: true }, { label: "Hele samtalen" }, { label: "Nei" }],
      note: "Sier du nei, sendes ingenting."
    }
  },
  "modell-svar": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Har dere noe sånt som risboller?", svar: utenKilder("…") },
      { trykk: "Denne gangen", svar: enRett(R.arancini, { route: "model" }) }
    ],
    skisse: {
      kind: "model", eyebrow: "Fra menyen", question: "Har dere noe sånt som risboller?", hideBadge: true,
      modelMark: "Tolket av en språkmodell", modelNote: "Modellen pekte på Arancini. Teksten er fra menyen."
    }
  },
  "modell-nei": {
    modus: "svar", bredde: 1280,
    steg: [
      { si: "Har dere noe sånt som risboller?", svar: utenKilder("…") },
      { trykk: "Nei", svar: utenKilder("Greit. Da er ingenting sendt. Prøv gjerne med andre ord, eller spør personalet.") }
    ],
    skisse: { kind: "receipt", eyebrow: "Ikke funnet", question: "Har dere noe sånt som risboller?", hideWarning: true, hideSources: true }
  },
  // 9 ────────────────────────────────────────────────────────────────────────
  "behold-inngang": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker sitron", svar: konvolutt("…") }],
    skisse: {
      kind: "strip-only",
      noted: [{ text: "liker sitron" }, { text: "liker ikke ost" }, { text: "tåler ikke nøtter", cls: "avoid" }],
      notedHelp: NOTERT_HJELP, keepLink: "Behold til neste gang"
    }
  },
  "behold-panel": {
    modus: "svar", bredde: 1280,
    steg: [{ si: "Jeg liker sitron", svar: konvolutt("…") }],
    skisse: {
      kind: "strip-only",
      noted: [{ text: "liker sitron" }, { text: "liker ikke ost" }, { text: "tåler ikke nøtter", cls: "avoid" }],
      notedHelp: NOTERT_HJELP,
      keep: {
        title: "Vil du beholde dette til neste gang?",
        text: "Da lager du din egen gjesteprofil hos Palazzo. Det du krysser av, flyttes dit. Huset ser det ikke uten at du sier ja til det.",
        items: [
          { text: "liker sitron", checked: true },
          { text: "liker ikke ost", checked: true },
          { text: "tåler ikke nøtter", checked: false, small: "Dette handler om helse. Det tas bare med hvis du krysser av." }
        ],
        actions: [{ label: "Lag gjesteprofil", primary: true }, { label: "Nei, behold ingenting" }]
      }
    }
  }
};

// Hvert bilde: tittel, hva gjesten har skrevet, og rammene med bildetekst.
const BILDER = [
  {
    fil: "concierge-tilbud-v1", tittel: "1 · Et tilbud som svar",
    ingress: "Gjesten skriver «Jeg liker ost». Conciergen svarer med osteretten og spør om hun vil ha den til dessert.",
    rader: [[{ ramme: "tilbud", tekst: "Concierge-delen av siden. Nytt: «Slik forsto jeg deg», spørsmålet i svaret, de to knappene med linjen under, «Notert i denne samtalen», og setningen under «Hva vil du vite?» om hva som huskes. Merkelappen «høy sikkerhet», som siden setter på svar i dag, er tatt bort på tilbudet (se tilleggsbildet om merkelappen)." }]]
  },
  {
    fil: "concierge-tilbud-flere-v1", tittel: "2 · Tilbud om andre slags ting",
    ingress: "Ordlyden følger rettens plass på menyen: «til forrett» og «til hovedrett» her, «til dessert» i bilde 1. En pizza: «Vil du ha den?». Drikke uten alkohol: «Vil du ha det å drikke?». Drikke med alkohol tilbys aldri. Hvert tilbud har linjen om allergener under seg, som svarene på nett i dag. Kildene er tatt ut av utsnittene.",
    rader: [
      [{ ramme: "flere-forrett", tekst: "En forrett." }, { ramme: "flere-hovedrett", tekst: "En hovedrett." }],
      [{ ramme: "flere-pizza", tekst: "En pizza." }, { ramme: "flere-drikke", tekst: "En drikk uten alkohol. Drikke har ingen beskrivelse i menyen." }]
    ]
  },
  {
    fil: "concierge-forteller-v1", tittel: "3 · Et svar som bare forteller",
    ingress: "Gjesten skriver «Jeg liker pistasj». To retter passer, så conciergen nevner begge og spør ikke.",
    rader: [[{ ramme: "forteller", tekst: "Ingen knapper. «pistasi» står slik i menyen, og gjengis ordrett." }]]
  },
  {
    fil: "concierge-kvittering-v1", tittel: "4 · En kvittering uten tilbud, og listen etter «Jeg tåler ikke nøtter.»",
    ingress: "Sier gjesten noe hun ikke liker eller ikke tåler, kvitterer conciergen og tilbyr ingenting. Etter «tåler ikke» tilbyr den ingen retter resten av samtalen.",
    kolonner: [
      [{ ramme: "kvittering-liker-ikke", tekst: "A. «Jeg liker ikke ost». Retter med ost trekkes ned. De stenges ikke ute." }, { ramme: "kvittering-taaler-ikke", tekst: "B. «Jeg tåler ikke nøtter.»" }],
      [{ ramme: "liste-etter-noetter", tekst: "C. Etter B spør gjesten «Hva har dere til dessert?». Ingen rett tilbys. Ostekaken står først fordi den er merket med nøtter. For de to andre vises merkingen og beskrivelsen slik de står. Svaret sier ikke at noe er trygt." }]
    ]
  },
  {
    fil: "concierge-ja-v1", tittel: "5 · Når gjesten sier ja til et tilbud",
    ingress: "Etter bilde 1 trykker gjesten «Ja, det vil jeg». Ingenting blir bestilt.",
    rader: [[{ ramme: "ja", tekst: "Interessen er blitt et formål, og står som det i «Notert». Kelneren ser det ikke; det er bestillingsoppgaven. Linjen om allergener står under, fordi svaret nevner en rett." }]]
  },
  {
    fil: "concierge-unngaar-v1", tittel: "6 · Listen etter «Jeg tåler ikke selleri.», og etter «Jeg spiser ikke kjøtt.»",
    ingress: "Conciergen sier hva merkingen og beskrivelsen sier, og hva som ikke er bekreftet. Den velger ikke ut retter som «uten».",
    rader: [[
      { ramme: "unngaar-selleri", tekst: "A. «Jeg tåler ikke selleri.» og så «Hva har dere av forretter?». Carpaccio di polpo står først: beskrivelsen nevner stangselleri, og retten er ikke merket med selleri. Ostriche: merkingen er ikke bekreftet." },
      { ramme: "unngaar-kjoett", tekst: "B. «Jeg spiser ikke kjøtt.» og så «Hvilke pizzaer har dere?». Svaret sier hvilke som nevner kjøttvarer, og sier ikke at resten er uten. Pizza Salina har ansjos; conciergen regner ikke fisk som kjøtt." }
    ]]
  },
  {
    fil: "concierge-notert-v1", tittel: "7 · Det conciergen har notert, og hvordan gjesten fjerner det",
    ingress: "Bare det gjesten sier om seg selv, noteres. Et spørsmål noterer ingenting. Det ligger nederst i kortet og følger med fra svar til svar.",
    rader: [
      [{ ramme: "notert", tekst: "A. Etter tre setninger. Det hun unngår, har rød kant. Nytt også: setningen under «Hva vil du vite?»." }],
      [{ ramme: "notert-fjernet", tekst: "B. Etter ✕ på «liker ikke ost»." }, { ramme: "notert-tomt", tekst: "C. Etter «Fjern alt». Stripen er borte." }]
    ]
  },
  {
    fil: "concierge-modell-bak-v1", tittel: "8 · Når matchen feiler: spørsmålet til gjesten, og et svar tolket av en språkmodell",
    ingress: "Gjesten skriver «Har dere noe sånt som risboller?». Ingen ord i setningen treffer husets graf. Siden spør før noe sendes. Eksempelsetningen byttes med en som er målt som bom, før G3.",
    kolonner: [
      [{ ramme: "modell-spoer", tekst: "A. Spørsmålet. «Hele samtalen» gjelder til siden lukkes." }, { ramme: "modell-nei", tekst: "C. Etter «Nei»." }],
      [{ ramme: "modell-svar", tekst: "B. Etter «Denne gangen». Modellen har pekt på en rett; teksten er menyens, og overskriften sier «Fra menyen», ikke «Kontrollert svar»." }]
    ]
  },
  {
    fil: "concierge-behold-v1", tittel: "9 · Når gjesten vil beholde det som er notert",
    ingress: "Gjelder først når veien fra siden til en egen gjesteprofil finnes. Bildet viser inngangen, ikke onboardingen.",
    rader: [[
      { ramme: "behold-inngang", tekst: "A. Lenken «Behold til neste gang» i stripen." },
      { ramme: "behold-panel", tekst: "B. Etter trykk. Det hun ikke tåler, er ikke krysset av på forhånd." }
    ]]
  },
  {
    fil: "tillegg-concierge-tilbud-smal-skjerm-v1", tittel: "Tillegg · Bilde 1 på en smal skjerm (390 punkter)",
    ingress: "Ikke ett av de ni. Viser at de nye delene får plass på en telefon.",
    rader: [[{ ramme: "tilbud-mobil", tekst: "Kortet på 390 punkters bredde." }]]
  },
  {
    fil: "tillegg-concierge-merkelapp-v1", tittel: "Tillegg · Merkelappen på et tilbud: forslaget, og slik siden gjør i dag",
    ingress: "Ikke ett av de ni. Siden setter i dag «høy sikkerhet», «middels sikkerhet» eller «lav sikkerhet» på et svar den har kilde for. Ordet gjelder hvor sikkert svaret er, men ved siden av en rett kan det leses som at retten er sikker. I forslaget er merkelappen tatt bort på svar som tilbyr eller nevner retter. Valget er ditt.",
    rader: [[
      { ramme: "merkelapp-forslag", tekst: "A. Forslaget, slik det står i bildene 1, 2, 3, 6B og 8B: ingen merkelapp." },
      { ramme: "merkelapp-som-i-dag", tekst: "B. Det samme svaret med merkelappen siden setter i dag: «høy sikkerhet». Resten av rammen er forslaget, og kildene er tatt ut av utsnittet. Samme merkelapp står på rettbeskrivelser på nett nå." }
    ]]
  }
];

module.exports = { RAMMER, BILDER, LINJER: { enRett: LINJE_EN_RETT, flere: LINJE_ALLERGEN, kort: LINJE_KORT, personal: LINJE_PERSONAL, datert: LINJE_DATERT } };
