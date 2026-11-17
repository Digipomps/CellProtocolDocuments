# Astra: motsvar til nattens formålsmatching

**Dom: NEEDS_ONE_BOUNDED_CORRECTION. Gjennomgang fullført med dokumenterte begrensninger.** Den sterkeste støttede konklusjonen er at den valgte matcheren treffer Losens konstruerte utviklingssett bedre enn den lokale nøkkelordsbaselinen: 8/50 → 20/50. Dette er reprodusert. Det er ikke en uavhengig sluttmåling, og verken «lekker ikke» eller «resten er registerets problem» holder. Grunnlag: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:14`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:2720`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:43`. Beregninger og motprøver kan gjentas med den skrivebeskyttede kjøreblokken sist i denne filen.

**Lesemåte:** OBSERVERT = lest i angitt kilde; MÅLT = kjørt i denne gjennomgangen; TOLKNING = slutning med begrensning; FORSLAG = ikke gjennomført. `ukjent` betyr at kildene ikke avgjør spørsmålet. Alle kildebaner er relative til `HAVEN/`.

**K1–K6, kort avgjort**

| Påstand | Dom og korrigering | Kilde |
|---|---|---|
| K1: 0,16 → 0,40; FA 0,11 → 0 | Tallene stemmer: 8 → 20 av 50 ekte, 1 → 0 av 9 lokkeduer. «Holdout» må omdøpes til gjenbrukt utviklingssett etter adaptive runder. | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:14`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:2720`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:43` |
| K2: norske alias gir største enkelteffekt | Hints-ablasjonen gir 3 → 12 treff, +0,18. Den endrer både alias og tokens, på flere språk, samt valgt τ; den isolerer ikke norske alias. | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:67`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:126`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:238` |
| K3: Book-avledet prior gir +0,14 uten lekkasje | Uavhengig avledning er `ukjent`. +0,14 inneholder tre treff fra lavere τ og fire fra QWORD ved fast τ. Spesifisitetsvekting hindrer ikke lekkasje generelt. | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:177`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:222`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1140`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1364` |
| K4: skop må være multiplikativt | Den additive implementasjonen skaper score fra null. Multiplikasjon bevarer null, men kan løfte irrelevant positiv score over τ. +0,08 er her fire terskelpasseringer, ikke fire nye riktige rangeringer. | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:156`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:169`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:401`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:406` |
| K5: fin hjelper bare ett ord og lekker | Ett ekstra ett-ord-treff i én sammenligning, n=6. Matchet R2-sammenligning har samme FA for full og fin: 3/9. Ingen isolert dokumentasjon for at finsplittingen skaper denne lekkasjen. | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:798`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1022`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1588`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1700` |
| K6: resten er registeret | Avvist som årsaksforklaring. Diagnosen er R3s 32 bom, ikke R4s 30. Tre ytterligere bom kan repareres ved tekstnormalisering uten nye registeralias; «uten norsk»-listen har direkte moteksempler. | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:2`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1930`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:2720`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:513` |

**1. Forfatterlekkasje: hva kan faktisk belegges?**

OBSERVERT: QWORD er en håndskrevet konstant med 15 nøkler. Kommentaren sier «avledet av Book», men ingen funksjon avleder tabellen fra titler, og ingen kilde per kobling eller blind avledningslogg følger med. Book 23 peker til den maskinlesbare boken; der finnes meningsfulle utgangspunkt som «Duration, withdrawal and deletion» og «Control that can actually be exercised». Det forklarer en mulig inspirasjon, ikke hvorfor akkurat «kan jeg» skal bety utøvbar datakontroll. Tabellen omfatter dessuten contact.introduction, access.audit.privacy, test.acceptance, skeleton.owner-entity-access og bibliotekarformål utover den oppgitte undertre-/explain-avledningen. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:177`, `CellProtocolDocuments/Book/23_Purpose_Knowledge_Base.md:11`, `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json:2110`, `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json:2183`.

MÅLT: Jeg brukte **nøyaktig kodebetingelsen** `(" " + q) in (" " + tekst.lower() + " ")`, ikke en strengere ordgrensetest. «Gold peker på» betyr medlemskap i minst én av de aktiverte nøklene sine ref-lister. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:224`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:16`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:310`.

| Del | Ytringer | Minst én QWORD-nøkkel | Gold i aktivert ref-liste | QWORD-dekkede lokkeduer |
|---|---:|---:|---:|---:|
| Hele korpuset | 150 | 35 | 21 | 2 |
| Trening | 91 | 19 | 15 | 0 |
| Holdout | 59 | 16 | 6 | 2 |

Dette er 21/35 samsvar totalt, men bare 6/16 på holdout (6/14 blant QWORD-dekkede ekte). Alle 15 nøkler forekommer i korpuset. De 15 radene nedenfor har 36 forekomster fordi én ytring aktiverer to nøkler; tabellen over teller hver ytring én gang. Beregningsgrunnlag: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:179`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:16`.

| Nøkkel | Hele korpuset: dekket / gold i liste | Holdout: dekket / gold i liste |
|---|---:|---:|
| hvor lenge | 1 / 1 | 1 / 1 |
| hvem | 7 / 2 | 4 / 0 |
| hvor lagres | 1 / 1 | 0 / 0 |
| hvor er | 1 / 1 | 0 / 0 |
| hvordan vet | 2 / 1 | 1 / 0 |
| kan jeg | 3 / 1 | 1 / 0 |
| hvor mye | 1 / 1 | 1 / 1 |
| hva brukes | 1 / 1 | 1 / 1 |
| til noe annet | 1 / 1 | 0 / 0 |
| hvorfor | 3 / 1 | 1 / 0 |
| hva er | 8 / 4 | 3 / 1 |
| hva betyr | 2 / 1 | 1 / 0 |
| hvordan virker | 1 / 1 | 1 / 1 |
| forklar | 2 / 2 | 0 / 0 |
| slett | 2 / 2 | 1 / 1 |

TOLKNING: Felles forfatter, alle nøkler representert i testkorpuset og manglende uavhengig avledning gjør korpustilpasning plausibel. Det beviser **ikke** om Losen faktisk tenkte «fra Book» eller «fra korpus» da tabellen ble skrevet; det er `ukjent`. Den ærlige betegnelsen er «manuelt konstruert norsk spørreordsleksikon, inspirert av formålstaksonomien og ikke uavhengig validert». «Ingen norsk lagt til for hånd» er derfor bare sant om selve registerfilene, ikke om hele matcheren. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:4`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:177`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:36`.

**Hvor kommer +0,14 fra?** MÅLT med samme funksjoner som R2-a/R2-c:

| Modell | τ | Riktige av 50 | FA av 9 |
|---|---:|---:|---:|
| R2-a uten QWORD, originalt valgt τ | 0,25 | 11 | 0 |
| R2-a uten QWORD, kontroll med fast τ | 0,15 | 14 | 0 |
| R2-c med QWORD, originalt valgt τ | 0,15 | 18 | 1 |
| R2-c med QWORD, kontroll med fast τ | 0,25 | 11 | 0 |

De fire QWORD-gevinstene ved τ=0,15 er «hvor mye deler jeg», «hvor lenge lagres det», «hva brukes dataene til» og «hvordan virker dette». De tre øvrige gevinstene er «foreslå hva jeg bør få med meg på Arendalsuka», «eksporter historikken min» og «hvilke kilder bygger dette på»: ingen av dem har QWORD-treff; de passerer bare den lavere terskelen. **Fire av de sju ekstra treffene kan tilskrives prioren ved denne faste terskelen; tre kan ikke.** Dette er en kontrollert dekomponering ved τ=0,15, ikke en påstand om terskeluavhengige additive effekter. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:389`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:391`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:319`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:53`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:82`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:99`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:125`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:139`.

MÅLT: På sluttmodellen gir fjerning av QWORD, med gain=3 og τ=0,15, 16/50 → 20/50 når QWORD settes tilbake: +0,08, begge med 0/9 FA. Den faktiske R2-c-lokkeduen er «hvem vant VM i 1998» → access.audit.privacy, score 0,18. Rapportens forklaring med «hva er klokka» beskriver ikke den målte holdout-feilen i R2-c. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:391`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:154`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:50`.

**2. Holdout-disiplin: τ er treningsvalgt; slutthypotesen er det ikke dokumentert at er**

OBSERVERT: `choose_tau` får bare trening og maksimerer `top1 - decoy_false_accept`. Scoringsfunksjonene får flate og tekst, ikke gold. Dette holder på funksjonsnivå. Men `run_round` skriver ut holdout-score og de første tolv feilene for hver kandidat. Det finnes ingen kode som velger én endelig kandidat og alle vektene etter en forhåndsbestemt treningsregel. Boost, QWORD-vekt, skop-gain og varianter er håndsatt; 27 kandidater rapporteres. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:319`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:360`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:139`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:407`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:414`.

MÅLT: gain=3 og gain=5 har begge treningsmål 0,288596 (top-1 27/76 minus FA 1/15), mens gain=2 har 0,262281. Valg av gain=3 **kan** forsvares som lavere gain blant treningslikestilte kandidater, men denne utvalgsregelen er ikke dokumentert som bestemt på forhånd. R3-e med priorvekt 0,20 har også treningsmål 0,288596, mot R3-as 0,235965; videreføringen av 0,12 er ikke forklart som ren maksimering av treningsmålet. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:320`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:401`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:407`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`.

TOLKNING: Rapporten beskriver selv «hypotese → resultat → justering», inkludert valg etter holdout-FA. Rundene er utvikling på den samme synlige delmengden. Jeg kan derfor ikke verifisere påstanden «ingen kandidat valgt etter å ha sett holdout»; dokumentasjonen støtter det motsatte på designnivå. At skriptet nå kjører deterministisk, gjenskaper ikke historisk blindhet. Hvor stor del av +0,24 som generaliserer, er `ukjent`; det finnes ingen forsvarlig prosentvis «rabatt» på 0,40. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:43`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:53`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:382`.

FORSLAG til ærlig formulering: «På 50 syntetiske ekte ytringer som ble brukt til å utvikle hypotesene, økte den valgte varianten fra 8 til 20 treff. Ingen av de ni negative ytringene i denne delmengden ble akseptert. Uavhengig test av sluttvarianten gjenstår.» Grunnlaget er de samme resultatene, uten å tillegge delmengden blindhet den mistet. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:14`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:2720`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:43`.

**3. Er 8 → 20 større enn tilfeldig parvis variasjon?**

MÅLT: Jeg rekonstruerte alle prediksjonene; resultatfilen alene lagrer bare tolv feil per kandidat. På de 50 ekte ytringene er den parvise tabellen slik. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:373`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:346`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:260`.

| | R4 feil | R4 riktig | Sum |
|---|---:|---:|---:|
| M0 feil | 29 | 13 | 42 |
| M0 riktig | 1 | 7 | 8 |
| Sum | 30 | 20 | 50 |

Eksakt tosidig McNemar/binomialtest på de 14 uenige parene:

`p = 2 × [C(14,0) + C(14,1)] / 2^14 = 30/16384 = 0,0018310546875.`

TOLKNING: For to på forhånd faste matchere og uavhengige ytringspar er denne skjevheten lite forenlig med lik sannsynlighet for forbedring og forverring. Svaret på det snevre spørsmålet er **ja**. Den eneste tapte baselinetrefferen er «hvor står vi nå på prosjektet», som R4 flytter fra current-status til forelderen overview-and-sharing. Men p-verdien er ukorrigert for adaptiv modellutvikling; den er ikke et bekreftende produktbevis. Ytringer laget for samme formål kan dessuten være avhengige. Kilder og parenes konstruksjon: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:18`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:20`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:310`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:29`.

MÅLT/TOLKNING: Bootstrapintervallet [0,26, 0,54] gjelder treffandelen til én modell, ikke differansen mellom to parvise modeller. Metoden trekker enkelt-ytringer og modellerer verken forfatteravhengighet eller modellvalget. 0/9 lokkeduer har ved en uavhengig binomialmodell ensidig 95 % øvre grense `1 - 0,05^(1/9) = 28,3 %` (tosidig Clopper–Pearson øvre grense 33,6 %). 1 → 0 av 9 gir eksakt tosidig parvis p=1. Null observerte feil er et lite antall observasjoner, ikke en garanti. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:296`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:14`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:2720`.

**4. Registeret er en del av problemet; diagnosen frikjenner ikke matcheren**

MÅLT: Alle de 32 femfeltsradene i `holdout_misses` matcher **R3-a nøyaktig**, inklusive score avrundet til tre desimaler. R4 har 30 bom, og 16 av de 32 diagnoseradene har endret prediksjon eller score. To av de 22 radene merket «har norsk» er allerede riktige i R4: «hva gjenstår før vi er ferdige» og «send skjemaet til de påmeldte». Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:27`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:67`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:401`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`.

OBSERVERT: «30 av 90 uten norsk» kan ikke brukes som målt språkdiagnose. Listen inneholder blant annet digital-work.coordinate med «prosjektstyring», work-items med «oppgaver», project-portfolio med «prosjektoversikt» og self-determination.data med «selvbestemmelse over egne data». Omvendt er «noen må se på dette» merket `true` for norsk i diagnosen, men gold-noden request-human-review har tomme alias/tokens i unionen. Kriteriet som produserte språkflagget finnes ikke i treningsskriptet; et korrekt samlet antall noder uten norsk er **ukjent** uten en definert språkrevisjon. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:75`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:260`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:412`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:483`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:513`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:1737`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/runtime_taxonomy.json:119`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:38`.

**Hva kunne en bedre tokeniser tatt?** MÅLT, som en avgrenset reparerbarhetsprøve: beholdt register, QWORD, aliasboost, gain=3 og τ=0,15; endret bare tekstnormalisering for TF-IDF i minnet. Skopets lengdeberegning brukte original `tok`, slik at gevinsten ikke skyldtes en ny skopvekt. Tre små regler, anvendt likt på nodetekst og spørring, rettet tre av de oppgitte 22 radene. Kilder for eksisterende tokeniser og skop: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:59`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:74`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:169`. Regler og måling er gjengitt i kjøreblokken.

| Ytring | Normalisering mot allerede eksisterende tekst | Ny riktig score | Eksisterende bevis |
|---|---|---:|---|
| feltet er borte | feltet / tekstfelt / søkefelt → felt | 0,376 | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:887`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:211` |
| følg opp | følg opp → oppfølging | 0,558 | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:162`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:59` |
| hva står igjen | står igjen → gjenstår | 0,451 | `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:584`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:43` |

MÅLT: Samlet 20 → 23 av 50, ingen tidligere riktige tapt, fortsatt 0/9 på de gamle lokkeduene. Hver av de tre reglene alene rettet sin ene rad. To ytterligere prøver, `nytt/nye → ny` og `funnet/finne/finner/finnes → finn`, rettet ingen ekstra top-1-bom. **Svar: tre demonstrert reparerbare uten nye registeralias; to andre av de 22 var allerede fikset i R4; de resterende 17 er ikke vist løst.** Grunnlag for de 22 og de prøvde formene: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:2`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:139`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:235`.

TOLKNING: Dette er et eksistensbevis for reparerbarhet, ikke et estimat på hvor mange en generell tokeniser vil løse. «Står igjen → gjenstår» er semantisk frasenormalisering, ikke bare stemming; også «følg opp» krever håndtering av flerordsuttrykk. Jeg har dermed lagt språkkompetanse i matcherprøven, men ikke i registeret. Reglene ble valgt etter å ha sett feilene, og 0,46 skal **ikke** presenteres som ny holdout-score. Eksakt maksantall blant de resterende 17 er `ukjent`. Dagens implementasjon kutter prefikser; den gjør ingen slik frasenormalisering. Kilde: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:59`.

OBSERVERT/TOLKNING: Flere andre feil har alternative forklaringer. «Hvor står vi nå på prosjektet» har allerede tekstoverlapp med gold, men rangeringen velger forelderen; «nytt formål» har også norsk gold-hint («nye formål automatisk»). «Help me» og «jeg kan ikke trykke på den» inneholder derimot ikke den nødvendige betydningen som en vanlig bøyingsnormalisering alene kan trekke fra gold-teksten; henvisningen «den» kan kreve avklaring eller eksplisitt kontekst. Det er urimelig å føre alle disse på én aliasmangel-konto. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:582`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:1539`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:1435`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:887`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:35`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:219`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_diagnose.json:243`.

OBSERVERT/MÅLT: To ekte holdout-gold er **umulige primærtreff uansett flere alias**: construct-cellconfiguration («bygg en konfigurasjon for menyen») og reuse-visible-configuration («hvor gjør jeg det»). Begge fjernes av `exclude_facet=True`. Dette er en konflikt mellom etikettoppgaven og kandidatpolitikken, ikke bare registerdekning. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:48`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:242`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:36`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:132`.

OBSERVERT/TOLKNING: Feiletikettering av «husk det jeg sa» som semantic-state er godt underbygd: noden gjelder sted/tid. Men «husk at jeg ikke liker koriander» kan allerede høre under owner-controlled preferences, som skal bevare eksplisitte preferansefakta. «Intet slikt formål i hele registeret» er derfor for bredt; et eget formål for generell samtalehukommelse er **ikke funnet ved tekstsøk etter memor/remember/husk/history/prefer/context og lesing av treffene i unionen**, mens en konkret preferansedel allerede finnes. Requester-control dekker dessuten innsyn i egen spørrehistorikk; det er ikke grunnlag for å kalle enhver minne-/historikkytring et registerhull. Kilde: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/kallimachos_taxonomy.json:27`. At human-agency er en gren gjør heller ikke alene gold ulovlig: evaluatoren tillater ikke-blad som gold og har ingen generell bladregel. De omstridte etikettene må dømmes, ikke automatisk slettes fra nevneren. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:1609`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/book_taxonomy.json:1108`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:54`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:93`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:279`.

**5. Prinsipp: ingen funnet atferdslæring; reell svakhet i hva som regnes som tekstbevis**

OBSERVERT / IKKE FUNNET VED KONTROLL: I vinnerens vei fant jeg **ingen læring fra observert atferd**: ingen klikk, tidsbruk, ignorering, personhistorikk eller eiers perspektivgraf leses. Den bruker statiske taksonomier, en syntetisk fasit til τ, flate, teksten og håndskrevne regler. Dette bryter ikke i seg selv grensen mot atferdslæring i kontrakt §4 og Book 09 §7. Det er en avgrenset vurdering av dette skriptet, ingen sertifisering av HAVEN-runtime. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:21`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:319`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md:61`, `CellProtocolDocuments/Book/09_Purpose_Interests.md:139`.

OBSERVERT: Multiplikasjonen i `apply_scope_mult` bevarer en **inngangsscore** på null. Men vinneren legger QWORD til scoren **før** multiplikasjonen. QWORD kan gi positiv score når TF-IDF og aliasboost er null for alle noder. «Null tekst → null» er derfor bare sant dersom «tekstbevis» defineres til å omfatte generiske spørreord som «kan jeg». Det er ikke det samme som bevis for hvilket domenespesifikt formål personen ønsker. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:169`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:222`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`.

MÅLT, urørt R4 og τ=0,15:

| Flate / tekst | Maks TF-IDF + aliasboost | QWORD til vinner | Sluttscore / prediksjon |
|---|---:|---:|---|
| onboarding / «kan jeg» | 0 | 0,12 | 0,48 / data.exercisability |
| onboarding / «hvor lenge koker poteter» | 0 | 0,12 | 0,24 / data.duration |
| hjelp / «hva er klokka» | 0 | 0,06 | 0,18 / knowledge.explain-policy |
| onboarding / «asdfgh» | 0 | 0 | 0 / unknown |

Første probe er underbestemt, andre er irrelevant til databruk, tredje er en allerede deklarert lokkedue flyttet til en annen flate. De to første viser at en nøkkel med bare én ref får **ingen demping** av 1/antall-regelen. Den tredje viser at delt vekt også kan bli stor nok etter skop. Den fjerde bekrefter den smale nullinvarianten. Grunnlag: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:180`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:184`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:227`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:175`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:148`.

MÅLT: Alle 24 eksisterende lokkeduer kjørt på alle fire flater gir 96 kontekstvarianter: R3-a aksepterer 5/96; R4 aksepterer 8/96. Dette er en stresstest med avhengige varianter, ikke 96 uavhengige nye observasjoner. Eksempelvis avviser R4 «hva er klokka» i butler, men aksepterer den i Kallimachos, onboarding og hjelp. Dessuten inkluderer onboarding `purpose://root`; undertreet dekker 88/90 noder og gir derfor liten tematisk avgrensning. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:147`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:174`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:110`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:169`.

TOLKNING: Jeg fant ikke at **skop alene** gjør eksakt null til positiv score i vinneren. Jeg fant at **QWORD + skop** gjør fravær av registertekstbevis til et akseptert treff. Hvis kravet er domeneforankret tekstbevis før kontekst får påvirke, feiler vinneren kravet. Hvis et generisk spørreord regnes som tilstrekkelig erklært bevis, holder nullinvarianten formelt, men den sikrer ikke meningsfull avvisning. Dette er ikke det samme som brudd på forbudet mot atferdslæring. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:175`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:227`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md:65`.

**6. Granularitet og andre forutsetninger som ikke holder**

- **«Fin» er ikke bare blad splittet på Goal-signaler.** Koden beholder alle originalnoder og legger biter under alle noder som har signaler, ellers beskrivelsessetninger. Prediksjonene kollapses så tilbake til originalref før scoring. Eksperimentet måler alternative tekstrepresentasjoner og konkurranse mellom dem; det validerer ikke treffsikkerhet på nye, menneskelig meningsfulle finformål. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:247`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:265`.
- **«Bare ett ord» hviler på ett tilfelle.** Matchet R1-full (M5) gir 2/6 ett-ord-treff og fin 3/6; M2b uten finsplitting har allerede 3/6. I R2-e mot R2-f er ett-ord-andelen lik og FA lik 3/9; lavere total top-1 for fin er reell her, økt lekkasje fra fin er ikke isolert. R3s «fin ved ≤2 tokens» bruker dessuten lærdomstekst i fin-grenen, mens basegrenen ikke gjør det. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:350`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:798`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1022`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1588`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:1700`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:404`.
- **«Skop gir +0,08» betyr ikke nødvendigvis bedre valg mellom formål.** I den rene R3-ablasjonen var de fire nye riktige allerede først rangert uten skop, alle med score 0,12 < τ. Skop løftet dem over terskelen. «Må være multiplikativt» er også sterkere enn beviset: denne additive funksjonen er feilaktig for nullinvarianten; andre funksjoner som eksplisitt krever tekstbevis er ikke testet. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:166`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:401`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:406`.
- **«Dagens router» er en proxy.** M0 er en lokal funksjon skrevet for forsøket, ikke et kall gjennom dagens router. Denne gjennomgangen har ikke kontrollert ekvivalens med runtime; reell produktforbedring er `ukjent`. Også M1-navnet «tittel+desc» utelater at Goal-signaler/outcome fortsatt inkluderes når bare hints slås av. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:126`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:67`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:337`.
- **«Kjør alt på nytt» fungerer ikke fra leveransen som lå her.** Full `main()` reproduserte hele runde 1 bit-for-bit som JSON-verdier, men stoppet deretter med FileNotFoundError for `haven_lessons_register_v0.json`. Filen kreves lokalt av H8. M0, R2-a/R2-c, R3-a og R4 ble rekonstruert fra de tilgjengelige funksjonene og dataene; lærdomsvariantene er derfor lest, ikke selvstendig reprodusert her. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:214`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:383`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:128`.
- **Dommerrunden er ikke alltid fem blinde alternativer.** JSON-en har 30 holdout-saker og seks lokkeduer, men antall alternativer er 0/1/2/3/4/5 i henholdsvis 3/9/5/4/4/5 saker. Alle 24 ekte gold er med. Noen saker viser bare gold; «foreslå et forskningsspørsmål» har bare commons-growth med score 0. Dette kan forankre menneskedommen til Losens etikett. Nettgrensesnittets faktiske visning og eventuelle tidligere svar er `ukjent`; jeg har kontrollert JSON-en. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_dommer_runde2.json:1`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_dommer_runde2.json:73`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_dommer_runde2.json:103`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:110`.

**7. Neste eksperiment og Kjetils del**

FORSLAG, ikke implementert: Først frys R4, M0, registeret, QWORD, τ og beslutningsregelen. Behandle nattkorpuset som utviklingsdata. Gjør én ny evaluering på et sett skrevet og merket uten innsyn i QWORD eller modellutdata, av Kjetil eller en annen uavhengig dommer. Splitt etter formål/frasefamilie og forfatter, ikke bare tilfeldig etter flate. Dette angriper nettopp fellesforfatter- og gjenbruksproblemet i den nåværende konstruksjonen. Grunnlag: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:4`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:310`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:43`.

FORSLAG: Prioriter en avvisningstest før mer taksonomigranularitet. For hver QWORD-familie: relevante ytringer, irrelevant domene med samme spørreord, parafraser uten nøkkelen og underbestemte ytringer. Kryss et fast negativsett med alle fire flater. Sammenlign frossen R4 med (a) uten QWORD, (b) QWORD som bare får hjelpe når det allerede finnes uavhengig domenetekstbevis, og (c) en på forhånd bestemt generell tokeniseringsvariant. Mål parvise treff, feilaksept, avvisning av ekte, og resultater med/uten QWORD per flate. Velg ingen variant etter å ha sett sluttsettet; eventuelle justeringer krever et nytt sluttsett. Behovet er konkret demonstrert av `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:415` og de motprøvde reglene i `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:179`.

FORSLAG: Avtal størrelsen før kjøring. Eksempel: minst 150 nye ekte og 100 nye, selvstendig formulerte negativer, med en egen holdt-utenfor del og dekning av QWORD-familiene. Ved null feil i 100 uavhengige negativer blir ensidig 95 % øvre grense omtrent 2,95 %, fortsatt ikke null. Dette er et praktisk forslag, ikke en gjennomført styrkeberegning. Utgangspunktet som må forbedres er 50 ekte og ni negative i dagens evalueringsdel. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:260`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:310`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_resultater.json:5`.

**Kjetil bør gjøre dette selv:** Døm de 30 eksisterende sakene i «Dommerbenken — chat» som en **etikettrevisjon**, ikke som et nytt blindt generaliseringsbevis. Skriv helst ønsket formål eller «uklart / trenger kontekst / intet formål» før alternativene vises; bruk «Ingen av disse» når nødvendig. Avgjør spesielt minne versus preferanse versus sted/tid, den generelle oppstartsytringen, og om facet-only-oppgaver skal ha et annet primærformål. Deretter erklærer han hvilke begreper/alias og lenker han faktisk vil godta; systemet må ikke behandle tid brukt, hopp over eller museklikk som implisitt læringsfasit. Dette er en foreslått bruk av eksplisitte dommer, i tråd med kontrakten. Kilder: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_dommer_runde2.json:1`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/NATT_RAPPORT.md:110`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:54`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:93`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md:65`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md:73`.

Kjetil trenger ikke egenhendig skrive alle språkvarianter. FORSLAG: Losen kan foreslå alias med eksplisitt kilde og begrunnelse; Kjetil avgjør og erklærer de usikre betydningene. Den avgjørende handlingen er dommen og kildevalget, ikke at den samme personen må forfatte all tekst. Neste evalueringsforfatter bør uansett ikke samtidig være den som tilpasser QWORD. Grunnlag: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md:65`, `CellProtocolDocuments/Book/09_Purpose_Interests.md:139`.

**Dekning, ukjent og reproduserbarhet**

Denne gjennomgangen leste hele NATT_RAPPORT, begge Python-filene, alle kandidatposter i resultat-JSON og hele diagnose-JSON; deretter de pålagte prinsipptekstene, Book 23 med det lenkede maskinlesbare artefaktet, de tre taksonomiuttrekkene og dommersettet. Kontrollen var lokal. Ingen live chat, faktisk router, dommer-UI eller eierdata ble brukt. Ukjent: QWORDs historiske tanke-/tilblivelsesprosess, uavhengig produkteffekt, korrekt menneskelig gold og en gjennomført, definert norskdekningsrevisjon. Relevante avgrensninger følger av `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:13`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_trening.py:126`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_korpus.py:4` og `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23/natt_dommer_runde2.json:1`.

Kontrollblokken under er kjørt fra denne rapporten: **exit 0**, alle assertions bestått og **inputs_unchanged=True**. Dette bekrefter de avgrensede målingene; den dokumenterte manglende lærdomsfilen hindrer fortsatt full gjentakelse av alle runder.

Kjøremetode: import med `sys.dont_write_bytecode=True`; resultatfilskriving i `main()` ble omdirigert til minne, øvrig skriving avvist. Ingen git-kommandoer eller kildekodeendringer. Bare denne rapportfilen er skrevet. Nøkkelartefaktenes SHA-256 ved kontroll:

```text
natt_trening.py     f5b16e825eea1808084d590a9ce7120e354c3972f0006c7d343bffe59a2469f7
natt_korpus.py      6dd2d4cd7b10df194c67256a08ae7929a13dfd5881864df06db10225ebc9a7aa
natt_resultater.json 3fd44841cf9b5d1c3fece280bdc8c507fcc54d890359fc000413152f960bd595
natt_diagnose.json  0f48f7f2c3fd111f47af4cb3c1f5f304ae96fb6151580eab06b2ba0508f7c452
```

Kjøreblokken nedenfor kjøres fra `HAVEN/`, med Python 3 og stdlib. Den skriver bare til stdout, og kontrollerer at inputfilenes innhold ikke endres. Forventningene gjelder de kontrollerte artefaktene, ikke vilkårlige fremtidige versjoner.

```sh
python3 - <<'PY'
import sys, io, json, math, re, hashlib, contextlib, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
p = Path("CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/natt-2026-09-23").resolve()
before = {f: hashlib.sha256(f.read_bytes()).hexdigest()
          for f in p.iterdir() if f.is_file()}
spec = importlib.util.spec_from_file_location("audit_natt", p / "natt_trening.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
saved = json.loads((p / "natt_resultater.json").read_text())

# Kjør main uten å overskrive resultatfilen.
real_open, sinks = open, []
def readonly_open(file, mode="r", *args, **kwargs):
    if any(c in mode for c in "wax+"):
        assert Path(file) == p / "natt_resultater.json"
        sink = io.StringIO()
        sinks.append(sink)
        return sink
    return real_open(file, mode, *args, **kwargs)
t.open = readonly_open
try:
    with contextlib.redirect_stdout(io.StringIO()):
        all_results = t.main()
    print("full_main_matches", all_results == saved)
except FileNotFoundError as exc:
    print("full_main_missing", Path(exc.filename).name)
assert json.loads(sinks[0].getvalue())["rounds"][0] == saved["rounds"][0]
print("round1_identical", True)

nodes = t.load_union()
ch = t.children_map(nodes)
idx = t.TfIdf({r: t.node_text(n) for r, n in nodes.items()})
train, hold = t.split(t.KORPUS)
def predictor(prior=t.qword_prior_specific, gain=3, index=idx):
    def run(f, s):
        sc = t.m_tfidf_alias_boost(nodes, s, index)
        if prior is not None:
            sc = t.add(sc, prior(s))
        if gain:
            sc = t.apply_scope_mult(nodes, sc, f, ch, s, gain=gain)[0]
        return t.rank(sc, nodes, exclude_facet=True)
    return run
f0 = lambda f, s: t.rank(t.m_keyword(nodes, s), nodes)
fa = predictor(None, 1)
fc = predictor(t.qword_prior, 1)
f3 = predictor(gain=1)
f4 = predictor()
rows = {}
for label, fn in [("M0", f0), ("R2a", fa), ("R2c", fc), ("R3a", f3), ("R4", f4)]:
    tau = t.choose_tau(fn, train, nodes)
    result, rows[label] = t.evaluate(fn, hold, nodes, tau)
    print(label, "tau", tau, "top1", result["top1"], "FA", result["decoy_false_accept"])
assert [sum(r[2] == r[3] and r[2] != t.UNKNOWN for r in rows[k])
        for k in ["M0", "R2a", "R2c", "R3a", "R4"]] == [8, 11, 18, 18, 20]
pairs = t.Counter((a[2] == a[3], b[2] == b[3])
                  for a, b in zip(rows["M0"], rows["R4"]) if a[2] != t.UNKNOWN)
wins, losses = pairs[(False, True)], pairs[(True, False)]
assert (wins, losses, pairs[(True, True)], pairs[(False, False)]) == (13, 1, 7, 29)
pv = min(1, 2 * sum(math.comb(wins + losses, k)
                   for k in range(min(wins, losses) + 1)) / 2**(wins + losses))
print("paired", dict(pairs), "exact_two_sided_p", pv)
print("zero_of_9_upper_one_sided_95", 1 - .05**(1/9))

def keys(s):
    return [q for q in t.QWORD if " " + q in " " + s.lower() + " "]
for label, data in [("all", t.KORPUS), ("train", train), ("hold", hold)]:
    covered = [d for d in data if keys(d[1])]
    aligned = [d for d in covered if any(d[2] in t.QWORD[q] for q in keys(d[1]))]
    print("QWORD", label, len(data), len(covered), len(aligned),
          "decoys", sum(d[2] == t.UNKNOWN for d in covered))
for q, refs in t.QWORD.items():
    counts = []
    for data in [t.KORPUS, hold]:
        ds = [d for d in data if q in keys(d[1])]
        counts.append((len(ds), sum(d[2] in refs for d in ds)))
    print("QKEY", q, counts)

for label, fn, tau in [
    ("R2a_fixed015", fa, .15), ("R2c_fixed025", fc, .25),
    ("R4_no_QWORD", predictor(None, 3), .15),
    ("R3_no_scope", predictor(gain=0), .15)
]:
    res, _ = t.evaluate(fn, hold, nodes, tau)
    print("ablation", label, res["top1"], res["decoy_false_accept"])
_, low_a = t.evaluate(fa, hold, nodes, .15)
for a, b in zip(rows["R2a"], rows["R2c"]):
    if a[2] != t.UNKNOWN and (a[2] == a[3]) != (b[2] == b[3]):
        print("R2_gain", a[1], "qkeys", keys(a[1]))
_, no_scope = t.evaluate(predictor(gain=0), hold, nodes, .15)
for a, b in zip(no_scope, rows["R3a"]):
    if (a[2] == a[3]) != (b[2] == b[3]):
        print("scope_transition", a, b)
for label, fn in [
    ("R3a", f3), ("R3e", predictor(lambda s: t.qword_prior_specific(s, .20), 1)),
    ("R4g2", predictor(gain=2)), ("R4g3", f4), ("R4g5", predictor(gain=5))
]:
    tau = t.choose_tau(fn, train, nodes)
    res, _ = t.evaluate(fn, train, nodes, tau)
    print("train_objective", label, res["top1"], res["decoy_false_accept"],
          res["top1"] - res["decoy_false_accept"])

diagnosis = json.loads((p / "natt_diagnose.json").read_text())
dm = diagnosis["holdout_misses"]
assert [d[:5] for d in dm] == [list(r) for r in rows["R3a"] if r[2] != r[3]]
flagged = {d[1] for d in dm if d[5]}
assert len(flagged) == 22
print("diagnosis_is_R3", True, "R4_misses",
      sum(r[2] != r[3] for r in rows["R4"]))
print("R4_changed_diagnosis_rows",
      sum(d[:5] != list(next(r for r in rows["R4"] if r[1] == d[1])) for d in dm))

old_tok = t.tok
rules = [
    ("felt", r"\b(?:tekstfelt|søkefelt|feltet)\b", "felt"),
    ("oppfølging", r"\bfølg\s+opp\b", "oppfølging"),
    ("gjenstår", r"\bstår\s+igjen\b", "gjenstår"),
]
extra = [("ny", r"\b(?:nytt|nye)\b", "ny"),
         ("finn", r"\b(?:funnet|finne|finner|finnes)\b", "finn")]
for label, active_rules in [(x[0], [x]) for x in rules + extra] + [("combined3", rules)]:
    def norm_tok(s):
        for _, pattern, replacement in active_rules:
            s = re.sub(pattern, replacement, s.lower())
        return old_tok(s)
    t.tok = norm_tok
    index2 = t.TfIdf({r: t.node_text(n) for r, n in nodes.items()})
    def normalized(f, s):
        t.tok = norm_tok
        sc = t.add(t.m_tfidf_alias_boost(nodes, s, index2), t.qword_prior_specific(s))
        t.tok = old_tok  # hold skopets lengdeberegning uendret
        return t.rank(t.apply_scope_mult(nodes, sc, f, ch, s, gain=3)[0],
                      nodes, exclude_facet=True)
    tau = t.choose_tau(normalized, train, nodes)
    res, changed = t.evaluate(normalized, hold, nodes, .15)
    recovered = [b for a, b in zip(rows["R4"], changed)
                 if a[2] != a[3] and b[2] == b[3]]
    lost = [b for a, b in zip(rows["R4"], changed)
            if a[2] == a[3] and b[2] != b[3]]
    print("normalization", label, "train_tau", tau, res["top1"],
          res["decoy_false_accept"], "recovered", recovered, "lost", lost)
    if label == "combined3":
        assert res["top1"] == .46 and not lost
        assert sum(r[1] in flagged for r in recovered) == 3
t.tok = old_tok

for f, s in [
    ("onboarding", "kan jeg"), ("onboarding", "hvor lenge koker poteter"),
    ("hjelp", "hva er klokka"), ("onboarding", "asdfgh")
]:
    base = t.m_tfidf_alias_boost(nodes, s, idx)
    print("probe", f, s, "base_max", max(base.values(), default=0),
          "prior", t.qword_prior_specific(s), "rank", f4(f, s)[:2])
decoys = [(f, s, g, lc) for _, s, g, lc in t.KORPUS if g == t.UNKNOWN
          for f in t.FLATE_SKOP]
for label, fn in [("R3a", f3), ("R4", f4)]:
    res, rr = t.evaluate(fn, decoys, nodes, .15)
    print("decoy_cross", label, len(rr), sum(r[3] != t.UNKNOWN for r in rr))
print("scope_sizes", {f: len(t.subtree(nodes, roots, ch))
                      for f, roots in t.FLATE_SKOP.items()})
print("facet_only_gold", [(s, g) for _, s, g, _ in hold
                          if nodes.get(g, {}).get("facetOnly")])
judges = json.loads((p / "natt_dommer_runde2.json").read_text())
print("judge", len(judges), sum(x["gold"] == t.UNKNOWN for x in judges),
      dict(t.Counter(len(x["alternativer"]) for x in judges)))
assert all(x["tekst"] in {d[1] for d in hold} for x in judges)
assert all(x["gold"] == t.UNKNOWN or
           x["gold"] in {a["ref"] for a in x["alternativer"]} for x in judges)
assert before == {f: hashlib.sha256(f.read_bytes()).hexdigest()
                  for f in p.iterdir() if f.is_file()}
print("inputs_unchanged", True)
PY
```

Arbeidet er avsluttet som kildeforankret motsvar med dokumenterte begrensninger. Ingen implementasjon er foretatt eller forutsatt godkjent.
