# Bilder til G1-GUI — entitetsutvidelse som virker

Navn: `<flate>-<web|app>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent (G1-GUI i `../STATUS.md`) teller som referanse ved P5.
Tre oversiktsark samler bildene per flate: `oversikt-min-entitet-v1.png`, `oversikt-koble-enhet-v1.png`, `oversikt-hjemmescaffold-v1.png`.

## Rendret med web-rendereren fra skjelett-JSON, ikke tegnet

Skjelettene i `../skeleton/*.cellconfiguration.json` og eksempeldataene `../skeleton/state-*.json` er laget av `gen_skeleton.py`
og rendret av `render.js` i Chromium med CellScaffolds egne filer:

| Fil fra CellScaffold `origin/main` `b049a6e1` | md5 |
|---|---|
| `Public/js/skeleton-runtime.js` | `bc728d825d46b2a9e8ac960cae63a7e6` |
| `Public/css/porthole-webo.css` | `5309243a7f2b40eb88b94aeb420394ff` |
| `Public/js/haven-localization.js` | `e424e58703fc8b1514a29bf9ab045259` |

Harnessen er `<main class="canvas view-mode">` (lys flate), `createRenderer({rootElement, skeleton, onAction}).update(state)`,
bredde 1180 med `pointer, hover, keyboard, drag` for web og 390 med `touch` for app-bredde.
`render-report.json`: 19 bilder, 0 feil i konsollen, 0 `Unsupported`-elementer, ingen vannrett rulling.

## Det bildene viser

| Flate | Bilde | Tilstand | Bladformål |
|---|---|---|---|
| Min entitet | `min-entitet-web-alt-naabart-v1.png`, `min-entitet-app-alt-naabart-v1.png` | 3 hele enheter, 1 avgrenset, 3 steder, alt virker | E1, E2, E5, D2 |
| Min entitet | `min-entitet-web-ett-sted-utilgjengelig-v1.png` | ett sted svarer ikke og avviser koblede enheter til listen er fersk | B3, E4 |
| Min entitet | `min-entitet-web-lenke-trukket-v1.png`, `min-entitet-app-lenke-trukket-v1.png` | iPhone trukket; to steder vet det, ett henter senest 12:56 | B3, E4 |
| Min entitet | `min-entitet-web-tom-v1.png` | bare eierenheten og ett sted | E1 |
| Koble til enhet | `koble-enhet-web-eier-start-v1.png`, `-eier-kode-`, `-eier-godkjenn-`, `-eier-ferdig-` | eierens fire skjermbilder | B2, D1 |
| Koble til enhet | `koble-enhet-app-ny-start-v1.png`, `-ny-venter-`, `-ny-ferdig-` | den nye enhetens tre skjermbilder | D1 |
| Koble til enhet | `koble-enhet-app-avvist-utlopt-v1.png`, `koble-enhet-app-avvist-avslaatt-v1.png`, `koble-enhet-web-avvist-passkey-v1.png` | de tre avvisningstekstene | B2, D2 |
| Hjemmescaffold | `hjemmescaffold-web-ikke-koblet-v1.png`, `-koblet-`, `-feil-passkey-` | kobling av hjemmescaffoldet med passkey | F2 |

## Håndgrep, talt fra bildene

| Part | I bildene | I dag (lest fra `VaporIdentityLink.swift`, ikke talt på skjerm) |
|---|---|---|
| Eieren, ny hel enhet | 3 trykk og 1 passkey: «Koble til en ny enhet», «Lag koblingskode», «Godkjenn med passkey» etter å ha sammenlignet tre ord. **Én gang for alle steder.** | lage billett, sammenligne ord, godkjenne med passkey, **per vert** |
| Den nye enheten | 1: skrive koden og trykke Enter (eller åpne lenken). Resten går av seg selv. | sende forespørsel, fullføre, **per vert** |
| Eieren, hjemmescaffold | 1 trykk og 1 passkey | finnes ikke med passkey i dag |
| Eieren, trekke tilbake | 1 trykk | 1 trykk per vert |

Rekkefølge: eier 1 → eier 2 → ny enhet 1 → ny enhet 2 og eier 3 samtidig → eier 4 og ny enhet 3.
Med tre steder blir det 4 håndgrep for eieren mot 9 i dag, og 1 for den nye enheten mot 6.

## Det bildene ikke viser

- **Passkey-dialogen.** Den tegnes av nettleseren eller systemet, ikke av skjelettet.
- **Native visning i Binding (SwiftUI).** Måles ved P5. App-bildene er web-rendereren i telefonbredde.
- **At cellene leverer disse dataene.** Tilstandene er eksempeldata. `entityMap.state` og `enrollmentView` finnes ikke i koden i dag.
- **Handlingene.** Stiene er forslag, se `render-report.json` → `behaviour`: `me.entityMap.device.revoke {linkID}`, `me.entityMap.device.add`,
  `me.entityMap.refresh`, `me.identityLinks.startEnrollment {scope}`, `me.identityLinks.requestEnrollment "<kode>"`,
  `me.identityLinks.approveEnrollment {requestID}`, `me.identityLinks.declineEnrollment {requestID}`, `home.link.anchor {}`.
  Bare `approveEnrollment` og `link.anchor` finnes i dag, og de tar imot andre data enn her.
- **QR-kode.** Skjelettformatet har ikke noe QR-element. Koden skrives inn, eller lenken åpnes.
- **Stedsnavnene.** «Informasjonssystemer (UiO)» og adressen er eksempler.

## Sett i rendereren, ikke rettet

- Tekstfeltet «Kode, for eksempel …» er mørkt på lys flate. Det er rendererens egen stil for felt i `view-mode`.
- En tom `List` beholder avstanden til naboen i en `VStack` med `spacing`. Luften ligger derfor på raden (`gap()` i `gen_skeleton.py`),
  ikke på forelderen (`lesson.empty-list-keeps-its-slot`).

## Spørsmål til Kjetil ved G1-GUI

1. **Skal «Trekk tilbake» spørre én gang til før det skjer?** Forslag: ja, én bekreftelse uten passkey, fordi et feiltrykk ellers
   stenger en enhet ute. Uten bekreftelse er det 1 håndgrep, med er det 2. Bildene viser knappen, ikke bekreftelsen.
2. **Skal de tre ordene sammenlignes når koden allerede er skrevet inn?** De finnes i dagens flyt. Forslag: behold dem, fordi koden
   beviser at enheten kjenner koden, mens ordene beviser at det er samme forespørsel du godkjenner. Uten dem er det ett blikk mindre.
