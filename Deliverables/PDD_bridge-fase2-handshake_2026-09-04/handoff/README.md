# Codex-handoff — bridge fase 2 (`native-porthole/session`)

Status: **slicene er blokkert til G2.** Ved Kjetils G2 endres merkene til
`godkjent`, og denne linjen limes inn i terminalen på Mac-en:

```bash
/Users/kjetil/.local/bin/codex exec -C /Users/kjetil/Build/Digipomps/HAVEN "Les /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_bridge-fase2-handshake_2026-09-04/handoff/README.md og utfør slicene som er merket godkjent, i rekkefølge."
```

Kontrakten som implementeres: `../contract/bridge_session_handshake_contract_v1.json`
(referansesemantikk i `../contract/validate_contract.py`, 9/9 PASS — Swift-testene
skal dekke de samme casene). Beslutninger: eget scope-felt; kanaltak 64;
socket-tap = bygg på nytt, `resumeFromSequence` fjernes; celle-bevis-felter
reserveres som valgfrie, versjonerte felter (implementeres IKKE nå).

## Ikke gjør

- Ikke rør de eksisterende arbeidstrærne (CellProtocol står på
  `claude/perspective-entities-invite-20260822`, CellScaffold på
  `claude/working-tree-salvage-20260829` — begge har andre tråders arbeid).
  Bruk `git worktree add` fra `origin/main`.
- Ikke endre default `.dedicated` → `.multiplexedV2` noe sted.
- Ikke svekk noen eksisterende validering i `shouldUpgrade`/kontraktsjekken.
- Ikke rør `wsce`, browserhead, E2EE-filer eller backpressure.
- Ikke merge/push til `main`; én `codex/`-branch per repo, én commit per slice.
- Ingen kommentar på samme linje som en kommando.

## Slice A (CellProtocol) — status: blokkert til G2

```bash
cd /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol
git worktree add /tmp/wt-bridge-fase2-cp origin/main
cd /tmp/wt-bridge-fase2-cp
git switch -c codex/bridge-fase2-socketloss-20260904
```

I `Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift` (+ `BridgeCommand.swift`):

1. `closeChannel`-hook på `BridgeMultiplexServerSession`: callback ved lukking av
   én logisk kanal, slik at verten kan avregistrere kanalens emit-celle (fase
   1-P1). 2. Ved fysisk socket-tap: hver aktiv kanaldelegat får eksplisitt
   closed-signal (ingen stille foreldreløse). 3. Fjern `resumeFromSequence`
   fullstendig (deklarasjon `BridgeCommand.swift:73`, init/dekode/enkode
   `:136,:147,:160,:176`, serialiseringstest `BridgeMultiplexingTests.swift:351,361`).
   4. `sendSetValueState` på begge sesjonstyper (`BridgeMultiplexing.swift:610,1145`)
   fannes ut til alle aktive kanaldelegater i stedet for å kastes.

Nye tester: socket-tap varsler N delegater; closeChannel-hook kalles; fanout når
alle kanaler. Kjør (forvent rød første gang, fiks, aldri taus utgang):

```bash
arch -arm64 swift test --filter BridgeMultiplex
```

Forventet slutt: alle BridgeMultiplex-tester grønne, 0 treff på
`resumeFromSequence` i repoet. Én commit. Stopp hvis eksisterende tester må
svekkes for å bli grønne — rapporter i stedet.

## Slice B (CellScaffold) — status: blokkert til G2 (krever Slice A)

```bash
cd /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold
git worktree add /tmp/wt-bridge-fase2-cs origin/main
cd /tmp/wt-bridge-fase2-cs
git switch -c codex/bridge-fase2-native-session-20260904
```

Pek CellProtocol-avhengigheten midlertidig på `/tmp/wt-bridge-fase2-cp`
(lokal path i Package.swift, én egen commit merket `TEMP: local dep`, reverteres
før PR). Deretter, etter mønsteret fra fase 1 (`AdminScaffoldBridgeRoutes.swift:418`
`registerMultiplexSessionRoute` + `AdminScaffoldMultiplexSessionRegistry`):

1. Ny rute `v1/resolver/native-porthole/:pubId/session` i
   `VaporSproutResolver.swift`-familien. `shouldUpgrade` gjenbruker
   `validateNativePortholeUpgrade`-kjeden (`SproutResolverCompatibility.swift:839`)
   uendret **pluss**: kontrakten må ha `scope` (ellers typed avslag
   `sessionScopeMissing` — en gyldig legacy-kontrakt uten scope når bare dagens
   per-celle-rute). 2. `channelFactory`: per `openChannel` — eksakt
   `publishedCellName ∈ scope.channels`, kanaltall ≤ min(`scope.channelCap`, 64)
   (vertskonstant 64, env-overstyrbar), ellers `channelRejected`; øvrige kanaler
   overlever. Dekod `actorCell`-feltet tolerant (ignorér når policy ikke krever
   det; feltet gir ALDRI autoritet). 3. Per-kanal avregistrering via Slice
   A-hooken; socket-close river alt (fase 1-mønsteret). 4. Opt-in som i fase 1:
   default `.dedicated` uendret. 5. Oppdater `Docs/BridgeCachingAndMultiplexing.md`
   i samme commit («Last verified against code: 2026-09-04»).

Nye tester (speil `../contract/fixtures/`-casene + fase 1-testfilen
`Tests/AppTests/AdminScaffoldBridgeMultiplexRouteTests.swift`): uten scope,
utenfor scope, utløpt, ukjent schema-versjon, tak (N ok, N+1 avvist, de N
lever), to kanaler over én socket, socket-close-opprydding.

```bash
arch -arm64 swift test --filter NativePortholeSession
```

Forventet slutt: nye tester grønne + `AdminScaffoldBridgeMultiplexRouteTests`
fortsatt grønn. Én commit for ruta + tester (pluss TEMP-committen).

## Rapportkrav (begge slices)

Avslutt med: hva som ble endret (filer), eksakt testutdata (antall), og en
obligatorisk **«Utelatt / ikke dekket»**-seksjon. Skriv rapporten til
`/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_bridge-fase2-handshake_2026-09-04/handoff/RAPPORT_<slice>.md`.
Ikke push; Kjetil avgjør PR/pin-oppdatering (tog-disiplinen).
