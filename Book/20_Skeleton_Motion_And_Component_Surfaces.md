# Chapter 20 - Skeleton Motion And Component Surfaces

Date: 2026-05-07

This chapter documents the V1 contract for purpose-driven motion and component
surfaces in CellProtocol/HAVEN.

Porthole is a Cell and the user's interface into the CellProtocol/HAVEN
universe. Binding apps and CellScaffold programs/processes are scaffolds. Both
use Porthole and must be able to render the same portable skeleton semantics.

## 1. Why Motion Exists

Motion is not decoration. In the chat workbench it explains why a helper surface
appears, where it came from, and how it can be minimized or restored.

The normal loop is:

1. The user writes a prompt in chat.
2. The assistant matches the prompt to Purpose/Interest candidates.
3. The user opens a helper without side effects.
4. The helper surface appears with a short motion hint.
5. The user can minimize, restore, pin or dismiss it.
6. Domain side effects happen only after an explicit target action.

Examples:

- "jeg har en ide jeg maa skrive ned" opens an Ideas/Vault helper.
- "vi trenger avstemning" opens a poll helper.
- "inviter Anna" opens an invite helper or a candidate chooser.
- a user shortcut with `personal.chat.assist.idea.capture` can open the same
  idea helper without pretending to be a new primitive.

## 2. Skeleton Modifier Contract

`SkeletonModifiers` now supports:

- `motionHint: SkeletonMotionHint?`
- `motionSourceRole: String?`

`SkeletonMotionHint` values:

- `appear`
- `expand`
- `collapse`
- `minimize`
- `restore`
- `replace`
- `emphasize`

The skeleton never owns timing, easing, keyframes or platform-specific
animation. Renderers own that. A skeleton only says what semantic transition is
happening.

`motionSourceRole` points to a semantic source role already present in the UI,
usually the `styleRole` of another element:

- `chat-composer`
- `suggestion-card`
- `component-surface`
- `minimized-helper-pill`

Portable JSON example:

```json
{
  "Section": {
    "header": { "Text": { "text": "Forslag" } },
    "content": [],
    "modifiers": {
      "styleRole": "suggestion-card",
      "motionHint": "appear",
      "motionSourceRole": "chat-composer"
    }
  }
}
```

## 3. Renderer Rules

Porthole web:

- maps motion fields to `data-motion-hint` and `data-motion-source-role`
- adds sanitized classes such as `motion-hint-expand`
- uses short opacity/translate/focus-ring transitions
- disables or replaces motion under `prefers-reduced-motion: reduce`

Apple/Binding:

- wraps rendered skeleton elements in `SkeletonMotionHost`
- maps hints to opacity, small move transitions or emphasis highlight
- respects `accessibilityReduceMotion`
- must not change layout only because motion metadata is present

All renderers must avoid:

- bounce
- spin
- parallax
- long staggered sequences
- auto-oscillation
- full-screen motion that disorients the user

Motion is never the only signal. Text and visible structure must also explain
what appeared and why.

## 4. Component Surface State

Chat V1 stores component surface state inside `PersonalChatHubCell`, not in a
global UI singleton and not in the target domain cell.

Read keypaths:

- `chatHub.state.ui.componentSurfaces`
- `chatHub.state.ui.activeComponentSurfaceID`
- `chatHub.state.ui.minimizedComponentSurfaces`
- `chatHub.state.ui.lastMotionEvent`

Write keypaths:

- `chatHub.ui.openComponentSurface`
- `chatHub.ui.minimizeComponentSurface`
- `chatHub.ui.restoreComponentSurface`
- `chatHub.ui.dismissComponentSurface`
- `chatHub.ui.pinComponentSurface`

`openComponentSurface` is side-effect free. It may never save an idea, invite a
person, create a poll, query a RAG, invoke an AI provider or enqueue an agent
intent. It only changes chat-local UI state.

Surface record fields:

- `id`
- `kind`
- `title`
- `summary`
- `purposeRef`
- `interests`
- `targetCellEndpoint`
- `targetActionKeypath`
- `grantStatus`
- `state`
- `motionHint`
- `sourcePromptPreview`

The target cell still owns its own domain logic and must validate grants and
input when the user clicks the real action.

## 5. Ideas/Vault Flow

Purpose ref:

- `personal.chat.assist.idea.capture`

Intent triggers:

- "jeg har en ide"
- "jeg har en idé"
- "maa skrive ned"
- "ma skrive ned"
- "skriv ned"
- "hva om vi"
- user-defined shortcuts with the same purpose

V1 target preference:

1. `cell:///IdeaTaskWorkspace` with `ideaWorkspace.captureIdea`
2. Vault-like cells only when visible in the requester's scope

If no target is in scope, the chat may show why the helper is unavailable, but
it must not fake a local save. In the current implementation, capture returns
`idea_workspace_unavailable` when `IdeaTaskWorkspace` is not granted.

## 6. Absorbed Chats

Chat can keep compact references to other chat cells:

Read keypaths:

- `chatHub.state.ui.absorbedChats`
- `chatHub.state.ui.activeAbsorbedChatID`
- `chatHub.state.ui.combinedChatView`

Write keypaths:

- `chatHub.absorbChat`
- `chatHub.releaseAbsorbedChat`
- `chatHub.setActiveAbsorbedChat`
- `chatHub.setCombinedChatView`

Rules:

- every absorbed chat must have a visible source badge
- missing grants show an access requirement, not messages
- combined view is allowed only when source badges remain visible
- messages from different threads must never be mixed without labels

## 7. Binding Parity

This V1 deliberately does not add a new skeleton element type. It uses existing
portable primitives:

- `Tabs`
- `Section`
- `List`
- `TextField`
- `TextArea`
- `Button`
- `Grid`
- `VStack`
- `HStack`

This keeps Binding and Porthole aligned. Binding can choose native motion
transitions, but it must preserve the same safety model:

- opening a helper is not accepting a suggestion
- side effects require explicit target action
- reduced motion is respected
- missing target grants are visible and non-leaky

## 8. Test Requirements

Protocol tests:

- encode/decode `motionHint` and `motionSourceRole`
- decode legacy skeleton JSON without these fields

Renderer tests:

- web emits `data-motion-hint` and `data-motion-source-role`
- web honors reduced motion
- Apple renderer does not change layout when motion is absent
- Apple renderer honors `accessibilityReduceMotion`

Chat tests:

- `openComponentSurface` changes only UI state
- `idea_capture` opens an idea helper and does not save without click
- target grants are checked before capture
- minimized helpers can be restored
- absorbed chat without grant never exposes messages

