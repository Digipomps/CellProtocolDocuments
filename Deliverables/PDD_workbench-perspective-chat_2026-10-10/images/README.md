# Referansebilder for G1-GUI

2026-10-10. **Designkandidat med syntetiske data. G1 og G1-GUI er godkjent (2026-10-10 / 2026-10-11).**

Start med [bildegalleriet](../GUI_GALLERY.html). Klikk et bilde for original størrelse.
Bildene er gjengitt med CellScaffolds uendrede web-renderer fra
`7678b2c3d293978b5b179cdcada5e843f17c5b73`. Dette er ikke skjermbilder fra produksjon.

| Kontroll | Målt resultat |
|---|---|
| Rendringer | 54 (27 lys, 27 mørk) |
| JS-/unsupported-/komponentfeil | 0 |
| Horisontal overflyt | 0 ved de prøvde breddene |
| Tekstkontrast | Minst 4.99:1 for målte synlige Text, etiketter og kontrolltekster |
| Registrerte kontrollhandlinger | 926, fordelt på 43 keypaths |
| Separate mount-/session-payloads | Kontrollert i lys og mørk komponentprøve |
| Skriv → Send/Lagre | Integrasjonsgap påvist; fersk tekst følger ikke knapp-payload automatisk |

Kontrastmålingen bruker beregnede CSS-farger mot nærmeste ugjennomsiktige bakgrunn.
Den er ingen full tilgjengelighetsrevisjon: fokus, skjermleser, placeholder-kontrast,
alle hover-tilstander, touchbruk og native rendering er ikke komplett kontrollert.
Smal visning er Chromium ved 390 px med `touch`-kapabilitet, **ikke SwiftUI/Binding-bevis**.

## Kilder og stil

Fire frosne filer lastes: skeleton-runtime.js, haven-localization.js, porthole-webo.css
og developer-workbench.css. Den eksporterte theme-aliasfilen lastes ikke.
Kildehashene står i [renderer/manifest.json](../renderer/manifest.json).

| Kilde | MD5 |
|---|---|
| Public/js/skeleton-runtime.js | `f24e5f98ecaad31bd6429a9a5b695227` |
| Public/js/haven-localization.js | `e424e58703fc8b1514a29bf9ab045259` |
| Public/css/porthole-webo.css | `7747a044e4d8c5ce83a35fbcc2612480` |
| Public/css/themes/Developer Workbench.css | `10a3f9615b2accca2da4c2bedf121de9` |
| Public/css/developer-workbench.css | `c67f67c263932182f804a778b8a9df8e` |

`candidate.css` er en eksplisitt kandidat-utvidelse: tomme valgfrie List-plasser uten
synlig boks, felter som fyller plassen, én TextArea-ramme, flat sidemeny og nowrap
for deklarerte HStack-rader. Rendererfilene er ikke endret.
Alle innholdstekster, knapper og felt i produktbildet kommer fra Skeleton og fixture.
Den grå «DESIGNKANDIDAT»-stripen kommer fra harnessens HTML.

Vi har ikke skjult varsler fra en innlogget side: ingen live side er brukt. Hele
innholdsrammen gjengis med fullPage. Portholes globale navigasjon/editor er ikke med
i denne isolerte flateprøven. Smal navigasjon skjules via Skeleton layoutVariant;
bilder av smal bredde gjelder bare den selvstendige chatten.

## Grenser

Alle nye actions er designkontrakter. De er **ikke** dokumentert som implementerte
Explore-handlinger. Knappetrykk registreres lokalt og utfører ingenting. Menyer kan
åpnes og felter kan fylles i testharnessen; navigasjon mellom kandidatbilder, faktisk
søk/filtrering, modellkall, lagring, kø, merge og deploy er ikke koblet til backend.
Backend skal validere gjeldende filter-/preview-revisjon og faktisk requester.

Se [GUI_REVIEW.md](../GUI_REVIEW.md) for godkjenningsomfang og implementeringsgap.
`render-report.json` inneholder rå mål, payloads og gap-prober. `action-inventory.json`
er en kompakt liste. `image-manifest.json` låser akkurat bildefilene som fremlegges.

## Reprodusere

Fra denne leveransemappens rot, med eksisterende Playwright installert:

```sh
python3 generate.py
node render.js
python3 build_review.py
```

Harness støtter `NODE_PATH` til et eksisterende Playwright-miljø og `CHROMIUM_PATH`
til en allerede installert Chromium. Ingen npm-installasjon, Swift-bygg, server,
ekstern nettverksforespørsel eller GitHub Actions trengs. Alle nettverksforespørsler
fanges og besvares fra lokal fil eller avbrytes. En lokal Chromium-prosess kan kreve
OS-/sandbox-godkjenning. Testen bruker en isolert midlertidig profil.
