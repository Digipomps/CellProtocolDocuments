# FORMÅLSSPEC — album med felles cover

Iterasjon 1 · 2026-10-06 · punkt 2 av seks i rekkefølgen Kjetil godkjente 2026-10-05

## P0 — hva Kjetil sa

> «Jeg ba for en stund siden om støtte for album, egne spillelister, loop, og
> mulighet til å endre rekkefølgen på sangene i en publisert liste.»

Og i rekkefølgen han godkjente: «album med felles cover».

## Formål

En utgiver kan samle flere sanger til én utgivelse med ett bilde og én tittel, og
lytteren møter den som en helhet: coveret, tittelen, sangene i utgiverens rekkefølge.

## Hva som skal være sant når dette er ferdig

1. Den som har rett til å publisere, kan lage et album, gi det tittel og bilde, og
   legge publiserte sanger i det.
2. Lytteren ser albumet som én blokk i lista, med sangene nummerert.
3. Coveret følger sangen: det vises i spilleren når en sang fra albumet spilles.
4. «Spill album» spiller sangene i albumets rekkefølge.
5. Å løse opp et album avpubliserer ingenting.
6. Et album uten publiserte sanger vises ikke, og coveret til et slikt album kan ikke
   hentes.

## Generelt, ikke Butterpop

Albumet ligger i `MusicLibraryCell`. Enhver utgiver får det.

## Åpne valg — ligger i bildet, og er Kjetils

- En sang står i ett album, eller for seg selv. Samlinger der samme sang går igjen,
  er ikke med.
- Coveret er et åpent bilde. Det vernes ikke slik lyden skal bli (se
  `PDD_innholdsvern-lyd-20260909_2026-09-10`).
- PNG eller JPEG, opptil 2 MB.
- Ikke med: kjøp av et helt album, egen side per album, eget cover per sang.
  `MusicTrackRecord.coverAssetID` finnes fra før og kan settes når en sang lages
  eller endres, men ingenting viser eller leverer det.

## Henger sammen med

- **Rekkefølge** (punkt 3): albumet bygger på samme ordnede liste og samme fane i
  Studio. Rekkefølge bør derfor inn først.
- **Lagringscellene** (bestilt 2026-10-05): coveret er en liten fil og kan ligge i
  dagens lokale lager. Flyttes lagringen, flyttes coveret med.
