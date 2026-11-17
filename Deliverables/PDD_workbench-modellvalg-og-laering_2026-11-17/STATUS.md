# STATUS — workbench modellvalg og laering

- surfaces: cell, gui, skeleton
- tags: ai-gateway, credentials, learning

## Porter
- G1: godkjent 2026-11-17 (Kjetil 13:34Z: «G1 godkjent.»)        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: godkjent 2026-11-17 (Kjetil 22:10Z: «G1-GUI godkjent»)        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-11-17 — BYOK-lageret (`ButlerProviderConfigurationStore`) er aldri koblet til i `configure.swift` og henger på Vapor-appen, så en celle når det ikke. Planen gir lageret én felles instans som både HTTP-rutene og WorkbenchHelperCell bruker. Formatet og forseglingen er uendret fra det G1 godkjente.

## Logg
- 2026-11-17: opprettet; FORMAALSSPEC iterasjon 0 sendt til Kjetil for G1
- 2026-11-17: G1 godkjent av Kjetil 13:34Z uten endringer; anbefalingene i §6 gjelder. Han ba i tillegg om en vurdering av trådadministrasjon (TRAADADMINISTRASJON.md).
- 2026-11-17: Kjetil 13:36Z la til hjelp til studenten (Sara) og generell HAVEN-hjelp. FORMAALSSPEC iterasjon 1: grenen haven-help.* som fase 2, ikke godkjent ennå. Bilder til G1-GUI (fase 1) sendt.
- 2026-11-17: G1-GUI godkjent av Kjetil 22:10Z for de seks bildene i images/. Iterasjon 1 (haven-help.*) er fortsatt ikke besvart. PLAN.md skrevet og sendt til G2.
