# Lærdommer fra implementering og kontroll

2026-10-12. Disse seks er lagt til i Book/haven_lessons_register_v0.json.
Schema og fixture-navn er også anvendt/distribuert til de kanoniske skills.

## lesson.context-purpose-alias-before-priority

Symptom: Lokal vekt 0 kunne motsies av en positiv portable alias ved materialisering.

Dokumentert årsak: Prioritetsvalget brukte rå referansestrenger mens effektivt sett identifiserte ett Purpose.

Forebygging/test: Kanoniser til samme Purpose-reference før prioritet; avvis to aliaser innen samme regel; prøv lokal 0 mot lavere portable 1.

## lesson.explore-requiredkeys-match-codable

Symptom: Schema-gyldig konfigurasjon kunne mangle felt som Codable krever.

Dokumentert årsak: Initializer-defaults endrer ikke syntetisert Decodable sine krav til ikke-optional felt.

Forebygging/test: Sammenlign requiredKeys med avvisning ved fjerning av hvert required felt; ta med nested visibility/privacy og recursive kind/all/any.

## lesson.context-startup-independent-task-cycle

Symptom: TaskLocal vernet samme kallkjede, men kildekontroll fant mulig motsatt gate-rekkefølge for to oppstarts-Tasks.

Dokumentert årsak: Uavhengige Tasks har separate TaskLocal-stakker og kunne holde hver sin connectionGate.

Forebygging/test: Serialiser uavhengige røtter før lokale gates og bevar nested scope; test to samtidige røtter i en allerede syklisk fixture.

## lesson.context-snapshot-expiry-single-timestamp

Symptom: Beslutning ved utløp kunne få endret innhold ved samme revisjon mellom emisjon og snapshot.

Dokumentert årsak: Flere Date-evalueringer innen én transaksjon kunne havne på hver sin side av validUntil.

Forebygging/test: Fang evalueringstid én gang; expire, snapshot og emisjon bruker samme tid under transaksjonsgate; prøv expiry-revisjon og gjenbekreftelse.

## lesson.shared-cellresolver-fixture-unique-names

Symptom: Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.

Dokumentert årsak: ScaffoldUnique registrering håndterer eksisterende registerReference-feil og kan beholde gamle referanser.

Forebygging/test: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.

## lesson.context-disconnect-revision-durable-before-emission

Symptom: cleanup kunne sende høyere revisjon enn lagret og forvirre en konsument
som fortsetter under Perspective-only restore. Dokumentert årsak: direkte runtime-
mutasjon ved disconnect/expire, uten save-before-emission. Forebygging: samme
candidate/save/assign/emit på alle revisjonsstier; sammenlign faktisk lagret fil og
emitted revision, og bekreft høyere revisjon etter fersk decode/snapshot.

Anvendt og distribuert til cellprotocol-contract-testing-skillen.
