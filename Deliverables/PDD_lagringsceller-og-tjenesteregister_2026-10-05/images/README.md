# Renderingsgrunnlag

Bildene er skjermbilder av `../mockup.html` med eksempeldata, rendret med Chromium 2026-10-05 (1100 px, og 390 px for `register-smal-v1.png`). `../render.cjs` lager dem på nytt. Ingen tall er liveobservasjoner. Ikke godkjent.

## RENDERINGSERKLÆRING

Bildene er HTML-skisser, ikke Porthole-preview. Dette er ikke bevist at dagens skeleton kan rendre:

- Rader med fem kolonner i fast rutenett. Skissen bruker det i tjenestelisten og fillisten; i skeleton blir dette List-rader, og kolonnejusteringen kan avvike.
- Venstrestilt tekst i Binding (lesson.sketch-assumed-a-renderer-it-did-not-have). Web er venstrestilt; Binding er ikke sjekket for disse flatene.
- Fargede merkelapper («Kontrollert», «Utdatert», «Utelukket») og nedtonede rader. Må uttrykkes med det skeleton har av tekststil; eksakt utseende er ikke bevist.
- Fargede bannere med knapper inni. Blir trolig et kort med tekst og knapper under.
- Tre talltavler side om side. Kan bli stablet.
- Omregning av «Anslått per måned» når kravene endres skjer i cellen, ikke i flaten. Skissen regner ikke.

Det skissen forutsetter at finnes: List, Text, TextField, Picker og Button. Ingen nye skjelettelementer er forutsatt.
