STATUS: STOPPET — HVELV-F5-F9 er STOPPET og arbeidstreet har sporede endringer; byggevakten passerte med 56,5 GiB ledig; lokalt head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 29.09.2026, **runde 6**, `PDD_sindre-import-uten-bruker_2026-09-25.F4`. Ingen F4-retting eller nytt runtime-/transporttestbevis er levert. Ingen bygg, tester, commit, push, merge eller ny CI. **Ikke merge.**

## Bevaring

Forrige rapport, runde 5, er bevart **byte-identisk** som [HVELV-F4-runde5-20260929.md](HVELV-F4-runde5-20260929.md), SHA-256:

```text
d3c9c643d3415802b1cd126c3303b072581390db1c71a10e066ba0c50a87a63b
```

Tidligere arkiver er urørt. Runde-5-rapportens redegjørelse for manglende runde-4-arkiv er bevart der; intet slikt arkiv er konstruert.

## Stoppgrunn og ny kapasitetsmåling

[HVELV-F5-F9.md](HVELV-F5-F9.md):1 er fortsatt **STOPPET**, nå runde 6. Oppdragets «Er den STOPPET: stopp og rapporter» stopper F4 uavhengig av diskplass. Arbeidstreet har også seks sporede endringer og åtte usporede F1-utkast og oppfyller ikke kravet om rent arbeidstre.

Den uttrykkelig bestilte byggevakten ble kjørt **29.09 kl. 18:18:15 UTC / 20:18:15 Oslo**, fra `CellScaffold/_wt-forvaltet-import-20260926`:

```sh
env -u HAVEN_BUILD_RESERVE_GIB -u HAVEN_BUILD_MIN_FREE_GIB -u HAVEN_BUILD_MIN_FREE_PERCENT scripts/check_build_capacity.sh .
```

```text
Build capacity: 56.5 GiB free (6%); reserving 10 GiB leaves 46.5 GiB (5%).
Exit status: 0
```

**Vakten passerte denne gangen.** Vaktens bytes er identiske med lokal HEAD. De tre terskelvariablene ble fjernet fra prosessmiljøet slik at uendrede standardverdier gjaldt. Ingen overstyring, cacheendring eller rydding er utført. Arbeidstreets AGENTS.md omtaler 10 %, mens den uendrede vaktens faktiske prosentterskel er 5 %; ingen av dem er endret her.

`df -Pk` etter vakten målte **59 200 000 KiB tilgjengelig** av **971 298 980 KiB** på `/dev/disk3s5`. Dette er denne jobbens nye måling, ikke gjenbruk av rydderapporten eller forgjengerens tall. Årsaken til plassendringen er ikke undersøkt eller tilskrevet bane b. [Rå måling](evidence-hvelv-f4-runde6-20260929/build-capacity.txt) og [kommando, miljøavgrensning og exitkode](evidence-hvelv-f4-runde6-20260929/build-capacity.json).

## Bevart arbeidstre og revisjonsgrense

Lokal gren er `pdd/forvaltet-kunstnerimport`, head `b658ef53e14dccdb12009991e78b1b44d47dac8a`. Ekstern PR-head og CI er **ikke kontrollert på nytt i denne runden**, siden stoppreglene allerede var utløst. Runde 5 bekreftet samme PR-head; dette er historisk informasjon.

Sporede endringer ved inngangen:

- `.github/workflows/admin-scaffold-image.yml`
- `Documentation/Operations/Managed_Artist_Import_2026-09-28.md`
- `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift`
- `Tests/AppTests/ManagedArtistImportTests.swift`
- `ci/run-tests.sh`
- `ci/test-filter.txt`

De åtte usporede filene er navngitt i [entry-state.json](evidence-hvelv-f4-runde6-20260929/entry-state.json) og beskrevet som F1-utkast av forgjengerjobben. Ingen egne usporede testrester vises i Git-status. Ingenting er flyttet til `_to_delete/`, slettet, stashet eller overskrevet i arbeidstreet. Status og SHA-256 for alle 14 arbeidsfiler er kontrollert uendret ved avslutning; se [preservation-check.json](evidence-hvelv-f4-runde6-20260929/preservation-check.json).

## F4: fortsatt åpent

Fil:linje nedenfor er Astras kildeankre på vurdert PR-head, videreført fra [ASTRA-HVELV-5.md](ASTRA-HVELV-5.md):92 og [ASTRA-HVELV-2.md](ASTRA-HVELV-2.md):131–137. Dette er ikke ny kildeverifikasjon eller linjenumre i lokale F1-utkast. Kildestiene er relative til CellScaffold.

| Del av F4 | Fil:linje | Testnavn og om den ville fanget originalmangelen |
|---|---|---|
| Kald gjenstart av alle lagre | `Tests/AppTests/ManagedArtistImportTests.swift:257`, `:393`; `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:506`, `:541`, `:609` | `testVaultReloadAndGenericIssuanceDenied` gjenåpner bare hvelvet i active. `testInterruptedClaimHidesBothCellsAndCanResumeSameClaimant` fortsetter med samme runtime/celleobjekter. **Nei**, de beviser ikke ny prosess med alle lagre lastet fra disk. Ingen konkret original restartfeil er påvist. |
| Virkelig ekstern klient og klientlokale private nøkler | `Tests/AppTests/ManagedArtistImportTests.swift:637`; `Documentation/Operations/Managed_Artist_Import_2026-09-28.md:46` | `ManagedArtistTestSigningBridge` er en lokal signeringsfixture, ikke en ekstern klienttest. **Nei**, den beviser ikke planlagt transport eller eierens lokale signering. Ingen ny test eller mutationstest er skrevet eller kjørt. |

Gjenstående bindende krav fra Astra 1, 2 og 5:

- Ny prosess etter mandatforbruk før issue, etter issue/under import, etter lagret transferring, etter hvert eierskifte og før/etter terminalt snapshot. Last mandat, issuance-hvelv, Publication og ArtistSales fra disk. Dokumenter forbrukt mandat uten issuance-record.
- Skjulte flater under ufullført overføring; samme mottakers retry; avvist annen mottaker/replay; én utstedelse; varig bindingsforbruk, key retirement og tombstone. Skill prosessrestart fra strømbruddsgaranti.
- Testidentiteter over planlagt ekstern transport, samme fulle kanoniske fingeravtrykk på begge enheter, eierens engangsbinding signert med egen nøkkel på egen enhet og token + binding + fersk signatur fra bundet kunstnernøkkel. Kontroller private-key-grensene i relevante serverlagre og transport-/diagnostikklogger.

Astra 5 er bindende: F1/F5/F6/F9 blokkerer merge; F4/F7/F8 må også lukkes før AP6. Denne jobben lukker ingen funn. Kjetils godkjenningsløype og kodeankerbeslutning endres ikke.

## Verifikasjonsgrense og videreføring

Kjørt: dokument-/statuskontroll, ny kapasitetsvakt, byte-identisk arkivering og bevaringskontroll. Gjeldende F5–F9 og forrige F4 er lest; F4-avsnitt og relevante føringer i Astra 1, 2 og 5 er kontrollert i eksplisitte utdrag. Den første samlede utskriften ble avkortet; rapportene erklæres ikke fullstendig gjennomlest. FORMAALSSPEC, PLAN og driftsnotatet er ikke lest på nytt etter at stoppreglene inntraff. Lokale F1-kodeutkast er ikke faglig vurdert.

**Ikke kjørt:** isolert runtime, kald gjenstart, ekstern klient, signering eller privatnøkkelinspeksjon; `scripts/run_swift_bounded.sh … --disable-sandbox`, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh`; ny CI eller CI-venting. Historisk grønn CI brukes ikke som F4-bevis.

Ingen skript er skrevet under `HAVEN-Deploy/_handoff/SINDRE/`: stoppreglene inntraff før sandbox-/transportmuligheten ble undersøkt. Det er ikke påvist at ekstern kjøring krever arbeid utenfor Codex-sandkassen. Sentralhvelvets strict-oppførsel, avvisningstester og skips/exclusions er ikke endret av denne jobben.

F1 og forgjengerjobben F5–F9 må ferdigstilles og handoff oppdateres; arbeidstreet må være rent på aktuell PR-head før F4 fortsetter. Kapasitetsmålingen er et øyeblikksbilde, og vakten skal kjøres igjen før et fremtidig bygg. Ingen ny nøkkelbeslutning etterspørres.

Bare denne rapporten, runde-5-arkivet og evidensmappen er skrevet i PDD-mappen. Rapporten er lokal, ikke committet eller pushet. Læringsvurdering: ingen ny generell læring; den nye målingen og kjent avhengighets-/WIP-blokkering er dokumentert her. `haven_learn.py none --reason ...` er kjørt og registrert i den uversjonerte læringsloggen.
