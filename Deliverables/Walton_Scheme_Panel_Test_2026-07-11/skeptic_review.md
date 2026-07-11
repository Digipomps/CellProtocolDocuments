# Skeptic Review — Do Walton schemes earn their keep on the hosted-only case?

Adviser B (skeptic). Date: 2026-07-10.

Feature under test: `haven.claim-scheme.v0` (`ClaimScheme.swift`,
`ClaimSchemeInstance.swift`, Book 29 §6). Schemes name the Walton inferential
pattern a claim uses and attach a fixed catalog of *critical questions* (CQs).
Unexamined CQ → deduced subtask (`deducedSubtasks()`); challenged CQ →
undercutting defeater (`undercutCounters()` → Pollock undercut in §4 evaluation).

## The real question I was asked to test

Not "are Walton schemes good in general" — they are a respectable tool. The
question is narrower and harder: **on THIS case, do the critical questions
surface anything the plain baseline did not already find on its own?** The two
baselines (wa, wb) reached a strong, correct-looking result *without* schemes:
both contradicted premise 1 (local-too-weak) and premise 3 (gdpr-eu-region) as
stated, flagged premise 2 (hosted-cheaper-tco) as unaudited/source_missing, and
both spontaneously produced the hybrid alternative as the deciding rebuttal.
Given the prior benchmark finding that the plain method is *fully reproducible by
a capable model with repo access*, the burden is on the schemes to show they
generate insight rather than reformat insight the model already produced.

Classification I use per CQ:

- **REDUNDANT** — the baseline already found this substance unaided.
- **CEREMONY** — technically a legitimate question, but adds no decision-relevant
  traction on this case (the answer is trivial, N/A, or immaterial to the verdict).
- **GENUINE-ADD** — a real gap at least one baseline missed that the CQ reliably catches.

## Scheme → claim mapping

I attach the most natural Walton scheme to each node, and note alternates that
yield the same coverage (so I am not cherry-picking a scheme that happens to be
redundant).

| Node | Primary scheme | Alternate(s) with equivalent CQ coverage |
| --- | --- | --- |
| Root: "drop local, use hosted-only" | practical-reasoning | positive-consequences (via premise 2) |
| P1 local-too-weak | example (benchmarks → general capability) | sign (score as sign of weakness) |
| P2 hosted-cheaper-tco | positive-consequences | (statistical claim; same CQs) |
| P3 gdpr-eu-region | verbal-classification ("EU region" ⇒ "GDPR-compliant") | cause-to-effect (choose region → GDPR solved) |

---

## Root proposal — practical-reasoning CQs

| CQ | Question | Class | Reasoning |
| --- | --- | --- | --- |
| `alternatives` | Are there alternative actions that reach the goal? | **REDUNDANT** | Both baselines produced the hybrid/5-lane ladder *unprompted* and made it the deciding rebuttal (`claim.mixed-lane-better`, `claim.counter.diversity-is-panel-value`, wa's "narrowed variant"). The CQ asks for exactly what the baseline already delivered as its central move. |
| `efficiency` | Is the proposed action the best/most efficient means? | **REDUNDANT** | The baseline's whole adjudication *is* an efficiency comparison: equal quality band (P1), unquantified cost (P2), plus lost fallback. It concluded hosted-only is not shown to be the best means. |
| `side-effects` | Side effects or conflict with other goals? | **REDUNDANT** | Baseline surfaced both: loss of offline fallback + determinism (`local-lane-is-fallback-and-determinism`) and conflict with the privacy goal (data-class egress). These *are* the side-effects/goal-conflicts. |
| `feasibility` | Is the action actually possible to carry out? | **REDUNDANT** (marginal structural sharpening) | wa's `data-class-boundary-forbids-egress` already found hosted-only *cannot* process several data classes at all — a feasibility hard-stop. Content is covered. The only thing the scheme adds is *filing* it as a feasibility defeater on the action rather than an undercut on completeness — a cleaner classification, not new content. |

All four practical-reasoning CQs reproduced by the baseline. This is the single
most damaging result for the feature: on the root claim — the one that matters
most — the capable model asked and answered the entire Walton checklist unaided.

## P1 local-too-weak — example (and sign) CQs

| CQ | Question | Class | Reasoning |
| --- | --- | --- | --- |
| `example.instance` | Is the example actually an instance of the generalization? | **REDUNDANT** | Both baselines' central refutation: the CoPilot daily-speech / JSON-mode benchmark is an *adjacent task, not claim-extraction*. This CQ = the baseline's headline finding on P1. |
| `example.representative` | Is the example typical, not exceptional? | **REDUNDANT** | wb S4 explicitly flags the 8-case co-pilot set as unrepresentative of high-stakes claim-extraction and deduces "extend the benchmark." That is the representativeness question, already deduced as a subtask. |
| `example.counterexamples` | Are there counterexamples to the generalization? | **REDUNDANT** | The counterexample *is* the baseline's kill shot: hosted small models score in the *same 73–89% band*, so weakness tracks model **size**, not local-vs-hosted. Both baselines lead with this. |
| `sign.reliability` (alt) | Is the sign a reliable indicator? | **REDUNDANT** | Same as `example.instance` — is a daily-speech score a reliable sign of claim-extraction capability? Baseline says no. |
| `sign.alternatives` (alt) | Could other events account for the sign? | **REDUNDANT** | "Model size, not lane, explains the low scores" — exactly the baseline's alternative explanation. |

No add. Whether you model P1 as example or as sign, every CQ maps onto something
the baseline already stated, usually as its *primary* argument.

## P2 hosted-cheaper-tco — positive-consequences CQs

| CQ | Question | Class | Reasoning |
| --- | --- | --- | --- |
| `likelihood` | How likely are the cited positive consequences? | **REDUNDANT** | Baseline: "cheaper" is volume-dependent with an unstated break-even; direction unknown. That is a likelihood judgment already made. |
| `evidence` | Is there evidence the consequences follow? | **REDUNDANT** | Baseline states flatly "no TCO model exists" (`source_missing` / `needs_external_source_audit`) and deduces the TCO subtask. This CQ = that finding verbatim. |
| `counterbalance` | Negative consequences that outweigh them? | **GENUINE-ADD** (low decision-weight) | Baselines counterbalance with lost fallback and "near-zero maintenance savings if local is kept for on-device anyway." But **neither names the commercial-dependency counterbalance**: once the local lane is eliminated you are a captive buyer, exposed to provider price increases, model deprecation, and ToS/retention changes over time. That directly bears on P2's own claim — a TCO that ignores the pricing-power risk of eliminating your outside option is incomplete. This is the one CQ that reliably drags out a real gap both baselines left implicit. See "Concessions" below. |

## P3 gdpr-eu-region — verbal-classification (and cause-to-effect) CQs

| CQ | Question | Class | Reasoning |
| --- | --- | --- | --- |
| `property` | Does the thing actually have the classifying property? | **REDUNDANT** | Baseline: EU region is *necessary-not-sufficient* — it does not carry the property "GDPR-compliant." Precisely this CQ. |
| `definition` | Is the classification based on a precise, non-vague definition? | **REDUNDANT** | wa *decomposed the vague term itself*: "'GDPR' is not one thing — legal basis, DPA, subprocessor chain, retention (30-day/ZDR), transfer, special-category data each need separate handling." That is the definition CQ, answered in more detail than the CQ asks. |
| `cause-to-effect.causal-law` (alt) | General causal link cause→effect? | **REDUNDANT** | "Region alone does not cause compliance" — stated. |
| `cause-to-effect.strength` (alt) | Strong link or mere correlation? | **REDUNDANT** | "Necessary-not-sufficient / partly true for synthetic/public only" — a strength judgment already made. |
| `cause-to-effect.interference` (alt) | Intervening factors that block the effect? | **REDUNDANT** | Baseline enumerates the intervenors: retention, subprocessors, DPA execution, data-class egress, special-category data. |

No add. P3 is the case where the baseline was *most* thorough, so the schemes are
most redundant here.

---

## Tally

| Class | Count | Notes |
| --- | --- | --- |
| REDUNDANT | 15 of 16 applicable CQs | Includes all 4 root practical-reasoning CQs and all P1/P3 CQs under either scheme choice. |
| CEREMONY | 0 pure | None were *empty* on this case — every applicable CQ was answerable — but that cuts against the feature: the model answered them without the scaffold. |
| GENUINE-ADD | 1 (`positive-consequences.counterbalance` on P2) | Real content gap (commercial lock-in / pricing-power exposure), but low decision-weight: the root is already contradicted on stronger grounds. |

## Concessions (being honest about where value exists)

1. **One genuine content add.** `positive-consequences.counterbalance` reliably
   pulls out the vendor-lock-in / pricing-power / model-deprecation risk of
   eliminating the local outside option — a real hole in both baselines, and one
   that actually sharpens the P2 (cost) audit rather than being decorative. I
   concede this as a true GENUINE-ADD. Caveat: it *strengthens the case against*
   hosted-only, so it changes the reasoning's completeness, not the verdict; and
   a capable model would plausibly have produced it too — the baselines simply
   didn't this run.

2. **A structural sharpening, not new content.** The practical-reasoning
   `feasibility` lens correctly reclassifies the data-class hard-stop as "the
   action is partly impossible" rather than "the support is weakly undercut."
   That is a cleaner argument shape (and a legitimately stronger point than the
   unaudited premises), but the substance was already in wa's ledger.

3. **Process value that is real but conditional.** The catalog is a fixed,
   deterministic checklist; the challenged-CQ → undercut bridge is a correct
   Pollock mapping; `deducedSubtasks()` and `undercutCounters()` route answers
   straight into §4 evaluation. This gives **coverage guarantees, cross-run
   determinism, and an auditable trail** — every run demonstrably asks the same
   questions. That value is real for weaker models, rushed/adversarial runs, or
   many-claim batches where hand-wiring undercuts does not scale. It is **not**
   an insight value on this run: a capable model with repo access already
   reproduced the content, so here the scaffold certifies coverage the model
   would have achieved anyway.

## Costs the schemes carry (the skeptic's ledger)

- **Authoring overhead is non-trivial and manual.** Book 29 §7 is explicit:
  scheme instances are *authored, not auto-detected*. This case needs ~4–5
  instances (root + 3 premises, plus an alternate for P1/P3), each carrying 2–6
  CQ states — roughly 18–24 statuses to set by hand. That is labor spent
  re-encoding conclusions the analyst already reached in prose.

- **False-precision risk in `completeness`.** `ClaimSchemeEvaluation.completeness`
  is a `Double` (answered/applicable). Book 29 §6 promises "no false precision,"
  but a "6/6 answered = 1.0" figure is exactly the kind of number that gets
  read downstream as *measured argument quality* when it is only bookkeeping over
  hand-set statuses. The metric looks earned; it is asserted.

- **Subtask over-proliferation is the default failure mode.** `unexamined` is the
  default on instantiation, and `deducedSubtasks()` emits *every* unexamined CQ.
  Naively instantiating the four schemes yields ~18–24 work items — versus the
  baseline's 3–4 real subtasks (S1 bench, S2/S3 cost+GDPR, S4 adjudicate). Most
  of the 18–24 are questions the model can answer immediately from the repo. Used
  naively the scheme *buries* the 3–4 decision-critical subtasks under a pile of
  already-answerable ones — worse signal-to-noise than the plain method. (The
  proliferation only shrinks back to S1–S3 if the analyst first hand-sets most
  CQs to `answered`/`not-applicable` — i.e. does the plain analysis first, then
  transcribes it. The scaffold rides on the plain work; it does not replace it.)

## Verdict

**On this case, the schemes do not earn their keep as an analysis engine.** 15 of
16 applicable critical questions are REDUNDANT — the plain baseline reproduced
them unaided, frequently as its *headline* arguments (adjacent-task, same-band
counterexample, necessary-not-sufficient, no-TCO-model, hybrid alternative). The
single genuine content add (lock-in/pricing-power under P2 counterbalance) does
not move the already-contradicted verdict. Against that thin marginal insight sit
real costs: manual authoring of ~20 CQ states, a completeness ratio that invites
false precision, and a default subtask-explosion that degrades signal unless the
plain analysis is done first anyway. This case is close to the worst case for the
feature precisely because the analyst is a capable model on a well-documented
proposal — exactly the regime where the plain method was already shown fully
reproducible.

**Where schemes *would* earn their keep** (and where I would not object):

- Weaker analyst models, or humans under time pressure, where the fixed checklist
  prevents omission the capable model avoids by having strong priors.
- Novel/unfamiliar argument types where the model lacks priors and the catalog
  supplies the questions it would not think to ask.
- Governance / defensibility: when you must *demonstrate* the standard questions
  were asked (audit, dispute, regulator), not merely that they happened to be.
- Cross-run consistency and many-claim batches where the challenged→undercut
  bridge scales and hand-wiring defeaters does not.

**Recommendation to the panel:** treat schemes as an *optional audit/consistency
layer*, not as the analytic method, and gate their cost. Concretely: (a) do not
instantiate schemes on claims a capable analyst has already fully adjudicated —
require them only where a CQ is expected to be *challenged* or genuinely
*unexamined*; (b) suppress `completeness` from any surface that could read as a
quality score; (c) require CQs to be triaged to `answered`/`not-applicable`
*before* `deducedSubtasks()` runs, so the loop never emits already-answerable
work. Under those guards the feature keeps its real strengths (coverage
guarantee, Pollock-correct undercut bridge, cross-run determinism) without
charging the panel ceremony on cases the plain method already handles.
