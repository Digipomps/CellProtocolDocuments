# Brief til Fabel: etterkontroll av G2-artefaktene

Dato: 02.10.2026, sen kveld. Du gransket G2-artefaktene i `panel/FABEL_SVAR_G2.md`. Alt du fant, er forsøkt tatt inn. Nå skal du kontrollere at rettelsene faktisk løser det du pekte på, og at de ikke har laget nye feil.

## Hva som er endret

Sporingen punkt for punkt står nederst i `PLAN_VEDLEGG.md`, avsnittet «Fabels gransking av G2-artefaktene». Filene som er endret:

- `contract/trinn1-2-programmer.md` (skrevet om), `contract/config-tillegg-trinn1-2.json`, `contract/scheduled-task-stamp-v1.schema.json`, stempel-eksemplene
- `contract/trinn3-cron.md`, `contract/cron_reference.py` (regelen for løpende uttrykk ser nå på alle ledd; korteste avstand regnes over `(after, until]`), `contract/fixtures/cron-forventninger.json` (22 gyldige, 11 tellinger, 16 ugyldige, 8 korteste avstander)
- `contract/trinn4-jobber-og-godkjenning.md` (skrevet om), `contract/trinn5-kontrollbro.md`, `contract/README.md`, `contract/mcp-verktoy.json`, `contract/saker-job.example.json`, skjemaene for styring, kjøretilstand, status og bestilling
- `contract/fixtures/ScheduledJobs/` (ny mappe; erstatter `fixtures/jobb-*.json`)
- `contract/kontroller_kontrakt.py` og `contract/KONTROLL.txt`
- `dataflow.md`, `handoff/README.md`
- `PLAN.md` (sikkerhetsavsnittet; trinn 1 har to ja; «Tre presiseringer av formålene» under «Det du godkjenner i G2»)
- `FORMAALSSPEC.md` (§1c er ny; påstandstabellen; §7)
- `images/README.md`, `images/meny-v4.html`, `images/meny-jobb-godkjenning-v4.png`, `images/meny-planlagte-jobber-ro-v3.png`

Kildene er de samme som sist, på de samme stiene.

## Det jeg ber om

1. For hvert av dine seks «må rettes» og tjue «bør rettes»: er det løst, delvis løst eller ikke løst? Vis til fil og linje i den nye teksten.
2. Tre valg er gjort annerledes enn du foreslo. Si om de holder:
   - Regelen for løpende uttrykk avviker nå fra cronie: et uttrykk er løpende når minutt- eller timefeltet har et ledd som er `*` eller `*/n`, uansett plass i lista. Regn etter de nye tilfellene i fasiten med din egen framgangsmåte.
   - Agenten får ingen kopi av køens tillatt-liste. Jobbmalen kontrolleres bare for form, og køen håndhever sin egen liste når jobben kjøres.
   - Faste hendelser kan settes på pause og startes igjen fra menylinjen og kommandolinjen, men ikke stoppes for godt, og ikke styres gjennom MCP.
3. Let etter nye feil som rettelsene har laget: steder der to dokumenter nå sier ulike ting, regler som ikke lar seg bygge, og tekst i `PLAN.md` som sier mer enn kildene gir grunnlag for.
4. Les «Tre presiseringer av formålene» i `PLAN.md` og §1c i `FORMAALSSPEC.md` slik Kjetil vil lese dem. Er det klart hva han tar stilling til, og hva som skjer hvis han sier nei til en av dem?

## Slik svarer du

Skriv til `panel/FABEL_ETTERKONTROLL_G2.md`, på norsk. Del den slik: **Utfall per punkt** (tabell), **De tre valgene**, **Nye feil** (nummerert, med fil, linje og hva som bør stå), **Presiseringene slik Kjetil leser dem**. Samme grenser som sist: bare lesing utenom rapportfila, ingen verktøy som når Macen eller andre tjenester, ingen private detaljer fra `panel/kilder-utdrag/` i rapporten.
