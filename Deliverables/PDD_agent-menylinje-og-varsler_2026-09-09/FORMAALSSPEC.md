# Formålsspesifikasjon — agent menylinje og varsler

Oppgavemappe: `PDD_agent-menylinje-og-varsler_2026-09-09` · Opprettet 2026-09-09 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.
>
> **Merknad om rekkefølge, 2026-09-09:** Kjetil ba om «implementer det, test og vis meg imorgen» og
> la seg. G1 og G1-GUI kan ikke settes uten hans ord. Arbeidet går derfor videre parallelt med at
> denne spesifikasjonen ligger til godkjenning, slik at han i morgen har både formålene å godkjenne
> **og** noe kjørende å se på. Portene står `venter` i STATUS.md til han sier noe annet, og det som
> er bygget måles mot §3 når han har sagt sitt. Blir §1 endret, er koden det som viker.

## 0. Intensjon (ordrett) og brief-audit

> Ok - jeg har sagt kanskje her kanskje en annen tråd at jeg vil ha en menylinjeitem med status på hva som skjer i HAVENAgentD - med mulighet for å åpne en full adminflate der. Og jeg vil at challenges for å gi tilgang eller topup, eller noe annet som trenger brukerns oppmetksomhet og interaksjon dukker opp som notifikations i macos notifications liste - kan gøre det samme med de andre apple os'ene også. Implementer det, test og vis meg imorgen

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «HAVENAgentD» finnes og kjører hos Kjetil | **retrieved** — SwiftPM-pakke, macOS 13+, tre kjørbare (`haven-agentd`, `haven-agentd-mcp`, `haven-correspondence-mcp`) | `HavenAgentD::Package.swift` |
| Agenten kjører som en brukerprosess, ikke systemdaemon | **retrieved** — LaunchAgent med `RunAtLoad`, `KeepAlive`, `ProcessType Interactive` | `HavenAgentD::Launchd/io.digipomps.haven.agentd.plist` |
| Det finnes et menylinjeitem i dag | **contradicted** — ingen treff på `NSStatusItem`, `MenuBarExtra`, `UNUserNotification` eller `NSUserNotification` i hele repoet | grep over `HavenAgentD::Sources`, `Packaging`, `Docs` |
| Det finnes «en full adminflate der» i dag | **contradicted for «admin»** — flaten som finnes er *onboarding*, ikke administrasjon: `GET /onboard` serverer «HAVEN Agent Onboarding» | `HavenAgentD::Sources/HavenAgentCellRuntime/Resources/Onboarding/index.html`, `AgentControlBridgeServer.swift:35` |
| Agenten har allerede en lokal flate å hente status fra | **retrieved** — lokal kontrollbro på `127.0.0.1:43110`, tokenautentisert (`?token=`), med `GET /health`, `GET /onboard/status.json`, POST-kommandoer og WebSocket `/bridgehead/:route/:id` | `AgentControlBridgeServer.swift`, `AgentConfig.swift:150` |
| Det finnes allerede en rik statusstruktur | **retrieved** — `AgentStatusReport` med binary, sprout, identity, config, provisioning, controlBridge og `nextSteps` | `HavenAgentD::Sources/HavenAgentRuntime/StatusService.swift:90` |
| «Challenges» finnes som begrep i agenten | **retrieved, men uten samlet inngang** — operatørgodkjenning finnes som CLI: `review-state`, `review-approve --intent-id`, `review-reject --intent-id`; broen har rutene `intent-inbox` og `intent-review` («Operator review boundary for verified intents»). Det finnes **ingen ett samlet «dette venter på deg»-endepunkt** | `HavenAgentMain.swift:643–672`, `AgentConfig.swift:164–173` |
| Jobber som venter på godkjenning (`awaitingApproval`) kan brukes som challenge-kilde | **contradicted på basen** — `AgentJobModels.swift`, `JobStore.swift` og `JobCompletionService.swift` er **usporede filer** i det delte treet, ikke på `main` (`git ls-files --error-unmatch` feiler). De tilhører AgentJobs-arbeidet fra en tidligere økt som ennå ikke er landet. Kilden er derfor **ikke tilgjengelig** for denne oppgaven og er tatt ut av v1 | `git status --porcelain` i `HavenAgentD`, 2026-09-09 |
| «Topup» håndteres av agenten | **contradicted** — null treff på topup i `HavenAgentD::Sources`. Topup og tilgangsgodkjenning bor i scaffolden: `AdminFundingQueueCell` med `queryRequests`, `approveRequest`, `rejectRequest` | grep `HavenAgentD::Sources`; `CellScaffold::Sources/App/Cells/Admin/AdminFundingQueueCell.swift:43–70` |
| macOS-varsler kan sendes fra agenten i dag | **retrieved, med en viktig begrensning** — `NetworkAlertNotificationDispatcher` sender `display notification` via et fast, allowlistet AppleScript, portvakt på `notificationsEnabled` **og** et formålsfilter (`NetworkHealthPurposeCatalog.warrantsNotification`). Denne veien kan ikke bære knapper/handlinger og opptrer under skriptvertens identitet, ikke HAVENs | `HavenAgentD::Sources/HavenAgentRuntime/NetworkAlertNotificationDispatcher.swift:1–60` |
| Et varsel med handlingsknapper og et menylinjeikon kan lages uten app-bundle | **contradicted** — både `NSStatusItem`/`MenuBarExtra` og `UNUserNotificationCenter` krever en app-bundle med bundle-ID. En ren launchd-kjørbar kan ikke registrere varselkategorier eller eie et statusikon. Dette er den arkitektoniske konsekvensen hele oppgaven henger på | Apple-plattformkrav; bekreftes i WP0 ved at appen bygges som bundle |
| «De andre Apple-OS-ene» kan gjøre det samme | **unavailable som påstand om i dag** — iOS/iPadOS kan ikke kjøre agenten; de kan bare motta challenges som push, som krever APNs-oppsett og en avsender scaffolden ikke har verifisert. Se §2: eksplisitt utenfor denne oppgaven, med kravlisten skrevet ned | ingen iOS-mål i `Package.swift`; `CellScaffold::Sources/App/Cells/ConferenceMVP/Notifications/PushProviderAdapter.swift` finnes, men `notificationStatus: failed` 2026-09-08 er uoppklart |
| Kjetil har bedt om dette før («kanskje en annen tråd») | **unavailable** — ikke funnet i noen PDD-mappe i `CellProtocolDocuments::Deliverables/`. Behandles som ny bestilling; finnes en eldre tråd, er den ikke lastbærende her | søk i Deliverables |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.agent-menu.root` | Agenten er synlig og svarbar der Kjetil er | `purpose://human-agency` | Kjetil ser uten å lete hva agenten hans holder på med, og kan svare på det som venter på ham, fra menylinjen | Alle blad under er grønne | candidate |
| `purpose://candidate.agent-menu.status-at-a-glance` | Tilstand i ett blikk | `purpose://candidate.agent-menu.root` | Ikonet i menylinjen viser én av tre tilstander — i orden / trenger deg / nede — og menyen sier i klartekst hva agenten gjør nå | `test.menu.three-states` | candidate (blad) |
| `purpose://candidate.agent-menu.absence-is-explained` | Tomt er ikke det samme som stille | `purpose://candidate.agent-menu.status-at-a-glance` | Når appen ikke fikk svar, ikke har token, eller ikke har tilgang, sier flaten **det** — den viser aldri «alt i orden» eller en tom liste den ikke har dekning for | `test.menu.unknown-is-not-ok` | candidate (blad) |
| `purpose://candidate.agent-menu.admin-surface` | En faktisk adminflate å åpne | `purpose://candidate.agent-menu.root` | Ett valg i menyen åpner et vindu med hele `AgentStatusReport`, ventende challenges og lenker videre til onboarding-flaten og scaffoldens adminflate | `test.menu.admin-window-shows-report` | candidate (blad) |
| `purpose://candidate.agent-menu.challenge-inbox` | Én samlet inngang for det som venter på mennesket | `purpose://scaffold.operations` | Agenten har ett endepunkt som svarer «dette venter på deg», med kilde, hva det gjelder, når det kom, og hvilke svar som er mulige | `test.challenge.inbox-shape`, `test.challenge.sources` | candidate (blad) |
| `purpose://candidate.agent-menu.answerable-where-seen` | Svar der du ser det | `purpose://self-determination.data.exercisability` | En challenge kan besvares fra varselet eller menyen, og svaret går gjennom agentens egen godkjenningsvei (`review-approve`/`review-reject`), ikke en snarvei rundt den | `test.challenge.answer-uses-real-path` | candidate (blad) |
| `purpose://candidate.agent-menu.notification-when-needed` | Varsler når det trengs, ikke ellers | `purpose://candidate.agent-menu.root` | Challenges som trenger mennesket havner i macOS' varslingsliste med handlingsknapper; alt annet gjør det ikke | `test.notify.appears-in-center`, `test.notify.purpose-gate`, `test.notify.no-duplicates` | candidate (blad) |
| `purpose://candidate.agent-menu.no-secrets-in-notification` | Varselet lekker ingenting | `purpose://access.audit.privacy` | Varseltekst og menytekst inneholder aldri token, nøkler, signaturer eller engangshemmeligheter — bare hva det gjelder og hvem det kommer fra | `test.notify.no-secrets` | candidate (blad) |
| `purpose://quality.build-and-regression` | Bygg og regresjon | `purpose://quality` | Alle berørte mål bygger; ingen nye røde tester | `test.build`, `test.regression` | pakke |
| `purpose://quality.docs-in-same-change` | Dokumentasjon i samme endring | `purpose://quality` | Dokumentene som beskriver endret oppførsel er oppdatert og datert | `test.docs-updated` | pakke |
| `purpose://quality.work-is-visible` | Arbeidet er synlig | `purpose://quality` | STATUS.md speiler faktisk tilstand; branchen har commitene | `test.status-current`, `test.branch-has-commits` | pakke |

## 2. Avgrensning og avhengigheter

Hva dette **ikke** er:

- **Ikke iOS/iPadOS/watchOS i denne runden.** «Kan gjøre det samme» er notert som retning, ikke bestilling. Det som faktisk kreves før det kan gjøres, er skrevet ned her så det ikke må gjenoppdages: (1) en APNs-avsender med sertifikat/nøkkel eid av Digipomps, (2) en enhetstoken-registrering knyttet til entiteten, (3) en avklaring av at `notificationStatus: failed` fra 2026-09-08 ikke er et symptom på (1) eller (2), og (4) en HAVEN-app-mottaker som kan besvare challengen. Challenge-kontrakten i §1 er med vilje laget plattformnøytral, slik at iOS senere kan konsumere samme liste.
- **Ikke en ny autorisasjonsmodell.** Menylinjen viser og videresender; den utvider ingen rettigheter. En challenge Kjetil ikke har lov til å besvare, blir ikke besvarbar av at den vises.
- **Ikke scaffoldens adminflate på nytt.** Topup- og tilgangsgodkjenninger *bor* i `AdminFundingQueueCell` og på `https://staging.haven.digipomps.org/admin/funding`. Denne oppgaven henter dem fram og lenker dit; den flytter dem ikke.
- **Ikke pakking og notarisering i første runde.** Appen skal kjøre og vises i morgen. Å få den inn i `.pkg`-en med Developer ID og notarisering er egen arbeidspakke (WP8), og den er ikke akseptansekriterium for G3 med mindre Kjetil sier det.
- **Ikke endring av `NetworkAlertNotificationDispatcher`s eksisterende oppførsel.** Den nye veien legges ved siden av; nettverksvarsler fortsetter som i dag til Kjetil eventuelt vil samle dem.

Kapabiliteter og avhengigheter:

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Lokal kontrollbro svarer på `127.0.0.1:43110` med token | `AgentControlBridgeServer.swift`, `AgentConfig.swift:150` | Bare loopback; token i `~/Library/Application Support/HAVENAgent/config.json` | **Ja** — uten den har menyen ingen kilde |
| `AgentStatusReport` bygges av `StatusService` | `StatusService.swift:90` | Beskriver oppsett og helse, ikke løpende aktivitet | Ja |
| Operatørgodkjenning finnes som ekte vei | `HavenAgentMain.swift:643–672` | Gjelder verifiserte remote-intents, ikke topup | **Ja** — svarveien skal gå her, ikke rundt |
| ~~Jobber i `awaitingApproval`~~ | usporet i delt tre, ikke på `main` | **Utenfor v1.** Challenge-kontrakten får en `source`-verdi `job` som ingen produsent fyller ennå, slik at AgentJobs kan koble seg på uten kontraktsendring | Nei |
| Scaffoldens godkjenningskø | `CellScaffold::Sources/App/Cells/Admin/AdminFundingQueueCell.swift` | Krever at agentens identitet faktisk har leserett; per 2026-09-09 er `entity:digipomps`/`entity:dimy` **ikke** opprettet på staging | Nei — men da **skal** menyen si «får ikke lest», ikke vise tom liste (`lesson.test-corpus-is-not-shipped-corpus`) |
| macOS-varsler med handlinger | `UNUserNotificationCenter` | Krever app-bundle, bundle-ID og brukerens samtykke ved første kjøring | **Ja** |
| Agentens eksisterende AppleScript-varselvei | `NetworkAlertNotificationDispatcher.swift` | Ingen knapper, feil avsenderidentitet | Nei — erstattes ikke, brukes som fallback når appen ikke kjører |

## 3. Forventningskontrakt — «Det du kommer til å se»

| # | Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|---|
| L1 | Denne formålsspesifikasjonen | fil | `P FORMAALSSPEC.md` | — | nei (G1 venter) |
| L2 | Rendret bilde av menylinjen i tre tilstander + adminvinduet | bilde | `P images/` | `menu-ok-v1.png`, `menu-attention-v1.png`, `menu-down-v1.png`, `admin-window-v1.png` | nei (G1-GUI venter) |
| L3 | Challenge-kontrakt: hva en challenge er, hvilke svar som finnes | fil | `P contract/agent-challenge_v1.json` + fixtures | — | nei |
| L4 | Kode: nytt app-mål `HavenAgentMenu` + challenge-inngang i agenten, egen gren, commit per bladformål | kode | `HavenAgentD`, gren `pdd/agent-menylinje-og-varsler` | — | nei |
| L5 | Kjørende menylinjeitem på Kjetils Mac, med adminvindu | kjørende flate | menylinjen | skjermbilder i `P images/actual-*` | nei |
| L6 | Et faktisk varsel i macOS' varslingsliste, med knapper | bilde | `P images/notification-actual-v1.png` | — | nei |
| L7 | Testutdata for hver rad i §5 | fil | `P TESTRESULT.md` | — | nei |
| L8 | Akseptanse: forventning mot faktisk | fil | `P ACCEPT.md` | — | nei |

Etter G2 teller bare disse radene som fremdrift. **L5 og L6 er de to som avgjør om oppgaven er løst** — et bilde av en meny er ikke en meny, og en test som sier at et varsel ble sendt er ikke et varsel i listen.

## 4. Tilknyttede formålspakker og lærdommer

`pkg.std.everything-works` er festet (bygg, regresjon, docs i samme endring, STATUS current).

Lærdommer som direkte former denne oppgaven:

- `lesson.test-corpus-is-not-shipped-corpus` og `lesson.tested-a-different-path-than-production` → `purpose://candidate.agent-menu.absence-is-explained` og `test.challenge.answer-uses-real-path`. En grønn test på en tom liste er nøyaktig feilen som holdt Relasjoner-flaten tom i to uker.
- `lesson.text-ux-is-not-design` → L2 er bilder, ikke beskrivelser.
- `lesson.plan-instead-of-delivery` → L5/L6 er kjørende flate og faktisk varsel.
- `lesson.syntax-check-reported-as-delivered` → ingen arbeidspakke er levert før et faktisk bygg er kjørt.
- `lesson.branch-is-empty-after-eight-work-packages` → `test.branch-has-commits`, og commit-pakke etter første grønne bygg, ikke til slutt.
- `lesson.codex-workspace-write-cannot-build-cellscaffold` → bygg kjøres detached med `danger-full-access`, ikke som køjobb.
- `lesson.corr-approval-surfaces-timed-out` → §2 lister avhengighetene med verifier.

## 5. Avledede tester

| Test | Type | Hva den gjør | Bevis lander i |
|---|---|---|---|
| `test.menu.three-states` | command | Enhetstest: statusmodellen gir `ok` / `attention` / `down` for tre innmatinger (frisk rapport, rapport med ventende challenge, ingen kontakt) | `TESTRESULT.md#menu` |
| `test.menu.unknown-is-not-ok` | command | Enhetstest: manglende token, tilkoblingsfeil og 401 gir hver sin **egen** tilstand med tekst — aldri `ok`, aldri tom liste | `TESTRESULT.md#menu` |
| `test.menu.admin-window-shows-report` | inspection | Skjermbilde av adminvinduet med felt fra `AgentStatusReport` synlige, sammenlignet med `haven-agentd status` kjørt i terminal samme minutt | `TESTRESULT.md#admin` |
| `test.challenge.inbox-shape` | command | Enhetstest mot `contract/agent-challenge_v1.json`: påkrevde felt, ukjent kilde avvises, ugyldig svaralternativ avvises | `TESTRESULT.md#challenge` |
| `test.challenge.sources` | command | Hver kilde i v1 (intent-review, scaffold-kø, agentens egen helse) gir en challenge med riktig `source`; en kilde som ikke kan leses gir `unreadable` med grunn, ikke ingenting. `job` er deklarert i kontrakten uten produsent og skal gi tom, ikke feil | `TESTRESULT.md#challenge` |
| `test.challenge.answer-uses-real-path` | command | Godkjenning fra menyen ender i `RemoteIntentReview`s egen godkjenningsfunksjon — samme kodevei som `haven-agentd review-approve` — verifisert ved at intentens tilstand faktisk endres | `TESTRESULT.md#challenge` |
| `test.notify.appears-in-center` | inspection | Skjermbilde av macOS' varslingsliste med varselet, tatt på Kjetils maskin | `TESTRESULT.md#notify` |
| `test.notify.purpose-gate` | command | Enhetstest: en challenge som ikke trenger mennesket gir ingen varsling; en som gjør det, gir én | `TESTRESULT.md#notify` |
| `test.notify.no-duplicates` | command | Samme challenge sett tre ganger på rad gir ett varsel; et besvart varsel gjenoppstår ikke | `TESTRESULT.md#notify` |
| `test.notify.no-secrets` | command | Varsel- og menytekst for alle fixtures matcher ikke token-, nøkkel- eller signaturmønstre | `TESTRESULT.md#notify` |
| `test.build` | command | `swift build` for alle berørte mål + appmålet | `TESTRESULT.md#build` |
| `test.regression` | command | Hele `swift test` i HavenAgentD, mot målt baseline | `TESTRESULT.md#regression` |
| `test.branch-has-commits` | command | `git rev-parse pdd/agent-menylinje-og-varsler` ≠ `git rev-parse <base>` | `TESTRESULT.md#branch` |
| `test.docs-updated` | inspection | Docs-diff i samme endring, datert | `ACCEPT.md#docs` |
| `test.status-current` | inspection | STATUS.md speiler faktisk tilstand | `ACCEPT.md#status` |

## 6. Åpne spørsmål (endrer treet)

| # | Spørsmål | Hvorfor det betyr noe | Antakelse jeg går på inntil svar |
|---|---|---|---|
| Q1 | Skal menylinjeappen kjøre som egen LaunchAgent ved innlogging, eller startes manuelt? | Avgjør om oppgaven også eier en installasjonsseremoni | Egen LaunchAgent, `LSUIElement`, men installasjonen legges i WP8 og er ikke G3-krav |
| Q2 | «Full adminflate» — er det agentens egne saker, eller også scaffoldens adminflate i samme vindu? | Avgjør om vinduet må autentisere mot staging | Agentens egne saker i vinduet + tydelige lenker ut til `/onboard` og scaffoldens `/admin/funding` |
| Q3 | Skal topup-/tilgangskøen hentes med Kjetils identitet eller agentens? | Agentens identitet har i dag ikke nødvendigvis leserett; scaffold-admin-delegeringen er ikke landet | Agentens identitet, og **når den ikke får lese, sier flaten det** — ingen tom liste |
| Q4 | Hvor mange varsler er for mange? | Formålsfilteret trenger en grense | Én varsling per challenge, ingen gjentakelse, og en samlevarsling hvis mer enn tre kommer innen ett minutt |

## 7. Revisjonslogg

| Iterasjon | Dato | Hva som endret seg |
|---|---|---|
| 1 | 2026-09-09 | Første fullstendige spesifikasjon. Skrevet mens Kjetil sov, på hans bestilling om å implementere og vise i morgen. G1/G1-GUI står `venter`. |
| 1a | 2026-09-09 | Auditen fanget en feil i min egen første versjon: jobbkøen (`awaitingApproval`) finnes bare som usporede filer i det delte treet, ikke på `main`. Kilden er tatt ut av v1 og erstattet med en tom, deklarert `job`-kilde i kontrakten. |
