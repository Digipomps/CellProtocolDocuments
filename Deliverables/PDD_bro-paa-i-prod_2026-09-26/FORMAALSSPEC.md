# Formålsspesifikasjon — bro paa i prod

Oppgavemappe: `PDD_bro-paa-i-prod_2026-09-26` · Opprettet 2026-09-26 · Iterasjon 2 (G1 godkjent 2026-09-27)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Kjetil 2026-09-26 (ordrett): «Broen er slått av i Prod - fungerer ikke kontakt fra andre scaffolds som HAVEN eller HAVENAgentD? Den må absolutt være på - ellers er det bare juks du driver med når disse prøver å kommunisere med prod eller staging. At Brigde fungerer og er robust er forutsetningen for å ha et helt desentralisert økosystem.»

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Broen er slått av i prod | retrieved — bekreftet | Målt 2026-09-26 ca. 19:50Z fra Chrome: `GET https://haven.digipomps.org/bridgehead/Porthole/CloudBridge` → 404; WebSocket til samme sti → lukket 1006 uten oppkobling. `/health/build`: app `18c14c32`, CellProtocol `473357cf`, `environment: production`. |
| … og i staging | retrieved — bekreftet | Samme måling mot `staging.haven.digipomps.org` (app `4dd70c52`, CellProtocol `473357cf`): 404 / 1006. |
| Siden når, og hvorfor | retrieved | CellScaffold `14b50a51` (2026-07-13, «Enforce vault-bound access across scaffold sessions») tømte `VaporBridgehead.boot` med kommentaren «The legacy bridgehead had no authenticated session/channel binding. Native porthole is the supported contract-authorized replacement.» `d6623294` (samme dag, «Remove legacy admin access paths») fjernet registreringen i `Sources/App/routes.swift`. Broen har altså vært av i begge miljøer i ca. 2,5 måneder. |
| Kontakt fra HAVEN/HavenAgentD virker ikke | retrieved for at endepunktet mangler; unavailable for hver enkelt klient (ingen ende-til-ende-kjøring ennå) | Klientene går mot `bridgehead`: CellProtocol `Sources/CellBase/Cells/CellResolver/CellResolver.swift:91` (standard `websocketEndpoint`), HavenAgentD `Sources/HavenAgentRuntime/DeviceActionRelay.swift:865` og `Sources/HavenCorrespondenceMCP/CorrespondenceContracts.swift:16`. CellScaffold deler selv ut `/bridgehead/<publisher>/<bro>` i `Sources/App/Services/SproutBridgeDiscoveryCompatibility.swift:172`, og staging-fiksturen `Sources/App/Cells/SkeletonParity/SkeletonParityFixtureCells.swift:384` peker på `wss://staging.haven.digipomps.org/bridgehead/…`. |
| Den eneste innkommende broen som finnes i dag | retrieved | `/v1/resolver/native-porthole/:pubId/:bridgeId` (`Sources/App/Controllers/VaporSproutResolver.swift:60`). Målt: åpner og lukkes med 1008 uten gyldig Sprout-kontrakt. Riktig for native Porthole, men ingen bro for andre scaffolds. |
| CellProtocol kan bevise identitet over broen | retrieved at det finnes; ikke vurdert som kanalbinding | `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1044, 1422–1474, 1784` og `BridgeIdentityProofAuthorization.swift` (IdentitySigningChallenge, replay-lager, signaturverifisering). Laget for bevis per operasjon. |
| Utgående bro fra CellScaffold har egen transportadgang | retrieved | `Sources/ScaffoldKit/RemoteBridgeheadAccess.swift`: `HAVEN_BRIDGEHEAD_TOKEN` + `HAVEN_BRIDGEHEAD_HOSTS`, «transport admission … independent of Cell authority». |
| HavenAgentD har en lokal bridgehead med autorisasjon og tillatelsesliste | retrieved | `HavenAgentD/Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:96–140` (`authorize(req)`, `routeLookup`, lukker 1008 ved avslag). |
| HAVEN-appen som klient | unavailable — hvilket repo og hvilken sti appen bruker mot prod er ikke lest ennå | Leses før G2; legges til i formålet om at eksisterende klienter skal virke |
| «Juks»: påstander om kommunikasjon med prod/staging | unavailable — ikke revidert | Blir formål 7. |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.bro-paa-i-prod.root | Andre scaffolds kan kommunisere med prod og staging over Bridge, autentisert og robust | — | HavenAgentD på Kjetils Mac løser en celle i staging og i prod over `wss://…/bridgehead/…` og får et svar tilbake | Ende-til-ende-kjøring fra Mac-en, logg i TESTRESULT.md#e2e | candidate |
| purpose://candidate.bro-paa-i-prod.kanalen-finnes | Bro-endepunktet svarer i begge miljøer | root | `wss://<vert>/bridgehead/<publisher>/<broId>` oppgraderes (101), ikke 404, på staging og prod | WebSocket-probe utenfra etter hver utrulling | candidate |
| purpose://candidate.bro-paa-i-prod.kanalen-er-bundet-til-identitet | Kanalen er bundet til en bevist identitet før første kommando rutes | root | Uten gyldig bevis lukkes kanalen (1008). Et gjenbrukt bevis avvises. Et bevis for en annen identitet avvises. Dette er grunnen til at broen ble slått av 13.07, og den må være løst | Negative tester i CI + probe mot staging | candidate |
| purpose://candidate.bro-paa-i-prod.noklene-forblir-private | Private nøkler forlater aldri brukerens sikre, private sted | kanalen-er-bundet-til-identitet | Beviset lages ved signering hos klienten (brukerens enhet/vault). Prod og staging lagrer og ser bare offentlige nøkler; ingen privat nøkkel, token eller signeringsmulighet for brukerens identitet finnes på en skyvert. En presentert deskriptor gir aldri en lokal vault (jf. CellProtocol #39 / HD-0080) | Kodegjennomgang + test som viser at serveren avviser en identitet den bare har deskriptoren til, og inspeksjon av at ingen nøkkel skrives server-side | candidate |
| purpose://candidate.bro-paa-i-prod.ingen-svake-ledd | Ingen hackbare svake ledd i kjeden | kanalen-er-bundet-til-identitet | Astra (Codex) har gjort en trusselmodell og en kodegjennomgang av hele kjeden (klient → proxy → bridgehead → BridgeBase → celle) før implementering og etter, og hvert funn er rettet eller eksplisitt akseptert av Kjetil | handoff/ASTRA-TRUSSELMODELL.md og handoff/ASTRA-KODEGJENNOMGANG.md | candidate |
| purpose://candidate.bro-paa-i-prod.celleautoritet-uendret | Transportadgang gir aldri cellerettigheter | root | Hver kommando over broen autoriseres av målcellen som om den kom lokalt: feil requester, feil keypath og `purpose://prompt.unknown` avvises | test.cell.auth-negative kjørt over broen | candidate |
| purpose://candidate.bro-paa-i-prod.klientene-treffer | Eksisterende klienter virker uten ny konfigurasjon | root | Hver klient i §0 (CellResolver-standard, HavenAgentD relay og correspondence, bro-oppdagelsen, SkeletonParity-fiksturen) når en celle i staging og deretter prod | Én kjøring per klient, logg i TESTRESULT.md#klienter | candidate |
| purpose://candidate.bro-paa-i-prod.robust | Broen tåler utrulling, nettbrudd og mange klienter | root | Klienten kobler seg på igjen innen 30 s etter omstart/drain; heartbeat holder kanalen i live; foreldede økter ryddes; tak på samtidige økter per identitet | Utrulling på staging mens en klient er tilkoblet; måling i TESTRESULT.md#robust | candidate |
| purpose://candidate.bro-paa-i-prod.aldri-stille-av-igjen | En utrulling uten bro stopper | root | `haven-deploy`-verifiseringen og promoteringsskriptene kjører bro-proben og nekter å promotere ved 404. En CI-test feiler hvis ruten ikke registreres. `/health/ready` rapporterer broen | Ruten fjernet i en testgren → CI rød; deploy-logg viser proben | candidate |
| purpose://candidate.bro-paa-i-prod.aerlige-paastander | Påstander siden 13.07 om kontakt med prod/staging er gjennomgått | root | Liste over rapporter og tester som har påstått kontakt med prod/staging, hver merket: over HTTP / over bro / uverifisert, med rettelse i kildedokumentet der påstanden var feil | Liste i ACCEPT.md#paastander | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke å gjenåpne den gamle broen uten kanalbinding. Den ble slått av av en reell grunn.
- Ikke en endring av native-porthole-ruten, som virker og er kontraktsbasert.
- Ikke anonym tilgang til celler. Broen er transport; cellene bestemmer.
- Ikke en ny bro-protokoll hvis CellProtocol allerede har mekanismen. Det avgjøres ved lesing av koden i G2, ikke antatt her.

Kapabiliteter og avhengigheter oppgaven bygger på:
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Bro-protokollen (BridgeBase), CellProtocol-pin `473357cf` | `CellProtocol/Sources/CellBase/Cells/Bridging/` | Virker lokalt (HavenAgentD bruker den). Ikke målt mot prod siden 13.07 | ja |
| IdentitySigningChallenge med replay-lager | `BridgeBase.swift:1422–1474` | Laget for bevis per operasjon; om den kan binde en hel kanal er ikke vurdert | ja |
| Vault-bundet tilgang | CellScaffold `14b50a51` | Broen må ikke omgå den | ja |
| WebSocket-upgrade gjennom vertens proxy | vertens proxy-oppsett | native-porthole-WS oppgraderes på samme vert, så upgrade virker generelt. Selve `/bridgehead`-stien er ikke prøvd | ja |
| Utrullingskjeden | HAVEN-Deploy (`haven-deploy`, promoteringsskriptene) | Har i dag ingen bro-probe | nei; formålet om at broen aldri skal være stille av igjen legger den til |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
| Leveranse | Type (bilde / fil / testutdata / kjørende flate) | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| WebSocket-probe mot staging og prod: 101 og «ready» fra broen | testutdata | TESTRESULT.md#probe | — | nei |
| HavenAgentD på Mac-en henter en verdi fra en celle i staging, så i prod, over broen | kjørende flate + logg | TESTRESULT.md#e2e | — | nei |
| Negative tester (uten bevis, replay, feil identitet, feil keypath) grønne i CI | testutdata | TESTRESULT.md#auth | — | nei |
| Utrulling på staging med tilkoblet klient: påkobling igjen innen 30 s | testutdata | TESTRESULT.md#robust | — | nei |
| Deploy-logg der bro-proben stopper en utrulling uten bro og slipper en med | fil | HAVEN-Deploy/_handoff/BRO/ | — | nei |
| Liste over påstander siden 13.07, med status og rettelser | fil | ACCEPT.md#paastander | — | nei |
| PR merget til main, rullet ut til staging og prod | kjørende flate | `/health/build` + probe | — | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.bro.probe | purpose://candidate.bro-paa-i-prod.kanalen-finnes | WebSocket-probe utenfra mot `/bridgehead/<publisher>/<broId>` på staging og prod, før og etter endring | TESTRESULT.md#probe | venter |
| test.bro.auth-negative | purpose://candidate.bro-paa-i-prod.kanalen-er-bundet-til-identitet | Enhetstester: uten bevis → 1008; replay → avvist; bevis for annen identitet → avvist | TESTRESULT.md#auth | venter |
| test.bro.celleautoritet | purpose://candidate.bro-paa-i-prod.celleautoritet-uendret | test.cell.auth-negative kjørt gjennom broen, ikke lokalt | TESTRESULT.md#auth | venter |
| test.bro.klienter | purpose://candidate.bro-paa-i-prod.klientene-treffer | Én kjøring per klient i §0 mot staging, så prod | TESTRESULT.md#klienter | venter |
| test.bro.e2e | purpose://candidate.bro-paa-i-prod.root | HavenAgentD på Mac-en løser en celle i staging og prod og får svar | TESTRESULT.md#e2e | venter |
| test.bro.robust | purpose://candidate.bro-paa-i-prod.robust | Utrulling på staging med tilkoblet klient; mål tid til påkobling; tak per identitet | TESTRESULT.md#robust | venter |
| test.bro.deploy-gate | purpose://candidate.bro-paa-i-prod.aldri-stille-av-igjen | Kjør promoteringsskriptet mot et bilde uten rute → stopper; med rute → slipper | HAVEN-Deploy/_handoff/BRO/ | venter |
| test.bro.ci-route | purpose://candidate.bro-paa-i-prod.aldri-stille-av-igjen | CI-test som krever at `bridgehead`-ruten er registrert | TESTRESULT.md#ci-route | venter |
| test.bro.paastander | purpose://candidate.bro-paa-i-prod.aerlige-paastander | Søk i HAVEN-Deploy/_handoff, Deliverables og prosjektdokumentene etter påstått kontakt med prod/staging siden 13.07 | ACCEPT.md#paastander | venter |
| test.bro.noklene-private | purpose://candidate.bro-paa-i-prod.noklene-forblir-private | Test: serveren avviser en identitet den bare har deskriptoren til; inspeksjon: ingen privat nøkkel eller signeringstoken lagres på serveren | TESTRESULT.md#nokler | venter |
| test.bro.astra | purpose://candidate.bro-paa-i-prod.ingen-svake-ledd | Astra trusselmodell (før) og kodegjennomgang (etter); hvert funn rettet eller akseptert | handoff/ASTRA-*.md | venter |

## 6. Åpne spørsmål til Kjetil — besvart 2026-09-27

1. Bevis ved åpning av broen: **signert identitet** (IdentitySigningChallenge med replay-vern). Kjetil: «det å bevise identitet over bridge er helt nødvenig. Da kan brukeren ha sine private nøkler i et sikkert og privat sted - ikke på en skyvert.»
2. Hvem får åpne broen: **alle med bevist identitet**; cellene avgjør resten; tak per identitet.
3. Prioritet: **først** i køen.
4. Kjetil: «Be astra ta en code review på dette - vi skal ikke ha noen hackbare svake ledd i kjeden.» → formålet ingen-svake-ledd, med Astra før og etter implementering.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-26 | Opprettet | Losen |
| 1 | 2026-09-26 | §0–§3, §5, §6 fylt etter måling av prod og staging og lesing av 14b50a51/d6623294 | Losen |
| 2 | 2026-09-27 | G1 godkjent av Kjetil med to tillegg: nøklene forblir private (ikke på skyvert) og Astra-gjennomgang uten svake ledd. §6 besvart. | Losen |
