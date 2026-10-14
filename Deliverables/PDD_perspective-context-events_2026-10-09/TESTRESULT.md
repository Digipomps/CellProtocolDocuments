# Testresultat — Perspective context events

2026-10-12. Målt lokalt med Apple Swift 6.4 / Xcode 27 på macOS arm64.
Kandidatens base er 253b4afe11af8b58bfcc433d9b7dc7393c761e24. De 14 endrede/nye
filene er låst med SHA-256 i evidence/candidate-sha256.json. Koden ligger ucommittet
i det isolerte arbeidstreet knyttet til chatten; evidence/candidate.patch er en
kontrollert gjenopprettbar kopi. Ingen eksisterende committet test er endret.

## Baseline

S0: 30 bestått, 0 feil (evidence/baseline.log). Filteret omfattet eksisterende
GoalEvaluationEngine-, GoalEvaluationCell- og Perspective-tester.
En tidligere utvidet kjøring har 95 beståtte test-terminaler i evidence/extended.log;
statusloggen oppga tidligere 94. Den korrigerte opptellingen kommer fra råloggen.
Disse tallene summeres ikke med senere kjøringer.

## Build og regression

Kommando fra det isolerte CellProtocol-arbeidstreet:

```sh
HAVEN_SWIFTPM_CACHE_KEY=perspective-context-events bash scripts/haven-swiftpm.sh -- test --disable-sandbox
```

Endelig full kjøring: exit 0; 1363 startet og avsluttet, 1361 bestått, 2 hoppet over,
0 feil. CellBaseTests-bundlen kjørte 1334 tester; øvrige bundler inngår i totalsummen.
Alle 24 nye PerspectiveContext-tester inngår og bestod. Rålogg:
evidence/completion-full.log. Maskinlesbar opptelling: evidence/test-counts.json.

Hoppet over: AudioSignalAnalysisTests.testReferenceFileMatchesChapter34AndIsDeterministic
og MatcherBaselineDumpTests.testWriteMatcherDump. De samme to finnes i den tidligere
fullkjøringen evidence/full-tests.log. Ingen nye tester er ekskludert.

Fokusert kjøring med --filter 'PerspectiveContext': 24 bestått, 0 feil
(evidence/durable-focused.log). Den kontrollerer den siste varige avkoblingsrettelsen;
fullkjøringen over kontrollerer hele pakken etterpå. En første kompilering
overlapppet redigeringen av oppkoblingshjelperen og fikk «no member perform» mellom
CellBase og CellApple. Råloggen er beholdt i evidence/completion-build-overlap.log.
Ny kompilering og begge avsluttede testkjøringer er grønne. Det hevdes ikke at hver
ny test ble kjørt rød før implementering.

## Dependencies

Ekte GeneralCell.attach/absorbFlow og Perspective.flow er målt i
PerspectiveContextFlowTests.testRealSubscriptionChangesEffectivePurposesAndDepartureRestoresBaseline.
Integrasjon bruker CellResolver.sharedInstance med unike registreringsnavn, faktisk
CellResolver.loadCell og root.flow. Dette er innløpet CellViewModel bruker for
Porthole. Det beviser levering til innløpet; skjermrendring, telefon og sensorer er
ikke målt. Cell-lokal filpersistens er målt gjennom fersk decode/readiness og
avkobling, og lagrefeil avviser kvittering og ny state.

## Subscription — test.context.subscription

Ekte abonnement mottar ankomst og avreise. Ukjent sourceID avvises i modelltesten
for forsinkede/konfliktende eventer. Etter detach emitterer fixture-kilden igjen;
state/revisjon står uendret og ingen context.changed leveres i observasjonsvinduet.
Konfigurasjonsendring er en separat tillatt transition og er prøvd i scenario-testen.
Kontroll-eventer konsumeres ved Perspective/filter.

## State — test.context.state

PerspectiveContextTests dekker full snapshot-state, kjent tom label-liste,
duplikat/eldre revisjon, konflikter ved samme revisjon, samtidig sted/tid/nærvær,
utløp og gjenbekreftelse etter restart. Utløp øker revisjonen én gang; et utløpt
snapshot bekrefter ikke gammel tilstedeværelse. Integrasjonstestene sammenligner også faktisk lagret revisjon med emisjonen ved
kilde-snapshotfeil, og høyere revisjon etter standalone restore. De måler lagret
disabled kilde, vanlig Flow-oppstart etter fersk decode, og at lagrefeil ikke
bekrefter eller installerer ny konfigurasjon.

## Purposes — test.context.purposes

Tilstandene nedenfor er verifisert med XCTest-assertions, ikke telefonmålinger:

| Inngang / overgang | Verifisert resultat | Test |
|---|---|---|
| Alle 8 kombinasjoner av morning/home/family | morning akkurat når morning AND (home OR family) | testMorningNeedsTimeAndHomeOrFamilyAndKnownEmptySources |
| Home-event, regelvekt 0, deretter departure | Familieformål utelatt, så grunnvekt 0.5 gjenopprettet | testRealSubscriptionChangesEffectivePurposesAndDepartureRestoresBaseline |
| Overlappende regler og lik prioritet | Høyeste prioritet; leksikalsk regel-ID ved likhet; vekt 0 tillatt | testPrioritySupportsLowerWeightsAndDeactivationAndStableTies |
| Lokal vekt 0 med lavere prioritert portable vekt 1 | Ett kanonisk formål; høy prioritet deaktiverer; to aliaser i samme regel avvises | testPurposeAliasesUseOnePriorityWinnerAndDuplicateAliasesAreRejected |
| Office, fysisk parents, digital parents, important news | Uavhengige job/parent-meeting/digital-meeting/news-alert labels; fysisk avreise avslutter bare fysisk møte | testJobParentMeetingDigitalGroupAndNewsLabelsAreIndependentRules |

Jobb/møte/nyhet demonstreres som aktive regel-labels i den siste testen.
Formålsvekter demonstreres i Flow-/prioritets-/alias-testene. Reelle geofencer,
tidsvinduer og person-/gruppegjenkjenning inngår ikke i kandidatens implementering.

## Explanation — test.context.explanation

State/Flow inneholder labels, activeRules, purposeWeights, purposeRules,
sourceRevisions, unknownSources og validUntil. Modelltestene avstemmer vinnende
regel og revisjon. Flow-testen observerer home og departure-beslutninger; samme
observasjon har ingen ingest-effekt. Utløp, snapshot og emisjon bruker samme
fangede evalueringstid. Selvreferanse og to uavhengige samtidige sykliske oppstarter
returnerer feil innen testens 3-sekundersgrense. Malformet kontroll-data avvises.

## Filter — test.context.filter

Faktisk resolver-lastet root.flow: home leverer news.family, blokkerer news.work
og lekker ingen perspective.context.changed til innholdet. Departure-testen
sender news.work én gang under home (0 leverte i vinduet), så etter departure
(1 levert). Samme filterkonfigurasjon beholder aktiv restriksjon. Modelltesten
verifiserer snitt av flere restriksjoner innen grunnfilteret og tilbakefall til
grunnfilter ved ukjent/utløpt kontekst. Nyhet som kilde kan aktivere news-alert-regel;
filterpolicy bruker regel-labels uavhengig av hvilken semantisk kilde de kom fra.

## Auth — test.cell.auth-negative

Ny konfigurasjonstest bruker ikke debug-bypass for negativ requester-test og avviser
ikke-eier. Ukjent purpose://prompt.unknown som formålsreferanse avvises.
GeneralCellInterfaceTests i fullkjøringen dekker ugyldige/blanke keypaths, sentral
autorisasjon og at requester ikke eskalerer rettigheter utover template.
EntityAnchorAccessBoundaryTests.testUnknownPurposeFailsClosed er også grønn.
Disse eksisterende kontrollene er ikke erstattet av formålsmatch.

## Contract — test.cell.contract-fixtures

checks/validate_contract.py: 5/5 positive/negative observasjonsfixtures korrekte
(evidence/contract-validator.log), også kjørt av Swift-testen for golden fixtures.
Schema-testen sammenligner publiserte requiredKeys med faktisk Codable-avvisning
ved fjerning av hvert påkrevd GoalDefinition-felt. Nested evidence/privacy/predicate
krav er prøvd; rekursive barn beskrives eksplisitt i Explore-descriptoren.

Explore-audit: 324 komplette av 335 handler-operasjoner, 7 feil og 20 advarsler.
Ren base: 318 av 329, også 7 feil/20 advarsler. Finding-listene er identiske;
ingen ny finding fra kandidaten. Dette er ikke en grønn global audit.
Se evidence/audit-base.json, evidence/audit-final.json og evidence/audit-comparison.json.

Den globale purpose_dev-validatoren har 5 eksisterende ugyldige lesson-referanser;
logg lagres som evidence/pdd-validation.log. Ingen grønn global PDD-status hevdes.

## Lokal integrasjon 2026-10-13

Etter commit 9171dcfe0dee68dfd9486388b836f00932930618 og fast-forward til lokal main er 103
berørte tester bestått direkte i hovedarbeidstreet (alle 24 nye konteksttester),
0 feil/skips, exit 0. Brukerens tidligere staged/untracked endringer er bevart.
Dette summeres ikke med G3-fullpakken over. Se INTEGRATION.md og
evidence/integration-2026-10-13/main-test-result.json.
