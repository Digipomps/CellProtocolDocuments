# Brief til Fabel: G2-artefaktene for planlagte jobber

Dato: 02.10.2026, kveld. Du er en uavhengig gransker. Du skal ikke bygge noe og ikke endre noe utenfor rapportfila di.

## Hva som skal granskes

PDD-mappen ligger her: `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/pdd-cron/`

| Fil | Hva det er |
|---|---|
| `FORMAALSSPEC.md` | formålene F1–F10, påstandstabellen (§0), avhengighetene (§2), testene (§5). G1 er godkjent av Kjetil, og endringene E1–E6 er godkjent. |
| `PLAN.md` | planen Kjetil skal ta stilling til (G2). Den skal kunne leses av Kjetil uten forkunnskap. |
| `PLAN_VEDLEGG.md` | arbeidspakkene AP0–AP14 og avsnittet «Endret da kontrakten ble skrevet». |
| `contract/` | kontraktene: `README.md`, `trinn1-2-programmer.md`, `trinn3-cron.md`, `trinn4-jobber-og-godkjenning.md`, `trinn5-kontrollbro.md`, skjemaene, `mcp-verktoy.json`, `saker-job.example.json`, `config-tillegg-trinn1-2.json`, `cron_reference.py`, `kontroller_kontrakt.py`, `KONTROLL.txt`, `fixtures/`. |
| `dataflow.md` | dataflyten med navngitte kanter. |
| `handoff/README.md` | rekkefølgen og jobbene som går til køene på Macen. |
| `images/README.md`, `images/meny-v3.html`, `images/meny-v2.html` | skissene til menylinjen (PNG-ene ligger ved siden av). |

Eldre granskinger ligger i `panel/` (`FABEL_SVAR_RUNDE3.md`, `FABEL_ETTERKONTROLL_RUNDE3.md`). Filer som slutter på `.runde3-foer-g2artefakter`, er utgavene før kveldens endringer.

## Kildene du kan lese

- HavenAgentD slik det er på `origin/main` (`ea558ba`), et utvalg filer: `/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/` (`Sources/`, `Docs/`, `Contracts/`, `Scripts/`, `Launchd/`, `Package.swift`).
- Køene på Macen: `/mnt/user-data/uploads/HAVEN/.agent-tools/agent_job_runner.py`, `/mnt/user-data/uploads/HAVEN/_losen-queue/LES_MEG.md`, `/mnt/user-data/uploads/HAVEN/_losen-queue/runner.sh`.
- Utdrag av filer som ikke er kopiert hit i sin helhet, og målinger fra Macen i dag: `panel/kilder-utdrag/` i PDD-mappen. Utdragene er utskrifter (`cat -n`, `grep -n`) tatt fra Macen tidligere i dag. Der et utdrag ikke dekker en påstand, sier du det.

Macen er ikke tilkoblet nå. Du kan ikke lese andre filer enn disse.

## Det jeg ber om

1. **Kontroller påstandene mot kildene.** Gå gjennom kontraktene, `dataflow.md`, `handoff/README.md`, og de delene av `PLAN.md`, `PLAN_VEDLEGG.md` og `FORMAALSSPEC.md` som viser til kode. For hver påstand om hvordan koden som finnes oppfører seg: stemmer den, stemmer den ikke, eller kan den ikke kontrolleres med kildene du har? Oppgi fil og linje. Ta særlig for deg:
   - hva planleggeren som kjører i dag gjør (`ScheduledEventService.swift`, `SubprocessRunner.swift`, `LocalTaskRunner.swift`, `AutomationPolicy.swift`, `HavenAgentMain.swift`), og om programmet i trinn 1–2 kan henge den, starte dobbelt eller gi feil utfall;
   - hva en eldre agent tåler av nye felt og filer (påstandene i `contract/trinn3-cron.md` om `config.json` og `State/scheduled-events.json`);
   - hvordan markører blir til saker, og hva som gjør en kilde ulesbar eller hele innboksen ugyldig (`CorrespondenceWaiting.swift`, `AgentChallenge.swift`, `ChallengeInboxService`, kontrollbroens rute `challenges`);
   - hva «Åpne», «Ignorer i dag», «Godkjenn» og «Avvis» gjør i menyen, i adminvinduet og fra et varsel;
   - hva MCP-serveren lar en klient gjøre i dag (`HavenAgentMCPService.swift`), og om det som står om dette i `PLAN.md` og `contract/trinn4-jobber-og-godkjenning.md` er riktig og fullstendig;
   - køenes regler (`agent_job_runner.py`, `LES_MEG.md`) mot det `handoff/README.md` sier.
2. **Let etter feil i selve kontrakten.** Tilstander som ikke er dekket, kappløp mellom prosesser, måter en jobb kan kjøre uten godkjenning eller kjøre to ganger, måter en sak kan bli stående eller aldri komme, falske alarmer, og steder der to dokumenter sier ulike ting. Regn selv etter på minst fem av tilfellene i `contract/fixtures/cron-forventninger.json`, med en annen framgangsmåte enn `cron_reference.py` bruker, og si om reglene i `contract/trinn3-cron.md` er entydige.
3. **Les `PLAN.md` slik Kjetil vil lese den.** Han er ikke utvikler på detaljnivå i denne koden. Sier planen hva hvert punkt innebærer og hva han selv må gjøre? Er det noe han i praksis tar stilling til ved å godkjenne, som ikke står tydelig? Er noe sagt sikrere enn kildene gir grunnlag for?
4. **Si hva som mangler** for at G2-artefaktene skal være nok til å bygge trinn 1 og 2 uten nye antakelser.

## Slik svarer du

Skriv rapporten til `panel/FABEL_SVAR_G2.md` i PDD-mappen, på norsk. Del den slik:

- **Må rettes før G2** (nummerert; hvert punkt med hva som er feil, hvor, kilden, og hva som bør stå)
- **Bør rettes** (samme form)
- **Påstander kontrollert** (tabell: påstand, hvor den står, utfall `stemmer` / `stemmer ikke` / `kan ikke kontrolleres`, kilde med linje)
- **Egne utregninger av cron-tilfellene**
- **Mangler**

Ikke gjenta det som er riktig i lange vendinger. Skriv det du faktisk fant, også når det er «fant ingen feil her». Ikke gjett: det du ikke kan kontrollere, skal stå som det.

## Grenser

- Bare lesing, utenom rapportfila. Ikke endre noen annen fil.
- Ikke bruk verktøy som når Macen, korrespondansen, nettlesere eller andre tjenester. Ikke send meldinger til noen.
- Ikke skriv ut eller gjengi enhets-ID-er, meldingsemner eller andre private detaljer fra `panel/kilder-utdrag/` i rapporten. Vis til fil og linje i stedet.
