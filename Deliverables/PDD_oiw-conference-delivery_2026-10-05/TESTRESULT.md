# Verifikasjon — stopp før teststart

## Første bygg

Kommando i den låste worktree-en: `HAVEN_SWIFTPM_RUNNER=/private/tmp/oiw-swiftpm-no-gc.sh scripts/run_swift_bounded.sh test --disable-sandbox --filter ConferenceCommonsStateTests`.

Baseline `e5c3434510884275cae4a732935ab4b55cf7fad9` med ukommittert kandidat. Full logg: `evidence/first-build.log`. Loggen ender med `status=1`; compiler meldte `type 'DecodingError' has no member 'dataCorruptedError'` i ConferenceCommonsCell. Ingen tester kjørte. Kilden bruker nå `Foundation.DecodingError.dataCorruptedError`. Bygget er ikke kjørt igjen.

Wrapperens `--dry-run` gjelder cache-GC; Swift-byggingen kjørte faktisk. Standard bounded-runner og delt lease ble brukt. Ingen cache-sletting ble utført.

## Kandidat etter første bygg — ikke kjørt

`evidence/candidate-manifest.json` lagrer hash for hver berørt kildefil og lister 21 nye testmetoder: 18 modell-/konfigurasjonstester og 3 publisher-policytester. Alle har status NOT RUN. Ingen eksisterende committet test er redigert av denne kandidaten.

Uavhengig kildegjennomgang førte til kandidatrettelser for stale opt-in, delvis reserverte tidsvinduer, idempotent stopp, visning av konkret møteplan, usikker lagring og private formkopier etter utløp/revokering. Senere kildearbeid la til eksplisitt nytt utkast, mål/versjon/publikum i godkjenningspayload, synlige feilmeldinger og fjernet global revisjon fra visningen. Dette er kildeendringer, ikke beståtte tester.

WP6 fikk bare additive medlemsfelt, streng nøkkel-/utløpsevaluering og nøkkelbinding ved ny publisher. Den bredere grant/revoke-kandidaten ble ikke brukt etter negative rådgiverfunn. Ingen ny medlemsendrings-/tilbakekallingsskriver er levert.

## Verifikasjonsmatrise

| Kontroll | Resultat | Bevis/begrensning |
|---|---|---|
| Første lokale bygg | FAIL før teststart | `evidence/first-build.log` |
| Bygg etter rettelser | IKKE KJØRT | Venter på Kjetils ord etter PDD A11 |
| Nye modell-/policytester | 0 kjørt av 21 skrevet | `evidence/candidate-manifest.json`; teller kilde, ikke testresultater |
| Full regresjon | IKKE KJØRT | Ingen bestått App-bygg ennå |
| Resolver, HTTP, lagringsfeil/restart | IKKE KJØRT | Modelltestene kan ikke erstatte dette |
| Web/native GUI-paritet | IKKE KJØRT | Lokal fixture-preview ble forberedt, men ikke åpnet eller vurdert |
| To verter / Entity / tapt svar | IKKE KJØRT | WP5 integrasjon gjenstår |
| Nearby/mikrofon på to enheter | IKKE KJØRT | Native adapter gjenstår |
| DiMy provider | IKKE KJØRT | Rute/grant/budsjett gjenstår |
| Swarm domene-scenario | IKKE KJØRT | Fixture er en spesifikasjon, ingen run-kvittering |
| Invitert pilot | IKKE GJENNOMFØRT | Runbook forberedt |

## Stoppregel

Gjeldende `haven-purpose-driven-dev/SKILL.md`, A11: “The check is not run again without his word.” Spørsmålet om å rette/teste videre automatisk er stilt i tråden og står ubesvart ved dette kontrollpunktet. Design/G1/G2 krever ingen ny godkjenning.
