# Minimal fixes for administrator import

Read-only plan, 2026-09-18. No source/Git/host changes or tests were run by the auditor. Source baseline is the session-recovery worktree at `7ddae1a0` plus its dirty manifest; root is importing it into the recovery candidate. Existing owner proof, signed Contract, staging environment, RP, revision, identity binding and four-action restrictions remain intact.

## 1. Project representative status for the actual user

File: `Sources/App/Controllers/PortholeWebSessionSupport.swift`, `attachedReferenceRequester`.

Add `if target is ScaffoldMandateCell { return requester }` alongside the existing `WorkbenchAccessGrantCell`/chat special cases, before the generic `GeneralCell` branch. No change to `referenceResolutionRequester`: resolving the scaffold-unique Cell may need the scaffold owner as lookup identity, but inspecting `representative.status` must use the authenticated web requester. `ownerRequester` itself is already identity-preserving and must not be rewritten.

This repairs the fallback path in `bootstrapValueInRequestScope`: an unattached reference uses `referenceResolutionRequester`, which resolves a scaffold-unique target with its owner. Without the special case the subsequent successful status projection is for that owner; the later redaction pass only removes denied fields, not a successful wrong-principal status.

Test through production `PortholeWebSessionSupport.bootstrapValue`, not just the new helper: configure distinct scaffold owner, authorized browser representative, and unrelated requester. Leave the mandate reference unattached so fallback inspection is required. Verify representative status is `authorized` for the representative, `not_authorized` with empty actions for the stranger, and is not copied from the owner. Repeat with the reference attached. Use an isolated real runtime and signed representative Contract, with the same private/public boundaries as existing provisioner tests. The full projection must not contain the representative's credentials, Fido ID or identity proof payload.

## 2. Render unavailable when the mandate endpoint is absent

Files: the same Porthole bootstrap method, the admin factory status binding, and optionally the status helper in `ScaffoldMandateCell` for a common shape.

Immediately before `stateObject[reference.label] = .object(cellState)`, for the exact local `ScaffoldMandateContract.endpoint` and label `scaffoldAdministrator` only, check whether a well-shaped `representative.status` projection was obtained. If not, write a nested presentation value at `representative.status` using the existing Object setter:

```text
status: unavailable
authorized: false
authorizationSource: none
authorityActions: []
administratorEntityRef: null
validUntil: null
statusLabel: Ikke tilgjengelig
```

Keep any `connected=false` diagnostic and existing access-requirement diagnostics. Do not synthesize an authorized record, create a mandate Cell, register an absent resolver mapping, grant access, or overwrite a valid returned status. Read failures/denial should also produce unavailable presentation rather than preserving a stale authorized status. Populate `statusLabel` for the successful existing status codes too (`authorized`, `not_authorized`, `not_provisioned`) if the factory binds the new label. Otherwise keep the existing stable `status` field and ensure the renderer visibly exposes its unavailable value.

Do not add `ScaffoldMandate` to a broad utility/owner-authority bypass list. The fix is a display projection for this one known local reference. Do not apply it to arbitrary remote Cells or merely matching names.

Test a require-existing runtime with no admin resolves/mappings: bootstrap the Product Administration configuration; assert `unavailable`, `authorized=false`, empty actions and visible text; compare resolver mappings before/after to prove no implicit provisioning. Existing `testRequireExistingAcceptsAbsentPairButRejectsPartialMapping` continues to require ready for an absent pair and unavailable readiness for a partial pair. Also cover a reachable but unregistered registry returning the Cell's existing `not_provisioned` status, which must not be overwritten by the fallback.

## 3. Reject corrupted authority before any mutation

Files: `ScaffoldAdministratorProvisioner.swift` and a narrow strict-read helper in `ScaffoldMandateProofSupport.swift` (or the provisioner itself).

Current problem: `let existing = try? await ...storedRepresentativeAgreement` conflates absent, malformed and unreadable proof. Merely changing this outer `try?` is insufficient: `EntityAnchorProofSupport.storedValue` catches any first read error and tries local-vault fallback. Do not alter that shared helper globally as part of this small repair.

Add a strict existing-authority reader for this operator path:

1. Resolve the representative's real EntityAnchor using the existing resolver and authenticated representative; successfully read its `proofs` root and require an Object. A storage/authorization failure is an error, not proof of absence.
2. Inspect `scaffold.issuerAuthority` in that root. Where historical local fallback storage is supported, also inspect `identity.proofs.scaffold.issuerAuthority` and `proofs.scaffold.issuerAuthority` in `representative.properties`. Use Object keypath lookup with an explicit catch for `KeyPathError.notFound` only. Treat `typeMismatch`, invalid paths, `.null`, unexpected scalar/list shapes and other errors as corruption. Do not use `try?` for these checks.
3. Decode every present candidate as Contract. Any decode failure is `authorityConflict`. If multiple storage locations contain authorities, require canonical decoded Contract equality; a conflicting copy is a conflict, not permission to select whichever grants rights. Return nil only when the successfully read backing state and all supported local locations prove absence.
4. Keep the current full `verifyRepresentative` checks for existing decoded Contracts: owner, subject, registration-receipt domain, actions and validity. Existing expired or mismatched authority remains a conflict. Do not renew or repair automatically.

Call the strict reader **before** the first registry `.register` at present line 159. Today authority reading happens around line 190, after the registry may have changed. If an existing authority is present but the registry is unregistered, reject the inconsistent pre-existing state before registering anything; otherwise validate against the existing registry context before writes. Only a proven-absent authority may enter the current new-authority creation path.

Tests in `ScaffoldAdministratorProvisionerTests`: seed malformed primary authority (`.string`, `.null`, malformed Contract Object), malformed legacy property authority, conflicting primary/local Contracts and a storage-denied/unreadable source. Invoke the provisioner; expect `authorityConflict`, unchanged registry registration/history and unchanged persisted proof bytes after cold vault reload. Retain the positive first provisioning and idempotent reload test. Add expired/wrong-domain existing Contract controls to ensure parsed invalid authority is not silently replaced. A real read failure is never an empty-authority fixture.

The existing registry uses public organization references; private identity fields remain outside its public read model. No new grants are introduced by strict reading.

## 4. Bound stdin before materializing all input

Files: `ScaffoldAdministratorProvisioner.swift`, `Sources/Run/main.swift`, provisioner tests.

Expose a small `public static func readRequestData(from handle: FileHandle) throws -> Data` on the provisioner so Run can use it. Reuse its existing 32 KiB limit. Read in a loop using `read(upToCount:)`, accumulating at most 32,769 bytes (limit+1); each requested chunk is bounded by the remaining allowance, e.g. `min(4096, maximumInputBytes + 1 - data.count)`. Stop at nil/empty EOF. Throw `inputTooLarge` immediately when count exceeds 32,768. Propagate I/O errors. Keep `decodeAndValidate`'s existing second size/schema check.

Replace `FileHandle.standardInput.readDataToEndOfFile()` with this helper. Prefer reading bounded input before `configure(app)` for an enabled one-shot command, so an oversized input cannot start provisioning setup before it is rejected. Do not read stdin during a normal service start. All existing staging/provision-only validation must still run before authority mutation; bounded reading itself confers no authority.

Test using real temporary files/FileHandles: exactly 32,768 bytes returned; 32,769 bytes rejected; a much larger file rejected with handle offset at most 32,769; empty bytes pass to the existing schema validator and become invalidRequest. If testing pipes, use a concurrent writer so the test does not block writing more than pipe capacity before the reader starts. Do not weaken production validation to make tests inject a smaller bound.

## 5. Disarm rollback before destroying rollback material

File: `scripts/provision-scaffold-administrator-staging.sh`.

Add `COMMITTED=0` next to the existing transaction flags. The exit handler may stop/restore the service only when `status != 0`, `SERVICE_STOPPED == 1`, **and `COMMITTED == 0`**. A nonzero result after commit must report a cleanup/output failure without stopping or restoring the healthy service.

Split the final Docker helper into phases:

1. After both ready/revision checks, persist the verified operator receipt with private permissions while the backup still exists. Do not delete the backup in that helper. Record backup disposition honestly as pending cleanup, not already deleted.
2. Once receipt persistence succeeds, set `COMMITTED=1`. This is the point after which trap rollback is forbidden.
3. Delete the archive/checksum in a separate cleanup operation. On success update the receipt's backup disposition to deleted. On failure retain/report pending or failed cleanup; never roll back committed authority or stop the service. Failure to print the final receipt must likewise leave the service running.

Keep the exit handler's temporary-secret-directory cleanup. Diagnostic printing inside a trap should not itself bypass cleanup (use best-effort stderr output). Preserve the fixed staging container, environment/RP checks, immutable image and revision checks, private request file, deploy lock, checksum verification before destructive restore, network isolation and current readiness/restart verification. Do not expose configurable production data paths merely to simplify tests.

Failure-injection test matrix for the actual script with mocked Docker/curl commands in a disposable harness (no real Docker socket or host service): provisioning failure, invalid receipt, first-start failure, second-restart failure and receipt-write failure all restore from intact backup; backup deletion failure and final-output failure after commit never invoke stop/restore; normal success deletes backup only after verified restarts and durable receipt. Assert event order and resulting service state, not just source text. The fixed deploy-lock path can be substituted once in a temporary script copy inside the test harness; production script/environment restrictions remain unchanged. A checksum failure must stop before the restore helper's deletion command.

The README currently claims the caller request file is deleted, while the script preserves it. Correct the retention description; do not add inferred deletion of a caller-supplied file. The one-shot remains staging-only and is separate from ordinary production image deployment.

## Focused verification order for root

Run the direct requester/fallback bootstrap regressions; strict corrupt-authority plus idempotent provisioner tests; bounded-reader tests; then the mocked script failure matrix. Retain registry absent/partial readiness, mandate positive/negative/threshold fixtures, and role-is-not-authority coverage. Use the repository's bounded test runner. No success or runtime safety claim is made here until these checks execute against the integrated candidate.
