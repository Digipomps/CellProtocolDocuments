# Chapter 27 - Text Reliability Analysis

Status: draft operational contract.

Last updated: 2026-06-23.

This chapter defines a HAVEN workflow for analyzing written material without
turning the analysis system into a content generator. It is intended for
op-eds, political statements, project descriptions, web captures and other
texts where the user wants to evaluate argumentation, rhetoric and source
grounding.

Machine-readable contract:

`Book/text_reliability_analysis_contract_v1.json`

Reference tool:

`Tools/TextReliability/text_reliability.py`

## 1. Purpose

The analyzer answers:

- what claims does the text make?
- what argument structure supports those claims?
- which claim clusters and argument graph summarize the structure?
- which rhetorical moves are present?
- which claims are grounded in sources, missing sources, or not checkable?
- which claims require source-auditor follow-up?
- whether quantitative productivity/value claims use transparent assumptions?
- how reliable is the text along explicit dimensions?

The analyzer must not:

- rewrite the text;
- produce better arguments for the author;
- invent missing evidence;
- infer hidden motives;
- treat rhetoric as automatically bad;
- publish or mutate entity state without a separate explicit action.

## 2. Analysis Pipeline

### 2.1 Intake and boundaries

Each input receives a stable `input_id`, metadata, text length, optional source
URL and a list of exact quote anchors. Metadata can come from a manual submit,
RAG/Vault document, or an Add2Entity web-page capture.

The intake layer must record:

- date/time of analysis;
- source mode;
- language if known;
- genre and author if provided;
- source URL if provided;
- whether the text came through Add2Entity, RAG, Vault or manual input.

### 2.2 Claim extraction

Claims are normalized into a claim ledger. Markdown structure is parsed before
claim extraction so headings, table separators and fenced code blocks are not
mistaken for prose claims. Markdown table data rows can become
`markdown_table_row` claims with table metadata.

Every claim must include:

- `claim_id`;
- `input_id`;
- exact quote;
- character span;
- claim type: `factual`, `causal`, `normative`, `predictive`,
  `statistical`, or `project_capability`;
- strength: `assertive`, `moderated`, or `speculative`;
- source references found inside the same sentence or paragraph;
- `origin`: currently `sentence` or `markdown_table_row`;
- `section_id` when the text has a markdown heading before the claim;
- `is_inferred=false` unless a later adviser explicitly infers a premise.

The quote is the audit anchor. If the analyzer cannot anchor a claim to exact
input text, the claim must not appear in the ledger.

### 2.3 Claim clustering and source matrix

The analyzer emits:

- `claim_clusters`: section-based clusters with claim counts, origin counts,
  claim type counts and source-audit status counts;
- `claim_source_matrix`: one row per claim with cluster, section, type, quote,
  source refs, source-check status, source-audit status and evidence grade.

This matrix is the handoff surface for a source-auditor agent or RAG/web
verification pass.

### 2.4 Argument map and graph

The argument map separates:

- conclusions explicitly stated in the text;
- premises explicitly stated in the text;
- inferred warrants or missing bridges.

Inferred warrants must be marked as `is_inferred=true` and must be phrased as an
analysis relation, not as a new claim made by the author.

The reference tool also emits `argument_graph`:

- graph nodes are deterministic claim-cluster nodes;
- graph edges include section-order `develops` links and heuristic inferred
  support/context links;
- `argument_graph.mermaid` contains a Mermaid `flowchart TD` visualization.

This graph is an orientation aid, not final adjudication. A reasoning model or
human reviewer should refine warrants for high-stakes use.

Runtime claim structures that share this chapter's wire vocabulary (claim
types, strength, source-audit statuses) are defined in
`Book/29_Claim_Argument_Model.md`.

### 2.5 Rhetorical analysis

Rhetorical findings are evidence tags, not automatic defects. The analyzer can
tag ethos, pathos, logos, framing, loaded language, contrast, strawman, false
dichotomy, anecdotal evidence, cherry-picking, authority appeal and certainty
inflation.

Each finding must include:

- exact quote;
- character span;
- type;
- whether the rhetoric appears to substitute for evidence or only shape
  presentation.

### 2.6 Source-auditor phase and evidence checks

Source mode controls how far the system may go:

- `text_only`: analyze only submitted text and sources named inside it.
- `verifying`: external lookup may verify, contradict, or mark missing support
  for submitted claims.
- `investigative`: missing and contrary sources may be searched, but must stay
  separate from the text's own argument.

Status per claim:

- `supported`;
- `partly_supported`;
- `contradicted`;
- `source_missing`;
- `not_found`;
- `not_checkable`.

The local reference tool does not fetch the web. It now emits a separate
`source_audits` ledger and annotates each claim with:

- `source_check_status`;
- `source_audit_status`;
- `source_audit_required`;
- `evidence_grade`.

Current deterministic source-audit statuses:

- `text_only_not_audited`: source mode forbids external checking;
- `needs_external_source_audit`: a URL or source anchor exists, but was not
  fetched or verified by the local tool;
- `source_cue_without_anchor`: the text names a source generically but does not
  provide a retrievable anchor;
- `source_missing`: no nearby source reference was found.

URL-backed claims remain `not_checkable` until a source-auditor agent or RAG/web
tool actually performs the check. The deterministic phase prepares the work; it
does not claim support.

### 2.7 Quantitative model pass

When text or CLI policy supplies productivity/value-creation inputs, the tool
emits `quantitative_models`.

The first implemented model is:

`productivity-compound-level-effect`

It computes:

```text
base_gdp_bn * ((1 + base_growth + delta) ** years - (1 + base_growth) ** years)
```

Supported inputs:

- `base_gdp_bn`;
- `base_growth_pct`;
- repeated `productivity_delta_pp` values;
- `model_years`;
- `fiscal_gap_share_pct`.

The model may also extract obvious Norwegian policy-report patterns such as
`579,4 mrd. / 0,131 = ca. 4 423 mrd. kroner` and `0,3 prosentpoeng`.

Boundary: this is a sizing model, not a causal proof that innovation will
deliver the productivity gain.

### 2.8 Contrary evidence

Contrary evidence is allowed only as a separate ledger. It must not be blended
into the author's argument. A contrary-evidence item needs a source anchor,
retrieval date and explanation of which submitted claim it affects.

### 2.9 Adviser panel and adjudication

V1 adviser roles:

- text-internal analyst;
- source auditor;
- skeptic;
- steelman/fairness reviewer;
- domain expert when needed;
- final adjudicator.

The adviser panel is a workflow and prompt contract, not a global runtime object.
Purpose- and claim-grounded task decomposition for panel work is defined in
`Book/30_Panel_Task_Decomposition_Workflow.md`.
The final adjudicator may only conclude from quote anchors, source anchors and
explicitly marked inferences.

## 3. Model Routing

Use the model ladder from Chapters 24 and 26:

1. deterministic local rules for parsing, anchoring, validation and report
   shaping;
2. small/cheap structured-output models for bulk claim and rhetoric extraction;
3. frontier reasoning models for argument adjudication and source conflicts;
4. source-auditor tools for web/RAG verification;
5. human review for high-stakes or unresolved claims.

Model recommendations are date-sensitive. Refresh provider/model metadata before
production routing, procurement or public claims about which model is best.

## 4. Add2Entity Integration

Add2Entity can feed this workflow directly because its capture contract already
contains `content.text`, source URL, title, author-like metadata, target project
metadata and RAG case metadata.

Recommended flow:

1. User captures a web page through Add2Entity.
2. Add2Entity prepares `haven.add2entity.webpage-capture.v1`.
3. A user-visible action runs text reliability analysis on `content.text`.
4. The analyzer returns a sidecar object:
   `haven.text_reliability.add2entity_sidecar.v1`.
5. The user may attach the sidecar to the RAG chunk metadata or target project
   as provenance.

Important boundary:

- the analysis sidecar is `mutatesEntity=false`;
- Add2Entity must not silently write reliability findings into
  `EntityRepresentation`;
- linking a sidecar to a project, idea or RAG case requires a separate explicit
  user action and normal CellProtocol grants.

Minimum Add2Entity sidecar fields:

```json
{
  "schema": "haven.text_reliability.add2entity_sidecar.v1",
  "captureID": "capture-id",
  "analysisSchema": "haven.text_reliability.analysis.v1",
  "analysisID": "analysis-id",
  "mutatesEntity": false,
  "target": {
    "kind": "project",
    "projectID": "project-id",
    "cellEndpoint": "cell:///ProjectPortfolio"
  },
  "summary": {
    "claimCount": 0,
    "sourceMissingCount": 0,
    "notCheckableCount": 0,
    "rhetoricFindingCount": 0
  }
}
```

## 5. Reference Tool

Run a manual text file:

```bash
python3 -B Tools/TextReliability/text_reliability.py \
  --text-file sample.txt \
  --title "Sample" \
  --out-json Tools/TextReliability/results/sample.analysis.json \
  --out-md Tools/TextReliability/results/sample.report.md
```

Run with explicit productivity model inputs:

```bash
python3 -B Tools/TextReliability/text_reliability.py \
  --text-file sample.txt \
  --base-gdp-bn 4423 \
  --productivity-delta-pp 0.3 \
  --productivity-delta-pp 0.5 \
  --model-years 10 \
  --fiscal-gap-share-pct 6.2 \
  --out-json Tools/TextReliability/results/sample.analysis.json \
  --out-md Tools/TextReliability/results/sample.report.md
```

Run an Add2Entity capture:

```bash
python3 -B Tools/TextReliability/text_reliability.py \
  --add2entity-capture capture.json \
  --out-json Tools/TextReliability/results/capture.analysis.json
```

The reference tool is deliberately conservative. It provides deterministic
anchoring, Markdown table parsing, heuristic claim/rhetoric extraction, claim
clusters, claim-to-source matrix rows, per-claim source-audit statuses, a
Mermaid-ready argument graph, optional productivity sizing models and a report.
It does not call hosted models, browse the web or publish to RAG.

## 6. Acceptance Criteria

- every claim and rhetoric finding has an exact quote anchor;
- Markdown headings, table separators and fenced code blocks do not become
  ordinary prose claims;
- table claims carry `origin=markdown_table_row` and table metadata;
- every claim has a source-audit status and appears in `claim_source_matrix`;
- source support is not claimed unless a source-auditor step has checked it;
- argument graph edges produced by the deterministic tool are marked as
  heuristic/inferred where applicable;
- productivity models expose assumptions, formula, scenarios and limitations;
- inferred argument bridges are marked as inferred;
- Add2Entity linkage is sidecar/provenance only until the user explicitly
  commits it;
- high-stakes analysis defaults to human review.
