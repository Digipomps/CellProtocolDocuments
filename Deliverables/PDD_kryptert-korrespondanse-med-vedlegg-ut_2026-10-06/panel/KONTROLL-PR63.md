Merge: ja etter rettelsene under

Leser: Claude Opus (Fabel er uten kvote til 08.10 kl. 10:00Z), bestilt av korrespondanse-tråden 07.10. PR-hode `7f87b8e`.

# Uavhengig sikkerhetskontroll – CellProtocol PR #63 (korr, 7f87b8e mot 68069b6)

Kun lesing, Swift er ikke kjørt. Linjenumre gjelder 7f87b8e.

## Kort konklusjon

Den kryptografiske innslippskjeden holder. Jeg fant ingen vei der noen uten eierens private nøkkel får
medlemskap, lesetilgang eller kan tilbakekalle eller endre andres tilgang via `agreement.accept` eller `agreement.revoke`.
Bindingen (`targetCellUUID`, `signaturePurpose`) ligger i signerte bytes (Contract.swift:80-91, 225-238).
Kontrakter for andre celler, fjernet eller endret binding og formål, framdaterte kontrakter
(GeneralCell.swift:1490/1519, uten skew), forfalskede tilbakekall og avspilte tilbakekall avvises.
Avspilling er dekket av cutoff `issuedAt > revokedBefore` (GeneralAuditor.swift:494-501).
Den endelige kontrollen ligger i auditor-actoren (GeneralAuditor.swift:454-473), så await-kappløp i GeneralCell-laget lukkes.
MÅ 1 fra proben er rettet i GeneralCell- og auditor-laget. Det står igjen et tilsvarende hull ett lag opp:
CorrespondenceCells egen krypteringsmedlemsliste (MÅ 1 under).

## MÅ (før merge)

1. **Krypteringsmedlemslisten følger ikke aktiv autorisasjon. Medlemmer med utløpt kontrakt, og i et kappløp også
   tilbakekalte medlemmer, blir værende som påkrevde mottakere.**
   - `refreshAuthorizedMembership` (CorrespondenceCell.swift:301-309) bygger `memberIdentityUUIDs` fra
     `authorizationMembers()`. Det er auditorens rå medlemsliste, og den filtreres aldri på `temporalStatus`.
     Et medlem med utløpt kontrakt blir derfor stående i listen helt til noen tilbakekaller eller fjerner det.
   - `envelopeRecipientsMatchCurrentMembership` (CorrespondenceCell.swift:661-665) krever eksakt mengdelikhet med listen.
     Avsender må derfor pakke innholdsnøkkelen også til det utløpte medlemmet, ellers avvises meldingen.
     `attachments.prepare` gjør det samme (CorrespondenceCell.swift:1023).
   - Kappløpet: `acceptExternallySignedAgreement` → `refreshAuthorizedMembership` leser medlemmer (await) og skriver
     først etterpå. Et samtidig tilbakekall kan fullføre sin egen refresh i mellomtiden. Da overskriver
     aksept-refreshen resultatet med en liste der det tilbakekalte medlemmet fortsatt er med (CorrespondenceCell.swift:289, 295, 299, 302-308).
     `memberIdentityUUIDs` er dessuten en vanlig klasseegenskap uten lås eller actor.
   - Server-gatingen holder fortsatt, fordi Meddle-grant og Flow sjekkes per element (FeedAuthorizationRegistry.swift:104-111).
     Men ciphertext som lagres på verten blir dekrypterbar for det tidligere medlemmet. Et utløpt eller tilbakekalt
     medlem som samarbeider med vertsoperatøren, eller som får tak i en lekket backup, kan da lese nye meldinger.
     Det bryter målet om at verten bare skal se krypterte konvolutter.
   - Retting:
     - Beregn listen fra kontrakter som er aktive nå (`relevantContracts`/`temporalStatus == .active`) pluss eier.
     - Serialiser oppdateringen: en actor, eller lås og revisjonsnummer slik at en eldre snapshot ikke kan overskrive en nyere.
     - Kjør oppdateringen også ved kontraktutløp, eller lat ved `sendMessage`/`inbox`.
     - Sjekk fingerprint på nytt rett før `insert` i `sendMessage`. Sjekken på 489-500 skjer før await på 527-529.
   - Legg til tester for et utløpt medlem i mottakermengden og for aksept mot tilbakekall i CorrespondenceCell-laget.

2. **Filnavn og lokale stier ligger i klartekst hos verten.** Dette må rettes, eller Kjetil må akseptere det eksplisitt.
   - `CorrespondenceAttachmentRequest.metadata` (navn, medietype, størrelse) sendes i klartekst ved `attachments.prepare`.
   - Den lagres i `state.json` (CorrespondenceAttachmentStorage.swift:239-250) og returneres av `attachments.metadata` (318-322).
   - `attachments.probe` uten `confirmation` returnerer `sourceDescriptor` med `referenceURL`, det vil si vertens lokale filsti,
     og navn (CorrespondenceCell.swift:1013-1019, Storage:198-202). Dette gjelder enhver `sourceID` og ethvert medlem,
     uten binding til en sendt melding.
   - Navnet finnes allerede signert og kryptert i det indre manifestet (CorrespondenceAttachment.swift:30). Serverkopien er derfor unødvendig.
   - Docs/CorrespondenceAttachments.md:66 sier at visning før henting inneholder navn, men sier ikke at verten ser det.
   - Retting: fjern `name` fra metadata som verten ser (behold byteCount og mediaType ved behov). Alternativt kan dette
     dokumenteres og aksepteres eksplisitt i PR-en. Bind også `probe` og `sourceDescriptor` til en publisert melding og mottaker.

## Svar på kontrollspørsmålene

1. **Uautorisert innslipp, lesing eller tilbakekall: ingen vei funnet.**
   - Kontrakter for andre celler, uten binding og med feil formål avvises (1488-1500).
   - Subjekt-nøkkelbevis kreves (`checkIdentityOrigin`, 1498). Nøkkelbytte i avtalen avvises (CorrespondenceCell.swift:274-283).
   - Grantene må være eksakt like malens (286-287). Varigheten er begrenset av malen (GeneralCell.swift:1602).
   - Fornyelse kan bare erstatte kontrakter med senere `expiresAt` (GeneralAuditor.swift:464-470), og eieren må signere.
   - Tilbakekall krever eiersignatur over celle, subjekt, kontrakt, avtale, domene og tid (ContractRevocation.swift:117-133).
   - Verten kan ikke signere selv. Lokal signering (GeneralCell.swift:1420-1448) krever eiernøkkel.
   - Kjent begrensning: se BØR 1.
2. **MÅ 1 fra proben: rettet i autorisasjonslaget.**
   - Cutoff settes ved hver fjerning (GeneralAuditor.swift:476-492) og kontrolleres atomært ved installasjon.
   - Fjerning mens innslipp venter: aksepten krevde `issuedAt <= klokke`. Fjerningens cutoff blir derfor `>= issuedAt`,
     og installasjonen avvises (test ExternalAgreementAdmissionTests:360-376).
   - Snapshot: `revokedBefore` kodes og dekodes (GeneralCell.swift:546, 569) og hydreres (GeneralAuditor.swift:519-531, GeneralCell.swift:2276-2282).
   - Unntak: medlemslisten i korrespondanselaget, se MÅ 1.
3. **Lekkasje**
   - Flow og `state` inneholder bare den ytre konvolutten og ciphertext.
   - Hver Flow-hendelse autoriseres på nytt, så ikke-medlemmer og tilbakekalte medlemmer får ingen hendelser.
   - Filnavn og stier: se MÅ 2. Feiltekster: se BØR 5.
   - Avvisningslogger er generiske (GeneralCell.swift:1479-1534).
4. **Vedlegg**
   - Ikke-medlemmer avvises (CorrespondenceCell.swift:950-957 og grant-sjekk). Eierens vedlegg bindes til `agreementID == cell.uuid`.
   - Utløp sjekkes ved hver tilgang og ryddes av en timer og ved oppstart (Storage:162-177, 255-268, 309-316).
   - Tilbakekalte medlemmer mister tilgang via grant-sjekk. Bytene lever til meldingen utløper, som forventet.
   - Se BØR 7 og 10.
5. **Bakoverkompatibilitet: OK.**
   - Felt med nil utelates av syntetisert Codable, både i `Contract` og `SigningPayload`. Eldre signerte bytes er derfor uendret
     (test ExternalAgreementAdmissionTests:197-212).
   - Atferden for andre celler endres på tre punkter:
     - `removeMember` setter nå en varig cutoff for alle celler (2069-2097). Lokal re-innslipp får fersk `issuedAt` (1428) og er testet.
     - `Contract.signed` lagrer nå offentlige snapshots av utsteder og subjekt for alle kallere (Contract.swift:106-107).
       Det fjerner properties, grants og homeVaultReference. Ingen bruk av disse ble funnet.
     - `revokedBefore` skrives alltid i snapshot (GeneralCell.swift:569).
6. **Testene**
   - Separate vaults (E/H/I og A/B/S) brukes. Debug-flagget assertes som av.
   - Negative tester starter fra autentiske signerte bytes (positiv kontroll i `signed()`, ExternalAgreementAdmissionTests:64-79).
     De er altså ikke tautologiske. Svakheter: se BØR 12.

## BØR

1. `agreement.revoke` kan ikke tilbakekalle en kontrakt som ennå ikke er presentert. `applyRevocation` krever installert kontrakt
   (GeneralAuditor.swift:494-501, GeneralCell.swift:1548-1552). En invitasjon sendt til feil person kan bare stoppes med
   en direkte `removeMember.<uuid>` med eierens nøkkelbevis (GeneralCell.swift:1935). Tillat et signert cutoff for et subjekt
   uten installert kontrakt, eller dokumenter at eieren må bruke `removeMember`.
2. Klokkeskew uten toleranse.
   - `issuedAt` og tilbakekallets tid må være `<=` vertens klokke (GeneralCell.swift:1490, 1519, 1545).
   - `removeMember` bruker vertens klokke som cutoff (2075, 2091). Hvis Macen går foran, avvises en fersk signatur.
     Hvis den går bak, avvises en fersk re-innslipp etter `removeMember` til klokken har tatt igjen cutoff.
   - Det feiler lukket, men bør dokumenteres eller håndteres med en eksplisitt feilkode.
3. `replaceAuthorization(... revokedBefore: = [:])` (GeneralAuditor.swift:508): standardverdien gjør at en framtidig kaller i stillhet
   kan slette alle cutoffs. Fjern standardverdien.
4. `sendMessage`: medlemskap og fingerprint sjekkes før await-kall (CorrespondenceCell.swift:489-529) og ikke på nytt før insert (544).
   Sjekk dem på nytt etter siste await.
5. Feiltekster kan inneholde vertsstier og interne detaljer: CorrespondenceCell.swift:530 (`String(describing: error)`)
   og 987 (`localizedDescription` fra `storageFailure`/`cleanupFailure`). Returner bare koder.
6. `inviteIdentities` (CorrespondenceCell.swift:590-627) legger inn UUID-er uten kontrakt. Neste refresh overskriver dem i stillhet
   (301-309). Dette gir to konkurrerende kilder til medlemskap. Deaktiver eller fjern for relasjonscellen.
7. Når et medlem tilbakekalles, kan heller ikke eieren hente vedlegg som medlemmet sendte, fordi
   `memberIdentityUUIDs.contains(request.senderIdentityUUID)` (953) feiler. Meldingene ligger likevel i historikken.
8. Datakappløp: `memberIdentityUUIDs`, `attachmentCells` og `attachmentReservations` er ubeskyttede klasseegenskaper.
   `senderAttachmentCell` (938-947) gjør check-then-set over en await. TSan-jobben dekker ikke samtidig
   aksept, tilbakekall og vedlegg.
9. `fetchOnDemand` lar verten lese kildefila i klartekst og holde sealer-nøkkelen (Storage:331-346). Det er akseptabelt bare når
   verten er avsenderens egen maskin. Blokker `registerAttachmentSource` på serververt, eller dokumenter det tydelig i
   Documentation/CorrespondenceRelationship.md.
10. Én feilet `erase` setter `cleanupFailure` permanent (Storage:127-128, 172-177, 317). Da stopper all senere purge, og
    andre utløpte byte blir liggende på disk (selv om tilgangen avvises). Prøv igjen per oppføring i stedet for å låse hele lageret.
11. `Contract.signed` med `targetCellUUID` setter alltid formålet, men ingen kodesti krever `signaturePurpose == nil` når binding mangler.
    Vurder å avvise `purpose != nil && target == nil` generelt.
12. Testene:
    - Gjenopprettet celle avviser gammel kontrakt (CorrespondenceRelationshipTests:189-191, ExternalAgreementAdmissionTests:244-247),
      men ingen positiv kontroll viser at den samme gjenopprettede cellen godtar en fersk kontrakt. Avvisningen kan dermed skyldes
      noe annet, for eksempel at runtime ikke er klar.
    - Avvisningstestene sjekker bare `.rejected` og ikke `reasonCode`.
    - Det mangler tester for MÅ 1, MÅ 2 og samtidig aksept mot tilbakekall i CorrespondenceCell.
    - Sett `debugValidateAccessForEverything = false` eksplisitt i setUp i stedet for bare å asserte det.
