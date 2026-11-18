# Bilder for G1-GUI

Rendret 14.11.2026 i skycontaineren med Playwright 1.63 og den ekte web-rendereren fra CellScaffold `8e8f8e0`:
`Public/js/skeleton-runtime.js`, `Public/js/haven-rich-document.js`, `Public/css/porthole-webo.css`, `Public/css/rich-document.css` og Quill.
Skjelettet er det samme som `RichDocumentCell.configuration()` (richDocument + documentHelp + documentChat).
Skriptene ligger i `kilde/`.

| Bilde | Hva som er ekte | Hva som er tegnet |
|---|---|---|
| `dokument-i-dag-laptop.png` | Alt. Slik Dokument ser ut i dag | – |
| `skrivehjelp-forslag-*-v1.png` | Editor, kommentarer, dokumentchat | Skrivehjelp-panelet (injisert HTML): modellinje, markert tekst, modusvalg, «Spør modellen», logg med «Bruk forslaget» |
| `skrivehjelp-av-*-v1.png` | Som over | Panelet når modellhjelp er av, med eierens knapp |
| `skrivehjelp-feil-*-v1.png` | Som over | Panelet når den som spør ikke har valgt modell (knappen er deaktivert), og et foreldet forslag |

## Hva skjelettet ikke kan rendre i dag

- Panelet finnes ikke i `haven-rich-document.js`; det må skrives (web).
- Binding (Swift) rendrer verken `richDocument`, `documentHelp` eller `documentChat`: `CellApple/.../SkeletonView.swift:2593` viser «Visualization kind '…' støttes ikke ennå». Ingen Binding-bilde er laget før §6 spørsmål 3 er besvart.
- Markeringen i editoren (blå bakgrunn på den markerte setningen) vises ikke i bildene; i ekte flate er det Quills vanlige markering.
- Navn (Sara, Petter, Kari) er eksempler. I dag viser loggen identitets-ID, ikke navn.

## v2 (2026-11-15): rendret fra skeleton-JSON

Etter G1 valgte Kjetil vei (a): panelet bygges av vanlige skeleton-elementer, så det også virker i Binding.
`skrivehjelp-*-v2.png` er rendret fra `skeleton/dokument-med-skrivehjelp.v1.json` med `Public/js/skeleton-runtime.js`
fra CellScaffold `9612217` (main 15.11) og tilstandene i `skeleton/tilstander.v1.json`. Skript: `skeleton/render-v2.js`.

- Ekte: hele panelet er vanlige elementer (Text, Picker, TextArea, Button, List med radknapper og `visibility` på radnivå). Ingenting er injisert.
- Knappeprobe (`skeleton/knappeprobe-v2.jsonl`): hver knapp sendte riktig keypath og nyttelast, f.eks. `document.assist.apply` med `{"entryId":"e2"}` fra raden.
- Tilstandene (`document.assistPanel`) er tegnet data. Cellen som lager dem finnes ikke ennå.
- Ikke rendret i Binding ennå. Panelet bruker bare elementer CellApple tegner, men editoren (`richDocument`) og dokumentchatten (`documentChat`) vises der fortsatt som «støttes ikke ennå».
- Avvik fra v1: «Spør modellen» er ikke deaktivert uten modell. Knappen står, og cellen svarer med varselet «Ingen forespørsel er sendt», fordi en deaktivert knapp må styres av en betingelse på toppnivå, som Binding ikke evaluerer pålitelig (skeleton-skillen, reachability.md). Etiketten over avsnittsvelgeren er blek i dagens web-tema.
- Teksten som sendes velges i «Tekst modellen skal se»: et avsnitt, eller det du har markert i editoren (web). Binding har ingen editor ennå, så der velger man avsnitt.
