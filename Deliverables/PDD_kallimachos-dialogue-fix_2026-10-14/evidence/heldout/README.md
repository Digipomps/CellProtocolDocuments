# Frozen independent semantic evaluation

Created 2026-10-14 before inspecting the candidate implementation or its outputs.
Sources: Documents Git HEAD `c8029847502fe007833d1ebd371bcb5adc01c3ae`, only
Book/01_CellProtocol_Core.md and Book/02_Cell_Interfaces.md, plus the prior
Kallimachos_RAG_Chain_2026-10-13/RESULTAT.md diagnostic report.

The ten cases sample contrast retrieval, real conversational references,
missing context, topic changes, evidence boundaries and both harmful and benign
authority/deletion language. The four response examples deliberately distinguish
assertion from quotation, criticism and hypothetical design. A validator that
rejects every mention of access or deletion must fail the positive controls.

Questions differ from the previous run, but this is an independently authored
regression set informed by known failure classes, not a random unseen domain
sample. It cannot establish general model quality or hallucination freedom.
The independent author has not read product code, candidate tests, candidate
prompts or model outputs and has not made a model call. JSON syntax and file
hashes are checked; execution, integration schema compatibility and semantic
outcomes are not yet checked. Validator examples are semantic exemplars; any
adapter must preserve all summary/claim text and record its mapping.

Start a fresh conversation per case. Record retrieved excerpts, their IDs, raw
model output, validated user-visible output and latency separately. Evaluate
actual assistant history, not a substituted ideal answer. Do not rewrite the
set after exposure to candidate outputs. Fixes made after first exposure require
an explicitly identified subsequent run, not a claim of fresh held-out success.

The freeze manifest hashes the exact JSON, this explanation and the exact Git
source texts; it records the prior report hash without incorporating that report
as a source of protocol semantics.
