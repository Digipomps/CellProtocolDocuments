STATUS: STOPPET — byggevakt exit 75: 54,6 GiB ledig, 44,6 GiB / 4 % etter reserve; HVELV-F1 er STOPPET og arbeidstreet har sporede endringer; lokalt head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 29.09.2026, **runde 6**, `PDD_sindre-import-uten-bruker_2026-09-25.F5-F9`. Ingen F5–F9-retting er levert. Ingen kode-/testendring, bygg, testkjøring, commit, push, merge, ny CI eller utrulling er utført. **Ikke merge.** Oppdragets stoppregler er fulgt.

## Bevaring

Forrige gjeldende rapport, runde 5, er bevart **byte-identisk** som [HVELV-F5-F9-runde5-20260929.md](HVELV-F5-F9-runde5-20260929.md), SHA-256:

```text
2fb0998df78da6c7b19a9fdfd9633310e61da14c15c31b8b2b8b750cf28f82fc
```

Tidligere arkiver er urørt. Runde-5-rapportens redegjørelse for manglende runde-4-arkiv er bevart der; intet runde-4-arkiv er konstruert.

## Målt stoppgrunn

Kl. **18:14:59 UTC / 20:14:59 Oslo** ble følgende kjørt fra `CellScaffold/_wt-forvaltet-import-20260926`:

```sh
scripts/check_build_capacity.sh .
```

```text
Build capacity: 54.6 GiB free (5%); reserving 10 GiB leaves 44.6 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
Exit status: 75
```

Vakten er byte-identisk med lokal HEAD. Ingen av `HAVEN_BUILD_RESERVE_GIB`, `HAVEN_BUILD_MIN_FREE_GIB` eller `HAVEN_BUILD_MIN_FREE_PERCENT` var satt; alle tre ble også fjernet fra kommandoens miljø slik at uendrede standardverdier ble brukt. Ingen overstyring er brukt. GiB-gulvet passeres; **prosentgulvet på 5 % etter 10 GiB reserve blokkerer**. Arbeidstreets AGENTS.md omtaler 10 %, men den uendrede vaktens faktiske terskel er 5 %.

`df -Pk` etter vakten målte **57 200 000 KiB tilgjengelig** av **971 298 980 KiB** på `/dev/disk3s5`. Dette er denne jobbens måling, senere enn rydderapportens 59 GiB fra 11:52Z. Årsaken til forskjellen er ikke undersøkt eller tilskrevet bane b. Ingen rydding, stopp av andre prosesser, alternativ cache/scratch-path, cachemarkering eller terskelendring er forsøkt. [Rå kapasitetsmåling](evidence-hvelv-f5-f9-runde6-20260929/build-capacity.txt) og [kommando/miljø/exitkode](evidence-hvelv-f5-f9-runde6-20260929/build-capacity.json).

[HVELV-F1.md](HVELV-F1.md):1 er fortsatt **STOPPET**, nå runde 6, samme lokale head. Oppdragets «Er den STOPPET: stopp og rapporter» blokkerer F5–F9 uavhengig av kapasiteten.

## Arbeidstre og revisjon

Lokal gren er `pdd/forvaltet-kunstnerimport`, head `b658ef53e14dccdb12009991e78b1b44d47dac8a`. Ekstern head/status for PR #270 og CI er **ikke kontrollert på nytt i denne runden**. Runde 5 bekreftet samme PR-head. Historisk grønn CI er ikke bevis for F5–F9.

Arbeidstreet har **seks sporede endringer og åtte usporede F1-filer**. Det oppfyller ikke oppdragets krav om rent arbeidstre. De sporede endringene er:

- `.github/workflows/admin-scaffold-image.yml`
- `Documentation/Operations/Managed_Artist_Import_2026-09-28.md`
- `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift`
- `Tests/AppTests/ManagedArtistImportTests.swift`
- `ci/run-tests.sh`
- `ci/test-filter.txt`

De åtte usporede filene er F1-utkast, ikke testrester som denne jobben kan flytte. Ingen `.hvelv-test-root/` eller andre usporede testrester vises i Git-status; ingenting er flyttet til `_to_delete/`. Ingen kildefiler er slettet, stashet eller overskrevet. [Inngangstilstand og SHA-256](evidence-hvelv-f5-f9-runde6-20260929/entry-state.json) og [sluttkontroll](evidence-hvelv-f5-f9-runde6-20260929/preservation-check.json) dokumenterer bevaringen. Annet eksisterende WIP i hovedrepoene er urørt.

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

Kjørt: lese-/statuskontroll, ny kapasitetsvakt (exit 75), byte-identisk arkivering og rapportering. F1 runde 6 og forrige F5–F9-rapport er lest. F5–F9-avsnittene og relevante test-/AP6-krav i bindende Astra 2 og Astra 5 er lest som utdrag; dette er ikke en ny kildekodeaudit. Astra 1, FORMAALSSPEC, PLAN og driftsnotatet er ikke lest på nytt i denne runden, ettersom stoppreglene allerede var utløst. Full innlesing må gjøres før gjenopptatt implementering.

Ikke kjørt: `scripts/run_swift_bounded.sh … --disable-sandbox`, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh`, Swift-/ACL-/kø-/tombstone-/manifesttester, negative tester/mutationstester, ny CI eller CI-venting. Ingen nøkler er hentet eller signering utført. Sentralhvelvets strict-oppførsel, eksisterende avvisningstester og skips/exclusions er ikke endret av denne jobben.

F1 må fullføres og få oppdatert handoff før F5–F9 fortsetter. Byggevakten må passere uten overstyring, og ansvarlig F1-jobb må ferdigstille endringene slik at arbeidstreet er rent på aktuell PR-head. Deretter gjenopptas implementering og lokale tester før bestilt commit/push og maksimalt 60 minutters CI-venting. Ingen ny beslutning om eieranker trengs.

Bare denne rapporten, runde-5-arkivet og evidensmappen er skrevet i PDD-mappen. Læringsvurdering: ingen ny generell læring; dette gjentar kjent kapasitets-/avhengighetsblokkering. `haven_learn.py none --reason ...` er kjørt og registrert i den uversjonerte læringsloggen.
