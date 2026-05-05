# Vegar-pakke: CellProtocol + Scaffold i Kotlin

Denne pakken samler dokumentasjonen som er mest relevant for å implementere `CellProtocol` og `Scaffold` i Kotlin.

## Innhold

- `source_docs/README-CellProtocol.md`
- `source_docs/Book/01_CellProtocol_Core.md`
- `source_docs/Book/02_Cell_Interfaces.md`
- `source_docs/Book/03_Identity_Model.md`
- `source_docs/Book/04_Agreements_Contracts.md`
- `source_docs/Book/05_Flows_Lifecycle.md`
- `source_docs/Book/06_CellResolver.md`
- `source_docs/Book/07_Scaffold_Runtime.md`
- `source_docs/Book/08_Bridging_Transport.md`
- `source_docs/Book/09_Purpose_Interests.md`
- `source_docs/Book/10_Quickstart.md` (Swift-eksempler, men nyttig for runtime-oppsett)
- `source_docs/Book/11_Developer_Guide_Cell.md` (Swift-eksempler, men nyttig for Cell-mønstre)
- `source_docs/Book/12_Skeleton_Spec.md`
- `source_docs/Book/13_Agent_Instructions.md`
- `source_docs/Book/14_Perspective_Runtime_Matching.md`
- `Kotlin_Implementation_Checklist.md`
- `Swift_to_Kotlin_Mapping.md`

## Foreslått leserekkefølge

1. Start med kjerne og interfaces:
   - `01_CellProtocol_Core.md`
   - `02_Cell_Interfaces.md`
2. Gå videre til runtime/scaffold:
   - `06_CellResolver.md`
   - `07_Scaffold_Runtime.md`
   - `05_Flows_Lifecycle.md`
3. Implementer cell-API og config-kontrakter:
   - `11_Developer_Guide_Cell.md`
   - `10_Quickstart.md`
4. Implementer Skeleton-JSON og rendering:
   - `12_Skeleton_Spec.md`
5. Hvis dere trenger matching/perspective:
   - `09_Purpose_Interests.md`
   - `14_Perspective_Runtime_Matching.md`

## Viktig avgrensning

Swift-filene beskriver dagens referanseimplementasjon. Kotlin-implementasjonen bør bevare:

- samme semantikk
- samme kontrakter (payload/formater)
- samme deterministiske egenskaper

...men trenger ikke speile Swift-strukturen 1:1.
