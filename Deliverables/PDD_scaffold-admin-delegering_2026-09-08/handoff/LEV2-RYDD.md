STATUS: DELVIS — 42 GiB ledig; diskvakten trenger ~57

# Opprydding — byggrester og cacher

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-rydd2.sh` 2026-09-23T13:20:19Z. Bevis: `evidence/rydd/`.

Ledig foer: **29 GiB** av 926 GiB.

Maal: 110 GiB ledig. Diskvakten i `ci/run-tests.sh` krever at det som blir igjen
etter en 10 GiB reserve er minst 40 GiB og minst 5 % — altsaa ~57 GiB ledig for aa starte.

## Hva som ble slettet

```text
slettet  3.0G  /Users/kjetil/Build/Digipomps/HAVEN/_worktrees/HavenAgentD-agentmenu-window-20260923/.build  (byggkatalog, lages paa nytt av swift build)
slettet  5.8G  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-admin-levering-20260923/.build  (byggkatalog, lages paa nytt av swift build)
slettet  6.7G  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/.build  (byggkatalog, lages paa nytt av swift build)
slettet  336M  /Users/kjetil/Library/Caches/org.swift.swiftpm  (SwiftPM-cache, hentes paa nytt)
```

Ledig etter: **42 GiB** (var 29 GiB).

Rørt ikke: kildekode, `.git`, bevis, `_losen-queue`, dokumenter, `node_modules` (Playwright trenger den, og `npm ci` krever nett), og byggkatalogen i `_wt-admin-prod-20260923` som CI-filteret skal bruke.

**Ikke nok ennaa.** Neste kandidater, i rekkefoelge: byggkatalogen i den aktive worktreen (6,8 GiB, men da maa CI-filteret bygge alt paa nytt), `node_modules` (krever `npm ci` og nett), og DerivedData yngre enn sju dager.
