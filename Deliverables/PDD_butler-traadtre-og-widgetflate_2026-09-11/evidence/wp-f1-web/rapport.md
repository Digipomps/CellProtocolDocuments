Utgangspunkt: CellScaffold `pdd/skjelett-elementer-web` @ `4d6a0ac226f1dc554c909b77d977a871b5b269a8` (WP-B5), CellProtocol `1b92d01a030bac424e5172c875753a1dcfe41752` (bygger på WP-F1 `6ce8252a4283d4c9379aa04467d9f7e94412882b`).

Endring: OK: WP-F web lagt paa (2 filer); ny spec `playwright/skeleton-format-round-b.spec.js`, ny test `Tests/AppTests/SkeletonFormatRoundBRuntimeTests.swift` (i CI-filteret). Diff: `evidence/wp-f1-web/change.patch`.

## Web (uten server)

Node-kontrakt: exit 0 — # pass 11 # fail 0 
Playwright (ett nytt forsøk per test): exit 1 —   2 failed   72 passed (42.1s) 

```text
FEILET porthole-skeleton-atomic-swap.spec.js:176 Porthole rejects an uncommitted renderer without activating global listeners
FEILET skeleton-map-renderer.spec.js:61 renders geospatial features and dispatches feature payload
```

```text
✓   1 playwright/admin-web.spec.js:9:1 › admin catalog preserves filter focus and loads the control plane with mutation protection (518ms)
✓   2 playwright/admin-web.spec.js:76:1 › local usage-quota admin confirms and locks mutations while preserving human-readable context (847ms)
✓   3 playwright/admin-web.spec.js:158:1 › admin skeleton semantics remain labelled and responsive on a narrow viewport (254ms)
✓   4 playwright/butler-chat-starter.spec.js:158:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › tom samtale viser startforslag, ikke en tom rute (978ms)
✓   5 playwright/butler-chat-starter.spec.js:184:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag holder seg lesbart på mobilbredde (840ms)
✓   6 playwright/butler-chat-starter.spec.js:209:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag forsvinner når samtalen er i gang, og Butler-svaret får egen stil (596ms)
✓   7 playwright/porthole-skeleton-atomic-swap.spec.js:35:1 › reordered JSON object fields preserve a document and its pending image read (172ms)
✓   8 playwright/porthole-skeleton-atomic-swap.spec.js:91:1 › Porthole retains the rendered node when a refreshed skeleton is malformed (245ms)
✘   9 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (225ms)
✘  10 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (retry #1) (199ms)
✓  11 playwright/porthole-skeleton-atomic-swap.spec.js:256:1 › Porthole rejects malformed action editor state without replacing the rendered node (494ms)
✓  12 playwright/porthole-skeleton-atomic-swap.spec.js:312:1 › Porthole exposes typed source write failure and keeps the working surface (348ms)
✓  13 playwright/porthole-skeleton-localization.spec.js:9:1 › Porthole applies supplied locale and catalog-only refresh to its mounted skeleton (407ms)
✓  14 playwright/rich-document.spec.js:77:1 › typing while an acknowledgement waits batches unsent edits and preserves the sent envelope (547ms)
✓  15 playwright/rich-document.spec.js:100:1 › cancelling unsent typing emits no empty mutation and keeps the in-flight edit (583ms)
✓  16 playwright/rich-document.spec.js:120:1 › two real Skeleton surfaces converge, preserve formatting, range comments, presence and chat (3.2s)
✓  17 playwright/rich-document.spec.js:149:1 › lost acknowledgement and unmounted draft do not lose local text (409ms)
✓  18 playwright/rich-document.spec.js:163:1 › onboarding, embedded image/chart and downloadable Markdown PDF Word (2.0s)
✓  19 playwright/rich-document.spec.js:193:1 › large image after bidirectional typing reaches both document surfaces (2.3s)
✓  20 playwright/rich-document.spec.js:216:1 › uncertain persistence retains the draft and retries the exact command (3.3s)
✓  21 playwright/rich-document.spec.js:230:1 › writing waits for the initial current definition (796ms)
✓  22 playwright/rich-document.spec.js:247:1 › switching document identity remounts the editor and keeps the old draft separate (422ms)
✓  23 playwright/skeleton-atomic-render.spec.js:40:3 › Skeleton renderer atomic admission › rejects root and nested multi-key updates without touching healthy DOM (176ms)
✓  24 playwright/skeleton-atomic-render.spec.js:85:3 › Skeleton renderer atomic admission › shows an explicit initial diagnostic and recovers with a later valid tree (184ms)
✓  25 playwright/skeleton-atomic-render.spec.js:112:3 › Skeleton renderer atomic admission › rejects schema-invalid ZStack, Object, and Toggle payloads without replacing healthy DOM (174ms)
✓  26 playwright/skeleton-atomic-render.spec.js:150:3 › Skeleton renderer atomic admission › deferred mount preserves visibility and presentation bindings through atomic admission (258ms)
✓  27 playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile (1.6s)
✓  28 playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA (434ms)
✓  29 playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data (394ms)
✓  30 playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata (561ms)
✓  31 playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll (252ms)
✓  32 playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls (515ms)
✓  33 playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate (152ms)
✓  34 playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control (912ms)
✓  35 playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops (792ms)
✓  36 playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic (706ms)
✓  37 playwright/skeleton-format-round-b.spec.js:43:3 › WP-F format round B › instanceIDKeypath: one surface per List row, own state, survives reorder (475ms)
✓  38 playwright/skeleton-format-round-b.spec.js:66:3 › WP-F format round B › ComponentSurface needs exactly one of instanceID and instanceIDKeypath (270ms)
✓  39 playwright/skeleton-format-round-b.spec.js:84:3 › WP-F format round B › layout variants: width at wide, hidden at narrow, switching keeps the element (158ms)
✓  40 playwright/skeleton-format-round-b.spec.js:102:3 › WP-F format round B › a fixed width holds in a row like a native frame; the flexible neighbour wraps (224ms)
✓  41 playwright/skeleton-list-follow-tail.spec.js:60:3 › Skeleton list followTail › follows the newest row in a plain overflow container (no styleRole needed) (408ms)
✓  42 playwright/skeleton-list-follow-tail.spec.js:70:3 › Skeleton list followTail › leaves a reader who scrolled up where they were (791ms)
✓  43 playwright/skeleton-list-follow-tail.spec.js:80:3 › Skeleton list followTail › a list without followTail does not scroll on its own (476ms)
✓  44 playwright/skeleton-list-tree.spec.js:86:3 › Skeleton list tree (childrenKeypath) › starts fully expanded when no expandedStateKeypath is given, with depth per row (191ms)
✓  45 playwright/skeleton-list-tree.spec.js:97:3 › Skeleton list tree (childrenKeypath) › seeds expansion from state and collapses/expands locally without dispatching an action (396ms)
✓  46 playwright/skeleton-list-tree.spec.js:114:3 › Skeleton list tree (childrenKeypath) › selection follows the row identity when the tree is re-flattened (355ms)
✓  47 playwright/skeleton-list-tree.spec.js:133:3 › Skeleton list tree (childrenKeypath) › a plain list without childrenKeypath renders exactly as before (186ms)
✓  48 playwright/skeleton-localization.spec.js:36:1 › language changes update mounted labels, preserve draft/caret and make no network calls (194ms)
✓  49 playwright/skeleton-localization.spec.js:64:1 › language changes during an action preserve payload, busy state and completion (513ms)
✓  50 playwright/skeleton-localization.spec.js:74:1 › data updates change plural arguments and item labels, and missing values use a literal reserve (158ms)
✓  51 playwright/skeleton-localization.spec.js:89:1 › unsupported slots are rejected before replacing the healthy surface (220ms)
✓  52 playwright/skeleton-localization.spec.js:103:1 › 200 mounted message bindings reuse formatters on repeated language switches (183ms)
✓  53 playwright/skeleton-localization.spec.js:130:1 › catalog revisions replace text atomically without resetting a draft (267ms)
✓  54 playwright/skeleton-localization.spec.js:149:1 › localized arguments remain plain text even with a legacy HTML formatter (152ms)
✓  55 playwright/skeleton-localization.spec.js:163:1 › 1000 localized list items keep scroll position and nodes (461ms)
✓  56 playwright/skeleton-localization.spec.js:189:1 › the shared message corpus agrees in the actual browser (218ms)
✘  57 playwright/skeleton-map-renderer.spec.js:61:3 › Skeleton map visualization renderer › renders geospatial features and dispatches feature payload (285ms)
✘  58 playwright/skeleton-map-renderer.spec.js:61:3 › Skeleton map visualization renderer › renders geospatial features and dispatches feature payload (retry #1) (227ms)
✓  59 playwright/skeleton-native-parity.spec.js:53:3 › WP-B4 web/native layout parity › Spacer takes the free space; a Spacer with width stays fixed (273ms)
✓  60 playwright/skeleton-native-parity.spec.js:70:3 › WP-B4 web/native layout parity › stacks fill a column; their own alignment places content, not the stack (307ms)
✓  61 playwright/skeleton-native-parity.spec.js:93:3 › WP-B4 web/native layout parity › maxWidthInfinity fills a column, maxHeightInfinity fills a row, also after a layout variant flips the axis (317ms)
✓  62 playwright/skeleton-native-parity.spec.js:117:3 › WP-B4 web/native layout parity › TextArea modifiers form one box; the field inside has no border of its own (236ms)
✓  63 playwright/skeleton-native-parity.spec.js:138:3 › WP-B4 web/native layout parity › skeleton colors win over the product-view chat log colors (237ms)
✓  64 playwright/skeleton-navigation.spec.js:47:3 › Skeleton button navigation › renders a safe relative URL as a link and never dispatches a cell action (437ms)
✓  65 playwright/skeleton-navigation.spec.js:78:3 › Skeleton button navigation › rejects unsafe navigation and preserves non-empty keypath actions (446ms)
✓  66 playwright/skeleton-navigation.spec.js:127:3 › Skeleton button navigation › anchors the first VStack navigation bar, tracks active state, and single-flights its action (195ms)
✓  67 playwright/skeleton-navigation.spec.js:194:3 › Skeleton button navigation › uses the exact configuration name for cross-configuration active state and safe navigation (371ms)
✓  68 playwright/skeleton-navigation.spec.js:226:3 › Skeleton button navigation › keeps a ScrollView-anchored navigation bar pinned while its content scrolls (193ms)
✓  69 playwright/skeleton-navigation.spec.js:295:3 › Skeleton button navigation › fails closed when a navigation bar item is missing its portable label contract (238ms)
✓  70 playwright/skeleton-presentation.spec.js:37:3 › Skeleton presentation modifiers › opens, dismisses, and annotates a modal presentation (225ms)
✓  71 playwright/skeleton-real-configuration-corpus.spec.js:49:3 › Named real CellConfiguration/Skeleton corpus › renders every named checked-in skeleton artifact without generic fallback (1.3s)
✓  72 playwright/skeleton-tabs-optimistic-hold.spec.js:84:1 › naar handlingen feiler, gaar markeringen tilbake i stedet for aa bli staaende (1.0s)
✓  73 playwright/skeleton-textarea-submit.spec.js:33:3 › Skeleton TextArea submitActionKeypath › plain editor submits current text only to the dedicated action (194ms)
✓  74 playwright/skeleton-textarea-submit.spec.js:69:3 › Skeleton TextArea submitActionKeypath › rich Markdown editor honors submitActionKeypath and serialized payload (192ms)
✓  75 playwright/skeleton-visibility.spec.js:37:3 › Skeleton conditional visibility › updates element visibility from root data (151ms)
✓  76 playwright/skeleton-workbench-autoscroll.spec.js:54:3 › Skeleton workbench auto-scroll › coalesces back-to-back renders without losing bottom or reader intent (451ms)
```

Kontroll uten endringen (samme maskin) for specer som feilet:

```text
FEILET skeleton-map-renderer.spec.js:61 renders geospatial features and dispatches feature payload
```

## Fokuserte Swift-tester

`swift test --disable-sandbox --filter 'SkeletonFormatRoundBRuntimeTests|SkeletonRuntimeDecoderTests|SkeletonRuntimeSourceTests|SkeletonStyleParityCSSDriftTests|ButlerChatSkeletonDumpTests|SkeletonElementParityMatrixTests|ConferencePublicConfigurationPolicyTests|ProductionSkeletonBindingIntegrityTests|PersonalCopilotHelperTree|PersonalCopilotWorkbench|PersonalCopilotWidgetCanvasTests'`: exit 1; Executed 9 tests, with 0 failures (0 unexpected) in 0.744 (0.744) seconds

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
  ✓  1 playwright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2) (7.5s)
  1 passed (7.9s)
```

Commit: `055b34385a34663ce2075572498cd9e504fa71c7` på `pdd/skjelett-elementer-web` (lokal, ikke pushet). Sporede endringer etter commit: 0.
