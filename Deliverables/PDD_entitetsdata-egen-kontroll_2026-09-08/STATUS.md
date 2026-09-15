# STATUS — entitetsdata egen kontroll

- surfaces: binding, cell, gui, skeleton
- tags: ai, autorisasjon, eierskap, entitet, tillit

## Porter
- G1: godkjent 2026-09-15    (formålsspesifikasjon godkjent av Kjetil, iterasjon 3)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-08: opprettet
- 2026-09-15: G1 godkjent av Kjetil. Samtidig fire klargjøringer som gjør treet enklere, ikke større:
  entitetsankeret opprettes i det øyeblikket entiteten trenger å persistere entitydata; adressebok-import
  for å invitere noen uten HAVEN-representasjon *er* en slik hendelse; VC-bevis hører også hjemme i
  entitydata; betaling via Palazzos egen PSP kommer senere og avhenger av at DiMyMint og
  DiMyMicropayments hentes inn. Konsekvens: §6.1 og §6.2 bortfaller — importen og genesis er samme flyt,
  ikke to runder. Neste port er G1-GUI.
