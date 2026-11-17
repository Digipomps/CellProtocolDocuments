# TESTRESULT — spillverksted

## motor

T-D1, 2026-10-09. Spørsmålet: skriver en språkmodell riktig spillkode for KAPLAY og Phaser uten å slå opp dokumentasjon?

**Oppsett.** To Claude-agenter fikk samme fem spillbestillinger, én agent per motor. De fikk ikke lese dokumentasjon, pakker eller nettet, og de fikk ikke kjøre koden. Motorer: KAPLAY 3001.0.19 og Phaser 4.2.1, lastet som vanlige skript. Hvert spill ble kjørt i Chromium i 1,5 sekunder, så fikk det piltaster, mellomrom og seks klikk (`engine/measure.js`, rådata i `engine/result.json`, bilder i `engine/sheet.png`).

| Spill | KAPLAY linjer | KAPLAY resultat | Phaser linjer | Phaser resultat |
|---|---|---|---|---|
| 1 Hoppespill | 90 | kjører, ingen feil | 108 | kjører, ingen feil |
| 2 Fangespill | 66 | kjører, ingen feil | 110 | kjører, ingen feil |
| 3 Labyrint | 57 | kjører, ingen feil | 96 | kjører, ingen feil |
| 4 Romskip | 72 | kjører; logikkfeil: skudd i lufta gir poeng etter «Game over» | 117 | kjører, ingen feil |
| 5 Klikkspill | 57 | kjører, ingen feil | 84 | kjører, ingen feil |
| **Sum** | **342** | 5 av 5 starter, 1 logikkfeil | **515** | 5 av 5 starter |

**Funn.**
- Begge motorene ga kjørbar kode på første forsøk i alle ti spillene. Risikoen vi antok for Phaser 4 (at modellen skriver Phaser 3-kode som ikke virker) slo ikke til for disse fem spillene.
- KAPLAY-koden er en tredjedel kortere (342 mot 515 linjer) og har færre begreper å forklare. Phaser trenger scener med preload/create/update, teksturer generert fra grafikk og fysikkgrupper.
- Den ene feilen (KAPLAY romskip) er en logikkfeil, ikke en API-feil. Slike feil fanger ikke en automatisk kjøring; de krever at noen spiller.

**Konklusjon.** Målingen støtter KAPLAY som første motor på grunn av lesbarhet, ikke fordi Phaser feiler. Phaser er et trygt neste trinn bak adapteren.

**Begrensninger.** Én modell (Claude), ett forsøk per spill, fem små spill. «Kjører» betyr ingen feil og at bildet endrer seg; spillbarhet er vurdert ved å se på skjermbildene, ikke ved at Sverre har spilt. Lesbarhet for et barn er en vurdering, ikke målt.

## forhandsvisning

WP-B2/WP-D1, `Visualization` `gamePreview` (`purpose://candidate.workbench-assistant.preview-before-change`, `purpose://candidate.game-workshop.engine.sandbox-isolation`). CellScaffold `cb91f0b`, Chromium i skycontaineren, 2026-10-09.

```
$ npx playwright test playwright/game-preview-visualization.spec.js
Running 6 tests using 1 worker
  ✓  1 playwright/game-preview-visualization.spec.js:77:3 › gamePreview visualization › runs the game in a sandbox without same-origin and shows that it runs (535ms)
  ✓  2 playwright/game-preview-visualization.spec.js:86:3 › gamePreview visualization › a crash is shown and sent once to actionKeypath (700ms)
  ✓  3 playwright/game-preview-visualization.spec.js:96:3 › gamePreview visualization › the game cannot read the session, cookies or storage (526ms)
  ✓  4 playwright/game-preview-visualization.spec.js:106:3 › gamePreview visualization › a URL outside the sandbox route is refused (418ms)
  ✓  5 playwright/game-preview-visualization.spec.js:115:3 › gamePreview visualization › a data refresh with the same URL keeps the running game (745ms)
  ✓  6 playwright/game-preview-visualization.spec.js:126:3 › gamePreview visualization › no preview says so instead of drawing nothing (446ms)
  6 passed (4.6s)
```

Testen «the game cannot read the session…» viser at sandkassen holder i rendreren: `self.origin` er `"null"`, og cookie og localStorage er blokkert. Sandkasseruten på serveren (WP-D2, T-D2) er ikke laget ennå; ruten i testen er en Playwright-stub med samme CSP.

## bibliotek-validator

T-C1, `purpose://candidate.tool-library.purpose-keyed-entries`.

```
$ node Tools/GameToolLibrary/library.mjs validate
gyldig
```

## utledet

T-C3, `purpose://candidate.tool-library.derived-from-sources`. Biblioteket bygges fra `library-source.json` og KAPLAYs `doc.d.ts`; en funksjon som fjernes fra motoren, fjerner oppføringen.

```
$ node --test Tools/GameToolLibrary/library.test.mjs
ok 1 - T-C3: the committed library is exactly what the sources build
ok 2 - T-C3: a function removed from the engine removes its entry
ok 3 - API summaries come from the engine's own documentation
ok 4 - T-C1: the committed library is valid
ok 5 - T-C1: entries without purpose, license or source are refused
# tests 5
# pass 5
# fail 0
```

## kaplay-vendret

```
$ sha256sum Public/vendor/kaplay/3001.0.19/kaplay.js
88a946eafc4161f83505449d830b87c7bc15822bb0dae8ce03b2437506ef4a4b  Public/vendor/kaplay/3001.0.19/kaplay.js
```

## porthole-grunnlag

WP-0b, målt ved å lese koden 2026-10-09: `Public/js/skeleton-runtime.js` hadde ingen iframe, og en ukjent `Visualization`-type viste «Visualization kind '…' is not supported yet.». Derfor ble `gamePreview` laget (beslutning 1 i G2).

## versjoner

WP-E2: test skrevet, ikke kjørt. Kommando: `HAVEN_BUILD_MIN_FREE_PERCENT=10 CELLPROTOCOL_PUBLISHED_API=1 HAVEN_SWIFTPM_CACHE_KEY=spillverksted-r1 scripts/run_swift_bounded.sh test --filter GameProjectCellTests`.

```text
Build capacity: 92.4 GiB free (9%); reserving 10 GiB leaves 82.4 GiB (8%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 10%.
```

## sandkasse

Siste kjøring: 14 Playwright-tester passerte på Chromium lokalt (8 `game-sandbox.spec.js`, 6 `game-preview-visualization.spec.js`). HTML-malen og CSP-strengen er lest fra Swift-rutens ressurser/kilde; HTTP-ruten og session-middleware er ikke kjørt. Kommando: `NODE_PATH="$PWD/.game-test-tools/node_modules" .game-test-tools/node_modules/.bin/playwright test playwright/game-sandbox.spec.js playwright/game-preview-visualization.spec.js`.

```text
14 passed (9.6s)
```

Swift-hodetesten er ikke kjørt (kapasitetsgrensen).

## oppslag

WP-C2-kode og to Swift-enhetstester er skrevet. Den uavhengige tjueønskers-fiksturen fantes ikke i PDD-mappen ved inventaret, så T-C2-treffrate med/uten tekstsøk er **ikke målt**. De fem eksisterende bibliotekvalidator-/generator-testene passerte på Node; dette er ikke Swift-oppslagstesten.

## runde1-sluttkontroll

Kildetre: `tmp/codex-spillverksted-r1`, gren `codex/spillverksted-runde1`. Råbevis: `tmp/codex-spillverksted-r1/Documentation/Spillverksted/evidence/runde1/`.

- `playwright.log`: 14 tester passerte (8 nye sandkassemal-/CSP-tester + 6 eksisterende gamePreview-tester). Ingen Swift-server startet.
- `library-node.log`: 5 eksisterende Node-bibliotektester passerte. Ikke en erstatning for T-C2.
- `syntax.json`: exit 0 for Swift-parse av nye kilder og tester. Ingen typesjekking.
- `static-checks.json`: bundle-kopi byte-lik original, ni nye Swift-testmetoder, ingen testsuite uten CI-filter/unntak.
- `explore-audit.json`: seks statisk gjenkjente handleroperasjoner, seks komplette kontrakter, null errors/warnings. Dynamiske nøkler/effekter ikke runtime-verifisert. Maskinrot normalisert til punktum i audit-artefaktene.
- `value-literals.log`: grønn literalkontroll. Package.resolved har ingen endring.

Siste Swift-forsøk: `HAVEN_BUILD_MIN_FREE_PERCENT=10 CELLPROTOCOL_PUBLISHED_API=1 HAVEN_SWIFTPM_CACHE_KEY=spillverksted-r1 scripts/run_swift_bounded.sh test --filter "GameProjectCellTests|GameSandboxTests|GameToolLibraryCellTests"`, exit 75. **Ingen av de ni Swift-testmetodene er kjørt.**

```text
Build capacity: 90.3 GiB free (9%); reserving 10 GiB leaves 80.3 GiB (8%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 10%.
```

T-E1-inspeksjon, T-C2-måling, typer/API, lagring og levende autentisert sandkasserute er ikke bevist. Første runde er ikke grønn. Runde 2 er ikke startet.

### GitHub Actions etter PR-opprettelse

PR https://github.com/Digipomps/CellScaffold/pull/312, head `12d5be6efa3dd480331eddfdb617476560bd0d07`, utkast og ikke merget. [Actions-kjøring 37991437821](https://github.com/Digipomps/CellScaffold/actions/runs/37991437821) feilet i Initialize containers, **før checkout, bygg og tester**. Råloggens feil:

```text
Focused control-plane gates	Initialize containers	2026-10-09T21:07:07.4966567Z Error response from daemon: toomanyrequests: You have reached your unauthenticated pull rate limit. https://www.docker.com/increase-rate-limit
Focused control-plane gates	Initialize containers	2026-10-09T21:07:15.8983121Z Error response from daemon: toomanyrequests: You have reached your unauthenticated pull rate limit. https://www.docker.com/increase-rate-limit
Focused control-plane gates	Initialize containers	2026-10-09T21:07:25.7789150Z Error response from daemon: toomanyrequests: You have reached your unauthenticated pull rate limit. https://www.docker.com/increase-rate-limit
Focused control-plane gates	Initialize containers	2026-10-09T21:07:25.7874189Z ##[error]Docker pull failed with exit code 1
```

Dette er containeroppstartens nedlastingsgrense, ikke testfeil i spillverkstedskoden. Bygg og test er fremdeles ikke bevist. Ingen manuell nykjøring foretatt. package-release-policy-kontrollen passerte.

## runde1-ci

CI on PR #312 (https://github.com/Digipomps/CellScaffold/pull/312), head acad07d, 2026-10-13. Job "Focused control-plane gates" in run 38476583245 is green: 35 of 35 test blocks passed, and the Swift build of every target succeeded. This is the first Swift build of round 1. Codex could not build locally because of the capacity gate.

Fixes needed before it compiled and passed:
- `try await` inside a ternary does not compile. It is now an if/else.
- `registerSet` takes a non-throwing handler, so `create` is wrapped in do/catch.
- `FlowElement` content is `FlowElementValueType`, so the ack goes in as `.object(ack)`.
- Test: a foreign write is refused by the authorization layer throwing before the handler runs. The test accepts either refusal and checks that the pending proposal survives.
- CI: the build step now repeats compiler errors after `KOMPILERINGSFEIL:` at the tail of the log.

### oppslag

T-C2 (fixture `Tools/GameToolLibrary/fixtures/t-c2-wishes.v1.json`, 20 child wishes), from the CI log:

```
T-C2 hit rate: purpose+text 20/20, text only 15/20
```

The five misses on text alone:
- «Fienden skal gå fram og tilbake hele tiden»
- «Spillet skal bli raskere etter ti sekunder»
- «Når jeg dør skal det komme en skjerm der jeg kan prøve igjen»
- «Det skal si pling når jeg tar en mynt»
- «Jeg vil at helten skal se ut som en ordentlig figur, ikke en firkant»

### versjoner og sandkasse

The CI log shows these tests passing:
- GameProjectCellTests (4/4): ten changes plus a revert give 11 versions and survive encode/decode; a pending proposal can be discarded; the 200 kB limit and an unknown version are refused; a project create links ProjectPortfolio and two WorkItems; the sandbox refuses a foreign or forged requester.
- GameSandboxTests (3/3): CSP and security headers, no Set-Cookie, a generic 404 when unauthenticated, and the `</script>` boundary.
- GameToolLibraryCellTests (3/3).

## auth

Runde 2: B4 implementert og Swift-tester skrevet, men ikke kjørt ennå. `ci/check-value-literals.sh` exit 0. Kapasitetsport med repoets 10 %-krav: exit 75; 101,2 GiB ledig, reserve 10 GiB, projisert 91,2 GiB / 9 %. Logg i CellScaffold-worktree: `Documentation/Spillverksted/runde2-evidence/capacity.log`. Ingen grønn Swift-påstand.
