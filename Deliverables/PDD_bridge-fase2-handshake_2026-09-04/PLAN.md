# PLAN — bridge fase 2 (`native-porthole/session`)

Dato: 2026-09-04 · G1 godkjent 2026-09-04 («G1 godkjent - og bruk codex») · G2: venter

Grunnlag verifisert av Codex (read-only git, 2026-09-04): fase 1-multipleksingen
er på CellScaffold `origin/main` (`dd72f4ed` «Add opt-in v2 bridge multiplexing
behind ADMIN_SCAFFOLD_BRIDGE_CONNECTION_SHARING»), og `BridgeMultiplexing.swift`
er på CellProtocol `origin/main`. Begge arbeidstrær står på andre tråders
grener — **alt arbeid skjer derfor i friske worktrees fra `origin/main`.**

## Arbeidspakker (1:1 mot bladformål, avhengighetsrekkefølge)

| WP | purposeRef | Hva | Utfører | Tester (→ evidens) | Status |
|---|---|---|---|---|---|
| WP0 | (forutsetning, §2) | Git-verifikasjon av fase 1-plassering | Codex (read-only) | — | **utført 04.09** |
| WP1 | `cell-proof-fields-reserved` + `session-scope-explicit` (kontraktdelen); pkg.std.cell-contract | Kontrakt v1 + 9 fixtures + referansevalidator | Claude | test.bridge.contract-fixtures → `contract/validate_contract.py`: **9/9 PASS 04.09** | **utført (inngår i G2)** |
| WP2 | `socket-loss-explicit`, `setup-errors-reach-channels` | CellProtocol: `closeChannel`-hook for per-kanal opprydding; eksplisitt closed-signal til alle kanaldelegater ved socket-tap; fjern `resumeFromSequence` helt; `sendSetValueState` fannes ut til kanaldelegatene | Codex (`codex exec`), worktree fra CellProtocol `origin/main`, branch `codex/bridge-fase2-socketloss-20260904` | test.bridge.socket-loss, test.bridge.setup-error-fanout + hele `--filter BridgeMultiplex` grønn → TESTRESULT.md#socket-loss, #setup-error | blokkert til G2 |
| WP3 | `session-scope-explicit`, `channel-authz-per-open`, `no-weakened-upgrade`, `channel-cap-explicit` | CellScaffold: `native-porthole/<pubId>/session`-rute — sesjonsvalidering med dagens kjede + scope-felt (fail-closed uten scope), `channelFactory`-authz per kanalåpning mot scope, kanaltak 64 (env-styrt opt-in; default `.dedicated` uendret), typed avslag, per-kanal avregistrering via WP2-hooken | Codex (`codex exec`), worktree fra CellScaffold `origin/main`, branch `codex/bridge-fase2-native-session-20260904` | test.bridge.session-scope-negative, channel-open-authz, upgrade-parity, channel-cap → TESTRESULT.md#auth, #cap, #session-route | blokkert til G2; kodeavhengig av WP2-hooken |
| WP4 | `quality.docs-in-same-change` | `Docs/BridgeCachingAndMultiplexing.md` + `Book/08` §1 (envelope-signatur merkes som krav/reservert felt, «Last verified against code») — i samme endringer som WP2/WP3 | Codex i samme grener | test.docs-updated → ACCEPT.md#docs | blokkert til G2 |
| WP5 | pkg.std.everything-works | TESTRESULT.md med reelt utdata for hver §5-rad; ACCEPT.md forventet↔faktisk; ledgerpost | Claude etter WP2/WP3 | test.status-current → ACCEPT.md#status | blokkert til G2 |

Kryssrepo-avhengighet (eksplisitt): WP3 bruker WP2s hook. Codex bygger WP3 mot
WP2-worktreet med lokal path-avhengighet; pin-oppdatering av CellProtocol i
CellScaffold gjøres som eget, siste steg og er **Kjetils** push/PR-beslutning
(tog-disiplinen). Ingen merge til main i denne pakken.

## Dataflow {#dataflow}

Se `dataflow.md` — hver kant navngitt med endepunkt/kontrakt; kantene for
scope-avslag, tak-avslag og socket-tap er med.

## Det som bevisst IKKE gjøres (fra §2)

Ingen default-flip til `.multiplexedV2`; ingen backpressure (P2-etterarbeid);
ingen implementasjon av celle-bevisene (bare feltene fra WP1); ingen berøring
av `wsce`, E2EE eller de to eksisterende arbeidstrærne.

## Utførelse

Codex kjøres fra Mac-en med én linje (se `handoff/README.md`). Slicene der er
merket `blokkert til G2`; ved G2 endres merkene til `godkjent` og linjen limes
inn. MCP-kanalen brukes ikke til bygg (`lesson.codex-mcp-60s`); git kjøres aldri
fra mounten (`lesson.mount-is-not-git`).
