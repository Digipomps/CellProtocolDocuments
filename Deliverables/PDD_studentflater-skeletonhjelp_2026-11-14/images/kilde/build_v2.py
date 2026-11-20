"""Bygger skeleton/studio-hjelp-v2.skeleton.json. Hvert element har en formålsmerknad i FORMAL nedenfor."""
import json, pathlib
INK, MUTED, LINE, CARD, BLUE = "#0f172a", "#64748b", "#e2e8f0", "#ffffff", "#1d4ed8"
def text(t=None, kp=None, size=None, weight=None, color=None, **m):
    d = {"text": t} if t is not None else {"keypath": kp}
    mod = {k: v for k, v in dict(fontSize=size, fontWeight=weight, foregroundColor=color, **m).items() if v is not None}
    if mod: d["modifiers"] = mod
    return {"Text": d}
def button(label, kp, primary=False, payload=None):
    b = {"keypath": kp, "label": label}
    if payload is not None: b["payload"] = payload
    b["modifiers"] = ({"background": BLUE, "foregroundColor": "#ffffff", "cornerRadius": 8, "fontWeight": "semibold"} if primary
                      else {"background": "#ffffff", "foregroundColor": INK, "borderColor": LINE, "borderWidth": 1, "cornerRadius": 8})
    return {"Button": b}
def row(*els, spacing=10, **m):
    return {"HStack": {"spacing": spacing, "wrap": True, "elements": list(els), **({"modifiers": m} if m else {})}}
def col(*els, spacing=12, **m):
    return {"VStack": {"spacing": spacing, "elements": list(els), **({"modifiers": m} if m else {})}}
def card(*els, bg=CARD, border=LINE):
    return col(*els, spacing=14, background=bg, borderColor=border, borderWidth=1, cornerRadius=14, padding=20)
def when(kp, *els):
    # Kommer og går med cellens tilstand: en liste med null eller én rad (ingen betingelse på toppnivå).
    return {"List": {"keypath": kp, "flowElementSkeleton": col(*els)}}

S = "configurationStudio.state."
skeleton = col(
    # 1 Topp: hva dette er, status, hvem som er med, del
    row(col(text("Ny flate", size=26, weight="semibold", color=INK),
            text(kp=S+"statusLine", size=14, color=MUTED), spacing=2),
        {"Spacer": {}},
        text(kp=S+"coedit.editorsText", size=14, color=MUTED),
        button("Del", "configurationStudio.openShare")),
    # 2 Konflikt: bare når en annen har lagret først
    when(S+"coedit.conflicts",
         card(text(kp="title", size=16, weight="semibold", color="#92400e"),
              text(kp="text", color="#78350f"),
              row(button("Hent den nyeste versjonen", "configurationStudio.reloadSelectedConfiguration", primary=True)),
              bg="#fffbeb", border="#fcd34d")),
    # 3 Del: bare når eieren har trykket Del
    when(S+"coedit.sharePanel",
         card(text("Rediger sammen", size=16, weight="semibold", color=INK),
              text("Den du inviterer, kan endre det samme utkastet. Du kan ta tilgangen tilbake.", color=MUTED),
              row({"TextField": {"sourceKeypath": S+"coedit.inviteDraft", "targetKeypath": "configurationStudio.setInviteDraft",
                                  "placeholder": "Navn eller HAVEN-adresse",
                                  "modifiers": {"background": "#ffffff", "foregroundColor": INK, "borderColor": LINE, "borderWidth": 1, "cornerRadius": 8}}},
                  button("Inviter", "configurationStudio.inviteEditor", primary=True)),
              row(button("Del lenke i en samtale", "configurationStudio.shareToChat"), button("Lukk", "configurationStudio.closeShare")))),
    # 4 Beskriv: én oppgave, én hovedknapp
    card(text("Hva skal flaten gjøre?", size=18, weight="semibold", color=INK),
         {"TextArea": {"sourceKeypath": S+"assist.description", "targetKeypath": "configurationStudio.setAssistDescription",
                       "placeholder": "For eksempel: vis gjøremålene mine med frist, og la meg krysse dem av",
                       "modifiers": {"background": "#ffffff", "foregroundColor": INK, "borderColor": LINE, "borderWidth": 1, "cornerRadius": 10, "minHeight": 96}}},
         when(S+"assist.canDraft", row(text(kp="modelText", size=13, color=MUTED), {"Spacer": {}}, button("Lag forslag", "configurationStudio.assistDraft", primary=True))),
         when(S+"assist.noModel",
              text(kp="text", color=MUTED),
              {"FileUpload": {"title": "Last opp en fil du har laget selv", "actionKeypath": "configurationStudio.importDraftConfigurationFile",
                              "acceptedContentTypes": ["application/json"], "supportsDrop": True, "uploadMode": "base64", "submitOnSelection": True,
                              "maxSizeBytes": 524288, "emptyTitle": "Slipp en JSON-fil her", "emptyMessage": "Se guiden «Lag din egen flate»."}})),
    # 5 Resultat: status i klartekst, forhåndsvisning først, detaljer bak en fane
    when(S+"result",
         card(row(text(kp="badge", size=13, weight="semibold", foregroundColorKeypath="badgeColor", backgroundKeypath="badgeBackground", cornerRadius=12, padding=6, lineLimit=1)),
              text(kp="headline", size=17, weight="semibold", color=INK),
              text(kp="explanation", color=MUTED),
              when("fixes", row(button("Lag nytt forslag som retter dette", "configurationStudio.assistDraft", primary=True))),
              {"Tabs": {"activeTabStateKeypath": S+"ui.resultTab", "selectionActionKeypath": "configurationStudio.setResultTab",
                        "tabsKeypath": S+"ui.resultTabs", "idKeypath": "id", "labelKeypath": "title",
                        "panels": [{"id": "visning", "content": [col({"Reference": {"keypath": "preview"}}, background="#f8fafc", borderColor=LINE, borderWidth=1, cornerRadius=10, padding=16)]},
                                   {"id": "bygget", "content": [{"List": {"keypath": "details", "flowElementSkeleton": col(
                                       row(text(kp="label", size=13, color=MUTED, width=150), text(kp="value", size=13, color=INK)))}}]}]}})),
    # 6 Lagre: én hovedhandling, angre ved siden av
    when(S+"saveBar", row(text(kp="text", size=13, color=MUTED), {"Spacer": {}},
                          button("Forkast", "configurationStudio.discardDraft"),
                          button("Lagre", "configurationStudio.saveDraftVersion", primary=True))),
    spacing=18, maxWidthInfinity=True)
out = pathlib.Path(__file__).resolve().parents[2] / "skeleton" / "studio-hjelp-v2.skeleton.json"
out.write_text(json.dumps(skeleton, ensure_ascii=False, indent=2))
print(out)

helper = col(
    text("Hjelper", size=22, weight="semibold", color=INK),
    {"List": {"keypath": "workbenchHelper.state.messages", "flowElementSkeleton": col(
        text(kp="who", size=13, weight="semibold", color=MUTED), text(kp="text", color=INK), spacing=4,
        backgroundKeypath="bg", borderColor=LINE, borderWidth=1, cornerRadius=12, padding=14)}},
    row(button("Åpne Studio med denne beskrivelsen", "workbenchHelper.openStudioWithRequest", primary=True)),
    spacing=14, maxWidthInfinity=True)
(out.parent / "hjelper-v2.skeleton.json").write_text(json.dumps(helper, ensure_ascii=False, indent=2))
