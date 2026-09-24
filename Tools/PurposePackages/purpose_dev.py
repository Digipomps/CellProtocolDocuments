#!/usr/bin/env python3
"""purpose_dev.py — verktøy for formålsdrevet utvikling (PDD) i HAVEN.

Ren stdlib. Kjører både i macOS-terminalen og i Cowork-VM-en (device_bash).

Kommandoer
  validate [TASKDIR]          Valider formålspakker, lærdomsregister og (valgfritt) en oppgavemappe.
  lookup  --tags T.. --surfaces S..
                              Vis hvilke pakker, formål, avledede tester og lærdommer som festes.
  new SLUG --intent "…" [--tags T..] [--surfaces S..]
                              Opprett Deliverables/PDD_<SLUG>_<dato>/ med FORMAALSSPEC.md, STATUS.md, images/.
  gates TASKDIR               Vis portstatus (G1, G1-GUI, G2, G3) utledet fra artefaktene i mappen.
  lesson add TASKDIR          Interaktivt: legg til en lærdom i registeret (skriver til Book/haven_lessons_register_v0.json).
  judge TASKDIR --run RUN.json
                              Registrer G1-treff, repeatOf og håndhevelse; fortsett uten --run.

Eksempel
  python3 Tools/PurposePackages/purpose_dev.py lookup --tags gui palazzo bestilling --surfaces skeleton
  python3 Tools/PurposePackages/purpose_dev.py new palazzo-gjestebestilling --intent "Gjesten bestiller fra egen telefon" --tags gui palazzo --surfaces skeleton cell
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys

from purpose_composition import Composition, LOG_FIELDS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
KB_PATH = os.path.join(REPO, "Book", "haven_purpose_knowledge_base_v0.json")
PKG_PATH = os.path.join(REPO, "Book", "haven_purpose_packages_v0.json")
LESSONS_PATH = os.path.join(REPO, "Book", "haven_lessons_register_v0.json")
DELIVERABLES = os.path.join(REPO, "Deliverables")

GATES = ["G1", "G1-GUI", "G2", "G3"]
GUI_SURFACES = {"gui", "skeleton", "porthole", "binding", "web"}
COMPOSITION_FILE = "PURPOSE_COMPOSITION.json"


# ---------------------------------------------------------------- loading

def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_all():
    kb = _load(KB_PATH) if os.path.exists(KB_PATH) else {"nodes": [], "facets": []}
    pk = _load(PKG_PATH)
    ls = _load(LESSONS_PATH)
    return kb, pk, ls


def all_purpose_refs(kb, pk):
    refs = {n["purposeRef"] for n in kb.get("nodes", [])}
    for p in pk["packages"]:
        for n in p.get("purposes", []):
            refs.add(n["purposeRef"])
    return refs


def composition_context(kb, pk, taskdir=None):
    """Combine definitions without changing canonical nodes or inventing defaults."""
    nodes = list(kb.get("nodes", []))
    documents = [kb, pk]
    for package in pk.get("packages", []):
        nodes.extend(package.get("purposes", []))
    task = {}
    load_errors = []
    if taskdir:
        path = os.path.join(taskdir, COMPOSITION_FILE)
        if os.path.exists(path):
            try:
                task = _load(path)
                if not isinstance(task, dict) or not isinstance(task.get("nodes", []), list):
                    raise ValueError("oppgavefilen må være et objekt med nodes-liste")
                nodes.extend(task.get("nodes", []))
                documents.append(task)
            except (OSError, ValueError) as exc:
                load_errors.append(f"{path}: {exc}")
                task = {}
    execution = {field: [] for field in LOG_FIELDS}
    for document in documents:
        log = document.get("execution", {})
        if not isinstance(log, dict):
            load_errors.append("execution må være et objekt")
            continue
        if set(log) - set(LOG_FIELDS):
            load_errors.append("execution har ukjente felt")
        for field in LOG_FIELDS:
            entries = log.get(field, [])
            if not isinstance(entries, list):
                load_errors.append(f"execution.{field} må være en liste")
            else:
                execution[field].extend(entries)
    engine = Composition(nodes, execution)
    engine.errors.extend(load_errors)
    return engine, task


# ---------------------------------------------------------------- validate

def validate(taskdir=None):
    kb, pk, ls = load_all()
    errors, warnings = [], []
    composition, _ = composition_context(kb, pk, taskdir)
    comp_errors, comp_warnings = composition.validate()
    errors.extend(comp_errors)
    warnings.extend(comp_warnings)
    refs = all_purpose_refs(kb, pk)
    lesson_refs = {l["lessonRef"] for l in ls["lessons"]}

    for p in pk["packages"]:
        pref = p.get("packageRef", "?")
        for key in ("packageRef", "title", "summary", "status", "triggers", "purposes", "requiredArtifacts", "lessonRefs"):
            if key not in p:
                errors.append(f"{pref}: mangler felt '{key}'")
        for n in p.get("purposes", []):
            nref = n.get("purposeRef", "?")
            if not nref.startswith("purpose://"):
                errors.append(f"{pref}/{nref}: purposeRef må starte med purpose://")
            if n.get("parentRef") not in refs:
                errors.append(f"{pref}/{nref}: parentRef '{n.get('parentRef')}' finnes ikke i Book 23 eller pakkene")
            g = n.get("goal") or {}
            for key in ("goalRef", "lifecycle", "outcome", "successSignals", "verifier"):
                if not g.get(key):
                    errors.append(f"{pref}/{nref}: goal mangler '{key}' (goalRequirement i Book 23)")
            tests = n.get("derivedTests") or []
            if not tests:
                errors.append(f"{pref}/{nref}: ingen derivedTests — et formål uten test er en intensjon")
            for t in tests:
                for key in ("testRef", "kind", "description", "how", "evidence"):
                    if not t.get(key):
                        errors.append(f"{pref}/{nref}/{t.get('testRef','?')}: test mangler '{key}'")
        for lr in p.get("lessonRefs", []):
            if lr not in lesson_refs:
                errors.append(f"{pref}: lessonRef '{lr}' finnes ikke i registeret")
        for ir in p.get("inheritedPurposeRefs", []):
            if ir not in refs:
                errors.append(f"{pref}: inheritedPurposeRef '{ir}' finnes ikke")

    for l in ls["lessons"]:
        lref = l.get("lessonRef", "?")
        for key in ls["entryRules"]["required"]:
            if not l.get(key):
                errors.append(f"{lref}: mangler '{key}'")
        for pr in l.get("purposeRefs", []):
            if pr not in refs:
                errors.append(f"{lref}: purposeRef '{pr}' finnes ikke")
        if l.get("cause", "").strip().lower() in ("", "?"):
            warnings.append(f"{lref}: cause er tom — skriv 'ukjent' eksplisitt")

    if taskdir:
        errors += validate_taskdir(taskdir, pk)

    for w in warnings:
        print("ADVARSEL:", w)
    for e in errors:
        print("FEIL:", e)
    n_p = sum(len(p["purposes"]) for p in pk["packages"])
    kb_refs = {n["purposeRef"] for n in kb.get("nodes", [])}
    missing_kb = sum(ref in kb_refs for ref in composition.missing_composition)
    print(f"Composition regel 1: {len(composition.missing_composition)} noder uten composition "
          f"({missing_kb} Book 23-noder) — advarsel, ingen default")
    print(f"{len(pk['packages'])} pakker, {n_p} pakkeformål, {len(ls['lessons'])} lærdommer, {len(kb.get('nodes', []))} Book 23-noder — "
          f"{'OK' if not errors else str(len(errors)) + ' feil'}")
    return 0 if not errors else 1


def read_status(taskdir):
    """STATUS.md: linjer som '- G1: godkjent 2026-09-04' / '- G1-GUI: venter'."""
    path = os.path.join(taskdir, "STATUS.md")
    status = {g: "mangler" for g in GATES}
    surfaces, tags = set(), set()
    if not os.path.exists(path):
        return status, surfaces, tags
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\s*-\s*(G1-GUI|G1|G2|G3)\s*:\s*(\S+)", line)
        if m:
            status[m.group(1)] = m.group(2).lower()
        m = re.match(r"\s*-\s*surfaces\s*:\s*(.*)", line, re.I)
        if m:
            surfaces = {s.strip() for s in m.group(1).split(",") if s.strip()}
        m = re.match(r"\s*-\s*tags\s*:\s*(.*)", line, re.I)
        if m:
            tags = {s.strip() for s in m.group(1).split(",") if s.strip()}
    return status, surfaces, tags



def declaration_satisfies(taskdir, artifact):
    """Noen artefakter er betinget: de kreves bare når en bestemt vei er brukt.

    Alternativet er ikke aa hoppe over sjekken, men aa kreve at valget er skrevet ned.
    `satisfiedByDeclaration` peker paa en fil og en overskrift; under overskriften maa det
    staa minst `minItems` punkter. En tom eller manglende erklaering teller ikke.

    Returnerer (ok, forklaring). Forklaringen sier hvordan kravet kan oppfylles.
    """
    spec = artifact.get("satisfiedByDeclaration")
    if not spec:
        return False, ""
    path = os.path.join(taskdir, spec["file"])
    marker = spec["marker"]
    need = int(spec.get("minItems", 1))
    hint = (f"alternativet er en erklaering under '{marker}' i {spec['file']}, "
            f"med minst {need} punkt (kule- eller nummerliste) om hva skjelettet ikke kan rendre")
    if not os.path.exists(path):
        return False, hint
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return False, hint
    idx = text.find(marker)
    if idx < 0:
        return False, hint
    tail = text[idx + len(marker):]
    stop = re.search(r"^#{1,6} ", tail, re.M)
    if stop:
        tail = tail[:stop.start()]
    items = [ln for ln in tail.splitlines() if re.match(r"\s*(?:[-*]|\d+[.)]) \S", ln)]
    if len(items) < need:
        return False, (f"erklaeringen under '{marker}' i {spec['file']} har {len(items)} punkt, "
                       f"det kreves {need}")
    return True, ""


def validate_taskdir(taskdir, pk):
    errors = []
    if not os.path.isdir(taskdir):
        return [f"oppgavemappe finnes ikke: {taskdir}"]
    status, surfaces, tags = read_status(taskdir)
    attached = attach(pk, tags, surfaces)
    gui = bool(surfaces & GUI_SURFACES)
    # Port-regler: en port kan bare være 'godkjent' hvis artefaktene for porten finnes.
    for p in attached:
        for a in p.get("requiredArtifacts", []):
            gate = a["gate"]
            if status.get(gate) == "godkjent":
                ap = os.path.join(taskdir, a["path"])
                exists = os.path.isdir(ap) and any(os.scandir(ap)) if a["path"].endswith("/") else os.path.exists(ap)
                if not exists:
                    ok, why = declaration_satisfies(taskdir, a)
                    if ok:
                        continue
                    msg = f"{os.path.basename(taskdir)}: {gate} er satt til godkjent, men artefakt '{a['path']}' ({a['description']}) mangler"
                    if why:
                        msg += f" — {why}"
                    errors.append(msg)
    if gui and status.get("G2") == "godkjent" and status.get("G1-GUI") != "godkjent":
        errors.append(f"{os.path.basename(taskdir)}: GUI-oppgave med G2 godkjent uten G1-GUI godkjent — bilde før kode")
    if status.get("G1") != "godkjent" and status.get("G2") == "godkjent":
        errors.append(f"{os.path.basename(taskdir)}: G2 godkjent før G1 — ingen plan før formålet er godkjent")
    spec = os.path.join(taskdir, "FORMAALSSPEC.md")
    if os.path.exists(spec):
        text = open(spec, encoding="utf-8").read()
        if gui and "images/" not in text:
            errors.append(f"{os.path.basename(taskdir)}: GUI-oppgave, men FORMAALSSPEC.md §3 refererer ingen images/-fil")
        if re.search(r"\bTBD\b|\bTODO\b", text) and status.get("G1") == "godkjent":
            errors.append(f"{os.path.basename(taskdir)}: G1 godkjent, men FORMAALSSPEC.md inneholder TBD/TODO")
    return errors


# ---------------------------------------------------------------- lookup

def _match(trig, values):
    return "*" in trig or bool(set(trig) & values)


def attach(pk, tags, surfaces):
    out = []
    for p in pk["packages"]:
        t = p.get("triggers", {})
        if p["packageRef"] in pk.get("alwaysAttach", []) or _match(t.get("tags", []), tags) or _match(t.get("surfaces", []), surfaces):
            out.append(p)
    return out


def matching_lessons(ls, tags, surfaces, purpose_refs):
    out = []
    keys = tags | surfaces
    for l in ls["lessons"]:
        if set(l.get("tags", [])) & keys or set(l.get("purposeRefs", [])) & purpose_refs:
            out.append(l)
    return out


def kb_matches(kb, tags):
    """Book 23-noder hvis aliases/tokens treffer tags (enkel leksikalsk match, kun forslag)."""
    hits = []
    low = {t.lower() for t in tags}
    for n in kb.get("nodes", []):
        mh = n.get("matchingHints", {})
        words = {w.lower() for w in mh.get("tokens", [])}
        aliases = " ".join(mh.get("aliases", [])).lower()
        if words & low or any(t in aliases for t in low):
            hits.append(n)
    return hits


def lookup(tags, surfaces, as_markdown=False):
    kb, pk, ls = load_all()
    tags, surfaces = set(tags), set(surfaces)
    attached = attach(pk, tags, surfaces)
    prefs = {n["purposeRef"] for p in attached for n in p["purposes"]}
    for p in attached:
        prefs |= set(p.get("inheritedPurposeRefs", []))
    lessons = matching_lessons(ls, tags, surfaces, prefs)
    kbhits = kb_matches(kb, tags)
    return render_lookup(attached, lessons, kbhits, as_markdown)


def render_lookup(attached, lessons, kbhits, md):
    lines = []
    h = (lambda s: f"## {s}") if md else (lambda s: f"=== {s} ===")
    lines.append(h("Formålspakker som festes"))
    for p in attached:
        lines.append(f"- **{p['packageRef']}** — {p['title']}" if md else f"* {p['packageRef']} — {p['title']}")
        for n in p["purposes"]:
            lines.append(f"    - {n['purposeRef']}: {n['goal']['outcome']}")
            for t in n.get("derivedTests", []):
                lines.append(f"        - test {t['testRef']} [{t['kind']}]: {t['description']} → {t['evidence']}")
        for a in p.get("requiredArtifacts", []):
            lines.append(f"    - artefakt {a['path']} (port {a['gate']}): {a['description']}")
    lines.append("")
    lines.append(h("Lærdommer du må lese før dekomponering"))
    if not lessons:
        lines.append("(ingen treff — vurder om tags er for smale)")
    for l in lessons:
        lines.append(f"- **{l['lessonRef']}** ({l['date']}, {l['severity']}): {l['symptom']}" if md else f"* {l['lessonRef']} ({l['date']}, {l['severity']}): {l['symptom']}")
        lines.append(f"    - forebygging: {l['prevention']}")
    lines.append("")
    lines.append(h("Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)"))
    for n in kbhits:
        lines.append(f"- {n['purposeRef']} [{n['status']}] — {n['title']}")
    return "\n".join(lines)


# ---------------------------------------------------------------- new

SPEC_TEMPLATE = """# Formålsspesifikasjon — {title}

Oppgavemappe: `{dirname}` · Opprettet {date} · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> {intent}

| Påstand i intensjonen / antatt kapabilitet | Audit (retrieved / recalled / unavailable / contradicted) | Kilde |
|---|---|---|
| | | |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.{slug}.root | | | | | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
-

Kapabiliteter og avhengigheter oppgaven bygger på (hver med kilde og hva den ikke dekker):
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| | | | |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
{gui_note}
| Leveranse | Type (bilde / fil / testutdata / kjørende flate) | Hvor | Referanse (images/…-v1.png osv.) | Godkjent |
|---|---|---|---|---|
| | | | | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

{lookup}

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
{tests}

## 6. Åpne spørsmål til Kjetil

1.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | {date} | Opprettet | Losen |
"""

STATUS_TEMPLATE = """# STATUS — {title}

- surfaces: {surfaces}
- tags: {tags}

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: {gui}        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- {date}: opprettet
"""


def new_task(slug, intent, tags, surfaces):
    date = _dt.date.today().isoformat()
    dirname = f"PDD_{slug}_{date}"
    taskdir = os.path.join(DELIVERABLES, dirname)
    if os.path.exists(taskdir):
        print("finnes allerede:", taskdir)
        return 1
    os.makedirs(os.path.join(taskdir, "images"))
    kb, pk, ls = load_all()
    tags_s, surf_s = set(tags), set(surfaces)
    attached = attach(pk, tags_s, surf_s)
    prefs = {n["purposeRef"] for p in attached for n in p["purposes"]}
    lessons = matching_lessons(ls, tags_s, surf_s, prefs)
    look = render_lookup(attached, lessons, kb_matches(kb, tags_s), md=True)
    tests = []
    for p in attached:
        for n in p["purposes"]:
            for t in n.get("derivedTests", []):
                tests.append(f"| {t['testRef']} | {n['purposeRef']} | {t['how']} | {t['evidence']} | venter |")
    gui = bool(surf_s & GUI_SURFACES)
    gui_note = ("**GUI-oppgave:** hver flate og hver viktig tilstand (tom, fylt, feil) må ha et rendret bilde i `images/` "
                "som Kjetil har godkjent før G1-GUI. Porthole-preview av skeleton-JSON når formatet tillater det; ellers mockup med "
                "eksplisitt liste over hva dagens skeleton ikke kan rendre.") if gui else "(ingen GUI-flate deklarert — sett `surfaces` i STATUS.md hvis det er feil)"
    title = slug.replace("-", " ")
    with open(os.path.join(taskdir, "FORMAALSSPEC.md"), "w", encoding="utf-8") as fh:
        fh.write(SPEC_TEMPLATE.format(title=title, dirname=dirname, date=date, intent=intent, slug=slug,
                                      gui_note=gui_note, lookup=look, tests="\n".join(tests) or "| | | | | |"))
    with open(os.path.join(taskdir, "STATUS.md"), "w", encoding="utf-8") as fh:
        fh.write(STATUS_TEMPLATE.format(title=title, surfaces=", ".join(sorted(surf_s)), tags=", ".join(sorted(tags_s)),
                                        gui="venter" if gui else "ikke relevant", date=date))
    with open(os.path.join(taskdir, "images", "README.md"), "w", encoding="utf-8") as fh:
        fh.write("Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.\n")
    print("opprettet", taskdir)
    print(look)
    return 0


# ---------------------------------------------------------------- gates

def gates(taskdir):
    kb, pk, _ = load_all()
    status, surfaces, tags = read_status(taskdir)
    attached = attach(pk, tags, surfaces)
    print(f"{os.path.basename(taskdir)} — surfaces={sorted(surfaces)} tags={sorted(tags)}")
    for g in GATES:
        need = [a for p in attached for a in p.get("requiredArtifacts", []) if a["gate"] == g]
        have = []
        for a in need:
            ap = os.path.join(taskdir, a["path"])
            ok = (os.path.isdir(ap) and any(f for f in os.listdir(ap) if f != "README.md")) if a["path"].endswith("/") else os.path.exists(ap)
            have.append(f"{'✓' if ok else '✗'} {a['path']}")
        print(f"  {g:7} {status.get(g, 'mangler'):18} artefakter: {', '.join(have) or '(ingen krevd)'}")
    errs = validate_taskdir(taskdir, pk)
    composition, task = composition_context(kb, pk, taskdir)
    comp_errors, _ = composition.validate()
    errs.extend(comp_errors)
    # Evaluate task purposes and attached collections, including composed ancestors.
    scope = {n["purposeRef"] for n in task.get("nodes", [])
             if isinstance(n, dict) and isinstance(n.get("purposeRef"), str)}
    scope.update(n["purposeRef"] for p in attached for n in p.get("purposes", []))
    scope.update(ref for p in attached for ref in p.get("inheritedPurposeRefs", []))
    scope.update(r["purposeRef"] for r in composition.execution.get("reports", [])
                 if isinstance(r, dict) and isinstance(r.get("purposeRef"), str))
    for ref in list(scope):
        seen = set()
        while isinstance(ref, str) and ref in composition.nodes and ref not in seen:
            seen.add(ref)
            if "composition" in composition.nodes[ref]:
                scope.add(ref)
            ref = composition.nodes[ref].get("parentRef")
    collections = sorted(ref for ref in scope if isinstance(ref, str) and ref in composition.nodes
                         and (composition.children.get(ref) or "composition" in composition.nodes[ref]))
    results = {}
    if collections:
        print("  Formålssammensetning (utledet fra registrert kjøringslogg):")
        for ref in collections:
            result = composition.evaluate(ref)
            results[ref] = result
            print(f"    {ref}: {result['state']} — {result['reason']}"
                  + (f"; branchRef={result['branchRef']}" if "branchRef" in result else ""))
    else:
        print(f"  Formålssammensetning: unverified — ingen samlinger i oppgavens omfang; bruk {COMPOSITION_FILE}")
    # A disjunction may be green with a red/unverified unselected collection.
    # Descendants are displayed, but only top-level scoped collections form ports.
    roots = set(collections)
    for ref in collections:
        parent = composition.nodes[ref].get("parentRef")
        seen = {ref}
        while isinstance(parent, str) and parent in composition.nodes and parent not in seen:
            seen.add(parent)
            if parent in results:
                roots.discard(ref)
                break
            parent = composition.nodes[parent].get("parentRef")
    states = {results[ref]["state"] for ref in roots}
    # Preserve blocked even when another collection is red. Errors remain visible.
    if "blocked" in states:
        overall = "blocked"
    elif errs or "red" in states:
        overall = "red"
    elif not results or "unverified" in states:
        overall = "unverified"
    else:
        overall = "green"
    print(f"  Composition-port: {overall}")
    for e in errs:
        print("  FEIL:", e)
    return {"green": 0, "red": 1, "blocked": 2, "unverified": 3}[overall]


# ---------------------------------------------------------------- lesson add

def lesson_add(taskdir):
    ls = _load(LESSONS_PATH)
    print("Ny lærdom (tomt felt avbryter).")
    entry = {}
    for key in ["lessonRef", "symptom", "cause", "prevention", "purposeRefs", "tags", "severity"]:
        val = input(f"{key}: ").strip()
        if not val:
            print("avbrutt"); return 1
        entry[key] = [v.strip() for v in val.split(",")] if key in ("purposeRefs", "tags") else val
    entry["date"] = _dt.date.today().isoformat()
    entry["source"] = os.path.relpath(taskdir, REPO)
    ls["lessons"].append(entry)
    with open(LESSONS_PATH, "w", encoding="utf-8") as fh:
        json.dump(ls, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("lagt til", entry["lessonRef"], "— kjør validate")
    return 0


# ---------------------------------------------------------------- main

def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("taskdir", nargs="?")
    lk = sub.add_parser("lookup"); lk.add_argument("--tags", nargs="*", default=[]); lk.add_argument("--surfaces", nargs="*", default=[]); lk.add_argument("--md", action="store_true")
    nw = sub.add_parser("new"); nw.add_argument("slug"); nw.add_argument("--intent", required=True); nw.add_argument("--tags", nargs="*", default=[]); nw.add_argument("--surfaces", nargs="*", default=[])
    g = sub.add_parser("gates"); g.add_argument("taskdir")
    la = sub.add_parser("lesson"); la.add_argument("action", choices=["add"]); la.add_argument("taskdir")
    ju = sub.add_parser("judge", help="rask menneskevurdering av en frosset G1-liste")
    ju.add_argument("taskdir"); ju.add_argument("--run"); ju.add_argument("--batch-size", type=int, default=0, help="0 = alle; positivt tall for delrunder")
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        return validate(a.taskdir)
    if a.cmd == "lookup":
        print(lookup(a.tags, a.surfaces, a.md)); return 0
    if a.cmd == "new":
        return new_task(a.slug, a.intent, a.tags, a.surfaces)
    if a.cmd == "gates":
        return gates(a.taskdir)
    if a.cmd == "lesson":
        return lesson_add(a.taskdir)
    if a.cmd == "judge":
        from purpose_judgments import judge
        try:
            return judge(a.taskdir, a.run, a.batch_size)
        except (ValueError, OSError) as exc:
            print("FEIL:", exc); return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
