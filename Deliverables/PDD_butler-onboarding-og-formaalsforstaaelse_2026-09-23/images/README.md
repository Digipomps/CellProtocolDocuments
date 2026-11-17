# Bilder — Butler onboarding (G1-GUI, iterasjon 1)

**Dette er mockups, ikke Porthole-preview.** Grunnlaget er et ekte skjermbilde av Butler-
arbeidsflaten (lokal testvert, samme kode som prod `77a922bc`:
`PDD_butler-traadtre-og-widgetflate_2026-09-11/evidence/web-regresjon/plassering/sonde-etter.png`).
Bare innholdet i midtpanelet er tegnet om, med `gen.py` i denne mappen. Alt annet er ekte rendering.

| Bilde | Tilstand |
|---|---|
| `butler-onboarding-steg-v1.png` | Onboarding pågår, steg 1 av 3 (vanlig spørsmål) |
| `butler-onboarding-noekkel-v1.png` | Steg 3 av 3, API-nøkkel — hemmelig felt |
| `butler-onboarding-feil-v1.png` | Onboardingen kunne ikke starte — med årsak og kode |

## RENDERINGSERKLÆRING — hva dagens skeleton ikke kan rendre

Lest i CellProtocol på revisjonen prod kjører (`473357cf`, `Sources/CellBase/Skeleton/SkeletonDescription.swift`):

- **Plassholder fra data.** `SkeletonTextArea.placeholder` og `SkeletonTextField.placeholder` er faste strenger.
  Det finnes ingen `placeholderKeypath`. «Svar på steg 1: leverandør og modell …» krever enten et nytt felt,
  eller en omvei innenfor formatet: to skrivefelt byttet med `visibleWhen`, der onboarding-feltet har en fast
  tekst («Svar på onboarding-steget …») og selve steget står i stripen over.
- **Skjult inndata.** Verken `TextField` eller `TextArea` har en `secure`-modus (`editorMode` er bare
  `plain` / `richMarkdown`). Et maskert nøkkelfelt krever en ny skeleton-kapabilitet i CellProtocol, i
  web-rendereren og i den native rendereren. Uten den vises nøkkelen mens den skrives — det oppfyller ikke
  formålet `…onboarding.hemmelig-inndata`.
- Det som *kan* rendres i dag: stripen «Onboarding pågår» (HStack + tekst + `visibleWhen`), stegprikker
  (liste med stilrolle), «Avbryt onboarding» som knapp, feilkortet med årsak og kode (tekstbindinger).
