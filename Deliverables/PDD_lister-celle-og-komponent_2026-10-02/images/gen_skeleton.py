#!/usr/bin/env python3
"""Genererer kandidat-skjelettene for PDD_lister-celle-og-komponent (G1-GUI).

Én funksjon lager sjekkliste-fragmentet; «Mine lister»-flaten og komponent-
monteringen (SkeletonComponentMount) bruker samme fragment, bare med ulikt
keypath-prefiks (flaten går gjennom Porthole-referansen `my`, monteringen
snakker rett med cellen). Swift-fabrikken skal gjøre det samme senere.
"""
import json, os, sys

OUT = os.environ.get("OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skeleton")
os.makedirs(OUT, exist_ok=True)

SECONDARY = "#8E8E93"   # iOS secondaryLabel
ACCENT = "#007AFF"      # iOS systemBlue


def text(t=None, keypath=None, **mods):
    body = {}
    if t is not None:
        body["text"] = t
    if keypath is not None:
        body["keypath"] = keypath
    if mods:
        body["modifiers"] = mods
    return {"Text": body}


def item_visible(keypath, equals):
    return {"visibility": {"when": {"scope": "item", "keypath": keypath, "equals": equals}}}


def button(keypath, label="", icon=None, payload_keypath=None, **mods):
    body = {"keypath": keypath, "label": label}
    if icon:
        body["icon"] = icon
    if payload_keypath:
        body["payloadKeypath"] = payload_keypath
    if mods:
        body["modifiers"] = mods
    return {"Button": body}


def checklist_item_row(p):
    """Én rad i sjekklista: sirkel/hake, tittel, opp/ned/fjern. Alt leser radens egne data."""
    unchecked = button(p + "item.toggle", label="○", payload_keypath="togglePayload",
                       controlStyle="plain", fontSize=22, foregroundColor=SECONDARY,
                       accessibilityLabel="Merk som utført", width=28,
                       **item_visible("done", False))
    checked = button(p + "item.toggle", label="", icon="checkmark.circle.fill", payload_keypath="togglePayload",
                     controlStyle="plain", fontSize=22, foregroundColor=ACCENT,
                     accessibilityLabel="Merk som ikke utført", width=28,
                     **item_visible("done", True))
    title = text(keypath="title", fontStyle="body", foregroundColorKeypath="titleColor")
    hide_when_drag = [{"requiresCapability": ["drag"], "hidden": True}]   # web har dra-og-slipp; appen får pilene
    up = button(p + "item.move", label="", icon="chevron.up", payload_keypath="moveUpPayload",
                controlStyle="plain", foregroundColor=SECONDARY, accessibilityLabel="Flytt opp",
                layoutVariants=hide_when_drag, **item_visible("done", False))
    down = button(p + "item.move", label="", icon="chevron.down", payload_keypath="moveDownPayload",
                  controlStyle="plain", foregroundColor=SECONDARY, accessibilityLabel="Flytt ned",
                  layoutVariants=hide_when_drag, **item_visible("done", False))
    remove = button(p + "item.remove", label="", icon="trash", payload_keypath="removePayload",
                    controlStyle="plain", foregroundColor=SECONDARY, accessibilityLabel="Fjern")
    return {"VStack": {"elements": [
        {"HStack": {"spacing": 8, "elements": [unchecked, checked, title, {"Spacer": {}}, up, down, remove],
                    "modifiers": {
                        "draggableRole": "list-item", "dragPayloadKeypath": "dragPayload",
                        "dropTargetRole": "list-item-slot", "acceptedDragRoles": ["list-item"],
                        "dropTargetPayloadKeypath": "dropPayload", "dropActionKeypath": p + "item.move",
                        "accessibilityDragLabel": "Dra for å flytte",
                        "paddingInsets": {"top": 6, "bottom": 6, "leading": 0, "trailing": 0}}}}
    ]}}


def checklist(p):
    """Sjekkliste-fragmentet for ÉN liste. Leser radens/monteringens item: title, items, hasDone…"""
    header = {"HStack": {"spacing": 8, "elements": [
        {"TextField": {"sourceKeypath": "title", "targetKeypath": p + "list.rename",
                       "placeholder": "Listenavn", "modifiers": {"fontStyle": "title2", "fontWeight": "semibold"}}},
        {"Spacer": {}},
        text(keypath="summaryText", fontStyle="caption", foregroundColor=SECONDARY),
        button(p + "list.remove", label="", icon="trash", payload_keypath="removeListPayload",
               controlStyle="plain", foregroundColor=SECONDARY, accessibilityLabel="Slett listen"),
    ]}}
    add = {"TextField": {"targetKeypath": p + "item.add", "placeholder": "Legg til …",
                         "modifiers": {"maxWidthInfinity": True}}}
    items = {"List": {"keypath": "items", "flowElementSkeleton": checklist_item_row(p),
                      "modifiers": {"itemSpacing": 0, "rowDecoration": "none"}}}
    empty = {"List": {"keypath": "emptyRows", "flowElementSkeleton": {"VStack": {"elements": [
        text(keypath="text", fontStyle="callout", foregroundColor=SECONDARY)]}}}}
    clear_done = {"List": {"keypath": "doneRows", "flowElementSkeleton": {"VStack": {"elements": [
        {"HStack": {"elements": [{"Spacer": {}},
            button(p + "list.clearDone", label="Fjern utførte", payload_keypath="clearDonePayload",
                   controlStyle="plain", foregroundColor=ACCENT, fontStyle="callout")]}}]}}}}
    return {"VStack": {"spacing": 10, "elements": [header, add, items, empty, clear_done]}}


def mine_lister_configuration():
    p = "my.lists."
    new_list = {"TextField": {"targetKeypath": p + "list.create", "placeholder": "Ny liste … (Enter)",
                              "modifiers": {"maxWidthInfinity": True}}}
    list_row = {"VStack": {"elements": [
        {"HStack": {"spacing": 8, "elements": [
            text(keypath="title", fontStyle="body", fontWeight="semibold", **item_visible("isActive", True)),
            text(keypath="title", fontStyle="body", **item_visible("isActive", False)),
            {"Spacer": {}},
            text(keypath="summaryText", fontStyle="caption", foregroundColor=SECONDARY),
        ]}}]}}
    lists = {"List": {"keypath": p + "state.lists", "selectionMode": "single",
                      "selectionValueKeypath": "id", "selectionPayloadMode": "item_id",
                      "selectionActionKeypath": p + "list.select", "allowsEmptySelection": False,
                      "flowElementSkeleton": list_row,
                      "modifiers": {"itemSpacing": 0}}}
    hint = {"List": {"keypath": p + "state.emptyHint", "flowElementSkeleton": {"VStack": {"elements": [
        text(keypath="text", fontStyle="callout", foregroundColor=SECONDARY)]}}}}
    notice = {"List": {"keypath": p + "state.notice", "flowElementSkeleton": {"VStack": {"elements": [
        text(keypath="text", fontStyle="callout", foregroundColor="#FFB4AB")],
        "modifiers": {"background": "#B0002033", "cornerRadius": 8, "padding": 10}}}}}
    active = {"List": {"keypath": p + "state.activeAsRows", "flowElementSkeleton": checklist(p),
                       "modifiers": {"itemSpacing": 0}}}
    left = {"VStack": {"spacing": 10, "elements": [
        text("Mine lister", fontStyle="title", fontWeight="bold"), new_list, lists, hint]}}
    right = {"VStack": {"spacing": 10, "elements": [notice, active]}}
    skeleton = {"VStack": {"spacing": 16, "elements": [
        {"HStack": {"spacing": 24, "elements": [
            {"VStack": {"elements": [left], "modifiers": {"layoutVariants": [{"minAvailableWidth": 701, "width": 300}]}}},
            {"VStack": {"elements": [right], "modifiers": {"maxWidthInfinity": True}}}],
          "modifiers": {"vAlignment": "top", "layoutVariants": [
              {"maxAvailableWidth": 700, "axis": "vertical"}]}}}],
        "modifiers": {"padding": 16}}}
    return {
        "name": "Mine lister",
        "description": "Brukerens egne lister (handleliste, huskeliste, idéliste …) fra cell:///Lists: velg liste, legg til, kryss av, flytt, fjern. Utførte sorteres i bunn.",
        "discovery": {"sourceCellEndpoint": "cell:///Lists", "sourceCellName": "ListsCell",
                      "purpose": "Mine lister", "purposeDescription": "Holde brukerens lister og krysse av det som er gjort.",
                      "interests": ["lists", "handleliste", "huskeliste", "ideer", "todo"],
                      "menuSlots": ["lowerMid"]},
        "cellReferences": [{"endpoint": "cell:///Lists", "label": "my"}],
        "skeleton": skeleton,
    }


def mount(list_view):
    return {"componentID": "haven.lists.checklist", "revision": "1", "sourceCellEndpoint": "cell:///Lists",
            "skeleton": checklist("lists."), "item": list_view}


def host_with_components():
    """Eksempel på vert som «drar inn» alle lister som komponenter (én ComponentSurface per rad)."""
    return {"name": "Lister som komponenter (eksempel)",
            "cellReferences": [{"endpoint": "cell:///Lists", "label": "my"}],
            "skeleton": {"VStack": {"spacing": 16, "elements": [
                text("Dashbord med lister (eksempel på vert)", fontStyle="title", fontWeight="bold"),
                {"List": {"keypath": "my.lists.state.lists", "flowElementSkeleton": {"VStack": {"elements": [
                    {"ComponentSurface": {"sourceKeypath": "mount", "instanceIDKeypath": "id", "variant": "inline",
                                          "modifiers": {"background": "#FFFFFF14", "cornerRadius": 12, "padding": 12}}}]}},
                          "modifiers": {"itemSpacing": 12}}}],
                "modifiers": {"padding": 16}}}}


# ---------- eksempeldata (det cellen vil levere) ----------

def item(list_id, iid, title, done=False):
    row = {"id": iid, "title": title, "done": done,
            "togglePayload": {"listId": list_id, "itemId": iid},
            "moveUpPayload": {"listId": list_id, "itemId": iid, "direction": "up"},
            "moveDownPayload": {"listId": list_id, "itemId": iid, "direction": "down"},
            "removePayload": {"listId": list_id, "itemId": iid},
            "dragPayload": {"listId": list_id, "itemId": iid},
            "dropPayload": {"listId": list_id, "itemId": iid}}
    if done:
        row["titleColor"] = SECONDARY   # utførte dempes; åpne arver flatens tekstfarge
    return row


def list_view(list_id, title, kind, items, active=True):
    open_items = [i for i in items if not i["done"]]
    done_items = [i for i in items if i["done"]]
    ordered = open_items + done_items
    n_open, n_done = len(open_items), len(done_items)
    summary = (f"{n_open} igjen" if n_open else "alt utført") + (f" · {n_done} utført" if n_done else "")
    if not items:
        summary = "tom"
    return {"id": list_id, "title": title, "kind": kind, "isActive": active,
            "openCount": n_open, "doneCount": n_done, "summaryText": summary,
            "items": ordered,
            "emptyRows": [] if items else [{"text": "Ingen punkter ennå. Skriv noe over og trykk Enter."}],
            "doneRows": [{"id": "clear"}] if n_done else [],
            "removeListPayload": {"listId": list_id},
            "clearDonePayload": {"listId": list_id},
            "selectPayload": {"listId": list_id}}


def state(lists, active_id, notice=None):
    rows = []
    for lv in lists:
        rows.append({"id": lv["id"], "title": lv["title"], "summaryText": lv["summaryText"],
                     "isActive": lv["id"] == active_id, "selectPayload": {"listId": lv["id"]},
                     "mount": mount(dict(lv, isActive=False))})
    active = [dict(lv, isActive=True) for lv in lists if lv["id"] == active_id]
    return {"my": {"lists": {"state": {
        "status": "ok", "schemaVersion": "haven.lists.state.v1",
        "lists": rows, "activeListId": active_id, "activeAsRows": active,
        "emptyHint": [] if lists else [{"text": "Du har ingen lister ennå. Skriv et navn over og trykk Enter."}],
        "notice": [{"text": notice}] if notice else [],
        "counts": {"lists": len(lists), "open": sum(l["openCount"] for l in lists), "done": sum(l["doneCount"] for l in lists)},
    }}}}


handle = list_view("l-handle", "Handleliste", "shopping", [
    item("l-handle", "i1", "Melk"), item("l-handle", "i2", "Brød"), item("l-handle", "i3", "Egg"),
    item("l-handle", "i4", "Kaffe"), item("l-handle", "i5", "Smør", done=True), item("l-handle", "i6", "Pasta", done=True)])
huske = list_view("l-huske", "Huskeliste", "reminders", [
    item("l-huske", "h1", "Ringe tannlegen"), item("l-huske", "h2", "Levere pakke på posten"),
    item("l-huske", "h3", "Bestille vinterdekk", done=True)], active=False)
ideer = list_view("l-ideer", "Idéer", "ideas", [
    item("l-ideer", "d1", "Celle for lister som kan dras inn hvor som helst"),
    item("l-ideer", "d2", "Palazzo: ukens Sicilia-artikkel"),], active=False)

STATES = {
    "fylt": state([handle, huske, ideer], "l-handle"),
    "tom": state([], None),
    "ny-liste": state([list_view("l-ny", "Pakkeliste", "custom", [])], "l-ny"),
    "feil": state([handle, huske, ideer], "l-handle",
                  notice="Kunne ikke lagre siste endring (lagring ikke bekreftet). Endringen er gjort i minnet — prøv igjen."),
}

if __name__ == "__main__":
    cfg = mine_lister_configuration()
    with open(os.path.join(OUT, "mine-lister.cellconfiguration.json"), "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, "checklist-component.mount.json"), "w") as f:
        json.dump(mount(handle), f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, "vert-med-komponenter.cellconfiguration.json"), "w") as f:
        json.dump(host_with_components(), f, ensure_ascii=False, indent=2)
    for name, st in STATES.items():
        with open(os.path.join(OUT, f"state-{name}.json"), "w") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
    print("ok", sorted(os.listdir(OUT)))
