#!/usr/bin/env python3
"""Cell-shaped concierge knowledge corpus prototype.

This is a deliberately small, dependency-free implementation of the
ConciergeKnowledgeCorpusCell contract. It is meant to be easy to port into the
Swift Cell runtime once the CellScaffold workspace is the active writable repo.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


DEFAULT_CORPUS_PATH = Path(__file__).with_name("palazzo_seed_corpus.json")
REQUIRED_RESPONSE_KEYS = {
    "answer",
    "citations",
    "last_verified",
    "confidence",
    "audience",
    "needs_human_review",
}

STRUCTURED_TERMS = {
    "allergen",
    "allergener",
    "allergi",
    "gluten",
    "melk",
    "milk",
    "egg",
    "nuts",
    "notter",
    "skalldyr",
    "shellfish",
    "menu",
    "meny",
    "pris",
    "price",
    "opening",
    "apning",
    "hours",
    "drikke",
    "beverage",
    "wine",
    "vin",
    "beer",
    "ol",
}

ALCOHOL_TERMS = {
    "alcohol",
    "alkohol",
    "wine",
    "vin",
    "beer",
    "ol",
    "cocktail",
    "pairing",
    "paring",
    "anbefal",
    "recommend",
}

NO_ANSWER = (
    "I do not have a verified source for that yet. Do not answer guests from "
    "memory; ask staff to verify or add a cited source to the corpus."
)


def normalize(text: str) -> str:
    text = (
        text.replace("æ", "ae")
        .replace("Æ", "Ae")
        .replace("ø", "o")
        .replace("Ø", "O")
        .replace("å", "a")
        .replace("Å", "A")
    )
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return ascii_text.lower()


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalize(text))


def has_term(query_tokens: set[str], terms: set[str]) -> bool:
    for token in query_tokens:
        if token in terms:
            return True
        if any(token.startswith(term) for term in terms if len(term) >= 4):
            return True
    return False


def hashed_vector(input_tokens: list[str], dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    for token in input_tokens:
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).digest()
        bucket = int.from_bytes(digest, "big") % dimensions
        vector[bucket] += 1.0
    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector
    return [value / magnitude for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def today() -> dt.date:
    return dt.date.today()


def parse_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def newest_date(values: list[str]) -> str:
    dates = [parse_date(value) for value in values]
    dates = [value for value in dates if value is not None]
    if not dates:
        return ""
    return max(dates).isoformat()


class ConciergeKnowledgeCorpusCell:
    """Dispatches Cell-style knowledge actions over a typed JSON corpus."""

    def __init__(self, corpus: dict[str, Any]):
        self.corpus = corpus
        self.sources_by_id = {source["id"]: source for source in corpus.get("sources", [])}
        self.documents = self._build_documents()

    @classmethod
    def load(cls, path: Path = DEFAULT_CORPUS_PATH) -> "ConciergeKnowledgeCorpusCell":
        with path.open("r", encoding="utf-8") as handle:
            return cls(json.load(handle))

    def dispatch(self, action: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = payload or {}
        if action == "concierge.knowledge.query":
            return self.query(
                str(payload.get("query", "")),
                audience=str(payload.get("audience", "concierge")),
            )
        if action == "source.list":
            return self.source_list(audience=str(payload.get("audience", "concierge")))
        if action == "source.refresh":
            return self.source_refresh(audience=str(payload.get("audience", "concierge")))
        if action == "menu.current":
            return self.menu_current(audience=str(payload.get("audience", "concierge")))
        if action == "beverage.current":
            return self.beverage_current(audience=str(payload.get("audience", "concierge")))
        if action == "claim.review":
            return self.claim_review(str(payload.get("claim_id", "")), audience=str(payload.get("audience", "concierge")))
        if action == "audit.answer":
            return self.audit_answer(payload.get("response", {}), audience=str(payload.get("audience", "concierge")))
        return self._response(
            answer=f"Unsupported action: {action}",
            citations=[],
            confidence="blocked",
            audience=str(payload.get("audience", "concierge")),
            needs_human_review=True,
            warnings=["The action is not exposed by ConciergeKnowledgeCorpusCell."],
        )

    def source_list(self, audience: str = "concierge") -> dict[str, Any]:
        sources = self.corpus.get("sources", [])
        citations = [self._citation(source["id"]) for source in sources[:8]]
        return self._response(
            answer=f"{len(sources)} sources are registered for {self.corpus['tenant']['name']}.",
            citations=citations,
            confidence="high",
            audience=audience,
            needs_human_review=False,
            records=sources,
        )

    def source_refresh(self, audience: str = "concierge") -> dict[str, Any]:
        refresh_rows = []
        for source in self.corpus.get("sources", []):
            last_verified = parse_date(source.get("last_verified"))
            cadence = int(source.get("refresh_cadence_days", 30))
            stale = True
            age_days = None
            if last_verified is not None:
                age_days = (today() - last_verified).days
                stale = age_days > cadence
            refresh_rows.append(
                {
                    "source_id": source["id"],
                    "title": source["title"],
                    "last_verified": source.get("last_verified"),
                    "refresh_cadence_days": cadence,
                    "age_days": age_days,
                    "stale": stale,
                    "adapter": source.get("adapter", "manual"),
                }
            )
        stale_count = sum(1 for row in refresh_rows if row["stale"])
        return self._response(
            answer=(
                f"Refresh check completed from local metadata: {stale_count} of "
                f"{len(refresh_rows)} sources are stale or unverified."
            ),
            citations=[self._citation(row["source_id"]) for row in refresh_rows[:8]],
            confidence="medium",
            audience=audience,
            needs_human_review=stale_count > 0,
            records=refresh_rows,
            warnings=[
                "This prototype does not fetch remote content; production should use crawler/OCR adapters."
            ],
        )

    def menu_current(self, audience: str = "concierge") -> dict[str, Any]:
        menu_items = self.corpus.get("menu_items", [])
        unverified = [item for item in menu_items if not item.get("human_verified")]
        answer = (
            f"{len(menu_items)} menu items are seeded from Palazzo's image-based menu PDF. "
            "Use this as Concierge draft context only until staff verifies current menu, prices, and allergens."
        )
        return self._response(
            answer=answer,
            citations=[self._citation("src-palazzo-menu-pdf")],
            confidence="medium" if menu_items else "blocked",
            audience=audience,
            needs_human_review=bool(unverified),
            records=menu_items,
            warnings=[
                "Image-based PDF extraction requires OCR plus human verification before guest-safe use."
            ],
        )

    def beverage_current(self, audience: str = "concierge") -> dict[str, Any]:
        beverages = self.corpus.get("beverage_items", [])
        has_wine_gap = any(claim["id"] == "claim-wine-list-gap" for claim in self.corpus.get("claims", []))
        answer = (
            f"{len(beverages)} beverage items are seeded. Wine availability is not verified in this corpus."
        )
        return self._response(
            answer=answer,
            citations=[self._citation("src-palazzo-menu-pdf")],
            confidence="medium",
            audience=audience,
            needs_human_review=has_wine_gap,
            records=beverages,
            warnings=["Do not claim current wine availability until the restaurant wine list is ingested."],
        )

    def claim_review(self, claim_id: str, audience: str = "concierge") -> dict[str, Any]:
        claim = next((row for row in self.corpus.get("claims", []) if row["id"] == claim_id), None)
        if claim is None:
            return self._response(
                answer=f"Claim not found: {claim_id}",
                citations=[],
                confidence="blocked",
                audience=audience,
                needs_human_review=True,
                warnings=["Use source.list or query first to discover available claims."],
            )
        citations = [self._citation(source_id) for source_id in claim.get("source_ids", [])]
        return self._response(
            answer=claim["text"],
            citations=citations,
            confidence=claim.get("confidence", "medium"),
            audience=audience,
            needs_human_review=claim.get("needs_human_review", False),
            records=[claim],
            warnings=claim.get("warnings", []),
        )

    def audit_answer(self, response: dict[str, Any], audience: str = "concierge") -> dict[str, Any]:
        issues = []
        missing = sorted(REQUIRED_RESPONSE_KEYS - set(response.keys()))
        if missing:
            issues.append(f"Missing required response keys: {', '.join(missing)}")
        if not response.get("citations"):
            issues.append("No citations attached.")
        answer = str(response.get("answer", ""))
        if "allergen" in normalize(answer) and not response.get("needs_human_review", True):
            issues.append("Allergen answer is marked guest-safe without human review flag.")
        if any(term in tokens(answer) for term in ALCOHOL_TERMS) and not response.get("citations"):
            issues.append("Alcohol-related answer lacks cited source.")
        return self._response(
            answer="Answer audit passed." if not issues else "Answer audit found issues.",
            citations=[],
            confidence="high" if not issues else "blocked",
            audience=audience,
            needs_human_review=bool(issues),
            records=[{"issues": issues}],
        )

    def query(self, query: str, audience: str = "concierge") -> dict[str, Any]:
        query_norm = normalize(query)
        query_tokens = set(tokens(query))
        if not query_tokens:
            return self._response(
                answer="Ask a concrete question about Palazzo, the menu, beverages, ingredients, regions, or nearby context.",
                citations=[],
                confidence="blocked",
                audience=audience,
                needs_human_review=False,
            )
        if has_term(query_tokens, {"allergen", "allergener", "allergi", "gluten", "melk", "milk", "egg", "nuts", "notter"}):
            return self._answer_allergen_query(query, audience)
        if has_term(query_tokens, {"menu", "meny", "mat", "food", "pris", "price"}):
            return self.menu_current(audience)
        if has_term(query_tokens, {"drikke", "beverage", "beverages", "ol", "beer"}):
            return self.beverage_current(audience)
        if has_term(query_tokens, {"vin", "wine"}):
            return self._answer_wine_query(query, audience)
        if has_term(query_tokens, {"apning", "opening", "hours", "stengt", "open"}):
            return self.claim_review("claim-opening-hours", audience)
        if "current" in query_tokens and has_term(query_tokens, STRUCTURED_TERMS):
            return self._unknown_structured(query, audience)
        return self._answer_search_query(query, audience)

    def _answer_allergen_query(self, query: str, audience: str) -> dict[str, Any]:
        item = self._best_record_match(query, self.corpus.get("menu_items", []))
        if item is None:
            return self._response(
                answer=(
                    "I cannot identify the menu item from the verified corpus. "
                    "Ask staff or add the item from the allergen sheet before answering."
                ),
                citations=[self._citation("src-mattilsynet-allergen")],
                confidence="blocked",
                audience=audience,
                needs_human_review=True,
                warnings=["Allergen questions require item-level verification."],
            )
        allergen_codes = item.get("allergen_codes", [])
        allergen_names = [self._allergen_name(code) for code in allergen_codes]
        if not item.get("human_verified_allergens"):
            answer = (
                f"I cannot give a guest-safe allergen answer for {item['name']} yet. "
                f"The seeded menu extraction lists: {', '.join(allergen_names) or 'no parsed allergens'}, "
                "but it needs staff verification against the current allergen sheet."
            )
            return self._response(
                answer=answer,
                citations=[self._citation("src-palazzo-menu-pdf"), self._citation("src-mattilsynet-allergen")],
                confidence="low",
                audience=audience,
                needs_human_review=True,
                records=[item],
                warnings=["Do not present this allergen answer to guests until verified."],
            )
        return self._response(
            answer=f"{item['name']} is marked with: {', '.join(allergen_names)}.",
            citations=[self._citation(source_id) for source_id in item.get("source_ids", [])],
            confidence="high",
            audience=audience,
            needs_human_review=False,
            records=[item],
        )

    def _answer_wine_query(self, query: str, audience: str) -> dict[str, Any]:
        pairings = self._rank_records(query, self.corpus.get("pairings", []), limit=3)
        warnings = [
            "Wine availability is not verified. Keep answers factual and ask the sommelier for current bottles."
        ]
        if pairings:
            lines = [f"{row['record']['menu_item_name']}: {row['record']['guidance']}" for row in pairings]
            answer = (
                "No verified wine list is ingested. Draft internal pairing notes: "
                + " ".join(lines)
            )
            source_ids = sorted({source_id for row in pairings for source_id in row["record"].get("source_ids", [])})
            citations = [self._citation(source_id) for source_id in source_ids] or [self._citation("src-helsedir-alcohol-ad")]
        else:
            answer = (
                "No verified wine list or producer sheet is ingested yet. Do not claim availability; ask the sommelier."
            )
            citations = [self._citation("src-helsedir-alcohol-ad"), self._citation("src-palazzo-menu-pdf")]
        return self._response(
            answer=answer,
            citations=citations,
            confidence="low",
            audience=audience,
            needs_human_review=True,
            records=[row["record"] for row in pairings],
            warnings=warnings,
        )

    def _answer_search_query(self, query: str, audience: str) -> dict[str, Any]:
        ranked = self._rank_documents(query, limit=5)
        if not ranked:
            return self._unknown_structured(query, audience)
        top = ranked[0]["record"]
        source_ids = sorted({source_id for row in ranked for source_id in row["record"].get("source_ids", [])})
        snippets = []
        for row in ranked[:3]:
            record = row["record"]
            label = record.get("name") or record.get("title") or record.get("id")
            text = record.get("text") or record.get("description") or record.get("guidance") or ""
            snippets.append(f"{label}: {text}")
        confidence = "medium" if ranked[0]["score"] >= 2.0 else "low"
        needs_review = any(row["record"].get("needs_human_review") for row in ranked)
        if any(term in tokens(query) for term in ALCOHOL_TERMS):
            needs_review = True
        return self._response(
            answer=" ".join(snippets),
            citations=[self._citation(source_id) for source_id in source_ids],
            confidence=confidence,
            audience=audience,
            needs_human_review=needs_review,
            records=[row["record"] for row in ranked],
            warnings=self._guardrail_warnings(query, ranked),
        )

    def _unknown_structured(self, query: str, audience: str) -> dict[str, Any]:
        citations = [self._citation("src-palazzo-site")]
        return self._response(
            answer=NO_ANSWER,
            citations=citations,
            confidence="blocked",
            audience=audience,
            needs_human_review=True,
            warnings=["Structured facts require a fresh cited record before Concierge can answer."],
        )

    def _guardrail_warnings(self, query: str, ranked: list[dict[str, Any]]) -> list[str]:
        warnings = []
        query_tokens = set(tokens(query))
        if query_tokens & ALCOHOL_TERMS:
            warnings.append("Alcohol answers must stay sober and informational under Norwegian advertising rules.")
        if query_tokens & {"allergen", "allergener", "gluten", "melk", "milk", "egg", "nuts", "notter"}:
            warnings.append("Allergen answers require item-level human verification.")
        if any(row["record"].get("needs_human_review") for row in ranked):
            warnings.append("At least one supporting record is flagged for human review.")
        return warnings

    def _build_documents(self) -> list[dict[str, Any]]:
        documents = []
        collections = [
            ("claim", "claims"),
            ("menu_item", "menu_items"),
            ("beverage_item", "beverage_items"),
            ("ingredient", "ingredients"),
            ("allergen", "allergens"),
            ("producer", "producers"),
            ("region", "regions"),
            ("place", "places"),
            ("pairing", "pairings"),
        ]
        for record_type, collection in collections:
            for record in self.corpus.get(collection, []):
                text = " ".join(
                    str(record.get(field, ""))
                    for field in ("name", "title", "text", "description", "guidance", "notes")
                )
                text += " " + " ".join(record.get("tags", []))
                documents.append(
                    {
                        "record_type": record_type,
                        "record": record,
                        "tokens": tokens(text),
                        "vector": hashed_vector(tokens(text)),
                    }
                )
        return documents

    def _rank_documents(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        query_tokens = tokens(query)
        if not query_tokens:
            return []
        query_vector = hashed_vector(query_tokens)
        avg_len = sum(len(doc["tokens"]) for doc in self.documents) / max(len(self.documents), 1)
        document_frequency = {}
        for token in set(query_tokens):
            document_frequency[token] = sum(1 for doc in self.documents if token in doc["tokens"])
        ranked = []
        for doc in self.documents:
            lexical_score = self._bm25_score(query_tokens, doc["tokens"], document_frequency, avg_len)
            vector_score = cosine(query_vector, doc["vector"])
            tag_boost = self._tag_score(query_tokens, doc["record"].get("tags", []))
            score = lexical_score + (0.75 * vector_score) + tag_boost
            if lexical_score > 0 or tag_boost > 0 or vector_score >= 0.60:
                ranked.append({"score": score, "record": doc["record"], "record_type": doc["record_type"]})
        ranked.sort(key=lambda row: row["score"], reverse=True)
        return ranked[:limit]

    def _rank_records(self, query: str, records: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
        query_tokens = set(tokens(query))
        ranked = []
        for record in records:
            record_tokens = set(tokens(" ".join(str(record.get(field, "")) for field in record.keys())))
            overlap = len(query_tokens & record_tokens)
            tag_boost = self._tag_score(list(query_tokens), record.get("tags", []))
            score = overlap + tag_boost
            if score > 0:
                ranked.append({"score": score, "record": record})
        ranked.sort(key=lambda row: row["score"], reverse=True)
        return ranked[:limit]

    def _best_record_match(self, query: str, records: list[dict[str, Any]]) -> dict[str, Any] | None:
        ranked = self._rank_records(query, records, limit=1)
        if not ranked:
            return None
        if ranked[0]["score"] <= 0:
            return None
        return ranked[0]["record"]

    def _bm25_score(
        self,
        query_tokens: list[str],
        doc_tokens: list[str],
        document_frequency: dict[str, int],
        avg_len: float,
    ) -> float:
        if not doc_tokens:
            return 0.0
        k1 = 1.2
        b = 0.75
        score = 0.0
        doc_len = len(doc_tokens)
        total_docs = max(len(self.documents), 1)
        for token in query_tokens:
            frequency = doc_tokens.count(token)
            if frequency == 0:
                continue
            df = document_frequency.get(token, 0)
            idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
            numerator = frequency * (k1 + 1)
            denominator = frequency + k1 * (1 - b + b * doc_len / max(avg_len, 1))
            score += idf * numerator / denominator
        return score

    def _tag_score(self, query_tokens: list[str], tags: list[str]) -> float:
        tag_tokens = set(tokens(" ".join(tags)))
        return 0.5 * len(set(query_tokens) & tag_tokens)

    def _allergen_name(self, code: str) -> str:
        allergen = next((row for row in self.corpus.get("allergens", []) if row["code"] == code), None)
        return allergen["name"] if allergen else code

    def _citation(self, source_id: str) -> dict[str, Any]:
        source = self.sources_by_id.get(source_id)
        if source is None:
            return {
                "source_id": source_id,
                "title": "Unknown source",
                "url": None,
                "last_verified": None,
                "status": "missing",
            }
        return {
            "source_id": source["id"],
            "title": source["title"],
            "url": source.get("url"),
            "section": source.get("section"),
            "last_verified": source.get("last_verified"),
            "license": source.get("license"),
            "status": source.get("status", "active"),
        }

    def _response(
        self,
        *,
        answer: str,
        citations: list[dict[str, Any]],
        confidence: str,
        audience: str,
        needs_human_review: bool,
        records: list[dict[str, Any]] | None = None,
        warnings: list[str] | None = None,
    ) -> dict[str, Any]:
        cited_dates = [citation.get("last_verified") for citation in citations if citation.get("last_verified")]
        return {
            "answer": answer,
            "citations": citations,
            "last_verified": newest_date(cited_dates),
            "confidence": confidence,
            "audience": audience,
            "needs_human_review": needs_human_review,
            "records": records or [],
            "warnings": warnings or [],
            "contract_version": self.corpus.get("contract_version", "unknown"),
        }


def parse_payload(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    if value == "-":
        return json.load(sys.stdin)
    return json.loads(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the ConciergeKnowledgeCorpusCell prototype.")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    query = subparsers.add_parser("query", help="Run concierge.knowledge.query")
    query.add_argument("text")
    query.add_argument("--audience", default="concierge")

    action = subparsers.add_parser("action", help="Dispatch a Cell-style action")
    action.add_argument("name")
    action.add_argument("--payload", default=None, help="JSON object or '-' for stdin")

    subparsers.add_parser("source-list", help="List registered sources")
    subparsers.add_parser("refresh", help="Run local source freshness check")
    subparsers.add_parser("menu", help="Return current menu seed")
    subparsers.add_parser("beverages", help="Return current beverage seed")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cell = ConciergeKnowledgeCorpusCell.load(args.corpus)
    if args.command == "query":
        response = cell.dispatch(
            "concierge.knowledge.query",
            {"query": args.text, "audience": args.audience},
        )
    elif args.command == "action":
        response = cell.dispatch(args.name, parse_payload(args.payload))
    elif args.command == "source-list":
        response = cell.dispatch("source.list")
    elif args.command == "refresh":
        response = cell.dispatch("source.refresh")
    elif args.command == "menu":
        response = cell.dispatch("menu.current")
    elif args.command == "beverages":
        response = cell.dispatch("beverage.current")
    else:
        raise AssertionError(f"Unhandled command: {args.command}")
    print(json.dumps(response, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
