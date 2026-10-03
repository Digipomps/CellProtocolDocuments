# Brief til Fabel: etterkontroll av rettelsene i koden for trinn 3

Dato: 03.10.2026. Du har ikke sett dette før. Gransk som uavhengig kodegransker, og ta ikke mine konklusjoner for gitt.

Alt ligger under `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/` (heretter `S/`).

## Bakgrunn

Koden for trinn 3 (cron og planleggeren i HavenAgentD) ligger i `S/trinn3/`. Hva filene er, hvor grunnlaget fra `origin/main` ligger, kontrakten, og hvordan det bygges her, står i `S/pdd-cron/panel/BRIEF_KODE_TRINN3.md`. Les den først.

En første gransking ga rapporten `S/pdd-cron/panel/FABEL_KODE_TRINN3.md`: tre feil som måtte rettes, og femten som burde. Rettelsene er gjort. Hva som ble gjort med hvert punkt, står i tabellen «Fabels gransking av koden for trinn 3» nederst i `S/pdd-cron/PLAN_VEDLEGG.md`. Koden slik den var før rettelsene, ligger i `S/work/trinn3-foer-fabelrettelser/` (`Sources/`, `Tests/`, `Docs/`, `patcher/`), så du kan se nøyaktig hva som er endret:

```
diff -ru S/work/trinn3-foer-fabelrettelser/Sources S/trinn3/Sources
diff -ru S/work/trinn3-foer-fabelrettelser/Tests S/trinn3/Tests
```

Testene den første granskeren skrev, ligger i `S/fabel-trinn3/kopi/Tests/HavenAgentRuntimeTests/Fabel*.swift`. Bruk dem gjerne, men i din egen mappe.

## Det jeg ber om

1. **Er de tre «må rettes» lukket?** (a) Stoppes arbeideren midt i en runde, skal neste forfalte hendelse stå som forfalt, ikke bli startet og drept. (b) Blir tilstandsfila uleselig mens arbeideren går, skal arbeideren komme seg videre, og en arbeider som ikke kan skrive, skal ikke se levende ut. (c) Første kjøring av en hendelse på intervall skal ikke telle noe som passert. Prøv hver av dem selv, ikke bare med testene som følger med.
2. **Har rettelsene åpnet noe nytt?** Se særlig på: veien der et tidspunkt gis tilbake fordi oppgaven ble avbrutt mens det ble skrevet (`runEvent`); `runDueEvents` når fila ikke kan leses, og `ScheduledEventStore.update(replacingUnreadableFile:)` (kan en fil som bare er midlertidig uleselig, eller halvskrevet av noe annet, bli overskrevet med mindre enn den hadde? hva med `schedule-stop` i samme øyeblikk?); `adopt` som nå bringer poster uten `countingFrom` i takt og lagrer; `stopEvent`; `recoverInterruptedRun` for en stoppet post; `holdHeartbeat` (kan livstegnet bli stående holdt tilbake etter at skrivingen virker igjen?); `BoundedProcessRunner` med alle signaler satt til standard (er `sigfillset`-veien riktig på Darwin og løkka riktig på Linux?), vakten mot prosess-ID 1 og lavere, og den siste `SIGKILL` som nå bare sendes når gruppen står.
3. **«Bør rettes» 1–14:** er hvert punkt gjort slik tabellen sier, og er det gjort riktig?
4. **De nye testene** (i `S/trinn3/Tests/`, 65 i alt): prøver de det de sier, kan noen gå grønt av feil grunn, og kan noen vakle på en treg eller travel maskin?
5. **Kontrakten og dokumentet** (`S/pdd-cron/contract/trinn3-cron.md`, `S/trinn3/Docs/ScheduledEvents.md`): sier de nå det koden gjør, verken mer eller mindre?

Bygg og kjør i din egen mappe `S/fabel-trinn3-etterkontroll/` (lag den; kopier `S/trinn3-bygg-trinn3/` dit, gjerne uten `.build`):

```
. S/swift-tc/env.sh
cd S/fabel-trinn3-etterkontroll/<kopien> && swift test --no-parallel -Xswiftc -Xfrontend -Xswiftc -disable-cross-import-overlays
```

## Slik svarer du

Skriv til `S/pdd-cron/panel/FABEL_KODE_TRINN3_ETTERKONTROLL.md`, på norsk: en tabell over de tre «må» og de femten «bør» med «lukket», «delvis» eller «ikke lukket» og hvordan du prøvde det; deretter **Nye funn som må rettes**, **Nye funn som bør rettes**, **Kontrollert og funnet i orden**, **Ikke kontrollert**. Vis til linjer, og vis hvordan du har prøvd det du påstår.

Grenser: du kan lese alt som er nevnt, og bygge og kjøre i din egen mappe. Du skal ikke endre noe i `S/trinn3/`, `S/impl/`, `S/koe/`, `S/work/`, `S/pdd-cron/` (utenom rapportfila), `S/fabel-trinn3/` eller byggemappene `S/trinn3-bygg-*`. Ingen montering av filsystemer. Ingen verktøy som når Macen, nettlesere, korrespondanse eller andre tjenester, ingen nedlasting fra nettet, og ingen meldinger til noen. Ingen private detaljer fra `S/pdd-cron/panel/kilder-utdrag/` i rapporten.

Svaret ditt til meg skal være kortversjonen: status for de tre «må», hvert nytt «må rettes» på én linje med fil og linje, og antallet nye «bør rettes» med stikkord.
