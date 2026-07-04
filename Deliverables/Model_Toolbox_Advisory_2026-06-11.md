# HAVEN / CellProtocol Model Toolbox Advisory

Date: 2026-06-11

Status: advisory working note, not a normative CellProtocol contract.

## Purpose

This note captures a model-toolbox advisory round for HAVEN / CellProtocol.
The question was whether we should use or keep available other language
models for specific tasks, adapted to the resources and trust boundaries of
each scaffold.

The recommendation is intentionally not "pick one best model". HAVEN's model
choice should be cell-scoped, purpose-bound and auditable:

1. deterministic local rules first
2. on-device / local model when available
3. scoped RAG over authorized material
4. external API model only after explicit escalation
5. agent bridge only as signed, reviewable intent

This matches the current Chat Workbench direction in
`Book/19_Chat_Workbench_Central_Interface.md`: no global provider, no hidden
RAG, no hidden remote model call, no hidden agent action.

## Current HAVEN Direction

### Why

HAVEN / CellProtocol exists to make digital relationships, tools and value
flows explicit, local-first, replayable and permissioned. The product pressure
is real: AI, events, sponsor value and personal copilots all benefit from
automation, but the core thesis is damaged if private signals become a platform
feed, global score or hidden lead product.

The model toolbox must therefore help users propose, explain, structure,
summarize, validate and coordinate. It must not silently rank people, leak
private entity values, create global profiles or mutate state without grants.

### What is actively documented

- `CellScaffold` is the reference/workbench scaffold, not the long-term
  deployment unit for every DiMy or HAVEN surface.
- Personal Co-Pilot V1 is a private, consent-first workspace with Home,
  Profile, Directory, Matches, Chat, Vault, Workflow and Privacy surfaces.
- Chat Workbench is the central interface for natural language -> Purpose /
  Interest -> helper cards, CellConfigurations, RAG cases, agent actions and
  cell-scoped AI providers.
- The conference product is the most concrete commercial wedge: consent-bound
  lead logic, sponsor value, entitlement, gatekeeper, audit, resource metering
  and reporting.
- Documentation / Book / RAG / Vault / Todo workbench is an internal developer
  and knowledge workspace, with orchestration still missing.

## Local Test Results

- `claude -p --model claude-fable-5 ...` succeeded and returned a usable
  advisory answer.
- Claude's own answer said it could not verify its identity beyond the selected
  CLI alias. Treat the test as "the alias works locally", not as cryptographic
  proof of the backend model.
- `claude --version` returned `2.1.139 (Claude Code)`.
- Local Claude config still contains a tip saying Fable 5 is available with
  Claude Code `v2.1.170+`. Because the Fable call succeeded anyway, this setup
  should be cleaned up or rechecked before making Fable 5 part of a durable
  automation path.
- `ollama` is installed at `/usr/local/bin/ollama`, but `ollama list` failed
  because the Ollama app/server was not responding. No local Ollama model
  inventory was verified in this round.
- The machine reports `arm64` and macOS `26.5.1`. More detailed hardware checks
  were blocked by sandbox restrictions, so local model sizing still needs a
  real hardware pass before committing to specific local models.

## External Model Facts Checked

- OpenAI's current model docs list GPT-5.5 as the flagship model for complex
  reasoning and coding, with GPT-5.4 mini / nano for lower-latency and lower
  cost workloads:
  https://developers.openai.com/api/docs/models
- Anthropic's current Claude model docs list Claude Fable 5
  (`claude-fable-5`) as the most capable widely released Claude model, generally
  available beginning 2026-06-09, with Claude Opus 4.8, Sonnet 4.6 and Haiku 4.5
  as the comparison family:
  https://platform.claude.com/docs/en/about-claude/models/overview
- Google Gemini docs list Gemini 3.x text/reasoning models, Nano Banana image
  models, Veo video models, Live/TTS/audio models, Deep Research and Gemini
  Embedding models:
  https://ai.google.dev/gemini-api/docs/models
- Apple documents the Foundation Models framework as a native Swift API for the
  on-device model that powers Apple Intelligence, with provider abstraction,
  multimodal prompts, dynamic profiles and tool calls:
  https://developer.apple.com/apple-intelligence/whats-new/
- OpenAI's gpt-oss model card describes `gpt-oss-120b` and `gpt-oss-20b` as
  open-weight reasoning models released under Apache 2.0, with agentic
  capabilities such as browsing, Python tool use and developer functions:
  https://arxiv.org/abs/2508.10925
- OpenAI business/API privacy material says business/API data is not used for
  training by default, and API inputs/outputs may be retained up to 30 days for
  service and abuse monitoring except for eligible Zero Data Retention cases:
  https://openai.com/enterprise-privacy/

## Recommended Toolbox By Model Class

### 1. Deterministic local rules

Use for:

- provider pre-routing
- cheap intent classification
- known command detection
- skeleton/Explore validation gates
- unsafe data class blocking
- "recommendation not invocation" policy

Default everywhere. No model call should be needed for first-pass safety.

### 2. On-device Apple / Foundation Models

Use primarily in Binding and Apple-native shells:

- draft intent classification
- Purpose / Interest suggestion
- short copy rewrite
- helper-card field extraction
- explaining why a local helper was recommended
- small structured outputs that can be validated

Do not use for:

- hidden reads of contacts, calendar, files or other cells
- large unverified skeleton generation
- bypassing CellProtocol grants
- silent escalation to remote API

### 3. Small local / open-weight models

Candidate lane:

- `gpt-oss-20b` if local hardware supports it
- smaller local models through MLX / llama.cpp / Ollama for high-frequency
  classification, copy, short summaries and PII leakage checks

Use for:

- "which template fits?"
- "which purpose refs apply?"
- "does this public copy reveal too much?"
- short summaries over owner-scoped data

Current blocker:

- Ollama inventory was not available in this round. Before committing to a
  default local model, start the server and benchmark latency, memory, quality
  and output stability on representative HAVEN prompts.

### 4. Scoped RAG models and embedding models

Use for:

- Book / docs questions with citations
- conference agenda and policy lookup
- vault note summaries when the user selected the note/corpus
- product support over public or explicitly authorized material

Rules:

- embeddings over private text are data processing and should be local or
  explicitly granted
- RAG query is a side effect and must require a click or equivalent explicit
  action
- citations must point to canonical docs, not copied cache artifacts
- never use RAG as hidden autocomplete over private folders or entities

### 5. External frontier reasoning / coding models

Candidates:

- GPT-5.5 for hard architecture, coding, migration, review and long-context
  synthesis
- GPT-5.4 / GPT-5.4-mini for cost/latency-sensitive coding or subagent work
- Claude Fable 5 for heavyweight advisory, long-horizon reasoning, design
  critique and architecture review
- Claude Opus 4.8 / Sonnet 4.6 for lower-cost or already-integrated Claude
  workflows

Use for:

- repo-grounded implementation and test planning
- protocol design review
- hard skeleton / renderer / contract reasoning
- codebase migration strategy
- public/product copy critique after context minimization

Do not use for:

- raw private cell dumps
- hidden personal data enrichment
- sponsor lead generation without consent
- direct execution of shell, AppleScript, shortcuts or device actions

### 6. Multimodal design models

Candidates:

- Gemini 3.x for multimodal understanding and design-to-structure analysis
- Nano Banana / Imagen / GPT Image for visual generation or editing when a
  bitmap artifact is useful
- Claude / GPT vision models for screenshot critique and UI comprehension

Use for:

- design sketch -> skeleton fit analysis
- screenshot critique
- visual style comparison
- image assets for product docs and demos

Rules:

- screenshots can contain PII; treat them as external data sharing
- strip unrelated context
- ask for gap analysis, not invented keypaths
- validate any generated skeleton through Explore before preview

### 7. Realtime, voice, audio and translation models

Not a V1 default, but keep available for later:

- conference concierge voice
- accessibility summaries
- live translation
- meeting recap and transcription

Use only after consent, because speech often captures bystanders and sensitive
meeting content.

### 8. Agent models

Use only behind AgentD / bridge policy:

- signed review intents
- allowlisted tools
- dry-run first
- explicit user approval for irreversible actions
- audit FlowElements for route, model, grant, prompt manifest and result hash

No chat surface should directly run raw shell, AppleScript or local file
operations.

## Recommended Toolbox By Scaffold

| Scaffold / surface | Default model lane | Escalation lane | Avoid |
| --- | --- | --- | --- |
| `CellProtocol` core | No model as protocol semantics; validators, Explore, deterministic tests | Model descriptors as contract metadata only after schema is stable | Provider-specific behavior inside protocol core |
| `CellScaffold` workbench | Full palette for experiments: local rules, Apple/on-device, scoped RAG, AIGateway, AgentD review | GPT-5.5 / Claude Fable 5 / Gemini for hard review, coding, design and research | Treating workbench as production monolith or global provider catalog |
| Porthole web / staging | local rules, visible helper cards, server-side scoped RAG/API through declared cells | external model only through explicit button + resolver grant | native-only capability claims, auto-RAG on page load, file/device access |
| Binding native | Apple Foundation Models first, local rules, local small model where available | API/RAG after explicit consent; AgentD as pending review action | silent cloud escalation, hidden reads of contacts/calendar/files |
| HAVENAgentD / sprout / bridge | agent-capable reasoning/coding models with strict allowlists | GPT-5.5, Claude Fable 5, Claude Opus/Sonnet, Gemini agent models for bounded jobs | raw shell from chat, unreviewed remote intents, private data mining |
| DiMy conference scaffold | curated domain RAG, small assistant model, matching/explanation model, content/sponsor helper | stronger external model for organizer/admin summaries or complex support after consent | global memory, cross-event profiling, sponsor lead sharing without grant |
| Documentation / Book / RAG / Vault / Todo | embeddings + retrieval + summarizer over canonical docs and selected notes | frontier model for architecture synthesis with citations | answers without source paths, stale copied docs, hidden note-to-prompt injection |
| Spatial / registry scaffolds | deterministic matching and local metadata classifiers | external reasoning only for simulation/research artifacts | location/person graph export without explicit purpose and TTL |
| Palazzo / domain concierge scaffolds | published-domain RAG + small local copy/summarizer | external provider for staff-facing plan drafts after guest consent | sales pressure, private guest profile expansion, cross-venue memory |

## Provider Descriptor Fields To Standardize

Use these names in future RAG/Explore/provider descriptors:

- `provider_kind`
- `provider_id`
- `model_id`
- `model_alias`
- `execution_scope`
- `chat_scope`
- `cell_scope`
- `requester_scope`
- `purpose_refs`
- `interest_refs`
- `requires_network`
- `requires_grant`
- `requires_approval`
- `side_effect_requires_click`
- `privacy_level`
- `data_classes_allowed`
- `data_classes_denied`
- `retention_class`
- `jurisdiction_or_egress_class`
- `cost_policy`
- `quota_policy`
- `tool_policy`
- `audit_visibility`
- `last_verified`
- `source_code`
- `canonical_doc_path`

Recommended `provider_kind` values should stay aligned with Book 19:

- `local_rules`
- `apple_intelligence`
- `subscription`
- `api_gateway`
- `rag_gateway`
- `agent_bridge`
- `custom`

## Audit Events

Model routing should become FlowElement-visible, not only app logs.

Recommended event names:

- `model.route.recommended`
- `model.route.invoked`
- `model.route.denied`
- `model.route.completed`
- `model.route.failed`

Recommended payload fields:

- `correlationId`
- requester identity hash or scoped pseudonym
- domain
- active cell scope
- purpose refs
- provider kind
- provider policy version
- retention class
- data classification
- redaction profile
- prompt manifest hash, not full prompt by default
- result hash, not full output by default
- grant / contract id
- user-click event id
- token/cost summary
- rejection or failure reason
- TTL

Full prompt/output should only be retained encrypted, owner-scoped and with a
short TTL when replay, complaint handling, debugging or compliance requires it.

## Red Lines

- No global AI provider.
- No hidden RAG query.
- No hidden remote model call.
- No hidden AgentD action.
- No raw shell, AppleScript, shortcut body or local file content in chat
  autocomplete or provider ranking.
- No private keys, vault secrets, device tokens, push tokens, bridge session
  IDs or private route refs to any model.
- No cross-domain identity merge, global reputation, hidden behavior profiling
  or sponsor lead sharing without explicit grant.
- No "AI consent" as a blanket switch. Grants must bind model class, cell,
  purpose, data class and duration.

## Recommended Next Steps

1. Keep this note as the advisory artifact for now.
2. Add a compact "Model / Toolbox Policy" section to
   `Book/19_Chat_Workbench_Central_Interface.md` after Kjetil approves the
   direction.
3. Backfill machine-readable provider descriptors through Explore once the
   descriptor schema is stable.
4. Start Ollama or another local inference server and benchmark at least one
   small local model against HAVEN prompts.
5. Update Claude Code to a version that matches the local Fable 5 tip, then
   retest `claude-fable-5` and record whether alias, model ID and capabilities
   are stable.
6. Add focused tests that recommendation and invocation are separate keypaths,
   and that `requires_grant` / `requires_approval` gates cannot be bypassed.

