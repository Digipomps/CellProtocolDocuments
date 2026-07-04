# Text Reliability Tools

This folder contains the local, deterministic v1 reference implementation for
Chapter 27, Text Reliability Analysis.

The tool analyzes one or more text inputs, or an Add2Entity web-page capture,
and emits:

- `haven.text_reliability.analysis.v1` JSON;
- parsed markdown structure, including sections and markdown tables;
- section-based claim clusters;
- a claim-to-source matrix with one row per claim;
- a deterministic source-audit ledger with per-claim audit status;
- an argument graph with Mermaid source;
- optional productivity sizing scenarios for value/productivity claims;
- optional human-readable markdown report;
- optional Add2Entity sidecar metadata inside the analysis output.

It does not fetch the web, call hosted models, publish to RAG, mutate projects,
or mutate `EntityRepresentation`.

## Commands

Manual text:

```bash
python3 -B Tools/TextReliability/text_reliability.py \
  --text-file Tools/TextReliability/fixtures/project_description.txt \
  --title "Project description" \
  --out-json Tools/TextReliability/results/project.analysis.json \
  --out-md Tools/TextReliability/results/project.report.md
```

Manual text with explicit productivity scenarios:

```bash
python3 -B Tools/TextReliability/text_reliability.py \
  --text-file Deliverables/Norwegian_Innovation_Policy_Purpose_Goals_2026-06-21.md \
  --base-gdp-bn 4423 \
  --productivity-delta-pp 0.3 \
  --productivity-delta-pp 0.5 \
  --model-years 10 \
  --fiscal-gap-share-pct 6.2 \
  --out-json Tools/TextReliability/results/policy.analysis.json \
  --out-md Tools/TextReliability/results/policy.report.md
```

Add2Entity capture:

```bash
python3 -B Tools/TextReliability/text_reliability.py \
  --add2entity-capture Tools/TextReliability/fixtures/add2entity_capture.json \
  --out-json Tools/TextReliability/results/add2entity.analysis.json
```

Tests:

```bash
python3 -B -m unittest Tools/TextReliability/tests/test_text_reliability.py
```

## Boundaries

- Source status is conservative. URLs are `not_checkable` until a source auditor
  actually checks them.
- `source_audits` and `claim_source_matrix` prepare source-auditor work; they do
  not themselves prove source support.
- Missing citation language is `source_missing`.
- Markdown headings, table separators and fenced code blocks are structural
  input and should not be interpreted as prose claims.
- Rhetorical findings are not reliability verdicts by themselves.
- Inferred argument links are marked as inferred.
- Productivity models are sizing models only. They do not prove that a policy or
  innovation intervention caused the modeled productivity change.
