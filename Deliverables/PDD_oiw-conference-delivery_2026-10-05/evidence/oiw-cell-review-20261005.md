# Brief audit — ConferenceCommons Cell, 2026-10-05

Read-only source review of the candidate in `CellScaffold/.worktrees/oiw-conference-20261005`; no code edits, build, tests, browser, network or device use by this advisor. The parent changed source during review. Findings below distinguish initial defects from fixes subsequently observed. These are source findings, not an acceptance claim.

Base: `codex/oiw-conference-20261005`, HEAD `e5c3434510884275cae4a732935ab4b55cf7fad9`. Worktree has modified `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift`, `Sources/App/Controllers/VaporEventPlatform.swift`, `Sources/App/configure.swift`; new `Sources/App/Cells/ConferenceCommons/` and `Tests/AppTests/ConferenceCommonsStateTests.swift`. Line references are to the reviewed candidate; ongoing parent edits can move them. CellProtocol actually used by the build cache is `81601a6f835252aba7e99d43786fb5d67227c245` (published 2026.9.4), not the newer local scanner candidate.

## Findings

### P1 — A failed readback could restore old consent/content through later persistence (source fix observed)

Initially `ConferenceCommonsCell.perform` always cleared `pending` in its defer, including when snapshot persistence may have succeeded but the readback failed. `encode` chooses `pending ?? committed`; after this ambiguous outcome it would encode the old committed state. For example, a stored revocation followed by a readback error could later be overwritten with the old, unrevoked content by ordinary Cell persistence.

Observed parent fix: `Sources/App/Cells/ConferenceCommons/ConferenceCommonsCell.swift:121–125` retains the candidate when `durabilityUncertain`; `:231–232` hides content during the unresolved write. `:197–202` requires storage plus typed readback equality, and `:116` blocks further mutation. This fixes the identified stale overwrite route in source. No fault-injection verification was run. Browser refresh alone has no recovery mechanism in this Cell: the flag is not cleared anywhere; presentation must not promise refresh resolves it. A reload/reconciliation needs to establish which snapshot won before mutations resume.

This readback matters with the actual dependency: CellProtocol `Sources/CellBase/Cells/CellResolver/CellResolver.swift:553–592` returns true after invoking `storeAsTypedCell` and touching lifecycle state; true is not itself a storage write acknowledgement. The candidate correctly adds a decoded-state equality check rather than treating that bool as full confirmation.

### P1 — The recipient could approve a plan they were never shown (source fix observed)

Originally meeting rows and selections omitted participants, start/end/timezone, retention deadline and source metadata. A second participant could receive the proposal and press `meeting.approve` without any projection carrying the actual plan. Review approval likewise omitted the sources that would be published with the text. The model binds approval to revision, but version binding cannot make absent material reviewable.

Observed parent fix: `Sources/App/Cells/ConferenceCommons/ConferenceCommonsCell.swift:262–268` now includes names, exact time window, timezone, private access expiry, explicit no-recording wording, shared text and sources in the meeting detail; the revision and audience remain in the note. `Sources/App/Cells/ConferenceCommons/ConferenceCommonsConfiguration.swift:869–871` and `:975–977` are the approval actions. Source fix observed; actual List rendering and two-requester approval path remain untested. Names are presentation labels, not cryptographic identity proof.

### P1 — Revocation/expiry left server-side form copies of the shared text (source fix observed, lifetime qualification below)

Originally `ui.select` copied meeting shared text into `drafts[principal]`; the public state response later returned those fields without checking the meeting. Revoking or expiring the canonical Meeting erased/hid its text but the same server continued serving the copied private text in `state.draft.content`. Reproduce with A/B: B selects review, A revokes, B reads state again.

Observed parent fix: `Sources/App/Cells/ConferenceCommons/ConferenceCommonsCell.swift:234–240` clears retained form content/source fields linked to a missing, revoked or expired meeting before state projection. The review remains read-only; no cross-requester or race verification was executed. This is server-cache cleanup, not removal of previously delivered bytes from participants' devices.

### P1 — Deadline deletion was promised but only opportunistic expiry was implemented (claim corrected in source)

`Sources/App/Cells/ConferenceCommons/ConferenceCommonsState.swift:343` clears private meeting material when explicitly called. Its only production caller in the reviewed candidate is `ConferenceCommonsCell.swift:143`, on a tentative copy inside another command. The deletion reaches persistent state only if that command succeeds and persists. No new action, or a failed command, leaves expired material in the existing encoded snapshot indefinitely. Filtering expired rows on GET does not erase stored material.

The initial skeleton called the field “Slett privat møtemateriale senest” (`ConferenceCommonsConfiguration.swift:846,853`). This was stronger than the implementation. A complete deletion claim needs an independently committed expiry sweep (including restart/dormancy behavior and retained private form copies), with acknowledged storage failure handling. The smaller truthful first delivery is access expiry: label it that way, document that persistent deletion is not implemented, and do not claim a hard deletion deadline. At final inspection both the input label (`Configuration:846,853`) and meeting detail (`Cell:267`) use access-expiry wording. Thus the overclaim is corrected in source; persistent deletion remains unimplemented and must also be bounded in delivery documentation.

### P2 — There is no normal UI path to create a second contribution

`Sources/App/Cells/ConferenceCommons/ConferenceCommonsCell.swift:138` generates a new contribution ID only when the private form ID is empty. Saving leaves that ID in the form. Selecting any visible contribution also places its ID there (`:258–260`). The skeleton shows this ID as read-only Text (`ConferenceCommonsConfiguration.swift:277–285`), and its save/publish/withdraw actions all use the current form with `{}` payload (`:270–317`). No new-draft/reset action was present at this inspection.

Reproduce: save and publish contribution 1, replace its text, press “Lagre privat utkast”. The action tries to edit the immutable published contribution 1 and fails; choosing somebody else's public contribution makes the form target an item the requester cannot edit. Add an explicit “Nytt privat utkast” action that clears contribution selection/revision/content/source metadata and copy permission while keeping the selected umbrella. Test two sequential publications and selecting someone else's contribution before starting a new one. This does not require a new persistence model.

## Authority and transport checks

- Requester authority is evaluated by the actual Cell. The Cell principal includes requester UUID and signing-key fingerprint; `validateCellSpecificAccess` calls `verifyRequesterIdentityControl`; writes repeat that check. This prevents trusting arbitrary form UUIDs for private participant actions. It is not itself proof of publisher membership: CellProtocol `GeneralCell.swift:2249–2284` proves control of the presented key. The reviewed `ConferenceCommonsCell.can` still calls the legacy publisher access evaluator. Parent had independently identified this and is integrating registry-bound publisher keys; do not count self-key control plus a UUID ACL as a publisher binding.
- Private contribution projection filters by requester author; meetings filter by participant, umbrella, deadline and phase. No new cross-principal read leak was confirmed beyond the server draft lifetime defect above. The pure model accepts string principals/capability booleans and therefore cannot prove the real Cell authority path.
- The suspected prefixed-keypath mismatch is **not a bug in the served web host**: `Public/js/conference-mvp.js:779–790` removes the configured root alias. The configuration's first reference is `conferenceCommons`. `:116–141` dispatches actions and awaits field flushing; `:181–205` serializes pending field submissions. The HTTP route `Sources/App/Controllers/VaporEventPlatform.swift:235–240` passes the normalized keypath and payload to the Cell. This source evidence is not a rendered or native acceptance result.
- Parent's independently found Tabs envelope mismatch and `Foundation.DecodingError` qualification were already corrected in source during review. They are not new findings here. Parent reports the initial build stopped at the decoder error; this advisor did not execute any test or build.
- `Tests/AppTests/ConferenceCommonsStateTests.swift` currently exercises the value-state model and configuration decoding. Its expiry test manually calls `expireMeetingContent`; it cannot prove an actual scheduled deletion, real Cell authorization, stored-write acknowledgement, API action journey, or native rendering.

## Small next verification slice, when tests are authorized

Use the actual Cell + Resolver boundary for (1) a successful store followed by failed readback and later encode/reload; (2) two separate proven requesters selecting and revoking a shared review; (3) complete plan/source projection before each approval; (4) two consecutive new contributions through the actual skeleton action envelopes. Keep storage-fault tests separate from pure state transitions. There is no native microphone adapter or real nearby/device claim in these files, and none was introduced by this review.

Learning handoff to parent: the main reusable pitfall is that requester-filtered canonical reads do not erase private copies in transient UI form caches, and a pending storage candidate must survive an uncertain acknowledgement so normal persistence cannot restore old authority/content. Parent owns required learning capture; advisor made no repository/skill mutations.
