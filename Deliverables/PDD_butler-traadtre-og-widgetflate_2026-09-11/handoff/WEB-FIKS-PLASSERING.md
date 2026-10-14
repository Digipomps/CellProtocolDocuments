STATUS: LEVERT — skrivefeltet ligger inne i vinduet, spec-ene groenne, commit 07521356ef916fe85512ba7344182aff2c5669e4

# Web-fiks 2 — skrivefeltet inne i vinduet

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-web-fiks2.sh` 2026-09-22T09:59:52Z. Bevis: `evidence/web-regresjon/plassering/`.

Endring: OK: Public/css/porthole-webo.css — skallet bindes til vindushoeyden naar arbeidsflaten vises.

Endring: OK: playwright/butler-explicit-helper-placement.spec.js — tre-delen foelger arbeidsflaten. `node --check`: OK.

```text
 Public/css/porthole-webo.css                       | 10 ++++++
 .../butler-explicit-helper-placement.spec.js       | 41 ++++++++++++++++------
 2 files changed, 41 insertions(+), 10 deletions(-)
```

## `butler-explicit-helper-placement.spec.js` med rammen paa

exit 0 — 

```text

Running 3 tests using 1 worker

[1A[2K[1/3] playwright/butler-explicit-helper-placement.spec.js:16:5 › Butler explicit helper placement › desktop keeps the response in chat until the user opens one helper
[1A[2K[2/3] playwright/butler-explicit-helper-placement.spec.js:16:5 › Butler explicit helper placement › mobile-375 keeps the response in chat until the user opens one helper
[1A[2K[3/3] playwright/butler-explicit-helper-placement.spec.js:138:1 › unapproved external model is selectable and blocked without consent
[1A[2K  3 passed (22.6s)
```

## Naboene paa samme flate

exit 0 — 

```text

Running 4 tests using 1 worker

[1A[2K[1/4] playwright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2)
[1A[2Kplaywright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2)
T-P1-MAALING {"baseURL":"http://127.0.0.1:9391","rootRows":2,"rootClarificationCards":1,"rootHelpLines":1,"rootInitiallyExpanded":false,"childCount":16,"childID":"helper-invite","childComposerTarget":"skriver til: Inviter","childRows":0,"childClarificationCards":0,"childHelpLines":0,"rootRowsAfterReturn":2,"childrenAfterCollapse":0}

[1A[2K[2/4] playwright/chat-conversation-layout.spec.js:54:3 › Butler Chat-seksjonens layout › docken holder seg innenfor seksjonen naar alle kortene er synlige
[1A[2K[3/4] playwright/chat-conversation-layout.spec.js:65:3 › Butler Chat-seksjonens layout › loggen ruller i seg selv og kan naa siste melding
[1A[2K[4/4] playwright/skeleton-workbench-autoscroll.spec.js:54:3 › Skeleton workbench auto-scroll › coalesces back-to-back renders without losing bottom or reader intent
[1A[2K  4 passed (7.5s)
```

## Mobil-chatten (kjent roed i denne runden)

Med rammen: exit 1 — 

Uten rammen: exit 1 — 

Roed baade med og uten rammen — altsaa brutt tidligere i runden av den stablede
arbeidsflaten, ikke av denne rettelsen. Foert opp som kjent mangel under appbredden.

Commit `07521356ef916fe85512ba7344182aff2c5669e4`.
