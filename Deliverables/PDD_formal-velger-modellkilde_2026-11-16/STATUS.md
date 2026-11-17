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
