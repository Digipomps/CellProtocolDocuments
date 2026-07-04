# Chapter 25 — SecretCredentialCell

Status: draft Cell contract.

Last updated: 2026-06-18.

`SecretCredentialCell` is the entity-scoped credential boundary for HAVEN. It
stores or references provider credentials without exposing raw secrets to
scaffolds, prompts, skeletons, logs, Book docs, Git, or ordinary Cell state.

The short answer to the storage question is: yes, use a private credential
vault, with platform secret storage as the root of trust. For the Mac/Apple
path, the recommended durable shape is a ChaChaPoly-encrypted vault envelope
with the wrapping material stored in Keychain or an equivalent OS secret store.

Important implementation note: this Cell should not duplicate the credential
work already present in the codebase. Treat `SecretCredentialCell` as the
policy, authorization and provider-invocation surface over existing primitives:

- `CredentialVaultService` for metadata + secret handle lifecycle;
- `SecureCredentialStore` for raw secret storage abstraction;
- `AppleKeychainSecureCredentialStore` for Apple Keychain-backed storage;
- `IdentityVault`/`ScopedSecretProviderProtocol` for scoped secret material;
- `ScopedCredentialCell` as an existing CellScaffold UI/session surface whose
  current v1 behavior is `session_only_redacted`, not a durable vault.

Do not use Secure Enclave as a blanket answer for this Cell. Secure Enclave is
excellent for certain private-key operations, but model-provider API keys are
shared secrets and ChaChaPoly is symmetric encryption. The correct first step
is Keychain-backed secret material plus AEAD-encrypted credential envelopes,
with CellProtocol controlling who may use a credential.

Apple references:

- <https://developer.apple.com/documentation/cryptokit/chachapoly>
- <https://developer.apple.com/documentation/security/keychain-services>
- <https://developer.apple.com/documentation/security/keychain-items>

## 1. Responsibility

`SecretCredentialCell` owns credential storage, metadata, policy and audit for
provider/API credentials attached to an entity-controlled identity.

It does not make a credential globally readable.

It does not make an external provider GDPR-approved.

It does not make a model action safe.

It answers one narrower question:

Can this requester, for this purpose and data class, use this credential or
provider route right now?

## 2. Endpoint

Canonical endpoint:

`cell:///entity/credentials`

Suggested local AgentD route:

`credentials`

Flow topic:

`entity.credentials`

## 3. Protected Resource

Protected resources:

- raw API keys;
- OAuth refresh/access tokens;
- external login provider account links, for example a Featherless account
  authenticated through Hugging Face;
- short-lived provider session tokens;
- bring-your-own-key provider settings;
- provider spend limits;
- credential-to-purpose policy;
- DPA/GDPR approval metadata;
- audit records that could reveal provider use patterns.

Public read models must be metadata-only and must never include raw secret
material.

## 4. Storage Architecture

Use a two-layer model:

```text
SecretCredentialCell state
  - credential metadata
  - policy
  - audit digests
  - encrypted vault envelope reference

Private credential vault
  - ChaChaPoly encrypted secret payload
  - nonce/tag/ciphertext
  - key version
  - credential id

Platform secret store
  - Keychain / equivalent stores wrapping key or per-credential data key
```

Recommended Apple MVP:

1. Generate a random per-credential data encryption key.
2. Store that data key in Keychain under an access-controlled service/account
   pair, or store a vault wrapping key in Keychain and wrap the per-credential
   data key.
3. Encrypt the provider secret payload with `ChaChaPoly.seal`.
4. Store the sealed box in a private vault file under the entity/AgentD state
   root.
5. Store only `secretRef`, metadata, policy and audit digests in Cell state.

Acceptable simpler Apple MVP:

- Store the raw provider API key directly as a Keychain generic-password item.
- Store only a Keychain item reference and metadata in Cell state.

The encrypted-vault envelope is preferred because it gives HAVEN a portable
credential record, explicit key versions, backup/restore semantics, and a
natural place for audit metadata. Direct Keychain storage is simpler, but less
portable across HAVEN runtimes.

Non-Apple equivalent:

- Linux desktop: Secret Service/libsecret or a configured local secret service;
- server: cloud KMS/secret manager or an operator-controlled encrypted secret
  store;
- Android: Android Keystore-backed wrapping key;
- Windows: DPAPI/Credential Manager;
- development-only fallback: encrypted local file with an operator-supplied
  passphrase, never a plaintext file.

## 5. Public Keypaths

Readable metadata keys:

| Keypath | Returns | Secret exposure |
| --- | --- | --- |
| `credentials.state` | cell health, storage backend, counts, policy version | none |
| `credentials.list` | credential summaries | no raw secret, no prompt |
| `credentials.describe` | one credential metadata object | no raw secret |
| `credentials.policy` | allowed providers, data classes, spend caps | none |
| `credentials.audit` | bounded audit digest page | hashes/previews only |
| `providers.allowed` | provider/model routes available to requester | none |

Writable/action keys:

| Keypath | Purpose |
| --- | --- |
| `credential.register` | add a new credential from a user/operator-provided secret |
| `credential.rotate` | replace secret material and record old key as retired |
| `credential.revoke` | disable use without deleting audit metadata |
| `credential.delete` | delete encrypted secret and metadata when retention allows |
| `credential.test` | run a minimal provider health test without exposing the key |
| `credential.authorizeUse` | return an invocation authorization, not the raw secret |
| `provider.invoke` | optional trusted proxy invocation inside the same local boundary |

`credential.reveal` should not exist in the stable contract. If a local operator
needs emergency reveal, make it a separate admin-only recovery tool outside the
normal scaffold/Cell path and require explicit local confirmation.

## 6. Register Payload

`credential.register` accepts:

```json
{
  "providerID": "featherless",
  "credentialLabel": "Featherless test key",
  "secret": "<operator supplied once>",
  "secretKind": "api_key",
  "ownerIdentityDomain": "domain:personal:ai",
  "allowedPurposeRefs": [
    "purpose://conference.co-pilot.model-evaluation"
  ],
  "allowedScaffolds": [
    "CellScaffold",
    "Binding",
    "Porthole",
    "HAVENAgentD"
  ],
  "allowedDataClasses": [
    "public",
    "synthetic",
    "internal_non_sensitive"
  ],
  "blockedDataClasses": [
    "private_contact_info",
    "sponsor_leads_without_consent",
    "health",
    "payment",
    "children"
  ],
  "maxMonthlySpendNOK": 500,
  "requiresUserApproval": true,
  "rotationDays": 90,
  "dpaStatus": "unknown"
}
```

The `secret` field is accepted only on the write/action path. It must not be
echoed in the response, audit log, flow event, result file or error.

Return:

```json
{
  "status": "registered",
  "credentialID": "cred.featherless.primary",
  "providerID": "featherless",
  "secretRef": "secret://entity/provider/featherless/api-key",
  "storageBackend": "keychain-wrapped-chachapoly-vault",
  "policyVersion": 1
}
```

## 7. Authorize Use Payload

`credential.authorizeUse` accepts:

```json
{
  "credentialID": "cred.featherless.primary",
  "providerID": "featherless",
  "modelID": "Qwen/Qwen3-8B",
  "purposeRef": "purpose://conference.co-pilot.model-evaluation",
  "scaffoldID": "CellScaffold",
  "dataClass": "synthetic",
  "estimatedInputTokens": 1200,
  "estimatedOutputTokens": 300,
  "requiresNetwork": true,
  "correlationID": "eval-2026-06-17-001"
}
```

Return on allowed:

```json
{
  "status": "authorized",
  "authorizationID": "cred-auth.20260617.001",
  "credentialID": "cred.featherless.primary",
  "providerID": "featherless",
  "modelID": "Qwen/Qwen3-8B",
  "expiresAt": "2026-06-17T12:15:00Z",
  "maxUses": 1,
  "mustInvokeInsideBoundary": true
}
```

This response is not a bearer token for arbitrary clients. It is a short-lived
local authorization that a trusted provider invocation cell or HAVENAgentD
route can consume. It must not contain the API key.

Return on denied:

```json
{
  "status": "denied",
  "reason": "dataClassBlocked",
  "credentialID": "cred.featherless.primary",
  "dataClass": "private_contact_info",
  "requiredAction": "Use local AgentD model or create an Agreement/DPA-approved route."
}
```

## 8. Provider Invoke Payload

`provider.invoke` is optional but useful for the first implementation because
it keeps the key and network request inside the same trusted boundary.

It accepts a prompt manifest, not arbitrary hidden state:

```json
{
  "providerID": "nanogpt",
  "modelID": "openai/gpt-4.1-mini",
  "credentialID": "cred.nanogpt.primary",
  "purposeRef": "purpose://conference.co-pilot.model-evaluation",
  "scaffoldID": "CellScaffold",
  "dataClass": "synthetic",
  "promptManifest": {
    "promptHash": "sha256:...",
    "containsPII": false,
    "sources": [
      "Tools/CoPilotChatLanguageBenchmark/cases.no.jsonl"
    ],
    "redactionPolicy": "none-needed"
  },
  "request": {
    "messages": [
      {
        "role": "user",
        "content": "..."
      }
    ],
    "temperature": 0,
    "maxTokens": 300
  },
  "correlationID": "model-eval-001"
}
```

The audit record should include prompt and response hashes, token counts and
cost estimate. It should not include full prompt/response by default when
personal data could be present.

## 9. Flow Events

Emit `FlowElement`s on `entity.credentials` for:

- `credential.registered`
- `credential.rotated`
- `credential.revoked`
- `credential.deleted`
- `credential.tested`
- `credential.use.authorized`
- `credential.use.denied`
- `provider.invocation.completed`
- `provider.invocation.failed`

Flow payloads must never include raw secrets. For provider invocation events,
include hashes and short safe previews only when the data class allows it.

## 10. Denial Rules

Deny credential use when:

- requester lacks Agreement/capability;
- purpose ref is not allowed;
- scaffold is not allowed;
- data class is blocked;
- provider DPA/GDPR status is insufficient for the data class;
- spend cap is exceeded;
- key is revoked/expired;
- requested model violates license/policy;
- prompt manifest is missing for external provider calls;
- user approval is required but missing.

Denial is not an error state. It is a normal policy result and should be
visible enough that the UI can explain what safer route is available.

## 11. Minimal Explore Contract

Machine-readable seed:

`Book/secret_credential_cell_contract_v0.json`

The implementation should register complete Explore contracts for every public
get/set key before skeletons or agents rely on this Cell.

## 12. Implementation Placement

Recommended first implementation target:

- `Binding/HavenAgentD`, because it already has `AgentLocalModelCell`,
  loopback bridge, local identity, local state root and operator context.

Shared portable contract:

- document here in `CellProtocolDocuments`;
- later promote protocol-neutral structs/tests into `CellProtocol` if more
  than AgentD needs to host the Cell directly.

Do not put raw credentials in `CellProtocolDocuments`.

## 13. Tests Required

Minimum tests:

1. Register credential returns metadata and no secret.
2. List/describe/audit never returns the raw secret.
3. Allowed purpose/data class returns authorized use.
4. Blocked data class returns denied result.
5. Revoked credential cannot be used.
6. Rotation invalidates old key version.
7. Provider invoke does not log prompt/response when data class blocks logging.
8. Missing Agreement/capability is denied.
9. Wrong identity domain is denied.
10. Corrupt vault envelope fails closed.

## 14. Residual Assumptions

- Keychain or equivalent platform secret store is trusted to protect wrapping
  material on the local device.
- The local operator can still compromise their own device; this Cell reduces
  accidental and cross-scaffold leakage, not all local compromise risk.
- External providers remain separate GDPR/subprocessor decisions. A credential
  being present does not mean the provider may receive personal data.
