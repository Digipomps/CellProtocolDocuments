# Skeleton style vocabulary and public book fixture audit

Read-only source audit, 2026-09-17. Candidate roots `/private/tmp/haven-prod-20260917/CellScaffold` and sibling `CellProtocol`. No source, Git, build, test or deployment mutations. Only this report was written.

| Corpus | Observed result | Classification | Minimal correction |
|---|---|---|---|
| Public CSS/HTML/JS style-role selectors vs CP registry | 139 found, 61 declared; 79 missing, 1 stale, 3 JS overlaps, no native overlaps | stale shared vocabulary | Update CP sets, retain strict equality tests |
| Native SkeletonView style handling | Metadata-only for new roles; markdown and chat-primary-action remain special | no new native styling contract | Keep nativeOnlyRoles and agreedRoles unchanged |
| Group20 MarkdownRendererCellTests | All 4 tests fail, 23 assertions; candidate docs folder empty, sibling missing | test-harness-gap | Materialize the exact pinned public book used by CI |

Apply only in `CellProtocol/Sources/CellBase/Skeleton/SkeletonStyleParity.swift`: add the 79 roles below to `webStylesheetRoles`; remove `admin-action-row`. Result is 139 roles. Set `webJavaScriptRoles` to `[]`: its existing three roles (`admin-form-field`, `admin-page-heading`, `admin-section-heading`) are included in the additions and now have actual CSS selectors. Change its documentation to mean JS-only roles without CSS. Retain JS handling in the renderer. Update the generated-count/date comment. Do not change agreedRoles (empty), nativeOnlyRoles (`markdown`, `chat-primary-action`), classify, normalization, or the drift-test assertions.

Evidence: `CellScaffold/Tests/AppTests/SkeletonStyleParityCSSDriftTests.swift:24` scans css/html/js with exact regex at112; assertions38-87 enforce equality and disjoint JS-only classification. `Public/js/skeleton-runtime.js:839` and1066 still handle the three admin roles; their CSS sources are listed below. Native `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:199-218` only assigns accessibility metadata for generic roles, while1688 implements markdown and1882 recognizes chat-primary-action. No new admin/Butler role has special native handling in the inspected CellApple sources.

Exact additions (all classify webOnly, 71 admin and 8 Butler/chat):

| Role | First matching source selector |
|---|---|
| `admin-actions` | `Public/css/admin-skeleton.css:653` |
| `admin-banner-critical` | `Public/css/admin-skeleton.css:815` |
| `admin-banner-ok` | `Public/css/admin-skeleton.css:813` |
| `admin-banner-warn` | `Public/css/admin-skeleton.css:814` |
| `admin-button` | `Public/css/admin-skeleton.css:656` |
| `admin-button-danger` | `Public/css/admin-skeleton.css:658` |
| `admin-button-primary` | `Public/css/admin-skeleton.css:657` |
| `admin-button-quiet` | `Public/css/admin-skeleton.css:659` |
| `admin-canvas` | `Public/css/admin-skeleton.css:232` |
| `admin-crumb` | `Public/css/admin-skeleton.css:193` |
| `admin-crumb-current` | `Public/css/admin-skeleton.css:199` |
| `admin-crumb-sep` | `Public/css/admin-skeleton.css:206` |
| `admin-drawer` | `Public/css/admin-skeleton.css:586` |
| `admin-drawer-body` | `Public/css/admin-skeleton.css:637` |
| `admin-drawer-footer` | `Public/css/admin-skeleton.css:645` |
| `admin-drawer-header` | `Public/css/admin-skeleton.css:616` |
| `admin-drawer-title` | `Public/css/admin-skeleton.css:624` |
| `admin-empty` | `Public/css/admin-skeleton.css:964` |
| `admin-env` | `Public/css/admin-skeleton.css:211` |
| `admin-field` | `Public/css/admin-skeleton.css:737` |
| `admin-field-hint` | `Public/css/admin-skeleton.css:745` |
| `admin-field-label` | `Public/css/admin-skeleton.css:739` |
| `admin-form-field` | `Public/css/admin-skeleton.css:703` |
| `admin-main` | `Public/css/admin-skeleton.css:172` |
| `admin-note` | `Public/css/admin-skeleton.css:828` |
| `admin-page-header` | `Public/css/admin-skeleton.css:239` |
| `admin-page-heading` | `Public/css/admin-skeleton.css:247` |
| `admin-page-subtitle` | `Public/css/admin-skeleton.css:255` |
| `admin-page-titles` | `Public/css/admin-skeleton.css:245` |
| `admin-panel` | `Public/css/admin-skeleton.css:299` |
| `admin-panel-body` | `Public/css/admin-skeleton.css:336` |
| `admin-panel-head` | `Public/css/admin-skeleton.css:318` |
| `admin-panel-row` | `Public/css/admin-skeleton.css:343` |
| `admin-picker` | `Public/css/admin-skeleton.css:764` |
| `admin-rail` | `Public/css/admin-skeleton.css:80` |
| `admin-rail-brand` | `Public/css/admin-skeleton.css:97` |
| `admin-rail-kind` | `Public/css/admin-skeleton.css:113` |
| `admin-rail-mark` | `Public/css/admin-skeleton.css:105` |
| `admin-rail-nav` | `Public/css/admin-skeleton.css:129` |
| `admin-rail-nav-current` | `Public/css/admin-skeleton.css:162` |
| `admin-rail-section` | `Public/css/admin-skeleton.css:120` |
| `admin-section-heading` | `Public/css/admin-skeleton.css:325` |
| `admin-shell` | `Public/css/admin-skeleton.css:50` |
| `admin-stat` | `Public/css/admin-skeleton.css:348` |
| `admin-stat-label` | `Public/css/admin-skeleton.css:357` |
| `admin-stat-value` | `Public/css/admin-skeleton.css:366` |
| `admin-status-critical` | `Public/css/admin-skeleton.css:793` |
| `admin-status-ok` | `Public/css/admin-skeleton.css:791` |
| `admin-status-unknown` | `Public/css/admin-skeleton.css:794` |
| `admin-status-warn` | `Public/css/admin-skeleton.css:792` |
| `admin-table` | `Public/css/admin-skeleton.css:440` |
| `admin-table-empty` | `Public/css/admin-skeleton.css:538` |
| `admin-table-frame` | `Public/css/admin-skeleton.css:340` |
| `admin-table-head` | `Public/css/admin-skeleton.css:404` |
| `admin-table-row` | `Public/css/admin-skeleton.css:442` |
| `admin-table-row-note` | `Public/css/admin-skeleton.css:525` |
| `admin-table-scroll` | `Public/css/admin-skeleton.css:428` |
| `admin-tabs` | `Public/css/admin-skeleton.css:263` |
| `admin-tabs-current` | `Public/css/admin-skeleton.css:292` |
| `admin-td` | `Public/css/admin-skeleton.css:452` |
| `admin-td-actions` | `Public/css/admin-skeleton.css:509` |
| `admin-td-mono` | `Public/css/admin-skeleton.css:453` |
| `admin-td-primary` | `Public/css/admin-skeleton.css:490` |
| `admin-td-secondary` | `Public/css/admin-skeleton.css:498` |
| `admin-td-stack` | `Public/css/admin-skeleton.css:478` |
| `admin-td-status` | `Public/css/admin-skeleton.css:454` |
| `admin-th` | `Public/css/admin-skeleton.css:412` |
| `admin-timestamp` | `Public/css/admin-skeleton.css:223` |
| `admin-toggle` | `Public/css/admin-skeleton.css:752` |
| `admin-topbar` | `Public/css/admin-skeleton.css:180` |
| `admin-value-mono` | `Public/css/admin-skeleton.css:391` |
| `butler-helper-tree-chat` | `Public/css/porthole-webo.css:4675` |
| `butler-helper-tree-layout` | `Public/css/porthole-webo.css:4656` |
| `butler-helper-tree-rail` | `Public/css/porthole-webo.css:4664` |
| `chat-clarification-card` | `Public/css/porthole-webo.css:3699` |
| `chat-help-line` | `Public/css/porthole-webo.css:3800` |
| `chat-help-line-text` | `Public/css/porthole-webo.css:3796` |
| `chat-starter-card` | `Public/css/porthole-webo.css:3708` |
| `chat-starter-row` | `Public/css/porthole-webo.css:3739` |


Public book setup: `CellScaffold/Sources/App/Cells/Markdown/BookReferenceCatalog.swift:515-532` searches `CELLPROTOCOL_DOCUMENTS_ROOT/Book/book_catalog.json`, then nested and sibling CellProtocolDocuments. The candidate nested directory exists but is empty; sibling is missing. Its default package root comes from the compiled source path (194-200), not cwd. The local CI replica omitted the explicit docs checkout in `.github/workflows/admin-scaffold-image.yml:43-59`. The workflow pins `a08f72f369fad5be22364e35f92de52a41e04033` at31. Materialize that public snapshot at `/private/tmp/haven-prod-20260917/CellScaffold/CellProtocolDocuments`, or set CELLPROTOCOL_DOCUMENTS_ROOT to an equivalent pinned public checkout. Do not loosen render assertions or use catalog-less fallback slugs.

The tests in `MarkdownRendererCellTests.swift:10,25,39,78` require book_catalog.json and these catalog entries/files:

- book-home → Book/00_Book_Home.md
- book-10-quickstart → Book/10_Quickstart.md (slug quickstart, /book/quickstart)
- book-17-conference-ownership-dataflow → Book/17_Conference_Ownership_Dataflow.md
- book-18-conference-connectionhub-agreement-lifecycle → Book/18_Conference_ConnectionHub_Agreement_Entity_Lifecycle.md

Use the whole pinned public Book snapshot, preserving linked resources. File names were cross-checked against the available local Book/book_catalog.json; this audit did not inspect a Git revision. CI verifies the pinned checkout separately. Successful catalogs are cached; unsuccessful loads are not, and `invalidateCachedCatalogForTesting` exists at213 if root reruns inside the same process.

Recommended verification by root after integration: existing CP SkeletonStyleParityTests, CS SkeletonStyleParityCSSDriftTests, then MarkdownRendererCellTests with pinned book installed. Strict expected results remain webStylesheetRoles count139 with no missing/stale/JS/native overlap; native roles still classify nativeOnly; agreedRoles stays empty; four Markdown tests render actual canonical content and links. No render/behavior parity is certified by this static audit.

Concurrency note: while this report was being assembled, root updated the candidate stylesheet set to139. The exact additions table is therefore preserved from the failing bolk-28 log and cross-checked against current CSS, rather than recomputed against the already corrected set. This agent made no source changes.
