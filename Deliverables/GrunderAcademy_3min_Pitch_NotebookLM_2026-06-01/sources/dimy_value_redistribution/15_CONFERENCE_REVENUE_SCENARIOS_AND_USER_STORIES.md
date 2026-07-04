# DiMy konferanseprodukt: inntektsscenarier, cellebidrag og brukerhistorier

Oppdatert: 2026-05-14

Status: scenario- og prioriteringsnotat. Dette er ikke en forecast, ikke juridisk rådgivning og ikke et kundetilbud. Tallene er modellantakelser basert på det vi har dokumentert/implementert i HAVEN/DiMy og må kalibreres med faktiske pilotpriser, cloud-kost, supporttid, sponsorbetalingsvilje og juridisk vurdering før ekstern bruk.

## Kort konklusjon

DiMy kan tjene penger på konferanser på to nivåer:

1. **Workspace/drift:** arrangøren betaler for konferanseflate, deltakerportal, agenda, matching, møteflyt, Jitsi/media, support og rapportering.
2. **Sponsorverdi:** sponsorer/exhibitors betaler for kvalifiserte, samtykkede lead unlocks med audit trail.

Det andre nivået er det store økonomiske potensialet. I scenariomodellen står `ConferenceSponsorLeadAggregateCell + LeadVaultCell + ConsentReceiptCell + ExhibitorAccessCell` for 58-86 % av bruttoinntekten avhengig av arrangementsstørrelse. Det betyr at DiMy bør prioritere produktet som **"sponsorverdi med samtykke og audit"**, ikke bare "konferanseapp".

Trygg produktsetning:

> DiMy lar arrangører selge bedre sponsorverdi uten å gjøre deltakerdata ugjennomsiktig: hvert unlock må ha samtykke, kvalifisering, kostgrunnlag og audit.

## Kilder og antakelser

Sjekket 2026-05-14:

- Vipps MobilePay viser standardpriser for bedrifter, blant annet `2,49 % + 1 NOK` per transaksjon for betalingslenker og `2,99 % + 1 NOK` for integrert/API-basert betaling. Modellen bruker `2,5 % + 1 NOK` som enkel PSP-antakelse: [Vipps MobilePay priser](https://vippsmobilepay.com/nb-NO/pricing).
- OpenAI viser at GPT-5.4 mini prises til `$0.75 / 1M` input tokens og `$4.50 / 1M` output tokens per 2026-05-14. Modellen bruker likevel høyere AI-kost per aktiv AI-bruker for å dekke routing, retry, support og usikkerhet: [OpenAI API pricing](https://openai.com/api/pricing/).
- Jitsi beskriver Jitsi Meet som 100 % open source og selv-hostbar. Derfor behandles video/media som utskiftbart underlag, ikke DiMy-IP: [Jitsi Meet](https://jitsi.org/jitsi-meet/).
- Finanstilsynet beskriver e-penger som elektronisk lagret pengeverdi med kumulative vilkår, inkludert fordring på utsteder og aksept som betalingsmiddel av andre enn utsteder. Derfor holdes v0 til ikke-overførbar tilgang/usage/benefit, ikke wallet/cash-out: [Definisjonen av e-penger](https://www.finanstilsynet.no/tillatelser/e-pengeforetak/definisjonen-av-e-penger/).
- Finanstilsynet beskriver MiCA som regelverk for kryptoeiendeler, inkludert krav ved CASP-aktivitet og EMT/ART. Derfor er tokens, cash-out, P2P og ekstern aksept hard stop før juridisk løp: [Kryptoeiendelsloven/MiCA](https://www.finanstilsynet.no/tema/kryptoeiendeler-mica/).

Modellen er generert av:

- [conference_revenue_scenarios.mjs](scripts/conference_revenue_scenarios.mjs)
- [conference_revenue_scenarios_2026-05-14.json](outputs/conference_revenue_scenarios_2026-05-14.json)
- [conference_revenue_scenarios_2026-05-14.csv](outputs/conference_revenue_scenarios_2026-05-14.csv)

## Scenarioantakelser

Inntektsmodellen har disse pakkene:

- `Conference Workspace`: arrangørpakke + deltakerplattformfee.
- `Sponsor Package`: sponsor-/exhibitorflate, pipeline og rapportering.
- `Lead Unlock`: kvalifisert, samtykket lead unlock.
- `AI Concierge`: betalt add-on for guided onboarding, matching, sponsor/organizer-assistent.
- `Audit / Transparency`: verdi- og ressursrapport, role-scoped export, policyforklaring.

Kostmodellen inkluderer:

- PSP-gebyr,
- storage,
- runtime CPU/minne/workers,
- Jitsi/media-båndbredde,
- AI-provider,
- LeadVault-operasjoner,
- support,
- audit export,
- risikobuffer.

Etter kost beregnes en policy-simulering:

- 55 % av positiv margin til DiMy operator,
- 20 % til HAVEN commons,
- 25 % til deltaker-/gruppe-benefit som ikke-overførbar simulering.

Dette er en scenario-policy, ikke juridisk eller regnskapsmessig konklusjon.

## Resultater

| Scenario | Deltakere | Sponsorer | Unlocks | Brutto | Kost | Margin | DiMy operator, 55 % av margin | LeadVault-andel |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Lite fagarrangement | 120 | 4 | 40 | 106 380 NOK | 31 350 NOK | 75 031 NOK | 41 267 NOK | 58,3 % |
| Mellomstor bransjekonferanse | 500 | 15 | 450 | 654 875 NOK | 144 632 NOK | 510 243 NOK | 280 634 NOK | 75,6 % |
| Stor industrikonferanse | 1 500 | 45 | 2 200 | 2 721 125 NOK | 521 255 NOK | 2 199 870 NOK | 1 209 928 NOK | 82,3 % |
| Expo / stort hybridt event | 5 000 | 120 | 9 000 | 9 270 000 NOK | 1 728 271 NOK | 7 541 729 NOK | 4 147 951 NOK | 85,8 % |

Tolkning:

- Tallene blir store når sponsor unlock-volumet blir stort. Dette er en styrke hvis betalingsviljen finnes, men også største usikkerhet.
- DiMy sin direkte operator-andel etter policy ligger i modellen på ca. 39-45 % av bruttoinntekt.
- Uten LeadVault/sponsorprodukt blir konferansen primært en driftet workspace med lavere, men mer forutsigbar SaaS-/serviceinntekt.
- Den viktigste kommersielle hypotesen å teste er ikke "vil noen bruke appen?", men "vil sponsorer betale for kvalifiserte, samtykkede, auditerbare relasjoner?"

## Sensitivitet

| Scenario | +/- 100 NOK per unlock | +/- 10 % sponsorpakke | +/- 1 NOK per deltaker-time media |
| --- | ---: | ---: | ---: |
| Lite fagarrangement | 4 000 NOK | 3 200 NOK | 600 NOK |
| Mellomstor bransjekonferanse | 45 000 NOK | 18 000 NOK | 8 000 NOK |
| Stor industrikonferanse | 220 000 NOK | 81 000 NOK | 45 000 NOK |
| Expo / stort hybridt event | 900 000 NOK | 300 000 NOK | 250 000 NOK |

Konklusjon: unlock-pris og unlock-rate dominerer økonomien mer enn media-kost i denne modellen. Derfor bør produktet bygges for å bevise sponsorverdi, consent og lead quality tidlig.

## Hvilke celler genererer hva

| Celle/gruppe | Nåværende status | Genererer kundeverdi | Genererer DiMy-inntekt | Kost-/auditgrunnlag |
| --- | --- | --- | --- | --- |
| `ConferencePublishedContentCell` + `ConferencePublicShellCell` | implementert/demoable | landing, program, artikler, publikumsflate | del av organizer package | storage, bandwidth, publish events |
| `ConferenceRegistrationCell` | implementert | påmelding, deltakerbinding | deltakerplattformfee | storage, registration events |
| `ConferenceOnboardingCell` + `ConferencePublicProfileCell` | implementert | profil, purpose, visibility, consent-forberedelse | deltakerplattformfee, sponsorverdi indirekte | storage, consent metadata, visibility policy |
| `ConferenceAgendaCell` | implementert | agenda, saved/focused sessions | del av workspace | storage, interaction events |
| `ConferenceRecommendationCell` + `ConferenceEntityDiscoveryCell` | implementert | relevante folk/sesjoner, discovery | premium workspace/AI add-on | CPU, matching events, no global reputation |
| `ConferenceSchedulingCell` | implementert | møteintensjon, availability, koordinering | premium workspace/sponsorverdi | CPU, meeting events |
| `ConferenceConnectionHubCell` + shared chat/session cells | implementert | relasjoner, møter, thread/polling | workspace, sponsor follow-up | storage, bandwidth, message/thread events |
| `ConferenceConciergeCell` + `ConferenceAIGatewayPreviewCell` + `AIGatewayCell` | delvis implementert | guided onboarding, sponsor/organizer assistant | AI Concierge add-on | provider/model/tokens, quota, no prompt/output in cost event |
| `ConferenceInsightAggregateCell` + `ConferenceOrganizerProjectionCell` | implementert/demoable | KPI, rapportering, sponsor proof | audit/transparency package | aggregate compute, no raw private payloads |
| `ConferenceSponsorLeadAggregateCell` | implementert/demoable | sponsor-safe candidate/handoff | lead product foundation | CPU, aggregate events |
| `LeadVaultCell` | implementert | capture, qualify, reclaim, export | Lead Vault + unlock/reporting | lead capture, qualification, export audit |
| `ConsentReceiptCell` | implementert | consent grant/revoke/receipt | muliggjør betalt unlock | consent proof, revoke/reclaim chain |
| `ExhibitorAccessCell` | implementert, men ikke ledger-backed nok | credits, unlock, reclaim/refund | lead unlock revenue | credit grants, unlock events, must link DiMyMint |
| `PaymentGateCell` / `PaymentProofDoorCell` / `DiMyMint` | implementert/delvis | PSP -> entitlement/proof/ledger | muliggjør betalt flow | PSP fee, ledger, reservation, receipt |
| `JitsiConferenceGatekeeperCell` / media adapter | dokumentert plan, ikke funnet som runtime-cell | kortlivede konferansetokens, roller, join/leave audit | del av workspace/media package | bandwidth, session events, auth decisions |
| `ValueFlowViewerCell` | kontrakt/fixture, ikke runtime-cell | transparent pris, verdi og audit | transparency package, trust moat | ValueFlowEvent/ResourceMeterEvent/allocation |
| `ConferenceSimulation*` cells | implementert/demo | salgsdemo, synthetic population, playback | indirekte salgsverdi | ikke produksjonsinntekt, men bevisverktøy |

## Hva vi mangler før betalt pilot

P0, må på plass:

1. **Runtime `ResourceMeterEvent`** fra konferanseceller, Jitsi/media og `AIGatewayCell`.
2. **Ledger-backed `ExhibitorAccessCell`**: `grantCreditsFromWebhook` må kreve `DiMyMint` ledgerEventRef, idempotency, policyHash, expiry og conference scope.
3. **PSP-signatur og avstemming** for valgt betalingsløp, ikke bare syntetisk eller placeholder.
4. **Runtime `ValueFlowEvent`** for PSP inflow, ledger credit, entitlement grant, lead unlock, reclaim/refund og allocation.
5. **Role-scoped `ValueFlowViewerCell`** eller tilsvarende kunde-/operatørflate.
6. **Consent revoke -> reclaim/refund path** testet end-to-end.
7. **Conference media metering**: session start/join/leave/refresh, participant-minutes, bandwidth estimate/actual, recording/transcription hvis brukt.
8. **Audit export manifest** med checksum, policyHash og private-payload guardrail.
9. **Kundevennlig pricing policy** som kan forklare basepris, inkludert kvote, overage og sponsor unlock.
10. **Juridisk vurdering** før ekte benefit/rebate/grant, og hard stopp for cash-out, P2P, transferable credits eller ekstern aksept.

P1, bør på plass for skalerbar salgsdemo:

1. Sponsor self-service kjøp av unlock pack.
2. Participant consent inbox / approval inbox.
3. Post-event survey + query-list opt-in.
4. Organizer value report som kan deles med styre/sponsorer.
5. Sponsor ROI dashboard med qualified/unlocked/reclaimed/follow-up.
6. DiMy operator margin dashboard med ressurskost og policy warnings.

## Hva vi bør implementere i tillegg

| Prioritet | Ny/utvidet celle | Verdiforslag | Hvorfor den er god for DiMy |
| --- | --- | --- | --- |
| P0 | `ConferenceValueReportCell` | arrangør får post-event rapport over sponsorverdi, samtykke, kost og audit | gjør transparens til betalt pakke og salgsmateriell |
| P0 | `ConferenceResourceMeterAdapter` | alle conference/Jitsi/AI-kostnader blir `ResourceMeterEvent` | nødvendig for margin, pricing og tillit |
| P0 | `LeadUnlockPurchaseCell` eller self-service flow rundt `ExhibitorAccessCell` | sponsor kjøper unlock pack og ser saldo/bruk | direkte inntektsmotor |
| P0 | `ParticipantConsentInboxCell` | deltaker ser og godkjenner sponsor-/arrangørforespørsler | gjør sponsorinntekt mulig uten tillitstap |
| P1 | `ConferenceSponsorROIDashboardCell` | sponsor ser unlocks, meetings, reclaim/refund, kvalifisering | øker fornyelse og sponsorpris |
| P1 | `ConferencePostEventSurveyCell` | opt-in til follow-up/query-list og forbedring av neste event | utvider livstiden på eventet og skaper ny inntekt |
| P1 | `ConferenceQueryLeaseCell` | tidsavgrenset tilgang til bestemte query surfaces | gjør follow-up juridisk/teknisk ryddigere |
| P1 | `ConferenceAIConciergePaidTier` | betalt guided onboarding, matching, summaries og sponsor/organizer brief | lett å forstå som add-on; måles via AIGateway |
| P2 | CRM/export connectors med explicit grants | sponsor kan sende godkjente leads til eget CRM | enterprise-verdi og høyere sponsor WTP |

Anbefalt neste implementeringsrekkefølge:

1. `ConferenceResourceMeterAdapter` + runtime `ResourceMeterEvent`.
2. Ledger-backed `ExhibitorAccessCell` + `ValueFlowEvent`.
3. `ValueFlowViewerCell` / `ConferenceValueReportCell` over eksisterende scenario-output.
4. Sponsor self-service unlock pack.
5. Participant consent inbox.
6. Post-event survey + query lease.
7. Paid AI Concierge tier.

## Brukerhistorier som bør lages

### 1. Arrangør får transparent event-quote

Som arrangør vil jeg velge antall deltakere, sponsorer, videobehov, AI og auditnivå og få en forklarbar pris før jeg kjøper, slik at jeg kan forankre budsjettet.

DiMy-verdi:

- selger `Conference Workspace`,
- gjør overage akseptabelt fordi kostgrunnlaget er synlig,
- skaper første `ValueFlowViewer`-moment.

Aksept:

- quote viser base, deltakerfee, media-estimat, AI-estimat, support/audit og policyHash,
- ingen kostbærende handling uten synlig quote.

### 2. Sponsor kjøper unlock pack etter å ha sett kvalifisert potensial

Som sponsor vil jeg se aggregerte, consent-safe lead-kategorier og kjøpe unlock credits for bare relevante leads, slik at jeg får høyere ROI enn generisk logoeksponering.

DiMy-verdi:

- direkte sponsorinntekt,
- høy margin hvis unlock-pris og lead quality holder,
- differensierer DiMy fra generisk konferanseplattform.

Aksept:

- betaling går PSP -> DiMyMint ledger -> non-transferable event-scoped entitlement,
- `ExhibitorAccessCell` kan ikke gi credits uten ledgerEventRef.

### 3. Deltaker godkjenner sponsorinteresse og får receipt

Som deltaker vil jeg forstå hvilken sponsor som ber om hva, hvorfor jeg matcher, og hva jeg får igjen, slik at jeg kan samtykke uten å føle at profilen min selges bak ryggen min.

DiMy-verdi:

- øker consent-rate,
- reduserer churn/tillitstap,
- gjør sponsorproduktet etisk og salgbart.

Aksept:

- consent receipt opprettes,
- deltaker kan revoke,
- unlock/reclaim-historikk er synlig rollebegrenset.

### 4. Sponsor unlocker kvalifisert lead og booker møte

Som sponsor vil jeg bruke én credit på et kvalifisert, samtykket lead og umiddelbart kunne foreslå møte eller follow-up, slik at verdien blir handlingsbar.

DiMy-verdi:

- lead unlock revenue,
- møte-/follow-up flyt øker sponsorfornyelse,
- skaper data for sponsor ROI dashboard.

Aksept:

- lead må være qualified og consent granted,
- unlock lager `ValueFlowEvent`,
- meeting/follow-up lager relation event uten å eksponere mer enn granted scope.

### 5. Arrangør ser live verdi og post-event rapport

Som arrangør vil jeg se deltakerdynamikk, sponsorverdi, consent-rate, unlocks, reclaims og ressurskost i én rapport, slik at jeg kan dokumentere verdien til neste års sponsorer.

DiMy-verdi:

- selger `Value Transparency Pack`,
- gjør DiMy sticky for neste event,
- gir casemateriale til Innovasjon Norge/investorer.

Aksept:

- rapport bruker aggregate/role-scoped data,
- viser brutto, PSP, resource cost, DiMy allocation, HAVEN commons og eventuell benefit simulation.

### 6. DiMy operator ser margin og policy-warnings

Som DiMy operator vil jeg se margin per arrangement, per sponsorprodukt og per ressurs, slik at jeg kan justere pris før marginen spises av media/support/AI.

DiMy-verdi:

- beskytter lønnsomhet,
- gjør support og risk buffer synlig,
- hindrer at "transparens" blir ulønnsomt.

Aksept:

- dashboard viser faktisk resource events og ikke bare estimater,
- varsler ved negativ margin, manglende policyHash, manglende ledgerRef eller private payload i event.

### 7. Participant AI Concierge blir betalt add-on uten å bli skjult kjøp

Som deltaker vil jeg få bedre onboarding, anbefalinger og oppsummeringer, men vite når AI koster penger eller forlater device/runtime.

DiMy-verdi:

- AI Concierge fee,
- mer engasjement gir mer sponsorverdi,
- `AIGatewayCell` gjør kost og quota målbar.

Aksept:

- AI-call har quote eller inkludert kvote,
- provider/model og kostgrunnlag vises uten prompt/output i value events.

### 8. Post-event query-list opt-in

Som deltaker vil jeg kunne si ja til bestemte typer oppfølging etter eventet, og som arrangør vil jeg kunne spørre deltakere senere uten å få bred, permanent tilgang.

DiMy-verdi:

- forlenger arrangementets kommersielle liv,
- skaper fremtidige sponsor-/communityprodukter,
- styrker HAVEN-fortellingen om tidsavgrensede grants.

Aksept:

- query lease har scope, purpose, expiry og revoke,
- ingen global identity eller skjult profilering.

## Diagram

- [conference_revenue_cell_map.mmd](diagrams/conference_revenue_cell_map.mmd)

