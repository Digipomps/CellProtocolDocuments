# k17 — HavenAgentD PR #36 repinnet etter CellProtocol #67

Levert 2026-10-13. PR-en er fortsatt **OPEN / DRAFT**. Ingen merge, tag, deploy, installerbygg eller vertsendring er utført. Alle identiteter og meldinger i testene er syntetiske.

- PR: https://github.com/Digipomps/HavenAgentD/pull/36
- Gren: `codex/k15-attachment-backpressure`
- Ny head: `8ae4c276ecedb26c784a19274756906f7415435b`
- Commit: https://github.com/Digipomps/HavenAgentD/commit/8ae4c276ecedb26c784a19274756906f7415435b
- Forrige head: `538e8187d9476fdf50806b0cfefe54a65fd64895`
- Arbeidstre: `_worktrees/k15-agentd-client`, rent etter commit/push og ved sluttkontroll.

## Pinne og endringsomfang

CellProtocol er pinnet til squash-revisjonen på main etter #67:
`34cecefcb78e4e3775c116a50b0d96a32c1e2f9c`.

GitHub tag-ref for `2026.9.10` returnerte HTTP 404 ved oppstart; derfor er det brukt eksakt revisjon som bestilt. Main og #67s merge-revisjon ble kontrollert mot GitHub. `Package.resolved` ble regenerert med SwiftPM; kun CP-pinnen og manifestets `originHash` endret seg. **Alle 35 andre pinner er identiske**, uten tillegg eller fjerning.

Committen endrer bare disse tre filene i HavenAgentD:

1. `Package.swift` — ny CP-revisjon.
2. `Package.resolved` — regenerert låsefil.
3. `Tests/HavenCorrespondenceMCPTests/CorrespondenceSigningRetryTests.swift` — utvidet eksisterende negativ test med ren meldingstekst `signingTemporarilyUnavailable`.

Ingen produksjonskode måtte endres for retry. `CorrespondenceSigningRetry.run` fanger `BridgeSigningBackpressure`; GET og SET går gjennom denne mekanismen. Parseren i den faktisk bygde CP-revisjonen bruker `status`, `&bridgeRetry`, `reasonCode` og positiv `retryAfterSeconds`, ikke `message`. Den utvidede testen bekrefter ett forsøk og ingen venting for den nye tekstfeilen, slik som for `attachmentUnavailable` og ukjent SET-resultat. Alle fire retry-tester bestod. Retry-grensene er uendret.

## Verifikasjon

| Kontroll | Resultat |
|---|---|
| SwiftPM resolve og maskinell sammenligning av pinner | Exit 0; bare CP endret blant 36 pinner |
| Full lokal `swift test --jobs 2 --no-parallel --disable-automatic-resolution`, via bounded-runner | **Exit 0; 369 tester, 70 suiter, alle sju testmål** |
| Lokal kvoteregresjon med 1 100 037 byte begge veier, tilbakekall og avslag etterpå | Bestod på **1330,367 s**, uendret produksjonspolicy |
| Lokal daemon-smoke med egen syntetisk runtime-rot | **Exit 0** |
| Python-hjelpetester for CI-fase og testkjører | **8 bestod** |
| Diff-hygiene, kildehash og commit-binding | Grønt; commit-diffen er byte-identisk med den testede kandidaten |
| CI «Assert every pinned dependency is on its own main» | **SUCCESS** |
| CI «Assert Package.resolved matches the manifest» | **SUCCESS** |
| CI «Test and smoke-check HavenAgentD» | **SUCCESS; 369 tester / 70 suiter**, kvoteregresjon **1327,931 s** |
| CI «Stage tested runtime candidate» | **SUCCESS**; ordinær CI-staging av testet runtime, ingen installerbygg |

Lokal plattform: macOS 27.0.1 arm64, Xcode 27.0 / Swift 6.4. CI: macOS 26 / Xcode 26.3. Kandidaten ble testet før commit og deretter kontrollert mot commit-diffen; ingen kildeendring kom mellom grønn port og push.

**HavenAgentD CI er terminalt grønn for ny head:**
https://github.com/Digipomps/HavenAgentD/actions/runs/38375104071

Jobb med de konkrete portene:
https://github.com/Digipomps/HavenAgentD/actions/runs/38375104071/job/115221391204

## Første lokale forsøk og ny kjøring

Første fulltest avsluttet exit 1 kl. 08:42:17Z. 56 tester bestod, inkludert hele korrespondansepakken og kvoteregresjonen. Fem senere testbundler kunne ikke lastes fordi en samtidig byggejobb hadde overtatt cache-leien som «stale» og slettet den aktive cachen. Den andre jobbens logg dokumenterer slettingen; hvorfor leien ble feilklassifisert er ikke fastslått. **Første forsøk regnes ikke som en grønn fullport.**

Andre forsøk brukte samme kandidat, bounded-runner, cache-nøkkel, to byggejobber, diskvakt og 24 GiB cachetak, med egen administrert cacherot for å unngå samme kollisjon. GC var fortsatt report-only. Ingen manuell sletting eller delt cacheopprydding ble utført av k17. Den komplette nye fulltesten og daemon-smoken bestod. Første forsøk og kollisjonsbevis er bevart.

## Eksisterende forhold utenfor repinnen

- PR #32 er fortsatt åpen og er fortsatt en dokumentert forutsetning for eventuell senere landing av #36. Ingen merge er gjort.
- Den separate, **uendrede** `.github/workflows/private-release-artifact.yml` feiler før noen jobber starter. Dette skjedde også på forrige head. GitHub CLI angir sannsynlig workflow-filproblem; presis validator-annotasjon er ikke hentet i k17. Ingen release-workflow ble manuelt startet. Ny feilregistrering: https://github.com/Digipomps/HavenAgentD/actions/runs/38375095899 ; tidligere: https://github.com/Digipomps/HavenAgentD/actions/runs/38317560792 . Dette er skilt fra den grønne **HavenAgentD CI**-kjøringen over.
- Læring `L-2026-10-13-en-samtidig-swiftpm-gc-slettet-k17s-aktive` er fanget og anvendt i `CellScaffold/.claude/skills/haven-git-workflow/SKILL.md`; ZIP er generert. Synk til hjemmemappens skill-kopier ble blokkert av sandkassens skrivegrense (EPERM). Distribusjon er derfor ufullført, og læringskontrollens `--strict` returnerer 1. Den begrensningen er ikke omgått.
- Primærutsjekkene hadde eksisterende urelatert arbeid. Ingen av disse kodeendringene ble tatt med i committen.

## Bevis

Alle stier her er relative til HAVEN-roten. Beviskatalog:
`HAVEN-Deploy/_handoff/KORR-UT/k17/`.

- `startup.json`, `pin-comparison.json`, `resolve.log`, `resolve-r2.log`, `dependency-main-preflight.json` — pinnevalg og oppløsning.
- `candidate.json`, `candidate.patch`, `local-results.json`, `new-head.txt` — kilde-/commit-binding og lokale resultater.
- `full-r2.log`, `full-native-r2-queue.txt`, `smoke.log`, `smoke-result.json`, `cp-checkout-r2.json`, `retry-source-inspection.json` — komplett grønn lokal kjøring.
- `full.log`, `full-native-queue.txt`, `cache-collision-evidence.json` — bevart første feilkjøring.
- `ci-final.json`, `ci-logs.zip`, `ci-test.log`, `ci-test-results.json`, `pr-final.json` — terminal CI, rålogg og PR-status.
- `release-validator-before.json`, `release-validator-after.json` — uendret separat workflow-feil med null jobber.
- `learning-check-result.json`, `learning-check.txt` — læringsstatus, inkludert ufullført synk.
- `evidence-sha256.json` — SHA-256 for sentrale bevisfiler.

STATUS: LEVERT
