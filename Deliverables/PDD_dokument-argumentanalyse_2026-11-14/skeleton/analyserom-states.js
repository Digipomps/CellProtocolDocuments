// Tilstander for G1-GUI. Påstandene i «fylt» og «uten-modell» er det TextReliability faktisk ga
// for fixtures/eksempeltekst.md (results/eksempeltekst.analysis.json). Modellforslagene er illustrasjoner.
const fs = require("node:fs");
const path = require("node:path");
const dir = path.join(__dirname, "..");
const a = JSON.parse(fs.readFileSync(path.join(dir, "results", "eksempeltekst.analysis.json"), "utf8"));
const text = fs.readFileSync(path.join(dir, "fixtures", "eksempeltekst.md"), "utf8");
const TYPE = { factual: "Faktapåstand", statistical: "Statistikk", causal: "Årsak", normative: "Normativ", predictive: "Prognose", project_capability: "Kapabilitet" };
const STYRKE = { assertive: "bastant", moderated: "moderert", speculative: "spekulativ" };
const KILDE = { source_missing: "Kilde mangler", source_cue_without_anchor: "Viser til kilde uten lenke", needs_external_source_audit: "Lenke oppgitt, ikke sjekket", not_checkable: "Ikke sjekkbar" };
const marks = { "claim-0003": "1 uenig (Sara)", "claim-0004": "1 enig", "claim-0007": "2 enig · 1 uenig" };
const sjekket = { "claim-0004": "Kilde sjekket av Petter" };
const paastander = a.claim_ledger.map((c) => ({
  id: c.claim_id, idKort: "P" + Number(c.claim_id.slice(-4)), sitat: "«" + c.quote + "»",
  typeEtikett: TYPE[c.claim_type] || c.claim_type, styrkeEtikett: STYRKE[c.strength] || c.strength, opphavEtikett: "",
  kildeEtikett: sjekket[c.claim_id] || KILDE[c.source_audit_status] || c.source_audit_status, markeringer: marks[c.claim_id] || "Ingen markeringer ennå",
}));
const kort = (id) => "P" + Number(id.slice(-4));
const lab = (c) => kort(c.claim_id) + ": " + (c.quote.length > 46 ? c.quote.slice(0, 44) + " …" : c.quote);
const byId = Object.fromEntries(a.claim_ledger.map((c) => [c.claim_id, c]));
const conc = new Set(a.argument_map.explicit_conclusion_claim_ids);
const grunnGraf = {
  nodes: a.claim_ledger.map((c) => ({ id: c.claim_id, label: lab(c), kind: conc.has(c.claim_id) ? "Konklusjon" : "Påstand", group: conc.has(c.claim_id) ? "konklusjon" : "premiss", color: conc.has(c.claim_id) ? "#F59E0B" : "#60A5FA" })),
  edges: a.argument_map.inferred_links.flatMap((l) => l.from_claim_ids.map((f) => ({ source: f, target: l.to_claim_id, label: "antatt støtte", color: "#94A3B8" }))),
};
const modellGraf = {
  nodes: grunnGraf.nodes.map((n) => n.id === "claim-0005" ? { ...n, kind: "Motargument", group: "mot", color: "#F87171" } : n.id === "claim-0006" ? { ...n, kind: "Tilbakevisning", group: "tilbake", color: "#A78BFA" } : n),
  edges: [
    { source: "claim-0002", target: "claim-0007", label: "støtter", color: "#34D399" },
    { source: "claim-0004", target: "claim-0007", label: "støtter", color: "#34D399" },
    { source: "claim-0001", target: "claim-0007", label: "støtter (svakt)", color: "#34D399" },
    { source: "claim-0003", target: "claim-0002", label: "støtter (antatt)", color: "#94A3B8" },
    { source: "claim-0005", target: "claim-0007", label: "angriper", color: "#F87171" },
    { source: "claim-0006", target: "claim-0005", label: "tilbakeviser", color: "#A78BFA" },
  ],
};
const chat = [
  { forfatter: "Sara", tid: "12:04", tekst: "P3 er bare påstått. «Alle vet» er et retorisk grep, ingen kilde." },
  { forfatter: "Petter", tid: "12:06", tekst: "Sjekket NHH-lenken i P4. Studien finnes, men gjelder ett fylke." },
  { forfatter: "Kjetil", tid: "12:09", tekst: "Da er P4 sjekket, men den bærer mindre enn konklusjonen krever." },
];
const base = {
  rom: { tittel: "Analyserom: Mobilforbud i skolen", deltakere: "Sara, Petter og Kjetil · 3 deltakere · tilgang via invitasjon" },
  chatUtkast: "", aktivFane: "paastander", faner: [{ id: "paastander", title: "Påstander" }, { id: "graf", title: "Argumentgraf" }, { id: "tekst", title: "Teksten" }],
};
const tekst = { tittel: "Mobilforbud i skolen virker", meta: "Lastet opp av Sara 14.11 kl. 12:01 · eksempeltekst.md · 7 påstander", innhold: text.replace(/^# .*\n\n/, "") };
module.exports = {
  tom: { analyse: { state: { ...base, rom: { tittel: "Analyserom: Mobilforbud i skolen", deltakere: "Sara og Petter · 2 deltakere · tilgang via invitasjon" }, harTekst: false, utkast: { tittel: "", kilde: "", tekst: "" },
    chat: [{ forfatter: "Sara", tid: "11:58", tekst: "Jeg legger inn kronikken vi snakket om." }], modell: { tilgjengelig: true } } } },
  fylt: { analyse: { state: { ...base, harTekst: true, tekst, paastander, chat, harForslag: false,
    modell: { tilgjengelig: true }, oppsummering: "7 påstander · 1 konklusjon · 3 uten kilde · 1 lenke ikke sjekket · Analysert av grunnanalysen og modellen (lokal modell)",
    grafForklaring: "Gul = konklusjon, blå = premiss, rød = motargument. Grå kanter er antatt. Trykk på en node for å se påstanden.", graf: modellGraf } } },
  "fylt-graf": { analyse: { state: { ...base, aktivFane: "graf", harTekst: true, tekst, paastander, chat, harForslag: false, modell: { tilgjengelig: true },
    oppsummering: "", grafForklaring: "Gul = konklusjon, blå = premiss, rød = motargument, lilla = tilbakevisning. Grå kanter er antatt. Trykk på en node for å se påstanden.", graf: modellGraf } } },
  modellforslag: { analyse: { state: { ...base, harTekst: true, tekst, paastander, chat: chat.slice(0, 2), harForslag: true, modell: { tilgjengelig: true },
    oppsummering: "7 påstander fra grunnanalysen · 2 modellforslag venter på vurdering",
    forslag: [
      { id: "f1", typeEtikett: "Skjult premiss", sitat: "«Derfor bør alle skoler innføre et nasjonalt mobilforbud»", begrunnelse: "Konklusjonen forutsetter at resultatet fra én studie gjelder alle skoler. Forankret i P7 og P4." },
      { id: "f2", typeEtikett: "Motargument", sitat: "«Kritikerne mener at forbudet tar fra elevene et viktig læringsverktøy.»", begrunnelse: "P5 er et motargument, ikke en faktapåstand. P6 svarer på det." },
    ], grafForklaring: "", graf: modellGraf } } },
  "uten-modell": { analyse: { state: { ...base, aktivFane: "graf", harTekst: true, tekst, paastander, chat, harForslag: false,
    modell: { tilgjengelig: false, tittel: "Modellhjelp er ikke tilgjengelig nå", forklaring: "Grunnanalysen virker uten modell: påstander, kilder og en enkel graf. Koblingene under er antatt fra ordene i teksten («derfor», «bør»)." },
    oppsummering: "7 påstander · 1 konklusjon · 3 uten kilde · Analysert av grunnanalysen",
    grafForklaring: "Gul = konklusjon, blå = premiss. Alle kanter er antatt av grunnanalysen. Modellhjelp er ikke tilgjengelig nå.", graf: grunnGraf } } },
};
