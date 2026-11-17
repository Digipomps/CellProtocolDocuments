# Implemented candidate dataflow

Last verified against code: 2026-10-12. Phone/sensor producers are not implemented.

```mermaid
flowchart LR
    S[Configured semantic source Cells] -->|context.observation.changed| P[PerspectiveCell]
    S -->|authorized snapshot get| P
    P -->|perspective.context.changed| F[ContextFlowFilterCell]
    P -->|perspective.context.state get| F
    N[Authorized content sources] -->|content Flow| F
    F -->|permitted content only| R[Resolver-loaded rootCell]
    R -->|flow| V[Porthole CellViewModel input]
```

Source bindings use context:sourceID labels; Perspective consumes their observation
events and evaluates current state. The filter binds Perspective separately as
filter:perspective, consumes control events, and intersects content constraints on
filter:content:index subscriptions. Snapshot reads happen after subscriptions, with
revision checks. Existing source and content admission remain required.

The runtime integration test uses CellResolver.loadCell and root.flow, the same
entrypoints read in CellViewModel. It does not render or certify a screen.
