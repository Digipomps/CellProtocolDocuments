Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

Skrevet 7. oktober 2026 (natt til 7.), av Losen, og rettet samme natt etter en uavhengig kontroll (se «Rettet etter kontrollen» sist). Du har ikke sett den første utgaven, så filnavnene er de samme. G1-GUI er Kjetils ord og er ikke gitt. Stier er relative til HAVEN-roten.

## RENDERINGSERKLÆRING

Bildene er skisser. De er ikke skjermbilder fra nett, og de er ikke rendret fra et skjelett. Conciergens side er HTML, så det finnes ikke noe skjelett å rendre. Ingen programkode har laget svarene: de viser foreslått ordlyd og plassering, og er til for at du skal se hva gjesten kommer til å se før noe bygges.

Slik er de laget:

- **Grunnlaget er sidens egne filer**, kopiert fra `PalazzoScaffold/Public` slik mappen står på grenen `deploy/palazzo-demo-20260930` (de samme filene som i `c5058f49`, utgaven på nett): `PalazzoScaffold/Public/palazzo/index.html` (md5 `c638fc69ac57797fa44267441a4f1292`), `PalazzoScaffold/Public/css/palazzo-communale.css` (md5 `63284bdc9f370ff05786749f0388be4b`), `PalazzoScaffold/Public/js/palazzo-communale.js` (md5 `0e929f12959bc122e82c6ed66c6b7beb`), og skriftene og bildene under `PalazzoScaffold/Public/css/themes/palazzo/`. Siden er rendret i Chromium (Playwright) i Losens skyarbeidsområde.
- **Tjenesten er byttet ut med faste svar.** `POST /palazzo/api/ask` gir konvolutten som står i `images/kilde/tilstander.js`, og `GET /palazzo/api/state` gir en fast tjenestestatus. Spørsmålet er skrevet i spørrefeltet og sendt med Enter, og **sidens eget skript har tegnet spørsmålet, svarteksten, advarslene, kildene og datoen**.
- **Det nye er lagt på etterpå** av skissen: `images/kilde/skisse.css` (bare nye regler, bygget på sidens egne farger og skrifter) og funksjonen `leggPaaSkisse` i `images/kilde/rendre.js`. Det gjelder linjen «Slik forsto jeg deg», knappene under svaret med linjen under, merket «Tolket av en språkmodell», stripen «Notert i denne samtalen», panelet «Vil du beholde dette til neste gang?», overskriftene «Notert», «Fjernet», «Ikke funnet» og «Fra menyen», merkelappen «må bekreftes av personalet», og den nye setningen under «Hva vil du vite?». Ingenting av dette finnes på siden i dag.
- **Skissen tar også bort to ting sidens skript tegner.** Merkelappen «høy sikkerhet» eller «middels sikkerhet» er tatt bort på svar som tilbyr eller nevner retter (se «Merkelappen» under). Advarselen og kildene er tatt bort i kvitteringene som ikke nevner noen rett, og i spørsmålet om modellen. Kildene er også tatt ut av de fire utsnittene i bilde 2 og av kvitteringen i bilde 5.
- **Tekstene om retter og drikke er kopiert fra korpuset**, ikke skrevet av (`PalazzoScaffold/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json`). `images/kilde/sjekk_tekster.js` holder det gjesten ser i rammene, mot korpuset og mot reglene i kontrakten: 330 kontroller, 0 feil, kjørt etter siste rendring. 78 av dem gjelder korpuset: 25 beskrivelser står ordrett, 24 avsnitt begynner med et navn som finnes, 8 linjer «Merket med: …» er rettens merking, 8 sier riktig om merkingen er bekreftet, 1 drikk er uten alkohol, og 12 er faste kontroller av kategorier og lister. 133 gjelder ord conciergen ikke skal bruke om en rett («trygg», «trygt», «sikker», «garant», «uten risiko», «ufarlig»): 25 i svarene i hvert steg, og 108 i det skissen legger på. 25 gjelder at ingen svar sier at noe «er uten», «ikke inneholder» eller er «fritt for» noe. 23 gjelder merkelappen rammen ender med, 14 at linjen om allergener vises i den formen koden på nett bruker, 10 at ingen rett tilbys etter «tåler ikke», 1 at kvitteringen etter «liker ikke» ikke lover å holde noe ute, og 46 at rammer og bilder henger sammen. Linjene om allergener er skrevet av fra koden inn i skriptet, så det ikke kontrollerer filen mot seg selv.
  Skriptet ser det som står i `images/kilde/tilstander.js`. Det ser ikke pikslene i bildene og ikke bildetekstene, det kjenner bare igjen et tilbud på formen (knappene, «Vil du ha», og ord som «anbefaler»), og det vet ikke om et svar er klokt. Kjørt mot utgaven før rettingen gir det 18 feil (`images/kilde/sjekk-mot-utgaven-foer-rettingen.txt`; kjør `node sjekk_tekster.js <den gamle filen>`). `images/kilde/proev_sjekken.py` endrer rammene på seks måter, og skriptet blir rødt for hver (`images/kilde/sjekken-proevd.txt`). «pistasi» står slik i menyen og er gjengitt ordrett.
- **Advarslene og kilden** er dem siden viser i dag. Linjen om allergener har de tre formene koden på nett bruker (regel 3 i strakstiltaket, `PalazzoScaffold/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, linje 17–19): «Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller.» under én rett, «Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller.» under flere, og «Spør personalet om allergener før du bestiller.» under et svar uten beskrivelse (drikken i bilde 2 og kvitteringen i bilde 5). «Svaret bygger på et datert kunnskapsgrunnlag. …», «Palazzo Communales meny (PDF)» og «Sist verifisert: 2026-06-03» er hentet fra et svar målt på nett 6. oktober (`HAVEN-Deploy/_handoff/HD-0077/maal/nett-ut/spoersmaal-strakstiltak-nett-20261006-20261006T132126Z.jsonl`). Linjen «Merkingen dekker ikke spor eller krysskontakt. Si fra til personalet før du bestiller.» er ny.
- Bredden er 1280 punkter (390 for tilleggsbildet). Bilde 1 og 7A viser hele concierge-delen av siden. Bilde 3 og 5 viser kortet med spørrefeltet. De andre rammene er utsnitt: spørsmålet, svaret og «Notert», uten spørrefeltet, satt på hvit bunn. Tittelen, ingressen, den lille linjen under og tekstene under hver ramme er lagt på av `rendre.js` og er ikke en del av siden.
- Fokusmarkeringen siden setter rundt svaret når spørsmålet sendes med tastaturet, er tatt bort før bildet ble tatt.

Verktøyene ligger i `images/kilde/`: `rendre.js` (rendrer rammene og setter bildene sammen), `tilstander.js` (hver ramme: hva gjesten skrev, konvolutten og det skissen legger på), `skisse.css`, `sjekk_tekster.js`. Stiene inne i dem viser til Losens skyarbeidsområde. md5 da bildene ble laget på nytt: `tilstander.js` `9b4bc6b31d63f8fe034d4dbff4eede68`, `skisse.css` `1fe152e2b18fbc808ac551afd1848955`, `rendre.js` `6afb4bdbab2928aebafe701638886b98`, `sjekk_tekster.js` `144c8ba14d61058d052569a77db7c958`. Filene på Mac-en er noen tusen byte større enn i Losens skyarbeidsområde: overføringen legger en blokk med innholdsmerking i hver PNG. Bildedataene er de samme (kontrolltråden regnet det for den første utgaven).

## De ni bildene

| Bilde | Rad i §3 | Hva gjesten har skrevet | Hva bildet viser |
|---|---|---|---|
| `concierge-tilbud-v1.png` | Siden med et tilbud som svar | «Jeg liker ost» | Osteretten med menyens beskrivelse, «Vil du ha det til dessert?», knappene «Ja, det vil jeg» og «Nei takk», og «Et ja bestiller ikke. Du bestiller hos kelneren.» |
| `concierge-tilbud-flere-v1.png` | Tilbud om andre slags ting | «Jeg liker blekksprut», «Jeg liker lam», «Jeg liker trøffel», «Jeg liker eplemost» | Ordlyden for en forrett, en hovedrett, en pizza og en drikk uten alkohol |
| `concierge-forteller-v1.png` | Et svar som bare forteller | «Jeg liker pistasj» | Begge rettene med pistasj, uten spørsmål og uten knapper |
| `concierge-kvittering-v1.png` | En kvittering uten tilbud, og listen etter «Jeg tåler ikke nøtter.» | «Jeg liker ikke ost»; «Jeg tåler ikke nøtter.»; og så «Hva har dere til dessert?» | To kvitteringer, og dessertlisten med merking og beskrivelse, uten tilbud |
| `concierge-ja-v1.png` | Svaret når gjesten sier ja til et tilbud | «Jeg liker ost», og så trykk på «Ja, det vil jeg» | «Notert: du vil ha Formaggi misti til dessert. …», og formålet i «Notert» |
| `concierge-unngaar-v1.png` | Listen etter «Jeg tåler ikke selleri.», og etter «Jeg spiser ikke kjøtt.» | «Jeg tåler ikke selleri.» og «Hva har dere av forretter?»; «Jeg spiser ikke kjøtt.» og «Hvilke pizzaer har dere?» | Merking og beskrivelse for hver forrett, med Carpaccio di polpo og Ostriche først; pizzaene som nevner kjøttvarer, og de andre uten påstand om at de er uten |
| `concierge-notert-v1.png` | Det conciergen har notert, og hvordan gjesten fjerner det | «Jeg liker pistasj», «Jeg liker ikke ost», «Jeg spiser ikke kjøtt.» | Stripen nederst i kortet, etter ✕ på én ting, og etter «Fjern alt» |
| `concierge-modell-bak-v1.png` | Når matchen feiler | «Har dere noe sånt som risboller?» | Spørsmålet til gjesten med tre valg, svaret merket «Tolket av en språkmodell», og svaret etter «Nei» |
| `concierge-behold-v1.png` | Når gjesten vil beholde det som er notert | (trykk på «Behold til neste gang») | Inngangen og panelet med avkryssing. Gjelder først når veien fra siden til en egen gjesteprofil finnes |

`tillegg-concierge-tilbud-smal-skjerm-v1.png` er ikke ett av de ni og ikke en akseptreferanse. Det viser bilde 1 på 390 punkters bredde, så du ser at de nye delene får plass på en telefon.

`tillegg-concierge-merkelapp-v1.png` er heller ikke ett av de ni. Det viser samme tilbud to ganger: slik forslaget er, og med merkelappen siden setter på svar i dag. Ramme B har forslagets nye deler og merkelappen fra i dag; kildene er tatt ut av begge rammene.

## Merkelappen «høy sikkerhet»: et spørsmål til deg

Siden setter i dag «høy sikkerhet», «middels sikkerhet» eller «lav sikkerhet» øverst i et svar den har kilde for (`PalazzoScaffold/Public/js/palazzo-communale.js`, linje 79 og 102–104). Ordet gjelder hvor sikkert svaret er. Ved siden av en rett kan det leses som at retten er sikker, og regel 1 i kontrakten sier at ingen svartype sier at en rett er trygg.

I den første utgaven av bildene sto «høy sikkerhet» på åtte rammer med et tilbud eller et rettnavn (sju i de ni bildene, og tilleggsbildet for smal skjerm), og «middels sikkerhet» på én. Jeg hadde ikke nevnt merkelappen noe sted. Kontrolltråden fant det.

I forslaget nå er merkelappen tatt bort på svar som tilbyr eller nevner retter (bildene 1, 2, 3, 6B og 8B). Listene etter «tåler ikke» har «må bekreftes av personalet», som før.

Overskriften «Kontrollert svar» står fortsatt over tilbudene i bildene 1, 2 og 3. I bilde 8B er den byttet til «Fra menyen», fordi svaret der er tolket av en språkmodell: teksten er menyens, men at modellen pekte riktig, er ikke kontrollert. Om «Kontrollert svar» skal stå over et tilbud, er også ditt valg.

| Du velger | Da skjer dette |
|---|---|
| Ingen merkelapp på slike svar (forslaget) | Bildene står som de er. Siden tegner ikke merkelappen for de nye svartypene |
| Merkelappen som i dag | Bildene 1, 2, 3, 6B og 8B rendres på nytt med den. Tilleggsbildet viser hvordan det blir |
| Et annet ord | Du sier hvilket, og bildene rendres på nytt |

Samme merkelapp står på rettbeskrivelser på nett i dag, i svarene fra `ask`. Å endre den der er en endring på nett, og gjøres ikke uten ditt ord.

## Ordlyden i tilbudene

Mønsteret i bildene er «Vi har ⟨navn⟩: ⟨menyens beskrivelse⟩ Vil du ha det ⟨når⟩?». Navnet og beskrivelsen står ordrett som i menyen, og «når» følger rettens plass på menyen:

| Plass på menyen (korpusets kategori) | Spørsmålet |
|---|---|
| antipasti | «Vil du ha det til forrett?» |
| primi | «Vil du ha det som pastarett?» (ikke vist i bildene) |
| secondi | «Vil du ha det til hovedrett?» |
| dolce | «Vil du ha det til dessert?» |
| pizze | «Vil du ha den?» |
| drikke uten alkohol | «Vi har ⟨navn⟩. Vil du ha det å drikke?» (drikke har ingen beskrivelse i menyen) |
| drikke med alkohol | tilbys aldri |

Eksempelet ditt var «Vi har et utvalg med oster - vil du ha det til dessert»?. Den setningen kan ikke bygges av menyens tekst for hver rett uten å skrive om beskrivelsen. Mønsteret over gir samme innhold for osteretten, med navnet i tillegg: «Vi har Formaggi misti: Utvalg av oster fra små utvalgte gårder i Italia med tilbehør. Vil du ha det til dessert?». Vil du ha setningen din ordrett, blir det en håndskrevet setning for den ene retten, og de andre rettene trenger hver sin, godkjent av deg.

## Det bildene ikke viser

- Hvordan siden ser ut mens den venter på svar, og feilmeldingene. De er som i dag.
- Onboardingen etter «Lag gjesteprofil» (bilde 9). Den hører til onboarding-oppgaven.
- Svaret når gjesten har sagt ja til «Hele samtalen» og matchen bommer igjen: det er bilde 8B uten spørsmålet først.
- En setning med både et spørsmål og «uten …», som «Har dere dessert uten nøtter?». Den får samme liste som i bilde 4C.
- Eksempelsetningen i bilde 8 («Har dere noe sånt som risboller?») er valgt av meg. Den byttes med en setning som er målt som bom, før G3.
- I bilde 6B står Pizza Salina, med ansjos, blant «De andre pizzaene». Conciergen regner ikke fisk som kjøtt. Om den skal si fra om fisk til en gjest som ikke spiser kjøtt, er ditt valg; grafen har emnet `fisk` på den pizzaen.
- Hvilken rett som står først når to har samme tall etter et «liker ikke». Det er valg 19 i `PLAN.md`.
- Bilde 1 og 7A viser sidens tre snarveier slik de står i dag, blant dem «Allergener og hensyn · Usikker informasjon stoppes alltid». De er ikke endret i forslaget.
- Kvitteringene som ikke nevner noen rett (4A, 4B, 7A–C, 8A og 8C), har ikke linjen om allergener. Regel 3 på nett gjelder hvert publisert svar; forslaget gjelder svar som nevner en rett eller en drikk (regel 7 i `contract/README.md`). Det er valg 21 i `PLAN.md`.

## Slik tas motstykket på nett ved G3

Chrome gjennom utvidelsen holder vinduet på 1280 punkters bredde (målt 6. oktober), så referansene har den bredden. For hvert bilde skrives de samme setningene i spørrefeltet på `https://palazzo.digipomps.org/palazzo`, i samme rekkefølge, og knappene trykkes der bildet sier det. Skjermbildet tas av vinduet etter hvert svar. Er svaret høyere enn vinduet, rulles det ned og tas flere bilder som overlapper. Sammenligningen gjøres ramme for ramme: for utsnittene holdes spørsmålet, svaret og «Notert» på nett mot utsnittet. Tilleggsbildet på 390 punkter kan ikke tas den veien; det kan du ta på telefonen.

## Det som står på nett i dag for de samme setningene

Strakstiltaket for allergenveien står på nett (`c5058f49`). «Jeg tåler ikke nøtter.» og «Jeg tåler ikke selleri.» får i dag bare henvisningen til personalet, fordi de har ord fra listen. Bildene 4 og 6 viser det som kommer i stedet når den nye allergenveien (F8) er bygget, angrepet og godkjent av deg. Til da står strakstiltaket.

## Rettet etter kontrollen (7. oktober 2026)

Kontrolltråden K4 åpnet alle bildene og holdt dem mot korpuset, sidens skript og planen (`HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/K4-HOVEDOPPGAVEN.md`). Bildene er rendret på nytt 7. oktober kl. 02:09–02:12 UTC, og en gang til kl. 02:36 UTC etter kontrollen av rettingene. Den første utgaven ligger i `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/k4/foer/`.

| Bilde | Sto | Står nå | Hvem fant det |
|---|---|---|---|
| 1, 2, 3, 6B, 8B og tillegget for smal skjerm | «Høy sikkerhet» (6B: «middels sikkerhet») over et tilbud eller et rettnavn, ikke nevnt | Ingen merkelapp, og spørsmålet er stilt over | K4 |
| 2 | Advarselen var skjult i de fire tilbudene | Hvert tilbud har linjen om allergener | K4 |
| 4A | «Jeg foreslår ikke retter med ost i denne samtalen» | «Jeg foreslår helst andre retter. Spør du om ost, får du svar likevel.» Et «liker ikke» trekker ned; det stenger ikke | K4 |
| 8 | «Ingen rett når terskelen» | «Ingen ord i setningen treffer husets graf», som i eksempelet i kontrakten | K4 |
| 9 | «liker pistasj» og «tåler ikke nøtter» på samme gjest | «liker sitron» | K4 |
| 1, 2, 8B | Linjen om allergener i flertall («Beskrivelsene …») under én rett | Formen for én rett, som koden på nett bruker | Losen, ved ny rendring |
| 5 | Kvitteringen etter et ja nevnte retten uten linjen om allergener | Linjen står under | Losen, ved ny rendring |
| alle | «127 påstander, 0 feil» mot korpuset | 330 kontroller, og hva de er | K4 |
| 8A | Ingen «Slik forsto jeg deg» | «Slik forsto jeg deg: du spør om noe huset har.», som i eksempelet i kontrakten | K7 |
| 8B | «Kontrollert svar» over et svar tolket av en språkmodell | «Fra menyen» | K7 |
| 2 og tillegget om merkelappen | Ingressen nevnte «til dessert», som ikke vises der; tekst B sa «slik siden ville tegnet det» om en ramme med forslagets nye deler | Rettet | K7 |

Bildene etter første retting ble åpnet av en ny uavhengig tråd (K7) 7. oktober kl. 02:18–02:29 UTC, alle elleve (`HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/K7-HOVEDOPPGAVEN-RETTING.md`). Den fant ingen merkelapp om sikkerhet på et tilbud eller et rettnavn, riktig form på linjen om allergener i alle rammer, og ingen tilbud etter «tåler ikke». Den fant fire tilfeller der kontrollskriptet ble grønt og skulle vært rødt, og fem tekster som sa mer enn rammen viste. Det er rettet, og bildene er rendret på nytt kl. 02:36 UTC. De tre bildene som ble endret da (2, 8 og tillegget om merkelappen), ble åpnet av enda en tråd (K8) kl. 02:39–02:50 UTC, som også regnet etter tallene for kontrollskriptet: de stemte. Etter det er bare ingressen i tilleggsbildet om merkelappen endret (den nevner nå alle tre ordene siden bruker), rendret kl. 02:52 UTC.
