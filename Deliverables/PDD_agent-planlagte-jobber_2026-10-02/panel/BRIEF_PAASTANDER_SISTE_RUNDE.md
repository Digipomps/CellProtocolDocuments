# Brief til Fabel: stemmer påstandene om siste retterunde?

Dato: 03.10.2026. Du er uavhengig kontrollør. Du har ikke sett koden eller samtalen før.

`S` er `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad`.

## Hva dette er, og hva det ikke er

Koden for «planlagte jobber» i HAVEN Agent (trinn 1–3) er gransket flere ganger. Etter de to siste granskingene ble 17 punkter rettet (åtte i Swift, ni i Python). **De rettelsene er ikke gransket.** Losen har skrevet hva som ble gjort, og Kjetil skal lese det. Din oppgave er å kontrollere at det som står skrevet, er sant.

Dette er **ikke** en ny gransking på jakt etter forbedringer. Du skal ikke lete etter nye «bør». Finner du underveis noe som er galt på en måte som ville gitt feil oppførsel på Macen (ikke stil, ikke restvinduer på mikrosekunder), fører du det opp under en egen overskrift til slutt, kort.

## Det du kontrollerer

Pakken slik den ble levert, ligger utpakket i `S/work/kodepakke2/` (`LES_MEG.md`, `kode/`, `koe/`, `trinn3/`). PDD-dokumentene ligger i `S/pdd-cron/`. Statusfila slik den står på Macen, ligger i `S/work/STATUS-mac-1103Z.md`. De to granskingene rettelsene svarer på, er `S/pdd-cron/panel/FABEL_KODE_TRINN3_ETTERKONTROLL.md` (avsnittet «Nye funn som bør rettes», 8 punkter) og `S/pdd-cron/panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL3.md` (Bør 1–9). Koden før rettelsene ligger i `S/work/trinn3-foer-etterkontrollrettelser/` (Swift) og `S/work/korrespondanse_vakt.py.foer-etterkontroll3` og `S/work/test_korrespondanse_vakt.py.foer-etterkontroll3` (Python), så du kan lese forskjellen med `diff -u`.

For hver påstand under svarer du **holder**, **holder ikke** eller **kan ikke avgjøres her**, med belegg: fil og linje, eller kommandoen du kjørte og det den skrev.

### A. Swift (trinn 3)

Påstandene står i `S/pdd-cron/PLAN_VEDLEGG.md`, tabellen med åtte rader under «Fabels gransking av koden for trinn 3», og avsnittet etter tabellen. Kontroller hver rad mot `S/work/kodepakke2/trinn3/Sources/`, `Tests/`, `Docs/ScheduledEvents.md` og `S/pdd-cron/contract/trinn3-cron.md`. Særlig:

1. `BoundedProcessRunner` gir `notStarted` når oppgaven avbrytes før programmet finnes (tre steder), og `interrupted` bare når programmet ble startet. Ingen loggfil i de to første tilfellene; i det tredje kan den stå tom.
2. Arbeideren (`runEvent`) gir tidspunktet tilbake ved `notStarted`: posten blir som før tidspunktet ble tatt, og et stopp som en annen prosess har skrevet i mellomtiden, beholdes.
3. «Tre skrivinger som feiler på rad»: kodekommentaren, dokumentet og kontrakten sier det telleren `failedWrites` faktisk gjør.
4. Første kjøring på intervall tar det siste tidspunktet på intervallet som er kommet, regnet fra `firstFireAt`, og teller ingenting. Senere kjøringer er uendret.
5. `lastOutcome` og `attention.kind` er lukkede mengder: kontrakten og dokumentet sier det, og oppførselen er den de beskriver (arbeideren nekter å starte; en arbeider som går, skriver fila på nytt fra minnet; `schedule-list` og `schedule-stop` nekter og skriver ikke over).
6. `ScheduledEventError.stateFileUnreadable`: kastes fra `start` bare ved dekodingsfeil, nevner filstien og at fila må flyttes til side; arbeiderlåsen slippes; fila røres ikke.
7. Avsnittet «When the state file cannot be read» i `Docs/ScheduledEvents.md`: **hver** setning og hvert punkt i lista er sant for koden.
8. «En stoppet hendelse ber ikke om noe»: gjelder alle veier (`stopEvent` i fila og i minnet, flettingen i `persist`, tilbakegivingen, `recoverInterruptedRun`, `attention(for:)`), og `lastOutcome` og `lastError` står.
9. Kontrakten har regelen om første tegn i en id, og dokumentet sier «an error without `cron`».
10. **71 tester er grønne.** Bygg og kjør selv, fra pakken, i ditt eget byggetre:
    `TRINN3_KILDE=S/work/kodepakke2/trinn3 TRINN3_TRE=fabel-paastander S/trinn3/sky/bygg.sh trinn3` (bytt `S` med hele stien). Det lager `S/trinn3-bygg-fabel-paastander/`; den mappen er din. Første bygg tar et par minutter. Kjør testene to ganger. Verktøykjeden er Swift 6.2.3 fra Ubuntu-arkivet (`S/swift-tc/env.sh`); `bygg.sh` setter den opp selv.
11. **Mutasjonsprøven gir sju røde av sju.** Skriptet `trinn3/sky/mutasjon.py` regner stier fra der det ligger, og det bygger i treet `trinn3-bygg-mutasjon`, som er Losens. Gjør derfor slik: kopier `S/work/kodepakke2/trinn3/` til `S/fabel-paastander/trinn3/`, og endre i **din kopi** av `mutasjon.py` den ene linja som setter `TRINN3_TRE="mutasjon"`, til `TRINN3_TRE="fabel-mutasjon"`. Da havner kopiene og loggene i `S/fabel-paastander/work/mutasjon/` og bygget i `S/trinn3-bygg-fabel-mutasjon/`. Kjør `python3 -B S/fabel-paastander/trinn3/sky/mutasjon.py`. Les minst tre av loggene, og si om testene feiler på den forventningen som hører til rettelsen, eller av en annen grunn.
12. De to patchene i `trinn3/patcher/` legger seg rent på filene fra `main`, som ligger i `/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/` (prøv i en kopi i din mappe).

### B. Python (trinn 1 og 2)

Påstandene står i `S/pdd-cron/PLAN_VEDLEGG.md`, tabellen med ni rader (Bør 1–9) under «Fabels gransking av koden for trinn 1 og 2», og avsnittet etter den. Kontroller hver rad mot `S/work/kodepakke2/kode/Scripts/scheduled/korrespondanse_vakt.py`, `kode/Tests/scheduled/test_korrespondanse_vakt.py`, `kode/Docs/ScheduledEvents.md` og `S/pdd-cron/contract/trinn1-2-programmer.md`. I tillegg:

13. Selvtesten gir `SELVTEST OK 126 kontroller` (kjør den fra `kode/` med `python3 -B`).
14. Hele testmengden gir 42 tester OK. Kjør den én gang på én Python-versjon (den tar omtrent fem minutter): fra en **kopi** av `kode/` i din mappe, `python3 -B -m unittest discover -s Tests/scheduled -p "test_*.py"`.
15. Sjekksummene i `LES_MEG.md` og i `koe/korrespondansevakt.sh` er sjekksummene til filene i `kode/Scripts/`.

### C. Dokumentene Kjetil leser

16. `S/work/STATUS-mac-1103Z.md`: de seks loggpunktene datert 2026-10-03 fra «ca. 09:30Z–10:15Z» og ut, og avsnittet «Valg Losen har tatt i koden». Er tallene og påstandene sanne? (Det som gjelder Macen selv — ledig disk, hvor filer ligger der — kan du ikke kontrollere; si det.)
17. `S/work/kodepakke2/LES_MEG.md`: filtabellene, MD5 av grunnlaget (regn dem ut fra `main`-kopien over), og avsnittene «Slik er det prøvd» og «Det som ikke er bevist». Er noe utelatt fra «ikke bevist» som burde stått der?
18. `S/pdd-cron/handoff/README.md`: avsnittet «Koden for S3 er skrevet» med filtabellen.

## Grenser

- Du kan lese alt som er nevnt. Egne filer legger du i `S/fabel-paastander/` (mappen finnes). Du kan bygge i `S/trinn3-bygg-fabel-paastander/` og i ett byggetre til med et navn du velger selv som begynner med `trinn3-bygg-fabel-`.
- Du skal ikke endre eller slette noe i `S/work/`, `S/trinn3/`, `S/impl/`, `S/koe/`, `S/pdd-cron/` eller Losens byggetrær (`S/trinn3-bygg-trinn3`, `-mutasjon`, `-grunnlinje`, `-bygg0`), med ett unntak: rapportfila.
- Bruk `python3 -B`, så det ikke legges `__pycache__` noe sted.
- Ingen verktøy som når Macen (`mcp__remote-devices__*`), ingen korrespondanseverktøy, ingen nettleser, ingen meldinger til noen. Ikke hent noe fra nettet.
- Mappen `S/pdd-cron/panel/kilder-utdrag/` skal du ikke lese eller sitere fra.

## Rapporten

Skriv `S/pdd-cron/panel/FABEL_PAASTANDER_SISTE_RUNDE.md` på norsk bokmål:

1. Én setning først: holder det som står skrevet, ja eller nei.
2. En tabell med de 18 punktene: nummer, dom, belegg (fil og linje, eller kommando og utdata).
3. «Påstander som ikke holder»: for hver, hva som står, hva som er sant, og hvor det står (fil og linje), så det kan rettes.
4. «Feil som ville gitt gal oppførsel på Macen» (bare hvis du fant noen).
5. «Ikke kontrollert»: det du ikke kunne avgjøre her, og hvorfor.

Svar meg til slutt med de samme fem delene i kortform.
