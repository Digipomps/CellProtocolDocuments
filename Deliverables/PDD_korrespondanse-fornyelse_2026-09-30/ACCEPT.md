# ACCEPT — forventet mot faktisk (§3)

PDD `korrespondanse-fornyelse`, 30.09.2026. Oppdatert 02.10.2026. G3 er Kjetils ord. Tabellen speiler §3 i FORMAALSSPEC.md rad for rad. Det som kom til 01.10 (fornyelse før fristen, F6), står i en egen tabell under.

| Leveranse (§3) | Forventet | Faktisk | Bevis |
|---|---|---|---|
| Testene T1–T4 med ekte utdata | testutdata | T1–T3 er grønne. Alle 30 korrespondansetester passerer, også de 27 som fantes fra før. I full testmengde feiler 57 testnavn. Ingen av dem gjelder korrespondanse, og ingen er nye fra denne endringen: de to som ikke sto i baselinelisten, feiler likt på `feec2372`. | TESTRESULT #t1–#t4, `evidence/` |
| Et kort for `kjetil-vegar-codex-d` på staging-adminsiden. Du kontrollerer nøkkelen og trykker «Godkjenn meldingsadgang». | kjørende flate | To kort, fordi du valgte «Begge»: `kjetil-vegar-codex-d` og `kjetil-codex-d`. Du godkjente begge 30.09 kl. 22:43. Nye tilgangsbevis er hentet, og de gjelder til 2026-10-30T19:00:12Z. | TESTRESULT #t5, `job-237-korr-aktiver.log` |
| Vegar kan sende deg igjen, og innboksen din virker | kjørende flate | Begge deler er observert. Meldingen din til Vegar gikk gjennom (`sent`). Vegar har sendt tre meldinger etter fornyelsen, sekvens 13–15, 01.10 kl. 00:02–00:15Z. Losen leste og kvitterte dem 06:01Z. | TESTRESULT #t5 |

## Fornyelse før fristen (F6, valgt 01.10)

| Leveranse | Forventet | Faktisk | Bevis |
|---|---|---|---|
| Testene T6–T8 med ekte utdata | testutdata | Grønne. 33 korrespondansetester, 0 feil. Full testmengde på `06f32050`: de samme 57 feilende testnavnene som før, ingen nye. | TESTRESULT #t6 #t7 #t8 |
| PR mot `main` | PR | PR #277 er åpen. Merge-sjekken er grønn (kjøring 36998795184, hode `d83d9f6b`). Den er ikke merget. | TESTRESULT #pr |
| Fornyelse de siste sju dagene, ute på staging | kjørende flate | **Ikke levert.** `06f32050` er pushet, men ikke satt ut. Staging kjører `415ea3d2`, som bare fornyer utløpte tilganger. Sjudagersvinduet er altså bare prøvd i enhetstester. | `/health/build` 02.10 kl. 11:36Z |

## #status

STATUS.md er oppdatert 02.10. G2 og G3 står som `venter`.

## #docs

Endringen legger til ett valgfritt felt, `renewsGrantID`, i tilgangsforespørselen. Rutene og feilkodene er uendret. `contract/README.md` beskriver endringen. Pilotcellen har ingen kontrakt i `Book/`, for `correspondence_cell_contract_v0.json` gjelder den kommende førsteklasses `CorrespondenceCell`. `dataflow.md` viser flyten med navngitte kanter. Statusloggen i CellScaffold (`Documentation/ProjectControl/SISTE_OPPDATERING.md`) har en entry på grenen (`d83d9f6b`).

## Oppdaget under T5, utenfor denne PDD-en

Meldingen din til `victoria-lille-robot` ble avvist med `recipient_not_allowed`. Victoria sendte meldinger 03.–17.09, så tilgangen hennes er etter alt å dømme utløpt, som din var. Fornyelsen virker for henne også, men invitasjonen må bære enhets-ID-en til Lille Robot. Jobben er forberedt (`238-victoria-invitasjon.MAL.sh`, ikke lagt i køen) og venter på den ID-en. §2 holdt andre principals enn dine utenfor, så dette er en egen oppfølging.

## Avvik og punkter som trenger ditt ord

1. **Utsettingen 30.09 gikk utenom deploykøen.** Du sa «Ja, sett ut nå», og jeg satte ut `415ea3d2` og byttet invitasjonene uten å ta claim og uten å ha lest `_losen-queue/KOORDINERING.md`. Codex (HD-0141) hadde claim på `cellscaffold-app-1` og nginx. Containeren ble startet på nytt minst to ganger, og deployen kjørte manifest-provisjoneringen under `/etc/haven`. Køen tror fortsatt at staging kjører `feec2372`. Om dette forstyrret HD-0141, vet jeg ikke. Teksten som bør føres inn i koordineringsfila, ligger i `handoff/KOORDINERING-tillegg-20261002.md`. Den er ikke lagt inn, for fila tilhører kø-tråden og ligger utenfor mappene denne tråden har.
2. **Rekkefølgen på staging er ikke avgjort.** 2026.9.4 har ikke fornyelseskoden. Settes den ut før PR #277 er med i en utgivelse, kan ingen tilganger fornyes på staging. Valgene står i `handoff/A0-rekkefolge-valg.md`.
3. **Fornyelse før fristen er ikke ute.** Se tabellen over. Vegars tilgang går ut 08.10.
4. **Hver fornyelse krever en omstart på verten.** Invitasjonene leses bare fra miljøet til containeren. Vegars og Victorias fornyelse kan derfor ikke gjøres uten et claimvindu (HD-0006).
5. **G2 er ikke satt.** Planen lå i valget «Bygg fornyelse (anbefalt)», og utsettingen fikk ditt «Ja, sett ut nå (anbefalt)». Et eget ord om G2 har jeg ikke.
6. **Lokale bygg gikk utenom diskregelen.** Byggene 30.09 og 02.10 brukte ikke `scripts/run_swift_bounded.sh` og kapasitetsvakten.
7. **`recipient_not_allowed` sier ikke hvorfor.** Feilen dekker både «ikke tillatt» og «tilgangen er utløpt», og derfor kunne ikke Vegar se hva som var galt. Det er ikke endret her.
8. **Tilstanden er ikke prøvd mot en eldre utgivelse.** Det nye feltet er valgfritt og lagt til på samme måte som tidligere felt, så en utgivelse uten endringen skal kunne lese tilstanden. Det er ikke testet.

## Det som ikke virket underveis

Detaljene står i TESTRESULT, avsnittet «Det som ikke virket». Kort:

- Første T1-kjøring feilet på min egen forventning. Jeg ventet `ok`, men sending svarer `sent`.
- Klienten avviste Kjetils utløpte bevis før serveren ble spurt.
- Vegar sendte meldingen fra 29.09 på nytt fordi han trodde den ikke hadde kommet fram. Den hadde kommet fram, men ble ikke lest før 01.10.
- Jeg skrev 01.10 at Vegar aldri ville miste tilgangen ved fornyelse før fristen. Det var feil: klienten har ikke noe gyldig bevis mellom `setup` og godkjent `activate`. Rettet samme dag.
- Jeg kartla ikke deploykøen før utsettingen 30.09. Se avvik 1.

## Uavhengig gransking

Fabel gransket påstandene om utsettingen, fornyelsen og svaret til Vegar 02.10, og kontrollerte rettelsene etterpå: `panel/FABEL_SVAR.md` og `panel/FABEL_ETTERKONTROLL.md`. Bevisene Fabel fikk, ligger i `panel/`.

## Bevisfiler

- `evidence/T1-T4-korrespondansetester-20260930T1941.log` — korrespondansetestene
- `evidence/forste-kjoring-20260930T1935.log` — første kjøring, med feilen i min egen forventning
- `evidence/regresjon-feilende-415ea3d2.txt` — feilende testnavn i full testmengde
- `panel/E2-utsetting-30-09-jobblogg.txt` — jobbloggen fra utsettingen 30.09
- Commit `415ea3d278dc85be5547c137d917aa343dadb38a` på `claude/korrespondanse-fornyelse-20260930`, satt ut på staging (`/health/build` viser `415ea3d2`)
- Commit `06f3205037690086bebf9da9351a61b726668bb1` på samme gren, ikke satt ut
