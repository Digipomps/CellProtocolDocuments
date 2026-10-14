# Brief til Fabel: gransk koden for trinn 1 og 2

Dato: 02.10.2026, natt. Koden for korrespondansevakten er skrevet og testet i skyen mens G2 venter. Ingenting er lagt på Macen eller i noe repo. Gransk den som en uavhengig kodegransker før den legges fram.

## Hva som finnes

Mappen `impl/` ligger ved siden av `pdd-cron/`:
`/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/impl/`

| Fil | Hva |
|---|---|
| `Scripts/scheduled/korrespondanse_vakt.py` | programmet: `sjekk`, `frist`, `selvtest` |
| `Scripts/install-scheduled-tasks.sh` | inngangen (bash 3.2) |
| `Scripts/scheduled/installer.py` | installasjonsrutinen: `toerr`, `utfoer`, `fjern` |
| `Tests/scheduled/test_korrespondanse_vakt.py`, `test_installer.py`, `fixtures/` | testene |
| `Contracts/scheduled-task-stamp-v1.schema.json`, `.example.json`, `README.md` | stempelet |
| `Docs/ScheduledEvents.md`, `Docs/OperatorRunbook.md` | dokumentasjonen (tillegg til filene på `origin/main`) |

Omslaget for køen ligger i `scratchpad/koe/korrespondansevakt.sh` (laget av `lag_omslag.py`).

Kontrakten er `pdd-cron/contract/trinn1-2-programmer.md` (oppdatert etter at koden ble skrevet; utgaven fra før ligger som `.foer-implementasjon`) og `pdd-cron/handoff/README.md` S1–S2. Kildene er der de lå: pilotklienten i `pdd-cron/panel/kilder-utdrag/`, agenten under `/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/`, køene under `/mnt/user-data/uploads/HAVEN/`.

Testene er kjørt slik, og var grønne (26 tester) på 3.9, 3.11 og 3.13:

```
cd impl && /root/.local/bin/python3.9 -m unittest discover -s Tests/scheduled -p "test_*.py"
/root/.local/bin/python3.9 Scripts/scheduled/korrespondanse_vakt.py selvtest
```

Macen har `/usr/bin/python3` 3.9.6 og bash 3.2. Programmet startes av planleggeren under launchd (`ScheduledEventService.swift`, `SubprocessRunner.swift`), som ikke har tidsgrense og leser utdata først når programmet er ferdig.

## Det jeg ber om

1. **Feil som kan henge planleggeren eller gi feil sak.** Les `korrespondanse_vakt.py` mot kontrakten og mot planleggerens kilde. Let etter: veier der programmet kan bruke mer enn 60 sekunder; barneprosesser som kan overleve; utdata over én linje; kappløp mellom vakttråden og hovedløpet; markører som kan bli fjernet når profilen ikke ble lest; markører som kan gjøre agentens kilde ulesbar (se `CorrespondenceWaiting.swift` og `AgentChallenge.swift`); tekst som kan bære en ID inn i noe som vises.
2. **Protokollen mot pilotklienten.** Stemmer `Client`, `_find_tool`, `_page` og `read_inbox` med `pilotklient-CorrespondenceMCPProtocol.txt` og `pilotklient-service-contracts-client-utdrag.txt`? Hva skjer hvis klienten spør nøkkelringen og blir stående?
3. **Installasjonen.** Kan `installer.py` skade `config.json` (tap av nøkler, feil rettigheter, halvskrevet fil), skrive ut tokenet, eller legge inn noe annet enn tørrkjøringen viste? Er bindingen med `HAVEN_FORVENTET_CONFIG_SHA256` tett? Hva skjer i `fjern` hvis planleggeren kjører en av oppgavene? Stemmer `build_addition` med `contract/config-tillegg-trinn1-2.json`? Er omslaget riktig for `_losen-queue/runner.sh` (modus `skript`)?
4. **macOS og Python 3.9.6.** Noe som virker på Linux og Python 3.9.23 her, men ikke der: `ps -o stat=`, `os.killpg` mot en gruppe som er borte, `select` på rør, `signal.alarm` sammen med tråder, `/bin/sh`-omslaget i selvtesten, stier med mellomrom («Application Support»).
5. **Testene.** Hva er ikke prøvd som burde vært det? Kjør gjerne testene selv, og prøv egne tilfeller mot programmet i en midlertidig mappe.
6. **Dokumentasjonen.** Sier `Docs/ScheduledEvents.md` og tillegget i `Docs/OperatorRunbook.md` noe koden ikke gjør?

## Slik svarer du

Skriv til `pdd-cron/panel/FABEL_KODE_TRINN1-2.md`, på norsk. Del den slik: **Må rettes før installasjon** (nummerert, med fil, linje, hva som skjer, og hva som bør stå), **Bør rettes**, **Kontrollert og funnet i orden** (kort liste), **Ikke kontrollert** (det som bare kan måles på Macen). Vær konkret: vis til linjer, og vis hvordan du har prøvd det du påstår.

Grenser: du kan lese alt og kjøre programmene og testene. Du kan opprette filer i midlertidige mapper under `/tmp`. Du skal ikke endre filene i `impl/`, `koe/` eller `pdd-cron/`, utenom rapportfila. Ingen verktøy som når Macen, nettlesere, korrespondanse eller andre tjenester, og ingen meldinger til noen. Ingen private detaljer fra `panel/kilder-utdrag/` i rapporten.

Svaret ditt til meg skal være kortversjonen: hvert «må rettes» på én linje, og antallet «bør rettes».
