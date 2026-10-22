# Hvorfor HAVEN? Argumenter med motargumenter

Status: batch 1 · godkjent av Kjetil 2026-10-16 · kildegrunnlag: snapshot 2026-10-07, ankre kontrollert ordrett 2026-10-15 · godkjenner: Kjetil (per batch)

Dette er de tolv argumentene rådgiversvermen merket «kan sies i dag», etter rettelser fra opponentene. Hvert argument har et motargument og et ærlig svar. Når et argument brukes i et svar om nytte, skal minst én begrensning (B1–B4 eller argumentets eget motargument) være med eller tilbys.

P1 og L1 beskriver problemer. De er ikke bevis for at HAVEN løser dem.

## Deles dataene mine med tredjeparter uten at jeg vet det?

**[med forbehold] ARG-P1.** Det er dokumentert i flere tilfeller, også i norske saker, at vanlige apper har delt personopplysninger med mange tredjeparter uten gyldig samtykke.

*Forbehold:* Si «dokumentert i flere tilfeller», aldri «alle apper». Primærkildene (Forbrukerrådets rapport fra 2020 og dommen i Grindr-saken) er ikke hentet på nytt; bare sekundærkilder er kontrollert. Dette er bevis for problemet, ikke for at HAVEN løser det.

*Motargument:* «Det er gamle tilfeller (2020); praksis kan ha blitt bedre etter håndheving.»  
*Ærlig svar:* Riktig at testen er fra 2020. Grindr-saken ble likevel stadfestet i 2025. Vi sier ikke at alt er slik i dag, bare at problemet er dokumentert og har vært straffbart.

*Skal ikke sies:* «Alle apper selger dataene dine.»

Kilder:
- Ekstern kilde: <https://www.eff.org/deeplinks/2020/01/new-report-exposes-adtech-invading-our-privacy> (sekundær-verifisert 2026-10-07 (R2); primærrapport ikke hentet)
- Ekstern kilde: <https://cms.law/en/nor/publication/gdpr-enforcement-tracker-report-2025/norway> (sekundær-verifisert 2026-10-07 (R2))
- Ekstern kilde: <https://www.grcreport.com/post/norwegian-court-upholds-fine-against-adult-dating-app-over-data-privacy-violations> (sekundær-verifisert 2026-10-07 (R2); primær dom ikke lest)

## Kan jeg se, eksportere og slette det jeg har spurt om?

**[med forbehold] ARG-P5.** Spørrehistorikken hos bibliotekaren kan eksporteres og slettes, avgrenset til deg og relasjonen du spør fra, og det finnes en navngitt test for det. I rådgiveren Kallimachos er i dag bare sletting tilgjengelig, ikke eksport.

*Forbehold:* Gjelder spørrehistorikken i cellen, ikke kostnadsposter, AIGateway-journal, flythendelser eller lagring hos modellleverandøren (HF-03-03). Testen er lest, ikke kjørt i denne gjennomgangen.

*Motargument:* «Sletting i cellen er ikke sletting overalt (backup, logger, modellleverandør).»  
*Ærlig svar:* Riktig. Påstanden gjelder spørrehistorikken. Brukes en ekstern modell, sies det i svaret.

*Skal ikke sies:* «Alt om deg er slettet overalt.»

Kilder:
- `CellScaffold/Tests/AppTests/CommonsLibrarianCellTests.swift` linje 273: «testAuditExportAndDeleteAreRequesterAndRelationScoped»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 42: «static let deleteHistoryKeypath = "deleteHistory"»
- `raadgivere/O1_opponent.md` linje 29 (intern rådgiverrapport, ikke offentlig kilde): «R1 F2: rådgiveren eksponerer bare 'deleteHistory', ikke eksport.»

## Hvorfor er innlåsing et problem?

**[kan sies] ARG-L1.** Når det koster mye å bytte og verdien ligger i nettverket, blir brukere og organisasjoner låst til én leverandør. Dette er grundig beskrevet i økonomisk forskning, og britiske konkurransemyndigheter har pekt på slike byttehindringer i skytjenester.

*Begrensning:* Generell teori. Det er ikke bevis for at HAVEN fjerner innlåsing.

*Motargument:* «Innlåsing kan også gi stordriftsfordeler og bedre produkter.»  
*Ærlig svar:* Ja. Forskningen sier ikke at innlåsing alltid er skadelig, bare at den gir leverandøren makt. Spørsmålet er om du kan gå når du vil.

Kilder:
- Ekstern kilde: <https://eml.berkeley.edu/~farrell/ftp/lockin3.pdf> (metadata-verifisert 2026-10-07 (R2); innhold ikke lest)
- Ekstern kilde: <https://www.gov.uk/government/news/cma-announces-package-of-actions-on-business-software-and-cloud-services.> (verifisert 2026-10-07 (R2))

## Trenger katalogsvar en språkmodell?

**[med forbehold] ARG-L6.** Når bibliotekaren svarer rett fra katalogen, kalles ingen språkmodell og ingen nettverkstjeneste, og det finnes en navngitt test for det. Rådgiveren Kallimachos kaller i dag likevel en modell for hvert spørsmål som slipper gjennom evidensporten.

*Forbehold:* Gjelder katalogsvar fra bibliotekaren, ikke rådgiversvar. Blir riktig også for rådgiveren først når svar uten modell er eget nivå og standard.

*Motargument:* «Deterministiske svar er dårligere enn modellsvar.»  
*Ærlig svar:* De er smalere. Til gjengjeld er de reproduserbare og sitert ordrett.

Kilder:
- `CellScaffold/Tests/AppTests/CommonsLibrarianCellTests.swift` linje 213: «testQueryEmitsRedactedAuditFlowAndNeverInvokesProviderOrNetworkPath»
- `raadgivere/O1_opponent.md` linje 29 (intern rådgiverrapport, ikke offentlig kilde): «Argumentene er sanne for 'CommonsLibrarianCell', men ikke for Kallimachos-rådgiveren som brukeren snakker med.»

## Hvorfor kan HAVEN være gratis for noen?

**[kan sies] ARG-V1.** Vedtektene § 4 sier ordrett: «Stiftelsen kan ta betalt av kommersiell bruk av plattformen for å muliggjøre størst mulig grad av gratis tjenester for ikke-kommersielle registrerte.»

*Begrensning:* Dette er hjemmel og formål, ikke et resultat. Stiftelsen har ingen slike inntekter å fordele i dag.

*Motargument:* «En vedtekt er en intensjon, ikke en garanti.»  
*Ærlig svar:* Riktig. Den sier hva stiftelsen har lov og formål til; driften har ennå ingen inntekter å fordele.

*Skal ikke sies:* «HAVEN er gratis for alle for alltid.»

Kilder:
- `Kallimachos/Kilder/Vedtekter_Stiftelsen_Digipomps_2019-01-03_transkripsjon.md` linje 56: «Stiftelsen kan ta betalt av kommersiell bruk av plattformen for å muliggjøre»
- `Kallimachos/Kilder/Vedtekter_Stiftelsen_Digipomps_2019-01-03_transkripsjon.md` linje 57: «størst mulig grad av gratis tjenester for ikke-kommersielle registrerte.»
- `Kallimachos/Kilder/Vedtekter_Stiftelsen_Digipomps_2019-01-03_transkripsjon.md` linje 10: «§ 4 er i tillegg identisk med formålsteksten Stiftelsesregisteret»

## Er sitatene ordrette?

**[med forbehold] ARG-T2.** Når bibliotekaren siterer katalogen, er sitatet en ordrett del av kildefila, og det finnes en navngitt test for det. Det rådgiveren formulerer med modell, er ikke sitater.

*Forbehold:* Gjelder katalogsitater. Modellsvaret kontrolleres ennå ikke mot kildene (HF-04-05).

*Motargument:* «Et korrekt sitat fra en feil kilde er fortsatt feil.»  
*Ærlig svar:* Riktig. Derfor har hver kilde ferskhet og status, og kilder vurderes for seg.

*Skal ikke sies:* «Alt Kallimachos sier er sant.»

Kilder:
- `CellScaffold/Tests/AppTests/CommonsLibrarianCellTests.swift` linje 53: «testEveryCitationExcerptIsAnExactSourceFileSubstring»

## Hva skjer når Kallimachos ikke vet svaret?

**[med forbehold] ARG-T3.** Finner bibliotekaren ikke noe i katalogen, svarer den med et ærlig hull og teller hullet, slik at noen kan fylle det. Det finnes en navngitt test for det, og rådgiveren teller også hullene.

*Forbehold:* Rådgiveren lar en modell formulere svaret også ved hull, og den formuleringen kontrolleres ennå ikke (HF-04-05).

*Motargument:* «Språkmodeller hallusinerer likevel.»  
*Ærlig svar:* Ja. Derfor er katalogsvaret deterministisk, og modellsvaret får status og kilder.

*Skal ikke sies:* «Kallimachos hallusinerer aldri.»

Kilder:
- `CellScaffold/Tests/AppTests/CommonsLibrarianCellTests.swift` linje 89: «testUnknownTopicReturnsHonestGapAndIncrementsDemandWithoutCitation»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 692: «persistedState.gapCount += 1»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 196: «catalog-gap uten citations; gapteksten er hele evidensgrunnlaget.»

## Gir samme spørsmål samme svar?

**[med forbehold] ARG-T4.** Med samme kildemanifest og samme versjon av korpuset gir bibliotekaren samme svar, og det finnes en navngitt test for det. Andre kan derfor etterprøve katalogsvaret. Det gjelder ikke modellsvar fra rådgiveren.

*Forbehold:* Gjelder katalogsvar.

*Motargument:* «Reproduserbarhet gjelder ikke modellsvar.»  
*Ærlig svar:* Riktig, og det sies.

Kilder:
- `CellScaffold/Tests/AppTests/CommonsLibrarianCellTests.swift` linje 170: «testSameManifestAndGitSnapshotProduceSameIndexHashAndIdenticalAnswer»

## Har HAVEN brukere og effektdata?

**[kan sies] ARG-B1.** Ærlig status per 2026-09-07: HAVEN har ingen brukere utenfor teamet, ingen feltcase, ingen effektdata, ingen uavhengig sikkerhetsrevisjon og ingen ekstern operatør som har drevet det i minst 90 dager.

*Begrensning:* Listen må friskes opp ved hver endring i tillitspakken eller modenhetsmatrisen; den skal oppdateres, ikke slettes.

*Motargument:* «Da er alt det andre bare ord.»  
*Ærlig svar:* Det andre er byggesteiner og prinsipper med status. Nytten er ikke vist; det er nettopp det vi vil teste.

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 96: «Users outside the team · a field case · effect data · an external operator running HAVEN for ≥ 90 days»
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 96: «an independent security audit or penetration test»

## Hjelper HAVEN meg hvis ingen andre bruker det?

**[kan sies] ARG-B2.** Et personvernvennlig alternativ hjelper deg bare hvis tjenestene du trenger, er med. I dag er de ikke det.

*Motargument:* «Da er det ingen grunn til å begynne.»  
*Ærlig svar:* Grunnen er å teste i avgrensede miljøer der nettverket er lite (for eksempel én konferanse), ikke å love bred nytte.

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 96: «Users outside the team · a field case»
- Ekstern kilde: <https://eml.berkeley.edu/~farrell/ftp/lockin3.pdf> (metadata-verifisert 2026-10-07 (R2); innhold ikke lest)

## Hvor godt forstår Kallimachos hva jeg vil?

**[kan sies] ARG-B3.** Uten språkmodell treffer Kallimachos riktig formål øverst i 17–32 % av tilfellene i vår egen måling: 32 % totalt og 17 % på holdout (96 meldinger, 17 formål), og 44 % blant de tre øverste. Det er ikke målt på et uavhengig korpus.

*Begrensning:* Egen måling med meldinger skrevet av teamet og modeller. Tidligere erfaring er at holdout fra samme skribenter overdriver gevinsten.

*Motargument:* «Da er formålsruting ubrukelig.»  
*Ærlig svar:* Den er tidlig. Det viktige er at tallet publiseres, ikke skjules.

*Skal ikke sies:* «Kallimachos forstår hva du vil.» · «Kallimachos treffer omtrent en tredjedel.»

Kilder:
- `Book/38_Measuring_Purpose_Understanding_Without_A_Model.md` linje 93: «96 meldinger mot 17 formål. Riktig formål øverst 32 % (holdout 17 %), blant tre øverste 44 %.»
- `raadgivere/O1_opponent.md` linje 35 (intern rådgiverrapport, ikke offentlig kilde): «Si «17–32 % (n=96, holdout 17 %), ikke målt på uavhengig korpus».»

## Hva skjer hvis grunnleggeren slutter?

**[kan sies] ARG-B4.** HAVEN avhenger i dag i stor grad av grunnleggeren. At andre kan drive og vedlikeholde det, er ikke vist.

*Begrensning:* Saklig, ikke personlig: vurder begrunnelser, ikke personer.

*Motargument:* «Stiftelsesformen sikrer kontinuitet.»  
*Ærlig svar:* Den sikrer formål og styre, ikke kompetanse eller vedlikehold.

Kilder:
- `Kallimachos/Claude outputs/B3_OPPONENT.md` linje 195: «noen andre enn grunnleggeren vedlikeholder systemet»
- `Kallimachos/Claude outputs/B3_OPPONENT.md` linje 195: «founder-dependence og for kort historikk»
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 96: «an external operator running HAVEN for ≥ 90 days»
