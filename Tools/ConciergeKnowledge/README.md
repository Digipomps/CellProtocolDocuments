# Concierge Knowledge Corpus Prototype

This directory contains a runnable contract prototype for a Palazzo-first
`ConciergeKnowledgeCorpusCell`.

It is intentionally dependency-free and conservative:

- structured lookup is used before free-text search for menu, allergens, prices,
  opening hours, beverages, wine, and availability
- every response includes `answer`, `citations`, `last_verified`, `confidence`,
  `audience`, and `needs_human_review`
- allergen, current menu, price, opening-hour, and wine-availability answers are
  blocked or flagged until a current source is verified
- alcohol-related answers stay factual and cite the compliance source
- free-text retrieval combines BM25-style lexical scoring, tag boosts, and a
  local deterministic hashed-vector scorer so it can run without external
  embedding infrastructure

## Run

```bash
python3 Tools/ConciergeKnowledge/concierge_knowledge.py query "Hva er allergenene i arancini?"
python3 Tools/ConciergeKnowledge/concierge_knowledge.py query "Hvilken vin passer til vongole?"
python3 Tools/ConciergeKnowledge/concierge_knowledge.py menu
python3 Tools/ConciergeKnowledge/concierge_knowledge.py source-list
python3 Tools/ConciergeKnowledge/concierge_knowledge.py refresh
```

## Sicilia Food And Wine Research

The first review-first research pass for a Sicilian food and wine supplement
lives in `sicilia_research/` and is validated by
`sicilia_research_agent.py`. It does not publish to RAG or runtime storage; it
only validates candidate sources/claims and emits a review bundle.

```bash
python3 Tools/ConciergeKnowledge/sicilia_research_agent.py validate
python3 Tools/ConciergeKnowledge/sicilia_research_agent.py bundle
python3 Tools/ConciergeKnowledge/sicilia_research_agent.py publishable
```

Use this before adding approved Sicilian context to the Palazzo concierge
runtime. Alcohol-related claims must stay neutral and factual, and current
Palazzo wine availability still requires a Palazzo-owned source or staff
confirmation.

Cell-style dispatch:

```bash
python3 Tools/ConciergeKnowledge/concierge_knowledge.py action concierge.knowledge.query \
  --payload '{"query":"Hva er historien rundt Bronte-pistasj?", "audience":"concierge"}'
```

## Exposed Actions

- `concierge.knowledge.query`
- `source.list`
- `source.refresh`
- `menu.current`
- `beverage.current`
- `claim.review`
- `audit.answer`

## Data Shape

`palazzo_seed_corpus.json` contains typed collections for:

- `KnowledgeSource` -> `sources`
- `KnowledgeClaim` -> `claims`
- `MenuItem` -> `menu_items`
- `BeverageItem` -> `beverage_items`
- `Ingredient` -> `ingredients`
- `Allergen` -> `allergens`
- `Producer` -> `producers`
- `Region` -> `regions`
- `Place` -> `places`
- `Pairing` -> `pairings`

This is not a production crawler. The PDF menu is image-based; menu and allergen
records are seed data that must be OCR-checked and staff-verified before
guest-facing use.

## Porting To CellScaffold

When the writable workspace is `CellScaffold`, port the Python class to a Swift
`GeneralCell`:

- keep `state` read-only for source/corpus summary
- register the actions above as explicit get/set or query intercepts
- emit audit flows for answered queries and blocked safety-critical questions
- add Explore contracts for every public keypath
- wire the Cell into the RAG gateway as a case such as
  `palazzo-communale-concierge`

The current prototype is useful as a golden behavior harness for that port:
answers should preserve the same response envelope and guardrails.
