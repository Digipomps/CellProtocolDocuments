# Bilder

Skisser til G1-GUI, runde 3 (02.10.2026). De er ikke godkjent.

| Fil | Viser | Trinn |
|---|---|---|
| `plan-oversikt-v2.png` | hva du får og når, og hvordan en jobb går | alle |
| `meny-post-ulest-v2.png` | ulest post som sak, slik menyen du har i dag viser den | 1 |
| `meny-jobb-godkjenning-v4.png` | en assistent ber om en jobb, og du godkjenner | 4 |
| `meny-planlagte-jobber-ro-v3.png` | «Planlagte jobber» når alt går | 5 |
| `meny-planlagte-jobber-feil-v3.png` | en jobb feilet, og en ble passert | 4 og 5 |
| `meny-planleggeren-staar-v2.png` | planleggeren går ikke | 4 og 5 |

Endret 02.10 kveld, etter at kontrakten ble skrevet og gransket:

- **Godkjenningsbildet (v4).** Menyen sier «Claude ber om en planlagt jobb», ikke «Losen ber om …»: agenten ser bare hvilken app som ber. Tittelen bestilleren skrev, står i anførselstegn. Linjen under har agentens kortform av hva som kjøres («køjobb: git fetch, swift test»), i tillegg til tidsplanen og sluttdatoen. I v2 sto bare tidsplanen der, så du kunne godkjent uten å se hva jobben gjorde.
- **«Planlagte jobber» når alt går (v3).** Et fast program har bare «Sett på pause». «Stopp» finnes for jobber en assistent har bedt om.
- **En jobb feilet (v3).** Saken om fristvarselet har bare «Kvitter» og «Åpne». Fristvarselet er et fast program, og det kan ikke stoppes fra menyen. I v2 hadde saken knappen «Stopp jobben», men den ville bare satt programmet på pause. Pause og fortsett for faste programmer står ett sted, i lista «Planlagte jobber». Saker om jobber en assistent har bedt om, har fortsatt «Stopp jobben».

`meny-jobb-godkjenning-v2.png`, `meny-planlagte-jobber-ro-v2.png`, `meny-planlagte-jobber-feil-v2.png`, `*-v1.png`, `meny-v2.html`, `meny.html` og `plan.mmd` er eldre utgaver og gjelder ikke.

## RENDERINGSERKLÆRING

Flaten er en native macOS-meny (`MenuBarExtra` i `Sources/HavenAgentMenu/HavenAgentMenuApp.swift`), ikke et HAVEN-skjelett. Det finnes derfor ingen `CellConfiguration` å rendre i Porthole, og mappen `skeleton/` brukes ikke. Bildene er tegnet som HTML (`meny-v4.html`, `plan-v2.html`) og rendret til PNG i Chromium (`shot4.js`). `meny-v4.html` tegner alle fem tilstandene; versjonstallet i hvert bildenavn sier når den tilstanden sist ble endret.

- Skrift, avstander, farger og bakgrunn er tilnærmet. De er ikke målt mot macOS.
- Rekkefølgen og teksten i linjene som finnes i dag («Åpne adminflate…», «Oppdater nå», «Varsler: på», «Varselinnstillinger…», «Avslutt», og overskriften «1 venter på deg»), er hentet fra `HavenAgentMenuApp.swift` og `MenuPresentation.swift` på `origin/main` (`ea558ba`).
- Undertittelen i en sak («Vegar · correspondence · kjetil-vegar-d») følger `MenuPresentation.subtitle`: navnet på den som ber, kilden og «Gjelder».
- En undermeny åpner seg til høyre for linjen i macOS. I tre av bildene er den nederste undermenyen flyttet ned for å få plass, og bildet sier det.
- «Sett alle på pause» i lista setter hver jobb på pause, én for én. Det finnes ingen egen kommando for det.
- Adminvinduet vises ikke. Det er der «Åpne» tar deg, og der detaljteksten for en sak står. Vinduet finnes i dag og endres ikke i trinn 1–4.
- Varselet (banneret) vises ikke.
- Linjen «Planlagte jobber» og undermenyene under den finnes ikke i dag. De bygges i trinn 5 etter disse bildene.
