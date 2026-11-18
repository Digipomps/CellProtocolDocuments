# STATUS — workbench modellvalg og laering

- surfaces: cell, gui, skeleton
- tags: ai-gateway, credentials, learning

## Porter
- G1: godkjent 2026-11-17 (Kjetil 13:34Z: «G1 godkjent.»)        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: godkjent 2026-11-17 (Kjetil 22:10Z: «G1-GUI godkjent»)        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-11-18 (Kjetil 06:35Z: «1. G2 Godkjent»)        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-11-17 — BYOK-lageret (`ButlerProviderConfigurationStore`) er aldri koblet til i `configure.swift` og henger på Vapor-appen, så en celle når det ikke. Planen gir lageret én felles instans som både HTTP-rutene og WorkbenchHelperCell bruker. Formatet og forseglingen er uendret fra det G1 godkjente.
- 2026-11-18 — Butler-rutene `/butler/api/v1/providers/*` kobles likevel ikke til lageret i denne runden. De er slått av med vilje i dag, og stoppregelen sier at Butler ikke røres uten Kjetils ord. Cellen bruker `ButlerProviderConfigurationStore.shared`; rutene skal bruke samme instans når de slås på.
- 2026-11-18 — Nøkkelen sendes med Enter i det skjulte feltet, ikke med knappen «Lagre og test» fra bildet. Rendreren lar ikke en knapp lese et skjult felt (WP-S regel 4), og det er riktig oppførsel.
- 2026-11-18 — Treffraten i flaten måles med regelmotoren (hvor mange godkjente bestillinger reglene forstår før og etter nye ord), ikke ved et kall til PurposeQualityMonitor. Testsettet eksporteres i formen `quality.compareChatPrompts` leser, og T-L3 kjøres på eksempler fra staging slik planen sier.

## Logg
- 2026-11-17: opprettet; FORMAALSSPEC iterasjon 0 sendt til Kjetil for G1
- 2026-11-17: G1 godkjent av Kjetil 13:34Z uten endringer; anbefalingene i §6 gjelder. Han ba i tillegg om en vurdering av trådadministrasjon (TRAADADMINISTRASJON.md).
- 2026-11-17: Kjetil 13:36Z la til hjelp til studenten (Sara) og generell HAVEN-hjelp. FORMAALSSPEC iterasjon 1: grenen haven-help.* som fase 2, ikke godkjent ennå. Bilder til G1-GUI (fase 1) sendt.
- 2026-11-17: G1-GUI godkjent av Kjetil 22:10Z for de seks bildene i images/. Iterasjon 1 (haven-help.*) er fortsatt ikke besvart. PLAN.md skrevet og sendt til G2.
- 2026-11-18: G2 godkjent av Kjetil 06:35Z uten endringer; anbefalingene gjelder (nanoGPT ikke nå, regeltreff blir læring). Bygging startet.
- 2026-11-18: WP1–WP7 skrevet i CellScaffold (gren claude/project-thread-fkjjgp): WorkbenchHelperModels.swift, WorkbenchHelperCell.swift, DeveloperWorkbenchConfiguration.swift, WorkbenchHelperModelTests.swift. `contract/` og `dataflow.md` lagt til. Ikke kompilert ennå: skyen har ikke Swift, og bygget på Macen eller i CI gjenstår.
