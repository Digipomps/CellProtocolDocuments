# PerspectiveCell + felles formålstrær per skop

2026-09-12. **Eksperiment levert; kravet «målbart bedre enn alternativene» er ikke oppfylt.**
På retrospektiv fasit (**n=4**) får kandidat 6 R+@10 **0,476**, lik TF-IDF; MRR+ faller fra **0,642 til 0,544**. Holdout-valgte vekter gir R+@10 **0,393**. Det er **ikke avgjørbart** om et reelt, eierbekreftet perspektiv gir produktnytte; dette forsøket dokumenterer ingen retrospektiv gevinst.

Den separate **konstruerte flertydighetstesten** gir kandidat 6 R+@10 **0,404 mot 0,111**, men tekst + skop alene gir **0,457**. Den støtter en kontekstmekanisme i enkelte tilfeller, ikke at akkurat alle tre komponentene er best, og ikke produktnytte. Fire oppgaveeiere er fire statistiske klynger selv om hver får tolv spørringer.

**OBSERVERT** nedenfor betyr lest kode eller målte artefakter; **SIMULERT/FORESLÅTT** betyr deklarerte antakelser. Swift er ikke kjørt. Nett, modeller, git-mutasjon, Docker, bygg og nye avhengigheter er ikke brukt. Bare filer under denne PDD-mappen er skrevet. FORMAALSSPEC.md og STATUS.md er urørt. Brukerbestillingen autoriserer måleskriptet og artefaktene; ferdigheten for avgrenset analyse er brukt for kilde- og usikkerhetsdisiplin.

## 1. Hva modellen og integrasjonen faktisk representerer

| Spørsmål | OBSERVERT i kilde; ikke runtime-verifisert |
|---|---|
| Hvor er brukerens aktivt fulgte formål? | `PerspectiveCell.context: Perspective` ligger i `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:40`; den konkrete samlingen er `Perspective.activePurposes: [Weight<Purpose>]` i `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:101`. Dette er noe annet enn en tilfeldig nodes relasjon `purposes`. |
| Interesser og entiteter? | `activeInterests` og `activeEntities` er egne vektede samlinger i `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:102`; sorterte, terskelfiltrerte lesemetoder finnes ved `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:958`, `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:965` og `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:972` i samme fil. |
| Hvordan blir et formål aktivt og varig? | `upsertActivePurpose` setter/erstatter den vektede oppføringen i `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:979`. Cellens `upsertPurposes` kaller dette og persisterer i `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:814`. |
| Hva inneholder Perspective.json? | Lasting/lagring er i `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:196` og `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:215`; `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:1074` dekoder og `CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:1079` enkoder **[Weight<Purpose>]**. Det er ikke en toppnivåserialisering av alle tre aktive samlinger; separate aktive interesser/entiteters persistens kan ikke utledes av denne filbanen alene. |
| Hvordan kan konsumenter lese perspektivet? | `activePurpose` og `perspective.query.activePurposes` er registrert i `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:98` og `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:164`; payload bygges fra konteksten med interessevalg i `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:509`. `perspective.state` inkluderer også aktive entiteter ved `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:487`. |
| Hvilke kanter finnes? | `types`, `subTypes`, `parts`, `partOf`, `interests`, `purposes`, `entities`, `states` er `[Weighted]` i `CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:44`; ref kommer fra nodeIdentifier eller navn ved `CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:72`. Det finnes ikke et eget generelt skopfelt i denne nodekontrakten. |
| Er skop bare states/entities? | **Nei som strukturell begrensning:** treet kan også uttrykkes med parts/partOf eller types/subTypes. **Ukjent som ferdig kobling:** ingen aktiv område→felles skoprot→signaler-adapter ble funnet i de undersøkte Perspective-/Signal-/GraphMatch-filene. `EntityRepresentation` kan ha purposes, entities og states ved `CellProtocol/Sources/CellBase/PurposeAndInterest/EntityRepresentation.swift:79`; dette definerer ikke automatisk betydningen «jeg er på jobb». |
| Finnes allerede en annen Perspective-matcher? | `perspective.query.match` går til `matchPayload`, som sammenligner formålsreferanser og delte interessereferanser med min-vektprodukter i `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:645`, `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:684` og `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift:713`. Den banen er ikke et kall til WeightedGraphRuntime. |

### Felles trær utover Book 23

**OBSERVERT:** Book-filen har 57 noder; samme 57 + 13 supplerende pakkenoder = 70 formål brukes i dette forsøket, slik som sist. Sammenslåingen gjenbrukes fra `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/leksikon.py:33`; snapshot- og Book-hasher er kontrollert mot forrige kjøring og lagret i resultatet. Ingen nye lærdommer eller native formålsnoder er lagt i målekorpuset.

**OBSERVERT:** `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:7` har eksplisitt `purposeRef`/`parentRef`, og `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:19` eksporterer `childPurposeRefs`. Et felles konferanseundertre finnes ved `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:101`: event-deltakelse, programanbefalinger, møteutkast, møtested, gruppeavstemning, programendring og privat nettverksbygging. Arendalsuka er eksplisitt kapabilitetskontekst for demokrati/avstemning og møtested ved `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:100` og `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:104`. Det er altså mer enn bare Book 23-JSON tilgjengelig som definisjoner, men dette er en egen Swift-kilde, ikke påvist synkronisert én sannhet eller ferdig Perspective-graf.

**OBSERVERT:** «Home/Work/lunch» er representert som formålet `personal-context.semantic-state` ved `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:108`, merket candidate. Beskrivelsen er ikke bevis for et ferdig aktivt skopregister. `CellScaffold/Sources/App/Cells/MatchMaker/TestConferencePurposesCell.swift:69` returnerer bare «Test Purpose»; navnet på cellen er ikke bevis for et konferanseformålstre.

**OBSERVERT:** En kontekstpakke finnes dessuten allerede i `PurposeKnowledgeBase.contextPack`, med tokenBudget, maxPurposeNodes og fokus/utvidede refs ved `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:257`; den returnerer purposeNodes, compactText og budsjett ved `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:337`. Dette er et annet gjenbrukspunkt enn GraphMatchTool; det er ikke målt her og er ikke koblet til kandidat 6 av dette arbeidet.

**Søkedekning:** de navngitte Swift-filene, resten av `CellProtocol/Sources/CellBase/PurposeAndInterest`, `CellProtocol/Sources/CellApple/PurposeAndInterest`, `CellProtocol/Sources/CellApple/Intelligence` og tekstsøk i `CellScaffold/Sources/App`. Søk: Perspective/activePurposes, Signal/WeightedGraph, scopeRef/scopeTree, conference/Arendalsuka + purpose, parentRef, purposeTree/purposeNodes og init av Purpose. `rg` finnes ikke i dette miljøet; Python-pathlib/tekstfiltrering ble brukt. Genererte bygg, avhengigheter, personlige Perspective.json-filer, runtime-lagre og nett er ikke undersøkt. «Ikke funnet» er avgrenset til disse søkene. Arendalsuka/jobb/trening som en komplett felles skopkatalog: **ukjent**.

### Eksisterende signalmotor og det som mangler

**OBSERVERT:** `Signal` bærer relationship, weight, tolerance, token, ttl, hops, localVariables og collector i `CellProtocol/Sources/CellBase/PurposeAndInterest/Signal.swift:20`. `token` er kjøringsidentitet, ikke språktokens. HitCollector beholder beste treff per ref ved `CellProtocol/Sources/CellBase/PurposeAndInterest/Signal.swift:60`; den summerer ikke tre uavhengige komponenter.

**OBSERVERT:** `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:420` starter fra én ferdig node. Konfigurasjonen har relasjonsvalg, hopptak, TTL, minScore, maxHits og Interest-condition-kontekst ved `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:242`. Kantbidrag er `max(0, 1−abs(edgeWeight−signal.weight)/tolerance)` og multipliseres langs stien (`CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:475`, `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:594`, `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:602`). Weight er nærhet til ønsket vekt; det er ikke automatisk relevans. Evidens inkluderer kant, fra/til, bidrag og akkumulert score (`CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:38`), og treff har sti og evidens (`CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:72`). Resultatet begrenser treff ved `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:399`, men beholder visitedRefs og accumulatedEvidence.

**OBSERVERT:** MatchStrategyPlanner tar kandidatantall, interesser, graf/indeks-tilgjengelighet, tvetydighet og latensbudsjett ved `CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift:35`; den velger en plan ved `CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift:150`. Den returnerer primary/fallbacks/escalationTriggers (`CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift:128`), ikke en treffliste eller tolkning av spørsmålet. 1 000-grensen (`CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift:84`) og kost-/kvalitetsestimatene (`CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift:228`) er heuristikk, ikke denne målingens kvalitetsbevis.

**FORESLÅTT integrasjon, ingen ny motor:** (1) les eierens godkjente aktive samlinger; (2) få eksplisitt aktiv skopref med felles treversjon og valgt undertre; (3) adapter Book/pakke→Purpose/Interest/EntityRepresentation med stabile refs, inverse lærdomskanter og bevart metadata; (4) projiser tekst, perspektiv og skop til vektede seeds; (5) kjør eksisterende traversal, og kombiner de tre komponentenes normaliserte scorer utenfor collector. Et startnav med seed-kanter eller flere startkjøringer kan brukes. `signal.weight=1, tolerance=1` kan representere bidrag c med kantvekt c; dagens nesten uendelige toleranse passer ikke denne vektingen. Valg av parts kontra types, skopskifte, ukjent skop, signalterskel, cache-invalidering og eierskap må være eksplisitt. Python er en ablasjon og ingen Swift-paritetsbevis. Basisklassens tomme decoder (`CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:85`) er ikke en registeradapter.

## 2. Eksperimentkontrakt og deklarerte perspektiver

Samme evaluator, k og fasit som GRAF_OG_VEKTER: snapshot `1437e34b2faa23210156cc71ef981e20cdd57ec18a0c2739a49e1d06ab26f00f`, **19 oppgaver / 44 lærdommer, retrospektiv fasit n=4**, 15 source-positive par, ingen negative eller fullt vurderte oppgaver. `korpus.json` har 45; den er lest, men **korpus_44.json** brukes som før. `retrospektiv_fasit.json` leses direkte, og etikettene kontrolleres mot `truth_labels` (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:364`). Originalfasiten endres ikke.

P+@5 er kjent positiv / 5, makrosnitt over **19** oppgaver; sann presisjon er ukjent og øvre grense er 1. R+@10 og MRR+ har **retrospektiv fasit n=4**; total relevant dekning og sann MRR er ukjent. MRR+ bruker hele rangeringen, og MRR+@10 finnes i JSON. Avsnitt@10 er som før 20. Kjøringen bruker uendret `run_matcher` (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/evaluer.py:241`), `score` (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/evaluer.py:261`) og `paired_stats` (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/evaluer.py:294`); marginale CI og timing gjenbrukes fra `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/laer_vekter.py:127` og `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/laer_vekter.py:191`.

Alle relevansintervaller er 95 % persentil-bootstrap, **10 000 uttrekk, seed 20260912**, samme hele oppgave som enhet. Parvise tester bruker samme evaluator og eksakt fortegnspermutasjon; Bonferroni over 165 nye par/metrikker finnes i JSON. Dette korrigerer ikke for tidligere eksperimentvalg. Degenerert ΔR+-CI [0,0] betyr at de fire observerte forskjellene er null; det utelukker ikke en annen effekt på nye oppgaver.

**SIMULERT:** `perspektiver.json` har 19 redigerbare poster med kilde, linje, utdrag og filhash for semantiske felt, samt eksplisitt opprinnelse for vekter og skopkoblinger. 18 oppgaver får tre formål fra §1. Utvalget er første tre innholdsfylte rader; Butler bruker rot/A/B og admin første tre blad. Ingen mål er valgt fordi de treffer fasit. Interesser og entiteter er bokstavelige §1-termer med vekt 0,5; formål har vekt 1,0. Begrep som ikke finnes blir ukjent og aktiverer ingenting. Det er ikke innhentet data om Kjetils faktiske aktive perspektiv.

**Datagap:** `CellProtocolDocuments/Deliverables/PDD_palazzo-gjestebestilling_2026-09-03/FORMAALSSPEC.md:20` har bare tom rot. Posten får to synlige ukjent-plasser med vekt null; kravet om 2–5 kildeutledede formål kan ikke oppfylles for den oppgaven. Den beholdes i alle 19-oppgavemål. To tilknyttede termforslag er også ukjente: «kryptert» i correspondence-§1 og «Perspective» i formålsregisterets §1.

**Samtidig kildeendring oppdaget ved sluttkontroll:** denne PDD-ens FORMAALSSPEC.md har nå hash `f444b0811ae50cfbc1ceabab2401008a2fc54b39b199f8afc5b2142d8700661b`, mens uttrekkets kildehash i perspektiver.json er `077b729e4b5ba3849448e917a1a1e54573deac479f7881c215d75cfeae0348d5`. De tre brukte §1-radene er fortsatt identiske på linje 56–58; innholdet i måleprofilen er beholdt. Hvem som skrev den samtidige endringen er ukjent. Det frosne korpuset, originalfasiten og måleinputene har fortsatt sine kontrollerte hasher. Ny kjøring bruker den lagrede profilen og leser ikke dagens §1 på nytt.

Skop er manuelt simulerte områdekoblinger til eksisterende Book/pakkerøtter; hele parentRef-undertreet aktiveres med `0,8^dybde`. Samme område deler samme tre. Kandidatspesifikke §1-formål legges ikke i det felles skoptreet. Ingen skop→lærdom-kant utledes fra source-fasiten. Treet er synlig gjennom `purposeRoots`, `purposeRootSources` og resultatets `scopeNodeRefs` (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:77`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:210`). Det finnes ingen Arendalsuka-oppgave blant de 19; Arendalsuka er undersøkt i kode, ikke lagt til som ny evaluering.

| Oppgave | Simulert skop | Aktive formål fra §1 |
|---|---|---|
| agent-menylinje-og-varsler_2026-09-09 | deploy | Agenten er synlig og svarbar der Kjetil er; Tilstand i ett blikk; Tomt er ikke det samme som stille |
| arbeidsko-ai-utforere_2026-09-07 | deploy | Én arbeidskø, tre utførere, ingen postbud; Ett jobbformat = HAVEN-Deploy-task; Dispatcher på Mac-en |
| bridge-fase2-handshake_2026-09-04 | bridge | Multipleks uten svekket grense; Handshake-scope er eksplisitt; Autorisasjon per kanalåpning |
| butler-traadtre-og-widgetflate_2026-09-11 | arbeid | Rot —; ### A. Hjelpertre med ruting og skop —; ### B. Dra element ut av en flate og feste det — |
| correspondence-vedlegg_2026-09-04 | correspondence | Melding kan bære ikke-tekstlig innhold; Vedlegg refereres, ikke inlines; Manifestet ligger i det indre konvoluttet |
| entitetsdata-egen-kontroll_2026-09-08 | egne-data | Data self-determination; Første kjøring forsegler entiteten til den som startet den; Lesing krever bevis, ikke bare mutasjon |
| entitetsnokler_2026-09-04 | egne-data | En nøkkel hører til entiteten som bruker den; Hemmeligheten ligger i cellens egen persisterte tilstand; Kryptert på hvile |
| formaalsregister-som-graf_2026-09-11 | kunnskap | Formålsregisteret er én graf signalmatching kan kjøre på; Én taksonomi, én sannhet; De 39 avvikende nodene er avgjort, ikke slettet |
| haven-visionos_2026-09-10 | gui | HAVEN i rommet; Flere Portholes samtidig; Porthole er instansierbar |
| innholdsvern-lyd-20260909_2026-09-10 | musikk | Åndsverket forlater ikke huset som fil; Klartekst forlater aldri serveren; Nøkkelen går samme vei som lyden |
| musikkstatistikk-20260904_2026-09-05 | musikk | Bruk synlig, uten overvåking; Anonym: teller, ikke logg; Anonym gjennomspilling, hvis det går rent |
| palazzo-gjestebestilling_2026-09-03 | palazzo | ukjent; ukjent |
| palazzo-husk-det-jeg-sa_2026-09-05 | palazzo | «Husk det jeg sa»; Huset publiserer menyendring som signal; Tagger foreslås, huset godkjenner |
| palazzo-rollesimulering_2026-09-08 | palazzo | Hver rolle når sine formål, og hvert stopp er begrunnet; Rollene har nedskrevne formål med observerbart utfall; Simulert aktør går produksjonens vei |
| palazzo-sicilia-artikler_2026-09-07 | palazzo | Artikler som bygger formål og interesser; Artikler publiseres med godkjente tagger; Reaksjon blir post i gjestens entitet |
| scaffold-admin-delegering_2026-09-08 | administrasjon | Hvert scaffold har en organisasjonsentitet registrert som administrator, og den registreringen er lesbar uten å kjenne noen persons identitet.; En person handler bare med et mandat som navngir celle, keypath, formål, varighet og tilbakekallsreferanse.; admin.operator og de andre rolleetikettene gir fortsatt null cellemyndighet. |
| skeleton-render-paritet_2026-09-07 | gui | Eieren ser samme flate uansett klient; Veiene inn finnes; Elementene virker, ikke bare vises |
| tillitspakke-agentflaate_2026-09-08 | administrasjon | Brukeren ser, justerer og etterprøver agentflåtens myndighet; Pakken er en projeksjon av det som håndheves; Transitiv rekkevidde er synlig |
| utviklerbenk-oppgavegraf_2026-09-10 | arbeid | Oppgaven først: fra løs idé til levert endring uten å miste tråden; Idéer i tre og graf; Fangst uten beslutninger |

### Hvordan de tre komponentene kombineres

**SIMULERT metode, fastlagt før første måling:** T er uendret spike-TF-IDF cosine. P er sterkeste vektede aktivering fra hver aktiv formåls-/interesse-/entitetsnode. S er tilsvarende fra felles skoptre. Nodetekst går gjennom eksisterende leksikon og `Spread.activate(hops=1)`; hvert purposeRefs-ledd gir 0,5 × 0,5 = 0,25. En eksplisitt eksisterende formålsref kan også aktivere dens lærdomskanter direkte med 0,25. Ukjente/forkortede refs brukes bare som lokale forklaringsetiketter, aldri som oppfunne kanoniske kanter. Beviset viser sterkeste seed og sti (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:253`; `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/spredning.py:30`).

Komponentene normaliseres hver mot sin største lærdomsscore (tom komponent er null). Score = **wT·T + wP·P + wS·S**. Lik score bruker samme synkende lessonRef som TF-IDF. Full rangering gir MRR; topp-10 er samme avkorting (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:281`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:288`). Kandidat 2/3 har ingen querybidrag, selv om den felles funksjonen beregner en ubrukt tekstkomponent. Cache er semantisk innhold→aktivering, ikke oppgave-ID→fasit.

§0 og §1 er dagens retrospektive tekster, ikke bevist historisk G1-input; senere auditnotater kan gi informasjon som ikke var tilgjengelig da oppgaven startet. Dette måler ekstra deklarert kontekst. Tekst i §1 tilfører informasjon utover §0; eventuell gevinst kan ikke alene tilskrives grafstruktur. Det er heller ingen ny test av språklig forståelse, negasjon eller frie parafraser.

## Alle alternativer, samme retrospektive fasit (n=4) og samme k

Først de nye ablasjonene og uendret referanse. Vektene står som **T/P/S**; ingen tapende kandidat er utelatt.

| Kandidat (T/P/S) | P+@5 nedre grense, n=19 | R+@10, n=4 | MRR+, n=4 | Avsnitt@10, n=19 | Hva raden viser |
|---|---:|---:|---:|---:|---|
| 1 TF-IDF, uendret (1/0/0) | 0.063 [0.000, 0.158] | 0.476 [0.143, 0.833] | 0.642 [0.283, 1.000] | 20.000 [20.000, 20.000] | Referansen gjenfinner flest kjente positive sammen med 4, 6 og 6a. |
| 2 Perspektiv alene (0/1/0) | 0.011 [0.000, 0.032] | 0.107 [0.000, 0.321] | 0.291 [0.048, 0.762] | 20.000 [20.000, 20.000] | Simulert perspektiv alene gjenfinner lite av source-fasiten. |
| 3 Skoptre alene (0/0/1) | 0.032 [0.000, 0.063] | 0.420 [0.107, 0.812] | 0.206 [0.118, 0.300] | 20.000 [20.000, 20.000] | Felles skoptre gir signal, men lavere R+ og MRR+ enn referansen. |
| 4 Tekst + perspektiv (0.5/0.5/0) | 0.053 [0.000, 0.126] | 0.476 [0.143, 0.833] | 0.432 [0.130, 0.833] | 20.000 [20.000, 20.000] | Perspektivet flytter rangene uten å øke R+. |
| 5 Tekst + skop (0.5/0/0.5) | 0.042 [0.000, 0.116] | 0.420 [0.107, 0.812] | 0.552 [0.104, 1.000] | 20.000 [20.000, 20.000] | Skoptillegget senker observert R+ og MRR+. |
| 6 Tekst + perspektiv + skop (0.5/0.25/0.25) | 0.053 [0.000, 0.147] | 0.476 [0.143, 0.833] | 0.544 [0.087, 1.000] | 20.000 [20.000, 20.000] | Tre komponenter gir samme R+, men lavere P+ og MRR+. |
| 6a Teksttung (0.75/0.125/0.125) | 0.063 [0.000, 0.158] | 0.476 [0.143, 0.833] | 0.574 [0.149, 1.000] | 20.000 [20.000, 20.000] | Større tekstvekt bevarer P+ og R+, men ikke MRR+. |
| 6b Like vekter (0.333333/0.333333/0.333333) | 0.042 [0.000, 0.116] | 0.429 [0.000, 0.857] | 0.407 [0.063, 0.771] | 20.000 [20.000, 20.000] | Like vekter senker alle tre observerte relevansmål. |
| 6c Perspektivtung (0.25/0.5/0.25) | 0.042 [0.000, 0.116] | 0.429 [0.000, 0.857] | 0.283 [0.067, 0.500] | 20.000 [20.000, 20.000] | Høy perspektivvekt gir lavere R+ og MRR+. |
| 6d Skoptung (0.25/0.25/0.5) | 0.042 [0.000, 0.116] | 0.393 [0.000, 0.786] | 0.404 [0.058, 0.766] | 20.000 [20.000, 20.000] | Høy skopvekt gir lavere R+ og MRR+. |
| 6 Holdout-valgte vekter (foldvis) | 0.053 [0.000, 0.147] | 0.393 [0.000, 0.786] | 0.533 [0.065, 1.000] | 20.000 [20.000, 20.000] | Vekter valgt uten testoppgaven gir lavere R+ enn TF-IDF. |

Tidligere alternativer er **beholdt fra graf_resultater.json**, med identisk snapshot og kontrollerte kilde-/kodehasher; de er ikke trent eller målt om. TF-IDF-raden over er nøyaktig lik forrige resultat. Trening-radene under er fortsatt trening, aldri holdout. Retrospektiv fasit **n=4**.

| Tidligere kandidat | P+@5, n=19 | R+@10, n=4 | MRR+, n=4 | Avsnitt@10 | Hva raden viser |
|---|---:|---:|---:|---:|---|
| vis_alt44 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.036 [0.025, 0.046] | 20.000 [20.000, 20.000] | Registerrekkefølgen har ingen kjente positive blant de første ti. |
| dagens_tag_vis_alt | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.050 [0.029, 0.072] | 20.000 [20.000, 20.000] | Tag-rekkefølgen gjenfinner ikke source-positive i topp-10. |
| tilfeldig | 0.000 [0.000, 0.000] | 0.134 [0.000, 0.268] | 0.114 [0.081, 0.148] | 20.000 [20.000, 20.000] | En fast tilfeldig rangering er en svak kontroll. |
| bm25 | 0.042 [0.000, 0.116] | 0.393 [0.000, 0.786] | 0.539 [0.079, 1.000] | 20.000 [20.000, 20.000] | BM25 har lavere observerte mål enn TF-IDF. |
| leksikon | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] | Leksikonet har ingen dokumentert gevinst mot TF-IDF. |
| graf1 | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] | Ett hopp endrer ikke resultatet mot leksikon. |
| graf2 | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] | To hopp gir ingen målt relevansgevinst. |
| graf3 | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] | Tre hopp gir ingen målt relevansgevinst. |
| laert_refs_trening | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] | Lærte purposeRefs alene forbedrer ikke treningsrangene. |
| laert_positiv_trening | 0.074 [0.011, 0.168] | 0.673 [0.417, 0.929] | 0.708 [0.417, 1.000] | 20.000 [20.000, 20.000] | Positiv feedback forbedrer trente oppgaver. |
| laert_lukket_trening | 0.105 [0.021, 0.232] | 0.917 [0.750, 1.000] | 0.875 [0.625, 1.000] | 20.000 [20.000, 20.000] | Simulerte negative gir sterk treningsgevinst uten generaliseringsbevis. |
| hyppighet_trening | 0.053 [0.000, 0.137] | 0.500 [0.000, 1.000] | 0.356 [0.087, 0.773] | 20.000 [20.000, 20.000] | Global hyppighet gjenfinner kjente treningsoppgaver. |
| leksikon_x_hyppighet_trening | 0.053 [0.000, 0.126] | 0.714 [0.250, 1.000] | 0.458 [0.167, 0.812] | 20.000 [20.000, 20.000] | Tekst ganger popularitet hjelper på treningsdata. |
| leksikon_x_hyppighet_holdout | 0.000 [0.000, 0.000] | 0.071 [0.000, 0.214] | 0.066 [0.042, 0.095] | 20.000 [20.000, 20.000] | Popularitet feiler på utelatte oppgaver. |
| laert_lukket_holdout | 0.032 [0.000, 0.084] | 0.357 [0.000, 0.750] | 0.233 [0.049, 0.417] | 20.000 [20.000, 20.000] | Lært signalmatching slår ikke TF-IDF på holdout. |
| laert_holdout_blockervern | 0.032 [0.000, 0.084] | 0.357 [0.000, 0.750] | 0.233 [0.049, 0.417] | 20.000 [20.000, 20.000] | Blocker-vernet endrer ikke disse samlede holdout-målene. |
| tilfeldig_forventning | 0.018 [0.002, 0.038] | 0.227 [0.227, 0.227] | 0.227 [0.136, 0.317] | 20.000 [20.000, 20.000] | Eksakt tilfeldig forventning unngår en heldig eller uheldig seed. |
| Lokal embedding | ukjent | ukjent | ukjent | ukjent | Ingen offline-modell er kjørt; alternativet er fortsatt ukjent. |

### Holdout og parvise forskjeller — retrospektiv fasit n=4

Faste vekter 1–6d trenes ikke. Den ekstra 6-holdout-raden velger blant de fem forhåndsdeklarerte 6-variantene på **tre andre positive oppgaver**. Mål: først R+@10, deretter MRR+, deretter fast rekkefølge. Hele oppgaven, dens perspektiv og dens dommer utelates fra vektvalget. De 15 uvurderte får valg fra de fire positive; ingen av deres egne dommer finnes. Det samme foldvalget brukes i flertydighetstesten, uten tuning på korte spørringer. Samtlige vektsett og treningsmål per fold ligger i JSON (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:333`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:364`).

Holdout beskytter vekttreningen; det gjør ikke manuelt utformede utviklingsdata til et blindt produkttestsett.

| Utelatt oppgave | Valgt T/P/S | TF-IDF R+@10 | Fast 6 R+@10 | Holdout 6 R+@10 |
|---|---|---:|---:|---:|
| PDD_agent-menylinje-og-varsler_2026-09-09 | 0.75/0.125/0.125 | 0.571 | 0.571 | 0.571 |
| PDD_palazzo-husk-det-jeg-sa_2026-09-05 | 0.333333/0.333333/0.333333 | 0.333 | 0.333 | 0.000 |
| PDD_scaffold-admin-delegering_2026-09-08 | 0.75/0.125/0.125 | 0.000 | 0.000 | 0.000 |
| PDD_utviklerbenk-oppgavegraf_2026-09-10 | 0.75/0.125/0.125 | 1.000 | 1.000 | 1.000 |

| B − TF-IDF | Mål | n | Forskjell [95 % bootstrap] | Eksakt p |
|---|---|---:|---:|---:|
| 6 Tekst + perspektiv + skop | p5 | 19 | -0.011 [-0.032, 0.000] | 1.000 |
| 6 Tekst + perspektiv + skop | r10 | 4 | 0.000 [0.000, 0.000] | 1.000 |
| 6 Tekst + perspektiv + skop | mrr | 4 | -0.098 [-0.281, 0.000] | 0.500 |
| 6 Holdout-valgte vekter | p5 | 19 | -0.011 [-0.032, 0.000] | 1.000 |
| 6 Holdout-valgte vekter | r10 | 4 | -0.083 [-0.250, 0.000] | 1.000 |
| 6 Holdout-valgte vekter | mrr | 4 | -0.109 [-0.312, 0.000] | 0.500 |

Ingen korrigert p-verdi gir en vinner. Med retrospektiv fasit **n=4** er minste mulige tosidige fortegns-p 0,125 selv ved fire ensrettede forbedringer. «Ingen gevinst dokumentert» betyr ikke at et annet, bekreftet perspektiv umulig kan hjelpe.

## 3. Flertydighet: separat konstruert fasit

Tolv korte tekster: **status; hva mangler; rydd opp; deploy; sjekk dette; neste steg; kan vi gå videre; virker det; hva bør jeg passe på; hva står igjen; hjelp meg videre; hva gjør vi nå**. Hver prøves i de fire oppgavenes perspektiv/skop: **48 tilfeller, 12 ulike tekster, fire oppgaveklynger**. Baseline gir identisk rangering for samme tekst i alle fire kontekster, kontrollert maskinelt.

**Konstruert riktig svar = source-lærdommene til oppgaven perspektivet tilhører.** De øvrige lærdommene regnes negative bare i denne mekanismetesten. At en lærdom tilhører oppgaven betyr ikke nødvendigvis at den hjelper med «status» eller «deploy»; testen har ingen menneskelig dom av det. De 15 oppgavene uten source-lærdommer får ikke oppfunne eierfasiter. Dette er ikke en større retrospektiv fasit; den opprinnelige fasiten er fortsatt **n=4**. Implementasjon: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:428`.

Samme score/evaluator og k=5/10 som ellers. CI resampler de **fire eieroppgavene**, etter gjennomsnitt over deres tolv tekster, ikke 48 uavhengige par (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:442`). P+ er her presisjon innen den konstruerte, lukkede verdenen; sann produktpresisjon er ukjent.

| Kandidat | P+@5, 4 konstruerte klynger | R+@10, 4 konstruerte klynger | MRR+, 4 konstruerte klynger | Avsnitt@10 | Hva raden viser |
|---|---:|---:|---:|---:|---|
| 1 TF-IDF, uendret | 0.083 [0.025, 0.171] | 0.111 [0.056, 0.167] | 0.258 [0.141, 0.467] | 20.000 [20.000, 20.000] | Identisk tekst gir identisk liste i alle perspektiver. |
| 2 Perspektiv alene | 0.050 [0.000, 0.150] | 0.107 [0.000, 0.321] | 0.291 [0.048, 0.762] | 20.000 [20.000, 20.000] | Perspektiv alene slår ikke den korte tekstens R+. |
| 3 Skoptre alene | 0.150 [0.050, 0.200] | 0.420 [0.107, 0.812] | 0.206 [0.118, 0.300] | 20.000 [20.000, 20.000] | Skoptreet alene løfter samlet konstruert dekning. |
| 4 Tekst + perspektiv | 0.117 [0.021, 0.296] | 0.184 [0.035, 0.385] | 0.289 [0.095, 0.628] | 20.000 [20.000, 20.000] | Perspektivtillegget gir et mindre samlet løft. |
| 5 Tekst + skop | 0.113 [0.025, 0.200] | 0.457 [0.143, 0.828] | 0.299 [0.132, 0.486] | 20.000 [20.000, 20.000] | Denne ablasjonen har høyest samlet konstruert R+. |
| 6 Tekst + perspektiv + skop | 0.167 [0.025, 0.346] | 0.404 [0.045, 0.762] | 0.302 [0.107, 0.524] | 20.000 [20.000, 20.000] | Kontekst løfter samlet R+, men tre komponenter slår ikke tekst + skop. |
| 6a Teksttung | 0.154 [0.033, 0.312] | 0.406 [0.056, 0.756] | 0.309 [0.132, 0.516] | 20.000 [20.000, 20.000] | Mer tekst gir omtrent samme konstruerte R+ som 6. |
| 6b Like vekter | 0.163 [0.000, 0.350] | 0.419 [0.035, 0.804] | 0.268 [0.057, 0.480] | 20.000 [20.000, 20.000] | Like vekter løfter R+ litt mot 6, med lavere MRR+. |
| 6c Perspektivtung | 0.142 [0.000, 0.400] | 0.434 [0.010, 0.857] | 0.210 [0.053, 0.368] | 20.000 [20.000, 20.000] | Perspektivtung vekting løfter R+ mot 6, med lavere MRR+. |
| 6d Skoptung | 0.163 [0.000, 0.338] | 0.406 [0.021, 0.792] | 0.307 [0.062, 0.552] | 20.000 [20.000, 20.000] | Skoptung vekting gir omtrent samme R+ som 6. |
| 6 Holdout-valgte vekter | 0.150 [0.025, 0.312] | 0.406 [0.056, 0.756] | 0.291 [0.095, 0.516] | 20.000 [20.000, 20.000] | Holdout opprettholder det samlede utslaget, uten robust signifikans. |

| Eierperspektiv, snitt over 12 tekster | TF-IDF R+@10 | Kandidat 6 R+@10 |
|---|---:|---:|
| PDD_agent-menylinje-og-varsler_2026-09-09 | 0.167 | 0.607 |
| PDD_palazzo-husk-det-jeg-sa_2026-09-05 | 0.028 | 0.028 |
| PDD_scaffold-admin-delegering_2026-09-08 | 0.083 | 0.062 |
| PDD_utviklerbenk-oppgavegraf_2026-09-10 | 0.167 | 0.917 |

Kandidat 6 − TF-IDF: **ΔR+=0.292 [-0.010, 0.595], eksakt p=0.500**, Bonferroni p=1. To oppgaver bedres, én er lik, én svekkes. Byttes konteksten til hver av de tre andre oppgavene, får 6 gjennomsnittlig R+@10 **0.230**, mot **0,404** med riktig kontekst. Dette er en ekstra kontroll av kontekststyringen, ikke flere uavhengige dommer.

**Vurdering:** mekanismen kan styre samme tekst mot ulike lærdommer; det samlede utslaget er i forventet retning. Gevinsten i dette forsøket drives særlig av skop, og tre komponenter slår ikke tekst + skop. Konstruert fasit og fire klynger kan verken etablere produktnytte eller en statistisk robust generell effekt.

## 4. Kontekstpakke og AI-agent

**MÅLT uten modell:** faktisk JSON for topp-10 **lærdomsnoder**, med full symptom/cause/prevention/tags/purposeRefs og kompakt rangeringsbevis. Bevis inkluderer tekststammer og sterkeste perspektiv-/skopseed, sti og bidrag; det er bevis for rangeringen, ikke for semantisk sannhet. Høyst åtte stammer per kanal, aldri avkortet lærdomstekst. Alle pakker, tegnantall og hasher finnes i JSON (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:301`, `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:329`).

Tegn = Unicode-tegn i sortert, kompakt JSON; **grove tokens = tegn/4**. Ingen tokenizer eller modell er brukt; tallene er ikke fakturerbare modell-tokens. Query og vekter er med på begge sider. Hele-treet-baseline er 70 formål (57 Book + 13 pakkeformål med metadata), alle 44 lærdommer og samme query. Fasit/source-felt fra lærdommene er utelatt på begge sider. Dette er en deklarert alternativ kontekstpakke, ikke målt nåværende GraphMatchTool-trafikk.

Snitt over 19 pakker; forhold = gjennomsnitt av hvert par `kompakt/hel`, ikke forholdet mellom to gjennomsnitt. R+ i pakken bruker **retrospektiv fasit n=4**, samme topp-10 som hovedtabellen.

| Kandidat | Tegn, snitt | Grove tokens, snitt | Pakke / hele treet | R+ i pakken, n=4 |
|---|---:|---:|---:|---:|
| 1 TF-IDF, uendret | 14790 | 3697 | 0.129 | 0.476 [0.143, 0.833] |
| 2 Perspektiv alene | 15848 | 3962 | 0.138 | 0.107 [0.000, 0.321] |
| 3 Skoptre alene | 15839 | 3960 | 0.138 | 0.420 [0.107, 0.812] |
| 4 Tekst + perspektiv | 17430 | 4357 | 0.152 | 0.476 [0.143, 0.833] |
| 5 Tekst + skop | 17375 | 4344 | 0.151 | 0.420 [0.107, 0.812] |
| 6 Tekst + perspektiv + skop | 20276 | 5069 | 0.177 | 0.476 [0.143, 0.833] |
| 6a Teksttung | 20103 | 5026 | 0.175 | 0.476 [0.143, 0.833] |
| 6b Like vekter | 20138 | 5034 | 0.175 | 0.429 [0.000, 0.857] |
| 6c Perspektivtung | 19906 | 4976 | 0.174 | 0.429 [0.000, 0.857] |
| 6d Skoptung | 19969 | 4992 | 0.174 | 0.393 [0.000, 0.786] |
| 6 Holdout-valgte vekter | 20249 | 5062 | 0.176 | 0.393 [0.000, 0.786] |
| Hele 70-treet + alle 44 | 114299 | 28575 | 1,000 | 1,000 [1,000, 1,000] |

Kandidat 6 er **0.177×** fullpakken, omtrent **5.66 ganger mindre / 82.3 % færre tegn**; spenn mellom oppgaver 0.112–0.247. Mot bare **57 Book-noder + 44 lærdommer** er forholdet **0.202×** (fullpakken 99903 tegn). Mot en nøktern 70-nodepakke med bare ref/parent/title/summary/hints/interests er forholdet **0.281×** (fullpakken 71815 tegn). Innsparingen avhenger altså av hvor omstendelig alternativet er.

Prisen er tapt informasjon: R+ i kandidat 6-pakken er **0,476 på retrospektiv fasit n=4**, mot 1,000 når alle 44 sendes. Innsparing med bevart svar-/agentkvalitet er **ukjent**. Pakke 6 er også større enn TF-IDF-pakken fordi den bærer to ekstra beviskanaler. Påstander om at dette slår en AI-agent eller gir bedre modellbeslutninger kan ikke trekkes fra tegnregnskapet.

### Hva GraphMatchTool gjør i dag

**OBSERVERT:** `AppleIntelligenceCell` registrerer GraphMatchTool i en FoundationModels `LanguageModelSession` og instruerer modellen om å bruke verktøyet: `CellProtocol/Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:662`. Dette er den konkrete graf + språkmodell-kombinasjonen; verktøyet selv gjør ikke et eget modellkall.

`GraphMatchTool` tar kategori og `naturalLanguageQuery` (`CellProtocol/Sources/CellApple/Intelligence/Tools/GraphMatchTool.swift:50`), resolver Perspective med requester (`CellProtocol/Sources/CellApple/Intelligence/Tools/GraphMatchTool.swift:63`), men starter alltid fra `getPrimaryPurpose` (`CellProtocol/Sources/CellApple/Intelligence/Tools/GraphMatchTool.swift:119`). Kategori og fritekst påvirker ikke rangeringen; de logges/videresendes bare til en funksjon som ignorerer kategorien. Primary velger den høyest **positivt** vektede activePurpose (`CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:210`).

Signalet har interests, ønsket vekt 0,5, tolerance `Double.greatestFiniteMagnitude`, to hopp og ett sekund; konfigurasjonen traverserer alle åtte relasjoner og tar inntil 50 treff (`CellProtocol/Sources/CellApple/Intelligence/Tools/GraphMatchTool.swift:74`). For ordinære endelige vekter blir bidraget fra toleranseformelen praktisk talt 1, så de vanlige vektforskjellene skiller lite. Resultatet serialiseres i sin helhet (`CellProtocol/Sources/CellApple/Intelligence/Tools/GraphMatchTool.swift:98`): treff med refs/navn/sti/bevis, visitedRefs, samlet evidens, localVariables, tid og diagnostikk, jf. `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:399`. Det hentes ingen lærdomstekst fra dette 44-korpuset, og maxHits begrenser ikke all returnert evidens. Faktisk modelltokenbruk og svarvirkning for denne banen: **ukjent**.

**FORESLÅTT for pakke 6:** bruk spørsmålet som T, les flere aktive formål/interesser/entiteter som P, og et eksplisitt valgt/versionert skoptre som S. Bevar requesterens avtalebaserte lesetilgang ved hydrering. Materialiser ref-adapteren og seed-kanter, kjør eksisterende runtime, og kombiner kanalene med synlige vekter/normalisering utenfor best-hit-collector. Returner ti lærdomsnoder med relevante stier og full lærdomstekst i en separat budsjettert kontekstpakke; skill omfattende diagnostikk fra modellpakken. Få med ukjente refs, lav/tom aktivering og pakkens avkorting, slik at modellen kan be om mer kontekst. Gjenbruk gjerne `PurposeKnowledgeBase.contextPack`-kontrakten fremfor å lage enda en usammenhengende pakke. Dette krever adapter og konsumentendringer; ingen ny traverseringsmotor er nødvendig. Ingen av endringene er implementert i Swift her.

## 5. Billigere menneskedommer og nødvendig utvalg

[DOMMER_ventende.md](../maaling/DOMMER_ventende.md) har nøyaktig **15 uvurderte oppgaver**, hver med topp-10 fra fast kandidat 6 og uendret kandidat 1 side om side. Nummer er felles på tvers av kolonnene; unionen dedupliseres, med kort forebygging og utfellbar full symptom/forebygging og testrefs. Tre svar følger «Billig menneskeflyt»: relevante/uvurderte, gjentakelse, vern eller sann grunn til manglende vern. Ingen dom eller standardgrunn er utfylt. Kode: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:547`; eksisterende flyt er beskrevet i `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/handoff/TESTSTRATEGI_MATCHING.md:62`.

**Under ett minutt er et mål etter vanlig G1-lesing, ikke et målt resultat.** Første fem bør registrere tid og uvurdertandel. Blanketten er ikke blind siden kandidatkolonner er uttrykkelig bestilt; det kan gi forventningsskjevhet. Den er heller ikke en automatisk importfil: svar må valideres med riktig snapshot før de lagres i judge-format. Unionen kan ha opptil 20 lærdommer, og utenfor unionen forblir uvurdert. En dømt union gir pool-R+, ikke ekte total R. De fire gamle source-oppgavene er ikke menneskedømt av dette arbeidet.

For **δ=0,15 absolutte R+@10-poeng** følger vi §5 i TESTSTRATEGI. CI-grense og planlagt styrke er ulike spørsmål:

- Normal 95 %-halvbredde: `1,960 × s_d / √n < 0,15`.
- Student-t-halvbredde: `t(0,975; n−1) × s_d / √n < 0,15`.
- 80 % styrke ved tosidig α=0,05: `n ≈ ceil(((1,960+0,842) × s_d / 0,15)²)`.

Beregningene er stdlib, med numerisk t-kvantil; de **erstatter ikke** evaluatorens bootstrap (`CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:344`). De gjelder en faktisk observert forskjell på +0,15 med den antatte variansen, ikke de null forskjellene vi har nå.

| Antatt paret s_d | n, normal CI | n, t-CI | n, ca. 80 % styrke |
|---:|---:|---:|---:|
| 0.10 | 2 | 5 | 4 |
| 0.20 | 7 | 10 | 14 |
| 0.30 | 16 | 18 | 32 |
| 0.50 | 43 | 46 | 88 |

Ved s_d≈0,30: **18 dømte, tilstrekkelig uavhengige oppgaver** for at en observert +0,15 skal ligge utenfor et slikt 95 % t-intervall; **32 nye** for et grovt 80 %-styrkescenario. Ved s_d≈0,50: **46 / 88**. Normalanslaget alene er 16 / 43. Små n-scenarioer er særlig upålitelige; tosidig eksakt permutasjon kan uansett ikke gi p<0,05 med bare fire ensrettede par.

Dette er **ingen garanti** for at bootstrap-CI eller eksakt test vil gi signifikans. Dagens kandidat 6−1 har s_d=0 på retrospektiv fasit **n=4**, fordi alle fire R+-forskjeller er null; å bruke det til å anbefale null eller én ny oppgave ville vært feil. Nødvendig virkelig n er **ukjent** før en ny pilot gir varians. De 15 ventende er nyttige utviklingsdommer, men utviklingsdata skal ikke både velge og bekrefte vinneren. Etter låsing av kandidat/primærmål bør nye oppgaver brukes; relaterte Palazzo-/GUI-/driftsoppgaver er ikke nødvendigvis uavhengige. Behovet er oppgaver med vurderte relevante lærdommer, ikke et bestemt antall avkryssinger.

## 6. Hastighet og validering

macOS-26.5.1-x86_64-i386-64bit-Mach-O, Python 3.13.5. Samme metode som GRAF_OG_VEKTER §5: perf_counter, **30 varme batcher med alle 19 queryer**, ferdig indeks. Perspektiv/skop er forhåndsdeklarert og deres innholdsaktivering bufret; hver query scores på nytt. Varm tjenestevei, ikke innlesing/annotering av §1. Ingen modell eller nett. Kilde: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py:496`.

| Kandidat, 19 varme oppslag | Median ms | p95 ms | Maks ms |
|---|---:|---:|---:|
| 1 TF-IDF, uendret | 9.69 | 9.88 | 10.09 |
| 2 Perspektiv alene | 9.61 | 9.85 | 10.05 |
| 3 Skoptre alene | 9.56 | 9.91 | 12.20 |
| 4 Tekst + perspektiv | 9.54 | 9.66 | 9.74 |
| 5 Tekst + skop | 9.53 | 9.67 | 9.69 |
| 6 Tekst + perspektiv + skop | 9.52 | 9.66 | 9.71 |
| 6a Teksttung | 9.52 | 9.65 | 9.79 |
| 6b Like vekter | 9.51 | 9.62 | 9.66 |
| 6c Perspektivtung | 9.51 | 9.66 | 9.68 |
| 6d Skoptung | 9.53 | 9.76 | 12.80 |
| 6 Holdout-valgte vekter | 9.53 | 9.58 | 9.60 |
| 6, inkl. bevispakke og JSON-serialisering | 39.09 | 58.40 | 79.68 |

Alle målte varme batcher holder 100 ms-grensen. Høyeste enkeltoppslag for 6 blant 19×30 målinger: **1.05 ms**. Dette lover ikke en absolutt frist under annen maskinlast eller ved større korpus. Hele statistikkjobben tok **26.6 sekunder** og er ikke et oppslag; <100 ms for hele jobben er ikke oppfylt. Swift-ytelse, kald produktstart, skopoppdatering og faktisk modellrespons er ukjent.

**Kontrollert:** identiske input-/kodehasher mot forrige måling; 19/19 TF-IDF-rangeringer nøyaktig lik original; unike refs og riktig topp-k i alle kandidater; holdout uten egne oppgaver; identisk tekstbaseline ved kontekstbytte; 15 tomme dommerblanketter. I tillegg ble de seks hovedadapterne kjørt gjennom `evaluer.evaluate`: **114/114 rangeringer og R+-aggregater samsvarer**. Den ekstra adapterkontrollen brukte 100 uttrekk; rapportens CI bruker 10 000. Python-syntaks er parsbar. Ingen Swift-test eller bygg er kjørt.

## Reproduksjon og leveranse

Fra HAVEN-roten:

```sh
python3 -B CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/perspektiv_skop.py
```

Dette bruker eksisterende `perspektiver.json`, skriver `perspektiv_resultater.json` og regenererer den tomme DOMMER-blanketten. **Fjern GENERATED-kommentaren før menneskesvar fylles inn**; da nekter skriptet å overskrive dommerfilen. `--init-profiles` er bare for første opprettelse og nekter å overskrive eksisterende perspektiver. Etter Kjetils rettelser er inputhashen ny; behold tidligere resultat ved behov og rapporter neste runde som ny deklarasjon, aldri samme blinde test.

Leveranser: [perspektiv_skop.py](../maaling/perspektiv_skop.py), [perspektiver.json](../maaling/perspektiver.json), [perspektiv_resultater.json](../maaling/perspektiv_resultater.json), [DOMMER_ventende.md](../maaling/DOMMER_ventende.md), denne rapporten og [svar.md](../svar.md).

**Åpent:** eierbekreftede perspektiver; §1-innhold for gjestebestilling; aktivt Arendalsuka-/jobb-/treningsskop med grafadapter; flere uavhengige menneskedommer; reell effekt på språkmodellens svar; embedding-/agentbaseline; Swift-integrasjon og ytelse. Ingen av disse er påstått levert. Hypotesen er undersøkt innen mandatet; nyttekravet står ubekreftet.

