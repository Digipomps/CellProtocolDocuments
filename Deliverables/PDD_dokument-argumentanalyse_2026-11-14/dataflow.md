# Dataflyt — analyserom (iterasjon 1)

```
Student (Porthole web / Binding)
  │ FileUpload base64 / TextArea          set analyse.inntak.*
  ▼
TextAnalysisRoomCell (CellScaffold, ny)  ── Agreement-vilkår: medlem / akseptert invitasjon ──┐
  │ analyze(text)                                                                              │
  ├─► TextReliabilityAnalyzer (Swift, ny, ren funksjon)  → påstander, kilder, grunngraf        │
  │ proposeModel(text, claims)  [bare når autorisert rute finnes]                               │
  ├─► AIGatewayCell purposeBound invoke (orchestration parallel + adjudicator for panel)       │
  │      ◄─ forslag → QuoteAnchorValidator (avviser forslag uten ordrett sitat)                 │
  │ state analyse.state.*  ◄─ get                                                               │
  │ Flow topic «analysis.change» ─► alle deltakere                                              │
  ├─► ChatCell (CellBase) for rommets chat; samme admission-vilkår                              │
  │ eksport.json / eksport.mermaid  → nedlasting                                                │
  ▼                                                                                             │
Skeleton: Tabs(Påstander | Argumentgraf | Teksten) + Chat                                       │
  └ Visualization kind «argumentmap» (ny i CellProtocol: CellBase-spec + CellApple-renderer;   │
    web-renderer i CellScaffold skeleton-runtime.js)                                            │
```

| Kant | Fra → til | Endepunkt / event | Kontrakt |
|---|---|---|---|
| E1 | Porthole → rom | `set analyse.inntak.fil` (base64, ≤1 MB, text/plain, text/markdown) | WP5 Explore-skjema |
| E2 | Porthole → rom | `set analyse.inntak.tekst/tittel/kilde`, `set analyse.inntak.analyser` | WP5 |
| E3 | rom → analysator | `TextReliabilityAnalyzer.analyze(_:)` (in-process) | `Book/text_reliability_analysis_contract_v1.json` |
| E4 | rom → AIGateway | `invokePurposeBound` med purposeRef `purpose://candidate.tekstanalyse.modellhjelp` | `AIGatewayPurposePolicy` |
| E5 | rom → deltakere | Flow `analysis.change` | WP5 |
| E6 | Porthole → rom | `set analyse.marker.{enig,uenig,kildeSjekket}`, `analyse.kommenter`, `analyse.forslag.{godta,avvis}` | WP5 |
| E7 | rom ↔ ChatCell | chat via CellBase ChatCell, admission `audience.admission.member` | `CellBase/Cells/Chat/ChatCell.swift` |
| E8 | rom → renderer | `get analyse.state.graf` (argumentmap v1) | `contract/argumentmap.v1.schema.json` |
| E9 | rom → nedlasting | `get analyse.eksport.json`, `analyse.eksport.mermaid` | Book 27-kontrakten |
