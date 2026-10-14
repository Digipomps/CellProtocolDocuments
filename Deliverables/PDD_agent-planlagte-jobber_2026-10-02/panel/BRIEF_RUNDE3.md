# BRIEF til uavhengig gransking, runde 3: planlagte jobber i HavenAgentD

Du er «Fabel», en uavhengig gransker. Du skal ikke være enig for å være hyggelig. Finn det som er galt, mangler eller er påstått uten belegg. Svar på norsk. Du skal bare lese, ikke endre filer og ikke kontakte noe utenfor.

## Hva som har skjedd

Kjetil eier HAVEN. «Losen» er en Claude-tråd i Cowork som arbeider for ham. Kjetil, ordrett 01.10.2026: «Vi må implementere muligheter for cron-liknende funksjonalitet - dette bør være i agenten eller tilgjengelig for agenten.» Han godkjente formålene F1–F10 (G1) 02.10 og valgte «Også Losens skript», «Cron og intervall» og «Én gang ved oppvåkning».

En uavhengig gransker («Fabel», runde 2) gikk gjennom den første planen og krevde åtte endringer. Svaret ligger i `panel/FABEL_SVAR.md`, briefen i `panel/BRIEF.md`.

Etter det fant Losen at Macen alt har tre jobbkøer under launchd, og at flere tråder koordinerer gjennom en fil Losen ikke hadde lest. Losen har skrevet spesifikasjonen og planen på nytt (runde 3). Det er runde 3 du skal granske. Ingenting av runde 3 er lagt fram for Kjetil ennå.

## Det du skal lese

Runde 3 (i denne mappens foreldermappe, `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/pdd-cron/`):

- `FORMAALSSPEC.md` (runde 3; §1b har endringene E1–E5)
- `PLAN.md` (runde 3)
- `panel/FABEL_SVAR.md` og `panel/BRIEF.md` (runde 2)
- `panel/E-prosjektminne-utdrag.txt` (påstander fra tidligere økter, og målinger 02.10)

Agentens kilder, grenen den installerte agenten er bygget fra: `/mnt/user-data/uploads/HavenAgentD/.worktrees/main-20260922/`. Særlig:

- `Sources/HavenAgentRuntime/ScheduledEventService.swift`, `Tests/HavenAgentRuntimeTests/ScheduledEventServiceTests.swift`
- `Sources/HavenMacAutomation/AutomationPolicy.swift`, `LocalTaskRunner.swift`, `SubprocessRunner.swift`
- `Sources/HavenAgentD/HavenAgentMain.swift` (linje 335–381), `AgentChallengeWiring.swift`
- `Sources/HavenAgentRuntime/AgentChallenge.swift`, `ChallengeInboxService.swift`, `AgentConfig.swift`
- `Sources/HavenAgentDMCP/HavenAgentMCPService.swift` (`callTool` rundt linje 199), `HavenAgentDMCPMain.swift`
- `Sources/HavenAgentMenuCore/MenuPresentation.swift`, `Sources/HavenAgentMenu/HavenAgentMenuApp.swift`
- `Docs/ScheduledEvents.md`, `Docs/AgentJobs.md`, `Docs/SecurityModel.md`, `Docs/AgentMenylinje.md`, `Docs/OperatorRunbook.md`
- `Scripts/install-agent-dev.sh`

Køene som finnes, lest fra Macen 02.10 (jobblogger i `/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/`):

- `job-245-les-eksisterende-koer.log`: `.agent-tools/README.md`, hodet av `agent_job_runner.py` (tillatt-lista), `.agent-spool/`, `_losen-queue/`, `KOE-GAMMEL-RUNNER-20261001.md`, `HAVEN-Deploy/README.md`, `launchctl list`
- `job-246-les-koer-2.log`: `_losen-queue/LES_MEG.md`, første del av `KOORDINERING.md`, utdrag av `runner.sh`, resten av `agent_job_runner.py`
- `job-247-les-koordinering.log`: køens tavle, resten av `KOORDINERING.md` (blant annet installasjonsvinduet for AgentD)
- `job-2425-lesesjekker-planlegger.log`: planleggeren under launchd, konfigurasjonen

Det som ikke ligger her, og som du derfor ikke kan belegge: `CorrespondenceWaiting.swift` (markørkontrakten), `AgentControlBridgeServer.swift`, korrespondanseklientens kilde, planleggerens plist, og tilstanden i HavenAgentD-repoet på GitHub (grener og PR #25). Macen er frakoblet akkurat nå.

## Spørsmålene

- **P1. De åtte punktene.** Gå gjennom «Må endres før G2» i `panel/FABEL_SVAR.md`. For hvert punkt: er det løst, flyttet, eller borte uten å være løst i runde 3? Tabellen «Det runde 2 fant, og hvor det ble av» i planen er Losens egen påstand. Prøv den.
- **P2. Trinn 1 og 2 på planleggeren som kjører i dag.** Planen vil la dagens planlegger (kildene over, uendret) starte et Python-program hvert 30. minutt og et annet én gang i døgnet. Les `ScheduledEventService.swift` og `SubprocessRunner.swift` på nytt med det for øye. Hva kan gå galt, konkret? Hva må programmene garantere for at planleggeren ikke henger? Hva skjer med hendelsene ved omstart av tjenesten, ved søvn, og når konfigurasjonen endres mens arbeideren kjører? Er «uten ny agent» en holdbar påstand?
- **P3. Køjobber (`spoolJob`).** Planen sier at planleggeren kan legge en jobb i `.agent-spool`, og at køens tillatt-liste avgjør hva som kjøres. Les tillatt-lista og avvisningsreglene i `agent_job_runner.py`. Hva kan en jobb som slipper gjennom lista, likevel gjøre? Er sikkerhetsavsnittet i planen ærlig og dekkende? Er F5 slik den er formulert i runde 3, sann?
- **P4. Korrespondansesjekken (F8).** Kjetil valgte 10.09 at agenten poller selv, og at Losen markerer hva som krever svar. Planens program skriver en markør for all ukvittert post. Er det samme ting? Hva skjer når Losen kvitterer en melding som likevel krever Kjetil? Hva skjer når programmet feiler stille? Er «leser ikke meldingsinnhold» nok til å holde regelen om at markøren aldri bærer meldingsteksten? Pek på det som må avgjøres av Kjetil, ikke av Losen.
- **P5. Formål og tester.** Hvilke av F1–F10 har ingen test som faktisk måler formålet? Hvilke tester måler noe annet enn de sier? Hva mangler i T0–T10?
- **P6. Koordinering.** Les installasjonsvinduet for AgentD og reglene 1–6 i `KOORDINERING.md`. Hva i planen kan kollidere med HD-0156 og PR #25, med regelen om å installere fra `main`, og med banene i `_losen-queue`? Er det noe planen lar Losen gjøre som reglene sier at en annen skal gjøre eller avgjøre?
- **P7. Rekkefølgen.** Planen leverer F8 og F9 først, deretter cron. Kjetil ba om cron. Er rekkefølgen forsvarlig mot det han faktisk ba om, eller er det en omvei? Finnes en kortere vei til det samme?
- **P8. Språk og forståelighet.** Kjetil har sagt at planer er «veldig vanskelig å forstå hva det innebærer og hva jeg skal gjøre». Les `PLAN.md` som ham. Hva er uklart? Hva forutsetter kunnskap han ikke har fått? Hva kan strykes?

## Svarformat

For hvert spørsmål: konklusjon først (én setning), deretter belegget. Hver påstand om kildene merkes `[belagt: fil:linje]`. Det du ikke fant belegg for, merkes `[ikke belagt]`. Avslutt med tre lister: «Må endres før dette legges fram for Kjetil», «Bør endres», «Kan vente». Hold svaret under 800 ord per spørsmål.
