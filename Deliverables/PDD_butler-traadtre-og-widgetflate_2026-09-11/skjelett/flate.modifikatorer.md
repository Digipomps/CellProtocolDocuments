# Flate — startverdier fra mockupens CSS

Alle tabellverdier er brukt i kandidaten. Foreslåtte nye felt finnes bare i rapporten. Uniform padding bruker CSS-verdien for vertikal avstand; horisontal avstand er et dokumentert avvik, ikke en ny CSS-verdi. `fontWeight: "600"` følger CSS/web, men Binding tolker i dag navngitte vekter; dette krever rendererretting. Kilde: `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:519`, `CellScaffold/Public/js/skeleton-runtime.js:4140`, `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:33`.

| selektor | CSS-verdi | modifikatorfelt | startverdi | kilde |
|---|---|---|---|---|
| `.widget .tools button` | padding:2px 6px; bare uniform padding i dagens format | `padding` | `2` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget .tools button` | border-radius:5px; button reset border:0; inherited font:14px / muted | `cornerRadius` | `5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget .tools button` | border-radius:5px; button reset border:0; inherited font:14px / muted | `borderWidth` | `0` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget .tools button` | border-radius:5px; button reset border:0; inherited font:14px / muted | `background` | `"#ffffff"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget .tools button` | border-radius:5px; button reset border:0; inherited font:14px / muted | `fontSize` | `14` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget .tools button` | border-radius:5px; button reset border:0; inherited font:14px / muted | `foregroundColor` | `"#556273"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget .tools button` | border-radius:5px; button reset border:0; inherited font:14px / muted | `fontWeight` | `"400"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:110` |
| `.widget h3` | font-size:12.5px; color:#17212b; font-weight:600 | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:108` |
| `.widget h3` | font-size:12.5px; color:#17212b; font-weight:600 | `foregroundColor` | `"#17212b"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:108` |
| `.widget h3` | font-weight:600 | `fontWeight` | `"600"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:108` |
| `.widget > header` | padding:8px 10px; bare uniform padding i dagens format | `padding` | `8` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:107` |
| `.state i / .ok i` | 6×6px; border-radius:50%; background:#0f8a61 | `width` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .ok i` | 6×6px; border-radius:50%; background:#0f8a61 | `height` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .ok i` | 6×6px; border-radius:50%; background:#0f8a61 | `cornerRadius` | `3` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .ok i` | 6×6px; border-radius:50%; background:#0f8a61 | `background` | `"#0f8a61"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .warn i` | 6×6px; border-radius:50%; background:#ef7c2d | `width` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .warn i` | 6×6px; border-radius:50%; background:#ef7c2d | `height` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .warn i` | 6×6px; border-radius:50%; background:#ef7c2d | `cornerRadius` | `3` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .warn i` | 6×6px; border-radius:50%; background:#ef7c2d | `background` | `"#ef7c2d"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .idle i` | 6×6px; border-radius:50%; background:#b9c6d3 | `width` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .idle i` | 6×6px; border-radius:50%; background:#b9c6d3 | `height` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .idle i` | 6×6px; border-radius:50%; background:#b9c6d3 | `cornerRadius` | `3` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state i / .idle i` | 6×6px; border-radius:50%; background:#b9c6d3 | `background` | `"#b9c6d3"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:90` |
| `.state` | font-size:11px; color:#17212b | `fontSize` | `11` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:89` |
| `.state` | font-size:11px; color:#17212b | `foregroundColor` | `"#17212b"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:89` |
| `.row` | font-size:12.5px; color:#17212b | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:86` |
| `.row` | font-size:12.5px; color:#17212b | `foregroundColor` | `"#17212b"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:86` |
| `.row .m` | font-size:12.5px; color:#556273 | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:88` |
| `.row .m` | font-size:12.5px; color:#556273 | `foregroundColor` | `"#556273"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:88` |
| `.row` | padding:5px 11px; bare uniform padding i dagens format | `padding` | `5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:86` |
| `.row + .row / footer` | border-top:1px solid #eaf0f6; representert som egen linje | `height` | `1` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:87` |
| `.row + .row / footer` | border-top:1px solid #eaf0f6; representert som egen linje | `background` | `"#eaf0f6"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:87` |
| `.stat` | font-size:12.5px; color:#17212b | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:112` |
| `.stat` | font-size:12.5px; color:#17212b | `foregroundColor` | `"#17212b"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:112` |
| `.stat b` | font-size:12.5px; color:#17212b; font-weight:700 | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:114` |
| `.stat b` | font-size:12.5px; color:#17212b; font-weight:700 | `foregroundColor` | `"#17212b"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:114` |
| `.stat b` | font-weight:700 | `fontWeight` | `"700"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:114` |
| `.stat` | padding:6px 11px; bare uniform padding i dagens format | `padding` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:112` |
| `.widget footer` | font-size:11.5px; color:#556273 | `fontSize` | `11.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:111` |
| `.widget footer` | font-size:11.5px; color:#556273 | `foregroundColor` | `"#556273"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:111` |
| `.widget footer` | padding:6px 10px; bare uniform padding i dagens format | `padding` | `6` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:111` |
| `.row + .row / footer` | border-top:1px solid #d5e0eb; representert som egen linje | `height` | `1` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:87` |
| `.row + .row / footer` | border-top:1px solid #d5e0eb; representert som egen linje | `background` | `"#d5e0eb"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:87` |
| `.widget footer (feil)` | font-size:11.5px; color:#9a4a12 | `fontSize` | `11.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:209` |
| `.widget footer (feil)` | font-size:11.5px; color:#9a4a12 | `foregroundColor` | `"#9a4a12"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:209` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `borderWidth` | `1` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `borderColor` | `"#d5e0eb"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `cornerRadius` | `9` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `background` | `"#ffffff"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `shadowRadius` | `2` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `shadowX` | `0` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `shadowY` | `1` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.widget` | border:1px solid #d5e0eb; border-radius:9px; background:#fff; shadow:0 1px 2px rgba(16,32,48,.05) | `shadowColor` | `"#1020300d"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106` |
| `.rows` | padding:4px 0; approximert uniform | `padding` | `4` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:85` |
| `.placeholder` | 1.5px dashed #0f4c81; radius9; background#e8f1f9; color#0a3558; height96 | `borderWidth` | `1.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:123` |
| `.placeholder` | 1.5px dashed #0f4c81; radius9; background#e8f1f9; color#0a3558; height96 | `borderColor` | `"#0f4c81"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:123` |
| `.placeholder` | 1.5px dashed #0f4c81; radius9; background#e8f1f9; color#0a3558; height96 | `cornerRadius` | `9` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:123` |
| `.placeholder` | 1.5px dashed #0f4c81; radius9; background#e8f1f9; color#0a3558; height96 | `background` | `"#e8f1f9"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:123` |
| `.placeholder` | 1.5px dashed #0f4c81; radius9; background#e8f1f9; color#0a3558; height96 | `height` | `96` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:123` |
| `.placeholder` | font-size:12.5px; color:#0a3558 | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:124` |
| `.placeholder` | font-size:12.5px; color:#0a3558 | `foregroundColor` | `"#0a3558"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:124` |
| `.emptyhint` | min-height:180; padding16; dashed1.5 #d5e0eb; radius9 (height er fast tilnærming) | `height` | `180` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:192` |
| `.emptyhint` | min-height:180; padding16; dashed1.5 #d5e0eb; radius9 (height er fast tilnærming) | `padding` | `16` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:192` |
| `.emptyhint` | min-height:180; padding16; dashed1.5 #d5e0eb; radius9 (height er fast tilnærming) | `borderWidth` | `1.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:192` |
| `.emptyhint` | min-height:180; padding16; dashed1.5 #d5e0eb; radius9 (height er fast tilnærming) | `borderColor` | `"#d5e0eb"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:192` |
| `.emptyhint` | min-height:180; padding16; dashed1.5 #d5e0eb; radius9 (height er fast tilnærming) | `cornerRadius` | `9` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:192` |
| `.emptyhint` | font-size:12.5px; color:#556273 | `fontSize` | `12.5` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:193` |
| `.emptyhint` | font-size:12.5px; color:#556273 | `foregroundColor` | `"#556273"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:193` |
| `.canvas .body` | padding12; flex:1 (maxHeightInfinity er bare tilnærming) | `padding` | `12` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:105` |
| `.canvas .body` | padding12; flex:1 (maxHeightInfinity er bare tilnærming) | `maxHeightInfinity` | `true` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:105` |
| `.panel.canvas` | width384 fra stage:29; height1250-52-28=1170; border1 #d5e0eb; radius10; surface#fff | `width` | `384` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:31` |
| `.panel.canvas` | width384 fra stage:29; height1250-52-28=1170; border1 #d5e0eb; radius10; surface#fff | `height` | `1170` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:31` |
| `.panel.canvas` | width384 fra stage:29; height1250-52-28=1170; border1 #d5e0eb; radius10; surface#fff | `borderWidth` | `1` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:31` |
| `.panel.canvas` | width384 fra stage:29; height1250-52-28=1170; border1 #d5e0eb; radius10; surface#fff | `borderColor` | `"#d5e0eb"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:31` |
| `.panel.canvas` | width384 fra stage:29; height1250-52-28=1170; border1 #d5e0eb; radius10; surface#fff | `cornerRadius` | `10` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:31` |
| `.panel.canvas` | width384 fra stage:29; height1250-52-28=1170; border1 #d5e0eb; radius10; surface#fff | `background` | `"#ffffff"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:31` |
| `.panel h2` | font-size:13px; color:#17212b; font-weight:600 | `fontSize` | `13` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:33` |
| `.panel h2` | font-size:13px; color:#17212b; font-weight:600 | `foregroundColor` | `"#17212b"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:33` |
| `.panel h2` | font-weight:600 | `fontWeight` | `"600"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:33` |
| `.panel header .sub` | font-size:12px; color:#556273 | `fontSize` | `12` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:34` |
| `.panel header .sub` | font-size:12px; color:#556273 | `foregroundColor` | `"#556273"` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:34` |
| `.panel > header` | padding:11px 13px; bare uniform padding i dagens format | `padding` | `11` | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:32` |

`#1020300d` er nærmeste 8-bits alfa til rgba(16,32,48,.05): 13/255 ≈ .05098. Radius/blur i CSS og SwiftUI kan gi ulike piksler; verdien er et startpunkt, ikke verifisert skyggeparitet. Kilder: `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:106`, `CellScaffold/Public/js/skeleton-runtime.js:4175`, `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:727`.

Øvrig geometri for neste iterasjon:

| selektor | CSS-verdi | modifikatorfelt | startverdi |
|---|---|---|---|
| `.canvas .body` / `.widget > header` / `.tools` | gap 12 / 8 / 2 | eksisterende stack `spacing` (ikke modifier) | 12 / 8 / 2 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:105`, `:107`, `:109`) |
| `.widget .row` | minmax(0,1fr) 74px 66px; gap8 | eksisterende `Grid.columns`, `spacing` | flexible(min:0), fixed74, fixed66; 8 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:86`) |
| `[data-full="1"] .widget.w1 .row` | 1fr 120px 120px 110px; padding9 14; font13 | foreslått `layoutVariants`; `paddingInsets` | ingen fullvariant i kandidaten (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:157`) |
| `[data-full="1"] .canvas .body` | padding14 | variant av `padding` | 14 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:151`) |
| `[data-viewport="app"] .canvas .body` | row; padding10; gap10 | foreslått `layoutVariants` + `itemSpacing` | horizontal / 10 / 10 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:178`) |
| `[data-viewport="app"] .widget` | min-width236; flex0 0 236 | variant bredde / krymping | 236 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:179`) |
| `[data-viewport="app"] .widget footer` | font11; padding5 10 | variant `fontSize`, `paddingInsets` | 11; 5/10 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:177`) |
| `[data-viewport="app"] .widget .row` | 1fr 62px 62px; font12 | variant `Grid.columns`, `fontSize` | flexible, 62, 62; 12 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:185`) |
| `[data-viewport="app"] .canvas` | max-height250; under drag330 | foreslått `maxHeight` + `layoutVariants` | 250 / 330 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:175`, `:182`) |
| `[data-drag="1"] .canvas` | border#0f4c81; shadow0 0 0 2px #dbe9f5 | statevariant + foreslått `shadowSpread` | 2; eksisterende shadowRadius>0 kan ikke gi denne ringen (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:133`; `CellScaffold/Public/js/skeleton-runtime.js:4175`) |
| `.emptyhint`, `.placeholder` | dashed1.5; høyde180 minimum / høyde96 | foreslått `borderStyle`, `minHeight` | dashed; 180 / 96 (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:123`, `:193`) |
| `.panel h2`, `body`, `.stat b` | letter-spacing.2px; Avenir Next/Segoe UI/system; line-height1.45; tabular-nums | foreslått `letterSpacing`, `fontFamily`, `lineHeight`, `numericVariant` | .2; CSS-stakken;1.45;tabular (`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:15`, `:33`, `:114`) |

Kandidatens hjelpe-linjer bruker 1px høy tom VStack i stedet for Divider for å gi eksplisitt farge. Dermed unngås å anta at `Divider.background` erstatter rendererens egne border-regler. `separatorAfter` skal ha én rad unntatt på siste rad. Web-/app-listenes egne avstander kommer i tillegg og er et kjent gap: `CellScaffold/Public/css/porthole-webo.css:3025`, `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift:181`, `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift:235`.
