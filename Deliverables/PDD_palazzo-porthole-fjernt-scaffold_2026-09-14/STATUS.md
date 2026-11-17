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
- 2026-09-14, WP5: brotesten bruker ekte CellResolver/BridgeBase og uendret Palazzo-eksport med probe-publisist. En felles test av de to App-modulene ville kreve ny pakkekobling; denne ble ikke innført. Virkelig Palazzo-app-integrasjon er derfor uverifisert, og G3 holdes ventende. Baseline-feilen i Conference Participant Portal-dokumentasjon beholdes utenfor slicen.

## Logg
- 2026-09-14: opprettet etter at run-g5.sh feilet i steg 4 (Porthole addConfiguration 400). Årsak lest i CellScaffold (FORMAALSSPEC §0). G1/G2 på Kjetils ord samme dag. Codex-jobb `pz1-porthole-fjernt-scaffold-20260914` lagt i _losen-queue (workspace-write, cwd HAVEN-rot). Kjetil kjører run-g5.sh på nytt når jobben er ferdig.

- 2026-09-14, Astra (Codex), WP0–WP5: **skrevet, verifisert med avgrenset test**. Før/gjentatt før: bygg pass, 121 tester, 2 hoppet over, 1 identisk feil. Etter: bygg pass, 129 tester, 2 hoppet over, samme feil; 8/8 nye tester pass. Fjernoppslag med keypath, trust, referanseomskriving, allowlist og de tre pålagte preview-kommandoene er skrevet. Offline preview-kontrakt, node --check og bash -n pass. TESTRESULT.md, ACCEPT.md og evidence/files.json finnes. Palazzo-app/G5/parity uverifisert; WP6 hos Kjetil, WP7 urørt. Ingen git, nettverk, CellProtocol-endring eller svekkelse av eksisterende tester.
