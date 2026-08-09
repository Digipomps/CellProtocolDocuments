# Kallimachos W1/W2 — oppfølgings-, beslutnings- og tillitsrapport

- Dato: 2026-08-08
- Beslutningseier: Kjetil
- Omfang: svarene gitt etter W1/W2-leveransen
- Status: implementert og verifisert; staging-deploy blokkert av eksplisitte
  readiness- og runtime-porter; eksakte commit-SHA-er rapporteres ved overlevering

## Brancher, eksakte SHA-er og fillister

| Repo / leveranse | Branch | Eksakt SHA |
| --- | --- | --- |
| CellScaffold W1 original | `codex/kallimachos-v1-rung01` | `94ad40db0edc98516226a450283f97fc890d5e5e` |
| CellScaffold delt ScaffoldKit + demo + hardening, HEAD | `codex/kallimachos-arendalsuka-server-ai-demo-20260808` | `432ca14875b7df04ee5ff402e59fbb3f6447c556` |
| CellProtocolDocuments W2 benchmark | `codex/kallimachos-librarian-benchmark` | `a7dbda0bafd6def126a1b37ce2853ca946e57ae4` |
| Binding/HAVENAgentD profiler + ekte smoke, HEAD | `codex/havenagentd-kallimachos-model-profiles-20260808` | `836d656212dc0e619fa32b1c47d7def0c77d5e42` |
| CellProtocolDocuments Book-katalog | `codex/kallimachos-librarian-docs-followup-20260808` | `84a2cbeab94286f170f14eac4187cd25d5c30fe2` |

Rapportcommiten kan ikke inneholde sin egen SHA uten en sirkulær endring;
branchens eksakte endelige HEAD rapporteres derfor i overleveringsmeldingen.

Filliste, W1 original `94ad40db`:

- `Package.swift`
- `Sources/App/Cells/CommonsLibrarian/CommonsLibrarianCell.swift`
- `Sources/App/Cells/CommonsLibrarian/CommonsLibrarianCorpus.swift`
- `Sources/App/Cells/CommonsLibrarian/CommonsLibrarianModels.swift`
- `Sources/App/Cells/CommonsLibrarian/commons_corpus_sources.v1.json`
- `Sources/App/Cells/CommonsLibrarian/commons_librarian_persona.v1.json`
- `Sources/App/Cells/CommonsLibrarian/haven-figure-traits.v1.json`
- `Sources/App/configure.swift`
- `Tests/AppTests/CommonsLibrarianCellTests.swift`

Filliste, CellScaffold hardening `432ca148`:

- `Documentation/Kallimachos_Arendalsuka_Server_AI_Demo_Runbook_2026-08-08.md`
- `Public/js/porthole-webo.js`
- `Sources/App/Cells/AI/AIGatewayCell.swift`
- `Sources/ScaffoldKit/CommonsLibrarian/CommonsLibrarianCell.swift`
- `Sources/ScaffoldKit/CommonsLibrarian/CommonsLibrarianModels.swift`
- `Tests/AppTests/AIGatewayCellTests.swift`
- `Tests/AppTests/CommonsLibrarianCellTests.swift`

Filliste, W2 `a7dbda0b`:

- `Tools/CoPilotChatLanguageBenchmark/README.md`
- `Tools/CoPilotChatLanguageBenchmark/librarian_cases.no.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/librarian_contexts.v1.json`
- `Tools/CoPilotChatLanguageBenchmark/results/Kallimachos_Librarian_Benchmark_2026-08-06.md`
- `Tools/CoPilotChatLanguageBenchmark/run_llama_cli_cases.py`
- `Tools/CoPilotChatLanguageBenchmark/run_mlx_vlm_cases.py`
- `Tools/CoPilotChatLanguageBenchmark/summarize_results.py`

Filliste, AgentD live-smoke `836d6562`:

- `HavenAgentD/Docs/LocalModels.md`
- `HavenAgentD/Sources/HavenAgentCells/AgentLocalModelCell.swift`
- `HavenAgentD/Tests/HavenAgentCellsTests/AgentCellsTests.swift`

## Fokusert W1-testkjøring — kommando og full suite-output

Kommando:

```bash
CELLPROTOCOL_LOCAL_PACKAGE_PATH=/private/tmp/codex-cellprotocol-kallimachos-runtime-20260808 \
swift test --disable-sandbox --skip-update --filter CommonsLibrarianCellTests
```

Full XCTest-output for den nye testklassen, uten de forutgående
SwiftPM-kompilatorvarslene og de etterfølgende vault-debuglinjene:

```text
Test Suite 'CommonsLibrarianCellTests' started at 2026-08-08 15:31:02.994.
Test Case 'testAllAnswerLikeKeypathsReturnCompletePalazzoEnvelope' passed (0.016 seconds).
Test Case 'testAuditExportAndDeleteAreRequesterAndRelationScoped' passed (0.009 seconds).
Test Case 'testBundledManifestPersonaAndTraitVocabularyAreVersionedAndConsistent' passed (0.001 seconds).
Test Case 'testConfirmedBulkExportReturnsOnlyAuthenticatedRequestersHistoryAcrossRelations' passed (0.006 seconds).
Test Case 'testEveryCitationExcerptIsAnExactSourceFileSubstring' passed (0.004 seconds).
Test Case 'testExploreCatalogIncludesExportDeleteAndQueryFlowContracts' passed (0.008 seconds).
Test Case 'testNameDiscretionIsRoleFirstAndNarratesHistoryOnlyOncePerRelation' passed (0.004 seconds).
Test Case 'testPendingCorpusManifestReviewPropagatesToSourceBasedAnswers' passed (0.004 seconds).
Test Case 'testQueryEmitsRedactedAuditFlowAndNeverInvokesProviderOrNetworkPath' passed (0.004 seconds).
Test Case 'testRelationIDIsMandatoryAndInvalidRequestDoesNotPersistHistory' passed (0.003 seconds).
Test Case 'testRetentionPolicyIsInactiveUntilValidDaysAreConfigured' passed (0.000 seconds).
Test Case 'testSameManifestAndGitSnapshotProduceSameIndexHashAndIdenticalAnswer' passed (0.005 seconds).
Test Case 'testTimeRetentionPrunesTimestampedHistoryButDoesNotInferLegacyExpiry' passed (0.006 seconds).
Test Case 'testUnknownTopicReturnsHonestGapAndIncrementsDemandWithoutCitation' passed (0.004 seconds).
Test Suite 'CommonsLibrarianCellTests' passed at 2026-08-08 15:31:03.070.
    Executed 14 tests, with 0 failures (0 unexpected) in 0.075 (0.076) seconds
```

Supplerende porter:

| Kontroll | Eksakt resultat |
| --- | --- |
| AIGateway proof-bearing lifecycle-flow | 1 test, 0 feil, 0,009 s |
| Kallimachos demo uten live-guard | 5 kjørt, 4 bestått, 1 eksplisitt skip, 0 feil, 0,047 s |
| Ekte Qwen demo-cell | 1/1 bestått; AIGateway 2 224 ms i den fokuserte Cell-testen |
| Chromium/Porthole | 1/1 bestått, 19,5 s; kald AIGateway-generering 11 536 ms |
| HAVENAgentD full pakke | 147 tester i 32 suites, 0 feil, 4,101 s |
| Ekte AgentD Qwen / Gemma | 1/1 på 1,776 s / 1/1 på 3,324 s |
| Docs MCP | 7 tester, 0 feil, 0,059 s; begge Book-resurser listet og søkbare |

## Korpusmanifest — include/exclude-review

Reviewstatus er `approved` etter Kjetils uttrykkelige svar. Manifestet bruker
kun Git-trackede filer og beholder Deliverables som `public-review-required`.

| Include | Audience |
| --- | --- |
| `Book/**/*.md` | `public` |
| `Deliverables/**/*.md` | `public-review-required` |
| `Deliverables/**/*.txt` | `public-review-required` |

| Exclude | Begrunnelse |
| --- | --- |
| `Backups/**` | backups er aldri offentlig korpus |
| `**/*handoff*`, `**/*handover*` | interne overleveringer krever publiseringsbeslutning |
| `**/*panel*`, `**/round*/**`, `**/brieftest/**` | panel-/mellomartefakter er arbeidsmateriale |
| `**/*credential*`, `**/*secret*`, `**/.env*` | credential-, secret- og miljøfiler ekskluderes konservativt |
| `**/*private*` | eksplisitt privatmerkede filer er aldri korpuskilder |

Dette reviewpunktet er lukket for v1. En ny include-pattern eller oppmykning av
eksklusjonene krever en ny eksplisitt beslutning; `approved` er ikke en generell
påstand om at alt fremtidig innhold under Deliverables er offentlig.

## Fire komplette konvolutteksempler

Eksemplene under er generert av den fokuserte syntetiske test-fixturen. De
viser norsk gap, engelsk katalogtreff og en navnesekvens i samme relasjon.

### 1. Engelsk eksakt overskriftstreff — `Deterministic catalog`

```json
{
  "answer": "The librarian in HAVEN found these verbatim catalogue excerpts:\n\n«Deterministic catalog»: ## Deterministic catalog\n\nThe same corpus snapshot produces the same deterministic index and exact source excerpts.",
  "answer_id": "sha256:e1ee1eddede1d5a63078830a2023d44afc2457d96d80849177144bc37c2bdf55",
  "audience": "requester",
  "citations": [
    {
      "content_sha256": "a9daef5f9421aa1c66a2ba29f049fa8e82956540e2d7bbc1a5c1d2f6e27fcf3d",
      "excerpt": "## Deterministic catalog\n\nThe same corpus snapshot produces the same deterministic index and exact source excerpts.",
      "last_verified": "2026-08-05T10:00:00Z",
      "section": "Deterministic catalog",
      "source_id": "commons-doc:cb69b348a93d3961",
      "source_path": "Book/10_Quickstart.md",
      "source_type": "git-head-document",
      "title": "Quickstart"
    }
  ],
  "confidence": "high",
  "contract_version": "haven.commons-librarian.v1",
  "corpus_version": "fixture-v1",
  "index_hash": "9224b95d2f97ff8e94f02464e9cd850bf87a6727bdbd4119a44d8831c02655d0",
  "last_verified": "2026-08-05T10:00:00Z",
  "needs_human_review": false,
  "records": [
    {
      "exact_heading_match": true,
      "score": 11210,
      "section": "Deterministic catalog",
      "source_path": "Book/10_Quickstart.md"
    }
  ],
  "route": "exact-heading"
}
```

### 2. Norsk gap — `kvantebananbibliografi 9000`

```json
{
  "answer": "Bibliotekaren i HAVEN: Det har jeg ikke i katalogen ennå.",
  "answer_id": "sha256:b4bedbfb2fec533f13a41c41a47a64083ad86d774728c2d38e14273ee3dce184",
  "audience": "requester",
  "citations": [],
  "confidence": "low",
  "contract_version": "haven.commons-librarian.v1",
  "corpus_version": "fixture-v1",
  "index_hash": "9224b95d2f97ff8e94f02464e9cd850bf87a6727bdbd4119a44d8831c02655d0",
  "last_verified": "2026-08-05T10:00:00Z",
  "needs_human_review": false,
  "records": [],
  "route": "catalog-gap"
}
```

### 3. Første norske navnespørsmål i `chat-1`

```json
{
  "answer": "Jeg heter Kallimachos — etter bibliotekaren i Alexandria som laget den første katalogen. Jeg prøver å leve opp til Pinakes.",
  "answer_id": "sha256:faffdccf45e8092be5c2df46960e827891ab021c352786add33cc12c9589f2a8",
  "audience": "requester",
  "citations": [
    {
      "content_sha256": "578d8be82df562917e082b4752c469be9e738a7aba77a28aa57ad58866c0c088",
      "excerpt": "Jeg heter Kallimachos — etter bibliotekaren i Alexandria som laget den første katalogen. Jeg prøver å leve opp til Pinakes.",
      "last_verified": "2026-08-05",
      "section": "nameHistory.nb",
      "source_id": "commons-persona:578d8be82df56291",
      "source_path": "bundle://commons_librarian_persona.v1.json",
      "source_type": "versioned-configuration",
      "title": "CommonsLibrarianPersona"
    }
  ],
  "confidence": "high",
  "contract_version": "haven.commons-librarian.v1",
  "corpus_version": "fixture-v1",
  "index_hash": "9224b95d2f97ff8e94f02464e9cd850bf87a6727bdbd4119a44d8831c02655d0",
  "last_verified": "2026-08-05",
  "needs_human_review": false,
  "records": [
    {
      "history_told_now": true,
      "relation_id": "chat-1",
      "role": "bibliotekaren i HAVEN"
    }
  ],
  "route": "direct-name-history"
}
```

### 4. Andre norske navnespørsmål i samme `chat-1`

```json
{
  "answer": "Jeg heter Kallimachos.",
  "answer_id": "sha256:19ad8e67dfa07116d91c28651d2b167840addb40ad4746ec17103889eea326d2",
  "audience": "requester",
  "citations": [
    {
      "content_sha256": "578d8be82df562917e082b4752c469be9e738a7aba77a28aa57ad58866c0c088",
      "excerpt": "Jeg heter Kallimachos — etter bibliotekaren i Alexandria som laget den første katalogen. Jeg prøver å leve opp til Pinakes.",
      "last_verified": "2026-08-05",
      "section": "nameHistory.nb",
      "source_id": "commons-persona:578d8be82df56291",
      "source_path": "bundle://commons_librarian_persona.v1.json",
      "source_type": "versioned-configuration",
      "title": "CommonsLibrarianPersona"
    }
  ],
  "confidence": "high",
  "contract_version": "haven.commons-librarian.v1",
  "corpus_version": "fixture-v1",
  "index_hash": "9224b95d2f97ff8e94f02464e9cd850bf87a6727bdbd4119a44d8831c02655d0",
  "last_verified": "2026-08-05",
  "needs_human_review": false,
  "records": [
    {
      "history_told_now": false,
      "relation_id": "chat-1",
      "role": "bibliotekaren i HAVEN"
    }
  ],
  "route": "direct-name-short"
}
```

## Formål

| Formål | Begrunnelse |
| --- | --- |
| `purpose://knowledge` | Kallimachos skal være en delt, kildebevisst bibliotekarimplementasjon med deterministisk trinn 0–1. |
| `purpose://access.audit.privacy` | Requesteren skal kunne eksportere og slette egen rå spørre- og svarhistorikk uten tilgang til andres historikk. |
| `purpose://grounding.local-model-assisted-decomposition` | De lokalt testede Qwen3/Gemma-rutene skal ha stabile AgentD-identifikatorer uten å gjøre modellen til policyautoritet. |

## Goals

| Goal | Målbar terminaltilstand | Status | Evidens |
| --- | --- | --- | --- |
| G1 | `CommonsLibrarianCell` eies av ScaffoldKit; `relation_id` er obligatorisk for katalogspørring; relasjons- og requester-bulkeksport, bekreftet sletting og opt-in TTL har komplette Explore-kontrakter og fokuserte tester. | complete | `swift test --disable-sandbox --skip-update --filter CommonsLibrarianCellTests`: 14 tester, 0 feil. |
| G2 | HAVENAgentD kjenner stabile Qwen3-8B- og Gemma 4 E4B-profiler og kan kjøre ekte Cell-smoke mot begge loopback-runtimeene. | complete | Full HAVENAgentD-pakke: 147 tester i 32 suites, 0 feil. Ekte opt-in smoke: Qwen 1/1 og Gemma 1/1. |
| G3 | Manifestbeslutningen og de to kanoniske Kallimachos-dokumentene er i dokumentrepoet, og dokumentene har egne `Book/book_catalog.json`-poster. | complete | JSON-validering, Docs MCP resource-listing og Kallimachos-søk bestått. |
| G4 | Arendalsuka-flaten bruker lokal server-AI uten modellpolicy, owner-proof-diagnostikken er rettet og brukerflyten er kjørt i Chromium. | complete lokalt | Chromium 1/1; ekte Qwen; citation og sletting; ingen owner-proof-diagnostikk. |
| G5 | Samme flyt er deployet og bestått på valgt stagingvert. | blocked | `/health/ready` er 503; containeren har ikke modellruntime på appens eksakte loopback `127.0.0.1:8083`; godkjent atomisk deployartefakt mangler. |

## Bindende beslutninger fra Kjetil

| ID | Beslutning | Implementert konsekvens |
| --- | --- | --- |
| D1 | Include/exclude-manifestet godkjennes, og panelartefakter forblir ekskludert. | `reviewStatus` settes til `approved`; eksisterende panel-/handoff-eksklusjoner beholdes; `reviewQuestions` tømmes. |
| D2 | Wire lokale modeller nå. | To kjente AgentD-profiler legges til med stabile profil- og provider-ID-er; begge forblir merket eksperimentelle for produktbruk. |
| D3 | Flytt `CommonsLibrarianCell` til ScaffoldKit. | Swift-kode og versjonerte ressurser flyttes til ScaffoldKit-target; App beholder bare resolver-registreringen. |
| D4 | Eksport og sletting av spørrehistorikk skal implementeres. | `librarian.audit.export` og `librarian.audit.delete` legges til som requester- og relasjonsavgrensede SET-handlinger. |
| D5 | `relation_id` er obligatorisk. | Explore-skjema og runtime avviser katalogspørring uten ikke-tom `relation_id`; avvist spørring lagres ikke. |
| D6 | `8083` er kanonisk Qwen-port. | Demo- og AgentD-profil bruker `127.0.0.1:8083`. |
| D7 | Requesteren skal kunne eksportere alle egne relasjoner uten persondatalekkasje. | Ny, eksplisitt bekreftet `librarian.audit.export_all`; caller kan ikke velge requester-ID; negative isolasjonstester. |
| D8 | Historikken skal ha tidsbasert TTL. | Opt-in policy er implementert med `COMMONS_LIBRARIAN_AUDIT_TTL_DAYS`; dagtall er fortsatt åpent og ingen verdi er antatt. |
| D9 | Kallimachos-dokumentene skal inn i Book-katalogen. | To egne katalogposter peker på de kanoniske Deliverables uten å duplisere innhold. |
| D10 | Ekte AgentD-smoke skal kjøres mot både Qwen og Gemma. | Opt-in Cell-smoke tester `llm.health` og `llm.generate`; begge er kjørt mot ekte lokale runtimes. |
| D11 | Qwen og direkte `llama-server` er enklest for første publikumsdemo. | Porthole-demoen bruker den eksakte lokale Qwen-ruten; AgentD-smoken er separat bevis, ikke demoens prosesseier. |
| D12 | Staging er valgt demovert. | Vert er probet read-only; deploy er ikke utført mens readiness og modelltopologi er røde. |
| D13 | Kjetil er primæroperatør; Vegar er foreslått reserve. | Kjetil er ført som eier; Vegars aksept står som åpent spørsmål, ikke som faktum. |
| D14 | Screenshots skal være lokale/regenererbare. | `test-results/` committes ikke. |
| D15 | Owner-proof-diagnostikken må fikses. | `AIGatewayCell` beholder autentisert, proof-bearing requester ved flow-emisjon; målrettet test og Chromium-flyt består. |

## Claim graph summary

### C1 — delt implementasjon

- Claim: `CommonsLibrarianCell` bør eies av ScaffoldKit.
- Type: project capability / normative, assertive.
- Premisser: App er allerede avhengig av ScaffoldKit; resolverregistrering trenger bare en offentlig celletype og kontrakt; ressursene kan eies av ScaffoldKit-bundlen.
- Counterargument: flyttingen øker ScaffoldKit-targetens omfang og gjør admin-plane-eksporten avhengig av bibliotekarressursene.
- Steelman: en egen mindre pakke kunne gitt skarpere avhengighetsgrense enn ScaffoldKit.
- Adjudication: beslutningen er bindende. Begge Package.swift-manifestene får eksplisitte ressurser slik at ingen host får en skjult Bundle-feil.
- Støtter: G1.

### C2 — requester- og relasjonsavgrenset personvernhandling

- Claim: datatilgang må alltid utledes fra autentisert requester; sletting og
  relasjonseksport krever eksplisitt relasjon, mens requester-bulkeksport er en
  separat bekreftet handling som ikke tar requester-ID fra payload.
- Type: privacy/design, assertive.
- Premisser: historikken inneholder rå spørsmål; navnehistorikk og auditposter er allerede knyttet til `relationID`; D5 gjør relasjon eksplisitt.
- Counterargument: en «eksporter alt»-handling er enklere for dataportabilitet.
- Steelman: komplett requester-eksport er nødvendig for dataportabilitet, men må ikke la payload velge en annen identitet.
- Adjudication: relasjonseksport beholdes. Den separate bulkhandlingen krever `confirm: true`, slår opp historikk kun under den autentiserte requesterens UUID og returnerer ingen rå poster uten bekreftelse. Sletting forblir eksplisitt relasjonsavgrenset.
- Støtter: G1 og `purpose://access.audit.privacy`.

### C3 — stabil rute, eksperimentell modell

- Claim: stabil AgentD-identitet kan wires uten å hevde at modellen er stabil produktpolicy.
- Type: architecture/project capability, moderated.
- Premisser: W2 kjørte begge lokale runtimes, men ikke AgentD; AgentD støtter allerede profiler, loopback-gate og miljøoverstyring; Gemma-serveren krever maskinlokal modellsti.
- Counterargument: en profil som trenger miljøoverstyring er ikke fullstendig nullkonfigurasjon.
- Steelman: AgentD kunne senere eie en installasjons-/modellsti-resolver, men det er utenfor denne endringen.
- Adjudication: profil/provider-ID og porter er stabile; `isExperimental` beholdes; Gemma-sti leveres gjennom eksisterende miljøvariabel og committes ikke. Ekte AgentD Cell-smoke har bestått for begge modeller.
- Støtter: G2.

### C4 — lokal verifikasjon er ikke staging-verifikasjon

- Claim: demoen kan ikke kalles staging-klar før app-containeren både er ready og kan nå den eksakt allowlistede loopback-modellen.
- Type: operations/security, assertive.
- Premisser: staging returnerer HTTP 503 fra `/health/ready`; dagens app-container deler ikke vertens loopback; den eldre deployveien er fail-closed; atomisk v3 krever godkjente releaseartefakter.
- Counterargument: den lokalt beståtte Qwen-flyten viser at applikasjonskoden virker.
- Steelman: lokal flyt er sterk funksjonell evidens, men den beviser ikke container-nettverk, restore eller staging-readiness.
- Adjudication: ingen deploy ble forsøkt. G5 er blokkert og blir ikke omdefinert til complete.

## Brief audit

### Verifiserte fakta

- W1-committen registrerer `CommonsLibrarianCell` i to resolver-oppsett i `Sources/App/configure.swift`.
- ScaffoldKit er et target og produkt i samme CellScaffold-pakke; App er direkte avhengig av targetet.
- Historikk lagres i `CommonsLibrarianPersistedState.auditRecordsByRequester`, avgrenset med requester-UUID og maksimalt 500 poster per requester.
- Eksisterende AgentD-kode avviser ikke-loopback backend som standard og tillater eksplisitt miljøoverstyring av profil, provider, URL og modell.
- W2-rapporten dokumenterer benchmarkruntimene Qwen3 53/72 og Gemma 56/72. Den opprinnelige benchmarken brukte ikke AgentD; den nye separate Cell-smoken har senere kjørt begge modellene gjennom AgentD.
- Staging `/health/build` rapporterte app-revisjon `9da79bc788240b56fd5b10b206fad3cf62b165f2`; `/health/ready` svarte 503 med `arendalsuka_canonical_atlas_unavailable` og `typed_restore_published_read_agreement_unavailable`.

### Bindende regler

- D1–D15 over er beslutninger fra Kjetil, ikke utledede fakta. D13 skiller
  uttrykkelig mellom Kjetil som bekreftet primæroperatør og Vegar som foreslått
  reserve uten bekreftet aksept.
- Ingen modell skal eie kildevalg, gap-policy, sletting, autorisasjon eller annen deterministisk policy.
- Ingen modellsti, modellvekt, venv, credential eller generert korpusindeks committes.

### Vurderinger og begrensninger

- Requester-avgrensningen er applikasjonslogikk i tillegg til resolverens Agreement-sjekk; testen bruker en annen requester under tillatt direkte testtilgang for å bevise at lagringsnøkkelen ikke lekker.
- «Stabil profil» betyr stabil ruteidentitet, ikke produksjonsgodkjent modellkvalitet.
- Sletting dekker rå auditposter, avledede gap-tellere og relasjonens navnenarrasjonstilstand. Den skriver ikke en ekstern eller Entity-basert kvittering.

## Personal-data trust package

### Data og formål

- Datakategori: rå katalogspørsmål, relasjons-ID, deterministiske svar, citations og avledede gap-tellere.
- Formål: etterprøvbar katalogdialog og requesterens egen eksport/sletting.
- Requester/decision basis: Kjetil har godkjent funksjonen; hver konkret sletting krever fortsatt callerens uttrykkelige `confirm: true`.

### Dataflyt

```text
requester -> resolver/Agreement -> CommonsLibrarianCell
          -> requester UUID + relation_id -> persistent Cell state
          -> export response tilbake til samme autoriserte requester
          -> delete muterer bare samme requester + relation og gir receipt
```

- Runtime gjør ingen modell- eller nettverkskall i trinn 0–1.
- Export returnerer data i Cell-responsen; den skriver ingen fil og gjør ingen ekstern disclosure.
- Flow-hendelsen for katalogsvar inneholder ikke rå query- eller answer-tekst.

### Lagring og retention

- Lagringssted: persistent Cell state, ikke Entity og ikke ekstern tjeneste.
- Grense: 500 auditposter og 200 gap-emner per requester.
- Eksport: enten én eksplisitt relasjon eller, etter `confirm: true`, alle relasjoner for den autentiserte requesteren; rå spørsmål og registrerte svar følger med.
- Sletting: én requester + én eksplisitt relasjon; gap-tellere bygges på nytt fra gjenværende poster.
- Tidsretention: implementert, men inaktiv inntil et eksplisitt dagtall settes. Timestampede poster eldre enn policyen prunes; eldre legacy-poster uten timestamp slettes aldri ved antakelse.

### Autorisasjon og isolasjon

- Leseflater krever `r---`; handlinger krever `-w--`.
- Alle handlere kaller `validateAccess` før tilstand leses eller muteres.
- Ingen eksport- eller slettepayload kan velge en annen requester-ID; ukjente `requester_id`-felt ignoreres og er ikke del av Explore-skjemaet.
- En annen requester med samme `relation_id` får null poster og kan ikke slette eierens poster.

### Kvittering og disclosure

- Sletting returnerer `haven.commons-librarian-deletion-receipt.v1` med relasjon, antall slettede/gjenværende poster, narrasjonstilstand og SHA-256.
- `external_disclosure=false` inngår i eksportmetadata og slettekvittering.
- Ingen ekstern recipient, jurisdiksjon, DPA eller provider er involvert i runtime-operasjonene.

## Decision log

| Dato | Beslutning/handling | Eier | Resultat |
| --- | --- | --- | --- |
| 2026-08-05 | W1/W2-handoff og opprinnelige constraints. | Kjetil | W1/W2 levert i separate commits. |
| 2026-08-08 | D1–D5 bekreftet. | Kjetil | Oppfølgingsimplementasjon startet i tre rene worktrees. |
| 2026-08-08 | D6–D15 bekreftet eller avgrenset i oppfølgingssvar. | Kjetil | Port/runtime/vert/operatørvalg registrert; ubekreftet reserve og manglende TTL-dager holdes åpne. |
| 2026-08-08 | Personvernminimum for destructive action. | Implementasjon under Kjetils D4/D5 | Relasjonsscope + `confirm: true` + deterministisk receipt. |
| 2026-08-08 | Fokusert CellScaffold-verifikasjon. | Codex | 14/14 `CommonsLibrarianCellTests` og 1/1 owner-proof-regresjon bestått. |
| 2026-08-08 | Full og ekte AgentD-verifikasjon. | Codex | 147 tester bestått; ekte Qwen- og Gemma-smoke bestått med syntetiske prompts. |
| 2026-08-08 | Funksjonell publikumsflyt. | Codex | Chromium/Porthole 1/1 med ekte Qwen, citation og bekreftet sletting; ingen owner-proof-advarsel. |
| 2026-08-08 | Read-only staging-port. | Codex | Build-endepunkt svarer; readiness er 503. Deploy ikke utført. |

## W2 score-tabell og anbefaling

| Modell | Total | Middel/median per case | Eksakt sitatfidelitet |
| --- | ---: | ---: | ---: |
| Qwen3-8B Q4_K_M (GGUF/CPU) | 53/72 (73,6 %) | 42,552 / 42,326 s | 1/3 (33,3 %) |
| Gemma 4 E4B QAT (MLX/VLM/Metal) | 56/72 (77,8 %) | 14,621 / 13,814 s | 3/3 (100 %) |

| Dimensjon | Qwen3-8B | Gemma 4 E4B QAT |
| --- | ---: | ---: |
| Intent | 3/12 (25,0 %) | 5/12 (41,7 %) |
| Action | 11/12 (91,7 %) | 12/12 (100 %) |
| Clarification | 11/12 (91,7 %) | 10/12 (83,3 %) |
| Safety | 10/12 (83,3 %) | 10/12 (83,3 %) |
| Must mention | 7/12 (58,3 %) | 7/12 (58,3 %) |
| Must not mention | 11/12 (91,7 %) | 12/12 (100 %) |

W2-anbefalingen står: Gemma er første kandidat for en senere, avgrenset
formulerings-/oppsummeringsrung fordi den ledet denne lille kjøringen og hadde
3/3 eksakte sitater. Qwen brukes i Arendalsuka-demoen fordi Kjetil valgte den
enkleste direkte runtimeveien; dette er et driftsvalg, ikke en omgjøring av
benchmarkens kvalitetsanbefaling. Kildevalg, gap, invitasjonsminne, sitatsjekk
og autorisasjon forblir deterministisk utenfor modellen.

## Åpne spørsmål til Kjetil

1. Hvor mange dager skal `COMMONS_LIBRARIAN_AUDIT_TTL_DAYS` være på staging? Ingen verdi er antatt; policyen er inaktiv uten et eksplisitt heltall 1–3650.
2. Bekrefter Vegar at han er reserveoperatør med ansvar for modelloppvarming, helsesjekk, restart og sletting mellom publikumssesjoner?
3. Hvilken godkjent staging-topologi skal gi app-containeren eksakt loopback-tilgang til Qwen på 8083, og hvem leverer den eiergodkjente opaque-preservation-hashen for atomisk deploy?

Spørsmål 1–3 blokkerer stagingkonfigurasjon/deploy, men ikke de lokalt
verifiserte leveransene. De er ikke behandlet som stille prosjektfakta.
