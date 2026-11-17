# Oppdrag: uavhengig kontroll av fornyelsen av korrespondansetilgang (HD-0006)

Du er en uavhengig kontrollør. Jeg (en annen Claude-tråd) har skrevet skript og trukket konklusjoner som en eier skal handle på. Jobben din er å finne det som er galt, ikke å bekrefte. En konklusjon som ikke tåler kilden, skal felles, også når den er min.

## Hva det gjelder

To personer, Vegar og Victoria, har hver en lokal klient (`haven-correspondence-mcp`, «pilotklienten», skjema 1) som er meldt inn hos en tjener (staging). Tilgangen til Vegar går ut 08.10.2026. Victorias gikk ut 29.09.2026. Eieren, Kjetil, skrev 05.10: «Bygg en ny universal installerer om det trengs - men DET MÅ VIRKE! - før jeg sender dem en ny installerer».

Jeg har konkludert med at ingen ny installerer trengs: mottakerne fornyer med klienten de har, en fersk invitasjon og én fil, `forny-haven-tilgang.sh`. Før noe sendes, skal det prøves på to prøveidentiteter (`sim-a`, `sim-b`) på Kjetils Mac mot staging. Ingenting er kjørt ennå, verken mot staging eller på macOS.

Det som står på spill: en mottaker som kjører noe som låser profilen sin, en eier som bruker godkjenninger og en omstart av staging på en prøve som feiler av en grunn jeg kunne sett, eller en melding til mottakerne med en oppskrift som ikke virker.

## Regler

- Du leser bare. Alt du trenger, ligger i denne mappen: `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/fabel-hd0006/`.
- Du skriver bare i undermappen `arbeid/`. Rapporten din er `arbeid/rapport.md`. Vil du kjøre skript eller tester, kopierer du dem til `arbeid/` først og kjører dem der, med `TMPDIR` satt til en mappe under `arbeid/`.
- Ikke bruk verktøy som heter `mcp__remote-devices__*`, ingen korrespondanseverktøy, ingen nettleser, ingen meldinger, ikke noe nett. Ikke les utenfor denne mappen, bortsett fra `/root/.local/bin/python3.9` (Python 3.9, samme versjon som `/usr/bin/python3` på Macen) når du kjører tester.
- Skriv ikke lange tilfeldige strenger (nøkler, koder, ID-er) inn i rapporten. Pek på fil og linje i stedet.
- Skriv rapporten på norsk bokmål.

## Det du har

- `kilder/tjener-e5c3434/`: tjenerens celle, kontrakter og HTTP-lag slik de står på staging (CellScaffold `e5c3434`, utgivelsen 2026.9.5).
- `kilder/klient-e88a697/`: pilotklienten ved revisjonen manifestet i pakken Vegar fikk 08.09, oppgir. `kilder/klient-401f1b21/`: samme filer ved revisjonen en pakke fra 10.08 ble bygget fra. `AgentIdentityStore.swift` er der nøkkelen holdes.
- `kilder/generator/`: skriptet som lager invitasjoner.
- `kilder/hd/`: `hdlib` (`cli.py`, `core.py`, `locking.py`) og `vert.sh`, som `bytt-invitasjoner.sh` bruker.
- `kilder/maalt/LES-INSTALLERT-utdrag.md`: målt på Kjetils Mac 05.10 (klienten som er installert der, og de to pakkene).
- `kilder/sendt/`: det som fulgte pakken Vegar fikk (`Vegar-pakke-LES_MEG.md`, manifestet), og `PROVENANCE.md` for pakken fra 10.08.
- `skript/`: det som skal kontrolleres: `forny-haven-tilgang.sh` (det mottakerne får), `lag-invitasjoner.sh`, `proev-fornyelse.sh`, `bytt-invitasjoner.sh`, `LES-MEG.md`, og testene: `proeve/test_forny.py` med stedfortrederen `proeve/stub_klient2.py`, og `proeve-sky/test_proev.py`.

Det du ikke har, og derfor ikke kan avgjøre: innholdet i e-postene mottakerne fikk (jeg har lest et utkast fra 30.08 som sier at Victoria fikk «en pilotpakke, ikke en signert release», med kommandoen `haven-correspondence-mcp setup --invite …` og profilen `victoria`), verten, staging, og macOS selv. Si fra når et svar hviler på noe av dette.

## Del 1: svar fra kilden, før du leser konklusjonene mine

Les kildene i `kilder/` og svar på disse uten å se i `skript/LES-MEG.md` først. Oppgi fil og linje for hvert ledd.

1. En mottaker har en innmeldt profil. Eieren lager en fersk invitasjon for samme principal, uten enhets-ID. Hva skjer, ledd for ledd, hos klienten og hos tjeneren når mottakeren kjører `setup --invite <fila>` (a) med fila som den er, (b) etter å ha satt profilens enhets-ID inn i fila? Ta tre tilfeller: tilgangen er gått ut; den har tre døgn igjen; den har tjue døgn igjen. Hva skriver klienten til disk i hvert tilfelle, og når?
2. Fra `setup` er godtatt til eieren har bestemt seg: hva kan mottakeren gjøre med kanalen, med en klientprosess som alt kjører, og med en som startes på nytt? Hva skjer hvis eieren aldri svarer, og hvis eieren avslår? Kan samme invitasjon brukes en gang til?
3. Hva må være likt mellom tilgangen som finnes og den nye forespørselen for at tjeneren skal godta den? Finnes det noe tjeneren har lagret fra før, som kan stoppe en fornyelse selv om mottakeren gjør alt riktig?
4. Hva skriver klienten ut for `identity`, `setup` og `activate`, i hvilken form, og med hvilke avslutningskoder? Hvilke feller er det for et skallskript som skal lese status og enhets-ID ut av det?
5. Hvordan blir fila mottakeren laster ned fra onboarding-siden til: navn, form, hvilke felt, og hva med enhets-ID?
6. Hvilke forskjeller er det mellom de to klientrevisjonene, og betyr noen av dem noe for fornyelsen?
7. Hvor ligger den private nøkkelen? Hva skjer når en annen binær enn den som laget den, ber om den? Finnes det en kommando som kan lage en ny identitet uten at brukeren ba om det, og skrive over den gamle?
8. Hvilke krav stiller tjeneren til en melding som sendes (mottaker, formål, ID), og hva svarer den for liste, les, send og kvitter?

## Del 2: påstander som skal avgjøres

For hver: **holder**, **holder ikke** eller **kan ikke avgjøres her**, med fil og linje, og med det som mangler når den ikke kan avgjøres. Påstandene står i `skript/LES-MEG.md` (tabellen «Det som er lest og målt 05.10» og resten av teksten). Ta alle radene i tabellen, og i tillegg disse:

- P1. Fornyelsen trenger ingen ny installerer.
- P2. Kjører mottakeren `setup` rett på fila fra siden, avviser tjeneren, og ingenting er endret hos mottakeren eller brukt opp hos tjeneren.
- P3. Mens forespørselen venter, gjelder tilgangen fra før på tjeneren, og `tilbake` gir mottakeren den igjen i profilen.
- P4. Godkjennes ikke forespørselen innen 24 timer, trengs en ny invitasjon.
- P5. Å legge en ny liste med bare fire invitasjoner i tjenerens miljø tar ikke tilgangen fra noen som har den.
- P6. Prøven på `sim-a` og `sim-b` prøver det samme tjeneren vil gjøre for Vegar (fornyelse før fristen), så lenge den tas før 08.10 kl. 13:03Z.
- P7. Kjører noen `forny-haven-tilgang.sh` to ganger, eller `aktiver` før godkjenning, tar profilen ingen skade.
- P8. Skriptene skriver aldri engangskoder, invitasjons-ID-er, lenker eller enhets-ID-er i klartekst til utdata.

## Del 3: gransk skriptene

Les `skript/` som en som skal stå ansvarlig når de kjøres. Finn feil, ikke stil.

- `forny-haven-tilgang.sh` kjøres av mottakerne på macOS med `/bin/bash` 3.2 og BSD-verktøy (`sed`, `ls`, `mktemp`, `expr`, `cut`, `head`, `grep`, `date`). Jeg har bare kjørt den på Linux (bash 5, `dash`, `bash --posix`, GNU-verktøy). Gå gjennom hver kommando og si hva som kan oppføre seg annerledes på macOS. Se etter veier der profilen kan bli stående uten tilgang, der feil klient eller feil fil velges, der en hemmelighet blir liggende igjen, og der en melding til brukeren sier noe som ikke er sant.
- `stub_klient2.py` står i stedet for klienten og tjeneren i testene. Sammenlign den med kilden og list hver forskjell som kan få en test til å gå grønt mens den ekte klienten eller tjeneren ville gjort noe annet. Dette er den viktigste delen: en tidligere stedfortreder delte en feil antakelse med programmet den prøvde, og alt var grønt.
- `test_forny.py` og `test_proev.py`: hva dekker de ikke? Du kan kjøre dem (`python3 -B skript/proeve/test_forny.py`; `PROEV_GENERATOR=<banen til generatoren> python3 -B skript/proeve-sky/test_proev.py`), og du kan legge inn feil i en kopi av skriptene for å se om testene merker det.
- `proev-fornyelse.sh`: se særlig på henting av invitasjonen fra staging (samsvarer den med det siden gjør?), valg av klient, tidsgrensen, meldingsrunden i fasen `aktiver` (samsvarer verktøynavn, argumenter og svarfelt med kilden?), og hva som skjer når en fase kjøres to ganger eller i feil rekkefølge.
- `lag-invitasjoner.sh`: samsvarer bruken av generatoren med generatoren? Blir tjenerfila slik tjeneren leser den?
- `bytt-invitasjoner.sh` skal kjøres av en annen tråd mot verten og er ikke prøvd. Sammenlign bruken av `hd` og `vert.sh` med `kilder/hd/`. Hva kan gå galt i `utfoer`, og blir en claim stående?
- `LES-MEG.md`: er det noe en mottaker eller eieren kan misforstå, eller som ikke stemmer med skriptene?

## Rapporten

`arbeid/rapport.md`, med disse delene:

1. **Funn**, sortert etter alvor: «stopper» (må rettes før noe kjøres), «bør rettes», «merknad». Hvert funn: fil og linje, hva som skjer, et konkret forløp der det går galt, og hva som retter det. Ingen ros, og ingen funn uten et forløp.
2. **Svarene på del 1**, korte, med fil og linje.
3. **Påstandene i del 2**, én linje hver med dom og belegg.
4. **Det du ikke kunne avgjøre**, og hva som skulle til.
5. **Det du kjørte**, med kommando og utfall.

Skriv det du faktisk fant. Fant du ingenting i en del, skriv det, og skriv hva du gjorde for å lete. Svar meg til slutt med de viktigste funnene i noen få linjer og banen til rapporten.
