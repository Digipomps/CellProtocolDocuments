# Gemini Design Sketch -> Skeleton Pack

This package is meant to be given to Gemini when Gemini should:

- read one or more design sketches
- propose a valid HAVEN / CellProtocol Skeleton UI
- judge how faithfully the current runtime can render that design
- identify what needs approximation, renderer work, or a custom cell

## What Gemini Should Produce

Gemini should return all of the following:

1. A short summary of the intended UI and interaction model.
2. A valid `skeleton` JSON proposal, or a full `CellConfiguration` JSON if that is more useful.
3. A capability gap analysis grounded in the current Swift runtime.
4. Explicit assumptions where the sketch is ambiguous.
5. A list of minimal extensions if the design cannot be represented well enough today.

## Reading Order

1. `01_Context_and_Runtime_Model.md`
2. `02_Normative_CellConfiguration_and_Skeleton_JSON.md`
3. `03_Gemini_Task_Brief.md`
4. `04_Capability_Gap_Analysis_Framework.md`
5. `05_GUI_Questions_For_Gemini.md`
6. `examples/*.json`

## Source Of Truth

This package is stricter than the current Book chapter where the Book lags behind code.

Primary code sources:

- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift`
- `CellProtocol/Tests/CellBaseTests/SkeletonTests.swift`

Conceptual sources:

- `Book/11_Developer_Guide_Cell.md`
- `Book/12_Skeleton_Spec.md`
- `Book/13_Agent_Instructions.md`

## Important Ground Rules

- Emit canonical `flowElementSkeleton`, never legacy `flowELementSkeleton`.
- Emit wrapped `Object` form: `{ "Object": { "elements": ... } }`.
- Do not invent unsupported stack properties like `spacing` or `alignment` on `HStack` / `VStack`.
- Do not place `scaledToFit` or `resizable` inside `modifiers`; they belong on `Image`.
- Prefer conservative JSON that matches current runtime over ambitious JSON that only looks plausible.
- Treat remote image rendering as a known gap in the current Swift renderer.

## Known Mismatches Between Model And Runtime

- `TextArea` exists in code and renders, but older docs may omit it.
- `Image.url` and `Image.type` exist in the model, but the newer Swift renderer currently uses `Image.name` and ignores remote URL loading.
- `HStack` and `VStack` have `modifiers` properties in Swift types, but their JSON wire format is still array-only and does not encode stack modifiers.
- `Text` supports `styleRole: "markdown"` in the Swift renderer.

## Package Goal

This package is not trying to prove every implementation detail in HAVEN. It is trying to help Gemini make one good decision:

Can this design be shown well enough with current Skeleton UI, and if not, what is the smallest honest gap?
