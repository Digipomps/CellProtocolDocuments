#!/usr/bin/env python3
"""Validerer fixtures mot apns_invite_v1.json uten eksterne pakker.
positive/ må bestå, negative/ må feile (og feile med riktig grunn, oppgitt i filens "_expect").
Bruk: python3 validate_contract.py            (kjører alle)
Utdata: siste linje er «RESULT: N grønne, M røde»."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "apns_invite_v1.json"), encoding="utf-8"))
REG = C["endpoints"]["push.register"]["request"]
PAY = C["endpoints"]["invite.push"]["apns"]["payload"]
TICKET = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

def check_register(d):
    errs = []
    for k in REG["required"]:
        if k not in d: errs.append("missing:" + k)
    for k in d:
        if k not in REG["fields"]: errs.append("extra:" + k)
    f = REG["fields"]
    if "environment" in d and d["environment"] not in f["environment"]["enum"]: errs.append("bad_environment")
    for k in ("entity", "bundleId", "token"):
        if k in d and not re.match(f[k]["pattern"], str(d[k])): errs.append("bad_" + k)
    if d.get("schema") != f["schema"]["const"]: errs.append("bad_schema")
    sg = d.get("signer")
    if isinstance(sg, dict):
        for k in f["signer"]["required"]:
            if k not in sg: errs.append("signer_missing:" + k)
        if str(sg.get("uuid", "")).lower() != str(d.get("entity", "")).lower(): errs.append("signer_not_entity")
    elif "signer" in d: errs.append("signer_not_object")
    pf = d.get("proof")
    if isinstance(pf, dict):
        for k in f["proof"]["required"]:
            if k not in pf: errs.append("proof_missing:" + k)
        if str(pf.get("by", "")).lower() != str(d.get("entity", "")).lower(): errs.append("proof_not_by_entity")
        if not re.match(r"^[A-Za-z0-9_-]{16,}$", str(pf.get("sg", ""))): errs.append("bad_signature")
    elif "proof" in d: errs.append("proof_not_object")
    if "issuedAt" in d and not isinstance(d["issuedAt"], int): errs.append("bad_issuedAt")
    return errs

def check_payload(d):
    errs = []
    raw = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(raw) > PAY["maxBytes"]: errs.append("too_large")
    for k in PAY["required"]:
        if k not in d: errs.append("missing:" + k)
    for k in d:
        if k not in PAY["required"]: errs.append("extra:" + k)
    aps, hv = d.get("aps", {}), d.get("haven", {})
    for k in aps:
        if k != "alert": errs.append("extra_aps:" + k)
    al = aps.get("alert", {})
    if not isinstance(al, dict): errs.append("alert_not_object"); al = {}
    for k in al:
        if k not in ("title", "body"): errs.append("extra_alert:" + k)
    if al.get("title") != "HAVEN": errs.append("bad_title")
    if al.get("body") != PAY["aps"]["alert"]["bodyNb"]: errs.append("bad_body")
    for k in hv:
        if k not in ("k", "id"): errs.append("extra_haven:" + k)
    if hv.get("k") != "invite": errs.append("bad_kind")
    if not TICKET.match(str(hv.get("id", ""))): errs.append("bad_ticket_id")
    return errs

CHECKS = {"register": check_register, "payload": check_payload}
green = red = 0
for polarity in ("positive", "negative"):
    d = os.path.join(HERE, "fixtures", polarity)
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"): continue
        doc = json.load(open(os.path.join(d, name), encoding="utf-8"))
        kind = doc.pop("_kind"); expect = doc.pop("_expect", None)
        errs = CHECKS[kind](doc)
        ok = (not errs) if polarity == "positive" else (bool(errs) and (expect is None or any(e == expect or e.startswith(expect) for e in errs)))
        print(("OK   " if ok else "FEIL ") + polarity + "/" + name + ("" if not errs else "  -> " + ",".join(errs)))
        green += ok; red += (not ok)
print("RESULT: %d grønne, %d røde" % (green, red))
sys.exit(1 if red else 0)
