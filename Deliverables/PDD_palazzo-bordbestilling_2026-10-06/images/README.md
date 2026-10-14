Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

Skrevet 7. oktober 2026 av Losen. G1-GUI er Kjetils ord og er ikke gitt. Stier er relative til HAVEN-roten.

## RENDERINGSERKLÆRING

Ingen av bildene er et skjermbilde av en kjørende flate, og ingen er rendret fra et skjelett. Det finnes ikke noe skjelett for disse flatene, og ingen av flatene er bygget. Bildene er HTML tegnet for hånd og rendret i Chromium (Playwright) i Losens skyarbeidsområde, 1280 punkter bredt.

- **Farger og skrifter** er Palazzos egne: fargene fra `PalazzoScaffold/Public/css/palazzo-communale.css`, og skriftene Jost og Playfair Display fra `PalazzoScaffold/Public/css/themes/palazzo/fonts/`. Oppsettet er mitt, ikke sidens.
- **Tallene og referansene er et eksempel.** De er satt opp for hånd for én lørdag, med planen testene bruker (bord 1 og 2 for én til to, bord 4 for tre til fire, bord 9 for fem til åtte, og ett bord i en stengt bar). Eksempelet følger reglene i koden: hvert bord holdes i to timer, og ingen to bestillinger deler bord i overlappende tid. Ingen kode har regnet dem ut.
- **Tekstene** er mine forslag. Ingen av dem står i koden. Cellens egne svar er på norsk, men kortere og med datoen som `åååå-mm-dd`.
- **Bildene er rettet én gang**, natt til 7. oktober, etter at en uavhengig tråd holdt dem mot koden (se «Rettet etter kontrollen» under). Du har ikke sett den første utgaven, så filnavnene er de samme.

Kildene ligger i `images/kilde/`: `felles.css`, `hvor.html`, `bordbok.html`, `gjest.html` og `rendre.js`. Skriftene hentes der fra Losens skyarbeidsområde, så de må pekes om før filene kan rendres et annet sted.

## Bildene

| Bilde | Hva det er | Hva det viser |
|---|---|---|
| `tillegg-hvor-ligger-hva-v1.png` | En tegning av det som er bygget. Ikke en flate | Hvem som eier hva: gjestens entitet, husets celle, regneark og logg, og hva kelneren ser. Hva som ikke lagres hos huset |
| `husflate-bordbok-dagen-v1.png` | Forslag til en flate for huset og de ansatte. Ikke bygget | Dagen: nøkkeltall, bestillingene etter klokkeslett med handlinger, ventelisten, bordene med hvem som sitter når, og områdene |
| `gjesteflate-bestill-bord-v1.png` | Forslag til en flate for gjesten, på telefon. Ikke bygget | Tre tilstander: velge tid, bestilt, og fullt med venteliste |

## Rettet etter kontrollen

Kontrolltråden K2 fant at tre tekster sa mer enn koden gjør, og at eksempelet ikke hang sammen på tvers av bildene. Rapporten: `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/K2-DOKUMENTER.md`.

| Bilde | Sto | Står nå |
|---|---|---|
| `gjesteflate-bestill-bord-v1.png`, skjerm 1 og 2 | «Huset har bare referansen, tidspunktet, antallet og bordet» | Huset har også at bestillingen er gjestens, og en peker til gjestens entitet |
| samme, skjerm 3 | «Blir det ledig, gir huset bordet til den som ba først» | Huset ser hvem som ba først, og gir bordet selv. Til da kan andre bestille det. Reglene holder ikke bordet av |
| samme, skjerm 1 og 3 | Venteliste bare på 19:00, og 20:00 vist som ledig etter bestillingen i skjerm 2 | Venteliste på begge de fulle tidene, og 20:00 er ikke blant de ledige i skjerm 3 |
| `tillegg-hvor-ligger-hva-v1.png` | Gjesten ser «alt huset holder»; loggen føres «hver gang huset fører noe» | Gjesten ser bestillingene slik huset har dem, og om huset har pekeren; loggen føres ved bestilling, endring, avbestilling og bord fra ventelisten. Kanalen er sju faste ord. Gjestens post har også statusen, og oppdateres ikke |
| `husflate-bordbok-dagen-v1.png` | De tre bestillingene kl. 19:00 i en rekkefølge jeg hadde satt for hånd | I den rekkefølgen koden gir (etter referanse) |

## Hva skjelettformatet ikke kan rendre

Ingenting her er prøvd mot skjelettformatet. Det jeg vet, er lest, ikke målt: designdokumentet fra 2. september sier at skjelettet mangler kalender- og bordelementer, og at nye elementtyper ikke lages uten Kjetil (`PalazzoComunaleScaffold/docs/Design_Integrasjoner_og_Datastrategi_2026-09-02.md`, gjengitt i `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/les/L1-GASTROPLANNER.md`). Skal flatene bygges, må det avgjøres om de blir HTML-sider, som de offentlige flatene under `PalazzoScaffold/Public/`, eller om skjelettformatet skal få nye elementer.

## Tilstander som mangler

Før G1-GUI kan gis for en flate, må disse tegnes:

- Husets bordbok: en dag uten bestillinger, en feil (planen er ikke lagt inn), telefonbredde, og skjemaet for å føre en bestilling.
- Husets plan: hvordan bord, områder og seteplaner legges inn. Ikke tegnet i det hele tatt.
- Gjestens side: «Mine bestillinger», endring, avbestilling, feilmeldingene, og hvordan gjesten kommer inn og blir en identitet.
- Kelnerflaten: «Bookinger» med husets egne bestillinger. Koden er skrevet og testet, men flaten er ikke sett kjørende, fordi ingenting er satt ut.
