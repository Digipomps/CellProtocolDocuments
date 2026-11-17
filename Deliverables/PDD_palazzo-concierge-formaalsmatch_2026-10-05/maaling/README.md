# Måling: korpus og sølvfasit (arbeidspakke 1)

Laget 7. oktober 2026 kl. 08:33–08:47 UTC av Losen, med fem skrivetråder og fjorten tolketråder (uavhengige Claude-tråder). Metoden er den i `CellProtocolDocuments/Book/38_Measuring_Purpose_Understanding_Without_A_Model.md`. Stier er relative til denne mappen der ikke annet står. Tallene under er regnet av kode fra filene her.

## Hva som ligger her

| Mappe | Innhold |
|---|---|
| `korpus/` | `korpus-v1.jsonl`: 769 setninger, frosset (md5 i `korpus/FROSSET.md`). 249 skrevet av fem skrivetråder, 307 målte spørsmål fra 4.–6. oktober, 179 fra det blinde angrepet 6. oktober, og 34 spørsmål fra gjester i settet fra mai. Hver rad har kilden, en opak id og om den er holdout (25 %, av hash av kildens id) |
| `skribenter/inn/`, `skribenter/ut/` | Reglene, de fem oppgavene, menyen skribentene fikk se, og de fem filene de leverte (50 setninger hver, med skribentens eget formål og mening). Skribentene så menyen slik en gjest ser den. De så ikke katalogen, emnene eller grafen |
| `tolk/inn/`, `tolk/ut/` | Reglene, katalogen (formål, retter, drikke, emner, allergener), de fjorten bunkene og de fjorten svarfilene. To tolker (A og B) leste alle 769 setningene hver for seg, i ulik stokket rekkefølge, sju bunker hver. Bunkene har bare opak id og tekst |
| `fasit/` | `tolk-raa.json` (begge tolkenes svar), `solvfasit-v1.jsonl` (689 rader der de to er enige om formål og om nodene med fortegn), `uenige-v1.jsonl` (80 rader der de ikke er det; de er satt til side og brukes ikke) |

## Tallene

| | Antall | Andel |
|---|---|---|
| Setninger | 769 | |
| Tolkene enige om formål | 750 | 98 % |
| Tolkene enige om nodene (med fortegn) | 706 | 92 % |
| Enige om begge: sølvfasit | 689 | 90 % |
| Enige også om slaget på hver node | 676 | 88 % |
| Skrevne setninger der skribenten og begge tolkene har samme formål | 239 av 249 | 96 % |

Sølvfasiten per formål: vite 282, unngaa 190, spise 62, drikke 39, selv 39, bord 32, aapningstid 22, ingen 23. 517 er treningsrader og 172 holdout. 505 har minst én node. 175 er merket som allergi eller trygghet av begge tolkene.

## Det som ikke er bra nok

- **Dette er sølv, ikke gull.** To tolker som er enige, kan ta feil på samme måte. Ingen dommer har sett sakene, og ingen lokkeduer er brukt (`test.maal.lokkeduer` er utsatt i spesifikasjonen).
- **Regelfilen og katalogen sa ulikt om «har dere <en drikk>?».** Regelfilen la «har dere …» under `vite`; katalogen hadde «har dere eplemost» som eksempel under `drikke` (det står slik i `../graf/emner-v1.md`). Tolkene delte seg. Fire rader ble uenige av den grunn, og flere tolker meldte det.
- **Allergener uten at noen sier de ikke tåler dem** («er det egg i pastaen?»): reglene sa ikke om allergenets node skal brukes. Tolkene delte seg, og slike rader er ofte blant de uenige.
- **Oversatte rettnavn** («trøffelpizzaen», «lemon cream»): noen tolker valgte retten, andre emnene.
- **Settet er skjevt.** 368 av de 769 setningene kommer fra sett som ble skrevet for å prøve allergenveien 5. og 6. oktober (gruppene `blind1-*`, `de21`, `de28` og det blinde angrepet). Vanlige ønsker om mat og drikke kommer mest fra de 249 skrevne.
- **Dette er et utviklingssett.** Skribentene har ikke sett grafen, men settet brukes til å justere den. Tallet som teller, kommer fra et korpus skrevet etter at grafen er frosset, av nye skribenter (`test.maal.uavhengig-korpus`).

## Slik er de opake id-ene laget (`test.maal.opake-id`)

Hver setning fikk en tilfeldig id (`s` og sju heksadesimale tegn) fra en tilfeldig-generator med fast frø, uavhengig av kilde og rekkefølge. Bunkene til tolk A og tolk B er stokket med hvert sitt frø. Tolkenes innfiler har bare `id` og `tekst`. Eksemplene i regelfilen er laget for regelfilen og finnes ikke i korpuset (kontrollert med kode).
