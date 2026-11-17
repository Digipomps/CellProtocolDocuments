# PLAN (utkast) — forskningsdata for studentene

Status: **utkast, ikke til godkjenning ennå.** Kjetil ba om en plan; den ligger her slik at han ser omfanget. G2 bes om etter G1 og G1-GUI, og planen justeres etter svarene i FORMAALSSPEC §6.

Utførere: **Claude** (skycontaineren: kode, web-rendering, Playwright, Py/Go, dokumenter), **Codex** (på Macen, via køen i `/Users/kjetil/Build/Digipomps/HAVEN/_losen-queue/`), **Xcode** (Binding og CellApple på Macen, via Remote Control), **Kjetil** (roller, beslutninger, deploy via HAVEN-Deploy). Claude merger, tagger og deployer aldri. Staging går via en FORESPOERSEL i HAVEN-Deploy, og alt i køen er bygget og testet først.

Swift først i hver pakke som har Swift. Python og Go kommer etter, mot Swift-fixtures.

## Fase 1 — katalog, anonyme samletall, visning, dashbord i onboarding

| WP | purposeRef | Hva | Utfører | Test som skal bli grønn | Leverer til §3 |
|---|---|---|---|---|---|
| WP0 | (avhengigheter §2) | Baseline: bygg og full test på ren eksport av `origin/main` i CellProtocol, CellScaffold, Binding, PyCellProtocol, GoCellProtocol. Mål hva `AdminResolverStats`, `AdminCellLifecycle` og `AdminMetricsHistory` gir på staging med Kjetils observer-rolle | Claude + Kjetil (rolle) | test.build, test.regression (baseline) | TESTRESULT.md#baseline |
| WP1 | catalog | `contract/research-metric-catalog.v1.json` + skjema + sjekkskript. Bare tall med kilde som finnes i koden (WP0) | Claude | test.fd.katalog-dekker-kilder | katalog |
| WP2 | researcher-role | `ResearcherCredential` + bruksvilkår som Agreement-vilkår, samme mønster som `AdminMetricsSupport.applyRoleCondition`. Utstedelse via invitasjon fra noden. Swift i CellScaffold | Claude (kode), Codex (Mac-bygg) | test.fd.rolle-vilkaar | — |
| WP3 | anonymous-aggregates | `ResearchAggregateCell` i CellScaffold (Swift): leser admincellene internt, gir bare tellinger i faste bøtter, merker under k som skjult | Claude, Codex (bygg) | test.fd.ingen-identifikator, test.fd.k-terskel, test.fd.faste-bokter | — |
| WP4 | release-log | Utleveringslogg i samme celle | Claude | test.fd.utleveringslogg | — |
| WP5 | questionnaire-promise | Rett `QuestionnaireCampaignCell` slik at synligheten holdes i innsikt og eksport | Claude, Codex (bygg) | test.fd.sporreskjema-synlighet | TESTRESULT.md#sporreskjema |
| WP6 | display-suppressed | Skjulte bøtter i `skeleton-runtime.js` (web) og CellApple `SkeletonView.swift` (Binding), med samme datakontrakt | Claude (web + Swift-patch), Xcode (Binding-snapshot) | test.fd.skjult-vises | skjermbilder |
| WP7 | display | Tall-flis, opphavskort og samtykketrakt som skeleton-byggeklosser (vanlige elementer) i studentguiden | Claude | test.gui.parity | bilder |
| WP8 | export | `research.dataset.v2` med manifest; eksport fra `ResearchAggregateCell`; DatasetCell i PyResearchScaffold leser v2 | Claude (kontrakt, Py), Codex (PyResearchScaffold på Macen) | test.fd.eksport-til-pyresearch | evidence/eksport |
| WP9 | dashboard-template | Malen «Mitt forskningsdashbord» som CellConfiguration, importert i Studio | Claude | test.fd.mal-naabar | — |
| WP10 | share-with-supervisor | Lese-Agreement for veileder på dashbordet | Claude | test.fd.deling-veileder | — |
| WP11 | onboarding | Trinn i `KOM_I_GANG.md` + måling med ny testkonto | Claude, Kjetil (invitasjon) | test.fd.onboarding-tid | KOM_I_GANG, TESTRESULT.md#onboarding |
| WP12 | researcher-role (interop) | Rolle-vilkår som fixtures i Py og Go | Claude | test.fd.rolle-interop | TESTRESULT.md#interop |

Avhengighet: WP9–WP11 trenger nåbarhetssjekken fra `PDD_studentflater` (WP «studio-audit» eller `skeleton-check`).

## Fase 2 — spørre entitetene (N2, N3)

Avhenger av InvitationAdmission fra `PDD_dele-dokumenter` (G1 venter).

| WP | purposeRef | Hva | Utfører | Test |
|---|---|---|---|---|
| WP13 | request | `ResearchRequestCell` (mal, en per forespørsel): bygger, validering, forhåndsvisning av kortet | Claude, Codex (bygg) | test.fd.forespørsel-valideres |
| WP14 | request-reach | Sending til gruppemedlemmer og rekrutteringslenke | Claude | test.fd.rekkevidde |
| WP15 | entity-decides | «Forskningsforespørsler» i entiteten: kort, Ja / Ikke nå / Aldri, web og Binding | Claude, Xcode | test.fd.kort-viser-alt, test.fd.ja-ikke-naa-aldri |
| WP16 | consent-as-agreement | Aksept gir kontrakt via InvitationAdmission-vilkår på entitetens forskningscelle | Claude | test.fd.opptak-via-vilkaar, test.cell.auth-negative |
| WP17 | query-at-entity | Bidrag regnes i entitetens celle; samling i nodeeid celle; svar bare over k | Claude | test.fd.student-ser-ikke-bidrag, test.fd.k-terskel-svar |
| WP18 | pseudonymous-rows | Pseudonym per forespørsel | Claude | test.fd.pseudonym-ukoblet |
| WP19 | withdraw | Trekk og utløp, synlig for begge | Claude | test.fd.trekk, test.fd.utlop |
| WP20 | cross-language | Swift-fixtures, så Py og Go | Claude | test.fd.interop-fixtures |
| WP21 | root | Ende til ende med tre testkontoer på staging, etter deploy via HAVEN-Deploy | Claude, Kjetil (deploy) | test.fd.e2e-student |

## Fase 3 — lagring, syntetisk populasjon, sterkere personvern

| WP | purposeRef | Hva | Utfører | Test |
|---|---|---|---|---|
| WP22 | entity-storage | Forskningsfelt med fast skjema i entiteten | Claude, Codex | test.fd.lagring-skjema-og-sletting |
| WP23 | synthetic | Generator for syntetiske entiteter (Python først, for tema B), samme skjema | Claude | test.fd.syntetisk-samme-skjema |
| WP24 | privacy-stronger | Spesifikasjon av støy med budsjett og sikker summering, som mulig forskningsspørsmål | Claude | test.fd.f3-spesifisert |

## Det som ikke er med

Deploy, merge og tagging (Kjetil, via HAVEN-Deploy). Innsamling fra ekte deltakere (etter §6 spørsmål 1). Flere serier i samme diagram (egen oppgave hvis noen trenger det).
