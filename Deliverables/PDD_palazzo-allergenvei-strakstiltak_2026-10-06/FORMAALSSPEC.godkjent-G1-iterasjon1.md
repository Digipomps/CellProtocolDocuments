# Formålsspesifikasjon — palazzo allergenvei strakstiltak

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_palazzo-allergenvei-strakstiltak_2026-10-06` · Opprettet 2026-10-06 · Iterasjon 1 (ikke godkjent)

Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold`, `CPD` for `CellProtocolDocuments`, og `PDD` for denne oppgavemappen. Koden som er lest, er `PS` på grenen `deploy/palazzo-demo-20260930`, `a3fc5042`. Det er utgaven som står på nett. Alle klokkeslett er UTC.

Ordene brukes slik her. **Oppslaget** er koden som finner svaret i husets kunnskapsgrunnlag. **Merkingen** er husets allergenkoder for en rett, i formen «… er merket med: …». **Publiseringen** er steget som avgjør om oppslagets svar kan vises til gjesten. **Modellen og vakten** er AI-modellen som kan si et godkjent svar med andre ord, og kontrollen som bare slipper det gjennom når innholdet er uendret. Et **publisert svar** er et svar siden viser under «Kontrollert svar». **Avvist** betyr at siden viser «Ikke bekreftet ennå» og ber gjesten spørre vertskapet. **Henvisningen** er samme avvisning, gitt av tiltaket.

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## Kort — les dette først

**På seks linjer.**

1. I dag får gjester som spør om allergi, ofte et svar som ikke svarer på det de spurte om. Av 60 blinde spørsmål fikk 28 et publisert svar, og 9 av dem var en merking.
2. Tiltaket er tre regler: spørsmål med et ord fra en liste får henvisningen til personalet; merkingen vises aldri; hvert publisert svar får en linje som viser til personalet for allergener.
3. Listen er en ordliste og fanger ikke alt. I den eneste blinde prøven fanget den 42 av 60. Regel 2 og 3 står bak for resten.
4. Det koster: vanlige spørsmål med ord som fisk, egg, melk, trygt og gravid får også henvisningen, og de få svarene om allergi som er riktige i dag, forsvinner til F8.
5. Du må svare på fire spørsmål: G1, et lite tillegg, bildene, og hvor langt jeg går uten å spørre.
6. Tiden: rundt fem timer til det er målt på nett, hvis du velger «Auto, hele veien» og ingenting stopper meg.

**Hva du valgte.** Valget ditt «Strakstiltak i koden» ble lest 6. oktober kl. 06:05. Teksten på valget var min: «Alle spørsmål med ord om allergi eller trygghet får bare henvisningen til personalet.» Dette er spesifikasjonen for det. Den gjør mer enn teksten på valget sa. Hva, står under «Det G1 omfatter». Ingenting er endret i koden eller på nett.

**Formålet.** Til den nye allergenveien er bygget (F8 i `CPD/Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05/FORMAALSSPEC.md`), får ingen gjest et svar om allergi som huset ikke kan stå for. Spørsmål vi kjenner igjen, får henvisningen til personalet. Ingen merking kommer ut. Hvert svar conciergen likevel gir, viser til personalet for allergener.

**Hva som er galt i dag.** Målt på nett mot `a3fc5042`.

- 5. oktober skrev jeg 21 spørsmål om allergi og trygghet. 2 gikk riktig vei: gjesten spurte om gluten eller melk i en navngitt rett, og merkingen for retten har det. 3 ble avvist. 16 fikk et publisert svar som ikke svarte på det de spurte om: 9 fikk bare rettbeskrivelsen, 3 fikk merkingen for en rett de ikke nevnte, og 4 fikk merkingen for retten de nevnte, men hadde spurt om noe merkingen ikke sier noe om (selleri, egg, melk, og om retten er trygg ved nøtteallergi).
- 6. oktober skrev en uavhengig tråd 60 spørsmål om allergi, intoleranse og trygg mat, uten å ha fått se koden eller listen. 28 av de 60 fikk et publisert svar: 9 merkinger, 9 rettbeskrivelser, 7 pizzalister, 2 rettlister og 1 drikkeliste. 32 ble avvist. Bare én av de 9 merkingene svarte på det gjesten spurte om («allergener i pizza Salina?»).

| Gjesten skriver | Svaret på nett i dag | Hva som er galt | Fra |
|---|---|---|---|
| «Er det hvete i Carpaccio di polpo?» | «Carpaccio di polpo: Blekksprutcarpaccio med kokt potet, stangselleri, olivenolje og sitron.» | Bare beskrivelsen. Retten er merket med hvete. Svaret nevner verken merkingen eller personalet | de 21 |
| «Har dere pizza uten gluten?» | «Pizza Margherita er merket med: hvete/gluten (kode HV), melk (kode M), lupin (kode L). Ved alvorlig allergi eller spørsmål om krysskontakt må personalet bekrefte før bestilling.» | Svarer om en rett gjesten ikke nevnte | de 21 |
| «Jeg er allergisk mot selleri. Kan jeg spise Carpaccio di polpo?» | «Carpaccio di polpo er merket med: skalldyr (kode SK), hvete/gluten (kode HV). Ved alvorlig allergi eller spørsmål om krysskontakt må personalet bekrefte før bestilling.» | Rettens beskrivelse sier stangselleri. Merkingen har ikke selleri, og svaret sier ikke ja eller nei | de 21 |
| «Bruge dokke same frityren te arancini og fisk? Eg e allergisk mot fisk så eg må vida det» | «Arancini er merket med: hvete/gluten (kode HV), egg (kode E), melk (kode M), lupin (kode L). Ved alvorlig allergi eller spørsmål om krysskontakt må personalet bekrefte før bestilling.» | Gjesten spør om felles frityr. Svaret er en liste med koder, uten fisk | det blinde settet |
| «Eg toler ikkje mjølk. Kva pizza kan eg få utan ost, og er det mjølk i sjølve botnen?» | «Pizzaene i kunnskapsgrunnlaget er: Pizza Margherita, Pizza Siciliana, Pizza Vulcano, Pizza Tartufo "Umami", Pizza Salina.» | En liste med pizzaer som svar på hva gjesten tåler | det blinde settet |
| «Hva bør jeg bestille når jeg ikke kan spise mandler?» | «Bordbestilling hos Palazzo gjøres via bookinglenken https://booking.gastroplanner.no/palazzo/t. Kontakt: booking@Palazzocomunale.no. Telefon: +47 904 70 296. Concierge kan hjelpe med å formulere ønsket tidspunkt, antall gjester og behov, men kan ikke opprette eller endre reservasjonen her.» | Svaret om bordbestilling, fordi spørsmålet har ordet «bestille» | målt i dag kl. 09:16 |

Siden lover noe annet. Snarveien «Allergener og hensyn» har underteksten «Usikker informasjon stoppes alltid».

**Hva tiltaket gjør.** Tre regler i koden bak gjestens side. Oppslaget, modellen og vakten røres ikke.

- **Regel 1, ordlisten.** Har spørsmålet et ord fra listen, får gjesten henvisningen. Oppslaget spørres ikke.
- **Regel 2, ingen merking.** Merkingen («… er merket med: …») vises aldri. Svarer oppslaget med den, får gjesten henvisningen.
- **Regel 3, linjen.** Hvert publisert svar får en linje som viser til personalet for allergener, hvis det ikke har en linje om allergi fra før. Når merkingen er borte, er det bare rettlisten som har det.

```
Gjesten skriver i spørrefeltet,                 Gjesten trykker snarveien
eller trykker «Allergener og hensyn»            «Hva står på menyen?» eller «Hva kan jeg drikke?»
   │                                               │
   ▼                                               │
REGEL 1: ORDLISTEN (ny)                            │
   har spørsmålet et ord fra listen?               │
   ├── ja ──►  HENVISNINGEN til personalet.        │
   │           Oppslaget spørres ikke.             │
   └── nei                                         │
   ▼                                               ▼
OPPSLAGET        som i dag
   ▼
PUBLISERINGEN    som i dag, med to nye regler:
   │             REGEL 2: merkingen vises aldri. Kommer den hit, får gjesten henvisningen.
   │             REGEL 3: hvert publisert svar får en linje om allergener.
   ▼
MODELLEN OG VAKTEN   som i dag. Linjen står, også når modellen har formulert svaret.
```

En ordliste kjenner ord, ikke hva gjesten mener. Derfor står regel 2 og 3 bak den. Regel 2 trengs også fordi oppslaget sender flere ord til allergenveien enn listen fanger. Målt kl. 08:23: «Are there chestnuts in the Agnello arrosto?», «Har dere donuts til Arancini?» og «In a nutshell, what is Vitello tonnato?» får alle en merking i dag.

Med de tre reglene er hvert svar på gjestens side ett av to: avvisningen, som selv sier «Spør vertskapet, særlig om allergener», eller et publisert svar med en linje om allergener under. (Feilmeldinger, som at conciergen er utilgjengelig eller at det er sendt for mange spørsmål, er ikke svar og får ingen linje.)

**Det du kommer til å se.** Åtte bilder, laget med sidens egne filer og svar i samme form som tjenesten gir. Slik de er laget, står i `PDD/images/README.md`.

- `PDD/images/concierge-allergi-foer-etter-v3.png`: samme spørsmål i dag og etter. Under henvisningen står de to linjene avvisningen har i dag, og setningen siden selv legger til under alt som ikke er et kontrollert svar. Feltet «Kilder» vises ikke, fordi oppslaget ikke er spurt.
- `PDD/images/concierge-allergi-henvisning-mobil-v2.png`: henvisningen på en telefon.
- `PDD/images/concierge-linje-om-allergener-v2.png`: linjen under en rettbeskrivelse: «Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller.»
- `PDD/images/concierge-linje-to-retter-v1.png`: linjen når svaret har flere retter: «Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller.»
- `PDD/images/concierge-linje-under-lister-v1.png`: linjen under pizzalisten og drikkelisten: «Spør personalet om allergener før du bestiller.» Pizzalisten i bildet er formulert av modellen («Vi har disse pizzaene: …»).
- `PDD/images/concierge-linje-bordbestilling-v1.png`: samme linje under svaret om bordbestilling.
- `PDD/images/concierge-allergi-ordlyd-v5.png`: ordlyd A og B (se «Ordlyden»).
- `PDD/images/concierge-eksempel-v2.png`: tillegget (se «Tillegget»).

Rettlisten får ingen ny linje. Den har «Ved alvorlig allergi eller krysskontakt må personalet bekrefte før bestilling.» fra før (målt kl. 08:23 og 08:34).

**Hvor godt det virker.** Regnet med listen mot de 60 blinde spørsmålene, og holdt mot svarene på nett. Listen er ikke kjørt i Swift ennå. Bare første kolonne er en blind prøve. Listen som legges fram, er rettet etter settet og etter fire kontroller, og tallet for den er ikke en prøve. Prøven kommer i angrepet, med et nytt sett.

| De 60 blinde spørsmålene, etter tiltaket (regnet) | Listen slik den var da settet ble skrevet (blind prøve) | Listen som legges fram (utgave 5) |
|---|---|---|
| Får henvisningen | 42 (23 avvist i dag, 19 publisert i dag) | 51 (29 avvist i dag, 22 publisert i dag) |
| Fanges ikke, og blir avvist av oppslaget som i dag | 9 | 3 |
| Fanges ikke, og får samme svar som i dag | 9 (8 får den nye linjen; rettlisten har sin) | 6 (5 får den nye linjen; rettlisten har sin) |
| Får en merking | 0 (i dag 9) | 0 (i dag 9) |

Tråden som skrev settet, sier selv at rundt en tredel av de 60 er sjeldne tilstander, og at tallet bør leses med det. Alt står spørsmål for spørsmål i `HD/maal/STRAKSTILTAK-BLIND1-UTGAVE5-20261006.md`.

**Hva listen ikke fanger.**

- Ni av de 60 blinde: medisiner ved navn (Marevan, Antabus), sykdommer ved navn (urinsyregikt, Crohns, høyt blodtrykk, PKU), symptomer uten ordene på listen (spørsmålet som begynner «Blir kjempedårlig av glutamat»), ett spørsmål på italiensk, og ett der bokstaver er byttet med like tegn fra et annet alfabet. Seks av de ni får et publisert svar i dag, og får det samme etterpå. Linjen de får, handler om allergener. Fem av de seks spør om noe annet (blodfortynnende, Antabus, salt, urinsyregikt, Crohns), så for dem er svaret like lite til hjelp som i dag.
- Listen har navnene på allergengruppene, ikke alt som hører til dem. «Nøtter» treffer; «mandler», «pistasj» og «cashew» gjør det ikke. «Melk» treffer; «ost», «smør» og «fløte» gjør det ikke. «Skalldyr» treffer; «reker» gjør det ikke. Tre retter på menyen har mandler eller pistasj. «Er det mandler i Orata al forno a legna?» får samme svar som i dag, med linjen. Skal mandler, pistasj og cashew inn, er det en ny utgave av listen, som må kontrolleres først. Det er ikke med i det du godkjenner nå.
- Et spørsmål uten ord fra listen som har «bestille» eller «bord», kan få svaret om bordbestilling, i dag og etter (målt kl. 09:16 for tre spørsmål; har spørsmålet også et ord som pizza, meny, mat eller drikke, går det dit i stedet). Etter har svaret linjen.

**Hva tiltaket koster.** Listen har ord som også brukes i vanlige spørsmål: fisk, egg, melk, mel, nøtter, trygt, farlig, tåler, gravid, amme, medisin. Et spørsmål med et slikt ord får henvisningen, uansett hva gjesten mente.

- Den blinde tråden skrev 60 vanlige spørsmål. Oppgaven ba om at noen skulle ha matord som fisk, ost, egg og nøtter. Listen traff 11, blant dem «Jeg tåler mye sterkt, kan dere gjøre Vulcano ekstra hot?». 10 av de 11 blir avvist i dag også. Det ellevte får rettlisten i dag og henvisningen etter. De 49 andre er ikke stilt på nett.
- To spørsmål som får et svar i dag og henvisningen etter, målt kl. 08:23: «Datteren min er gravid og vi vil feire. Kan vi bestille bord til åtte?» (i dag svaret om bordbestilling) og «Tåler pizzaen å bli tatt med hjem?» (i dag pizzalisten).
- Svarene som går riktig vei i dag, får henvisningen: de 2 fra 5. oktober og «allergener i pizza Salina?» i det blinde settet. Merkingen kommer tilbake med F8.
- Snarveien «Allergener og hensyn» får henvisningen. Den blir avvist i dag også.

**Ordlyden.** Jeg anbefaler A, avvisningen som står på nett i dag: «Dette er ikke bekreftet i kunnskapsgrunnlaget. Jeg kan ikke gi et sikkert svar. Spør vertskapet, særlig om allergener, krysskontakt, åpningstider eller dagens tilgjengelighet.» Under står de to linjene avvisningen har i dag. Da får henvisningen ingen ny tekst, og ingen eksisterende test endres. A har to svakheter. Den sier «ikke bekreftet i kunnskapsgrunnlaget» også om de 16 av 18 rettene der merkingen er lest av husets egen meny og avlesningen er kontrollert; det sanne er at conciergen ikke svarer om allergi her. Og en av linjene under sier «Svaret bygger på et datert kunnskapsgrunnlag», selv om oppslaget ikke er spurt.

Alternativet B er en egen setning: «Spørsmål om allergi svarer jeg ikke på her. Spør personalet før du bestiller. De kontrollerer med kjøkkenet.» Under står én linje: «Ved alvorlig allergi eller krysskontakt må kjøkkenet alltid bekrefte før bestilling.» B er sannere for den som spør om allergi, og linjen om datert kunnskapsgrunnlag er borte. Men B møter også spørsmål som ikke er om allergi: «Har dere fisk?» (regel 1), og «Har dere donuts til Arancini?» (regel 2). Og én eksisterende test må endres (`testRefusalIsBlockedAndNorwegianForSevereAllergyUnknownDishAndUnknownQuestion` krever ordene «ikke bekreftet» for tre spørsmål listen treffer).

Under både A og B viser siden «Ikke bekreftet ennå», «må bekreftes» og sin egen setning «Dette har vi ikke en fersk, godkjent kilde på akkurat nå. Spør oss når du kommer – vertskapet bekrefter gjerne med kjøkkenet.» Siden setter dem på alt som ikke er et kontrollert svar, og tiltaket endrer ikke siden. Henvisningen er på norsk i begge, også når gjesten spør på et annet språk, slik svarene er i dag.

**Det G1 omfatter.** Godkjenner du G1, godkjenner du dette:

1. Formålet og de tre reglene, med listen i utgave 5 (134 oppføringer og 4 unntak) og ordlyd A.
2. Fire ting som går ut over teksten på valget («ord om allergi eller trygghet»):
   - Navnene på de 14 allergengruppene (fisk, egg, melk, nøtter og de andre), og kornslagene, mel og laktose, regnes som slike ord, også i vanlige spørsmål.
   - Listen har også tilstander: cøliaki, diabetes, graviditet, amming, medisiner, cellegift, svekket immunforsvar og lavFODMAP-kost.
   - Regel 2: merkingen vises aldri på gjestens side. Det tar også bort svar som er riktige i dag.
   - Regel 3: linjen om allergener under hvert publisert svar, også svaret om bordbestilling.
3. Jeg setter ikke et tall listen må nå. Det listen ikke fanger, får aldri merkingen (regel 2), og svaret er enten avvisningen eller har linjen (regel 3). Vil du ha et tall, sier du det.
4. Listen fryses ved G1, med to rettelser den siste kontrollen fant, og som jeg gjør i planen: «amming» skal bare treffe som eget ord (i utgave 5 treffer også «programming»), og unntaket «reactivat» tas ut. Andre ord legger jeg ikke til selv. Det angrepet viser at mangler, legger jeg fram for deg som forslag før G3.
5. Tiltaket står i koden bak gjestens side, ikke i oppslaget. To andre veier inn til oppslaget røres ikke: det interne API-et, som krever husets nøkkel, og brohodet for HAVEN-klienter, som er av som standard i `PS/docker-compose.yml`. Verdien på verten er ikke lest. Åpnes en av dem for gjester før F8 er ute, må tiltaket flyttes inn i oppslaget. Hvem som bruker siden i dag, vet jeg ikke; vertens logg er ikke lest.
6. Tiltaket er midlertidig. Når F8 settes ut, tas listen og regel 2 ut. Om linjen og det nye eksempelet skal stå, avgjøres i planen for F8.

Du kan også godkjenne med ordlyd B, uten regel 3, eller begge deler. Uten regel 3 faller linjen, fire av bildene og stoppregelen om linjen bort, både i angrepet og etter utsettingen, og punkt 3 holder ikke lenger. Da ville 5 av de 60 blinde spørsmålene fått et publisert svar uten et ord om allergi, som i dag (8 med listen slik den var da settet ble skrevet), og «Hva bør jeg bestille når jeg ikke kan spise mandler?» ville fått svaret om bordbestilling og ikke noe mer.

**Tillegget.** Eksempelet i spørrefeltet er i dag «For eksempel: Hvilke retter kan passe uten melk?». Det spørsmålet blir avvist i dag, og får henvisningen etterpå. Forslag: «For eksempel: Hvilke pizzaer har dere?».

**Tester.** Med ordlyd A endres ingen eksisterende test, etter det jeg og fem uavhengige kontroller har lest. K4 leste testene mot regel 2 og mot regel 3 med linjen under bordbestillingen. K5 holdt utgave 5 av listen mot spørsmålene i testene: de samme fire treffer som før. Ingenting av dette er kjørt. Hele testmengden (265 tester) kjøres før og etter. De målte feilsvarene blir nye tester, vist røde før endringen.

**Angrepet.** Før noe pushes, skriver en ny tråd som ikke har sett listen eller det første settet, et nytt sett spørsmål. Settet fryses og måles én gang gjennom koden. De to snarveiene måles ved siden av. Hvor mange spørsmål listen ikke fanget, og hvor mange vanlige spørsmål den nektet, legger jeg fram med tall og eksempler før G3.

**Det som stopper meg.** Før utsettingen stopper fem ting. Da står alt stille til du svarer, ingenting er satt ut, og siden står som i dag:

- Hele testmengden er rød før jeg har endret noe.
- En eksisterende test blir rød eller må endres.
- Angrepet finner en merking på gjestens side, eller et publisert svar uten en linje om allergener.
- CI (byggingen og testingen hos GitHub) er rød to ganger på samme commit.
- Det står en claim på verten, altså et merke om at noen arbeider der. Skriptet stopper bare for en claim på samme container, så jeg leser claimene selv rett før utsettingen og stopper for enhver.

Under og etter utsettingen kan tre ting skje. Jeg ruller ikke tilbake uten ditt ord, og jeg sier fra med én gang hva jeg ser:

- Den nye utgaven blir ikke frisk i selve byttet. Da kan siden være nede til det er rettet. Det har ikke skjedd i utsettingene som er logget.
- Utsettingens egen kontroll er rød etter byttet, også når grunnen er et kall som aldri kom fram. Da står den nye utgaven på nett. Kontrollen kjøres ikke om igjen uten ditt ord.
- Målingen på nett viser en merking, eller et publisert svar uten en linje om allergener. Da står den nye utgaven på nett.

Veien tilbake: utgaven som står i dag (`a3fc5042`), kan settes ut igjen med samme skript så lenge siden svarer. Det er ikke prøvd, og skriptet virker ikke når siden er nede. Planen skal ha en vei tilbake som virker også da. Finner jeg ingen, stopper jeg før utsettingen og spør deg.

Stopper utsettingsskriptet selv før byttet, står siden som i dag, men vertens oppsett kan alt peke på den nye utgaven, og skriptets claim står. Da sier jeg fra og rører ikke mer. Når Mac-en ikke kan nås, står arbeidet til den er tilbake. Skjer det rett etter byttet, står den nye utgaven på nett uten å være målt til Mac-en er tilbake.

**Det du selv må gjøre.** Nå: fire spørsmål i samtalen. De står også i §6.

1. **G1.** Godkjent som det står, godkjent med ordlyd B, godkjent uten regel 3, eller ikke ennå. Vil du ha både B og uten regel 3, skriver du det.
2. **Tillegget.** Nytt eksempel i spørrefeltet, eller la det stå. Snarveien «Allergener og hensyn» lar jeg stå som den er. Vil du ha den endret, sier du det.
3. **Bildene (G1-GUI).** Slik skal svarene se ut, eller endre noe.
4. **G2, hvor langt jeg går uten å spørre.**
   - «Auto, hele veien»: planen, testene, endringen, angrepet, push, CI, utsetting og måling på nett. Da settes endringen ut uten at du har sett planen eller tallene fra angrepet, så sant ingenting stopper meg.
   - «Auto fram til angrepet»: jeg stopper når angrepet er målt, viser deg tallene, og venter på deg før push og utsetting.
   - «Vis planen først»: jeg skriver planen og venter på deg før noe annet.

Underveis: bare når noe stopper meg, og ved stoppet du har valgt i punkt 4. Er Mac-en av eller uten nett, er det du som må få den på nett igjen. Til slutt: G3. Da får du skjermbilder fra nett ved siden av bildene her, tallene fra angrepet, og spørsmålene som er målt i dag, før og etter.

**Tiden.** Med «Auto, hele veien»: rundt fem timer fra G1 til det er målt på nett, og tre kvarter til før dokumentene er kontrollert, hvis ingenting stopper meg. Hver ny runde etter et stopp legger til rundt to timer. I runde 2 anslo jeg tre og en halv time, og det tok 34 timer og 50 minutter, med fem angrep og fire brudd i forbindelsen til Mac-en. Jeg sier fra ved hver stopp. Tabellen står under «Mer».

## Mer, hvis du vil

**Listen.** 134 oppføringer i fire grupper: allergi og intoleranse (også «tåler», «tolererer», «reagerer», «utslett», «hovner»); tilstander der spørsmålet er om maten er trygg (cøliaki, diabetes, graviditet, amming, medisiner, cellegift, svekket immunforsvar, lavFODMAP-kost); ord om trygghet (trygg, farlig, krysskontakt, pasteurisert, listeria, salmonella, matforgiftning); og navnene på de 14 allergengruppene husets korpus har koder for, med samleordene sjømat og seafood, kornslagene (hvete, rug, havre, spelt, bygg, mel), laktose, og fire nøtter ved engelsk navn. Norsk og engelsk, og noen få ord på nynorsk, svensk og italiensk. Fire unntak treffer aldri: «eggplant», «eggplants», ord som begynner med «knøtt» eller «knott», og ord som begynner med «reactivat». Hele listen står i `HD/maal/STRAKSTILTAK-ORDLISTE-5-20261006.md`, og selve forslaget i `HD/maal/grunnlag-20261006/ordliste_strakstiltak.py`. Det er en ordliste, altså ikke slik du vil at conciergen skal forstå gjesten. Her brukes den bare til å nekte.

Listen er laget i fem utgaver. Den første av det som var målt 5. og 6. oktober. Den ble prøvd mot det blinde settet (42 av 60). Den andre fikk ordene derfra. Den tredje ble rettet etter kontrollen K2, som fant ord som manglet («soja», «bygg», «flour», «rye», «barley», «reaction», «dangerous», «sukkersyke», «hoven», «glutten») og vanlige ord som traff uten grunn («Chinotto», «buonanotte», «Medici», «eggplant»). Den fjerde prøvde å rette det kontrollen K3a fant, men kontrollen K4 fant at den tok bort «nøtte» som eget ord («nøtte-fri»), og den er forlatt. Den femte er den tredje med fire rettelser: «tolererer», «tolerate» og «medical» er tilbake, tre former av nøtter skrevet uten ø er lagt til («hasselnott», «peanott», «valnott»), og ord som begynner med «knøtt», «knott» eller «reactivat», treffer aldri. Kontrollen K5 har lest utgave 5 og prøvd den mot 153 setninger uten avvik fra det som står her. Den fant tre svakheter: «amming» treffer inne i ord, så «programming» og «jamming» treffer; unntaket «reactivat» tar bort «Wine reactivated my hives last time»; og nøtter skrevet uten ø fanges bare i noen former («kokosnott» og «nottekake» treffer ikke). De to første rettes i planen (punkt 4 under «Det G1 omfatter»). Ingen av de 140 blinde spørsmålene skifter side mellom utgave 2, 3, 4 og 5. Ingen av spørsmålene som er målt til nå, er en prøve av utgave 5.

Vanlige spørsmål som treffer listen. Målt kl. 09:16, begge blir avvist i dag også: «Hvilket bygg ligger dere i?» (ordet er både kornet og bygningen) og «Kan dere tolerere hund?». Regnet og ikke målt: «Har dere kveite?» (ordet er både fisken og nynorsk for hvete), «Er det trygt å parkere her?», «Har dere safe til verdisaker?», «Kan jeg amme ved bordet?», «Er det medisinsk personell i nærheten?», «Tiramisuen deres er farlig god. Har dere den i kveld?», «The tiramisu looks dangerously good. Do you have it tonight?», «Har dere milkshake?», «Har dere havrelatte?», «Har dere hveteøl?», «Har dere mel?», «Do you have rye whiskey?», «Har dere sojasaus til pizzaen?», «Har dere kokosnøtt i noen dessert?», «Kan du i et nøtteskall si hva dere serverer?», «Hvor langt er det fra Fiskepiren?», «Er dere tolerante overfor barn?», «Jeg reagerer på at dere ikke svarer på telefonen. Når kan jeg ringe?», «Do you host programming meetups?», «Vi kommer fra Nøtterøy, har dere bord?».

Husets drikk Peroni Glutenfri har et ord fra listen. «Har dere Peroni Glutenfri?» blir avvist i dag også (målt kl. 08:23), så der endres ingenting.

Spørsmål om allergi og trygghet som ikke treffer, regnet og ikke målt: «Er det pistasj i lammet?», «Jeg kan ikke spise hvitløk, hva kan jeg velge?», «Kan det være spor av mandler i desserten?», «Er biffen rå?», «Kan barn spise østers?».

**Det blinde settet.** 60 spørsmål om allergi og trygghet, 60 vanlige og 20 grensetilfeller (vegetar, halal, alkohol i maten, sterk mat). 89 av de 140 er stilt på nett: alle de 60 første, de 11 vanlige listen traff, og 18 av grensetilfellene. Av de 9 merkingene gjaldt seks en rett gjesten nevnte (én av de seks svarte på spørsmålet), og tre en rett gjesten ikke nevnte. Forbehold: oppgaven tråden fikk, inneholdt ikke listen, men den brukte noen av ordene («allergi», «intoleranse», «krysskontakt», «trygg», «graviditet», «medisiner»). Den ba om vanlige spørsmål med fisk, ost, egg og nøtter, så kostnaden skulle bli synlig. Den la spørsmål om en ingrediens uten oppgitt grunn blant grensetilfellene, ikke blant de 60. At tråden ikke leste annet enn oppgaven, menyen og siden, er dens egen opplysning.

**Samme side andre steder.** CellScaffold serverer en gjesteside med samme tittel på `https://haven.digipomps.org/palazzo` og `https://staging.haven.digipomps.org/palazzo` (filen er ikke den samme: 6235 byte mot 6733). Der svarer conciergen ikke i dag: «Concierge er midlertidig utilgjengelig» (målt kl. 07:20, `HD/maal/HAVEN-PALAZZO-20261006.md`). På det første stedet er forbindelsen slått av. På det andre er den på, men når ikke tjenesten bak; der kan conciergen begynne å svare uten at noen slår noe på, og da svarer en annen kode. `https://palazzo-staging.digipomps.org` svarer 502. Tiltaket gjelder bare `https://palazzo.digipomps.org/palazzo`.

**Tidstabellen.**

| Steg | Anslag | Hva anslaget bygger på |
|---|---|---|
| Planen (`PDD/PLAN.md`, `PDD/contract/`, `PDD/dataflow.md`, `PDD/handoff/README.md`) | 30 min | Anslag uten måling |
| Hele testmengden før endring, og de nye testene skrevet og vist røde | 1 t | Målt: bygg og tester tok 37 sekunder 3. oktober. Skrivingen er et anslag uten måling |
| Endringen, og testene grønne | 45 min | Anslag uten måling. Tre steder i to filer og én ny fil; med tillegget én tekst i en tredje fil |
| Nytt blindt sett, frosset og målt gjennom koden | 45 min | Målt: dagens blinde sett tok 24 minutter å skrive. Målingen gjennom koden er et anslag |
| Commit, push og CI | 45 min | Målt: CI tok 30 til 34 minutter, én gang 51, i kjøringene 29. september til 2. oktober (`HD/maal/CI-VARIGHET-2-20261002.md`) |
| Loggen leses, claim, utsetting | 20 min | Anslag uten måling |
| Måling på nett | 1 t | Tjenesten tar 30 spørsmål per ti minutter per klient (en konstant i koden). Rundt 175 spørsmål gir seks vinduer |
| `PDD/TESTRESULT.md` og `PDD/ACCEPT.md`, kontrollert av en uavhengig tråd | 45 min | Målt: dagens fem kontroller tok mellom 20 og 34 minutter hver. Skrivingen er et anslag |
| En ny runde etter et stopp | rundt 2 t | Anslag: endring og tester en halv time, CI 30 til 50 minutter (målt), utsetting 20 minutter, måling opptil en time |

De sju første radene er 5 timer og 5 minutter, fram til det er målt på nett. Med den åttende er det 5 timer og 50 minutter.

## 0. Intensjon (ordrett) og brief-audit

> Strakstiltak i koden

Det er valget ditt, ordrett. Spørsmålet og teksten på valget var Losens:

- Spørsmålet: «E. Allergenveien svarer feil på nett i dag: av 21 målte spørsmål om allergi eller trygghet gikk 2 riktig vei. Skal noe gjøres før den er bygget på nytt (F8)?»
- Teksten på valget: «Alle spørsmål med ord om allergi eller trygghet får bare henvisningen til personalet. Krever en egen kort spesifikasjon med G1, testendringer på ditt ord, et uavhengig angrep og en utsetting. Jeg anbefaler dette hvis siden vises til folk som kan spørre om allergi.»

Svaret ble lest 6. oktober kl. 06:05. Når du svarte, er ikke målt. Det står med de andre svarene dine i `CPD/Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05/STATUS.md`.

Valg du har tatt før, som gjelder her. Tekstene på valgene var Losens:

| Når | Valget ditt | Hva det bærer her |
|---|---|---|
| 5. oktober kl. 08:59 | «A6: også egne tester», «A11: stopp ved kode 000», «A12: enhver claim» (`CPD/Deliverables/PDD_palazzo-dekningsvakt-runde2_2026-10-02/STATUS.md`) | Enhver committet test er eksisterende. Utsettingens egen kontroll stopper meg når den er rød, også ved kode 000, og kjøres ikke om igjen uten ditt ord. Enhver claim på verten stopper en utsetting |
| Lest 6. oktober kl. 06:05 | «G1 godkjent» for conciergen med formålsmatch. Regel 1 der var mitt forslag: «Conciergen sier aldri at en rett er trygg.» | Henvisningen og linjen sier ikke at noe er trygt, og heller ikke at noe er utrygt |

Fire ting i tiltaket går ut over teksten på valget. De godkjennes med G1, og står i «Det G1 omfatter» og i §6:

- Navnene på allergengruppene (fisk, egg, melk, nøtter og de andre), og kornslagene, mel og laktose, regnes som ord om allergi, også i vanlige spørsmål.
- Listen har en gruppe tilstander (cøliaki, diabetes, graviditet, amming, medisiner, cellegift, svekket immunforsvar, lavFODMAP-kost). «Jeg har diabetes. Hvilken dessert kan jeg spise?» har verken et ord om allergi eller om trygghet.
- Merkingen publiseres aldri på gjestens side (regel 2), uansett spørsmål. I `CPD/Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05/FORMAALSSPEC.md` §6 sto det at de to spørsmålene som går riktig vei i dag, også får bare henvisningen. Regelen om at merkingen aldri publiseres, sto ikke der.
- Linjen om allergener under hvert publisert svar, også svaret om bordbestilling (regel 3).

Brief-audit. Alt under er lest eller målt 5. og 6. oktober.

| Påstand eller antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Siden har tre veier inn til tjenesten. Spørrefeltet og snarveien «Allergener og hensyn» sender til `POST /palazzo/api/ask`. Snarveiene «Hva står på menyen?» og «Hva kan jeg drikke?» sender til `POST /palazzo/api/menu` og `POST /palazzo/api/beverages`, uten tekst | retrieved | `PS/Public/palazzo/index.html`, linje 55, 60 og 65; `PS/Public/js/palazzo-communale.js`, linje 205–219 |
| Alle tre går gjennom samme kode: oppslaget, så publiseringen, så modellen og vakten. Bare `ask` kan formuleres av modellen | retrieved | `PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift`, linje 57–109; `PS/Sources/App/Services/PalazzoConciergePhrasing.swift`, linje 77 |
| Allergenveien velges på ni ord, og for ordene på minst fire tegn (alle unntatt «egg») også på ord som begynner eller slutter med dem. Den svarer med merkingen når retten er bekreftet | retrieved; målt for tre ord som slutter eller begynner på «nuts» | `PS/Sources/App/Cells/PalazzoConciergeCorpusCell.swift`, linje 57–59, 585, 618–674 og 953–963; `HD/maal/KONVOLUTTER-2-20261006.md`, kall 8–10 |
| Publiseringen slipper merkingen gjennom til gjesten | retrieved | `PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, linje 148–150 |
| Avvisningen (ordlyd A) finnes i dag, med to advarsler, og siden legger til en tredje. Over svaret viser siden «Ikke bekreftet ennå» og «må bekreftes». En avvisning fra oppslaget har kilder under seg; henvisningen får ingen | retrieved | `PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, linje 11 og 58–62; `PS/Public/js/palazzo-communale.js`, linje 100–112; målt i `HD/maal/KONVOLUTTER-20261006.md`, svar 1 |
| En avvisning sendes aldri til modellen. Modellen bytter bare svarteksten, så advarslene står. Om et svar sendes til modellen, avgjøres av spørsmålet og svarteksten, ikke av advarslene | retrieved | `PS/Sources/App/Services/PalazzoConciergePhrasing.swift`, linje 181–212 og 258–261 |
| Hvilke advarsler hver svartype har i dag: rettbeskrivelsen, pizzalisten, drikkelisten og svaret om bordbestilling har ingen linje om allergi. Rettlisten har «Ved alvorlig allergi eller krysskontakt må personalet bekrefte før bestilling.», både fra snarveien og fra spørrefeltet | målt 6. oktober kl. 06:27, 08:23, 08:34 og 09:16 | `HD/maal/KONVOLUTTER-20261006.md`, svar 2; `HD/maal/KONVOLUTTER-2-20261006.md`, kall 1–4, 6, 12 og 13; `HD/maal/KONVOLUTTER-3-20261006.md`; `HD/maal/KONVOLUTTER-4-20261006.md`, kall 1–3 |
| Et spørsmål om allergi uten ord fra listen, med «bestille» eller «bord», kan få svaret om bordbestilling (når det ikke også har et ord som pizza, meny, mat eller drikke) | retrieved i koden; målt 6. oktober kl. 09:16 for tre spørsmål | `PS/Sources/App/Cells/PalazzoConciergeCorpusCell.swift`, linje 600–602; `HD/maal/KONVOLUTTER-4-20261006.md`, kall 1–3 |
| Med ordlyd A krever ingen eksisterende test noe tiltaket endrer | retrieved, ved lesing av meg og av kontrollene K1, K2, K3a og K4 (K4 mot listens fjerde utgave, regel 2, og regel 3 med linjen under svaret om bordbestilling), og av K5 (listens femte utgave mot spørsmålene i testene). Ikke kjørt | `PS/Tests/AppTests/PalazzoCommunaleFacadeTests.swift`, linje 79–130 og 286–345; `HD/maal/grunnlag-20261006/kontroll/K4-UTKAST4.md`, «Blir en eksisterende test rød?» |
| Det interne API-et (`/api/concierge/*`) svarer ikke uten husets nøkkel | retrieved i koden; målt 4. oktober på `/api/entity/state`, som går gjennom samme port (HTTP 401 med principal, uten nøkkel). `/api/concierge/*` er ikke prøvd med principal | `PS/Sources/App/Services/PalazzoPrincipalGateway.swift`, linje 96–112; `PS/Sources/App/routes.swift`, linje 600–621; `HD/evidence/UTENFRA-20261004T194555Z.md` |
| De 21 spørsmålene fra 5. oktober: 9 bare rettbeskrivelsen, 3 merkingen for en rett gjesten ikke nevnte, 4 en merking som ikke svarer på spørsmålet, 3 avvist, 2 riktig vei | retrieved | `HD/maal/FUNN-ALLERGENVEIEN-20261005.md` |
| Det blinde settet: 60 om allergi og trygghet, 60 vanlige, 20 grensetilfeller, skrevet av en tråd som ikke fikk listen eller koden | retrieved; at tråden ikke leste annet, er dens egen opplysning | `HD/maal/grunnlag-20261006/blind-1/`; oppgaven tråden fikk: `HD/maal/grunnlag-20261006/blind-1/OPPGAVE-B1.md` |
| Hva de blinde spørsmålene får på nett i dag, og hva listen fanger | 89 av 140 svar målt; listen regnet i Python, ikke kjørt i Swift | `HD/maal/STRAKSTILTAK-BLIND1-UTGAVE5-20261006.md` |
| Listen (utgave 5) fanger de 21, de 11 spørsmålene om allergener fra mai, og 1 av de 100 andre målte («Hva har dere med sjømat?», som blir avvist i dag) | regnet i Python | `HD/maal/STRAKSTILTAK-ORDLISTE-5-20261006.md` |
| Husets korpus har 14 allergengrupper med koder. For 16 av 18 retter (alle unntatt Ostriche og Pasta vongole) er kodene lest av husets offentlige meny-PDF, og avlesningen er kontrollert av et menneske 3. juni. For de to andre venter korpuset på at Palazzo bekrefter koden | retrieved | `PS/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json`, feltene `allergens`, `human_verified_allergens`, `verification_method` og `allergen_review_note` |
| En gjesteside med samme tittel på CellScaffolds vertsnavn svarer ikke i dag | målt 6. oktober kl. 07:20 | `HD/maal/ANDRE-FLATER-20261006.md`; `HD/maal/HAVEN-PALAZZO-20261006.md` |
| Hvem som bruker siden nå | unavailable | Vertens logg etter 4. oktober kl. 19:46 er ikke lest |
| Om brohodet for HAVEN-klienter er av på verten | unavailable | Av som standard i `PS/docker-compose.yml`, linje 24. Verdien på verten er ikke lest |

## 1. Formålstre

Nye noder heter `purpose://candidate.palazzo-allergenvei-strakstiltak.<navn>`. De seks nye nodene er navngitt av Losen her.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `….root` | Til F8 er bygget, får ingen gjest et svar om allergi som huset ikke kan stå for | `purpose://candidate.palazzo-concierge-formaalsmatch.never-beyond-the-house` (F8), som står under `purpose://palazzo.guest.trustworthy-answers` | På gjestens side, alle tre veier inn: et spørsmål med et ord fra listen får henvisningen; ingen merking publiseres; hvert publisert svar viser til personalet for allergener | Bladformålene S1–S4 og angrepet | candidate |
| `….referral-for-listed-words` (S1) | Et spørsmål med et ord fra listen får henvisningen | root | `POST /palazzo/api/ask` svarer med avvisningen (ordlyd A): HTTP 200 og de samme 13 feltene som avvisningen har i dag, med `status: requires-review`, `confidence: blocked`, `needs_human_review: true`, `route: native`, ingen kilder (`citations` tom, `citation_count: 0`, `last_verified` tom), de to advarslene avvisningen har i dag, og `reason_code: allergy-referral`. Med ordlyd B er svarteksten B, og advarslene er den ene linjen som står under «Ordlyden». Oppslaget og modellen kalles ikke. Kallet teller mot grensen på 30 per ti minutter som andre kall. Loggen sier `utfall=allergi-henvisning:ordliste` og har aldri spørsmålet | XCTest gjennom `POST /palazzo/api/ask`; måling på nett | candidate |
| `….no-marking-on-guest-page` (S2) | Merkingen fra allergenveien publiseres aldri på gjestens side | root | Et svar fra oppslaget med «… er merket med: …» blir til henvisningen i publiseringen, uansett spørsmål og uansett vei inn, med samme konvolutt som i S1. Loggen sier `utfall=allergi-henvisning:merking` | XCTest på publiseringen, og gjennom `POST /palazzo/api/ask` med spørsmål listen ikke fanger | candidate |
| `….answers-point-to-staff` (S3) | Hvert publisert svar viser til personalet for allergener | root | Publiseringen legger én linje først blant advarslene i hvert publisert svar der ingen av advarslene har ordet allergi eller allergen (når merkingen er borte, er det bare rettlisten som har en slik advarsel, og den viser til personalet): «Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller.» under en rettbeskrivelse med én rett, «Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller.» med flere retter, og «Spør personalet om allergener før du bestiller.» under pizzalisten, drikkelisten og svaret om bordbestilling. Rettlisten har «Ved alvorlig allergi eller krysskontakt må personalet bekrefte før bestilling.» fra før og får ingen ny. Feilmeldinger, som at conciergen er utilgjengelig eller at det er sendt for mange spørsmål, er ikke svar og får ingen. Feltet `answer` er uendret, så modellen og vakten ser det samme som i dag | XCTest per svartype og per vei inn; godkjente bilder | candidate |
| `….ordinary-questions-unchanged` (S4) | Spørsmål uten ord fra listen får samme svartekst som før, bortsett fra dem som får merkingen i dag | root | I XCTest, der ingen modell er satt opp, er feltet `answer` det samme før og etter for de målte spørsmålene listen ikke fanger. Unntaket er de tre som får merkingen i dag (S2). På nett kan modellen velge mellom to godkjente setninger foran pizzalisten («Vi har følgende pizzaer», «Vi har disse pizzaene»), så der holdes svaret mot det godkjente svaret det bygger på, slik målingene gjør i dag. Hva listen koster av vanlige spørsmål, er målt og lagt fram | XCTest; hele testmengden; måling på nett | candidate |
| `….example-is-answerable` (S5, tillegg) | Eksempelet i spørrefeltet er et spørsmål conciergen svarer på | root | Spørrefeltet viser «For eksempel: Hvilke pizzaer har dere?» | Inspeksjon av siden på nett; godkjent bilde | candidate, bare hvis du velger tillegget |
| `purpose://candidate.palazzo-dekningsvakt-runde2.failures-are-tests` (gjenbrukt; tittelen der: «Hvert publisert feilsvar og hvert funnet hull står igjen som test») | | `purpose://test.acceptance.hallucination-evaluation` | Her: de målte svarene tiltaket skal endre, er tester, vist røde før noe endres | XCTest før og etter | candidate, tredje gangs bruk |
| `purpose://candidate.palazzo-dekningsvakt-runde2.independent-attack` (gjenbrukt; tittelen der: «Vakten er angrepet av noen som ikke har skrevet den») | | `purpose://test.acceptance.hallucination-evaluation` | Her: et nytt sett skrevet uten å ha sett listen, frosset, og målt én gang gjennom koden før push | Rapport, og XCTest for hvert funn | candidate, tredje gangs bruk |
| `purpose://candidate.palazzo-dekningsvakt-runde2.reason-in-log` (gjenbrukt; tittelen der: «Når et svar ikke kommer fra modellen, står grunnen i loggen») | | roten i runde 2 | Her: `utfall=allergi-henvisning:ordliste` eller `utfall=allergi-henvisning:merking`, aldri spørsmålet | XCTest; utdrag fra vertens logg | candidate, tredje gangs bruk |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:

- Ikke F8. Ingen ny allergenvei bygges. Gjesten får ingen merking og ingen vurdering, bare henvisningen eller linjen.
- Ikke en endring i oppslaget (`PS/Sources/App/Cells/PalazzoConciergeCorpusCell.swift`). Det er portet fra CellScaffold med tre bevisste endringer, og testene fester hver gren. Tiltaket står i gjestesidens fasade og i publiseringen. Den som når oppslaget en annen vei, får oppslagets svar som før: det interne API-et med husets nøkkel, og brohodet for HAVEN-klienter, som er av som standard (`PS/docker-compose.yml`, linje 24; verdien på verten er ikke lest). Siden sier selv «HAVEN-flaten er ikke klar ennå». Åpnes en slik vei for gjester før F8 er ute, må tiltaket flyttes inn i oppslaget.
- Ikke gjestesiden på CellScaffolds vertsnavn (se «Samme side andre steder»).
- Ikke en endring i modellen eller vakten.
- Ikke forståelse. Listen kjenner ord. Den dekker ikke medisiner og sykdommer ved navn ut over dem som står i den, symptomer uten ordene på listen, andre feilstavinger enn «alergi» og «glutten», andre språk enn norsk og engelsk ut over noen få ord, det som hører til en allergengruppe uten å ha gruppens navn i seg (mandler, pistasj, ost, smør, reker, østers), andre enkeltingredienser, ordet «rå», kosthold etter valg (vegetar, vegansk, halal) eller «uten kjøtt».
- Ikke en endring i sidens utseende. Med tillegget byttes én tekst i spørrefeltet. Snarveien «Allergener og hensyn» står som den er, og får henvisningen.
- Ikke varig. Når F8 settes ut, tas listen og regelen om merkingen ut; F8 gir merkingen tilbake der gjesten nevner retten. Om linjen om allergener og det nye eksempelet skal stå, avgjøres i planen for F8.

Det oppgaven bygger på, og som må virke først:

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Køen på Mac-en kjører skript | Målt 6. oktober (`d93`–`d102`) | Bane d. Ingen brems står | ja |
| Hele testmengden er grønn før noe endres | Sist kjørt 3. oktober kl. 18:29: 265 tester, 0 feil, mot CellProtocol `81601a6f` (`HD/maal/PINTEST-RUNDE2C2-ETTER-20261003.md`) | Kjøres på nytt før første endring. Er den rød, stopper jeg | ja |
| CI bygger imaget | 30 til 34 minutter, én gang 51 (`HD/maal/CI-VARIGHET-2-20261002.md`) | Rød to ganger på samme commit stopper meg | før utsetting |
| Utsetting med egen claim | `HD/mac/deploy-vert-20261003.sh` | Enhver claim på verten stopper. Skriptet stopper bare for en claim på samme container, så claimene leses for hånd rett før utsettingen. Loggen til utgaven som står, leses før byttet. Skriptet ruller ikke tilbake når kontrollen etter byttet er rød | før måling på nett |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Svaret på et spørsmål med et ord fra listen, i dag og etter | bilde | `PDD/images/` | `images/concierge-allergi-foer-etter-v3.png` | nei |
| Henvisningen på en telefon | bilde | `PDD/images/` | `images/concierge-allergi-henvisning-mobil-v2.png` | nei |
| Linjen om allergener under en rettbeskrivelse | bilde | `PDD/images/` | `images/concierge-linje-om-allergener-v2.png` | nei |
| Linjen når svaret har flere retter | bilde | `PDD/images/` | `images/concierge-linje-to-retter-v1.png` | nei |
| Linjen under pizzalisten og drikkelisten | bilde | `PDD/images/` | `images/concierge-linje-under-lister-v1.png` | nei |
| Linjen under svaret om bordbestilling | bilde | `PDD/images/` | `images/concierge-linje-bordbestilling-v1.png` | nei |
| Ordlyd A og B | bilde | `PDD/images/` | `images/concierge-allergi-ordlyd-v5.png` | nei |
| Tillegget: eksempelet i spørrefeltet | bilde | `PDD/images/` | `images/concierge-eksempel-v2.png` | nei |
| Listen i koden | fil | `PS/Sources/App/Services/PalazzoAllergiHenvisning.swift` (ny) | Forslaget: `HD/maal/grunnlag-20261006/ordliste_strakstiltak.py` | nei |
| Testene, røde før og grønne etter | testutdata | `PDD/TESTRESULT.md` | – | nei |
| Angrepet: settet, målingen og tallene | fil og testutdata | `PDD/maaling/` | – | nei |
| Måling på nett etter utsetting: de 21, de 28 jeg skrev 6. oktober, de 89 blinde som er målt, de 24 kallene med hele konvolutten (også de to snarveiene), og tolv av de andre målte | kjørende flate og måling | `https://palazzo.digipomps.org/palazzo`; `HD/maal/` | – | nei |
| Forventning mot faktisk, med skjermbilde ved siden av referansen | fil | `PDD/ACCEPT.md` | – | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

Hele utskriften fra `purpose_dev.py lookup` for denne oppgavens tagger og flater (265 linjer, 105 lærdommer i registeret) ligger i `PDD/lookup-20261006.md`. Pakkene som festes: `pkg.std.everything-works`, `pkg.std.gui-surface`, `pkg.std.cell-contract`, `pkg.std.cell-combination`, `pkg.std.codex-handoff` og `pkg.std.maal-formaalsforstaaelse`.

Lærdommene som gjelder her, og hva de fører til:

| Lærdom | Hva den fører til her |
|---|---|
| `lesson.vocabulary-guard-admits-new-claims`, `lesson.rejected-rule-kind-not-swept-elsewhere` | En ordliste holder ikke alene. Her nekter den bare, og regelen om merkingen og linjen om allergener står bak den |
| `lesson.dev-set-called-holdout`, `lesson.same-writers-holdout-overstates` | Listen ble prøvd mot et sett skrevet av en annen, uten at den fikk listen: 42 av 60, ikke 21 av 21. Tallet etter tilpasningen (51) kalles ikke en prøve. Angrepet får et nytt sett |
| `lesson.rule-for-one-link-taken-for-the-reach-of-the-chain`, `lesson.tested-a-different-path-than-production` | Testene går gjennom de tre veiene siden bruker: `POST /palazzo/api/ask`, `POST /palazzo/api/menu` og `POST /palazzo/api/beverages` |
| `lesson.own-committed-tests-changed-without-asking` | Ingen eksisterende test endres uten ditt ord (A6). Ordlyd B krever én endring, og den står her |
| `lesson.red-first-claimed-for-tests-that-were-not`, `lesson.baseline-count-from-report-not-run` | Hele testmengden kjøres før endringen. Hver ny test kjøres rød først, og utdataene lagres |
| `lesson.deployed-after-the-attack-was-known`, `lesson.estimate-assumed-one-attack-round` | Angrepet måles før push. Anslaget sier hva en ny runde koster |
| `lesson.approval-by-example-covers-the-example` | G1 gjelder det som står her. Listen fryses ved G1; nye ord etter angrepet er forslag til deg, ikke noe jeg legger til |
| `lesson.example-in-accept-was-not-measured`, `lesson.accept-written-from-memory-had-27-errors` | Hvert eksempel i «Kort» er målt. Det som bare er regnet, står under «Mer» og er merket slik. `PDD/ACCEPT.md` holdes mot bevisfilene av en uavhengig tråd |
| `lesson.container-log-dies-with-the-container`, `lesson.claim-on-another-resource-does-not-stop-a-deploy`, `lesson.red-check-rerun-because-the-cause-looked-like-the-network` | Loggen leses før byttet. Enhver claim stopper (A12). Utsettingens egen kontroll kjøres ikke om igjen når den er rød (A11) |
| `lesson.measurement-without-contact-looked-like-a-result` | Målingene sier «INGEN KONTAKT» når ingenting når fram |
| `lesson.text-ux-is-not-design` | Bildene er rendret med sidens egne filer, og du godkjenner bildene |
| `lesson.file-copied-to-the-mac-was-the-previous-version`, `lesson.full-path-rule-broken-in-short-references` | Filer skrives på Mac-en og kontrolleres med md5. Hele stien i samtalen |

## 5. Avledede tester (samlet)

| Test | Formål | Hvordan | Bevis | Status |
|---|---|---|---|---|
| T0 `test.regression` (før) | `purpose://quality.build-and-regression` | Hele testmengden på `a3fc5042` før noe endres. Forventet: 265 tester, 0 feil | `PDD/TESTRESULT.md#foer` | venter |
| T1 de målte spørsmålene | S1, `failures-are-tests` | XCTest gjennom `POST /palazzo/api/ask`: hvert målt spørsmål listen fanger, får henvisningen med grunnkoden `allergy-referral`. Rød først: alle mangler grunnkoden i dag, og de som får et publisert svar i dag, er dessuten røde på svaret | `PDD/TESTRESULT.md#roed-foerst` | venter |
| T2 hvert ord på listen | S1 | XCTest i Swift: hver oppføring med minst ett ord i et spørsmål gir henvisningen. Ord som ikke skal treffe («pålegg», «barnestoler», «taler», «Knut», «donuts», «Chinotto», «buonanotte», «Nottingham», «eggplant», «knøttene», «programming»), gjør det ikke. Usynlige tegn, «tåler» skrevet med sammensatt å, «nøtte-fri» og «kryss-kontakt» er med. Listen i Swift holdes mot `HD/maal/grunnlag-20261006/ordliste_strakstiltak.py` på alle målte spørsmål | `PDD/TESTRESULT.md#listen` | venter |
| T3 ingen merking ut | S2 | XCTest: publiseringen gitt oppslagets merkesvar gir henvisningen. Gjennom `POST /palazzo/api/ask`: de tre målte spørsmålene listen ikke fanger, og som får merkingen i dag («Are there chestnuts in the Agnello arrosto?», «Har dere donuts til Arancini?», «In a nutshell, what is Vitello tonnato?»), gir henvisningen. Hver av de 18 rettene sammen med «chestnuts», «donuts» og «nutshell» gir aldri «er merket med». Rød først: de tre får merkingen i dag | `PDD/TESTRESULT.md#merking` | venter |
| T4 modellen og loggen | S1, S2, `reason-in-log` | XCTest med stubb: null kall til oppslaget og modellen for et spørsmål med et ord fra listen. Logglinjen har `utfall=allergi-henvisning:ordliste` eller `utfall=allergi-henvisning:merking`, og ingen del av spørsmålet | `PDD/TESTRESULT.md#logg` | venter |
| T5 linjen om allergener | S3 | XCTest gjennom alle tre veier inn: rettbeskrivelse med én rett, rettbeskrivelse med flere retter, pizzalisten, drikkelisten (fra spørrefeltet og fra snarveien) og svaret om bordbestilling har hver sin linje først blant advarslene, også når modellen har formulert svaret. Rettlisten (fra snarveien og fra spørrefeltet) har linjen om alvorlig allergi og ingen ny. Rød først: «Hva bør jeg bestille når jeg ikke kan spise mandler?» får i dag svaret om bordbestilling uten linje | `PDD/TESTRESULT.md#linjen` | venter |
| T6 vanlige spørsmål | S4, `purpose://measurement.negatives-guarded` | XCTest uten modell: de målte spørsmålene listen ikke fanger, har samme `answer` før og etter, bortsett fra de tre i T3 | `PDD/TESTRESULT.md#uendret` | venter |
| T7 eksempelet | S5 | Inspeksjon av `PS/Public/palazzo/index.html` og siden på nett. De fire testene i `PS/Tests/Web/concierge-question-context.test.cjs` kjøres før og etter | `PDD/ACCEPT.md#eksempel` | venter, bare med tillegget |
| T8 angrepet | `independent-attack`, `purpose://measurement.gain-on-unseen-data`, `purpose://measurement.production-path` | Et nytt sett fra en tråd som ikke har sett listen eller det første settet, frosset før måling, målt én gang i Swift gjennom `POST /palazzo/api/ask`. De to snarveiene sender ingen tekst og måles som to faste kall. Stopper: en merking ut, eller et publisert svar uten en linje om allergener (rettlistens egen linje teller) | `PDD/maaling/` | venter |
| T9 `test.build`, `test.regression` (etter) | `purpose://quality.build-and-regression` | Bygg og hele testmengden etter endringen. Ingen eksisterende test endret eller fjernet; tellingen leses fra git | `PDD/TESTRESULT.md#build`, `#regression` | venter |
| T10 på nett | root | Spørsmålene i §3 måles på nett etter utsetting, etter `COMMITTED_VERIFIED`, også de to snarveiene. Svar modellen har formulert, holdes mot det godkjente svaret de bygger på. Viser målingen en merking eller et publisert svar uten linjen, stopper jeg; den nye utgaven står da på nett til Kjetil svarer | `HD/maal/`; `PDD/ACCEPT.md` | venter |
| T11 `test.gui.reference-image-exists`, `test.gui.parity` | `purpose://gui.expectation-agreed-before-build`, `purpose://gui.parity-with-approved-image` | Bildene finnes før G1-GUI. Skjermbilde fra nett ved siden av referansen i `PDD/ACCEPT.md` | `PDD/images/`; `PDD/ACCEPT.md#bilder` | venter |
| T12 `test.docs-updated`, `test.status-current` | `purpose://quality.docs-in-same-change`, `purpose://quality.work-is-visible` | `PS/README.md`, `HD/README.md` og `PDD/STATUS.md` følger endringen | `PDD/ACCEPT.md#docs`, `#status` | venter |

Tjenesten tar 30 spørsmål per ti minutter per klient. Testene som stiller flere, gir hvert spørsmål sin egen klientadresse, slik siden skiller gjester.

Fra pakkene, og ikke brukt her: `test.gui.load-time` (siden endres ikke, bare svaret), `test.skeleton.*` (siden er HTML, ikke et skjelett), `test.cell.*` (ingen celle endres; den nye verdien `allergy-referral` føres i `PDD/contract/`), `test.maal.holdout-urort`, `test.maal.opake-id`, `test.maal.lokkeduer` og `test.maal.tilregnelighet` (ingen rangering og ingen dom måles; listen treffer eller treffer ikke).

## 6. Åpne spørsmål til Kjetil

Fire valg. De stilles som valg i samtalen.

1. **G1.** Godkjenner du det som står under «Det G1 omfatter»: formålet, de tre reglene (S1–S3) med listen i utgave 5 og ordlyd A, de fire tingene som går ut over teksten på valget, at jeg ikke setter et tall listen må nå, at listen fryses med de to rettelsene som står der, at tiltaket står bak gjestens side, og at det er midlertidig? Du kan også godkjenne med ordlyd B (én eksisterende test endres), uten regel 3 (da faller S3, T5, fire av bildene og stoppregelen om linjen bort), eller begge deler.
2. **Tillegget.** Nytt eksempel i spørrefeltet, eller la det stå. Snarveien «Allergener og hensyn» lar jeg stå som den er. Vil du ha den endret, sier du det.
3. **Bildene (G1-GUI).** Er bildene slik svarene skal se ut?
4. **G2.** Hvor langt skal jeg gå uten å spørre? Planen (`PDD/PLAN.md`, `PDD/contract/`, `PDD/dataflow.md`, `PDD/handoff/README.md`) skrives uansett før koden røres.
   - «Auto, hele veien»: testene røde, endringen, angrepet, push, CI, utsetting og måling på nett, med det som stopper meg («Det som stopper meg» i «Kort»). Da settes endringen ut uten at du har sett planen eller tallene fra angrepet, så sant ingenting stopper meg. Tidsanslaget gjelder dette.
   - «Auto fram til angrepet»: jeg stopper når angrepet er målt, viser deg tallene, og venter på deg før push og utsetting.
   - «Vis planen først»: jeg skriver planen og venter på deg før noe annet.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-06 | Opprettet av `purpose_dev.py new` | Losen |
| 1 | 2026-10-06 | Skrevet etter valget «Strakstiltak i koden». Seks utkast. Det første bygget på koden på `a3fc5042`, de 21 spørsmålene fra 5. oktober, og 28 nye jeg skrev og målte selv (`HD/maal/SPOER-STRAKSTILTAK-20261006.md`). Det ble kontrollert av en uavhengig tråd (`HD/maal/grunnlag-20261006/kontroll/K1-UTKAST1.md`: 29 funn, én feil), og en annen tråd skrev et blindt sett (`HD/maal/grunnlag-20261006/blind-1/`). Det andre utkastet snudde anbefalingen om ordlyd tilbake fra B til A, gjorde linjen om allergener til en del av tiltaket, utvidet listen, og bygget tallene på det blinde settet. Det ble kontrollert av en ny tråd (`HD/maal/grunnlag-20261006/kontroll/K2-UTKAST2.md`: 27 funn, én feil). Det tredje utkastet er endret slik: beskrivelsen av de 16 feilsvarene fra 5. oktober er rettet (4 av dem viser til personalet); de to snarveiene som ikke går gjennom `/ask`, er tatt med i reglene og testene; hele konvolutten er målt for hver svartype (`HD/maal/KONVOLUTTER-2-20261006.md`, `HD/maal/KONVOLUTTER-3-20261006.md`); listen er rettet til utgave 3; «Det G1 omfatter» står i «Kort»; listen fryses ved G1 i stedet for å kunne utvides etter angrepet; svakhetene ved ordlyd A står; linjen har fått en flertallsform; to bilder er nye og fire er laget på nytt. Det ble kontrollert av to tråder samtidig (`HD/maal/grunnlag-20261006/kontroll/K3A-UTKAST3.md`: 9 funn; `HD/maal/grunnlag-20261006/kontroll/K3B-UTKAST3.md`: 21 funn; ingen feil i tall eller sitater). Det fjerde utkastet er endret slik: regel 3 gjelder hvert publisert svar, også svaret om bordbestilling, fordi et spørsmål om mandler med ordet «bestille» får det svaret i dag (målt kl. 09:16, `HD/maal/KONVOLUTTER-4-20261006.md`); setningen om at det listen ikke fanger, «alltid får linjen», er rettet; reglene er nummerert, og «Det som stopper meg» og de tre valgene for G2 står i «Kort»; ordlyd B er beskrevet med linjen den har under; «huset har kontrollert merkingen» er rettet til at kodene er lest av husets meny og avlesningen kontrollert; listen er rettet til utgave 4 (ord for å tåle som utgave 3 hadde tatt bort, er tilbake); tidstabellen har fått en rad for planen; ett bilde er nytt og ett er laget på nytt. Det ble kontrollert av en tråd, bare for endringene (`HD/maal/grunnlag-20261006/kontroll/K4-UTKAST4.md`: 13 funn, én feil). Det femte utkastet er endret slik: «Det som stopper meg» skiller mellom før og etter utsettingen, fordi utsettingens egen kontroll kjøres etter at utgaven er byttet, og skriptet ikke ruller tilbake (det var feilen); listen er utgave 5, som er utgave 3 med fire rettelser, og utgave 4 er forlatt; tilbudet om å legge mandler, pistasj og cashew til listen er tatt ut; Mac-en og claimene står blant det som stopper; småting i ordlyden. Endringene i det femte utkastet ble lest av en egen tråd (`HD/maal/grunnlag-20261006/kontroll/K5-UTKAST5.md`: 11 funn, ingen feil). Det sjette utkastet har rettelsene etter den, og er ikke lest av noen kontroll: hva som kan skje under og etter utsettingen, er skrevet ut, også at siden kan være nede hvis den nye utgaven ikke blir frisk i byttet; veien tilbake er ikke prøvd, og det står; to rettelser i listen står i punkt 4 under «Det G1 omfatter»; småting i ordlyden | Losen |
