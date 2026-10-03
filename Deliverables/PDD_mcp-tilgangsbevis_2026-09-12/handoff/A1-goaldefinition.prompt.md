# A1 — `goalDefinition` inn i `Purpose` (CellProtocol / CellBase)

Mappe: `CellProtocolDocuments/Deliverables/PDD_mcp-tilgangsbevis_2026-09-12/`. Les `BESLUTNINGER.md` §B1 først — den er spesifikasjonen. Deretter `PLAN.md` A1.

## Absolutte grenser
- Arbeid i `CellProtocol/` på branch `pdd/goal-definition-in-purpose` opprettet fra `origin/main` (kjør `git fetch origin main` først; lokal main er ikke main — `lesson.local-main-is-not-main`). Opprett worktree fra macOS, ikke fra VM.
- Ingen `swift build`/`swift test` i denne jobben (sandkassen tåler det ikke — `lesson.codex-workspace-write-cannot-build-cellscaffold`). Rapporter «skrevet, ikke verifisert». Bygg og test kjøres som egen detached jobb (A1-build).
- Ingen endring i andre filer enn de fire under. Ingen push.

## Endringer (nøyaktig)

1. `CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift`
   - Nytt lagret felt `public private(set) var goalDefinition: GoalDefinition?` ved siden av `goal`/`helperCells`/`composition`.
   - `CodingKeys` får `goalDefinition`.
   - `init(...)` får parameter `goalDefinition: GoalDefinition? = nil`.
   - `init(from:)`: `decodeIfPresent(GoalDefinition.self, forKey: .goalDefinition)`. **Etter** at `name`/`nodeIdentifier` er dekodet: hvis `goalDefinition != nil && goalDefinition.purposeRef != reference` → kast `DecodingError.dataCorruptedError(forKey: .goalDefinition, in: container, debugDescription: "goalDefinition.purposeRef must equal purpose reference")` (bruk `Swift.DecodingError` — `lesson.cellbase-decodingerror-shadows-swift`).
   - `encode(to:)`: `encodeIfPresent(goalDefinition, forKey: .goalDefinition)`.
   - `public func setGoalDefinition(_ definition: GoalDefinition?)` med samme likhetsregel (kast egen feil `PurposeError.goalDefinitionPurposeMismatch`).
   - Dokumentasjonskommentar på `goal`: «Configuration of the cell that evaluates this purpose's goal (see GoalEvaluationCell). Declarative goal lives in `goalDefinition`.» Ingen atferdsendring på `goal`.

2. `CellProtocol/Sources/CellBase/PurposeAndInterest/GoalDefinition.swift`
   - `fromPerspectiveFields`: lag **ikke** predikatet `kind: "evidence-rule", operation: "satisfies"`. Regel: hvis `target` er satt og `evidenceRule` er nil → `GoalPredicate(kind: "value", sourceID: sourceID, operation: "equals", expected: target, metric: metric)`; ellers `predicate: nil` og `evaluatorKind: .custom`, og `tags` får `"evaluator:missing"`.

3. `CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift`
   - Der predikat mangler eller `kind` ikke er kjent (i dag → `false` → `active`): returner evaluering med `status: .unknown` og `missing: ["predicate"]` (manglende) eller `missing: ["predicate:<kind>(unsupported)"]` (ukjent). Rør ikke `network-ping`-grenen. De fem eksisterende testene i `GoalEvaluationEngineTests.swift` skal forbli uendret og grønne.

4. `CellProtocol/Tests/CellBaseTests/PurposeGoalDefinitionTests.swift` (ny) med fire tester:
   - `testPurposeWithGoalDefinitionRoundTripsThroughJSON` — Purpose med `nodeIdentifier = "purpose://candidate.mcp-tilgangsbevis.root"` og en GoalDefinition med samme `purposeRef`; encode → decode; sammenlign felt for felt (aldri hele `ValueType`-objekter — `lesson.valuetype-equality-false-for-objects`).
   - `testLegacyPurposeJSONWithoutGoalDefinitionDecodesWithNil` — bruk JSON-strengen fra `PurposeCompositionTests.testPurposeCompositionRoundTripsThroughPurposeJSON` som mal.
   - `testGoalDefinitionWithForeignPurposeRefFailsToDecode` — `XCTAssertThrowsError`, og feilen er `DecodingError`.
   - `testUnknownPredicateEvaluatesToUnknownNotActive` — GoalDefinition med `predicate: GoalPredicate(kind: "evidence-rule", ...)` og én deklarert kilde med fersk observasjon → `status == .unknown`, `missing` inneholder `"predicate:evidence-rule(unsupported)"`.

## Rapport
Skriv `CellProtocolDocuments/Deliverables/PDD_mcp-tilgangsbevis_2026-09-12/handoff/A1-RAPPORT.md`: branch og `git rev-parse HEAD` (fra macOS), diff-statistikk per fil, hver test med én setning om hva den beviser, og overskriften «Skrevet, ikke verifisert — bygg kjøres i A1-build». Ingen påstand om grønn kjøring.
