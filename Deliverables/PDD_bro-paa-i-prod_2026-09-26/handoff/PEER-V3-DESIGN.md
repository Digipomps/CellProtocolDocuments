STATUS: LEVERT — mønster: SIGMA-I, tilpasset lokale signeringsvaults, med to Finished-meldinger

Astra · 2026-09-28 · N22 i CellProtocol PR #53 · normativ implementeringsdesign for kontroll 5.

**Leveransegrense.** Dette dokumentet spesifiserer v3; det beskriver ikke ferdig implementasjon eller beståtte v3-tester. Ingen kode, commit, push, merge eller produksjonsgodkjenning inngår. «SKAL» og «SKAL IKKE» nedenfor er krav til implementasjonen. Alle 13 funn N10–N22 skal fortsatt rettes før merge, etter Kjetils beslutning. V3 alene lukker ikke de andre funnene.

**0. Fastlåst grunnlag**

GitHub rapporterte PR #53 som OPEN med head **`605298fe404d46827100559a862ec2e9b1978fc8`** ved designarbeidets start. CP-kildene nedenfor er lest med `git show` fra dette commitobjektet, ikke fra arbeidstreet. Kontroll 4 vurderte `1b8efe1cbca33997facf50a37ee0fbfff9dc7b14`. Ny head inneholder N17/N19-endringer; av de seks særskilt bestilte CP-filene er bare `BridgeChannelSession.swift` endret mellom disse revisjonene. Dette er ingen ny full kontroll av N17/N19.

| Lest grunnlag | Bane relativt til HAVEN-roten |
| --- | --- |
| Kontroll 4, særlig N22 og §§3–4 | `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/ASTRA-ETTER-CP53-4.md` |
| V2-kontrakt | `CellProtocol/Documentation/BridgePeerChannelV2.md` |
| Peer-operasjon | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgePeerChannelAuthentication.swift` |
| Record-lag | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgePeerRecordLayer.swift` |
| Gate | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelTransport.swift` |
| Sesjon og kvoter | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeChannelSession.swift` |
| Lokal signeringskontrakt | `CellProtocol/Sources/CellBase/Identity/IdentitySigningChallenge.swift` |
| Supplerende, samme head | `BridgeChannelAuthentication.swift` og auth-relevant codec i `BridgeCommand.swift` i samme Bridging-mappe, `IdentityPublicKeySignatureVerifier.swift` i samme Identity-mappe, relevante invitasjons-/adapter-/livsløpsutdrag av `CellProtocol/Sources/CellApple/EntityRadar/ScannerService.swift`, og `CellProtocol/SECURITY.md` |

**1. Valg, mål og tillitsgrense**

Velg **SIGMA-I**: efemær DH, signatur over utvekslingskontekst, separat DH-avledet MAC som binder signerens identitet til utvekslingen, og kryptering av autentiseringsfeltene. Responder autentiserer først; initiator røper sin identitet etter kontroll av responder. Dette passer signeringsnøkler i lokal vault uten eksport, konvertering til DH eller en ny statisk DH-identitet. Mønsteret og den asymmetriske identitetsbeskyttelsen bygger på [Krawczyks SIGMA, §§2.2, 5.1–5.2](https://iacr.org/cryptodb/archive/2003/CRYPTO/1495/1495.pdf).

Noise XX bruker statiske DH-nøkler og DH-tokenene `es`/`se`. Å bytte disse mot signaturer er en egen konstruksjon, ikke standard Noise XX med arvede testvektorer. Noise er nyttig som sammenligningsgrunnlag, men ikke wireprotokollen her. [Noise, §§7.5–7.8](https://noiseprotocol.org/noise.html#interactive-handshake-patterns-fundamental).

Denne profilen er **en konkret SIGMA-I-basert instansiering**, med CP-encoding, kontekstsignaturer, retningsbestemte nøkler, padding og to Finished-meldinger. Den er ikke IKE, TLS eller Noise-kompatibel. SIGMA-familiens analyse er begrunnelsen for mønsteret; den er ikke et formelt bevis for denne nye instansieringen, parseren eller Swift-livsløpet. Ingen påstand om absolutt fravær av sårbarheter følger av designet.

Beskyttet ressurs er opptak til én kryptert peer-kanal og dens identitetsfelt. Kontroll av den erklærte signeringsnøkkelen gir en kanalprincipal. Resolver, Agreement, Grant, origin-proof og celleeierkontroll er fortsatt autoritetsgrensen for cellehandlinger. Endpoint-/discovery-navn, invitasjonsaksept og deltakelse i DH beviser ikke en person, enhet eller rettighet.

**2. Fast profil og lokal kontekst**

- `P = "org.haven.bridge-peer-channel.v3"`; action er fortsatt `openPeerBridgeChannel`.
- Fast suite: X25519, HKDF-SHA256, HMAC-SHA256 og ChaCha20-Poly1305 med full 16-byte tag. Ingen suiteforhandling, resumption, PSK, 0-RTT, early data eller nøkkeloppdatering innenfor denne profilen.
- Signeringsalgoritmen følger den lokale identiteten. Tillatte par er nøyaktig v2s EdDSA/Curve25519 og ECDSA/P256. Algoritme, kurve og offentlige nøkkelbytes er del av den krypterte og autentiserte identitetsdeskriptoren; de er ikke et forhandlingstilbud.
- Roller `I = initiator`, `R = responder` bestemmes av den aksepterte invitasjonen før M1. Ingen rollebytte eller automatisk retry som motsatt rolle etter feil.
- `E = Endpoint{initiator,responder,setupID,domain}` beholdes med v2s validering: ulike, ikke-tomme initiator/responder på høyst 512 UTF-8-bytes hver, ikke-tomt domain på høyst 512 bytes, gyldig UUID som setupID. Samme eksakte E må allerede være frosset lokalt hos begge parter fra invitasjonen. Mottatt E kan bare sammenlignes med dette; det kan ikke erstatte lokal E.
- Nye setupID og lokale kanalgenerasjoner for hver utveksling. V3-generasjon og nygenerert setupID serialiseres som store ASCII-heksadesimalsifre i UUIDs 36-tegns bindestrekformat. Generasjonene må være forskjellige. N08s lokale transportinstans-ID er et eget begrep; den må ikke forveksles med den felles E.setupID.
- Fersk X25519-privatnøkkel og tilfeldig 32-byte nonce per rolle og forsøk; ingen cache/gjenbruk. Identitetens signeringsnøkkel brukes aldri i DH eller som krypteringsnøkkel.
- Signeringsidentitet hentes fra lokal eier/vault, aldri fra en innkommende signeringsforespørsel. `BridgeIdentityVault` er forbudt som signer i håndtrykket. Bare offentlige nøkkeldata går til verifikator; ingen mottakerverifikasjon spør en vault om signeringsmyndighet.

Fysisk binding er en uforanderlig lokal tuple: **akseptert invitasjonsinstans, E, rolle, fysisk peer-objekt, MCSession-objekt, adapterinstans, gate og kanalgenerasjon**. Objektbindingen er lokal og kan ikke erstattes med en wire-streng. MC-kryptering kreves fortsatt. N11 må fryse pending/accepted-bindingen før discovery-loss eller ny discovery kan påvirke den.

**3. Bytekontrakt, størrelser og synlighet**

Notasjonene her er normative:

| Symbol | Eksakt betydning |
| --- | --- |
| `U(s)` | UTF-8-bytes av strengen s; ingen avsluttende NUL |
| `U16(n)`, `U32(n)`, `U64(n)` | Usignert heltall i henholdsvis 2, 4 og 8 bytes, big endian |
| `LP(b)` | `U32(b.count) \|\| b` |
| `F(label,b1,…,bn)` | `LP(U(P)) \|\| LP(U(label)) \|\| U32(n) \|\| LP(b1) \|\| … \|\| LP(bn)` |
| `H(b)` | SHA-256, rå 32-byte digest |
| `hex(b)` | Små heksadesimalsifre, to tegn per byte |
| `C(value)` | Eksakt UTF-8 JSON fra `BridgeChannelAuthentication.encode`: sortedKeys, withoutEscapingSlashes, Data som standard base64 med padding og uten linjeskift |
| `Envelope(name,body)` | `C(BridgeCommand(cmd:name, payload:.string(UTF8(C(body))), cid:0))` |

Alle wire-envelopes må være byteidentiske ved decode→encode. De eksakte ytre JSON-nøklene er **`&string`, `cid`, `cmd`**: `&string` inneholder JSON-teksten C(body), `cid` er tallet 0 og `cmd` er trinnets faste navn. Dette er eksisterende BridgeCommand-codec for `.string`; det finnes ikke et wirefelt kalt `payload`. Alle andre felt skal være fraværende, inkludert identity, transportmetadata med `&`-prefiks, alternative payload-typer og error. Ukjente eller dupliserte felt, ekstra null-felt, alternative tall/base64-encodings, whitespace og etterfølgende bytes avvises; dette gjelder også JSON inni payload og dekryptert JSON. Bruk strenge typede strukturer, ikke en dictionary som beholder ukjente felt. Rå wirebytes beholdes bare bounded i den aktive operasjonen for transcript-beregningen. `||` betyr bytekonkatenering, `UTF8(C(body))` betyr tapsfri konvertering av JSON-bytes til String, og NUL er byteverdien null.

En identitetsfri hello `H_s` har nøyaktig:

```
{profile, role, ephemeralPublicKey, nonce, generation, issuedAtMilliseconds}
```

`profile=P`; `role` er eksakt riktig rolle; DH-public og nonce er Data på 32 bytes; tid er ikke-negativ Int64, hele millisekunder. Ingen E, identitet, fingeravtrykk, identitetshash, certificate, navnehint eller liste over signeringsalgoritmer ligger i hello. R offentliggjør H_R sammen med sin krypterte blokk. E inkluderes bare inne i krypterte autentiseringsblokker; heller ikke en hash av E sendes i klartekst.

Begge helloer valideres før DH/signering: forventet profil/rolle, lengder, UUID-format, remote generation forskjellig fra lokal, og `nowWallMS−10_000 < remote.issuedAtMilliseconds <= nowWallMS+5_000`, med overløpssikker aritmetikk. Tid sjekkes ved mottak, ikke gjenfortolkes ved hvert senere trinn. Håndtrykket må i tillegg fullføres før operasjonens opprinnelige 10-sekunders monotone frist og før `min(t_I,t_R)+30_000` etter veggklokken; meldinger forlenger ingen frist. Aktiv kanal utløper senest `min(t_I,t_R)+300_000`, med både monoton og veggklokkebasert sjekk som i v2.

`PublicIdentity` beholder nøyaktig `{uuid,algorithm,curve,publicKey}` og v2s validering. EdDSA bruker 32-byte offentlig representasjon og 64-byte signatur. P256 tillater provider-validerte 33-byte komprimerte eller 65-byte X9.63 offentlige representasjoner og DER-signatur, høyst 256 bytes. De **faktisk sendte** representasjonene bindes i transcript/signatur. Ikke normaliser dem etter signering; kanonisering for N17s kvotenøkkel skjer separat. Ingen properties, displayName, grants, vaultreference, privatnøkkelflagg eller DH-identitetsnøkkel inkluderes.

For å skjule deskriptor-/signaturlengde defineres:

```
Pad_N(value) = U32(C(value).count) || C(value) || zeroBytes(N−4−C(value).count)
```

M2/M3 bruker N=8192. M4/M5 bruker N=1024. Lengden må være 1…N−4; ellers avvises lokalt, uten variabel padding eller ekstra pakker. Ved åpning kreves eksakt N bytes, korrekt lengde, kanonisk JSON og bare nullbytes i resten. Dermed er `sealed` eksakt 8208 bytes i M2/M3 og 1040 bytes i M4/M5, inkludert tag. Padding ligger **inni** AEAD; det finnes ingen kompresjon. Dette er en eksplisitt v3-grense: ellers gyldige v2-strenger som ikke passer den faste auth-blokken kan ikke sendes i v3. Test denne grensen før utrulling; ikke utvid blokken dynamisk etter identitet.

Hele `Envelope` har fortsatt maksimum 16 384 bytes, kontrollert før JSON-dekoding/allokering av større innhold. M1 har i tillegg maksimum 2048 bytes. Paddingstørrelsene inkluderer ikke base64 og JSON; faktisk ferdig wirelengde regnes i kvoten. De fastsatte blokkene skal testes mot begge plattformenes encoder og totalgrensen. Detaljerte decode-/policy-/signeringsfeil returneres ikke på wire; terminal close er eneste feilrespons.

**4. Transcript og nøkkelplan**

La Wj være **eksakte kanoniske bytes for hele Envelope i Mj**, inkludert ciphertext og tag der de finnes. Det finnes ingen selvrefererende hash; alle formler bruker bare allerede tilgjengelige bytes:

```
T1  = H(F("wire-1", W1))
T0  = H(F("clear-2", T1, C(H_R)))
T2  = H(F("wire-2", T0, W2))
T3  = H(F("wire-3", T2, W3))
T4  = H(F("wire-4", T3, W4))
T5  = H(F("wire-5", T4, W5))
```

Navnet T0 betyr pre-auth-kontekst etter **begge** helloer, ikke hash før M1. T0 binder begge efemære public keys, noncer, generasjoner, tider, roller, profil og M1s envelope. T2 legger til hele responders krypterte autentisering. T3 legger til hele initiators krypterte autentisering. T4/T5 legger til Finished i riktig rekkefølge. T2–T5 og identitetsavhengige digests skal ikke eksporteres i klartekst eller logger. Hash av ciphertext binder de eksakte sendte, autentiserte feltene; signaturene konstrueres over de eksplisitte kontekstene i §5, ikke over fremtidig ciphertext.

```
Z   = X25519(localEphemeralPrivate, remoteEphemeralPublic)
PRK = HKDF-Extract-SHA256(salt=T0, IKM=Z)

K(label, direction, context) = HKDF-Expand-SHA256(
    PRK,
    info=F("kdf", U(label), U(direction), context, U16(32)),
    L=32)
```

X25519 bruker providerens RFC 7748-semantikk. Providerfeil og all-zero Z er terminale. Ekstrakontrollen OR-er alle bytes uten tidlig retur. De mottatte public-key-bytes inngår uendret i hello/transcript selv om X25519-provider aksepterer ekvivalente inputrepresentasjoner. Ikke bruk public DH som principal. Dette følger kontrollbehovet i [RFC 7748, §§6.1 og 7](https://www.rfc-editor.org/rfc/rfc7748#section-6.1).

Hver rad avleder **to** 32-byte nøkler, én for hver av de eksakte direction-strengene `initiator-to-responder` og `responder-to-initiator`:

| Variabel | HKDF-label | context | Bruk |
| --- | --- | --- | --- |
| `Khs[d]` | `handshake-key` | T0 | AEAD for M2–M5, aldri appdata |
| `Kid[d]` | `identity-mac-key` | T0 | HMAC på egen autentiseringsblokk i M2 eller M3 |
| `Kfin[d]` | `finished-key` | T3 | Finished-HMAC i M4 eller M5 |
| `Kapp[d]` | `application-key` | T5 | App-/kontrollrecords etter håndtrykket |

PRK og context er forskjellige typer: PRK er hemmelig og skal aldri serialiseres. HKDF-info binder profil, formål, retning, transcript og lengde. Dette er en konkret bruk av [RFC 5869, §§2–3](https://www.rfc-editor.org/rfc/rfc5869#section-3.2); det er ikke TLSs HKDF-Expand-Label.

Håndtrykks-AEAD bruker `nonce = zeroBytes(4) || U64(counter)`. Telleren er implisitt og bestemt av trinnet:

| Melding | Nøkkel | counter | AAD |
| --- | --- | --- | --- |
| M2 | Khs[R→I] | 0 | `F("handshake-aead", U("2"), T0)` |
| M3 | Khs[I→R] | 0 | `F("handshake-aead", U("3"), T2)` |
| M4 | Khs[R→I] | 1 | `F("handshake-aead", U("4"), T3)` |
| M5 | Khs[I→R] | 1 | `F("handshake-aead", U("5"), T4)` |

`sealed = ciphertext || tag`; ingen nonce sendes. Eksakte trinn/roller bestemmer tillatt nøkkel; aldri prøv flere nøkler eller eldre profiler etter åpnefeil. Hver utgående melding forsegles høyst én gang. Ingen håndtrykksretransmisjon eller omkryptering i samme operasjon; feil krever ny invitasjons-/kanalgenerasjon og nytt DH. Mottatt duplikat er terminalt. Full tag og unik nonce per nøkkel følger [RFC 8439, §§2.8 og 4](https://www.rfc-editor.org/rfc/rfc8439#section-2.8).

DH-privatreferansen og Z slippes etter ett derive-forsøk, også ved feil. Kid kan slippes etter identitetsutvekslingen. PRK, Khs og Kfin slippes etter vellykket M5/avledning av Kapp, eller ved enhver terminal overgang. Bare Kapp per retning blir igjen i record-laget. Ingen nøkkeleksport, persistens eller Codable-nøkkelholder. Dette er livsløpskrav; det påstår ikke attestert nullstilling av alle Swift-/provider-/OS-minnekopier.

**5. Signaturer og identitets-MAC**

Følgende er lokale signaturkontekster, ikke selvstendige wiremeldinger. Feltnavn og fravær er bindende. Det brukes ikke v2s `Transcript` med identiteter i begge helloer.

```
D_R = {profile:P, signer:"responder", helloDigest:hex(T0),
       endpoint:E, identity:Id_R}
D_I = {profile:P, signer:"initiator", helloDigest:hex(T0),
       previousDigest:hex(T2), endpoint:E, identity:Id_I,
       peerIdentity:Id_R}
d_R = hex(H(C(D_R)))
d_I = hex(H(C(D_I)))
```

For signer s bygger operasjonen selv en `IdentitySigningChallenge` med:

| Felt | Eksakt verdi |
| --- | --- |
| type/version/purpose | Eksisterende `IdentitySigningChallenge` type, version=1, purpose=`identity-origin-proof` |
| identityUUID | Id_s.uuid |
| publicKeyFingerprint | Eksisterende `Id_s.makeIdentity().signingPublicKeyFingerprint`, beregnet fra akkurat deskriptoren som signeres |
| domain | E.domain |
| resource | P + `:` + d_s |
| action | `openPeerBridgeChannel` |
| audience | P + `:` + hex(H(C(E))) |
| nonce | Motpartens hello-nonce, n_I for R og n_R for I |
| issuedAt | `Date(timeIntervalSince1970: Double(min(t_I,t_R))/1000)` gjennom eksisterende constructor |
| validity | 30 sekunder; expiresAt bestemmes av constructor |

`signingData = C(challenge)`. V3 bruker altså encoder uten slash-escaping også her, eksplisitt forskjellig fra v2s lokale `.sortedKeys`-encoder for signeringsdata. `IdentitySigningChallenge`-typen og vault-API-et trenger ingen semantisk endring: `validateSigningData` validerer innhold, og vault signerer de leverte bytes. Verifikator rekonstruerer akkurat samme bytes. Integer-millisekunder→TimeInterval og JSONs tidsrepresentasjon skal låses med macOS/Linux-vektorer, også for brøkdelen av et sekund. V3s strengere frister gjelder selv om den generelle challenge-validatoren tillater større clock skew.

Fingeravtrykket i dagens kontrakt er en algoritme/kurve/base64-streng, ikke en ekstra SHA-256-identitet. Det forblir inni lokalt konstruert signeringsdata og krypterte sammenhenger. Ingen caller kan sende vilkårlig `signingData` til håndtrykksoperasjonen.

Signer utfører lokal challenge-validering, lokal vault-eksistenssjekk og én signering. Det returnerte resultatet verifiseres mot egen offentlige deskriptor og valideres på nytt mot tid/livsløp før det kan sendes. Liveness-reglene i §8 gjelder etter **hvert** await, også vault-eksistenssjekken. Det er bare én identitetssignering per rolle per utveksling.

```
Proof_R = {sessionID:E.setupID, generation:H_I.generation, signature:Sig_R}
Proof_I = {sessionID:E.setupID, generation:H_R.generation, signature:Sig_I}
Core_R  = {endpoint:E, identity:Id_R, proof:Proof_R}
Core_I  = {endpoint:E, identity:Id_I, proof:Proof_I}

mac_R = HMAC-SHA256(Kid[R→I],
    F("identity-mac", U("responder"), T0, C(Core_R)))
mac_I = HMAC-SHA256(Kid[I→R],
    F("identity-mac", U("initiator"), T2, C(Core_I)))

Auth_R = {endpoint:E, identity:Id_R, proof:Proof_R, identityMAC:mac_R}
Auth_I = {endpoint:E, identity:Id_I, proof:Proof_I, identityMAC:mac_I}
```

MAC er rå 32-byte Data i JSON. Begge MAC-er binder egen identitet, eget proof og endpoint til DH og riktig trinn/retning. De erstattes ikke av AEAD-tag eller signatur. Sammenligning av MAC/Finished bruker providerens konstanttidsverifikasjon.

En bevisst forskjell fra v2: R kan ikke signere I-identiteten i M2 uten at I allerede har røpet den. R signerer begge helloer og egen identitet; I signerer dessuten R-identiteten og T2. R binder deretter hele tosidige utvekslingen, inkludert I-identiteten, med Finished over T3. Kapp binder T5. **Sluttegenskapen er gjensidig identitets-/nøkkel-/transcript-binding; påstanden «begge identitetssignaturene inneholder begge identiteter» videreføres ikke.** Ingen ekstra R-signering eller endring til statisk DH skal smugles inn for å beholde den gamle strukturformen.

**6. Eksakt femmeldingsflyt og aktivering**

`Seal` i tabellen bruker nøkkel/nonce/AAD fra §4 og returnerer ciphertext||tag. De fem command-navnene er nye, eksakte og disjunkte fra v1/v2 og WS. Alle body-skjemaer har bare de oppgitte feltene.

| Nr. | Retning og command | Body i ytre, kanonisk Envelope | Kryptert plaintext |
| --- | --- | --- | --- |
| M1 | I→R `channelAuthPeerV3Hello` | H_I | Ingen |
| M2 | R→I `channelAuthPeerV3ResponderAuth` | `{hello:H_R,sealed:Seal(Pad_8192(Auth_R))}` | E, Id_R, Proof_R, identitets-MAC og padding |
| M3 | I→R `channelAuthPeerV3InitiatorAuth` | `{profile:P,sealed:Seal(Pad_8192(Auth_I))}` | E, Id_I, Proof_I, identitets-MAC og padding |
| M4 | R→I `channelAuthPeerV3ResponderFinished` | `{profile:P,sealed:Seal(Pad_1024(Finished_R))}` | Ack_R, Finished-MAC og padding |
| M5 | I→R `channelAuthPeerV3InitiatorFinished` | `{profile:P,sealed:Seal(Pad_1024(Finished_I))}` | Ack_I, Finished-MAC og padding |

Finished defineres slik:

```
Ack_R = {sessionID:E.setupID, generation:H_R.generation, transcriptDigest:d_I}
Ack_I = {sessionID:E.setupID, generation:H_I.generation, transcriptDigest:d_R}

verify_R = HMAC-SHA256(Kfin[R→I], F("finished", U("4"), T3, C(Ack_R)))
verify_I = HMAC-SHA256(Kfin[I→R], F("finished", U("5"), T4, C(Ack_I)))

Finished_R = {ack:Ack_R, verifyData:verify_R}
Finished_I = {ack:Ack_I, verifyData:verify_I}
```

Ack bevarer v2s betydning: avsender er verifier for det mottatte identitetsproofet; `generation` er derfor **ack-avsenderens** generasjon. Mottaker kontrollerer ack mot sin egen tidligere signerte kontekst. Finished-HMAC dekker i tillegg hele forutgående wire-transcript. Separate Finished-nøkler og HMAC på transcript er også et etablert konstruksjonsgrep i [TLS 1.3, §4.4.4](https://www.rfc-editor.org/rfc/rfc8446#section-4.4.4); v3 kopierer ikke TLSs håndtrykk eller nøkkelplan.

**M1 / responder.** Gate og pending-/arbeidskvote finnes før M1 behandles. R krever rett transportinstans og rolle, validerer W1/H_I og bruker sin allerede opprettede H_R. R gjør ett DH/Extract-forsøk, bygger D_R med lokal E og Id_R, signerer lokalt, bygger mac_R og sender M2. R kjenner ingen verifisert remote identity ennå. Det opprettes **ingen** remote principal, per-key-bøtte, aktiv session eller Base på grunnlag av DH eller M1. R venter bare på M3.

**M2 / initiator.** I validerer envelope/H_R, beregner T0 og avleder handshake-/identitets-MAC-nøkler. Før plaintext tas i bruk kreves gyldig AEAD, korrekt padding og strengt Auth_R-skjema. I krever E byte-/feltlik lokal frosset E, riktig sessionID og verifier-generation, gyldig PublicIdentity, korrekt mac_R og gyldig Sig_R over **lokalt rekonstruert** D_R/challenge. Ingen wire-levert challenge godtas. Per-key-opptak reserveres først etter korrekt MAC og signatur. I utfører deretter lokal responder-/røpingspolicy (§7) og livsløpssjekk. **Først nå** bygger og signerer I D_I, konstruerer mac_I og sender M3. Før dette punktet sendes ikke noe identitetsavhengig I-felt, heller ikke en hash eller feiltekst. I venter bare på M4.

**M3 / responder.** R åpner med Khs[I→R], counter 0 og T2-AAD; validerer padding, skjema, lokal E, proof-binding, Id_I, mac_I og Sig_I. D_I rekonstrueres med Rs egen Id_R og lagrede T0/T2. Feil i en av kontrollene er terminal, også om AEAD eller en isolert signatur er korrekt. R reserverer den verifiserte nøkkelkvoten/principalen, utfører lokal peer-policy og revaliderer etter await. Deretter beregnes T3 og Kfin; R bygger Ack_R/verify_R og sender M4. R forblir ikke-aktiv og venter bare på M5. Ingen Base-factory, appdata eller NI-broadcast kan starte her.

**M4 / initiator.** I åpner, validerer Ack_Rs tre felt og verify_R mot T3, og beregner T4. I revaliderer levetid, binding og policy. I bygger Ack_I/verify_I og W5, forsegler én gang og sender M5 med reservert bytekvote. Etter vellykket lokal innlevering, ny livsløpssjekk og beregning av T5 kan I avlede/installere Kapp, aktivere session og starte factory. Etter factory-await revalideres samme session/transport før delegate og `peerReady` publiseres. I har mottatt Rs nøkkelbekreftelse; I vet på dette tidspunktet **ikke** at R har mottatt M5.

**M5 / responder.** R åpner, validerer Ack_I og verify_I mot T4, beregner T5, revaliderer og avleder/installere Kapp. Først da kan session aktiveres og factory startes med samme etter-await-kontroll som hos I. En holdt M5 hindrer R-factory og enhver appdispatch. R må ikke bli aktiv bare fordi I sendte et korrekt proof i M3.

Kvittert nøkkelbesittelse og begge identitetsproof må altså foreligge lokalt før aktivering. At siste avsender ikke vet om siste melding er levert er samme siste-meldingsgrense som i v2, ikke felles kunnskap om at begge applikasjoner er klare. N18s leveringskvitteringer er et eget formål (§9).

Hver operasjon bruker eksplisitte tilstander, ikke lister over tillatte plaintext-sends:

```
I: created → sentM1/waitM2 → verifiedR/signingI → sentM3/waitM4
   → verifiedFinishedR/sendingM5 → activating → active → terminal
R: created/waitM1 → signingR/sendingM2 → waitM3
   → verifiedI/sendingM4 → waitM5 → activating → active → terminal
```

Inngang til signering/verifikasjon/sending reserveres atomisk før await. Et duplikat får ikke starte en andre operasjon. Kun neste forventede wiremelding tillates; ingen buffering av en fremtidig auth-melding for senere godkjenning. Den ordnede, bounded mottakskøen kan beholde bytes som ankommer mens forventet melding behandles. Køen må fullføre auth-behandlingen før den åpner neste frame. Etter aktivering er alle auth-command-navn forbudt i begge retninger, også inne i en gyldig app-record. Enhver feil i state, AEAD, MAC, proof, policy, deadline, kapasitet eller transport gjør tilstanden terminal; samme gate gjenåpnes aldri.

Bare peer-operasjonen kan bygge og forsegle W2–W5. Adapteren får de ferdige bytes gjennom gatens interne auth-sendsti og kontrollerer at de er den eksakte, engangsreserverte meldingen for fanget operasjon/trinn før fysisk innlevering. Den skal verken forsegle dem en gang til med Kapp eller godta vilkårlige «allerede krypterte» auth-bytes fra offentlig `sendData`. Mottatt W2–W5 går bare til denne operasjonens åpning/validering; dekryptert Auth/Finished sendes aldri til vanlig BridgeCommand-/celle-dispatch.

**7. Identitetsvern og eksplisitt røpingspolicy**

V3 krever at I før M3 både verifiserer nøkkelkontroll og tar en **lokal, eksplisitt beslutning om at denne R-identiteten kan motta Id_I**. Peer-konstruktøren skal ikke arve en stille standard `{ _ in }` som om den betydde forventet motpart. Eksisterende `recheckPolicy` kan brukes til kontrollen, men verten må konfigurere én av følgende betydninger ved invitasjonsaksept:

- **Forventet identitet/akseptert sett:** eksakt domene og aksepterte deskriptorer eller kanoniske signeringsnøkler kommer fra lokal betrodd kontekst. Kravet til UUID versus bare nøkkel må være eksplisitt i denne konteksten. Oppgitt discovery-UUID er aldri et slikt bevis.
- **Førstekontakt med enhver bevist identitet:** verten velger uttrykkelig at hvilken som helst støttet, korrekt bevist nøkkel kan motta lokal identitet. Dette bevarer førstekontaktmuligheten, men gir ikke vern mot en aktiv M som presenterer sin egen nøkkel.

Ingen automatisk pinning av første mottatte nøkkel beskrives som forhåndstillit. Policy og dens versjon/revokasjonstilstand fanges sammen med invitasjonen; endringer revalideres før utsending/aktivering. R må tilsvarende ha lokal tillatelse til å røpe Id_R til en foreløpig uautentisert initiator når invitasjonen aksepteres. Hvis en vert krever at **begge** identiteter holdes tilbake til motparten er autentisert, kan denne v3-profilen ikke oppfylle den policyen; forsøket skal avvises lokalt, ikke falle tilbake til en svakere profil.

| Observatør/situasjon | Id_I | Id_R | Presis grense |
| --- | --- | --- | --- |
| M terminerer ytre transport, men videresender det indre håndtrykket uendret | Skjult | Skjult | M kjenner ikke Z; ingen stabile identitetsfelt/fingeravtrykk/signaturer finnes i klartekst. Fast auth-padding skjuler deres lengder. |
| Aktiv M starter DH som initiator mot ærlig R | M er selv initiator | **Synlig for M etter M2** | R må sende først og har ikke sett initiatorproof. Brukeraksept/rategrenser kan begrense sondering, men endrer ikke denne egenskapen. |
| Aktiv M svarer på ærlig Is M1 med eget DH og falskt R-proof | Skjult | Eventuell oppgitt M-identitet er uverifisert | I sender ikke M3 når proof/MAC/policy feiler. |
| Aktiv M svarer med eget DH og gyldig proof for egen, ikke-akseptert nøkkel | Skjult ved forventet-identitet-policy | M kjenner sin egen | Korrekt selvsignering er ikke tilstrekkelig for røping. |
| Samme aktive M, men I har valgt enhver bevist identitet | **Synlig for M etter M3** | M kjenner sin egen | M er blitt en akseptert kryptografisk motpart; profilen identifiserer den som M, ikke som den ønskede personen. |
| Ærlig R før R har bevist seg overfor I | Skjult for R | Sendes kryptert i M2 | I frigir Id_I først etter proof og røpingspolicy. |
| Ærlig I før I har bevist seg overfor R | Ikke sendt ennå | **Tilgjengelig for I i M2** | I kjenner handshake-nøklene før eget proof. |
| En motpart som faktisk er akseptert og fullfører | Synlig for motparten | Synlig for motparten | Ingen identitetshemmelighet overfor den autoriserte kanalmotparten. |

Tabellen er v3s konkrete trusselmodell. SIGMA-I begrunner rekkefølgen; aktive egenskaper for I er betinget av akseptpolicyen. Noise beskriver også identitetsvern med en forutsetning om at ukjente/ikke-betrodde peer-nøkler avvises. [Noise, §7.8](https://noiseprotocol.org/noise.html#identity-hiding).

En aktiv M kan etablere to selvstendige, aksepterte kanaler hvis begge ender faktisk aksepterer M. Den kan da lese identitetene og data på sine egne kanaler. Den kan ikke fremstille disse som en intakt, autentisert A–B-kanal uten proof for de relevante nøklene. En ren A–M–B-videresender kan fortsatt videresende, droppe og forsinke, men ikke utlede Kapp eller endre akseptert innhold. Signaturer over begge DH-verdier, identitets-MAC, rolle-/endpoint-binding, Finished og T5-avledning må vurderes sammen ved UKS-/refleksjonskontroll.

**Hva som ikke oppnås:** generell anonymitet, usporbar fysisk kommunikasjon, skjuling av profil, rolle, klokke, generasjon innen samme forbindelse, trafikkmønster eller app-record-størrelser. E kan allerede være kjent fra ytre invitasjon; discovery-/advertisement-/transportnavn kan være stabile eller identitetsavslørende. V3 må ikke kopiere Id, nøkkel, fingerprint eller identitetshash dit. Samme ytre metadata kan fortsatt knytte to forbindelser sammen selv når Id-feltene er kryptografisk skjult. «M kan ikke korrelere identitetsfeltene» gjelder direkte felt-/ciphertext-korrelasjon ved fersk korrekt DH, ikke all trafikk- eller sidekanalanalyse.

Det gis heller ikke vern mot kompromittert vault/endepunkt, samtidige minneuttrekk, dårlig tilfeldighet, DoS, kvantedatamaskiner eller senere misbruk fra en akseptert motpart. Senere kompromiss av bare langsiktig signeringsnøkkel skal ikke dekryptere tidligere innspilte håndtrykk/appdata når efemære og avledede hemmeligheter er slettet. Dette er forventet forward secrecy under primitive-/implementasjonsforutsetningene, ikke post-compromise recovery. Ingen deniability-garanti: motparten kan beholde deskriptorer og signaturer, og Is signerte kontekst inkluderer Id_R.

**8. Gate, session og suspendert signer**

Endringene holdes på peer-grenen; felles WS-signering og celleautorisasjon skal ikke gis nye unntak.

| Komponent | Nødvendig v3-endring |
| --- | --- |
| `BridgePeerChannelAuthentication` | Del identitetsfri Hello fra Auth-blokker; implementer de fem faste trinnene, transcript/KDF, padding, lokale kontekster og engangssignering. DH for handshake må kunne utføres før remote identity er kjent. |
| `BridgeChannelTransport` | Erstatt v2s `peerPlainSends/Receives` og record-zero-ack-logikk med eksplisitt v3-state. Bare M1 og den identitetsfrie delen av M2 er klartekstinnhold. M2–M5 går gjennom egne handshake-nøkler; de må ikke passere en generisk «plaintext tillatt»-vei. |
| `BridgeChannelSession` | Peer-challenge konstrueres etter dekryptert Id_R hos I, og etter dekryptert Id_I hos R. Behold reserve→policy-recheck→activate. Pending-challenge må ha lokal E, remote public identity, sessionID, lokal verifier-generation, signingData, digest d_s og tidsgrenser; den er intern, ikke Codable fra wire. |
| Session-tilstand | `unauthenticated` under Rs M1/M2 er normalt: ingen remote identitet å reservere ennå. `challengeIssued` og `verifying` oppstår ved mottatt Auth-blokk. `authenticated`, Base-factory og `peerReady` avhenger også av riktig Finished-trinn. DH/AEAD-suksess alene er aldri autentisering. |
| `BridgePeerRecordLayer` | Tar ferdig avledede Kapp og bundne generasjoner/roller fra vellykket v3-operasjon. Den skal ikke lenger avlede direkte fra v2-hello/signaturtranscripts. Begge datatellere starter på 0 etter håndtrykket. |
| `IdentitySigningChallenge` / vault | Samme lokale type, validering og signerings-API; v3s kontekst/encoder bygges av peer-operasjonen. Ingen remote signer, rå signingData-inngang, privatnøkkeleksport eller statisk DH-tillegg. |

Ved alle await-grenser i vault-eksistenssjekk, signering, peer-policy, send og factory skal continuation sjekke den **fangede** operasjonen: ikke terminal/kansellert, samme fysisk binding og session generation, gyldig monoton/veggklokkefrist og fortsatt gyldig policybeslutning. Kontrollen kreves også **før neste** sensitive await, særlig mellom `identityExistInVault` og `signMessageForIdentity`. Ett `active`-flagg kontrollert bare før hele sekvensen er utilstrekkelig.

Close/revoke setter terminal tilstand synkront, sperrer nye state-overganger og nye sendopptak, og kansellerer arbeid. Cancellation er ikke bevis for at vault-arbeid har stoppet. Når en ikke-samarbeidende signer senere returnerer, skal signaturen forkastes; ingen M2/M3, nøkkeinstallasjon, ny delegate eller Base får oppstå. Den beholdte arbeidsleasen frigjøres først når arbeid faktisk returnerer. Et resultat for gammel gate kan aldri velge ny gate via discovery-UUID.

Endelig state-/sendkontroll og fysisk sendopptak må ha et definert synkront lineariseringspunkt sammen med adapterens sendrekkefølge. Close som vinner dette punktet forhindrer den nye utsendingen. En frame som allerede er innlevert før close kan ikke tilbakekalles; det skal ikke rapporteres som om revokasjon kunne slette bytes fra nettet. Ingen lås holdes over vault-/policy-/factory-await. En factory som returnerer etter pensjonering må ryddes uten å publiseres; ved close mellom `session.activate()` og factory-retur skal `peerReady` forbli false.

Lokal signeringsidentitet og remote kanalprincipal må skilles ved revokasjon. Dagens `limits.revoke(identity,domain)` treffer registrerte remote principals, ikke automatisk en ukjent M1-peer eller lokal vaultidentitet. Før remote proof er registrert må close av den konkrete gaten eller vertens oppdaterte policy sperre opptaket. Lokal eierrevokasjon må kansellere den aktuelle signeringsoperasjonen. En generell varig nøkkelsperre er fortsatt et separat vertspolicyregister; v3 skal ikke beskrive dagens lease-revoke som dette.

**9. Record-lag, kvoter, N18 og N08/N11**

App-record beholder v2s form og grenser, med følgende fastsatte endringer:

```
header = U("HPC3") || U(senderGeneration) || directionByte || U64(counter)
nonce  = zeroBytes(4) || U64(counter)
AAD    = U(P + NUL + "record" + NUL) || header
wire   = header || ChaCha20Poly1305(Kapp[direction], nonce, plaintext, AAD)
```

Generation er nøyaktig 36 ASCII-bytes. directionByte er 0 for I→R, 1 for R→I. Header er 49 bytes, tag er 16, samlet overhead 65. Plaintext er 1…1 048 576 bytes. Counter starter på 0 separat i hver retning; `UInt64.max` brukes aldri. Record 0 er nå ordinær kryptert app-/kontrollrecord, **ikke Finished**. Ingen datanøkkel eller datateller deles med håndtrykket. Eget magic og profil i AAD avviser gamle frames selv om header omskrives; T5-avledede nøkler binder den nye utvekslingen.

Mottaker krever neste eksakte teller, riktig generasjon/retning og gyldig tag før dekoding. Replay, gap, refleksjon, feil generasjon, plaintext, gamle magic, tom/trunkert/for stor record eller tagfeil er terminalt. App-`peerGeneration`, session-/principal-sjekk og forbudet mot `ready` beholdes. Alle kommandoer, responses, origin-signerings-RPC-er, flows, NI-data og eventuelle kvitteringer går gjennom samme AEAD-grense. Kryptering autoriserer ikke cellekallet.

Seal+tellerallokering+fysisk innlevering bevarer én sendeorden. Åpning og auth-trinn behandles i én bounded mottaksorden. N10 må i tillegg sikre ordnet opptak/levering for ordensavhengige konsumentmeldinger; serialisert AEAD er ikke tilstrekkelig. Å vente på hele celleoperasjonen i mottaksloopen må ikke deadlocke signerings-RPC-svar. N13s lease/generasjon følger det reelle asynkrone konsumentarbeidet til slutt.

Globale pending-/rate-/arbeidsgrenser gjelder **før** DH, JSON som kan bli stor, nye Tasks og signering. Dagens 64 operasjoner/4 MiB adapterkø og gategrenser beholdes som minimum, men er ikke et samlet reassembly-/maskinminnebevis. Før identity proof finnes bare fysisk/source/global kvote; ikke opprett en per-key-bøtte fra ukryptert hint. Etter MAC+signatur reserveres `quotaKeyIdentifier()` fra N17-headen: kanonisk signeringsnøkkel, ikke selvoppgitt UUID/domain. Kanalprincipal beholder sin separate autorisasjonsbetydning. Padding, JSON, base64 og tag regnes med i faktiske wirebytes.

**N18-integrasjonskontrakt:** v3 gir ikke selv en generell leverings-/flytkontrollprotokoll. Den rettingen må fortsatt dokumentere sitt presise wireformat og vindu. Følgende regler er obligatoriske for at den kan brukes med v3:

- Handshake-sendkvote må holdes til autentisert fremdrift bekrefter mottak, eller fysisk pensjonering faktisk frigjør ressursen. Gyldig M2 bekrefter W1, gyldig M3 bekrefter W2, gyldig M4 bekrefter W3 og gyldig M5 bekrefter W4 gjennom transcript-kjeden hos en korrekt implementert motpart. Ikke frigjør på en ukontrollert neste command eller på vellykket MC-kølegging. M5 kan regnes kvittert ved første gyldige R→I-app/control-record under T5-avledet Kapp, eller frigjøres ved faktisk fysisk opprydding. Dette er autentisert fremdrift, **ikke bevis mot en løgnaktig motpart for fysisk levering**: en DH-deltaker kan beregne de symmetriske Finished-verdiene selv. Fravær av slik trafikk beholder den bounded M5-reservasjonen til timeout/close. Håndtrykkets absolutte femmeldings-/størrelsestak gjelder uansett.
- Alle senere leveringskvitteringer skal være egne strengt validerte **krypterte kontrollrecords** under Kapp, aldri nye plaintext-auth-meldinger eller misbruk av Finished. De må identifisere denne session/generasjonen og den bekreftede senderretning/telleren. Ingen autentiserings- eller policyvirkning.
- Et verifisert ack kan frigjøre kun faktisk utestående records i samme sendvindu. Forbudt: framtidige tellere, feil retning/generasjon, undertelling ved duplikat, frigjøring av andre peers eller gjenbruk av ack etter reconnect. Receipt selv tar neste record-teller i sin egen retning. Kontrolltypen er internt eid av gaten og må ikke kunne injiseres som lokal appkommando.
- En tellerkvittering alene er ikke robust mottaksbevis mot en ondsinnet peer som gjetter neste teller og kvitterer før datamottak. Hvis N18 bruker receipt til en slik ressursgaranti, må den kreve en fersk, uforutsigbar senderbestemt receipt-verdi i den forseglede recorden, bundet til hele recorden/telleren/generasjonen, og kontrollere denne før frigjøring. Ikke avled denne verdien bare fra felles Kapp: mottaker kjenner Kapp. Den eksakte plasseringen og kvitteringskodingen hører til N18-kontrakten; selv dette beviser ikke når OS har frigjort alle interne buffere.
- Ingen ack-av-ack-løkke. Kontrolltrafikk må ha et lite, bounded reservert budsjett så et fullt datavindu ikke hindrer kvittering. Kvittering etter bounded mottaksopptak betyr ikke ferdig cellehandling eller persistens. En ondsinnet mottaker kan lyve om egen behandling; receipt er ikke et forretningsbevis.
- Ingress/reassembly før MC-callback, faktisk fysisk frigjøring og RSS under mottrykk må fortsatt dokumenteres/måles av N18/N15. V3-kryptering og et remote ack beviser ikke et slikt OS-ressurstak.

Det kreves altså ingen sjette handshake-melding for identitetsvern. N18 kan sende en første R-kontrollrecord ved aktivering for rask frigjøring av Is M5; den ligger under Kapp og den valgte N18-kontrakten. Ingen ny receipt-funksjon skal aktiveres ved uautentisert forhandling. Hvis N18 endrer den fastsatte record-headeren eller innfører forhandlede kryptofelt, må dette designet revideres før samme v3-profil brukes.

**N08/N11-binding:** pending og accepted invitasjon må eie sin peer/session/E/rolle/instans uten oppslag i dagens discovery-indeks. Aksept er atomisk, og utgående/aksepterte forsøk uten kanal pensjoneres på timeout. LostPeer fjerner oppdagelsesdata, ikke en fortsatt eid binding. Crossed invitations avgjøres én gang før v3-oppretting; gammel callback eller ny C med Bs discovery-UUID kan verken bytte rolle/E, sende gjennom B eller lukke en ny generasjon. Gammel fanget adaptercallback avvises uten skade på ny gate. Gammel ciphertext levert til **gjeldende** adapter er derimot protokollfeil som lukker den gaten, som i v2.

N12s NI-binding, N14s resource/stream-avslag, N15s fysisk pensjonering, N16s discovery-opptak, N19s private diagnostikk og N20s kontaktproof-binding forblir egne rettinger. V3s verifiserte principal/generasjon må føres til disse konsumentene; de kan ikke utledes av navnet eller en løs signatur. N21-dokumentene må ved implementering peke på én faktisk v3-kontrakt og merke v2 som avvist, ikke la begge fremstå som aktive.

**10. Avvisning av nedgradering**

Bare P, de fem `channelAuthPeerV3…`-navnene og `HPC3` støttes på peer-grensen. Peer v1/v2, gamle hello/proof/accepted-navn, `HPC2`, manglende profil, liste over profiler, feil suitefelt, ukjente extensions og blandede trinn avvises terminalt. Ingen «prøv v2 hvis timeout», legacy-ready, plaintext-appmodus eller alternativ nøkkel ved decrypt-feil. Ny tilkobling etter avslag forsøker fortsatt bare v3.

WS forblir `org.haven.bridge-channel.v1` med action `openBridgeChannel` og sin eksisterende endpoint-/signeringskontrakt. Det er **ikke** en akseptert eldre peer-profil. En peer-v3-envelope kan ikke omdirigeres til WS-parseren eller omvendt. Ikke fjern WSs v1 fordi peer v1 avvises. Oppgraderte og ikke-oppgraderte peer-binarier kan ikke etablere kanal; utrullingen må håndtere denne bevisste inkompatibiliteten.

**11. Testplan og målbare kriterier for kontroll 5**

Dette er bestilt testplan. Ingen av de følgende v3-testene er kjørt i denne designøkten. Eksisterende v2-testnavn brukes som plasseringsforslag, ikke som påstand om dekning. Alle identiteter, markører og nøkkelmateriale i senere testfixtures skal være syntetiske; denne designfilen inneholder ingen nøkkelverdier.

**11.1 Uavhengige testvektorer.** Utvid `BridgePeerRecordLayerTests` og lag en egen peer-v3-handshake-fixture. Lag forventningsverdier med en uavhengig liten referanseimplementasjon, ikke ved å serialisere produksjonskodens egne resultater og kalle dem fasit. Kjør samme fixtures på macOS/CryptoKit-støttet kode og Linux/Swift Crypto. Arkiver referanseverktøyets kilde/version og fixture-hash i implementørens bevispakke.

| Vektorfamilie | Må fryse/verifisere |
| --- | --- |
| Primitive kjent-svar | RFC 7748 §6.1, RFC 5869 Appendix A og RFC 8439 §2.8.2; providerfeil og all-zero-rejection i tillegg |
| Full I/R-utveksling | Faste syntetiske DH-input, noncer, tider, UUID-er, E og Id; eksakte C(H_I), C(H_R), W1, alle F-input, T1/T0, Extract-output og begge Khs/Kid |
| Signeringsbytes | C(D_R), C(D_I), d_R/d_I, nøyaktige challenge-bytes, begge signaturer, Core/Auth-blokker, MAC-er og full padding |
| Hele handshake-wire | W2–W5 byte for byte, alle AAD/nonce/counter, T2–T5, Kfin/Kapp i begge retninger, ack-felter og verifyData |
| Record-wire | HPC3-header, AAD, ciphertext/tag for hver retning ved counter 0 og 1; ulik plaintext av samme lengde; counter-grense |
| Encodinggrenser | Unicode, kontrolltegn, slash og JSON-escaping i gyldige syntetiske scope/UUID-strenger; brøkdelssekunder; full blokk, én byte for stor blokk og maks ferdig envelope |
| Signeringsvarianter | EdDSA/EdDSA, P256/P256 og begge blandede retninger; både tillatte P256-public encodings og DER-validering; N17-kvoteidentitet lik for samme P256-nøkkel |

EdDSA kan gi en helt deterministisk fullfixture. P256-fasiten skal bruke en fast **gyldig** fixturesignatur over de eksakte bytes; en levende vault kan produsere en annen gyldig DER-signatur. Live-testen skal da verifisere signaturen og samsvar hos begge parter, ikke kreve tilfeldig signaturlikhet. En fixture med endret signatur krever nye ciphertext-/transcript-/Kapp-verdier. Ingen test skal få samme expected og actual fra samme produksjonshelper.

**11.2 A–M–B, ren videresender.** Bruk den eksisterende kontrollerte adapterseamen til å la M se, holde og videresende **alle** inner-wirebytes. Kjør ekte lokal-vault-signering og gjennomfør faktisk description, attach, feed og en origin-signatur-RPC etter M5. Assertér at både I og R får riktig principal, nøyaktig konsumentrekkefølge og data begge veier.

- Pars M1–M5 som en angriper. Klartekstfelt må samsvare eksakt med allowlisten i §3/§6. Ingen PublicIdentity, UUID-identitet, public signing key, fingerprint, signatur, E eller deres direkte identitetshasher kan finnes som egne klartekstfelter. Suppler med søk etter syntetiske markører i råbytes, base64 og JSON; søk alene er utilstrekkelig.
- Samme identiteter i minst to helt ferske håndtrykk gir nye DH/noncer/generasjoner og ulike M2/M3-ciphertexts. Bytte mellom ulike identiteter med ulike descriptor-/signaturlengder gir fortsatt eksakt 8208 sealed-bytes per Auth-blokk og 1040 per Finished. Ingen identitets-/algoritmehint i hello.
- Gi M kandidatlisten over alle syntetiske offentlige identiteter, men ingen DH-hemmeligheter. Ingen protokollfelt gir en offentlig equality-/fingerprint-test mot kandidatene. Assertér schema/padding/ferskhet og at M ikke kan åpne med egne, uvedkommende DH-nøkler. En statistisk «classifier accuracy»-test eller fravær av ASCII-markør er ikke et kryptografisk bevis for usporbarhet.
- M kan ikke lese appinnhold eller bytte en gyldig plaintext-response inn på wire. Hold M4: ingen I-factory. Hold M5: ingen R-factory. Etter frigivelse fungerer ekte appflyt. Ingen appframe får dispatch mens Finished fortsatt ventes.
- Gjenta på tre reelle prosesser med M som to ytre MC-endepunkter hvis adapteren støtter denne prøven. Rapporter separat seambevis, faktisk MC-bevis og eventuelle radioprøver. Ikke kall to ærlige prosesser en utført treparts-MITM-test. Testen skal observere inner-wiregrensen; ytre kryptering alene ville skjult v2-lekkasjen for feil testpunkt.

**11.3 Aktiv M og identitetsrøping.** Fire egne positive/negative forløp er obligatoriske:

1. M starter DH som I mot B. M kan åpne Bs M2 og lese Id_B uten eget identitetsproof; B oppretter ingen Base. Dette er en **forventet begrensning som testen skal bekrefte**, ikke et testavvik som skjules.
2. M svarer A som R med egne DH-bytes, men gjenbruker Bs proof eller presenterer Bs deskriptor uten Bs signatur. A avviser før egen signer kalles/M3 sendes. Samme resultat ved DH-substitusjon i hver retning eller replay fra annet endpoint/generasjon.
3. M har egen gyldig signeringsidentitet. A med forventet-B-policy avviser M før egen signering/røping. A med eksplisitt enhver-bevist-identitet-policy kan fullføre med M og avsløre Id_A; principal er M, aldri B. Assertér denne forskjellen, også om discovery-navnet sier B.
4. M lager to uavhengige DH-utvekslinger mellom A og B, bytter identiteter/roller/E eller forsøker å skjøte Finished fra én kanal til den andre. Uten aksept for M og de nødvendige identitetssignaturene skal det ikke oppstå en A–B-principal med M-lesbare data. Ren uendret videresending skal fortsatt fungere.

Ta også med samme signeringsnøkkel på begge ærlige ender, ulik rolle/generasjon, som refleksjonsregresjon. E krever fortsatt ulike endpoint-navn; sikker retning må ikke avhenge av at signeringsnøklene er forskjellige.

**11.4 Enkeltfeltmutasjoner.** For hver mutasjon kreves eksplisitt forventet avslagspunkt, ingen factory/dispatch etter feil, terminal opprydding, korrekt beholdt/frigjort kvote og fortsatt fungerende søskenkanal. Prøv både én bit endret uten reparert tag, og relevante varianter laget av en **legitim DH-deltaker** med ny korrekt AEAD/MAC. Bare tagfeil tester ikke signatur-, kontekst- eller policyvalideringen.

| Gruppe | Muter ett felt om gangen, begge roller der feltet finnes |
| --- | --- |
| Hello | profile, role, hver DH-public, nonce, generation, issuedAt; manglende/ekstra felt; feil lengde; lik generation; utløpt/fremtidig tid; Int64-grenser |
| E | initiator, responder, setupID, domain; gyldig signatur over en annen selvkonsistent E må likevel avvises mot lokal invitasjon |
| Identity | uuid, algorithm, curve, publicKey, feil nøkkelrepresentasjon; samme key/ny UUID; ukjent signer under expected-identity-policy |
| Proof/challenge | sessionID, verifier-generation, signatur, signerrolle, resource, audience, domain, nonce og issued/expires; signér med testvault over én feil lokalt forventet kontekst |
| Auth-MAC | manglende/trunkert/feil identityMAC; feil retning, feil Kid, riktig MAC over annen Core eller T0/T2; signatur korrekt men MAC feil og omvendt |
| Finished | ack.sessionID, ack.generation, ack.transcriptDigest og verifyData; feil T3/T4, retning/nøkkel/trinn, gyldig AEAD men feil HMAC |
| Krypteringsramme | sealed-lengde, tag, ciphertext, implicit nonce/counter, paddinglengde, ikke-null padding, JSON-lengde, ukjente/dupliserte/nestede metadata, trailing bytes |
| State | gjenta, utelat eller bytt hvert Mj; M3 før M2, M5 før M4, data før Finished, auth etter active, cross-session-splicing og parallelle duplikater |
| Record | magic, generation, direction, counter, tag; replay/gap/refleksjon, gamle ciphertexts med omskrevet ny header, 0/maks/maks+1 bytes og telleruttømming |
| Kompatibilitet | v1, v2, HPC2, WS-envelope, manglende v3-felt og foreslått fallback; ingen ny v2-utsending ved avslag/timeout |

Ved endring som en akseptert peer legitimt kan velge og korrekt signere, skal testen **ikke** automatisk kreve kryptografisk avslag. Eksempel: annen Id under enhver-bevist-identitet-policy er tillatt, men må gi annen principal og fortsatt korrekt kvotering. For avslagstesten må den muterte påstanden bryte den frosne lokale konteksten, proofet eller den erklærte policyen. Dette hindrer at testen forveksler «gyldig signatur over annen påstand» med aksept av den forventede påstanden.

**11.5 Suspendert lokal signer, revokasjon og ressurslivsløp.** Bruk deterministiske barrierer, ikke tilfeldige sleeps. Test I og R separat med en vault som ignorerer Task-cancellation, men til slutt returnerer en gyldig signatur:

- Suspender `identityExistInVault`; close/revoke/utløp; slipp barrieren. Ingen kall til `signMessageForIdentity` etterpå.
- Suspender selve signeringen; close av fanget gate, direkte session-revoke, lokal eierrevokasjon, stop og transportfeil i separate forløp; opprett deretter ny frisk kanal med samme discovery-navn. Slipp gammel signer. Ingen gammel M2/M3, nøkkelinstallasjon, factory eller påvirkning av ny gate.
- Suspender remote `recheckPolicy`, fysisk send og factory hver for seg. Revoker/utløp og returner så suksess. Ingen delegate/peerReady publiseres etter pensjonering; eventuell returnert factory ryddes. Dersom send allerede vant sitt opptak før close, logges det som før-close-innlevering; ingen ny utsending tillates.
- Kontroller `maximumOutstandingWork`, pending og beholdt connection før/etter close. Hengende arbeid skal fortsatt telles, og frigjøres nøyaktig én gang når det returnerer. Gjenta til grense+1; en storm av avslag må ikke skape ubegrensede Tasks.
- Test faktisk `limits.revoke` etter at remote principal er registrert. Test før registrering som eget tilfelle: den kan ikke forventes å finne en ukjent identitet; oppdatert vertspolicy eller konkret gate-close må stoppe den. Verifiser at ingen dokumentasjon lover automatisk varig sperring.
- Injiser klokker for eksakte fristgrenser, veggklokkehopp begge veier og monoton timeout mens vault er suspendert. Ingen ekstra ti sekunder etter siste melding. Fristberegning må ikke wrappe ved ekstreme input.

**11.6 Integrasjon og bevispakke.** Kjør N08/N11 med A/B/C, lostPeer før/under aksept, atomisk overgang, crossed invitation, invitasjonstimeout, ny gyldig invitasjon og gammel callback. Hold første konsumentlevering etter åpning og krev eksakt rekkefølge, samtidig som origin-signerings-RPC fortsatt svarer (N10). Test kvote med én kanonisk signeringsnøkkel/mange UUID-er og P256-encodings (N17), og diagnosticLogHandler aktivert med hemmelige testmarkører i Auth, feil og apppayload (N19). Ingen rå/dekrypterte autentiseringsblokker, signatures, fingerprints eller innhold skal logges; bruk begrensede lokale feilkoder.

N18 må kjøre langsom/manglende og løgnaktig kvitterende mottaker, tap/duplikat/feilgenerasjon/framtidig ack, fullt datavindu med kontrollfremdrift, close med utestående bytes og gjentatte reconnects. Mål wirebytes, beholdte records/leases og faktisk minne; vis fungerende søsken. Handshake alene er bounded også når siste Finished holdes. N12–N16/N20 må fortsatt ha de produksjonskonsument-/iOS-/MC-prøvene kontroll 4 krever; v3-seamen erstatter dem ikke.

For kontroll 5 leveres eksakt implementert head-SHA, diff mot denne designbasen, fixture-/referanseversjon, testkommandoer, råresultater og tydelig skille mellom kjørt, ikke kjørt og begrunnet utenfor testmiljøet. macOS, Linux og relevant iOS-bygg inngår i total PR-port. Sikkerhetsgjennomgang skal kontrollere asymmetrien i §7, alle nøkkelbruk og await-/sendgrenser direkte i koden, ikke bare telle grønne tester. En egen kryptografisk review eller modell av denne konkrete instansieringen styrker grunnlaget; eksisterende SIGMA-/Noise-analyser må ikke listes som et utført bevis for v3.

**12. Primærkilder og avgrenset konklusjon**

Kildene er kontrollert på nettet under denne økten. Meldingsformat, labels, padding, CP-policybinding og testkriterier ovenfor er **designbeslutninger i dette dokumentet**, ikke sitater eller standardiserte SIGMA-felter.

| Primærkilde | Hva den brukes til |
| --- | --- |
| [Hugo Krawczyk: SIGMA, CRYPTO 2003, §§2.2, 5.1–5.2](https://iacr.org/cryptodb/archive/2003/CRYPTO/1495/1495.pdf) | Sign-and-MAC-mønster, adskilte nøkkelformål, kryptert autentisering og initiator/responder-asymmetri |
| [Noise Protocol Framework, §§7.5–7.8](https://noiseprotocol.org/noise.html) | XXs statiske DH-tokenstruktur og vilkår/begrensninger for identitetsvern; grunnlag for å ikke kalle v3 standard XX |
| [RFC 7748, §§5–7](https://www.rfc-editor.org/rfc/rfc7748) | X25519-semantikk, DH-kjent-svar, all-zero og behovet for å binde de offentlige inputverdiene |
| [RFC 5869, §§2–3 og Appendix A](https://www.rfc-editor.org/rfc/rfc5869) | Extract/Expand, kontekstseparasjon i info og kjente testvektorer |
| [RFC 8439, §§2.8, 2.8.2 og 4](https://www.rfc-editor.org/rfc/rfc8439) | ChaCha20-Poly1305, AAD, nonce-disiplin, full tag og kjent-svar |
| [RFC 8446, §4.4.4](https://www.rfc-editor.org/rfc/rfc8446#section-4.4.4) | Sammenligningsgrunnlag for separat Finished-HMAC over transcript; ingen TLS-kompatibilitet hevdes |
| [CellProtocol PR #53](https://github.com/Digipomps/CellProtocol/pull/53) og [fastlåst commit](https://github.com/Digipomps/CellProtocol/commit/605298fe404d46827100559a862ec2e9b1978fc8) | Implementeringsgrunnlaget for v2, gate, session, vault og kvoter |

N22 kan lukkes når implementasjonen følger denne kontrakten og den faktiske inner-wireprøven viser at en ren videresender ikke får stabile identitetsfelt/signaturer i klartekst, samtidig som aktive begrensninger rapporteres som i §7. Leveringen av dette dokumentet alene lukker ikke N22 og opphever ikke «alle 13 før merge».

Varig læring i denne leveransen: skill mellom DH-deltakelse, nøkkelkontroll, akseptert identitet, fysisk binding og celleautorisasjon; særlig må «initiatorvern mot aktiv M» ikke brukes uten å angi røpingspolicy. Læringsruting pekte på `cellprotocol-identity-capability-security`. Beslutningen er bevart her. Separat skill-/ledger-/loggoppdatering er ikke utført, fordi denne konkrete bestillingen begrenser skriving til én designfil.
