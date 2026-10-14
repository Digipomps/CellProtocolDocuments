Skjelettrunden fra PDD_butler-traadtre-og-widgetflate: de elementene og modifikatorene Butlers
trådtre og widgetflate trenger, testet mot funksjon og formål før main.

**Hva som er nytt**

- `Tree` som eget element: én radmal i stedet for ni synlighetsvarianter, med selection/expansion,
  bekreftet utbretting, tastatur og ARIA-nivå fra data.
- `ComponentSurface`: en vert kan montere en versjonert definisjon fra en kildecelle. Én av
  `instanceID` og `instanceIDKeypath` — med keypath leses instans-ID fra radens data, så hver rad i
  en `List` får sin egen flate og tilstand.
- `SkeletonLayoutVariant` kan skjule et element eller gi det fast bredde etter målt plass, i tillegg
  til akse, kolonner, avstand, polstring, høyde, flexGrow, skrift og farger.
- Modifikatorene M1–M10 (polstring, typografi, listerader, størrelser, kontrollstil, kanter,
  layoutvarianter, dra/slipp, tekstdekorasjon, leadingMarker).
- Native layout tolker nå likt som SwiftUI-stakken den erstattet: en `Spacer` uten bredde tar ledig
  plass, og lang tekst brytes i raden i stedet for å gå ut over kanten.
- `SkeletonStyleParity.webStylesheetRoles` kjenner rollene web faktisk styler.

**Testet**

Hele CellProtocol-suiten er grønn på grenens siste commit (1 225 tester, 0 feil). T-F1/T-F2
(format, rundtur, audit) og de nye rundene for formatet og native layout er i suiten. Web-siden av
det samme er testet i CellScaffold på `pdd/skjelett-elementer-web` (node-kontrakt, nettleserspecer
og CI-filteret uten nye feil), og formålstesten T-P1 kjøres mot lokal testvert med skjermbilder.

Bevis og beslutninger: `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/`
(`STATUS.md`, `handoff/WP-*.md`, `evidence/`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011CHU13qBKbb5szsQQo53rW
