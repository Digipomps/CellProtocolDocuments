# TESTRESULT — palazzo bordbestilling

Skrevet 7. oktober 2026 av Losen, og skrevet om samme natt etter at fem uavhengige tråder hadde lest koden og dokumentene (se «Uavhengig kontroll» nederst). Alt under er kjørt på Kjetils Mac gjennom køen (bane d), i arbeidstreet `_worktrees/palazzoscaffold-bordbestilling`, mot CellProtocol-pinnen `81601a6f835252aba7e99d43786fb5d67227c245`. Hver kjøring er `swift build` og så `swift test --disable-sandbox --skip-update`, med CellProtocol fra `/tmp/cp-verify/CellProtocol`. Seks av kjøringene gikk med `--filter` og kjørte bare en del av testene; tabellen sier hvilke. Skriptet er `HAVEN-Deploy/_handoff/HD-0077/mac/bordbestilling-wt-20261007.sh`. Stier er relative til HAVEN-roten. Tidene er UTC; norsk tid er to timer senere.

Svaret fra hver kjøring ligger i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/svar/`, og hele loggen i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/logg/`.

## Oversikt

| Kjøring | Tid (UTC) | Hva | Resultat | Logg eller svar |
|---|---|---|---|---|
| d136 | 6. okt. 23:31 | Utgangspunktet `31ce1ae7`, ingen endring. Hele testmengden | 281 tester, 0 feil | `logg/test-20261006T233251Z.log` |
| d137 | 23:42 | Reglene og testene av dem. Bare regeltestene (`--filter`) | 16 tester, 0 feil | `logg/test-20261006T234231Z.log` |
| d138 | 23:43 | Reglene med én innsatt feil. Bare regeltestene | 16 tester, 33 feil i 6 tester | `logg/test-20261006T234402Z.log` |
| d139 | 23:50 | Cellen, rutene og endringene i seks eksisterende filer. Hele testmengden | 298 tester, 0 feil | `logg/test-20261006T235053Z.log` |
| d140 | 23:56 | Testene gjennom rutene lagt til. Hele testmengden | 310 tester, 0 feil | `logg/test-20261006T235646Z.log` |
| d141 | 23:57 | Cellen med fire innsatte feil. Bare celletestene | 12 tester, 67 feil i 7 tester | `logg/test-20261006T235827Z.log` |
| d142 | 7. okt. 00:00 | Grense per gjest lagt til. Hele testmengden | 312 tester, 0 feil | `logg/test-20261007T000109Z.log` |
| d143 | 00:02 | Første commit | `7976bb15c8ce525f343103e98ebbb2f82be48568` | `svar/d143-commit.md` |
| d144 | 00:09 | Det committede treet en gang til, etter en retting i kjøreskriptet (se under). Hele testmengden | 312 tester, 0 feil; arbeidstreet rent | `svar/d144-etter-commit.md` |
| d145 | 01:05 | Rettingene etter kontrollen, første runde. Hele testmengden | 326 tester, 0 feil | `logg/test-20261007T010619Z.log` |
| d146 | 01:08 | Åtte innsatte feil i reglene, og cellen og kelnerflaten slik de sto i første commit. Testene med «Booking» i navnet | 47 tester, 55 feil i 13 tester | `logg/test-20261007T010831Z.log` |
| d147 | 01:09 | Låsen i cellen brutt med vilje. Bare testen med tolv samtidige bestillinger | 1 test, 2 feil: alle tolv fikk bord | `logg/test-20261007T011012Z.log` |
| d148 | 01:28 | Rettingene, andre runde (etter kontrollen av rettingene). Hele testmengden | 328 tester, 0 feil | `logg/test-20261007T012856Z.log` |
| d149 | 01:30 | Elleve innsatte feil i den andre runden. Testene med «Booking» i navnet | 49 tester, 22 feil i 9 tester | `logg/test-20261007T013118Z.log` |
| d150 | 01:33 | Utgaven som ble committet. Hele testmengden | 328 tester, 0 feil | `logg/test-20261007T013410Z.log` |
| d151 | 01:35 | Commit, stoppet av skriptet: listen hadde filer uten endring. Ingenting ble committet | — | `svar/d151-k-commit.md` |
| d152 | 01:35 | Andre commit, med listen rettet til de sju endrede filene | `7eb404f1f8e3baf16e93f8a1b1447ed1c6f3b508` | `svar/d152-k-commit-2.md` |
| d153 | 01:36 | Det committede treet en gang til. Hele testmengden | 328 tester, 0 feil; arbeidstreet rent | `logg/test-20261007T013702Z.log` |

## En ting ved kjøringene selv

Bygget startes gjennom launchd, fordi køens grense for filstørrelse ellers stopper det. launchd starter et slikt skript på nytt når det er ferdig. I kjøringene d136–d142 begynte derfor et nytt bygg i sekundene før jobben ble fjernet, og de første linjene av det står sist i hver logg. Tallene for de kjøringene er lest fra den første, fullstendige kjøringen i hver logg: i loggen for d142 står `--- swift test rc=0` på linje 4479, rett etter oppsummeringen med 312 tester, og omstarten begynner på linje 4480. Skriptet er rettet, så en omstart nå avslutter med en gang. Loggene fra d144 og utover slutter med `--- swift test rc=…` og har ingen omstart. Skriptet det er bygget over, `HAVEN-Deploy/_handoff/HD-0077/mac/cp-pin-verifiser-og-test-20260929.sh`, har samme feil og er ikke rettet.

## Utgangspunktet {#baseline}

Målt i arbeidstreet før første endring, ikke hentet fra en rapport:

```
  byggets rc=0 etter 71s
  swift build rc=0
  swift test rc=0
	 Executed 281 tests, with 0 failures (0 unexpected) in 9.492 (9.502) seconds
```

## Bygg {#build}

Utgaven som er committet i `7eb404f1` (d150). Filene som ble kopiert inn i arbeidstreet, med md5:

```
    a9549b1021718d0d18a7c31b181d9b9f  Sources/App/Models/PalazzoTableBookingModels.swift
    892b3e1ea9aae46dd42fa536d1c4b050  Sources/App/Cells/PalazzoBookingCell.swift
    c9fd1d2242d945f3652ec68f241ff60c  Tests/AppTests/PalazzoTableBookingEngineTests.swift
    abb668693366c291d59a191325cc6d1e  Sources/App/Support/PalazzoScaffoldContract.swift
    6bad9ce3a395ec8e0961f116a16d94ec  Sources/App/configure.swift
    0bec56c547056acb50b74867ce2c439b  Sources/App/routes.swift
    72464a8d9307acc696972e8b530d2087  Sources/App/Cells/PalazzoScaffoldInfoCell.swift
    b5c55cc10fc8c057b0c694e8db009974  Sources/App/Cells/PalazzoStaffShellCell.swift
    fc9e064770ec9586dc35721d22fffee1  README.md
    44eede8ea8e1adf546d5d3fb1524de5c  Tests/AppTests/PalazzoBookingCellTests.swift
    b0a895a6d00e7fddffc191e652441eef  docs/Bordbestilling_2026-10-07.md
  kopiert: 11 filer
  byggets rc=0 etter 30s
  swift build rc=0
```

Alle elleve er lest tilbake fra git-objektene etter commiten, uten å kjøre git gjennom den delte mappen, og er like det som står over. Commiten har `7976bb15` som forelder, og grenreferansen peker på den.

## Hele testmengden {#regression}

```
  swift test rc=0
	 Executed 328 tests, with 0 failures (0 unexpected) in 10.065 (10.076) seconds
```

Det er den siste oppsummeringslinjen i loggen for d150. 281 tester fantes fra før; alle er med og grønne. Ingen eksisterende test er endret, fjernet eller hoppet over. 47 er nye: 27 av reglene (`PalazzoTableBookingEngineTests`) og 20 i celletestene (`PalazzoBookingCellTests`). 31 av dem kom i første commit, 16 i den andre. I den andre commiten er hjelperen som leter etter dobbeltbestilling i regeltestene, utvidet til å se over midnatt; den brukes av tester fra første commit, og de er grønne med den.

## Reglene {#regler}

`PalazzoTableBookingEngineTests`, 27 tester, ingen celle og ingen nett.

| Test | Formål | Kom i |
|---|---|---|
| `testCalendarKnowsRealDatesWeekdaysAndTimes` | Grunnlaget: datoer som finnes, ukedager, klokkeslett | `7976bb15` |
| `testPlanProblemsAreNamedOneByOne` | B1 | `7976bb15` |
| `testClosingAnAreaTakesItsTablesOutOfAvailability` | B1 | `7976bb15` |
| `testStartTimesFollowTheSeatingAndTheWeekday` | B2 | `7976bb15` |
| `testCapsPerStartApplyToGuestsAndNotToTheHouse` | B2 | `7976bb15` |
| `testSmallestFittingTableIsChosenAndNeverGivenTwice` | B3 | `7976bb15` |
| `testTablesAreJoinedOnlyWhenNoSingleTableFits` | B3 | `7976bb15` |
| `testAHoldEndsWhenTheDurationIsOver` | B3 | `7976bb15` |
| `testGuestMustHitABookableTimeAndStayUnderTheHouseLimit` | B4 | `7976bb15` |
| `testCancellingFreesTheTableAndObeysTheDeadlineForGuests` | B4 | `7976bb15` |
| `testAChangeThatDoesNotFitLeavesTheBookingUntouched` | B4 | `7976bb15` |
| `testMarkingFollowsTheAllowedTransitions` | B4 | `7976bb15` |
| `testAGuestCannotHoldMoreOpenBookingsThanTheHouseAllows` | B9 | `7976bb15` |
| `testWalkInTakesATableNowOrIsRefused` | B5 | `7976bb15` |
| `testWaitlistHoldsNoTableAndCandidatesAppearAfterACancellation` | B6 | `7976bb15` |
| `testOverviewCountsCoversTablesAndKeyFigures` | B7 | `7976bb15` |
| `testABookingHasNoFieldForGuestDetails` | B8 | `7976bb15` |
| `testTheGuestsOwnRecordCarriesTheInstantAndNothingAboutTheTable` | B9 | `7976bb15` |
| `testATableHeldPastMidnightIsNotGivenAgainTheNextDay` | B3 | `7eb404f1` |
| `testAGuestStoppedByACapCanStandOnTheWaitingList` | B6 | `7eb404f1` |
| `testAGuestOnTheWaitingListCannotTakeATableAfterTheTimeHasStarted` | B6 | `7eb404f1` |
| `testAGuestsChangeNeedsANewConfirmationWhenTheHouseConfirmsItself` | B4 | `7eb404f1` |
| `testTheHouseKeepsTheTablesItPointedOutWhenItChangesABooking` | B4 | `7eb404f1` |
| `testAGuestCanChangeThePartySizeOfABookingTheHouseMovedOffTheGrid` | B4 | `7eb404f1` |
| `testAChannelIsOneOfAClosedListAndNeverFreeText` | B8 | `7eb404f1` |
| `testAPlanCannotRemoveOrShrinkATableSomeoneHolds` | B1 | `7eb404f1` |
| `testStoredStateThatCannotBeReadIsAnErrorAndNotAnEmptyHouse` | Lagringen: det som ikke lar seg lese, er en feil | `7eb404f1` |

Kalenderregningen (dager siden 1970, ukedag) er i tillegg holdt mot Pythons kalender for hver dag fra oktober 1967 til april 2134, i Losens skyarbeidsområde: 0 avvik. Det er en kontroll av formlene, ikke av Swift-koden.

## Rutene {#ruter}

`PalazzoBookingCellTests`, 20 tester. Sytten går gjennom HTTP-rutene som gjest, ansatt og hus. Én leser cellens lagrede tilstand tilbake. To prøver sammenslåingen på kelnerflaten som ren funksjon.

| Test | Formål | Kom i |
|---|---|---|
| `testHouseSetsThePlanAndABrokenPlanIsRefusedWithEveryProblem` | B1 | `7976bb15` |
| `testPlanCannotRemoveATableSomeoneHolds` | B1 | `7976bb15` |
| `testAnAreaCanBeClosedAndOpenedAgain` | B1 | `7976bb15` |
| `testGuestBooksAndTheBookingLandsInTheirOwnEntityWhileTheHouseKeepsNoDetails` | B3, B8, B9 | `7976bb15` |
| `testTheSameTableIsNeverGivenTwiceAndAFullHouseMeansTheWaitingList` | B3, B6 | `7976bb15` |
| `testOneGuestCannotBookOutTheHouse` | B9 | `7976bb15` |
| `testOnlyTheHolderOrTheHouseCanChangeOrCancel` | B4, B9 | `7976bb15` |
| `testGuestCannotCancelAfterTheDeadlineButTheHouseCan` | B4 | `7976bb15` |
| `testStaffCreatesSeatsWalkInsMarksAndSeesTheDay` | B5, B7 | `7976bb15` |
| `testGuestsAndUnrosteredStaffCannotReachTheHouseSide` | B11 | `7976bb15` |
| `testWaiterSeesOwnBookingsAndFindsTheGuestFromTheReference` | B10 | `7976bb15` |
| `testMergedBookingsLeaveTheImportAloneWhenTheHouseHasNoneOfItsOwn` | B10 | `7976bb15` |
| `testTheHouseCanAskItsOwnNumbersInTheSheet` | B12 | `7976bb15` |
| `testTheHouseCannotWriteGuestDetailsIntoTheChannel` | B8 | `7eb404f1` |
| `testAPlanSentWithoutAreasKeepsAClosedAreaClosed` | B1 | `7eb404f1` |
| `testThePlanCannotShrinkATableSomeoneHolds` | B1 | `7eb404f1` |
| `testTheGuestSeesThatTheHouseHoldsThePointerAndUnreadFieldsAreNamedOnAChange` | B8, B9 | `7eb404f1` |
| `testGuestsAskingAtTheSameMomentNeverShareATable` | B3 | `7eb404f1` |
| `testTheCellRefusesToStartFromStoredBookingsItCannotRead` | Lagringen | `7eb404f1` |
| `testMergedBookingsSayWhenTheHousesOwnCameBackWithoutAList` | B10 | `7eb404f1` |

## Tilgang {#auth}

`testGuestsAndUnrosteredStaffCannotReachTheHouseSide`. For en gjest, og for en `staff:`-påstand som ikke står på husets liste:

- `GET /api/booking/state` og `GET /api/booking/plan` gir 403.
- `POST /api/booking/` med `plan`, `area`, `create`, `walkin`, `mark`, `promote`, `lookup` og `overview` gir 403.
- `POST /api/cell/set` med nøkkelstien `booking.plan.set` gir 403. Det er nøkkelstien som avgjør, ikke ruten.
- `POST /api/cell/get` med `insight.bookings.upcoming` gir 403 uten avtale.
- Etterpå er bestillingen og planen som før.
- Når huset har lagt den ansatte på listen, når den husets side, men ikke planen: `POST /api/booking/plan` gir fortsatt 403.

`testOnlyTheHolderOrTheHouseCanChangeOrCancel`: en annen gjest som prøver å avbestille eller endre, får 409 med `unknown_booking`. Testen krever at meldingen er lik den for en referanse som ikke finnes.

Pakken ber om et tilfelle til: at `purpose://prompt.unknown` avvises. Cellen tar ikke imot noe formål i forespørselen, så det tilfellet finnes ikke her.

## Vist rød med vilje {#roed}

En grønn kjøring sier lite hvis testene ikke kan feile. Fem ganger i natt er koden gjort feil med vilje for å se at testene merker det. De feilaktige utgavene fra kjøringene etter kontrollen ligger i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/roed-med-vilje/`, og skriptene som lager dem (`k_muter.py` og `k2_muter.py`), i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/verktoy/`. De feilaktige utgavene fra d138 og d141 er ikke tatt vare på.

| Kjøring | Hva som ble gjort feil | Røde tester |
|---|---|---|
| d138 | Én linje i bordvalget: et bord regnes som ledig også når det er opptatt | 6 regeltester, 33 feil |
| d141 | Fire ting i cellen og kelnerflaten: ansattlisten sjekkes ikke, det gjesten sendte, legges ved svaret, ingen rader skrives til regnearket, sammenslåingen på kelnerflaten er snudd | 7 celletester, 67 feil |
| d146 | Åtte ting i reglene (samme dato for opptatte bord, ingen venteliste ved tak, ingen ny bekreftelse, huset beholder ikke bord, gjesten må alltid treffe seteplanen, fri tekst i kanalen, bord kan krympes, lagret tilstand leses mildt), med cellen og kelnerflaten slik de sto i første commit | 13 tester, 55 feil: 8 regeltester og 5 celletester |
| d147 | Låsen i cellen: lese, vente og skrive i tre grep | 1 test: alle tolv samtidige bestillinger fikk bord, der to skulle fått |
| d149 | Elleve ting fra andre runde: seks i reglene og fem i cellen | 9 tester, 22 feil: 5 regeltester og 4 celletester |

Fra d146, der kanalen var fri tekst. Teksten kom tilbake i svaret, sto i regnearket og i svaret som kan deles med en avtale:

```
testTheHouseCannotWriteGuestDetailsIntoTheChannel] : XCTAssertEqual failed: ("200 OK") is not equal to ("400 Bad Request")
testATableHeldPastMidnightIsNotGivenAgainTheNextDay] : XCTAssertEqual failed: ("["1"]") is not equal to ("["2"]")
```

Den første linjen fortsetter i loggen med hele svaret, der det blant annet står `"source":"telefon – Ola Nordmann 90000000, nøtteallergi"`. Den andre er bord 1 som ble gitt på nytt ti over midnatt.

Fra d147:

```
testGuestsAskingAtTheSameMomentNeverShareATable] : XCTAssertEqual failed: ("12") is not equal to ("2") - to bord for to finnes, så to får bord: [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
```

Det viser to ting: at de tolv kallene i testen faktisk løper samtidig inne i tjenesten, og at det er låsen som holder dem fra hverandre.

Fra d138 og d141, som før:

```
testSmallestFittingTableIsChosenAndNeverGivenTwice] : XCTAssertTrue failed - A og B deler bord ["1"]
testWaitlistHoldsNoTableAndCandidatesAppearAfterACancellation] : XCTAssertEqual failed: ("confirmed") is not equal to ("waitlisted")
testGuestBooksAndTheBookingLandsInTheirOwnEntityWhileTheHouseKeepsNoDetails] : XCTAssertFalse failed - Ola Nordmann kom tilbake i svaret
testGuestsAndUnrosteredStaffCannotReachTheHouseSide] : XCTAssertEqual failed: ("200 OK") is not equal to ("403 Forbidden") - guest:test-<uuid> GET …
```

Etter hver av de fem kjøringene ble filene satt tilbake. For d146, d147 og d149 er md5 lest rett etter tilbakesettingen, og var lik utgaven før feilene ble satt inn. For d138 og d141 står ikke md5 etter tilbakesettingen i noen svarfil, fordi filene var endret videre før neste kjøring; det som er sikkert, er at neste kjøring var grønn.

**Hvor mange av testene er vist røde.** Av de 47 nye testene er 29 vist røde minst én gang: 13 av de 31 fra første commit, og alle 16 fra den andre. De 18 som aldri er vist røde, er disse:

- Regeltester (12): `testCalendarKnowsRealDatesWeekdaysAndTimes`, `testPlanProblemsAreNamedOneByOne`, `testClosingAnAreaTakesItsTablesOutOfAvailability`, `testStartTimesFollowTheSeatingAndTheWeekday`, `testCapsPerStartApplyToGuestsAndNotToTheHouse`, `testGuestMustHitABookableTimeAndStayUnderTheHouseLimit`, `testCancellingFreesTheTableAndObeysTheDeadlineForGuests`, `testMarkingFollowsTheAllowedTransitions`, `testAGuestCannotHoldMoreOpenBookingsThanTheHouseAllows`, `testOverviewCountsCoversTablesAndKeyFigures`, `testABookingHasNoFieldForGuestDetails`, `testTheGuestsOwnRecordCarriesTheInstantAndNothingAboutTheTable`.
- Celletester (6): `testHouseSetsThePlanAndABrokenPlanIsRefusedWithEveryProblem`, `testPlanCannotRemoveATableSomeoneHolds`, `testAnAreaCanBeClosedAndOpenedAgain`, `testTheSameTableIsNeverGivenTwiceAndAFullHouseMeansTheWaitingList`, `testOneGuestCannotBookOutTheHouse`, `testStaffCreatesSeatsWalkInsMarksAndSeesTheDay`.

## Kontraktfixtures {#contract}

Ikke kjørt. Det finnes ingen kontrakt-JSON med validator for denne cellen. `contract/README.md` er en tabell skrevet fra koden, og `contract/noekkelstier.json` er en liste over nøkkelstiene, holdt mot kildefilene med et skript. Testene gjennom rutene er det som holder kontrakten i dag.

## Lastetid og finnbarhet {#load-time}

Gjelder ikke ennå. Ingen flate er bygget, så det finnes ingenting å måle lastetid på, og ingen skjelett å kjøre finnbarhetskontrollen over.

## Uavhengig kontroll {#kontroll}

Fem tråder som ikke hadde skrevet noe av dette, leste det i natt. Rapportene ligger i `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/`.

| Tråd | Leste | Fant |
|---|---|---|
| K1 | Koden i første commit | Tre alvorlige feil, fem feil og tolv svakheter |
| K2 | Dokumentene i denne mappen og beskrivelsen i repoet | To alvorlige feil, fem feil og tretten svakheter |
| K5 | Rettingene, før de ble committet | Ingen alvorlige, to feil rettingene selv hadde laget, og en rekke svakheter |

K3 og K4 leste de to andre oppgavene fra natten, ikke denne.

De tre alvorlige fra K1, og hva som ble gjort:

1. **Samme bord kunne gis to ganger over midnatt.** Opptatte bord ble regnet per dato. Rettet: regnes i minutter fra en fast dag. Prøvd i reglene.
2. **`channel` var fri tekst fra huset** og gikk i regnearket og i svaret som kan deles med en avtale. Rettet: sju faste ord. Prøvd i reglene og gjennom rutene.
3. **Lagret tilstand som ikke lot seg lese, ble til tom tilstand i stillhet.** Rettet: lesingen gir feil. Prøvd for typen og for cellen. Hva tjenesten gjør med feilen ved en omstart, er lest i kjernen og ikke prøvd.

De to feilene K5 fant i rettingene (en ny bekreftelse som ikke gjaldt utenom seteplanen, og en vei for en gjest på ventelisten til å ta bordet etter at tiden hadde begynt), er rettet og prøvd i d148–d150. Det som er funnet og ikke rettet, står under «Kjente svakheter» i `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md`.

Rettingene etter K5 er ikke lest av en uavhengig tråd. De er prøvd, og vist røde i d149.

## Det som ikke er prøvd

- **Linux.** Bygget og testene er kjørt på Mac. CI er ikke kjørt, fordi grenen ikke er pushet.
- **Omstart.** Ingen test starter tjenesten på nytt og ser at planen og bestillingene leses tilbake. Det som er prøvd, er at cellen koder seg selv og leser seg tilbake i samme prosess.
- **Samtidighet, ut over én ting.** Tolv samtidige bestillinger om to bord er prøvd. En ny plan samtidig med en bestilling er ikke prøvd, og heller ikke samtidig skriving til regnearket og til disk for seg.
- **Ekte bruk.** Ingen har brukt dette: ingen ekte plan fra Palazzo, ingen ekte gjest.
- **Midnatt gjennom rutene.** Reglene er prøvd over midnatt med faste klokkeslett. Testene gjennom rutene bruker klokken som den er, og er kjørt mellom kl. 01 og 04 norsk tid.
- **Testene to ganger i samme prosess.** Cellen er én for hele prosessen. K1 regnet ut at flere celletester ville feile om de ble kjørt to ganger uten ny prosess. `swift test` starter en ny prosess hver gang.
- **Flere kjøringer.** Hele testmengden er kjørt åtte ganger i natt med nye tester (d139, d140, d142, d144, d145, d148, d150, d153), alle grønne; tre av dem med alle 47. Det er ikke nok til å utelukke en test som feiler en sjelden gang.
