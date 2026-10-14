# TESTRESULT — palazzo allergenvei strakstiltak

Sist oppdatert: 2026-10-06 kl. 15:18 UTC, av Losen. Tallene og utskriftene under er hentet fra bevisfilene som står ved hver test. Der en blokk er kortet ned eller satt sammen av flere linjer, er tallene de samme som i kilden. Ingenting er skrevet etter hukommelsen. Alt unntatt T10 og T11 er lest av en uavhengig tråd (K8a, `HD/maal/grunnlag-20261006/kontroll/K8A-TESTRESULTAT.md`); det den fant, er rettet her. T10 og bildene (T11) er lest av K8 (`HD/maal/grunnlag-20261006/kontroll/K8-G3.md`), før de 27 siste kallene var målt. De endelige tallene i T10 er regnet etter fra råfilene av K9 kl. 15:03–15:12 UTC (`HD/maal/grunnlag-20261006/kontroll/K9-FERDIG.md`): ingen feil i tallene. Avsnittet «Hva de publiserte svarene svarer på» under T10 er lagt til etter K9 og er ikke lest på nytt.

I dokumentet står `HD` for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold` og `PDD` for `CellProtocolDocuments/Deliverables/PDD_palazzo-allergenvei-strakstiltak_2026-10-06`. Testene er de tretten i §5 (T0–T12) i den godkjente spesifikasjonen (`PDD/FORMAALSSPEC.godkjent-G1-iterasjon1.md`).

## Kort

| Test | Hva den prøver | Utfall | Bevis |
|---|---|---|---|
| T0 | Hele testmengden før noe ble endret | 265 tester, 0 feil | `HD/maal/STRAKSTILTAK-T0B-20261006.md` |
| T1 | De 125 målte spørsmålene med et ord fra listen får henvisningen | rød før (125 av 125 fikk den ikke), grønn etter | `HD/maal/STRAKSTILTAK-KJEDE-ROED-4-20261006.md`, `HD/maal/PINTEST-STRAKSTILTAK-COMMITTET-20261006.log` |
| T2 | Hver oppføring på listen gir henvisningen; listen i Swift er lik referansen | grønn (4 tester) | samme logg |
| T3 | Merkingen kommer aldri ut | rød før (51 av 57 svar hadde merkingen), grønn etter | som T1 |
| T4 | Oppslaget og modellen spørres ikke; loggen har aldri spørsmålet | grønn (2 tester, og en tredje for at henvisningen teller mot grensen) | samme logg |
| T5 | En linje om allergener under hvert publisert svar | rød før (104 av 154 publiserte svar manglet den), grønn etter (3 tester) | som T1 |
| T6 | Kall uten ord fra listen får samme svar som før | grønn (182 kall sammenlignet) | samme logg |
| T7 | Eksempelet i spørrefeltet; de fire nettestene | grønne etter endringen. **Ikke kjørt før endringen, slik §5 sier.** Siden på nett står i `PDD/ACCEPT.md#eksempel` | `HD/maal/NETTEST-STRAKSTILTAK-122916-20261006.md` |
| T8 | Det uavhengige angrepet, målt én gang før commit | 180 spørsmål: 0 merkinger, 0 publiserte svar uten linjen. De to snarveiene var ikke med i den kjøringen | `PDD/maaling/` |
| T9 | Bygg og hele testmengden etter endringen | 280 tester, 0 feil lokalt; CI grønn, med 280 tester der også; ingen eksisterende test endret | `HD/maal/STRAKSTILTAK-COMMIT-PUSH-20261006.md` |
| T10 | De 174 kallene målt på nett etter utsettingen | Alle 174 kom fram, 147 i første kjøring og 27 i en ny: 0 merkinger, 0 publiserte svar uten linjen, alle med samme utfall som i Swift | `HD/maal/STRAKSTILTAK-MAAL-NETT-20261006.md`, `HD/maal/STRAKSTILTAK-MAAL-NETT-REST-20261006.md` |
| T11 | Skjermbilder fra nett ved siden av de godkjente bildene | står i `PDD/ACCEPT.md#bilder` | `PDD/images/nett-20261006/` |
| T12 | Dokumentene følger endringen | ja, med én feil som er min egen: `README.md` i commiten. Se `PDD/ACCEPT.md#docs` | `PDD/ACCEPT.md#docs`, `PDD/ACCEPT.md#status` |

To ting er ikke gjort slik §5 sier: de fire nettestene ble ikke kjørt før endringen (T7), og de to snarveiene var ikke med i kjøringen av angrepet (T8). Begge står under testen de gjelder. Ellers er ingen test hoppet over eller svekket. Det som ikke er prøvd, står sist i dokumentet.

## T0 — før noe ble endret {#foer}

Hele testmengden på `a3fc5042`, kjørt 6. oktober kl. 10:53–10:56 UTC mot CellProtocol `81601a6f`.

```
HEAD:  a3fc5042e15bbb6d2b896c116d980cad0b21bf2e
	 Executed 265 tests, with 0 failures (0 unexpected) in 7.063 (7.073) seconds
```

Kilde: `HD/maal/STRAKSTILTAK-T0B-20261006.md`, `HD/maal/PINTEST-STRAKSTILTAK-T0-20261006.md`.

Første forsøk (kl. 10:51) kom aldri til testene: arbeidsutsjekken av CellProtocol i `/tmp/cp-verify` på Mac-en manglet `HEAD` og `config` («fatal: not a git repository»). Hvorfor filene var borte, er ikke funnet. De to arbeidsmappene ble flyttet til side, ingenting ble slettet, og alt ble hentet på nytt (`HD/maal/PINTEST-STRAKSTILTAK-T0-FORSOEK1-20261006.md`).

## T1, T3 og T5 — røde først {#roed-foerst}

De nye testene ble lagt inn i treet mens koden sto urørt på `a3fc5042`, og hele testmengden ble kjørt. Kjøringen under er den fjerde og siste (kl. 12:21 UTC), med testfilen slik den ble committet. De 265 gamle testene var grønne i alle fire.

```
gren deploy/palazzo-demo-20260930, HEAD a3fc5042e15bbb6d2b896c116d980cad0b21bf2e, ingen fremmede endringer
	 Executed 272 tests, with 245 failures (5 unexpected) in 14.399 (14.412) seconds
roede tester: testT1MaalteSpoersmaalMedOrdFraListenFaarHenvisningen testT3MerkingenKommerAldriUtPaaGjestensSide testT5HvertPublisertSvarHarEnLinjeOmAllergener testT5LinjenPerSvartypeOgVeiInn testT5LinjenStaarNaarModellenHarFormulertSvaret
  testT1…: kastet: "T1: 125 av 125 målte spørsmål med et ord fra listen fikk ikke henvisningen: M001 M002 M009 …"
  testT3…: kastet: "T3: 51 av 57 svar hadde merkingen, og 51 var ikke henvisningen eller en avvisning (oppslaget svarte med merkingen på 48 av de 54 spørsmålene med rett og ord; publiseringen av merkesvaret ga henvisningen: false). …"
  testT5HvertPublisertSvar…: kastet: "T5: 104 av 154 publiserte svar hadde ingen linje om allergener (M002 M008 M009 …"
  testT5LinjenPerSvartypeOgVeiInn: kastet: "T5: 7 av 9 svartyper hadde ikke advarslene kontrakten sier: «Hva er Carpaccio di polpo?» (ask) | «Er det mandler i Orata al forno a legna?» (ask) | «Hvilke pizzaer har dere?» (ask) | «Hva kan jeg drikke?» (ask) | …"
  testT5LinjenStaarNaarModellenHarFormulertSvaret: kastet: "T5: linjen om allergener sto ikke først under svaret modellen formulerte, for: pizzalisten, rettbeskrivelsen"
<!-- KJEDE ROED FERDIG tester=272 roede=5 -->
```

Kilde: `HD/maal/STRAKSTILTAK-KJEDE-ROED-4-20261006.md`; hele loggen i `HD/maal/PINTEST-STRAKSTILTAK-ROED-122126-20261006.log`. De tre første kjøringene: `HD/maal/STRAKSTILTAK-KJEDE-ROED-20261006.md`, `HD/maal/STRAKSTILTAK-KJEDE-ROED-2-20261006.md`, `HD/maal/STRAKSTILTAK-KJEDE-ROED-3-20261006.md`.

Tallet 272 er de 265 gamle testene og de sju i den første nye testfilen. De to andre testfilene (ordlisten og angrepet) kan ikke bygges uten den nye koden, og er derfor ikke vist røde.

**Et funn om XCTest.** I de røde kjøringene førte XCTest bare 30, 28, 30 og 26 av de 125 feilmeldingene i T1, alltid de første radene, og to av 48 ble borte i T3 i de tre første. Årsaken er ikke funnet. Testene samler derfor avvikene selv og kaster ett sammendrag til slutt; det kom fram i hver kjøring. «245 failures» over er altså et tall XCTest førte, ikke antall avvik.

Etter endringen (det committede treet `c5058f49`, kl. 12:31 UTC):

```
PalazzoAllergiHenvisningTests testT1MaalteSpoersmaalMedOrdFraListenFaarHenvisningen passed (0.113 seconds).
PalazzoAllergiHenvisningTests testT3MerkingenKommerAldriUtPaaGjestensSide passed (0.508 seconds).
PalazzoAllergiHenvisningTests testT5HvertPublisertSvarHarEnLinjeOmAllergener passed (1.375 seconds).
PalazzoAllergiHenvisningTests testT5LinjenPerSvartypeOgVeiInn passed (0.042 seconds).
PalazzoAllergiHenvisningTests testT5LinjenStaarNaarModellenHarFormulertSvaret passed (0.015 seconds).
```

Kilde: `HD/maal/PINTEST-STRAKSTILTAK-COMMITTET-20261006.log`.

## T2 — listen {#listen}

Fire tester i `PS/Tests/AppTests/PalazzoAllergiOrdlisteTests.swift`. Listen i Swift holdes mot referansen (`HD/maal/grunnlag-20261006/ordliste_strakstiltak.py`, utgave 6: 134 oppføringer og tre unntak) gjennom fiksturen `PS/Tests/AppTests/Fixtures/allergi-ordliste-utgave6-20261006.json`, som er skrevet ut av referansen.

```
PalazzoAllergiOrdlisteTests testT2HverOppfoeringGirHenvisningen passed (0.137 seconds).
PalazzoAllergiOrdlisteTests testT2ListenErReferansenOppfoeringForOppfoering passed (0.000 seconds).
PalazzoAllergiOrdlisteTests testT2OrdSomSkalOgIkkeSkalTreffe passed (0.003 seconds).
PalazzoAllergiOrdlisteTests testT2SwiftTrefferSomReferansenPaaHvertMaaltSpoersmaal passed (0.038 seconds).
```

Kilde: `HD/maal/PINTEST-STRAKSTILTAK-COMMITTET-20261006.log`.

Listen er utgave 5 med de to rettelsene fra G1, punkt 4, og ingenting annet: «amming» treffer bare som eget ord, og unntaket «reactivat» er ute. Følgen av den første: «ammingen», «amminga», «fullamming» og «ammingsperioden» treffer ikke.

## T3 — ingen merking ut {#merking}

Testen `testT3MerkingenKommerAldriUtPaaGjestensSide`: publiseringen gitt oppslagets merkesvar gir henvisningen; de tre målte spørsmålene listen ikke fanger, og som fikk merkingen før («Are there chestnuts in the Agnello arrosto?», «Har dere donuts til Arancini?», «In a nutshell, what is Vitello tonnato?»), gir henvisningen; og hver av de 18 rettene sammen med «chestnuts», «donuts» og «nutshell» gir aldri «er merket med». Rød før og grønn etter: se over.

I målingen av de 310 målte kallene gjennom koden (uten modell) gikk merkingene fra 25 til 0:

```
før (a3fc5042):   henvisning=0   avvist=156 publisert_med_linje=25  publisert_uten_linje=104 merking_ut=25
etter (endringen): henvisning=128 avvist=81  publisert_med_linje=101 publisert_uten_linje=0   merking_ut=0
```

Kilde: `HD/maal/STRAKSTILTAK-SVAR-FOER-20261006.md`, `HD/maal/STRAKSTILTAK-SVAR-ETTER-20261006.md`. Linjene er satt sammen av sluttlinjen i hver fil.

«Etter» ble målt kl. 11:37 UTC på arbeidstreet, før commit, og målingen fører ikke md5 for kodefilene. Det som binder den til `c5058f49`: kodefilene ble lagt inn fra pakken med md5 kontrollert kl. 11:35 (`HD/maal/STRAKSTILTAK-KJEDE-GROENN-1-20261006.md`), commiten har filene med samme md5 (`HD/maal/STRAKSTILTAK-COMMIT-PUSH-20261006.md`), testene på det committede treet holder de samme kallene fast (T1, T3, T5 og T6), og på nett ga kallene som kom fram, samme utfall som her (T10).

## T4 — modellen og loggen {#logg}

```
PalazzoAllergiOrdlisteTests testT4HenvisningenSpoerVerkenOppslagetEllerModellenOgLoggenHarAldriSpoersmaalet passed (0.016 seconds).
PalazzoAllergiOrdlisteTests testT4LogglinjenOgKodene passed (0.000 seconds).
PalazzoAllergiOrdlisteTests testHenvisningenFoeresIAktivitetenOgTellerMotGrensen passed (0.030 seconds).
```

Kilde: `HD/maal/PINTEST-STRAKSTILTAK-COMMITTET-20261006.log`. De to første er T4 slik §5 beskriver den. Den tredje prøver det S1 sier om at kallet teller mot grensen på 30 per ti minutter og føres i aktiviteten som andre kall.

Vertens logg etter utsettingen, lest kl. 14:22 UTC (`HD/maal/VAKTLOGG-STRAKSTILTAK-ETTER-20261006.md`): 156 linjer siden utgaven startet kl. 13:19:12. Hver linje har bare handlingen og utfallet; ingen har noe av et spørsmål.

```
2026-10-06T13:21:26.674972574Z [ NOTICE ] concierge-formulering handling=ask utfall=allergi-henvisning:ordliste
## antall linjer: 156
      105 utfall=allergi-henvisning:ordliste
       12 utfall=ikke-sendt:ikke-aapent-spoersmaal
        9 utfall=ikke-sendt:ikke-besvart
        7 utfall=modell
        6 utfall=ikke-sendt:kontakt
        4 utfall=ikke-sendt:holdes-ordrett
        4 utfall=ikke-sendt:flere-kolon
        3 utfall=ikke-sendt:handling
        3 utfall=allergi-henvisning:merking
        2 utfall=ikke-sendt:spoersmaal
        1 utfall=ikke-sendt:forbehold:ingen
```

De 156 linjene er de to kallene i utsettingens egen kontroll, de 147 kallene i målingen som kom fram i første kjøring, og sju kall fra nettleseren da skjermbildene ble tatt. Kl. 14:53 var det 183 linjer: de 27 kallene i den nye kjøringen kom i tillegg (`HD/maal/STRAKSTILTAK-LEST-ETTER-20261006.md`). De 108 henvisningene er de 106 i målingen og spørsmålet om hvete, som ble stilt to ganger for skjermbildet.

## T5 — linjen om allergener {#linjen}

Tre tester: hvert publisert svar blant de målte kallene har en linje om allergener; hver svartype har sin linje først blant advarslene gjennom veien den kommer inn (spørrefeltet, snarveien til menyen, snarveien til drikke); og linjen står også når modellen har formulert svaret (pizzalisten og en rettbeskrivelse, med en stubb for modellen). Rød før og grønn etter: se over.

## T6 — vanlige spørsmål {#uendret}

```
PalazzoAllergiHenvisningTests testT6SpoersmaalUtenOrdFraListenFaarSammeSvartekstSomFoer passed (1.323 seconds).
```

Kilde: `HD/maal/PINTEST-STRAKSTILTAK-COMMITTET-20261006.log`. Testen holder 182 kall mot svarene koden ga på `a3fc5042` (fiksturen `PS/Tests/AppTests/Fixtures/allergi-henvisning-foer-20261006.json`): de 185 målte kallene listen ikke treffer, minus de tre som fikk merkingen før. HTTP-kode, svartekst, status, vei og antall kilder er like; for avvisninger også grunnkoden og advarslene. Testen kjører uten modell.

Hva listen koster av vanlige spørsmål, er målt i angrepet (T8): 3 av 60 vanlige spørsmål fikk henvisningen, og 13 av 20 vanlige som var skrevet med ord en ordliste lett tar feil av.

## T7 — eksempelet og nettestene {#eksempel-tester}

Én linje er endret i `PS/Public/palazzo/index.html`:

```
-  … placeholder="For eksempel: Hvilke retter kan passe uten melk?"></textarea>
+  … placeholder="For eksempel: Hvilke pizzaer har dere?"></textarea>
```

De fire testene i `PS/Tests/Web/concierge-question-context.test.cjs`, etter endringen:

```
# tests 4
# pass 4
# fail 0
```

Kilde: `HD/maal/NETTEST-STRAKSTILTAK-122916-20261006.md`, og to kjøringer før den (`HD/maal/NETTEST-STRAKSTILTAK-113540-20261006.md`, `HD/maal/NETTEST-STRAKSTILTAK-122240-20261006.md`). Filene fører verken tid eller md5. At de er kjørt etter at endringen var lagt inn, står i kjedens logg: trinnet legger inn `Public/palazzo/index.html` med md5 `c638fc69ac57797fa44267441a4f1292` før det kjører dem (`HD/maal/STRAKSTILTAK-KJEDE-GROENN-3-20261006.md`, trinn 2 og 4).

**Avvik fra §5:** testene skulle kjøres før og etter. Før endringen ble de ikke kjørt i dag. Det nærmeste som finnes, er CI for `a3fc5042` 4. oktober, som kjører dem som eget steg og var grønn (`HD/maal/PUSH-RUNDE2C2-20261003.md`: `conclusion=success sha=a3fc5042e15bbb6d2b896c116d980cad0b21bf2e`). CI kjørte dem igjen for `c5058f49`. Siden på nett: `PDD/ACCEPT.md#eksempel`.

## T8 — angrepet {#angrepet}

Settet, målingen og tallene ligger i `PDD/maaling/`. Kort: en tråd som ikke hadde sett listen, koden eller det første blinde settet, skrev 180 spørsmål i fem grupper. Settet ble frosset kl. 12:22 UTC, før jeg hadde lest spørsmålene, og målt én gang gjennom fasaden kl. 12:24–12:27 UTC, før commit.

```
rader: 180
  henvisningen (grunnkode allergy-referral):       81
  avvist av oppslaget, som før tiltaket:           62
  publisert, med en linje om allergener:           37
  PUBLISERT UTEN en linje om allergener:           0
  EN MERKING UT:                                   0
per gruppe:
  A:                     henvisning 50, avvist 6, publisert_med_linje 4
  B:                     henvisning 3, avvist 36, publisert_med_linje 21
  C:                     henvisning 9, avvist 8, publisert_med_linje 3
  D:                     henvisning 6, avvist 5, publisert_med_linje 9
  E:                     henvisning 13, avvist 7
```

Kilde: `HD/maal/STRAKSTILTAK-ANGREP-BLIND2-20261006.md`. Ingen av de to tingene som skulle stoppe meg, ble funnet.

**Avvik fra §5:** der står det at de to snarveiene måles som to faste kall sammen med angrepet. Kjøringen hadde de 180 spørsmålene og ikke snarveiene. De to snarveiene er målt gjennom samme kode i målingen av de 310 kallene kl. 11:37 (begge publisert med en linje om allergener), de prøves i T5, og de er målt på nett (T10). Angrepet står igjen som test (`PS/Tests/AppTests/PalazzoAllergiAngrepTests.swift`), som holder utfallet for hver av de 180 radene fast.

## T9 — bygg og hele testmengden etter endringen {#build}

Det committede treet `c5058f49640fc71a2b684713e7406add9e81b183`, kl. 12:31 UTC:

```
	 Executed 280 tests, with 0 failures (0 unexpected) in 15.549 (15.590) seconds
      swift build rc=0
      swift test rc=0
```

CI (Linux, samme tester og nettestene, og imaget):

```
conclusion=success sha=c5058f49640fc71a2b684713e7406add9e81b183 url=https://github.com/DiMy-io/PalazzoScaffold/actions/runs/37463952874
IMAGE=ghcr.io/dimy-io/palazzoscaffold:sha-c5058f49640fc71a2b684713e7406add9e81b183
```

Kilde: `HD/maal/STRAKSTILTAK-COMMIT-PUSH-20261006.md`. CI var grønn første gang. CI-loggen har samme tall: «Executed 280 tests, with 0 failures», og for nettestene «# pass 4», «# fail 0» (`HD/maal/CI-TESTTALL-STRAKSTILTAK-20261006.md`).

### Ingen eksisterende test er endret {#regression}

Lest fra git (`HD/maal/COMMIT-STRAKSTILTAK-20261006.md`): commiten har tolv filer. Fire er endret, og ingen av dem er en test. Åtte er nye.

```
 M Public/palazzo/index.html
 M README.md
 M Sources/App/Controllers/PalazzoCommunaleFacade.swift
 M Sources/App/Controllers/PalazzoCommunaleProjection.swift
?? Sources/App/Services/PalazzoAllergiHenvisning.swift
?? Tests/AppTests/Fixtures/allergi-angrep-blind2-20261006.json
?? Tests/AppTests/Fixtures/allergi-henvisning-foer-20261006.json
?? Tests/AppTests/Fixtures/allergi-henvisning-maalt-20261006.json
?? Tests/AppTests/Fixtures/allergi-ordliste-utgave6-20261006.json
?? Tests/AppTests/PalazzoAllergiAngrepTests.swift
?? Tests/AppTests/PalazzoAllergiHenvisningTests.swift
?? Tests/AppTests/PalazzoAllergiOrdlisteTests.swift
kontroll: commiten har nøyaktig filene i listen
```

265 tester før, 280 etter: 15 nye (7 + 7 + 1), ingen fjernet.

## T10 — målt på nett {#nett}

Etter utsettingen ble de 174 kallene i `HD/mac/spoersmaal-strakstiltak-nett-20261006.txt` sendt fra Mac-en mot `https://palazzo.digipomps.org/palazzo/api/`, 27 per ti minutter, kl. 13:21–14:22 UTC. Listen er de 21 fra 5. oktober, kallene med hele konvolutten (25 som ikke alt var med, også de to snarveiene), de 28 fra 6. oktober (27 som ikke alt var med), de 89 fra det første blinde settet og tolv andre målte kall.

**147 av 174 kom fram i første kjøring.** De 27 kallene i den sjette bolken kom aldri fram: fra kl. 14:11:51 UTC feilet skriptets forsøk med «Could not resolve host», to forsøk per kall, i rundt ett minutt. Mac-en fikk ikke slått opp vertsnavnet. Skriptet førte dem som «INGEN KONTAKT» og kalte målingen ufullstendig.

```
kall: 174 av 174 i listen
  henvisningen (grunnkode allergy-referral):       106
  avvist av oppslaget:                             9
  publisert, med en linje om allergener:           32
  PUBLISERT UTEN en linje om allergener:           0
  EN MERKING UT:                                   0
  annet (ikke HTTP 200, eller ukjent status):      0
  INGEN KONTAKT (kallet kom aldri fram):           27
kall som fikk 429 og ble sendt igjen etter ventetiden: 0
<!-- MAAL-NETT UFULLSTENDIG revisjon=c5058f49640fc71a2b684713e7406add9e81b183 kall=174 henvisning=106 avvist=9 publisert_med_linje=32 publisert_uten_linje=0 merking_ut=0 annet=0 ingen_kontakt=27 -->
```

Kilde: `HD/maal/STRAKSTILTAK-MAAL-NETT-20261006.md`; råsvarene i `HD/maal/nett-ut/spoersmaal-strakstiltak-nett-20261006-20261006T132126Z.jsonl`. Av de 32 publiserte svarene har 26 den nye linjen først blant advarslene. De seks andre er rettlisten, som har sin egen linje om allergi fra før og ikke får noen ny.

**De 27 ble målt på nytt kl. 14:52:58–14:53:01 UTC**, med andre utgave av skriptet (`HD/mac/strakstiltak-maal-nett-2-20261006.sh`) og listen `HD/mac/spoersmaal-strakstiltak-nett-rest-20261006.txt`. Alle kom fram:

```
kall: 27 av 27 i listen
  henvisningen (grunnkode allergy-referral):       20
  avvist av oppslaget:                             3
  publisert, med en linje om allergener:           4
  PUBLISERT UTEN en linje om allergener:           0
  EN MERKING UT:                                   0
  annet (ikke HTTP 200, eller ukjent status):      0
  INGEN KONTAKT (kallet kom aldri fram):           0
<!-- MAAL-NETT FERDIG revisjon=c5058f49640fc71a2b684713e7406add9e81b183 kall=27 henvisning=20 avvist=3 publisert_med_linje=4 publisert_uten_linje=0 merking_ut=0 annet=0 ingen_kontakt=0 -->
```

Kilde: `HD/maal/STRAKSTILTAK-MAAL-NETT-REST-20261006.md`; råsvarene i `HD/maal/nett-ut/spoersmaal-strakstiltak-nett-rest-20261006-20261006T145258Z.jsonl`.

**I alt, 174 kall:** 126 henvisninger, 12 avvist (11 med grunnkoden `requires-human-review`, 1 med `requires-norwegian-review`), og 36 publisert med en linje om allergener. Av de 36 har 30 den nye linjen først blant advarslene (7 under én rett, 4 under flere retter, 19 under lister og svaret om bordbestilling), og 6 er rettlisten med sin egen linje. Ingen publiserte svar manglet linjen, og ingen merking kom ut. Regnet av de to råfilene.

**Hva de publiserte svarene svarer på.** Ti av de 36 publiserte svarene er på spørsmål om helse eller om noe gjesten ikke tåler, etter min lesing av spørsmålene: `M010`, `M012`, `M029`, `M135`, `M215`, `M233`, `M274`, `M286`, `M288` og `M307`. De fikk en rettbeskrivelse, pizzalisten, rettlisten eller svaret om bordbestilling, alle med en linje om allergener som viser til personalet. Eksempel: `M286` «Sønnen min blir syk av pistasj. Hva kan vi bestille?» fikk svaret om bordbestilling. Det er regel 3 slik spesifikasjonen beskriver den, og det samme utfallet som i Swift før commit. Se `PDD/ACCEPT.md`, «Hva listen ikke fanger».

**Mot Swift.** Hvert kall som kom fram, er holdt mot svaret det samme kallet ga gjennom koden i Swift kl. 11:37 UTC (uten modell): samme utfall, samme advarsler og samme status, grunnkode og antall kilder for alle. Fire svar var formulert av modellen, alle med en av formene vakten tillater, og med linjen om allergener først blant advarslene:

```
M143 | Hva er Carpaccio di polpo?
   godkjent svar: Carpaccio di polpo: Blekksprutcarpaccio med kokt potet, stangselleri, olivenolje og sitron.
   modellen:      Carpaccio di polpo er blekksprutcarpaccio med kokt potet, stangselleri, olivenolje og sitron.
M197 | Hvilke pizzaer har dere?
   godkjent svar: Pizzaene i kunnskapsgrunnlaget er: Pizza Margherita, Pizza Siciliana, Pizza Vulcano, Pizza Tartufo "Umami", Pizza Salina.
   modellen:      Vi har disse pizzaene: Pizza Margherita, Pizza Siciliana, Pizza Vulcano, Pizza Tartufo "Umami", Pizza Salina.
M081 | Fortell om Vitello tonnato.
   modellen:      Vitello tonnato er tynne skiver kalveroastbiff med tunfiskmajones, ristet kalvebrissel og asparges.
M150 | Hva er Formaggi misti?
   modellen:      Formaggi misti er utvalg av oster fra små utvalgte gårder i Italia med tilbehør.
```

Kilde: `HD/maal/STRAKSTILTAK-NETT-MOT-SWIFT-20261006.md` for begge kjøringene, 174 kall (første kjøring alene: `HD/maal/STRAKSTILTAK-NETT-MOT-SWIFT-1-20261006.md`). Laget med `HD/maal/grunnlag-20261006/sammenlign_nett.py`.

**En feil i råfilen fra første kjøring.** For de 27 kallene som ikke kom fram, har råfilen `"http": 0` sammen med et svar som ikke er deres: skriptet lot filen med forrige svar stå. Oppsummeringen regnet riktig, fordi den ser på `http` først, men den som leser råfilen uten å gjøre det, ser 27 svar som aldri kom. Andre utgave av skriptet (`HD/mac/strakstiltak-maal-nett-2-20261006.sh`) tømmer filen før hvert kall.

## Det som ikke er prøvd

- **Henvisningen når oppslaget ikke kan nås: ett tilfelle er prøvd etter G3.** Regel 1 står foran kallet til cellen. Etter rekkefølgen i koden får et spørsmål med et listeord derfor henvisningen (HTTP 200) også da, der andre spørsmål får 503 eller 403. Spesifikasjonen sier ikke noe om det. Da dokumentet ble lagt fram, prøvde ingen test det. Etter G3 holder én test det fast for ett tilfelle: identitetshvelvet er borte (se «Etter G3» sist). De andre måtene veien til cellen kan svikte på (avvist tilgang, et korpus som ikke er pakket med, andre feil), er ikke laget hver for seg.
- **Selve byttet tilbake.** Veien tilbake (`HD/mac/tilbake-vert-20261006.sh`) er tørrkjørt to ganger, og forutsetningene er lest på verten. Byttet tilbake til `a3fc5042` er aldri kjørt.
- **De røde kjøringene for ordlisten og angrepet.** De to testfilene kan ikke bygges uten den nye koden (se over).
- **Nettestene før endringen**, og **snarveiene i kjøringen av angrepet**: se T7 og T8.
- **Modellen i XCTest.** Testene bruker en stubb for modellen. Den virkelige modellen er bare med i målingen på nett.

## Etter G3 — testen som holder avvik 4 fast {#avvik4}

Lagt til 6. oktober 2026 kl. 22:58 UTC, av Losen, og rettet 7. oktober 2026 etter en uavhengig kontroll (se «Rettet etter kontrollen» sist). Dokumentet over er slik det ble lagt fram ved G3, bortsett fra første kule under «Det som ikke er prøvd». Den ble skrevet om etter G3: overskriften er ny, og «ingen test prøver det» er byttet mot det testen dekker og ikke dekker. Filen slik den sto ved G3, ligger urørt i `PDD/TESTRESULT.ved-G3-20261006.md`.

Kjetil valgte ved G3 «La stå, med en test (Recommended)» for avvik 4 (`PDD/STATUS.md`). Testen er `PS/Tests/AppTests/PalazzoAllergiHenvisningUtenOppslagTests.swift`, én test: `testListeordFaarHenvisningenOgsaaNaarOppslagetIkkeKanNaas`. Den setter opp sin egen fasade under `/utenoppslag`, uten modell, og tar bort identitetshvelvet mens appen er oppe, så fasaden ikke kan hente husets identitet. Et vanlig spørsmål («Hvilke pizzaer har dere?») skal da få 503 med `error` satt, uten svar og uten grunnkode (teksten i feilmeldingen prøves ikke), og et spørsmål med et listeord («Er det hvete i Carpaccio di polpo?») skal få henvisningen, lik den det fikk før hvelvet ble tatt bort, med én logglinje. Hvelvet settes tilbake på hver vei ut, og testen krever at det vanlige spørsmålet får svar igjen etterpå.

| Trinn | Når (UTC) | Utfall | Bevis |
|---|---|---|---|
| Uavhengig kontroll av testen, skriptet, setningen i `README.md` og commit-meldingen, før noe ble committet (K10) | 21:59–22:08 | K10 fant ingen feil i testen slik den sto da (md5 `048e5071cff122d696dc753ac46980e0`), og skrev at sammenligningen av de to svarene holder. I utgaven etter K10s rettelser (md5 `0ea7f8ea0e642ee629f2938ae948b18a`) feilet den kl. 22:12. Fem funn i skriptet og ordlyden (ett utelatt, fire upresise); alle rettet før commit. Utgaven som ble committet (md5 `65489c32aa58b2a876afa489a3a17342`), er laget etter K10 | `HD/maal/grunnlag-20261006/kontroll/K10-AVVIK4.md` |
| Rød: testen mot en fasade der henvisningen spør oppslaget først (én linje satt inn i arbeidstreet, tatt ut igjen) | 22:15 | 281 tester, 9 feil, alle i den nye testen; ingen annen test rød | `HD/maal/STRAKSTILTAK-AVVIK4-ROED-3-20261006.md` |
| Grønn: testen og `README.md` mot koden slik den står | 22:16 | 281 tester, 0 feil | `HD/maal/STRAKSTILTAK-AVVIK4-GROENN-2-20261006.md` |
| Commit `31ce1ae7fd648cdbbfd51c59ce107cbc11bc5508`: testfilen og `README.md`, ingenting annet. Hele testmengden på det committede treet | 22:17 | 2 filer, 169 linjer inn og 2 ut; 281 tester, 0 feil | `HD/maal/STRAKSTILTAK-AVVIK4-COMMIT-PUSH-2-20261006.md`, `HD/maal/PINTEST-STRAKSTILTAK-AVVIK4-COMMITTET-20261006.log` |
| Push og CI | 22:17–22:52 | CI grønn (https://github.com/DiMy-io/PalazzoScaffold/actions/runs/37539688672). Imaget er bygget av CI. Testtallet i CI er ikke lest. **Ingenting er satt ut.** Da dette ble skrevet, var nett sist lest kl. 14:53 UTC (`c5058f49`). Det ble lest på nytt 7. oktober kl. 01:57 UTC og viste det samme | samme fil, `HD/maal/PUSH-STRAKSTILTAK-AVVIK4-20261006.md` og `HD/maal/STRAKSTILTAK-LEST-NATT-20261007.md` |

De ni feilene i den røde kjøringen, fra beviset. Navnet på testen foran hver linje er tatt bort, og halen ` - {` på sju av dem. Den andre linjen er kortet med «…»:

```
XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
XCTAssertEqual failed: ("{"error":true,"reason":"Palazzo Communale er midlertidig utilgjengelig."}") is not equal to ("{"answer":"Dette er ikke bekreftet i kunnskapsgrunnlaget. …
XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.string("allergy-referral"))")
XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.string("requires-review"))")
XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.string("blocked"))")
XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.bool(true))")
XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(0))")
XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.string("Dette er ikke bekreftet i kunnskapsgrunnlaget. Jeg kan ikke gi et sikkert svar. Spør vertskapet, særlig om allergener, krysskontakt, åpningstider eller dagens tilgjengelighet."))")
XCTAssertEqual failed: ("[]") is not equal to ("["notice concierge-formulering handling=ask utfall=allergi-henvisning:ordliste"]")
```

**Det som gikk galt underveis. Min feil.** Første grønne kjøring (kl. 22:12, `HD/maal/STRAKSTILTAK-AVVIK4-GROENN-20261006.md`) var ikke grønn: 281 tester, 1 feil, i min egen test. Jeg sammenlignet to hele svar med `XCTAssertEqual` på `ValueType`-objekter, og kjernens `==` svarer usant for sammensatte verdier med likt innhold. Fellen står i lærdomsregisteret fra 9. september (`lesson.valuetype-equality-false-for-objects`). Jeg slo ikke opp lærdommene før jeg skrev denne lille testen. Kontrollen (K10) leste sammenligningen og skrev at den holder; den kunne ikke kjøre testen. Skriptet stoppet commiten, fordi det krever et grønt bevis for nøyaktig den filen som skal inn. Testen sammenligner nå kanonisk JSON (sorterte nøkler), og rød og grønn ble kjørt på nytt med den rettede filen før commit. Fra commiten ble stoppet (kl. 22:14:10 UTC) til den gikk (kl. 22:17:12 UTC), tok det tre minutter. De fire kjøringene før de rettede ligger som bevis: rød kl. 21:59 (`HD/maal/STRAKSTILTAK-AVVIK4-ROED-20261006.md`), rød på nytt kl. 22:11 etter at testen, skriptet og teksten i `README.md` var rettet etter K10 (`HD/maal/STRAKSTILTAK-AVVIK4-ROED-2-20261006.md`), den grønne som var rød kl. 22:12 (`HD/maal/STRAKSTILTAK-AVVIK4-GROENN-20261006.md`), og commiten som ble stoppet kl. 22:14 (`HD/maal/STRAKSTILTAK-AVVIK4-COMMIT-PUSH-20261006.md`).

**Hva testen ikke dekker.** Bare ett av tilfellene er laget: hvelvet er borte, og fasaden får 503 før cellen er spurt. Avvist tilgang (403), et korpus som ikke er pakket med (503) og andre feil fra cellekallet ligger i samme del av fasaden, som henvisningen aldri kaller, men er ikke laget hver for seg. Kommentaren øverst i testen og setningen i `PS/README.md` sier det samme.

Tallene i tabellen er hentet fra bevisfilene. Avsnittet var ikke lest av en uavhengig tråd da det ble skrevet. Det ble lest natt til 7. oktober (K3); se under.

### Rettet etter kontrollen (7. oktober 2026) {#rettet-k3}

Kontrolltråden K3 leste dette tillegget, tillegget i `PDD/ACCEPT.md`, loggen i `PDD/STATUS.md` og avsnittet i `HD/README.md` mot svarfilene, bevisfilene, testen og skriptet, 7. oktober kl. 00:23–00:31 UTC. Den fant ingen alvorlig feil, én liten feil, åtte upresise steder og to bagateller. Tallene, klokkeslettene, commiten og de ni feilene stemte med svarfilene. Rapporten: `HD/maal/grunnlag-20261007/kontroll/K3-STRAKSTILTAK.md`. Filen slik den sto før rettingen: `HD/maal/grunnlag-20261007/kontroll/k3/foer/TESTRESULT.md`.

| Sto | Står nå | Hvorfor |
|---|---|---|
| «De tre første kjøringene ligger som bevis» | Fire kjøringer, hver med klokkeslett og fil | Det var fire før de rettede. Filen jeg kalte den tredje, var den fjerde |
| «Det kostet rundt fem minutter» | Tre minutter, fra commiten ble stoppet til den gikk | Regnet av svarfilene: 3 min 2 s |
| «skal da få 503 med feilmeldingen» | 503 med `error` satt, uten svar og uten grunnkode | Testen prøver ikke teksten i feilmeldingen |
| «Ingen feil i testen» (K10) | K10 leste en tidligere utgave, og skrev at sammenligningen som siden feilet, holder | Utgaven som ble committet, er laget etter K10. Den var ikke lest av en uavhengig tråd før K3 leste den 7. oktober; K3 fant ikke annet i den enn det som står i rapporten |
| «på nett står fortsatt `c5058f49`» | Sist lest kl. 14:53 UTC da det ble skrevet. Lest på nytt 7. oktober kl. 01:57 UTC: `c5058f49` | Det var sluttet av at ingen utsetting var kjørt, ikke lest |
| «CI grønn», uten mer | Testtallet i CI er ikke lest | Svaret fra CI har bare at kjøringen lyktes |
| Kulen under «Det som ikke er prøvd» hadde mistet «Spesifikasjonen sier ikke noe om det» | Setningen står igjen | `PDD/FORMAALSSPEC.md` har samme md5 som den godkjente kopien (`88a43b6400f8711ef0b65db8a427de70`), og sier fortsatt ikke noe om det |
| «ordrett fra beviset» om de ni feilene | Sagt hva som er tatt bort | Navnet på testen og halen ` - {` var tatt bort uten at det sto |
| Ikke nevnt | Testen bruker sin egen fasade under `/utenoppslag`, uten modell | Det sto i testen, ikke her |
| I `HD/README.md`: `commit` krever bevis «som bærer md5 for nøyaktig de filene som skal inn» | Det røde beviset bærer testfilens md5, det grønne også md5 for `README.md` | Skriptet krever ikke md5 for `README.md` i det røde beviset |

Tillegget sier «kl. 22:58 UTC». Filen har tiden 23:02 UTC.

Rettelsene i denne tabellen ble lest av en ny uavhengig tråd (K6) 7. oktober kl. 02:18–02:24 UTC: ingen alvorlig feil, ingen feil, og fem upresise steder, tre av dem bagateller (`HD/maal/grunnlag-20261007/kontroll/K6-STRAKSTILTAK-RETTING.md`). De fem er rettet her, i `PDD/ACCEPT.md`, i `PDD/STATUS.md` og i `HD/README.md`. Den siste rettingen er ikke lest av andre.
