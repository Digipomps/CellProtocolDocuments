# Emner for retter og drikke, første forslag (`graf/emner-v1.md`)

Laget 7. oktober 2026 av Losen med `graf/lag_emner.py`. Dette er data til husets graf (F7), ikke kode, og ingenting er bygget på det ennå. Teksten er rettet samme natt etter de uavhengige kontrollene (K4 og K7): avsnittet om allergener under og regnestykket for «liker ikke» sist er nye. Emnene, koblingene og vektene er de samme, og `graf/emner-v1.json` er uendret.

Hvert emne er hentet fra én av fire kilder i korpuset (`PalazzoScaffold/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json`): rettens norske beskrivelse (B), en engelsk tagg (T), kategorien (K) eller navnet (N). Skriptet kontrollerer at hvert emne kan spores til kilden det oppgir; 151 emnekoblinger er kontrollert, 0 feil.

Vektene er et første forslag i fem klasser, satt av meg og ikke målt: 1,0 retten er dette · 0,7 det retten bygger på · 0,5 kategori · 0,4 nevnt som ingrediens · 0,3 sted eller svak kobling. Det er disse revisoren (F4) skal foreslå endringer i, og tallene settes ikke fast før første måling.

Tre ting er holdt utenfor med vilje:

- **Ingen kant fra ingrediens til allergen.** Majones til egg og smør til melk sier noe om hva retten inneholder, og må komme fra huset. Allergener leses fra merkingen.
- **Mozzarella, taleggio og caciocavallo er ikke koblet til «ost».** «Jeg liker ost» ville da gitt fire av fem pizzaer. Koblingen er et spørsmål for målingen.
- **Ragu er ikke koblet til «kjøtt».** Beskrivelsen av Arancini sier «ragu», ikke hva raguen er laget av. Det må huset si.

**Allergenene er ikke emner, og forslaget mangler noder for dem.** 2 emner har samme navn som et allergen i korpusets liste: `fisk` og `selleri`. De er hentet fra ord i beskrivelsene og fra tagger (`selleri` fra «stangselleri» i beskrivelsen av Carpaccio di polpo, som ikke er merket med selleri; `fisk` fra taggen `fish` og fra «ansjos» i beskrivelsen av Pizza Salina), og sier hva kilden nevner, ikke hva retten er merket med. Ingen emner heter nøtter, egg eller melk. Forslaget sier derfor ikke hvilken node «tåler ikke nøtter» skal peke på. Det må inn i datafilen før den nye allergenveien (F8) bygges: én node per allergen i korpusets liste (14), laget av merkingen og ikke av beskrivelsene. Det gjesten ikke tåler, kan også være et vanlig emne, som løk, eller noe grafen ikke kjenner. Kontrakten sier hva som skjer i hvert av de tre tilfellene (`contract/README.md`, feltet `noted` og regel 2).

## Rettene

| Rett | Kategori | Emner (vekt, kilde: ordet i kilden) |
|---|---|---|
| Pane di campagna focaccia e olio | antipasti | brød (1,0, B: landbrød); focaccia (1,0, B: focaccia); olivenolje (0,4, B: olivenolje); forrett (0,5, K: antipasti) |
| Arancini | antipasti | arancini (1,0, N: arancini); ris (0,7, B: riskroketter); ragu (0,4, B: ragu); safran (0,4, B: safran); ost (0,4, B: ost); fritert (0,3, B: friterte); sicilia (0,3, T: sicily); forrett (0,5, K: antipasti) |
| Ostriche | antipasti | østers (1,0, B: østers); sjømat (0,5, T: seafood); forrett (0,5, K: antipasti) |
| Carpaccio di polpo | antipasti | blekksprut (1,0, B: blekksprutcarpaccio); carpaccio (0,7, B: blekksprutcarpaccio); potet (0,4, B: potet); selleri (0,4, B: stangselleri); olivenolje (0,4, B: olivenolje); sitron (0,4, B: sitron); sjømat (0,5, T: seafood); forrett (0,5, K: antipasti) |
| Vitello tonnato | antipasti | kalv (1,0, B: kalveroastbiff); tunfisk (0,7, B: tunfiskmajones); majones (0,4, B: tunfiskmajones); brissel (0,4, B: kalvebrissel); asparges (0,4, B: asparges); kjøtt (0,5, B: kalveroastbiff); fisk (0,4, T: fish); forrett (0,5, K: antipasti) |
| Busiate Primavera | primi | pasta (1,0, B: pasta); asparges (0,4, B: asparges); erter (0,4, B: erter); fava (0,4, B: fava); mandler (0,4, B: mandler); salvie (0,4, B: salvie); mynte (0,4, B: mynte); sitron (0,4, B: sitron); grønnsaker (0,5, T: vegetable); sicilia (0,3, T: sicily) |
| Pasta vongole | primi | pasta (1,0, B: linguine); linguine (0,7, B: linguine); skjell (0,7, B: teppekjell); hvitvin (0,4, B: hvitvin); sitron (0,4, B: sitron); persille (0,4, B: bladpersille); sjømat (0,5, T: seafood) |
| Orata al forno a legna | secondi | havbrasme (1,0, B: havbrasme); fisk (0,7, T: fish); vedfyrt (0,4, B: vedfyrt); urter (0,4, B: urter); sitron (0,4, B: sitron); potet (0,4, B: poteter); kapers (0,4, B: kapersmør); hovedrett (0,5, K: secondi) |
| Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso | secondi | okse (1,0, B: okse); linser (0,7, B: linser); rødvin (0,4, B: rødvinsbraiserte); salat (0,4, B: salat); potet (0,4, B: potet); kjøtt (0,5, B: okse); modica (0,3, B: modica); hovedrett (0,5, K: secondi) |
| Agnello arrosto con salsa di pistacchio di Brontë | secondi | lam (1,0, B: lammecarré); pistasj (0,7, B: pistasj); gulrot (0,4, B: gulrot); løk (0,4, B: løk); kjøtt (0,5, B: lammecarré); bronte (0,3, B: brontë); sicilia (0,3, T: sicily); hovedrett (0,5, K: secondi) |
| Torta di mascarpone e pistacchi | dolce | ostekake (1,0, B: ostekake); kake (0,7, B: ostekake); mascarpone (0,7, B: mascarpone); pistasj (0,7, B: pistasi); ost (0,3, B: ostekake); bronte (0,3, B: brontë); dessert (0,5, K: dolce) |
| Crema di limone Siciliana | dolce | sitron (1,0, B: sitronkrem); sorbet (0,7, B: sitronsorbet); krem (0,7, B: sitronkrem); karamell (0,4, B: karamellisert); sicilia (0,3, T: sicily); dessert (0,5, K: dolce) |
| Formaggi misti | dolce | ost (1,0, B: oster); italia (0,3, B: italia); dessert (0,5, K: dolce) |
| Pizza Margherita | pizze | pizza (1,0, K: pizze); tomat (0,4, B: tomatsaus); mozzarella (0,4, B: mozzarella); basilikum (0,4, B: basilikum) |
| Pizza Siciliana | pizze | pizza (1,0, K: pizze); tomat (0,4, B: tomatsaus); aubergine (0,4, B: aubergine); oliven (0,4, B: oliven); kapers (0,4, B: kapers); caciocavallo (0,4, B: caciocavallo); mozzarella (0,4, B: mozzarella); sicilia (0,3, T: sicily) |
| Pizza Vulcano | pizze | pizza (1,0, K: pizze); sterk (0,7, B: piccant); salami (0,4, B: chilisalami); nduja (0,4, B: nduja); chili (0,4, B: chilisalami); tomat (0,4, B: tomatsaus); mozzarella (0,4, B: mozzarella); kjøtt (0,5, B: chilisalami) |
| Pizza Tartufo "Umami" | pizze | pizza (1,0, K: pizze); trøffel (0,7, B: høsttrøffel); salami (0,4, B: trøffelsalami); taleggio (0,4, B: taleggio); mozzarella (0,4, B: mozzarella); kjøtt (0,5, B: trøffelsalami) |
| Pizza Salina | pizze | pizza (1,0, K: pizze); ansjos (0,7, B: ansjos); tomat (0,4, B: tomatsaus); hvitløk (0,4, B: hvitløk); kapers (0,4, B: kapers); fisk (0,4, B: ansjos) |

## Drikkene

Drikkene har ingen beskrivelse i korpuset, bare navn og tagger. De seks ølene tilbys aldri (regel 4); de står i grafen så et spørsmål om øl kan kjennes igjen.

| Drikk | Kategori | Emner |
|---|---|---|
| Frydenlund 0.5 | alcoholic_beer | øl (1,0, T: beer) |
| Frydenlund 0.25 | alcoholic_beer | øl (1,0, T: beer) |
| Peroni | alcoholic_beer | øl (1,0, T: beer) |
| Poretti | alcoholic_beer | øl (1,0, T: beer) |
| Peroni Glutenfri | alcoholic_beer | øl (1,0, T: beer) |
| Brooklyn IPA | alcoholic_beer | øl (1,0, T: beer) |
| Carlsberg Free | non_alcoholic | alkoholfritt øl (1,0, T: non alcoholic); alkoholfritt (0,5, T: non alcoholic) |
| Alkoholfri vin | non_alcoholic | alkoholfri vin (1,0, N: alkoholfri vin); alkoholfritt (0,5, T: non alcoholic) |
| Alkoholfri Gin Tonic | non_alcoholic | mocktail (1,0, T: mocktail); alkoholfritt (0,5, T: non alcoholic) |
| Eplemost | non_alcoholic | eplemost (1,0, N: eplemost); eple (0,7, N: eplemost); juice (0,7, T: apple juice); alkoholfritt (0,5, T: non alcoholic) |
| Grimstad Brusfabrikk | non_alcoholic | brus (1,0, T: soda); alkoholfritt (0,5, T: non alcoholic) |
| Ferrarelle | non_alcoholic | vann (1,0, T: water); mineralvann (0,7, T: sparkling water); alkoholfritt (0,5, T: non alcoholic) |
| Pepsi Max | non_alcoholic | brus (1,0, T: soda); alkoholfritt (0,5, T: non alcoholic) |
| Pepsi | non_alcoholic | brus (1,0, T: soda); alkoholfritt (0,5, T: non alcoholic) |
| Solo | non_alcoholic | brus (1,0, T: soda); alkoholfritt (0,5, T: non alcoholic) |
| Italian sodas | non_alcoholic | brus (1,0, T: soda); alkoholfritt (0,5, T: non alcoholic) |
| Dagens Mocktail | non_alcoholic | mocktail (1,0, T: mocktail); alkoholfritt (0,5, T: non alcoholic) |

## Emnene, og hvilke retter og drikker de når

| Emne | Antall | Når |
|---|---|---|
| alkoholfritt | 11 | Carlsberg Free, Alkoholfri vin, Alkoholfri Gin Tonic, Eplemost, Grimstad Brusfabrikk, Ferrarelle, Pepsi Max, Pepsi, Solo, Italian sodas, Dagens Mocktail |
| øl | 6 | Frydenlund 0.5, Frydenlund 0.25, Peroni, Poretti, Peroni Glutenfri, Brooklyn IPA |
| brus | 5 | Grimstad Brusfabrikk, Pepsi Max, Pepsi, Solo, Italian sodas |
| forrett | 5 | Pane di campagna focaccia e olio, Arancini, Ostriche, Carpaccio di polpo, Vitello tonnato |
| kjøtt | 5 | Vitello tonnato, Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso, Agnello arrosto con salsa di pistacchio di Brontë, Pizza Vulcano, Pizza Tartufo "Umami" |
| pizza | 5 | Pizza Margherita, Pizza Siciliana, Pizza Vulcano, Pizza Tartufo "Umami", Pizza Salina |
| sicilia | 5 | Arancini, Busiate Primavera, Agnello arrosto con salsa di pistacchio di Brontë, Crema di limone Siciliana, Pizza Siciliana |
| sitron | 5 | Carpaccio di polpo, Busiate Primavera, Pasta vongole, Orata al forno a legna, Crema di limone Siciliana |
| mozzarella | 4 | Pizza Margherita, Pizza Siciliana, Pizza Vulcano, Pizza Tartufo "Umami" |
| tomat | 4 | Pizza Margherita, Pizza Siciliana, Pizza Vulcano, Pizza Salina |
| dessert | 3 | Torta di mascarpone e pistacchi, Crema di limone Siciliana, Formaggi misti |
| fisk | 3 | Vitello tonnato, Orata al forno a legna, Pizza Salina |
| hovedrett | 3 | Orata al forno a legna, Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso, Agnello arrosto con salsa di pistacchio di Brontë |
| kapers | 3 | Orata al forno a legna, Pizza Siciliana, Pizza Salina |
| ost | 3 | Arancini, Torta di mascarpone e pistacchi, Formaggi misti |
| potet | 3 | Carpaccio di polpo, Orata al forno a legna, Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso |
| sjømat | 3 | Ostriche, Carpaccio di polpo, Pasta vongole |
| asparges | 2 | Vitello tonnato, Busiate Primavera |
| bronte | 2 | Agnello arrosto con salsa di pistacchio di Brontë, Torta di mascarpone e pistacchi |
| mocktail | 2 | Alkoholfri Gin Tonic, Dagens Mocktail |
| olivenolje | 2 | Pane di campagna focaccia e olio, Carpaccio di polpo |
| pasta | 2 | Busiate Primavera, Pasta vongole |
| pistasj | 2 | Agnello arrosto con salsa di pistacchio di Brontë, Torta di mascarpone e pistacchi |
| salami | 2 | Pizza Vulcano, Pizza Tartufo "Umami" |
| alkoholfri vin | 1 | Alkoholfri vin |
| alkoholfritt øl | 1 | Carlsberg Free |
| ansjos | 1 | Pizza Salina |
| arancini | 1 | Arancini |
| aubergine | 1 | Pizza Siciliana |
| basilikum | 1 | Pizza Margherita |
| blekksprut | 1 | Carpaccio di polpo |
| brissel | 1 | Vitello tonnato |
| brød | 1 | Pane di campagna focaccia e olio |
| caciocavallo | 1 | Pizza Siciliana |
| carpaccio | 1 | Carpaccio di polpo |
| chili | 1 | Pizza Vulcano |
| eple | 1 | Eplemost |
| eplemost | 1 | Eplemost |
| erter | 1 | Busiate Primavera |
| fava | 1 | Busiate Primavera |
| focaccia | 1 | Pane di campagna focaccia e olio |
| fritert | 1 | Arancini |
| grønnsaker | 1 | Busiate Primavera |
| gulrot | 1 | Agnello arrosto con salsa di pistacchio di Brontë |
| havbrasme | 1 | Orata al forno a legna |
| hvitløk | 1 | Pizza Salina |
| hvitvin | 1 | Pasta vongole |
| italia | 1 | Formaggi misti |
| juice | 1 | Eplemost |
| kake | 1 | Torta di mascarpone e pistacchi |
| kalv | 1 | Vitello tonnato |
| karamell | 1 | Crema di limone Siciliana |
| krem | 1 | Crema di limone Siciliana |
| lam | 1 | Agnello arrosto con salsa di pistacchio di Brontë |
| linguine | 1 | Pasta vongole |
| linser | 1 | Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso |
| løk | 1 | Agnello arrosto con salsa di pistacchio di Brontë |
| majones | 1 | Vitello tonnato |
| mandler | 1 | Busiate Primavera |
| mascarpone | 1 | Torta di mascarpone e pistacchi |
| mineralvann | 1 | Ferrarelle |
| modica | 1 | Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso |
| mynte | 1 | Busiate Primavera |
| nduja | 1 | Pizza Vulcano |
| okse | 1 | Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso |
| oliven | 1 | Pizza Siciliana |
| ostekake | 1 | Torta di mascarpone e pistacchi |
| persille | 1 | Pasta vongole |
| ragu | 1 | Arancini |
| ris | 1 | Arancini |
| rødvin | 1 | Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso |
| safran | 1 | Arancini |
| salat | 1 | Tagliata di manzo "Cuvette" con lenticchie di Modica bresato al vino rosso |
| salvie | 1 | Busiate Primavera |
| selleri | 1 | Carpaccio di polpo |
| skjell | 1 | Pasta vongole |
| sorbet | 1 | Crema di limone Siciliana |
| sterk | 1 | Pizza Vulcano |
| taleggio | 1 | Pizza Tartufo "Umami" |
| trøffel | 1 | Pizza Tartufo "Umami" |
| tunfisk | 1 | Vitello tonnato |
| urter | 1 | Orata al forno a legna |
| vann | 1 | Ferrarelle |
| vedfyrt | 1 | Orata al forno a legna |
| østers | 1 | Ostriche |

## Formålene, første liste

| Formål | Måltekst (forslag) | Former som gir det (eksempler, ikke hele listen) |
|---|---|---|
| spise | Retten er servert til gjesten (samme måltekst som gjesteflaten har i dag) | «jeg vil ha …», «jeg har lyst på …», «kan jeg få …», «noe med …» |
| drikke | Drikken er servert til gjesten | «noe å drikke», «har dere eplemost», «hva kan jeg drikke» |
| vite | Gjesten har fått svaret fra husets data | «hva er …», «fortell om …», «hvilke … har dere», «har dere …» |
| unngå | Gjesten har fått merkingen og beskrivelsen for det hun spør om, og er vist til personalet | «jeg tåler ikke …», «jeg er allergisk mot …», «jeg spiser ikke …», «uten …» |
| bord | Gjesten har fått vite hvordan hun bestiller bord | «bestille bord», «booke», «reservere» |
| åpningstid | Gjesten har fått åpningstiden, eller beskjed om at den må bekreftes | «når åpner dere», «åpningstider», «har dere åpent» |

«Jeg liker …» og «jeg liker ikke …» er ikke formål, men interesser med fortegn.

## To måter å regne på, med samme emner

Gjesteflaten regner i dag slik (`PalazzoScaffold/Sources/App/Models/PalazzoSignalGraph.swift`, linje 234–246): gjestens vekt ganger andelen av rettens emner som treffes. Kjernen har en annen ferdig regning (`CellProtocol/Sources/CellBase/PurposeAndInterest/InterestPurposeWeightedSum.swift` på pinnen `81601a6f`): gjestens vekt ganger vekten på kanten, summert. Tabellen viser hva de gir med emnene over. Tallene er regnet av skriptet, ikke av programkoden.

| Setning | Gjesteflatens regning (enhetsvekt på kantene) | Kjernens regning (vektene over) |
|---|---|---|
| «Jeg liker ost» | 0,333 Formaggi misti<br>0,143 Torta di mascarpone e pistacchi<br>0,125 Arancini | 1,0 Formaggi misti<br>0,4 Arancini<br>0,3 Torta di mascarpone e pistacchi |
| «Jeg liker pistasj» | 0,143 Torta di mascarpone e pistacchi<br>0,125 Agnello arrosto con salsa di pistacchio di Brontë | 0,7 Agnello arrosto con salsa di pistacchio di Brontë<br>0,7 Torta di mascarpone e pistacchi |
| «Jeg liker blekksprut» | 0,125 Carpaccio di polpo | 1,0 Carpaccio di polpo |
| «Jeg liker lam» | 0,125 Agnello arrosto con salsa di pistacchio di Brontë | 1,0 Agnello arrosto con salsa di pistacchio di Brontë |
| «Jeg liker trøffel» | 0,167 Pizza Tartufo "Umami" | 0,7 Pizza Tartufo "Umami" |
| «Jeg liker sitron» | 0,167 Crema di limone Siciliana<br>0,143 Pasta vongole<br>0,125 Carpaccio di polpo<br>0,125 Orata al forno a legna<br>0,1 Busiate Primavera | 1,0 Crema di limone Siciliana<br>0,4 Busiate Primavera<br>0,4 Carpaccio di polpo<br>0,4 Orata al forno a legna<br>0,4 Pasta vongole |
| «Jeg liker ikke ost», og så desserter | 0,167 Crema di limone Siciliana | 0,5 Crema di limone Siciliana<br>0,2 Torta di mascarpone e pistacchi<br>-0,5 Formaggi misti |
| «Jeg liker ost», og så desserter | 0,667 Formaggi misti<br>0,286 Torta di mascarpone e pistacchi<br>0,167 Crema di limone Siciliana | 1,5 Formaggi misti<br>0,8 Torta di mascarpone e pistacchi<br>0,5 Crema di limone Siciliana |
| «Jeg spiser ikke kjøtt», pizzaene | -0,125 Pizza Vulcano<br>-0,167 Pizza Tartufo "Umami" | -0,5 Pizza Tartufo "Umami"<br>-0,5 Pizza Vulcano |

Gjesteflatens regning er her regnet med `negativeScale` 1,0, som på grenen som står på nett. Vektene du valgte 2. oktober har `negativeScale` 0,5 (grenen `codex/palazzo-vekter-20260928`). Da blir raden «Jeg liker ikke ost», og så desserter: 0,167 Crema di limone Siciliana, 0,167 Formaggi misti, 0,071 Torta di mascarpone e pistacchi. Med 1,0 faller osteretten og ostekaken til null; med 0,5 er osteretten fortsatt med. En rett med sum null er utelatt i tabellen; en negativ sum betyr at retten trekkes ned.

Det tabellen viser: med gjesteflatens regning avgjør antall emner på retten. Formaggi misti har tre emner og Arancini åtte, så «ost» gir osteretten først uten at noen vekt er satt. Med kjernens regning avgjør vekten på kanten. Begge gir osteretten først for «Jeg liker ost» og begge gir to retter for «Jeg liker pistasj». De skiller seg når en rett har mange emner: da taper den i gjesteflatens regning selv om emnet er det retten er.

## Et «liker ikke», regnet på fire måter

Gjesten har sagt «Jeg liker ikke ost», og spør så etter desserter. Testen i spesifikasjonen (`test.samtale.liker-ikke`) krever at osteretten ikke står først, og at den ikke er stengt ute. Tabellen viser alle tre dessertene, også når summen er null. Tallene er regnet av skriptet, ikke av programkoden.

| Regning | Torta di mascarpone e pistacchi | Crema di limone Siciliana | Formaggi misti | Øverst |
|---|---|---|---|---|
| Gjesteflatens regning, `negativeScale` 1,0 (på nett i dag) | 0,0 | 0,167 | 0,0 | Crema di limone Siciliana. Osteretten har null og faller ut |
| Gjesteflatens regning, `negativeScale` 0,5 (vektene du valgte 2. oktober) | 0,071 | 0,167 | 0,167 | likt øverst: Crema di limone Siciliana og Formaggi misti |
| Planens forslag (vekt på kanten), `negativeScale` 1,0 | 0,048 | 0,139 | -0,278 | Crema di limone Siciliana |
| Planens forslag (vekt på kanten), `negativeScale` 0,5 | 0,083 | 0,139 | 0,0 | Crema di limone Siciliana. Osteretten har null og faller ut |

Det tabellen viser: med vektene du valgte 2. oktober (0,5) og gjesteflatens regning står osteretten likt med sitronkremen øverst, og da avgjør rekkefølgen ved likt tall om testen holder. I de tre andre regningene står sitronkremen alene øverst. Osteretten får null i to av dem og en negativ sum i én, og er da ute av det conciergen foreslår selv for dette spørsmålet. Spesifikasjonen åpner for det (F5: «det kan falle under terskelen for det conciergen foreslår selv, men spør gjesten om det, får hun svar»). Planen foreslår en regel for likt tall (valg 19 i `PLAN.md`), så testen ikke henger på rekkefølgen to like tall får.

