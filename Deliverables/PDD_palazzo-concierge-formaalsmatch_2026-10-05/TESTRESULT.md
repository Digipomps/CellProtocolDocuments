# TESTRESULT — PDD_palazzo-concierge-formaalsmatch

Andre utgave, 7. oktober 2026 kl. 16:45 UTC (første kl. 15:37 UTC), for **utsetting 1** (vakten svarer rett fra matchen; modellen bak og
revisoren kommer i utsetting 2 og 3). Alt under er kjørt gjennom `_losen-queue` på Mac-en (bruker kjetil), i arbeidstreet
`_worktrees/palazzoscaffold-formaalsmatch` (gren `losen/palazzo-formaalsmatch-20261007`, base `31ce1ae7`, ingen commits).
Svarene står i `HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/svar/`, loggene i `…/formaalsmatch/logg/`. Stier under er
relative til HAVEN-roten. **Ingenting er committet, pushet eller satt ut.** Rader merket `venter` er ikke kjørt ennå og
kalles ikke grønne; rader merket `utsetting 2`/`utsetting 3` hører til senere utsettinger.

## build

`swift build` rc=0 i hver kjøring. Siste: `d181-pakke7.md` (bygget på 91 s) og `d182-pakke10.md` (81 s).

## regression

Hele testmengden, kronologisk (`swift test`, alle mål, ingen test fjernet eller svekket):

| Jobb | Hva | Tester | Feil | Svar |
|---|---|---|---|---|
| `d164` | grunnlinjen på `31ce1ae7` (265 den 3. oktober; 281 med strakstiltakets tester) | 281 | 0 | `formaalsmatch/svar/d164-grunnlinje.md` |
| `d170` | pakke 2 og 3, datafil `.1` | 321 | 0 | `formaalsmatch/svar/d170-groenn-1.md` |
| `d171` | datafil `.2` | 321 | 0 | `formaalsmatch/svar/d171-dataversjon-2.md` |
| `d172b` | målingen av kommentarfeltet (4 tester til, tatt ut igjen) | 325 | 0 | `formaalsmatch/svar/d172b-maal-kommentarfelt.md` |
| `d173` | pakke 4 (matchen) | 331 | 0 | `formaalsmatch/svar/d173-pakke4.md` |
| `d177` | datafil `.3` | 331 | **1** (`testDekomponeringenErRask`, 12,3 ms per setning mot grensen 10 ms) | `formaalsmatch/svar/d177-dataversjon-3.md` |
| `d178` | datafil `.4`, samme kode | 331 | 0 (9,26 ms) | `formaalsmatch/svar/d178-dataversjon-4.md` |
| `d179` | pakke 5 og 6 (svaret og samtalen) | 373 | **2** i én test (feil forventning i testen; se `pakker/pakke5b/LES-MEG.md`) | `formaalsmatch/svar/d179-pakke5.md` |
| `d180` | pakke 5b (testen rettet) | 373 | 0 (7,85 ms) | `formaalsmatch/svar/d180-pakke5b.md` |
| `d181` | pakke 7 (posten vakten laget kan sendes tilbake; én test til) | 374 | 0 (7,42 ms) | `formaalsmatch/svar/d181-pakke7.md` |
| `d182` | pakke 10 (siden) | 374 | 0 | `formaalsmatch/svar/d182-pakke10.md` |
| `d183` | pakke 11a: det uavhengige angrepet målt én gang (197 samtaler, 233 steg) | 375 | **1** (angrepstesten: 6 brudd, to ekte — `vil-ha`/`liker` på et alkoholemne ble godtatt — og to testfeil) | `formaalsmatch/svar/d183-pakke11a.md` |
| `d184` | pakke 11b: rettingene (datafil `.5`, leseren, referansene) | 375 | 0 (angrepet: 0 brudd; 9,12 ms) | `formaalsmatch/svar/d184-pakke11b.md` |

Siste utskrift (`d184-pakke11b.md`):

```
swift build rc=0
swift test rc=0
Executed 375 tests, with 0 failures (0 unexpected) in 47.475 (47.489) seconds
MAALT tid setninger=769 sekunder=7.013 per_setning_ms=9.12
MAALT tilregnelighet 7 av 7
MAALT referanse versjon=husgraf-20261007.5 setninger=769 avvik=0
MAALT angrep steg=233 brudd=0 statuser=200:198,400:14,413:4,422:17
```

De 94 nye testene (281 → 375) er alle i nye filer (`formaalsmatch/kilde.filer`); de fire filene som finnes i HEAD og
byttes, er `PalazzoSignalGraph.swift`, `PalazzoSignalGraphMatcher.swift`, `PalazzoCommunaleFacade.swift` og
`PalazzoCommunaleProjection.swift` (md5 før bytte i `formaalsmatch/pakker/*/foer.md5`), og de tre filene for siden.
«Rød først» (`test.feil-er-tester`): se `#roed`.

## dekomponering

`PalazzoDekomponeringTests` (18 tester), `PalazzoOrdtreffTests` (6) og `PalazzoDekomponeringMaaltTests` (4), grønne i
`d170`–`d182`. Dekker `test.dekomp.ordformer`, `.nektelse`, `.formaal`, `.samme-regel` (Butlers tilfeller ordrett,
`PalazzoOrdtreffTests`), `.uten-modell` (null kall til modellstubben; også `testModellenSpoerresBareNaarOppslagetSvarerOgDaSomIAsk`).
Swift gir det samme som utgaven utenfor Swift for alle 769 setningene (`MAALT referanse … avvik=0`), med datafil `.5`
fra `d184` (ordene fra angrepet; seks setninger i korpuset leses annerledes, alle mot fasiten eller riktigere, `graf/ENDRINGSLOGG.md`).

## match

`PalazzoHusmatchTests` (10 tester), grønne fra `d173`. `test.match.en-regning`: conciergens sum er
`PalazzoSignalGraph.contributions` (`testConciergensSumErGjesteflatensFunksjon`). `test.match.forklart`, `.terskel`
(terskelen fra grafens data; en bom har en grunn; et ufullstendig søk er en bom). `test.match.avgjoerelsen`: avgjort i
grafen, null kall til modellen for tilbud, forteller og kvittering (`testTilbudGjennomFasaden`). `test.match.tid`: ikke
målt på nett ennå (`venter`); dekomponeringens del: 7,42–12,3 ms per setning på Mac-en, svinger med lasten (`d177`, `d178`,
`d180`, `d181`), grensen 10 ms i testen er Losens, ikke Kjetils.

## samtale

`PalazzoSamtaleTests` (27 tester), `PalazzoSamtaleReferanseTests` (5), `PalazzoSamtaleFasadeTests` (11) og
`PalazzoSamtaleAngrepMaaltTests` (1), grønne i `d184`. Swift lik utgaven utenfor Swift (`maaling/prototype/samtale_sim.py`)
for alle 166 samtalene med 421 steg
(`Tests/AppTests/Fixtures/formaal-samtale-referanse.json`), og for hvert steg godtar leseren av forespørselen alt som står
notert (lagt til 7. oktober kl. 15:33 UTC etter lesingen av siden, `formaalsmatch/kontroll/LES10-JS.md`).

| testRef | Test | Står |
|---|---|---|
| test.samtale.liker | `testDetHunLikerTellerMedISpoersmaaletEtterpaa` | grønn |
| test.samtale.liker-ikke | `testLikerIkkeGirKvitteringTrekkerNedOgStengerIkke` | grønn |
| test.samtale.taaler-ikke | `testTaalerIkkeGirHenvisningenOgNoteres`, `testSpiserIkkeOmEnDrikkMedAlkoholNoteresIkkeOgListenKanSendesTilbake` | grønn for utsetting 1: etter «tåler ikke» kommer henvisningen og intet tilbud. Listen med merking (bilde 4B) er F8, utsetting 2 |
| test.samtale.taaler-ikke-beskrivelsen | — | utsetting 2 (F8) |
| test.samtale.taaler-ikke-ingen-tilbud | `testStaarDetNoeGjestenUnngaarKommerVerkenTilbudEllerListe`, `testEtterNoeGjestenUnngaarGirIngenSetningTilbudEllerListe`, `testHenvisningenErOrdrettSomAskOgDetGjestenUnngaarNoteres`, `testDetGjestenUnngaarStaarNaarGrafenErNy`, `testNotaterLagetMotEnAnnenGrafversjon` | grønn for delen «ingen tilbud»; listen med merking er utsetting 2 |
| test.samtale.spiser-ikke | `testSpiserIkkeGirKvitteringOgIngenListe` | grønn for utsetting 1 (kvittering, ingen liste); listen over pizzaer med kjøttvarer er F8, utsetting 2 |
| test.samtale.spoersmaal-noterer-ikke | `testSpoersmaalOgOenskerNotererIngenting` | grønn |
| test.samtale.synlig-og-fjernbar | `testDetSomErNotertFoelgerKalleneOgTjenestenHolderIngenting`, `testFjernOgFjernAlt`, `testNoterHolderDetStrengeste`, `testMerkelappene` | grønn: tjenesten holder ingenting; siden holder listen i minnet (lest: `LES10-JS.md` punkt 3) |
| test.samtale.behold | — | venter, avhenger av veien fra siden til gjestens entitet (§2) |

## tilbud

| testRef | Test | Står |
|---|---|---|
| test.svar.formaal | `testJegVilHaNoeMedOstSierNaar` | grønn |
| test.svar.tilbud | `testJegLikerOstGirTilbudOmOsteretten`, `testTilbudGjennomFasaden` | grønn (hvert innholdsord er postens) |
| test.svar.forteller | `testPistasjGirBeggeRetteneUtenSpoersmaal` | grønn |
| test.svar.kvittering | `testLikerIkkeGirKvitteringTrekkerNedOgStengerIkke`, `testTaalerIkkeGirHenvisningenOgNoteres` | grønn |
| test.svar.ja | `testEtJaGirEnKvitteringOgEnPostIDetSomErNotert`, `testSvarVaktenByggerOgValgNaarIngenCelle` | grønn: ingen nøkkel kalles, kvitteringen kommer uten celle. På nett: `venter` |
| test.svar.ikke-alkohol | `testIngenSvarVaktenByggerHarEnDrikkMedAlkohol`, `testVinOgAlkoholGaarTilOppslagetOgNotererIngenting` | grønn (seks drikker med alkohol og tre alkoholfrie utgaver nevnes aldri) |

## graf

`PalazzoHusgrafTests` (12 tester), grønne fra `d170`. `test.graf.dekning`, `.en-kilde`, `.formaal-har-maal`, `.versjon`
(`testVersjonenErDenDatafilenHar`; på nett `venter`), `.endring-er-data` (også `testAvsnittetSvarHoldesMotGrafen`),
`.emner`. `test.graf.lager`: `maaling/rapport/` (grafen lastes fra fil; grafdatabasen målt og ikke valgt for utsetting 1).
Datafilen: `Sources/App/Resources/RestaurantConcierge/palazzo_husgraf.json`, versjon `husgraf-20261007.5`
(`graf/palazzo_husgraf-20261007.5.json`, endringene i `graf/ENDRINGSLOGG.md`; `.5` legger bare til ord etter angrepet).

## allergi

| testRef | Står |
|---|---|
| test.aldri.allergi, test.aldri.allergi-svar | utsetting 2 (F8). I utsetting 1 gir «tåler ikke» og spørsmål om allergi henvisningen `ask` gir i dag, ordrett (`testHenvisningenErOrdrettSomAskOgDetGjestenUnngaarNoteres`, `testAllergenordGrafenKjennerFaarHenvisningen`) |
| test.aldri.trygg | grønn for det vakten bygger: `testIngenTekstVaktenByggerSierAtNoeErTrygtUtenNoeEllerFrittForNoe` (ingen tekst sier «trygg», «sikker», «uten», «fri»); lageren av referansen stopper om en overskrift gjør det |
| test.aldri.vin-og-alkohol | grønn: `testVinOgAlkoholGaarTilOppslagetOgNotererIngenting`, `testModellenSpoerresBareNaarOppslagetSvarerOgDaSomIAsk` |
| test.aldri.modellen-avgjoer | utsetting 3 |

## contract

`contract/SAMTALE-UTSETTING-1.md` (andre utgave med tillegg kl. 15:33 UTC), `contract/eksempler/`.
`test.cell.contract-fixtures`: `testForespoerselenLesesEtterKontrakten`, `testFeilFormAvvises` (400),
`testInnholdSomIkkeKanBrukesAvvises` (422), `testEnForLangSetningAvvises` (413), `testKonvoluttenHarDeTrettenNoekleneOgDeNye`,
`testKildeneErPostenesOgGaarGjennomPubliseringensKontroll`, `testValgSomPekerPaaNoeSomIkkeFinnesAvvises`,
`testFeilSvarerMedStatusOgNorskTekstUtenGjestensOrd` — grønne. Eksemplene i `contract/eksempler/` er regnet for hånd før koden
(versjon `emner-v1-forslag-20261007`, terskel 0,05); `gyldig-01-tilbud.svar.json` byttes med svaret koden gir, før commit.

## auth

`test.cell.auth-negative`: de negative autorisasjonstestene på HEAD kjører i hele mengden (grønne i alle jobbene);
`testJsonLesesIkkeDypereEnnKontraktenGaar`, `testFartsgrensenGjelderDetNyeKallet` (samme grense som `ask`, felles),
`testKalletFinnesBareNaarBryterenErPaa` (uten `PALAZZO_CONCIERGE_SAMTALE=1` finnes ikke kallet, og de fem rutene er som før).
Fasaden får ingen ny tilgang til gjestens celle (ingen celle kalles i utsetting 1).

## grunn

`test.logg`: `testLoggenHarVeiOgGrunnOgAldriGjestensOrd` — grønn (`oppslag:<grunn>`, `avvist:`, `henvist:merking`,
`concierge-bom …`; aldri gjestens ord, aldri nøkkelen). På nett: `venter`.

## fasit

`maaling/korpus/`, `maaling/fasit/` (sølvfasit fra den blinde tolken; 689 rader, 517 trening og 172 holdout).
`test.maal.opake-id`: innfilene til tolken har opake id-er i stokket rekkefølge (`maaling/tolk/`, `maaling/tolk2/`).
`test.maal.lokkeduer`: utsatt (ingen dommerbenk).

## forstaaelse

`testMaaltMotSoelvfasitenTreningOgHoldoutHverForSeg` (bare samlede tall; ingen holdout-rad er lest), `d184` med `.5`
(`d181` med `.4` ga holdout 146/145/125):

```
MAALT graf=husgraf-20261007.5 fasit=solvfasit-v1 (689 rader, 517 trening og 172 holdout)
MAALT trening/alle n=517 formaal=486 (94.0 %) noder=478 (92.5 %) begge=452 (87.4 %)
MAALT holdout/alle n=172 formaal=147 (85.5 %) noder=146 (84.9 %) begge=126 (73.3 %)
MAALT tilregnelighet 7 av 7
```

`test.maal.produksjonsvei`: målingen kaller `PalazzoDekomponering` og `PalazzoSamtale` direkte, mot datafilen som settes
ut. `test.maal.holdout-urort`: `graf/ENDRINGSLOGG.md` begrunner hver endring med treningsrader; ingen holdout-rad er lest
(Book 38). `test.maal.negativer`: småprat og setninger utenfor huset er bom med grunn (`testTerskelenLesesFraGrafensDataOgEnBomHarEnGrunn`,
samtalen `bom` i referansen); allergi og trygghet går til henvisningen som i dag. Før/etter for dagens oppslag mot matchen:
`maaling/rapport/` (`venter` for tallene på nett). `test.modell-bak.gir-endring`, `test.revisor.*`: utsetting 2 og 3.

## modell-bak, foert-opp

Utsetting 3 (F3). I utsetting 1 er `interpreted_by_model` alltid `null`, og en bom får én linje i loggen uten gjestens ord
(`concierge-bom grunn=… graf=… noder=0`, `testLoggenHarVeiOgGrunnOgAldriGjestensOrd`).

## uavhengig

`test.angrep`: **kjørt**. En tråd som ikke hadde skrevet koden, skrev 197 samtaler (233 steg); settet ble frosset kl. 16:19 UTC
og målt én gang i Swift (`d183`): 6 brudd, to ekte (`vil-ha`/`liker` på et alkoholemne ble godtatt og gitt tilbake som
merkelapp) og to testfeil, og 28 av 32 allergisetninger skrevet som helse fikk liste eller tilbud. Rettet (pakke 11b: leseren,
datafil `.5`), målt på nytt (`d184`): 0 brudd, 28 av 32 henvist. Rapport med dommen for hvert funn:
`HAVEN-Deploy/_handoff/HD-0077/maal/uavhengige/ANGREP-FORMAALSMATCH-RAPPORT-20261007.md`; settet, angriperens notat og
begge målingene steg for steg ligger ved siden av. Settet kjører nå i hele testmengden (`PalazzoSamtaleAngrepMaaltTests`).
Lesinger før bygg: `formaalsmatch/kontroll/LES5-A-kompilering.md`, `LES5-B-logikk.md` (pakke 5) og `LES10-JS.md` (siden);
alle «må rettes»-punkter er rettet (pakke 5b, 7 og 10).
`test.maal.uavhengig-korpus`: utsetting 2.

## roed

`test.feil-er-tester`: de målte feilsvarene fra 4. og 5. oktober gjelder allergenveien (F8, utsetting 2) og strakstiltaket
(PDD4, satt ut som `c5058f49`). For utsetting 1 er «rød først» ført per pakke: `d179` (pakke 5) rød i én test før rettingen i
`d180`; `d177` rød i tidsmålingen før den raskere dekomponeringen. Pakke 7: feilen (en post vakten laget, som leseren avviste)
ble vist i utgaven utenfor Swift før rettingen (`samtale_sim.py` noterte `spiser-ikke bev-peroni`, `gyldig_notat` ga False),
ikke som en rød Swift-test først; Swift-testen `testSpiserIkkeOmEnDrikkMedAlkoholNoteresIkkeOgListenKanSendesTilbake` ble
skrevet sammen med rettingen og var grønn i `d181`. Pakke 11: angrepstesten var rød først (`d183`, to ekte brudd) og grønn etter
rettingene (`d184`). Ingen test er fjernet eller svekket.

## commit

`test.eksisterende-tester`: ikke kjørt ennå (`venter`, før commit, med `HAVEN-Deploy/_handoff/HD-0077/mac/testendringer-20261003.sh`).
De endrede testfilene i HEAD: ingen. Nye testfiler: ti (`formaalsmatch/kilde.filer`).

## deploy

`test.deploy.claim`: `venter` (`hd coord status` leses før forsøket). `test.deploy.kvittering`: `venter`.
`test.gui.load-time`, `test.live`: `venter` (måles på nett etter utsetting bak bryteren).

## reachability

Ikke aktuell (HTML, ikke skjelett). Hver knapp på bildene er prøvd på siden i skyen med sidens eget skript:
`formaalsmatch/kontroll/RAMMER10/vist.json` (Ja, Nei, ✕ på en post, «Fjern alt»; hva siden sendte, og hva den viste).

## dry-run

`test.handoff.dry-run`: blocked, kjent hull fra runde 2 (skriptene i `HAVEN-Deploy/_handoff/HD-0077/mac/` har ikke
tørrkjøring). Ikke rettet i denne oppgaven.
