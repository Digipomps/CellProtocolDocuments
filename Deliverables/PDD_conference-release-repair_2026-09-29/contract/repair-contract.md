# Repair contract — 2026-09-29

Last verified against source, not an executed release.

## Admin transport
Input: an existing permitted admin endpoint, unchanged HMAC credential and requester.
The transport must finish only after the WebSocket is delivered and inbound handlers are installed.
Timeout/cancellation must release the wait and close a late connection without installing it.
HMAC upgrade is workload admission only; target CellProtocol identity/agreement checks remain authoritative.
A 101 result is not proof that Admin Workbench can read its required cells.

## ProjectPortfolio selection
Existing scalar ID and id/projectID objects remain valid. Skeleton activation/selection envelopes accept interacted before selected, then value, with the existing string/object ID decoder. Unknown IDs return the existing error and retain the prior selection. Existing rw-- authorization and owner boundary remain in force.

## Developer Workbench history
A stable built-in configuration UUID resolves against a newly constructed catalog. An explicit unknown UUID must still fail even if name and endpoint match. The UUID is configuration identity, not a user/project identity or access grant. No new keypaths, UI sections or privileges.

## Checks written, not executed
AdminAuthenticatedVaporBridgeTransportTests: four upgrade lifecycle cases.
ProjectPortfolioCellTests: selection/activation, legacy IDs, malformed and unknown IDs.
HavenWorkbenchConfigurationTests: fresh-catalog back lookup plus unknown-UUID rejection.
Swift compilation/execution is blocked by the capacity guard (exit 75).
