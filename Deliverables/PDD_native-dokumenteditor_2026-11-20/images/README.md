# Bilder — native dokumenteditor i Binding

**Dette er HTML-mockups**, ikke skjermbilder fra Binding. SwiftUI kan ikke rendres i skycontaineren. Kilde: `kilde/mockup.html`, rendret med `kilde/render.js` (Playwright, 2x).

| Fil | Flate | Tilstand |
|---|---|---|
| editor-tom-iphone-v1.png | iPhone, Binding | Nytt tomt dokument, tastatur oppe, formatlinje over tastaturet |
| editor-fylt-iphone-v1.png | iPhone | Overskrifter, fet/kursiv, liste, sitat, lenke, kommentarmarkering, Saras markør, diagram |
| editor-frakoblet-iphone-v1.png | iPhone | Frakoblet: endringer lagret på enheten, sendes senere |
| kommentarer-iphone-v1.png | iPhone | Kommentar-ark: ny kommentar til markert tekst, liste med «Vis i teksten»/«Løs» |
| editor-tom-mac-v1.png | Mac | Tomt dokument, verktøylinje, kommentarpanel |
| editor-fylt-mac-v1.png | Mac | Som fylt iPhone, med kommentarer i sidepanelet |
| editor-frakoblet-mac-v1.png | Mac | Frakoblet-banner og status nederst |

Hva mockupen ikke viser, men som gjelder i Binding: systemets tastatur og tekstmarkering (håndtak, forstørrelse), systemets delingsark for eksport, systemfonter (SF) i stedet for nettleserens. Skrivehjelp- og chatpanelet ligger under dokumentet som i dag og er ikke tegnet på nytt her.

## RENDERINGSERKLÆRING

Bildene er mockups, ikke Porthole-preview. Editoren er en native visualisering (`richDocument`) og kan ikke uttrykkes som skeleton-JSON. Det skjelettet og mockupen ikke kan vise:
- Systemets tastatur, tekstmarkering med håndtak og forstørrelsesglass (iOS).
- Systemets delingsark og eksportdialoger.
- SF-systemfonten og nøyaktig linjeavstand fra TextKit.
