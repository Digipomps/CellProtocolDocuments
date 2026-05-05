# Vegar-pakke: SkeletonElement bruk og rendering

Denne pakken er laget for implementasjonsteam som trenger en grundig og operasjonell beskrivelse av hvordan `SkeletonElement` skal **modelleres, parses, brukes og rendres**.

## Mål

- gi én praktisk oppskrift for å implementere en kompatibel renderer
- redusere tolkning av spesifikasjonen
- dekke både happy-path, fallback og kompatibilitetsdetaljer

## Innhold

- `SkeletonElement_Rendering_Handbook.md` — hoveddokument (semantikk + rendering-regler)
- `Kotlin_Renderer_Blueprint.md` — konkret Kotlin/Compose-strategi
- `Skeleton_Test_Validation_Plan.md` — test- og kvalitetssikring
- `fixtures/*.json` — startsett med JSON-fixtures for parser/render-tester
- `source_docs/Book/*.md` — originaldokumentasjon som pakken bygger på

## Kildedokumenter inkludert

- `source_docs/Book/12_Skeleton_Spec.md` (primærkilde)
- `source_docs/Book/11_Developer_Guide_Cell.md`
- `source_docs/Book/13_Agent_Instructions.md`
- `source_docs/Book/10_Quickstart.md`
- `source_docs/Book/06_CellResolver.md`
- `source_docs/Book/07_Scaffold_Runtime.md`

## Prioritert leserekkefølge

1. `SkeletonElement_Rendering_Handbook.md`
2. `Kotlin_Renderer_Blueprint.md`
3. `Skeleton_Test_Validation_Plan.md`
4. `source_docs/Book/12_Skeleton_Spec.md`

## Normativitet

- Normative regler er hentet fra `12_Skeleton_Spec.md`.
- Der håndboken beskriver konkrete implementasjonsvalg for Kotlin-renderer, er det presentert som anbefalt strategi for å holde determinisme og kompatibilitet.
