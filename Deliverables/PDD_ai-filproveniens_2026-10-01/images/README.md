# GUI-referanse til G1-GUI — ikke godkjent ennå

2026-10-02. Bilder fra faktisk Porthole skeleton-runtime.js og Workbench CSS på lokal origin/main fdcfe7a566ae4e73febbba464edb190e9e9cea08, med eksplisitt lokale fixtures. Ingen runtime-, MCP- eller graph-writes. Se ../sources.json for kildeblobber, ../candidate.skeleton.json for skjelett og ../render-result.json for kontroller.

- oversikt-filled-dark-v1.png / oversikt-filled-light-v1.png: fylt liste, filtre og detaljer.
- oversikt-empty-dark-v1.png / oversikt-empty-light-v1.png: ingen registrerte artefakter.
- oversikt-error-dark-v1.png / oversikt-error-light-v1.png: manglende forbindelse/ferskhet hindrer ryddegrunnlag.
- relasjoner-dark-v1.png: relasjonsliste og navigasjon tilbake til artefakten.
- bevaring-dark-v1.png: forklaring på bevaring og ukjent opphav.
- oversikt-filled-mobile-v1.png / detaljer-mobile-v1.png: 390 px, to faktisk synlige utsnitt.

Renderingserklæring: Text, HStack, VStack, Section, List, Picker, Button og Tabs finnes i dagens skjelettmodell. Ingen nye elementtyper eller produkt-CSS ble skrevet. Den lille topplinjen er kun for designgjennomgang. Den innlagte fixture-handleren støtter navigasjon/filter/detalj i forhåndsvisningen; preview.* finnes ikke som live Explore-kontrakt. Produktintegrasjon og native Binding-paritet er ikke verifisert. Vi hevder ikke at automatisk sporing, grafimport eller rydding er levert.

Eksisterende nettverksrenderer har avvik mellom SVG-linjer og HTML-noder i brede flater; se ../evidence/network-before.png. Relasjonslisten er grunnlaget for denne godkjenningen. Grafisk nettverksvisning skal verifiseres etter retting før den vises som korrekt.

Kjøring: render-review.cjs bruker tilgjengelig installert Chrome via Playwright i en separat midlertidig profil. Alle forespørsler oppfylles fra denne mappen; ingen data sendes til internett. Den skriver kun egne bilder og resultatfiler. En fullPage-mobilfangst ga feil stitching; endelige mobilbilder er viewport-fangster, med egen kontroll for horisontal overflow og tilgjengelige detaljer.
