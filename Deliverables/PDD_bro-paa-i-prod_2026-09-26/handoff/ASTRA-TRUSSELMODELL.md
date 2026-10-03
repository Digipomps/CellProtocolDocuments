STATUS: LEVERT — 10 funn (2 blokkerer)

# Astra — trusselmodell før implementering av bro i prod

Dato: 2026-09-27. Eier: Astra (Codex). Mottaker/integrator: Losen og Kjetil.
Arbeids-ID: PDD_bro-paa-i-prod_2026-09-26/astra-forhaandsreview.
Leveransen er en kildebasert vurdering før implementering, ikke produksjonsgodkjenning. Bare denne rapportfilen er skrevet. Ingen kodeendring, gren, commit, push, bygg eller testkjøring er utført.

**Konklusjon:** Det er mulig å bevise brukeridentitet uten brukerens private nøkkel eller signeringstoken på prod/staging. De eksisterende signeringsprimitivene kan gjenbrukes, men dagens `IdentitySigningChallenge`-løp autentiserer ikke en hel forbindelse. Minste riktige første leveranse er en eksplisitt, engangs autentisering ved åpning, en uforanderlig requester-binding gjennom forbindelsens levetid, og fortsatt ordinær celleautorisasjon. Å fjerne senere identitetsbevis krever i tillegg en ny, intern beviskontekst i CellProtocol; å sette `ready = true` eller feste serverens vault på requesteren er ikke en løsning. Kildegrunnlaget og skillet mellom eksisterende mekanismer og forslag følger nedenfor.

## 1. Revisjoner, metode og avgrensning

Alle kodehenvisninger gjelder `git --no-optional-locks -C <repo> show origin/main:<fil>` ved revisjonene under. Intervaller angir leste linjer, ikke linjer i arbeidskopiene. Forkortelsene `CP/`, `CS/` og `AD/` betyr henholdsvis `CellProtocol/`, `CellScaffold/` og `HavenAgentD/` relativt til HAVEN-roten.

| Repo | Lest `origin/main` | Nettkontroll |
|---|---|---|
| CellProtocol | `3fbdb953ba7db549238c7fe165ec388f30d9ad00` | Samme SHA fra `git --no-optional-locks ls-remote origin refs/heads/main`. |
| CellScaffold | `ea00be47cdfc40deb9977f1df4322baa22efa99d` | Samme SHA fra `ls-remote`. |
| HavenAgentD | `ca1eda9aec72c7bce5bcdd99060721dad378afd1` | GitHub-main var `a9da717453ef3061d288fb5abbb29135c17fc720`. De tre etterspurte filene er sammenlignet byte for byte med GitHub Contents API på denne SHA-en og er identiske. Ingen lokal ref er oppdatert. Resten av forskjellen er **ikke lest**. |
| CellProtocolDocuments | `c83dab6e1ee3c481c99758b09e03cf610a7011b5` | Samme SHA fra `ls-remote`. Formålsspesifikasjonen er lest fra oppgitt oppgavemappe, som oppgavegrunnlag. |

Arbeidskopiene hadde allerede mange endringer; ingen av dem er brukt som kodegrunnlag. `rg` var ikke installert; kildesøk er gjort med `git --no-optional-locks grep` og målrettet lesing av Git-objekter.

`FORMAALSSPEC.md` §0, §1 og §6 er lest. Målingene der fra 26.09 (404/1006, app- og dependency-revisjoner) er **Losens historiske målinger**, ikke målinger gjentatt av Astra. Ingen aktuell prod/staging-tilstand, privat nøkkelbestand, vertslogg, brannmur eller aktiv proxykonfigurasjon er inspisert.

**Viktig korrigering av en mulig premissfeil:** [CellProtocol PR #39](https://github.com/Digipomps/CellProtocol/pull/39) var `OPEN`, head `5fa0b96e718c418e2a2e306fd6b4f809231bc093`, uten merge-commit ved `gh pr view`; hele diffen er lest med `gh pr diff`. Likevel finnes Vapor-rettelsen allerede på main: `CP/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift:218–230`. Filhistorikken viser integrasjonscommit `b5b7282b495e96a7899a189087592581426f4bfb` (#40), som er forfar til både dagens main og CS-pinnen. PR #39s egen head er ikke forfar til main. Åpen PR betyr her ikke manglende rettelse.

CS pinner CP til `5609a9ad23e76999e1cf1609e1de5a010ae2e3c9`: `CS/Package.swift:123–129`, `CS/Package.resolved:40–45`. Vapor-vaultvalget er kontrollert også på pinnen. `BridgeBase.swift`, `BridgeIdentityProofAuthorization.swift` og `IdentitySigningChallenge.swift` er byte-identiske mellom pinnen og gjennomgått CP-main. Dette sier ikke hvilken revisjon som faktisk kjører i prod.

Historikken er lest særskilt: `14b50a51fbfd2e351098501bdde04145bf3bb22b` fjernet WebSocket-handleren og begrunnet det med manglende autentisert sesjons-/kanalbinding; `d662329442a3b6e6413b5272d1c7bf85d343b190` fjernet registreringen. Dagens bekreftelse er `CS/Sources/App/Controllers/VaporBridgehead.swift:14–16` og ruteregistreringen i `CS/Sources/App/routes.swift:269–320`. Den gamle usikre handleren skal ikke gjeninnføres.

Lest: de etterspurte filene; de sikkerhetsrelevante delene av Bridging-katalogen; identitetsverifikasjon, replay, offentlig snapshot, lokal vaultmatching, celleautorisasjon og feed-revalidering; relevante testkilder; readiness/deploy-utdrag; repoets nginx-eksempler. `BridgeBase`, resolveren, multiplexing, Lightweight-transporten og store vault-/appfiler er lest målrettet, ikke linje for linje i sin helhet. Alle målcelleoverstyringer, øvrige klienter i Binding/HAVEN-appen, full native-porthole-kontraktvalidering, alle tredjepartsbiblioteker og hele utrullingssystemet er **ikke lest**. `HAVEN-Deploy` hadde ikke lesbar `origin/main`; promoteringskoden der er **ikke lest**. Dette er ikke en revisjon som kan love «ingen hackbare ledd» i alle eksterne komponenter.

## 2. Tillitsgrenser og det som faktisk finnes

Beskyttede verdier er brukerens signeringsnøkkel, identitetens opprinnelse, private celledata, skrive-/handlingsmyndighet, samtidige økter og tilgjengelighet. Angriperen kan være en uautentisert nettklient, en autentisert identitet uten rettigheter til målcellen, en ondsinnet peer som ber klienten signere, eller en aktør som gjentar/omruter observerte meldinger. Feil utrulling inngår som en tilgjengelighetstrussel.

Den anbefalte tillitsgrensen er:

```text
brukerens lokale vault
    │ offentlig deskriptor + snevert åpningsbevis
klient-scaffold
    │ sertifikatverifisert WSS
betrodd TLS-proxy
    │ beskyttet backend-forbindelse
/bridgehead/<publisher>/<broId> — autentisering før celleoppslag
    │ serveropprettet sesjon + uforanderlig offentlig requester
BridgeBase / resolver
    │ samme requester, konkret handling/nøkkelsti og gjeldende policy
målcellens autorisasjon
```

Dette forslaget stoler på at TLS-proxy og serverprosessen håndhever bindingen. En overtatt proxy kan endre senere usignerte kommandoer; en overtatt serverprosess kan forfalske sin egen interne autorisasjon. Å holde privatnøkkelen lokalt beskytter ikke alene mot disse to hendelsene. Skal proxyen være ubetrodd, trengs en ende-til-ende beskyttet protokoll til runtime-endepunktet, eller klientverifiserbare meldingssignaturer som også binder kommandoinnhold. Det er en større leveranse enn åpning av kanalen og må ikke påstås levert av et innloggingsbevis.

Eksisterende kjede og vern:

| Grense | Faktisk kode og betydning |
|---|---|
| Klient → endpoint | Standardruten er `bridgehead`, normalt dedikert forbindelse: `CP/Sources/CellBase/Cells/CellResolver/CellResolver.swift:66–100`. Automatisk scheme blir WSS bortsett fra eksplisitt tillatt lokal bruk: samme fil `:1620–1640`, `:1737–1745`. AD relay og correspondence velger denne ruten: `AD/Sources/HavenAgentRuntime/DeviceActionRelay.swift:856–872`, `AD/Sources/HavenCorrespondenceMCP/CorrespondenceContracts.swift:11–16,41–49`. |
| TLS/proxy → app | Repoets prod-eksempel bruker TLS og loopback-backend, med Upgrade: `CS/Documentation/Operations/nginx/haven_production.conf:20–35,78–89`. Staging-eksemplet har tilsvarende proxy/TLS: `CS/Documentation/Operations/nginx/staging_haven.conf:48–64`. Inkluderte `/etc/nginx/proxy_params` og TLS-options samt faktisk installasjon er **ikke lest**. |
| App → BridgeBase | Den generelle ruten er fjernet; native-porthole har separat kontraktvalidering før broopprettelse og lukker med policy violation ved feil: `CS/Sources/App/Controllers/VaporBridgehead.swift:14–16`, `CS/Sources/App/Controllers/VaporSproutResolver.swift:60–79,108–115`. Det er ikke bevis for en generell identitetsbundet bro. |
| Wire → requester | CP saniterer alle ikke-`.sign`-requestere til offentlig snapshot, fast offentlig metadata-grant og `BridgeIdentityVault`: `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1264–1277`. Vapor gir alltid bridge-vault: `CP/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift:184–230`. |
| Bridge → målcelle | `.get`, `.set`, `.admit`, `.agreement` og feed videresender requester: `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1284–1322,1350–1404,1600–1613`. Eget oppslagsprinsipal kan velges før resolveroppslag: samme fil `:902–939`. |
| Målcelle → bevis | Owner kontrolleres mot betrodd eiernøkkel; lenket identitet mot registerets nøkkel; kontraktsubjekt beviser sin nøkkel: `CP/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:2035–2067,2185–2203`. Origin-beviset er en ny utfordring med målcellens domene/UUID, `checkIdentityOrigin`, `GeneralCell`, nonce og offentlig verifikasjon: samme fil `:2253–2292`. |
| Bevis → lokal signering | Bare aktive, lokalt initierte operasjoner gir signeringslease; riktig prinsipal, domene, ressurs, handling og publikum kreves: `CP/Sources/CellBase/Cells/Bridging/BridgeIdentityProofAuthorization.swift:40–81`. `.sign` krever ready, containment, lease og lokal vaultmatching; signatursvaret verifiseres mot den lagrede forespørselen: `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1422–1485,1775–1794`. |

En WebSocket-oppgradering er ikke i seg selv brukerautentisering; TLS beskytter transporten, mens applikasjonen må definere autentiseringen. Det følger også av [RFC 6455 §10.5–10.6](https://www.rfc-editor.org/rfc/rfc6455#section-10.5).

## 3. Funn, rangert etter risiko for den planlagte åpningen

«Blokkerer» betyr at formålet ikke kan leveres forsvarlig/funksjonelt før forholdet er løst. De øvrige gradene uttrykker konsekvens og eksponering. Funnene er ikke påstander om at den fjernede prod-ruten kan utnyttes akkurat nå. Alle åpne funn må rettes eller få eksplisitt, dokumentert risikobehandling før produksjonsgodkjenning.

| ID | Grad | Funn |
|---|---|---|
| F01 | **blokkerer** | Ingen autentisert kanaltilstand som binder alle innkommende kommandoer til bevist identitet. |
| F02 | **høy** | HD-0080-klassen er rettet i Vapor, men lokale vault-fallbacks finnes fortsatt i Apple/Lightweight. |
| F03 | **høy** | Eksisterende replay-vern er for signering, ikke engangs adgang til en bestemt serverkanal. |
| F04 | **høy** | Manglende kanalbinding innebærer også manglende livsløp for tilbakekalt/utløpt kanalidentitet. |
| F05 | **høy** | Discovery/scheme/header-tillit kan gi feil mottaker eller nedgradering; aktiv proxy er ikke verifisert. |
| F06 | **høy** | Ruteidentitet, broeier og requester må skilles; eksisterende oppslagsunntak og UUID-cache er farlige å gjøre til autoritet. |
| F07 | **høy** | Eksisterende grenser stopper ikke total overbelastning fra mange forbindelser/identiteter. |
| F08 | **blokkerer** | Generell bridgehead-rute mangler, og lest readiness/deploy-kontroll verifiserer ikke brokontrakten. |
| F09 | **middels** | ADs lokale token-/allowlist-mønster er ikke en produksjonsmodell for bevist brukeridentitet. |
| F10 | **middels** | Sendfeil kan svelges; eksisterende ready-reset er ikke en autentisert reconnect-kontrakt. |

### F01 — Identitetsforfalskning, identitetsbytte og tidlig kommando

**Utnyttelse ved naiv gjenåpning:** Angriperen oppgraderer WS, sender `ready`, og sender kommandoer med vilkårlige offentlige identiteter, eventuelt A ved åpning og B senere. Det finnes ingen serverlagret, verifisert kanalprinsipal som sammenlignes med hver kommando. `.ready` setter bare flagget; `.get/.set` har ingen tilsvarende ready/auth-vakt: `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1265–1282,1350–1404`.

**Eksisterende vern:** Det gir ikke automatisk tilgang til en korrekt beskyttet celle: sanitering fjerner lokale grants/vaults, og GeneralCell krever owner-/kontraktsbevis og keypath-autorisasjon (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1267–1276`; `CP/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:1986–2009,2035–2098,2193–2203`). En gyldig signatur med angriperens egen nøkkel og offerets UUID er ikke bevis for offerets betrodde nøkkel.

**Også multiplex:** `openChannel` kontrollerer deskriptorformat, ikke en signatur; kanalposten lagrer delegate/transport, ikke bevist identitet, og senere kommandoer dispatches etter kanal-ID: `CP/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift:760–767,863–920,967–990`. Navn eller kommentar om «identity-bound» er derfor ikke nok.

**Forslag:** En eksplisitt tilstandsmaskin før BridgeBase-dispatch: unauthenticated → challengeIssued → verifying → authenticated → revoked/closed. Bare verifieren kan åpne den. Identitetsbytte, klientstyrt `ready`, kommando før bevis og ukjent protokollversjon avvises uten resolver-/cellekall. Gjelder også `.response`, `.sign`, close/openChannel og feed, med eksplisitte roller for de to retningene.

### F02 — Presentert deskriptor som lokal vault (HD-0080)

**Utnyttelse:** Peer sender UUID og nøkkelfingerprint som matcher en identitet mottakeren faktisk har lokalt. Hvis transporten velger vault etter «kjent nøkkel», kan en wire-identitet få referanse til den lokale signeringstjenesten. Dette er mer alvorlig enn å eie en offentlig deskriptor.

**Rettet i Vapor:** `CP/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift:218–230` returnerer alltid `BridgeIdentityVault`, også uten delegate. CSs autentiserte transport gjør det samme: `CS/Sources/ScaffoldKit/AdminAuthenticatedVaporBridgeTransport.swift:419–421`. De tre regresjonstestene finnes på main: `CP/Tests/CellBaseTests/VaporBridgeTransportTests.swift:90–188`; de er lest, **ikke kjørt** her.

**Gjenstående kildefunn:** `CP/Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift:821–845` returnerer lokal/default vault ved kjent identitet og har default-fallback uten delegate. Wire-dekoding bruker resultatet før både command/response: samme fil `:944–971`. `CP/Sources/CellApple/AppleBridgeTransport.swift:148–185` har tilsvarende lokale fallbacks.

**Begrensning av funnet:** BridgeBase-saniteringen og lokal signeringslease hindrer den enkle direkte veien til signering i de gjennomgåtte BridgeBase-handlingene (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1267–1277,1456–1485`). Full utnyttelse gjennom disse lagene er ikke demonstrert. Likevel brytes proveniensgrensen før delegate-kallet, særlig for alternative delegates/svar. Rett alle innkommende transportvalg etter opprinnelse; ikke lag et «serverens egen identitet»-unntak basert på wire-data.

Visiting-registeret er ikke en privat vault: `CP/Sources/CellVapor/VaporIdentityVault.swift:2335–2348,2506–2513`. Men det indekserer etter UUID og prioriteres ved oppslag; ukontrollerte besøksdeskriptorer må ikke bli en betrodd nøkkelkatalog. Registrer helst først etter bevis, avgrens levetid, og bruk domene/UUID/fingerprint der tillit eller kvoter avgjøres.

### F03 — Replay, feil publikum og falsk friskhet

**Utnyttelse ved gjenbruk av dagens primitive som innlogging:** Et observert bevis presenteres på ny socket, annen kanal, publisher, prosess eller etter restart. En implementering som bare validerer utfordringsformat og signatur har ikke kontrollert at serveren faktisk utstedte utfordringen på denne forbindelsen.

**Eksisterende vern:** `IdentitySigningChallenge` har type/versjon/purpose, UUID, fingerprint, domene, ressurs, handling, publikum, nonce og tid. Validatoren begrenser payload til 8 KiB, nonce til 32–128 bytes, scope til 512 tegn og gyldighetsintervall til 60 s: `CP/Sources/CellBase/Identity/IdentitySigningChallenge.swift:22–44,99–164`. Signaturverifieren bruker bare offentlig nøkkel, avviser private/feilbrukte nøkler og ukjente algoritmepar: `CP/Sources/CellBase/Identity/IdentityPublicKeySignatureVerifier.swift:14–71`.

**Gap:** Validatoren krever ikke at audience/domain/resource/action er lik en lokalt forventet kanal; den krever primært ikke-tomme scopes. Den tillater issuedAt inntil 300 s fremover (`IdentitySigningChallenge.swift:142–163`). En utfordring med 60 s intervall kan dermed ha utløp opptil ca. 360 s fra verifierens nåtid. Det er ikke en garantert 60 s serverfrist.

Replay-lageret er en prosesslokal actor med engangs consume, expiry-opprydding og nøkkel av identitet+scope+nonce: `CP/Sources/CellBase/Security/CellSecuritySigningChallengeReplayStore.swift:14–41,53–79`. Det kalles i `.sign` før lokal signering, betinget på at det finnes: `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1466–1479`. Det er normalt opprettet, men kan settes til nil: `CP/Sources/CellBase/Cells/CellRuntimeEnvironment.swift:24,214–216`. Dette er ikke et obligatorisk serverregister for aksepterte innlogginger.

**Forslag:** Serverutstedt, uforutsigbar engangsnonce og eksakt lagret transcript per fysisk forbindelse/generasjon; signatur over samme bytes; atomisk consume før authenticated. Lokalt utstedelsestidspunkt og monoton deadline bestemmer aksept. Samme bevis på annen socket/instans må være ukjent, ikke «signaturen var gyldig». Ved connection-affinitet og ingen resume kan dette løses uten varig, global replaydatabase: restart mister pending/session-state og avviser alt gammelt. Hvis handshakes eller resume flyttes mellom instanser, kreves felles atomisk lager eller én eksklusiv eier per utfordring. Ny nonce alene uten slik binding er utilstrekkelig.

### F04 — Gjenbruk etter tilbakekalling, utløp eller nøkkelbytte

**Utnyttelse:** En tidligere gyldig klient beholder socket/feed etter at nøkkel, kontrakt eller identitetslenke er tilbakekalt. Et fremtidig engangsbevis som caches uten levetid gjør problemet større.

**Eksisterende vern må bevares:** GeneralCell sjekker aktuelle kontrakter/vilkår og tidsstatus (`CP/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:2087–2098,2185–2203`). Lenkeoppslaget krever aktiv status, nøkkel og godkjent domene: `CP/Sources/CellBase/Identity/IdentityLinkRegistry.swift:65–103`. Feed går via requester-autorisasjon, ikke rå publisher: `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1600–1610`; `CP/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:1273–1286`. Feed-registeret reautoriserer hendelser og kan invalidere et subjekt: `CP/Sources/CellBase/Cells/GeneralCell/FeedAuthorizationRegistry.swift:82–143`. Testkilden trekker tilbake én av to feeds og forventer at bare den andre fortsetter: `CP/Tests/CellBaseTests/BridgeIdentityBoundaryTests.swift:339–417` (**ikke kjørt**).

**Gap:** Dette tilbakekaller cellemyndighet, ikke en generell autentisert kanalidentitet. Dagens bridge har verken slik kanalpost eller dens utløps-/revokasjonspolicy; `ready` er et boolsk flagg (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:145–162,1280–1282`). En signatur beviser kontroll over en nøkkel, ikke at nøkkelen fortsatt er godkjent. Lokal sletting av nøkkel kan heller ikke alene informere en skyserver.

**Forslag:** Definer hvem som kan tilbakekalle hva: serverens transportadgang for domene+UUID+nøkkel, nøkkelens betrodde rotasjon/revokasjon, og målcellens egne avtaler/lenker er separate tilstander. Ny felles kanalpost trenger generation/authEpoch, absolutt utløp, invalidasjon og reautentisering. Sjekk kanalstatus før hvert dispatch og hver utgående feed-leveranse; kjør fortsatt celleautorisasjon. Ved tilbakekalling: sperr nye operasjoner atomisk, avbryt ventende signering og feeds, kast køet data, lukk berørte kanaler. Sett en målbar maksimal propagasjonstid; ikke lov øyeblikkelig global tilbakekalling uten en autoritativ, tilgjengelig kilde. Ukjent/stale nødvendig status skal feile lukket.

### F05 — Man-in-the-middle, discovery og nedgradering

**Utnyttelse:** En feilkonfigurert proxy slipper inn angriperstyrt Host/Forwarded-Proto; discovery signerer en feil eller ukryptert endpoint. Eller klienten bruker en eksplisitt usikker transport og et opptatt bevis relés til et annet mål.

**Kilde:** Discovery leser `Host` og `X-Forwarded-Proto` direkte: `CS/Sources/App/Controllers/VaporSproutBridgeDiscovery.swift:10–16`. Disse brukes til endpoint, som deretter signeres: `CS/Sources/App/Services/SproutBridgeDiscoveryCompatibility.swift:107–131,159–177`. Scheme-funksjonen faller tilbake til `ws` når forwarded proto mangler/er ukjent: `CS/Sources/App/Services/SproutResolverCompatibility.swift:1135–1148`. Domenekontroll og purpose-allowlist finnes (`SproutBridgeDiscoveryCompatibility.swift:88–104`), men verifiserer ikke request-host som autoritativ endpoint. `verifySignature()` bruker nøkkelen i deskriptoren selv (`:35–39`); tillit til utsteder krever en separat forankring hos konsumenten, som er **ikke lest** her.

**Eksisterende vern:** Resolverens normale eksterne rute velger WSS og avviser eksplisitt WS når policy ikke tillater det (`CP/Sources/CellBase/Cells/CellResolver/CellResolver.swift:1630–1640,1737–1745`). Repoets nginx-eksempler støtter TLS/upgrade, men arver headerregler fra uleste include-filer; se §2. Ingen demonstrert MITM i prod er gjort.

**Tilleggsrisiko:** `RemoteBridgeheadAccess.headers` kan sende bearer-token over både ws og wss til allowlistet host/port: `CS/Sources/ScaffoldKit/RemoteBridgeheadAccess.swift:48–58`. Dette er transportadgang, ikke brukerbevis. Ikke gjør tokenet til identitet eller signerautoritet.

**Forslag:** Konfigurert kanonisk offentlig WSS-origin per miljø; strengt sertifikat-/vertsnavnssjekk; ingen automatisk ws-fallback ved TLS/auth-feil; eksplisitt lokal-dev-unntak. Bind origin, port, rute, domene og protokollprofil i åpningsbeviset. Proxy må overskrive forwarded headers, avvise ukjente hosts, hindre direkte ekstern backend-adgang og beskytte backend-hop. Origin-policy for browserklienter er et tillegg; native klienter autentiseres med bevis, ikke Origin-header. HTTP-redirect alene er ikke bevis for sikker WS-adferd. Faktisk proxykonfigurasjon og en negativ nedgraderingstest må fremlegges før åpning.

### F06 — Forvirret stedfortreder og oppslag under feil identitet

**Utnyttelse ved feil implementering:** Rute-/broeieren brukes som requester, eller et verifisert bevis for A følges av kommando B. Da kan et auth-gate utilsiktet gjøre serveren til brukerens stedfortreder med serverens rettigheter. Klientvalgt `broId` kan også bli en felles registreringsnøkkel og fortrenge en annen økt.

**Eksisterende skille:** `inboundPublisherLookupIdentity` brukes til oppslag, men original sanitert requester sendes videre til cellen: `CP/Sources/CellBase/Cells/Bridging/BridgeBase+Config.swift:20–25`; `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:902–939,1350–1404`. `VaporBridgehead.bridgeConfig` pinner oppslaget til publisherIdentity (`CS/Sources/App/Controllers/VaporBridgehead.swift:49–69`); dette er nå en helper, ikke en registrert rute (`:14–16`). Det er derfor ikke grunnlag for å hevde at dagens get/set alltid bruker broeieren som requester.

**Gap/risiko:** Inbound-cache bruker bare lowercased UUID (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:908–918`), og multiplex-serverens convenience-factory ignorerer open-identiteten og bruker bridgeOwner (`CP/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift:826–859`). Dette gir ingen ny autoritet alene, men kan ikke brukes som den nye tillitsbindingen. AD registrerer klientvalgt bridgeID under owner (`AD/Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:307–328`); kollisjonsvirkning i alle resolvervarianter er **ikke lest**.

**Forslag:** Fast requester fra verifisert sesjon; wire-identitet må matche UUID+nøkkel eller avvises, aldri byttes stille. Eventuell egen publisher-lookup-identitet er et eksplisitt lokalt rutekart, ikke arv av adminrettigheter. Cache og registrering nøstes under serveropprettet sessionID/generation og verifisert nøkkel/domene. Ekstern broId er et rutefelt, ikke eierskap. Test privat celle til A, servereier, B og samme UUID med annen nøkkel; cellen skal se nøyaktig den beviste requesteren og evaluere den konkrete handlingen.

### F07 — Tjenestenekt gjennom kanaler, utfordringer og ventende arbeid

**Utnyttelse:** Mange sockets før bevis, mange gyldige selvgenererte identiteter, mange challenges eller langsomme peers fyller registre/arbeidskøer. Kvoter per selvvalgt identitet alene stopper ikke dette.

**Eksisterende vern:** Bridge JSON har 1 MiB og nesting 64 før dekoding: `CP/Sources/CellBase/Security/BridgeInboundPayloadValidator.swift:23–45,64–87`; Vapor bruker validatoren (`CP/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift:184–198`). Utfordringer har 8 KiB-grense (`CP/Sources/CellBase/Identity/IdentitySigningChallenge.swift:28–31,105–107`). Multiplex har default 128 kanaler, 32 pending opens og reservasjonskontroll (`CP/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift:803–811,923–933`). Signering har rate-limit; CS aktiverer localProtection utenfor testing (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1179–1216`; `CS/Sources/App/configure.swift:1163–1171`). Standard signeringsgrense er 12/60 s (`CP/Sources/CellBase/Security/CellSecurityContainment.swift:19–26,244–264`).

**Gap:** Signeringsscope inneholder bridge-UUID, så flere broer får ulike bøtter (`BridgeBase.swift:1194–1202`). Multiplex-grensene gjelder én server-session. Replay-lageret har TTL-opprydding, men intet antallstak (`CP/Sources/CellBase/Security/CellSecuritySigningChallengeReplayStore.swift:14–40,53–57`); visiting-registeret vokser ved nye UUID-er (`CP/Sources/CellVapor/VaporIdentityVault.swift:2335–2340`). Ingen samlet pre-auth-/identitetskvote finnes i de leste generelle route-/bridge-handlerne. Maksgrenser på WebSocket-frame/reassembly i faktisk server og biblioteker er **ikke lest**; JSON-grensen beviser ikke vern før buffring.

**Forslag:** Globale, per-kilde og per-bevist-nøkkel tak før dyre operasjoner; atomisk reservasjon og ubetinget frigivelse ved feil/lukking; handshake-timeout, bounded task queues, feed/backpressure og begrenset audit-volum. Forhindr store fragmenterte meldinger allerede på WS-laget. Dette samsvarer med krav om begrensninger på både frames og reassemblerte meldinger i [RFC 6455 §10.4](https://www.rfc-editor.org/rfc/rfc6455#section-10.4). Konkrete startverdier står i §6, merket som forslag.

### F08 — Ruten kan være borte uten at readiness stopper utrullingen

**Feilscenario:** En deploy passerer HTTP/readiness-kontroll selv om broen er fjernet eller autentiseringshandleren aldri blir klar. Det er tilstrekkelig for å bryte det desentraliserte klientløpet, også uten en angriper.

**Kilde:** Den generelle route-handleren er ikke registrert (`CS/Sources/App/Controllers/VaporBridgehead.swift:14–16`; `CS/Sources/App/routes.swift:269–320`), samtidig som discovery og parity-fiksturen annonserer bridgehead (`CS/Sources/App/Services/SproutBridgeDiscoveryCompatibility.swift:168–172`; `CS/Sources/App/Cells/SkeletonParity/SkeletonParityFixtureCells.swift:378–385`). `/health/ready` bygger på deployment- og canonical-runtime-snapshots, uten en eksplisitt bridge-status/handshake: `CS/Sources/App/routes.swift:235–262`. Canonical-store er klar når blockerlisten er tom; de leste komponentene inkluderer ikke bridge (`CS/Sources/App/Support/CanonicalCellRuntimeReadinessStore.swift:34–43,126–140`).

`haven-deploy` sin leste `wait_ready` godtar statusstrengen `ready`, og senere sjekkes app-revisjon/restart: `CS/scripts/production/haven-deploy:355–374,639–648`. Ingen bro-probe ble funnet ved kildesøk i denne filen. Hele HAVEN-Deploy/promoteringsløpet er **ikke lest**; det hevdes ikke at alle eksterne deploy-verktøy mangler kontroll.

**Forslag:** Bro er påkrevd readiness-komponent i prod/staging, initialt ikke klar. Registrert rute, fungerende obligatorisk verifier, replay-/sesjonslager, resolver og kvotepolicy må inngå. CI skal teste faktisk boot/route, ikke tekstsøk. Promoteringsporten må utføre en ekstern, vellykket signert handshake og beskyttet celleoperasjon, pluss avvisning uten bevis. Bare 101, et GET mot WS-stien eller native-porthole-test er utilstrekkelig.

### F09 — Lokal AD-autorisasjon kan ikke kopieres som prod-auth

**Utnyttelse hvis mønsteret løftes uendret til internett:** Manglende token gjør `authorize` til en tidlig retur; ved aktiv token brukes queryparameter, som kan havne i URL-logger. En delt token beviser uansett ikke hvem som senere er requester.

**Kilde/vern:** `AD/Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:40–49` viser optional token og querylesing. Bridge-handleren kaller authorize og krever allowlistet route før opprettelse, og lukker med 1008 ved feil (`:293–338`). Host er konfigurasjonsstyrt (`:405–409`); faktiske host-/tokenverdier er **ikke lest**. Den separate workbench-HTTP-ruten krever alltid header-token (`:52–58`), men dette er ikke WS-handlerens kontroll.

**Forslag:** Behold AD-løpet som lokalt, særskilt vurdert grense. Den nye prod-ruten krever signert identitet uavhengig av miljøtoken. Alle som beviser en identitet får forsøke cellens normale autorisasjon innen kvotene; ikke erstatt Kjetils valg med en global bruker-allowlist. Rutebegrensninger er eksponeringspolicy, ikke brukerrettigheter. Ingen bruker-signeringstoken i URL, miljø på server eller discovery-deskriptor.

### F10 — Tapte transportfeil og krav til autentisert reconnect

**Feilscenario:** Forbindelsen er borte, men send rapporterer ikke feil oppover. Klienten kan vente på et svar til en melding som aldri ble sendt, og overvåkning som bare ser send-retur kan gi falskt positiv status. En ny auth-implementering må dessuten unngå å arve en gammel principals binding ved reconnect.

**Kilde:** `VaporBridgeTransport.sendData` returnerer ved manglende socket og fanger/loggfører sendfeil uten å kaste dem videre (`CP/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift:116–150`); close-oppryddingen avregistrerer delegate (`:163–182`). `BridgeBase.ready()` bruker boolsk ready (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:428–439`). Et viktig eksisterende vern er at `setTransport` nullstiller proof-leases, feeds, ready, description-state og inbound-cache (`:440–474`); `close` nullstiller leases og transport (`:717–721`). Det er dermed feil å si at `setTransport` beholder ready. Disse resetene er likevel ikke en brukerautentisering eller dens revokasjonskontrakt. Lightweight har heartbeat/reconnect og egen generasjon (`CP/Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift:929–940,978–1015,1018–1047,604–618`); det beviser ikke at en brukerkanal reautentiseres.

**Forslag:** Egen auth-generation som alltid ugyldiggjøres ved tap/bytte av fysisk transport; nye challenges før ny ready; terminer ventende forespørsler med eksplisitt feil. Ikke replay muterende cellekommandoer automatisk ved reconnect; resultat kan være usikkert og krever idempotensnøkkel eller kontrollert read-back i cellens kontrakt. En gammel socket-callback må ikke lukke eller autentisere en nyere generasjon.

## 4. Kan IdentitySigningChallenge binde hele kanalen?

**Som byggestein: ja. Som eksisterende ferdig mekanisme: nei.**

Det finnes allerede kanonisk JSON med sorterte nøkler og de nødvendige grunnfeltene, signering hos lokal eier, offentlig signaturverifikasjon og prosesslokalt replay-vern (`CP/Sources/CellBase/Identity/IdentitySigningChallenge.swift:22–44,72–97,211–214`; `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1456–1485,1775–1794`; `CP/Sources/CellBase/Security/CellSecuritySigningChallengeReplayStore.swift:19–41`). Det finnes ikke en tilsvarende kanaltilstand og requester-binding; se F01/F03/F04.

Det eksisterende `.sign`-løpet kan ikke bare brukes før åpning: det krever ready (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:1063–1074,1434–1443`), og tillatelsen gjelder bare `action == checkIdentityOrigin`, `audience == GeneralCell`, med aktiv lokalt startet operasjon (`CP/Sources/CellBase/Cells/Bridging/BridgeIdentityProofAuthorization.swift:50–81`). Å åpne et generelt `.sign`-unntak før ready ville svekke et konkret vern.

**Minste riktige første tillegg (anbefalt):**

1. Ny, snever kanalåpningsprofil og autentiseringstilstand i CellProtocol; bruk eksisterende challenge/verifier-format der feltsemantikken passer. Signer lokalt fordi klienten selv har startet akkurat denne forbindelsen, ikke fordi serveren har sendt en vilkårlig `.sign`.
2. Knytt verifisert offentlig identitet til akkurat fysisk socket/generation og konkret rute, og håndhev den på alle senere innkommende kommandoer. Transportadapteren får ikke skape grants eller lokal signeringsmyndighet.
3. Behold ordinær requester-/celleautorisasjon, inkludert dagens snevre origin-bevis tilbake til klienten. Dette oppfyller «hele kanalen tilskrives bevist identitet» og «målcellen autoriserer som lokalt», uten å kreve at alle senere origin-bevis fjernes.

**Hvis kravet også er bare én signering for hele kanalen:** GeneralCell krever i dag en ny signatur, og en deskriptor uten vault avvises (`CP/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:2253–2288`). Da mangler en alternativ, intern kilde til identitetsbevis. Minste forsvarlige utvidelse er en ikke-serialiserbar `VerifiedRequesterContext` (foreslått navn), opprettet bare av den godkjente verifieren og knyttet til identitet+nøkkel, domene, endpoint, sesjon/generasjon, utløp og revokasjonsversjon. Den må videreføres eksplisitt gjennom resolver, cellekall og asynkrone feeds; en løs bool i Identity eller tillit til innkommende JSON er ikke nok. GeneralCell kan bruke denne som bevis for nøkkelkontroll, men må fortsatt kjøre samme owner-/link-/kontrakt-/keypath-/purpose-/vilkårspolicy. Det er en CellProtocol-runtimeendring, ikke en Vapor-shortcut. Tilfeldig kode skal ikke kunne konstruere eller kode/dekode en slik autoritativ kontekst.

Kanalbinding beviser hvem den betrodde serveren mottok kommandoen fra; den beviser ikke at hver fremtidig payload var signert eller at en helsesjekk er et brukerbevis. Et domene i en signert utfordring er avgrensning, ikke medlemskap eller en rettighet. Godta en ny, selvkontrollert nøkkel som kanalidentitet, men ikke som et eksisterende offers identitet bare fordi UUID-en er lik.

## 5. Nøkkelkravet — hva kan bevises uten skyvault?

**Arkitekturelt:** Den nye serverens autentiseringsfunksjon trenger bare offentlig nøkkel, serverutstedt utfordring, signatur, pending-state og gjeldende revokasjonspolicy. `IdentityPublicKeySignatureVerifier` verifiserer direkte med offentlig nøkkel og kaller ingen vault (`CP/Sources/CellBase/Identity/IdentityPublicKeySignatureVerifier.swift:14–71`). Dermed er brukerens private nøkkel, et bearer-token til den eller en lokal bruker-vault ikke en nødvendig avhengighet.

Det finnes også et testeksempel med separat clientVault og serverVault, offentlig owner-snapshot på servercellen, faktisk proof-rundtur, og avslag på signeringsforespørsel etter avsluttet operasjon: `CP/Tests/CellBaseTests/BridgeIdentityBoundaryTests.swift:294–336`. Dette er lest testkode, ikke et måleresultat fra denne vurderingen.

Eksisterende offentlige snapshots fjerner vault, homeVaultReference, grants og properties og godtar bare offentlige nøkler (`CP/Sources/CellBase/Identity/Identity.swift:66–94`). `Identity`-dekoding starter uten vault, men vanlig encode serialiserer også properties, nøkkelfelter og homeVaultReference (`:134–174`). Derfor må den nye håndtrykkspakken eksplisitt bruke en minimal offentlig deskriptor; ikke anta at `JSONEncoder(identity)` i seg selv er en datasanitering.

Konkrete steder hvor nøkkelkravet kunne brytes:

- Lokal vault valgt fra presentert deskriptor: F02. Vapor er rettet, Apple/Lightweight må få tilsvarende grense.
- Signering direkte i serverens `VaporIdentityVault`: den signerer når UUID/fingerprint matcher en lokalt lagret nøkkel (`CP/Sources/CellVapor/VaporIdentityVault.swift:2540–2567`). Riktig for en lokalt autorisert egen identitet; feil hvis en innkommende brukerdeskriptor gis denne vaulten.
- Å sette servereieren som requester eller bruke shared/default vault som reserve ved manglende klientbevis: F06 og `CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:929–939`.
- Å gjøre klientens eksisterende `.sign` til et generelt signeringsorakel: dagens permit gjelder bare en bestemt identitet og målcellens scope. En `.feed`-lease har ikke egen utløpstid, og permit er scope-basert, ikke bundet til konkret get/set-payload (`CP/Sources/CellBase/Cells/Bridging/BridgeIdentityProofAuthorization.swift:63–81`). Den er et begrenset origin-bevis, ikke en brukers godkjenning av alle handlinger mot den cellen. Ikke utvid den til kanalinnlogging, vilkårlige domener, meldinger eller tokenutstedelse. Behold eller stram inn klientens lokale scopes.
- Å logge eller persistére hele Identity-/challenge-/wireobjekter. Eksisterende decode-feillogg kan inkludere mottatt beskrivelse (`CP/Sources/CellBase/Cells/Bridging/BridgeBase.swift:954–960`), og visiting-registeret beholder wiremetadata (`CP/Sources/CellVapor/VaporIdentityVault.swift:2335–2341`). Ny auth-logging skal bare inneholde begrensede reason codes og korrelasjon, aldri hemmeligheter eller full pakke.

`BridgeIdentityVault` er en proxy som ber peer om et snevert bevis; den har ikke brukerens private nøkkel. Den kan ikke hente/utstede identiteter og feiler uten peer (`CP/Sources/CellBase/Identity/BridgeIdentityVault.swift:58–75`). Å la denne eksisterende proxyen støtte fortsatt cellebevis er ikke det samme som å gi prod et frittstående token som kan signere som brukeren. Hvis «ingen signeringsmulighet» skal bety at prod heller ikke kan be om senere origin-bevis, må alternativet med intern beviskontekst i §4 velges; serveren skal da ikke bruke en bruker-signervault overhodet.

Serverens egen TLS-nøkkel og egen tjenesteidentitet er separate fra brukeridentiteten. Ingen av dem skal kunne brukes som bevis for brukeren. Faktisk hemmelighetsbestand på vertene er **ikke lest**; denne rapporten viser at løsningen kan bygges uten brukerhemmeligheter på serveren, ikke at dagens verter er tømt for dem.

## 6. Anbefalt design — forslag, ikke eksisterende kode

### Håndtrykk og signert innhold

1. **Klienten velger mål før signering.** Den oppretter en lokalt initiert tilkoblingsoperasjon med forventet kanonisk WSS-origin, publisher, broId, domene og støttet auth-profil. Sertifikat/vertsnavn verifiseres. Ingen transporttoken kan erstatte brukerbevis.
2. **Begrenset oppgradering.** Serveren validerer ruteformat, eksponert lokal target og pre-auth-kvote. WS 101 betyr bare at auth-meldinger kan utveksles. Ingen resolveroppslag, celleregistrering, feed eller vanlig BridgeBase-kommando tillates ennå.
3. **Klient → server: hello.** Strengt offentlig deskriptor (UUID, algoritme, kurve, offentlig signeringsnøkkel), klientnonce, protokollprofil. Ett bevis for én identitet per fysisk forbindelse i første versjon. Multiplex kan senere dele samme beviste prinsipal; ny identitet krever ny forbindelse eller særskilt autentisert logisk kanal.
4. **Server → klient: challenge.** Kryptografisk tilfeldig nonce på minst 32 bytes, servervalgt sessionID/generation, issuedAt, kort handshake-utløp og deklarert absolutt kanalutløp. Signeringsdata har `type/version` fra challenge-formatet, `purpose = identity-origin-proof`, eksakt UUID/fingerprint, `action = openBridgeChannel`, og audience lik kanonisk WSS-origin+rute. Handlingen/publikummet er en ny eksplisitt profil, ikke `GeneralCell`-origin-profilen.
5. **Transcript-binding.** `domain` er det avtalte, lokalt forventede domenet. `resource` kan være en domeneadskilt SHA-256-digest av en kanonisk tuple: profil/versjon, origin/port, publisher, broId, begge noncer, sessionID, generation, retning, domene, nøkkelfingerprint og kanalutløp. Tuple og encoding må spesifiseres entydig; ikke strengkonkatener felter med en uescapet separator. Klienten rekonstruerer og kontrollerer tuple fra egen tilkobling/hello og serverens svar før den signerer utfordringens eksakte kanoniske bytes.
6. **Klienten signerer lokalt.** Bare denne aktive connect-operasjonen kan be egen vault signere `openBridgeChannel`. Ingen nøkkel eksporteres, ingen bruker-signeringstoken opprettes. Serveren mottar signatur og identifikator for sin pending challenge, ikke en klientvalgt «gyldig» utfordring som den erstatter pending-state med.
7. **Serveren verifiserer og konsumerer.** Streng format-/algoritmesjekk, identitetsmatch, eksakt transcript/forbindelse, lokal deadline og offentlig signaturverifikasjon. Atomisk overgang fra pending via verifying til authenticated; ny kontroll etter async-arbeid for lukking/revoke/generation. Bare én samtidig vinner. Alle avvik lukker med 1008; ressurs-/størrelsesfeil kan bruke egnet WS-feilkode. Ukjent/eldre auth-profil skal feile lukket, aldri falle tilbake til gammel ready-only bro.
8. **Server → klient: authenticated/ready.** Bekreft sessionID, prinsipal-fingerprint, profil og utløp over samme WSS-forbindelse. Først nå bindes requester og target, og normale kommandoer slippes til. Senere wire-identitet brukes bare til konsistenskontroll; ingen kommando kan omdefinere prinsipal. Cellepolicy evalueres ved hver operasjon og stream-leveranse som før.

Startforslag: challenge signeringsgyldighet 30 s (maks 60 s), pre-auth socket-deadline 10 s, kanalens absolutte auth-levetid 5 min med klientinitiert fornyelse. Dette er forslag som skal last- og brukstestes, ikke målte kapasiteter. Handshake-utløp og kanalutløp er ulike ting; det siste må også være bundet i transcriptet. Serverens lokale tid/deadline avgjør aksept selv om klientklokker avviker.

Ingen 0-RTT-auth eller muterende kommando i TLS early data. TLS 1.3 gir ikke iboende replayvern for 0-RTT; også klientretry kan duplisere applikasjonsmeldinger. Dette er begrunnelsen for forslaget, ikke en påstand om dagens TLS-oppsett: [RFC 8446 §8](https://www.rfc-editor.org/rfc/rfc8446#section-8).

### Hva serveren lagrer

- **Før auth, kun kortvarig:** Intern socket-ID/generation, kanonisk rute, begrenset offentlig deskriptor, challengebytes/transcripthash, noncer, deadline, status og kvotereservasjon.
- **Etter auth, i minne:** Uforanderlig offentlig prinsipal, domene, fysisk forbindelse/generation, godkjent auth-profil, tidspunkt/utløp, authEpoch/revokasjonsversjon, kanal-/inflight-/feedkvoter og eksplisitte ressursreferanser. Signaturen kan kastes etter verifikasjon; ikke gjør den til bearer-token eller varig autorisasjonscache.
- **Driftsdata:** Aggregerte tellere, avgrensede reason codes, build/profile-versjon og kortvarig korrelasjons-ID. Ikke full deskriptor, challenge, token, privat payload eller signeringstranscript i offentlig health/logg.
- **Ved disconnect/revoke/restart:** Ugyldiggjør hele generasjonen; kast pending, queues og autorisasjonsreferanser; frigjør kvoter; terminer callbacks; stopp feeds; fjern bare registreringene denne generasjonen eier. Reconnect betyr nytt bevis, ikke gjenbruk av gammel kanal-ID som credential.

Session-state inneholder verken brukerens private nøkkel, frittstående signeringsmulighet eller en vault som kan signere som brukeren. En intern requester-kontekst er verifikasjonsresultat, ikke en ny nøkkel eller nye cellerettigheter.

### Grenser og robusthet

Foreslåtte startgrenser, som må justeres ut fra målte scenarier:

- Per bevist `(domene, UUID, nøkkelfingerprint)`: 8 samtidige fysiske forbindelser, 16 logiske kanaler totalt, 32 samtidige celleoperasjoner, 16 aktive feeds og 12 handshake/fornyelsesforsøk per minutt med liten burst.
- Per uautentisert forbindelse: én pending challenge, auth-envelope maks 16 KiB, challenge maks eksisterende 8 KiB, ingen cellekommandoer i kø. Lukking ved 10 s uten fullført bevis.
- På instans/innløp: eksplisitt, konfigurert samlet socket-/pending-/CPU-/minnegrense; som første lasttestprofil 256 pending handshakes totalt og 4 per verifisert nett-kilde. Nett-kilde skal komme fra socket/betrodd proxy, aldri vilkårlig X-Forwarded-For. NAT og mange legitime brukere må måles før produksjonsverdi bestemmes.
- Rate-limit forsøk også før identitet er bevist; angriperen må ikke kunne låse ut et offer bare ved å oppgi offerets UUID. Selvgenererte nøkkelidentiteter kan omgå rene identitetskvoter, så globale/pre-auth-grenser er nødvendige.
- Avgrens WS-reassembly, dekoding, signaturverifikasjonskø, response-bytes og samlet ventende sendearbeid. Ikke kast brukte, fortsatt gyldige replayoppføringer for å gi plass; avvis nytt arbeid når lageret er fullt.
- Heartbeat og drain med målt reconnect innen formålets 30 s, ny autentisering ved reconnect og jitter for å unngå samtidige reconnect-stormer. Draining skal slutte å ta imot nye kanaler og avslutte gamle kontrollert. Ingen automatisk gjentakelse av uavklarte writes.

### /health/ready og utrullingsport

Foreslått struktur er `bridge: { required, routeRegistered, authProfile, verifierReady, sessionStoreReady, limitsConfigured, acceptingNewChannels, status, reasonCode }`. Top-level readiness må være falsk/503 når en påkrevd brokomponent er fraværende, auth kan omgås, eller instansen dreneres. Manglende felt er feil, ikke en kompatibel «ready». Prod/staging skal ikke kunne skjule dette ved å sette `required=false` uten en særskilt endring av release-policy.

Readiness er lokal komponentstatus; den kan ikke alene bevise offentlig proxy, DNS, sertifikat, rute og celleautorisasjon. Derfor en separat ekstern release-probe per miljø: faktisk WSS → signert handshake → begrenset beskyttet celleoperasjon → negativt forsøk uten bevis → disconnect/opprydding. Probeidentitetens private nøkkel skal ligge i ekstern klient/probeløper, ikke på målserveren og aldri være brukerens produksjonsnøkkel. Beviset skal merke app-SHA, CP-pin, profil, miljø og målte resultater. Kontrollen må stanse kandidat/promotering hvis ruten fjernes, hvis auth åpnes anonymt, eller hvis en gammel klient bare får 101 men ikke authenticated.

## 7. Fordeling mellom repoene

| Eier | Foreslått arbeid |
|---|---|
| **CellProtocol** | Kanonisk auth-profil og validering; lokal connect-signering; engangs pending/session-state med generation og revokasjon; uforanderlig requester-binding i dedicated/multiplex-dispatch; korrekt provenance på alle transportadaptere; strenge decode-/algoritmegrenser; eksplisitte transportfeil og reset; integrasjon med ordinær celleautorisasjon. Eventuell `VerifiedRequesterContext` og GeneralCell-støtte for kun ett bevis hører her. Ingen kontraktsrettigheter skal tildeles av transporten. |
| **CellScaffold** | Ny registrert `/bridgehead/<publisher>/<broId>` med gate før celleoppslag; canonical origin og proxy-policy; lokal eksponeringspolicy/rutekart uten requester-substitusjon; kvoter, drain/heartbeat, readiness og begrenset logging; discovery som bare annonserer reell og sikker rute; CI som booter faktisk applikasjon; oppdatert verifisert CP-pin. Native-porthole skal ikke få et nytt auth-unntak gjennom denne endringen. |
| **HavenAgentD og øvrige klienter** | Forstå auth-profil, initiere lokal signering og håndtere ny ready/reconnect; bevare eget nøkkelsted. Eksisterende endpointkonfigurasjon kan beholdes, men dagens klientkode kan ikke forventes å støtte et nytt håndtrykk uten oppdatering. Hvilke konkrete HAVEN/Binding-transportvalg som må oppdateres er **ikke lest**. |
| **Utrullingsansvarlig / HAVEN-Deploy** | Faktisk proxy-/backend-hardening, ekstern positiv/negativ probe, stans ved manglende route/auth, kontroll av SHA/pin, og bevis fra staging før prod. Her foreslås arbeid; ulest promoteringskode er ikke godkjent. |

## 8. Negative tester og bevis som må finnes før etterreview

Ingen tester er kjørt i denne lesejobben. Følgende er krav til implementeringens bevis, ikke rapporterte testresultater.

| Testgruppe | Negativt tilfelle og påkrevd observasjon |
|---|---|
| Første kommando / F01 | Manglende bevis, falsk ready, get/set/admit/description/feed/sign/response/openChannel før auth, ukjent auth-profil og feil rekkefølge: avvisning/1008 og **null** resolver-/cellekall. Samtidig proof og get må ikke slippe get før fullført atomisk overgang. |
| Identitetsforfalskning / F01,F06 | Offerets UUID med angriperens nøkkel; riktig UUID med feil fingerprint; riktig deskriptor uten privatnøkkel; A autentisert og B i neste kommando; nil/malformet identitet. Ingen oppgradering til owner eller servereier. Positiv kontroll med reell nøkkel og korrekt rettighet må lykkes. |
| Replay / F03 | Samme proof to ganger, parallelt på samme socket, på annen socket/kanal/publisher/broId/host/miljø/domene/generasjon, etter close/restart og på annen instans. Maks én aksept; ukjent pending-state avvises. Endret nonce, transcript, audience eller kanalutløp avvises. |
| Tid / F03,F04 | Utløpt challenge, issuedAt langt frem, altfor lang validity, lokal deadline utløper under verifikasjon, gammel kanalutløpstid og clock-skew. Tiden kontrolleres på nytt før installasjon; ingen arvet ready ved reconnect. |
| Proveniens / F02 | Kjør Vapor-main-testene `VaporBridgeTransportTests.swift:90–188` og tilsvarende wire-command/response-tester for Apple/Lightweight/multiplex med faktisk lokal nøkkel som kopieres. Ingen innkommende deskriptor får lokal vault, også uten delegate. Observer transportgrensen før BridgeBase-sanitering. |
| Signeringsorakel / §5 | Ubedt `.sign`, rå bytes, feil action/audience/domain/resource, feil principal, avsluttet lokal operasjon, feed-avslutning, disconnect og gammel permit under await. Ingen signatur; egen connect-lease kan bare signere eget eksakte åpnings-transcript. Ikke utvid eksisterende GeneralCell-permit for å få testen grønn. |
| Ingen serverhemmelighet / §5 | End-to-end med tom server-vault for klientidentiteten og reell signering kun på klienten. Instrumentert server-signer skal feile testen hvis den kalles for brukeridentiteten. Inspiser wire/persistens/loggartifakter med testnøkler: kun offentlig deskriptor/signatur, ingen privat nøkkel, token, vault eller private Identity-properties. |
| Autorisasjonsparitet / F06 | Samme get/set/execute/attach/feed kjøres lokalt og over bro med feil requester, feil keypath, feil permission, feil domene, tilbakekalt/utløpt kontrakt og `purpose://prompt.unknown`; lik avvisning. Eksakt gyldig grant åpner bare sitt scope. Purpose må testes i den faktiske målcellekontrakten; et felt i bridge-handshaken skal aldri gi myndighet. |
| Tilbakekalling / F04 | Tilbakekall én identitet/nøkkel/lenke/kontrakt mens to klienter er aktive. Nye handlinger og køet feed fra den berørte avvises; den andre fortsetter. Revoke under async verifier, cellekontroll og send må testes. Mål propagasjonstid og sluttpunkt for eventuelle allerede igangsatte handlinger. |
| TLS/proxy / F05 | Feil/utløpt sertifikat, feil vert, WS-nedgradering, endret Host/Forwarded-Proto, falsk discovery-utsteder, feil miljø/audience, uventet redirect og direkte backend-adgang. Ingen signering til uventet mål og ingen token over usikker ekstern transport. Faktisk proxykonfigurasjon inngår i beviset. |
| Kvoter / F07 | Kvote+1 sockets, pending challenges, logiske kanaler, inflight og feeds; mange selvgenererte nøkler; langsomme klienter; store/dype/fragmenterte pakker; gjentatte feil; samtidige disconnect/reservasjoner. Begrenset minne/CPU/task-antall og full frigivelse etter feil. Andre klienter beholder tjenesten. |
| Rute og release / F08 | Faktisk applikasjon uten route, uten verifier, uten obligatorisk lager, uten policy, med gammel ready-only handler: CI/readiness/ekstern promoteringsprobe skal bli rød. Native-porthole eller en HTTP-200 kan ikke gjøre dette grønt. |
| Robusthet / F10 | Brudd før/etter write, tapt svar, server-drain, reconnect, stale callbacks og duplisert svar: eksplisitt feil/ukjent resultat, ingen usynlig write-retry, frisk auth og målte ≤30 s reconnect under avtalt last. |
| Reelle klienter | CellResolver-standard, AD relay, AD correspondence, discovery og parity-fikstur, pluss faktisk HAVEN-app når kodeveien er identifisert. Hver må utføre autorisert celleoperasjon og et negativt forsøk i staging før prod. Ingen konklusjon bare fra mock-transport. |

Eksisterende testkilder gir nyttige regresjonsankre: scope-/leaseavslag i `CP/Tests/CellBaseTests/BridgeIdentityProofAuthorizationTests.swift:11–68`; to adskilte vaults og stengt signeringsmyndighet i `CP/Tests/CellBaseTests/BridgeIdentityBoundaryTests.swift:294–336`; feed-tilbakekalling i samme fil `:339–417`; og Vapor-proveniens i `CP/Tests/CellBaseTests/VaporBridgeTransportTests.swift:90–188`. Testpass, Linux/macOS-paritet og faktiske WS-resultater er **uverifisert i denne jobben**.

## 9. Leveringsgrense og neste kontroll

Denne forhåndsvurderingen er levert. Åpning av generell bro i prod er ikke godkjent av vurderingen. F01 og F08 stopper selve leveransen; F02–F07 og F09–F10 må ha rettelse eller eksplisitt risikobehandling, med testbevis i etterreview. Særlig må man ikke «løse» kanalbinding ved å gi serveren brukerens nøkkel, en lokal bruker-vault eller et bredere `.sign`-unntak.

Neste Astra-gjennomgang skal bruke konkrete CellProtocol-/CellScaffold-revisjoner, faktisk consumer-pin, endelig proxykonfigurasjon og positive/negative resultater for den implementerte kjeden. Uleste deler og antakelser ovenfor skal enten få evidens eller fortsatt stå som avgrensninger. Det er ingen ny forespørsel om G1-godkjenning; formålene er allerede godkjent av Kjetil.
