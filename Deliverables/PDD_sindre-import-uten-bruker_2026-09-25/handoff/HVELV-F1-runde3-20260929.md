STATUS: STOPPET — runtime-manifestet signeres med serverens tekniske eiernøkkel; uavhengig eierforankring fra Mac mangler, head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 29.09.2026, for Kjetil og Losen. Arbeidsreferanse `PDD_sindre-import-uten-bruker_2026-09-25.F1`. **F1 er fortsatt åpen. Stoppkriteriet i oppdragets punkt 1 er oppfylt. Ingen implementering, bygg, signering, commit, push, merge eller utrulling i denne runden.** Bare rapport/evidens, driftsnotat og obligatorisk læringsfangst er skrevet.

Forrige rapport er bevart byte-identisk som [HVELV-F1-runde2-20260928.md](HVELV-F1-runde2-20260928.md). Valget **A er avklart**: HavenAgentD-nøkkelen på Kjetils Mac skal være personlig eieranker kun for mottakerbindinger. Det som mangler er en tillitskjede som håndhever dette uten en erstatningsvei kontrollert av serveren. Det er ikke behov for å velge A på nytt.

## Utgangspunkt og stoppgrunn

Arbeidstre `CellScaffold/_wt-forvaltet-import-20260926`, gren `pdd/forvaltet-kunstnerimport`, [PR #270](https://github.com/Digipomps/CellScaffold/pull/270). GitHub bekreftet OPEN og samme head som lokalt; base `feec23725321320ab00f0e7f7bf728b775869ec7`. Arbeidstreet er fortsatt låst mot prune. Se [PR-metadata](evidence-hvelv-f1-owner-anchor-20260929/pr-state.json) og [kildehashene](evidence-hvelv-f1-owner-anchor-20260929/source-state-before.json).

Alle sju eksisterende endringer var de autoriserte F1-utkastene: binding-helper, helpertester, Python-klient, Python-tester, testskript, CI-filter og driftsnotat. Disse var **ikke stoppgrunn**. Ingen usporede testrester forelå i Git-status; ingen nye tester er kjørt og ingen rester flyttet. Docs-repoets omfattende WIP og hele PDD-mappen som untracked er bevart. HavenAgentD har annen WIP og er ikke endret; signeringskilden der ble lest fra det navngitte Git-objektet.

Oppdraget sier: «Er dagens manifest signert av en nøkkel som ligger på serveren, stopp og beskriv nøyaktig hva som mangler for å oppfylle kravet.» Den bestilte revisjonens produksjonskode og deployskript viser nettopp serverlokal signering. Derfor er ikke de avhengige F1-endringene eller publiseringsstegene utført.

## Hvilken nøkkel signerer manifestet, hvor og hvordan?

Alle CellScaffold-ankre nedenfor er på eksakt head `b658ef53e14dccdb12009991e78b1b44d47dac8a`. De inspiserte produksjonsfilene er byte-identiske med Git-head. CellProtocol-ankre er lest med `git show` på PR-ens uendrede pin `2026.9.3`, SHA `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366`.

| Ledd | Fil:linje | Kildebekreftet oppførsel |
|---|---|---|
| Produksjonens tekniske eier | `scripts/production/manifest-provision-production.conf:11` | Den innsjekkede konfigurasjonen velger `OWNER_CONTEXT = HavenProduction`. Faktisk installert konfigurasjon, nøkkel-UUID og nøkkelfingeravtrykk er ikke lest. |
| Signeringssted | `scripts/production/haven-manifest-provision:640`, `:676`, `:703` | Skriptet kopierer serverens vault-masterkey til en beskyttet seremonifil, sender vault-rot og masterkey-sti til bootstrap, og kjører verifieren med `unshare --net` som UID/GID 995 på Linux-verten. Masterkeyen er krypteringsnøkkelen til vaulten, ikke selve Ed25519-signeren. |
| Valg av signeringsidentitet | `Sources/App/Support/CellScaffoldRuntimeIdentityProvisioner.swift:1472`, `:1504`, `:1548` | Bootstrap velger `VaporIdentityVault.shared`, finner eierbindingen for den konfigurerte konteksten og utleder eier-UUID/fingeravtrykk derfra. |
| Signering av nytt manifest | `Sources/App/Support/CellScaffoldRuntimeIdentityProvisioner.swift:451`, `:478` | Provisjoneringen krever eksisterende eksakt eier i vaulten og sender denne identiteten til `CellScaffoldRuntimeIdentityManifest.sign`. |
| Byteformat og algoritme | `Sources/App/Support/CellScaffoldRuntimeIdentityManifest.swift:100`, `:181`, `:195`, `:322`, `:328` | Ed25519 over v3-domeneprefikset `HAVEN\0runtime-identity-manifest.v3\0` fulgt av kanonisk JSON. `owner.sign(data:)` utfører signeringen; signaturen verifiseres før dokumentet returneres. |
| Privatnøkkelgrensen | CellProtocol `Sources/CellVapor/VaporIdentityVault.swift:1559`, `:1588`, `:2540`, `:2638` | `requireIdentity` leser den eksisterende vaulten og knytter den til identiteten. Signeringskallet bruker `privateSecureKey.compressedKey` til å opprette `Curve25519.Signing.PrivateKey` og signere lokalt i serverprosessen. |
| Strengt lagringsformat | CellProtocol `Sources/CellVapor/VaporIdentityVault.swift:1146`, `:1163`, `:1185`, `:2887` | Strict-validering krever 32-byte privat signeringsmateriale, riktig privat SecureKey og samsvar med offentlig nøkkel. Privatmaterialet inngår i vaultens serialisering. En offentlig Mac-nøkkel kan ikke bare settes inn som denne eieren uten å endre strict-kontrakten eller kopiere privatnøkkelen. Ingen av delene er gjort. |
| Verifikasjon ved oppstart | `Sources/App/configure.swift:548`, `:561`, `:577` | Strict aktiveres; forventet eier løses fra `VaporIdentityVault.shared`; signaturen verifiseres mot denne tekniske eieren og eksakt profil/build/vault. |

Direkte kildeankre: [provisjonering](https://github.com/Digipomps/CellScaffold/blob/b658ef53e14dccdb12009991e78b1b44d47dac8a/Sources/App/Support/CellScaffoldRuntimeIdentityProvisioner.swift#L451), [serverkjøring](https://github.com/Digipomps/CellScaffold/blob/b658ef53e14dccdb12009991e78b1b44d47dac8a/scripts/production/haven-manifest-provision#L676), [signering med privatmateriale](https://github.com/Digipomps/CellProtocol/blob/9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366/Sources/CellVapor/VaporIdentityVault.swift#L2638).

**Konklusjon fra kilden:** dagens manifest signeres med scaffoldets tekniske Ed25519-eiernøkkel fra servervaulten. Å signere et nytt felt med den samme nøkkelen beviser ikke Kjetils godkjenning på Mac-en. Den som kan benytte denne serverholdte signeringsnøkkelen, ville fortsatt kontrollere godkjenningen av et slikt felt. Strict-modus, filrettigheter og historikkverifikasjon har reelle andre vern, men skaper ikke den manglende uavhengige eierforankringen.

Dette er **ikke** en påstand om at Kjetils personlige HavenAgentD-privatnøkkel er funnet på serveren. Ingen levende vault, private nøkkelbytes, installert daemonkonfigurasjon, servermiljø eller produksjonsmanifest er lest. Det er den leverte program- og driftsveiens krav til serverholdt signeringsmateriale som er dokumentert, ikke en inventarliste over produksjonens faktiske nøkler.

## Det som konkret mangler før F1 kan fortsette

1. **Autentisert innrullering av A:** Kjetils offentlige Mac-nøkkel, algoritme, kanoniske fingeravtrykk og nøyaktig scaffold må etableres som tillitsrot gjennom eierstyrt bevis. En rot som bare godtas fordi et serverkontrollert manifest eller miljøfelt oppgir den, oppfyller ikke kravet. Nåværende schema har ikke et eget mottakeranker (`CellScaffoldRuntimeIdentityManifest.swift:65`).
2. **Eierstyrt signaturkjede for ankeret:** mottakerankerets innhold og alle endringer må kreve signatur på eierens enhet. Manifest-/bootstrap-/runtime-kjeden må verifisere denne mot allerede betrodd offentlig rot uten fallback til serverens tekniske eier, default-vault, konfigurasjon eller miljø. Definer første innrullering, nøkkelrotasjon/gjenoppretting og håndtering av eldre gyldig oppsett. Dette er manglende design/implementering, ikke en levert migrasjonskommando. Sentral strict-policy og avvisningstester må bevares.
3. **Klientløype med testidentiteter:** eksisterende HavenAgentD-signering kan brukes som lokal signeringsmekanisme, men erstatter ikke punkt 1–2. Klienten mangler fortsatt kall til den, mottak/verifikasjon av konvolutten og den komplette claim-løypen.
4. **Claim og testbevis:** alle F1-integrasjoner og regresjoner nedenfor må fullføres etter at tillitskjeden er løst. Kjør deretter bounded bygg/test, de to bestilte CI-gatene, commit med de oppgitte PDD/F1-/medforfatter-/sesjonslinjene, push og CI-venting. Ingen slike kodeendringer er publisert nå.

Eksisterende lokal signering er kontrollert på HavenAgentD `a9da717453ef3061d288fb5abbb29135c17fc720`: `Sources/HavenAgentRuntime/AgentSignatureStatement.swift:353` validerer request og lokal signer, `:389` reserverer nonce og `:390` signerer med daemonens lokale identitet. `Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:163` er `POST /commands/identity/sign-statement`; `Sources/HavenAgentDMCP/HavenAgentMCPService.swift:1237` krever aktiv loopback-bridge og videresender til denne ruten ved `:1255`. Dette korrigerer de tidligere linjenumrene 80/960, som ikke gjelder dette Git-objektet. Signeringsfilens SHA-256 er fortsatt `7e1efeb0ec6e5410b8f193bc8ec97b7d30886bdb1acc36d9a5b879828c0f39ad`. Ingen signeringsroute/MCP-signering er kalt, verken med testidentitet eller Kjetils nøkkel. Ingen HavenAgentD-PR er opprettet.

## Krav og tester — faktisk status

Forkortelser under: `V` = `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift`; `B` = `ManagedArtistRecipientBinding.swift` i samme mappe (**tidligere ucommittet utkast**); `T` = `Tests/AppTests/ManagedArtistRecipientBindingTests.swift` (**tidligere utkast**); `I` = `Tests/AppTests/ManagedArtistImportTests.swift`. Ingen test i tabellen er kjørt i denne runden. «Fanger?» vurderer testens eksisterende assertions mot original F1; det er ikke en kjørt mutationstest.

| Krav | Fil:linje / hva som finnes | Testnavn og om den ville fanget originalfeilen |
|---|---|---|
| Eieranker A, ikke serverstyrt | Manifest/provisioner/kildekjeden over. Intet A-anker implementert. | `CellScaffoldRuntimeIdentityManifestTests.swift:140` `testWrongOwnerServiceSignerAndSignatureShapeFailClosed` prøver feil signer mot teknisk eier. **Nei**, ikke uavhengig Mac-anker eller servergodkjent ankerbytte. |
| Lokal signering fra klient | `scripts/managed_artist_recipient.py:96` tilbyr bare `fingerprint` og `prepare`; `:113` skriver offentlige utkast. | T:40 `testApprovedBindingAndExistingAgentDEnvelopeVerify` lager fixture-konvolutt. **Nei**, ingen virkelig klient-/daemonløype. |
| Ny importørstyrt peer med riktig token avvises | V:483/:489 krever ennå ingen eiersignert binding ved første claim. | I:359 `testClaimPreservesIDsAssetsAndNeverStoresArtistsPrivateKey` forventer at tilfeldig ny peer lykkes. **Nei**, originalfeilen er fortsatt positiv forventning. |
| Representant/tilfeldig signerer/feil eier | B:137 tar `trustedOwner` fra kalleren, uten produksjonsforankring. | T:84 `testWrongOwnerAndForgedEnvelopeRejected`. **Nei for original claim**; helperens avvisning alene endrer ikke V. Representant-integrasjon mangler. |
| Ingen lokal eier-snarvei | V:487 krever bridge for claimant; det finnes ingen eiergodkjenningsgate. | I:342 `testClaimNeedsTokenProofAndRightsAttestation` avviser lokal importør ved :354. **Nei**, den prøver verken serverlokal godkjenningssignatur eller ny ekstern importørpeer. |
| Alle signerte felt uforanderlige | B:55/:137 definerer scope, nøkkel, UUID, fingeravtrykk, tider, schema og engangs-ID samt konvoluttverifikasjon. | T:48 `testEveryBoundFieldMutationInvalidatesOwnerSignature`. **Nei for original claim**; utkastets helpertest er ikke integrert. |
| Eksakt import/slug/scaffold og mottaker | B:74 validerer eksakt scope/mottaker. V:452 tillater ingen bindingspayload. | T:65 `testValidSignatureStillNeedsExactScopeRecipientAndShortLifetime`. **Nei for original claim**; claim-integrasjon mangler. |
| Utløp | B:84 krever aktiv binding med maks 600 sekunder; V har ikke denne kontrakten. | Samme T:65. **Nei for original claim**. |
| Entydig fingeravtrykk på begge enheter | B:31/:47 normaliserer Ed25519/P256 og beregner domeneseparert SHA-256. | T:11 `testClientAndServerFingerprintGoldenVector`; T:24 `testP256CompressedAndUncompressedHaveOneFingerprint`. **Nei for original autorisasjonsfeil**; ingen kjørt full klientløype. |
| Replay av binding eller gammel mottakersignatur | V:429 har fersk challenge; V:506 lagrer `transferring`, uten bindings-ID/digest/forbruk. | I:359 prøver fullført claim på nytt ved :387. **Nei**, ikke bindingsreplay eller gjenbrukt utfordringssignatur. Nye tester mangler. |
| Varig atomisk bindingsforbruk og parallelle claims | V:176 record mangler bindingsforbruk; V:506 lagrer bare claimant/fase. | Ingen slik claim-test. I:314 `testConcurrentReplayHasExactlyOneSuccessfulImport` gjelder execute. **Nei**. |
| Retry bare med samme bundne mottaker | V:489 har samme claimant-nøkkel etter påbegynt overføring, uten eierbinding. | I:393 `testInterruptedClaimHidesBothCellsAndCanResumeSameClaimant` prøver samme peer i samme runtime. **Nei** for annen mottaker/varig binding etter reload; de bestilte negative testene mangler. |
| Positiv godkjent overtakelse, attestasjon først etter gate | V:506–512 flytter cellene uten F1-gate. | I:359, med attestasjon ved :386. **Nei**, positiv peer er ennå ikke eiergodkjent. |
| Begge personers private nøkler forblir lokale | B:174 avviser ukjente felter. Faktisk lagrings-/transportinspeksjon med to testidentiteter mangler. | T:105 `testUnknownAndPrivateFieldsAreRejectedAtEveryPayloadLevel`; I:359 inspiserer kunstnerfixturens private bytes i dekryptert issuance-snapshot og begge celler ved :377. **Nei** for Kjetils nye eierkjede og samlet ende-til-ende-krav. Ingen reelle nøkler lest. |

Sentral strict-oppførsel, manifestkode, provisjonering, claim, lagring, eksisterende avvisningstester og package-pinner er urørt. Det tidligere filtertillegget for `ManagedArtistRecipientBindingTests` er bevart. Ingen nye skips/exclusions eller filterendringer er lagt til i denne runden. F4/F5/F6/F7/F8/F9 er ikke rettet eller godkjent av denne F1-kontrollen.

## Hva Kjetil og Sindre konkret skal gjøre

**Ingen produksjonsovertakelse nå.** Driftsnotatet i arbeidstreet, `Documentation/Operations/Managed_Artist_Import_2026-09-28.md:7`, beskriver stoppgrunnen; `:79` beskriver den tilsiktede sekvensen og hvilke klientsteg som mangler. Den er ikke fremstilt som en ferdig kommando-/GUI-løype.

Når tillitskjeden og testløypen er levert:

1. Sindre viser sitt fulle kanoniske fingeravtrykk på egen enhet og deler bare offentlig descriptor `{uuid, algorithm, publicKeyBase64URL}`. Kjetil beregner samme fingeravtrykk på Mac-en og sammenligner alle tegn med Sindre ansikt til ansikt eller på video.
2. Kjetil kontrollerer nøyaktig import-ID, slug, scaffold, mottakernøkkel og utløp; `prepare` lager `binding.json` og `sign-request.json`. Det eksisterende utkastet signerer ingenting.
3. Kjetil godkjenner og signerer bindingen med den fast forankrede HavenAgentD-nøkkelen på sin egen Mac. Klienten skal returnere offentlig binding og signatur; denne klientintegrasjonen er ikke levert. Privatnøkkelen skal ikke flyttes til scaffoldets vault.
4. Sindre sender token + offentlig binding/signatur fra egen klient, bekrefter rettighetene og svarer med fersk signatur fra akkurat den bundne nøkkelen. Serveren skal deretter lagre forbruk atomisk før eierskap/attestasjon endres. Denne F1-integrasjonen mangler fortsatt.

Kjetil trenger ikke velge eieranker på nytt eller bruke sin produksjonsnøkkel til å teste dette. Det tekniske neste arbeidet er å etablere og verifisere eierstyrt innrullering/signaturkontroll for A; deretter testes sekvensen med testidentiteter før Sindre bruker den.

## Kontroller, endringer og avgrensning

Utført: Git-status/head/arbeidstrelås; GitHub-lesing av PR-metadata; lesing av ASTRA-HVELV-2 §1, ASTRA-HVELV-3, forrige F1, FORMAALSSPEC/PLAN og driftsnotatet; kildefølging av manifestets signering og servervaultens privatnøkkelbruk på eksakte revisjoner; inspeksjon av relevante testkropper og utkast; byte-identisk arkivering av forrige rapport; kildehashinventar og etterkontroll av at bare driftsnotatet er endret i PR-arbeidstreet i denne runden.

**Ikke kjørt:** `scripts/run_swift_bounded.sh … --disable-sandbox`, byggkapasitetsvakten, Swift-/Python-tester, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh`, live HavenAgentD-signering, ny-prosess-/parallelle-claim-/replayprøver, private-key-lagringsinspeksjon med testidentiteter, staging/prod/GUI. Stoppet kom før bygg, så diskplassen er ikke målt i denne runden og gammel diskblokkering er ikke brukt som begrunnelse. Ingen byggvakt er omgått.

Ingen commit/push eller ny CI er startet; 60-minuttersvinduet har ikke startet. Historisk grønn CI for F2 brukes ikke som bevis for F1. Den bestilte commitmeldingen og trailerne gjenstår sammen med implementasjonen. Ingen merge.

Sluttkontroll: `git diff --check` PASS; arkivkopien er byte-identisk med forrige rapport; alle inspiserte kode-/test-/filterfiler har uendret hash fra før arbeidet; head er uendret. Se [kontrollresultatene](evidence-hvelv-f1-owner-anchor-20260929/final-checks.json).

Læringsfangst: `L-2026-09-29-runtime-manifestet-i-cellscaffold-pr-270`, mål er driftsnotatet i PR-arbeidstreet. Kildebeviset og valget A er skrevet der; `applied` og `sync` er gjennomført. Docs-sync distribuerer via Git; uten commit/push er oppdateringen lokal. `check --strict` avsluttet med 0 og ingen åpne læringer; 24 andre oppdaterte, ikke-distribuerte poster er ikke håndtert av denne jobben. Se [læringsposten](evidence-hvelv-f1-owner-anchor-20260929/learning-records.json) og [kontrollutdata](evidence-hvelv-f1-owner-anchor-20260929/learning-check.txt). Losen-logg og læringsledger er oppdatert av læringsverktøyet; øvrig WIP er bevart.
