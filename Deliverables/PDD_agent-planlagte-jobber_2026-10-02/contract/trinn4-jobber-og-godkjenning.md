# Trinn 4: jobber en assistent ber om, og godkjenningen

Faste hendelser står i `config.json` og er Kjetils egne (trinn 1–3). Dette trinnet gjelder jobber som blir bedt om mens agenten går: av en assistent gjennom MCP, eller fra kommandolinjen. De bor i `State/ScheduledJobs/` og kjører aldri før de er godkjent.

## Filene, og hvem som skriver dem

Alle ligger i `~/Library/Application Support/HAVENAgent/State/ScheduledJobs/`. `<id>` er jobbens id.

| Fil | Skjema | Skrives av | Endres den? |
|---|---|---|---|
| `<id>.spec.json` | `scheduled-job-v1` | `ScheduledJobRequestService.request`, som MCP-verktøyet og `schedule-request` kaller | Nei. En ny bestilling med samme id bytter hele fila og krever ny godkjenning. |
| `<id>.<tolv tegn>.spool.json` | jobbformatet i `.agent-spool` | samme, bare for køjobber. De tolv tegnene er begynnelsen av malens sjekksum, så en `spec`-fil aldri kan peke på en annen mal enn sin egen. | Nei |
| `<id>.control.json` | `scheduled-job-control-v1` | `ScheduledJobControlService.set`, som MCP, kommandolinjen og kontrollbroen kaller | Hele fila byttes, under lås |
| `<id>.approval.json` | `scheduled-job-approval-v1` | bare `ScheduledJobApprovalService.decide` | Byttes ved ny avgjørelse |
| `<id>.ack.json` | `scheduled-job-ack-v1` | bare `ScheduledJobApprovalService.acknowledge` | Byttes ved ny kvittering |
| `<id>.runtime.json` | `scheduled-job-runtime-v1` | bare arbeideren | Ja, av arbeideren |
| `worker.json`, `worker.lock` | se `trinn3-cron.md` | bare arbeideren | |
| `Removed/` | | `agent.schedule.remove` flytter en jobbs filer hit | Leses ikke av noen |

En eldre agent kjenner ikke mappen og leser den ikke. Rulles agenten tilbake, står disse jobbene stille til den nye er tilbake.

## Bestillingen

`ScheduledJobRequestService.request` gjør dette, i denne rekkefølgen, under en lås på mappen (`flock` på `.requests.lock`), så to bestillinger samtidig ikke kan gå forbi taket:

1. **Id.** Oppgis ingen id, lages en fra tittelen. Finnes den fra før, avvises bestillingen (`id-in-use`). En bestilling erstatter en eldre bare når id-en er oppgitt uttrykkelig. Ellers kunne en ny bestilling med lik tittel ta godkjenningen fra en jobb som går. En id som er lik id-en til en hendelse i `config.json`, avvises alltid.
2. **Tidsplan.** Cron må ha tidssone og gi minst ett tidspunkt innen åtte år. `once` må ligge fram i tid. Korteste avstand mellom to kjøringer i jobbens levetid, fra nå til `endsAt`, må være minst 900 sekunder (`shortest_gap_seconds` i referansen).
3. **Sluttdato.** `endsAt` settes til 30 døgn fram når den mangler, og mer enn 90 døgn avvises. For `once` er standarden ett døgn etter tidspunktet.
4. **Handling.** `localTask` må finnes i `automationPolicy.localTasks` nå. `spoolJob` krever at `scheduledJobs.spoolInbox` og `scheduledJobs.spoolOutbox` er satt i `config.json`. Jobbmalen kontrolleres for form: `cwd` er en relativ sti uten `..`; `steps` er en liste med minst ett steg, der hvert steg har `cmd` som en liste av tekster med minst ett ledd; `timeoutSeconds` i et steg, hvis det finnes, er et heltall fra 1 til 10800, som er køens tak; `name` i et steg er en tekst, og `stopOnFailure` er sann eller usann; og `env`, hvis det finnes, er et objekt der hver nøkkel begynner med `HAVEN_` og hver verdi er en tekst. Køen regner om `timeoutSeconds` uten egen feilhåndtering (`agent_job_runner.py` linje 214), så en tekst der ville gitt en feilet jobb etter at du hadde godkjent den. Køen nekter alt annet i `env` (`agent_job_runner.py` linje 199–208), og en mal som ikke holder formen, avvises her (`invalid-job`), så ikke en jobb du har godkjent, nektes av en grunn saken ikke viste. Agenten har ikke sin egen kopi av køens tillatt-liste. Køen håndhever sin egen når jobben kjøres, og et steg køen nekter, gir utfallet `refused` og en sak.
5. **Tidsgrense.** Høyst 900 sekunder for et fast program.
6. **Tak.** Det kan være høyst ti jobber som venter på godkjenning eller er aktive.
7. **Teksten saken skal vise** lages (under). Kan jobben ikke vises i sin helhet, avvises den med `cannot-be-shown`.
8. **Skriving.** Jobbmalen først og `spec`-fila sist, begge byttet på plass. En eldre `approval`-fil for samme id fjernes.

`requestedBy` settes av agenten. MCP-serveren leser navnet klientprogrammet oppgir i `initialize` (`clientInfo.name`): inneholder det «claude», blir det «Claude»; inneholder det «codex», blir det «Codex»; ellers «En assistent». Navnet velges av programmet som kobler seg til, ikke i verktøykallet. Det er til opplysning og avgjør ingenting. Serveren leser ikke `clientInfo` i dag (`HavenAgentDMCPMain.swift`), så dette er ny kode, og de faktiske navnene måles i T6. «En assistent» er det lengste navnet agenten bruker, og det må forbli det lengste: med en tittel på 40 tegn blir godkjenningstittelen da nøyaktig 80 tegn, som er grensen.

Jobben bærer bare `kind` og `id` for et fast program. Argumentene står i policyen, og de kan ikke overstyres.

## Tidspunktene for en jobb

| Slag | Tidspunkter | Passering |
|---|---|---|
| `cron` | etter `trinn3-cron.md`, fra godkjenningen (eller `notBefore`) til `endsAt` | som for faste hendelser |
| `interval` | godkjenningstidspunktet (eller `notBefore`) pluss `everySeconds`, og så videre i et fast rutenett. Rutenettet flytter seg ikke om en kjøring blir forsinket. | tidspunkt i rutenettet som passerte, telles |
| `once` | `at` | Godkjennes jobben etter `at`, kjøres den ikke. Sov Macen over `at`, kjøres jobben ved oppvåkning hvis det er før `endsAt`. |

Ingenting kjøres på etterskudd for tiden før godkjenningen.

## Godkjenningen

- **Sjekksummen.** `specDigest` er `sha256:` og SHA-256 av bytene i `<id>.spec.json`. Jobbmalens sjekksum står inne i `spec`-fila, så den er med.
- **Saken er bundet til sjekksummen.** Sakens id er `job:scheduled:<id>:approval:<de tolv første tegnene i sjekksummen>`. Endres bestillingen etter at saken ble vist, får den en ny id og vises på nytt som en ny sak.
- **Svaret kontrolleres mot fila slik den ligger nå.** `ScheduledJobApprovalService.decide` leser `spec`-fila, regner sjekksummen og krever at den begynner med de tolv tegnene i saken. Stemmer det ikke, skrives ingenting, og svaret blir `accepted: false` med teksten «Jobben er endret etter at saken ble laget. Se den nye saken.»
- **Én funksjon, to innganger.** Menylinjen når den gjennom `POST /challenges/respond` (grenen `job:` i `AgentChallengeWiring.responseHandler`). Kommandolinjen når den med `haven-agentd schedule-approve --id <id> --digest <tolv tegn>`. Det er samme regel som for fjernintenter: flaten har ingen egen, kortere vei.
- **Ingen MCP-verktøy godkjenner.** `agent.schedule.*` har ikke noe slikt verktøy. `agent.review.approve` går til `ReviewCommandService` og kjenner bare fjernintenter. T5 prøver begge.
- **En bestilling som ingen svarer på, utløper.** Ved `endsAt`, og for `once` ved `at`, forsvinner saken, og jobben får status `ended`. Til da teller den mot taket på ti.

## Når arbeideren kjører en jobb

Alle disse må holde, og de kontrolleres ved hver runde, ikke bare når jobben ble bedt om:

1. `spec`-fila kan leses og følger skjemaet.
2. `approval`-fila finnes, har `decision: approved`, og `specDigest` er lik sjekksummen av `spec`-fila nå.
3. Styringen er `active` (eller fila mangler).
4. Nå er etter `notBefore` og før `endsAt`.
5. Handlingen finnes fortsatt: programmet står i policyen, eller køen er navngitt i `config.json` og jobbmalens sjekksum stemmer.
6. Et planlagt tidspunkt er passert siden `lastOccurrence`, og siden jobben sist ble startet igjen etter en pause (se styringen).

Feiler 1 eller 5, får jobben `attention.kind: invalid`, og det blir en sak. Feiler 2, 3 eller 4, skjer ingenting: jobben venter, er satt på pause, eller er ferdig.

## De to handlingene

**`localTask`.** Arbeideren kjører det faste programmet gjennom `LocalTaskRunner`, slik den gjør for hendelsene i `config.json`, med tidsgrensen og loggfila fra trinn 3.

**`spoolJob`.** Arbeideren kopierer jobbmalen til `<spoolInbox>/<id>-<tidspunkt>.json`, via `.partial` og omdøping, slik køen krever. `<tidspunkt>` skrives `20261014T000000Z`. Køen tar bare filnavn av bokstaver, sifre, punktum, strek og understrek (`agent_job_runner.py` linje 40); et tidspunkt med kolon ville blitt liggende urørt. Deretter er kjøringen «lagt i kø», og arbeideren går videre. Ved hver senere runde ser den etter `<spoolOutbox>/<id>-<tidspunkt>.result.json`. Status `ok` gir utfallet `ok`. `refused` gir `refused`. Alt annet gir `failed`. Arbeideren venter altså aldri på køen, og køen eier sine egne tidsgrenser.

**En køfil som ikke er tatt, trekkes tilbake.** Køen tar en jobb ved å flytte fila ut av `inbox/`. Står køen, blir fila liggende, og den ville blitt kjørt når køen kom tilbake, kanskje dager senere. Arbeideren sletter derfor fila fra `inbox/` når den fortsatt ligger der og ett av dette skjer: resultatet har ikke kommet innen `timeoutSeconds` (utfallet blir `no-result`), jobben settes på pause eller stoppes, `endsAt` passeres, eller godkjenningen ikke lenger gjelder. Lykkes slettingen, ble jobben aldri tatt. Da er utfallet `no-result` når fristen gikk ut, og ellers `withdrawn`. Finnes ikke fila, er den tatt, og resultatet føres når det kommer.

`scheduledJobs.spoolInbox` og `scheduledJobs.spoolOutbox` er nye, valgfrie nøkler i `config.json`. Uten dem avvises køjobber når de bes om. En eldre agent ser bort fra nøklene når den leser.

## Styring: pause, fortsett, stopp

`ScheduledJobControlService.set` skriver `<id>.control.json` under samme lås som bestillingene.

| Fra | `pause` | `resume` | `stop` |
|---|---|---|---|
| `active` | `paused` | — | `stopped` |
| `paused` | — | `active` | `stopped` |
| `stopped` | avvises | avvises | — |

- **Jobber som er bedt om**, kan styres gjennom MCP, kommandolinjen og kontrollbroen. `stopped` er endelig: jobben må bestilles og godkjennes på nytt for å gå igjen.
- **Faste hendelser i `config.json`** kan settes på pause og startes igjen fra kontrollbroen (menylinjen) og kommandolinjen. De kan ikke stoppes for godt herfra; de tas ut med installasjonsskriptet. **MCP-verktøyene styrer ikke faste hendelser.** En assistent skal ikke kunne slå av sjekken som sier fra om ulest post. Dette er en innsnevring av F4 som Kjetil tar stilling til i G2.
- `resume` godkjenner ingenting. En jobb som aldri ble godkjent, står og venter.
- **`resume` henter ikke inn pausen.** Arbeideren regner planlagte tidspunkt etter det seneste av `lastOccurrence` og `changedAt` i styringsfila når tilstanden er `active`. Det som passerte under pausen, kjøres ikke og telles ikke. Første kjøring etter `resume` er neste planlagte tidspunkt. Styringsfila skrives fortsatt bare av styringstjenesten, og kjøretilstanden bare av arbeideren.
- Det samme gjelder faste hendelser. En fast hendelse på intervall uten cron har ikke noe rutenett: den kjøres ved første runde etter `resume`, og forsinkelsen regnes fra `resume`, ikke fra tidspunktet som sto fra før pausen.

## Sakene under kilden `job`

`saker-job.example.json` har ett eksempel av hver, gyldig etter `agent-challenge-v1`. Menyappen som er installert i dag, viser og besvarer dem uten endring.

| Sak | `id` | Tittel | Svar |
|---|---|---|---|
| Venter på godkjenning | `job:scheduled:<id>:approval:<tolv tegn>` | «`<Hvem>` ber om en planlagt jobb: «`<tittel>`»» | «Godkjenn» (`approve`), «Avvis» (`reject`), «Åpne» |
| Feilet, passert eller ugyldig | `job:scheduled:<id>:attention` | «Planlagt jobb feilet: `<tittel>`», «Planlagt jobb ble passert: `<tittel>`» eller «Planlagt jobb kan ikke kjøres: `<tittel>`» | «Kvitter» (`approve`) og «Åpne». En jobb som er bedt om, har også «Stopp jobben» (`reject`). |
| Planleggeren går ikke | `job:scheduler:stopped` | «Planleggeren går ikke» | «Åpne», «Ignorer i dag» |

- **Én sak per jobb.** Feiler jobben igjen før saken er kvittert, er det samme sak med ny tekst, og det kommer ikke nytt varsel. Feil går foran passering.
- **Passering gir sak bare for jobber og hendelser som går én gang i døgnet eller sjeldnere** (`trinn3-cron.md`). For de som går oftere, står antallet i lista «Planlagte jobber».
- **«Kvitter»** skriver `ack`-fila med tidspunktet saken gjaldt. Saken vises igjen bare når et nyere tidspunkt feiler eller passeres. **«Stopp jobben»** står bare på saker om jobber som er bedt om. Den setter styringen til `stopped` og kvitterer.
- **Saker om faste hendelser har bare «Kvitter» og «Åpne».** En fast hendelse kan ikke stoppes herfra, og en knapp som heter stopp, skal ikke sette på pause. Pause og fortsett for faste hendelser står ett sted: i lista «Planlagte jobber» fra trinn 5, og på kommandolinjen. Sakene er derfor like i trinn 4 og 5, og agenten trenger ikke vite hvilken menyapp som er installert.
- **Et svar saken ikke tilbyr, gjør ingenting.** Kontrollbroen tar imot hvilken som helst svar-id (`AgentControlBridgeServer.swift` linje 137–145). Står svaret ikke blant sakens `responses`, for eksempel `reject` på en sak om en fast hendelse, er svaret `accepted: false`, og ingenting skrives.
- **Titler over 80 tegn avkortes.** Agenten kutter tittelen til 79 tegn og setter «…» til slutt, slik den gjør for post (`CorrespondenceWaiting.swift` linje 105–110). Én for lang tittel ville gjort hele innboksen uleselig (`AgentControlBridgeServer.swift` linje 109–124). Det gjelder faste hendelser uten `title`, der id-en vises: id-er i `config.json` har ingen lengderegel.
- **«Åpne»** åpner adminvinduet, der detaljteksten står. Sakene har `handleAt.venue: admin-window`, så knappen gjør det samme fra menyen, fra adminvinduet og fra et varsel.
- **Faste hendelser** fra `config.json` får samme slags sak når de feiler, og når de passeres og går én gang i døgnet eller sjeldnere. Kvitteringen og styringen deres ligger i samme mappe, under hendelsens id. Agenten leser derfor `State/scheduled-events.json` fra dette trinnet.

### Hva du ser før du trykker

Menyen viser tittelen og én linje under: hvem som ber, kilden og «Gjelder». Detaljteksten vises bare i adminvinduet (`MenuPresentation.swift` linje 178–184, `HavenAgentMenuApp.swift` linje 76–91). Den som ber om en jobb, skriver bare tittelen (høyst 40 tegn), og den står i anførselstegn i saken. Alt annet lager agenten fra `spec`-fila, og det er det samme som kjøres:

- **«Gjelder»** (`subject`, i menyen): hva som kjøres i kortform, tidsplanen og sluttdatoen.
  - Fast program: «fast program korrespondanse-sjekk · hverdager kl. 02:00 · til 11.11.»
  - Køjobb: programmet og underkommandoen i hvert steg, «køjobb: git fetch, swift test · hverdager kl. 02:00 · til 11.11.»
- **Detalj** (i adminvinduet): hva som kjøres i sin helhet, tidsplanen med tidssone, første tidspunkt, sluttdato og tidsgrense. For et fast program: beskrivelsen fra policyen og id-en. For en køjobb: mappen, hvert steg slik det står i malen, og `env` når malen har det.
- **Tidsplanen i klartekst.** Agenten kjenner igjen noen vanlige former: «hver dag kl. 09:00», «hverdager kl. 02:00», «mandager kl. 07:30», «hver time», «hvert 15. minutt», «den 1. i måneden kl. 06:00». Alt annet vises som uttrykket selv, med tidssonen. Første tidspunkt står alltid med dato og klokkeslett i detaljen.

En jobb avvises med `cannot-be-shown` når «Gjelder» blir over 200 tegn eller detaljen over 400, når tittelen, «Gjelder» eller detaljen inneholder noe som likner en hemmelighet, eller når et steg i en køjobb ikke kan gjengis ordrett. Det som ikke kan vises, kan ikke godkjennes. Kontrakten er her strengere enn koden: agenten kontrollerer ikke «Gjelder» mot hemmelighetsregelen i dag (`AgentChallenge.swift` linje 262–285).

Du kan altså godkjenne fra menyen og se hvem som ber, tittelen de skrev, og agentens kortform av hva som kjøres og når. Hele jobben, med hvert steg ordrett, står i adminvinduet.

## Leverandøren for kilden `job`

- Leverandøren leser bare toppnivået i mappen, ikke `Removed/`.
- Kan mappen leses og alle filene tolkes, er kilden `read`, også når det ikke finnes noen jobber.
- Kan mappen ikke listes, eller en `approval`-, `ack`-, `control`- eller `runtime`-fil ikke tolkes, er kilden `unreadable` med en grunn på høyst 200 tegn. Da lager innboksen som i dag saken «Får ikke lest job». En `spec`-fil som ikke kan tolkes, gjør ikke kilden ulesbar: den jobben blir en sak for seg («kan ikke kjøres»), så én ødelagt bestilling ikke skjuler de andre.
- **«Planleggeren går ikke».** Saken lages når `worker.json` er eldre enn 180 sekunder, det finnes minst én aktiv hendelse eller jobb, og tilstanden har vart i minst 120 sekunder mens Macen har vært våken (målt med en klokke som står stille under søvn). Uten den siste regelen ville saken kommet hver gang Macen våkner, i sekundene før arbeideren har skrevet nytt livstegn.

## Det godkjenningen ikke stopper

Dette står også i `Docs/SecurityModel.md` når trinnet bygges (AP14), og i `PLAN.md`.

- **Køene.** Kode som kjører som Kjetil, kan skrive `approval`-fila selv, eller endre `config.json`. En assistent kan få slik kode kjørt gjennom `.agent-spool` og `_losen-queue`.
- **Kontrollbroen.** Agenten kan ikke skille menylinjen fra et annet program som har tokenet.
- **Faste programmer kan alt kjøres med en gang gjennom MCP.** `agent.jobs.register` tar imot `onComplete.actions` som peker på handlinger i policyen, og `agent.jobs.complete` gjør jobben ferdig. Da kjører agenten handlingene (`JobCompletionService.dispatchActions`), uten at noen har trykket. Det er slik AgentJobs er laget, og AgentJobs er slått på i konfigurasjonen som er installert. Trykket for planlagte jobber stopper derfor ikke at et fast program kjøres én gang nå. Det stopper at noe settes til å gå igjen og igjen uten at du har sett det, og det stopper køjobber.

## Tester

T4, T5, T6 og T7. Hva hver av dem prøver, står i `../FORMAALSSPEC.md` §5, som er den ene lista over tester.
