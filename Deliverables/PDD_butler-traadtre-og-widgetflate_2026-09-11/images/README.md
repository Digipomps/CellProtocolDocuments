# Referansebilder — Butler Chat: trådtre, skop og widgetflate

Navn: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent (G1-GUI i `../STATUS.md`) teller som referanse for `test.gui.parity`.

## Dette er mockups, ikke Porthole-preview

Bildene er rendret med Chromium (Playwright, `render.js` i denne mappen) fra Kjetils mockup
`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup.html`, utvidet med tilstandene *tom* og *feil* i
`HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html` (`?state=tom|drag|full|feil`, `?viewport=app`).
Ingen piksel kommer fra HAVEN-serveren, skjelettformatet eller Porthole. De viser **hva som skal bygges**, ikke hva som finnes
(`lesson.mockup-er-ikke-leveranse`, `lesson.scaffold-without-porthole-host-has-no-preview`).

Det bildene viser som dagens skjelettformat **ikke** kan rendre (kilde `../handoff/KAPASITET_SKJELETT.md`, oppsummert i FORMAALSSPEC §3):

- et navigerbart tre med utbretting og tastaturstyring;
- skop som *operasjon* over etterkommere («Undertre» / «Bare denne»), ikke bare skjul/vis;
- en widget som fortsetter å følge kilden etter at den er festet («oppdatert 09:26», «kilden svarer ikke — viser siste kjente verdi»);
- automatisk bytte av kolonner mellom kompakt og full flate;
- på app-siden: generisk dra-og-slipp (Binding mangler det; egen PDD-oppgave, jf. §6 spm. 3).

Navnet «Losen» i bildene er mockupens eget navn på assistenten og er ikke en designbeslutning i denne oppgaven.

## Bildene

| Fil | Flate | Tilstand | Viser | Bladformål |
|---|---|---|---|---|
| `web-tom-v1.png` | web 2000×1250 | tom | bare Butler-roten i treet (1 samtale, 0 grener), startkort «Slik kan jeg hjelpe deg i gang» med fire rader, tom flate med hint om å dra ut et kort | A1, A4, B1 |
| `web-fylt-v1.png` | web | fylt | tre med grener (Sponsorsamtale, Pressemelding), skop «Undertre · 2 grener», grenstart i loggen, to festede widgets | A1, A2, B3 |
| `web-dra-v1.png` | web | dra | kort dras ut av chatten (halvgjennomsiktig), slippsone «Slippes her — over ‹Sponsorstatus›», flaten markert | B1, B2 |
| `web-full-v1.png` | web | full flate | widget utvidet til hele flaten, flere kolonner (innleder), chatten dokket | B4 |
| `web-feil-v1.png` | web | feil | rutelinje «Rutet til Butler. Hjelperen ‹Pressemelding› kunne ikke svare (avslo …)» med «Gi tilgang / Vis ruten», grenen merket «avslo», widget med «kilden svarer ikke — viser siste kjente verdi» | A3, B3 |
| `app-normal-v1.png` | app 780×1688 | normal | treet bak «Tråder»-knappen, chat med kort, flaten som horisontal rekke nederst | C1 |
| `app-dra-v1.png` | app | dra | kort dras ned til flaten, slippsone «Slippes her» | B1, C1 |
| `app-tom-v1.png` | app | tom | startkort og tom flate i app-bredde | A4, C1 |

Tilstandene *tom* og *feil* finnes ikke i Kjetils originale mockup; de er lagt til av Claude for at
`test.routing.fallback` (A3) og første-gangs-bruk (A4/B1) skal ha et referansebilde. Godkjennes de ikke, er det mockup-utvidelsen
som forkastes, ikke originalen.

## Rendre på nytt

```
cd CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/images
node render.js            # krever playwright; CHROMIUM=… og MOCKUP=… kan overstyres
```

Ny versjon av et bilde får nytt `-v<n>`; gamle beholdes til G3 er satt.
