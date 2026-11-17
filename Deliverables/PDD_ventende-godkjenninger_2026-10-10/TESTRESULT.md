# TESTRESULT — ventende godkjenninger (2026-10-10, Claude)

## url-keypath
- CellProtocol #66, commit 84afbf1, i scratch-klonen: `swift test --filter SkeletonButtonResolutionTests` → «Executed 6 tests, with 0 failures» (4 nye, 2 eksisterende). Rødt først: de nye testene kompilerer ikke på main, fordi feltet mangler der.
- CellScaffold web (`Public/js/skeleton-runtime.js`, #315), Chromium headless 1193, fire rader med `urlKeypath: "whereURL"`:
  - origin/main: 0 radlenker. Alle fire ble knapper.
  - grenen: lenker for `https://developer.apple.com/account` og `https://github.com/Digipomps/CellScaffold/pull/313`. `javascript:alert(1)` ble knapp, ikke lenke. Den relative stien ble en lenke på samme opphav (`https://haven.example/Users/...`), som er eksisterende oppførsel for relative URL-er. Lesemodellen setter derfor bare `whereURL` for https.
  - Uten `urlKeypath` leses ikke radens `url` på web (knappens faste url beholdes).
- `playwright/skeleton-button-url-keypath.spec.js`: **ikke kjørt** (`@playwright/test` er ikke installert på Mac-en).
- Binding: **blocked**. Trenger CellProtocol-tag med feltet.

## pointer / stale (CellScaffold #315)
- `WorkItemOverviewPointerTests` (5 tester): **ikke kjørt lokalt**. CS-bygget er ikke kjørt fordi disken var under fullport-gulvet (88–92 GiB ledig, gulv ~110). Syntakssjekk `xcrun swiftc -parse` OK på de tre endrede Swift-filene, og `node --check` OK på runtime. CI på #315 venter.
- Codex' eksisterende tester er uendret.

## coverage / button-roundtrip (HAVEN-Deploy)
- `python3 -m unittest tests/test_godkjenninger.py` → «Ran 7 tests … OK».
- Tørrkjøring mot ekte `hd status --json` 20:13Z: 17 kort, det vil si 5 trådforespørsler, 11 HD-poster og 1 samlekort for 68 avviste pakker. HD-0169 og HD-0207 dekkes av trådforespørslene. Alle 81 i forkastet-banen er representert.
- Skriving til staging: **blocked**. Broen svarer `400 unavailable` (målt 18:13Z).

## build / regression
- CellProtocol og CellScaffold: CI startet på begge draft-PR-ene. Resultatet er ikke lest ennå.
