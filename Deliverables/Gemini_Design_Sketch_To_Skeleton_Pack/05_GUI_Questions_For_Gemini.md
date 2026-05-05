# GUI Questions For Gemini

These are intentionally hard questions. Answer them explicitly if the design sketch pushes into these areas.

## 1. Auto-Layout Without Stack Spacing

Current `HStack` and `VStack` JSON do not carry explicit `spacing` or `alignment`, even though real designs often depend on them.

Question:

- When a sketch clearly depends on non-default spacing, what is your best conservative mapping using only current Skeleton primitives?
- When is that compromise acceptable, and when should it be marked as a real gap?

## 2. Remote Images As First-Class UI

`Image.url` exists in the model but the current Swift renderer does not load remote images in the newer `SkeletonView`.

Question:

- If a sketch depends on avatars, cover art, product thumbnails, or hero images from remote URLs, do you recommend:
  - a temporary asset-only approximation
  - renderer support for `Image.url`
  - a custom image cell

Please explain the tradeoff.

## 3. Modern Card Polish

Skeleton has border, corner radius, shadow, background color, and text styling, but not gradients, blur, material, masks, or advanced strokes.

Question:

- For modern card-heavy UI, what can still look intentional with the current primitive set?
- Which single styling extension would unlock the most visible quality?

## 4. Tabs, Segments, And Navigation

Many sketches imply tabs, segmented controls, bottom bars, sheets, or route stacks.

Question:

- Which of these should be treated as outside Skeleton and owned by app shell?
- Which are worth encoding into Skeleton itself?

## 5. Breakpoints And Responsive Behavior

The current JSON has `Grid` and adaptive columns, but not a breakpoint language.

Question:

- How would you approximate desktop/mobile variations from a single design system using current Skeleton?
- What would be the smallest backward-compatible JSON addition for responsive layout?

## 6. Rich Message Composer

We have `TextArea`, Markdown display via `Text.styleRole = "markdown"`, and buttons/toggles, but not a real rich text editor.

Question:

- If a sketch shows a Slack-like or Notion-like composer, what can be represented honestly today?
- Where does the line go from "acceptable approximation" to "needs extension"?

## 7. Design Tokens Versus Hardcoded Styling

`styleRole` and `styleClasses` exist, but current renderer mainly exposes them as style metadata plus one special markdown role.

Question:

- Should Gemini emit token-style metadata aggressively even when the current renderer does not fully consume it?
- Or should it keep JSON concrete and visual until there is a stronger token system?

## 8. Minimum Useful Extension Set

Question:

- If you were allowed to add only three backward-compatible Skeleton improvements, which three would unlock the widest range of high-fidelity GUI designs?
