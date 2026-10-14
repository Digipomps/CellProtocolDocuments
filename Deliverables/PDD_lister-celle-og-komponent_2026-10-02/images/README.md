# Referansebilder — Mine lister: celle og listekomponent

Navn: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent (G1-GUI i `../STATUS.md`) teller som referanse for `test.gui.parity`.

## Dette er rendret med web-rendereren fra skjelett-JSON — ikke mockups

Hver piksel kommer fra **CellScaffolds egen skjelettrenderer** kjørt i Chromium (Playwright) på skjelett-JSON-en i `../skeleton/`
og eksempeldataene `../skeleton/state-*.json` (den formen `cell:///Lists` skal levere på `lists.state`):

| Fil fra CellScaffold `origin/main` `fdcfe7a5` | md5 |
|---|---|
| `Public/js/skeleton-runtime.js` | `62669757ccf462e998d85f3752efe35d` |
| `Public/css/porthole-webo.css` | `9370667c5d88ded9a60384dcc0565c4e` |
| `Public/js/haven-localization.js` | `e424e58703fc8b1514a29bf9ab045259` |

Harnessen er den samme som `playwright/skeleton-element-catalog.spec.js` bruker (`<main class="canvas product-view view-mode">` +
`HavenSkeletonRuntime.createRenderer({rootElement, skeleton, onAction}).update(state)`), med `setLayoutContext` som i `porthole-webo.js` 8366–8370
(capabilities `pointer, hover, keyboard, drag`; bredde = viewport − 32).

**Hva bildene beviser:** at dagens web-renderer kan vise dette skjelettet uten ett eneste `Unsupported`-element, uten umappede ikoner,
at alle synlighetsbetingelser løses i rader, at `ComponentSurface`-monteringene løses (`componentErrors: [ok, ok, ok]`), og at de fem
handlingene (trykk på sirkel, Enter i «Legg til», Enter i «Ny liste», radvalg, dra-og-slipp) sender nøyaktig de payloadene cellen skal ta
imot — se `render-report.json` → `behaviour.actions`.

**Hva bildene IKKE beviser:**

- native (SwiftUI) rendering i HAVEN-appen. Den måles ved P5. Ventede avvik: (1) knapper i rader er fylte knapper på web fordi
  `.canvas.product-view .skeleton-button` overstyrer `controlStyle: plain` (`porthole-webo.css` 4759), i appen er de ikoner;
  (2) appen viser pilene «flytt opp/ned» fordi Binding ikke erklærer `drag` (`PortholeView.swift` 72–74); web skjuler dem.
- at Porthole-serverens bootstrap faktisk leverer `lists.state` i denne formen — det er cellens kontrakt (P3/P4), ikke rendererens.
- lys modus: produktvisningen i Porthole web er mørk; appen følger systemet. Alle farger er hex med alfa der de ikke arver (B10).

## Bildene

| Fil | Flate | Tilstand | Viser | Bladformål |
|---|---|---|---|---|
| `mine-lister-web-fylt-v1.png` | «Mine lister», web 1180×820 | fylt | tre lister (Handleliste aktiv i fet), 4 åpne punkter + 2 utførte dempet i bunn med hake, «Fjern utførte», ingen piler (web har dra) | cell.lists-crud, order.done-bottom, component.plain-surface, gui.capability-not-client |
| `mine-lister-web-tom-v1.png` | web | tom | «Ny liste …»-feltet og hintet; ingen tomme bokser | component.plain-surface (lesson.empty-list-keeps-its-slot) |
| `mine-lister-web-ny-liste-v1.png` | web | ny liste | «Pakkeliste» uten punkter: tittelfelt, «Legg til …», hint i sjekklisten | cell.items-crud |
| `mine-lister-web-feil-v1.png` | web | feil | rød melding «Kunne ikke lagre siste endring …» over listen; innholdet står | cell (persistens), gui.* |
| `mine-lister-app-fylt-v1.png` | app-bredde 390×844 (web-renderer) | fylt | kolonnene stablet (`maxAvailableWidth: 700` → vertikal); samme innhold | gui.capability-not-client |
| `mine-lister-app-tom-v1.png` | app-bredde | tom | som web-tom i smal bredde | component.plain-surface |
| `vert-komponenter-web-fylt-v1.png` | eksempelvert, web | fylt | tre `ComponentSurface`-monteringer fra `my.lists.state.lists` (én per liste) i kort | component.mount |
| `vert-komponenter-app-fylt-v1.png` | eksempelvert, app-bredde | fylt | samme, smal | component.mount |

Dempet tekst på utførte punkter er `#8E8E93` via `foregroundColorKeypath: titleColor` (bare satt på utførte); åpne punkter arver flatens tekstfarge.

## WP5 — rendret fra cellens EKTE tilstand (2026-10-08)

`skeleton/state-fra-cellen.json` er `lists.state` slik `ListsCell` faktisk leverer den (skrevet av
`ListsCellTests.testPrintsRealStateForTheWebHarness` i byggejobb `l9` på Macen, kopiert hit av `wp-lister-build-test.sh`).
`render-wp5.js` rendrer samme skjelett med den, og `render-report-wp5.json` har DOM-funn, variantprøven og
oppførselen inne i en montering (handlingene bærer `mount.instanceID`).

| Fil | Viser | Pikseldiff mot referansen |
|---|---|---|
| `mine-lister-web-fra-cellen-v1.png` | «Mine lister» web fra ekte state | 0 piksler mot `mine-lister-web-fylt-v1.png` |
| `mine-lister-app-fra-cellen-v1.png` | app-bredde, uten `drag` (pilene synlige) | 0 piksler mot `mine-lister-app-fylt-v2.png` |
| `vert-komponenter-web-fra-cellen-v1.png` | tre monteringer fra `my.lists.state.lists` | 0 piksler mot `vert-komponenter-web-fylt-v1.png` |

**App-bildene har fått `-v2`:** `mine-lister-app-fylt-v2.png`, `mine-lister-app-tom-v2.png`, `vert-komponenter-app-fylt-v2.png`
er rendret med kapabilitet `touch` (som Binding på iOS), altså uten `drag`, og viser pilene «flytt opp/ned». `-v1` ble rendret med
webens kapabiliteter og skjulte dem; forskjellen er 0,913 % av pikslene, alle i pilkolonnen. Alt annet er likt. v2 er det riktige
referansebildet for appen og legges fram for G3.

## Rendre på nytt

```
cd CellProtocolDocuments/Deliverables/PDD_lister-celle-og-komponent_2026-10-02/images
python3 gen_skeleton.py            # skriver ../skeleton/*.json (OUT kan overstyres)
WEB_SRC=<mappe med de tre filene over> node render.js   # krever playwright + Chromium
```

Ny versjon av et bilde får nytt `-v<n>`; gamle beholdes til G3 er satt.
