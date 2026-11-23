# STATUS — egen agent mcp

- surfaces: python,cell,bridge,codex,terminal,gui
- tags: mcp,agreement,llm,provider,consent,privacy,identity

## Porter
- G1: godkjent 2026-11-21 (Kjetil i tråden 21:23Z, «G1 godkjent»; forslagene i §6 gjelder)
- G1-GUI: godkjent 2026-11-23 (Kjetil i tråden 12:34Z, «G1-GUI godkjent»; åtte bilder i images/)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
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
