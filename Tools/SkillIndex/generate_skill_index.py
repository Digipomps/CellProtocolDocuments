#!/usr/bin/env python3
"""PROTOTYPE (forslag, ikke vedtatt): generert indeks over skills.

Leser skill-mapper på ett eller flere steder og skriver SKILLS.md og skills_index.json.
Endrer aldri en skill-fil. Kun standardbiblioteket. Ingen absolutte hjemmestier i
utdata (hjemmemappen vises som ~). Utdata er deterministisk, så --check kan brukes
som drift-sjekk.

  python3 Tools/SkillIndex/generate_skill_index.py --out Tools/SkillIndex
  python3 Tools/SkillIndex/generate_skill_index.py --check Tools/SkillIndex
  python3 Tools/SkillIndex/generate_skill_index.py --root min=/sti/til/skills --no-defaults
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

HOME = Path.home()
SKILL_FILE_NAMES = ("SKILL.md", "Skill.md", "skill.md")
DEFAULT_ROOTS = {
    "user": HOME / ".claude/skills",
    "scaffold": HOME / "GitHub/CellScaffold/.claude/skills",
    "tilinfo": HOME / "ClaudesFiles/TilInfo/haven-skills",
    "codex": HOME / ".codex/skills",
    "cpdocs": HOME / "GitHub/CellProtocolDocuments/.claude/skills",
}
WORKSPACE_GLOB = (HOME / "GitHub", "CellScaffold-*/.claude/skills")
DESC_LIST_LIMIT = 1536  # skillListingMaxDescChars, standardverdi oppgitt av Vegar
STOPWORDS = set(
    "this that with from have will your their when use used using into also such than then "
    "they them been being which where while about after before only over under more most "
    "other each both does done make made need needs task tasks work works file files skill "
    "skills should would could must like for the and not any all are but can its has was were "
    "who how why what one two".split()
)
OVERLAP_THRESHOLD = 0.12
OVERLAP_MAX_PAIRS = 15


def display_path(path: Path) -> str:
    text = str(path)
    home = str(HOME)
    return "~" + text[len(home):] if text.startswith(home) else text


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    data: dict[str, str] = {}
    current = None
    for line in text[3:end].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            current = match.group(1)
            value = match.group(2).strip()
            data[current] = "" if value in (">", ">-", "|", "|-") else value.strip("\"'")
        elif current and line.startswith((" ", "\t")):
            data[current] = (data[current] + " " + line.strip()).strip()
    return data, text[end + 4 :]


def dir_hash(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.name != ".DS_Store":
            digest.update(str(path.relative_to(directory)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()[:10]


def last_changed(directory: Path) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", str(directory), "log", "-1", "--format=%cs", "--", "."],
            capture_output=True, text=True, timeout=10,
        )
        if done.returncode == 0 and done.stdout.strip():
            return done.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    newest = max((p.stat().st_mtime for p in directory.rglob("*") if p.is_file()), default=0)
    return "mtime:" + datetime.fromtimestamp(newest).strftime("%Y-%m-%d") if newest else "ukjent"


def first_sentence(text: str, limit: int = 150) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    cut = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    return cut if len(cut) <= limit else cut[: limit - 1].rstrip() + "…"


def scan(roots: dict[str, Path]) -> dict[str, dict[str, dict[str, Any]]]:
    found: dict[str, dict[str, dict[str, Any]]] = {}
    for label, root in roots.items():
        if not root.is_dir():
            continue
        for directory in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
            skill_file = next((directory / n for n in SKILL_FILE_NAMES if (directory / n).exists()), None)
            record: dict[str, Any] = {"path": display_path(directory), "hash": dir_hash(directory), "problems": []}
            if skill_file is None:
                record["problems"].append("mangler SKILL.md")
            else:
                text = skill_file.read_text(encoding="utf-8", errors="replace")
                front, body = parse_frontmatter(text)
                if front is None:
                    record["problems"].append("mangler frontmatter")
                else:
                    if front.get("name") != directory.name:
                        record["problems"].append(f"name={front.get('name')!r} er ikke mappenavnet")
                    if not front.get("description"):
                        record["problems"].append("mangler description")
                description = (front or {}).get("description", "")
                if len(description) > DESC_LIST_LIMIT:
                    record["problems"].append(f"description {len(description)} tegn > {DESC_LIST_LIMIT}")
                record["description"] = description
                record["desc_len"] = len(description)
                record["body_lines"] = body.count("\n")
                record["references"] = sum(1 for p in (directory / "references").rglob("*") if p.is_file()) if (directory / "references").is_dir() else 0
                record["hardcoded_user_paths"] = len(re.findall(r"/Users/[A-Za-z0-9_.-]+/", text))
                record["last_changed"] = last_changed(directory)
            found.setdefault(directory.name, {})[label] = record
    return found


def terms(description: str) -> set[str]:
    words = re.findall(r"[a-zæøå][a-zæøå0-9_-]{3,}", description.lower())
    return {w for w in words if w not in STOPWORDS}


def overlaps(skills: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    names = sorted(skills)
    out = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            ta, tb = skills[a]["_terms"], skills[b]["_terms"]
            if not ta or not tb:
                continue
            score = len(ta & tb) / len(ta | tb)
            if score >= OVERLAP_THRESHOLD:
                out.append({"a": a, "b": b, "score": round(score, 2), "shared": sorted(ta & tb)[:6]})
    return sorted(out, key=lambda x: (-x["score"], x["a"], x["b"]))[:OVERLAP_MAX_PAIRS]


def build(roots: dict[str, Path], budget_chars: int) -> dict[str, Any]:
    found = scan(roots)
    skills: dict[str, dict[str, Any]] = {}
    for name, per_root in sorted(found.items()):
        # Lengste beskrivelse er referansen for lengde/formål; alle varianter listes under "variants".
        described = {l: r for l, r in per_root.items() if r.get("description")}
        reference = max(described.values(), key=lambda r: r["desc_len"], default=None) if described else None
        groups: dict[str, list[str]] = {}
        for label, record in per_root.items():
            groups.setdefault(record["hash"], []).append(label)
        entry = {
            "name": name,
            "scopes": sorted(per_root),
            "purpose": first_sentence(reference["description"]) if reference else "",
            "desc_len": reference["desc_len"] if reference else 0,
            "variants": [{"hash": h, "scopes": sorted(ls)} for h, ls in sorted(groups.items())],
            "drift": len(groups) > 1,
            "last_changed": max((r.get("last_changed", "") for r in per_root.values()), default=""),
            "references": max((r.get("references", 0) for r in per_root.values()), default=0),
            "hardcoded_user_paths": max((r.get("hardcoded_user_paths", 0) for r in per_root.values()), default=0),
            "problems": sorted({f"{p} ({l})" for l, r in per_root.items() for p in r["problems"]}),
            "group": name.split("-", 1)[0] if "-" in name else "(uten prefiks)",
            "_terms": terms(reference["description"]) if reference else set(),
        }
        skills[name] = entry
    per_scope_chars = {
        label: sum(r.get("desc_len", 0) for per_root in found.values() for l, r in per_root.items() if l == label)
        for label in roots
    }
    ws = [l for l in roots if l.startswith("ws-")]
    combos = {f"user+{l}": per_scope_chars.get("user", 0) + per_scope_chars[l] for l in ws}
    pair_overlaps = overlaps(skills)
    for entry in skills.values():
        entry.pop("_terms")
    return {
        "roots": {label: display_path(path) for label, path in roots.items() if path.is_dir()},
        "counts": {
            "unique_names": len(skills),
            "with_drift": sum(1 for s in skills.values() if s["drift"]),
            "single_scope": sum(1 for s in skills.values() if len(s["scopes"]) == 1),
            "with_problems": sum(1 for s in skills.values() if s["problems"]),
        },
        "description_chars_per_scope": per_scope_chars,
        "listing_if_combined": combos,
        "listing_budget_chars": budget_chars,
        "overlap_candidates": pair_overlaps,
        "skills": list(skills.values()),
    }


def render_markdown(index: dict[str, Any]) -> str:
    c = index["counts"]
    lines = [
        "# Skill-indeks (generert, forslag)",
        "",
        "Generert av `Tools/SkillIndex/generate_skill_index.py`. Ikke rediger for hånd. Leser skill-mapper, endrer dem aldri.",
        "",
        f"- Unike navn: **{c['unique_names']}**. Med avvik mellom kopier: **{c['with_drift']}**. Bare ett sted: **{c['single_scope']}**. Med problemer: **{c['with_problems']}**.",
        f"- Steder: {', '.join(f'`{l}`' for l in index['roots'])}.",
        "",
        "## Beskrivelsestegn per sted (det som havner i skill-listen)",
        "",
        "| Sted | Tegn |",
        "|---|---:|",
    ]
    for label, chars in index["description_chars_per_scope"].items():
        lines.append(f"| {label} | {chars} |")
    if index["listing_if_combined"]:
        lines += ["", "Brukerskills pluss én worktree i samme økt (kopier med samme navn telles to ganger):", "", "| Kombinasjon | Tegn |", "|---|---:|"]
        for label, chars in index["listing_if_combined"].items():
            lines.append(f"| {label} | {chars} |")
    lines += [
        "",
        f"Budsjettet i tegn er satt til {index['listing_budget_chars']} for denne rapporten (se forutsetning i forslaget).",
        "",
        "## Skills",
        "",
        "| Navn | Sted | Formål (første setning) | Tegn | Avvik | Sist endret |",
        "|---|---|---|---:|:-:|---|",
    ]
    for s in index["skills"]:
        scopes = ", ".join(s["scopes"]) if len(s["scopes"]) <= 3 else f"{len(s['scopes'])} steder"
        purpose = s["purpose"].replace("|", "\\|")
        lines.append(f"| `{s['name']}` | {scopes} | {purpose} | {s['desc_len']} | {'ja' if s['drift'] else ''} | {s['last_changed']} |")
    lines += ["", "## Avvik mellom kopier", ""]
    for s in index["skills"]:
        if s["drift"]:
            lines.append(f"- `{s['name']}`: " + " · ".join(f"{v['hash']} = {', '.join(v['scopes'])}" for v in s["variants"]))
    lines += ["", "## Mulig overlapp (heuristikk på ord i beskrivelsene, ikke dom)", ""]
    if index["overlap_candidates"]:
        for o in index["overlap_candidates"][:25]:
            lines.append(f"- `{o['a']}` ↔ `{o['b']}` ({o['score']}): {', '.join(o['shared'])}")
    else:
        lines.append("- Ingen over terskelen.")
    lines += ["", "## Problemer", ""]
    problem_lines = [f"- `{s['name']}`: {'; '.join(s['problems'])}" for s in index["skills"] if s["problems"]]
    hard = [f"- `{s['name']}`: {s['hardcoded_user_paths']} hardkodede /Users/…-stier" for s in index["skills"] if s["hardcoded_user_paths"]]
    lines += (problem_lines + hard) or ["- Ingen."]
    return "\n".join(lines) + "\n"


def collect_roots(args: argparse.Namespace) -> dict[str, Path]:
    roots: dict[str, Path] = {} if args.no_defaults else dict(DEFAULT_ROOTS)
    if not args.no_defaults:
        base, pattern = WORKSPACE_GLOB
        for path in sorted(base.glob(pattern)):
            roots["ws-" + path.parts[-3].replace("CellScaffold-", "")] = path
    for item in args.root or []:
        label, _, value = item.partition("=")
        if not value:
            raise SystemExit(f"--root forventer navn=sti, fikk {item!r}")
        roots[label] = Path(value).expanduser()
    return roots


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generer skill-indeks (forslag).")
    parser.add_argument("--root", action="append", metavar="NAVN=STI", help="Ekstra sted å skanne (kan gjentas).")
    parser.add_argument("--no-defaults", action="store_true", help="Skann bare stedene gitt med --root.")
    parser.add_argument("--budget-chars", type=int, default=8000, help="Antatt listebudsjett i tegn (standard ca. 1 %% av 200k tokens).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", metavar="MAPPE", help="Skriv SKILLS.md og skills_index.json hit.")
    group.add_argument("--check", metavar="MAPPE", help="Sammenlign med filer i mappen; exit 1 ved avvik.")
    args = parser.parse_args(argv)

    index = build(collect_roots(args), args.budget_chars)
    markdown = render_markdown(index)
    as_json = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "SKILLS.md").write_text(markdown, encoding="utf-8")
        (out / "skills_index.json").write_text(as_json, encoding="utf-8")
        print(f"Skrev {out/'SKILLS.md'} og {out/'skills_index.json'} ({index['counts']['unique_names']} skills).")
        return 0
    out = Path(args.check)
    stale = [n for n, text in (("SKILLS.md", markdown), ("skills_index.json", as_json)) if not (out / n).exists() or (out / n).read_text(encoding="utf-8") != text]
    if stale:
        print("Indeksen er utdatert: " + ", ".join(stale), file=sys.stderr)
        return 1
    print("Indeksen er à jour.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
