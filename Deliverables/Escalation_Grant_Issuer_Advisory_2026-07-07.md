# Escalation Grant Issuer — Advisory Panel Adjudication

Date: 2026-07-07
Panel: `escalation_grant_issuer_2026-07-07` (5 models over NanoGPT)
Raw responses: `Tools/ModelKnowledge/generated/panel_escalation_grant_issuer_2026-07-07_20260707T123042Z.json`
Method: Book 30 panel decomposition; Book 29 claim adjudication.
Decision owner: Kjetil. The panel makes assumptions/risks/alternatives visible; it does not decide.

## Formål (intent) and Goals

- **Purpose** (candidate ref `purpose://haven.advisory-panel.escalation-grant-architecture`): decide the production-ready architecture for a real issuer of the Co-Pilot interpreter escalation grant, so sub-slice A (real issuer, no live external call) can be built without open blockers.
- **Goal** (`haven.goal-definition.v1`): every one of the three owner decisions + the A/B fork has an adjudicated recommendation with reasoning; the two cross-cutting production questions (self-issued threat model, replay/determinism) are answered well enough to write a Codex handoff. **Status: satisfied.**

## Panel

| Model | Role | Q1 | Q2 | Q3 |
|---|---|---|---|---|
| GPT-5.5 | capability/authorization security architect | **B** | per-scaffold | 24h |
| GLM-5.2 | independent architecture critic | **B** | per-scaffold | 7 days |
| Gemini-3.1-Pro | replay-determinism & auditability | **A** | Entity-base | 7 days |
| DeepSeek-V4-Pro | contrarian red-team | **A** | per-scaffold | session + opt-in |
| Kimi-K2.6 | production-readiness & consent-UX | **A** (partial; truncated after Q1) | — | — |

## Decision log

### Q1 — Architecture fork (A vs B): **near-even split, adjudicated to B on HAVEN's guardrail.**

Raw tally: 2 full A (Gemini, DeepSeek) + 1 partial A (Kimi, truncated) vs 2 B (GPT-5.5, GLM-5.2). Not a clean majority — a genuine fork.

- **Pro-A argument** (Gemini/DeepSeek/Kimi): reuse the tested capability machinery; a bespoke verifier in the engine is a "shadow authorization layer" that drifts from the resolver and reintroduces confused-deputy risk; adding one `EscalationCondition` is a "low-risk extension" since the resolver already dispatches on condition type; the resolver then makes post-expiry/revocation execution *mathematically impossible*.
- **Pro-B argument** (GPT-5.5/GLM-5.2): do not couple *volatile* product policy (providers, model classes, pricing, PII rules — the least stable part of the system) to the *most safety-critical, most stable* core primitive. Wrong direction of the dependency arrow. B is acceptable **only** if it re-establishes signature-binding, domain-scoping, revocation, replay-protection and audit-binding by hand, with explicit code-review discipline.

**Adjudication (mine, for Kjetil's sign-off):** The panel under-weighted one fact not in the brief — HAVEN's **standing guardrail forbids CellResolver/core-`Agreement` changes without explicit owner approval**. Option A *is* a core change (new `Condition` type in `CellBase/Agreement/Condition/`). The A camp's "low-risk extension" framing does not hold under HAVEN's actual risk posture. The pro-B dependency-direction argument is also architecturally stronger for a churning domain. **Recommend B — but fold in the A camp's decisive insight:** issuance and revocation must be **resolver-gated writes anchored to a real `Grant` on a dedicated keypath** (e.g. `chatHub.assistant.escalationGrant`), so authority is never a purely ad-hoc struct. Both GPT-5.5 and GLM-5.2 independently required exactly this. Net: the *rich escalation policy* is a signed descriptor evaluated by the chat engine (no core churn); the *authority to issue/revoke* is a real resolver-gated capability (no shadow layer). Option A remains the purer long-term architecture and becomes worth its core-change cost only **if external model invocation ever becomes a first-class CellProtocol capability** (GPT-5.5's explicit caveat). This is the one decision that touches the core-change guardrail, so it is surfaced for Kjetil to confirm or override to A.

### Q2 — Grant ownership layer: **per-scaffold (3-1).**

Consensus on per-scaffold, with Entity-base only as a *prefill template* that materializes a fresh signed per-scaffold grant — never a live authority. Reasoning: smaller blast radius; the downward-only conference clamp should be defense-in-depth, not the primary boundary (a clamp/classification bug must not leak a base grant into a context never reasoned about); scalpel-not-sledgehammer revocation; clearer mental model ("this Co-Pilot may auto-escalate; that one may not"). Gemini's lone Entity-base vote relied on the clamp fully mitigating blast radius — the majority (incl. the red-team) treated that as too much trust in a mitigation. **Recommend per-scaffold default + an Entity-level "revoke all" emergency switch + a visible list of active grants.**

### Q3 — Grant duration: **persistent-with-expiry, default 7 days, hard downgrade, no silent renewal (consensus on shape, spread on the number).**

Unanimous: hard downgrade to ask-this-time on expiry; **silent renewal is an absolute anti-pattern**; renewal requires a fresh consent surface + new signature; never offer "never expire." Duration spread: 24h (GPT-5.5), 7d (GLM-5.2, Gemini), session+opt-in (DeepSeek). **Recommend 7 days as default, user-selectable {this session, 24h, 7 days}.** 7d is the median of the persistent camp and balances consent-fatigue (which trains blind "allow-all" clicking — the exact red-line failure) against silent-re-escalation risk. A "renew with same terms" one-click is acceptable **only if the full terms are displayed alongside the click**, never hidden behind it.

### Q4 — Self-issued threat model: **consensus — meaningful, not theater.**

The signature does not (and should not) protect against the user; it is load-bearing against **software/state attacks**: (1) fabrication by a compromised/buggy cell minting an unsigned descriptor; (2) replay of an expired/revoked grant; (3) confused-deputy reuse across Entity/scaffold/purpose. Minimum mechanisms: canonical serialization; signature over the complete descriptor verified against the user Identity on **every** routing decision (not cached across messages); unique grant id/nonce; issued-at + expiry; online revocation/active-set check; audience+purpose+Entity+scaffold binding; reject any detached grant not present in authoritative owner-scoped state. Named caveat (all): if the signing key or consent UI is compromised, the signature no longer proves consent — key protection and issuance-surface integrity are part of the TCB.

### Q5 — Replay/determinism reconciliation: **consensus — record the I/O boundary; the call is outside the replay boundary.**

The external call is a non-deterministic, cost-bearing side effect; "no side effect without a click" holds only by treating the prior signed grant as pre-authorization — do not pretend the later call is not a side effect. Reconciliation: emit `model.route.invoked` (grant id, issuer, correlationId, provider/model, data-class result, **input digest not raw draft**, quota reservation) before, `model.route.completed|failed` (response **hash** not raw output, cost/tokens, quota settlement) after. **Replay must NOT re-invoke the provider** — it consumes the recorded completed/failed observation and re-presents the staged proposal by hash. External output stays **proposal-only** (never enters cell state without a click). Quota is decremented deterministically **from the event log** (reserve at invoked, settle at completed; failed still consumes; denied does not). GLM-5.2's open sub-question: hash-only audit vs an encrypted cell-scoped audit vault for "what was actually sent" — **lean hash-only for V1**, revisit if forensics demand it.

### Q6 — Production hardening: **consensus.** Folded directly into the handoff as requirements (consent surface disclosure list, one-click revoke, quota from event-log, credentials never in grant/flow/cell, failure→downgrade-never-silent, full audit chain call→grant→issuer→time).

### Q7 — Split: **unanimous GO.** Sub-slice A (real issuer + signature + storage + revocation + quota accounting + full audit chain, **no live external call**, fully testable with a mock adapter) → sub-slice B (wire exactly one real external lane behind the verified grant). Named risk (GLM-5.2): the mock adapter must have a **byte-identical interface** to the real adapter so B is a credential+endpoint swap, not a redesign.

## Open items

- **Q1 owner confirmation**: B-anchored-to-real-Grant (recommended) vs Option A core change. Only this touches the core-change guardrail. — owner: Kjetil.
- **Audit depth** (Q5): hash-only vs encrypted audit vault. Deferred to post-V1 unless forensics require. — owner: Kjetil.
- Corpus registration: register this deliverable in `model_knowledge_sources.json` and rebuild if it should be RAG-discoverable.

## Cross-runtime note

Signature verification + owner-scoped storage must be byte-identical across Porthole (web) and Binding (native); the issuance consent surface is a skeleton. DeepSeek flagged cross-runtime signature-verification drift as a concrete exploit surface — parity test required in sub-slice A.
