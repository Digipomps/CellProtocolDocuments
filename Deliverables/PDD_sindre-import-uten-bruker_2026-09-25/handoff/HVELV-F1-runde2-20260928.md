STATUS: DELVIS — eierankeravklaring, claim-integrasjon, Swift-verifikasjon, commit/push og CI gjenstår, head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 28.09.2026, for Kjetil og Losen. **F1 er fortsatt åpen. Ingen commit, push, merge, utrulling eller produksjonsovertakelse.** Lokale kilde-/testutkast er bevart i det bestilte arbeidstreet. De er ikke kompilert og er ikke koblet til claim. Denne rapporten erstatter forrige STOPPET-rapport; stoppet på gamle testrester gjelder ikke denne økten.

Arbeidsreferanse `PDD_sindre-import-uten-bruker_2026-09-25.F1`; utførende Codex, integrator Kjetil/Losen. Arbeidstre `CellScaffold/_wt-forvaltet-import-20260926`, gren `pdd/forvaltet-kunstnerimport`, [PR #270](https://github.com/Digipomps/CellScaffold/pull/270). F2 er LEVERT, ikke STOPPET. Starttreet var helt rent på SHA-en over. Ingen `.hvelv-test-root/` eller fremmede usporede filer fantes ved start; ingen gamle testrester ble flyttet. GitHub bekreftet OPEN og samme head både ved start og ved siste kontroll; [siste tilstand](evidence-hvelv-f1/pr-state.json). Docs-repoet hadde omfattende eksisterende WIP og hele PDD-mappen untracked; det er ikke ryddet eller committet.

## Avklaring som er sendt Kjetil, uten svar i denne økten

Dagens tekniske scaffold-eier og Kjetils personlige signeringsnøkkel er ikke dokumentert som samme tillitsrot:

- `Sources/ScaffoldKit/Application+ScaffoldOwnerRuntime.swift:124` løser scaffold-eieren fra runtime/default-vault, inkludert `VaporIdentityVault`.
- `Sources/ScaffoldKit/PaymentGateOwnerIdentitySupport.swift:44` kan hente signeringshåndtak fra serverens default-vault. Denne veien er uttrykkelig forbudt som F1-eiergodkjenning og er ikke brukt i utkastet.
- Eksisterende lokal signering finnes i `HavenAgentD/Sources/HavenAgentRuntime/AgentSignatureStatement.swift:353`, med signering ved `:390`; route i `HavenAgentD/Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:80` og MCP-adapter i `HavenAgentD/Sources/HavenAgentDMCP/HavenAgentMCPService.swift:960`. Signer er daemonens lokale identitet. En gyldig signatur derfra beviser ikke alene at nøkkelen er scaffoldeierens betrodde anker.
- HavenAgentD `origin/main` ble hentet, SHA `a9da717453ef3061d288fb5abbb29135c17fc720`. Hele `AgentSignatureStatement.swift` er byte-identisk med inspisert lokal fil: SHA-256 `7e1efeb0ec6e5410b8f193bc8ec97b7d30886bdb1acc36d9a5b879828c0f39ad`. Det lokale HavenAgentD-utsjekket har annen WIP; ingen fil der er endret av denne jobben.

Spørsmålet er om Kjetils lokale HavenAgentD-nøkkel skal provisjoneres som et eksplisitt offentlig eieranker, avgrenset til mottakerbindingen, eller om et eksisterende personlig eieranker skal brukes og hvor dette finnes. Ingen ny tillitsrot er valgt eller provisjonert på eget initiativ. Faktiske offentlige/private produksjonsnøkler, installert signeringsruntime og daemonkonfigurasjon er ikke lest. Ingen signeringsverktøy er kalt med Kjetils identitet.

## Lokale utkast og deres begrensning

Alle CellScaffold-linjer nedenfor gjelder det **ucommittede arbeidstreet**, ikke PR-headen. `B` = `Sources/App/Cells/ManagedArtistImport/ManagedArtistRecipientBinding.swift`, `T` = `Tests/AppTests/ManagedArtistRecipientBindingTests.swift`.

| Funn/krav | Fil:linje og nåtilstand | Testnavn / ville fanget originalfeilen? |
|---|---|---|
| F1: vilkårlig ny peer med korrekt token | Eksisterende `ManagedArtistIssuanceVault.swift:483` er **uendret**. Ingen claim-gate er koblet til utkastet. | Eksisterende positive tilfeldig-peer-test er **ennå ikke rettet**. Ingen ny kjørbar claim-regresjon beviser lukking av originalfeilen. |
| Eiersignert binding av hvert felt | B:55 definerer import/scaffold/slug/UUID/nøkkel/fingeravtrykk/utstedt/utløper/engangs-ID/schema. B:137 verifiserer detached HavenAgentD-konvolutt mot offentlig `trustedOwner` gitt av kalleren. Ingen produksjonskaller/ankeroppløsning ennå. | T:48 `testEveryBoundFieldMutationInvalidatesOwnerSignature`; T:84 `testWrongOwnerAndForgedEnvelopeRejected`. Ikke kjørt. **Nei som ende-til-ende-regresjon**: de tester et nytt hjelpe-API som gammel claim ikke kaller. |
| Entydig fingeravtrykk | B:14/:31/:47 normaliserer P256 33/65 til 33 byte; Ed25519 er 32 byte. Domeneseparert SHA-256, full lowercase `sha256:<hex>`. Bevisst forskjellig fra CPs interne descriptor og mandatets gamle bytehash. Python-klient: `scripts/managed_artist_recipient.py:32`. | T:11 `testClientAndServerFingerprintGoldenVector`, T:24 `testP256CompressedAndUncompressedHaveOneFingerprint`. Ikke kjørt i Swift. Python-motsatsene er PASS. Originalen hadde ingen F1-fingeravtrykkskontrakt; ingen kjørt mutation-test. |
| Riktig import/slug/scaffold, mottaker og kort levetid | B:76 validerer eksakt scope/mottaker og maks 600 sekunder. | T:65 `testValidSignatureStillNeedsExactScopeRecipientAndShortLifetime`. Ikke kjørt. Dekker helperkontrakten, **ikke** original claim ennå. |
| Ingen ukjente privatnøkkelfelter | B:174 streng roundtrip/16-KiB-grense for offentlig binding + konvolutt. Ingen signerings-/vault-oppslag i produksjonsutkastet. | T:105 `testUnknownAndPrivateFieldsAreRejectedAtEveryPayloadLevel`. Ikke kjørt. Lagringsinspeksjon for begge personenes nøkler gjenstår. |
| Positiv godkjent binding | B:137 lokal offentlig verifikasjon av eksisterende HavenAgentD-format. | T:40 `testApprovedBindingAndExistingAgentDEnvelopeVerify`. Testsignatur lages i fixture med to uavhengige nøkler, ikke virkelig klient/runtime. Ikke kjørt. **Nei**, viser ikke overtakelse. |
| Varig engangsforbruk, parallelle claims, replay og samme mottaker ved retry | Ikke implementert i record/claim; B:186 inneholder bare en foreslått digest-hjelper. | Alle nødvendige claim-/reload-/parallelle-/retrytester gjenstår. |
| F2-testrester | `scripts/test_managed_artist_import.sh:10/:20` lager egen rot under HAVEN `_to_delete/`, utenfor repoene, og rydder den via EXIT-trap. Bounded cache beholdes. | Den faktiske kjøringen ble blokkert av byggvakten, exit 75; etterpå fantes ingen `hvelv-f1.*`-rot. Normal testavslutning/crash ikke kjørt. Fjerner årsaken til rester ved denne testkommandoen; ingen generell opprydding av brukerens TMPDIR. |

`ci/test-filter.txt` har én ny suite: `ManagedArtistRecipientBindingTests`. Ingen skips/exclusions er lagt til eller endret. Sentral strict-oppførsel, avvisningstester, manifest/provisioner, package-pinner, eksisterende claim-/attestasjonskode og sikker lagringskode er urørt. Dette er kildekontroll, ikke ny kjørt strict-regresjon.

Klientverktøyet støtter foreløpig bare `fingerprint` og `prepare`. Det eksporterer offentlige utkast (`binding.json`, `sign-request.json`), signerer ikke og sender ingenting. Driftsnotatet ved `Documentation/Operations/Managed_Artist_Import_2026-09-28.md:7` skiller uttrykkelig mellom utkast, eksisterende signeringsroute og den manglende endelige claim-løypen. Det finnes ennå ingen verifisert full operatørsekvens for overtakelse.

## Kjørte kontroller

| Kontroll | Resultat / bevis |
|---|---|
| `scripts/run_swift_bounded.sh build --disable-sandbox` med 10 %-grense | **BLOKKERT / exit 75 før Swift**. 94,6 GiB ledig; 10 GiB reserve gir 84,6 GiB / 9 %. [Logg](evidence-hvelv-f1/build.log) |
| `bash scripts/test_managed_artist_import.sh` → bounded test `--disable-sandbox` | **BLOKKERT / exit 75 før Swift** av samme vakt; taskens rot ryddet. [Logg](evidence-hvelv-f1/tests.log) |
| `/usr/bin/python3 -B scripts/tests/test_managed_artist_recipient.py` | **4/4 PASS**: normalisering, fingeravtrykksvektor, kanonisk binding/request, avvisning av private/ukjente/ugyldige felter. [Logg](evidence-hvelv-f1/client-tests.log) |
| `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh` | PASS, 23 eksisterende baseline-oppføringer. [Logg](evidence-hvelv-f1/value-literals.log) |
| `ci/test-suite-coverage.sh` | PASS, 345 suiter / 325 dekket / 21 oppføringer i eksisterende exclusionliste. [Logg](evidence-hvelv-f1/suite-coverage.log) |
| `bash -n scripts/test_managed_artist_import.sh`, `git diff --check` | PASS |

Byggvakten er ikke svekket eller omgått. Ingen byggcache er slettet, ingen ad-hoc scratch-path eller lokal package-override er laget. Diskopprydding utenfor taskens egen midlertidige testrot er ikke utført. Ingen ny CI-kjøring er startet, så 60-minutters CI-venting har ikke startet. F2s historiske grønne CI er ikke bevis for disse utkastene.

## Videre arbeid

1. Avklar riktig personlig offentlig eieranker. Verifiser hvordan det bindes til nøyaktig scaffold uten at representant/importør/teknisk servereier kan velge ny mottakergodkjenner.
2. Fullfør Kjetils lokale signeringsløype med eksisterende vault og entydig fingeravtrykkvisning. Verifiser installert klient/daemon med testidentitet først. Ikke importer eier- eller kunstnerprivatnøkkel til serveren.
3. Koble binding+eiersignatur til claim; valider før frisk challenge og revalider under mutasjonslåsen. Lagre valgt mottaker, binding-ID/digest og forbruk atomisk med `transferring`. Definer retry/utløp eksplisitt; en utløpt initial binding må ikke åpne første claim, og en annen mottaker må aldri overta en påbegynt transfer.
4. Rett alle eksisterende positive claim-fixtures til uttrykkelig eiergodkjent kunstnernøkkel. Legg til alle bestilte negative integrationstester, frisk-signatur-replay, samtidighet, varig forbruk/reload, annen mottaker under retry og inspeksjon av begge personers private nøkler i alle relevante lagre. Nye helpertester alene lukker ikke F1.
5. Få byggkapasiteten innenfor uendret vakt; kjør bounded build/Swift-regresjon, gates og ny testrotopprydding. Fullfør driftsnotatets faktiske operatørsekvens.
6. Review diff, commit med bestilt PDD/F1-tekst og begge medforfatter-/sesjonslinjene, push #270 og vent på CI i maks 60 minutter. **Ikke merge.**

F4/F5/F6/F7/F8/F9 fra ASTRA-HVELV-2 er ikke rettet eller sertifisert i denne F1-jobben. Ingen kald runtime-gjenstart, virkelig ekstern bridgeklient, produksjonslagring, staging/prod, GUI eller reell Sindre-claim er testet.

Læringsfangst `L-2026-09-28-havenagentd-sin-lokale-sign-statement-kontrakt` er registrert, brukt til å oppdatere driftsnotatet og kjørt gjennom `applied`/`sync`. Verktøyet sier docs distribueres via Git; siden ingen commit/push er gjort, er denne læringen foreløpig lokal. Læringsledger og én Losen-logglinje er også skrevet i hovedarbeidsområdet. Ingen skills utenfor tillatte filrøtter er endret.
