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

All paths below are relative to the **CellProtocolDocuments** repo — not CellProtocol, not CellScaffold. A Cowork thread must have CellProtocolDocuments connected before P1, and `purpose_dev.py new` creates the task folder in `CellProtocolDocuments/Deliverables/`.

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

### "Read" names a reader and a file list (HD-0077, 2026-10-07)

A plan may say a source "is read" only about the files a named reader actually read. The plan for the
Palazzo concierge said the kernel folder "is read (29 files)" when Losen had read 12 and parts of
three; an independent thread counted it. Write who read which files (Losen, or a reading thread with
the path to its report), and list the files nobody read. When a claim in the plan rests on unread
files, send a reading thread with a hard time limit before the plan is presented. The fourteen unread
files changed two findings and added three
(`HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/les/L6-KJERNEREST.md`).

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

### Measure what the step before yours delivers (HD-0077, 2026-10-04)

Pitfall: a rule for one link was taken for the reach of the chain. The task was to let a
language model phrase more of the Palazzo concierge's answers. The guard was rebuilt so that
53 texts can be published: five for the pizza list, and four for each of twelve dishes after
one of eleven question forms. The lookup that produces the approved answer stood in §2 only
as something the task would not improve. It was not a dependency row with a measurement of
what it returns for those questions. Measured on the running service afterwards, with two
of the eleven forms («Hva er `<navn>`?», «Fortell om `<navn>`.»), the lookup returns the
dish for six of the twelve; four get no answer and two get the pizza list. 29 of the 53
texts are shown to reach a guest. Three of those answers had been measured two days earlier
in the same task and were not used.

- Every step **before** the one you change is a §2 row whose verifier is a measurement on
  the running service, taken before G1: what does it deliver for the inputs the purpose is
  about? If it cannot be measured yet, the row says «ikke målt» and the reach is unknown.
- State the reach of a purpose as a measured number ("six of twelve dishes on the web"),
  not as the size of the rule ("twelve of eighteen dishes").
- Before writing §1, search the task's own evidence folder for earlier measurements of the
  same dependency.

Evidence: `HAVEN-Deploy/_handoff/HD-0077/maal/SPOER-RUNDE2C2-RETTER-20261004.md`,
`HAVEN-Deploy/_handoff/HD-0077/maal/SPOER-PROEVE-20261002.md`,
`HAVEN-Deploy/_handoff/HD-0077/maal/SPOER-PROEVE-2-20261002.md`.

### A limit in today's code is a finding, not a premise (correspondence thread, 2026-10-06)

Pitfall: the purpose was that Kjetil and each of two people write to each other, encrypted and
with attachments. Reading the code showed that in the correspondence cell the owner receives
everything but cannot send an attachment, and that the client has no path for the owner in
production (the client code accepts an owner profile, and the tests use one). The spec laid out
for G1 took that as given. Its first choice said «Da må noen andre enn de to være eier»,
recommended that the server own the cell, and advised against the alternative where the owner is
himself a party with the key his agent uses, for three reasons, two of which were things the code
does not do today. The spec did not say what the alternatives were ranked by. An independent
checker, given the same frame and asked for a simpler fourth way, found none, and wrote that the
recommendation «følger av koden som minste konsistente endring». Kjetil, the same evening: «Jeg
synes du har rotet det til. En chat celle må kunne brukes av eier også. Om det er vanskelig så
er  det feil satt sammen.»

- When today's code rules out the plain reading of the purpose (here: that the owner can use his
  own cell, which he said in so many words afterwards), write that in §0 as a finding about the
  code, and make «change the code so that it can» the first alternative. An alternative that
  builds around the limit says that this is what it does, and what it costs.
- Say what the alternatives are ranked by. «Least change to the code» is a ranking he has to ask
  for. A reason against an alternative that reads «the code cannot do this today» is a work
  package.
- Give the checker his words from §0, not your summary of them. The brief said «to agenter (hans
  egen og en samarbeidspartners)»; his words named two people. Ask it where the text goes from
  «the code is like this» to «so the model must be like this», and whether that step is put to
  him as a choice.
- Before designing around a gap, look for a cell that already does the thing. He pointed to the
  chat cell: everyone who wants messages subscribes to Flow, and `get state` gives the history.
  The spec did not mention it.

Evidence: `Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/iterasjon-2/FORMAALSSPEC.md`
(§6, choice 1), `panel/FABEL-G1-RUNDE-2-MODELL.md` and `STATUS.md` in the same task folder.

### «Few steps» is counted for every party, from the images (correspondence thread, 2026-10-07)

Kjetil, 2026-10-06: «Og det er altfor mye manuelle operasjoner.» The G1 page drafted the day
after counted three handgrips for the recipient (install one package, give the agent one link,
send a code) and said «én gang per person» for the owner; the specification behind it said «ett
trykk». The image for that step showed two Touch ID prompts per person (make the link, approve)
and a code to compare, and the page listed the approval before the sending of the package and
the link. The check before G1 found both.

- Count the handgrips for each party the purpose names, the owner first, per person and per
  round (first time, renewal). Take the count from the images or the skeleton, not from the
  prose.
- Write them in the order they happen.
- A step that exists because of a proposal of yours (here: a six-digit code) is marked as a
  proposal, with the count with and without it.
- Make the count a row in §3 with a test: a recording on a clean machine where the handgrips are
  counted.

Evidence: `Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/KONTROLL-G1-ITERASJON-3.md`
(points 1 and 4).

## P1-GUI — The image gate (mandatory for any visual surface)

If any surface is `gui skeleton porthole binding web`, or any deliverable in §3 is
something Kjetil will look at:

- Produce a **rendered image per surface and per important state** (empty, filled,
  error). Order of preference: (1) Porthole runtime preview of the actual
  CellConfiguration/skeleton JSON, screenshot saved to `images/` and the JSON to
  `skeleton/`; (1b) **the web renderer alone, without a server** — export
  `Public/js/skeleton-runtime.js`, `Public/css/porthole-webo.css` and
  `Public/js/haven-localization.js` from CellScaffold `origin/main` (md5 in
  `images/README.md`), render the candidate skeleton JSON with sample data in
  Playwright/Chromium (template: `Deliverables/PDD_lister-celle-og-komponent_2026-10-02/images/render.js`;
  runs in the Cowork VM, no Swift needed), and record the `onAction` payloads of every
  button, field and drag in the same run — those are the shapes the cell must accept;
  (2) HTML mockup or design canvas at the same size, with an explicit
  list in §3 of what today's skeleton format cannot render (see
  `cellconfiguration-skeleton-authoring` for the limits — never imply a capability
  the renderer lacks).
- Render the app width with the app's capabilities (`touch`, or `pointer/hover/keyboard`),
  not the web's (`drag`): a `layoutVariants` element that hides on `drag` otherwise shows
  the web variant in the "app" image (PDD_lister, app images had to become `-v2`).
- Close the loop after implementation: a test that the Swift factory's skeleton is
  canonically byte-identical to the fixture the images were rendered from
  (`ListsConfigurationTests.testFactoryProducesTheApprovedSkeletonByteForByte`), and at P5
  a render from the cell's *real* state with a pixel diff against the reference
  (`lesson.render-candidate-skeleton-with-the-web-renderer-before-g1-gui`; PDD_lister: 0 px).
- A textual UX description does not count (`lesson.text-ux-is-not-design`).
- Kjetil approves the *image*. The approved image becomes the acceptance reference
  for `test.gui.parity` at P5. Deviations found later are listed in ACCEPT.md and
  each is either fixed or approved by Kjetil with a reason.
- Write `- G1-GUI: godkjent <date>` only after that.
- A PNG delivered from a Cowork cloud session has so far had another md5 than the rendered
  file, and the same picture (four files measured 2026-10-07, and the earlier cases in the line
  referred to here): a `caBX` chunk is added on the way; which step adds it is not measured (see
  «Checksums do not tell…» under P3–P4). Compare the `IDAT` data or the pixels, and take the md5
  of an approved image from the delivered file.

### A sketch rendered from the live page carries the page's own labels (HD-0077, 2026-10-07)

When the reference image is rendered from the page's own HTML, CSS and script with canned answers,
everything the page already draws comes along. On Palazzo the badge «høy sikkerhet» sat above every
offer of a dish, where it can be read as "the dish is safe", and nobody had mentioned it. Before an
image is shown:

- Read the whole frame against the rules of the task, not only the parts the sketch adds.
- List in `images/README.md` everything the sketch takes away (a hidden warning, hidden sources). A
  crop that hides the allergen line shows an answer the guest will never get.
- When something visible is Kjetil's choice, render the alternative next to the proposal in an extra
  image, and put the question in the README with what each answer leads to.
- Let the text checker see what the frame ends with (the visible badge, warnings shown or hidden),
  carry the reference strings itself, and be tried with changes that must turn it red
  (`Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05/images/kilde/proev_sjekken.py`).

## P2 — Plan from the leaves

Kjetil reads PLAN.md as "what does it mean and what do I do" (2026-09-13). Start it with a
table **«Dette skal du gjøre»** (when / what / why, Kjetil's rows only), and add a lanes
graph: one lane per actor (Kjetil, Losen in the cloud, the queue on the Mac, documents),
one box per work package along time, arrows for order — template
`Deliverables/PDD_lister-celle-og-komponent_2026-10-02/images/plan-v1.html` → PNG with
Playwright. Kjetil 2026-10-08: this lane view belongs in the developer workbench too
("mest nyttig når det er flere som skaper sammen").

PLAN.md: one work package per leaf purpose, in dependency order, each with
`purposeRef`, executor, the derived test(s) it must turn green, and the artifacts
it produces for §3. Add the package artifacts (`contract/`, `dataflow.md`,
`handoff/README.md`) the attached packages require. Work that goes to Codex or the
terminal follows `pkg.std.codex-handoff`: idempotent script, dry-run default, no
comment after a command, no git through the mount.

### Stop rules when Kjetil says "auto" (his reading, 2026-10-05)

A plan that runs on "auto" names when the thread stops and waits for Kjetil. In HD-0077
three such rules were read more loosely than he meant. Asked afterwards which of them
should be read more strictly, he chose all three:

- **«A6: også egne tester».** "An existing test" is any committed test, also one the thread
  wrote earlier the same day. Changing it is a question to Kjetil first.
- **«A11: stopp ved kode 000».** A red check stops the run also when the cause is a call
  that never arrived. The check is not run again without his word.
- **«A12: enhver claim».** Any claim on the host stops a deploy, not only a claim on the
  same service or container.

He decided this for HD-0077. Take it as the default reading elsewhere, and ask before
assuming a looser one. Write a stop rule so that it cannot be read two ways: say what counts
("any committed test", "any claim on the host") and what the thread does then ("stop and
tell Kjetil"), never "try again".

**A brake works only if it is in place before the checkpoint.** On 2026-10-06 a commit showed
172 changed lines in a file where about 50 were expected. The brake file was written 13
seconds after the chain had passed its brake check in front of the push, so the commit was
pushed. Let the chain itself assert the size it expects (lines in, lines out, the list of
files) and stop when it differs, and run commit and push as two queue jobs whenever a number
a person must read sits between them.

Source: `Deliverables/PDD_palazzo-dekningsvakt-runde2_2026-10-02/STATUS.md` (his answers,
verbatim) and `Deliverables/PDD_palazzo-dekningsvakt-runde2_2026-10-02/ACCEPT.md` §3, rows
A6, A11 and A12.

### Promise the rule, not the category (HD-0077, 2026-10-07)

"A sentence with a phone number is never sent to the model" is a promise about a category, and no
list of patterns keeps it: three check rounds each found a way of writing a number or an address
that slipped through. In a plan, a contract and a test name, state the rule that will be built, and
what gets through it. For anything that leaves the house, prefer a list of what is let through
(letters, spaces, plain punctuation) to a list of what is stopped: what passes is then known by
construction. Compute the examples with a script kept next to the contract
(`Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05/contract/forhaandssjekk_regnet.py`),
including the sentences that still pass, and name the deviation when an approved test promised the
category.

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
- **Anyone who writes a test on cell data** (you, Codex, a subagent) compares `ValueType` `.object`/`.list` as sorted-key JSON, never with `XCTAssertEqual` on the values. Equal content compares unequal (lesson.valuetype-equality-false-for-objects). Say it in every prompt that asks for such tests, and check your own tests for it before the first run. It recurred 2026-09-29 in the Palazzo bench self-test (6 false failures) and 2026-10-06 in a test Losen wrote himself: two identical response envelopes compared unequal, so the test was red against correct code. The green run caught it. A helper that works: parse both response bodies with `JSONSerialization` and compare the `.sortedKeys` output (`kanonisk` in `HAVEN-Deploy/_handoff/HD-0077/strakstiltak-20261006/steg5/Tests/AppTests/PalazzoAllergiHenvisningUtenOppslagTests.swift`).
- XCTest did not record every failure message from a loop with many failing assertions: in three runs it kept 30, 28 and 30 of 125 (2026-10-06; cause unknown). Collect the deviations in the loop and throw one error at the end with the count and the rows, and count from that error, not from the messages. Example: `Avvik` in `PalazzoScaffold/Tests/AppTests/PalazzoAllergiHenvisningTests.swift`.
- Before judging images from a gate run, check that they come from that run: compare md5 with the previous run, and read which port stopped. On 2026-09-29 a copy step picked the newest artefact folder that existed, from an earlier run, and the stale images looked new (new mtime). Copy only from the run's own evidence folder.
- Checksums do not tell whether a PNG is the same picture once it has left a Cowork cloud session. The session's outputs folder (the one `SendUserFile` delivers from) adds a `caBX` chunk of about 5.8 kB to PNG files, so the delivered copy has another md5 than the copy in scratch, with the same pixels. To decide whether an approved image has changed, compare pixels (PIL: `ImageChops.difference(a.convert("RGBA"), b.convert("RGBA")).getbbox() is None`), and when a package is rebuilt, take the image bytes from what was delivered, so what Kjetil has seen stays byte for byte the same. Seen 2026-10-03 with the three G1-GUI images in `Deliverables/PDD_agent-planlagte-jobber_2026-10-02/images/` (`L-2026-10-03-en-png-som-har-gatt-gjennom-utdatamappen-i-en`).
  - Measured again 2026-10-07 on four PNGs in `Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/` (`figur/` and `images/`): each file on the Mac had one `caBX` chunk of 5758 bytes right after `IHDR` and was 5770 bytes larger than the rendered file, and the `IDAT` chunks put together had the same md5 in both. The readable labels in the chunk are those of a C2PA manifest (`c2pa.claim.v2`, claim generator «Anthropic Files», action `com.anthropic.claude.provided`). For one of the four, the copy in the outputs folder (file time 15:31:57Z) had no chunk at 15:40Z, while the file on the Mac, written 15:32Z, had one. Which step adds the chunk, and when, was not measured: three of the four copies in the outputs folder had it and one did not, so that the outputs folder adds it, as the line above says, is not shown for every file. For that file the copy in the outputs folder did not tell what was delivered: take the md5 of a delivered image from the delivered file. Nine text files written to the same folder that day had the same md5 on both sides. `panel/png_blokker.py` in that folder (standard library only) prints the chunks and the md5 of the `IDAT` data for each file it is given. The thread that measured this had `lesson.md5-differs-for-images-written-from-the-cloud` listed in §4 of its own spec (printed there by `lookup`) and, by its own account, still took the mismatch for something new: when the md5 of a delivered file differs, search this skill and the lessons register for the file type before measuring. Evidence: `Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/MAALT-PNG-CABX-20261007.md`.
- When Kjetil must choose or tune values, give him a page he can operate: presets as buttons, the values as controls, the effect on the purposes shown live, and a button that saves the choice where Losen can read it (artifact `db`). Options named only in chat text, and a test that writes a report, are not something he can use. Verify the page's formula against the real test output before publishing. Seen 2026-09-29 with the Palazzo weight bench.
- Binding pins CellProtocol in two places: the `XCRemoteSwiftPackageReference` requirement in `Binding.xcodeproj/project.pbxproj` (`kind = revision`) and `Package.resolved` in the project workspace. A pin lift must change both, and they may disagree beforehand. On 2026-09-30 main had 79497e8 in the pbxproj and b5b7282 in Package.resolved. `HAVEN-Deploy/_handoff/PALAZZO-VEKT/wp7-binding-pin.sh` does the lift with BindingTests before and after.
- In xcodebuild logs, read the test total from the line after `Test Suite 'All tests' passed|failed`. The last `Executed N tests` line belongs to the last sub-suite. Keep «no new failures» and «green» as separate verdicts, and report which one it is. On 2026-09-30 a WP7 run reported 9 tests and GREEN, while the suite had 162 tests and was red both before and after.
- Do not conclude that something «does not exist» or «does not work» from status documents. «Not verified», «not approved» and «open findings» mean nobody has shown it, not that it fails. Check the code and try the real path first, and say which of the two you did. On 2026-10-03 Losen told Kjetil the bridge chain did not exist after reading three status files; CellBridge is in CellProtocol main, Palazzo registers a bridgehead with passing bridge tests, and Binding already opens a Palazzo surface over `wss://…/bridgehead/…`. For parity without a live connection, Binding's `SkeletonSnapshotRenderXCTest` (`BINDING_SNAPSHOT_CORPUS_DIR`) renders a frozen corpus (`<name>/skeleton.json`, `state.json`, `surface.json`); that is a supplement, not a replacement for the running app.

### Prove the layer below before fixing the layer above (Kjetil 2026-10-07)

Kjetil: «Du må være sikker på at CellProtocol er fikset før du prøver å fikse på kode som bruker den.» and «DU må verifisere at ting virker.»

- **A green test suite is not proof of the path a consumer needs.** On 2026-10-07 CellProtocol had 1297 green tests on the pinned revision, and every bridge test used the owner. The path the admin surfaces needed (a non-owner reads across the bridge with an owner-issued credential and proof of its own key) had no test. Write one test for exactly that path, in the lower layer, run it on the pinned revision and on `main`, and only then touch the consumer.
- **Read the test file yourself.** Check that it uses separate vaults, a requester who is not the owner, and no bypass. A table that says «green» is a receipt, not a verification.
- **When a surface does not open, read the server's own error lines before reading code.** A source-only diagnosis of 33 failing surfaces ended, honestly, with 33 of 33 «unknown». The log gave the answer in two minutes. Tool and pitfalls: `HAVEN-Deploy/_handoff/RELEASE/LES_MEG.md`, section «Serverens feilspor når en flate ikke åpner».
- **Never call a failure «only an approval the user must give» until you have tried the approval.** The «Approve now» banner could not grant anything; the action answered HTTP 200 `ok: true` and changed nothing.
- **A measurement job and a fix job are different orders.** A queue job that says «follow this skill» and asks for a fix stops at G1, correctly, when no approved FORMAALSSPEC exists. Order the reproduction (one test, no change in `Sources/`, no push) as a measurement, and bring the fix to Kjetil as G1 with the measurement in hand.

## P5 — Accept against the expectation contract

ACCEPT.md mirrors §3 row by row: expected → actual, with the evidence link. For
GUI: reference image and actual screenshot side by side, same viewport, plus the
behaviour checks (buttons hit real keypaths, fields take input —
`lesson.parity-was-correctness-not-decoration`). Send Kjetil the artifacts, not a
description of them. G3 is his word.

### Build ACCEPT.md from the evidence, and have it checked (HD-0077, 2026-10-04)

Kjetil reads ACCEPT.md and TESTRESULT.md as fact. In HD-0077 round 2 a first draft, written
from the session's memory while the evidence lay on a machine out of reach, had 27 errors
when an independent thread held it against the evidence files. What worked after that:

- **Numbers, times, commits and quotes are filled in by code.** The documents are templates
  with placeholders. A values module reads each evidence file and asserts the counts it
  expects, and the build refuses to write a document while a value is missing. What exists
  only in the session, with no evidence file, is named as such at the top of the document.
- **An independent thread checks the built documents before Kjetil gets them.** It gets the
  documents and read-only copies of the evidence, and a bounded brief: which sections, what
  to compare, what not to judge (language, whether the rules are good), one verdict per
  statement (`stemmer`, `FEIL`, `upresis`, `uten bevis`, `uten bevis (oppgitt)`,
  `kan ikke kontrolleres her`), a time limit, and a list of what it did not reach. The
  second check held 160 statements
  against the evidence: 132 matched, 1 was wrong, 5 were imprecise, 9 had no evidence file
  and 13 could not be checked from the package.
- **Corrections made after the check are unchecked.** Say so in the document.
- **The same holds for a status message, and for the README beside a script.** On 2026-10-06
  a message went to Kjetil a quarter of an hour before the documents it pointed to were
  checked. The check found eleven places: an inference written as a measurement («the tool
  would have run with umask 077», which follows from sudo's documented default and was not
  measured on the host), the reviewers' remarks rendered as «a fault» and «all corrected»,
  an answer left out where a safeguard was described, and a time for when a run would be
  done, with no basis given. Write at each statement whether it is measured, read or
  inferred, give an estimate as a span with what it rests on, and let the check come before
  the message. Report: `Deliverables/PDD_korrespondanse-fornyelse_2026-09-30/panel/FABEL_DOK_RUNDE4.md`.
- **Every question Kjetil is asked to try has been asked of the running service first.** A
  draft used «Hva er Arancini?» as its example. The service does not answer that question.
- **A statement about all tests is a statement about each of them.** The one error the check
  found was «røde først» claimed for every new or changed test. Twelve changes to existing
  tests had come in with the code and were never run red.
- **The check comes after the last number, and it reads the message too.** On 2026-10-06 a
  check read ACCEPT.md while 27 of 174 measured calls were still to be run again; the final
  numbers went in afterwards, unchecked. A second check right before sending, with the brief
  «recompute the numbers from the raw files, and hold the message to Kjetil against them»,
  found no wrong number and eight other things: the message put a weakness on a test run
  made before the commit, though the raw answers from the live site showed the same; it was
  milder than the document in four places; and one explanation in the document did not add
  up. The message is a document like the others.
- **Give the checker the commit, not your copy.** The same day a README went into a commit
  built on a stale copy from earlier in the session, and 104 lines from three commits fell
  out. The check before the commit did not find it: it was pointed at the same copy. Build
  every changed file on the git object of the parent commit (from a Cowork VM, where git
  must not be run against the mount: `haven-git-workflow`, «Reading a commit from the Cowork
  VM without running git»), and tell the checker to find the base itself.
- **Set a hard time limit, and make the checker watch the clock.** «Aim for about 15
  minutes» ran to 28–45 minutes three times. «TIDEN ER HARD: 12 minutter. Kjør `date -u` når
  du starter og underveis. Når tiden er gått, leverer du det du har, med resten under ‘Ikke
  kontrollert’» held four times out of four (9–13 minutes). Order the brief by importance,
  so what is cut is what matters least.
  On 2026-10-07 a brief with a soft limit («Svar på under ti minutter») and five questions in no
  order took 17 minutes for a short status message. Two briefs the same day that gave the limit
  and the questions to take first took 9 and 8 minutes; one of them also said what the check was
  not («Dette er en kontroll av én side, ikke en gjennomgang av spesifikasjonen. Prioriter
  spørsmål 1, 2 og 4.»). The times are read from the file times of brief and report. They were
  three different tasks, so this is weak evidence.
- **The checker is a model with a quota: have a second one ready, and name the model.** By the
  thread's own log and notes, a document check on 2026-10-06 at about 21:30Z was broken off: the
  subagent on model `fable` («Fabel») answered HTTP 429, weekly limit, until 2026-10-08 10:00Z.
  By the same notes, the updated documents were not written to the task folder until the check
  had run, the next day, with `model: "opus"` on the Agent call. Write in the report, in
  `STATUS.md` and in the message to Kjetil which model read the text, and that it was not the
  usual one.
- **A check holds up the thread that ordered it.** Tool calls in one block run one after
  another, and a call to a subagent holds everything behind it until it returns. Put the
  long queue job in first, then start the check, and say in the brief what that job changes
  in the working tree while the checker reads (on 2026-10-06 a red-run step set one line
  into a source file for two minutes; the brief said so and pointed to the commit).
- **Evidence names what it proves.** A chain step that requires «red first, then green»
  before a commit must require it for the exact files it commits: put the md5 of each file
  in the marker line and match on it. Otherwise a file corrected after the check is
  committed on the old evidence. Example:
  `HAVEN-Deploy/_handoff/HD-0077/mac/strakstiltak-avvik4-20261006.sh`.

The briefs, the build scripts and the templates as they were run:
`HAVEN-Deploy/_handoff/HD-0077/maal/DOKUMENTBYGG-20261004.tar.gz`. The reports:
`HAVEN-Deploy/_handoff/HD-0077/maal/uavhengige/KONTROLL-AKSEPTUTKAST-RAPPORT.md` and
`HAVEN-Deploy/_handoff/HD-0077/maal/uavhengige/KONTROLL-AKSEPT-2-RAPPORT.md`. From
2026-10-06: `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261006/kontroll/` has the fixed
rules for a read-only checker (`REGLER-K1.md`), two short briefs with a hard limit
(`OPPGAVE-K9.md`, `OPPGAVE-K10.md`) and their reports (`K9-FERDIG.md`, `K10-AVVIK4.md`).

### A correction is new text: have it checked, and say which round nobody read (HD-0077, 2026-10-07)

Every check of a correction found errors in the correction: three rounds on one plan (two serious
findings, two serious, then none and three errors), and the same in code, where a fix let a
wait-listed guest take a table after the time had started. So:

- Plan the check of the corrections when the first check is planned, with the before and after
  folders and the diff ready for the checker.
- Stop when the remaining findings are small, and write in the document and in the message to Kjetil
  that the last round has not been read by an independent thread.
- A correction must not point to a file before the file is there. Let the script that writes the
  text require that the report or copy it refers to exists at that path
  (`HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/k3/rett_pdd4_2.py` does).

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

He had to say it a third time on 2026-10-05: «Du må legge med hele banen til filer som
dette: ACCEPT.md». A hand-over message, the questions put to him with AskUserQuestion, and a
reference like «ACCEPT.md §8» had only the file name. The rule holds for **every mention in
every message**, not for the first. Check it mechanically before a message is sent:
`HAVEN-Deploy/_handoff/HD-0077/mac/sjekk-melding-20261005.py <file with the message text>`
flags every word that ends in a file extension and does not start at a root.

The checker sees file extensions only. Two kinds of mention pass it and still break the
rule: a file named by a description («akseptdokumentet», «README-filen for
PalazzoScaffold»), and files delivered as cards in the chat, which show only the base name.
Put the full path beside a description the first time it is used in a message, and list the
full path of every delivered file in the message that goes with it. On 2026-10-06 a G3
request passed the checker with both gaps; they were corrected in the next message.

**A message with several choices gets its own check before it is sent (HD-0077, 2026-10-07).**
The overview that put ten questions to Kjetil after a night's work went out with only the path
checker run on it; the documents behind it had been checked three times. An independent thread
that read the hand-over document half an hour later found four places where the message said too
much or too little, and he got them as corrections. P5 already says the check reads the message
too. What was missing was a brief for it. Give the checker the message, the documents and
`STATUS.md`, and ask:

- **Is the recommended alternative named for every choice?** One choice read «under every answer,
  or only under answers that name a dish», without saying which one the plan recommended.
- **What does a bare yes accept?** «If you only say approved, the recommended choices apply» makes
  every recommendation the message does not name, and every deviation it leaves out, part of his
  yes. List them. If a recommended alternative is narrower than a rule that is live (here: which
  answers carry the allergen line), say so in the message and keep the live rule until he has
  chosen.
- **Does every sentence about what was done when match `STATUS.md`?** «By then I had done what I
  could on the main task» stood against a log that showed the independent checks and three rounds
  of corrections still to come. It was the sentence his decision on a condition rested on.
- **Are summary words held to the standard of the documents?** «The kernel is read» was in the
  message; the plan named the reader and the files (P0).

Report: `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/K9-OVERLEVERING.md`. The
corrections as sent: `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/RETTELSE-MORGENMELDING-20261007.md`.

**Old messages can arrive again.** In a Cowork session on 2026-10-06, two earlier messages
from Kjetil came up again as new ones, word for word, each time the answers to a question
card were read, and once as the opening text of a resumed turn (four times that day). One
was the path rule above, the other a change of direction from the day before. Before you
act on a message that corrects you or changes direction, hold it against his earlier words
in `STATUS.md` and §0. If it is the same text, treat it as the same message, tell him once
that it came again, and go on. On the night to 2026-10-07 the same message arrived three
times as a new turn while he slept; each got its answer, the second and third in short form
with the time of the first.

The correspondence thread saw two forms on 2026-10-07: an older message glued in front of a new
one with no space between them («…manuelle operasjoner.Jeg har godkjent prøveparet»), and the
same older message once more when the answers to two question cards were read. It wrote «Kjetil
sendte meldingen fra 06.10 kl. 10:10Z på nytt» in `STATUS.md` and «gjentok ordrett» in its
memory. It had seen the message arrive, not him send it. Write «the message arrived again», read
the new part as his message, and ask him once.

## A status message between gates (correspondence thread, 2026-10-07)

Kjetil, 2026-10-06, in a task whose purpose was encrypted correspondence with attachments out to
two people: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre. Formålet er å få
ut correnspondence til vegar og victoria, med støtte for vedleg og kryptert kommunikasjon. Hva
gjenstår for å få testet med dem. De har ikke fått noen ny installerer pakke. Og det er altfor
mye manuelle operasjoner.» By the thread's own note from that day, the status he had been given
was about a queue that stood still. Which messages he was answering is not kept word for word.

- **First: where the purpose stands for the people it is for.** The status line on the G1 page
  the day after read «Vegar og Victoria har ikke fått noe nytt, og ingen ny installerer er
  bygget.» When the answer is «nothing yet», that is the first sentence.
- **Then what he must do, numbered, and no more points than there are things to do.** Each is an
  act he can carry out from the message alone: the full path of the file, the address, the
  deadline.
- **Then what remains before the purpose is met,** as the links in order and who has each, not
  as a log of what was done. A figure of the links helps.
- **Work on a side track is called a side track,** in a line or two. Here an old channel had to
  be kept alive while the new one is built.
- **A decision is put as a question card (AskUserQuestion) with two or three plain
  alternatives, or as numbered questions.** By the thread's own note, a choice written into a
  long message on 2026-10-06 (where the owner's keys should lie) was not answered in his next
  message, which answered a later request sent the same evening. Put as a card the day after,
  with one other, both were answered. Five numbered points sent later that day got a reply
  number by number: two approvals, two questions back, and under the fifth number his direction
  on another matter on the page (by the thread's own note of the times, within the hour). These
  are single observations, not a comparison.
- **A question uses his words, and says what a thing does before asking about it.** Two of those
  five came back as questions: «Hva gjør assistentidentiteten?», and «Hva mener du med at vedlegg
  kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.» The first had named
  a thing, «en delegert assistentidentitet», without saying what it does. The second had said
  «vedlegg» and `main`; by the author's account it meant the code that handles attachments, and
  the main branch. The check before sending read an earlier draft with four questions and was
  asked six things; none was whether he could answer the questions without the repo's
  vocabulary. The page was changed after the check, and the changes were not checked again. Ask
  the checker that question, on the page as it will be sent.
- **A request with a deadline says what follows when the deadline passes, and names every later
  step that is his.** A draft asked him to approve two access requests within 24 hours. It left
  out that the invitation is then spent and a new one is needed, which by the checker's reading
  meant a new swap on the host and a new restart of staging. It also left out the step after:
  his approval of the two recipients' own requests, each within 24 hours. The check before
  sending found both:
  `Deliverables/PDD_korrespondanse-fornyelse_2026-09-30/panel/FABEL_BYTTEMELDING.md`.
- **No message when nothing has changed for him.**

## Completion checklist

- [ ] §0 verbatim intent, all claims audited with status
- [ ] Every leaf purpose has goal (outcome, signals, verifier) and a §5 test
- [ ] Lessons from `lookup` quoted in §4 and reflected in §2/§5
- [ ] §3 expectation contract filled; GUI rows point at approved `images/` files
- [ ] STATUS.md gates set only by Kjetil's word; `validate` is clean
- [ ] Every gate request to Kjetil names the **absolute path** of the document he is being asked to approve
- [ ] TESTRESULT.md has real output for every §5 row (or `blocked` + reason)
- [ ] ACCEPT.md pairs expected/actual for every §3 row
- [ ] ACCEPT.md and TESTRESULT.md are built from the evidence files and were checked by an
      independent thread; every question Kjetil is asked to try was measured on the running service
- [ ] The independent check came after the last number was filled in, and it read the message
      that goes to Kjetil; every file in that message has its full path, also files sent as cards
- [ ] A message that puts choices to Kjetil was read by an independent thread before it was sent: the
      recommended alternative is named for each choice, and what a bare yes would accept is listed
- [ ] A status message opens with where the purpose stands for the people it is for, then his
      numbered actions, each with its deadline and what follows when it passes
- [ ] Where «few steps» is a purpose, the handgrips are counted per party, the owner included,
      from the images
- [ ] Every question to Kjetil uses his words and says what a thing does before asking about it
- [ ] §2 has a measured row for every step before the one being changed
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

