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

### Present the tree visually (Kjetil 2026-09-28)

Show the §1 tree in the **Formålstrær** page (https://claude.ai/artifact/DAXLyDGAwej65jb7fnfVJS), not only as a table. Write it to the page's database as `trees/<id>` with `ArtifactData set`. The format and the sync rules are in `Deliverables/PDD_formaalstre-verktoy_2026-09-28/README.md`, and the parse script in `seed/`. Pull Kjetil's edits back into §1 and §7 before a gate. Changes to Book 23 arrive as `proposals/*`, and only `godkjent` ones are applied.

Pitfall seen 2026-09-28: when editing a FORMAALSSPEC with Python `str.replace`, a test-id anchor also matches the §1 verifier cell. Row insertions then land in the purpose table. Slice to the section first, for example `s.index('## 5.')`, and replace inside that slice only.

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

### Verification and landing tools (queue-run on the Mac)

- `HAVEN-Deploy/_handoff/LANDING/land-cellprotocol.sh <spec>` runs the full `swift test` on a clean export of `origin/main` against the worktree, checks that every bundle completes, and blocks on any new failure. The test-count difference must equal the number of new test methods. It then commits and pushes to main.
  - With `PORTS_ONLY=1` it runs every gate but does not land. Use this when Kjetil must see the result first. His rule is that a new capability is tested against function and purpose before it reaches main.
  - With `ARTIFACT_TEST`/`ARTIFACT_ENV` it runs a gated test that must write files, for example screenshots.
- `HAVEN-Deploy/_handoff/LANDING/verify-palazzo.sh <spec>` does the same for a PalazzoScaffold branch. Both runs build against a clean export of a named CellProtocol revision (`CP_REV`), never the shared `../CellProtocol`. It pushes the branch with `PUSH=1` and never merges.
- `HAVEN-Deploy/_handoff/LANDING/ci-status.sh <owner/repo>@<sha>` reports CI for a landed commit. `/usr/local/bin/gh` on Kjetil's Mac is an Intel binary and fails with «Bad CPU type»; the script picks a working `gh`.
- Keys and gates are documented in `HAVEN-Deploy/_handoff/LANDING/README.md`. For screenshots of a native SwiftUI `List`, use `NSHostingView` in an off-screen window with `cacheDisplay`. It was verified 2026-09-28 with `HAVEN-Deploy/_handoff/PALAZZO-VEKT/bildevei-probe.sh`, which also runs on Macs in dark mode. `ImageRenderer` draws a yellow "not supported" placeholder in place of the `List`. A pixel-variety check does not catch that, so look at the image or assert on content.
- Codex prompts that ask for tests on cell data must say: compare `ValueType` `.object`/`.list` as sorted-key JSON, never with `XCTAssertEqual` on the values. Equal content compares unequal (lesson.valuetype-equality-false-for-objects). This recurred 2026-09-29 in the Palazzo bench self-test (6 false failures).
- Before judging images from a gate run, check that they come from that run: compare md5 with the previous run, and read which port stopped. On 2026-09-29 a copy step picked the newest artefact folder that existed, from an earlier run, and the stale images looked new (new mtime). Copy only from the run's own evidence folder.
- Checksums do not tell whether a PNG is the same picture once it has left a Cowork cloud session. The session's outputs folder (the one `SendUserFile` delivers from) adds a `caBX` chunk of about 5.8 kB to PNG files, so the delivered copy has another md5 than the copy in scratch, with the same pixels. To decide whether an approved image has changed, compare pixels (PIL: `ImageChops.difference(a.convert("RGBA"), b.convert("RGBA")).getbbox() is None`), and when a package is rebuilt, take the image bytes from what was delivered, so what Kjetil has seen stays byte for byte the same. Seen 2026-10-03 with the three G1-GUI images in `Deliverables/PDD_agent-planlagte-jobber_2026-10-02/images/` (`L-2026-10-03-en-png-som-har-gatt-gjennom-utdatamappen-i-en`).
- When Kjetil must choose or tune values, give him a page he can operate: presets as buttons, the values as controls, the effect on the purposes shown live, and a button that saves the choice where Losen can read it (artifact `db`). Options named only in chat text, and a test that writes a report, are not something he can use. Verify the page's formula against the real test output before publishing. Seen 2026-09-29 with the Palazzo weight bench.
- Binding pins CellProtocol in two places: the `XCRemoteSwiftPackageReference` requirement in `Binding.xcodeproj/project.pbxproj` (`kind = revision`) and `Package.resolved` in the project workspace. A pin lift must change both, and they may disagree beforehand. On 2026-09-30 main had 79497e8 in the pbxproj and b5b7282 in Package.resolved. `HAVEN-Deploy/_handoff/PALAZZO-VEKT/wp7-binding-pin.sh` does the lift with BindingTests before and after.
- In xcodebuild logs, read the test total from the line after `Test Suite 'All tests' passed|failed`. The last `Executed N tests` line belongs to the last sub-suite. Keep «no new failures» and «green» as separate verdicts, and report which one it is. On 2026-09-30 a WP7 run reported 9 tests and GREEN, while the suite had 162 tests and was red both before and after.
- Do not conclude that something «does not exist» or «does not work» from status documents. «Not verified», «not approved» and «open findings» mean nobody has shown it, not that it fails. Check the code and try the real path first, and say which of the two you did. On 2026-10-03 Losen told Kjetil the bridge chain did not exist after reading three status files; CellBridge is in CellProtocol main, Palazzo registers a bridgehead with passing bridge tests, and Binding already opens a Palazzo surface over `wss://…/bridgehead/…`. For parity without a live connection, Binding's `SkeletonSnapshotRenderXCTest` (`BINDING_SNAPSHOT_CORPUS_DIR`) renders a frozen corpus (`<name>/skeleton.json`, `state.json`, `surface.json`); that is a supplement, not a replacement for the running app.

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
- If the lesson changes how a *thread* should work (a tool, a route, a pitfall in
  a skill or prompt), also route it there: from the HAVEN root
  `python3 CellScaffold/scripts/haven_learn.py capture --what … --kind pitfall --target skill:<name>`,
  edit the target, `applied <id>`, `sync --id <id>` (skill `haven-learning-capture`).
  The lessons register says what went wrong; the learning ledger says which skill
  changed because of it, and whether that change reached every client.
- Run `purpose_dev.py validate` and fix what it reports.

## Boundaries

- Purposes never grant rights; a match is not an authorization (Purpose-Bound
  External Action Contract). `purpose://prompt.unknown` fails closed.
- Do not document planned behaviour as implemented. Do not mark a gate approved on
  Kjetil's behalf. Do not replace an image with a description.
- The method is meant to become cells in HAVEN; this skill and the JSON files are
  the seed and the reference implementation, not the product.

## Asking for a gate

A gate request is a message Kjetil must be able to act on without searching. It carries, every time:

1. The **absolute path** of the document — `/Users/<user>/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/<folder>/<file>.md`, not a bare filename.
2. What he is deciding, in one or two sentences.
3. What is deliberately not done, named.

He stated the path rule 2026-09-09 and had to repeat it 2026-10-01 after a G2 request that named
only `PLAN-E8.md`. Repeating a rule costs him more than the rule saves.

## Completion checklist

- [ ] §0 verbatim intent, all claims audited with status
- [ ] Every leaf purpose has goal (outcome, signals, verifier) and a §5 test
- [ ] Lessons from `lookup` quoted in §4 and reflected in §2/§5
- [ ] §3 expectation contract filled; GUI rows point at approved `images/` files
- [ ] STATUS.md gates set only by Kjetil's word; `validate` is clean
- [ ] Every gate request to Kjetil names the **absolute path** of the document he is being asked to approve
- [ ] TESTRESULT.md has real output for every §5 row (or `blocked` + reason)
- [ ] ACCEPT.md pairs expected/actual for every §3 row
- [ ] New lessons recorded; candidate purposes promoted or dropped

## Independent purposes must have independent failures

When one run serves two purposes, a failure in the lesser one must not take the greater one
with it. Measured 2026-09-30 in HD-0077: the host deploy served two purposes — *get the
guest and waiter surfaces onto the web* and *let a model phrase the concierge's answers*.
The model key turned out to be unusable, the host script returned exit 4, and the deploy
script treated that as fatal. The surfaces were never deployed, because a **wording** feature
had failed.

The purposes were independent. The failure handling was not.

Checks to run whenever a script or a pipeline serves more than one purpose:

- **List the purposes the run serves**, and for each, name what must be true for it to be
  met. If purpose B can fail while purpose A is still met, B's failure is a warning.
- **Order the steps so the shared prerequisites come first**, then the independent parts, so
  a failure late in B cannot undo A.
- **Never infer that a purpose was met from an input being present.** The deploy assumed
  "a key file existed, therefore the model is on" and set the acceptance expectation from
  that — which would have failed the whole acceptance run on something that is not a defect.
  Measure the outcome on the host and set the expectation from the measurement.
- **Say which purpose failed, in the report**, so the next reader does not think the whole
  run is broken.

