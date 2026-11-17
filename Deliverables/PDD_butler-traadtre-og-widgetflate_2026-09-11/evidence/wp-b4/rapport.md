Utgangspunkt: CellScaffold `d38151d7faad0793edd211b3115f043eb1de7f87`, CellProtocol `d810720f4910c026fe61dd9fd167357a328f7476`.

Endring: OK: WP-B4 paritet lagt paa skeleton-runtime.js porthole-webo.css. Diff: `evidence/wp-b4/change.patch`. Ny spec: `playwright/skeleton-native-parity.spec.js`.

## Web (uten server)

Node-kontrakt: exit 0 — # pass 11 # fail 0 
Playwright (ett nytt forsøk per test): exit 1 —   2 failed   68 passed (41.0s) 

```text
FEILET porthole-skeleton-atomic-swap.spec.js:176 Porthole rejects an uncommitted renderer without activating global listeners
FEILET skeleton-map-renderer.spec.js:61 renders geospatial features and dispatches feature payload
```

```text
✓   1 playwright/admin-web.spec.js:9:1 › admin catalog preserves filter focus and loads the control plane with mutation protection (903ms)
✓   2 playwright/admin-web.spec.js:76:1 › local usage-quota admin confirms and locks mutations while preserving human-readable context (881ms)
✓   3 playwright/admin-web.spec.js:158:1 › admin skeleton semantics remain labelled and responsive on a narrow viewport (314ms)
✓   4 playwright/butler-chat-starter.spec.js:158:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › tom samtale viser startforslag, ikke en tom rute (1.2s)
✓   5 playwright/butler-chat-starter.spec.js:184:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag holder seg lesbart på mobilbredde (670ms)
✓   6 playwright/butler-chat-starter.spec.js:209:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag forsvinner når samtalen er i gang, og Butler-svaret får egen stil (747ms)
✓   7 playwright/porthole-skeleton-atomic-swap.spec.js:35:1 › reordered JSON object fields preserve a document and its pending image read (255ms)
✓   8 playwright/porthole-skeleton-atomic-swap.spec.js:91:1 › Porthole retains the rendered node when a refreshed skeleton is malformed (162ms)
✘   9 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (350ms)
✘  10 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (retry #1) (268ms)
✓  11 playwright/porthole-skeleton-atomic-swap.spec.js:256:1 › Porthole rejects malformed action editor state without replacing the rendered node (404ms)
✓  12 playwright/porthole-skeleton-atomic-swap.spec.js:312:1 › Porthole exposes typed source write failure and keeps the working surface (384ms)
✓  13 playwright/porthole-skeleton-localization.spec.js:9:1 › Porthole applies supplied locale and catalog-only refresh to its mounted skeleton (358ms)
✓  14 playwright/rich-document.spec.js:77:1 › typing while an acknowledgement waits batches unsent edits and preserves the sent envelope (543ms)
✓  15 playwright/rich-document.spec.js:100:1 › cancelling unsent typing emits no empty mutation and keeps the in-flight edit (682ms)
✓  16 playwright/rich-document.spec.js:120:1 › two real Skeleton surfaces converge, preserve formatting, range comments, presence and chat (3.0s)
✓  17 playwright/rich-document.spec.js:149:1 › lost acknowledgement and unmounted draft do not lose local text (632ms)
✓  18 playwright/rich-document.spec.js:163:1 › onboarding, embedded image/chart and downloadable Markdown PDF Word (2.4s)
✓  19 playwright/rich-document.spec.js:193:1 › large image after bidirectional typing reaches both document surfaces (1.7s)
✓  20 playwright/rich-document.spec.js:216:1 › uncertain persistence retains the draft and retries the exact command (3.4s)
✓  21 playwright/rich-document.spec.js:230:1 › writing waits for the initial current definition (468ms)
✓  22 playwright/rich-document.spec.js:247:1 › switching document identity remounts the editor and keeps the old draft separate (279ms)
✓  23 playwright/skeleton-atomic-render.spec.js:40:3 › Skeleton renderer atomic admission › rejects root and nested multi-key updates without touching healthy DOM (244ms)
✓  24 playwright/skeleton-atomic-render.spec.js:85:3 › Skeleton renderer atomic admission › shows an explicit initial diagnostic and recovers with a later valid tree (224ms)
✓  25 playwright/skeleton-atomic-render.spec.js:112:3 › Skeleton renderer atomic admission › rejects schema-invalid ZStack, Object, and Toggle payloads without replacing healthy DOM (175ms)
✓  26 playwright/skeleton-atomic-render.spec.js:150:3 › Skeleton renderer atomic admission › deferred mount preserves visibility and presentation bindings through atomic admission (292ms)
✓  27 playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile (1.4s)
✓  28 playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA (672ms)
✓  29 playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data (175ms)
✓  30 playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata (538ms)
✓  31 playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll (166ms)
✓  32 playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls (458ms)
✓  33 playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate (150ms)
✓  34 playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control (948ms)
✓  35 playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops (953ms)
✓  36 playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic (777ms)
✓  37 playwright/skeleton-list-follow-tail.spec.js:60:3 › Skeleton list followTail › follows the newest row in a plain overflow container (no styleRole needed) (608ms)
✓  38 playwright/skeleton-list-follow-tail.spec.js:70:3 › Skeleton list followTail › leaves a reader who scrolled up where they were (471ms)
✓  39 playwright/skeleton-list-follow-tail.spec.js:80:3 › Skeleton list followTail › a list without followTail does not scroll on its own (240ms)
✓  40 playwright/skeleton-list-tree.spec.js:86:3 › Skeleton list tree (childrenKeypath) › starts fully expanded when no expandedStateKeypath is given, with depth per row (183ms)
✓  41 playwright/skeleton-list-tree.spec.js:97:3 › Skeleton list tree (childrenKeypath) › seeds expansion from state and collapses/expands locally without dispatching an action (272ms)
✓  42 playwright/skeleton-list-tree.spec.js:114:3 › Skeleton list tree (childrenKeypath) › selection follows the row identity when the tree is re-flattened (443ms)
✓  43 playwright/skeleton-list-tree.spec.js:133:3 › Skeleton list tree (childrenKeypath) › a plain list without childrenKeypath renders exactly as before (182ms)
✓  44 playwright/skeleton-localization.spec.js:36:1 › language changes update mounted labels, preserve draft/caret and make no network calls (174ms)
✓  45 playwright/skeleton-localization.spec.js:64:1 › language changes during an action preserve payload, busy state and completion (283ms)
✓  46 playwright/skeleton-localization.spec.js:74:1 › data updates change plural arguments and item labels, and missing values use a literal reserve (178ms)
✓  47 playwright/skeleton-localization.spec.js:89:1 › unsupported slots are rejected before replacing the healthy surface (217ms)
✓  48 playwright/skeleton-localization.spec.js:103:1 › 200 mounted message bindings reuse formatters on repeated language switches (222ms)
✓  49 playwright/skeleton-localization.spec.js:130:1 › catalog revisions replace text atomically without resetting a draft (192ms)
✓  50 playwright/skeleton-localization.spec.js:149:1 › localized arguments remain plain text even with a legacy HTML formatter (189ms)
✓  51 playwright/skeleton-localization.spec.js:163:1 › 1000 localized list items keep scroll position and nodes (585ms)
✓  52 playwright/skeleton-localization.spec.js:189:1 › the shared message corpus agrees in the actual browser (170ms)
✘  53 playwright/skeleton-map-renderer.spec.js:61:3 › Skeleton map visualization renderer › renders geospatial features and dispatches feature payload (300ms)
✘  54 playwright/skeleton-map-renderer.spec.js:61:3 › Skeleton map visualization renderer › renders geospatial features and dispatches feature payload (retry #1) (238ms)
✓  55 playwright/skeleton-native-parity.spec.js:53:3 › WP-B4 web/native layout parity › Spacer takes the free space; a Spacer with width stays fixed (376ms)
✓  56 playwright/skeleton-native-parity.spec.js:70:3 › WP-B4 web/native layout parity › stacks fill a column; their own alignment places content, not the stack (177ms)
✓  57 playwright/skeleton-native-parity.spec.js:93:3 › WP-B4 web/native layout parity › maxWidthInfinity fills a column, maxHeightInfinity fills a row, also after a layout variant flips the axis (285ms)
✓  58 playwright/skeleton-native-parity.spec.js:117:3 › WP-B4 web/native layout parity › TextArea modifiers form one box; the field inside has no border of its own (311ms)
✓  59 playwright/skeleton-native-parity.spec.js:138:3 › WP-B4 web/native layout parity › skeleton colors win over the product-view chat log colors (161ms)
✓  60 playwright/skeleton-navigation.spec.js:47:3 › Skeleton button navigation › renders a safe relative URL as a link and never dispatches a cell action (535ms)
✓  61 playwright/skeleton-navigation.spec.js:78:3 › Skeleton button navigation › rejects unsafe navigation and preserves non-empty keypath actions (487ms)
✓  62 playwright/skeleton-navigation.spec.js:127:3 › Skeleton button navigation › anchors the first VStack navigation bar, tracks active state, and single-flights its action (158ms)
✓  63 playwright/skeleton-navigation.spec.js:194:3 › Skeleton button navigation › uses the exact configuration name for cross-configuration active state and safe navigation (292ms)
✓  64 playwright/skeleton-navigation.spec.js:226:3 › Skeleton button navigation › keeps a ScrollView-anchored navigation bar pinned while its content scrolls (159ms)
✓  65 playwright/skeleton-navigation.spec.js:295:3 › Skeleton button navigation › fails closed when a navigation bar item is missing its portable label contract (256ms)
✓  66 playwright/skeleton-presentation.spec.js:37:3 › Skeleton presentation modifiers › opens, dismisses, and annotates a modal presentation (227ms)
✓  67 playwright/skeleton-real-configuration-corpus.spec.js:49:3 › Named real CellConfiguration/Skeleton corpus › renders every named checked-in skeleton artifact without generic fallback (1.2s)
✓  68 playwright/skeleton-tabs-optimistic-hold.spec.js:84:1 › naar handlingen feiler, gaar markeringen tilbake i stedet for aa bli staaende (1.1s)
✓  69 playwright/skeleton-textarea-submit.spec.js:33:3 › Skeleton TextArea submitActionKeypath › plain editor submits current text only to the dedicated action (158ms)
✓  70 playwright/skeleton-textarea-submit.spec.js:69:3 › Skeleton TextArea submitActionKeypath › rich Markdown editor honors submitActionKeypath and serialized payload (207ms)
✓  71 playwright/skeleton-visibility.spec.js:37:3 › Skeleton conditional visibility › updates element visibility from root data (227ms)
✓  72 playwright/skeleton-workbench-autoscroll.spec.js:54:3 › Skeleton workbench auto-scroll › coalesces back-to-back renders without losing bottom or reader intent (445ms)
```

Kontroll uten endringen (samme maskin) for specer som feilet:

```text
FEILET skeleton-map-renderer.spec.js:61 renders geospatial features and dispatches feature payload
```

## Fokuserte Swift-tester

`swift test --disable-sandbox --filter 'SkeletonRuntimeSourceTests|SkeletonStyleParityCSSDriftTests|ButlerChatSkeletonDumpTests|SkeletonElementParityMatrixTests'`: exit 1; Executed 3 tests, with 2 failures (0 unexpected) in 1.126 (1.126) seconds

```text
FEILET SkeletonElementParityMatrixTests/testMatrixRevisionMatchesPackagePin
FEILET SkeletonElementParityMatrixTests/testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips
FEILET SkeletonRuntimeSourceTests/testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning
FEILET SkeletonRuntimeSourceTests/testRuntimeDispatchesDropTargetPayloadAndHorizontalScrollAxis
```

## CI-filteret

```text
TOTALT {'started': 2430, 'passed': 2418, 'skipped': 10, 'failed': 2}
SIGNAL 0
AVBRUTT 0
KJENT -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
KJENT -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
NYE 0
```

## T-P1 hjelpertreet

```text
  ✓  1 playwright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2) (7.5s)
  1 passed (7.9s)
```

Commit: `5e8feb1ca9f26bfb6e0b5ef887e492653e0c8666` på `pdd/skjelett-elementer-web` (lokal). Sporede endringer etter commit: 
