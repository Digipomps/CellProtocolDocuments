# Kotlin Implementation Checklist (CellProtocol + Scaffold)

## 1. Grunnmodell

- Definer kjerne-typer: `Identity`, `ValueType`, `FlowElement`, `ConnectState`, `Agreement`, `Condition`.
- Sikre stabil serialisering/deserialisering (JSON) med eksplisitte feltnavn.
- Etabler deterministisk tids-/sekvenshåndtering for flow.

## 2. Cell-interfaces

Implementer separerte grensesnitt i tråd med `02_Cell_Interfaces.md`:

- `Emit`: kun utgående observerbar strøm
- `Absorb`: tilkobling/forhandling av tilgang
- `Meddle`: eksplisitte state-endringer
- `Explore`: sideeffektfri metadata/schema-beskrivelse
- `GroupProtocol` (valgfritt)

## 3. Resolver

- Bygg en sentral `CellResolver` som eneste inngang for `Absorb` og `Meddle`.
- Legg inn validering for identity, capability, condition og contracts.
- Enforce sekvensintegritet i flow og replay.
- Legg til livssyklus (`instantiation`, `activation`, `running`, `suspension`, `termination`).

## 4. Scaffold-runtime

- Isoler celler fra hverandre (feil i én celle skal ikke krasje andre).
- Koble på storage med atomiske writes og ordnet flow-persist.
- Implementer replay med deterministisk re-kjøring.
- Implementer supervisor-regler for feil, retry og suspensjon.

## 5. Cell-kontrakter og registrering

- Definer en Kotlin-vennlig registrerings-API som tilsvarer resolver-registrering av cell-typer.
- Definer `CellConfiguration`-modell med:
  - `cellReferences`
  - subscriptions
  - initielle `set`-verdier
  - valgfri skeleton

## 6. Skeleton JSON

Bruk `12_Skeleton_Spec.md` som fasit:

- Enkelt nøkkelobjekt per element (f.eks. `{ "Text": { ... } }`).
- `flowElementSkeleton` er canonical key.
- `Object` skal støttes i wrapped format ved encoding; dekoding kan støtte legacy-format.
- Implementer elementtyper og `modifiers` med samme semantikk.

## 7. Transport og remote refs

- Hold transport semantisk nøytral (WebSocket/QUIC/WebRTC/IPC).
- Støtt `cell://<host>/<CellName>` ruting der relevant.
- Legg inn en tydelig sikkerhetspolicy for `ws://` vs `wss://`.

## 8. Testkrav før første release

- Kontraktstester for `Emit/Absorb/Meddle/Explore`.
- Golden tests for `Skeleton` encode/decode.
- Replay-tester: samme input + state + history => samme output.
- Resolver policy-tester: avvisning ved manglende capability/condition.

## 9. Optional: Perspective matching

Hvis dere skal støtte weighted matching:

- Implementer query-kontrakter fra `14_Perspective_Runtime_Matching.md`.
- Hold scoring deterministisk og forklarbar.
- Støtt `portableRefs-v1` for cross-runtime matching.
