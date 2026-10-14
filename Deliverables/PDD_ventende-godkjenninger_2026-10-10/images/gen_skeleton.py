#!/usr/bin/env python3
"""Kandidat-skjelett for «Venter på deg» (G1-GUI), PDD_ventende-godkjenninger.

Bygger videre på Codex' «Oversikt» (gren codex/arbeidsbenk-oversikt-20261009,
WorkItemOverviewConfiguration.swift): samme seksjon og samme keypaths
(workItems.state.overview.*, workItems.setStatus, workItems.overview.ask).
Nytt i raden: kilde, frist, «Hvor»-peker og knappetekst per rad (labelKeypath).
Bare elementer som finnes i dagens skjelettformat brukes.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "skeleton")
os.makedirs(OUT, exist_ok=True)
S = "workItems.state.overview"
GREY = "#6E6E73"
RED = "#C0392B"


def text(t=None, keypath=None, **mods):
    body = {}
    if t is not None:
        body["text"] = t
    if keypath is not None:
        body["keypath"] = keypath
    if mods:
        body["modifiers"] = mods
    return {"Text": body}


def vis(keypath, equals=True):
    return {"visibility": {"when": {"scope": "item", "keypath": keypath, "equals": equals}}}


def button(keypath, label="", payload=None, label_keypath=None, **mods):
    body = {"keypath": keypath, "label": label}
    if payload:
        body["payloadKeypath"] = payload
    if label_keypath:
        body["labelKeypath"] = label_keypath
    if mods:
        body["modifiers"] = mods
    return {"Button": body}


def hstack(*els, spacing=8):
    return {"HStack": {"spacing": spacing, "elements": list(els)}}


def decision_row():
    return {"VStack": {"spacing": 6, "elements": [
        hstack(text(keypath="sourceLabel", fontStyle="caption", foregroundColor=GREY),
               text(keypath="ageText", fontStyle="caption", foregroundColor=GREY),
               text(keypath="deadlineText", fontStyle="caption", fontWeight="semibold", foregroundColor=RED,
                    **vis("hasDeadline"))),
        text(keypath="title", fontStyle="headline"),
        text(keypath="summary", fontStyle="callout"),
        hstack(text("Hvor:", fontStyle="caption", fontWeight="semibold"),
               text(keypath="whereText", fontStyle="caption", fontDesign="monospaced", textSelection=True)),
        hstack(text("Ja utløser:", fontStyle="caption", fontWeight="semibold"),
               text(keypath="nextAction", fontStyle="caption")),
        hstack(
            button("workItems.setStatus", "Ja", payload="yesPayload", label_keypath="yesLabel",
                   controlStyle="borderedProminent", **vis("hasYes")),
            button("workItems.setStatus", "Nei", payload="noPayload", label_keypath="noLabel",
                   controlStyle="bordered", **vis("hasNo")),
            button("workItems.setStatus", "Merk som løst", payload="resolvedPayload",
                   controlStyle="bordered", **vis("hasYes", False)),
            button("workItems.overview.ask", "Spør", payload="askPayload", controlStyle="bordered"),
            {"Button": {"keypath": "", "label": "Åpne", "urlKeypath": "whereURL",
                        "modifiers": {"controlStyle": "bordered", **vis("hasURL")}}},
        ),
    ]}}


def card(title, lst, row, extra=()):
    header = hstack(text(title, fontStyle="title3", fontWeight="semibold"),
                    text(keypath=f"{S}.{lst}Count", fontStyle="title3", foregroundColor=GREY))
    return {"Section": {"header": header, "content": [
        text(keypath=f"{S}.{lst}EmptyText", foregroundColor=GREY),
        {"List": {"keypath": f"{S}.{lst}", "flowElementSkeleton": row}},
        *extra,
    ]}}


def mirror_row():
    return {"VStack": {"spacing": 4, "elements": [
        hstack(text(keypath="sourceLabel", fontStyle="caption", foregroundColor=GREY), text(keypath="title")),
        text(keypath="detail", fontStyle="caption", foregroundColor=GREY)]}}


skeleton = {"Section": {
    "header": text("Oversikt", fontStyle="title2", fontWeight="bold"),
    "modifiers": {"styleRole": "workbench-overview", "styleClasses": ["haven-workbench-overview"]},
    "content": [
        text(keypath=f"{S}.mirrorFreshness", fontStyle="caption", foregroundColor=GREY),
        text(keypath=f"{S}.mirrorWarningText", fontStyle="caption", foregroundColor=RED),
        card("Venter på deg", "needsYou", decision_row(), [
            text(keypath=f"{S}.oldestNeedsYouText", fontStyle="caption", foregroundColor=GREY)]),
        card("Kjører nå", "running", mirror_row()),
    ]}}

json.dump(skeleton, open(os.path.join(OUT, "venter-paa-deg.skeleton.json"), "w"), ensure_ascii=False, indent=1)


def row(i, source, age, title, summary, where, next_action, yes=None, no=None, deadline=None):
    r = {"sourceLabel": source, "ageText": age, "title": title, "summary": summary, "whereText": where,
         "nextAction": next_action, "hasDeadline": bool(deadline), "deadlineText": deadline or "",
         "hasYes": bool(yes), "yesLabel": yes or "", "hasNo": bool(no), "noLabel": no or "",
         "yesPayload": {"id": i, "status": "done", "decisionComment": "JA"},
         "noPayload": {"id": i, "status": "wont-do", "decisionComment": "NEI"},
         "resolvedPayload": {"id": i, "status": "done"},
         "askPayload": {"id": i}, "hasURL": where.startswith("https://"),
         "whereURL": where if where.startswith("https://") else ""}
    return r


needs = [
    row("hd-HD-0169", "Deploykø · HD-0169 · tråden «PR review og merge»", "for 21 t siden",
        "Kjør Sprout-fornyelsen på staging igjen",
        "Pakkefeilen er rettet. Skriptet må kjøres fra din Mac; det kan ikke trykkes herfra.",
        "cd /Users/kjetil/Build/Digipomps/HAVEN && bash HAVEN-Deploy/_handoff/HD-0169/KJOR-ALT.sh",
        "Fornyet Sprout-beskrivelse før utløp; HD-0141 kan lukkes", deadline="Frist 13.10 12:00Z"),
    row("hd-HD-0207", "Deploykø · HD-0207", "for 8 t siden",
        "Bekreft at APNs-nøkkel HW58HG7D3C er «Sandbox & Production»",
        "Sjekkes i Apple Developer → Keys.",
        "https://developer.apple.com/account/resources/authkeys/list",
        "Invitasjon-tråden kjører første ekte push-test fra iPhone mot prod",
        yes="Bekreftet", no="Ikke riktig"),
    row("hd-HD-0013", "Deploykø · forkastet · HD-0013", "for 33 d siden",
        "WP3 ekte Codex read-only røykprøve stoppet",
        "Stoppet for inspeksjon før ny prøve (HANDOFF_REQUIRED).",
        "python3 tools/hd.py task set HD-0013 --status READY",
        "Jobben går tilbake i køen (READY) med notat «køet på nytt fra arbeidsbenken»",
        yes="Køe på nytt", no="La ligge"),
    row("pkg-admin-scaffold-m4", "Leveransegap · avvist pakke", "for 87 d siden",
        "codex/admin-scaffold-m4 avvist (263 filer)",
        "Gammel, bred integrasjonsgren; main har flyttet seg hundrevis av commits.",
        "python3 tools/hd.py gap decide --branch codex/admin-scaffold-m4 --decision INN",
        "Ja: avvisningen står og raden forsvinner. Nei: pakken går inn igjen (INN)",
        yes="Bekreft avvisning", no="Køe inn igjen"),
]

running = [{"sourceLabel": "Losen-kø · bane x", "title": "d221 agentd-bro årsak", "detail": "startet 10:58Z"}]

filled = {"workItems": {"state": {"overview": {
    "mirrorFreshness": "Speilet fra deploykøen og trådene 11:15Z",
    "mirrorWarningText": "",
    "needsYouCount": "4", "needsYouEmptyText": "", "needsYou": needs,
    "oldestNeedsYouText": "Eldste: 87 dager · 77 eldre avviste pakker vises med «Vis alle»",
    "runningCount": "1", "runningEmptyText": "", "running": running}}}}
empty = {"workItems": {"state": {"overview": {
    "mirrorFreshness": "Speilet fra deploykøen og trådene 11:15Z", "mirrorWarningText": "",
    "needsYouCount": "0", "needsYouEmptyText": "Ingenting venter på deg nå.", "needsYou": [],
    "oldestNeedsYouText": "", "runningCount": "0", "runningEmptyText": "Ingen agent kjører.", "running": []}}}}
stale = json.loads(json.dumps(filled))
stale["workItems"]["state"]["overview"]["mirrorWarningText"] = (
    "Speilet er 26 t gammelt: arbeidsbenken på staging svarte 401. Listen kan mangle nye forespørsler.")

for name, st in [("state-fylt", filled), ("state-tom", empty), ("state-foreldet", stale)]:
    json.dump(st, open(os.path.join(OUT, name + ".json"), "w"), ensure_ascii=False, indent=1)
print("ok")
