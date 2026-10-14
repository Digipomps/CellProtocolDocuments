# Bolk 3 — integrasjonsgrense under arbeid

Dette er et kildeinventar og en integrasjonsavklaring under arbeid, ikke funksjonsbevis
eller en ferdig leveranse. Ingen ny rute er hevdet implementert her.

## Vertskandidaten lest

Bolk 4 har gjenopptatt kildearbeidet etter den tidligere stoppmeldingen.
`_worktrees/cellscaffold-korr-staging-20261007/Documentation/Correspondence/RelationshipHosting.md`
og `Sources/App/Services/CorrespondenceRelationshipHost.swift` i samme arbeidstre
beskriver en factory med publisher `CorrespondenceRelationships`, proof-resource
`49BFEC72-9D56-4532-AB65-76F2406F5244` og SET `create` med tomt objekt.
Svaret har `uuid`, `publisher`, `address`, `status`. Relasjonens publisher er
`Correspondence-<uuid>`; celle-UUID og publishernavn er altså forskjellige.
Opprettelse er ikke idempotent. Koden er en kandidat, ikke en deployet tjeneste.

HavenAgentDs nåværende målvalidering forutsetter UUID som publisher. Klienten
må kunne beholde både UUID (signert kontrakt/kryptobinding) og det avledede
publishernavnet (bare transport). Den delte autentiserte broen bruker session-
ruta, og den logiske kanalens mål må være riktig publisher. Dette er en
transporttilpasning, ikke en ny medlemsrett.

## Manglende innmeldingskontrakt

Det leste vertslaget har opprettelse, videreføring av CellProtocol-operasjoner,
lagring og readiness. Det har ennå ingen kontrakt for følgende C1/C2-flyt:

1. Eiersignert invitasjon gir en ikke-admittert mottaker rett til å sende sin
   offentlige signerings- og X25519-beskrivelse og sitt nøkkelbevis til eieren.
2. Eierens Mac får forespørselen uten at verten får eierens private nøkkel.
   Mottakeren og eieren beregner samme seks-sifrede kode fra samme, verifiserte
   nøkkelbinding; personnavnet forblir bare på eierens Mac.
3. Mottakeren mottar den ferskt eiersignerte, cellebundne Contract etter
   godkjenning, og sender den med `agreement.accept`. Avslag, utløp og replay
   må gi et entydig resultat. Ingen forhåndssignert lenke gir medlemskap.

Den eksisterende klientens HTTP-innmelding er ikke et bevis for denne nye
flyten. Det leste nye vertslaget implementerer ikke den HTTP-kontrakten.
CellProtocols `ChatInvitationProofUtility` har signert invitasjonsartefakt og
mottakeraksept som kan vurderes som grunnlag; den automatiske
`audience.acceptInvitationArtifact`-flyten skal ikke brukes som erstatning for
fersk, menneskelig godkjenning og cellebundet Contract.

Alternativene er å utvide native vertslaget med en uttrykkelig, begrenset
forespørsels-/beslutningsformidling, eller å levere en annen avtalt
innmeldingskontrakt som gir de samme garantiene. Ingen av dem er implementert
av bolk 3. CellScaffold/CellProtocol er utenfor denne jobbens skriveomfang.

## Signering på Macen

Første pakke bruker deltakerens eksisterende identitetsmodell; separat
agentidentitet/delegering er uttrykkelig utelatt i FORMAALSSPEC §2.
En begrenset tjeneste med samme eieridentitet er et implementasjonsalternativ.
Den må eie både eierens private signeringskapabilitet og eierens autentiserte
bro-kanal. Å eksponere generell nøkkelbevis-signering til agentprosessen kan
gi den en eierkanal med flere operasjoner enn vanlig lesing og sending.

Den vanlige agentflaten må derfor være typede meldings-/vedleggsoperasjoner,
uten rå signering, nøkkel-eksport eller vilkårlige bridge-kommandoer. Hvert
administrativt dokument må konstrueres i tjenesten og signeres etter fersk
`userPresence`. Nøkkelringen skiller ikke i seg selv mellom to dokumenttyper
som signeres med samme Ed25519-nøkkel; det skillet må håndheves av den betrodde
tjenesten. Dette er ikke etablert i den nåværende rå-nøkkel-klienten.

Ingen GUI-, Touch ID- eller installerakseptanse er hevdet i dette notatet.

## Beslutning mottatt 00:37Z

Korrespondanse-tråden har navngitt grenseflaten i
`handoff/BESLUTNING-20261008-innmelding-og-vedleggsrot.md`: `join.request`,
`join.pending`, `join.decide`, `join.result`, målrettet join-Flow og felles
seks-sifret kodehjelper. Alternativspørsmålet ovenfor er dermed besvart som
grenseflate. Protokoll-/vertsimplementering og eksakte Swift-/wire-typer er
fortsatt ikke verifisert eller tilgjengelige i den pinnede 7f87b8e-kandidaten.
Bolk 3 bygger klienten mot den leverte kontrakten når typene foreligger.
Dette er ikke et funksjonsbevis eller en ny påstand om ferdig innmelding.

## 08.10: C3 renewal delivery gap on published p2 head

Read-only source check on `a2b1fc2f8f6c1b9d7887a018d89c959138418d2d`:
`CorrespondenceJoinLedger.decide` accepts only `pending`; `join.result.<requestID>`
returns the already approved Contract. `agreement.accept` proves the Contract's
subject, so the owner cannot apply the invitee's renewal by submitting it as the
owner. k1's existing socket test attempts a freshly owner-signed renewal submitted
by the invitee; that full socket test has not passed, and its design does not prove C3's owner button plus automatic client retrieval
following expiry. This is not a new product choice: FORMAALSSPEC C3 already
requires that behavior.

Proposed minimal upstream integration (not implemented): let an owner-approved
request be renewed through `join.decide` with a fresh later-expiring Contract,
keeping the exact Cell, signing/X25519 identities and grant set. Store the latest
approved Contract in that request; the same requester key can fetch it through
its existing `join.result` even after expiry, then submit `agreement.accept`.
Reject a different identity/key, grants, stale signature, non-later expiry,
replayed old decision and post-revocation replay. Repeated invitation use must
remain rejected. k1 must store requestID locally for owner renewal and requester
refresh; that storage and refresh integration are not implemented. This needs p2 source/tests, then k1's actual end-to-end expiry/renewal
proof. k1 must not claim the existing invitee-submitted test proves this path.
