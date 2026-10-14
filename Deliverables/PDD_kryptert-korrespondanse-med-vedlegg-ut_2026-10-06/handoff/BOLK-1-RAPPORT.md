| Steg | Utfall | Bevis (kommando, exit-kode, antall tester) |
|---|---|---|
| Baseline, korrigert fixture | Rød som forventet: 5 feilede testtilfeller, 10 feilassertjoner | b47: `bash HAVEN-Deploy/_handoff/KORR-UT/wp-korr-admission-focused.sh red-final`; exit 1; 15 tester |
| Endret kode, første prøve | Grønn | b48: samme skript, `green`; exit 0; 15 tester |
| Endret kode, endelig prøve | Grønn | b49: samme skript, `green-final`; exit 0; 18 tester |
| Full pakke | Grønn: 1577 bestått, 0 feilet, 5 eksisterende skips | c41: `bash HAVEN-Deploy/_handoff/KORR-UT/wp-korr-admission-full.sh`; bygg exit 0; test exit 0 |
| Fjernforbindelse og Touch ID/passord hver gang | Ikke vist | Ingen nettverks-/maskin-/dialogtest kjørt |

# Bolk 1 — rapport

Status: lokal prøve ferdig, klar for korrespondanse-trådens og en uavhengig lesers gjennomgang. Ingen arkitekturanbefaling. Rapporten er ikke uavhengig gjennomgått.

## 1. Grunnlag og leveranse

Gren `codex/korr-innslipp-proeve-20261007`, lokal commit `8dfbd3f0787fcd64a32b52abad9518885ebba28e`.
Grunnlag: lokalt `origin/main` = `68069b697a22246ffb4d8add5ecc42e3d0d5ba38`, tag `2026.9.5`.
Arbeidstre `_worktrees/cp-korr-innslipp-proeve-20261007`, låst mot prune. Hovedarbeidstreet og a35 er ikke endret.
Ingen fetch, push, PR, merge, tag, pinnendring eller deploy fra denne jobben.

`git diff origin/main --stat`:

```text
 Documentation/ExternalAgreementAdmissionProbe.md   |  38 ++++
 Sources/CellBase/Agreement/Contract.swift          |  16 +-
 .../CellBase/Cells/GeneralCell/GeneralCell.swift   |  57 +++++
 .../ExternalAgreementAdmissionTests.swift          | 231 +++++++++++++++++++++
 4 files changed, 338 insertions(+), 4 deletions(-)
```

`handoff/BOLK-1-ENDRING.patch` er skrevet med `git diff origin/main --binary` fra prøvearbeidstreet. Stiene i patchen er relative til CellProtocol. Ingen eksisterende test er fjernet eller endret.

## 2. Punkt 1 — kan det gjøres?

**Kjørt:** A signerer `Contract.signed(... targetCellUUID: celle.uuid)` med test-eierens nøkkellager. JSON encode/decode overfører de signerte bytene. S legger den dekodede kontrakten fram gjennom `GeneralCell.acceptExternallySignedAgreement(_:for:)`.
B huser en testcelle med kun eierens offentlige identitet og et eget tomt nøkkellager; testen krever at B ikke finner eieridentiteten og ikke kan signere som eieren. S har et tredje nøkkellager. B installerer offentlige medlemsdeskriptorer, ikke S sitt nøkkellager.
En GET av `name` lykkes etter innslipp. En SET av samme felt er avvist og navnet er uendret. Malen gir bare lesing.

Dette er separate nøkkellagerkontekster i én testprosess. To fysiske maskiner eller prosesser er ikke kjørt.
Handlerne installeres gjennom CellProtocols eksisterende runtime-binding-scope; det gir ingen medlems-/tilgangsbypass. `debugValidateAccessForEverything` må være av, og hver tests setup feiler hvis det er på. Ingen ekte identiteter eller nøkler brukes.

Baselineproduksjonskoden var uendret. Fordi mottaksfunksjonen ikke finnes der, hadde testfilen en uttrykkelig merket, testlokal adapter som alltid returnerte `.rejected`. Den er fjernet i den leverte testen. Baselinens grønne avvisningstester mot adapteren er ikke bevis på implementert importkontroll. Rød cellebindingskontroll brukte den ekte eksisterende signaturverifikasjonen.

Rå testresultatlinjer, valgt uendret fra b47 og b49:

```text
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testExternalOwnerSignatureAdmitsSubjectWithoutOwnerKeyInHostAndRejectsWrite]' failed (3.306 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testExternalOwnerSignatureAdmitsSubjectWithoutOwnerKeyInHostAndRejectsWrite]' passed (0.006 seconds).
```

## 3. Punkt 2 — minste endring som ble prøvd

**Kjørt:** 18 tester etter endringen. **Lest i kode:** følgende endringer på den lokale commiten:

- `Sources/CellBase/Agreement/Contract.swift:22`: avledet semantikk for cellebundet variant; eksisterende v1 beholdes når bindingen er nil.
- Samme fil, linje 34, 75 og 88: valgfri `targetCellUUID` i Contract, wire-koding og SigningPayload.
- `Contract.signed`, linje 91, og `signingData`, linje 221: signaturen dekker cellebindingen når den er gitt. Gamle kall får nil og beholder eksisterende payload.
- `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:1455`, `acceptExternallySignedAgreement`: fryser framlagt Contract gjennom JSON før await; krever celle, eier, subjekt, domene, signatur, aktiv tid, subjektets nøkkelbevis, malens grants/varighet/policy/vilkår og oppfylte vilkår. Installerer med eksisterende `auditor.installAuthorization`.
- Samme fil, `authorizationContracts(for:)`, linje 2251/2257: også senere tilgang avviser en cellebundet Contract med annen cellebinding. Eksisterende lokale kontrakter med nil endres ikke.

Ingen brorute eller ny innslippspolicy er lagt til. `.ownerApprovalRequired` er uendret. Eierens gyldige signatur er godkjenningen på den nye importveien. Dette viser denne ene endringen; det er ikke en påstand om at alle mulige mindre endringer er undersøkt.

## 4. Punkt 3 — det som fortsatt avvises

**Kjørt:** én test per a–h, med separate tester for begge tids- og malgrensene. Før avvisning starter testene med kryptografisk gyldige JSON-overførte kontrakter; feilutstederen har eget nøkkellager og eierens UUID, men annen nøkkel. Ingen avvisning får etterlate et medlem eller en kontrakt.

| Tilfelle | Test |
|---|---|
| a, annen nøkkel med eierens UUID | `testRejectsSignatureFromOtherKeyWithOwnerUUID` |
| b, annen celle med samme eier, mal og domene | `testRejectsOwnerSignatureForOtherCellWithSameTemplateAndDomain` |
| c, utløpt | `testRejectsExpiredSignature` |
| c, ikke gyldig ennå | `testRejectsNotYetValidSignature` |
| d, subjekt uten nøkkelbevis | `testRejectsSubjectWithoutPrivateKeyProof` |
| e, grant utenfor mal | `testRejectsGrantOutsideTemplate` |
| e, varighet over mal | `testRejectsDurationBeyondTemplate` |
| f, tredjepart legger fram S sin kontrakt og prøver å lese | `testRejectsThirdIdentityPresentingSubjectsContractAndReading` |
| g, to framlegginger gir ett medlem og én kontrakt | `testRepeatedPresentationDoesNotGrowMembersOrContracts` |
| h, lokal `addAgreement` uten eiernøkkel | `testRejectsHostAddAgreementWithoutOwnerPrivateKey` |

Cellebindingen er `targetCellUUID`, dekket av utstedersignaturen og kontrollert mot cellens UUID. På grunnlaget har Contract ingen egen, obligatorisk cellebinding. Prøvemalen har ingen policybinding eller vilkår som binder den til en bestemt celle. En egen test endrer bare wire-feltet og krever at signaturkontrollen feiler.

Rå b47-resultatlinjer for punkt 3 (adapterbegrensningen over gjelder):

```text
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsChangedCellBindingAfterWireRoundTrip]' failed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsDurationBeyondTemplate]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsExpiredSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsGrantOutsideTemplate]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsHostAddAgreementWithoutOwnerPrivateKey]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsNotYetValidSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsOwnerSignatureForOtherCellWithSameTemplateAndDomain]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsSignatureFromOtherKeyWithOwnerUUID]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsSubjectWithoutPrivateKeyProof]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsThirdIdentityPresentingSubjectsContractAndReading]' failed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRepeatedPresentationDoesNotGrowMembersOrContracts]' failed (0.001 seconds).
```

Rå b49-resultatlinjer for punkt 3 og de ekstra kontrollene:

```text
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsChangedCellBindingAfterWireRoundTrip]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsConditionsDifferentFromCurrentTemplate]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsDurationBeyondTemplate]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsExpiredSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsGrantOutsideTemplate]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsHostAddAgreementWithoutOwnerPrivateKey]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsNotYetValidSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsOwnerSignatureForOtherCellWithSameTemplateAndDomain]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsOwnerSignatureForWrongDomain]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsSignatureFromOtherKeyWithOwnerUUID]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsSubjectWithoutPrivateKeyProof]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsThirdIdentityPresentingSubjectsContractAndReading]' passed (0.002 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRejectsUnboundLegacyContractWhileKeepingItsSignatureValid]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testRepeatedPresentationDoesNotGrowMembersOrContracts]' passed (0.002 seconds).
```

## 5. Punkt 4 — subjektets bevis over en forbindelse

**Lest i kode:** `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`, `checkIdentityOrigin(_:against:)`, linje 2336, lager en ressurs-/domene-/identitetsbundet utfordring og ber identitetens vault signere; offentlig deskriptor alene avvises.
`Sources/CellBase/Identity/BridgeIdentityVault.swift:70`, `signMessageForIdentity`, validerer utfordringen og sender den gjennom `cloudBridge.signMessageForIdentity`.
`Sources/CellBase/Cells/Bridging/BridgeBase.swift:1102`, `signMessageForIdentity`, krever klar kanal og kontrollert signeringskontekst. `consumeCommand` rundt linje 1553 krever en lokal signeringstillatelse, at identiteten finnes i det lokale nøkkellageret, rett kanal/generasjon/frister og ikke-gjenbrukt utfordring før nøkkellageret signerer.
`Sources/CellBase/Cells/Bridging/BridgeIdentityProofAuthorization.swift:52`, `begin`, oppretter tillatelsen bare for en aktiv lokalt startet operasjon med den lokale, nøkkelbærende identiteten; `permit`, linje 75, krever matching scope og `checkIdentityOrigin`/`GeneralCell`.

**Kjørt:** en offentlig kopi uten proxy kan ikke bevise kontroll; S med eget lokalt nøkkellager kan. Rå b49:

```text
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testPublicRemoteSubjectWithoutSigningProxyCannotProveControl]' passed (0.000 seconds).
```

**Ikke vist:** S i annen prosess over faktisk forbindelse. Den nye direkte mottaksfunksjonen er ikke en eksisterende BridgeCommand. Ingen ruting er bygget i denne bolken. Om den eksisterende klientoperasjonen kan autorisere alle utfordringer ved en framtidig import, vet jeg ikke; det er ikke testet.

## 6. Punkt 5 — tilbakekall

Bare **lest i kode**, ikke bygget/testet her:
`GeneralCell.removeMember(member:requester:)` og `removeMember(uuid:requester:)`, linje 2015 og 2029, krever `validateAccess("-w--", at: "members", for: requester)`. Det kan være en bevist eier eller en bevist kontraktpart med den tilgangen; navnet/UUID-et alene gir ikke adgang. Prøvemalen gir ikke slik tilgang.
De fjerner medlemmet og alle autorisasjonskontrakter for subjektets UUID med `GeneralAuditor.removeAuthorization`, oppdaterer lagret autorisasjon og revaliderer feeds.
`Sources/CellBase/Cells/GeneralCell/Cast/GeneralAuditor.swift:441`, `removeContract(contract:)`, og linje 447, `removeContracts(subjectUUID:)`, er interne auditor-metoder. Auditoren er privat i GeneralCell, ikke en ekstern requester-autorisert kontraktfjerningsflate. Ingen ny tilbakekallsfunksjon er laget.

## 7. Punkt 6 — eierens to bruk av nøkler

**Kjørt, samme identitet:** cellens eier kan lese med sin nøkkelbærende identitet; offentlig kopi av samme eier avvises. Eieridentiteten er den samme som signerer innslippet i punkt 1.
**Kjørt, ulike identiteter:** eieren signerer innslipp for S; S leser med sin egen nøkkel, offentlig kopi av S avvises, og eieren kan også lese med sin egen nøkkel.

Rå b47/b49:

```text
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testOwnerAndSeparateAgentIdentityBothRequireTheirOwnKeyProof]' failed (0.001 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testOwnerSameIdentityRequiresKeyProofForOrdinaryRead]' passed (0.002 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testOwnerAndSeparateAgentIdentityBothRequireTheirOwnKeyProof]' passed (0.002 seconds).
Test Case '-[CellBaseTests.ExternalAgreementAdmissionTests testOwnerSameIdentityRequiresKeyProofForOrdinaryRead]' passed (0.001 seconds).
```

**Lest i kode:** eieradgang krever eierens nøkkelbevis; medlemstilgang krever subjektets bevis og aktiv, malavgrenset Contract. GeneralCell skiller ikke Touch ID/passord-modus etter om en nøkkel brukes til innslipp eller vanlig tilgang.
`Sources/CellApple/IdentityVault.swift:1124`, `signMessageForIdentity`, krever lokal identitet og matching offentlig nøkkel; `signMessageForVaultIdentity`, linje 1146, henter privat nøkkel og signerer. `keychainPrivateKey`, linje 655, bruker vaultens LAContext; `storePrivateKeyReference`, linje 681, og `createKeyPairForDomainv4`, linje 1402, bruker userPresence/privateKeyUsage. Konteksten tillater autentiseringsgjenbruk. Koden har også legacy-/rå nøkkelrepresentasjoner. Dette er kodelesing, ikke bevis på den observerte dialogen på en bestemt maskin.
**Ikke vist:** faktisk send-handling i CorrespondenceCell, Apple-dialoger, Touch ID/passord ved hvert innslipp og fravær av dialog ved agentens lesing/sending. Testene bruker EphemeralIdentityVault. Ingen av de to identitetsoppsettene anbefales framfor det andre.

## 8. Hele testmengden

**Kjørt:** c41, bygg exit 0 (383 s), tester exit 0 (102 s). Køskriptets egen exit er også 0; konklusjonen bygger på bygg-/testkodene. Full kjøring: **1577 beståtte Test Case-resultater, 0 feilede, 5 skip**. Alle 18 prøvetester besto også i denne kjøringen.

Kommandoen er `bash HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh codex/korr-innslipp-proeve-20261007`, kjørt av `wp-korr-admission-full.sh` med samme `swift build --build-tests --disable-automatic-resolution` og `swift test --disable-automatic-resolution --jobs 2` gjennom den bounded runneren. Bygg får også jobs 2.

Opptellingen søker etter `Test Case '...' passed/failed/skipped (` i hele råloggen, også når et diagnostikkutskrift ligger før resultatet på samme linje. Å kreve `^Test Case` overser åtte beståtte resultater. De faktiske tallene er 1577/0/5; summen 1582 samsvarer med de tre bundleoppsummeringene inkludert skips. Ingen av de eksisterende skipsene er lagt til av denne endringen. Alle resultattekstene er bevart i `HAVEN-Deploy/_handoff/KORR-UT/bolk1/full-result-lines.log`; selve Test Case-tekstene er uendret, diagnostikkprefikser er utelatt der utskrifter ble flettet sammen.

Rå porter og bundleoppsummeringer:

```text
bygg: exit=0, 383 s
tester: exit=0, 102 s
linjer med testfeil: 0
STATUS: LEVERT — CellProtocol codex/korr-innslipp-proeve-20261007 (8dfbd3f078) bygger, og hele testmengden er grønn på Mac-en
Test Suite 'HavenCommonsTests.xctest' passed at 2026-10-07 18:20:09.593.
	 Executed 26 tests, with 0 failures (0 unexpected) in 0.017 (0.018) seconds
Test Suite 'CellNearbyTests.xctest' passed at 2026-10-07 18:20:10.107.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'CellBaseTests.xctest' passed at 2026-10-07 18:21:39.622.
	 Executed 1553 tests, with 5 tests skipped and 0 failures (0 unexpected) in 88.048 (88.145) seconds
```

Rå skips:

```text
Test Case '-[CellBaseTests.AudioSignalAnalysisTests testReferenceFileMatchesChapter34AndIsDeterministic]' skipped (0.001 seconds).
Test Case '-[CellBaseTests.BridgeChannelProcessTests testIsolatedServerWorker]' skipped (0.000 seconds).
Test Case '-[CellBaseTests.MatcherBaselineDumpTests testWriteMatcherDump]' skipped (0.000 seconds).
Test Case '-[CellBaseTests.ScannerMultipeerProcessTests testMultipeerWorker]' skipped (0.001 seconds).
Test Case '-[CellBaseTests.ScannerMultipeerProcessTests testTwoProcessesUseRealMultipeerInBothInvitationDirections]' skipped (0.001 seconds).
```

Fullportens midlertidige kontrollarbeidstre ble låst under kjøringen. Derfor lot grunnmurskriptets automatiske remove det stå; etter ferdigmarkøren ble bare denne jobbens kontrollarbeidstre låst opp og fjernet. Det leverte prøvearbeidstreet beholdes låst.

Hovedutsjekken i CellScaffold manglet `scripts/run_swift_bounded.sh` og `scripts/check_build_capacity.sh`; eksisterende kopier i `_worktrees/release-2026.9.7/scripts/` brukes bare lesende. Ingen fil der ble endret. Begge portene hever og skriver filtaket og sjekker kapasitet uten overstyring. Fullportens midlertidige kontrollarbeidstre er også låst mens testen kjører.

Rå logger er under `HAVEN-Deploy/_handoff/KORR-UT/bolk1/` og `HAVEN-Deploy/_handoff/GRUNNMUR/logg-8dfbd3f078/`. Rå testresultatlinjer ovenfor er hentet fra loggene uendret; fulle bygglogger er ikke limt inn fordi de inneholder maskinens brukerstier. Avhengighetsinnhenting i byggverktøyet er separat fra testene; prøvetestene gjør ingen nettverkskall.

## 9. Ikke vist

- To prosesser eller maskiner og innslipp over broen: separate nøkkellagre i én prosess og direkte API-kall er kjørt.
- Ny brorute/tilhørende operasjonstillatelse: ikke laget. Om eksisterende ruting er tilstrekkelig, vet jeg ikke.
- Senderfunksjon, vedlegg, kryptert CorrespondenceCell, staging, M2 eller Intel: utenfor denne prøven.
- Touch ID/passord hver gang og dialogfri agentbruk: ikke testet med EphemeralIdentityVault.
- Tilbakekall: bare kodelest etter oppdragets punkt 5.
- Uavhengig review og korrespondanse-trådens gjennomgang: ikke utført av denne jobben.

## 10. Avvik fra det som er lest

`origin/main` inkluderer readiness-endringen: `addAgreement` kaller `ensureRuntimeReady` før requesterbevis og returnerer `.rejected` hvis bindingene mangler. De beskrevne øvrige funksjonene og Contract-feltene stemte ved lesing av grunnlaget. `locallyRestoredOwner` prøver `owner.identityVault` og `CellBase.defaultIdentityVault`; hvilken som helst slik implementasjon som kan finne/prove identiteten må fortsatt gi kryptografisk bevis. Ingen test her viser eiernøkkellager i en annen prosess via den gjenopprettingen.

`Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:198`, `establishInitialMembership`, ble lest: den legger eierens UUID i `memberIdentityUUIDs` hvis det mangler. Dette stemmer med den tidligere lesingen, men er ikke et nytt kjørebevis på relasjonscellen; prøven bruker GeneralCell med runtime-handlere.

## 11. Læringsfangst

`L-2026-10-07-pa-68069b6-har-contract-ingen-signert` er fanget, anvendt og markert synced. Dokumentet `Documentation/ExternalAgreementAdmissionProbe.md` er med i den lokale commiten og patchen; ingen main-implementasjon er dokumentert som ferdig. `L-2026-10-07-swift-xctest-resultater-kan-fa-diagnostikk-foran` fanger også tellefellen i denne rapporten; den er anvendt og markert synced. Dokumentmål distribueres med Git/leveransen, ikke skill-sync. `haven_learn.py check --strict` viser andre tråders åpne læringer (exit 1); begge denne jobbens poster er oppdatert og markert synced. Ingen fremmed læring er endret.

Første baselineforsøk b46 kompilerte ikke: testen refererte en privat auditor. Ingen tester kjørte der. Feilen ble rettet i testfixturen før b47; ingen produksjonskode ble endret før den korrigerte baselinekjøringen.

Baselinefixturen fra b47 er rekonstruert fra de uendrede skrive-/rettingsskriptene og bevart i `HAVEN-Deploy/_handoff/KORR-UT/bolk1/baseline-test.swift`. Den har 15 tester og den tydelig merkede testadapteren. Patchen er sjekket med `git apply --check --reverse` mot det leverte arbeidstreet (exit 0).

Etter c41 ble bare jobbens egen bounded-cache (`52eb8d45e116`, 9,1 GiB) fjernet med runnerens eksisterende `delete_managed_cache`-funksjon, etter eierskapsmarkør, eksklusiv lease og kontroll av åpne filer (exit 0). Rå logger beholdes. Egne midlertidige skrive-/rettingsskript og fixturekopier er fjernet; andre arbeidstrær og cacher ble ikke manuelt ryddet.
