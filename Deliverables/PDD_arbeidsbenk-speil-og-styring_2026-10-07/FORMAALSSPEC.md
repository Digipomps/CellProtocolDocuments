# Formålsspesifikasjon — arbeidsbenken speiler og styrer agentene

Oppgavemappe: `PDD_arbeidsbenk-speil-og-styring_2026-10-07` · Opprettet 2026-10-07 22:55Z · Iterasjon 1
Skrevet av Losen (prosjekttråden). Last verified against code: 2026-10-07 (CellScaffold `origin/main` 381094bb, HavenAgentD `origin/main` ea558ba).

> Portene i natt er **delegert**: Kjetil valgte 22:32Z «Helt til staging» på kortet «Hvor langt kan jeg gå med arbeidsbenkene i natt uten å spørre deg?». Kortets tekst: «Jeg godkjenner designbilder selv mot dine kjente valg, bygger, tester og setter ut på staging i natt. Prod får ingenting, og du ser alt i morgen.» Det er ikke Kjetils G1/G1-GUI/G2 på dette dokumentet; han ser det i morgen og kan forkaste alt.

## 0. Intensjon (ordrett) og brief-audit

> «Bruk ledig kapasitet til å populere og forbedre admin og utvikler arbeidsbenkene. Jeg vil at alt vi gjør her - Claude Desktop, ChatGPT/Codex og muligheter for andre - både gjenspeiles og kan styres. Vurder flatene ut ifra brukervennlighet - og bruker effektivitet - i tillegg til å få det til å virke og se pent ut. Sørg for å unngå å måtte hente tillatelser utover natten så du stopper opp. Hent inn eventuelle tillatelser nå før jeg legger meg.» (Kjetil, 07.10 22:31Z)

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Developer Workbench har en flate for agentkjøringer | retrieved: seksjonen «Agentkjøringer» (`AgentRunWorkbenchConfiguration.swift`) settes inn i HAVEN Workbench; ingen kontroll-handling | CellScaffold `Sources/App/Cells/WorkItems/AgentRunWorkbenchConfiguration.swift`, `AgentRunCell.swift:12-45` |
| Flaten viser noe i dag | contradicted (uten måling i staging): ingenting mater `agentRun.observe`; ingen kilde i HAVEN kaller den | `git grep agentRun.observe` i CellScaffold og HavenAgentD, 07.10 |
| Agentene på Mac-en kan skrive til arbeidsbenken | retrieved: HavenAgentD har `agent.workbench.call` (state, query, capture, setStatus, setPriority, addEvidence, addRelation, addComment) via `POST /commands/workbench` → bro til staging | HavenAgentD `Sources/HavenAgentRuntime/WorkbenchConnection.swift`, `AgentControlBridgeServer.swift:52` |
| …og at den forbindelsen virker | contradicted: hvert kall siden 03.10 gir `unavailable`, også 22:42Z i kveld; konfigen tillater bare `state`/`query` | `HAVEN-Deploy/_handoff/ARBEIDSBENK/PROEVE-WORKBENCH-BRO-2-20261007.md`, `AGENTD-LOGG-2-20261007.md`, `AGENTD-KONFIG-20261007.md` |
| Kjetil klikker på beslutningskortene i staging | contradicted: 13 kort `losen-beslutning-*`, ingen klikk 15:12Z–21:36Z; svarene kom i chat og på kort i prosjektchatten | `_losen-queue/KOORDINERING.md` 18:07Z, 18:57Z, 21:36Z |
| Styring av kjøring finnes | retrieved (delvis): AgentD har signerte remote intents med review (`RemoteIntentInboxCell`/`intent-review`) og `GET /challenges` («alt som venter på et menneske»); Workbench har ingen styring (`executionControlNames` er bevisst utelatt) | `AgentControlBridgeServer.swift:96-`, `AgentRunCell.swift:38-44`, `workbench-1.0/WO-5-agent-run-control.md` §5.3 |
| Losen-køen (Codex + skript, baner a–d) er det mest av nattens arbeid kjører i | retrieved: `_losen-queue/` inbox*/running/done, `logs/runner.log` | `_losen-queue/LES_MEG.md` |
| Utviklerverktøy skal ikke deployes til verten | retrieved (Kjetils regel 09.09, HD-0023) | AGENTS.md § Rolle; minne `loggforing-og-verktoyscope` |
| Godkjenninger i arbeidsbenken er spesifisert | retrieved: b43 G1-spec, ikke godkjent | `PDD_godkjenninger-i-arbeidsbenken_2026-10-07/FORMAALSSPEC.md` |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.arbeidsbenk.root` | Kjetil ser og styrer agentarbeidet fra ett sted | — | Han åpner arbeidsbenken og vet på under ett minutt hva som venter på ham, hva som kjører og hva som er levert | T7 (måling i staging) | candidate |
| `…arbeidsbenk.trenger-deg` | «Trenger deg» øverst | root | Beslutninger til Kjetil står først, hver med hva et ja utløser, anbefaling og Ja/Nei på samme rad | T3, T4 | candidate |
| `…arbeidsbenk.speil` | Speil av alle agenter | root | Kø-jobber (Codex/skript, bane), Codex- og Claude-økter og AgentD-jobber vises med kilde, tilstand og tid, maks 3 min gamle | T2, T5 | candidate |
| `…arbeidsbenk.bro` | AgentD når arbeidsbenken | speil | `agent.workbench.call state` mot kjetil2s celle svarer 200 med `items` | T1 | candidate |
| `…arbeidsbenk.styring` | Styring som virker tilbake | root | Ja/Nei på et kort, og «Hold»/«Slipp» på en kø-jobb, gir effekt på Mac-en innen 3 min, med kvittering på kortet | T6 | candidate |
| `…arbeidsbenk.admin-utgivelse` | Utgivelser i Admin | root | Admin viser staging/prod-revisjon, siste kvittering og hva neste steg venter på | T3 | candidate |

## 2. Avgrensning og avhengigheter

Ikke: prod; nye skjelett-elementtyper; deploy av statusprojeksjon/feed/menylinje til verten (feeden kjører på Mac-en og skriver gjennom broen som Kjetils agent); styring som starter prod eller merger uten Kjetils ord (prod-ja forblir i chat, b43 del 9); lesing av samtaleinnhold fra Claude/Codex (bare metadata: tittel/id, tilstand, tid).

| Avhengighet | Kilde | Verifier | Målt før G1 |
|---|---|---|---|
| AgentD → staging Workbench-bro | HavenAgentD WorkbenchConnection | T1 | **rød**: `unavailable` siden 03.10 (d180 diagnoserer) |
| AgentDs identitet har grant på kjetil2s WorkItem-celle | WorkbenchAccessGrant | T1 skriving | ikke målt |
| Release-kjeden til staging | `RELEASE/wp-rel-*.sh` | c57 | 2026.9.7 i gang (c57) |
| Developer Workbench laster i staging | GUI-akseptanse 2026.9.6 | lastetid | grønn 06.10 (Safari) |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse |
|---|---|---|---|
| Developer Workbench med «Trenger deg», «Kjører nå», «I kø», «Levert siste døgn» | bilde (fylt, tom) | `images/` | `utviklerbenk-fylt-v1.png`, `utviklerbenk-tom-v1.png` |
| Admin «Utgivelser» | bilde | `images/` | `admin-utgivelser-v1.png` |
| Diagnose og retting av AgentD-broen | fil + testutdata | `HAVEN-Deploy/_handoff/ARBEIDSBENK/` | `D180-WORKBENCH-PROBE.md` |
| Speil-feed på Mac-en | kjørende tjeneste + fil | `HAVEN-Deploy/tools/arbeidsbenk-speil/` | T2/T5 |
| Flaten i staging | kjørende flate | staging, Developer Workbench | T3, T7 |

## 4. Pakker og lærdommer

`pkg.std.everything-works`, `pkg.std.gui-surface`, `pkg.std.codex-handoff`. Relevante lærdommer: `lesson.text-ux-is-not-design` (bilder før kode), `lesson.findability-is-not-usability` (handlingene må nås: T4), `lesson.tested-a-different-path-than-production` (T5 måler gjennom samme bro som feeden), `lesson.plan-instead-of-delivery`, «ikke konkluder fra statusdokumenter» (skill, 03.10: broen ble målt i kveld, ikke lest), `lesson.mount-is-not-git`.

## 5. Avledede tester

| Id | Type | Hvordan | Bevis |
|---|---|---|---|
| T1 | command | `proeve-workbench-bro.sh state` gir HTTP 200 med `items` for `kjetil2-staging-work` | `ARBEIDSBENK/PROEVE-WORKBENCH-BRO-*.md` |
| T2 | command | feeden kjører én runde tørt og viser hvilke poster den ville skrevet (kø, økter, AgentD-jobber) | TESTRESULT.md#feed |
| T3 | inspection | skjermbilde av flaten i staging ved siden av godkjent bilde | ACCEPT.md#parity |
| T4 | command | `SkeletonReachabilityAudit`: Ja/Nei/Hold/Slipp finnes i `reachableActionKeypaths` | TESTRESULT.md#reachability |
| T5 | measurement | tid fra en kø-jobb starter til den står som «Kjører nå» i staging, tre målinger | TESTRESULT.md#latency |
| T6 | command | Ja på et testkort gir JA-fil på Mac-en og kvitteringskommentar på kortet; «Hold» gir `.hold` | TESTRESULT.md#styring |
| T7 | measurement | Kjetil (eller Losen i hans økt) finner tre ventende beslutninger på under ett minutt | ACCEPT.md |
| T0 | command | full regresjon for berørte repoer, ingen svekkede tester | TESTRESULT.md#regression |

## 6. Åpne spørsmål (endrer treet; standardvalg i natt i parentes)

1. Skal et klikk i staging telle som ja for merge/tag/G-porter, slik kortene i dag sier? (Ja for alt unntatt prod, som i STATUS-20261007 §8.)
2. Skal Hold/Slipp på kø-jobber kunne gjøres fra arbeidsbenken? (Ja; bare for jobber som ikke har startet. Stopp av en kjørende jobb tas ikke i natt.)

## 7. Iterasjoner
- 1 (22:55Z): første versjon, broen målt rød.
