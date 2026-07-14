# Terminology and claims canon

Dette dokumentet er kanon for neste implementeringsfase. Hvis eldre research eller pitch-tekst motsier dette, skal dette dokumentet vinne inntil vi eksplisitt oppdaterer det.

## Begreper

- `Entity`: konseptuell aktør. Skal ikke brukes som runtime-container.
- `Identity`: domain-scoped kryptografisk identitet. Ingen global ID og ingen automatisk cross-domain linkage.
- `Runtime`: kjørende miljø/scaffold som hoster celler.
- `Cell`: deterministisk komponent med capability-grenset state/handlinger.
- `Agreement`: forespørsel om capabilities, purpose og evidence.
- `Contract`: faktisk tildelt autoritet.
- `Purpose`: eksplisitt deklarert intensjon. Skal ikke infereres fra skjult atferd.
- `Interest`: semantisk kategori. Skal ikke bli ranking eller profilscore.
- `Entitlement`: rett til tilgang eller bruk innen et avgrenset domene.
- `Credit`: intern verdi/tilgangsenhet. Skal ikke tolkes som penger uten juridisk klassifisering.
- `Payout`: value-return-record. I v0 skal dette være non-transferable credit, rebate eller grant.
- `ContributionProof`: domain-scoped bevis for samtykke, bruk, arbeid, kuratering, lead-kvalifisering eller commons-bidrag.
- `ValuePoolPolicy`: replaybar policy som fordeler verifisert verdi til individer, commons og operatør.

## Harde prinsipper

- Ingen global reputation.
- Ingen global person-ID.
- Ingen skjult atferdsprofilering.
- Ingen transferability, cash-out, P2P value eller multi-vendor credit network i v0.
- PSP håndterer real-money betaling i første fase.
- Ledger og audit må være mer autoritative enn UI-state.
- Alle value-return claims må kunne spores til Contract, proof og ledger event.

## Trygge claims

- CellProtocol gir byggesteiner for domain-scoped identity, explicit contracts, capabilities, replay og audit.
- Purpose/Interests kan brukes som human-aligned semantic layer uten global reputation.
- DiMyMint/DiMyMicropayments har primitives for issue/spend/redeem, spent-set og internal value units.
- ProofDoor/PaymentGate viser en praktisk path fra payment/access til VC-basert entitlement proof.
- Value redistribution er en forsknings- og pilotretning, ikke en ferdig økonomisk mekanisme.

## Risikable claims som krever caveat

- "Micropayments reduserer økonomisk konsentrasjon."
- "Credits er ikke e-money."
- "Dette kan skaleres globalt."
- "Trust policy er abuse-proof."
- "AI entitlement kan brukes som økonomisk fordelingsgrunnlag."

## Forbudte claims inntil dokumentert

- "Dette løser ulikhet."
- "Dette er regulatorisk avklart."
- "Dette er lovlig i alle relevante markeder."
- "Systemet hindrer kollaps."
- "Dette er penger uten lisensbehov."
- "Vi har en ferdig global verdiomfordelingsprotokoll."

## Kildegrunnlag

- `global_value_redistribution_research/04_claims_og_mangler.md`
- `global_value_redistribution_research/01_syntese.md`
- `global_value_redistribution_research/sources/existing-research-pack/01_glossary.md`
- `global_value_redistribution_research/sources/existing-research-pack/02_claim_bank.md`
