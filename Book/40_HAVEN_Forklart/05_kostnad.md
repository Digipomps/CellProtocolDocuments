# Hva koster det, og hvem betaler?

Status: batch 1 · godkjent av Kjetil 2026-10-16 · kildegrunnlag: snapshot 2026-10-07, ankre kontrollert ordrett 2026-10-15 · godkjenner: Kjetil (per batch)

## Hvem betaler for Kallimachos i dag?

**[kan sies] HF-05-01.** Ingen inntekt er koblet til Kallimachos. Hele den målte kostnaden er udekket, og Kallimachos påstår ikke at den finansierer seg selv.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1051: «Ingen inntektskilde er koblet i denne kjøringen.»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1014: «ingen påstand om at Kallimachos finansierer seg selv.»

## Hvorfor står kostnaden som 0?

**[kan sies] HF-05-02.** Når driftsoperatøren ikke har lagt inn listepriser, kan kostnadsfeltet vise 0. Det betyr «pris ikke satt», ikke at svaret var gratis.

*Begrensning:* Feilen er kjent og foreslått rettet i bølge 0 (vis «pris ikke konfigurert» i stedet for 0).

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 148: «Provider list prices are not known to the code. Ticks stay zero unless an»

## Hva koster ett råd med språkmodell?

**[med forbehold] HF-05-03.** Et overslag fra 2026-10-07 er omtrent 0,007 kr per råd med en liten modell (Claude Haiku 5.5) og 0,14 kr med en mellomstor (Sonnet 5.5).

*Forbehold:* Overslaget bygger på listepriser hentet 2026-10-07 og antakelser om lengde på spørsmål og svar. Prisene endrer seg. Svar uten modell koster ikke modellpenger.

Kilder:
- `RAPPORT_Kallimachos_raadgiversverm_2026-10-07.md` linje 17 (intern rådgiverrapport, ikke offentlig kilde): «Ett råd koster omtrent 0,007 kr med Claude Haiku 5.5 og 0,14 kr med Sonnet 5.5.»
- `raadgivere/O1_opponent.md` linje 44 (intern rådgiverrapport, ikke offentlig kilde): «Claude Haiku 5.5 koster 0,10/0,50 USD per MTok»

## Er credits penger?

**[kan sies] HF-05-04.** Credits i DiMy er en intern verdi- eller tilgangsenhet. De skal ikke tolkes som penger uten juridisk klassifisering. I første versjon kan verdi ikke overføres, tas ut eller sendes mellom personer.

Kilder:
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 16: «'Credit': intern verdi/tilgangsenhet. Skal ikke tolkes som penger uten juridisk klassifisering.»
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 26: «- Ingen transferability, cash-out, P2P value eller multi-vendor credit network i v0.»

## Er dette regulatorisk avklart?

**[ikke ennå] HF-05-05.** Nei. Det er ikke juridisk avklart, og en skriftlig klassifisering fra en navngitt jurist mangler. Kallimachos kan bare gjengi en skriftlig juridisk vurdering hvis den finnes i katalogen.

*Skal ikke sies:* «Dette er regulatorisk avklart.» · «Dette er lovlig i alle relevante markeder.» · «Credits er ikke e-penger.»

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 78: «**This is not legally cleared.**»
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 50: «- "Dette er regulatorisk avklart."»
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 42: «- "Credits er ikke e-money."»

## Kan jeg få modellbruk dekket av stiftelsen eller DiMy?

**[ikke ennå] HF-05-06.** Ikke ennå. Ingen slik ordning finnes. Rekkefølgen for finansiering (svar uten modell, så egen nøkkel eller lokal modell, så allmenningskvote, DiMy senere) er et forslag som venter på beslutning.

*Skal ikke sies:* «Modellbruken er gratis for deg.» · «DiMy betaler for språkmodellen.»

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1051: «Ingen inntektskilde er koblet i denne kjøringen.»
- `RAPPORT_Kallimachos_raadgiversverm_2026-10-07.md` linje 142 (intern rådgiverrapport, ikke offentlig kilde): «| B7 | Finansieringsrekkefølge |»
