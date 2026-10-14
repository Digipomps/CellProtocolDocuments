# RAPPORT: UTKAST.md kontrollert mot kilder/ (2026-10-06). L = lest i kilden, S = sluttet av meg.

**Dom:** Kan ikke sendes som det står. Det tekniske (byttet, revisjon, liste, claim, prøveparets tilstand, 144 av 145) stemmer med utdataene,
men kortnavnene står ikke i kildene, to ting eieren må vite/gjøre er utelatt (følgen av å ikke godkjenne i tide, og steg 11), og nedetid og 20:57Z er for enkelt lest.

**MÅ endres**
1. «kortene Torrkjoring A/B»: står ikke i noen kilde. Kildene har bare profil/principal sim-a (sim-torrkjoring-a) og sim-b (sim-torrkjoring-b) (PROEVE-7:6,10,20,24) og handlingen «Godkjenn meldingsadgang» (LES-MEG:19) L. Bruk de navnene, ellers leter eieren etter kort som ikke finnes.
2. Følgen av å ikke godkjenne innen fristen mangler: en forespørsel står i høyst 24 t, så er invitasjonen brukt opp og det trengs en ny (LES-MEG:169, :142, :147) L; ny invitasjon = steg 1 og 5 på nytt, altså nytt bytte og ny omstart av staging (LES-MEG:141) S. Dette er grunnen til at fristen er alvorlig, og det må stå.
3. «Etter godkjenningen din» stopper ved steg 10. Steg 11 mangler: eieren må også godkjenne Vegars og Victorias forespørsler innen 24 t når de sier fra, og avtale tidspunktet først så de er uten bevis i minutter, ikke timer (LES-MEG:21, :44) L; et meldingsverktøy som alt kjører hos Vegar virker til godkjenningen og må så startes på nytt (LES-MEG:113) L.
4. «nede i 22 sekunder»: loggen sier STOPPED 21:06:08Z («nedetiden starter her»), READY_OK 21:06:19Z, så «kontrollert restart» og READY_OK 21:06:30Z (UTFOER:34,37-40) L. Altså to bolker innenfor 22 s, kort oppe 21:06:19Z; og loggens egne «etter 15s» (to ganger) stemmer ikke med 11 s mellom klokkeslettene, så sekundene er usikre S. Skriv «nede i to omganger innenfor 22 sekunder (21:06:08Z–21:06:30Z)».
5. «alle 134 testene var grønne kl. 20:57Z» og «lagt til før byttet»: 134 og OK stemmer (hele-testrekka:4-6) L, men ingen fil oppgir klokkeslett; 20:57Z og «før byttet» er sluttet fra filnavnet «2049» + 495,667 s S. Skriv «ca. 20:57Z» eller sløyf klokkeslettet.

**Bør med (utelatt, ikke feil)**
- Prøveprofilene er uten tilgangsbevis mens de venter (GODTAS:5,9; LES-MEG:113) L. Én bisetning holder.
- Invitasjonene i den nye lista går ut 13.10 kl. 07:13Z (LES-MEG:46; UTFOER:3-6 «154 timer til») L: det er vinduet Vegar og Victoria må kjøre fila i.
- Prøven tas før 08.10 og dekker Vegars tilfelle (fornyelse før fristen), ikke Victorias (tilgangen hennes gikk ut 29.09) (LES-MEG:11, :48) L/S.
- Lenkene har engangskode og skal ikke stå andre steder (LES-MEG:91) L: «to ferdige meldinger med hver sin lenke» bør ikke havne i kø- eller statusfiler S.
- Byttet la igjen en kopi av fila under /etc/haven og tjenerfil/logger hos ops, som skriptet ikke fjerner (UTFOER:47-48; LES-MEG:87) L. Kan nevnes.

**Påstand for påstand**
- «Byttet er gjort, staging er oppe; to godkjenninger trengs for prøveparet»: stemmer (UTFOER:43,50; PROEVE-7:33) L.
- Adressen: stemmer (PROEVE-7:33; LES-MEG:19) L. 24-timersfristen: stemmer (PROEVE-7:14,28,33; LES-MEG:169) L.
- «Fristen er 07.10 kl. 21:11Z»: stemmer som utledet: sendt 21:11:06Z og ca. 21:11:07Z (PROEVE-7:1,31), utløp = min(invitasjonsutløp, +24 t) (LES-MEG:169) S. «23:11 norsk tid»: riktig (sommertid, UTC+2), står ikke i kildene S. «I morgen tidlig er tidsnok»: holder for fristen, men Vegars utløp 08.10 (LES-MEG:11) taler for tidlig S.
- «21:05:54Z: linja byttet i fila på staging-verten, som root»: tid og bytte stemmer (UTFOER:24) L; «som root» står i metoden (LES-MEG:54) og følger av at fila eies av root med 600 (UTFOER:16), ikke i selve utdatalinja S.
- «21:06:08Z til 21:06:30Z … containeren laget på nytt … starter den to ganger … tidene fra haven-deploy-loggen, ikke målt utenfra»: klokkeslett, ny container, to starter og forbeholdet stemmer (UTFOER:27,34-40,45) L. «nede i 22 sekunder»: se MÅ 4.
- «Samme revisjon som før»: stemmer (UTFOER:7,29,43) L. «lista i containeren er den nye»: stemmer (UTFOER:45,46) L. «frigav claimen»: stemmer (UTFOER:50; = utfall 2 i LES-MEG:68) L. «Ingen HINDER eller MERK»: ingen treff i noen av de fem utdatafilene, alle kontroller «ok» (UTFOER:2-50) L.
- «21:08:46Z: tjeneren godtar fortsatt tilgangen prøveparet hadde før omstarten»: stemmer (PROEVE-6:1,10,16,17) L.
- «21:11Z: prøveparet kjørte fila Vegar og Victoria skal få, HD-0006/forny-haven-tilgang.sh»: stemmer (PROEVE-7:1,2,16,30; LES-MEG:20,91) L; strengt tatt kjørte tråden skriptet for begge profilene, med to ulike klienter (PROEVE-7:3-4) L. «Begge forespørslene venter nå på deg»: stemmer (PROEVE-7:13,27,33) L.
- «21:12Z: tjeneren godtar fortsatt det gamle beviset mens forespørslene venter, som ventet»: stemmer (GODTAS:1,4,8,11) L. Samme fil sier at profilene nå er uten bevis (GODTAS:5,9), se Bør.
- «henter de nye tilgangene og sender en melding hver vei»: stemmer med steg 9 (LES-MEG:42; PROEVE-7:34) L. «jeg måler at det gamle beviset da blir avvist»: stemmer, det er målefasen etter godkjenning (LES-MEG:237, :163) L.
- «Er det grønt, får du to ferdige meldinger … hver sin lenke og fila»: stemmer med steg 10 og teksten til mottakerne (LES-MEG:20,43,91,115-127) L; lenken settes inn per mottaker (LES-MEG:127). «Vegars tilgang går ut 08.10»: stemmer (LES-MEG:11,48) L.
- Stiene til utdatafilene: filnavnene finnes i kildene, og HD-0006-mappa stemmer med PROEVE-7:16; selve Mac-stiene kan ikke kontrolleres herfra S.
- «144 av 145 innsatte feil ble fanget»: stemmer (runde4.log:147; den ufangede er :117, «fila legges tilbake mens haven-deploy kanskje går») L. «Testen for den siste ble lagt til»: stemmer (m100.log:1-3 «1 av 1 fanget»; 133 tester i LES-MEG:184 mot 134 i hele-testrekka:4) L; «før byttet» bare S (MÅ 5). «rød mot feilen»: stemmer (ny-test:1,3,5) L. «grønn mot skriptet»: trolig; halen viser 134 OK, men ikke navnet på den nye testen (hele-testrekka:1-6) S.
- «LES-MEG.md og statusfilene er ikke ført opp etter byttet»: stemmer; LES-MEG:5 og :185 sier fortsatt at byttet/utfoer ikke er kjørt, og :184 venter på 145-tallet L.
