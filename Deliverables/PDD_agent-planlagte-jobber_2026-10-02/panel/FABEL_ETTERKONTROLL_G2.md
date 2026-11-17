# Fabel: etterkontroll av G2-artefaktene

Kontrollert 02.10.2026 (sen kveld) mot `panel/BRIEF_G2_ETTERKONTROLL.md`. Kildene er de samme som i `panel/FABEL_SVAR_G2.md` (`origin/main` `ea558ba` eksportert under `.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/`, køene, og utdragene i `panel/kilder-utdrag/`). Linjenumre uten filsti gjelder den nye teksten i PDD-mappen. Ingen private detaljer fra utdragene gjengis.

Kortversjon: alle seks «må» og alle tjue «bør» er løst i teksten, og de sytten manglene er dekket. De 57 cron-tilfellene i den nye fasiten reproduseres med min egen framgangsmåte. De tre valgene som ble gjort annerledes enn jeg foreslo, holder. Rettelsene har laget tretten nye feil, fem av dem bør rettes før G2: knappen «Stopp jobben» på saker om faste hendelser *pauser* dem; testtabellen i FORMAALSSPEC §5 er ikke oppdatert og sier noe annet enn kontraktene; §6 sier «ingen åpne spørsmål» mens §1c stiller tre; `resume` etter pause mangler regel for `lastOccurrence`; og en fast hendelse uten `title` og med lang id kan gi en sakstittel over 80 tegn, som gjør hele innboksen uleselig.

---

## Utfall per punkt

| Punkt | Fabel fant | Utfall | Hvor det nå står |
|---|---|---|---|
| Må 1 | Menyraden der «Godkjenn» ligger, viser ikke hva som kjøres | **løst** | `contract/trinn4-jobber-og-godkjenning.md` 112–124: «Gjelder» har hva som kjøres i kortform, tittelen i anførselstegn, og det sies rett ut at Kjetil kan godkjenne fra menyen uten å åpne. `saker-job.example.json` 48, 54. `PLAN.md` 59. `images/meny-v4.html` (undertittelen har «køjobb: git fetch, swift test»). `FORMAALSSPEC.md` §1c F5 (89–95). |
| Må 2 | Daglig falsk sak etter søvn for korrespondansesjekken | **løst** | `trinn3-cron.md` 72, 77 (sak for passering bare ved takt ≥ 23 timer); `trinn4` 107, 110; `PLAN.md` 130; `FORMAALSSPEC.md` §1c F6. T3 i `trinn3` 94 prøver åtte timers søvn for 30-minuttshendelsen. |
| Må 3 | Køfilas navn kunne gjøre at jobben aldri kjøres | **løst** | `trinn4` 75 (`20261014T000000Z`, med henvisning til `agent_job_runner.py` linje 40); `PLAN_VEDLEGG.md` AP10 (22); `kontroller_kontrakt.py` 5b prøver navnet og det lengste tilfellet mot køens mønster. |
| Må 4 | En køfil som ikke ble tatt, kjøres likevel senere | **løst** | `trinn4` 77 (slettes ved `no-result`, pause, stopp, `endsAt`, tapt godkjenning; `withdrawn`); `scheduled-job-runtime-v1.schema.json` 148–150 og statusskjemaet 160–168 har `withdrawn`; `dataflow.md` K28 (83). |
| Må 5 | Installasjonskommandoen for ny agent kunne ikke kjøres | **løst** | `handoff/README.md` 122–130: bygg i `.agent-spool`, én installasjon per produkt med `--source`, `/bin/zsh` fra omslag, og hvorfor `--product all`/`--build` ikke brukes; linje 18 om bash 3.2. Stemmer med `Scripts/install-agent-dev.sh` 233–236, 307–315, 317. |
| Må 6 | Fristgrensen motsa sin egen fasit | **løst** | `trinn1-2-programmer.md` 116 (hele døgn rundet ned ≤ `--dager`; 8 d 0 t ingen, 7 d 23 t markør) og 149 (selvtest). `fixtures/markor-frist.json` (7 d 12 t igjen → «om 7 dager») er nå i samsvar med regelen. |
| Bør 1 | Falsk «har stoppet» etter lang søvn og ved pause | **løst** | `trinn1-2` 93 og 133 (krever eget ferskt stempel); søskenvakten tas ut i trinn 4 (93); selvtest 148. |
| Bør 2 | Livstegnet må skrives uavhengig av kjøringen | **løst** | `trinn3` 84; T7 i `trinn4` 143 (program som sover fem minutter). |
| Bør 3 | Vakttråden hoppet over `finally`; alarmen uten behandler | **løst** | `trinn1-2` 26 (behandler som kaster; vakttråden dreper klienten og skriver stempel med kode 3 før `os._exit`). |
| Bør 4 | Tidsbudsjettet tok ikke høyde for klientens egen tidsgrense | **løst** | `trinn1-2` 62 (25 s per profil, 12 s per forsøk, rekkefølgen roterer) og 73 (nytt forsøk etter 3 s når minst 8 s er igjen). Regnestykket holder for to profiler: 12 + 3 + 10 = 25, og 2 × 25 = 50 < 55. Se ny feil 6 for tre eller flere. |
| Bør 5 | «Eldre agent ser bort fra nye felt» gjaldt lesing, ikke skriving | **løst** | `trinn3` 18–22 (arbeideren og `setup` stripper feltene; ny binær må modellere dem), 85 (pause beholder `nextFireAt`); AP6 (18); `handoff` 145; T10 i `trinn3` 94. |
| Bør 6 | Sikkerhetslista utelot `agent.xcode.ensure_workspace` og var abstrakt | **løst** | `PLAN.md` 74 og 76 (de to faste programmene er navngitt). |
| Bør 7 | Generert id kunne erstatte en godkjent jobb | **løst** | `trinn4` 26; `mcp-verktoy.json` 7, 20, `id-in-use` (251); T4 i `trinn4` 143. |
| Bør 8 | MCP kunne stoppe Kjetils faste hendelser uten trykk | **løst**, med annet valg (se under) | `trinn4` 92; `mcp-verktoy.json` 2, 123, 151, 174, 197, `fixed-event` (254); `trinn5` 14 og 25 (gjenstart av stoppet fast hendelse); `FORMAALSSPEC.md` §1c F4. |
| Bør 9 | «Siste skriver vinner» mot «stopped kan ikke gjøres om» | **løst** | `trinn4` 83–89 (én funksjon under lås, overgangstabell); `scheduled-job-control-v1.schema.json` 5; T5 i `trinn4` 143. |
| Bør 10 | «For ofte» var avhengig av bestillingsdato | **løst** | `cron_reference.py` 203–217 (`(after, until]`); `trinn4` 27; to nye tilfeller i fasiten (`10 2,3 * * *` i oktober 2026 og mars 2027, 3600 og 600 s). |
| Bør 11 | Regelen for løpende uttrykk ga overraskelser | **løst**, med annet valg (se under) | `trinn3` 41, 48–49, 52–60; `cron_reference.py` 103; fasiten har de tre følgene som tellinger og gyldige tilfeller. |
| Bør 12 | Tidsstempler med millisekunder og `Z` | **løst** | `trinn1-2` 40–42; selvtest 145. |
| Bør 13 | Diffen i `config.json` uleselig uten normalisering | **løst** | `handoff` 19 (`shasum -a 256`, `date -u …Z`) og 79 (samme oppsett før sammenligning). |
| Bør 14 | Omstart av planleggeren midt i en kjøring | **løst** | `handoff` 81 (venter til ingen post er `running`) og 84 («kjører allerede» som mulig første utfall). |
| Bør 15 | Porten av køens kontroll var ufullstendig | **løst**, med annet valg (se under) | `trinn4` 29 (ingen kopi; formkontroll; køen håndhever); `kontroller_kontrakt.py` 6 sier nå at lista der bare er en kontroll av eksempelet. |
| Bør 16 | Ventende godkjenning utløp aldri; `Removed/` | **løst** | `trinn4` 56 (utløper ved `endsAt`, for `once` ved `at`) og 18, 128 (`Removed/` leses ikke). |
| Bør 17 | Flimmer ved ny bestilling på samme id | **løst** | `trinn4` 12 (`<id>.<tolv tegn>.spool.json`); `fixtures/ScheduledJobs/regresjon-havenagentd.e4ecf2296f0f.spool.json`; sjekksummene henger sammen (kontrollert uavhengig: spec-, godkjennings- og kjøretilstandsfila peker på samme sjekksum, og malfilas navn og innhold stemmer). |
| Bør 18 | Småting der dokumentene sa ulikt | **løst** for det jeg pekte på | `dataflow.md` 36 (begge verktøynavn), 43 (samlevarsel), 97 (Losen har ikke verktøy), 99 (agenten leser fra trinn 4); `contract/README.md` 37 («Gjelder» er kontraktens egen regel); `FORMAALSSPEC.md` §0 («fire skript»); `PLAN.md` 89 (to ja); `trinn5` 30 («Sett alle på pause» er nå i kontrakten). Rettelsene har laget nye uoverensstemmelser, se «Nye feil». |
| Bør 19 | Mål før S1 og S3 stoler på det | **løst** | `handoff` 34, 39 (`git push --dry-run` i S0), 134 (signering fra køjobb måles i tørrkjøringen), 20 (Codex-binæren). Se ny feil 9 om refspec-en. |
| Bør 20 | Hvor `requestedBy` kommer fra | **løst** | `trinn4` 35 (regelen for «claude»/«codex»/«En assistent», at serveren ikke leser `clientInfo` i dag, og at navnene måles i T6). |

De sytten manglene er dekket: 1–10 i `trinn1-2-programmer.md` (68, 69, 73, 30, 34, 87–93, 127–133, 38, 18/66, 157, 160) og `handoff/README.md` (18–20, 71, 75–82, 86); 11–17 i `trinn3` 14, 22, 78, 84 og `trinn4` 35, 41–47, 77, 83–94 og `trinn5` 25–26. To av dem har fått en ny åpen kant, se ny feil 4 (resume) og 10 (`--root`).

Sum: 26 av 26 løst, 0 delvis, 0 ikke løst.

---

## De tre valgene

**1. Løpende uttrykk: et ledd som er `*` eller `*/n`, uansett plass i lista (`trinn3` 41; `cron_reference.py` 103).** Holder. Regelen er entydig, bestemmes ved tolkningen av leddene og ikke av verdimengden, og den tar bort rekkefølgefølsomheten cronie har (`5,*/10` og `*/10,5` gir nå det samme). Det som står igjen av overraskelser, er bevisst og dokumentert i 52–60: alt som er skrevet med `*` følger klokka, alt som er skrevet med tall er fast, så `0-59 2 * * *` (60 kjøringer 25.10, én 28.03) og `* 2 * * *` (120 og ingen) er ulike selv om mengdene er like. Samme skille gjelder timefeltet: `30 */2 * * *` er løpende og `30 0-23/2 * * *` er fast (13 mot 12 kjøringer 25.10, 11 mot 12 den 28.03, regnet med referansen). Det bør stå som eksempel på timefeltet i 54–60, ellers er regelen komplett.

Egen etterregning av den nye fasiten: samme framgangsmåte som sist (løpende uttrykk: hvert UTC-minutt prøves mot lokal tid; faste klokkeslett: per lokal dato kartlegges første UTC-minutt for hvert `(time, minutt)`, og et klokkeslett som ikke finnes, gir første UTC-minutt med lokal tid etter det, med duplikater slått sammen), men med klassifiseringen endret til den nye regelen. **57 av 57 stemmer**: 22 gyldige, 11 tellinger, 16 ugyldige og 8 korteste avstander, inkludert de nye (`5,*/10 2 25 10 *` og `*/10,5 2 25 10 *` gir de samme 14 instantene; `0 2,3 28 3 *` gir én kjøring kl. 01:00Z; `0-59 2 * * *` gir 60 og 1; strengt «etter» med sekunder; `10 2,3 * * *` gir 3600 s i oktober 2026 og 600 s i mars 2027; `0 9 * * *` gir 86400 i oktober og 82800 i mars). Sakene 25.10/28.03 er dessuten resonnert for hånd i forrige rapport, og de er uendret.

**2. Ingen kopi av køens tillatt-liste i agenten (`trinn4` 29; `mcp-verktoy.json` 86; `kontroller_kontrakt.py` 6).** Holder, og det er det ærligste valget: en kopi ville drevet fra køen, og køen eier regelen. Tre følger bør sies: (a) Kjetil kan godkjenne en jobb som køen kommer til å nekte; han ser program og underkommando i «Gjelder», men ikke om de står på lista, og svaret kommer først som saken «Planlagt jobb feilet» med `refused` etter at tiden var inne. (b) Assistenten får ingen tidlig beskjed; `agent.schedule.request` kan ikke si «dette nekter køen». (c) Formkontrollen bærer derfor hele vernet mot `cannot-be-shown`-omgåelse: et steg som ikke kan gjengis ordrett, avvises fortsatt (122), og det er riktig. Formkontrollen i 29 bør også kreve at `env`, hvis det finnes, er et objekt med nøkler som begynner på `HAVEN_`, for det nekter køen (`agent_job_runner.py` 199–208), og at hvert `cmd` har minst ett ledd.

**3. Faste hendelser kan settes på pause og startes igjen, ikke stoppes, og ikke styres gjennom MCP (`trinn4` 85–92; `trinn5` 14, 25; `mcp-verktoy.json` 2, 254).** Holder, og det stenger den veien jeg pekte på (en assistent som slår av postsjekken). Tre ting følger: (a) knappen «Stopp jobben» på saker om faste hendelser betyr nå «sett på pause», men heter fortsatt «Stopp jobben» — se ny feil 1; (b) `schedule-stop` fra kommandolinjen stopper fortsatt faste hendelser som i dag, og `trinn5` 25 sier riktig hvordan `resume` henter dem tilbake; (c) `PLAN.md` 131 sier «Det kan bare du, fra menyen», mens kontrakten også åpner kommandolinjen — se ny feil 7. Og som før: kode som kjører som Kjetil, kan skrive styringsfila selv; det står i `PLAN.md` 80.

---

## Nye feil

Rangert etter hva som bør rettes først.

1. **«Stopp jobben» pauser en fast hendelse, men heter og forklares som stopp.** `trinn4` 108 sier «For en fast hendelse setter den hendelsen på pause», men saken `job:scheduled:korrespondanse-frist:attention` i `saker-job.example.json` 93–97 har etiketten «Stopp jobben» og begrunnelsen «Du kan kvittere eller stoppe både der og her» (105); `dataflow.md` K32 (87) sier det samme; `images/meny-v4.html` 119 forklarer ««Stopp jobben» avslutter den», og `images/README.md` 11 holder `meny-planlagte-jobber-feil-v2.png` som gjeldende. Kjetil ville trykket «stopp» og fått «pause». Bør stå: for saker om faste hendelser heter `reject` «Sett på pause», begrunnelsen «Du kan kvittere eller sette på pause både der og her», og feil-bildet får en v3 med riktig etikett. Alternativt tilbys ikke `reject` på saker om faste hendelser.

2. **Testtabellen i `FORMAALSSPEC.md` §5 (158–168) er ikke oppdatert, og sier noe annet enn kontraktene.** Kontraktene har utvidet testene: T1 med følgene av den nye regelen (`trinn3` 54–60), T3 med «en hendelse hvert 30. minutt gir ingen sak etter åtte timers søvn, og en daglig gir sak etter to døgn» (`trinn3` 94), T4 med id-regelen, køfilas navn og tilbaketrekking (`trinn4` 143), T5 med «MCP kan ikke styre en fast hendelse» og «pause og stop samtidig ender i stopped» (143), T7 med «Planleggeren går ikke» kommer ikke mens et program kjører i fem minutter (143), T9 med grensetilfellene 8 d 0 t og 7 d 23 t (`trinn1-2` 149), T10 med at den nye binæren skriver `config.json` uten å miste feltene (`trinn3` 94). §5 er det Kjetil får som bevisliste. Bør stå: §5 oppdateres til kontraktenes tekst, og kontraktene viser til §5 i stedet for å gjenta testene.

3. **§6 sier «Ingen åpne spørsmål om formålene» (`FORMAALSSPEC.md` 172), mens §1c (88–95) legger fram tre presiseringer Kjetil skal svare på.** Bør stå: §6 får de tre spørsmålene, nummerert, med «ja» som anbefalt svar og hva «nei» betyr (se neste avsnitt), og `PLAN.md` 127–131 får samme tre spørsmål, så det er klart at de besvares hver for seg og ikke følger av et «ja til G2».

4. **`resume` etter pause mangler regel for `lastOccurrence`.** `trinn4` 94 sier «Mens en jobb er på pause, telles ikke passerte tidspunkt», men regel 6 (67) kjører ved «et planlagt tidspunkt passert siden `lastOccurrence`», og 76 i `trinn3` legger resten i `missedCount`. Uten en regel for `resume` kjører jobben straks den startes igjen (det første tidspunktet under pausen er passert), og de andre telles likevel. Bør stå: ved `resume` settes `lastOccurrence` til tidspunktet for `resume`; ingenting kjøres på etterskudd, og `missedCount` rører ikke pausen. Gjelder også faste hendelser (`trinn5` 24–25).

5. **En fast hendelse uten `title` kan gi en sakstittel over 80 tegn og slå ut hele innboksen.** `trinn3` 14: «Uten det vises id-en». Sakstitlene i `trinn4` 103 er «Planlagt jobb kan ikke kjøres: <tittel>» (31 tegn pluss tittel), «Planlagt jobb ble passert: » (27) og «Planlagt jobb feilet: » (22). Hendelses-id-er i `config.json` har ingen lengderegel, og dagens ene er 41 tegn; en id over 49 tegn gir en tittel over 80, som broen avviser med 500 og menyappen med `malformed` (`AgentChallenge.swift` 265–266; `AgentControlBridgeServer.swift` 118–122; `AgentBridgeClient.swift` 137–143). Bør stå: tittelen avkortes med «…» til 80 tegn, slik `asChallenge()` gjør for post (`CorrespondenceWaiting.swift` 106–110), og installasjonsskriptet krever `title` eller en id på høyst 40 tegn for hendelsene det legger inn.

6. **Tidsbudsjettet i `trinn1-2` 62 er skrevet for to profiler.** 25 s per profil og alarm etter 55 s (26) gir 50 s for to; en tredje `--profil` ville blitt avbrutt hver gang og, med roteringen, gitt `partial` i hver kjøring uten at noen profil feiler to ganger på rad. Bør stå: «høyst to profiler per hendelse», eller «budsjettet er 50 s delt på antall profiler».

7. **`PLAN.md` sier mindre enn kontrakten på to steder.** 113: programlinjen for `korrespondanse-sjekk` nevner «stiene til klienten, markørmappen og tilstandsmappen», men `config-tillegg-trinn1-2.json` 23–24 har også `--klientrot`, og 109 sier tillegget står «ordrett» der. 131: «Det kan bare du, fra menyen» — `trinn4` 92 og `trinn5` 14 åpner også kommandolinjen. Bør stå: «pluss stiene til klienten, klientens rot, markørmappen og tilstandsmappen» og «fra menyen eller kommandolinjen på Macen».

8. **`mcp-verktoy.json` 243 (`spool-not-enabled`) nevner bare `spoolInbox`,** mens `trinn4` 29 og 79 krever både `spoolInbox` og `spoolOutbox`. Bør stå: begge nøklene.

9. **Prøven av `git push` i S0 kan gi falskt «nei».** `handoff` 34 skyver `origin/main:refs/heads/main` som tørrkjøring. Er den lokale `origin/main` bak GitHub (ingen `fetch` i jobben før steget), svarer serveren «rejected (non-fast-forward)», og 39 leser det som «køen kan ikke skyve». Bør stå: legg `git fetch origin main` først, eller skyv `--dry-run` til et grennavn som ikke finnes (`HEAD:refs/heads/koe-proeve-<dato>`), og regn «rejected» som bevis på at nøklene virket.

10. **Ingen regel når klienten ikke tar `--root`.** `trinn1-2` 18 og 66 bruker `--root`; 160 sier det måles av installasjonsskriptet. Står ikke hva som skjer hvis målingen sier nei (installasjonen stopper? programmet faller tilbake til uten `--root`?). Bruksteksten fra den installerte binæren i `maaling-job-251.txt` 213–218 viser `[--root /path]`, så det er trolig i orden, men regelen bør stå: «tar klienten ikke `--root`, stopper `toerr`».

11. **Eksempelet i `trinn3` 78 er bare omtrent riktig.** «Antall hele intervaller mellom det planlagte tidspunktet og starten» gir 16 når det er nøyaktig åtte timer mellom dem; «åtte timers søvn gir 15» stemmer bare når det planlagte tidspunktet lå inntil 30 minutter etter at Macen sovnet. Bør stå: «gir 15 eller 16», eller definer tellingen som antall rutenettpunkter som passerte.

12. **Formkontrollen i `trinn4` 29 mangler `env`.** Køen nekter `env` som ikke er et objekt med `HAVEN_`-nøkler (`agent_job_runner.py` 165–208). Siden saken ikke viser `env`, bør formkontrollen avvise alt annet, så ikke en jobb Kjetil godkjente nektes av en grunn han ikke kunne se.

13. **Småting.** `PLAN.md` 5 sier «gransket av Fabel to ganger»; det er tre. Verste godkjenningstittel («En assistent ber om en planlagt jobb: «» pluss 40 tegn pluss «»») er nøyaktig 80 tegn — det passer, men uten margin, så «En assistent» må forbli det lengste navnet, og det bør stå i `trinn4` 35.

---

## Presiseringene slik Kjetil leser dem

`PLAN.md` 127–131 og `FORMAALSSPEC.md` §1c (88–95) sier det samme, kort og uten fagord. Det er klart *hva* hver presisering gjør: (1) menyen viser kortform, hele jobben står i adminvinduet; (2) passering gir sak bare for jobber som går én gang i døgnet eller sjeldnere, feil gir alltid sak; (3) assistenter kan ikke sette de faste programmene på pause eller stoppe dem. Punkt 2 er det best skrevne: det sier hva problemet var («en sak hver morgen»), hva forslaget er, og hva som fortsatt gir sak.

Det som ikke står, og som han trenger for å kunne si nei:

- **Om det er ett eller tre svar.** Presiseringene står under «Det du godkjenner i G2» (107), og §6 sier at det ikke finnes åpne spørsmål. Slik det står nå, blir et «ja til G2» lest som ja til alle tre. §1c sier derimot «Tabellen i §1 endres når Kjetil har svart». Spør eksplisitt, ett spørsmål per presisering, som §6 gjorde for E1–E6.
- **Hva «nei» betyr for hver.** (1) F5: menyen kan ikke vise mer enn tittel og én linje, og menyen og adminvinduet tegner de samme knappene fra saken (`HavenAgentMenuApp.swift` 83–91; `AdminWindow.swift` 136–143). Et nei betyr derfor enten ny menyapp alt i trinn 4 (med egen visning for jobbsaker), eller at godkjenning bare kan gis fra kommandolinjen (`schedule-approve`) og ikke fra menyen. Det bør stå, for det flytter trinn 4. (2) F6: et nei betyr at hver natt Macen har sovet over én time, gir korrespondansesjekken en sak som må kvitteres — eller at han velger en annen grense (for eksempel sak bare når mer enn N tidspunkt er passert). (3) F4: et nei betyr at en assistent kan sette korrespondansesjekken og fristvarselet på pause eller stoppe dem uten trykk; det gir F8 og F9 en ny måte å slutte å virke på. Én setning per punkt holder.
- **Punkt 1 sier «Du kan godkjenne fra menyen uten å åpne» i `PLAN.md` 59, men ikke i presiseringen (129).** Det er akkurat det han tar stilling til; ta setningen inn i punkt 1.
- **Punkt 3 sier «Det kan bare du, fra menyen».** Kontrakten åpner også kommandolinjen (`trinn4` 92), og `PLAN.md` 80 sier at kode som kjører som Kjetil kan gjøre det samme som han. Skriv «fra menyen eller kommandolinjen på Macen», så presiseringen ikke lover mer enn resten av planen.

Ellers: ordene «passering», «fast program» og «adminvinduet» er forklart tidligere i planen (13–27, 100–102), så presiseringene kan leses uten forkunnskap, og det er tydelig at de endrer ordlyd i formål han alt har godkjent, ikke hva som bygges.
