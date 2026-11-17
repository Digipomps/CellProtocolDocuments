Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

## RENDERINGSERKLÆRING

- `artikkel-tolkning-v1.png` er en HTML-mockup. Den er ikke rendret av Binding eller Porthole, fordi PalazzoScaffold ikke har noen Porthole-vert (lesson.scaffold-without-porthole-host-has-no-preview). Godkjent 2026-09-26, variant B.
- Det dagens skjelett ikke kan rendre som i bildet:
  - brikkene i åpen rad. De blir én innrykket barnerad med tekst som brytes (avvik 1 i FORMAALSSPEC §3);
  - den lukkede raden i native. `List.childrenKeypath` er ikke implementert i CellApple, så dette leveres av formål A1.
- `vektjustering-forklart-v1.png` er en forklaringsfigur, ikke en flate. Tallene i den er et eksempel.
- `actual/porthole-brikker-spike-*.png` er en strukturprøve fra 2026-09-28, rendret av Porthole-rendereren (`CellScaffold::Public/js/skeleton-runtime.js`, origin/main `adf48d46`) med husets stilark. Skriptet er `actual/porthole-brikker-spike.py`. S2 er valgt. Prøven er ikke native og ikke en akseptanse.
- `plan-v1.png` er en planfigur, ikke en flate.
