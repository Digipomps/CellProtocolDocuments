STATUS: LEVERT — anbefaling: ikke merge, 13 funn (10 blokkerer)

Astra, kontroll 4 av CellProtocol PR #53. Dato: 2026-09-28. Beslutningseier: Kjetil.

Den nye nøkkelutvekslingen lukker den opprinnelige kryptografiske N07-feilen på den undersøkte bytegrensen: et mellomledd som videresender ekte håndtrykk får ikke meldingsnøklene. Jeg fant ingen konkret signatur-, KDF- eller AEAD-forfalskning i denne konstruksjonen. **Peer-kanalen som helhet er likevel ikke klar for merge.** Det finnes resterende feil i invitasjonsbinding, leveringsrekkefølge, NI, ressurslivsløp og mottakerens behandling av kontaktbevis. Grønn CI dekker ikke disse feilforløpene.

Alle nye funn er tatt med, også eksisterende kode som nå ligger i den undersøkte peer-kjeden, dokumentasjonsfeil, en dokumentert personvernbegrensning og et funn som gjelder en udokumentert ressursgrense fremfor en målt uttømming. N19, N21 og N22 er ikke selvstendige mergeblokkere; de skal også følges opp med retting etter Kjetils instruks. Tidligere N05 og eksterne produksjonsporter telles ikke på nytt.

**Revisjon, metode og lesegrense**

Begge implementørhandoffene er LEVERT. Den siste, `CP53-N07.md`, oppgir **`1b8efe1cbca33997facf50a37ee0fbfff9dc7b14`**. GitHub bekreftet samme faktiske head på [PR #53](https://github.com/Digipomps/CellProtocol/pull/53), OPEN. Dette er vurdert revisjon; ingen fallback var nødvendig. Alle CP-kilder er lest fra commitobjekter med `git show`, `git grep` og `git diff`, ikke fra det skitne hovedarbeidstreet. Den dedikerte PR-worktreen var ren på denne headen.

| Prefiks | Bane relativt til HAVEN, på vurdert head |
|---|---|
| `S` | `CellProtocol/Sources/CellApple/EntityRadar/ScannerService.swift` |
| `E` | `CellProtocol/Sources/CellApple/EntityRadar/EntityScannerCell.swift` |
| `P` | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgePeerChannelAuthentication.swift` |
| `R` | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgePeerRecordLayer.swift` |
| `G` | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelTransport.swift` |
| `L` | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelSession.swift` — også `BridgeChannelLimits` |
| `A` | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelAuthentication.swift` |
| `B/` | `CellProtocol/Sources/CellBase/Cells/Bridging/` |
| `T` | `CellProtocol/Tests/CellBaseTests/ScannerPeerAuthenticationTests.swift` |
| `V` | `CellProtocol/Tests/CellBaseTests/BridgePeerRecordLayerTests.swift` |
| `M` | `CellProtocol/Tests/CellBaseTests/ScannerMultipeerProcessTests.swift` |
| `D` | `CellProtocol/Documentation/BridgePeerChannelV2.md` |
| `CP/` | `CellProtocol/` |

Lest: alle tre tidligere Astra-rapporter, begge bestilte implementørhandoffer, hele P/R/G/L/A/S/D, WS-klientoperasjonen, hele T/V/M og invitation-testfilen. Base, mux, Identity/verifikator/signing challenge, diagnostikk og EntityScanner er lest i de relevante utsnittene som refereres nedenfor. For E omfatter dette kanalens kontakt-/probe-dispatch, kontaktrequest/aksept, signaturkontroll, encounter-bygging/lagring, invitasjons-/lost-/status-callbacks og tilstandsovergangene. **Resten av E, hele Base/mux/resolver, øvrige celler og separate advertisement-protokoller er ikke lest i sin helhet i denne kontrollen.** Bokkapitler/SECURITY er brukt som bakgrunn, ikke som erstatning for head-koden. Primitive- og protokollkilder er kontrollert på nettet.

Dette er den bestilte lese- og vurderingsjobben. **Ingen nye CP-bygg, testkjøringer, utnyttelsesforsøk, iOS-kjøringer eller radioprøver er utført av meg.** Nye feilforløp er kildebaserte slutninger. Eksisterende lokale rålogger, workerartefakter og CI er kontrollert nedenfor. Ingen ekte private nøkler er inspisert. En kildegjennomgang og grønne tester kan ikke gi et ubetinget matematisk løfte om fravær av alle sårbarheter.

**1. N07, N08 og N09**

| Tidligere funn | Konklusjon på denne headen | Ville regresjonen fanget originalfeilen? |
|---|---|---|
| **N07: A–M–B kan lese/endre trafikk etter videresendt proof** | **Lukket for dette kryptografiske feilforløpet.** Begge signaturer binder begge efemære nøkler og hele hello-paret (`P:60–70,91–123`). Retningsnøkler avledes fra X25519 og transcript (`R:20–38`); all applikasjonsdata går gjennom seal/open ved fysisk adapter (`S:98–104,127–145`). Begge sider krever beskyttet record 0 før Base (`G:99–126,203–235`). Ressurs- og applikasjonsfunnene nedenfor består. | **Ja på adapterens bytegrense.** `T:410–430` videresender fem virkelige handshake-meldinger og leverer faktiske flows begge veier. Gammel plaintext-transport ville feilet ciphertext-/JSON-/markørkontrollene. Den gyldige plaintext-response-varianten ved `T:455–463` ville tidligere kunne leveres, men må nå avvises. `T:467–493` bytter hver efemær nøkkel og prøver signaturkontrollen. Tilfeldig ødelagt JSON alene ville også blitt avvist før N07; derfor er ikke alle de andre negative variantene isolert sett bevis for originalfeilen. |
| **N08: discovery overtar etablert gate, gamle callbacks rammer ny generasjon** | **Den etablerte fysiske bindingen og de opprinnelige callback-forløpene er rettet. N08 kan ikke lukkes bredt for hele invitasjons-/mottakerlivsløpet.** `S:65–89,450–460,648–675,803–825,1064–1098,1127–1130` fryser peer/session/transport og fanger riktig objekt før async arbeid. **N11** viser gjenværende bindingstap før gate-oppretting; **N13** viser at generasjonen ikke følger alt senere mottakerarbeid. | **Ja for de opprinnelige etablerte rutene.** `T:234–276` bruker A/B/C, prøver discovery-kollisjon, måler fysisk mottaker og lar C forsøke å konsumere Bs ventende cid. De direkte mapping-/mottakerassertene ville fanget gammel discovery-routing selv om AEAD nå også beskytter innholdet. `T:279–353,557–586` prøver faktiske Base-cid-kollisjoner, gamle bytes, fanget gammel transport, sen feil og fungerende søsken. De prøver ikke N11s pending/accepted-vindu eller Es avkoblede mottakeroppgaver. |
| **N09: rå iOS NI-broadcast uten gate/kvote** | **Den konkrete rå utsendingen er fjernet.** Det eneste leste `MCSession.send` i S er `S:458`; iOS arkiverer og bruker felles helper ved `S:852–858`, som velger aktive gates ved `S:838–848`. **Dette lukker utsendingsfeilen i kilde, men sertifiserer ikke NI-funksjonen. N12 består.** | Helper-testen `T:356–407` prøver aktiv B, pending/revoked C, fullført handshake etter broadcast og sendbyteavslag. Den ville oppdaget feil peer-utvalg i helperen. **Den ville ikke oppdaget at en rå `#if os(iOS)`-utsending ble gjeninnført ved siden av helperen**, og prøver ikke ekte arkiv/dekode, NISession eller korrekt peer for måleresultatet. iOS-banen er ikke bygget/testet i det leverte beviset. |

M i N07-testen er `ScannerControlledWire`, ikke en tredje Scanner eller to levende MC-forbindelser terminert av en tredje prosess (`T:412,626–657,742–758`). Seamen gir likevel M den relevante evnen til å lese, holde, endre og videresende alle bytes uten nøkler. Det er meningsfylt adversarielt adapterbevis, **ikke en utført treprosess-/treradio-MITM-prøve**. Den reelle toprosessprøven har bare ærlige endepunkter.

**2. Nye funn — alle skal følges opp**

**N10 — Middels, blokkerer: ordnede records gir ikke ordnet levering til konsumenten.**

Kilde: `S:126–145,1189–1206`; `G:263–277,311–321`; `B/BridgeBase.swift:1816–1880`. Test: `T:534–554`.

`receiveTail` venter bare på forrige **preparation**. Applikasjonsdispatch kjøres i en separat Task som ikke inngår i halen. Record n+1 kan derfor åpnes og få sin dispatch-Task kjørt før record n får sin. Deretter oppretter gaten enda en Task. Base har ingen gjenoppretting av record-rekkefølge før en feed-response publiseres. To gyldige, korrekt ordnede feed- eller out-of-band-meldinger kan komme frem i motsatt rekkefølge; en senere verdi kan overskrives av en eldre. Det krever ikke forfalsket chiffertekst. Det er ikke krav om at alle uavhengige RPC-er skal fullføre i sendeorden, men en ordnet flow må bevare leveringsrekkefølgen.

Testen sjekker stigende wiretellere og deretter `Set(observer.flows.map(\.title)).count == 20`. Det oppdager tap/duplikat, ikke omordning. **Retting:** bevar ordnet opptak/levering for flows og andre ordensavhengige meldinger etter dekryptering. Signeringssvar må fortsatt kunne betjene en ventende operasjon; å vente på hele cellekallet i én mottakerløkke kan introdusere deadlock. Regresjon: hold første dispatch etter åpning, la neste record ankomme, og krev eksakt konsumentrekkefølge og fungerende origin-signatur-RPC.

**N11 — Middels, blokkerer: discovery kan fortsatt bryte bindingen til pending/akseptert invitasjon.**

Kilde: `S:187–192,422–428,552–561,624–656,991–1003,1037–1044`. Test: `CP/Tests/CellBaseTests/ScannerServiceInvitationTests.swift:8–22,87–109`; `T:234–276`.

Accepted-state lagrer endpoint etter remoteUUID, uten den aksepterte MCPeerID-en. Discovery-kollisjonsvakten for invitasjoner forutsetter at `_foundPeersDict[remoteUUID]` fortsatt finnes. Forløp: A inviterer/aksepterer B; før gate finnes kommer `lostPeer(B)` og fjerner begge discovery-mappinger. C annonserer deretter Bs UUID. Det finnes ingen bound gate og ingen `existing`-mapping, så C tas inn selv om `invitationEndpoints[B]` eller en pending B-invitasjon består. Bs rediscovery kan nå bli avvist som kollisjon mot C. Ved pending invitasjon kan `respondToInvitation(B)` ikke lenger finne Bs handler. Dette er et konkret tilgjengelighets-/bindingsbrudd; jeg hevder ikke at C dermed får Bs kryptografiske principal.

I tillegg er fjerning av pending og installasjon av accepted endpoint to adskilte `withState`-seksjoner (`S:553–560`): en discovery-callback kan passere mellom dem. Utgående endpoint ryddes heller ikke ved invitetimeout uten opprettet transport; den kan påvirke senere crossed-invitation-valg (`S:640–642`).

**Retting:** la pending og accepted invitasjon eie uforanderlig peer/session/endpoint/instans, uavhengig av discovery-indeksen. Gjør akseptovergangen atomisk; pensjoner utgående og aksepterte oppsett som aldri blir til kanal. Test discovery-loss og C-kollisjon både før og under aksept, deterministisk race mellom de to nåværende låsseksjonene, timeout og ny gyldig invitasjon. Dagens test kolliderer først etter etablerte gates og dekker ikke dette.

**N12 — Høy, blokkerer: NI-token og nærhetsresultater er ikke bundet til riktig peer/generasjon.**

Kilde: `S:344–352,852–878,894–918,1104–1113,1154–1178,1244–1274,1281–1337,1343–1382`; opprydding `S:526–542,803–825,1073–1086`.

Alle peers deler én `niSession`, én `peerDiscoveryToken` og ett `connectedRemoteUUID`. Mottatt token mister den autentiserte transportbindingen; `userUuid` sendes til en funksjon som ikke bruker den, og det faktiske `remoteUUID` brukes ikke ved installasjon. Forløp: B er valgt/nylig tilkoblet; allerede autentisert C sender sitt eget gyldige NI-token. C overskriver den globale tokenen. NISession-resultat for Cs token rapporteres nå under Bs `connectedRemoteUUID`. Dette krever ingen forfalskning av Bs kanalbevis.

`startup()` lager ny NISession ved hvert vellykket peer-oppsett, men beholder gammel peer-token. Close/revoke/stop invaliderer ikke NI-tilstanden her. Delegate-callbackene kontrollerer ikke at `session === niSession`, og timeout/suspension/invalidation kan kjøre gammel konfigurasjon eller starte på nytt. Tokenoppdatering skjer fra mottakeroppgaver, mens startup og NI-callbacks bruker andre køer; feltene har ingen felles actor/lås. Dermed kan også utløpt eller gammel generasjon levere feilmerket nærhet eller påvirke ny sesjon.

**Retting:** bind NI-livsløp og token til autentisert fysisk peer, principal og kanalgenerasjon. Enten ha eksplisitt valgt enkeltpeer med streng seleksjon, eller separate støttede NI-sesjoner; ikke la «siste token» velge identitet. Isoler tilstand på én executor, invalider ved pensjonering og avvis callbacks fra gamle NISession-objekter. Bygg iOS og prøv ekte tokenarkiv/dekode, B/C samtidig, gammel token/callback, reconnect, revokasjon og stop. macOS-helperen kan ikke bevise dette.

**N13 — Høy, blokkerer: out-of-band-arbeid slipper kvote og generasjon før den faktiske behandlingen er ferdig.**

Kilde: `S:1201–1204,1154–1182`; `E:61–78,1235–1249,1346–1365,1504–1526,1614–1644,1647–1690`. Adapteropptak: `S:118–150,1127–1130`.

Gatens `withAuthenticatedWork` avsluttes når den synkrone callbacken returnerer. Den virkelige EntityScanner-delegaten starter en ny, uregistrert `Task`; kontaktverifikasjon, Perspective/resolver og encounter-lagring kan derfor fortsette etter at både receive- og gatekvoten er frigitt. Denne Task-en får bare remoteUUID, ingen fanget session/generasjon, og er ikke kansellert av gate-close. En gyldig kontaktaksept kan bli liggende i et await, kanalen kan lukkes/gjenopprettes, og gammelt arbeid kan deretter oppdatere tilstand eller lagre et encounter uten ny livsløpskontroll. Dette beviser ikke automatisk uautorisert celleadgang, men bryter påstanden om at kvote/generasjon følger arbeidet til slutt.

En enklere DoS trenger ikke hengende await: en autentisert peer sender mange ulike `probeDetailRequest.requestId` eller kontaktrequest-ID-er. `pendingDetailRequests` har ingen antallsgrense/TTL ved innsetting; `pendingIncomingRequests` beholder også ugyldige signerte payloads etter verifikasjonsforsøket. Momentane gatekvoter begrenser ikke akkumulert lagring. De samme dictionaryene leses/endres fra uavhengige Tasks og discovery-/lost-callbacks uten felles isolasjon. GeneralCell er en klasse, ikke en actor som serialiserer disse metodekallene.

Også før gate-dispatch finnes oppgaver uten felles opptak: `didReceive` starter en setup-Task per frame, og køavslag lager en ny Task per avslag. Den lokale 64/4 MiB-grensen er nyttig, men er ikke et globalt regnskap for hele denne kjeden.

**Retting:** behold eksisterende ressurslease til faktisk asynkron konsumentbehandling er ferdig, før session/generasjon videre og revalider ved sikkerhetsrelevante await-grenser. Samle state-mutasjoner på én executor; sett per-peer/globale antalls-/bytegrenser og TTL for pending kontakt-/detaljdata, og rydd dem ved pensjonering. Start setup én gang og begrens avvisningsarbeid før Task-allokering. Test med den virkelige EntityScannerCell, suspendert verifikasjon/resolver/lagring, reconnect/revoke, mange request-ID-er og TSAN. ScannerStatusObserver i T returnerer synkront og avslører ikke dette.

**N14 — Høy, blokkerer: MC resource/stream er ubegrensede sideinnganger uten peer-gaten.**

Kilde: `S:1133–1142` sammenholdt med gateinngangen `S:1127–1130`.

En invitert MC-peer kan bruke `sendResource` eller `startStream` i stedet for `send(Data)`, også før appens proof er ferdig eller etter logisk revokasjon. De tre callbackene logger bare. De sjekker ingen kanal, avbryter ikke `Progress`, lukker ikke stream og bruker ingen byte-/arbeidskvote. Ressursoverføringen kan derfor oppta nettverk og midlertidig lagring uten noen `HPC2`-record. Dette er en ressurs-sideinngang, ikke påvist dispatch til en celle. Apple beskriver at ressursen skrives til midlertidig fil, og at mottakerens Progress kan avbryte den: [sendResource-dokumentasjon](https://developer.apple.com/documentation/MultipeerConnectivity/MCSession/sendResource%28at%3AwithName%3AtoPeer%3AwithCompletionHandler%3A%29?changes=__9).

**Retting:** avvis/lukk ubrukte streams og kanseller ubrukte ressursoverføringer ved første callback, med korrekt peer-/generasjonsbinding og begrenset feilhåndtering. Hvis de skal støttes, kreves eksplisitt autentisert, kryptert og kvotert protokoll. Test stor ressurs og mange streams på faktisk MC før auth, etter revoke og med en frisk søskenpeer. T/V/M bruker bare Data-meldinger.

**N15 — Middels, blokkerer: logisk close frigir ikke den fysiske MC-forbindelsen.**

Kilde: `S:156,377–385,462–466,478–480,803–825`; `G:397–416`; `L:164–168`.

Gaten rydder og frigir transportreservasjonen etter `ScannerPeerTransport.close()`, men den funksjonen fjerner bare appens registreringer. Den kobler ikke peer fra MCSession. Etter falskt proof, timeout, ugyldig record eller revokasjon kan en ondsinnet peer bli værende i `mcSession.connectedPeers`, holde fysisk kapasitet og bruke N14-sideinngangene. Friske søsken må ikke ofres for å få ut den ene peer-en. Dagens felles MCSession gjør dette til et konkret adapterproblem, ikke bare en manglende `close`-assert.

Apple dokumenterer at `disconnect()` forlater sesjonen, mens `cancelConnectPeer` gjelder tilkoblingsforsøk; det er ikke dokumentert som utkastelse av en allerede tilkoblet enkeltpeer. Se [MCSession](https://developer.apple.com/documentation/multipeerconnectivity/mcsession) og [cancelConnectPeer](https://developer.apple.com/documentation/multipeerconnectivity/mcsession/cancelconnectpeer%28_%3A%29?language=objc).

**Retting:** ha en støttet fysisk pensjoneringsstrategi som isolerer feilende peers, eksempelvis forbindelse/sesjon per peer hvis MC-API-et krever det. Behold reell fysisk ressurs i regnskapet til den er borte. Test en motpart som ignorerer app-close, kapasitet over gjentatte feil, naturlig expiry og fortsatt trafikk hos frisk søsken. `bridgeDelegateCount == 0` og `retainedConnectionCount == 0` i mock-seamen beviser ikke fysisk frigjøring.

**N16 — Middels, blokkerer: discovery og invitasjonskøen er uten egne opptaksgrenser.**

Kilde: `S:275–285,311–321,568–594,624–644,953–969,981–1008`; gatekvote begynner ved `S:661–663` / `L:248–254`.

Før noen bruker har godkjent kanal, kan mange oppdagede MCPeerID-er/UUID-er fylle discovery-tabeller, pending handlers, timeout-arbeid og UI-events. Ingen global/per-peer antalls-/byte-/rategrense er brukt her. Full navneliste bygges ved hvert funn. Gategrensen på pending forbindelser hjelper først ved `prepareBridge`, altså for sent for disse ressursene. Timeout begrenser varighet per innkommende invitasjon, ikke antall innenfor vinduet. Utgående accepted-state uten ferdig transport har i tillegg N11s manglende pensjonering.

`source: remoteUUID` ved `S:663` er en uverifisert discovery-streng, så per-source handshakegrensen kan ikke omtales som en stabil angripergrense; UUID-rotasjon gir nye bøtter. Den globale grensen består — dette er ikke ubegrenset opptak gjennom selve L.

**Retting:** begrens discovery/invitasjoner og deres tasks/metadata før lagring og publisering, med globalt tak og begrenset rate-/levetidsregnskap. Bind source til beste tilgjengelige fysiske kontekst, og beskriv Sybil-begrensningen ærlig. Test mange unike peers og metadata uten brukeraksept, kvote+1, timeout/cleanup og at en legitim invitasjon fortsatt håndteres. Invitation-testens 100 kall gjelder samme peer og dokumenterer ikke denne belastningen.

**N17 — Middels, blokkerer: «per key»-kvotene kan nullstilles med nytt selvoppgitt identity-UUID.**

Kilde: `L:87–95,105–120,197–205,324–327`; `A:22–47`; `CP/Sources/CellBase/Identity/IdentitySigningChallenge.swift:218–231`.

`maximumConnectionsPerKey`, verified-handshake-rate og ressursgrenser grupperer etter `principal = hash([domain, identity.uuid, fingerprint])`. UUID-en er selvoppgitt og det finnes ingen unik nøkkel→UUID-binding i kanalopptaket. En peer kan bruke **samme private nøkkel** og signere komplette, korrekte håndtrykk med stadig nye UUID-er. Hver får ny «key»-bøtte. P256 kan dessuten representeres komprimert eller ukomprimert; dagens fingerprint bruker de rå bytes og normaliserer ikke disse representasjonene. Globale grenser stopper fortsatt totalen, men de navngitte per-key-grensene gjør ikke det de lover.

**Retting:** behold den sikkerhetsbundne principalen for autorisasjon, men bruk en separat kanonisk nøkkelidentifikator for nøkkelkvoter og nøkkelrate. Normaliser støttede offentlige nøkkelrepresentasjoner. Test én nøkkel med mange UUID-er og begge P256-encodings, fylt kvote, avslag uten undertelling og en uavhengig nøkkel som fortsatt virker. Dette er kvoteomgåelse, ikke en påstand om at angriperen får en annen principals grants.

**N18 — Middels, blokkerer ressursgarantien: sendbytekvoten teller MC-innlevering, ikke utestående levering.**

Kilde: `G:365–387`, særlig `defer releaseSend`; `S:98–104,450–458`; `L:137–149`. Tester: `T:399–407,589–602`.

`await physical.sendData` avsluttes når det synkrone `MCSession.send` har returnert. Apple sier uttrykkelig at denne metoden er asynkron/nonblocking og at vellykket retur betyr **lagt i leveringskø**, ikke levert: [sendData](https://developer.apple.com/documentation/multipeerconnectivity/mcsession/send%28_%3Atopeers%3Awith%3A%29?language=objc). Dermed kan en langsom peer ha flere tidligere records stående i MC-køen mens gatens pending-byte-regnskap igjen er null. 32 samtidige sends begrenser ikke mange sekvensielle innleveringer. På mottakersiden kommer `Data` først etter komplett mottak; grensen ved `S:120` beskytter ikke reassembly-minnet før callbacken.

Dette er en **påvist regnskaps-/verifikasjonsgrense**, ikke en måling av at Apples interne kø er uendelig eller at maskinen faktisk gikk tom. Eksisterende tester viser at én for stor innlevering avvises og overhead telles; de viser ikke et samlet tak under nettverksmottrykk.

**Retting:** etabler og mål en bounded flytkontroll-/leveringsgrense som faktisk dekker adapterens utestående bytes, samt en dokumentert grense for ingress/reassembly. En autentisert kvitterings-/vinduordning eller annen egnet transportmekanisme må selv være bounded og generasjonsbundet. Ikke slipp kvote fordi kølegging lyktes. Kjør langsom/manglende mottaker, vedvarende feed, store rammer og close mens bytes står i kø; mål minne, antall records og friske søsken.

**N19 — Lav, ikke selvstendig mergeblokk: dekryptert payload kan dumpes i diagnostikk.**

Kilde: `B/BridgeBase.swift:1026,1830,1846,1866,1883,1974`; `CP/Sources/CellBase/Cells/CellRuntimeEnvironment.swift:20,233–247`.

Når bridge-diagnostikk er aktivert, logger ukjent response-cid hele `BridgeCommand`, og flere feilstier interpolerer hele payload/description. Et legitimt, men sent svar med privat strenginnhold kan dermed havne i logg selv om peer-wire er kryptert. Loggføring er av som standard; jeg har ikke observert en faktisk privat logglekkasje. Jeg fant heller ingen eksplisitt logging av den nye efemære private nøkkelen eller recordnøklene.

**Retting:** logg begrensede metadata, feilkode og lokal korrelasjon, aldri hele dekrypterte kommandoer/payloads. Legg syntetisk hemmelig markør i feiltypene og kontroller den aktiverte diagnosticLogHandler. Behold denne som egen retting; «bare debug» lukker ikke lekkasjeveien.

**N20 — Høy, blokkerer ende-til-ende peer-bevis: kontaktaksept validerer signatur, men ikke bindingen til den ventende requesten.**

Kilde: `S:1201–1204`; `E:778–799,812–842,1647–1690,845–916`.

En peer mottar en legitim kontaktrequest Q og dens requestId. Den sender en korrekt selvsignert acceptance med samme requestId, men feil `requestHash`, encounterId, sesjonsfelter, protocolVersion eller messageType. `handleIncomingContactAcceptance` finner Q bare med requestId og verifiserer signaturen over det avsenderen faktisk valgte å signere. Den sammenligner ikke acceptance.requestHash med hashen av Q og kontrollerer ikke de andre bindingsfeltene. Etter dette bygges og lagres request- og acceptance-proof som et encounter, og «Contact Established» kan publiseres. En gyldig signatur over **en annen påstand** er ikke aksept av Q.

Transportens beviste principal følger heller ikke denne callbacken. Payloadens responderIdentity kan derfor være en annen nøkkel enn kanalens. Hvis flere identiteter per enhet er ønsket, trenger det en eksplisitt, verifisert binding/delegasjon; man kan ikke slutte fra kanal-B til at enhver vedlagt identitet er B. Jeg hevder ikke at dette alene gir generelle Resolver-/cellegrants, eller at en ærlig tredjeparts signatur kan forfalskes.

**Retting:** valider type/versjon, eksakt request-hash, request-/encounter-ID, lokal/remote sesjonsbinding og forventet signer eller uttrykkelig identitetsdelegasjon før tilstandsendring og persistens. Bind pending-record til kanal/principal/generasjon og konsumer atomisk, med tids-/replayregler. Behandle en signert request/acceptance som et konkret bevis med scope, ikke bare `verified=true`. Test en korrekt signert acceptance med **hvert bindingsfelt feil**, urelatert signer, annen kanal og to samtidige aksepter, pluss en positiv virkelig encounter-lagring. T bruker GeneralCell/ScannerStatusObserver og dekker ikke denne produksjonskonsumenten.

**N21 — Lav, ikke selvstendig mergeblokk: protokolldokumentene motsier hverandre på head.**

Kilde: `CP/Docs/ScannerMultipeer.md:53–73` mot `D:108–123,127–134`, `G:216–228` og `R:65–78`.

Scanner-dokumentet sier at N07 fortsatt er åpent og at et mellomledd kan endre ordinære meldinger. Det sier også at gamle generasjonsframes forkastes uten å lukke ny gate. N07 har levert AEAD og endret replay på nåværende transport til fatal feil; koden og v2-dokumentet sier dette. Den samme Scanner-teksten lover dessuten at discovery ikke kan endre pending rute, som N11 avkrefter. En integrator som følger den gamle teksten kan implementere feil kompatibilitet eller feil reconnect-forventning.

**Retting:** oppdater ScannerMultipeer.md til vurdert v2-kontrakt og lenk én autoritativ wirebeskrivelse. Skill gammel fanget transportcallback fra gammel chiffertekst levert på aktuell transport. Rett pending-påstanden sammen med N11. Ingen ny protokoll trengs for dokumentrettingen.

**N22 — Lav, ikke selvstendig mergeblokk: et ytre transportmellomledd kan lese og korrelere begge identiteter.**

Kilde: `P:31–58`; `G:94–109,203–235`; `D:27–31,136–142`.

M terminerer de ytre MC-forbindelsene og videresender det indre håndtrykket uendret. De tre første meldingene er ukrypterte i den indre protokollen: M ser begge PublicIdentity-deskriptorer og identitetssignaturer. Gjentatt bruk av samme identitet kan korreleres på tvers av nye kanalgenerasjoner og efemære nøkler. Appdata er fremdeles beskyttet; dette er metadataeksponering, ikke gjenåpning av N07s meldingsforfalskning. En vanlig passiv radioavlytter må i tillegg overvinne MC-krypteringen for å få samme innsyn.

D opplyser korrekt at identitetsbeskyttelse er utenfor v2-målet. Jeg registrerer likevel begrensningen som eget funn etter bestillingen om også å ta med forenklinger. **Retting:** spesifiser og innfør indre håndtrykksbeskyttelse av identiteter/signaturer med et analysert mønster, og test at et rent videresendende M ikke kan lese eller korrelere de stabile identitetsfeltene. Skill uttrykkelig mellom passiv videresending og en aktiv motpart som selv deltar i DH; SIGMA-I og Noise XX har ikke identisk identitetsvern mot alle aktive roller. Dette krever protokolldesign og ny profil-/kompatibilitetsvurdering, ikke bare kryptering av dagens transcript etter signering. Sammenligningen og primærkildene står nedenfor.

**3. Samlet adversariell kryptovurdering**

| Tema | Kildebasert konklusjon og begrensning |
|---|---|
| Transcript-binding | Begge komplette helloer inngår i begge signerte transcripts. Dette dekker profil, endpoint.initiator/responder/setupID/domain, rolle, identity.uuid/algorithm/curve/publicKey, begge efemære nøkler, noncer, generasjoner, utstedelsestider og signerrollen (`P:31–70`). Challenge binder også action/audience/resource og verifier-nonce. De faste KDF-/AEAD-valgene følger v2; det finnes ingen usignert algoritmeforhandling. Levetid er en fast profilregel avledet fra tid, ikke et fritt forhandlet felt. Jeg fant ikke et utelatt forhandlet kryptofelt. MCPeerID/sertifikatet er ikke med: beskyttelsen er ende-til-ende-nøkkelutveksling, ikke MC-sertifikatattestasjon. |
| Unknown-key-share | Endring av en parts identitet/nøkkel endrer både signert transcript og KDF-salt (`P:60–70`; `R:29–36`). Det stenger den klassiske identitetsommerkingen under uendrede nøkler. Ingen konkret kryptografisk UKS funnet. Discovery-navn er fortsatt ikke en betrodd person-/nøkkelbinding, og applikasjonsbindingene i N11/N12/N20 må ikke forveksles med denne kryptografiske egenskapen. |
| Refleksjon / roller | Motsatt rolle kreves; transcripts har signerrolle; key-info og record-header er retningsbestemt (`P:91–99`; `R:31–42,70–75`). Rollebytte/feil profil og record-refleksjon testes (`T:68–83,433–464`). Ingen konkret refleksjonsvei funnet, heller ikke behov for å anta ulike identitetsnøkler på de to enhetene for at retningsvernet skal virke. |
| Nedgradering / ekstra felter | V2 og 32-byte efemær offentlig nøkkel er obligatorisk. Plaintext-listene er faste og engangs; deretter kreves AEAD. Auth-envelopes må roundtrippe kanonisk, og ukjente metadata avvises (`A:151–155`; `G:59–63,203–235,325–333`). `T:496–509` prøver v1 og manglende nøkkel. Ingen v1-/ready-fallback funnet. |
| Noncer / tellere / gjenbruk | Hello får fersk tilfeldig 256-bit nonce og fresh efemær nøkkel; sessions får ny UUID-generasjon. Record-nonce er 0^32 || counter64BE med separat nøkkel per retning. Counter starter på 0, økes etter vellykket crypto, max brukes ikke, og feil ødelegger recordnøklene (`P:82–89`; `L:233`; `R:44–78`). Ingen wrap-/nonce-reuse-vei funnet gjennom adapteren. Record-rekkefølge er ikke applikasjonsrekkefølge, jf. N10. |
| Retning og generasjon | HKDF-salt inkluderer begge hele transcripts; info inneholder peer-profil, key-formål og retning. AAD inkluderer profil/record-formål, magic, sendergenerasjon, retning og teller (`R:29–51`). Ny nøkkel ved reconnect og omskrevet gammel header prøves i `T:557–586`. Ingen kjent key-reuse mellom retninger/generasjoner. |
| Lavordens X25519-punkter | Providerens key agreement er kastende, og all-zero shared secret avvises i tillegg med OR over alle bytes (`R:25–28`). `V:72–79` prøver 0, 1, p−1, p og p+1 på macOS/Linux. Dette er et utvalg av input, ikke en uttømmende punkt-/backend-revisjon. RFC 7748 beskriver all-zero-kontrollen og binding av begge offentlige DH-verdier: [§6.1 og §7](https://www.rfc-editor.org/rfc/rfc7748). |
| Nøkkelbekreftelse | Begge parter må åpne korrekt record 0 og kontrollere sessionID/generation/transcriptDigest før egen aktivering/factory (`G:118–126`; `P:113–117`). Initiator aktiverer etter å ha sendt egen bekreftelse, uten å vite at responder allerede har behandlet den; dette er ikke mangel på lokal mottatt nøkkelbekreftelse. `T:512–531` holder den siste bekreftelsen og hindrer responder-Base. |
| Formålsseparasjon mellom confirmation og data | Samme retningsnøkkel brukes til ack record 0 og senere app-records, med forskjellige noncer og strengt forventet førstetype. Jeg har ikke funnet et angrep bare på grunn av manglende egen finished-nøkkel. Det er likevel en konstruksjonsforskjell fra SIGMAs separate nøkkelformål, ikke noe SIGMA-bevis automatisk dekker. |
| Efemære nøkler / minne / logger | Privat efemær nøkkel er lokal, ikke Codable, opprettes i Operation og slippes etter ett derive-forsøk eller cancel (`P:82–89,119–125`). Recordnøklene er private, ikke eksportert/persistert, og nullstilles ved close (`R:13–14,81`; `G:397–410`). Ingen ny key-logging funnet. Dette er Swift-referanselivsløp, ikke attestert zeroization av alle kopier/OS-minne; D sier det korrekt. Dekrypterte applikasjonslogger har N19. |
| Feilorakel | AEAD utføres før plaintext-dispatch; tagkontrollen er Crypto-providerens, og første crypto-feil er terminal. Headerfeil og tagfeil har ulike lokale feiltyper, men headeren er offentlig. Jeg fant ingen konkret padding-/plaintext-dekrypteringsoracle eller fri signeringsoracle i den nye handshake-koden. Signering er lokal engangsoperasjon bundet til begge helloer (`P:101–111`); angriperen får ikke velge vilkårlige signingData. Generiske error-objekter i UI/logg bør avgrenses som i N19; ingen timingmåling eller full providerrevisjon er utført. |
| Tid / revokasjon | Pending og aktiv session sjekker monoton frist og veggklokke, også rundt aktivering (`L:307–355,374–380`). Peer Operation har egen 10-sekunders frist. `revoke` sperrer nåværende leases; det er **ikke et varig nøkkelregister**. Scanner oppgir ingen egen `recheckPolicy` ved `S:661–672`; verten må ikke beskrive dette som permanent sperring av alle fremtidige innlogginger. Ny brukeraksept, vertspolicy og cellegrants er egne krav. |
| DoS / store rammer | 16 KiB auth, 1 MiB plaintext + 65 bytes record, 64/4 MiB lokal receive-kø, gate-work/send/opptaksgrenser og ratevinduer finnes. Overhead-/counter-/størrelsestestene er relevante (`V:82–105`; `T:399–407,589–602`). N13–N18 viser hvorfor disse ikke er en samlet vertskvote eller generell DoS-attest. |

Tids-/nonce-/transcript-testsuiten bør ved rettingene suppleres med enkeltfeltmutasjoner for begge identiteter, algoritme/kurve, begge noncer/generasjoner/tider og domain, selvkonsistente feiltranscripts, suspendert lokal signer med close/revoke, køgrense+1 og isolasjon under last. Faste vektorer er nyttige, men erstatter ikke disse tilstandsforløpene. Dette er presisering av testbeviset; jeg har ikke funnet en særskilt kryptofeil for hvert uprøvde felt.

**4. Sammenligning med SIGMA-I og Noise XX**

Dette er en **egen signert efemær DH-protokoll**, ikke en implementasjon av SIGMA-I eller Noise XX. Den har nødvendige felles byggesteiner: friske DH-verdier, autentisert sammenbinding av partene, avledede retningsnøkler, bekreftet nøkkelbesittelse og AEAD-records.

SIGMA kombinerer signaturer og en DH-avledet MAC som binder identitet til nøkkelen; SIGMA-I krypterer identiteter/signaturer og skiller autentiserings-, handshake-krypterings- og sesjonsnøkler. Krawczyk beskriver også hvorfor inkludering av mottakeridentitet i signaturen hindrer den konkrete identity-misbindingen i ISO-varianten. CPs full-transcript-signatur, KDF-binding og forseglede acknowledgements må vurderes som **dens egen** løsning; fravær av et separat felt kalt MAC er ikke alene en demonstrert svakhet her. [SIGMA-papiret, §§4–5](https://iacr.org/cryptodb/archive/2003/CRYPTO/1495/1495.pdf).

Noise XX har en spesifisert token-/tilstandsmaskin, handshake-hash/chaining-key, krypterte statiske nøkler og adskilte transportretninger. Noise presiserer også applikasjonens ansvar for blant annet aksepterte statiske nøkler og rammegrenser. CP har tilsvarende formål flere steder, men bruker signeringsidentiteter, JSON-transcript og sin egen femmeldingsprogresjon; Noise XXs analyser/testvektorer kan ikke arves ved likhet i primitivevalg. [Noise, §§5, 7.5, 7.8, 13](https://noiseprotocol.org/noise.html).

**Det konstruksjonen mangler sammenlignet med disse mønstrene:** identitetsbeskyttelse i det indre håndtrykket, samme etablerte mønsters analysegrunnlag og standardisert interoperabilitet/tilstandsmaskin. Begge PublicIdentity-er og identitetssignaturer er synlige for M som terminerer ytre MC, selv om M ikke kan lese appdata (`P:31–58`; `G:94–109`). Dette er uttrykkelig avgrenset i D og registrert som personvernfunnet **N22**; det skal ikke markedsføres som SIGMA-I-/XX-identitetsskjerming. Det er ikke en påvist AEAD-sårbarhet. Identitetsbeskyttelse krever et eget protokollvalg, ikke bare å kryptere dagens identitetsavhengige transcript etterpå.

Bruken av full transcript-kontekst og forskjellige HKDF-info-strenger samsvarer med behovet for kontekstbinding i [RFC 5869 §3.2](https://www.rfc-editor.org/rfc/rfc5869). Teller/nonceregelen og full tag er forenlig med [RFC 8439](https://www.rfc-editor.org/rfc/rfc8439). Dette kontrollerer bruken av primitive byggesteiner; det er ikke et formelt sikkerhetsbevis for den samlede CP-protokollen. N10–N20 ville heller ikke blitt løst automatisk ved å bytte kun kryptobibliotek.

**5. WS og ready**

WS-profilen er fortsatt **`org.haven.bridge-channel.v1` / `openBridgeChannel`**, med kanonisk origin/rute/domene (`A:9–10,64–97,175–186`). Peer er **`org.haven.bridge-peer-channel.v2` / `openPeerBridgeChannel`**, med endpoint-hash som audience og peer-transcript-hash som resource (`P:10,29,60–70`). Ingen falsk WSS-origin eller profilkryssing ble funnet.

`BridgeChannelAuthentication`, `BridgeChannelClientOperation`, `BridgeChannelSession`, Base og mux er byteuendret fra forrige vurderte `101e5452` til denne headen. Felles G og BridgeCommand er endret, så **ikke hele WS-implementasjonen er byteuendret**: peerGeneration er et nytt valgfritt codec-felt, og auth avviser det eksplisitt (`G:325–329`). WS sender det ikke og bruker ikke record-laget. WS-signert transcript og vanlig WS-wire er bevart.

Ingen ready-unntak funnet: gate avviser ved `G:299`, Base ved `B/BridgeBase.swift:1348,1369–1370`, mux ved `B/BridgeMultiplexing.swift:928`. Lokal `activateAuthenticatedChannel` krever session.check før ready settes (`B/BridgeBase.swift:466–471`). NI og negative cid-er avviser vanlig `ready`; N14 er en annen MC-ressursinngang, ikke et ready-unntak.

**6. Verifikasjon på vurdert revisjon**

GitHub Actions API filtrert på hele head-SHA og PR-rollup bekrefter fem fullførte success-kjøringer, alle attempt 1. Ingen CI er startet eller repetert av meg.

| Workflow | Kontrollert resultat |
|---|---|
| [macOS regression, 36404729039](https://github.com/Digipomps/CellProtocol/actions/runs/36404729039) | Nettloggen er hentet og relevante linjer lest. Fulltest **1421 tester, 5 skipped, 0 feil**. Alle 26 ScannerPeerAuthentication- og 4 BridgePeerRecordLayer-tester har passed-linjer. De tre lokale Keychain-feiltestene består også her. |
| [CellProtocol Swift Linux, 36404728906](https://github.com/Digipomps/CellProtocol/actions/runs/36404728906) | Run/head/status verifisert på nett. Implementørens bevis sier **98/0**, inklusive fire record-tester. Hele Linux-råloggen er **ikke lest på nytt** i denne kontrollen. |
| [Vapor identity vault Linux, 36404728860](https://github.com/Digipomps/CellProtocol/actions/runs/36404728860) | Run/head/status verifisert på nett. Handoff sier **25/0**; detaljert rålogg er **ikke lest på nytt**. |
| [Runtime capacity, 36404728851](https://github.com/Digipomps/CellProtocol/actions/runs/36404728851) | Run/head/status verifisert. Benchmarkens detaljer er **ikke lest**; dette er ikke peer-/MC-kølastbevis. |
| [Notify PyCellProtocol, 36404726429](https://github.com/Digipomps/CellProtocol/actions/runs/36404726429) | Success på pull_request_target. Varsling, ikke peer-runtime-test. |

**CI er ikke identisk med hele head-treet.** Nettloggen sjekker ut `c009e132ecb5ca5f491a65979c18e19523fa6cc4`, med foreldre `81601a6f835252aba7e99d43786fb5d67227c245` og vurdert head. Jeg kontrollerte commitobjektene: CI-tre `b0c7ad8c14b938bc4affe696cedda8441a03f5d2`, head-tre `a7b78237c507d41700f94496f8c1837c0968bab1`. Diffen er fem Vault-retention-/workflowfiler fra nyere main; de undersøkte peer-/brofilene, testfilene, Package.swift og Package.resolved er identiske. PR-APIets base-snapshot var fortsatt `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366`. CI-resultatet gjelder integrasjonen med nyere main, ikke et påstått identisk totalt head-tre.

TSAN-steget er tre repetisjoner av **bare `BridgeDescriptionConcurrencyTests`**, ikke Scanner/NI/EntityScanner (`CP/.github/workflows/security-regression-macos.yml:33–46`). Ingen iOS-byggjobb finnes i dette macOS-beviset.

Lokale bevis i `/private/tmp/cp53-n07-evidence/` er lest: `head-results.json`, sammendrag/feillinjer i `head-build.log`, `head-test.log`, `head-multipeer.log`, `final-security.log`, samt CI-tree-/testinventaroversikter. Dette er implementørens kjøringer på oppgitt head, ikke nye Astra-kjøringer.

- Bygg: **exit 0**, `Build complete! (2,42 sek)`.
- Fulltest: **exit 1**. CellBase-bundlen har **1387 tester, 12 skipped, 3 feil**; HavenCommons **26/0** og CellNearby **3/0** gir totalt **1416** oppdagede tester. Fem VaultIdeaRetention-tester forklarer CI-totalen 1421 i den kontrollerte inventaroversikten.
- De tre konkrete feilene er `testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns` og `testLegacyEmbeddedPrivateKeyStillSigns` med CDSA/EPERM 100001, samt `testScopedSecretDataStaysStableInUnsignedTestHost` med −25291 (`head-test.log:248,251,260`). De samme tre navnene er eksplisitt passed i nettloggen. Miljøforklaringen er støttet; lokal fulltest er fortsatt rød, og jeg har ikke kjørt en ny basekontroll.
- Siste målrettede sikkerhetslogg: **30 tester / 0 feil**. Det er funksjons-/regresjonsbevis for det suiteinnholdet, ikke fravær av funnene over.

**Reell toprosess-Multipeer:** parent-loggen viser **1 test / 0 feil**, 8.969 sekunder. Jeg leste de faktiske fire workerloggene og `.passed`-filene, ikke bare JSON-oppsummeringen. Alle har 1 test / 0 feil og markører for authenticated, description, attach og feed:

| Inviter | Worker a, sent/received records | Worker b, sent/received records |
|---|---:|---:|
| a | 46 / 27 | 27 / 46 |
| b | 27 / 46 | 46 / 27 |

Kataloger under `/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/`: `cp53-multipeer-5D215FBD-7E0C-4BB3-9286-348D1E3DAF32` og `cp53-multipeer-670ECDE4-3964-4213-89A7-421FC337414C`. Systemlinjen `nwi_state: registration failed (9)` finnes, men workerprøvene fullførte med nevnte funksjon og null XCTest-feil. M bruker reelle MC-adaptere og to prosesser, syntetiske lokale vaults og testvertens GeneralCell/Lobby. **Den bruker ikke den fulle EntityScannerCell-konsumenten** og dekker ikke N13/N20.

Ikke utført eller bevist av denne pakken: iOS-kompilering/NI/UWB, to fysiske enheter, tre faktiske MC-prosesser med mellomledd, reelt MC-reconnect/nettbytte, naturlig femminuttersutløp med fysisk opprydding, vedvarende peer-last/RSS, fulle Scanner-/EntityScanner-racetester, eksternt kryptografisk/formelt bevis, Binding/CellScaffold-konsumenter eller staging/prod. Ingen av disse er omdøpt til bestått fordi CP-CI er grønn.

**7. Beslutning og rettingsport**

**Ikke merge denne headen.** N10–N18 og N20 er de ti selvstendige blokkene i denne kontrollen. N19, N21 og N22 er tre ytterligere rettinger som skal med; de er ikke utelatt fordi de er mindre alvorlige eller dokumenterte begrensninger. Rett først de konkrete grensene og legg til regresjonene under hvert funn. Verifiser deretter ny eksakt head med macOS/Linux, relevant iOS-bygg og NI-prøver, ekte MC-feil/close/last og den faktiske EntityScanner-konsumenten. Behold WS-domeneadskillelse, ingen ready-unntak, lokale signeringsnøkler og uendret celleautorisasjonsgrense.

Tidligere N05 i Binding og eksterne migrerings-/produksjonsporter er **ikke lest på nytt og ikke opphevet**. Denne kontrollen er ikke produksjonsgodkjenning og lover ikke at uleste kodeområder er feilfrie.

Dette er den eneste filen jeg har skrevet. Eksisterende skitne arbeidstrær er bevart. Ingen kodeendring, commit, push, merge, PR-kommentar, agentjobb, dependency-pin eller deploy er utført.
