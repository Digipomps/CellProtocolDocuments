# Formålsspesifikasjon — studentflater skeletonhjelp

Oppgavemappe: `PDD_studentflater-skeletonhjelp_2026-11-14` · Opprettet 2026-11-14 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> «Du får i oppdrag i å lobbyere for og å sjekke at studentene får tilgang til språkmodell drevet dokument, argumentaanalyse, generell HAVEN, skriveverktøy, skeleton design hjelp så de kan sette opp sine egne dashboards og flater. Se hva som er på vei sørg for at det blir aktivt jobbet med og start nye tråder der du trenger forskning på og implementering av manglende funksjonalitet.»
>
> «Ha i bakhodet at dette skal være samarbeidsverktøy så funksjonalitet som chat er naturlig nok med»
>
> — Kjetil, 14.11.2026. Denne PDD-en dekker arbeidspakke E i audit-rapporten: **skeleton-designhjelp**.

Lest fra CellScaffold `8e8f8e0` (origin/main 13.11, samme som staging), CellProtocol `14fd9dc` (origin/main 12.11), CellProtocolDocuments `bcbd1c2`.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Studentene har ingen språkmodell på staging | retrieved (audit 14.11, ikke målt på nytt her) | /mnt/project-files/masterhaven26/sprakmodell-audit-2026-11-14.md |
| Cell Configuration Studio kan ta imot et helt CellConfiguration-utkast som cellehandling | retrieved: `setDraftConfiguration`, `setDraftSkeleton`, `importDraftConfigurationFile` (JSON-fil, maks 512 KB) | CellScaffold Sources/App/Cells/CellConfigurationStudio/CellConfigurationStudioCell.swift:182-209 |
| Studio sjekker om utkastet viser sine egne veier inn | contradicted: Studio dekoder bare; ingen kall til `SkeletonReachabilityAudit` | samme fil (grep «Reachability»: 0 treff) |
| Studio-utkast kan deles med andre | contradicted: utkast og versjoner er identitetseide og private (`DraftVersion`) | samme fil, `saveDraftVersion`/`restoreDraftVersion` |
| Architect kan foreslå CellConfiguration med modell | retrieved, delvis: knappen «Invoke architect» sender en tekstprompt til `aiGateway`; svaret er tekst og har ingen vei inn i Studio | CellScaffold Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:6141-6420 |
| Workbench-hjelperen svarer «forsto ikke» | retrieved: standardsettet er «Denne flaten» (`current-surface`), som bare kan flytte WorkItems mellom faner. Alt annet ender i `notUnderstood` | CellScaffold Sources/App/Cells/WorkbenchHelper/WorkbenchHelperCell.swift:120, 588-603; WorkbenchHelperPlanner.swift:31-41 |
| Settet «Flater og GUI» mangler «en cellehandling for forhåndsvisning og lagring av skjelett» | contradicted (delvis): Studio har den cellehandlingen i dag (`setDraftConfiguration` + `saveDraftVersion`). Teksten i settet er utdatert | WorkbenchHelperPlanner.swift:24-27 |
| Studentene kan lese skeleton-skillen | retrieved: offentlig i CellProtocol `commons/skills/cellconfiguration-skeleton-authoring/` (127 linjer). Den mangler avsnittene om synlighet og nåbarhet som den interne versjonen har, peker på Kjetils Mac-stier og på `npm run skeleton:iterate` i det private CellScaffold | CellProtocol commons/skills/cellconfiguration-skeleton-authoring/SKILL.md |
| `SkeletonReachabilityAudit` er offentlig API | retrieved: `audit(_:)` og `reachableActionKeypaths(_:)` er `public` i CellBase | CellProtocol Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:136,152 |
| Studentene kan sjekke et utkast lokalt uten CellScaffold | contradicted: CellProtocol har ingen kjørbar sjekk for en CellConfiguration-fil (bare `haven-commons` og benchmarks) | CellProtocol Package.swift:26-27 |
| Det finnes arbeid på vei for skeleton-designhjelp | contradicted: ingen åpne PR-er i CellScaffold om dette (åpne: #433-#440) | `gh api repos/Digipomps/CellScaffold/pulls` 14.11 |
| Briefen i /Users/kjetil/Build/Digipomps/HAVEN/MasterHAVEN26/sprakmodell-audit-2026-11-14/NYE_TRAADER.md | unavailable: Macen er ikke koblet til denne tråden; brukte koordinatorens sammendrag | — |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.studentflater-skeletonhjelp.root | En student lager sin egen flate, med hjelp, sammen med andre | purpose://gui.quality.functional-accessible | En ny studentkonto på staging går fra en beskrivelse med egne ord til en forhåndsvist, privat lagret flate som en medstudent kan se og kommentere | test.e2e.student-flow | candidate |
| purpose://candidate.studentflater-skeletonhjelp.guide | Studentguide: lag din egen flate | root | En student uten tilgang til CellScaffold kan følge guiden og få et eget utkast forhåndsvist i Studio på under 30 minutter | test.guide.walkthrough | candidate |
| purpose://candidate.studentflater-skeletonhjelp.public-skill-current | Den offentlige skeleton-skillen er like streng som den interne | guide | `commons/skills/cellconfiguration-skeleton-authoring` har avsnittene Visibility And Scope og Reachability, ingen Mac-stier, og sier hvordan en student uten CellScaffold forhåndsviser | test.skill.diff | candidate |
| purpose://candidate.studentflater-skeletonhjelp.local-check | Sjekk et utkast lokalt | guide | `swift run skeleton-check <fil>` i CellProtocol dekoder en CellConfiguration-fil og skriver nåbarhetsfunn og nåbare handlinger; avslutter ≠0 ved funn | test.local-check.cli | candidate |
| purpose://candidate.studentflater-skeletonhjelp.studio-audit | Studio sier fra når en flate skjuler sine egne veier inn | root | Når et utkast settes eller importeres i Studio, viser Studio nåbarhetsfunnene (element og tapte handlinger) ved siden av forhåndsvisningen | test.studio.audit | candidate |
| purpose://candidate.studentflater-skeletonhjelp.model-draft | Modellen foreslår et utkast rett inn i Studio | root | Studenten skriver hva flaten skal gjøre, trykker «Lag utkast», og får et dekodbart, nåbarhetssjekket utkast i Studio-forhåndsvisningen. Ugyldig svar gir en forklaring, aldri et tomt utkast | test.model-draft.contract, test.model-draft.invalid | candidate |
| purpose://candidate.studentflater-skeletonhjelp.model-route | Utkasthjelpen bruker den modellen studenten har tilgang til | model-draft | Samme handling virker med lokal modell, egen nøkkel eller tildelt kvote via AIGateway; uten modell sier flaten det og peker på guiden og malene | test.model-route.none, test.model-route.gateway | candidate |
| purpose://candidate.studentflater-skeletonhjelp.helper-routes | Workbench-hjelperen sender flate-bestillinger dit de kan gjøres | root | En bestilling om å lage eller endre en flate i settet «Denne flaten» gir et svar som peker på «Flater og GUI» / Studio, ikke «forsto ikke»; settet «Flater og GUI» har Studio-handlingene og en riktig «mangler»-liste | test.helper.routes | candidate |
| purpose://candidate.studentflater-skeletonhjelp.share-draft | Del et utkast med en medstudent | root | Eieren av et Studio-utkast kan gi en navngitt person lesetilgang via en Agreement; den andre ser forhåndsvisningen i sin egen Porthole og i Binding | test.share.agreement-swift, test.share.binding | candidate |
| purpose://candidate.studentflater-skeletonhjelp.discuss-draft | Snakk om utkastet i chat | share-draft | Et delt utkast kan sendes som lenke i en eksisterende gruppesamtale, og mottakerne åpner forhåndsvisningen derfra | test.share.chat-link | candidate |

Swift er referansen: Studio, hjelperen og delingen er Swift-celler i CellScaffold, og visningen skal virke i Binding (Swift) og i Porthole. Tilgang til et delt utkast avgjøres bare av Agreement-vilkår.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke nye skeleton-elementer eller ny renderer-semantikk. Kan studenten ikke få det de ber om med dagens format, sier flaten det.
- Ikke samtidig redigering av samme utkast. Deling er lesing og kommentar (chat); den andre lager sin egen kopi for å endre.
- Ikke publisering til offisielle flater. Studio-utkast forblir private eller delt med navngitte personer.
- Ikke valget av hvilken modell studentene får. Det er Kjetils beslutning (tråd A / F); denne PDD-en virker med den ruten som finnes.
- Ikke Butler i gruppesamtale (arbeidspakke F).

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Studio tar imot utkast som cellehandling | CellConfigurationStudioCell.swift:182 | Bare dekoding; ingen nåbarhetssjekk | ja; målt i kode, ikke på staging |
| Studio-forhåndsvisning for en ny studentkonto | audit 14.11 | Målt i nettleser, ikke i Binding | ja; Binding **ikke målt** |
| AIGateway `ai.invoke` for en studentkonto | AIGatewayCell.swift:472 | Ny konto har ingen rute (audit). Lokal Qwen på staging var nede | bare for model-draft; i dag **ikke tilgjengelig** |
| `SkeletonReachabilityAudit` i CellBase | SkeletonReachabilityAudit.swift | Rot-scope-betingelser rapporteres, men renderer-oppførselen endres ikke | ja |
| DraftVersion og Agreement-deling | CellConfigurationStudioCell.swift (`draft.create`, `version.get`) | Ingen delingsvei i dag | for share-draft; **ikke målt** |
| Gruppesamtale (chat) med lenker | ChatCell / Invite Chat på staging | Sara-demoen 12.11 viste chat; lenke til et delt utkast er ikke prøvd | for discuss-draft; **ikke målt** |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Studentguide «Lag din egen flate» | fil | /mnt/project-files/masterhaven26/LAG_DIN_EGEN_FLATE.md og CellProtocolDocuments (PR) | — | nei |
| Oppdatert offentlig skeleton-skill | fil (PR) | CellProtocol commons/skills/cellconfiguration-skeleton-authoring/ | — | nei |
| `skeleton-check` kjørt på et godt og et dårlig eksempel | testutdata | TESTRESULT.md#local-check | — | nei |
| Studio med «Beskriv flaten» + «Lag utkast» og nåbarhetsfunn, tom / utfylt / feil | bilde | images/studio-utkast-{tom,utfylt,feil}-v1.png | rendres etter G1 | nei |
| Workbench-hjelperen svarer på «lag en flate som viser oppgavene mine» | bilde + testutdata | images/hjelper-flate-v1.png, TESTRESULT.md#helper | rendres etter G1 | nei |
| Delt utkast sett fra medstudentens konto, web og Binding | bilde | images/delt-utkast-{web,binding}-v1.png | rendres etter G1 | nei |
| Kjørende flyt på staging for en ny studentkonto | kjørende flate | staging, via FORESPOERSEL til Deploy etter verifisert bygg | — | nei |

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

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
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
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
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
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.shared-cellresolver-fixture-unique-names** (2026-10-12, minor): Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.
    - forebygging: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | `swift build` CellProtocol og CellScaffold på Macen; Binding i Xcode | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Full `swift test` CellProtocol + CellScaffold; BindingTests; antall før/etter | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med mappen | ACCEPT.md#status | venter |
| test.guide.walkthrough | guide | En fersk tråd uten CellScaffold følger guiden mot staging med ny konto; tid og hvert avvik loggføres | TESTRESULT.md#guide | venter |
| test.skill.diff | public-skill-current | Diff mot intern skill; grep etter `/Users/` gir 0 treff; avsnittene finnes | TESTRESULT.md#skill | venter |
| test.local-check.cli | local-check | `swift run skeleton-check` på et eksempel uten funn (exit 0) og et med rot-portet seksjon (exit 1, navngir tapt handling) | TESTRESULT.md#local-check | venter |
| test.studio.audit | studio-audit | Celletest: utkast med rot-portet knapp → `state.reachability.findings` har elementet og keypathen | TESTRESULT.md#studio | venter |
| test.model-draft.contract | model-draft | Celletest med fast modellsvar: gyldig JSON → utkast satt, audit kjørt, kilde «modell» | TESTRESULT.md#model-draft | venter |
| test.model-draft.invalid | model-draft | Fast modellsvar som ikke dekoder / bruker ukjent element → forklaring, utkastet uendret | TESTRESULT.md#model-draft | venter |
| test.model-route.none | model-route | Konto uten rute: knappen gir «ingen modell tilgjengelig» med lenke til guiden, ingen tom tilstand | TESTRESULT.md#model-route | venter |
| test.model-route.gateway | model-route | Ekte kall via AIGateway med den ruten Kjetil velger, på staging | TESTRESULT.md#model-route | blocked (ingen rute) |
| test.helper.routes | helper-routes | Planner-test: «lag en flate som viser oppgavene mine» i «Denne flaten» → peker på «Flater og GUI»; i «Flater og GUI» → Studio-handling foreslås | TESTRESULT.md#helper | venter |
| test.share.agreement-swift | share-draft | Swift-celletest: navngitt person får lese via Agreement-vilkår; fremmed nektes; tilbakekalt nektes | TESTRESULT.md#share | venter |
| test.share.binding | share-draft | Binding viser det delte utkastet (snapshot-korpus eller kjørende app) | TESTRESULT.md#share | venter |
| test.share.chat-link | discuss-draft | Lenke i gruppesamtale åpner forhåndsvisningen for et medlem | TESTRESULT.md#share | venter |
| test.e2e.student-flow | root | Playwright på staging med to ferske kontoer: beskriv → utkast → lagre → del → se | TESTRESULT.md#e2e | venter |
| test.reachability.shipped | studio-audit, helper-routes | Nye/endrede flater (Studio, Workbench) gjennom `testNoLocalSurfaceHidesItsOwnWaysIn` | TESTRESULT.md#reachability | venter |

## 6. Åpne spørsmål til Kjetil

1. **Rekkefølge.** Forslag: guide, offentlig skill, `skeleton-check` og Studio-audit først (virker uten modell), så hjelper-rettingen, så modell-utkast, så deling. Ok?
2. **Deling.** Er «les + chat, egen kopi for å endre» riktig første steg, eller vil du ha felles redigering av samme utkast?
3. **`skeleton-check` i CellProtocol.** Et nytt kjørbart mål i det offentlige repoet. Ok å legge det der (krever tag/pin-runde), eller heller et skript i CellProtocolDocuments som bruker CellBase som avhengighet?

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-11-14 | Opprettet | Losen |
| 1 | 2026-11-14 | §0-§3, §5, §6 skrevet fra kode på origin/main | Claude (tråd «Gi studentene hjelp til å designe egne flater») |
