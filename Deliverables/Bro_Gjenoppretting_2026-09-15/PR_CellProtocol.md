# Carry signed caller proof on dedicated remote Cell bridges

## Problem og endring

Oppdragsgiver målte HTTP 404 og WebSocket-lukking 1006 for CellScaffolds
bridgehead på staging og produksjon 2026-09-15. Palazzo-broen svarte `ready`
på begge verter. Målingen er oppgitt i oppdraget; den er ikke gjentatt her.

Den dedikerte Cell-broen beholdt ikke det signerte opprinnelsesbeviset og
sendte heller ikke query-parametrene fra `remoteWebSocketQueryItemsProvider`.
Patchen fra `claude/bridge-query-credential-20260830` er anvendt med
`git apply -3` på `c430a24c0d93d2cec9984149c4fb7546c6341bd3`, uten konflikter.
Den bevarer utfordring og signatur og sender dem som `bridge_proof` og
`bridge_signature`, sammen med leverandørens øvrige query-parametere.
To nye tester kontrollerer URL-en som den dedikerte forbindelsen bruker.

CellResolver.swift er bare endret gjennom den opprinnelige patchen.
Ingen eksisterende test er fjernet eller svekket.

## Samordnet CellScaffold-endring

Den lokale følgehendringen registrerer `VaporCellBridge` før `VaporBrowserhead`.
**Ruten er på som standard.** Kjetil kan overstyre dette med
`HAVEN_CELL_BRIDGE_DISABLED=1`. `HAVEN_CELL_BRIDGE_ENABLED=1` beholdes som
eksplisitt på-slag; av-bryteren vinner hvis begge er satt til sann.
En eksplisitt usann verdi i den eldre `HAVEN_CELL_BRIDGE_ENABLED` deaktiverer
også ruten. Tilgang til selve cellen skal fortsatt avgjøres av dens Agreement.

Følgehendringen har uløste funn rundt replay, binding av innkommende kommandoer
til den autentiserte kalleren og tillit til Sprout-utsteder. Den er ikke
funksjonelt godkjent. Denne klientpatchen alene gjenoppretter ikke tjenesten.

## Validering

Kjørt fra `CellProtocol/_wt-bro-20260915`:

```sh
bash Scripts/haven-swiftpm.sh -- build --disable-sandbox
bash Scripts/haven-swiftpm.sh -- test --filter Bridge --disable-sandbox
```

```text
Build complete! (107.37s)
Test Suite 'BridgeTests' passed at 2026-09-15 12:16:21.756.
Executed 52 tests, with 0 failures (0 unexpected) in 107.646 (107.654) seconds
Test Suite 'Selected tests' passed at 2026-09-15 12:16:22.187.
Executed 116 tests, with 0 failures (0 unexpected) in 108.285 (108.299) seconds
```

Begge nye tester kjørte og bestod. Den separate Swift Testing-linjen med
«0 tests» er ikke brukt som suksessbevis.

De opprinnelig oppgitte kommandoene ga exit 64: runneren krever `--` og
avviser `--package-path`. Normal manifestkjøring ble deretter avvist av
`sandbox-exec: sandbox_apply: Operation not permitted`; flagget ovenfor
gjelder SwiftPMs interne sandkasse. Øktens ytre begrensninger var fortsatt på.
Ingen markørfil manglet. Alle rå logger er bevart i leveranserapporten.

## Leveransestatus

Lokal commit: `04068ac` (Losen, `kjetil@dimy.io`). Push feilet på DNS til
github.com. Denne filen er et PR-utkast, ikke en opprettet PR.
Ingen merge eller deploy er utført.
