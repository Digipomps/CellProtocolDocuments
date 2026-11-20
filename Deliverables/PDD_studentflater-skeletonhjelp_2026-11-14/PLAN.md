# PLAN — studentflater skeletonhjelp

Forutsetter G1 (godkjent 2026-11-15) og G1-GUI. Rekkefølge etter Kjetils svar 15.11: det som virker uten modell først, så modellutkast, så felles redigering.

| WP | purposeRef | Hva | Repo | Utfører | Tester (§5) | Artefakter |
|---|---|---|---|---|---|---|
| WP0 | — | Baseline: ren klone av origin/main, `swift build` + `swift test` i CellProtocol og CellScaffold; tall føres i TESTRESULT | CellProtocol, CellScaffold | Mac (kø) | test.build, test.regression | TESTRESULT.md#build |
| WP1 | public-skill-current | Oppdater `commons/skills/cellconfiguration-skeleton-authoring`: elementliste fra koden, Visibility/Reachability-avsnitt, `flowElementSkeleton` = VStack, ingen Mac-stier, Studio-veien for studenter | CellProtocol | Claude | test.skill.diff | PR |
| WP2 | local-check | Nytt kjørbart mål `skeleton-check` (CellBase): dekoder fil, kjører `SkeletonReachabilityAudit`, sjekker `flowElementSkeleton`, exit ≠0 ved funn; tester; tag + pin-løft etter vanlig løp | CellProtocol | Claude, Mac for bygg | test.local-check.cli | PR, TESTRESULT.md#local-check |
| WP3 | studio-audit | Studio kjører auditen ved `setDraftConfiguration`/`importDraftConfigurationFile` og eksponerer `state.reachability` (summary, findings) | CellScaffold | Claude, Mac for bygg | test.studio.audit, test.reachability.shipped | PR |
| WP4 | helper-routes | WorkbenchHelper: flate-bestillinger i «Denne flaten» peker til «Flater og GUI»; «Flater og GUI» får Studio-handlingene; rett «mangler»-teksten | CellScaffold | Claude | test.helper.routes | PR, images/hjelper-flate |
| WP5 | model-draft, model-route | Studio `assistDraft`: prompt med skill-utdrag + katalogkontrakter → AIGateway (PurposeBoundAIGateway, Mistral EU når tilgang finnes) → dekoding + audit → utkast eller forklaring; «Lag flaten med hjelp»-seksjonen | CellScaffold | Claude | test.model-draft.*, test.model-route.none, test.model-route.gateway (blocked til tilgang) | PR, images/studio-utkast-* |
| WP6 | co-edit-draft, discuss-draft | Felles utkast: delt utkastcelle med invitasjon/opptak via Agreement (InvitationAdmission fra PDD_dele-dokumenter), revisjonsbasert lagring med avvisning av utdatert skriving, «Del lenke i en samtale»; Binding viser og lagrer | CellProtocol, CellScaffold, Binding | Claude + Xcode | test.coedit.* | PR-er, images/felles-utkast-* |
| WP7 | root | E2E på staging med to ferske kontoer, etter FORESPOERSEL til Deploy med verifisert bygg | — | Claude + Deploy | test.e2e.student-flow, test.guide.walkthrough | TESTRESULT.md#e2e |

WP6 venter på G1 i PDD_dele-dokumenter (InvitationAdmission). Bygger ikke WP6 en egen invitasjonsmekanisme.
WP5s ekte modellkall venter på at tråden for modelltilgang avgjør Mistral-tilgangen for studenter.
