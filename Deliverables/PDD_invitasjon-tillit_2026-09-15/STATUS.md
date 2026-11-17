# STATUS — invitasjon tillit

- surfaces: binding, cell, gui, skeleton
- tags: invitasjon, onboarding, personvern, relasjon, tillit

## Porter
- G1: godkjent 2026-09-24 (Kjetil: «De fem setningene er bra. G1 er godkjent»)
- G1-GUI: godkjent 2026-09-24 (Kjetil, på v1-bildene; avsender-forhandsvisning-v2.png med private notater venter for seg)
- G2: godkjent 2026-09-26 (Kjetil: «gå videre med G2 som er godkjent»)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-09-26: Runde A WP1–WP5 deles i to PR-er: del 1 = CellProtocol (typer, verifisering, tester), del 2 = CellScaffold + Binding. Grunn: nedstrøms pinner CellProtocol; del 2 kan først bygge mot en main som har del 1. Lesson: aldri krasj bygger.

## Logg
- 2026-09-15: opprettet
- 2026-09-15: iterasjon 1 skrevet. Forskningsgrunnlaget (kontaktoppdagelse, interdependent privacy,
  kontekstuell integritet, Perkins v. LinkedIn) er lest og lagt i FORMAALSSPEC §0.3, og gir fire
  generelle konsepter: ingen katalog å slå opp i; én invitasjon, to leveranser; invitasjonen er en
  påstand om en annen; nei skal være like lett som ja. Elleve formål (A–J + gjenbruk), fjorten
  avledede tester, fem åpne spørsmål. Avhenger av PDD_entitetsdata-egen-kontroll (filimport,
  genesis, signering) — den er forutsetning, ikke leveranse her. Venter på G1.
- 2026-09-17: iterasjon 2. Kjetil rettet oppdagelsesmodellen: det finnes en tredje vei mellom
  «katalog som lekker» og «ingen oppdagelse», og skillet går mellom publisert og ikke publisert.
  Formål A erstattet av A1–A5. §6.1 bortfaller; tre nye åpne spørsmål om registerverten (DiMy),
  hva man publiserer om seg selv, og hva C ser når A spør om B. Venter fortsatt på G1.
- 2026-09-18: iterasjon 3. §6.1 besvart: overlappet regnes ut inne i entiteten av en modell eieren
  eier og kjører privat, aldri ved å spørre en tjeneste, og aldri ut av en celle andre eier — men
  det er lov å be om tilgang til å spørre. Nytt formål A6 med tre negative tester. §6.6–6.8 står.
- 2026-09-23: iterasjon 4. Kjetil besvarte §6.2–6.8 (avsender = domenets identitet; nykommer lander hos
  avsender og kan flytte; utløp 14 d/maks 90; avsender ser «besvart — ikke nå»; verten ser bare at en
  gyldig avtale spurte; avledet nøkkel per register; C ser A, B hører først ved invitasjon). Fem nye
  formål K–O, sju nye tester. Beslutning: ende-til-ende testes mellom Kjetil og Vegar over invite +
  chat, ikke correspondence; simulerte entiteter i swarm er eget scaffold og egen PDD senere. Brief-
  audit oppdatert mot origin/main (CellProtocol a785dc7, Binding 8ce634f6, CellScaffold 77a922bc).
  Ingen åpne spørsmål igjen. Venter på G1-ordet.
- 2026-09-23: iterasjon 5. Kjetil rettet N: hvor nykommeren lander avhenger av veien inn — direkte
  mot avsenders scaffold gir en entitet der, forseglet til nykommeren; via HAVEN-appen lager appen sin
  egen entitet ved første oppstart. Nytt formål P (midlertidig entitet/fragment kan flytte hjem) og
  Q (invite→chat er én ren, tillitvekkende stripe, avgjort av bildene). §3: tre stripebilder,
  flytt-hjem-bilde, ordliste. Venter på G1-ordet.
- 2026-09-24: G1 godkjent av Kjetil. Neste: G1-GUI — bildene i §3.
- 2026-09-24: G1-GUI-bilder levert: 3 striper + 7 enkeltbilder i images/, README.md med RENDERINGSERKLÆRING og sju valg bildene tar (bl.a. at «opened» ikke vises for avsender), ORDLISTE.md, mockup-kilde i images/mockup/. Venter på Kjetils ord.
- 2026-09-24: G1-GUI godkjent av Kjetil. Tillegg etter porten: private notater — Kjetil valgte «egen del:
  vises aldri, sendes aldri». Formål R og test.invite.private-notes-never-leave lagt til (iterasjon 6);
  avsender-forhandsvisning-v2.png viser skuffen «sendes ikke» og venter på eget ja. Neste: PLAN.md (G2).
- 2026-09-24: PLAN.md skrevet (20 arbeidspakker i tre runder: A = kjeden Kjetil→Vegar, B = flytt hjem, C = registre), dataflow.md og contract/invite_v1.json + 12 fixtures (check_fixtures.py: 0 avvik). Venter på G2.
- 2026-09-24 kl. 13:45: PLAN §3 oppdatert — tre av fem blokkeringer borte (Binding, CellScaffold, push). PR #47 venter på Kjetils merge. Gjenstår: entitetsdata runde 2 og vault-fabrikk. Venter på G2.
- 2026-09-26: G2 godkjent av Kjetil. Runde A starter: WP0 baseline, så WP1–WP5.
- 2026-09-26: iterasjon 7 — formål T (nøkkelavtale-nøkkel følger aksepten) inn i WP7, U (vedlegg) som WP12b runde B. Svar på Kjetils spørsmål i §0.1f.
- 2026-09-26 kl. 13:20: WP0 grønn — CellScaffold 6f5b99ef og Binding 8ce634f6 bygger mot CellProtocol main 7577d74. Neste: WP1–WP5 (CellProtocol-delen først: identityDomain + basis på billetten, utløp i verifikatoren, gravstein-type, T i aksepten).
- 2026-09-26 kl. 13:47: Runde A del 1 grønn — HavenInviteRoundATests 15/15, CellBaseTests 1277/0 feil, commit a82e9f4 på pdd/invitasjon-runde-a, PR #51 (utkast). Nytt i CellProtocol: identityDomain + basis på billetten, TTL 14/90 d, HavenInviteReply (yes/notNow/never), HavenInviteTombstone(+Ledger), HavenInviteSenderView/-Report, HavenContactBasisV1 (grunnlag + privateNotes), nøkkelavtale-nøkkel i chat-aksept og kontaktforespørsel, EphemeralIdentityVault med X25519. Se TESTRESULT.md#rundeA. Neste: Kjetil merger #51 når CI er grønn; så del 2 (CellScaffold + Binding). Merk: Kjetils checkout av CellProtocol har lokale endringer i ChatCell, ChatInvitationProofUtility og EphemeralIdentityVault (annen tråd) — kan gi konflikt ved neste sync.
- 2026-09-29 kl. 13:56: Kjetils checkout av CellProtocol ryddet (Kjetil valgte «snapshot + rent main»): alt ucommittet (CellIdentifier/UUIDText-refaktoreringen fra 23.09, Docs/EntityData-Review, 135 filer) ligger nå som commit 200c970 på `wip/uuid-nokling-2026-09-23` (pushet, ikke bygget/testet); checkouten står på main 81601a6 (= origin/main, med #47/#50/#51), `swift build` OK. Ingen konflikt igjen for ChatCell/ProofUtility/EphemeralIdentityVault. Logg: handoff/rundeA/snapshot-og-main-20260929-135602.log. Neste: chat/samarbeid mellom inviterte (WP7-forberedelse: to entiteter, aksept med nøkkelavtale-nøkkel, forseglet melding) og runde A del 2 (CellScaffold + Binding).
