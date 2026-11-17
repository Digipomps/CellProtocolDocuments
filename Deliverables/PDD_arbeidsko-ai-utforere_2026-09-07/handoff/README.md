# Codex-handoff — arbeidskø (2026-09-07)

Les: `../PLAN.md`, `../FORMAALSSPEC.md` §1/§5, `HAVEN-Deploy/CONTRACT.md`, `AGENTS.md`, `FORMAAL.md`, `tools/hd.py`, `tools/hdlib/`, `HAVEN/_losen-queue/runner.sh` (adapter-forbildet).
Slicer WP0–WP6 GODKJENT; WP7 er Kjetils; WP-GUI BLOKKERT.
Regler: stdlib-only python ≥3.10 (VM har 3.10.12 — ikke bruk 3.11+-syntaks); ingen git-mutasjon; ingen `rm` i HAVEN-treet; eksisterende tester og `hd validate` skal være grønne; hemmeligheter aldri i jobbfil/event; ikke installer den nye plisten selv (WP7 er Kjetils) — men test dispatcheren direkte (`python3 tools/dispatch.py --once`) mot en ekte read-only Codex-jobb og en ekte claude-local-jobb.
Rapport: `HAVEN-Deploy/docs/Rapport_Arbeidsko_2026-09-07.md` + `../TESTRESULT.md` med ankre `#build #regression #schema #dispatch #codex #claude #cell #board #lesson #no-shell #no-escalation #e2e`. Svar kun med rapporten.
