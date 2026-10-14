# FORMÅLSSPEC: planlagte jobber i agenten (cron-liknende)

PDD `agent-planlagte-jobber`, 01.10.2026. Utfører: Losen (Claude-tråden i prosjektet «HavenAgentD»). Repo: HavenAgentD. Status: G1 godkjent 02.10.2026. De seks endringene i runde 3 (§1b) ble godkjent samme dag. G2 og de tre presiseringene i §1c ble godkjent 05.10.2026. Bildene (G1-GUI) er ikke godkjent.

To tråder heter Losen. I dette dokumentet er «Losen» tråden som skriver det, og «kø-tråden» er Claude-tråden som administrerer deploykøen (`HAVEN-Deploy`, `_losen-queue`).

## §0 Intensjon, ordrett

Kjetil, 01.10.2026: «Vi må implementere muligheter for cron-liknende funksjonalitet - dette bør være i agenten eller tilgjengelig for agenten.»

Bakgrunnen i samme økt: jobbløperen (`Claude outputs/agentd-runner.command`) stoppet av seg selv etter ti timer kl. 05:07. Losens sjekker kl. 23:00 og 23:45 30.09 kjørte i skyen og fant Macen frakoblet, så ingenting ble gjort før Kjetil spurte kl. 08. Løperen måtte startes igjen fra Finder.

### Kjetils valg ved G1, 02.10.2026

| Spørsmål | Valg | Beskrivelsen han valgte |
|---|---|---|
| Hva skal en planlagt jobb kunne kjøre, og hvem oppretter den? | «Også Losens skript (anbefalt)» | Losen oppretter og stopper jobber gjennom MCP. Jobbene kan kjøre godkjente handlinger og skript Losen legger i køen. Det gjør løperen varig: den lar allerede Losen kjøre hva som helst som deg, men nå hele tiden, synlig i menylinjen og med en stoppknapp. |
| Hvilke tidsuttrykk trengs? | «Cron og intervall (anbefalt)» | Fem felt som i cron, i tidssonen Europe/Oslo, pluss intervall og «én gang» som i dag. |
| Hva skal skje med en kjøring som ble passert mens Macen sov? | «Én gang ved oppvåkning (anbefalt)» | Er flere tidspunkt passert, kjøres jobben bare én gang. Passeringen registreres og vises. |
| G1 | «Ja, G1 godkjent» | |

### Kjetils svar ved G2, 05.10.2026

Ordrett: «G2 er godkjent og det er også forslagene dine til F5 F6 F4. Bygg en ny universal installerer om det trengs - men DET MÅ VIRKE! - før jeg sender dem en ny installerer»

Slik er det lest. G2 og de tre presiseringene i §1c er godkjent. Bildene (G1-GUI) er ikke nevnt, og står som før. «Dem» er lest som Vegar og Victoria. Vegar fikk pakken `HAVENAgentD-0.3.2-universal2.pkg` som ble bygget 08.09. Det Victoria fikk 30.08, kan ikke være den pakken, som ble bygget ni dager senere. E-postutkastet fra den dagen sier «en pilotpakke, ikke en signert release», og fila hun fikk, er ikke funnet. (Første utgave av denne setningen sa at begge har 0.3.2-pakken. Det var ikke belagt for Victoria; rettet 05.10 kveld.) Setningen om installereren gjelder andre maskiner enn Kjetils, og det holder §2 utenfor denne PDD-en. Den er derfor ikke tatt inn i formålene. Det som er målt om den, står i tabellen under, og spørsmålet om hva mottakerne skal ha, står i §6.

| Forutsetning i setningen | Status | Kilde |
|---|---|---|
| Mottakerne har en installerer som virker i dag | hentet for pakkene (målt 05.10 kl. 14:16Z). Utilgjengelig for det Victoria fikk. | To pakker heter `HAVENAgentD-0.3.2-universal2.pkg`: én bygget 10.08 (`CellScaffold/Artifacts/AssistantCorrespondenceAgent/0.3.2/`) og én bygget 08.09 (den Vegar fikk). For begge er signaturen gyldig, billetten fra Apple er stiftet på, og Gatekeeper svarer «accepted, Notarized Developer ID». Korrespondanseklienten i begge har både `x86_64` og `arm64`, gyldig signatur, og starter på arm64. Råutdata: `evidence/LES-INSTALLERT-20261005-utdrag.md`. Det finnes ingen spor av at noen har fått pakken fra 10.08. Victoria fikk en usignert pilotpakke 30.08; klienten på Kjetils Mac (bygget 27.08, fra en pilotpakke) er av samme slag. |
| Intel-delen av binærene virker | utilgjengelig | Macen har ikke Rosetta, så `x86_64`-delen kunne ikke startes her. Den er ikke prøvd på en Intel-Mac i denne økten. |
| Fornyelsen av tilgangen deres krever en ny installerer | motsagt av kilden (lest 05.10). Ikke prøvd med binærene deres. | Klienten i begge pakkene (kilde `401f1b21` i Binding og `e88a697` i HavenAgentD) bruker nøkkelen den har fra før, og tar enhets-ID-en fra invitasjonsfila. Tjeneren (2026.9.5) krever samme enhets-ID som ved innmeldingen, og sammenligner den ikke med invitasjonen. Fornyelsen går derfor med klienten de har, når invitasjonsfila bærer enhets-ID-en deres. Klienten Kjetil fornyet med 30.09, er en tredje utgave (bygget 27.08, bare arm64, ad hoc-signert), så fornyelsen er aldri kjørt med binærene fra pakkene. Mottakeren setter enhets-ID-en inn selv, med skriptet `HAVEN-Deploy/_handoff/HD-0006/forny-haven-tilgang.sh`, som finner klienten både der pakken og der pilotpakken legger den. Skriptet og prøven av det hører til PDD-en `PDD_korrespondanse-fornyelse_2026-09-30`. |
| En installerer bygget fra `main` i dag ville virke for dem | motsagt (kilde lest 05.10) | Oppskriften på `main` (`Packaging/build_pkg.sh`) tar med korrespondanseklienten fra `main`. Det er den nye klienten (skjema 2, over broen), og den når ikke staging før bro-ruten finnes der (HD-0166). |
| En ny installerer kan gi mottakerne planlagte jobber | hentet (kilde lest 05.10): ikke uten tre deler som mangler | Pakken starter ikke agenten, og har verken planleggerens LaunchAgent eller menyappen (`Packaging/README.md`). Korrespondansevakten er et Python-program og trenger `/usr/bin/python3`, som på Macen her kommer fra Xcode. At den mangler på en Mac uten utviklerverktøy, er husket og ikke målt. |

### Påstandene intensjonen bygger på

Status: `hentet` betyr lest fra en fil eller målt i denne økten, med kilde. `husket` betyr ikke sjekket nå. Ingenting som er `husket`, bærer planen.

| Påstand | Status | Kilde |
|---|---|---|
| Agenten har en planlegger | hentet | `Docs/ScheduledEvents.md` og `Sources/HavenAgentRuntime/ScheduledEventService.swift`: `AgentConfig.scheduledEvents` med `firstFireAt`, `repeatMode` (én gang, antall, til stoppet) og `intervalSeconds`. Tilstanden lagres i `State/scheduled-events.json`. Filene er like på `origin/main` og på grenen kildene ble lest fra (målt 02.10). |
| Planleggeren kjører under launchd nå | hentet (målt 02.10) | `io.digipomps.haven.agentd.scheduler`: `haven-agentd-scheduler schedule-worker`, `KeepAlive` og `RunAtLoad`, pid 18244, i gang siden 26.09. Miljøet er bare `PATH=/usr/bin:/bin:/usr/sbin:/sbin` og `SSH_AUTH_SOCK`. Plisten ligger i `~/Library/LaunchAgents/`, ikke i repoet. |
| Agenten som kjører, er bygget fra `main` | hentet (målt 02.10) | Binærene i `~/Library/Application Support/HAVENAgent/bin/` er fra 26.09 kl. 20:45. Sikkerhetskopien før dem heter `pre-workbench-ca1eda9`, og `ca1eda9` (PR #24) er på `origin/main`. Runde 2 sa at agenten var bygget fra testflyt-grenen. Det var husket, og det var utdatert: innholdet i den grenen kom på `main` som `claude/testflyt-verktoycelle-v2`. |
| En planlagt hendelse kan bare kjøre navngitte, godkjente handlinger | hentet | `ScheduledEvents.md` linje 54–57: en `localTask` har fast program og faste argumenter i policyen, og hendelsen peker bare på ID-en. |
| Planleggeren kjenner ikke cron-uttrykk eller tidssone | hentet | `ScheduledEventService.swift` linje 271–274: neste tidspunkt er «nå pluss intervall». |
| En hendelse som ble passert mens Macen sov, kjøres én gang når arbeideren ser den. Passeringen telles ikke. | hentet | `ScheduledEventService.swift` linje 216–226 og 271–274 |
| Én hendelse som henger, stopper alle de andre. Det finnes ingen tidsgrense. | hentet | Hendelsene kjøres én om gangen (linje 224–226). `SubprocessRunner.swift` linje 61–71 leser utdata først når programmet er ferdig. |
| Losen kan ikke opprette, se eller stoppe planlagte jobber | hentet (målt 02.10) | Kilden på `origin/main` har 23 MCP-verktøy. Ingen gjelder planlegging. Den installerte MCP-binæren har heller ingen. |
| Agentens MCP-server er ikke lagt inn i Claude-appen | hentet (målt 02.10) | `claude_desktop_config.json` har fire servere: to for korrespondanse og to for filutveksling. Codex har `haven-agentd` i sin konfigurasjon. |
| **Macen har alt tre jobbkøer under launchd** | hentet (målt 02.10) | (1) `no.digipomps.haven.agent-runner`: `.agent-tools/agent_job_runner.py`, kø i `.agent-spool/`, alltid på (pid 4834). Jobbene er JSON med kommandoer som lister, og bare det som står på en tillatt-liste kjøres: bygg, test, en del `git`-kommandoer, `gh pr`, `gh repo`, `gh run`, `gh api` og fire skript (`scripts/run_swift_bounded.sh`, som løses mot jobbens egen mappe, og tre faste under HAVEN-roten). (2) `org.digipomps.losen-queue`: `_losen-queue/runner.sh` hvert 60. sekund, fire baner, kjører Codex-jobber eller ett navngitt skript under `HAVEN-Deploy/_handoff/`. (3) `org.digipomps.haven-dispatch`: `HAVEN-Deploy/tools/dispatch.py --once` hvert 60. sekund. Alle stier er under `~/Build/Digipomps/HAVEN/`. |
| Tillatt-lista i `.agent-spool` er ikke en vegg | hentet | `agent_job_runner.py`: `scripts/run_swift_bounded.sh` løses mot jobbens egen mappe, `swift test` kjører testkode, og `gh api` kan gjøre det `gh pr merge` er nektet. |
| Køen `.agent-spool` kjører under launchd uten Homebrew på `PATH` | hentet (målt 02.10) | Plisten har ingen miljøvariabler. Om `gh` kan nås derfra, er ikke målt. |
| Denne tråden brukte en egen løper fordi kømappene ikke var koblet til økten | hentet | Tilkoblede mapper var HavenAgentD, Binding, CellProtocolDocuments, sprout og Skrivebord. HAVEN-roten ble koblet til 02.10 kl. 18:44Z, etter Kjetils ja. |
| Losens egen løper kjører hva som helst fra en mappe Losen selv skriver i | hentet | `Claude outputs/agentd-runner.command`. Losen endret selv tidsgrensen 02.10. |
| Menylinjen har en kilde for jobber, uten noe som fyller den | hentet (målt 02.10) | `GET /challenges` gir kilden `job` som `not-configured`. `AgentChallenge.swift` linje 21–23: «deklarert uten produsent i v1». |
| Menylinjen leser kilden for post, og ingen fyller den | hentet (målt 02.10) | `GET /challenges` gir `correspondence` som `read` med null saker. `CorrespondenceWaiting.swift`: markører etter `haven.correspondence-waiting.v1` i `Inbox/CorrespondenceWaiting/` (felt `schema`, `id`, `profile`, `from`, `summary`, `markedAt`, `markedBy`). Tittelen blir alltid «Post fra … venter på svar». Mappen er tom. |
| Kjetil har valgt at agenten selv poller korrespondansen, og at Losen markerer hva som krever svar | husket | Prosjektminnet `menylinje_og_varsler` (10.09). Pollingen er ikke bygget. Valget bekreftes på nytt i G2. |
| Fristen for Kjetils tilgangsbevis kan leses lokalt | hentet (målt 02.10) | `profile.json` i hver profilmappe har `accessCredential.payload.expiresAt`. Begge går ut 30.10.2026 kl. 20:00 norsk tid. |
| Deploykøen har en åpen oppgave for samme behov som F8 | hentet (02.10) | HD-0069: «Ny correspondence-post gir ingen macOS-varsel — Kjetil må be Losen sjekke innboksen». |
| Korrespondanseklienten som er installert, er ikke den som ligger på `main` | hentet (02.10) | Binæren i `~/Library/Application Support/HAVEN/AssistantCorrespondence/bin/` er fra 16.08 og er pilotklienten: verktøyet for innboksen tar `afterSequence` og `limit`. `Sources/HavenCorrespondenceMCP` på `origin/main` (`ea558ba`) er en ny klient der hvert verktøy krever `relationshipID`. En senere utgave av pilotklientens kilde (11.09) finnes i arbeidstreet `.worktrees/varsler-20260911`; der heter verktøyet `correspondence.list_inbox`. Hva binæren fra 16.08 kaller det, måles i trinn 1. |
| Kilden `job` var satt av til AgentJobs-køen | hentet (02.10) | `AgentChallenge.swift` linje 21–23 og `Contracts/agent-challenge-v1.schema.json`. AgentJobs er siden landet på `main` (`Docs/AgentJobs.md`), uten leverandør for kilden. |
| En MCP-klient kan alt i dag godkjenne fjernintenter og få et fast program kjørt | hentet (02.10) | `HavenAgentMCPService.swift`: `agent.review.approve`; `agent.jobs.register` med `onComplete.actions` og `agent.jobs.complete`. `JobCompletionService.dispatchActions` kjører handlingene når jobben meldes ferdig. Utførerne for Codex og Claude Code er avslått i konfigurasjonen som er installert (nøklene mangler, og standarden er av). |
| Agenten har én tidsplan til, som ikke er en jobbplanlegger | hentet (02.10) | `PersonalButlerScheduleService.swift` og `Docs/PersonalButlerSchedule.md`: daglige og ukentlige tidspunkt for Personal Butler, med stille timer. Den åpner HAVEN-appen og kjører ikke jobber. Den røres ikke her. |
| En annen tråd arbeider i HavenAgentD, og agentinstallasjon har en regel | hentet (02.10) | `_losen-queue/KOORDINERING.md`: HD-0156 (Codex, PR #25). Agenten installeres fra merge-commiten på `main`, bare når køen er tom, med en linje i koordineringsfila før og etter, og med forrige binær klar. |
| Lokale Swift-bygg er ikke lov akkurat nå | hentet (målt 02.10 kl. 18:56Z) | Macen har 54 GiB ledig. Regel 1 i `KOORDINERING.md` krever minst 40 GiB og 5 % ledig etter 10 GiB reserve, omtrent 57 GiB. |

## §1 Formål med mål

At planleggeren skal finnes, er ett formål. Hva den skal løse, er egne formål (F7–F10). Løsningen velges etter dem.

Tabellen viser formålene slik de er etter at §1b ble godkjent 02.10 og §1c ble godkjent 05.10. Det som er endret siden G1, er merket.

| Id | Formål | Mål (observerbart) | Verifikator |
|---|---|---|---|
| F1 | Tider kan uttrykkes som i cron | Et uttrykk med fem felt (minutt, time, dag, måned, ukedag) i en navngitt tidssone gir riktige neste tidspunkt, også over sommertid-skiftene 25.10.2026 og 28.03.2027. Intervall og «én gang» virker som før. | T1 |
| F2 | Jobbene kjører uten at noen starter dem | Planleggeren kjører under launchd og går igjen når Kjetil har logget inn etter en omstart. Fra trinn 3 har hver jobb en tidsgrense, så en jobb som henger eller skriver mye, ikke stopper de andre. *(Presisert.)* | T2, T6 |
| F3 | Det er bestemt hva som skjer når Macen sov | En jobb som ble passert mens Macen sov eller var av, kjøres én gang ved oppvåkning. Antall passerte tidspunkt registreres og vises. Samme tidspunkt kjøres aldri to ganger. | T3 |
| F4 | Agenten kan bruke planleggeren | Losen kan be om og liste planlagte jobber gjennom MCP-verktøy i agenten, uten å redigere konfigurasjonen. Pause og stopp gjennom MCP gjelder jobber som er bedt om. De faste programmene i `config.json` styres bare fra menylinjen og kommandolinjen på Macen. HAVEN og menylinjen får status og stopp gjennom kontrollbroen. *(Innsnevret: opprett og pause fra HAVEN blir en egen runde. Presisert 05.10, se §1c.)* | T5 |
| F5 | Det Losen ber om gjennom agenten, kjører ikke før Kjetil har godkjent det | Det finnes to slags godkjenning. En fast handling står i agentens policy. En jobb Losen ber om gjennom MCP, godkjenner Kjetil med ett trykk før den går første gang. Saken i menyen viser tittelen og én linje som agenten lager selv fra jobben: kortformen av hva som kjøres, når, og når det slutter. Hele jobben, med hvert steg ordrett, står i adminvinduet. «Godkjenn» står begge steder. En jobb som ikke kan vises i sin helhet i adminvinduet, avvises. Endres jobben, må den godkjennes på nytt. Ingen MCP-verktøy kan gi godkjenningen. Planleggeren kjører aldri skalltekst. Ukjent eller ikke godkjent jobb kjøres ikke, verken når den opprettes, når planleggeren starter eller når tiden er inne. Godkjenningen stopper ikke kode som alt kjører som Kjetil (se §2). *(Omformulert. Presisert 05.10, se §1c.)* | T4 |
| F6 | Kjetil ser hva som skjer | Hver kjøring har tidspunkt, resultat og kort sammendrag. En jobb som feiler, blir alltid én sak i menylinjen, ikke én per gang. En jobb som ble passert, blir én sak bare når den går én gang i døgnet eller sjeldnere. For jobber som går oftere, telles passeringene og vises i lista «Planlagte jobber». Står planleggeren, eller kan tilstanden ikke leses, sier menyen det. En tom liste betyr ikke ro. *(Presisert 05.10, se §1c.)* | T7, bilde |
| F7 | Losens jobber går uten egen løper | Denne tråden bruker køene som finnes. Løperen i Terminal-vinduet legges ned. Ingen ny kø bygges. *(Endret.)* | T0 |
| F8 | Ulest post blir synlig av seg selv | Innboksene sjekkes hvert 30. minutt av et fast program i agenten. Post som ingen har kvittert, blir en sak i menylinjen. Saken forsvinner når posten er kvittert. *(Presisert. Dekker behovet i HD-0069.)* | T8, bilde |
| F9 | Frister varsles i tide | Går en av Kjetils korrespondansetilganger ut om sju dager eller mindre, blir det en sak i menylinjen. *(Presisert.)* | T9 |
| F10 | Avdrift kan oppdages etter plan | Avdriftssjekken fra PDD-en om tilgangsbevis (12.09) kan settes opp som planlagt jobb når den finnes som godkjent handling. Selve sjekken bygges ikke her. | T4 (bare at en godkjent handling kan planlegges) |

## §1b Endringer i runde 3 (godkjent 02.10.2026)

Kjetil svarte 02.10 ca. kl. 18:43Z «Ja, med ett trykk (anbefalt)»: E1–E6 slik de står, og en jobb Losen ber om, venter på «Godkjenn» i menylinjen før første kjøring.

I runde 2 gransket Fabel den første planen (`panel/FABEL_SVAR.md`). Etterpå fant Losen køene som alt finnes på Macen. Fabel gransket så runde 3 (`panel/FABEL_SVAR_RUNDE3.md`). Endringene under er resultatet.

| # | Hva | Slik det sto i G1 | Foreslått nå | Hvorfor |
|---|---|---|---|---|
| E1 | F7 og valget «Også Losens skript» | Losens egen løper gjøres varig, synlig og stoppbar. Den kjører hva som helst. | Ingen ny kø. Denne tråden går over på køene som finnes. En planlagt jobb fra Losen blir en jobb i `.agent-spool`. Frie skallskript startes ikke av planleggeren. | En fjerde kø ville gitt enda et sted der noe kan kjøre som deg, utenfor koordineringen de andre trådene følger. |
| E2 | F5 | En jobb kan bare utløse handlinger du har godkjent. | En jobb Losen ber om, venter på ett trykk fra deg i menylinjen før den går første gang. Endres jobben, må den godkjennes på nytt. | I G1 valgte du at Losens jobber går uten godkjenning. Fabel pekte på at Losen da får noe nytt: å sette i gang arbeid om natten, hver natt, også etter å ha blitt lurt av innhold den har lest. Ett trykk per ny jobb stenger den veien gjennom agenten. Det stenger ikke veien gjennom køene, der kode kjører som deg. Vil du heller ha det som i G1, sier du det. |
| E3 | F4 | HAVEN når det samme som Losen gjennom en celle på kontrollbroen. | HAVEN og menylinjen får status og stopp nå. Opprett og pause fra HAVEN blir en egen runde. | Det holder for å se og stoppe. Resten er en ny flate i HAVEN. |
| E4 | F8 og F9 | Kjøres som planlagte jobber. | To faste programmer i agenten. De leveres først, på planleggeren som kjører i dag. | De finnes ikke i dag. De kan leveres uten ny agent, og bygg av ny agent er stanset av diskregelen akkurat nå. |
| E5 | F6 | En ny kilde i menylinjen for planlagte jobber. | Kilden `job` og de fire svarene som finnes (godkjenn, avvis, åpne, ignorer i dag) brukes. | En ny kilde eller et nytt svar gjør at en eldre menyapp ikke kan lese noe (HD-0074). |
| E6 | F8 | «Det som krever Kjetil, blir en sak.» | Saken betyr «ulest post som Losen ikke har lest ennå». Programmet kan ikke vurdere hva som krever deg. Det gjør Losen når den leser, og sier det i samtalen som i dag. | Et program som teller ukvitterte meldinger, kan ikke vite mer enn det. |

## §1c Presiseringer, godkjent 05.10.2026

Kjetil svarte 05.10.2026: «G2 er godkjent og det er også forslagene dine til F5 F6 F4.» Alle tre presiseringene er dermed godkjent slik de sto, og tabellen i §1 er endret etter dem. Kolonnen «Slik det står» viser ordlyden fra før 05.10.

Bakgrunnen: da kontrakten ble skrevet og gransket (`panel/FABEL_SVAR_G2.md`), viste tre av målene seg å si mer enn det som kan bygges, eller noe som ville plaget Kjetil daglig. De ble lagt fram i `PLAN.md` under «Tre presiseringer du svarer på hver for seg», hver for seg, fordi et ja til G2 ikke var et svar på dem.

| Formål | Slik det sto før 05.10 | Presiseringen (godkjent) | Hva et nei ville betydd |
|---|---|---|---|
| F5 | Saken viser hva som kjøres, når, og når det slutter | Menyen viser tittelen og én linje: agentens kortform av hva som kjøres, og når. Hele jobben står i adminvinduet. «Godkjenn» står begge steder. En jobb som ikke kan vises i sin helhet i adminvinduet, avvises. | «Godkjenn» står bare i adminvinduet. Menyen og adminvinduet tegner i dag de samme knappene fra saken (`HavenAgentMenuApp.swift` linje 83–91, `AdminWindow.swift` linje 136–143), så det krever ny menyapp alt i trinn 4. |
| F6 | En jobb som feiler eller ble passert, blir én sak | Feil gir alltid sak. Passering gir sak bare for jobber som går én gang i døgnet eller sjeldnere. For de som går oftere, telles passeringene og vises i lista «Planlagte jobber». | Korrespondansesjekken gir en sak hver gang Macen har sovet i mer enn en time, eller Kjetil velger en annen grense. |
| F4 | Losen kan be om, liste, pause og stoppe planlagte jobber gjennom MCP | Pause og stopp gjennom MCP gjelder jobber som er bedt om. De faste programmene i `config.json` styres bare fra menylinjen og kommandolinjen på Macen. | En assistent kan sette korrespondansesjekken og fristvarselet på pause eller stoppe dem uten trykk. Da får F8 og F9 en ny måte å slutte å virke på. |

## §2 Grense

Dette er ikke med:

- En ny jobbkø. Køene som finnes, endres heller ikke. Svakhetene i tillatt-lista i `.agent-tools/agent_job_runner.py` meldes til kø-tråden som egen oppgave.
- Frie skallskript til planlagt tid.
- Et vern mot kode Losen får kjørt gjennom køene. Den koden kjører som Kjetil. Den kan endre agentens konfigurasjon, og den kan gi godkjenningen i F5 selv, fordi agenten ikke kan skille menylinjen fra et annet program på samme Mac. Det vernet finnes ikke i dag, og denne PDD-en lager det ikke.
- Planlagte oppgaver i Claude-skyen. De når ikke Macen når broen er nede. Det er problemet denne PDD-en løser.
- `TimeEventEmitterCell` og Vapor Queues på serveren (CellScaffold).
- Produksjon og andre maskiner enn Kjetils.
- Varsel om at andres tilganger går ut (Vegars eller Victorias). Det vet bare serveren, og det hører hjemme i CellScaffold.
- At Losen kan skrive egne «krever deg»-saker for post. Det trenger et eget verktøy.
- Selve avdriftssjekken (F10 gjelder bare at den kan planlegges).
- Deploy-status i menylinjen. Den har egen oppgave i deploykøen (HD-0075).

Avhengigheter, hver med sin verifikator:

| Avhengighet | Verifikator | Tilstand 02.10 |
|---|---|---|
| Mappene `.agent-spool`, `_losen-queue` og `HAVEN-Deploy` er koblet til denne tråden | En jobb fra tråden kjører i `.agent-spool`, og resultatfila kommer i `outbox/` | koblet til 02.10 (HAVEN-roten). Jobben er ikke kjørt ennå. |
| `gh` kan nås fra `.agent-spool` | En jobb med `gh api user` gir `ok` | trolig ikke: løperen har ikke Homebrew på `PATH`, og den godtar bare programnavnet `gh`. Måles i trinn 0. Virker det ikke, går `gh`-arbeid som navngitte skript i `_losen-queue`. |
| Planleggeren kjører | `launchctl print` viser den som kjørende | målt: kjører |
| Menylinjen leser kilden `correspondence` | `GET /challenges` gir kilden som `read` | målt: `read` |
| Klienten som er installert, har verktøyet programmet venter | `tools/list` viser `correspondence_list_inbox` (eller `correspondence.list_inbox`) uten krav om `relationshipID` | måles i trinn 1. Programmet måler det selv ved hver kjøring. |
| Korrespondanseklienten kan kjøres av planleggeren uten dialog | Den første planlagte kjøringen av korrespondansesjekken gir `lastError: null` i tilstandsfila | måles i trinn 1 |
| Fristen for tilgangsbeviset kan leses lokalt | `profile.json` har `accessCredential.payload.expiresAt` | målt: finnes |
| Det er nok disk til å bygge agenten | Kapasitetsvakten (40 GiB og 5 % etter reserve) slipper bygget gjennom | målt 02.10 kl. 18:56Z: 54 GiB, for lite |
| Agenten bygges og installeres etter køens regel | PR mot `main`, merge på Kjetils ord, installasjon fra merge-commiten i et vindu avtalt i `_losen-queue/KOORDINERING.md` | ikke avtalt |
| En ny agentbinær kan installeres uten at macOS dreper den | `Scripts/install-agent-dev.sh` (Developer ID, `bootout` og `bootstrap`); `launchctl print` viser jobben som kjørende | virket 26.09 |
| En eldre agent tåler det den nye skriver | Binæren fra 26.09 leser konfigurasjonen og tilstandsmappen etter trinn 3 uten å krasje | testes i T10 |
| Agentens MCP-server kan nås fra Claude-appen | `tools/list` fra appen viser `agent.schedule.list` | ikke lagt inn |
| Varsler kan dempes av Fokus (målt 23.09) | Saken vises i menyen og i tallet ved ikonet selv om banneret uteblir | uendret |

## §3 Det du kommer til å se

Etter G2 er det bare denne tabellen som teller som fremdrift.

| # | Leveranse | Type | Hvor |
|---|---|---|---|
| 1 | Jobbene fra denne tråden går gjennom `.agent-spool`, og Terminal-vinduet er borte | kjørende flate | `.agent-spool/outbox/` |
| 2 | Ulest post gir en sak i menylinjen, uten at noen har startet noe | kjørende flate, med bilde av den ekte menyen | menylinjen; `images/` |
| 3 | En sak sju dager før en av tilgangene dine går ut | kjørende flate og testutdata | menylinjen; `TESTRESULT.md#t9` |
| 4 | Testene T1–T5 med ekte utdata | testutdata | `TESTRESULT.md` |
| 5 | Losen ber om en jobb fra Claude-appen mens du ser på. Du godkjenner den i menylinjen, og den kjører til avtalt tid. | bilde som godkjennes før bygging, deretter kjørende flate | `images/meny-jobb-godkjenning-v4.png` |
| 6 | «Planlagte jobber» i menylinjen, med pause og stopp, og en sak når en jobb feiler | bilde som godkjennes før bygging, deretter kjørende flate | `images/meny-planlagte-jobber-ro-v3.png`, `images/meny-planlagte-jobber-feil-v3.png`, `images/meny-planleggeren-staar-v2.png` |
| 7 | Dokumentasjon av kontrakten, og hva køene åpner for | fil | `Docs/ScheduledEvents.md`, `Docs/SecurityModel.md`, `Docs/OperatorRunbook.md` |

## §4 Lærdommer som gjelder

- `lesson.paste-command-instead-of-queue`: Kjetil skal aldri få kommandoer å lime inn.
- `lesson.purpose-never-grants-rights`: et formål eller en tidsplan kan innsnevre en rett, aldri opprette den.
- `lesson.plan-instead-of-delivery`: etter G2 teller bare leveransene i §3.
- `lesson.corr-approval-surfaces-timed-out`: avhengighetene i §2 sjekkes før den egentlige testen.
- `lesson.bridge-inferred-architecture-from-one-use`: les kilden før en antakelse bærer planen.
- Fra denne økten, lagt i registeret: Losen kartla bare HavenAgentD før G1 og før den første planen, og fant ikke køene og koordineringsreglene i mappen over. Kartleggingen skal dekke hele `HAVEN`-roten og `launchctl list` før en ny kø, løper eller tjeneste foreslås. Og: en påstand fra minnet om hva som er installert, måles på nytt før den bærer en plan.

## §5 Tester

Dette er den ene lista over tester. Kontraktene i `contract/` viser hit.

| Id | Tester | Hvordan | Bevis |
|---|---|---|---|
| T0 | Avhengighetene i §2, og at tråden bruker køen som finnes | målinger på Macen, én rad per avhengighet. `swift test` av HavenAgentD kjøres gjennom `.agent-spool` med kapasitetsvakten før trinn 3 starter. | TESTRESULT#t0 |
| T1 | Cron-uttrykk og tidssone | enhetstester med fast klokke mot fasiten i `contract/fixtures/cron-forventninger.json` (22 uttrykk med tidspunkt, 15 tellinger, 18 som avvises, 8 korteste avstander): `30 2 28 3 *` og `30 3 28 3 *` i 2027, `30 2 25 10 *` i 2026, `* * * * *` over begge skiftene, 0 og 7 som søndag, dag eller ukedag, lister, områder og steg, og avvisning av umulig uttrykk og ukjent tidssone. Følgene av regelen for løpende uttrykk er med: `* 2 * * *` mot `0-59 2 * * *`, `5,*/10` likt med `*/10,5`, og `30 */2` mot `30 0-23/2`. | TESTRESULT#t1 |
| T2 | En jobb kan ikke henge de andre, og tilstanden overlever omstart | en jobb som sover lenger enn tidsgrensen, blir avbrutt; en jobb som skriver mer enn 64 KiB, og en som etterlater en barneprosess, henger ikke planleggeren; en jobb som skriver mer enn 8 MiB, avbrytes med utfallet `output-limit`; arbeideren stoppes og startes mellom to kjøringer; en arbeider nummer to får ikke låsen og avslutter | TESTRESULT#t2 |
| T3 | Passerte kjøringer | klokken hopper over to tidspunkt: én kjøring, passeringen telt og vist. Arbeideren drepes midt i en kjøring: samme tidspunkt kjøres ikke på nytt, og jobben blir en sak. En hendelse hvert 30. minutt gir ingen sak etter åtte timers søvn, men passeringene er telt; en daglig hendelse gir sak etter to døgn. En jobb som startes igjen etter en pause, kjøres ikke på etterskudd, og pausen telles ikke som passering. Unntaket er en fast hendelse på intervall uten cron: den kjøres straks etter at den er startet igjen, og pausen telles heller ikke da. | TESTRESULT#t3 |
| T4 | Bare det godkjente kjører | hver av de seks reglene for kjøring i `contract/trinn4-jobber-og-godkjenning.md`; ukjent handling avvises ved opprettelse, ved start og ved kjøring; en jobb med skalltekst eller egne argumenter avvises; en jobb Losen har bedt om, kjører ikke før den er godkjent; endres den etter godkjenning, kjører den ikke; en bestilling uten oppgitt id kan ikke erstatte en jobb som finnes; en jobb som ikke kan vises i sin helhet i saken, avvises; køjobb avvises når køen ikke er navngitt i konfigurasjonen; en jobbmal med `env` utenom `HAVEN_`, med et steg uten `cmd`, eller med tekst i `timeoutSeconds`, avvises; køfila får et navn køen tar, og trekkes tilbake når køen ikke har tatt den; en sak for en jobb gjør ikke innboksen uleselig (ID-liknende navn, lang tittel, en fast hendelse med id på 60 tegn) | TESTRESULT#t4 |
| T5 | MCP-kontrakten og samtidighet | `tools/list` viser verktøyene; be om, list, pause, fortsett, stopp og fjern går rundt; ingen verktøy kan godkjenne en jobb, heller ikke `agent.review.approve`; MCP kan ikke styre en fast hendelse (`fixed-event`); to bestillinger samtidig går ikke forbi taket på ti; to prosesser som styrer samme jobb samtidig, etterlater en gyldig styringsfil, og `pause` og `stop` samtidig ender i `stopped` | TESTRESULT#t5 |
| T6 | Live på Macen | en jobb Losen ber om, godkjennes i menyen og kjører til avtalt tid. Det måles hvilket navn Claude-appen og Codex oppgir, og at saken sier «Claude» eller «Codex». Etter omstart av Macen og innlogging går planleggeren igjen. | TESTRESULT#t6 |
| T7 | Synlig i menylinjen | en jobb som feiler, gir én sak; kvitteringen overlever omstart og et døgn; en ny feil etter kvittering gir ny sak; en stoppet jobb kjører ikke; står arbeideren, kommer saken «Planleggeren går ikke», og den kommer ikke mens et program kjører i fem minutter; kan tilstanden ikke leses, er kilden `job` ulesbar og ikke tom; en sak om en fast hendelse har bare «Kvitter» og «Åpne», og et `reject` sendt på den likevel gir `accepted: false` og skriver ingenting | bilde av den ekte menyen + TESTRESULT#t7 |
| T8 | Korrespondansesjekken | med prøvedata (programmets `selvtest`, se `contract/trinn1-2-programmer.md`): ulest post gir markør, kvittert post fjerner den, to feil på rad gir markøren «sjekken feilet» mens markørene for ulest post står urørt, en klient med annen kontrakt gir feil og ikke tom liste, en klient som henger, blir drept innen tidsgrensen, tre profiler deler tidsbudsjettet og fem avvises, søskenvakten gir ikke markør når eget stempel er gammelt, en avsender med ID-liknende navn eller lang tittel gjør ikke innboksen uleselig. Live: en ekte ulest melding gir en sak, og menyen leses av 30 minutter etter at planleggeren er stoppet. | TESTRESULT#t8 + bilde |
| T9 | Fristvarselet | med prøvedata: 8 døgn og 0 timer igjen gir ingen sak, 7 døgn og 23 timer gir sak, passert frist gir «gikk ut», manglende bevis gir «uten bevis», fornyet tilgang fjerner saken | TESTRESULT#t9 |
| T10 | Ingen regresjon, og eldre agent tåler det nye | full testmengde i HavenAgentD med `swift test --no-parallel`, sammenlignet på testnavn mot `origin/main`. Binæren fra 26.09 startes mot ny konfigurasjon og ny tilstandsmappe uten å krasje, og kjører fristvarselet på intervall. Den nye binæren skriver `config.json` uten å miste de nye feltene. Installasjonen av de faste programmene tas ut igjen og legges inn igjen. | TESTRESULT#t10 |

## §6 Åpne spørsmål

Ingen spørsmål om formålene F1–F10 er åpne. De tre om presiseringene i §1c ble besvart 05.10.2026, med ja til alle tre:

1. **F5.** Holder det at menyen viser agentens kortform av jobben, og at hele jobben står i adminvinduet, når «Godkjenn» står begge steder? **Ja.**
2. **F6.** Skal passering gi sak bare for jobber som går én gang i døgnet eller sjeldnere? **Ja.**
3. **F4.** Skal pause og stopp gjennom MCP bare gjelde jobber som er bedt om? **Ja.**

De to spørsmålene fra runde 3 ble besvart 02.10:

1. Godkjenner du endringene E1–E6 i §1b? **Ja.**
2. E2: ett trykk per ny jobb, eller uten godkjenning som i G1? **Ett trykk.**

Ett spørsmål er åpent. Det gjelder grensen i §2, ikke formålene:

1. **Skal Vegar og Victoria ha planlagte jobber på sine Macer?** Det betyr en sak i menylinjen når det ligger ulest post, og når tilgangen deres snart går ut. §2 sier i dag at andre maskiner enn Kjetils ikke er med. Et ja betyr en egen formålsrunde for en ny installerer, med tre deler som ikke finnes i dag: agenten og planleggeren må startes hos dem, menyappen må inn i pakken, og korrespondansevakten må skrives om fra Python til Swift. Anbefalingen er ikke nå, av to grunner. Sakene har gale titler til trinn 5 er ferdig. Og den nye korrespondanseklienten bør følge med i samme pakke, og den virker ikke mot staging før bro-ruten er der (HD-0166). Fornyelsen deres trenger ingen ny installerer (§0).

Uansett når en ny installerer kommer, prøves den slik før Kjetil sender den. Lista er et utgangspunkt for den formålsrunden, ikke en godkjent testliste:

1. Fila som sendes, er fila som ble prøvd: sjekksummen tas etter at billetten er stiftet på.
2. Gatekeeper slipper den gjennom på en Mac som aldri har sett Digipomps.
3. Hver binær har begge arkitekturer, og starter både på Apple Silicon og på en Intel-Mac. Finnes ingen Intel-Mac å prøve på, står det i klartekst.
4. Installert over 0.3.2 virker korrespondansen videre uten ny innmelding: liste, lese, sende og kvittere mot staging.
5. Fornyelse med fersk invitasjon virker med klienten i pakken.
6. Det nye pakken har med, virker uten utviklerverktøy på Macen og uten dialoger brukeren ikke er forberedt på.
7. 0.3.2 kan legges inn igjen, og virker da som før.

## §7 Runder

| Runde | Dato | Hva som endret seg |
|---|---|---|
| 1 | 01.10–02.10.2026 | Utkast med F1–F10 og tre spørsmål. Kjetil svarte og godkjente G1 02.10. |
| 2 | 02.10.2026 | Fabel gransket planen. Tre endringer i formålene foreslått. Køen skulle bli en egen launchd-jobb. Ikke lagt fram for Kjetil. |
| 3 | 02.10.2026 | Losen fant tre jobbkøer under launchd og koordineringsreglene i `_losen-queue/`. Planen fra runde 2 er trukket. Ingen ny kø. Fabel gransket runde 3 og krevde ti endringer, og kontrollerte dem etterpå (`panel/FABEL_ETTERKONTROLL_RUNDE3.md`). De er tatt inn: F5 handler om godkjenning og får ett trykk per ny jobb (E2), F8 sier hva saken betyr (E6), F6 bruker kilden og svarene som finnes (E5), trinnene på dagens planlegger har grensene sine skrevet ned, og eldre agent skal tåle det nye. Påstandstabellen er målt på nytt: agenten er bygget fra `main`, ikke fra testflyt-grenen. |
| 3, fortsatt | 02.10.2026 kveld | Kjetil godkjente E1–E6 med ett trykk per ny jobb. Kontraktene (`contract/`), dataflyten og rekkefølgen for køene ble skrevet mot kilden på `origin/main`. Formålene F1–F10 er uendret. Nytt i påstandstabellen: den installerte korrespondanseklienten er pilotklienten og ikke den på `main`; kilden `job` var satt av til AgentJobs; en MCP-klient kan alt i dag godkjenne fjernintenter og få et fast program kjørt; agenten har en egen tidsplan for Personal Butler. T5 og T8 er presisert. Bildet for godkjenning er rettet (v4), og bildet av lista (v3). Fabel gransket G2-artefaktene (`panel/FABEL_SVAR_G2.md`: seks punkter som måtte rettes, tjue som burde, sytten mangler). Alt er tatt inn; tre av dem er presiseringer av F4, F5 og F6 som legges fram sammen med G2 (§1c). Fabel kontrollerte rettelsene (`panel/FABEL_ETTERKONTROLL_G2.md`): 26 av 26 var løst, og rettelsene hadde laget tretten nye feil. De er rettet, og Fabel kontrollerte rettelsene (`panel/FABEL_ETTERKONTROLL2_G2.md`: 13 av 13 løst, fem småting til, som også er rettet): saker om faste hendelser har bare «Kvitter» og «Åpne», og pause står i lista «Planlagte jobber» (feil-bildet v3), §5 er den ene lista over tester, de tre presiseringene står som åpne spørsmål i §6, `resume` henter ikke inn pausen, og titler over 80 tegn avkortes. |
| 4 | 05.10.2026 | Kjetil godkjente G2 og de tre presiseringene. §1 er endret for F4, F5 og F6, og §1c og §6 sier at de er godkjent. §0 har fått svaret ordrett, med det som er målt om installereren. Ett nytt åpent spørsmål i §6, om grensen i §2: skal mottakerne ha planlagte jobber på sine Macer. |
| 4, fortsatt | 05.10.2026 kveld | §0 er rettet: det var ikke belagt at Victoria har 0.3.2-pakken. Formålene er uendret. CI for PR #30 ble rødt av en grunn som også gjelder `main`, og en uavhengig kontroll fant seks feil i planleggeren, to av dem på `main`; rettelsene er i `ffe1aae` (lokalt). Det står i `TESTRESULT.md` og `STATUS.md`, og endrer ikke formålene eller testene i §5. |
