STATUS: LEVERT — PR https://github.com/Digipomps/CellScaffold/pull/262, commit 9950a6dc27ad327a82286715b58ea62ca73c8c86, CI grønn (actions/runs/36079253838); lokalt 38 tester, 0 feil (Losen skrev denne linjen 2026-09-25T01:35:28Z etter CI; Codex' rapport under)

# Skive 1a + 1b — Butterpop, 2026-09-25

PR: https://github.com/Digipomps/CellScaffold/pull/262
Gren: `pdd/musikkstatistikk-skive1`
Commit: `42d266150b690da1f5ef4b1e5349d4365271f328`
Base: `origin/main`, `4db0b1d6`.
Worktree: `CellScaffold/_wt-musikkstat-20260925`.
Ingen merge eller deploy utført. Losen eier merge og utrulling etter grønn CI.

## Leveranse og cellevalg

`MusicLibraryCell` eier allerede den publiserte katalogen og er persistent.
Den får `usageByTrackID`, med nøyaktig fem Codable-felt per låt:
`starts`, `previews`, `completions`, `downloads`, `since`.
Dermed behøves ingen ny celle, konsument, runtime-identitet eller gullkornendring.
Oppfylte kodekontrakter knytter seg til formålene `anonym-telles-uten-spor`,
`anonym-gjennomspilling-uten-pii`, `to-tall-blandes-aldri`,
`artisten-ser-bare-fordelinger` og `nedlasting-er-overfoering`.

Nye låter får tellere ved publisering. Eldre publiserte/unlisted låter migreres
ved lasting, og migreringen persisteres etter eiergjenoppretting før nye
intersepter registreres. `since` er uforanderlig gjennom hendelser og reload.
Inkrement og lagring serialiseres. Lagringen bruker eksisterende
`MusicPublishingPersistence`/TypedCell med kryptering som øvrige musikkceller.

Eierbeskyttet GET `usageStatistics` returnerer aggregater. Eierbeskyttet SET
`recordUsage` tar bare `{trackID, counter}` og avviser ekstra felt. Det finnes
ingen FlowElement per inkrement, og ingen lytterdata sendes til biblioteket.
Eksisterende leveransetokens i `MusicDeliveryCell` er ikke statistikk og endres
ikke til en ny lytterlogg. Bibliotekets faktiske persistensdump testes for
cookie, token-ID, forespørsels-UUID-er, IP og user agent.

HTTP:
- `play` og begge grener av `buy-play`: én start etter vellykket tokenutstedelse.
- `preview`: bare preview-telleren. Byte-lesinger øker ikke lytte-/starttellere.
- `played-through`: samme same-origin-sjekk som `play`, publisert/unlisted låt,
  eksisterende minnebasert ratebegrenser i egne bøtter, 204 ved suksess.
- Spillerens `ended`: én lydløs POST for aktuell publisert fullversjon, før købytte.
  Privat miks, preview, lukket spiller og duplisert `ended` rapporteres ikke.
- Alle tre leveranselesebanene teller vellykkede, ikke-tomme download-lesinger
  separat. Nedlasting er fortsatt deaktivert i produksjon. Testen restaurerer
  en legacy download-ressurs/tokenfixture; ingen produksjonssperre fjernes.
- `GET /butterpop/api/workspace/statistics`: innlogging + samme `workspace.read`
  som workspace-state. `{tracks: [...]}`, med bare `trackID`, `title`, fire tellere,
  `since` som UTC ISO 8601 og `verified:false` per rad. Ingen identitetsfelt.

Statistikkfanen (1c), samtykke/Agreement, per-lytterhistorikk og skive 2 inngår ikke.

## Filer endret i PR

- `Sources/App/Cells/MusicPublishing/MusicPublishingCells.swift`
- `Sources/App/Cells/MusicPublishing/MusicUsageStatistics.swift` (ny)
- `Sources/App/Cells/MusicPublishing/MusicAccessAndDeliveryCells.swift`
- `Sources/App/Controllers/VaporButterpopStudio.swift`
- `Public/js/butterpop-studio.js`
- `Tests/AppTests/MusicUsageStatisticsTests.swift` (ny, ni tester)
- `ci/test-filter.txt` (ny musikksuite og hele registry-suiten; ikke exclusions)
- `Documentation/ButterpopStudio_Product.md`

Rapporten her ligger separat i CellProtocolDocuments etter instruks. Eksisterende
endringer i hovedsjekkoutene og andre worktrees er ikke tatt med i PR-en.

## Testresultat / faktisk utført

Lokal Swift-bygging og etterspurt filter ble forsøkt med alle seks oppgitte
miljøvariabler unset, gjennom `scripts/run_swift_bounded.sh` som repoets
`AGENTS.md` krever. Wrapperen kjører kapasitetssjekk før Swift. Begge stoppet
med exit 75 før kompilering/testkjøring:

```text
Build capacity: 50.4 GiB free (5%); reserving 10 GiB leaves 40.4 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
```

Kommandoer:
```sh
scripts/run_swift_bounded.sh build --disable-sandbox --build-tests
scripts/run_swift_bounded.sh test --disable-sandbox --skip-build --filter 'MusicUsageStatisticsTests|MusicPublishingMVPRoutesTests|MusicPublishingConfigurationFactoryTests|ButterpopPilotReadinessTests|CellScaffoldRuntimeIdentityRegistryTests'
```

Samme kommandoer og filter ble kjørt på `origin/main` i det samme, rene
worktreet (midlertidig detached HEAD, deretter tilbake på leveransegrenen).
Samme exit 75, ingen tester kjørte:

```text
Baseline build exit: 75; baseline test exit: 75
Build capacity: 50.7 GiB free (5%); reserving 10 GiB leaves 40.7 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
```

Eksisterende CI for nøyaktig base-commit `4db0b1d6d619863d7f56f74129755ec826670a43`
var grønn: https://github.com/Digipomps/CellScaffold/actions/runs/36006238563.
GitHub rapporterte `Build every target: success` (28 min 14 s) og
`Run focused Swift gates: success` (13 min 20 s). Dette er tidligere CI-evidens,
ikke en ny lokal kjøring av det etterspurte filteret.

Ingen test er svekket eller hoppet over. Det foreligger ingen lokal bestått
Swift-testkjøring; kun syntaksanalyse med `swiftc -frontend -parse` (exit 0).

`HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, exit 0. Første forsøk
uten override valgte `/usr/local/bin/python3.12` og feilet med `Bad CPU type in
executable`. Den støttede miljøvariabelen rettet verktøyvalget; scriptet ble ikke endret.

```text
ok: liten literal (8) passerer
ok: stor literal (25) stoppes
ok: baseline dekker registrert stoerrelse
ok: vekst utover baseline stoppes
ok: kommentar og streng teller ikke
ok: indre literal over grensen fanges
ValueType-literaler over 20 oppfoeringer: 27 | dekket av baseline: 27
OK: ingen ValueType-literal er stor nok til aa velte typesjekkeren.
```

`ci/test-suite-coverage.sh`, exit 0:
```text
testsuiter:      338 | kjøres:      318 | unntatt:       21
OK: ingen testsuite faller stille utenfor.
```

`node --check Public/js/butterpop-studio.js`, exit 0. I tillegg en Node/VM-prøve
som kjører den faktiske spillerkoden med DOM-/nettverksadaptere, inklusive
avvist POST (ingen uhåndtert feil):
```text
PASS: ended once per track; paid/free tracking; private/preview/closed excluded; rejected POST swallowed.
```

Explore-audit på `Sources/App/Cells/MusicPublishing`: 94 komplette kontrakter,
94 handlers, 0 feil, 0 advarsler. Baseline `origin/main`: 92/92, også 0/0.
På den uendrede lokale CellProtocol-kilden ga ferdighetens generelle audit
311 komplette kontrakter, 320 handlers, 5 feil og 19 advarsler. Disse ligger
utenfor PR-en og er ikke merket som bestått.

## CI og åpne begrensninger

Første CI-kjøring `36069672074` ble avbrutt av Codex etter at en oppfølging
sikret stabil `since` også for migrerte nulltellere før første API-lesing.
CI https://github.com/Digipomps/CellScaffold/actions/runs/36069956161
på implementasjonscommit `cec4834a00164930b7513b7e47dc5e24c3e67ca3`
bygde alle mål og bestod alle 30 Swift-bolker. Den ble deretter avbrutt av Codex
for å prioritere oppfølgingskjøringen med full registry-dekning. Jobbens samlede
status er derfor `cancelled`; bygg- og Swift-teststegene er bekreftet `success`.

Sitert CI-utdata (2026-09-24 UTC, 2026-09-25 norsk tid):
```text
Test Suite 'MusicUsageStatisticsTests' passed at 2026-09-24 23:30:26.781
Executed 9 tests, with 0 failures (0 unexpected) in 13.664 (13.664) seconds
alle 30 bolker grønne
```

Alle ni nye tester passerte, inkludert de seks navngitte akseptansetestene,
rate-/same-origin-/publiseringskontroll, feilutstedelse og migrering. Øvrige
etterspurte musikkregresjoner i samme kjøring: `ButterpopPilotReadinessTests`
2/2, `MusicPublishingConfigurationFactoryTests` 4/4,
`MusicPublishingMVPRoutesTests` 1/1, alle med null feil.

Det gamle CI-filteret kjørte bare tre metoder i
`CellScaffoldRuntimeIdentityRegistryTests` (3/3 grønne). Siste commit
`42d266150b690da1f5ef4b1e5349d4365271f328` endrer bare filteret til hele suiten
med 21 metoder, slik at CI også dekker hele den femte suiten Kjetil ba om.
Det er ingen produksjonskodeendring siden den grønne Swift-kjøringen.

Oppfølgings-CI: https://github.com/Digipomps/CellScaffold/actions/runs/36073750383
Ved overlevering pågår denne kjøringen (`Build every target`). Hele registry-suiten
med 21 tester er ennå ikke bekreftet kjørt. Dette er det eneste nye testomfanget
siden den grønne implementasjonskjøringen. Losen må avvente grønn CI på
**42d26615** før merge og utrulling. LEVERT betyr levert kode/PR, ikke deployet
eller ferdig godkjent siste CI. Codex har ikke merget eller rullet ut.

Tallene er usikrede forespørselstellere, ikke unike lyttere eller bevis på at
lyden ble hørt. Ingen deduplisering over omstart eller per-lytterlagring innføres.
En download-range telles som en overføringslesing; ingen påstand om komplett
fildekning. Eksisterende persistenshjelper har ingen feilkvittering til kalleren;
reload-testen verifiserer normal lagringsbane, ikke simulert disktap.

## Retting 2026-09-25

Denne seksjonen erstatter tidligere leveringsstatus ovenfor.
Siste commit: `9950a6dc27ad327a82286715b58ea62ca73c8c86`, pushet til samme gren
`pdd/musikkstatistikk-skive1` i PR https://github.com/Digipomps/CellScaffold/pull/262.
Produksjonsrettingen ligger i `a5b64dc9083d501a60f7ad125876d4ee806ce44b`;
siste commit justerer bare testfixturens venting på gjenoppretting.
Ingen force-push, merge eller deploy. Commitmeldingen er
«Musikkstatistikk skive 1: telling stopper aldri avspilling», med begge pålagte
linjer for `Co-Authored-By` og `Claude-Session`.

`VaporButterpopStudio.recordUsage` er nå en ikke-kastende best-effort-wrapper.
Den fanger både oppslagssvikt i biblioteket og avvist telleroppdatering. Alle
tokenutstedelsesveiene (`play`, gratis og betalt `buy-play`, `preview`) beholder
svaret og spillercookien ved tellerfeil. `played-through` beholder 204 ved
tellerfeil; eksisterende publiserings-, same-origin- og ratekontroller gjelder
fortsatt. Feilen logges med `req.logger.warning`; selve loggteksten interpolerer
bare `trackID` og tellertype, aldri feilobjekt, identitet, token eller cookie.

Nedlastingskontrollen avdekket at `false` **tidligere stoppet leveransen**:
to `guard`-uttrykk returnerte `error: download statistics unavailable` etter
at autoriserte bytes allerede var lest. Begge kallstedene ignorerer nå
best-effort-resultatet (`_ = await recordDownloadIfNeeded(...)`) og returnerer
data som før. Dette dekker `readToken`, `readTokenRange` og `readTokenEnvelope`.
Tillatelses-, token-, ressurs- og filkontrollene er beholdt. Produksjonens
nedlastingssperre er ikke endret.

Ny `testCounterFailureNeverBlocksPlayback` bruker eksisterende eierstyrte
intercept-API til å la bibliotekets `recordUsage` returnere `false`. Testen
bekrefter først faktisk `counterRejected`, deretter HTTP 200, `status: issued`,
spillercookie og lesbare, korrekte lyddata for `play`, gratis `buy-play` og
`preview`, samt tomt 204-svar for `played-through`. Tellerne forblir null.
Den eksisterende nedlastingstesten verifiserer også avvist telling og uendret
dataleveranse gjennom alle tre leseveier. Ingen test-seam er lagt til i
produksjonskoden. Betalt `buy-play` er kontrollert i kildekoden og bruker samme
feilhåndteringswrapper; den nye HTTP-testen bruker gratis-fixturen.

Lokal verifikasjon er nå grønn:

- `scripts/run_swift_bounded.sh build --disable-sandbox --build-tests`: exit 0,
  171,01 sekunder. Kapasitetsvakten rapporterte 62,6 GiB ledig og 52,6 GiB / 5 %
  etter 10 GiB reserve. To Swift-jobber, ingen omgåelse av byggevakten.
- `scripts/run_swift_bounded.sh test --disable-sandbox --skip-build --filter 'MusicUsageStatisticsTests|MusicPublishingMVPRoutesTests|MusicPublishingConfigurationFactoryTests|ButterpopPilotReadinessTests|CellScaffoldRuntimeIdentityRegistryTests'`:
  exit 0, **38 tester, 0 feil**. Fordeling: MusicUsageStatistics 10,
  MusicPublishingMVPRoutes 1, MusicPublishingConfigurationFactory 4,
  ButterpopPilotReadiness 2 og hele CellScaffoldRuntimeIdentityRegistry 21.
- `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`,
  `ci/test-suite-coverage.sh`, syntaksanalyse av de tre endrede Swift-filene og
  `git diff --check`: alle bestått. `Package.resolved` er uendret.

Bygg-/testlogger: `/private/tmp/musikkstat-retting-build.log` og
`/private/tmp/musikkstat-retting-tests.log`.

CI for produksjonsrettingen (`a5b64dc9`):
https://github.com/Digipomps/CellScaffold/actions/runs/36075374277.
Alle mål bygde grønt, men Swift-testgaten feilet. Den nye
`testCounterFailureNeverBlocksPlayback` passerte i Linux-CI (1,085 sekunder),
og hele registry-suiten passerte (21/21). De øvrige tre etterspurte suitene
passerte også (2 + 4 + 1 tester). MusicUsageStatistics hadde 9/10 grønne;
totalt feilet 1 av 30 Swift-bolker, bolk 9. Nedlastingstesten feilet med:

```text
MusicUsageStatisticsTests.testDownloadCountsAsTransferNotListening : threw error "notFound"
```

Kjøringen fullførte med samlet `failure`; et etterfølgende kanselleringsforsøk
ble avvist fordi den allerede var ferdig. Bygging, Admin web-kontrollene,
Thursday demo P0 og document live collaboration var grønne. Swift-teststeget
var `failure`; de to etterfølgende shell-/pakkekontrollene ble hoppet over.
Loggutdraget er fra `/private/tmp/musikkstat-retting-ci-job.txt`;
dette er ikke grønn CI.

Kildegjennomgangen avdekker en mulig race i den eksisterende testventingen:
dekoding installerer handlerne asynkront, og `state` installeres **før**
lesehandlerne. Testfixturen venter nå på svar fra den sist installerte handleren,
med en ugyldig payload som hverken leser bytes eller teller. De faktiske
nedlastingslesingene kjører fortsatt uten retry, med alle assertions beholdt.
Dette endrer ingen produksjonskode eller runtime-kontrakt. Feilen ble ikke
reprodusert lokalt; Linux-verifikasjon av den nye ventebetingelsen gjenstår.

Etter testrettingen ble det samme fem-suite-filteret bygget og kjørt på nytt
via `scripts/run_swift_bounded.sh test --disable-sandbox --filter ...`:
**38 tester, 0 feil**, exit 0. Logg:
`/private/tmp/musikkstat-retting-ready-tests.log`. Literal-sjekken og
`git diff --check` passerte igjen.

CI for siste commit (`9950a6dc`):
https://github.com/Digipomps/CellScaffold/actions/runs/36079253838.
Status ved overlevering: `in_progress`, aktivt steg `Build every target`.
Overvåkingen med `gh run watch --exit-status` stoppet ved den opprinnelige
fristen 2026-09-25 00:58:38 UTC (02:58:38 norsk tid), med watcher-exit 124.
Ingen ny 60-minuttersperiode ble startet etter testoppfølgingen. Avsluttende
GitHub-kontroll kl. 00:59 UTC bekreftet at kjøringen fortsatt bygger, og at
PR-en er `OPEN` med head `9950a6dc27ad327a82286715b58ea62ca73c8c86`.
Selve CI-kjøringen er ikke kansellert og fortsetter i GitHub. Resultatet er
**uavklart**, ikke grønt. Merge må fortsatt avvente grønn CI på siste commit.

Overvåkingsresultat og logg finnes i
`/private/tmp/musikkstat-retting-ci-v2-result.json` og
`/private/tmp/musikkstat-retting-ci-v2-watch.log`.

Etter omtrent åtte minutter i kø ble den utdaterte kjøringen `36073750383`
for `42d26615` på samme PR kansellert for å slippe fram rettingen. Den kjørte
da `Run focused Swift gates`; dette var en pull-request-testjobb, ikke deploy.

Rapporten er oppdatert lokalt i det separate CellProtocolDocuments-repoet;
den var allerede untracked og er ikke tatt med i kodecommiten. Øvrige
eksisterende endringer i dokumentasjonsrepoet er urørt. Kodeworktreet er rent.
