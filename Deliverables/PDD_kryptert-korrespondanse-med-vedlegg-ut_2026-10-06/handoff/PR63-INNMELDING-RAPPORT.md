# PR #63 — innmelding og vedleggsrot ved oppstart

Kandidat og nytt PR-hode: `a2b1fc2f8f6c1b9d7887a018d89c959138418d2d`, oppå p1s `66e165becf52e3f057d1596f23e05d7078b3bc2c`.
Gren: `codex/korr-relasjonscelle-20261007`. [PR #63](https://github.com/Digipomps/CellProtocol/pull/63) forblir OPEN og kladd. Ingen merge eller tag.

## Krav og faktisk bevis

Alle «kjørt» nedenfor gjelder macOS 27, Xcode 27 og Swift 6.4. F = fokusert r4: 75 tester, 0 feil, runner exit 0. G = full grunnmurport på eksakt kandidat: bygg exit 0 (272 s), test exit 0 (112 s), **1627 bestått / 5 hoppet over / 0 feil**, totalt **1632** XCTest-utfall. Tallene er kontrollert mot individuelle testlinjer, ikke siste suite-oppsummering.

| Krav | Test | Utfall | Bevis |
|---|---|---|---|
| Betrodd lokal vertsrot, uten medlemsbevis; utløpt vedlegg slettes ved kald gjenoppretting uten reconnect | `testTrustedHostAttachmentRootPurgesAtColdRestartWithoutMember` | Kjørt grønt: fersk dekoding, utløpt diskindeks, både vedleggsmappe og indeksoppføring fjernet uten deltakeroperasjon | F og G; redigert formålsutskrift |
| Rotbindingen er bare Swift-API, ingen wire-operasjon eller grant | `configureTrustedHostAttachmentStorage(root:)`, registrerte operasjoner og Explore | Lest i kode; ingen egen negativ wire-probe kjørt. API-et gir ikke medlemskap eller signeringskapabilitet | Kandidatens kilde; uendret eksisterende requester-API |
| Gyldig request → eierens kode og beslutning → result med avtale → agreement.accept → tekst/vedlegg | `testLocalPurposeThreeVaultsTextAttachmentsFlowRenewalAndRevocation` | Kjørt grønt med E/H/I; alle fire join-operasjonene og agreement.accept gjennom resolver. Tekst og 1 100 037 vedleggsbyte begge veier, Flow, fornyelse og tilbakekall beholdt | F og G; redigert formålsutskrift |
| Avslag, utløpt og gjenbrukt invitasjon, feil nøkkelbevis | `testJoinRejectionsPrivacyRestartAndFlow` | Kjørt grønt: konkrete wire-resultater, ugyldig proof forbruker ikke invitasjonen, replay avvises også etter lagring/dekoding | F og G |
| Resultat med annen nøkkel gir ingenting, også samme UUID med reelt nøkkelbevis | `testJoinRejectionsPrivacyRestartAndFlow` | Kjørt grønt: vanlig annen identitet og bevist annen nøkkel med samme UUID får null | F og G |
| Ikke-medlem får ingen Flow; request bare til eieren, decision bare til forespørselens nøkkel | `testJoinRejectionsPrivacyRestartAndFlow`, `testJoinFlowIsBoundToKeyAndRecipient` | Kjørt grønt: ikke-medlemsabonnement avvises; riktig mottaker får hendelse; feil mottaker og gammelt medlems nøkkel får ingen join-hendelse | F og G |
| Vert uten eierens nøkkelbevis kan ikke godkjenne; personnavn og privat nøkkel ikke lagret | `testJoinRejectionsPrivacyRestartAndFlow`; snapshotkontroller i formålsprøvens join-hjelper | Kjørt grønt: offentlig eierbeskrivelse alene avvises; fritekstnavn i signert avtale avvises; både denied- og approved-snapshots uten displayName/privateKey:true; gjenopprettet approved Contract beholder gyldig signatur | F og G |
| Begge sider får samme sekssifrede kode, prøvd annen nøkkel får annen kode, formelen har uavhengig golden | Formålsprøvens join-hjelper; `testJoinCodeGoldenAndPendingExpiry` | Kjørt grønt; golden `983780` beregnet med Python hashlib uavhengig av Swift-hjelperen | F og G |
| Ventende request utløper, også om beslutning forsøkes etter fristen | `testJoinCodeGoldenAndPendingExpiry` | Kjørt grønt med deterministisk tidsinput på ledger-nivå; dette er ikke en ventet wire-/OS-omstartstest | F og G |
| Ingen eksisterende test fjernet eller assertions svekket; hele pakken virker | Eksisterende full grunnmurport | Kjørt grønt. Den eksisterende formålsprøven er utvidet med join før innslipp; øvrige assertions er beholdt | G, 1632 utfall |

Før grønt: r1 stoppet med filstørrelsesgrense før tester; r2 stoppet ved en kompilatorfeil i GET-handlerens valgfrie retur. R3 kjørte 74/0. Uavhengig Codex-lesekontroll fant deretter UUID-only Flow-filter og fritekst i avtalen; begge rettet før r4, fullport, commit og push. Etterkontrollen fant ingen gjenværende funn i disse rettelsene. Dette er lest i kode av en separat Codex-agent med arvet modell, ikke tester kjørt av kontrollagenten.

Den statiske Explore-auditen har fire nye komplette kontrakter (322 → 326, handleroperasjoner 333 → 337). De 7 feilene og 20 advarslene er nøyaktig de samme funnene som på p1-basisen; denne auditen omtales derfor ikke som en helt grønn repo-audit.

## Avgrensning

E/H/I og kald gjenoppretting er kjørt i én lokal testprosess med adskilte nøkkellagre og fersk dekoding av lagret celle/indeks, ikke tre maskiner eller en fysisk prosessomstart. Ingen nye private nøkler overføres gjennom join. Fast protokolltekst i Agreement/Grant.name er tillatt; person-/kontakt-/visningsnavn er ikke lagret. Signerte proof- og avtaledokumenter lagres med offentlige nøkler. Vertens snapshotlagring må fortsatt utføres av integrasjonen; dette beviser ikke motstand mot tilbakerulling av backup eller en ondsinnet vert.

Ingen staging, fjernbro, Touch ID, klientpakke, installer, notarisering eller deploy er kjørt i p2. k1/s2 må pinne det grønne PR-hodet og verifisere sin egen integrasjon. Ventende ikke-medlem poller resultatet; medlemskravet på Flow er beholdt.

## CI på eksakt PR-hode

**4/4 SUCCESS**, kontrollert etter avsluttet watcher. PR-head, OPEN og isDraft=true ble kontrollert sammen med sjekkene. macOS-jobbens normale testtrinn og Thread Sanitizer-trinn er begge SUCCESS; TSAN-trinnet kjører de relevante suitene i tre adskilte prosesser.

| CI-sjekk | Status | Bevis |
|---|---|---|
| Persisted Cell file bounds | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37714535803/job/113107881889) |
| regression | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37714535748/job/113107882072) |
| bounded synthetic runtime matrix | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37714535710/job/113107881932) |
| Vapor identity vault strict storage | SUCCESS | [GitHub-jobb](https://github.com/Digipomps/CellProtocol/actions/runs/37714535713/job/113107881900) |

## Eksakt kontrakt for k1 og s2

`await configureTrustedHostAttachmentStorage(root:)` er kun lokal vertsbinding etter decode og før betjening av forespørsler. Behold relation UUID og betrodd lagerkonfigurasjon utenfor Cell-snapshotet. Gjenbruk av `ChatInvitationProofUtility` gjelder offentlige nøkkelbeskrivelser og rekonstruksjon; canonical payload og den eksisterende offentlige signaturverifikatoren brukes, ingen automatisk chat-invitasjonsaksept.

## Wire

JSON uses Codable's standard Base64 strings for Data and Unix epoch seconds for times. All UUIDs are strings. No name or path is accepted in join types. Operations require the existing authenticated requester proof; forwarding does not authorize a decision.

- SET `join.request`: `CorrespondenceJoinRequest`: `version:1`, `purpose:"haven.correspondence.join.request.v1"`, `invitation`, `identityUUID`, `signingPublicKey`, `signingAlgorithm`, `signingCurve`, `agreementPublicKey` (32 raw X25519 bytes), `requestedAt`, `signature`.
- `invitation`: `version:1`, `purpose:"haven.correspondence.join.invitation.v1"`, `cellUUID`, `invitationID` (UUID), `issuedAt`, `expiresAt`, `signature`. Positive lifetime at most 604800 seconds. Invitation signature is verified against the relation owner's public signing key. Request signature is verified against the submitted public signing key. Both signatures cover `CanonicalPayloadEncoder`'s payload excluding only their respective top-level `signature`; the request includes the entire signed invitation. The request timestamp is within 300 seconds of the host clock; future invitation issuance tolerates five seconds.
- Successful request: `{requestID,status:"pending"}`. Rejected request: `{status:"rejected",code:"invitation.used"|"invitation.expired"|"invitation.invalid"|"join.proof.invalid",requestID:""}` (validation rejection may omit requestID). A valid invitation is consumed atomically on the first valid request, including a later denied request. Invalid proof does not consume it. Consumption survives snapshot decode.
- GET `join.pending`: owner proof required. Returns an array of `{requestID,invitationID,identityUUID,signingPublicKey,signingAlgorithm,signingCurve,agreementPublicKey,receivedAt}` for unexpired pending requests. This read has no payload.
- SET `join.decide`: `{requestID,approve:true,contract:<existing Contract JSON>}` or `{requestID,approve:false}`. Only the proven owner may decide. An approval requires a valid, active, cell-bound owner-signed Contract for the exact requesting identity and X25519 key, issued no earlier than receivedAt minus five seconds. Signed identity labels must be UUID fallbacks; identifying metadata or private material is rejected. Agreement and grant names must equal the fixed attachment template names, conditions must be empty, policy binding nil, and the two signatories must be exactly the owner and requester. Contract issuance cannot be more than five seconds in the future. Response `{requestID,status:"approved"|"denied"|"expired"}`. Invalid approval returns `{status:"rejected"}`; unknown or already decided request returns null. This does not install the agreement.
- GET `join.result.<requestID>`: requestID is the trailing keypath component (the Cell GET interface has no separate payload). Requires control of the request's exact signing key and identity UUID. Returns `{requestID,status:"pending"|"approved"|"denied"|"expired",contract?:<Contract>}`. Only approved results contain a contract. An unrelated requester or unknown ID receives JSON null. Pending requests expire at invitation expiry; already approved/denied decisions remain available.
- After approval the invitee submits the returned Contract through existing SET `agreement.accept`; all existing admission checks still apply. The link alone and join approval alone grant no membership.

GET `join.result` is the Explore parent entry, not a result without a requestID. Adapters must forward the full `join.result.<requestID>` keypath. Owner-only accesses throw the existing denied error when requester proof fails.

## Flow and code

Topic `haven.correspondence` carries `join.requested` with `requestID`, `recipientIdentityUUID` (owner), `recipientSigningFingerprint` (owner key); `join.decided` with `requestID`, `status`, `recipientIdentityUUID` (requester), `recipientSigningFingerprint` (request key). The authenticated member publisher filters each join event to its recipient UUID and signing fingerprint. Nonmembers cannot subscribe to this publisher; the pending invitee polls `join.result.<requestID>`. Other members do not see an owner's join request or somebody else's decision.

`CorrespondenceJoinCode.code(cellUUID:invitationID:signingPublicKey:agreementPublicKey:)` hashes the concatenation of UTF-8 cellUUID, UTF-8 invitationID, raw signingPublicKey, raw agreementPublicKey, in that order. Interpret the first four SHA-256 digest bytes as unsigned big-endian UInt32, take modulo 1000000, and format with six decimal digits and leading zeros. Use exact strings from the signed invitation, without normalization. Six-digit codes can collide; a different key is not mathematically guaranteed to produce a different code.

The persisted join ledger has public keys, signed proofs, IDs, timestamps, decision state and an approved public Contract. It keeps invitation consumption permanently. Runtime vault references/private keys and personal labels are not serialized by the correspondence identity codec. Host disk persistence and backup rollback protection remain integration responsibilities.

## Leveransebevis

Formålsutskrift: `bolk2-formaalsproeve-innmelding.txt` (bare abstrakte E/H/I og testutfall; ingen nøkler eller ekte identiteter). Grunnmur: eksisterende `wp-cellprotocol-grunnmur.sh` med argument `codex/korr-relasjonscelle-20261007`, som skriptjobb i bane b. Fokus: b-p2-korr-focused-r4-20261008. Fullport: b-p2-korr-full-grunnmur-20261008. Push/CI: b-p2-korr-push-ci-20261008. Arbeidstreet er rent og beholdt låst. Læring om integrasjonsgrensen er fanget og følger kandidatens dokumentasjon i git; global learning-strict er fortsatt rød på andre, eksisterende åpne poster.

STATUS: LEVERT


## Tillegg p3 — autentisert bro med sign-only requester (2026-10-08)

PR #63 er fortsatt åpen kladd. Nytt hode: `b95a0886f730cf9001af69a9b82c9b5eef93aaa8`, gren `codex/korr-relasjonscelle-20261007`, fra rent `a2b1fc2f8f6c1b9d7887a018d89c959138418d2d`. Ingen merge eller tag.

Join-forespørselens X25519-nøkkel bindes av signaturen over den kanoniske forespørselen, inklusive celle/invitasjon, signeringsnøkkel, X25519 og tidspunkt. UUID og signeringsnøkkel må samsvare med autentisert requester. Requesterens egen X25519 kan mangle; finnes den, må den samsvare. Transportprincipal, PublicIdentity og brorettigheter er ikke utvidet.

| Krav | Test | Utfall | Bevis |
| --- | --- | --- | --- |
| Sign-only requester kan melde seg inn | `testSignOnlyBridgeRequesterJoinsAcceptsAndReadsEncryptedMessage` rekonstruerer requester med `BridgeChannelAuthentication.PublicIdentity.makeIdentity()` og eget isolert nøkkellager | Bestått: pending → eiergodkjenning → signert avtale/resultat → agreement.accept → krypterte meldinger begge veier | `HAVEN-Deploy/_handoff/KORR-UT/p3/r1.log`; `Tests/CellBaseTests/CorrespondenceRelationshipTests.swift` på nytt hode |
| Endret X25519 etter signering, UUID, usignert, feil celle og annen ekte signerer avvises | `testSignOnlyBridgeRequesterRejectsAlteredJoinProofsAndResultSigner` | Bestått; alle negative varianter avvist, gyldig variant pending | Samme fokuslogg og testfil |
| X25519 kontrolleres når transportidentiteten faktisk har den | Begge nye tester har motstridende requester-X25519; avtaleaksept testes også | Bestått; motstrid avvist | Samme fokuslogg og testfil |
| join.result bindes til samme UUID og signeringsnøkkel | Annen kontrollert signerer, samt samme UUID med annen nøkkel, forsøker resultathenting | Bestått; ingen resultatutlevering | Samme negative test |
| Andre join-/avtaleveier følger samme grense | Kildereview av agreement.accept, join.decide/result og revocation; eksisterende avtale-/korrespondansetester | Ingen resterende krav om requester-X25519 uten alternativ signaturbinding | `Documentation/CorrespondenceJoin.md`; `HAVEN-Deploy/_handoff/KORR-UT/p3/source-review.md` |
| Ingen tester fjernet eller svekket | Bevaring av eksisterende testmetoder og assert-linjer, samt uavhengig kildereview | 19 → 21 testmetoder; alle 102 tidligere linjer med XCTAssert*/XCTFail beholdt (nå 113) | `HAVEN-Deploy/_handoff/KORR-UT/p3/test-preservation.json`; kildereview |
| Fokusert testport i bane b | `ExternalAgreementAdmissionTests|Correspondence` | 77 tester, 0 feil | `HAVEN-Deploy/_handoff/KORR-UT/p3/focused-r1.txt`; `p3/r1.log` i samme mappe |
| Fullport som skriptjobb i bane c | `HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh codex/korr-relasjonscelle-20261007` | Bygg exit 0; tester exit 0; 1634 XCTest-utfall: 1629 bestått, 5 hoppet over, 0 feil | `HAVEN-Deploy/_handoff/KORR-UT/p3/fullport.txt`; `HAVEN-Deploy/_handoff/GRUNNMUR/logg-b95a0886f7/build.log` og `test.log` |

`agreement.accept` henter avtalesubjektets X25519 fra eierens signerte kontrakt og kontrollerer subject/signatory-samsvar. Presenterens UUID, signeringsnøkkel og levende signaturbevis kontrolleres fortsatt; dersom presenter-X25519 finnes, må den samsvare med kontrakten. Eierens X25519 kontrolleres mot lagret celleeier. `join.decide` bruker signerte forespørselsnøkler fra pending-ledger og lagret eier. `join.result` kontrollerer UUID/signeringsnøkkel. Tilbakekalling bruker eierens signatur og celle/domene, og trenger derfor ikke requester-X25519.

Fullporten kjørte på macOS 27.0, Xcode 27.0 (27A266a), Swift 6.4. Bygg tok 189 sekunder og tester 105 sekunder. Tallet 1634 er summen av XCTest-utfall på tvers av testbundler, ikke den siste enkeltbundle-oppsummeringen på 1605.

Testene bruker den samme principal-rekonstruksjonen som broen, gjennom resolver/celle og eget nøkkellager. Dette er regresjonsbevis for kodeendringen; p3 har ikke kjørt en ny ekte WebSocket-/stagingrunde, deploy eller installerbygg.

En første køinnmelding fikk feil filnavn (`.job.job`) og ble avvist før bygg/test startet. Korrekt innmelding kjørte deretter fullporten. Ingen testfeil skjules av dette; se `HAVEN-Deploy/_handoff/KORR-UT/p3/queue-filename-error.txt`. Publiseringsjobben traff sin ti minutters watchdog mens to CI-sjekker fortsatt kjørte (exit 143); en separat lesende køjobb fulgte de samme kjøringene videre. Ingen CI-omkjøring er bestilt.

CI på publisert hode (ingen omkjøring):

| Sjekk | Utfall | Bevis |
| --- | --- | --- |
| Persisted Cell file bounds | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37729740225/job/113155920475) |
| regression | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37729740179/job/113155920753) |
| bounded synthetic runtime matrix | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37729740186/job/113155920713) |
| Vapor identity vault strict storage | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37729740189/job/113155920669) |

Eksakt hode, OPEN/kladd og fire SUCCESS er lagret i `HAVEN-Deploy/_handoff/KORR-UT/p3/ci.json`. Begge p3-læringer er oppdatert og distribuert; global læringssjekk har eldre åpne poster utenfor p3.

STATUS: LEVERT


## Tillegg p4 — fornyelse etter utløp gjennom join (2026-10-08)

Grunnlag: godkjent FORMAALSSPEC C3 og k1s koordineringsforespørsel 04:32Z. CellProtocol-kandidat fra rent p3-hode `b95a0886f730cf9001af69a9b82c9b5eef93aaa8`; nytt hode `3d6be30a108c72aeb3ce632a8b08f49ca3d9586c` på `codex/korr-relasjonscelle-20261007`. PR #63 beholdes OPEN/kladd; ingen merge eller tag.

`join.decide` erstatter kontrakten på samme godkjente requestID. Ny kontrakt må ha en annen kontrakt-UUID, strengt nyere issuedAt og senere expiresAt; Agreement-ID, celle, domene, signerings-/X25519-nøkler og faste rettigheter bevares. Utløp tillater fornyelse, men registrert tilbakekall avviser fornyelse av den godkjente forespørselen. `join.result.<requestID>` kan hentes med samme UUID/signeringsnøkkel uten aktivt medlemskap. Resultatet installeres først når den inviterte presenterer det med `agreement.accept`.

| Krav | Test | Utfall | Bevis |
| --- | --- | --- | --- |
| Fornyelse etter utløp, samme requestID/Agreement-ID; siste kontrakt hentes og aksepteres | `testJoinRenewalAfterExpiryReplacesContractAndSurvivesDecode` | Bestått; utløpt tilgang avvist før fornyelse, nytt resultat bevart gjennom decode, avtaleaksept gjenoppretter tilgang | `HAVEN-Deploy/_handoff/KORR-UT/p4/r2.log`; `Tests/CellBaseTests/CorrespondenceRelationshipTests.swift` på nytt hode |
| Samme fornyelse over broens sign-only requester | `testSignOnlyBridgeRequesterRenewsAfterExpiryAndAcceptsLatestResult` | Bestått med `BridgeChannelAuthentication.PublicIdentity.makeIdentity()` og inviterte eget isolerte nøkkellager | Samme fokuslogg og testfil |
| Medlems- og kontraktlistene vokser ikke | Begge fornyelsestestene kontrollerer authorization snapshot før/etter | Bestått; én kontrakt erstattes av den nye, samme medlemsantall; join-godkjenning alene installerer ingen ny kontrakt | Samme fokuslogg og testfil |
| Eldre/gjentatt beslutning, signerings-/X25519-bytte, flere rettigheter, annen celle/Agreement-ID/eier, samt avslag på godkjent forespørsel avvises | `testJoinRenewalRejectsReplayOlderKeysGrantsCellAndAgreementChanges` | Bestått; 12 negative varianter avvist og lagret resultat uendret. Freshness-variantene holdes aktive slik at utløp ikke maskerer avvisningen | Samme fokuslogg og testfil |
| Nyeste resultat beholdes også etter invitasjonsutløp; sen eldre fornyelse/replay kan ikke overskrive | `testJoinLedgerRenewalIgnoresInvitationExpiryAndRejectsLateReplay` | Bestått; siste kontrakt beholdt, pending-listen tom | Samme fokuslogg og testfil |
| Fornyelse med fersk signatur etter tilbakekall avvises, også etter decode | `testJoinRenewalRejectsFreshSignatureAfterRevocationAndDecode` | Bestått; opprinnelig resultat beholdt og tilbakekalt tilgang fortsatt avvist | Samme fokuslogg og testfil |
| Ventende beslutning kan ikke bli fornyelse etter samtidig godkjenning/aksept/tilbakekall | `testPendingDecisionCannotRenewAcrossConcurrentApprovalAndRevocation` | Bestått; deterministisk pause etter validering, annen beslutning godkjent/akseptert/tilbakekalt, forsinket beslutning avvist | Samme fokuslogg og testfil; `HAVEN-Deploy/_handoff/KORR-UT/p4/source-review.md` |
| Ingen eksisterende test svekket eller fjernet | Byte-sammenligning mot p3 etter at bare det nye tillegget fjernes | Bestått; eksisterende testfil byte-identisk; seks nye tester | `HAVEN-Deploy/_handoff/KORR-UT/p4/test-preservation.json` |
| Fokusert port i bane b | `ExternalAgreementAdmissionTests|Correspondence` | 83 tester, 0 feil, exit 0 | `HAVEN-Deploy/_handoff/KORR-UT/p4/focused-r2.txt`; `HAVEN-Deploy/_handoff/KORR-UT/p4/r2.log` |
| Full grunnmur som skriptjobb i bane c | `HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh codex/korr-relasjonscelle-20261007` | Bygg exit 0, 196 s; tester exit 0, 120 s. 1640 XCTest-utfall: 1635 bestått, 5 hoppet over, 0 feil | `HAVEN-Deploy/_handoff/KORR-UT/p4/fullport.txt`; `HAVEN-Deploy/_handoff/GRUNNMUR/logg-3d6be30a10/build.log` og `test.log` |

Fullport kjørte på macOS 27.0, Xcode 27.0 (27A266a), Swift 6.4. Tallene er opptelling av XCTest-utfall på tvers av bundler, ikke den siste enkeltbundle-oppsummeringen. Testet filinnhold og uavhengig kontroll er bevart i `HAVEN-Deploy/_handoff/KORR-UT/p4/tested-files.json`, `results.json` og `source-review.md` i samme mappe.

Første fokusjobb stoppet i kompileringen av en ny test fordi propertynavnet var feil (`publicSigningKey`); rettet til eksisterende `publicSecureKey`. Ingen test kjørte i det forsøket. Feilbeviset er bevart i `HAVEN-Deploy/_handoff/KORR-UT/p4/r1.log`. Uavhengig Codex-kildekontroll (samme modell som hovedtråden) fant ett konkret pending/approved-samtidighetshull før sluttrettingen; ny kontroll vurderte rettelsen lukket, og regresjonstesten bestod.

Testene beviser celle-/resolver-API og broens principal-rekonstruksjon med eget nøkkellager, ikke en ny ekte WebSocket-/stagingrunde, deploy, installer eller klientens automatiske polling. Disse integrasjonsdelene er ikke kjørt i p4.

P4-læringen er oppdatert og distribuert. Global `haven_learn.py check --strict` er fortsatt rød på eldre åpne poster utenfor p4; egen post er applied/synced. Bevis: `HAVEN-Deploy/_handoff/KORR-UT/p4/learning-sync.txt` og `learning-check.txt` i samme mappe.

CI på eksakt publisert hode (første kjøringer, ingen omkjøring):

| Sjekk | Utfall | Bevis |
| --- | --- | --- |
| Persisted Cell file bounds | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37733147941/job/113166632240) |
| regression | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37733148098/job/113166632864) |
| bounded synthetic runtime matrix | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37733147856/job/113166632271) |
| Vapor identity vault strict storage | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37733147931/job/113166632186) |

Alle fire SUCCESS, eksakt hode og OPEN/kladd er verifisert samlet i `HAVEN-Deploy/_handoff/KORR-UT/p4/ci.json`. Jobbene er `b-p4-korr-focused-r2-20261008`, `c-p4-korr-full-grunnmur-20261008` og `b-p4-korr-push-ci-20261008`; publiseringsjobben er avsluttet. Arbeidstreet er rent og låst.

STATUS: LEVERT


## Tillegg p5 — separat signert eieravtale for inviteIdentities (2026-10-08)

Bestilt kontrakt beholdt. Regresjonen kom fra PR #63-commit `adfb453`: `inviteIdentities` fikk en UUID-only guard som avviste også den separat autoriserte eierdelegaten. Eieravtalerettingen er commit `9cd04b2a870543e940a181bd1c0d86889328f265` fra rent `3d6be30a108c72aeb3ce632a8b08f49ca3d9586c`. Sluttkandidaten med nedenfor beskrevne Scanner-fixture-retting og checked-await-fixture er `36959ae4a114503b08ff85785e0d73f865d4758e`, gren `codex/korr-relasjonscelle-20261007`. PR #63 beholdes OPEN/kladd; ingen merge eller tag.

Håndtereren bruker eksisterende verifiserte avtaler: eierens utstedersignatur, binding til subjektet og levende requester-proof, domene, tidsvindu, revocation, mal og eventuell cellebinding kontrolleres fortsatt av GeneralCell. Den krever i tillegg den komplette, eksakte eiermalens navn, grants, tomme conditions og policybinding. En ordinær medlemsavtale eller en delvis eieravtale gir ingen invitasjonsrett. Separat autorisert requester kan gjenta invitasjon av eksisterende medlem med `unchanged`; en batch med nye identiteter avvises før endring. Nye innslipp krever fortsatt faktisk eiers proof og eierens signatur (D3), uten eiersubstitusjon.

| Krav | Test | Utfall | Bevis |
| --- | --- | --- | --- |
| Separat signert eieravtale godtas idempotent gjennom resolver | `testS54SeparateOwnerAgreementAllowsIdempotentInviteThroughResolver` | Bestått; to invitasjonskall i samme test ga unchanged, samme fingerprint, kontrakt- og medlemsantall | `HAVEN-Deploy/_handoff/KORR-UT/p5/r5.log`; `Tests/CellBaseTests/CorrespondenceCellTests.swift` på sluttkandidaten (første port: r3.log) |
| Ordinært medlem og ekstern invitasjon avvises | Ny S54-test samt eksisterende `testS2TemplatesAreExactAndResolverDeniesOwnerSurfaceToExternalAgreement` | Bestått; medlem/outsider og faktisk external-avtale avvist med grantNotHeld; external-malen beholder fire grants | Samme fokuslogg/testfil |
| Utløpt eller endret eieravtale, delvis eiermal og avtale for annen celle avvises | `testS54RejectsExpiredAlteredPartialAndWrongCellOwnerAgreements` | Bestått; hostile persisted state går gjennom normal resolver-verifikasjon; gyldig kontroll blir unchanged, alle fire negative avvist uten medlemsendring | Samme fokuslogg/testfil |
| D3: separat avtale gir ingen signeringsrett for nye innslipp | Ny positiv S54-test prøver også ny identitet; kildekontroll | grantNotHeld, fingerprint uendret; faktisk eier må signere ny Contract | Samme fokuslogg; `HAVEN-Deploy/_handoff/KORR-UT/p5/source-review.md` |
| HavenAgentD S54 mot kandidat uten endring i k2 | Eksisterende `S54ResolverDeniesExternalInvitationAndAcceptsSeparateOwnerAgreement` og `S54ProfileContractCannotAuthorizeAnotherCell` | 2 tester bestått, 0 issues; bygg/test exit 0 | `HAVEN-Deploy/_handoff/KORR-UT/p5/s54-third.log` og `s54-third-result.txt`; første kjøring `s54.log`/`s54-result.txt` |
| K2-kilde bevares | Før/etter SHA-256 av Sources, Tests, Scripts og begge package-filer | Alle 213 filer uendret; separat kopi, lokal CP-package-overstyring kun i kopien, ingen commit i HavenAgentD | `HAVEN-Deploy/_handoff/KORR-UT/p5/s54-source-before.json`, `s54-source-unchanged.json` og `s54-third-source-check.json` |
| Ingen eksisterende test svekket/fjernet | Byte-sammenligning etter at bare de to nye testmetodene tas ut | Opprinnelig Correspondence-testfil byte-identisk; Scanner beholder alle assertions og fristen med sterkere ventebetingelse; Vapor-fixturen beholder alle assertions og faktisk NIO/produksjonsbane | `HAVEN-Deploy/_handoff/KORR-UT/p5/test-preservation.json` og `scanner-assert-preservation.json` |
| Fokusert bane b på sluttkandidaten | ExternalAgreementAdmissionTests + Correspondence + ScannerPeerAuthenticationTests + VaporWebSocketAdmissionTests + BridgeChannelWebSocketTests | 135 tester, 0 feil, exit 0; første eieravtaleport var 85/0, mellomport 118/0 | `HAVEN-Deploy/_handoff/KORR-UT/p5/focused-r5.txt` og `r5.log`; første port `focused-r3.txt`/`r3.log` |
| Full grunnmur, bane c, eksakt committet hode | `HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh codex/korr-relasjonscelle-20261007` | Bygg exit 0; tester exit 0; 1643 XCTest-utfall: 1638 bestått, 5 hoppet over, 0 feil | `HAVEN-Deploy/_handoff/KORR-UT/p5/third-fullport.txt`; `HAVEN-Deploy/_handoff/GRUNNMUR/logg-36959ae4a1/build.log` og `test.log` |

Fullport kjørte på macOS 27.0, Xcode 27.0 (27A266a), Swift 6.4. XCTest-antall er summen på tvers av bundler. Testet filinnhold og patch er bevart i `HAVEN-Deploy/_handoff/KORR-UT/p5/tested-files-third.json` og `candidate-third.patch`. Uavhengig Codex-kildereview (samme modell som hovedtråden) fant ingen konkret sikkerhetsfeil i sluttkandidaten. Eksisterende lokale kontrakter uten targetCellUUID beholder sin tidligere regel; cell-bound avtaler for annen celle avvises. Varighet må være gyldig og innen aktiv mal, ikke identisk med ett år.

Første CI på `9cd04b2` ga én faktisk XCTest-feil: eksisterende `ScannerPeerAuthenticationTests.testMissingReceiptDeadlinePhysicallyRetiresOnlyExpiredPeer`, 348 beholdte byte i stedet for 0. Logisk `closed` og fysisk antall kunne observeres før den asynkrone bytefrigjøringen var fullført. Commit `27000be` endrer bare testens ventebetingelse til å vente på alle opprinnelige oppryddingskrav innen samme `3000 × 1 ms`-grense. Alle assertions, timerkravet og den friske søskenkanalen beholdes. Uavhengig kildereview bekreftet rekkefølgen; ingen produksjonskode ble endret av denne oppfølgingen. Første røde kjøring og de tre grønne sjekkene på det første hodet er bevart i `HAVEN-Deploy/_handoff/KORR-UT/p5/ci-first.json` og `ci-regression-first.log`. Assertion-bevis: `scanner-assert-preservation.json` i samme mappe. Ny fokusport, full grunnmur og S54 ble bestilt før ny push; ingen uendret CI-jobb er kjørt om.

Første fokusinnmelding ble avvist før kjøring fordi promptfilen manglet. Neste bygg stoppet på en ny testfixture som brukte privat auditor; ingen tester kjørte da. Fixturen ble rettet til serialisert tilstand og normal resolver-verifikasjon. Begge feilspor er beholdt; ingen assert er svekket.

S54 kjørte fra kopi av k2s aktuelle arbeidstre, inklusive dets ucommittede kildearbeid; bare kopiens manifest fikk en lokal CP-package-overstyring. Sammenligning av Package.resolved viser bare at remote CellProtocol-pinnen er fjernet av den lokale overstyringen; alle andre dependency-pinner er uendret (`HAVEN-Deploy/_handoff/KORR-UT/p5/s54-package-graph.json`). Dette beviser den eksisterende HavenAgentD-prøven mot kandidatens kilde, ikke remote pin-resolusjon, en full HavenAgentD-port, faktisk WebSocket-/stagingrunde, GUI, deploy eller installer. Ingen annen produktkilde enn CellProtocol ble endret av p5.

P5-læringen er applied/synced og distribueres med kandidatens dokumentasjon gjennom git. Global learning-strict er fortsatt rød på andre eksisterende poster.

CI på eksakt publisert hode: **4/4 SUCCESS**, samlet kontrollert med OPEN/kladd i `HAVEN-Deploy/_handoff/KORR-UT/p5/ci-third.json`. Normal testsuite og alle tre TSAN-pass er grønne; rålogg `ci-regression-third.log` i samme mappe. Ingen uendret CI-jobb er kjørt om.

Andre CI på `27000be`: normal testsuite og TSAN-pass 1 og 2 bestod; pass 3 rapporterte datarace i NIOs `EventLoopFuture.get()`/`UnsafeContinuation.resume` under VaporWebSocketAdmissionTests. Loggen identifiserer ikke hvilket get-kall og beviser ikke en upstream-feil eller false positive. En privat helper i denne testfixturen bruker checked continuation med `Value: Sendable`, én faktisk NIO whenComplete-callback og én resume(with:). Den nye testen kontrollerer umiddelbare og event-loop-fullførte verdier, samme kastede feil og uendret cancellation-adferd. Alle eksisterende assertions, faktisk sockettransport og produksjonens get-kall beholdes; ingen TSAN-suppression, testekskludering eller nye unchecked Sendable. Andre røde CI er bevart i `HAVEN-Deploy/_handoff/KORR-UT/p5/ci-second.json` og `ci-regression-second.log`; assertion-bevis i `vapor-assert-preservation.json`. Lokal TSAN: 17 tester, 0 feil, exit 0 (`HAVEN-Deploy/_handoff/KORR-UT/p5/tsan.log` og `tsan-result.txt`). CI på eksakt publisert hode oppgis nedenfor.

Første grunnmurkjøring på sluttkandidaten bygde grønt, men diskvakten avviste teststart (exit 75; 0 tester). Etter at den samtidige S54-jobben fullførte ordinær managed-cache-GC, godkjente vakten ny kjøring på samme hode: bygg 48 s, full test 150 s, begge exit 0. Ingen terskel eller lease ble overstyrt. Første stopp og logger er bevart i `HAVEN-Deploy/_handoff/KORR-UT/p5/third-fullport-capacity-stop.txt` og `HAVEN-Deploy/_handoff/GRUNNMUR/logg-36959ae4a1-capacity-stop/`.

| Krav | Test | Utfall | Bevis |
| --- | --- | --- | --- |
| CI på eksakt hode | Persisted Cell file bounds | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37765453980/job/113271889256) |
| CI på eksakt hode | regression | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37765454201/job/113271889466) |
| CI på eksakt hode | bounded synthetic runtime matrix | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37765453960/job/113271888379) |
| CI på eksakt hode | Vapor identity vault strict storage | SUCCESS | [GitHub Actions](https://github.com/Digipomps/CellProtocol/actions/runs/37765454135/job/113271890913) |

Arbeidstreet er rent og beholdt låst. Slutthodet er publisert i eksisterende kladd-PR #63; ingen merge eller tag.

STATUS: LEVERT
