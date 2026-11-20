# G1-GUI-bilder — Informasjonssystemer som gruppeentitet

Rendret 2026-11-18 med den ekte web-rendereren i CellScaffold (`Public/js/skeleton-runtime.js`,
`porthole-webo.css`, `admin-skeleton.css`, CellScaffold `b95f156d`) via `skeleton/render.js`.
Skjelett-JSON og tilstander ligger i `skeleton/`. Bredder: laptop 1280, iPhone 390.

| Flate | Tilstand | Filer |
|---|---|---|
| Gruppeflaten (eiere) | v1, Kjetil alene, forslag om Petter som eier venter | `gruppe-forslag-{laptop,iphone}-v1.png` |
| Gruppeflaten (eiere) | v2, to eiere, tre aktive roller og én trukket | `gruppe-eier-fylt-{laptop,iphone}-v1.png` |
| Gi rolle | utfylt, student MasterHAVEN26 | `gi-rolle-{laptop,iphone}-v1.png` |
| Mine roller (medlem) | to gyldige roller | `min-rolle-gyldig-{laptop,iphone}-v1.png` |
| Mine roller (medlem) | studentrollen trukket | `min-rolle-trukket-{laptop,iphone}-v1.png` |

## Renderingserklæring — hva bildene ikke viser

- Alle keypaths under `group.*` og `myRole.*` er forslag. Ingen finnes i CellScaffold i dag.
- Binding (SwiftUI) er ikke rendret. Paritet mot Binding er en egen test (`test.gui.parity`).
- Godkjenning med passkey/Face ID er en systemdialog og vises ikke.
- Status-teksten i en rad har én farge (grønn) også for «trukket»; skjelettet kan ikke velge farge etter verdien uten en egen rad per tilstand. Implementeringen kan gi «trukket» en egen rad med rød farge.
- Mørke felt og nedtrekkslister er rendererens standard for `TextField`/`Picker` i `view-mode` (kjent fra tidligere PDD-er).
- Navnene «Sara Nilsen», «Ola Student» og «Testkonto 3» er fiktive testdata.
