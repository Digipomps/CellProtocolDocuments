# Bilder til G1-GUI — La formålet velge språkmodellkilde

Rendret 2026-11-17 med den ekte web-rendereren i CellScaffold (`Public/js/skeleton-runtime.js`, `porthole-webo.css`, `admin-skeleton.css`, main `57ce8c0`) via `../skeleton/render.js`. Skjelettet står i `../skeleton/valgliste-og-min-maskin.v1.json`, tilstandene i `../skeleton/tilstander.v1.json`.

Grunnlag: AI-panelets valgliste i Co-Pilot Chat (`chatHub.state.assistant.providerChoices`, valg til `chatHub.assistant.provider.select`, fra `PersonalCopilotConfigurationFactory.swift:2270–2290`, dumpet i `playwright/fixtures/butler-chat-skeleton.json`).

| Bilde | Tilstand |
|---|---|
| `valgliste-laptop-tilgjengelig-{laptop,iphone}-v1.png` | Kjetil har sagt at laptopen er tilgjengelig; den er valgt for «utvikle og teste» |
| `valgliste-laptop-trukket-{laptop,iphone}-v1.png` | Kjetil har trukket den tilbake; den er borte fra listen, Mistral er valgt |
| `valgliste-laptop-annen-bruker-{laptop,iphone}-v1.png` | En annen bruker med Agreement ser «Kjetils laptop» som valg, men den er ikke valgt automatisk |

Dette er mockups, ikke Porthole-preview av en kjørende celle:
- Nøkkelstiene under `chatHub.state.localModelAvailability.*` og radfeltene `whereLabel`, `factsLabel` og `badge` finnes ikke ennå. Dagens rader har `title`, `modelID` og `availability`.
- Dagens Co-Pilot Chat har mørkt tema (`product-view`); bildene bruker lyst lerret.
- Modellnavn (Gemma 4 12B), svartider og klokkeslett er eksempler, ikke målinger.
- Valglisten bruker `styleRole: admin-table`. Uten den viser web-rendereren to «[x]»-merker i den valgte raden (funnet her; to `.skeleton-list-row-check` per rad når raden er en VStack).
- «Gjør tilgjengelig» finnes bevisst ikke på web: bare laptopen selv kan si at den er tilgjengelig (AgentD-menyen eller Binding på samme Mac). Den flaten er ikke tegnet her.
