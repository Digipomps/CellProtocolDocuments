# UiO HAVEN Research Question Pack

Denne pakken er laget for å hjelpe med å utvikle og spisse forslag til forskningsspørsmål for studenter ved Institutt for informatikk, gruppen Informasjonssystemer, rundt HAVEN som infrastruktur, plattform og samfunnsmodell.

## Innhold

- `01_Kontekstnotat_UiO_HAVEN_og_Informasjonssystemer.md`
  Kort forskningsbrief som kobler HAVEN til en informasjonssystemfaglig ramme.
- `02_Forslag_til_Forskningssporsmal.md`
  Et kuratert sett med forskningsspor og konkrete forskningsspørsmål.
- `03_ChatGPT_DeepResearch_Prompt.md`
  En lim-inn-klar prompt for ChatGPT Deep Research.
- `04_Veiledernotat_1_side.md`
  Kort veilederversjon med anbefalte spor, vurderingskriterier og råd om avgrensning.
- `05_DeepResearch_Prompt_Prioriter_3_5_Masteroppgaver.md`
  En runde-2-prompt som ber ChatGPT Deep Research velge og spisse 3-5 sterke masteroppgaver.
- `06_DeepResearch_Prompt_Endelig_Problemstilling_og_Metode.md`
  En runde-3-prompt som gjør ett valgt spor om til endelig problemstilling, metodeopplegg og kapittelskisse.

## Anbefalt bruk

1. Start et nytt Deep Research-oppdrag i ChatGPT.
2. Last opp:
   - `01_Kontekstnotat_UiO_HAVEN_og_Informasjonssystemer.md`
   - `02_Forslag_til_Forskningssporsmal.md`
   - eventuelt utvalgte HAVEN-kapitler fra `Book/`
3. Velg `Deep research` og bruk opplastede filer som primærkontekst.
4. Prioriter troverdige nettsteder i stedet for å la oppgaven drive på helt fri websøk.
5. Lim inn prompten fra `03_ChatGPT_DeepResearch_Prompt.md`.
6. Gjør en manuell gjennomgang av forskningsplanen ChatGPT foreslår før du starter kjøringen.
7. Kjør en andre runde på de 2-5 beste forslagene for å snevre inn problemstilling, metode og empirisk opplegg.
8. Når dere vil gå fra bred idébank til noen få konkrete masterspor, bruk `05_DeepResearch_Prompt_Prioriter_3_5_Masteroppgaver.md`.
9. Når ett spor er valgt, bruk `06_DeepResearch_Prompt_Endelig_Problemstilling_og_Metode.md` for å lande endelig problemstilling og oppgavedesign.

## Anbefalte nettsteder å prioritere

Disse er best egnet som prioriterte kilder, ikke nødvendigvis som hard avgrensning:

- `uio.no`
- `aisnet.org`
- `link.springer.com`
- `sciencedirect.com`
- `tandfonline.com`
- `sagepub.com`
- `cambridge.org`
- `jstor.org`

Hvis dere vil holde oppgaven tett på norsk eller skandinavisk kontekst, kan `uio.no` og andre universitetsdomener vektes ekstra høyt.

## Hvorfor denne arbeidsflyten passer Deep Research

OpenAI beskriver Deep Research som et verktøy for komplekse, flerstegs oppgaver der brukeren:

- beskriver ønsket utfall
- velger hvilke kilder som kan brukes
- vurderer og justerer forskningsplanen før kjøring
- får en strukturert rapport med sitater eller kildelenker

OpenAI oppgir også at Deep Research kan bruke opplastede filer, offentlige nettsteder og spesifiserte domener, og at ferdige rapporter kan lastes ned i blant annet Markdown, Word og PDF. I oppdateringen publisert 10. februar 2026 beskriver OpenAI dessuten at Deep Research kan begrense websøk til betrodde nettsteder, vise fremdrift i sanntid og avbrytes underveis for presisering.

Kilder:

- <https://help.openai.com/en/articles/10500283-deep-research>
- <https://openai.com/index/introducing-deep-research/>

## Viktig avgrensning

HAVEN er foreløpig best egnet som:

- designobjekt
- prototypisk case
- normativ kontrast til dagens plattformmodeller
- analytisk linse for å diskutere styring, verdi, data og makt

Det betyr at mange gode studentprosjekter bør utformes som:

- konseptuelt teoriarbeid
- komparative caseanalyser
- design science / prototypeevaluering
- workshop- eller intervjubaserte studier
- governance- og institusjonsanalyser

Det er mindre klokt å formulere alle oppgaver som om HAVEN allerede er et ferdig, storskala empirisk felt med moden brukermasse.
