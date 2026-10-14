# Palazzo delivery verification — git-admin-losen-20260909

Verified at 2026-09-09T13:03:49.299176+00:00. Slice: Palazzo delivery. Status: VERIFIED for source preservation and fixture tests only.

## Decision

Preserve the exact eleven files as an archival source snapshot under the existing PDD deliverable in CellProtocolDocuments. Keep PalazzoScaffold/Tests/Roles/ intact as the live operational location. Do not initialize Git for the whole scaffold or move the live directory. Label the snapshot as an archive, record origin and SHA-256 hashes, and document that subsequent source changes require a new snapshot or a dedicated source-repository decision.

## Freshness and ownership

- PalazzoScaffold has no .git; git status --short exits 128 (not a git repository).
- Read all eleven scoped source files plus PDD PLAN.md, STATUS.md and TESTRESULT.md.
- Two existing __pycache__ files in the live directory were excluded from the scoped copy.
- Five JSON role files contain 26 purposes (gjest 8, annen-gjest 4, personale 4, hus 6, agent 4).
- Copies and manifest are stored in this temporary directory; no original source, PDD file or Git state was changed by this worker.
- All original and copied source bytes still match the initial manifest after tests; the temporary source directory contains exactly eleven files. Total: 57,559 bytes.

## Verification

- Python 3.13.2 parses all four Python files; all five role files parse as JSON.
- Initial selftest under the filesystem sandbox: schema check passed, fixtures could not bind loopback ports (PermissionError); exit 1. This was an environment restriction.
- Retry with loopback access and unmodified selftest: schema plus six cases passed; broken-positive and leaky-null could not bind 8101/8102 because Docker PID 1806 owns those listeners; exit 1. Docker was not modified or stopped.
- Final run: identical selftest.main, changing only its hardcoded base port from 8099 to 18199 in memory; source files remained unchanged. Ports 18200–18207 were checked with lsof before use. PYTHONDONTWRITEBYTECODE=1 and task-specific TMPDIR confined reports to this temporary directory. Schema check and all 8/8 fixture cases passed; exit 0. Raw evidence: selftest-isolated-ports.txt.
- Final expected exits: normal 0, broken-positive 2, leaky-null 2, ignores-principal 2, null-leak 3, unexpected-stop 4, privacy-leak 5, unevaluable 2.
- No real Palazzo server, external deployment, gateway secret or live user data was used. WP10 and WP11 remain outstanding.

## Limitations found by source inspection (no implementation changes)

- run_roles.py:264 and :404 execute all actions before calibration_verdict at :409; the calibration gate controls report interpretation, not whether later HTTP actions execute.
- run_roles.py:283 rejects a null calibration only when the outcome is OPPNÅDD. UKLASSIFISERT on a null calibration, or a missing calibration pair, is not rejected by this function. The unclassified exit check at :456 examines normal rows, not calibration rows.
- run_roles.py:450–458 has no nonzero exit for rows classified stop_is=feil, although the report lists them. A zero exit cannot be treated as proof that all purposes succeeded.
- roles_from_trust_package.py generates purpose records without calibration fields. Replacing handwritten agent.json with its output does not preserve the required calibration pair; selftest.check_schema would expose this, but run_roles.main does not call it.
- The fixed fixture ports are an actual portability issue on this machine. Future test improvements should use configurable or OS-assigned ports; source preservation does not require altering this historical delivery.
- Existing PDD PLAN.md calls PalazzoScaffold a repository although no Git repository exists; add an explicit archival decision note while preserving the operational path.

## Source inventory

| Path relative to PalazzoScaffold/Tests/Roles | Bytes | SHA-256 |
|---|---:|---|
| run_roles.py | 19524 | 1d9b398d15838b150d70e9d0caba19508a43160d83edefa86d81e00794449e57 |
| fixture_server.py | 6196 | 2e756769ffbadb13ee99f8e848b4ea936d5eeaf97daa92918ec1ac5a68a9e642 |
| selftest.py | 5993 | b50b31df4d11f40ad9a8af84190d1b5d1d8ce1de9ffeb54ec61115a5534dac4b |
| roles_from_trust_package.py | 5684 | 583034b339b94cd2fe34a69523455fcc637344b1f2dd4c2f7f9efb0d3c99bc33 |
| README.md | 3508 | 71ec2570c14c0fd3264c5b773033bfd118e26ad675d67cfdf66d5f821f644a0c |
| .gitignore | 43 | 3881a532969193702d51e3be0ffb7fe997139ecb5a59d0f62cc774e9d5513142 |
| roles/gjest.json | 4815 | 6b901ac37d572ee5402c4f4ec14a4abc1c71af8253054f9afd0568b9da1d5b7e |
| roles/annen-gjest.json | 2420 | d45c0cef20817444c952fcc238d115c6cd33d2d2f7b5ff7c5cc70f2fd7500519 |
| roles/personale.json | 3058 | e7e47662a351cd2ab5f2a2f7865f7451e47608fa30d3ae4d9ce69c84bb1b2362 |
| roles/hus.json | 3015 | f6f3ba14b5370b0ab1c3575548b74957cfdf086ab9aad8251b1c3a0aae639a20 |
| roles/agent.json | 3303 | b8c5f3dfec40b1f5214a44145b496e232be1ae092491614508b019ccfb694df6 |
