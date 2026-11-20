# Bilder til G1-GUI — modell i felles chat

Rendret 2026-11-15 med den ekte web-rendereren i CellScaffold (`Public/js/skeleton-runtime.js` og `Public/css/porthole-webo.css`, main `9612217`) fra skeleton-JSON i `../skeleton/`. Kommando:

    node skeleton/render.js <CellScaffold> images skeleton

Grunnlaget er Samtaler-skjelettet slik `playwright/fixtures/samtaler-skeleton.js` speiler `PersonalCopilotConfigurationFactory.conversationsSkeleton()`, utvidet med modelldeltakeren.

| Bilde | Tilstand |
|---|---|
| `modellchat-forslag-{laptop,iphone}-v1.png` | Ola har foreslått modellen, Sara har sagt ja, du blir spurt |
| `modellchat-fylt-{laptop,iphone}-v1.png` | Modellen er med, to svar: ett fra Qwen (spurt av Ola), ett fra Mistral (spurt av deg, med kvote) |
| `modellchat-feil-{laptop,iphone}-v1.png` | Lokal modell svarte ikke; bare den som spurte ser meldingen, med «Prøv med Mistral» |

## Hva skjelettet ikke kan rendre / hva bildene ikke viser

- Ingen nye elementtyper: alt er `Text`, `Button`, `List`, `TextArea`, `VStack/HStack` med `visibility` (rot og rad) og `backgroundKeypath`, som Samtaler bruker i dag.
- `labelKeypath` på knapper løses bare mot raden, ikke mot roten. Derfor er modellvalget to faste knapper per modell, der rot-betingelsen `model.mistralSelected` viser den valgte fylt. Kvoten står i teksten under.
- Bildene er ikke tatt fra Binding. Paritet i Binding er `test.gui.parity` etter implementering.
- Invitasjonslenke-blokken er uendret og ikke vist.
