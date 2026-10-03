STATUS: LEVERT — anbefaling: ikke merge, 7 funn (7 blokkerer)

Astra / Codex, kontroll 7, 29.09.2026. Vurdert CellProtocol-head: **`3824cf84b58903f900a49b0987ee660085f3d875`**. Dette er siste DELVIS-leveranse, fra N31-rapporten. Den er lokal og ikke pushet. Live PR #53 står fortsatt på **`02f857e0dcd8f3aa59d19c6abf3bbe1e0ca61b2f`**, OPEN, uten merge, med fem vellykkede sjekker; sist kontrollert 13:46 UTC.

**Ikke merge denne leveransen.** Åpne poster er N12, N31, N32 og nye N35–N38. Alle syv blokkerer etter Kjetils beslutning om at alle funn skal håndteres før merge. Det betyr ikke at alle syv rammer WS-serveren: **N35 rammer Vapor/WS med flere logiske mux-kanaler på samme socket.** N12/N32/N36/N37/N38 gjelder Scanner, nærhetsradar eller kontaktgodkjenning. N31 gjelder pakkens deklarerte iOS-minimum og manglende verifikasjon av siste commit.

N27 og N34 er lukket for de påviste feed-/RPC-feilene. N30s opprinnelige manglende callback-opptak er rettet, men den nye ordningen har N35. N29s gamle svar-/pending-binding er rettet, men brukerhandling og tilstandsretur har N36/N38. N28s tre navngitte dictionaries er nå begrenset; andre beholdte consumer-data har N37. N33 er lukket for samlet fysisk forbindelsesliste og gammel callback innen samme ScannerService. N32 er bare delvis lukket.

Ingen kode, commit, push, merge, bygg eller testkjøring er utført av denne kontrollen. **Denne rapporten er eneste fil jeg har skrevet.** Nye feilforløp nedenfor er kildebaserte funn, ikke påstått kjørte reproduksjoner. Jeg har kontrollert eksisterende testkilde, rålogger og CI-resultater, og skiller dette fra selvstendig kjøring.

**1. Leveransegrunnlag og presisjon**

Jeg leste `ASTRA-ETTER-CP53-6.md`, relevante tilbakeblikk i -4/-5 og `PEER-V3-DESIGN.md`, deretter implementørrapportene i bestilt rekkefølge:

| Rapport | Status | Oppgitt leveranse-head |
|---|---|---|
| `CP53-N27-N34.md` | LEVERT | `dab8106a5e1f2004bfa06587b5fa68c2bb30ac35` |
| `CP53-N30.md` | LEVERT | `e1e5e1134d4cea66b8f4d01c4684d025809fabe3` |
| `CP53-N28-N33.md` | DELVIS | `02f857e0dcd8f3aa59d19c6abf3bbe1e0ca61b2f` |
| `CP53-N31.md` | DELVIS | **`3824cf84b58903f900a49b0987ee660085f3d875`** |

Ingen av de fire bestilte rapportene mangler eller har STATUS: STOPPET. «CI pågår» i N28–N33-rapporten er senere avklart av `HAVEN-Deploy/_handoff/VERKTOY/ci-status-20260929.md` og live GitHub: alle fem sjekker på 02f857e0 er SUCCESS. N31 og siste iOS-forsøk er derimot faktisk stoppet av diskvakten før kompilering. Dette skal ikke omskrives til bestått bygg eller test.

Kilden er lest med `git show <SHA>:<fil>`, ikke fra skittent arbeidstre. Diff fra kontroll 6 (`1e3e7f10…`) til review-head omfatter 27 filer. Mellom CI-head 02f857e0 og review-head er **bare CellTreeView.swift endret, +11/−1 linjer**. Brokoden og brotestene er dermed identiske mellom disse to headene; den siste SwiftUI-endringen har likevel ingen ny CI eller vellykket lokal kompilering.

Transport-, identitetssikkerhets-, kontrakttest- og claim-drift-skillene ble brukt som vurderingssjekklister. «Ville fanget originalfeilen» nedenfor betyr at testens inngang og assertions treffer feilforløpet. Der implementøren også har kjørt gammel kode/mutasjon, oppgis det særskilt. Jeg har ikke selv gjentatt disse mutasjonene.

Alle CP-fil:linje-henvisninger nedenfor gjelder **3824cf84…**, også når beviskjøringen gjaldt en tidligere SHA. Disse entydige aliasene brukes for lesbarhet. `T/` betyr `CellProtocol/Tests/CellBaseTests/`; øvrige stier er relative til HAVEN-roten.

| Alias | Fil |
|---|---|
| B | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeBase.swift` |
| M | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift` |
| G | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelTransport.swift` |
| V | `CellProtocol/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift` |
| VB | `CellProtocol/Sources/CellVapor/CloudBridge/VaporBridgeReceiveBudget.swift` |
| S | `CellProtocol/Sources/CellApple/EntityRadar/ScannerService.swift` |
| SA | `CellProtocol/Sources/CellApple/EntityRadar/ScannerAdmission.swift` |
| SC | `CellProtocol/Sources/CellApple/EntityRadar/ScannerConsumerContext.swift` |
| E | `CellProtocol/Sources/CellApple/EntityRadar/EntityScannerCell.swift` |
| NP | `CellProtocol/Sources/CellApple/EntityRadar/NearbyProbe.swift` |
| RM | `CellProtocol/Sources/CellApple/EntityRadar/RadarModels.swift` |
| NI | `CellProtocol/Sources/CellApple/EntityRadar/ScannerNearbyInteraction.swift` |

**2. N27–N34: er rettingene lukket?**

| ID / alvorlighet | Vurdering og kilde på review-head | Ville testen fanget originalfeilen? |
|---|---|---|
| **N27 — middels** | **Lukket for produsentrekkefølge og normal completion.** B:1775–1816 reserverer operasjon/bytes og legger verdier i én kø fra sink-callbacken. B:1819–1902 har én drenerer, normal completion venter på køen, og upstream-/sendfeil pensjonerer eksplisitt. En allerede innlevert send beholder reservasjonen til retur. | **Ja.** `T/BridgeFeedAndRPCOrderingTests.swift:46–75,149–158,187–239,287–335` holder første send før fysisk innlevering, produserer neste og completion, og krever eksakt rekkefølge; tester også synkron endelig publisher, failure og byte-/antallsoverløp. `T/BridgePeerV3Tests.swift:1240–1270` bruker den reelle krypterte peer-banen. Implementørens tre utvalgte originalregresjoner mot gammel BridgeBase ga 7 feil; dette er ikke en komplett gammel-head-kjøring av alle peer-/mux-varianter. |
| **N28 — middels** | **De tre opprinnelig navngitte tabellene er rettet; samlet consumer-påstand er fortsatt DELVIS, med resten ført som N37.** E:1153–1176 knytter peerStates/peerBeacons/peerOverlaps til levende source-lease og separat consumer-opptak. E:1180–1233 pensjonerer ved erstatning/loss. SA og S:586–627 bevarer felles opptak gjennom forsinket consumer-opprydding. RadarEntityLedger og probe-historikk faller utenfor: se N37; ingen dobbelttelling. | **Ja for de tre tabellene.** `T/ScannerRetainedStateTests.swift:10–55` bruker virkelig EntityScannerCell, UUID-rotasjon og 20 vinduer med drenering. :58–90 prøver delt budsjett mellom to scannere mens gammel consumer-opprydding holdes. Assertions teller de tre tabellene og lease-bytes, **ikke** radarLedger eller hele probeSession. De kan derfor passere med N37. |
| **N29 — middels** | **Lukket for gamle/ugyldige utgående aggregate-/detail-svar og pending-lekkasjen.** SC:50–118 har felles antalls-/byte-/TTL-grense og eksakt fysisk context/principal/generasjon. E:1346–1455 validerer nonce, størrelse og overgang før konsum; E:1484–1520 binder utgående detail. Gamle UI-godkjenninger og `.probing` etter retirement er separate rester N36/N38. | **Ja.** `T/EntityScannerConsumerSecurityTests.swift:397–426` prøver feil nonce, annen peer, for stor payload, deretter gyldig svar og replay. :429–455 prøver samme UUID med annen signeringsnøkkel/generasjon og frisk detail etterpå. :458–485 prøver kombinert pending-grense, TTL og ny aggregate etter timeout. Testen prøver **ikke** første friske aggregate etter kanal-close, eller en gammel godkjenningshandling mot en ny pending. |
| **N30 — middels** | **Lukket for opprinnelig opptak etter Task-opprettelse og receive-reordering.** V:256–269 velger synkron WebSocket-callback. V:275–325 reserverer før Data-kopi og Task, ordner preparation og holder reservasjon gjennom consumer/audit. VB:9–35 setter felles og per-socket grenser. V:219–254,340–379 samler fysisk close/unregister. **N35** gjelder den nye dispatch-serialiseringens mux-konsekvens. | **Ja.** `T/VaporWebSocketAdmissionTests.swift:22–253` injiserer frames ved ekte WebSocketKit/NIO-handler: før-proof-burst, count/bytes+1, holdt consumer, blandet tekst/binær, rekkefølge, kontrollpassering, holdt close/audit og felles budsjett over flere sockets. Original callback-mutasjon ga 5 feil i 2 tester; gammel cleanup ga 3 feil i 2 tester. Testens «sibling» er en **annen fysisk socket**, så N35 slipper gjennom. |
| **N31 — middels** | **DELVIS: plausibel og avgrenset kilderetting, ikke verifisert lukket.** `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellTreeView.swift:132,221–229` bruker nå availability-modifikator. `CellProtocol/Package.swift:12` beholder iOS 16. Ingen vellykket minimumskompilering av rettingen. | **Den opprinnelige iOS-minimumskompileringen fanget feilen, men er ikke bestått etter retting.** Seneste forsøk på review-head ble stoppet før kompilatoren. Ingen XCTest kan erstatte dette bygget. Se avsnitt 4 og 6. |
| **N32 — lav** | **DELVIS.** S:597–627,765–813 har nå en separat, engangs terminalpublisering og ordnet restart på samme tjeneste. E:531–556 slipper imidlertid tjenesten før den svakt fangede publikasjonen nødvendigvis kjører. Cell-delegatene mangler dessuten avvisning av status fra erstattet service. Resten beskrives under avsnitt 4. | **Ja for den opprinnelige stoppede eventkøen, nei for faktisk eierslipp/servicebytte.** `T/ScannerRetainedStateTests.swift:93–113` fyller vanlig eventkvote, prøver stop to ganger og restart, men beholder både lokal `service` og `cell.connectService` og drenerer eksplisitt. Dermed tvinger testen frem en levetid den vanlige stoppbanen ikke lover. |
| **N33 — lav** | **Lukket for originalfeilen.** S:1347–1377 validerer aktuell fysisk slot før state-endring. S:605–625 bygger samlet sortert snapshot av tilkoblede, ikke-pensjonerte fysiske slots. B-close fjerner ikke C fra listen. Resten ved utskifting av hele ScannerService føres under N32. | **Ja.** `T/ScannerRetainedStateTests.swift:116–150` krever B+C, deretter C, deretter ny B+C; holdt gammel callback må ikke publisere. `T/ScannerPhysicalIsolationTests.swift:148,161–167,193` legger til assertions for faktiske MCSession-forbindelser og publisert liste i native flerprosessprøven. |
| **N34 — middels** | **Lukket for tidlige svar, samme-keypath-kollisjon og gammel cleanup.** B:27–37,849–870,888–912 registrerer cid-eid Future før send og rydder bare egen waiter. B:1914–1943 revaliderer under livsløpslås; B:2001–2008 fullfører riktig set; B:2119–2155 feiler pending ved retirement. | **Ja.** `T/BridgeFeedAndRPCOrderingTests.swift:83–145,160–185,241–280,337–351` prøver umiddelbart svar inne i send, to sets på samme path i motsatt svarrekkefølge, én timeout mens annen lever, samtidige descriptions, feil payloadtype og sen gammel generasjon. Peer-variant ved `T/BridgePeerV3Tests.swift:1273–1293`. Description-assertionen prøver feil payloadtype, ikke en vilkårlig malformet JSON-body inne i et allerede dekodet AnyCell. |

Mutasjonsloggen for N28–N33 (`evidence-cp53-n28-n33/original-mutation.log`) viser **7 tester, 480 feil, én unexpected** med gamle relevante produksjonsmetoder satt tilbake. Dette styrker originalfeil-dekningen, men er en utvalgt mutasjon i en nyere testvert, ikke bevis fra en uendret full checkout av gammel head. N27-/N30-loggene har tilsvarende avgrensning. Jeg har lest relevante feil-/oppsummeringslinjer og restaureringsbevis, ikke kjørt driverne selv.

**3. Nye funn — N35–N38**

**N35 — Middels. Én holdt celleoperasjon blokkerer andre logiske mux-kanaler og deres close på samme Vapor-socket. Teknisk WS-produksjonsblokkering.**

Kilde: **V:299–311**, **M:810–824,938–971**, **B:1344–1366,1439–1465,1474–1497**.

N30s nye `dispatchTail` er felles for hele den fysiske transporten. Alle ordinære kommandoer venter på at forrige `dispatchCommand` returnerer. Muxens `record.dispatch` venter igjen på at hele cellens get/set/resolver-arbeid returnerer. Bare `.sign` og et lokalt registrert origin-signatursvar går utenom denne halen. `.closeChannel`, ny åpning og ordinært arbeid på en annen channelID går ikke utenom.

Konkret forløp: autentiser én WS-forbindelse og åpne logiske A og B. Hold en tillatt get/set på A inne i en ikke-samarbeidende celleintercept/resolver. Send så en rask get på B og en closeChannel for A. Begge blir stående **før mux-dispatch**, bak As fullføring. B kan få timeout selv om Bs celle er frisk, og A kan ikke pensjoneres gjennom den innkommende logiske close-meldingen. Fysisk stenging kan tilbakekalle forbindelsen, men tar da også B. Det finnes ikke et krav i Meddle-kontrakten om at enhver tillatt operasjon returnerer raskt.

Dette er blokkering mellom logiske kanaler på samme socket; jeg påstår ikke at én socket dermed omgår proof, tømmer et ubegrenset task-budsjett eller blokkerer alle andre fysiske sockets. N30s opptaksgrenser er reelle. Feilen er at korrekt ordning av en strøm nå også serialiserer fullføringen av uavhengige operasjoner og livsløpsmeldinger.

Eksisterende tester fanger ikke dette: `T/VaporWebSocketAdmissionTests.swift:22–49,223–253` bruker separate sockets som søsken. `T/BridgeChannelWebSocketTests.swift:48–105` åpner én logisk kanal og beviser origin-signering under protected read. Den beviser ikke fremdrift for to logiske kanaler.

Rett ved å skille ordnet, begrenset opptak/levering fra venting på fullført cellearbeid, med passende eierskap per logisk kanal/strøm og fremdrift for close. Bevar N24s channelID-/send-levetid, N27s eksakte feedrekkefølge og N30s opptak før nye kopier/tasks. **Påkrevd regresjon:** virkelig Vapor WS med minst to logiske kanaler, barrierestoppet A, vellykket B før A slippes, selektiv close av A, beholdt kvote for faktisk uferdig A-arbeid og avvisning av sent A-resultat. Kjør også samme-kanal feedrekkefølge og signing-control igjen.

**N36 — Høy. En gammel godkjenningshandling kan godkjenne en ny pending-request med samme fjern-ID og requestId. Gjelder kontakt og detaljdeling.**

Kilde: **E:643–665,972–994,1458–1481,1499–1528,1567–1578** og **SC:50–57,70–94,109–118**.

Det innkommende kontaktvarselet viser den verifiserte forespørselen og legger hele request-objektet i `acceptContact`-handlingen. Men akseptfunksjonen bruker bare `requesterSessionUUID` og `requestId` fra det viste objektet. Den finner **nåværende** `service.consumerContext` og konsumerer den pending-recorden som finnes under disse ID-ene i den nåværende generasjonen. Deretter signerer og lagrer den `record.payload`, ikke nødvendigvis forespørselen som brukeren så.

En remote kan velge requestId. Etter at gammel generasjon er pensjonert, kan en ny autentisert kanal med samme fjern-UUID legge inn en ny, gyldig signert forespørsel med samme requestId, annen kropp og eventuelt annen signeringsnøkkel. Brukeren kan så klikke den gamle handlingen. Alt nytt kryptografisk proof kan være korrekt, men klikket blir brukt som samtykke til **det nye innholdet/den nye principalen**. Samme kanal kan også gjenbruke requestId etter pending-TTL med en ny gyldig forespørsel; tombstonen hindrer bare gjenbruk mens den beholdes.

Detaljgodkjenning har samme problem: handlingen inneholder bare remoteUUID/requestId/action, og :1507/:1522 velger nåværende context/pending før valgte referanser deles. Dette omgår ikke gate eller resolver-grants. Det bryter bindingen mellom det mennesket godkjente, og effekten som utføres: signert kontaktbevis/persistens eller utlevering av valgte detaljer.

`T/EntityScannerConsumerSecurityTests.swift:73–104` dekker normal godkjenning/replay og proof-binding. :429–455 dekker gamle **svar** etter reconnect. Ingen av dem beholder en gammel brukerhandling, setter inn en ny pending med samme ID og utfører den gamle handlingen.

Rett med en lokal, engangs godkjenningsidentifikator bundet til nøyaktig pending-instans, request-hash, principal og kanalgenerasjon. En foreldet handling må avvises før consume/sign/send/persist, og må ikke konsumere den nye legitime recorden. **Påkrevd regresjon:** hold gammel UI-payload; close/reconnect med samme UUID og annen nøkkel; legg inn ny gyldig request med samme ID; bruk gammel handling og krev null signering, sending og lagring, samt at ny pending fortsatt kan godkjennes med sin ferske handling. Gjenta for samme-kanal TTL/gjenbruk og for detaljdeling.

**N37 — Middels. Consumerens øvrige beholdte data er ikke omfattet av den nye count-/byte-/levetidsgrensen. To konkrete deler må håndteres. Gjelder radar, ikke WS.**

**a. Radarens entitetsliste.** Kilde: **E:169–174,1130–1138,1153–1163,1180–1233**; **RM:392–401,420–441,460–480**. Hver godkjente found-event går også inn i `radarLedger.entitiesById`. `retirePeerState` fjerner de tre nye kvotebelagte tabellene og probe-resultatet, men fjerner ikke entiteten fra ledgeren. En lost-event oppdaterer en eksisterende rad; den fjerner den heller ikke. Den eneste `radarLedger.prune` i EntityScannerCell skjer ved et autorisert **get av radar**. Verken discovery-expiry, UUID-erstatning eller periodisk servicevedlikehold kaller denne.

Dermed kan en aktiv scanner uten polling av radar-get beholde stadig flere ledger-rader gjennom mange discovery-/TTL-vinduer mens de tre testede dictionary-tellerne og consumer-leases ser korrekte ut. Dette krever ikke kanalproof: discovery er nok. Selv når radar-get kalles, mangler listen en eksplisitt count-/byte-grense uavhengig av polling. En godkjent tidsbegrenset scanning begrenser angrepsvarigheten, men er ikke den leverte faste consumer-kvoten. Jeg har ikke målt OOM eller RSS for dette forløpet.

**b. Probe-historikken.** Kilde: **NP:72–79,83–123,132–139**, **E:1402–1435,1153–1163,531–550**. Gyldige innkommende aggregate-forespørsler legger requestId, nonce og remoteUUID i `handledRequestIDs`, `handledNonces` og `probeCountByRemoteUUID`. Bare minutttidsstemplene beskjæres. Peer-retirement fjerner kun `resultsByRemoteUUID`; de tre historikksamlingene blir igjen til full `probeSession.reset()` ved stopp. De er ikke med i ScannerPendingRequests eller consumer-budsjettet.

Denne delen krever autentiserte, godkjente peer-kanaler og gyldig overlap. Standardpolicy er åtte timer, to forespørsler per remote og tolv per minutt (`NearbyDisclosurePolicy.swift:6,44–45`), så standardforløpet har en tids-/rateavledet grense på omtrent 5760 innkommende forespørsler per full åttetimersperiode. Jeg kaller det **ikke uendelig vekst under standardpolicy**, eller bevist minneutmattelse. Policyvalideringen ved :110–128 setter imidlertid ikke noe maksimalt tidsvindu eller positivt ratetak. Nye remote-UUID-er kan fylle historikken på tvers av pensjonerte peers og vinduer, uten den faste globale count-/byte-grensen som N28-leveransen ellers søker å etablere. Replay-/personvernregnskapet skal fortsatt beholdes lenge nok; blind sletting ved hver reconnect er heller ikke en sikker retting.

`T/ScannerRetainedStateTests.swift:10–90` ville fanget den opprinnelige veksten i peerStates/beacons/overlaps, men teller ikke ledger-rader eller disse historikksamlingene. De gamle probe-testene av rate/replay beviser heller ikke samlet retained state over mange peer-/policyvinduer.

Rett med eksplisitt eierskap og count-/byte-/levetidsgrenser også for disse dataene. Discovery-opprydding må ikke avhenge av at UI leser, og replay/rate-historikk må ha en begrenset modell som ikke åpner gjenbruk ved rask reconnect. **Påkrevd regresjon:** kjør UUID-rotasjon og expiry gjennom virkelig EntityScannerCell uten ett eneste radar-get; mål alle beholdte samlinger og faktisk beholdte bytes, og krev hardt tak samt fungerende legitim peer. Legg til gyldige innkommende probes over flere ratevinduer og mange pensjonerte UUID-er, med assertions for både begrensning og fortsatt replay-/ratebeskyttelse. Del a og b er begge åpne; N28/N16 telles ikke i tillegg.

**N38 — Lav. Pending pensjoneres ved close, men aggregate-tilstanden kan bli stående i `.probing`; første friske forsøk feiler. Gjelder radar.**

Kilde: **E:1320–1322,1367–1393,1279–1294**, **SC:70–76**, **S:586–592** og `CellProtocol/Sources/CellApple/EntityRadar/NearbyPeerState.swift:25–38`.

Start en aggregate-probe og lukk kanalen før svar mens peerens discovery-lease fortsatt lever. `scannerChannelRetired` fjerner pending for generasjonen, men `retire` kaller ikke expiry-funksjonen som setter state tilbake. `scannerPeerStateChanged` kan beholde peer-state fordi source fortsatt er den samme levende discovery-leasen. Etter reconnect står den derfor i `.probing` uten en tilhørende utestående aggregate.

Den neste friske aggregate-forespørselen forsøker overgangen `.probing → .probing`, som er ulovlig, og returnerer feil. Catch-banen setter deretter state tilbake til `.beaconMatched`, slik at et senere manuelt forsøk kan virke. Det er altså **ikke** bevist permanent blokkering av alle manuelle forsøk. Automatisk onOverlap er derimot også avhengig av `.beaconMatched` og engangssettet `automaticProbeRemoteUUIDs`, som ikke fjernes av kanalretirement når discovery beholdes; automatisk gjenforsøk kan dermed utebli.

Reconnect-testen `T/EntityScannerConsumerSecurityTests.swift:429–455` prøver frisk **detail**, som ikke trenger denne overgangen. :458–485 prøver aggregate etter TTL mens context lever. Ingen prøver den første friske aggregate etter close/reconnect med beholdt discovery.

Rett ved å pensjonere pending og dens eide operasjonstilstand samlet, bundet til riktig generasjon, uten at gammel cleanup kan nullstille en ny probe. **Påkrevd regresjon:** gate-close og reconnect med beholdt discovery, gammel response avvises, første friske aggregate lykkes, automatisk retry følger valgt policy, og en annen peer påvirkes ikke.

**4. Tidligere funn som fortsatt er åpne**

**N12 — Høy, native NI-verifikasjon mangler fortsatt. Bare nærhetsradar; ikke WS-serverens proof-bane.**

NI-koden er uendret fra kontroll 6. NI:61–78 binder wiretoken til format, identitet, sessions/setup og NI-generasjon. NI:83–163 oppretter/retter/pensjonerer per fysisk context. NI:169–223 har separat native NISession, secure archive/decode, konfigurering og filtrering av eksakt session/token i callback. S:1174–1183 sender i fanget autentisert context; S:1433–1445 oppretter relevant NI-entry før innkommende token behandles. Den gamle globale B/C-feiltilordningen er rettet i lest kilde.

`T/ScannerNearbyInteractionTests.swift:41–171` ville fanget den **modellerte** originalfeilen: feil peer, B/C, gammelt callback, stop/revoke/reconnect/suspension. Men fake-driveren ved :180–194 bruker syntetiske tokenbytes, og fixture ved :207–210 injiserer den. Den iOS-spesifikke testen ved :174–175 prøver avvisning av et ugyldig arkiv. Den beviser verken gyldig native NIDiscoveryToken-rundtur eller faktisk ranging.

Før lukking trengs vellykket relevant iOS-bygg/test, en gyldig native secure-archive/decode-rundtur og **NI mellom to støttede fysiske iPhones**, med logg som binder resultatet til riktig autentisert kanal. Den opprinnelige B/C-feilen krever i tillegg native interleaving med flere sessions/tokens og kontroll av sen callback, reconnect, revoke, stop og suspension; en enkel totelefon-demonstrasjon alene beviser ikke alle disse variantene. Apple beskriver faktisk tokenutveksling, NINearbyPeerConfiguration og NISessionDelegate-livsløp; fake-driverne erstatter ikke dette. [Apple: Initiating and maintaining a session](https://developer.apple.com/documentation/nearbyinteraction/initiating-and-maintaining-a-session).

**N31 — Middels, minimumsbygg og siste SHA er uverifisert. Gjelder iOS-pakken, ikke Vapor-kompilering på server.**

Kildeendringen ved `CellTreeView.swift:221–229` bruker iOS 17-guard for `.focusable(false)` og beholder macOS-grenen. Dette samsvarer med API-ets tilgjengelighet og eksisterende modifikatormønster ved :231–239. [Apple: focusable(_:)](https://developer.apple.com/documentation/swiftui/view/focusable%28_%3A%29).

Det er en rimelig retting av den observerte iOS 16-kompilatorfeilen. Men det finnes fortsatt **ingen vellykket iOS 16-kompilering på 3824cf84**. Diskvakten stoppet også den bestilte etterfølgende iOS-jobben. Flere byggefeil kan bli synlige etter denne. Full macOS build/test og CI for den siste committen er heller ikke kjørt. Dette er en verifikasjonsrest, ikke en påstand om at den nye availability-guarden er bevist feil. Minimumsbygg, relevante tester og ny CI må knyttes til den faktisk leverte headen før lukking.

**N32 — Lav, terminalstatusens levetid/service-eierskap er fortsatt feil. Gjelder radarstatus.**

Kilde: **E:531–556,1141–1150,1268–1277**, **S:597–627,749–762,781–813**, **RM:254–267,439–453,529–535**.

Den direkte eventkø-feilen er rettet. Men `stopConnectService` setter `connectService = nil`, kaller `service.stop()` og returnerer uten å vente på terminalpublisering. S:601 planlegger den med `[weak self]`. Med ingen andre sterke eiere kan tjenesten deinitialiseres før MainActor-tasken kjører, slik at «stopped» faller bort. Timeren fanger også self svakt. Testen beholder derimot tjenesten gjennom eksplisitt drenering.

Dette repareres ikke av cellens «Stopping»-flow: den bruker topic `scanner`, mens statusparseren forventer `scanner.status`; `radarLedger.clear()` nullstiller ikke `scannerStatus`. Radar-spec kan derfor fortsette med gammel status og aktiv sweep etter stopp.

Motsatt, hvis gammel service holdes i live av uferdig arbeid og terminalpubliseringen kommer etter at ny service er startet, avviser verken `scannerStatusChanged` eller `connectedDevicesChanged` den gamle manageren. Den gamle terminalstatusen/tomme forbindelseslisten kan da overskrive ny services publiserte bilde. Den nye `scannerPeerStateChanged` har korrekt manager-vakt ved E:1154, men de to publiseringsbanene har ikke tilsvarende vern. Terminal-generasjon internt i én service løser ikke bytte av hele serviceobjektet.

Rett terminallevering med eksplisitt levetid og riktig service-eierskap helt ut til consumer/UI. **Påkrevd regresjon:** kjør faktisk `EntityScannerCell.stopConnectService`, slipp siste sterke service-referanse før utsatt drenering, og krev stopped én gang og inaktiv radar. Start deretter ny service før en holdt gammel terminal/callback slippes; ny status og forbindelsesliste skal forbli riktige. Dette er en rest under N32, ikke et nytt N39-funn eller påstand om fortsatt kanalmyndighet.

**5. Adversariell vurdering av samspillet og tidligere rettinger**

Jeg finner ingen ny konkret nøkkel-, signatur- eller AEAD-omgåelse i den leste endringsflaten. Dette er **ikke** et nytt fullstendig kryptografisk sikkerhetsbevis. `BridgePeerChannelAuthentication`, `BridgePeerRecordLayer`, `BridgePeerFlowControl`, `BridgeChannelAuthentication`, `BridgeChannelSession` og `BridgeChannelClientOperation` har ingen diff fra kontroll 6; den tidligere designvurderingen er derfor arvet for disse filene, ikke fremstilt som en ny full kildeaudit.

Samspillet er kontrollert særlig på disse punktene:

- **Feed og pensjonering:** B:1775–1902 tar opptak før køing og beholder kvote for pågående fysisk send etter close. Dette bevarer hensikten i N18/N24/N25. Upstream failure har eksplisitt avslutning; normal completion drenerer. Mux-søskentesten ved `T/BridgeFeedAndRPCOrderingTests.swift:356–383` kontrollerer selektiv feil i den logiske feedbanen, men den utelukker ikke N35 i den ytre Vapor-mottakskøen.
- **RPC og principal:** cid-eierskap og revalidering under samme livsløpslås gjør at tidlig eller gammel set/description-response ikke lenger velger en tilfeldig keypath-waiter. N23s get-retting og N34s utvidelse er forenlige. Dette bør ikke svekkes når parallelle mux-kanaler rettes.
- **Origin-signering gjennom WS:** V:300 og G:489–495 klassifiserer et signeringssvar ved lokal pending-request, ikke ved at motparten bare sender en signaturlignende payload. Hintet gir køprioritet; normal gate-/responsevalidering består. M:975–978 bruker også channelID. Den virkelige loopback WS-/mux-testen ved `T/BridgeChannelWebSocketTests.swift:44–112` krever proof før protected read og null bruk av serverens signer. Den er viktig positiv evidens, men dekker én logisk kanal.
- **Grense før arbeid:** V:275–325 er en reell forbedring før Data-kopi/Task. Reservasjonene beholdes også ved holdt audit/consumer, og fysisk close samles. Dette gir ikke automatisk en total prosess-/kernelminnegrense eller fri fremdrift mellom logiske kanaler.
- **Consumer-effekter:** SCs frosne principal/generasjon hindrer at et gammelt svar får nytt kanalmandat. N36 viser en annen grense: valget av hvilken ny record et gammelt menneskelig klikk skal konsumere. Kanalautentisering kan ikke erstatte bindingen til den viste forespørselen. N37 og N38 viser tilsvarende at riktig pending-levetid ikke alene begrenser all kopiert state eller rydder alle state-machine-overganger.

For sporbarhet videreføres tidligere poster med opprinnelig alvorlighet: **N07/N08/N14/N20/N23 (høy), N09/N10/N11/N15/N17/N18/N24/N25 (middels), N19/N21/N22/N26 (lav)** var lukket for sine konkrete feilforløp i kontroll 6. Ingen av dem erklæres som en helt ny fullstendig audit her. N13 (høy) og N16 (middels) hadde allerede rester ført videre som N29 og N28; nye tilgrensende rester står nå uttrykkelig i N36–N38. De telles ikke dobbelt. N12 er fortsatt åpen som beskrevet. Eldre N01–N06 er ikke revurdert i denne kontrollen; særlig tidligere N05 om downstream-inngress er **ikke lest/lukket på nytt** og ligger utenfor denne PR-funntellingen.

Designets grenser består: proof viser kontroll over en nøkkel, ikke personidentitet, sannheten i discovery eller fysisk nærhet. En aktivt akseptert motpart får den identitetsdisclosure som policyen tillater. MCs `.required` ytre kryptering erstatter ikke indre v3-proof/AEAD. Ingen ekstern/formell kryptorevisjon eller attestert nullstilling av alle OS-/providerkopier følger av de leverte testene.

**6. CI, lokale resultater, native MC og iOS**

Resultatene er eksisterende leveranser kontrollert mot relevante rålinjer, manifest/markører og GitHub. Ingen nye tester ble kjørt av meg. Evidensstier nedenfor er relative til denne rapportens katalog med mindre HAVEN-prefiks er oppgitt.

| Kontroll | Kontrollert resultat | Avgrensning |
|---|---|---|
| N28–N33 lokalt bygg | `evidence-cp53-n28-n33/final-build.log`: **Build complete, 5,65 s, COMMAND_EXIT=0** | Gjelder 02f857e0-leveransen, ikke den etterfølgende N31-committen. |
| N28–N33 lokal fulltest | `delivered-test.log:4582`: **CellBase 1507 tester, 12 skips, 3 feil**, 65,146 s; HavenCommons 26/0 og CellNearby 3/0, totalt 1536 rapporterte tester | Lokal fullsuite er **ikke grønn**. |
| De tre lokale feilene | Samme to legacy-private-key-/migreringstester med CDSA/EPERM 100001 og scoped-secret-test med Keychain −25291 som tidligere | De samme tre testene består i macOS-CI. Det støtter miljøforklaringen, men jeg har ikke selv årsaksisolert eller rettet den lokale Keychain-verten. |
| N28–N33 lokal relevant TSAN | `final-tsan.log:1421`: **169 tester, 0 feil**, 49,014 s | Kjøringen var før siste native assertions; rapportens produksjonskode var den samme. Filtrert matrise, ikke hele appen/native NI. |
| N28–N33 native MC-parent | `native-connections.log:204`: **1 parenttest, 0 feil**, 44,012 s | Parent starter begge inviterretninger, fysisk treprosess-isolasjon og treprosess-relay. Én Mac med flere OS-prosesser. |
| N27/N34 historiske lokale prøver | Full CellBase **1489 / 12 skips / 3 feil**; relevant TSAN **157 / 0** | Tidligere leveranse i samme rettingsrekke, ikke nye resultater på 3824cf84. |
| N30 historiske lokale prøver | Full CellBase **1500 / 12 skips / 3 feil**; relevant TSAN **162 / 0**, 32,844 s | Samme avgrensning; senere N28–N33-resultater er ferskere. |
| macOS-CI | [run 36561187257](https://github.com/Digipomps/CellProtocol/actions/runs/36561187257): **1541 tester, 5 skips, 0 feil**; TSAN **3 × 169, 0 feil** | Rå `0_regression.txt`: fullsuite :30591; TSAN :57838/:58768/:59698. TSAN 46,036 / 51,645 / 48,097 s. Ingen av de tre lokale Keychain-testene feilet. |
| Linux-CI | [run 36561187246](https://github.com/Digipomps/CellProtocol/actions/runs/36561187246): **162 tester, 0 feil**, 10,731 s | Konfigurert Linux-subsett, ingen Apple MC/NI. Rå ZIP i `ci-linux-logs.zip`. |
| Vapor vault-CI | [run 36561187272](https://github.com/Digipomps/CellProtocol/actions/runs/36561187272): **25 tester, 0 feil**, 0,440 s | Vault-porten, ikke alene WS-/mux-adversarialitet. Rå ZIP i `ci-vault-logs.zip`. |
| Øvrige sjekker | [Capacity 36561187249](https://github.com/Digipomps/CellProtocol/actions/runs/36561187249) og [Notify 36561182929](https://github.com/Digipomps/CellProtocol/actions/runs/36561182929): SUCCESS | Status kontrollert. Benchmarkinnholdet er **ikke lest** i denne kontrollen. Notify er ingen sikkerhetstest. |
| Eksakt review-head 3824cf84 | **Ingen vellykket ny build/test/CI** | N31-rapporten sier dette eksplisitt. Kun SwiftUI-guarden skiller fra den CI-testede brokoden. |

PR-sjekkene er knyttet til 02f857e0. macOS-/Linux-/vault-jobbene bruker syntetisk PR-merge **`5a1afa92ae30a72bec9b2fca9a64f522e3b7ac0c`**, med main `81601a6f835252aba7e99d43786fb5d67227c245` og PR-head som foreldre. Dette er en CI-checkout, ingen faktisk merge av PR-en. Sammenligning mot 02f857e0 gir fem main-forskjeller: Linux-workflow, Vault-Idea-Retention-doc, VaultCell, VaultIdeaRetention og dens test. Ingen bro-/Scanner-/brotestfil ligger i forskjellen. CI er dermed relevant for brokoden, men skal ikke beskrives som bygg av eksakt 3824cf84.

**Native toprosess-/flerprosessbevis.** De siste fire scenarienes markører er kontrollert i artefaktene referert av N28–N33-manifestet:

- Direkte par `cp53-multipeer-3B44B991-F852-46D0-B3E8-07EFBCEA6A30`: begge `.passed`, sealed send/receive 71/71. Motsatt inviterretning `cp53-multipeer-3DF257B0-0452-442A-ACA7-951448FA3F2E`: begge `.passed`, henholdsvis 65/65 og 71/71.
- `cp53-isolation-F4813929-0C9A-496F-8BE7-E188A94FD47C`: `blocked.full` viser **32 records / 1 583 870 bytes**, RSS **51 036 160 → 53 248 000**. `blocked.checked` viser én frisk fysisk forbindelse og **178 søskenverdier**. A og C har passed-markører. Den faktiske 64 MiB-resourceoverføringen ble avbrutt; resource-completion rapporterte feil, og fysisk disconnect ble observert. Streammarkøren viser ni åpninger og disconnect. No-proof-expiry ble observert etter ca. **10,187 s**; dette er ikke et naturlig femminuttersutløp for en allerede autentisert produksjonskanal.
- `cp53-relay-43E0DB7E-3CCD-494D-A0AC-A642DFC87E2F`: M/I/R har passed-markører; M bruker to uavhengige MC-forbindelser, videresender de indre wirebytene uten endpoint-nøkler, og endepunktene rapporterer åtte ordnede private verdier.

`T/ScannerMultipeerProcessTests.swift:18–47,63–84` viser ekte discovery/invitasjon/MCSession og begge retninger, men testverten bruker **GeneralCell** som scanner-consumer. Den er ikke et komplett native EntityScannerCell/UI-forløp. Den separate relayen bruker produksjonsgaten med testadapter og syntetiske lokale vaults. Parent/oppsett og relevante isolation-assertions er lest; hele relay-testfilen er **ikke lest på nytt i denne kontrollen**. Markører og tidligere kontroll kan ikke oppgraderes til en full ny native kodeaudit.

N18s dokumenterte plattformgrense gjelder fortsatt: MC kan materialisere Data før appens callback, og den leverte koden dokumenterer ikke et absolutt før-allokerings-/kernelminnetak. Resource-cancel og et målt bounded vindu er nyttige bevis, men ikke total DoS-beskyttelse. Ingen ny før-callback allokasjonsmåling ble utført.

**iOS-forløpet, fra privat bevisplassering.** Jeg brukte `HAVEN-Deploy/_handoff/BRO/cp53-n12-evidence/ios-*`, ikke en antatt fortsatt plassering i det offentlige CP-repoet. `head.txt` og relevante operatorlogglinjer er kontrollert. Lange logger er lest i relevante utdrag, ikke linje for linje.

| Beviskatalog / logg | Head / resultat | Hva som faktisk ble kjørt |
|---|---|---|
| `ios-20260929T093621` | 1e3e7f10; operator.log :408/:413: Xcode build-system crash / BUILD FAILED | CellApple `generic/platform=iOS Simulator` **build**, Xcode 27.0 / 27A266a. Ingen XCTest. |
| `ios-20260929T133057` | 02f857e0; diskvakt stoppet før kompilering | Intet kompilasjons-/simulatortestresultat. |
| `ios-20260929T135351` | 02f857e0; samme build-system crash ved :408/:413 | Nytt feilet byggforsøk, ingen bestått test. |
| `ios-20260929T135702` | 02f857e0; operator.log :26045: `.focusable` krever iOS 17; :26538 BUILD FAILED | Kompilatoren nådde den konkrete N31-feilen. Dette var fortsatt en build-kommando, ikke en simulatortest. |
| `ios-20260929T153115` og `cp53-ios-bygg-5-20260929.log:1–3` | **3824cf84**; diskvakt stoppet før kompilering | 55,2 GiB / 5 % fri; 10 GiB reserve ville gitt 45,2 GiB / 4 %. Kravet er minst 40 GiB **og** 5 %. Ingen ny Swift-/Xcode-test ble kjørt. |

Kontroll 6 hadde en bestått iOS 18 device-target-krysskompilering på 1e3e7f10. Den er historisk støtte for at den daværende iOS-kodegrenen kunne kompilere, ikke et bestått iOS 16-minimumsbygg, simulator-XCTest eller NI/UWB-bevis på denne leveransen. Ingen av de nye loggene endrer dette.

**Fortsatt ikke kjørt/bevist:** gyldig native NIDiscoveryToken archive/decode-rundtur; vellykket iOS-simulatortestkjøring; NI mellom to fysiske iPhones; native B/C-token-/callback-interleaving; native NI-reconnect/revoke/stop/suspension; nye reproduksjoner for N35–N38 og N32-rest; eksakt review-heads minimumsbygg/fulltest/CI. Heller ikke to fysiske Mac-er/nettbytte, ekstern treg WS-motpart, langvarig fuzz-/lastkampanje, naturlig native femminuttersutløp, Binding-/CellScaffold-appbygg eller faktisk produksjonsutrulling er verifisert av denne kontrollen.

**7. Merge- og produksjonsbeslutning**

| Åpen post | Alvorlighet | Teknisk berørt flate | Hva som må til før posten kan lukkes |
|---|---|---|---|
| N12 | Høy | Native NI / nærhetsradar | iOS-/native-tokenbevis og fysisk NI-verifikasjon, inklusive korrekt peer-/livsløpsbinding. |
| N31 | Middels | iOS 16-pakken og siste commits verifikasjon | Vellykket minimumsbygg og aktuelle lokale/CI-resultater på faktisk leveranse-head. |
| N32 | Lav | Radarstatus ved stopp/servicebytte | Terminallevering med korrekt eierskap og faktisk cellestopp-/ny-service-regresjon. |
| N35 | Middels | **Vapor/WS med mux** | Uavhengig fremdrift og selektiv close for logiske kanaler, med kvoter og ordning bevart. |
| N36 | Høy | Kontaktgodkjenning og radardetaljer | Engangsbinding mellom vist godkjenning og eksakt pending/principal/generasjon. |
| N37 | Middels | Radarens beholdte state | Hardt og målt tak for ledger **og** probe-historikk, uavhengig av UI-polling og med replayvern bevart. |
| N38 | Lav | Aggregate-probe etter kanalretirement | Pending og eiet state pensjoneres sammen; første friske/automatiske forsøk testes. |

For **WS-broen i prod** er N35 et konkret nytt problem i den leverte produksjonsadapteren. En ren enkeltkanal-socket rammes ikke av akkurat søskenkanal-eksempelet, men jeg har ikke lest/verifisert produksjonsvertens nåværende muxvalg eller tidligere N05/downstream-porter og kan derfor ikke bruke en antatt «mux av»-konfigurasjon som produksjonsgodkjenning. Ingen ny påstand om at NI-feil i seg selv kompromitterer WS-proof er gjort.

For **hele PR #53** gjelder Kjetils valgte port: alle funn rettes før merge. Derfor er anbefalingen **ikke merge**, også om radar/NI ikke tas i bruk ved første WS-utrulling. De syv postene omfatter både kilderettinger og utestående bevis; å kalle dem «syv kodefeil» ville være upresist. Etter retting må de foreslåtte målrettede regresjonene, relevant eksisterende suite og CI knyttes til ny faktisk head. En grønn kjøring på 02f857e0 alene er ikke tilstrekkelig.

**8. Lesedekning og læring for neste kontroll**

Lest på review-SHA: endringene og relevante omkringliggende livsløp i B, M, G, V/VB, S/SA/SC, E, NI og CellTreeView; NP, policy/state-machine og aktuelle RM-områder; de siterte testmetodene og relevante fixture-oppsett. Den store EntityScannerCell er **ikke lest i sin helhet**. Heller ikke hele BridgeBase/mux-hjelpekoden, alle dependencies, hele advertisement-protokollen, alle resolver-/lagringspolicier eller alle UI-renderere er en full audit i denne runden. Uendrede kryptokjernefiler støttes av kontroll 6 og diffkontroll, ikke av en påstått ny total gjennomlesing. Binding/CellScaffold/prod-konfigurasjon og alle gamle mellomkjøringslogger er **ikke lest** utover uttrykkelig nevnte bevis.

Gjenbrukbar læring: mål **alle** beholdte kopier i virkelig consumer, også UI-ledger og replay/rate-historikk; en grønn test av nye lease-tellere er ikke tilstrekkelig. Test livsløpet der eieren faktisk slipper objektet, ikke bare en test som beholder service og drenerer manuelt. Prøv friske operasjoner etter retirement, ikke bare at gamle svar avvises. Og prøv to logiske mux-kanaler gjennom den faktiske ytre adapteren; uavhengige fysiske sockets beviser en annen egenskap.

Disse læringene er bevart her. Etter den uttrykkelige bestillingen **«én rapportfil»** har jeg ikke endret skills, læringsledger, hendelseslogg eller kjørt muterende haven_learn capture/sync. Eksisterende arbeidstrær og leveransefiler er urørt.
