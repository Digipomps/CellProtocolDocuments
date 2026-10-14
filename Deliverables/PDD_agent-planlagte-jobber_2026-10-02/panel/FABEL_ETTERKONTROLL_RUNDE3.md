# Fabel: etterkontroll av runde 3, «planlagte jobber i HavenAgentD»

Etterkontroll 02.10.2026 av en uavhengig Claude-tråd («Fabel»). Teksten under er Fabels svar, uendret.

---

# Fabel, etterkontroll av runde 3 (02.10.2026)

Kildestier er relative til `HavenAgentD/.worktrees/main-20260922/`. Utilgjengelig, derfor `[ikke belagt]`: `AdminWindow`, `ChallengeNotifier`, `CorrespondenceWaiting.swift` (bare Losens gjengivelse) og klientens listeverktøy.

## 1. De ti punktene

**Konklusjon:** Sju er løst (2, 3, 4, 7, 8, 9, 10), to delvis (1, 6), og ett er åpent byttet ut med noe annet (5); vedleggstabellen holder, unntatt at rad 5 er en erstatning og rad 6 overdriver.

- **1 delvis.** Betydning og kvitteringsfølge står [belagt: FORMAALSSPEC.md:80; PLAN.md:96], alternativet er lagt bort [belagt: PLAN.md:113]. Men feilmarkørene `sjekk-feilet`/`sjekk-stoppet` [belagt: PLAN_VEDLEGG.md:13-14] får samme tittel «Post fra … venter på svar» (`asChallenge()` gir alltid den, etter Losens måling); planen sier ikke at en feil vil se ut som post [belagt: PLAN.md:82].
- **2 løst** [belagt: PLAN.md:76-82; FORMAALSSPEC.md:59, 149].
- **3 løst** [belagt: PLAN_VEDLEGG.md:14-15]; `schedule-list` validerer uten å skrive [belagt: HavenAgentMain.swift:350-363].
- **4 løst** [belagt: PLAN_VEDLEGG.md:13; FORMAALSSPEC.md:149]; hva `from` blir uten `--navn`-treff, står ikke.
- **5 byttet ut.** F5 er omdøpt, men T4 beviser «bare godkjent innhold kjører», ikke «det Kjetil har godkjent» (se 2). Maler i policyen er avvist med åpen begrunnelse [belagt: PLAN_VEDLEGG.md:36].
- **6 delvis.** Relativ sti, `gh api`-merge og skriptet som endrer konfigurasjonen står [belagt: PLAN.md:54-60]; at samme vei kan gi selve trykket, står ikke.
- **7 løst** [belagt: PLAN.md:37, 71, 105].
- **8 løst** [belagt: PLAN_VEDLEGG.md:18; FORMAALSSPEC.md:110, 151]; mangler at tilbakerulling stanser cron-jobbene og fristvarselet (flyttet til spec-fil i AP7).
- **9 løst** [belagt: PLAN_VEDLEGG.md:21, 24].
- **10 i hovedsak løst** [belagt: PLAN.md:20-41, 84-100]; «Hva du avgjør nå» er spredt over PLAN.md:84-100 og FORMAALSSPEC.md:155-156.

## 2. Ett trykk i menylinjen (E2, AP8–AP10, F5)

**Konklusjon:** Den installerte menyappen kan vise saken og sende svaret, men viser bare tittel og undertittel, dagens daemon avviser svaret, og trykket kan gis av enhver prosess som kjører som Kjetil — E2 stenger MCP-veien, ikke Losen.

- **Visning.** `job`, `intent-approval` og svarene finnes [belagt: AgentChallenge.swift:23, 34, 83-88]; raden blir en undermeny med undertittel og én knapp per svar [belagt: MenuPresentation.swift:106-113; HavenAgentMenuApp.swift:76-92]. `detail` vises aldri i menyen [belagt: MenuPresentation.swift:31-45], så «nøyaktig det innholdet han så» [belagt: FORMAALSSPEC.md:62] er 80 tegn tittel pluss «Losen · job · …»; jobbmalen ser han ikke. «Åpne» åpner adminvinduet [belagt: HavenAgentMenuApp.swift:85-86]; at det viser jobben, er [ikke belagt] — må det endres, trenger trinn 4 ny menyapp likevel.
- **Svar.** Dagens `responseHandler` godtar bare `intent-review:` og tool-link; alt annet får `answeredVia: "ingen"` [belagt: AgentChallengeWiring.swift:200-207; Docs/AgentMenylinje.md:60-63]. AP9 forutsetter en ny gren der uten å nevne det [belagt: PLAN_VEDLEGG.md:21].
- **Omgåelse.** Godkjenningen er en fil under `State/` og et POST på loopback. Token leses fra `config.json` av menyappen [belagt: AgentBridgeClient.swift:84-89] og av MCP-serveren [belagt: HavenAgentMCPService.swift:1088-1104]; `reviewer` er fri tekst [belagt: AgentChallengeWiring.swift:198]. En `swift test`-jobb eller et `.sh` i `_handoff/` kjører som Kjetil [belagt: PLAN.md:54-55] og kan skrive `<id>.approval.json` eller sende svaret selv. Mønsteret finnes alt: `agent.review.approve` lar MCP godkjenne intenter som `mcp-operator` [belagt: HavenAgentMCPService.swift:473-478, 1047-1056]. Et varselbanner gir også «ett trykk» [belagt: AgentMenuModel.swift:40-42; Docs/AgentMenylinje.md:66-73].
- **Ærlighet.** PLAN.md:60 sier kø-kode «kan gjøre det samme som du kan», men PLAN.md:50 og E2 («fjerner det» [belagt: FORMAALSSPEC.md:76]) framstiller trykket som absolutt.
- **Felle.** Tittel eller detalj med ID-liknende streng (jobb-ID, sjekksum, `planlagte-jobber-20261002`) gjør hele innboksen `malformed` [belagt: AgentChallenge.swift:154-184, 249-254; AgentBridgeClient.swift:138-142]; T4/T6 tester det ikke for jobbsaker.

## 3. PLAN.md lest som Kjetil

**Konklusjon:** Hva han får, rekkefølgen, hva han gjør og hva som kan stanse det, er klart nå; «når» er rekkefølge uten tid, og fire løfter bærer kildene ikke.

- **Klart:** trinntabellen og «ikke cron før trinn 3» [belagt: PLAN.md:22-32], stopperne [34-41], tallene [100], diff før konfigurasjonsendring [86].
- **Uklart:** ingen datoer, og disk-ryddingen har ingen eier [belagt: PLAN.md:36]; «kl. 09:00 … også 25.10» [71] forutsetter trinn 3 installert før 25.10. «Sier om køjobber skal slås på» [72] skjuler at Losens skript skriver `scheduledJobs.spoolInbox` [belagt: PLAN_VEDLEGG.md:22]. `gh` fra køen «måles» [40], men målingene som finnes, sier nei: løperen arver launchd-PATH, godtar bare `HAVEN_*`-miljø og bare programnavnet `gh` [belagt: job-245:174-182, 260-266; job-246:423-432, 459-466], og `gh` ligger i `/opt/homebrew/bin`. Ordlista mangler `_losen-queue`, HD-0156/PR #25/Codex, CI, merge/gren/arbeidstre, G1-GUI/G3, kontrollbroen, sjekksum og profilnavnene.
- **Ikke båret:** (a) «ett trykk … nøyaktig det du så» [50], se 2; (b) «programmene passer på hverandre» [81] — døgnprogrammet ser 30-minuttssjekken død først neste morgen, og meldingen heter «Post fra … venter på svar»; (c) oversiktsbildet lover «Du ser utfallet i menylinjen» i flyten «fra trinn 4», mens utfall i menyen er trinn 5 [belagt: PLAN_VEDLEGG.md:24-25]; (d) «forsvinner når Losen har … kvittert» [69] krever at listeverktøyet viser `acknowledgedAt` [ikke belagt]. HD-0069s to godkjenninger bes fortsatt ikke om [belagt: PLAN.md:107].

## 4. Menybildene

**Konklusjon:** Ingenting i de fem bildene er umulig for den native menyen — tekst, skillelinjer, undermeny og knapper er det den alt bruker [belagt: HavenAgentMenuApp.swift:33, 71-110], og undermeny i undermeny er standard NSMenu [ikke belagt i kildene] — men to undertitler og én tittel stemmer ikke med hvordan de bygges.

- Undertittel = `[displayName] · kilde · [subject]` [belagt: MenuPresentation.swift:178-184]. Godkjenning-v2 stemmer hvis `displayName` er «Losen» og `subject` er tidsteksten; feil-v2 bare hvis `subject` er «kl. 09:00 · programmet ga status 1» — `subject` er i dag en handlings-ID [belagt: AgentChallengeWiring.swift:34], men filtreres ikke, så det er trygt. Post-ulest-v2 krever at `asChallenge()` setter `requestedBy` og `subject`; Losens gjengivelse nevner ingen av dem [ikke belagt] — ellers står det bare «correspondence».
- Planleggeren-står-v2: AP12 sier kilden blir `unreadable` [belagt: PLAN_VEDLEGG.md:24]; da lager daemonen «Får ikke lest job» med undertittel «agent-health» [belagt: ChallengeInboxService.swift:112-132; MenuPresentation.swift:178-184], ikke «Planleggeren går ikke» / «job · siste livstegn …». Bildet og AP12 beskriver to mekanismer.
- Ro-v2: «Sist lest 13:42» er ISO-8601 i UTC i koden, og ok-tilstanden har raden «Ingenting venter — 5 av 6 kilder lest», som bildet mangler [belagt: MenuPresentation.swift:131-144; HavenAgentMenuApp.swift:94]; AP13 nevner ikke endringen. Godkjenning-v2 og feil-v2 viser «Åpne», som AP9/AP12 ikke lister [belagt: PLAN_VEDLEGG.md:21, 24]. Ikon, tall og overskrift stemmer [belagt: HavenAgentMenuApp.swift:49-63; AgentChallenge.swift:438-447].

## Må fortsatt endres før Kjetil får dette

1. F5, E2 og PLAN.md:50: trykket stenger MCP-veien; kø-kode kan gi trykket selv; ingen MCP-verktøy får godkjenne (T5 beviser det), og daemonen kan ikke skille menyappen fra andre med token.
2. Hva Kjetil ser før han trykker: jobbmalen inn i saken (under 400 tegn, uten ID-strenger), eller si at adminvinduet må bygges om — og at trinn 4 da trenger ny menyapp.
3. AP9: `responseHandler` får en `job:`-gren; T4/T6 tester at jobbsaker ikke gjør innboksen `malformed`.
4. Trinn 1–2: si at feilmarkører vises som «Post fra … venter på svar», og velg `from` deretter.
5. Planleggeren-står-bildet rettes til AP12 (eller omvendt); post-ulest-undertittelen bekreftes mot `CorrespondenceWaiting.swift`.
6. «Når»: dato eller «ukjent, fordi …» per trinn, og en eier for disk-ryddingen.
7. `gh` fra køen: skriv «virker trolig ikke» med grunn, og hva skript-veien i `_losen-queue` koster.
8. Ordlista utvides.

## Kan stå

- Punkt 2, 3, 4, 7, 8, 9 og språkgrepene (trinntabell, stoppere, tall, diff før endring).
- Rekkefølgen 0→1→2→3, nå som planen sier at 1–2 ikke er cron.
- Bildenes form og native menystil.
- E6-betydningen av markøren, med kvitteringsfølgen.
- Tilbakerullingsregelen (AP6/T10), pluss én setning om at cron-jobber og fristvarsel da står stille.
