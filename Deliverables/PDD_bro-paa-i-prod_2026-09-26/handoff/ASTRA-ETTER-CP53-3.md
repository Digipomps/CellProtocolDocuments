STATUS: LEVERT — anbefaling: merge etter 3 rettinger, 3 nye funn (3 blokkerer)

Astra, kontroll 3 av CellProtocol PR #53. Dato: 2026-09-28. Beslutningseier: Kjetil.

**Ikke merge foreliggende head. N06 er lukket, og rebasen er korrekt. R3 gjenoppretter et reelt, testet Scanner/Lobby-løp gjennom den felles porten, men peer-grensen er ikke sikker nok:** signaturene er ikke bundet kryptografisk til MCSession, discovery kan omdirigere en allerede autentisert kanal, og iOS har fortsatt en utsending utenom porten. Dette er N07–N09 nedenfor. Funnantallet gjelder denne kontrollen; tidligere konsumentblokk N05 og produksjonsportene telles ikke på nytt.

**Vurdert revisjon og lesegrense.** `CP53-REBASE.md` er LEVERT, og jeg har brukt dens head **`101e5452ed7aecbbf947ed1205c3941ec24782a8`**, ikke fallbacken. Base/main er **`9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366`**. Begge ble bekreftet med GitHub API; [PR #53](https://github.com/Digipomps/CellProtocol/pull/53) var OPEN, `mergedAt=null`, `MERGEABLE/CLEAN`. Kodehenvisninger gjelder commitobjektet, lest med `git show`/`git diff`, ikke det skitne CP-hovedarbeidstreet.

| Prefiks | Bane relativt til HAVEN; revisjon |
|---|---|
| `B/` | `CellProtocol/Sources/CellBase/Cells/Bridging/`, vurdert head |
| `S` | `CellProtocol/Sources/CellApple/EntityRadar/ScannerService.swift`, vurdert head |
| `T/` | `CellProtocol/Tests/CellBaseTests/`, vurdert head |
| `CP/` | `CellProtocol/`, vurdert head |
| `H/` | `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/`, lokale rapporter |
| `G/` | `CellProtocolDocuments/Deliverables/Bro_Gjenoppretting_2026-09-15/`, lokale historiske dokumenter |
| `OLD-CS/` | `CellScaffold/`, historisk commit `ec4375010297741aa1a794b3d9dfaa7af37a08b7`; uttrykkelig ikke dagens main |
| `HD/` | `HAVEN-Deploy/_handoff/HD-0040/`, historiske dokumenter fra 16.09 |

Lest: begge tidligere Astra-rapporter, `CP53-R3.md`, `CP53-REBASE.md`, hele den nye peer-profilen, felles auth/session/transport/client-operation, R3-diffen, Scanner-utsnittene henvist nedenfor, de to nye Scanner-testfilene, invitation-testene og N06-regresjonene. Base, mux og resolver er lest i relevante utsnitt/differ; øvrige deler er **ikke lest på nytt**. Historisk grunnlag: hele Binding-forensikken fra 02.09, `G/RAPPORT.md:1–230`, begge PR-utkastene, hele `bro-cp.patch`, den opprinnelige `VaporCellBridge` i relevante utsnitt og den gjenopprettede varianten på `OLD-CS`, samt rapportene og evidensnotatene i HD-0040. Det enorme råloggvedlegget i `G/RAPPORT.md` er **ikke lest i sin helhet**. Relevante bokkapitler, CPs SECURITY og Apples primærdokumentasjon er også lest.

Dette er kildevurdering og kontroll av eksisterende testbevis. **Jeg har ikke kjørt bygg, CP-tester, MITM-angrep, radioprøve eller staging/prod i denne kontrollen.** Nye feilforløp er kildebaserte slutninger, ikke påståtte utførte utnyttelser. Testlogger og GitHub-resultater er kontrollert som angitt nedenfor. Ingen ekte private nøkler er inspisert.

**1. N06 er lukket, og regresjonen ville fanget den gamle feilen.**

`B/BridgeChannelSession.swift:426–441` starter leasen med `released = true`; først etter at `session.acquire` har returnert, settes den til `false` (`:433–435`). Throwing-init/deinit kan derfor ikke trekke fra en reservasjon som aldri ble oppnådd. Den låste, idempotente release beholder vernet mot dobbelt fratrekk.

`T/BridgeChannelLifetimeQuotaTests.swift:41–67` holder en første lease på **samme sesjon**, prøver fem avslag, og tillater først nytt opptak etter faktisk release. Begge ressurser, feed/channel, prøves mot både per-key- og globalgrense. Dobbel release og close med beholdt eier inngår. Med gammel `released=false` ville første avslag dekrementert eierens teller, og neste `XCTAssertThrowsError` ved `:52` ville feilet. Dette er nettopp den tidligere manglende situasjonen.

Mux-prøven ved `:70–99` går gjennom faktisk auth-gate og `BridgeMultiplexServerSession`: én aktiv kanal, fem avslag uten ekstra factory, deretter close og én ny godkjent åpning. Gammel feil ville gitt `channelOpened` i avslagssløyfen og flere factory-kall (`:90–91`). Produksjonsbruken av lease ligger i `B/BridgeMultiplexing.swift:1038–1055`.

Implementørens før-logg `/private/tmp/cp53-n06-before.log:174–221` er lest: de to navngitte testene gir **38 assertion failures**, blant annet nettopp uventet `channelOpened` og manglende throw. Etter-loggen gir **7 tester / 0 feil**. Jeg har ikke gjentatt mutasjonskjøringen selv; kildeforløpet forklarer den, og begge regresjonene har eksplisitte passed-linjer i nettloggen på vurdert head. N06 og den tilhørende R2-regnskapsfeilen kan lukkes.

**2. Peer-profilen gjenbruker hovedmekanismen, men mangler tre nødvendige vern.**

Den beskyttede ressursen er kanalen inn til Base/resolver og senere cellekommandoer, svar og flows. Peer-beviset skal fastslå nøkkelkontroll for den bestemte forbindelsen; Agreement, grants, formål og cellens eiergodkjenning avgjør fortsatt hvilke operasjoner som tillates. En angriper må kunne være en nærliggende, allerede invitert eller senere ondsinnet peer, kontrollere discovery/context/egne meldinger, videresende et håndtrykk og forsøke gamle meldinger etter reconnect. Vi forutsetter ikke brutt signaturkryptografi eller stjålet lokal privat nøkkel.

| Trussel/egenskap | Vurdering på head |
|---|---|
| Falsk nøkkel / kopiert offentlig descriptor | En nullsignatur eller offentlig kopi uten signer gir ikke bevis. `B/BridgePeerChannelAuthentication.swift:86–105`, `B/BridgeChannelSession.swift:307–331`; negative prøver `T/ScannerPeerAuthenticationTests.swift:46–64,233–250`. Egne gyldige nøkler beviser egen nøkkelkontroll, ikke at discovery-navnet tilhører en bestemt person/enhet. Den sterkere falsk-peer-varianten står i N07/N08. |
| Replay av auth-bevis | Begge helloer binder noncer, roller, offentlige identiteter, setup-ID og generasjoner. Verifierens pending forbrukes før signaturkontroll; bare én state-overgang kan vinne. `B/BridgePeerChannelAuthentication.swift:30–68`; `B/BridgeChannelSession.swift:256–265,307–331`. Gamle proof og ferskt handshake med samme MCPeerID-objekter prøves ved `T/ScannerPeerAuthenticationTests.swift:46–64,85–120`. Dette beviser ikke vern for gamle vanlige dataframes; se N08. |
| Rolleforveksling/refleksjon | Motsatt rolle kreves i `prepare`, signerrollen inngår i transcript, og transporten tillater fire bestemte rolle/melding-kombinasjoner. `B/BridgePeerChannelAuthentication.swift:39–68,86–94`; `B/BridgeChannelTransport.swift:83–113`. Endret rolle/profil/endpoint avvises i testen ved `T/ScannerPeerAuthenticationTests.swift:67–82`. |
| Domeneadskillelse fra WS | **Ja.** Peer bruker `org.haven.bridge-peer-channel.v1`, `openPeerBridgeChannel` og audience-hash av peer-endpoint; WS bruker `org.haven.bridge-channel.v1`, `openBridgeChannel` og kanonisk origin/rute. Ressurshashen dekker det respektive transcriptet. `B/BridgePeerChannelAuthentication.swift:9,28,58–68`; `B/BridgeChannelAuthentication.swift:9–10,64–97,175–186`. Peer-strenger går til egen rolle-dispatch, ikke WS-dispatch. Ingen falsk WSS-origin. |
| MITM mellom to krypterte MC-forbindelser | **Ikke lukket. N07.** Gyldige signaturer kan videresendes fordi de ikke binder MC-kanalens kryptografiske endepunkter. |
| Reconnect med samme peer-ID | Gamle **transportobjekters** send/close er gjerdet med lokal setup-ID (`S:389–399`), og registreringsopprydding avventes (`:622–630,755–775`). Testene viser dette og ferskt proof. Inngående callbacks og mutable discovery-ruter har ikke samme binding; N08. Reell MC-reconnect/utløp er ikke bevist av toprosesstesten. |
| Lokal-vault-proveniens | **Rettet i den leste Scanner-veien.** Wire-identitet får alltid `BridgeIdentityVault`, også før Base; ingen default-vault-fallback (`S:1108–1113,1154–1156`). Lokal `Operation` beholder bare eksplisitt lokal owners vault og avviser proxy-vault (`B/BridgePeerChannelAuthentication.swift:80–105`). Base-signering krever fortsatt aktivt, avgrenset permit (`B/BridgeBase.swift:1547–1579`). |
| Funksjon og celleautorisasjon | Den positive testen gjør faktisk description, admit, GeneralCell.attach og feed (`T/ScannerPeerAuthenticationTests.swift:149–182`). En egen test får avslag fra Lobby etter vellykket peer-proof (`:185–204`). Det viser at transportbevis ikke automatisk gir eierens tillatelse. Testvertsgrants er eksplisitte; de er ikke standard produksjonspolicy. |

**Det er én felles autoritativ sesjonsmaskin.** Peer-profilen normaliseres til `BridgeChannelSession.Pending`, bruker samme `reserveOpen`, `recheckBeforeActivation`, `activate`, expiry/revoke og kvoter (`B/BridgeChannelSession.swift:213–265,307–355,374–421`). `BridgeChannelTransport` gjenbruker trackedWork, sendregnskap, dispatch og close (`:184–239,282–323`). Base opprettes i gate-factory etter proof; setup/lookup/registrering følger `startPeer` (`S:591–620,671–721`).

Presiseringen er at peer-håndtrykket likevel har **egen nødvendig protokollprogresjon**: `Operation.active/outgoing/signingStarted`, rolle-dispatch og `peerReady` (`B/BridgePeerChannelAuthentication.swift:73–114`; `B/BridgeChannelTransport.swift:22–23,60–113`). «Ingen parallell state-maskin» er riktig om admission/ressurslivsløpet, ikke bokstavelig «ingen ekstra state». `peerReady` venter på ferdig factory/ack; å erstatte det mekanisk med `session.state == authenticated` ville slippe setup frem for tidlig, siden aktivering skjer før awaited factory.

Den vurderte WS-protokollen trenger bare offentlig identitet/signatur på mottakersiden. Peer-signering skjer på hver enhets egen lokale vault; ingen ny kode sender en privat nøkkel til en skyvert. Dette er et positivt, avgrenset proveniensfunn, **ikke** en attest på all nøkkellagring i skyinstallasjonen eller uleste konsumenter.

**N07 — Høy, blokkerer: peer-proof autentiserer ikke den krypterte MCSession-kanalen.**

`S:324` oppretter MCSession med `securityIdentity: nil` og `.required`. Ingen sertifikatverifikasjon finnes i den leste MCSessionDelegate-implementasjonen (`S:995–1106`). Apple skiller eksplisitt mellom autentisering og kryptering i [MCSession-initialiseringen](https://developer.apple.com/documentation/multipeerconnectivity/mcsession/init%28peer%3Asecurityidentity%3Aencryptionpreference%3A%29); uten implementert [sertifikatcallback](https://developer.apple.com/documentation/multipeerconnectivity/mcsessiondelegate/session%28_%3Adidreceivecertificate%3Afrompeer%3Acertificatehandler%3A%29) validerer ikke rammeverket peerens sertifikat på appens vegne.

Peer-transcriptet har ingen sertifikat-/kanalbinding og ingen autentisert nøkkelutveksling som beskytter senere bytes (`B/BridgePeerChannelAuthentication.swift:14–68`). Det binder appens discovery-strenger. Disse kommer fra peerens `info["uuid"]`, ikke fra verifisert MC-kryptografi (`S:930–942`). Etter handshake sendes vanlige BridgeCommand-JSON direkte gjennom MCSession; gate sjekker sesjonsstatus og offentlig identitet, men ingen perframe-MAC/signatur fra den beviste nøkkelen (`S:389–410,1146–1167`; `B/BridgeChannelTransport.swift:214–238,282–295`; `B/BridgeCommand.swift:55–85`).

Konkret angrepsforløp: M er kryptert transportmotpart for A og B og annonserer de forventede discovery-ID-ene på hver side. Invitasjonen blir akseptert. M videresender samme endpoint, hello, responder-proof, initiator-proof og ack uendret mellom A og B. Alle signaturer og noncer er ekte; ingen kryptografi brytes. A og B beviser sine nøkler til hverandre, men **M terminerer begge MC-forbindelsene**. M kan deretter lese og endre vanlige svar/flows og presentere den allerede beviste offentlige command-identiteten. Cellens grants og snevre origin-proof begrenser enkelte cellehandlinger, men autentiserer ikke alle transportbytes eller svarpayloads; eksempelvis leveres feed-payload etter cid-oppslag i `B/BridgeBase.swift:1811–1818,1875–1880`.

Dette er mer enn den dokumenterte avgrensningen «ikke attestert person/enhet». Selv med riktig forventet offentlig nøkkel mangler bindingen mellom **den nøkkelen og forbindelsen som bærer kommandoene**. To ærlige prosesser og testen med endret hello-felt fanger ikke en videresender som lar alle signerte felt være uendret.

Nødvendig retting: bind peer-beviset til autentiserte kryptografiske transportendepunkter som faktisk verifiseres, eller bruk en etablert autentisert ende-til-ende-kanal som beskytter alle etterfølgende frames. Bare en ekstra UUID, forventet hello-nøkkel eller usignert «channel binding»-streng løser ikke dette. Behold den eksisterende gaten og celleautorisasjonen. Regresjon må ha A–M–B med to terminerte krypterte forbindelser, videresende ekte proof og forsøke payload-endring; M må ikke kunne få en brukbar kanal eller endre/lese beskyttede frames. Ingen privat brukernøkkel skal flyttes til mellomleddet som løsning.

**N08 — Høy, blokkerer: autentisert transport er bundet til en muterbar discovery-rute, og inbound-callbacks mangler generasjonsbinding.**

`ScannerPeerTransport` lagrer `remoteUUID` og lokal `setupID`, men ikke den opprinnelige MCPeerID/MCSession-bindingen (`S:65–78`). Et nytt `foundPeer` overskriver `_foundPeersDict[remoteUUID]` og legger til motsatt mapping uten å beskytte en allerede autentisert rute (`S:933–946`). `prepareBridge` returnerer deretter eksisterende transport for UUID-en etter å ha sjekket **de oppdaterte** tabellene (`:591–595`). Send slår opp mottaker fra samme mutable tabell (`:389–410`); receive velger gate fra den (`:1146–1152`). Setup-ID-vakten beskytter ikke mot dette, fordi transportobjektet aldri ble erstattet.

Konkret forløp: A har en autentisert kanal til B. En annen MC-tilkoblet peer C annonserer B sin discovery-UUID; callbacken setter `found[B]=C` og `reverse[C]=B`. Et vanlig svar fra C velger nå **B sin autentiserte gate**. En response uten identity er lovlig, og en kommando med Bs offentlige descriptor passerer principal-sammenligningen (`B/BridgeChannelSession.swift:274–281,374–380`). Utgående bytes for B sendes også til C hvis C er MC-tilkoblet. C trenger ikke Bs private nøkkel eller et nytt B-proof. Forløpet forutsetter at C kan sende på en MC-forbindelse, eksempelvis etter en tidligere legitim invitasjon; dette er ikke påstått som et angrep fra en vilkårlig, utilkoblet radiolytter. Allerede tilkoblet peer må likevel ikke kunne overta en annens autentiserte kanal gjennom discovery-metadata.

Samme manglende binding har en reconnect-variant: `didReceive` oppretter en ubundet `Task` og velger transporten først senere (`S:1076–1090`). Bytes mottatt under gammel generasjon kan derfor behandles etter at samme peer-ID har fått en ny gate. Vanlige frames har ingen obligatorisk generasjon (`B/BridgeCommand.swift:55–85`); en gammel response med gjenbrukt cid kan treffe ny ventende operasjon (`B/BridgeBase.swift:1811–1818`). Det ytre catch-oppryddingsløpet velger også nåværende remote og kaller `removeBridge` uten gammel setup-ID. Forsinket `.notConnected`-behandling er tilsvarende rutebasert (`S:1002–1018`).

Dette er ikke de feilforløpene reconnect-testene dekker: `T/ScannerPeerAuthenticationTests.swift:85–120` kaller gamle transporters send/close og leverer et gammelt **auth-proof**. De holder ingen allerede mottatt vanlig frame eller fysisk callback gjennom gjenopprettingen, og bruker ingen tredje peer/UUID-kollisjon.

Nødvendig retting: en autentisert kanal må eie en uforanderlig fysisk peer-/forbindelsesbinding; discovery må ikke omdirigere den. Avvis kollisjoner eller krev ny autentisering før en ny fysisk peer overtar. Fang riktig transport/generasjon før async dispatch, og la sen feil/opprydding bare ramme den generasjonen. Ved reautentisering på samme fysiske kanal må også gamle frames kunne skilles fra nye. Test kolliderende discovery etter autentisering, tredje tilkoblet peer, gammel vanlig command/response over reconnect med cid-kollisjon, og sen feil/close mens ny kanal og søsken fortsatt virker.

**N09 — Middels, blokkerer R3-leveransen: iOS sender fortsatt NI-token utenom peer-porten.**

`S:786–803` bygger en `response` med discovery-token og `owner.uuid`, og sender den direkte med `mcSession.send(... toPeers: mcSession.connectedPeers ...)`. Den bruker verken den autentiserte gaten, per-peer-utvalg eller dens sendkvoter. `startup()` kalles etter ett vellykket peer-oppsett (`S:1042–1044`) og kaller denne funksjonen (`:843–858`), men det beviser ikke at **alle** MC-tilkoblede peers har fullført proof eller fortsatt har gyldig kanal.

Med A ferdig autentisert og C fortsatt pending/mislykket/revoked kan C dermed få samme token/UUID. En ærlig pending mottaker kan dessuten avvise den vanlige response-rammen før auth og miste oppsettet (`S:1154–1169`; `B/BridgeChannelTransport.swift:173–179`). Dette er ikke eksport av privat nøkkel, men det bryter den nye «data først etter autentisert kanal»-grensen. Den gamle rå utsendelsen ble stående mens `sendScannerFlowElement` faktisk ble migrert til gaten (`S:381–386`).

Nødvendig retting: send også NI-token gjennom riktig autentisert per-peer-transport og eksisterende ressurs-/livsløpsvern. En annen peer som er pending, utløpt eller tilbakekalt skal ikke motta data eller få sin handshake avbrutt. Test blandingen av én aktiv og én pending/revoked peer. Denne koden er `#if os(iOS)`; den beståtte macOS-prosesstesten kan ikke dekke den.

**3. Avviksmålingen stemmer, men netto linjer er ikke et mål på sikkerhet eller kompatibilitet.**

Jeg gjentok `git diff --numstat` på commitobjektene. Rebaset N06-head `fe8957e` → vurdert head gir Scanner **+238/−183**, Bridging **+276/−24**: Base +8/−7, Session +65/−12, Transport +87/−5, PeerAuthentication +116/−0. Hele PR-en mot ny main gir Bridging **+1565/−106**; main flyttet ikke disse filene, så dette er også tallet mot gammel base. R3-tabellen er korrekt. Scanner netto +55 skjuler likevel 421 berørte linjer og endringer i både invitasjon, setup, dispatch og teardown. Hele PR-en er **39 filer, +5287/−597**, inkludert tester/dokumentasjon, med 27 berørte linjer i resolver; det er en betydelig større kontraktsendring enn septemberpatchen.

Vurdering av hver nye produksjonstype i implementørens R3-tabell:

| Type | Min vurdering |
|---|---|
| `BridgePeerChannelAuthentication` | Berettiget separat profil/navnerom. WSs origin-modell skal ikke strekkes til falsk WSS. N07 krever likevel mer enn navnerommet. `B/BridgePeerChannelAuthentication.swift:7–9`. |
| `.Role` | Berettiget og liten; signer-/verifier-retning må være eksplisitt. `:10–12,39–44`. |
| `.Endpoint` | Berettiget scope-type, men den inneholder **discovery-strenger**, ikke autentiserte fysiske peer-ID-er. Begrunnelsen må presiseres, og N07/N08 må lukkes. `:14–28`. |
| `.Hello` | Berettiget: begge sider trenger egen identitet/nonce/generasjon/rolle/tid. `:30–38`. |
| `.Transcript` | Berettiget signert sammenbinding av begge helloer og signerrolle. Ingen ny kryptografisk primitiv. `:39–46`. |
| `.Challenge` | Rimelig intern, uforanderlig samling av transcript og signingData. Den sendes ikke som egen peer-wiremelding; offentlig `Codable`-API er mer enn dagens bruk trenger. Jeg ville begrenset synligheten, ikke fjernet den nødvendige sammenbindingen. `:47–53,58–68`. |
| `.Offer` | Berettiget wirepakke for responderens hello + proof. Den eksisterende WS Challenge uttrykker ikke dette. `:54–57`; `B/BridgeChannelTransport.swift:87–97`. |
| `.Operation` | Berettiget lokal engangsautorisasjon med rolle-/scopevalidering. En viss signer-/deadline-duplisering med WS finnes, men en stor generisk auth-abstraksjon er ikke en nødvendig forbedring nå. Behold profilspesifikk validering. `B/BridgePeerChannelAuthentication.swift:73–114`. |
| `BridgeChannelSession.Pending` | God gjenbruk: én intern verifikasjonsrepresentasjon for begge profiler, fremfor egen peer-sesjonsmaskin. `B/BridgeChannelSession.swift:216–223,256–265,289–331`. |

Vurdering av hver ny testtype: `ScannerPeerAuthenticationTests` er nødvendig for Scanner-grensen; `ScannerPair` for to reelle Scanner-objekter; `ScannerControlledWire` for styrt levering; `.Frame` er en liten, rimelig retningsbærer; `ScannerStatusObserver` måler faktisk konsumentfeil; `ScannerObservedLobby` beholder ekte Lobby og gjør abonnement/suspensjon synlig; `ScannerWorkBarrier` trengs for ikke-samarbeidende arbeid; `ScannerMultipeerProcessTests` trengs for den virkelige OS-adapteren; `MultipeerProcessObserver` er rimelig for discovery/invitasjon i to prosesser. Ingen av disse bør fjernes for å få ned linjetallet. Kilder: `T/ScannerPeerAuthenticationTests.swift:8,254–362`; `T/ScannerMultipeerProcessTests.swift:10–119`. Utvid særlig wiren til tre parter og holdte callbacks; dagens to-partsmodell utelater N07/N08.

**Det jeg ville fjernet eller forenklet:** den rå NI-utsendelsen (N09); routing av etablerte kanaler gjennom discovery-tabellen (N08); og overflødig Scanner-state. `bridgeDelegatesByRemoteUUID` blir nå skrevet/ryddet og telt, mens dispatch bruker `physical.gate`/`physical.bridge` (`S:259,492,740–751,1146–1167`). Den er kandidat for fjerning med tilpasset testobservasjon. `invitedRemoteUUIDs` ved `S:252,370,681` dupliserer inviterrollen som allerede er lagret i endpoint ved `:366,600,606`; bruk én uforanderlig kilde til rollen. Dette er forenklingsforslag, ikke ytterligere blockerfunn. Jeg ville ikke introdusert en ny resolver, global identitetsmodell, separat peer-kvotemanager eller generisk auth-rammeverk.

**4. Rebasen er riktig, og main tilførte ingen ny ready-only-bro.**

Uavhengig `git range-diff a6fa51a..b4f66b4 9c60001..101e5452` viser 23 bevarte commits, 22 like patcher og én workflow-konteksttilpasning. Konflikten er korrekt løst: genesis-suiten består ved `CP/.github/workflows/cellprotocol-swift-linux.yml:98`, og **SimulatedEntity, MockBridgeTransport og AuthenticatedBridgeFixture** kopieres ved `:106–108`. Ingen produksjonskode ble konfliktløst. `git diff --check` er grønn.

Main-deltaet er ni filer, +599/−6. Produksjonsdiffen er genesis-klassifisering og videreføring av seal ved restore. Alle åtte filer utenom workflowen er byteidentiske mellom ny main og vurdert head. Bridging, Scanner og resolver er byteidentiske med `b4f66b4` etter rebase. Søk i main-deltaet med `-G 'BridgeBase|BridgeTransport|ready' -- Sources Tests` gir ingen treff. Jeg fant derfor ingen **ny main-bruker** som har gått utenom porten. Dette er komposisjonskontroll, ikke en ny full sikkerhetsrevisjon av genesis-endringen.

Dedikert og multiplexet resolver bruker porten (`CP/Sources/CellBase/Cells/CellResolver/CellResolver.swift:2250,2301,2323`), og Scanner har factory etter proof (`S:599–609`). `.ready` avvises i gate, Base og mux (`B/BridgeChannelTransport.swift:220`; `B/BridgeBase.swift:1348,1369`; `B/BridgeMultiplexing.swift:928`). Lokal Base-aktivering krever `session.check()` (`B/BridgeBase.swift:466–470`). N07–N09 er peer-integrasjonsfeil i det bevarte R3-settet, ikke rebasekonflikter.

**5. CI og lokale feil på endelig head.**

GitHub Actions API filtrert på hele head-SHA og PR-ens check-rollup viser fem fullførte, grønne kjøringer, alle attempt 1. De fire test-/benchmarkkjøringene er nå `pull_request`, ikke de tidligere manuelt startede kjøringene på gammel head.

| Workflow | Resultat og kilde |
|---|---|
| macOS regression | [success, 36373503285](https://github.com/Digipomps/CellProtocol/actions/runs/36373503285). Fulltest-resultater og utvalgte passed-linjer kontrollert i jobb-logg hentet fra GitHub. |
| CellProtocol Swift Linux | [success, 36373503313](https://github.com/Digipomps/CellProtocol/actions/runs/36373503313). Eksisterende `ci-linux.log:1479–1484` viser genesis-suiten og 82/0 i det relevante sammensatte teststeget; øvrige loggdetaljer er **ikke lest**. |
| Vapor identity vault Linux | [success, 36373503255](https://github.com/Digipomps/CellProtocol/actions/runs/36373503255). Detaljert testlogg **ikke lest**. |
| Runtime capacity benchmark | [success, 36373503315](https://github.com/Digipomps/CellProtocol/actions/runs/36373503315). Detaljerte måleresultater **ikke lest**. |
| Notify PyCellProtocol | [success, 36373501744](https://github.com/Digipomps/CellProtocol/actions/runs/36373501744), `pull_request_target`; varsling, ikke peer-/Swift-runtime-bevis. |

macOS sjekket ut syntetisk PR-mergecommit `110f45c840334fb47272adc34ce4c4098d1d425a`. `git rev-parse` bekrefter at både den og vurdert head har Git-tre **`24b0937492754eb4dbb31fe208b378f5722cd508`**. Nettloggens siste fulltestlinje er **1398 tester, 5 skipped, 0 feil**, 41.865 (42.153) sekunder. Begge N06-tester og positiv peer-reconnect er eksplisitt passed. Workflowen bruker pinnede dependencies og etterfølgende diff-kontroll (`CP/.github/workflows/security-regression-macos.yml:24–32`). TSAN gjelder bare BridgeDescriptionConcurrencyTests, tre runder (`:33–46`), ikke alle peer-livsløp.

Implementørens lokale rebase-logger er lest i relevante utsnitt: bygg complete 12,94 sekunder; lokal fulltest har tre feil. Ingen ny basekjøring eller egen fulltest er kjørt av meg.

| Lokal feil, `/private/tmp/cp53-rebase-evidence/test.log` | Samme test i nettloggen på vurdert tre |
|---|---|
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns`, linje 270: CDSA/EPERM, NSOSStatus 100001, `IdentityVault.swift:1374` | passed, 0.080 s |
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyStillSigns`, linje 273: samme feil | passed, 0.054 s |
| `AppleIdentityVaultKeyStorageTests.testScopedSecretDataStaysStableInUnsignedTestHost`, linje 282: status −25291, `IdentityVault.swift:780` | passed, 0.008 s |

Vault-kilden og denne testfilen er uendret fra base. Miljøforklaringen er godt støttet; lokal fulltest skal likevel rapporteres som rød. **Forskjellen i testantall er nå forklart:** lokal Swift 6.4-kjøring har separate bundler med HavenCommons **26/0**, CellNearby **3/0** og CellBase **1369, 12 skipped, 3 feil**. CI har én samlet `CellProtocolPackageTests.xctest` med **1398**. Jeg sammenlignet de unike `Test Case … started`-navnene: begge logger har de samme 1398 navnene, ingen bare på én side. De syv ekstra lokale skips er Keychain-tester. «1369 mot 1398» skyldes altså oppsummeringsgrensen, ikke 29 uoppdagede tester.

Den eksplisitte toprosessprøvens parent-logg viser **1 test / 0 feil**, 9.511 (9.512) sekunder. Jeg kontrollerte også begge workerlogger og `.passed`-markører i begge katalogene som `CP53-REBASE.md` navngir: `cp53-multipeer-24730BE4-62F7-43F6-9BFE-132A0110DD22` og `cp53-multipeer-5E07BE86-15CF-4A15-972E-D3BB0822906A` under oppgitt macOS-tempbane. Det støtter at ekte MCSession, invitasjon, oppsett og feed ble kjørt i begge inviterretninger. Testkoden bruker ekte adapter, to prosesser og lokale syntetiske nøkler (`T/ScannerMultipeerProcessTests.swift:11–98`). Ordinær CI skipper prøven. Den tester ikke MITM, tre peers, reconnect på ekte MC, femminutters expiry eller iOS/NearbyInteraction.

**5b. Arbeidet fra 02.–16.09 burde vært del av planens grunnlag. Det var ikke bare en gammel uautentisert stub.**

Binding-forensikken beskriver både en faktisk `VaporCellBridge` med to bevisveier og en CP-klientpatch som bevarer og sender et allerede eksisterende origin-bevis. Den sier uttrykkelig at eget vokabular ble forkastet da eksisterende `IdentitySigningChallenge`/resolver-vokabular ble funnet (`Binding/Documentation/HAVEN_Bro_Forensikk_og_Status_2026-09-02.md:128–183,270–295`). Det er relevant tidligere implementasjon med samme formål og lokal signering. Å utelate den 26.09 var et reelt hull i kildegrunnlaget; linjetellingen i R3 forsvarer ikke utelatelsen.

Men den sterkere historiske formuleringen «kjeden er dermed hel i kode» (`:293–295`) blir korrigert av den senere, konkrete kontrollen: `G/RAPPORT.md:158–186` finner tre åpne sikkerhetsfeil, og begge PR-utkastene sier ikke klar for merge. 116 grønne CP-tester og kompilerende server var ikke en bestått autentisert ende-til-ende-prøve. `G/PR_CellProtocol.md` beskriver URL-testene; `G/PR_CellScaffold.md` og `G/RAPPORT.md:145–149` sier at den nye rutens E2E ikke var utført.

| Funn fra 15.09 | Løser PR #53 det? |
|---|---|
| **Samme bevis forbrukes to ganger** | **Ja i den nye kanalprotokollen; nei som patch av den gamle ruten.** Historisk `OLD-CS/Sources/App/Controllers/VaporCellBridge.swift:158,182,327–329` forbruker det samme query-beviset i både upgrade-kontroll og handler. CP53 holder én challenge per sesjon og forbruker pending atomisk én gang (`B/BridgeChannelSession.swift:307–317`); policy-recheck/activate konsumerer ikke beviset på nytt (`:334–355`; `B/BridgeChannelTransport.swift:256–267`). Den gamle handleren er ikke endret av CP-PR-en. Gjenbruk av den uten migrering beholder dobbeltforbruket. |
| **Caller er ikke bundet til kommandoene** | **Ja ved korrekt integrert gate, med ny peer-svakhet N07/N08.** Historisk caller ender i loggen; config/transport får ikke caller (`OLD-CS/Sources/App/Controllers/VaporCellBridge.swift:182–212,224–238`). CP53 sammenligner innkommende principal, saniterer requester og binder mux-factory til bevist identitet (`B/BridgeChannelSession.swift:374–409`; `B/BridgeBase.swift:1343–1365`; `B/BridgeMultiplexing.swift:1040–1045`). Dette er en reell reparasjon på protokollgrensen. Den sertifiserer ikke en gammel route eller en peer-adapter som velger feil fysisk motpart. |
| **Sprout-utsteder er ikke forankret** | **Nei.** Historisk sjekk av selvoppgitt signatur og substring-endpoint ved `OLD-CS/Sources/App/Controllers/VaporCellBridge.swift:363–379` er ikke reparert av PR53. Auth-profilene kontrollerer nøkkelbesittelse og kanalscope, ikke om en Sprout-utsteder har myndighet. Ingen Sprout/`issued_by`-verifikasjon finnes i de leste nye brofilene. Vertsintegrasjonen må binde kontraktens subject til bevist kanalprincipal og kontrollere betrodd utsteder, eksakt konfigurert endpoint, expiry og relevant formål. |

Et konkret gjenbruksgrunnlag for siste rad fantes allerede: `OLD-CS/Sources/App/Services/SproutResolverCompatibility.swift:839–878`, særlig sammenligning med resolverens offentlige nøkkel (`:864–867`) og eksakt endpoint (`:869–877`). Gjenbruk **kontrollene**, ikke hele funksjonen ukritisk: den har publisher-allowlist og bygger forventet URL med request-headerkontekst. Den generelle broens formål var nettopp ikke en hardkodet celleliste. Ny vert må bruke betrodd offentlig konfigurasjon og gjeldende kontraktpolicy.

**Hva burde vært gjenbrukt konkret:**

- `VaporCellBridge` som vertsintegrasjonens skisse: faktisk RouteCollection, `/bridgehead/:cellName/:bridgeID`, brytere, innkommende avvisning, opprydding og skillet mellom lokal publisher-oppløsning og requester. Installer CP53-gaten før Base/lookup, fjern ready og reparer de tre dokumenterte feilene; ikke innfør en konkurrerende generell rute. Historisk kode: `OLD-CS/Sources/App/Controllers/VaporCellBridge.swift:39–68,138–238`.
- Eksisterende `IdentitySigningChallenge`, offentlig verifikator, lokal vault og Base/resolver/Agreement-modell. **Disse er faktisk gjenbrukt i PR53**, både i WS- og peer-profilen. Ny proof-kode er derfor ikke et nytt kryptobibliotek eller en ny cellemodell (`B/BridgeChannelAuthentication.swift:175–186`; `B/BridgePeerChannelAuthentication.swift:58–68`; `CP/Sources/CellBase/Cells/CellResolver/CellResolver.swift:2419–2449`).
- Erfaringen fra `bro-cp.patch`: dedikert forbindelse må faktisk bære nødvendig klientbevis/kontraktkontekst; URL-byggeren alene beviser ikke en fungerende rute. Patchen var +181/−11 i to CP-filer; gjenopprettet CS-commit var +515 i to filer. Behold problemforståelsen og positive/negative rutetester. **Ikke kopier query-beviset inn i den nye profilen:** CP53 avviser query ved `B/BridgeChannelAuthentication.swift:77–87` og erstatter det med ferskt kanalbevis. Eventuell Sprout-kontekst trenger en eksplisitt migrert, autorisert vei, ikke taus bortfiltrering eller en gammel ready-sideinngang.
- HD-0040s avklaring av hvilke prosesser som eier hvilke ruter, og behovet for faktisk beskyttet `adminOverview`-lesing. `HD/BRO-RUTE-20260916.md:17–42,48–63,81–91` beviser at `VaporBridgehead` på den basen var en helper uten RouteCollection, og skiller hovedappens generelle rute fra AdminScaffolds egne dedicated/mux-ruter. PR53 registrerer ingen av dem.

HD-evidensen må leses kritisk: notatet `HD/evidence/BRO-prod-20260916T1030Z.md:13–35` sluttet for sterkt fra 1006 og en kontrollrutes 101/1008; dette ble uttrykkelig korrigert i rapporten. Et gammelt admin-image er relevant driftsevidens, ikke alene bevis for alle brofeilenes årsak. Runde 3 av vertslesingen korrigerer også «MANGLER» fra tidligere runder til manglende lesetilgang (`HD/evidence/ADMIN-VERT-3-20260916T1843Z.md:3–15`). Disse er historiske observasjoner; dagens prod er **ikke lest eller målt**.

**Svar til Kjetil om «opprinnelig implementasjon»: PR53 er lenger unna septemberløsningen i wire/API og endringsomfang, men beholder det opprinnelige bromaskineriet.** Query-bevis/upgrade/ready er erstattet med obligatorisk challenge/proof/ack, sesjonsprincipal, expiry og kvoter for alle Base-konsumenter. R3 var nødvendig fordi akkurat denne kontraktsendringen brøt den eksisterende Scanner-veien. Derfor er det misvisende å beskrive arbeidet som bare å gjenregistrere en rute eller som et ubetydelig tillegg fordi Scanner har netto +55 linjer.

Samtidig er det begrunnet å flytte principalbinding og engangsopptak til en felles port: det lukker to feil som den lille septemberruten faktisk hadde, og unngår at hver vert må lage sin egen sesjonsautoritet. Scanner beholder MC/discovery/invitasjon, per-peer-adapter, setup-operation og Lobby/GeneralCell.attach. Det er ikke en parallell broimplementasjon. Jeg ville **ikke** rullet tilbake disse sikkerhetsgrensene for å gjøre diffen liten. Jeg ville gjenbrukt den gamle vertsruten og issuer-kontrollene i det videre integrasjonsarbeidet, fjernet redundant Scanner-state og rettet den fysiske peer-bindingen. PR53 er nærmere kravet om bevist caller for WS, men er fortsatt ikke en gjenopprettet, verifisert produksjonstjeneste eller en lukket peer-sikkerhetskjede.

**6. Beslutning og aksept før merge.** Anbefalingen er **merge etter tre rettinger**, med ny vurdering av de konkrete bevisene:

1. N07: kryptografisk binding mellom bevist peer og transport/dataframes; ekte videresendings-/MITM-regresjon med positive kontroller.
2. N08: uforanderlig fysisk rute og generasjon gjennom receive/send/close; tester for discovery-kollisjon og sen vanlig data/callback over reconnect.
3. N09: iOS-token gjennom autentisert per-peer-port; test at aktiv/pending/revoked-blanding ikke gir utsending til feil peer eller ødelegger handshake.

N06, rebasen og den dokumenterte positive toprosessfunksjonen trenger ikke omarbeides for å behandle disse funnene. De nødvendige rettingene skal beholde én gate/sesjonsmaskin, lokal nøkkelkontroll og vanlig celleautorisasjon; deretter må CI og relevant adapterfunksjon kontrolleres på nytt på endelig head.

Tidligere N05 i Bindings egendefinerte transport er **ikke lest på nytt** og er ikke opphevet. CellScaffold/HavenAgentD/andre konsumenters nye heads, WSS/proxy/discovery, Sprout-policy, readiness og AP9b er **ikke verifisert i denne kontrollen**. Kravene i forrige rapport om koordinert migrering og reelle beskyttede operasjoner står ved lag. Grønn CP-CI og en CP-merge er ikke produksjonsgodkjenning.

Arbeidstrærne hadde eksisterende endringer. Den vurderte CP-worktreen var ren ved kontroll. **Denne rapporten er den eneste filen jeg har skrevet.** Ingen kode, commit, push, merge, PR-kommentar, dependency-pin, køpost eller deploy er endret.
