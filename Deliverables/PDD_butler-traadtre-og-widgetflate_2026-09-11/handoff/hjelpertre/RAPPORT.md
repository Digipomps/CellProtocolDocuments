# Butler: hjelpertre med skop — WP-A5, WP-A1, WP-A2

## Rettelse 5 — panelRows / semantisk likhet, 2026-09-15

Ny SHA `cde7871ea7a9e6e58921d887d08e80c17623cc16`, forelder `147ff38b`, gren `pdd/butler-hjelpertre`. Én lokal commit, 4 filer (+86/−24), ren kodeworktree, ingen push. Kjetils loggutdrag fra `34950634405` (2026-09-15 10:13Z) sier bygg grønt, bolk 25 rød; ingen nettverkskontroll her.

Fjernet railens døde root-visibility i `PersonalCopilotConfigurationFactory+HelperTree.swift:35–37` på forelderen. `panelRows=[]/[{}]` styrer lukket/åpen; CSS :4624 slipper også den tomme List-wrapperens bredde. Alle 83 JSON-scope-felt og grenmerkets Swift-betingelse er `item`. Reachability-testen bygger fortsatt endelig Co-Pilot Chat og krever alle fem handlinger, men kontrollerer nå også eksplisitt åpen `[{}]`-projeksjon. Auditen traverserer List-radmaler uten runtime-state-input; produktstandarden forblir lukket. Standard-åpen bred flate hører til **WP-K3**.

Hele modelltestfilen er gjennomgått: listetomhet → antall; scope → `mode`/`nodeID`; projeksjoner → rekursiv kontroll av nøkkelsett, listeantall/rekkefølge og skalarfelt, uten ValueType-objekt/listelikhet eller dumper. Pinnen bekrefter årsaken på `ValueType.swift:258–261`.

Åpen-rail-anslag: desktop **288+12+880=1180 px**, textarea-bunn≈**790<900**. Mobil chat **317 px**, rail **288 px** som overlegg med **0 px** y-bidrag, textarea-bunn≈**798<812**; 216 px radscroller på begge. **Ikke nye DOM-målinger**; mobilmargin≈14 px krever åpen-rail-browserbevis.

Syntaksparse av tre berørte Swift-filer, literal-gate, statisk JSON/webvalidering og diffkontroll: exit 0. Swift-tester, full typesjekk, CI, faktisk åpen-rail-geometri, Binding og staging er ukjent på ny SHA. Totalsøket finner fortsatt **16 eksplisitte root-betingelser fra basen** i den uendrede hovedfabrikken, pluss en standardparameter; ingen i hjelpertretillegget. De eldre reglene er ikke funksjonsverifisert eller endret.

Full årsak sti:linje, åpen-tilstandsresonnement, søkeavvik, lærdomskandidat til Claude og kontrollbevis: [PR-butler-hjelpertre.md](/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/NATT/PR-butler-hjelpertre.md). Bare de to bestilte håndoffene er skrevet utenfor kodeworktreen; de inngår ikke i kodecommiten. Tidligere rettelser nedenfor er historikk.

## Rettelse 4 — pinnet SkeletonCondition / filterbolk, 2026-09-15

Ny lokal commit `147ff38badecb49518782ea5298d784a5dd32995` på `pdd/butler-hjelpertre`, forelder `68b6d91d`; én commit, ren kodeworktree, ingen push. PR #242/kjøring `34932934356` feilet ifølge Kjetils loggutdrag i «Build every target»: testen leste `when?.keypath`, men pinnet CellProtocol `e03923cb2f1d5a339eaf62585ddc9dddf7750cec` har `SkeletonVisibilityRule.when: SkeletonCondition?` (`Sources/CellBase/Skeleton/SkeletonDescription.swift:139`), enumcaset `.expression` (:175) og `keypath` på `SkeletonConditionExpression` (:226).

[Reachability-testen:25](/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-butler-hjelpertre/Tests/AppTests/PersonalCopilotHelperTreeReachabilityTests.swift:25) pakker nå ut uttrykket; :28 leser `openCondition.keypath`. Alle Skeleton-lesinger i de to testfilene og alle brukte initialisatorer/felt i produktfabrikken, inkludert 40 JSON-feltpar og seks elementnavn, er kontrollert mot pinnen. Ingen flere manglende API-er funnet. Modelltesten og CloudStore-tillegget bruker ingen Skeleton-typer. Produktfilene er uendret.

[A-filterbolken:389](/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-butler-hjelpertre/ci/test-filter.txt:389) er flyttet før Arendalsuka. Faktisk parser gir samme 26 grupper, bare A/Arendalsuka bytter plass. Filteret fletter med B med exit 0 og null markører. **Samlet merge-tree er fortsatt ikke konfliktfritt:** tre markører i to andre produktfiler (`PersonalCopilotCloudStore.swift:1219/:1286` og `PersonalCopilotConfigurationFactory.swift:1401`); `merge-tree --write-tree` bekrefter exit 1. Ingen faktisk merge, B-endring eller konfliktløsning i disse filene er utført.

Syntaksparse av alle fire Swift-filer og diffkontroll: exit 0. Commit: 2 filer, 9 innsettinger, 6 slettinger. Full typesjekk, Swift-tester, CI, browser, Binding og staging på ny SHA er fortsatt ukjent. Ingen bygg, docker, push eller PR-endring. Bare de to bestilte dokumentene er skrevet utenfor den rene kodeworktreen; de inngår ikke i kodecommiten.

Full egenskap→type→pinnet sti:linje-tabell, initialisatorkontroll, filtersemantikk, flettingsbevis og lærdomskandidat: [PR-butler-hjelpertre.md](/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/NATT/PR-butler-hjelpertre.md). Rettelse 3 og eldre nedenfor er historikk.

## Rettelse 3 — browser-layout, 2026-09-14

Ny lokal commit `68b6d91da084f636ffe36316ee29aa4599f69308` på `pdd/butler-hjelpertre`, forelder `3385391e`. Én commit, ren kodeworktree, ingen push. PR #242s browser-fail skyldtes 1170 px rail + egen 52 px stripe, utbrettet rot og HStack som pakket chatgridet ned under treet. Trace viste textarea-bunn 2044,23 px ved 900 px viewport.

Rettet med 288 px rail og fleksibelt chatpanel i HStack, 216 px ScrollView for radene og Butler `expanded=false`. Eksisterende `isOpen` + 0/1 `panelRows` starter lukket på begge bredder; «Tråder» åpner panelet fra chatoverskriften. Skopvelger ligger i railens fot. 34 avgrensede CSS-linjer gir sidepanel på desktop og tilstandsstyrt overlegg på kompakt web; JS er uendret. `presentation` er valgt bort fordi Apple-rendereren kun bruker feltet som metadata. Automatisk åpent/utbrettet panel på bred flate er en **WP-K3-justering**; lagrede brukervalg bevares.

Forventninger fra DOM/CSS, ikke browser-målinger: desktop `288+12+880=1180` og textarea-bunn≈790 < 900; mobil chatbredde `375−20−2−36=317`, overlegg 288 ≤317, textarea-bunn≈798 < 812. Svarets høyrekant anslås≈1211/327 < 1280/375; forventet documentScrollWidth=1280/375. Mobilanslaget har 14 px margin og må bekreftes i CI.

Syntaksparse av fire Swift-filer, literal-gate, statisk JSON/web-validator og diffkontroll er grønne. Reachability krever fortsatt selectNode/setExpanded/setScopeMode/open/close; migreringstesten og en ny geometriregresjon er oppdatert, men Swift-testene er ikke kjørt. Ny typesjekk/CI, Playwright, Binding og staging er ukjent. Ingen bygg, docker, push, PR-endring eller merge; øvrige kodearbeidskopier er urørt. De to bestilte dokumentene inngår ikke i kodecommiten.

Full feil, årsak, kildehenvisninger, måltabell, lærdomskandidat og kontrollbevis: [PR-butler-hjelpertre.md](/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/NATT/PR-butler-hjelpertre.md). Opplysningene under «Rettelse 2» er historikk.

## Rettelse 2 — CI-typesjekk, 2026-09-14

Ny lokal commit: `3385391e66218ffe16fe6a547840978bd08cb555` — `fix(butler): typet mellomledd for state-literalet så typesjekkeren ikke gir opp (CI #242)`. Forelder: `74c6dc435607351cc23bc5e6025a0b011dabe0c9`. Én ny commit på `pdd/butler-hjelpertre`, ren kodeworktree, ingen push. Diff mot forelder: **1 fil, 4 innsettinger, 2 slettinger**.

CI-feilen ordrett fra Kjetils loggutdrag for PR #242, commit `74c6dc43`, «Focused control-plane gates» → «Build every target», etter 19m 55s; rapportert 25 ganger:

```text
Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:1219:16: error: the compiler is unable to type-check this expression in reasonable time; try breaking up the expression into distinct sub-expressions
```

Årsak: state-literalet var flyttet fra `return [...]` med konkret returtype `Object` til et samlet uttrykk med `??`, implisitt fabrikk og `.project(into: [...])`, som sprengte typesjekkbudsjettet. Rettelse: eksplisitt `PersonalCopilotHelperTree.migrating`, eget `let base: Object = [...]`, så `return tree.project(into: base)`. Literalet er bytekontrollert identisk med lokal `origin/main`; ingen andre deler av filen er endret. `project(into source: Object) -> Object` er kildebekreftet. Det bestilte diff-søket over `Sources` viser bare metodesignaturen og projeksjonen av `base`, ingen andre treff med direkte literalargument.

`xcrun swiftc -frontend -parse` på den endrede filen: exit 0, **kun syntaks**. `ci/check-value-literals.sh`: exit 0 uten nettverk, seks selvtester passerte, 28 eksisterende funn dekket av uendret baseline. Staget diffkontroll: exit 0. Full typesjekk/bygg, Swift-testutfall, grønn CI etter rettelsen og staging er fortsatt ukjent; literal-gaten beviser ikke typesjekk. Ingen bygg, docker, pin-endring, push, PR-endring, merge eller endringer i `CellScaffold/`-arbeidskopien eller B-grenen.

Detaljer og kontrollbevis: [PR-butler-hjelpertre.md](/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/NATT/PR-butler-hjelpertre.md). Bare de to bestilte håndoffene er oppdatert utenfor kodeworktreen; de inngår ikke i kodecommiten.

## Tidligere leveranse og rettelse 1 — historikk

Opplysningene nedenfor gjelder før rettelse 2; gjeldende SHA og verifikasjon står øverst.

Status 2026-09-14: opprinnelig kode og tester i `d14c0362a895d27c139cf3a26efd606063e6dec3`, rettelse i `74c6dc435607351cc23bc5e6025a0b011dabe0c9`. **Blokkeringen er omgått med en teststøttekopi; avhengighetsgapet er ikke løst.** Pinnen er urørt. Syntaksparse av begge testfilene og støttefilen ga exit 0; kompilering, testutfall og staging er fortsatt ukjent.

Gren: `pdd/butler-hjelpertre`. To commits foran base, ren kodeworktree etter rettelsescommit. Worktree: `_worktrees/cellscaffold-butler-hjelpertre`.
Base: lokal `origin/main` = `649255bb777b3a5135bd9c50512d3074bd23935b`.
`git -C CellScaffold fetch origin` feilet med `Could not resolve hostname github.com: -65563`; ingen oppdatert remote-status er kjent.

## Formål og resultat

- `purpose://candidate.butler.helper-tree-model` (A5): Butler som rot; den eksisterende helperRows-katalogen migreres idempotent til barn; gamle promptmeldinger får Butler som node.
- `purpose://candidate.pattern.reference-tree.model` (A1): stabile node-ID-er uavhengig av referert verktøy/celle/chat; validering av rot, forelder, unik ID og sykler; ny node kan legges til uten rotendring.
- `purpose://candidate.pattern.reference-tree.scope` (A2): valgt node og `subtree`/`node` gir én ferdig filtrert chatlogg med synlig grenopphav og sammenhengende tellere. Inn-/utbretting påvirker bare hvilke trenoder som er synlige.

## Endringer per fil

Alle stier er relative til HAVEN-roten.

| Fil | Hva som er skrevet |
|---|---|
| `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore+HelperTree.swift:8` | Node/referanse, validert Codable-tre v1, migreringsfunksjon, upsert med sykelavvisning, fem UI-handlinger og samlet projeksjon. Historikkfallback kan ta med refererte noder uten å overstyre destinasjonens skop. |
| `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:976` | Valgfritt lagret tre og valgfritt nodeID for bakoverkompatibel dekoding, ett projeksjonskall på :1219, liten actionbro på :3136, nodeID i alle fem eksisterende loggappend-kall og migrering ved første lasting av en UI-scope på :10555. Eksisterende `setChatUIActiveHelper` på :3150 er byte-for-byte uendret. |
| `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells+HelperTree.swift:8` | Registrerer `ui.helperTree.selectNode`, `setExpanded`, `setScopeMode`, `open`, `close`, r-/rw-tilgang etter eksisterende mønster, eksplisitte Explore-skjemaer og requester-rettet `ui.helperTree`-event ved godkjent endring. Nye lesninger hentes fra produksjonens `chatState`. |
| `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1597` | Ett kall til registrering ved dagens `ui.setActiveHelper`. |
| `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory+HelperTree.swift:9` | Innebygd WP-K1-kandidat, semantisk identisk JSON; venstrepanel rundt eksisterende samtalearbeidsflate. Enkel åpne/lukke-kontroll via 0/1 `helperTree.panelRows`, chatoverskrift og grenmerker med eksisterende elementer. |
| `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:1401` | Tre små innkoblinger: grenmerke i promptmalen, skopoverskrift inne i rullefeltet (:1775), venstrepanel rundt samtalepanelet (:2838). Øvrig innhold beholdt. |
| `_worktrees/cellscaffold-butler-hjelpertre/Tests/AppTests/PersonalCopilotHelperTreeTests.swift:17` | Seks målrettede tester gjennom modellens produksjonskode, faktisk CloudStore-dekoding/lagring/projeksjon og Cell SET/GET/flow. |
| `_worktrees/cellscaffold-butler-hjelpertre/Tests/AppTests/PersonalCopilotHelperTreeReachabilityTests.swift:10` | Dekoder den ferdige `Co-Pilot Chat`-konfigurasjonen og bruker `HelperTreeSkeletonReachabilityAudit.reachableActionKeypaths` for alle fem handlinger fra `tre.handlinger.md`, også close. |
| `_worktrees/cellscaffold-butler-hjelpertre/Tests/AppTests/Fixtures/PersonalCopilotHelperTreeLegacy.json:1` | Syntetisk fixture med de 16 eksisterende helper-ID-ene/titlene og gammel persistert UI-form med tre meldinger uten nodeID. **Ikke eksport fra staging.** |
| `_worktrees/cellscaffold-butler-hjelpertre/Tests/AppTests/Support/HelperTreeSkeletonReachabilityAudit.swift:1` | Midlertidig, kildeidentisk audit med nytt typenavn, proveniensheader og `import CellBase`; se kompileringsrisiko. |
| `_worktrees/cellscaffold-butler-hjelpertre/ci/test-filter.txt:397` | Begge suitene i egen bolk: `---`, kommentaren «WP-A5/A1/A2: hjelpertre med skop — modell, migrering, skop og produksjonsaudit.», deretter modell- og reachability-suiten. Gruppegrensene over beholdes. |

## Lagring og datakontrakt

Ingen ny lagringsmekanisme. Treet ligger i `chatUIStatesByScopeID[requesterUUID:threadID-or-default].helperTree` sammen med promptloggen. Kilden er `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:1603`; eksisterende skriving av UI-scope er :10622, lasting :15472, atomisk JSON-save :15510 og filnavn :15517. Logisk filsti: `<CellBase.documentRootPath>/PersonalCopilot/personal-copilot-cloud.json`. Uten dokumentrot brukes eksisterende system-tempfallback `CellScaffoldPersonalCopilot/PersonalCopilot/personal-copilot-cloud.json`. Faktisk staging-dokumentrot: **ukjent**.

Migreringen kjører første gang en requester/thread-UI lastes uten tre, og lagrer via eksisterende `save()`. Valg, modus og expanded lagres på samme måte. Eksisterende `try? save()`-mønster beholdes; skrivefeil er derfor en kjent begrensning og lokal syntakskontroll beviser ikke holdbar lagring. Historikk uten nodeID får `butler`; nye append-kall bruker valgt nodeID. Treet eier referansene, historikken forblir én eksisterende promptliste. Et valgt nodeID er samtaleopphav/mottakerkontekst; A3-ruting til en kapabel hjelper er ikke implementert.

Leverte bindinger: alle feltene i `tre.keypaths.md`, inkl. `conversationSummary`, `scopeSummary`, `visibleRows`, `scopeControlRows[].mode`, samt `chatPanelRows[].title/count/countLabel/scopeDescription/scopeChips/composerTargetLabel` og `promptMessages[].branchChips`. Også `scope`, `isOpen`, `version` og den ekstra 0/1-listen `panelRows` eksponeres. `chatPanelRows[].mode` er `expanded`; widgetgrenens restore/docking-kontrakt er utenfor denne leveransen.

Telledefinisjoner, siden kontrakten lot dem stå åpne:

- `conversationSummary`: én rot + antall direkte rotbarn, uavhengig av utbretting. Migrert full katalog gir 17 samtaler; en modell uten hjelpere gir 1. Dette er ikke mockupens hardkodede 4.
- `countText`: unike, beholdte meldinger i radnodens undertre, uavhengig av valgt skopmodus.
- Chat `count`/`countLabel`: samme filtrerte, kronologiske og dedupliserte meldingsutvalg som loggen. Tidsstempler parses som ISO8601; like tidspunkter bevarer lagret rekkefølge.
- Grener i skop: alle noder i skopet unntatt Butler. En valgt hjelper inngår selv; `node` på en hjelper har derfor 1 gren, `node` på Butler har 0. `scopeChips` følger samme mengde, og `branchChips` er tom for Butler og én rad for annen opphavsnode.
- `visualDepth = min(2, max(0, depth - 1))`: vilkårlig modelldybde beholdes, men dype noder flates visuelt til kandidatens siste innrykk. Ingen noder skjules fordi modellen er dypere enn tre malnivåer. Valg har prioritet over `inscope`. Alle underhjelpere har foreløpig tone `branchA`; ingen avslag eller A3-status fabrikkeres.

## §5-tester skrevet

Mønster fulgt: `_worktrees/cellscaffold-butler-hjelpertre/Tests/AppTests/PersonalCopilotV1Tests.swift:16` (IsolatedCellTestCase, EphemeralIdentityVault, null resolver, eksisterende resetForTests), :48 (testidentitet), :1699 (promptlogg fra virkelig actionresultat) og :4846 (flow-abonnement med XCTest-forventning). Basisens isolerte dokumentrot finnes i `_worktrees/cellscaffold-butler-hjelpertre/Sources/ScaffoldTestKit/IsolatedCellTestCase.swift:19`.

| Test | Dekning |
|---|---|
| `test.tree-model` | `testTreeModelThreeLevelsSharedReferenceAndCycleRejection`: tre nivåer, uendret rot, to node-ID-er med samme verktøy, sykel/orphan/root-mutasjon avvist, Codable-rundtur og ugyldig persistert sykel avvist. |
| `test.migration` | `testMigrationPreservesLegacyHelpersAndMessagesAndIsIdempotent`: gammel fixture gjennom produksjonens CloudStore-dekoder, første lesning, migrering/save, ny store-instans og samme noder/meldinger. Bevarer antall, titler og referanser; meldinger under Butler. Ekte staging-fixture mangler. |
| `test.scope.switch` | `testScopeSwitchChangesLogCountersAndChipsWithoutLosingHistory`: ekte store-actions, undertre/egen node, søsken utelatt, riktige tellere/chips, innbretting uten loggtap, ugyldig node uten mutasjon, gjenlasting og retur til hele utvalget. |
| Supplerende kontraktstest | `testCellRegistersActionsAndReadsAndKeepsLegacyHelperSelection`: faktiske registrerte Cell-actions og getter, flow ved endring, open/close, ugyldig bool, modus bevart og gammel setActiveHelper uendret. |
| Supplerende produksjonsvei | `testPromptSubmitRecordsSelectedNodeThroughProductionAppendPath`: faktisk prompt.submit og opphav/chips på resultatets meldinger. Ingen alternativ testlogg-implementasjon. |
| Supplerende projeksjon | `testProjectionChronologyDeduplicationAndDeeperVisualRows`: tidssoner, brøkdelssekunder, stabil rekkefølge ved lik tid, duplikat-ID og dype synlige noder. |
| Reachability | `testFinalChatConfigurationExposesTreeAcceptanceActions`: ferdig fabrikkskjelett, JSON-rundtur, teststøttekopien `HelperTreeSkeletonReachabilityAudit` av produksjonsauditen; krever selectNode/setExpanded/setScopeMode/open/close og ingen tapte trehandlinger. |

Sju tester skrevet, **ingen Swift-tester kjørt**. Begge suitene er i CI-filteret. Neste målrettede vertsverifikasjon fra worktreen er: `scripts/run_swift_bounded.sh test --filter PersonalCopilotHelperTree` (ikke kjørt her).

## Byggfrie kontroller kjørt

- Rettelse 2026-09-14: fra `_worktrees/cellscaffold-butler-hjelpertre` ga `xcrun swiftc -frontend -parse Tests/AppTests/PersonalCopilotHelperTreeTests.swift Tests/AppTests/PersonalCopilotHelperTreeReachabilityTests.swift Tests/AppTests/Support/HelperTreeSkeletonReachabilityAudit.swift` exit 0. **Kun syntaks**; ingen import-/typesjekk, bygg eller testkjøring. Kildesammenligning bekreftet uendret auditlogikk, bare navnebytter i reachability-testen og uendret modelltest/pin. `git diff --cached --check` ga exit 0 før rettelsescommiten.

Kontrollene nedenfor er fra den opprinnelige leveransen 2026-09-13 og er ikke kjørt på nytt i rettelsen:

- `xcrun swiftc -frontend -parse` på seks berørte produksjonsfiler og begge testfiler: exit 0. **Kun syntaks**, ingen import-/typesjekk eller bygg.
- `ci/check-value-literals.sh`: exit 0; seks selvtester passerte; 28 eksisterende store literaler dekket av eksisterende baseline, ingen vekst. Baseline og store eksisterende literaler er ikke omarbeidet, i tråd med oppdragets krav om små innkoblinger.
- `ci/test-suite-coverage.sh`: exit 0; 294 deklarerte testsuiter, 274 i kjørefilteret, 21 i unntaksfilen. Dette er kildeinventar, ikke kjørte tester.
- Node/VM med **worktreens** `Public/js/skeleton-runtime.js`: innebygd kandidat er semantisk identisk med PDD-JSON; `validateSkeleton` returnerte `valid:true, error:null`. Dette er strukturkontroll av kandidaten, ikke rendering eller reachability av ferdig konfigurasjon.
- Explore-kildeaudit over PersonalCopilot: baseline 14 komplette registreringer/285 handlers; endringen 16/287. Begge: 142 errors og 129 warnings, ingen nye funn. Auditen teller de dynamiske registreringsløkkene som to kildekall; dette er ikke en runtime-Explore-manifestverifikasjon og ikke et grønt kontraktsertifikat.
- `git diff --cached --check`: exit 0. Den gamle `setChatUIActiveHelper`-funksjonen er sammenlignet mot base og er uendret.

## Kompileringsrisiko og uutført arbeid

**Bekreftet avhengighetsgap, blokkeringen omgått — ikke løst:** `_worktrees/cellscaffold-butler-hjelpertre/Package.swift` og `Package.resolved` pinner fortsatt CellProtocol `e03923cb2f1d5a339eaf62585ddc9dddf7750cec`, som mangler `SkeletonReachabilityAudit`. Rettelsen legger auditen i `Tests/AppTests/Support/HelperTreeSkeletonReachabilityAudit.swift`: en ordrett kopi av lokal `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift` fra `83de32626390928f477c47b39df4dd13ae7831e3`, med audittypen omdøpt til `HelperTreeSkeletonReachabilityAudit`, B-grenens femlinjers kilde-/fjerningsheader og `import CellBase`. Logikken er uendret, og reachability-testen har bare tre navnebytter. Kilderevisjonen er hentet med `git -C CellProtocol log -1 --format=%H -- Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift`; kopien er bytekontrollert mot kilden etter reversering av header/import/navneendring.

Pakkepin, `Package.resolved` og CellProtocol er urørt. **Koordinert pin-oppdatering står igjen som egen oppgave og er Kjetils beslutning.** Fjern teststøttekopien og bruk den eksporterte auditen når pinnet CellBase har API-et. Kun syntaks er kontrollert; import-/typesjekk mot pinnen, kompilering av hele AppTests, Swift-testresultater og grønn CI er fortsatt ukjent.

Øvrige API-er er kildeavstemt, men typesjekk og runtimeutfall er **ukjent**:

- Strenge registerGet/registerSet-overloads følger `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1597` for tilgang/dispatch og `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell+InterceptRegistration.swift:54` / :81 for Explore-overloads; SET-overloaden er også bekreftet i pinnen. Skjemamønster: `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PurposeQuality/PurposeQualityMonitorCell.swift:56`.
- FlowElement.Properties + pushFlowElement følger `_worktrees/cellscaffold-butler-hjelpertre/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:708` / :736 og `CellProtocol/Sources/CellBase/FeedItem/FlowElement.swift:29`. Nye flow-events bærer bare actionnavnet, ikke samtaletekst.
- SkeletonVStack/HStack/List/Text/Button følger `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1240`, :1307, :1407, :1752 og eksisterende fabrikk :1394. Innebygd JSON er ikke kjørt gjennom Swift-dekoderen her; fabrikken krever at konstanten dekoder, og den nye testen kontrollerer samme kodevei.
- Optional `helperTree`/`nodeID` bygger på eksisterende syntetiserte Codable-typer; diskfixturetesten må bekrefte migreringen. Source-path fixturelesning følger testens `#filePath`; ikke en runtime-ressurs.

Ikke gjort: WP-A3 fallback/ruting, WP-A4 foreslå/opprette hjelper gjennom UI, widgetflate, restore/docked-chatpanel, renderer- eller formatendring, pikselparitet, generisk tretastatur, drawer/backdrop/fokushåndtering, Binding-fabrikkdeling, ekte staging-migrering, nettverks-Explore, GUI-preview, bygg, kjøring, docker, push, PR-oppretting, merge eller deploy. Den eksisterende grensen på 40 promptlogginnslag er beholdt. Kompakt layout og relative nestede List-bindinger må verifiseres separat på web og Binding; kandidaten har kjent fast geometri og er bare tilnærmet.

## Kjent ved merge

A og B legger hver sin egen bolk til slutten av `ci/test-filter.txt`. Når den andre PR-en merges, forventes en enlinjes konflikt her; behold begge bolkene med hver sin `---`, kommentar og testsuiter, slik at gruppegrensene over ikke forskyves. Ingen merge er prøvd i denne rettelsen.

## Hvordan Kjetil ser resultatet på staging

Etter verifisering mot pinnet CellProtocol, grønn CI og Kjetils vanlige staging-deploy: kontroller `/health/build` mot den deployede merge-revisjonen. Nåværende staging-SHA og URL er **ukjent** i denne økten.

1. Åpne **Co-Pilot Chat → Samtale** (Butler Chat), kilde `cell:///PersonalChatHub`.
2. Se Butler-roten til venstre med migrerte hjelpere. Klikk en hjelper, eksempelvis **Docs/RAG**; skopoverskriften og «skriver til» skal endres. Meldinger fra gammel historikk ligger under Butler.
3. Send en ufarlig melding i den valgte grenen. Den skal bli stående i én logg med grenmerke. Dette verifiserer nodetilhørighet; A3-verktøyruting leveres senere.
4. Velg Butler, veksle **Undertre / Bare denne**: undertre skal inkludere den nye grenmeldingen; bare Butler skal utelate den. Antall i loggoverskriften må følge utvalget. Velg hjelperen igjen for å se dens egne meldinger.
5. Brett Butler inn/ut: synlige barn endres, valgt skop og meldingsutvalg skal bestå. **Lukk tre** fjerner panelet, **Tråder** åpner det igjen. Ingen drawer-/fokusparitet hevdes.
6. Last flaten på nytt og kontroller valgt node, modus, utbretting, grenopphav og samme meldingsmengde. Reell persistens og rendereratferd må godkjennes her.

## Arbeidsgrenser

Kodeendringer og begge kodecommits er i `_worktrees/cellscaffold-butler-hjelpertre`; denne rettelsen la til nøyaktig én commit. `CellScaffold/`-arbeidskopiens filer er ikke endret; den sto på `pdd/tillitspakke-agentflaate` og hadde omfattende eksisterende endringer. Bare den uttrykkelig bestilte fetch/worktree-operasjonen brukte dette repoets Git-metadata. Ingen annen agents arbeid er inkludert. I rettelsen ble B-grenens støttefil bare lest som topptekstreferanse; B-grenen og `CellScaffold/`-arbeidskopien er ikke endret, og ingen fetch er kjørt.

Utenfor worktreen skrives bare de to uttrykkelig bestilte leveransefilene: `HAVEN-Deploy/_handoff/NATT/PR-butler-hjelpertre.md` og `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/handoff/hjelpertre/RAPPORT.md`. Disse ligger i allerede urene, separate arbeidskopier og inngår ikke i CellScaffold-commiten. Ingen kø, logger eller øvrige filer er endret.

## Git-bevis

Arbeidsmappe for kommandoene: `_worktrees/cellscaffold-butler-hjelpertre`.
Repoets eksisterende Git-identitet ble brukt; author/committer står derfor som Claude i loggen. Koden i denne leveransen er skrevet i denne Codex-økten; Git-konfigurasjonen ble ikke endret.

`git log -1 --format=fuller`:

```text
commit 74c6dc435607351cc23bc5e6025a0b011dabe0c9
Author:     Claude <noreply@anthropic.com>
AuthorDate: Mon Sep 14 00:38:27 2026 +0200
Commit:     Claude <noreply@anthropic.com>
CommitDate: Mon Sep 14 00:38:27 2026 +0200

    test(butler): reachability-audit som teststøtte-kopi til CellProtocol-pinnen er oppdatert
```

`git diff origin/main --stat`:

```text
 .../PersonalCopilotCells+HelperTree.swift          |  97 ++++++
 .../PersonalCopilot/PersonalCopilotCells.swift     |   1 +
 .../PersonalCopilotCloudStore+HelperTree.swift     | 244 ++++++++++++++
 .../PersonalCopilotCloudStore.swift                |  41 ++-
 ...nalCopilotConfigurationFactory+HelperTree.swift | 227 +++++++++++++
 .../PersonalCopilotConfigurationFactory.swift      |   4 +-
 .../Fixtures/PersonalCopilotHelperTreeLegacy.json  | 133 ++++++++
 ...ersonalCopilotHelperTreeReachabilityTests.swift |  24 ++
 .../AppTests/PersonalCopilotHelperTreeTests.swift  | 244 ++++++++++++++
 .../HelperTreeSkeletonReachabilityAudit.swift      | 355 +++++++++++++++++++++
 ci/test-filter.txt                                 |   5 +
 11 files changed, 1370 insertions(+), 5 deletions(-)
```

`git status --porcelain=v1`: tomt resultat (ren worktree).
`git rev-list --count origin/main..HEAD`: `2`.
`git rev-list --count d14c0362a895d27c139cf3a26efd606063e6dec3..HEAD`: `1` (nøyaktig én ny commit).
Rettelsescommiten inneholder bare støttefilen, de tre navnebyttene i reachability-testen og CI-bolkskillet: 3 filer, 360 innsettinger og 3 slettinger.
Ingen push, PR, merge eller deploy er utført.

## Fem linjer svar

1. Levert: A5/A1/A2-kode i `_worktrees/cellscaffold-butler-hjelpertre`, gren `pdd/butler-hjelpertre`, nyeste commit `74c6dc435607351cc23bc5e6025a0b011dabe0c9`; ren worktree.
2. Butler er rot; migrerte hjelpere, nodetilhørighet, skop, tellere, grenmerker og venstrepanel er skrevet i produksjonsveien.
3. Sju Swift-tester skrevet; kun syntaks, webstruktur, literalgrense, CI-suiteinventar, kildeaudit og diffkontroll er kjørt.
4. Blokkeringen er omgått med en kildeidentisk teststøttekopi; pinnet CellProtocol mangler fortsatt auditen. Kompilering, Swift-testresultater og staging er ukjent.
5. Neste eier er Kjetil: verifiser mot pinnen, håndter PR/CI og staging med klikklisten over. Koordinert pin-oppdatering og fjerning av kopien står igjen som egen oppgave; forventet CI-filterkonflikt er beskrevet under «Kjent ved merge».
