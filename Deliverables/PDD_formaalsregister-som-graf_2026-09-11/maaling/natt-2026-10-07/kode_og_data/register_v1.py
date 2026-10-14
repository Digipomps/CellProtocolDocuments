# -*- coding: utf-8 -*-
"""Register v1-kandidat: nattens union (natt_trening.load_union) + Kjetils avgjørelser 2026-10-07.

Avgjørelser (svar på de fire spørsmålene i DOMMER_RUNDE2_FUNN.md, Kjetil 2026-10-07):
 1. «ja» -> Samtalehandlinger er formål, men foreslår aldri en flate (neverSurface, samme mekanisme som facet-only
    for flater). Åpne, godta, avvise, presenter deg. Hva et ja/nei gjelder hentes fra det som er aktivt i perspektivet.
 2. «husker ikke - tror det var meningen å forklare 'the AI figure itself'» -> Tittelen lurte. librarian.explain-haven
    splittes: «presenter deg selv» (AI-figuren: navn, rolle, hva den gjør) blir eget formål; explain-haven beholder HAVEN.
 3. «ja» -> Kandidatformål: foreslå problemstilling; eksportere data til filformat; regelen verb -> formål, argumenter
    fra perspektivet (regelen er en matcherregel, se dekomp.py, ikke en node).
 4. «ja» -> frossen R4 kjøres på butler korpus v2 med etikett-kart (uavhengig_v2.py).

Ingen av nodene her er skrevet inn i Book 23. De er kandidater i et eksperiment-overlay; endring i Book blir forslag.
"""
from __future__ import annotations
import json
from pathlib import Path
import natt_trening as T

HERE = Path(__file__).resolve().parent

NEW_NODES = [
    # ---- samtalehandlinger (avgjørelse 1) ----
    {"ref": "purpose://conversation", "parent": None, "title": "Conversation acts",
     "desc": "Acts that steer the conversation itself rather than asking for a capability. They never propose a surface; what they refer to is resolved from what is active in the perspective.",
     "neverSurface": True},
    {"ref": "purpose://conversation.open", "parent": "purpose://conversation", "title": "Open a conversation or request",
     "desc": "Greeting or opening that starts a request. The assistant answers and invites the request; nothing is proposed.",
     "neverSurface": True},
    {"ref": "purpose://conversation.accept", "parent": "purpose://conversation", "title": "Accept what is proposed",
     "desc": "Agree to, confirm or go ahead with the proposal, claim or step that is active in the perspective.",
     "neverSurface": True},
    {"ref": "purpose://conversation.reject", "parent": "purpose://conversation", "title": "Reject what is proposed",
     "desc": "Decline, refuse or do not accept the proposal, claim or step that is active in the perspective.",
     "neverSurface": True},
    {"ref": "purpose://conversation.introduce-self", "parent": "purpose://conversation", "title": "Introduce yourself",
     "desc": "The AI figure presents itself: its name, what it does, what role it has and what it can and cannot do.",
     "neverSurface": True},
    # ---- kandidatformål (avgjørelse 3) ----
    {"ref": "purpose://librarian.propose-research-question", "parent": "purpose://knowledge", "title": "Propose a research question",
     "desc": "Suggest a problem statement or research question worth investigating, grounded in what the commons holds and where its gaps are."},
    {"ref": "purpose://digital-work.export-to-file", "parent": "purpose://digital-work", "title": "Export data to a file format",
     "desc": "Export and download data the owner may access (for example a table or list) to a file format such as spreadsheet, CSV or JSON."},
]

# avgjørelse 2: explain-haven mister AI-figur-halvdelen og «hvem er du»-aliaset
EDITS = {
    "purpose://librarian.explain-haven": {
        "title": "Explain HAVEN",
        "desc": "Explain HAVEN's concepts, rules and maturity with the right status (principle / implemented / tested / internal prototype / research direction).",
        "aliases_remove": ["hvem er du", "hva kan du"],
    },
}


def load_register(overlays=()):
    """Union + v1-kandidat. overlays: liste av dict {ref: {aliases_add, tokens_add, desc_add, desc_replace}} (tuning)."""
    nodes = T.load_union()
    for ref, e in EDITS.items():
        n = nodes[ref]
        n["title"] = e.get("title", n["title"]); n["desc"] = e.get("desc", n["desc"])
        n["aliases"] = [a for a in n["aliases"] if a not in e.get("aliases_remove", [])]
    for nn in NEW_NODES:
        nodes[nn["ref"]] = {"ref": nn["ref"], "parent": nn["parent"], "title": nn["title"], "desc": nn["desc"],
                            "aliases": [], "tokens": [], "signals": [], "outcome": "", "src": "V1",
                            "facetOnly": False, "neverSurface": nn.get("neverSurface", False)}
    for n in nodes.values():
        n.setdefault("neverSurface", False)
    for ov in overlays:
        for ref, o in ov.items():
            if ref not in nodes: continue
            n = nodes[ref]
            n["aliases"] = n["aliases"] + list(o.get("aliases_add", []))
            n["tokens"] = n["tokens"] + list(o.get("tokens_add", []))
            if o.get("desc_replace"): n["desc"] = o["desc_replace"]
            if o.get("desc_add"): n["desc"] = (n["desc"] + " " + o["desc_add"]).strip()
    return nodes


# Gull fra Kjetils dom i runde 2 + avgjørelsene over, brukt for å oppdatere nattkorpusets etiketter (dev-sett).
GOLD_UPDATES = {
    "hei": "purpose://conversation.open",
    "ja": "purpose://conversation.accept",
    "nei": "purpose://conversation.reject",
    "hvem er du": "purpose://conversation.introduce-self",
    "foreslå et forskningsspørsmål": "purpose://librarian.propose-research-question",
    "ønske: eksport til regneark": "purpose://digital-work.export-to-file",
    "personvern": "purpose://self-determination.data",
    "hvordan vet vi at det ikke er funnet på": "purpose://self-determination.data.verifiability",
}


def dev_corpus():
    """Nattkorpuset (150) med etiketter rettet etter Kjetils dom. Bare der dommen gjelder samme ytring.
    Saker der Kjetil svarte «Ingen av disse» uten at formålet finnes (send skjemaet, noen må se på dette) står som før,
    merket i KJETIL_INGEN."""
    from natt_korpus import KORPUS
    out = []
    for f, t, g, lc in KORPUS:
        out.append((f, t, GOLD_UPDATES.get(t, g), lc))
    return out
