# Sicilia Food And Wine Research Agent

Status: review-first candidate pipeline.

This directory is the first executable step toward a Sicilian food and wine
supplement for Palazzo Concierge. It does not publish to RAG or runtime storage.
It creates a small candidate bundle that a human can review before ingestion.

## Inputs

- `candidate_sources.jsonl`: minimal source registry.
- `candidate_claims.jsonl`: extracted factual/policy claims.

Keep records small. Do not store raw HTML, full pages, or large excerpts here.
Each claim should carry source IDs, confidence, relevance, and guardrails.

## Run

```bash
python3 Tools/ConciergeKnowledge/sicilia_research_agent.py validate
python3 Tools/ConciergeKnowledge/sicilia_research_agent.py bundle
python3 Tools/ConciergeKnowledge/sicilia_research_agent.py publishable
```

The bundle output is:

```text
Tools/ConciergeKnowledge/sicilia_research/sicilia_research_review_bundle.json
```

## Review Rules

- `public_guest` claims must be cited.
- Alcohol-related claims require `alcohol_policy`.
- Wine availability at Palazzo is always blocked unless a current Palazzo source
  proves availability.
- `single_source` food context stays in `staff_review` until checked against a
  primary source such as eAmbrosia, MASAF, a product consortium, or Slow Food.
- RAG chunks are generated only for claims that pass local publishability checks.

## Intended CellProtocol Path

1. Use `WebFetchCell` for explicit source previews.
2. Use a local assistant to propose candidate JSONL records.
3. Run this validator.
4. Human review approves or rejects records.
5. Publish approved chunks through `RAGGatewayCell.catalog.publish` into a case
   such as `palazzo_sicilia_supplement`.
6. Keep deterministic facts and guardrails in a metadata/claim store, not only
   in vector retrieval.

## Current Seed Scope

The first seed focuses on Cerasuolo di Vittoria DOCG, Norwegian alcohol
guardrails, and a small Sicilian food-context discovery set. It is deliberately
small so the review shape is clear before broad collection.
