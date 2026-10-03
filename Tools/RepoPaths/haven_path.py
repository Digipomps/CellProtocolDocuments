#!/usr/bin/env python3
"""
haven_path.py -- turn `Repo::relative/path` into one precise absolute path.

The whole purpose, and nothing else: a reference written in a document must
resolve to an unambiguous full path on any machine, whatever the developer
called their folders or wherever they put them. Repo structure is identical for
everyone; repo *placement* is a device setting.

    CellProtocolDocuments::Book/23_Purpose_Knowledge_Base.md
        -> /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/23_…
        -> /home/dev/src/haven-docs/Book/23_…            on another machine
        -> /sessions/…/mnt/HAVEN/CellProtocolDocuments/Book/23_…   in the VM

Device file: $HAVEN_REPOS, else ~/.haven/repos.json. `init` writes it by looking
at what is actually on the machine, so nobody hand-maintains a list.

    haven_path.py init [ROOT]        write the device file from what is there
    haven_path.py path REF           print the absolute path (or fail, loudly)
    haven_path.py check              every declared repo resolves and is itself
    haven_path.py scan FILE...       every Repo::path reference in these files

Failure is never a guess. No search, no fallback to a sibling, no cwd. A
reference that cannot be resolved names the repo and the reason, and exits
non-zero.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCHEMA = "haven.repo-locations.v1"
REF = re.compile(r"\b([A-Za-z][A-Za-z0-9_.-]{1,63})::([^\s`'\"<>()\[\],;]+)")


class Unresolved(Exception):
    def __init__(self, reason: str, detail: str = ""):
        super().__init__(f"{reason}{': ' + detail if detail else ''}")
        self.reason = reason


def config_path(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    return Path(os.environ.get("HAVEN_REPOS", "~/.haven/repos.json")).expanduser()


def load(explicit: str | None = None) -> dict:
    p = config_path(explicit)
    if not p.is_file():
        raise Unresolved("config_missing", str(p))
    try:
        cfg = json.loads(p.read_text())
    except Exception as e:
        raise Unresolved("config_invalid", f"{p}: {e}")
    if cfg.get("schema") != SCHEMA:
        raise Unresolved("config_invalid", f"{p}: schema is {cfg.get('schema')!r}")
    if not cfg.get("repos"):
        raise Unresolved("config_invalid", f"{p}: no repos declared")
    cfg["_file"] = str(p)
    return cfg


def repo_root(repo: str, cfg: dict) -> Path:
    entry = cfg["repos"].get(repo)
    if entry is None:
        raise Unresolved("repo_not_declared", f"{repo} (in {cfg['_file']})")
    raw = entry["path"]
    p = Path(raw).expanduser()
    if not p.is_absolute():
        common = cfg.get("commonRoot")
        if not common:
            raise Unresolved("no_common_root", f"{repo} path {raw!r} is relative")
        p = Path(common).expanduser() / p
    p = p.resolve()
    if not p.is_dir():
        raise Unresolved("repo_missing", f"{repo} -> {p}")
    marker = entry.get("marker")
    if marker:
        m = (p / marker["path"]).resolve()
        if not str(m).startswith(str(p) + os.sep):
            raise Unresolved("marker_escapes_repo", f"{repo} -> {m}")
        if not m.is_file():
            raise Unresolved("marker_missing", f"{repo} -> {m}")
        want = marker.get("contains")
        if want and want not in m.read_text(errors="replace"):
            raise Unresolved("marker_mismatch", f"{repo} -> {m} lacks {want!r}")
    return p


def resolve(ref: str, cfg: dict) -> Path:
    """`Repo::relative/path`, or just `Repo`, to one absolute path."""
    repo, _, rel = ref.partition("::")
    root = repo_root(repo, cfg)
    if not rel or rel == ".":
        return root
    if rel.startswith("/") or rel.startswith("~"):
        raise Unresolved("not_repo_relative", ref)
    target = (root / rel).resolve()
    if target != root and not str(target).startswith(str(root) + os.sep):
        raise Unresolved("escapes_repo", f"{ref} -> {target}")
    return target


# ------------------------------------------------------------------- init
def _marker_for(root: Path, name: str) -> dict | None:
    pkg = root / "Package.swift"
    if pkg.is_file():
        text = pkg.read_text(errors="replace")
        want = f'name: "{name}"'
        if want in text:
            return {"path": "Package.swift", "contains": want}
        return {"path": "Package.swift"}
    for cand in sorted(root.glob("README*.md")) + sorted(root.glob("*.md")):
        return {"path": cand.name}
    return None


def cmd_init(args) -> int:
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1
    # A folder counts as a repo unless it is obviously scratch. Keying on `.git`
    # was the first attempt and it silently dropped PalazzoScaffold, which has a
    # Package.swift and no checkout of its own -- and which documents already
    # reference. Declaring one folder too many costs nothing; missing one breaks
    # every reference into it, which is the failure this tool exists to remove.
    skip = {"node_modules", "build", ".build", "DerivedData"}
    repos = {}
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name.startswith("_"):
            continue
        if child.name in skip or child.name.lower().startswith("claude output"):
            continue
        entry = {"path": child.name}
        m = _marker_for(child, child.name)
        if m:
            entry["marker"] = m
        repos[child.name] = entry
    cfg = {"schema": SCHEMA, "commonRoot": str(root), "repos": repos}
    out = config_path(args.config)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cfg, indent=2) + "\n")

    # Bootstrap: to resolve `CellProtocolDocuments::…` you need this tool, and to
    # find this tool you need a path. Breaking that circle needs exactly one
    # absolute path per machine that is a device setting by definition, so init
    # puts a copy beside the config. From then on ~/.haven/haven_path.py is the
    # single entry point and everything else derives from it.
    me = Path(__file__).resolve()
    beside = out.parent / "haven_path.py"
    if me != beside:
        beside.write_text(me.read_text())
        beside.chmod(0o755)
    print(f"{len(repos)} repoer erklært i {out}")
    print(f"verktøyet kopiert til {beside} — bruk den stien i skript")
    for name in repos:
        print(f"  {name}")
    return 0


# ------------------------------------------------------------------ checks
def cmd_check(args) -> int:
    cfg = load(args.config)
    bad = 0
    for repo in sorted(cfg["repos"]):
        try:
            print(f"  ok   {repo}::  ->  {repo_root(repo, cfg)}")
        except Unresolved as e:
            bad += 1
            print(f"  FAIL {repo}::  {e}", file=sys.stderr)
    print(f"\n{len(cfg['repos']) - bad}/{len(cfg['repos'])} repoer lot seg avlede "
          f"({cfg['_file']})")
    return 1 if bad else 0


def cmd_path(args) -> int:
    try:
        print(resolve(args.ref, load(args.config)))
        return 0
    except Unresolved as e:
        print(f"haven-path: {e}", file=sys.stderr)
        return 1


def cmd_scan(args) -> int:
    cfg = load(args.config)
    seen, bad = 0, 0
    for f in args.files:
        text = Path(f).read_text(errors="replace")
        for m in REF.finditer(text):
            ref = m.group(0).rstrip(".,:;")
            if m.group(1) not in cfg["repos"] and not args.strict:
                continue          # `cell://`-like or prose, not a repo reference
            seen += 1
            try:
                p = resolve(ref, cfg)
                if not p.exists():
                    raise Unresolved("target_missing", str(p))
                if args.verbose:
                    print(f"  ok   {ref}  ->  {p}")
            except Unresolved as e:
                bad += 1
                print(f"  FAIL {f}: {ref}  {e}", file=sys.stderr)
    print(f"{seen - bad}/{seen} referanser gav en eksisterende full path")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--config", help="device file (default $HAVEN_REPOS or ~/.haven/repos.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init"); i.add_argument("root", nargs="?", default="."); i.set_defaults(fn=cmd_init)
    p = sub.add_parser("path"); p.add_argument("ref"); p.set_defaults(fn=cmd_path)
    c = sub.add_parser("check"); c.set_defaults(fn=cmd_check)
    s = sub.add_parser("scan"); s.add_argument("files", nargs="+")
    s.add_argument("--verbose", action="store_true"); s.add_argument("--strict", action="store_true")
    s.set_defaults(fn=cmd_scan)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except Unresolved as e:
        print(f"haven-path: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
