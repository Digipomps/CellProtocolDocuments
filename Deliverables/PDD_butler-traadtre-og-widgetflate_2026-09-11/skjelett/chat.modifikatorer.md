# Chat — startverdier for visuell iterasjon

Kilde for alle farger og mål: `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html:7–15`, med selektorlinjene under. Dette er startverdier, ikke målte rendererresultater. Ingen modifikatoriterasjon eller preview er kjørt. Tallene er CSS-piksler på referanseflaten; SwiftUI tolker dem som punkter (`CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:702–740`).

`padding` har bare én Double (`CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:521`). Kandidaten bruker normalt CSS-verdien vertikalt på alle kanter. Det er en bevisst tilnærming: 11px 13px → 11, 8px 13px → 8, 14px 16px → 14, 8px 10px → 8, 5px 11px → 5, 1px 8px → 1, 6px 10px → 6, 9px 11px → 9, 10px 12px → 10, 12px 14px → 12. `.rows` 4px 0 blir 4; `.railview` 12px 6px blir 6. Ikke betrakt chipens form eller panelgeometrien som riktig før per-kant-padding eller ekvivalent komposisjon er prøvd.

`fontWeight` er CSS-strengen «400»/«600». Web setter denne direkte, mens appens `weightFrom` bare gjenkjenner navn og ellers bruker regular. Dette er renderer-semantikk, ikke en ny type: `CellScaffold/Public/js/skeleton-runtime.js:4140–4142`; `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:33–45`.

| selektor | CSS-verdi | modifikatorfelt | startverdi |
|---|---|---|---|
| `.row` (kilde :86) | `12.5px` | `fontSize` | `12.5` |
| `.row` (kilde :86) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.row` (kilde :86) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.row .m` (kilde :88) | `12.5px` | `fontSize` | `12.5` |
| `.row .m` (kilde :88) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.row .m` (kilde :88) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.state i` (kilde :90) | `6px` | `width` | `6` |
| `.state i` (kilde :90) | `6px` | `height` | `6` |
| `.state i` (kilde :90) | `50%` | `cornerRadius` | `3` |
| `.state i` (kilde :90) | `#0f8a61 / var(--branch-a) (:11/:65/:91)` | `background` | `"#0f8a61"` |
| `.state i` (kilde :90) | `var(--accent) = #ef7c2d (:9)` | `background` | `"#ef7c2d"` |
| `.state i` (kilde :90) | `#b9c6d3` | `background` | `"#b9c6d3"` |
| `.state` (kilde :89) | `11px` | `fontSize` | `11` |
| `.state` (kilde :89) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.state` (kilde :89) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.row` (kilde :86) | `5px 11px` | `padding` | `5` |
| `.chip` (kilde :69) | `11px` | `fontSize` | `11` |
| `.chip` (kilde :69) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.chip` (kilde :69) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.chip` (kilde :69) | `1px 8px` | `padding` | `1` |
| `.chip` (kilde :69) | `20px` | `cornerRadius` | `20` |
| `.chip` (kilde :69) | `1px` | `borderWidth` | `1` |
| `.chip` (kilde :69) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.card footer` (kilde :92) | `11.5px` | `fontSize` | `11.5` |
| `.card footer` (kilde :92) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.card footer` (kilde :92) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.card footer` (kilde :92) | `6px 10px` | `padding` | `6` |
| `.btn.p` (kilde :95) | `5px 11px (arvet .btn :94)` | `padding` | `5` |
| `.btn.p` (kilde :95) | `7px` | `cornerRadius` | `7` |
| `.btn.p` (kilde :95) | `1px` | `borderWidth` | `1` |
| `.btn.p` (kilde :95) | `var(--primary) = #0f4c81 (:9)` | `borderColor` | `"#0f4c81"` |
| `.btn.p` (kilde :95) | `var(--primary) = #0f4c81 (:9)` | `background` | `"#0f4c81"` |
| `.btn.p` (kilde :95) | `12.5px` | `fontSize` | `12.5` |
| `.btn.p` (kilde :95) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.btn.p` (kilde :95) | `var(--surface) / #fff = #ffffff (:8/:63)` | `foregroundColor` | `"#ffffff"` |
| `.btn` (kilde :94) | `5px 11px` | `padding` | `5` |
| `.btn` (kilde :94) | `7px` | `cornerRadius` | `7` |
| `.btn` (kilde :94) | `1px` | `borderWidth` | `1` |
| `.btn` (kilde :94) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.btn` (kilde :94) | `var(--surface) / #fff = #ffffff (:8/:63)` | `background` | `"#ffffff"` |
| `.btn` (kilde :94) | `12.5px` | `fontSize` | `12.5` |
| `.btn` (kilde :94) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.btn` (kilde :94) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.actions` (kilde :93) | `9px 11px` | `padding` | `9` |
| `.grip` (kilde :83) | `15px` | `fontSize` | `15` |
| `.grip` (kilde :83) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.grip` (kilde :83) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.grip` (kilde :83) | `2px 4px` | `padding` | `2` |
| `.grip` (kilde :83) | `5px` | `cornerRadius` | `5` |
| `.card h3` (kilde :79) | `12.5px` | `fontSize` | `12.5` |
| `.card h3` (kilde :79) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.card h3` (kilde :79) | `600` | `fontWeight` | `"600"` |
| `.card > header` (kilde :78) | `8px 10px` | `padding` | `8` |
| `.card > header` (kilde :78) | `var(--surface) / #fff = #ffffff (:8/:63)` | `background` | `"#ffffff"` |
| `.rows` (kilde :85) | `4px 0` | `padding` | `4` |
| `.card` (kilde :77) | `var(--surface-muted) = #f8fbfe (:8)` | `background` | `"#f8fbfe"` |
| `.card` (kilde :77) | `1px` | `borderWidth` | `1` |
| `.card` (kilde :77) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.card` (kilde :77) | `9px` | `cornerRadius` | `9` |
| `.card .tools button` (kilde :81) | `2px 6px` | `padding` | `2` |
| `.card .tools button` (kilde :81) | `5px` | `cornerRadius` | `5` |
| `.card .tools button` (kilde :81) | `12px` | `fontSize` | `12` |
| `.card .tools button` (kilde :81) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.card .tools button` (kilde :81) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.card .tools button` (kilde :81) | `var(--surface) / #fff = #ffffff (:8/:63)` | `background` | `"#ffffff"` |
| `.errline b` (kilde :207) | `12.5px` | `fontSize` | `12.5` |
| `.errline b` (kilde :207) | `#9a4a12` | `foregroundColor` | `"#9a4a12"` |
| `.errline b` (kilde :207) | `600` | `fontWeight` | `"600"` |
| `.errline` (kilde :206) | `12.5px` | `fontSize` | `12.5` |
| `.errline` (kilde :206) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.errline` (kilde :206) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.body` (kilde :15) | `12.5px` | `fontSize` | `12.5` |
| `.body` (kilde :15) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.body` (kilde :15) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.errline` (kilde :206) | `9px 11px` | `padding` | `9` |
| `.errline` (kilde :206) | `#fff7f0` | `background` | `"#fff7f0"` |
| `.errline` (kilde :206) | `1px` | `borderWidth` | `1` |
| `.errline` (kilde :206) | `#f3c9a8` | `borderColor` | `"#f3c9a8"` |
| `.errline` (kilde :206) | `9px` | `cornerRadius` | `9` |
| `.branchline::before, .branchline::after` (kilde :74) | `1px` | `height` | `1` |
| `.branchline::before, .branchline::after` (kilde :74) | `var(--border) = #d5e0eb (:9)` | `background` | `"#d5e0eb"` |
| `.branchline` (kilde :73) | `12px` | `fontSize` | `12` |
| `.branchline` (kilde :73) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.branchline` (kilde :73) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.msg .who` (kilde :63) | `11px` | `fontSize` | `11` |
| `.msg .who` (kilde :63) | `var(--surface) / #fff = #ffffff (:8/:63)` | `foregroundColor` | `"#ffffff"` |
| `.msg .who` (kilde :63) | `600` | `fontWeight` | `"600"` |
| `.msg .who` (kilde :63) | `28px` | `width` | `28` |
| `.msg .who` (kilde :63) | `28px` | `height` | `28` |
| `.msg .who` (kilde :63) | `50%` | `cornerRadius` | `14` |
| `.msg .who` (kilde :63) | `var(--primary) = #0f4c81 (:9)` | `background` | `"#0f4c81"` |
| `.msg .who` (kilde :63) | `#0f8a61 / var(--branch-a) (:11/:65/:91)` | `background` | `"#0f8a61"` |
| `.msg .who` (kilde :63) | `var(--accent) = #ef7c2d (:9)` | `background` | `"#ef7c2d"` |
| `.msg .name` (kilde :67) | `13px` | `fontSize` | `13` |
| `.msg .name` (kilde :67) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.msg .name` (kilde :67) | `600` | `fontWeight` | `"600"` |
| `.msg .time` (kilde :68) | `11px` | `fontSize` | `11` |
| `.msg .time` (kilde :68) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.msg .time` (kilde :68) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.state i` (kilde :90) | `var(--branch-b) = #7a4fbf (:11)` | `background` | `"#7a4fbf"` |
| `.body` (kilde :15) | `14px` | `fontSize` | `14` |
| `.starter h4` (kilde :196) | `11.5px` | `fontSize` | `11.5` |
| `.starter h4` (kilde :196) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.starter h4` (kilde :196) | `600` | `fontWeight` | `"600"` |
| `.starter .row` (kilde :197) | `12.5px` | `fontSize` | `12.5` |
| `.starter .row` (kilde :197) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.starter .row` (kilde :197) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.starter .row span:last-child` (kilde :199) | `12px` | `fontSize` | `12` |
| `.starter .row span:last-child` (kilde :199) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.starter .row span:last-child` (kilde :199) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.starter .row` (kilde :197) | `7px 0` | `padding` | `7` |
| `.starter` (kilde :195) | `12px 14px` | `padding` | `12` |
| `.starter` (kilde :195) | `1px` | `borderWidth` | `1` |
| `.starter` (kilde :195) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.starter` (kilde :195) | `9px` | `cornerRadius` | `9` |
| `.starter` (kilde :195) | `var(--surface-muted) = #f8fbfe (:8)` | `background` | `"#f8fbfe"` |
| `.composer .box` (kilde :100) | `9px 11px` | `padding` | `9` |
| `.composer .box` (kilde :100) | `1px` | `borderWidth` | `1` |
| `.composer .box` (kilde :100) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.composer .box` (kilde :100) | `9px` | `cornerRadius` | `9` |
| `.composer .box` (kilde :100) | `var(--surface-muted) = #f8fbfe (:8)` | `background` | `"#f8fbfe"` |
| `.composer .box` (kilde :100) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.composer .box` (kilde :100) | `14px` | `fontSize` | `14` |
| `.composer .box` (kilde :100) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.composer .hint` (kilde :101) | `11.5px` | `fontSize` | `11.5` |
| `.composer .hint` (kilde :101) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.composer .hint` (kilde :101) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `5px 11px (arvet .btn :94)` | `padding` | `5` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `1px` | `borderWidth` | `1` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `var(--primary) = #0f4c81 (:9)` | `borderColor` | `"#0f4c81"` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `7px` | `cornerRadius` | `7` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `var(--primary) = #0f4c81 (:9)` | `background` | `"#0f4c81"` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `var(--surface) / #fff = #ffffff (:8/:63)` | `foregroundColor` | `"#ffffff"` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `12.5px` | `fontSize` | `12.5` |
| `.btn.p (tilgjengelig sendeknapp fra fabrikken)` (kilde :95) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.composer` (kilde :99) | `10px 12px` | `padding` | `10` |
| `.composer` (kilde :99) | `var(--surface) / #fff = #ffffff (:8/:63)` | `background` | `"#ffffff"` |
| `.panel h2` (kilde :33) | `13px` | `fontSize` | `13` |
| `.panel h2` (kilde :33) | `var(--text) = #17212b (:8)` | `foregroundColor` | `"#17212b"` |
| `.panel h2` (kilde :33) | `600` | `fontWeight` | `"600"` |
| `.panel header .sub` (kilde :34) | `12px` | `fontSize` | `12` |
| `.panel header .sub` (kilde :34) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.panel header .sub` (kilde :34) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.panel > header` (kilde :32) | `11px 13px` | `padding` | `11` |
| `.scope-line` (kilde :60) | `12px` | `fontSize` | `12` |
| `.scope-line` (kilde :60) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.scope-line` (kilde :60) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.scope-line` (kilde :60) | `8px 13px` | `padding` | `8` |
| `.scope-line` (kilde :60) | `var(--surface-muted) = #f8fbfe (:8)` | `background` | `"#f8fbfe"` |
| `.msgs` (kilde :61) | `14px 16px` | `padding` | `14` |
| `.panel.chat` (kilde :31) | `var(--surface) / #fff = #ffffff (:8/:63)` | `background` | `"#ffffff"` |
| `.panel.chat` (kilde :31) | `1px` | `borderWidth` | `1` |
| `.panel.chat` (kilde :31) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.panel.chat` (kilde :31) | `10px` | `cornerRadius` | `10` |
| `.railview .pill` (kilde :149) | `12px` | `fontSize` | `12` |
| `.railview .pill` (kilde :149) | `var(--primary) = #0f4c81 (:9)` | `foregroundColor` | `"#0f4c81"` |
| `.railview .pill` (kilde :149) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.railview` (kilde :148) | `11px` | `fontSize` | `11` |
| `.railview` (kilde :148) | `var(--muted) = #556273 (:8)` | `foregroundColor` | `"#556273"` |
| `.railview` (kilde :148) | `normal = 400 (arvet body/button :15–16)` | `fontWeight` | `"400"` |
| `.railview` (kilde :148) | `12px 6px` | `padding` | `6` |
| `.railview` (kilde :148) | `76px` | `width` | `76` |
| `.railview` (kilde :148) | `var(--surface) / #fff = #ffffff (:8/:63)` | `background` | `"#ffffff"` |
| `.railview` (kilde :148) | `1px` | `borderWidth` | `1` |
| `.railview` (kilde :148) | `var(--border) = #d5e0eb (:9)` | `borderColor` | `"#d5e0eb"` |
| `.railview` (kilde :148) | `10px` | `cornerRadius` | `10` |

## Presiseringer av avledede verdier og manglende felter

- `cornerRadius:14` for 28×28-avatar og `3` for 6×6-prikk er 50 % fra CSS :63 og :90; dette er avledning, ikke frie designvalg. Prikker er tomme `VStack` med fast bakgrunn, ikke et fonttegn. Fonttegnet «●» ville hatt fontavhengig diameter og baseline.
- `.railview`-kandidatens `width:76`, hvit flate, kant og radius 10 kommer fra panel/scene :31 og :144, ikke fra :148. Tittelen er foreløpig horisontal; ingen rotasjonsmodifikator finnes.
- `.errline` bruker `.btn`-utseendet for de to handlingene som en synlig tilnærming. Den faktiske referansen bruker nettleserlenker med understrek (:294), ikke knapper. CSS :16 gir knappene normal vekt; `.btn.p` arver størrelse, radius og padding fra :94.
- `.grip` bruker radius 5 og vertikal padding 2 fra :83; bokstavavstand −2px og hover :84 kan ikke uttrykkes. Dra-egenskaper er eksisterende metadatafelter, ikke CSS-verdier.
- Kandidatens `.branchline`-linjer bruker `Divider` med høyde 1 og bakgrunn #d5e0eb (:74). Webs `hr` har egen margin og native Divider har egen tegning; standardkanten kan derfor gi feil farge/tykkelse. Erstatt med/iterer en tom stack hvis målingen viser det. Linjene i kandidatens grenmarkør er ikke brukt som generelle panelkanter.
- CSS-arv er skrevet eksplisitt på tekst/knapper siden appens generelle containermodifikator ikke setter tekstfont/farge (:702–760 i native SkeletonView). `hAlignment`, `vAlignment`, `maxWidthInfinity`, `maxHeightInfinity`, `wrap`, `visibility`, dra-felter og `styleRole` er strukturelle valg, ikke påståtte CSS-mål. `chat-gap-*` er kun inspeksjonsnavn, uten nye CSS-regler.
- Avstander i stackene: header 8 (:32), scope 10 (:60), meldinger 14 (:61), avatar→innhold 10 (:62), head 8 og head→body 2 (:66), chip/prikk 5 (:69/:89), kortheader 8 (:78), verktøy 2 (:80), row 8 (:86), footer/handlinger 8 (:92–93), hint 6 over/8 mellom (:101), rail 12 (:148), starter 8 (:196). Kandidatens meldings-VStack bruker 2 også mellom body og kort; CSS krever separat margin-top 8 (:77), et dokumentert avvik.
- `.row` bruker `Grid.columns = flexible(min:0), fixed(74), fixed(66)` og spacing 8 fra :86. Det er elementfelter, ikke modifikatorer. Appreferansen bruker 62/62 og 12px tekst (:185); kandidaten beholder web-startverdiene. Tre kolonner skal ikke erstattes med tre fleksible kolonner.
- Dragtilstanden krever kortopacity .42 (:96), meldingsliste .82 og composer .5 (:134–135). Disse settes ikke statisk i kandidaten. Effektiv opasitet for kildekortet er .42 × .82 = .3444. Ghostens geometri :138–141 er rendererarbeid.
- Fontfamilie `Avenir Next, Segoe UI, system-ui, sans-serif`, line-height 1.45 (:15), headertracking .2px (:33), startertracking .03em og uppercase (:196) og vertikal railtittel (:149) mangler komplette portable kontrakter. Starteroverskriften er skrevet med store bokstaver; det erstatter ikke et generelt textTransform-felt.

Første målepass: fastslå faktisk font og samme innholdsflate; rett listekontekst, listeskall og scrollfordeling; mål så tekst/baseline, padding, border og radbredder. Juster ett dokumentert felt om gangen, med samme JSON og samme data begge steder. Ikke godkjenn pixel-likhet fra denne starttabellen.
