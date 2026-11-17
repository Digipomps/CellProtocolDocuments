#!/usr/bin/env python3
"""Kontraktsjekk for invite_v1. Ren stdlib. Kjør: python3 check_fixtures.py  → 0 avvik = grønt.
Reglene her er invariantene i invite_v1.json, skrevet som kode. De sier hva implementeringen skal
avvise; de er ikke implementeringen."""
import json, glob, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
MAX_TTL = 90 * 86400
SENDER_VIEW = {"published": "published", "opened": "published", "accepted": "answered", "declined": "answered", "expired": "expired", "revoked": "revoked"}

def verdict(f):
    k = f["kind"]
    if k == "HavenInviteTicket":
        t = f["ticket"]
        if t["expiresAt"] <= t["createdAt"] or t["expiresAt"] < 1790000000:  # fixture-tid: "nå" = 1790000000
            return "rejected", "expired"
        if t["expiresAt"] - t["createdAt"] > MAX_TTL:
            return "rejected", "ttlOver90Days"
        s = f.get("sentinel")
        if s and s in json.dumps(t, ensure_ascii=False):
            return "rejected", "privateNotesLeak"
        if "basis" not in t:
            return "rejected", "missingBasis"
        return "valid", None
    if k == "InviteReply":
        d = f["reply"].get("decision")
        if d not in ("yes", "notNow", "never"):
            return "rejected", "unknownDecision"
        if d != "yes" and f.get("senderViewAfter") != "answered":
            return "rejected", "senderMustSeeAnsweredOnly"
        return "valid", None
    if k == "SenderView":
        want = SENDER_VIEW[f["lifecycle"]]
        return ("valid", None) if f["senderView"] == want else ("rejected", f"expected {want}")
    if k == "ContactRecord":
        b = f["record"]["basis"]
        extra = set(b) - {"name", "endpoint", "origin", "status"}
        if extra:
            return "rejected", "basis may not carry free text"
        if b.get("status") not in ("unconfirmed", "confirmed") or "origin" not in b:
            return "rejected", "basis needs status+origin"
        return "valid", None
    return "rejected", f"unknown kind {k}"

def main():
    n = bad = 0
    for p in sorted(glob.glob(os.path.join(HERE, "fixtures", "*.json"))):
        f = json.load(open(p, encoding="utf-8"))
        got, why = verdict(f)
        ok = got == f["expect"]
        n += 1; bad += (not ok)
        print(("OK  " if ok else "AVVIK ") + os.path.basename(p) + f"  → {got}" + (f" ({why})" if why else ""))
    print(f"{n} fixtures, {bad} avvik")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
