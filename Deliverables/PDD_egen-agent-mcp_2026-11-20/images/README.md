# Bilder til G1-GUI — «Egne agenter»

Rendret 2026-11-21 med den ekte web-rendereren i CellScaffold (`Public/js/skeleton-runtime.js`, `porthole-webo.css`, `admin-skeleton.css`, CellScaffold main `62bb34b`), laptop 1280 px og iPhone 390 px, `deviceScaleFactor` 2.
Skjelett: `../skeleton/egne-agenter.v1.json`. Tilstander: `../skeleton/egne-agenter-tilstander.v1.json`. Skript: `../skeleton/render.js` (sjekker at forventet tekst finnes og at skjulte deler er skjult).

| Bilde | Viser | Formål |
|---|---|---|
| `egen-agent-foresporsel-{laptop,iphone}-v1.png` | Ny forespørsel fra Claude Code: maskin, fingeravtrykk, leverandør, hva som sendes ut, celler den ber om, hva som holdes tilbake og hvorfor, varighet, «Godkjenn med passkey» / «Avvis» | F2b, F3, F3c, F4, F4a, F4b |
| `egen-agent-godkjent-{laptop,iphone}-v1.png` | To tilkoblede agenter (Claude Code og Codex) med leverandør, gyldighet, celler, sist brukt, «Vis logg» og «Koble fra» | F2b, F7 |
| `egen-agent-frakoblet-{laptop,iphone}-v1.png` | Claude Code er koblet fra: neste kall avvises, loggen kan fortsatt leses | F2b |
| `egen-agent-logg-{laptop,iphone}-v1.png` | Loggen for én agent: lagret utkast, lest, delvis (andres meldinger holdt tilbake), avvist (forskningsnivå), søk | F3a, F3b, F3c, F4b, F7 |

Navn, maskiner og dokumenter er eksempler. Alle nøkkelstier under `ownAgents.*` er forslag; ingen finnes i CellScaffold i dag.

Det dagens skjelettformat ikke gir her:
- Statusteksten til høyre har samme farge (grønn) for «tilkoblet» og «frakoblet», fordi fargen settes per element og ikke per rad. Rød for frakoblet krever to tekstelementer med synlighet per rad, eller en fargenøkkel i tilstanden.
- Passkey-dialogen er ikke vist; den er nettleserens egen.
- Agentens side (terminalen som viser samme fingeravtrykk) er ikke en HAVEN-flate og er ikke tegnet.
