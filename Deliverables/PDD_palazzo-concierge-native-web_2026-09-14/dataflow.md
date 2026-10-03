# Dataflyt — offentlig concierge servert av PalazzoScaffold

```mermaid
flowchart LR
  U[Gjestens nettleser] -->|GET /palazzo| S[Public/palazzo/index.html + js + css]
  U -->|POST /palazzo/api/ask {query}| F[PalazzoCommunaleFacade<br/>rate-limit, body ≤ 4096, ingen token]
  F -->|concierge.knowledge.query som fasadens principal| K[PalazzoConciergeCorpus<br/>korpus, allergen fail-closed]
  K -->|svar| F
  F -->|konvolutt v1, route=native| U
  U -->|GET /palazzo/api/state| F
```

| Kant | Fra → til | Endepunkt | Kontrakt |
|---|---|---|---|
| 1 | nettleser → statisk | `GET /palazzo`, `/js/…`, `/css/…` | contract/palazzo_public_concierge_contract_v1.json (routes) |
| 2 | nettleser → fasade | `POST /palazzo/api/ask` | samme (askEnvelope, limits) |
| 3 | fasade → korpuscelle | `concierge.knowledge.query` (`PalazzoScaffoldContract.Concierge.query`) | `PalazzoScaffold::Sources/App/Support/PalazzoScaffoldContract.swift` |
| 4 | fasade → nettleser | konvolutt | samme |
| 5 | nettleser → fasade | `GET /palazzo/api/state` | stateFields |
