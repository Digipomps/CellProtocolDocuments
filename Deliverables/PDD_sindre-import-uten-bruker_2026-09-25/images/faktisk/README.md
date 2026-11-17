# Faktiske verk-sider — AP2–AP5/AP7 runde 3

`verk-forvaltet.html` og `verk-bekreftet.html` er uendrede, anonyme HTTP-svar fra `VaporPublication`, etter import og etter overtakelse i isolert test-runtime. De er skrevet av `ManagedArtistImportTests.testPilotSeedThroughImportAndHTTPBeforeAndAfterClaim`, ikke bygget av referansens mock-data. Ingen produksjonsimport eller faktisk kunstnerovertakelse er utført.

Seed: fem utstillinger og 14 verk. 13 godkjente forhåndsvisninger er lastet inn via import-API-et; serverens bildesvar ligger under `pub/sindre-hustveit/verk/<workID>/preview`. Batikk mangler kildebilde og beholder tom rute. Alle 13 bilder ble kontrollert ferdig lastet i Chrome; 14 kort var til stede både før og etter overtakelsen. Hele HTML-responsene er identiske etter at samtykkelinjen og tilhørende tom linje er fjernet.

`verk-forvaltet.png` og `verk-bekreftet.png` er fullsidefangster ved samme 1100 CSS-pikslers bredde som referansene. `verk-forvaltet-topp.png` er et topputsnitt. Referanse-PNG-ene har 1,5× pikselratio; disse fangstene bruker 1×. Chrome arvet maskinens mørke tema, og verktøyet tilbød ingen fargepreferanse-emulering. Derfor er fangstene laget fra eksplisitte `*-lys-visning.html`-kopier hvor kun `@media (prefers-color-scheme:dark)` erstattes med `@media not all`. Dette tilsvarer lys visning av samme stylesheet. `light-view.py` viser hele transformasjonen; HTTP-originalene er bevart urørt. Ingen tekster, bilder eller layoutmål er endret for fangsten. Playwright-MCP krevde utilgjengelig approval; Chrome via CUA ble brukt i stedet.

Visuell kontroll: samme noteplassering, typografi, kolonner, kort, rekkefølge, krediteringer og nøytrale aksent som godkjent bilde. Produksjonens CSS er byte-identisk med referanse-HTML-ens CSS. Etter overtakelse er linjen borte. Bevisste dataavvik: faktisk publiseringsdato 28.09.2026 i stedet for mock-datoer, og ingen CV-lenke fordi seed ikke leverer noen CV-side. Sted og år kommer fra seed. Dette er ikke en påstand om pikselidentisk mock-innhold.

Åpne via en lokal HTTP-server med denne mappen som rot, slik at de absolutte preview-stiene virker. HTTP-rutenes før/etter/utløp-status og bildebytes er separat verifisert i XCTest; den lokale nettleservisningen serverer bare de eksporterte svarene.

Siste pilot-eksport etter UUID-avgrensningen er kjørt grønt, og begge uendrede HTTP-HTML-filer er byte-identiske med de allerede fangede sidene. PNG-ene gjelder dermed samme responsinnhold.
