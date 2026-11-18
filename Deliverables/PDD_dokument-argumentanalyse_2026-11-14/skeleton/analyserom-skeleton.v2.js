// Analyserom-skjelettet, v2 (WP8). Samme oppsett som G1-GUI-bildene (v1), med
// keypathene TextAnalysisRoomCell faktisk har, argumentkartet i stedet for
// nettverket, og chatten som egen fane på smal skjerm.
// `node skeleton/export-skeleton.js` skriver JSON-en som Swift-fabrikken bygger inn.
const ink = { foregroundColor: "#172033" };
const subtle = { foregroundColor: "#475569", fontSize: 13 };
const primary = { background: "#1D4ED8", foregroundColor: "#FFFFFF", cornerRadius: 6 };
const secondary = { background: "#FFFFFF", foregroundColor: "#334155", borderColor: "#CBD5E1", borderWidth: 1, cornerRadius: 6 };
const card = { padding: 12, cornerRadius: 10, background: "#F8FAFC", borderColor: "#E2E8F0", borderWidth: 1 };
const field = { background: "#FFFFFF", foregroundColor: "#111827", borderColor: "#CBD5E1", borderWidth: 1, cornerRadius: 6, paddingInsets: { top: 9, bottom: 9, leading: 12, trailing: 12 } };
const when = (keypath, equals = true) => ({ visibility: { when: { scope: "root", keypath, equals } } });
const T = (text, m = ink) => ({ Text: { text, modifiers: m } });
const K = (keypath, m = ink) => ({ Text: { keypath, modifiers: m } });
const B = (keypath, label, extra = {}, m = secondary) => ({ Button: { keypath, label, ...extra, modifiers: m } });
const H = (elements, m = {}) => ({ HStack: { elements, spacing: 8, modifiers: { wrap: true, ...m } } });
const V = (elements, m = {}, spacing = 8) => ({ VStack: { elements, spacing, modifiers: m } });
const S = "analyse.state.";

const inntak = V([
  T("Legg inn teksten dere skal analysere", { ...ink, fontSize: 17, fontWeight: "semibold" }),
  { FileUpload: { title: "Last opp tekst", helperText: "Tekst (.txt) eller Markdown (.md), maks 1 MB. Alle i rommet ser teksten.",
    actionKeypath: "analyse.inntak.fil", acceptedContentTypes: ["text/plain", "text/markdown"], allowsMultiple: false,
    supportsDrop: true, emptyTitle: "Ingen fil valgt", emptyMessage: "Slipp en fil her eller velg fra maskinen.",
    maxSizeBytes: 1000000, uploadMode: "base64", submitOnSelection: true } },
  T("eller lim inn", subtle),
  { TextField: { placeholder: "Tittel, for eksempel «Kronikk i Aftenposten 12.11»", sourceKeypath: S + "utkast.tittel", targetKeypath: "analyse.inntak.tittel" } },
  { TextField: { placeholder: "Kilde (lenke eller referanse)", sourceKeypath: S + "utkast.kilde", targetKeypath: "analyse.inntak.kilde" } },
  { TextArea: { modifiers: field, editorMode: "plain", minLines: 6, maxLines: 14, placeholder: "Lim inn teksten her …", sourceKeypath: S + "utkast.tekst", targetKeypath: "analyse.inntak.tekst" } },
  H([B("analyse.inntak.analyser", "Analyser teksten", { payload: {} }, primary)]),
], { ...card, background: "#FFFFFF", ...when(S + "harTekst", false) });

const modellBanner = V([
  K(S + "modell.tittel", { ...ink, fontWeight: "semibold" }),
  K(S + "modell.forklaring", subtle),
], { padding: 10, cornerRadius: 8, background: "#FEF9C3", borderColor: "#FDE68A", borderWidth: 1, ...when(S + "modell.tilgjengelig", false) });

const paastandRad = V([
  H([K("idKort", { ...subtle, fontWeight: "semibold" }), K("typeEtikett", { fontSize: 12, foregroundColor: "#1D4ED8" }), K("styrkeEtikett", { fontSize: 12, foregroundColor: "#7C3AED" }), K("opphavEtikett", { fontSize: 12, foregroundColor: "#B45309" })]),
  K("sitat", { ...ink, fontSize: 15 }),
  H([K("kildeEtikett", { fontSize: 12, foregroundColor: "#0F766E" }), K("markeringer", subtle)]),
  H([B("analyse.marker.enig", "Enig", { payloadKeypath: "id" }), B("analyse.marker.uenig", "Uenig", { payloadKeypath: "id" }), B("analyse.marker.kildeSjekket", "Kilde sjekket", { payloadKeypath: "id" }), B("analyse.kommenter", "Kommenter", { payloadKeypath: "id" })]),
], { ...card, background: "#FFFFFF" }, 6);

const kommentar = V([
  K(S + "valgt.tekst", subtle),
  { TextArea: { modifiers: { ...field, ...when(S + "valgt.harValgt") }, editorMode: "plain", minLines: 2, maxLines: 6, placeholder: "Skriv en kommentar …", targetKeypath: "analyse.kommentar.send", submitOnEnter: true } },
], { ...card });

const forslagRad = V([
  H([T("Modellforslag", { fontSize: 12, foregroundColor: "#B45309", fontWeight: "semibold" }), K("typeEtikett", { fontSize: 12, foregroundColor: "#1D4ED8" })]),
  K("sitat", ink),
  K("begrunnelse", subtle),
  H([B("analyse.forslag.godta", "Godta", { payloadKeypath: "id" }, primary), B("analyse.forslag.avvis", "Avvis", { payloadKeypath: "id" })]),
], { ...card, background: "#FFFBEB", borderColor: "#FDE68A" }, 6);

const modellHjelp = V([
  K(S + "modell.forklaring", subtle),
  H([B("analyse.modell.foreslaa", "Be modellen om forslag", { payload: {} })]),
], when(S + "modell.tilgjengelig"));

const paastander = V([
  K(S + "oppsummering", subtle),
  modellBanner,
  modellHjelp,
  V([T("Til vurdering fra modellen", { ...ink, fontWeight: "semibold" }),
     { List: { keypath: S + "forslag", elements: [], flowElementSkeleton: forslagRad } }], when(S + "harForslag")),
  kommentar,
  { List: { keypath: S + "paastander", elements: [], flowElementSkeleton: paastandRad } },
], {}, 10);

const kart = V([
  K(S + "grafForklaring", subtle),
  { Visualization: { kind: "argumentmap", keypath: S + "graf", stateKeypath: S + "valgt", actionKeypath: "analyse.velgNode" } },
]);

const tekst = V([K(S + "tekst.tittel", { ...ink, fontWeight: "semibold" }), K(S + "tekst.meta", subtle), K(S + "tekst.innhold", ink)], { ...card, background: "#FFFFFF" });

const eksport = V([
  K(S + "eksport.forklaring", subtle),
  K(S + "eksport.mermaid", { ...ink, fontSize: 12 }),
], { ...card, background: "#FFFFFF" });

const chatInnhold = (id) => [
  T("Chat i rommet", { ...ink, fontWeight: "semibold" }),
  { List: { keypath: S + "chat", elements: [], flowElementSkeleton: V([
    H([K("forfatter", { fontSize: 12, fontWeight: "semibold", foregroundColor: "#1D4ED8" }), K("tid", { fontSize: 12, foregroundColor: "#94A3B8" })]),
    K("tekst", ink)], { padding: 8, cornerRadius: 8, background: "#F1F5F9" }, 2) } },
  { TextArea: { modifiers: field, editorMode: "plain", minLines: 1, maxLines: 6, placeholder: "Skriv til gruppa …", sourceKeypath: S + "chatUtkast", targetKeypath: "analyse.chat.send", submitOnEnter: true } },
];

// Bred skjerm: chatten står i en kolonne til høyre. Smal skjerm: kolonnen skjules og chatten er en fane.
const chatKolonne = V(chatInnhold("kolonne"), { ...card, minWidth: 280, layoutVariants: [{ maxAvailableWidth: 899, hidden: true }, { minAvailableWidth: 900, width: 340 }] });
const chatFane = V([
  V(chatInnhold("fane"), { ...card, layoutVariants: [{ minAvailableWidth: 900, hidden: true }] }),
  T("Chatten står til høyre på bred skjerm.", { ...subtle, layoutVariants: [{ maxAvailableWidth: 899, hidden: true }] }),
]);

const hoved = V([
  inntak,
  { Tabs: { tabsKeypath: S + "faner", activeTabStateKeypath: S + "aktivFane", idKeypath: "id", labelKeypath: "title", modifiers: { ...when(S + "harTekst") },
    // Fanenavnene kommer fra `faner` i tilstanden (labelKeypath); Swift har ikke tittel på panelet.
    panels: [
      { id: "paastander", content: [paastander] },
      { id: "graf", content: [kart] },
      { id: "tekst", content: [tekst] },
      { id: "eksport", content: [eksport] },
      { id: "chat", content: [chatFane] },
    ] } },
], { flexGrow: 1 }, 12);

const analyseromSkeleton = V([
  V([K(S + "rom.tittel", { ...ink, fontSize: 22, fontWeight: "bold" }), K(S + "rom.deltakere", subtle)], {}, 2),
  { HStack: { spacing: 16, elements: [hoved, chatKolonne], modifiers: { vAlignment: "top", layoutVariants: [{ maxAvailableWidth: 899, axis: "vertical" }] } } },
], { padding: 16, background: "#FFFFFF" }, 14);

module.exports = { analyseromSkeleton };
