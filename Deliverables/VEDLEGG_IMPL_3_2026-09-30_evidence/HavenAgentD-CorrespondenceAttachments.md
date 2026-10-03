# Correspondence MCP attachments

Candidate implementation. Rebuild with its paired CellProtocol revision before
using the new tools. Existing signed four-action profiles continue to work for
messages and are denied attachment operations. Provision an explicitly signed
`CorrespondenceAgreementTemplates.withAttachments` contract; do not edit grants
inside an already signed profile.

The client uses `CorrespondenceEnvelopeClient`, the existing Bridge/Resolver
transport and the relationship's agreement. It does not send private file bytes
through model text, HTTP upload routes or a separate authority system.

## Tool surface and authority limits

All tools require the selected `relationshipID`.

| Tool | Purpose | Does **not** authorize |
| --- | --- | --- |
| `correspondence_list_inbox` | Envelope listing | Reading bodies, downloading, acknowledging, sending or execution. |
| `correspondence_read_message` | Deliberate local decryption; signed attachment display if present | Attachment byte fetch, receipt, ownership transfer, export or execution. |
| `correspondence_send_message` | Encrypted text | Implicit attachment, local machine actions or execution. |
| `correspondence_ack_message` | Existing message receipt bit | File receipt, fetch or ownership transfer. |
| `correspondence_send_attachment` | Message with exactly one local `filePath` or registered `sourceID` | Caller mode choice, deleting the original, transferring ownership, installing/opening/running. |
| `correspondence_attachment_metadata` | Signed name/type/size, mode/reason and permitted next step | Download, file receipt, permanent export or execution. No hash/key is displayed. |
| `correspondence_probe_attachment_source` | Recipient tests an explicitly shared source reference without reading file contents | Fetching bytes, sending, minting grants or transfer. |
| `correspondence_fetch_attachment` | Explicit verified managed download; for reference mode, return the already accessible reference with zero bytes copied | New permanent ownership, export, opening or execution. |
| `correspondence_revoke_attachment` | Sender revokes its managed delivery | Deleting an external original, user-made copy or transferred file. |
| `correspondence_transfer_attachment` | Separate, named sender offer after verified fetch in copy mode | Recipient acceptance, implicit execution or silent consent without owner policy. |
| `correspondence_accept_attachment_transfer` | Recipient accepts offer and atomically exports to `destinationPath` | Overwriting a destination, installation or execution. |

Unknown arguments are rejected. There is no `mode`, `deleteOriginal` or arbitrary
server file-path argument. A local file path explicitly selects that client's
file; a source ID selects a file already provisioned inside its sender Cell.

## Mode rule

- `reference`: retained registered source + explicit shared file reference +
  recent actual recipient readability probe. The existing path is returned;
  no attachment stream or downloaded copy is created.
- `fetchOnDemand`: source remains in sender Cell but shared-reference reachability
  is unavailable, unknown or stale. Stream starts on recipient fetch.
- `copy`: local file outside the source catalog, or host-provisioned nonretaining
  source policy. Encrypted chunks are imported into the sender-owned Cell.

The reference adapter currently supports file/shared-volume URLs. It does not
pretend to support arbitrary web/cloud/Cell reference providers. A shared path
must mean the same source on both ends. Shared source readability does not grant
rights the recipient did not already hold.

## Ownership cost and policy

`AttachmentDisplay.ownershipTransferAvailable` is false in reference and
fetch-on-demand, and those modes have no transfer consequence prompt. Copy
metadata shows the exact confirmation text. Owner offer requires it, unless the
owner has explicitly set local profile `attachmentTransferPolicy` to that same
text. Policy supplies the answer to the named tool, not an automatic transfer on
send/read/download.

The cost is explicit: the sender loses revocation, and the recipient's owned
file no longer expires with the message. The recipient must already have fetched
and verified it and must accept the offer. Sender-managed ciphertext is then
removed; the external original is untouched. `destinationPath` never overwrites.

Downloads use a private managed cache under the correspondence profile, with a
per-profile process lock. Interrupted downloads keep no final-named partial.
Startup cleans orphan partials only after acquiring that lock. Timers and startup
sweeps apply message expiry. Committed transferred files are exempt. An ambiguous
acceptance response leaves a recorded, unresolved transfer intent quarantined;
explicit retry reconciles the server record. Such an error is not success.

## Build/test pairing and deployment boundary

During branch review, use:

```sh
export CLANG_MODULE_CACHE_PATH=/private/tmp/haven-attachments-review-modulecache
export SWIFTPM_MODULECACHE_OVERRIDE="$CLANG_MODULE_CACHE_PATH"
export HAVEN_ATTACHMENT_CELLPROTOCOL_PATH=/absolute/path/to/paired/CellProtocol
mkdir -p "$CLANG_MODULE_CACHE_PATH"
swift test --disable-sandbox
```

The environment override selects the paired local package under the explicit
package name `CellProtocol`; no deployed profile is modified. The package job
must publish/pin the paired revision and provision signed attachment agreements
and sender storage. Existing text-only deployments cannot serve these actions.
No operative correspondence is sent by this implementation task.

Protocol details and failure/lifetime limits are in CellProtocol's
`Docs/CorrespondenceAttachments.md`. Book follow-up: 04, 05, 08 and 21; the Book
is not edited here.
