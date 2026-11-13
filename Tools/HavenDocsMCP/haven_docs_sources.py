"""PROTOTYPE (forslag, ikke vedtatt): ekstra kildetyper, implementation_status og ferskhet.

Utvider haven_docs_mcp.py uten å erstatte Book-kontrakten (Book/15). Alt er av
som standard og slås på med --with-sources eller HAVEN_DOCS_WITH_SOURCES=1.
Kun standardbiblioteket. Skriver aldri til noen repo; git kalles bare lesende
(rev-parse, rev-list, log, status, ls-remote).
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

IMPLEMENTATION_STATUSES = ("implemented", "decided", "proposal", "mixed", "unknown")
STATUS_BASES = ("code-verified", "doc-self-declared", "unverified")
CONFIG_PATH = Path(__file__).with_name("sources.json")
GIT_TIMEOUT_SECONDS = 8
MAX_FILE_BYTES = 512 * 1024
STALE_FETCH_SECONDS = 24 * 3600

SECTION_MARKER = re.compile(r"<!--\s*haven:implementation_status\s*=\s*([a-z]+)\s*-->")
NOT_IMPLEMENTED_PHRASES = re.compile(
    r"ikke implementert|ikke bygget|ingen swift-implementasjon|ennå ikke implementert"
    r"|not implemented|not yet implemented|no implementation",
    re.IGNORECASE,
)
# Filer som ser ut som korrespondanse og må vurderes av et menneske før de indekseres.
CORRESPONDENCE_HINT = re.compile(r"correspond|korrespond|epost|e-post|inbox", re.IGNORECASE)


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or CONFIG_PATH
    if not config_path.is_file():
        return {"sources": [], "exclude_global": [], "status_overrides": []}
    return json.loads(config_path.read_text(encoding="utf-8"))


def normalize_status(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text if text in IMPLEMENTATION_STATUSES else "unknown"


def normalize_basis(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text if text in STATUS_BASES else "unverified"


# --- git (kun lesing) -------------------------------------------------------


def git(root: Path, *args: str, timeout: int = GIT_TIMEOUT_SECONDS) -> str | None:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0")
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    return done.stdout.strip()


def main_checkout_parent(repo_root: Path) -> Path | None:
    """Mappen som inneholder hovedklonen, også når vi kjører fra en worktree."""
    common = git(repo_root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not common:
        return None
    return Path(common).parent.parent


def resolve_root(source: dict[str, Any], repo_root: Path) -> Path | None:
    if source.get("root"):
        candidate = Path(os.path.expanduser(source["root"]))
        return candidate if candidate.is_dir() else None
    env_name = source.get("root_env")
    if env_name and os.environ.get(env_name):
        candidate = Path(os.path.expanduser(os.environ[env_name]))
        return candidate if candidate.is_dir() else None
    bases = [repo_root.parent]
    main_parent = main_checkout_parent(repo_root)
    if main_parent and main_parent not in bases:
        bases.append(main_parent)
    for base in bases:
        candidate = base / source["repo"]
        if candidate.is_dir():
            return candidate
    return None


_freshness_cache: dict[tuple[Any, ...], tuple[float, dict[str, Any]]] = {}
_provenance_cache: dict[tuple[str, str, str], dict[str, Any]] = {}


def provenance(root: Path, rel_path: str) -> dict[str, Any]:
    """Commit-hash og dato for sist endring av én fil, pluss om den er lokalt endret."""
    head = git(root, "rev-parse", "HEAD") or ""
    key = (str(root), rel_path, head)
    if key in _provenance_cache:
        return _provenance_cache[key]
    log = git(root, "log", "-1", "--format=%H%x1f%cI", "--", rel_path)
    result: dict[str, Any] = {"tracked": False, "commit": None, "commit_short": None, "committed_at": None}
    if log and "\x1f" in log:
        commit, committed_at = log.split("\x1f", 1)
        result.update(tracked=True, commit=commit, commit_short=commit[:7], committed_at=committed_at)
    dirty = git(root, "status", "--porcelain", "--", rel_path)
    result["dirty"] = bool(dirty)
    result["age_days"] = age_days(result["committed_at"])
    _provenance_cache[key] = result
    return result


def age_days(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        from datetime import datetime, timezone

        moment = datetime.fromisoformat(iso)
        return max(0, (datetime.now(timezone.utc) - moment).days)
    except ValueError:
        return None


def freshness(
    root: Path,
    *,
    label: str,
    base_ref: str = "origin/main",
    expected_branch: str = "main",
    check_remote: bool = False,
) -> dict[str, Any]:
    """Hvor langt klonen ligger bak. Uten nettverk bruker vi den lokale refen og sier fra om hvor gammel den er."""
    key = (str(root), base_ref, expected_branch, check_remote)
    cached = _freshness_cache.get(key)
    if cached and time.time() - cached[0] < 30:
        return cached[1]

    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    head = git(root, "rev-parse", "HEAD")
    info: dict[str, Any] = {
        "source": label,
        "root": str(root),
        "branch": branch,
        "head": head[:7] if head else None,
        "head_committed_at": git(root, "log", "-1", "--format=%cI") if head else None,
        "base_ref": base_ref,
        "behind": None,
        "ahead": None,
        "last_fetch": None,
        "remote_checked": False,
        "remote_has_unfetched_commits": None,
        "warnings": [],
    }
    warnings: list[str] = info["warnings"]
    if head is None:
        warnings.append(f"{label}: git ikke tilgjengelig eller ikke et repo; ferskhet kan ikke vurderes.")
        info["summary"] = warnings[0]
        return info

    counts = git(root, "rev-list", "--left-right", "--count", f"HEAD...{base_ref}")
    if counts:
        ahead, behind = counts.split()
        info["ahead"], info["behind"] = int(ahead), int(behind)
    else:
        warnings.append(f"{label}: fant ikke {base_ref} lokalt.")

    common = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if common:
        fetch_head = Path(common) / "FETCH_HEAD"
        if fetch_head.exists():
            fetched = fetch_head.stat().st_mtime
            info["last_fetch"] = time.strftime("%Y-%m-%d", time.localtime(fetched))
            if time.time() - fetched > STALE_FETCH_SECONDS:
                warnings.append(
                    f"{label}: {base_ref} ble sist hentet {info['last_fetch']}; tallet bak kan være utdatert "
                    "(kjør git fetch, eller bruk --check-remote)."
                )
        else:
            warnings.append(f"{label}: ingen registrert git fetch; {base_ref} kan være utdatert.")

    if check_remote:
        remote_branch = base_ref.split("/", 1)[1] if "/" in base_ref else base_ref
        out = git(root, "ls-remote", "origin", f"refs/heads/{remote_branch}")
        remote_sha = out.split()[0] if out else None
        if remote_sha:
            info["remote_checked"] = True
            local_sha = git(root, "rev-parse", base_ref)
            if remote_sha == local_sha:
                info["remote_has_unfetched_commits"] = False
            elif git(root, "cat-file", "-e", f"{remote_sha}^{{commit}}") is not None:
                info["remote_has_unfetched_commits"] = False
                real_behind = git(root, "rev-list", "--count", f"HEAD..{remote_sha}")
                if real_behind is not None:
                    info["behind"] = int(real_behind)
            else:
                info["remote_has_unfetched_commits"] = True
                warnings.append(
                    f"{label}: origin/{remote_branch} har commits som ikke er hentet lokalt; klonen ligger bak "
                    "med et ukjent antall (kjør git fetch)."
                )
        else:
            warnings.append(f"{label}: kunne ikke nå origin for sjekk av {base_ref}.")

    if branch and branch != expected_branch:
        warnings.append(f"{label}: klonen står på gren {branch}, ikke {expected_branch}; svaret gjenspeiler grenen.")
    if info["behind"]:
        warnings.append(f"{label}: klonen er {info['behind']} commits bak {base_ref}.")

    info["summary"] = summarize_freshness(info)
    _freshness_cache[key] = (time.time(), info)
    return info


def summarize_freshness(info: dict[str, Any]) -> str:
    if info.get("head") is None:
        return info["warnings"][0] if info.get("warnings") else f"{info['source']}: ukjent ferskhet."
    behind = info.get("behind")
    position = "ukjent avstand til" if behind is None else ("à jour med" if behind == 0 else f"{behind} commits bak")
    parts = [f"{info['source']}: {info['branch']}@{info['head']} er {position} {info['base_ref']}"]
    if info.get("last_fetch"):
        parts.append(f"ref sist hentet {info['last_fetch']}")
    if info.get("remote_checked"):
        parts.append("sjekket mot origin nå")
    suffix = "; ".join(parts)
    problems = info["warnings"]
    return suffix + (" ⚠ " + " | ".join(w.split(": ", 1)[-1] for w in problems) if problems else "")


# --- oppdagelse -------------------------------------------------------------


def excluded(rel: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(rel, pattern):
            return True
        if pattern.startswith("**/") and fnmatch.fnmatch(rel, pattern[3:]):
            return True
    return False


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if match:
            data[match.group(1)] = match.group(2).strip("\"'")
    return data


def title_for(path: Path, text: str, front: dict[str, str]) -> str:
    if front.get("title"):
        return front["title"]
    if path.suffix == ".json":
        try:
            value = json.loads(text).get("title")
            if isinstance(value, str) and value:
                return value
        except (ValueError, AttributeError):
            pass
        return path.name
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.name


def override_for(overrides: list[dict[str, Any]], source_id: str, rel: str) -> dict[str, Any] | None:
    for item in overrides:
        if item.get("source") == source_id and rel in item.get("paths", []):
            return item
    return None


def discover_docs(config: dict[str, Any], repo_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    docs: list[dict[str, Any]] = []
    reports: list[dict[str, Any]] = []
    global_exclude = list(config.get("exclude_global", []))
    overrides = list(config.get("status_overrides", []))
    for source in config.get("sources", []):
        source_id = source["id"]
        report: dict[str, Any] = {"source": source_id, "repo": source["repo"], "root": None, "indexed": 0, "skipped": {}}
        reports.append(report)
        root = resolve_root(source, repo_root)
        if root is None:
            report["error"] = f"fant ikke {source['repo']} lokalt (sett {source.get('root_env', 'root')})."
            continue
        report["root"] = str(root)
        exclude = global_exclude + list(source.get("exclude", []))
        seen: set[str] = set()
        for pattern in source.get("include", []):
            for path in sorted(root.glob(pattern)):
                if not path.is_file():
                    continue
                rel = path.relative_to(root).as_posix()
                if rel in seen:
                    continue
                seen.add(rel)
                reason = skip_reason(path, rel, exclude)
                if reason:
                    report["skipped"][reason] = report["skipped"].get(reason, 0) + 1
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                front = parse_frontmatter(text)
                if front.get("index", "").lower() == "false" or "haven:index=false" in text[:400]:
                    report["skipped"]["index=false"] = report["skipped"].get("index=false", 0) + 1
                    continue
                docs.append(build_doc(source, source_id, root, rel, path, text, front, overrides))
                report["indexed"] += 1
    return docs, reports


def skip_reason(path: Path, rel: str, exclude: list[str]) -> str | None:
    if excluded(rel, exclude):
        return "exclude-glob"
    if path.stat().st_size > MAX_FILE_BYTES:
        return "for-stor"
    return None


def build_doc(
    source: dict[str, Any],
    source_id: str,
    root: Path,
    rel: str,
    path: Path,
    text: str,
    front: dict[str, str],
    overrides: list[dict[str, Any]],
) -> dict[str, Any]:
    override = override_for(overrides, source_id, rel)
    if front.get("implementation_status"):
        status = normalize_status(front["implementation_status"])
        basis = normalize_basis(front.get("status_basis"))
    elif override:
        status = normalize_status(override.get("implementation_status"))
        basis = normalize_basis(override.get("status_basis"))
    else:
        status, basis = "unknown", "unverified"
    is_json = path.suffix == ".json"
    return {
        "doc_id": f"{source_id}/{rel}",
        "title": title_for(path, text, front),
        "path": rel,
        "slug": f"{source_id}/{rel}",
        "group": source.get("group", source_id),
        "audience": "both",
        "status": front.get("status", "unlabeled"),
        "order": 1000,
        "mime_type": "application/json" if is_json else "text/markdown",
        "source": source_id,
        "root": str(root),
        "implementation_status": status,
        "status_basis": basis,
        "owner": front.get("owner", source.get("owner", "")),
        "last_verified": front.get("last_verified", ""),
    }


# --- lint -------------------------------------------------------------------


def lint(index: Any) -> dict[str, Any]:
    """Heuristikk, ikke bevis: finner motsigelser mellom etikett og tekst, og filer som bør vurderes manuelt."""
    conflicts: list[dict[str, Any]] = []
    unlabeled_hits: list[dict[str, Any]] = []
    invalid: list[str] = []
    review_candidates: list[str] = []
    counts: dict[str, int] = {}
    for doc in index.docs:
        counts[doc.implementation_status] = counts.get(doc.implementation_status, 0) + 1
        if doc.source != "book" and CORRESPONDENCE_HINT.search(doc.path):
            review_candidates.append(f"{doc.source}:{doc.path}")
        for section in index.sections(doc):
            if section.level == 0 and len(index.sections(doc)) > 1:
                continue
            effective = section.implementation_status or doc.implementation_status
            hits = [
                line_no
                for line_no, line in enumerate(section.text.splitlines(), start=section.line_start)
                if NOT_IMPLEMENTED_PHRASES.search(line)
            ]
            if not hits:
                continue
            entry = {
                "doc_id": doc.doc_id,
                "heading": section.heading,
                "line": hits[0],
                "effective_status": effective,
            }
            if effective == "implemented":
                conflicts.append(entry)
            elif effective in ("unknown", "mixed"):
                unlabeled_hits.append(entry)
    return {
        "counts_by_implementation_status": counts,
        "conflicts_label_says_implemented_text_says_not": conflicts,
        "text_says_not_implemented_but_unlabeled": unlabeled_hits[:40],
        "text_says_not_implemented_but_unlabeled_total": len(unlabeled_hits),
        "review_before_indexing": review_candidates,
        "note": "Regexbasert. Treff er arbeidsliste for eier, ikke dom.",
    }
