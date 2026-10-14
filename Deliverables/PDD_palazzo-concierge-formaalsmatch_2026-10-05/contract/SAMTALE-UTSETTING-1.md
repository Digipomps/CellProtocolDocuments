# Det nye kallet i utsetting 1: hva det svarer, og hva det lar stå som i dag

Skrevet 7. oktober 2026 av Losen, etter G2. Andre utgave samme dag kl. 14:47 UTC, etter at reglene ble skrevet utenfor Swift, kjørt på husets egne data, og lest av to uavhengige tråder (se «Endret i andre utgave» sist). Stier er relative til HAVEN-roten; `PS` står for `PalazzoScaffold`. Dette er arbeidspakke 5 og 6 i `../PLAN.md` gjort presise nok til å skrive tester av. Det legger ikke til formål. Der planen ikke sa hva som skjer, er valget mitt merket **Valgt her**, og står samlet sist så Kjetil kan si nei.

Reglene finnes i to utgaver skrevet hver for seg: `../maaling/prototype/samtale_sim.py` (utenfor Swift) og `PS/Sources/App/Services/PalazzoSamtale.swift`. `PS/Tests/AppTests/PalazzoSamtaleReferanseTests.swift` krever at de gir det samme på 162 samtaler med 402 steg. Per 14:47 UTC er Swift-utgaven skrevet og ikke kompilert. Datafilen er versjon `husgraf-20261007.4`.

Utsetting 1 har matchen (F2), svarene (F6), samtalen (F5) og siden. Den nye allergenveien (F8) og modellen bak (F3) kommer i utsetting 2 og 3. Dette dokumentet sier derfor også hva kallet gjør med setninger som hører til dem: de får det conciergen svarer i dag.

## Rekkefølgen for en setning (`query`)

| # | Steg | Utfall |
|---|---|---|
| 1 | Forespørselen leses etter `README.md` her | 400 eller 422 ved feil. Er `graph_version` en annen enn tjenestens, fjernes det gjesten liker og har valgt, det hun unngår står, og svaret sier det. Mangler `graph_version` når noe er notert, er formen feil (400) |
| 2 | Strakstiltaket: har setningen et ord fra listen (`PS/Sources/App/Services/PalazzoAllergiHenvisning.swift`), eller leser dekomponeringen at den handler om et allergen eller om noe gjesten ikke tåler | Henvisningen til personalet, ordrett som i dag (`kind: refused`). Det setningen sier at gjesten unngår, noteres (`taaler-ikke` eller `spiser-ikke`), så resten av samtalen er uten tilbud. Se «Steg 2 i detalj» |
| 3 | Dekomponeringen (F1) | Formål, og interesser med fortegn og ordene som traff |
| 4 | Vin og alkohol: setningen har et ord fra listene i `PS/Sources/App/Services/PalazzoConciergePhrasing.swift` (`neverRephrasedTerms`, `neverRephrasedWords`), eller en interesse er en drikk med alkohol, et emne som bare fører til slike (vin, øl), eller en alkoholfri utgave av en slik drikk (se regel 3: Carlsberg Free, Alkoholfri vin og Alkoholfri Gin Tonic) | Som i dag (`kind: answer`): setningen går til oppslaget slik `ask` gjør. Ingenting noteres |
| 5 | Det setningen sier om gjesten selv, noteres: `liker`, `liker-ikke`, `spiser-ikke`. Et spørsmål (`spoer-om`) noterer ingenting. Et ønske om et emne («noe med ost») noteres ikke; et ønske om en rett ved navn noteres i steg 8 | `noted` i svaret er listen etter dette |
| 6 | Står det en post av slaget `taaler-ikke` eller `spiser-ikke` i `noted` | Ingen tilbud og ingen liste fra matchen. Sier setningen bare hva gjesten ikke spiser eller ikke liker, er svaret en kvittering. Ellers som i dag (`kind: answer`). Listene med merking kommer med F8 |
| 6b | Formålet er bord eller åpningstid | Som i dag (`kind: answer`), også når setningen nevner noe huset har |
| 7 | Setningen sier bare noe gjesten ikke liker | Kvittering (`kind: receipt`) |
| 8 | Setningen nevner en rett eller en drikk uten alkohol ved navn | «Vil ha»: kvitteringen som etter et ja (`receipt`). «Liker», eller en drikk (som ikke har noen beskrivelse å fortelle): tilbud (`offer`). Ellers forteller svaret om den (`tell`): navnet og beskrivelsen ordrett, i formen `ask` bruker for én rett i dag |
| 9 | Setningen har emner: matchen (F2) regner med dem og med det som er notert | Leder én post klart: tilbud (`offer`). Flere: forteller (`tell`). Ingen når terskelen: bom. Bare poster som nås av noe setningen selv nevner, står i svaret |
| 10 | Bom, eller dekomponeringen fant ingenting huset har (småprat, ukjente ord) | Som i dag (`kind: answer`): oppslaget, publiseringen og formuleringen slik `ask` gjør det. Spørsmålet om modellen kommer i utsetting 3 |

«Som i dag» er samme kode som `ask` kaller, ikke en kopi. Svaret har de 13 nøklene derfra, og de nye feltene i tillegg. `PS/Tests/AppTests/PalazzoSamtaleFasadeTests.swift` holder de 13 nøklene mot det `ask` svarer på samme setning, også når modellen har formulert teksten.

### Steg 2 i detalj

Henvisningen kommer i fire tilfeller:

1. Setningen har et ord fra strakstiltakets liste. Grunnen i loggen er `ordliste`, som for `ask`.
2. Dekomponeringen sier at setningen handler om allergi: den sier at noen ikke tåler noe, har et ord for allergi, eller nevner et allergen. Husets graf kjenner flere ord for allergener enn listen gjør. 78 av de 168 ordene i versjon `husgraf-20261007.3` treffer ikke listen: skrivemåter på nynorsk og dialekt («mjøl», «mjelk», «fesk»), og dansk, svensk, tysk og italiensk («nødder», «ägg», «weizen», «uova», «seleri»). De får samme svar som listens ord, også de ni som er skrivemåter av «fisk» og «selleri», som er emner i grafen i tillegg. Grunnen er `dekomponering`. Unntaket er når gjesten sier at hun liker eller vil ha noe med et slikt ord («Jeg liker mælk»): da finner dekomponeringen ingenting huset har, og oppslaget svarer som i dag.
3. Setningen sier at gjesten ikke tåler eller ikke spiser et allergen, eller ikke tåler noe annet.
4. Formålet er å unngå noe, og grafen vet ikke hva («Jeg er vegetarianer»). Da noteres noden `ukjent`.

Det som noteres: et allergen er alltid `taaler-ikke`, også når gjesten skrev «uten gluten» eller «spiser ikke». Kontrakten har ingen annen plass for et allergen i `noted`. Et emne beholder slaget gjesten brukte. En rett eller drikk hun ikke tåler, og alt grafen ikke kjenner, blir noden `ukjent`. Det hun liker eller ikke liker i samme setning, noteres ikke: svaret er henvisningen, og den sier ingenting om det.

### Det som er notert

- Samme post står én gang.
- Om det hun liker, gjelder det siste hun sa: «liker ost» og så «liker ikke ost» gir «liker ikke ost».
- Det strengeste står. En node med `taaler-ikke` får ikke `spiser-ikke`, `liker` eller `liker-ikke` ved siden av seg, og en node med `spiser-ikke` får ikke `liker` eller `liker-ikke`.
- Listen har høyst 24 poster. Er den full, går det eldste som ikke er noe hun unngår, ut. Er alt noe hun unngår, står listen som den er.
- Tjenesten holder ingenting. Listen kommer med hvert kall og går tilbake i svaret. Siden sender bare `kind` og `node` for hver post; `label` er svarets, og en post med ekstra felt avvises (422).
- En drikk med alkohol, eller en alkoholfri utgave av en (regel 3), kan ikke stå notert (422). Svaret gir merkelappen tilbake, og vakten nevner aldri en slik drikk, heller ikke på den veien.

### Notater laget mot en annen versjon av grafen

Er `graph_version` en annen enn tjenestens, fjernes det gjesten liker og har valgt, uten at det leses. **Det hun unngår, står:** en node grafen fortsatt har, beholdes, og en node den ikke har lenger, blir noden `ukjent`. Poster som ikke lar seg lese (ukjent slag, ekstra felt, fritekst), fjernes uten feil: de er laget mot en graf tjenesten ikke har, og kan ikke holdes mot noe. Svaret sier hva som skjedde, først blant advarslene, foran linjen om allergener. **Valgt her.** Kontrakten sier at notatene kastes. Med det kunne en gjest som har sagt «Jeg tåler ikke nøtter», få et tilbud i neste svar fordi menyen ble oppdatert midt i samtalen.

Mangler `graph_version` når `noted` har poster, er formen feil (400): siden får versjonen fra `GET samtale` og sender den med hvert kall. En tom `noted` uten versjon er i orden.

## Regler

1. **Matchen først, så dagens oppslag.** Forstår dekomponeringen noe huset har, svarer grafen. Dagens oppslag svarer når den ikke gjør det. **Valgt her.**
2. **Tilbud bare når én post leder klart.** Det er når bare én post når terskelen, eller den sterkeste har minst `klar_leder` ganger summen til den neste. Tallet står i grafens data (2,5 i versjon `husgraf-20261007.3`) og er foreløpig: bildene fastsetter bare at «ost» gir et tilbud (5,6 ganger) og «pistasj» ikke (1,02 ganger). **Valgt her.** Tabellen «Hva tallet for klar leder gjør» viser hva det betyr for hvert emne.
3. **Et tilbud peker aldri på en drikk med alkohol** (regel 4 i kontrakten), og en drikk med alkohol står aldri i en liste fra matchen (steg 4 tar setningen først). Det samme gjelder en alkoholfri utgave av en slik drikk: en drikk som nås fra et emne med et alkoholemne i navnet («alkoholfritt øl», «alkoholfri vin»), eller som selv har et ord for alkohol i navnet, med samme ordliste som holder setninger unna modellen. I korpuset er det Carlsberg Free, Alkoholfri vin og Alkoholfri Gin Tonic. «Har dere alkoholfritt øl?» går alt som i dag fordi setningen har ordet alkohol, og «Har dere Carlsberg Free?» er samme spørsmål ved navn. **Valgt her.** En rett med vin i beskrivelsen er ikke en drikk og kan tilbys (valg 14). Dagens Mocktail, brusen, eplemosten og vannet tilbys.
4. **Et «liker ikke» trekker ned og stenger ikke.** Det som er notert som `liker`, regnes med som interesse; `liker-ikke` regnes med negativt fortegn. Spør setningen selv etter emnet («Har dere oster?»), gjelder spørsmålet, ikke det som er notert om samme emne.
4b. **Det som er notert, teller med i summen, men bringer ikke inn en rett alene.** Har gjesten sagt «Jeg liker ost» og sier så «Jeg liker lam», er svaret lammet. Osteretten står ikke i svaret, for setningen nevner ikke ost. Uten denne regelen sto osteretten først i svaret på «Jeg liker pistasj». **Valgt her.**
5. **Ved likt tall** står en post med et emne gjesten ikke liker, etter de andre (valg 19).
6. **Et ja bestiller ikke.** Et `choice` med `ja` legger en post `vil-ha` i `noted` og gir en kvittering. Ingen nøkkel for bestilling kalles, og ingen celle: testen tar bort husets identitet og får kvitteringen likevel. Står det noe gjesten unngår, noteres ikke et ja. Hun får henvisningen.
7. **Teksten bygges av vakten.** Navn og beskrivelse er postens felt ordrett. Ingen modell kalles for tilbud, forteller eller kvittering (`test.match.avgjoerelsen`, `test.dekomp.uten-modell`). Svar «som i dag» formuleres som i dag, med de lukkede spørsmålene `ask` har. At dekomponeringen avgjør hva modellen får formulere (valg 13), er en egen del av arbeidspakke 5 og bygges etter dette.
7b. **Bare en bekreftet post nevnes.** Posten må ha en plass på menyen (tabellen under), være bekreftet av et menneske og ikke merket for ny gjennomgang, ha kilde og dato, og for en drikk være bekreftet tilgjengelig. Kildene i svaret er postenes, og går gjennom samme kontroll som i `ask`. Slipper ikke kilden gjennom, svarer oppslaget som i dag.
8. **Linjen om allergener** står først blant advarslene i hvert svar som nevner en rett eller en drikk, i de tre formene koden på nett har; bare linjen om at menyen er oppdatert (over) står foran den. Til Kjetil har valgt (valg 21), står den også under kvitteringene.
9. **Ingen svartype sier at noe er trygt, uten noe eller fritt for noe.**

## Ordlyden

Fra bildene (`../images/kilde/tilstander.js`), ordrett. ⟨navn⟩ og ⟨beskrivelse⟩ er postens felt.

| Svar | Tekst |
|---|---|
| Tilbud, rett | «Vi har ⟨navn⟩: ⟨beskrivelse⟩ ⟨spørsmål⟩» |
| Tilbud, drikk | «Vi har ⟨navn⟩. Vil du ha det å drikke?» |
| Forteller, flere | «Vi har ⟨antall⟩ ⟨hva⟩:» og så én linje per post: «⟨navn⟩ (⟨plass⟩): ⟨beskrivelse⟩» |
| Kvittering, liker ikke | «Notert: du liker ikke ⟨emne⟩. Jeg foreslår helst andre retter. Spør du om ⟨emne⟩, får du svar likevel.» |
| Kvittering, ja | «Notert: du vil ha ⟨navn⟩ ⟨når⟩. Jeg kan ikke bestille for deg, og kelneren ser ikke dette. Si det til kelneren når du bestiller.» |
| Fjernet én | «Fjernet: «⟨det som sto⟩». Jeg regner ikke lenger med det.» |
| Fjernet alt | «Alt er fjernet. Jeg husker ingenting av det du har sagt om deg selv.» |
| Slik forsto jeg deg | «du ⟨verb⟩ ⟨navn⟩ og …»: liker, liker ikke, tåler ikke, spiser ikke, vil ha, spør om, nevner, «vil ha noe annet enn». Uten interesser, etter formålet: «du spør om noe huset har.», «du spør om bord.», «du spør om åpningstidene.», «du vil ha noe å spise.», «du vil ha noe å drikke.», «du vil unngå noe.» |
| Merkelappene | «liker ost», «liker ikke ost», «tåler ikke nøtter», «spiser ikke kjøtt», «vil ha Formaggi misti til dessert» |

| Plass på menyen (korpusets kategori) | ⟨spørsmål⟩ i tilbudet | ⟨når⟩ i kvitteringen | ⟨plass⟩ i forteller |
|---|---|---|---|
| `antipasti` | «Vil du ha det til forrett?» | «til forrett» | «forrett» |
| `primi` | «Vil du ha det som pastarett?» | «som pastarett» | «pastarett» |
| `secondi` | «Vil du ha det til hovedrett?» | «til hovedrett» | «hovedrett» |
| `dolce` | «Vil du ha det til dessert?» | «til dessert» | «dessert» |
| `pizze` | «Vil du ha den?» | (ingenting) | «pizza» |
| `non_alcoholic` | «Vil du ha det å drikke?» | «å drikke» | «drikke» |

## Det bildene ikke viser, og som trengs i utsetting 1

Hver av disse er ny ordlyd. De står i svarene til Kjetil har sett dem ved G3, og er samlet i `ACCEPT.md` da.

| Tilfelle | Tekst | Hvorfor |
|---|---|---|
| Forteller om én navngitt rett | «⟨navn⟩: ⟨beskrivelse⟩» | Bilde 3 viser to retter under en overskrift. For én rett gjesten selv nevner, er dette formen `ask` svarer med i dag |
| Forteller, når overskriften ikke kan bygges av ett emne | «Dette har vi som passer til det du skrev:» | «Vi har to retter med pistasj» lar seg ikke si om «sterk», «sicilia» eller to emner samtidig. Emnene som har en egen form («desserter», «pizzaer», «retter med pistasj»), står i grafens data |
| Forteller om drikke | «⟨navn⟩ (drikke).» per linje | Drikke har ingen beskrivelse i menyen |
| «Nei takk» til et tilbud | «Greit. Da noterer jeg ingenting.» | Bildene viser bare ja |
| Kvittering, spiser ikke | «Notert: du spiser ikke ⟨emne⟩. Jeg foreslår derfor ingen retter selv. Spør personalet om hva som passer.» | Bilde 7A lover en liste over hva som nevner kjøttvarer. Den kommer med F8 og loves ikke før |
| `noted` kastet fordi grafen er ny | «Menyen er oppdatert siden du begynte. Det som var notert, er fjernet.» som første advarsel | Kontrakten sier at svaret sier det, ikke hvordan |
| Det samme, når noe gjesten unngår, står igjen | «Menyen er oppdatert siden du begynte. Det du unngår, står notert. Resten er fjernet.» | Se «Notater laget mot en annen versjon av grafen» |
| Merkelappen for noe gjesten unngår, som grafen ikke kjenner | «unngår noe conciergen ikke kjenner igjen» | Valg 20: ordet lagres ikke. Første utgave hadde «tåler ikke noe …». Det ble feil for «Jeg er vegetarianer» |
| Kvittering når det står noe hun unngår, og setningen bare sier hva hun ikke liker | «Notert: du ⟨det som står notert om det hun nevnte⟩.», som «Notert: du liker ikke ost.» | Kvitteringen i bildet lover «andre retter», og det stemmer ikke når conciergen ikke foreslår noe. Uten denne svarte oppslaget med osteretten på «Jeg liker ikke ost» |
| Fjern noe det ikke står noe notert om | «Det står ingenting notert om dette.» | To trykk på samme knapp, eller en liste siden har fra før menyen ble oppdatert, er ikke en feil. Siden får listen slik den er |

## Hva tallet for klar leder gjør

Regnet utenfor Swift (`../maaling/prototype/husmatch_sim.py`) for hvert emne der mer enn én post når terskelen. De 61 andre emnene fører til én post og gir et tilbud uansett tall. Forholdet er summen til den sterkeste posten delt på summen til den neste.

| Emne | Poster over terskelen | Forhold | Med 2,0 | Med 2,5 | Med 3,0 |
|---|---|---|---|---|---|
| ost | 3 | 5,56 | tilbud | tilbud | tilbud |
| sitron | 5 | 2,85 | tilbud | tilbud | forteller |
| sjømat | 3 | 2,05 | tilbud | forteller | forteller |
| dessert | 3 | 2,00 | tilbud | forteller | forteller |
| mozzarella | 4 | 1,55 | forteller | forteller | forteller |
| pizza | 5 | 1,50 | forteller | forteller | forteller |
| tomat | 4 | 1,50 | forteller | forteller | forteller |
| olivenolje | 2 | 1,48 | forteller | forteller | forteller |
| forrett | 5 | 1,45 | forteller | forteller | forteller |
| fisk | 3 | 1,37 | forteller | forteller | forteller |
| salami | 2 | 1,24 | forteller | forteller | forteller |
| kjøtt | 5 | 1,21 | forteller | forteller | forteller |
| pasta | 2 | 1,12 | forteller | forteller | forteller |
| kapers | 3 | 1,12 | forteller | forteller | forteller |
| asparges | 2 | 1,07 | forteller | forteller | forteller |
| sicilia | 5 | 1,03 | forteller | forteller | forteller |
| bronte | 2 | 1,02 | forteller | forteller | forteller |
| hovedrett | 3 | 1,02 | forteller | forteller | forteller |
| pistasj | 2 | 1,02 | forteller | forteller | forteller |
| alkoholfritt | 11 | 1,00 | forteller | forteller | forteller |
| brus | 5 | 1,00 | forteller | forteller | forteller |
| mocktail | 2 | 1,00 | forteller | forteller | forteller |
| potet | 3 | 1,00 | forteller | forteller | forteller |
| øl | 6 | 1,00 | forteller | forteller | forteller |

Øl er med i tabellen, men får aldri et tilbud eller en liste fra matchen: steg 4 tar setningen først. «alkoholfritt» når matchen bare med skrivemåter uten ordet alkohol («alkofri», «alc free», «uten alk»; 5 av 27 ordformer): da er svaret listen over de ni drikkene som ikke er øl, vin eller en alkoholfri utgave av dem, under overskriften «Dette har vi som passer til det du skrev:». Med ordet alkohol i setningen svarer oppslaget som i dag. «sjømat», «fisk» og «selleri» står på strakstiltakets liste, så en setning med ordene får henvisningen (steg 2) og når ikke matchen i utsetting 1. «dessert» ligger på 2,00 fordi osteretten har færre emner enn de to andre dessertene, ikke fordi den er mer dessert.

## Feil

Feil form gir 400, innhold tjenesten ikke kan bruke gir 422, og en setning over 1200 tegn gir 413. Svaret er `{"error": true, "reason": …}`, og teksten har aldri noe av det gjesten sendte.

| Status | Når | Tekst |
|---|---|---|
| 400 | Ikke JSON, eller ikke et objekt | «Send et JSON-objekt.» |
| 400 | Et felt kontrakten ikke har | «Forespørselen har et felt tjenesten ikke kjenner.» |
| 400 | Både `query` og `choice`, eller ingen av dem | «Send enten en setning i feltet query eller et valg i feltet choice.» |
| 400 | `query`, `noted`, `graph_version` eller `choice` har feil type | «Feltet ⟨navn⟩ skal være ⟨type⟩.» |
| 400 | `noted` har poster, og `graph_version` mangler | «Feltet graph_version mangler.» |
| 422 | Tom setning | «Skriv et spørsmål før du sender.» |
| 422 | `model_consent` har en annen verdi enn de tre kontrakten har | «Feltet model_consent har en verdi tjenesten ikke kjenner.» |
| 422 | En post i `noted` med ukjent slag, ukjent node, ekstra felt eller fritekst, eller en drikk fra regel 3 | «Det som var notert, kunne ikke leses.» |
| 422 | Flere enn 24 poster i `noted` | «Det kan stå høyst 24 ting notert.» |
| 422 | Et valg med feil eller ekstra felt, eller som peker på en node som ikke finnes | «Valget kunne ikke leses.» |
| 422 | Et valg kontrakten ikke har i denne utgaven (`model`) | «Valget finnes ikke.» |
| 422 | Ja eller nei til en rett eller drikk som ikke finnes, ikke kan nevnes, eller har alkohol | «Tilbudet finnes ikke.» |
| 413 | Setningen er over 1200 tegn | «Forespørselen er for stor. Bruk maksimalt 4096 byte og 1200 tegn i spørsmålet.» |

Fartsgrensen (429), 4096 byte (413) og `application/json` (415) er mellomvaren `ask` har, uendret.

Gjestens JSON leses med en egen leser som bare tar tekst, lister og objekter, og bare så dypt som kontrakten går. Den leses aldri som `ValueType`: den typen har innpakkede former (`&cell`, `&cellConfiguration`) som ikke hører hjemme på en åpen flate.

## Bryteren og `GET /palazzo/api/samtale`

Kallet finnes bare når miljøvariabelen `PALAZZO_CONCIERGE_SAMTALE` er `1` og husets graf lar seg lese med avsnittet `svar`. Ellers svarer både `POST` og `GET` 404, og de fem rutene fra før er uendret. Er variabelen `1` og grafen ikke kan brukes, sier loggen hvorfor.

`GET /palazzo/api/samtale` svarer `{"schema", "graph_version", "noted_max"}`. Siden spør der om kallet finnes, og får versjonen notatene skal lages mot. **Valgt her**; kontrakten sier bare at kallet svarer 404 når det er av.

## Loggen

Én linje per svar: `concierge-formulering handling=samtale utfall=<vei>:<grunn>`.

| Vei | Grunn | Når |
|---|---|---|
| `match` | `offer`, `tell` | Vakten har bygget svaret av husets graf |
| `kvittering` | `noted`, `removed`, `answered` | En kvittering. `answered` er «nei takk» og «det står ingenting notert om dette» |
| `henvist` | `ordliste`, `dekomponering`, `notert-unngaar`, `merking` | Henvisningen til personalet. `merking` er regel 2 i strakstiltaket: oppslaget svarte med merkingen |
| `oppslag` | `alkohol`, `notert-unngaar`, `formaal`, `bom`, `upubliserbar` | Oppslaget svarte og svaret er publisert. Grunnen er hvorfor matchen ikke svarte. Linjen har i tillegg `formulering=<utfall>`, med samme verdier som for `ask` |
| `avvist` | de samme | Oppslaget svarte med en avvisning |

`oppslag` er ny i forhold til kontrakten, som ikke hadde en vei for svar «som i dag». En bom har i tillegg linjen `concierge-bom grunn=<miss_reason> graf=<versjon> noder=0`. Ingen linje har noe gjesten skrev; testen sender setninger med egne ord og leter etter dem i loggen.

## Valgt her: det Kjetil kan si nei til

1. Matchen svarer før dagens oppslag i det nye kallet (regel 1). Det andre er omvendt: dagens oppslag først, og matchen bare når oppslaget avviser.
2. Tallet for «leder klart» er 2,5 (regel 2). «dessert» ligger nøyaktig på 2,0, så med 2,0 ville «Hva har dere til dessert?» gitt osteretten alene. Med 3,0 ville «Jeg liker sitron» gitt fem retter i stedet for sitronkremen. (Første utgave brukte «sjømat» som eksempel. Det ordet står på strakstiltakets liste og når ikke matchen.)
3. Etter «tåler ikke» og «spiser ikke» gir utsetting 1 ingen tilbud og ingen liste fra matchen (steg 2 og 6). «Tåler ikke» gir henvisningen til personalet, ordrett som i dag. Sier setningen bare hva gjesten ikke spiser eller ikke liker, er svaret en kvittering; ellers svarer conciergen som i dag. Listene i bilde 4C, 6 og 7A kommer i utsetting 2.
4. En setning der gjesten sier at hun ikke tåler noe, noteres alt i utsetting 1, selv om svaret er henvisningen som i dag. Uten det kunne et tilbud komme senere i samme samtale, og det er en av tingene som stopper en utsetting.
5. Ordlyden i tabellene over.
6. En setning som nevner et allergen med et ord grafen kjenner og listen ikke har, får henvisningen (steg 2, tilfelle 2). Det andre er at bare listens ord gir henvisningen, som for `ask`. Da svarte conciergen «Notert: du liker ikke nøtter» på «Jeg liker ikke nødder» uten å notere noe, og «Har dere seleri?» ga et tilbud om blekksprutcarpaccioen mens «Har dere selleri?» ga henvisningen.
7. Alkoholfrie utgaver av øl, vin og brennevin går som øl og vin, også ved navn (regel 3). Det gjelder Carlsberg Free, Alkoholfri vin og Alkoholfri Gin Tonic. Dagens Mocktail og brusen tilbys. Alkoholloven § 9-2 forbyr også reklame for andre varer med samme merke som en drikk med alkohol; hvor grensen går for et tilbud fra en concierge, er ikke min avgjørelse. Vil du at de tre skal tilbys, sier du det.
8. Det gjesten unngår, står når grafen er ny (se «Notater laget mot en annen versjon av grafen»). Det andre er kontraktens: alt kastes, og svaret sier det.
9. Det som er notert, bringer ikke inn en rett alene (regel 4b).
10. En rett gjesten sier at hun liker, ved navn, gir et tilbud om den («Jeg liker Arancini»). En drikk ved navn gir et tilbud også når hun bare spør, fordi drikke ikke har noen beskrivelse å fortelle.
11. Fjern noe det ikke står noe notert om, gir en kvittering og ikke en feil.
12. Bord og åpningstid svarer oppslaget på (steg 6b), også når setningen nevner en rett.
13. `GET /palazzo/api/samtale` finnes.
14. Noe notert uten `graph_version` er feil form (400), ikke notater fra en annen graf.
15. Datafilen `husgraf-20261007.4`: overskriften «drikker uten alkohol» for emnet alkoholfritt er tatt ut. Den sa «uten» (regel 9), og nådde gjesten med skrivemåter som «alkofri». Ellers er `.4` lik `.3`.

## Endret i andre utgave (7. oktober 2026 kl. 13:45 UTC)

Reglene ble skrevet utenfor Swift og kjørt på husets data, først 27 samtaler og så 161. Det som kom fram, og som er endret her:

- **Det som er notert, brakte inn retter setningen ikke handlet om.** «Jeg liker pistasj» etter «Jeg liker ost» ga osteretten først. Regel 4b er ny.
- **Merkelappen for `ukjent` sa «tåler ikke»** om en gjest som hadde skrevet «Jeg er vegetarianer». Den er «unngår noe conciergen ikke kjenner igjen».
- **«uten gluten» sto som «spiser ikke»** i «Slik forsto jeg deg» og som «tåler ikke» i det som var notert. Nå står det samme begge steder.
- **78 ord for allergener treffer ikke strakstiltakets liste.** Med «liker ikke» foran ga 69 av dem en kvittering som sa «Notert» uten at noe ble notert. Steg 2 har fått tilfelle 2.
- **Etter «spiser ikke kjøtt» svarte oppslaget med osteretten på «Jeg liker ikke ost».** Steg 6 har fått kvitteringen «Notert: du liker ikke ost.».
- **Carlsberg Free ble tilbudt ved navn**, mens «alkoholfritt øl» gikk som i dag. Regel 3 er utvidet.
- **Et tilbud kunne komme etter «tåler ikke» når menyen ble oppdatert midt i samtalen.** Det gjesten unngår, står nå.
- **Gjestens JSON ble lest som `ValueType`** i første utkast til koden. Den typen leser innpakkede former. Det nye kallet har sin egen leser.
- Eksempelet med «sjømat» i punkt 2 over er byttet. Steg 6b, loggen, feilene og bryteren er skrevet ut.

**Funnet av de to uavhengige leserne** (`HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/kontroll/LES5-A-kompilering.md` og `LES5-B-logikk.md`, relativt til HAVEN-roten), og rettet her:

- **En forfalsket forespørsel fikk navnet på en øl tilbake.** `noted` tok imot `vil-ha` på `bev-peroni`, og svaret ga merkelappen «vil ha Peroni». Begge utgavene delte feilen, så referansen så den ikke. En slik post avvises nå (422), og i den andre grenen (annen graf) blir den noden `ukjent`.
- **«Har dere alkofri?» ga overskriften «Vi har ni drikker uten alkohol:».** Teksten sto i datafilen (`fortell`), og første utgave av dette dokumentet sa feil at «alkoholfritt» aldri når matchen. Overskriften er tatt ut i datafilen `.4`, referansen har setningen, og lageren av referansen stopper om en overskrift sier «uten», «fri», «trygg» eller «sikker».
- **Alkoholfri Gin Tonic** ble tilbudt som mocktail. Regel 3 gjelder nå også drikke med et ord for alkohol i navnet.
- `kanNevnes` svarte ja uten avsnittet `svar` i datafilen (da vet grafen ikke hvilke emner som er alkoholemner). Nå nei.
- Noe notert uten `graph_version` ble stille behandlet som notater fra en annen graf. Nå 400.
- Regel 8 sa at linjen om allergener står først; linjen om at menyen er oppdatert, står foran den. Rettet i regel 8.
- Det leserne ellers pekte på, og som står som det er: `understood.text` gjengir det gjesten skrev også når oppslaget svarer («du spør om Carlsberg Free.»); matchen kan gi `incomplete` under last (kjernens tidsbudsjett er ett sekund), og svarer da som i dag; fartsgrensen deles med `ask` (valg 5 i meldingen til Kjetil kl. 14:40 UTC).

Kjørt i Swift kl. 14:57 UTC (`svar/d180-pakke5b.md`): 373 tester, 0 feil; Swift lik referansen på 769 setninger og 402 steg.

## Endret etter lesingen av siden (7. oktober 2026 kl. 15:33 UTC)

Den uavhengige leseren av sidens skript (`HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/kontroll/LES10-JS.md`) fant to ting som
gjaldt tjeneren like mye som siden. Begge er rettet i begge utgavene (pakke 7 for Swift):

- **En post vakten selv laget, kunne ikke sendes tilbake.** «Jeg tåler ikke nøtter. Jeg spiser ikke Peroni.» ga henvisningen
  og noterte `spiser-ikke bev-peroni` ved siden av allergenet: steg 2 noterer alt gjesten unngår, og hadde ikke
  alkoholkontrollen steg 4 har. Leseren av forespørselen avviser en slik post (422), så siden fikk 422 på hvert kall
  etterpå, også på «Fjern alt», som sender listen med. Nå gir «spiser ikke» om en drikk med alkohol, eller en alkoholfri
  utgave av en, ingen post; «Slik forsto jeg deg» sier fortsatt «du tåler ikke nøtter og spiser ikke Peroni.». Regelen som
  gjelder fra nå: **alt som står i `noted` i et svar, godtar leseren av neste forespørsel** — referansetesten sjekker det
  for hvert av de 411 stegene, og lageren av referansen stopper om det brytes. Ingen av de 162 samtalene i referansen
  endret seg; to er lagt til.
- **Siden sendte grafens versjon fra `GET` til den ble lastet på nytt.** Ble menyen oppdatert mens siden sto åpen, gikk
  hvert kall etterpå i grenen «notater laget mot en annen versjon av grafen», og advarselen om at menyen er oppdatert sto
  i hvert svar. Siden tar nå versjonen fra `match.graph_version` i hvert svar, og listen slik svaret ga den.

## Endret etter det uavhengige angrepet (7. oktober 2026 kl. 16:40 UTC)

En tråd som ikke hadde skrevet koden, skrev 197 samtaler for å få et galt, villedende eller farlig svar
(`HAVEN-Deploy/_handoff/HD-0077/maal/uavhengige/ANGREP-FORMAALSMATCH-NOTAT-20261007.md`), målt én gang i Swift
(`HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/svar/d183-pakke11a.md`). Det som ble funnet, og endret her:

- **Et alkoholemne kan ikke stå notert.** `noted` tok imot `vil-ha` på `emne:øl` og `liker` på `emne:vin`, og svaret ga
  merkelappen «vil ha øl» tilbake. Regelen for en drikk med alkohol gjelder nå også emnene «øl», «vin», «hvitvin» og
  «rødvin», uansett slag: leseren avviser dem (422), i grenen for en annen graf blir de `ukjent`, og «tåler ikke øl» i en
  setning noteres som `ukjent`, «drikker ikke øl» noteres ikke.
- **Allergi skrevet som helse får henvisningen.** «Mozzarella gjør meg syk. Hva har dere av pizza?», «Pistasj kan drepe
  meg», «Tomat gir meg kvalme» ga liste eller tilbud med nettopp det hun ikke tåler, fordi verken strakstiltakets liste
  eller stikkordene for allergi kjente ordene. Datafilen `.5` har 116 slike uttrykk til under `ALLERGI`, 13 omvendte former
  under `SPISER_IKKE` («kan jeg ikke ha») og «fritt for» under `UNNGAAR` (`graf/ENDRINGSLOGG.md`). Det er data, ikke kode:
  26 av angrepets 32 setninger får nå henvisningen, med emnet notert som «tåler ikke». Setningen «Jeg er al lergisk mot
  ost» (delt ord) når fortsatt matchen; det gjør ingen liste for ord noe med.
- I grenen for en annen graf leses en post bare med nøyaktig `kind` og `node`, som i grenen for samme graf.
- **Står som det er, og vises for Kjetil ved G3:** «Slik forsto jeg deg» snur en dobbel nektelse («Jeg hater ikke ost»,
  «Ikke at jeg ikke liker ost» → «du liker ikke ost»), og «alt annet enn ost» noteres ikke. Det gjesten ser, kan hun fjerne
  med ✕, og et «liker ikke» trekker bare ned. «Er Arancini fri for nøtter?» gir henvisningen og noterer «spiser ikke
  Arancini» (retten hun spurte om); det er F8-veien i utsetting 2 som gir det riktige svaret. Et ord gjesten limer til et
  emneord («ostQX7») kommer tilbake, normalisert, i `understood.interests[].matched` (ordet som traff), aldri i teksten
  siden viser eller i loggen.
