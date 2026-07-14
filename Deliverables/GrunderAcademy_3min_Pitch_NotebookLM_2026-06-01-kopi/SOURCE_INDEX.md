# Source Index for NotebookLM Upload

Dato: 2026-06-01

Denne pakken er selvstendig: filene under `sources/` er kopier eller teksteeksporter av de lokale kildene som ellers ikke er tilgjengelige for NotebookLM.

## Anbefalt opplasting

Last opp disse filene til NotebookLM:

1. `KILDEPAKKE.md`
2. `NotebookLM_PROMPT.md` kan også lastes opp, men bør primært limes inn som prompt.
3. Alle filene i `sources/pages_exports/`
4. Alle filene i `sources/dimy_value_redistribution/`
5. Alle filene i `sources/cellprotocol_documents/`

Merk: ZIP-filen er praktisk for transport/backup, men NotebookLM bør normalt få selve dokumentfilene som kilder, ikke bare en zip, hvis den ikke pakker ut zip-arkiver automatisk.

## `sources/pages_exports/`

- `3_min_pitch_forslag.txt`  
  Eksport fra Pages-dokumentet med Claude-, Codex- og ChatGPT-varianter.

- `funn_markedsundersokelsen.txt`  
  Eksport fra Pages-dokumentet med samtalebaserte markedsfunn og hypoteser.

- `gunderacademy_3min_pitch_old.txt`  
  Eksport fra gammel pitch.

- `gunderacademy_3min_pitch_2_old.txt`  
  Alternativ/duplikat eksport av gammel pitch-versjon.

## `sources/dimy_value_redistribution/`

- `00_START_HERE.md`  
  Nåværende fase, safe thesis, hva som ikke kan påstås, og lese-/implementeringsrekkefølge.

- `01_TERMINOLOGY_AND_CLAIMS_CANON.md`  
  Kanon for trygge, risikable og forbudte claims.

- `05_ASSURANCE_MATURITY_MATRIX.md`  
  Modenhetsstatus: hva som er implementert, spesifisert, deferred eller forbudt.

- `14_CONFERENCE_PRODUCT_IP_AND_VALUE_PROPOSITION.md`  
  Hovedkilden for konferanseproduktets IP, verdiforslag, målgrupper og pitchformuleringer.

- `15_CONFERENCE_REVENUE_SCENARIOS_AND_USER_STORIES.md`  
  Hovedkilden for scenariomodell, inntektslinjer, kostnader, usikkerheter og brukerhistorier.

- `17_CONFERENCE_PERSONAS_AND_STORY_SIMULATION.md`  
  Proto-personaer og storymomenter for deltaker, arrangør, sponsor, DPO/gatekeeper m.m.

- `18_ICP_AND_PERSONA_DEVELOPMENT.md`  
  ICP/persona-rammeverk, særlig relevant for startup-konferanser og founder/investor-situasjoner.

- `conference_revenue_scenarios.mjs`  
  Scriptet som genererer scenariomodellen. Brukes som kilde for at tallene er modellantakelser.

- `conference_revenue_scenarios_2026-05-14.json`  
  Maskinlesbar output med scenario `medium-500`, inkludert brutto 654 875 NOK og sponsorandel 75,6 %.

- `conference_revenue_scenarios_2026-05-14.csv`  
  Tabelloutput fra samme modell.

## `sources/cellprotocol_documents/`

- `17_Conference_Ownership_Dataflow.md`  
  Forklarer hvordan konferanseflater, deltaker-eid kontekst, arrangør-eid publisering og shared/agreement-backed relasjoner bør skilles.

## Promptbruk

Etter opplasting: lim inn innholdet fra `NotebookLM_PROMPT.md` i NotebookLM og be den levere:

- ferdig treminutters manus
- 20-sekunders versjon
- påstandssjekk
- alternative åpninger

