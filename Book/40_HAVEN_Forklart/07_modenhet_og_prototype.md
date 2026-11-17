# Hvor modent er HAVEN?

Status: batch 1 · godkjent av Kjetil 2026-10-16 · kildegrunnlag: snapshot 2026-10-07, ankre kontrollert ordrett 2026-10-15 · godkjenner: Kjetil (per batch)

## Er Kallimachos ferdig?

**[kan sies] HF-07-01.** Nei. Kallimachos er merket som intern prototype og eksperimentell demo.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 974: «"maturityLabel": .string("Intern prototype")»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 1012: «"maturity": .string("experimental-demo")»

## Hva er bygget, og hva er bare spesifisert?

**[kan sies] HF-07-02.** Ifølge modenhetsmatrisen er domeneavgrenset identitet og eksplisitte kontrakter og tilganger implementert. Ekte betaling via betalingsleverandør er delvis implementert. Verdifordelingspolitikken (ValuePoolPolicy) er bare spesifisert, kjøretidscellen for verdifordeling er utsatt, overførbare tokens og uttak er utsatt til juridisk klassifisering finnes, og global omdømmescore er forbudt.

*Begrensning:* Matrisen skal oppdateres etter hver implementeringsrunde; tallene her er fra snapshot 2026-10-07.

Kilder:
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 13: «| Domain-scoped identity | implemented | Verify for pilot domain |»
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 14: «| Explicit contracts/capabilities | implemented | Wire to ProofDoor/AI paths |»
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 20: «| Real PSP top-up | partly implemented |»
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 25: «| ValuePoolPolicy | specified here | deterministic simulator first |»
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 26: «| Runtime ValuePoolCell | deferred | wait for simulator and ledger truth |»
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 27: «| Transferable tokens | deferred | legal classification required |»
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 29: «| Global reputation | forbidden | keep context-local only |»

## Kan offentlig tekst si at noe er mer modent enn det er?

**[kan sies] HF-07-03.** Nei. Regelen er at offentlig tekst aldri skal påstå et høyere modenhetsnivå enn modenhetsmatrisen viser. Det gjelder også dette korpuset.

Kilder:
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md` linje 44: «Never let public copy claim a maturity level higher than this table.»

## Hva er ikke bygget i tillitsmodellen?

**[kan sies] HF-07-04.** Distribuert tilbaketrekking av tilganger og en journal som tåler sletting og gjenoppbygger hva en KI har gjort, er ikke implementert.

Kilder:
- `Book/36_Agent_Trust_Package.md` linje 155: «- **Distribuert revokasjon:** ikke implementert»
- `Book/36_Agent_Trust_Package.md` linje 157: «- **Full rekonstruksjon av AI-effekter og slettesikker journal:** ikke implementert.»

## Hva sier HAVEN ikke om seg selv?

**[ikke ennå] HF-07-05.** Ingen av disse påstandene kan sies før de er dokumentert: at HAVEN løser ulikhet, er regulatorisk avklart, er lovlig i alle relevante markeder, hindrer kollaps, er penger uten lisensbehov, eller er en ferdig global protokoll for verdiomfordeling.

*Skal ikke sies:* «Dette løser ulikhet.» · «Dette er regulatorisk avklart.» · «Dette er lovlig i alle relevante markeder.» · «Systemet hindrer kollaps.» · «Dette er penger uten lisensbehov.» · «Vi har en ferdig global verdiomfordelingsprotokoll.»

Kilder:
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 47: «## Forbudte claims inntil dokumentert»
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 49: «- "Dette løser ulikhet."»

## Er HAVEN åpen kildekode?

**[med forbehold] HF-07-06.** Alle de 55 Swift-filene fra CellProtocol og CellScaffold i kildeutdraget har lisenshodet Apache-2.0. Hvilken lisens som gjelder for hvert repo, er ikke bekreftet, og lisensen er ikke kontrollert mot DPG-standarden.

*Forbehold:* Telling i et utdrag (29 filer i CellProtocol, 26 i CellScaffold), ikke en kontroll av hele repoene. Én fils lisenshode sier ikke hva repoets lisens er.

Kilder:
- `CellProtocol/Sources/CellBase/PurposeAndInterest/GoalDefinition.swift` linje 1: «// SPDX-License-Identifier: Apache-2.0»
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 55: «Open-source licence meeting the DPG Standard | NOT DONE — to be confirmed per repository»
