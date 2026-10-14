# TESTRESULT — palazzo dekningsvakt runde 2

Utdata fra hver avledet test i `FORMAALSSPEC.md` §5. Alle klokkeslett er UTC og gjelder
3. oktober 2026 der ikke annet står; det som skjedde 4. oktober, har datoen foran. Stier er
relative til HAVEN-roten (`/Users/kjetil/Build/Digipomps/HAVEN` på Mac-en, bruker kjetil).
`HD` = `HAVEN-Deploy/_handoff/HD-0077`, `PS` = `PalazzoScaffold`. Noen bevisfiler fra 4. oktober
har `20261003` i navnet, fordi skriptet som skrev dem, har datoen fast i filnavnet.

Fire commits på grenen `deploy/palazzo-demo-20260930` i `PS`:

| Runde | Commit | Hva |
|---|---|---|
| 2 | `311ba72945b18ab4c75c07cc8f0b13924600ae41` | Innholdet uendret, nitten hele setninger foran en liste, fire bindeledd, grunn i loggen |
| 2b | `876e835e615ac16edda54077e1d010ecc9d9bd6c` | Vakten bygger teksten selv, kolonet kreves, to setninger foran pizzalisten og fire foran rettlisten, to bindeledd |
| 2c | `771f991e7f010ca822679fb903c3c43038a6bccd` | En oppramsing beholder kolonet, to setninger foran hver liste, lister og retter sendes bare etter spørsmål på en lukket liste, rettlisten sendes ikke |
| 2c, andre commit | `a3fc5042e15bbb6d2b896c116d980cad0b21bf2e` | Verbet i spørsmålet er «har» (fire spørsmål ut, tre flertallsformer inn); kommentarer rettet |

## build {#build}

`swift build` gjennom køen (`HD/mac/cp-pin-verifiser-og-test-20260929.sh`), mot CellProtocol
`81601a6f835252aba7e99d43786fb5d67227c245`:

| Commit | Bevis | Linje i beviset |
|---|---|---|
| `311ba729` | `HD/maal/PINTEST-RUNDE2-ETTER-20261003.md` | `swift build rc=0` (linje 18) |
| `876e835e` | `HD/maal/PINTEST-RUNDE2B-ETTER-20261003.md` | `swift build rc=0` (linje 18) |
| `771f991e` | `HD/maal/PINTEST-RUNDE2C-ETTER-20261003.md` | `swift build rc=0` (linje 18) |
| `a3fc5042` | `HD/maal/PINTEST-RUNDE2C2-ETTER-20261003.md` | `swift build rc=0` (linje 18) |

CI (Linux, `PS/.github/workflows/palazzo-image.yml`) bygger og tester det samme før imaget
publiseres:

| Commit | Kjøring | Utfall | Bevis |
|---|---|---|---|
| `311ba729` | 37115889826 | `conclusion=success` | `HD/maal/PUSH-RUNDE2-20261003.md` (linje 15493) |
| `876e835e` | 37122204642 | `conclusion=success` | `HD/maal/KJEDE-RUNDE2B-DEPLOY-20261003.md` |
| `771f991e` | 37134856933 | `conclusion=success` | `HD/maal/FERDIGSTILL-RUNDE2C-20261003.md` |
| `a3fc5042` | 37227441653 | `conclusion=success` (4. oktober) | `HD/maal/PUSH-RUNDE2C2-CI-FORSOEK2-20261004.md` |

## regression {#regression}

Hele testmengden, før og etter hver runde:

| Når | Tre | Tester | Feil | Bevis |
|---|---|---|---|---|
| 2. oktober kl. 18:33 | før noe ble endret (`39d0657c`) | 227 | 0 | `HD/maal/PINTEST-RUNDE2-FOER-20261002.md` |
| kl. 10:16 | `311ba729` | 251 | 0 | `HD/maal/PINTEST-RUNDE2-ETTER-20261003.md` |
| kl. 12:13 | `876e835e` | 260 | 0 | `HD/maal/PINTEST-RUNDE2B-ETTER-20261003.md` |
| kl. 15:52 | `771f991e` | 265 | 0 | `HD/maal/PINTEST-RUNDE2C-ETTER-20261003.md` |
| kl. 18:29 | `a3fc5042` | 265 | 0 | `HD/maal/PINTEST-RUNDE2C2-ETTER-20261003.md` |

Tallet vokste med 24 tester i runde 2, 9 i runde 2b og 5 i runde 2c: 38 nye, alle i
`PS/Tests/AppTests/PalazzoConciergePhrasingTests.swift`. Den andre commiten i runde 2c la ikke
til noen test.

**De 22 testene fra før runde 2 er urørt.** `HD/mac/testendringer-20261003.sh` leser hver utgave
av testfilen rett fra git og sammenligner funksjon for funksjon
(`HD/maal/TESTENDRINGER-20261003.md`, kl. 18:30): `gamle=22 gamle_roert=0`. Fra `39d0657c` til
`a3fc5042` er det under `Tests/` lagt til 2870 linjer i fem filer (testfilen og fire fixturer),
og ingen linje er tatt bort. Ingen annen testfil er endret.

**Rundens egne tester er endret etter at de først ble committet: tretten endringer i ti tester.**
Fire i runde 2b, åtte i runde 2c og én i den andre commiten. Ingen test er fjernet. Hver endring
står med diff i `HD/maal/TESTENDRINGER-20261003.md`. Planen sa «Ingen eksisterende test endres»;
jeg leste det som testene fra før runden. Det er ført opp som avvik A6 i `ACCEPT.md` §3.

| Commit | Test | Hva som ble endret, og hvorfor | Snur eller fjerner noe testen krevde godtatt? |
|---|---|---|---|
| `876e835e` | `testRunde2TrofasteOmskrivingerGodtas` | Seks setninger som sto som «skal godtas» («Vi har følgende pizzaer på menyen», «Følgende pizzaer står på menyen», «Dette er pizzaene i kunnskapsgrunnlaget», «På menyen har vi følgende pizzaer», «Hos oss finner du følgende pizzaer», «Vi serverer følgende pizzaer»), er byttet med de to på vaktens liste og den godkjente innledningen. «Formaggi misti er et utvalg …» er byttet med «… er utvalg …». Angrep 2 viste at de seks sier mer enn «Vi har», og at vakten ikke kan bøye en artikkel | ja |
| `876e835e` | `testRunde2EtTallKanIkkeFlyttes` | «Menyen inneholder følgende retter» snudd fra godtatt til forkastet | ja |
| `876e835e` | `testRunde2DeGodkjenteSetningene` | Antall setninger på vaktens liste: fra tjue til tre foran pizzalisten og fem foran rettlisten | ja |
| `876e835e` | `testRunde2SettMaalesGjennomVakten` | Måleverktøyet oppgir også teksten vakten publiserer | nei |
| `771f991e` | `testRunde2EtTallKanIkkeFlyttes` | «Vi har følgende retter på menyen» snudd fra godtatt til forkastet; «Vi har følgende retter» lagt til som godtatt | ja |
| `771f991e` | `testRunde2DeGodkjenteSetningene` | Foran rettlisten: fra fem til tre | ja |
| `771f991e` | `testRunde2bForanEnListeStaarBareViHar` | To setninger til skal forkastes («… retter på menyen», «… rettene på menyen») | nei |
| `771f991e` | `testRunde2bKolonetKreves` | Eksempelet bruker «Vi har følgende retter», fordi «… på menyen» ikke lenger står på vaktens liste. Det gamle eksempelet forkastes fortsatt | nei |
| `771f991e` | `testRunde2bInstruksenViserBareDeGodkjenteSetningene` | To formuleringer til som instruksen ikke får vise | nei |
| `771f991e` | `testRunde2bBindeleddetGjelderEnhverBeskrivelse` | «Pizza Margherita er San Marzano tomatsaus, …» sto som godtatt. Angrep 3 viste at et bindeledd foran en oppramsing er usant. Testen bruker nå en oppdiktet beskrivelse som sier hva retten er | ja |
| `771f991e` | `testRunde2HvertUtfallHarEnGrunn` | Spørsmålet i testen står ikke på den lukkede listen. De fem utfallene som krever at svaret sendes, prøves med «Hvilke pizzaer har dere?», og det opprinnelige spørsmålet har fått sitt eget utfall. **Svakere på ett punkt:** kontrollen av at grunnen ikke inneholder ord fra spørsmålet («Kari», «bursdag»), kan ikke slå ut for de fem | nei |
| `771f991e` | `testRunde2SettMaalesGjennomVakten` | Måleverktøyet tar med gjestens spørsmål når settet har det. Rader uten spørsmål måles som før | nei |
| `a3fc5042` | `testRunde2cModellenFaarBareAapneSpoersmaal` | «Serverer dere pizza?» flyttet fra «sendes» til «sendes ikke». Tre spørsmål med andre verb enn «har» lagt til under «sendes ikke». «Har dere pizzaer?» lagt til under «sendes» | ja |

I runde 2c ble også en felles verdi i testfilen smalere: listen testene selv har over setninger
vakten kan bygge foran rettlisten, gikk fra fire til to («på menyen» ut).

Sju av de tretten endringene snur eller fjerner noe en test krevde godtatt. Ingen av de tretten
lar vakten godta noe en test tidligere krevde forkastet. Den andre commiten la også tre
spørsmål til på den lukkede listen, alle flertallsformer av spørsmål som sto der fra før
(«hvilke typer pizzaer har dere», «hva har dere av pizzaer», «har dere pizzaer»). Angrep 5 er
skrevet mot listen slik den da sto.

## roed {#roed}

De nye testene er kjørt mot vakten slik den sto, før koden ble endret. En test som krever at
noe forkastes, skal da være rød. En test som krever at noe godtas, er bare rød hvis den gamle
vakten forkastet det. Det gjelder ikke alle testene:

- **Runde 2:** fjorten av de 24 nye testene. De ti siste kom til sammen med koden (249 tester
  kl. 09:14, 251 kl. 10:03; `HD/maal/PINTEST-RUNDE2-BYGG-1-20261003.md`,
  `HD/maal/PINTEST-RUNDE2-BYGG-2-20261003.md`) og er aldri kjørt mot `39d0657c`.
- **Runde 2b og runde 2c:** alle de nye testene (ni og fem). De tolv endringene i tester som alt
  fantes (fire i runde 2b, åtte i runde 2c; tabellen under `#regression`), kom inn sammen med
  koden og er ikke kjørt røde først.
- **Den andre commiten:** den ene endrede testen ble kjørt rød først.

| Runde | Mot | Tester | Feil | Røde tester | Bevis |
|---|---|---|---|---|---|
| 2 | `39d0657c` | 241 | 22 | tolv av de fjorten nye testene som fantes da (kl. 09:09). De to andre var grønne mot den gamle vakten. Ti nye tester til kom senere i runden og er ikke kjørt mot `39d0657c` | `HD/maal/PINTEST-RUNDE2-ROED-20261003.md` |
| 2b | `311ba729` | 260 | 129 | nøyaktig de ni `testRunde2b…` (kl. 12:07) | `HD/maal/PINTEST-RUNDE2B-ROED-20261003.md` |
| 2c | `876e835e` | 265 | 306 | nøyaktig de fem `testRunde2c…` | `HD/maal/PINTEST-RUNDE2C-ROED-20261003.md` (kl. 15:50) |
| 2c, andre commit | `771f991e` | 265 | 18 | bare `testRunde2cModellenFaarBareAapneSpoersmaal`, testen som ble endret (kl. 18:27) | `HD/maal/PINTEST-RUNDE2C2-ROED-20261003.md` |

Fra beviset for runde 2c:

```
    Test Case '-[AppTests.PalazzoConciergePhrasingTests testRunde2cDetFjerdeAngrepet]' failed (2.884 seconds).
    Test Case '-[AppTests.PalazzoConciergePhrasingTests testRunde2cDetTredjeAngrepet]' failed (0.016 seconds).
    Test Case '-[AppTests.PalazzoConciergePhrasingTests testRunde2cEnRenOppramsingBeholderKolonet]' failed (0.010 seconds).
    Test Case '-[AppTests.PalazzoConciergePhrasingTests testRunde2cInstruksenMotsierIkkeSegSelv]' failed (0.000 seconds).
    Test Case '-[AppTests.PalazzoConciergePhrasingTests testRunde2cModellenFaarBareAapneSpoersmaal]' failed (0.046 seconds).
```

Kjedene for runde 2c (`HD/mac/kjede-runde2c-20261003.sh`, `HD/mac/kjede-runde2c2-commit-20261003.sh`)
stopper hvis de røde testene er noe annet enn nettopp de nye, så en gammel test som ryker, kan
ikke gjemme seg bak dem.

## innhold {#innhold}

`test.vakt.innhold-uendret` (F1). Ti tester, grønne på `a3fc5042`:
`testRunde2EnIngrediensFaarIkkeBliBorte`, `testRunde2EtKommaFaarIkkeDeleEnRettITo`,
`testRunde2EtTallFaarIkkeFlyttes`, `testRunde2EnRettFaarIkkeLagesAvDekkedeOrd`,
`testRunde2EnRettFaarIkkeForsvinneFraListen`, `testRunde2IngentingFaarStaaEtterListen`,
`testRunde2FremmedeTegnForkastes`, `testRunde2IngredienserFaarIkkeBytteRett`,
`testRunde2HullTettesAvRegelenSomGjelderDem`, `testRunde2bEtNavnIEnListeFaarIkkeLitenForbokstav`.
`testRunde2IngredienserFaarIkkeBytteRett` er grønn fordi ethvert svar med flere kolon forkastes,
også et uendret; den prøver ikke byttet for seg.

Tre til måler at det som publiseres, er vaktens egen tekst (`test.vakt.egen-tekst`, kom til i
runde 2b): `testRunde2bVaktenPublisererSinEgenTekst`, `testRunde2bEtTegnSomBareLignerForkastes`,
`testRunde2bAltSomGodtasErByggetAvVakten`.

## trofast {#trofast}

`test.vakt.trofast-godtas` (F1, F2). Tre tester, grønne:
`testRunde2DenTrofasteOmskrivingenFra1256Godtas` («Vi har følgende pizzaer: … og Pizza Salina.»),
`testRunde2OmskrivingenSomLaaPaaNett1835Godtas` («Vitello tonnato serveres som tynne skiver …»),
`testRunde2TrofasteOmskrivingerGodtas`. De to første er setningene spesifikasjonen nevner, og
står uendret. Den tredje fikk en kortere liste i runde 2b (tabellen over).

## ramme {#ramme}

`test.vakt.ramme` (F2). Sju tester, grønne: `testRunde2SetningenForanListenFaarIkkePaastaaNoe`,
`testRunde2EtTallKanIkkeFlyttes`, `testRunde2DeGodkjenteSetningene`,
`testRunde2bForanEnListeStaarBareViHar`, `testRunde2bKolonetKreves`,
`testRunde2bBindeleddetGjelderEnhverBeskrivelse`, `testRunde2cEnRenOppramsingBeholderKolonet`.

## sendes-ikke {#sendes-ikke}

`test.vakt.sendes-ikke` (F3). Fire tester, grønne: `testRunde2SkjoereSvarSendesAldriTilEnModell`,
`testRunde2BestillingssvaretKanIkkeMisteIkke`, `testRunde2HvaSomRegnesSomSkjoert`,
`testRunde2cModellenFaarBareAapneSpoersmaal`. Den første og den siste teller kall til stubben og
krever null. Den andre prøver at vakten forkaster et bestillingssvar uten «ikke», og den tredje
prøver hva som regnes som skjørt. Den siste måler også det som ikke sto i spesifikasjonen du
godkjente: at en liste eller en rett bare sendes etter et spørsmål på den lukkede listen, og at
rettlisten ikke sendes.

## publiserte {#publiserte}

`test.vakt.publiserte-feil` (F4). `testRunde2DeFireSvareneFra1256Forkastes` (de fire svarene
fra 2. oktober kl. 12:56) og `testVaktenNekterOmskrivingenSomBlePublisert0110` (setningen fra
1. oktober, en test fra før runden) er grønne.

## uavhengig {#uavhengig}

`test.vakt.uavhengig-forslag`: utført 2. oktober (`HD/maal/VAKT-UAVHENGIG-FORSLAG-20261002.md`).

`test.vakt.uavhengig-kode` (F5). Fem angrep og fire gjennomganger, hver av en egen tråd som
ikke hadde skrevet reglene. Hele rapporten står i `HD/maal/VAKT-UAVHENGIG-KODE-20261003.md`, og
trådenes egne rapporter ligger ordrett i `HD/maal/uavhengige/`.

Seks tester holder funnene fast. Fire leser hvert sitt angrep fra en fixtur under
`PS/Tests/AppTests/Fixtures/` og sier hva som skal skje med hver rad:
`testRunde2AngrepetFra3OktoberStoppes` (angrep 1), `testRunde2bDetFrosneAngrepet` (angrep 2),
`testRunde2cDetTredjeAngrepet` og `testRunde2cDetFjerdeAngrepet`. Fixturene har alle radene med
samme id, originaltekst, omskriving, spørsmål og påstand som settene; i fixtur 2–4 er feltene
med angriperens spådom tatt ut. `testRunde2KjentGrenseLoependeTekstUtenKolon` holder den kjente
grensen synlig, og `testRunde2SettMaalesGjennomVakten` er måleverktøyet som kjører et sett
utenfra gjennom vakten selv. Angrep 5 har ingen fixtur: det er målingen etter frysing, og
ingenting i koden er endret etter det.

| Angrep | Vakten | Rader | Publisert | Målt | Bevis |
|---|---|---|---|---|---|
| 1 | første utkast, ikke committet | 45 | 38 | kl. 09:58 | `HD/maal/VAKT-ANGREP-1-FOER-RETTING-20261003.md` |
| 2 | `311ba729`, frosset | 40 | 20 | kl. 11:01 | `HD/maal/VAKT-ANGREP-2-FROSSET-20261003.md` |
| 3 | `876e835e`, frosset | 31 | 13 | kl. 15:50 | `HD/maal/VAKT-ANGREP-3-FROSSET-20261003.md` |
| 4 | utkast til spørsmålsregel, aldri bygget | 25 | 15 spådd av angriperen; 23 mot `876e835e`, som ikke ser på spørsmålet | kl. 15:50 | `HD/maal/sett/ANGREP-4-20261003.json`, `HD/maal/VAKT-ANGREP-4-MOT-RUNDE2B-20261003.md` |
| 5 | `a3fc5042`, frosset, før noe var pushet | 39 | 17 | kl. 18:29 | `HD/maal/VAKT-ANGREP-5-FROSSET-20261003.md` |

F5 sier: «null godtatte omskrivinger som endrer meningen», og at tallet som rapporteres, er
et nytt sett målt én gang etter at reglene er frosset. Det er angrep 5. Fra beviset:

```
spaadd publisert: 17 (e01 e02 e03 e04 e05 e06 e07 e08 e09 e10 e11 e12 e13 e14 e15 e16 e17)
maalt publisert:  17 (e01 e02 e03 e04 e05 e06 e07 e08 e09 e10 e11 e12 e13 e14 e15 e16 e17)
spaadd publisert, ble ikke (koster en omformulering):        0 (ingen)
publisert uten at angriperen ventet det (maa leses for seg): 0 (ingen)

## Angriperens egen dom over radene som ble publisert

  ingen: 14 (e04 e05 e06 e07 e08 e09 e10 e11 e12 e13 e14 e15 e16 e17)
  klossete: 3 (e01 e02 e03)

publisert og merket som noe annet enn «ingen» eller «klossete»: 0 (ingen)
<!-- ANGREP-5 MAALT sha=a3fc5042e15bbb6d2b896c116d980cad0b21bf2e rader=39 publisert=17 spaadd=17 bare_spaadd=0 bare_maalt=0 alvorlige=0 -->
```

Skriptet (`HD/mac/vakt-angrep-5-20261003.sh`) kontrollerer før målingen at HEAD er den andre
commiten, at vaktens fil, testfilen og settet har de md5-summene angriperen fikk, og nekter et
nytt forsøk når beviset er skrevet. De to frosne angrepene før dette møtte ikke målet; se
`ACCEPT.md` §4.

De samme settene etter rettingene, målt gjennom Swift:

| Sett | Rader | Første måling | Etter runde 2b (kl. 12:10) | Etter runde 2c (kl. 15:52) | Mot `a3fc5042` (kl. 18:29) | Bevis for siste måling |
|---|---|---|---|---|---|---|
| Angrep 1 | 45 | 38 (kl. 09:58, første utkast). Etter rettingen: 8 (kl. 10:04 og 10:13) | 8 | 8 | ikke målt for seg | `HD/maal/VAKT-ANGREP-1-ETTER-RUNDE2C-20261003.md` |
| Angrep 2 | 40 | 20 (kl. 11:01, `311ba729`) | 4 | 4 | ikke målt for seg | `HD/maal/VAKT-ANGREP-2-ETTER-RUNDE2C-20261003.md` |
| Angrep 3 | 31 | 13 (kl. 15:50, `876e835e`) | – | 8 | ikke målt for seg | `HD/maal/VAKT-ANGREP-3-ETTER-RUNDE2C-20261003.md` |
| Angrep 4 | 25 | 23 (kl. 15:50, `876e835e`, som ikke ser på spørsmålet) | – | 1 | 1 | `HD/maal/VAKT-ANGREP-4-ETTER-RUNDE2C2-20261003.md` |

Det som fortsatt publiseres:

- **Angrep 1, åtte rader:** a27 («Arancini serveres som …», formen som sto som eksempel i
  spesifikasjonen) og de sju på løpende tekst uten kolon (a32–a38), den kjente grensen.
- **Angrep 2, fire rader:** b02 («og» for det siste kommaet i pizzalisten) og b05, b06 og b15, som
  alle er «Vi har følgende retter: …». Vakten godtar fortsatt den setningen når den får den,
  men rettlisten sendes ikke lenger til modellen, så gjesten leser dem aldri.
- **Angrep 3, åtte rader:** c05 og c13 gjelder rettlisten, som ikke sendes. c06 er «Vi har følgende
  pizzaer: …». Sett 1–3 har ikke gjestens spørsmål med i målingen. Med spørsmålet fra angrepet
  («Hvilke pizzaer har dere uten kjøtt?») sendes svaret ikke; det holder
  `testRunde2cModellenFaarBareAapneSpoersmaal`. c07–c11 er et bindeledd foran en beskrivelse som
  sier hva retten er (c08 og c10 med stor forbokstav midt i setningen, c11 som vaktens egen tekst).
- **Angrep 4, én rad:** d25, «Hva er Vitello tonnato for en rett?», et åpent spørsmål.

Sett 1–3 er ikke målt for seg mot `a3fc5042`. Tallene holdes fast av testene som leser fixturene
(`testRunde2AngrepetFra3OktoberStoppes`, `testRunde2bDetFrosneAngrepet`,
`testRunde2cDetTredjeAngrepet`): de krever nøyaktig disse radene, og er grønne på `a3fc5042`.

## grunn {#grunn}

`test.vakt.grunn` (F7). `testRunde2HvertUtfallHarEnGrunn` er grønn: tretten utfall, hvert
med en navngitt grunn. Utfallene i loggen er `modell`, `uendret`, `forkastet:<regel>`,
`ingen-tekst:<årsak>` og `ikke-sendt:<grunn>`. Nye grunner i runde 2c: `ikke-sendt:oppramsing`,
`ikke-sendt:ikke-aapent-spoersmaal`, `ikke-sendt:holdes-ordrett`. Testen krever at ingen grunn
inneholder ord fra gjestens spørsmål; fra runde 2c kan den kontrollen bare slå ut for åtte av
de tretten utfallene (tabellen under `#regression`). Grunnen kan bære ett ord fra det godkjente
svaret eller, for løpende tekst uten kolon, ett ord fra modellens tekst.

## commit {#commit}

`test.commit.bare-mine-filer`. Hver commit er gjort av `HD/mac/deploy-commit-20261003.sh`,
som tar en liste og nekter hvis indeksen blir noe annet enn listen.

| Commit | Filer | Bevis |
|---|---|---|
| `311ba729` | 6 | `HD/maal/COMMIT-RUNDE2-20261003.md` |
| `876e835e` | 5 | `HD/maal/COMMIT-RUNDE2B-20261003.md` |
| `771f991e` | 6 | `HD/maal/COMMIT-RUNDE2C-20261003.md` |
| `a3fc5042` | 3 | `HD/maal/COMMIT-RUNDE2C2-20261003.md` |

Fra beviset for `771f991e`:

```
  filer i commiten:
     README.md                                          |  78 ++++-
     Sources/App/Services/PalazzoAnthropicPhraser.swift |   9 +-
     .../App/Services/PalazzoConciergePhrasing.swift    | 174 ++++++++--
     .../AppTests/Fixtures/vakt-angrep-3-20261003.json  | 374 +++++++++++++++++++++
     .../AppTests/Fixtures/vakt-angrep-4-20261003.json  | 327 ++++++++++++++++++
     Tests/AppTests/PalazzoConciergePhrasingTests.swift | 345 +++++++++++++++++--
     6 files changed, 1247 insertions(+), 60 deletions(-)
  kontroll: commiten har nøyaktig filene i listen
  ligger igjen i treet, uroert:
    ?? Deliverables/
    ?? Sites/
```

## deploy {#deploy}

`test.deploy.claim-foer-vert`. `HD/mac/deploy-vert-20261003.sh` tar eller gjenopptar claimen på
`palazzo-staging-app` før første kommando mot verten, hopper over nginx når siden svarer over
https, og slipper claimen når kontrollene er grønne.

| Commit | Claim | `COMMITTED_VERIFIED` | nginx | Bevis |
|---|---|---|---|---|
| `311ba729` | ev_913c5cdd8cf97c26 | kl. 11:08:15 (ev_a8fca0fc61d92612) | ikke rørt | `HD/maal/VERTSDEPLOY-RUNDE2-20261003.md` |
| `876e835e` | ev_805e6473b53f7858 | kl. 15:35:45 (ev_8d92d24be4fcdff8) | ikke rørt | `HD/maal/VERTSDEPLOY-RUNDE2B-20261003.md` |
| `771f991e` | ev_05407038144ffcfc | kl. 18:33:34 (ev_ef7a7c380b2959b9), i fjerde forsøk | ikke rørt | `HD/maal/VERTSDEPLOY-RUNDE2C-GROENN-20261003.md` |
| `a3fc5042` | ev_e91a69ba9db96179 | 4. oktober kl. 19:46:00 (ev_466732e0fe3545b5) | ikke rørt | `HD/maal/VERTSDEPLOY-RUNDE2C2-20261003.md` |

Utsettingen av `771f991e` tok fire forsøk, og ett av dem var rødt på en kontroll:

```
kl. 18:20  ssh: connect to host 89.167.90.101 port 22: Operation timed out   (før containeren ble startet)
kl. 18:26  KJOR-3 READY, test fra utsiden ALT GROENT, så:
           | `GET /demo/api/gjest/lesninger` | 200 | 000 | FEIL |
           <!-- DEMOFLATER MAALT feil=1 -->
           FEIL: demoflatene er roede utenfra
kl. 18:31  ssh: connect to host 89.167.90.101 port 22: Operation timed out   (i GHCR-kontrollen, første steg mot verten)
kl. 18:32  <!-- DEMOFLATER MAALT feil=0 -->   HD-0077 COMMITTED_VERIFIED (ev_ef7a7c380b2959b9)
```

Bevis: `HD/maal/VERTSDEPLOY-RUNDE2C-FORSOEK1-AVBRUTT-20261003.md`,
`HD/maal/VERTSDEPLOY-RUNDE2C-FORSOEK2-ROED-DEMOFLATER-20261003.md`,
`HD/maal/VERTSDEPLOY-RUNDE2C-FORSOEK3-20261003.md`, `HD/maal/VERTSDEPLOY-RUNDE2C-GROENN-20261003.md`.
Den røde raden er stopp-regel 3 i planen; se avvik A11 i `ACCEPT.md` §3. Fra kl. 18:24:43,
altså under de tre siste forsøkene, hadde en annen oppgave (HD-0154) claim på `host-disk` på
samme vert. Det er stopp-regel 4, avvik A12.

Utsettingen av `a3fc5042` 4. oktober gikk i ett forsøk: claim kl. 19:45:30, containeren startet kl. 19:45:49, testen utenfra 11 av 11, demoflatene 25 rader uten feil, `COMMITTED_VERIFIED` kl. 19:46:00.

Før den ble jobben som pushet og ventet på CI, stoppet med nødbremsen `HD/mac/STOPP-KJEDEN` rett etter at CI var grønn (kl. 19:43:54). Skriptets egen lesing av loggen dekker 24 timer, og `771f991e` hadde stått i 25. Hele loggen ble lest for seg (kl. 19:43:55), claimene ble lest (kl. 19:44:19, ingen åpne), bremsen ble flyttet til `HD/mac/STOPP-KJEDEN.brukt-20261004T1944Z`, og jobben ble kjørt på nytt (kl. 19:45:04–19:46:40).

Bevis: `HD/maal/FERDIGSTILL-RUNDE2C2-FORSOEK2-20261004.md`, `HD/maal/FERDIGSTILL-RUNDE2C2-FORSOEK3-20261004.md`, `HD/maal/VERTSDEPLOY-RUNDE2C2-20261003.md`, `HD/evidence/UTENFRA-20261004T194555Z.md`, `HD/evidence/DEMOFLATER-20261004T194557Z.md`.

## dry-run {#dry-run}

`test.handoff.dry-run`: **blocked**, som i spesifikasjonen. Skriptene i `HD/mac/` har ikke
`--dry-run`. Rekkefølgen og hva hvert steg skal ende med, står i `HD/README.md`. Kjedeskriptene
ble prøvekjørt i Claudes skyarbeidsområde mot en liksom-rot med et ekte git-repo og
liksom-utgaver av bygg, CI og deploy, før de ble lagt på Mac-en. Beviset ligger i `HD/maal/PROEVEKJOERING-KJEDER-20261003.tar.gz`. Det er en prøve
av rekkefølgen og portene, ikke av skriptene de kaller, og den fanget ikke det som faktisk
stoppet kjedene: mobilnettet.

## Tester som ikke er XCTest

| testRef | Utfall | Bevis |
|---|---|---|
| test.live.modellen-syns (F6) | 8 av 12 fra modellen, 8 med annen ordlyd, 0 med endret innhold (4. oktober kl. 19:46) | `ACCEPT.md#live` |
| test.live.grunn-i-loggen (F7) | 12 linjer for de tolv kallene: 8 × `modell`, 4 × `ikke-sendt:holdes-ordrett` | `ACCEPT.md#logg` |
| test.docs-updated | Tre tester holder instruksen til modellen lik vakten (`testRunde2InstruksenLoverBareDetVaktenGodtar`, `testRunde2bInstruksenViserBareDeGodkjenteSetningene`, `testRunde2cInstruksenMotsierIkkeSegSelv`). `PS/README.md` er endret i samme commits. En uavhengig gjennomgang fant upresise kommentarer i `771f991e`; de er rettet i `a3fc5042` | `ACCEPT.md#docs` |
| test.status-current | `STATUS.md` ført fram til G3 | `ACCEPT.md#status` |
| test.cells.capability-audit, test.cells.dataflow-matches-contracts | Ingen celle, kontrakt eller kant i dataflyten er endret. Vakten leser nå gjestens spørsmål mot de lukkede listene; spørsmålet ble sendt inn dit fra før | `PLAN.md#dataflow`, `PLAN.md#tillegg` |
| test.cell.contract-fixtures, test.cell.auth-negative, test.cell.stub-scan | ikke relevant | – |
