# Akseptgrunnlag — Perspective context events

2026-10-12. Implementeringen ble akseptert i det isolerte CellProtocol-arbeidstreet.
2026-10-13 er den committet og integrert i hovedarbeidstreet; se INTEGRATION.md. G1/G2/G3 er godkjent. Kjetil godkjente G3 2026-10-12:
«Jeg godkjenner G3.»

## Forventning mot faktisk

| Godkjent leveranse (§3 i FORMAALSSPEC) | Faktisk levert | Evidens / avgrensning |
|---|---|---|
| Perspective reagerer gjennom Flow og endrer kontekst/formål etter konfigurasjon | Semantic snapshot-kilder absorberes; regler velger midlertidige effektive formålsvekter; grunnvekter bevares | Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell+Context.swift; TESTRESULT.md subscription/state/purposes |
| Felles eventkontrakt, eksempler og navngitt dataflyt | ContextObservation/ContextConfiguration/ContextDecision, Explore, 5 fixtures, kontrakt og diagram | Sources/CellBase/PurposeAndInterest/PerspectiveContext.swift; ContextSchemas.swift; Docs/Perspective_Context_Events.md; contract/context-v1.json; dataflow.md |
| Demonstrasjon av morgen, jobb, foreldremøte og fysisk/digitalt nærvær | 8 morning-kombinasjoner, Flow med vekt 0→grunnvekt 0.5, uavhengige job/møte/news labels og prioritering | TESTRESULT.md purposes; evidence/completion-full.log; job/møte er regel-labels, ingen sensordemonstrasjon |
| Eventstyrt filter før Porthole | ContextFlowFilterCell absorberer kontroll og innhold; snitt innen grunnfilter; faktisk loadCell/root.flow viser blokkering ved home og levering etter departure | Sources/CellApple/PurposeAndInterest/Cells/ContextFlowFilterCell.swift; TESTRESULT.md filter; innløp målt, skjerm ikke rendret |

Kode-/test-/Docs-stiene i tabellen er relative til det isolerte CellProtocol-arbeidstreet.
Andre artefakter er relative til denne PDD-mappen. Arbeidspakkene W1–W5 svarer fortsatt
1:1 til de fem bladformålene. Ingen ny protokoll-, resolver- eller tilgangssemantikk.

## Avvik rettet

- Kildebinding/configure og samtidige transaksjoner er serialisert.
- Samme filterkonfigurasjon beholder aktiv restriksjon; kontroll-data valideres.
- Vanlig Flow etter fersk decode kobler kilder og bekrefter snapshot igjen.
- Utløp, snapshot/emisjon og avkobling avstemmes på ett evalueringstidspunkt; alle revisjonsøkninger lagres før emisjon.
- Lokal/portable formålsalias normaliseres før prioritet; duplikater innen regel avvises.
- Explore requiredKeys samsvarer med påkrevde Codable-felt og dokumentets JSON-eksempel.
- Syklisk oppkobling avvises før lokal gate, også med to uavhengige oppstarts-Tasks.

24 nye tester og full regresjon er grønne. Full kjøring: 1361 bestått, 2 hoppet over,
0 feil, exit 0. To eksisterende skips, 7 preeksisterende Explore-feil og 5 eksisterende
PDD-referansefeil er oppgitt i TESTRESULT.md; de er ikke skjult eller løst her.

## Leveranse og gjenoppretting

14 endrede/nye filer i arbeidstreet; baserevisjon og SHA-256 står i
evidence/candidate-sha256.json. evidence/candidate.patch inneholder hele kandidatens
kode/test/Docs-endring og er prøvd med git apply --check mot ren eksport av basen.
Ved G3 var kandidaten ucommittet. 2026-10-13 er den committet som 9171dcfe0dee68dfd9486388b836f00932930618 og integrert i lokal main.
Ingen push/PR eller publisering hevdes; commit-/bevaringsevidens står i INTEGRATION.md.
Det opprinnelige arbeidstreets andre endringer er bevart.

## Docs — test.docs-updated / stubs

Docs/Perspective_Context_Events.md beskriver implementerte nøkler, wire-data,
persistens, prioritet/aliaser og filter. contract/context-v1.json og dataflow.md er
avstemt. Alle nye get/set-handlere har implementert oppførsel og status/feilkvittering;
ingen ny handler er en tom stub. Felles GoalEvaluationEngine er gjenbrukt.

## Uavhengig kontroll

Codex-agent /root/review_plan (arvet modell; eksakt modell-ID ikke tilgjengelig i
verktøyresultatet) kontrollerte kilde og rettelser read-only. Rapporter og siste
akseptkontroll lagres i evidence/review.md. Kontrolløren kjørte ikke testene og
verifiserte ikke telefon, GUI eller CI. Den siste dokument-/tallkontrollen er avsluttet etter ferdig rålogg og tall;
kontrolløren recomputed terminaler og alle 14 hasher og fant ingen nye vesentlige avvik.

## Status og beslutning — test.status-current

G3 gjelder aksept av denne implementeringen med kontrollerbare semantiske kildeceller
og filter ved Porthole-innløpet. Telefon-GPS, læring av områder, faktiske tidsvinduer,
fysisk/digital gruppeoppdagelse, GUI og deploy ligger utenfor godkjent G2-omfang.
G3 er godkjent 2026-10-12 etter Kjetils uttrykkelige «Jeg godkjenner G3.»
STATUS.md og forventningskontrakten er oppdatert med denne aksepten.

## Læring

Schema/Codable og unike CellResolver-fixture-registreringer er fanget, anvendt i
kanoniske skills og synkronisert. PDD-lærdommer lagres i LESSONS.md og lessons-registeret.
Global læringskø har andre åpne/udistribuerte entries; denne oppgaven lukker sine egne.
