# Kryptert korrespondanse med vedlegg, ut til Vegar og Victoria — det du trenger for å ta stilling (G1)

Dette er et utdrag av `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/FORMAALSSPEC.md`, iterasjon 2. Det har ingenting som ikke står der. Det er den fulle spesifikasjonen du godkjenner eller avviser; her står bare det du må lese for å gjøre det. Henvisninger som «A7 i §0», «§2» og «§3b» peker dit. Skrevet 06.10.2026 av Claude-tråden i prosjektet «HavenAgentD» («korrespondanse-tråden»).

## 1. Kort sagt

- Det Vegar og Victoria har i dag, er den gamle kanalen. Der ser tjeneren meldingene i klartekst, og vedlegg finnes ikke.
- Dette finnes for den nye, krypterte korrespondansen: cellen som lagrer meldingene (i CellProtocol, i revisjonen staging kjører), en klient for den parten som blir invitert (på `main` i HavenAgentD), og vedlegg (skrevet og testet lokalt, ikke gjennomgått, ikke på `main`).
- Dette mangler:
  1. **To agenter kan ikke skrive til hverandre i én celle slik koden står.** Koden regner med at den ene parten eier cellen. Eieren er mottaker av alt, har ingen vei til klienten utenom testene, og kan ikke sende vedlegg. Se A7–A10 i §0.
  2. Staging kan ikke huse de nye cellene, og kan ikke melde noen inn i dem.
  3. Broen meldingene skal gå over, er merget i CellProtocol, men ikke utgitt, og ruta mangler i CellScaffold.
  4. Ingen pakke med den nye klienten er bygget.
- Punkt 1 betyr at «tjenerdelen» er mer enn å sette cellen på staging. Reglene for hvem som er med i en celle, må gjøres ferdige først. Det er valg 1 under, og det avgjør hvor du godkjenner og hvor lang tid dette tar.
- Første pakke har ikke dette, slik forslaget står: varsel ved ny post, som du har bedt om to ganger (S2 under); vedlegg som referanse eller hent ved behov, bare som kopi (S1 under); og delegering (valg 3). Si fra hvis noe av det må inn.
- Tid: leddene korrespondanse-tråden har, er fem til ni uker når de tas etter hverandre, og tre til fem hvis Codex tar en del samtidig. Bro-leddene har jeg ikke tall for. Ingen dato er lovet (§3b).
- Dokumentet sier hva som skal være sant når Vegar og Victoria bruker det, og hva som teller som bevis for det. Det er ikke en plan. Planen kommer etter at du har godkjent formålene (G1) og bildene (G1-GUI).

Figuren `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/figur/leddene-v2.svg` viser leddene, hvor hvert av dem står i dag, og hvor ordet ditt trengs.

## 2. De fem valgene

Fem valg. Hvert av dem endrer treet eller tiden. Anbefalingen min står først i hvert. Under valgene står ti standardvalg jeg har tatt. To av dem, S1 og S2, gjelder noe du har sagt eller bedt om før; les dem. Resten trenger du bare å lese hvis du vil ha noe annerledes.

**1. Hvem slipper inn medlemmer i en relasjonscelle?**

Hver celle har én eier, og bare eieren kan gi en identitet en avtale. I koden i dag er eieren selv den ene parten og mottaker av alt (A7–A10 i §0). For at agenten din og Vegars agent skal kunne skrive til hverandre, begge veier og med vedlegg, må de begge være inviterte. Da må noen andre enn de to være eier, og eieren må ikke være mottaker.

- **1a) Tjeneren eier cellen, men er ikke mottaker (anbefalt).** Begge parter er inviterte og bruker samme klient. Du godkjenner på adminsiden, bak innloggingen din, som i dag, og tjeneren signerer avtalene når du har trykket.
  - Må bygges i CellProtocol og klienten: regelen om at eieren alltid er mottaker, må bort. Nøklene til begge medlemmene må stå i det tjeneren signerer. Vedleggsreglene følger etter. Klienten må godta en eier som ikke er medlem. Cellen må lukkes når medlemslista endres (Book 33 §11); det finnes ikke i dag.
  - Må bygges på tjeneren: innmeldingen. Koden krever at den som får en avtale, beviser nøkkelen sin i samme kall som eieren signerer. Hvordan det gjøres mot en klient som er koblet til over broen, har jeg ikke sett løst noe sted. Innmeldingen må også gi klienten begge medlemmene og den nye avtalen.
  - Hva som hindrer at en nøkkel til kommer stille inn: klientene krypterer bare til nøklene som står i den signerte avtalen de har, og cellen krever nøyaktig de mottakerne. Lukkingen må også gjelde i klienten: den skal nekte å ta imot en ny medlemsliste for en relasjon den alt har. Da gir en nøkkel til en ny relasjon som begge parter ser. Dette holder mot en tjener som følger koden; en drift som jukser med vilje, er utenfor det som prøves (§2).
  - Pris: tjeneren avgjør hvem som er med. Book 33 §3.4 sier at driften bare skal styre livsløp, så den setningen må endres, og det er din avgjørelse. Planen fra 09.09 (§3.3) beskriver denne måten. S6-dokumentet beskriver tjeneren som vert og utsteder, men sier ikke at den ikke skal være mottaker.
  - For forbudet mot at en agent slipper inn noen (D3 i §1): en agent kan ikke godkjenne med sin egen identitet. Men en agent som styrer nettleseren din mens du er innlogget, kan trykke på kortet. Vernet er ditt ja og regelen, som for sending i dag, ikke en lås.
- **1b) En egen eiernøkkel på Macen din, bak Touch ID.** For det som må bygges i CellProtocol og klienten, er det som 1a. Forskjellen er at nøkkelen din signerer avtalene, ikke tjeneren. Tjeneren kan da ikke slippe inn noen, og en agent kan ikke godkjenne for deg: forbudet (D3) blir en lås. Det følger Book 33 slik den står, og det du sa 22.09 om at en celle i skyen som du eier, er innenfor din entitet.
  - Kommer i tillegg til 1a: et lite godkjenningsvindu på Macen. En vei inn i cellen for en avtale som er signert et annet sted enn der cellen kjører; kontrollen av en slik avtale finnes, det som mangler, er stedet å levere den. Og klientene må kjenne eiernøkkelen din, ellers kunne tjeneren byttet den ut; den kan følge med lenken.
  - Pris: godkjenningen skjer på Macen din, og den må være på. Anslagsvis 4–7 arbeidsdager mer enn 1a, og mer å gjennomgå. Anslaget er mitt og er ikke kontrollert.
  - 1b kan komme etter 1a. Da endres klientene én gang til, for eiernøkkelen.
- **1c) Du eier cellen med nøkkelen agenten din alt bruker.** Vegars og Victorias side bruker klienten som den er. Din side bruker klienten med en eierprofil; det finnes i testene, men ingen kommando lager en slik profil. Jeg anbefaler den ikke, av tre grunner. Eieren kan ikke sende vedlegg (A10), så installerpakken kunne ikke gå fra deg til Vegar uten samme regelendring som i 1a. Eierens nøkkel må signere der cellen kjører, altså på staging; da må nøkkelen din enten kopieres dit, eller så trengs samme vei som i 1b. Og agenten din holder nøkkelen som slipper inn folk: S6-dokumentet sier at eierrettigheter aldri skal gis til MCP-prosessen, og forbudet (D3) kan ikke oppfylles.

Ingen av de tre er prøvd. Planen starter med en liten prøve av den du velger (ledd 3 i §3b).

**2. Hvordan ser du at en forespørsel er fra rett person?**

I dag sammenligner du fem lange identitetsverdier som mottakeren sender deg. Book 33 §2 sier at verken en invitasjonsfil eller en adresse gir myndighet alene. Valget er skrevet for 1a. Med 1b står koden i vinduet på Macen din, og 2c faller bort. Med 1c finnes ikke kortet.

- **2a) En kort kode (anbefalt).** Når oppsettet er ferdig, ser mottakeren seks sifre, regnet ut av nøkkelen deres på deres egen maskin. De sender deg sifrene der dere ellers snakker. Kortet viser de samme sifrene. Stemmer de, er forespørselen fra dem. Tjeneren lagrer ingen navn. En invitasjon skal bare kunne brukes én gang, som i den gamle kanalen. Derfor holder seks sifre: den som snapper lenken og melder seg inn først, får en annen kode enn mottakeren, og mottakeren får da ikke meldt seg inn. Pris: ett håndgrep for mottakeren og ett blikk for deg, én gang per nøkkel.
- **2b) Lenken er beviset.** Kortet viser navnet du ga invitasjonen, og ingen kode. Pris: navnet ligger da på tjeneren, og det bryter den fjerde egenskapen i Book 33. Den som får tak i lenken før mottakeren, kan be om tilgang som ham.
- **2c) Som 2b, men navnet ligger bare i nettleseren din.** Tjeneren ser et nummer. Pris: lenken er fortsatt beviset, og navnene følger ikke med til en annen nettleser eller maskin.

**3. Venter delegering til etter første pakke?**

Book 33 §10 punkt 5 sier at en pakke ikke forlater huset før en delegert assistentidentitet sender, og mottakeren verifiserer både assistenten og hvem som står bak. S6-dokumentet har det som forutsetning. Det finnes ikke i koden (A11 i §0). Skillet mellom agenter og identiteter (porten G0 i planen fra 09.09) venter uansett hva du svarer her; det står i §2.

- **3a) Ja, den venter (anbefalt).** Agentene bruker identitetene som i dag. Pakketeksten sier rett ut at hvem som står bak en agent, ikke kan etterprøves kryptografisk ennå. Dette krever at du sier uttrykkelig at punkt 5 venter, for boka sier at alle seks punktene skal være vist først.
- **3b) Nei, delegeringen bygges først.** Da får treet et blad til under A (en delegert identitet sender, og mottakeren verifiserer begge). Anslagsvis en til to uker mer, og en egen gjennomgang.

**4. Kan vedleggene gå til `main` før Vegar og Victoria har prøvd dem?**

Vedleggs-PDD-en sier: «Funksjonsprøvene og de to mottakeroppgavene må begge bestå før noe foreslås mot main.» Regelen din fra 18.09 sier det samme om nye kapabiliteter. Men en pakke bygges fra `main`: HavenAgentD får ikke bygge mot en CellProtocol-revisjon som ikke ligger på CellProtocols `main`, og et skript i CI håndhever det (`HavenAgentD/Scripts/assert_dependencies_are_on_their_main.sh`). Mottakerne kan altså ikke prøve noe som ikke er på `main`.

- **4a) Ja (anbefalt).** Dette er nok for `main`: funksjonsprøvene, Astras gjennomgang, og en formålsprøve med prøveparet, der den ene siden sender den faktiske installerpakken og den andre henter den og installerer den i en ren bruker. Mottakerprøven er første ekte bruk, og den avgjør G3. Det er et unntak fra regelen din, og gjelder bare dette.
- **4b) Nei.** Da kan ikke vedlegg være med i den første pakken. Det blir to pakker: først kryptert tekst, så vedlegg. I treet faller B1–B3 ut av første pakke, A1 mister de to vedleggshandlingene, A4 får fire handlinger i stedet for fjorten, og testene T-A1, T-A4 og T-B1–T-B3 endres. Det går mot svaret ditt i dag («Kryptert og vedlegg samlet»).

**5. Skal det å invitere en ny person uten drift være med i første pakke?**

- **5a) Nei, det kommer etterpå (anbefalt).** Første pakke bruker én invitasjonsliste for prøveparet, deg, Vegar og Victoria, lagt inn én gang med én omstart av staging (ca. 35 sekunder). Fornyelse krever ikke drift (C3), og tilgangen varer til sluttdatoen du setter, så runden kommer ikke igjen hver måned slik som i den gamle kanalen. Neste gang det trengs drift, er når du vil invitere en ny person.
- **5b) Ja.** Invitasjoner lages fra adminsiden og virker uten omstart. Det er en ny flate med eget bilde, og anslagsvis 6–9 arbeidsdager mer (W3 i planen fra 09.09).

### Standardvalg (S1–S10)

S1 og S2 gjelder noe du har sagt eller bedt om før. Resten trenger du bare å lese hvis du vil ha noe annerledes.

| Nr. | Hva | Standard jeg har valgt | Følge | Si fra hvis |
|---|---|---|---|---|
| S1 | Hvordan vedlegg overføres. **Avviker fra svaret ditt 28.09 («Alle tre må støttes»).** | Som kopi i første pakke. | Avsenders krypterte kopi ligger på staging til meldingen utløper, til den kalles tilbake, eller til den er overdratt til mottakeren. «Referanse» og «hent ved behov» finnes i koden, men kan ikke nås mot en celle på staging (A18 i §0): de krever at avsenders celle kjører der filene ligger. For en installerpakke og et budsjett som ligger som filer hos deg, er kopi uansett modusen svaret ditt gir. | de to andre må virke mot Vegar og Victoria i første pakke. Det krever celler som kjører hos dere, og er et eget arbeid. |
| S2 | Varsel ved ny post. **Du har bedt om det to ganger (HD-0069 og HD-0093).** | Ikke i første pakke. | Vegar, Victoria og du må be agenten se etter post, som i dag. I september ble post liggende ulest på den måten. Varsel for de nye cellene trenger en ny rettighet i avtalen (å abonnere på egne hendelser), som Book 33 §3.4 ikke gir i dag, og PDD-en fra 12.09 er bygget for den gamle cellen. | varsel skal inn. Da blir det et eget formål her, med eier og tid. |
| S3 | Rydding ved utløp | En jobb på staging fjerner utløpte meldinger og vedlegg hver time. | A6 kan prøves uten at noen leser. I koden i dag fjernes en utløpt melding først neste gang noen kaller cellen. | det holder at de fjernes ved neste kall. Da endres A6 og T-A6. |
| S4 | Levetid for en melding | 30 dager når avsenderen ikke sier noe, høyst 90, som i koden. | Book 33 §5.2 sier at standarden for kontakt bør være lang, og at eieren skal kunne sette den per relasjon. Det siste er ikke bygget. | du vil ha andre tall i første pakke. |
| S5 | Hvor lenge en tilgang varer | Til sluttdatoen du setter når du godkjenner. Setter du ingen, ett år, som er det lengste koden tillater (`Contract.maximumDuration`). | Ingen fornyelse før den datoen. | standarden skal være kortere. |
| S6 | Plass til vedlegg | Ingen grense per fil (svaret ditt 28.09). Staging avviser et nytt vedlegg når datadisken har mindre enn 10 GB ledig. | Tallet er et forslag. Ledig plass måles i planen. | du vil ha en annen terskel. |
| S7 | Hvem som legger klienten inn hos mottakerens agent | Mottakerens agent gjør det selv, når mottakeren gir den lenken. | Installereren rører fortsatt ikke oppsettet til Claude eller Codex. Slik er det i dag: pakken skriver ut hva mottakeren selv må kjøre i Terminal, og det lille pilotskriptet lar med vilje oppsettet være (`HavenAgentD/Packaging/README.md`). | installereren skal gjøre det. |
| S8 | Hvilken pakke | Hele pakken, signert og notarisert. | Book 33 §10 punkt 6, og ordene dine 05.10. Ikke åpent; står her for at det skal være sagt. Det lille, usignerte pilotskriptet brukes ikke. | — |
| S9 | Hvem som gjør relasjonsmodellen ferdig i CellProtocol og klienten | Korrespondanse-tråden, fordi det henger sammen med tjenerdelen du ga den i dag. Astra gjennomgår. | Alt går etter hverandre i én tråd (§3b). | Codex skal ha det, siden Codex skrev cellen og klienten. Da går det samtidig med tjenerdelen, og samlet tid blir kortere. |
| S10 | Et nytt felt i klartekst | Ytterdelen av konvolutten har på vedleggsgrenen fått nummeret på avtalen vedlegget er bundet til. Feltet står. | Driften kan se at en melding har vedlegg. Book 33 §5.1 lister ikke feltet. Det samme nummeret står uansett i klartekst i kallet som sender meldingen, i vedleggshandlingene og i lagerets register, så å flytte feltet inn i den krypterte delen skjuler ingenting. Det legges inn i endringsforslaget til boka, og Astra får det som eget punkt. | du vil at det ikke skal synes for driften at en melding har vedlegg. Det er et større arbeid enn å flytte ett felt. |

## 3. Det du selv må gjøre, og tid

Haster, fordi Vegars tilgang i den gamle kanalen går ut 08.10:
1. Svare ja eller nei på spørsmålet jeg stilte 06.10 kl. 12:01Z: kan jeg bruke root på staging-verten til å bytte den ene linja med invitasjoner i `/etc/haven/staging-correspondence-invites.env`? Uten det kan fornyelsen ikke kjøres av meg. Etter byttet: godkjenne to kort for prøveparet, videresende én melding til Vegar og én til Victoria, og godkjenne kortene deres.

Nå, for det nye:
2. Svare på de fem valgene over, lese S1 og S2 samme sted, og si om G1 er godkjent.
3. Spørre Vegar og Victoria hvilken Mac de har (Intel eller Apple Silicon, og hvilken macOS), og Victoria hva hun har installert. Har en av dem Intel: si hvem som kan prøve pakken på en Intel-Mac, for din har ikke Rosetta.
4. Si hvilken installerpakke og hvilken budsjettfil som skal sendes som vedlegg, og hvem som skal ha budsjettet.

Før planen:
5. Se på bildene av kortet og av mottakerens oppsett, og godkjenne dem (G1-GUI).
6. Godkjenne planen (G2).

Underveis:
7. Bestemme om de åpne brofunnene (N32 og N36–N39) skal rettes først eller godtas skriftlig, så CellProtocol kan gis ut.
8. Si «merge» for hver PR, og ja til hver utsetting til staging. Si ja eller nei til endringsforslaget til Book 33.
9. Gi uttrykkelig godkjenning for at relasjonscellene opprettes og avtalene utstedes på staging (S6-dokumentet krever det), og logge inn på staging som admin når kortet skal prøves.
10. Installere pakken på din egen Mac (dobbeltklikk og passord), i et vindu der køen står stille, og svare «Tillat alltid» når macOS spør om nøkkelringen. Den gamle klienten blir stående ved siden av til begge mottakerne er over.
11. Godkjenne forespørslene, én per person som ber om tilgang: prøveparet, din egen identitet, Vegar og Victoria. Regn med fem til seks trykk; det nøyaktige tallet følger av kortet du godkjenner som bilde. Med valg 2a: se at koden stemmer for hver.
12. Godkjenne pakketeksten, og videresende én melding til Vegar og én til Victoria.
13. Trolig i begynnelsen av november: én fornyelse til i den gamle kanalen (ja til en omstart, og godkjenne kortene på nytt), hvis det nye ikke er ute før 05.11.

Til slutt:
14. Når begge har bekreftet: si at de gamle tilgangene kan trekkes (C5), og om G3 er godkjent.

**Samlet.** Leddene korrespondanse-tråden har (3–9, 12 og 13), er 26–43 arbeidsdager når de tas etter hverandre. Det er fem til ni uker, før runder. Tar Codex ledd 4–6 mens korrespondanse-tråden tar ledd 7–9, går to løp samtidig, og tre til fem uker er mulig. Jeg lover ingen dato. Bro-leddene (1 og 2) har jeg ikke tall for.

**Følge for den gamle kanalen.** Når fornyelsen som pågår, er gjennomført, har Vegar og Victoria tilgang der til 05.11. Etter anslaget over er det nye neppe ute før den datoen. Da må den gamle kanalen fornyes én gang til i november, med skriptet som blir ferdig nå.

## 4. Det jeg ikke vet

- Om N35 er lukket i #53, og hvor mye som gjenstår på bro-leddene.
- Hva #53 gir en klient å bygge på for håndtrykket; tittelen sier at AP7 er med, og jeg har ikke lest det.
- Hvordan en invitert identitet skal bevise nøkkelen sin i innmeldingen når den er koblet til over broen (valg 1).
- Om `/admin/funding` er rammet av feilen i adminflatene (HD-0143).
- Hvilke Macer Vegar og Victoria har, og hva Victoria har installert.
- Hvor mye ledig plass datadisken på staging har.
- Hva godkjenningsflaten for den gamle kanalen inneholder; jeg har sett at fila finnes, ikke lest den.
- Hvor mange runder gjennomgangene tar.

## 5. Ordliste

| Ord | Betyr her |
|---|---|
| Relasjonscelle | Én celle per relasjon. Du og Vegar er én relasjon, du og Victoria en annen. Cellen lagrer meldingene mellom de to, og ingenting annet. I koden heter den `CorrespondenceCell`. |
| Konvolutt | En melding slik den ligger lagret: en kryptert innerdel (emne, innhold, beskrivelse av vedlegg) og en liten ytterdel i klartekst (avsenderens identitetsnummer, tid, utløp, størrelse). |
| Korrespondanseidentitet | Et nøkkelpar som bare brukes til korrespondanse. Tjeneren kjenner nummeret og den offentlige nøkkelen, ikke hvem som står bak. |
| Avtale | Det signerte beviset som sier hva en identitet får gjøre i en celle: se innboksen, lese en melding, sende, kvittere, og vedleggshandlingene. |
| Eier av en celle | Identiteten som signerer avtalene, og dermed den som slipper inn medlemmer. |
| Den inviterte parten | Den som har fått en avtale av eieren. Klienten på `main` virker bare for denne parten. |
| Broen | Den krypterte forbindelsen fra en klient til celler på en tjener (WSS, altså WebSocket over TLS). Etter PR #53 i CellProtocol må klienten bevise identiteten sin med et håndtrykk når forbindelsen åpnes. |
| Innmelding | Det klienten gjør første gang: lager nøkler, ber om tilgang, og henter avtalen når forespørselen er godkjent. |
| Pin | Hvilken revisjon av CellProtocol et annet repo bygger mot. |
| Staging | Prøvetjeneren, `staging.haven.digipomps.org`. |
| Prøveparet | To prøveidentiteter korrespondanse-tråden styrer. Alt prøves på dem før Vegar og Victoria får noe. |
| Kortet | Flaten der du godkjenner eller avslår en forespørsel om tilgang. I dag: «Godkjenn meldingsadgang» under `/admin/funding` på staging. |
| Astra | Codex når den gjør uavhengig sikkerhetsgjennomgang. |
| Fabel | En uavhengig Claude-kontrollør som ikke har sett arbeidet før. |
| Pakketeksten | Det som står i meldingen du videresender til en mottaker, og i veiledningen i pakken. |
| Undercelle | En celle som ligger inne i en annen. Her: lageret for én avsenders vedlegg, inne i relasjonscellen. |
| S6-dokumentet | Beskrivelsen fra 07.09 av hva som må endres på tjeneren for den nye korrespondansen, og hva som må være på plass først: `HavenAgentD/Docs/CorrespondenceS6ChangeSetAndRollback.md`. |
| Planen fra 09.09 | `CellProtocolDocuments/Deliverables/Correspondence_Uten_Agent_I_Runtime_Plan_2026-09-09.md`. Et forslag, ikke gjennomført. W0–W7 er arbeidspakkene der, og G0–G7 portene. G0 er porten for at agenter ikke skal kunne bruke korrespondanseidentiteter. |
| N32, N35, N36–N39 | Nummererte funn fra Astras gjennomganger av broen (PR #53). |
| HD-0006, HD-0166 og lignende | Oppgaver i deploy-køen, `HAVEN-Deploy/queue/tasks/`. |
| AP5, AP6, AP7 | Arbeidspakker i bro-planen, `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/PLAN.md`. |
| Signert og notarisert | Pakken er signert med utviklernøkkelen din og godkjent av Apple, så macOS (Gatekeeper) åpner den uten advarsel. |
| CI | De automatiske byggene og testene på GitHub. |
