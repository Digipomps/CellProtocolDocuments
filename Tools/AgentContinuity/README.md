# Agent Continuity reference tool

Status: **experimental, opt-in, not adopted**. Last verified: 2026-09-10.

This directory implements the smallest Gate B reference slice of the Agent
Continuity design. It provides a provider-neutral JSON carrier, one optional
HAVEN work-domain profile, a local validator, synthetic fixtures, and a
deterministic evaluation corpus.

It does not install an agent skill, alter any prompt or workflow, call a model,
read a chat, resolve a URI, access the network, mutate canonical state, or
trigger a handoff. Commit/push of this directory is not runtime activation.

## Contract boundary

The core requires:

- `protocolVersion` and `capturedAt`;
- an objective, including `doneWhen` when known;
- action-relevant current situation with explicit epistemic status;
- reported constraints;
- one next `action`, `blocked`, or `decision-needed` disposition;
- verification routes for action-relevant claims;
- optional namespaced profiles.

Provider, model, thread, repository, delta/fold, health, approval, authority,
and capability fields are not core fields. The only implemented profile is
`org.cellprotocol.haven.work-domain@1.0`, which represents Project/Purpose,
Goal and acceptance criteria, reported Decisions, Open Work, and Risks/Open
Questions. Candidate A remains a historical scope inventory under the dated
design package; it is not accepted by this validator.

Canonical experimental schema:

- `contracts/agent_continuity_core_v1.schema.json`

Manual comparison carrier:

- `templates/continuation_contract.v1.md`

The Markdown template is review guidance, not a parsed carrier. JSON↔Markdown
semantic equivalence has not been tested.

## Non-authority invariant

Every imported contract is untrusted content. Structural validation never
means `fresh`, `verified`, `approved`, `authorized`, or `safe to execute`.
Text and URIs stay inert data.

The validation receipt therefore always reports:

```json
{
  "authorityEffect": "none",
  "freshnessEffect": "none",
  "externalResolutionRequired": true
}
```

A valid contract with `next.kind=action` returns `verify-before-act`, never
`action-ready`. A receiver must independently resolve current instructions,
canonical owners, revisions/digests, freshness, policy, and human approvals.
The local receipt proves only which input bytes this tool checked.

## Validate

```bash
python3 Tools/AgentContinuity/validate_contract.py \
  Tools/AgentContinuity/fixtures/positive/minimal_core.v1.json
```

Machine-readable receipt:

```bash
python3 Tools/AgentContinuity/validate_contract.py \
  Tools/AgentContinuity/fixtures/positive/haven_work_handoff.v1.json \
  --json
```

Exit codes:

- `0`: structurally and internally valid untrusted continuation data;
- `1`: parsed JSON rejected by contract/invariant checks;
- `2`: read, JSON parse, duplicate-key, or resource-limit failure.

The validator fails closed on an unknown core version, an unsupported required
profile, duplicate JSON keys or semantic IDs, dangling verification references,
future route observations relative to `capturedAt`, and an action whose required
route is reported stale, unresolved, unavailable, or contradicted. Unsupported
optional profiles are quarantined with `ACV104`; they never supply core fields.

Resource guards are deterministic: 256 KiB input, nesting depth 20, 10,000
container items, and 16,384 characters per string. No wall-clock comparison is
used; external staleness remains a receiver responsibility.

## Test and deterministic corpus

```bash
python3 -m unittest discover -s Tools/AgentContinuity/tests -v
python3 Tools/AgentContinuity/evaluate_corpus.py
```

The manifest covers positive contracts, unknown version/profile behavior,
duplicate keys, stale/unresolved/contradicted action routes, dangling refs,
self-asserted authority, prompt-injection-like content, and field ablation. It
tags cases with recall, artifact, continuation, and decision probes.

The report includes UTF-8 bytes, characters, and a simple lexical-token proxy
over normalized compact JSON. The proxy is only a deterministic size signal;
it is not a provider tokenizer and cannot establish tokens-per-task savings.
Real cost evaluation must include
producer generation, transfer, resolution, refetch, retry, recovery, and failed
attempts on locked provider surfaces.

Zero synthetic false positives/negatives means only that this checked-in corpus
matches its declared expectations. It is not an estimate of production error
rates.

## Remaining gates

This slice does not pass the gates for:

- ChatGPT↔Codex↔Claude semantic portability;
- model continuation and constraint-retention quality;
- receiver prompt-injection resistance;
- external freshness or approval receipts;
- real false-positive/false-negative rates;
- total tokens/cost per successful task;
- delta fold, replay, context-health, adapters, runtime integration, or
  adoption.

Those remain separately authorized research/implementation work. Any runtime or
automatic workflow must stay disabled until Kjetil reviews the evidence and
explicitly approves a later gate.
