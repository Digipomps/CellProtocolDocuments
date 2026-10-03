# Formålsspesifikasjon — arbeidsko ai utforere

Oppgavemappe: `PDD_arbeidsko-ai-utforere_2026-09-07` · Opprettet 2026-09-07 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Ok - dette var ikke noe særlig vellykket. Vi må få opp en enklere måte å gjøre dette på. Det er veldig lite effektivt at jeg skal lime inn kommandoer og det øker risikoen for feil. Altså vi må få fikset så vi kan bruke agenten til å køe jobber som den kan gi til deg, codex eller celle-baserte ai agenter.

Hendelsen bak: 2026-09-07 fikk Kjetil et innlimingsskript med et ugyldig flagg (`--full-auto` finnes ikke på `codex exec`), mens en fungerende kø (`HAVEN/_losen-queue`, 38 fullførte jobber) allerede fantes og ikke ble brukt. Feilen var to ting: kommando gitt til et menneske i stedet for til en kø, og køen var ukjent for økten. Begge er formål under.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| `_losen-queue` finnes: launchd hvert 60 s, én jobb om gangen, `codex exec --sandbox <read-only|workspace-write> --skip-git-repo-check -C <cwd>`, cwd må ligge under HAVEN, ingen vilkårlig shell; svar i `done/<id>.svar.md` | retrieved | `HAVEN/_losen-queue/runner.sh`, `LES_MEG.md`, `org.digipomps.losen-queue.plist` |
| Runneren er i drift (jobber 04.09, 06.09, 07.09 12:19Z START husk-impl) | retrieved | `_losen-queue/logs/runner.log` |
| Runneren har en kjent skavank: `flock: command not found` i `launchd.err` (linje 13) — låsen bruker `mkdir`, så feilen er kosmetisk men støyer | retrieved | `_losen-queue/logs/launchd.err` |
| HAVEN-Deploy har allerede en kø-modell med sannhet i filer: `queue/tasks/<id>.json` + append-only `queue/events/`, `hd`-CLI, statusvokabular, `owner`/`executed_by` ∈ kjetil/claude/codex/ci, `needs`, `depends_on`, lessons, regler, rådgiver | retrieved | `HAVEN-Deploy/CONTRACT.md`, `FORMAAL.md` F1–F7, `AGENTS.md` |
| HAVEN-Deploy sier selv: «Codex tar … lange jobber på Mac-en via `codex exec` under launchd», og B3: signalmatching er *ikke* kø-motor; B1(d): celler er lesere/visere, ikke lager | retrieved | `HAVEN-Deploy/AGENTS.md`, `docs/Arkitektur.md` B1, B3 |
| `hd board` viser 9 poster (HD-0002…HD-0011) med eier og blokkeringer — køen er i bruk | retrieved | `python3 tools/hd.py board` 2026-09-07 |
| Fra Cowork kan Losen skrive filer i tilkoblede mapper, men ikke starte prosesser på Mac-en; Codex-MCP og `launchctl` via MCP avvises av klassifisereren for skrivende arbeid | retrieved (denne økten) | feilmeldinger 2026-09-07; `feedback_codex_queue.md` |
| Claude som utfører på Mac-en (Claude Code CLI `claude -p`) | retrieved — `/Users/kjetil/.local/bin/claude` → Claude Code 2.1.221; codex-cli 0.153.4; docker.sock finnes men nektes i Codex-sandkassen | `_losen-queue/done/env-check-20260907-2004.svar.md` |
| Claude som utfører i skyen (Cowork planlagte oppgaver, `create_trigger`/`fire_trigger`) | retrieved — finnes i Losens verktøy; kan startes bare fra en Claude-økt, ikke fra Mac-en | verktøylisten denne økten |
| Cellebasert AI-utfører | unavailable — `AIGatewayCell` finnes i CellScaffold; `cell:///AdvisorPanel` er besluttet (PDD_radgiverpanel-og-persona_2026-09-05), ikke levert | minne 2026-09-05 |

## 1. Formålstre

Rot: Losen (og senere andre agenter) legger en jobb i én kø med utfører, avhengigheter og akseptkrav — uten at Kjetil er postbud — og jobben kjører hos riktig utfører (Claude, Codex eller celle-agent), med resultat, status og lærdom tilbake på ett sted Kjetil kan se. Invariant (fra HAVEN-Deploy F6): sannheten er filer i git; ikke bytt ut ved neste deploy.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.arbeidsko.root | Én arbeidskø, tre utførere, ingen postbud | HAVEN-Deploy F1 (kø) · F6 (vekst) | En jobb Losen skriver fra Cowork kl. T kjører hos angitt utfører innen T+2 min uten at Kjetil gjør noe, og resultatet ligger som fil + hendelse innen jobben er ferdig. | `test.ko.e2e` (én jobb per utfører) | candidate |
| purpose://candidate.arbeidsko.one-job-format | Ett jobbformat = HAVEN-Deploy-task | root | Jobben er en `haven.deploy.task.v1`-post med `mutation_type: none|code`, nytt felt `executor ∈ codex|claude-local|claude-cloud|cell` og `job: {prompt_ref, cwd, sandbox, timeout_s, accept}`. `_losen-queue`-formatet (to filer) blir en *utfører-adapter*, ikke et eget køformat. Skjemaet i `schema/task.schema.json` utvides bakoverkompatibelt; eksisterende HD-poster validerer uendret. | `test.ko.schema` | candidate |
| purpose://candidate.arbeidsko.dispatcher | Dispatcher på Mac-en | root | Én launchd-jobb (generalisering av `runner.sh`) leser `queue/tasks/*.json` med status `READY` og oppfylte `depends_on`, tar én jobb per utfører om gangen, skriver `job.started`/`job.finished`/`job.failed`-hendelser (append-only, deterministisk id), håndhever `timeout_s`, og fjerner aldri en jobb — feil gir `HANDOFF_REQUIRED` etter HAVEN-Deploys R-F45. Ingen vilkårlig shell: dispatcheren kjenner bare utfører-adaptere. | `test.ko.dispatch` | candidate |
| purpose://candidate.arbeidsko.executor-codex | Utfører: Codex | dispatcher | Adapter = dagens `runner.sh`-kommando (`codex exec --sandbox … --skip-git-repo-check -C …`). Svar til `queue/results/<id>.md`, stderr til `logs/`. `flock`-støyen fjernes. | `test.ko.codex` | candidate |
| purpose://candidate.arbeidsko.executor-claude | Utfører: Claude | dispatcher | To adaptere, valgt per jobb: `claude-local` (Claude Code CLI på Mac-en, `claude -p` med eksplisitt verktøyliste og cwd under HAVEN) og `claude-cloud` (Cowork planlagt oppgave, startes av en Claude-økt som *ser* jobben — dispatcheren kan ikke nå skyen). Minst én av dem må virke ende-til-ende; hvilken avgjøres av §6.2. | `test.ko.claude` | candidate |
| purpose://candidate.arbeidsko.executor-cell | Utfører: celle-agent | dispatcher | Adapter som sender `job.prompt` til en agent-celle over HTTP (`cell:///AIGatewayCell` i lokal CellScaffold nå; `cell:///AdvisorPanel` når den finnes) og henter svaret som resultatfil. Cellen får aldri filsystem- eller shell-tilgang gjennom køen — bare tekst inn, tekst ut. | `test.ko.cell` | candidate |
| purpose://candidate.arbeidsko.queue-from-cowork | Losen kan legge jobb uten Kjetil | root | `hd task new … --executor codex --job-prompt <fil>` (eller å skrive task-JSON direkte) fra Cowork-VM-en via mount er nok til at jobben kjører. Ingen `launchctl`, ingen MCP-kjøring, ingen innliming. | `test.ko.from-cowork` | candidate |
| purpose://candidate.arbeidsko.visible | Køen er synlig | root | `hd board` viser arbeidsjobber med utfører og status ved siden av deploy-poster, og en read-only celle (`WorkQueueViewCell`, B1(d)) eksponerer det samme til en skeleton-flate i HAVEN. GUI-delen krever bilde før kode. | `test.ko.board`, `test.gui.reference-image-exists` | candidate |
| purpose://candidate.arbeidsko.learns | Feilede jobber blir lessons | root | Hver `job.failed` med samme fingeravtrykk to ganger → `HANDOFF_REQUIRED` + `hd lesson new` innen 48 t (HAVEN-Deploy G7.1). Innlimingsfeilen 2026-09-07 registreres som første lesson. | `test.ko.lesson` | candidate |
| purpose://candidate.arbeidsko.no-arbitrary-shell | Skal ikke: køen kjører vilkårlige kommandoer | root · polarity: prohibited | Jobbposten inneholder aldri en kommando; bare utfører, prompt-referanse, cwd (under HAVEN), sandkasse og timeout. Dispatcheren avviser alt annet. Hemmeligheter når aldri jobbfil eller hendelse (HAVEN-Deploy G4.4). | `test.ko.no-shell` | candidate |
| purpose://candidate.arbeidsko.no-self-escalation | Skal ikke: en jobb kan gi seg selv mer tilgang | root · polarity: prohibited | En jobb kan ikke opprette eller endre en annen jobb med videre sandkasse/utfører enn sin egen; bare Kjetil/Losen-økt kan legge jobber med `workspace-write`. | `test.ko.no-escalation` | candidate |

Utenfor treet: signalmatching som kø-motor (HAVEN-Deploy B3: nei), grafdatabase (B2: måles først), ruting av jobber til utfører ved matching (én utvikler), fjernkjøring over ssh (AGENTS.md: ingen ssh).

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en ny kø ved siden av HAVEN-Deploy. Det er HAVEN-Deploys kø + en dispatcher + utfører-adaptere. `_losen-queue` fases inn som Codex-adapteren og pensjoneres som eget format.
- Ikke en agent-orkestrator med planlegging. Avhengigheter er `depends_on`; rekkefølge er dispatcherens; ingen LLM velger utfører.
- Ikke deploy på verten. Dispatcheren kjører bare på Mac-en; vert-mutasjoner følger HAVEN-Deploys claim-regler uendret.
- Ikke et nytt GUI først. `hd board` er flaten til bildet for `WorkQueueViewCell` er godkjent.

| Kapabilitet / avhengighet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| launchd-agent på Mac-en (installert én gang av Kjetil) | `_losen-queue/org.digipomps.losen-queue.plist` | Den eneste handlingen som krever Kjetil: bytte plist til den nye dispatcheren (`launchctl unload/load`) — én gang | ja |
| `hd`-CLI, task/event-skjema, `hd reindex` | `HAVEN-Deploy/tools/hd.py`, `schema/*.json`, `CONTRACT.md` | stdlib-only python ≥3.10; utvidelse må holde `python3 -m unittest tests/test_hd.py` grønn | ja |
| `codex exec` med `--sandbox`/`--skip-git-repo-check`/`-C` | `_losen-queue/runner.sh` | flagg verifisert i drift; `--full-auto` finnes ikke på `exec` | ja |
| Claude Code CLI på Mac-en | ukjent | verifiseres først; uten den finnes bare `claude-cloud` | ja — §6.2 |
| Agent-celle med HTTP-endepunkt lokalt | CellScaffold `AIGatewayCell` | krever kjørende scaffold; modell-nøkkel i cellens hemmelighetsceller, aldri i jobben | ja — for `test.ko.cell` |
| Mount fra Cowork er ikke git | lesson.mount-is-not-git | dispatcheren og Losen gjør aldri git-mutasjon; hendelsesfiler er skrevet én gang og committes av Kjetil/Codex | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| `schema/task.schema.json` utvidet med `executor` og `job`; `hd task new --executor … --job-prompt …`; `hd board` med arbeidsjobber | fil + testutdata | `HAVEN-Deploy/` | `tests/test_hd.py` grønn | nei |
| `tools/dispatch.py` + `org.digipomps.haven-dispatch.plist` (erstatter `_losen-queue/runner.sh`), med `LES_MEG.md` | fil | `HAVEN-Deploy/tools/`, `HAVEN-Deploy/launchd/` | — | nei |
| Adaptere `tools/executors/{codex,claude_local,claude_cloud,cell}.py` | fil | `HAVEN-Deploy/tools/executors/` | — | nei |
| Én jobb per utfører kjørt ende-til-ende fra Cowork, med hendelser og resultatfiler | testutdata | `TESTRESULT.md#e2e` + `queue/events/` | — | nei |
| `lessons/L-2026-09-07-innliming-i-stedet-for-ko.json` + regel som nekter jobbposter med `command`-felt | fil | `HAVEN-Deploy/lessons/`, `rules/` | — | nei |
| `_losen-queue/LES_MEG.md` merket «pensjonert → HAVEN-Deploy/tools/dispatch.py» | fil | `HAVEN/_losen-queue/` | — | nei |
| Skeleton-flate «Arbeidskø» (senere; bilde først) | bilde | `images/arbeidsko-v1.png` | — | nei |

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
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.

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
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://human-agency [draft] — Human agency and understanding
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.participation [draft] — Event participation
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://grounding [active] — Grounding

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
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | ./<skript>.sh (uten --go) | TESTRESULT.md#dry-run | venter |
| test.ko.schema | one-job-format | `python3 -m unittest tests/test_hd.py` + ny test: HD-post uten `executor` validerer; jobb med `executor: codex` validerer; jobb med `command`-felt avvises. | TESTRESULT.md#schema | venter |
| test.ko.dispatch | dispatcher | Enhetstest med falsk utfører: to jobber med `depends_on` kjøres i rekkefølge; timeout gir `job.failed`; samme fingeravtrykk ×2 → `HANDOFF_REQUIRED`; ingen jobb slettes. | TESTRESULT.md#dispatch | venter |
| test.ko.codex | executor-codex | Ekte jobb: `read-only` prompt «list filene i PalazzoScaffold/Sources/App/Cells» → resultatfil med listen; `launchd.err` uten `flock`-linjer. | TESTRESULT.md#codex | venter |
| test.ko.claude | executor-claude | Ekte jobb i valgt adapter: prompt «skriv dagens dato i queue/results/<id>.md» → fil finnes. | TESTRESULT.md#claude | venter |
| test.ko.cell | executor-cell | Ekte jobb mot lokal AIGatewayCell: prompt → svar i resultatfil; cellen har ingen fil-/shell-tilgang (inspeksjon av adapteren). | TESTRESULT.md#cell | venter |
| test.ko.from-cowork | queue-from-cowork | Losen skriver task-JSON via mount fra denne økten; jobben starter innen 2 min uten annen handling (runner.log). | TESTRESULT.md#from-cowork | venter |
| test.ko.board | visible | `hd board` viser jobben med utfører/status; `WorkQueueViewCell` leser samme indeks (når bygd). | TESTRESULT.md#board | venter |
| test.ko.lesson | learns | Lesson-fil for 07.09 finnes med `rule_id`; `preflight.py` slår ned på jobbpost med `command`. | TESTRESULT.md#lesson | venter |
| test.ko.no-shell | no-arbitrary-shell (antiformål) | Jobbpost med `command`/`script`-felt avvises av `hd` og av dispatcheren; grep i adaptere viser ingen `subprocess` med brukerstyrt streng utenfor de tre faste kommandoene. | TESTRESULT.md#no-shell | venter |
| test.ko.no-escalation | no-self-escalation (antiformål) | Jobb kjørt som `read-only` forsøker å skrive ny jobb med `workspace-write` → dispatcheren avviser (opphav = jobb-id, ikke Losen/Kjetil). | TESTRESULT.md#no-escalation | venter |
| test.ko.e2e | root | Tre jobber (codex, claude, cell) lagt fra Cowork → alle `job.finished` med resultatfil, uten at Kjetil gjorde noe etter plist-byttet. | TESTRESULT.md#e2e | venter |

## 6. Åpne spørsmål til Kjetil

Besvart 2026-09-07 (Kjetil: «ingen grunn til å ikke gjøre det»; Losens forslag gjelder): 1 samme kø · 2 `claude-local` primær (CLI finnes), `claude-cloud` sekundær · 3 AIGatewayCell nå · 4 bare Kjetil/Losen-økt kan legge workspace-write · 5 GUI etter.

Opprinnelige spørsmål:

1. **Samme kø som HAVEN-Deploy, eller egen?** Forslag: samme (task/event-modellen, `hd`, board, lessons — én sannhet, og F6 «ikke bytt ut»). `_losen-queue` blir Codex-adapteren og pensjoneres som format. Alternativ: egen lettvekts-kø ved siden av.
2. **Claude-utfører:** er Claude Code CLI installert på Mac-en? Hvis ja → `claude-local` først (dispatcheren kan starte den). Hvis nei → bare `claude-cloud` (Cowork planlagte oppgaver), som krever at en Claude-økt ser køen — jeg kan sette opp en planlagt oppgave som sjekker køen hver time. Forslag: begge, `claude-local` som primær hvis den finnes.
3. **Celle-utfører nå eller vente på AdvisorPanel-cellen?** Forslag: adapter mot `AIGatewayCell` nå (tekst inn/ut), byttes til `cell:///AdvisorPanel` når den er levert — samme adapter-grensesnitt.
4. **Hvem kan legge jobber med `workspace-write`?** Forslag: bare Kjetil og Losen-økter (opphav i posten); jobber kan bare legge `read-only`-jobber. 
5. **GUI-flate «Arbeidskø» i HAVEN** — nå (bilde først) eller etter at `hd board` har vist seg tilstrekkelig? Forslag: etter.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-07 | Opprettet | Losen |
| 2 | 2026-09-07 | §0: Claude CLI verifisert (env-check-jobb); §6 besvart; G1/G2 satt | Kjetil/Losen |
| 1 | 2026-09-07 | §0 audit (10 rader), §1 tre med 9 formål + 2 antiformål, §2, §3 (7 leveranser), §5 +11 tester, §6 fem spørsmål; venter G1 | Losen |
