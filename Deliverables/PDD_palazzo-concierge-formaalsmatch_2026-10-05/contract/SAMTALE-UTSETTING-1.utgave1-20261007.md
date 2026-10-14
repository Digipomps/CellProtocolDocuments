# Det nye kallet i utsetting 1: hva det svarer, og hva det lar stå som i dag

Skrevet 7. oktober 2026 av Losen, etter G2. Stier er relative til HAVEN-roten; `PS` står for `PalazzoScaffold`. Dette er arbeidspakke 5 og 6 i `../PLAN.md` gjort presise nok til å skrive tester av. Det legger ikke til formål. Der planen ikke sa hva som skjer, er valget mitt merket **Valgt her**, og står samlet sist så Kjetil kan si nei.

Utsetting 1 har matchen (F2), svarene (F6), samtalen (F5) og siden. Den nye allergenveien (F8) og modellen bak (F3) kommer i utsetting 2 og 3. Dette dokumentet sier derfor også hva kallet gjør med setninger som hører til dem: de får det conciergen svarer i dag.

## Rekkefølgen for en setning (`query`)

| # | Steg | Utfall |
|---|---|---|
| 1 | Forespørselen leses etter `README.md` her | 400 eller 422 ved feil. Er `graph_version` en annen enn tjenestens, kastes `noted`, og svaret sier det |
| 2 | Strakstiltaket: har setningen et ord fra listen (`PS/Sources/App/Services/PalazzoAllergiHenvisning.swift`), eller leser dekomponeringen at gjesten ikke tåler noe | Henvisningen til personalet, ordrett som i dag (`kind: refused`). Sier setningen at gjesten selv ikke tåler noe, noteres det (`taaler-ikke`), så resten av samtalen er uten tilbud |
| 3 | Dekomponeringen (F1) | Formål, og interesser med fortegn og ordene som traff |
| 4 | Vin og alkohol: setningen har et ord fra listene i `PS/Sources/App/Services/PalazzoConciergePhrasing.swift` (`neverRephrasedTerms`, `neverRephrasedWords`), eller en interesse er en drikk med alkohol eller et emne som bare fører til slike (vin, øl) | Som i dag (`kind: answer`): setningen går til oppslaget slik `ask` gjør. Ingenting noteres |
| 5 | Det setningen sier om gjesten selv, noteres: `liker`, `liker-ikke`, `spiser-ikke`. Et spørsmål (`spoer-om`) noterer ingenting, og et ønske (`vil-ha`) noteres ikke | `noted` i svaret er listen etter dette |
| 6 | Står det en post av slaget `taaler-ikke` eller `spiser-ikke` i `noted` | Ingen tilbud og ingen liste fra matchen. Sier setningen bare dette, er svaret en kvittering. Ellers som i dag (`kind: answer`). Listene med merking kommer med F8 |
| 7 | Setningen sier bare noe gjesten ikke liker | Kvittering (`kind: receipt`) |
| 8 | Setningen nevner en rett eller en drikk uten alkohol ved navn | «Vil ha»: kvitteringen som etter et ja (`receipt`). Ellers forteller svaret om den (`tell`): navnet og beskrivelsen ordrett, i formen `ask` bruker for én rett i dag |
| 9 | Setningen har emner: matchen (F2) regner med dem og med det som er notert | Leder én post klart: tilbud (`offer`). Flere: forteller (`tell`). Ingen når terskelen: bom |
| 10 | Bom, eller dekomponeringen fant ingenting huset har (bord, åpningstid, småprat, ukjente ord) | Som i dag (`kind: answer`): oppslaget, publiseringen og formuleringen slik `ask` gjør det. Spørsmålet om modellen kommer i utsetting 3 |

«Som i dag» er samme kode som `ask` kaller, ikke en kopi. Svaret har de 13 nøklene derfra, og de nye feltene i tillegg.

## Regler

1. **Matchen først, så dagens oppslag.** Forstår dekomponeringen noe huset har, svarer grafen. Dagens oppslag svarer når den ikke gjør det. **Valgt her.**
2. **Tilbud bare når én post leder klart.** Det er når bare én post når terskelen, eller den sterkeste har minst `klar_leder` ganger summen til den neste. Tallet står i grafens data (2,5 i versjon `husgraf-20261007.3`) og er foreløpig: bildene fastsetter bare at «ost» gir et tilbud (5,6 ganger) og «pistasj» ikke (1,02 ganger). **Valgt her.** Tabellen «Hva tallet for klar leder gjør» viser hva det betyr for hvert emne.
3. **Et tilbud peker aldri på en drikk med alkohol** (regel 4 i kontrakten), og en rett eller drikk med alkohol står aldri i en liste fra matchen (steg 4 tar setningen først).
4. **Et «liker ikke» trekker ned og stenger ikke.** Det som er notert som `liker`, regnes med som interesse; `liker-ikke` regnes med negativt fortegn. Spør setningen selv etter emnet («Har dere oster?»), gjelder spørsmålet, ikke det som er notert om samme emne.
5. **Ved likt tall** står en post med et emne gjesten ikke liker, etter de andre (valg 19).
6. **Et ja bestiller ikke.** Et `choice` med `ja` legger en post `vil-ha` i `noted` og gir en kvittering. Ingen nøkkel for bestilling kalles.
7. **Teksten bygges av vakten.** Navn og beskrivelse er postens felt ordrett. Ingen modell kalles for tilbud, forteller eller kvittering (`test.match.avgjoerelsen`, `test.dekomp.uten-modell`). Svar «som i dag» formuleres som i dag, med de lukkede spørsmålene `ask` har. At dekomponeringen avgjør hva modellen får formulere (valg 13), er en egen del av arbeidspakke 5 og bygges etter dette.
8. **Linjen om allergener** står først blant advarslene i hvert svar som nevner en rett eller en drikk, i de tre formene koden på nett har. Til Kjetil har valgt (valg 21), står den også under kvitteringene.
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
| Merkelappen for noe gjesten ikke tåler, som grafen ikke kjenner | «tåler ikke noe conciergen ikke kjenner igjen» | Valg 20: ordet lagres ikke |

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

Øl er med i tabellen, men får aldri et tilbud eller en liste fra matchen: steg 4 tar setningen først. «dessert» ligger på 2,00 fordi osteretten har færre emner enn de to andre dessertene, ikke fordi den er mer dessert.

## Valgt her: det Kjetil kan si nei til

1. Matchen svarer før dagens oppslag i det nye kallet (regel 1). Det andre er omvendt: dagens oppslag først, og matchen bare når oppslaget avviser.
2. Tallet for «leder klart» er 2,5 (regel 2). Med 2,0 ville «Jeg liker sjømat» gitt et tilbud om østers alene, og «dessert» ligger nøyaktig på 2,0. Med 3,0 ville «Jeg liker sitron» gitt fem retter i stedet for sitronkremen.
3. Etter «tåler ikke» og «spiser ikke» gir utsetting 1 ingen tilbud og ingen liste fra matchen (steg 2 og 6). «Tåler ikke» gir henvisningen til personalet, ordrett som i dag. Sier setningen bare at gjesten ikke spiser noe, er svaret en kvittering; ellers svarer conciergen som i dag. Listene i bilde 4C, 6 og 7A kommer i utsetting 2.
4. En setning der gjesten sier at hun ikke tåler noe, noteres alt i utsetting 1, selv om svaret er henvisningen som i dag. Uten det kunne et tilbud komme senere i samme samtale, og det er en av tingene som stopper en utsetting.
5. Ordlyden i tabellen over.
