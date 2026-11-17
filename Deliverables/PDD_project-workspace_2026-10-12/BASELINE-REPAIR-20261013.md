# Prosjektbaseline: målt feil og avgrenset testrettelse

2026-10-13. **Rød lokal baseline. Forslaget nedenfor er ikke anvendt eller kjørt.**

## Målt resultat

Den koordinerte kjøringen gikk 14:53:16Z–15:13:02Z på CellScaffold `3a6680446e55fc1644afb368ac2bf48dd0720e30`, med publisert CellProtocol `b4100f5734bb0b3781600845a267e424e55c0989` (2026.9.7). Alle 112 forventede metoder startet og fikk én sluttstatus: 111 besto, én feilet. Swift og kødriver returnerte 1. Køens `.done` og `EXIT=1` er verifisert. Kildearbeidstreet er rent; Package.resolved er byteidentisk før/etter. Ingen CI eller deploy.

| Suite | Besto | Feilet |
|---|---:|---:|
| PortholeComponentSourceActionTests | 10 | 0 |
| PortholeConfigurationLoadingTests | 50 | 1 |
| PortholeWebActionStateSourceTests | 2 | 0 |
| ProjectPortfolioCellTests | 13 | 0 |
| WorkbenchAccessGrantConfigurationTests | 36 | 0 |

Feilen er `PortholeConfigurationLoadingTests.testBootstrapAddsAccessRequirementOverlayAndPrefillsPromptForBlockedReference`, linje 1806: `XCTAssertNotNil(approveButton)`. Oppsummering, avvisningsknapp og øvrige assertions i samme test feilet ikke. Tilgangsvisningen er dermed ikke helt borte: det er forventningen om den gamle godkjenningshandlingen som feiler.

## Kildegrunnlag

- Testens positive forventning om `porthole.approveAccessRequirement` kommer fra `191447af3` (2026-04-16).
- `21219a834592955928a165415d754178fe8a54cc` (2026-10-07) endret knappen til `porthole.requestAccessRequirement`, «Be om tilgang», og la til `porthole.recheckAccessRequirement`. Endringen er med i den målte kilden.
- `CellScaffold/Documentation/Operations/Admin_Access_Banner.md` sier eksplisitt at ingen overlay tilbyr inline approval; den gamle kompatibilitetshandlingen forblir fail-closed.
- `CellScaffold/Tests/AppTests/AdminAccessBannerTests.swift`, særlig `testOwnedLocalGrantRemainsGrantAndDoesNotOfferIneffectiveApproval`, krever at request/recheck finnes og at approve er borte. Disse fire nyere testene var ikke med i den 112-metoders baselinen; de er lest, ikke kjørt av denne økten.

## Konkret foreslått rettelse

`evidence/proposed-access-banner-test-20261013.patch` endrer bare den ene eksisterende testmetoden:

1. Krev request-knappen og recheck-knappen.
2. Krev at den utdaterte approve-knappen er fraværende.
3. Behold alle andre assertions og testoppsettet.

Ingen produkt-, identitets-, grant- eller autorisasjonskode endres. Patchen er klargjort som forslag; committed testfil er urørt. Patchens og kandidatfilens SHA256 står i `evidence/baseline-failure-20261013.json`.

## Neste lokale kjøring — krever godkjenning

Anvend den ene testrettelsen. Frys en ny pakke med de opprinnelige 112 metodene pluss de fire eksisterende AdminAccessBannerTests, totalt **116**. Kjør den én gang gjennom køeieren, med to Swift-jobber og samme 40 GiB/10 % etter reserve. Ingen CI/deploy. Ved grønt går den allerede godkjente og fortsatt ukjørte CP8→CS17-pakken videre med fersk admission; ved rødt stopper kjeden igjen. Ikke gjenbruk eller endre den avsluttede baselinepakken.

Grunnen til ny avklaring er den godkjente PLAN.md §Verifikasjon punkt 1–2: rød kjøring gjentas ikke automatisk, og committed tester endres ikke uten Kjetils godkjenning. Samme regel er konkretisert i `CellProtocolDocuments/.claude/skills/haven-purpose-driven-dev/SKILL.md`, «A6: også egne tester» og «A11: stopp ved kode 000». G2 for prosjektflaten står fortsatt godkjent; det er ingen ny G1/G2-port.

## Prosjektarbeid og kø

CP8→CS17 har ingen attempt-started og ingen fersk ADMISSION. Dens AUTHORIZATION.json er urørt. Køeier bekreftet hold og frigjorde vinduet 15:15:12Z. Andre tråders jobber røres ikke. Ny prosjektkode er ikke lagt inn på rød baseline. Forberedte P1-kildekrav, G2 og godkjent GUI er bevart. Første produktdel er fortsatt direkte åpning med autorisert, isolert prosjektkontekst.

Råresultatene ligger under `HAVEN-Deploy/_handoff/ARBEIDSBENK/PROJECT-WORKSPACE-BASELINE-20261013/`. Den gamle avviste jobbkonvolutten før Swift-start og den faktiske røde testkjøringen er separate hendelser.

## Kontroll av forslaget

`git apply --check` mot det urørte prosjektarbeidstreet passerte. Patchen er fortsatt ikke anvendt. Dette er anvendbarhetskontroll av diffen, ikke en ny Swift-test. Øktens køkonvolutt-læring er applied/synced til Codex og Claude; global læringskø har fortsatt andre åpne poster.

## 2026-10-13T15:48:07.579970+00:00 — Kjetil approved and patch applied

«Jeg godkjenner testrettelsen og én ny lokal baseline på 116 tester. Ved grønt kjører du de allerede godkjente 8+17 testene og fortsetter med prosjektflaten. Ingen CI eller deploy.»

The exact proposed patch (93a4e5a61625f974eb4242975f8e2aecaab42d27ebc3aae8bf5eccb293fd45f1) is now applied to the isolated project worktree, with no product edits. New packet `HAVEN-Deploy/_handoff/ARBEIDSBENK/PROJECT-WORKSPACE-BASELINE-R1-20261013` is frozen at manifest `c2d85e1999b8bdd6fd4abe7121879426fff34f15d7ece11a07ced8e2aa60f73b`. Its non-Swift checks passed in both locales, the queue envelope uses the HAVEN root, and the method list contains exactly 116 unique tests. No new test attempt or admission has been created by this preparation. Queue owner must grant a fresh exclusive window. Earlier red evidence is unchanged.
