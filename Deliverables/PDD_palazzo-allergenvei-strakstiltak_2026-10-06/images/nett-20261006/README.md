# Skjermbilder fra nett etter utsettingen (6. oktober 2026)

Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`. Alle klokkeslett er UTC.

## Hva bildene er

Bildene `nett-*.png` er skjermbilder av `https://palazzo.digipomps.org/palazzo` slik siden sto etter at commiten `c5058f49` var satt ut kl. 13:19. De er tatt i Chrome på Kjetils Mac (gjennom Claude-utvidelsen) mellom kl. 13:33 og 14:16. Ingenting er byttet ut: siden, svarene og modellen er de som står på nett.

- Spørsmålene er skrevet i spørrefeltet og sendt med Enter. Drikkelisten er hentet ved å trykke sidens egen snarvei «Hva kan jeg drikke?» med musen. Slik ble også de godkjente bildene laget.
- Vinduet er 1280 punkter bredt og 752 eller 757 punkter høyt. Kortet med spørrefeltet og et svar er høyere enn vinduet. Seks av bildene er derfor satt sammen av to skjermbilder av samme side, tatt ved to rulleposisjoner uten at noe annet er rørt imellom. Bildet av det tomme spørrefeltet (`nett-eksempel.png`) er ett skjermbilde. Delene ligger i `raa/`, med rulleposisjonen i filnavnet.
- Sammensettingen er gjort med `sy_sammen.py` (ligger her): den klipper ut kortet med tolv punkter kant og legger den nedre delen under den øvre. Ingen bildepunkter er endret.
- Bildene `sammen-*.png` viser det godkjente bildet og skjermbildet ved siden av hverandre, laget med `HD/maal/grunnlag-20261006/render/sett_sammen.py`. Venstre side er høyre halvdel («Etter») av det godkjente bildet, slik den ble rendret 6. oktober (`raw-etter-*.png`). Overskriftene og tekstene over bildene er lagt på og er ikke en del av siden.

## Filene på Mac-en

Bildene er laget i Losens skyarbeidsområde og kopiert hit. Kopieringen la en metadatablokk på rundt 5,8 kB inn i hver bildefil, så md5 er ikke den samme som i skyen. Bildepunktene er de samme: kontrollert for `nett-henvisning-hvete.png` og `raa/hvete-del1-scrollY941.jpg` ved å hente filene tilbake og sammenligne punkt for punkt.

## Det som ikke lot seg ta

**Henvisningen på en telefon (390 punkter).** Chrome gjennom utvidelsen holder vinduet på 1280 punkter uansett hvor smalt vinduet gjøres, og siden nekter å bli vist i en ramme (`frame-ancestors 'none'`), så bredden lot seg heller ikke prøve på den måten. Det er ikke tatt noe skjermbilde på telefonbredde. Det som er målt i stedet: for «Er det hvete i Carpaccio di polpo?» er svaret nettstedet ga kl. 13:21 (kallet `M037` i `HD/maal/nett-ut/spoersmaal-strakstiltak-nett-20261006-20261006T132126Z.jsonl`) likt i alle 13 felt med svaret det godkjente telefonbildet ble rendret av (`HD/maal/grunnlag-20261006/render/etter-henvisning.json`); md5 av de to, skrevet ut med sorterte nøkler, er `c01c3017bd321c4701e3dc597241c2c1` for begge. Og sidens CSS og JavaScript på nett er filene bildet ble rendret med (tabellen under).

## Sidens filer på nett

Hentet i nettleseren fra `https://palazzo.digipomps.org` kl. 13:44, og holdt mot filene i `PalazzoScaffold` (sha256):

| Fil | På nett | I repoet | Lik |
|---|---|---|---|
| `/palazzo` (`Public/palazzo/index.html`) | 6723 byte, `ab208462a95c1c1e4417645760e9748a06d4b2bfdca7827cde3e6775dd6c3af4` | filen i `c5058f49` (md5 `c638fc69ac57797fa44267441a4f1292`): samme sha256 | ja |
| `/css/palazzo-communale.css` | 24156 byte, `08abbc45edf1faf5ae178d8ddfedc09e33dc046000ec4a99c11f84d56be1283a` | filen de godkjente bildene ble rendret med (md5 `63284bdc9f370ff05786749f0388be4b`): samme sha256 | ja |
| `/js/palazzo-communale.js` | 9024 byte, `1f9174cf022386413bc93c7056be1b9732ff63965ed1960a01a7c34204d1175c` | filen de godkjente bildene ble rendret med (md5 `0e929f12959bc122e82c6ed66c6b7beb`): samme sha256 | ja |

Siden på nett er altså filen som ble committet, og utseendet (CSS og JavaScript) er det samme som da de godkjente bildene ble laget.

## Bildene

| Fil | Spørsmål | Tatt kl. | Deler i `raa/` |
|---|---|---|---|
| `nett-henvisning-hvete.png` | «Er det hvete i Carpaccio di polpo?» | 13:43 | `raa/hvete-del1-scrollY941.jpg`, `raa/hvete-del2-scrollY1091.jpg` (og et første skjermbilde kl. 13:31, `raa/hvete-kl1331-del1-scrollY941.jpg`) |
| `nett-linje-en-rett.png` | «Hva er Carpaccio di polpo?» | 13:33 | `raa/rett-del1-scrollY941.jpg`, `raa/rett-del2-scrollY1125.jpg` |
| `nett-linje-to-retter.png` | «Er det mandler i Orata al forno a legna?» | 13:43 | `raa/to-retter-del1-scrollY941.jpg`, `raa/to-retter-del2-scrollY1184.jpg` |
| `nett-linje-pizzalisten.png` | «Hvilke pizzaer har dere?» | 14:02 | `raa/pizzalisten-del1-scrollY941.jpg`, `raa/pizzalisten-del2-scrollY1145.jpg` |
| `nett-linje-drikkelisten.png` | snarveien «Hva kan jeg drikke?», trykket med musen | 14:02 | `raa/drikkelisten-del1-scrollY941.jpg`, `raa/drikkelisten-del2-scrollY1263.jpg` |
| `nett-linje-bordbestilling.png` | «Hva bør jeg bestille når jeg ikke kan spise mandler?» | 14:15 | `raa/bordbestilling-del1-scrollY941.jpg`, `raa/bordbestilling-del2-scrollY1263.jpg` |
| `nett-eksempel.png` | ingen; siden lastet på nytt, feltet tomt | 14:16 | `raa/eksempel-scrollY941.jpg` (og ett med feltet i fokus kl. 14:01, `raa/eksempel-feltet-i-fokus-scrollY941.jpg`) |

Nettleseren sendte sju kall for disse bildene: seks ulike, og spørsmålet om hvete to ganger, fordi det første skjermbildet manglet den nedre delen. De kommer i tillegg til de 174 i målingen, og står i vertens logg sammen med dem.
