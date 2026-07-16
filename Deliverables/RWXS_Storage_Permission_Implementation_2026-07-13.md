# RWXS Storage Permission Implementation — 2026-07-13

Status: implemented and verified. The CellProtocol and CellScaffold code is
already published; the canonical documentation is prepared from the current
CellProtocolDocuments `origin/main` in a clean worktree.

Task owner and human decision-maker: Kjetil.

## Formål and Goals

### `purpose://access.audit.privacy`

Intent: make persistent-retention authority explicit, identity-bound, auditable,
and distinguishable from read access and forwarding authority.

Goal `goal.rwxs.runtime-contract.2026-07-13` (`haven.goal-definition.v1`):

- metric: canonical permission parsing/matching and identity-bound allow/deny proof
- baseline: the runtime emitted three positions and accepted a fourth only as `-`
- target: canonical `rwxs`, additive Storage bit, legacy decode without implicit
  Storage, and passing positive/rejection tests
- timeframe: 2026-07-13
- evidence: `Permission.swift`, `AgreementCodingTests.swift`,
  `GeneralCellInterfaceTests.swift`, full `swift test`
- status: satisfied

Goal `goal.rwxs.knowledge-retrieval.2026-07-13` (`haven.goal-definition.v1`):

- metric: canonical documentation and retrieval from both local Docs MCP and
  `dimy_docs`
- baseline: Storage semantics were absent and RAG could not retrieve them
- target: Book documents define RWXS, limitations, lifecycle distinction, and
  forwarding boundary; both retrieval paths return those sections
- timeframe: 2026-07-13
- evidence: Book chapters 01, 04, 06, 07, and 22; `Gap_Analysis.md`; Docs MCP
  test/search output; `dimy_docs` sync and retrieval output
- status: satisfied

Goal `goal.rwxs.scaffold-authoring.2026-07-13` (`haven.goal-definition.v1`):

- metric: Agreement Workbench preserves and explains the fourth permission
  position
- baseline: its normalizer truncated permission input to three characters and
  would therefore erase `S`
- target: canonical four-character output, explicit Storage choices and
  explanation, legacy three-character input without implicit Storage, and a
  passing focused integration suite
- timeframe: 2026-07-13
- evidence: `AgreementWorkbenchCell.swift` and
  `AgreementWorkbenchCellTests.swift` in CellScaffold
- status: satisfied

### `purpose://gui.quality.functional-accessible`

Intent: determine whether Agreement Workbench is both functionally usable and
clear enough for its intended audience, based on a real Porthole user path rather
than source inspection alone.

Goal `goal.agreement-workbench.functional-path.2026-07-16`
(`haven.goal-definition.v1`):

- metric: direct launch, tab navigation, RWXS selection, review, signed save,
  and reload persistence
- baseline: unit tests proved state behavior but no dedicated end-to-end
  Agreement Workbench story existed
- target: the complete path works on clean published source without browser
  console errors
- timeframe: 2026-07-16
- evidence: browser run against CellProtocol `2c668fb97d3ef2b7ec494cd7ac14942f6c1954d2`
  and CellScaffold `163901d456c85dfedf208e382413046ce7a6dbf2`
- status: satisfied

Goal `goal.agreement-workbench.end-user-quality.2026-07-16`
(`haven.goal-definition.v1`):

- metric: coherent language, accurate control state, non-blocking access flow,
  understandable status, and absence of raw implementation detail
- baseline: a nine-tab technical workbench with no dedicated browser smoke
- target: no contradictory control state, stale loading state, repeated access
  prompt, or raw Contract/identity payload in the ordinary editing path
- timeframe: 2026-07-16
- evidence: the same browser run plus screenshots and the structured UX summary
- status: unsatisfied

## Claim ledger and adjudication

### `claim.rwxs.storage-authority`

- type: normative
- strength: assertive
- source: task-owner definition
- statement: the compact permission contract consists of Read, Write, Execute,
  and Storage; Storage authorizes persistent retention and serves as evidence of
  that authority
- adjudication: supported as the task owner's normative protocol decision and
  implemented in code and documentation

### `claim.rwxs.not-copy-prevention`

- type: factual
- strength: assertive
- statement: an `S` Grant cannot technically prevent a non-compliant recipient
  from copying already revealed output
- support: the permission model controls resolver/Contract decisions; it does
  not control an external recipient's storage system
- adjudication: supported, with the limitation stated in Chapters 04 and 06

### `claim.rwxs.not-forwarding`

- type: normative
- strength: assertive
- statement: Storage authority does not imply disclosure, redistribution,
  publication, or forwarding authority
- counter checked: readers could otherwise mistake retained possession for a
  transferable right
- adjudication: supported; forwarding remains a separate, not-yet-defined
  authorization path rather than an invented capability name

### `claim.rwxs.compatibility`

- type: project_capability
- strength: assertive
- statement: Storage can be added without reinterpreting persisted `r/w/x` bits
- support: the existing bits remain `4/2/1`, Storage uses bit `8`, integer JSON
  round-trip tests pass, and legacy three-/six-character strings never infer `S`
- adjudication: supported by contract tests and the full Swift suite

### `claim.agreement-workbench.quality-high-enough`

- type: project_capability
- strength: assertive
- statement: Agreement Workbench has a sufficiently high-quality user
  experience
- support: direct launch, all nine tabs, `r--s` editing, Review projection,
  signed save, agreement refs, and reload persistence worked; the browser
  reported no console warning or error
- counterevidence: an access-approval prompt repeatedly interrupted internal
  tab/actions for an already available self-reference and displayed the full raw
  Agreement JSON plus a local identity-storage reference; after `r--s` was
  selected and persisted, the permission control rendered `---- Ingen`; the
  initial loading banner remained after the surface had rendered; mixed
  Norwegian/English terms, incorrect summary grammar, and raw status tokens such
  as `broad-warning`, `medium`, and `high` were user-visible
- adjudication: partially supported for an internal expert prototype, rejected
  for a general end-user release

No formal argumentation scheme was required for this UX claim: the decisive
counterevidence was reproduced directly in the target user path.

No argumentation scheme was instantiated: the critical questions were directly
answered by the task-owner decision, current source, and deterministic tests.

## Decision log

1. Canonical emitted permission strings are four lowercase positions: `rwxs`.
2. Storage is additive bit `8`; existing persisted `r/w/x` integer meanings do
   not change.
3. Three- and six-character input remains decode-compatible and always implies
   no Storage authority. Canonical group/other input is eight characters.
4. Production literals were normalized to four characters; legacy width is
   retained only in explicit compatibility tests.
5. `S`, the Scaffold storage engine, and `ColdStorageCondition` are separate
   concepts.
6. No forwarding capability name was invented in this change.
7. Agreement Workbench now emits four-character permissions, exposes `---s`
   and `r--s`, and warns that Storage does not authorize forwarding.

## Verification

- `swift test --filter AgreementCodingTests`: 10 passed
- `swift test --filter 'AgreementCodingTests|IdentityAgreementTests|GeneralCellInterfaceTests'`:
  40 passed before the additional resolver-level Storage test
- `swift test --filter GeneralCellInterfaceTests/testStoragePermissionRequiresExplicitIdentityBoundSGrant`:
  1 passed
- full `swift test`: 592 passed, 0 failed
- isolated CellScaffold `AgreementWorkbenchCellTests`: 16 passed, 0 failed,
  built against a clean temporary CellProtocol copy containing the RWXS source
  changes
- `python3 -m unittest discover Tools/HavenDocsMCP/tests`: 7 passed
- Docs MCP lexical search for `Storage permission forwarding`: Chapter 04 is
  the top result and Chapters 06/07 are also returned
- `dimy_docs` admin sync: 40 mirror files scanned, 1 document created,
  8 updated, 31 unchanged, 0 deleted, no errors
- `dimy_docs` retrieval for RWXS/Storage/forwarding: returned the new Chapter 04
  RWXS definition and forwarding boundary, Chapter 06 resolver limitation,
  Chapter 01 core statement, and Chapter 07 storage-engine distinction
- clean-source Agreement Workbench user path: direct launch, `r--s` selection,
  Review, signed save, Save & Handoff, and reload persistence all completed
- the saved Agreement retained `r--s` and exposed one agreement reference after
  reload; browser console warnings/errors: 0
- UX artifacts: `agreement-workbench-overview.png`,
  `agreement-workbench-grants.png`,
  `agreement-workbench-save-handoff.png`, and
  `agreement-workbench-ux-summary.json` under the isolated verification
  artifact directory

## Residual assumptions and open items

- The runtime can enforce `S` only when a Cell or consumer path explicitly asks
  for `---s`; it cannot infer external persistence after output disclosure.
- Future features that persist another Cell's output must add explicit Storage
  requests and both allowed/denied tests.
- Forwarding/disclosure authorization still needs a separately approved
  capability/Contract design before implementation.
- Cross-language CellProtocol ports must preserve the same four-position wire
  semantics when their permission parsers are updated.
- Agreement Workbench is functionally useful for an internal technical user,
  but its recurring access prompt, raw payload disclosure, and permission-control
  desynchronization are release blockers for a general end-user experience.
- The UX findings were recorded, not fixed, because this follow-up requested a
  quality assessment and safe publication rather than a broader redesign.

Final human inspection/sign-off remains with Kjetil.
