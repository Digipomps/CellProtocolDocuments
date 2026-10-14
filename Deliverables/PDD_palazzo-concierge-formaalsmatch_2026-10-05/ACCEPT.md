# ACCEPT — PDD_palazzo-concierge-formaalsmatch

Andre utgave, 7. oktober 2026 kl. 16:45 UTC (første kl. 15:40 UTC), for **utsetting 1**, før noe er satt ut. Forventningen er §3 i
`FORMAALSSPEC.md`; de godkjente bildene (G1-GUI, 7. oktober) er referansen for `test.gui.parity`. Faktisk er siden slik
den står i arbeidspakke 10 (`HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/pakker/pakke10/`, grønn i `svar/d182-pakke10.md`),
rendret i skyen med sidens eget skript og konvolutter laget av utgaven utenfor Swift (samme form som koden gir;
`formaalsmatch/kontroll/RAMMER10/`). Radene «kjørende flate» fylles når utsettingen står bak bryteren — de er `venter`,
ikke grønne. G3 er Kjetils ord; ingenting her setter den.

## parity

Side om side, samme vindusbredde (1280 px, 390 px for den smale), i `images/aksept/<ramme>-side-om-side.png`. Tre rammer er
piksel for piksel like de godkjente (`tilbud`, `forteller`, `ja`). Avvikene:

| Avvik | Rammer | Rettet / til Kjetil |
|---|---|---|
| **Linjen «Spør personalet om allergener før du bestiller.» står under kvitteringene.** Bildene 4A og 7A–C har ingen advarsel under en kvittering; kontraktens regel 8 sier at linjen står der til Kjetil har valgt (valg 21) | `kvittering-liker-ikke`, `notert`, `notert-fjernet`, `notert-tomt`, `nei`, `spiser-ikke` | **til Kjetil** (valg 21). Linjen er den korte av de tre koden på nett har |
| Hjelpelinjen under det som er notert: bilde 7A har «… Trykk ✕ for å fjerne én ting, eller «Fjern alt».» i tillegg; alle de andre bildene har bare «Gjelder mens du har siden åpen. Ikke lagret.». Siden har én linje, den korte | `notert` | **til Kjetil**: den korte står i fem av seks bilder med stripen; ✕ har «Fjern «…»» som tilgjengelighetsnavn |
| Kvitteringen etter «Jeg spiser ikke kjøtt.» sier «Notert: du spiser ikke kjøtt. Jeg foreslår derfor ingen retter selv. Spør personalet om hva som passer.» Bilde 7A lover listen over hva som nevner kjøttvarer; den kommer med F8 (utsetting 2) og loves ikke før (kontrakten, «Det bildene ikke viser») | `notert`, `spiser-ikke` | **til Kjetil** (ordlyd som ikke står i bildene) |
| «liker Eplemost» med stor E i «Slik forsto jeg deg» og i stripen; bildet har «eplemost». Grafen har ingen emne «eplemost», setningen når posten `bev-eplemost`, og navnet er postens felt ordrett (regel 7) | `flere-drikke` | **til Kjetil**: enten slik, eller et emne «eplemost» i datafilen (en dataendring, ingen kode) |
| Bildet for de fire tilbudene viste bare svaret (kildene og stripen var skjult i skissen for å få fire rammer ved siden av hverandre). Siden viser kildene og stripen («liker blekksprut» osv.), som i bilde 1 | `flere-forrett`, `flere-hovedrett`, `flere-pizza`, `flere-drikke` | ikke et avvik i siden; skissens beskjæring. Delen over kildene er piksel for piksel lik |
| Den smale rammen er 2 px lavere enn den godkjente; innholdet er det samme (delpikselavrunding i skissens ekstra stilark) | `tilbud-mobil` | ingen handling |
| «Slik forsto jeg deg» sto over kvitteringene i første rendering; bildene 4A og 7A har den ikke der | — | **rettet** før pakken (linjen vises over tilbud, forteller og henvisning, ikke over kvitteringer) |

Rammer uten godkjent bilde (ny ordlyd i utsetting 1, «Det bildene ikke viser» i kontrakten), vist for Kjetil her:

| Ramme | Hva | Ordlyd |
|---|---|---|
| `henvist-taaler-ikke` | «Jeg tåler ikke nøtter.» i utsetting 1: henvisningen `ask` gir i dag, med «Slik forsto jeg deg: du tåler ikke nøtter.» og «tåler ikke nøtter» (rød kant) i stripen. Bilde 4B (listen med merking) er F8, utsetting 2 | som i dag |
| `nei` | «Nei takk» til et tilbud | «Greit. Da noterer jeg ingenting.», med «Svar» over |
| `spiser-ikke` | «Jeg spiser ikke kjøtt.» alene | «Notert: du spiser ikke kjøtt. Jeg foreslår derfor ingen retter selv. Spør personalet om hva som passer.» |
| `lister-pizza` | «Hvilke pizzaer har dere?» | «Vi har fem pizzaer:» og én linje per pizza, «⟨navn⟩ (pizza): ⟨beskrivelse⟩»; «Slik forsto jeg deg: du spør om pizza.»; ingenting notert |

Det angrepet fant og som står (vises her for G3, `TESTRESULT.md#uavhengig`): «Slik forsto jeg deg» snur doble nektelser
(«Jeg hater ikke ost» → «du liker ikke ost»; gjesten ser det og kan fjerne det med ✕, og et «liker ikke» trekker bare ned);
«Er Arancini fri for nøtter?» gir henvisningen og noterer «spiser ikke Arancini» (F8, utsetting 2, gir svaret); «Jeg er
al lergisk mot ost» (delt ord) når matchen; ordet som traff, kommer tilbake normalisert i `understood.interests[].matched`.

Knappene (`test.live`, delen som kan prøves før utsetting): Ja, Nei, ✕ på en post og «Fjern alt» er trykket på siden i
skyen, og det siden sendte, står i `formaalsmatch/kontroll/RAMMER10/vist.json` (bare `kind` og `node` i `noted`,
`graph_version` med, `choice` nøyaktig slik leseren vil ha den). Det siden ikke gjør: lagrer noe (ingen localStorage,
cookies eller IndexedDB — `LES10-JS.md` punkt 3), setter inn tekst som HTML (punkt 4), kaller `ask` når det nye kallet
finnes (punkt 2).

## Rad for rad (§3)

| Leveranse (§3) | Forventet | Faktisk | Evidens | Står |
|---|---|---|---|---|
| Siden med et tilbud («Jeg liker ost») | `images/concierge-tilbud-v1.png` | piksel for piksel lik | `images/aksept/tilbud-side-om-side.png`, `tilbud-mobil-side-om-side.png` | lik |
| Tilbud om andre slags ting (forrett, hovedrett, pizza, drikk) | `images/concierge-tilbud-flere-v1.png` | lik over kildene; «Eplemost» med stor E | `images/aksept/flere-*-side-om-side.png` | til Kjetil (E) |
| Et svar som bare forteller («Jeg liker pistasj») | `images/concierge-forteller-v1.png` | piksel for piksel lik | `images/aksept/forteller-side-om-side.png` | lik |
| En kvittering uten tilbud («Jeg liker ikke ost»), og svaret på en liste etter «Jeg tåler ikke nøtter.» | `images/concierge-kvittering-v1.png` | 4A: lik, pluss linjen om allergener (valg 21). 4B: utsetting 2; i utsetting 1 henvisningen | `images/aksept/kvittering-liker-ikke-side-om-side.png`, `henvist-taaler-ikke-side-om-side.png` | til Kjetil (valg 21); 4B venter |
| Svaret når gjesten sier ja | `images/concierge-ja-v1.png` | piksel for piksel lik | `images/aksept/ja-side-om-side.png` | lik |
| Listen etter «Jeg tåler ikke selleri.» og etter «Jeg spiser ikke kjøtt.» | `images/concierge-unngaar-v1.png` | utsetting 2 (F8). I utsetting 1: henvisningen, og kvitteringen uten liste | `images/aksept/spiser-ikke-side-om-side.png` | venter (utsetting 2) |
| Det conciergen har notert, og hvordan gjesten fjerner det | `images/concierge-notert-v1.png` | 7A: lik, pluss linjen om allergener, kortere hjelpelinje, kvitteringsteksten for utsetting 1. 7B, 7C: like, pluss linjen om allergener | `images/aksept/notert-side-om-side.png`, `notert-fjernet-…`, `notert-tomt-…` | til Kjetil (valg 21, hjelpelinjen, ordlyden) |
| Når matchen feiler: spørsmålet til gjesten, «tolket av en språkmodell» | `images/concierge-modell-bak-v1.png` | utsetting 3 | — | venter (utsetting 3) |
| Når gjesten vil beholde det som er notert | `images/concierge-behold-v1.png` | avhenger av veien fra siden til gjestens entitet (§2) | — | venter |
| «Jeg liker ost» på nett gir tilbudet | kjørende flate | ikke satt ut | — | venter |
| Et ja på nett gir svaret på bildet, og ingenting bestilles | kjørende flate | ikke satt ut (i testene: ingen nøkkel kalles, `testSvarVaktenByggerOgValgNaarIngenCelle`) | `TESTRESULT.md#tilbud` | venter |
| «Jeg liker ikke ost» på nett gir en kvittering uten tilbud | kjørende flate | ikke satt ut | — | venter |
| «Hva er egentlig Arancini?» … «Hva har dere med pistasj?» gir rettene | kjørende flate | ikke satt ut; i referansen: `navngitt`, `forteller-pistasj`, `lister` | `Tests/AppTests/Fixtures/formaal-samtale-referanse.json` | venter |
| «Er det hvete i Carpaccio di polpo?» … gir aldri bare rettbeskrivelsen | kjørende flate | som i dag (`c5058f49`, strakstiltaket); det nye kallet gir henvisningen ordrett (`testHenvisningenErOrdrettSomAskOgDetGjestenUnngaarNoteres`) | `TESTRESULT.md#allergi` | venter på nett |
| «Jeg tåler ikke nøtter.» og så «Hva har dere til dessert?» | kjørende flate | utsetting 2 (listen med merking). Utsetting 1: intet tilbud, henvisningen (`testStaarDetNoeGjestenUnngaarKommerVerkenTilbudEllerListe`) | `TESTRESULT.md#samtale` | venter |
| «Jeg tåler ikke selleri.» / «Jeg tåler ikke egg.» og så forrettene | kjørende flate | utsetting 2 | — | venter |
| «Jeg spiser ikke kjøtt.» og så «Hvilke pizzaer har dere?» | kjørende flate | utsetting 2. Utsetting 1: ingen liste fra matchen, oppslaget svarer som i dag (`testSpiserIkkeGirKvitteringOgIngenListe`) | `TESTRESULT.md#samtale` | venter |
| En setning matchen bommer på: spørsmålet til gjesten | kjørende flate | utsetting 3 | — | venter |
| Gjesten som vil beholde det som er notert | gjesteflaten | §2 | — | venter |
| Emnene for de 18 rettene og 17 drikkene | `graf/emner-v1.md` | finnes; «vin» kom til (`testEmneneErDemIForslagetOgVin`) | `TESTRESULT.md#graf` | levert |
| Korpus og fasit | `maaling/korpus/`, `maaling/fasit/` | finnes (689 rader, 517/172) | `TESTRESULT.md#fasit` | levert |
| Husets graf, første utgave, med versjon | `PS/Sources/App/Resources/RestaurantConcierge/palazzo_husgraf.json` | `husgraf-20261007.5` i arbeidstreet; `graf/palazzo_husgraf-20261007.5.json` | `TESTRESULT.md#graf` | levert, ikke committet |
| Prøven av grafdatabasen mot fil | `maaling/rapport/` | `MAALING-1-20261007.md` | `TESTRESULT.md#graf` | levert |
| Måling før og etter | `maaling/rapport/` | dekomponeringen målt (87,4 % trening, 72,7 % holdout, begge deler); dagens oppslag mot matchen på nett: ikke målt | `TESTRESULT.md#forstaaelse` | delvis |
| Revisorens forslag og endringsloggen | `maaling/grafendringer/` | utsetting 2/3; grafens endringer står i `graf/ENDRINGSLOGG.md` | — | venter |
| Det som er ført opp ved bom på nett | `HD/maal/BOMLOGG-<dato>.md` | ikke satt ut | — | venter |
| Kontrakten og dataflyten | `contract/`, `dataflow.md` | `contract/SAMTALE-UTSETTING-1.md` (andre utgave), `dataflow.md` | `TESTRESULT.md#contract` | levert |
| Uavhengig angrep | `HD/maal/uavhengige/` | kjørt: 197 samtaler, målt én gang (`d183`, to ekte funn), rettet, målt på nytt (`d184`, 0 brudd). `HD/maal/uavhengige/ANGREP-FORMAALSMATCH-RAPPORT-20261007.md` | `TESTRESULT.md#uavhengig` | levert |
| Hele testmengden | `HD/maal/PINTEST-*-<dato>.md` | 375 tester, 0 feil (`d184`); «rød først» per pakke | `TESTRESULT.md#regression` | grønn i arbeidstreet |
| Kvittering for utsettingen | `HD/maal/VERTSDEPLOY-*-<dato>.md` | ingen | — | venter |

## live, samtale, logg, deploy

Fylles etter utsetting bak `PALAZZO_CONCIERGE_SAMTALE=1`, på Kjetils ord. Ingen måling på nett er gjort for det nye kallet.

## docs, status, stubs, ways-in

- `docs`: `PalazzoScaffold/README.md` er ikke oppdatert ennå (gjøres i commiten); `HAVEN-Deploy/_handoff/HD-0077/README.md` får
  et avsnitt før push. Setningen til gjesten på siden (`Spør med egne ord, eller velg en snarvei. Det du sier om deg selv,
  huskes mens du har siden åpen, og lagres ikke.`) vises bare når det nye kallet finnes.
- `status`: `STATUS.md` er à jour per 15:33 UTC (loggen).
- `stubs`: ingen tomme stubber i de 28 filene (`formaalsmatch/kilde.filer`); `interpreted_by_model` er `null` med vilje i utsetting 1.
- `ways-in`: ikke aktuell (HTML).
