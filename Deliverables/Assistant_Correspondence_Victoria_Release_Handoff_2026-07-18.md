# Assistant Correspondence — Victoria release handoff

Date: 2026-07-18  
Human task owner: Kjetil  
Prepared by: Codex  
Status: controlled test candidate ready; staging enrollment and formal Apple distribution remain open

## Source basis

- Signed package and release files in
  `/Users/kjetil/Desktop/HAVEN-Assistant-Correspondence-Pilot-0.3.1-universal2-TESTKANDIDAT-2026-07-18`
- `HavenAgentD/Documentation/ProvisioningPack.md` and
  `HavenAgentD/Documentation/OperatorRunbook.md` from the reviewed Binding PR
- `Binding/HavenAgentD/Packaging/Resources/ASSISTANT_CORRESPONDENCE.md`
- `CellScaffold/scripts/create-assistant-correspondence-pilot.py`
- Canonical identity, agreement, resolver and security chapters
- Coordination response from the Codex task `Evaluer admin-tjenesten`

No invitation secret, access credential, private key or server environment value
is included in this handoff.

## Formål

### `purpose://contact.communication`

Intent: establish a persistent, purpose-limited asynchronous mailbox between
Lille Robot at Victoria and Codex at Kjetil without turning message content into
remote execution authority.

Goal: the M4 Mac mini installs the signed client, requests access, receives a
human-issued Entity/device-bound proof, and exchanges one authenticated harmless
message in each direction.

Done means: both profiles pass `doctor`; `victoria-lille-robot` can send only to
an allowed peer using the four correspondence operations; the first message is
observed and recorded as a milestone.

### `purpose://access.audit.privacy`

Intent: make participation explicit, revocable, inspectable and narrower than
possession of an installer or invitation.

Goal: the invitation is short-lived, single-use, transferred separately with
mode `0600`; staging stores only its hash; Kjetil explicitly approves or rejects
the signed request; every later operation presents a fresh device signature and
the signed capability proof.

Done means: no secret appears in Git, chat, the public installer folder or this
handoff; the issued proof is bound to Entity, identity key, device, resource,
purposes, four operations, expiry, approval receipt and revocation reference.

### `purpose://test.acceptance`

Intent: distinguish a controlled product test from a formal distribution claim.

Goal: architecture, package hash, Developer ID signature, timestamp,
Gatekeeper/notarization status, activation state and end-to-end message behavior
are each verified with explicit evidence.

Done means: Apple status is `Accepted`, the ticket is stapled, final package hash
is regenerated, staging cutover passes its release gates, enrollment passes, and
the authenticated round trip is green.

## Goal status

| Goal | Status | Evidence or blocker |
| --- | --- | --- |
| Sendable controlled test candidate | satisfied | Universal package SHA-256 `dc6bf8a5235235023be3636737a7ee79a77cbf90fa8ec3082c5c384d399a2b3a`; Developer ID Installer chain and trusted timestamp verified; `LES_MEG.md` describes the non-notarized status and boundaries. |
| Secret-free public package | satisfied | Desktop candidate contains no `victoria-invite.json`; client invitation is explicitly a separate trusted-channel artifact. |
| Apple-notarized formal package | blocked | The local execution policy denied upload of the private package to Apple's notarization service, even after informed user approval. No upload occurred; Apple did not reject the package. |
| Safe Victoria staging activation | blocked | Admin/release coordination forbids a standalone mutation/recreate on live `f916`; it would risk the known cold-restart/rehydration defect and invalidate locked release evidence. |
| Victoria access proof | pending | Requires fresh invite activation, Victoria's signed request and Kjetil's explicit action `Utsted adgangsbevis`. |
| Authenticated mailbox milestone | pending | Requires a valid proof and first message with sender ID `victoria-lille-robot`. An hourly read-only sender monitor is active on Kjetil's machine. |

## Claim graph summary

Root claim: **Assistant Correspondence is ready for a controlled Victoria test,
but not yet for an unqualified formal-distribution claim.**

Composition: `allOf` for the final product claim, with the following evaluated
premises:

1. The package is universal and signed by the expected Developer ID identity —
   supported by the manifest, hashes and macOS signature verification.
2. A non-notarized candidate may be transferred for an informed, controlled
   test — supported with the qualifier that Gatekeeper is expected to reject it
   as `Unnotarized Developer ID`, and the receiver must verify source, hash and
   signature.
3. Possession of an invite grants collaboration authority — contradicted by the
   protocol contract. An invite only authorizes a signed request.
4. Live `f916` can safely be restarted solely to rotate Victoria — contradicted
   by the locked release evidence and the Admin/release coordination decision.
5. The end-to-end product is complete — unsupported until staging activation,
   human approval, proof verification and authenticated message exchange pass.

The root claim for a **controlled test candidate** is supported. The stronger
claim for a **completed formal product delivery** remains open because its
composition is `allOf` and three operational premises are not yet satisfied.

## Decision log

1. Preserve the already sent preview and create a new, explicitly named
   `TESTKANDIDAT` rather than silently replacing files.
2. Do not place an invitation in the public installer folder.
3. Do not generate the short-lived Victoria secret before the coordinated
   cutover window. Generating it early would create a dead or expired artifact
   while staging intentionally rejects it.
4. Give the Admin/release task ownership of the exact-revision environment
   merge and app recreation. It must preserve all other participant hashes and
   volumes, create a backup and have rollback ready.
5. Treat first authenticated contact as a milestone, but monitor only envelope
   metadata until the user or assistant deliberately reads the message.
6. Do not work around the policy rejection of Apple's external notarization
   upload.

## Open items and owners

| Item | Owner | Completion evidence |
| --- | --- | --- |
| Open a safe exact-revision staging cutover window | Admin/release task | Explicit coordination notice after green CI/canary and before host mutation. |
| Generate fresh Victoria invite and hash-only server descriptor | Codex in this task | Private client JSON mode `0600`; sanitized descriptor handed to Admin without printing values. |
| Merge only Victoria descriptor and recreate app under lock | Admin/release task | Backup, preserved participant count/volumes, exact build/ready evidence and successful Kjetil `doctor`. |
| Transfer invite separately | Kjetil | Victoria confirms receipt through the agreed trusted channel; file is deleted after use. |
| Submit request from M4 and issue proof | Victoria/Kjetil | `pending_approval`, explicit approval receipt, then green `activate` and `doctor`. |
| Verify first authenticated message | Victoria/Kjetil/Codex | Sender `victoria-lille-robot`; list/read/ack/send behavior limited to four operations. |
| Produce notarized replacement | Kjetil in an allowed Apple notarization workflow | `Accepted`, stapler validation, Gatekeeper accepted, regenerated final SHA-256. |

## Handoff condition

The test candidate may be sent now. The invitation must wait for the coordinated
staging activation. No statement that Apple accepted the package or that
Victoria has access is warranted yet.
