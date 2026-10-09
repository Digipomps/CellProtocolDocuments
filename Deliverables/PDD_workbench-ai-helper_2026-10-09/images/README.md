Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

## Bildene (v1, 2026-10-09, til G1-GUI)

| Fil | Viser | Formål |
|---|---|---|
| `hjelperpanel-tom-v1.png` | Panelet i fanen intake før noe er spurt. Valgt sett, hva hjelperen ser, forslag og Butler-knapp. | A2, C2, F, F1 |
| `hjelperpanel-fylt-v1.png` | «Flytt alt fra inbox over til triage»: forslag med de 7 elementene markert, ikke utført ennå. | C1, C2, A4 |
| `hjelperpanel-feil-v1.png` | Settet «Flater og GUI» får en bestilling som ikke kan gjøres (bildetekst på publisert verk). Hjelperen sier hva som mangler og tilbyr å gi saken til Butler. | B4, F2 |
| `sett-rediger-v1.png` | Redigering av settet «Denne flaten»: instruksjonstekst, låste handlinger, versjoner og diff mot forrige. | A1, A2, A3, A4 |

Kilde: `mock.html?state=tom|fylt|feil|rediger`, rendret med Playwright (Chromium) i 1440×860, skala 2.

## RENDERINGSERKLÆRING

Bildene er mockups i HTML, ikke Porthole-preview fra skjelett-JSON. Det skjelettet ikke kan rendre i dag:

- **Hjelperpanel ved siden av en annen flate.** `HStack` med en `Reference` til en hjelpercelle kan legge panelet ved siden av, men det finnes ingen fast sidekolonne som følger med mellom fanene. Det må enten være en del av Developer Workbench sin egen konfigurasjon, eller et Porthole-skall-element som Butler-knappen.
- **Markering av elementer i en annen liste.** At de 7 elementene i intake lyser opp fordi hjelperen foreslår dem, krever at forslaget skrives til en keypath listen leser (for eksempel `selection`). `WorkItem` har `select` og `clearSelection`, så det kan bindes, men det er ikke prøvd.
- **Diff med farger.** Ingen skjelettelement viser tekstforskjeller. Diffen må lages i cellen som en liste med radtype, og fargen settes med modifikatorer per rad. Ikke prøvd.
- **Låste handlinger.** Listen er ren visning. Låsen håndheves i cellen (A4), ikke av at feltet ikke kan redigeres.

Det skjelettet kan i dag: `TextArea` for instruksjonene, `Picker` for valg av sett, `List` for versjoner og elementer, `Button` med keypath for Utfør, Forkast, Gå tilbake hit og Butler.
