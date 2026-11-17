STATUS: LEVERT — commit 81b47bada14068cb9b98b015a1e7940412e302d8 på pdd/skjelett-elementer-web — en rad bryter bare med wrap: true på web, som i appen; nettleserspecer, CI og T-P1 uten nye feil

# WP-B6 — en rad bryter linjen bare med wrap: true, som i appen

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-b6-rad.sh` 2026-09-20T13:21:09Z. Bevis: `evidence/wp-b6/`.

Utgangspunkt: CellScaffold `pdd/skjelett-elementer-web` @ `055b34385a34663ce2075572498cd9e504fa71c7` (WP-F1 web), CellProtocol `1b92d01a030bac424e5172c875753a1dcfe41752`.

Endring: OK: WP-B6 lagt paa (9 filer); ny spec `playwright/skeleton-row-wrap-parity.spec.js`. Diff: `evidence/wp-b6/change.patch`.

## Web (uten server)

Node-kontrakt: exit 0 — # pass 11 # fail 0 
Playwright (ett nytt forsøk per test): exit 1 —   1 failed   74 passed (34.7s) 

```text
FEILET porthole-skeleton-atomic-swap.spec.js:176 Porthole rejects an uncommitted renderer without activating global listeners
```

```text
✓   1 playwright/admin-web.spec.js:9:1 › admin catalog preserves filter focus and loads the control plane with mutation protection (458ms)
✓   2 playwright/admin-web.spec.js:76:1 › local usage-quota admin confirms and locks mutations while preserving human-readable context (650ms)
✓   3 playwright/admin-web.spec.js:158:1 › admin skeleton semantics remain labelled and responsive on a narrow viewport (191ms)
✓   4 playwright/butler-chat-starter.spec.js:158:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › tom samtale viser startforslag, ikke en tom rute (693ms)
✓   5 playwright/butler-chat-starter.spec.js:184:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag holder seg lesbart på mobilbredde (686ms)
✓   6 playwright/butler-chat-starter.spec.js:209:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag forsvinner når samtalen er i gang, og Butler-svaret får egen stil (613ms)
✓   7 playwright/porthole-skeleton-atomic-swap.spec.js:35:1 › reordered JSON object fields preserve a document and its pending image read (270ms)
✓   8 playwright/porthole-skeleton-atomic-swap.spec.js:91:1 › Porthole retains the rendered node when a refreshed skeleton is malformed (142ms)
✘   9 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (188ms)
✘  10 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (retry #1) (211ms)
✓  11 playwright/porthole-skeleton-atomic-swap.spec.js:256:1 › Porthole rejects malformed action editor state without replacing the rendered node (263ms)
✓  12 playwright/porthole-skeleton-atomic-swap.spec.js:312:1 › Porthole exposes typed source write failure and keeps the working surface (274ms)
✓  13 playwright/porthole-skeleton-localization.spec.js:9:1 › Porthole applies supplied locale and catalog-only refresh to its mounted skeleton (261ms)
✓  14 playwright/rich-document.spec.js:77:1 › typing while an acknowledgement waits batches unsent edits and preserves the sent envelope (495ms)
✓  15 playwright/rich-document.spec.js:100:1 › cancelling unsent typing emits no empty mutation and keeps the in-flight edit (529ms)
✓  16 playwright/rich-document.spec.js:120:1 › two real Skeleton surfaces converge, preserve formatting, range comments, presence and chat (2.5s)
✓  17 playwright/rich-document.spec.js:149:1 › lost acknowledgement and unmounted draft do not lose local text (474ms)
✓  18 playwright/rich-document.spec.js:163:1 › onboarding, embedded image/chart and downloadable Markdown PDF Word (2.0s)
✓  19 playwright/rich-document.spec.js:193:1 › large image after bidirectional typing reaches both document surfaces (1.5s)
✓  20 playwright/rich-document.spec.js:216:1 › uncertain persistence retains the draft and retries the exact command (3.2s)
✓  21 playwright/rich-document.spec.js:230:1 › writing waits for the initial current definition (557ms)
✓  22 playwright/rich-document.spec.js:247:1 › switching document identity remounts the editor and keeps the old draft separate (388ms)
✓  23 playwright/skeleton-atomic-render.spec.js:40:3 › Skeleton renderer atomic admission › rejects root and nested multi-key updates without touching healthy DOM (173ms)
✓  24 playwright/skeleton-atomic-render.spec.js:85:3 › Skeleton renderer atomic admission › shows an explicit initial diagnostic and recovers with a later valid tree (147ms)
✓  25 playwright/skeleton-atomic-render.spec.js:112:3 › Skeleton renderer atomic admission › rejects schema-invalid ZStack, Object, and Toggle payloads without replacing healthy DOM (173ms)
✓  26 playwright/skeleton-atomic-render.spec.js:150:3 › Skeleton renderer atomic admission › deferred mount preserves visibility and presentation bindings through atomic admission (293ms)
✓  27 playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile (1.1s)
✓  28 playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA (514ms)
✓  29 playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data (177ms)
✓  30 playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata (384ms)
✓  31 playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll (253ms)
✓  32 playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls (408ms)
✓  33 playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate (195ms)
✓  34 playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control (695ms)
✓  35 playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops (592ms)
✓  36 playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic (754ms)
✓  37 playwright/skeleton-format-round-b.spec.js:43:3 › WP-F format round B › instanceIDKeypath: one surface per List row, own state, survives reorder (308ms)
✓  38 playwright/skeleton-format-round-b.spec.js:66:3 › WP-F format round B › ComponentSurface needs exactly one of instanceID and instanceIDKeypath (256ms)
✓  39 playwright/skeleton-format-round-b.spec.js:84:3 › WP-F format round B › layout variants: width at wide, hidden at narrow, switching keeps the element (210ms)
✓  40 playwright/skeleton-format-round-b.spec.js:102:3 › WP-F format round B › a fixed width holds in a row like a native frame; the flexible neighbour wraps (204ms)
✓  41 playwright/skeleton-list-follow-tail.spec.js:60:3 › Skeleton list followTail › follows the newest row in a plain overflow container (no styleRole needed) (333ms)
✓  42 playwright/skeleton-list-follow-tail.spec.js:70:3 › Skeleton list followTail › leaves a reader who scrolled up where they were (378ms)
✓  43 playwright/skeleton-list-follow-tail.spec.js:80:3 › Skeleton list followTail › a list without followTail does not scroll on its own (233ms)
✓  44 playwright/skeleton-list-tree.spec.js:86:3 › Skeleton list tree (childrenKeypath) › starts fully expanded when no expandedStateKeypath is given, with depth per row (163ms)
✓  45 playwright/skeleton-list-tree.spec.js:97:3 › Skeleton list tree (childrenKeypath) › seeds expansion from state and collapses/expands locally without dispatching an action (314ms)
✓  46 playwright/skeleton-list-tree.spec.js:114:3 › Skeleton list tree (childrenKeypath) › selection follows the row identity when the tree is re-flattened (285ms)
✓  47 playwright/skeleton-list-tree.spec.js:133:3 › Skeleton list tree (childrenKeypath) › a plain list without childrenKeypath renders exactly as before (143ms)
✓  48 playwright/skeleton-localization.spec.js:36:1 › language changes update mounted labels, preserve draft/caret and make no network calls (174ms)
✓  49 playwright/skeleton-localization.spec.js:64:1 › language changes during an action preserve payload, busy state and completion (273ms)
✓  50 playwright/skeleton-localization.spec.js:74:1 › data updates change plural arguments and item labels, and missing values use a literal reserve (143ms)
✓  51 playwright/skeleton-localization.spec.js:89:1 › unsupported slots are rejected before replacing the healthy surface (143ms)
✓  52 playwright/skeleton-localization.spec.js:103:1 › 200 mounted message bindings reuse formatters on repeated language switches (206ms)
✓  53 playwright/skeleton-localization.spec.js:130:1 › catalog revisions replace text atomically without resetting a draft (158ms)
✓  54 playwright/skeleton-localization.spec.js:149:1 › localized arguments remain plain text even with a legacy HTML formatter (157ms)
✓  55 playwright/skeleton-localization.spec.js:163:1 › 1000 localized list items keep scroll position and nodes (482ms)
✓  56 playwright/skeleton-localization.spec.js:189:1 › the shared message corpus agrees in the actual browser (136ms)
✓  57 playwright/skeleton-map-renderer.spec.js:61:3 › Skeleton map visualization renderer › renders geospatial features and dispatches feature payload (245ms)
✓  58 playwright/skeleton-native-parity.spec.js:53:3 › WP-B4 web/native layout parity › Spacer takes the free space; a Spacer with width stays fixed (141ms)
✓  59 playwright/skeleton-native-parity.spec.js:70:3 › WP-B4 web/native layout parity › stacks fill a column; their own alignment places content, not the stack (200ms)
✓  60 playwright/skeleton-native-parity.spec.js:93:3 › WP-B4 web/native layout parity › maxWidthInfinity fills a column, maxHeightInfinity fills a row, also after a layout variant flips the axis (314ms)
✓  61 playwright/skeleton-native-parity.spec.js:117:3 › WP-B4 web/native layout parity › TextArea modifiers form one box; the field inside has no border of its own (174ms)
✓  62 playwright/skeleton-native-parity.spec.js:138:3 › WP-B4 web/native layout parity › skeleton colors win over the product-view chat log colors (156ms)
✓  63 playwright/skeleton-navigation.spec.js:47:3 › Skeleton button navigation › renders a safe relative URL as a link and never dispatches a cell action (247ms)
✓  64 playwright/skeleton-navigation.spec.js:78:3 › Skeleton button navigation › rejects unsafe navigation and preserves non-empty keypath actions (313ms)
✓  65 playwright/skeleton-navigation.spec.js:127:3 › Skeleton button navigation › anchors the first VStack navigation bar, tracks active state, and single-flights its action (166ms)
✓  66 playwright/skeleton-navigation.spec.js:194:3 › Skeleton button navigation › uses the exact configuration name for cross-configuration active state and safe navigation (237ms)
✓  67 playwright/skeleton-navigation.spec.js:226:3 › Skeleton button navigation › keeps a ScrollView-anchored navigation bar pinned while its content scrolls (188ms)
✓  68 playwright/skeleton-navigation.spec.js:295:3 › Skeleton button navigation › fails closed when a navigation bar item is missing its portable label contract (161ms)
✓  69 playwright/skeleton-presentation.spec.js:37:3 › Skeleton presentation modifiers › opens, dismisses, and annotates a modal presentation (286ms)
✓  70 playwright/skeleton-real-configuration-corpus.spec.js:49:3 › Named real CellConfiguration/Skeleton corpus › renders every named checked-in skeleton artifact without generic fallback (1.1s)
✓  71 playwright/skeleton-row-wrap-parity.spec.js:28:1 › a row wraps only with wrap: true, as in the app (217ms)
✓  72 playwright/skeleton-tabs-optimistic-hold.spec.js:84:1 › naar handlingen feiler, gaar markeringen tilbake i stedet for aa bli staaende (1.1s)
✓  73 playwright/skeleton-textarea-submit.spec.js:33:3 › Skeleton TextArea submitActionKeypath › plain editor submits current text only to the dedicated action (157ms)
✓  74 playwright/skeleton-textarea-submit.spec.js:69:3 › Skeleton TextArea submitActionKeypath › rich Markdown editor honors submitActionKeypath and serialized payload (158ms)
✓  75 playwright/skeleton-visibility.spec.js:37:3 › Skeleton conditional visibility › updates element visibility from root data (175ms)
✓  76 playwright/skeleton-workbench-autoscroll.spec.js:54:3 › Skeleton workbench auto-scroll › coalesces back-to-back renders without losing bottom or reader intent (306ms)
```

## Fokuserte Swift-tester

`swift test --disable-sandbox --filter 'ConfigurationCatalog|ConferencePublicProfile|ConferenceShellConfigurationFactoryTests|ConferencePublicConfigurationPolicyTests|SkeletonElementParityMatrixTests|SkeletonPortableModelTests|ProductionSkeletonBindingIntegrityTests|SkeletonRuntimeSourceTests|SkeletonStyleParityCSSDriftTests|SkeletonRuntimeDecoderTests'`: exit 1; Executed 8 tests, with 0 failures (0 unexpected) in 0.222 (0.222) seconds

```text
FEILET SkeletonElementParityMatrixTests/testMatrixRevisionMatchesPackagePin
FEILET SkeletonElementParityMatrixTests/testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips
FEILET SkeletonRuntimeSourceTests/testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning
FEILET SkeletonRuntimeSourceTests/testRuntimeDispatchesDropTargetPayloadAndHorizontalScrollAxis
```

## CI-filteret

```text
TOTALT {'started': 2438, 'passed': 2426, 'skipped': 10, 'failed': 2}
SIGNAL 0
AVBRUTT 0
KJENT -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
KJENT -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
NYE 0
```

## T-P1 hjelpertreet

```text
  ✓  1 playwright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2) (7.0s)
  1 passed (7.3s)
```

Commit: `81b47bada14068cb9b98b015a1e7940412e302d8` på `pdd/skjelett-elementer-web` (lokal, ikke pushet). Sporede endringer etter commit: 0.
