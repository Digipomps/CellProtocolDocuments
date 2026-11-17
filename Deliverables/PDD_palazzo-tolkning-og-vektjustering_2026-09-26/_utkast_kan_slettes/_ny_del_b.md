## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.native.tree-list | A1 native-tre-liste | CellApple-tester som bygger en `SkeletonList` med `childrenKeypath`, og sjekker: lukket når `expandedStateKeypath` gir `[]` eller ikke kan løses; alt åpent når feltet mangler; åpne/lukke endrer bare synlige rader og sender ingenting til cellen | TESTRESULT.md#native-tree | venter |
| test.native.tree-parity | A1 | Samme skjelett og data i Porthole (eksisterende `playwright/skeleton-list-tree.spec.js`) og i native: samme synlige rader i samme rekkefølge, lukket og åpen | TESTRESULT.md#native-tree | venter |
| test.cell.reaction-row | A2 reaksjon-lesbar | Ingen reaksjon → 0 rader. Ett trykk → 1 rad med emnene frosset på posten. To trykk → raden viser det siste. Huset endrer emnene på artikkelen etterpå → raden er uendret | TESTRESULT.md#cell | venter |
| test.cell.auth-negative | A2 | Annen requester, feil keypath og `purpose://prompt.unknown` blir alle avvist | TESTRESULT.md#auth | venter |
| test.skeleton.no-unreachable-elements | A3 artikkelflate | `SkeletonReachabilityAudit` på artikkelkonfigurasjonen. Ingen funn, og de tre reaksjonsknappene og kommentarfeltet er nåbare | TESTRESULT.md#reachability | venter |
| test.article.row-refresh | A3 | I kjørende flate, fra artikkel uten reaksjon: (1) «Interessant» → én lukket rad; (2) åpne raden, trykk «Vil smake» → raden viser «Vil smake» og er fortsatt åpen; (3) «Ikke for meg» → teksten fra avvik 2; (4) «Vil smake» igjen → positiv tekst. Ingen navigering ut og inn mellom trinnene. Skjermbilde per trinn, i Binding. | ACCEPT.md#parity | venter |
| test.gui.parity | A4 | Skjermbilder i samme viewport ved siden av referansen, med avvikene fra §3 listet | ACCEPT.md#parity | venter |
| test.weights.last-tap-decides | B1 | [Ikke for meg, Vil smake] → artikkelen er ikke stengt. [Vil smake, Ikke for meg] → stengt. [Ikke for meg, Interessant, Ikke for meg] → stengt | TESTRESULT.md#weights | venter |
| test.weights.veto-article-only | B2 | «Ikke for meg» på caponata. En rett med «oliven» er ikke stengt, men summen for den er lavere enn uten trykket. Selve artikkelen er stengt | TESTRESULT.md#weights | venter |
| test.weights.threshold | B3 | Innhold under terskelen blir ikke anbefalt. Innhold på eller over blir det | TESTRESULT.md#weights | venter |
| test.weights.monotone | B3 | (a) Et positivt trykk på en *annen* artikkel senker aldri summen for innhold med felles emne. (b) Et sterkere trykk («Vil smake») gir aldri lavere sum enn et svakere («Interessant») på samme plass i rekken. Kjøres på mange tilfeldige rekker med fast frø, slik at kjøringen kan gjentas. | TESTRESULT.md#weights | venter |
| test.weights.repeat-bounded | B (kjernen) | «Vil smake» én, to og tre ganger på samme artikkel. Vekten øker ikke over en øvre grense, og den er ikke summen av trykkene | TESTRESULT.md#weights | venter |
| test.weights.sign-follows-last | B1 | Etter [Ikke for meg, Vil smake] teller emnene for, ikke mot. Etter [Vil smake, Ikke for meg] teller de mot. Gjelder begge modellene i §6 spm. 2 | TESTRESULT.md#weights | venter |
| test.weights.policy-single-source | B4 | Søk etter tallkonstanter i graf- og matcherfilene. Ingen vekter eller terskler utenfor `PalazzoWeightPolicy` | ACCEPT.md#policy | venter |
| test.maal.produksjonsvei | B5 vektbenk | Benken kaller `PalazzoSignalGraphMatcher.match` med policyen, ikke en kopi av logikken | TESTRESULT.md#bench | venter |
| test.bench.inert-by-default | B5 | Uten miljøvariabelen `PALAZZO_WEIGHT_BENCH_PATH` gjør benken ingenting og skriver ingenting | TESTRESULT.md#bench | venter |
| test.bench.has-null-reference | B5 | Tabellen har en kolonne «dagens oppførsel» målt på `f548282`. Et parametersett som gir samme tabell som dagens, er merket som likt | `maaling/vektbenk-v1.md` | venter |
| test.principles | prinsipper-holder | Uavklart ved utløpt budsjett, bare `source == "self"`, veto for artikkelen og ingen ny anbefaling av en artikkel hun allerede har reagert på. Én test per prinsipp, nye eller eksisterende, navngitt | TESTRESULT.md#principles | venter |
| test.build | quality | `swift build` i CellProtocol og PalazzoScaffold. Binding-bygg for A4 | TESTRESULT.md#build | venter |
| test.regression | quality | Hele testmengden på ren eksport av utgangsrevisjonen mot arbeidstreet (`land-cellprotocol.sh`, og `test-vetofelle.sh`-mønsteret for Palazzo) | TESTRESULT.md#regression | venter |
| test.docs-updated | quality | Kodekommentarene i graf og matcher, pluss skjelettdokumentasjonen for native støtte av `childrenKeypath` | ACCEPT.md#docs | venter |
| test.status-current | quality | STATUS.md mot filene i mappen | ACCEPT.md#status | venter |

## 6. Åpne spørsmål til Kjetil

Ordforklaring: *matcheren* er koden som avgjør hva gjesten tilbys. *Benken* er en testkjøring med oppdiktede gjester som viser hva hver av dem ville fått. *Vekt* er hvor sterkt et emne teller.

1. Når du har valgt tall fra benken: skal de ligge fast i koden, eller skal gjesten selv kunne endre dem? Anbefaling: fast i koden nå. Det er enklest å teste og å forklare, og kan åpnes senere som et eget formål.
2. **Hva gjør et nytt trykk med emnene?** (a) Siste trykk bestemmer om emnene teller for eller mot, og styrken glir mot det nye trykket. (b) Et motsatt trykk nullstiller emnene og starter på nytt fra det nye trykket. Anbefaling: (a), fordi det følger «siste trykk gjelder» og samtidig lar flere trykk justere. Benken kjører begge.
3. **Skal vekten også avgjøre om noe tilbys, eller bare rekkefølgen?** I dag er ett positivt trykk med et felles emne nok, og vekten brukes ikke. Bare rekkefølge endrer minst for gjester som aldri trykker to ganger. En terskel gjør at svake trykk ikke alene fører til tilbud. Anbefaling: begynn med bare rekkefølge. Benken viser også terskelverdier, så du kan se forskjellen.
4. Benkens simulerte gjester: jeg foreslår seks, hver med sitt eget formål. Én ombestemmer seg, én liker Palermo men ikke fritert mat, én er vegetar, én trykker mye «Interessant» og aldri noe annet, én gir bare «Ikke for meg», og én trykker samme knapp flere ganger. Legg gjerne til flere eller endre dem.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-26 | Opprettet | Losen |
| 1 | 2026-09-26 | §0–§3, §5 og §6 skrevet fra G1-GUI-valget (B), Kjetils tre svar og kildelesning. Rettelse: den native rendereren ligger i CellProtocol/CellApple, ikke i Binding. | Losen |
| 2 | 2026-09-26 | Fabels gjennomgang: B3 merket som Losens slutning og flyttet til §6. Modellen for fortegn og styrke er gjort til et valg. Monotonitesten er rettet, så den ikke motsier glidende vekt. Nye tester: repeat-bounded og sign-follows-last. Row-refresh er utvidet. Hvert avvik har egen godkjent-rute. Beslutningsboksen og ordforklaringen er lagt til. | Losen |
