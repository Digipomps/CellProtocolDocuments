# STATUS — ventende godkjenninger

- surfaces: cell, gui, scaffold, skeleton
- tags: approval, decision, deploy, workbench

## Porter
- G1: godkjent 2026-10-10 (Kjetil 18:10Z: «G1 og G1-GUI godkjent»)        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: godkjent 2026-10-10 (samme melding; v1-bildene)        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-10-10 (Kjetil 20:05Z: «auto»)        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-10: opprettet
- 2026-10-10: iterasjon 1 av FORMAALSSPEC og fire G1-GUI-bilder lagt fram for Kjetil i tråden «Ventende godkjenninger i arbeidsbenken»
- 2026-10-10 18:10Z: G1 og G1-GUI godkjent. De tre valgene i §6 ble ikke besvart; Claude går videre på de anbefalte (1a Oversikt/HD-0210, 2a Mac-skript kjører kommandoen, 3a ingen lenkeknapp) og sier det i tråden.
- 2026-10-10 20:05Z: G2 «auto». Stopp-reglene i PLAN.md gjelder (ingen endring av eksisterende tester uten spørsmål, rød port kjøres ikke på nytt uten ord, ingen merge/deploy/tag).
- 2026-10-10 20:15Z: CP draft #66 (urlKeypath, 6/6 fokusert). CS draft #315 (rad + web urlKeypath; på HD-0210). HAVEN-Deploy: tools/arbeidsbenk-speil/godkjenninger.py + tests/test_godkjenninger.py (7/7) + _handoff/GODKJENNINGER/forespoersler.json, ikke committet (mappen er usporet, eies av arbeidsbenk-speil-PDD-en). Skill haven-work-intake oppdatert og synket. Blokkert: CP-tag (Kjetil), Workbench-bro (agentd-bro-aarsak-jobbene), disk for CS-port.
