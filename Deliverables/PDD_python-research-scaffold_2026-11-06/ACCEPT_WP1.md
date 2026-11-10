# WP1 — forventet mot faktisk

Første måling gjelder WP1 ved commit 5e1954c. Nyeste status står under oppfølgingen nedenfor.

Dette er en leveransesammenstilling, ikke Kjetils G3-godkjenning.

| Forventning | Faktisk | Bevis |
|---|---|---|
| Verifisert PyCellProtocol-grunnlag | 46 tester bestått, pin og kildehashkontroll | PyResearchScaffold/docs/evidence/pycellprotocol-baseline.json |
| Lokal resolver/runtime | Installerbar pakke, CLI-probe og eide celler | PyResearchScaffold/docs/evidence/wheel-probe.json |
| Varige jobber/avbrytelse/Flow | Implementert og feiltestet | PyResearchScaffold/docs/evidence/wp1-tests.xml |
| Svar på CellBridge fra annet scaffold | Separat Python-prosess med egen vault og resolver gjør proof, get/set og feed over ekte TCP | PyResearchScaffold/docs/evidence/wheel-bridge.log |
| Native Swift consumer | Bestått: ekte vault/resolver, metadata, beskyttet get/set og typed denial; Flow ikke native-testet | PyResearchScaffold/docs/evidence/swift/run-result.json |
| Forskningsdatasett/lineær regresjon/figur/rapport | Ikke del av denne WP1-leveransen | PLAN.md WP2–WP5 |

Repo-stiene i tabellen er relative til HAVEN-roten. Det er ikke startet noen permanent tjeneste.

## Oppfølging 7. november 2026

Autorisert Swift Flow, siste avmelding og resultatlesing besto etter en avgrenset stopFeed-retting. 56 scaffold-tester besto. Ved uautorisert feed observerte Swift ingen Combine-avslutning etter serverens avslag. Full Agreement-paritet er motbevist. Se [paritetsrapporten](../../../PyResearchScaffold/docs/SWIFT_PARITY.md).
