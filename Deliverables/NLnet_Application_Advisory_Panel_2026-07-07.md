# NLnet Application Advisory Panel

Date: 2026-07-07

Status: panel handoff, not submission-ready application text.

Human decision owner: Kjetil.

Recommended working direction: NGI Fediversity first. NGI TALER remains a
separate possible branch only if the proposal commits to a concrete GNU Taler
integration.

## Source Basis

Official NLnet sources checked on 2026-07-07:

- Proposal form: <https://nlnet.nl/propose/>
- NGI Fediversity main page: <https://nlnet.nl/fediversity/>
- NGI Fediversity guide for applicants:
  <https://nlnet.nl/fediversity/guideforapplicants/>
- NGI Fediversity eligibility:
  <https://nlnet.nl/fediversity/eligibility/>
- NGI Fediversity funded-project overview:
  <https://nlnet.nl/thema/NGIFediversityFund.html>
- NGI TALER main page: <https://nlnet.nl/taler/>
- NGI TALER guide for applicants:
  <https://nlnet.nl/taler/guideforapplicants/>
- NGI TALER eligibility:
  <https://nlnet.nl/taler/eligibility/>
- NLnet GenAI policy:
  <https://nlnet.nl/foundation/policies/generativeAI/>

Local source basis:

- `Deliverables/NLnet_Trust_Packet_Structure_2026-07-06.md`
- `README-CellProtocol.md`
- `Book/01_CellProtocol_Core.md`
- `Book/03_Identity_Model.md`
- `Book/04_Agreements_Contracts.md`
- `Book/08_Bridging_Transport.md`
- `Book/21_Contact_Endpoint_Cell.md`
- `Deliverables/DevPlatform_Hetzner_CoPilot_Plan_2026-06-11.md`

External local HAVEN source basis, read-only during this pass:

- `/Users/kjetil/Build/Digipomps/HAVEN/DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/DiMyDocuments/ValueRedistribution/02_PRODUCT_VARIANT_AND_REGULATORY_MATRIX.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md`

## Formaal And Goals

| Formaal | purposeRef | Goal | Status |
| --- | --- | --- | --- |
| Understand exactly what the NLnet application asks for. | `purpose://source.methodology.current` | The required form fields, evaluation criteria, and call constraints are listed with source URLs. | satisfied |
| Identify missing information before drafting final answers. | `purpose://test.acceptance.hallucination-evaluation` | Every answer draft has a support status and missing-info flag where relevant. | satisfied |
| Produce first-pass answers without inventing facts. | `purpose://project-work.share-selected-intent` | Provisional answer text exists for each proposal-form question, with placeholders where facts are missing. | satisfied |
| Critique the draft against NLnet criteria. | `purpose://content.review-before-publish` | A final review panel evaluates strength, risks, and blockers. | satisfied with blockers |

## Panel Structure

The panel runs in three rounds.

| Round | Panel | Mandate | Output |
| --- | --- | --- | --- |
| 1 | Requirements and Evidence Panel | Determine what the application asks for and what information must be gathered. | Requirements ledger and missing-info list. |
| 2 | Answer Drafting Panel | Draft answers to the application questions using only supported facts or explicit placeholders. | Provisional English answer draft. |
| 3 | Review and Skeptic Panel | Evaluate answer quality against criteria and attack unsupported claims. | Claim adjudication, risk list, revision instructions. |

## Round 1 - Requirements And Evidence Panel

### What The NLnet Form Asks For

The current proposal form asks for:

| Field group | Required information | Evidence status |
| --- | --- | --- |
| Call selection | Choose NGI TALER or NGI Fediversity. | supported by proposal form |
| Contact | Name, email, phone, organisation, country. | missing human/applicant data |
| Project info | Proposal name, website/wiki, abstract/outcomes, relevant prior involvement. | partly available, public URL missing |
| Requested support | Amount in EUR, budget use, other funding sources, task/effort breakdown with explicit rates. | missing budget/rates/funding facts |
| Fit and feasibility | Comparison with existing efforts, significant technical challenges, ecosystem engagement/promotion. | partly available, needs focused comparison/upstream plan |
| Attachments | Optional background, task description, cost justification, endorsements; proposal must be self-contained. | trust-packet structure exists |
| GenAI disclosure | Whether GenAI was used; if yes, model, dates, prompts, unedited output. | required because Codex is being used |
| Privacy acknowledgement | Human applicant must acknowledge privacy statement. | human action |

### Evaluation Criteria

For both Fediversity and TALER, the guide says projects are judged on:

- technical excellence / feasibility: 30%
- relevance / impact / strategic potential: 40%
- cost effectiveness / value for money: 30%

The weighted score must be above 5.0 out of 7 to pass to the second stage. The
second stage can ask clarifying questions about differences from existing
projects, complicating factors, claim validation, standards/collaboration,
budget rates, sustainability, and upstream project posture.

### Fediversity-Specific Requirements

Fediversity currently asks for contributions to "the hosting stack of the
future" with service portability, personal freedom, NixOS, reproducibility,
secure operation, easier deployment, open source licensing and open standards.
Eligible activities include FOSS design/development, validation, software
quality, testing/CI, documentation, usability/inclusive design, deployability
and packaging.

Strongest HAVEN framing:

> A reproducible, self-hostable CellProtocol runtime package and conformance
> harness that demonstrates user-owned, capability-governed services with
> portable TrustPacket/ContactEndpoint evidence surfaces.

Weak framing to avoid:

> HAVEN is a broad decentralised protocol for everything.

### TALER-Specific Requirements

TALER asks for contributions aligned with GNU Taler and privacy-preserving
digital payments. Eligible work includes FOSS development, validation,
software quality, testing/CI, documentation, usability, deployability and
packaging, provided there is a clear link to TALER.

Strongest HAVEN framing if TALER is chosen:

> A GNU Taler integration that turns Taler payment confirmation into a
> CellProtocol access-entitlement receipt and audit trail.

Weak framing to avoid:

> DiMy/HAVEN has its own micropayment/value redistribution system.

### Missing Information Ledger

These facts must be gathered before final submission:

| ID | Missing fact | Why it matters | Owner |
| --- | --- | --- | --- |
| M1 | Final call choice: Fediversity or TALER. | The answer text, comparison set, and deliverables change materially. | Kjetil |
| M2 | Applicant legal/contact details. | Required form fields. | Kjetil |
| M3 | Public website/wiki/repository URL. | Required/expected field and reviewer verification. | Kjetil |
| M4 | Open-source license status for the repos or deliverables. | NLnet requires recognised open/free licensing for software outcomes. | Kjetil |
| M5 | Exact requested amount and hourly/day rates. | NLnet asks for explicit rates and value-for-money assessment. | Kjetil/Codex |
| M6 | Other funding sources, past and present. | Required form question. | Kjetil |
| M7 | Exact Fediversity deliverable: NixOS module, package, container-to-Nix bridge, or conformance harness. | Without this, the proposal is too abstract. | Kjetil/Codex |
| M8 | Upstream/community engagement plan. | Reviewers may ask how upstream projects feel about the proposal. | Kjetil/Codex |
| M9 | Existing efforts comparison beyond first pass. | The form explicitly asks for comparison with existing/historical efforts. | Codex |
| M10 | GenAI prompt provenance log. | Required because this work uses Codex. | Codex/Kjetil |

Round 1 decision:

Proceed with a Fediversity-first provisional draft, but mark it non-submission
ready until M1-M10 are resolved. Do not draft a final TALER answer unless M1
chooses TALER and M7 becomes a concrete GNU Taler integration.

## Round 2 - Answer Drafting Panel

The following is written for the NLnet form in English, because the form asks
for English. It is intentionally bracketed where facts are missing.

### Thematic Call

`NGI Fediversity`

Status: recommended, but requires human confirmation.

### Proposal Name

`CellProtocol Fediversity Pack`

Alternative:

`HAVEN CellProtocol Self-Hosted Runtime Pack`

Panel preference: `CellProtocol Fediversity Pack` is clearer and less broad.

### Website / Wiki

Draft answer:

`[NEEDS PUBLIC URL: project website, wiki, repository or public documentation index]`

Do not submit without a real URL unless there is a deliberate reason.

### Abstract

Draft answer:

```text
CellProtocol Fediversity Pack will make a minimal CellProtocol runtime easier
to run, inspect and validate as a self-hosted service. The project will produce
a reproducible deployment package, a small conformance test harness, and a
demonstration service showing domain-scoped identity, explicit capability
contracts, replayable audit, and a portable TrustPacket/ContactEndpoint flow.

The expected outcome is not a full hosted platform. It is a focused R&D package
that helps developers and self-hosters evaluate whether CellProtocol can
support user-owned, capability-governed services in a Fediversity-compatible
environment. The work will include packaging/deployment material, tests,
documentation, and a runnable demo released under an open source licence.
```

Support status: partial. The CellProtocol foundation is documented locally.
The reproducible deployment package is proposed work, not current fact.

### Relevant Prior Involvement

Draft answer:

```text
[NEEDS HUMAN BIO AND PUBLIC LINKS]

The applicant has been developing HAVEN/CellProtocol, a privacy-first protocol
model for small deterministic cells with explicit capability contracts,
domain-scoped identity and replayable audit. Existing local work includes
CellProtocol documentation, CellScaffold runtime surfaces, a TrustPacket
workbench for consent-bound receipts, and deployment planning for self-hosted
runtime infrastructure.

We can provide links to the relevant repositories and documentation once the
public submission URLs are selected.
```

Support status: local evidence exists, but public URLs and applicant biography
are missing.

### Requested Amount

Draft answer:

```text
[NEEDS FINAL AMOUNT]

Panel recommendation: request between 40,000 and 50,000 EUR only if the work
plan includes real packaging, conformance tests, documentation and a runnable
demo. Do not request the maximum unless explicit rates and task estimates
justify it.
```

Support status: incomplete. NLnet allows up to 50 kEUR per proposal, but the
actual amount must be based on real rates and scope.

### Explain What The Budget Will Be Used For

Draft answer:

```text
The budget will be used for four work packages:

1. Reproducible deployment package for a minimal CellProtocol runtime.
2. Conformance tests for identity, capability contracts, replay/audit and
   transport-independent behaviour.
3. A small demo service using TrustPacket/ContactEndpoint-style flows to show
   purpose-bound sharing, receipt/provenance and explicit consent.
4. Documentation, usability review, release preparation and project
   coordination.

[NEEDS RATES AND PERSON-DAYS]
```

Support status: good work-package shape, but budget details missing.

### Other Funding Sources

Draft answer:

```text
[NEEDS FACTUAL ANSWER FROM KJETIL: list past/present funding, or say none if
that is true.]
```

Support status: unknown. Do not infer.

### Task Breakdown And Effort

Provisional structure, not final budget:

| Task | Output | Estimate status |
| --- | --- | --- |
| Packaging/deployment | Minimal reproducible deployment package for CellProtocol runtime. | scope defined, effort missing |
| Conformance harness | Tests for identity, contracts, replay/audit and transport semantics. | scope defined, effort missing |
| Demo flow | TrustPacket/ContactEndpoint demo service. | scope defined, effort missing |
| Documentation/usability | User/dev docs, setup guide, accessibility and reviewer notes. | scope defined, effort missing |
| Project/release | Public release, issue tracking, final report. | scope defined, effort missing |

Submission blocker: explicit rates are required.

### Compare With Existing Or Historical Efforts

Draft answer:

```text
Fediversity already funds important work around NixOS deployment, service
portability and self-hosted applications. Relevant examples include NixOS
fleet-management work, source-based Nextcloud/OnlyOffice packaging, Magic Nix
VFS, NixEdgeOpt, Nocloud, SelfPrivacy and lightweight self-hosted cloud
services.

CellProtocol Fediversity Pack is different in scope. It is not a cloud suite,
CMS integration, file hosting service or scheduler. It focuses on a small
runtime model for user-owned services where identity is domain-scoped, access
is granted through explicit contracts, and behaviour is replayable/auditable.
The proposed work is meant to complement the Fediversity stack by making this
runtime model deployable, testable and inspectable in a self-hosted setting.
```

Support status: partial. Examples are source-backed by the Fediversity funded
projects page. A deeper comparison should be added before submission.

### Significant Technical Challenges

Draft answer:

```text
The main technical challenges are:

1. Defining a minimal deployable CellProtocol runtime without turning the
   proposal into a broad platform rewrite.
2. Packaging the runtime in a way that is reproducible and useful to the
   Fediversity/NixOS ecosystem.
3. Preserving the protocol boundary: transport and hosting must not change
   identity, authorization or replay semantics.
4. Designing conformance tests that make capability contracts and replay/audit
   behaviour easy for reviewers and downstream developers to verify.
5. Keeping the demo honest: TrustPacket verifies receipt payload, provenance
   and declared boundaries; it does not score people or create global
   reputation.
```

Support status: good, grounded in local protocol docs and claim guardrails.

### Ecosystem Engagement And Promotion

Draft answer:

```text
We will publish the work under an open source licence, document setup and
verification steps, and provide a small demo that reviewers and developers can
run. We will engage with the Fediversity/NixOS community around the packaging
approach, and will compare the result against existing Fediversity-funded
deployment and self-hosting efforts.

[NEEDS SPECIFIC CHANNELS/UPSTREAM PLAN: e.g. NixOS packaging review, NLnet
office hour, Fediversity community contact, issue tracker, release repository.]
```

Support status: weak until M8 is resolved. The intent is good; the concrete
engagement plan is missing.

### Attachments

Recommended attachments:

1. `NLnet_Trust_Packet_Structure_2026-07-06.md` or a shortened derivative.
2. Budget/task breakdown with explicit rates.
3. Public repository/documentation links.
4. GenAI prompt provenance log.

Do not attach a broad HAVEN manifesto.

### Trust-Packet Position

Panel recommendation: yes, use a trust-packet, but only as a narrow evidence
packet. It should help reviewers verify sources, claim boundaries, local test
status, missing facts, budget assumptions, GenAI disclosure and reproducible
demo steps. It should not imply a global trust score, reputation system,
certification, security audit or production-readiness guarantee.

### GenAI Disclosure

Draft answer:

```text
Yes. We used OpenAI Codex/GPT-5 in the Codex desktop environment to inspect
local HAVEN/CellProtocol documentation, compare it with official NLnet source
pages, structure the advisory-panel review, and draft provisional application
answers. The human applicant remains responsible for selecting the final
proposal, checking facts, editing the text and submitting it.

[ATTACH/PASTE PROMPT LOG WITH DATES, PROMPTS AND UNEDITED OUTPUT.]
```

Support status: required and accurate in principle, but prompt log must be
assembled from this thread before submission.

## TALER Branch - Not Ready Unless Scope Changes

If Kjetil chooses TALER instead, the proposal must be rewritten around a
concrete GNU Taler integration. The safe root claim would be:

```text
The project will integrate GNU Taler payment confirmation with CellProtocol
access-entitlement receipts, so Taler handles the payment while CellProtocol
records purpose-bound access, provenance and audit.
```

Do not submit TALER language about:

- DiMy internal credits as money
- transferable value
- wallet/custody
- cash-out
- multi-merchant credits
- global micropayment economy
- value redistribution as a finished mechanism

Current TALER status: not submission-ready. Missing facts include the exact GNU
Taler integration point, upstream/community posture, and legal/product boundary.

## Round 3 - Review And Skeptic Panel

### Scorecard

| Criterion | Draft strength | Review |
| --- | --- | --- |
| Technical excellence / feasibility | medium | Strong protocol foundation, but exact Fediversity packaging deliverable is not yet specified. |
| Relevance / impact / strategic potential | medium-high | Good if tied to self-hosting, service portability, reproducible deployment and user-owned runtime operation. Too weak if framed broadly. |
| Cost effectiveness / value for money | unknown | Cannot assess without rates, effort and amount. |
| Eligibility | likely but unconfirmed | Needs final call choice, open licence verification, European-dimension check and public repo/URL. |
| Source grounding | medium-high | NLnet criteria and local protocol docs are checked. Existing-project comparison needs deeper pass. |
| Claim safety | good | Risky payment/reputation claims are excluded. |
| Submission readiness | not ready | Blocked on M1-M10. |

### Root Claim Ledger

| Claim ID | Claim | Type | Status | Support | Counter / Caveat |
| --- | --- | --- | --- | --- | --- |
| C1 | Fediversity is the strongest default NLnet call for HAVEN/CellProtocol now. | normative | supported with caveat | NLnet/Fediversity focus on self-hosting, service portability, NixOS/reproducibility, deployability; prior local analysis agrees. | Requires an actual packaging/deployability deliverable. |
| C2 | The current draft can be submitted as-is. | factual | contradicted | The form requires applicant details, exact budget/rates, other funding, website and GenAI prompt log. | Do not submit yet. |
| C3 | CellProtocol can be framed as a user-owned runtime foundation without overclaiming. | project_capability | partly supported | Local docs support identity/contracts/replay/audit/transport independence. | Production readiness and Fediversity packaging are proposal work, not current facts. |
| C4 | TrustPacket strengthens the application. | causal | partly supported | Existing evidence packet and local verification support consent/provenance/audit framing. | Keep it as evidence attachment, not core claim or reputation signal. |
| C5 | TALER should be the main proposal now. | normative | unsupported | TALER fit requires direct GNU Taler integration. | Current inspected sources do not establish a concrete Taler integration. |
| C6 | We can safely make payment-regulatory claims. | factual | contradicted | Internal guardrails explicitly require legal/current-source verification. | Use access-entitlement framing only. |

### Reviewer Questions We Should Expect

1. What exactly will be packaged for NixOS/Fediversity?
2. How is this different from SelfPrivacy, Nocloud, NixEdgeOpt or other
   deployment/self-hosting projects?
3. Where is the public repository and what licence will the deliverables use?
4. Why is the requested budget cost-effective?
5. Which part is already implemented, and which part is funded work?
6. How can reviewers run the demo and the conformance tests?
7. How will this be sustained after the grant?
8. Has the relevant upstream/community been contacted?
9. Did GenAI produce any application text or code, and where is the prompt log?

### Required Next Iteration

The next panel round should happen after Kjetil provides or decides:

1. Final call choice.
2. Applicant details.
3. Public URL/repository/wiki.
4. Licence/open-publication plan.
5. Requested amount, rates and effort model.
6. Other funding answer.
7. Exact Fediversity technical deliverable.
8. Upstream/community engagement plan.

Until then, the panel cannot honestly produce final answers. It can only
produce placeholders and recommend where facts must be gathered.

## Decision Log

| Decision | Status | Reason |
| --- | --- | --- |
| Use a three-round panel. | accepted | Matches user request and Book 30 workflow. |
| Draft Fediversity first. | accepted as provisional | Best fit from current evidence. |
| Keep TALER branch separate. | accepted | Avoids payment/regulatory ambiguity. |
| Mark incomplete fields instead of inventing. | accepted | Required by user and claim-review guardrails. |
| Do not claim NixOS packaging already exists. | accepted | Not established in inspected local sources. |

## Final Panel Verdict

The advisory panel is set up and has completed the first three iterations:

1. requirements and information needs,
2. provisional answer drafting,
3. critique and claim adjudication.

The current Fediversity-first draft is coherent but not submission-ready. The
main argument is solid only if we define a narrow deliverable:

> reproducible packaging + conformance tests + runnable demo for a minimal
> CellProtocol runtime in a Fediversity-compatible self-hosting context.

The strongest next action is not more prose. It is to decide and document the
exact technical deliverable and budget.
