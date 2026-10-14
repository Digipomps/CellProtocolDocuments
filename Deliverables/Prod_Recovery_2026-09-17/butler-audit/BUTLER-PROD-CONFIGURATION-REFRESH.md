# Butler production configuration refresh audit

Date: 2026-09-18. Scope: source-only audit of `/private/tmp/haven-prod-20260917/CellScaffold`. No production data read, no host/source/Git mutation, no build or test execution. The integration worktree is changing under the root agent; line numbers below identify the inspected snapshot, not an immutable release.

## Decision

**An image/factory upgrade alone does not guarantee the new Butler thread/helper-tree UI for an existing user.** The saved active `CellConfiguration` contains its complete skeleton. Ordinary bootstrap intentionally preserves it when its source and reference set still match the published configuration. The old main factory (`b4a2779a`) and current factory both use the same `chatHub`, `agreementWorkbench`, `spatial`, and `perspective` references; adding the helper tree does not create the missing-reference condition that triggers repair.

There is a separate account-continuity nuance: that path rewrites the saved `chatHub` reference to the compatibility endpoint. The published-repair comparison uses the raw factory endpoint, so it can trigger repair on every full bootstrap even without a real schema change. Successful repair would pick up the new skeleton, but reference resolution/authorization may fail and return the old configuration. This is not a reliable, intentional version-migration contract and must not be used as evidence that all existing users upgrade.

## Evidence chain

1. `Sources/App/Cells/SimpleProjectManager/OrchestratorCell.swift:939` decodes the complete `cellConfig` from the persisted cell snapshot; `:947` encodes it. `:1253` also writes `CellConfiguration.json` and persists the resolver snapshot. Initialization reads that file (`:253`); `restoreSidecarConfigurationIfNeeded` only restores it when the active field is nil (`:288`). Restarting the image does not discard the saved skeleton.
2. `Sources/App/Controllers/PortholeWebSessionSupport.swift:716` invokes `repairedActiveConfigurationIfNeeded` during full bootstrap. Shell bootstrap deliberately skips repair, references and overlays. `:4516` obtains a matching current catalog entry and loads it only if `activeConfigurationNeedsPublishedRepair` returns true.
3. That predicate (`:4653`) checks only missing skeleton, missing source endpoint, or missing label/endpoint reference pairs. It does not compare skeleton content or factory version. Repair failures are caught and the old active configuration is returned.
4. `configurationWithDefaultChatWorkbench` (`:2926`) supplies the compiled factory skeleton only when the current skeleton is nil, a literal `Hello HAVEN` placeholder, or the specifically recognized legacy resource router. The legacy predicate requires all three encoded strings `chatHub.state.assistant.resourceMatches`, `Last inn flaten`, and `actionKeypath` (`:3000`). The old main chat factory does not contain `Last inn flaten`. This is not a general pre-helper-tree migration.
5. `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:2743` builds defaults from the compiled factories. Its cache (`:80`, `:105`, `:2757`) is request scoped. It does not keep an old compiled factory across image changes.
6. `Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1349` returns the current factory from `skeletonConfiguration` after normal authorization. PersonalChatHub does not expose `libraryCellConfiguration` or `editableCellConfigurationState`. The generic `EditableCellConfigurationOverlayResolver` therefore cannot freshen a saved PersonalChatHub skeleton through those source-backed paths.
7. `AccountContinuityPortholeCell` inherits the same persistence/bootstrap behavior. `configurationForControlCell` (`PortholeWebSessionSupport.swift:2969`) rewrites the chat reference endpoint, not skeleton content. `loadPortholeConfigurationInAction` (`:4591`) persists that rewritten configuration through the ordinary loader, after checking the existing compatibility mapping and proof-bearing session. The raw factory-reference comparison explains the repeated-repair nuance above. Pruned optional references can similarly trigger repeated repair attempts.
8. `Public/js/porthole-webo.js:898` fetches fresh bootstrap and renders the returned skeleton. The inspected `localStorage` calls persist floating-panel state, menu preferences/visibility and a bridge device identifier, not the active skeleton. Browser refresh still receives the server's persisted configuration. `Co-Pilot Chat` is shown as `Butler Chat` by `productFacingConfigurationName` (`:3956`).

## Same-surface reload is insufficient

`resolveRequestedCellConfigurationInAction` (`PortholeWebSessionSupport.swift:4354`) checks whether the request matches the active configuration **before** its pinned factory lookup. A matching UUID or name/source endpoint returns the current active configuration plus generic editable overlay. That overlay has no PersonalChatHub source-backed configuration contract to use, as above.

The ordinary JS library/menu load sends exactly such a lookup (`porthole-webo.js:3926`, `:3961`). Clicking Butler again while Butler is active can therefore preserve the stale skeleton. Sending a complete current configuration with the same identity does not bypass the earlier active-match shortcut either.

## Existing authorized refresh path

An existing session can load a **different already published, legitimately accessible surface**, then load Butler via its exact pinned lookup. Since Butler is no longer active, the pinned factory lookup (`PortholeWebSessionSupport.swift:4381`, helper `:4470`) can return the compiled configuration, and normal overlay/reference authorization/loading/persistence follows.

The second request, using the existing authenticated action route, is:

```json
{
  "keypath": "addConfiguration",
  "payload": {
    "configurationLookup": {
      "name": "Co-Pilot Chat",
      "sourceCellEndpoint": "cell:///PersonalChatHub"
    }
  }
}
```

Route: `POST /browserhead/porthole/action`. Bootstrap: `GET /browserhead/porthole/bootstrap` without `phase=shell`. Prefer the existing UI library navigation for the actual acceptance check; preserve all normal authentication and request protections when using the route. The alternative surface must be valid and already authorized; no new grants, identity substitution or direct persisted-file edits are involved.

This navigation replaces the active workspace configuration through its existing user action. It does not reset PersonalChatHub storage, conversation history or the identity vault. Do not claim it preserves arbitrary custom edits to the outgoing active workspace: changing surfaces intentionally replaces that active configuration. Do not use a fake/empty configuration as the first hop just to evade normal loading.

## Minimal implementation recommendation if automatic upgrade is required

For the stated overnight objective, add a narrowly identified built-in Butler migration to the existing repair path and make the same-active lookup consult that migration as well. Recognize only exact known previous factory skeletons (canonical serialized content/hash fixtures with fixed known source/name), then replace the skeleton with the current factory through the normal loader. Preserve user-customized skeletons, additional references and source-backed overrides. An absent revision marker alone cannot prove a configuration was not user edited. A broad condition such as “PersonalChatHub lacks helper-tree keypath” would overwrite custom workspaces and is not a safe migration predicate.

If introducing version metadata, stamp factory-managed configurations going forward, but use exact prior factory identification for unstamped existing snapshots. Retain normal reference authorization, rollback behavior, account-continuity endpoint mapping, and optional-reference isolation. No direct edits to user `CellConfiguration.json`, no clearing resolver snapshots, no vault/key replacement, and no global editable-configuration reset are needed.

`Services/EditableCellConfigurationSupport.swift:386` stores source-owned overrides in `CurrentCellConfiguration.json`; `shouldUseStateConfiguration` (`:1018`) explicitly preserves `hasStoredOverride`. Its reset contract applies only to cells implementing that contract and is not a Butler-wide refresh endpoint. Existing source-backed edit preservation is tested in `Tests/AppTests/PortholeConfigurationLoadingTests.swift:3330` and should remain intact.

## Verification required of the integrating agent

- Seed the exact old-main Butler configuration with its full existing reference set; bootstrap after upgrade must show the helper-tree opener. Confirm this currently fails without a migration or explicit navigation refresh.
- Exercise same-active `addConfiguration` and the existing alternate-surface/back-to-Butler path. The latter must show the new factory and persist it across reload/restart. No test was run by this audit.
- Repeat on both ordinary Orchestrator and AccountContinuityPorthole paths. Assert the compatibility mapping remains unchanged, no historical cell is relabelled/copied, and authorization failure rolls back without granting access. Include omitted optional references to avoid an unnoticed perpetual repair loop.
- Preserve a deliberately customized Butler skeleton and a source-backed `hasStoredOverride` configuration during automatic migration. Unknown legacy content must remain unchanged, with explicit navigation available.
- In an actual logged-in production browser, wait for full bootstrap, verify the current helper-tree action keypaths appear, click **Tråder**, expand the Butler root, select a valid node and verify scope/state updates. The helper rail is initially closed and the root initially collapsed; an invisible rail alone is not evidence the skeleton is old.
- Verify a chat message receives the intended model response in the selected scope and remains visible after reload. Static tree controls or a successful catalog lookup do not establish a functioning production Butler.

Production's actual saved configuration and user identity path were deliberately not inspected here. The result is a demonstrated code-level upgrade gap plus an existing refresh contract, not a claim that the production user currently has any particular persisted value.

## Operator preparation, 2026-09-18 00:07 UTC

Root verified the source-supported display parameter `showProductChrome=1` (`initialProductChromeRevealed`, `Public/js/porthole-webo.js:132`). It exposes the normal toolbar on `/browserhead/webo`; it does not change authorization. On the existing staging account, the normal **Bibliotek** menu opens and lists **CellScaffold Configuration Catalog** (`cell:///ConfigurationCatalog`) and **Butler Chat** (`cell:///PersonalChatHub`). No surface was loaded during this preparation; the menu was closed again. This provides an ordinary navigation route if the deployed account retains the old skeleton. Use a fresh accessibility snapshot after deployment, because element IDs will change.

Staging acceptance tab remains `333534269` in Chrome browser `2`, on `https://staging.haven.digipomps.org/browserhead/webo?showProductChrome=1`. Production acceptance tab is `333534367`, on the normal production `/browserhead/webo` URL. Do not clear conversation history or reuse the destructive synthetic-account Playwright fixtures against these accounts.

Both public `/health/build` endpoints still returned old application revision `b4a2779a5122d56ecdd9c9475fe772790bfd180c` during this preparation. This is pre-deployment navigation evidence, not acceptance of the candidate.
