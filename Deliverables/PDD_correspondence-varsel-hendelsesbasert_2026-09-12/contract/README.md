# contract/ — kontrakter denne leveransen bygger på eller lager

- `HavenAgentD::Contracts/agent-challenge-v1.schema.json` — innbokskontrakten (saker + kilder). Utvides med kilden `correspondence` (fra grenen 11.9, HD-0071) og med håndtering av ukjent kilde (WP-A4, HD-0074). Fixtures: `HavenAgentD::Tests/HavenAgentRuntimeTests/Fixtures/Challenge/`.
- `agent_challenges_cell_contract_v0.json` (her, **utkast**) — cellen `agent/challenges`: `get`/`set`-nøkler og flow-hendelser. Løftes til `HavenAgentD::Contracts/` med fixtures og validator i WP-A3; til `Book/` når den er stabil.
- Correspondence-cellens hendelser (`haven.assistant.correspondence.*`) — `CellScaffold::Sources/App/Cells/Agent/AssistantCorrespondenceContracts.swift`; mottaker-skopet feed dokumenteres i WP-S1.
