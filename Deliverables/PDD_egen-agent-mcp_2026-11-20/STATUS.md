# STATUS — egen agent mcp

- surfaces: python,cell,bridge,codex,terminal,gui
- tags: mcp,agreement,llm,provider,consent,privacy,identity

## Porter
- G1: godkjent 2026-11-21 (Kjetil i tråden 21:23Z, «G1 godkjent»; forslagene i §6 gjelder)
- G1-GUI: godkjent 2026-11-23 (Kjetil i tråden 12:34Z, «G1-GUI godkjent»; åtte bilder i images/)
- G2: godkjent 2026-11-23 (Kjetil, 12:50Z) (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-11-20: opprettet
- 2026-11-21: FORMAALSSPEC iterasjon 1 (rot + 15 formål, 1 antiformål, 4 spørsmål). Venter på G1.
- 2026-11-21: G1 godkjent av Kjetil. Forslagene i §6 gjelder: Python i PyCellProtocol, Swift i CellProtocol, Go senere, celler uten mottakervilkår er stengt, bare utkast i egen celle. Neste: bilder til G1-GUI.
- 2026-11-21: Åtte bilder til G1-GUI rendret med web-rendereren (images/README.md). Venter på G1-GUI.
- 2026-11-23: G1-GUI godkjent av Kjetil. Neste: PLAN.md til G2.
- 2026-11-23: PLAN.md (WP0–WP16), dataflow.md, contract/ og handoff/ skrevet. Funn: lenke «samme entitet» gir eiermakt i hele domenet (GeneralCell.swift:2339–2350), så utvidelsen bygges som delegering i Agreement (AgentDelegation + DelegatedAgentCondition). Venter på G2.
- 2026-11-23 12:50Z: G2 godkjent av Kjetil. Merknad: analysen «Entitetsutvidelse i HAVEN» (https://claude.ai/artifact/MZbPNcKM387qAfQak9uhBS) anbefaler at WP3 bruker avgrenset lenke i stedet for AgentDelegation/DelegatedAgentCondition; planbytte spørres før WP3. WP0/WP1 starter.
- 2026-11-23 22:33Z: Planbytte 1 valgt av Kjetil (beslutningskort): WP3 bygger avgrenset lenke (extensionKind scoped, scopeGrants, recipient, expiresAt) i stedet for AgentDelegation/DelegatedAgentCondition. WP2, WP5, WP6, WP8, WP10, dataflow.md og contract/ oppdatert. RecipientCondition beholdes. Formål og bilder uendret.
- 2026-11-23 23:55Z: WP3+WP4 i CellBase: CellProtocol PR #114 (utkast, 1320a34). Linux: 8 nye tester grønne, ingen nye røde blant 1489. Venter på Mac-kjøring.
- 2026-11-25: Kjetil ba om formålsbeskrivelse av hva som er lov, sikkerhetsvurdering av utvidelsen med resonneringstre, kart over entitetens utstrekning, og sikkerhetsrevisjon. Iterasjon 2 skrevet som utkast (`FORMAALSSPEC-ITERASJON-2-UTKAST.md`, F9–F11), G1 for iterasjon 2 spurt. Revisjon: `SIKKERHETSREVISJON_2026-11-25.md`; R1–R5 lukket i CellProtocol #114 (`cbfb881`), E1–E4 åpne og venter på valg. WP2/WP5 (Python/Go) ikke startet: Python og Go mangler lenker i tilgangsavgjørelsen.
- 2026-11-25 (senere): Kjetil valgte «Ja, alle fire» (beslutningskort 09:49Z). Lukket i utkast: E1 PyCellProtocol #5 (eierløs celle avviser, 328 grønne); E2, E3, E4 og nytt E2b (batch og direkte flow-skriving under `identityLinks`) i CellProtocol #117 (`5ec10ba`, `EntityAnchorLinkGuard` i CellBase, felles for CellVapor og CellApple); FlowPlacement til signert innmelding i CellScaffold #514. Linux: 5 regeltester og 34 anker- og FlowPlacement-tester grønne mot ekte CellVapor-anker. Ikke kjørt: macOS, CellApple-bygg, App-målet i CellScaffold. Rester: publikum/opphav fra verten (E3), `proofs` i malen (E4), passkey-flate for hjemmescaffoldet.
