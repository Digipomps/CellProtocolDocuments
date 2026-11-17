Ledig foer: **46 GiB** av 926 GiB.

Maal: 110 GiB ledig. Diskvakten i `ci/run-tests.sh` krever at det som blir igjen
etter en 10 GiB reserve er minst 40 GiB og minst 5 % — altsaa ~57 GiB ledig for aa starte.

## Hva som ble slettet

```text
slettet  0B  /tmp/wp-lev-mint-clang-cache  (min egen skrivebordsrest)
slettet  59M  /tmp/wp-lev-mint-swift-cache  (min egen skrivebordsrest)
slettet  117M  /tmp/wp-r4d-swift-cache  (min egen skrivebordsrest)
slettet  133M  /tmp/haven-swiftpm-bounded  (min egen skrivebordsrest)
slettet  4.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-butler-smoke-20260902/test-results  (Playwright-utdata, lages paa nytt)
slettet  4.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-chatlog-20260902/test-results  (Playwright-utdata, lages paa nytt)
slettet  4.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-queue-20260903/test-results  (Playwright-utdata, lages paa nytt)
slettet  4.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-butler-signal-20260908/test-results  (Playwright-utdata, lages paa nytt)
slettet  4.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-know-off/test-results  (Playwright-utdata, lages paa nytt)
slettet  248K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-tabs/test-results  (Playwright-utdata, lages paa nytt)
slettet  4.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-list-tree-20260905/test-results  (Playwright-utdata, lages paa nytt)
slettet  3.9M  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-kallimachos-fix/test-results  (Playwright-utdata, lages paa nytt)
slettet  4.8M  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-mix-tidy-20260904/test-results  (Playwright-utdata, lages paa nytt)
slettet  182M  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/test-results  (Playwright-utdata, lages paa nytt)
slettet  3.2M  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/test-results  (Playwright-utdata, lages paa nytt)
slettet  1.5G  /Users/kjetil/Build/Digipomps/HAVEN/DiMyMicropayments/.build  (byggkatalog, lages paa nytt av swift build)
slettet  0B  /Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-formaalsregister-wp0/.build  (byggkatalog, lages paa nytt av swift build)
slettet  0B  /Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-bridge-provenance/.build  (byggkatalog, lages paa nytt av swift build)
slettet  11G  /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/.build  (byggkatalog, lages paa nytt av swift build)
slettet  2.6G  /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata/.build  (byggkatalog, lages paa nytt av swift build)
slettet  6.0G  /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/.build  (byggkatalog, lages paa nytt av swift build)
slettet  3.1G  /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/.build  (byggkatalog, lages paa nytt av swift build)
slettet  8.0K  /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.build  (byggkatalog, lages paa nytt av swift build)
slettet  1.3G  /Users/kjetil/Build/Digipomps/HAVEN/DiMyMint/_wt-lev-mint-20260922/.build  (byggkatalog, lages paa nytt av swift build)
slettet  96K  /Users/kjetil/Library/Developer/Xcode/DerivedData/CompilationCache.noindex  (Xcode DerivedData, ubrukt i over sju dager)
slettet  410M  /Users/kjetil/Library/Caches/org.swift.swiftpm  (SwiftPM-cache, hentes paa nytt)
```

Ledig etter: **67 GiB** (var 46 GiB).

Rørt ikke: kildekode, `.git`, bevis, `_losen-queue`, dokumenter, `node_modules` (Playwright trenger den, og `npm ci` krever nett), og byggkatalogen i `_wt-skjellettelementer-web-20260919` som CI-filteret skal bruke.
