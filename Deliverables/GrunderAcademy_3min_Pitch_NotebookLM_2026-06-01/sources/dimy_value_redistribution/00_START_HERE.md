# HAVEN/DiMy Value Redistribution - start her

Oppdatert: 2026-05-04

Dette er arbeidsområdet for å gjøre value redistribution-prosjektet implementerbart. `global_value_redistribution_research/` er kildearkivet. Denne mappen er det operative laget: hva vi tror, hva vi ikke kan si, hva som skal bygges først, og hvilke prompts/skills som skal brukes.

## Nåværende fase

Fase: **ProofDoor/AI entitlement wedge, ledger-first**.

Målet i første fase er å bevise en liten, replaybar verdiløkke:

1. funded internal value inn via PSP/top-up eller kontrollert testtop-up,
2. autoritativ ledger/reservation,
3. entitlement/proof utstedt etter betalt access,
4. AI-bruk eller ProofDoor-access meteres,
5. audit export viser hva som skjedde,
6. value-return policy kan simuleres på hendelsene.

Dette er ikke ennå en global økonomisk omfordelingsmotor.

## Safe thesis

Trygg formulering:

> Vi undersøker om CellProtocol kan gi et etterprøvbart og privacy-preserving underlag for å føre mer verdi tilbake til individer og commons. Første fase er avgrensede piloter med PSP-betaling, entitlements, context-local trust og simulerbar fordelingspolicy.

## Ikke påstå dette

- At prosjektet løser økonomisk ulikhet.
- At credits eller tokens er regulatorisk avklart.
- At dette ikke er e-money, crypto-asset, EMT, CASP-aktivitet eller betalingstjeneste.
- At systemet hindrer kollaps eller singulariteter.
- At global reputation eller global identity er en del av løsningen.
- At production-grade money crypto er ferdig.

## Leserekkefølge

1. `ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md`
2. `ValueRedistribution/02_PRODUCT_VARIANT_AND_REGULATORY_MATRIX.md`
3. `ValueRedistribution/03_MECHANISM_SPEC.md`
4. `ValueRedistribution/04_PILOT_BLUEPRINTS.md`
5. `ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md`
6. `ValueRedistribution/06_IMPLEMENTATION_LOG.md`
7. `ValueRedistribution/07_CLAUDE_SKILLS_AND_NEXT_SKILLS.md`
8. `ValueRedistribution/08_DIMY_BUSINESS_MODEL_AND_HAVEN_BOUNDARY.md`
9. `ValueRedistribution/09_ECOSYSTEM_VALUE_FLOW_AND_REVENUE_MODEL.md`
10. `ValueRedistribution/10_VALUE_MODEL_DATA_REQUIREMENTS.md`
11. `ValueRedistribution/12_CONFERENCE_AND_PERSONAL_COPILOT_VALUE_FLOWS.md`
12. `ValueRedistribution/13_VALUE_FLOW_IMPLEMENTATION_SLICE_2026-05-11.md`
13. `ValueRedistribution/14_CONFERENCE_PRODUCT_IP_AND_VALUE_PROPOSITION.md`
14. `ValueRedistribution/15_CONFERENCE_REVENUE_SCENARIOS_AND_USER_STORIES.md`
15. `ValueRedistribution/16_CONFERENCE_SPONSOR_TARGET_RESEARCH_2026-05-15.md`
16. `ValueRedistribution/17_CONFERENCE_PERSONAS_AND_STORY_SIMULATION.md`
17. `ValueRedistribution/18_ICP_AND_PERSONA_DEVELOPMENT.md`
18. `global_value_redistribution_research/README.md` ved behov for kildearkiv.

## Implementeringsrekkefølge

1. Gjør DiMyMint til autoritativ source of truth for funded internal value.
2. Herd `PaymentAccessCredential` og ProofDoor med consumed-set, TTL, JTI/nonce og TrustedIssuer-policy.
3. Definer AI entitlement tiers og usage metering.
4. Simuler `ValuePoolPolicy` på metering/payment events.
5. Først etter dette: bygg `ContributionProofCell`, `ValuePoolCell`, `MicropayoutPolicyCell`, `AuditAppealCell` som runtime-celler.

## Første konkrete leveranse

Første leveranse skal være liten nok til at den kan testes:

- DiMyMint ledger reservation/release/issue-from-reservation/redeem-with-ledger API eller tilsvarende dokumentert gap hvis ikke nok grunnlag finnes.
- ProofDoor/AI entitlement spec med usage event schema.
- Audit export som kan replays/sjekkes deterministisk.

## Analysepakke for verdiflyt og omsetning

Nyeste analysepakke:

- `ValueRedistribution/09_ECOSYSTEM_VALUE_FLOW_AND_REVENUE_MODEL.md`
- `ValueRedistribution/10_VALUE_MODEL_DATA_REQUIREMENTS.md`
- `ValueRedistribution/11_SOMEBODYMAKEIT_AGREEMENT_VALUE_FLOW.md`
- `ValueRedistribution/models/haven_dimy_value_model.xlsx`
- `ValueRedistribution/diagrams/ecosystem_value_map.png`
- `ValueRedistribution/diagrams/ai_hosting_revenue_loop.png`
- `ValueRedistribution/diagrams/value_accumulation_heatmap.png`

Første beregningscase er AI entitlement + hosted HAVEN, Norge som pilotmarked og EU som upside-scenario. Første eksterne marketplace-case er SomebodyMakeIt som Agreement-basert transparent split-/royalty-/milestone-flow med PSP som pengelag.

## Testbar value-flow implementation slice

Nyeste testbare slice:

- `ValueRedistribution/13_VALUE_FLOW_IMPLEMENTATION_SLICE_2026-05-11.md`
- `ValueRedistribution/contracts/resource_unit_registry.v0.json`
- `ValueRedistribution/contracts/cell_event_adapter_contracts.v0.json`
- `ValueRedistribution/fixtures/conference_value_flow.synthetic.json`
- `ValueRedistribution/fixtures/personal_copilot_value_flow.synthetic.json`
- `ValueRedistribution/scripts/value_pool_simulator.mjs`
- `ValueRedistribution/viewer/value_flow_viewer.cellconfiguration.v0.json`
- `ValueRedistribution/outputs/value_pool_simulation_manifest.json`

Kjør:

```bash
node ValueRedistribution/scripts/value_pool_simulator.mjs --write
```

## Konferanseprodukt, IP og verdiforslag

Nyeste kommunikasjonsnotat for Innovasjon Norge, investorer og arrangører:

- `ValueRedistribution/14_CONFERENCE_PRODUCT_IP_AND_VALUE_PROPOSITION.md`
- `ValueRedistribution/15_CONFERENCE_REVENUE_SCENARIOS_AND_USER_STORIES.md`
- `ValueRedistribution/diagrams/conference_ip_stack.mmd`
- `ValueRedistribution/diagrams/conference_audience_story_map.mmd`
- `ValueRedistribution/diagrams/conference_revenue_cell_map.mmd`
- `ValueRedistribution/16_CONFERENCE_SPONSOR_TARGET_RESEARCH_2026-05-15.md`
- `ValueRedistribution/outputs/conference_sponsor_targets_2026-05-15.csv`
- `ValueRedistribution/17_CONFERENCE_PERSONAS_AND_STORY_SIMULATION.md`
- `ValueRedistribution/fixtures/conference_personas_and_story_scenarios.v0.json`
- `ValueRedistribution/outputs/conference_story_swarm_example_2026-05-22.md`
- `Prompts/conference_persona_story_swarm.md`

## ICP/persona-utvikling

Nyeste persona- og ICP-rammeverk:

- `ValueRedistribution/18_ICP_AND_PERSONA_DEVELOPMENT.md`
- `ValueRedistribution/fixtures/persona_icp_examples.v0.json`
- `Prompts/persona_icp_interview_guide.md`

Kjør konferanseinntektsmodellen:

```bash
node ValueRedistribution/scripts/conference_revenue_scenarios.mjs --write
```

## Agent-/skill-støtte

Codex-skills er installert under `/Users/kjetil/.codex/skills/`.

Claude Code-kompatible skills er installert under `/Users/kjetil/.claude/skills/` og kan kalles som:

- `/dimy-value-redistribution`
- `/dimy-payment-regulatory-guardrails`
- `/haven-claim-review`

## Relevant eksisterende kode

- `CellScaffold/Sources/App/Cells/Micropayments/PaymentGateCell.swift`
- `CellScaffold/Sources/App/Cells/Micropayments/PaymentProofDoorCell.swift`
- `CellScaffold/Sources/App/Cells/Micropayments/PaymentGatePolicy.swift`
- `CellProtocol/Sources/CellBase/VerifiableCredentials/TrustedIssuerCell.swift`
- `DiMyMint/Sources/DiMyMintCore/FundingService.swift`
- `DiMyMint/db/migrations/0001_three_ledger_init.sql`
- `DiMyMicropayments/Sources/DiMyWalletCell/WalletCell.swift`
- `DiMyMicropayments/Sources/DiMyAccessCell/AccessCell.swift`
