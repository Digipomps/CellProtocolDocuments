Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

## RENDERINGSERKLÆRING

Bildene er HTML-mockups fra `prototype/`, ikke Porthole-preview av en CellConfiguration. Skjelettet for de tre flatene lages i WP-GUI. Dette kan skjelettformatet ikke rendre slik bildene viser det:

- Spillforhåndsvisningen fantes ikke i formatet før `Visualization`-typen `gamePreview` (PR #306, 2026-10-09). Den rendres i Porthole på web, men ikke i Binding (SwiftUI).
- Fargede verktøykort med ikon og lisensmerke i rutenett. Skjelettet har lister og kort, men ikke fri plassering av merker i hjørnene.
- Chat-bobler med ulik justering for barn og assistent i samme liste.
- Endringslisten («Hva endret seg») ved siden av forhåndsvisningen i én rad på smale skjermer. Skjelettet bryter den under.
