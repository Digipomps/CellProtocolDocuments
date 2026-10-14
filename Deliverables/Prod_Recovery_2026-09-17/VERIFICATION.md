# Release verification — in progress

This index distinguishes local candidate evidence from CI and deployed behavior.
Nothing below certifies production until the deployment and browser rows are filled.
Original working trees and stashes remain preserved.

| Gate | Evidence | Result |
| --- | --- | --- |
| CellProtocol | PR40, main b5b7282b; local final log | 1190 tests, one skip, zero failures; Linux, macOS and strict-vault CI passed |
| DiMyMicropayments | PR13, main ff291214; signed migration/restart log | 54 tests passed; PR CI passed |
| DiMyMint | PR13, main 930efa50; CI35280805447 | Published pins verified; PostgreSQL CI passed; local32 tests with one DB skip |
| CellScaffold local Swift | swift-gates-4 plus final-retest and integration-linux-guard-fix | 40 groups executed. Two old fixtures failed and were corrected/retested; subsequent105 affected tests passed. Historical failing logs retained. |
| Gateway and credentials | gateway-review-final, gateway-final-consent-envelope | 47 focused tests plus final consent response test passed. Includes route binding, atomic sealed storage, consent one-use persistence. In-process provider doubles only. |
| Live local browser matrix | live-ui-final-4 | 15 cases passed |
| Extended Butler tree | live-butler-tree-final-3 | Desktop/mobile expand, child selection, scope, reload persistence and model chooser:3 cases passed |
| Live document collaboration | live-document-final | Image upload, second session updates and reload persistence passed |
| Legacy publication URLs | publication-legacy-route-final | 17 tests passed; decoded legacy state through actual HTTP, published body preserved and draft withheld |
| Linux API compatibility | linux-api-compatibility-final | 70 affected local tests passed; new Linux run pending after Darwin-only API and fixture corrections |
| Prior Linux f26 | https://github.com/Digipomps/CellScaffold/actions/runs/35289022246 | Full build + browser/document PASS; one cancellation-fixture failure among29Swift groups, corrected in5c |
| Admin navigation | admin-navigation-fix-final-2 | 16local tests PASS; exact built-in factory selection and mismatch guards |
| Stream cancellation fixture | webfetch-stream-cancellation-fix | 18local tests PASS; exact cancellation and deadline |
| Prior 5c Linux | https://github.com/Digipomps/CellScaffold/actions/runs/35291752920 | Build/allSwift/adminweb/document PASS;14/15browser PASS, discovery race corrected in6e |
| Latest 53064b03 Linux | https://github.com/Digipomps/CellScaffold/actions/runs/35296514357 | Build/adminweb/Thursdaybrowser/document PASS;28/29Swift groups PASS. Sole failure: WorkItem read-after-write durability mismatch in bolk28. Merge and image publication correctly stopped. Root cause reproduced and fixed in6fbe3c1a; exact replacement CI pending |
| Admin operator tools | HEAD975de195; admin-canonical-linux-no-permission-change.json | 71tests PASS local/Linux; actual Docker clone normalization PASS; live deployment pending |
| Backup repair | admin-backup-install-existing-permissions.json | Actual quiesced archive/checksum/manifest, same-container restart, readiness/metrics/fresh signed snapshot PASS; unit/security unchanged |
| In-flight provider node | provider-origin-node-regression-final; live-butler-origin-node | 9focused tests +3live localGUI cases PASS; synthetic provider callback changes scope while response is pending |
| Canonical WorkItem persistence | workitem-canonical-red/green logs;6fbe3c1a | Red:17 assertions failed, including all16 reloads. Sorted set encoding fix:20 focused tests PASS |
| Combined runtime/operator candidate |3eb47cd9; CI35308195232 | Exact full Linux CI35308195232 PASS, including all29Swiftgroups and browser/document proofs;71 operator/workflow tests PASS locally |
| Installed admin tools |admin-tool-install-acceptance.json | Reviewed controller/relay bytes installed root0755; private evidence roots0700. No container promotion |
| CellUtility readiness |b25841d3 plus isolated compatibility fixes | Workspace and final active-repo Xcode project each built;13 tests /0 failures each. Active source e5d553ed; notarized distribution pending |
| Main immutable images | main87256f9a;release35310477005 | SUCCESS; published metadata, OCI revisions and actual web/admin pulls verified |
| Staging web deploy/restart | receipt87256f9a; fresh public health09:13UTC | committed_verified; identity/storage fingerprints preserved. Logged-in browser acceptance pending |
| Production web deploy/restart | receipt87256f9a; fresh public health09:13UTC | committed_verified; same staging digest; identity/storage fingerprints preserved. Logged-in browser acceptance pending |
| Real model response | Pending existing approved provider | No actual model invocation proved; do not infer from synthetic tests |

Retained logs and SHA-256 manifest are under verification-evidence/. Local screenshots are under browser-evidence/. Repository inclusion/exclusion evidence is under repo-audit/ and butler-audit/. All original references were inventoried; unresolved native prototypes, separate services and draft authority changes are explicitly listed, not described as deployed.

## Web production deployment, 2026-09-18

Web production deploy completed08:46:47UTC: receipt committed_verified, main87256f9ac643b27fa4667ec167023249f2a2a5e6, same digestbe4429388d5dd0feb87f15287435ef6afe4f009b3c6290bdbd0de23b9e0d1a31 as staging. Independent public build and ready passed; targeted persistence/identity fingerprints identical before, first start and restart. Production browser was reloaded and now requires re-login; user asked, no answer yet. No claim of actual-account thread/UI/model acceptance. Admin staging still original healthyf76de5a; its candidate trial remains handoff_required and under diagnosis; admin production unchanged. Overall all-repository objective remains open.

## 2026-09-18T09:15:30.917853+00:00 — operator and native acceptance

Web staging and production run 87256f9ac643b27fa4667ec167023249f2a2a5e6, independently rechecked against public build/ready at 09:13 UTC. Main image release 35310477005 succeeded. Both exact deploy receipts are committed_verified, including restart and unchanged targeted identity/persistence fingerprints. Actual-account Butler UI and a real approved provider response are still not proved: staging tab 333534373 and production tab 333534372 are at login; the earlier user login questions remain pending.

Admin health root cause confirmed: nginx limits public health to 30/min, while retry loops exhausted it and starved /build. Operator eed434b9 (PR248) spaces requests by three seconds and adds explicit read-only reconciliation of an already restored original. 77 tests passed; installed hash3195af5f5fe5f1afe7935d5a5ca054ccff785620c6c9760d8ef2ecc5a9268924; previous source retained. Failed transaction852aece4 was reconciled with original ID/config/image/mounts/owner/manifest/current health, preserving its old failure evidence and explicitly not asserting live storage byte equality. New real staging rollback rehearsal27a4b4ed passed09:09:05UTC: candidate start, restart, fresh signed snapshot, SIGTERM at actual browser-proof request, rolled_back/interrupted. Staging original remains running; production admin untouched. Final admin promotion needs logged-in Inspector observation; no fabricated proof.

Binding PR34 merged maina5a9b1aa; exact main/tested tree709a37c4 confirmed, 678 passed/0 failed/24 skipped. HavenAgentD PR18 merged main5417a7c3, 274 native tests and exact CI passed; native installation still unverified. PythonPalazzo candidate1175b25 fixes copied-UUID operator admission, denies unauthorized shared feed and undeclared writes; actual WebSocket red/green plus full69tests passed and wheel built. Public bridge authenticated operator sessions remain unimplemented, readiness false. No Python host deployment; HD0077 Palazzo claim untouched.

HD0101 captures admin health/reconciliation defect; HD0102 captures PythonPalazzo identity defect. HD0100 overall remains DEPLOYING/incomplete. Old queue inventory has one undecided/208 but is169h old; do not use it as current completeness. The two web environment projections were repaired from fresh receipts/health; other feature inventory records preserved. HD validate937records/0problems. Original working trees/stashes preserved.
