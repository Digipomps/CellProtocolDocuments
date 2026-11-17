Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

## Bildene (v1, 2026-11-17, til G1-GUI)

| Fil | Viser | Formål |
|---|---|---|
| `panel-modell-valgt-v1.png` | Hjelperpanelet med modellvelger. Modellen har tolket en bestilling reglene ikke forstår, og forslaget sier hvilken modell, svartid og tokens. | velg, anthropic-forst, laer |
| `panel-modell-mangler-v1.png` | Ingen modell valgt. Panelet sier at bestillingen trenger en modell, med «Legg til modell» og Butler. | si-fra |
| `panel-modell-feil-v1.png` | Leverandøren avviste nøkkelen (401). De andre meldingene er listet. | si-fra |
| `mine-modeller-tom-v1.png` | Fanen hjelper › Mine modeller uten modeller, med skjemaet ferdig utfylt for Anthropic. | mine-modeller |
| `mine-modeller-fylt-v1.png` | Fire modeller, én i bruk, testresultat per modell, «Bruk denne», «Test», «Bytt nøkkel», «Fjern». | mine-modeller, velg |
| `laering-v1.png` | Fanen hjelper › Læring: eksempler med utfall, bryter, sletting, treffrate og eksport av testsett. | laer, tren-formaalsanalysen, data.manner |

Kilde: `mock.html?state=valgt|mangler|feil|modeller-tom|modeller-fylt|laering`, rendret med Playwright (Chromium) i 1440×860, skala 2.

Håndgrep for å legge til en modell, talt fra `mine-modeller-tom-v1.png`: velg leverandør (modell og navn fylles ut), lim inn nøkkel, trykk «Lagre og test». Tre håndgrep.

## RENDERINGSERKLÆRING

Bildene er mockups i HTML, ikke Porthole-preview fra skjelett-JSON. Avvik fra det skjelettet kan i dag:

- **Tre kolonner i fanen hjelper.** Fanen har i dag sett, instruksjoner og versjoner. «Mine modeller» og «Læring» blir trolig egne seksjoner under hverandre eller egne faner, ikke en venstremeny.
- **Kort med knapper på samme rad** bygges som `List` med `HStack` per rad. Fargeprikken for teststatus blir tekst.
- **Bryteren** blir en knapp («Slå av læring»/«Slå på læring»), fordi skjelettet ikke har en bryter som er prøvd her.
- **Tallene** (37 eksempler, 61 % og 84 %, svartider) er eksempler i skissen. Ingen av dem er målt.
- **«Slett valgte»** krever flervalg i en liste. Hvis det ikke lar seg gjøre, blir det «Slett» per rad.

Det skjelettet kan i dag: `Picker` for modell og leverandør, `TextField` med `secure: true` for nøkkelen, `List`, `Button` med keypath.

Alt på bildene som finnes fra før (sett-velgeren, Butler-knappen, «Hjelperen ser») er uendret fra PR #305.
