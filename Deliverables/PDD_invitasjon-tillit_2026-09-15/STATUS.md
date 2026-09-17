# STATUS — invitasjon tillit

- surfaces: binding, cell, gui, skeleton
- tags: invitasjon, onboarding, personvern, relasjon, tillit

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

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
