# PLAN — fra mockup til visionOS-simulator

**Status: G1 godkjent 2026-09-16, G2 godkjent 2026-09-16** (Kjetils svar på beslutningsspørsmålet; `STATUS.md`).
G1-GUI venter. Kode finnes som patcher i `handoff/patches/` og legges bare i egne worktrees av `handoff/KJOR-SELV-visionos.command`.
Planen svarer på Kjetils spørsmål 2026-09-16: *«Kan du implementere denne mocken og kjøre det i simulatoren med VisionOS?»*

Grafikk: `images/plan-simulator-v1.png` — samme innhold som §2, tegnet som tre baner (Kjetil, Losen, Macen).

Merking: `[belagt: fil:linje]` = lest i koden (Macen 16.09 der ikke annet står), `[vurdering]` = mitt anslag,
`[usikker]` = ikke sjekket. §7 sier hva den uavhengige motlesningen («Fabel») endret.

## 0. Kort svar

Ja — i skiver. Den raskeste ærlige veien til «det kjører i simulatoren» er å måle først (steg 0–1), så få
appen til å **starte** der som nativ visionOS-app (steg 2), og parallelt bygge den første skiven av mocken
— baksiden (steg 3) — som er plattformnøytral og kan vises på Mac før simulatoren er klar. De andre
scenene (inspektør/FlowTap, rommet) og «mange Portholes som vinduer» er egne PDD-er etterpå.

Tre ting bestemmer tempoet, og ingen av dem kan jeg gjøre alene herfra:

1. **Bygg og simulator kjører bare på Macen.** Skyen og Linux-VM-en (`device_bash`) har verken `xcodebuild`
   eller simulator. Codex-MCP er frakoblet. Veiene som finnes: jeg styrer Terminal på Macen (skjermstyring),
   eller Kjetil kjører ett skript selv, eller køen (`_losen-queue`) — §3.
2. **Vi vet ikke om visionOS-SDK-en og simulator-kjøretiden er installert** [usikker]. De er to forskjellige
   ting: SDK-en følger Xcode og holder for å *kompilere* (steg 1); kjøretiden (~7–8 GB egen nedlasting
   [vurdering]) trengs for å *starte* appen (steg 2). Steg 0 sjekker begge på ett minutt.
3. **Portordene.** Arbeidsflyten krever Kjetils «G1 godkjent» før kode, «G1-GUI godkjent» for bildet som
   skal bygges (v2 av baksiden, med tomtilstander — §2 steg 3), og «G2 godkjent» for denne planen.
   Jeg setter aldri en port selv.

## 1. Hva «mocken» består av, og hva som finnes i dag

| Scene (bilde i `images/`) | Formålsgren | Bygger på data som finnes i dag? | Størrelse [vurdering] | Plass i planen |
|---|---|---|---|---|
| 2 `bakside-datastrommer-v1.png` — baksiden av flaten | B `purpose://candidate.porthole.backside` | **Tre av fire soner: dataene finnes, men må hentes fra cellen, ikke fra view-modellen.** Absorberte celler = cellens `cellConfiguration.cellReferences` (privat, intern getter `getCellConfiguration()`) [belagt: OrchestratorCell.swift:22,380,447]; view-modellens egen kopi settes bare i `load(configuration:)` og er tom etter kaldstart [belagt: PortholeBindingViewModel.swift:375; OrchestratorCell.swift:479–491]. Tilkoblingsstatus per label finnes: `attachedStatuses` → `ConnectionStatus(name:connected:active:)` [belagt: GeneralCell.swift:2441–2447]. Puls = `flowElements` [belagt: PortholeBindingViewModel.swift:32,649], men elementene bærer bare valgfri `origin`, ikke label → et lite origin→label-oppslag må skrives. **Set/get-sonen: nei** — bare tekstlinjen `INTR:…` fra `CellResolver.logAction` [belagt: CellResolver.swift:3000–3011] (F3 mangler). | Middels: én ny visning i CellApple, bryter i redigeringsmodus, to felter + ett oppslag i view-modellen | **Steg 3** — første skive, kan gå parallelt med steg 2 |
| 1 `rommet-portholes-v1.png` — flere Portholes som egne vinduer | A `purpose://candidate.porthole.many` | Nei. `cell:///Porthole` er én identitetsunik celle; skeleton-rendereren har basen hardkodet 11 steder [belagt: `grep -c 'cell:///Porthole' SkeletonView.swift` = 11] | Stor: instansregister + base-kontekst i rendereren + `WindowGroup(for:)` + `UIApplicationSupportsMultipleScenes` | Egen PDD etter steg 4 |
| 3 `inspektor-flowtap-v1.png` — FlowTap-celle og inspektør | C `purpose://candidate.cell.traffic-inspection` | Halvveis: `FlowProbeCell` tar opp men videresender ikke; feed-intercepten i `GeneralCell` kan videresende [belagt: GeneralCell.swift:1074; OrchestratorCell.swift:88–128] | Middels: ny celle (`FlowTap`) med ventil + opptak, så en flate | Egen PDD |
| 4 `informasjonspress-rom-v1.png` — rommet | D `purpose://candidate.information-pressure.visible-adjustable` | Nei. Krever aggregat over alle celler + `ImmersiveSpace`/`RealityView` | Stor, og den eneste som er ekte romlig | Egen PDD, sist |

Alle fire er mockups (ikke Porthole-forhåndsvisning) uten tomtilstander — `images/README.md`. `FORMAALSSPEC.md` §3
krever `bakside-*-v2.png` med tomtilstander før G1-GUI for gren B.

## 2. Stegene

Hvert steg sier hva det innebærer, hvem som gjør det, hva Kjetil selv må gjøre, når, og hva som er beviset.

### Steg 0 — Forhåndssjekk på Macen (tørrkjøring, ~1 minutt, endrer ingenting)

| | |
|---|---|
| purposeRef | `purpose://candidate.platform.visionos-native` (hypotese H1 i `ANALYSE.md` §3) |
| innebærer | Kjøre `handoff/h1_compile_probe.sh` **uten** `--go`. Den skriver: Xcode-versjon, ledig disk (stopper under 30 GB), om `xrsimulator`-SDK finnes, om visionOS-simulatorkjøretiden finnes (`xcrun simctl list runtimes`), og branch/HEAD/antall ucommittede filer i Binding og CellProtocol. (Oppdatert 16.09 etter motlesningen: kjøretid og disk manglet i skriptet.) |
| utfører | Losen via skjermstyring **eller** Kjetil (én kommando, §3) |
| Kjetil gjør | Velger vei i §3. Sier steg 0 «BLOCKED» (SDK mangler) eller «Simulator-kjøretid: MANGLER»: installerer i Xcode › Settings › Components — bare han kan (Apple-ID, disk). Viser steg 0 **ucommittede filer > 0** i Binding eller CellProtocol: avgjør om de skal committes til en gren først — ellers måler steg 1 noe annet enn det som ligger i hovedtreet, og en rød baseline gir ingen H1-måling. |
| når | Så snart planen er lest — steget er lesing, ikke endring. Macen må være våken. |
| kommando (fra HAVEN-roten) | `zsh CellProtocolDocuments/Deliverables/PDD_haven-visionos_2026-09-10/handoff/h1_compile_probe.sh` |
| bevis | Utskriften i terminalen. «Tørrkjøring ferdig» = klar for steg 1. |

### Steg 1 — H1: byggeproben (`--go`, 15–45 minutter [vurdering])

| | |
|---|---|
| purposeRef | `purpose://candidate.platform.visionos-native` — `test.h1.compile-probe` |
| innebærer | Ren eksport av HEAD (`git archive`, rører ikke hovedtrærne) til `_h1-visionos-probe-<dato>/`; baseline-bygg for macOS; i eksportens `project.pbxproj` utvides `SUPPORTED_PLATFORMS` med `xros xrsimulator`, enhetsfamilie 7 og `XROS_DEPLOYMENT_TARGET = 26.0` (alle mål — det er en probe); CellApple og HAVEN bygges for `generic/platform=visionOS Simulator` med `CODE_SIGNING_ALLOWED=NO` (proben måler kompilering, ikke signering). Bygges med `-project` — schemet HAVEN er delt [belagt: Binding.xcodeproj/xcshareddata/xcschemes/HAVEN.xcscheme]. Feil per fil → `TESTRESULT.md#h1`, pluss hvor mye disk scratch tok. |
| hvorfor | Jeg fant **tre** feil ved lesing [belagt: ContentView.swift:1691,1699; RootView.swift:188; ScannerService.swift:288]. Kompilatoren finner den ekte listen — også i de åtte pakkeavhengighetene, som alle må kompilere for xrsimulator [vurdering]. Alt etter dette dimensjoneres av tallet. |
| utfører | Samme vei som steg 0. Skriptet gjør alt; ingen retting (handoff-regel 11). |
| Kjetil gjør | Ingenting, utover at Macen er våken og har nett (SwiftPM kloner alle avhengigheter i fersk DerivedData, også de som ikke bygges [belagt: Package.swift:26–35]). Etterpå: ja til sletting av `_h1-visionos-probe-<dato>/` (anslag 3–8 GB [vurdering]; 131 GB ledig 16.09). |
| når | Rett etter et rent steg 0. Én kjøring per dag; `--go --again` sletter dagens scratch og kjører på nytt. |
| kommando | samme som steg 0 med `--go` på slutten |
| bevis | `TESTRESULT.md#h1`. **Rød baseline** (HEAD bygger ikke for macOS) er et gyldig utfall: da stopper vi og Kjetil velger ref (§4 rad 4) før noe annet. |

### Steg 1b (valgfritt, null kode) — HAVEN som «Designed for iPad» i visionOS-simulatoren

| | |
|---|---|
| innebærer | iPad-appen kjørt i visionOS-simulatoren i kompatibilitetsmodus. Krever ingen kodeendring: `SUPPORTS_XR_DESIGNED_FOR_IPHONE_IPAD` mangler i prosjektet og standard er YES [belagt: ingen `SUPPORTS_`-nøkler i pbxproj; `OS_KAPABILITETSAUDIT.md` §1]. Det er det raskeste ærlige svaret på «kan det kjøre i simulatoren» — men det er port-vei 0 (`ANALYSE.md` §2), ikke nativ visionOS: flatt iPad-vindu, ingen glass, ingen visionOS-API-er. |
| utfører | Samme vei som steg 1; xcodebuild-syntaksen for varianten (`variant=Designed for iPad`) er ikke verifisert [usikker] — prøves i samme kjøring som steg 2 og rapporteres som virket/virket ikke. |
| bevis | `images/simulator-steg1b-<dato>.png` eller én linje om hvorfor det ikke gikk. |

### Steg 2 — HAVEN starter nativt i visionOS-simulatoren (gren E, F7 steg 1)

| | |
|---|---|
| purposeRef | `purpose://candidate.platform.visionos-native.conditionals-honest`, `.visionos-blockers-isolated` — tester `test.host.no-appkit-in-else` (rød i dag: 3), `test.lint.platform-conditionals`, `test.h1.compile-probe` |
| innebærer | **Kode, første gang.** I egne worktrees (§3), aldri i hovedtrærne. (1) De tre `#else`-grenene med AppKit byttes til `#if canImport(UIKit) Color(uiColor:) #elseif canImport(AppKit) Color(nsColor:) #else Color.clear #endif` — nøytral `#else` som auditens regel og presedensen i samme fil [belagt: ContentView.swift:8475–8481; auditen §4.1]. (2) `impactGenerator` i `ScannerService.swift:288–291` har ingen bruksted utover deklarasjonen (motlesningens grep 16.09) → hele `#if canImport(UIKit)`-blokken fjernes som død kode; finnes et bruksted likevel: API-gate `#if canImport(UIKit) && !os(visionOS)` **og** allowlisten oppdateres i samme endring (ScannerService 9→10), ellers blir linten rød av vår egen rettelse. (3) `project.pbxproj`, HAVEN-målet (to konfigurasjoner, linje 547/553 og 618/624): `SUPPORTED_PLATFORMS` += `xros xrsimulator`, `TARGETED_DEVICE_FAMILY = "1,2,7"`, `XROS_DEPLOYMENT_TARGET = 26.0`; **og** per-SDK-nøklene som ellers faller til macOS-varianten: `CODE_SIGN_ENTITLEMENTS[sdk=xros*]`/`[sdk=xrsimulator*]` → `Binding/Binding-iOS.entitlements` (ellers brukes macOS-filen med app-sandbox) [belagt: pbxproj:493–495], `INFOPLIST_KEY_UIApplicationSceneManifest_Generation[sdk=xros*]`/`[sdk=xrsimulator*] = YES` [belagt: pbxproj:522–523]. (4) `Package.swift` røres **ikke** — `.visionOS` krever tools 5.9, filen står på 5.8 [belagt: Package.swift:1]; ulistet plattform = støttet fra visionOS 1.0. (5) Det H1 fant utover dette — antall ukjent til steg 1 er kjørt. Deretter: simulatorenhet «Apple Vision Pro» bootes, appen bygges (simulator trenger ikke sertifikat; ad hoc/`CODE_SIGNING_ALLOWED=NO` [vurdering]), installeres, startes, og skjermbilde tas med `xcrun simctl io … screenshot` → `images/simulator-steg2-<dato>.png`. |
| utfører | Losen skriver patchene (Python; hvert anker med forventet treffantall — pbxproj-nøklene treffer 2 ganger på HAVEN-målet, det sjekkes eksplisitt — testet i skycontaineren først) og `handoff/KJOR-SELV-steg2-simulator.sh` (tørrkjøring uten `--run`). Bygg + simulator på Macen via valgt vei. |
| Kjetil gjør | Sier ja til `git worktree add` (det lager grener og `.git/worktrees` i hans repoer) og godkjenner mappetilgang til `_worktrees/` når spørsmålet kommer. Ellers ingenting. |
| når | Etter «G2 godkjent» og et ferdig steg 1. |
| bevis | Skjermbildet fra simulatoren + `TESTRESULT.md#steg2` (bygg-exit, `simctl launch` uten krasj). `test.host.no-appkit-in-else` 3→0. Linten: ContentView 22→20, RootView 2→1, ScannerService 9→8 (eller 9→10 med oppdatert allowlist) — tallene føres inn, ikke «uendret». |
| kjent usikkerhet | Førstegangs identitetsflyt i simulator: `targetEnvironment(simulator)` slår av Keychain-`SecAccessControl` — om onboardingen fullfører uten Optic ID er ikke sjekket [usikker]. visionOS faller i dag i iOS-overlays inne i et macOS-lignende skall (auditen §4.3) og 148 rå hex-bakgrunner (H7): skjermbildet vil se «feil» ut utover det steget lover — det er ærlig, og det er gren E `.capability-axis`/`.glass-safe-styles`, ikke dette steget. Lagdelt visionOS-appikon mangler trolig → advarsel, ikke feil [usikker]. `onOpenURL` er `os(iOS)`-gatet [belagt: RootView.swift:73] → ingen URL-åpning i simulatoren i steg 2. |

### Steg 3 — Baksiden av flaten (gren B) — den første skiven av mocken

| | |
|---|---|
| purposeRef | `purpose://candidate.porthole.backside` med bladene `.flip`, `.honest-absence`; `purpose://candidate.cell.interaction-events` **utsettes** (F3) — tester `test.backside.four-zones`, `test.backside.absence-states` |
| innebærer | Først **`bakside-datastrommer-v2.png`** med tomtilstander (lest/uleselig/stille/ikke koblet) — det er bildet G1-GUI gjelder. Så: ny visning `PortholeBacksideView` i CellApple ved siden av Porthole-visningene (`flowElements` er intern i modulen, så visningen må bo der) [belagt: PortholeBindingViewModel.swift:32], vist som flipp (`rotation3DEffect`) fra redigeringsmodus i `PortholeCanvas` [belagt: ContentView.swift ~8457]. Fire soner: **Absorbert** (fra `getCellConfiguration().cellReferences` via `portholeMeddle as? OrchestratorCell`, som view-modellen allerede gjør [belagt: PortholeBindingViewModel.swift:377]), **Abonnert** (`subscribeFeed`/`subscriptions` per referanse), **Puls** (siste FlowElements med ankomsttid — `FlowElement` har ikke tidsstempel [belagt: FlowElement.swift:9–14], så view-modellen lagrer `receivedAt` ved innsetting, og et origin→label-oppslag gir riktig rad), tilstand per rad fra `attachedStatuses`, **Set/get** i ærlig fravær: «ikke koblet — krever strukturert hendelsesstrøm (F3)». Virker på Mac og i simulatoren (H9: plattformnøytral). |
| utfører | Losen (v2-bilde, patch/worktree) + Macen (bygg, skjermbilde på Mac; i simulator når steg 2 er grønt) |
| Kjetil gjør | Sier «G1-GUI godkjent» for v2 **før** koden skrives, eller sier hva som skal tegnes om. |
| når | Etter «G1 godkjent» (gren B) og «G1-GUI godkjent» (v2). **Ikke** gatet på steg 2: grenen rører andre filer enn steg 2 og er uavhengig av SDK-nedlasting og H1-tallet — den bygges og vises på Mac først. |
| bevis | `images/mac-steg3-<dato>.png`, og `images/simulator-steg3-<dato>.png` når steg 2 er grønt, satt ved siden av v2; `TESTRESULT.md#steg3`. |

### Steg 4 — G3 og levering

| | |
|---|---|
| innebærer | Kjetil sammenligner forventning (`FORMAALSSPEC.md` §3 + v2) med faktisk (skjermbildene). Alle avledede tester i §5 for grenene E og B grønne. Deretter PR fra worktree-grenene (Binding og CellProtocol, samme grennavn), CI, merge — samme kjede som alt annet implementert. Worktrees fjernes (`git worktree remove` + `prune`), scratch slettes. |
| Kjetil gjør | Sier «G3 godkjent» eller peker på avviket. |
| når | Etter steg 3 (og steg 2 for simulator-delen). |

**Utenfor denne planen** (egne PDD-er, i denne rekkefølgen [vurdering]): C FlowTap-celle og inspektør
(scene 3), A Porthole-instanser og vinduer (scene 1), D rommet (scene 4). A er den som gir «mange
Portholes» på visionOS og er den største rammeverksendringen; B og C gir nytte på Mac allerede.

## 3. Hvordan bygg og kjøring faktisk skjer

**Tre veier for det som må kjøres på Macen** (steg 0–3). Kjetil velger én:

| Vei | Hva det innebærer | Fordel | Ulempe |
|---|---|---|---|
| 1. Ett dobbeltklikk: `handoff/KJOR-SELV-visionos.command` | **Rettet 16.09 kl. 19:** skjermstyringen gir bare *klikk* i Terminal og Xcode, ikke tasting. Derfor er alle stegene samlet i én `.command`-fil som Kjetil dobbeltklikker i Finder (eller jeg dobbeltklikker den via skjermstyring av Finder). Den gjør steg 0, 1, 2 og 3 i ett løp og skriver alt til `TESTRESULT.md`, `handoff/logs/` og `images/`. | Ingen innliming, ingen tasting; jeg leser resultatet fra oppgavemappen (den er montert). | Ett langt løp (20–60 min første gang); feiler et steg, stopper stegene som avhenger av det, resten skrives. |
| 2. Kjetil kjører skriptet selv | Samme skript, samme kommando, når det passer ham. | Full kontroll. | Kjetil er i løkka for hvert bygg (3–6 bygg totalt). |
| 3. Køen (`_losen-queue`, Codex) | Jobbfilen ligger i `handoff/queue-ready/`. | Ingen menneske i løkka. | **Går ikke:** runneren tillater bare `read-only`/`workspace-write` [belagt: `_losen-queue/runner.sh` linje `case "$sandbox"`], og i `workspace-write` feiler SwiftPM-sandkassen og nettet er av (lokalt-bygg-lærdommen 31.08). Ute av planen. |

**Hvor koden skrives.** HAVEN-mappene er én delt arbeidskopi (flere økter + køen). Derfor egne worktrees:
`_worktrees/visionos-<dato>/Binding` og `_worktrees/visionos-<dato>/CellProtocol` som **søsken** — prosjektet
refererer pakken som `../CellProtocol` [belagt: project.pbxproj:769–770]. Gren `losen/visionos-sim-<dato>` i
begge, laget fra **den ref-en steg 1 målte grønn baseline på** (proben logger branch og SHA), ikke blindt
fra `origin/main` (`lesson.main-does-not-build-without-unlanded-changes`). Hovedtrærne røres ikke; ingen git
fra `device_bash` mot monteringen; `git worktree add` kjøres på Macen med Kjetils ja.

**Disk.** 131 GB ledig på Macen 16.09. Proben (steg 1) 3–8 GB, worktrees med DerivedData (steg 2–3) 7–17 GB
[vurdering]; simulator-kjøretiden (~7–8 GB) kommer i tillegg hvis den må installeres. Alt unntatt kjøretiden
slettes når PDD-en er levert; skriptene skriver ut hvor mye de brukte.

**Gjort herfra 16.09 etter «G2 godkjent»:** `handoff/patches/apply_patches.py` (fase P/A/B, ankere med
treffantall, testet mot dagens kildefiler fra Macen: alle ankere traff, idempotent), `handoff/patches/PortholeBackside.swift`
(baksiden: modell, flipp-beholder, flate) og `handoff/KJOR-SELV-visionos.command` (steg 0–3 i ett løp, `zsh -n` ren).
Ingenting er kompilert ennå — første kompilering skjer i løpet på Macen, og feil der er forventet og blir rettet i worktreet.

## 4. Hva Kjetil selv må gjøre — samlet

| # | Hva | Når | Hvorfor bare du |
|---|---|---|---|
| 1 | Si portordene: «G1 godkjent» (minst grenene E og B), «G2 godkjent» for denne planen — eller si hva som skal endres. «G1-GUI godkjent» kommer når v2 av baksiden er tegnet. | Nå | Bare ditt ord setter en port |
| 2 | Velg vei 1, 2 eller 3 i §3 | Nå | Det er din skjerm og din maskin |
| 3 | Installer visionOS-SDK og/eller simulator-kjøretid i Xcode › Settings › Components hvis steg 0 sier de mangler | Etter steg 0 (kjøretiden kan lastes ned mens steg 1 bygger) | Apple-ID, disk, admin |
| 4 | Avgjør ref hvis steg 0 viser ucommittede filer, eller steg 1 gir rød baseline: committe til gren først, eller måle på det som er | Etter steg 0/1 | Det er dine halvferdige endringer |
| 5 | Si ja til `git worktree add` i Binding og CellProtocol, og godkjenn spørsmålene som dukker opp: skjermstyring (vei 1), mappetilgang til `_worktrees/` (steg 2) | Når de kommer | Grener og tilgang i dine repoer gis bare av deg |
| 6 | La Macen være våken og på nett under steg 1 og hvert bygg i steg 2–3 (15–45 min hver) | Under kjøring | Bygget dør hvis maskinen sover; SwiftPM trenger nett |
| 7 | Si ja til sletting av `_h1-visionos-probe-<dato>/` og worktrees når de er brukt | Etter steg 1 / steg 4 | Sletting på din disk skjer aldri uten ja |
| 8 | Døm G3: forventning mot faktisk | Etter steg 3 | Akseptanse er din |

## 5. Risikoer og det som ikke er sjekket

- **Rød baseline**: eksporten av HEAD bygger kanskje ikke for macOS i det hele tatt (delt, skittent arbeidstre).
  Da finnes ingen H1-måling før Kjetil har valgt ref (§4 rad 4). Proben skriver dette eksplisitt.
- **Antall kompileringsfeil** er ukjent til steg 1 er kjørt; tre er funnet ved lesing, 24 falske negativer
  (`OS_KAPABILITETSAUDIT.md` §4.2) blokkerer ikke bygg men gir feil oppførsel (ingen push-innrullering,
  ingen `onOpenURL`, ingen tale). De rettes ikke i steg 2 — de er egne pakker i gren E.
- **SDK/kjøretid** kan mangle (steg 0). Nedlastingen er Kjetils.
- **Signering**: `CODE_SIGN_IDENTITY = "Apple Development"` og `CODE_SIGN_STYLE = Automatic` gjelder alle SDK-er
  [belagt: pbxproj:496,498]; proben slår signering av, og simulatorkjøring trenger ikke sertifikat [vurdering].
- **Simulator ≠ enhet**: ingen UWB, haptikk, ekte push-token, ekte Optic ID; Keychain-gaten over. Det vi
  beviser i steg 2–3 er «starter og viser», ikke «virker på Vision Pro».
- **Utseende**: iOS-overlays i macOS-skall (auditen §4.3) og 148 rå hex-bakgrunner (H7) gjør at simulatorbildet
  ser feil ut utover glass. Skjermbildene skal vise det som det er.
- **Delt arbeidskopi**: HEAD i Binding/CellProtocol kan stå på en annen økts gren når proben eksporterer;
  proben logger branch/HEAD, og worktrees lages fra den målte ref-en.
- **Ikke etterprøvd** (fra motlesningen): om `Binding.xcworkspace` er sporet i git (proben bruker nå `-project`
  og er uavhengig av det); `variant=Designed for iPad`-syntaksen; at `UIImpactFeedbackGenerator` er
  `API_UNAVAILABLE(visionos)` i SDK-headeren (fra dokumentasjon); `ENABLE_APP_SANDBOX` på xros; Assets for visionOS.

## 6. Planbytte mot FORMAALSSPEC §6

Spesifikasjonen foreslo rekkefølgen B → C → E → A → D. Denne planen kjører **E og B parallelt**: E først i
tid (steg 0–2) fordi spørsmålet 16.09 er «kjør det i simulatoren», og uten E starter ingenting der; B (steg 3)
er ikke gatet på E og vises på Mac først. Byttet føres i `STATUS.md` under Planbytter når G2 er godkjent.

## 7. Uavhengig validering («Fabel», 2026-09-16)

Egen Claude-tråd leste utkastet mot koden og spesifikasjonen med oppdrag om å motsi. Dom: «i hovedsak ærlig og
godt merket, men tre ting framstilles som sikrere enn de er». Det som endret planen:

1. **Steg 2-beviset var selvmotsigende** — «linten uendret» mens rettelsen i ScannerService la til et `os(`-direktiv.
   Nå: død kode fjernes, eller allowlisten oppdateres i samme endring; tallene føres inn.
2. **Steg 0 lovet mer enn skriptet gjorde** (kjøretid og disk ble ikke sjekket; «nekter ny kjøring» var feil —
   skriptet slettet stille). Skriptet er rettet: kjøretid, disk, `--again`-vakt, `-project`, `CODE_SIGNING_ALLOWED=NO`.
3. **Rød baseline hadde ingen gren** — lagt til i steg 1, §4 rad 4 og §5.
4. **«Tre av fire soner: ja» overdrev** — dataene må hentes fra cellen (`getCellConfiguration()`, `attachedStatuses`),
   puls trenger origin→label-oppslag; størrelse liten → middels.
5. **pbxproj trengte mer** — entitlements og scene-manifest per SDK, signering; sed-ankere som treffer to ganger.
6. **Rekkefølge** — steg 1b «Designed for iPad» lagt til som null-kode-svar; steg 3 ikke lenger gatet på steg 2.
7. **G1-GUI på feil bilde** — v2 med tomtilstander tegnes før spørsmålet stilles.
8. **Manglende Kjetil-rader** — `git worktree add`, nett, signering, ref-valg.
9. Anslag: 10–30 min → 15–45 min; kjøretiden utenfor disk-totalen.

Bekreftet uten endring: canImport-formen (med nøytral `#else`), `Package.swift` urørt (tools 5.8), søsken-worktrees,
set/get-fravær, at `FlowElement` mangler tidsstempel, at det er nøyaktig tre AppKit-i-`#else`.
