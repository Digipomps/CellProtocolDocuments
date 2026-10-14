# HD-0196 — plan og stopp ved opptaksgrensen

G1/G2 er godkjent 08.10 07:07Z for A med vilkårene i §6. Denne planen er kildebasert; ingen API eller test nedenfor er implementert. Leser: Codex h1.

## Konklusjon før kode

A kan ikke leveres med den krevde siste levende kontrollen ved faktisk nøkkelbruk gjennom dagens uendrede BrowserClientIdentityVault-API. Oppdragets stoppregel utløses. Ingen produksjonskode, arbeidstre, gren, push eller PR opprettes.

## Lest grunnlag og dataflyt

- Hele FORMAALSSPEC.md og STATUS.md i denne leveransen, inkludert autoritetskontrakt og T1–T8.
- Køreglene og relevante koordineringsinnlegg fra 07.10 21:00Z og senere, samt korrespondansens BOLK-4-RAPPORT.md. Sistnevntes resultater er rapporterte resultater fra s2, ikke kjøringer fra h1.
- Hele AdminBrowserBridgeIdentityVault.swift i korrespondansekandidaten: bind beviser possession; gammel signeringsvei kontrollerer existence/home, deretter await til source.signMessageForIdentity.
- CellProtocol origin/main, lokalt referansehode afa8cbf98f1b49dd8adee93f61a178b360afcc40: hele BridgeChannelClientOperation.swift. Public init/sign; kontroll før og etter await til vault; ingen connect-kontekst ved vault-grensen. Remote-ref er ikke hentet på nytt i denne økten.
- BrowserClientIdentityVault.swift: initialisering/actor og utvalgte funksjoner ensureVaultLoadedIfNeeded, loadVaultFromDiskIfAvailable, identityExistInVault, identityDomainBinding, signMessageForIdentity, signingPublicKeyMatches og signMessageForVaultIdentity. Signeringsfunksjonen er også lest direkte fra HD-0190-base d726890683d1ad0ccf0f0c70d290a1fb438f01cd, med samme kontrollflyt. Resten av vault-filen er ikke gjennomlest.

Dagens effektkjede er CP actor → adapter → await til strict-vault actor → eventuell async lasting → strict home/nøkkelkontroll → synkron privat signering. Den siste funksjonen mottar data og VaultIdentity; den mottar ingen operasjonsautoritet og sjekker verken avbrudd eller connect-deadline.

## Konkret problem med atomisk opptak

En planlagt CP-kontekst med låst active/deadline/consumed kan atomisk avvise eller konsumere i adapteren etter adapterens existence/home-await. Men deretter må adapteren kalle den andre actorens async signMessageForIdentity. Det er ikke en synkron nøkkelbruksgrense.

Mulig rekkefølge, utledet fra kode og ikke runtime-målt:

1. Adapteren ser aktiv kontekst og konsumerer.
2. Await til strict-vault venter på actor-eksekvering; eventuell lasting kan også vente.
3. Operasjonen avbrytes eller monotont deadline utløper før privat nøkkelbruk.
4. Strict-vaults uendrede metode kan likevel signere: den kjenner ikke konteksten og har ingen siste live-check.

En post-check kan forkaste signaturen, men kan ikke gi T5s null nøkkelkall. Å kalle steg 1 «faktisk nøkkelopptak» omdefinerer §5 og den godkjente autoritetskontrakten. Prewarming fjerner heller ikke actor-hopet. Task-kansellering er kooperativ og dagens vault sjekker den ikke. Å beholde en synkron lås over await er ingen akseptabel løsning: tilbakekalling blokkeres, deadline kan passere, og låsen ligger fortsatt utenfor nøkkelbruken.

## Alternativer til beslutning

1. **Behold sikkerhetsmålet; avgrenset endring i strict-vaultens signeringsinngang.** Nytt IdentityVaultProtocol-krav med BridgeConnectSigningContext og legacy-default. Strict-vault må etter siste await kontrollere/konsumere levende autoritet på sin egen actor umiddelbart ved synkron signering. Samme home/fingerprint-validering, nøkkelvalg og lagringsformat beholdes. Dette er en endring av strict-vault og krever endret oppdragsgrense; ikke autorisert her.
2. **Behold strict-vault uendret; endre opptakskontrakten.** Atomisk consume i adapteren betyr ugjenkallelig autorisasjon før async videresending, med post-check som stopper proof/aktivering. Dette tillater nøkkelbruk etter avbrudd/utløp som skjer etter adapterens consume og før signering. Det oppfyller ikke godkjent T5; bare aktuelt etter uttrykkelig endring av formålet.
3. **Større vault-/prosessgrense.** Flytt signing og levende admission sammen bak en ny kontrollert tjeneste. B/C alene løser ikke effekten dersom de fortsatt ender i det samme context-frie async vault-kallet. Større scope, ingen implementering foreslått som ferdig løsning.

Første alternativ bevarer det godkjente sikkerhetsmålet best. Ingen av alternativene er godkjent gjennom dette dokumentet.

## Arbeidspakker hvis grensen blir endret

Alle utføres av Codex; ikke startet. Ingen ny G1/G2 antas.

| Formål | Konkret arbeid | Verifikasjon |
|---|---|---|
| open | Godkjent holder-oppstart med privat beholdt capability; eksakt endpoint/principal/vault-binding. Transport får bare en operasjonsavgrenset autoritet fra denne inngangen. | T1 ekte handshake og konsumentens observer-flow |
| exclusive | Ikke-Codable context uten offentlig init; nytt protokollkrav for existential dispatch; ingen fallback etter strict-avslag. Public actor/sign og annen transport uten holder-capability får ikke gyldig utstedelse. | T2/T4/T8, ekstern modul uten @testable og positiv kontroll |
| lifecycle | Låst engangs-state med monotont deadline og terminal tilbakekalling; admission ved faktisk synkron nøkkelbruk etter siste await, forutsatt alternativ 1. | T3/T5, styrte barrierer og nøkkelkallteller, begge cancel-rekkefølger |
| paths | Legacy-default og eksisterende owner/runtime-token/origin-proof uendret. | T6 baseline og regresjon uten assert-endring |
| strict-storage | Samme strict principal/home, samme lagring, ingen capability på wire/disk. | T7 inspeksjon og tester |

API-navn og access-levels må sluttføres etter beslutningen, særlig hvordan adapteren eier holder-capability uten å eksponere en ny mintingvei gjennom public actor/transport. Ingen produksjonsgaranti hviler på denne uferdige API-skissen.

## Porter og koordinering

Etter løst stoppvilkår: eget CP-arbeidstre fra ferskt origin/main, fokusert rød/grønn i bane b; grunnmur gjennom wp-cellprotocol-grunnmur.sh som skriptjobb; reviewed push og kladd-PR med CI til grønn. Deretter eget CellScaffold-arbeidstre på d7268906 med eksakt CP-head, ekte T1/AdminNonOwnerBridgeTests og fullport etter banepolitikk. Milepæler appendes til KOORDINERING med backup og md5-kontroll. Ingen merge/tag/deploy.

Ingen bygg er kølagt nå: opptaksgrensen ble funnet før implementering, slik oppdraget krever.


## h2 — endelig API før kode (09.10.2026)

Alternativ 1 er autorisert av Kjetil 09.10 11:01Z («Ja, endre»), gjengitt i h2-oppdraget. h1-stoppet over er historisk, ikke gjeldende oppdragsgrense. Følgende er besluttet implementeringsdesign, ennå ikke implementert eller testet. CP-base er ferskt origin/main 97b348483448fb29dfe089bd96ab4d4adb384a76.

- `public final class BridgeConnectHolderCapability: @unchecked Sendable`: offentlig init lager et nytt, tomt prosesslokalt objekttoken. Det gir ingen myndighet i en eksisterende adapter. Adapteren oppretter og beholder nøyaktig ett token privat etter strict possession/home-validering, og aksepterer bare kontekster med samme objektidentitet. Ingen offentlig lookup, registrering eller getter returnerer adapterens token.
- `public func holderIdentity(_ identity: Identity) -> Identity` på tokenet lager en lokal identitetskopi med en CP-intern tokenreferanse. Tokenreferansen finnes verken i Identity.CodingKeys eller publicIdentitySnapshot. Nye selvlagde tokens på samme offentlige metadata avvises av adapterens objektsammenligning. Full autorisert holder-identitet er selve oppstartskapabiliteten; besittelse av den omfattes av §6 Q1, ikke offentlig descriptor.
- `public final class BridgeConnectSigningContext: @unchecked Sendable`, uten public init, Codable eller decoder. Internal init brukes bare av connect-actoren etter full transcript-validering. Den beholder eksakte signingData, principal UUID/fingerprint, endpoint og den private holder-tokenreferansen, samt låst active/consumed og monotont deadline. Offentlig `validate(holder:messageData:identity:endpoint:)` kontrollerer adapterens forventede token og eksakte binding uten consume. Offentlig synkron `consume(messageData:identity:) throws` er siste engangsopptak for strict-vault; internal `invalidate()` brukes ved cancel/finish/feil.
- Nytt **protokollkrav** `signMessageForIdentity(messageData:identity:bridgeConnectContext:) async throws -> Data`, med ikke-optional BridgeConnectSigningContext. Legacy-default delegerer til eksisterende krav. Ingen fallback ved context-avslag. Operasjoner uten holder-token følger eksisterende legacy-vei; strict adapter avviser alle openBridgeChannel-kall i gammel vei, også med korrekt home.
- BridgeChannelClientOperation fanger holder-token før den lager sitt offentlige principal-snapshot. Den oppretter høyst én context, sender den gjennom existential vault, og tilbakekaller den ved feil, cancel, finish og Task-kansellering. Context bindes til den allerede validerte operasjonens eksakte transcript-bytes og ti sekunders monotone deadline. Offentlig actor/transport med rekonstruert holder-snapshot har ikke tokenet og kan derfor ikke utstede kontekst som adapteren aksepterer.
- AdminBrowserBridgeIdentityVault beholder tokenet privat og legger det bare på den direkte returen fra sin eksisterende possession-validerte bind-vei. Protokollens offentlige identity(for:), identity(forUUID:) og addIdentity-returer får ikke tokenet; ellers ville oppslag med offentlig UUID blitt en ny mintingvei. Ny signeringsmetode sjekker eksakt token, principal, bridge-domain og endpoint fra validert challenge, før den videresender context og samme beholdte strict principal til source. Den konsumerer ikke før actor-hopet.
- BrowserClientIdentityVault har ny overload og en privat felles signeringsimplementering. Etter siste lasting-await gjentas home/fingerprint-valideringen, deretter context.consume, deretter eksisterende synkrone signMessageForVaultIdentity uten await mellom. Nøkkelvalg, private signeringsfunksjon og lagringsformat beholdes.

Testgrenser: T1–T8 fra §5 beholdes. Ny ekstern-modulfixture bruker `import CellBase` uten @testable. Styrte barrierer og nøkkelkallteller skal vise cancel-før-opptak = 0, opptak-før-cancel = 1 med tilbakeholdt proof, og ingen retry-myndighet. API-design er ikke leveransebevis før disse målingene og begge fullportene foreligger.

Testinstrumentering i strict signeringsinngang: kun DEBUG interne barrierer før siste admission og etter synkron signering, samt teller rett før eksisterende private signer. Ingen offentlig test-/mintinginngang, ingen Release-state eller lagringsfelt. Resolverens eksisterende lokale requester-kopi bevarer den interne tokenreferansen; offentlig snapshot er fortsatt uten den.


## h2 — målt implementeringsstatus ved stopp 09.10.2026

API-designet over er nå implementert i CP503f688 (PR65,grunnmur1671utførelser/5skip/0feil,CI5/5). Avgrenset konsument og strict-inngang er implementert i lokal CS83985fcb påd7268906,ikke pushet. Siste selected-kontroll:9tester/0feil,actual-source sisteadmission og ekte T1medtrewebfaser samt konkretlagringsfil verifisert.

Dette er ikke full konsumentleveranse:første samlede admin-fokus er rødt på eksisterende testRevocationStopsExistingOverviewFeed. Sammecapacity/timeout ble målt medoriginale CS-vaultfiler på både CP503ogmain97førh2. Den presise avvisningsgrenen er ikke fastslått. Reparasjonavtransport/kvoter/eksisterendeasserts ligger utenforalternativ1ogbleikkegjort. FullCS/#286-kopi ogCS-push/PR stopper her. RAPPORT-h2.md har STATUS:STOPPET ogTESTRESULT.md allekjørtekommandoer/feilkontroller.


## h3 — bestilt feilårsaksanalyse og fullføring (09.10)

Kjetils h3-oppdrag autoriserer bisekt, midlertidig diagnostikk og retting i repoen årsaken tilhører, inkludert eksisterende feed-fixture uten svekkelse av beviset. G1/G2 og signeringskontrakten beholdes. Ingen merge, tag, deploy eller installerbygg.

1. Eksakt d7268906-fixture mot CP afa8cbf før #63. Gjenta røde/grønne kontroller; bisekter #63-commitene dersom afa8cbf er grønn.
2. Observer konkret avvisningsgren, kommando og fase. Gjenopprett diagnostikk med kilde-MD5. `capacity` alene er ikke årsaksbevis.
3. Ved CP-regresjon: rød isolert CP-test først og retting på PR65-grenen. Ved fixturefeil: rett h2-arbeidstreet slik at autorisert levering, tilbakekalling av begge credential-typer, ingen videre feed-data og avvist lesing fortsatt bevises.
4. CP-grunnmur og CI hvis CP endres. Full CS-port på h2-treet før kladd-PR. Samme CP-hode og nødvendig CS-diff i separat #286-kopi; full 33/33 før push til #286.
5. RAPPORT-h3 og TESTRESULT med eksakte hoder, resultater og grenser; KOORDINERING-append med backup/MD5. Læringsfangst ved slutt.

Disk- og cachegrenser følger KOORDINERING regel 1–2. Første gate: 84,7 GiB ledig, 74,7 etter reserve, grønn. Dette avsnittet beskriver planlagt arbeid; resultater føres separat.


### h3 tillegg: sekundær socket-fixture-race funnet i fullport

Første kopiport32/33 feiler i person-bridge-fixturens socket setup. Uendrede fokusløp grønn/grønn/rød viser ustabilitet også ved0.776s, ikke bare buildlast. Valgt WebSocketKit-kilde90bbbdab3ede12c803cfbe91646f291c092517a3 viser at async connect starter onUpgrade i Task uten å vente på callbacken. Fixturen kan deretter sende auth før underlying er installert. Midlertidig25ms schedulerforsinkelse og grenmarkør skal bekrefte dette; MD5-restaurering kreves.

Foreslått retting etter rødt bevis: bare testtransportens setup bruker eksplisitt EventLoopFuture<Void> og synkron onUpgrade; awaitfuture.get etter installering. Ingen assertion, nøkkelautoritet, protokoll-/wire-kode, kvote eller deadline endres. Begge CS-kandidater får samme kilde. Ny fokus og komplett32/32 +33/33 på nye committede hoder kreves før de publiseres. Første rødeporter beholdes; grønne bolker skal ikke sys sammen mellomkjøringer.


Presisering før implementering: NIOHTTPClientUpgradeHandler kaller upgradeCompletionHandler før upgrader.upgrade. Bare bytte til synkron callback er derfor ikke en tilstrekkelig readiness-kontrakt. Foreslått fixturekode beholder async callback men venter på egen EventLoopPromise<Void>, fullført først etter atomisk transportinstallering. Close feiler en eventuell pendingpromise og avviser sen installering. Ingen ekstra ventefrist eller retry; opprinnelig CP-auth-deadline gjelder fortsatt.


### h3 byggobservasjon — ingen kvoteendring

Ny fullport påda7313fd har infrastrukturrød bolk10: bare diskguard logget, ingen test kjørt. Own wrapper har ubevoktet du|awk underpipefail; eksisterende #286-wrapper håndterer cache-GC under måling og er ellers byte-identisk. Kontrollert shellprobe viser oldexit1/no runner, eksisterende copyexit0/runner invoked/metricunknown, og copybevarer runnerexit7. Ingen ekte Swift-jobb er simulert som grønn fullport; dette er separat feilinjeksjon på observasjonsmåling.

Etter aktivport er ferdig: port kopiens eksisterende wrapper til own, med helt uendrede kapasitet-/reserve-/jobs-/cachegrenser og fortsatt eksakt runnerstatus. Commit nytt ownhode, ny komplett32-port og så kopiens33-port. Ingen endring av aktive shellfiler.


### h3 gjennomført sluttstatus

Endelig testtransport bruker både synkron callback på socket-eventloop og separat readinesspromise; connect-futuren alene er ikke readiness. Cacheobservasjonsguard portert etter avsluttet kjøring. Nye komplette porter32/32 og33/33 er kjørt på sluttcommits og publisert som kladd307/oppdatert286. G3-akseptanse/release er ikke gitt. RAPPORT-h3.md og TESTRESULT.md inneholder faktiske hoder, resultat og avvik; tidligere planalternativer ovenfor er historiske.
