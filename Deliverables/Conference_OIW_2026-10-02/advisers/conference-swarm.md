Brief audit
===========

2026-10-02. Advisor role: repository source auditor and skeptical implementation reviewer.

1. The user's OIW umbrella, open creation, discoverable purpose/availability, shared conference knowledge and private enrichment are **normative product proposals**, not evidence of current implementation or official OIW affiliation. Official OIW facts are owned by the parent's separately fetched source audit; this slice does not independently certify them.
2. “Existing swarm” is supported by source, but conflates three distinct things: UserSimulationScaffold's transport simulator, conference-specific synthetic population/playback cells, and the new Swarm workbench visual design. They have different execution and persistence boundaries.
3. “No conference simulation exists” would be wrong: population and playback are implemented and merged by ConferenceAdminShell, despite stale phase-1 placeholder text inside ConferenceSimulationStudio.
4. A brief error here outranks a subject-matter verdict, because it would contaminate every downstream recommendation.

## Scope and evidence status

Read-only local source inspection; no build, test execution, service start, provider request, mutation of entities, or deployment performed. The only output written is this `/private/tmp` report. Bounded inspection used relevant source slices, two test files, recent workbench status/design approval, and the existing runner/runbook. Searches outside those slices were inventories, not an exhaustive repo audit.

All source paths below are relative to `CellScaffold/`. Branch: `codex/entitetsutvidelse-20260929`; HEAD: `942965ca24e9a418b531f9514c1da75d6d529e30`. **The checkout is substantially dirty.** `Sources/EventCells/`, its registry test, and `Deliverables/PDD_swarm-workbench_2026-09-29/` are untracked; other files are modified or moved elsewhere in the checkout. Thus SHA identifies the base checkout, not a reproducible commit containing all inspected evidence. The inspected UserSimulationScaffold files and named conference app cells did not show changes in the targeted `git status`, but they depend on the dirty checkout. No deployment status is inferred.

Status language: **implemented** = inspected source behavior exists; **partial** = useful component with a material missing link; **not found** = absent from the bounded inspected path, not proof of global absence; **untested** = not executed in this audit.

## Evidence table

| Capability / claim | Status and finding | Retrieved evidence (path:line) |
|---|---|---|
| Independent publishers and events | Implemented source. Authenticated publisher onboarding creates a profile; requester becomes its admin. Publisher permission gates event creation. Events support draft/create/update/publish/archive; hard delete was not found. | `Sources/App/Controllers/VaporEventPlatform.swift:25`; `Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:246`, `:494`, `:65` |
| “Anyone can create an event” | Partial. Any authenticated user can enter publisher onboarding; creating an event requires that publisher's `createEvent` permission. Anonymous unrestricted creation is not established. | `Sources/App/Controllers/VaporEventPlatform.swift:25`; `Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:500` |
| Public event discovery and stable publication | Implemented source. `/events`, `/actors/:actorSlug`, `/events/:actorSlug/:eventSlug`, `/event-admin/:actorSlug/:eventSlug`; publication snapshots separate visible content from later draft edits. | `Sources/App/Controllers/VaporEventPlatform.swift:52`, `:108`, `:141`, `:175`; `Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:675`, `:781` |
| Publisher access and identity | Implemented source. Authenticated identity requires an active vault binding and signing key. Explicit publisher permissions include membership, editing, publishing and federation. | `Sources/App/Controllers/VaporEventPlatform.swift:298`; `Sources/EventCells/EventPlatform/EventPlatformModels.swift:41`; registry `:500` |
| Umbrella / OIW membership | Not found in event model. Events belong to one `actorSlug`; no umbrella ID, parent-event link, affiliation claim, admission decision or independent-owner membership contract appears in EventDefinition. Conference simulation subevents are scenario composition, not those governance semantics. | `Sources/EventCells/EventPlatform/EventPlatformModels.swift:144`; `Sources/App/Cells/ConferenceMVP/Cells/ConferenceSimulationStudioCell.swift:157`, `:466` |
| Federation | Partial and narrower than the label suggests. Opt-in richer public search exists, but reads local registry publication snapshots and applies a substring query; no remote publisher transport or OIW hierarchy is established by this code. | `Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:699`, `:721`; `Sources/EventCells/EventPlatform/EventFederationBrokerCell.swift:108` |
| Event persistence | Partial assurance. Registry encodes/decodes publisher records, audit and snapshots and describes itself as cell-persisted; source inspection does not certify durable store configuration or recovery in a running deployment. Separate ConferenceStorageAdapter supports conference/participant/consent/meeting/event records; InMemory implementation is explicitly process-local. | `Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:32`, `:47`, `:190`; `Sources/EventCells/ConferenceMVP/Storage/ConferenceStorageAdapter.swift:28`; `Sources/EventCells/ConferenceMVP/Storage/InMemoryConferenceStorage.swift:8` |
| Purpose and interests | Implemented conference model and participant snapshots. The inspected recommendation algorithm uses explicit purpose/interest label overlap, role and track, gated by matchmaking consent. It is not an assessment of actual meeting value. | `Sources/EventCells/ConferenceMVP/Models/ConferenceDomainModels.swift:291`; `Sources/App/Cells/ConferenceMVP/Cells/ConferenceRecommendationCell.swift:1007` |
| Live purpose/availability matching | Partial. The recommendation loop explicitly passes `Self.directoryCandidates()`; that function contains five fixed candidates. `availableForMeetings` is a candidate Boolean. Participant scheduling separately hydrates slots from Entity and toggles availability; a live join between every independent event's capacities, participant calendars and recommendations is not established. | `Sources/App/Cells/ConferenceMVP/Cells/ConferenceRecommendationCell.swift:321`, `:943`, `:1020`; `Sources/App/Cells/ConferenceMVP/Cells/ConferenceSchedulingCell.swift:162`, `:185`, `:295` |
| Participant discovery | Partial portable aggregation. Discovery normalizes recommendations, search and known participant rows, with chat/proof invitation paths and optional nearby enrichment. This is broader than only the fixed recommendation examples, but does not establish an umbrella-wide semantic directory. | `Sources/App/Cells/ConferenceMVP/Cells/ConferenceEntityDiscoveryCell.swift:227`, `:256`, `:343`, `:417` |
| Conference simulation UI | Implemented source path. `/conference-admin` is admin-only; AdminShell merges Studio with actual Population/Playback states and forwards their actions. Studio alone still contains stale “phase 1” placeholders. UI not launched here. | `Sources/App/Controllers/VaporConferenceMVP.swift:135`; `Sources/App/Cells/ConferenceMVP/Cells/ConferenceAdminShellCell.swift:783`, `:1824`; `Sources/App/Cells/ConferenceMVP/Cells/ConferenceSimulationStudioCell.swift:167` |
| Synthetic conference entities | Implemented source. Population resolves synthetic identities, registration and onboarding, writes profile, purpose snapshot and consent and publishes a demo contact endpoint. This is real mutation through cells, not merely counters. Reset clears the working set but leaves persisted entities and organizer aggregates intact. | `Sources/App/Cells/ConferenceMVP/Cells/ConferenceSimulationPopulationCell.swift:243`, `:293`, `:451` |
| Conference playback | Partial replay. Organizer-owned inspect-only snapshots; selecting a snapshot does not restore participant entities or aggregate truth. It is not deterministic replay of every semantic action. | `Sources/App/Cells/ConferenceMVP/Cells/ConferenceSimulationPlaybackCell.swift:134`, `:154`, `:215` |
| Swarm runtime | Implemented source executable and single/coordinator/worker modes. WebSocket connection factory; workers/shards; deterministic identity context naming; generated signing keys. | `Sources/UserSimulationScaffold/main.swift:11`; `Sources/UserSimulationScaffoldCore/SimulationRoutes.swift:415`; `Sources/UserSimulationScaffoldCore/SimulationModels.swift:442` |
| Swarm administration | Implemented API: create/get run, pause/resume/stop run or shard, list/control users, inject failure, behavior mix, JSON/Prometheus metrics. `/swarm/cells` is a descriptor catalogue, not a graphical control plane or proof that cells are registered and callable in a target resolver. | `Sources/UserSimulationScaffoldCore/SimulationRoutes.swift:44`; `Sources/UserSimulationScaffoldCore/SwarmToolCells.swift:44`, `:132` |
| Swarm graphical workbench | Design approved, implementation not established. 2026-09-30 approval explicitly covers visual sketches only; G1/G2/G3 remain waiting. Do not represent mockup buttons as connected runtime. | `Deliverables/PDD_swarm-workbench_2026-09-29/STATUS.md:6`, `:20`, `:25`; `Deliverables/PDD_swarm-workbench_2026-09-29/DESIGN_APPROVAL.json:7` |
| Swarm behaviors | Implemented transport behaviors: lurker, reader, requester, agentConversationUser, slowSubscriber, reconnectingMobile. Reader gets `state`; requester writes `simulation.ping`; conversation user sends generic request/post prompts. No event/company/availability/meeting workflow behavior is present in this enum/switch. | `Sources/UserSimulationScaffoldCore/SimulationModels.swift:49`; `Sources/UserSimulationScaffoldCore/VirtualUser.swift:277`, `:285` |
| Swarm persistence and repeatability | Partial. Run dictionary starts empty in memory; stop writes a summary best-effort. Identity context is repeatable, but new Curve25519 private keys are generated on creation. Stable naming is not persisted entity identity or reproducible key material. Restart/run recovery was not established. | `Sources/UserSimulationScaffoldCore/SimulationCoordinator.swift:16`, `:94`; `Sources/UserSimulationScaffoldCore/SimulationModels.swift:463` |
| Swarm security | Implemented signed requests with body hash, time window, nonce replay check and role credential; observer reads/operator writes/nodeAgent worker calls. Default mode permits legacy token **or** identity, with default local-dev token and loopback bind; production safety depends on configuration, not the mere presence of signed access code. | `Sources/UserSimulationScaffoldCore/SimulationAdminAccess.swift:272`, `:302`, `:463`; `Sources/UserSimulationScaffoldCore/SimulationRoutes.swift:276` |
| Existing test evidence | Tests present, unexecuted. Event tests cover creator ownership, create/publish/archive, invalid schedule, permission gates, snapshot semantics and federation opt-in. Small swarm test uses six users and ScriptedLoadBridgeConnectionFactory; this is useful simulator-contract coverage, not live OIW entities. | `Tests/EventCellsTests/EventPublisherRegistryCellTests.swift:10`, `:72`, `:148`, `:249`, `:385`; `Tests/UserSimulationScaffoldTests/UserSimulationScaffoldTests.swift:483` |

## Answer to “does the swarm have an admin UI?”

**It has an administrative API. A new graphical Swarm workbench has approved sketches, with no implemented runtime wiring demonstrated in the inspected work. Separately, the conference already has an admin simulation UI backed by conference-specific cells.** These should be presented as three distinct surfaces. A generic statement “there is no administration” is as misleading as “the approved workbench already runs the swarm.”

## Existing local runner and what can actually run now

An executable exists at `CellScaffold/.build/out/Products/Debug/UserSimulationScaffold`, size 105,694,000 bytes, executable bit set, mtime 2026-09-28 23:43:43 UTC. That is artifact inventory only; its build revision/dependencies were not authenticated. No listener was found on local TCP 8091 or 9089. It was **not executed**.

`scripts/run-swarm-level2-performance.sh:4` expects an already running swarm at 8091 and target bridge at 9089. It defaults to 50 users, has bounded timeout and a stop trap, but its behavior mix includes generic AI conversation prompts (`:84`) and requester writes. Running it unchanged would not meet a read-only/provider-free first phase. It also proves bridge metrics, not semantic conference outcomes.

The existing six-user small test (`UserSimulationScaffoldTests.swift:483`) supplies a scripted connection factory. Its test name “realistic” must not be inflated into live conference verification. No ready standalone UserSimulation test executable was found in the inspected build products; an AppTests bundle is a different artifact.

Parent decision: do not run the stale binary and do not invent a fake bridge merely to get a green result. The proposed GUI simulation is a **scenario preview**, not an executed backend simulation.

## Smallest useful next simulation

Split the next proof into two explicit goals; neither should claim success for the other.

**Goal A — technical swarm proof:** use a verified current executable and a dedicated already verified local bridge/scaffold with synthetic identities, no real user dataset and no AI provider. Six users, two shards, seed 42, lurker/reader only, 15-second duration. Reuse real coordinator/worker/VirtualUser and metrics code. Pass conditions: six correctly isolated synthetic identities connect and subscribe; reader requests receive the expected target state; run stops and releases sockets; artifact report records errors and timing. `get` send latency alone is not proof of a successful semantic response. No new fake adapter is necessary if a suitable verified target bridge exists; none was available in this audit.

Future command shape (supported `serve` entrypoint in `Dockerfile.swarm:108` and runbook `Documentation/SwarmScaffold_Staging_Runbook_2026-06-20.md:30`; not executed here):

```sh
# VERIFIED_SWARM_EXECUTABLE must identify a freshly verified build.
# SIMULATION_ADMIN_TOKEN must be a fresh local token, not an existing secret.
SIMULATION_MODE=single SIMULATION_HOSTNAME=127.0.0.1 SIMULATION_PORT=8091 \
SIMULATION_RUN_DIR=/tmp/oiw-technical-swarm \
"$VERIFIED_SWARM_EXECUTABLE" serve
```

Create request body supported by `SimulationModels.swift:128`:

```json
{
  "runId": "oiw-technical-synthetic-001",
  "userCount": 6,
  "shardCount": 2,
  "seed": 42,
  "targets": [{"id": "verified-local-test-scaffold", "baseURL": "http://127.0.0.1:9089", "weight": 1}],
  "ramp": {"initialUsers": 2, "rampUsersPerSecond": 2, "maxDurationSeconds": 15},
  "behaviorMix": [{"script": "lurker", "weight": 1}, {"script": "reader", "weight": 1}],
  "topics": ["conference.chat"],
  "bridge": {"mode": "bridgehead", "publisherId": "Porthole", "bridgeId": "CloudBridge"}
}
```

Future authenticated calls: `POST /simulation/runs`; `GET /simulation/runs/oiw-technical-synthetic-001/users`; `GET /simulation/metrics?runId=oiw-technical-synthetic-001`; optionally `format=prometheus`; explicit cleanup `POST /simulation/runs/oiw-technical-synthetic-001/stop`. Use a bounded supervisor and stop cleanup even on failed assertions. These routes are retrieved source facts, not a statement that those ports are live.

**Goal B — smallest meaningful conference scenario:** two independent publishers, one proposed umbrella collection, three events with one time conflict, six synthetic participants spanning three explicit purposes, one participant unavailable and one withholding matching consent. Shared event facts change once; only one consenting participant receives private enrichment. Assert separate publisher edit authority, visible publication snapshots, affiliation labeling, no double-booked meeting, no use of nonconsenting private data, source-attributed advice, and restoration/cleanup of the test namespace. This is a proposed acceptance scenario, not supported out of the box.

Exact missing adapters/contracts for Goal B:

1. **Scenario-to-domain adapter:** compile umbrella/publisher/event/person/company fixtures to EventPublisherRegistry and ConferenceRegistration/Onboarding calls; explicitly bridge event identifiers into the conference workspace. Current swarm scenario only contains users/shards/targets/topics/behavior mix.
2. **Identity adapter:** bind each `simulation.<run>.user.<index>` to a synthetic participant/entity and the correct authorization context. Current conference population and swarm independently manufacture identities; stable string context alone does not join them.
3. **Domain behavior runner:** actions for discover published events, publish/update event under correct authority, modify purpose/availability/consent, request/accept/decline meeting, ask an advisor and verify result. Current VirtualUser switch issues generic transport actions once at connection start.
4. **Live matching projection:** feed actual consented synthetic participant data and availability into ranking; the inspected recommendation generator uses fixed candidate fixtures, and event models lack purpose/availability contracts.
5. **Umbrella membership contract:** shared collection and provenance without transferring child organizer authority; explicit distinction between proposed membership, accepted membership and official affiliation. Local opt-in search is not this contract.
6. **Clock and evidence adapter:** relate compressed ConferenceSimulationClock to swarm task scheduling and semantic assertions; record seed, domain actions, outputs, source revisions, access decisions and expected/actual outcomes. Current conference playback only inspects snapshots; swarm metrics primarily count transport events.
7. **Isolation and cleanup adapter:** disposable storage/identity namespace and cleanup receipts. `simulation.resetPopulation` explicitly leaves entities and organizer aggregates intact, so it cannot be used as transactional rollback.

The primary shared-knowledge/secondary private-enrichment architecture is a sound candidate to test, not established by this audit. Its retrieval contracts and advisor orchestration are outside this source slice and remain the parent's knowledge/advisor assessment.

## Three strongest counterarguments

1. **Reuse of the swarm does not validate the event product.** A swarm can successfully create sockets, send `state` and count flows while every recommendation or meeting is wrong. Steelman: the real existing coordinator, authentication, shards and metrics are worthwhile infrastructure. Ruling: reuse them, but require semantic adapters and assertions before calling the product simulation successful.
2. **A federation label does not supply independent-event governance.** Existing implementation has multiple publishers and opt-in search, which is substantive reuse. But umbrella membership, provenance and organizer autonomy remain separate contracts; treating a local registry query as federation would conceal the hardest boundary. Ruling: implement only the missing umbrella link, not a parallel event CRUD system.
3. **Rich simulation can manufacture evidence of usefulness.** Fixed candidates, hand-authored synthetic purposes and consented profiles can make matching look convincing without predicting actual user benefit. Existing live cells reduce some integration risk, but reset leaves persistent truth and playback is inspect-only. Ruling: first prove source/authority/consent/time-conflict invariants on a disposable fixture; measure useful recommendations with real participant evaluation separately.

## Terminal assessment and handoff

Purpose for this advisor: reduce implementation uncertainty; taxonomy reference deliberately `purpose://prompt.unknown` rather than inventing a canonical purpose. Goal: retrieve named source anchors for conference CRUD, umbrella, purpose/availability, swarm administration, execution and persistence and give a falsifiable minimal next run. **Satisfied for the bounded source audit.** Execution and semantic integration remain explicitly untested/open, owned by the parent task and Kjetil's subsequent implementation decision.

Load-bearing adjudications: multi-publisher CRUD supported in source; local opt-in federation supported but broad federation undercut; admin API supported; completed graphical workbench unsupported; conference-specific synthetic population supported; swarm-to-conference semantic adapter not found; deployment and run success open/untested.

Quality diagnostics: Q1 all corrections cite code (notably Studio placeholders versus AdminShell merge); Q2 mixed result, both substantial reuse and material missing links; Q3 all implementation findings carry retrieved anchors, negative findings explicitly bounded; Q4 findings do not depend on whether OIW or another umbrella is chosen; Q5 no unflagged unfalsifiable capability claims; Q6 no actual scenario run in this audit, so no probability claim; Q7 motives/person scoring not applicable; Q8 all verdicts closed or explicitly open with owner; Q9 strongest reuse defense comes from existing source, no independent opposing empirical source reviewed; Q10 no unanchored concessions.

Reusable learning to capture centrally in the parent session: **conference simulation and generic swarm are separate; ConferenceAdminShell overrides stale Studio phase-1 placeholders with real Population/Playback, while Swarm workbench approval covers sketches only.** No skill/source edits made by this read-only advisor. Parent should route the learning with `haven_learn.py` before choosing its canonical target.
