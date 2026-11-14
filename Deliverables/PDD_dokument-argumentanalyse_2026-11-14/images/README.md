# Bilder til G1-GUI (iterasjon 1, 2026-11-14)

## Rendret fra skeleton-JSON (ekte web-renderer)
`analyserom-*-{laptop,iphone}-v1.png` er rendret med CellScaffold `8e8f8e0` sin `Public/js/skeleton-runtime.js` og `Public/css/porthole-webo.css` fra `skeleton/analyserom-skeleton.js` og tilstandene i `skeleton/analyserom-states.js` (`skeleton/render.js`). Ikke Porthole med celle bak, og ikke Binding.

- Påstandene, typene, styrken og kildestatusen er det TextReliability faktisk ga for `fixtures/eksempeltekst.md` (`results/eksempeltekst.analysis.json`).
- Markeringer, chat og modellforslag er illustrasjoner.
- Grafen i `fylt-graf` og `modellforslag` viser hvordan dagens `Visualization kind: network` tegner argumentet. Den er laget for å utforske nettverk: bare valgt node har etikett, kantene har ingen tekst, og webens og Swifts utgave ser ulike ut.

## Mockup (HTML, ikke skeleton)
`argumentkart-mockup-{laptop,iphone}-v1.png` fra `mockup/argumentkart-mockup.html` viser et lesbart argumentkart: konklusjon øverst, merkede kanter (støtter, angriper, tilbakeviser), antatte kanter stiplet, kildestatus i hver boks. **Dette kan dagens skeleton ikke rendre.** Det krever enten en ny visningstype i CellProtocol (web + CellApple) eller et Mermaid-bilde.

## Kjente svakheter i bildene
- På iPhone ligger chatten nederst, under alle påstandene.
- En lang URL i P4 går litt utenfor kortet på iPhone.
- Fanene er dagens standardknapper.
