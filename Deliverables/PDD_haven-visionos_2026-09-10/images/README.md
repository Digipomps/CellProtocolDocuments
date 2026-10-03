# images/ — mockups, ikke Porthole-preview

Alle fire bildene er **mockups** rendret fra `mockups/haven-visionos-mockups.html` med Chromium
(1600×900 @2x). De er ikke Porthole-preview av skeleton-JSON
(`lesson.scaffold-without-porthole-host-has-no-preview`), fordi dagens skeleton-format og
Porthole ikke kan rendre det bildene viser: vinduer i rom, glass, ornaments, flipp/bakside,
kjede-diagram, partikler, ventiler. Innholdet *i* flatene er HAVEN-flater i stil, ikke rendret
av rendereren.

| Fil | Viser | Tilstander |
|---|---|---|
| `rommet-portholes-v1.png` | Tre Portholes som egne vinduer, ornament per Porthole, Porthole-kø | fylt |
| `bakside-datastrommer-v1.png` | Baksiden av én Porthole: Absorbert, Abonnert, Puls, set/get — med lest/uleselig/ikke koblet/stille | fylt + feil |
| `inspektor-flowtap-v1.png` | Inspektørvindu: kjede Porthole → FlowTap → celle, Explore, Snapshot, Live, Opptak, Ventil | fylt + feil (deniedNoGrant) |
| `informasjonspress-rom-v1.png` | ImmersiveSpace (mixed): kilder rundt brukeren, strømmer, ventiler, filter | fylt |

Gule bokser er forklaringer til Kjetil, ikke del av flaten. G1-GUI-godkjenning gjelder det som
står inne i glasset. Tomme tilstander mangler i v1 og lages i v2 for den grenen som starter.

## Plangrafikk (ikke mockup)

| Fil | Viser | Kilde |
|---|---|---|
| `plan-simulator-v1.png` | `PLAN.md` §2 som fem steg i tre baner (Kjetil / Losen / Macen) pluss bevisraden. Rødt merke = krever Kjetils ord. | `mockups/plan-simulator.html`, rendret 2026-09-16 |
