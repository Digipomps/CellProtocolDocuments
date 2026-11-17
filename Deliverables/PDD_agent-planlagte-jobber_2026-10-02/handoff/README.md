# Handoff: rekkefølge og kommandoer

PDD `agent-planlagte-jobber`, G2-artefakt, 02.10.2026. Dette er det som går til køene på Macen, i rekkefølge. Ingen kommandoer her er ment for Kjetil. Alt kjøres av køene som finnes, og Losen (tråden i prosjektet «HavenAgentD») legger jobbene inn.

Hver bolk er merket **godkjent** eller **venter**. En bolk som venter, legges ikke i noen kø.

## De to køene

| Kø | Brukes til | Jobben er |
|---|---|---|
| `.agent-spool` | `git`, `gh`, `swift build` og `swift test` | en JSON-fil i `.agent-spool/inbox/`, skrevet som `<id>.json.partial` og omdøpt. Resultatet kommer i `.agent-spool/outbox/<id>.result.json` og `<id>.log`. |
| `_losen-queue`, modus `skript` | alt som rører agentens mapper eller tjenester | én navngitt `.sh` under `HAVEN-Deploy/_handoff/`. To filer i innboksen: `<id>.prompt.md` først, så `<id>.job` flyttet inn med `mv`. Banen tildeles av kø-tråden etter en linje i `_losen-queue/KOORDINERING.md`. |

Regler som gjelder alle skriptene:

- Tørrkjøring er standard. De kan kjøres flere ganger uten å gjøre noe to ganger.
- Utdataene havner i en fil under `HAVEN-Deploy/_handoff/`, for køen sender skriptets stdout dit. De bærer derfor aldri tokenet, og ID-liknende tekst er byttet med `<id>`.
- De skriver hva de har gjort og målt til stdout, og aldri tokenet til kontrollbroen.
- Køen kjører skriptet med `bash` (`runner.sh` linje 170–172), og macOS har bash 3.2. Skriptene her er skrevet for det. Et zsh-skript, som `Scripts/install-agent-dev.sh`, kalles uttrykkelig med `/bin/zsh` fra en omslagsfil.
- Sjekksummer tas med `shasum -a 256`. Tid skrives med `date -u +%Y-%m-%dT%H:%M:%SZ`.
- Køen kjører bare når Codex-binæren finnes, også for skriptjobber (`runner.sh` linje 20). Mangler den, står jobben.
- `git` kjøres aldri gjennom den tilkoblede mappen fra skyen.

## S0 — over på køene som finnes · **godkjent 02.10** (Kjetil: «HAVEN-roten») · **gjort 03.10**

Resultatet (03.10 ca. kl. 09:20Z, `HAVEN/.agent-spool/outbox/planlagte-jobber-s0-maaling-20261003.result.json`):

- `.agent-spool` lever, og `git push --dry-run` svarte `[new branch]`. Køen kan skyve en gren til `Digipomps/HavenAgentD`.
- `gh` finnes ikke i den køens søkesti (`[Errno 2] No such file or directory: 'gh'`). En PR opprettes derfor som skriptjobb i `_losen-queue`, eller for hånd.
- Hovedutsjekken av HavenAgentD står på `main`, 1 foran og 42 bak `origin/main`, med endrede og usporede filer. Den røres ikke.
- Den gamle løperen gikk ikke (ingen `runner.lock`). `STOP` er lagt i køen dens, og `.command`-fila har fått navnet `agentd-runner.command.utgaatt-20261002`. Punkt 2 under ble derfor ikke gjort: signaturen leses som skriptjobb i `_losen-queue` før S3.
- Punkt 8 er lagt til i `_losen-queue/KOORDINERING.md`.

Slik var S0 planlagt:

1. **Mål køen.** Jobben under legges i `.agent-spool/inbox/`. Den endrer ingenting.

   ```json
   {
     "cwd": "HavenAgentD",
     "stopOnFailure": false,
     "steps": [
       {"name": "git", "cmd": ["git", "status", "--short", "--branch"], "timeoutSeconds": 60},
       {"name": "gh", "cmd": ["gh", "api", "user", "--jq", ".login"], "timeoutSeconds": 60},
       {"name": "push-toerr", "cmd": ["git", "push", "--dry-run", "origin", "HEAD:refs/heads/koe-proeve-20261002"], "timeoutSeconds": 60}
     ]
   }
   ```

   Ferdig når `outbox/<id>.result.json` finnes. Steget `push-toerr` sender ingenting og oppretter ingen gren; det viser om køen har nøkler til å skyve en gren. Grennavnet finnes ikke på GitHub, så svaret avhenger ikke av om den lokale kopien er oppdatert. «new branch» eller «rejected» betyr at køen nådde GitHub med nøkler som kan skyve. «Permission denied», «Authentication failed» eller «could not read Username» betyr at den ikke kan. Feiler `gh` eller `push-toerr`, går det arbeidet som navngitte skript i `_losen-queue`, som har Homebrew i søkestien (`runner.sh` linje 13).
2. **Les signaturen på binærene som er installert** (`codesign -dv` på de tre i `~/Library/Application Support/HAVENAgent/bin/`). Det er siste jobb for den gamle løperen i Terminal-vinduet.
3. **Stopp den gamle løperen.** Fila `HavenAgentD/.tmp-clang-module-cache/agentd-diag/queue/STOP` opprettes. Løperen avslutter innen tre sekunder og fjerner `runner.lock`. `HavenAgentD/Claude outputs/agentd-runner.command` får navnet `agentd-runner.command.utgaatt-20261002`. Mappen med jobbloggene blir stående; den er bevis for utsettingen 30.09.
4. **Én linje i `_losen-queue/KOORDINERING.md`** om at løperen er stoppet.

## S1 — kilden til korrespondansevakten · **godkjent 05.10 (G2)** · **gjort 05.10**

Resultatet (05.10): arbeidstreet og grenen finnes, korrespondansevakten er commit `1ee0abb`, og PR #30 mot `main` er opprettet (https://github.com/Digipomps/HavenAgentD/pull/30). PR-en har også trinn 3 og tre små rettelser, se S3. Skriptet som opprettet PR-en, er `HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/opprett-pr.sh`.

Slik var S1 planlagt:

Gren `claude/planlagte-jobber-20261002` fra `origin/main`, i eget arbeidstre. Opprettes med en jobb i `.agent-spool`:

```json
{
  "cwd": "HavenAgentD",
  "steps": [
    {"name": "hent", "cmd": ["git", "fetch", "origin", "main"], "timeoutSeconds": 300},
    {"name": "tre", "cmd": ["git", "worktree", "add", ".worktrees/planlagte-jobber-20261002", "-b", "claude/planlagte-jobber-20261002", "origin/main"], "timeoutSeconds": 120}
  ]
}
```

Filene som skrives i arbeidstreet:

| Fil | Innhold |
|---|---|
| `Scripts/scheduled/korrespondanse_vakt.py` | programmet, etter `contract/trinn1-2-programmer.md` |
| `Scripts/install-scheduled-tasks.sh` | inngangen til installasjonen, se S2. Bash 3.2. Finner `/usr/bin/python3` og starter rutinen. |
| `Scripts/scheduled/installer.py` | selve rutinen: kandidat, validering, forskjell, bytte, omstart og rapport |
| `Tests/scheduled/test_korrespondanse_vakt.py` | testene T8 og T9 med prøvedata. Markørene sammenlignes med eksemplene i kontrakten. |
| `Tests/scheduled/test_installer.py` | installasjonen fra ende til ende mot en liten agent, planlegger, klient og kontrollbro i en midlertidig mappe |
| `Tests/scheduled/fixtures/` | markøreksemplene, tekstene som skal nektes, og tillegget i `config.json` |
| `Contracts/scheduled-task-stamp-v1.schema.json` og `.example.json`, `Contracts/README.md` | stempelet |
| `Docs/ScheduledEvents.md`, `Docs/OperatorRunbook.md` | de to faste programmene, og rutinen for å legge inn og ta ut. Runbooken på `main` slutter med to linjer verktøymarkering som ikke hører hjemme der; de tas bort i samme endring. |

Commit og push går som jobb i `.agent-spool` (`git add`, `git commit`, `git push origin claude/planlagte-jobber-20261002`); S0 viste at køen kan skyve. PR mot `main` opprettes samme dag, som skriptjobb i `_losen-queue` eller for hånd, for `.agent-spool` har ikke `gh`. Merge skjer på Kjetils ord, og kø-tråden ser på PR-en først.

## S2 — installasjonen av korrespondansevakten · **godkjent 05.10 (G2)** · tørrkjøringen er gjort · **`utfoer` venter på Kjetils ja til forskjellen**

Resultatet så langt (05.10): kø-tråden tildelte bane b kl. 14:15Z. Tørrkjøringen stoppet første gang i steg 2 og fant en feil i programmet: klienten leser `--root` som profilens egen mappe. Den er rettet i commit `081d52d`, og steg 2 i tabellen under gjelder nå med `--root <klientens rot>/<profil>`. Etter det gikk tørrkjøringen gjennom alle seks steg, sist kl. 15:02Z på commit `653fb87`. Utskriftene ligger i `evidence/` og i `HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/maal/`. Omslaget har sjekksummene for filene i `653fb87`. Punkt 1 og 2 i rekkefølgen nederst er gjort; punkt 3 er Kjetils.

Slik er S2 planlagt:

`Scripts/install-scheduled-tasks.sh` tar ett argument: `toerr` (standard), `utfoer` eller `fjern`. Alt det validerer med agenten, kjøres med binæren som er installert: `~/Library/Application Support/HAVENAgent/bin/haven-agentd`.

`utfoer` krever miljøvariabelen `HAVEN_FORVENTET_CONFIG_SHA256`: sjekksummen av `config.json` slik tørrkjøringen så den. Tørrkjøringen skriver den ut. Er fila endret siden, stopper `utfoer`. Da er det som legges inn, det samme som ble vist. Omslagsfila setter variabelen.

| Steg | `toerr` | `utfoer` |
|---|---|---|
| 1 | Måler at `/usr/bin/python3` er 3.9 eller nyere, og kjører `korrespondanse_vakt.py selvtest` | samme |
| 2 | Skriver SHA-256 av programmet og av korrespondanseklienten. Viser om klienten tar `--root`, og spør den om verktøylista for én profil. Ingen innboks leses. Tar klienten ikke `--root`, stopper skriptet her. | samme |
| 3 | Lager en kandidat i en midlertidig mappe: `config.json` pluss `contract/config-tillegg-trinn1-2.json`, med `firstFireAt` satt til nå. Alle andre nøkler i fila bevares som de er. | samme |
| 4 | Validerer kandidaten med `validate-config --config <kandidat>` og `schedule-list --config <kandidat>`, både med `haven-agentd` og med `haven-agentd-scheduler`, for det er planleggerbinæren som skal laste fila. Kontrollerer selv at hver hendelse peker på et fast program i kandidaten, for det gjør ikke agenten. Krever `title`, eller en id på høyst 40 tegn, for hver hendelse det legger inn. Kontrollerer at den ekte `State/scheduled-events.json` har samme endringstid før og etter. | samme |
| 5 | Skriver forskjellen mellom dagens `config.json` og kandidaten. Begge leses og skrives ut med samme oppsett før sammenligningen, og tokenet til kontrollbroen er byttet med `<skjult>`, så forskjellen bare viser det som er lagt til. | samme |
| 6 | Stopper her, og skriver sjekksummen `utfoer` skal ha | Krever at `config.json` har sjekksummen fra tørrkjøringen. Kopierer programmet til `bin/`, tar `config.json.pre-korrespondansevakt-<tid>`, og bytter `config.json` på plass med samme rettigheter som før |
| 7 | | Venter til ingen post i `State/scheduled-events.json` står som `running` (høyst 60 sekunder). Starter så planleggeren på nytt: `launchctl kickstart -k gui/<uid>/io.digipomps.haven.agentd.scheduler`. Binæren er den samme, så rutinen for bytte av binær trengs ikke. |
| 8 | | Venter til begge hendelsene har `runCount` over 0 og `lastFinishedAt` satt (høyst 120 sekunder), og skriver: posten for hver hendelse, de to stemplene, vaktens markører med avsender og profil (filnavn skrives ikke ut), kildene fra `GET /challenges`, og titlene på sakene fra kilden `correspondence`. Saker fra andre kilder bare telles. Fantes en hendelse fra før, ventes det ikke på den. |

Ble en kjøring avbrutt av omstarten, kan første utfall for en hendelse være «kjører allerede». Da kommer markørene ved neste kjøring.

`fjern` tar de to programmene og de to hendelsene ut av `config.json`, starter planleggeren på nytt, venter inntil 70 sekunder på en kjøring av vakten som fortsatt går, og fjerner vaktens egne markører, stempler, låsfiler, midlertidige filer og programfila i `bin/`. Markører andre har skrevet, røres ikke. Postene i `State/scheduled-events.json` forsvinner av seg selv, for planleggeren bygger lista fra hendelsene i `config.json` når den starter. `fjern` legger ikke tilbake sikkerhetskopien blindt, for `config.json` kan være endret i mellomtiden.

Skriptet kjøres fra `_losen-queue` gjennom en omslagsfil, fordi `skript`-modus bare kjører filer under `HAVEN-Deploy/_handoff/`:

- `HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/korrespondansevakt.sh` har sjekksummene til `install-scheduled-tasks.sh`, `scheduled/installer.py` og `scheduled/korrespondanse_vakt.py` skrevet inn. Den kontrollerer dem og starter installasjonen fra arbeidstreet. Stemmer ikke en sjekksum, stopper den. For `utfoer` har den også sjekksummen av `config.json` fra tørrkjøringen.
- Jobbfila `inbox-<bane>/<id>.job`, seks linjer (den første er tom og betyr HAVEN-roten):

  ```

  skript
  HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/maal/KORRESPONDANSEVAKT-TOERR-<dato>.md
  10
  HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/korrespondansevakt.sh
  toerr
  ```

Rekkefølgen:

1. Linje i `KOORDINERING.md`: hva som skal installeres, og at planleggeren startes på nytt. Kø-tråden tildeler bane.
2. `toerr`-jobben. Losen viser Kjetil forskjellen i `config.json` og sjekksummen.
3. Kjetil sier ja til det han ser. Det er et eget ja, i tillegg til G2.
4. `utfoer`-jobben. Utdataene går i `TESTRESULT.md` (T8 og T9 live, og avhengigheten «klienten kan startes av planleggeren»).
5. Bilde av den ekte menyen når en ulest melding ligger der (T8).
6. Linje i `KOORDINERING.md` om at det er gjort. Trinn 1 føres på HD-0069.

Programmet installeres fra grenen, med sjekksummen vist, mens PR-en venter. Endres programmet før merge, kjøres installasjonen på nytt fra `main` etterpå. Regelen om å installere fra merge-commiten gjelder agentbinæren (S3).

## S3 til S5 — ny agent · S3 er **godkjent 05.10 (G2)**, bygget og i PR #30 · installasjonen **venter på merge og køvindu** · S4 og S5 **venter**

Resultatet for S3 (05.10): koden ble lagt i samme arbeidstre og på samme gren som S1, ikke i et eget tre etter at S1 var merget. Kjetil ba 05.10 om færre Actions-løp, og én PR gir ett. `Docs/ScheduledEvents.md` fra S1 lå alt på grenen. Første bygg på macOS var grønt: 394 tester i 59 suiter, commit `9af7811` (`TESTRESULT.md` t1, t2, t3 og t10). Det som står under om eget arbeidstre og egen gren, gjelder derfor ikke lenger.

| Bolk | Hva | Kø | Venter på |
|---|---|---|---|
| S3 | Cron og robusthet i planleggeren (AP5–AP7). Tester T1–T3 og T10. | `.agent-spool`: `swift build`, `swift test --no-parallel` i arbeidstreet | G2. Minst 57 GiB ledig på Macen (53 målt 03.10 kl. 10:52Z). |
| S4 | Bestilte jobber, godkjenning, MCP-verktøy, sakene (AP8–AP11). Tester T4–T7. | samme | S3 |
| S5 | Rutene på kontrollbroen og menyen (AP12–AP13). | samme, og `Packaging/menu-app/make_app.sh` som skript | G1-GUI for bildene, S4 |
| MCP i Claude-appen | `haven-agentd` legges i `claude_desktop_config.json` | `_losen-queue`, `skript` | Kjetils ja (se `PLAN.md` om hva det gir Claude) |

**Koden for S3 er skrevet** (03.10, i skyen; se `LES_MEG.md` i kodepakken `planlagte-jobber-kode-20261003.tar.gz` og `PLAN_VEDLEGG.md`). 71 tester er grønne på Linux. Fabel har gransket den to ganger. Den siste retterunden (åtte punkter) er ikke gransket som kode etterpå, men Fabel har kontrollert at det som står skrevet om den, stemmer med koden (`panel/FABEL_PAASTANDER_SISTE_RUNDE.md`). Den legges i et eget arbeidstre og en egen gren fra `origin/main` etter at S1 er merget, for `Docs/ScheduledEvents.md` bygger på utgaven fra S1:

| Fil | Innhold |
|---|---|
| `Sources/HavenAgentRuntime/CronSchedule.swift` | ny. Cron i navngitt tidssone (AP5). |
| `Sources/HavenMacAutomation/BoundedProcessRunner.swift` | ny. Egen prosessgruppe, tidsgrense, loggfil, tak på utdata. |
| `Sources/HavenAgentRuntime/ScheduledEventService.swift` | endret. Hele fila byttes; den offentlige API-en står. |
| `Sources/HavenAgentRuntime/ScheduledJobStateFiles.swift`, `ScheduledWorkerPresence.swift` | nye. Lesere for styring og kvittering; lås og livstegn. |
| `Sources/HavenAgentD/HavenAgentMain.swift` | endret med `patcher/HavenAgentMain.swift.patch` (to steder). |
| `Scripts/install-agent-dev.sh` | endret med `patcher/install-agent-dev.sh.patch`. |
| `Launchd/io.digipomps.haven.agentd.scheduler.plist` | ny. Malen for planleggerens LaunchAgent, etter målingen 02.10. |
| `Tests/HavenAgentRuntimeTests/CronScheduleTests.swift`, `ScheduledEventScheduleTests.swift`, `Fixtures/cron-forventninger.json` | nye tester. `Package.swift` trenger ingen endring: testmålet har alt `resources: [.copy("Fixtures")]`. |
| `Tests/HavenMacAutomationTests/BoundedProcessRunnerTests.swift` | nye tester. Testmålet `HavenMacAutomationTests` finnes i `Package.swift` på `main` (`ea558ba`). |
| `Docs/ScheduledEvents.md` | hele dokumentet etter trinn 3 |

Første jobb i arbeidstreet er `swift build` og `swift test --no-parallel` med Macens kompilator. Det er første gang macOS-grenene i koden kompileres, og det er beviset; kjøringen i skyen er bare en kontroll på Linux.

**Installasjonen av ny agent** skjer fra merge-commiten på `main`, etter merge på Kjetils ord, når køen er tom, med en linje i `KOORDINERING.md` før og etter, og med forrige binær klar:

1. Bygg i `.agent-spool`, i et arbeidstre på merge-commiten: `swift build -c release --product haven-agentd`. Bygget skjer altså ikke inne i `_losen-queue`, der skriptjobber kjører med et mykt tak på 2 GiB per fil (`runner.sh` linje 170–172).
2. En omslagsfil under `HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/` kaller `/bin/zsh Scripts/install-agent-dev.sh` to ganger, først uten `--apply` (tørrkjøring), så med:
   - `--product haven-agentd --source <arbeidstre>/.build/release/haven-agentd --tag planlagte-jobber`
   - `--product haven-agentd-scheduler --source <samme binær> --tag planlagte-jobber`

   `--product all` kan ikke brukes sammen med `--source` (`install-agent-dev.sh` linje 317), og `--build` ville bygget inne i køjobben.
3. Skriptet legger forrige binær tilbake selv hvis den nye ikke kommer opp.

Ikke målt ennå, og måles i tørrkjøringen før noe byttes:

- **Signeringen fra en køjobb.** `install-agent-dev.sh` krever at signeringsidentiteten ligger i påloggingsnøkkelringen, og sier «run from a logged-in Terminal» (linje 304–305). Om den når nøkkelringen fra `_losen-queue`, er ikke prøvd.
- **Installasjon av `haven-agentd-mcp` og av menyappen.** `install-agent-dev.sh` dekker bare agenten og planleggeren. Trinn 4 trenger ny MCP-binær i `bin/`, og trinn 5 trenger ny menyapp i `/Applications/HAVEN Agent.app`. Rutinene skrives i de trinnene og vises før de kjøres.

To ting føres i `KOORDINERING.md` før S3 starter:

- **Hvordan Swift-bygg i HavenAgentD skal begrenses.** Regel 2 viser til `scripts/run_swift_bounded.sh`, som ligger i CellScaffold. HavenAgentD har ikke skriptet.
- **PR #25 (HD-0156)** endrer `HavenAgentMCPService.swift` og `AgentControlBridgeServer.swift`. S4 og S5 endrer de samme filene, og bygger derfor på `main` etter at #25 er merget.

## Slik tas alt ut igjen

- Korrespondansevakten: `fjern`-jobben i S2.
- Ny agent: `install-agent-dev.sh` legger forrige binær tilbake selv hvis den nye ikke kommer opp. Etter en tilbakerulling kjører fristvarselet videre på intervall, og jobbene i `State/ScheduledJobs/` står stille (`contract/trinn3-cron.md`). `haven-agentd setup` skal ikke kjøres med den eldre binæren.
- Den gamle løperen: `agentd-runner.command.utgaatt-20261002` kan få navnet sitt tilbake. Det er ikke meningen.
