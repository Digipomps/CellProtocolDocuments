# iPhone-sjekkliste (test.matrise.iphone-checklist og test.apns.real-sandbox-send)

Dette er stegene bare Kjetil kan gjøre, siden de krever en ekte iPhone og Apple-konto. Kryss av og skriv dato/merknad.
Alt som kan kjøres uten telefon (kontrakt, payload, registrering, planlegger, dispatcher) er allerede dekket av testene i TESTRESULT.md.

## A. Før noe sendes (engang)
- [ ] Bundle-ID bestemt: `org.digipomps.haven` eller `havenplayground`? (må være lik i appen, i token-registreringen og i `APNS_BUNDLE_ID`)
- [ ] Push Notifications-capability slått på for appen i Xcode (Signing & Capabilities)
- [ ] APNs auth-nøkkel (.p8) opprettet i Apple Developer (Keys). Noter Team ID og Key ID. Nøkkelen limes aldri inn i chat.
- [ ] Scaffoldet startet med `APNS_TEAM_ID`, `APNS_KEY_ID`, `APNS_PRIVATE_KEY_PATH` (eller `_BASE64`), `APNS_BUNDLE_ID`, og `APNS_USE_SANDBOX=true` for utviklingsbygg

## B. På telefonen
- [ ] Appen bygget og kjørt på iPhone fra Xcode (utviklingsprofil, ikke TestFlight) — da gjelder sandbox
- [ ] Appen ber om varslingstillatelse; trykk «Tillat»
- [ ] Appen registrerer token (signert med entitetens nøkkel). Sjekk: scaffoldets registry har én aktiv oppføring for din entitet (ikke navn, ikke e-post)

## C. Selve testen
- [ ] Fra en annen entitet (annen simulator/Mac/scaffold): opprett invitasjon som navngir din entitet (via relasjoner eller register — WP13)
- [ ] Scaffoldets logg viser `sent` med et `apns-id` (ikke token)
- [ ] Telefonen viser varselet: tittel «HAVEN», tekst «Du har en invitasjon å svare på.» — ingen avsendernavn, ingen annen tekst
- [ ] Trykk på varselet: appen henter billetten, verifiserer den og viser invitasjonen med avsenders navn fra den verifiserte billetten
- [ ] Svar «Ikke nå»: avsenderen ser bare «Besvart»
- [ ] Ny invitasjon, svar «Aldri»: ingen ny varsling, heller ikke ved ny billett fra samme avsender

## D. Negative kontroller
- [ ] Ugyldig/utløpt billett (trykk på et gammelt varsel): feilflate, ikke invitasjon
- [ ] Trukket registrering (slå av varsler i appen): neste invitasjon gir ingen varsel; scaffoldet logger `token_revoked`/`no_registration`
