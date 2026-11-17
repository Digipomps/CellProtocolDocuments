# Fabel: kontroll av rettelsene etter etterkontrollen

Kontrollert 02.10.2026 (sen kveld) mot `panel/BRIEF_G2_ETTERKONTROLL2.md`, ved å sammenligne hver fil med utgaven `.foer-etterkontroll` og lese den nye teksten mot kildene. `kontroller_kontrakt.py` er kjørt på nytt uten å skrive noe (139 av 139, cron 61 av 61), og de fire nye tellingene (`30 */2` og `30 0-23/2` på 25.10.2026 og 28.03.2027) er regnet etter med min egen framgangsmåte: 13, 11, 12 og 12, som fasiten. Linjenumre gjelder de nye filene.

## Utfall per feil

| # | Feil | Utfall | Hvor det nå står |
|---|---|---|---|
| 1 | «Stopp jobben» på saker om faste hendelser pauset dem | **løst** | `contract/trinn4-jobber-og-godkjenning.md` 104, 109–110 (faste hendelser har «Kvitter» og «Åpne» i trinn 4, «Sett på pause» fra trinn 5, ikke destruktiv); `trinn5-kontrollbro.md` 32; `saker-job.example.json` 93–96, 104; `dataflow.md` K32 (87); `images/meny-v4.html` 119, 134; `images/README.md` 11, 18–19 (feil-v2 er utgått, v3 gjelder); `PLAN_VEDLEGG.md` AP9 (21), AP13 (25); kontroll 4b i `kontroller_kontrakt.py`. |
| 2 | §5 var ikke oppdatert | **løst** | `FORMAALSSPEC.md` 156 («den ene lista») og 161–170 (T1–T10 har alt kontraktene la til); `trinn3` 96, `trinn4` 146 og `trinn1-2` 152 viser dit. |
| 3 | §6 sa «ingen åpne spørsmål» | **løst** | `FORMAALSSPEC.md` §1c 90 («Hver besvares for seg; et ja til G2 er ikke et svar på dem») og ny kolonne «Sier Kjetil nei» 92–96; §6 174–180 (tre spørsmål, hvert med hva nei betyr); `PLAN.md` 127–137 (egen seksjon med tabell). |
| 4 | `resume` manglet regel for `lastOccurrence` | **løst** | `trinn4` 67 (regel 6) og 94–95; `trinn3` 87; `trinn5` 30; `dataflow.md` K33 (88); §5 T3. Lar seg bygge uten at to prosesser skriver samme fil: arbeideren *leser* `changedAt` i styringsfila og skriver bare kjøretilstanden. Se ny feil 1 om intervallhendelser. |
| 5 | Tittel over 80 tegn for fast hendelse uten `title` | **løst** | `trinn4` 111 (79 tegn + «…», som `asChallenge()`); `trinn3` 14; `handoff/README.md` 78 (`title` eller id ≤ 40); `config-tillegg-trinn1-2.json` 80 (`title` fra trinn 3); kontroll 4b og linje 298 i `kontroller_kontrakt.py`; §5 T4 (id på 60 tegn). |
| 6 | Tidsbudsjettet for mer enn to profiler | **løst** | `trinn1-2` 62 (50 s delt på antall profiler, høyst 25 per profil, høyst fire profiler, kode 2 for flere) og 149; §5 T8. Regnestykket holder: fire profiler gir 12,5 s hver, nok til ett forsøk på 12 s. |
| 7 | `PLAN.md` sa mindre enn kontrakten | **løst** | `PLAN.md` 113–114 (klientens rot), 135 (presisering 3: «fra menyen eller kommandolinjen på Macen»). |
| 8 | `spool-not-enabled` nevnte én nøkkel | **løst** | `mcp-verktoy.json` 243; kontroll i `kontroller_kontrakt.py` 318. |
| 9 | `git push`-prøven kunne gi falskt nei | **løst** | `handoff/README.md` 34 (`HEAD:refs/heads/koe-proeve-20261002`, tørrkjøring) og 39 (hvilke svar som betyr ja og nei). `--dry-run` er ikke et forbudt flagg (`agent_job_runner.py` 61–67), og `HavenAgentD` er ikke en vernet utsjekk (77). |
| 10 | Ingen regel når klienten ikke tar `--root` | **løst** | `trinn1-2` 161 («`toerr` stopper … programmet har ingen utgave uten `--root`»); `handoff` 76. |
| 11 | «åtte timers søvn gir 15» | **løst** | `trinn3` 80 («15 eller 16, etter hvor lenge det var igjen til neste kjøring da Macen sovnet»). |
| 12 | Formkontrollen manglet `env` | **løst** | `trinn4` 29 (`env` er objekt med `HAVEN_`-nøkler og tekstverdier, `steps` minst ett steg, `cmd` minst ett ledd) og 122 (`env` i detaljen); `mcp-verktoy.json` 252; kontroll 6b. Se ny feil 3 om feltene som fortsatt ikke kontrolleres. |
| 13 | Småting | **løst** | `PLAN.md` 5 (fire granskinger); `trinn4` 35 («En assistent» er det lengste navnet); `cron-forventninger.json` 381–412 (fire tellinger) og `trinn3` 36, 54–62 (tabellen med timefeltet). |

Sum: 13 av 13 løst.

## Nye feil

Ingen av dem hindrer G2. Alle er små.

1. **To dokumenter sier ulikt om hva «Fortsett» gjør for en fast hendelse på intervall uten cron.** `trinn4` 95 sier den «kjøres ved første runde etter `resume`», fordi slike hendelser ikke har noe rutenett (`nextFireAt` fra før pausen er passert, og dagens planlegger kjører forfalte én gang, `ScheduledEventService.swift` 216–226). `trinn5` 30 («første kjøring er neste planlagte tidspunkt») og `FORMAALSSPEC.md` §5 T3 («kjøres ikke på etterskudd») sier det uten unntak. For korrespondansesjekken, som er en slik hendelse, er det `trinn4` 95 som gjelder. Bør stå i `trinn5` 30 og i T3: «for faste hendelser på intervall uten cron kjøres første gang straks etter «Fortsett», og passeringen telles ikke».

2. **«Fra trinn 5» er ikke noe agenten kan vite.** `trinn4` 104 og 110 og `trinn5` 32 sier at saker om faste hendelser får «Sett på pause» fra trinn 5, fordi «Fortsett» da står i lista. Knappen lages av agenten, mens lista er menyappens. Går trinn 4 og 5 i samme agentinstallasjon (`PLAN.md` 37), må agenten likevel vite om menyappen med lista er installert. Bør stå: knappen slås på med en nøkkel i `config.json` (for eksempel `scheduledJobs.menuHasList`) som installasjonsskriptet for menyappen setter, eller den sendes alltid fra den agentbygget som også har `GET /scheduled-jobs` — og da sier `PLAN.md` at knappen kan dukke opp før lista.

3. **Formkontrollen slipper gjennom to felt køen snubler på.** `trinn4` 29 kontrollerer `cwd`, `steps`, `cmd` og `env`, men ikke `timeoutSeconds` og `name` i hvert steg. Køen gjør `int(step.get("timeoutSeconds", …))` utenfor sin egen feilhåndtering (`agent_job_runner.py` 214); en tekst der gir en krasj som ender som `error` i resultatfila (424–437), altså `failed` og en sak, etter at Kjetil har godkjent. Bør stå: `timeoutSeconds`, hvis det finnes, er et heltall mellom 1 og 10800 (køens tak, linje 39), og `name`, hvis det finnes, er tekst; `stopOnFailure` er sann eller usann. Kontroll 6b får samme tilfeller.

4. **Ingen regel for `reject` på en sak uten den knappen.** Før trinn 5 har saker om faste hendelser bare «Kvitter» og «Åpne» (`trinn4` 110), men `POST /challenges/respond` tar hvilken som helst svar-id (`AgentControlBridgeServer.swift` 137–145). Bør stå i `trinn4`, under godkjenningen eller sakene: et svar saken ikke tilbyr, gir `accepted: false` og skriver ingenting.

5. **Småting.** `images/README.md` 11 fører feil-v3 under «4 og 5», men bildet viser trinn 5-utgaven med «Sett på pause»; linje 18 forklarer det, så kolonnen kan stå «5 (i trinn 4 uten «Sett på pause»)». `trinn4` 110 sier «Eksempelet i `saker-job.example.json` viser saken slik den er fra trinn 5» — det stemmer, og `kontroller_kontrakt.py` 4b krever den formen, så en som bygger trinn 4 må vite at eksempelet har én knapp for mye for sitt trinn; én setning om det i `saker-job.example.json` sin `sources`-del eller i `contract/README.md` 28 hadde holdt.

## Presiseringene slik Kjetil leser dem

`PLAN.md` 127–137 og `FORMAALSSPEC.md` §6 174–180 sier nå tydelig at det er tre egne svar («Et ja til G2 er derfor ikke et ja til disse. Jeg spør om dem én for én»), og kolonnen «Sier du nei» er sann mot kilden: for F5 tegner menyen og adminvinduet de samme knappene fra saken (`HavenAgentMenuApp.swift` 83–91, `AdminWindow.swift` 136–143), så «Godkjenn bare i adminvinduet» krever ny menyapp i trinn 4; for F6 gir to passerte tidspunkt etter én times søvn `missedCount` 1 og dermed en sak (regnet i forrige rapport); for F4 er alternativet nøyaktig det den første kontrakten tillot. Punkt 1 har nå setningen «du kan godkjenne fra menyen uten å åpne», og punkt 3 sier «fra menyen eller kommandolinjen på Macen». Det eneste som kunne vært klarere, er at «Sier du nei» for F6 nevner «en annen grense» uten å si hva som er mulig (for eksempel sak først når mer enn N tidspunkt er passert); det holder som det står.
