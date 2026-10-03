# Fabel, runde 3: uavhengig gransking av «planlagte jobber i HavenAgentD»

Gransket 02.10.2026 av en uavhengig Claude-tråd («Fabel») mot `panel/BRIEF_RUNDE3.md`. Teksten under er Fabels svar, uendret.

---

# Fabel, runde 3: uavhengig gransking av «planlagte jobber i HavenAgentD»

Gransket 02.10.2026 mot `panel/BRIEF_RUNDE3.md`. Stier under `Sources/`, `Docs/`, `Scripts/`, `Launchd/`, `Tests/` er relative til `HavenAgentD/.worktrees/main-20260922/`. Jobbloggene refereres som `job-245`, `job-246`, `job-247`, `job-2425` med linjenummer i loggfila. Ikke tilgjengelig, og derfor alltid `[ikke belagt]`: `CorrespondenceWaiting.swift`, `AgentControlBridgeServer.swift`, korrespondanseklientens kilde, planleggerens plist, `Contracts/agent-challenge-v1.schema.json`, `images/plan-oversikt-v2.png`, og GitHub-tilstanden (grener, PR #25).

---

## P1. De åtte punktene

**Konklusjon:** Tre av åtte er løst i planen (2, 3, 4), to er delvis løst (6, 8), og tre er flyttet eller borte uten å være løst (1, 5, 7); tabellen «Det runde 2 fant, og hvor det ble av» overdriver på punkt 1, 5, 7 og 8c.

**1. Løper og program ut av Claude-skrivbar mappe, hash pinnet, eier/symlenke/`.ready`-sjekk.** Løperen legges ned og F8/F9-programmene legges i `bin/` `[belagt: PLAN.md:25, 43]`. Men: (a) hash-pinning er borte uten begrunnelse — `LocalTaskDefinition` har fortsatt bare sti og argumenter `[belagt: AutomationPolicy.swift:112-132]`, og AP8 nevner bare type og ID `[belagt: PLAN.md:64]`. (b) «der bare installasjonsskriptet skriver» er en konvensjon, ikke en egenskap ved mappen: installasjonsskriptet kjøres selv som `skript`-jobb fra `_losen-queue` `[belagt: PLAN.md:71]`, som kjører enhver `.sh` Losen legger under `HAVEN-Deploy/_handoff/` `[belagt: job-246:36-47, 322-337]`. (c) Problemet flyttet inn i `.agent-spool`: tillatt-lista inneholder `scripts/run_swift_bounded.sh` som løses relativt til jobbens egen `cwd` `[belagt: job-246:378-381, 448-449]`, og `cwd` kan være hvilken som helst mappe under HAVEN `[belagt: job-245:241-249]`. Det er nøyaktig «program i mappe Losen skriver i», bare i en annen kø. Status: **flyttet, ikke løst**.

**2. Én skriver per fil, låsfil, idempotens per forekomst, ingen running→scheduled-reset fra ikke-arbeidere.** AP6 lister spec/runtime-splitt, låsfil, «hver forekomst kjøres høyst én gang», avbrutt kjøring blir sak `[belagt: PLAN.md:62]`; T2/T3 dekker det `[belagt: FORMAALSSPEC.md:133-134]`. Resetten i `start` for ikke-arbeidere `[belagt: ScheduledEventService.swift:161-165]` er ikke nevnt eksplisitt, men følger av splitten. Status: **løst i plan, fra trinn 3**. Merk at trinn 1–2 kjører på dagens kode med alle kappløpene.

**3. Sommertid som instanter, avgrenset søk, validering.** AP5 og T1 krever akkurat instantene runde 2 ba om `[belagt: PLAN.md:61; FORMAALSSPEC.md:132]`. Status: **løst i plan**.

**4. Rør → loggfil, tidsgrense, tester for barnebarn og >64 KiB.** AP6 og T2 `[belagt: PLAN.md:62; FORMAALSSPEC.md:133]`. Status: **løst i plan, fra trinn 3**. Men F2 sier «hver jobb har en tidsgrense» `[belagt: FORMAALSSPEC.md:54]` — det er usant i trinn 1–2, der programmene kjører uten tidsgrense `[belagt: SubprocessRunner.swift:51-79; LocalTaskRunner.swift:10-24]`.

**5. Dynamiske handlinger = {kind, id}; avgjør opprinnelse.** Første halvdel i AP8 `[belagt: PLAN.md:64]`. Opprinnelse: ingen setning i spesifikasjon eller plan. Alt planleggeren kjører har `origin: .local` `[belagt: ScheduledEventService.swift:280, 285]`, og `.local` hopper over `allowedForRemoteExecution` `[belagt: AutomationPolicy.swift:161-162, 180-182]`. En jobb Losen oppretter fra skyen via MCP får dermed mer enn en signert fjernintent. Status: **halvt borte uten å være løst**.

**6. Planleggerens plist i repo og installskript; målinger før F7 påstås.** `Launchd/` har fortsatt bare `io.digipomps.haven.agentd.plist` (filliste). Planen sier «Plisten legges i repoet i AP7» `[belagt: PLAN.md:92]`, men `install-agent-dev.sh` krever at plisten alt ligger i `~/Library/LaunchAgents` og installerer den ikke `[belagt: Scripts/install-agent-dev.sh:121-122]`. Målingene (miljø, ssh, gh, nøkkelring) er erstattet med én jobb (`gh api user`, `git status`) i T0 `[belagt: PLAN.md:56]` — og løperens PATH er launchd-standard uten `/opt/homebrew/bin` `[belagt: job-2425:8-22 har ingen EnvironmentVariables; sammenlign dispatch job-2425:40-42]`, så `gh` kan mangle. Status: **delvis**.

**7. Kontrakt, fixtures og menyapp sammen; kvittering; én sak per jobb.** Kilden `job` finnes `[belagt: AgentChallenge.swift:21-23]`, så kilde-enumen er trygg. Men AP11 lover «Stopp jobben» som svar `[belagt: PLAN.md:67]`, og `AgentChallengeResponseID` er en lukket enum med fire verdier `[belagt: AgentChallenge.swift:83-88]`. En ny verdi gjør at en eldre menyapp dekoder hele innboksen som `malformed` `[belagt: AgentBridgeClient.swift:138-142; MenuPresentation.swift:98-103]` — samme klasse som HD-0074 `[belagt: job-247:40-41]`. «Kontrakten endres ikke» `[belagt: PLAN.md:93]` holder derfor ikke. Hvor «Kvitter» lagres, sies ikke; dagens `dismissToday` er bare i flaten og utløper med døgnet `[belagt: AgentMenuModel.swift:113-117; AgentChallengeWiring.swift:227-233]`. Status: **delvis; påstanden om uendret kontrakt er feil**.

**8. F8/F9 får komponent, F4 innsnevres, F5 får fotnote.** F8/F9 har komponenter (trinn 1–2) og F4 er innsnevret (E3) `[belagt: FORMAALSSPEC.md:56, 72-73]`. Fotnoten på F5 ble ikke lagt til, men fjernet gjennom omformulering (E2) med begrunnelsen at køen har tillatt-liste `[belagt: FORMAALSSPEC.md:71]`. Se P3: tillatt-lista er ikke en vegg, og planen sier det selv to avsnitt senere `[belagt: PLAN.md:16]`. Status: **8c borte uten å være løst**.

Fra «Bør endres»: `requiresUserSession` er fortsatt bare deklarert `[belagt: AutomationPolicy.swift:117, 219-230]`, og dagens eneste localTask har `requiresUserSession: true` `[belagt: job-2425:133]`; søvn/`pmset` er ikke nevnt noe sted i runde 3.

---

## P2. Trinn 1 og 2 på planleggeren som kjører i dag

**Konklusjon:** «Uten ny agent» er sann som mekanisme, men da bærer programmene alene hele ansvaret for at planleggeren ikke henger, en feil i konfigurasjonen gir en krasjløkke som `validate-config` ikke fanger, og en død sjekk er usynlig i menyen til trinn 5.

**Hva som kan gå galt, konkret**

1. **Rørene.** Utdata leses først etter avslutning, uten tidsgrense `[belagt: SubprocessRunner.swift:61-63]`. Programmet starter en korrespondanseklient som barneprosess `[belagt: PLAN.md:58]`. Arver klienten fd 1/2 og lever videre (nettverkshang, glemt `kill` på feilveien), kommer EOF aldri; `runEvent` står i `running` for alltid `[belagt: ScheduledEventService.swift:233-238]`, og neste runde kommer ikke fordi hendelsene kjøres i rekkefølge `[belagt: 224-226]`. Da stopper også fristvarselet. Et barn som skriver mer enn rørbufferen (gjelder også stderr: Python-tracebacks) blokkerer på samme måte; `prefix(4_000)` skjer etter lesing `[belagt: 240]`.

2. **Krasjløkke ved konfigurasjonsfeil.** `schedule-worker` kaller `start`, som kjører `validate` `[belagt: HavenAgentMain.swift:342-345; ScheduledEventService.swift:152, 297-309]`. Ugyldig `firstFireAt` eller manglende `intervalSeconds` kaster, prosessen dør, `KeepAlive` starter den igjen `[belagt: job-2425:25-34]`. AP3 validerer kopien med `haven-agentd validate-config` `[belagt: PLAN.md:59]`, men den kommandoen bare dekoder JSON `[belagt: HavenAgentMain.swift:163-168; AgentRuntime.swift:300-302]`. `schedule-list --config <kopi>` kjører derimot `validate` uten å skrive `[belagt: HavenAgentMain.swift:357-362]`. Ukjent handlings-ID oppdages uansett først ved kjøring `[belagt: LocalTaskRunner.swift:11]`, og synes da bare i `lastError` i en fil ingen flate leser.

3. **Omstart av tjenesten.** SIGTERM → `stop()` avbryter løkken, men ikke barneprosessen; `stop` venter på `runEvent` `[belagt: ScheduledEventService.swift:185-190; HavenAgentMain.swift:347-348, 1166-1186]`. Dreper launchd prosessen (`ExitTimeOut`, `[ikke belagt]`), står posten i `running`; neste start setter den til `scheduled` med gammel `nextFireAt` og kjører straks igjen `[belagt: 161-165, 216-223]`, mens det foreldreløse barnet fortsatt kjører. To sjekker skriver da samme markører samtidig. Idempotens og atomisk skriving (tmp + rename) i programmet er nødvendig, ikke valgfritt.

4. **Søvn.** Løkken sover 1 s mellom runder `[belagt: 173-182]`; etter oppvåkning kjøres forfalte hendelser én gang og neste tidspunkt blir «nå + intervall» `[belagt: 271-274]`. Det er dagens oppførsel og greit for F8/F9, men intervallet driver med kjøretiden, og døgnhendelsen glir over sommertidsskiftet (planen vet det `[belagt: PLAN.md:48]`).

5. **Konfigurasjon endret mens arbeideren kjører.** Ingenting skjer: definisjonene leses bare i `start` `[belagt: 146-167]`; løkken leser tilstandsfila på nytt hvert sekund `[belagt: 213-215]`, men den inneholder de gamle definisjonene. Nye hendelser krever omstart, som AP3 gjør. Omstarten fører til punkt 3.

6. **Miljø.** PATH er `/usr/bin:/bin:/usr/sbin:/sbin`, cwd er `/`, bare `SSH_AUTH_SOCK` arves `[belagt: job-2425:170-176]`. `/usr/bin/python3` er Apples CLT-stubb; versjonen følger Xcode CLT `[ikke belagt hvilken]`. Alt i programmet må være absolutte stier, inkludert korrespondanseklientens binær. Hvor den ligger er `[ikke belagt]`; ligger den i et `.build/` i et arbeidstre, er «fast program» tomt igjen (P1-1).

**Hva programmene må garantere**

- Avslutter alltid innen en egen grense (alarm + `os._exit`), også når klienten henger på nett.
- Barn startes med `stdin=DEVNULL`, `stdout`/`stderr` til rør eller fil — aldri arvet — i egen prosessgruppe, og hele gruppen drepes i `finally`.
- Under 64 KiB på stdout og stderr hver (AP2 lover 1 KiB stdout `[belagt: PLAN.md:58]`, sier ingenting om stderr).
- Ingen dialoger: nøkkelring, TCC, CLT-installasjon. §2 krever «uten dialog» `[belagt: FORMAALSSPEC.md:98]`, men T0 må kjøre `/usr/bin/python3 --version` og klienten *fra planleggeren*, ikke fra Terminal.
- Markøren skrives atomisk før prosessen avslutter, på alle veier; en halvskrevet fil gjør hele kilden `unreadable` `[belagt: AgentChallengeWiring.swift:128-134]`.
- Låsfil per program, siden punkt 3 gir to instanser.

**Er «uten ny agent» holdbar?** Ja for mekanismen. Nei for løftene: F2s tidsgrense og F6s «tom liste betyr ikke ro» leveres ikke i trinn 1–2. En død planlegger gir ingen nye markører; gamle står og ser ferske ut, og ingen markør leses som `read` med null saker → «Ingenting venter» `[belagt: ChallengeInboxService.swift:59-67; MenuPresentation.swift:131-144]`. Planen må si det i «Det du ser» for trinn 1, og T8 må måle hva menyen viser 30+ minutter etter at planleggeren er stoppet.

---

## P3. Køjobber (`spoolJob`)

**Konklusjon:** En jobb som slipper gjennom tillatt-lista kan kjøre vilkårlig kode som Kjetil på minst tre måter, sikkerhetsavsnittet er ærlig i ånd men utelater den mest direkte, og F5s overskrift «ingen nye rettigheter» er sann bare hvis «rettighet» betyr «identitet og liste» — planen sier selv at det nye er tid.

**Hva som slipper gjennom**

1. **Relativ skriptsti.** `scripts/run_swift_bounded.sh` står på lista og løses mot jobbens `cwd` `[belagt: job-245:175; job-246:378-381, 448-449]`. `cwd` kan være enhver mappe under HAVEN `[belagt: job-245:241-249]`. Den som kan skrive `tmp/x/scripts/run_swift_bounded.sh` (alle tråder med mappen koblet til), kjører hva som helst. README sier «no quoting or injection surface» `[belagt: job-245:62-63]`; det gjelder sitering, ikke dette.
2. **`swift build|test|package`.** Sjekken ser bare på `cmd[1]` `[belagt: job-246:264-267 via job-245:257-267]`. Tester og `Package.swift` kjører vilkårlig kode; `swift package <alt>` passerer.
3. **`gh api`.** Vilkårlig REST/GraphQL som Kjetil. `PUT /repos/…/pulls/N/merge` merger en PR selv om `gh pr merge` er nektet `[belagt: FORBIDDEN_FLAGS job-245:199-203]`. README: «Merging a pull request is deliberately not delegable» `[belagt: job-245:82]` — det er ikke sant i virkning. KOORDINERING sier merge er Kjetils avgjørelse `[belagt: job-246:211]`.
4. **`git`.** Bare `cmd[1]` og noen flagg sjekkes `[belagt: job-245:177-181, 192-198]`. `git remote add` + `git push` til fremmed fjernlager passerer. `git fetch --upload-pack=<kommando>` passerer flaggsjekken; om det kjører lokalt er ikke målt her.
5. **Vernet av primærsjekkouter** gjelder bare når `cwd` er nøyaktig rotmappen `[belagt: job-246:370-376]`; en undermappe omgår det.
6. **`.py`-skriptene** løses fra HAVEN-roten `[belagt: job-246:383-386, 450-451]`, men ligger i repoer Losen skriver i. Samme svakhet som P1-1.

**Er sikkerhetsavsnittet ærlig?** Delvis. «En test kan kjøre hvilken som helst kode, og `gh api` kan gjøre det meste `gh` kan» `[belagt: PLAN.md:16]` er sant og godt sagt. Men «trygge `git`-kommandoer» `[belagt: PLAN.md:14]` er for snilt, punkt 1 og merge-omgåelsen er ikke nevnt, og avsnittet sier ikke at `install-scheduled-tasks.sh` — som endrer `config.json`, agentens policy — selv kjøres fra en kø som kjører enhver `.sh` Losen legger under `_handoff/` `[belagt: PLAN.md:71; job-246:36-47]`. `SecurityModel.md` krever at `config.json` bare skrives fra «a trusted local admin workflow» `[belagt: Docs/SecurityModel.md:331-339]`. Dermed er «Punkt 2 er avslått til du slår det på» `[belagt: PLAN.md:20]` en port Losen selv kan åpne. Porten er bare reell hvis Kjetils ja er påkrevd per konfigurasjonsendring, og det må stå.

**Er F5 sann?** Mekanismesetningen («to ting») er sann. Overskriften er ikke det Kjetil vil lese ut av den. Planens egen tekst `[belagt: PLAN.md:18]`: det nye er at Losen kan sette noe til å skje i natt, hver natt, uten økt — og etter prompt-injeksjon. En tryggere form som gjør F5 sann: jobbmalene (AP9) ligger i `automationPolicy` og godkjennes av Kjetil som enhver annen handling; MCP kan bare planlegge maler som finnes. Da er `spoolJob` en navngitt handling, ikke en kanal for maler Losen skriver selv. Hvor malene lagres står ikke i planen `[belagt: PLAN.md:65]`.

**Stille forutsetning:** §2 sier `.agent-tools/agent_job_runner.py` eies av andre tråder og ikke endres `[belagt: FORMAALSSPEC.md:82]`. Eierskapet er `[ikke belagt]` i loggene. Hullene over kan da ikke lukkes av denne PDD-en, og det må sies til Kjetil at tillatt-lista forblir som den er.

---

## P4. Korrespondansesjekken (F8)

**Konklusjon:** Programmet gjør noe annet enn det Kjetil valgte 10.09 — det markerer all ukvittert post, ikke det som krever ham — og i trinn 1–2 er en død sjekk usynlig; markørens innhold kan dessuten slå ut hele menyen.

**Er det samme ting?** Nei. Valget (husket, ikke målt `[belagt: FORMAALSSPEC.md:39]`) var: daemonen poller, *Losen markerer* hva som krever svar. Kilden er bygget for akkurat det: «viser bare det Losen har vurdert at krever mennesket» `[belagt: AgentChallengeWiring.swift:116-118]`. Programmet skriver markør for alt ukvittert `[belagt: PLAN.md:47, 58]`, uten vurdering. Følger: (a) når Losen ikke kjører — mesteparten av tiden — blir hver melding en sak for Kjetil, også de Losen ville ordnet selv; (b) når Losen kjører, kvitterer Losen uten å spørre (prosjektminnet `[belagt: E-prosjektminne:4]`), og programmets markør forsvinner neste runde, også om meldingen krevde Kjetil. Da er programmets markør støy når Losen er borte og borte når den trengs. Det eneste som da bærer «krever Kjetil», er en markør Losen eventuelt skriver — og det verktøyet finnes ikke `[belagt: E-prosjektminne:12]`.

En ærlig omforming: programmets markør betyr «N uleste meldinger venter på Losen» (kjernen i HD-0069 `[belagt: job-247:36]`), med `handleAt: .assistant` `[belagt: AgentChallenge.swift:53-54]`, og sier aldri «venter på svar». Losens egne markører betyr «krever deg». To betydninger, to titler.

**Når programmet feiler stille.** AP2 skriver «kunne ikke leses» ved feil `[belagt: PLAN.md:58]` — bra, men bare når programmet kjører. Kjører det ikke (hengt planlegger, krasjløkke, Mac av, CLT-dialog), skrives ingenting: gamle markører ser ferske ut, ingen markør gir `read` med null saker, menyen sier «Ingenting venter» `[belagt: ChallengeInboxService.swift:59-67; AgentChallengeWiring.swift:128-131; MenuPresentation.swift:131-144]`. Ingen «sist sjekket» finnes i kontrakten (`[ikke belagt]`: `CorrespondenceWaiting.swift`), og trinn 1–2 forbyr daemonendringer. Først kilden `job` i trinn 5 kan vise «korrespondanse-sjekk: siste kjøring 3 t siden». Planen må si at en død sjekk er usynlig til da, og T8 må måle det.

**Er «leser ikke meldingsinnhold» nok?** Ikke alene. Markøren bærer `from` `[belagt: E-prosjektminne:12]`, og tittelen bygges av den («Post fra … venter på svar»). Menyappen validerer hele innboksen `[belagt: AgentBridgeClient.swift:138-142]`: tittel over 80 tegn, detalj over 400, eller en streng på 24+ tegn med bokstaver og sifre `[belagt: AgentChallenge.swift:154-184, 238-261]` gjør **hele** svaret `malformed` og skjuler alle andre saker. En DID, principal-ID eller meldings-ID i `from` eller `summary` slår altså ut menyen. Programmet må skrive visningsnavn, aldri ID-er, og stabil `id` per profil (ny `id` per telling gir nytt varsel hver gang `[belagt: AgentMenuModel.swift:75-91]`). Om `correspondence_list_inbox` endrer kvitteringsstatus på serveren er `[ikke belagt]` og må måles i T0.

**Kjetil, ikke Losen, må avgjøre**

1. Hva daemonens markør betyr: «ulest, venter på Losen» eller «krever meg».
2. Om Losen fortsatt skal kvittere automatisk når en daemon-markør finnes.
3. Om avsenders navn skal stå i menylinjen (andre kan se skjermen).
4. Bekrefte valget fra 10.09 på nytt — det er `husket`, og det gir agenten tilgang til korrespondansenøklene.
5. Hvert 30. minutt, og varselsamtykket HD-0069 krever `[belagt: job-247:37]`.

---

## P5. Formål og tester

**Konklusjon:** F2, F6, F7 og F8 har ingen test som måler kjernen i formålet, T6 og T7 måler noe smalere enn de sier, og T0 mangler akkurat den målingen som avgjør om trinn 3 kan bygges.

**Formål uten test som måler formålet**

- **F2** «går igjen når Kjetil har logget inn etter en omstart» `[belagt: FORMAALSSPEC.md:54]`. T6 måler «omstart av tjenesten» `[belagt: 137]`, T2 måler at tilstanden overlever stopp/start `[belagt: 133]`. Ingen test måler omstart av Macen med innlogging. Plisten er ikke i repoet, så ingen test kan heller sjekke `RunAtLoad`/`KeepAlive`.
- **F6** «En tom liste betyr ikke ro» `[belagt: 58]`. T7 tester «en jobb som feiler gir én sak» `[belagt: 138]`. Ingen test: arbeideren død eller tilstandsfila uleselig → kilden `job` må melde `unreadable`, ikke `read` med null saker. Det var runde 2s krav `[belagt: FABEL_SVAR.md:140]`.
- **F7** «Denne tråden bruker køene som finnes» `[belagt: 59]`. T0 kjører `gh api user` og `git status` `[belagt: PLAN.md:56]`. F7 finnes for bygg og tester av HavenAgentD; det måles ikke. Den målingen avgjør trinn 3: `swift test` i et arbeidstre gjennom køen, med diskvakten (56 GiB ledig `[belagt: job-247:131]` mot kravet ca. 57 `[belagt: job-246:230]`), `arch -arm64` `[belagt: job-246:415-420]` og uten `CLANG_MODULE_CACHE_PATH` (bare `HAVEN_*`-miljø tillates `[belagt: job-246:389-391, 423-432]`, og `Scripts/test_haven_agentd.sh` står ikke på lista).
- **F8** «sjekkes hvert 30. minutt» `[belagt: 60]`. T8 tester markørlogikk og én ekte melding `[belagt: 139]`. Ingen test av at sjekken har stoppet, eller at to kjøringer over 60 minutter faktisk skjer.
- **F9** forutsetter at utløpet kan leses lokalt uten nett `[belagt: PLAN.md:48]`. At det står i profilmappen er `[ikke belagt]`; CellScaffold-diffen viser `expiresAt` på serversiden `[belagt: korr-fornyelse-kilder.diff:77-83]`. §2 mangler denne avhengigheten.

**Tester som måler noe annet enn de sier**

- **T6** heter «Live på Macen» og «planleggeren kjører etter omstart» — det er en tjenesteomstart, ikke F2.
- **T7** «den kan kvitteres» — kvittering finnes ikke som varig tilstand i dag `[belagt: AgentMenuModel.swift:113-117]`; testen må si hvor kvitteringen lagres og at den overlever omstart og 24 timer.
- **T4** måler «ukjent handling avvises», ikke «ingen nye rettigheter». Gi F5 den overskriften T4 beviser.
- **T0**-raden «Korrespondanseklienten kan kjøres fra planleggeren, uten dialog» `[belagt: FORMAALSSPEC.md:98]` må kjøres som planlagt hendelse, ikke fra Terminal, ellers måler den feil miljø `[belagt: job-2425:170-176]`.

**Mangler i T0–T10**

- Test at en markør med ID-liknende `from` eller lang tittel ikke gjør innboksen `malformed`.
- Test at gammel binær (tilbakerullingen `[belagt: Scripts/install-agent-dev.sh:288-295]`, eller `main` installert av Codex) dekoder ny `config.json` og ny tilstandsmappe uten å krasje.
- `install-scheduled-tasks.sh --fjern` som rundtur, og at `kickstart` under en pågående kjøring ikke gir to instanser.
- T3 bør dekke «passert» også i menyen (F3 sier «vises» `[belagt: 55]`).
- T10: `swift test --no-parallel` som skriptet `[belagt: Scripts/test_haven_agentd.sh:27]`.

---

## P6. Koordinering

**Konklusjon:** Planen siterer installasjonsregelen uten første ledd («fra `main`»), lover Kjetil «Ingenting» i trinn 3 der regelen krever merge på hans ord, og tar ikke høyde for at Losens config- og tilstandsendringer kan knekke en installasjon fra `main`.

**Installasjonsvinduet.** Regelen har fire ledd: fra merge-commiten på `main`, tom kø, linje før og etter, forrige binær klar `[belagt: job-247:113-117]`. Planen gjengir tre `[belagt: PLAN.md:63, 76]`. Det første leddet er det som binder: agenten kjører fra testflyt-grenen (husket `[belagt: FORMAALSSPEC.md:42]`), og en install fra Losens gren bryter regelen; en install fra `main` sletter testflyten `[belagt: PLAN.md:77]`. Spørsmålet stilles Kjetil (§6) — bra — men trinn 3 sier likevel «Det du gjør: Ingenting» `[belagt: PLAN.md:36]`. Merge krever Kjetils ord og en annen utfører `[belagt: job-246:211]`.

**Tom kø og egen jobb.** Installasjon skal gå som `skript`-jobb i `_losen-queue` `[belagt: PLAN.md:71]`. Da er køen per definisjon ikke tom (egen jobb i `running/`). Køtråden har alt dokumentert selvreferanse-problemet med `kickstart` fra en køjobb `[belagt: job-245:425-428]`. Regelen må leses «ingen *annen* jobb», og det må avtales i KOORDINERING.

**HD-0156 og PR #25.** Eget arbeidstre og gren oppfyller regel 3 `[belagt: job-246:232]`. Men Codex skal installere fra `main` etter merge `[belagt: job-247:110, 114]`. Hvis Losens trinn 3 har endret `config.json` til cron-felt uten `firstFireAt`, krasjer `main`-binæren ved `AgentConfig.load` — `firstFireAt` er påkrevd `[belagt: ScheduledEventService.swift:12; AgentConfig.swift:529, 533-536]` — og `config.json` deles av agentd, planlegger, menyapp og MCP `[belagt: job-2425:28-33, 60-65]`. Likeså: tilstandsmappe-splitten (AP6) gjør at en eldre binær finner gammel `scheduled-events.json` og kjører på nytt. Planen har ingen setning om bakoverkompatibilitet. Det er kollisjonen å frykte, ikke grenen.

**Diskregelen.** Regel 1 krever ca. 57 GiB `[belagt: job-246:230]`; Macen har 56 `[belagt: job-247:131]`. Planen sier bygg «følger diskregelen» `[belagt: PLAN.md:79]` uten å si at det betyr stopp i dag, og at HD-0156 bygger samme repo samtidig. 5,9 GiB `.build` i `korr-fornyelse-20260930` er frigjørbar `[belagt: job-247:132]`.

**Banene.** Ingen synlig kollisjon: a ledig (A1 på hold), b i orden, c ferdig med c1/c2 på hold, d ledig `[belagt: job-246:216-221; job-2425:157-159]`. Men «i den banen kø-tråden tildeler» `[belagt: PLAN.md:71]` skjuler at kø-tråden også heter Losen `[belagt: job-246:205, 210]`; planen bør navngi trådene.

**Det planen lar Losen gjøre som andre skal avgjøre.** (1) Endre `automationPolicy` og `scheduledEvents` i `config.json` gjennom et skript Losen skriver og køen kjører — `SecurityModel.md` kaller det admin-eid `[belagt: Docs/SecurityModel.md:331-339]`; G2-godkjenningen `[belagt: PLAN.md:41-48]` må derfor være per endring, med diff. (2) Si at HD-0069 «løses i hovedsak» `[belagt: PLAN.md:78]` — oppgaven er blokkert av to Kjetil-godkjenninger (varselsamtykke, omstart) `[belagt: job-247:36-38]`, som planen ikke ber om. (3) Tolke installasjonsregelen (skrevet for HD-0156) som generell — rimelig, men si det.

---

## P7. Rekkefølgen

**Konklusjon:** Rekkefølgen er forsvarlig bare hvis planen sier rett ut at trinn 1–2 ikke er cron, at cron tidligst kommer i trinn 3 og «tilgjengelig for agenten» i trinn 4, og hva som kan stanse begge; den korteste veien til det Kjetil ba om er 0 → 3 → 4, med F8/F9 som første ekte cron-jobber.

**Hva som ble bedt om.** «Cron-liknende funksjonalitet … i agenten eller tilgjengelig for agenten» `[belagt: FORMAALSSPEC.md:7]`. Bakgrunnen var en løper som døde `[belagt: 9]`. Trinn 0 løser bakgrunnen (F7) uten noe cron. Trinn 1–2 leverer F8/F9 — to forbrukere som ikke trenger cron; de kjører på intervall. Cron (F1–F3) er trinn 3, agentens tilgang (F4) trinn 4 `[belagt: PLAN.md:36-37]`. Kjetils bestilling oppfylles altså tidligst etter fire trinn, hvorav to ikke bidrar til den.

**Argumentet for rekkefølgen** (E4: «gir deg noe å se, krever ingen ny agent» `[belagt: FORMAALSSPEC.md:73]`) holder, med forbehold: det Kjetil ser i trinn 1 kan være feil (P4), og det kjører uten vern (P2). Argumentet er egentlig: F8/F9 er testlasten trinn 3 trenger. Det bør sies.

**Argumentet mot.** Trinn 1–2 bygger et installasjonsskript og en døgnhendelse som trinn 3 erstatter `[belagt: PLAN.md:63]`. Det er omvei målt i arbeid, ikke bare i tid. Og trinn 3 er gjerdet av tre ting planen ikke eier: disk (P6), HD-0156-vinduet, og grenspørsmålet. Blir de stående, får Kjetil to intervalljobber og ingen cron — og en plan som «er i rute».

**Kortere vei til det samme.** 0 → 3 → 4 → 1/2 → 5: F8/F9 lander på ny planlegger med tidsgrense, loggfil og `0 9 * * *` fra dag én; ingen midlertidig installasjon; T8/T9 måles én gang. Kostnad: Kjetil ser ingenting før trinn 3 er installert. Korteste tekniske vei til «cron tilgjengelig for agenten» er ellers launchd `StartCalendarInterval`-plister lagt inn som `skript`-jobber — null agentkode, men utenfor policy og meny, så F5/F6 faller. Som i runde 2: nevnt for ærlighet, ikke anbefalt.

**Min vurdering.** Behold 1–2 først bare hvis (a) P4-betydningen er avgjort av Kjetil, (b) planen sier at en død sjekk er usynlig til trinn 5, og (c) trinn 3+4 får en egen rad «Når får du cron, og hva kan stoppe det». Ellers reorganiser.

---

## P8. Språk og forståelighet

**Konklusjon:** Trinntabellen og sikkerhetsavsnittet er gode, men planen forutsetter at Kjetil kjenner ti systemnavn, sier «Ingenting» der han må avgjøre, gir tall som «et tak» uten verdi, og rundt halvparten av teksten er skrevet til Losen og Fabel, ikke til ham.

**Uklart for Kjetil**

- «Ingenting» i trinn 3 `[belagt: PLAN.md:36]` — han må godkjenne merge/gren (§6) og tåle en omstart.
- «Godkjenner de to linjene i policyen» `[belagt: 34]` — det er fire oppføringer i to deler av `config.json` `[belagt: 43-48]`, og det er Losens skript som skriver dem. Hvem som skriver, står ikke.
- «Slår på køjobber i konfigurasjonen» `[belagt: 37]` — hvordan? Av hvem?
- «Det er et tak på hvor mange jobber … og hvor ofte» `[belagt: 23]` — ingen tall. Han skal godkjenne tallene.
- «Punkt 2 er avslått til du slår det på» `[belagt: 20]` — men `.agent-spool` er åpen for Losen i dag uansett; porten gjelder bare planlagt tid.
- Hva han *ikke* får: at trinn 1–2 ikke er cron; at en død sjekk er usynlig; at diskregelen stopper bygg i dag.

**Forutsatt kunnskap han ikke har fått**

`.agent-spool`, `_losen-queue`, launchd, `localTask`, policy, MCP, kontrollbroen, kilden `job`, HD-0156, PR #25, AP, T0–T10, G1-GUI, jobbmal, `.spec.json`/`.runtime.json`, låsfil, `0 9 * * *`, `haven_learn.py`, `purpose_dev.py validate`. Hver kan få én setning første gang, eller gå i en ordliste. «Kø-tråden» og «Losen» brukes om to tråder med samme navn `[belagt: PLAN.md:71; job-246:205]`.

**Hva som kan strykes eller flyttes** (til et vedlegg for Losen): «Arbeidspakkene» `[belagt: 52-71]`, «Det runde 2 fant» `[belagt: 81-94]`, det meste av «Koordinering» utenom de to punktene som krever ham. Det som bør inn i stedet: en kort «Hva du får, og når» (cron i trinn 3, agenten bruker den i trinn 4), en «Hva kan stanse planen» (disk, HD-0156, gren, varselsamtykke, MCP i Claude-appen, klient fra planleggeren) og en «Hva du avgjør nå» (E1–E5, markørens betydning, tallene).

Bildet `images/plan-oversikt-v2.png` `[belagt: PLAN.md:7]` er `[ikke belagt]`; finnes det, er det rett grep.

---

## Må endres før dette legges fram for Kjetil

1. **F8-markørens betydning** legges fram som et valg for Kjetil («ulest, venter på Losen» eller «krever meg»), med konsekvensen for Losens automatiske kvittering (P4).
2. **Trinn 1–2 får sine grenser skrevet inn**: ingen tidsgrense, en død sjekk er usynlig til trinn 5, og T8 måler menyen etter at planleggeren er stoppet (P2, P5).
3. **Programkravene** (P2-lista: egen tidsgrense, ingen arvede rør, prosessgruppe drepes, <64 KiB på begge rør, ingen dialoger, atomisk markør, låsfil) inn i AP2/AP4, og `schedule-list --config <kopi>` i AP3 i stedet for bare `validate-config`.
4. **Markørinnhold**: visningsnavn, aldri ID; stabil `id` per profil; test mot `looksLikeSecret` og tittellengde (P4, P5).
5. **F5** får overskriften T4 beviser, og `spoolJob`-maler legges i `automationPolicy` som godkjente handlinger, ikke opprettes via MCP (P3).
6. **Sikkerhetsavsnittet** nevner den relative skriptstien i `.agent-spool`, merge via `gh api`, og at konfigurasjonsendringer gjøres av Losens skript fra køen — og hva Kjetils godkjenning da faktisk binder (P3, P6).
7. **Installasjonsregelen** gjengis med alle fire ledd; «Ingenting» i trinn 3 erstattes med det Kjetil må avgjøre; «tom kø» tolkes og avtales i KOORDINERING (P6).
8. **Bakoverkompatibilitet**: ny `config.json` og ny tilstandsmappe skal dekodes av `main`-binæren og tilbakerullingen; egen test (P6, P5).
9. **AP11** bruker eksisterende svar-ID-er (f.eks. `reject` med etikett «Stopp jobben») eller erkjenner kontraktsendring og bygger menyapp samtidig; sier hvor «Kvitter» lagres (P1-7).
10. **Språk**: «Hva du får, og når», «Hva kan stanse planen», «Hva du avgjør nå», tallene for tak og sluttdato, og AP/runde 2-tabellen til vedlegg (P8).

## Bør endres

- Rekkefølgen vurderes mot 0 → 3 → 4 → 1/2 → 5, eller trinn 3+4 får egen rad som «cron-milepælen» (P7).
- Opprinnelse for MCP-opprettede jobber avgjøres (ikke `.local` uten begrunnelse) (P1-5).
- Hash av programmene i `bin/` føres i TESTRESULT og i Kjetils godkjenning, inntil pinning finnes i policyen (P1-1).
- T0 kjører `swift test` av HavenAgentD gjennom `.agent-spool`, med diskvakten, før trinn 3 planlegges (P5).
- F9 får avhengigheten «utløp kan leses lokalt» i §2 (P5).
- `requiresUserSession` håndheves eller fjernes; søvn (`pmset`) måles, siden det kan være nattens egentlige årsak.
- HD-0069s to Kjetil-godkjenninger bes om eksplisitt i stedet for å påstå at trinn 1 løser oppgaven.
- Scheduler-plisten inn i repo *og* installeres av skriptet.

## Kan vente

- Hullene i `.agent-tools/agent_job_runner.py` (relativ sti, undermappe-omgåelse, PATH) meldes eieren som egen oppgave.
- Egen macOS-bruker for jobbene (fortsatt den eneste formen som begrenser skaden).
- Samtidige hendelser i planleggeren.
- Opprett og pause fra HAVEN.
