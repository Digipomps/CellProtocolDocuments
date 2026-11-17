# Dataflyt — Porthole laster flate fra PalazzoScaffold over bro

```mermaid
flowchart LR
  T[skeleton-iterate preview<br/>--configurationKeypath] -->|addConfiguration {name, sourceCellEndpoint, keypath}| P[Porthole (CellScaffold)<br/>resolveRequestedCellConfiguration]
  P -->|host:port godkjent?| R[RemoteBridgeheadAccess<br/>HAVEN_BRIDGEHEAD_HOSTS + token]
  R -->|ja| C[CellResolver.cellAtEndpoint<br/>cell://host:port/PalazzoGuestShell]
  C -->|WS bridgehead, Bearer| B[PalazzoBridgehead<br/>isPublishable]
  B --> G[PalazzoGuestShell.get(guest.configuration)]
  G -->|CellConfiguration (cell:///X)| W[rewrite cell:///X → cell://host:port/X]
  W --> L[loadRequestedConfiguration<br/>isPortholePublishedConfiguration = true]
  L --> V[Renderer leser guest.* / entity.* over samme bro]
  R -->|nei| E[400, ingen nettverkskall]
```

| Kant | Fra → til | Endepunkt / hendelse | Kontrakt |
|---|---|---|---|
| 1 | preview → Porthole | `POST /browserhead/porthole/action` `addConfiguration` | contract/porthole_remote_lookup_contract_v1.json |
| 2 | Porthole → RemoteBridgeheadAccess | `allows(host:port:)` | samme (regel 2) |
| 3 | Porthole → resolver → bridgehead | `cellAtEndpoint(cell://host:port/PalazzoGuestShell)`; WS `/bridgehead/PalazzoGuestShell/<uuid>` med Bearer | `PalazzoScaffold::Sources/App/Controllers/PalazzoBridgehead.swift` |
| 4 | Porthole → PalazzoGuestShell | `get guest.configuration` | `PalazzoScaffold::Sources/App/Support/PalazzoScaffoldContract.swift` |
| 5 | rewrite → load | omskrevet `CellConfiguration` | samme kontrakt (regel 4–5) |
| 6 | renderer → Palazzo-celler | `guest.guest.state.*`, `entity.*` over bro | eksisterende Palazzo-kontrakter (`PalazzoScaffold::docs/sicilia-gui-evidence/inputs/*.contracts.json`) |
