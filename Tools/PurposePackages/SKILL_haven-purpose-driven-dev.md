---
name: haven-purpose-driven-dev
description: Use for ANY development task in HAVEN/CellProtocol/Binding/Palazzo — code, CellConfiguration/skeleton, or cell combinations — when Kjetil states something he wants built, changed, or fixed. Runs the purpose-driven development workflow (formålsdrevet utvikling, PDD) — intent → purpose tree with goals → iterate with Kjetil until approved (G1) → rendered image approved for anything visual (G1-GUI) → plan (G2) → implement → tests derived from goals and standard purpose packages → acceptance against the expectation contract (G3) → record lessons. Trigger on "jeg vil at…", "lag…", "implementer…", "endre flaten…", "sett opp celler for…", "dekomponer i formål", "formålspakke", or any request that would otherwise jump straight to code or a plan. Do NOT use for pure analysis/panel tasks (use haven-panel-task-decomposition) or for public-claim review.
---

# HAVEN Purpose-Driven Development (formålsdrevet utvikling)

The workflow exists to remove one failure above all others: Kjetil approves a
description, sees the result, and it is not what he meant — most often with GUI.
Everything below is built so that *what he will see* is agreed before anything is
built, tests fall out of the purposes rather than being invented afterwards, and
mistakes already made are shown again before they can be repeated.

Related skills: `haven-panel-task-decomposition` (analysis and claim adjudication —
reuse its brief-audit and goal discipline), `cellconfiguration-skeleton-authoring`
(how to render a skeleton through Porthole preview), `codex-collaboration` and
`cellprotocol-docs-and-rag-maintenance` (handoff and docs hygiene).

## Canonical sources (read before the first decomposition of a session)

- `Book/haven_purpose_knowledge_base_v0.json` — the purpose tree (57 nodes, `purpose://…`). Decomposition is **classification over this tree first**, generation second.
- `Book/haven_purpose_packages_v0.json` — reusable purpose packages (formålspakker) with derived tests, required artifacts and lesson refs. Attached automatically by tags/surfaces.
- `Book/haven_lessons_register_v0.json` — the register of experienced mistakes. Shown to Kjetil at decomposition time; grows in phase P6.
- `Tools/PurposePackages/purpose_dev.py` — `lookup`, `new`, `validate`, `gates`, `lesson add`. Pure stdlib; runs in the macOS terminal and in the Cowork VM.
- `Prompts/Purpose_Driven_Dev_Spec.md` — the FORMAALSSPEC template and the rules for each section.
- `Book/35_Purpose_Driven_Development_Workflow.md` — the contract for this workflow.

## Phases and gates

Every task lives in one folder: `Deliverables/PDD_<slug>_<date>/`. Create it with
`python3 Tools/PurposePackages/purpose_dev.py new <slug> --intent "…" --tags … --surfaces …`.
Surfaces: `gui skeleton porthole binding web cell scaffold bridge python codex terminal xcode`.

| Phase | Output | Gate | Who approves |
|---|---|---|---|
| P0 Intent | §0 of FORMAALSSPEC.md: Kjetil's words verbatim + brief audit | — | — |
| P1 Decompose | §1–§6: purpose tree, boundary, expectation contract, packages+lessons, derived tests, open questions | **G1** | Kjetil |
| P1-GUI Render | `images/<flate>-<tilstand>-v<n>.png` (+ `skeleton/` JSON when Porthole-rendered) | **G1-GUI** | Kjetil, by looking at the image |
| P2 Plan | PLAN.md: work packages 1:1 with leaf purposes; each names its test and its executor (Claude / Codex / Xcode / Kjetil) | **G2** | Kjetil (may say "auto" for small tasks) |
| P3 Implement | code / skeleton / contracts; each change references its purposeRef | — | — |
| P4 Test | TESTRESULT.md: output of every derived test (§5) | — | — |
| P5 Accept | ACCEPT.md: expectation (§3) next to actual, per deliverable; GUI side-by-side | **G3** | Kjetil |
| P6 Learn | new entries in the lessons register; candidate purposes promoted or dropped; packages updated | — | Losen, then Kjetil sees the diff |

STATUS.md holds gate state (`- G1: godkjent 2026-09-04`). Only Kjetil's explicit
word sets a gate to `godkjent`. `purpose_dev.py validate <folder>` refuses a gate
whose required artifacts are missing, G2 before G1, and G2 before G1-GUI on any
task with a GUI surface.

## P0 — Intent, verbatim, then audited

Paste Kjetil's request unchanged into §0. Then audit every factual claim and every
capability the request assumes, exactly as the panel skill does:
`retrieved` (read from a file this session, path given) / `recalled` / `unavailable` /
`contradicted`. Nothing `recalled` may become a load-bearing assumption of the plan.
If the request assumes something about bridge, skeleton format, a cell, or a
scaffold, read the source and cite the path — this is `lesson.bridge-inferred-architecture-from-one-use`.

## P1 — Decompose into purposes with goals

1. Run `purpose_dev.py lookup --tags … --surfaces …` and read the lessons it prints
   **before** writing a single purpose. Quote the relevant ones in §4.
2. Build the tree in §1. For each node:
   - Prefer an existing `purpose://` node from Book 23 or a package as parent or as
     the node itself. New nodes are `purpose://candidate.<slug>.<name>` and are named
     by you, never left to a model to invent (`lesson.decomposition-is-classification`).
   - Goal = `outcome` + `successSignals` + `verifier`, in the Book 23 shape. A node
     whose success cannot be observed is not ready; say so instead of padding it.
   - Every leaf gets at least one test in §5 (`command` / `inspection` /
     `measurement` / `artifact`), with *how* and *where the evidence lands*.
3. §2 Boundary: what this is **not**, and every dependency the task needs to be
   working first, each as its own row with a verifier (`lesson.corr-approval-surfaces-timed-out`).
4. §3 Expectation contract — "Det du kommer til å se". One row per deliverable:
   type (image / file / test output / running surface), where, reference. After G2
   this table is the only thing that counts as progress. A document *about* the
   deliverable is never the deliverable (`lesson.plan-instead-of-delivery`).
5. §6 Open questions: at most the ones that change the tree. Ask them with
   AskUserQuestion when Kjetil is present.
6. Present the spec to Kjetil as the spec itself (send the file), not a summary.
   Iterate: each round is a new row in §7 with what changed. Stop when Kjetil says
   G1 is approved; write `- G1: godkjent <date>` in STATUS.md.

No planning, no code, no skeleton edits before G1. If Kjetil asks for the result
directly, do P0–P1 in the same reply, compressed, and still get the G1 word.

## P1-GUI — The image gate (mandatory for any visual surface)

If any surface is `gui skeleton porthole binding web`, or any deliverable in §3 is
something Kjetil will look at:

- Produce a **rendered image per surface and per important state** (empty, filled,
  error). Order of preference: (1) Porthole runtime preview of the actual
  CellConfiguration/skeleton JSON, screenshot saved to `images/` and the JSON to
  `skeleton/`; (2) HTML mockup or design canvas at the same size, with an explicit
  list in §3 of what today's skeleton format cannot render (see
  `cellconfiguration-skeleton-authoring` for the limits — never imply a capability
  the renderer lacks).
- A textual UX description does not count (`lesson.text-ux-is-not-design`).
- Kjetil approves the *image*. The approved image becomes the acceptance reference
  for `test.gui.parity` at P5. Deviations found later are listed in ACCEPT.md and
  each is either fixed or approved by Kjetil with a reason.
- Write `- G1-GUI: godkjent <date>` only after that.

## P2 — Plan from the leaves

PLAN.md: one work package per leaf purpose, in dependency order, each with
`purposeRef`, executor, the derived test(s) it must turn green, and the artifacts
it produces for §3. Add the package artifacts (`contract/`, `dataflow.md`,
`handoff/README.md`) the attached packages require. Work that goes to Codex or the
terminal follows `pkg.std.codex-handoff`: idempotent script, dry-run default, no
comment after a command, no git through the mount.

## P3–P4 — Implement and test what the purposes say

Implement per work package. Then run **every** row of §5 and paste real output into
TESTRESULT.md under the anchors the tests name (`#build`, `#regression`,
`#load-time`, `#auth`, …). A test that could not be run is `blocked` with the
reason — never silently dropped. `pkg.std.everything-works` is always attached:
build, full regression, docs in the same change, STATUS.md current.

## P5 — Accept against the expectation contract

ACCEPT.md mirrors §3 row by row: expected → actual, with the evidence link. For
GUI: reference image and actual screenshot side by side, same viewport, plus the
behaviour checks (buttons hit real keypaths, fields take input —
`lesson.parity-was-correctness-not-decoration`). Send Kjetil the artifacts, not a
description of them. G3 is his word.

## P6 — Learn, so it is not repeated

For every deviation, bug, misunderstanding, or blocked test: add a lesson
(`purpose_dev.py lesson add <folder>` or edit the JSON) with symptom, documented
cause (write `ukjent` rather than guess), a prevention phrased so it can become a
`derivedTest`, the purposeRefs and tags that should surface it next time, and the
source path. Then:

- Promote `candidate` purposes that proved durable into a package or into Book 23
  via the capture process (Book 23 §8) — never mutate Book 23 canonically without
  Kjetil.
- If a lesson repeats a pattern, add the prevention as a `derivedTest` on the
  relevant package purpose so it is enforced, not just remembered.
- Run `purpose_dev.py validate` and fix what it reports.

## Boundaries

- Purposes never grant rights; a match is not an authorization (Purpose-Bound
  External Action Contract). `purpose://prompt.unknown` fails closed.
- Do not document planned behaviour as implemented. Do not mark a gate approved on
  Kjetil's behalf. Do not replace an image with a description.
- The method is meant to become cells in HAVEN; this skill and the JSON files are
  the seed and the reference implementation, not the product.

## Completion checklist

- [ ] §0 verbatim intent, all claims audited with status
- [ ] Every leaf purpose has goal (outcome, signals, verifier) and a §5 test
- [ ] Lessons from `lookup` quoted in §4 and reflected in §2/§5
- [ ] §3 expectation contract filled; GUI rows point at approved `images/` files
- [ ] STATUS.md gates set only by Kjetil's word; `validate` is clean
- [ ] TESTRESULT.md has real output for every §5 row (or `blocked` + reason)
- [ ] ACCEPT.md pairs expected/actual for every §3 row
- [ ] New lessons recorded; candidate purposes promoted or dropped
