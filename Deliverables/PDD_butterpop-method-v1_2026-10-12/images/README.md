# Renderingserklæring — designutkast v1

Rendret 2026-10-12 fra `Butterpop_method/design/butterpop-v1.html`, med prosjektets `design/render-preview.cjs` og Playwright mot installert Google Chrome i headless-modus. Kilden her er en frossen referansekopi; redigerbar kilde ligger i Butterpop_method. `manifest.json` dokumenterer sjekksummer.

Dette er en HTML-mockup, ikke en Porthole- eller Binding-render og ikke en kjørende musikkeditor. Den har ingen lydfiler eller pasientopplysninger. Lokal tilstand demonstrerer visningsbytte, loopvalg, mute/solo, volum, enkel angre og eksportvalg. Flere arrangementhandlinger viser bare en forklaring av planlagt oppførsel. Ingen lagring eller eksport utføres.

## Bildesett

- Utforsk, Bygg, Studio × fylt/tom/feil: 9 bilder ved viewport1280×1050, rotflaten tatt i full høyde.
- Logic-eksportdialog: 1 bilde.
- Mobiloppsett ved viewport390×1100: 3 bilder; dette lover ikke produktstøtte for mobil lyd.
- Studio i mørk visning: 1 bilde.
- `render-check.json`: faktisk utført skissekontroll, ikke produkttester.

## Hva dagens Skeleton ikke gir her

Skeleton har generelle kontroller, tabs, grid og komponentmontering, men ingen dedikert flerspors tidslinje, klippredigerer, waveforms, synkron audio scheduler eller offline bounce. `Visualization` med en selvvalgt kind lager ikke automatisk dette; `ComponentSurface` er heller ikke bevis på en ferdig audio-plugin-adapter. Vi foreslår derfor egen webeditor i scaffoldet og generelle celler/modeller bak den. Ingen native-paritet er bekreftet.

## Senere sammenligning med produktet

WP5 skal åpne faktisk lokal scaffold-URL med Playwright/Chrome, samme viewports, theme og prosjektfixture; ta rot-/fullflatescreenshot og sammenligne side om side. Denne opptaksveien er prøvd mot HTML-skissen, men kan ikke prøves mot et scaffold som ennå ikke er implementert. Safari testes i tillegg ved produktakseptanse. Ingen G1-GUI-godkjenning er registrert.
