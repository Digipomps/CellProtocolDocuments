#!/usr/bin/env python3
"""Read-only MCP server for HAVEN CellProtocol documentation.

The server intentionally uses only the Python standard library so it can run in
fresh agent environments without installing the MCP SDK first. It implements the
stdio JSON-RPC surface needed by MCP clients for resources, tools, and prompts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote, unquote, urlparse


SERVER_NAME = "haven-docs-mcp"
SERVER_TITLE = "HAVEN Docs MCP"
SERVER_VERSION = "0.1.0"
SUPPORTED_PROTOCOL_VERSIONS = (
    "2025-11-25",
    "2025-06-18",
    "2025-03-26",
    "2024-11-05",
)
DEFAULT_MAX_CHARS = 24000
MAX_SEARCH_RESULTS = 20

ROOT = Path(__file__).resolve().parents[2]
BOOK_DIR = ROOT / "Book"
CATALOG_PATH = BOOK_DIR / "book_catalog.json"


class DocsError(Exception):
    """Domain error that maps cleanly to a JSON-RPC or tool error."""

    def __init__(self, message: str, code: int = -32602, data: Any | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data


@dataclass(frozen=True)
class DocEntry:
    doc_id: str
    title: str
    path: str
    slug: str
    group: str
    audience: str
    status: str
    order: int
    mime_type: str = "text/markdown"

    @property
    def uri(self) -> str:
        return f"haven-docs://book/{quote(self.doc_id, safe='')}"

    @property
    def absolute_path(self) -> Path:
        return resolve_repo_path(self.path)

    def metadata(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "path": self.path,
            "slug": self.slug,
            "group": self.group,
            "audience": self.audience,
            "status": self.status,
            "order": self.order,
            "uri": self.uri,
            "mimeType": self.mime_type,
        }


@dataclass(frozen=True)
class Section:
    doc: DocEntry
    heading: str
    heading_anchor: str
    level: int
    line_start: int
    line_end: int
    text: str

    def citation(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc.doc_id,
            "title": self.doc.title,
            "path": self.doc.path,
            "slug": self.doc.slug,
            "heading": self.heading,
            "heading_anchor": self.heading_anchor,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "status": self.doc.status,
        }


def resolve_repo_path(path_text: str) -> Path:
    path = (ROOT / path_text).resolve()
    root = ROOT.resolve()
    if path != root and root not in path.parents:
        raise DocsError(f"Path escapes repository root: {path_text}", data={"path": path_text})
    if not path.is_file():
        raise DocsError(f"Documentation file not found: {path_text}", code=-32002, data={"path": path_text})
    return path


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_catalog() -> tuple[dict[str, Any], list[DocEntry]]:
    catalog = json.loads(read_text_file(CATALOG_PATH))
    docs = [
        DocEntry(
            doc_id=item["doc_id"],
            title=item["title"],
            path=item["path"],
            slug=item["slug"],
            group=item["group"],
            audience=item.get("audience", "both"),
            status=item.get("status", "active"),
            order=int(item.get("order", 0)),
        )
        for item in catalog.get("documents", [])
    ]
    extra_docs = [
        DocEntry(
            doc_id="repo-readme-cellprotocol",
            title="CellProtocol Documentation Index",
            path="README-CellProtocol.md",
            slug="readme-cellprotocol",
            group="navigation",
            audience="both",
            status="active",
            order=-30,
        ),
        DocEntry(
            doc_id="repo-developers",
            title="CellProtocolDocuments Developer Guide",
            path="DEVELOPERS.md",
            slug="developers",
            group="developer-guides",
            audience="both",
            status="active",
            order=-20,
        ),
        DocEntry(
            doc_id="repo-gap-analysis",
            title="CellProtocol Documentation Gap Analysis",
            path="Gap_Analysis.md",
            slug="gap-analysis",
            group="developer-guides",
            audience="both",
            status="active",
            order=-10,
        ),
    ]
    return catalog, sorted(extra_docs + docs, key=lambda doc: (doc.order, doc.path))


def normalize_anchor(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[`*_~\[\]<>]", "", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def parse_sections(doc: DocEntry) -> list[Section]:
    text = read_text_file(doc.absolute_path)
    lines = text.splitlines()
    headings: list[tuple[int, int, str, str]] = []
    seen_anchors: dict[str, int] = {}
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        heading = match.group(2).strip().strip("#").strip()
        base_anchor = normalize_anchor(heading)
        count = seen_anchors.get(base_anchor, 0) + 1
        seen_anchors[base_anchor] = count
        anchor = base_anchor if count == 1 else f"{base_anchor}-{count}"
        headings.append((index, len(match.group(1)), heading, anchor))

    if not headings:
        return [
            Section(
                doc=doc,
                heading=doc.title,
                heading_anchor="",
                level=0,
                line_start=1,
                line_end=max(1, len(lines)),
                text=text,
            )
        ]

    sections: list[Section] = [
        Section(
            doc=doc,
            heading=doc.title,
            heading_anchor="",
            level=0,
            line_start=1,
            line_end=max(1, len(lines)),
            text=text,
        )
    ]

    for pos, (start, level, heading, anchor) in enumerate(headings):
        end = len(lines)
        for next_start, next_level, _next_heading, _next_anchor in headings[pos + 1 :]:
            if next_level <= level:
                end = next_start
                break
        section_text = "\n".join(lines[start:end]).strip()
        sections.append(
            Section(
                doc=doc,
                heading=heading,
                heading_anchor=anchor,
                level=level,
                line_start=start + 1,
                line_end=max(start + 1, end),
                text=section_text,
            )
        )
    return sections


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[\w:/.-]+", text, flags=re.UNICODE) if len(token) > 1]


class DocsIndex:
    def __init__(self) -> None:
        self.catalog, self.docs = load_catalog()
        self.by_id = {doc.doc_id: doc for doc in self.docs}
        self.by_slug = {doc.slug: doc for doc in self.docs}
        self.by_path = {doc.path: doc for doc in self.docs}

    def list_docs(
        self,
        *,
        status: str | None = None,
        group: str | None = None,
        audience: str | None = None,
    ) -> list[DocEntry]:
        docs = self.docs
        if status:
            docs = [doc for doc in docs if doc.status == status]
        if group:
            docs = [doc for doc in docs if doc.group == group]
        if audience:
            docs = [doc for doc in docs if doc.audience in (audience, "both")]
        return docs

    def resolve_doc(self, identifier: str) -> DocEntry:
        identifier = identifier.strip()
        if identifier in self.by_id:
            return self.by_id[identifier]
        if identifier in self.by_slug:
            return self.by_slug[identifier]
        if identifier in self.by_path:
            return self.by_path[identifier]
        if identifier.startswith("haven-docs://"):
            parsed = urlparse(identifier)
            if parsed.netloc == "book":
                doc_id = unquote(parsed.path.lstrip("/"))
                if doc_id in self.by_id:
                    return self.by_id[doc_id]
        raise DocsError(
            f"Unknown documentation identifier: {identifier}",
            code=-32002,
            data={"identifier": identifier},
        )

    def sections(self, doc: DocEntry) -> list[Section]:
        return parse_sections(doc)

    def read_section(
        self,
        identifier: str,
        *,
        heading: str | None = None,
        anchor: str | None = None,
        max_chars: int = DEFAULT_MAX_CHARS,
    ) -> dict[str, Any]:
        doc = self.resolve_doc(identifier)
        sections = self.sections(doc)
        selected = sections[0]
        if heading or anchor:
            wanted_heading = heading.lower().strip() if heading else None
            wanted_anchor = normalize_anchor(anchor or heading or "")
            matches = [
                section
                for section in sections
                if (wanted_heading and section.heading.lower() == wanted_heading)
                or (
                    wanted_anchor
                    and (
                        section.heading_anchor == wanted_anchor
                        or section.heading_anchor.endswith(f"-{wanted_anchor}")
                    )
                )
            ]
            if not matches:
                raise DocsError(
                    f"Section not found in {doc.doc_id}: {heading or anchor}",
                    code=-32002,
                    data={"doc_id": doc.doc_id, "section": heading or anchor},
                )
            selected = matches[0]
        text = truncate_text(selected.text, max_chars)
        return {
            "document": doc.metadata(),
            "citation": selected.citation(),
            "text": text,
            "truncated": len(text) < len(selected.text),
            "headings": [
                {
                    "heading": section.heading,
                    "heading_anchor": section.heading_anchor,
                    "level": section.level,
                    "line_start": section.line_start,
                }
                for section in sections
                if section.level > 0
            ],
        }

    def search(
        self,
        query: str,
        *,
        status: str | None = None,
        group: str | None = None,
        max_results: int = 8,
    ) -> dict[str, Any]:
        query = query.strip()
        if not query:
            raise DocsError("Search query is required.")
        max_results = max(1, min(max_results, MAX_SEARCH_RESULTS))
        tokens = set(tokenize(query))
        scored: list[tuple[float, Section, str]] = []

        for doc in self.list_docs(status=status, group=group):
            for section in self.sections(doc):
                if section.level == 0:
                    continue
                score = score_section(query, tokens, section)
                if score <= 0:
                    continue
                scored.append((score, section, make_snippet(section.text, tokens)))

        scored.sort(key=lambda item: (-item[0], item[1].doc.order, item[1].line_start))
        results = [
            {
                "score": round(score, 3),
                "citation": section.citation(),
                "snippet": snippet,
                "resource_uri": section.doc.uri,
            }
            for score, section, snippet in scored[:max_results]
        ]
        return {
            "query": query,
            "result_count": len(results),
            "results": results,
            "note": "Read-only lexical search over canonical repo docs; use haven_docs_read for full sections.",
        }

    def resources(self) -> list[dict[str, Any]]:
        resources = [
            {
                "uri": "haven-docs://catalog/book",
                "name": "book_catalog.json",
                "title": "Book Catalog",
                "description": "Machine-readable CellProtocol Book catalog.",
                "mimeType": "application/json",
                "annotations": {"audience": ["assistant"], "priority": 1.0},
            }
        ]
        for doc in self.docs:
            resources.append(
                {
                    "uri": doc.uri,
                    "name": doc.doc_id,
                    "title": doc.title,
                    "description": f"{doc.path} ({doc.group}, {doc.status})",
                    "mimeType": doc.mime_type,
                    "annotations": {"audience": ["user", "assistant"], "priority": 0.85},
                }
            )
        return resources

    def read_resource(self, uri: str) -> dict[str, Any]:
        parsed = urlparse(uri)
        if parsed.scheme != "haven-docs":
            raise DocsError("Unsupported resource URI scheme.", code=-32002, data={"uri": uri})
        if parsed.netloc == "catalog" and parsed.path == "/book":
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(self.catalog, indent=2, ensure_ascii=False),
                    }
                ]
            }
        if parsed.netloc == "book":
            doc_id = unquote(parsed.path.lstrip("/"))
            result = self.read_section(doc_id, anchor=parsed.fragment or None, max_chars=0)
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": result["document"]["mimeType"],
                        "text": result["text"],
                    }
                ]
            }
        raise DocsError("Resource not found.", code=-32002, data={"uri": uri})


def truncate_text(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 32)].rstrip() + "\n\n[truncated]"


def score_section(query: str, tokens: set[str], section: Section) -> float:
    haystack = f"{section.doc.title}\n{section.heading}\n{section.doc.path}\n{section.text}".lower()
    heading_haystack = f"{section.doc.title} {section.heading} {section.doc.path}".lower()
    score = 0.0
    phrase = query.lower()
    if phrase in heading_haystack:
        score += 12.0
    elif phrase in haystack:
        score += 6.0
    for token in tokens:
        if token in heading_haystack:
            score += 4.0
        count = haystack.count(token)
        score += min(count, 6) * 0.75
    if section.doc.status == "active":
        score += 0.2
    return score


def make_snippet(text: str, tokens: set[str], size: int = 420) -> str:
    clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in clean_lines:
        lower = line.lower()
        if any(token in lower for token in tokens):
            return truncate_text(line, size)
    return truncate_text(" ".join(clean_lines[:3]), size)


def tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "haven_docs_list",
            "title": "List HAVEN Docs",
            "description": "List canonical HAVEN CellProtocol documentation records from book_catalog.json and entrypoint docs.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Optional status filter such as active or draft."},
                    "group": {"type": "string", "description": "Optional catalog group filter."},
                    "audience": {"type": "string", "description": "Optional audience filter: human, assistant, or both."},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "haven_docs_search",
            "title": "Search HAVEN Docs",
            "description": "Read-only lexical search across canonical HAVEN documentation sections with citations.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query, symbol, endpoint, keypath, or topic."},
                    "status": {"type": "string", "description": "Optional status filter such as active or draft."},
                    "group": {"type": "string", "description": "Optional catalog group filter."},
                    "max_results": {"type": "integer", "minimum": 1, "maximum": MAX_SEARCH_RESULTS},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
        {
            "name": "haven_docs_read",
            "title": "Read HAVEN Doc",
            "description": "Read a canonical doc or a specific heading section by doc_id, slug, path, or haven-docs URI.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "identifier": {"type": "string", "description": "doc_id, slug, path, or haven-docs://book/{doc_id} URI."},
                    "heading": {"type": "string", "description": "Optional exact heading title."},
                    "heading_anchor": {"type": "string", "description": "Optional normalized heading anchor."},
                    "max_chars": {"type": "integer", "minimum": 0, "maximum": 200000},
                },
                "required": ["identifier"],
                "additionalProperties": False,
            },
        },
        {
            "name": "haven_docs_resolve",
            "title": "Resolve HAVEN Doc Target",
            "description": "Resolve a symbol, endpoint, keypath, slug, or path to likely canonical docs.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Symbol, endpoint, keypath, slug, path, or topic to resolve."},
                    "max_results": {"type": "integer", "minimum": 1, "maximum": MAX_SEARCH_RESULTS},
                },
                "required": ["target"],
                "additionalProperties": False,
            },
        },
    ]


def prompt_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "haven_docs_lookup_before_answering",
            "title": "Lookup HAVEN Docs Before Answering",
            "description": "Static reading path for grounding a HAVEN/CellProtocol answer in canonical docs before responding.",
            "arguments": [
                {"name": "question", "description": "The user question or implementation task.", "required": True},
                {"name": "status", "description": "Optional doc status filter, usually active.", "required": False},
            ],
        },
        {
            "name": "cellprotocol_implement_cell",
            "title": "Implement A Cell From Docs",
            "description": "Static reading path and constraints for implementing or changing a Cell.",
            "arguments": [
                {"name": "task", "description": "The Cell implementation task.", "required": True},
            ],
        },
        {
            "name": "cellprotocol_author_skeleton_from_explore",
            "title": "Author Skeleton From Explore",
            "description": "Static reading path for authoring skeleton UI from Explore contracts.",
            "arguments": [
                {"name": "task", "description": "The skeleton authoring task.", "required": True},
            ],
        },
    ]


def validate_args(args: dict[str, Any], allowed: set[str]) -> None:
    unknown = set(args) - allowed
    if unknown:
        raise DocsError(f"Unknown argument(s): {', '.join(sorted(unknown))}")


def call_tool(index: DocsIndex, name: str, args: dict[str, Any] | None) -> dict[str, Any]:
    args = args or {}
    try:
        if not isinstance(args, dict):
            raise DocsError("Tool arguments must be an object.")
        if name == "haven_docs_list":
            validate_args(args, {"status", "group", "audience"})
            docs = [
                doc.metadata()
                for doc in index.list_docs(
                    status=args.get("status"),
                    group=args.get("group"),
                    audience=args.get("audience"),
                )
            ]
            structured = {"documents": docs, "count": len(docs)}
            return tool_success(structured, f"Listed {len(docs)} HAVEN documentation records.")

        if name == "haven_docs_search":
            validate_args(args, {"query", "status", "group", "max_results"})
            structured = index.search(
                required_string(args, "query"),
                status=args.get("status"),
                group=args.get("group"),
                max_results=bounded_int(args.get("max_results", 8), "max_results", 1, MAX_SEARCH_RESULTS),
            )
            return tool_success(structured, format_search_text(structured))

        if name == "haven_docs_read":
            validate_args(args, {"identifier", "heading", "heading_anchor", "max_chars"})
            structured = index.read_section(
                required_string(args, "identifier"),
                heading=args.get("heading"),
                anchor=args.get("heading_anchor"),
                max_chars=bounded_int(args.get("max_chars", DEFAULT_MAX_CHARS), "max_chars", 0, 200000),
            )
            text = f"{structured['citation']['path']}#{structured['citation']['heading_anchor']}\n\n{structured['text']}"
            return tool_success(structured, text)

        if name == "haven_docs_resolve":
            validate_args(args, {"target", "max_results"})
            target = required_string(args, "target")
            try:
                doc = index.resolve_doc(target)
                structured = {"target": target, "exact": doc.metadata(), "results": []}
                return tool_success(structured, f"Resolved exactly: {doc.path}")
            except DocsError:
                structured = index.search(
                    target,
                    max_results=bounded_int(args.get("max_results", 5), "max_results", 1, MAX_SEARCH_RESULTS),
                )
                return tool_success(structured, format_search_text(structured))

        raise DocsError(f"Unknown tool: {name}")
    except DocsError as error:
        return {
            "content": [{"type": "text", "text": error.message}],
            "isError": True,
            "structuredContent": {"error": error.message, "data": error.data},
        }


def required_string(args: dict[str, Any], key: str) -> str:
    value = args.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DocsError(f"Required string argument missing: {key}")
    return value.strip()


def bounded_int(value: Any, key: str, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise DocsError(f"Argument must be an integer: {key}")
    if number < minimum or number > maximum:
        raise DocsError(f"Argument out of range: {key}", data={"minimum": minimum, "maximum": maximum})
    return number


def tool_success(structured: dict[str, Any], text: str) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": text}],
        "structuredContent": structured,
        "isError": False,
    }


def format_search_text(structured: dict[str, Any]) -> str:
    if not structured["results"]:
        return f"No HAVEN docs matches for: {structured['query']}"
    lines = [f"Matches for: {structured['query']}"]
    for item in structured["results"]:
        citation = item["citation"]
        anchor = citation["heading_anchor"]
        suffix = f"#{anchor}" if anchor else ""
        lines.append(f"- {citation['path']}{suffix}: {citation['heading']} - {item['snippet']}")
    return "\n".join(lines)


def get_prompt(name: str, args: dict[str, Any] | None) -> dict[str, Any]:
    args = args or {}
    if not isinstance(args, dict):
        raise DocsError("Prompt arguments must be an object.")
    if name == "haven_docs_lookup_before_answering":
        question = required_string(args, "question")
        status = args.get("status", "active")
        prompt = (
            "Before answering, use haven_docs_search with the user question, then "
            "use haven_docs_read for the most relevant canonical sections. Keep "
            "validated documentation facts separate from assumptions. Cite doc "
            "paths and headings. This is a lookup workflow, not a model-adaptive "
            "RAG prompt package; use RAGPromptTransformerCell for that. Status "
            f"filter: {status}.\n\nQuestion:\n{question}"
        )
        return prompt_result("Ground the answer in HAVEN docs.", prompt)
    if name == "cellprotocol_implement_cell":
        task = required_string(args, "task")
        prompt = (
            "Use this reading path before implementation: Book/10_Quickstart.md, "
            "Book/11_Developer_Guide_Cell.md, Book/13_Agent_Instructions.md, and "
            "Book/22_Explore_Contracts_For_Skeleton_Authoring.md. Inspect code "
            "before changing behavior, keep docs aligned, and treat missing "
            "Explore contracts as contract work.\n\nTask:\n" + task
        )
        return prompt_result("Implement Cell with canonical docs.", prompt)
    if name == "cellprotocol_author_skeleton_from_explore":
        task = required_string(args, "task")
        prompt = (
            "Use Book/12_Skeleton_Spec.md and "
            "Book/22_Explore_Contracts_For_Skeleton_Authoring.md before authoring. "
            "Generate only bindings backed by complete Explore manifests, run the "
            "skeleton validator, and preserve owner/entity access affordances.\n\nTask:\n"
            + task
        )
        return prompt_result("Author skeleton from Explore contracts.", prompt)
    raise DocsError(f"Unknown prompt: {name}")


def prompt_result(description: str, text: str) -> dict[str, Any]:
    return {
        "description": description,
        "messages": [
            {
                "role": "user",
                "content": {"type": "text", "text": text},
            }
        ],
    }


def resource_templates() -> list[dict[str, Any]]:
    return [
        {
            "uriTemplate": "haven-docs://book/{doc_id}",
            "name": "HAVEN Book Document",
            "title": "HAVEN Book Document",
            "description": "Read a canonical Book markdown document by doc_id.",
            "mimeType": "text/markdown",
        },
        {
            "uriTemplate": "haven-docs://book/{doc_id}#{heading_anchor}",
            "name": "HAVEN Book Section",
            "title": "HAVEN Book Section",
            "description": "Read a canonical Book markdown section by doc_id and heading anchor.",
            "mimeType": "text/markdown",
        },
    ]


class MCPServer:
    def __init__(self) -> None:
        self.index = DocsIndex()

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        message_id = message.get("id")
        params = message.get("params") or {}
        if not isinstance(params, dict):
            return error_response(message_id, -32602, "Params must be an object.")

        try:
            if method == "initialize":
                return response(message_id, self.initialize(params))
            if method == "notifications/initialized":
                return None
            if method == "ping":
                return response(message_id, {})
            if method == "resources/list":
                return response(message_id, {"resources": self.index.resources()})
            if method == "resources/read":
                return response(message_id, self.index.read_resource(required_string(params, "uri")))
            if method == "resources/templates/list":
                return response(message_id, {"resourceTemplates": resource_templates()})
            if method == "tools/list":
                return response(message_id, {"tools": tool_definitions()})
            if method == "tools/call":
                return response(
                    message_id,
                    call_tool(self.index, required_string(params, "name"), params.get("arguments") or {}),
                )
            if method == "prompts/list":
                return response(message_id, {"prompts": prompt_definitions()})
            if method == "prompts/get":
                return response(
                    message_id,
                    get_prompt(required_string(params, "name"), params.get("arguments") or {}),
                )
            return error_response(message_id, -32601, f"Method not found: {method}")
        except DocsError as error:
            return error_response(message_id, error.code, error.message, error.data)
        except Exception as error:  # pragma: no cover - final guard for MCP clients
            return error_response(message_id, -32603, "Internal server error.", {"detail": str(error)})

    def initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        requested = params.get("protocolVersion")
        protocol_version = requested if requested in SUPPORTED_PROTOCOL_VERSIONS else SUPPORTED_PROTOCOL_VERSIONS[0]
        return {
            "protocolVersion": protocol_version,
            "capabilities": {
                "resources": {"listChanged": False},
                "tools": {"listChanged": False},
                "prompts": {"listChanged": False},
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "title": SERVER_TITLE,
                "version": SERVER_VERSION,
                "description": "Read-only lookup over HAVEN CellProtocolDocuments canonical docs.",
            },
            "instructions": (
                "Use resources for canonical markdown/JSON, tools for read-only lookup, "
                "and prompts for HAVEN documentation workflows. This server does not mutate files."
            ),
        }


def response(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def error_response(message_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": message_id, "error": error}


def run_stdio() -> int:
    server = MCPServer()
    for raw_line in sys.stdin.buffer:
        line = raw_line.decode("utf-8").strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as error:
            write_message(error_response(None, -32700, "Parse error.", {"detail": str(error)}))
            continue
        messages = payload if isinstance(payload, list) else [payload]
        replies = []
        for message in messages:
            if not isinstance(message, dict):
                replies.append(error_response(None, -32600, "Invalid request."))
                continue
            reply = server.handle(message)
            if reply is not None:
                replies.append(reply)
        if isinstance(payload, list):
            if replies:
                write_message(replies)
        elif replies:
            write_message(replies[0])
    return 0


def write_message(message: Any) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only HAVEN Docs MCP server.")
    parser.add_argument("--list-tools", action="store_true", help="Print tool definitions as JSON and exit.")
    parser.add_argument("--list-resources", action="store_true", help="Print resources as JSON and exit.")
    parser.add_argument("--search", help="Run local search once and exit.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    server = MCPServer()
    if args.list_tools:
        print(json.dumps(tool_definitions(), indent=2, ensure_ascii=False))
        return 0
    if args.list_resources:
        print(json.dumps(server.index.resources(), indent=2, ensure_ascii=False))
        return 0
    if args.search:
        print(json.dumps(server.index.search(args.search), indent=2, ensure_ascii=False))
        return 0
    return run_stdio()


if __name__ == "__main__":
    raise SystemExit(main())
