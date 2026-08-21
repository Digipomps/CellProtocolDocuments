# HAVENAgentD Repository Relocation

Status: Completed 2026-08-21  
Last verified: 2026-08-21

## Decision

HAVENAgentD source development has moved from the embedded location
`Digipomps/Binding/HavenAgentD` to the private canonical repository
[`Digipomps/HavenAgentD`](https://github.com/Digipomps/HavenAgentD).

The extracted `main` revision at the time of the move is
`f3a9f94b021fa4013a7a2045187d759ec126bcaf`. The corresponding Binding
extraction is tracked in
[`Digipomps/Binding#29`](https://github.com/Digipomps/Binding/pull/29), and the
CellScaffold consumer notice is
[`CellScaffold Discussion #139`](https://github.com/Digipomps/CellScaffold/discussions/139).

## Repository Boundary

- HAVENAgentD owns its Swift package, sources, tests, CI, packaging, agent-only
  scripts, and operational documentation.
- Binding remains a consumer. It must run without a HAVENAgentD source checkout
  or installed agent.
- Release and production consumers should use installed, signed executables.
- Local multi-repository development should use sibling `Binding` and
  `HavenAgentD` checkouts, or the explicit `HAVEN_AGENTD_REPO` override.
- Binding binary overrides remain explicit through
  `BINDING_HAVEN_AGENTD_BINARY` and `BINDING_HAVEN_AGENTD_MCP_BINARY`.
- The move does not add a Git submodule and does not change runtime protocol
  semantics.

## Contract Continuity

The cross-repository registration-observation contract is versioned as
`haven.agentd-registration-observation.v1`.

- Canonical agent fixtures live under `Contracts/` in `Digipomps/HavenAgentD`.
- Binding retains compatibility fixtures under
  `Documentation/TestData/HavenAgentD/`.
- Repository relocation must not be used as a reason to silently change the
  schema, event order, or compatibility identity.

## Documentation Follow-up

The following actionable documents still contain embedded source or build
paths and should be updated to the canonical repository boundary:

- `Book/21_Contact_Endpoint_Cell.md`
- `Book/25_SecretCredentialCell.md`
- `Deliverables/HavenAgentD_Gemma4_MLX_Runtime_Integration_2026-06-12.md`
- `Deliverables/Kontekstgraf_For_Kodeagenter_Plan_2026-08-09.md`
- `Deliverables/Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md`

Historical deliverables may preserve the former path when it is part of a
dated record, but actionable commands should use the sibling checkout,
installed executable, or an explicit environment override. Do not hand-edit
`Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl`; regenerate it
through the normal model-knowledge pipeline after correcting canonical source
documents.

## Verification Recorded At Extraction

- The standalone package resolved pinned CellProtocol and Sprout revisions
  without sibling checkouts.
- The focused standalone registration-observation suite passed all three tests.
- Binding passed eight post-removal tests covering the registration adapter and
  independence from the former embedded source tree.
- Shell syntax, package-manifest parsing, JSON syntax, fixture identity, and
  `git diff --check` passed.
