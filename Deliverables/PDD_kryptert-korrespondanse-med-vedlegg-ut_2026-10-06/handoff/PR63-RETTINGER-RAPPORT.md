# PR #63 — rettinger etter uavhengig kontroll

Kandidat: `66e165becf52e3f057d1596f23e05d7078b3bc2c`, gren `codex/korr-relasjonscelle-20261007`.
PR: https://github.com/Digipomps/CellProtocol/pull/63 (kladd). Kandidaten er pushet og alle fire CI-sjekker er grønne. PR-en er OPEN og fortsatt kladd, bekreftet etter CI.
Linjenumre gjelder kandidaten; filnavn nedenfor er kildefiler i CellProtocol.

| Funn | Retting (fil:linje) | Test | Utfall |
|---|---|---|---|
| MÅ 1: utløpt medlem i krypteringslisten | `CorrespondenceCell.swift:339`: aktive kontrakter, cutoff og eier; lat refresh ved sending/innboks | `testExpiredMemberIsNotEncryptionRecipient` | Grønn |
| MÅ 1: eldre aksept-refresh overskriver tilbakekall | `CorrespondenceCell.swift:346`: autorisasjonsrevisjon, refreshteller og lås | `testAcceptRefreshCannotOverwriteConcurrentRevocation` suspenderer den eldre snapshoten over tilbakekall | Grønn |
| MÅ 1 / BØR 4: endring under sending | `CorrespondenceCell.swift:611`, `GeneralAuditor.swift:535`: ny fingerprint-/mottakerkontroll og insert i samme synkrone autorisasjonsactor-operasjon | `testMembershipChangeWhileSendingRejectsCommit` | Grønn; ingen melding lagret |
| MÅ 1: endring under vedleggsforberedelse | `CorrespondenceCell.swift:1083`: captured fingerprint kontrolleres igjen etter storage-await | `testMembershipChangeDuringAttachmentPrepareRejectsResult` | Grønn |
| MÅ 2: navn i request, plan og indeks | `CorrespondenceAttachmentStorage.swift:71`, `:126`, `:366`: wire- og lagringsredaksjon; legacy-indeks skrives om; navn blir i kryptert manifest | `testWireAndDurableMetadataExcludeFilename`, `testLegacyIndexIsRedactedWhenLoaded`, `testRestoredCopyUsesHostProvisioningAndEncryptedFilename` | Grønn |
| MÅ 2: lokale kildestier/deskriptorer | `CorrespondenceCell.swift:1076`, `:1080`; `CorrespondenceAttachmentStorage.swift:126`: peer probe avvises, peer prepare tar bare krypterte chunks, lokale kilder er ikke persistente | `testHostAttachmentMetadataAndProbeDoNotDiscloseNameOrPath`, `testLocalSourcesAreNotPersistedOnHost` | Grønn |
| MÅ 2 / BØR 5: feiltekster røper interne detaljer | `CorrespondenceCell.swift:590`, `:1049`; `CorrespondenceAttachment.swift:76`: faste feilkoder, ingen underliggende feiltekst på wire | `testStorageErrorsHaveFixedDescriptions`; peer-probe-/prepare-avvisninger sjekker fast kode | Grønn |
| BØR 3: standardverdi sletter cutoffs | `GeneralAuditor.swift:504`: `revokedBefore` er påkrevd | Kompilering og alle 29 `ExternalAgreementAdmissionTests` | Grønn |
| BØR 10: én erase-feil låser hele lageret | `CorrespondenceAttachmentStorage.swift:207`: fortsetter andre oppføringer; feilede oppføringer kan prøves i neste purge; ingen permanent feillås | `testCleanupContinuesAfterOneFailureAndRetries` | Grønn |
| BØR 12: gjenopprettingsavvisning mangler positiv kontroll | `CorrespondenceRelationshipTests.swift:400`: samme restaurerte celle avviser gammel kontrakt og godtar fersk kontrakt etter cutoff | `testRestoredRevocationAlsoAllowsFreshContract` | Grønn |
| BØR 2: klokkeforskjell | `GeneralCell.swift:392`, `:1440`, `:1568`, `:2090`: fem sekunders ekstern toleranse, samme vindu i cutoff ved fjerning og signert tilbakekall; lokal gjeninnslipp trekker tidsforskyvningen fra varigheten | `testSmallExternalClockToleranceAndRevocationCutoff`, `testLocalReadmissionDoesNotExtendRequestedExpirationDeadline`, eksisterende action-expiry-prøve; 60 sekunders framdatering avvises | Grønn |
| BØR 6: UUID-liste uten kontrakt | `CorrespondenceCell.swift:664`: lokal eiersnarvei oppretter ekte eiersignert kontrakt og krever subjektets nøkkelbevis | Alle eksisterende `CorrespondenceCellTests` | Grønn |
| BØR 8: delt medlems-/vedleggstilstand | `CorrespondenceCell.swift:102`: medlemsfelter, sendercelle-oppslag/innsetting og reservasjoner beskyttes av lås; autorisasjon har actor-revisjon | Samtidighetsregresjonene og eksisterende 128 parallelle sendinger/snapshots | Endelig normalport og CI-TSAN grønne |

## Porter og CI

- Fokusert skriptjobb i bane b: r5 før lokal utløpsrettelse, bygg/test exit 0, **70 tester, 0 feil**.
- Endelig kompatibilitetsport i bane b: r2 på `66e165b`-treet, bygg/test exit 0, **112 tester, 0 feil** (Correspondence, ExternalAgreementAdmission, DeviceIngress og BridgeChannelTransport). Første kompatibilitetsforsøk hadde to assertions i den nye fixture-prøven; standardbetingelser var ikke oppfylt. Fixtureens betingelser er nå eksplisitt satt som i eksisterende prøver, alle assertions beholdt.
- Tidligere forsøk: r1/r2 stoppet ved kompilering; ingen tester kjørt. r3 kjørte 70 tester og hadde fire feil. Alle fire er rettet før r4; resultatene skjules ikke.
- Thread Sanitizer i bane b på `adfb453039aef137ec829e807ff6a8c542438e42` (før styrket probe-prøve og senere lokal utløpsrettelse; ikke et TSAN-bevis på endelig hode): bygg/test exit 0, **70 tester, 0 feil**, ingen rapportert datarace.
- Hele grunnmurporten r1: Swift meldte `Build complete`, men kjeden returnerte exit 1 før teststart; ingen kompilatorfeil funnet. Årsaken til skriptavslutningen er ikke isolert. Råresultat og bygglogg er bevart lokalt. Ingen tester ble kjørt i r1.
- Hele grunnmurporten r2 på `f6a0ddb`: bygg exit 0; **1621 bestått, 5 hoppet over, 1 mislykket test** (to assertions). Eksisterende action-expiry-prøve fant forlenget lokal kontraktutløp. Rettingen er i `66e165b`, eksisterende test uendret.
- Hele grunnmurporten r3 på `66e165b`: igjen `Build complete`, skript exit 1 før tester. Kort separat dry-run GC og størrelsesmåling ga begge exit 0; avslutningsårsaken er ikke isolert. R1/r3 regnes ikke som grønne porter.
- Hele grunnmurporten r4 på endelig kandidat: **bygg exit 0 (93 s), test exit 0 (121 s); 1623 bestått, 5 hoppet over, 0 feil — totalt 1628 testutfall over alle XCTest-targets**. Største suite rapporterer 1599, derfor brukes per-case-totalen fra skriptet. Ingen test fjernet. Verktøykopien fikk bare ekstra exitkode-/stderr-logging, ingen endret gate. Kommando: `bash HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh codex/korr-relasjonscelle-20261007`.
- CI: **4/4 SUCCESS** på `66e165becf52e3f057d1596f23e05d7078b3bc2c`. macOS-jobbens normale testtrinn, Thread Sanitizer-trinn (inkludert CorrespondenceRelationshipTests) og kontroll av sårbar downstream-pin er alle SUCCESS.
- Push lyktes; første umiddelbare PR-head-assertion stoppet oppfølgingen. Idempotent fortsettelse bekreftet riktig hode uten ny push/CI-rerun. Etter alle sjekkene ble samme head og `isDraft = true` kontrollert igjen. **Ingen merge eller tag.**

| CI-sjekk | Status | Bevis |
|---|---|---|
| regression | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37711012408/job/113096687315) |
| bounded synthetic runtime matrix | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37711012321/job/113096687245) |
| Persisted Cell file bounds | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37711012393/job/113096687806) |
| Vapor identity vault strict storage | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37711012303/job/113096687211) |

## Bevarte tester og kompatibilitet

Ingen eksisterende test er fjernet eller svekket. Utløpsprøven bruker nå fixtureens betrodde lagerrot i stedet for å hente en lokal sti fra snapshotet. Den beholder positiv kontroll av chunk før utløp og fravær av chunk etter utløp, og sjekker at snapshotet ikke inneholder lagerrot.

Kontraktens offentlige subjektrolle lagres som `correspondenceContractSubject`, adskilt fra meldingssubject. Dekoding gjenoppretter rollen før signaturkontroll; signerte byte endres ikke. Eldre snapshotform dekodes fortsatt. Den eksisterende testen for fravær av klare subject/content-felt er beholdt.

Et gjenopprettet vedleggslager må re-provisjoneres med `configureAttachmentStorage(root:requester:)` fra vertens betrodde konfigurasjon. Uprovisjonert vedleggsbruk avvises. Gjenopprettingsprøven viser faktisk henting av de samme krypterte copy-bytene og klientens filnavn fra det krypterte manifestet.

## Øvrige BØR og avgrensninger

- BØR 1: signert revocation krever fortsatt en installert kontrakt. En ikke-framlagt invitasjon stoppes med eksisterende eiersikret `removeMember`; `testOwnerRemovalBeforeAdmissionBlocksPreviouslySignedContract` er grønn. Ny wire-kommando for cutoff uten kontrakt utvides ikke i denne rettingen.
- BØR 7: vedleggslesing krever nå aktiv autorisasjon hos leseren, ikke fortsatt medlemskap hos historisk avsender. Opprinnelig melding/avtale/avsenderbinding kontrolleres fortsatt i lageret. Begge retninger er prøvd; egen henteprøve etter avsenderens tilbakekall er ikke kjørt.
- BØR 9: peer prepare kan ikke be verten lese lokal kildefil eller utstede kildekrypteringsnøkkel. Den direkte lokale kilde-API-en er fortsatt for avsenderens egen maskin og må re-registreres etter omstart; lokale reference/fetch-on-demand-prøver er beholdt. Ingen påstand om sikker stagingkobling av denne lokale API-en.
- BØR 11: generelt avslag på `purpose != nil && target == nil` for alle legacy-kontrakter er utsatt som en separat kompatibilitetsendring. Relasjonscellens eksterne innslipp krever allerede både eksakt binding og signert formål.
- BØR 12: debug-policy settes eksplisitt til false; gamle assertions og avvisningsprøver er beholdt. Nye wire-avvisninger kontrollerer konkrete koder. Hele det eldre `.rejected`-API-et er ikke erstattet med et nytt resultatformat.
- Klienter må beholde original metadata for det krypterte manifestet; vertsplanens tomme navn skal ikke brukes som filnavn. Dette er beskrevet i kandidatens vedleggs- og relasjonsdokumentasjon.
- Dette er CellProtocol-verifikasjon, ikke deploy, staging-E2E eller nye installerere. PR-en skal forbli kladd.

## Gjenbrukbar integrasjonsoppskrift — læring L-2026-10-08-ved-klientintegrasjon-av-pr63-ma-original

Gjelder den testede PR63-kandidaten, ikke en påstand om at main eller staging har denne kontrakten:

1. Klienten beholder original `CorrespondenceAttachmentMetadata` før request-encoding. Bygg det krypterte `CorrespondenceAttachment`-manifestet med denne, ikke med den redigerte vertsplanens metadata.
2. Verten bevarer relasjonens celle-UUID og sin betrodde lagerkonfigurasjon uavhengig av Cell-snapshotet. Etter decode kalles `configureAttachmentStorage(root:requester:)` før vedleggsoperasjoner.
3. Bekreft både navnet i det åpnete indre manifestet og byteidentitet etter snapshot/decode/re-provisjonering. Kandidatens `testRestoredCopyUsesHostProvisioningAndEncryptedFilename` viser dette i lokal testprosess; det beviser ikke staging eller klientimplementasjonen i andre repoer.

Læring L-2026-10-08-pr63-local-cutoff-expiry: en lokal signering forbi cutoff må ikke flytte bestilt utløpsfrist. Kandidaten trekker tidsforskyvningen fra heltallsvarigheten, konservativt avrundet opp. Fullporten må beholde action-expiry-prøven og positiv lokal gjeninnslipp, i tillegg til tilbakekallprøvene.

STATUS: LEVERT
