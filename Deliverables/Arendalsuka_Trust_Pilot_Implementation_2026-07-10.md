# HAVEN Arendalsuka trust pilot - implementation status

Date: 2026-07-10  
Target: Arendalsuka 2026, 10-14 August  
Delivery horizon: 31 days

## Decision summary

The participant-facing trust pilot is implemented on `codex/arendalsuka-trust-pilot` and is a credible release candidate for the central story: HAVEN acts as a participant-owned digital extension that keeps private context local and shares only an explicit, reviewable meeting package.

Release-candidate commits: `93604b9`, `cfbb8f0` and import-security commit `1a8f67c`.

The code and browser journey are ready for staging review. Fabel 5 found no remaining P1 code defects in its final meeting-flow review; its two P2 staging gates were then fixed and covered by focused regression tests. The POI operational gate is now closed: 271 named OSM candidates were posted in six successful batches, producing 268 local actors and 468 map features. The strict staging data canary passes with 2218 program sessions and 80 visible sessions.

## Formål og mål

### Formål 1: Gjør tillit observerbar

Goal: A participant must be able to see what HAVEN shares, what remains private, and whether an action actually succeeded.

Status: **Achieved for the meeting pilot.**

- The meeting surface separates `Dette deles` from `Dette forblir privat` before sending.
- Private agenda, notes, search, ranking, precise location, email and raw identity keys are excluded from the meeting payload.
- Sending and responding require explicit participant actions.
- A participant is hidden from the meeting directory until they explicitly enable visibility; reading state has no directory or profile persistence side effect.
- Disabling visibility prevents new requests while preserving existing request, meeting and receipt history.
- A duplicate pending request returns an explicit `already_pending` outcome in either direction and emits no false creation event.
- The hub uses the signed requester as actor and ignores actor spoofing fields.
- Recipients must already be known in the server-side participant directory.
- Meeting purpose is locked to `purpose://event.meeting-place.agree`.
- Request and meeting identifiers are server-owned in the Arendalsuka variant.
- Receipts distinguish persisted, partial, failed and declined outcomes.
- A persisted agreement record is described as `lagret avtalepost`, explicitly not as a cryptographic signature.
- Unsupported rescheduling and shared-message actions are absent from the pilot Cell surface.

### Formål 2: Vær nyttig under Arendalsuka

Goal: Combine the official program, a private agenda, sourced places and participant-to-participant meeting coordination.

Status: **Program, meeting core and sourced local POI layer achieved on staging.**

- Staging program journal: 2218 sessions, loaded.
- Staging visible sessions: 80.
- Staging map features after POI import: 468.
- Staging local actors/POIs after import: 268.
- Fresh local runtime intentionally starts without imported journals and therefore shows zero program rows. Import remains a signed admin operation rather than hidden demo seeding.
- The OSM/Overpass package contained 271 named POI candidates: 169 shops, 51 restaurants/cafes, 44 services and 7 bars/pubs. All six import batches succeeded through the authenticated import route.
- Import supports two explicit authority paths: an authenticated allowlisted admin session, which receives a 15-minute atlas-issued VC for the exact action, or a non-admin identity with an installed, atlas-signed `ArendalsukaImportAccessCredential` covering the action.
- Legacy capability proof artifacts are rejected as import authority even when cryptographically valid.

### Formål 3: Gjør HAVEN superb å bruke

Goal: The participant surface should feel like a focused product, not a protocol inspector.

Status: **Achieved for the implemented surface, subject to live-user review.**

- Product-first hero and Norwegian participant language.
- Four stable tabs: Program, Min agenda, Kart og steder, Møter.
- Responsive summary grid and two-column privacy comparison on desktop.
- Two-column tabs and single-column meeting flow on 390 px mobile.
- Minimum 44 px primary controls, visible focus states and restrained 6-8 px radii.
- No participant-visible UUIDs, `cell:///` endpoints, `purpose://` references or raw keypaths in the tested journey.
- Visibility status uses unambiguous language both before opt-in and after an explicit choice to hide.
- No console errors or page errors in the fresh desktop/mobile browser run.

### Formål 4: Gjør verifiseringen troverdig

Goal: Tests must not write to the user's real HAVEN storage and must not hide runtime races.

Status: **Substantially improved; suite-wide legacy debt remains.**

- XCTest runtime storage is process-isolated under the temporary directory.
- Each configured test app gets its own HOME, CellsContainer and SQLite database.
- Browser identity vaults capture one coherent storage root.
- Concurrent Porthole runtime binding installs are serialized per target and owner.
- The previous `AIAssistantThread` full-suite process crash no longer reproduces.
- Two historical test-created directories in the real user container were identified but intentionally left untouched pending owner decision.

## Verification evidence

| Evidence | Result |
|---|---:|
| ConferenceConnectionHub security and receipt tests | 4/4 passed |
| Arendalsuka atlas and participant program tests | 29/29 passed |
| Combined Arendalsuka + hub tests | 33/33 passed |
| Final post-Fabel hub/participant regression set | 6/6 passed |
| BrowserClientIdentityVault isolation tests | 12/12 passed |
| Published Arendalsuka API agreement/auth test | passed |
| Production skeleton binding integrity, isolated class | 4/4 passed |
| Desktop view smoke, 1440x1000, post-Fabel | passed, 0 console/page errors |
| Mobile view smoke, 390x844, post-Fabel | passed, 0 console/page errors |
| Fabel 5 final diff review | no P1 defects; two P2 gates fixed afterward |
| Import authorization route regression set | 3/3 passed, including issuer/subject/action/expiry boundaries |
| Arendalsuka import scripts, Node syntax | 3/3 passed |
| Final independent import-security review | CODEKLAR: GO, no actionable P0-P3 findings |
| OSM/POI staging import | 6/6 batches, 271/271 candidates, no failed batches |
| Strict staging data canary after import | passed: 2218 sessions, 268 local actors, 468 map features, 80 visible |

Browser artifacts: `/private/tmp/cellscaffold-arendalsuka-visual-proof-v7`.

POI import artifacts: `/private/tmp/arendalsuka-osm-import-2026-07-10`.

## Full-suite residuals

The latest complete suite snapshot before the final hub hardening completed without a process crash: 1214 tests executed, 9 skipped. It still reported 65 assertion failures across 35 test methods, including 19 unexpected thrown errors. The release-candidate baseline was covered by a focused 33/33 run; the later Fabel corrections were covered by a final 6/6 regression run and the isolated 4/4 production binding class. The dominant residuals are:

1. Shared `CellResolver` registrations with different scopes across test classes. An Arendalsuka renderer class is 4/4 green alone, while one atlas test can inherit a previously configured `scaffoldUnique` resolve in a mixed process.
2. AdminNodeFleet and Workbench tests that no longer satisfy current owner-proof/grant enforcement even when run without an Arendalsuka app in front of them.
3. WebKit/Mermaid integration assertions that remain environment-sensitive.

These failures prevent a claim that all of CellScaffold is green. They do not invalidate the focused Arendalsuka user-path evidence, but they must remain visible release debt.

## Walton-style claim review

Root claim: **A participant can reasonably trust HAVEN as a digital extension of self in the Arendalsuka meeting journey.**

Support:

- The participant sees the proposed disclosure before the side effect.
- Private fields are excluded by construction and covered by tests.
- Identity authority comes from a signable requester, not payload IDs.
- Server-known counterpart and purpose constraints limit confused-deputy behavior.
- Outcome language distinguishes a stored record from a cryptographic signature.

Critical questions:

- Does this prove HAVEN is universally secure? **No.** It proves this bounded journey and its tested contracts.
- Can a participant verify every downstream data use? **Not yet.** The receipt proves the hub outcome, not every later human or service action.
- Is the local-area utility complete? **For the bounded source set, yes.** The staging atlas now has sourced OSM POIs; field relevance and freshness still require live-user review.
- Does a polished UI alone establish trust? **No.** The trust claim depends on enforced identity, purpose, minimization and receipt behavior.

Adjudication: **Supported for a bounded live pilot; unsupported as a broad platform-wide trust claim.**

## Fabel 5 follow-up review

Fabel's first review identified three P1 defects: implicit directory enrollment on read, silent duplicate-send success, and an incomplete meeting package for the recipient. The final review confirmed all three closed in implementation and tests.

The final review then raised two P2 staging gates. Both are now closed:

- The hidden-state copy no longer says `skjult som standard`; it says the participant is hidden from new meeting requests, which remains true after an explicit opt-out.
- The participant-level incoming duplicate branch is exercised end to end: the reverse request is not created, the original incoming request remains unique, the draft is preserved, and the participant receives an honest status message.

Fabel also noted that a new request is possible after an earlier request is accepted. This is intentional: deduplication covers only a pending pair, while a later independent request may refer to another session or place. Rescheduling an existing Arendalsuka request remains disabled.

An independent Codex security review of the import hardening initially found that the legacy proof-artifact path could authorize a non-admin without the required atlas VC. That path was removed. The same correction removed self-issued admin fallback, restricted admin fallback credentials to one action and 15 minutes, moved CLI secrets to environment-only input, required HTTPS outside loopback, and added negative route coverage.

A follow-up review found that malformed legacy proof values could be mistaken for an absent field. Raw field-presence detection now rejects valid, malformed and scalar legacy proof inputs before either stored-VC evaluation or admin fallback. The final independent review found no actionable P0-P3 findings and marked the change `CODEKLAR: GO`.

The remaining release blockers are live-user and device evidence, not the POI data gate.

## Release gates

### Completed staging prerequisites

- Authenticated staging admin identity established without exposing its credentials in the report.
- Atlas-issued import credential exercised on staging.
- Prepared 271-candidate OSM package posted through the authenticated import route.
- Strict `arendalsuka:data-health` passed with no relaxed thresholds.

### Must pass before public live pilot

- Two real identities complete send, receive, accept and decline on staging.
- Verify persisted/partial/failed receipts against staging storage.
- Run mobile checks on iOS Safari and Android Chrome, not only Playwright Chromium.
- Add monitoring for program journal age, hub errors and failed agreement persistence.
- Prepare a participant-facing fallback when program import or meeting hub is unavailable.

## Recommended next sequence

1. Push and deploy the hardened release-candidate branch; verify health/build/ready, strict data health and the exact Arendalsuka deep link.
2. Perform a two-person staging rehearsal with real passkeys and capture receipts.
3. Run iOS Safari and Android Chrome field checks around Arendal with real location conditions.
4. Use the remaining July window for operational monitoring, fallback behavior and field usability before expanding the public feature surface.

## Sources

- Official event and dates: https://www.arendalsuka.no/
- Official program: https://www.arendalsuka.no/program?program=Hovedprogram
