STATUS: LEVERT — lytterbalansen rettet, spec-ene groenne, commit dbf6667df3c2f35da9d8fb606f1e9757ec80dd5a

# Web-fiks 1 — globale drag-lyttere foelger mount

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-web-fiks1.sh` 2026-09-22T09:07:55Z. Bevis: `evidence/web-regresjon/`.

Endring: OK: Public/js/skeleton-runtime.js — drag-lytterne foelger naa mount, ikke opprettelsen.

`node --check`: OK.

```text
 Public/js/skeleton-runtime.js | 30 ++++++++++++++++++++----------
 1 file changed, 20 insertions(+), 10 deletions(-)
```

## Spec-ene fra «Admin web accessibility and responsive gates»

exit 0 — 

```text
[1A[2K[1/24] playwright/porthole-skeleton-atomic-swap.spec.js:35:1 › reordered JSON object fields preserve a document and its pending image read
[1A[2K[2/24] playwright/porthole-skeleton-atomic-swap.spec.js:91:1 › Porthole retains the rendered node when a refreshed skeleton is malformed
[1A[2K[3/24] playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners
[1A[2K[4/24] playwright/porthole-skeleton-atomic-swap.spec.js:256:1 › Porthole rejects malformed action editor state without replacing the rendered node
[1A[2K[5/24] playwright/porthole-skeleton-atomic-swap.spec.js:312:1 › Porthole exposes typed source write failure and keeps the working surface
[1A[2K[6/24] playwright/porthole-skeleton-localization.spec.js:9:1 › Porthole applies supplied locale and catalog-only refresh to its mounted skeleton
[1A[2K[7/24] playwright/rich-document.spec.js:77:1 › typing while an acknowledgement waits batches unsent edits and preserves the sent envelope
[1A[2K[8/24] playwright/rich-document.spec.js:100:1 › cancelling unsent typing emits no empty mutation and keeps the in-flight edit
[1A[2K[9/24] playwright/rich-document.spec.js:120:1 › two real Skeleton surfaces converge, preserve formatting, range comments, presence and chat
[1A[2K[10/24] playwright/rich-document.spec.js:149:1 › lost acknowledgement and unmounted draft do not lose local text
[1A[2K[11/24] playwright/rich-document.spec.js:163:1 › onboarding, embedded image/chart and downloadable Markdown PDF Word
[1A[2K[12/24] playwright/rich-document.spec.js:193:1 › large image after bidirectional typing reaches both document surfaces
[1A[2K[13/24] playwright/rich-document.spec.js:216:1 › uncertain persistence retains the draft and retries the exact command
[1A[2K[14/24] playwright/rich-document.spec.js:230:1 › writing waits for the initial current definition
[1A[2K[15/24] playwright/rich-document.spec.js:247:1 › switching document identity remounts the editor and keeps the old draft separate
[1A[2K[16/24] playwright/skeleton-localization.spec.js:36:1 › language changes update mounted labels, preserve draft/caret and make no network calls
[1A[2K[17/24] playwright/skeleton-localization.spec.js:64:1 › language changes during an action preserve payload, busy state and completion
[1A[2K[18/24] playwright/skeleton-localization.spec.js:74:1 › data updates change plural arguments and item labels, and missing values use a literal reserve
[1A[2K[19/24] playwright/skeleton-localization.spec.js:89:1 › unsupported slots are rejected before replacing the healthy surface
[1A[2K[20/24] playwright/skeleton-localization.spec.js:103:1 › 200 mounted message bindings reuse formatters on repeated language switches
[1A[2K[21/24] playwright/skeleton-localization.spec.js:130:1 › catalog revisions replace text atomically without resetting a draft
[1A[2K[22/24] playwright/skeleton-localization.spec.js:149:1 › localized arguments remain plain text even with a legacy HTML formatter
[1A[2K[23/24] playwright/skeleton-localization.spec.js:163:1 › 1000 localized list items keep scroll position and nodes
[1A[2K[24/24] playwright/skeleton-localization.spec.js:189:1 › the shared message corpus agrees in the actual browser
[1A[2K  24 passed (19.1s)
```

## Naboene (drag, presentasjon, synlighet, skjelettformat)

exit 0 — 

```text

Running 21 tests using 1 worker

[1A[2K[1/21] playwright/skeleton-atomic-render.spec.js:40:3 › Skeleton renderer atomic admission › rejects root and nested multi-key updates without touching healthy DOM
[1A[2K[2/21] playwright/skeleton-atomic-render.spec.js:85:3 › Skeleton renderer atomic admission › shows an explicit initial diagnostic and recovers with a later valid tree
[1A[2K[3/21] playwright/skeleton-atomic-render.spec.js:112:3 › Skeleton renderer atomic admission › rejects schema-invalid ZStack, Object, and Toggle payloads without replacing healthy DOM
[1A[2K[4/21] playwright/skeleton-atomic-render.spec.js:150:3 › Skeleton renderer atomic admission › deferred mount preserves visibility and presentation bindings through atomic admission
[1A[2K[5/21] playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile
[1A[2K[6/21] playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA
[1A[2K[7/21] playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data
[1A[2K[8/21] playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata
[1A[2K[9/21] playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll
[1A[2K[10/21] playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls
[1A[2K[11/21] playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate
[1A[2K[12/21] playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control
[1A[2K[13/21] playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops
[1A[2K[14/21] playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic
[1A[2K[15/21] playwright/skeleton-format-round-b.spec.js:43:3 › WP-F format round B › instanceIDKeypath: one surface per List row, own state, survives reorder
[1A[2K[16/21] playwright/skeleton-format-round-b.spec.js:66:3 › WP-F format round B › ComponentSurface needs exactly one of instanceID and instanceIDKeypath
[1A[2K[17/21] playwright/skeleton-format-round-b.spec.js:84:3 › WP-F format round B › layout variants: width at wide, hidden at narrow, switching keeps the element
[1A[2K[18/21] playwright/skeleton-format-round-b.spec.js:102:3 › WP-F format round B › a fixed width holds in a row like a native frame; the flexible neighbour wraps
[1A[2K[19/21] playwright/skeleton-presentation.spec.js:37:3 › Skeleton presentation modifiers › opens, dismisses, and annotates a modal presentation
[1A[2K[20/21] playwright/skeleton-row-wrap-parity.spec.js:28:1 › a row wraps only with wrap: true, as in the app
[1A[2K[21/21] playwright/skeleton-visibility.spec.js:37:3 › Skeleton conditional visibility › updates element visibility from root data
[1A[2K  21 passed (10.8s)
```

Commit `dbf6667df3c2f35da9d8fb606f1e9757ec80dd5a`. Ikke pushet — web-fiks 2 (skrivefeltet i vinduet) skal med i samme oppdatering av PR-en.
