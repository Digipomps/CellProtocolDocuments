# T-F3 web — katalogspeccen kjørt utenfor Codex-sandkassen
STATUS: GRØNN — alle testene i katalogspeccen bestod (exit 0)

- Kjørt: 2026-09-19T05:25:13Z
- Worktree: CellScaffold/_wt-skjellettelementer-web-20260919
- HEAD: 943a3bce6ff8bbaa9a0e3884fecf78915fd1e8c5
- Gren: pdd/skjelett-elementer-web
- Kommando: ./node_modules/.bin/playwright test --config=playwright.config.js playwright/skeleton-element-catalog.spec.js --reporter=list
- Exit: 0
- Full logg: CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/evidence/wp-r2-web/t-f3-20260919T0525Z/playwright.log

## Resultat per test
```
  ✓   1 playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile (1.8s)
  ✓   2 playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA (319ms)
  ✓   3 playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data (270ms)
  ✓   4 playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata (620ms)
  ✓   5 playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll (350ms)
  ✓   6 playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls (401ms)
  ✓   7 playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate (192ms)
  ✓   8 playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control (830ms)
  ✓   9 playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops (710ms)
  ✓  10 playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic (921ms)
  10 passed (6.9s)
```

## Siste 40 linjer av loggen
```

Running 10 tests using 1 worker

  ✓   1 playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile (1.8s)
  ✓   2 playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA (319ms)
  ✓   3 playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data (270ms)
  ✓   4 playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata (620ms)
  ✓   5 playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll (350ms)
  ✓   6 playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls (401ms)
  ✓   7 playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate (192ms)
  ✓   8 playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control (830ms)
  ✓   9 playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops (710ms)
  ✓  10 playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic (921ms)

  10 passed (6.9s)
```
