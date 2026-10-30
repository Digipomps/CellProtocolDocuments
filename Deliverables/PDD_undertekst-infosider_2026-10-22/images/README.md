# RENDERINGSERKLÆRING

- Dagens skeleton-format kan ikke rendre dette nettstedet i det hele tatt: digipomps.org er håndskrevet HTML og CSS (egen typografi, klebrig toppmeny, kort-rutenett, artikkel-layout), ikke CellConfiguration. Det finnes derfor ingen `skeleton/`-mappe, og bildene er ikke Porthole-forhåndsvisninger.
- Bildene er i stedet Chromium-render (Playwright) av selve HTML-filene, altså det samme som en nettleser viser; ingenting i bildene er mockup.

Bildene i denne mappen er skjermbilder tatt med Chromium (Playwright) av de statiske HTML-filene i `Website/`, servert lokalt med `python3 -m http.server 4173` i Cowork-VM-en 2026-10-22. De er ikke Porthole-forhåndsvisninger: nettstedet er håndskrevet HTML og CSS, ikke CellConfiguration/skeleton, så det finnes ingen `skeleton/`-mappe å vise til.

- `for-*.png`: `origin/main` ad91600 (lik kjørende produksjon for disse tre sidene, ifølge Macens arbeidskopi 2026-10-22).
- `etter-*.png`: gren `claude/undertekst-infosider-20261022`.
- Viewport 1280 × 900 for desktop, 390 × 900 for `*-mobil.png`; elementskjermbilde av `#mennesket-og-fellesskapet` (forsiden), `#mennesket-forst` (artikkeloversikten) og `article#mennesket-forst` (artikkelen).
- `*-mobil.png` er tatt som helsideskjermbilde klippet til seksjonens rammeboks (sidekoordinater), ikke som elementskjermbilde: ved 390 px la den klebrige toppmenyen og hopp-til-innhold-lenken seg over toppen av seksjonen i et elementskjermbilde (sett 2026-10-22, første runde). Toppmenyen er dermed ikke med i mobilbildene.
- Skrift og linjebryting kan avvike litt fra Kjetils nettleser; innholdet og plasseringen er det som godkjennes.
- Opptaksvei ved G3: samme skript (`shots.js`, i Cowork-økten) mot `https://digipomps.org` etter utrulling, samme selektorer og viewporter.
