# Fractal Dimension As A Content-Blind Measure Of Graph Data Value

Date: 2026-07-04

Status: advisory panel deliverable, not a normative CellProtocol contract.
Not implementation. The recommended metric suite is a proposal until Kjetil
approves it and it is implemented as reviewed code. Literature references
marked "verified 2026-07-04" were checked against external sources on that
date; other references are standard literature reported by panelists and
were not independently re-verified in this round.

Panel roles used: network-science rigor reviewer, independent methodological
critic, measurement-theory advisor, contrarian red team, data-economics
advisor. Human decision owner: Kjetil.

Raw panel artifact:
`Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json`

## Kortversjon (norsk)

Hypotesen var at fraktal dimensjon kan brukes som et generelt, innholdsblindt
mål på nåværende og potensiell verdi av grafstrukturerte data (celler, formål,
argumenter) — til bruk ved datasettutveksling, som vekstmål for formål, og som
mål på HAVENs samlede verdi.

Et panel på fem uavhengige modeller (GPT-5.5, GLM-5.2, Gemini 3.1 Pro,
DeepSeek V4 Pro, Kimi K2.6 via NanoGPT) var **enstemmig**: fraktal dimensjon
bør ikke brukes som hovedmetrikk. Tre uavhengige grunner, hver alene
diskvalifiserende:

1. **Ikke estimerbar på HAVEN-skala.** Småverden-grafer med diameter 5–15 gir
   3–5 brukbare boksstørrelser; en pålitelig potenslov-tilpasning krever
   størrelsesordener mer. Under ~10⁵ noder og diameter ~15–20 er estimatet
   støy. Småverden-egenskapen står dessuten i direkte konflikt med fraktal
   skalering (Csányi & Szendrői 2004).
2. **Måler feil ting.** Fraktal dimensjon fanger topologisk selvlikhet og
   hierarkisk modularitet — ikke informasjonsinnhold, nytte eller verdi. En
   fraktal graf kan være verdiløs; en ikke-fraktal graf kan være uvurderlig.
   Kategorifeil som verdimål.
3. **Trivielt gambar.** Syntetiske kjeder og trær blåser opp estimatet uten å
   tilføre verdi.

Men intuisjonen bak forslaget står seg delvis: innholdsblind struktur bærer
reell signalverdi når den brukes som en **profil av flere metrikker**, ikke én
skalar. Panelet konvergerte på samme alternative suite: bruksvektede metrikker
fra FlowElements (nåværende verdi), åpne triader/strukturelle hull/randvekst
(potensiell verdi), spektral entropi og MDL-kompresjon (kompleksitet), alt
normalisert mot typede nullmodeller. HAVEN er uvanlig godt posisjonert for den
forsvarlige varianten: FlowElements gir bruksvekting og identitetslaget gir
proveniensvekting — begge er antifusk-kravene som gjør slike mål robuste.

Anbefaling: avvis fraktal dimensjon som hovedmetrikk; vedta i stedet en
"Structural Value Profile" (fem pilarer, se §7) som verdimåls-retning, med
fraktal dimensjon kun som eksperimentell diagnostikk bak strenge porter.

## 1. Formål

| # | purposeRef | Goal | Status |
|---|---|---|---|
| F1 | `purpose://value-and-commons` (candidate root node, Book 23) | `goal.value-metrics.adjudicate-fractal-hypothesis`: all root claims in the ledger reach a terminal adjudication (supported/contradicted) grounded in panel evidence and audited sources, within the 2026-07-04 panel round | satisfied |
| F2 | `purpose://project-work.work-items` | `goal.value-metrics.deliverable-in-corpus`: this report exists in `Deliverables/`, is registered in the model-knowledge corpus manifest, and is committed to the primary GitHub remote | satisfied (commit is the final step of this round) |
| F3 | `purpose://scaffold.operations` (candidate node, Book 23) | `goal.advisory-panel.reusable-runner`: a reusable panel runner exists and completed with ≥4/5 panelists responding | satisfied (5/5, runner at `Tools/ModelKnowledge/run_advisory_panel.py`) |

Candidate purpose intake: a child node `purpose://value-and-commons.structural-value-metrics`
("measure the value of graph-structured data without inspecting content") does
not exist in the Book 23 taxonomy and is recorded here as a candidate, not
used as a live ref.

## 2. Hypothesis Under Evaluation

Owner's proposal (translated from Norwegian; original in the session that
produced this report):

> It would be practical to have a general unit of measure for the potential
> value of data. If the data is graph-structured — as in Cells, purposes, or
> arguments in HAVEN/CellProtocol — fractal dimension could be used to say
> something about the possible value of the data, preferably both current and
> potential value, without knowing anything about the content. Useful when
> exchanging datasets (relative value/complexity), for measuring growth (e.g.
> a purpose whose goal is increasing value), and for saying something about
> HAVEN's value and how it grows.

## 3. Scientific Background

### 3.1 Fractal dimension on networks

The canonical definition is the box-covering dimension of Song, Havlin &
Makse: a network is fractal if the minimum number of boxes `N_B` of graph
diameter `l_B` needed to cover it scales as `N_B(l_B) ~ l_B^(-d_B)` over a
meaningful range of scales (Song, Havlin & Makse 2005, Nature 433:392–395 —
verified 2026-07-04). The alternative cluster-growing dimension measures how
node mass grows with topological radius.

Estimation requirements that matter here:

- A power-law fit needs many distinct usable box sizes — in practice roughly
  6–10 usable radii and ideally more than one order of magnitude of scale.
- Minimum box covering is NP-hard; practical greedy/coloring heuristics
  (Song, Gallos, Havlin & Makse 2007) introduce estimator variance.
- Small-world networks exhibit exponential neighborhood growth, which is in
  direct conflict with power-law (fractal) scaling. Csányi & Szendrői
  demonstrated this dichotomy empirically: most non-geographic real-world
  networks are small-world and not fractal (Phys. Rev. E 70:016122, 2004 —
  verified 2026-07-04).

### 3.2 HAVEN graph character

HAVEN/CellProtocol graphs (cell reference graphs, purpose trees with
cross-links, argument graphs) are typed property graphs / multigraphs at
realistic scales of 10²–10⁴ nodes per domain, with small diameters. Every
mutation is a replayable flow event, so usage traces exist by construction —
a fact that turns out to carry most of the defensible value signal.

## 4. Panel Setup And Method

One shared written brief (context, proposal, seven fixed questions Q1–Q7,
format constraints, explicit anti-flattery instruction) was fanned out to five
models through the NanoGPT OpenAI-compatible API, each with a distinct system
role. Single round, independent answers, no cross-talk between panelists.
Temperature 0.2, max 8000 tokens. The brief and all responses are preserved
verbatim in the raw artifact (path in the header); the brief is also stored at
`Tools/ModelKnowledge/panels/fractal_dimension_value_2026-07-04.json`.

| Panelist | Model ID | Role | Result |
|---|---|---|---|
| GPT-5.5 | `openai/gpt-5.5` | network-science and fractal-geometry rigor | ok, 91.0 s |
| GLM-5.2 | `zai-org/glm-5.2:thinking` | independent methodological critic | ok, 49.6 s |
| Gemini 3.1 Pro | `google/gemini-3.1-pro-preview` | measurement theory and operationalization | ok, 33.9 s |
| DeepSeek V4 Pro | `deepseek/deepseek-v4-pro:thinking` | contrarian red team | ok, 49.7 s |
| Kimi K2.6 | `moonshotai/kimi-k2.6:thinking` | data economics and valuation | ok, 25.7 s |

Reproduction:

```bash
NANOGPT_API_KEY=... python3 Tools/ModelKnowledge/run_advisory_panel.py \
  --provider nanogpt \
  --spec Tools/ModelKnowledge/panels/fractal_dimension_value_2026-07-04.json
```

## 5. Panel Findings

### Q1 Estimability — unanimous: not estimable at HAVEN scale

All five panelists independently concluded that box-covering and
cluster-growing dimension cannot be reliably estimated on small-world graphs
of 10²–10⁴ nodes. Convergent quantitative thresholds: diameters of 5–15 yield
only ~3–5 usable box sizes; a trustworthy estimate needs roughly N ≳ 10⁵ and
diameter ≳ 15–30 with a demonstrated scaling plateau. GPT-5.5: below diameter
~15 the estimates are "mostly decorative". GLM-5.2: "At HAVEN's current
scale, the metric is noise."

### Q2 Meaning — unanimous: no link between fractal dimension and value

Fractal dimension, where defined, captures topological self-similarity,
hierarchical modularity and hub-repulsion (disassortativity). No panelist
could identify a theoretical or empirical link to data value, information
content or usefulness; two called the proposal a category error. Gemini added
the sharpest structural point: highly integrated, cross-referenced datasets —
exactly what HAVEN wants — are typically small-world and therefore
*non-fractal*; a high fractal dimension would, if anything, indicate the
opposite of the integration HAVEN values.

### Q3 Current vs potential value — unanimous split into usage vs structure

Pure structure cannot separate current from potential value ("an unread
encyclopedia has the same structure as a heavily read one" — Gemini). With
usage traces the split becomes operational:

- **Current value (realized):** recency-decayed distinct-actor traversal
  counts, flow entropy over traversal paths, usage-weighted PageRank, count
  of workflows/decisions depending on nodes.
- **Potential value (option):** open triads / unclosed wedges, structural
  holes and brokerage positions (Burt 1992), boundary/periphery growth rate,
  typed-path diversity, novelty (MDL residual) against a typed null model.

All panelists flagged these as proxies for affordances, not value itself.
Kimi grounded the limit in the data-economics literature: true potential
value is task-dependent and ultimately needs marginal-contribution valuation
(Data Shapley — Ghorbani & Zou, ICML 2019 — verified 2026-07-04).

### Q4 Alternatives — convergent ranking

Aggregated ranking across the five panelists (agreement was strong):

1. **Usage/provenance-weighted reuse metrics** — closest to revealed
   preference; content-blind but behavior-aware.
2. **Von Neumann / spectral graph entropy** — normalized-Laplacian eigenvalue
   entropy (Braunstein, Ghosh & Severini density-matrix construction;
   Passerini & Severini 2008 — verified 2026-07-04); information-theoretic
   grounding, computable at 10⁴ nodes, normalizable by log N.
3. **Compressibility / MDL** — nontrivial structure beyond a typed null
   model; penalizes arbitrary inflation.
4. **Typed motif / graphlet diversity** — for argument graphs the typed
   motifs (claim–evidence–objection patterns) are the actual atomic units of
   value (Milo et al. 2002).
5. **Component/reachability structure, brokerage metrics** — navigability and
   integration.
6. **Degree heterogeneity** — cheap but ambiguous and easy to game.
7. **Network-value laws** — Metcalfe n² overstates; Odlyzko & Tilly's n log n
   is the defensible baseline (verified 2026-07-04, including the documented
   counterpoint literature arguing Metcalfe fits some platform data).
8. **Fractal / spectral dimension** — last in every panelist's ranking.

### Q5 Goodhart/gaming — unanimous: any priced structural metric will be gamed

Attack vectors named independently by multiple panelists: synthetic
node/edge minting, chain/tree appendages tuned to inflate the rewarded
statistic, motif stuffing, Sybil usage bots, duplicate subgraphs. Defenses
converged on: provenance weighting through bound identities, usage weighting
(structure that is never traversed counts ~0), cost anchoring for mutations,
time decay, deduplication, anomaly detection against typed null models, and
never letting a single metric dominate. DeepSeek noted these defenses "align
with HAVEN's permissioned, event-sourced design."

### Q6 Concrete suites — convergent three-to-five-pillar profiles

All five proposed near-identical suites; §7 merges them.

### Q7 Verdict — unanimous no

Five of five: do not adopt fractal dimension as a headline value metric. Two
panelists allowed a residual role as an experimental topology diagnostic once
graphs exceed ~10⁵ nodes with diameter ≳ 15–20, reported with confidence
intervals and an explicit "not estimable" outcome otherwise.

## 6. Claim Ledger And Adjudication

Claim structures follow `haven.claim-definition.v0` (Book 29); evaluation
follows the Book 29 semantics (conservative score policy). Support records
cite the raw panel artifact and the sources verified 2026-07-04.

```json
{
  "schema": "haven.claim-definition.v0",
  "claims": [
    {
      "claimID": "claim.fractal.estimable",
      "statement": "Fractal dimension is reliably estimable on HAVEN-scale graphs (10^2-10^4 nodes, small-world).",
      "claimType": "statistical",
      "strength": "speculative",
      "isInferred": true,
      "purposeRef": "purpose://value-and-commons",
      "supports": [
        {"kind": "counterargument", "statement": "Small-world diameter 5-15 yields only 3-5 usable box sizes; power-law fit unidentifiable; box covering NP-hard with heuristic variance; small-world growth is exponential, not fractal (Csanyi & Szendroi 2004; Song-Havlin-Makse 2005; 5/5 panelists).", "sourceRefs": ["Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json"], "sourceAuditStatus": "supported", "confidence": 0.95}
      ]
    },
    {
      "claimID": "claim.fractal.value-link",
      "statement": "Fractal dimension indicates the current or potential value of the underlying data.",
      "claimType": "causal",
      "strength": "speculative",
      "isInferred": true,
      "purposeRef": "purpose://value-and-commons",
      "supports": [
        {"kind": "counterargument", "statement": "Fractal dimension measures topological self-similarity, not information content or usefulness; no theoretical or empirical link found; integrated datasets are typically non-fractal (5/5 panelists).", "sourceRefs": ["Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json"], "sourceAuditStatus": "supported", "confidence": 0.9}
      ]
    },
    {
      "claimID": "claim.fractal.headline-metric",
      "statement": "HAVEN should adopt fractal dimension as a headline content-blind value metric.",
      "claimType": "normative",
      "strength": "moderated",
      "isInferred": false,
      "purposeRef": "purpose://value-and-commons",
      "composition": {
        "type": "countered",
        "base": {
          "type": "allOf",
          "children": [
            {"type": "claim", "claimRef": "claim.fractal.estimable"},
            {"type": "claim", "claimRef": "claim.fractal.value-link"}
          ]
        },
        "counters": [
          {"role": "rebuts", "composition": {"type": "claim", "claimRef": "claim.panel.unanimous-rejection"}}
        ]
      }
    },
    {
      "claimID": "claim.panel.unanimous-rejection",
      "statement": "Five independent expert-role models unanimously recommend against fractal dimension as a headline value metric, on estimability, construct-validity and gaming grounds.",
      "claimType": "factual",
      "strength": "assertive",
      "isInferred": false,
      "supports": [
        {"kind": "evidence", "statement": "All five Q7 verdicts answer no.", "sourceRefs": ["Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json"], "sourceAuditStatus": "supported", "confidence": 1.0}
      ]
    },
    {
      "claimID": "claim.structure.partial-signal",
      "statement": "A content-blind structural metric PROFILE (usage-weighted, entropy/MDL-based, null-model-normalized) provides a defensible partial signal of dataset complexity and value trajectory.",
      "claimType": "predictive",
      "strength": "moderated",
      "isInferred": false,
      "purposeRef": "purpose://value-and-commons",
      "supports": [
        {"kind": "evidence", "statement": "Convergent Q4/Q6 suites across all panelists; established literature for each component (BGS entropy, MDL, motifs, structural holes).", "sourceRefs": ["Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json"], "sourceAuditStatus": "supported", "confidence": 0.8},
        {"kind": "qualifier", "statement": "Proxies estimate affordances, not value; task-dependent value needs marginal-contribution methods (Data Shapley).", "sourceRefs": ["https://proceedings.mlr.press/v97/ghorbani19c.html"], "sourceAuditStatus": "supported", "confidence": 0.9}
      ]
    },
    {
      "claimID": "claim.metric.will-be-gamed",
      "statement": "Any structural metric that influences pricing or purpose success will be gamed unless provenance-, usage- and cost-anchored.",
      "claimType": "predictive",
      "strength": "assertive",
      "isInferred": false,
      "supports": [
        {"kind": "evidence", "statement": "Unanimous Q5 findings with concrete attack vectors; Goodhart dynamics.", "sourceRefs": ["Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json"], "sourceAuditStatus": "supported", "confidence": 0.95}
      ]
    }
  ]
}
```

Adjudication (Book 29 semantics, conservative policy):

| Root claim | Evaluation | Reasoning |
|---|---|---|
| `claim.fractal.estimable` | **contradicted** | Dominant counterevidence, no support survives |
| `claim.fractal.value-link` | **contradicted** | Dominant counterevidence, no support survives |
| `claim.fractal.headline-metric` | **contradicted** | Base `allOf` collapses (contradicted premises make the base unsupported); the `rebuts` counter (`claim.panel.unanimous-rejection`, supported at 1.0) dominates zero base support → `rebuttalDominates` |
| `claim.structure.partial-signal` | **supported (moderated)** | Convergent panel evidence + verified literature; qualifier attached |
| `claim.metric.will-be-gamed` | **supported** | Unanimous, mechanism-level evidence |

Every root claim is terminally adjudicated; goal G1 is satisfied.

## 7. Recommendation: HAVEN Structural Value Profile (proposal)

Replace the single-scalar ambition with a five-pillar profile per dataset /
purpose graph / domain. All pillars are content-blind; none requires reading
node content. Names below are working names, not implemented capabilities.

1. **Scale and health.** N, E, active fractions, component structure and
   giant-component share, effective diameter, typed edge density, dangling
   references. Baseline context for everything else.
2. **Current value (realized).** From FlowElements: recency-decayed
   distinct-actor traversal counts, flow entropy over traversal paths,
   usage-weighted PageRank, dependent-workflow counts. HAVEN's event-sourced
   design makes this pillar native.
3. **Potential value (option).** Open-triad ratio and closure rate,
   structural-hole/brokerage scores, boundary growth toward new
   domains/purposes/types, typed-path diversity, MDL novelty residual versus
   a typed configuration-model null.
4. **Complexity.** Von Neumann spectral entropy normalized by log N, typed
   3-node motif entropy, MDL compression ratio — each reported as a z-score
   against typed null models preserving N, E, degree sequence and type
   distribution.
5. **Fractal diagnostic (optional, gated).** Only on projections with ≥6–10
   usable radii and diameter ≳ 15–20; multiple box-covering heuristics;
   power-law vs exponential model comparison by AIC/BIC; bootstrap
   confidence intervals; explicit "not estimable" outcome otherwise. Never
   in pricing or purpose-success logic.

Cross-dataset comparison: report per-node/per-edge rates, log-N-normalized
entropies, and null-model z-scores — never raw counts. Growth measurement:
snapshot the profile on a fixed cadence, track deltas and z-scores against a
rolling baseline; a purpose with an "increase value" goal binds its
`GoalDefinition` to profile deltas, not to any single scalar.

Anti-Goodhart requirements (mandatory before any pricing/success use):
provenance weighting through HAVEN's bound identities, usage weighting so
untraversed structure counts ~0, cost anchoring on mutations, time decay,
deduplication, anomaly detection against nulls, ensemble reporting. These are
exactly the properties HAVEN's identity and flow layers already provide,
which is the strongest finding of the round: **HAVEN is structurally better
positioned than generic platforms to run a defensible version of this
metric** — but only for the suite, not for fractal dimension.

Boundary (claim safety): none of this prices people, ranks persons, or
creates a global score; profiles are domain-scoped and describe datasets.
Public claims like "HAVEN's value grows superlinearly" must go through
`haven-claim-review` and should default to Odlyzko's n log n framing, not
Metcalfe's n².

### Intended-use verdicts

- **(a) Dataset exchange:** the profile works as a comparability "nutrition
  label" (scale, complexity, realized use, option structure), not as a price.
  Pricing needs task anchoring or marginal-contribution evaluation.
- **(b) Purpose growth goals:** workable now via profile deltas with
  null-model z-scores; goal-definition compatible.
- **(c) HAVEN network value:** track profile trajectories protocol-wide;
  claim growth in trends, never in single-scalar headlines.

## 8. Limitations Of This Round

- Single-round panel, no deliberation or rebuttal phase; unanimity may
  partly reflect shared training-data priors (correlated errors), though the
  independently verified literature carries the load-bearing points.
- Literature audit covered the five load-bearing citation clusters only;
  other citations are as reported by panelists.
- No empirical experiment was run on actual HAVEN graphs; the estimability
  conclusion follows from theory and scale arithmetic, not from measurement
  on HAVEN data.
- Panel responses are model outputs, not human peer review.

## 9. Decision Log And Open Items

Decisions recorded (panel recommends; Kjetil decides):

1. Reject fractal dimension as headline value metric — adjudicated
   `contradicted`; recommendation unanimous.
2. Adopt the Structural Value Profile direction (§7) as the working
   hypothesis for content-blind value measurement — pending Kjetil's
   sign-off.

Open items:

- [ ] Kjetil: approve/reject the Structural Value Profile direction.
- [ ] Candidate purpose intake: `purpose://value-and-commons.structural-value-metrics`.
- [ ] Empirical calibration: compute pillars 1–4 on 2–3 real HAVEN graphs
      (e.g. a purpose tree, an argument graph, a conference cell graph) and
      inspect stability before any goal binds to them. Requires approval as
      new tooling/cell work (native-cell rule applies to any runtime cell).
- [ ] Revisit the fractal diagnostic if/when protocol-wide graphs exceed
      ~10⁵ nodes with diameter ≳ 15–20.
- [ ] Decide whether profile snapshots should become FlowElement-visible
      audit events (aligns with Model_Toolbox_Advisory audit-event pattern).

## 10. References

Verified against external sources 2026-07-04:

- Song, C., Havlin, S. & Makse, H.A. (2005). Self-similarity of complex
  networks. *Nature* 433, 392–395.
- Csányi, G. & Szendrői, B. (2004). Fractal–small-world dichotomy in
  real-world networks. *Phys. Rev. E* 70, 016122.
- Braunstein, S., Ghosh, S. & Severini, S. (2006). The Laplacian of a graph
  as a density matrix (BGS entropy); Passerini, F. & Severini, S. (2008).
  The von Neumann entropy of networks.
- Odlyzko, A. & Tilly, B. (2005). A refutation of Metcalfe's Law and a
  better estimate for the value of networks and network interconnections.
  (Counterpoint noted: later work argues Metcalfe's law fits some platform
  data — treat n log n as the conservative default.)
- Ghorbani, A. & Zou, J. (2019). Data Shapley: Equitable Valuation of Data
  for Machine Learning. *ICML* 2019, PMLR 97:2242–2251.

Reported by panelists, standard literature, not independently re-verified in
this round: Song, Havlin & Makse (2006); Song, Gallos, Havlin & Makse (2007);
Gallos et al. (2007); Rozenfeld et al. (2007); Watts & Strogatz (1998); Burt
(1992, 2004); Milo et al. (2002); Körner (1973); Dehmer (2008); Rissanen
(1978); Li & Vitányi (2008); Zenil et al. (2015); Jia et al. (2019);
Bergemann et al. (2022); Schneider et al. (2012); Briscoe et al. (2009);
Goodhart (1975).

## Appendix: Artifacts

- Panel brief + roles: `Tools/ModelKnowledge/panels/fractal_dimension_value_2026-07-04.json`
- Raw responses (verbatim, with hashes and usage):
  `Tools/ModelKnowledge/generated/panel_fractal_dimension_value_2026-07-04_20260704T094413Z.json`
- Panel runner: `Tools/ModelKnowledge/run_advisory_panel.py`
- NanoGPT model snapshot used for panelist selection:
  `Tools/ModelKnowledge/generated/nanogpt_models_20260704T081559Z.json`
