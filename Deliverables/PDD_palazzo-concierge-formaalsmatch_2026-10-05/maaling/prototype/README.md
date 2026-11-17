# Prototypen: dekomponeringen skrevet utenfor Swift

Laget 7. oktober 2026 av Losen. Stier er relative til denne mappen der ikke annet står.

Dette er dekomponeringen (F1) og leseren av husets graf (F7) skrevet i Python, linje for linje slik Swift-koden gjør det. Den finnes av to grunner:

1. **Verksted.** En endring i ordlistene måles her på sekunder. Et bygg på Mac-en tar et par minutter gjennom køen.
2. **Referanse.** `lag_referanse.py` skriver ut hva prototypen gir for hver av de 769 setningene i korpuset. Swift-testen `PalazzoScaffold/Tests/AppTests/PalazzoDekomponeringMaaltTests.swift` krever at Swift-koden gir det samme, setning for setning, og at tallene mot fasiten er like. To utgaver skrevet hver for seg må altså være enige før noe er grønt.

Tallene som legges fram for Kjetil, er dem Swift-testen skriver ut (linjene som begynner med `MAALT`). Prototypen er ikke produksjonskode og settes ikke ut.

## Filene

| Fil | Hva den gjør |
|---|---|
| `stier.py` | Hvor korpusene, fasitene, katalogen, menyen og ordlistetrådenes filer ligger, relativt til denne mappen og til HAVEN-roten. `HAVEN_ROOT` og `PALAZZO_MAALING` overstyrer |
| `ordtreff.py` | Butlers `normalize` og `termMatchesToken`, portet (svarer til `PalazzoScaffold/Sources/App/Support/PalazzoOrdtreff.swift`) |
| `husgraf.py` | Leser datafilen og korpuset og bygger leksikonet (svarer til `PalazzoScaffold/Sources/App/Models/PalazzoHusgraf.swift`). `valider()` gjør kontrollene Swift-leseren gjør, også for avsnittet `svar` |
| `dekomp.py` | Dekomponeringen (svarer til `PalazzoScaffold/Sources/App/Services/PalazzoDekomponering.swift`) |
| `lag_data.py` | Bygger datafilen: emnene og kantene fra `../../graf/emner-v1.json`, ordformene og stikkordene som står i skriptet, og ett eller flere tillegg når de oppgis. Uten `GRUNN=3` bygger den versjon `.2` som før. Med `GRUNN=3` tas de navngitte rettelsene etter `.2` med, og avsnittet `svar`; `UTEN=<navn>` holder én rettelse utenfor i en prøve |
| `flett_leks.py` | Lager tillegget av forslagene i `../ordlister/ut/`, med kontrollene som står øverst i skriptet |
| `lag_leksinn.py`, `flett_leks2.py` | Runde 2 av ordlistene: lager innfilene trådene fikk (`../ordlister2/inn/`), og fletter det de leverte (`../ordlister2/ut/`) med det som er avgjort for hånd (`../ordlister2/haand/`) |
| `lag_referanse.py` | Skriver referansen Swift-testen holdes mot |
| `maal.py`, `vis.py`, `feiltyper.py`, `sammenlign.py` | Måler mot sølvfasiten. Radene som skrives ut, er alltid treningsrader. Holdout skrives bare som tall, og bare når `HOLDOUT=1` er satt |
| `maal2.py`, `sammenlign2.py` | Det samme for et hvilket som helst korpus med fasit (`maal2.py <datafil> <korpus> <fasit> [trening]`), og to datafiler mot begge korpusene (`sammenlign2.py <før> <etter>`). Avholdte rader skrives aldri ut |
| `endringslogg.py` | For hver oppføring i datafilen: hvilke treningsrader den retter (oppføringen tas ut alene, og treningsradene måles på nytt) |
| `endringslogg2.py` | Det samme, med treningsradene fra flere korpus (brukt fra versjon `.3`: 714 rader) |
| `kollisjoner.py` | Hvert ord i treningsradene og i menyen som treffer en term uten å være lik den. Listen leses for hånd; en kollisjon blir et unntak i datafilen |
| `proev.py`, `sjekk_swifttester.py` | Tilfellene fra spesifikasjonen, og forventningene i Swift-testene, kjørt i prototypen før noe sendes til bygg |
| `husmatch_sim.py` | Matchen (F2) regnet etter utenfor Swift: samme regning som `PalazzoSignalGraph.contributions` med vekt på kantene. Brukes bare til å kontrollere forventningene i `PalazzoScaffold/Tests/AppTests/PalazzoHusmatchTests.swift`. Kjøres med datafilen som argument |
| `samtale_sim.py` | Samtalen og svarene (F5 og F6) skrevet utenfor Swift, steg for steg som `PalazzoScaffold/Sources/App/Services/PalazzoSamtale.swift`, etter `../../contract/SAMTALE-UTSETTING-1.md`. Svar «som i dag» regnes ikke her; utfallet er da veien «som-i-dag» med grunnen |
| `lag_samtalereferanse.py` | Skriver referansen `PalazzoScaffold/Tests/AppTests/PalazzoSamtaleReferanseTests.swift` holdes mot: 41 skrevne samtaler, og én per rett, drikk og emne laget av grafen (162 samtaler, 402 steg med datafil `.4`). Kontrollerer dataene først (ingen overskrift sier «uten» eller «fri»; hver post uten alkohol kan nevnes). `python3 -B lag_samtalereferanse.py ../../graf/palazzo_husgraf-20261007.4.json <ut.json> vis` |

## Slik lages en ny versjon av datafilen

Fra denne mappen, på en maskin som har HAVEN-roten (ellers med `HAVEN_ROOT` satt):

```
python3 lag_data.py /tmp/grunn.json husgraf-proeve
python3 flett_leks.py /tmp/grunn.json /tmp/tillegg.json
python3 lag_data.py /tmp/palazzo_husgraf.json <ny versjon> /tmp/tillegg.json
python3 sammenlign.py <forrige datafil> /tmp/palazzo_husgraf.json     # hvilke treningsrader ble rettet, og hvilke ødelagt
python3 lag_referanse.py /tmp/palazzo_husgraf.json /tmp/formaal-dekomp-referanse.json
```

De to siste filene legges i `HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/data/<versjon>/`, og `HAVEN-Deploy/_handoff/HD-0077/mac/formaalsmatch-dataversjon-20261007.sh <versjon>` bygger og tester med dem. Ingen kode endres.

## Regler som gjelder her

- **Holdout-radene leses ikke.** Ingen endring begrunnes med en holdout-rad (`test.maal.holdout-urort`). Skriptene skriver bare tall for dem.
- **Tomt er ikke grønt.** Swift-testen krever 769 setninger og 689 fasitrader før den måler noe.
- **En rad er riktig på noder** når mengden av (node, fortegn) er lik fasitens. Noden `ukjent` telles ikke, og heller ikke noder tolkene ikke hadde i katalogen sin (`../tolk/inn/katalog.json`); i dag gjelder det bare emnet `vin`.
- Versjon `husgraf-20261007.3` bygges med `GRUNN=3` og tre tillegg; kommandoene står i `../ordlister2/README.md`. Den og versjon `.2` er bygget om igjen fra denne mappen på Mac-en 7. oktober 2026 kl. 12:32 UTC, og ga samme md5 som filene i `../../graf/`.
- Versjon `husgraf-20261007.1` av datafilen ble bygget før tre rettelser ordlistetrådene pekte på (se `../../graf/ENDRINGSLOGG.md`). Skriptet slik det står, bygger derfor versjon `.2` og senere; versjon `.1` ligger som fil i `../../graf/`.
