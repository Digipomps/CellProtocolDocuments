#!/usr/bin/env python3
"""Bygger maaling/korpus/korpus-v1.jsonl + maaling/etikett-kart.json fra de fire generatorpersonaene.
Deterministisk: samme raw.json gir samme fil (id-rekkefølge = persona, så linjeorden)."""
import json, hashlib
raw = json.load(open("raw.json"))
ORDER = ["p1-grunder", "p2-pensjonist", "p3-internasjonal", "p4-driftsleder"]

# Etikett → hva Butler BURDE gjøre, i produksjonens egne navn (fra PromptPurposeLab-fasiten og kildekoden 77a922bc).
H = {  # hjelper: suggestion.kind == intentKind, purposeRef == ref
 "H.invite": ("invite_person", "personal.chat.assist.invite"),
 "H.poll": ("create_poll", "personal.chat.assist.poll"),
 "H.idea": ("idea_capture", "personal.chat.assist.idea.capture"),
 "H.workitem": ("work_item", "personal.chat.assist.work-item.capture"),
 "H.project": ("project", "personal.chat.assist.project"),
 "H.todo": ("todo", "personal.chat.assist.todo"),
 "H.reminder": ("reminder", "personal.chat.assist.reminder"),
 "H.meeting": ("schedule_meeting", "personal.chat.assist.meeting.schedule"),
 "H.video": ("meeting_video", "personal.chat.assist.meeting.video"),
 "H.agent": ("agent_action", "personal.chat.assist.local-agent-action"),
 "H.onboarding": ("guided_onboarding", "personal.chat.assist.guided-onboarding"),
 "H.advisory": ("advisory_report", "personal.chat.assist.advisory-report"),
 "H.capability": ("capability_request", "personal.chat.assist.capability-request"),
}
S = {  # flate: suggestion.kind == resource_match og purposeRef i settet (likeverdige navn fra kildekoden)
 "S.agenda": ["conference.agenda.view", "arendalsuka.agenda.personal-plan"],
 "S.docs": ["cellprotocol.docs.lookup", "knowledge.demo.kallimachos", "personal.chat.assist.docs-rag"],
 "S.map": ["personal.chat.assist.spatial-query", "knowledge.map.visualize"],
 "S.agreement": [],  # ingen flate i katalogen erklærer dette formålet (sjekkes mot katalog.json) → graf-hull
 "S.profilepage": ["personal.profile.page.create"],
 "S.publish": ["personal.public-presence.publish"],
 "S.music": ["personal.music.publish", "rag.media.publish"],
 "S.mermaid": ["personal.diagram.mermaid.render", "graph.subgraph.mermaid"],
 "S.entity": ["personal.entity.relations.manage"],
 "S.admin": ["admin.scaffold-operations.observe", "admin.cell-lifecycle.cleanup-review", "admin.identity.vc.request"],
 "S.aigateway": ["personal.ai.gateway.configure"],
 "S.meetplace": ["purpose://event.meeting-place.agree", "arendalsuka.meeting-place.agree"],
 "S.commerce": ["arendalsuka.local-commerce.discover"],
 "S.networking": ["arendalsuka.social-networking.meet"],
 "S.vote": ["purpose://democracy.vote.participate", "arendalsuka.democracy.vote"],
 "S.cellconfig": ["purpose://capability.construct-cellconfiguration", "goal.capability.construct-cellconfiguration", "purpose-node.capability.construct-cellconfiguration"],
}
kart = {}
for k, (kind, ref) in H.items():
    kart[k] = {"forventet": "hjelper", "intentKind": kind, "purposeRefs": [ref]}
for k, refs in S.items():
    kart[k] = {"forventet": "flate", "intentKind": "resource_match", "purposeRefs": refs}
kart["M.meta"] = {"forventet": "meta", "purposeRefs": [], "merknad": "riktig = ingen handling foreslått (Butler svarer om seg selv)"}
kart["C.clarify"] = {"forventet": "avklaring", "purposeRefs": [], "merknad": "riktig = status needs_clarification"}
kart["N.none"] = {"forventet": "ingen", "purposeRefs": [], "merknad": "riktig = ingen forslag (unknown/low_confidence)"}
kart["G.gap"] = {"forventet": "hull", "purposeRefs": [], "merknad": "riktig = ingen feil flate; capability_request godtas"}

def ref_for(label):
    k = kart[label]
    if k["forventet"] in ("hjelper", "flate"):
        return (k["purposeRefs"] or ["none-i-katalogen"])[0]
    return "none"

rows = []
n = 0
for p in ORDER:
    for r in raw[p]:
        n += 1
        rid = f"k1-{n:04d}"
        h = int(hashlib.sha256(rid.encode()).hexdigest()[:8], 16)
        rows.append({"id": rid, "text": r["text"], "lang": r["lang"], "style": r["style"], "label": r["label"],
                     "intendedPurposeRef": ref_for(r["label"]), "split": "holdout" if h % 4 == 0 else "trening",
                     "generatedBy": f"claude-subagent-{p}-2026-09-23"})
with open("korpus-v1.jsonl", "w") as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
json.dump({"schema": "haven.butler-maaling.etikett-kart.v1", "kilde": "PromptPurposeLab-fasit + grep i CellScaffold 77a922bc", "etiketter": kart},
          open("etikett-kart.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(rows), Counter(r["split"] for r in rows), Counter(r["lang"] for r in rows))
print(Counter(r["style"] for r in rows))
print("holdout per etikett min/max:", min(Counter(r["label"] for r in rows if r["split"]=="holdout").values()), max(Counter(r["label"] for r in rows if r["split"]=="holdout").values()))
