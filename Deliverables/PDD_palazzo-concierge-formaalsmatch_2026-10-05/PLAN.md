# PLAN — palazzo concierge formaalsmatch

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05` · Skrevet natt til 7. oktober 2026 (6. oktober kl. 22:24–23:25 UTC), av Losen, og rettet 7. oktober etter en uavhengig kontroll (se «Rettet etter kontrollen» sist). G1 er godkjent (6. oktober). **G1-GUI og G2 er godkjent (7. oktober, lest ca. kl. 08:15 UTC).** Planen slik den ble godkjent, ligger uendret i `PDD/PLAN.godkjent-G2-20261007.md`. Det som er kommet til etter godkjenningen, står i «Etter G2» sist, og teksten ellers er som da den ble godkjent.

Stier er relative til HAVEN-roten. `PS` står for `PalazzoScaffold`, `CS` for `CellScaffold/_wt-butler-e1-20260929` (arbeidstreet som står på CellScaffolds main per 28. september), `CP` for `CellProtocol` lest på commiten `81601a6f835252aba7e99d43786fb5d67227c245` (pinnen `PS` bygger mot), `CPD` for `CellProtocolDocuments`, `HD` for `HAVEN-Deploy/_handoff/HD-0077`, og `PDD` for denne oppgavemappen. Klokkeslett er UTC. Formålene (F1–F8) og testene er dem som står i den godkjente spesifikasjonen, `PDD/FORMAALSSPEC.godkjent-G1-iterasjon1.md`. Planen legger ikke til og tar ikke bort formål.

## Kort

**Etter G2:** listen under er slik den sto da planen ble lagt fram. Hva som er gjort siden, og hva som venter på deg nå, står i «Etter G2» sist.

**Det du må gjøre nå.**

1. Se på de ni bildene i `PDD/images/` og si om de er slik gjesten skal se det (G1-GUI). `PDD/images/README.md` sier hva som er skissert, og hva som ikke vises. Ett spørsmål hører til bildene: om et tilbud skal ha merkelappen «høy sikkerhet», som siden setter på svar i dag (`PDD/images/tillegg-concierge-merkelapp-v1.png`).
2. Velg vei for koden: portet til Palazzo nå, eller løftet til kjernen først (valg 1 under).
3. Les valgene i tabellen «Valg i planen». Sier du bare at G2 er godkjent, gjelder de anbefalte. Ett unntak, sagt til deg 7. oktober kl. 05:38 (03:38 UTC): valg 21. Der står linjen om allergener under hvert svar til du har valgt.

**Rekkefølgen jeg foreslår.** Tre utsettinger, hver angrepet av en uavhengig tråd før den settes ut, og hver bak en bryter som kan slås av.

```
 0  Grunnlinjen og vektene     hele testmengden før noe endres; vektene du valgte 2. oktober inn
 1  Korpus og sølvfasit        målte og nye gjestesetninger; en blind tolk sier hva hver ber om     ingenting på nett
 2  Husets graf (F7)           retter, drikke og emner som data med versjon, laget av korpuset
 3  Dekomponeringen (F1)       setningen → formål og interesser med fortegn, uten modell
 4  Matchen (F2)               interessene mot husets graf, med terskel og forklaring
 5  Svaret (F6)                tilbud, forteller, kvittering, ja
 6  Samtalen (F5)              det gjesten har sagt om seg selv, på siden, synlig og fjernbart
10  Siden                      etter bildene, når du har godkjent dem
11  ──► UTSETTING 1            angrep, commit, CI, utsetting bak bryteren, måling på nett.  DU: slå på
 7  Den nye allergenveien (F8) merking, beskrivelse og personalet; erstatter strakstiltaket
11  ──► UTSETTING 2            eget angrep.                                                  DU: si at strakstiltaket kan byttes ut
 8  Modellen bak (F3)          spør gjesten, forhåndssjekk, modellen peker ut noder
11  ──► UTSETTING 3            eget angrep.                                                  DU: slå på
 9  Revisoren (F4)             i utvikling og test, fra steg 4 og utover: foreslår tillegg og vekter;
                               gevinsten måles på setninger grafen ikke har sett.           DU: terskelen og målene
12  «Behold» (F5, det varige)  venter på veien fra siden til gjestens entitet (onboarding-oppgaven)
```

**Hva det å lese kjernen endret.** Spesifikasjonen sa at kjernen ikke var lest. Nå er mappen lest, på pinnen: `CP/Sources/CellBase/PurposeAndInterest/` har 29 filer. Jeg leste 12 av dem og deler av tre før planen ble skrevet, og en lesetråd leste testene. De fjorten andre, og resten av de tre, ble lest av en lesetråd 7. oktober, etter at kontrollen fant at planen sa «lest» om filer ingen hadde lest. Hvem som har lest hva, og hva den siste lesingen endret, står under «Det kjernen har, og det den mangler». Fire ting:

1. **Kjernen har mer av dette enn spesifikasjonen regnet med.** En ferdig vektet sum mellom den som spør og det som tilbys, med et flagg for om søket ble fullstendig (`InterestPurposeWeightedSum`). Navnene for «match først, så dypere» (`MatchStrategyPlanner`: `system1Preconfigured`, `system2Reconfiguration`, og utløsere som `lowConfidence` og `ambiguousTopK`). Sammensatte formål med oppfyllelse (`PurposeComposition`). Mål med status (`GoalDefinition`, `GoalEvaluation`). Planen bruker disse der de passer, og lager ikke egne.
2. **Restaurantmodellen din ligger alt i kjernens depot.** `CP/commons/benchmarks/purpose-interest/Sources/PurposeInterestBenchmarkSupport/RestaurantPurposeScenarioSupport.swift` og `CP/Docs/PurposeInterest_Matching_ExperimentPlan_NO.md`: restauranter annonserer formål med interessevekter, brukeren har formål med interessevekter, og anbefalingen er overlappet. Husets graf i F7 følger den formen. Samme dokument har formatet for lokale vektjusteringer oppå en felles sannhet (formål, interesse, operasjon, verdi, grunn). Revisorens forslag (F4) skrives i det formatet.
3. **Kjernen har ikke det F1 trenger.** Ingenting der gjør tekst om til interesser: ingen bøyningsregel og ingen nektelse. Den ene normaliseringen som finnes (privat, i `GoalEvaluationEngine`), sammenligner bare merkelapper. Butlers regel ligger i CellScaffolds app (`CS/Sources/App/Support/ButlerSignalMatcher.swift`, 323 linjer, bare Foundation).
4. **Ni funn i kjernen som angår denne oppgaven.** De står i tabellen «Funn i kjernen» (seks fra første lesing, tre fra lesetråden 7. oktober). To av dem betyr noe for personvernet: `Perspective.addPurpose` skriver formålets navn til standard ut uten betingelse, tre steder til skriver navn når en oppdatering kommer med et annet navn enn det som står, og `Perspective` har ingen måte å fjerne en aktiv interesse på.

**En kollisjon jeg fant i regelen vi skal gjenbruke.** Butlers regel sier at et ord treffer en term på tre tegn når ordet begynner med termen og er høyst tre tegn lengre. «østers» blir «osters» etter normaliseringen, begynner med «ost» og er seks tegn. «Jeg liker østers» ville gitt interessen ost. Palazzo har begge deler på menyen. Dekomponeringen får derfor én regel til, som Butler ikke har: når to noder treffer samme ord, vinner den lengste termen. Det står som egen test i arbeidspakke 3 (regnet av koden, ikke kjørt). Kontrolltråden fant flere kollisjoner med samme regel, og jeg har regnet dem etter for elleve ord valgt for hånd (`PDD/graf/kollisjoner_regnet.py`, i Python og ikke kjørt i Swift): «lokale» og «lokalt» treffer emnet løk, «risiko» treffer ris, «lampe» treffer lam, og «desserter» treffer både dessert og erter. Emnet øl blir «ol» på to tegn og får ingen bøyning, så «ølet» treffer ikke. «Lengste term vinner» hjelper bare der en lengre term finnes. Kollisjonene skal derfor finnes med kode før termene settes fast: en test kjører hver term mot ordene i korpuset og i de målte setningene, og hver kollisjon avgjøres som data (et unntak eller en lengre term), ikke for hånd.

**Tid.** Jeg oppgir tid per arbeidspakke og per runde, ikke en sluttid. Antall runder med angrep er ukjent til første angrep er målt. Grunnlaget er de to rundene vi har: strakstiltaket tok 4 timer og 37 minutter fra G1 var lest til det var lagt fram (tre regler, én angrepsrunde), og runde 2 av vakten tok 34 timer og 50 minutter fra G1 til siste måling (fem angrep, fire utgaver satt ut). Fram til utsetting 1 er det rundt 24–35 arbeidstimer for meg hvis én angrepsrunde holder (summen av pakkene 0–6, 10 og 11 i tabellen under), og 3–5 timer til for hver runde utover det. Det er to til tre døgn med økter, ikke en natt.

**Bedre treff er ikke lovet.** Det står i spesifikasjonen med tallene bak, og gjelder fortsatt. Første måling på usette setninger kommer i arbeidspakke 9.

## Valg i planen

Hvert valg har en anbefaling. Sier du bare at G2 er godkjent, gjelder de anbefalte. Unntaket er valg 21 (se raden).

| # | Valg | Anbefalt | Det andre | Hva det betyr for deg |
|---|---|---|---|---|
| 1 | Hvor koden for dekomponeringen ligger | **Portet til Palazzo nå**, i én fil uten Palazzo-typer, med Butlers tester kopiert ordrett. Løftes til kjernen som egen oppgave når det er målt | Løftet til kjernen først | Se «To veier for koden». Løft først berører `CellProtocol` main, CellScaffold (Butler) og pinnen i Palazzo, og legger til en utgivelse i hvert depot før noe vises på conciergen |
| 2 | Regningen i matchen | **Gjesteflatens regning**, slik G1 sier (vekt ganger andel felles emner), utvidet så kantene kan ha vekt. Med enhetsvekt gir den nøyaktig dagens tall | Kjernens ferdige sum (`InterestPurposeWeightedSum`) | Se «Regningen». Gjesteflatens tester står urørt. Å bytte begge flatene til kjernens sum er en egen oppgave |
| 3 | Hvor samtalens Perspective ligger mellom to spørsmål | **På siden hos gjesten**, sendt med hvert spørsmål. Tjenesten holder ingenting | I tjenestens minne, med en nøkkel og en utløpstid | Se «Samtalens Perspective». Samtalen er slutt når siden lukkes eller lastes på nytt |
| 4 | Nytt kall eller endret `ask` | **Nytt kall, `POST /palazzo/api/samtale`**, bak en bryter. `ask` står urørt | Endre `ask` | Med nytt kall endres ingen committet test. Bryteren er også første vei tilbake |
| 5 | Formålene conciergen kjenner | **spise, drikke, vite, unngå, bord, åpningstid**, med måltekst i `PDD/graf/emner-v1.md` | En annen liste | Listen må være fast før den blinde tolken begynner |
| 6 | Emnene for retter og drikke | **Forslaget i `PDD/graf/emner-v1.md`** (85 emner, 151 koblinger, hver sporet til menyens tekst, en tagg, kategorien eller navnet). Du trenger ikke godkjenne dem | Du går gjennom dem | Tre ting er holdt utenfor med vilje, og allergenene har ikke egne noder ennå. Begge deler står øverst i filen |
| 7 | Fasiten | **Sølvfasit fra en blind tolk**, som du svarte for rådgiverpanelet 28. september | Dommerbenk med lokkeduer | Med sølvfasit dømmer du ingen saker. Ingen tall kalles gull |
| 8 | Modellen i utvikling og test | **To referanser, holdt fra hverandre:** en uavhengig Claude-tråd nå (trenger ingen nøkkel), og modellen på verten når utsetting 3 står bak bryteren | En egen nøkkel på Mac-en | Nøkkelen på verten flyttes ikke. De to er ikke samme modell, og rapporten sier hvilken hvert tall gjelder |
| 9 | «På linje med modellen» | **Like stor andel riktige mot fasiten**, ikke samme svar rad for rad | Samme svar rad for rad | Matchen kan være på linje og likevel svare annerledes på enkeltrader |
| 10 | Vektene du valgte 2. oktober | **Tallene (`fa66868b`) flettes inn før matchen**, og benken kjøres på nytt. `96f1c5f9` (bare testkode, med én test som feilet 3. oktober) tas ikke med | Vente | Se arbeidspakke 0. Benkens 7 av 7 ble kjørt før to senere endringer i regningen på grenen som står på nett |
| 11 | Hva som ikke sendes til modellen | **Forhåndssjekken som en liste over det som slipper gjennom:** en setning sendes bare når hvert tegn er en bokstav, et mellomrom eller vanlig skilletegn. Et siffer, en «@», en parentes eller et punktum inne i et ord stopper den. I tillegg stoppes setninger med ord om allergi, trygghet, vin eller alkohol | En liste over det som stoppes (Kallimachos' fem mønstre, eller en egen). Eller uten unntak, som meldingen din lyder | Det er et unntak fra «Send til modellen om svaret feiler». To kontrollrunder fant nye hull i listen over det som stoppes. Med en liste over det som slipper gjennom, er det bare det som er skrevet med ord, som går ut: et nummer eller en adresse med bokstaver, og navn. Prisen er at en setning med et tall ikke går til modellen. Testen i spesifikasjonen lover mer enn noen regel kan holde. Se «Forhåndssjekken» |
| 12 | Hva en bom på nett etterlater | **Grunn, grafens versjon og antall noder**, ikke gjestens ord | Også ordene, etter gjestens ja | Uten ordene ser vi hvor grafen mangler dekning, ikke hvilke ord som manglet. Ordene kommer fra korpuset i utvikling |
| 13 | Hvilke spørsmål modellen får formulere svar på | **Dekomponeringen avgjør:** modellen velger blant vaktens ferdige tekster bare når setningen ikke avgrenser noe («uten», «ikke», noe gjesten unngår). Gjelder det nye kallet | Lukkede lister med hele spørsmål, som i dag | Rettlisten kommer da tilbake til modellen, slik du valgte 5. oktober, uten at de to testene i `ask` endres |
| 14 | Sperren for vin og alkohol | **Gjelder det gjesten spør om**, ikke at en rett har vin i beskrivelsen | Som i dag (ordet i spørsmål og svar) | Pasta vongole og Tagliata di manzo behandles som andre retter |
| 15 | Revisoren og rådgiverpanelet | **Revisoren bygges her**, og panelets mappe får en henvisning hit | To løp | Panelet er din oppgave |
| 16 | Grafen som data med versjon, og prøven av grafdatabasen | **En datafil med versjon i pakken**, lest av korpuscellen. Grafdatabasen prøves som en egen måling etter utsetting 1 | Grafdatabasen først | Grafdatabasen ligger i CellScaffold og har ikke vekter på kantene. Prøven krever et CellScaffold-bygg |
| 17 | «Behold» og veien til gjestens entitet | **Venter på onboarding-oppgaven.** Denne oppgaven fastsetter hva siden gir fra seg | Bygges her | Se arbeidspakke 12 |
| 18 | Terskelen og tallene som er mål | **Settes av deg etter første måling** | – | Før det oppgis bare målte tall |
| 19 | Likt tall etter et «liker ikke» | **En rett med et emne gjesten ikke liker, står etter retter med samme tall** | La rekkefølgen i grafen avgjøre | Gjelder bare når to retter får samme tall. Med vektene du valgte 2. oktober og gjesteflatens regning slik den er i dag, får osteretten og sitronkremen samme tall for «Jeg liker ikke ost» og så desserter (1/6 og 1/6; i flyttall kan de skille seg i siste siffer), og uten regelen er det tilfeldig hvem som står først. Med planens forslag (vekt på kanten) får osteretten null eller mindre og er ute av det conciergen foreslår selv; da trengs ikke regelen for dette eksempelet. Den andre halvdelen av testen `test.samtale.liker-ikke`, at «Har dere oster?» gir osteretten likevel, avgjøres ikke av tallet, men av at conciergen svarer på det gjesten spør om (arbeidspakke 6). Tallene står sist i `PDD/graf/emner-v1.md` |
| 20 | Når gjesten ikke tåler noe grafen ikke kjenner | **Ingen tilbud resten av samtalen, og henvisning til personalet.** Ordet lagres ikke; siden husker bare at det er noe (noden `ukjent`) | Som en vanlig bom: spørsmålet om modellen | Uten dette gjelder «ingen tilbud etter tåler ikke» bare det grafen kjenner. Gjelder først når den nye allergenveien (F8) erstatter strakstiltaket. Til da får setningen henvisningen som i dag |
| 21 | Hvilke svar som har linjen om allergener | **Svar som nevner en rett eller en drikk** (regel 7 i kontrakten) | Hvert svar, som regel 3 på nett | Kvitteringer som «Notert: du liker ikke ost», og spørsmålet om modellen, står uten linjen i bildene. Velger du «hvert svar», rendres de på nytt. **Et bart «G2 godkjent» velger ikke det anbefalte her:** det er smalere enn regelen som står på nett, og meldingen 7. oktober sa ikke hvilket alternativ som var anbefalt. Linjen står under hvert svar til du har valgt |

## Det kjernen har, og det den mangler

Lest på pinnen 6. oktober kl. 22:24–22:31 UTC, rett fra git-objektene (ikke arbeidstreet, som står på en annen commit). Testene er lest av en lesetråd samme kveld (`HD/maal/grunnlag-20261007/les/L5-KJERNETESTER.md`).

Av de 29 filene i mappen leste jeg 12 (`Signal`, `Weight`, `Protocols`, `PerspectiveNode`, `Interest`, `Purpose`, `PurposeInterestAdjacencyIndex`, `WeightedGraphRuntime`, `PurposeComposition`, `MatchStrategyPlanner`, `InterestPurposeWeightedSum`, `Constraint`) og deler av tre (`Perspective`, `GoalDefinition`, `GoalEvaluationEngine`). De fjorten andre leste jeg ikke: `Action`, `ClaimComposition`, `ClaimDefinition`, `ClaimScheme`, `ClaimSchemeInstance`, `EntityRepresentation`, `EntityRepresentationDataCodec`, `Facilitator`, `Goal`, `PerspectiveEntityProjection`, `RelationalDecayPolicy`, `RelationalLearningEngine`, `RelationalLearningModels` og `SDGPilotPurposeCatalog`. I `PerspectiveEntityProjection` slo jeg bare opp funksjonene K2 viser til, og det tabellen sier om `RelationalLearningEngine`, bygger på `CP/Docs/RelationalLearning_Architecture_NO.md` og på at filen finnes.

De fjorten, og resten av de tre, ble lest av en lesetråd 7. oktober kl. 02:18–02:25 UTC (`HD/maal/grunnlag-20261007/les/L6-KJERNEREST.md`). Den støttet K3 og K6 og radene for F2 og F6. Den rettet K2 (et aktivt formål kan fjernes ved å sette hele listen på nytt), utvidet K1 (flere steder skriver navn til standard ut) og la til K7, K8 og K9. Linjene den viser til for K1, K2, K7 og K8, og avkortingen i K9, har jeg lest etter selv.

| Oppgaven trenger | Kjernen har (i `CP/Sources/CellBase/PurposeAndInterest/`) | Kjernen har ikke |
|---|---|---|
| F1: setning → formål og interesser | Typene å bære det i: `Purpose`, `Interest`, `Weight`, og `PurposeComposition` (`allOf`, `anyOf`, `sequence`, `atLeast`) | Tekst til noder: ingen bøyning eller nektelse, og ingen normalisering av gjestens tekst (en privat `normalize` i `GoalEvaluationEngine.swift`, linje 307–312, sammenligner merkelapper). Tekstsakene i kjernens måleverktøy har interessene ført opp for hånd |
| F2: match først | `InterestPurposeWeightedSum.match` (den som spør × det som tilbys, rangert, med `complete`), `WeightedGraphRuntime` (signal, toleranse, hopp, frist, evidens), `PurposeInterestAdjacencyIndex` (forhåndsbygd) | Terskel og oppsamling. Oppsamlingsnoder med terskel står som neste steg i `CP/Docs/PurposeInterest_Matching_ExperimentPlan_NO.md`, ikke bygget |
| F3: modellen bak ved bom | Navnene: `MatchStrategyPlanner` med `system1Preconfigured` og `system2Reconfiguration`, og utløserne `lowConfidence`, `ambiguousTopK`, `missingPreconfiguredCoverage`, `requiresNewKnowledge`, `privacyOrCapabilityGate`, `latencyBudgetExceeded`. Planleggeren anslår; den utfører ikke | Selve kallet. Palazzo har sitt (`PS/Sources/App/Services/PalazzoAnthropicPhraser.swift`) |
| F4: revisoren foreslår vekter | Formatet for justeringer oppå en felles sannhet (`ScenarioWeightTuningConfig`: formål, interesse, `set`/`add`/`multiply`/`remove`, verdi, grunn), med rapport over hvor toppsvaret endres. Det ligger i måleverktøyet, som ikke er et bibliotek Palazzo kan bygge på. `RelationalLearningEngine` for vekter som læres av hendelser; den avkorter alle vekter til 0–1, så den kan ikke bære et «liker ikke» (K9). Lesetråden L6 leste at den bare opprettes i `CellApple` | En revisor |
| F5: Perspective for samtalen | `Perspective`: aktive formål, interesser og entiteter med vekt | Fjerning av en aktiv interesse. Et aktivt formål kan bare fjernes ved å sette hele listen på nytt. `PerspectiveCell` ligger i `CellApple`, som Palazzo ikke bygger på |
| F6: svaret viser oppnåelse | `PurposeComposition.evaluate` (oppfylt, delvis, ikke oppfylt, og hva som mangler), `GoalDefinition` og `GoalEvaluation` | Behandling av mål som venter på at et menneske bekrefter |
| F7: husets graf | Formen: `InterestPurposeCandidate` (id, beskrivelse, interessevekter), som i restaurantmodellen din | Dataene |

### Funn i kjernen

Ingen av dem rettes i denne oppgaven. De er ført opp så du kan ta dem som en egen liten oppgave i `CellProtocol`.

| # | Funn | Sted på pinnen | Hva det betyr her |
|---|---|---|---|
| K1 | `Perspective.addPurpose` skriver «Adding purpose: ⟨navn⟩» til standard ut uten betingelse (også nådd fra `updatePurpose` og `buildPurposeList`). Tre steder til skriver navn på interesser, formål og entiteter når en oppdatering kommer med et annet navn enn det som står. En testfunksjon skriver interessenavn, og dekodingen skriver én linje uten navn | `CP/Sources/CellBase/PurposeAndInterest/Perspective.swift`: linje 198 (uten betingelse); 725, 779 og 835 (ved ulikt navn); 701–709 (testfunksjonen); 51 (dekodingen) | Navn på det gjesten har sagt om seg selv ville havnet i containerens logg. Samtalens Perspective bygges av kjernens typer (`Interest`, `Purpose`, `Weight`) uten å kalle funksjonene i `Perspective` som skriver ut, og en test fanger standard ut for hele kallet. Kjernens diagnoselogg skriver også navn når domenet `semantics` er slått på; det er av som standard, og testen krever at det er av |
| K2 | Ingen offentlig måte å fjerne en aktiv interesse på. Et aktivt formål kan bare fjernes ved å sette hele listen på nytt (`setPurposeJsonData`). Entiteter kan fjernes én og én | samme fil, linje 958–1059 og 1074–1077; `PerspectiveEntityProjection.swift`, linje 82, 128, 198 | «Fjern» på siden kan ikke bygges på et Perspective som lever i tjenesten uten å utvide kjernen. Det er én grunn til valg 3 |
| K3 | `getActiveInterests` siler på `weight >= minWeight` med standard 0,0 | samme fil, linje 965–970 | En interesse med negativ vekt («liker ikke») kommer ikke med uten at kallet ber om det |
| K4 | Ingen test i kjernen bruker negative vekter i den vektede summen. Regningen gir −0,9 for −1,0 × 0,9, uten avkorting | `CP/Tests/CellBaseTests/InterestPurposeWeightedSumTests.swift`; `InterestPurposeWeightedSum.swift`, linje 177 (lest av lesetråden, regnet og ikke kjørt) | Fortegn virker etter koden, men er ikke holdt fast av noen test |
| K5 | Fristen i grafkjøringen sjekkes bare når en ny ramme tas ut av køen | `CP/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift`, linje 441–444 | Med ett hopp blir det én sjekk per interesse. Greit for 35 poster; ført opp fordi `complete` avgjør om en match gjelder |
| K6 | Målmotoren har ingen egen behandling av `human-confirmation`, og setter aldri `not-started` | `CP/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift` (lest av lesetråden) | «Målet er nådd når retten er servert» kan ikke avgjøres av kjernen i dag. Gjesteflaten sier det samme: «No pretend Goal evaluator» (`PS/Sources/App/Models/PalazzoSignalGraph.swift`, linje 264) |
| K7 | `Perspective.getInterest(name:)` lager en ny interesse når navnet ikke finnes | `CP/Sources/CellBase/PurposeAndInterest/Perspective.swift`, linje 391–399 | Slås det opp med gjestens ord, havner ordet i grafen. Dekomponeringen slår bare opp noder som finnes i husets graf |
| K8 | `updateInterest` og `updatePurpose` legger noden til og kaster likevel en feil første gang | samme fil, linje 716–723 og 771–777 | De kan ikke brukes til å bygge et Perspective per kall uten å fange feilen. Planen bruker dem ikke |
| K9 | `RelationalLearningEngine` avkorter vekter til 0–1 og avviser hendelser utenfor | `CP/Sources/CellBase/PurposeAndInterest/RelationalLearningModels.swift`, linje 511–516; resten lest av lesetråden | Revisoren (F4) kan ikke bruke den til «liker ikke» slik den står |

## To veier for koden

Spørsmålet gjelder det kjernen mangler: regelen som gjør tekst til interesser. Resten bruker kjernen slik den er, uansett vei.

| | Portet til Palazzo nå (anbefalt) | Løftet til kjernen først |
|---|---|---|
| Hva som skrives | Én fil i `PS` med rene funksjoner uten Palazzo-typer: normalisering, bøyningsregelen, nektelse. Butlers 26 tester (`CS/Tests/AppTests/ButlerSignalMatcherTests.swift`) kopieres ordrett for det de gjelder. Det conciergen trenger i tillegg (fortegn, «uten», sammensetninger for korte ord, lengste term vinner), ligger i en egen fil | Samme funksjoner i `CellProtocol/Sources/CellBase/PurposeAndInterest/`, med testene. Butler i CellScaffold byttes til å kalle kjernen. Palazzo får ny pin |
| Depoter som berøres | `PalazzoScaffold` | `CellProtocol` (main, utgivelse), `CellScaffold` (Butler og hans tester), `PalazzoScaffold` (ny pin, hele testmengden på nytt) |
| Hva som må virke før conciergen viser noe | Ingenting utenfor Palazzo | En utgivelse av `CellProtocol`, og at alt mellom pinnen og main tåles av Palazzo. Hvor langt main ligger foran pinnen, er ikke målt |
| Faren | To kopier av regelen som kan gli fra hverandre | At conciergen venter på tre depoter, og at en feil i regelen treffer Butler samtidig |
| Hva som holder faren nede | Filen sier hvilken commit den er kopiert fra, og testene er Butlers egne. Å løfte senere er å flytte filen | Alt prøves mot funksjon og formål før det pushes til `CellProtocol` main, slik regelen din sier |
| Passer med | «match først», og at treffet måles før noe løftes | Det du sa 21. september: «en gjennomgående funksjonalitet i hele CellProtocol» |

Jeg anbefaler å porte nå og løfte når regelen er målt og angrepet. Da løftes noe som har tålt et angrep, og Butler får det i samme oppgave. Løftet og funnene K1–K3 hører sammen og kan gå til Codex som én oppgave i `CellProtocol`.

## Regningen

G1 godkjente at matchen regner «slik gjesteflaten regner i dag (vekt ganger andel felles emner), på kjernens graftyper», og testen `test.match.en-regning` krever at conciergen og gjesteflaten kaller samme funksjon. Etter å ha lest kjernen må jeg si at det finnes to ferdige regninger, ikke én:

| | Gjesteflatens (`PS/Sources/App/Models/PalazzoSignalGraph.swift`, linje 234–246) | Kjernens (`CP/Sources/CellBase/PurposeAndInterest/InterestPurposeWeightedSum.swift`) |
|---|---|---|
| Sum per rett | gjestens vekt × (emner som treffes / alle rettens emner), ganget med `negativeScale` når bidraget er negativt | gjestens vekt × vekten på kanten, summert over felles interesser |
| Vekt på kanten fra emne til rett | nei, alle teller likt | ja |
| Terskel | ja, i vektene du valgte (`PalazzoWeightPolicy`) | nei |
| Sier om søket ble fullstendig | ja, gjennom `WeightedGraphRuntime` | ja, `complete` |
| Brukt av | gjesteflaten på nett | kjernens måleverktøy, blant annet restaurantmodellen |

`PDD/graf/emner-v1.md` har begge regnet på de samme emnene. For «Jeg liker ost» gir begge osteretten først: 0,333 mot 0,143 for ostekaken og 0,125 for Arancini med gjesteflatens, og 1,0 mot 0,4 for Arancini og 0,3 for ostekaken med kjernens. Andreplassen bytter altså mellom de to. De skiller seg når en rett har mange emner: i gjesteflatens regning taper den selv om emnet er det retten er.

**Forslaget:** conciergen kaller gjesteflatens funksjon, slik G1 sier, og funksjonen utvides så en kant kan bære en vekt: andelen blir summen av vektene på emnene som treffes, delt på summen av alle rettens vekter. Med enhetsvekt er det nøyaktig dagens regning, og gjesteflatens tester (`PS/Tests/AppTests/PalazzoSignalGraphTests.swift`, `PalazzoWeightPolicyTests.swift`) skal stå grønne uten endring. Det er beviset på at regningen er den samme. Da har revisoren (F4) vekter å foreslå endringer i, og det finnes fortsatt bare én regning i Palazzo. Kjernens `complete` avgjør om en match gjelder: et ufullstendig søk er en bom, aldri en rangering. Det er regelen kjernens restaurantmodell selv følger («A partial search is not a ranking»).

Om gjesteflaten og conciergen senere skal over på kjernens sum, er et spørsmål for målingen og en egen oppgave.

## Samtalens Perspective

Du skrev: «Vakten må også holde et Perspective for samtalen - og for gjesten om gjesten vil.» Valg D ga «Vakten, for samtalen». To måter å holde det på mellom to spørsmål:

| | På siden hos gjesten (anbefalt) | I tjenestens minne |
|---|---|---|
| Hvor det ligger | I sidens minne. Sendes med hvert spørsmål som nodeid og slag, aldri fritekst | I et lager i tjenesten, under en tilfeldig nøkkel siden får |
| Hva tjenesten holder mellom to spørsmål | Ingenting | Alt som er notert, til det utløper |
| «Fjern» | Siden tar det ut. Ingenting å slette i tjenesten | Krever fjerning i kjernens `Perspective`, som ikke finnes (K2), eller et eget lager |
| Når samtalen er slutt | Siden lukkes eller lastes på nytt | En utløpstid, som må bygges og prøves |
| «Ingenting skrives til disk» | Følger av at tjenesten ikke holder noe | Må bevises: minne, logg, omstart |
| Omstart av containeren midt i en samtale | Merkes ikke | Det som er notert, er borte |
| Kan noen sende inn noe galt | Bare nodeid-er fra husets graf og fem slag godtas. Det gjesten kan forfalske, er hva hun selv har sagt om seg selv | Samme |

Med forslaget bygger vakten et Perspective for hvert kall av det siden sender og det setningen sier, i kjernens typer, og regner med det. Det er «Vakten holder et Perspective for samtalen» uten at huset lagrer noe. Det går også i retning av det du bestemte 5. september (matchingen hos gjesten): det som er notert, bor hos gjesten, og huset ser det bare mens det svarer.

Siden sier i dag «Spørsmålene lagres ikke av denne flaten.» Den setningen byttes i bildene til «Det du sier om deg selv, huskes mens du har siden åpen, og lagres ikke.»

## Forhåndssjekken

Testen i spesifikasjonen (`test.modell-bak.forhaandssjekk`) sier at en setning med e-postadresse, telefonnummer, kortnummer eller personnummer ikke sendes til modellen. Planen har hatt tre forslag, og de to første holdt ikke:

1. Første utgave viste til de fem mønstrene Kallimachos har (`CS/Sources/App/Cells/AI/KallimachosAdvisorCell.swift`, linje 246–252). De krever «+» og landkode foran et telefonnummer, og sammenhengende sifre i et kortnummer. Kontrolltråden K4 fant det.
2. Så foreslo jeg en egen liste over det som stoppes («@», «(at)», og seks sifre eller flere). K7 og K8 fant skrivemåter som slapp gjennom, i hver sin runde: «kari(a)example.org», «kari at example.org», og et nummer delt på to meldinger.
3. Forslaget nå snur regelen til en liste over det som slipper gjennom. En setning sendes bare når hvert tegn er en bokstav, et mellomrom eller vanlig skilletegn (komma, spørsmålstegn, utropstegn, kolon, semikolon, bindestrek og anførselstegn), og et punktum bare sist i en setning. Alt annet stopper den: et siffer, en «@», en parentes, et punktum inne i et ord.

Tabellen er regnet i Python (`PDD/contract/forhaandssjekk_regnet.py`), ikke kjørt i Swift:

| Setning | Skal stoppes | Kallimachos' fem mønstre | Liste over det som stoppes | Forslaget: liste over det som slipper gjennom |
|---|---|---|---|---|
| «Ring meg på 912 34 567» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Ring 91234567» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Nummeret er +47 912 34 567» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer, tegnet «+») |
| «Nummeret er +4791234567» | ja | stopper (telefon med landkode) | stopper (seks sifre eller flere) | stopper (et siffer, tegnet «+») |
| «Ring 0047 91234567» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Ring meg på 555 1234» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Kortet er 4111 1111 1111 1111» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Kortet er 4111-1111-1111-1111» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Kortet er 4111111111111111» | ja | stopper (kortnummer) | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Fødselsnummeret er 010190 12345» | ja | stopper (personnummer) | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Kontoen er NO93 8601 1117 947» | ja | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer) |
| «Skriv til kari@example.org» | ja | stopper (e-postadresse) | stopper («@», «(at)» eller «[at]») | stopper (punktum inne i et ord, tegnet «@») |
| «Skriv til kari @ example.org» | ja | slipper gjennom | stopper («@», «(at)» eller «[at]») | stopper (punktum inne i et ord, tegnet «@») |
| «Skriv til kari(at)example.org» | ja | slipper gjennom | stopper («@», «(at)» eller «[at]») | stopper (punktum inne i et ord, tegnet «(» «)») |
| «Skriv til kari[at]example.org» | ja | slipper gjennom | stopper («@», «(at)» eller «[at]») | stopper (punktum inne i et ord, tegnet «[» «]») |
| «Skriv til kari(a)example.org» | ja | slipper gjennom | slipper gjennom | stopper (punktum inne i et ord, tegnet «(» «)») |
| «Skriv til kari at example.org» | ja | slipper gjennom | slipper gjennom | stopper (punktum inne i et ord) |
| «Nummeret er 9123» | ja | slipper gjennom | slipper gjennom | stopper (et siffer) |
| «og så 4567» | ja | slipper gjennom | slipper gjennom | stopper (et siffer) |
| «Ring meg på 912 34 fem seks sju» | ja | slipper gjennom | slipper gjennom | stopper (et siffer) |
| «Skriv til kari krøllalfa example punktum org» | ja | slipper gjennom | slipper gjennom | slipper gjennom |
| «Ring meg på ni en to tre fire fem seks sju» | ja | slipper gjennom | slipper gjennom | slipper gjennom |
| «Jeg heter Kari Nordmann og bor i Storgata» | ja | slipper gjennom | slipper gjennom | slipper gjennom |
| «Har dere bord til 4 den 12.10.2026 kl. 19:00?» | nei | slipper gjennom | stopper (seks sifre eller flere) | stopper (et siffer, punktum inne i et ord) |
| «To pizzaer og 3 øl» | nei | slipper gjennom | slipper gjennom | stopper (et siffer) |
| «Noe f.eks. med fisk?» | nei | slipper gjennom | slipper gjennom | stopper (punktum inne i et ord) |
| «Har dere noe sånt som risboller?» | nei | slipper gjennom | slipper gjennom | slipper gjennom |
| «Jeg vil ha noe søtt.» | nei | slipper gjennom | slipper gjennom | slipper gjennom |

Av 23 setninger som skal stoppes, slipper Kallimachos' mønstre 19 gjennom, listen over det som stoppes 8, og forslaget 3. Av 5 som ikke trenger å stoppes, stopper de 0, 1 og 3.

Det som slipper gjennom forslaget, er det som er skrevet med bare bokstaver: et nummer eller en e-postadresse skrevet med ord, og navn og gatenavn. Det kan ingen regel på tegn fange. Testen i spesifikasjonen kan derfor ikke holdes for alt den sier. Det er et avvik fra ordlyden du godkjente, og er ditt å ta stilling til ved G2. Gjesten har sagt ja til at setningen sendes, og siden sier det før hun svarer.

Det forslaget koster: en setning med et tall går ikke til modellen, heller ikke «To pizzaer og 3 øl» eller en med «f.eks.». Gjesten får da avvisningen som i dag, uten spørsmålet om modellen. Hvor ofte det skjer, måles i arbeidspakke 1. Er det for ofte, er alternativet listen over det som stoppes, med hullene som står i tabellen.

Regelen slik den står her, er ikke lest av en uavhengig tråd.

## Arbeidspakker

Pakkene følger bladformålene, men ikke én til én. F5 har to pakker (6 for samtalen og 12 for det varige), og F4 har to (1 for målingen, som spesifikasjonen kaller metoden for F4, og 9 for revisoren). Tre pakker er ikke bladformål (0, 10 og 11). Spesifikasjonen sier «1:1 mot bladformål»; delingen er et avvik fra det, og er ditt å godkjenne ved G2. «Tester» viser til §5 i spesifikasjonen. Der det står Losen som utfører, går bygg, tester, commit og utsetting gjennom køen på Mac-en som i `PDD/handoff/README.md`. Tiden er per runde.

| # | Formål | Hva som gjøres | Tester som skal bli grønne | Utfører | Tid per runde |
|---|---|---|---|---|---|
| 0 | Grunnlinjen (`purpose://quality.build-and-regression`) | Hele testmengden på grenens hode før noe endres (281 tester 6. oktober). Vektene: `fa66868b` inn som egen commit; benkens selvtest og gjesteflatens tester kjøres. **Stopper** hvis benken ikke gir 7 av 7 med låsen som kom etterpå | `test.build`, `test.regression` | Losen. Du: valg 10 | 1–2 t |
| 1 | Målingen (`pkg.std.maal-formaalsforstaaelse`) | Treningssett: de 121 målte spørsmålene, de 174 fra strakstiltaket, de 100 fra mai, og genererte gjestesetninger. En blind tolk (egen tråd, opake id-er, stokket) sier formål og noder for hver. Et usett sett skrives senere av tråder som ikke har sett grafen | `test.maal.opake-id`, `test.maal.produksjonsvei`, `test.maal.tilregnelighet`, `test.maal.negativer` | Losen og uavhengige tråder | 3–5 t |
| 2 | F7 Husets graf | `PDD/graf/emner-v1.json` blir datafilen i pakken (emner, ordformer, vekter, terskel, formål med måltekst, versjon). En leser bygger grafen av filen og korpuset; rettene bærer korpusets id. Versjonen vises i `state` for det nye kallet | `test.graf.dekning`, `.en-kilde`, `.formaal-har-maal`, `.versjon`, `.endring-er-data`, `.emner` | Losen | 2–3 t |
| 3 | F1 Dekomponeringen | Butlers regel portet (valg 1) med hans tester. I tillegg: fortegn i stedet for å droppe treffet, «uten» alene, sammensetninger for «vin» og «ost», lengste term vinner («østers» er ikke «ost»), og formålet fra verbet eller spørreformen. Hver tolkning har ordene som traff | `test.dekomp.ordformer`, `.nektelse`, `.formaal`, `.samme-regel`, `.uten-modell`, `.maalt` | Losen | 4–6 t, og 2–3 t per runde etter måling |
| 4 | F2 Matchen | Gjesteflatens regning utvidet med vekt på kanten (valg 2). Terskelen leses fra grafens data. En bom har en grunn med kjernens navn | `test.match.avgjoerelsen`, `.forklart`, `.en-regning`, `.terskel`, `.tid` | Losen | 2–3 t |
| 5 | F6 Svaret | Vakten bygger tilbud, forteller, kvittering og svaret på ja, av postens felt. Tilbud bare når én rett leder klart, ingen drikke med alkohol, og et ja bestiller ikke | `test.svar.formaal`, `.tilbud`, `.forteller`, `.kvittering`, `.ja`, `.ikke-alkohol` | Losen | 3–4 t |
| 6 | F5 Samtalen | `noted` i forespørsel og svar (valg 3). Bare det gjesten sier om seg selv, noteres. «Liker ikke» trekker ned uten å stenge; ved likt tall står retten gjesten ikke liker, sist (valg 19). Spør gjesten om det hun ikke liker, får hun svar: spørsmålet avgjør, ikke tallet | `test.samtale.liker`, `.liker-ikke`, `.spoersmaal-noterer-ikke`, `.synlig-og-fjernbar` | Losen | 2–3 t |
| 7 | F8 Den nye allergenveien | Etter «tåler ikke» og for spørsmål om allergi om en rett: merkingen, det beskrivelsen nevner utover den, om merkingen er bekreftet, og personalet. Aldri «trygg». **Strakstiltaket står til du har sett angrepet og sagt at det kan byttes ut** | `test.aldri.allergi`, `.allergi-svar`, `.trygg`, `.vin-og-alkohol`, `test.samtale.taaler-ikke`, `.taaler-ikke-beskrivelsen`, `.taaler-ikke-ingen-tilbud`, `.spiser-ikke`, `test.feil-er-tester` | Losen | 3–5 t, og angrepsrunder |
| 8 | F3 Modellen bak | Spørsmålet til gjesten, forhåndssjekken (valg 11), kallet med det huset kan tilby, valideringen, merket, og linjen per bom (valg 12) | `test.modell-bak.bare-tilbudt`, `.forhaandssjekk`, `.samtykke`, `.merket`, `.foert-opp`, `.gir-endring`, `test.aldri.modellen-avgjoer` | Losen | 3–4 t, og angrepsrunder |
| 9 | F4 Revisoren | En uavhengig tråd får teksten, matchens svar og modellens svar for hver treningsrad, og foreslår tillegg og vekter i formatet fra kjernens måleverktøy. Hvert forslag har radene det retter. Gevinsten måles på det usette settet. Ingen endring går inn ulest | `test.revisor.uavhengig`, `.gevinst`, `test.maal.holdout-urort`, `.uavhengig-korpus` | Uavhengige tråder; Losen fører inn; du: valg 18 | 2–3 t per runde |
| 10 | Siden (`pkg.std.gui-surface`) | `PS/Public/palazzo/index.html`, `PS/Public/js/palazzo-communale.js` og `PS/Public/css/palazzo-communale.css` etter bildene, slik du har godkjent dem (G1-GUI er ikke gitt ennå) | `test.gui.parity`, `test.gui.load-time`, `test.docs-updated` | Losen | 3–4 t |
| 11 | Angrep og utsetting (roten) | For hver av de tre utsettingene: uavhengig angrep målt én gang før push, commit av navngitte filer, CI, claimene lest, utsetting bak bryteren, måling på nett, skjermbilder mot bildene | `test.angrep`, `test.logg`, `test.eksisterende-tester`, `test.deploy.claim`, `.kvittering`, `test.live`, `test.status-current`, `test.cell.*`, `test.cells.*` | Losen. Du: slå på bryteren | angrep 1–2 t per runde; commit og CI rundt 40 min; utsetting og måling rundt 2 t |
| 12 | F5 Det varige: «Behold» | Fastsetter hva siden gir fra seg når gjesten trykker «Behold til neste gang». Selve veien til en egen entitet bygges i onboarding-oppgaven | `test.samtale.behold` | Codex (onboardingen); Losen (formatet) | venter |

### Arbeidspakke 0: vektene, slik de står nå

Lest av en lesetråd 6. oktober (`HD/maal/grunnlag-20261007/les/L3-VEKTER-OG-GJESTEFLATE.md`), rett fra git-objektene:

- Grenen som står på nett, har alt vektgrenen slik den sto 29. september (flettet i `95c06a79`). Det som mangler, er to commiter: `fa66868b` (tallene du valgte: `negativeScale` 0,5 og terskel 0, mot 1,0 og 0,05 i dag) og `96f1c5f9` (bare testkode).
- Ingen fil er endret på begge sider, så tallene kan flettes inn uten kollisjon.
- Benkens 7 av 7 ble kjørt 29. september. Etter det har grenen på nett endret regningen to steder (matcheren krever et positivt bidrag før noe tilbys; kommentaren til en avvisning arver fortegnet). Om 7 av 7 holder med dem, er ikke regnet. Derfor kjøres benken på nytt, og et annet tall stopper pakken.
- `96f1c5f9` ga 191 tester og 1 feil 3. oktober (en midlertidig mappe som ikke lot seg fjerne). Den er en annen tråds testkode, og tas ikke med her.
- Valget ditt 2. oktober er knappen «A · Anbefalt» på vektbenk-siden (`CPD/Deliverables/PDD_palazzo-tolkning-og-vektjustering_2026-09-26/STATUS.md`, linje 127). G3 venter i den oppgaven.

Terskel 0 betyr at ethvert positivt overlapp er et treff på gjesteflaten. Conciergen trenger sin egen terskel i grafens data (valg 18), fordi «ingen node når terskelen» er det som utløser spørsmålet om modellen.

### Arbeidspakke 3: tilfellene som må med

Fra Butlers tester (kopieres ordrett, listet i `HD/maal/grunnlag-20261007/les/L4-BUTLER-KALLIMACHOS.md`): halen på tre tegn for korte termer og sju for lange, at «ide» ikke treffer «identitet», at «ingen» inni «tingen» ikke er en nektelse, og vinduet på 34 tegn.

Nye for conciergen, hver med en test som har «ikke» (lærdommen `lesson.helper-bypassed-shared-negation-check`):

| Setning | Skal gi | Hvorfor den er med |
|---|---|---|
| «Jeg liker østers» | østers, ikke ost | Kollisjonen over: «osters» begynner med «ost» |
| «Jeg liker ikke ost, men jeg liker pistasj» | ost med minus, pistasj med pluss | En nektelse gjelder bare det den står foran. Butlers vindu på 34 tegn ville tatt begge |
| «Har dere dessert uten nøtter?» | formålet vite, dessert, og nøtter som noe hun unngår | «uten» alene finnes ikke hos Butler |
| «hvitvin», «rødvinsbraiserte» | vin | Butler gir ikke korte termer sammensetninger |
| «pistasi», «pistasj» | samme node | Menyen skriver ordet på to måter |
| «Pizza Tartufo» | pizzaen, ikke pizzalisten | Korte navn. Målt feil 5. oktober |
| «Jeg er ikke så glad i fisk» | fisk med minus | Nektelsen står lenger fra ordet |

### Arbeidspakke 12: hva siden gir fra seg, og onboardingen

Du spurte 6. oktober om dataene fra onboardingen lagres i brukerens entitetsdata. Svaret var nei: i dag lagres ingenting noe sted. Forslaget for når veien finnes, er at begge deler blir poster i gjestens egen entitet (`PalazzoEntityCell`, skjema `haven.palazzo.entity.v1`: `PS/Sources/App/Cells/PalazzoEntityCell.swift`, linje 46), med kilden `self`, så gjesteflatens graf leser dem som den leser et trykk i dag:

| Fra | Blir til | Postens slag |
|---|---|---|
| Onboardingen: `intent` (`food` eller `discover`) | et formål | `purpose` |
| Onboardingen: `topics` (høyst to) | interesser | `interest` |
| Conciergen: «liker», «liker ikke» | interesser med fortegn | `interest` |
| Conciergen: «vil ha ⟨rett⟩» | et formål med måltekst | `purpose` |
| Conciergen: «tåler ikke», «spiser ikke» | bare når gjesten krysser av for det, hver for seg | `constraint` |

Ingenting av dette bygges før onboarding-oppgaven har fått sin G1 (`PS/Deliverables/PDD_palazzo-onboarding_2026-10-02/`), og «tåler ikke» er en opplysning om helse. Jeg er ikke jurist og har ikke vurdert hva reglene krever.

## Eksisterende tester som berøres

Med valg 4 (nytt kall): **ingen committet test endres.** Det gjelder også de to testene som valget ditt 5. oktober kl. 08:59 åpnet for å endre (`testRunde2cModellenFaarBareAapneSpoersmaal` og `testRunde2cDetFjerdeAngrepet` i `PS/Tests/AppTests/PalazzoConciergePhrasingTests.swift`): rettlisten kommer tilbake til modellen i det nye kallet, og `ask` står som det er.

Velger du å endre `ask` i stedet, blir disse røde, regnet av en lesetråd fra påstandene i testfilene (`HD/maal/grunnlag-20261007/les/L2-CONCIERGEKONTRAKT.md`, punkt 7), ikke kjørt: fem tester i `PalazzoCommunaleFacadeTests.swift` og to i `PalazzoAllergiHenvisningTests.swift` ved et nytt felt i svaret; `testT6…` (182 målte kall) ved annen svartekst; `testT4…` i `PalazzoAllergiOrdlisteTests.swift` og flere i `PalazzoConciergePhrasingTests.swift` ved annet antall kall til modellen eller cellen; `testDetFrosneAngrepetHolder` (180 spørsmål) ved annet utfall. Hver av dem ville vært et spørsmål til deg.

Gjesteflatens tester skal stå urørt og grønne gjennom arbeidspakke 4. En rød der stopper pakken.

Før hver commit leses testendringene rett fra git (`HD/mac/testendringer-20261003.sh`).

## Det som stopper meg

Som i runde 2 og strakstiltaket, uendret:

- Et funn i et angrep stopper utsettingen. Angrepet måles før noe pushes.
- En rød kontroll stopper, også når årsaken ser ut som nettet. Den kjøres ikke om igjen uten ditt ord.
- Enhver claim på verten stopper en utsetting.
- En committet test endres ikke uten ditt ord.
- En merking ut, et svar som sier at noe er trygt, eller et tilbud etter «tåler ikke», i en måling på nett: jeg slår av bryteren og sier fra med én gang. Å slå av bryteren er det eneste jeg gjør på verten uten å spørre, og det setter siden tilbake til `ask` slik den står i dag.
- Strakstiltaket byttes ikke ut uten ditt ord.

## Veien tilbake

Første vei tilbake er bryteren for det nye kallet: av, og siden bruker `ask`, som er urørt. Det krever en omstart av containeren med ny miljøfil, ikke et nytt image. Den andre er imaget som står på nett i dag (`sha-c5058f49640fc71a2b684713e7406add9e81b183`), med skriptet fra strakstiltaket (`HD/mac/tilbake-vert-20261006.sh`, tørrkjørt, byttet aldri kjørt). Begge prøves i tørrkjøring før utsetting 1, og bryteren prøves på ordentlig i testene.

## Det planen ikke har svar på

- Hvor langt `CellProtocol` main ligger foran pinnen, og hva en ny pin ville kostet Palazzo. Ikke målt. Gjelder bare hvis du velger løft først.
- Om benken gir 7 av 7 med regningen slik den står på nett. Måles i arbeidspakke 0.
- Hva den eksterne modellen beholder av en setning den får. Ikke undersøkt.
- Om terskelen bør være én for alt, eller ulik for tilbud og for svar på spørsmål. Avgjøres etter første måling.
- Hvor godt dette treffer. Første tall på usette setninger kommer i arbeidspakke 9.

## Rettet etter kontrollen (7. oktober 2026)

Kontrolltråden K4 holdt planen, kontrakten, dataflyten, emnene og bildene mot kildene 7. oktober kl. 00:23–00:38 UTC (`HD/maal/grunnlag-20261007/kontroll/K4-HOVEDOPPGAVEN.md`). Den fant to alvorlige ting, tre feil og tolv upresise steder. Henvisningene til kjernen, regnestykkene og kontrakten slik koden er i dag, stemte. Utgaven før rettingen ligger i `HD/maal/grunnlag-20261007/kontroll/k4/foer/`.

| Funn | Sto | Står nå |
|---|---|---|
| A1 | Forhåndssjekken var Kallimachos' fem mønstre, og planen lovet at telefonnummer og kortnummer aldri sendes | Egne, strengere regler, og hva de ikke fanger (valg 11 og «Forhåndssjekken»). Av atten eksempler slipper de fem mønstrene fjorten gjennom, og forslaget fire |
| A2 | «Høy sikkerhet» sto på tilbudene i bildene uten å være nevnt, og advarselen var skjult i bilde 2 | Merkelappen er tatt bort i forslaget og lagt fram som et spørsmål, med eget bilde. Advarselen vises (`PDD/images/README.md`) |
| F1 | Bilde 4A lovet «Jeg foreslår ikke retter med ost i denne samtalen» | «Jeg foreslår helst andre retter. Spør du om ost, får du svar likevel.» Likt tall etter et «liker ikke» er valg 19 |
| F2 | «127 påstander, 0 feil» mot korpuset | 330 kontroller, og hva de er: 78 gjelder korpuset (`PDD/images/README.md`) |
| F3 | Kjernen «er lest», 29 filer | Hvem som har lest hvilke filer. Resten ble lest av en lesetråd, og det endret K1 og K2 og ga K7–K9 |
| S1 | 0,4 og 0,3 sto i en rekkefølge som byttet Arancini og ostekaken | Rettet |
| S2 | Én kollisjon i regelen (østers og ost) | Fem til, og at de skal finnes med kode |
| S3 | «Tre koblinger er holdt utenfor» | Tre ting |
| S4 | Ingen node for et allergen | Sagt som en mangel i forslaget, med hva som må inn (`PDD/contract/README.md`, `PDD/graf/emner-v1.md`) |
| S5 | Bilde 9: «liker pistasj» og «tåler ikke nøtter» på samme gjest | «liker sitron» |
| S6 | `testT4…` ført til feil testfil | Rettet |
| S7 | «Én pakke per bladformål» | Delingen er sagt som et avvik fra spesifikasjonen |
| S8 | Eksemplene hadde en annen grafversjon enn datafilen | Samme versjon |
| S9 | Bilde 8 sa «ingen rett når terskelen» | «Ingen ord i setningen treffer husets graf», som i eksempelet |
| S10 | Pizza Salina, med ansjos, blant «De andre pizzaene» | Sagt i bildeteksten, og stilt som spørsmål i `PDD/images/README.md` |
| S11 | PNG-filene på Mac-en har en blokk skyens kopier ikke har | Nevnt i `PDD/images/README.md` |
| S12 | Skjemanavnet ført til feil fil | Rettet |

To ting fant jeg selv da bildene ble rendret på nytt. Linjen om allergener hadde flertallsformen også under ett enkelt tilbud, og kvitteringen etter et ja manglet den. Begge følger nå formene koden på nett har, og kontrakten har fått det som regel 7.

### Kontrollen av rettingene

Rettingene over ble lest av en ny uavhengig tråd (K7) 7. oktober kl. 02:18–02:29 UTC (`HD/maal/grunnlag-20261007/kontroll/K7-HOVEDOPPGAVEN-RETTING.md`). Den åpnet alle elleve bildene. Den fant to alvorlige ting, tre feil og ni upresise steder i det jeg hadde rettet:

| K7 | Fant | Gjort |
|---|---|---|
| AL1 | De nye reglene for forhåndssjekken ble sagt å «dekke» telefonnumre og e-postadresser, men slapp «kari @ example.org», «kari(at)example.org» og et sjusifret nummer gjennom | Ordet «dekker» er tatt bort, og avviket fra testen i spesifikasjonen er sagt. Etter neste kontroll (K8) er regelen snudd til en liste over det som slipper gjennom; se under |
| AL2 | Jeg snevret «tåler ikke» inn til de 14 allergenene uten å si hva som skjer med «Jeg tåler ikke løk» | Tre slag noder for «tåler ikke» (allergen, emne, ukjent), og regel 2 gjelder alle (`PDD/contract/README.md`). Det ukjente tilfellet er et spørsmål til deg |
| FE1 | To steder sa at filer lå på Mac-en før de var overført | Overført, og kontrollert med md5 |
| FE2 | «Det meste av kjernen er lest» var 35 prosent av linjene | Resten er lest av en lesetråd, og avsnittet sier hvem som har lest hva |
| FE3 | Valg 19 ble sagt å avgjøre testen. Det gjelder bare én av fire regninger | Skrevet om |
| SV1–SV9 | Kontrollskriptet for bildene ble grønt i fire tilfeller det skulle fanget; «Kontrollert svar» sto over et svar tolket av en modell; flere bildetekster sa mer enn rammen viste | Skriptet er strammet og prøvd med seks endringer (`PDD/images/kilde/sjekken-proevd.txt`), bilde 8B sier «Fra menyen», og tekstene er rettet (`PDD/images/README.md`) |

Rettet kl. 02:38 UTC.

Andre runde ble lest av enda en uavhengig tråd (K8) kl. 02:39–02:50 UTC (`HD/maal/grunnlag-20261007/kontroll/K8-HOVEDOPPGAVEN-RUNDE2.md`). Den fant ingen alvorlige ting, tre feil og ni upresise steder. Tallene, linjehenvisningene til kjernen og de tre bildene som var endret, stemte.

| K8 | Fant | Gjort |
|---|---|---|
| FE1 | Flere skrivemåter av en e-postadresse slapp gjennom listen over det som stoppes («kari(a)example.org», «kari at example.org»), og teksten sa at tabellen hadde alt som slapp gjennom | Regelen er snudd til en liste over det som slipper gjennom (valg 11 og «Forhåndssjekken»). Da er det bare det som er skrevet med ord, som går ut |
| FE2 | Gamle tall for kontrollskriptet i tabellen over (279 og 54) | 330 og 78 |
| FE3 | Regel 2 sa at et emne bare leses av beskrivelsen. Emnene kommer også fra tagger, kategori og navn, og «løk» treffer ikke `hvitløk` | Regel 2 sier hva svaret ser på, og hva det ikke vet (`PDD/contract/README.md`) |
| SV1 | «Uten betingelse» gjaldt bare én av utskriftene i `Perspective` | K1 skiller dem |
| SV2 | Spørsmålet om noden `ukjent` sto ikke blant valgene | Valg 20. Valg 21 gjelder hvilke svar som har linjen om allergener |
| SV3–SV9 | `fisk` og `selleri` er både emne og allergen; hvilke ord som teller for et allergen; «null» i valg 19; «som på nett i dag» sto igjen ett sted | Rettet i kontrakten og her |

Rettet kl. 02:54 UTC. Det som er gjort etter K8, er ikke lest av en uavhengig tråd. Hver av de tre kontrollrundene fant feil i det jeg nettopp hadde rettet, færre for hver runde. Regn med at noe står igjen.

### Etter at planen ble lagt fram (7. oktober 2026 kl. 03:38 UTC)

En niende uavhengig tråd (K9, kl. 03:24–03:34 UTC, `HD/maal/grunnlag-20261007/kontroll/K9-OVERLEVERING.md`) leste overleveringen, ikke denne planen. Den fant at meldingen som la planen fram, sa for lite to steder som gjelder denne filen. Begge er sagt til Kjetil som rettelser kl. 03:38 UTC (`HD/maal/grunnlag-20261007/RETTELSE-MORGENMELDING-20261007.md`).

| Hva meldingen sa | Hva som gjelder |
|---|---|
| Valg 21 ble stilt uten å si hvilket alternativ som er anbefalt. Med «gjelder de anbefalte» ville et bart ja gjort regelen som står på nett, smalere | Et bart «G2 godkjent» velger ikke det smale. Linjen om allergener står under hvert svar til Kjetil har valgt. Ført inn tre steder her: under «Kort», over tabellen «Valg i planen», og i raden for valg 21 |
| Avviket fra «1:1 mot bladformål» under «Arbeidspakker» var ikke nevnt | Nevnt for ham i rettelsen. Teksten under «Arbeidspakker» er uendret |

Det som er ført inn her etter kl. 03:02 UTC, er ikke lest av en uavhengig tråd. Planen slik den ble lagt fram (md5 `f998d1df0d80e37e2195a8a1b2b97485`), ligger i `HD/maal/grunnlag-20261007/kontroll/k9/foer/PLAN.md`.

## Etter G2 (7. oktober 2026)

Ført av Losen 7. oktober kl. 12:30 UTC, og à jour kl. 14:55 UTC. Ikke lest av en uavhengig tråd.

**Kjetils ord**, lest ca. kl. 08:15 UTC: «G1-GUI godkjent. Vis det uten - men det burde kunne være en brukerinnstilling. Gjør rekkefølgen du foreslår. Jeg skal ha et møte med Andre kl 13. Få det deployet til da. Vis meg hvor jeg kan teste onborading». Lest slik: bildene er godkjent; et tilbud vises uten merkelappen «høy sikkerhet»; rekkefølgen under «Kort» er godkjent med de anbefalte valgene. Utsetting til kl. 13 lot seg ikke gjøre, og det ble sagt til ham kl. 08:23 UTC.

### Valg som står åpne

| # | Valg | Hvor det står |
|---|---|---|
| 10 | Vektene fra 2. oktober | **Stoppet.** Planen sa inn før matchen. Målingen `HD/formaalsmatch/svar/d165-vekter-maalt.md` ga én rød test på gjesteflaten (`testUtenFortegnetVilleKommentarenHaBlittEnGrunn`), og en rød der stopper pakken. Losen anbefaler nå alternativet i raden, å vente. Kjetil er spurt kl. 12:22 UTC: «vent» eller «inn nå». Til han har svart, bygges matchen på tallene som står i grenen (negativ vekt 1,0 og terskel 0,05) |
| 11 | Hva som ikke sendes til modellen | Ikke valgt. Gjelder utsetting 3 |
| 21 | Hvilke svar som har linjen om allergener | Ikke valgt. Linjen står under hvert svar til han har valgt |
| 22 | Merkelappen «høy sikkerhet» som innstilling (nytt krav fra Kjetil 7. oktober) | Tilbud vises uten merkelapp. Hvem som skal kunne slå den av og på, gjesten eller huset, er spurt kl. 12:22 UTC. Til han har svart, bygges siden uten merkelapp og uten innstilling |

### Valgt av Losen etter G2, som Kjetil kan si nei til

Arbeidspakke 5 og 6 er gjort presise i `PDD/contract/SAMTALE-UTSETTING-1.md`. Fem ting planen ikke sa, er valgt der, og lagt fram for Kjetil kl. 12:22 UTC. At han ikke svarer, er ikke et ja til å sette ut.

| # | Valg | Valgt | Det andre |
|---|---|---|---|
| 23 | Hvem som svarer først i det nye kallet | Matchen. Dagens oppslag svarer når matchen ikke finner noe | Dagens oppslag først, og matchen bare når oppslaget avviser |
| 24 | Når én post «leder klart» | Den er alene over terskelen, eller har minst 2,5 ganger summen til den neste. Tallet står i grafens data | 2,0 (da gir «dessert» ett tilbud; «sjømat» står på strakstiltakets liste og når ikke matchen) eller 3,0 (da gir «sitron» fem retter) |
| 25 | Etter «tåler ikke» og «spiser ikke» i utsetting 1 | Ingen tilbud og ingen liste fra matchen. «Tåler ikke» gir henvisningen som i dag. «Spiser ikke» alene gir en kvittering | Listene i bilde 4C, 6 og 7A alt i utsetting 1 |
| 26 | Når «tåler ikke» noteres | Alt i utsetting 1, selv om svaret er henvisningen som i dag | Først i utsetting 2 |
| 27 | Ordlyd som ikke står i bildene | Sju tekster, i tabellen «Det bildene ikke viser» i filen. De vises for Kjetil ved G3 | – |
| 28–37 | Ti valg til, tatt da reglene ble kjørt på husets data og lest av to uavhengige tråder (andre utgave av `PDD/contract/SAMTALE-UTSETTING-1.md`, punkt 6–15 sist i filen). De tre som betyr mest for gjesten: allergenord grafen kjenner og listen ikke har, gir henvisningen; alkoholfrie utgaver av øl, vin og brennevin tilbys aldri; det gjesten unngår, står notert når menyen er oppdatert midt i samtalen | Sagt til Kjetil kl. 14:40 UTC (`HD/formaalsmatch/meldinger/m25-punkter.md`) | Står i filen |
| 38 | Fartsgrensen for det nye kallet | Delt med `ask`: 30 kall per ti minutter per klient | En egen, romsligere grense for samtalen. Kjetil er spurt kl. 14:40 UTC |

### Avvik fra planen

- **Butlers regel for «ikke» er ikke portet** (valg 1 og arbeidspakke 3 sa «Butlers regel portet»). Ordtreffet hans er portet med testene. Nektelsen hans er et vindu på 34 tegn foran treffet, og det rekker over «men»: i «Jeg liker ikke ost, men jeg vil gjerne ha Pizza Tartufo» ville Pizza Tartufo blitt regnet som noe gjesten ikke vil ha. Conciergen leser nektelsen ledd for ledd i stedet. Sagt til Kjetil kl. 12:22 UTC.
- **Stikkordene er data, ikke kode**, og leseren av datafilen leser korpuset og artiklene selv. Se «Planbytter» i `PDD/STATUS.md`.
- **Første tall på usette setninger kom i arbeidspakke 1, ikke 9**: 176 av 281 (62,6 %) på setninger fra seks skribenter reglene ikke var skrevet mot. `PDD/maaling/rapport/MAALING-1-20261007.md`.

### Hvor arbeidspakkene står

| # | Pakke | Står |
|---|---|---|
| 0 | Grunnlinjen og vektene | Grunnlinjen er grønn (`d164`). Vektene er målt og stoppet (`d165`), se valg 10 |
| 1 | Korpus og sølvfasit | Gjort. To korpus, sølvfasit for begge. En firedel er holdt unna og er ikke lest |
| 2, 3 | Husets graf og dekomponeringen | Kompilert og kjørt i Swift: 321 tester, 0 feil med `.1` (`d170`) og `.2` (`d171`); Swift gir samme lesing som utgaven utenfor Swift for alle 769 setningene med `.1`, `.2` og `.3`. Med `.3` var tidsmålingen rød én gang (`d177`, 12,3 ms per setning mot grensen 10 ms i §5) og grønn med samme kode og `.4` (`d178`, 9,3 ms): tiden svinger med lasten. Dekomponeringen er gjort raskere i pakke 5 uten at lesingen er endret: 7,9 ms (`d180`) |
| 4 | Matchen | Kompilert og kjørt: 331 tester, 0 feil (`d173`) |
| 5, 6 | Svaret og samtalen | **Kompilert og grønne** (`d184`, med pakke 7 og 11b): 375 tester, 0 feil med datafil `.5`. Swift og utgaven utenfor Swift gir det samme på 166 samtaler (421 steg), og alt som står notert i et svar, godtas av neste forespørsel. Lest av to uavhengige tråder før bygg; funnene er rettet. Ordlyden som ikke står i bildene, står i `ACCEPT.md` for Kjetil ved G3 |
| 10 | Siden | **Bygget og grønn** (`d182`: 374 tester, 0 feil). Rendret i skyen: tre rammer piksel for piksel like bildene, avvikene i `ACCEPT.md#parity`. Skriptet lest av en uavhengig tråd (`HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/kontroll/LES10-JS.md`); begge «må rettes» er rettet |
| 11 | Angrep og utsetting 1 | **Angrepet er gjort** (`d183` rød først, to ekte funn; rettet i pakke 11b; `d184`: 375 tester, 0 feil, 0 brudd). Ingenting er committet, pushet eller satt ut. Igjen: `PalazzoScaffold/README.md` og `HAVEN-Deploy/_handoff/HD-0077/README.md`; `testendringer-20261003.sh`; commit av de 28 filene i `kilde.filer` gjennom `formaalsmatch-wt-20261007.sh commit`; push til CI og utsetting bak bryteren **bare på Kjetils ord** |

Bane d ble ledig kl. 13:48 UTC; spørsmålet om bane b er bortfalt.

### Funn utenfor oppgaven

Tekstfeltet på gjestens artikkelside lagrer en avvisende setning som en interesse, og rettelsen fra 30. september dekker ikke feltet. Det er grunnen til at vektene ga en rød test. `HD/formaalsmatch/funn/FUNN-kommentarfeltet-20261007.md`. Lagt fram for Kjetil kl. 12:22 UTC med tre retninger. Kjørt i Swift kl. 13:51 UTC (`d172b`, `HD/formaalsmatch/svar/d172b-maal-kommentarfelt.md`): utregningen stemmer, også med tallene fra 2. oktober. Valget er hans; sagt igjen kl. 14:40 UTC. Ingenting er endret i `PS` for dette.
