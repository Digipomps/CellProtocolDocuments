// Analyserom-skjelettet for G1-GUI (iterasjon 1). Blir Swift-fabrikk etter G1/G2.
const ink = { foregroundColor: "#172033" };
const subtle = { foregroundColor: "#475569", fontSize: 13 };
const primary = { background: "#1D4ED8", foregroundColor: "#FFFFFF", cornerRadius: 6 };
const secondary = { background: "#FFFFFF", foregroundColor: "#334155", borderColor: "#CBD5E1", borderWidth: 1, cornerRadius: 6 };
const card = { padding: 12, cornerRadius: 10, background: "#F8FAFC", borderColor: "#E2E8F0", borderWidth: 1 };
const when = (keypath, equals = true) => ({ visibility: { when: { scope: "root", keypath, equals } } });
const whenItem = (keypath, equals = true) => ({ visibility: { when: { scope: "item", keypath, equals } } });
const T = (text, m = ink) => ({ Text: { text, modifiers: m } });
const K = (keypath, m = ink) => ({ Text: { keypath, modifiers: m } });
const B = (keypath, label, extra = {}, m = secondary) => ({ Button: { keypath, label, ...extra, modifiers: m } });
const H = (elements, m = {}) => ({ HStack: { elements, spacing: 8, modifiers: { wrap: true, ...m } } });
const V = (elements, m = {}, spacing = 8) => ({ VStack: { elements, spacing, modifiers: m } });

const inntak = V([
  T("Legg inn teksten dere skal analysere", { ...ink, fontSize: 17, fontWeight: "semibold" }),
  { FileUpload: { title: "Last opp tekst", helperText: "Tekst (.txt) eller Markdown (.md), maks 1 MB. Alle i rommet ser teksten.",
    actionKeypath: "analyse.inntak.fil", acceptedContentTypes: ["text/plain", "text/markdown"], allowsMultiple: false,
    supportsDrop: true, emptyTitle: "Ingen fil valgt", emptyMessage: "Slipp en fil her eller velg fra maskinen.",
    maxSizeBytes: 1048576, uploadMode: "base64", submitOnSelection: true } },
  T("eller lim inn", subtle),
  { TextField: { placeholder: "Tittel, for eksempel «Kronikk i Aftenposten 12.11»", sourceKeypath: "analyse.state.utkast.tittel", targetKeypath: "analyse.inntak.tittel" } },
  { TextField: { placeholder: "Kilde (lenke eller referanse)", sourceKeypath: "analyse.state.utkast.kilde", targetKeypath: "analyse.inntak.kilde" } },
  { TextArea: { modifiers: { background: "#FFFFFF", foregroundColor: "#111827", borderColor: "#CBD5E1", borderWidth: 1, cornerRadius: 6, paddingInsets: { top: 9, bottom: 9, leading: 12, trailing: 12 } }, editorMode: "plain", minLines: 6, maxLines: 14, placeholder: "Lim inn teksten her …", sourceKeypath: "analyse.state.utkast.tekst", targetKeypath: "analyse.inntak.tekst" } },
  H([B("analyse.inntak.analyser", "Analyser teksten", { payload: {} }, primary)]),
], { ...card, background: "#FFFFFF", ...when("analyse.state.harTekst", false) });

const modellBanner = V([
  H([K("analyse.state.modell.tittel", { ...ink, fontWeight: "semibold" })]),
  K("analyse.state.modell.forklaring", subtle),
], { padding: 10, cornerRadius: 8, background: "#FEF9C3", borderColor: "#FDE68A", borderWidth: 1, ...when("analyse.state.modell.tilgjengelig", false) });

const paastandRad = V([
  H([K("idKort", { ...subtle, fontWeight: "semibold" }), K("typeEtikett", { fontSize: 12, foregroundColor: "#1D4ED8" }), K("styrkeEtikett", { fontSize: 12, foregroundColor: "#7C3AED" }), K("opphavEtikett", { fontSize: 12, foregroundColor: "#B45309" })]),
  K("sitat", { ...ink, fontSize: 15 }),
  H([K("kildeEtikett", { fontSize: 12, foregroundColor: "#0F766E" }), K("markeringer", subtle)]),
  H([B("analyse.marker.enig", "Enig", { payloadKeypath: "id" }), B("analyse.marker.uenig", "Uenig", { payloadKeypath: "id" }), B("analyse.marker.kildeSjekket", "Kilde sjekket", { payloadKeypath: "id" }), B("analyse.kommenter", "Kommenter", { payloadKeypath: "id" })]),
], { ...card, background: "#FFFFFF" }, 6);

const forslagRad = V([
  H([T("Modellforslag", { fontSize: 12, foregroundColor: "#B45309", fontWeight: "semibold" }), K("typeEtikett", { fontSize: 12, foregroundColor: "#1D4ED8" })]),
  K("sitat", ink),
  K("begrunnelse", subtle),
  H([B("analyse.forslag.godta", "Godta", { payloadKeypath: "id" }, primary), B("analyse.forslag.avvis", "Avvis", { payloadKeypath: "id" })]),
], { ...card, background: "#FFFBEB", borderColor: "#FDE68A" }, 6);

const paastander = V([
  K("analyse.state.oppsummering", subtle),
  modellBanner,
  V([T("Til vurdering fra modellen", { ...ink, fontWeight: "semibold" }),
     { List: { keypath: "analyse.state.forslag", elements: [], flowElementSkeleton: forslagRad } }], when("analyse.state.harForslag")),
  { List: { keypath: "analyse.state.paastander", elements: [], flowElementSkeleton: paastandRad } },
], {}, 10);

const graf = V([
  K("analyse.state.grafForklaring", subtle),
  { Visualization: { kind: "network", keypath: "analyse.state.graf", stateKeypath: "analyse.state.grafValg", actionKeypath: "analyse.velgNode" } },
  H([B("analyse.eksport.mermaid", "Last ned Mermaid", { payload: {} }), B("analyse.eksport.json", "Last ned analyse (JSON)", { payload: {} })]),
]);

const tekst = V([K("analyse.state.tekst.tittel", { ...ink, fontWeight: "semibold" }), K("analyse.state.tekst.meta", subtle), K("analyse.state.tekst.innhold", ink)], { ...card, background: "#FFFFFF" });

const chat = V([
  T("Chat i rommet", { ...ink, fontWeight: "semibold" }),
  { List: { keypath: "analyse.state.chat", elements: [], flowElementSkeleton: V([
    H([K("forfatter", { fontSize: 12, fontWeight: "semibold", foregroundColor: "#1D4ED8" }), K("tid", { fontSize: 12, foregroundColor: "#94A3B8" })]),
    K("tekst", ink)], { padding: 8, cornerRadius: 8, background: "#F1F5F9" }, 2) } },
  { TextArea: { modifiers: { background: "#FFFFFF", foregroundColor: "#111827", borderColor: "#CBD5E1", borderWidth: 1, cornerRadius: 6, paddingInsets: { top: 9, bottom: 9, leading: 12, trailing: 12 } }, editorMode: "plain", minLines: 1, maxLines: 6, placeholder: "Skriv til gruppa …", sourceKeypath: "analyse.state.chatUtkast", targetKeypath: "analyse.chat.send", submitOnEnter: true } },
], { ...card, minWidth: 280, layoutVariants: [{ minAvailableWidth: 900, width: 340 }] });

const hoved = V([
  inntak,
  { Tabs: { tabsKeypath: "analyse.state.faner", activeTabStateKeypath: "analyse.state.aktivFane", idKeypath: "id", labelKeypath: "title", modifiers: { ...when("analyse.state.harTekst") },
    panels: [
      { id: "paastander", title: "Påstander", content: [paastander] },
      { id: "graf", title: "Argumentgraf", content: [graf] },
      { id: "tekst", title: "Teksten", content: [tekst] },
    ] } },
], { flexGrow: 1 }, 12);

const analyseromSkeleton = V([
  H([V([K("analyse.state.rom.tittel", { ...ink, fontSize: 22, fontWeight: "bold" }), K("analyse.state.rom.deltakere", subtle)], { flexGrow: 1 }, 2),
     B("analyse.inviter", "Inviter", { payload: {} })]),
  { HStack: { spacing: 16, elements: [hoved, chat], modifiers: { vAlignment: "top", layoutVariants: [{ maxAvailableWidth: 899, axis: "vertical" }] } } },
], { padding: 16, background: "#FFFFFF" }, 14);

module.exports = { analyseromSkeleton };
