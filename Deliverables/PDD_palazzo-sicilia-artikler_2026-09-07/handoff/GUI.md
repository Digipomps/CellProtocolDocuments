# Codex-handoff — WP-GUI Sicilia-artikler (2026-09-07, G1-GUI godkjent av Kjetil)

Formål (mål alt mot dette): gjesten skal se «Fra Sicilia»-seksjonen, åpne en artikkel, reagere med tre knapper
og en kommentar; huset skal godkjenne tagger på artikkelutkast — **eksakt slik bildene i `../images/` viser**,
og det skal se likt ut i HAVEN-appen (Porthole web og native Binding) som i bildene. Antiformål: ingen lesesporing.

Forutsetning: `sicilia-impl` (WP0–WP5) er kjørt ferdig og grønn i `PalazzoScaffold` (les `docs/Rapport_Sicilia_2026-09-07.md`).
Hvis den ikke er ferdig/grønn: stopp, skriv rapport med hvorfor, gjør ingen endringer.

## Sannhetskilde for skeleton-format
Bruk bare typer/felt som finnes i `HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
(og mønstrene som allerede brukes i `PalazzoScaffold/Sources/App/Skeleton/PalazzoGuestConfigurationFactory.swift`:
`SkeletonSection(header:content:)`, `SkeletonButton(keypath:label:icon:)`, `SkeletonTextArea(submitActionKeypath:)`,
`SkeletonList(flowElementSkeleton:)` med rad-objekt som bærer `"payload"`). Finn du et felt i `../skeleton/*.json`
som IKKE finnes i SkeletonDescription.swift: bruk nærmeste eksisterende mønster og noter avviket i rapporten.
Ikke legg til nye skeleton-typer eller renderer-oppførsel i CellProtocol/CellScaffold — det er Kjetils beslutning.

## Slicer
| # | Hva | Test |
|---|---|---|
| G1 | `PalazzoGuestConfigurationFactory`: ny `siciliaSection()` etter `houseSection()`, 1:1 med `../skeleton/gjest-sicilia-liste.json` (List over `guest.state.house.articles`-radene: `id,title,lead,region,payload{articleID}`; single selection `item_id` → `guest.article.open`; kort med `styleClasses: pz-article-card`). Seksjonen utelates når det ikke finnes publiserte artikler (bilde `gjest-sicilia-tom-v1.png`). | test.skeleton.sicilia-list, test.skeleton.sicilia-empty |
| G2 | Ny fabrikk `PalazzoArticleConfigurationFactory` for `guest.article.configuration` 1:1 med `../skeleton/gjest-sicilia-artikkel.json`: region, tittel, brødtekst, opphav, Divider, «Hva gjør du med dette?», tre knapper mot `entity.article.react` med fast payload `{articleID, reaction}` (fabrikken setter artikkel-ID — ikke `$id`-tekst), TextArea med `submitActionKeypath` → kommentar med `{articleID, reaction: "comment", comment}` (hvis TextArea ikke kan bære fast payload: egen keypath `entity.article.comment` som tar `{articleID, text}` — noter valget), og løftet «Bare det du trykker eller skriver lagres — aldri at du leste.» `guest.article.open` (fra G1) returnerer/navigerer til denne konfigurasjonen. Erstatter den minimale Text-only-konfigurasjonen fra WP5. | test.skeleton.sicilia-article, test.sicilia.reaction (eksisterende, må fortsatt være grønn) |
| G3 | `PalazzoHouseDraftConfigurationFactory`: `content.draft.tags.pending` viser artikler (kind: article) i samme kort som retter, 1:1 med `../skeleton/hus-artikkel-tagger.json` (overskrift «Nye artikler i utkastet — tagger» når raden er artikkel; feltnavn `dishTitle/dishDescription/proposedTagsText` beholdes hvis cellen allerede leverer dem — ellers `title/description`). | test.skeleton.house-article-tags |
| G4 | Antiformål: test som åpner gjesteflaten og `guest.article.configuration` via fabrikkene og verifiserer at `entity.records` og event-loggen er uendret. | test.sicilia.no-tracking (utvid) |
| G5 | **Visuell verifikasjon i Porthole**: kjør fra `HAVEN/CellScaffold` `npm run skeleton:iterate -- --mode preview …` for de tre konfigurasjonene (seed: `../content/artikler_v1.json`, minst 3 publiserte artikler med godkjente tagger; PalazzoScaffold kjøres lokalt som kilde). Lagre desktop+mobil-skjermbilder som `../images/verify/porthole-<navn>-v1.png` og skriv `../images/verify/AVVIK.md`: per bilde, side om side med G1-GUI-bildet, hva er likt / hva avviker (tekst, rekkefølge, knapper, tom tilstand). Avvik i **innhold, rekkefølge, knapper, felt, bindinger** er akseptansefeil og skal rettes; avvik i **farger/fonter/avstander** noteres bare (styleClasses er metadata). Ingen debug-/action-tekst synlig som produkttekst. | test.skeleton.porthole-parity (artefakt) |
| G6 | Native HAVEN-app (Binding): hvis det finnes en CLI-/snapshot-vei (se `HAVEN/Binding` for `xcodebuild`-snapshot-tester eller skjermbilde-script), kjør den og legg bildene i `../images/verify/native-<navn>-v1.png`. Finnes ingen slik vei: skriv nøyaktig hva Kjetil må gjøre for å åpne de tre flatene i appen (URL/endpoint/konfigurasjonsnavn), i `../images/verify/NATIVE.md`. Ikke installer eller endre Binding. | artefakt |

## Regler
Som `README.md` her: CellProtocol/CellScaffold/Binding røres ikke; ingen test fjernes/svekkes; hver ny handler
kaller `validateAccess`; ingen språkmodell; **ingen git**; `swift build --disable-sandbox` / `swift test --disable-sandbox`.
Testnavn = testRef. Skeleton-testene decoder fabrikkens `CellConfiguration` til JSON og sammenligner elementtyper,
tekster, keypaths og payloads mot `../skeleton/*.json` (ikke bytesammenligning — feltrekkefølge er fri).

## Rapport
`PalazzoScaffold/docs/Rapport_Sicilia_GUI_2026-09-07.md`: rå utdata før/etter (testantall), per slice gjort/avvik,
filliste, lenker til `../images/verify/`. Oppdater `../TESTRESULT.md` med ankre `#skeleton-list #skeleton-article
#skeleton-house #porthole-parity #native`. Svar kun med rapporten.
