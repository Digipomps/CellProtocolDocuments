# Kontrakter — entitetsdata egen kontroll

Skrevet til G2, 2026-09-21. Tre skjemaer, tolv fixturer, og et skript som kjører dem.

| Fil | Hva den fester |
|---|---|
| `entityanchor_genesis_v1.json` | Forseglingen. Irreversibel, én initiatorlenke, `localEntityAnchor`. |
| `trustedmodels_v1.json` | Eierens tillitserklæring per modellvei. Eiersignert, revokerbar. |
| `aigateway_contract_v1.json` | Invoke mot gatewayen. Gir et forslag, aldri en endring. |

## Kjør dem

    python3 check_fixtures.py

De negative fixturene er poenget. `fixture_trustedmodels_nei_apple_hevder_haandhevelse.json`
skal avvises fordi en Apple Intelligence-rute aldri kan sette `enforcedByUs: true` — vi kan erklære
veien, ikke håndheve den. `fixture_trustedmodels_nei_lokal_er_ikke_loopback.json` skal avvises fordi
en «lokal» modell på en https-adresse ikke er lokal. Slutter en negativ fixture å bli avvist, har
skjemaet sluttet å håndheve noe det ble laget for.

## Hva skjemaene bevisst ikke gjør

De sjekker form, ikke sannhet. At `dataLeavesDevice: false` står i en erklæring gjør den ikke sann —
den gjør den *etterprøvbar*, fordi påstanden nå er skrevet ned og kan motsies. For rutene der
`enforcedByUs` er `false` er det alt vi kan tilby, og skjemaet tvinger oss til å innrømme det i
stedet for å la det være underforstått.

Kryssjekkene som ikke kan uttrykkes i JSON Schema — at `proposalScope` er en delmengde av
`mayPropose`, at signaturen faktisk verifiserer — hører hjemme i cellens egne kontraktstester
(`pkg.std.cell-contract`), ikke her.
