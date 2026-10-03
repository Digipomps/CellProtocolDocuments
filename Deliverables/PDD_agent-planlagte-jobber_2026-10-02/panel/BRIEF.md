# BRIEF til uavhengig validering: planlagte jobber i HavenAgentD

Du er «Fabel», en uavhengig gransker. Du skal ikke være enig for å være hyggelig. Finn det som er galt, mangler eller er påstått uten belegg. Svar på norsk.

## Formål (godkjent av Kjetil, G1 02.10.2026)

Kjetil, ordrett: «Vi må implementere muligheter for cron-liknende funksjonalitet - dette bør være i agenten eller tilgjengelig for agenten.»

Bakgrunn: Losen (Claude i Cowork) kjører bygg, tester, git og ssh på Kjetils Mac gjennom et skript i et Terminal-vindu («løperen») som tar skript fra en kømappe. Løperen stoppet av seg selv etter ti timer, og planlagte sjekker i skyen nådde ikke Macen da broen var nede. Kjetil vil at arbeid til faste tider, og Losens kø, skal gå uten at noen starter noe.

Kjetils valg ved G1:

1. Rettigheter: «Også Losens skript». Losen oppretter og stopper jobber gjennom MCP. Jobbene kan kjøre godkjente handlinger og skript Losen legger i køen. Det gjør løperen varig, synlig i menylinjen og med en stoppknapp.
2. Tidsuttrykk: cron med fem felt i tidssonen Europe/Oslo, pluss intervall og «én gang» som i dag.
3. Passert kjøring (Macen sov): kjør én gang ved oppvåkning, registrer og vis passeringen.

Formålene F1–F10 står i `FORMAALSSPEC.md` i denne mappen.

## Kildene du skal lese

Alt ligger under `/mnt/user-data/uploads/HavenAgentD/.worktrees/main-20260922/` (grenen den installerte agenten er bygget fra):

- `Sources/HavenAgentRuntime/ScheduledEventService.swift` (hele planleggeren, 320 linjer)
- `Tests/HavenAgentRuntimeTests/ScheduledEventServiceTests.swift`
- `Sources/HavenMacAutomation/AutomationPolicy.swift`, `LocalTaskRunner.swift`, `SubprocessRunner.swift`
- `Sources/HavenAgentD/HavenAgentMain.swift` (linje 335–381: `schedule-worker`, `schedule-list`, `schedule-stop`)
- `Sources/HavenAgentDMCP/HavenAgentMCPService.swift` (verktøyene; se `callTool` rundt linje 199)
- `Sources/HavenAgentRuntime/AgentChallenge.swift`, `ChallengeInboxService.swift`, `Sources/HavenAgentD/AgentChallengeWiring.swift`
- `Sources/HavenAgentMenuCore/MenuPresentation.swift`, `Sources/HavenAgentMenu/HavenAgentMenuApp.swift`
- `Docs/ScheduledEvents.md`, `Docs/AgentJobs.md`, `Docs/SecurityModel.md`, `Docs/AgentMenylinje.md`, `Docs/OperatorRunbook.md`
- `Scripts/install-agent-dev.sh`, `Launchd/io.digipomps.haven.agentd.plist`

Målt på Macen 02.10.2026: `io.digipomps.haven.agentd.scheduler` kjører under launchd (`haven-agentd-scheduler`, pid 18244, aldri avsluttet). `State/scheduled-events.json` finnes (896 byte, sist skrevet 26.09). Dagens løper er `Claude outputs/agentd-runner.command`: en zsh-løkke som tar `queue/*.sh` i navnerekkefølge, logger til `job-<navn>.log`, merker `JOB-DONE-<navn>-rc<kode>`, stopper på `queue/STOP`.

## Designvalgene som skal granskes

- **D1 Cron.** `ScheduledEventDefinition` får `cron: String?` og `timeZone: String?`. En ren type `CronSchedule` (minutt, time, dag i måned, måned, ukedag; `*`, lister, områder, steg; 0 og 7 er søndag; når både dag og ukedag er begrenset, holder det at én treffer). Neste tidspunkt beregnes med `Calendar` i jobbens tidssone ved å gå dag for dag og bygge lokale tider. Et lokalt klokkeslett som ikke finnes (sommertid starter) kjøres på tidspunktet `Calendar.date(from:)` gir. Et klokkeslett som finnes to ganger (sommertid slutter) kjøres én gang, første forekomst.
- **D2 Passert.** Som i dag kjøres en forfalt hendelse én gang når arbeideren ser den. Nytt: antall passerte tidspunkt og forsinkelsen registreres (`missedCount`, `lastMissedAt`, `lastDelaySeconds`). Ingen etterkjøring av hvert passerte tidspunkt.
- **D3 Dynamiske jobber.** Poster i `State/scheduled-events.json` får `origin` (`config` eller `dynamic`). `start(definitions:)` beholder dynamiske poster og erstatter bare konfigurasjonens. CLI og MCP er egne prosesser som endrer filen (legg til, pause, fortsett, stopp, fjern). Arbeideren leser filen på nytt hvert sekund, som i dag. Arbeideren skriver tilbake med les–endre–skriv for den ene posten den har kjørt.
- **D4 MCP.** Nye verktøy `agent.schedule.list`, `.create`, `.pause`, `.resume`, `.stop`, `.remove`. `create` avviser en handling som ikke finnes i `AutomationPolicy`. Ved kjøring valideres handlingen på nytt (som i dag). Ingen nye handlingstyper.
- **D5 Losens kø som godkjent lokal oppgave.** Kjetil legger én `localTask` i policyen, `losen-queue-ensure`, med fast program og faste argumenter. En planlagt jobb kjører den hvert minutt. Skriptet starter køarbeideren løsrevet hvis ingen lever (lås og hjerteslag), og returnerer straks. Køarbeideren er dagens løper uten tidsgrense. Utdata fra arbeideren går til fil, slik at rørene til `FoundationProcessRunner` lukkes. Stopp: `queue/STOP` og stopp av den planlagte jobben.
- **D6 Synlighet.** Ny kilde i challenge-innboksen for planlagte jobber: en feilet eller passert kjøring blir en sak. Menylinjen får en del «Planlagte jobber» med «Stopp køen». Kontrollbroen får ruter for status og stopp.
- **D7 Utgangspunkt.** Arbeidet gjøres i et nytt worktree fra grenen den installerte agenten er bygget fra (`claude/testflyt-verktoycelle-20260923`), ikke fra `origin/main`, fordi en ny binær ellers mister testflyten og menylinjen.

## Spørsmålene

- **P1.** Er D5 forenlig med `Docs/SecurityModel.md` og sikkerhetsmodellen i `Docs/AgentJobs.md`? Hvem kan skrive til kømappen, og hva er det svakeste punktet? Finnes en tryggere form som fortsatt lar Losens skript kjøre uten at Kjetil starter noe? Kjetil har valgt dette med åpne øyne; spørsmålet er om utformingen er den minst farlige som oppfyller valget.
- **P2.** D3: hvilke kappløp oppstår når flere prosesser skriver samme tilstandsfil? Les `runDueEvents`, `runEvent` og `start`. Er det en enklere og mer robust form?
- **P3.** D1: er sommertid-reglene rimelige, og stemmer antakelsene om `Calendar.date(from:)`? Hva går galt?
- **P4.** `runDueEvents` venter på hver hendelse i rekkefølge, og `FoundationProcessRunner` leser rørene til slutt. Hva betyr det for D5 og for andre hendelser når en lokal oppgave varer lenge eller etterlater barneprosesser?
- **P5.** Køarbeideren blir et barn av en launchd-jobb. Hva må måles på Macen før vi kan si at bygg, `git push` over ssh, `gh` og nøkkelringen virker derfra? Hva skjer med arbeideren når launchd-jobben startes på nytt?
- **P6.** `Docs/ScheduledEvents.md` sier at vilkårlige kommandoer ikke er en del av kontrakten. Hvordan dokumenteres D5 ærlig uten å late som om grensen står?
- **P7.** Hva mangler i planen for at F1–F10 faktisk er oppfylt og testet? Pek på formål uten test og tester som ikke måler formålet.

## Svarformat

For hvert spørsmål: konklusjon først (én setning), deretter belegget. Hver påstand om koden merkes `[belagt: fil:linje]`. Det du ikke fant belegg for, merkes `[ikke belagt]`. Avslutt med en kort liste: «Må endres før G2», «Bør endres», «Kan vente». Hold svaret under 900 ord per spørsmål. Du skal bare lese, ikke endre filer.
