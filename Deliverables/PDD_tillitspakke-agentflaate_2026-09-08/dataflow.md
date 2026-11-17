# Dataflyt — AgentTrustPackage

```mermaid
flowchart LR
  P[Porthole / Binding<br/>skeleton for + etter] -- E10 get/set --> T[cell:///AgentTrustPackage]
  T -- E1 agreementTemplate --> A[cell:///PurposeBoundAIGateway]
  T -- E1 agreementTemplate --> W[cell:///WebFetch]
  T -- E1 agreementTemplate --> C[cell:///ScopedCredential]
  T -- E2 Contracts (verifisert) --> EA[(EntityAnchor)]
  T -- E3 policy, rute, instruksjons-digest --> A
  T -- E4 les ceiling --> W
  T -- E5 adjust → ceiling (kun innsnevring) --> W
  T -- E5 adjust → ceiling --> A
  T -- E6 approve → signert snapshot over digest --> EA
  A -- E7 godkjent digest? --> T
  W -- E7 godkjent digest? --> T
  A -- E8 signert ActionDecisionReceipt --> R[(kvitteringslager, append-only)]
  W -- E8 signert EffectReceipt --> R
  T -- E9 diff planlagt/observert --> R
  A -. modellforslag, aldri myndighet .-> M[[hostet modell]]
```

Kant-tabellen med kontraktreferanser står i `PLAN.md#dataflow`. Ingen kant går fra modellen til noen celle: modellen leverer tekst til AIGateway, og alt AIGateway gjør videre er begrenset av Grants/ceilings som pakken viser.
