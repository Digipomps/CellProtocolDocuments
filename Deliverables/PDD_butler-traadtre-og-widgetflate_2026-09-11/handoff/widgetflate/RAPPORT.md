# CI-rettelse 2026-09-14 — PR #243

Ny lokal commit: `f45368ed1b99da010f48064966d066809f8e3198` på `pdd/butler-widgetflate`; rent worktree, ingen push/bygg/Docker/PR-endring.
CI-metadata bekrefter grønt bygg og feilende Swift-gate for `94d92a1a`. Det oppgitte utdraget viser åtte assertions i tre testmetoder (Drop fem, Cancel én, Reload to); seks øvrige tester har ingen oppgitt feil. Full rålogg lot seg ikke laste ned i denne økten.

Årsak: `ValueType.==` returnerer ubetinget `false` for `.object`/`.list` (`/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/ValueTypes/ValueType.swift:258`), også med identisk innhold. På `:121` er begge sider samme objekt-case med like bladverdier; ingen skjult feltdifferanse. Dictionary-utskriftsrekkefølgen er et sidesymptom.
Åtte sammenligninger er omskrevet til kanonisert JSON med sorterte nøkler og normaliserte tidsstempler. Kildeposter kontrolleres også via ID/antall; diskens bytekontroller beholdes. Rekursiv keypath-/type-diagnostikk ligger i teststøtten. Ingen produktkode er endret. `Self.now()` er privat/ikke overstyrbar (`PersonalCopilotCloudStore.swift:15724`); alle ni tester er kontrollert for klokke-/ID-avhengighet og bruker returnerte ID-er, ikke tilfeldige forventninger.

AIGateway-feilen er utenfor grenens diff. Bolk 7 og alle første 25 bolker er uendret mot lokal `origin/main`; mulig flakiness/rekkefølge, ikke reproduksjonsbekreftet. Testen er urørt.
`xcrun swiftc -frontend -parse` på begge endrede Swift-filer, literal-gate og diffkontroller passerer. **Kun syntaks/statikk; ingen Swift-tester eller ny CI-kjøring.**

Forebygging: Kontroller `Equatable` før sammenligning av hele `ValueType`-projeksjoner. Sorter JSON-nøkler, behold listeorden/ID-er/null og normaliser tidsstempler; bruk rekursiv diagnostikk. Ikke registrer nøkkelrekkefølge som rotårsak når container-likheten alltid returnerer `false`.
Detaljer, per-test-tabell og kilder: [leveransen](/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/NATT/PR-butler-widgetflate.md).

---

## Historisk leveranse fra 94d92a1a

Den oppdaterte CI-/commitstatusen står øverst; opprinnelig leveranse følger uendret.

# feat(butler): widgetflate med dra-ut og feste — B0, B2b, B1 (PDD butler-traadtre-og-widgetflate)

Butler får «Flaten rundt» på web. Et kildeidentifisert kort i loggen kan dras over
eller festes med knappen «Fest»; samme mottaker oppretter én selvstendig pinned-post.
Duplikat/ukjent rolle avslås uten å endre den lagrede listen. Originalkortet beholdes.

Commit: `94d92a1ac83e5db919a4e92180c09386242fc47b` (én commit på grenen).

Gren: `pdd/butler-widgetflate`. Worktree: `_worktrees/cellscaffold-butler-widgetflate`.
Baseline: lokal `origin/main` = `649255bb777b3a5135bd9c50512d3074bd23935b`.
`git -C CellScaffold fetch origin` ble forsøkt og feilet: `Could not resolve hostname github.com`.
Om server-main har nyere commits er ukjent. Ingen push, faktisk PR, merge, docker eller deploy.
CellScaffold-arbeidskopien står fortsatt på `pdd/tillitspakke-agentflaate` og er ikke redigert.

## Formål og avgrensning

- `purpose://candidate.pattern.detachable-surface-element.grip-and-drop` (B1).
- `purpose://candidate.pattern.detachable-surface-element.owned-and-persisted` (B2b, godkjent nattfallback).
- B4 i denne skiven: de tre bestilte action-keypathene registreres og inngår i
  `SkeletonReachabilityAudit.reachableActionKeypaths`-testen. Naturlig-språk-ruting
  av «fest programmet her» er ikke implementert.

## B0: avkreftet ved kildeinspeksjon

På baseline tar `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:1188`
alle ikke-dismissed pinned-poster inn i pinned-listen, mens `:1189` utelater dem
fra aktiv hjelper. Restore `:3430` og mutatoren `:10665` beholder pinned.
Det tilfredsstiller den bestilte kontrakten: posten forblir synlig i flaten og
beholder festingen gjennom restore. Det åpner ikke nødvendigvis aktiv hjelper
eller målcellens innhold. Filter/restore er derfor uendret.

B0-testen ble skrevet før widgetimplementeringen. Ingen test er kjørt;
en feilende test eller runtime-reproduksjon hevdes ikke. Kildelinjene i leveransen
står ved `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:1190`,
`:1191`, `:3434` og `:10700`.

## Endringer per fil

Alle baner er relative til HAVEN-roten.

| Fil | Endring |
|---|---|
| `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore+WidgetCanvas.swift` | Nye widget-actions, kildevalidering, duplikatkontroll, unpin/fullvalg, valgfri Codable-metadata og samlet canvas-/kortprojeksjon. |
| `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory+WidgetCanvas.swift` | Dra-kort med grep og Fest, kandidatbasert Flaten rundt, widgetrader, slippbindinger og tilnærmet web-layout. |
| `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalChatHubCell+WidgetCanvas.swift` | Actionregistrering med Explore-input/resultat og eksisterende validateAccess-mønster. |
| `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` | Valgfri metadata på eksisterende post, én samlet UI-projeksjonskobling, transient feedback og liten adapter til private scoped state/save med tilbakeføring ved skrivefeil. Ingen endring i drop.receive. |
| `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift` | To koblinger: loggradens componentCards og arbeidsflatens canvas-komposisjon. Eksisterende kortmodifikator gjenbrukes. |
| `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift` | Ett kall som registrerer de nye handlingene. |
| `_worktrees/cellscaffold-butler-widgetflate/Tests/AppTests/PersonalCopilotWidgetCanvasTests.swift` | Ni tester gjennom celle-set/get, faktisk state-projeksjon, diskinnlasting og produksjonsfabrikk. |
| `_worktrees/cellscaffold-butler-widgetflate/Tests/AppTests/Support/WidgetCanvasSkeletonReachabilityAudit.swift` | Navneromsavgrenset kopi av eksisterende CellProtocol-audit; begrunnelse nedenfor. |
| `_worktrees/cellscaffold-butler-widgetflate/Tests/AppTests/Fixtures/WidgetCanvas/flate.handlinger.md` | PDD-handlingskontrakten som testfixture. Bare nattens tre handlinger hevdes dekket. |
| `_worktrees/cellscaffold-butler-widgetflate/ci/test-filter.txt` | Registrerer den nye testsuiten i CI. |
| `_worktrees/cellscaffold-butler-widgetflate/Documentation/Operations/butler-widgetflate/CONTRACT.md` | Varig bindingskontrakt, B0-belegg, lagringsavvik, begrensninger og staging-steg. |

## B2b: nøyaktig hva som persisteres, og forskjellen fra CellConfiguration

Butler-kilden er ikke source-backed editable etter dagens registreringer.
`_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1347` registrerer
kun lesing av `skeletonConfiguration` fra fabrikken. PersonalChatHub mangler
library/state/apply/reset i `EditableCellConfigurationContract`, definert i
`_worktrees/cellscaffold-butler-widgetflate/Sources/App/Services/EditableCellConfigurationSupport.swift:38`.

Som uttrykkelig godkjent for denne nattskiven lagres de nye pinned-postene der
cellen allerede lagrer brukerens UI-tilstand:
`chatUIStatesByScopeID[requesterUUID:threadID].componentSurfaces`, med
`requesterUUID:default` uten tråd. Filen er
`<CellBase.documentRootPath>/PersonalCopilot/personal-copilot-cloud.json`, med den
allerede eksisterende temporaryDirectory/CellScaffoldPersonalCopilot-fallbacken
når documentRootPath mangler. Ingen ny lagring eller nettleserlagring er innført.

Belegg i `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift`:
modell `:966`, scoped kart `:1602`, dekoding `:1716`, scoped lagring `:10624`,
scope-ID `:10628`, load `:15474`, atomisk save `:15512`, lagringsbane `:15519`.
På origin/main: `:964`, `:1600`, `:1714`, `:10589`, `:10593`, `:15439`, `:15477`, `:15484`.

**Dette er ikke widgetdefinisjoner i Portholens CellConfiguration.** Det er
requester-/trådavgrenset UI-tilstand i cellens eksisterende tjenestelagring,
uten konfigurasjonsrevisjon, Porthole-ID eller propagering til denne/alle/utvalg.
Disse mål-/revisjonsfeltene er `null`; spesifikke mål avslås. Ny fysisk enhet
og synkronisering mellom tjenesteinstanser er ukjent/ikke testet.

For full B2b må PersonalChatHub få editable library/state/apply/reset med
rettighetskontroll og revisjonssjekk, etter det eksisterende mønsteret i
`_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/Chat/ChatCell.swift:258` og `:382`, koblet til
`OwnedCellConfigurationStore.persist` i
`_worktrees/cellscaffold-butler-widgetflate/Sources/App/Services/EditableCellConfigurationSupport.swift:428`.
Widgetdefinisjonenes representasjon i CellConfiguration må avklares, de
nåværende postene migreres uten tap, og Porthole-ID/skop kobles til før reload
og flerflate-/enhetstester. Dagens CellConfiguration har ikke et toppfelt
`widgets`; ingen slik formatendring innføres her.

## §5-tester skrevet (ikke kjørt)

Suite: `_worktrees/cellscaffold-butler-widgetflate/Tests/AppTests/PersonalCopilotWidgetCanvasTests.swift`.

| §5 / test | Dekning |
|---|---|
| B0 / `testPinnedSurfaceStaysVisibleAfterMinimizeAndRestore` | Faktisk open → pin → minimize → restore; én synlig pinned-post, fortsatt pinned, tom minimized-liste. |
| `test.dnd.attach` / `testDropAttachesOnceAndRefusalsDoNotChangePersistedState` | Gyldig payload via registrert action fester én post; samme payload gir «duplikat»; ukjent rolle gir avslag; poster og filbytes uendret ved avslag. |
| `testUnknownSourceAndOtherRequesterCannotPinOrUnpinOwnersCard` | Requester-avgrensning, ukjent kilde/widget og uendrede lagringsbytes. Testoppsettet bruker eksisterende debug-access-mønster; dette er ikke en resolver-/grant-sikkerhetstest. |
| `testCancelWithoutDropLeavesTheCellAndDiskUnchanged` | Lesing av drakilde uten SET gir ingen widgetmutasjon. Faktisk dragend/Escape krever nettleserprøve. |
| `test.widget.persisted` / `testWidgetAndFullSurfaceSelectionSurviveFreshStoreLoad` | Ny store leser den virkelige lagringsfilen; kilde-ID og fullvalg beholdes; unpin bevarer kilden/loggen og overlever ny lasting. Ingen mock av save/load. |
| `testLegacyPinLoadsWithoutWidgetMetadataAndRemainsASourceOnUnpin` | Gammel post uten widgetmetadata dekodes; fullvalg/unpin bevarer kildeposten. |
| `testSameTitleCanIdentifyTwoDifferentSources` | To like titler, ulike kilde-ID-er: to widgets og korrekt summary. |
| `testUnsupportedTargetAndTamperedSourceAreRefusedWithoutSaving` | Ukjent mål og endret kildemetadata avslås uten lagring. |
| Reachability / `testProductionSkeletonMakesScopedFlateActionsReachable` | pinFromDrop/unpin/toggleFullSurface finnes både i handlingsfixture og audit av produksjonsfabrikken. Tester også de faktiske drag-/drop-modifikatorene og at canvas ikke har strukturelt utilgjengelige elementer. |

Den låste CellProtocol-revisjonen i `_worktrees/cellscaffold-butler-widgetflate/Package.swift:128`,
`e03923cb2f1d5a339eaf62585ddc9dddf7750cec`, mangler SkeletonReachabilityAudit.
Teststøtten er derfor kopiert fra den eksisterende audit-kilden i CellProtocol,
commit `83de32626390928f477c47b39df4dd13ae7831e3`, uten logikkendring, men med
CellBase-import og eget navnerom for å unngå kollisjon med nattskive A.
Den kaller produksjonens SkeletonCondition-evaluator. Kopien kan fjernes når
pinnen oppdateres. Audit samler ikke dropActionKeypath; derfor finnes en synlig
Fest-knapp til samme pinFromDrop, og separate assertions kontrollerer slippbindingen.

## Utførte kontroller og kompileringsrisiko

- `xcrun swiftc -frontend -parse` på de åtte berørte Swift-filene: exit 0.
  Kun syntaks; ingen typesjekking, linking, bygg eller XCTest-kjøring.
- `bash ci/check-value-literals.sh`: exit 0. Ingen nye literaler over grensen.
  Eksisterende store literaler er beholdt for å respektere grensen om små koblingsdiff.
- `bash ci/test-suite-coverage.sh`: exit 0. Statisk testinventar:
  293 suiter, 273 i filter, 21 i unntaksfilen; dette er ikke kjørte tester eller testutfall.
- `git diff --check` / `git diff --cached --check`: exit 0.
- Audit-kopien er sammenlignet byte for byte med commitkilden etter fjerning av navnerom/importheader: lik logikk.

Ingen kjent, uløst signaturkonflikt etter kildekontroll; kompilering er fortsatt
**ukjent**. CI må særlig typekontrollere disse grensene:

1. Optional Codable/Equatable-widgetmetadata i
   `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:756`
   og `PersonalCopilotCloudStore+WidgetCanvas.swift:9`; følger eksisterende
   Codable-surface `:739` og valgfrie loggfelter i samme store, origin/main:1300.
2. Skjelett-API i
   `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory+WidgetCanvas.swift:7`,
   `:33`, `:104`: kontrollert mot **låst** CellProtocol-revisjon ovenfor,
   `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:811`
   (Text med separat modifiers-tilordning), `:1254`/`:1321` (stacks), `:1786`
   (Button/payloadKeypath), `:1937` (ScrollView med separat modifiers), `:2344`
   (Grid). Eksisterende fabrikkmønster for kort: `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:3972`;
   drakilde-mekanisme `:4009`.
3. Actionregistrering i
   `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalChatHubCell+WidgetCanvas.swift:7`
   følger låst `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell+InterceptRegistration.swift:81`
   og tilgangsmønsteret ved `_worktrees/cellscaffold-butler-widgetflate/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1634`.
   Audit-kopi og testressurs Bundle.module må også type-/ressurskontrolleres i CI.

## Ikke gjort / kjente funksjonsgrenser

Ingen levende binding (WP-B2), kildeabonnement, kildeoppdateringstid,
program-/statistikkdata eller full flate-layout (WP-B3/WP-R).
`programRows`/`statRows`/`errorFooters` er tomme, normalFooter opplyser at
kortet mangler løpende oppdatering. Fullknappen endrer bare lagret bool og etikett.
Ingen nye skjelettelementer, modifikatorer eller rendererendringer.

`dropSlots=[]`, fordi web ikke publiserer aktiv dratilstand til cellen.
Hele canvas er slippmål; dagens generiske ghost og hover-tilstand brukes.
Ingen innsettingsplassholder, sortering, før-widget-plassering, propageringsskop,
Binding-/app-paritet, naturlig-språk-ruting, Explore-runtime-manifest eller
pixel-/lastetidsaksept er levert. Tomme deler bruker 0/1-lister og ingen nye
celletilstandsbetingelser på toppnivå. Web på denne baselinen har tomlistemarkør
uten teksten «Ingen elementer» (`_worktrees/cellscaffold-butler-widgetflate/Public/js/skeleton-runtime.js:6305`),
så den eldre gaprapportens generiske tomtekst gjelder ikke denne baselinekoden.

## Slik ser Kjetil resultatet på staging senere

Forutsetning: Kjetil publiserer grenen/oppretter PR, CI blir grønn, og han følger
sin staging-flyt. Hva staging kjører nå er ukjent; ingen deploy er forsøkt.

1. Åpne **Co-Pilot Chat / Butler → Samtale** på bred webflate. **Flaten rundt**
   skal stå til høyre. Eksisterende aktiv hjelper er under chatten i venstre
   kolonne. Smal flate følger dagens adaptive Grid; dette er tilnærmet mockupen.
2. Skriv **«vi trenger avstemning»** og klikk **Åpne hjelper / Lag avstemning**
   i svaret. Ingen avstemning behøver å publiseres. Et kildekort med grep og
   **Fest** skal vises i den tilhørende loggraden.
3. Dra grepet til **Flaten rundt** og slipp: én widget, originalkortet beholdt.
   Alternativt bruk **Fest**, som sender samme payload til samme action.
4. Fest samme kort igjen: «duplikat», fortsatt én widget. Avbryt et nytt drag
   uten slipp: uendret liste. Lag to ulike kort for å kontrollere telleren.
5. Last siden på nytt med samme identitet/tråd: widgeten skal stå der.
   **⤢ / ↩** bytter bare tilstandsvalg; **✕** løsner widgeten uten å fjerne kilden.

Faktisk klikk-, drag-, reload- og layoututfall er **ukjent** før denne prøven.

## Git-bevis og leveranser

Kontrollert etter commit. Arbeidskopien `CellScaffold/` er ikke redigert.
Worktree: `_worktrees/cellscaffold-butler-widgetflate`.
PR-tekst: `HAVEN-Deploy/_handoff/NATT/PR-butler-widgetflate.md`.
Rapport: `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/handoff/widgetflate/RAPPORT.md`.
De to uttrykkelig bestilte handoff-filene er skrevet på leveransestiene; kode og
varig kontraktdokumentasjon er i den ene worktree-committen. Ingen andre filer
i dokumentasjons-/deploy-arbeidskopiene er endret av denne jobben.

`git log -1 --format='commit %H%nDate: %cI%nSubject: %s'`:

```text
commit 94d92a1ac83e5db919a4e92180c09386242fc47b
Date: 2026-09-13T23:29:01+02:00
Subject: feat(butler): widgetflate med dra-ut og feste — B0, B2b, B1 (PDD butler-traadtre-og-widgetflate)
```

`git diff origin/main --stat` (filbanene her er relative til worktreen):

```text
 .../Operations/butler-widgetflate/CONTRACT.md      | 135 ++++++++
 .../PersonalChatHubCell+WidgetCanvas.swift         |  33 ++
 .../PersonalCopilot/PersonalCopilotCells.swift     |   1 +
 .../PersonalCopilotCloudStore+WidgetCanvas.swift   | 275 ++++++++++++++++
 .../PersonalCopilotCloudStore.swift                |  47 ++-
 ...lCopilotConfigurationFactory+WidgetCanvas.swift | 126 ++++++++
 .../PersonalCopilotConfigurationFactory.swift      |  12 +-
 .../Fixtures/WidgetCanvas/flate.handlinger.md      |  22 ++
 .../PersonalCopilotWidgetCanvasTests.swift         | 302 +++++++++++++++++
 .../WidgetCanvasSkeletonReachabilityAudit.swift    | 358 +++++++++++++++++++++
 ci/test-filter.txt                                 |   4 +
 11 files changed, 1300 insertions(+), 15 deletions(-)
```

`git diff --stat`: tomt.
`git status --porcelain`: tomt — ren worktree.
`git rev-list --count origin/main..HEAD`: 1.

## Fem linjer svar

1. Levert: web-widgetflate, dra/Fest, validering, avfesting og lagret fullvalg; commit `94d92a1a`.
2. B0: avkreftet for avtalt pinned/restore-kontrakt ved kildeinspeksjon; regresjonstest skrevet først, ikke kjørt.
3. Persistens: eksisterende requester/tråd-UI i personal-copilot-cloud.json; CellConfiguration-lagring gjenstår.
4. Kontroll: syntaks og to CI-vakter gikk gjennom; ni Swift-tester skrevet; bygg, testutfall og staging er ukjent.
5. Neste eier: Kjetil publiserer/oppretter PR, lar CI bygge og kjører staging-stegene; denne jobben har ikke pushet.
