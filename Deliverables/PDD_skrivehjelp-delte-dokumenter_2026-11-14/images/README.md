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
