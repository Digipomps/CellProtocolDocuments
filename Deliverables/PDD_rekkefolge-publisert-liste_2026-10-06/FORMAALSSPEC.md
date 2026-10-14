# FORMÅLSSPEC — rekkefølge i publisert liste

Iterasjon 1 · 2026-10-06 · punkt 3 av seks i rekkefølgen Kjetil godkjente 2026-10-05

## P0 — hva Kjetil sa

> «Jeg ba for en stund siden om støtte for album, egne spillelister, loop, og
> mulighet til å endre rekkefølgen på sangene i en publisert liste.»

## Formål

Utgiveren bestemmer i hvilken rekkefølge lytterne møter sangene. I dag bestemmer
publiseringstidspunktet det: nyeste øverst, og ingen kan gjøre noe med det.

## Hva som skal være sant når dette er ferdig

1. Den som har rett til å publisere, kan sette rekkefølgen på det som er publisert.
2. Lytteren ser lista i den rekkefølgen, og «Spill alle» følger den.
3. En utgiver som aldri har ordnet noe, merker ingen forskjell: nyeste øverst.
4. En ny sang legges øverst til den blir flyttet.
5. Rekkefølgen overlever omstart.
6. En rekkefølge som ikke stemmer med det som står i lista (en sang er trukket, eller
   nevnt to ganger) avvises og endrer ingenting. Utgiveren får vite hvorfor.

## Generelt, ikke Butterpop

Rekkefølgen ligger i `MusicLibraryCell`, og handlingen går gjennom arbeidsrommet som
de andre publiseringshandlingene. Enhver utgiver får den.

## Henger sammen med

- **Album** (punkt 2): rekkefølgen i et album er samme sak, ett nivå ned. Den delen
  kommer med albumet, ikke her.
- **Egne spillelister** (punkt 5): lytterens rekkefølge, ikke utgiverens. Eget arbeid.

## Avgrensning

Ikke dra-og-slipp i første omgang. Ikke rekkefølge per lytter.
