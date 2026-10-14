STATUS: LEVERT — head b658ef53e14dccdb12009991e78b1b44d47dac8a, CI grønn (https://github.com/Digipomps/CellScaffold/actions/runs/36396748001)

Codex, 28.09.2026, for Kjetil og Losen. **F2 er implementert; F3 er dokumentert med metodevis kjøring på begge bestilte revisjoner. Ingen merge.** F1 er urørt og venter fortsatt på Kjetils valg; F4 gjenstår før AP6.

Arbeidsreferanse `PDD_sindre-import-uten-bruker_2026-09-25.F2-F3`; utførende/eier Codex, integrator Kjetil/Losen. Arbeidstre `CellScaffold/_wt-forvaltet-import-20260926`, gren `pdd/forvaltet-kunstnerimport`, [PR #270](https://github.com/Digipomps/CellScaffold/pull/270). Starttreet var rent på `9209ce100446866c9869550ca53273665fde4304`; GitHub bekreftet denne headen og base `feec23725321320ab00f0e7f7bf728b775869ec7`.

[Commit b658ef53](https://github.com/Digipomps/CellScaffold/commit/b658ef53e14dccdb12009991e78b1b44d47dac8a) er pushet og remote-SHA er lest tilbake. Committen har PDD-identifikatoren, F2, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` og `Claude-Session: https://claude.ai/code/session_011CHU13qBKbb5szsQQo53rW`. Eksisterende Git-konfigurasjon setter forfatter/committer til Claude; arbeidet her er utført av Codex.

**F2 — implementasjon og testbevis**

Filreferanser gjelder levert head. `V` nedenfor er `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift`; `S` er `Sources/App/Support/SecureRuntimeIdentityManifestFile.swift`. Lagringstestene er i `Tests/AppTests/ManagedArtistVaultFileTests.swift` (`T`); integrasjonstestene i `Tests/AppTests/ManagedArtistImportTests.swift` (`I`). Linjene kan åpnes på [V](https://github.com/Digipomps/CellScaffold/blob/b658ef53e14dccdb12009991e78b1b44d47dac8a/Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift), [S](https://github.com/Digipomps/CellScaffold/blob/b658ef53e14dccdb12009991e78b1b44d47dac8a/Sources/App/Support/SecureRuntimeIdentityManifestFile.swift), [T](https://github.com/Digipomps/CellScaffold/blob/b658ef53e14dccdb12009991e78b1b44d47dac8a/Tests/AppTests/ManagedArtistVaultFileTests.swift), [I](https://github.com/Digipomps/CellScaffold/blob/b658ef53e14dccdb12009991e78b1b44d47dac8a/Tests/AppTests/ManagedArtistImportTests.swift).

| Krav | Fil:linje / oppførsel | Test og testfil:linje (lokalt PASS) |
|---|---|---|
| Betrodd kjede helt fra `/`, inkludert konfigurert rot | V:107; S:223. Hvert åpent katalogledd krever UID root/prosess og ingen gruppe-/andre-skrivebit. Ingen sticky-unntak. | T:35 `testRejectsWritableAncestorRootAndStickyTemporaryDirectory`; T:55 `testWritableAncestorDuringOperationLatchesUnavailable` |
| ACL uten fremmed skrive-/slette-/omdøpingsrett | S:235, S:329; samme descriptor-kontroll brukes på forfedre, rot, hvelvkatalog, lease og snapshot. Darwin avviser konservativt alle muterende grant-ACE-er, også til root/eier. Deny/read-only kan aksepteres for utstedelseshvelvet. Linux gjenbruker hele xattr-listesjekken og avviser også default/access POSIX ACL. | T:171 `testRejectsMutatingACLOnAncestorVaultLeaseAndSnapshot`; T:192 `testRejectsDeleteAndRenameOnlyACLGrants` (Darwin); T:201 `testDenyOnlyAncestorACLIsSafeButManifestStillRejectsAnyACL` (Darwin) |
| Hvelvkatalog 0700; lease/snapshot regulær, 0600, én lenke og trygg eier | V:42, V:45, V:149; felles S:223. Nye pending-filer kontrolleres også (V:78, V:93). | T:128 `testRejectsWrongModesOnVaultLeaseAndSnapshot`; T:142 `testSharedOwnerCheckRejectsAnUntrustedUIDAndAcceptsRoot` |
| Hardlink avvises ved åpning og under drift | S:234, V:135, V:149 | T:109 `testRejectsHardlinkedLeaseAndSnapshotAtOpenAndDuringOperation`; testen kontrollerer også at feilende init slipper leasen |
| Konfigurert sti må fortsatt vise til åpent katalog-deskriptor | V:126 sammenligner device/inode; gjenåpner hele kjeden uten symlink-følging. | T:68 `testRenamedVaultAndReplacementAtConfiguredPathFailClosed`; T:83 `testRenamedAncestorFailsEvenThoughHeldDirectoryStillExists` |
| `.lease` må være inode-en som faktisk er låst | V:132–137 sammenligner navngitt og låst device/inode. | T:94 `testReplacedLeaseIsNotTheLockedInodeAndStaysUnavailableAfterRestoration` (den gamle inode-en beholdes med én lenke, så dette tester mer enn lenketall) |
| Avvik → `unavailable`, varig lukket instans | V:62, V:71, V:140. Kontroll før/etter lesing og ved skrivecommit/readback; alle operasjonsfeil setter latch. Ingen ny operasjon tillates etter at avvik er observert, heller ikke etter gjenopprettet sti/lease. | T:55, T:83, T:94; I:294 `testStorageNamespaceDriftMakesImportedContentUnavailable` kontrollerer record-feil, synlighet, redigering og skjulte verk/previews |
| Gyldig beskyttet rot virker og gjenlastes | V:29, V:71. Låsing, AES-GCM, fsync/rename/readback er beholdt. | T:17 `testProtectedRootWritesReloadsAndKeepsExclusiveLease`; I:257 `testVaultReloadAndGenericIssuanceDenied`; I:276 `testVaultRejectsSecondWriterWrongKeySymlinkAndDrift` |
| Gjenbruk uten svekking av sentral strict/manifest | S:223 gjenbruker metadata, ACL og xattr-kontroller. Manifestets kall ved S:86/S:264 bruker fortsatt standarden «ingen ACL», samme UID/GID og 0700/0400. Provisioner/writer, configure og eksisterende strict-testassertions er uendret. | I:115 `testCentralVaultRemainsStrictAndByteIdenticalDuringImportAndClaim`; T:201 og F3-tabellen nedenfor |

På macOS kjører UID-negativene den faktiske descriptor-validatoren med en annen forventet prosess-UID, fordi denne jobben ikke har root-rett til å chown til en annen bruker. Root-grenen i samme test gjør ekte `fchown` og kontrollerer også hvelvets init ved fremmed eier; Samme metode er også PASS i Linux-CI; root-grenen utføres når testprosessen har effektiv UID 0. macOS-spesifikke ACL-tester er kompilert for Darwin; Linux bruker ekte POSIX ACL-xattrs, inkludert default ACL som ikke trenger å endre katalogens modus.

Beskyttet ressurs er det separate utstedelseshvelvets lagringsnavnerom og lås. Root/prosess-UID er OS-tillitsgrensen. Mandat-, proof-, utstedelses- og claim-/overtakelseslogikken etter lagringsklassen er byte-identisk med start-head; F1 er ikke endret. [Scope-bevis](evidence-hvelv-f2/scope-invariants.json). Ingen nye rettigheter, payloadfelter, publiserte persondata eller nøkkeloverføring. Rot/prosess-kompromiss, backup-rollback og atomisitet over flere postlagre er fortsatt separate drifts-/F4-grenser.

**F3 — samme tester, gyldig testrot, ingen regelendring**

Det isolerte arbeidstreet `CellScaffold/_wt-hvelv-f3-verification` ble først bygget på `9209ce10`, deretter på `feec2372`. Begge hadde identiske produksjonsfiler og testassertions fra den respektive revisjonen. Bare de to testfixturenes katalogbase ble flyttet til en beskyttet 0700-katalog under arbeidstreet. Den samme [firelinjers fixture-patchen](evidence-hvelv-f2/f3-fixture-root-only.patch) ble brukt på begge revisjoner, og ved F2-regresjonen. Ingen skips/exclusions eller avvisningsregler ble endret. Fixturendringene ble fjernet før commit; isolert arbeidstre er igjen rent på basen.

[Kildehashene](evidence-hvelv-f2/f3-source-evidence.json) dokumenterer at reader, writer og begge testfilene var identiske mellom base og opprinnelig head. Resultater: [PR-head](evidence-hvelv-f2/f3-head-protected-root.log), [base](evidence-hvelv-f2/f3-base-protected-root.log), [F2-regresjon](evidence-hvelv-f2/f2-regression.log), [maskinlesbar metodeoversikt](evidence-hvelv-f2/method-results.json).

De første to metodene tilhører `CellScaffoldRuntimeIdentityProvisionerTests`; de øvrige tilhører `SecureRuntimeIdentityManifestFileTests`.

| Metode | PR-head `9209ce10` | Base `feec2372` | Levert F2-kode |
|---|---|---|---|
| `testWriterRejectsExtendedAttributesOnExistingManifest` | PASS | PASS | PASS |
| `testWriterRejectsOverwriteWithoutExactOldDigestAndUses0600` | PASS | PASS | PASS |
| `testErrorsNeverContainPathOrManifestBytes` | PASS | PASS | PASS |
| `testMissingFileHasStableSanitizedReason` | PASS | PASS | PASS |
| `testPathReplacementIsDetectedByStableDescriptorMetadata` | PASS | PASS | PASS |
| `testReadsExactContainerOwned0700And0400File` | PASS | PASS | PASS |
| `testRejects0600RuntimeFileAndNonRegularFinalComponents` | PASS | PASS | PASS |
| `testRejectsEmptyAndOversizedFile` | PASS | PASS | PASS |
| `testRejectsFinalAndAncestorSymlinks` | PASS | PASS | PASS |
| `testRejectsHardlinkAndExtendedAttribute` | PASS | PASS | PASS |
| `testRejectsParentExtendedAttribute` | PASS | PASS | PASS |
| `testRejectsSameInodeMutationBetweenStableReads` | PASS | PASS | PASS |
| `testRejectsWrongParentModeOwnerAndGroupExpectations` | PASS | PASS | PASS |

Hver av de bestilte F3-kjøringene: **13 tester, 0 feil**. F2-kolonnen er samme produksjonskode som committen; fixture-patchen var kun lokal under kjøringen.

Årsak til de tidligere røde testene er nå målt:

- Skriverens to metoder: original `NSTemporaryDirectory().resolvingSymlinksInPath()` ga fremdeles `/var/folders/...`. Descriptor-traversering av `var` med `O_NOFOLLOW | O_DIRECTORY` feilet med errno 20 (`ENOTDIR`). Dermed feilet `readCanonicalManifest`/`writeCanonicalManifest` i `openDirectory` (provisioner:878/:923), før de tiltenkte assertions. Ingen regel skal akseptere denne symlinken.
- Leserens `testReadsExactContainerOwned0700And0400File` og `testRejectsEmptyAndOversizedFile`: original fixture under `/private/tmp` hadde katalog-GID **0** og fil-GID **20**. Eksakt GID-kontroll i `SecureRuntimeIdentityManifestFile.validateFileMetadata` avviste korrekt med `manifestMetadataUnsafe`, før innhold/size-kontroll. Den andre metoden ga to assertion-feil fordi den ventet `manifestNoncanonical`/`manifestTooLarge`.
- Første kontroll med originalfixturer og bare TMPDIR var fortsatt rød: 4 av 13 metoder, 5 feil totalt (3 unexpected). [Logg](evidence-hvelv-f2/f3-original-head.log). Separat testlokal diagnose målte sti/syscall-feil og UID/GID/modus/xattrs: [diagnostikk](evidence-hvelv-f2/f3-root-diagnostics.log), [midlertidig diagnosekode](evidence-hvelv-f2/f3-diagnostic-overlay.patch). Diagnosen endret ingen produksjonsregler. Flyttet fixture-base fjerner begge feilforutsetningene og lar samtlige assertions kjøres.

OS-detaljene er også kontrollert mot Apples [ACL-implementasjon](https://raw.githubusercontent.com/apple-oss-distributions/Libc/main/posix1e/acl_file.c) og [ACL-iterator](https://raw.githubusercontent.com/apple-oss-distributions/Libc/main/posix1e/acl_entry.c); Linux ACL-xattrs er beskrevet i [kernel-dokumentasjonen](https://www.kernel.org/doc/html/v4.19/filesystems/ext4/ondisk/index.html). Resultatene over er fra faktiske lokale kjøringer, ikke utledet fra grønn Linux-CI.

**Bygg og porter**

Alle vertskjøringer brukte `scripts/run_swift_bounded.sh … --disable-sandbox`, stabil cachefamilie `HAVEN_SWIFTPM_CACHE_KEY=cellscaffold-managed-artist-import`, to jobber og `HAVEN_BUILD_MIN_FREE_PERCENT=10`. Skriptets kapasitetssjekk kjørte hver gang. Ca. 112–113 GiB ledig og >10 % etter 10-GiB-reserve ga grønn vakt. Aktiv samlet cache var ca. 12,6 GiB, over myk 12-GiB-grense; dette ble vurdert før videre bygg. Ingen senket terskel, ny scratch-path, manuell cache-sletting eller lokal package-override.

| Kontroll | Resultat / bevis |
|---|---|
| Bounded `build --disable-sandbox` på F2 | PASS / exit 0, [logg](evidence-hvelv-f2/f2-build.log) |
| Bounded `test --disable-sandbox --filter 'ManagedArtistImportTests\|ManagedArtistVaultFileTests\|CellScaffoldRuntimeIdentityRegistryTests\|CellScaffoldRuntimeIdentityManifestTests\|CellScaffoldRuntimeIdentityProvisionerTests\|SecureRuntimeIdentityManifestFileTests'` | **114/114 PASS**, [logg](evidence-hvelv-f2/f2-regression.log): 24 + 12 + 21 + 15 + 31 + 11 |
| F3 original PR-head og base | **13/13 PASS hver**, metodevis ovenfor |
| `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh` | PASS / exit 0, 23 eksisterende baseline-oppføringer, [logg](evidence-hvelv-f2/value-literals.log) |
| `ci/test-suite-coverage.sh` | PASS / exit 0, 344 suiter, 324 dekket, ingen ny exclusion; [logg](evidence-hvelv-f2/suite-coverage.log) |
| `git diff --check` | PASS |
| Package.swift/Package.resolved, configure, provisioner, exclusions/skips | Uendret; [hashkontroll](evidence-hvelv-f2/scope-invariants.json) |

Ny lagringssuite er tatt inn i `ci/test-filter.txt:472`. Driftskrav og F3-årsak er oppdatert i `Documentation/Operations/Managed_Artist_Import_2026-09-28.md:35`.

**CI — grønn på eksakt levert head**

[AdminScaffold immutable images, run 36396748001](https://github.com/Digipomps/CellScaffold/actions/runs/36396748001) er **completed / success**, `headSha=b658ef53e14dccdb12009991e78b1b44d47dac8a`. Start `2026-09-28T08:20:11Z`, ferdig/sist oppdatert `09:12:54Z`: **52 min 43 sek**, innen 60-minuttersgrensen. Native `gh run watch --exit-status` returnerte 0; ingen timeout eller omkjøring. [Terminal JSON med jobb/steg](evidence-hvelv-f2/ci-result.json), [watch-logg](evidence-hvelv-f2/ci-watch.log), [normalisert jobblogg](evidence-hvelv-f2/ci-focused-job.log).

Faktiske testlinjer i Linux-jobben viser **24/24 `ManagedArtistImportTests` og 10/10 `ManagedArtistVaultFileTests` PASS**, inkludert namespace-drift, ACL, hardlink, modus og UID-testen. De to ekstra Darwin-ACL-metodene inngår i den lokale 12/12-kjøringen, ikke Linux-kompileringen. [Uttrukne testlinjer](evidence-hvelv-f2/ci-managed-tests.log), [antall](evidence-hvelv-f2/ci-managed-counts.json). F3-resultatene er fortsatt de eksplisitte lokale metodekjøringene ovenfor; CI-filteret er ikke utvidet til å omfatte de to gamle writer-metodene eller den ekskluderte reader-suiten.

Alle kjørte porter i hovedjobben er grønne: bygg av alle mål, literals, testdekning, fokuserte Swift-tester, gjentatte bridge-prosesser, shell/package-kontroll, tilgjengelighet/responsivitet, Thursday-demo og document live collaboration. `Publish signed-source image pair` er **skipped**. Notify PyCellProtocol er også success. [Siste PR-status](evidence-hvelv-f2/final-pr-state.json) bekrefter **OPEN**, samme head og base `feec2372`. Ingen merge, image-publisering eller utrulling er utført av denne jobben.

**Ikke kjørt / gjenstående grenser**

- Hele vertens samling av 344 testsuiter er ikke kjørt lokalt; den målrettede regresjonen er 114 tester. F3 er et selvstendig lokalt metodebevis; de eksisterende Linux-exclusions/enkeltmetodefiltrene er uendret.
- Produksjonsrotens faktiske eier, moduser, ACL-er, mounts eller backupoppsett er ikke inspisert/provisjonert. Dette må være i orden før AP6.
- F1 mottakerbinding, F4 kald gjenstart ved alle lagringsgrenser og virkelig ekstern klient, strømbrudd, staging/prod, produksjonsmandat, virkelig kunstnerovertakelse og GUI-/bildeparitet er ikke utført i denne jobben.
- Ingen merge. Kodearbeidstreet har ingen gjenværende tracked endringer; bare taskens `.hvelv-test-root/` med tomme midlertidige marker-/låsefiler er untracked. Det isolerte F3-arbeidstreet er rent på `feec2372`.
- Docs-repoet hadde betydelig eksisterende WIP og hele PDD-mappen untracked ved start. Denne rapporten og `evidence-hvelv-f2/` er lokale handoff-artefakter; annen WIP er urørt. Ingen docs-repo-commit er laget.
