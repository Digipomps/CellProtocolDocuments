# STATUS - musikkstatistikk 20260904

- surfaces: cell, gui, web
- tags: agreement, delivery, music, privacy, statistics

## Porter
- G1: **godkjent 2026-09-08** (FORMAALSSPEC.md, iterasjon 1)
- G1-GUI: **godkjent 2026-09-08** (fire bilder i images/)
- G2: PLAN.md skrevet 2026-09-24 kveld; Kjetil: «bare fiks det - du administrerer» — skive 1a+1b (tellere og lese-API, ingenting synlig endres) settes i gang i natt. Skive 1c (fanen) venter på bilde v2, skive 2 på §6.1. Tidligere: G2 sto stille fra 2026-09-08 til 2026-09-24 uten at planen ble skrevet (Losens feil). Kjetil 2026-09-24: fortsatt ønsket, også fra ikke innlogget bruk (§6.2 = ja).
- G3: ikke startet

## Valg (Kjetil)

2026-09-08 - to spor for lagring:
- Anonym lytter: spoerres ikke, lagres ikke. Bare tellere paa laata.
- Innlogget lytter: aktiv samtykke-utfordring i overlay; samtykket lever
  som egen signert Agreement.
- Artisten ser bare fordelinger, aldri enkeltlyttere.

## Valg tatt for dekomponering (Kjetil, 2026-09-05)
- Lagring: per lytter, bak Agreement
- Maaling: baade «levert» og «lyttet», holdt fra hverandre
- Flate: Butterpop Studio

## Bilder til godkjenning
| Fil | Tilstand |
|---|---|
| images/statistikk-fylt-v1.png | Normal drift, tre publiserte laater |
| images/statistikk-tom-v1.png | Ingenting talt ennaa |
| images/statistikk-blindflekk-v1.png | Nesten alt utenfor samtykke |
| images/statistikk-detalj-v1.png | En laat, frafall gjennom laata |

Bildene er HTML-mockup rendret med Butterpop Studios egen butterpop-studio.css,
1260 px bredde, 2x. Ikke Porthole-preview: Studio er en Leaf-flate med egen
CSS/JS, ikke en skeleton-rendret flate, saa mockupen med den ekte stylesheeten
ligger naermere sannheten enn en skeleton-preview ville gjort.

## Kjent avvik fra dagens kode, som maa med i planen
- `.segmented` i butterpop-studio.css er `repeat(4, minmax(0,1fr))`. En femte fane
  krever at den endres til 5. Mockupen bruker en `.is-five`-variant.

## Ingen kode er skrevet
Ingenting er implementert. Dette er P0-P1 + P1-GUI.

## Logg
- 2026-09-25 01:50Z: Skive 1a+1b (tellere og lese-API) merget som CellScaffold PR #262 → main `e6277af1`. Codex implementerte; Losen fant at en tellefeil kunne stoppe avspilling, Codex rettet det og fant i tillegg at nedlasting ble stoppet av en tellefeil (rettet). Lokalt 38 tester / 0 feil; CI grønn (run 36079253838). Image for main bygges (kjøring 36083749837). Fanen (1c) venter på bilde v2; skive 2 på §6.1. Rapport: `handoff/SKIVE1.md`.
- 2026-09-25 04:57Z: **I prod.** Main `e6277af1` (metodikk + Butterpop AP1 #261 + musikkstatistikk skive 1 #262): image 36083749837 publisert 04:46Z, staging COMMITTED_VERIFIED 04:48:53Z, prod 04:49:20Z, `/health/build` bekreftet. Kapittel 38 i prod-containeren (9 276 byte). Butterpop 200; `/butterpop/api/workspace/statistics` anonymt 401. Staging lagt tilbake til PR #254-imaget `4dd70c52` 04:57Z (hentesteget feilet fordi imaget bare finnes lokalt; lagt tilbake uten det). Bevis: `HAVEN-Deploy/_handoff/NATT/NATT-B2-UT.md`, `STAGING-TILBAKE.md`.
- 2026-09-25 05:00Z: Bilde v2 av fanen laget til G1-GUI: `images/statistikk-skive1-v2.png` (slik fanen ser ut før samtykke-sporet) og `images/statistikk-fylt-v2.png` (ferdig). Kilde `mock-v2.html`. Venter på Kjetil.
- 2026-09-25 07:50Z: Kjetil: «1. Ok 2. 90 dager ok» → G1-GUI v2 godkjent, §6.1 = 90 dager. Skive 1c (fanen) til Codex. Skive 2: bilde av samtykke-spørsmålet lages til G1-GUI.
