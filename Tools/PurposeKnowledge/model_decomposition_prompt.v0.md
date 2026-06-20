# HAVEN Purpose Decomposition Prompt v0

Use this prompt when asking a language model to decompose a user prompt into HAVEN purposes for evaluation.

Return only JSON matching `haven.purpose-model-output.v0`.

```text
You are evaluating a user prompt against the HAVEN purpose taxonomy.

Task:
- Select the smallest sufficient set of HAVEN purposeRefs.
- Include goalRefs that would prove the purpose is achieved.
- Include nearestSharedPurposeRef for the selected primary purposes.
- Use purpose://prompt.unknown when the prompt is not covered.
- Do not invent purposeRefs. Unknown or new purposes go in candidatePurposeRefs.
- Do not claim side effects. This task is analysis only.

Output JSON schema:
{
  "schema": "haven.purpose-model-output.v0",
  "id": "<case id>",
  "status": "resolved | unknown | partial",
  "purposeRefs": ["purpose://..."],
  "goalRefs": ["goal..."],
  "nearestSharedPurposeRef": "purpose://...",
  "candidatePurposeRefs": [],
  "missingCapabilities": [],
  "reviewRequired": false,
  "confidence": 0.0,
  "sideEffectFree": true,
  "mutatesPerspective": false,
  "mutatesEntity": false,
  "briefRationale": "One short sentence."
}

Known purposeRefs and goalRefs:
<INSERT COMPACT PURPOSE KB OR RETRIEVED NODE SUBSET HERE>

Case:
id: <CASE_ID>
locale: <LOCALE>
prompt: <USER_PROMPT>
visibleCapabilities: <VISIBLE_CAPABILITIES_JSON>
```

Evaluation modes:

- `closed-book`: omit the known purpose list; checks whether the model understands the task unaided.
- `open-taxonomy`: provide compact purpose nodes, aliases, parent refs, and goal refs.
- `retrieved-context`: provide only top-K nodes from the deterministic HAVEN resolver.
- `repair`: provide the model's previous JSON and validator errors, then ask for corrected JSON.

The gold label remains the HAVEN fixture/human-reviewed expectation. Frontier models can suggest new cases and explain disagreements, but they are not the authority.
