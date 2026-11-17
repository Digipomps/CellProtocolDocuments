# ACCEPT — palazzo bordbestilling

Skrevet 7. oktober 2026 av Losen, og rettet samme natt etter den uavhengige kontrollen. G3 er ikke bedt om: G1, G1-GUI og G2 er ikke gitt. Dette er det som er bygget, holdt mot «Det du kommer til å se» i `FORMAALSSPEC.md` §3, så du kan se hvor det står. Stier er relative til HAVEN-roten.

## Forventet mot faktisk

| Leveranse i §3 | Forventet | Faktisk | Bevis |
|---|---|---|---|
| Koden på en egen gren | Celle, regler og ruter for husets egen bordbestilling | To commits på `losen/palazzo-bordbestilling-20261007`: `7976bb15c8ce525f343103e98ebbb2f82be48568` (11 filer, 4234 linjer inn, 4 ut) og `7eb404f1f8e3baf16e93f8a1b1447ed1c6f3b508` (rettinger etter kontrollen: 7 filer, 1225 inn, 129 ut). Ikke pushet | `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/svar/d143-commit.md` og `d152-k-commit-2.md` |
| Testene | Reglene og rutene, grønne, og vist røde med vilje | 328 tester, 0 feil. 47 er nye. 29 av de 47 er vist røde med vilje i fem kjøringer; 18 er ikke det | `TESTRESULT.md` |
| Beskrivelsen av rutene | Hvem som når hva, hva som lagres hvor | Skrevet om etter kontrollen, og med i den andre commiten | `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md` på grenen. Samme utgave ligger i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/kilde/docs/` |
| Tegningen av hvor bestillingen ligger | Ett bilde | Laget, og rettet etter kontrollen | `images/tillegg-hvor-ligger-hva-v1.png` |
| Husets bordbok | Forslag til flate | Skisse laget. Flaten er ikke bygget | `images/husflate-bordbok-dagen-v1.png` |
| Gjesten bestiller bord | Forslag til flate | Skisse laget, og rettet etter kontrollen. Flaten er ikke bygget | `images/gjesteflate-bestill-bord-v1.png` |
| Kelnerflatens «Bookinger» | Teller husets egne bestillinger | Koden er skrevet og testet. Ikke sett på en kjørende flate, fordi ingenting er satt ut | `TESTRESULT.md#ruter` |

## Avvik fra arbeidsflyten

1. **Koden er skrevet før G1, G1-GUI og G2.** Sagt på forhånd kl. 23:49 (21:49 UTC) 6. oktober, og ført i `STATUS.md`. Ordene dine var en tillatelse med et vilkår («om du slipper opp for ting å gjøre»). Om vilkåret var oppfylt, er ditt å si. Ingen flate er bygget.
2. **`FORMAALSSPEC.md` er skrevet samme natt som koden, etter at koden var grønn.** Formålene og testlisten var bestemt før koden, men bare i arbeidsnotatene mine. Dokumentet du leser, er skrevet etterpå.
3. **Skissene er laget etter koden.** For rutene spiller det ingen rolle. For flatene betyr det at de må godkjennes før noe bygges, som vanlig.
4. **Den første utgaven hadde tre alvorlige feil som testene mine ikke fant.** En uavhengig tråd fant dem ved å lese koden: samme bord kunne gis to ganger over midnatt, kanalen var fri tekst, og lagret tilstand som ikke lot seg lese, ble til tom tilstand. De er rettet i den andre commiten. Jeg hadde skrevet «huset lagrer ingenting om gjesten» uten å prøve det for det ene feltet huset selv fyller ut.
5. **Rettingene er gjort uten nytt ord fra deg.** De retter feil i det som var skrevet. To legger til noe: huset kan peke ut bord på nytt i en endring, og kanalen er en lukket liste jeg har valgt.
6. **Den siste runden rettinger er ikke lest av en uavhengig tråd.** K5 leste første runde og fant to feil i den. Rettingene av de to er prøvd og vist røde, men ikke lest av andre.

## Docs {#docs}

| Endret oppførsel | Hvor det står |
|---|---|
| Ny celle, nye ruter, nytt ark | `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md` (ny), `PalazzoScaffold/README.md` (rutetabellen, celletabellen) |
| HTTP 409 for `refused` | `PalazzoScaffold/README.md`, avsnittet om svar |
| Kelnerflaten teller egne bestillinger | `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md`, avsnittet «Kelnerflaten» |
| Discovery lister cellen og rutene | `PalazzoScaffold/Sources/App/Cells/PalazzoScaffoldInfoCell.swift` |
| Kanalene, midnatt, ny bekreftelse, bord i en endring, kjente svakheter | `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md`, skrevet om i den andre commiten |

Alt er i samme commit som koden det beskriver.

## Status {#status}

`STATUS.md` sier det samme som denne filen: ingen port gitt, to commits (`7976bb15` og `7eb404f1`), 328 tester, ikke pushet, ikke satt ut.

## Tomme handlere {#stubs}

Søkt i `PalazzoScaffold/Sources/App/Cells/PalazzoBookingCell.swift`: 16 nøkkelstier er registrert (15 under `booking.` og `insight.bookings.upcoming`), i tillegg til `integration.state` og samtykkeflaten fra felles kode. Hver av de 16 gjør noe og har minst én test som kaller den. Ingen svarer uten å ha gjort jobben. Det cellen ikke gjør, står i `booking.state` under `notBuilt`: tolv punkter, de samme som i beskrivelsen. De 16 står også i `contract/noekkelstier.json`, som er holdt mot kildefilene med et skript.

## Paritet og veier inn {#parity}

Gjelder ikke ennå. Ingen flate er bygget.
