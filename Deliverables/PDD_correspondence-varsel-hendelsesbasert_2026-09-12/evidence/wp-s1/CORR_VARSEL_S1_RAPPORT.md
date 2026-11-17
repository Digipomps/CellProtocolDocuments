Avvik fra «Dagens tilstand» ved kildegjennomgangen:

- `configureAgreementTemplate()` legger ikke selv til `feed`, men den lokale CellProtocol-koden oppretter standardavtalen med en `r---`-grant på `feed`: `CellProtocol/Sources/CellBase/Agreement/Agreement.swift:104` og `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:328`. «Bare eier» er derfor ikke en generell garanti ved en separat, signert avtale. Den nye `flow(requester:)` krever correspondence-godkjenning også når superklassens feedkontroll godtar en slik avtale.
- Før endringen lå `emitEvent` på linje 1921, emisjonen på linje 1935 og kallstedet på linje 543 i `AssistantCorrespondenceCell.swift`. Oppgitte linjetall var eldre.
- `Sources/App/Cells/Agent/AgentTrustPackageCell.swift` finnes ikke i dette worktreet. Eksisterende mønster for emitterinstallasjon er brukt fra `Sources/App/Cells/RichDocument/RichDocumentCell.swift:64`.
- Den lokale `CellProtocol/Sources/CellBase/Cells/Chat/ChatCell.swift:517` overstyrer `flow`, men filtrerer ikke publisheren; den registrerer abonnement og publiserer deltaker/status-hendelser.

# WP-S1 / HD-0072 — mottaker-skopet correspondence-feed

Status: skrevet, ikke verifisert

Formål: `purpose://candidate.corr-varsel.recipient-scoped-events`.
Dato: 2026-09-12. Arbeidsmappe: `_worktrees/cellscaffold-corr-varsel-s1`.
Grenen `pdd/corr-varsel-recipient-feed` er oppgitt i oppdraget; ingen Git-kommando er kjørt for å kontrollere eller endre den.

## Skrevet

- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift:4`: import av eksisterende HAVENRuntime-SPI og Combine/OpenCombine.
- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift:53` og `:188`: prosesslokal celle-eid emitter, opprettet under runtime-binding og opprettet igjen ved rehydrering. Ingen ny persistensmodell.
- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift:1588`: celle-spesifikk adgang bare for nøyaktig `r---` på `feed`, med nøkkelkontroll og aktiv, godkjent grant.
- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift:1599`: eier beholder den eksisterende publisheren etter superklassens adgangskontroll. Andre får bare correspondence-topicets `message.send` / `message.ack` med egen `message.recipientID`.
- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift:1626` og `:1635`: matching på `identityUUID` og SHA-256/base64url-fingeravtrykk av innmeldt Ed25519-nøkkel; sjekk av godkjent access request og kvittering, utstedelsestid, utløp, `revokedAt` og miljøbasert tilbakekall. Tvetydig binding til flere aktive principaler avvises. Filteret gjentar grantsjekken ved hver relevant hendelse uten polling.
- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift:551` og `:2000`: operasjonens emisjon bruker celle-eid emitter i stedet for innringerens feed-skriverett. Eksisterende fjerning av `message.content` beholdes; `inbox.list` bygger allerede metadata uten innhold.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1393`: ni nye tester og tilhørende lokale hjelpere. Eksisterende tester/hjelpere er byte-for-byte uendret, bortsett fra SPI-importen øverst i filen.
- `Documentation/Staging_Deployment.md:116`: kort avsnitt om feedkontrakten med den pålagte teksten «Last verified against code: 2026-09-12». Avsnittet sier uttrykkelig at dette er kildegjennomgang og at bygg, tester og brokjøring gjenstår.
- `CORR_VARSEL_S1_RAPPORT.md`: denne rapporten er skrevet i roten og ikke lagt til i Git.

## Tester som er skrevet

- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1393` — `testFeedWithoutGrantOrWithPendingApprovalThrowsStreamStateDenied`: Avslag med nøyaktig StreamState.denied uten grant, ved ventende godkjenning og selv med en vanlig signert feed-avtale.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1409` — `testFeedRejectsSameUUIDWithWrongKeyAndIdentityWithoutKeyControl`: Samme UUID med feil nøkkel, offentlig identitetskopi uten nøkkelkontroll og falsk eiernøkkel avvises.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1423` — `testActiveGrantReceivesOwnSendFromSenderWithoutFeedWriteAccess`: Aktiv mottaker får egen message.send fra en avsender med signedRequest-avtale, uten feed-skriverett. Andre keypaths og RWXS-rettigheter åpnes ikke.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1465` — `testRecipientFeedExcludesOtherRecipientsSendAndAck`: Andre mottakeres message.send og message.ack skjules; egen send og ack slipper gjennom med riktig recipientID/messageID.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1513` — `testInboxListAndMessageReadNeverReachRecipientFeed`: Vellykkede inbox.list og message.read gir ingen ekstra hendelser til mottakeren, selv når read returnerer innhold til den autoriserte innringeren.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1537` — `testOwnerKeepsAllOperationEventsAndNoFeedEventContainsMessageContent`: Eier beholder send/list/read/ack; både eierens og mottakerens hendelsespayload sjekkes rekursivt for fravær av content og for fravær av testmeldingskroppen i JSON.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1590` — `testExpiredOrRevokedGrantDeniesNewFeedAndStopsExistingSubscription`: Tilbakekall og kontrollert klokkeutløp avviser nye abonnement og stopper en eksisterende strøm; celle-eid synkron emisjon gjør negative sjekker uavhengige av ventetider.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1617` — `testRecipientFeedExcludesAdministrativeTopicAndMalformedEvents`: Administrativt topic, ukjent operasjon, manglende message/recipientID og feil payloadtype stoppes, mens eier ser hendelsene.
- `Tests/AppTests/AssistantCorrespondenceCellTests.swift:1649` — `testRecipientFeedAndCellOwnedEmissionSurviveRuntimeRebindingAfterDecode`: Grantfiltrering, avsenderens action-avtale og celle-eid emitter brukes igjen etter encode/decode og runtime-binding.

Testoppsettet bruker flyktige testidentiteter med ekte signering, invitasjon, eiergodkjenning, signert access-status og signerte meldingsoperasjoner. Ingen private produksjonsdata brukes. Objektasserts leser enkeltfelt eller kontrollert JSON; ingen nye tester sammenligner hele `ValueType.object`-verdier.

## Utførte statiske kontroller

- `ci/check-value-literals.sh`: exit 0. Regelens seks selvtester passerte. 28 eksisterende store literaler i Sources dekkes av gjeldende baseline; ingen nye overskridelser. Den endrede cellefilen står ikke i baseline.
- `python3 ci/check_value_literals.py Tests/AppTests/AssistantCorrespondenceCellTests.swift --max-entries 20 --baseline /dev/null`: exit 0, null overskridelser.
- `swift-format format` fra Xcode-toolchainen: exit 0 for begge endrede Swift-filer, uten parserdiagnostikk. Bare ny kode ble formatert; dette er ikke Swift-typesjekking eller et bygg.
- Sammenligning mot kopier tatt før redigering: eksisterende testfunksjoner/hjelpere er urørt, og nye linjer har ikke etterfølgende blanktegn.

Disse kontrollene kjører ikke AppTests og gir ingen runtime-konklusjon.

## Ikke gjort og hvorfor

- Ingen Swift-bygg eller Swift-testkjøring: oppdraget krever bygg utenfor denne sandkassen før annen status. Ingen byggrøtter eller dependency-oppløsning ble opprettet. `Package.swift` og `Package.resolved` er ikke endret.
- Ingen bro-/WebSocket-/HTTP-kjøring eller staging-kjøring. Testene er cellekontrakttester; faktisk brotransport og plattformkompilering gjenstår.
- Ingen HTTP-ruter, andre cellers autorisasjon, CellProtocol-kjerne eller avtaletemplate er endret. Ingen ny polling, sentral profilering eller meldingsinnhold er lagt til i hendelser.
- Ingen commit, staging eller push. `.git` er ikke lest eller endret; rapporten er ikke lagt til i Git.
- Ingen ny Explore-nøkkel eller endret get/set-skjema: endringen bruker eksisterende `flow(requester:)` og `feed`-adgang. Derfor er ingen generell Explore-katalogaudit kjørt.

Neste kontroll utenfor sandkassen er et avgrenset bygg og hele den berørte testklassen, med kapasitetssjekken og to jobber som runneren håndhever:

```sh
scripts/run_swift_bounded.sh test --filter AssistantCorrespondenceCellTests
```

Dette steget må rapportere faktisk bygg-/testresultat og etterfølges av brokjøring dersom HD-0072 skal gis en ende-til-ende-konklusjon.
