STATUS: STOPPET — byggevakt exit 75 etter første byggforsøk: 54,2 GiB ledig, 44,2 GiB / 4 % etter reserve; head b658ef53e14dccdb12009991e78b1b44d47dac8a

Anker-fingeravtrykk: **`sha256:41054cb1022ee5a79934d702a3986bafdfb1bebd515be86d6c90a014fb6d4e2d`** — offentlig nøkkel hentet fra lokal HavenAgentD og lagt i lokalt kodeutkast; **ikke committet, pushet eller lagt i PR-beskrivelsen**.

Codex, 29.09.2026, **runde 5**, `PDD_sindre-import-uten-bruker_2026-09-25.F1`. [PR #270](https://github.com/Digipomps/CellScaffold/pull/270) ble kontrollert OPEN på samme head som arbeidstreet. **F1 er ikke levert eller lukket. Ikke merge.** Ingen commit, push, merge, utrulling eller ny CI er utført.

Forrige gjeldende rapport var runde 4. Den er bevart byte-identisk som [HVELV-F1-runde4-20260929.md](HVELV-F1-runde4-20260929.md), SHA-256 `6370fe87db1f44bb6b96606d6bbd9ba0f9f48b971d1506472483d265384c7c24`. Det eksisterende [runde-3-arkivet](HVELV-F1-runde3-20260929.md) er bevart urørt. Ny rapport overskriver ikke noe tidligere rundenummer.

## Målt stoppgrunn

Før implementering kjørte den uendrede byggevakten uten overstyringer og passerte: **58,7 GiB ledig; 48,7 GiB / 5 % etter 10 GiB reserve**, exit 0, kl. 10:39:17Z. [Første kapasitetsmåling](evidence-hvelv-f1-runde5-20260929/build-capacity.txt).

Deretter ble ordinær App-kompilering, **uten testinjeksjonsflagget**, forsøkt:

```sh
HAVEN_SWIFTPM_CACHE_KEY=cellscaffold-managed-artist-import scripts/run_swift_bounded.sh build --target App --disable-sandbox --force-resolved-versions
```

Runneren kjørte sin egen kapasitetsvakt, også exit 0. Kompileringen nådde App og feilet på `ManagedArtistRecipientAnchor.swift:28`: den pinnede `Identity`-konstruktøren trenger `displayName`. Argumentet er rettet lokalt; samme feil ble rettet i tre tidligere ukompilerte testfixture-konstruktører. **Rettelsene er ikke kompilert.** [Full bygglogg](evidence-hvelv-f1-runde5-20260929/build-production-path.log), exit 1.

Før et nytt bygg ble `scripts/check_build_capacity.sh .` kjørt på nytt, uten noen av `HAVEN_BUILD_RESERVE_GIB`, `HAVEN_BUILD_MIN_FREE_GIB` eller `HAVEN_BUILD_MIN_FREE_PERCENT` satt:

```text
2026-09-29T10:54:58Z
Build capacity: 54.2 GiB free (5%); reserving 10 GiB leaves 44.2 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
Exit status: 75
```

`df -Pk` målte **56 800 000 KiB tilgjengelig** av **971 298 980 KiB**. Prosentgulvet blokkerer. [Ny måling og eksakt kommando](evidence-hvelv-f1-runde5-20260929/build-capacity-after-compile.txt). Vakten er byte-uendret. Det første byggforsøket rapporterte også totalt 15 552 596 KiB administrert cache mot standardgrensen 12 582 912 KiB; ingen cacheopprydding, ny scratch-path, terskelendring eller eierskapsmarkering er forsøkt. Endringen i ledig plass er en måling over intervallet, ikke bevis på at hele endringen skyldes denne jobben.

Kjetils uttrykkelige regel om stopp ved diskblokkering er fulgt. Etter exit 75 er bare rapport/evidens, driftsnotat, læringsfangst og kontroll av bevart arbeid håndtert. Ingen videre kodeendring, test, bygg eller publisering.

## Offentlig anker og faktisk lokal signeringsprøve

Den eksisterende autentiserte lokale ruten `GET http://127.0.0.1:43110/onboard/status.json` returnerte én offentlig identitet:

- UUID: `CAE0170A-9A90-4212-A5AA-FB8FA391203A`
- Algoritme: `Ed25519`
- Offentlig nøkkel, kanonisk base64url: `uCexInamQw9X9VyJqnQmoGOE5KaVp3wt9PWj0Q8CCM8`
- Formålsavgrensning i utkastet: `purpose://publication.managed-artist-recipient-binding`
- Fingeravtrykket over er SHA-256 av UTF-8 `haven.artist-recipient-key.v1\nEd25519\n` etterfulgt av de 32 offentlige nøkkelbytene, vist som full liten heksadesimal med `sha256:`-prefiks.

Tilgangstokenet kom fra eksisterende lokal bridge-konfigurasjon og ble ikke skrevet ut eller lagret i evidensen. Bare offentlig descriptor og en sladdet forespørselskvittering ble beholdt. Agentens private identitetsfil, Keychain og produksjonsvault ble ikke åpnet av denne jobben. Ingen signeringsforespørsel brukte Kjetils identitet. Den offentlige routen beviser nøkkelen som lokal daemon presenterte; **Kjetils egen sammenligning og godkjenning er fortsatt nødvendig før merge**.

Kilden som ble lest for eksisterende signering var HavenAgentD head `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98`, særlig `Sources/HavenAgentRuntime/AgentSignatureStatement.swift:353`, `Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:80` og `Sources/HavenAgentDMCP/HavenAgentMCPService.swift:1008`. HavenAgentD har fremmed WIP som er urørt; ingen endring eller egen PR der var nødvendig for den prøvde signeringsruten. Installerte binærens kildeekvivalens er ikke sertifisert fra dette headet.

En separat prosess av den **installerte** HavenAgentD-binæren ble startet med `onboard --root <egen-testrot> --config <egen-testkonfig>`, egen loopback-port, testidentitet og deaktivert nettverksovervåking. Binær-SHA-256: `9055259e01540eced9153822488786a8c5428a102d938e73ff1536d5a53928f4`. Python-klienten hentet testidentitetens offentlige descriptor, sendte bindingen til `POST /commands/identity/sign-statement` og verifiserte konvolutten. Bare testharnessen substituerte den offentlige testnøkkelen. Det produksjonsrettede kodeankeret ble ikke endret.

Resultat: **PASS for lokal testidentitet/signering/klientverifikasjon**. Prosessen er stoppet. Testroten, som inneholder generert testidentitetsmateriale, er flyttet til HAVEN `_to_delete/hvelv-f1-runde5-20260929/`. Se [signeringskvittering](evidence-hvelv-f1-runde5-20260929/agentd-test-receipt.json) og [offentlig testkonvolutt](evidence-hvelv-f1-runde5-20260929/agentd-test-public-envelope.json). En offentlig JSON-fixture er også lagt i AppTests; Swift-verifikasjonen av den er skrevet, **ikke kjørt**. Dette er ikke en ekstern artist-claim, full restartprøve eller inspeksjon av serverlagring.

## Krav, lokale kildeankre og testevne

Alle kildeankre gjelder **lokale utkast i `CellScaffold/_wt-forvaltet-import-20260926`**, ikke levert PR-head. `A` = `Sources/App/Cells/ManagedArtistImport/ManagedArtistRecipientAnchor.swift`; `B` = `ManagedArtistRecipientBinding.swift` i samme mappe; `V` = `ManagedArtistIssuanceVault.swift` i samme mappe; `I` = `Tests/AppTests/ManagedArtistImportTests.swift`; `T` = `Tests/AppTests/ManagedArtistRecipientBindingTests.swift`; `C` = `scripts/managed_artist_recipient.py`.

«Fanger originalfeilen?» er kildevurdering av assertions, **ikke** en kjørt mutationstest. Ingen Swift-test er kjørt denne runden. En negativ med det nye feltet kan også avvises av gammel kode fordi feltet er ukjent; det teller ikke alene som et målrettet F1-regresjonsbevis.

| Krav | Faktisk lokal endring / fil:linje | Test og vurdering mot original F1 |
|---|---|---|
| 1. Ett kodeanker; bare mottakerbindinger | `ManagedArtistRecipientAnchorSource.swift:9` inneholder den ene offentlige literaldefinisjonen. A:19 validerer algoritme/formål/fingerprint; A:38 bruker produksjonsankeret. A:47 har injeksjon bare under `MANAGED_ARTIST_TESTING`, ikke vanlig DEBUG. | I:481 `testProductionAnchorIgnoresEnvironmentConfigManifestAndServerVaultOverrides` er skrevet. Python `test_production_anchor_ignores_environment_and_no_key_is_sent_on_local_mismatch` **PASS**. Produksjonskompilering/symbolkontroll og særskilt CLI-/binærtest **mangler**. Ingen lukking. |
| 2. Offentlig nøkkel og egen ankercommit | Offentlig GET-henting og fingerprint er målt, og ankeret står i lokal kilde. | Descriptor/kvittering er bevis for offentlig henting, ikke original claim-retting. **Ankercommit og PR-body mangler** etter diskstopp. |
| 3. Signering lokalt og kontroll før utskrift | C:57 sender bare til loopback uten proxy/redirect; C:81 henter offentlig identitet; C:176 verifiserer konvolutt med OpenSSL 3; C:229 sammenligner lokal signer med kodeankeret før signering. | Fire nye Python-tester + fire tidligere **PASS**. Isolert, faktisk HavenAgentD-prosess **PASS**. T:48 `testActualLocalAgentDTestIdentityEnvelopeAndClientCanonicalization` er skrevet, ikke kjørt. Mekanismebevis, **ikke alene original claim-regresjon**. |
| 4. Token + eierbinding + fersk kunstnerproof | V:494 tillater `recipientApproval`; V:534–547 parser og validerer den mot kodeankeret og binder artist-challenge til godkjenningsdigest. V:561 kaller forbruk før eierskiftene. | I:361 `testTokenAndFreshImporterControlledPeerWithoutOwnerApprovalCannotClaim`: **ja, denne negative ville direkte oppdaget originalfeilen**, fordi gammelt payloadformat med riktig token og ny peer da lykkes. Skrevet, ikke kjørt. |
| 4/5. Positiv rett mottaker og attestasjon | Den tidligere tilfeldige-peer-positiven er erstattet av I:511 `testOwnerApprovedClaimPreservesIDsAssetsAndNeverStoresEitherPrivateKey`; helper I:687 lager eksplisitt test-eiergodkjenning. | Gammel kode ville ikke oppfylle det nye positive forløpet. Testen er ukjørt; det finnes fortsatt ikke en vellykket kompilert F1-claim her. |
| 5. Representant/importør/servereier/tilfeldig signer | A:19/38 henter aldri servereier fra vault; B:139 krever forhåndsfestet signer; I:379 bruker faktisk signering med fire ulike test-vault-identiteter. | `testRepresentativeImporterServerOwnerAndRandomSignerCannotApproveRecipient` skrevet. Negativene alene ville også blitt avvist som ukjent payload av original kode; **ikke isolert originalregresjon**. |
| 5. Hvert bundet felt, scope, mottaker, utløp | B:57/75/139 binder særskilt formål, schema, import, scaffold, slug, UUID, kanonisk key/fingerprint, tidsrom og binding-ID. | I:401 `testEveryChangedBindingFieldRejectedByClaimBeforeAttestation`; I:430 `testSignedWrongImportSlugScaffoldRecipientPurposeAndExpiredBindingsRejected`; T:81/98 helpernegativer. Skrevet, ukjørt; Python-felt-/signatur-/utløpsnegativer PASS. Ikke alene originalregresjon. |
| 5. Varig/atomisk forbruk, replay og parallelle claims | V:189–191 lagrer scaffold/approval/forbrukstid; V:294 `beginClaim` setter approval, claimant og `transferring` i ett snapshot og sjekker brukt binding-ID på tvers av records. | I:456 `testParallelClaimsConsumeExactlyOneApprovalAndRejectTerminalReplayAfterReload` skrevet, ukjørt. Forbruk i gammel kode mangler; nye assertions ville ikke vært oppfylt. Egen replaytest med samme binding-ID og ny ellers gyldig binding på en annen import er **ikke skrevet ferdig**. |
| 5. Resume med samme binding/nøkkel og fersk proof | V:309/540 krever eksakt lagret approval og samme signing identity. Retry validerer fristen mot opprinnelig forbrukstid; krever ny challengesignatur. | I:550 `testInterruptedClaimHidesBothCellsAndCanResumeSameClaimant` er utvidet med hvelv-reload, annen UUID, samme UUID/annen nøkkel, gammel claim-signatur og samme binding etter frist. Skrevet, ukjørt. Bare hvelvet restartes; **ikke F4s nye prosess og alle lagre**. |
| 5. Begge private nøkler fraværende fra serverlagring | I:511 er utvidet til å lete etter både test-eierens og test-kunstnerens private bytes/base64/base64url i issuance-plaintext og begge serialiserte celler. B:183 avviser ekstra/private felter. | T:138 `testUnknownAndPrivateFieldsAreRejectedAtEveryPayloadLevel` og lagringsassertions er ukjørt. Python HTTP-fixturen sjekket offentlige payloads; **full transport-/logg-/lagringsinspeksjon er ikke levert**. Ingen reelle private nøkler er inspisert. |
| 6. Operatørsekvens og bytte | Driftsnotatets nye runde-5-del gir public-identity/fingerprint/sign-kommandoer, nøkkelbytte via ny PR/release og begrensning ved gamle binærer. | Lokal signer er prøvd med testidentitet. **Ekstern Sindre-claim-kommando/GUI og full ende-til-ende-prøve mangler**. |

Sentral strict-produksjonskode, eksisterende strict-avvisningsassertions, manifestkode, package-pinner og skips/exclusions er ikke endret. Eksisterende claim-testinput er styrket med eksplisitt binding, slik at token- og attestasjonsnegativene ikke bare feiler på manglende binding. Test-build-flagget er lagt til i lokal F1-testwrapper og CI-testkommandoene; det er **ikke verifisert i CI**. Ingen runtime-miljøvariabel aktiverer injeksjonen i vanlig bygget app. At det ferdige produksjonsproduktet faktisk er uten injeksjon er **ikke bevist av et vellykket bygg** her.

## Hva Kjetil og Sindre konkret må gjøre

Før videre utvikling må uendret byggevakt passere igjen. Denne jobben har ikke ryddet plass. Fortsett på det bevarte arbeidstreet; ikke forkast utkastene. Før commit/push må rettet App og testmål kompileres, manglende F1-prøver fullføres, og alle påkrevde lokale porter passere. Den separate ankercommiten skal ha meldingen:

```text
F1-anker: Kjetils HavenAgentD offentlige nøkkel, fingeravtrykk sha256:41054cb1022ee5a79934d702a3986bafdfb1bebd515be86d6c90a014fb6d4e2d
```

Alle commits skal også ha PDD/F1-referansen og de bestilte Co-Authored-By-/Claude-Session-linjene. Deretter push til PR #270, fingerprint i PR-body og maks 60 minutters CI-venting. **Ingen av disse publiseringsstegene er utført.**

Fra PR-arbeidstreet på Kjetils Mac finnes nå denne offentlig-visningskommandoen i klientutkastet:

```sh
/usr/bin/python3 scripts/managed_artist_recipient.py public-identity --out /private/tmp/kjetil-havenagentd-public.json
```

Målfilen må være ny. Kommandoens underliggende offentlige route/helper er prøvd; selve CLI-invokasjonen over ble ikke separat kjørt. Sammenlign hele fingerprintet med egen Mac og med ankercommiten/PR-beskrivelsen når de er levert. **Ikke merge denne runden.** Ingen ny beslutning om A eller «I koden via PR» trengs.

Sindre viser fullt fingerprint fra egen offentlig descriptor:

```sh
/usr/bin/python3 scripts/managed_artist_recipient.py fingerprint artist-public.json
```

Kjetil beregner samme streng fra offentlig fil, sammenligner den med Sindre og kontrollerer eksakt import/slug/scaffold. Når testet og releaset, signerer han på egen Mac med `sign --artist artist-public.json --import-id <UUID> --scaffold <ref> --slug <slug> --confirm-fingerprint <hele-strengen> --out recipient-approval.json`; driftsnotatet gir full kommando. Kjetils ekte nøkkel skal ikke brukes for å bevise integrasjonen.

Sindre må deretter sende token + offentlig approval gjennom sin egen eksterne signing-klient, bekrefte rettigheter/innhold og besvare fersk challenge med nøyaktig bundet nøkkel. En ferdig runnable kommando/GUI for dette steget er **ikke levert**. Celle-API-beskrivelsen skal ikke omtales som ferdig operatørløype.

Ankerbytte krever ny offentlig nøkkel i ny PR, Kjetils kontroll/merge og ny release. En gammel binær inneholder fortsatt gammelt anker; kildekonstanten alene beskytter ikke mot utrulling av gammel binær. Release-/rollbackkontroll gjenstår. Eldre records uten scaffold-/bindingsfelt og eventuelle allerede claimed før-F1-records må gjennomgås før drift; ingen produksjonsdata er migrert.

## Teststatus, bevarte endringer og øvrige funn

Kjørt før diskstopp:

- Kapasitetsvakt: først PASS, sist exit 75 med målingen over.
- Ordinært bounded App-bygg: **FAIL**, én ny konstruktørfeil; rettelsen er ikke bygget.
- `/usr/bin/python3 -m unittest discover -s scripts/tests -p test_managed_artist_recipient.py -v`: **8 tester PASS** etter klientendringene.
- Separat faktisk HavenAgentD-testprosess: **PASS** for lokal signering og klientverifikasjon; prosessen stoppet.
- `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`: **PASS**, 23 store literaler, alle 23 dekket av uendret baseline.
- `ci/test-suite-coverage.sh`: **PASS**, 345 suiter, 325 kjøres, 21 unntaksoppføringer. Ingen nye unntak/skips.

Ikke kjørt: vellykket Swift-bygg, noen Swift-test, produksjonsbinær-/test-hook-symboleksklusjon, full F1-claim/replay/parallelle/restartprøve, full privatnøkkel-lagrings-/transport-/logginspeksjon, ekte Sindre-klient, alle-lagre-kaldstart/F4, Darwin ACL-prøver, staging/prod/GUI, commit/push/ny CI. CI-vinduet er ikke startet; historisk F2-grønt er ikke F1-bevis.

Alle sju opprinnelige F1-utkast var autoriserte og ikke stoppgrunn. Lokale endringer omfatter nå ankerfiler, binding-helper, claim/forbruk, klient, tester/offentlig signaturfixture, testwrapper, CI-testflagging/filter og driftsnotat. De skal bevares til neste kjøring. Ingen fremmed endring er brukt som stoppgrunn. Ingen annens arbeid er endret. HavenAgentD- og øvrig Docs-WIP er bevart. Kildehash-/Git-sluttinventar er i `evidence-hvelv-f1-runde5-20260929/final-checks.json`.

Astra 5 er bindende: **F1/F5/F6/F9 blokkerer merge; F4/F7/F8 er også åpne før AP6.** Denne runden lukker ingen av dem. F5–F9-koden er ikke rettet her; F1-retrytesten erstatter ikke F4. Nye kildeutkast er ikke vurdert av Astra. Alle påviste rester må fortsatt håndteres, og eksisterende F2/F3-bevis skal bevares.

Læringsfangst: `L-2026-09-29-f1-klienten-hentet-offentlig-havenagentd` er skrevet i PR-ens driftsnotat, `applied` og docs-`sync` er gjennomført. Docs følger Git; dette er **lokalt**, siden ingen commit/push ble gjort. Global `check --strict` er rød på en fremmed åpen diskryddingspost (`L-2026-09-29-rydding-i-private-tmp-etter-bare-eier-alder-uten`), som er urørt. Læringsverktøyet varslet at målet ligger i et arbeidstre; det låste arbeidstreet og denne rapporten bevarer beviset, men Git-levering gjenstår.
