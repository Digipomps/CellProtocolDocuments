STATUS: STOPPET — byggevakt exit 75: 54,2 GiB ledig, 44,2 GiB / 4 % etter reserve; HVELV-F1 er STOPPET og arbeidstreet har sporede endringer; head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 29.09.2026, **runde 5**, `PDD_sindre-import-uten-bruker_2026-09-25.F5-F9`. Ingen F5–F9-retting er levert. Ingen kode-/testendring, bygg, testkjøring, commit, push, merge eller ny CI er utført. **Ikke merge.**

Forrige rapport er bevart byte-identisk som [HVELV-F5-F9-runde3-20260929.md](HVELV-F5-F9-runde3-20260929.md), SHA-256 `a6681208308faec18cc42ed8922e87ad731fc0a2e18cab00745f77b53d0403cc`. Den faktiske filen var merket runde 3, selv om oppdraget omtaler runde 4. Ingen F5–F9-runde-4-rapport fantes i mappen; intet slikt arkiv er konstruert. Runde 1 og 2 er urørt.

## Stoppgrunn og ny kapasitetsmåling

[HVELV-F1.md](HVELV-F1.md):1 er **STOPPET**, nå runde 5, på samme head. Den beskriver et mislykket App-bygg, lokale rettelser som ikke er kompilert, og deretter kapasitetsstopp. Oppdragets «Er den STOPPET: stopp og rapporter» blokkerer avhengig F5–F9-implementering.

Den uttrykkelig bestilte byggevakten er kjørt på nytt fra HAVEN-roten, uten terskeloverstyring:

```sh
env -u HAVEN_BUILD_RESERVE_GIB -u HAVEN_BUILD_MIN_FREE_GIB -u HAVEN_BUILD_MIN_FREE_PERCENT CellScaffold/_wt-forvaltet-import-20260926/scripts/check_build_capacity.sh CellScaffold/_wt-forvaltet-import-20260926
```

```text
Build capacity: 54.2 GiB free (5%); reserving 10 GiB leaves 44.2 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
Exit status: 75
```

Dette er **denne jobbens måling**, ikke gjenbruk av F1s tall eller rydderapportens tidligere 60 GiB. Vakten er byte-identisk med PR-head. GiB-gulvet passeres, prosentgulvet blokkerer. Ingen rydding, terskelendring, alternativ cache eller eierskapsmarkering er forsøkt. Målingen fastslår ikke hvilke jobber som har brukt plassen. [Kapasitetsevidens](evidence-hvelv-f5-f9-runde5-20260929/build-capacity.txt).

## PR og bevart arbeidstre

`/opt/homebrew/bin/gh pr view 270 --repo Digipomps/CellScaffold --json number,url,headRefName,headRefOid,state` bekreftet [PR #270](https://github.com/Digipomps/CellScaffold/pull/270) **OPEN**, gren `pdd/forvaltet-kunstnerimport`, head `b658ef53e14dccdb12009991e78b1b44d47dac8a`. Lokal HEAD er identisk.

Arbeidstreet `CellScaffold/_wt-forvaltet-import-20260926` har **seks sporede endringer og åtte usporede F1-filer**. Det oppfyller ikke kravet om rent arbeidstre. Sporede endringer:

- `.github/workflows/admin-scaffold-image.yml`
- `Documentation/Operations/Managed_Artist_Import_2026-09-28.md`
- `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift`
- `Tests/AppTests/ManagedArtistImportTests.swift`
- `ci/run-tests.sh`
- `ci/test-filter.txt`

De usporede filene er tre recipient anchor/binding-filer, binding-test og offentlig testfixture, recipient-klienten og to testskript. Fullt inventar og hasher ligger i [entry-state.json](evidence-hvelv-f5-f9-runde5-20260929/entry-state.json). F1-utkastene er bevart, ikke flyttet som testrester. Ingen `.hvelv-test-root/` eller andre usporede testrester vises i Git-status. Ingenting er flyttet til `_to_delete/`, slettet, stashet eller overskrevet i arbeidstreet.

## F5–F9: fortsatt åpne

Fil:linje nedenfor er **Astras kildeankre på PR-head**, fra [ASTRA-HVELV-5.md](ASTRA-HVELV-5.md) og [ASTRA-HVELV-2.md](ASTRA-HVELV-2.md). De er ikke linjenumre i lokale F1-utkast eller ny kildeverifikasjon. Stiene er relative til CellScaffold. Ingen ny negativ test eller mutationstest er skrevet eller kjørt.

| Funn | Fil:linje på PR-head | Testnavn / ville fanget originalfeilen? | Gjenstående krav |
|---|---|---|---|
| F5 | `Sources/App/Support/SecureRuntimeIdentityManifestFile.swift:235`, `:346`; `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:46` | Ingen ny test; ingen originalregresjon bevist. Astra: eksisterende `ManagedArtistVaultFileTests.swift:171/:192/:201` dekker ikke fremmed read/search-only. | Avvis fremmede lesende/search/arvede ACL-grants på private objekter, skill mot lesbare forfedre, prøv faktisk leaseopptak fra fremmed prosess/konto. |
| F6 | `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:403`, `:438`, `:459` | Ingen ny test; ingen originalregresjon bevist. Astra: samtidighetstesten i `ManagedArtistImportTests.swift:314` prøver bare autoriserte execute-kall. | Autorisasjon/proof før global kø, tidsgrense og per-kilde-grense, kø-/kanselleringsvern, revalidering før effekt; taus uautorisert peer samtidig med legitim claim/fjerning samt mange ventende/kansellerte kall. |
| F7 | `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:176`, `:274`, `:472`, `:625` | Ingen ny test; ingen originalregresjon bevist. Astra: fjerningsprøven i `ManagedArtistImportTests.swift:408` sjekker ikke lagret årsak/utfører. | Privat årsak og faktisk utfører med tombstone og kvittering; reload og tilgangsvern; ingen offentlig lekkasje. |
| F8 | `Tests/AppTests/CellScaffoldRuntimeIdentityProvisionerTests.swift:705`, `:811`; `Tests/AppTests/SecureRuntimeIdentityManifestFileTests.swift:200`; `ci/test-filter.txt:40` | Eksisterende `testWriterRejectsExtendedAttributesOnExistingManifest` og `testWriterRejectsOverwriteWithoutExactOldDigestAndUses0600` er navngitt i tidligere rapport; ikke kjørt her. Ingen ny regresjon levert. | Varig beskyttet, portabel fixture-rot og navngitt CI-dekning; uendrede assertions/strict-avvisninger, ingen nye skips/exclusions. |
| F9 | `Sources/App/Support/SecureRuntimeIdentityManifestFile.swift:334`, `:337`; manifestkall `:86`, `:264` | Ingen ny test; ingen originalregresjon bevist. Astra: deterministisk ACL-oppslagsfeil er ikke dekket. | Avvis Darwin-oppslagsfeil, tillat bare dokumentert fravær; negativ test for begge bruksmåter og positiv prøve for legitim tom ACL. |

Astra 5 er bindende: **F1/F5/F6/F9 blokkerer merge; F4/F7/F8 må også lukkes før AP6.** Denne jobben lukker ingen funn. Historisk F2-/F3-bevis beholdes; det er ikke F5–F9-regresjonsbevis.

## Verifikasjonsgrense og videreføring

Kjørt: dokument-/statuskontroll, GitHub PR-metadata, ny kapasitetsvakt (exit 75), byte-identisk arkivering og rapportering. F1 runde 5 og forrige F5–F9-rapport er lest; Astra 5 og relevante utdrag av Astra 2 er kontrollert. Tidligere Astra, FORMAALSSPEC og PLAN ble hentet, men samlet verktøyutskrift var avkortet; de erklæres ikke fullstendig gjennomlest. Driftsnotatet er lest fra PR-head. Lokale F1-kodeutkast er ikke faglig vurdert.

Ikke kjørt: `scripts/run_swift_bounded.sh … --disable-sandbox`, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh`, Swift-/ACL-/kø-/tombstone-/manifesttester, negative tester/mutationstester, ny CI eller CI-venting. Ingen nøkler er hentet eller signering utført. Strict-oppførsel, eksisterende avvisningstester og skips/exclusions er ikke endret av denne jobben.

F1 må fullføres og få oppdatert handoff før F5–F9 fortsetter. Byggevakten må passere uten overstyring, og ansvarlig F1-jobb må ferdigstille de bevarte endringene slik at arbeidstreet er rent på aktuell PR-head. Deretter gjenopptas full innlesing, implementering og lokale tester før commit/push og maks 60 minutters CI-venting. Ingen ny beslutning om eieranker er nødvendig.

Bare denne rapporten, arkivkopien og evidensmappen er skrevet i PDD-mappen. Ingen Git-levering er gjort. Læringsvurdering: ingen ny generell teknisk læring; gjentatt kapasitets-/avhengighetsblokkering dokumenteres her, og `haven_learn.py none` registrerer vurderingen.
