# Draft: restore the Cell bridgehead route with default-on configuration

## Problem og endring

Oppdragsgiver målte HTTP 404 og WebSocket-lukking 1006 på CellScaffolds
bridgehead på staging og produksjon 2026-09-15. Palazzo-broen svarte `ready`
på begge verter. Målingen er oppgitt i oppdraget, ikke gjentatt her.

Den eksisterende ukommitterte `VaporCellBridge.swift` fra
`_wt-bridge-identity-20260830` er kopiert inn på lokal `origin/main`
`6c391437e06d5510cabe8f361c76e5baa004d7ba`, og registreres nå før
`VaporBrowserhead`. Ruten registrerer `/bridgehead/:cellName/:bridgeID`.
Klientdelen ligger i CellProtocol-commit `04068ac1c1202c4633677e061b7e32e778021e86`.

**Enabled er nå på som standard.** Kjetil kan overstyre dette med
`HAVEN_CELL_BRIDGE_DISABLED=1`. `HAVEN_CELL_BRIDGE_ENABLED=1` beholdes som
eksplisitt på-slag; av-bryteren vinner når begge er sanne. Den eldre
`HAVEN_CELL_BRIDGE_ENABLED` kan også fremdeles settes eksplisitt usann.

## Ikke klar for merge

Den kopierte fila er ikke ferdig verifisert som autentisert bro:

- Det samme identitetsbeviset forbrukes i begge upgrade-kontrollene når
  replay-lager er konfigurert.
- Verifisert caller bindes ikke til identiteten i innkommende kommandoer.
- Sprout-kontraktens signatur sjekkes mot selvoppgitt `issued_by`, uten
  sammenligning med scaffoldets betrodde utsteder.

Disse kildefunnene er uløste. Cellens Agreement skal fortsatt avgjøre
autorisasjon, men påstanden om at alle kommandoer utføres for upgrade-kalleren
er ikke etablert. Det er ikke utført en ny ende-til-ende-test av denne ruten.

## Validering

Testmålet **kompilerte**, og 71 tester kjørte. Ingen eksisterende test ble
fjernet, endret, svekket eller hoppet over.

```text
Build complete! (327.21s)
Test Suite 'Selected tests' failed at 2026-09-15 12:23:27.265.
Executed 71 tests, with 1 failure (1 unexpected) in 4.830 (4.837) seconds
```

Feilen var i
`AdminEntryRemoteBridgeLoopbackTests.testStoredEntryCredentialVerifiesThroughRunningAdminScaffoldBridge`:

```text
failed: caught error: "bind(descriptor:ptr:bytes:): Operation not permitted) (errno: 1)"
```

Testen ble nektet å åpne en lokal lytteport. Testkommandoen returnerte exit 1.
`bash ci/check-value-literals.sh` returnerte exit 0:

```text
ValueType-literaler over 20 oppfoeringer: 28 | dekket av baseline: 28
OK: ingen ValueType-literal er stor nok til aa velte typesjekkeren.
```

Det vellykkede kompileringsforsøket brukte `Scripts/run_tests_isolated.sh
--filter Bridge --disable-sandbox --skip-update`, lokal CellProtocol gjennom
et alias med korrekt pakkenavn, og rene lokale DiMy-checkouts på manifestets
eksakte revisjoner. Opprinnelig kommando feilet først på SwiftPMs interne
sandkasse; øvrige forsøk avdekket katalogbasert pakkeidentitet, DNS og
revisjonsavhengigheter som peker på lokale pakker. Alle forsøk er logget i
`CellProtocolDocuments/Deliverables/Bro_Gjenoppretting_2026-09-15/RAPPORT.md`.
Runnerens diskplasskontroll og to-jobbsgrense var beholdt. Den genererte
`Package.resolved`-endringen ble gjenopprettet og er ikke med i committen.

CellProtocol-følgehendringen bygget og kjørte 116 tester med 0 feil.
Publisert CellProtocol-pin i denne PR-en er ikke oppdatert; lokal
pakkeoverstyring er kun utviklingsevidens.

## Leveransestatus

Lokal commit: `ec4375010297741aa1a794b3d9dfaa7af37a08b7`, forfatter/committer
`Losen <kjetil@dimy.io>`. Push/fetch feilet på DNS. GitHub-koblingen returnerte
404 for CellScaffold, så remote main er ikke bekreftet på nytt.
Dette er en forberedt PR-tekst; ingen PR er opprettet.
Ingen merge eller deploy er utført.
