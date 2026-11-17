#!/usr/bin/env python3
"""Post-hoc prompt experiment for errors observed in run-01, not a held-out test."""
import run_dialogue as baseline

baseline.POLICY += """
Kvalitetskontroll før svar: Sammenhold hver påstått forutsetning med den relevante
kildeteksten. Ikke gjør separate grensesnitt til en obligatorisk rekkefølge med mindre
kilden sier det uttrykkelig. Bevar avgrensningen av hver rolle, særlig når kilden
sier subscription, get/set eller resolver-mediated. Tidligere assistentsvar er ikke
autoritativ evidens. Rett tidligere feil tydelig når kildene tilsier det.
"""
quote_case = next(dict(c, id="RQ01") for c in baseline.CASES if c["id"]=="Q01")
baseline.CASES = [dict(c, id="R"+c["id"][1:]) for c in baseline.CASES if c["id"] in {"D02","D03","D04"}]
baseline.CASES.append({"id":"R05", "group":"explicit-source-review", "sources":[1,2], "history":True,
    "q":"Kontroller nå forklaringen din mot avsnitt 2 og 3 i S2. Er det kildegrunnlag for at en vanlig get-lesing må gå gjennom Absorb først? Rett eventuelle feil i det du sa.",
    "criterion":"On explicit review, distinguish subscription admission from authorization of get/set and correct unsupported prerequisite."})
baseline.CASES.append(quote_case)

if __name__=="__main__":
    import hashlib, json
    from pathlib import Path
    p=baseline.ROOT/"evidence/diagnostic-config.json"
    if p.exists(): raise SystemExit("Diagnostic configuration already exists; preserve this run")
    p.write_text(json.dumps({"scope":"post-hoc diagnostic, not held-out evaluation",
        "policy":baseline.POLICY,"cases":baseline.CASES,
        "driver_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+"\n")
    baseline.main()
