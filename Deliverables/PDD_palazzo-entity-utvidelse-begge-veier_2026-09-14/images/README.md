# images/ — referansebilder for G1-GUI (koble/utvide-opplevelsen)

Alle bilder er 390×844 @2x, rendret av `render.html` (headless Chromium, `shoot.py`) med Palazzo-temaets tokens og
de samme fallback-fontene som Porthole-temaet serverer (Jost for Futura, Playfair Display for Noe Display).
**Dette er mockups, ikke Porthole-preview** (`lesson.scaffold-without-porthole-host-has-no-preview`). Paritet
(test.gui.parity) er egen slice etter at PDD porthole-fjernt-scaffold har gjort Porthole-lasting mulig.

| Bilde | Tilstand | Formål |
|---|---|---|
| gjest-koble-tilbud-v1.png | Sheet over gjesteflaten: bekreftet hus, hvem ⇄ hvem, to setninger, bevislinje, «Koble — ett trykk», «Ikke nå», «Aldri for Palazzo», «Hva betyr dette?» | experience.one-tap, understandable, safe |
| gjest-koble-tilbud-forklart-v1.png | Samme, med «Hva betyr dette?» utvidet (bevis / endrer seg / endrer seg ikke / angre) | experience.understandable |
| gjest-koble-venter-v1.png | To enheter: kode `4F7K‑PZ`, «venter … fullfører automatisk», Avbryt | experience.one-tap (to-enhets-vei) |
| gjest-koble-koblet-v1.png | Kort «Koblet til HAVEN ✓» under «Delt med Palazzo», Angre (30 dager), Se koblinger | experience.safe |
| gjest-koble-aldri-v1.png | Stille linje «Kobling til HAVEN — avslått, vi spør ikke igjen — Endre» | detect.offer-once (reversibel) |
| haven-koble-tilbud-v1.png | Samme tilbud sett fra HAVEN-siden (Q2: begge kan tilby) | detect.D1 |

## Hva dagens skeleton IKKE kan rendre (og hva mockupen derfor viser)
1. **Avatar-sirkler med initial og ⇄-pil** — må bli HStack av Text med `styleClasses` (pz-avatar); sirkelform er tema-CSS, ikke skeleton.
2. **Ekspander («Hva betyr dette?»)** — finnes ikke som element; må enten være en Button som bytter til en konfigurasjon med forklaringen, eller en alltid-synlig seksjon. Må verifiseres i Porthole.
3. **Kode-visning med stiplet ramme** og **spinner** — Text med `styleClasses`; spinner finnes ikke (statisk tekst «venter …»).
4. **Understreket tekstlenke («Aldri for Palazzo»)** — Button med `styleClasses` (pz-quiet); understreking er tema.
5. **Sheet fra bunnen med backdrop** — `SkeletonPresentation.mobileFallback(kind: .sheet)` finnes i samtykkefabrikken; to knapperader i én modal er ikke verifisert (samme merknad som i husk-PDD-en).
6. **Bekreftet-segl** — Text/ikon med `styleClasses`; selve «bekreftet»-tilstanden må komme fra cellen (husets signatur), ikke fra temaet.

## v2 (2026-09-14 kveld) — tekster rettet etter Astra-audit (handoff/ASTRA_ANALYSE.md)
Samme layout og flyt som v1 (godkjent av Kjetil). Endret: «her på telefonen»/«lagres hos deg» → «Palazzo bekrefter gjesten din på sin server, HAVEN-appen bekrefter deg … Koblingen lagres i gjesteankeret ditt hos Palazzo, med kvittering i HAVEN»; «Ingen data flyttes / ikke se noe nytt» → «Innholdet ditt blir liggende der det er. HAVEN får den tilgangen … du velger; huset får ingen nye innsynsrettigheter»; «Angre (30 dager) / beviset slettes» → «Koble fra … tilgangen stopper med én gang; historikken beholdes»; «ett trykk» presisert med «du bekrefter med Face ID»; venter-flaten sier «bekreft at det er Palazzo Comunale du kobler til» og «kan bare brukes én gang». v1 beholdes som historikk. «Bekreftet hus»-seglet krever betrodd binding nøkkel↔hus↔vert i implementeringen — statisk i mockupen.
