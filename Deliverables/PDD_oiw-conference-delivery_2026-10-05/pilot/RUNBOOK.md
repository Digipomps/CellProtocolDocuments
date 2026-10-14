# Bounded OIW pilot

Status: prepared 2026-10-05; NOT executed, no invitations sent. Kjetil approved development/design, not an assertion of successful human acceptance. This is a product pilot, not an official OIW integration or representation.

## Scope and participants

First invited cohort: 6–8 people, two independent event organizers, one or two company representatives. Roles may overlap only if recorded. Use two actual participant identities for every mutual meeting check. Recruit no one automatically and import no attendee list. The host and data controller, actual dates, named cohort and contact person are selected before invitations.

Start with manually entered shared notes. Enable nearby/capture only after actual two-device and consent/revocation gates pass. Synthetic run results never count as human outcomes.

## Mandatory go/no-go before invitations

| Gate | Required observation | Current state |
|---|---|---|
| Build and regression | New and existing relevant suites pass on the exact release candidate | BLOCKED: first compilation failed; fix written, rerun awaiting user |
| Source/runtime identity | Deployed commit/image/pins, runtime owner and data root match evidence | NOT RUN |
| Event authority | Two publishers manage their own events; umbrella host cannot edit another publisher merely through affiliation | Tests written, NOT RUN |
| Private state | Private draft, non-discoverable intention and third-party meeting text absent from other requesters | Tests written, NOT RUN |
| Consent/version | Both users read and approve exact plan/content/audience; old approval fails after edits | Tests written, NOT RUN |
| Durability | Saved/revoked state survives clean process restart; uncertain write never reverts to older permissive state | NOT RUN |
| Group representation | Key-bound grant, expiry, renewal and revocation; retain permanent manager; no private employee Entity inheritance | Candidate under review, not applied |
| Entity expansion | Two processes/stores, real requester, exact selected version, recipient-owned signed commit, restart readback, lost-reply reconciliation | NOT RUN; shared Bridge integration dependency |
| Web/native GUI | All six approved areas usable in actual web and Binding hosts, compact/wide and light/dark | NOT RUN |
| Audio/nearby | Real device discovery plus separately approved capture; permission wait/revoke fence; retention cleanup | NOT RUN; microphone remains unavailable |
| Swarm | Real run ID, semantic assertions, fixed fixture, isolated synthetic identities, cleanup receipt | NOT RUN; existing generic transport metrics are insufficient |
| Rollback | Stop new writes, preserve evidence, restore prior release and verify private-state boundary | NOT RUN |

A failed required gate stops the relevant pilot leg. Notes-only can be its own expressly chosen scope; it must not be labelled as passing audio/nearby or cross-scaffold acceptance.

## Rehearsal journey

1. Organizer A creates one publisher and draft event; organizer B creates another. Publish each with valid schedule, create one umbrella, request affiliations, and approve them as its authorized manager.
2. Six participants enter a concrete purpose, what they can offer and what they need. One chooses not to be discoverable; one has no overlapping time; one has no matching topic. Confirm those negative outcomes without manufacturing recommendations.
3. Two participants choose a common slot. Simultaneously attempt a second booking for one participant; one confirmation must fail with a comprehensible conflict. Verify cancellation releases only its own reservation.
4. Each person saves a private contribution. A second participant must not see it. Publish one exact version with source and uncertainty. Create a disagreement/correction linked to it without rewriting the original.
5. Both meeting participants read purpose, participants, exact interval/timezone, retention deadline and capture scope. One approval is insufficient. Revoke while awaiting the other participant; stale approvals must fail.
6. Propose a short shared note. Both read the same revision and audience. Change one sentence; both approvals must be invalidated. Publish only after renewed approvals. Either participant withdraws; all cached views must drop the withdrawn meeting text.
7. For Entity expansion, select only a contribution whose author explicitly permits retention. Verify owner-controlled import, exact source/revision receipt and restart readback in another scaffold. Keep raw private meeting material outside the export.
8. A company manager removes one representative and allows another grant to expire. New company actions must fail for those principals; their private personal Entities remain intact.
9. Run the same semantic journey through Swarm with synthetic actors. Compare observed domain receipts, not sent-message counts. Stop/pause/resume and cleanup must have separately observed results.

## Evidence sheet (one row per actual run)

Record: run ID; source and binary SHA; dependency pins; local/staging host; two device/app versions where relevant; pseudonymous actor alias → protected identity fixture reference; fixed timezone; start/end; expected result; actual result; exact receipt/log/screenshot reference; reviewer; residual data after cleanup.

Store evidence in the task's private pilot directory. Do not put participant transcript/private content in general diagnostics. Identify uncertainty explicitly. A screen capture is evidence only for its recorded runtime and device, not every scaffold.

## Session and success criteria

Reserve about 60–90 minutes after technical gates, with a facilitator who can stop the session. Measure observed task completion, unassisted steps, confusing consent decisions, errors/timeouts and what genuinely improved shared understanding. Suggested pass: both independent events reachable, all private-state and unauthorized-action checks pass, each consenting pair completes versioned sharing, and every retained Entity contribution has its receipt. Any privacy breach, unauthorized effect, unexplained loss or false success is an immediate stop.

## Stop and recovery

Disable new cohort actions through the existing host policy; do not destroy transcripts/logs while diagnosing. Preserve exact failed request/ref and authority decision without printing private values. Restore the last verified release only through the coordinated deploy path and own claim. Recheck identity/persistence/version boundaries before resuming. Deletion and retention outcomes must be recorded separately from UI disappearance.

## Required human decisions before the actual pilot

Named coordinator/data controller, selected participants, target host, dates, consent information and retention policy, supported devices, and whether this cohort includes audio/nearby. These do not block the already approved source implementation. Do not send invitations until Kjetil explicitly authorizes recipients and message.
