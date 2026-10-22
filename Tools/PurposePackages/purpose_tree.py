#!/usr/bin/env python3
"""purpose_tree.py — formålstreet i en PDD som `tree.json` (haven.purpose-review.v0), og tilbake.

Ren stdlib. Brukes av `purpose_dev.py tree` og `purpose_dev.py treediff`.

  tree      Leser FORMAALSSPEC.md §1 (alle tabeller med kolonnen purposeRef) og lager treet som
            `cell:///PurposeReview` tar imot med `review.import` eller «Legg inn treet» i Developer
            Workbench. Valideres med de samme reglene som cellen (PurposeReviewCell.validationProblem).
            Pakkene i §4 («Formålspakker som festes») kommer med som grenen «Standardpakker
            (gjenbrukt)», med tittel, mål, tegn og verifier fra Book/haven_purpose_packages_v0.json,
            slik Formålstrær-siden viste dem.
  treediff  Sammenligner et tre hentet fra Workbench (tree.json) med §1 og skriver hva som er lagt
            til, fjernet og endret, så §1 og §7 kan oppdateres før en port. Endrer ingen filer.

Formatene i §1 varierer mellom PDD-ene; dette leses:
  - purposeRef: full ref (`purpose://…`), kode (`pc.chat`, `**sk.root**`), kode + ref i backticks,
    eller kode + forkortet ref (`…agreement.signatures`).
  - Overskrift: «## 1. …», «## §1 …» eller «## Formålstre». Tabeller med «Kode | purposeRef | …» leses også.
  - Forelder: kode i treet (`root`, `ft.view`, `R`), «rot»/«root», full eller kortet ref i treet
    (`human-agency`, `control` for …approvals.control), «—» for roten, eller en ref utenfor treet
    (Book 23) som da blir treets anchorRef.
  - Mangler Forelder: nærmeste ref-prefiks i treet, ellers overskriften («### 1.1 Gren 1 — X») som
    egen gren, ellers roten.
  - Står flere formål uten forelder i treet, blir …root (eller det første) roten og de andre legges
    under den, med den opprinnelige forelderen i `why` og en merknad. Uten rot lages en av tittelen.
  - Pakkeformål (Book/haven_purpose_packages_v0.json) øverst i §1 går til pakkegrenen. Rader som ikke
    er purposeRef, testrader og doble rader hoppes over med en merknad.
Eldre PDD-er med treet som punktliste, tekstdiagram eller mermaid leses ikke; da sier verktøyet det.
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
PACKAGE_LINE_RE = re.compile(r"^\s*-\s+\*\*(pkg\.[A-Za-z0-9._-]+)\*\*")
PACKAGES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             "Book", "haven_purpose_packages_v0.json")

COLUMNS = {
    "code": ("kode", "code"),
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
    start = next((i for i, l in enumerate(lines) if re.match(r"^##\s+(1\.|§1\b(?![a-z]))", l)), None)
    if start is None:
        # Eldre PDD-er: «## Formålstre» uten nummer.
        start = next((i for i, l in enumerate(lines) if re.match(r"^##\s+(\d+\.\s*)?Formålstre", l, re.I)), None)
    if start is None:
        raise ValueError("FORMAALSSPEC.md har ikke et «## 1.»-avsnitt")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s+§?\d", lines[i])), len(lines))
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
    heading = ""

    def flush():
        for cells in raw:
            row = {key: (cells[i] if i < len(cells) else "") for key, i in header.items()}
            if "parent" not in header and heading:
                # Uten Forelder-kolonne: overskriften over tabellen er grenen (eldre PDD-er).
                row["_heading"] = heading
            rows.append(row)
        raw.clear()

    for line in lines:
        if line.startswith("### "):
            heading = _clean(line[4:])
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
            # Også «Kode | purposeRef | …».
            first_ref = 1 if len(lowered) > 1 and lowered[0] in ("kode", "code") else 0
            if not lowered or not lowered[first_ref].startswith("purposeref"):
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
        if raw and len(cells) < width and not _identity_like(cells[header.get("ref", 0)] if len(cells) > header.get("ref", 0) else cells[0]):
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


def parse_spec(taskdir, gate=None, packages_path=None):
    return parse_spec_with_notes(taskdir, gate, packages_path)[0]


def attached_packages(text):
    """packageRef-ene i §4 «Formålspakker som festes», i rekkefølge."""
    refs, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = "formålspakker som festes" in line.lower()
            continue
        if inside:
            m = PACKAGE_LINE_RE.match(line)
            if m and m.group(1) not in refs:
                refs.append(m.group(1))
    return refs


def _load_registry(packages_path=None, notes=None):
    """packageRef → pakke fra Book/haven_purpose_packages_v0.json (tom hvis fila mangler)."""
    path = packages_path or PACKAGES_PATH
    try:
        with open(path, encoding="utf-8") as fh:
            return {p["packageRef"]: p for p in json.load(fh).get("packages", [])}
    except (OSError, ValueError, KeyError) as exc:
        if notes is not None:
            notes.append(f"pakkene ble ikke lest: {path} ({exc})")
        return {}


ROOT_WORDS = {"root", "rot"}
EMPTY_PARENT = re.compile(r"^(—|-|–|ingen\b|none\b|n/a\b)?$", re.I)


def _parent_target(parent, node, by_ref, by_code):
    """Hva Forelder-cellen peker på: ("node", ref), ("root", None), ("pkg", None),
    ("outside", ref eller None) eller ("none", None)."""
    text = parent.strip()
    if EMPTY_PARENT.match(text):
        return "none", None
    words = [w.strip("().,;:«»") for w in re.split(r"[\s;,]+", text) if w.strip("().,;:«»")]
    refs = [_strip_ref(m.group(0)) for m in REF_RE.finditer(text)]
    candidates = words[:1] + refs
    for token in candidates:
        if token in ROOT_WORDS:
            return "root", None
        if token.startswith("pkg."):
            return "pkg", None
        for key in (token, "purpose://" + token):
            hit = by_ref.get(key) or by_code.get(key if key == token else None)
            if hit is not None and hit is not node:
                return "node", hit["ref"]
        suffix = [r for r in by_ref if r != node["ref"] and r.endswith("." + token)]
        if len(suffix) == 1:
            return "node", suffix[0]
        codes = [c for c in by_code if by_code[c] is not node and c.endswith("." + token)]
        if len(codes) == 1:
            return "node", by_code[codes[0]]["ref"]
    if refs:
        return "outside", refs[0]
    first = words[0] if words else ""
    if CODE_RE.match(first) and ("." in first or "-" in first):
        return "outside", "purpose://" + first
    return "none", None


def _prefix_parent(ref, by_ref):
    """Nærmeste ref i treet som er et prefiks av ref (…onboarding.x → …onboarding)."""
    parts = ref.split(".")
    for cut in range(len(parts) - 1, 1, -1):
        candidate = ".".join(parts[:cut])
        if candidate in by_ref and candidate != ref:
            return candidate
    return None


def _heading_title(heading):
    title = re.sub(r"^\d+(\.\d+)*\s*", "", heading)
    title = re.sub(r"^(Gren|Branch)\s+\w+\s*[—:–-]\s*", "", title, flags=re.I)
    return title.strip() or heading


def _slug(text):
    text = text.lower()
    for a, b in (("æ", "ae"), ("ø", "o"), ("å", "a"), ("é", "e")):
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:40].rstrip("-") or "gren"


def _place_nodes(nodes, by_ref, by_code, package_refs, slug, text, notes):
    """Setter parentRef på alle noder. Gir (rootRef, anchorRef, anchorNote, noder til pakkegrenen).

    Nøyaktig én rot: noden med en forelder utenfor treet (Book 23) eller ingen forelder. Står
    det flere slike i §1, blir den som heter …root (eller den første som ikke er et pakkeformål)
    roten, og de andre legges under den med en merknad. Pakkeformål øverst går til pakkegrenen.
    Finnes ingen slik node, lages en rot av tittelen i FORMAALSSPEC.md.
    """
    placed, tops = {}, []
    for node in nodes:
        parent = node.pop("_parent")
        kind, target = _parent_target(parent, node, by_ref, by_code)
        if kind == "none":
            prefix = _prefix_parent(node["ref"], by_ref)
            if prefix:
                kind, target = "node", prefix
            elif node.get("_heading"):
                kind = "heading"
        placed[node["ref"]] = (kind, target, parent)
        if kind in ("none", "outside"):
            tops.append(node)

    def is_root_named(n):
        return n.get("code") == "root" or n["ref"].endswith(".root")

    root = next((n for n in tops if is_root_named(n)), None)
    if root is None:
        root = next((n for n in tops if n["ref"] not in package_refs), None)
    if root is None and len(tops) == 1:
        root = tops[0]
    if root is None:
        title_line = next((l for l in text.splitlines() if l.startswith("# ")), "")
        title = re.sub(r"^#\s*(Formålsspesifikasjon\s*[—-]\s*)?", "", title_line).strip() or slug
        root = {"ref": f"purpose://candidate.{slug}.root", "parentRef": None, "code": "root", "title": title,
                "status": "candidate", "signals": []}
        if root["ref"] in by_ref:
            raise ValueError(f"§1 har ingen rot, og {root['ref']} finnes allerede")
        nodes.insert(0, root)
        by_ref[root["ref"]] = root
        notes.append(f"§1 har ingen rot; lagde {root['ref']} («{title}») og la toppformålene under den")

    anchor_ref = anchor_note = None
    kind, target, parent = placed.get(root["ref"], ("none", None, ""))
    if kind == "outside":
        anchor_ref = target
        note = _clean(parent.replace(target, "").replace(target[len("purpose://"):], ""))
        note = re.sub(r"^anchorRef\b\s*", "", note).strip("()— ;,").strip()
        anchor_note = note or None
    root["parentRef"] = None

    outside, branches = [], {}
    stem = root["ref"][:-len(".root")] if root["ref"].endswith(".root") else root["ref"]
    for node in list(nodes):
        heading = node.pop("_heading", None)
        if node is root:
            continue
        kind, target, parent = placed.get(node["ref"], ("root", None, ""))
        if kind == "heading":
            branch = branches.get(heading)
            if branch is None:
                title = _heading_title(heading)
                ref = f"{stem}.{_slug(title)}"
                while ref in by_ref:
                    ref += "-gren"
                branch = {"ref": ref, "parentRef": root["ref"], "code": None, "title": title,
                          "status": "candidate", "signals": []}
                branches[heading] = branch
                nodes.insert(nodes.index(node), branch)
                by_ref[ref] = branch
                notes.append(f"lagde grenen «{title}» fra overskriften i §1 (tabellen har ingen Forelder-kolonne)")
            node["parentRef"] = branch["ref"]
        elif kind == "node":
            node["parentRef"] = target
        elif kind == "pkg" or (kind in ("none", "outside", "root") and node["ref"] in package_refs
                               and kind != "root"):
            outside.append(node)
        else:
            node["parentRef"] = root["ref"]
            if kind == "outside":
                node.setdefault("why", f"Forelder utenfor treet (Book 23): {target}")
                notes.append(f"{node.get('code') or node['ref']}: forelderen {target} er utenfor treet; lagt under roten")
            elif kind == "none":
                notes.append(f"{node.get('code') or node['ref']}: ingen forelder i §1; lagt under roten")
    return root["ref"], anchor_ref, anchor_note, outside


def package_nodes(text, root, existing, registry, outside=()):
    """Grenen «Standardpakker (gjenbrukt)»: pakkeformålene §1 har uten forelder i treet, og
    formålene i pakkene §4 fester."""
    refs = attached_packages(text)
    if not refs and not outside:
        return []
    prefix = root["ref"][:-len(".root")] if root["ref"].endswith(".root") else root["ref"]
    branch = {"ref": f"{prefix}.pkg.std", "parentRef": root["ref"], "code": "pkg.std",
              "title": "Standardpakker (gjenbrukt)", "outcome": "Alle standardformål grønne",
              "verifier": "§5 standardrader", "status": "candidate", "signals": []}
    if branch["ref"] in existing:
        for node in outside:
            node["parentRef"] = branch["ref"]
        return []
    for node in outside:
        node["parentRef"] = branch["ref"]
        node.setdefault("reused", node["ref"])
    nodes, seen = [branch], set(existing) | {branch["ref"]}
    for package_ref in refs:
        package = registry.get(package_ref)
        if package is None:
            continue
        for purpose in package.get("purposes", []):
            ref = purpose.get("purposeRef", "")
            if not ref.startswith("purpose://") or ref in seen:
                continue
            seen.add(ref)
            goal = purpose.get("goal") or {}
            node = {"ref": ref, "parentRef": branch["ref"], "code": ref[len("purpose://"):],
                    "title": purpose.get("title") or ref, "reused": ref}
            if goal.get("outcome"):
                node["outcome"] = goal["outcome"]
            node["signals"] = list(goal.get("successSignals") or [])
            if goal.get("verifier"):
                node["verifier"] = goal["verifier"]
            if purpose.get("status"):
                node["status"] = purpose["status"]
            nodes.append(node)
    return nodes if (len(nodes) > 1 or outside) else []


KNOWN_STATUS = {"candidate", "draft", "active", "accepted", "approved", "godkjent", "kandidat", "deprecated", "retired"}


def parse_spec_with_notes(taskdir, gate=None, packages_path=None):
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
        try:
            code, ref = _identity(row.get("ref", ""), slug)
        except ValueError:
            notes.append(f"hoppet over raden «{_clean(row.get('ref', ''))[:60]}»: ikke en purposeRef")
            continue
        if ref in by_ref:
            notes.append(f"{ref} står mer enn én gang i §1; den første raden er brukt")
            continue
        own_code = _clean(row.get("code", ""))
        if own_code and own_code not in by_code:
            code = own_code
        node = {"ref": ref, "parentRef": None, "code": code, "title": _clean(row.get("title", ""))}
        for key in ("outcome", "verifier", "status"):
            value = _clean(row.get(key, ""))
            if value:
                node[key] = value
        if row.get("signals"):
            node["signals"] = [s.strip() for s in re.split(r"<br\s*/?>|;", row["signals"]) if _clean(s)]
        node["_parent"] = _clean(row.get("parent", ""))
        if row.get("_heading"):
            node["_heading"] = row["_heading"]
        nodes.append(node)
        by_ref[ref] = node
        if code:
            by_code[code] = node

    registry = _load_registry(packages_path, notes)
    package_refs = {p.get("purposeRef") for pkg in registry.values() for p in pkg.get("purposes", [])}
    root_ref, anchor_ref, anchor_note, outside = _place_nodes(nodes, by_ref, by_code, package_refs, slug, text, notes)
    if anchor_ref is None:
        lead = " ".join(l for l in lines if not l.lstrip().startswith("|"))
        found = REF_RE.search(lead)
        anchor_ref = _strip_ref(found.group(0)) if found else None
    roots = [root_ref]

    nodes.extend(package_nodes(text, by_ref[root_ref], by_ref, registry, outside))

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
    lines = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    for line in lines:
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
