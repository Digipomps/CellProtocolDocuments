# Approved project baseline R1 — 116 tests

Kjetil: «Jeg godkjenner testrettelsen og én ny lokal baseline på 116 tester. Ved grønt kjører du de allerede godkjente 8+17 testene og fortsetter med prosjektflaten. Ingen CI eller deploy.»

Run exactly once via HAVEN-Deploy/_handoff/ARBEIDSBENK/PROJECT-WORKSPACE-BASELINE-R1-20261013/wp-project-baseline.sh run, after fresh exclusive ADMISSION from Deploy prosjekt køadministrasjon. Source is base 3a6680446e55fc1644afb368ac2bf48dd0720e30 plus the one approved stale-test patch; no product edit. Manifest SHA256 c2d85e1999b8bdd6fd4abe7121879426fff34f15d7ece11a07ced8e2aa60f73b.

Use the existing bounded managed cache, two jobs, capacity floor 40 GiB / 10 percent after 10 GiB reserve. Frozen collector is report-only. No CI/deploy. Stop on red. Preserve terminal logs/results and pins. On green, activate the unchanged G2-W1-CONTINUE-20261013 (manifest 9c481f32f273cd928a09eca02fd54073f2091fb591589ed78e220af4524ce469) with fresh admission; its activated queue envelope must use blank first line (HAVEN root). Never change that frozen packet.
