# Renderingsdeklarasjon

Dette er en lokal HTML/CSS/SVG-designkandidat, ikke en eksportert CellConfiguration og ikke et skjermbilde av ny funksjonalitet på staging.
Kilden er `../preview/index.html`, `app.css` og `app.js`. Ingen fetch, WebSocket, lagring, modellkall eller jobb-API inngår. Alle verdier og tider i kandidaten er syntetiske og merket i hele rammen.

Hvorfor HTML: dagens network-renderer har klikk/pan/zoom, men hardkodet mørk palett og gjenskaper nodene ved fokusskifte. Kontrakten for jevn fokusovergang og den sammensatte, autoriserte prosjektprojeksjonen finnes ikke i den leste koden. Dashboardkomponenter kan i hovedsak beskrives med eksisterende Skeleton tabs/liste/detalj/Visualization; domenebindinger/Explore og native renderer må kontrolleres og implementeres etter gate. Ingen nye Skeleton-felter antas støttet.

Ingenting er skjult eller beskåret fra en eksisterende levende produktside: kandidaten er bygd fra en tom ramme. Appbar og Porthole-hostnavigasjon må samordnes ved implementering; dagens Porthole-dobbeltkrom er ikke gjengitt her. Knapper for ekte Git-, chat-, prosjekt- og jobbendringer viser bare en lokal forhåndsvisning.

Chrome-skjermdumper er JPEG fra CUA. Vanlig viewport beholdes; responsive opptak har egen bredde. Native/Binding er ikke rendret. Bildenes faktiske piksler er referansen, ikke en påstand om kryssplattformparitet.

G3-opptaksvei: staging → Developer Workbench → Tilgjengelige prosjekter → Åpne arbeidsrom → Oversikt/Relasjoner/Arbeidsflyt. Dagens inngang er rapportert av brukeren og Portfolio-selection er prøvd, men dashboard-destinasjonen finnes ikke ennå; matchende live-opptak kan derfor ikke tas før implementering. Tom/offline/leser krever dedikert autorisert testoppsett. Mangelen er eksplisitt, ikke skjult bak kandidatbildet.
