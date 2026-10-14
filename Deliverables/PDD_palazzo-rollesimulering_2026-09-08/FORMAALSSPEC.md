# Formålsspesifikasjon — palazzo rollesimulering

Oppgavemappe: `PDD_palazzo-rollesimulering_2026-09-08` · Opprettet 2026-09-08 · Iterasjon 1 (ikke godkjent — til G1)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Vi bør egentlig teste dette med simulerte brukere i de forskjellige rollene med egne perspektiver slik at vi ser de oppnår alt de har formål til og på den måten kan avdekke om det er tilganger som hindrer brukeren i å oppnå sitt formål - og om det er feil eller riktig.

Sammenheng: sagt 2026-09-08 rett etter at Codex fant at gjeste- og innholdscellen ikke er publisert over bridgehead (Sicilia G5). Kjetils poeng er generelt: tilgangsfeil oppdages i dag *tilfeldig*, når en flate skal vises. Han vil at de skal oppdages *systematisk*, ved at hver rolle prøver å nå sine formål — og at hvert stopp vurderes: riktig stopp (personvern/eierskap) eller feil stopp (bug/manglende publisering).

| Påstand i intensjonen / antatt kapabilitet | Audit (retrieved / recalled / unavailable / contradicted) | Kilde |
|---|---|---|
| Palazzo har tre principal-roller: `guest:<id>`, `staff:<id>`, `house` (header `X-Palazzo-Principal`) | retrieved | `PalazzoPrincipalGateway.swift:17–58` |
| Hver handler validerer tilgang per keypath (`validateAccess`), og negative tester finnes (feil requester/keypath/ukjent formål) | retrieved | `PalazzoEntityCell.swift`; `PalazzoSiciliaTests.swift:290–330` |
| Rollenes *formål* er skrevet ned et sted maskinlesbart | unavailable — formålene finnes spredt i PDD-mappene (§1 i hver FORMAALSSPEC) og `Formalssett_service_hospitality_2026-08-26.md`, ikke som kjørbare rollescenarier | — |
| Bridgehead publiserer bare et utvalg celler (`isPublishable`) — gjest/innhold mangler | retrieved (rettes i Sicilia G7) | `PalazzoBridgehead.swift:118–130` |
| Eksisterende tester kjører HTTP via XCTVapor uten gateway-token; produksjon krever token | retrieved | `run-g5.README.md` §2, `PalazzoSiciliaTests.swift:332` |
| Explore-audit lister alle registrerte operasjoner per celle (101 i appen) | retrieved | `sicilia-gui-evidence/explore-app.md` |
| Simulert bruker = språkmodell som spiller rollen | **avvises som kjede-komponent** — rollen simuleres deterministisk (script med formålsliste); en modell kan brukes utenfor kjeden til å *foreslå* scenarier, aldri til å avgjøre riktig/feil | Kjetils regel «ingen språkmodell i kjeden» |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-rollesimulering.root | Hver rolle når sine formål, og hvert stopp er begrunnet | purpose://test.acceptance · purpose://access.audit.privacy | For hver rolle (gjest, annen gjest, personale, hus) finnes en formålsliste; en kjøring viser per formål OPPNÅDD / STOPPET, og hvert STOPPET er klassifisert `riktig` (forventet av personvern/eierskap, med referanse til formålet som krever det) eller `feil` (bug/manglende publisering, med HD-/PDD-post). Ingen uklassifiserte stopp ved G3. | `test.roles.report` | candidate |
| purpose://candidate.palazzo-rollesimulering.roles-have-purposes | Rollene har nedskrevne formål med observerbart utfall | root | `roles/<rolle>.json`: liste av {purposeRef, handling (keypath/rute + payload), forventet utfall (observerbar tilstand), forventet tilgang: `allowed` / `denied` (+ hvorfor)}. Kilde: §1 i eksisterende PDD-er + `Formalssett_service_hospitality`. Minst: gjest 8 formål, annen gjest 4, personale 4, hus 6. | `test.roles.schema` | candidate |
| purpose://candidate.palazzo-rollesimulering.simulated-actor-uses-production-path | Simulert aktør går produksjonens vei | root | Aktøren bruker HTTP-rutene med `X-Palazzo-Principal` og gateway-token (ikke celle-kall innenfra), mot en kjørende server med isolert vault — samme vei som HAVEN-appen. (lesson.tested-a-different-path-than-production) | `test.roles.production-path` | candidate |
| purpose://candidate.palazzo-rollesimulering.every-stop-is-classified | Hvert stopp er riktig eller feil — aldri bare rødt | root | Et `denied`/feil som *ikke* var forventet i formålslisten gir status `UKLASSIFISERT` og feiler kjøringen til et menneske (Kjetil) har satt `riktig`/`feil` i `roles/<rolle>.json`. Klassifiseringen gjøres aldri av kjøringen selv. | `test.roles.unclassified-fails` | candidate |
| purpose://candidate.palazzo-rollesimulering.agent-role | Agenten måles med samme metode som menneskene | root | Bridgehead-identiteten (Losen/agent) er femte rolle med egen formålsliste: hva den skal kunne nå på egne vegne, hva den skal kunne nå på en brukers vegne, og hva den aldri skal nå. Grants-listen den kjøres med er den samme som tillitspakken erklærer, slik at kjøringen også er en *etterprøving* av at pakken ble overholdt. Se `PDD_tillitspakke-agentflaate_2026-09-08`. | `test.roles.agent` | candidate |
| purpose://candidate.palazzo-rollesimulering.cross-role-privacy | Skal ikke: én rolle når en annens data | root · polarity: prohibited | «Annen gjest» prøver å lese første gjests `entity.records`, `insight.*` og reaksjoner → alle `denied`, klassifisert `riktig`. Personale når ikke gjestens entitet uten samtykke. | `test.roles.cross-privacy` | candidate |
| purpose://candidate.palazzo-rollesimulering.reachable-in-app | Formål via flate: knappen finnes og virker | root | For formål som har en GUI-flate: handlingens keypath finnes i fabrikkens `reachableActionKeypaths` (SkeletonReachabilityAudit) — ellers er formålet uoppnåelig i appen selv om ruten virker. (lesson.findability-is-not-usability) | `test.roles.reachable` | candidate |
| purpose://candidate.palazzo-rollesimulering.report-for-humans | Rapporten leses av Andre/Kjetil | root | `RAPPORT.md` per kjøring: én tabell per rolle (formål · handling · utfall · klassifisering · hvorfor), pluss liste «feil stopp» med HD-/PDD-referanse. | `test.roles.report` | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en språkmodell som «spiller» gjest. Rollen er en formålsliste + deterministisk aktør. (En modell kan foreslå nye formål til listen, utenfor kjeden.)
- Ikke en erstatning for enhetstestene — de består. Dette er laget over: formål → rolle → produksjonsvei.
- Ikke UI-automatisering i første runde (ingen Playwright-klikking); flate-oppnåelighet sjekkes via SkeletonReachabilityAudit, visuell paritet er Sicilia G5.
- Ikke automatisk vurdering av riktig/feil. Det er en menneskelig beslutning som lagres i rollefilen og gjenbrukes.

Kapabiliteter og avhengigheter oppgaven bygger på (hver med kilde og hva den ikke dekker):
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Kjørende Palazzo-server med token og isolert vault | `run-g5.sh` steg 1 (gjenbrukes) | krever miljø som tillater TCP-bind — ikke Codex-sandkassen; kjøres av Kjetil eller dispatcher-adapter med rettighet | ja |
| Principal-roller og gateway-token | `PalazzoPrincipalGateway.swift` | «annen gjest» = ny guest-id; ingen egen rolle for Losen/agent i første runde | ja |
| SkeletonReachabilityAudit | CellScaffold/PalazzoScaffold (brukt i `PalazzoRememberTests.testHuskSkeletonFactoriesUseReachableConcreteActions`) | gir keypaths, ikke visuell verifikasjon | ja |
| Formålslister | §1 i PDD husk/sicilia/gjestebestilling + `Formalssett_service_hospitality_2026-08-26.md` | må oversettes til handling+forventning per rolle — det er hoveddelen av arbeidet | nei (lages her) |
| Bridgehead-publisering av gjest/innhold | Sicilia G7 (i kø) | før G7: appveien stopper ved bridgehead — det er nettopp et «feil stopp» kjøringen skal finne | nei — **besluttet 2026-09-09: første kjøring gjøres før G7**, slik at metoden selv finner stoppet vi sist fant tilfeldig. Finner den det ikke, er det metoden som er for svak, ikke systemet som er friskt. |


## 2b. Kalibrering av aktøren — lagt til iterasjon 2

Denne delen finnes fordi nodegraf-arbeidet 8.–9. september ga tre måletall som
gjelder her uendret. Kilde: `UniverseSimulation/Documentation/Nodegraf_Vurdering_2026-09-08.md`
og `Nodegraf_Losen_Motsvar_2026-09-08.md`.

**Hvorfor en aktør må kalibreres før den leses.** Et søk over 9 000 kandidater
på *ren støy* nådde 4,546 der porten lå på 4,991 — altså nesten forbi, på data
der det ikke fantes noe å finne. En harness som ikke er vist å kunne skille de
to utfallene, produserer utfall uansett. Og en konformansprøve godtok en backend
som returnerte NaN, fordi sammenligningen `err > tol` er `False` for NaN: et
resultat som aldri ble evaluert telte som bestått. Begge feilene er billige å
forebygge og dyre å oppdage sent.

Oversatt til denne oppgaven: en rolleaktør som ikke *først* er vist å kunne
rapportere både OPPNÅDD og STOPPET på tilfeller der svaret er kjent, forteller
ingenting når den rapporterer om tilfellene der svaret er ukjent. Det er hele
poenget med oppgaven — å skille riktig stopp fra feil stopp — og det er nøyaktig
det en ukalibrert aktør ikke kan.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-rollesimulering.actor-is-calibrated | Aktøren viser begge utfall før noe resultat leses | root | Hver `roles/<rolle>.json` merker minst ett formål `calibration: positive` (sikkert oppnåelig for rollen — f.eks. huset leser sine egne data på riktig keypath) og minst ett `calibration: null` (sikkert forbudt — f.eks. annen gjest mot første gjests `entity.records`). Kjøringen feiler hvis et positivt kalibreringsformål rapporteres STOPPET, eller et null-kalibreringsformål rapporteres OPPNÅDD. Da er harnessen i stykker, ikke systemet, og resten av rapporten leses ikke. | `test.roles.calibration` | candidate |
| purpose://candidate.palazzo-rollesimulering.null-principal-run | Nullkjøring: en principal uten grants oppnår ingenting | root | Hele formålslisten kjøres på nytt med en gyldig, men tom principal (ny guest-id uten samtykke, uten grants). **Hvert eneste formål skal være STOPPET.** Ett OPPNÅDD betyr at suksessen lages av harnessen eller ruten — feil principal-header, mellomlagret svar, en rute som ignorerer principal — og ingen per-formål-gjennomgang ville sett det. Dette er direkte analog til nullarmen som ble kjørt 9. september og kom tilbake ren. | `test.roles.null-principal` | candidate |
| purpose://candidate.palazzo-rollesimulering.no-unevaluated-success | Et formål som ikke ble evaluert er aldri OPPNÅDD | root | Hvert utfall bærer sitt eget bevis: HTTP-status **og** den observerte tilstanden forventningen gjaldt. Kunne tilstandssjekken ikke kjøres (tomt svar, manglende felt, timeout), er utfallet UKLASSIFISERT — aldri OPPNÅDD, aldri stille grønt. | `test.roles.no-unevaluated-success` | candidate |
| purpose://candidate.palazzo-rollesimulering.scripted-is-reference-for-model | Skriptet kjøring er den målte referansen modellvarianten må slå | root · forhåndsregistrert | Når en språkmodell-aktør kommer (runde 2), sammenlignes den mot den skriptede kjøringen på tre tall som fryses nå: antall formål OPPNÅDD, antall **feil stopp funnet**, og kostnad per kjøring. Modellen har tilført noe bare hvis den finner feil stopp skriptet ikke fant, ved samme rollesett. Uten dette blir «modellen føltes bedre» konklusjonen. | (ingen test i runde 1 — forhåndsregistrering) | candidate |

### Kalibreringsparene, per rolle (besluttet 2026-09-09)

| Rolle | Positiv referanse (sikkert oppnåelig) | Nullreferanse (sikkert forbudt) |
|---|---|---|
| gjest | leser sin egen `entity.*` på egen principal | leser husets `house.ledger` |
| annen gjest | leser sin egen entitet | leser første gjests `entity.records` |
| personale | `/api/staff/brief` med stående samtykke returnerer de fem `briefKeypaths` som *delt* | samme brief uten samtykke returnerer «ikke delt» for alle fem — aldri en verdi |
| hus | leser `house.staff` (egen liste) | leser en gjests `insight.*` uten avtale |
| agent | de keypathene tillitspakken erklærer | ett keypath like utenfor pakken |

**Belegg for personale-paret** ([belagt], lest 2026-09-09):
`PalazzoStaffShellCell.briefKeypaths` er de fem `entity.visits.frequency`,
`entity.visits.last`, `entity.purposes`, `entity.interests`,
`entity.constraints.current` — allergenene ligger i den siste.
`PalazzoSurfaceTests.testBriefWithStandingConsentShowsWhatWasShared:262` viser
hele veien: gjesten gir grants på nøyaktig disse keypathene, personale poster
`/api/staff/brief`, og alle fem kommer tilbake som delt.
`testBriefWithoutConsentSaysNotSharedAndStartsTheAsk:208` og
`testWithdrawnConsentClosesTheBriefAgain:320` dekker de to andre retningene.
Samtykkeveien virker altså ende til ende i dag, og paret er trygt å bruke.

**Med ett forbehold som er selve grunnen til at kalibreringen finnes:** de
testene kjører in-process via XCTVapor **uten** gateway-token, mens rolleaktøren
skal gå over HTTP *med* token (§2, `simulated-actor-uses-production-path`). At
paret virker i enhetstesten er derfor ikke belegg for at det virker på
produksjonsveien — det er nøyaktig `lesson.tested-a-different-path-than-production`.
Kalibreringen må etableres på nytt på produksjonsveien i hver kjøring, og det er
det den er til for.

Regelen, som i `Tools/nodegraph/purpose.py`: **feiler en av de tre
kalibreringskontrollene, er kjøringen en instrumenteringsrunde og gater
ingenting.** Den skal rapporteres som det, ikke kjøres om igjen med justerte
forventninger.

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
(ingen GUI-flate deklarert — sett `surfaces` i STATUS.md hvis det er feil)
| Leveranse | Type (bilde / fil / testutdata / kjørende flate) | Hvor | Referanse (images/…-v1.png osv.) | Godkjent |
|---|---|---|---|---|
| Rollefiler: `roles/gjest.json`, `roles/annen-gjest.json`, `roles/personale.json`, `roles/hus.json` | fil | `PalazzoScaffold/Tests/Roles/` | schema i `roles/README.md` | nei |
| Aktør: `Tests/Roles/run_roles.py` (stdlib) — kjører alle roller mot en server, skriver RAPPORT.md + JSON | fil + kjørbar | `PalazzoScaffold/Tests/Roles/` | `python3 run_roles.py --base-url … --token …` | nei |
| Første rapport, kjørt av Kjetil **før Sicilia G7**: hvert stopp klassifisert | testutdata | `RAPPORT_<dato>.md` i denne mappen | — | nei |
| Liste over «feil stopp» registrert som HD-poster / PDD-slicer | fil | `STATUS.md` + HAVEN-Deploy | — | nei |
| Kalibreringsblokk øverst i hver rapport: de tre kontrollene med utfall, før noen rolletabell | testutdata | `RAPPORT_<dato>.md` §0 | — | nei |
| Nullkjøringens egen rapport (tom principal, alt skal være STOPPET) | testutdata | `RAPPORT_<dato>_nullprincipal.md` | — | nei |

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
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://project-work.overview-and-sharing [active] — Project work overview and sharing
- purpose://project-work.current-status-and-outstanding [active] — Current status and outstanding work
- purpose://quality [active] — Quality
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://validation [active] — Validation
- purpose://test.acceptance [active] — Acceptance tests
- purpose://test.acceptance.purpose-decomposition [active] — Purpose decomposition acceptance
- purpose://test.acceptance.hallucination-evaluation [draft] — Hallucination evaluation gate
- purpose://test.acceptance.questionnaire [active] — Questionnaire acceptance tests
- purpose://test.acceptance.project-work [active] — Project work acceptance tests
- purpose://self-determination.data.use-purpose [candidate] — Purpose binding for data use

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
| test.roles.schema | roles-have-purposes | Validator: hver rad har purposeRef, handling, forventet utfall, forventet tilgang; minimumsantall per rolle. | TESTRESULT.md#roles-schema | venter |
| test.roles.production-path | simulated-actor-uses-production-path | Aktøren bruker bare HTTP + principal-header + token; ingen import av App-modulen. | TESTRESULT.md#roles-path | venter |
| test.roles.unclassified-fails | every-stop-is-classified | Fixture med ett uventet denied → exit ≠ 0 og «UKLASSIFISERT» i rapporten. | TESTRESULT.md#roles-unclassified | venter |
| test.roles.cross-privacy | cross-role-privacy | Annen gjest/personale mot gjestens data → alle denied, alle `riktig`. | TESTRESULT.md#roles-privacy | venter |
| test.roles.reachable | reachable-in-app | Hvert GUI-formål sin keypath finnes i fabrikkens reachableActionKeypaths. | TESTRESULT.md#roles-reachable | venter |
| test.roles.agent | agent-role | Agentens formålsliste kjøres med tillitspakkens grants; hvert keypath utenfor pakken skal være denied, hvert innenfor allowed. Avvik ⇒ pakken ble ikke overholdt. | TESTRESULT.md#roles-agent | venter |
| test.roles.calibration | actor-is-calibrated | Kjør de merkede kalibreringsformålene først; positivt STOPPET eller null OPPNÅDD ⇒ exit ≠ 0 og resten av rapporten merkes «ikke lest». | TESTRESULT.md#roles-calibration | venter |
| test.roles.null-principal | null-principal-run | Hele listen med tom principal; ett eneste OPPNÅDD ⇒ exit ≠ 0. | TESTRESULT.md#roles-nullprincipal | venter |
| test.roles.no-unevaluated-success | no-unevaluated-success | Fixture der tilstandssjekken ikke kan kjøres (tomt svar) ⇒ UKLASSIFISERT, ikke OPPNÅDD. | TESTRESULT.md#roles-unevaluated | venter |
| test.roles.report | root · report-for-humans | Kjøring mot ekte server; RAPPORT.md uten UKLASSIFISERT; «feil stopp» har HD/PDD-ref. | RAPPORT_<dato>.md | venter |

## 6. Åpne spørsmål til Kjetil

1. Roller i første runde: gjest, annen gjest, personale, hus — riktig sett? Skal Losen/agent (bridgehead-identitet) være femte rolle nå, eller vente til tillitspakke-oppgaven?
2. Hvem klassifiserer «riktig/feil» ved første kjøring — du alene, eller du og Andre sammen (huset ser sine egne stopp)?
3. Forslag: første kjøring gjøres *før* G7 er levert, slik at bridgehead-stoppet dokumenteres som «feil stopp» av metoden selv (bevis på at metoden finner det vi fant tilfeldig). Ok?
4. Er det greit at formålslistene i første runde skrives av Losen ut fra eksisterende PDD-er, og at du retter dem — eller vil du skrive gjestens selv?
5. Kalibreringen (§2b) krever at hver rolle har minst ett formål som er *sikkert oppnåelig* og ett som er *sikkert forbudt*. For gjest og hus er de lette å peke ut. For personale er jeg usikker: er «kelner leser gjestens allergener når gjesten har gitt spørretilgang» sikkert nok til å være positiv referanse i dag, eller er den avhengig av noe som ennå ikke virker? Om den er usikker, er den et *formål å teste*, ikke en kalibrering — og da trenger personale-rollen en annen.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-08 | Opprettet | Losen |
| 1 | 2026-09-08 | Formålstre (6 blad + antiformål), avgrensning, forventningskontrakt, tester, 4 spørsmål | Losen |
| 3 | 2026-09-09 | Kjetils svar på §6: fem roller (Losen/agent med fra runde 1), første kjøring **før** Sicilia G7, personale-kalibrering = staff/brief med stående samtykke. Belegg for personale-paret lest i `PalazzoSurfaceTests`; forbeholdet om token-veien skrevet inn. Kalibreringstabell per rolle. | Losen |
| 2 | 2026-09-09 | §2b kalibrering av aktøren: positiv/null-referanse per rolle, nullkjøring med tom principal, «ikke evaluert er ikke oppnådd», og forhåndsregistrering av skriptet kjøring som referanse for modellvarianten. Tre nye tester, to nye rader i §3, ett nytt spørsmål. Bakgrunn: de tre måletallene fra nodegraf-arbeidet 8.–9.9. | Losen |
