# Local integrated-browser acceptance

These screenshots are LOCAL synthetic-account evidence, not production evidence.
The final source is PR247 candidate5db79970 plus the subsequent model-selection UI-envelope fix.

- Desktop/mobile: expand the Butler thread tree, select Docs/RAG, choose Bare denne, reload and verify the persisted composer target and open rail; return to Butler/subtree and close rail.
- Model chooser: discover a synthetic external descriptor, select it through the actual list payload, show actual consent review, reject confirmation without a trust packet. No external model is invoked.
- Live document: two authenticated sessions, image upload/edit, Flow update in the second session and persistence after reload.

Evidence logs: live-ui-final-4.log (15pass), live-butler-tree-final-3.log (3pass including expanded thread acceptance), live-document-final.log (1pass), under /private/tmp/haven-prod-20260917/logs.

Production acceptance remains pending immutable image publication and staging deployment.
