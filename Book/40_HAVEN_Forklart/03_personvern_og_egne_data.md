# Personvern og dine egne data

Status: batch 1 · godkjent av Kjetil 2026-10-16 · kildegrunnlag: snapshot 2026-10-07, ankre kontrollert ordrett 2026-10-15 · godkjenner: Kjetil (per batch)

## Lager HAVEN en profil av meg ut fra det jeg gjør?

**[kan sies] HF-03-01.** Ikke etter designet. Formål og interesser i HAVEN skal ikke spore brukere, ikke utlede atferd og ikke lage poengsummer. De erklæres alltid eksplisitt og utledes aldri.

*Begrensning:* Dette er regelen i spesifikasjonen. Den sier ikke at hver tjeneste bygget på HAVEN er kontrollert mot den.

Kilder:
- `Book/09_Purpose_Interests.md` linje 132: «do not track users»
- `Book/09_Purpose_Interests.md` linje 139: «All Purpose and Interest declarations are explicit, never inferred.»

## Hva lagres når jeg spør Kallimachos?

**[kan sies] HF-03-02.** Spørsmål og svar lagres i bibliotekaren (CommonsLibrarian), avgrenset til deg og relasjonen du spør fra.

*Begrensning:* Gjelder koden per 2026-10-07. Se HF-03-03 for hva sletting ikke dekker.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1005: «Rå spørsmål og svar lagres requester- og relation-avgrenset i CommonsLibrarianCell.»

## Hva dekker ikke slettingen?

**[kan sies] HF-03-03.** Når du sletter historikken din, blir dette liggende igjen: kostnadspostene i driftsregnskapet (uten spørsmåls- eller svartekst), AIGateway sin egen journal, flythendelser og det modellleverandøren selv lagrer.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1007: «Driftsledgerens kostnadsposter (uten spørsmåls- eller svartekst), AIGateways egen journal, flow-hendelser og leverandørens egen lagring.»

## Hva skjer hvis jeg skriver personopplysninger?

**[med forbehold] HF-03-04.** Kallimachos avviser spørsmål som ligner e-postadresser, personnummer, kortnummer, IBAN-kontonummer eller telefonnummer med landkode, før noe sendes videre til andre celler eller til en modell.

*Forbehold:* Det er en enkel mønstersjekk. Den fanger ikke navn, adresser, helseopplysninger eller andre personopplysninger. Skriv derfor bare syntetiske eller offentlige spørsmål.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 266: «Inndata ble avvist før alle celle- og modellkall fordi den ligner personopplysninger.»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1004: «Bruk bare syntetiske eller offentlige spørsmål.»

## Finnes det en personvernkonsekvensvurdering?

**[ikke ennå] HF-03-05.** Nei, ikke ennå. Det finnes ingen DPIA, og ingen jurist har klassifisert løsningen regulatorisk.

*Skal ikke sies:* «Kallimachos er GDPR-godkjent.» · «HAVEN er personvernvurdert.»

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 96: «a lawyer's regulatory classification · a DPIA»
