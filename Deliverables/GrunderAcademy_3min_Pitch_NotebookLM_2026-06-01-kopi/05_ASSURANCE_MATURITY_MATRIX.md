# Assurance maturity matrix

Status labels:

- `specified`: documented enough for implementation.
- `implemented`: exists in code.
- `tested`: has targeted tests.
- `pilot-ready`: ready for limited non-real-money or controlled-money pilot.
- `deferred`: intentionally not v0.

| Area | Current status | Next gate |
|---|---|---|
| Domain-scoped identity | implemented | Verify for pilot domain |
| Explicit contracts/capabilities | implemented | Wire to ProofDoor/AI paths |
| PaymentGate access flow | implemented | Route tests and ledger-source boundary |
| PaymentProofDoor VC proof | implemented | consumed-set, TTL, wrong subject/resource/issuer tests |
| TrustedIssuerCell | implemented in CellProtocol | register and seed payment-context policy in runtime |
| DiMyMint three-ledger model | specified/partly implemented | issue-from-reservation and ledger-wrapped redeem tests |
| DiMyMint wallet reservation/release | implemented/tested | idempotency and Postgres integration coverage |
| Real PSP top-up | partly implemented | real signature verification and no placeholder session URL |
| AI entitlement tiers | specified here | implement tier resolver and tests |
| Usage metering | specified here | implement schema/ingestion/idempotency |
| Audit export | specified here | deterministic manifest and checksum |
| ContributionProof | specified here | simulator/fixtures first |
| ValuePoolPolicy | specified here | deterministic simulator first |
| Runtime ValuePoolCell | deferred | wait for simulator and ledger truth |
| Transferable tokens | deferred | legal classification required |
| Cash-out | deferred | legal/licensing route required |
| Global reputation | forbidden | keep context-local only |

## Pilot readiness checklist

ProofDoor/AI pilot is not pilot-ready until:

- DiMyMint or equivalent ledger truth can explain funded, reserved, issued, redeemed and outstanding value.
- Payment proof consumed-set exists.
- TrustedIssuer payment-context policy is configured.
- Usage events are idempotent.
- Audit export is deterministic and excludes secrets.
- Regulatory matrix classifies the variant as access entitlement/usage quota, not money-like value.

## Review cadence

Update this matrix after every implementation slice. Never let public copy claim a maturity level higher than this table.
