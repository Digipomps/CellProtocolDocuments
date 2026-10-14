# Uavhengig kontroll av lokale testpakker

2026-10-13. Utført av `continuation_packet_review`, uavhengig av pakkeutformingen. Ingen blokkerende funn i de kontrollerte pakkene. Dette er kontroll av testopplegget, ikke et grønt Swift-resultat eller en aktivering.

## Frosne innganger

Stier nedenfor er relative til HAVEN-roten.

| Pakke | SHA-256 av manifest.json |
| --- | --- |
| `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CONTINUE-20261013` | `9c481f32f273cd928a09eca02fd54073f2091fb591589ed78e220af4524ce469` |
| `HAVEN-Deploy/_handoff/ARBEIDSBENK/PROJECT-WORKSPACE-BASELINE-20261013` | `09bdf3184388a5a9558312aa532db1fd7b1d8a78cf8ad6337e5e1093e63ed191` |

Begge pakkers `check` bestod. Kilde-/skripthashene, Git-revisjoner og arbeidsstatus stemte. Ingen av pakkene hadde ADMISSION.json, AUTHORIZATION.json, attempt-started eller result.json ved kontrollen. Alle manifestførte innfiler og køens refererte skript/prompt finnes; kjøringslogger og resultater er framtidige utdata.

CP-fortsettelsen beholder identiske produkt-/testinnganger, pins og 8 + 17 metoder fra den opprinnelige pakken. Originalresultatet er uendret: CP-prosess 0, åtte beståtte tester, null feil, deretter stopp på feilaktig loggtolkning før CS17. Ny kjøring krever egen manifestbundet brukergodkjenning og køeiers ferske adgang; prosjekt-G2 brukes ikke som nytt CP-ja.

Prosjektbaselinen binder ren CellScaffold `3a6680446e55fc1644afb368ac2bf48dd0720e30`, godkjent G2 og publisert CP `b4100f5734bb0b3781600845a267e424e55c0989`. Det statisk avleste inventaret i de fem testfilene stemmer eksakt med manifestets 112 metoder. Dette er ikke runtime-discovery eller bevis for den nye prosjektflatens oppførsel.

## Faktisk kontroll

- 19 parser-fixtures bestod, inkludert original grønn CP-logg med forventede avvisningsmeldinger, interleavet produktprefiks, feil rekkefølge, tester utenfor bundle, duplikater, feil prosesskode, manglende suiter og compilerfeil.
- Fem prosesskontroll-fixtures bestod: exitstatus, timeout, avbrudd ved spawn, barnets signalmaske og gjentatte signaler under gjenoppretting.
- Begge pakker bruker byte-identiske parser-/prosessmoduler. `owned_process.py`, `child_exec.py` og `xctest_receipts.py` er byte-identiske med `AUDIT-CP-20261012-R1`.
- Hele de aktuelle runnerne, parserne og prosesshjelperne ble lest. Manifest-/README-/job/prompt-filer og relevante bounded-runner-seksjoner ble kontrollert. Testkildene ble kontrollert som metodeinventar, ikke funksjonelt revidert i sin helhet.

Parserendringen følger den dokumenterte interleaving-fallgruven i `CellScaffold/.claude/skills/cellprotocol-contract-testing/SKILL.md`: komplette start-/terminalpar må ligge i avsluttede top-level bundles; kolonne-null er ikke et krav for case-records. Eksakte manifesttall og nestede suitekvitteringer beholdes. Tekstlig avstemming autentiserer ikke logger fra et fiendtlig program.

## Aktiveringsgrenser

Fersk eksklusiv køadgang og kapasitet må bestå før én-gangsmarkøren opprettes. Begge pakker bruker to Swift-jobber, administrert cache, 10 GiB reserve og 40 GiB/10 prosent gulv. Report-only GC sletter ikke byggcacher. Gruppebevis må foreligge før pins gjenopprettes; SIGKILL, strømbrudd og prosesser som etablerer ny session er ikke dekket av dette beviset. Rødt stopper uten automatisk omkjøring.

Prosjektbaselinen kan legges i avtalt vindu under eksisterende G2. CP-fortsettelsen venter på Kjetils uttrykkelige ja til nytt forsøk. Køeier må få de to endelige manifesthashene og beholder kontroll over rekkefølge og aktivering. Ingen Swift, betalt CI, Git-publisering eller deploy ble kjørt under denne kontrollen. Foreldretråden håndterer avsluttende macOS-tolokale-kontroll og læringsfangst separat.
