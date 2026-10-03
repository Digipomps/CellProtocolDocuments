# TESTRESULT — PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23

Skrevet 2026-09-24 natt av Losen. Hvert tall har en fil bak seg under `maaling/rapport/`. Positive meldinger er de der Butler burde gjøre noe (hjelper eller flate); negativer er småprat, «ikke gjør noe», spørsmål om Butler selv og ønsker utenfor HAVEN. «Top-1» betyr at det Butler faktisk foreslo, var riktig.

## #forstaaelse

Korpus v1: 396 meldinger fra fire personaer, 33 etiketter à 12, bokmål og engelsk. Holdout = 100 meldinger (hash av id) som ingen grafendring ble begrunnet med. Målt gjennom produksjonens egen `assistant.analyzeDraft` for en ny bruker uten språkmodell.

| Korpus v1 | før (`rapport/foer/score-v2-kart.md`) | graf v3 (`rapport/graf-v3/score-v2-kart.md`) |
|---|---|---|
| Holdout, top-1 (positive, n=81) | 20 % [11–28] | **40 % [28–51]** |
| Holdout, top-1 eller spurte med riktig valg | 22 % | 46 % |
| Holdout, riktig blant tre øverste (R@3) | 23 % | 57 % |
| Holdout, MRR | 0,23 | 0,56 |
| Holdout, negativer uten handling (n=6) | 100 % | 100 % |
| Trening, top-1 (n=231) | 17 % | 66 % |
| Alle, negativer uten handling (n=36) | 94 % | 94 % |
| PromptPurposeLab-fixturene (tilregnelighet, 101) | 101/101 | 101/101 |

Holdout-meldinger vunnet/tapt fra før til v3: 16 vunnet, 0 tapt (`grafendringer/GRAFENDRINGER-v3.md`).
Regresjon i samme jobb (`PersonalChatPromptEvaluationTests|ButlerSignalMatcherTests|ChatPurposeResourceRouterTests`): grønn (`rapport/graf-v3/regresjon.log`).

## #uavhengig

Korpus v2: 264 nye meldinger fra fire **nye** personaer (student, saksbehandler i kommune på nynorsk, idrettslagsleder som dikterer, utvikler med norsk som andrespråk), 33 etiketter à 8, halvt bokmål/nynorsk og halvt engelsk. Generert **etter** at graf v3 var frosset; ingen grafendring er begrunnet med dem. Tolken (haiku, opake id-er) var enig i 261 av 264 (98,9 %).

| Korpus v2, alle 264 (`rapport/foer-k2/`, `rapport/graf-v3-k2/`) | før | graf v3 |
|---|---|---|
| Top-1 (positive, n=208) | 20 % [14–25] | **28 % [23–35]** |
| Top-1 eller spurte med riktig valg | 25 % | 32 % |
| R@3 | 25 % | 36 % |
| MRR | 0,23 | 0,34 |
| Negativer uten handling (n=24) | 92 % | 88 % |
| Meldinger vunnet / tapt | | 18 / 1 |

**Forbedringen holder, men den er mindre enn holdout i v1 lovet: +8 prosentpoeng, ikke +20.** Holdout i v1 kom fra de samme fire personaene som treningsradene, og delte ordvalg med dem. Nye skribenter viser hva grafen faktisk har lært.

Hvor gevinsten kom: hjelpere med tydelige verb (video 2→7 av 8, gjøremål 2→5, onboarding 1→3, påminnelse 2→3), diagram 0→2, profilside 1→3. Hvor den ikke kom: kart, entiteter, publisering og musikk (alle 0 av 8 før og etter), avstemning (0/8). Indirekte meldinger: 4 → 9 av 86 (5 % → 10 %).

Tapt: `k2-0063` «bare så du vet, ikke gjør noe med det ennå: lurer på om vi skal flytte styremøtene til tirsdager …» ble et møteforslag med v3. Brukeren sa eksplisitt «ikke gjør noe». Det er en ekte regresjon med kjent årsak: møtegjenkjenningen (`scheduleMeetingIntentScore`) har aldri sjekket nektelse, i motsetning til de andre hjelperne, og v3 la til ukedager som tidsord, så «styremøtene … tirsdager» ble nok for et forslag. Graf v3 gikk i prod uten rettingen. Rettingen (graf v3.1, PR #258, ikke merget) er begrunnet med regelen de andre hjelperne allerede følger og treningsradene k1-0095/k1-0096, ikke med k2-0063. Målt 2026-09-24 (`rapport/graf-v3.1/`): korpus v1 uendret, korpus v2 top-1 28 % uendret, negativer 88 % → 92 %, ingen positive tapt. k2-0063 er dermed ikke lenger en uavhengig sjekk av akkurat denne oppførselen.

Per persona (top-1 positive, før → v3, av 52): student 10→17, saksbehandler 9→11, idrettslagsleder 13→18, utvikler 9→13.

## #kallimachos

Samme løp, bare adapteren byttet: `KallimachosCapabilityIndex.matchPurposes` i stedet for Butlers analyse. 96 meldinger mot 17 formål (+ 11 «ingen»), tolken enig i 96,9 %. Ingen endringer i Kallimachos; dette er utgangspunktet.

| Kallimachos v1 (`rapport/foer/`, `kallimachos-v1`) | Alle | Holdout |
|---|---|---|
| Riktig formål øverst (positive) | 32 % [22–42] | 17 % [0–33] |
| Riktig formål blant tre øverste | 44 % | 33 % |
| MRR | 0,38 | 0,28 |
| «Ingen» uten treff | 73 % | 100 % |

## Tester fra FORMAALSSPEC §5

| Test | Status | Bevis |
|---|---|---|
| test.fs.foer-etter-holdout | grønn | tabellen over; holdout rapportert for seg |
| test.fs.negativer | grønn | negativer 94 % → 94 %, holdout 100 % → 100 % |
| test.loep.endring-har-grunn | grønn | `grafendringer/GRAFENDRINGER-v3.md`: hver endring med treningsradene den retter |
| test.loep.en-kommando | grønn | `HAVEN-Deploy/_handoff/WP-R/wp-butler-maaling-v2.sh <variant>` |
| test.loep.korpus-fordeling | grønn | 33 etiketter à 12 (v1) og à 8 (v2), nb/en 2:1 (v1) og 1:1 (v2) |
| test.loep.lokkeduer-avsloeres | venter | Dommerbenken er publisert; Kjetil har ikke dømt ennå |
| test.loep.stikkproeve | venter | samme |
| test.metode.kallimachos-toerrkjoering | grønn | `#kallimachos` over |
