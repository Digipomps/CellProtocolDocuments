STATUS: LEVERT — anbefaling: ikke merge, 7 funn (7 blokkerer)

Astra / Codex, kontroll 8, 29.09.2026. Vurdert CellProtocol-head: **`3824cf84b58903f900a49b0987ee660085f3d875`**. Kilde og testkilde er lest fra dette Git-objektet med `git show`, ikke fra arbeidstreet. Dette er en lese- og vurderingsjobb: ingen kodeendring, commit, push, merge, bygg eller testkjøring. **Denne rapporten er eneste fil skrevet av kontrollen.**

**N31 er lukket. N32-resten og N35–N38 er ikke rettet. N12 mangler fortsatt native NI-bevis. Nytt funn er N39: en foreldet invitasjonshandling kan godkjenne en ny invitasjon.** De syv åpne postene teller som blokkerende etter Kjetils beslutning om at alle funn skal håndteres før merge. N12 er en verifikasjonsrest etter kilderetting, ikke en ny påstand om at den rettede native koden allerede er bevist feil.

**N35 er en konkret teknisk blokkering for WS/Vapor med flere logiske mux-kanaler på samme socket.** N12/N32/N36–N39 gjelder Scanner, nærhetsradar, kontakt- eller invitasjonsgodkjenning. De kompromitterer ikke dermed WS-håndtrykket. Hele PR-en er likevel underlagt den valgte mergeporten. Jeg har ikke funnet en ny konkret signatur-/nøkkel-/AEAD-omgåelse i den leste endringsflaten; dette er ingen garanti om fravær av sårbarheter.

**1. Leveransegrunnlag**

Jeg leste kontroll 6, kontroll 7 som nødvendig grunnlag for N35–N38, relevante tilbakeblikk i kontroll 4/5, og `PEER-V3-DESIGN.md`. Implementørrapportene ble lest i bestilt rekkefølge:

| Rapport/bevis | Faktisk status | Betydning |
|---|---|---|
| `CP53-N31.md` | **LEVERT**, head `3824cf84…` | Siste leverte head. iOS 16-krysskompilering, lokal fullsuite og ny CI er nå dokumentert. Dette erstatter kontroll 7s historiske opplysning om lokal/upushet/uverifisert N31. |
| `CP53-N32-N35-N38.md` | **STOPPET**, samme head uendret | Byggevakten stoppet jobben før implementasjon og tester. 55,7 GiB ledig; 45,7 GiB / 4 % etter 10 GiB reserve; kravet var minst 40 GiB **og** 5 %. Ingen retting av de fem postene er levert. |
| `HAVEN-Deploy/_handoff/BRO/cp53-ios-bygg-6-20260929.log:1–3` | **Stoppet før bygg**, samme head | 55,9 GiB ledig; 45,9 GiB / 4 % etter reserve. Ingen simulator-/XCTest-kjøring. |
| `HAVEN-Deploy/_handoff/BRO/cp53-n12-evidence/ios-*` | Seks kataloger finnes | Alle `head.txt` og relevante operatorlogglinjer er kontrollert; resultatene står i §6. |

Ingen av de to bestilte rapportfilene eller den bestilte iOS-loggen mangler. Den siste rettingsrapporten er STOPPET; den er **ikke** en ny leveranse som lukker N32/N35–N38. Den blokkerer heller ikke denne lesejobben. Vurdert SHA kommer fra N31s siste LEVERT-status.

Live [PR #53](https://github.com/Digipomps/CellProtocol/pull/53) viste samme head, `OPEN`, `mergedAt: null` og fem SUCCESS-sjekker under kontrollen. Mellom N31s forelder `02f857e0…` og review-head er bare `CellTreeView.swift` endret, +11/−1. Brokode, tester, manifest og pins er uendret. Kontroll 7 vurderte allerede **samme** review-SHA; endringen siden den kontrollen er nye verifikasjonsresultater, ikke nye brorettinger.

Transport- og identitetssikkerhets-skillene er brukt som lesesjekklister. Testresultater nedenfor er implementørens/CI-systemets eksisterende kjøringer kontrollert mot råbevis. «Ville fanget originalfeilen» er en vurdering av inngang og assertions, med faktisk historisk/mutasjonskjøring angitt særskilt. Jeg har ikke kjørt nye reproduksjoner eller mutasjoner.

Alle CP-fil:linje-henvisninger nedenfor gjelder **3824cf84…**. Aliasene er entydige; stiene er relative til HAVEN-roten. `T/` betyr `CellProtocol/Tests/CellBaseTests/`.

| Alias | Fil |
|---|---|
| B | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeBase.swift` |
| M | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift` |
| G | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelTransport.swift` |
| V | `CellProtocol/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift` |
| VB | `CellProtocol/Sources/CellVapor/CloudBridge/VaporBridgeReceiveBudget.swift` |
| E | `CellProtocol/Sources/CellApple/EntityRadar/EntityScannerCell.swift` |
| S | `CellProtocol/Sources/CellApple/EntityRadar/ScannerService.swift` |
| SC | `CellProtocol/Sources/CellApple/EntityRadar/ScannerConsumerContext.swift` |
| NI | `CellProtocol/Sources/CellApple/EntityRadar/ScannerNearbyInteraction.swift` |
| NP | `CellProtocol/Sources/CellApple/EntityRadar/NearbyProbe.swift` |
| RM | `CellProtocol/Sources/CellApple/EntityRadar/RadarModels.swift` |

**2. Bestilte rettinger: lukking og originalfeilens testbarhet**

| Post / alvorlighet | Vurdering på head | Ville eksisterende test fanget originalfeilen/resten? |
|---|---|---|
| **N31 — middels** | **Lukket for deklarert iOS 16-minimum.** `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellTreeView.swift:132,221–229` legger `.focusable(false)` bak iOS 17-guard og beholder macOS-grenen. `CellProtocol/Package.swift:12` beholder iOS 16. | **Ja, kompilering er riktig regresjon.** Før retting feilet faktisk simulatorbygg på `02f857e0`, `operator.log:26045` i `ios-20260929T135702`, med availability-feilen. På levert head består `swift build --target CellApple --triple arm64-apple-ios16.0` (full kommando i N31-evidensen). Den bygde `CellTreeView.o` har `platform IOS`, `minos 16.0`, `sdk 27.0`. Ingen ny gammel-kode-mutasjon er kjørt. Dette beviser ikke simulatorruntime eller NI-radio. |
| **N32 — lav** | **DELVIS, rest åpen.** E:531–556 slipper tjenesten før terminallevering; S:597–612 fanger den svakt. E:1141–1150 og :1268–1277 avviser ikke gammel manager ved servicebytte. | **Ja for opprinnelig stoppet eventkø; nei for resten.** `T/ScannerRetainedStateTests.swift:93–113` beholder både lokal service og `cell.connectService`, stopper direkte og drenerer manuelt. Den kjører ikke faktisk cellestopp med siste sterke eier sluppet eller sen terminal fra erstattet service. |
| **N35 — middels** | **Åpen; WS/Vapor-blokkering.** V:299–311 lar ordinære meldinger vente på én fysisk `dispatchTail`; M:810–824,938–971 venter på hele celleoperasjonen. | **Nei.** `T/VaporWebSocketAdmissionTests.swift:22–49,223–253` bruker en annen fysisk socket som søsken. `T/BridgeChannelWebSocketTests.swift:48–112` prøver én logisk mux-kanal. Ingen ny tokanalsregresjon er levert. |
| **N36 — høy** | **Åpen.** E:643–665,972–994 og :1458–1481,1499–1528 knytter et gammelt klikk til nåværende pending via fjern-ID/requestId. SC:50–57,70–118 beskytter recordens kanal, men binder ikke den viste handlingen til akkurat den recorden. | **Nei.** `T/EntityScannerConsumerSecurityTests.swift:73–104` prøver vanlig godkjenning/replay og feil signer; :429–455 prøver gamle svar etter reconnect. De holder ikke gammel UI-handling mens en ny pending med samme ID settes inn. |
| **N37 — middels** | **Åpen, begge deler.** E:1136,1160–1163,1180–1233 og RM:392–401,420–480 lar ledger-rader overleve consumer-retirement. NP:75–79,101–111,132–139 beholder probehistorikk uten den nye faste consumer-kvoten. | **Nei for resten.** `T/ScannerRetainedStateTests.swift:10–90` teller peerStates/beacons/overlaps og lease-bytes, ikke ledgeren eller hele probehistorikken. Den fanger de tre opprinnelige dictionary-lekkasjene. |
| **N38 — lav** | **Åpen.** E:1320–1322 og SC:76 fjerner pending uten å rydde eiet `.probing`-state. E:1367–1373 kan ikke gjenopprette gjennom en død context. Automatisk forsøk er dessuten låst av E:1279–1285. | **Nei.** `T/EntityScannerConsumerSecurityTests.swift:429–455` krever frisk **detail**, ikke første friske aggregate etter reconnect. :458–485 prøver aggregate etter TTL på levende context. |

Den historiske N28–N33-mutasjonen ga 7 tester / 480 feil / 1 unexpected (`evidence-cp53-n28-n33/original-mutation.log:662`). Gamle relevante produksjonsmetoder ble satt tilbake i ellers endret kode. Den bekrefter dekning av de opprinnelige testede feilene; den er hverken en uendret gammel checkout eller dekning av N32-resten/N35–N39.

**3. Alle åpne funn og nødvendige regresjoner**

**N12 — Høy. Native NI-verifikasjon er fortsatt ufullstendig. Bare nærhetsradar.**

NI:61–78 kontrollerer tokenmetadata mot principal, target, setup og NI-generasjon før native dekoding. NI:83–163 eier én entry per fysisk context og pensjonerer den ved kanal-/sessionstopp. NI:169–223 arkiverer/dekoder native `NIDiscoveryToken`, kjører `NINearbyPeerConfiguration` og filtrerer eksakt NISession/token i callback. S:1168–1192 og :1433–1445 fører den autentiserte contexten til send, installasjon og siste publisering. Den opprinnelige globale B/C-feiltilordningen er rettet i den leste koden.

`T/ScannerNearbyInteractionTests.swift:41–171` ville fanget den **modellerte** originalfeilen: to peers, feil binding, gammel callback, revoke/stop/reconnect/suspension. De syv macOS-testene består på review-head (`round3-macos-test.log:4122–4150`). Driveren ved :180–194 bruker syntetiske tokenbytes, injisert ved :207–210. Den iOS-spesifikke testen ved :174–175 tester bare avvisning av et ugyldig arkiv; den er ikke dokumentert kjørt.

N31 lukker kompileringsdelen av iOS 16-problemet. **Fortsatt mangler** vellykket relevant simulator-XCTest, gyldig native secure-archive/decode-rundtur og NI mellom to støttede fysiske iPhones. Det må vises at faktiske resultater følger riktig autentisert peer og at revoke, stop, reconnect og suspension avviser sene callbacks. Den opprinnelige B/C-feilen krever også native interleaving med flere sessions/tokens; en enkel avstandsmåling mellom to telefoner alene dekker ikke hele matrisen. Apples beskrivelse skiller tokenutveksling/konfigurering fra native måle- og livsløpscallbacks; et kompilert fake-driverforløp beviser ikke sistnevnte. [Apple: Initiating and maintaining a session](https://developer.apple.com/documentation/nearbyinteraction/initiating-and-maintaining-a-session).

**N32 — Lav. «Stopped» kan gå tapt eller gammel service kan overskrive ny radarstatus.**

E:531–556 setter `connectService = nil`, kaller `stop` og slipper lokal referanse ved retur. S:601 har en svakt fanget MainActor-task; ved siste eierslipp er terminalpublisering ikke sikret. E:552–556 sender «Stopping» på topic `scanner`, mens RM:254–267 forventer `scanner.status`. RM:449–453 nullstiller ikke `scannerStatus`; :529–535 kan derfor beholde aktiv sweep. Hvis gammel service derimot holdes i live av arbeid, kan dens sene status/forbindelsesliste nå E:1141 eller :1268 etter ny service uten manager-vakt. N33s korrekte fysisk-slot-vakt innen samme service løser ikke dette servicebyttet.

Påkrevd regresjon: faktisk `EntityScannerCell.stopConnectService`, slipp siste sterke service-eier før utsatt terminaldrenering, krev stopped én gang og inaktiv radar. Hold også gammel status/connected-callback til etter ny service; ny status/liste må bestå. Dette er fortsatt N32, ikke et nytt separat funn.

**N35 — Middels. Fullføring på A blokkerer B og logisk close på samme WS-socket.**

V:299–311 velger en felles ordinær dispatch-hale; bare `.sign` og lokalt registrert signeringssvar går utenom. M:810–824 venter på delegatens hele operasjon. M:938–971 legger både andre channelID-er og `.closeChannel` bak samme ytre hale.

Forløp: autentiser socketen, åpne logiske A og B, hold en tillatt get/set/resolver på A i ikke-samarbeidende arbeid, send rask get på B og closeChannel for A. Begge står før mux-dispatch til A returnerer. B kan time ut og A kan ikke pensjoneres via den mottatte logiske close-meldingen. Fysisk close kan stenge begge; det er ikke selektiv fremdrift. Dette er ikke en påstand om proof-omgåelse, ubundet taskvekst eller blokkering av alle andre sockets.

Rett skillet mellom ordnet opptak/levering og venting på fullført arbeid, med eierskap per logisk kanal/strøm og fremdrift for close. Påkrevd regresjon: **ekte Vapor-adapter**, minst to logiske kanaler på samme socket, barrierestoppet A, vellykket B og selektiv A-close før A slippes, beholdt kvote for uferdig A og ingen sen A-effekt. Bevar N24s ID-/sendlevetid, N27s feedrekkefølge, N30s callback-opptak og origin-signering. En direkte mux-test eller to fysiske sockets er ikke tilstrekkelig.

**N36 — Høy. Gammelt kontakt-/detaljsamtykke kan brukes på ny pending.**

Kontaktvarselet bærer den viste requesten, men E:645–651 bruker bare `requesterSessionUUID` og `requestId` til å hente **nåværende** context/pending. E:654–665 signerer/sender/persisterer `record.payload`, som kan være en nyere gyldig forespørsel. Etter reconnect med samme fjern-UUID, annen nøkkel og gjenbrukt requestId kan gammelt klikk godkjenne nytt innhold/principal. Samme kanal kan gjenbruke ID etter pending-TTL. Detail-handlingen ved E:1471–1478 inneholder bare remoteUUID/requestId/action og velger også nåværende record ved :1507/:1522.

Proof og resolver-grants kan være korrekte hele veien; feilen er bindingen mellom menneskets viste valg og effekten. Rett med lokal engangsidentifikator for nøyaktig pending-instans, request-hash, principal og kanalgenerasjon. Påkrevd regresjon for **både kontakt og detaljdeling**: hold gammel handling, sett inn ny gyldig request under samme ID etter reconnect/annen nøkkel og separat etter TTL på samme kanal. Gammel handling må gi null sign/send/persist, bevare ny pending og la fersk handling fungere.

**N37 — Middels. Ledger og probehistorikk står utenfor den leverte faste consumer-grensen.**

**a)** Found/status går via E:1136 til `radarLedger.entitiesById` (RM:422–441,470–480). E:1160–1163 fjerner tre peer-tabeller/resultatet, men ingen ledger-rad. Lost oppdaterer eksisterende rad ved RM:428–436. Ledger-pruning skjer ved radar-get (E:169–174), ikke som garantert del av discovery-retirement. En scanner uten radar-polling kan dermed samle rader over UUID-/TTL-vinduer selv om de tre målte tabellene er begrenset. Dette krever discovery, ikke peer-proof. OOM/RSS for dette forløpet er ikke målt.

**b)** NP:75–79,101–111 beholder `handledRequestIDs`, `handledNonces` og `probeCountByRemoteUUID`; retirement fjerner bare resultatet (:132), og full reset (:134–139) rydder historikken. Denne delen krever autentiserte peers og gyldig overlap. Standardpolicy har åtte timer, to per peer og tolv per minutt (`NearbyDisclosurePolicy.swift:6,44–45`), altså en tids-/rateavledet størrelsesorden på 5760 forespørsler per standardperiode. Dette er **ikke uendelig vekst under standardpolicy**. Men policyvalideringen ved :110–128 setter ingen maksimal varighet eller øvre rategrense; den faste globale count-/byte-grensen dekker fortsatt ikke disse samlingene.

Påkrevd regresjon: virkelig EntityScannerCell gjennom mange UUID-/rate-/TTL-vinduer **uten radar-get**; mål ledger, alle probehistorikker og beholdte bytes, krev fast tak og fungerende legitim peer. Bevar replay-/ratevernet gjennom reconnect; blind tømming hver gang en kanal lukkes er ikke en tilstrekkelig retting. Begge delene må håndteres, uten dobbelttelling av N28/N16.

**N38 — Lav. Pending ryddes, men første friske aggregate etter reconnect kan feile.**

Når discovery fortsatt lever, kan peerStates beholde `.probing`. E:1320–1322/SC:76 fjerner generasjonens pending uten expiry-callback; pruning gjennom SC:70–74 hjelper heller ikke når E:1369 krever den nå døde contexten. Første friske aggregate forsøker `.probing → .probing`, som avvises av `NearbyPeerState.swift:25–38`. Catch ved E:1387–1393 kan deretter returnere state til `.beaconMatched`, slik at et senere manuelt forsøk kan lykkes. Automatisk retry kan utebli fordi E:1279–1285 også krever `.beaconMatched` og en ubrukt `automaticProbeRemoteUUIDs`-post.

Rett pending og den eksakte generasjonens eide operasjonstilstand samlet. Påkrevd regresjon: close/reconnect med beholdt discovery, avvis gammelt svar, krev **første** friske aggregate og avtalt automatisk retry, og bevis at gammel cleanup ikke nullstiller ny probe eller annen peer. Dette er ikke påstått permanent blokkering av alle manuelle forsøk.

**N39 — Middels, nytt. En foreldet invitasjonshandling kan akseptere eller avvise en annen invitasjon. Bare peer/radar.**

Kilde: **E:410–419,1236–1258; S:823–839,869–879,911–920,932–943,1261–1277**.

Den lokale invitasjonen eier nå fysisk peer, MCSession, endpoint, generasjon og instans. Men den publiserte accept/reject-handlingen inneholder bare `remoteUUID` og `accept` (E:1252/:1257). Set-interceptet velger dagens `connectService` og kaller `respondToInvitation(remoteUUID:accept:)`. Denne funksjonen finner dagens pending under UUID-en; den får ingen instans-ID fra den viste handlingen å sammenligne med.

Et konkret kildebasert forløp er:

1. B annonserer UUID R og sender invitasjon I1. Brukeren får en handling for I1.
2. I1 utløper. S:869–879 fjerner og avviser den. B forsvinner; C kan nå annonseres under R og sende en ny invitasjon I2 med eget endpoint/setup. S:1263–1266 beskytter en **levende** binding, men I1 finnes ikke lenger.
3. Brukeren utfører den gamle I1-handlingen. E:419/S:826 finner I2 og sender `handler(true, I2.session)` ved S:835. Et gammelt reject kan tilsvarende avvise I2. Det samme instanshullet finnes ved ny invitasjon fra samme fysiske peer etter timeout og ved utskifting av hele serviceobjektet.

Dette krever et gammelt brukerklikk; en remote kan ikke alene gi seg selv celleautorisasjon. Angrepet bytter ikke kryptografisk principal B til C. Det bryter den eksplisitte invitasjonsgodkjenningen: gammel tillatelse åpner ny fysisk forbindelse. Med Scanner-policyen `.anyProvenIdentity(allowUnauthenticatedInitiator: true)` ved S:943 kan C deretter motta responderens identitet som aktiv håndtrykkspart, slik v3-designets §7 beskriver. Det forsterker betydningen av at godkjenningen gjelder riktig invitasjon.

N11s opprinnelige retting er fortsatt virksom **mens den gamle invitasjonen lever**. `T/ScannerServiceInvitationTests.swift:114–151,195–215` kontrollerer denne bindingen; :218–267 kontrollerer gammel disconnect og timeout fulgt av nytt forsøk. Ingen av disse sender den gamle publiserte handlingen gjennom EntityScannerCell etter utskifting. Jeg har ikke kjørt en ny native/UI-reproduksjon; dette funnet følger av den leste selector→lookup→handler-kjeden.

Rett med en lokal engangs godkjennings-ID bundet til eksakt servicegenerasjon og Invitation-instans/peer/session/endpoint. Valider den før handleren tas, og la foreldet handling være uten effekt på den nye invitasjonen. Påkrevd regresjon: fang faktisk publisert I1-action fra EntityScannerCell, utløp I1 med injisert klokke, legg inn I2 under samme UUID fra C, kjør gammel accept og reject. I2s handler må ikke kalles og I2 må fortsatt kunne godkjennes med fersk action. Gjenta samme-peer/nytt setup og servicebytte. Bevar N11s atomicitet og N16s begrensede opptak; opprett ikke et ubundet action-register.

N39 er en egen grense før kanalproof. N36 gjelder kontakt-/detaljgodkjenning etter autentisering. De har beslektet årsak, men krever separate effekter og regresjoner.

**4. Samspill med tidligere rettinger, særlig WS/Vapor**

- **Opptak og fysisk close:** V:256–325 bruker eksplisitt synkrone callbacks, reserverer antall/bytes før kopiering/Task og beholder dem gjennom dispatch og audit. VB:9–18 gir per-socket 64 / 4 MiB og prosessdelt 1024 / 32 MiB. V:219–254,340–379 samler close og resolver-unregister. `T/VaporWebSocketAdmissionTests.swift:142–202` holder fysisk close eller audit/unregister og krever beholdt kvote. Dette støtter N30s opprinnelige lukking, men reparerer ikke N35.
- **Signeringsprioritet gir ikke myndighet:** V:300 og G:489–494 bruker den lokalt registrerte signerings-RPC-en; M:975–978 bruker også riktig channelID; B:1908–1911 kontrollerer auditoren. Vanlig gate-/principalvalidering består ved G:470–508 og B:1344–1366. B:1329–1340,1581–1585 revaliderer signeringspermit/livsløp. N35 må rettes uten å fjerne denne fremdriftsbanen eller gjøre payloadformen til autorisasjon.
- **Faktisk WS-positivkontroll:** `T/BridgeChannelWebSocketTests.swift:44–112` prøver HTTP-upgrade, avvist pre-proof-get, etterfølgende protected read og null kall til serverens trap-signer, både uten mux og med én logisk mux-kanal. Dette er relevant funksjonsbevis, men ikke en tokanals- eller produksjonsvertstest.
- **Feed, kvoter og sene sends:** B:1775–1902 reserverer køverdier, drenerer i rekkefølge og håndterer completion/failure. `T/BridgeFeedAndRPCOrderingTests.swift:46–75` holder første fysiske send, legger til verdi 2 og completion og krever `[1,2]`, også for synkron endelig publisher. M:993–1003,1119–1178 beholder ID-/sendreservasjoner. Bevar dette når dispatch splittes. Testen ved :356–383 bruker direkte mux og beviser ikke fremdrift gjennom Vs ytre hale.
- **RPC og fabrikklevetid:** B:849–911 registrerer cid-eide Future-svar før send; :1914–1943 revaliderer etter lookup under livsløpslåsen. G:129–162 og M:1070–1104 eier returnerte factory-resultater gjennom rechecks/opprydding. Ingen ny konkret regresjon er identifisert i disse leste områdene. Historiske N23–N26-tester er ikke alle lest/kjørt på nytt.
- **Peer-designets grenser:** WS v1 og peer v3 er ulike profiler, ikke fallback for hverandre. Uendrede kryptokjernefiler støttes av kontroll 6 og diffkontroll, ikke en ny full kryptorevisjon her. Kanalproof beviser nøkkelkontroll, ikke personidentitet, sannhet i discovery eller fysisk nærhet. Aktivt akseptert motpart kan motta identitet etter vertens disclosurepolicy. MC-ytterkryptering erstatter ikke indre v3, og appkvoter beviser ikke et absolutt før-callback-/kernelminnetak.

For å bevare alle tidligere funn uten å telle samme rest to ganger:

| Tidligere poster / opprinnelig alvorlighet | Videreført vurdering |
|---|---|
| N07, N08, N14, N20, N23 — **høy** | Lukket for de konkrete feilforløpene i kontroll 6. Ingen ny full kilde-/testaudit av alle fem her. N39 utvider invitasjonsgrensen uten å gjenåpne N08s etablerte fysiske routingfeil. |
| N09, N10, N11, N15, N17, N18, N24, N25 — **middels** | Tidligere konkrete lukkinger videreføres. N18s OS-/MC-reassemblygrense består. N11s gamle binding lever fortsatt; ny handling etter utløp er N39. |
| N19, N21, N22, N26 — **lav** | Tidligere avgrensede lukkinger videreføres. Ingen total logg-/dokument-/kryptoaudit påstås. Dokumentasjonens brede consumerpåstander må samsvare med N32/N36–N39 ved retting. |
| N13 — **høy**, N16 — **middels** | Hovedrettinger videreføres; gjenstående konkrete consumerforløp står i N36–N38/N39. Ingen ekstra telling av disse samlepostene. |
| N27, N34 — **middels** | Lukket for ordnet feed/completion og cid-eide set/description-svar som i kontroll 7; relevante kilder og testutdrag kontrollert på samme SHA. |
| N28, N29 — **middels** | De opprinnelig testede tabell-/svarbindingsfeilene er rettet. Restene føres som N36–N38, ikke som to ekstra funn. |
| N30 — **middels**, N33 — **lav** | Opprinnelig callback-opptak/ordering og samlet fysisk forbindelsesliste er rettet. N35 og N32 er gjenværende separate grenser. |
| N31 — **middels** | Nå lukket med faktisk minimumskompilering og verifikasjon, jf. §2 og §5. |
| N01–N06 | **Ikke lest/revurdert i denne kontrollen.** Tidligere N05 om downstream-inngress/Binding er ikke opphevet og inngår ikke i tellingen av denne CP-leveransens åpne funn. |

**5. CI og lokale resultater**

Bevisrot for N31: `HAVEN-Deploy/_handoff/BRO/cp53-n31-evidence/`. Resultater er lest, ikke gjentatt av meg. Lange logger er kontrollert i relevante utdrag, ikke linje for linje.

| Kontroll | Kontrollert resultat | Nøyaktig avgrensning |
|---|---|---|
| N31 iOS 16 device-target | `round3-ios16.json`, `.log:1270–1272`: **exit 0, Build complete, 140,23 s**. `round3-ios16-object-target.log`: IOS/minos 16.0/sdk 27.0. | Eksakt review-head, arm64 iPhoneOS-krysskompilering av CellApple; ingen runtime eller radio. |
| N31 full lokal macOS-build | `round3-macos-build.log:49–51`: **exit 0, 13,45 s** | Eksakt review-head, ufiltrert `swift build`. |
| N31 full lokal macOS-test | `round3-macos-test.log:5124,5140`: **1507 CellBase-tester, 12 skips, 3 feil**, exit 1; HavenCommons 26/0 og CellNearby 3/0 separat, 1536 totalt. | Lokal fullsuite er **ikke grønn**. `round3-test-comparison.json` og `round3-skips-comparison.json` viser samme feilmetoder og samme 12 skips som forelder. |
| De tre lokale feilene | `testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns`, `testLegacyEmbeddedPrivateKeyStillSigns` (CDSA/EPERM 100001), `testScopedSecretDataStaysStableInUnsignedTestHost` (−25291). | Samme metoder består i CI, `round3-ci-regression-raw.log:26276,26278,26284`. Dette støtter miljøforklaringen; jeg har ikke selv årsaksisolert Keychain-verten. Ikke ført som tre nye kodefeil. |
| [macOS regression 36579591897](https://github.com/Digipomps/CellProtocol/actions/runs/36579591897) | **1541 tester, 5 skips, 0 feil**; TSAN **3 × 169 / 0 feil**. Rålogg :30638,57919,58849,59779. | Syntetisk merge-checkout, se nedenfor. TSAN er valgt matrise, ikke hele app/native NI. |
| [Linux 36579591920](https://github.com/Digipomps/CellProtocol/actions/runs/36579591920) | **162 tester / 0 feil**, 10,542 s; rå `0_Persisted Cell file bounds.txt:2023`. | Konfigurert Linux-subsett; ingen Apple MC/NI. Logg hentet read-only fra GitHub og lest i minnet. |
| [Vapor vault 36579591872](https://github.com/Digipomps/CellProtocol/actions/runs/36579591872) | **25 tester / 0 feil**, 0,628 s; rå `0_Vapor identity vault strict storage.txt:1296`. | Vault-port, ikke selvstendig bevis for N35. Logg kontrollert fra GitHub. |
| [Runtime capacity 36579591800](https://github.com/Digipomps/CellProtocol/actions/runs/36579591800) / [upstream sync 36579586761](https://github.com/Digipomps/CellProtocol/actions/runs/36579586761) | Begge **SUCCESS** | Status kontrollert; benchmarkinnhold **ikke lest**. Sync er ingen sikkerhetstest. |

CI sjekket ut **`7171dbd7ee747de5a1902250b93cffe3711c5efe`**, med foreldre main `81601a6f835252aba7e99d43786fb5d67227c245` og review-head `3824cf84…`; foreldrene ble kontrollert live via GitHub. Dette er en syntetisk CI-merge, ingen utført PR-merge. `round3-ci-checkout-comparison.json` viser fem forskjeller fra PR-head: Linux-workflow, Vault-Idea-Retention-doc, VaultCell, VaultIdeaRetention og dens tester. Bro-/Scanner-/N31-koden inngår ikke i forskjellen. Lokale N31-bygg/test gjelder eksakt head; CI gjelder dette merge-treet.

Ingen ny lokal fullsuite, TSAN, native MC, iOS eller CI ble startet av den stoppede N32/N35–N38-jobben. Grønn N31-CI er ikke evidens for rettinger som ikke finnes.

**6. Native Multipeer og iOS/simulator**

Siste leverte eksplisitte flerprosesskjøring er fra `CP53-N28-N33.md` på **02f857e0…**, ikke en ny kjøring på N31. Brokoden/testene er identiske med review-head. `evidence-cp53-n28-n33/native-connections.log:194–206` knytter kjøringen til fire artefaktkataloger og viser **1 parenttest / 0 feil**, 44,012 s, exit 0. Kommandoen var `CP53_MULTIPEER_TEST=1 swift test … --filter ScannerMultipeerProcessTests/testTwoProcessesUseRealMultipeerInBothInvitationDirections`.

`T/ScannerMultipeerProcessTests.swift:11–46` starter begge inviterretninger og deretter treprosess-isolasjon og relay. Det er faktiske MCSession-/discovery-/invitasjonsforløp i ulike OS-prosesser på **én Mac**, ikke to fysiske iPhones eller to fysiske Mac-er. Testverten bruker `GeneralCell` som scanner-consumer (:63–84), ikke et fullstendig EntityScannerCell/UI-forløp.

Følgende markører/råbevis er kontrollert under `evidence-cp53-n28-n33/native-artifacts/`:

| Katalog | Resultat |
|---|---|
| `cp53-multipeer-3B44B991-F852-46D0-B3E8-07EFBCEA6A30` | Begge passed; autentisering, description, attach/feed, sealed send/receive 71/71. |
| `cp53-multipeer-3DF257B0-0452-442A-ACA7-951448FA3F2E` | Motsatt inviterretning; begge passed, henholdsvis 65/65 og 71/71. |
| `cp53-isolation-F4813929-0C9A-496F-8BE7-E188A94FD47C` | A/B/C passed. `blocked.full`: **32 records / 1 583 870 bytes**, RSS **51 036 160 → 53 248 000**; `blocked.checked`: én fysisk søskenforbindelse og **178** søskenverdier. Resource-completion rapporterte feil og remote fysisk disconnect; ni streams ble åpnet i streamfasen. No-proof-expiry observert etter ca. **10,187 s**, ikke naturlig femminuttersutløp av autentisert kanal. |
| `cp53-relay-43E0DB7E-3CCD-494D-A0AC-A642DFC87E2F` | M/I/R passed; to uavhengige ytre MC-forbindelser, fem indre envelopes, kryptert apptrafikk og åtte ordnede private verdier hos endepunktene. Relayen er testadapter rundt produksjonsgaten, ikke tre komplette Scanner-consumere. |

SHA-256 ble kontrollert for **alle 183 kopierte filer** i `native-artifacts-manifest.json`; ingen avvik. Hashkontroll er integritetskontroll, ikke attestasjon av alle semantiske påstander i loggene. Hele relay-/isolation-testkilden er **ikke lest på nytt** i denne kontrollen. Historisk lokal TSAN før siste native assertions: `final-tsan.log:1421`, 169/0; dagens CI-matrise står i §5.

iOS-bevisrot: `HAVEN-Deploy/_handoff/BRO/cp53-n12-evidence/`. Simulatorinventar/schemelister er ikke bevis for kjørte tester.

| Katalog | Head | Faktisk resultat |
|---|---|---|
| `ios-20260929T093621` | 1e3e7f10… | `operator.log:408,413`: Xcodes byggesystem krasjet; BUILD FAILED. Kommandoen ved :8 var CellApple **build** for generic iOS Simulator, ikke test. |
| `ios-20260929T133057` | 02f857e0… | Kapasitetsvakt stoppet før kompilering. |
| `ios-20260929T135351` | 02f857e0… | `operator.log:408,413`: samme byggesystemkrasj / BUILD FAILED. |
| `ios-20260929T135702` | 02f857e0… | `operator.log:26045,26538`: konkret iOS 17-availability-feil ved focusable og BUILD FAILED; N31s originalbevis. |
| `ios-20260929T153115` | 3824cf84… | Diskvakt: 55,2 → 45,2 GiB / 4 % etter reserve. Ingen bygg/test. |
| `ios-20260929T195643` | 3824cf84… | Diskvakt: 55,9 → 45,9 GiB / 4 %. Samme innhold som bestilt `cp53-ios-bygg-6-20260929.log`. Ingen bygg/test. |

Det beståtte **separate** N31-device-target-bygget finnes i §5. Det endrer ikke simulatorforsøkenes utfall. Ingen av disse iOS-artefaktene dokumenterer en bestått simulator-XCTest eller NI mellom to iPhones.

**Ikke kjørt/bevist i denne kontrollen:** alle nye reproduksjoner for N32-rest/N35–N39; gyldig native NI-tokenrundtur og radiomatrisen i N12; fysisk flerenhet-/nettbytteprøve; ekstern treg WS-motpart; langvarig fuzz-/lastkampanje; absolutt MC-reassembly-/kernelminnetak; formell/ekstern kryptorevisjon; Binding-/CellScaffold-appbygg, deploy eller faktisk produksjonsflyt.

**7. Merge og produksjon**

| Åpen post | Alvorlighet | Teknisk flate | Blokkerer merge etter valgt port |
|---|---|---|---|
| N12 | Høy | Native NI / nærhetsradar, bevisrest | Ja |
| N32 | Lav | Radarstatus / servicelevetid | Ja |
| N35 | Middels | **Vapor/WS med logiske mux-søsken** | Ja |
| N36 | Høy | Kontaktbevis og detaljsamtykke | Ja |
| N37 | Middels | Radarens retained state og probehistorikk | Ja |
| N38 | Lav | Aggregate-probe etter retirement | Ja |
| N39 | Middels | Godkjenning av fysisk peer-invitasjon | Ja |

**Anbefaling: ikke merge.** Seks konkrete kode-/regresjonsposter står åpne (N32, N35–N39), i tillegg til N12s native bevisrest. N31 skal ikke fortsatt telles som åpen. Alle syv må håndteres før merge etter Kjetils beslutning.

For WS i prod må N35 rettes og testes gjennom faktisk Vapor-mux. De øvrige seks åpne postene er ikke i seg selv påvist WS-proof-omgåelse. Produksjonsvertens aktuelle muxvalg, hard-close-innkobling, TLS-/endpointkonfigurasjon og tidligere N05/downstream-inngress er **ikke lest/verifisert** her. Derfor gis ingen produksjonsgodkjenning basert på en antakelse om «mux av» eller på grønn pakketest alene. Native NI-bevis krever fysisk utstyr, men det er ingen grunn til å utsette N35 og de øvrige kildefeilene mens dette ordnes.

**8. Lesedekning og læring**

Lest på head: hele V/VB, SC og NI; de angitte områdene av B/M/G, S/E, RM/NP/policy/state-machine og N31-filen; siterte testmetoder og relevante fixture-oppsett. Store B/M/G/S/E er **ikke lest i sin helhet**. Uendrede kryptokjernefiler, alle resolver-/lagringspolicier, hele advertisement-protokollen og UI-rendererne er **ikke lest på nytt**. Henvisning til kontroll 6/7 betyr uttrykkelig arvet vurdering, ikke ny gjennomlesing. Ingen påstand om at uleste områder er feilfrie.

Gjenbrukbar læring fra denne kontrollen: sikker binding av et levende transport-/pending-objekt sikrer ikke at et senere menneskelig klikk velger samme objekt. Følg den faktisk publiserte action-payloaden helt til effekten, og prøv utskifting etter TTL samt servicebytte. En regresjon som bevarer referansen eller direkte kaller en service-metode kan gå forbi akkurat denne feilen. N39 dokumenterer kilde, feilforløp og nødvendig test for neste tråd.

Læringen er bevart i denne rapporten. Den uttrykkelige begrensningen **«én rapportfil»** går foran den generelle læringsfangstrutinen: ingen skill-, ledger-, hendelseslogg- eller `haven_learn`-registrering er skrevet. Eksisterende arbeidstrær og øvrige leveransefiler er bevart.
