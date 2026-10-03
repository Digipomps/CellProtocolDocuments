# Formålsspesifikasjon — spor AI-opprettede filer i eksisterende graf

HD-0154 · 2026-10-01 · P0/P1 godkjent av Kjetil 2026-10-02 (G1). Dette er spesifikasjon og kildebevis; automatisk filsporing er ikke implementert.

## 0. Intensjon (ordrett) og brief-audit

> Er det på laptop eller verten det mangler plass på? Vi må få opp en bedre måte å ha oversikt over hvilke filer og mapper AI modellene oppretter så vi kan få bedre rydderutiner og, som vi har snakket om, bruke bruke graph databasen vi har implementert.

| Påstand / kapabilitet | Audit | Kilde og konkret grense |
|---|---|---|
| Både laptop og vert ligger under relevante marginer | retrieved | evidence/capacity.json; Mac 48,1 GiB, vertens rot 35,1 GiB. Docker på verten ligger på eget filsystem. |
| Eksisterende grafdatabase kan gjenbrukes | retrieved | CellScaffold lokalt origin/main fdcfe7a566ae4e73febbba464edb190e9e9cea08: GraphStoreCell, GraphStoreNodeRow, GraphStoreEdgeRow, CreateGraphStoreTables. Autoriserte node/edge-upserts og Workbench-import finnes. |
| Eksisterende graf er aktiv og tilgjengelig i denne økten | unavailable | agent_workbench_targets feilet med Transport closed. Ingen innlasting eller privat graph-lesing ble utført. |
| Jobber har opphav og resultatfelt | retrieved | HavenAgentD lokalt origin/main ea558ba1af63caa48cd76253ea1cb588f37aa084: AgentJobModels har originator, workspacePath, purpose, execution.artifactPaths og completion.artifacts. Det beviser ikke all filopprettelse. |
| Første filgraf er implementert som automatisk sporing | contradicted | Forrige manuelle metadataoversikt har 154 noder/145 kanter og flaggene automaticTrackingImplemented=false/workbenchImported=false. |
| GraphStore tåler krasj i enhver skrivning | unavailable | persistSnapshotToSQLiteIfNeeded sletter og oppretter rader uten eksplisitt transaksjon i den leste funksjonen. Krever feilinjeksjon/atomisitetsbevis før den brukes som grunnlag for ryddebeslutninger. |

Stier i kildetabellen er HAVEN-relative. Eksakte revisjoner/blob-hasher og diskkommandoer er bevart i evidence/.

## 1. Formålstre

Kanoniske foreldre er lest fra Book 23; de nye bladene er lokale kandidater og endrer ikke kanon.

| purposeRef | Tittel | Forelder | Goal (outcome og signal) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://project-work.overview-and-sharing | Oversikt over arbeidets filer og kostnad | purpose://digital-work.coordinate | Kjetil finner hva en valgt jobb opprettet, hvor det ligger, hvor mye plass det tar og hvorfor det fortsatt beholdes. | Aksept: fra jobb til fil og tilbake på Mac og vert. | gjenbrukt, oppgavespesifikt mål |
| purpose://candidate.ai-filproveniens.capture | Opphav registreres når filen opprettes | purpose://project-work.overview-and-sharing | Alle opprettede artefakter i registrerte jobbområder har host, volume, jobb, agent/samtale, prosjekt, formål og bevis; avvik/ukjent dekning er synlig. | test.provenance.capture | candidate |
| purpose://candidate.ai-filproveniens.graph | Relasjoner finnes i eksisterende GraphStore | purpose://project-work.overview-and-sharing | Jobb–artefakt–prosjekt–bruker/avhengighet kan traverseres; samme hendelse gir ingen dubletter og eldre hendelser overskriver ikke nyere tilstand. | test.provenance.replay | candidate |
| purpose://candidate.ai-filproveniens.retention | Rydding styres av livsløp og avhengigheter | purpose://project-work.overview-and-sharing | Avsluttet jobb, utløpt bevaring og fravær av aktive referanser gir en begrunnet ryddekandidat; ukjent/aktivt/beskyttet blokkerer. | test.provenance.retention | candidate |
| purpose://candidate.ai-filproveniens.visibility | Oversikten er brukbar i Workbench | purpose://project-work.overview-and-sharing | Filtrer per maskin/disk/prosjekt/jobb/status, åpne filens relasjoner og se måletid/dekning. Bytes summeres uten å telle samme fil/delt cache flere ganger. | test.provenance.overview | candidate |
| purpose://candidate.ai-filproveniens.privacy | Metadata er eierstyrt og etterprøvbare | purpose://access.audit.privacy | Feil eier avvises; ingen filinnhold, nøkler, miljøvariabler eller kommandolinjer samles. Skriveadgang i grafen gir ikke sletteadgang til filsystemet. | test.provenance.auth | candidate |

## 2. Avgrensning og avhengigheter

Første omfang er artefakter og arbeidsområder opprettet gjennom registrerte agentjobber, bygg og deploy på Mac og HAVEN-verten. Eksisterende mapper kan kartlegges, men opphav merkes ukjent til det finnes jobb-/opprettelsesbevis. Agentens egenerklæring alene er ikke bevis. Ingen påstand om at alle programmer eller alle tidligere AI-filer kan identifiseres. Dekning fra registrerte skrivere og kontrollmålinger skal vises uttrykkelig.

Grafen gjenbruker eksisterende GraphStore og er søke-/relasjonslaget over hendelser med opprinnelse. Ingen ny grafmotor. Etterprøvbar hendelseshistorikk gjør projeksjonen gjenoppbyggbar. Nettbrudd må ikke blokkere jobben eller føre til tap av metadata; hendelser kan vente lokalt og spilles av senere. Dette er ønsket oppførsel, ikke en implementert garanti.

| Kapabilitet | Kilde | Avgrensning | Nødvendig kontroll |
|---|---|---|---|
| Agentjobbidentitet og artefaktfelt | HavenAgentD/Sources/HavenAgentRuntime/AgentJobModels.swift | Forventede/rapporterte resultater er ikke en systemomfattende filsensor. | Opprettelse, feil, avbrutt jobb og gjenstart må registreres fra faktisk utførelse. |
| Byggcache og lease | CellScaffold/scripts/run_swift_bounded.sh; CellProtocol/Scripts/haven-swiftpm.sh | Cache kan deles av flere jobber; OS-eier er ikke oppgaveeier. | Flere brukerkanter og aktiv lease beskytter delt cache. |
| GraphStore import og spørring | CellScaffold/Sources/App/Cells/Graph/GraphStoreCell.swift | sourceEventID/stateVersion er proveniensfelt, ikke dokumentert komplett dedupliserings-/rekkefølgevern. | Replay, rekkefølge, negativ autorisasjon og readback. |
| Disklagring | Samme fil, persistSnapshotToSQLiteIfNeeded | Kildelesing alene beviser ikke atomisitet eller crash recovery. | Feil midt i lagring skal bevare gammel komplett tilstand eller gi gjenoppbyggbar tilstand. |
| GUI | Eksisterende GraphStore explorer og skeleton graph/network | Ingen ny filoversikt er rendret eller godkjent. | Tom/fylt/feil-visning før G1-GUI, deretter virkelig brukerflyt. |
| Autorisert runtime | AgentD Workbench-target og resolver | MCP-transport utilgjengelig i denne økten; ingen alternativ sidekanal tatt i bruk. | Verifiser connection, eier, target og operasjoner før import. |

Minste metadata per artefakt: vert, filsystem, stabil artefakt-ID/generasjon, sti, type, målt/allokert størrelse og fullstendighet, opprettelsesobservasjon, jobb og agent/samtale, prosjekt/repo/worktree, formål, Git-status, regenererbarhet, sist observert bruk, aktive leases/mounts/prosesser, bevaringsregel/frigi-etter, avhengigheter, livsløp og kildebevis. Flyttet sti og gjenbrukt sti må ikke forveksles med samme artefakt.

Relasjoner: created_by, belongs_to, located_on, contained_in, derived_from, used_by, required_by, retained_for. Tilstander vises som aktiv, beholdes, kan vurderes for rydding, slettet eller ukjent. En utløpt TTL lager kun en kandidat. Kildetrær, WIP, identitets-/recoverydata, aktive deploy og avhengigheter bevares under gjeldende slettepolicy. Regelen for byggekapasitet endres ikke av denne oppgaven.

## 3. Forventningskontrakt — det Kjetil skal få

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Registrering fra virkelige Mac-/vertsjobber, også ved feil og avbrudd | kjørende funksjon + bevis | Eksisterende jobbløpere og wrappere | TESTRESULT.md#capture (etter implementering) | nei |
| Eierstyrte noder og relasjoner i eksisterende GraphStore, bevart etter restart | kjørende funksjon + bevis | Valgt Workbench-graf | TESTRESULT.md#replay | nei |
| Filoversikt med forklaring på aktiv/beholdes/ryddbar/ukjent og diskforbruk | kjørende flate | Developer Workbench; eventuell ryddeutførelse følger Admin/eksisterende rettigheter | images/README.md — fylt/tom/feil, lys/mørk, rendret 2026-10-02 | nei |
| Ryddeforslag med eksakte stier, avhengigheter, bevis og målt før/etter | reviewbar kandidat | Eksisterende godkjennings-/ryddeflyt | ACCEPT.md#cleanup | nei |
| Versjonert kode og eksakt test-/deployspor | PR og kvittering | HD-0154 med berørte repoer | PR, CI, staging og prod knyttet etter verifikasjon | nei |

Den vedlagte importskissen er for review og er ikke sendt til runtime. Dokumentet alene oppfyller ingen av funksjonsleveransene.

## 4. Tilknyttede formålspakker og lærdommer

Fullt maskinelt oppslag ligger i evidence/purpose-lookup.txt. Følgende pakker gjelder: pkg.std.everything-works (bygg, regresjon, dokumentasjon og status), pkg.std.gui-surface (godkjente referansebilder og virkelig GUI-paritet), pkg.std.cell-contract (kontrakt, autorisasjon og ingen tomme stubber), pkg.std.cell-combination (dataflyt og kapabilitetsgrenser), pkg.std.codex-handoff (etterprøvbar overlevering og dry-run).

Relevante registrerte lærdommer:

- lesson.bridge-inferred-architecture-from-one-use: Les faktisk kilde før en antatt kapabilitet blir premiss. Derfor er både GraphStore og AgentJobModels knyttet til navngitte lokale revisjoner.
- lesson.decomposition-is-classification: Gjenbruk kanoniske formål først; nye blad er kandidater.
- lesson.plan-instead-of-delivery: Et dokument om funksjonen er ikke en levert funksjon. Importskissen og denne spesifikasjonen er uttrykkelig ikke automatisk filsporing.
- lesson.text-ux-is-not-design og lesson.sketch-assumed-a-renderer-it-did-not-have: Ny filoversikt krever faktiske bilder og kontroll av rendrerens evner før GUI-godkjenning.
- lesson.green-gate-must-read-the-last-summary-line: Tester må vurderes fra endelig sammendrag, ikke en grønn delsuite.

Verifikasjon av PDD-kildene: Både global baseline-validering og validering med denne oppgaven gir de samme fem eksisterende feilene i lærdomsregisteret: fem referanser til purpose://candidate.testflyt-verktoycelle.haven-lenke-begge-veier finnes ikke i formålsregisteret. I tillegg gis 18 composition-advarsler. Ingen slik kanonisk referanse er opprettet eller omtolket her. Se evidence/pdd-baseline-validation.txt og evidence/pdd-validation.txt; valideringen er ikke grønn.

Læring fra kildeaudit: graph.workbench.applyUpdates kan returnere status=ok samtidig som skippedCount er større enn null. Verifiser node-/kantantall og les tilbake resultatet; sourceEventID/sourceStateVersion alene beviser ikke hendelsesdeduplisering eller riktig rekkefølge. Forventede AgentJob-artefakter beviser heller ikke at alle filopprettelser er fanget. Metadataimport, automatisk registrering og krasjsikker persistens må verifiseres hver for seg. Kildeidentiteter og linjemarkører finnes i evidence/source-audit.json.

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Godkjent kapasitets-/leasebeskyttet bounded runner for hvert berørt mål; konkret kommando fastsettes etter G1/G2. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | Godkjent xcode-check-wrapper med BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | Valider den versjonerte metadata-/cellekontrakten mot positive og negative fixtures; konkret validator fastsettes etter G1/G2. | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | Kjør avtalt innsamler/importør i dry-run og kontroller at ingen runtime- eller filsystemmutasjon skjer. | TESTRESULT.md#dry-run | venter |

| test.provenance.capture | purpose://candidate.ai-filproveniens.capture | Start ekte syntetisk jobb på begge verter som oppretter, flytter og endrer egne testfiler, samt feiler/avbrytes. Sammenlign med kontrollinventar; ukjent opphav/dekning skal forbli ukjent. | TESTRESULT.md#capture | venter |
| test.provenance.replay | purpose://candidate.ai-filproveniens.graph | Send samme hendelser to ganger, bytt rekkefølge, avbryt sync og restart lagring. Innhold/relasjoner må være uendret og gjenoppbyggbare; feilinjiser halvveis i persistens. | TESTRESULT.md#replay | venter |
| test.provenance.retention | purpose://candidate.ai-filproveniens.retention | Utløpt artefakt med aktiv jobb/lease/mount/avhengighet, beskyttet type eller ufullstendig scan kan ikke bli slettbar. Test også positiv regenererbar kandidat og at ingen sletting skjer ved klassifisering. | TESTRESULT.md#retention | venter |
| test.provenance.overview | purpose://candidate.ai-filproveniens.visibility | Følg fil→jobb→prosjekt i ekte GUI, mål filter, friske størrelser og diskgrenser. Delt cache og foreldre/barn skal ikke dobbelttelles. | ACCEPT.md#overview | venter |
| test.provenance.auth | purpose://candidate.ai-filproveniens.privacy | Feil eier/target/scope avvises. Fixtures med hemmelig filinnhold/argumenter verifiserer at bare tillatte metadata havner i hendelser/graf. | TESTRESULT.md#auth | venter |

## 6. Åpne spørsmål til Kjetil

G1 godkjent 2026-10-02: automatisk proveniens for registrerte agent-, bygg- og deployjobber på begge maskiner, eksisterende GraphStore og en Workbench-oversikt; gamle ukjente filer markeres ukjent, og sletting krever fortsatt egne kontroller.

Ingen beslutning om ny database, systemomfattende overvåking eller automatisk sletting inngår. Renderte GUI-stater og detaljert implementeringsplan foreligger fra 2026-10-02; se images/README.md og PLAN.md. G1-GUI og G2 er ikke godkjent. Eksisterende spørsmål om cleanup-buffer er separat fra denne oppgaven.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 1 | 2026-10-01 | Brukerens krav konkretisert; disk målt på begge verter; GraphStore og AgentJobs lest på navngitte origin/main-ref-er; MCP utilgjengelig; ingen live import. | Codex |

| 2 | 2026-10-02 | Kjetil godkjente omfanget ordrett: «Jeg Godkjenner dette omfanget for registrerte agent-, bygg- og deployjobber på begge maskiner». Formål og avgrensning er uendret. | Kjetil / Codex registrerte |

| 3 | 2026-10-02 | Plan og faktiske rendererbilder klare; grafisk nettverk har målt geometriavvik og relasjonslisten er GUI-referansen. MCP targets svarer igjen, men ingen graf-target finnes. | Codex |
