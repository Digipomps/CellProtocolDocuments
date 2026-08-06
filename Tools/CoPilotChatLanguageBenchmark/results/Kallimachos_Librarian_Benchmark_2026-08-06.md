# Kallimachos Librarian Benchmark

Date: 2026-08-06

## Scope

This run uses the existing Norwegian Co-pilot six-point scoring contract for
12 synthetic librarian cases:

- three summaries with an exact source quotation;
- three honest catalogue-gap responses;
- three gap-triggered, one-time invitations;
- three responses after the user has declined an invitation.

Exact citation fidelity is reported separately and does not change the
six-point total. A citation passes only when `parsed.slots.citation` equals
`expected.exactCitation` exactly as a decoded JSON string.

## Runtime Boundary

- Qwen3-8B Q4_K_M ran through the existing GGUF runner. That runner forces
  CPU (`--device none`) for its documented reproducible path.
- Gemma 4 E4B QAT ran through the existing MLX/VLM runner with Metal and
  `HF_HUB_OFFLINE=1` plus `TRANSFORMERS_OFFLINE=1`.
- Both runs used only the committed synthetic fixtures. No external provider
  or network source was used.
- HAVENAgentD was not used. Its current `AgentLocalModelProfile.knownProfiles`
  contains the Qwen 2.5 0.5B test and Borealis 4B profiles, not stable profiles
  for either model in this comparison.

The latency numbers are therefore useful for the tested local paths, but are
not an architecture-neutral speed comparison between the models.

## Results

| Model | Total | Parse errors | Mean latency/case | Median latency/case | Exact citation fidelity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen3-8B Q4_K_M (GGUF/CPU) | 53/72 (73.6%) | 0 | 42.552 s | 42.326 s | 1/3 (33.3%) |
| Gemma 4 E4B QAT (MLX/VLM/Metal) | 56/72 (77.8%) | 0 | 14.621 s | 13.814 s | 3/3 (100.0%) |

### Dimension scores

| Dimension | Qwen3-8B | Gemma 4 E4B QAT |
| --- | ---: | ---: |
| Intent | 3/12 (25.0%) | 5/12 (41.7%) |
| Action | 11/12 (91.7%) | 12/12 (100.0%) |
| Clarification | 11/12 (91.7%) | 10/12 (83.3%) |
| Safety | 10/12 (83.3%) | 10/12 (83.3%) |
| Must mention | 7/12 (58.3%) | 7/12 (58.3%) |
| Must not mention | 11/12 (91.7%) | 12/12 (100.0%) |

### Category scores

| Category | Qwen3-8B | Gemma 4 E4B QAT |
| --- | ---: | ---: |
| Summarize with exact quote | 15/18 (83.3%) | 18/18 (100.0%) |
| Catalogue gap | 12/18 (66.7%) | 12/18 (66.7%) |
| Gap invitation | 12/18 (66.7%) | 12/18 (66.7%) |
| Declined invitation | 14/18 (77.8%) | 14/18 (77.8%) |

## Recommendation

Use Gemma 4 E4B QAT as the first candidate for the next bounded rung where
the model phrases or summarizes after deterministic retrieval. It led this
small run on total score and exact citation fidelity.

Do not use either result to make the model a policy authority. Both models
were weak on the new intent labels, and both scored only 66.7% in the gap and
invitation categories. Keep gap detection, one-invitation maximum, refusal
memory, source selection, exact-citation validation and action authorization
deterministic outside the model.

This run did not include human naturalness or grounding scores. Three citation
cases are evidence for this fixture set, not a general quality guarantee.

## Reproduction

Both commands use:

```text
--cases Tools/CoPilotChatLanguageBenchmark/librarian_cases.no.jsonl
--contexts Tools/CoPilotChatLanguageBenchmark/librarian_contexts.v1.json
```

Run `summarize_results.py` over the generated JSONL result files to reproduce
the total, dimension, category, latency and exact-citation tables.
