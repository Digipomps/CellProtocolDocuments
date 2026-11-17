# ACCEPT — Palazzo concierge native web

2026-09-14 · Teknisk avstemming for WP0–WP4: **skrevet, verifisert med full regresjon**.
Dette er ikke Kjetils G3-godkjenning. Standalone/parity er fortsatt WP5.

| Forventning | Faktisk resultat | Evidens |
|---|---|---|
| Native offentlig ask uten nettleserhemmelighet | 200, fem pizzaer, minst én kilde; også uten Authorization i produksjonsmodus med token satt | [public-ask](TESTRESULT.md#public-ask) |
| Samme gjestekonvolutt og native route | Nøyaktig avtalt feltsett inkludert reason_code; native route; norsk tekst og kildefilter | [envelope](TESTRESULT.md#envelope) |
| Ærlig state | remoteMode native, limited for datert bundlet korpus, dato 2026-06-03 hentet fra cellen | [state-svar](evidence/responses/state.json) |
| Gateway-/privatgrense beholdes | Generisk API og eksisterende concierge-API avviser uten token; faste offentlige handlinger/principal | [auth](TESTRESULT.md#auth) |
| 30/10 min og 4096 byte | 31. forsøk gir 429; ugyldige forsøk teller; 413 over bytegrensen; remote/forwarded-fallback testet | [auth](TESTRESULT.md#auth) |
| Samme flate fra Public | HTML/JS/CSS og alle åtte refererte temaressurser gir 200; DOM-struktur og CSS-regler bevart | [leaf](TESTRESULT.md#leaf) |
| Bevar allergen- og nekt-semantikk | Seks nekt-scenarier på norsk; alle 20 eksisterende concierge-tester grønne; celle/korpus uendret | [refusal](TESTRESULT.md#refusal) |
| Bygg og full regresjon | Native arm64-bygg grønt; full swift test med lokalt x86_64/XCTest-valg: 116/116, exit 0 | [build](TESTRESULT.md#build), [regression](TESTRESULT.md#regression) |
| Filbevis | SHA-256-manifest, førbilde, statisk audit, kommandoer og rålogger | [files](TESTRESULT.md#files) |

## docs

`PalazzoScaffold/README.md` har «Offentlig concierge (/palazzo)» med
`Last verified against code: 2026-09-14`. Teksten beskriver ruter, konvolutt,
husets autoritetsbane, forwarding-forutsetning, datert korpus, lagringsgrense og
den faktiske lokale testkommandoen. Den tidligere formuleringen om token på
«alle kall» er presisert for principal-beskyttede API-er.

Avklaringer mot den gamle flaten:

- `configuration` er webmetadata. Den gamle Porthole-CellConfiguration er ikke portert; Porthole er utenfor denne slicen.
- «Åpne i HAVEN» bruker den eksisterende HAVEN-verten som foreløpig antakelse. Linkmålet er ikke nettverksverifisert.
- Demo-spørsmål 5 gir nekt-svar: native korpus kan ikke bekrefte en «helt uten hvete»-filtrering. Ingen kunnskap eller allergenregel er utvidet for å få et positivt svar.
- OFL-notiser for de kopierte fontene ligger i CSS-kommentarer. Bare de åtte refererte runtime-filene er kopiert under temaet.

## status

STATUS-loggen og PLAN-tabellen angir WP0–WP4 som utført/målt med de faktiske
testbegrensningene. G3 står fortsatt venter på Kjetil/WP5. Standard native
`swift test` er dokumentert som blocked av lokal lasterarkitektur; alternativ
full XCTest-kjøring er grønn og fjerner ingen tester. Ingen deploy, git eller
commit-pakke inngår i denne endringen.

## stubs

Ingen offentlige no-op-handlere er lagt til. De tre POST-rutene kaller ekte
kontraktsnøkkelstier via `PalazzoCellAccess`; state leser cellens status og
configuration returnerer eksplisitte webmetadata. Administrasjonsruter er
ikke eksponert. Lav tillit, ugyldige kilder og ukjent norsk tekstmal gir nekt.

## ways-in

Ask-skjemaet og meny-/drikkesnarveiene bruker `/palazzo/api/*`.
Allergen-snarveien sender et vanlig spørsmål gjennom samme offentlige ask.
DOM-id-ene og elementstrukturen er kontrollert; SkeletonReachabilityAudit er
ikke relevant for denne statiske HTML-flaten. Ekte nettleserklikk er WP5.

## parity

**Ikke akseptert eller målt her — Kjetils WP5.** Referansen finnes i
[palazzo-leaf-prod-v1.jpg](images/palazzo-leaf-prod-v1.jpg). Et faktisk nytt
skjermbilde, side-ved-side-vurdering, tre lastetidsmålinger og lokal standalone
oppstart gjenstår. Fil-/DOM-likhet er ikke et skjermbildebevis.
