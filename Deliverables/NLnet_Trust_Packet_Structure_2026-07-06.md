# NLnet Trust Packet Structure

Date: 2026-07-06

Status: working structure for an NLnet application evidence attachment.

Human decision owner: Kjetil.

Prepared with advisory-panel method from `Book/30_Panel_Task_Decomposition_Workflow.md`.

## Decision

Use a concise trust/evidence packet as an attachment to an NLnet proposal.

The packet should not be the proposal itself. The proposal form must stay
self-contained, short, concrete, and focused on what will be built and how. The
packet should only document the evidence behind the proposal: claims, maturity,
source grounding, risk boundaries, and verification status.

Preferred public-facing name:

`HAVEN / CellProtocol Evidence Packet for NLnet`

Avoid using the packet as a reputation signal. It should prove provenance and
claim discipline, not say that a person, team, or project is globally
"trustworthy".

## Source Basis

External programme sources checked on 2026-07-06:

- NLnet proposal form: <https://nlnet.nl/propose/>
- NGI TALER main page: <https://nlnet.nl/taler/>
- NGI TALER eligibility: <https://nlnet.nl/taler/eligibility/>
- NGI TALER guide for applicants: <https://nlnet.nl/taler/guideforapplicants/>
- NGI Fediversity main page: <https://nlnet.nl/fediversity/>
- NGI Fediversity eligibility: <https://nlnet.nl/fediversity/eligibility/>
- NGI Fediversity guide for applicants:
  <https://nlnet.nl/fediversity/guideforapplicants/>
- NLnet GenAI policy: <https://nlnet.nl/foundation/policies/generativeAI/>

Local HAVEN / CellProtocol sources inspected:

- `Book/01_CellProtocol_Core.md`
- `Book/03_Identity_Model.md`
- `Book/04_Agreements_Contracts.md`
- `Book/08_Bridging_Transport.md`
- `Book/21_Contact_Endpoint_Cell.md`
- `Deliverables/DevPlatform_Hetzner_CoPilot_Plan_2026-06-11.md`
- `CellScaffold/Sources/App/Cells/TrustPacket/TrustPacketWorkbenchCell.swift`
- `CellScaffold/Sources/App/Cells/TrustPacket/TrustPacketConfigurationFactory.swift`
- `CellScaffold/Tests/AppTests/TrustPacketConfigurationFactoryTests.swift`
- `CellScaffold/Sources/App/configure.swift`
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md`
- `DiMyDocuments/ValueRedistribution/02_PRODUCT_VARIANT_AND_REGULATORY_MATRIX.md`
- `DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md`

## Formaal And Goals

| Formaal | purposeRef | Goal | Status |
| --- | --- | --- | --- |
| Make the NLnet application more verifiable without making it bloated. | `purpose://project-work.share-selected-intent` | A 3-5 page attachment structure exists, with each section tied to a factual purpose and evidence source. | satisfied |
| Keep public claims defensible. | `purpose://source.methodology.current` | Load-bearing claims are classified as supported, partial, or open, with caveats where needed. | satisfied |
| Avoid payment/regulatory overclaim in TALER framing. | `purpose://access.audit.privacy` | TALER-related framing stays in access entitlement / proof / integration territory and avoids wallet, token, cash-out, or general payment-rail claims. | satisfied |

## NLnet Constraints That Shape The Packet

1. Current deadline is 2026-08-01 12:00 CEST, and NLnet is temporarily only
   accepting NGI TALER and NGI Fediversity proposals.
2. The application form asks for short, concrete answers, focused on what and
   how. Longer descriptions may be attachments, but the proposal must remain
   self-contained.
3. Attachments can include detailed task descriptions, budget justification,
   and endorsements, but NLnet explicitly says not to waste too much time on
   them.
4. Both TALER and Fediversity eligibility pages accept activities such as FOSS
   design/development, validation, software quality work, security/testing/CI,
   documentation, usability, standardisation, deployability and packaging, if
   linked clearly to the call.
5. The applicant guides emphasize value for money, strategic potential, and a
   maximum single-proposal request of 50 kEUR.
6. GenAI use in application preparation must be disclosed with a prompt
   provenance log.

Implication: the packet should be short, auditable and directly useful to
reviewers. It should not become a second application, a manifesto, or a broad
HAVEN story.

## Recommended Packet Structure

Target length: 3-5 pages, excluding optional appendices.

### 1. One-Paragraph Project Boundary

State which proposal this packet supports.

Recommended primary version:

> This evidence packet supports a Fediversity proposal for making a minimal
> CellProtocol runtime reproducibly self-hostable and verifiable, with
> domain-scoped identity, explicit capability contracts, replayable audit, and
> a small TrustPacket/ContactEndpoint demonstration.

Recommended TALER-specific version:

> This evidence packet supports a TALER proposal for integrating GNU Taler
> payment confirmation with CellProtocol access-entitlement proofs. Taler
> handles payment; CellProtocol records purpose-bound access, receipt,
> provenance and audit.

Do not combine these two unless the proposal itself is explicitly split into
separate work packages with separate outcomes. The cleaner route is one packet
per proposal.

### 2. Claim Map

Use a table with four columns:

| Claim | Evidence | Maturity | Caveat |
| --- | --- | --- | --- |
| CellProtocol is designed around deterministic events, explicit capability contracts, domain-scoped identity, replay and audit. | `Book/01`, `Book/03`, `Book/04` | documented / implemented foundation | Does not by itself prove production readiness for every runtime. |
| HAVEN has a TrustPacket workbench surface that makes draft, boundaries, receipt, signature, purpose candidates and actions visible. | `TrustPacketConfigurationFactory.swift`; `TrustPacketWorkbenchCell.swift` | implemented in CellScaffold | Current turn did not rerun live Porthole smoke. |
| TrustPacket actions are consent-gated and avoid global reputation/personscore language. | `TrustPacketConfigurationFactoryTests.swift` | tested in current focused run | Rerun before final submission if code changes. |
| Fediversity alignment is strongest when framed as reproducible deployability, service portability and user-owned runtime operation. | NLnet Fediversity page and eligibility | supported by external source | Current HAVEN deployment docs are Docker/Hetzner-first; NixOS packaging must be an actual deliverable. |
| TALER alignment is plausible only if the work integrates GNU Taler or its ecosystem directly. | NLnet TALER page and eligibility | supported by external source | Internal DiMy micropayment/value language is not enough and should be excluded from the TALER pitch. |

### 3. Maturity Snapshot

Use conservative labels:

| Area | Current status | Use in application |
| --- | --- | --- |
| Domain-scoped identity | implemented | Safe as foundation claim. |
| Explicit contracts/capabilities | implemented | Safe as foundation claim. |
| Replay/audit model | documented / implemented foundation | Safe with implementation-specific caveat. |
| TrustPacket workbench | implemented in CellScaffold | Safe as demonstrator claim, with current-verification caveat. |
| TrustPacket GUI tests | current focused run passed | Safe with caveat that live Porthole smoke was not rerun in this pass. |
| Fediversity/NixOS packaging | not currently established as deliverable | Proposal work item, not current capability. |
| TALER integration | not established in inspected sources | Proposal work item, not current capability. |
| Payment/value redistribution | research and pilot direction | Do not use as a TALER core claim. |
| Wallet, cash-out, transferable token, global reputation | forbidden/deferred | Exclude. |

### 4. Argument Chain For The Chosen Programme

#### Fediversity Primary Argument

Root claim:

> CellProtocol is a plausible Fediversity proposal foundation if the requested
> work is framed as reproducible self-hosting, service portability, and
> verifiable user-owned runtime operation.

Support:

- Fediversity explicitly focuses on a hosting stack with service portability,
  personal freedom, NixOS, reproducibility, secure operation and easier
  deployment.
- CellProtocol documentation defines transport-independent cells, domain-scoped
  identity, capability contracts, replay and audit.
- HAVEN already has Docker/Hetzner deployment thinking and self-hosted runtime
  work, which can be converted into a narrower reproducible packaging and
  verification proposal.

Counterargument:

- Fediversity is not a generic decentralised-app fund; a proposal that only
  says "CellProtocol is portable" is too abstract.

Resolution:

- Make NixOS/reproducible packaging, conformance tests, and a tiny
  self-hostable demo explicit deliverables.

#### TALER Secondary Argument

Root claim:

> CellProtocol is a plausible TALER proposal foundation only if the work is a
> concrete GNU Taler integration that turns a Taler payment event into a
> purpose-bound access-entitlement proof, receipt and audit trail.

Support:

- TALER eligibility includes FOSS development, adaptation to new usage areas,
  testing/CI, documentation, usability, deployability and packaging when linked
  directly to TALER.
- The TALER page explicitly invites integrations into FOSS applications and
  infrastructure components such as merchant backends.
- CellProtocol/ProofDoor style framing can keep payment and access separate:
  Taler handles payment; CellProtocol handles access proof and audit.

Counterargument:

- A general DiMy micropayments or value redistribution story is too broad and
  may create payment-regulatory ambiguity.

Resolution:

- Keep TALER scope to access entitlement, receipt verification and audit.
  Exclude wallet, transferable credits, cash-out, stored-value and investment
  language.

### 5. Risk And Boundary Register

| Risk | Packet language |
| --- | --- |
| The packet sounds like global reputation. | "TrustPacket verifies receipt payload, provenance and declared boundaries. It does not score people." |
| The TALER pitch sounds like a new payment rail. | "GNU Taler handles payment; CellProtocol handles purpose-bound access proof and audit." |
| The Fediversity pitch sounds like generic architecture. | "The funded output is a reproducible deployment package, conformance tests, documentation and a runnable demo." |
| The proposal overclaims maturity. | Use implemented/tested/specified/deferred labels. |
| NLnet dislikes attachment bloat. | Keep packet 3-5 pages and make proposal self-contained. |
| AI-assisted writing creates disclosure problem. | Maintain a prompt provenance log with model, dates, prompts and unedited outputs. |

### 6. Verification Appendix

Current verification in this pass:

```bash
cd /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold
swift test --filter TrustPacketConfigurationFactoryTests
```

Result on 2026-07-06: passed, 4 tests, 0 failures. The test run emitted two
existing SwiftPM warnings about unhandled markdown files under
`Sources/App/Cells/ConferenceMVP/Models/`; those warnings are not TrustPacket
test failures.

JSON fixture checks:

```bash
cd /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold
python3 -m json.tool playwright/skeleton-scenarios/trust-packet.preview.json
python3 -m json.tool playwright/skeleton-scenarios/trust-packet.view.json
```

Result on 2026-07-06: both JSON files parsed successfully.

If time allows, add a live Porthole/browser smoke. If it is blocked by
unrelated migrations or staging issues, report that exactly instead of hiding
it.

### 7. GenAI Provenance Note

Because this structure was created with Codex assistance, any final NLnet
proposal using this material should disclose GenAI use and keep a prompt log.

Minimum log fields:

- model/tool used
- date/time
- prompt
- unedited output or a clearly retained export of it
- human edits made afterward

## Advisory Panel Iterations

| Role | Finding | Change made |
| --- | --- | --- |
| Source auditor | NLnet wants concise, self-contained proposals and treats attachments as background. | Packet is positioned as a 3-5 page evidence attachment, not as the proposal. |
| Domain expert | Fediversity fit depends on reproducible deployability and service portability, not generic protocol enthusiasm. | Fediversity structure now requires NixOS/reproducible packaging, conformance tests and demo as deliverables. |
| Domain expert | TALER fit depends on real GNU Taler integration. | TALER structure now separates Taler payment from CellProtocol entitlement/audit. |
| Skeptic | "Trust" language can drift into person scoring. | Packet explicitly says receipt/provenance, not global reputation or personscore. |
| Claim reviewer | Payment/value claims are riskier than access-entitlement claims. | Wallet, token, cash-out, general payment rail and e-money-like claims are excluded. |
| Final adjudicator | The argument is coherent if the application chooses one programme and treats the packet as evidence. | Recommendation: Fediversity primary, TALER secondary only with concrete Taler integration. |

## Root Claim Adjudication

| Claim ID | Claim | Status | Why |
| --- | --- | --- | --- |
| C1 | A trust/evidence packet is useful for NLnet. | supported | NLnet accepts attachments for background, task detail and cost justification, while requiring the proposal itself to stay concise. |
| C2 | Fediversity is the stronger near-term programme fit. | supported with caveat | Strong alignment with self-hosting, service portability, reproducibility and deployability; caveat is that NixOS packaging must become actual work. |
| C3 | TALER is a possible but narrower fit. | partial | Strong only if there is direct GNU Taler integration; weak if framed as general DiMy micropayments or value redistribution. |
| C4 | Existing TrustPacket work can support the packet as evidence. | supported with verification caveat | Workbench, catalog and tests exist in CellScaffold; focused tests passed in this pass; live smoke was not rerun. |
| C5 | The packet can safely claim regulatory readiness. | contradicted | Internal guardrails require legal/current-source verification before money-like claims. The packet should not make this claim. |

## Final Recommended Attachment Outline

1. Project boundary and requested programme.
2. One-page claim map.
3. Maturity snapshot.
4. Programme fit argument chain.
5. Risk and boundary register.
6. Verification appendix.
7. GenAI provenance note.

Keep the packet short enough that a reviewer can read it in one sitting. The
point is to make the application feel grounded, not to force the reviewer to
learn all of HAVEN.

## Open Items Before Submission

- Choose whether the actual application is Fediversity-first or TALER-first.
- If Fediversity: define the exact NixOS/reproducible packaging deliverable.
- If TALER: define the exact GNU Taler integration point and check whether the
  GNU Taler Integration Community Hub should be contacted before submission.
- Rerun focused TrustPacket tests if CellScaffold changes before submission.
- Decide which repos/branches can be linked publicly.
- Prepare NLnet GenAI prompt provenance log.
