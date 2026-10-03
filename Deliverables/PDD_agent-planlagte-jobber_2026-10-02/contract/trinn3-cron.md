# Trinn 3: cron og robusthet i planleggeren

Trinn 3 endrer planleggeren i agenten (`ScheduledEventService`). Det krever ny agent, og det går som PR mot `main`.

## Hendelsene i `config.json` får fire valgfrie felt

`scheduledEvents` i `config.json` er Kjetils egne, faste hendelser. De får fire nye felt, alle valgfrie:

| Felt | Type | Betydning |
|---|---|---|
| `cron` | tekst | Fem felt. Når det er satt, styrer det tidspunktene, og `intervalSeconds` brukes ikke. |
| `timeZone` | tekst | IANA-navn, for eksempel `Europe/Oslo`. Påkrevd når `cron` er satt, og en feil uten `cron`. |
| `timeoutSeconds` | heltall | Tidsgrense for én kjøring. Standard 900. Minst 10, høyst 3600. |
| `title` | tekst | Navnet som vises i lista «Planlagte jobber» og i saker, høyst 40 tegn. Uten det vises id-en. Installasjonsskriptet krever `title`, eller en id på høyst 40 tegn, for hendelsene det legger inn. En sakstittel som likevel blir over 80 tegn, avkortes (`trinn4-jobber-og-godkjenning.md`). |

`firstFireAt`, `repeatMode` og `intervalSeconds` står som før, også når `cron` er satt, og en hendelse som gjentas, må fortsatt ha `intervalSeconds`. Med cron holder `firstFireAt` hendelsen tilbake: ingen tidspunkt før det kjøres. Det er bevisst: `ScheduledEventDefinition` har automatisk dekoding (`ScheduledEventService.swift` linje 10–16), så en agent uten cron ser bort fra de nye feltene når den leser, og kjører hendelsen på intervallet. Rulles agenten tilbake, går fristvarselet videre hvert døgn, bare ikke kl. 09:00.

Det gjelder lesing. En eldre agent som **skriver**, tar ikke de nye feltene med:

- Den eldre arbeideren skriver `State/scheduled-events.json` på nytt ved start og etter hver kjøring (linje 169, 235 og 268). Da er `lastOccurrence`, `missedCount` og `attention` borte. Når den nye agenten er tilbake, regner den fra første gang den ser hendelsen, uten etterslep.
- `haven-agentd setup` skriver `config.json` gjennom `AgentConfig.write` (`AgentSetupService.swift` linje 242). Kjøres `setup` med en eldre binær, forsvinner `cron`, `timeZone`, `timeoutSeconds`, `title` og `scheduledJobs` fra fila. Etter en tilbakerulling skal `setup` derfor ikke kjøres; skjer det likevel, legges feltene inn igjen med installasjonsskriptet.
- Den nye binæren må ha feltene i `ScheduledEventDefinition` og `AgentConfig`, så dens egen `write` tar dem med. T10 skriver og leser fila gjennom begge.

Dette endrer AP6 og AP7 i `PLAN_VEDLEGG.md`. Runde 3 sa at cron aldri skulle stå i `config.json`, for at en eldre agent skulle kunne lese fila. Med valgfrie felt kan den det, og faste hendelser slipper en egen fil. Jobber en assistent ber om, bor fortsatt utenfor `config.json` (trinn 4).

Tre ting må **ikke** endres, for da kan en eldre agent ikke lese filene i det hele tatt:

- Ingen nye verdier i `repeatMode` (`once`, `count`, `untilStopped`). En ukjent verdi gjør at hele `config.json` avvises, og da starter verken agenten eller planleggeren.
- Ingen nye verdier i `action.kind` (`shortcut`, `appleScript`, `localTask`) i `config.json`, av samme grunn. Køjobber (`spoolJob`) finnes derfor bare i jobbene fra trinn 4, som ligger utenfor `config.json`.
- Ingen nye verdier i `status` i `State/scheduled-events.json` (`scheduled`, `running`, `completed`, `stopped`). Pause lagres i en egen styringsfil (trinn 4 og 5).

Fra og med trinn 3 er to felt til lukket på samme måte: `lastOutcome` (`ok`, `failed`, `timeout`, `interrupted`, `output-limit`) og `attention.kind` (`failed`, `missed`) i `State/scheduled-events.json`. En fil med en annen verdi i ett av dem er uleselig for agenten fra trinn 3: en arbeider som starter, nekter å starte på den, og en arbeider som går, skriver den på nytt fra det den selv har. Senere trinn legger derfor ikke nye verdier i disse feltene. Skal noe nytt sies, får det et eget, valgfritt felt. Jobber en assistent ber om (trinn 4), har sin egen tilstandsfil, `State/ScheduledJobs/<id>.runtime.json`, med egne verdier (`invalid`, `refused`, `no-result`, `withdrawn`); de verdiene skal aldri stå i `State/scheduled-events.json`. En test i trinn 3 holder dette fast (`aStateFileWithAnOutcomeOrAKindThisAgentDoesNotKnowIsUnreadableToIt`).

En hendelse med `cron` og uten `timeZone`, eller med et uttrykk som ikke kan tolkes, er ugyldig. Da nekter planleggeren å starte, som den gjør for ugyldige hendelser i dag (`ScheduledEventService.validate`), og `schedule-list --config <fil>` viser feilen uten å skrive noe.

## Cron-reglene

`cron_reference.py` er reglene som kjørbar tekst, og `fixtures/cron-forventninger.json` er fasiten: 22 uttrykk med forventede tidspunkt, 15 tellinger over skiftene, 18 uttrykk som skal avvises, og 8 korteste avstander. Fasiten er regnet ut på to uavhengige måter, og Fabel har regnet den etter på en tredje (`../panel/FABEL_SVAR_G2.md` og `../panel/FABEL_ETTERKONTROLL_G2.md`). Swift-implementasjonen (`CronSchedule`) skal gi de samme svarene (T1). Den spør sonen om bare én ting, avstanden til UTC ved et tidspunkt, og regner resten med heltall. Den framgangsmåten er prøvd i Python mot fasiten og mot referansen på 700 tilfeldige uttrykk i tolv soner, uten avvik. Koden er skrevet 03.10 og ligger i kodepakken i `../handoff/`. Den er bygget og testet på Linux med Swift 6.2.3 (som lot seg hente fra Ubuntu-arkivet), og `CronSchedule` gir fasiten 63 av 63. macOS-grenene i koden er ikke kompilert; bygg på Macen eller i CI gjenstår.

1. Fem felt: minutt, time, dag i måneden, måned, ukedag. Ukedag 0 og 7 er søndag. Hvert felt er en kommaliste av `*`, `*/n`, `a`, `a-b` og `a-b/n`. Tall skrives med sifrene 0–9. Navn og makroer støttes ikke.
2. Er både dag i måneden og ukedag noe annet enn `*`, holder det at én av dem stemmer.
3. Uttrykket leses i tidssonen som er oppgitt. Sonen er `UTC` eller et IANA-navn på formen Område/Sted, for eksempel `Europe/Oslo`. Forkortelser («CET») og avstander («GMT+2») avvises, så regelen er lik på alle plattformer. Navn under `Etc/` har den godtatte formen og avvises ikke; `Etc/GMT+2` er to timer *vest* for UTC. Sonen lagres alltid uttrykkelig; det finnes ingen standardsone.
4. Sommertid. Et uttrykk er **løpende** når minutt- eller timefeltet har et ledd som er `*` eller `*/n`, uansett hvor i lista leddet står. Ellers er det et **fast klokkeslett**.

| | Time som kommer to ganger (25.10.2026 kl. 02) | Time som ikke finnes (28.03.2027 kl. 02) |
|---|---|---|
| Løpende, for eksempel `*/10 2 * * *` | kjører i begge timene | kjører ikke |
| Fast klokkeslett, for eksempel `30 2 * * *` | én kjøring, den første | én kjøring, i det klokka har hoppet (kl. 03:00) |

5. Flere faste klokkeslett i samme hopp gir én kjøring, også når tidspunktet de flyttes til, er et vanlig treff. `0 2,3 * * *` gir én kjøring 28.03.2027, kl. 03:00.
6. «Etter» er strengt. Tidspunktene er alltid hele minutter.
7. Søket etter neste tidspunkt stopper etter åtte år. Finnes ingen, er uttrykket umulig og avvises.

Reglene bygger på cronie, som er det folk kjenner fra Linux. Ett sted er de enklere: cronie ser bare på om feltet *begynner* med `*`, så `5,*/10` og `*/10,5` oppfører seg ulikt der. Her er begge løpende.

Følger som er verdt å vite, og som står i fasiten. Det som er skrevet med `*`, følger klokka. Det som er skrevet med tall, er fast, også når det treffer de samme minuttene eller timene:

| Uttrykk | 25.10.2026 (time 2 kommer to ganger) | 28.03.2027 (time 2 finnes ikke) |
|---|---|---|
| `* 2 * * *` (løpende) | 120 kjøringer | ingen |
| `0-59 2 * * *` (fast, selv om det ser likt ut) | 60 kjøringer | én, kl. 03:00 |
| `5,*/10 2 * * *` og `*/10,5 2 * * *` (begge løpende) | 14 kjøringer | ingen |
| `30 */2 * * *` (løpende i timefeltet) | 13 kjøringer det døgnet, mot 12 ellers | 11 |
| `30 0-23/2 * * *` (fast, selv om timene er de samme) | 12 | 12; den som mangler, går kl. 03:00 |

## Hva arbeideren husker per hendelse

`State/scheduled-events.json` får nye, valgfrie felt i hver post. En eldre agent ser bort fra dem.

| Felt | Betydning |
|---|---|
| `lastOccurrence` | Det planlagte tidspunktet som sist ble tatt, enten det ble kjørt eller hoppet over. Skrives **før** kjøringen starter. |
| `currentRun` | `occurrence` og `startedAt` for en kjøring som er startet og ikke ferdig. Skrives sammen med `lastOccurrence`, og fjernes når kjøringen er over. |
| `missedCount`, `missedSince`, `missedLatest` | Antall planlagte tidspunkt som passerte uten kjøring siden sist det ble kvittert, og det første og det siste av dem. Kvitteringen (`<id>.ack.json`, trinn 4) nullstiller tellingen når `throughOccurrence` når det siste. |
| `countingFrom`, `scheduleSignature` | For en hendelse med cron: når den først ble sett med dette uttrykket og denne sonen. Ingenting før det regnes som passert. Endres uttrykket eller sonen, begynner tellingen på nytt. |
| `lastOutcome` | `ok`, `failed`, `timeout`, `interrupted` eller `output-limit`. |
| `lastExitCode`, `lastLog` | Avslutningskode, og stien til loggfila under `Logs/ScheduledJobs/<id>/`. |
| `attention` | `{kind, occurrence, since}`. Satt med `kind: failed` når siste kjøring ikke var `ok`. Satt med `kind: missed` når tidspunkt er passert **og tidsplanen går én gang i døgnet eller sjeldnere** (korteste avstand minst 23 timer). Feil går foran passering. Det er dette som blir en sak i trinn 4. **En stoppet hendelse ber ikke om noe:** `attention` fjernes når hendelsen stoppes (`schedule-stop`), også når siste kjøring feilet eller ble avbrutt, for den som stoppet den, har bestemt at den er over. `lastOutcome` og `lastError` står, så lista fortsatt viser hva som skjedde sist. |

## Regler for kjøring

- **Passerte tidspunkt (F3).** Ved hver runde regnes alle planlagte tidspunkt etter `lastOccurrence` og fram til nå. Er det ett, kjøres hendelsen. Er det flere, kjøres den én gang for det siste, og resten legges til `missedCount`, høyst 10 000 i én runde. En hendelse uten `lastOccurrence` regner fra da den først ble sett (`countingFrom`), så ingenting kjøres på etterskudd første gang. Det samme gjelder en post som noe uten cron har skrevet, for eksempel en eldre agent: den regnes fra da den nye arbeideren ser den. Etter en kjøring er neste tidspunkt det første etter det som ble tatt, så et tidspunkt som passerte mens programmet gikk, er forfalt ved neste runde.
- **Passering gir ikke alltid en sak.** En hendelse som går oftere enn én gang i døgnet, passerer mange tidspunkt hver natt Macen sover. Korrespondansesjekken ville gitt en sak hver morgen. For slike hendelser telles passeringene og vises i lista «Planlagte jobber», men de gir ingen sak. For hendelser som går én gang i døgnet eller sjeldnere, gir passering en sak. Dette er en presisering av F6 som Kjetil tar stilling til i G2.
- **Intervall uten cron** virker som i dag: neste tidspunkt er forrige kjøring pluss intervallet. Starter en kjøring senere enn planlagt, legges antall hele intervaller mellom det planlagte tidspunktet og starten til `missedCount`. Åtte timers søvn gir 15 eller 16 for en hendelse hvert 30. minutt, etter hvor lenge det var igjen til neste kjøring da Macen sovnet. En hendelse som aldri har kjørt, teller ingenting ved første kjøring, uansett hvor gammel `firstFireAt` er. Ellers ville fristvarselet gitt en sak om passering første gang det kjørte med en ny tilstandsmappe. Tidspunktet den første kjøringen tar (`lastOccurrence`), er det siste på intervallet som er kommet, regnet fra `firstFireAt`. Feiler den første kjøringen, peker saken derfor på i dag og ikke flere døgn tilbake.
- **Aldri samme tidspunkt to ganger.** `lastOccurrence` og `currentRun` skrives til disk før programmet startes. Lykkes ikke skrivingen, startes ikke programmet. Finner arbeideren en `currentRun` uten slutt når den starter, ble kjøringen avbrutt. Da settes utfallet til `interrupted`, og kjøringen gjentas ikke. Bare arbeideren gjør dette, for bare den holder låsen som sier at ingenting kjører.
- **Arbeideren blir bedt om å stoppe.** Programmet som kjører, stoppes som ved tidsgrensen, og utfallet er `interrupted`. Arbeideren tar ikke flere tidspunkt: en hendelse som var forfalt og ikke startet, står som forfalt og kjøres av neste arbeider. Det gjelder også en hendelse som har fått tidspunktet sitt skrevet, men der programmet ennå ikke finnes: da gis tidspunktet tilbake, kjøringen telles ikke, og hendelsen ber ikke om noe. `BoundedProcessRunner` skiller de to: `notStarted` når ingenting ble startet, `interrupted` når programmet ble startet og stoppet. Ett tilfelle leses likevel som en avbrutt kjøring uten at noe kjørte: arbeideren drepes med SIGKILL mellom skrivingen av tidspunktet og tilbakegivingen. Neste arbeider kan ikke se forskjellen, og kjører ikke det tidspunktet.
- **Tidsgrense.** Programmet startes i egen prosessgruppe, med vanlig signalbehandling: arbeideren overser selv SIGTERM og SIGINT, og det ville ellers blitt arvet. Etter `timeoutSeconds`, regnet mens Macen er våken, får gruppen SIGTERM, og fem sekunder senere SIGKILL. Utfallet er `timeout`.
- **Utdata.** stdout og stderr går til `Logs/ScheduledJobs/<id>/<tidspunkt>.log` (starttidspunktet, på formen `20261003T073000Z`), ikke til rør, så verken mye utdata eller en barneprosess som holder røret åpent, kan henge arbeideren. Blir loggfila større enn 8 MiB, avbrytes kjøringen med utfallet `output-limit`. De siste 2000 tegnene blir sammendrag. Logger eldre enn 30 dager fjernes, og høyst 50 beholdes per hendelse.
- **Én om gangen.** Hendelsene kjøres fortsatt etter tur. Med tidsgrensen kan én hendelse forsinke de andre med høyst sin egen grense.
- **Én arbeider.** Arbeideren holder en lås (`flock`) på `State/ScheduledJobs/worker.lock` så lenge den lever. En arbeider som ikke får låsen, avslutter med en melding.
- **Tilstandsfila.** `State/scheduled-events.json` leses, endres og skrives mens `State/scheduled-events.json.lock` holdes, så `schedule-stop` og arbeideren ikke skriver over hverandre. `schedule-stop` endrer bare den ene hendelsen. Blir fila uleselig mens arbeideren går, skriver arbeideren den på nytt fra det den selv har, og sier fra på stderr. `schedule-list` og `schedule-stop` nekter å bruke en fil de ikke kan lese, og skriver aldri over den. En arbeider som finner fila uleselig **når den starter**, har ingen god kopi. Den lar fila stå, skriver på stderr hvilken fil det gjelder og at den må flyttes til side, og avslutter. launchd starter den igjen, og den nekter igjen: ingenting kjøres, og livstegnet uteblir, til fila er rettet eller flyttet. Flyttes den, begynner hver hendelse på nytt fra konfigurasjonen: en hendelse med cron regner fra da, en hendelse på intervall kjører én gang uten å telle noe, en engangshendelse som var kjørt, kjøres igjen, og en hendelse som var stoppet, blir planlagt igjen. En pause ligger i en egen fil og gjelder fortsatt; tellingene av passerte tidspunkt begynner på null, så en kvittering har ikke noe igjen å gjelde for. Dette står i `Docs/ScheduledEvents.md` («When the state file cannot be read»). En test holder fast at arbeideren nekter, hva den sier, at fila ikke skrives over, at ingenting kjøres, og hva som skjer med hver type hendelse når fila flyttes (cron, intervall, engang, antall, pause og stoppet), og at loggene står. At launchd starter arbeideren igjen, og at livstegnet uteblir så lenge, er lest av `HavenAgentMain.swift` og plistmalen, og ikke prøvd. Kan arbeideren ikke **skrive** fila, kjører den ingenting, og etter tre skrivinger som feiler på rad, holder den livstegnet tilbake til den kan skrive igjen. Det er normalt tre runder, og færre når flere hendelser er forfalt i samme runde, for arbeideren prøver én gang for hver av dem.
- **Livstegn.** Hvert 30. sekund skrives `State/ScheduledJobs/worker.json` med `pid`, `startedAt` og `heartbeatAt`. Det gjøres av en egen oppgave i arbeideren, uavhengig av løkka som kjører hendelsene, så et program som bruker ti minutter, ikke ser ut som en død planlegger. T7 prøver det med et program som sover i fem minutter.
- **Pause.** En fast hendelse som er satt på pause (trinn 5), beholder sitt `nextFireAt` i `State/scheduled-events.json`. Arbeideren lar bare være å kjøre den. Kan styringsfila ikke leses, kjøres hendelsen ikke, og `lastError` sier hvorfor: ukjent betyr nei. Sier fila `stopped` for en fast hendelse, kjøres den heller ikke, og `lastError` sier det. Et `changedAt` fram i tid leses som nå. Styrings- og kvitteringsfilene finnes bare for id-er av små bokstaver, sifre, `.`, `_` og `-` (høyst 64 tegn), der første tegn er en bokstav eller et siffer; en hendelse med en annen id kan ikke settes på pause eller kvitteres. Etter en tilbakerulling kjenner den eldre agenten ikke pausen og kjører hendelsen igjen. Når hendelsen startes igjen, hentes ikke pausen inn: det som passerte, kjøres ikke og telles ikke (regelen står i `trinn4-jobber-og-godkjenning.md`, under styringen).
- **Planleggerens plist** legges i `Launchd/io.digipomps.haven.agentd.scheduler.plist` i repoet som mal. `Scripts/install-agent-dev.sh` skriver den til `~/Library/LaunchAgents/` når det ikke ligger en plist der, og rører aldri en som finnes. I dag finnes den bare i `~/Library/LaunchAgents/`.

## Kommandoer

`schedule-worker`, `schedule-list` og `schedule-stop` finnes. `schedule-list` får de nye feltene i utdataene. `schedule-list --config <kopi>` validerer fortsatt uten å skrive, og det er slik installasjonsskriptet kontrollerer en endret konfigurasjon før den tas i bruk.

## Det som skal testes

T1, T2, T3 og T10. Hva hver av dem prøver, står i `../FORMAALSSPEC.md` §5, som er den ene lista over tester.
