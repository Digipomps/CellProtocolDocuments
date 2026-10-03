# STATUS — lister celle og komponent

- surfaces: binding, cell, gui, porthole, skeleton, web
- tags: cell, gui, lister, parity, skeleton

## Porter
- G1: godkjent 2026-10-02 (Kjetils ord, valgknapp i chatten: «G1 og G1-GUI godkjent»; FORMAALSSPEC revisjon 2)
- G1-GUI: godkjent 2026-10-02 (samme ord; referanse = de åtte `images/*-v1.png`, rendret med web-rendereren fra `skeleton/`)
- G2: venter        (PLAN.md skrevet 2026-10-02 med 8 pakker + «Dette skal du gjøre»; ett spørsmål A/B om ComponentActionContext i CellBase; venter på Kjetils ord)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-02: G1 og G1-GUI godkjent av Kjetil (valgknapp «G1 og G1-GUI godkjent»). PLAN.md (P2), dataflow.md, contract/ (kontrakt v0 + 18 fixtures + validator, GRØNN i skyen) og images/plan-v1.png skrevet. Venter på G2.
- 2026-10-02: opprettet
- 2026-10-02: §6 besvart av Kjetil i chatten (valgknapper): 1 piler + dra (pilene skjules der verten har `drag`), 2 CellProtocol `cell:///Lists`, 3 celle + konfig + tester i CellProtocol som én PR (meny i app/katalog som egen pakke etterpå), 4 idéer er vanlig liste i v1. FORMAALSSPEC iterasjon 2. Ingen port satt — venter på Kjetils ord for G1 og G1-GUI.
- 2026-10-02: FORMAALSSPEC iterasjon 1: §0 audit (21 rader, alle retrieved mot CellProtocol origin/main 253b4af og CellScaffold origin/main fdcfe7a5), §1 (15 noder + 3 antiformål), §2, §3 (15 rader), §5, §6 (4 spørsmål). Åtte referansebilder rendret i skyen med CellScaffolds skeleton-runtime.js (md5 i images/README.md) fra skeleton/*.json; oppførsel (5 handlinger) bekreftet i images/render-report.json. Funn underveis: webens produktvisning overstyrer `controlStyle: plain` (porthole-webo.css 4759); webens ikonkart mangler `circle`; Binding mangler både ComponentSurface-vertsadapter og drag-adapter (R6). Venter på G1, G1-GUI og svar på §6.

## Venter på Kjetil
- Ordet «G2 godkjent» (PLAN.md) og svar A/B på spørsmålet om `ComponentActionContext` i CellBase (PLAN.md øverst).
