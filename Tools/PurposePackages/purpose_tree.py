#!/usr/bin/env python3
"""purpose_tree.py — formålstreet i en PDD som `tree.json` (haven.purpose-review.v0), og tilbake.

Ren stdlib. Brukes av `purpose_dev.py tree` og `purpose_dev.py treediff`.

  tree      Leser FORMAALSSPEC.md §1 (alle tabeller med kolonnen purposeRef) og lager treet som
            `cell:///PurposeReview` tar imot med `review.import` eller «Legg inn treet» i Developer
            Workbench. Valideres med de samme reglene som cellen (PurposeReviewCell.validationProblem).
  treediff  Sammenligner et tre hentet fra Workbench (tree.json) med §1 og skriver hva som er lagt
            til, fjernet og endret, så §1 og §7 kan oppdateres før en port. Endrer ingen filer.

Formatene i §1 varierer mellom PDD-ene; dette leses:
  - purposeRef: full ref (`purpose://…`), kode (`pc.chat`, `**sk.root**`), kode + ref i backticks,
    eller kode + forkortet ref (`…agreement.signatures`).
  - Forelder: kode i treet (`root`, `ft.view`, `pc.root`), full ref i treet, «—» for roten, eller en
    ref utenfor treet (Book 23) som da blir treets anchorRef.
"""
from __future__ import annotations

import json
import os
import re

SCHEMA = "haven.purpose-review.v0"
GATES = ["G1", "G1-GUI", "G2", "G3"]
MAX_NODES = 400
REF_RE = re.compile(r"purpose://[A-Za-z0-9._\-/]+")
CODE_RE = re.compile(r"^[a-z][a-z0-9-]*(\.[a-z0-9][a-z0-9-]*)*$")

COLUMNS = {
    "ref": ("purposeref", "ref"),
    "title": ("tittel", "title"),
    "parent": ("forelder", "parent"),
    "outcome": ("goal", "mål", "outcome"),
    "verifier": ("verifier", "verifisering"),
    "status": ("status",),
    "signals": ("tegn", "signals", "successsignals"),
}


def _clean(text):
    return re.sub(r"\s+", " ", text.replace("**", "").replace("`", "")).strip()


def _strip_ref(ref):
    return ref.rstrip(".,;:)")


def folder_parts(taskdir):
    """PDD_<slug>_<YYYY-MM-DD> → (slug, dato)."""
    name = os.path.basename(os.path.normpath(taskdir))
    m = re.match(r"^PDD_(.+)_(\d{4}-\d{2}-\d{2})$", name)
    if not m:
        raise ValueError(f"{name} er ikke en PDD-mappe (PDD_<slug>_<dato>)")
    return m.group(1), m.group(2)


def _split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def section_one(text):
    """Teksten i «## 1.»-avsnittet."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r"^##\s+1\.", l)), None)
    if start is None:
        raise ValueError("FORMAALSSPEC.md har ikke et «## 1.»-avsnitt")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s+\d", lines[i])), len(lines))
    return lines[start:end]


def _identity_like(cell):
    text = _clean(cell)
    first = text.split(" ")[0] if text else ""
    return bool(REF_RE.search(text)) or first == "root" or first.startswith("test.") or (
        bool(CODE_RE.match(first)) and "." in first)


def table_rows(lines, notes=None):
    """Alle rader i tabeller med kolonnen purposeRef, som dict med kolonnenøklene over.

    En rad som er brutt over to linjer (den andre linjen starter ikke med en kode eller ref og
    har færre kolonner) slås sammen med raden over.
    """
    notes = notes if notes is not None else []
    rows, header, width = [], None, 0
    raw = []

    def flush():
        for cells in raw:
            rows.append({key: (cells[i] if i < len(cells) else "") for key, i in header.items()})
        raw.clear()

    for line in lines:
        if not line.lstrip().startswith("|"):
            if header:
                flush()
            header = None
            continue
        cells = _split_row(line)
        if all(re.match(r"^:?-{2,}:?$", c) for c in cells if c):
            continue
        if header is None:
            lowered = [_clean(c).lower() for c in cells]
            # Bare formålstabeller (purposeRef først); testtabeller har purposeRef lenger ut.
            if not lowered or not lowered[0].startswith("purposeref"):
                header = False
                continue
            header, width = {}, len(cells)
            for key, names in COLUMNS.items():
                for i, c in enumerate(lowered):
                    if any(c.startswith(n) for n in names) and key not in header:
                        header[key] = i
            continue
        if header is False:
            continue
        if raw and len(cells) < width and not _identity_like(cells[0]):
            raw[-1][-1] = (raw[-1][-1] + " " + cells[0]).strip()
            raw[-1].extend(cells[1:])
            continue
        if len(cells) > width:
            notes.append(f"raden «{_clean(cells[0])}» har {len(cells)} kolonner, tabellen {width}: sjekk raden i §1")
        raw.append(cells)
    if header:
        flush()
    return rows


def _identity(raw, slug):
    """(kode, ref) fra purposeRef-cellen."""
    text = _clean(raw)
    base = f"purpose://candidate.{slug}."
    full = REF_RE.search(text)
    first = text.split(" ")[0] if text else ""
    code = first if CODE_RE.match(first) else None
    if full:
        ref = _strip_ref(full.group(0))
    else:
        abbreviated = re.search(r"…([A-Za-z0-9._\-]+)", text)
        if abbreviated:
            ref = base + abbreviated.group(1).strip(".")
        elif code:
            tail = code.split(".", 1)[1] if "." in code else code
            ref = base + tail
        else:
            raise ValueError(f"forstår ikke purposeRef «{raw}»")
    if code is None:
        code = ref[len(base):] if ref.startswith(base) else None
    return code, ref


def parse_spec(taskdir, gate=None):
    return parse_spec_with_notes(taskdir, gate)[0]


KNOWN_STATUS = {"candidate", "draft", "active", "accepted", "approved", "godkjent", "kandidat", "deprecated", "retired"}


def parse_spec_with_notes(taskdir, gate=None):
    """(tre, merknader). Merknadene er rader som ble hoppet over eller ser feil ut i §1."""
    notes = []
    slug, date = folder_parts(taskdir)
    spec_path = os.path.join(taskdir, "FORMAALSSPEC.md")
    with open(spec_path, encoding="utf-8") as fh:
        text = fh.read()
    lines = section_one(text)
    rows = table_rows(lines, notes)
    if not rows:
        raise ValueError("fant ingen tabell med kolonnen purposeRef i §1")

    nodes, by_code, by_ref = [], {}, {}
    for row in rows:
        if _clean(row.get("ref", "")).startswith("test."):
            # En testrad som har havnet i formålstabellen; testene hører til §5.
            notes.append(f"hoppet over testraden «{_clean(row['ref']).split(' ')[0]}» i formålstabellen")
            continue
        code, ref = _identity(row.get("ref", ""), slug)
        if ref in by_ref:
            raise ValueError(f"{ref} står mer enn én gang i §1")
        node = {"ref": ref, "parentRef": None, "code": code, "title": _clean(row.get("title", ""))}
        for key in ("outcome", "verifier", "status"):
            value = _clean(row.get(key, ""))
            if value:
                node[key] = value
        if row.get("signals"):
            node["signals"] = [s.strip() for s in re.split(r"<br\s*/?>|;", row["signals"]) if _clean(s)]
        node["_parent"] = _clean(row.get("parent", ""))
        nodes.append(node)
        by_ref[ref] = node
        if code:
            by_code[code] = node

    anchor_ref, anchor_note, roots = None, None, []
    for node in nodes:
        parent = node.pop("_parent")
        first = parent.split(" ")[0] if parent else ""
        target = None
        if first in by_code:
            target = by_code[first]["ref"]
        else:
            found = REF_RE.search(parent)
            if found and _strip_ref(found.group(0)) in by_ref:
                target = _strip_ref(found.group(0))
            elif found:
                anchor_ref = anchor_ref or _strip_ref(found.group(0))
                note = _clean(parent.replace(found.group(0), "")).strip("()— ").strip()
                note = re.sub(r"^anchorRef\b\s*", "", note).strip("()— ").strip()
                anchor_note = anchor_note or (note or None)
        if target == node["ref"]:
            target = None
        node["parentRef"] = target
        if target is None:
            roots.append(node["ref"])
    if len(roots) != 1:
        raise ValueError(f"§1 må ha nøyaktig én rot; fant {len(roots)}: {roots[:5]}")
    if anchor_ref is None:
        lead = " ".join(l for l in lines if not l.lstrip().startswith("|"))
        found = REF_RE.search(lead)
        anchor_ref = _strip_ref(found.group(0)) if found else None

    title_line = next((l for l in text.splitlines() if l.startswith("# ")), "")
    title = re.sub(r"^#\s*(Formålsspesifikasjon\s*[—-]\s*)?", "", title_line).strip() or by_ref[roots[0]]["title"]
    tree = {
        "id": f"{slug}-{date}",
        "title": title,
        "pdd": os.path.basename(os.path.normpath(taskdir)),
        "gate": gate or next_gate(taskdir),
        "anchorRef": anchor_ref,
        "anchorNote": anchor_note,
        "rootRef": roots[0],
        "nodes": nodes,
    }
    for node in nodes:
        status = node.get("status")
        if status and status.lower() not in KNOWN_STATUS:
            notes.append(f"{node['code'] or node['ref']}: uvanlig status «{status}»")
    problem = validation_problem(tree)
    if problem:
        raise ValueError(problem)
    return tree, notes


def next_gate(taskdir):
    """Første port i STATUS.md som ikke er godkjent; G3 når alle er det."""
    path = os.path.join(taskdir, "STATUS.md")
    status = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r"\s*-\s*(G1-GUI|G1|G2|G3)\s*:\s*(\S+)", line)
            if m:
                status[m.group(1)] = m.group(2).lower()
    for gate in GATES:
        if not status.get(gate, "").startswith("godkjent"):
            return gate
    return GATES[-1]


def validation_problem(tree):
    """Samme regler som PurposeReviewCell.validationProblem."""
    if not str(tree.get("id", "")).strip():
        return "Treet mangler id."
    nodes = tree.get("nodes") or []
    if not nodes:
        return "Treet har ingen formål."
    if len(nodes) > MAX_NODES:
        return f"Treet har flere enn {MAX_NODES} formål."
    by_ref = {}
    for node in nodes:
        ref = node.get("ref", "")
        if not ref.startswith("purpose://"):
            return f"{ref} er ikke en purpose://-ref."
        if ref in by_ref:
            return f"{ref} står mer enn én gang."
        by_ref[ref] = node
    root = by_ref.get(tree.get("rootRef"))
    if root is None or root.get("parentRef") is not None:
        return "rootRef må være et formål i treet uten parentRef."
    for node in nodes:
        if node["ref"] == tree["rootRef"]:
            continue
        parent = node.get("parentRef")
        if parent not in by_ref:
            return f"{node['ref']} har ingen forelder i treet."
        seen, cursor = {node["ref"]}, by_ref[parent]
        while cursor is not None:
            if cursor["ref"] in seen:
                return f"Treet har en sykel gjennom {cursor['ref']}."
            seen.add(cursor["ref"])
            cursor = by_ref.get(cursor.get("parentRef"))
    return None


FIELDS = ("title", "parentRef", "code", "outcome", "verifier", "status", "signals", "reused")


def tree_diff(spec_tree, exported):
    """Hva Workbench-treet har endret i forhold til §1: (lagt til, fjernet, endret)."""
    problem = validation_problem(exported)
    if problem:
        raise ValueError(f"treet fra Workbench er ugyldig: {problem}")
    before = {n["ref"]: n for n in spec_tree["nodes"]}
    after = {n["ref"]: n for n in exported["nodes"]}
    added = [after[r] for r in after if r not in before]
    removed = [before[r] for r in before if r not in after]
    changed = []
    for ref in before:
        if ref not in after:
            continue
        fields = []
        for key in FIELDS:
            old, new = before[ref].get(key), after[ref].get(key)
            if (old or None) != (new or None):
                fields.append((key, old, new))
        if fields:
            changed.append((after[ref], fields))
    return added, removed, changed


def render_diff(spec_tree, exported):
    added, removed, changed = tree_diff(spec_tree, exported)
    out = [f"# Endringer i «{exported.get('title', spec_tree['title'])}» fra Workbench",
           "",
           f"Revisjon i Workbench: {exported.get('revision', '?')}. §1 har {len(spec_tree['nodes'])} formål, "
           f"Workbench {len(exported['nodes'])}.",
           ""]
    if not (added or removed or changed):
        out.append("Ingen endringer. §1 og Workbench er like.")
        return "\n".join(out) + "\n"
    if added:
        out += ["## Lagt til", "", "| purposeRef | Tittel | Forelder | Gjenbruk |", "|---|---|---|---|"]
        out += [f"| {n['ref']} | {n.get('title', '')} | {n.get('parentRef') or '—'} | {n.get('reused') or ''} |" for n in added]
        out.append("")
    if removed:
        out += ["## Fjernet", ""] + [f"- {n['ref']} — {n.get('title', '')}" for n in removed] + [""]
    if changed:
        out += ["## Endret", ""]
        for node, fields in changed:
            out.append(f"- {node['ref']}")
            for key, old, new in fields:
                out.append(f"  - {key}: {json.dumps(old, ensure_ascii=False)} → {json.dumps(new, ensure_ascii=False)}")
        out.append("")
    out.append("Oppdater §1 og skriv en linje i §7 før porten. En godkjent port i STATUS.md endres ikke av dette.")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- CLI (kalles fra purpose_dev.py)

def write_tree(taskdir, out=None, gate=None, title=None, to_stdout=False):
    tree, notes = parse_spec_with_notes(taskdir, gate)
    if title:
        tree["title"] = title
    text = json.dumps(tree, ensure_ascii=False, indent=2) + "\n"
    if to_stdout:
        print(text, end="")
        return 0
    out = out or os.path.join(taskdir, "formaalsside", "tree.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    branches = sum(1 for n in tree["nodes"] if n.get("parentRef") == tree["rootRef"])
    parents = {n.get("parentRef") for n in tree["nodes"]}
    leaves = sum(1 for n in tree["nodes"] if n["ref"] not in parents)
    print(f"{out}: {len(tree['nodes'])} formål ({branches} grener, {leaves} bladformål), port {tree['gate']}, "
          f"anker {tree['anchorRef'] or '—'}")
    for note in notes:
        print(f"  merk: {note}")
    print("  Lim inn i Developer Workbench → Formål → «Legg inn et formålstre», eller send med review.import.")
    return 0


def diff_command(taskdir, exported_path):
    with open(exported_path, encoding="utf-8") as fh:
        exported = json.load(fh)
    # review.state gir {selected: {tree: …}}; en ren tree.json brukes som den er.
    if isinstance(exported.get("selected"), dict) and isinstance(exported["selected"].get("tree"), dict):
        selected = exported["selected"]
        exported = dict(selected["tree"], id=selected.get("id"), revision=selected.get("revision"))
    spec_tree = parse_spec(taskdir)
    print(render_diff(spec_tree, exported), end="")
    return 0
