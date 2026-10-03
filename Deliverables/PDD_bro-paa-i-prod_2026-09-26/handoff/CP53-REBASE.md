STATUS: LEVERT — head 101e5452ed7aecbbf947ed1205c3941ec24782a8, base 9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366, CI grønn (https://github.com/Digipomps/CellProtocol/actions/runs/36373503285)

# CP53 — rebase på dagens main

Oppdatert: 2026-09-28T05:40:20+02:00.
work_id: `CP53-REBASE-20260928`; implementør/eier: Codex; integrator: Losen; beslutningseier: Kjetil.

[PR #53](https://github.com/Digipomps/CellProtocol/pull/53) er **OPEN og ikke merget** (`mergedAt=null`). Ingen utrulling eller konsument-pin er endret. Oppgaven gjelder bare rebase, komposisjonskontroll, verifikasjon og push av samme gren.

- Repo/arbeidstre: `CellProtocol/_wt-bro-kanal-auth-20260927`.
- Gren: `pdd/bro-kanal-auth`.
- Gammel head: `b4f66b4ece1692ea6ddb2429b252c8cac4f16562`.
- Gammel base: `a6fa51a8db059c64d5171cbc8d454eea412ada9d`.
- Ny base: `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366` (#54, tag `2026.9.3`).
- Ny head: `101e5452ed7aecbbf947ed1205c3941ec24782a8`.
- Lokal sikkerhetsgren med gammel head: `codex/cp53-pre-rebase-20260928`.

## Rebase og bevart historikk

Kjørte `git fetch origin` og `git -c rerere.enabled=false rebase --rebase-merges --empty=keep origin/main`. Alle **23 commits** ble replayet, uten squash eller dropp. Verifisert samme rekkefølge, commit-meldinger, forfattere og forfatterdatoer. De eksisterende `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`- og `Claude-Session: https://claude.ai/code/session_011CHU13qBKbb5szsQQo53rW`-trailerne er bevart. Commit-SHA og committerdato endres ved rebase.

`git range-diff a6fa51a..b4f66b4 9c60001..101e545` viser 22 like patcher og én konteksttilpasning i konfliktcommit `4132c45 → 9c07bdc`. Ingen produksjonskode måtte konfliktløses. `git diff --check` består.

## Konfliktliste — én konflikt

| Fil / replay-commit | Hva main endret | Hva PR-en endret | Sammenslått løsning og bevis |
|---|---|---|---|
| `.github/workflows/cellprotocol-swift-linux.yml`, `4132c45 → 9c07bdc` | #54 legger `IdentityLinkGenesisClassificationTests` i Linux-suitene og kopierer `TestSupport/SimulatedEntity.swift` til Linux-testpakken. | Kopierer `TestSupport/MockBridgeTransport.swift` og `TestSupport/AuthenticatedBridgeFixture.swift`, slik at brotester bruker den autentiserte kanalporten. | Beholder genesis-suiten og **alle tre** støttefiler i samme `cp`-kommando. Konflikten var samtidige tillegg etter `MockIdentityVault.swift`, ikke alternative implementasjoner. Endelig diff mot main legger bare til PR-ens to fixture-linjer. Linux-CI verifiserer den sammensatte pakken. |

Rå konflikt: `/private/tmp/cp53-rebase-evidence/conflict-1.diff`.

## Nye BridgeBase-brukere på main og ready-regelen

**Ingen nye eller endrede BridgeBase-/bridge-transport-/ready-brukere på main** mellom gammel og ny base. Hele main-deltaet er #54: 9 filer, +599/−6. Kontrollert hele diffen og `git diff a6fa51a origin/main -G 'BridgeBase|BridgeTransport|ready' -- Sources Tests` (tomt resultat), samt eksisterende brukersteder.

Main endrer `Sources/CellBase/Identity/IdentityLinkRegistry.swift` til å klassifisere genesis fra et verifisert seal/record-par. Genesis skjules fra innmeldingslisten, men beholdes for `sameEntityLink` og vanlig nøkkelbevis. Både `Sources/CellApple/Cells/EntityAnchorCell.swift` og `Sources/CellVapor/Cells/EntityAnchorCell.swift` sender seal til `restore`. Mains åtte filer utenom workflowen — produksjon, tester og dokumentasjon — er **byte-identiske med origin/main** etter rebase.

Sammensetningen fra PR-en er bevart:

- `CellResolver.swift:2250,2301,2323`: dedikert, remote og multiplexet fysisk forbindelse komponerer `BridgeChannelTransport` før `BridgeBase`/logiske kanaler.
- `ScannerService.swift:599,605`: peer-profilens endpoint/rolle komponeres gjennom samme gate før BridgeBase-factory; gjensidig proof kreves før oppsett.
- `BridgeChannelTransport.swift:220`: innkommende `ready` avvises før vanlig dispatch. `BridgeBase.swift:1348,1369` og logisk mux-kanal (`BridgeMultiplexing.swift:928`) avviser også `ready`.
- `BridgeBase.swift:466`: lokal aktivering krever `channelSession.check()`. Den eksisterende interne mux-klientens tidlige retur for en uadressert `ready` aktiverer ingen kanal; den fysisk komponerte gaten avviser meldingen før dette punktet.

Alle 16 filer i Bridging-/transport-/Scanner-utvalget samt `CellResolver.swift` er byte-identiske med gammelt PR-head. Ingen ready-unntak eller ny kompatibilitetsomgåelse er innført. Komposisjonsbevis og brukersteder: `/private/tmp/cp53-rebase-evidence/composition-proof.json`, `final-bridge-composition.txt`, `final-ready-gates.txt`.

## Lokal bygg og fulltest

Vert: Apple Swift 6.4, Xcode 27.0 (27A266a), arm64 macOS. Følgende miljø ble brukt for alle tre kommandoer:

```sh
export SWIFTPM_MODULECACHE_OVERRIDE=/private/tmp/cp53-module-cache
export CLANG_MODULE_CACHE_PATH=/private/tmp/cp53-module-cache
swift build --disable-sandbox --disable-automatic-resolution --cache-path /private/tmp/bro-swift-cache --jobs 4
swift test --disable-sandbox --disable-automatic-resolution --cache-path /private/tmp/bro-swift-cache --jobs 4
CP53_MULTIPEER_TEST=1 swift test --disable-sandbox --disable-automatic-resolution --cache-path /private/tmp/bro-swift-cache --jobs 4 --filter ScannerMultipeerProcessTests/testTwoProcessesUseRealMultipeerInBothInvitationDirections
```

Bare SwiftPMs nestede sandbox er slått av; den ytre agentsandboxen er beholdt. Kilder, testutvalg og dependency-lock er ikke tilpasset for å få grønt.

Full `swift build`: **exit 0**, `Build complete! (12,94 sek)`.

Full lokal `swift test`: **exit 1**, siste «Executed …»-linje:

```text
Executed 1369 tests, with 12 tests skipped and 3 failures (3 unexpected) in 30.328 (30.403) seconds
```

De samme tre lokale Keychain-hostfeilene som dokumentert i R3:

- `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns`: CDSA-nøkkelgenerering feiler med `EPERM`, status 100001.
- `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyStillSigns`: samme feil.
- `AppleIdentityVaultKeyStorageTests.testScopedSecretDataStaysStableInUnsignedTestHost`: `unhandledError(status: -25291)`.

Alle øvrige kjørte tester består, inkludert `ScannerPeerAuthenticationTests` (12), `BridgeChannelLifetimeQuotaTests` (7), mains `EntityAnchorEnrollmentContractTests` (4) og `IdentityLinkGenesisClassificationTests` (2). Ingen test fjernet eller ny skip lagt til.

Logger: `/private/tmp/cp53-rebase-evidence/build.log` og `test.log`.

## Reell Multipeer i to prosesser

**KJØRT OG BESTÅTT, exit 0**, begge inviterretninger. Begge workerprosesser har 0 feil og completion-markør for faktisk autentisering, Lobby-description, attach og feed. Siste parent-linje:

```text
Executed 1 test, with 0 failures (0 unexpected) in 9.511 (9.512) seconds
```

Artefakter:

- A inviterer B: `/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/cp53-multipeer-24730BE4-62F7-43F6-9BFE-132A0110DD22`.
- B inviterer A: `/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/cp53-multipeer-5E07BE86-15CF-4A15-972E-D3BB0822906A`.

Hver mappe har `a.log`, `b.log`, offentlige syntetiske deskriptorer og `a.passed`/`b.passed`. Samlet logg: `/private/tmp/cp53-rebase-evidence/multipeer.log`; maskinlesbar kontroll: `multipeer-results.json`. Opt-in-testen er lokal; ordinær CI kjører ikke denne radioprøven.

## Push, CI og GitHub-konfliktstatus

Push fullført til samme gren med eksplisitt lease mot kjent gammelt head:

```sh
git push --force-with-lease=refs/heads/pdd/bro-kanal-auth:b4f66b4ece1692ea6ddb2429b252c8cac4f16562 origin HEAD:refs/heads/pdd/bro-kanal-auth
```

Alle fem workflowene startet **automatisk** etter push; ingen manuell dispatch/rerun. Fire test-/benchmark-workflower kjører på `pull_request`; Notify kjører på `pull_request_target`. Alle run-metadata peker på nytt head `101e5452ed7aecbbf947ed1205c3941ec24782a8`.

| Workflow | Resultat | Event | URL |
|---|---|---|---|
| Vapor identity vault Swift Linux | success | pull_request | [kjøring](https://github.com/Digipomps/CellProtocol/actions/runs/36373503255) |
| CellProtocol Swift Linux | success | pull_request | [kjøring](https://github.com/Digipomps/CellProtocol/actions/runs/36373503313) |
| CellProtocol macOS regression | success | pull_request | [kjøring](https://github.com/Digipomps/CellProtocol/actions/runs/36373503285) |
| Runtime capacity benchmark (macOS) | success | pull_request | [kjøring](https://github.com/Digipomps/CellProtocol/actions/runs/36373503315) |
| Notify PyCellProtocol | success | pull_request_target | [kjøring](https://github.com/Digipomps/CellProtocol/actions/runs/36373501744) |

Alle fem kjøringer er **success**. Fulgt med `gh run watch --exit-status --interval 30` under én 60-minutters deadline; alle watcher-exit=0. Vakten brukte 923.8 sekunder (ca. 15.4 minutter), innen fristen. Ingen rerun.

Siste «Executed …»-linje i macOS-steget **Test exact sources and pinned dependencies**:

```text
Executed 1398 tests, with 5 tests skipped and 0 failures (0 unexpected) in 41.865 (42.153) seconds
```

Alle tre navngitte lokale Keychain-feiltester er eksplisitt **passed** i CI (henholdsvis 0.080, 0.054 og 0.008 sekunder). CI har ingen kilde-/dependency-lock-endringer under kjøringen. CI og lokal fulltest har ulike testtotaler (1398 og 1369); begge eksakte sammendrag er rapportert separat. Årsaken til forskjellen i oppdaget testutvalg er ikke utredet i denne rebasen.

MacOS-checkout bruker GitHubs syntetiske PR-testcommit `110f45c840334fb47272adc34ce4c4098d1d425a`, med foreldre ny main og nytt head. Hentet refen og verifiserte at hele treet er **identisk med PR-head** (`24b0937492754eb4dbb31fe208b378f5722cd508`). Dette er GitHubs testref; PR-en er fortsatt åpen og ingen merge til main er utført.

TSAN: `BridgeDescriptionConcurrencyTests` tre ganger, hver 2 tester / 0 feil. Kontrollen mot sårbar downstream transport-pin besto. Dette er avgrenset TSAN-dekning, ikke dekning av alle peer-livsløp.

Linux-sammensetningen fra konflikten kjørte faktisk genesis-testene sammen med brotest-fixturene: `Executed 82 tests, with 0 failures (0 unexpected) in 2.681 (2.681) seconds`; `IdentityLinkGenesisClassificationTests` er eksplisitt passed.

Fullstendige logger og bevis: `/private/tmp/cp53-rebase-evidence/ci-macos.log`, `ci-linux.log`, `ci-final.json`, `ci-watch-exits.json`, `ci-merge-tree-proof.json` og `pr-final.json`.


GitHub-verifikasjon: `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`, `state=OPEN`, `mergedAt=null`; base/head samsvarer med SHA-ene over. PR-en er **ikke lenger CONFLICTING**. Lokal `git merge-base --is-ancestor origin/main HEAD` består, og `git merge-tree --write-tree --name-only HEAD origin/main` gir samme tre som HEAD: `24b0937492754eb4dbb31fe208b378f5722cd508`.

## Gjenstående grenser og arbeidstre

Den lokale fulltesten er ikke grønn på grunn av de tre navngitte Keychain-feilene; CI-resultatet rapporteres separat. Ingen påstand om to fysiske enheter, iOS/UWB, langtidslast, staging/prod eller faktisk utrulling.

Kodearbeidstreet er rent etter bygg/test/push. Hovedarbeidstreet `CellProtocol` på `pdd/tillitspakke-agentflaate` hadde mange eksisterende endringer og er ikke endret av oppgaven. `CellProtocolDocuments` på `codex/docs-cleanup-20260810` var allerede skittent; kun denne rapporten er skrevet der, uten docs-commit eller docs-push. Startstatus er lagret under `/private/tmp/cp53-rebase-evidence/`. Losen kan gå videre med review av PR-en; **ingen merge er utført**.

## Commit-kart

| Gammel commit | Rebaset commit |
|---|---|
| `89954f3` | `5f604ca` |
| `f15c71d` | `4bb22b2` |
| `39b263d` | `ad6527c` |
| `196b910` | `4e0a0b5` |
| `dacf7d6` | `7a3e221` |
| `1183305` | `03e31de` |
| `5232688` | `f868efc` |
| `f52df27` | `d0b86ac` |
| `229a15b` | `8ec392d` |
| `303636b` | `e45d20e` |
| `f1e1507` | `f8f6f31` |
| `2416f45` | `735bd97` |
| `616a3b2` | `e72b17b` |
| `8649e23` | `b861e88` |
| `4132c45` | `9c07bdc` |
| `283cc3f` | `be5e7ec` |
| `4b367ef` | `8b6c9dd` |
| `0fee023` | `4980dfc` |
| `9ec3918` | `b1dc01d` |
| `22d7919` | `5d946ad` |
| `9a03a72` | `fe8957e` |
| `0350364` | `5cc8d8e` |
| `b4f66b4` | `101e545` |

Fullstendige SHA-er og forfatter-/meldingskontroll: `/private/tmp/cp53-rebase-evidence/commit-map.json`. Range-diff: `range-diff.txt` i samme mappe.
