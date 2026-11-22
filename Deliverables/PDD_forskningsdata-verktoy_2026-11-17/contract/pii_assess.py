#!/usr/bin/env python3
"""Reference assessment for research.pii-rules.v1 (PDD_forskningsdata-verktoy, WP1).

Pure stdlib. The Swift implementation (WP2) and the Py/Go ports must give the
same output for every case in pii-assessment-cases.v1.json.

Usage:
  python3 -I pii_assess.py check            # validate rules + run golden cases
  python3 -I pii_assess.py assess case.json # print assessment for one request
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(HERE, "research-pii-rules.v1.json")
CASES_PATH = os.path.join(HERE, "pii-assessment-cases.v1.json")
RULE_KEYS = {"answerForms", "minGroupSize", "finestBucket", "maxRetentionDays", "export",
             "requiresJustificationForRows", "requiresInstitutionalApproval", "allowed"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_rules(r):
    errors = []
    if r.get("schemaVersion") != "research.pii-rules.v1":
        errors.append("schemaVersion")
    ids = [d["id"] for d in r["degrees"]]
    ranks = [d["rank"] for d in r["degrees"]]
    if ranks != sorted(ranks) or len(set(ranks)) != len(ranks):
        errors.append("degree ranks must be unique and ascending")
    if set(r["rules"]) != set(ids):
        errors.append("rules must cover exactly the degrees")
    for d, rule in r["rules"].items():
        if set(rule) != RULE_KEYS:
            errors.append(f"rule {d}: keys {sorted(set(rule) ^ RULE_KEYS)}")
        for form in rule["answerForms"]:
            if form not in r["answerFormOrder"]:
                errors.append(f"rule {d}: unknown answer form {form}")
        if rule["finestBucket"] is not None and rule["finestBucket"] not in r["bucketOrder"]:
            errors.append(f"rule {d}: unknown bucket")
        if rule["export"] not in ("full", "aggregateOnly", "none"):
            errors.append(f"rule {d}: export")
    for kind, d in r["fieldKinds"].items():
        if d not in ids:
            errors.append(f"fieldKind {kind}: unknown degree {d}")
    # Stricter degree must never be looser than a weaker one.
    order = sorted(r["degrees"], key=lambda x: x["rank"])
    for a, b in zip(order, order[1:]):
        ra, rb = r["rules"][a["id"]], r["rules"][b["id"]]
        if rb["allowed"] and rb["minGroupSize"] < ra["minGroupSize"]:
            errors.append(f"{b['id']} has lower minGroupSize than {a['id']}")
        if not set(rb["answerForms"]) <= set(ra["answerForms"]) | {"pseudonymousRows"}:
            errors.append(f"{b['id']} allows an answer form {a['id']} does not")
    return errors


def assess(rules, req):
    rank = {d["id"]: d["rank"] for d in rules["degrees"]}
    by_rank = {d["rank"]: d["id"] for d in rules["degrees"]}
    buckets = rules["bucketOrder"]
    unknown = [f["kind"] for f in req.get("fields", []) if f["kind"] not in rules["fieldKinds"]]
    if unknown:
        return {"degree": None, "violations": ["unknown_field_kind"], "applied": [], "rules": None}
    kinds = [rules["fieldKinds"][f["kind"]] for f in req.get("fields", [])]
    degree = by_rank[max((rank[k] for k in kinds), default=0)]
    applied = []
    quasi = sum(1 for k in kinds if k == "quasi")
    eff = dict(rules["rules"][degree])
    for esc in rules["escalations"]:
        w, e = esc["when"], esc["effect"]
        hit = False
        if "quasiFieldCountAtLeast" in w and quasi >= w["quasiFieldCountAtLeast"]:
            hit = True
        if "researchQuestion.longitudinal" in w and req.get("researchQuestion", {}).get("longitudinal") is w["researchQuestion.longitudinal"]:
            hit = True
        if "populationBelowMultipleOfMinGroupSize" in w:
            pop = req.get("populationSize")
            if pop is not None and eff["minGroupSize"] > 0 and pop < w["populationBelowMultipleOfMinGroupSize"] * eff["minGroupSize"]:
                hit = True
        if not hit:
            continue
        applied.append(esc["id"])
        if "raiseDegreeTo" in e and rank[e["raiseDegreeTo"]] > rank[degree]:
            degree = e["raiseDegreeTo"]
            eff = dict(rules["rules"][degree])
        if "multiplyMinGroupSize" in e:
            eff["minGroupSize"] *= e["multiplyMinGroupSize"]
        if "coarsenBucketTo" in e and eff["finestBucket"] is not None:
            if buckets.index(e["coarsenBucketTo"]) > buckets.index(eff["finestBucket"]):
                eff["finestBucket"] = e["coarsenBucketTo"]
    v = []
    if not eff["allowed"]:
        v.append("degree_not_allowed")
    form = req.get("answerForm")
    if form not in eff["answerForms"]:
        v.append("answer_form_not_allowed")
    if form in ("pseudonymousRows", "rows") and eff["requiresJustificationForRows"] and not req.get("justification"):
        v.append("rows_require_justification")
    b = req.get("bucket")
    if b is not None and eff["finestBucket"] is not None and buckets.index(b) < buckets.index(eff["finestBucket"]):
        v.append("bucket_too_fine")
    pop = req.get("populationSize")
    if form == "aggregate" and pop is not None and pop < eff["minGroupSize"]:
        v.append("population_below_min_group_size")
    ret = req.get("retentionDays")
    if eff["maxRetentionDays"] is not None and ret is not None and ret > eff["maxRetentionDays"]:
        v.append("retention_too_long")
    if req.get("export") and eff["export"] == "none":
        v.append("export_not_allowed")
    if req.get("export") and eff["export"] == "aggregateOnly" and form != "aggregate":
        v.append("export_not_allowed")
    if eff["requiresInstitutionalApproval"] and req.get("realParticipants") and not req.get("institutionalApproval"):
        v.append("institutional_approval_required")
    return {"degree": degree, "violations": v, "applied": applied, "rules": eff}


def main():
    rules = load(RULES_PATH)
    if len(sys.argv) > 2 and sys.argv[1] == "assess":
        print(json.dumps(assess(rules, load(sys.argv[2])), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    errors = validate_rules(rules)
    for e in errors:
        print("REGELFEIL:", e)
    cases = load(CASES_PATH)["cases"]
    failed = 0
    for c in cases:
        got = assess(rules, c["request"])
        exp = c["expect"]
        ok = got["degree"] == exp["degree"] and sorted(got["violations"]) == sorted(exp["violations"]) \
            and all(got["rules"] and got["rules"][k] == val for k, val in exp.get("rules", {}).items()) \
            and sorted(got["applied"]) == sorted(exp.get("applied", []))
        if not ok:
            failed += 1
            print("FEIL", c["id"], json.dumps(got, ensure_ascii=False, sort_keys=True))
    print(f"regler: {len(errors)} feil; tilfeller: {len(cases) - failed} av {len(cases)} stemmer")
    return 1 if errors or failed else 0


if __name__ == "__main__":
    sys.exit(main())
