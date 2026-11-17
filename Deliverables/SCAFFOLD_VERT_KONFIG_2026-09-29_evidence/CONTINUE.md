# Fortsett verifikasjon etter diskplass er frigjort

Status: WIP-kode er committet og isolerte lesertester er grønne. Ingen push/deploy.
Originale dirty arbeidskopier er beholdt. Rapporten er ikke en full aksept.

Kandidat-worktrees: `.scaffold-instance-20260929/{Binding,CellScaffold,CellProtocolDocuments}`.
Branche: `codex/scaffold-instance-config-20260929`.

## Før/etter-gate som gjenstår

1. La `CellScaffold/scripts/check_build_capacity.sh` passere med gjeldende standardgrenser.
   Det ble bedt om minst 5 GiB frigjort plass; ingen svar/autorisasjon til rydding forelå.
2. Opprett nye rene baseline-worktrees fra eksakte baser i rapporten, med samme
   CellProtocol, DiMyMint og DiMyMicropayments 2026.9.3-worktrees som kandidaten.
   Ikke bygg fra de opprinnelige dirty arbeidskopiene og ikke gjett pakkeversjoner.
3. Kjør baseline med `scripts/run_tests_isolated.sh --disable-sandbox --jobs 4`.
   Sett `CELLPROTOCOL_LOCAL_PACKAGE_PATH`, `DIMYMINT_LOCAL_PACKAGE_PATH` og
   `DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH` til disse worktreene, og
   `HAVEN_SWIFTPM_RUNNER` til den eksplisitte CellProtocol-runneren.
   Bruk `SWIFTPM_MAX_CONCURRENT_OPERATIONS=1` og en stabil oppgavespesifikk cache-key.
   Sett begge modulcachevariablene til skrivbar sti før start; runneren setter sin
   administrerte modulcache videre. Behold baseline-logg og exitkode.
4. Kjør samme fulle CellScaffold-suite på kandidat. Sammenlign faktiske feilede
   testnavn og siste totalsummer. Tre Keychain-feil er oppgitt av Kjetil, men ble
   aldri observert her: ingen tester nådde start i full baseline. Gamle feil stopper
   ikke; nye røde må undersøkes mot gjentatt ren base.
5. Bygg/test Binding med Xcode-skjema HAVEN, macOS/arm64 og separat DerivedData.
   Kjør BindingTests på ren base og kandidat med samme lokale CellProtocol. Ikke
   endre plist-pins, signerte entitlements eller de opprinnelige brukerarbeidskopiene.
6. Kjør bare `ScaffoldInstanceConsumerTests` i egne nye testprosesser med en JSON-fil
   hvis scaffoldOrigin er `https://instance.example.test`, og
   `INSTANCE_TEST_EXPECTED_ORIGIN=https://instance.example.test`. Dette tester de
   virkelige katalog-/HTTP-konsumentene; de isolerte lesertestene beviser ikke dem.
   Standardregresjonen må kjøres uten en alternativ installasjonskonfigurasjon.
7. Oppdater rapportens faktiske resultater og WIP-status, commit videre på samme
   grener; ikke push.

## Allerede utført

- Fullt originalt og rent hostinventar, alle kilde/policy/fixture-grenser klassifisert.
- Seks isolerte XCTest-metoder mot produksjonsleseren, 0 feil.
- To faktiske Swift-interpreter-prosesslivsløp: gammel snapshot ved filendring,
  ny vert ved ny PID; swarm beholdt. Kildehash står i foundation-reader-tests.log.
- Typekontroll av leseren med Binding sin MainActor-standard, exit 0.
- 36 endrede Swift-filer syntaksparset, 0 feil. Dette er ikke appkompilering.
- Leser-byteparitet og ingen uklassifiserte hostselektorer i appens Swift-kilder.

## Avgrenset læring

Foundation Data(contentsOf:) ga NSError i NSCocoaErrorDomain kode 260 ved manglende
fil, og `error is CocoaError` var false. En CocoaError-cast gjorde staging-standarden
utilgjengelig. Eksakt NSError domain/code-sjekk er nå regresjonstestet. Dette ble
rettet før commit; det er ikke en gammel Keychain-baselinefeil.
