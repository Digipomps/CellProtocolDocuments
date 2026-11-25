#!/usr/bin/env python3
"""Kandidat-skjeletter for PDD_entitetsutvidelse-som-virker (G1-GUI).

Tre flater: «Min entitet» (kartet), «Koble til enhet» og «Hjemmescaffold».
Hver blokk som bare vises i noen tilstander er en List over en rekke i
tilstanden: tom rekke = ingenting tegnes. Handlingsstiene er forslag til hva
cellene skal ta imot; de finnes ikke i koden i dag.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT") or os.path.join(HERE, "..", "skeleton")
os.makedirs(OUT, exist_ok=True)

SECONDARY = "#5F6B7A"
OK = "#1B7F3B"
WARN = "#9A5B00"
BAD = "#B00020"
ACCENT = "#0A5FD0"
CARD = "#F4F6F8"
LINE = "#D9DEE5"


def text(t=None, keypath=None, **mods):
    body = {}
    if t is not None:
        body["text"] = t
    if keypath is not None:
        body["keypath"] = keypath
    if mods:
        body["modifiers"] = mods
    return {"Text": body}


def button(keypath, label, payload_keypath=None, **mods):
    body = {"keypath": keypath, "label": label}
    if payload_keypath:
        body["payloadKeypath"] = payload_keypath
    if mods:
        body["modifiers"] = mods
    return {"Button": body}


def rows(keypath, element, spacing=8):
    return {"List": {"keypath": keypath, "flowElementSkeleton": {"VStack": {"elements": [element]}},
                     "modifiers": {"itemSpacing": spacing, "rowDecoration": "none"}}}


def card(elements, **mods):
    m = {"background": CARD, "cornerRadius": 12, "padding": 14, "maxWidthInfinity": True}
    m.update(mods)
    return {"VStack": {"spacing": 6, "elements": elements, "modifiers": m}}


def gap(element, top=16):
    """Luft over et element. Lagt på raden, ikke på forelderen: en tom List skal ikke etterlate et hull."""
    return {"VStack": {"elements": [element], "modifiers": {"paddingInsets": {"top": top, "bottom": 0, "leading": 0, "trailing": 0}}}}


def notice_block(keypath):
    return rows(keypath, gap({"VStack": {"spacing": 4, "elements": [
        text(keypath="title", fontStyle="headline", fontWeight="semibold", foregroundColorKeypath="color"),
        text(keypath="text", fontStyle="callout"),
    ], "modifiers": {"background": "#FFF4E0", "cornerRadius": 10, "padding": 12, "maxWidthInfinity": True,
                     "borderWidth": 1, "borderColor": "#E8C98A"}}}), 0)


def stacked_on_phone():
    return [{"maxAvailableWidth": 700, "axis": "vertical"}]


# ---------- «Min entitet» ----------

def min_entitet_configuration():
    p = "me.entityMap."
    s = p + "state."
    device_row = card([
        {"HStack": {"spacing": 10, "elements": [
            {"VStack": {"spacing": 2, "elements": [
                text(keypath="name", fontStyle="headline", fontWeight="semibold"),
                text(keypath="scopeText", fontStyle="callout"),
                text(keypath="detailText", fontStyle="caption", foregroundColor=SECONDARY),
            ]}},
            {"Spacer": {}},
            {"VStack": {"spacing": 6, "elements": [
                text(keypath="statusText", fontStyle="callout", fontWeight="semibold", foregroundColorKeypath="statusColor"),
                rows("revokeRows", button(p + "device.revoke", "Trekk tilbake", payload_keypath="payload",
                                          controlStyle="plain", foregroundColor=BAD, fontWeight="semibold", accessibilityLabel="Trekk tilbake denne enheten"), 0),
            ], "modifiers": {"hAlignment": "trailing"}}},
        ], "modifiers": {"vAlignment": "top", "layoutVariants": stacked_on_phone()}}},
    ])
    place_row = card([
        {"HStack": {"spacing": 10, "elements": [
            {"VStack": {"spacing": 2, "elements": [
                text(keypath="name", fontStyle="headline", fontWeight="semibold"),
                text(keypath="address", fontStyle="caption", foregroundColor=SECONDARY),
                text(keypath="roleText", fontStyle="callout"),
                text(keypath="detailText", fontStyle="caption", foregroundColor=SECONDARY),
            ]}},
            {"Spacer": {}},
            {"VStack": {"spacing": 2, "elements": [
                text(keypath="statusText", fontStyle="callout", fontWeight="semibold", foregroundColorKeypath="statusColor"),
                text(keypath="seenText", fontStyle="caption", foregroundColor=SECONDARY),
            ], "modifiers": {"hAlignment": "trailing"}}},
        ], "modifiers": {"vAlignment": "top", "layoutVariants": stacked_on_phone()}}},
    ])
    devices = {"VStack": {"spacing": 10, "elements": [
        {"HStack": {"elements": [
            text("Enhetene mine", fontStyle="title2", fontWeight="semibold"), {"Spacer": {}},
            button(p + "device.add", "Koble til en ny enhet")]}},
        text("Hver enhet har sin egen nøkkel. Alle hele enheter er deg, og har de samme avtalene.",
             fontStyle="callout", foregroundColor=SECONDARY),
        rows(s + "devices", device_row, 10),
    ], "modifiers": {"maxWidthInfinity": True}}}
    places = {"VStack": {"spacing": 10, "elements": [
        {"HStack": {"elements": [
            text("Stedene mine", fontStyle="title2", fontWeight="semibold"), {"Spacer": {}},
            button(p + "refresh", "Sjekk nå")]}},
        text("Kartet ligger bare i dine egne data. Hvert sted har en kopi av de andre stedenes post.",
             fontStyle="callout", foregroundColor=SECONDARY),
        rows(s + "places", place_row, 10),
        rows(s + "emptyPlaces", text(keypath="text", fontStyle="callout", foregroundColor=SECONDARY)),
    ], "modifiers": {"maxWidthInfinity": True}}}
    skeleton = {"VStack": {"spacing": 0, "elements": [
        {"VStack": {"spacing": 4, "elements": [
            text("Min entitet", fontStyle="title", fontWeight="bold"),
            text(keypath=s + "summaryText", fontStyle="body"),
            text(keypath=s + "revocationText", fontStyle="caption", foregroundColor=SECONDARY),
        ]}},
        notice_block(s + "notices"),
        gap({"HStack": {"spacing": 24, "elements": [devices, places],
                    "modifiers": {"vAlignment": "top", "layoutVariants": stacked_on_phone()}}}, 20),
    ], "modifiers": {"padding": 20}}}
    return {
        "name": "Min entitet",
        "description": "Enhetene som er entiteten din, og stedene der entiteten din finnes. Les kartet, trekk en enhet tilbake, koble til en ny.",
        "discovery": {"sourceCellEndpoint": "cell:///EntityAnchor", "sourceCellName": "EntityAnchorCell",
                      "purpose": "Min entitet",
                      "purposeDescription": "Se og styre hvilke enheter som er meg, og hvor entiteten min finnes.",
                      "interests": ["entitet", "enheter", "identitet", "kart"], "menuSlots": ["lowerMid"]},
        "cellReferences": [{"endpoint": "cell:///EntityAnchor", "label": "me"}],
        "skeleton": skeleton,
    }


def device(did, name, scope, detail, status="Virker", color=OK, revocable=True):
    return {"id": did, "name": name, "scopeText": scope, "detailText": detail,
            "statusText": status, "statusColor": color,
            "revokeRows": [{"id": "r", "payload": {"linkID": did}}] if revocable else []}


def place(pid, name, address, role, detail, status="Nåbar", color=OK, seen="sjekket 12:47"):
    return {"id": pid, "name": name, "address": address, "roleText": role, "detailText": detail,
            "statusText": status, "statusColor": color, "seenText": seen}


MAC = device("owner", "MacBook Pro (denne enheten)", "Eiernøkkelen. Hele entiteten.",
             "Laget 02.09.2026 · kan ikke trekkes tilbake herfra", revocable=False)
PHONE = device("link-phone", "iPhone", "Hele entiteten, alle steder.",
               "Koblet til 12.11.2026 med passkey · sist brukt i dag 12:41")
SAFARI = device("link-safari", "Safari-utvidelsen", "Hele entiteten, alle steder.",
                "Koblet til 20.11.2026 med passkey · sist brukt i går 22:05")
CLAUDE = device("link-claude", "Claude Code på MacBook Pro", "Avgrenset: bare verktøyene du har valgt. Er ikke deg.",
                "Koblet til 23.11.2026 med passkey · utløper 23.12.2026")

HOME = place("home", "Mac-en hjemme", "cell://kjetil-mac.local", "Ankeret ligger her.",
             "23 celler · 9 avtaler · 4 enheter kjent")
STAGING = place("staging", "Staging hos Digipomps", "cell://staging.haven.nexus", "Kopi av kartet. Kjenner enhetene dine.",
                "14 celler · 6 avtaler · tilbaketrekkinger hentet 12:44")
UIO = place("uio", "Informasjonssystemer (UiO)", "cell://is.uio.example", "Kopi av kartet. Kjenner enhetene dine.",
            "3 celler · 2 avtaler · tilbaketrekkinger hentet 12:46")


def me_state(devices, places, summary, revocation, notices=None, empty_places=None):
    return {"me": {"entityMap": {"state": {
        "status": "ok", "schemaVersion": "haven.entity-map.state.v1",
        "summaryText": summary, "revocationText": revocation,
        "notices": notices or [], "devices": devices, "places": places,
        "emptyPlaces": empty_places or []}}}}


ME_STATES = {
    "alt-naabart": me_state([MAC, PHONE, SAFARI, CLAUDE], [HOME, STAGING, UIO],
        "Du har 3 hele enheter og 1 avgrenset, og finnes på 3 steder. Alt virker.",
        "Alle steder har ferske tilbaketrekkinger (eldste er 3 minutter gammel, grensen er 10)."),
    "ett-sted-utilgjengelig": me_state([MAC, PHONE, SAFARI, CLAUDE],
        [HOME, STAGING,
         dict(UIO, statusText="Ikke nåbar", statusColor=WARN, seenText="sist sett 11:58",
              detailText="3 celler · 2 avtaler · tilbaketrekkinger hentet 11:58")],
        "Du har 3 hele enheter og 1 avgrenset, og finnes på 3 steder. Ett sted svarer ikke.",
        "Informasjonssystemer (UiO) har ikke hentet tilbaketrekkinger på 49 minutter.",
        notices=[{"id": "n1", "color": WARN, "title": "Informasjonssystemer (UiO) svarer ikke",
                  "text": "Stedet avviser de koblede enhetene dine til det får hentet en fersk liste over tilbaketrekkinger. "
                          "Eiernøkkelen virker der som før. Du trenger ikke gjøre noe; det retter seg når stedet er nåbart."}]),
    "lenke-trukket": me_state(
        [MAC, dict(PHONE, statusText="Trukket tilbake", statusColor=BAD, revokeRows=[],
                   detailText="Trukket 25.11.2026 12:52 fra denne enheten"), SAFARI, CLAUDE],
        [dict(HOME, detailText="23 celler · 9 avtaler · vet at iPhone er trukket", seenText="12:52"),
         dict(STAGING, detailText="14 celler · 6 avtaler · vet at iPhone er trukket", seenText="12:53"),
         dict(UIO, statusText="Venter", statusColor=WARN, seenText="henter senest 12:56",
              detailText="3 celler · 2 avtaler · har ikke hentet tilbaketrekkingen ennå")],
        "Du har 2 hele enheter og 1 avgrenset, og finnes på 3 steder. iPhone er trukket tilbake.",
        "Tilbaketrekkingen gjelder straks her, og på de andre stedene senest 10 minutter etter.",
        notices=[{"id": "n1", "color": BAD, "title": "iPhone er ikke lenger deg",
                  "text": "2 av 3 steder har fått beskjed. Informasjonssystemer (UiO) henter listen senest 12:56. "
                          "Avtalene dine er ikke endret. Vil du bruke telefonen igjen, kobler du den til på nytt."}]),
    "tom": me_state([MAC], [dict(HOME, detailText="23 celler · 9 avtaler · 1 enhet kjent")],
        "Du har 1 enhet og finnes på 1 sted.",
        "Ingen koblede enheter ennå.",
        empty_places=[{"id": "e", "text": "Når du bruker et annet sted med en koblet enhet, kommer stedet hit av seg selv."}]),
}


# ---------- «Koble til enhet» ----------

def koble_configuration():
    p = "me.identityLinks."
    s = p + "enrollmentView."
    step = lambda keypath, elements: rows(s + keypath, gap(card(elements, padding=18)), 0)
    words = text(keypath="words", fontSize=30, fontWeight="bold")
    skeleton = {"VStack": {"spacing": 0, "elements": [
        {"VStack": {"spacing": 4, "elements": [
            text(keypath=s + "title", fontStyle="title", fontWeight="bold"),
            text(keypath=s + "subtitle", fontStyle="body", foregroundColor=SECONDARY)]}},
        notice_block(s + "rejections"),
        # Eieren, steg 1
        step("ownerStart", [
            text("Hva skal den nye enheten være?", fontStyle="headline", fontWeight="semibold"),
            text("En hel enhet er deg: den får de samme avtalene som du har, på alle stedene dine. "
                 "Du kobler den til én gang.", fontStyle="callout"),
            {"HStack": {"spacing": 10, "elements": [
                button(p + "startEnrollment", "Lag koblingskode", payload_keypath="payload")]}},
        ]),
        # Eieren, viser koden
        step("ownerCode", [
            text("Skriv denne koden på den nye enheten", fontStyle="headline", fontWeight="semibold"),
            text(keypath="code", fontSize=34, fontWeight="bold"),
            text(keypath="expiresText", fontStyle="caption", foregroundColor=SECONDARY),
            text("Du trenger ikke gjøre mer her før den nye enheten har svart.", fontStyle="callout", foregroundColor=SECONDARY),
        ]),
        # Eieren, godkjenner
        step("ownerApprove", [
            text(keypath="requestText", fontStyle="headline", fontWeight="semibold"),
            text("Sjekk at de samme tre ordene står på den nye enheten:", fontStyle="callout"),
            words,
            text(keypath="grantText", fontStyle="callout"),
            text(keypath="originText", fontStyle="caption", foregroundColor=SECONDARY),
            {"HStack": {"spacing": 10, "elements": [
                button(p + "approveEnrollment", "Godkjenn med passkey", payload_keypath="approvePayload"),
                button(p + "declineEnrollment", "Avvis", payload_keypath="declinePayload", controlStyle="plain", foregroundColor=BAD, fontWeight="semibold")]}},
        ]),
        # Den nye enheten, steg 1
        step("deviceStart", [
            text("Skriv koden som står på enheten du allerede bruker", fontStyle="headline", fontWeight="semibold"),
            {"TextField": {"targetKeypath": p + "requestEnrollment", "placeholder": "Kode, for eksempel 4F7K-92QD",
                           "modifiers": {"maxWidthInfinity": True}}},
            text("Trykk Enter. Du kan også åpne lenken du fikk på den andre enheten.", fontStyle="caption", foregroundColor=SECONDARY),
        ]),
        # Den nye enheten, venter
        step("deviceWaiting", [
            text("Sjekk at de samme tre ordene står på den andre enheten", fontStyle="headline", fontWeight="semibold"),
            words,
            text("Godkjenn der med passkey. Denne siden går videre av seg selv.", fontStyle="callout"),
            text(keypath="expiresText", fontStyle="caption", foregroundColor=SECONDARY),
        ]),
        # Ferdig (begge)
        step("done", [
            text(keypath="title", fontStyle="headline", fontWeight="semibold", foregroundColor=OK),
            text(keypath="text", fontStyle="callout"),
            rows("placeRows", {"HStack": {"spacing": 8, "elements": [
                text(keypath="name", fontStyle="callout"), {"Spacer": {}},
                text(keypath="statusText", fontStyle="callout", foregroundColorKeypath="statusColor")]}}, 4),
            {"HStack": {"elements": [button("me.entityMap.open", "Se «Min entitet»")]}},
        ]),
    ], "modifiers": {"padding": 20, "layoutVariants": [{"minAvailableWidth": 701, "width": 640}]}}}
    return {
        "name": "Koble til enhet",
        "description": "Gjør en ny enhet til en del av entiteten din, én gang for alle steder, godkjent med passkey på en enhet som allerede er deg.",
        "discovery": {"sourceCellEndpoint": "cell:///EntityAnchor", "sourceCellName": "EntityAnchorCell",
                      "purpose": "Koble til enhet", "purposeDescription": "Utvide entiteten med en ny enhet.",
                      "interests": ["entitet", "enheter", "kobling"], "menuSlots": []},
        "cellReferences": [{"endpoint": "cell:///EntityAnchor", "label": "me"}],
        "skeleton": skeleton,
    }


def link_state(title, subtitle, **blocks):
    view = {"title": title, "subtitle": subtitle, "rejections": [], "ownerStart": [], "ownerCode": [],
            "ownerApprove": [], "deviceStart": [], "deviceWaiting": [], "done": []}
    view.update(blocks)
    return {"me": {"identityLinks": {"enrollmentView": view}}}


OWNER_TITLE = ("Koble til en ny enhet", "På enheten du allerede bruker.")
DEVICE_TITLE = ("Koble denne enheten til entiteten din", "På den nye enheten.")
PLACES_DONE = [
    {"id": "home", "name": "Mac-en hjemme", "statusText": "Virker nå", "statusColor": OK},
    {"id": "staging", "name": "Staging hos Digipomps", "statusText": "Virker nå", "statusColor": OK},
    {"id": "uio", "name": "Informasjonssystemer (UiO)", "statusText": "Virker ved første besøk", "statusColor": SECONDARY},
]
APPROVE = {"id": "a", "requestText": "«Safari på iPhone» ber om å bli en del av entiteten din",
           "words": "fjord · lampe · rev",
           "grantText": "Den blir en hel enhet: samme avtaler som deg, på alle stedene dine. Du kan trekke den tilbake når som helst.",
           "originText": "Forespørselen kom til Mac-en hjemme 12:49. Koden ble laget her 12:48.",
           "approvePayload": {"requestID": "req-1"}, "declinePayload": {"requestID": "req-1"}}

LINK_STATES = {
    "eier-start": link_state(*OWNER_TITLE, ownerStart=[{"id": "s", "payload": {"scope": "same_entity"}}]),
    "eier-kode": link_state(*OWNER_TITLE, ownerCode=[{"id": "c", "code": "4F7K-92QD", "expiresText": "Gjelder i 10 minutter, til 12:58. Kan brukes én gang."}]),
    "eier-godkjenn": link_state(*OWNER_TITLE, ownerApprove=[APPROVE]),
    "eier-ferdig": link_state(*OWNER_TITLE, done=[{"id": "d", "title": "iPhone er koblet til",
        "text": "Den er nå deg på alle stedene dine. Du trenger ikke koble den til ett sted om gangen.", "placeRows": PLACES_DONE}]),
    "ny-start": link_state(*DEVICE_TITLE, deviceStart=[{"id": "s"}]),
    "ny-venter": link_state(*DEVICE_TITLE, deviceWaiting=[{"id": "w", "words": "fjord · lampe · rev", "expiresText": "Forespørselen gjelder til 12:58."}]),
    "ny-ferdig": link_state(*DEVICE_TITLE, done=[{"id": "d", "title": "Denne enheten er koblet til",
        "text": "Du har de samme avtalene her som på de andre enhetene dine.", "placeRows": PLACES_DONE}]),
    "avvist-utlopt": link_state(*DEVICE_TITLE, deviceStart=[{"id": "s"}],
        rejections=[{"id": "r", "color": BAD, "title": "Koden gjelder ikke lenger",
                     "text": "Koden var gyldig i 10 minutter og kan brukes én gang. Lag en ny kode på enheten du allerede bruker."}]),
    "avvist-avslaatt": link_state(*DEVICE_TITLE, deviceStart=[{"id": "s"}],
        rejections=[{"id": "r", "color": BAD, "title": "Koblingen ble avvist på den andre enheten",
                     "text": "Ingenting er endret. Var det du som avviste fordi ordene ikke stemte, lager du en ny kode og prøver igjen."}]),
    "avvist-passkey": link_state(*OWNER_TITLE, ownerApprove=[APPROVE],
        rejections=[{"id": "r", "color": BAD, "title": "Passkey-bekreftelsen ble ikke godtatt",
                     "text": "Bekreftelsen må være laget nå, for akkurat denne forespørselen. Trykk «Godkjenn med passkey» på nytt. "
                             "Enheten er ikke koblet til."}]),
}


# ---------- «Hjemmescaffold» ----------

def hjem_configuration():
    p = "home."
    s = p + "linkView."
    block = lambda keypath, elements: rows(s + keypath, gap(card(elements, padding=18)), 0)
    skeleton = {"VStack": {"spacing": 0, "elements": [
        {"VStack": {"spacing": 4, "elements": [
            text("Hjemmescaffoldet", fontStyle="title", fontWeight="bold"),
            text("Stedet der cellene dine kjører når du ikke har en enhet på.", fontStyle="body", foregroundColor=SECONDARY)]}},
        notice_block(s + "rejections"),
        block("unlinked", [
            text(keypath="name", fontStyle="headline", fontWeight="semibold"),
            text(keypath="address", fontStyle="caption", foregroundColor=SECONDARY),
            text("Hjemmescaffoldet er ikke koblet til entiteten din. Til det er gjort, kan det ikke handle som deg.", fontStyle="callout"),
            text("Koblingen signeres med passkey, akkurat som for en ny enhet. Du kan trekke den tilbake fra «Min entitet».",
                 fontStyle="callout", foregroundColor=SECONDARY),
            {"HStack": {"elements": [button(p + "link.anchor", "Koble til med passkey", payload_keypath="payload")]}},
        ]),
        block("linked", [
            text(keypath="name", fontStyle="headline", fontWeight="semibold"),
            text(keypath="address", fontStyle="caption", foregroundColor=SECONDARY),
            text(keypath="statusText", fontStyle="callout", fontWeight="semibold", foregroundColor=OK),
            text(keypath="detailText", fontStyle="callout"),
            {"HStack": {"elements": [button("me.entityMap.open", "Se «Min entitet»")]}},
        ]),
    ], "modifiers": {"padding": 20, "layoutVariants": [{"minAvailableWidth": 701, "width": 640}]}}}
    return {
        "name": "Hjemmescaffold",
        "description": "Koble hjemmescaffoldet til entiteten med en signert lenke godkjent med passkey.",
        "discovery": {"sourceCellEndpoint": "cell:///FlowPlacementHome", "sourceCellName": "FlowPlacementHomeCell",
                      "purpose": "Hjemmescaffold", "purposeDescription": "La hjemmescaffoldet handle som entiteten.",
                      "interests": ["entitet", "hjemmescaffold"], "menuSlots": []},
        "cellReferences": [{"endpoint": "cell:///FlowPlacementHome", "label": "home"},
                           {"endpoint": "cell:///EntityAnchor", "label": "me"}],
        "skeleton": skeleton,
    }


def home_state(**blocks):
    view = {"rejections": [], "unlinked": [], "linked": []}
    view.update(blocks)
    return {"home": {"linkView": view}}


HOME_ROW = {"id": "h", "name": "Staging hos Digipomps", "address": "cell://staging.haven.nexus", "payload": {}}
HOME_STATES = {
    "ikke-koblet": home_state(unlinked=[HOME_ROW]),
    "koblet": home_state(linked=[dict(HOME_ROW, statusText="Koblet til entiteten din",
        detailText="Koblet til 25.11.2026 12:50 med passkey. Hjemmescaffoldet er en hel enhet og står i «Min entitet».")]),
    "feil-passkey": home_state(unlinked=[HOME_ROW],
        rejections=[{"id": "r", "color": BAD, "title": "Passkey-bekreftelsen ble ikke godtatt",
                     "text": "Bekreftelsen må være laget nå, for akkurat denne koblingen. Trykk «Koble til med passkey» på nytt. "
                             "Hjemmescaffoldet er ikke koblet til."}]),
}


if __name__ == "__main__":
    def dump(name, value):
        with open(os.path.join(OUT, name), "w") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write("\n")
    dump("min-entitet.cellconfiguration.json", min_entitet_configuration())
    dump("koble-enhet.cellconfiguration.json", koble_configuration())
    dump("hjemmescaffold.cellconfiguration.json", hjem_configuration())
    for prefix, states in (("min-entitet", ME_STATES), ("koble-enhet", LINK_STATES), ("hjemmescaffold", HOME_STATES)):
        for name, st in states.items():
            dump(f"state-{prefix}-{name}.json", st)
    print("ok", len(os.listdir(OUT)), "filer i", os.path.normpath(OUT))
