# STATUS — formal velger modellkilde

- surfaces: binding, cell, gui, scaffold
- tags: agreement, availability, llm, provider, purpose

## Porter
- G1: godkjent 2026-11-17 (Kjetil i tråden 08:13Z, med tillegg om publisering og hendelser)
- G1-GUI: godkjent 2026-11-17 (Kjetil i tråden 08:43Z; seks bilder i images/)
- G2: godkjent 2026-11-17 (Kjetil i tråden 08:53Z)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-11-16: opprettet
- 2026-11-16: FORMAALSSPEC iterasjon 1 (13 formål, 12 formålstester, 4 spørsmål). Venter på G1. Bilder til G1-GUI lages etter G1.
- 2026-11-17: G1 godkjent av Kjetil. Iterasjon 3 legger inn tillegget hans (4 nye formål). Beslutningskort om hvem som ser laptopen. Neste: bilder til G1-GUI.
- 2026-11-17: seks bilder til G1-GUI rendret (images/README.md). Venter på G1-GUI.
- 2026-11-17: G1-GUI godkjent av Kjetil. Neste: PLAN.md til G2.
- 2026-11-17: PLAN.md skrevet (18 arbeidspakker). Venter på G2.
- 2026-11-17: G2 godkjent av Kjetil. Implementering startet med WP0–WP2.
- 2026-11-17: WP1–WP4 skrevet. CellScaffold utkast-PR #454 (egnethetskontrakt, kildefakta, hardt filter). TESTRESULT.md startet. Tillegg i kontrakten: servingClass requester_device (Apple Intelligence på enheten spørreren sitter ved).
- 2026-11-17: WP5, WP6, WP8 og WP9 på vertssiden skrevet (CellScaffold #454, `b533ecd`): cellen `LocalModelAvailability`, erklær og trekk tilbake, hendelser, målt helse. 41 tester grønne i isolert pakke. Merk: etter denne endringen vises ikke laptop-modellen før HavenAgentD sender erklæringen (WP7, ikke skrevet). Neste: CI-resultat, så WP7 og WP10.
- 2026-11-17: CI på CellScaffold #454 grønn. WP7 skrevet og bygget på Mac: HavenAgentD utkast-PR #43 (menyvalg, kunngjør og trekk tilbake). Neste: WP10 (panel og Agreement-holdere).
- 2026-11-18: HavenAgentD #43 rød i CI (stopp i ClaudeCodeBridgeTests, ikke gjenskapt lokalt); egen PR #46 bytter waitUntilExit med terminationHandler, grønn, venter på fletting. WP10 startet: whereLabel og factsLabel fra kildefakta (CellScaffold #454). Avvik fra G1-GUI-bildet: teksten «Spørsmålet forlater ikke maskinen» er tatt ut for laptopen, fordi spørsmålet går fra verten over broen til laptopen. Godtatt av Kjetil 2026-11-18. Gjenstår i WP10: panelskjelettet («Min maskin», «Hendelser») krever digest-migrering av lagrede skjeletter, og Agreement-holdere.
- 2026-11-18 (ettermiddag): WP10 del 2 i CellScaffold #454 (cbc55eb5), CI grønn: modellisten viser «Valgt», hvor modellen kjører og fakta; «Min maskin» (kun eier) med «Gjør utilgjengelig» (`chatHub.localModelAvailability.withdraw`); «Hendelser» fra `chatHub.state.localModelAvailability`. Agreement-holder ser ikke selected/fallback_used. Lagrede innebygde flater oppgraderes ved at fabrikken bygger forrige utgave (`chatHubSkeletonBeforeModelSourcePanels`). Gjenstår i WP10: hasAgreement-kobling for ikke-eiere og helsemeldinger fra AgentD.
