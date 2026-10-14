# Existing-data startup review

Read-only comparison of CellScaffold `b4a2779a5122d56ecdd9c9475fe772790bfd180c` to candidate `d7c2c332d8df3bd9777b2c6f7eebd714f7fc494a`, 2026-09-18. Scope: changed persisted models and startup/readiness code. No production data, secrets or host services inspected; no code/Git/build/test/deploy mutations.

## Concrete compatibility finding: existing publication entry `/verk` becomes 404

The baseline allows a publication entry with slug `verk`: its reserved-slug set does not contain that value. The candidate adds a constant `/pub/:slug/verk` route ahead of the entry route (`Sources/App/Controllers/VaporPublication.swift:133–141`). That route only calls `readPublicWorks` and returns 404 for its null result.

Existing publication themes decode with `showWorks == false` (`Sources/App/Cells/Publication/PublicationSupport.swift:313–319`). Consequently `readPublicWorks` returns null at `Sources/App/Cells/Publication/PublicationCell.swift:1554`, even when an existing published entry with slug `verk` is present. Its old navigation URL now reaches the new works route and its content is inaccessible. New installations without such entries do not reveal this regression.

Production occurrence is unknown: no stored production publication records were read.

Minimal correction: when works opt-in is off, the `/verk` route must preserve the existing published `entrySlug=verk` read through `readPublicSite`. Enabling works must also handle an existing slug collision explicitly, without silently displacing that entry.

Test seams: `Tests/AppTests/PublicationCellTests.swift:145` has the real site/owner/publication setup and a works-source stub. `PublicationPublicSurfaceTests.swift:15` has route setup, but its current route tests have no resolver and stop at 503. A useful legacy fixture encodes an established site and published entry, removes `sitesByID[*].theme.showWorks`, sets the entry slug to `verk`, then decodes the cell; exercise the real `/pub/<slug>/verk` route and assert the old body survives.

## Other bounded results

No additional concrete startup crash or incompatible decoder was found in the compared changes. In particular:

- New Butler selected-provider fields, helper tree and message node ID are optional. The consumed-consent dictionary uses `decodeIfPresent` and migrates old authorization receipts.
- WorkItem's added filter dictionary uses `decodeIfPresent` with an empty default. ArtistSales credits are optional. Publication's new theme flag has an explicit legacy default.
- Existing purpose-bound gateway and WebFetch cells default newly added receipt/fleet/ceiling fields on decode.
- Administrator readiness treats an absent registry/mandate pair as degraded-ready without provisioning authority; a partial or corrupt pair remains denied by design.
- `installPersonEvidence` creates its store configuration without reading existing data or requiring a new key at startup; its actual storage remains lazy.

These are source-review conclusions, not a production-data restart test.
