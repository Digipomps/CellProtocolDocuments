# FORMÅLSSPEC: fornyelse av utløpt korrespondansetilgang

PDD `korrespondanse-fornyelse`, 30.09.2026. Utfører: Losen (claude-cowork). Repo: CellScaffold, gren `claude/korrespondanse-fornyelse-20260930` fra `feec2372`, som er commiten staging kjører.

## §0 Intensjon, ordrett

Kjetil, 30.09.2026: «Vegar fikk denne meldingen - hva er feil?»

Meldingen Vegar fikk: «Sendingen feilet: recipient_not_allowed — "Recipient is not an active peer allowed by this grant." kjetil-vegar-codex-d er altså ikke lenger en godkjent mottaker under korrespondanse-grant-en,»

Kjetils valg, 30.09.2026: «Bygg fornyelse (anbefalt)». Beskrivelsen han valgte:

> Jeg lager fornyelse i serveren, med tester. Når en tilgang er utløpt, gir en ny invitasjon til samme principal, maskin og nøkkel en ny tilgangsforespørsel, som du godkjenner på adminsiden som før. Navnet kjetil-vegar-codex-d beholdes, så Vegar trenger ikke gjøre noe. Dette krever at vi setter det ut på staging, og det løser også at Vegars tilgang går ut 8.10. Du gjør to ting: sier ja til utsettingen og godkjenner på adminsiden.

### Kjetils valg om fornyelse før fristen, 01.10.2026

Vegar ba 01.10 (melding sekvens 15) om å få fornyet sin egen tilgang før den går ut 08.10. Kjetil valgte først «Fornyelse før fristen (anbefalt)». Beskrivelsen sa at Vegar aldri ville miste tilgangen. Det var feil: klienten forkaster beviset sitt ved `setup` og får nytt først med `activate` etter godkjenningen (`CorrespondenceClient.swift` i versjonen med `invite.deviceID`). Etter rettelsen valgte Kjetil «Serverendring, avtalt tid (anbefalt)»:

> Jeg bygger og tester endringen som du valgte og setter den ut på staging etter ditt ja. Du og Vegar avtaler et tidspunkt den siste uka før 08.10. Han kjører oppsettet, du godkjenner med en gang, og han kjører activate. Han er uten tilgang i noen minutter.

Samme dag sa Kjetil «Ja, lag PR (anbefalt)»: PR mot main, og han bestemmer når den merges.

### Påstandene intensjonen bygger på

| Påstand | Status | Kilde |
|---|---|---|
| Serveren avviser en mottaker som ikke selv har en aktiv tilgang | hentet | `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift`, `sendMessage` og `activeGrant` |
| Kjetils tilgang for `kjetil-vegar-codex-d` utløp 29.09 | husket, og støttet av hentet | Oppsettet 08.09 satte fristen til 29.09. Klienten avviser tilgangsbeviset 30.09. Koden gir `recipient_not_allowed` når mottakerens tilgang er utløpt. |
| Det finnes ingen måte å fornye på | hentet | `enroll` sender en eksisterende tilgang til `.existingGrant`. `issueAccessCredential` krever `expiresAt > now`, så resultatet blir `credential_issuance_failed`. Fra en ny enhet blir det `principal_already_enrolled`. |
| Staging kjører `feec2372`, og korrespondansekoden er lik på `origin/main` | hentet | `docker inspect cellscaffold-app-1` 30.09, og `git diff feec2372 origin/main` på korrespondansefilene gir ingen endring |
| Vegars tilgang utløper 08.10 | husket | Oppsettet 08.09 (`--grant-days 30`) |

## §1 Formål med mål

| Id | Formål | Mål (observerbart) | Verifikator |
|---|---|---|---|
| F0 | Kjetil og Vegar kan sende og lese korrespondanse igjen, uten at Vegar gjør noe | Vegars `message.send` til `kjetil-vegar-codex-d` gir `ok`. Kjetils `inbox.list` virker med nytt tilgangsbevis og viser meldingen. | T1 og live på staging (T5) |
| F1 | En utløpt tilgang kan fornyes med en fersk invitasjon og eierens godkjenning, med samme principal, enhet, nøkkel og entitet | En fersk invitasjon gir `pending_approval` med en ny forespørsel, ikke `credential_issuance_failed`. Etter godkjenning finnes en ny tilgang med ny frist. | T1 |
| F2 | Fornyelsen utvider ikke tilgangen | En tilbakekalt tilgang eller principal kan ikke fornyes. En annen enhet eller nøkkel avvises som før. En aktiv tilgang oppfører seg som før. Fornyelsen gir ikke flere mottakere enn invitasjonen. | T2, T3, den eksisterende `testApprovedGrantEnrollmentBehaviorRemainsUnchanged` og T1 (mottakerlisten) |
| F3 | Det er sporbart hva som ble fornyet | Tilgangsforespørselen har `renewsGrantID` som peker på den utløpte tilgangen | T1 |
| F4 | Ingen regresjon | Korrespondansetestene er grønne. Full testmengde gir ingen nye feil mot baseline; testnavnene sammenlignes, ikke bare summen. | T4 |
| F6 | En tilgang kan fornyes de siste sju dagene før fristen, på et avtalt tidspunkt (lagt til 01.10) | En fersk invitasjon gir `pending_approval` med `renewsGrantID` når tilgangen går ut innen sju dager. Den gamle tilgangen er aktiv til eieren har godkjent. Lenger fra fristen er alt som før, og en tilbakekalt principal fornyes ikke. | T6, T7, T8 |
| F5 | Det er ute hos brukeren, ikke bare i koden | Staging kjører commiten, Kjetils tilgang er fornyet, og Vegar når fram | T5 og Vegars bekreftelse |

## §2 Grense

Dette er ikke med:

- automatisk rotasjon eller fornyelse før fristen (punkt 6 i planen fra 09.09)
- endringer i admin-grensesnittet
- produksjon
- andre principals enn Kjetils

Avhengigheter, hver med sin verifikator:

| Avhengighet | Verifikator |
|---|---|
| Jobbløperen på Macen kjører | `runner-*.log` |
| ssh til verten | `docker inspect` virker |
| Image bygges på GitHub for commiten | `haven-ghcr-prefetch <sha> --check` |
| En ny invitasjon til `kjetil-vegar-codex-d` ligger i miljøet | invite-cutover gir `COMMITTED_VERIFIED` |
| Kjetil godkjenner på adminsiden | forespørselen får status `approved` |
| Den nye invitasjonen bærer Kjetils eksisterende `deviceID`. Pilotklienten (`haven-correspondence-mcp setup`) lager ellers en ny tilfeldig enhets-ID, og serveren svarer da `principal_already_enrolled`. Nøkkelen gjenbrukes fra `identity.json` i profilen. | `deviceID` i invitasjonen er lik den i `~/Library/Application Support/HAVEN/AssistantCorrespondence/<profil>/profile.json` |

## §3 Det du kommer til å se

| Leveranse | Type | Hvor |
|---|---|---|
| Testene T1–T4 med ekte utdata | testutdata | `TESTRESULT.md` |
| Et kort for `kjetil-vegar-codex-d` på staging-adminsiden. Du kontrollerer nøkkelen og trykker «Godkjenn meldingsadgang». | kjørende flate | https://staging.haven.digipomps.org/admin/funding |
| Vegar kan sende deg igjen, og innboksen din virker | kjørende flate | korrespondanse-MCP-en din, og Vegar |

## §4 Lærdommer som gjelder

- Tilgangsinvitasjoner og tilganger går ut. Invitasjonen fra 03.09 var ute 06.09 (`correspondence_invite_ops`), og nå gikk en tilgang ut uten at noe varslet.
- «Funksjonalitet som ikke kommer ut til brukerne eksisterer ikke» (Kjetil 29.09). Leveransen er F5, ikke en commit.
- `recipient_not_allowed` dekker tre tilfeller: mottakeren mangler, er ikke tillatt, eller har ikke aktiv tilgang. Planen fra 09.09 (E10) påpekte dette. Feilen i seg selv sier ikke hvilket av dem det er.

## §5 Tester

| Id | Tester | Hvordan | Bevis |
|---|---|---|---|
| T1 | Hele veien. Kjetils tilgang går ut, og Vegar får `recipient_not_allowed`. En fersk invitasjon gir ny forespørsel med `renewsGrantID`. Godkjenning gir nytt bevis. Vegar sender `ok`, og Kjetil leser meldingen. | `swift test --filter AssistantCorrespondenceCellTests/testExpiredRecipientGrantRenewsThroughFreshInviteAndOwnerApproval` | TESTRESULT#t1 |
| T2 | En tilbakekalt principal med utløpt tilgang kan ikke fornyes med fersk invitasjon | ny test | TESTRESULT#t2 |
| T3 | En annen enhet kan ikke fornye en utløpt tilgang (`principal_already_enrolled`) | ny test | TESTRESULT#t3 |
| T4 | Ingen regresjon | alle `AssistantCorrespondence*`-tester, deretter full `swift test` sammenlignet mot baseline | TESTRESULT#t4 |
| T5 | Live | staging-commit, fornyet tilgang, Vegars sending og Kjetils `inbox.list` | TESTRESULT#t5 |
| T6 | En aktiv tilgang med mindre enn sju dager igjen fornyes: forespørsel med `renewsGrantID`, gammel tilgang virker til godkjenningen, deretter bare det nye beviset, med ny frist | `testActiveGrantNearExpiryRenewsBeforeItLapses` | TESTRESULT#t6 |
| T7 | Lenger enn sju dager fra fristen: `already_enrolled`, ingen fornyelse | `testActiveGrantOutsideRenewalWindowKeepsExistingGrantBehavior` | TESTRESULT#t7 |
| T8 | En tilbakekalt principal fornyes ikke før fristen | `testRevokedPrincipalNearExpiryCannotRenewThroughFreshInvite` | TESTRESULT#t8 |

## §6 Åpne spørsmål

- Fornyelse **før** fristen: avgjort 01.10. Kjetil valgte serverendringen med avtalt tidspunkt (§0, F6). Utsettingen på staging er ikke gjort, se STATUS.

## §7 Runder

| Runde | Dato | Hva som endret seg |
|---|---|---|
| 1 | 30.09.2026 | F0–F5, T1–T5. G1 ved Kjetils valg «Bygg fornyelse (anbefalt)». |
| 2 | 01.10.2026 | F6 og T6–T8 lagt til etter Kjetils valg om fornyelse før fristen. Påstanden om at Vegar aldri mister tilgangen ble rettet før valget ble endelig. |
