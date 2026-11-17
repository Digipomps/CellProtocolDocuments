STATUS: LEVERT — anbefaling: ikke merge, 15 funn (15 blokkerer)

# Astra kontroll 5 — CellProtocol PR #53

Dato: 28.09.2026. Lese- og vurderingsjobb. Ingen kodeendring, testendring, commit, push eller merge. Denne rapporten er eneste tilsiktede filendring.

## 1. Konklusjon og vurdert kilde

**N17 og N19 er lukket. De øvrige elleve funnene fra kontroll 4 er ikke rettet. v3 er ikke implementert.** Fire ytterligere livsløpsfeil er identifisert i kildekoden, N23–N26. Dermed er dette ikke en kontroll av en ferdig rettet v3-leveranse: det er kontroll av siste faktisk leverte commit og av stoppene som hindret resten.

Vurdert head er **`605298fe404d46827100559a862ec2e9b1978fc8`**, siste LEVERT i den angitte rapportrekkefølgen. GitHub oppga samme head for den åpne [PR #53](https://github.com/Digipomps/CellProtocol/pull/53), uten merge. Kilde er lest med `git show <SHA>:<fil>`, ikke fra det skitne arbeidstreet. Commitobjektet og de relevante kildefilene er tilgjengelige selv om implementørens særskilte arbeidstre mangler Git-administrasjonsmappe. Dette gir grunnlag for LEVERT vurdering, ikke for å late som de stoppede arbeidene er utført.

Alle fire tidligere Astra-kontroller og `PEER-V3-DESIGN.md` er lest. Implementørrapportene er lest i bestilt rekkefølge:

| Rapport i handoff-mappen | Status | Betydning for denne kontrollen |
|---|---|---|
| `CP53-N17-N19.md` | LEVERT, `605298fe…` | Eneste nye implementasjonsleveranse. Første endringscommit `743fbaf…`, deretter endelig head med testfiksturretting. |
| `CP53-V3.md` | STOPPET | Arbeidstreets Git-administrasjonsmappe mangler. Ingen levert v3. |
| `CP53-N10-N11-N16.md` | STOPPET | Avhengig av stoppet v3 og samme arbeidstreproblem. |
| `CP53-N14-N15-N18.md` | STOPPET | Foregående arbeid stoppet; ingen levert retting. |
| `CP53-N13-N20.md` | STOPPET | Foregående arbeid stoppet; ingen levert retting. |
| `CP53-N12.md` | STOPPET | Foregående arbeid stoppet; ingen levert NI-retting. |
| `CP53-SAMLET.md` | STOPPET | Ingen samlet ferdigleveranse; heller ingen N21-lukking. |

Ingen av de sju rapportene mangler. Ingen er DELVIS. STOPPET-rapportenes eksistens er ikke leveransebevis.

Sammenliknet med kontroll 4-head `1b8efe1cbca33997facf50a37ee0fbfff9dc7b14` endres 14 filer, +450/−59 linjer. Endringene gjelder kanonisk kvotenøkkel, diagnostikk, tilhørende tester/dokumentasjon og Linux-testutvalg/fikstur. **Peer-handshake, recordlag, gate, Scanner, EntityScanner og mux er uendret.** Nye funn nedenfor betyr nyoppdaget i kontroll 5, ikke nødvendigvis introdusert av disse to commitene.

### Telling og alvorlighet

De 15 åpne, selvstendige funnene er **N10–N16, N18, N20–N26**: 5 høy, 7 middels, 3 lav. Elleve er videreført fra kontroll 4, fire er nye. N08s gjenværende bredere livsløpsproblem og N09s manglende NI-lukking telles ikke en gang til ved siden av de konkrete funnene som dekker dem.

Kontroll 4 skilte mellom selvstendige sikkerhetsblokkere og lavere alvorlighet. Kjetils senere beslutning om at **alle 13 skulle rettes før merge**, sammen med kravet om å luke ut nye oppdagede sårbarheter, gjør også de lave funnene til mergeblokkere i denne leveransen. Det gjør ikke alvorligheten deres høyere. Manglende tester/bygg er oppført som verifikasjonskrav, ikke ekstra funn for å blåse opp antallet.

### Henvisningsnøkkel

Alle `alias:linje` nedenfor viser til **vurdert head**, ikke dagens arbeidsfiler. Lenken på hvert alias åpner hele filen på denne SHA-en. Testalias uten annet oppgitt ligger i `Tests/CellBaseTests/`.

| Alias | Fil i CellProtocol |
|---|---|
| A | [Sources/CellBase/Cells/Bridging/BridgeChannelAuthentication.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeChannelAuthentication.swift) |
| P | [Sources/CellBase/Cells/Bridging/BridgePeerChannelAuthentication.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgePeerChannelAuthentication.swift) |
| R | [Sources/CellBase/Cells/Bridging/BridgePeerRecordLayer.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgePeerRecordLayer.swift) |
| C | [Sources/CellBase/Cells/Bridging/BridgeChannelClientOperation.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeChannelClientOperation.swift) |
| L | [Sources/CellBase/Cells/Bridging/BridgeChannelSession.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeChannelSession.swift) |
| G | [Sources/CellBase/Cells/Bridging/BridgeChannelTransport.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeChannelTransport.swift) |
| B | [Sources/CellBase/Cells/Bridging/BridgeBase.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeBase.swift) |
| BA | [Sources/CellBase/Cells/Bridging/BridgeBaseAuditor.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeBaseAuditor.swift) |
| X | [Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift) |
| S | [Sources/CellApple/EntityRadar/ScannerService.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellApple/EntityRadar/ScannerService.swift) |
| E | [Sources/CellApple/EntityRadar/EntityScannerCell.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellApple/EntityRadar/EntityScannerCell.swift) |
| W | [Sources/CellApple/WebSocketConnection.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Sources/CellApple/WebSocketConnection.swift) |
| T | [Tests/CellBaseTests/ScannerPeerAuthenticationTests.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Tests/CellBaseTests/ScannerPeerAuthenticationTests.swift) |
| V | [Tests/CellBaseTests/BridgePeerRecordLayerTests.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Tests/CellBaseTests/BridgePeerRecordLayerTests.swift) |
| I | [Tests/CellBaseTests/ScannerServiceInvitationTests.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Tests/CellBaseTests/ScannerServiceInvitationTests.swift) |
| M | [Tests/CellBaseTests/ScannerMultipeerProcessTests.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Tests/CellBaseTests/ScannerMultipeerProcessTests.swift) |
| Q | [Tests/CellBaseTests/BridgeCanonicalKeyQuotaTests.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Tests/CellBaseTests/BridgeCanonicalKeyQuotaTests.swift) |
| D | [Tests/CellBaseTests/BridgeDiagnosticPrivacyTests.swift](https://github.com/Digipomps/CellProtocol/blob/605298fe404d46827100559a862ec2e9b1978fc8/Tests/CellBaseTests/BridgeDiagnosticPrivacyTests.swift) |

## 2. N07–N22: lukking, originalfeil og testens utsagnskraft

### N07 — høy — den konkrete mangelen på ende-til-ende recordbeskyttelse er lukket

P:60–70 binder begge helloer til signaturen. R:20–38 avleder retningsdelte nøkler fra fersk X25519 og begge signerte transkripter. S:98–104 forsegler ved fysisk sending; S:127–145 åpner før dispatch. G:99–126 krever kryptert nøkkelbekreftelse før peer blir klar.

**Ville testen fanget originalfeilen? Ja.** T:410–430 reléer de faktiske håndtrykksmeldingene og kontrollerer forseglet trafikk begge veier. T:455–463 injiserer en legitimt formet klartekstkommando og forventer ingen dispatch; det er sterkere enn bare å sende ugyldig JSON. T:467–493 endrer DH-nøkkelen på hver side. V tester recordmanipulasjon. Den gamle løsningen med klartekst etter et relébart identitetsbevis ville ikke oppfylt disse forventningene.

Avgrensning: kontrollert ledning i testen er ikke en tredje, fysisk MC-prosess. V2s tre første meldinger eksponerer fremdeles identitet; T:414–415 forventer nettopp tre uforseglede meldinger. Det er N22, ikke en grunn til å benekte rettingen av N07s applikasjonskryptering.

### N08 — høy — delvis; aktiv fysisk binding rettet, samlet livsløpskrav ikke lukket

S:65–89 fanger fysisk peer, MCSession, rolle og oppsett. S:450–460 sender til dette objektet. S:648–675, S:1064–1098 og S:1127–1130 fører mottaket til fanget kanal fremfor å slå opp nytt mål senere.

**Originaltesten treffer den etablerte kanalfeilen:** T:234–276 dekker A/B/C-kollisjon etter installert mapping, med riktig mottaker og ventende cid. T:279–353 dekker gamle callbacks og faktisk cid-gjenbruk; T:557–586 avviser gammel ciphertext med omskrevet ny header. Disse ville fanget den tidligere aktive omrutingen.

**Ikke full lukking:** invitasjon før binding har N11, videre EntityScanner-arbeid har N13, og allerede innsluppet svararbeid i BridgeBase har N23. Ingen av de nevnte callback-testene holder svaret etter auditor-await i N23. Resten telles under disse konkrete funnene.

### N09 — middels — konkret rå NI-utsending rettet i kilde; NI-kjeden ikke verifisert

S:852–858 bruker nå S:838–848 og `canSendPeerData`. MC-sendingen på S:458 er rettet mot fanget fysisk peer. Den tidligere iOS-utsendingen direkte til alle `connectedPeers` er ikke til stede.

**Ville testen fanget originalfeilen? Delvis.** T:356–407 kontrollerer felles hjelpemetode med aktiv B og ventende/revokert C, samt avvisning ved kvote. Den fanger feil i denne mottakerfiltreringen. Den ville ikke automatisk fanget en ekstra rå sending inne i en separat `#if os(iOS)`-gren. Ingen kjørt test dekker ekte NI-tokenarkiv, iOS-bygget eller to NI-enheter. N12 gjør at NI-funksjonen som helhet fortsatt ikke kan godkjennes.

### N10 — middels — ÅPEN, blokkerer: mottaksrekkefølge stopper før applikasjonsarbeidet

S:118–150 serialiserer forberedelse/dekryptering, men starter dispatch som separat `Task` på S:140. G:263–277 oppretter enda en arbeidsoppgave. B:1816 har actor-await før blant annet feed-publisering på B:1880. Gyldige records i korrekt rekkefølge kan dermed gi applikasjonsresultater i omvendt rekkefølge.

**Eksisterende test ville ikke fanget originalfeilen:** T:534–554 kontrollerer tellere og et `Set` av titler, ikke leveringsrekkefølgen. Lukking krever test som holder første dispatch, slipper andre frem og kontrollerer ordnet konsum. Løsningen må samtidig bevare fremdrift for origin-proof RPC; en grov kø som venter på sitt eget svar er ikke tilstrekkelig.

### N11 — middels — ÅPEN, blokkerer: invitasjonen er ikke atomisk bundet til fysisk peer og oppsett

S:187–192 beskriver ventende invitasjon; akseptert endpoint lagres senere etter fjern-UUID. S:552–561 fjerner ventende innslag og installerer akseptert endpoint i separate kritiske seksjoner. S:624–656 er avhengig av discovery-mapping. Kollisjonsvernet S:991–1003 virker bare mens den aktuelle mappingen finnes; S:1037–1044 kan fjerne den ved lost-peer.

Forløp: B har en ventende/akseptert invitasjon; discovery-mappingen forsvinner før autentisert gate er bundet; C annonserer samme UUID. Tilstand som tilhører invitasjonen til B kan bli brukt ved C-oppsett. Dette er ikke bevis for at C kan forfalske Bs signatur; det bryter den lokale invitasjonens mål og kan blokkere eller omrute etableringen. Utgående invitasjonsstatus har dessuten ikke fullført levetidsrydding på S:422–428 og S:640–642.

**Testen treffer ikke dette:** I:8–22 tester kryssende akseptering, I:87–109 hundre kall mot samme peer; T:234 tester allerede aktiv mapping. Krev immutable `(MCPeerID, MCSession, oppsett/generasjon, rolle, endpoint)` gjennom pending og accepted, atomisk overgang og reelle timeout-/lost-/stop-racer.

### N12 — høy — ÅPEN, blokkerer: NI-resultat er ikke bundet til den autentiserte peeren

S:344–352 har felles NI-session/token-tilstand. S:863–878 tar imot peer-parametere uten å bruke dem til en slik binding. S:894–918 starter felles session; S:1104–1113 oppdaterer siste tilknyttede UUID. S:1154–1178 omsetter token uten å bevare fysisk kanal, principal og generasjon. S:1244–1274 tilordner resultatet gjennom `connectedRemoteUUID`; callbackene S:1281–1382 kontrollerer ikke at NI-sessionen er den aktuelle autentiserte målingen. Lukking på S:526–542, S:803–825 og S:1073–1086 gir ikke en tilsvarende NI-invalidering.

Dermed kan en autentisert Cs token/resultat tilordnes B, og sene NI-callbacks kan overleve kanalens avslutning. Kryptert tokenutsending alene retter ikke dette.

**Ingen relevant originalfeiltest:** T:356–407 tester sendehjelperen, ikke NI-assosiasjon. Krev per-måling binding til fysisk peer, bevisidentitet, kanal- og NI-generasjon; invalidate ved close/revoke/stop; kontroller B/C-interleaving og sen callback. Ekte NI på to enheter er fortsatt ikke kjørt.

### N13 — høy — ÅPEN, blokkerer: arbeidsbudsjett og generasjon følger ikke EntityScanner-handleren

S:1201–1204 omslutter et synkront delegate-kall med `withAuthenticatedWork`. E:1346–1365 starter derfra en selvstendig `Task`; gaten kan frigjøre arbeidsreservasjonen før verifisering og persistens på E:1614–1690 er ferdig. Handleren bærer heller ikke fanget autentisert generasjon gjennom sine awaits. E:67–78 har delte mutable pending-tabeller uten tilsvarende isolasjon; E:1504–1526 tar imot detaljforespørsler uten en slik samlet grense. E:1634–1635 lagrer også innkommende kontaktforespørsel uten at verifikasjonssvaret er et vilkår for innsetting.

Ekstra arbeid opprettes allerede på S:1129 og i avvisningsløpet S:123. Antall tabellinnslag, bytes, TTL og oppgaver må begrenses før angriperen får tilsvarende ressursbruk, også før autentisering.

**Testen ville ikke fanget originalfeilen:** T:206–232 holder et reelt BridgeBase-feedarbeid; T:762–773 har en synkron testobservatør. Ingen av dem kjører EntityScanners asynkrone persistenshandler under lukking. Krev async delegate-kontrakt med arbeidsreservasjon til faktisk slutt, generasjonskontroll før hver effekt, serialisert tilstand og grenser med frisk B som kontroll under Cs belastning.

### N14 — høy — ÅPEN, blokkerer: MC-stream og resource omgår datagatens ressursvern

S:1133–1142 logger stream/resource-callbacks uten å lukke stream eller kansellere mottakets `Progress`. De går ikke gjennom kanalbeviset eller data-/arbeidskvotene. En fysisk tilkoblet peer kan derfor bruke disse inngangene før app-autentisering og etter logisk tilbakekalling. Dette er et ressursvernfunn; jeg har ikke vist Cell-dispatch gjennom stream/resource.

**Ingen test ville fanget dette:** T, V og M bruker Data-banen. Test faktisk stream/resource fra uautentisert og revokert peer; avvis aktivt og mål avslutning/ressurser med frisk sibling. Apple dokumenterer at mottakets `Progress` kan kansellere overføringen, og at resource mottas til midlertidig fil. Se [mottakets Progress](https://developer.apple.com/documentation/multipeerconnectivity/mcsessiondelegate/session%28_%3Adidstartreceivingresourcewithname%3Afrompeer%3Awith%3A%29?language=objc) og [resource-overføring](https://developer.apple.com/documentation/multipeerconnectivity/mcsession/sendresource%28at%3Awithname%3Atopeer%3Awithcompletionhandler%3A%29?changes=___10&language=objc).

### N15 — middels — ÅPEN, blokkerer: logisk lukking fjerner ikke den fysiske MC-peeren

S:156 kaller `peerChannelClosed`; S:462–466/S:803–825 fjerner registreringer, men kobler ikke fra den etablerte fysiske peeren. MCSession er felles på S:377–385. Frakobling på S:479/S:531 gjelder sessionen. G:397–416 frigjør transportreservasjonen etter den logiske transportens close, selv om den aktuelle MC-peeren fortsatt kan sitte tilkoblet.

Dette skiller logisk fail-closed fra fysisk ressursfrigjøring. En uvennlig peer kan beholde fysisk kapasitet; en grov felles disconnect ville ramme friske siblings.

**Eksisterende tester er utilstrekkelige:** T:124–147 måler logiske tellere; M bruker samarbeidsvillige parter. Krev fysisk observerbar, isolert pensjonering og behold riktig kvote til ressursen er borte. Ikke bruk `cancelConnectPeer` som dokumentasjon på at en etablert forbindelse kan kastes ut: Apple beskriver den som kansellering av et tilkoblingsforsøk, og `disconnect` som at lokal peer forlater sessionen. [MCSession](https://developer.apple.com/documentation/multipeerconnectivity/mcsession).

### N16 — middels — ÅPEN, blokkerer: discovery/pending kan allokere før gatekvoten

S:275–285 og S:311–320 har discovery-/pending-tabeller; S:568–594 lager timeoutarbeid, S:953–969 håndterer invitasjonskontekst og S:981–1023 discovery uten samlet antalls-, byte- og rategrense. Gateopprettelse på S:661–663 kommer senere. Ubekreftet fjern-UUID er heller ikke et pålitelig vern mot mange annonserte identiteter.

**Originalfeilen dekkes ikke:** I:87–109 bruker samme peer hundre ganger, ikke mange fysiske peers, UUID-er og kontekster. Krev grenser og TTL før innsetting/Task-opprettelse, samt belastningstest som viser stabilt antall retained objekter og at en frisk peer fortsatt kan etablere seg.

### N17 — middels — LUKKET: samme signeringsnøkkel kan ikke rotere seg til nye kvotebøtter

A:46–61 lager en separat kvoteidentifikator ved SHA-256 av en entydig JSON-array med fast formålsmerke, algoritme, kurve og kanoniske offentlige nøkkelbytes. Ed25519 valideres som rå 32 bytes. P-256s støttede komprimerte og X9.63-representasjoner normaliseres til samme komprimerte nøkkel. A:39–41 bruker denne valideringen.

L:33 lagrer kvotenøkkelen; L:88–125 bruker den for autentiserte forbindelser/rate og ressursgrenser. L:328–330 installerer den først etter signaturverifisering. **Authority er fortsatt separat:** principal/revoke bruker fortsatt domene/UUID/fingerprint på L:199–207, og L:378–384 krever den eksakte bevisidentiteten. Dette endrer ikke hvilke identiteter som får tilgang til Cells.

**Ville testen fanget originalfeilen? Ja, og regresjonsbevis finnes.** Q:59–77 kontrollerer kanonisering uten sammenslåing av principal/revokasjon. Q:80–108 roterer UUID og encoding under connection-grense og beholdt arbeid; Q:110–129 prøver rateomgåelse på tvers av domene/kilde/WS/peer og tidsvindu; Q:131–160 prøver operasjon/feed/channel med aliaser. En uavhengig nøkkel forblir brukbar. Testene signerer reelle session-proofs for begge profiler; de er ikke komplette MC-håndtrykk.

Den bevarte mutasjonskjøringen med gammel `BridgeChannelSession.swift` gir feil i de tre kvoteatferdstestene. Den nye kanoniseringshjelperen var beholdt, så dette er ikke et urørt checkout av gammel baseline. Denne presiseringen svekker ikke beviset for den gamle kvoteomgåelsen.

### N18 — middels — ÅPEN, blokkerer: sendebudsjettet følger ikke faktisk kølevetid

G:180–186 og G:365–387 reserverer bytes bare til transportens `sendData` returnerer. S:98–104 → S:450–458 ender i ikke-blokkerende `MCSession.send`. Ingen kvotert, generasjonsbundet peer-ack holder et sendefenster frem til mottak/forbruk. Innkommende Data er dessuten allerede materialisert før S:120 reserverer sitt arbeid.

**WS-kontrollen bekrefter samme svakhet i Apple-banen:** W:291–317 kaller callback-basert `URLSessionWebSocketTask.send`, men async-funksjonen returnerer uten å avvente completion. AppleBridgeTransport venter derfor ikke på den completionen når G slipper sin reservasjon. En async-signatur alene gir ingen slik garanti.

**Eksisterende test ville ikke fanget køfeilen:** T:399–407 tester én for stor sending, T:589–602 inkluderer recordoverhead; de måler ikke treg mottaker, total retained bytebruk eller OS-kø. Krev et begrenset sendefenster, autentiserte/generasjonsbundne kvitteringer der de trengs, reell completion-håndtering og fysisk avvikling ved vedvarende manglende fremdrift. Beskriv ærlig hvilken allokering OS gjør før appen kan avvise. Jeg har ikke målt en uendelig Apple-kø; funnet er at dagens appkvote ikke beviser den lovede grensen. Apple bekrefter at [MCSession.send er ikke-blokkerende](https://developer.apple.com/documentation/multipeerconnectivity/mcsession/send%28_%3Atopeers%3Awith%3A%29).

### N19 — lav — LUKKET for de rapporterte brodiagnostikkbanene

B:1027 logger lengde fremfor ugyldig description; B:1830, B:1846, B:1866 og B:1883 logger forventet type og kommandometadata; B:1973 logger ikke ukjent responsinnhold. B:1407 tar ikke med agreement-payload. `BridgeCommand.swift:61` lager metadata fra kommandoenum og numerisk cid. B:1367/B:1814/B:1965 bruker denne, og feilbanene har faste feilkoder. Tilsvarende adapterrettinger finnes i `AppleBridgeTransport.swift:64,95,103,121`, `VaporBridgeTransport.swift:236` og W:181/W:327.

**Ville testen fanget originalfeilen? Ja.** D:15–23 aktiverer loggfangst og krever ikke-tom, avgrenset logg uten hemmelig markør. D:36–49 dekker feil payloadtyper/ukjent cid, D:52–57 ugyldig description, D:59–75 agreement/ukjent get, D:77–88 transportfeil. `AppleBridgeTransportTests.swift:104–126` og `VaporBridgeTransportTests.swift:37–51` dekker adaptermarkører. Mutasjon av gammel BridgeBase gir de forventede markørfeilene.

Dette er ingen generell sertifisering av alle logger eller sikkerhetshendelser. Ikke hver catch har egen test. Resolverens `.flow`-diagnostikk, EntityScanner-logger, vertsapplikasjoner og event sinks er ikke dermed gjort payloadfrie. Dokumentasjonens uttalte avgrensning må beholdes.

### N20 — høy — ÅPEN, blokkerer: kontaktaksept beviser ikke den konkrete aksepten som fullføres

E:1647–1690 finner pending ut fra `requestId` og verifiserer signaturen med identiteten i selve payloaden gjennom E:812–842. Den sammenlikner ikke hele forventede request-hash, type/versjon, encounter-ID, session-binding og forventet signerende kanalprincipal før persistens. Feltene finnes på E:778–799. E:845–922 persisterer med lokal eier; pending fjernes først etter awaits, ikke ved en atomisk enkeltgangsreservasjon.

En gyldig selvsignert, men feilbundet aksept kan dermed bli behandlet som «Contact Established»; samtidig dobbel levering kan konkurrere om samme pending. Dette krever ikke et brudd på peer-kryptografien.

**Ingen originalfeiltest i den gjennomgåtte peer-suiten:** observatøren er ikke den virkelige EntityScanner-aksepthandleren. Krev ellers gyldig signerte negative tilfeller for hvert bundet felt, feil signer/kanal, feil request-hash og konkurrerende dobbel aksept; positiv kontroll må bevise korrekt encounter og nøyaktig én persistens.

### N21 — lav — ÅPEN, blokkerer etter bestillingen: driftsdokumentasjonen motsier faktisk wire og livsløp

`Docs/ScannerMultipeer.md:53–73` beskriver fortsatt N07 som en klartekstbegrensning, samtidig som `Documentation/BridgePeerChannelV2.md:108–123` beskriver forseglede records. Scanner-dokumentet lover også beskyttelse av pending-ruting og at gamle generasjonsframes droppes uten å lukke, uten å skille gammel fysisk callback fra en ugyldig record sendt på gjeldende kanal. Sistnevnte er fatal i R:65–78. N11 viser at pending-løftet heller ikke holder.

**Ikke en kjørbar testlukking:** dokumentene må avstemmes med faktisk levert versjon, bevisgrenser, fysisk teardown og operatørprosedyre. `CP53-SAMLET.md` er STOPPET og har ikke gjort dette. Ikke skriv v3 som implementert før det faktisk er levert.

### N22 — lav — ÅPEN, blokkerer etter bestillingen: v2 røper identitet i håndtrykket

P:31–58 bærer full offentlig identitet i hello/proofmaterialet; G:94–109 sender de første tre meldingene uten det nye recordlaget. G:62–63 tillater denne fasen. En reléende mellompart kan observere identitetene selv om etterfølgende apptrafikk er forseglet. `Documentation/BridgePeerChannelV2.md:136–142` erkjenner grensen.

**Ingen v3-testlukking:** T:414–415 forventer dagens tre klartekstmeldinger. Den tester v2s appbeskyttelse, ikke identitetsskjuling. V3-designet nedenfor er ikke implementert, og det finnes derfor ingen kjørte v3-interoperabilitets-, disclosure- eller paddingtester i leveransen.

## 3. Nye funn N23–N26

Disse er **kildebaserte, konkrete feilforløp**, ikke kjørte exploit-reproduksjoner. Jeg har ikke endret kode eller lagt inn barrierer for å demonstrere dem. Testkravene angir hvordan de skal gjøres deterministisk etterprøvbare.

### N23 — høy — blokkerer: et allerede innsluppet svar kan mutere en fornyet BridgeBase

**Kilde:** B:1811–1816 kontrollerer sessionen før `await auditor.loadBridgeCommandForCommandId`, men kontrollerer ikke fanget session/generasjon igjen når actor-kallet returnerer. BA:46–48 returnerer en kopi av kommandoen. B:1826 konfigurerer nåværende description; B:1880 bruker nåværende flow-publisher; B:1901–1904 tar nåværende get-publisher ut fra **keypath**, ikke fra den gamle kommandoens livsløp. B:488–516 bytter session/transport/publishere ved fornyelse; B:2014–2048 rydder registrene, men kan ikke trekke tilbake en kopi som auditor allerede har returnert.

**Forløp:** Et gyldig gammelt svar passerer gate og session-check. Auditor returnerer det gamle get-kallet, men fortsettelsen får ikke kjøre ennå. Kanalen lukkes og samme BridgeBase fornyes. En ny get for samme keypath får en ny cid og en ny publisher. Den gamle fortsettelsen kjører B:1902 og leverer gammelt resultat til den nye forespørselen. Tilsvarende kan gammel description endre den nye proxyens metadata/scope, eller gammel feed leveres til den nye strømmen. Dette er gammelt, allerede dekryptert arbeid; avvisning av gammel ciphertext på en ny fysisk gate retter ikke feilen.

G:270 sjekker kansellering før arbeidskroppen; kansellering er ingen automatisk sperre etter B:1816. B:1799–1800 har dessuten en sen feed-tilstandsoppdatering etter send-await uten ny generasjonskontroll; dette tilhører samme behov for å beskytte mottakerens gjeldende tilstand.

**Rettelse/test:** Gjør responsens generasjon, registrerte operasjon og uttak/publisering til én gyldig livsløpsbeslutning; en løs check med ny race før effekt er ikke nok. Hold svaret etter auditor-oppslag, lukk/forny samme BridgeBase, opprett ny get på samme keypath med annen cid, og slipp gammelt svar. Ingen gammel verdi/description/feed må nå ny tilstand; frisk forespørsel skal lykkes. T:279–353 stopper gamle fysiske callbacks tidligere. `BridgeChannelTransportTests.swift:370–383` holder et gammelt innkommende get før svarsend, ikke dette utgående svarets auditor-await.

### N24 — middels — blokkerer: mux-svar mister logisk generasjonsbinding før fysisk overlevering

**Kilde:** X:1097–1101 kontrollerer objektidentitet én gang. X:1105–1107 skriver deretter bare det gjenbrukbare wire-channelID. X:1123/X:1130–1134 avventer fysisk sending med bare felles `closed` som kontroll. G:365–387 legger sendingen i separat tracked arbeid; det følger ikke med et immutable logisk ChannelRecord som kan avvises ved faktisk overlevering. X:938–950 kan samtidig fjerne gammel kanal, og X:995–1005 tillater en ny med samme ID. BA:20 og BA:29–31 starter cid-serien på nytt for en ny BridgeBase.

**Forløp:** Hold en gammel respons etter X:1099, men før den er overlevert til fysisk transport. Lukk logisk kanal, gjenåpne samme ID, og send en ny forespørsel med samme cid. Slipp gammel send. Den felles autentiserte fysiske sessionen er fortsatt gyldig; gammelt svar bærer det gjenbrukte ID-et og kan tolkes som nytt. AEAD-counter beskytter fysisk recordrekkefølge, ikke denne manglende logiske generasjonen. WS-mux er også berørt.

X:820–823 kansellerer kanalens oppgaver. Det er et eksisterende vern, men ikke en atomisk sendesperre: G:270 sjekker kansellering ved arbeidsstart, og transportarbeid som allerede har passert den sjekken trenger ikke stoppe av seg selv. Reproduksjonen må derfor holde etter siste relevante cancellation-check og før fysisk aksept, med en transport som ikke avslutter bare fordi Task er kansellert.

**Avgrensning:** Dette krever ikke tilbakekalling av bytes som allerede var fysisk sendt før close. Hullet ligger før denne overleveringen. Det trengs en eksplisitt og etterprøvbar regel for når sendingen tilhører en kanal som ikke lenger kan gjenbrukes.

**Rettelse/test:** Bevar logisk generasjon gjennom kø og overlevering; bruk en wire-generasjon eller en sperre mot ID-gjenbruk til gammel utsending er definitivt håndtert dersom lokal fencing ikke kan gi garantien. Test holdpunkt etter objektvakten med samme fysiske transport, samme channelID/cid og frisk sibling. `BridgeChannelTransportTests.swift:408–445` holder get/set/sign-denial ved selve cellarbeidet, før objektvakten; den passerer derfor selv om dette senere vinduet finnes.

### N25 — middels — blokkerer: sen factory kan etterlate delegate og ressurser på en lukket gate

**Kilde:** G:84–87 og G:345–348 avventer factory, sjekker session og installerer delegate, men har ikke en «ta eierskap eller rydd resultatet»-overgang. Hvis session-check kaster, ryddes ikke returnert delegate. G:145 tillater dessuten `setDelegate` selv når gaten er stoppet. G:398–406 tar bare med delegaten som fantes da close startet, og senere close returnerer straks. X:1045–1047 har samme sen-factory-vindu før oppryddingen på X:1058–1064; kast på X:1046 går i catch uten å pensjonere factoryresultatet.

**Konkret ressursforløp:** Factory suspenderer. Gaten lukkes. Factory fortsetter og konfigurerer BridgeBase med gaten gjennom B:510–511. Da kan stoppet gate igjen holde delegaten, mens BridgeBase holder gaten. Session-check kaster, neste close gjør ingenting, og de sterke referansene kan bli stående. Også factory-eide abonnementer/registreringer trenger eksplisitt retirement. Et kortere vindu mellom G:85/G:346 og delegate-innsettingen kan installere resultat etter close; G:126 setter også `peerReady` uten terminalitetsvakt.

Dette er et konkret eierskaps-/oppryddingshull, ikke vist uautorisert Cell-tilgang: etterkontrollen stopper ordinær aktivering, men det beviser ikke at resultatet er ryddet.

**Rettelse/test:** Atomisk adoption under terminalitetsvakt og nøyaktig én cleanup av alle sene factoryresultater, også ved kast mellom factory og innsetting. `setDelegate`/ready må ikke gjenopplive stoppet gate. Behold relevant ressursregnskap til cleanup er ferdig. `BridgeChannelLifetimeQuotaTests.swift:102–141` tester beholdte arbeidskvoter, men factory returnerer en bar BridgeBase uten dette oppsettet eller cleanup-observatør. Utvid med ekte transportbinding og spy for abonnement/retirement/deinit; kjør både WS, peer og mux og kontroller null late delegate samt frisk sibling.

### N26 — lav — blokkerer: tidsgrensen kontrolleres ikke ved faktisk vault-signering

**Kilde:** C:51–60 validerer connectpermit før `await identityExistInVault`, men kontrollerer etter dette await bare `active`. Fristen kontrolleres først etter at `signMessageForIdentity` er kalt, C:61–65. P:101–110 har samme mønster på P:106–108.

**Forløp:** Vaultens eksistensoppslag holdes til den monotone 10-sekundersfristen er passert. Hvis timer-/cancel-arbeidet ikke allerede har endret `active`, starter en privatnøkkeloperasjon på et utløpt connectpermit. Etterkontrollen avviser det sene kanalbeviset; jeg påstår derfor ikke at et sent kanalbevis sendes, eller at dette gir fri signering av vilkårlige bytes. Feilen er at signering i det hele tatt får starte etter at det lokale tillatelsesvinduet er utløpt. Den kan testes uten tidsgjetting i C ved injisert klokke.

Et beslektet hull i den separate origin-proof-banen må tas med i samme tidskontroll: B:1512 validerer challenge-tid før awaits til containment, vault og replay store; B:1574–1579 sjekker permit/session før og etter signering, men revaliderer ikke challenge-fristen. Et aktivt feedpermit kan leve videre mens den enkelte challengen utløper. At mottakeren skal avvise en utløpt challenge, gir ikke avsenderen rett til å starte/returnere den sene signeringen. Jeg har ikke vist at mottaker aksepterer et slikt utløpt bevis.

**Rettelse/test:** Kontroller monotont vindu, wall-clock/challenge-frist, kansellering og lokal tillatelse etter suspenderbart oppslag og umiddelbart før signering, og kontroller publiseringsvilkårene etterpå. `BridgeChannelAuthenticationTests.swift:243–260` holder selve signeringen og tester at sent bevis ikke returneres; støtteklassen på :453–456 holder ikke eksistensoppslaget. Ny test må holde eksistensoppslag/replay-oppslag, flytte klokke eller avslutte tillatelsen, og kreve **null signeringskall**, ikke bare null returnert proof. Test også utløpt origin-challenge under fortsatt aktivt feedpermit.

## 4. V3 mot designet

Sammenlikningsgrunnlag er [PEER-V3-DESIGN.md](PEER-V3-DESIGN.md), lest i sin helhet. **Ingen avvik kan godkjennes som en tilsiktet implementasjonsvariant: leveransen er fortsatt v2.** Fraværet er rapportert åpent av implementøren.

| Designkrav | Faktisk på vurdert head |
|---|---|
| Eksakt v3-profil; identitetsfri M1 med rolle, fersk ephemeral/nonce/generasjon/tid | P:31–58 bruker v2 og identitet i hello. |
| Fem navngitte v3-meldinger: Hello, ResponderAuth, InitiatorAuth, ResponderFinished, InitiatorFinished | G:90–127 bruker gamle PeerHello/Challenge/Proof/Accepted. Ingen v3-state machine. |
| Lokalt frosset E; E sendes bare kryptert, heller ikke en identifiserende E-hash i klartekst | Dagens hello og endpoint/transkript går i klartekst; ingen tilsvarende v3-disclosuremekanisme. |
| Eksplisitt expected-identity eller any-proven-key-policy før relevant identitetsdisclosure | Ingen implementert v3-disclosurepolicy. Discovery-/invitasjons-UUID gir ikke denne garantien. |
| Lengdeinnrammet F, T0–T5, adskilte Khs/Kid/Kfin/Kapp og retninger | R:29–38 har v2s transkriptsalt og to retningsnøkler. Det er ikke designets v3-nøkkelplan. |
| Identitets-MAC og begge Finished-MAC-er før appnøkler avledet fra T5 | G:117–126 bruker v2s krypterte acknowledgement under recordnøkler. |
| Auth-plaintext pad 8192 bytes, Finished-plaintext pad 1024; 16 KiB envelope, M1 maks 2 KiB | Ikke implementert som v3-formater eller tester. V2s egne størrelsesgrenser er ikke ekvivalente. |
| HPC3; app-record-counter starter ved null etter Finished | R:42 er `HPC2`; G:120 bruker første record som v2-ack. |
| Terminalitet, klokke/policy og generasjon etter awaits; eksplisitt tidspunkt for sendetillatelse | Eksisterende sjekker gir delvis vern, men N10–N18 og N23–N26 viser udekkede overganger. |
| Identitetsvern med presise begrensninger for aktive deltakere | Ikke levert. Designet lover uansett ikke at en aktiv, akseptert motpart aldri lærer identiteten, eller at discovery/MC blir anonym. |

Disse fraværene telles under N22/v3-leveransen, ikke som ni ekstra funn. Et v3-løft må fortsatt rette tilstand, NI, contact og ressursgrenser; bytte av håndtrykkskrypto løser dem ikke.

## 5. Ny adversariell gjennomgang — peer og WS

| Tema fra kontroll 4 §§2–3 | Resultat på vurdert head |
|---|---|
| Hva beviset faktisk sier | Offentlig-nøkkelverifikasjon beviser kontroll over presentert signeringsnøkkel i det bundne transkriptet. Den beviser ikke fysisk nærhet, en bestemt person, eller at discovery-navn/UUID tilhører forventet B. N11/N12/N20 er fortsatt vesentlige. |
| Valg av vault og authority | A validerer offentlig descriptor; `IdentityPublicKeySignatureVerifier.swift:14–82` bruker bare offentlig nøkkel og støtter Ed25519/P-256. L:408–413 lager requester med BridgeIdentityVault. `AppleBridgeTransport.swift:173–177` og `VaporBridgeTransport.swift:288–303` velger ikke lokal signeringsmyndighet fra wire-identitet. N17 slår sammen kvoter, ikke principal eller tillatelser. |
| Challenge-binding og replay | C:33–49 kontrollerer profil/retning, eksakt endpoint, identitet, nonce, session/generasjon og signeringsbytes. P:60–70 binder begge peer-helloer/roller. L:309–335 forbruker pending før signaturverifikasjon. L:338–384 kontrollerer frister og eksakt principal ved aktivering/bruk. Ingen ny signaturforfalskning funnet i disse leste banene; N26 viser at tidspunktet for selve signeringskallet likevel trenger retting. |
| Fullt transkript og unknown-key-share | P:31–70 binder profil, endpointets initiator/responder/setupID/domain, begge identiteters UUID/algoritme/kurve/nøkkel, begge ephemeral/noncer/generasjoner/tider og signerrolle. Identitetsendring endrer også R:29–36 sitt KDF-grunnlag. Ingen konkret kryptografisk UKS funnet. MC-sertifikatet er ikke attestert av dette; N11/N12/N20 er fortsatt separate bindingstap på applikasjonsnivå. |
| DH, nøkkeldeling og record | R:25–28 bruker separat X25519 og avviser all-zero; R:29–38 binder transkript og retning; R:48–78 bruker counter-nonce, autentisert header, eksakt neste counter, størrelsesgrense og fatal feil. Dette støtter N07-lukking. Ikke en formell verifikasjon av egen AKE eller kryptobiblioteket. |
| Lavordenspunkter og nonce-gjenbruk | V:72–79 prøver X25519-input 0, 1, p−1, p og p+1; dette er ikke uttømmende backend-verifikasjon. P:82–89 oppretter fersk nonce og ephemeral. R:44–78 øker counter etter vellykket kryptografi, bruker ikke maksimumsverdien og ødelegger recordnøklene ved feil. Ingen konkret wrap-/nonce-reuse-vei funnet i den leste adapterbanen. |
| Aktivt relé og endret ephemeral | De leste testene endrer begge sider av DH-utvekslingen og injiserer legitim klartekst. Ren videresending uten nøkkelendring gir ikke reléet appnøklene. V2-identitet forblir synlig, N22. Ingen ekte treprosess-MC MITM-test kjørt her. |
| Replay/refleksjon/gammel generasjon | R krever eksakt retning/generasjon/counter og gyldig tag. G:245–247 binder dekodet peer-generasjon. Gamle fysiske Scanner-callbacks er fanget. Dette beskytter ikke allerede innsluppet arbeid etter await, eller gjenbrukt logisk mux-ID: N23/N24. |
| Nedgradering og ekstra felter | P:91–99 krever eksakt profil, motsatt rolle og 32-byte ephemeral. G:59–63/G:203–235 har fast klartekstfase og deretter recordkrav; G:325–333 avviser ekstra auth-metadata. T:496–509 prøver v1 og manglende nøkkel. Ingen v1-/ready-fallback eller usignert algoritmeforhandling funnet. V3 er samtidig helt fraværende, ikke en forhandlet oppgradering. |
| Nøkkelbekreftelse og formålsdeling | G:118–126 og P:113–117 krever lokal mottatt, autentisert record 0 med riktig session/generasjon/digest. T:512–531 holder siste bekreftelse og hindrer responder-Base. V2 bruker samme retningsnøkkel til ack og app med ulike noncer og forventet førstetype. Ingen særskilt angrepsvei funnet bare av denne grunn, men det er ikke v3s separate Finished-/appnøkler og dekkes ikke automatisk av et SIGMA-bevis. |
| Minne og efemære hemmeligheter | P:119–125 slipper privat ephemeral etter ett derive-forsøk eller cancel; R:81 og G:397–410 fjerner recordnøkler ved close. Ingen ny eksport/persistens av disse nøklene funnet. Dette er kildebelegg for referanselivsløp, ikke attestert zeroization av kopier eller OS-minne. |
| Feilorakel | R:65–78 utfører AEAD før plaintext-dispatch og gjør første recordfeil terminal. Headerfeil og tagfeil kan gi ulike lokale feil, men headeren er offentlig. Ingen konkret plaintext-/padding-orakel funnet. Ingen timingmåling eller revisjon av providerens tagkontroll er utført. N26 gir en tidsgrensefeil, ikke fri signering av angripervalgte bytes. |
| Lokal origin-proof-autorisasjon | `BridgeIdentityProofAuthorization.swift:18–105` har lokal principal/vault, scope og lease; innkommende sign-kommando kan ikke opprette lease. B:1547–1580 sjekker den lokale tillatelsen, replay-beslutning og kanalen. Connectpermit og GeneralCell-originpermit er separate. Challenge-frist rundt awaits har N26. |
| Tid, revokasjon og ny innlogging | L:338–384 bruker monoton frist og veggklokke; P har eget 10-sekundersvindu. L:415–425 stanser gjeldende session. Dette er ikke et varig sperreregister for nøkkelen. Scanner oppgir ingen egen `recheckPolicy` på S:661–672; permanent sperring og ny lokal brukeraksept må komme fra uttrykkelig vertspolicy. N17s kvotesamling innfører ingen slik autorisasjonspolicy. |
| Parser/feil før dispatch | G:249–258 velger mindre handshake-grense og krever kanonisk auth-envelope; G:325–333 avviser ekstra auth-headerfelt. Apple/Vapor validerer payload før decode/dispatch. N14/N16 viser at disse kontrollene ikke dekker alle MC-innganger eller discovery-allokering. |
| Store rammer og total DoS-grense | Dagens 16 KiB auth-grense, 1 MiB plaintext pluss 65 bytes record, lokal receive-grense på 64/4 MiB og gatekvoter er reelle delgrenser. V:82–105 og T:399–407/T:589–602 tester relevante grenser. N13–N18 viser hvorfor de ikke gir et samlet tak på arbeid, minne eller transportressurser. |
| Lukking og ressurser | Beholdt arbeid/transportkvote er bedre enn bare å slette tabellinnslag. Det bevarer ikke EntityScanner-arbeid, fysisk MC-peer, OS-sendekø eller et sent factoryresultat automatisk: N13/N15/N18/N25. |
| TLS og WS-profil | WS forutsetter TLS-serverautentisering i tillegg til klientens nøkkelbevis. Peer-v2-record er en annen profil, ikke en erstatning for TLS. `CellResolver.swift:2247–2258,2293–2338` pakker både dedikert og pooled WS i BridgeChannelTransport. Endpoint/domain og development-only loopback-valg sendes eksplisitt til gaten. Ingen deployet TLS-konfigurasjon er inspisert. |
| WS-oppkobling og fysisk close | `VaporBridgeTransport.swift:119–171` har generasjonsbundet waiter, 10 s timeout, ramme-/akkumuleringsgrenser og avvisning av sen upgrade. :194–213 avvikler utgående loop og bruker eventuell verts-eid hard-close. Inngående verter må faktisk levere hard-close. W:251–260 kansellerer URLSession-task/session. Vertsinnkobling i CellScaffold/Binding er ikke lest på nytt. |
| WS/mux etter autentisering | Felles principal-check og gate gjelder fortsatt. N17/N19-regresjonstestene inkluderer WS-baner, men N23–N26 og Apple-delen av N18 står igjen. Den offentlige vertsens policy og caps kan ikke utledes av at pakken er grønn i CI. |
| Diagnostikk/disclosure | N19s konkrete diagnostikkfeil er rettet. N21s motstridende driftsbeskrivelse og N22s synlige identiteter består. Ikke grunnlag for en generell påstand om payloadfrie logger eller anonymitet. |

Kryptovurderingen er sammenholdt med primærkilder: [RFC 7748 §6.1](https://www.rfc-editor.org/rfc/rfc7748#section-6.1) om X25519/all-zero og binding av begge offentlige DH-nøkler, og [RFC 5869 §3.2](https://www.rfc-editor.org/rfc/rfc5869#section-3.2) om kontekstseparasjon i HKDF. Disse underbygger de konkrete kontrollene, ikke en sikkerhetsgaranti for hele HAVEN-protokollen. MC-API-utsagn er kontrollert mot Apple-lenkene ved N14/N15/N18.

## 6. CI og lokale bevis — hva som faktisk er kjørt

Jeg har **ikke kjørt nye Swift-bygg, Swift-tester, TSAN, MC-prosesser eller iOS/NI-tester** i denne kontrollen. Jeg har lest implementørens rålogger og resultatfiler, sammenholdt kilde/tester på SHA, og kontrollert PR-/Actions-status via GitHub. macOS-jobbens rålogg er også hentet direkte fra GitHub og bekrefter checkout, fullsuite, de nye testsuitene og tre TSAN-runder. Grønn CI er dermed verifisert status, ikke et påstått nytt lokalt testløp fra Astra.

### GitHub Actions

Fem checks var SUCCESS for head `605298fe…`, alle gjennomgåtte runs attempt 1:

| Kjøring | Resultat og dekning |
|---|---|
| [Security regression macOS 36434960586](https://github.com/Digipomps/CellProtocol/actions/runs/36434960586) | Full suite: **1432 tester, 5 skipped, 0 feil**, 38.028 s testtid / 38.292 s samlet. Inkluderer ScannerPeer 26, record 4, kanonisk kvote 4 og diagnostikk 4. |
| [Swift Linux 36434960564](https://github.com/Digipomps/CellProtocol/actions/runs/36434960564) | **106 tester, 0 feil** i valgt Linux-suite. Ingen Apple MC/NI-kjøring. |
| [Vapor identity vault Linux 36434960710](https://github.com/Digipomps/CellProtocol/actions/runs/36434960710) | **25 tester, 0 feil**. |
| [Runtime capacity macOS 36434960633](https://github.com/Digipomps/CellProtocol/actions/runs/36434960633) | SUCCESS. Generell kapasitetsjobb, ikke måling av angripers MC/NI-/OS-køene i funnene over. |
| [Notify PyCellProtocol 36434956850](https://github.com/Digipomps/CellProtocol/actions/runs/36434956850) | SUCCESS. `pull_request_target`-notifikasjon; ikke runtime-sikkerhetsbevis. Ingen melding sendt av denne kontrollen. |

macOS-jobben verifiserer pinned dependencies og at en sårbar downstream transportpin avvises. Den forventede dependency-resolution-feilen for gammel `swift-nio-ssl` er altså en positiv negativtest, ikke en skjult rød fullsuite.

**CI kjørte syntetisk PR-merge `0d5b4c985c0ceae099d3cbd6a37b9dba0b459c25`**, med foreldre main `81601a6f835252aba7e99d43786fb5d67227c245` og vurdert head. Jeg har kontrollert diffen: avvik fra head er Linux-workflowen og fire Vault-retention-filer (`Docs/Vault-Idea-Retention.md`, `VaultCell.swift`, `VaultIdeaRetention.swift`, `VaultIdeaRetentionTests.swift`). De vurderte brofilene og brotestene er identiske. Det forklarer også fem ekstra Vault-tester mot lokal fullsuite. CI-totalen skal ikke merkes som fullsuite på et helt identisk head-tre.

### TSAN

`.github/workflows/security-regression-macos.yml:33–46` kjører **bare `BridgeDescriptionConcurrencyTests`**, tre repetisjoner. Råloggen viser 2 tester/0 feil i hver repetisjon, med `TSAN_OPTIONS=halt_on_error=1`. Ingen rapportert TSAN-feil i disse kjøringene.

Det er **ikke** en peer-, Scanner-, EntityScanner-, invitasjons-, NI- eller generell mux-TSAN-kjøring. Spesielt N10–N13/N23–N25 er ikke friskmeldt av disse seks testutførelsene. Ingen ekstra TSAN kjørt lokalt av Astra.

### Lokale resultater fra N17/N19-leveransen

Råbevis er lest under `/private/tmp/cp53-n17-n19-evidence/`:

| Bevis | Resultat og begrensning |
|---|---|
| `final-local-results.json`, `final-build.log` | Build exit 0, «Build complete!» etter 2.88 s. |
| `final-test.log` | CellBase: **1398 tester, 12 skipped, 3 unexpected failures**. HavenCommons 26/0, CellNearby 3/0; totalt 1427 tester. Fulltest exit 1. Dette er ikke lokal grønn fullsuite. |
| De tre lokale feilene | `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns`, `testLegacyEmbeddedPrivateKeyStillSigns`: NSOSStatus 100001 / CDSA EPERM ved `IdentityVault.swift:1374`; `testScopedSecretDataStaysStableInUnsignedTestHost`: −25291 ved :780. De samme testene passerte macOS-CI. Miljøforskjell er forklaringen rapporten peker på, ikke en ny utført lokal avkrefting. |
| `focused.log` | **33 tester, 0 feil**: 4 quota, 4 diagnostikk, 11 Apple-adapter, 14 Vapor-adapter. |
| `original-regression-result.json`, `original-regression.log` | Exit 1. Med gammel session/BridgeBase innbyttet: 8 tester, **214 assertion failures**, 0 unexpected. Kvotetester 198, diagnostikk 16. Den nye canonical-helper-testen passerer; tre kvoteatferdstester feiler. Dette er målrettet mutasjon, ikke komplett kjøring på urørt gammel head. |
| `ci-fixture-regression.log` | Lifetime quota-suite **8 tester, 0 feil** etter fiksturretting. Fiksturen håndterer at ordinær BridgeCommand-JSON ikke har fast objektnøkkelrekkefølge; den endrer ikke wirekontrakten. |

For etterprøving: SHA-256 for lest `final-build.log` er `d8ef219d34a242b8826dd28c79492a32f6892350a351646f9feaf9df13cd094e`; for `final-test.log` er den `3e54a0b6c75dd326fdf1b0863c9b9d7e7104ca271c9b318fb9b2c785186d4e16`. Bevisene er midlertidige lokale filer, ikke en påstand om permanent arkivering i denne kontrollen.

### Faktisk toprosess-Multipeer

M:11–14 gjør testen opt-in; ordinær grønn suite betyr ikke at denne ble kjørt. M:47–104 bruker to virkelige prosesser med MCSession, en lokal testvault, GeneralCell og Lobby. Den bruker ikke EntityScanners kontakt-/NI-forløp.

Siste faktiske toprosessbevis er fra **kontroll 4-head `1b8efe1c…`**, ikke fra `605298fe…`. Følgende bevarte worker-logger og `.passed`-markører er lest på nytt under `/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/`:

| Kjøringsmappe | Verifisert innhold |
|---|---|
| `cp53-multipeer-5D215FBD-7E0C-4BB3-9286-348D1E3DAF32` | Inviter A: begge workers 1 test/0 feil, ca. 4.363 s; authenticated, description, attach, feed. A sealedSent/Received 46/27, B 27/46. |
| `cp53-multipeer-670ECDE4-3964-4213-89A7-421FC337414C` | Inviter B: begge workers 1 test/0 feil, ca. 4.366 s; samme milepæler. A 27/46, B 46/27. |

At MC-kildefilene er uendret gjør historikken relevant, men gjør den ikke til en ny kjøring av siste head med de nye felles kvoteendringene. Ingen ny toprosess-test er levert av de STOPPET-arbeidene. Ingen faktisk treprosess-MITM, uvennlig resource/stream-peer eller langsom MC-mottaker er kjørt i kontroll 5.

### iOS, NI og produksjonsvert

**iOS-bygg: ikke kjørt/verifisert på vurdert head. NI på to enheter: ikke kjørt.** Ingen levert NI-operatørkjøring, fysisk B/C-assosiasjonstest eller sen NI-callback-test. macOS har ikke kompilert og kjørt alle `#if os(iOS)`-grener for oss. Ingen gjennomgått Actions-jobb er et iOS-bygg.

Ingen ny deploy eller funksjonell produksjonsgjennomgang er gjort. Binding/CellScaffold-inngress, hard-close-innkobling, TLS-terminering, lokale disclosurevalg, produkttilgang og sluttbrukerflyt er ikke lest/verifisert på nytt her. Tidligere N05 om downstream-inngress kan derfor ikke erklæres lukket gjennom denne CellProtocol-kontrollen; det ligger utenfor tellingen N07–N26 som bestilt.

## 7. Mergekrav og lesegrenser

**Anbefaling: ikke merge.** Forutsetningen om at alle rettinger etter kontroll 4 er levert er ikke oppfylt. Det kreves retting av de 15 listede funnene, faktisk v3-leveranse, avstemt driftsdokumentasjon og målrettede bevis som treffer feilforløpene. Ny grønn fullsuite alene lukker ikke dem. En senere kontroll må ta utgangspunkt i ny levert SHA og skille kode, test, faktisk MC og iOS/NI like strengt.

Lest på vurdert SHA: hele A/P/R/C/L/G, hele ScannerService, BridgeBaseAuditor, BridgeIdentityProofAuthorization, offentlig signaturverifikator og IdentitySigningChallenge; hele de oppførte Scanner/record/invitasjons-/MC-/canonical-/diagnostikk-testfilene. AppleBridgeTransport er lest i sin helhet; Vapor-adapterens oppkobling, send, close, callbacks og identity-vault-vei er lest. Hele endringslisten fra kontroll 4 er sammenholdt med disse banene og implementørens tester.

Delvis lest med konkrete utsnitt: BridgeBase-konfigurasjon/renewal, authority, sign/get/set/feed, responsbehandling og cleanup; mux-serverens admission/dispatch/send/close og streamsekvenser; EntityScanner-tilstand, callback-dispatch, probe, kontaktverifikasjon og persistens; WebSocketConnection2s oppkobling/mottak/send/close/ping; resolverens dedikerte/pooled WS-oppsett. Testene for transport, lifetime og channel-auth er særlig lest ved holdpunktene som vurderes ovenfor. Resterende linjer i disse store filene er **ikke lest på nytt i sin helhet** i kontroll 5. Jeg har ikke utledet dekning av dem bare fra grep-treff.

**Ikke lest:** hele øvrige CellProtocol-repositoriet, kryptoleverandørenes implementasjonsinterner, alle tester i fullsuite, alle CI-kompileringslinjer, downstream-repoenes gjeldende kode, deployet miljø og fysiske enheters tilstand. Bokkapitler brukt som bakgrunn er lest som utsnitt, ikke komplett ny revisjon. Vurderingen er derfor en kildebasert sikkerhetskontroll med oppgitte grenser, ikke et bevis for fravær av alle mulige sårbarheter.

Læringsfangst for videre arbeid: (1) en test må holde ved riktig await/overlevering, ikke bare tidligere i samme operasjon; (2) kvotenøkkel må kanoniseres separat fra autorisasjonsprincipal; (3) fullsuite/TSAN/ekte MC har forskjellige og eksplisitte bevisgrenser. Disse er bevart her. Ingen læringsledger, skill eller synk er endret, fordi denne oppgaven uttrykkelig autoriserer én rapportfil og ingen andre filendringer.
