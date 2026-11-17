# TESTRESULT — arbeidskø AI-utførere

Last verified against code: 2026-09-07. Utfører: Codex. WP0–WP6 implementert i
rekkefølge. WP7 ikke utført; G3 blocked. [Samlet rapport](../../../HAVEN-Deploy/docs/Rapport_Arbeidsko_2026-09-07.md).
Alle stier under peker til den leverte HAVEN-Deploy-køen.

## build

**pass med runtime-avgrensning.** `python3 -m compileall -q tools` bestod.
`ast.parse(..., feature_version=(3,10))` bestod for 45 Python-filer i tools/tests.
Stdlib-only; kjørt med Python 3.13.2. Ingen faktisk Python 3.10.12-kjøring utført.
Plist parses med plistlib: StartInterval 60, --once, `/usr/local/bin/python3`.
`/usr/bin/python3` er 3.9.6 og brukes ikke i den leverte plisten.
[Byggbevis](../../../HAVEN-Deploy/logs/wp6-build.json).

## regression

WP0: `python3 tools/hd.py validate` → 240 records, 0 problems.
`python3 -m unittest tests/test_hd.py tests/test_preflight.py` → 60 tests, OK.
**Avvik:** eksisterende git-fixture startet git i tempkatalog, i strid med brukerens
forbud. Ingen git rettet mot HAVEN-repoene. Ingen eksisterende testfil endret.

Slutt: `python3 tools/test_no_git.py` → **88 tester, 87 bestått, 1 skippet, 0 feil**.
59 eksisterende + 28 nye tester bestod. Den ene git-fixturen skippes via sin
opprinnelige tilgjengelighetskontroll; alle git-subprosesser sperres av audit hook.
`hd validate` → **267 records, 0 problems**. Eksisterende ResourceWarning beholdt.
[Regresjonslogg](../../../HAVEN-Deploy/logs/wp6-regression.log).
Full T0/T1 har eksisterende ENV-001/SH-005-blokkeringer og Mac-path-advarsel;
KO-001 pass, 0 motorfeil. [Preflight](../../../HAVEN-Deploy/logs/wp6-preflight.json).

## schema

**pass.** TestWorkSchema: eldre task uten executor validerer; work-record validerer;
ukjente jobbfelt, ugyldig executor, timeout/type, stier, symlink-escape, sensitive
mønstre og feil livsløp avvises. READY/RUNNING brukes bare til arbeidsjobber.
`hd`-validering og dispatcher deler samme semantiske validator.
[Testkilde](../../../HAVEN-Deploy/tests/test_work.py).

## dispatch

**pass i kontrollerte tester.** Avhengigheter fullføres i rekkefølge; manglende,
sykliske og uoppfylte behov venter. Samtidige dispatchere utfører en jobb én gang;
låst Codex hindrer ikke Claude. En faktisk Python-underprosess tidsavbrytes.
Feil/akseptbrudd gir handoff, jobbfiler beholdes, retry beholder forsøksbevis.
Event-ID beregnes om og valideres. Reindeks av faktisk kø to ganger ga identiske
rader. [Tester](../../../HAVEN-Deploy/tests/test_dispatch.py),
[indeksbevis](../../../HAVEN-Deploy/logs/wp6-reindex.json).

## codex

**blocked — ekte kjøring forsøkt.** HD-0013, read-only, timeout 120:
`python3 tools/dispatch.py --once --task HD-0013` → exit 1/HANDOFF_REQUIRED.
CLI-feil: app-server-initialisering, Operation not permitted. Ingen filoversikt.
job.started `ev_00708540e730a4c2`; job.failed `ev_104ffc8678ef5606`.
[Resultat](../../../HAVEN-Deploy/queue/results/HD-0013.md),
[stderr](../../../HAVEN-Deploy/logs/HD-0013.attempt-1.stderr.log).
Fast argv/enkelt promptargument, --sandbox, --skip-git-repo-check og -C er testet.
Ingen flock-kall er introdusert; ny launchd-logg er ikke runtime-testet før WP7.

## claude

**blocked — ekte kjøring forsøkt.** HD-0014, read-only, timeout 90:
`python3 tools/dispatch.py --once --task HD-0014` → exit 1/HANDOFF_REQUIRED.
CLI-svar: Not logged in · Please run /login. Datoprompten skulle returnere dato
som stdout, deretter skulle dispatcheren skrive resultatfilen. Ingen datotekst
produsert, og ingen workspace-write-test gjennomført.
job.started `ev_f51efb7a42611850`; job.failed `ev_3d7b13dbaa995583`.
[Resultat](../../../HAVEN-Deploy/queue/results/HD-0014.md).

`claude --help` bekreftet brukte flagg på 2.1.221. Testet slutt-argv med --tools,
--allowedTools, dontAsk, safe-mode, ingen MCP/plugins og prompt etter --.
Read-only: Read/Glob/Grep. Workspace-write: tillegg Edit/Write, rettighet via
Edit(//cwd/**), som gjelder begge verktøy. Denne herdingen ble ferdigstilt etter
den blokkerte ekte prøven; innlogget kjøring av sluttversjonen gjenstår.
claude-cloud-stubb har exit 78 / status: not-implemented.
[Tester](../../../HAVEN-Deploy/tests/test_executors.py),
[lokal CLI-hjelp](../../../HAVEN-Deploy/logs/claude-help.txt).

## cell

**blocked for levende scaffold; kontrakttester pass.** HD-0015:
`python3 tools/dispatch.py --once --task HD-0015` → exit 69/HANDOFF_REQUIRED,
cell unavailable: URLError. Loopback 8080/8081 nektet EPERM fra denne sandkassen.
Dette beviser ikke fravær av scaffold. Ingen autorisert Porthole-session/model
kunne verifiseres. job.failed `ev_c333e525e35faef9`.
[Resultat](../../../HAVEN-Deploy/queue/results/HD-0015.md).

Kildekontroll korrigerte endpoint til cell:///AIGateway, keypath aiGateway.ai.invoke,
POST /porthole/action med {keypath,payload}. Positiv konvolutt, diagnostikkfeil,
denial, tomt svar, timeout og samme-origin polling testes med kontrollerte svar;
HTTP-server kjøres ikke i disse testene. Cellen mottar bare prompttekst, aldri
filsystem-/shellargumenter. [Tester](../../../HAVEN-Deploy/tests/test_cell_executor.py).

## board

**pass for CLI.** TestWorkBoard verifiserer egen arbeidsseksjon med utfører/status/
alder, work list/show og event-snapshot ved manglende cache. Ekte board viser
HD-0013/0014/0015 som HANDOFF_REQUIRED.
[Board-bevis](../../../HAVEN-Deploy/logs/wp6-board.txt).
WorkQueueViewCell og skeleton er ikke implementert; WP-GUI forblir blocked.

## lesson

**pass.** Timeout to ganger på samme jobb gir identisk fingerprint,
FINGERPRINT_REPEAT, HANDOFF_REQUIRED og lesson-stubb. Første feil stopper også
og krever eksplisitt retry-notat. Hver ekte prøvefeil har en lesson-stubb.
[L-2026-09-07-innliming-i-stedet-for-ko](../../../HAVEN-Deploy/lessons/L-2026-09-07-innliming-i-stedet-for-ko.json)
peker til KO-001. Preflight-test viser at command/script og job-origin med
workspace-write utløser denne blokkerende regelen.
Git-avviket er registrert i en separat lesson med test_no_git.py som forebygging.

## no-shell

**pass for køformat/dispatch.** job har additionalProperties:false; CLI og
semantisk validator nekter kommandoposter for work. Direkte manipulert JSON med
command når aldri adapteren. Kun fast register i executors kan velge kode.
Subprocess bruker argv-lister og shell=False; prompt etter -- i Codex/Claude.
Celle-worker mottar prompt på stdin og sender bare tekst over HTTP.
Dette forbyr kommandofelt i køen; det betyr ikke at Codex mangler egne verktøy
innen sin valgte sandkasse.

## no-escalation

**pass for deklarert opphav/negative kodeprøver; ekte agentprøve blocked.**
HAVEN_JOB_ID tvinger job:<id> i CLI; slike jobber får bare read-only og samme
executor som forelder. Validator/KO-001 avviser eskalerende direkte JSON.
Sterk autentisering av origin på et delt skrivbart filsystem er **ikke levert**:
en prosess med eksisterende fri skriverett kan forfalske metadata. Det er ingen
påstand om sterk isolasjon mellom slike produsenter.

## from-cowork

**blocked.** En kontrollert test publiserer direkte task-JSON og får resultat via
produksjonsdispatcheren med falsk utfører. Dette er ikke en ekte Cowork-mount-test.
Losen må utføre den etter Kjetils WP7; mål oppstart innen to minutter.

## e2e

**blocked.** Ingen ny launchd-plist er installert. Ingen av de ekte modellprøvene
produserte et vellykket resultat. Neste eiere: Kjetil for runtime/autentisering,
lokal session og WP7; Losen for faktisk Cowork → launchd → resultat hos utførerne.
Kommandoer og vilkår: [Arbeidsko.md](../../../HAVEN-Deploy/docs/Arbeidsko.md) og
[Arbeidsko-drift.md](../../../HAVEN-Deploy/docs/Arbeidsko-drift.md).
