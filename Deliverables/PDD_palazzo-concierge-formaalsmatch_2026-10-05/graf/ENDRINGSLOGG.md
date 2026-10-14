# Endringslogg for husets graf (`graf/ENDRINGSLOGG.md`)

Ført av Losen. Stier er relative til oppgavemappen der ikke annet står. Datafilen heter `PalazzoScaffold/Sources/App/Resources/RestaurantConcierge/palazzo_husgraf.json` i pakken; hver versjon ligger også her i `graf/`.

En endring i grafen er en endring i datafilen, ikke i koden. Hver versjon har en fil ved siden av seg, `graf/endringslogg-<versjon>.json`, som for hver oppføring sier hvilke treningsrader den retter. Den er regnet med `maaling/prototype/endringslogg.py` (fra versjon `.3` med `maaling/prototype/endringslogg2.py`, som også tar med treningsradene i korpus 2: 714 rader i alt): oppføringen tas ut alene, og treningsradene måles på nytt. Radene som da blir feil, er dem oppføringen retter. Holdout-radene er ikke målt der, og ingen oppføring er begrunnet med en holdout-rad (`test.maal.holdout-urort`).

En oppføring uten treningsrad er ikke nødvendigvis overflødig. Den kan være begrunnet i menyen, i en test, eller i det en uavhengig tråd vet om språk. Og når to oppføringer retter samme rad, viser ingen av dem det alene.

## Versjonene

| | `husgraf-20261007.1` | `husgraf-20261007.2` | `husgraf-20261007.3` | `husgraf-20261007.4` |
|---|---|---|---|---|
| emner | 86 | 86 | 86 | 86 |
| kanter | 151 | 151 | 151 | 151 |
| ordformer for emner | 285 | 654 | 964 | 964 |
| ekstra navn på retter og drikke | 20 | 20 | 20 | 20 |
| ord for allergener | 71 | 129 | 153 | 153 |
| ord som selv sier «tåler ikke» eller «uten» | 25 | 25 | 37 | 37 |
| unntak | 12 | 12 | 13 | 13 |
| stikkord | 368 | 470 | 758 | 758 |
| nektelser | 26 | 36 | 52 | 52 |
| ord i ordlistene | 167 | 233 | 444 | 444 |
| oppføringer i endringsloggen | 1103 | 1708 | 2570 | 2570 |
| av dem: retter minst én treningsrad alene | 220 | 211 | 257 | 257 |
| av dem: en treningsrad blir riktig uten oppføringen | 10 | 10 | 17 | 17 |
| treningsrader lest som fasiten (av 517), regnet i prototypen | 450 | 451 | 452 | 452 |
| treningsrader i korpus 2 lest som fasiten (av 197), regnet i prototypen | 112 | 122 | 145 | 145 |

### `husgraf-20261007.1` (7. oktober 2026 kl. 09:40 UTC)

Første versjon. Emnene og kantene er dem i `graf/emner-v1.json`, uendret: 85 emner og 151 kanter. I tillegg:

- **Emnet `vin`**, uten kant til noen rett eller drikk. Spesifikasjonen krever at «hvitvin» og «rødvinsbraiserte» gir vin (`test.dekomp.ordformer`), og forslaget hadde bare `hvitvin` og `rødvin`. Et ord kan gi to noder: «hvitvin» gir både `hvitvin` og `vin`. Huset har ikke vin på siden, så `vin` fører ikke til noe tilbud.
- **Én node per allergen** (14), laget av korpusets liste og ikke av beskrivelsene, slik `graf/emner-v1.md` sa måtte inn. Ordene for dem står under `allergenord`. Ingen kant går fra en ingrediens til et allergen.
- **Ordformer, navn og unntak**, skrevet av Losen med treningsradene og menyen foran seg.
- **Conciergens språk** (`spraak` i samme fil): stikkordene som sier hva gjesten gjør med det hun nevner (liker, vil ha, tåler ikke, uten …), nektelsene, og ordlistene for bord, åpningstid, kosthold, mat og drikke.
- **De 8 artiklene** leses fra `PalazzoScaffold/Sources/App/Resources/Demo/palazzo_demo_story.json` med tittel og emner. De står ikke i leksikonet, og dekomponeringen gir dem aldri.

Unntakene, og hvorfor: «ristet», «riste», «rista», «risiko», «risk» treffer ikke ris; «lokal» treffer ikke løk; «lampe» treffer ikke lam; «desserter» treffer ikke erter; «vinter», «vindu», «vinn», «vinge» treffer ikke vin. De er funnet med `maaling/prototype/kollisjoner.py` og med testen `testHvertUnntakGjelderEtOrdRegelenEllersVilleTruffet`.

Oppføringer som gjør en treningsrad feil, og som står likevel:

| Oppføring | Raden som blir riktig uten | Radene den retter |
|---|---|---|
| `graf/ordformer/kjøtt`: «kjøt» | s058e372 | s5607e6a, sffb7c28 |
| `graf/ordformer/kjøtt`: «meat» | s116e163 | ingen alene |
| `graf/drikkeemner`: «brus» | sc05e73f | s08b06b6 |
| `graf/drikkeemner`: «vin» | s66d0760, s83fcf01 | s80199c6, s9a3d655 |
| `graf/stedsemner`: «sicilia» | s66d0760 | s0b78b9e, s9a3d655 |
| `spraak/stikk/VIL`: «tenker på» | s520d126 | s6a500e0 |
| `spraak/stikk/VIL`: «bestille» | sf7e3193 | ingen alene |
| `spraak/stikk/ALLERGI`: «allerg*» | s13c4aa0, saed52c6 | s1066921, s26af161, s27535a8, s35444c2, s35f34a7, s38c97ae, s3ad7e74, s4ebc864, s67c638b, s8d36116, s97bd6ca, s9d791e2, sa7a04d8, sa877e32, sae1828e, sba7aa39, sc61ac47, sc70d208, sda72d4f, se28d183, sf693e59, sf92a718 |
| `spraak/stikk/SPOER`: «is there» | s1cede3c | ingen alene |
| `spraak/ordlister/har_dere`: «har dere» | s83fcf01 | s90f2f5f, s92a9eb8, s9a3d655, sc810143 |

Tre av dem retter ingen rad alene: «meat» (kjøtt), «bestille» (som ønske) og «is there» (som spørsmål). «bestille» tas ut i neste versjon; «kan jeg bestille» står. De to andre er vanlige ord for det de står for, og står.

### `husgraf-20261007.2` (7. oktober 2026 kl. 10:03 UTC)

Ordformer og stikkord fra fire uavhengige tråder som ikke hadde sett korpuset (`maaling/ordlister/README.md`): 371 ordformer for emner, 57 ord for allergener, 102 stikkord, 10 nektelser og 66 ord i ordlistene. Tre rettelser i det som sto: «kveite» (også en fisk) er byttet med «kveitemjøl» og «kveitemel» under hvete; «skaldjur» er tatt ut av emnet sjømat (det betyr skalldyr); «fried» er tatt ut av fritert (det betyr også stekt).

Målt i prototypen: én treningsrad til leses som fasiten (451 av 517), ingen blir dårligere. På holdout-radene, som ikke er lest: 121 av 172 mot 117 før. Tallene fra Swift-koden står i `TESTRESULT.md#forstaaelse`.

### `husgraf-20261007.3` (7. oktober 2026 kl. 11:28 UTC)

Laget etter den første målingen på setninger fra nye skribenter (`maaling/rapport/MAALING-1-20261007.md`), der versjon `.2` leste 176 av 281 slik tolkene gjorde. md5 `116d851f7e6db0cd4e671039b6a3483c`.

**Fra fem uavhengige tråder** som ikke hadde sett en eneste setning (`maaling/ordlister2/README.md`): 309 ordformer for emner, 23 ord for allergener, 270 stikkord, 16 nektelser og 212 ord i ordlistene. Runden ba særlig om talemål skrevet ned, svensk og dansk, engelsk slik turister skriver, og chat-språk.

**Fra Losen**, etter lesing av treningsradene i korpus 2 (`maaling/ordlister2/tillegg-egne-3.json`): 19 stikkord («tar vi gjerne», «vil æ ha», «jag tänkte ta», «etterpå», «til slutt», «drømmer om» og flere) og ordformen «ärter» for erter, som helt ord.

**Seks rettelser i det som sto.** Hver har et navn i `maaling/prototype/lag_data.py`, så den kan holdes utenfor i en prøve (`UTEN=<navn>`):

| Navn | Rettelse | Hvorfor |
|---|---|---|
| `menta` | «menta» under mynte treffer bare som helt ord | «dokumentasjon» traff mynte |
| `te` | «te» er tatt ut av ordene for drikke | «te» er trøndersk for «til» («bord te fire», «te mæ»). Tre av trådene pekte på det |
| `forskjell` | Nytt unntak: «forskjell» treffer ikke skjell | «forskjellen» traff skjell |
| `bestille` | «bestille» alene er tatt ut som ønske om mat. «kan jeg bestille» står | Varslet under versjon `.1`: ordet er oftere bord enn mat, og rettet ingen rad alene |
| `sedano` | «sedano» lagt til under allergenet selleri | Emnet selleri hadde ordet, allergenet ikke |
| `utsagn` | Tolv ord som i seg selv sier «uten» eller «tåler ikke» (25 ble 37) | Trådene foreslo dem som vanlige ord for allergener; de sier mer enn det |

**Nytt avsnitt `graf.svar`**, brukt av arbeidspakke 5 (`contract/SAMTALE-UTSETTING-1.md`): tallet for klar leder (2,5, foreløpig), emnene som bare fører til drikke med alkohol (hvitvin, rødvin, vin, øl; leseren kontrollerer listen mot kantene), og formen hvert emne har i en overskrift («retter med ost», «pizzaer», «drikker uten alkohol»).

**Avvist for hånd** (`maaling/ordlister2/haand/avvist.json`, 43 uttrykk med dem fra runde 1): nektelsene «shouldn t», «wouldn t» og «couldn t» gjorde en treningsrad feil («a town we shouldn't miss»); «først» som høflighetsord gjorde en treningsrad feil («er den kokt først?»); «til dessert», «til forrett» og «for starters» som høflighetsord ville slukt emneordet. Svensk «ärter» blir «arter» etter normaliseringen og traff «starter»; derfor står det som helt ord.

**Målt i prototypen** (`maaling/prototype/sammenlign2.py`): korpus 1 trening 452 av 517 (før 451), korpus 2 trening 145 av 197 (før 122). Ingen treningsrad som var riktig, ble feil. På radene som ikke er lest: korpus 1 125 av 172 (før 121), korpus 2 56 av 84 (før 54). De 84 er fra de samme seks skribentene som treningsradene i korpus 2, så det er ikke et nytt usett tall. Et nytt usett tall krever nye skribenter.

**Tre ting som svekker runden:** tre av de fem trådene gikk over fristen på 8 minutter (8 min 32 s, 10 min 5 s og 11 min 24 s). Reglene trådene fikk, hadde tre eksempelfraser hentet fra treningsrader i korpus 2 («har løst på», «I'm in the mood for», «could go for»), så trådene var ikke uavhengige for dem. Og Losens egne tillegg er gjort med treningsradene foran seg, slik ordlistene i versjon `.1` var.

**Kjørt i Swift 7. oktober kl. 13:53–13:54 UTC** (`d177`, `HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/svar/d177-dataversjon-3.md`, relativt til HAVEN-roten): Swift gir samme lesing som prototypen for alle 769 setninger (0 avvik), og på holdout-radene 125 av 172. Én test rød: dekomponeringen bruker 12,3 ms per setning mot grensen på 10 ms (`test.match.tid`); det er tiden, ikke lesingen. Referansen for Swift-testen ligger i `HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/data/husgraf-20261007.3/`; den dekker korpus 1. Korpus 2 er ikke lagt inn som fikstur for Swift ennå.

Oppføringer som gjør en treningsrad feil, og som står likevel (rader som begynner med `s`, er fra korpus 1; `t` er fra korpus 2):

| Oppføring | Raden som blir riktig uten | Radene den retter |
|---|---|---|
| `graf/ordformer/grønnsaker`: «grønt» | t86de21f | s978810b, sbacfb3b |
| `graf/ordformer/kjøtt`: «kjøt» | s058e372 | s5607e6a, sffb7c28 |
| `graf/ordformer/kjøtt`: «meat» | s116e163 | ingen alene |
| `graf/ordformer/kjøtt`: «kött» | s3df28f8 | t51b56b2, t5f03148 |
| `graf/allergenord/HV`: «flour» | t5f35b91 | ingen alene |
| `graf/drikkeemner`: «brus» | sc05e73f | s08b06b6, t40c7418, t7379cbf |
| `graf/drikkeemner`: «vin» | s66d0760, s83fcf01 | s80199c6, s9a3d655 |
| `graf/stedsemner`: «sicilia» | s66d0760 | s0b78b9e, s9a3d655 |
| `spraak/stikk/VIL`: «noe med» | t685f442 | s74f1ba6, sea7b70e, t1c23db0 |
| `spraak/stikk/VIL`: «tenker på» | s520d126 | ingen alene |
| `spraak/stikk/VIL`: «would like» | t1ba76bc | ingen alene |
| `spraak/stikk/ALLERGI`: «allerg*» | s13c4aa0, saed52c6 | s1066921, s26af161, s27535a8, s35444c2, s35f34a7, s38c97ae og 16 til |
| `spraak/stikk/UNNGAAR`: «vil ikkje ha» | t685f442 | ingen alene |
| `spraak/stikk/SPOER`: «is there» | s1cede3c | ingen alene |
| `spraak/ordlister/drikkeord`: «glass» | t3e19222 | ingen alene |
| `spraak/ordlister/har_dere`: «har dere» | s83fcf01 | s90f2f5f, s92a9eb8, s9a3d655, sc810143, t2e280f9 |
| `spraak/nektelser`: «itj» | t2163fa8 | s03b6422 |

Sju av dem retter ingen rad alene: «meat», «flour», «tenker på», «would like», «vil ikkje ha», «is there» og «glass». De er vanlige ord for det de står for, og står. «tenker på» rettet én rad i versjon `.1`; den raden leses nå riktig også uten.

### `husgraf-20261007.4` (7. oktober 2026 kl. 14:47 UTC)

Lik `.3` i alt som gjelder lesingen av en setning. Én nøkkel er tatt ut av avsnittet `graf.svar.fortell`: overskriften «drikker uten alkohol» for emnet alkoholfritt. Den sa «uten», som ingen svartype skal si (`contract/SAMTALE-UTSETTING-1.md`, regel 9), og nådde gjesten med skrivemåter som «alkofri» og «alc free», som ikke har ordet alkohol i seg. En uavhengig leser fant det. Listen over drikke uten øl og vin får nå den nøytrale overskriften. md5 `b75952b6d9f773746ddf3251031ece4d`.

Referansen for dekomponeringen er den samme som for `.3` bortsett fra versjonsnavnet (`HAVEN-Deploy/_handoff/HD-0077/formaalsmatch/data/husgraf-20261007.4/`, relativt til HAVEN-roten; md5 `52c11e7b94b9e6468428563465aee0ce`). Referansen for samtalen (`maaling/prototype/lag_samtalereferanse.py`) er laget mot `.4`. Ingen endringslogg-fil per oppføring er regnet på nytt: ingen oppføring som gjelder lesingen, er endret.

### `husgraf-20261007.5` (7. oktober 2026 kl. 16:40 UTC)

Etter det uavhengige angrepet på den ferdige koden (`HAVEN-Deploy/_handoff/HD-0077/maal/uavhengige/ANGREP-FORMAALSMATCH-NOTAT-20261007.md`,
relativt til HAVEN-roten). Bare ord er lagt til; ingen kant, intet emne og ingen post er endret. md5 `b96e3de41b98a947e02a894aacfd4e10`.

- `spraak/stikk/ALLERGI`: 116 uttrykk for at mat gjør noen syk, skrevet uten ordlistens ord — helse («gjør meg syk», «gir meg kvalme», «sykehus», «epipen»), fare («kan drepe meg», «dødelig for meg», «ta livet av»), følsomhet («sensitiv for», «ømfintlig», «histamin»), legen («legen har sagt»), og engelske former («could kill», «throw up»), samt bøyde former av uttrykk som alt sto («får jeg vondt av», «blir jeg dårlig»). Bare uttrykket «dødelig» alene er holdt unna: «livsfarlig god» og «dødelig god» er ros.
- `spraak/stikk/SPISER_IKKE`: 13 omvendte former («kan jeg ikke ha», «tåler jeg ikke», «må jeg ikke spise»).
- `spraak/stikk/UNNGAAR`: «fritt for», «frie for», «fritt frå», «free from any» («Har dere noe som er fritt for ost?» ga osteretten som tilbud).
- `graf/allergenutsagn/HV/spiser-ikke`: «gluttenfri», «gluttenfritt», «gluten fritt», «glutten fri».

Det retter: angrepets 26 setninger i gruppe C (av 32) får nå henvisningen, med det hun ikke tåler notert som emne; fem får oppslagets
svar som i dag; én («al lergisk», delt ord) når fortsatt matchen. I korpuset endres seks setninger, fire av dem treningsrader lest her:
s598681e (MSG, hodepine og kvalm → unngå), s765baf7 (legen sier … → `ukjent` tåles ikke, som fasiten), s9477ee7 («legen har sagt nei til
sterk mat» → sterk tåles ikke, som fasiten), se76e153 (sykehuset → chili tåles ikke, som fasiten), sfaf12b7 (epipen → sesam tåles ikke);
den sjette er en holdout-rad og er ikke lest. Samlet: trening 452 av 517 (uendret), holdout 125 → 126 av 172 med både formål og noder.
Referansen for dekomponeringen: md5 `c6cf460341ea675b60aee213a8b5f7d3`; for samtalen (166 samtaler, 421 steg): `8e0e391bbae02d610290ab17eecbe568`.

## Avvik fra `graf/emner-v1.md`

`test.graf.emner` sier at emnene i grafen er dem i `graf/emner-v1.md`. De er det, med ett tillegg: emnet `vin`. Allergenene er egne noder og ikke emner. `graf/emner-v2.md` lister det grafen har nå.
