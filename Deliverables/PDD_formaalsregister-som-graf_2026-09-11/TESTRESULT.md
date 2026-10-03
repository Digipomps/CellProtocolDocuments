# TESTRESULT — WP0: baseline for formålsregister som graf

Dato: 2026-09-15. **WP0: blocked.** Bygget stoppet ved avhengighetshenting under nettforbudet. Testbaseline er ikke målt. G2 er godkjent ifølge oppdraget; dette resultatet gjelder bare WP0.

## build

**test.build: blocked** — kommandoen feilet før produktkode og tester kunne bygges.

- Commit-SHA: `c430a24c0d93d2cec9984149c4fb7546c6341bd3` (lokal `origin/main`; ikke oppdatert over nett).
- Worktree: `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-formaalsregister-wp0`.
- Gren: `pdd/formaalsregister-som-graf`.
- Opprettelse: `_worktrees/agent-worktree.sh CellProtocol formaalsregister-wp0 --branch pdd/formaalsregister-som-graf --from origin/main`.

Kontroll av commit:

```text
git -C /Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-formaalsregister-wp0 log -1 --format='%H %s'
c430a24c0d93d2cec9984149c4fb7546c6341bd3 Run bounded runtime capacity benchmarks on macOS CI (#36)
```

Kontroll av rent utsjekk:

```text
git -C /Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-formaalsregister-wp0 status --short
```

Utdata var tom; exit 0. Samme kommando hadde tom utdata etter byggeforsøket. Maskinlesbart bevis: [checkout.json](evidence/wp0/checkout.json).

Byggkommando, kjørt i worktreet uten arkitekturprefiks:

```sh
swift build --disable-sandbox --build-tests
```

For å håndheve nettforbudet fikk underprosessen `GIT_ALLOW_PROTOCOL=file` og `GIT_TERMINAL_PROMPT=0`. Ingen avhengigheter ble hentet over nett. SwiftPM skrev «Fetching», men Git avviste HTTPS lokalt.

| Måling | Resultat |
|---|---|
| Start (UTC) | 2026-09-15T09:30:03.401732+00:00 |
| Slutt (UTC) | 2026-09-15T09:30:05.623469+00:00 |
| Veggklokketid | 2,220 s |
| Exit-kode for Swift | 1 |
| Advarsler | 4 utlinjer med `warning:` |

Advarslene gjelder utilgjengelig konfigurasjons-, sikkerhets- og avhengighetscache, samt skriving av manifest til skrivebeskyttet cachedatabase.

**Første feil:** [evidence/wp0/build.log](evidence/wp0/build.log), linje 6:

```text
error: Failed to clone repository https://github.com/Digipomps/FileUtils-c.git:
```

Årsaken står i samme logg: `fatal: transport 'https' not allowed`.
Relevant deklarasjon er `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-formaalsregister-wp0/Package.swift:40`. Selve feildiagnosen oppgir ingen kildefil eller linje; kompilatorfeilens sti:linje er derfor **ukjent / ikke oppgitt**. Deklarasjonsstedet er ikke en påvist kodefeil.

Fullstendig kombinert stdout/stderr: [build.log](evidence/wp0/build.log). Tidsmåling og exit-kode: [build.json](evidence/wp0/build.json). Loggen er kontrollert og inneholder ingen hemmeligheter.

## regression

**test.regression: blocked** — ikke kjørt, i henhold til oppdragets stoppregel ved byggfeil.
Commit-SHA: `c430a24c0d93d2cec9984149c4fb7546c6341bd3`; samme worktree som over.

Søk etter testbunt:

```sh
ls .build/arm64-apple-macosx/debug/*.xctest
```

Ingen treff; zsh returnerte `no matches found` og exit 1. Faktisk `<Pkg>PackageTests.xctest`-sti er **ukjent**. Foreskrevet testkommando, **ikke kjørt**:

```sh
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/<Pkg>PackageTests.xctest
```

| Måling | Resultat |
|---|---|
| Utførte tester | 0 — ingen testprosess startet |
| Totalt antall tester i suiten | ukjent |
| Røde tester, antall og navn | ukjent |
| Stabile røde etter isolert omkjøring | ukjent; ingen omkjøring utført |
| Flaky tester, antall og navn | ukjent |
| Tester som henger > 15 minutter | ukjent; ingen tester startet |
| Testvarighet og exit-kode | ukjent; ikke kjørt |

Ingen XCTest-logg finnes fordi testen ikke startet. [regression-not-run.log](evidence/wp0/regression-not-run.log) dokumenterer dette og utdata fra buntsøket; filen er ikke en testkjøringslogg. Isolert `-XCTest <Suite/test>` og 15-minuttersgrensen kom ikke til anvendelse.

## Avgrensning og ukjent

WP0 er blokkert på byggforutsetningene i denne offline-kjøringen. Om bygget og testene lykkes med tilgjengelige avhengigheter, er **ukjent**. Om lokal `origin/main` er lik serverens nåværende `main`, er **ukjent**, siden nett ikke var tillatt.

Ingen produktkode er endret, og ingen commit eller push er utført. Etter opprettelsen av worktreet er bare den nye worktreen og denne PDD-mappen brukt som skriveområder. WP1 og senere arbeid er ikke startet.
