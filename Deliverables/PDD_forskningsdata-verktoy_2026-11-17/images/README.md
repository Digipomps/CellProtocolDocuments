# Bilder til G1-GUI — forskningsdata for studentene

Rendret 2026-11-17 med den ekte web-rendereren i CellScaffold (`Public/js/skeleton-runtime.js`, `porthole-webo.css`, `admin-skeleton.css`, main `57ce8c0`) via `../skeleton/render.js`. Skjelettene og tilstandene står i `../skeleton/`. Skriptet sjekker at teksten i hver tilstand er der (og at det som skal være skjult, ikke er der) før bildet tas.

| Bilde | Flate og tilstand |
|---|---|
| `dashbord-fylt-{laptop,iphone}-v1.png` | Studentens forskningsdashbord med forskerrolle: tre tall-fliser (én skjult), søylediagram med én skjult uke, Mine forespørsler, Opphav |
| `dashbord-uten-rolle-{laptop,iphone}-v1.png` | Samme flate før studenten har forskerrollen: forklaring og «Be om forskertilgang» |
| `kort-ny-{laptop,iphone}-v1.png` | Forespørselskortet entiteten ser: hvem, formål, hva, hvem som ser hva, periode, hva trekk betyr, Ja / Ikke nå / Aldri |
| `kort-godtatt-{laptop,iphone}-v1.png` | Samme kort etter ja: kvittering og «Trekk samtykket» |
| `foresporsel-utfylt-{laptop,iphone}-v1.png` | Studentens forespørselsbygger, gyldig, med forhåndsvisning av kortet og «Send til gruppen» |
| `foresporsel-avvist-{laptop,iphone}-v1.png` | Samme, med to valideringsfeil (gruppe under k, «per person» uten begrunnelse); Send er borte |

Dette er mockups rendret av den ekte web-rendereren, ikke Porthole-preview av kjørende celler:
- Ingen av nøkkelstiene (`research.*`, `researchRequest.*`, `researchInbox.*`) finnes ennå. Tallene, navnet «Sara Nilsen», gruppene og hashene er eksempler, ikke målinger.
- Dagens diagram dropper punkter uten tall (`skeleton-runtime.js:3504–3523`, og likt i Binding). Den skjulte uken 44 står derfor som en rød linje under diagrammet. WP6 skal tegne den som et merket hull i selve diagrammet, i både web og Binding.
- Plukkerne og tekstfeltet er mørke og etikettene svake på lyst lerret. Det er dagens web-renderer (samme funn i `PDD_dele-dokumenter`), ikke et designvalg.
- Bildene viser web. Binding (Swift) er ikke rendret her. Alle elementene (`VStack`, `HStack`, `Text`, `List`, `Button`, `Picker`, `TextArea`, `Visualization` `chart`) finnes i CellApple, men parity er ikke målt; det gjøres i `test.gui.parity`.
