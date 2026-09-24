# Chapter 35 — Purpose-Driven Development Workflow

Status: draft-canonical-source · Created 2026-09-03 · Last verified against tooling: 2026-09-03

This chapter is the contract for how development work in HAVEN is defined,
agreed, built, tested and remembered. It applies to code (CellProtocol,
CellScaffold, Binding, PalazzoScaffold, Python companions), to
CellConfiguration/skeleton work, and to combinations of cells. It is the
development-side counterpart of Chapter 30 (panel task decomposition): Chapter 30
adjudicates claims; this chapter delivers things Kjetil will see and use.

The method is intended to become cells in HAVEN. Until then, the skill
`.claude/skills/haven-purpose-driven-dev/SKILL.md`, the JSON files in `Book/`,
and `Tools/PurposePackages/purpose_dev.py` are the reference implementation.

## 1. The problem the workflow solves

Three recurring failures are on record and each has a mechanism here:

| Failure (lesson ref) | Mechanism |
|---|---|
| Kjetil expected something else than what was shown, usually GUI (`lesson.text-ux-is-not-design`) | Gate **G1-GUI**: a rendered image per surface and state is approved before any implementation; the image is the acceptance reference. |
| A plan or document was delivered instead of the thing (`lesson.plan-instead-of-delivery`) | §3 *expectation contract* lists the concrete artifacts; after **G2** only those count as progress. |
| Known mistakes were repeated (`lesson.bridge-inferred-architecture-from-one-use`, `lesson.cellscaffold-two-holes`, tooling lessons) | The **lessons register** is matched on tags/purposeRefs and printed at decomposition time; preventions become derived tests on packages. |

## 2. Objects

### 2.1 Purpose node

Same shape as `haven.purpose-knowledge-base.v0` nodes (Chapter 23):
`purposeRef`, `parentRef`, `title`, `summary`, `status`, `goal{goalRef, lifecycle,
outcome, successSignals[], verifier}`, `matchingHints`. Package nodes add
`derivedTests[]` (below). New task-local nodes are `purpose://candidate.<slug>.<name>`
with `status: candidate`; they enter Book 23 only through the capture process in
Chapter 23 §8, never by side effect.

Decomposition is **classification first**: choose from Book 23 and the packages,
then name what is missing. A model may select among candidates; it never mints
`purpose://` refs (Small_Model_Purpose_Decomposition_Research_2026-07-11).

### 2.2 Derived test

```json
{ "testRef": "test.gui.parity", "kind": "inspection",
  "description": "Side-om-side referanse/faktisk per flate.",
  "how": "Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md.",
  "evidence": "ACCEPT.md#parity" }
```

`kind` ∈ `command | inspection | measurement | artifact`. A test without `how`
and `evidence` is an intention and fails validation. Status at run time:
`venter | grønn | rød | blocked`.

### 2.3 Purpose package (`haven.purpose-package-set.v0`)

`Book/haven_purpose_packages_v0.json`. A package is a reusable bundle:
`packageRef`, `triggers{surfaces[], tags[]}`, `purposes[]` (nodes with derived
tests), `inheritedPurposeRefs[]` (Book 23 nodes and facets that ride along),
`requiredArtifacts[{path, gate, description}]`, `lessonRefs[]`. Packages in
`alwaysAttach` are attached to every task. Packages are *not* rights and do not
authorize anything (Purpose_Bound_External_Action_Contract_2026-08-03).

Initial packages: `pkg.std.everything-works` (always), `pkg.std.gui-surface`,
`pkg.std.cell-contract`, `pkg.std.cell-combination`, `pkg.std.codex-handoff`.
Chapter 23's five facets are the de facto older form of the same idea; packages
reference them through `inheritedPurposeRefs` rather than duplicating them.

### 2.4 Lesson (`haven.lessons-register.v0`)

`Book/haven_lessons_register_v0.json`. Required fields: `lessonRef, date,
symptom, cause, prevention, purposeRefs, tags, source`; `severity` ∈
`blocker | major | minor`. `symptom` is the observation; `cause` is what is
documented (write `ukjent` rather than guess); `prevention` is phrased so it can
be lifted into a `derivedTest`. Lessons are matched on `tags ∩ (task tags ∪
surfaces)` or `purposeRefs ∩ attached purposes`.

### 2.5 Task folder

`Deliverables/PDD_<slug>_<date>/` with `FORMAALSSPEC.md` (§0–§7, see
`Prompts/Purpose_Driven_Dev_Spec.md`), `STATUS.md` (gates, surfaces, tags, plan
switches), and after G1: `PLAN.md`, `TESTRESULT.md`, `ACCEPT.md`, plus the
artifacts the attached packages require (`images/`, `skeleton/`, `contract/`,
`dataflow.md`, `handoff/`).

## 3. Phases and gates

```
P0 Intent ──► P1 Decompose ──G1──► [P1-GUI Render ──G1-GUI──►] P2 Plan ──G2──► P3 Implement ──► P4 Test ──► P5 Accept ──G3──► P6 Learn
                 ▲    │                                                                                          │
                 └────┘ iterate until Kjetil approves                                                            └──► lessons, promotions, package updates
```

| Gate | Set by | Precondition enforced by `validate` |
|---|---|---|
| G1 | Kjetil | `FORMAALSSPEC.md` exists, no TBD/TODO |
| G1-GUI | Kjetil, looking at the image | `images/` non-empty (and `skeleton/` when Porthole-rendered); required whenever surfaces include `gui skeleton porthole binding web` |
| G2 | Kjetil (or "auto" for small tasks, said explicitly) | G1 approved; G1-GUI approved for GUI tasks; `PLAN.md` and package artifacts present |
| G3 | Kjetil | `TESTRESULT.md`, `ACCEPT.md`, `STATUS.md` present |

A gate is a word from Kjetil, recorded as `- G1: godkjent <date>` in STATUS.md.
The tool cannot approve; it can only refuse.

## 4. Tooling

`Tools/PurposePackages/purpose_dev.py` (stdlib Python; runs in the macOS terminal
and in the Cowork VM through `device_bash`):

- `lookup --tags … --surfaces …` — which packages attach, their purposes and
  derived tests, the lessons to read, and Book 23 nodes that lexically match.
- `new <slug> --intent "…" --tags … --surfaces …` — creates the task folder with
  the spec prefilled (§4 and §5 generated).
- `validate [taskdir]` — schema and reference integrity of packages and lessons;
  gate/artifact consistency of a task folder.
- `gates <taskdir>` — gate readiness at a glance.
- `lesson add <taskdir>` — append a lesson interactively.

Codex follows the same files: give it the task folder path and the skill path;
it needs nothing else.

## 5. Where this knowledge lives — evaluation of RAG, graph and files

Kjetil asked whether the purpose packages and lessons should go into a RAG store,
a graph database, or something else. Decision for v0: **files in git are the
source of truth; indexes are derived; no new database.** Reasons:

1. Chapter 23 already defines the purpose tree as a JSON source with a derived
   index (`derive_purpose_index.mjs`: ordinals, DFS ranges, ancestor bitsets,
   token/capability/goal postings) and a deterministic resolver. Packages use the
   same node shape, so they can be merged into that index without a new store.
2. `Tools/ModelKnowledge/extract_haven_graphs.py` already derives
   `haven_purpose_graph.json`, the Book link graph and the claim/source graph.
   A graph *view* exists; a graph *database* would add an operational dependency
   for 57 + 12 nodes and 15 lessons.
3. The research on small-model decomposition (2026-07-11) and the AI Act
   derivation (2026-08-18) both concluded that matching must be classification
   over a known, structured set with confidence routing — which is what a
   versioned file plus a deterministic index gives, and what free-text RAG
   retrieval does not guarantee (`lesson.free-text-is-not-a-declaration`).
4. Retrieval for humans and agents already exists read-only through
   `Tools/HavenDocsMCP`; adding the two JSON files to its resources makes them
   searchable without a second retrieval path.

Revisit when any of these holds: more than ~300 lessons; lessons must be found by
semantic similarity across repositories rather than by tags/purposeRefs; or the
method has moved into cells and the runtime needs its own store. At that point the
natural home is a HAVEN cell that owns the register, with the same schema — not an
external database.

## 6. Roles

- **Kjetil** states intent, approves G1/G1-GUI/G2/G3, decides promotions to Book 23.
- **Losen (Claude)** decomposes, renders, plans, records lessons, keeps STATUS.md true.
- **Codex** implements work packages from PLAN.md and runs `command` tests; reports
  into TESTRESULT.md.
- **Xcode / Porthole** render and build; screenshots from them are the parity evidence.

## 7. Boundaries and non-goals

- Purposes never create, widen or inherit rights; `purpose://prompt.unknown` fails closed.
- No canonical mutation of Book 23 without Kjetil; task-local nodes stay `candidate`.
- No documentation of planned behaviour as implemented; every artifact carries a date.
- This chapter does not define how the method becomes cells; that is a later chapter
  with its own contract JSON.

## 8. First trial

The first real run is the Palazzo guest-ordering skeleton
(`Deliverables/PDD_palazzo-gjestebestilling_<date>/`), chosen because it exercises
all three: GUI gate, cell contracts (`lesson.cellscaffold-two-holes`) and cell
combination with OrderX/GastroPlanner/Planday integration boundaries.
