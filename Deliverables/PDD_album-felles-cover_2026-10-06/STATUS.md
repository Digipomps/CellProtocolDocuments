# STATUS — album med felles cover

2026-10-06 · punkt 2 av seks

## Porter
- G1: dekket av at Kjetil godkjente rekkefølgen på arbeidet og sa «gjør det nå» 2026-10-05
- G1-GUI: **venter på Kjetil** — `images/album-v1.png`
- G2: trengs her. Albumet har bildeopplasting og en ny offentlig rute; planen skrives
  når bildet er godkjent

## Skrevet
Ingenting i repoet. Bare bildet, og stilene bildet er tegnet med:
`images/forslag-stiler.css`.

## Hvorfor ikke mer
Albumet har flere valg som er Kjetils (se FORMAALSSPEC.md). Modellen skrives når de
er avgjort. Rekkefølge-modellen, som albumet bygger på, er skrevet på egen gren.

## Funn som hører hjemme i G2
Bildeopplasting og offentlig levering finnes alt i `PublicationCell`
(`Sources/App/Cells/Publication/PublicationCell.swift`): `uploadMedia` med filtypeliste,
størrelsesgrense og lagringskvote, og ruta `/pub/<slug>/media/<id>`. Lest i koden på
`origin/main` e5c34345, ikke kjørt. Albumcoveret bør gjenbruke den i stedet for å få
sitt eget lager — og da henger utgiverens publikasjon (profil, blogg) og musikken
sammen på samme sted. Avgjøres i G2. Grensen i bildet (PNG eller JPEG, opptil 2 MB) er
et forslag for cover spesielt; publikasjonens egne grenser er videre.

## Hvordan bildet er laget
Flatens egen mal, stilark og skript (`origin/main` e5c34345 + profil-lenka), rendret i
Chromium med alle kall fanget. Det nye er markup satt inn i siden og stilene i
`images/forslag-stiler.css`. Sangtitlene er eksempeldata, ikke Butterpops katalog.

## Rekkefølgen på arbeidet
Kjetil godkjente «2 album, 3 rekkefølge». Rekkefølge-modellen er likevel skrevet
først, fordi albumet trenger den: et album er en ordnet liste med bilde og tittel.
