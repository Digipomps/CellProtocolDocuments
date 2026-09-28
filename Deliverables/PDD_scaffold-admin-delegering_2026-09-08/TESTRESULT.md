# TESTRESULT — scaffold-administrator og delegering

Utdata fra hver rad i FORMAALSSPEC §5. Alt lim er fra faktisk kjøring.
Tester som ikke kunne kjøres står som `blocked` med årsak.

## Baseline <a id="baseline"></a>

WP0 er en måling før kildeendring. G2 er godkjent 2026-09-09. Målingen gjelder det eksisterende, skitne arbeidstreet; SHA alene identifiserer ikke hele det målte innholdet.

- Forhåndssjekk: 2026-09-09 ca. 04:52:47 CEST (Europe/Oslo; 02:52:47 UTC registrert rett etter sjekken).
- Repo: `CellScaffold`.
- Branch: `pdd/tillitspakke-agentflaate`.
- Kort SHA: `1dbdee23`.
- Antall skitne statusoppføringer: **181**, fra faktisk `git status --porcelain | wc -l`.
- Arbeidstreet er skittent fra før WP0. Etter eksplisitt WP0-instruks fortsetter målingen selv om handoff-regel 7 ellers sier stopp ved avvik.

Faktisk utdata fra forhåndssjekken:

```text
pdd/tillitspakke-agentflaate
1dbdee23
     181
```

Faktisk `git status --porcelain | head -30` nedenfor. Dette er de første 30 av 181 oppføringer, ikke en fullstendig liste; øvrige 151 oppføringer er ikke navngitt av den foreskrevne kommandoen.

```text
 M .claude/skills/codex-collaboration/SKILL.md
 M .gitignore
 M .mcp.json
 M Documentation/AdminScaffold_Secret_Provisioning.md
 M Documentation/ClaudeSkills/README.md
 M Documentation/ClaudeSkills/desktop-src/cellconfiguration-skeleton-authoring/references/runtime-publishing.md
 M Documentation/ClaudeSkills/desktop-src/codex-collaboration/Skill.md
 M Documentation/ClaudeSkills/desktop-src/haven-functional-service-verification/references/sandbox-capability-matrix.md
 M Documentation/ClaudeSkills/desktop-src/haven-prompt-purpose-testing/Skill.md
 M Documentation/ClaudeSkills/desktop-zips/binding-skeleton-parity-testing.zip
 M Documentation/ClaudeSkills/desktop-zips/cellconfiguration-skeleton-authoring.zip
 M Documentation/ClaudeSkills/desktop-zips/cellprotocol-distributed-entity-data.zip
 M Documentation/ClaudeSkills/desktop-zips/cellprotocol-docs-and-rag-maintenance.zip
 M Documentation/ClaudeSkills/desktop-zips/codex-collaboration.zip
 M Documentation/ClaudeSkills/desktop-zips/dimy-payment-regulatory-guardrails.zip
 M Documentation/ClaudeSkills/desktop-zips/dimy-value-redistribution.zip
 M Documentation/ClaudeSkills/desktop-zips/haven-claim-review.zip
 M Documentation/ClaudeSkills/desktop-zips/haven-functional-service-verification.zip
 M Documentation/ClaudeSkills/desktop-zips/haven-gui-testing.zip
 M Documentation/ClaudeSkills/desktop-zips/haven-prompt-purpose-testing.zip
 M Documentation/ClaudeSkills/desktop-zips/haven-xcode-workspace-recovery.zip
 M Documentation/ClaudeSkills/desktop-zips/omnigraffle-illustrations.zip
 M Documentation/ClaudeSkills/desktop-zips/personal-data-trust-package.zip
 M Documentation/ClaudeSkills/desktop-zips/public-presence-cell-authoring.zip
 M Documentation/Claude_Skills_and_Codex_Collaboration.md
 M Documentation/Operations/music-free-price-and-resolution-20260828/README.md
 M Documentation/Operations/purpose-cell-fase1-20260828/README.md
 M Documentation/ProjectControl/SISTE_OPPDATERING.md
 M Documentation/Skeleton_Runtime_Iteration_Workflow.md
 M Package.resolved
```

WP4-målingen ble kjørt fra HAVEN-roten etter bygg- og testkommandoen, 2026-09-09 ca. 04:55:20 CEST (02:55:20 UTC registrert rett etter målingen):

| Faktisk kommando | Antall matchende linjer |
|---|---:|
| `grep -rn "requireAdminUser" --include="*.swift" CellScaffold/Sources \| wc -l` | 48 |
| `grep -rn "AdminRoleProfile" --include="*.swift" CellScaffold/Sources \| wc -l` | 33 |

Rå utdata, i samme rekkefølge:

```text
      48
      33
```

Begge pipeline-kommandoene fullførte; kommandokallet hadde exit 0. Tallene teller matchende kildelinjer, ikke unike filer eller verifiserte myndighetsstier. Ingen kodeendring inngår i målingen.

## Bygg <a id="build"></a>

Kommando: `swift build`, cwd `CellScaffold`. Ingen ekstra flagg eller miljøoverstyringer.

- Start: 2026-09-09T04:54:26.077031+02:00.
- Slutt: 2026-09-09T04:54:28.558564+02:00.
- Varighet: 2.481 sekunder (veggklokke, monotonic).
- Exit-kode: `1`.
- Resultat: **RØD — `test.build` er blocked av kjøremiljøet** (ikke grønn).

Siste 11 linjer fra faktisk byggkjøring:

```text
warning: /Users/kjetil/Library/org.swift.swiftpm/configuration is not accessible or not writable, disabling user-level cache features.
warning: /Users/kjetil/Library/org.swift.swiftpm/security is not accessible or not writable, disabling user-level cache features.
warning: /Users/kjetil/Library/Caches/org.swift.swiftpm is not accessible or not writable, disabling user-level cache features.
error: 'cellscaffold': Invalid manifest (compiled with: ["/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc", "-vfsoverlay", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.pu5lVU/vfs.yaml", "-L", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-target", "arm64-apple-macosx14.0", "-plugin-path", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/host/plugins/testing", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/PrivateFrameworks", "-I", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-L", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-swift-version", "5", "-I", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-package-description-version", "5.9.0", "/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Package.swift", "-o", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.CsmaTJ/cellscaffold-manifest"])
sandbox-exec: sandbox_apply: Operation not permitted
error: 'cellscaffold': Invalid manifest (compiled with: ["/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc", "-vfsoverlay", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.xc53GA/vfs.yaml", "-L", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-target", "arm64-apple-macosx14.0", "-plugin-path", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/host/plugins/testing", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/PrivateFrameworks", "-I", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-L", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-swift-version", "5", "-I", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-package-description-version", "5.9.0", "/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Package.swift", "-o", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.qPaudO/cellscaffold-manifest"])
sandbox-exec: sandbox_apply: Operation not permitted
error: ExitCode(rawValue: 1)
[0/1] Planning build
error: 'cellscaffold': Invalid manifest (compiled with: ["/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc", "-vfsoverlay", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.sg2qlG/vfs.yaml", "-L", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-target", "arm64-apple-macosx14.0", "-plugin-path", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/host/plugins/testing", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/PrivateFrameworks", "-I", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-L", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-swift-version", "5", "-I", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-package-description-version", "5.9.0", "/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Package.swift", "-o", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.puyS90/cellscaffold-manifest"])
sandbox-exec: sandbox_apply: Operation not permitted
```

Avvik: `test.build` er **blocked** fordi SwiftPM ikke fikk opprette manifest-sandboxen (`sandbox-exec: sandbox_apply: Operation not permitted`). Dette dokumenterer en miljøhindring, ikke en påvist feil i applikasjonens kilder. Hele byggutdataen er de 11 linjene over. Advarslene gjelder tilgang til SwiftPM-konfigurasjon og cache, inkludert `security`-katalogen. Om noen advarsler er nye er ikke fastslått; kompilering av autorisasjonskoden kunne ikke vurderes.


### Forsøk 2 — detached, danger-full-access: GRØNT

Forsøk 1 over ble blocked av sandkassen. Andre forsøk kjørte som detached skript med
`danger-full-access`, på en **ren eksport** av CellScaffold `main`
`e1f3e22f02239e44eacaf12a741d78b4066d0c35` — ikke det delte arbeidstreet, som sto på
`pdd/tillitspakke-agentflaate` med 181 skitne oppføringer.

```text
=== BUILD START 2026-09-09T03:24:57Z
=== BUILD_RC=0 2026-09-09T03:28:11Z
```

- Varighet: 3 min 14 s. Toolchain: Apple Swift 6.2.4, target arm64-apple-macosx26.0.
- Logg: `CellScaffold/.build/sad-baseline/baseline.log`.
- Lærdom registrert: `lesson.codex-workspace-write-cannot-build-cellscaffold`, `lesson.baseline-measured-another-pdds-branch`.

## Regresjon <a id="regression"></a>

### Regresjon etter WP1 + WP2 + to feilrettinger — NULL nye feil

```text
	 Executed 2145 tests, with 11 tests skipped and 90 failures (6 unexpected) in 349.502 seconds
	 unike feilende testnavn: 29
	 NYE feil mot baseline: 0
```

Kjørt 2026-09-09 13:02–13:08 UTC i worktreet. De tre nye feilene fra forrige runde er
borte. 30 tidligere røde er grønne, men det tilskrives fortsatt miljøforskjellen mellom
ren eksport og worktre, ikke vårt arbeid.

De to feilrettingene som skulle til:

1. **Require-existing.** Registreringene flyttet til `reconcileScaffoldAdministratorCellResolves(owner:)`, gated på `eagerBootstrapPolicy == .provisionIfMissing` eller en eksisterende mapping. Kjøres etter at eier-orkestratoren har gjenopprettet NamedEmitters, slik at et senere endepunktoppslag ikke stille provisjonerer en celle.
2. **Provision-only.** Samme funksjon returnerer nå tidlig når `eagerBootstrapProvisionOnly` er satt. `TopUpCheckoutTests` teller cellene provision-only skal lage — de tre kanoniske eager-bootstrap-cellene pluss LiveInteraction — og våre to hører ikke til det settet. Jeg endret **ikke** testens forventning fra 4 til 5; den er en bevisst garanti skrevet av noen andre, og vår celle er scaffold-intern tilstand, ikke en kanonisk bootstrap-celle.

Lærdom: `lesson.new-cell-must-declare-its-provisioning-mode`. Enhver ny persistert celle i
CellScaffold må svare på tre spørsmål før den registreres — require-existing, provision-only,
og om den er en Porthole-publisert flate — ellers havner den i alle tre.


Kommando: `swift test`, cwd `CellScaffold`. Hele testmengden forespurt, ingen filter, ekstra flagg eller miljøoverstyringer.

- Start: 2026-09-09T04:55:09.170127+02:00.
- Slutt: 2026-09-09T04:55:10.774221+02:00.
- Varighet for testkommandoen: 1.604 sekunder (veggklokke, monotonic).
- Exit-kode: `1`.
- Resultat: **blocked — manifestbehandling stoppet før testene startet**.

### Faktiske `Executed`-linjer

Ingen `Executed`-linjer ble produsert. Testantall kan ikke oppgis fra denne kjøringen.

### Hver `error:`-/`failed`-linje fra kjøringen

Full utdata nedenfor, inkludert samtlige `error:`-linjer og sandbox-årsaken. Ingen `failed`-linjer ble produsert.

```text
warning: /Users/kjetil/Library/org.swift.swiftpm/configuration is not accessible or not writable, disabling user-level cache features.
warning: /Users/kjetil/Library/org.swift.swiftpm/security is not accessible or not writable, disabling user-level cache features.
warning: /Users/kjetil/Library/Caches/org.swift.swiftpm is not accessible or not writable, disabling user-level cache features.
error: 'cellscaffold': Invalid manifest (compiled with: ["/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc", "-vfsoverlay", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.B99R79/vfs.yaml", "-L", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-target", "arm64-apple-macosx14.0", "-plugin-path", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/host/plugins/testing", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/PrivateFrameworks", "-I", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-L", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-swift-version", "5", "-I", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-package-description-version", "5.9.0", "/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Package.swift", "-o", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.ws6bI3/cellscaffold-manifest"])
sandbox-exec: sandbox_apply: Operation not permitted
error: 'cellscaffold': Invalid manifest (compiled with: ["/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc", "-vfsoverlay", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.vIX5Kb/vfs.yaml", "-L", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-target", "arm64-apple-macosx14.0", "-plugin-path", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/host/plugins/testing", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/PrivateFrameworks", "-I", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-L", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-swift-version", "5", "-I", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-package-description-version", "5.9.0", "/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Package.swift", "-o", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.3yovxN/cellscaffold-manifest"])
sandbox-exec: sandbox_apply: Operation not permitted
error: ExitCode(rawValue: 1)
[0/1] Planning build
error: 'cellscaffold': Invalid manifest (compiled with: ["/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc", "-vfsoverlay", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.m3TTOq/vfs.yaml", "-L", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-target", "arm64-apple-macosx14.0", "-plugin-path", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/host/plugins/testing", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks", "-F", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/PrivateFrameworks", "-I", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-L", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib", "-swift-version", "5", "-I", "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/pm/ManifestAPI", "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.2.sdk", "-package-description-version", "5.9.0", "/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Package.swift", "-o", "/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/TemporaryDirectory.Sw9Wqn/cellscaffold-manifest"])
sandbox-exec: sandbox_apply: Operation not permitted
```

### Navngitte røde tester og avvik

Ingen tester startet; ingen navngitte røde tester kunne måles. Dette betyr ikke at testmengden er grønn.

- `test.regression`: **blocked** — `sandbox-exec: sandbox_apply: Operation not permitted` under SwiftPM-manifestbehandling; `swift test` avsluttet med exit 1 før teststart. `lesson.baseline-count-from-report-not-run`: ingen tall eller røde tester er hentet fra tidligere rapporter.



### Forsøk 2 — detached, ren eksport av main: EKTE TALL, RØDT FRA FØR

```text
Test Suite 'CellsContainerPackageTests.xctest' failed
	 Executed 2129 tests, with 11 tests skipped and 347 failures (6 unexpected) in 288.087 seconds
Test Suite 'All tests' failed
	 Executed 2129 tests, with 11 tests skipped and 347 failures (6 unexpected) in 288.087 seconds
```

- To kjøringer på samme eksport ga **346** og **347** feil. Baselinen er ikke helt
  deterministisk — ±1 mellom kjøringer. Det tallet hører i akseptansen, ellers blir
  tilfeldig flakiness lest som en regresjon.
- **59 unike testnavn** feiler, fordelt på ~25 suiter. Full liste:
  `handoff/baseline-failing-tests-main-e1f3e22f.txt`. Rå logg (2,4 MB):
  `CellScaffold/.build/sad-baseline/retest.full.log`.
- 11 tester hoppes over. swift-testing-løperen rapporterer «0 tests in 0 suites» —
  ingen swift-testing-suiter i dette målet, alt er XCTest.

Dette er tilstanden **før** vårt arbeid; ingen kildefil er endret. Et rødt baseline
stopper ikke arbeidet, men registreres som eget avvik
(`lesson.baseline-count-from-report-not-run`).

**Konsekvens for P5:** akseptansen kan ikke bruke «alle tester grønne» som mål. Den må
sammenligne mot 2 129 utført / 346–347 feil / 6 uventede og påvise at ingen ny feil er
kommet til.

#### To av de røde ligger i vårt eget område

- `AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter`
- `AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof`

Begge handler om admin-delegering av identitetsbundne credentials — akkurat der WP1 og
WP4 skal jobbe. WP4 må derfor måle «uendret mot denne listen», ikke «grønn».

**Undersøkt, og de er ikke det jeg først antok.** Jeg skrev over at de var «påfallende
nær knappen som feilet 8. september». Det stemmer ikke, og loggen viser hvorfor.
Autorisasjonen lykkes i begge testene:

```text
[App] Arendalsuka import access issue authorized by admin for subject identity
      B5113977-E6E1-43D6-812C-4A4DCF80B27E with 1 action(s).
[App] Arendalsuka import action atlas.ingestOSMPOIs authorized for authenticated user
      3A843172-A537-4090-8389-63219EA56C6A via accepted_vc.
[App] Abort.500: Published Arendalsuka atlas is unavailable through the resolver.
```

Admin utstedte altså det identitetsbundne beviset til en ikke-admin, mottakeren fikk
handlingen godkjent `via accepted_vc`, og **så** feilet det ett lag lenger ned: det
publiserte Arendalsuka-atlaset er ikke tilgjengelig gjennom resolveren i testkjøringen.
Det er en data-/fixturemangel, ikke en autorisasjonsfeil.

Knappen 8. september feilet et helt annet sted: i preflight, med
`agreement_or_proof_required`, **før** noen utstedelse. Ulik feil, ulikt lag.

To konsekvenser:

1. De to røde er ikke et tegn på at delegeringsmodellen er ødelagt. De sier ingenting
   om WP1s hypotese, verken for eller mot.
2. Viktigere: **delegeringen finnes allerede og virker** i denne kodestien — en admin
   utsteder et identitetsbundet, handlingsbegrenset bevis til en ikke-admin, og
   mottakeren bruker det. WP1 og WP2 bør lese
   `ArendalsukaImportAccessCredentialSupport` og disse to testene før de designer noe
   nytt; mønsteret er der, det er organisasjonsleddet og tilbakekallet som mangler.
   Det er billigere å generalisere noe som virker enn å finne opp noe ved siden av.

#### Alle 59 navn

```text
AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns
AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys
AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend
AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials
AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter
AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage
AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument
AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace
AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline
AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline
AppTests.BookReferenceRoutesTests testRenderedEndpointSupportsSwiftBackend
AppTests.ButterpopStudioProductTests testButterpopPageAndCatalogArePublicButWorkspaceSessionRequiresLogin
AppTests.ButterpopStudioProductTests testButterpopSurfaceRateLimitsScrapingBursts
AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview
AppTests.CellScaffoldRuntimeIdentityProvisionerTests testWriterRejectsExtendedAttributesOnExistingManifest
AppTests.CellScaffoldRuntimeIdentityProvisionerTests testWriterRejectsOverwriteWithoutExactOldDigestAndUses0600
AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback
AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp
AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable
AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned
AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell
AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead
AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC
AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof
AppTests.ConferenceSurfaceRoutesTests testArendalsukaLandingPageDeepLinkLoadsParticipantProgram
AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication
AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess
AppTests.ConferenceSurfaceRoutesTests testAuthenticatedPortholeConferenceControlTowerCanCreateAccessRequestFromOwnershipAndAccess
AppTests.ConferenceSurfaceRoutesTests testAuthenticatedPortholeConferenceDemoFlowSupportsCanonicalPersonaLockedSequence
AppTests.ConferenceSurfaceRoutesTests testAuthenticatedPortholeDeepLinkLoadsConferenceSkeletonComponentLibrary
AppTests.ConferenceSurfaceRoutesTests testAuthenticatedPortholeFallsBackToLiveRequesterWhenConferencePersonaIsUnknown
AppTests.ConferenceSurfaceRoutesTests testAuthenticatedPortholeResolvesOwnerPublishedRuntimeSurfaceIDThroughAgreement
AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies
AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator
AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay
AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction
AppTests.DocumentationWorkbenchRoutesTests testDocsRouteRendersBookContextSurface
AppTests.EventPlatformRoutesTests testPublicEventPlatformRoutesAreAvailableWithoutAuthentication
AppTests.LeadVaultRoutesTests testLeadVaultHarnessRouteRenders
AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent
AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState
AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata
AppTests.MarkdownRendererCellTests testRenderRawSourceResolvesRelativeMarkdownLinkAgainstBookCatalog
AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay
AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty
AppTests.MusicPublishingMVPRoutesTests testLegacyMusicPublishingRoutesRemainDisabled
AppTests.PalazzoCommunaleRoutesTests testPublicSurfaceConfigurationAndAllowlistedAPIAreProductionHardened
AppTests.PortholeIdentityContinuityRoutesTests testAmbiguousPersistedIdentityRendersSafeLocalizedServiceUnavailablePage
AppTests.PortholeIdentityContinuityRoutesTests testEstablishedRequesterWithPersonalChatHubLoadsCoPilotChat
AppTests.PortholeIdentityContinuityRoutesTests testFirstCoPilotChatEntryProvisionsRequesterOwnedPersonalChatHubAndLoads
AppTests.PortholeIdentityContinuityRoutesTests testLegacyPortholeAndChatRecoverToV2AcrossRestartAndStaleCookieWithinBudget
AppTests.PortholeMenuFallbackTests testOrchestratorLocalFallbackMenusExposeCatalogWithoutResolver
AppTests.PortholeMenuFallbackTests testPortholePublishedConfigurationsCoverMostRenderableCatalogEntries
AppTests.PortholeWebEditorSupportTests testDefaultComponentPaletteIncludesAdminCopilot
AppTests.RAGMVPRoutesTests testRAGPageAllowsRememberCookieAuthentication
AppTests.RestaurantSurfaceRoutesTests testPalazzoPageAccessPolicies
AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips
AppTests.SkeletonParityRoutesTests testSkeletonParitySuiteCatalogAndPagesArePublic
AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning
```

## Kontrakt <a id="contract"></a>

### WP2 — skrevet, ikke verifisert (2026-09-09)

Formål: `purpose://candidate.scaffold-admin.mandate-is-explicit-bounded-revocable`.
Arbeidstre: `CellScaffold::_wt-sad-20260909`, branch `pdd/scaffold-admin-delegering`.
Bare WP2-kode og tilhørende tester er skrevet. WP3–WP10 er ikke erklært utført.

Faktisk forhåndssjekk (oppdragets to tillatte git-lesekommandoer):

```text
pdd/scaffold-admin-delegering
       5
```

Kode i worktreet, med stier relative til arbeidstreets rot:

- `Sources/App/Cells/Admin/ScaffoldMandate.swift`: alle feltene i `mandateShape`, streng dekoding, eksplisitt `orgLinkRef: null`, avvisning av manglende/ tomt omfang, ukjent formål, utløpt/for langt mandat og utstederrett i `kind=use`. Bare `mandateID` kan utelates ved utstedelse; da brukes UUID-en som allerede står i den obligatoriske `revocationRef`. Ingen manglende omfangs-/tidsfelt fylles ut.
- `Sources/App/Cells/Admin/ScaffoldMandateCell.swift`: persistert mandat og rolleavtale, `mandate.issue/revoke/list/read`, `orgLink.issue/revoke/list`, beholdte tilbakekallsoppføringer og privat revisjonsspor. Registrert i `Sources/App/configure.swift` med samme scaffold-scope og eierdomene som WP1-registeret.
- `Sources/App/Cells/Admin/ScaffoldMandateProofSupport.swift`: faktisk signering/verifikasjon med eksisterende `Contract`/`Agreement` og `IdentityPublicKeySignatureVerifier`. Hver signatur binder mandat, signatar, signeringstid og begrunnelse. Wire-fingeravtrykket er `sha256:` + hex av SHA-256 over den komprimerte offentlige signaturnøkkelen; CellBase sitt interne `signingPublicKeyFingerprint` har et annet format.
- `Sources/App/Support/EntityAnchorProofSupport.swift`: lagrings-/indeksmønsteret er trukket ut fra `ArendalsukaImportAccessCredentialSupport.swift`, som nå bruker denne felles kodeveien. Både importbeviset og mandatet bruker mottakerens egne `proofs` og `proofs.index.byKeypath.<escaped-keypath>`. Den eksisterende indekskodingen er escaping, ikke en kryptografisk hash. Indeksen er bare oppslag; signatur, identitet, omfang og tilbakekall avgjør myndighet.

Utstedelsesforespørselen har en signeringskonvolutt: `{ mandate, subject, signerAuthorities, reason }`. `mandate` er kontraktens form med faktiske signaturer; `subject` er offentlig Identity-deskriptor; `signerAuthorities` er eier-signerte representant-Contracts. `reason` er 8–512 tegn og inngår i signaturene. Kontraktdokumentet definerer ikke denne transporten av signaturbevis eller nøkkeldeskriptorer; dette er WP2s konkrete kobling til eksisterende Contract-kode, dokumentert for integratoren. `orgLink.issue` bruker kontraktens felter samt `subject` og `reason` for å binde rolleavtalen og revisjonssporet til riktig identitet.

Lesevalg uttrykkes som `mandate.read.<UUID>` og eventuelt `mandate.list.<base64url(resourceRef)>`; `mandate.list` uten suffiks filtrerer til cellene requesteren eier, eller til scaffoldet for en verifisert administratormandatinnehaver. Suffikset er et oppslagsvalg under den dokumenterte leseoperasjonen. Det kontrolleres med cellens ordinære `authorizationDecision` og ressurskontroll; private mandat-ID-er registreres ikke som offentlige Explore-nøkler. Den kanoniske `revocationRef` binder UUID-en til `cell:///ScaffoldMandate/mandates/`; mandatkontrollen slår opp den tilsvarende beholdte posten i ScaffoldMandate ved hvert bruk.

`Tests/AppTests/ScaffoldMandateTests.swift` har **9 skrevne testmetoder**, med **22 fixture-caser** og tilleggsasserts for alle påkrevde felt, tomt omfang, faktisk målcellehandling, tilbakekall/idempotens, eierlesing, falsk representant, endret signaturinnhold, feil ressurs/celleinstans/formål, administratorskifte, private Explore-nøkler og lagringsinnlasting. Dette er opptelling i kildefilene, **ikke et kjøreresultat**. Testene bruker `configure(app)`, produksjonsresolveren, reelle vault-nøkler og produksjonscellens `set/get`/autorisasjonsfunksjon; ingen erstatningscelle eller stubbet autorisasjonsbeslutning. Sammensatte `ValueType` sammenlignes på kanonisk JSON.

Fixture-kopiene i `Tests/AppTests/Fixtures/ScaffoldMandate/` er byte-identiske med dokumentrepoet. Faktisk filkontroll:

```text
mandate-negative.json cases=14 same_as_contract=True sha256=ddddaf4e59f54bd5eaa03c8304c80cd354fb17a920c813e887c4419c5835c700
mandate-positive.json cases=2 same_as_contract=True sha256=15f9fb8c2a074974b4f69c892a4e3aecf654cbda35288f87254fdab2622d1b3c
threshold-policy.json cases=6 same_as_contract=True sha256=b98270d38cb65496f4e44205c9b19457c41e68a7734f8cf8e664a65248720a8c
```

Plassholdernøkler/-signaturer i fixtures erstattes av reelle bevis; datoene forskyves med samme relative varighet. Terskel-negative mandatrader materialiseres som `kind=administrate`. Dette endrer testinndata, ikke produksjonens beslutning. Fixture-navnene `role_label_is_not_authority` og `threshold_policy_invalid` krever to presiseringer: faktisk rolleavslag forblir `agreement_or_proof_required` etter FORMAALSSPEC/WP4; ugyldig policy testes mot WP1s eksisterende `RegistryError.invalidThreshold`/`invalidReason`. WP1s enum-navn er ikke endret til fixture-etiketten.

**Bygg, typekontroll, Swift-tester og funksjonell verifikasjon: blocked/ukjørt.** Oppdraget forbød bygg/test i denne køjobben på grunn av `lesson.codex-workspace-write-cannot-build-cellscaffold`. Det er ikke gjort et nytt byggforsøk og ingen gamle testtall brukes som WP2-bevis. `xcrun swiftc -frontend -parse` på de åtte berørte Swift-filene ga exit 0 uten utdata; dette er bare syntaks, ikke bygg/typekontroll.

Den statiske Explore-auditen over `Sources/App/Cells/Admin` ga 12 feil i de urørte `AdminFundingQueueCell.swift`/`ScaffoldSetupCell.swift` og to dynamiske advarsler. For den nye `ScaffoldMandateCell` var det **0 error-funn og 1 advarsel**: verktøyet følger ikke den beregnede skrive-nøkkellisten. Listen er manuelt lest: de fire skrivehandlingene registrerer `-w-s`, inn-/utskjema og flow-effekt før handleren. Dette er kildeinspeksjon, ikke et grønt runtime-resultat.

## Autorisasjon <a id="auth"></a>

### WP4 verifisert 2026-09-09 13:53 UTC — GRØNT, og egenskapen holder

```text
=== BUILD_RC=0 2026-09-09T13:52:39Z
=== TEST_RC=0 2026-09-09T13:53:10Z
	 Executed 48 tests, with 0 failures (0 unexpected) in 16.935 seconds
```

Full regresjon etterpå: **2150 tester, 90 feil, 29 unike, NULL nye mot baselinen.**

`ScaffoldRoleIsNotAuthorityTests` er nå regresjonsvernet for
`role-label-grants-nothing`. Fire tester, én per rolle
(`admin.observer`, `admin.operator`, `admin.nodeAgent`, `admin.security`): en identitet
med rollen — og uten mandat og uten owner-proof — avvises på `mandate.issue`,
`administrator.register`, `administrator.transfer` og `administrator.thresholdPolicy.set`,
med **samme avslag som en helt fremmed identitet**. Ingen mildere behandling, ingen egen
kodesti. I tillegg en tellertest som låser baselinen `requireAdminUser` = 48 og
`AdminRoleProfile` = 33, med en melding som ber om at et nytt bruksted vurderes mot
formålet og tallet oppdateres bevisst.

**Testene passerte uten at produksjonskoden måtte endres.** Egenskapen holdt allerede;
det som manglet var beviset. Det er nå låst.

#### Feilen i testoppsettet, og hvorfor den var lærerik

Alle fire feilet først i oppsettet, ikke i det de skulle måle: `deniedNoGrant` på
`requestEntry` mot `cell:///AdminEntry`. Testen forsøkte å gi identiteten rollen gjennom
**menneskets vei til å få en rolle** — `AdminEntry.requestEntry` og
`AdminRoleEnrollment.requestRole` — som krever kontrollplan-kontekst en celletest ikke har.

Huset har allerede `AdminRoleCredentialTestSupport.install(...)`, som legger et
eier-signert `AdminRoleCredential` på `role.proofKeypath`. Det er representasjonen
`AdminMetricsSupport.hasRoleProof` faktisk leser, og den alle andre admin-tester bruker.
To spørsmål ble blandet: «hvordan får noen rollen» og «hva gir rollen».
`lesson.test-the-representation-not-the-issuance-flow`.

To mindre kompileringsfeil på veien: `CellBase.defaultCellResolver` er
`any CellResolverProtocol`, ikke den konkrete `CellResolver`, og `Identity` har ingen
`identityDomain`-egenskap — hjelperen tar eierdomenet som streng, slik de andre testene
gir den.


### WP4 — skrevet, ikke verifisert (2026-09-09)

Formål: `purpose://candidate.scaffold-admin.role-label-grants-nothing`.
Forhåndssjekken i `CellScaffold/_wt-sad-20260909` ga faktisk
`pdd/scaffold-admin-delegering`. Handoff-regel 1–12, særlig regel 10, WP4 i
`PLAN.md` og bladformålet i `FORMAALSSPEC.md` §1 er lagt til grunn.

Ny fil: `CellScaffold/_wt-sad-20260909/Tests/AppTests/ScaffoldRoleIsNotAuthorityTests.swift`.
Den inneholder **5 skrevne XCTest-metoder**, ikke et antall utførte tester:
én negativ autorisasjonstest for hver av `admin.observer`, `admin.operator`,
`admin.nodeAgent` og `admin.security`, samt én tellertest.

Hver rolletest er skrevet for følgende matrise:

| Produksjonsendepunkt | Handling | Forventet feilkode for rolleholder og fremmed |
|---|---|---|
| `cell:///ScaffoldMandate` | `mandate.issue` | `agreement_or_proof_required` |
| `cell:///ScaffoldAdministratorRegistry` | `administrator.register` | `agreement_or_proof_required` |
| `cell:///ScaffoldAdministratorRegistry` | `administrator.transfer` | `agreement_or_proof_required` |
| `cell:///ScaffoldAdministratorRegistry` | `administrator.thresholdPolicy.set` | `agreement_or_proof_required` |

Testene starter `configure(app)` med isolert testlagring og løser de eksisterende
produksjonsendepunktene. Rollen gis av produksjonens `AdminRoleEnrollmentCell.requestRole`
med en ekte, eier-signert `AdminRoleCredential`, etter `AdminEntry.requestEntry`.
`storedAt` og gjenlest kredential kontrolleres mot `AdminRoleProfile.proofKeypath`;
`AdminMetricsSupport.hasRoleProof` skal bekrefte akkurat den aktuelle rollen og
ingen rolle for den fremmede. Ingen testhjelper erstatter rolleinnmelding,
autorisasjon eller resolver-factory.

For observer/operator/security kalles også
`AdminEntityProofPersistenceSupport.persistAcceptedCredential` og
`credentialForRestore`, med kanonisk sammenligning av gjenlest kredential.
`nodeAgent` er uttrykkelig utelatt fra produksjonens `humanProofKeypaths`; den
bruker derfor `requestRole` og sin ordinære proof-keypath uten å utvide
menneskekredentialenes lagringsmekanisme. Entry-beviset er kun kontrollplanets
forutsetning; rolleholderen får verken målcellens owner-proof, mandat eller
representant-Agreement.

Testene krever avslag både i `authorizationDecision` og ved faktisk `set`.
Feilkoden fra rolleholderens handling sammenlignes direkte med den fremmedes;
uventede feil eller normale returverdier feiler testen. Gyldige payloads brukes,
med positive kontroller gjennom samme handlinger: eieren for registerskrivingene,
og en separat identitet med eksplisitt representant-Agreement for `mandate.issue`.
Utstedt mandat går til en separat mottaker. Uendret register-/mandattilstand
kontrolleres etter avslag med `assertSameValue`-mønsteret fra
`ScaffoldAdministratorRegistryTests`, aldri sammensatt `ValueType.==`.

Tellertesten finner dette arbeidstreets `Sources` fra `#filePath` og teller
**matchende linjer i `*.swift`**, samme måleenhet som WP0. Grensene er 48 for
`requireAdminUser` og 33 for `AdminRoleProfile`; reduksjon tillates, økning feiler
med brukstedene og beskjed om å vurdere nye bruksteder mot
`role-label-grants-nothing` og oppdatere baselinen bevisst i samme endring.
Manglende/tom kildekatalog og lese-/traverseringsfeil skal ikke gi grønn test.

Faktisk statisk Python-opptelling av arbeidstreets Swift-kilder før og etter WP4:

```text
requireAdminUser: 48 matching Swift source lines
AdminRoleProfile: 33 matching Swift source lines
```

Innholdsdigest for `Sources` var identisk før og etter:
`ce2b21f7cf4f69b50bf36f182c1dd9170b6206b895b7b3e381ae6fcdb071ed3a`.
Dette er kildeinspeksjon, **ikke kjørt XCTest eller typekontroll**.
Ingen produksjonsendring, ny celle eller ny myndighetssti er skrevet.

**Bygg/typekontroll og alle Swift-tester: blocked / ikke kjørt**, etter oppdragets
eksplisitte sandboxbegrensning. Ingen `swift build`, `swift test`, docker eller
deploy er forsøkt. Eneste git-kommando var den pålagte branch-forhåndssjekken.
Losen må kjøre detached bygg, `ScaffoldRoleIsNotAuthorityTests` og full regresjon
mot dette arbeidstreet, med faktiske resultater før WP4 kan godkjennes.

### Feilretting require-existing — skrevet, ikke verifisert (2026-09-09)

Én avgrenset feilretting etter WP1+WP2. Forhåndssjekk uten git-kommandoer:
arbeidstreets `.git` peker på metadata for `_wt-sad-20260909`, metadataenes `HEAD`
angir `refs/heads/pdd/scaffold-admin-delegering`, og den lokale branchreferansen er
`e1f3e22f02239e44eacaf12a741d78b4066d0c35`. Handoff-regel 1–12 og arbeidstreets
`AGENTS.md` er lest. Bare kode i `CellScaffold/_wt-sad-20260909` og denne PDD-ens
to rapportfiler er endret.

**Årsak, kildebasert:** `addCellResolve` registrerer factory og Codable-type, men
oppretter ikke selve cellekatalogen. Det ubetingede `cellAtEndpoint`-kallet i
`refreshScaffoldAdministratorReadiness` var den opprettende stien: resolverens
`emitCellWithReference` for `.scaffoldUnique` faller tilbake til
`createAndRegisterCell`, som skriver `typedCell.json`. Dette er lest i den faktiske
CellProtocol-avhengigheten under
`CellScaffold/.build/sad-baseline/wp1scratch/checkouts/CellProtocol`, pin
`135d3c003c3932ee190cc1ec0fc0ae21ec766f21`. Kallet lå dessuten **før**
`ScaffoldOrchestratorCell.init` lastet `NamedEmitters.json`, slik at også en kald
omstart kunne opprette en ekstra registercelle før den gamle mappingen ble lest.

Skrevet endring:

- `CellScaffold/_wt-sad-20260909/Sources/App/configure.swift`: Begge administrator-
  og mandatregistreringene skjer etter at eierens orchestrator har lastet
  kanoniske mappinger. Hver registrering krever nå
  `eagerBootstrapPolicy == .provisionIfMissing` eller en eksisterende mapping for
  akkurat cellen. `shouldBootstrapResolver` avgjør ikke denne tillatelsen.
  Både vanlig oppstart og eier-reconciler sender policyen eksplisitt til readiness.
- `CellScaffold/_wt-sad-20260909/Sources/App/Support/ScaffoldAdministratorRuntimeSupport.swift`:
  Readiness bruker den eksisterende `requireSharedCanonicalMapping` før
  `cellAtEndpoint`. Den samme kontrollen som PaymentGate bruker, validerer lagret
  UUID/type/eier/nøkkelfingeravtrykk og gjenoppretter den eksakte instansen;
  manglende mapping kan bare provisjoneres når `provisionIfMissing` er sann.
  Feilstien beholder `scaffold_administrator_not_provisioned` og eksisterende
  unavailable-diagnostikk, uten å opprette et erstatningsregister.
- `CellScaffold/_wt-sad-20260909/Sources/App/Cells/SimpleProjectManager/ScaffoldOrchestratorCell.swift`:
  Kun synligheten til `requireSharedCanonicalMapping` er utvidet fra `private`
  til App-intern, med forklarende kommentar. Kontrollens implementasjon er uendret.
- `CellScaffold/_wt-sad-20260909/Tests/AppTests/ScaffoldAdministratorRegistryTests.swift`:
  Eksisterende test for lagret terskelpolicy sender orchestrator og eksplisitt
  `provisionIfMissing: false` ved gjentatt readiness. Ingen assertions er fjernet.

**Forventet virkning, ikke et testresultat:** På fersk lagring i `.requireExisting`
finnes ingen av de to mappingene, så ingen factory for disse cellene registreres.
Readiness stanser før det opprettende oppslaget og registrerer advarselen. Deretter
skal den uendrede PaymentGate-kontrollen fortsatt kaste
`persistedMappingUnavailable("PaymentGate")`, med samme tomme liste over
cellekataloger som før `configure(app)`. På lagret rot leses mappingen først, og
readiness kan gjenbruke det eksisterende registeret. `.provisionIfMissing` kan
fortsatt opprette et **tomt register**; ingen organisasjon registreres automatisk
som administrator.

**TopUp-konklusjon: begge nye testfeil henger sammen med WP1; de kan ikke avskrives
som miljø-/rekkefølgeflakiness.** Eksisterende `reg.full.log` viser to feil per test:

1. I `provisionEagerBootstrapProductionFixture` får begge `5 != 4` ved opptelling
   av `typedCell.json`. Testen forventer tre kanoniske bootstrap-celler pluss
   LiveInteraction. WP1s tomme administratorregister er den femte cellen.
2. Ved etterfølgende normal produksjonsstart er `RuntimeTreeSnapshot` endret med
   enda en celle. Den tidligere readiness-rekkefølgen over forklarer dette:
   registeret resolves før lagret mapping gjenopprettes. For allowlisted-testen
   viser loggen også den eksisterende `ScaffoldAdministratorRegistry`-mappingen
   under senere lasting av named emitters.

Bevis fra allerede kjørt regresjon, **ikke en ny kjøring i denne jobben**:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-sad-20260909/Tests/AppTests/TopUpCheckoutTests.swift:896: error: -[AppTests.TopUpCheckoutTests testSimulatedTopUpAllowsExplicitProductionAllowlistedUser] : XCTAssertEqual failed: ("5") is not equal to ("4") - Provision-only must create the three canonical eager-bootstrap Cells plus the explicitly inventoried LiveInteraction Cell.
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-sad-20260909/Tests/AppTests/TopUpCheckoutTests.swift:896: error: -[AppTests.TopUpCheckoutTests testSimulatedTopUpDefaultsToDeniedInProductionLikeEnvironment] : XCTAssertEqual failed: ("5") is not equal to ("4") - Provision-only must create the three canonical eager-bootstrap Cells plus the explicitly inventoried LiveInteraction Cell.
```

Kilde: `CellScaffold/.build/sad-baseline/reg.full.log`, linje 25614 og 25846;
snapshot-feilene står på 25742 og 25853, og registermappingen på 25735.
`retest.full.log` i samme mappe viser begge testene bestått i baselinen på linje
24359 og 24468. Det er lagringsassertions som feiler i regresjonsloggen, ikke
topup-rutenes allowlist-/denial-assertions.

TopUp-kode og tester er **urørt**. Rettingen forventes å fjerne omstartens ekstra
celle, men provisjoneringsinventarets `5 != 4` vil fortsatt måtte håndteres:
`.provisionIfMissing` oppretter fortsatt det tomme registeret. Ingen forventning
er hevet for å skjule en lagringsendring. Losen må vurdere eksplisitt inventar av
den femte cellen når dette bekreftes i detached kjøring.

Faktisk statisk opptelling før og etter denne rettingen, matchende linjer i
arbeidstreets `Sources/**/*.swift`:

```text
requireAdminUser 48
AdminRoleProfile 33
```

Ingen ny myndighetssti fra rolleetiketter er skrevet. De eksisterende 7
`ScaffoldAdministratorRegistryTests`- og 9 `ScaffoldMandateTests`-metodene finnes
fortsatt; dette er kildeopptelling, **ikke utførte tester**. `ScaffoldMandateTests`,
`OrchestratorPersistenceTests` og `TopUpCheckoutTests` er fil-for-fil uendret fra
før denne rettingen.

Bygg/typekontroll og alle Swift-tester: **blocked / ikke kjørt**, etter oppdragets
eksplisitte kø-/sandboxbegrensning. Ingen bygg, tester, git, docker eller deploy
er forsøkt. Status er **skrevet, ikke verifisert**. Losen må kjøre detached bygg,
den navngitte require-existing-testen, registerets 7 og mandatets 9 tester samt
full regresjon. Kald omstart med eksisterende register må fortsatt gjenbruke UUID
og lagret tilstand uten nye cellefiler; kildeinspeksjonen erstatter ikke den sjekken.

### WP2 verifisert 2026-09-09 12:05 UTC — GRØNT

```text
=== BUILD_RC=0 2026-09-09T12:04:43Z
=== TEST_RC=0 2026-09-09T12:05:33Z
	 Executed 16 tests, with 0 failures (0 unexpected) in 8.441 seconds
```

16 tester = WP1s 7 + WP2s 9, kjørt sammen mot `CellScaffold::_wt-sad-20260909`.
`requireAdminUser` uendret på 48.

Codex rapporterte korrekt «skrevet, ikke verifisert» denne gangen. To defekter måtte
likevel rettes før grønt:

- `Permission.fullPermissionString` er internal i CellBase; `permissionString` er public
  og gir nettopp firetegnsstrengen `-w-s` som koden sammenlignet mot. Ett ord.
  `lesson.cellbase-internal-members-look-public`.
- Testen skrev en sentinel til keypathen `profile` på abonnentens EntityAnchor og fikk
  `notFound` ved gjenlesing. EntityAnchor har registrerte keypaths; `profile` er ikke en
  av dem. Byttet til `relations.people[+]`, som `PersonalCopilotV1Tests` allerede bruker.
  Formålet er uendret: entitetsdataene skal overleve at rolleavtalen trekkes tilbake.
  `lesson.entityanchor-keypaths-are-registered`.

### Full regresjon etter WP1+WP2 — én ekte regresjon fra oss

```text
	 Executed 2145 tests, with 11 tests skipped and 93 failures (6 unexpected) in 336.588 seconds
	 unike feilende testnavn: 32
	 NYE feil mot baseline: 3
	 tidligere røde som nå er grønne: 30
```

**De 30 som ble grønne er ikke vår fortjeneste.** Baselinen ble målt på en ren eksport,
denne kjøringen i worktreet; flere av baseline-feilene var miljø- og fixtureavhengige
(blant annet Arendalsuka-atlaset). Sammenligningen er derfor gyldig for å finne *nye*
feil, ikke for å ta æren for gamle.

**Én av de tre nye er vår, og den er reell:**

    AppTests.OrchestratorPersistenceTests
    testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells

Testen kjører `configure(app)` i require-existing-modus mot fersk lagring og krever at
**ingen celle-kataloger opprettes**. Vår kode oppretter én. Det bryter vår egen
kontrakt, som sier at ingen administrator skal opprettes automatisk — og det er samme
klasse feil som formålet `authority-survives-or-fails-loudly` finnes for: tilstand som
materialiserer seg stille i en datarot der den ikke hører hjemme.

Første forsøk på retting — å flytte registreringene fra
`reconcilePortholePublishedCellResolves()` til `reconcileBootstrapOnlyCellResolves()` —
var **ikke nok**: `shouldBootstrapResolver` er sann også i denne testen, så vakten var
feil vakt. Riktig betingelse er `EagerBootstrapProvisioningPolicy`. Lagt som egen
feilretting i køen (`sad-fix-requireexisting-20260909`).

De to andre nye, begge i `TopUpCheckoutTests` om simulert topup i produksjonslikt miljø,
er sendt til undersøkelse — ikke til retting. De skal bare røres hvis de faktisk er våre.


### WP2 — skrevet, ikke verifisert (2026-09-09)

Representantmyndighet etableres av et eksplisitt **scaffold-eier-signert Contract**, ikke av organisasjonsnavnet eller en rolleetikett. Contractet navngir administrator-entiteten og er bundet til scaffoldRef samt siste registrerings-/overføringskvittering fra WP1. Scaffold-eier uten et slikt representantbevis kan tilbakekalle et mandat, men får ikke automatisk utstede på organisasjonens vegne. `signRepresentativeAgreement` signerer gjennom eksisterende Contract-kode; `installRepresentativeAgreement` bruker den samme private proof-lagringen. Ingen representanter er provisjonert i en kjørende tjeneste av denne jobben.

`administrator.thresholdPolicy` leses gjennom WP1-registerets produksjonsendepunkt. `administrate` krever policyens antall verifiserte, distinkte signatar-UUID-er; `use` krever én. Samme identitet to ganger teller én, også med forskjellig bokstavstørrelse i UUID. Signatarens nøkkel må komme fra det verifiserte representant-Contractet. Policyendring endrer ikke registreringskvitteringen, slik at terskelen kan heves uten nye kodeendringer eller automatisk representantprovisjonering. Administratorskifte gjør gamle representantbevis og mandater ubrukelige på det nye administratorgrunnlaget.

Et administratormandat kan etter positiv fixture navngi `mandate.issue`, og gir den kontraktsfestede lesetilgangen til mandater når det dekker scaffoldet. Det godtas **aldri som representantbevis for videre utstedelse**. Utstedelse og orgLink-handlinger krever fortsatt det separate, opprinnelige eier-signerte representant-Contractet. Et `use`-mandat som navngir mandat-/orgLink-utstedelse eller administratorhandling, avvises med `second_level_delegation_not_permitted`.

Bruk kontrollerer mottakerens nøkkelkontroll og lagrede signerte Agreement, eksakt ressurs/celle-UUID, handling og formål, utløp, signaturpolicy, administratorregistrering og tilbakekallsstatus. `mandate.revoke` beholder mandatet med `revokedAt` og begrunnelse. `orgLink.revoke` beholder rolleavtalen og markerer dens mandater tilbakekalt. Målcellens data og mottakerens beviskopi slettes ikke. Postene er ikke aktive før mottakerens proof-kopi/indeks er lest tilbake og sentral snapshot-lagring har fullført. En mislykket sentral lagring kan etterlate en uvirksom mottakerkopi; uten sentral aktiv post autoriserer den ikke.

Målcellekoblingen er skrevet i `ArendalsukaConfigurationPublisherCell.validateCellSpecificAccess` for de eksisterende `applyEditableCellConfiguration` og `resetEditableCellConfiguration`, med cellens eget publiseringsformål. Eierskap og eksisterende Agreements består som egne autorisasjonsgrunnlag. Mandatbruk installerer ikke en ubetinget Agreement i målcellen, som ellers kunne ha overlevd tilbakekall. Privat revisjonsspor registrerer både `issuerEntityRef` og `actingIdentityUUID` ved utstedelse, bruk og tilbakekall.

**Avgrensning i dette worktreet:** fixture-handlingen `publisherAccess.issue` finnes ikke i kilden på denne branchen. Fixture-casen prøver mandatets utstedelse og avgrensning; den beviser ikke at denne målcellehandlingen kan utføres. Den skrevne integrasjonstesten bruker i stedet cellens eksisterende reset-handling før/etter tilbakekall. Ingen ny `publisherAccess.issue`-handler er funnet på eller skrevet. Flere målceller må kobles til den felles mandatkontrollen for sine egne eksisterende keypaths/formål; resolverens generelle semantikk er ikke endret.

Faktisk statisk opptelling før og etter WP2, over worktreets `Sources`:

```text
requireAdminUser 48
AdminRoleProfile 33
WP1_registry_unchanged True
```

Antall rollehenvisninger har ikke økt. Dette er **ikke** en kjørt WP4-regresjon. Autorisasjonstestene er skrevet, men ingen Swift-test er kjørt i denne jobben.

## Terskel <a id="threshold"></a>

**Dekket av WP1 + WP2 — ingen egen arbeidspakke nødvendig.** Verifisert 2026-09-09 13:00 UTC,
43 tester grønne (ScaffoldAdministratorRegistry 7, ScaffoldMandate 9, OrchestratorPersistence 8,
TopUpCheckout 19).

`ScaffoldMandateTests.testSixThresholdFixturesReadWP1PolicyAndCountDistinctVerifiedSigners`
kjører alle seks fixturene i `contract/fixtures/threshold-policy.json` mot WP1s register:

- terskel settes gjennom `administrator.thresholdPolicy.set` **uten kodeendring**, og heving fra 1 til 2 tas i bruk umiddelbart av mandatutstedelsen
- én signatur mot terskel 2 avvises med `threshold_not_met`
- to distinkte styreidentiteter godtas
- to signaturer fra **samme** identitet avvises — de teller som én
- terskel 0 og terskel uten begrunnelse avvises med `invalidThreshold`/`invalidReason`, og policyen er **uendret etter avslaget** (lest før og etter)

`ScaffoldAdministratorRegistryTests.testRuntimeAdvisoriesFollowPersistedThresholdPolicy`
dekker `scaffold_administrator_threshold_below_two` mot den persisterte policyen.

Formålet `threshold-matches-blast-radius` er dermed oppfylt slik det er formulert. WP3 i
PLAN.md er ikke droppet — den er levert av WP1 og WP2 sammen, og dette er beviset.


_ikke kjørt ennå — WP3_

## Advarsel ved tom datarot <a id="advisory"></a>

**Dekket av WP1.** Verifisert i kjøringen 2026-09-09 13:53 (48 tester grønne).

- `ScaffoldAdministratorRegistryTests.testMissingScaffoldOwnerStillReportsUnprovisionedAtStartup` — oppstart uten registrering gir `scaffold_administrator_not_provisioned`, ikke en stille opprettet administrator.
- `testSeparateScaffoldRootDoesNotInheritRegistration` — en annen datarot arver ingenting. Dette er 19. august-feilen skrevet som test.
- `testRuntimeAdvisoriesFollowPersistedThresholdPolicy` — `scaffold_administrator_threshold_below_two` følger den persisterte policyen.

Formålet `authority-survives-or-fails-loudly` er dermed oppfylt: myndighet som mangler
sier fra, i stedet for å forsvinne stille slik den gjorde i august.

## Mandatliste for eier <a id="mandates"></a>

**Dekket av WP2.** `ScaffoldMandateTests.testOwnerCanListAndNonOwnerGetsDenialIncludingEmptyResource`:
eier ser aktive mandater på egen celle, og en ikke-eier får **avslag**, ikke en tom liste.
Skillet er poenget — en tom liste ville lekket at det ikke finnes noe å se.

## Tilbakekall av organisasjonstilknytning <a id="revoke"></a>

**Dekket av WP2.** `ScaffoldMandateTests.testRoleAgreementAloneGrantsNothingAndRevocationPreservesEntityData`:
rolleavtalen alene gir ingen tilgang, tilbakekall stopper mandatene under den, og
subjektets entitetsdata står urørt — verifisert både i minnet og etter gjenlasting av
cellen fra lagring. `testTargetCellChecksMandateOnEveryCallAndRevocationRetainsDataAndAuditPair`
dekker at målcellen sjekker mandatet ved hvert kall, og at revisjonssporet navngir både
organisasjonen og den handlende identiteten (formålet `audit-names-org-and-person`).

## Registerlesing <a id="registry"></a>

### Verifisert 2026-09-09 11:10 UTC — GRØNT

Alt under overskriften «WP1, 2026-09-09» nedenfor er Codex' rapport fra selve slicen,
der bygg og tester sto som `blocked`. Den er beholdt uendret som kilde, men
**statusene «blocked» der er nå erstattet av denne kjøringen.**

```text
=== BUILD_RC=0 2026-09-09T11:10:03Z
=== TEST_RC=0 2026-09-09T11:10:25Z
	 Executed 7 tests, with 0 failures (0 unexpected) in 3.911 seconds
```

Kjørt som detached skript med `danger-full-access` mot `CellScaffold::_wt-sad-20260909`
(`CellScaffold::.build/sad-baseline/wp1build.sh`), ikke som køjobb. Rollelinjene er
uendret mot baselinen: `requireAdminUser` 48, `AdminRoleProfile` 33 — WP1 innførte
ingen ny myndighetssti fra rolleetikett.

#### Slicen var ikke levert da den meldte at den var det

Codex rapporterte «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga
**50 kompileringsfeil**, og etter at de var rettet feilet **4 av 7 tester**. Begge var
ekte defekter. Årsaken til at det slapp gjennom var min egen instruks om å markere
bygget som blocked — da ble syntakssjekken eneste bevis
(`lesson.syntax-check-reported-as-delivered`).

**Feil 1 — 50 kompileringsfeil, én årsak.** `DecodingError.dataCorruptedError(...)`
finnes ikke i App-modulen: CellBase eksporterer sin egen `DecodingError`
(`CellProtocol::Sources/CellBase/Errors.swift:50`) som skygger for Swifts. Rettet med
`Swift.DecodingError` og en kommentar som forklarer hvorfor.
`lesson.cellbase-decodingerror-shadows-swift`.

**Feil 2 — fire tester som aldri kunne bli grønne.** Testene sammenlignet hele
`ValueType.object`-verdier med `XCTAssertEqual`. CellBase' `ValueType.==` har
`case (.object(_), _): return false`, og tilsvarende for `.list`, `.data`, `.keyValue`,
`.identity` med flere, uten strukturell fallback
(`CellProtocol::Sources/CellBase/ValueTypes/ValueType.swift:241-330`). **To identiske
objekter er aldri like.** Feilmeldingene så ut som rekkefølgeproblemer, men
sammenligningen kunne ikke lykkes uansett innhold. Rettet i testen med en
`assertSameValue`-hjelper som sammenligner kanonisk JSON (`.sortedKeys`); feltvise
assertions på skalarer er beholdt uendret — de virket hele tiden.
`lesson.valuetype-equality-false-for-objects`.

Dette siste er et funn i CellBase, ikke bare en testregel. Jeg gikk gjennom
App-kildene og fant ingen produksjonskode som sammenligner hele `ValueType`-verdier —
de destrukturerer først. CellBase selv er ikke revidert utover dette. En
`Equatable`-conformance som alltid svarer «ulik» for sammensatte verdier er en felle
som ikke gir feilmelding, og fortjener en egen vurdering.


WP1, 2026-09-09: **kilde og tester skrevet; bygg og funksjonell verifikasjon blocked**. Formål: `purpose://candidate.scaffold-admin.org-is-registered-administrator`. Kun WP1 er utført.

Forhåndssjekken ble kjørt først i `CellScaffold/_wt-sad-20260909`. Faktisk utdata, exit 0:

```text
pdd/scaffold-admin-delegering
e1f3e22f
       0
```

Implementasjonen ligger i dette worktreet:

- `Sources/App/Cells/Admin/ScaffoldAdministratorRegistryCell.swift`: tre get- og tre set-nøkler fra kontrakten, med Explore-kontrakter. `administrator.register` er idempotent for samme entitet og avviser overskriving; `administrator.transfer` gir egen revisjonsoppføring og Flow-kvittering. Alle tre skriver bare etter produksjonens `authorizationDecision` med verifisert `ownerProof`.
- `Sources/App/configure.swift` og `Sources/App/Support/ScaffoldAdministratorRuntimeSupport.swift`: registrering som `.scaffoldUnique`/`.persistant` i eksisterende scaffold-eierkontekst, gjenoppretting ved oppstart og oppdatering av de to advarslene. Ingen administrator opprettes automatisk. Feil ved lasting av registeret gir også `scaffold_administrator_registry_unavailable` i eksisterende readiness-mekanisme.
- `Sources/App/Support/CanonicalCellRuntimeReadinessStore.swift`: presisert dokumentasjon av offentlig scaffoldreferanse og policybegrunnelse i advisories; lagringsmekanismen er uendret.
- `Tests/AppTests/ScaffoldAdministratorRegistryTests.swift`: **7 nye testmetoder**, opptalt fra kilde; **ingen av dem er kjørt**.

Registeret følger dataroten. Den offentlige etiketten settes ved førstegangsoppretting fra `CELL_SCAFFOLD_REF`, eksempelvis `scaffold:cellscaffold-staging`; standard er `scaffold:cellscaffold`. Etiketten er persistert, gir ingen myndighet og erstatter ikke resolverens scaffold-avgrensning. Alle set-payloads må treffe den lagrede `scaffoldRef`. Et senere miljøvariabelbytte overskriver ikke registeret.

`administrator.state` inneholder bare de fem kontraktfeltene. `registeredBy` og policyens `setBy` er eksplisitt `null`: kontrakten oppgir feltnavnene samtidig som den forbyr personidentiteter i offentlig state, og scaffold-eierens organisasjon er ikke etablert av denne registreringen. Handlende identitet ligger i den private, persisterte revisjonsoppføringen. Organisasjonsreferansen er scaffold-eierens erklæring om en organisasjonsentitet, med validert `entity:`-format; WP1 verifiserer ikke organisasjonens rettslige status eller hvem som kan signere på dens vegne.

Startpolicy er lagret med `requiredSignatures = 1`, begrunnelse `utviklingsfase, styreleder alene` og dato `2026-09-09T00:00:00Z`. `administrator.thresholdPolicy.set` godtar heltall 1–5 og begrunnelse 8–512 tegn. Heving til 2 krever ingen kodeendring. Oppstart uten registrering gir `scaffold_administrator_not_provisioned`; policy under 2 gir `scaffold_administrator_threshold_below_two` med scaffold, begrunnelse og dato. Begge vises gjennom eksisterende `/health/ready` → `runtimeAdvisories`.

Skriving serialiseres og bruker `CellResolver.persistCellSnapshot`, fulgt av gjenlesing gjennom `TypedCellUtility` og sammenligning av hele registeret før vellykket svar/Flow. Dette er lokal lagringsbekreftelse, ikke en garanti mot strømtap eller en distribuert commit. Historikk er beskyttet av eksisterende eier-/Agreement-kontroll; selvgodkjent leseavtale gir ikke tilgang.

| Test i `ScaffoldAdministratorRegistryTests` | Dekning | Status |
|---|---|---|
| `testRegistryReadNamesOnlyOrganizationForUnrelatedIdentities` | Produksjonsresolver, delt scaffold-celle, offentlig organisasjonsreferanse uten personidentitet, idempotens | blocked |
| `testTransferIsSeparateAuditedActionAndSurvivesProductionStorageReload` | Avvist overskriving, Digipomps → DiMy, egne kvitteringer, Flow, faktisk lagringsgjenlesing og Explore etter reload i strict-modus | blocked |
| `testRuntimeAdvisoriesFollowPersistedThresholdPolicy` | Faktisk `/health/ready`, begge advarsler, heving til 2, gjenlasting og senking til 1 | blocked |
| `testRegistryDeniesMissingOwnerProofAndInvalidPayloadsWithoutMutation` | Uvedkommende/forfalsket eier-UUID, feil scaffold, identitet i stedet for entitetsreferanse, ugyldig terskel/begrunnelse | blocked |
| `testHistoryRequiresExistingOwnerAuthorizedAgreementPath` | Privat historikk, avvist selvgodkjenning, eksisterende signert Agreement-vei, ingen skriverett fra leseavtalen | blocked |
| `testSeparateScaffoldRootDoesNotInheritRegistration` | Egen datarot/scaffold arver ikke administrator | blocked |
| `testMissingScaffoldOwnerStillReportsUnprovisionedAtStartup` | Begge advarsler også når scaffold-eieren mangler | blocked |

Testene kaller `configure(app)` og løser `cell:///ScaffoldAdministratorRegistry` gjennom produksjonsresolveren før normal `get`/`set`. Miljøhjelperne setter bare opp applikasjon og identiteter; de registrerer ingen alternativ fabrikk, oppretter ikke registercellen direkte og slår ikke av autorisasjon. Gjenlasting leser resultatet fra produksjonens lagring, ikke en separat testserialisering.

Faktisk kjørt syntakssjekk fra worktreet:

```sh
swiftc -frontend -parse Sources/App/Cells/Admin/ScaffoldAdministratorRegistryCell.swift Sources/App/Support/ScaffoldAdministratorRuntimeSupport.swift Sources/App/Support/CanonicalCellRuntimeReadinessStore.swift Sources/App/configure.swift Tests/AppTests/ScaffoldAdministratorRegistryTests.swift
```

Resultat: **exit 0, ingen stdout/stderr**. Dette parser fem filer; det er ikke typekontroll, bygg eller testkjøring.

Faktisk Explore-kildeaudit med `CellProtocolDocuments/Tools/Explore/explore_contract_audit.py`, avgrenset til den nye cellen: **5 kall inspisert, 4 handler-deklarasjoner, 4 eksplisitte kontraktdeklarasjoner, 0 feil, 1 advarsel**:

```text
dynamic_key_needs_manual_review
Sources/App/Cells/Admin/ScaffoldAdministratorRegistryCell.swift:188
Handler key or method is computed and cannot be proven by this source audit.
```

Manuell oppfølging: de tre bokstavelige set-nøklene går gjennom samme `registerMutation`, som publiserer eksakt Explore-kontrakt før intercepten og kontrollerer `ownerProof` før mutasjon. De fire deklarasjonene er tre get-deklarasjoner og én gjenbrukt set-deklarasjon; auditen teller ikke seks runtime-operasjoner. Separat kildekontroll mot JSON-kontrakten ga faktisk:

```text
Contract key mapping: 3 GET + 3 SET, exact match
Mutation helper: all three literal keys reach ownerProof guard, serialization and persisted readback
Public registeredBy/setBy: null; actor stored only in private audit
Advisory codes: both contract codes present
New authority code: no requireAdminUser or AdminRoleProfile references
```

Faktisk opptelling før/etter i worktreets `Sources`: `requireAdminUser` **48 → 48 linjer / 48 → 48 forekomster**; `AdminRoleProfile` **33 → 33 linjer / 34 → 34 forekomster**. Baselinens «33» svarer til linjetreff, ikke enkeltforekomster. Ingen vekst. SHA-256-sammenligning av `Sources`/`Tests` før/etter viste bare de fem filene ovenfor endret/lagt til og ingen slettede filer; ingen ytterligere git-kommando ble brukt.

Bygg, typekontroll, `test.admin.registry-read` og regresjon er **blocked** av den forhåndsmålte workspace-write-begrensningen `sandbox-exec: sandbox_apply: Operation not permitted` (`lesson.codex-workspace-write-cannot-build-cellscaffold`). SwiftPM-bygg/test ble etter oppdragets instruks ikke forsøkt på nytt. Ingen nye `Executed`-tall foreligger, og ingen påstand om grønn funksjonalitet eller fravær av nye regresjoner er gjort. Den detached kjøringen må bruke worktreets kode og starte med de 7 testene via `scripts/run_swift_bounded.sh test --filter ScaffoldAdministratorRegistryTests`, etter vanlig kapasitetsport. Nødvendige API-er er kildekontrollert mot baselinens faktiske CellProtocol-pin `135d3c003c3932ee190cc1ec0fc0ae21ec766f21`; dette erstatter ikke bygg.

## WP0 — sluttmelding

WP0 målte forhåndsstatus i `CellScaffold` (`pdd/tillitspakke-agentflaate`, `1dbdee23`, 181 skitne statusoppføringer; de første 30 er gjengitt), kjørte `swift build` og deretter `swift test` uten filter, og telte `requireAdminUser` (**48**) og `AdminRoleProfile` (**33**) i Swift-kildene. Målingene er fra 2026-09-09, ca. 04:52–04:55 CEST.

Baseline er **RØD / blocked av kjøremiljøet**: byggkommandoen brukte **2.481 sekunder**, og testkommandoen brukte **1.604 sekunder**, begge med exit 1. Dette er testkommandoens varighet fram til manifestfeilen, ikke tiden for en gjennomført testmengde. Begge stoppet på `sandbox-exec: sandbox_apply: Operation not permitted`. Ingen tester startet, ingen `Executed`-linjer foreligger, og hvilke navngitte tester som er røde fra før er derfor **ikke målt**. Ingen testantall eller tidligere røde tester er kopiert fra en annen rapport (`lesson.baseline-count-from-report-not-run`).

Det skitne treet alene stopper ikke WP1, i tråd med oppdraget. Forhåndssjekken viser også endret `Package.resolved`, men virkningen av denne endringen og de øvrige 151 ikke-navngitte statusoppføringene er ikke undersøkt. Det er ikke påvist en konkret kildekonflikt som krever venting. **WP1-kildeimplementering bør likevel vente på en faktisk bygg- og full testbaseline før endring**, fordi denne kjøringen ble blokkert før teststart; eksisterende røde tester ville i seg selv ikke vært en stoppgrunn. Neste utfører trenger et kjøremiljø hvor de foreskrevne Swift-kommandoene kan fullføre, og må knytte den nye kjøringen til treet som da faktisk måles. Stabilitet i treet gjennom målevinduet er ikke bekreftet med en ny git-sjekk, siden oppdraget begrenser git til forhåndssjekken.

Ingen kildefiler er redigert av WP0. Ingen branch er laget eller byttet, ingen commit, ingen øvrige git-operasjoner og ingen docker er utført. Kun `TESTRESULT.md` og én linje under `STATUS.md` → `Logg` er skrevet av utføreren; ingen separate loggfiler er opprettet. WP1–WP10 er ikke utført.


## WP1 — sluttmelding

WP1-kode og 7 tester er levert i `CellScaffold/_wt-sad-20260909`: persistert scaffold-register, separate registrerings-/overføringshandlinger med revisjonsspor, offentlig organisasjonslesing, registrert terskelpolicy og begge runtime-advarsler. Syntaks og statiske kontraktkontroller er kjørt; rollehenvisningene har ikke økt. Bygg, typekontroll og alle Swift-tester er **blocked/ukjørt** med workspace-write-årsaken ovenfor. Koden er derfor ikke funksjonelt godkjent. Ingen git-operasjoner utover oppdragets forhåndssjekk, ingen docker og ingen deploy er utført.

WP2 trenger den registrerte `administratorEntityRef` og `administrator.thresholdPolicy` fra denne cellens produksjonsendepunkt. Fortsett i eksisterende `ArendalsukaImportAccessCredentialSupport`/Agreement-mønster med identitetsbundet bevis og mottakerens egen EntityAnchor-indeks. WP1 har ikke laget en ny credential-mekanisme, utstedt mandater, etablert signaturmyndighet for organisasjonen eller implementert tilbakekall. WP2 må binde organisasjonen til faktiske signatarbevis og håndheve mandatets ressurs, handling, formål, utløp og tilbakekall. Faktisk signaturtelling/unikhet er fortsatt WP3; registrering av en terskel håndhever ikke signaturer i seg selv. Historikkens eksisterende, eiergodkjente Agreement-vei er tilkoblingspunktet for senere mandatkontroll, uten å åpne de tre eierbeskyttede skrivehandlingene. `registeredBy`/`setBy` er offentlig `null`; ikke fyll dem med personidentiteter.

Integrator må først kjøre detached bygg og de nye testene mot dette worktreet, deretter vurdere regresjon mot den målte baselinen. Virkelig registrering av Digipomps/DiMy og scaffoldets driftsnavn hører til den senere, autoriserte provisionerings-/deployleveransen.


## WP2 — sluttmelding

**Skrevet, ikke verifisert.** Mandatform, signerte Agreements, gjenbrukt EntityAnchor-proof-lagring, organisasjonsbundet representantkontroll, policybasert signaturtelling, ett ledd, tilbakekall, eier-/administratorlesing og revisjonsspor er skrevet i `CellScaffold::_wt-sad-20260909`. Det samme gjelder 9 testmetoder med alle 2 + 14 + 6 fixture-casene og en integrasjonstest mot publisher-cellens eksisterende handling. WP1-registeret er uendret; `requireAdminUser`/`AdminRoleProfile` står fortsatt på 48/33.

Alt dette er **ubygd og utestet**: syntaks og statisk kildeinspeksjon erstatter ikke bygg, typekontroll, funksjonell verifikasjon eller regresjon. Losen må kjøre detached bygg og `ScaffoldMandateTests`, WP1s `ScaffoldAdministratorRegistryTests` og de eksisterende importbevis-/Arendalsuka-autorisasjonstestene som berøres av uttrekket til felles lagring. Eventuelle feil må rettes før en funksjonell akseptanse. Ingen git-operasjoner utover forhåndssjekkens to lesekommandoer, ingen docker og ingen deploy er utført.

## Feilretting require-existing — sluttmelding

**Skrevet, ikke verifisert.** Administrator-/mandatregistrering følger nå
provisjoneringspolicy og gjenopprettede mappinger. Administrator-readiness bruker
PaymentGates eksisterende kanoniske kontroll før endpoint-oppslag. Dette forventes
å bevare tom lagring og PaymentGate-avvisningen i den navngitte require-existing-
testen, og å unngå et ekstra register ved kald omstart.

`requireAdminUser` er fortsatt 48; `AdminRoleProfile` er 33. TopUp-loggene viser
WP1-relaterte lagringsfeil, og testene er urørt: inventarets `5 != 4` forventes å
gjenstå selv om den ekstra cellen ved omstart forsvinner. Se `#auth` for bevis og
avgrensning. Losen trenger detached bygg og regresjon, inkludert registerets 7 og
mandatets 9 tester. Ingen bygg/test, git, docker eller deploy er kjørt i denne jobben.

WP3 trenger WP1s `administrator.thresholdPolicy` og WP2s produksjonssti `mandate.issue` med signeringskonvolutten beskrevet over. Terskelcasene er allerede skrevet; de må kjøres mot faktisk lagring og deretter brukes til å bekrefte heving 1 → 2 med samme representantbevis, to distinkte signatarer, duplikatavslag og advisory-linjen. En virkelig utstedelse forutsetter eksplisitte eier-signerte representant-Contracts og at mottakerens eksisterende lokale/vault-/bridge-signaturhåndtak kan gjenopprettes for lagring i egen EntityAnchor. Manglende håndtak feiler lukket. Denne jobben har ikke etablert hvem som faktisk kan signere for Digipomps/DiMy, laget GUI/provisjoneringsseremoni, koblet alle målceller til mandatet eller implementert den manglende `publisherAccess.issue`-handlingen. Fixture-/transportpresiseringene og WP1s avvikende enum-navn for ugyldig policy står under Kontrakt og Autorisasjon; de må beholdes synlige under detached verifikasjon.


## WP4 — sluttmelding

**Skrevet, ikke verifisert.** Kun WP4 er utført: ny
`CellScaffold/_wt-sad-20260909/Tests/AppTests/ScaffoldRoleIsNotAuthorityTests.swift`
med fire rolletester og tellertest. Testene bruker produksjonens rolleinnmelding,
proof-keypaths og støttede EntityAnchor-lagring, sammenligner rolleholderens
avslag med en fremmeds på alle fire handlinger, og har positive kontroller med
faktisk eier-/representantmyndighet. Tellertestens grenser er 48 og 33, med krav
om bevisst vurdering mot `role-label-grants-nothing` ved økning.

Produksjonskildene er uendret; ingen ny celle, øvrig arbeidspakke, docker eller
deploy inngår. Bygg, typekontroll og Swift-tester er **blocked / ikke kjørt**
etter oppdraget. Bare den pålagte branch-forhåndssjekken brukte git. Losen trenger
detached bygg og kjøring av de fem nye testmetodene mot dette arbeidstreet,
deretter full regresjon. Kildeopptelling og skrevne assertions er ikke
kjørebevis; WP4 avventer disse resultatene.

## WP9 — dokumentasjon og kildeinspeksjon, 2026-09-09

**Ingen bygg eller tester kjørt i WP9.** Dette er fil-/kildeinspeksjon og
avstemming mot tidligere kjøringer, uten nye `Executed`-tall. Hele TESTRESULT
er lest. De senere grønne verifikasjonene under [#registry](#registry),
[#auth](#auth), [#threshold](#threshold), [#advisory](#advisory),
[#mandates](#mandates) og [#revoke](#revoke) er nåstatus; tidlige blocked- og
«skrevet, ikke verifisert»-rapporter er historikk. Også den gamle linjen
`_ikke kjørt ennå — WP3_` overstyres av den daterte grønne verifikasjonen
rett over den. Historiske rapporter og råutdata er ikke omskrevet.

### Artefakter L1–L7 <a id="wp9-artifacts"></a>

Forhåndssjekk uten git-kommando: `CellScaffold/_wt-sad-20260909/.git` peker
til arbeidstreets metadata; metadataenes `HEAD` inneholder
`ref: refs/heads/pdd/scaffold-admin-delegering`. De to nye cellefilene og de
tre PDD-testsuitene finnes der. Ingen git-status, commitlogg eller landing
er kontrollert.

| Rad | Faktisk filinspeksjon | Grense |
| --- | --- | --- |
| L1 | FORMAALSSPEC §3 finnes; STATUS fører G1 godkjent 2026-09-08. | Historisk brief er ikke ny staging-verifikasjon. |
| L2 | Begge JSON-kontrakter og tre fixturefiler finnes. Kontraktenes status/request-form er oppdatert med synlige begrensninger; byte-identiske speil er lagt i `Book/scaffold-administrator_v1.json` og `Book/scaffold-mandate_v1.json`. | JSON-lesing og speillikhet er filinspeksjon, ingen ny kontraktvalidator-/Swift-kjøring. |
| L3 | `dataflow.md` har K1–K14 og fire forbudte kanter, nå med faktisk intern kontrollsti og planlagte mål skilt ut. | Se #wp9-dataflow. |
| L4 | Kode og tester finnes i riktig worktree; tidligere kjørebevis er under #registry/#auth. | Ett commit per bladformål, review og landing er uverifisert av WP9. |
| L5 | Hele TESTRESULT er lest og historiske kjøringer beholdt; WP9-inspeksjoner er lagt til her. | Siste regresjon under #auth er 2150/90/29, null nye. Dette er eksisterende bevis, ikke ny måling. |
| L6 | `ACCEPT.md` er opprettet med L1–L7 og ankerne docs/stubs/status/audit. | G3 venter på Kjetil. |
| L7 | `handoff/WP10_DEPLOYKO.md` finnes som forberedt posttekst, eier Kjetil. | Ingen kvittering for registrering i HAVEN-Deploy er dokumentert/kontrollert; WP9 har ikke opprettet noen ekstern køpost. WP10 deploy er ikke kjørt. |

Fixturene er uendret og byte-identiske med arbeidstreets
`Tests/AppTests/Fixtures/ScaffoldMandate/`: 2 positive, 14 negative og
6 terskelcaser. Tidligere runtime-materialisering med reelle nøkler og
relative datoer, samt feilkodepresiseringene, er beskrevet under #contract.
JSON-filene, kontraktspeilene og dokumentenes lokale lenker/ankre er kontrollert
som filinspeksjon. Ingen renderer eller testsuite er kjørt.

### Dokumentdiff <a id="wp9-documentation"></a>

`test.docs-updated`: dokument-/kildeinspeksjon utført. Book 04 §13 beskriver
mandat, fem felt, ett ledd, separat representant-Contract, rollevern og audit.
Book 07 §9 beskriver organisasjon per scaffold, administratorskifte, lagret
terskel 1 med «utviklingsfase, styreleder alene», advisories og datarotgrenser.
Book 22 beskriver faktiske GET/SET-operasjoner, signeringskonvolutt og private
lesesuffikser. Endrede seksjoner er datert `Last verified against code:
2026-09-09`, med CellScaffold branch `pdd/scaffold-admin-delegering`.
Datoen gjelder disse seksjonene, ikke ny verifikasjon av hele boka eller staging.

Kontraktene/Book-speilene avstemmer faktisk request-form, feilkoder og de
uimplementerte delene. Gap Analysis, dataflow og WP10-postteksten skiller
grønt testbevis fra planlagt integrasjon/deploy. Ingen kapittelidentitet eller
katalogmetadata er endret; `book_catalog.json` er urørt. Ingen formål er
promotert til Book 23. Dokumentdiffen er beskrevet i [ACCEPT.md#docs](ACCEPT.md#docs).
Landing sammen med kode er integratorens gjenstående arbeid.

### Handlerinventar <a id="wp9-stubs"></a>

`test.cell.stub-scan`: **kildeinspeksjon utført med navngitte avvik**.
Hele `ScaffoldAdministratorRegistryCell.swift` og `ScaffoldMandateCell.swift`
er lest, inkludert løkkene, felles handlerhjelpere, mutasjon, lesing, audit og
lagring. Alle 13 kontraktoperasjoner har normal logikk; ingen er en ubetinget
tom suksesshandler. Fullt inventar: [ACCEPT.md#stubs](ACCEPT.md#stubs).

- Registerets tre GET-handlere har weak-self-fallback (`.null`, `.null`, `[]`).
  Alle tre SET-handlere deler `guard let self else { return .null }`.
  Manglende eksplisitt feil er **SAD-03, `not-implemented`**; livsløpsgrenene
  er ikke runtime-verifisert i det fremlagte beviset.
- Registerets samme-organisasjon-retur og gjentatt `mandate.revoke` er
  tilsiktet idempotens med grønne assertions. Gjentatt `orgLink.revoke` har
  samme type kildegren, men separat retry-bevis er ikke dokumentert.
- Mandatcellens weak-self-grener kaster `persistenceUnavailable`.
  Ufullstendige GET-valg og fangede autorisasjonsfeil avvises, ikke tom suksess.
- Mandat alene gir ikke registerhistorikk (**SAD-02, `not-implemented`**).
  `publisherAccess.issue` mangler i målcellen på denne branchen
  (**SAD-01, `not-implemented`**); positive fixtures beviser ikke utførelse.

Avstemt mot [Gap Analysis SAD-01–SAD-05](../../Gap_Analysis.md#scaffold-admin-delegering).
Dette lukker kravet om synlig dokumentasjon av stubber, ikke kodegapene.

### Dataflyt <a id="wp9-dataflow"></a>

K1–K6 er avstemt mot registerets GET/SET og runtime-advisories; grønt bevis
står under #registry/#threshold/#advisory. K7 krever separat organisasjonsbundet
representant-Contract; K8 bruker mottakerens eksisterende EntityAnchor-proof-
og indeksvei. K11–K14 svarer til `mandate.list`, `mandate.revoke`,
`orgLink.issue/revoke` og privat audit; #auth/#mandates/#revoke har beviset.

K9/K10 er kjørt grønt for publisherens `resetEditableCellConfiguration`.
K10 er presisert fra antatt offentlig GET til faktisk intern
`ScaffoldMandateProofSupport.authorize` → `ScaffoldMandateCell.authorize/validate`.
`revocationRef` binder den beholdte posten. `applyEditableCellConfiguration`
er koblet i kilde, men kjøringen beviser ikke publisering; `publisherAccess.issue`
og øvrige navngitte målcelleintegrasjoner er ikke ført som levert.
De fire kantene som med vilje ikke finnes er beholdt.

### Revisjonsspor <a id="wp9-audit"></a>

`test.admin.audit-pair`: avstemt med #revoke og faktisk kilde.
`ScaffoldMandateCell.Audit` inneholder `operation`, `mandateID`, `orgLinkRef`,
`issuerEntityRef`, `actingIdentityUUID`, `reason` og `at`. `issue` fyller
mandat-ID, verifisert utstederorganisasjon og requesterens UUID før `persist`.
`authorize(recordUse: true)` registrerer organisasjon og bruker; tilbakekall
registrerer den handlende identiteten.

Den grønne `testTargetCellChecksMandateOnEveryCallAndRevocationRetainsDataAndAuditPair`
krever `entity:digipomps` og subjektets UUID ved reset-bruk, samt eierens UUID
ved tilbakekall. Den grønne registeroverføringstesten krever Digipomps → DiMy,
ulike kvitteringer, gjenlastet historikk og eierens `actingIdentityUUID` i lagret
audit. Alle utstedelsesfeltene er i tillegg kontrollert i kilde; inspeksjonen
hevder ikke egne runtime-assertions på hvert felt. Sporet er privat persistert
celle-state, med redusert offentlig state/Flow. Ingen staging-utstedelseslogg
eller nytt audit-endepunkt er levert. Se [ACCEPT.md#audit](ACCEPT.md#audit).

### Status <a id="wp9-status"></a>

`test.status-current`: én WP9-logglinje er lagt til i STATUS. G1/G2 beholdes,
G3 står som venter. Linjen viser at dokumentarbeidet er skrevet og at
WP10/deploy, staging-entiteter, representantoppsett, Vegars tilgang og juridisk
vurdering gjenstår, med akseptansegrensen null nye feil. Commitstruktur/landing
og ekstern køregistrering er ikke bekreftet. [ACCEPT.md#status](ACCEPT.md#status)
lister de gjenstående punktene eksplisitt. WP9 godkjenner ingen port.

## WP9 — sluttmelding

Dokumentkapitler, kontraktstatus/Book-speil, gap-/no-op-avstemming, dataflyt,
WP10-presisering og ACCEPT er skrevet, samt denne inspeksjonsrapporten og én
STATUS-linje. Bygg, tester, kode, git, Docker og deploy er ikke utført av WP9.
Integrator/Kjetil må følge opp review/landing, G3, avvik og den faktiske
HAVEN-Deploy-posten; dokumentleveransen gir ingen stagingtilgang.
