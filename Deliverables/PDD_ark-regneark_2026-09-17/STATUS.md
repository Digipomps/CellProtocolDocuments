# STATUS — ark regneark

- surfaces: cell, gui, skeleton
- tags: regneark, skeleton, tabell, ytelse

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-17: opprettet
- 2026-09-17: iterasjon 1. Kjørende prototype bygget og målt (prototype/ark.html): konstant 880
  celler i DOM og 9,5 MB heap fra 1 000 til 250 000 rader, median tegnetid 2,3–3,6 ms. Retter mitt
  eget F1b-forslag fra 15.09 — SwiftUI Grid måler alle barn og duger ikke til et ark. Flaskehalsen
  er datakontrakten: getItems() henter hele settet. Tre bilder levert for G1-GUI. Venter på G1.
- 2026-09-18: Kjetil bekreftet delingen — Grid er et layoutverktøy for flater, ark er verktøyet for
  å vise tabell. Retningen godkjent. Formålstreet venter fortsatt på G1.
