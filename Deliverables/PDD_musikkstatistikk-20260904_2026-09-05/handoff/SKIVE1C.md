STATUS: LEVERT — PR https://github.com/Digipomps/CellScaffold/pull/263, commit 9e5113d1b8fc26cfdf6b46729fd690cb1a6b0e16, CI grønn (https://github.com/Digipomps/CellScaffold/actions/runs/36110978263)

# Skive 1c — Statistikk i Butterpop Studio

PR: https://github.com/Digipomps/CellScaffold/pull/263
Commit: `9e5113d1b8fc26cfdf6b46729fd690cb1a6b0e16`
Gren: `pdd/musikkstatistikk-fanen`
Base: `origin/main`, `e6277af1` (skive 1a/1b er merget).
Worktree: `CellScaffold/_wt-musikkstat-fanen-20260925`.
CI: https://github.com/Digipomps/CellScaffold/actions/runs/36110978263

Ingen merge eller deploy. Losen eier merge og utrulling.

## Leveranse

- Femte fane, mellom Publiser og Medlemmer. Synlighet krever autentisert
  sesjon og `workspace.read` fra workspace-projeksjonen. API-et beholder sin
  eksisterende autorisasjon. Anonyme og innloggede lyttere får ingen fane.
- Én rad per låt fra `GET /butterpop/api/workspace/statistics`, fire separate
  tellere og tidligste `since`. Datoer vises som UTC kalenderdatoer.
- «Alle avspillinger» og «usikret» står sammen; forklaring, slutt-undertekst,
  akselinje og tom samtykkeboks følger godkjent mock v2.
- API-projeksjonen får `downloadEnabled` fra eksisterende låtpolicy og valgfri
  `publishedAt` (UTC ISO 8601). Dette var nødvendig for å hente samtlige
  opplysninger i fanen fra ett endepunkt. Ingen nye lagrede tellerfelt.
  Ukjent publiseringsdato utelates; deaktivert nedlasting gis bare undertekst
  når API-et faktisk sier false.
- Tom liste: «Ingen publiserte låter ennå.» Feil eller ugyldige verdier:
  «Statistikken kunne ikke hentes nå.» Ingen tall eller dato i disse tilstandene.
  Gamle tall fjernes før ny henting. Forsinkede svar fra eldre henting ignoreres.
- Ingen endring i avspilling, tellerinkrementer, samtykke eller historikk.

Endrede kodefiler: `Public/js/butterpop-studio.js`,
`Public/css/butterpop-studio.css`, `Resources/Views/butterpop_studio.leaf`,
`Sources/App/Cells/MusicPublishing/MusicPublishingCells.swift`,
`Sources/App/Cells/MusicPublishing/MusicUsageStatistics.swift`,
`Tests/AppTests/MusicUsageStatisticsTests.swift`,
`playwright/butterpop-statistics.spec.js`, `package.json`,
`.github/workflows/admin-scaffold-image.yml` og
`Documentation/ButterpopStudio_Product.md`.

## Verifikasjon

Lokal Swift via repoets pålagte wrapper:

```sh
scripts/run_swift_bounded.sh test --disable-sandbox --filter 'MusicUsageStatisticsTests|MusicPublishingMVPRoutesTests|MusicPublishingConfigurationFactoryTests|ButterpopPilotReadinessTests'
```

**17 tester, 0 feil**, exit 0. MusicUsageStatistics 10, MusicPublishingMVPRoutes 1,
MusicPublishingConfigurationFactory 4, ButterpopPilotReadiness 2. Bygget brukte
den eksisterende lease-beskyttede cachen og to jobber. Kapasitetsvakten passerte:
64,1 GiB ledig, 54,1 GiB (5 %) etter reserve. Logg:
`/private/tmp/musikkstat-1c-swift.log`. `Package.resolved` er uendret.

`HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, JS-syntaks og
`git diff --check` passerte. Explore-audit av MusicPublishing: 94 komplette
kontrakter, 94 handlers, 0 feil/advarsler.

Ny Playwright-suite har 14 tester for eier/lesemedlem, anonym/lytter/medlem uten
leserett, riktige kolonner, tidligste dato, «usikret», tom tilstand, HTTP-feil,
ugyldige svar, fjerning av gamle tall ved ny henting, nedlasting på/av, manglende
publiseringsdato, HTML-escaping og mobilbredde. Kjører med mocket API og
produksjonsmalen, JS og CSS fra arbeidstreet, uten testspesifikke endringer i disse filene. Eget CI-artefakt beholder
desktop- og mobilbilder også når kjøringen lykkes.

Lokal standard Playwright-kjøring av statistikk-, kø- og miksryddesuitene ble
stoppet før første side lastet: `bootstrap_check_in ... MachPortRendezvousServer:
Permission denied (1100)`. Dette er en macOS-sandboxblokkering, ikke beståtte
eller feilede produktasserts. Logg: `/private/tmp/musikkstat-1c-playwright.log`.
Playwright-MCP krevde godkjenning, som øktens policy ikke tillater.

Alternativ lokal kontroll gjennom CUA/Chrome brukte
`http://127.0.0.1:8941/butterpop` med samme mockfunksjon fra den nye testsuiten
og de faktiske filene fra worktreet. Følgende ble synlig kontrollert:
fem faner, tre rader med korrekte kolonner, datoene, teksten og samtykkeboksen;
tomtilstand; HTTP 500 uten tall/dato; skjult fane for anonym og innlogget lytter;
nedlasting på uten «av»-tekst; ukjent publiseringsdato uten oppdiktet dato.
Mobil 390×844: document.scrollWidth 390, fem kolonner à 72 px og en separat
tabellrulleregion på 362 px for en 650 px bred tabell. Viewport-overstyringen
ble tilbakestilt. Dette erstatter ikke CI-kjøringen av Playwright-testene.

## Bilde og avvik

Godkjent referanse: `images/statistikk-skive1-v2.png`, kilde `mock-v2.html`.
**Faktisk Playwright-bilde:** [statistikk-faktisk-1c.png](../images/statistikk-faktisk-1c.png).
Bildet er lastet ned fra CI-artefaktet
`butterpop-statistics-b3d4060c50c97bbeae903eec675b7ad5470e391c`, og viser de
samme tre syntetiske låtene/tallene som referansen. Det er ikke produksjonsstatistikk.

Visuelt kontrollert: fem faner i riktig rekkefølge, aktiv svart Statistikk-fane,
papirbakgrunn, titler, tidligste dato, «usikret», ordrett forklaring, separate
kolonner og skillelinjer, radundertekster, akselinje og tom samtykkeboks.

Avvik fra referansen:
- Referansen er 2360×1358 ved dobbel pikseltetthet; CI-bildet er 1180×580 ved
  enkel tetthet. CI-bildet er beskåret til selve workspace-panelet og har ikke
  mockrammens ekstra luft over og under. Ingen bilder er skalert eller retusjert.
- Linux/Chromium gir litt annen skriftrasterisering og linjebryting enn
  referansen. Ingen pixel-for-pixel-likhet påstås.
- Den virkelige siden har også eksisterende Butterpop Studio-overskrift og
  øvrig sideinnhold utenfor dette utsnittet.
- Mobil er en tilleggskontroll uten godkjent mobilreferanse: fem kompakte
  faner og vannrett tabellrulling. Linux-bildet ved 390 px viser svært trang
  «Medlemmer»-etikett mot høyre kant; siste bokstav ser avklipt ut. Hele navnet
  finnes i tilgjengelighetstreet, og faneknappen virker. Mobiltesten bekrefter
  sidens bredde, fem kolonner og tabellrulling, ikke at hver etikett har fri luft.
  Dette er en gjenstående visuell begrensning ved smal bredde.

## Endelig CI og overlevering

CI for **siste commit** `9e5113d1b8fc26cfdf6b46729fd690cb1a6b0e16` er
`completed/success`: https://github.com/Digipomps/CellScaffold/actions/runs/36110978263.

- Alle mål bygget: success, 08:06:52–08:34:48 UTC.
- Swift-gaten: success, **alle 30 bolker grønne**. MusicUsageStatisticsTests
  bestod også i Linux-CI.
- Nettlesergaten: success. Den nye statistikk-suiten: **14 passed (9.6s)**,
  ferdig 08:49:43 UTC.
- Thursday demo P0 og document live collaboration: begge success. Eksisterende
  Butterpop kø- og miksryddetester er med i Thursday-gaten.
- Skjermbilder lastet opp: success. Publisering av images ble hoppet over for
  denne PR-kjøringen; ingen utrulling er gjort.

Native `gh run watch --exit-status` avsluttet med exit 0 kl. **08:56:26 UTC**,
før den opprinnelige fristen 08:59:03 UTC (maks 60 minutter). Terminalkontroll
bekreftet samme head-SHA på CI og PR, `OPEN`, `MERGEABLE`, `CLEAN` og
`mergedAt: null`. **Ikke merget. Losen eier merge og utrulling.**

Logger: `/private/tmp/musikkstat-1c-ci-v2-watch.log`,
`/private/tmp/musikkstat-1c-ci-v2-result.json`,
`/private/tmp/musikkstat-1c-ci-complete.log` og
`/private/tmp/musikkstat-1c-ci-test-evidence.txt`.
CI-artefakter er også lastet ned under
`/private/tmp/musikkstat-1c-ci-artifacts-36110978263`.

Første implementasjonscommit er `8ad56ed3`, med pålagt commitmelding,
PDD-referanse, Co-Authored-By og Claude-Session. Oppfølging `9e5113d1` endrer
bare versjonsparametrene i HTML-ens CSS-/JS-lenker for å unngå gammel nettlesercache,
og har de samme referanse-/attribusjonslinjene. Den eldre PR-kjøringen
36110458313 ble avbrutt for å slippe fram siste commit og er ikke brukt som
CI-bevis. Fristen ble ikke utvidet.

Kodeworktreet er rent. Rapport og bilde ligger separat, lokalt i
CellProtocolDocuments. Oppgavemappen var allerede untracked; øvrige lokale
endringer i begge hovedrepoene er urørt og er ikke med i kode-PR-en.
