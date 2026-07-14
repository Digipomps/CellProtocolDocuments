# HAVEN/CellProtocol — Uavhengig statusrevisjon

Dato: 2026-07-10. Reviewer: Claude (Fable 5), på oppdrag fra Kjetil.
Metode: lokal repo-inspeksjon, faktiske testkjøringer, runtime-prober mot kjørende tjenester, skjermbilde-/artefaktgjennomgang og dokumentlesing. Ingen kode ble endret. Alle påstander er merket med evidensnivå: **[bevist]** (kjørt/observert i denne revisjonen), **[sannsynlig]** (basert på kode/artefakter), **[intensjon]** (dokumentert plan), **[uavklart]**.

---

## 1. Executive Summary

**Dom:** HAVEN er et reelt, stort og aktivt system — ikke en skisse. Kjerneprotokollen er testet og grønn, to tjenester kjører live (lokal Porthole + staging med TLS), en signert daemon kjører på maskinen, og conference-demoen består 12 av 13 ende-til-ende-tester. Samtidig er release-kjeden umoden: CellScaffolds testsuite **krasjer i sin helhet** akkurat nå, det finnes i praksis ingen CI-gating, og mye kritisk tilstand (inkl. RAG-tilgangskonfig) ligger ukommittert på én utviklermaskin. Totalbilde: **sterk kjerne og pilotnær demo-evne, men «to personer og en fjelltur unna» å miste reproduserbarhet.**

### Viktigste funn

1. **[bevist]** CellProtocol-kjernen: 565 tester, 0 feil, 21,7 s. Rent arbeidstre. Dette er den sterkeste enkeltevidensen i hele porteføljen.
2. **[bevist]** CellScaffolds XCTest-suite dør med signal 6 (uncaught `NSInvalidArgumentException`) i `AIAssistantThreadCellTests`, utløst fra `GeneralCell.swift:1393` (`schemaDict` er ved runtime en String, ikke ordbok). Konsistent i 2 av 2 kjøringer. Suiten dør etter 3 testtilfeller — **hele suiten er i praksis rød**.
3. **[bevist]** Testene leser/skriver ekte brukertilstand (`~/CellsContainer/PrivateVaults/...`). `~/CellsContainer/` har **30 301 oppføringer** på toppnivå uten opprydding.
4. **[bevist]** HAVENAgentD: 111 tester i 25 suiter, alle grønne. Daemonen kjører via launchd, lytter kun på loopback (43110), krever token (401 uten), og automatiseringspolicyen er allowlistet med argumentvalidering og «draft, ikke send». Uvanlig god sikkerhetsdesign for et prosjekt i denne fasen.
5. **[bevist]** Conference-demo E2E lokalt: 12/13 bestått (2,8 min). Staging (`staging.haven.digipomps.org`) svarer 200 på 0,23 s med frisk `/health`.
6. **[bevist]** RAG-økosystemet virker: 170/171 pytest grønne, live korpus verifisert via API og DB (395 aktive dokumenter, alle fire kildetyper rutet og gjenfinnbare).
7. **[bevist]** Ingen CI-testgating på kjernerepoene: bare notify-/sync-workflows (unntak: DiMyMint har `swift-ci.yml`). All testkjøring skjer manuelt/lokalt.
8. **[bevist]** Konfigurasjonsdrift: `rag_service` har 51 ukommitterte filer, inkludert `rag_cases.yml`-endringen som styrer tilgang til private kildetyper. DiMyDevRAG-revisjonen i går viste at dokumentasjon ble utdatert **samme dag** den ble skrevet.
9. **[bevist]** Dokumentasjonen er uvanlig ærlig og omfattende: 35 Book-kapitler + maskinlesbar katalog, 115 dokumenter i CellScaffold/Documentation, eksplisitte «hva den ikke gjør ennå»-lister i HAVENAgentD og «Important truth about current parity» i Book Home.
10. **[bevist]** Ingen hemmeligheter i git: ingen sporede .env-filer, nøkler via Environment/Keychain; eneste treff i secret-skann var utkommentert eksempelkode.

### Viktigste risikoer

1. **Rød hovedsuite skjult av vaner** — krasjet i CellScaffold-testene maskeres lett av pipe-bruk (`| tail` gir exit 0); uten CI oppdages ikke regresjonen.
2. **Buss-faktor 1 på tilstand**: kritisk konfig (RAG-ruting, staging-tilgang, agent-binærer) lever ukommittert eller kun på én maskin.
3. **Robusthet i dekode-stier**: kjernen aborterer på uventet persistert tilstand i stedet for å feile kontrollert — samme mønster kan ramme produksjon ved korrupte/eldre vault-data.
4. **Ingen dokumentert, reproduserbar «fersk bruker»-reise** uten utviklerhjelp (login-terskelen på Porthole; personas er demo-artefakter).
5. **Autorisasjonsgrenser er dokumentert, men delvis ubevist**: rag_service public-ruter er case-filtrert, ikke bruker-autorisert (kjent og dokumentert); scaffold-rollegrenser testes i smoke, men ikke systematisk mot fiendtlig bruk.
6. **DiMy-betalingssporet er dev-modus**: nøkkelforvaltning/HSM/rotasjon gjenstår; testdekningen (9 tester) er tynn for pengelogikk.
7. **UI-detaljlekkasje**: rå UUID-er, keypaths (`identity.proofs.scaffold.admin.entry = true`), `entity://`-URI-er og invite-tokens vises i flatene; blandet norsk/engelsk; observert mørk-på-mørk-tekst.
8. **Binding-appen er ubevist i denne revisjonen**: bygget lokalt i natt (DerivedData-spor), men tester ble ikke kjørt og appen ble ikke startet.
9. **Repo-hygiene**: 36 ukommitterte filer i CellScaffold (music publishing i flukt), 44 i DiMyDocuments, 27 i sprout; gamle repoer (HAVEN_MVP, CellUtility) har uavklart status.
10. **Ekstern reviewer-avhengighet**: Codex-CLI-en lokalt kunne ikke kjøre (modell/versjonskonflikt, prosessen hang og døde) — ekstern kodegjennomgang er i praksis utilgjengelig akkurat nå.

### Hva er faktisk imponerende

- 565 grønne kjernetester på et protokollag med identitet, agreements, resolver, replay og skeleton-kontrakter **[bevist]**.
- En fungerende, deployet web-runtime (Porthole) der CellConfigurations rendres, personas byttes, og en conference-demo består E2E-tester **[bevist]**.
- HAVENAgentD-sikkerhetsmodellen: signerte remote intents med trusted-issuer-policy, eksplisitt approve/reject, loopback-token-bridge, allowlistet AppleScript med regex-validerte argumenter **[bevist i kode/config]**.
- Dokumentasjonskulturen: Book + katalog + RAG-indeksering + ærlige paritetsvurderinger **[bevist]**.
- Utviklingsfarten: 244 commits siste 30 dager i CellScaffold alene **[bevist]**.

### Hva er fortsatt prototype/ubevist

- Chat/co-pilot-workbench (krasjet skjer nettopp i AI-assistent-tråd-cellen; canary-tester finnes, men flaten er skjør) **[bevist krasj / uavklart modenhet]**.
- Binding som selvstendig app-produkt (separasjonsplan dokumentert, ikke verifisert her) **[intensjon + svake byggspor]**.
- DiMy-micropayments i noe som ligner produksjon **[bevist dev-modus]**.
- Multi-bruker-sikkerhet ende til ende (dokumenterte grenser, ikke adversarielt testet) **[uavklart]**.
- Onboarding for ekte, ukjente brukere **[uavklart]**.

---

## 2. Modenhetsmatrise (0–5)

| Område | Score | Evidens | Confidence | Største gap | Anbefalt neste steg |
|---|---|---|---|---|---|
| Core CellProtocol | **4** | 565/565 tester grønne, rent tre, 118k LOC, 97 testfiler [bevist] | Høy | Abort-på-dekodefeil (GeneralCell:1393-mønsteret); Explore-kontrakter ikke backfylt for legacy-celler | Gjør dekode-stier ikke-fatale; backfill Explore-kontrakter |
| Skeleton/CellConfiguration | **3** | Spec i Book 12/22; aktiv skeleton-iterate-testing m/ artefakter fra i går; parity-suiter i Binding-scripts [bevist artefakter] | Middels | Renderer-pariteter web/SwiftUI ikke samlet bevist grønt i én kjøring | Én samlet paritetskjøring med rapport pr. commit |
| CellScaffold/Porthole | **3** | Kjører lokalt + staging m/ TLS og health; 12/13 E2E; 719 commits; MEN testsuiten krasjer og 36 filer dirty [bevist] | Høy | Rød XCTest-suite; monolittisk App-modul (329k LOC) | Fiks krasjen, grønn suite i CI, del opp App-target |
| Binding/HAVEN native app | **2** | Bygget i Xcode i natt (DerivedData) [sannsynlig]; 39 testfiler finnes; tester ikke kjørt her; separasjonsplan dokumentert [intensjon] | Lav | Ingen verifisert bygg+test-kjøring i denne revisjonen | Skriptbar `xcodebuild test`-bane + kjør den |
| HAVENAgentD | **4** | 111/111 tester; kjørende daemon; token-gated loopback; signert+notarisert pkg (tidligere verifisert); ærlig «gjør ikke»-liste [bevist] | Høy | Operatør-mynteverktøy gjenstår; sprout-API-integrasjon delvis | Fullfør operatørverktøy; pilotér mot Victoria |
| Chat/co-pilot/workbench | **2** | Flater og canary-spec finnes; Co-Pilot Chat-knapp i UI; krasjen sitter i AIAssistantThreadCell [bevist] | Middels | Stabilitet + persistensrobusthet i tråd-celler | Fiks type-forvirringen; gjør canary til CI-gate |
| Event/conference-surfaces | **3–4** | 12/13 E2E lokalt; staging live; Arendalsuka-konfig under arbeid; QR-utfordringstest feiler lokalt [bevist] | Høy | Én rød smoke (bootstrap-owner-bevis); tilstandsavhengighet lokalt/staging | Reproduser QR-feilen på ren instans; grønn suite mot staging |
| DiMy/payment/usage-quota | **2** | 9+17 tester grønne; ærlig README (dev-Ed25519, HSM/KMS pending); regulatoriske rammedokumenter finnes; Stripe-skills installert [bevist/intensjon] | Middels | Nøkkelforvaltning, produksjonskrypto, tynn testdekning | Hold claims i dev-språk; vektorbaserte kontrakttester |
| Dokumentasjon/grant-readiness | **4** | 35 Book-kapitler + katalog; 115 scaffold-docs; gap-analyse oppdatert; DiMyDevRAG-korpuspolicy; ærlige paritetsnotater [bevist] | Høy | Stale-risiko (bevist i går: utdatert samme dag); investor-/grant-tekster ikke revidert her | Freshness-sjekk i RAG (finnes delvis); claim-review før ekstern bruk |
| Test/CI/deploy/release | **2** | Suiter finnes og de fleste er grønne lokalt; deploy-script m/ health/build-verifisering og dokumentert flyt; MEN ingen CI-gating, rød hovedsuite, 51 dirty i rag_service [bevist] | Høy | Ingen automatisk kvalitetsport noe sted | GitHub Actions: bygg+test på PR for de 4 kjernerepoene |

---

## 3. Kodekvalitet

**Arkitektur og modulgrenser.** Tydelig lagdeling på tvers av repoer: CellBase (protokoll) / CellApple / CellVapor i CellProtocol; Cells + ConfigurationFactory-mønsteret i CellScaffold; HavenAgentD delt i Bootstrap/Runtime/MacAutomation med eksplisitte trust-grenser **[bevist i struktur]**. Svakhet: CellScaffolds `Sources/App` er en monolitt på ~329k LOC der celler, tjenester og kontrollere bor i samme target — byggetid og koblingsrisiko vokser **[bevist størrelse, sannsynlig konsekvens]**.

**Naming/lesbarhet.** Konsistent og selvforklarende (`AccessRequirementPromptConfigurationFactory`, `PortholeLifecycleController`). Lav TODO-tetthet (33/19/1 i hhv. CellProtocol/CellScaffold/Binding) — enten god disiplin eller at intensjoner bor i docs i stedet; docs-volumet tyder på det siste **[bevist tall]**.

**Feilhåndtering.** Kjernefunnet: `exploreContractRegistrationDecision` antar at `schemaDict` er en ordbok; når persistert tilstand inneholder en String, aborterer prosessen (`unrecognized selector`). Dette er et mønster, ikke bare én linje: dekoding av gammel/fremmed tilstand må aldri kunne ta ned prosessen **[bevist krasj]**. Positivt: strukturerte felt-feil i VaultCell-testene og «structured field errors»-mønsteret finnes allerede **[bevist testnavn]**.

**State/dataflyt.** Vedvarende tilstand i `~/CellsContainer` uten synlig GC/kompaktering (30 301 oppføringer, 9,7 MB `.DS_Store`) **[bevist]**. Resolver-eventer logger «Saving identity named cells: 38 identities, 346 references» ved hver registrering under test — hyppig full lagring **[bevist logg; ytelseskonsekvens sannsynlig]**.

**Async/concurrency.** Actor-basert design i DiMy-cellene (WalletCell/AccessCell som «runtime actors») og async/await gjennomgående **[bevist i README/kode-signaturer]**. Ikke adversarielt vurdert her.

**Duplisering/døde stier.** `"legacy"`-rute registrert i scaffold; deprecated API-er beholdt med annotasjon (`setInterceptValueForKey`); gamle repoer (HAVEN_MVP, CellUtility «history»-remotes, sprout med 27 dirty) uten tydelig «arkivert»-markering **[bevist]**.

**Kompatibilitet Swift/web/server.** Skeleton-spec med dokumenterte encode/decode-kompatibilitetsfikser (objekt-wrapper, `flowELementSkeleton`-normalisering) og parallelle runtimes (Py/Go/Rust-porter, PyCellProtocol 29 grønne tester med wire-codec- og fixture-tester) **[bevist]**.

**Skjulte sideeffekter.** Tester som muterer ekte brukerdata er den største: en testkjøring i dag skrev til `~/CellsContainer/PrivateVaults/` **[bevist filsti i krasjlogg]**.

**Testenes kontraktsdekning.** Kjernetestene tester kontrakter (roundtrip, determinisme, strukturerte feil, replay) — ikke bare happy path **[bevist testnavn i logg]**. DiMyMicropayments har derimot bare 9 tester for utstedelse/spend/redeem — for tynt for pengelogikk **[bevist]**.

---

## 4. Brukergrensesnitt og opplevelse

Vurdert fra faktisk kjørende lokal Porthole (:9090), login-siden, og ferske test-skjermbilder (conference scaffold-setup, music publishing mobil) **[bevist]**.

- **Førsteinntrykk:** Login-siden («Open Porthole · HAVEN», «Sign in · HAVEN») er visuelt gjennomarbeidet med eget designspråk (paper/ink-palett, Fraunces/Geist-typografi). Mental modell for en ny bruker er derimot uklar: ingenting på login forklarer hva HAVEN *er*.
- **Forklarer UI hva brukeren kan gjøre?** Delvis. Conference-flatene har gode forklaringstekster («Tilgang kommer fra eksplisitt admin entry-proof …»), og musikk-konsollen forklarer roller (Reviewer/Editor/Publisher) i klart språk. Men flatene er konfigurasjonssentrerte — brukeren ser «Aktiv konfigurasjon: …» og Library(91) som primærnavigasjon, som er en utvikler-mental-modell.
- **Navigasjon/IA:** Breadcrumbs + Tilbake + Menus fungerer; toolbar-navigasjonstest består. Library med 91+ konfigurasjoner uten kuratering blir fort uoversiktlig for ikke-utviklere.
- **Tomme/lastende/feil-tilstander:** «Handlingen er utført.»-banner finnes (generisk). Feiltilstander ble ikke systematisk provosert i denne revisjonen **[uavklart]**.
- **Responsivitet:** Musikk-konsollen rendrer korrekt i mobilviewport (dedikerte mobile-smokes med artefakter) **[bevist]**.
- **Tilgjengelighet:** Ikke systematisk testet **[uavklart]**, men skjermbildet av scaffold-setup viser tekstblokker som fremstår mørk-på-mørk (Admin Entry / Identity Linking-kortene) — enten skjult innhold eller reell kontrastfeil **[bevist observasjon, årsak uavklart]**.
- **Språk:** Blandet norsk/engelsk i samme flate («Owner Status» + «Oppdater status»; «Innløs invite-token» + engelske rollebeskrivelser). For pilot med norske brukere bør én språklinje velges pr. flate.
- **Lekkasje av interne detaljer:** Rå konfigurasjon-UUID øverst i flaten, keypath-strenger som UI-tekst (`identity.proofs.scaffold.admin.entry = true`), `entity://TheButterpopCollective`, `conference-skeleton-iterate-bc616f75` og rå invite-tokens synlige **[bevist skjermbilder]**. Aksepterbart på admin-flater, ikke i deltaker-/artistreiser.
- **Sideeffekter tydelige/opt-in:** Sterkt på agent-siden (mail = synlig draft, aldri autosend) **[bevist config]**. I web-UI er handlingsknapper («Bootstrap scaffold owner») umiddelbare uten bekreftelsesdialog **[bevist skjermbilde]**.

---

## 5. Produkt- og brukerreiser

**Reiser som beviselig fungerer ende til ende (demo-nivå):**
- *Conference-organisator/deltaker (demo-personas):* login → Library → conference-konfigurasjoner → persona-bytte → deltaker-program → toolbar-navigasjon. 12 E2E-tester består lokalt **[bevist]**. Staging er oppe, men samme suite ble ikke kjørt mot staging i denne revisjonen (bevisst, for ikke å skrive til delt miljø) **[uavklart på staging]**.
- *Musikk-arbeidsflate (Butterpop Studio):* opprette/vise workspace, invitere medlem (token + haven://-lenke), rolleforklaringer, grant-plan — på mobil og desktop **[bevist artefakter fra i går]**; aktiv utvikling, delvis ukommittert.
- *Utvikler-/dokumentreise:* /book-browser, RAG-oppslag med kildetyper og case-status, vault-API **[bevist RAG-delen; /book ikke klikket gjennom her]**.
- *Operatør/agent:* daemon kjører, heartbeat, token-bridge, bootstrap-probe mot staging dokumentert **[bevist runtime; sprout-flyt ikke kjørt her]**.

**Hvor stopper reisene?**
- Ved «fersk bruker uten utvikler»: kontooppretting/onboarding-flyt er udokumentert utenfor demo-personas **[uavklart]**.
- Ved betaling: DiMy-flyt er in-memory/dev-modus — ingen ekte verdireise **[bevist status]**.
- Ved chat: co-pilot finnes som flate, men stabilitetsbeviset mangler (krasjen sitter i nettopp tråd-cellen) **[bevist]**.

**Demo vs. pilot vs. produkt:** Conference + musikk = solid **demo**, nær pilot. AgentD = nær **pilot** (Victoria). Chat-workbench, DiMy, Binding-app = **prototype**. Ingenting er **produkt** i drift-forstand (ingen CI, ingen overvåket produksjonsmiljø utover staging).

---

## 6. Sikkerhet, personvern og tillit

- **Secrets:** Ingen sporede .env/hemmeligheter i git **[bevist skann]**; nøkler i Keychain (KeychainManager; funn var utkommentert eksempel), server-nøkler via Environment-oppslag **[bevist]**. Agentd-token i config-fil i Application Support (bruker-lesbar) — akseptabelt for loopback-bridge, men bør nevnes i trusselmodellen **[bevist]**.
- **Owner/grant/capability-modell:** Eksplisitt i UI («Role Grant Boundary», admin entry-proof-tekst) og i AgentD (trusted-issuer-verifisering av signerte intents, eksplisitt approve/reject før sideeffekt) **[bevist konfig/UI]**. Adversariell testing av grensene: ikke utført **[uavklart]**.
- **Logging:** AgentD skriver redacted metadata for SecretCredentialCell **[bevist README]**; scaffold-testlogger printer identitets-/referansetellinger, ikke innhold **[bevist]**. Full logg-gjennomgang for PII ble ikke gjort **[uavklart]**.
- **Lokal daemon:** Loopback-only, token-gated (verifisert 401), launchd KeepAlive, allowlistet automatisering med argument-regex, `requiresUserSession`, mail kun som synlig draft **[bevist]**. Dette er et forbilledlig mønster.
- **Nettverk/transport:** Alle lokale tjenester binder 127.0.0.1 **[bevist lsof]**; staging bak nginx/TLS **[bevist + dokumentert]**. Staging-SSH-detaljer (IP, nøkkelsti) står i repo-docs — lav risiko, men unødvendig presist for et repo som kan bli delt **[bevist]**.
- **Authz/authn:** Porthole web krever login (303 → /login) **[bevist]**. Kjent, dokumentert gap: rag_service public-ruter er case-filtrert men ikke bruker-autorisert, og dokumentnedlasting er sensitiv — driftsmodellen (private instanser, INSTANCE_CASE_IDS, forskningstokens) er dokumentert i DiMyDevRAG/ACCESS_MODEL **[bevist docs + delvis runtime]**. Ikke egnet for offentlig multi-tenant før server-side authz finnes.
- **Betaling/regulatorisk språk:** DiMyMicropayments-README er eksemplarisk edruelig (dev-signing, «pending for production»). Vokt claims når Stripe-integrasjon starter (skills ligger klare i AgentD-repoet) — DiMy-guardrails-skillen bør brukes på alt utadrettet **[bevist status/intensjon]**.

---

## 7. Test, CI og deploy

**Kjørt i denne revisjonen (alle på denne maskinen, 2026-07-10):**

| Suite | Resultat | Tid |
|---|---|---|
| CellProtocol `swift test` | **565 bestått, 0 feil** | 21,7 s |
| CellScaffold `swift test` | **KRASJ** (signal 6 etter 3 tester; 2/2 kjøringer) | — |
| HavenAgentD `swift test` | **111 bestått** (25 suiter) | 5,1 s |
| PyCellProtocol pytest | **29 bestått** | 0,12 s |
| rag_service pytest | **170 bestått, 1 hoppet over** | 7 m 28 s |
| DiMyMicropayments `swift test` | **9 bestått** | <1 s |
| DiMyMint `swift test` | **17 bestått** | <1 s |
| Playwright conference-smoke (lokal :9090) | **12 bestått, 1 feilet** (QR/bootstrap-owner-bevis) | 2,8 min |

**Ikke kjørt / blockere:** Binding (`xcodebuild test` — tung workspace-kjøring; kun byggspor fra i natt), Playwright mot staging (bevisst utelatt for ikke å mutere delt miljø), GoCellProtocol/RustCellProtocol (tidlige porter, nedprioritert), Codex ekstern review (CLI-modellkonflikt; prosess hang og ble drept).

**Bygg/deploy:** Staging deployes med `scripts/deploy-staging.sh` (SSH → git-oppdatering → Docker-bygg på VPS → helse-/revisjonssjekk `GET /health/build`) **[bevist script/docs; ikke kjørt her]**. Ingen CI-bygde images/registry. RAG kjører som Docker Compose lokalt (verifisert) og på VPS (dokumentert).

**Mangler for release-confidence:** (1) grønn CellScaffold-suite, (2) CI som kjører alle suitene pr. PR, (3) Binding-tester i skriptbar bane, (4) staging-smoke som canary etter deploy, (5) commit av rag_service-konfig.

**Minimal smoke-suite pr. surface (forslag):**
- *Porthole web:* login → åpne én Library-konfig → utfør én handling → assert på dynamisk verdi (finnes i praksis: conference-smoke; gjør den til gate).
- *Chat/co-pilot:* personal-chat-prompt-canary (finnes) + «restore tråd fra persistert tilstand»-test (mangler — nettopp der krasjen bor).
- *AgentD:* eksisterende deterministic smoke (retry/renewal) + bridge-auth-probe (`401` uten token, `200` med).
- *RAG:* `rag_runtime_check.py` + case-status + én retrieve pr. kildetype (alt finnes; skriptes sammen).
- *Binding:* én `xcodebuild test`-kjøring av SkeletonParity-suiten.
- *DiMy:* vektor-basert issue→spend→redeem-kontraktstest (delvis: `Tests/vectors` finnes).

---

## 8. Dokumentasjon og claim safety

- **Stemmer med kode/runtime?** I hovedsak ja, med bevist unntak: DiMyDevRAG-bootstrap-dokumentene var utdatert samme dag (case-ruting endret etter skriving) — oppdaget og rettet i går. Lærdom: dokumenter runtime-avhengige fakta med dato + verifikasjonskommando (nå gjort i DiMyDevRAG) **[bevist]**.
- **Skiller visjon fra implementert?** Ja, uvanlig godt: «What it does not do yet» (AgentD), «Important truth about current parity» (Book Home), «pending for production» (DiMy) **[bevist]**.
- **Overclaims?** Ikke funnet i utvikler-docs. Investor-/grant-tekster (DiMyDocuments, InnovasjonNorge-mappen) ble ikke revidert i denne runden **[uavklart]** — kjør haven-claim-review før ekstern bruk.
- **How to run / verify:** Sterkt der det teller (Quickstart, deploy-rapport, DiMyDevRAG-runbooks med eksakte kommandoer). Svakt for Binding (ingen verifisert test-kommando i README).
- **Egnethet pr. målgruppe:** Utviklere: god. Pilotbrukere: mangler (ingen brukerguide for deltaker/artist-reisene). Investorer/grant-reviewers: råmaterialet finnes, men trenger claim-review og ferske evidenspakker.

---

## 9. Gap Register

| # | Gap | Alvor | Repo/surface | Brukereffekt | Teknisk årsak | Evidens | Løsning | Størrelse |
|---|---|---|---|---|---|---|---|---|
| 1 | CellScaffold-testsuite krasjer totalt | **P0** | CellScaffold (+CellProtocol) | Ingen release-tillit; regresjoner usynlige | `schemaDict` dekodes som String; abort i `GeneralCell.swift:1393`; test leser ekte vault | 2/2 kjøringer, full logg | Defensiv dekoding + testisolasjon (temp-container) | M |
| 2 | Ingen CI-testgating | **P0** | Alle kjernerepoer | Rød kode kan merges/deployes usett | Kun notify-workflows | `.github/workflows`-innhold | Actions: bygg+test på PR (4 repoer) | M |
| 3 | Ukommittert kritisk konfig | **P1** | rag_service (51 filer), CellScaffold (36) | Tilgangsstyring/arbeid tapes ved maskinfeil; ikke reproduserbart | Drift uten commit-disiplin på config | `git status` | Commit/review rag_cases.yml m.fl.; rydd arbeidstrær | S |
| 4 | Public RAG-ruter uten bruker-authz | **P1** | rag_service | Private dokumenter kan eksponeres ved feil deploy-modell | Design (case-filter ≠ authz) | Egen docs + rutekode | Hold private instanser; server-side authz før offentlig bruk | L |
| 5 | Tester muterer ekte brukerdata | **P1** | CellScaffold/CellProtocol | Flaky tester; risiko for datatap lokalt | Ingen container-isolasjon i testoppsett | Krasjloggens filsti; 30k dirs | `--root`-aktig isolasjon (AgentD har mønsteret) | M |
| 6 | CellsContainer vokser uten GC | **P1** | Runtime alle apper | Disk/ytelse forringes stille | Ingen opprydding/kompaktering | 30 301 oppføringer | Retensjonspolicy + GC-jobb | M |
| 7 | QR/bootstrap-owner-smoke rød lokalt | **P2** | CellScaffold conference | Identitetskobling-demo kan feile | Tilstandsavhengig (allerede bootstrappet?) el. regresjon | Playwright-feil + skjermbilde | Reproduser på ren instans; gjør testen idempotent | S |
| 8 | UI lekker interne detaljer | **P2** | Porthole-flater | Forvirrer/skremmer ikke-tekniske brukere | Keypaths/UUID/URI-er som UI-tekst | Skjermbilder | Presentasjonslag for identitet/bevis; skjul bak «detaljer» | M |
| 9 | Blandet språk + kontrastfeil | **P2** | Porthole-flater | Uprofesjonelt førsteinntrykk; a11y-risiko | Ingen språkpolicy pr. flate; theme-bug | Skjermbilder | Språkvalg pr. flate; kontrast-audit | S–M |
| 10 | DiMy-testdekning tynn | **P2** | DiMyMicropayments | Pengefeil oppdages sent | 9 tester totalt | Testkjøring | Vektor-/property-tester for kontraktene | M |
| 11 | Binding ubevist i skriptbar bane | **P2** | Binding | App-regresjoner usynlige | Ingen CLI-testkommando i bruk | Ikke kjørt her | `xcodebuild test`-script + kjør i CI | M |
| 12 | Gamle repoer/branches uavklart | **P3** | sprout, HAVEN_MVP, DiMyDocuments-branch | Forvirring om hva som er sannhet | Manglende arkiv-markering | git-status-kart | ARCHIVED.md / branch-rydding | S |
| 13 | Stale Playwright-HTML-rapport (mars) | **P3** | CellScaffold | Villedende historisk artefakt | Rapport ikke regenerert | Fildato | Regenerer/slett ved neste kjøring (ikke slettet nå) | S |

---

## 10. Neste 30/60/90 dager

**30 dager — høyest leverage, små sikre steg:**
- *Kode:* Fiks P0-krasjen (defensiv dekoding i GeneralCell + testisolasjon). Gjør CellScaffold-suiten grønn.
- *Testing:* GitHub Actions med bygg+test for CellProtocol, CellScaffold, HavenAgentD, PyCellProtocol. Conference-smoke som post-deploy-canary mot staging (med idempotent QR-test).
- *Sikkerhet:* Commit + review av rag_service-konfig; kort trusselmodell-notat for agentd-token og staging-SSH-detaljer.
- *Docs:* Dato + verifikasjonskommando-mønsteret (fra DiMyDevRAG) rulles ut til Book-kapitler som beskriver runtime-tilstand.
- *UX:* Kontrast-audit av scaffold-setup-flaten; språkpolicy-beslutning (norsk først på deltakerflater).

**60 dager — pilotklarhet:**
- *Kode/testing:* Binding `xcodebuild test` i CI; skeleton-paritet som samlet rapport; DiMy vektortester.
- *UX/produkt:* Én dokumentert «fersk bruker»-reise (invitasjon → login → deltakelse) uten utviklerhjelp, med onboarding-tekster og feilmeldinger; presentasjonslag som skjuler keypaths/UUID-er på deltakerflater.
- *Sikkerhet:* Adversariell test av rolle-/grant-grensene i scaffold (én dags øvelse, dokumentert); RAG privat-instans-sjekkliste kjørt på VPS.
- *Drift:* CellsContainer-retensjon + GC; CI-bygde images til registry.
- *Evidence/GTM:* Victoria-pilot for AgentD med operatør-mynteverktøy ferdig; evidenspakke (skjermbilder + testlogger) for grant-søknader, kjørt gjennom haven-claim-review.

**90 dager — produksjons-/partnerklarhet:**
- *Kode:* Del opp CellScaffold App-target i moduler; backfill Explore-kontrakter.
- *Testing:* Full pipeline: PR-gate → staging-deploy → canary → rulletilbake-øvelse gjennomført én gang.
- *Sikkerhet:* Server-side authz-design for offentlig RAG-eksponering (eller eksplisitt beslutning om å forbli privat); nøkkelrotasjonsseremoni-design for DiMy.
- *Produkt:* Chat-workbench stabilisert med restore-tester; Binding standalone-separasjon verifisert med egen suite.
- *GTM:* Partner-demo-miljø atskilt fra staging; pilotavtale-tekster claim-reviewet.

---

## 11. Endelig vurdering

**Hvor langt har vi kommet?** Omtrent to tredjedeler av veien til en troverdig pilot, og lenger enn de fleste prosjekter på dokumentasjon og sikkerhetsdesign — men med en release-kjede som fortsatt er håndverk. Kjernen (protokoll + agent + demo-flater) er reell og testet; det som mangler er industrialisering: CI, isolasjon, reproduserbarhet og én bevist brukerreise uten utviklerhender.

**Sterkeste kjerne:** CellProtocol-runtimen med kontraktstester (565 grønne) og HAVENAgentD-sikkerhetsmodellen. Dernest dokumentasjonskulturen — den er en faktisk konkurransefordel for agent-samarbeid.

**Hva må ikke påstås ennå:** «Produksjonsklar», «multi-tenant-sikker», «betalinger fungerer», «brukere kan onboarde selv», eller at CellScaffold-testene er grønne. Heller ikke «dokument-ACL i RAG» (eksplisitt advart mot i egne docs — respekter det).

**Bygg først:** (1) P0-krasjfiks + testisolasjon, (2) CI-gating, (3) én komplett fersk-bruker-reise på staging med artefakter. Alt annet er sekundært til disse tre.

**Kutt/parker:** Go/Rust-portene (til Py-porten har bevist verdi), HAVEN_MVP/CellUtility/gammel sprout (arkiver eksplisitt), offentlig RAG-eksponering (parker til authz finnes), og nye surface-familier inntil chat-workbenchen er stabil.

**De 3 mest manglende bevisene for pilot-klarhet:**
1. **Grønn, CI-håndhevet totalkjøring** av alle suitene (inkl. fikset CellScaffold og kjørt Binding) på ren maskin/container — beviser reproduserbarhet.
2. **Én fersk bruker gjennomfører conference- eller musikk-reisen på staging uten hjelp**, dokumentert med opptak/artefakter — beviser produkt, ikke demo.
3. **En adversariell dags-test av tilgangsgrensene** (scaffold-roller + RAG-instans) med rapport — beviser at sikkerhetsdesignet holder i praksis, ikke bare i dokumentasjon.

---

## Evidensappendiks

**Kommandoer kjørt (utvalg):**
- `git status/branch/log/rev-list` på 20 repoer (kart i seksjon om scope)
- `swift test` i CellProtocol, CellScaffold (×3), Binding/HavenAgentD, DiMyMicropayments, DiMyMint
- `pytest` i rag_service (170/1) og PyCellProtocol (29)
- `npx playwright test playwright/conference-demo.smoke.spec.js` mot `http://127.0.0.1:9090` (12/13)
- `curl`-prober: :9090 (root/login/health/porthole), :43110 (401-auth), :8102 (case-status, retrieve), staging (200 + /health)
- `lsof -iTCP -sTCP:LISTEN`, `launchctl list`, `docker ps`, `docker exec … printenv` (redigert), `psql`-oppslag i rag_dimy
- Secret-skann (grep-mønstre) over Sources i 7 repoer; `git ls-files`-sjekk for .env

**Filer inspisert (utvalg):** `GeneralCell.swift:1375–1409`, `KeychainManager.swift:60–84`, `RAGGatewayConfig.swift`, `sync_orchestrator.py`, `sync_folder.py`, `rag_cases.yml` (+diff), Playwright-spec:646–661, `playwright.config.js`, HavenAgentD `config.json` (redigert), launchd-plist, Book 00-Home, Gap_Analysis.md, HavenAgentD/Binding/DiMyMicropayments README-er, Vegar-deploy-rapport, DiMyDevRAG (alle 16 filer, forrige oppgave).

**Skjermbilder/runtime:** conference scaffold-setup failure-screenshot (rå UUID, keypath-tekst, mørk-på-mørk-observasjon), music-publishing mobil-smoke (roller, tokens, `entity://`-URI), login-side-HTML.

**Nettkilder:** Ingen brukt — alle fakta er lokale. (Staging-URL-en er prosjektets egen.)

**Ikke verifisert / blockere:**
- Binding-appens tester og kjøring (kun DerivedData-byggspor fra i natt)
- Playwright mot staging (bevisst utelatt — muterer delt miljø)
- VPS-tilstand utover HTTP-prober (ingen SSH-innlogging gjort)
- Investor-/grant-tekstene i DiMyDocuments/InnovasjonNorge
- Tilgjengelighet (a11y) systematisk; feil-/tomtilstander systematisk
- Ekstern Codex-review (CLI-modellkonflikt: `gpt-5.6-sol` krever nyere Codex; bundlet CLI hang og ble drept)
- `dimy_prompts`-casen og 8101-instansens innhold (kun helse sjekket)
