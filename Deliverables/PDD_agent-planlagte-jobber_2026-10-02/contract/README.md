# Kontrakter for planlagte jobber

PDD `agent-planlagte-jobber`, G2-artefakt, 02.10.2026. Skrevet mot `origin/main` i HavenAgentD (`ea558ba`, lest 02.10). Denne mappen sier hva som skrives hvor, av hvem, og i hvilket format. Planen står i `../PLAN.md`, arbeidspakkene i `../PLAN_VEDLEGG.md`, flyten i `../dataflow.md`.

Ingenting her er bygget. Skjemaene og eksemplene er det implementasjonen og testene skal holde seg til.

## Det som brukes uendret

| Kontrakt | Hvor den er definert | Hva planlagte jobber bruker den til |
|---|---|---|
| `haven.correspondence-waiting.v1` (markør for post) | `Sources/HavenAgentRuntime/CorrespondenceWaiting.swift` | Trinn 1 og 2 skriver slike markører. Agenten som kjører i dag, viser dem uten endring. |
| `automationPolicy.localTasks` og `scheduledEvents` | `Sources/HavenMacAutomation/AutomationPolicy.swift`, `Sources/HavenAgentRuntime/ScheduledEventService.swift`, `Docs/ScheduledEvents.md` | Trinn 1 og 2 legger to faste programmer og to hendelser i `config.json`. |
| Innboksen for saker, versjon 1 | `Contracts/agent-challenge-v1.schema.json`, `Sources/HavenAgentRuntime/AgentChallenge.swift` | Trinn 4 lager saker under kilden `job` med svarene som finnes: `approve`, `reject`, `open`, `dismiss-today`. Ingen ny kilde, ingen ny svartype, ingen ny sakstype. |
| Jobbformatet i `.agent-spool` | `.agent-tools/agent_job_runner.py` i HAVEN-roten | Trinn 4 kan legge en godkjent jobbmal i køen. Køen endres ikke. |

## Det som er nytt

| Trinn | Fil her | Hva den fastsetter |
|---|---|---|
| 1–2 | `trinn1-2-programmer.md` | De to faste programmene: argumenter, hva de leser og skriver, tidsgrenser, tekstene i markørene. |
| 1–2 | `config-tillegg-trinn1-2.json` | Nøyaktig det som legges i `config.json`. Dette er det Kjetil godkjenner i G2. |
| 1–2 | `scheduled-task-stamp-v1.schema.json` | Stempelet hvert program skriver etter en kjøring. |
| 1–2 | `fixtures/markor-*.json`, `fixtures/ugyldig-*.json` | Markørene programmene skriver, og tekst de skal nekte å skrive. |
| 3 | `trinn3-cron.md`, `cron_reference.py`, `fixtures/cron-forventninger.json` | Cron-reglene, også over sommertid, som kjørbar referanse med fasit. |
| 4 | `scheduled-job-v1.schema.json` og de fire skjemaene ved siden av | Filene for en jobb en assistent har bedt om: bestilling, styring, godkjenning, kjøretilstand, kvittering. `fixtures/ScheduledJobs/` er en mappe slik den ser ut med to jobber. |
| 4 | `trinn4-jobber-og-godkjenning.md` | Reglene: hvem som skriver hvilken fil, når en jobb kjører, og hva saken viser. |
| 4 | `mcp-verktoy.json` | Verktøyene `agent.schedule.*`. |
| 4 | `saker-job.example.json` | Sakene under kilden `job`, gyldige etter `agent-challenge-v1`. |
| 5 | `trinn5-kontrollbro.md`, `scheduled-jobs-status-v1.schema.json` | Rutene menylinjen og HAVEN bruker for status, pause og stopp. |

`kontroller_kontrakt.py` validerer eksemplene mot skjemaene, sakene mot `agent-challenge-v1`, og all tekst mot regelen for hemmelighetsliknende tekst. Utdata fra siste kjøring står i `KONTROLL.txt`.

## Regler som gjelder alt her

1. **Én skriver per fil.** Tabellen i `trinn4-jobber-og-godkjenning.md` sier hvem. Ingen andre endrer fila.
2. **Hele filer, byttet på plass.** Skriv til en midlertidig fil i samme mappe og bytt navn. Den midlertidige fila skal ikke ende på `.json`, for mappene leses etter filendelse.
3. **Tekst som vises, bærer aldri noe som likner en hemmelighet.** Regelen er `AgentChallengeTextSafety.looksLikeSecret`: et ord på minst 24 tegn av bokstaver, sifre, `_` og `-` med både bokstav og siffer, eller minst 32 heksadesimale tegn. Agenten kontrollerer tittel, detalj, knappetekst og begrunnelser. Én slik tekst i en sak gjør at kontrollbroen svarer med feil på hele innboksen (`AgentControlBridgeServer.swift`, ruten `challenges`). Kontrakten her er strengere enn koden og gjelder også «Gjelder»: enhets-ID-er, sjekksummer og meldings-ID-er står aldri i noe felt som vises.
4. **En eldre agent skal tåle det nye.** Nye felt er valgfrie. Nye filer ligger i en egen mappe en eldre agent ikke leser. Det som står i `config.json`, skal kunne leses av agenten fra 26.09.
5. **Ukjent betyr nei.** En jobb som ikke kan leses, ikke er godkjent, eller peker på en handling policyen ikke har, kjøres ikke. Den blir en sak, ikke en stille feil.

## Hvor dette havner i repoet

Skjemaene flyttes til `Contracts/` i HavenAgentD når trinnet de hører til, bygges, med ett `.schema.json` og ett `.example.json` per kontrakt, slik `Contracts/README.md` krever. Referansen for cron blir testdata under `Tests/HavenAgentRuntimeTests/Fixtures/`.

## To ting som ble oppdaget da kontrakten ble skrevet

Begge er målt mot kilden 02.10, og begge er tatt inn i planen.

- **Korrespondanseklienten som er installert, er ikke den som ligger på `main`.** Binæren i `~/Library/Application Support/HAVEN/AssistantCorrespondence/bin/` er pilotklienten fra 16.08. `Sources/HavenCorrespondenceMCP` på `main` er en ny klient der hvert verktøy krever `relationshipID`. Sjekkprogrammet i trinn 1 er skrevet mot pilotklienten. Det spør klienten hvilke verktøy den har, og skriver en feilmarkør hvis kontrakten er en annen enn ventet. Når den nye klienten tas i bruk, må programmet oppdateres.
- **Kilden `job` var satt av til AgentJobs-køen** (`AgentChallenge.swift` linje 21–23). Den har fortsatt ingen leverandør. Planlagte jobber deler kilden, og sakene får ID-er som begynner med `job:scheduled:`. Får AgentJobs egne saker senere, bruker de et annet prefiks, og én leverandør slår dem sammen, for en kilde kan bare stå én gang i innboksen.
