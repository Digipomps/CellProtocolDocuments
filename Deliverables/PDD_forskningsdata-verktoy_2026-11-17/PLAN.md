# PLAN — forskningsdata for studentene

Status: **til G2** (2026-11-18). G1 og G1-GUI er godkjent. Planen følger FORMAALSSPEC iterasjon 2: én arbeidspakke per bladformål, i avhengighetsrekkefølge.

Utførere: **Claude** (skycontaineren: kode, web-rendering, Playwright, Py/Go, dokumenter), **Codex** (på Macen, via køen i `/Users/kjetil/Build/Digipomps/HAVEN/_losen-queue/`), **Xcode** (Binding og CellApple på Macen, via Remote Control), **Kjetil** (roller, beslutninger, deploy via HAVEN-Deploy). Claude merger, tagger og deployer aldri. Alt som går til staging, går via en FORESPOERSEL i HAVEN-Deploy, og det er bygget og testet før det legges i køen.

Swift først i hver pakke som har Swift. Python og Go kommer etter, mot fixtures laget i Swift.

Hver pakke leveres som egen PR med egne tester. Swift-bygg og full test kjøres på Macen i en ren eksport av `origin/main` (Remote Control), fordi CellScaffold App ikke bygger i skycontaineren.

## Avhengigheter til andre PDD-er

| Fra | Hva vi trenger | Pakker som venter på det |
|---|---|---|
| `PDD_informasjonssystemer-gruppeentitet_2026-11-17` (PR #46) | Gruppeentiteten, rolle-VC `InformasjonssystemerRoleCredential` (`role` = `researcher`), og `ProvedClaimCondition` + TrustedIssuer i Py/Go | WP3, WP14 |
| `PDD_dele-dokumenter_2026-11-14` | InvitationAdmission (signert invitasjon og aksept som Agreement-vilkår) | WP17–WP19 |
| `PDD_studentflater-skeletonhjelp_2026-11-14` | Nåbarhetssjekk i Studio eller `skeleton-check` | WP11, WP13 |

Til gruppeentiteten finnes, utsteder noden forskerrollen (Kjetil som eier) med samme credential-type, slik at bare utstederen byttes senere.

## Fase 1 — katalog, persondatavurdering, anonyme samletall, visning, dashbord i onboarding

| WP | purposeRef | Hva | Utfører | Test som skal bli grønn | Leverer til §3 |
|---|---|---|---|---|---|
| WP0 | (avhengigheter §2) | Baseline: bygg og full test på ren eksport av `origin/main` i CellProtocol, CellScaffold, Binding, PyCellProtocol og GoCellProtocol. Mål hva `AdminResolverStats`, `AdminCellLifecycle` og `AdminMetricsHistory` gir på staging med Kjetils observer-rolle | Claude, Kjetil (rolle) | test.build, test.regression (baseline) | TESTRESULT.md#baseline |
| WP1 | pii-rules-table | `contract/research-pii-rules.v1.json`: fem grader (ingen, aggregert, indirekte identifiserende, direkte identifiserende, særlig kategori) × regler (svarform, minste k, oppløsning, lagringstid, eksport, krav om UiO-godkjenning). Skjema, versjonering, endring bare av eier av Informasjonssystemer. Utgangsverdi k = 5 for aggregert | Claude | test.fd.pii-regler-versjon | regeltabell |
| WP2 | pii-assessment | Vurderingsfunksjon i CellBase (Swift): tar en mal eller forespørsel med felt og forskningsspørsmål, gir grad og regler. Kvasi-identifikatorer i samme mal løfter graden. Brukes av alle celler under | Claude, Codex (bygg) | test.fd.pii-grad-gir-regler, test.fd.pii-haandheves | TESTRESULT.md#pii |
| WP3 | researcher-role | Forskerrollen som Agreement-vilkår: `ProvedClaimCondition` med `InformasjonssystemerRoleCredential`, `role` = `researcher`, pluss godtatte bruksvilkår (`LookupCondition target.research.termsAccepted`). Samme mønster som `AdminMetricsSupport.applyRoleCondition` | Claude, Codex (bygg) | test.fd.rolle-vilkaar | — |
| WP4 | catalog | `contract/research-metric-catalog.v1.json`: bare tall med kilde målt i WP0, hver med grad fra WP2. Sjekkskript | Claude | test.fd.katalog-dekker-kilder | katalog |
| WP5 | anonymous-aggregates | `ResearchAggregateCell` i CellScaffold (Swift), eid av Informasjonssystemer: leser admincellene internt, gir bare tellinger i faste bøtter, skjuler under k fra regeltabellen | Claude, Codex (bygg) | test.fd.ingen-identifikator, test.fd.k-terskel, test.fd.faste-bokter | — |
| WP6 | release-log | Utleveringslogg i samme celle | Claude | test.fd.utleveringslogg | — |
| WP7 | questionnaire-promise | Rett `QuestionnaireCampaignCell` slik at `aggregateOnly` og `pseudonymized` holdes i innsikt og eksport, med k fra regeltabellen | Claude, Codex (bygg) | test.fd.sporreskjema-synlighet | TESTRESULT.md#sporreskjema |
| WP8 | display-suppressed | Skjulte bøtter i `skeleton-runtime.js` (web) og CellApple `SkeletonView.swift` (Binding), samme datakontrakt `{value: null, suppressed: true, suppressedLabel}` | Claude (web + Swift-patch), Xcode (Binding-snapshot) | test.fd.skjult-vises | skjermbilder |
| WP9 | display | Tall-flis, opphavskort og samtykketrakt som skeleton-byggeklosser i studentguiden, rendret i web og Binding | Claude, Xcode | test.gui.parity | bilder mot G1-GUI-referansene |
| WP10 | export | `research.dataset.v2` med manifest (inkludert regelversjon); eksport fra `ResearchAggregateCell`; DatasetCell i PyResearchScaffold leser v2 | Claude (kontrakt), Codex (PyResearchScaffold på Macen) | test.fd.eksport-til-pyresearch | evidence/eksport |
| WP11 | dashboard-template | Malen «Mitt forskningsdashbord» som CellConfiguration, importert i Studio | Claude | test.fd.mal-naabar | — |
| WP12 | share-with-supervisor | Lese-Agreement for veileder på dashbordet | Claude | test.fd.deling-veileder | — |
| WP13 | onboarding | Trinnene i `KOM_I_GANG.md`, og måling med en ny testkonto | Claude, Kjetil (invitasjon) | test.fd.onboarding-tid | KOM_I_GANG, TESTRESULT.md#onboarding |
| WP14 | researcher-role (interop) | Rolle-vilkåret som fixtures i Py og Go, på porten fra PR #46 | Claude | test.fd.rolle-interop | TESTRESULT.md#interop |

## Fase 2 — spørre entitetene, lyttende aggregatorer, sverm

| WP | purposeRef | Hva | Utfører | Test |
|---|---|---|---|---|
| WP15 | request | `ResearchRequestCell` (mal, én per forespørsel): bygger, validering mot regeltabellen, forhåndsvisning av kortet | Claude, Codex (bygg) | test.fd.forespørsel-valideres |
| WP16 | request-reach | Sending til gruppemedlemmer og rekrutteringslenke | Claude | test.fd.rekkevidde |
| WP17 | entity-decides | «Forskningsforespørsler» i entiteten: kortet med Ja / Ikke nå / Aldri, i web og Binding | Claude, Xcode | test.fd.kort-viser-alt, test.fd.ja-ikke-naa-aldri |
| WP18 | consent-as-agreement | Aksepten gir kontrakt via InvitationAdmission-vilkår på entitetens forskningscelle | Claude | test.fd.opptak-via-vilkaar, test.cell.auth-negative |
| WP19 | query-at-entity | Bidraget regnes ut i entitetens celle; summen i en celle eid av Informasjonssystemer; svar bare over k | Claude | test.fd.student-ser-ikke-bidrag, test.fd.k-terskel-svar |
| WP20 | flow-aggregator | Aggregator eid av Informasjonssystemer som abonnerer på avtalte Flow-hendelser etter signContract, teller i faste bøtter, gir samletall over k | Claude, Codex (bygg) | test.fd.flow-krever-kontrakt, test.fd.flow-stopper-ved-trekk |
| WP21 | pseudonymous-rows | Pseudonym per forespørsel | Claude | test.fd.pseudonym-ukoblet |
| WP22 | withdraw | Trekk og utløp, synlig for begge parter | Claude | test.fd.trekk, test.fd.utlop |
| WP23 | swarm-behaviour | Nye `BehaviorScript`-er i `UserSimulationScaffoldCore`: invitere, svare på forespørsler, sende meldinger, lage og dele dokumenter | Claude, Codex (bygg) | test.fd.sverm-atferd |
| WP24 | swarm | Svermoppsett fra frø: studenten velger antall og atferdsmiks og kjører mot staging. Eksport i samme skjema | Claude | test.fd.sverm-samme-skjema, test.fd.sverm-reproduserbar |
| WP25 | snapshot-seed | Snapshot bare av entiteter med kontrakt og bare tillatte felt; identifikatorer byttes ut før snapshotet forlater entiteten; svermen starter fra det | Claude | test.fd.snapshot-bare-med-kontrakt, test.fd.snapshot-uten-identifikator |
| WP26 | cross-language | Swift-fixtures (forespørsel, aksept, opptak, avslag, trekk, k-terskel, flow-kontrakt), så Py og Go | Claude | test.fd.interop-fixtures |
| WP27 | root | Ende til ende med tre testkontoer og en sverm på staging, etter deploy via HAVEN-Deploy | Claude, Kjetil (deploy) | test.fd.e2e-student |

## Fase 3 — lagring hos entiteten og sterkere personvern

| WP | purposeRef | Hva | Utfører | Test |
|---|---|---|---|---|
| WP28 | entity-storage | Forskningsfelt med fast skjema i entiteten | Claude, Codex | test.fd.lagring-skjema-og-sletting |
| WP29 | privacy-stronger | Spesifikasjon av støy med budsjett og sikker summering, som mulig forskningsspørsmål | Claude | test.fd.f3-spesifisert |

## Rekkefølge og første leveranse

WP0 → WP1 → WP2 → WP3 → WP4 → WP5 → WP6, så WP7–WP14 i parallell der de ikke deler filer. Første leveranse du kan se, etter WP0–WP6 og WP8: dashbordet med ekte samletall fra staging i web og Binding, sammenlignet med `images/dashbord-fylt-*-v1.png`.

Fase 2 starter når InvitationAdmission fra `PDD_dele-dokumenter` er på main. WP20 og WP23–WP25 avhenger ikke av den og kan starte når fase 1 er levert.

## Ikke med

Deploy, merge og tagging (Kjetil, via HAVEN-Deploy). Innsamling fra ekte brukere på staging. Flere serier i samme diagram (egen oppgave hvis noen trenger det).
