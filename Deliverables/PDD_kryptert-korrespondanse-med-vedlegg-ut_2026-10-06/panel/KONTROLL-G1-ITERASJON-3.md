# RAPPORT — kontroll av G1-siden, iterasjon 3 (07.10.2026)

Forkortelser: K = `utkast/G1-KORT.md` · D = `utkast/spec-v2-til-v3.diff` · S = `utkast/FORMAALSSPEC.md` · E = `kilder/eierens-ord.md` · KO = koordineringsfila · KC = `kilder/kontroll-av-chatsvaret-0610.md` · B1/B2 = de to bildene · F = figuren. Tall etter kolon er linjer.

## Dom
**Nei, ikke som den står.** De sju punktene har bladformål og test i differansen, og fem av fem stikkprøver i koden stemmer.
Men siden lar eieren godkjenne valg han ikke har tatt, kaller tjeneren «blind», teller ikke hans egne håndgrep, og sier ikke det som haster (fornyelsen før 08.10).

## MÅ endres
1. **Koden på seks sifre står som avgjort.** Står: K:13, og D:341 «Avgjort … Følger av valg 1». Lest: i iterasjon 2 var koden et eget valg også med nøklene på Macen (D:304–307), og eieren fikk 07.10 høre to håndgrep, pakke og lenke (E:34). Bør stå: «Mitt forslag: mottakeren sender deg også en kode (tre håndgrep i alt). Uten den er lenken alene beviset.» Rett D:341.
2. **Det som er valgt bort, er ikke blant de fire spørsmålene, og «1 ja» sier ikke hva det dekker** (K:29–33, K:17, K:53). Varsel: eieren har bedt om det to ganger (D:346), men det står som avgjort på grunnlag av Flow-forslaget hans (D:343), og «kommer rett etter» (K:31) er et løfte uten formål, eier eller tid. Bare kopi: avviker fra svaret hans 28.09 (S:614), og det sies ikke (K:32). Sikkerhetskopi: forfatterens valg (D:139). Bør stå: et eget spørsmål, «Dette er ikke med i første pakke; si fra om noe må inn», med de to merknadene, og én setning om at ja til 1 ikke godkjenner standardvalgene.
3. **«Tjeneren er blind»** (K:10) og «verken har klartekst» (K:24) er for sterkt. Lest: et felt i klartekst viser at en melding har vedlegg (S:623), og ytterdata går åpent (KC:45). Bør stå: «Tjeneren kan ikke lese innholdet og ikke slippe inn noen. Den ser hvem (numre) som skriver, når, og om det er vedlegg.»
4. **Eierens egne håndgrep er ikke telt, og rekkefølgen er feil.** Står: «én gang per person» (K:12), «ett trykk» (D:123). B1 viser to Touch ID per person (lage lenke, godkjenne) og en kode å sammenligne. K:62 setter «godkjenne Vegar og Victoria» før «sende pakken og lenken». Bør stå, per person: lag lenke → send pakke og lenke → få koden og sammenlign → godkjenn.
5. **Det som haster, mangler.** K:15 sier at den gamle kanalen står. Lest: tilgangen der går ut 08.10 (S:248), eieren skal selv sende fornyelsen (S:290), den varer til 05.11, og F sier «klar til å sendes». Sluttet: den er ikke sendt. Bør stå øverst under «nå»: send fornyelsen før 08.10; blir det nye ikke ferdig til 05.11, kommer én runde til.
6. **Spørsmål 3 går i ring og er for smalt** (K:55). Prøveparet bruker programmet fra pakken (K:24), pakken bygges fra `main`, og `main` krever grønn prøve med prøveparet. Bør stå: «en lokal prøve med to prøveidentiteter». Det samme gjelder resten av celleendringene (D:224), ikke bare vedlegg. Legg til følgen av nei: to pakker (D:333).
7. **Hvem som gjennomgår.** Står: «Codex. Astra gjennomgår» (K:39). Lest: Astra er Codex (S:52), og godkjenningsvinduet, selve låsen, har ingen gjennomgang (K:40, D:123). Sluttet: etter «to løp» gjennomgår Codex sitt eget arbeid. Bør stå hvem som kontrollerer uavhengig.

## BØR endres
- **Status og «hva jeg skal gjøre» øverst.** Eieren har sagt tre ganger at han ikke ser det (E:4, 15, 30). Status står bare i F. Flytt K:51–58 opp, med én statuslinje: ingenting nytt er hos Vegar og Victoria, og ingen ny pakke er bygget.
- **Touch ID og vinduet** (K:12) følger ikke av valget 07.10 (E:19), men dekkes av spørsmål 1 og 4. Merk dem som forslag. B1 viser ikke passordveien.
- **Codex tar mer enn han valgte.** Valget gjaldt CellProtocol og klienten (E:24–27). K:40 legger til godkjenningsvinduet og oppsettet (før: denne tråden, D:118–119), og D:38 kaller pakken «ditt valg». Si det i tabellen. Si også at første ledd krever plass i Codex-køen (E:25).
- **Chat-cellen brukes ikke.** Eieren foreslo å bruke den (E:12). Differansen utvider korrespondansecellen (D:36, 71). K:5 og K:11 sier det ikke. Én setning med grunnen (klartekst, ingen vedlegg).
- **Agentene sender og leser fortsatt med eierens nøkkel, uten lås** (D:133, D:128). K:12 kan leses som mer. Ta det inn i spørsmål 2.
- **Bildene mot siden.** B2 «Jeg sier fra når han har godkjent» er et varsel, som K:31 sier ikke er med. B1 har «sju dager … én gang» og «Trekk tilgangen…»; søk i S gir ingen treff (sluttet: uten bladformål og test). B1 viser ett års tilgang (S:618), som ikke står på siden.
- **Figuren.** «DU» står fire steder, K:62 nevner flere (plan, merge, utsetting, prøveidentitet, siste ord). Ja-et til bro-utgivelsen står i F og D:242, ikke i K:51–58.
- **Broen (A23, D:74) kan ikke etterprøves:** fila jeg har, slutter 09:56Z (KO:141), og A23 viser til senere innlegg. A23 nevner ett funn færre enn KO:146. K:42 legger bro-ruta hos andre, mens D:362 sier at det ikke er kjent om den dekker korrespondansen.
- **Første prøve dekker bare innslipp.** Abonnement over broen er ikke prøvd (D:73, D:361), og eierens egen deltakelse fra en annen maskin er samme spørsmål (KC:61). A7 sier ikke hva som skjer med lese-registreringen (KC:60).
- **Tid** (K:49): ikke et løfte og ikke i strid med «CellProtocol først» (K:39, F). Sluttet: summen er over en måned og forbi 05.11; si det. Invitasjon fra Macen var «kommer etterpå» i iterasjon 2 (D:328); prisen står ikke.
- **Prisen** (K:17): si at Vegar og Victoria da må inviteres på nytt (sluttet). «Nøkkelen» i entall mot «nøklene» i K:10 (KC:14).

## Spørsmål 2 og 3, kort
Punkt 1 → A1, 2 → A3, 3 → A7 og A4, 4 → C2 og D3, 5 → C1 og C3, 6 → B1–B3, 7 → C4–C5 og D1 (D:102–128, S:198–207). Tre håndgrep for mottakeren er likt i K:25, B2 og D:122; navnet på C1 sier fortsatt «ett». Lest i koden, alle stemmer med A19–A22: malen har fire handlinger og ikke abonnement; de fire operasjonene sjekker bare medlemskap; fem hendelser; klienten krever nøyaktig fire og bruker bare les og skriv; broen har abonnementskommandoen.

## Spørsmål 4: valg forfatteren har tatt, som ikke står på siden
1. Korrespondansecellen utvides; chat-cellen brukes ikke. 2. Agentene bruker eierens nøkkel uten lås. 3. Levetider: melding 30 dager, høyst 90 (S:617); tilgang ett år (S:618); lenke sju dager (B1). 4. Bare kopi, mot svaret 28.09 (S:614). 5. Feltet i klartekst som viser vedlegg (S:623).

## Kan strykes (siden er 916 ord, omtrent to sider)
K:3 andre og tredje setning. K:5: behold første setning av sitatet. K:23 og K:45: filnavn i stedet for stier. K:24–27: én setning. K:37–43: figuren viser det samme; behold én linje. K:49: setning to til fire.

## Lest mot sluttet
Lest: K, E, D, de tre bildene, KC, KO:139–152, S-linjene over, og fem steder i koden. Sluttet: det som er merket slik. Ikke lest: resten av S og iterasjon 2. Ingen kode er kjørt.
