# Bilder til G1-GUI — dele dokumenter (v1, 15.11.2026)

Rendret med den ekte web-rendereren i CellScaffold `8e8f8e0` (`Public/js/skeleton-runtime.js`, `Public/css/porthole-webo.css`, Quill) i Playwright/Chromium. Skeleton-JSON og testdata står i `../skeleton/render.js`. Kjør på nytt med `node skeleton/render.js <CellScaffold>/Public images`.

Hva som er ekte og hva som er tegnet:
- Ekte: rendereren, alle elementtyper (VStack, HStack, Text, Button, List, Picker) og dokumenteditoren (`richDocument`-visualiseringen).
- Tegnet: dataene (navn, datoer, roller) og keypathene `documents.*` og `share.*`. Cellene som skal svare på dem finnes ikke ennå.
- Alle flatene utenom editoren er vanlige skeleton-elementer, så de skal kunne tegnes i Binding (Swift). Binding er ikke rendret her (ingen Swift i skycontaineren); det skjer i P5.

| Fil | Flate og tilstand |
|---|---|
| `dokumenter-fylt-{laptop,iphone}-v1.png` | «Dokumenter» med invitasjon, egne dokumenter og delt med meg |
| `dokumenter-tom-{laptop,iphone}-v1.png` | «Dokumenter» for en ny student |
| `inviter-{laptop,iphone}-v1.png` | Et dokument med panelet «Del dokumentet» (person, rolle, deltakere, Fjern) |
| `invitasjon-{laptop,iphone}-v1.png` | Det den inviterte ser når invitasjonen åpnes |
| `ingen-tilgang-{laptop,iphone}-v1.png` | Det en som ikke er invitert ser |

Kjent avvik i dagens renderer: etikettene på Picker («Person», «Rolle») er svært svake, og på smal skjerm blir nedtrekkslistene mørke. Det er rendererens standard, ikke noe tegnet. Det bør rettes eller godtas før G3.
