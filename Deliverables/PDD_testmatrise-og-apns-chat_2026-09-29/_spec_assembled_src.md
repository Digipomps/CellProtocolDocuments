# Formålsspesifikasjon — testmatrise og APNs-chat

Oppgavemappe: `PDD_testmatrise-og-apns-chat_2026-09-29` · Opprettet 2026-09-29 · Iterasjon 1 (venter på G1)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Sett opp forskjellige tester som går mellom forskjellige scaffolds, en mellom to eller tre brukere på samme scaffold, en test fra prod til en bruker på palazzo (kanskje en kelner?) og test fra de forskjellige enhetene HAVEN app kan kjøre fra. Når alt er klart for APNs testing så vil jeg ha det også slik at man kan initiere en chat fra et skyscaffold til f.eks en iPhone. Test og push all ucommitted kode.

Svar på oppklaring 29.09 (Kjetil): push = «bare mitt + wip-snapshot»; scaffolds = «lokale instanser først, prod↔Palazzo som skrivebeskyttet røyktest»; enheter = «simulator + Mac + kontrakt, ekte iPhone i manuell sjekkliste»; APNs = **«full implementasjon mot Apple»** (se §2: krever nøkler som bare Kjetil har).

### 0.1 Det forespørselen forutsetter, revidert mot koden (29.09)

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| To brukere kan chatte via invitasjon (Kjetil↔Vegar) | **retrieved**: typer, verifisering og nøkkelavtale-nøkkel er på main (#51, 81601a6, 15/15 + 1277/0 feil). Aksept → to envelopes → ChatCell klar (WP7) er **ikke** gjort | CellProtocol `HavenInviteRoundATests.swift`; PLAN.md WP7 |
| Landing/reply/gravstein/410/sender-status mot ekte scaffold | **unavailable**: del 2 (CellScaffold + Binding) er ikke skrevet | STATUS.md 26.09 |
| Et skyscaffold kan sende APNs | **retrieved, delvis**: `APNSPushProviderAdapter` finnes (JWT ES256, `api(.sandbox).push.apple.com`, topic, alert/background), konfigurert av `APNS_TEAM_ID`, `APNS_KEY_ID`, `APNS_PRIVATE_KEY_P8`/`_BASE64`/`_PATH`, `APNS_BUNDLE_ID`, `APNS_USE_SANDBOX`. Bygget for konferansevarsler (`NotificationOutboxCell`), ikke for chat/invitasjon | `CellScaffold/Sources/App/Cells/ConferenceMVP/Notifications/PushProviderAdapter.swift:116-162,272-341` |
| iPhone registrerer push-token mot scaffold | **retrieved, delvis**: `NotificationEnrollmentManager` kaller `registerForRemoteNotifications`, `updateAPNSToken`, registrerer enhet med konferanse-ID og emner. Ikke knyttet til en entitet/relasjon eller chat | `Binding/Binding/NotificationEnrollmentManager.swift:45-232` |
| Palazzo er en scaffold-installasjon vi kan nå fra prod | **recalled**: Palazzo-celler (`Restaurant/*`, `PalazzoCommunaleServiceCell`, `RestaurantStaffShellCell`) ligger i CellScaffold-koden; **hvilken vert/miljø Palazzo kjører på er ikke funnet** i Documentation/Operations (kun `haven.digipomps.org`, `staging.haven.digipomps.org`, `admin.*`) | `Restaurant/RestaurantStaffShellCell.swift`; grep i `Documentation/Operations` |
| «Kelner» finnes som rolle | **retrieved, delvis**: `RestaurantStaffShellCell` (staff-forhåndsvisning, «denied: staff preview owner required»). Ingen kelner-*identitet* funnet | `RestaurantStaffShellCell.swift:52-76` |
| Flere scaffolds kan kjøres lokalt samtidig | **recalled**: startskript finnes (`run_local_kallimachos_butler_admin_demo.sh`, `run_porthole_chat_canary.sh`), men ikke målt at to instanser med egen eier/vault og egen port kjører side om side | `CellScaffold/scripts/` |
| Appen kan kjøre fra flere enheter | **retrieved**: `Binding.xcodeproj` `SUPPORTED_PLATFORMS = iphoneos iphonesimulator macosx`, `TARGETED_DEVICE_FAMILY = 1,2` (iPhone + iPad). Linux-scaffold via `Tests/Linux/` | `Binding/Binding.xcodeproj/project.pbxproj:668-721` |
| «All ucommitted kode» er håndterbar | **contradicted i omfang**: Binding 409 endret + 42 035 uspora filer; CellScaffold 1 815 endret + 419 uspora; CellProtocolDocuments 883 endret. Mesteparten er andre tråders arbeid og bevismateriale | `git diff-files` / `ls-files -o` 29.09 |

## 1. Formålstre

Alle noder er `candidate` til Kjetil har sagt G1. Ingen gjenbrukes av Book 23 direkte, men rotens forelder er `purpose://contact.communication` (samme som invitasjonstreet).

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.testmatrise.root` | Samarbeid mellom inviterte kan bevises på alle veier | `contact.communication` | Hver vei en invitert kan komme inn og snakke — samme scaffold, mellom scaffolds, prod→Palazzo, alle enheter, skyscaffold→iPhone — har en kjørbar test som gir grønt eller `blocked` med grunn | §5 i sin helhet | candidate |
| **T1** `…testmatrise.same-scaffold-collaboration` | To–tre brukere på ett scaffold | root | Tre entiteter (egne vaults, tilfeldige UUID-er) inviterer, aksepterer og snakker i én invitasjonschat på ett scaffold; hver ser bare det de er invitert til; den tredje kan ikke lese de to andres samtale | `test.matrise.same-scaffold-three` | candidate |
| **T2** `…testmatrise.two-scaffolds-one-conversation` | Én samtale mellom to scaffolds | root | A på scaffold 1 inviterer B på scaffold 2 (lokale instanser, egen port, eier og vault hver); ja gir chat der begge ser samme meldinger, forseglet til hver mottakers nøkkel; ingen av scaffoldenes admin kan lese den andres celler | `test.matrise.cross-scaffold-chat`, `test.matrise.admin-cannot-enter-other-scaffold` | candidate |
| **T3** `…testmatrise.prod-to-palazzo-staff` | Prod → en bruker på Palazzo (kelner) | root | Fra prod-scaffold kan en invitasjon til en Palazzo-kelner *slås opp og leses* (røyktest, ingen skriving i prod uten Kjetils ja); det samme scenariet med skriving kjøres mot staging med en testkelner merket som test | `test.matrise.prod-readonly-smoke`, `test.matrise.staging-waiter-chain` | candidate |
| **T4** `…testmatrise.same-suite-on-every-device` | Samme suite på hver enhet | root | Chat-scenariene T1/T2 kjøres som *data-drevne enhetsprofiler*: Mac-app, iOS-simulator iPhone, iOS-simulator iPad, Linux-scaffold (klient uten UI). Ekte iPhone har en manuell sjekkliste med forventet observasjon per steg | `test.matrise.device-profiles`, `test.matrise.iphone-checklist` | candidate |
| **T5** `…testmatrise.cloud-scaffold-starts-a-chat-on-a-phone` | Skyscaffold starter en chat på en telefon | root | En eier på et skyscaffold inviterer en person som har HAVEN på iPhone; telefonen får en APNs-varsling som *ikke bærer innhold*, og trykk åpner invitasjonen i appen; ja gir chat | se T5.1–T5.5 | candidate |
| T5.1 `…apns.token-belongs-to-an-entity` | Push-token hører til en entitet, ikke en konferanse | T5 | iPhone registrerer token mot skyscaffoldet under entitetens egen identitet (signert), med `sandbox`/`production`, `bundleId`, og kan trekke det tilbake; scaffoldet lagrer token uten navn | `test.apns.token-registration-signed`, `test.apns.token-revoke` | candidate |
| T5.2 `…apns.payload-carries-no-content` | Varselet bærer ingen personinfo | T5 | Payload = `{aps:{alert:generisk tekst}, haven:{k:"invite", id:<ticketID>}}`. Ingen avsendernavn, ingen meldingstekst, ingen basis-felt. Tekst i §3 godkjennes av Kjetil | `test.apns.payload-has-no-content` | candidate |
| T5.3 `…apns.only-who-was-invited-is-pushed` | Bare den inviterte kan varsles | T5 | Varsel sendes bare til token registrert av entiteten billetten er adressert til (audience-token treffer); en annen entitets token, et utløpt eller trukket token, og en gravstein nekter | `test.apns.wrong-audience-not-pushed`, `test.apns.tombstone-blocks-push`, `test.apns.expired-not-pushed` | candidate |
| T5.4 `…apns.tap-opens-the-invitation` | Trykk åpner invitasjonen i appen | T5 | Appen mottar `haven.k/id`, henter billetten fra scaffoldet, verifiserer den (`HavenInviteVerifier`) og viser invitasjonsflaten. Ingen auto-aksept | `test.apns.tap-opens-verified-invitation` | candidate |
| T5.5 `…apns.real-sandbox-send` | Ekte sending mot Apple (sandbox) | T5 | Ett varsel går fra et skyscaffold til Kjetils iPhone via `api.sandbox.push.apple.com`; Apple svarer 200 med `apns-id`; varselet vises; trykk åpner appen | `test.apns.real-sandbox-send` (**blocked** til Kjetil har gitt nøkkel-oppsett og token, se §2) | candidate |
| **T6** `…testmatrise.nothing-uncommitted-is-lost` | Ingenting ucommittet går tapt | root | Alt ucommittet i CellProtocol, CellScaffold, Binding (og CellProtocolDocuments) ligger som en pushet wip-commit uten at noens checkout, indeks eller worktree er rørt; hemmeligheter og bygg-rot er ute; commit-hash er lest etter push | `test.push.snapshot-no-disturbance`, `test.push.no-secrets`, `test.push.hash-read-after-push` | candidate |

Regler: hvert blad har minst én test i §5. T5.5 er det eneste som ikke kan bli grønt uten noe bare Kjetil kan gi.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke skriving i prod uten et eget, eksplisitt ja fra Kjetil per gang. Prod-testen er lesing.
- Ikke en ny chat-implementasjon: T1–T4 tester kjeden som WP7 + runde A del 2 bygger. Der en test trenger noe som ikke finnes ennå, står den som `blocked: avhenger av WP<n>`, ikke som grønn.
- Ikke innhold i push. Aldri. Varselet sier at noe finnes, appen henter det selv.
- Ikke et varsel som kan sendes uten at den inviterte har registrert sitt eget token.
- Ikke å bygge inn andre tråders ucommitterte arbeid i mine PR-er, og ikke å røre deres checkouts (T6).
- Ikke å ta APNs-nøkkel, Team-ID eller token i hånden: jeg leser dem aldri, skriver dem aldri i chat eller repo. De settes som miljøvariabler på scaffoldet av Kjetil (se under).

Kapabiliteter og avhengigheter oppgaven bygger på:

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Invitasjonstyper, verifisering, gravstein, nøkkelavtale-nøkkel | CellProtocol main 81601a6 (#51) | ingen scaffold-side ennå | ja — **grønn** (15/15, 1277/0) |
| Aksept → to envelopes → ChatCell klar | PLAN.md WP7 | ikke skrevet | ja — T1/T2 `blocked` til den er grønn |
| CellScaffold-side av invitasjon (landing, reply, tombstone, 410, sender-status) | PLAN.md runde A del 2 | ikke skrevet | ja — T2/T3/T5 |
| `APNSPushProviderAdapter` + `PushHTTPTransport`-stub | `PushProviderAdapter.swift` | konferansevarsler; payload-form må byttes for invitasjon | ja for T5.2/T5.3 |
| Enhetsregistrering med `apnsToken` | `NotificationEnrollmentManager.swift`, `DeviceRegistrationReadinessTests` | knyttet til konferanse, ikke entitet | ja for T5.1 |
| Apple: APNs-nøkkel (.p8), Key-ID, Team-ID, bundle-ID/topic, push-entitlement i appen, enhets-token | **Kjetil** (Apple Developer) | kan ikke skaffes av meg | bare T5.5 |
| Palazzo-vert/miljø og kelner-identitet | ikke funnet | **åpent, se §6** | bare T3 |
| Xcode/simulator for enhetsprofiler | `Binding.xcodeproj`, macOS-skript via Finder | ekte iPhone styrer jeg ikke | T4 |

## 3. Forventningskontrakt — «Det du kommer til å se»

Etter G2 er dette det eneste som teller som fremdrift.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| **Testmatrisen**: én tabell scenario × miljø × enhet × resultat (grønn / rød / blocked + grunn) | fil | `TESTRESULT.md#matrise` | — | nei |
| Tre-brukere-på-ett-scaffold: testutdata + chronicle-spor per entitet | testutdata | `TESTRESULT.md#same-scaffold` | — | nei |
| Mellom-to-scaffolds: to kjørende lokale instanser, logg fra begge, samme meldinger på begge sider | testutdata + logger | `TESTRESULT.md#cross-scaffold`, `handoff/…/*.log` | — | nei |
| Prod-røyktest (bare lesing) med URL, statuskoder og hva som ble lest | testutdata | `TESTRESULT.md#prod-smoke` | — | nei |
| Staging-kjede prod-lignende → Palazzo-kelner (testentitet merket som test) | testutdata | `TESTRESULT.md#palazzo` | — | nei |
| Enhetsprofiler (Mac, iPhone-sim, iPad-sim, Linux) med resultat per profil | testutdata | `TESTRESULT.md#devices` | — | nei |
| Manuell iPhone-sjekkliste med forventet observasjon per steg | fil | `handoff/iphone-sjekkliste.md` | — | nei |
| APNs: `PushSendRequest` for invitasjon, stub-transport, payload-fixtures, kontrakt | kontrakt + fixtures | `contract/apns_invite_v1.json` + `contract/fixtures/` | — | nei |
| **Varslingsteksten** som vises på låseskjermen (hele teksten, ingen personinfo) | tekst — Kjetil dømmer | `FORMAALSSPEC.md §3.1` under | ja/nei | nei |
| Ekte sandbox-varsel på Kjetils iPhone | kjørende flate + apns-id i logg | `TESTRESULT.md#apns-real` | — | nei |
| Wip-snapshot per repo: commit-hash lest etter push, antall filer, hva som ble holdt ute og hvorfor | testutdata | `TESTRESULT.md#push` | — | nei |

### 3.1 Varslingsteksten (forslag — Kjetil godkjenner ordlyden i G1)

Låseskjerm, norsk: **tittel «HAVEN»**, **tekst «Du har en invitasjon å svare på.»** Ingen avsendernavn, ingen forhåndsvisning av melding. Det er avsenderens navn og grunnlag som vises *inne i appen*, etter at billetten er verifisert (jf. invitasjonsstripen, G1-GUI 24.09). Engelsk språkversjon følger appens språk; ordlisten fra invitasjons-PDD-en gjelder (ingen «entitet», «scaffold», «token» i teksten).


@@SEC4@@

## 5. Avledede tester (samlet)

Kolonnen «Kan kjøres» sier ærlig hva som er mulig før avhengighetene i §2 er grønne. En `blocked`-rad er ikke en grønn rad.

| Test | Type | Hva den viser | Hvor | Kan kjøres nå |
|---|---|---|---|---|
| `test.matrise.same-scaffold-three` | command | tre `SimulatedEntity`, invitasjonschat, C leser ikke A↔B | `TESTRESULT.md#same-scaffold` | delvis: nøkkelavtale-nøkkel og aksept-signatur ja; ChatCell-klar krever WP7 |
| `test.matrise.cross-scaffold-chat` | command | to lokale scaffolds (egne porter/eiere/vaults), samme meldinger begge veier | `#cross-scaffold` | nei — krever del 2 + WP7 |
| `test.matrise.admin-cannot-enter-other-scaffold` | command | admin på 1 nektes lesing/skriving/handlinger i celler på 2 (gjenbruker entitetsdata-fixtures) | `#cross-scaffold` | ja (fra runde 2-mønsteret) |
| `test.matrise.prod-readonly-smoke` | command | GET-oppslag mot prod: helse, offentlig invitasjonsoppslag av et *ikke-eksisterende* endepunkt gir samme svar som et ikke-publisert (A1). Ingen POST | `#prod-smoke` | ja, etter Kjetils ja til at jeg leser fra prod |
| `test.matrise.staging-waiter-chain` | command | testkelner-entitet på staging-Palazzo mottar invitasjon og chat | `#palazzo` | nei — krever §6.1–6.2 og del 2 |
| `test.matrise.device-profiles` | command | samme scenario med profil `mac-app`, `ios-sim-iphone`, `ios-sim-ipad`, `linux-client` (profil = data: plattform, destinasjon, hva som finnes av nøkkelchain) | `#devices` | delvis: profilene og kontraktnivå ja; app-kjøring via Xcode/Codex |
| `test.matrise.iphone-checklist` | inspection | Kjetil krysser av hvert steg | `handoff/iphone-sjekkliste.md` | ja, som fil |
| `test.apns.token-registration-signed` | command | usignert / feil-identitet registrering avvises; signert lagres uten navn | `#apns` | ja |
| `test.apns.token-revoke` | command | trukket token får aldri varsel | `#apns` | ja |
| `test.apns.payload-has-no-content` | command | golden fixture: payload inneholder bare generisk tekst + `haven.k/id`; sentinel i avsendernavn/basis/melding finnes ikke i noen byte | `#apns` | ja |
| `test.apns.wrong-audience-not-pushed` | command | token fra annen entitet → ingen sending | `#apns` | ja |
| `test.apns.tombstone-blocks-push` | command | «aldri» → ingen varsel, heller ikke ved ny billett | `#apns` | ja (gravstein fra #51) |
| `test.apns.expired-not-pushed` | command | utløpt/trukket billett → ingen varsel | `#apns` | ja |
| `test.apns.tap-opens-verified-invitation` | command | app-siden tar imot `haven.k/id`, henter, verifiserer, viser; ugyldig billett viser feilflate, ikke invitasjon | `#apns` | delvis: verifiseringsdelen ja; UI-delen krever Xcode |
| `test.apns.real-sandbox-send` | measurement | ekte 200 fra `api.sandbox.push.apple.com` + `apns-id` i logg; varsel vises på telefonen | `#apns-real` | **blocked** til Kjetil har satt `APNS_*` på scaffoldet og gitt et enhets-token |
| `test.push.snapshot-no-disturbance` | command | for hvert repo: HEAD, indeks og arbeidstre er byte-identiske før og etter (sha av `git diff-files` + `ls-files -o`) | `#push` | ja |
| `test.push.no-secrets` | command | skann av alt som ville gå med: `.p8`, `.pem`, `.env`, `*.key`, `*.mobileprovision`, `xcuserstate`, filer > 5 MB, `_wt*`, `_to_delete`, `.build` — ingen treff går med; hva som ble holdt ute listes | `#push` | ja (tørrkjøring først) |
| `test.push.hash-read-after-push` | command | `git ls-remote --heads origin <wip>` limt inn og lik lokal commit | `#push` | ja |
| `test.build` / `test.regression` | command | bygg CellProtocol/CellScaffold/Binding mot main; full CellBaseTests; scaffold- og Binding-tester som er grønne på main i dag forblir grønne | `#build`, `#regression` | ja |

Alle `command`-tester bruker de rette grønn-portene (`tail -1` av «Executed», POSIX `case`, jf. `lesson.green-gate-must-read-the-last-summary-line`).

## 6. Åpne spørsmål til Kjetil

Bare de som endrer treet.

1. **Palazzo — hvor kjører det?** Fant bare celler i CellScaffold-koden, ikke en vert. Er Palazzo (a) en egen scaffold-installasjon, (b) en konfigurasjon av samme prod-scaffold som `haven.digipomps.org`, eller (c) ikke oppe ennå? Svaret avgjør om T3 er «prod→annet scaffold» (som T2) eller «prod→annen rolle på samme scaffold» (som T1).
2. **Kelneren — ekte eller testentitet?** Skal røyktesten i prod bare lese, og staging-kjeden bruke en testkelner jeg oppretter (merket som test, i staging)? Eller finnes det en ekte kelner-identitet du vil bruke?
3. **APNs-oppsett (blokkerer bare T5.5):** hvilken bundle-ID er iPhone-appen (`org.digipomps.haven` eller `havenplayground`)? Bygges den fra Xcode (→ **sandbox**) eller TestFlight/App Store (→ **production**)? Og setter du selv `APNS_TEAM_ID`, `APNS_KEY_ID`, `APNS_PRIVATE_KEY_PATH` (peker på .p8 på scaffoldets disk — ikke inn i chat, ikke i repo) og `APNS_BUNDLE_ID` på det skyscaffoldet vi tester mot?
4. **Varselteksten** (§3.1): «HAVEN — Du har en invitasjon å svare på.» — ok, eller annen ordlyd?

## 7. Revisjonslogg

| Dato | Iterasjon | Hva endret seg |
|---|---|---|
| 2026-09-29 | 0 | Opprettet av `purpose_dev.py new` |
| 2026-09-29 | 1 | Full spec etter Kjetils svar (push-omfang, lokale instanser først, enhetsmatrise simulator+Mac, APNs full implementasjon). Audit mot kode: APNs-adapter og enhetsregistrering finnes, men er konferansevarsler; Palazzo-vert ikke funnet; «all ucommittet» er andre tråders arbeid i stort omfang (T6 løser det med snapshot uten å røre checkouts). |
