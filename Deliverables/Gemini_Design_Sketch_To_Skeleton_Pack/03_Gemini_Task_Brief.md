# Gemini Task Brief

Use this when asking Gemini to convert design sketches into Skeleton UI proposals.

## Mission

Read the design sketch or screenshots, infer the intended UI conservatively, and produce:

1. a valid Skeleton JSON proposal
2. a capability gap analysis against the current HAVEN / CellProtocol runtime
3. a short list of minimal extensions only where truly needed

## Operating Rules

- Read this package before proposing JSON.
- Prefer valid current JSON over speculative future JSON.
- Be explicit about approximation.
- If the sketch implies app-shell behavior rather than Skeleton behavior, say so.
- If data bindings are unclear, use placeholder/static values and list the missing bindings as assumptions.

## Required Output Format

### 1. Intent Summary

Describe:

- primary user task
- major layout regions
- key interactions
- whether the sketch looks data-driven, feed-driven, form-driven, or app-shell-driven

### 2. Fit Verdict

Provide one verdict:

- `direct`
  - current Skeleton should represent this well enough
- `approximate`
  - current Skeleton can represent the structure, but fidelity is visibly compromised
- `requires_extension`
  - current Skeleton cannot represent the design honestly enough

### 3. JSON Output

Return:

- `skeleton` JSON at minimum
- full `CellConfiguration` JSON if the bindings are clear enough

Rules:

- Use canonical field names only.
- Keep the JSON syntactically valid.
- Do not invent unsupported element types or stack fields.

### 4. Gap Analysis

Return a flat table with these columns:

- `design_feature`
- `status`
- `why`
- `current_workaround`
- `recommended_extension`

Status must be one of:

- `native`
- `approximate`
- `unsupported`

### 5. Assumptions

List all assumptions that affected the JSON:

- missing data source
- unknown runtime actions
- ambiguous navigation
- unknown responsive behavior

### 6. Minimal Extension Set

If the verdict is `requires_extension`, propose the smallest useful extension set.

Bad answer:

- "Add a complete custom renderer."

Good answer:

- "Add stack spacing support."
- "Add remote image loading for `Image.url`."
- "Add a `Badge` element."

## Prompt Template

```text
Read every file in the Gemini Design Sketch -> Skeleton Pack.

Then inspect the attached design sketch images.

Your task is to:
1. summarize the intended UI
2. decide whether current HAVEN Skeleton can represent it directly, approximately, or only with extensions
3. output valid canonical Skeleton JSON
4. produce a gap-analysis table
5. propose the smallest useful extension set if needed

Constraints:
- Follow the JSON contract exactly
- Do not invent unsupported stack spacing/alignment fields
- Treat remote image support as a known renderer gap
- Use `Text.keypath` mainly for row-local data and `Text.url` for top-level remote lookups
- Prefer conservative valid JSON over speculative future JSON
```

## Strategy Hints For Gemini

- Start by identifying the dominant structure:
  - linear layout
  - grid
  - layered hero card
  - feed list
  - form
- Then map each region to current Skeleton primitives.
- Only after that, list the leftover design features that do not map cleanly.

## When To Produce Two Variants

If a sketch contains both representable structure and unsupported polish, produce:

1. a `conservative` Skeleton variant that will work now
2. an `aspirational` variant description that names the missing renderer capabilities
