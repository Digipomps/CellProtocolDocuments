# Vedlegg til PLAN: arbeidspakker og sporing

PDD `agent-planlagte-jobber`, runde 3, 02.10.2026. Dette vedlegget er for den som utfører og den som gransker. Det Kjetil trenger, står i `PLAN.md`. Formatene står i `contract/`, flyten i `dataflow.md`, og rekkefølgen for køene i `handoff/README.md`. Der vedlegget og kontrakten sier ulike ting, gjelder kontrakten; avsnittet «Endret da kontrakten ble skrevet» nederst sier hva som ble endret.

## Arbeidspakkene

Alle pakkene utføres av Losen (tråden i prosjektet «HavenAgentD»). Test-ID-ene viser til `FORMAALSSPEC.md` §5.

| AP | Trinn | Hva som gjøres | Test |
|---|---|---|---|
| AP0 | 0 | HAVEN-roten er koblet til (02.10). Én jobb kjøres gjennom `.agent-spool`: `git status` i HavenAgentD og `gh api user`. Signaturen på de installerte binærene leses (`codesign -dv`), som siste jobb for den gamle løperen. `queue/STOP` stopper den, og `Claude outputs/agentd-runner.command` får navnet `agentd-runner.command.utgaatt-20261002`. Jobbkøen under `.tmp-clang-module-cache/agentd-diag/` flyttes ikke; den brukes ikke mer. | T0 |
| AP1 | 0 | En linje i `_losen-queue/KOORDINERING.md` når løperen er stoppet, og en rad før S1 starter: gren (`claude/planlagte-jobber-20261002` fra `origin/main`), arbeidstre, hva som skal installeres og når. Arbeidet er meldt 02.10 (punkt 7 i avsnittet «Korrespondanse-fornyelse»). Diskvakten kjøres før hvert Swift-bygg. | T0 |
| AP2 | 1 | `Scripts/scheduled/korrespondanse_vakt.py`, oppgaven `sjekk`, etter `contract/trinn1-2-programmer.md`. Starter korrespondanseklienten per profil, spør hvilke verktøy den har, og lister innboksen med blaing. Teller meldinger uten `acknowledgedAt`. Skriver én markør per avsender og profil etter `haven.correspondence-waiting.v1`: `id` er `ulest-<profil>-<avsender>`, `from` er visningsnavnet fra `--navn` og ellers «en ukjent avsender» (aldri en ID), `summary` er antall og eldste tidspunkt, `markedBy` er `agent-korrespondansesjekk`. Emne og innhold tas aldri med. Tidsbudsjettet er 50 sekunder delt på antall profiler, høyst 25 per profil og høyst fire profiler, og rekkefølgen flyttes ett hakk for hver kjøring. En profil som ikke kan leses to ganger på rad, gir markøren `sjekk-feilet-<profil>`; markørene for ulest post står da som de var. Tittelen lages av agenten og blir «Post fra … venter på svar» også for feil. | T8 med prøvedata |
| AP2-krav | 1–2 | Kravene til begge oppgavene står i `contract/trinn1-2-programmer.md`: tidsgrense på 60 sekunder (alarm og hard avslutning); klienten startes med egne rør i egen prosessgruppe som drepes i `finally`; under 4 KiB på både stdout og stderr; ingen dialoger; markører skrives til skjult midlertidig fil og byttes på plass; låsfil så to kjøringer ikke går samtidig; alle stier som argumenter, også klientens rot (`--root`); vakttråden dreper klienten og skriver stempel før den avslutter; tidspunkter med millisekunder tolkes av programmet selv; tekst kontrolleres mot samme regel som agenten bruker; stempel etter hver kjøring i `State/ScheduledTasks/`. Hver oppgave leser den andres stempel og skriver markøren `sjekk-stoppet-<navn>` når det er for gammelt og oppgavens eget forrige stempel er ferskt. Søskenvakten tas ut i trinn 4. `selvtest` dekker dette med prøvedata. | T8, T9 |
| AP3 | 1 | `Scripts/install-scheduled-tasks.sh` med `toerr` (standard), `utfoer` og `fjern`, etter `handoff/README.md` S2. Kjører selvtesten, skriver sjekksummene, lager en kandidat av `config.json` med tillegget i `contract/config-tillegg-trinn1-2.json`, og validerer kandidaten med `validate-config --config` og `schedule-list --config`, som ikke skriver noe. Kontrollerer selv at hver hendelse peker på et fast program, for det gjør ikke agenten. Viser forskjellen med tokenet skjult, etter at begge filene er skrevet ut med samme oppsett. `utfoer` tar sikkerhetskopi, bytter fila, venter til ingen hendelse kjører, starter planleggeren på nytt med `launchctl kickstart -k`, og skriver ut utfallet av første kjøring. Bash 3.2 og `/usr/bin/python3`. Kjøres som `skript`-jobb i `_losen-queue` gjennom en omslagsfil under `HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/` med sjekksummene skrevet inn. | T8 live, T10 |
| AP4 | 2 | Samme program, oppgaven `frist`: leser `accessCredential.payload.expiresAt` i `profile.json` per profil. Markør `frist-<profil>` når det er sju døgn eller mindre igjen, og når profilen ikke har noe bevis. Fjernes når fristen er flyttet. | T9 |
| AP5 | 3 | `CronSchedule`, etter `contract/trinn3-cron.md`. Fasiten er `contract/fixtures/cron-forventninger.json`, laget med `contract/cron_reference.py`: fem felt, lister, områder, steg, 0 og 7 som søndag, dag eller ukedag. Sommertid følger cronie: et løpende uttrykk (minutt eller time begynner med `*`) kjører i begge timene når en time kommer to ganger, og ikke i timen som mangler; et fast klokkeslett kjøres én gang, og rett etter hoppet når det ikke finnes. Søket er avgrenset til åtte år. Umulige uttrykk og ukjent tidssone avvises. Tidssonen lagres alltid uttrykkelig. | T1 |
| AP6 | 3 | Planleggeren, etter `contract/trinn3-cron.md`. Faste hendelser i `config.json` får de valgfrie feltene `cron`, `timeZone`, `timeoutSeconds` og `title`, og `AgentConfig` og `ScheduledEventDefinition` får dem også, så agentens egen `write` ikke mister dem; `firstFireAt`, `repeatMode` og `intervalSeconds` står, så en eldre agent kjører hendelsen på intervallet. Ingen nye verdier i `repeatMode`, `action.kind` eller `status`. Hver forekomst kjøres høyst én gang (`lastOccurrence` skrives før kjøringen). Passerte tidspunkt telles; de gir sak bare for hendelser som går én gang i døgnet eller sjeldnere. Tidsgrense per kjøring med SIGTERM og så SIGKILL til hele prosessgruppen. Utdata til `Logs/ScheduledJobs/<id>/<tidspunkt>.log`, ikke rør, med tak på 8 MiB. Lås (`flock`) så bare én arbeider går, og livstegn hvert 30. sekund fra en egen oppgave, også mens et program kjører. En kjøring som ble avbrutt, kjøres ikke på nytt; den blir en sak. | T2, T3 |
| AP7 | 3 | PR mot `main`. Planleggerens plist legges i `Launchd/`, og `Scripts/install-agent-dev.sh` installerer den. Etter merge på Kjetils ord: bygg gjennom `.agent-spool`, og signering og installasjon med `Scripts/install-agent-dev.sh` som `skript`-jobb i et avtalt vindu, én gang per produkt med `--source` (`handoff/README.md`). Skriptet er zsh og kalles med `/bin/zsh` fra en omslagsfil. Fristvarselet får `cron` `0 9 * * *` og `timeZone` `Europe/Oslo` i `config.json`, med samme installasjonsrutine som i AP3. | T2 og T3 live, T10 |
| AP8 | 4 | CLI og MCP, etter `contract/trinn4-jobber-og-godkjenning.md` og `contract/mcp-verktoy.json`: `schedule-request`, `-list`, `-state`, `-pause`, `-resume`, `-stop`, `-remove`, `-approve`, og `agent.schedule.*` uten noe verktøy for godkjenning. En jobb bor i `State/ScheduledJobs/<id>.spec.json`, endres aldri, og bærer bare handlingens type og ID. En bestilling uten oppgitt id kan ikke erstatte en jobb som finnes. Alle slike jobber må godkjennes, uansett hvem som ba, og en bestilling ingen svarer på, utløper ved sluttdatoen. MCP-verktøyene styrer bare jobber som er bedt om, ikke faste hendelser. Korteste avstand mellom to kjøringer regnes over jobbens levetid. `requestedBy` settes av agenten fra navnet MCP-klienten oppgir. Sluttdato settes alltid. Takene i `PLAN.md` håndheves under lås. Handlingen kjøres med samme opprinnelse som i dag (`local`). | T4, T5 |
| AP9 | 4 | Kilden `job` får en leverandør, og `AgentChallengeWiring.responseHandler` får en gren for `job:`, etter `contract/trinn4-jobber-og-godkjenning.md` og `contract/saker-job.example.json`. (a) Venter på godkjenning: `intent-approval` med «Godkjenn», «Avvis» og «Åpne». Sakens id bærer tolv tegn av sjekksummen til `spec`-fila, og svaret kontrolleres mot fila slik den ligger da. Tittelen bærer bestillerens tittel i anførselstegn. «Gjelder» (som menyen viser) og detaljen (som adminvinduet viser) lages av agenten; «Gjelder» har hva som kjøres i kortform. En jobb som ikke kan vises i sin helhet innenfor 400 tegn og uten ID-liknende tekst, avvises når den bes om. (b) Feilet, passert eller ugyldig: én sak per jobb med «Kvitter» og «Åpne», og «Stopp jobben» når jobben er bedt om. Saker om faste hendelser har bare «Kvitter» og «Åpne»; pause og fortsett for dem står i lista (AP13). Et svar saken ikke tilbyr, skriver ingenting. Titler over 80 tegn avkortes. Passering gir sak bare for jobber som går én gang i døgnet eller sjeldnere. Kvitteringen lagres i `<id>.ack.json` med tidspunktet den gjelder til. (c) «Planleggeren går ikke» når livstegnet er gammelt i to minutter våken tid. Kan mappen ikke leses, melder leverandøren `unreadable`. Sakene har `handleAt.venue: admin-window`, så «Åpne» gjør det samme fra menyen, adminvinduet og et varsel. Menyappen som er installert, viser og besvarer alle tre uten endring. Godkjenningen går gjennom én funksjon, som også `schedule-approve` bruker. Agenten kan ikke skille et svar fra menylinjen fra et svar fra et annet program med samme token; det står i `Docs/SecurityModel.md`. | T4, T6, T7 |
| AP10 | 4 | Handlingen `spoolJob`: jobbmalen lagres som `<id>.spool.json`, og sjekksummen står i `spec`-fila. Malen kontrolleres for form når jobben bes om; køen håndhever sin egen tillatt-liste når jobben kjøres, og agenten har ingen kopi av den. Til avtalt tid kopierer planleggeren malen til køen som er navngitt i konfigurasjonen (`scheduledJobs.spoolInbox`), som `<id>-<ÅÅÅÅMMDDTttmmssZ>.json`, via `.partial` og omdøping. En fil køen ikke har tatt, slettes igjen ved pause, stopp, sluttdato og utløpt frist. Avslått til konfigurasjonen navngir køen. Planleggeren venter ikke: resultatfila i `outbox/` leses ved en senere runde, og uteblir den, blir utfallet `no-result`. | T4, T6 |
| AP11 | 4 | Agentens MCP-server legges inn i Claude-appen, etter Kjetils ja. | T6 |
| AP12 | 5 | Kontrollbroen, etter `contract/trinn5-kontrollbro.md`: `GET /scheduled-jobs` gir statuslista (`scheduled-jobs-status-v1`), og `POST /scheduled-jobs/control` tar pause, fortsett og stopp. Token i `Authorization`-hodet. Rutene skriver styringsfila gjennom samme funksjon som CLI og MCP, under lås. Faste hendelser kan settes på pause og startes igjen herfra, ikke stoppes. | T7 |
| AP13 | 5 | Menylinjen etter de godkjente bildene: «Planlagte jobber» med neste tidspunkt, siste utfall, pause og stopp. Linjen kommer i tillegg til det menyen viser i dag. Sakene fra korrespondansesjekken får tittelen «Ulest post fra …» når `markedBy` er programmet, og feilmarkørene får en egen tittel. Pause og fortsett for faste hendelser står i lista, ikke på sakene. | T7, bilde av den ekte menyen |
| AP14 | 6 | `Docs/ScheduledEvents.md`, `Docs/SecurityModel.md` (hva køene åpner for, og hva godkjenningen ikke stopper), `Docs/OperatorRunbook.md` (planleggeren, programmene, målingene). `TESTRESULT.md`, `ACCEPT.md`, lærdommer, `haven_learn.py`. Svakhetene i `.agent-tools/agent_job_runner.py` meldes kø-tråden. | T10 og `purpose_dev.py validate` |

## Fabels ti punkter i runde 3, og hvor de ble av

| # | Fabel krevde | Nå |
|---|---|---|
| 1 | F8-markørens betydning legges fram som et valg | E6 i spesifikasjonen, og punkt 2 under «Det du godkjenner i G2». Feilmarkørene får samme tittelform; det står under «Grensene i trinn 1 og 2». |
| 2 | Grensene i trinn 1–2 skrives inn, og T8 måler menyen etter at planleggeren er stoppet | «Grensene i trinn 1 og 2» i planen, T8 |
| 3 | Programkravene, og validering med `schedule-list --config <kopi>` | AP2-krav, AP3 |
| 4 | Markørinnhold: visningsnavn, stabil `id`, test mot hemmelighetsfilteret og tittellengden | AP2, T8 |
| 5 | F5 får overskriften T4 beviser; jobbmaler godkjennes av Kjetil | Erstattet, ikke fulgt: Fabel foreslo maler i policyen. Planen har i stedet ett trykk per jobb (E2, AP9, AP10), fordi maler i policyen ville krevd en konfigurasjonsendring for hver ny jobb. F5 sier nå det T4 og T5 beviser: det Losen ber om gjennom agenten, kjører ikke før det er godkjent, og ingen MCP-verktøy kan godkjenne. |
| 6 | Sikkerhetsavsnittet nevner den relative skriptstien, merge gjennom `gh api`, og at Losens skript endrer konfigurasjonen | «Det du må vite om sikkerheten» i planen. Etter etterkontrollen sier avsnittet også at kode i køene kan gi godkjenningen selv. |
| 7 | Installasjonsregelen med alle fire ledd; «Ingenting» i trinn 3 erstattes; «tom kø» avtales | Trinn 3, «Koordinering», AP1, AP7. Basen er `origin/main`: agenten som kjører, er bygget fra `main`. |
| 8 | Eldre agent tåler ny konfigurasjon og tilstand | AP6 (cron aldri i `config.json`), T10 |
| 9 | AP11 bruker svar-ID-er som finnes, og sier hvor kvitteringen lagres | AP9, AP12 |
| 10 | Språk: hva du får og når, hva som kan stanse planen, hva du avgjør, tall | Planen er skrevet om. Arbeidspakkene er flyttet hit. |

Fra «Bør endres»: rekkefølgen er beholdt, og planen sier at trinn 1 og 2 ikke er cron. Opprinnelsen for jobber bedt om gjennom MCP er avgjort i AP8. Sjekksummene føres i `TESTRESULT.md` og vises Kjetil. `swift test` gjennom køen er lagt i T0. Avhengigheten for F9 er målt. HD-0069 lukkes av kø-tråden. Plisten legges i repoet og installeres av skriptet (AP7). `requiresUserSession` håndheves ikke i dag og røres ikke her; det står i `Docs/SecurityModel.md` som kjent avvik (AP14).

## Etterkontrollen (`panel/FABEL_ETTERKONTROLL_RUNDE3.md`)

| # | Fabel krevde | Nå |
|---|---|---|
| 1 | Trykket stenger MCP-veien, ikke køene; ingen MCP-verktøy får godkjenne | F5, E2, §2 i spesifikasjonen; sikkerhetsavsnittet i planen; T5 |
| 2 | Hva Kjetil ser før han trykker | AP9: agenten lager teksten fra spec-fila, og for store jobber avvises. Adminvinduet viser detaljen i dag (`AdminWindow.swift` linje 119–120, lest 02.10). |
| 3 | `responseHandler` får en gren for `job:`; test at jobbsaker ikke gjør innboksen uleselig | AP9, T4 |
| 4 | Feilmarkørene i trinn 1–2 vises som «Post fra … venter på svar» | AP2, «Grensene i trinn 1 og 2» |
| 5 | Bildet «planleggeren går ikke» og AP12 beskrev to mekanismer | AP9 (c): død lås gir saken i bildet; uleselig tilstand gir «Får ikke lest job» som i dag. Undertittelen i post-bildet er bekreftet mot `CorrespondenceWaiting.swift`: `requestedBy` er `from`, `subject` er `profile`. |
| 6 | «Når» per trinn, og en eier for diskryddingen | «Hva du får, og når» og «Hva som kan stanse planen» |
| 7 | `gh` fra køen virker trolig ikke | planen og §2 i spesifikasjonen |
| 8 | Ordlista utvides | «Ord som brukes» |

Utfall i menylinjen fra trinn 4: feil og passering blir saker i AP9, som hører til trinn 4. Lista «Planlagte jobber» er trinn 5.

## Fabels åtte punkter i runde 2

| Punkt | Nå |
|---|---|
| 1 Løperen ut av mappen Losen skriver i | Løperen legges ned. Faste programmer installeres i `bin/`, med sjekksum vist Kjetil. Sjekksum i policyen er ikke med i denne runden. |
| 2 Én skriver per fil, låsfil, høyst én kjøring per forekomst | AP6 |
| 3 Sommertid som faste UTC-tidspunkt, avgrenset søk, validering | AP5, T1 |
| 4 Utdata til loggfil, tidsgrense, tester for barneprosess og stor utdata | AP6, T2 |
| 5 Dynamiske handlinger er bare type og ID | AP8 |
| 6 Planleggerens plist i repoet | AP7 |
| 7 Kontrakt, testdata og menyapp sammen, kvittering, én sak per jobb | AP9, AP12. Kilden og svarene finnes, så kontrakten endres ikke. |
| 8 F8 og F9 får komponent, F4 innsnevres, F5 får fotnote | Trinn 1 og 2, E3, og F5 handler nå om godkjenning (E2). |

## Endret da kontrakten ble skrevet (02.10 kveld)

Kontrakten ble skrevet mot kilden på `origin/main` (`ea558ba`). Det ga disse endringene i arbeidspakkene:

| Hva | Før | Nå | Hvorfor |
|---|---|---|---|
| Programmene i trinn 1 og 2 | to filer | én fil, `korrespondanse_vakt.py`, med oppgavene `sjekk` og `frist` | Én fil og én sjekksum å kontrollere. Felles kode for tidsgrense, lås, markører og tekstkontroll. |
| Markør-id for ulest post | `ulest-<principal>` | `ulest-<profil>-<avsender>` | Samme avsender kan skrive til to profiler. |
| Når en feil blir en sak | første gang | etter to kjøringer på rad | Macen som våkner, eller en omstart på staging, skal ikke gi falsk alarm. |
| Hvilken klient programmet snakker med | «korrespondanseklienten» | pilotklienten som er installert. Programmet spør om verktøyene og sier fra hvis kontrakten er en annen. | Kilden på `main` er en ny klient der verktøyene krever `relationshipID`. |
| Cron for faste hendelser (AP6, AP7) | egen spec-fil; aldri i `config.json` | valgfrie felt i `config.json` | En eldre agent ser bort fra feltene og kjører på intervall. Det er bedre enn at hendelsen står stille etter en tilbakerulling. |
| Godkjenning (AP8, AP9) | bare for jobber bedt om gjennom MCP | for alle jobber i `State/ScheduledJobs/` | Arbeideren får én regel, og ingen kan slippe unna ved å oppgi et annet opphav. |
| Sakens id (AP9) | per jobb | per jobb og sjekksum | Endres jobben mellom visning og trykk, gjelder trykket ikke den nye. |
| Hvem saken sier ber | «Losen» | «Claude», «Codex» eller «En assistent», fra navnet MCP-klienten oppgir | Agenten vet ikke mer enn det. Bildet er rettet (v3). |
| «Åpne» på en sak (AP9) | antatt å åpne adminvinduet overalt | `handleAt.venue: admin-window` | I menyen åpner «Åpne» alltid adminvinduet. Fra et varsel og fra adminvinduet følger den `handleAt` (`ChallengeOpenPlan.swift`). |
| «Planleggeren går ikke» (AP9) | død lås | gammelt livstegn i to minutter våken tid | Ellers kommer saken hver gang Macen våkner. |
| Køjobbens resultat (AP10) | planleggeren leser resultatfila | leses ved en senere runde; `no-result` etter fristen | Planleggeren kjører én ting om gangen og skal ikke vente på en annen kø. |
| Ruter på kontrollbroen (AP12) | uspesifisert | token i `Authorization`-hodet | Slik den nyeste ruten gjør (`commands/workbench`). |
| T5 | ingen verktøy kan godkjenne | prøver også `agent.review.approve` | Det verktøyet godkjenner fjernintenter og finnes i dag. |

Nytt i sikkerhetsavsnittet i `PLAN.md`: hva Claude får når agentens MCP-server legges inn i Claude-appen. `agent.jobs.register` med `onComplete.actions` og `agent.jobs.complete` gjør at et fast program kan kjøres med en gang gjennom MCP (`JobCompletionService.dispatchActions`). Trykket for planlagte jobber endrer ikke det.

## Fabels gransking av G2-artefaktene (`panel/FABEL_SVAR_G2.md`)

Fabel kontrollerte omtrent 55 påstander mot kilden, regnet etter alle cron-tilfellene med en egen framgangsmåte, og fant seks punkter som måtte rettes, tjue som burde, og sytten mangler.

| # | Fabel fant | Nå |
|---|---|---|
| Må 1 | Menyraden der «Godkjenn» ligger, viser ikke hva som kjøres | «Gjelder» lages av agenten og har hva som kjøres i kortform; tittelen fra bestilleren står i anførselstegn; planen sier at hele jobben står i adminvinduet (`contract/trinn4`, `PLAN.md`, bildet v4). Presisering av F5 legges fram i G2. |
| Må 2 | Daglig falsk sak etter søvn for korrespondansesjekken | Passering gir sak bare for hendelser som går én gang i døgnet eller sjeldnere (`contract/trinn3`). Presisering av F6 legges fram i G2. |
| Må 3 | Køfilas navn kan gjøre at jobben aldri kjøres | `<id>-<ÅÅÅÅMMDDTttmmssZ>.json`; kontrollen prøver navnet mot køens mønster. |
| Må 4 | En køfil som ikke ble tatt, kjøres likevel senere | Arbeideren sletter fila ved pause, stopp, sluttdato og utløpt frist (`contract/trinn4`). |
| Må 5 | Installasjonskommandoen for ny agent kan ikke kjøres som skrevet | Bygg i `.agent-spool`; installasjon én gang per produkt med `--source`, kalt med `/bin/zsh` (`handoff/README.md`). |
| Må 6 | Fristgrensen motsier sin egen fasit | Terskelen er hele døgn igjen, rundet ned; selvtesten har grensetilfellene. |
| Bør 1 | Falsk «har stoppet» etter lang søvn og ved pause | Søskenvakten krever at eget forrige stempel er ferskt; den tas ut i trinn 4. |
| Bør 2 | Livstegnet må skrives uavhengig av kjøringen | Egen oppgave i arbeideren; T7 prøver det. |
| Bør 3 | Vakttråden hopper over `finally` | Vakttråden dreper klienten og skriver stempel før den avslutter; alarmen har en behandler som kaster. |
| Bør 4 | Tidsbudsjettet tar ikke høyde for klientens egen tidsgrense | 25 sekunder per profil, 12 per forsøk, og rekkefølgen flyttes. |
| Bør 5 | «Eldre agent ser bort fra nye felt» gjelder lesing, ikke skriving | Står i `contract/trinn3`, og T10 prøver skriving. |
| Bør 6 | Sikkerhetslista utelater `agent.xcode.ensure_workspace`, og er abstrakt | Lagt til i `PLAN.md`, med navnene på de to faste programmene som finnes. |
| Bør 7 | En generert id kan erstatte en godkjent jobb | Erstatning krever oppgitt id. |
| Bør 8 | MCP kan stoppe Kjetils faste hendelser uten trykk | MCP styrer bare jobber som er bedt om. Presisering av F4 legges fram i G2. |
| Bør 9 | «Siste skriver vinner» mot «stopped kan ikke gjøres om» | Én funksjon under lås, med faste overganger. |
| Bør 10 | «For ofte» avhenger av bestillingsdato | Regnes over jobbens levetid. |
| Bør 11 | Regelen for løpende uttrykk gir overraskelser | Regelen ser på alle ledd i lista, ikke bare det første; tre følger står i kontrakten og i fasiten. |
| Bør 12 | Tidsstempler med millisekunder og `Z` | Programmet tolker formen selv; selvtesten har tilfellet. |
| Bør 13 | Forskjellen i `config.json` blir uleselig uten normalisering | Begge filene skrives ut med samme oppsett før sammenligningen. |
| Bør 14 | Omstart av planleggeren midt i en kjøring | Skriptet venter til ingen hendelse kjører. |
| Bør 15 | Porten av køens kontroll er ufullstendig | Agenten har ingen kopi av tillatt-lista; køen håndhever sin egen. |
| Bør 16 | En ventende godkjenning utløper aldri | Utløper ved sluttdatoen; leverandøren leser ikke `Removed/`. |
| Bør 17 | Kort flimmer ved ny bestilling på samme id | Jobbmalen ligger under et navn med sjekksummen i. |
| Bør 18 | Småting der dokumentene sier ulikt | Rettet i `dataflow.md`, `contract/README.md`, `FORMAALSSPEC.md`, `PLAN.md` og bildene. |
| Bør 19 | Mål før S1 og S3 stoler på det | `git push --dry-run` i S0; signering fra en køjobb måles i tørrkjøringen. |
| Bør 20 | Hvor `requestedBy` kommer fra | Fra `clientInfo.name`, med regelen skrevet ned; måles i T6. |
| Mangler 1–10 | Trinn 1 og 2: oppdagelse av annen kontrakt, blaing, nytt forsøk, lås og stempel, markørenes livsløp, utskriften, klientens rot, installasjonsskriptet, omslaget | `contract/trinn1-2-programmer.md` og `handoff/README.md`. |
| Mangler 11–17 | Trinn 3–5: `interval` og `once`, tittel for faste hendelser, `AgentConfig`, stoppet fast hendelse, navnet fra klienten, livstegn og tilbaketrekking, passering for intervall | `contract/trinn3-cron.md`, `trinn4-jobber-og-godkjenning.md`, `trinn5-kontrollbro.md`. |

## Fabels etterkontroll av G2-artefaktene (`panel/FABEL_ETTERKONTROLL_G2.md`)

Fabel fant alle 26 punktene løst, regnet de 57 cron-tilfellene etter på nytt, og fant at de tre valgene som ble gjort annerledes enn den foreslo, holder. Rettelsene hadde laget tretten nye feil.

| # | Fabel fant | Nå |
|---|---|---|
| 1 | «Stopp jobben» på saker om faste hendelser satte dem på pause | Slike saker har bare «Kvitter» og «Åpne». Pause og fortsett for faste hendelser står i lista «Planlagte jobber» (`contract/trinn4`, `trinn5`, `saker-job.example.json`, `dataflow.md` K32, feil-bildet v3). |
| 2 | Testtabellen i §5 var ikke oppdatert | §5 er oppdatert og er den ene lista; kontraktene viser dit. |
| 3 | §6 sa «ingen åpne spørsmål» | §6 har de tre spørsmålene, og `PLAN.md` har dem i en egen tabell med hva et nei betyr. |
| 4 | `resume` manglet regel for `lastOccurrence` | Arbeideren regner fra det seneste av `lastOccurrence` og tidspunktet i styringsfila. Pausen hentes ikke inn og telles ikke (`contract/trinn4`, styringen). |
| 5 | En fast hendelse uten `title` kunne gi en tittel over 80 tegn | Titler avkortes til 80 tegn, og installasjonsskriptet krever `title` eller en id på høyst 40 tegn. |
| 6 | Tidsbudsjettet var skrevet for to profiler | 50 sekunder delt på antall profiler, høyst fire profiler. |
| 7 | `PLAN.md` sa mindre enn kontrakten to steder | Programlinjene nevner klientens rot, og presisering 3 sier «fra menyen eller kommandolinjen». |
| 8 | `spool-not-enabled` nevnte bare én nøkkel | Begge nøklene. |
| 9 | Prøven av `git push` i S0 kunne gi falskt nei | Tørrkjøring mot et grennavn som ikke finnes; «rejected» regnes som at nøklene virket. |
| 10 | Ingen regel når klienten ikke tar `--root` | `toerr` stopper. |
| 11 | Eksempelet «åtte timers søvn gir 15» | «15 eller 16». |
| 12 | Formkontrollen manglet `env` | `env` må være et objekt med `HAVEN_`-nøkler, hvert steg må ha minst ett ledd, og `env` vises i detaljen. |
| 13 | Småting | Tallet på granskinger er rettet, og «En assistent» er skrevet inn som det lengste navnet. Fasiten har fått `30 */2` mot `30 0-23/2` (fire tellinger). |

Fabel kontrollerte så rettelsene (`panel/FABEL_ETTERKONTROLL2_G2.md`): 13 av 13 løst, og fem småting til.

| # | Fabel fant | Nå |
|---|---|---|
| 1 | To dokumenter sa ulikt om hva «Fortsett» gjør for en fast hendelse på intervall | Unntaket står i `contract/trinn5` og i T3: en slik hendelse kjøres straks, og pausen telles ikke. |
| 2 | «Fra trinn 5» er ikke noe agenten kan vite | Knappen er tatt ut: saker om faste hendelser har «Kvitter» og «Åpne» i alle trinn. |
| 3 | Formkontrollen slapp gjennom `timeoutSeconds` og `name` | Heltall fra 1 til 10800, tekst for `name`, sann eller usann for `stopOnFailure`. |
| 4 | Ingen regel for et svar saken ikke tilbyr | `accepted: false`, og ingenting skrives. |
| 5 | Eksempelet hadde én knapp mer enn trinn 4 | Eksempelet og bildet har samme form som trinn 4 og 5. |

## Fabels gransking av koden for trinn 1 og 2 (`panel/FABEL_KODE_TRINN1-2.md`)

Koden ble skrevet og testet i skyen 02.10 mens G2 ventet, og ligger som pakke i `handoff/` til den kan legges i arbeidstreet. Fabel gransket den som uavhengig kodegransker, kjørte testene selv og prøvde ti egne tilfeller.

| # | Fabel fant | Nå |
|---|---|---|
| Må 1 | Blaingen stoppet på en kort side. Gir tjeneren færre per side enn det bes om, ble de nyeste meldingene aldri sett | Blaingen stopper på en tom side. Selvtesten har en klient som gir 50 per side. |
| Bør 1 | Alarmen under lukkingen kastet en lesing som var ferdig | Lesingen beholdes; kjøringen går rett til markørene. Selvtesten prøver det. |
| Bør 2 | Vakttråden gjorde filarbeid før den avsluttet | En siste tidtaker avslutter fem sekunder senere uten å røre noe. |
| Bør 3 | Et uventet unntak ga traceback | Én linje og kode 1. Årstall utenfor 2000–2999 regnes som «kan ikke tolkes». |
| Bør 4 | Klientens stderr kom ikke med ved tidsavbrudd | Legges ved, og det er slutten av fila som leses. |
| Bør 5 | Lange profilnavn ga «en ukjent avsender» på feilmarkørene | Profilnavn er høyst 36 tegn. |
| Bør 6 | Skjulte midlertidige filer ble aldri ryddet | Ryddes når de er ti minutter gamle, og av `fjern`. |
| Bør 7 | Markørfasen fjernet før den skrev | Skriver først. Alarmen slås av når lesingene er over. |
| Bør 8 | Kappløp ved den siste linjen | En lås mellom hovedløpet og vakttråden. |
| Bør 9 | `fjern` mens en kjøring går, etterlot en sak | `fjern` venter til ingen kjøring holder låsen. |
| Bør 10 | Kandidaten ble validert med `haven-agentd`, ikke planleggerbinæren | Valideres med begge. |
| Bør 11 | Andre feil enn ventet ga traceback i installasjonen | «STOPPET»-linje. |
| Bør 12 | Filnavn i markørmappen ble skrevet ut | Avsender og profil skrives, ikke filnavn. |
| Bør 13 | `__pycache__` i arbeidstreet | Skrives ikke. |
| Bør 14 | `config.json` fikk annet oppsett enn agentens | Samme skilletegn; resten står i runbooken. |
| Bør 15 | `urlopen` fulgte systemets proxy | Går aldri gjennom proxy. |
| Bør 16 | Kandidaten lå med 0644 | 0600. |
| Bør 17 | Setninger som sa mer enn koden | Rettet i `Docs/` og kontrakten. |
| Bør 18 | Det testene ikke prøvde | Lagt til: alarmen, treg lukking, 50 per side, de ekte grensene (50 sekunder), `fjern` mens en kjøring går, filfeil, tidspunkt som ikke kan tolkes. Omslaget for køen har fortsatt ingen automatisk test; det er prøvd for hånd av Losen og Fabel. |

Fabel kontrollerte rettelsene (`panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL.md`): 15 av 19 løst, fire delvis (to av dem med hensikt), og testene stabile (30 tester, selvtesten 120 kontroller, de ekte grensene 50,09 sekunder tre ganger). Tre nye funn, som er rettet:

| # | Fabel fant | Nå |
|---|---|---|
| 1 | Siste utvei ble avbestilt mens vakttråden kunne være i gang; sto den fast med låsen, hang prosessen. To linjer var fortsatt mulig. | Vakttråden sier fra før den tar låsen, siste utvei står når den er i gang, og en vakttråd som kommer etter at hovedløpet er ferdig, rører ingenting. Tre tester. |
| 2 | Et alarmsignal som alt var på vei, kunne lande i skrivingen | Behandleren kaster bare mens alarmen gjelder. |
| 3 | Årstallsvinduet sto bare i koden | Står i kontrakten og i `Docs/ScheduledEvents.md`. |

Disse tre rettelsene ble gransket av Fabel 03.10, sammen med en endring som kom til samme dag (`panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL2.md`). Fabel fant ingenting som måtte rettes før installasjon, og seks ting som burde rettes. Alle seks er tatt inn:

| # | Fabel fant | Nå |
|---|---|---|
| Bør 1 | Gikk alarmen akkurat mens den ble slått av, ble kjøringen «avbrutt av tidsgrensen» uten stempel og markører, selv om lesingen var ferdig | Alarmen slås av inne i `try`, og igjen der avbruddet fanges, så lesingene beholdes. |
| Bør 2 | Siste utvei ble avbestilt i `stop()`. Slo vakttråden inn rett etterpå og sto fast, avsluttet ingen | Siste utvei avbestilles først når hovedløpet holder sluttlåsen og er ferdig. Testen er skrevet om, og en ny test ser at ingen tidtaker står igjen etter en kjøring. |
| Bør 3 | Programmet kunne nå drepes av SIGTERM, men døde uten å rydde: låsen sto i ti minutter, og klienten ble foreldreløs | SIGTERM avslutter ordnet: klienten drepes, låsen slippes, én linje på stderr, kode 143. Stempel og markører røres ikke. Prøvd med en kjøring som stoppes midt i. |
| Bør 4 | SIGINT og SIGHUP ble også satt tilbake, uten grunn: Ctrl-C ga 20 linjer traceback, og `nohup` ble opphevet | Bare SIGTERM tas alltid over. SIGINT som er arvet som oversett, blir stående; ellers avslutter det ordnet som SIGTERM. SIGHUP røres ikke. |
| Bør 5 | Testene prøvde ikke arven over `exec`, som er veien planleggeren bruker | To tester starter programmet gjennom `/bin/sh -c 'trap "" TERM INT; exec …'`. |
| Bør 6 | Kontrakten sa ingenting om signalene | Egen rad i `contract/trinn1-2-programmer.md`, og avslutningskodene 143 og 130. |

Fabel foreslo også å føre i stempelet om SIGTERM var arvet som oversett, så det kan måles på Macen hva planleggeren gir videre. Det er gjort: `note` sier «startet med SIGTERM oversett». Bakgrunnen for endringen: planleggeren setter SIGTERM og SIGINT til oversett i sin egen prosess (`AgentMonitorShutdown` i `Sources/HavenAgentD/HavenAgentMain.swift`), og det arves av det den starter.

Fabel gransket de seks rettelsene samme dag (`panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL3.md`). Alle seks er lukket, ingenting må rettes før installasjon, og ni nye ting burde rettes: restvinduer på mikrosekunder, en test som lovet mer enn den prøvde, et hull i selvtesten og dokumentasjon. Alle ni er tatt inn:

| # | Fabel fant | Nå |
|---|---|---|
| Bør 1 | Kom det en annen feil enn ventet i lesefasen, sto alarmen på. Gikk den i oppryddingen, ble det traceback, og låsen sto i ti minutter | Alarmen slås også av i `finally`. |
| Bør 2 | Gikk alarmen akkurat mens klientens feilfil ble fjernet, ble en ferdig lesing kastet | Det kallet er dekket på samme måte som lukkingen. |
| Bør 3 | Landet et signal i en av tidtakertrådene, kunne avslutningen komme inntil tolv sekunder for sent | Signalene er blokkert i tidtakertrådene, så de lander i hovedtråden. |
| Bør 4 | Et SIGTERM mellom opprettelsen av låsfila og merket «holdt» lot låsfila stå | Merket settes rett etter at fila er laget. |
| Bør 5 | Et verktøy der `required` ikke er en liste, ga `TypeError` | «Annen kontrakt», med vanlig melding. Test. |
| Bør 6 | En test het at SIGINT avslutter kjøringen ordnet, men sendte aldri SIGINT | Ny test som sender SIGINT midt i en kjøring og ser kode 130, én linje, låsen sluppet og klienten drept. |
| Bør 7 | Selvtesten prøvde ikke signalene, og selvtesten er det eneste som kjøres på Macen før installasjon | Selvtesten prøver SIGTERM midt i en kjøring og merknaden i stempelet, gjennom `/bin/sh` med `exec`. 126 kontroller. |
| Bør 8 | Den dokumenterte testkommandoen la `__pycache__` i arbeidstreet | Kommandoene har `-B`. |
| Bør 9 | Merknaden om arvet SIGTERM sto sist i `note` og kunne kuttes bort | Står først. Test. |

Etter denne runden er de 42 testene grønne på Python 3.9.23, 3.11.15 og 3.13.13 på Linux, og selvtesten gir 126 kontroller på omtrent fjorten sekunder. **Disse ni rettelsene er ikke gransket av Fabel etterpå.** Fem av dem er Fabels egen patch, som Fabel prøvde i sin kopi; de fire andre (Bør 5, 6, 8 og 9) er skrevet av Losen.

Det Fabel ikke kunne kontrollere, og som måles på Macen: at `/usr/bin/python3` er 3.9 eller nyere, planleggerens miljø under launchd, hva binæren fra 16.08 kaller verktøyet og om den tar `--root`, hvor `--config <kandidat>` legger `State/`, og svaret fra `GET /challenges`. De fire første måles i tørrkjøringen av installasjonen. Det siste ble målt 02.10 kl. 12:24Z (jobb 253), etter at første forsøk ga 401 fordi tokenet ble sendt i feil form.

## Endret da koden for trinn 3 ble skrevet (03.10)

Koden for trinn 3 (AP5, AP6 og filene til AP7) ble skrevet i skyen 03.10 mens G2 ventet. Ingenting er lagt i noe repo. Swift lot seg bygge der likevel: Ubuntu-arkivet har Swift 6.2.3, og pakkene kan pakkes ut uten å installeres. Private avhengigheter kan ikke hentes, så bare `HavenMacAutomation` og de filene i `HavenAgentRuntime` som klarer seg med Foundation, er bygget, med stedfortredere for tre typer. macOS-grenene i koden er aldri kompilert.

Dette er presisert i `contract/trinn3-cron.md` etter at koden ble skrevet:

| Hva | Kontrakten sa | Nå | Hvorfor |
|---|---|---|---|
| Felt i tilstanden | `lastOccurrence`, `missedCount`, `missedSince`, `lastOutcome`, `lastExitCode`, `lastLog`, `attention` | i tillegg `currentRun`, `missedLatest`, `countingFrom`, `scheduleSignature` | Uten dem kan arbeideren ikke vite hva som ble avbrutt, hvilket passert tidspunkt saken gjelder, eller hva som skal telles etter at uttrykket er endret. |
| `firstFireAt` med cron | ikke nevnt | holder hendelsen tilbake | Feltet står i `config.json` uansett, for eldre agenter. |
| Første kjøring på intervall | telte hele intervaller siden `firstFireAt` | teller ingenting | Fristvarselet ville ellers gitt en sak om passering første gang det kjørte med ny tilstandsmappe. |
| Arbeideren stoppes | ikke nevnt | tar ikke flere tidspunkt; det som var forfalt, står | Ellers ble neste forfalte hendelse startet og drept, og fikk en falsk sak. |
| Tilstandsfila | én skriver | lås på fila; uleselig fil skrives på nytt av arbeideren | `schedule-stop` og arbeideren skriver begge. |
| Styringsfila | pause og fortsett | uleselig fil og `stopped` gir «kjøres ikke» med grunn i `lastError`; `changedAt` fram i tid leses som nå | Ukjent betyr nei. |
| Loggmappen | `Logs/ScheduledJobs/<id>/` | det samme når agenten oppgir mappen; ellers `State/ScheduledJobs/Logs/<id>/` | Tjenesten kjenner bare tilstandsfila når den brukes uten agentens stier, som i testene. |
| Plisten | `install-agent-dev.sh` installerer den | skriver den bare når det ikke ligger en der | En plist som finnes, skal ikke overskrives av en installasjon. |

## Fabels gransking av koden for trinn 3 (`panel/FABEL_KODE_TRINN3.md`)

Fabel bygget koden i sin egen kopi, kjørte de 54 testene, skrev ti egne (fem av dem røde), og prøvde `CronSchedule` mot referansen på 1000 tilfeldige uttrykk i 16 tidssoner uten avvik.

| # | Fabel fant | Nå |
|---|---|---|
| Må 1 | Ble arbeideren stoppet midt i en runde, tok den tidspunktet til neste forfalte hendelse, startet programmet og drepte det. Falsk sak | Arbeideren tar ikke flere tidspunkt når den er bedt om å stoppe, og gir tilbake et tidspunkt den var i ferd med å ta. Kjøreren starter ingenting for en oppgave som alt er avbrutt. Test. |
| Må 2 | Ble tilstandsfila uleselig mens arbeideren gikk, sto planleggeren stille for alltid mens livstegnet fortsatte | Arbeideren skriver fila på nytt fra det den har, og sier fra på stderr. Kan den ikke skrive, holder den livstegnet tilbake etter tre runder. Test. |
| Må 3 | Første kjøring på intervall telte alle intervaller siden `firstFireAt` som passerte | Teller ingenting første gang. Test. |
| Bør 1 | En post uten `countingFrom`, tatt opp fra fila, kjørte aldri igjen | Slike poster regnes fra da arbeideren ser dem. Test. |
| Bør 2 | `changedAt` fram i tid ga et tatt tidspunkt fram i tid | Leses som nå. Test. |
| Bør 3 | Etter en avbrutt kjøring sto sammendrag og logg fra kjøringen før | Sammendraget fjernes, og loggen er den avbrutte kjøringens når den finnes. Test. |
| Bør 4 | Siste SIGKILL til gruppen ble sendt også når gruppen var tom; ingen vakt mot prosess-ID 1 eller lavere | Sendes bare når gruppen står; vakt lagt inn. |
| Bør 5 | Bare seks signaler ble satt til standard i programmet | Alle som kan settes. Test med SIGUSR1. |
| Bør 6 | Testene med ekte programmer delte et tak på et halvt sekund | Taket er 20 sekunder, og 2 sekunder i testen der et program skal henge. |
| Bør 7 | Tester manglet for funnene, for stopp etter avbrutt kjøring, og for at tallene i kontrakten er standardverdiene | Lagt til. 65 tester. |
| Bør 8 | Styringsfil med `stopped` for en fast hendelse stanset den uten å si noe | Kjøres ikke, og `lastError` sier hvorfor. Test. |
| Bør 9, 10, 11, 14 | Kontrakten og dokumentet sa ikke hva som skjer med uleselig styringsfil, id-er som ikke kan være filnavn, navn under `Etc/`, taket på 10 000 og plisten | Skrevet inn i `contract/trinn3-cron.md` og `Docs/ScheduledEvents.md`. |
| Bør 12 | `timeZone` uten `cron` ble godtatt stille | Avvises. Test. |
| Bør 13 | `stopEvent` i arbeiderens egen prosess kunne miste det som ikke var lagret | Bare den ene posten tas inn fra fila. |
| Bør 15 | På Linux arver programmet åpne filer fra arbeideren | Gjelder ikke macOS, der alt utenom inn, ut og feil lukkes. Ikke endret. |

Etter rettelsene var 65 tester grønne på Linux elleve ganger på rad (i rekkefølge, parallelt og med maskinen holdt travel).

Fabel gransket rettelsene samme dag (`panel/FABEL_KODE_TRINN3_ETTERKONTROLL.md`), med 18 egne tester, og tok rettelsene bort igjen i en kopi for å se at de nye testene da ble røde (10 av 12 ble det; de to som ikke ble det, skulle ikke bli det). De tre «må» er lukket, ingenting nytt må rettes, og åtte nye ting burde rettes eller avklares. Alle åtte er tatt inn:

| # | Fabel fant | Nå |
|---|---|---|
| 1 | Et restvindu: ble arbeideren bedt om å stoppe etter at tidspunktet var skrevet og før programmet fantes, sto det som en avbrutt kjøring med sak, selv om ingenting var startet | Kjøreren skiller «ikke startet» (`notStarted`) fra «startet og stoppet» (`interrupted`), og ser etter to ganger før programmet finnes. Arbeideren gir da tidspunktet tilbake. To tester. Ett tilfelle står igjen og er skrevet inn i kontrakten: arbeideren drepes med SIGKILL mellom skrivingen og tilbakegivingen. |
| 2 | «Etter tre runder» var egentlig «etter tre skrivinger som feiler på rad»; med tre forfalte hendelser ble livstegnet holdt etter én runde | Teksten sier det koden gjør, i kode, dokument og kontrakt. Oppførselen er ikke endret. |
| 3 | Første kjøring på intervall fikk `lastOccurrence` lik `firstFireAt`, som kan ligge dager tilbake. En sak om en første kjøring som feilet, ville pekt fire døgn tilbake | Tar det siste tidspunktet på intervallet som er kommet, og teller fortsatt ingenting. Test. |
| 4 | En tilstandsfil med en verdi denne agenten ikke kjenner i `lastOutcome` eller `attention.kind`, er uleselig for den, og kontrakten nevnte det ikke | Kontrakten lukker de to feltene på samme måte som `status`, og sier at jobbene i trinn 4 har sin egen tilstandsfil med egne verdier. En test holder oppførselen fast. Dekodingen er ikke gjort romsligere: en ukjent verdi skal ikke gjettes om til «feilet». |
| 5 | Kontrakten manglet at første tegn i en id må være en bokstav eller et siffer | Skrevet inn. |
| 6 | Dokumentet kunne leses som «en feil uten tidssone» | «An error without `cron`». |
| 7 | Dokumentet sa ikke hvordan man kommer videre når arbeideren nekter å starte på en uleselig tilstandsfil | Arbeideren sier nå hvilken fil det gjelder, og at den må flyttes til side (før kom bare den generelle dekodingsfeilen, uten filnavn). Dokumentet har et eget avsnitt om hva som skjer med hver type hendelse når fila flyttes. En test holder fast at arbeideren nekter, hva den sier, at fila ikke skrives over, og hvert punkt i lista (cron, intervall, engang, antall, pause, stoppet, og at loggene står). At launchd starter arbeideren igjen, og at livstegnet uteblir så lenge, er lest av koden og plistmalen og ikke prøvd. |
| 8 | En hendelse som ble stoppet mens en kjøring var avbrutt, fikk en sak «Planlagt jobb feilet», og kontrakten sa ikke om det var meningen | **En stoppet hendelse ber ikke om noe.** `schedule-stop` fjerner `attention`, og en stoppet post får aldri en ny. `lastOutcome` og `lastError` står. Begrunnelse: en sak om feil forsvinner ellers først når en kjøring lykkes, og en stoppet hendelse kjører aldri igjen, så saken ville stått for alltid. Tre tester. Dette er et valg Losen har tatt; sier Kjetil at en stoppet jobb som feilet sist skal gi en sak, er det en liten endring: to linjer i `ScheduledEventService.swift`, og tre tester som snus. |

Etter denne runden er 71 tester grønne på Linux ti ganger (fem i rekkefølge, to parallelt, tre med maskinen holdt travel). For hver rettelse som endrer oppførsel, er rettelsen tatt bort igjen i en kopi, én om gangen, og testene som skal vokte den, ble røde hver gang, på den forventningen de er skrevet for (`trinn3/sky/mutasjon.py`; åtte endringer etter at pausen kom med). **Disse åtte rettelsene er ikke gransket av Fabel etterpå.** Det er et bevisst stopp: tre runder har gitt færre og mindre funn for hver runde (3 må og 15 bør, så 0 må og 8 bør), og det som gjenstår å vite, kan bare måles på en Mac.

Det Fabel ikke kunne kontrollere, og som må måles på en Mac eller i CI: at macOS-grenene kompilerer (`posix_spawn` med attributter, `flock`, typene som er ulike i Darwin og Glibc), at tidsgrensen står stille mens Macen sover, de ekte `ShortcutRunner` og `AppleScriptRunner` (stedfortredere er brukt), de to patchene mot `HavenAgentMain.swift` og `Scripts/install-agent-dev.sh`, og binæren fra 26.09 mot de nye filene (T10).

## Fabels kontroll av påstandene om siste runde (`panel/FABEL_PAASTANDER_SISTE_RUNDE.md`)

De 17 rettelsene i siste runde ble ikke gransket som kode. I stedet kontrollerte Fabel, som ikke hadde sett koden før, at det som står skrevet om dem, er sant: 18 punkter mot koden, pakken slik den ble levert kl. 11:00Z, kontrakten, dokumentet og statusfila. Fabel bygget koden fra pakken, kjørte de 71 Swift-testene to ganger, mutasjonsprøven (sju av sju røde, og loggene lest), selvtesten på tre Python-versjoner og de 42 Python-testene på 3.11.

Alle 18 punktene holder for koden. Ingen feil som ville gitt gal oppførsel på Macen, ble funnet i de 17 rettelsene. To formuleringer sa mer enn det var dekning for, og er rettet:

| # | Det sto | Det som er sant | Nå |
|---|---|---|---|
| 1 | «En test holder hver setning fast» om avsnittet «When the state file cannot be read» | Testen dekket nektingen, meldingen, at fila ikke skrives over, låsen, og fire av seks punkter i lista | Testen er utvidet til alle punktene i lista (også antall, pause og at loggene står), og teksten sier hva som er prøvd, og hva som bare er lest av koden. Setningen i dokumentet om kvitteringer er rettet: en kvittering har ikke noe igjen å gjelde for når tellingene begynner på null. |
| 2 | «Én linje å endre» om valget «en stoppet hendelse ber ikke om noe» | Regelen står to steder, og tre tester må snus | «To linjer», her og i `STATUS.md`. |

Fabel pekte også på to ting som manglet under «Det som ikke er bevist» i `LES_MEG.md`, og de er lagt til: `flock` mellom to prosesser er ikke prøvd (testene har begge tjenestene i én prosess), og om de ekte `ShortcutRunner` og `AppleScriptRunner` kaster `CancellationError` før programmet finnes. Gjør de det, gjelder regelen om «ikke startet» ikke for handlingene `shortcut` og `appleScript`; de to faste programmene er `localTask` og er ikke berørt.

Etter disse rettelsene er de 71 Swift-testene grønne ni ganger (fire i rekkefølge, to parallelt, tre med maskinen holdt travel), og mutasjonsprøven gir åtte røde av åtte (pausen er ny). Python-koden er ikke endret etter kontrollen. Utvidelsen av testen og de rettede setningene er ikke kontrollert av Fabel.
