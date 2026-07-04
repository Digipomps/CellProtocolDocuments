# Palazzo Concierge Knowledge Bank - Implementation Notes

Date: 2026-05-28

This delivery turns the plan into a runnable contract prototype in:

- `Tools/ConciergeKnowledge/concierge_knowledge.py`
- `Tools/ConciergeKnowledge/palazzo_seed_corpus.json`
- `Tools/ConciergeKnowledge/eval_questions.jsonl`
- `Tools/ConciergeKnowledge/tests/test_concierge_knowledge.py`

## What Is Implemented

- `ConciergeKnowledgeCorpusCell` prototype with Cell-style dispatch actions:
  `concierge.knowledge.query`, `source.list`, `source.refresh`,
  `menu.current`, `beverage.current`, `claim.review`, and `audit.answer`.
- Typed corpus collections for sources, claims, menu items, beverages,
  ingredients, allergens, producers, regions, places, and pairings.
- Response envelope required by the plan:
  `answer`, `citations`, `last_verified`, `confidence`, `audience`, and
  `needs_human_review`.
- Structured-first guardrails for allergens, menu/prices, opening hours, wine,
  beverages, and availability.
- Hybrid retrieval with BM25-style lexical scoring, tags, and a deterministic
  hashed-vector scorer that can be replaced with real embeddings later.
- A 100-question eval set covering menu, allergens, Sicilian food, wine,
  compliance, area context, source freshness, unknown cases, and conflict
  handling.

## Current Limits

- This is not yet a Swift `GeneralCell` in `CellScaffold`; this thread's writable
  root is `CellProtocolDocuments`, so runtime wiring should be done in the
  `CellScaffold` workspace.
- The Palazzo menu PDF is image-based. Seed menu/allergen data is useful for
  internal behavior tests, but must be OCR-checked and staff-verified before
  guest-facing answers.
- Wine list, bottle availability, importer sheets, producer sheets, POS data,
  and live booking/capacity feeds are not ingested.
- Source refresh is metadata-only in the prototype. Production needs crawler,
  PDF/OCR, API, and partner-data adapters.

## Port To Production

1. Port `ConciergeKnowledgeCorpusCell` to Swift as a `GeneralCell` with explicit
   get/set or query intercepts matching the action names above.
2. Register Explore contracts for every public keypath and run the Explore audit.
3. Wire the Cell into `VaporRAGMVP` as a named case, for example
   `palazzo-communale-concierge`.
4. Add ingestion adapters:
   Palazzo crawler, menu PDF OCR, staff allergen sheet import, wine/supplier
   sheet import, eAmbrosia/Wikidata/OSM/Entur adapters.
5. Add an answer audit log flow so Concierge can review low-confidence,
   blocked, stale, and conflict-heavy questions.
6. Keep guest-facing answers behind a curated projection that hides staff notes
   and unverified source fragments.

## Acceptance Checks

- Factual answers always include citations.
- Allergen answers remain blocked or human-review flagged until staff verified.
- Wine availability is never claimed without a verified wine list or inventory
  source.
- Alcohol answers stay factual and cite the compliance source.
- Unknown structured facts return a refusal instead of a guessed answer.
