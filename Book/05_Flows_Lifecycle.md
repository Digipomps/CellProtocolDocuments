# Chapter 05 — Flows and Stream Lifecycle

Last verified against CellProtocol:
`bfc176ffecd4f718cd47e4a9db6183a2b0378def` (2026-07-14)

Status: implemented and contract-tested for the local Swift `GeneralCell`
subscription lifecycle described below. Durable replay, universal per-event
signatures, and live remote teardown acknowledgement are not generic guarantees
of the current implementation.

Flows are the outbound event mechanism exposed through `Emit`. A `GeneralCell`
can attach labelled emitters, start and stop subscriptions, transform incoming
events through an intercept, and forward accepted events to its own feed.

## 1. Current `FlowElement` wire shape

The Swift runtime currently encodes these fields:

- `id`
- `title`
- `topic`
- `content`
- optional `properties`
- optional `origin`

`properties` can describe the element type, content type, and MIME type.

The generic `FlowElement` wire type does **not** currently contain a mandatory
sequence number, timestamp, producer signature, causation identifier, or
logical clock. Particular Cells and higher-level contracts may add such data to
their payloads, but callers must not infer those guarantees from `FlowElement`
itself.

## 2. Access boundary

Attaching an emitter and starting or mutating a labelled subscription are
Cell-specific write operations. `GeneralCell` validates `-w--` access at the
label before performing the supported mutation.

The owner is not replaced by a renderer, transport, cookie, or admin fallback.
Non-owner access must come from the normal Agreement/Contract capability path.
An unauthorized requester must not attach, start, pause, drop, or detach the
owner's flow.

## 3. Local subscription lifecycle

### 3.1 Attach

`attach(emitter:label:requester:)` associates an emitter object with a label
after authorization. Connection identity is object identity, not only the
emitter UUID. Replacing an emitter with a different object invalidates the old
subscription even when both objects carry the same UUID.

### 3.2 Start

`absorbFlow(label:requester:)` starts forwarding the attached emitter's flow.
If the emitter conforms to `CellRuntimeReady`, its runtime readiness is awaited
before the upstream flow is read.

Start is single-flight per label:

- concurrent callers share one pending setup result;
- only one upstream subscription is installed for that generation;
- all pending callers observe the same success or terminal failure;
- detach or replacement invalidates a late setup result before installation.

### 3.3 Forward

Each installed subscription has one serial event processor. Values are handled
in upstream order for that subscription:

1. load and run the optional async feed intercept;
2. re-check overflow/generation validity;
3. reserve an in-flight forwarding lease;
4. synchronously send the transformed value to the Cell feed;
5. release the forwarding lease.

A missing label fails only that start request. It does not terminate unrelated
subscribers to the Cell's shared feed.

### 3.4 Complete

Upstream completion is serialized after already accepted values. Completion
clears the active subscription generation while leaving the emitter connected,
so a later authorized `absorbFlow` can subscribe again.

### 3.5 Drop and detach

The waitable mutation APIs are:

- `dropFlowAndWait(label:requester:)`: stop the active subscription but keep the
  emitter connected;
- `detachAndWait(label:requester:)`: stop the active subscription and remove the
  emitter association.

The older `dropFlow` and `detach` entry points remain asynchronous convenience
wrappers. A host that must read status or replace a source immediately after a
mutation must use the waitable form.

Teardown removes the pending/active generation from actor state and invalidates
its forwarding leases before the first suspension. Upstream cancellation and
the drain of already-started downstream delivery run concurrently. Cleanup of
an old generation owns only its captured resources and cannot clear a newer
generation created through cancellation re-entry.

## 4. Bounded buffering and failure behavior

The local `GeneralCell` subscription processor uses a bounded buffer of 256
events. It does not silently accept unbounded memory growth.

If the buffer overflows, including when completion cannot be inserted at exact
capacity, the generation fails closed:

- the overflow state is marked once;
- queued forwarding becomes invalid;
- the event processor and upstream subscription are cancelled;
- pending callers receive the same overflow failure;
- status becomes inactive;
- a later explicit `absorbFlow` can create a fresh generation.

Overflow recovery reloads the currently connected emitter after awaited cleanup.
This prevents a stale emitter object from being selected if another object with
the same UUID is connected during cancellation.

The buffer bound is an implementation property of this local forwarding path.
It is not a universal transport-level backpressure guarantee.

## 5. Resource lifetime and cancellation

Subscription resources own the upstream cancellable, event processor,
continuation, and overflow/forwarding state.

The verified lifetime rules are:

- releasing a subscribed `GeneralCell` cancels the upstream subscription even
  without an explicit detach;
- suspension inside an async intercept does not keep the Cell alive;
- a synchronously blocked downstream subscriber does not keep the Cell's
  auditor/resource chain alive;
- explicit waitable teardown waits for an already-started forwarding lease;
- external cancellation callbacks are not executed while the auditor actor is
  holding its state transition.

An already-entered downstream callback is ordinary synchronous subscriber code
and may return later. Teardown prevents a new stale delivery; it cannot force
arbitrary subscriber code to return.

## 6. Status and graph traversal

Connected labels and attached status arrays use canonical sorted label order.
Status reports whether a label is connected and whether its current generation
is active.

Nested attached-status traversal is cycle-safe for self-cycles and multi-Cell
cycles. The traversal guard is path-scoped so sibling aliases that point to the
same Cell are still represented.

## 7. What the current contract does not prove

The current implementation and tests do **not** establish that:

- every FlowElement is signed, timestamped, or globally sequenced;
- every Cell has durable event storage or deterministic replay;
- replay always reproduces an exact historical stream;
- all transports have identical buffering, ordering, or teardown-ack behavior;
- a local waitable detach is acknowledged by a live remote peer;
- contradictory lifecycle calls are one globally serialized transaction;
- application-specific decoded bindings are ready unless the Cell exposes and
  the host awaits `CellRuntimeReady`;
- every first-party Cell or cross-language runtime uses this Swift
  `GeneralCell` lifecycle.

Generation identifiers make overlapping local cleanup safe: a new generation
may start while old external cancellation finishes, but the old cleanup cannot
install, forward through, or remove the new generation. This is generation
isolation, not global transaction serialization.

## 8. Required regression gates

Changes to this lifecycle should retain tests for:

- unauthorized attach/start/drop/detach;
- concurrent start single-flight and shared failure;
- detach or replacement during suspended setup;
- replacement by a distinct object with the same UUID;
- serialized async intercept/value/completion order;
- exact-capacity completion overflow and post-overflow fail-closed behavior;
- waitable teardown during in-flight downstream delivery;
- cancellation re-entry on the same label;
- Cell release during normal delivery, suspended intercept, and blocked
  downstream delivery;
- canonical status order and cycle-safe traversal;
- restart/resubscribe after completion or overflow.

At the verified revision, `IntegrationTests` executes 35 such integration tests
and the complete Swift package executes 705 tests with zero failures. Those
counts prove the tested revision and paths only; they are not evidence that all
HAVEN flow behavior, deployments, or cross-runtime implementations are robust.
