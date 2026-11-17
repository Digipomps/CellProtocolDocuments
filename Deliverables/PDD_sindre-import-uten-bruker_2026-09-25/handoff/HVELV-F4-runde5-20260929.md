STATUS: STOPPET — byggevakt exit 75: 54,2 GiB ledig, 44,2 GiB / 4 % etter reserve; HVELV-F5-F9 er STOPPET og arbeidstreet har sporede endringer; head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 29.09.2026, **runde 5**, `PDD_sindre-import-uten-bruker_2026-09-25.F4`. Ingen F4-retting eller nytt runtime-/transporttestbevis er levert. Ingen bygg, tester, commit, push, merge eller ny CI. **Ikke merge.**

Forrige rapport er bevart byte-identisk som [HVELV-F4-runde3-20260929.md](HVELV-F4-runde3-20260929.md), SHA-256 `993f381ce31e9b97e5236da7170cbf12ebe11f83109a92c2a239d5bdd27431a9`. Filen var faktisk merket runde 3, selv om oppdraget omtaler runde 4. Ingen runde-4-rapport fantes blant F4-rapportene i handoff-mappen; intet slikt arkiv er konstruert. Runde 1 og 2 er urørt.

## Stoppgrunn og måling

[HVELV-F5-F9.md](HVELV-F5-F9.md):1 er **STOPPET**, runde 5, på samme head. Oppdragets «Er den STOPPET: stopp og rapporter» stopper F4 uavhengig av diskplass. Arbeidstreet har i tillegg seks sporede endringer og åtte usporede filer, dokumentert som F1-utkast i forgjengerrapporten.

Den uttrykkelig bestilte byggevakten ble likevel kjørt på nytt, uten terskeloverstyring. Følgende tre miljøvariabler ble fjernet fra vaktens prosessmiljø slik at skriptets standardverdier gjaldt: `HAVEN_BUILD_RESERVE_GIB`, `HAVEN_BUILD_MIN_FREE_GIB`, `HAVEN_BUILD_MIN_FREE_PERCENT`. Tilsvarende kommando fra HAVEN-roten:

```sh
env -u HAVEN_BUILD_RESERVE_GIB -u HAVEN_BUILD_MIN_FREE_GIB -u HAVEN_BUILD_MIN_FREE_PERCENT CellScaffold/_wt-forvaltet-import-20260926/scripts/check_build_capacity.sh CellScaffold/_wt-forvaltet-import-20260926
```

```text
Build capacity: 54.2 GiB free (5%); reserving 10 GiB leaves 44.2 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
Exit status: 75
```

Dette er denne jobbens nye måling, ikke gjenbruk av rydderapportens 60 GiB eller forgjengerens tall. Vaktens bytes er identiske med PR-head. GiB-gulvet passeres; prosentgulvet blokkerer. Ingen terskler, cacheplasseringer eller eierskapsmarkører er endret. Målingen fastslår ikke hvilke jobber som har brukt plassen. [Kapasitetsevidens](evidence-hvelv-f4-runde5-20260929/build-capacity.txt).

## PR og bevart arbeidstre

GitHub-kontrollen med `gh pr view 270 --repo Digipomps/CellScaffold --json number,url,headRefName,headRefOid,state` bekreftet [PR #270](https://github.com/Digipomps/CellScaffold/pull/270) som **OPEN**, gren `pdd/forvaltet-kunstnerimport`, head `b658ef53e14dccdb12009991e78b1b44d47dac8a`. Lokal HEAD er identisk.

Git-status ved inngangen:

```text
 M .github/workflows/admin-scaffold-image.yml
 M Documentation/Operations/Managed_Artist_Import_2026-09-28.md
 M Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift
 M Tests/AppTests/ManagedArtistImportTests.swift
 M ci/run-tests.sh
 M ci/test-filter.txt
?? Sources/App/Cells/ManagedArtistImport/ManagedArtistRecipientAnchor.swift
?? Sources/App/Cells/ManagedArtistImport/ManagedArtistRecipientAnchorSource.swift
?? Sources/App/Cells/ManagedArtistImport/ManagedArtistRecipientBinding.swift
?? Tests/AppTests/Fixtures/managed-artist-local-agentd-approval.json
?? Tests/AppTests/ManagedArtistRecipientBindingTests.swift
?? scripts/managed_artist_recipient.py
?? scripts/test_managed_artist_import.sh
?? scripts/tests/test_managed_artist_recipient.py
```

Ingen egne usporede testrester vises i Git-status. F1-utkastene er bevart; ingenting er flyttet til `_to_delete/`, slettet, stashet eller overskrevet i arbeidstreet. Full status, tidspunkt, PR-metadata og filhasher ligger i [entry-state.json](evidence-hvelv-f4-runde5-20260929/entry-state.json).

## F4: fortsatt åpent

Ankrene nedenfor er videreført fra [ASTRA-HVELV-5.md](ASTRA-HVELV-5.md):92 og [ASTRA-HVELV-2.md](ASTRA-HVELV-2.md):131–137 på den vurderte PR-headen. De er ikke linjenumre i lokale F1-utkast eller ny kildeverifikasjon. Alle kildefilstier er relative til CellScaffold.

| Del av F4 | Fil:linje | Testnavn og om den ville fanget originalmangelen |
|---|---|---|
| Kald gjenstart av alle lagre | `Tests/AppTests/ManagedArtistImportTests.swift:257`, `:393`; `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:506`, `:541`, `:609` | `testVaultReloadAndGenericIssuanceDenied` gjenåpner bare hvelvet i active. `testInterruptedClaimHidesBothCellsAndCanResumeSameClaimant` bruker samme runtime/celleobjekter. **Nei**, de beviser ikke ny prosess med alle lagre lastet fra disk. Ingen konkret original restartfeil er påvist. |
| Virkelig ekstern klient og klientlokale private nøkler | `Tests/AppTests/ManagedArtistImportTests.swift:637`; `Documentation/Operations/Managed_Artist_Import_2026-09-28.md:46` | `ManagedArtistTestSigningBridge` er en lokal signeringsfixture, ikke en ekstern klienttest. **Nei**, den beviser ikke planlagt transport eller eierens lokale signering. Ingen ny test eller mutationstest er skrevet eller kjørt. |

Gjenstående krav fra Astra 2 og 5:

- Ny prosess etter mandatforbruk før issue, etter issue/under import, etter lagret transferring, etter hvert eierskifte og før/etter terminalt snapshot. Last mandat, issuance-hvelv, Publication og ArtistSales fra disk. Dokumenter forbrukt mandat uten issuance-record.
- Skjulte flater under ufullført overføring; tillatt retry fra samme mottaker; avvist annen mottaker/replay; nøyaktig én utstedelse; varig bindingsforbruk, key retirement og tombstone. Prosessrestart skal ikke omtales som strømbruddsgaranti.
- Ekstern klient med testidentitet over planlagt transport. Samme fulle kanoniske fingeravtrykk på begge enheter; eierens engangsbinding signert med egen nøkkel på egen enhet; token + binding + fersk signatur fra bundet kunstnernøkkel. Kontroller relevante serverlagre og transport-/diagnostikklogger for private-key-grensene.

Astra 5 er bindende: F1/F5/F6/F9 blokkerer merge, og F4/F7/F8 må også lukkes før AP6. Denne jobben lukker ingen av de sju funnene. Kjetils valg av godkjenningsløype endres ikke.

## Verifikasjonsgrense og videreføring

Kjørt: dokument-/statuskontroll, PR-metadata, ny kapasitetsvakt, byte-identisk arkivering og rapportering. Forrige F4-rapport og gjeldende F5–F9-rapport er lest; F4-avsnitt og relevante føringer i Astra 1, 2 og 5 er kontrollert. Enkelte samlede dokumentutskrifter ble avkortet; rapportene erklæres ikke fullstendig gjennomlest. FORMAALSSPEC, PLAN og driftsnotatet er ikke lest på nytt, siden oppdragets stoppregel inntraff ved inngangen. Lokale F1-kodeutkast er ikke faglig vurdert.

**Ikke kjørt:** isolert runtime, kald gjenstart, ekstern klient, signering eller privatnøkkelinspeksjon; `scripts/run_swift_bounded.sh … --disable-sandbox`, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh`; ny CI eller CI-venting. Ingen historisk grønn CI brukes som F4-bevis.

Ingen skript er skrevet under `HAVEN-Deploy/_handoff/SINDRE/`: arbeidet stoppet før sandbox-/transportmuligheten kunne undersøkes. Det er dermed ikke påvist at ekstern kjøring krever arbeid utenfor Codex-sandkassen. Strict-oppførsel, avvisningstester og skips/exclusions er ikke endret av denne jobben.

F1 og forgjengerjobben F5–F9 må fullføres, arbeidstreet må være rent på aktuell PR-head, og byggevakten må passere uten overstyring før F4 kan fortsette. Ingen ny nøkkelbeslutning etterspørres.

Bare denne rapporten, arkivkopien og evidensmappen er skrevet i PDD-mappen. Eksisterende WIP i dokumentrepoet er urørt; rapporten er lokal, ikke committet eller pushet. Læringsvurdering: ingen ny generell teknisk læring; kjent kapasitets-/avhengighetsblokkering, registrert med `haven_learn.py none`.
