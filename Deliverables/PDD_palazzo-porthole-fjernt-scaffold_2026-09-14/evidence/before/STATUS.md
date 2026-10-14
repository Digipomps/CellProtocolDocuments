# STATUS — palazzo porthole fjernt scaffold

- surfaces: bridge, cell, codex, porthole, scaffold
- tags: bridge, palazzo, porthole, scaffold
- HAVEN-Deploy: HD-0078

## Porter
- G1: godkjent 2026-09-14 (Kjetil: «Ja - men siden vi nå kjører i et eget scaffold kan vi flytte eventuelle https kall dit …»; presiseringen ligger i FORMAALSSPEC §2)
- G1-GUI: godkjent 2026-09-07 (arvet — samme tre Sicilia-flater; referansebildene kopiert til images/, se images/README.md)
- G2: godkjent 2026-09-14 (auto — Kjetil: «Kjør i gang Codex astra på dette så ser vi hvor langt vi kommer»)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne; test.g5 kjøres av Kjetil)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-14: opprettet etter at run-g5.sh feilet i steg 4 (Porthole addConfiguration 400). Årsak lest i CellScaffold (FORMAALSSPEC §0). G1/G2 på Kjetils ord samme dag. Codex-jobb `pz1-porthole-fjernt-scaffold-20260914` lagt i _losen-queue (workspace-write, cwd HAVEN-rot). Kjetil kjører run-g5.sh på nytt når jobben er ferdig.
