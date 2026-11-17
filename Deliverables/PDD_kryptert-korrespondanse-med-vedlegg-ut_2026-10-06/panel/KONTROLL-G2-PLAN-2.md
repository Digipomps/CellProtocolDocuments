# RAPPORT — etterkontroll av PLAN.md og MELDING-G2.md (07.10.2026)

**Dom:** Ja, etter rettelsene MÅ 1–6. Planen stemmer med de nye kildene, og de ni rettelsene er tatt inn.
Feilene ligger i meldingen: avsnittet om G2 sier både mer og mindre enn planen, og et bart «G2 ja» er ikke entydig for punkt 5.

Start 15:20:51Z, slutt 15:28:53Z. Spørsmål 1, 3, 2 og 4 er tatt, 5 delvis. L = lest i kilden, S = sluttet.

## MÅ endres
1. **MELDING, «Det du bestemmer med G2» (L).** Mer enn planen: unntaket for Fabel mangler, og «før noe går til hovedgrenen» er videre enn planen (trinn 2, CellProtocol). Mindre enn planen: «Når jeg kommer tilbake til deg uten at du har spurt» mangler. Riktig: «rekkefølgen i trinn 1 til 9 og hvem som skriver og gjennomgår hva; at bolkene åpnes i den rekkefølgen, og at ingen annen bolk åpnes før prøven i trinn 1 holder; den lokale formålsprøven før cellen går til hovedgrenen i CellProtocol (trinn 2); at en annen modell leser når Fabel ikke er tilgjengelig, og at det da står hvilken, unntatt gjennomgangen før «merge» av koden for vedlegg, der du avgjør om en annen modell holder; når jeg kommer tilbake til deg uten at du har spurt (fire tilfeller under «Trinnene»); og endringene i tabellen «Endringer etter G1».»
2. **MELDING, samme avsnitt og «Fra deg nå» punkt 2 (L, plan linje 176, 184, 186).** Første rad i «Endringer etter G1» tar ut punkt 7 fra G1 (den gamle kanalen står til begge er over) på en lesning han verken har rettet eller bekreftet. Meldingen sier ikke hva et bart «G2 ja» betyr for den. Legg til: «Tabellen har tolv rader. Tre endrer noe du godkjente i G1, etter min lesning: den gamle kanalen fornyes ikke (punkt 5), B1 gjennomgås av Fabel og ikke Astra, og koden på seks sifre er med. Sier du «G2 ja» uten å nevne punkt 5, tar jeg det som at lesningen står.»
3. **MELDING linje 12 (L).** Fjorten stemmer. «fram til Vegar og Victoria har bekreftet» stemmer ikke: punkt 12 til 14 kommer etterpå (trinn 9). «de fleste ett ord hver» stemmer ikke med lista: fire punkter (2, 8, 12, 14) er ett ord. Riktig: «fjorten punkter i alt, til og med G3. Fire er ett ord. Punkt 4 til 6 er minst tre «merge» og minst to ja, og punkt 10 er fire håndgrep per person, to av dem med Touch ID eller passord.»
4. **PLAN «Avgjort 07.10», rad A (L, Book33-utdraget).** §10 nevner ikke ordet hans. Den sier at en pakke kan sendes når punkt 5 (en delegert assistentidentitet sender og blir kontrollert) er vist. Riktig: «Book 33 §10 punkt 5 krever at en delegert assistentidentitet er vist før en pakke sendes ut. «A ja» er ordet hans om å sende første pakke uten. Avviket føres i endringsforslaget til Book 33 (punkt 12).»
5. **PLAN «Trinnene», trinn 3, «Venter på» (L, kø-trådens innlegg kl. 15:09Z).** For sterkt uten forbehold: innlegget sier at integrasjonen tar med bro-grenen og kontrollerer adminbro-ruta, uten push. Riktig: «Kø-trådens integrasjon av CellScaffold `2026.9.7`, som pågår (første steg lagt inn kl. 15:08Z). Om den dekker ruta korrespondansen trenger, er spurt kl. 15:10Z og ikke besvart.» Figuren, boks 3, har samme mangel.
6. **PLAN «Kontroll», siste punkt, og MELDING, siste linje.** «Ingenting av det som er endret etter kontrollen, er lest på nytt» er ikke lenger sant. Skriv at meldingen, rettelsene og det nye ble lest av en annen uavhengig leser (Claude Opus) 07.10 kl. 15:20–15:30Z, med dommen over, og at rettelsene etter den ikke er lest. Dommen fra første kontroll står i anførselstegn, men lyder i rapporten «Ja, etter rettelsene 1–9 under».

## BØR endres
- **MELDING «de ni trinnene»:** tabellen og figuren har ti (0 til 9), ni gjenstår. Skriv «trinn 1 til 9» (L).
- **MELDING «Fra deg nå»:** planen har tre punkter nå (macOS-versjonene, «ikke i dag»), meldingen to. Følgen mangler «i dag» og «Victoria er det alt» (L, plan punkt 1).
- **MELDING «Nytt fra målingene»:** «47 til 101 GB» stemmer (L: tre filsystemer med 47, 49 og 101; hvilket appens data ligger på, er ikke lest). «som må avgjøres før pakken kan bygges» er planens krav, ikke målt; målt er at begge er åpne og uten konflikt. «ikke på en gren, slik spesifikasjonen sa» kan leses begge veier.
- **PLAN «Målt», rad 1, og BOLK-1-OPPDRAG:** «PR #60 endrer blant annet `ensureRuntimeReady()`» står ikke i kildene (tittelen i målingen kl. 14:35Z sier noe annet). Si hvor det er lest. Samme for «Taggen `2026.9.6` peker på den (lest kl. 13:49Z)».
- **PLAN:** nevner ikke at kø-tråden retter avvisningsrekkefølgen i CellProtocol med ny tag på eierens ja (beslutningspunkt kl. 18:00Z), i området bolk 1 prøver (L).
- **PLAN lista mot «Trinnene»:** trinn 3 har «Ja til utsetting, hos kø-tråden», som ikke er blant de fjorten. Trinn 9 «Ditt ord» mangler ja eller nei til Book 33 (punkt 12). Figuren: boks 3 har ikke «DU»-merke.
- **PLAN AP-B1:** formålsteksten sier «gjennomgått av Astra», kolonnen «Hvem» sier Fabel. Merk raden «endres, se Endringer etter G1».
- **handoff/README:** bolk 3 venter på «CellProtocol `2026.9.5` med broen gitt ut», som er gjort. Bolk 5 mangler vilkårene i trinn 6: grønn hovedgren med #28 og #30 avgjort, macOS-versjonene og en måte å prøve Intel på (L).
- **contract/relasjonscelle-avtale.json:** `readFrom.revision` sier at hovedgrenen er den gamle revisjonen; det gjaldt til kl. 15:04Z. `clientRules` mangler fortsatt linje 494–501 og 555–559 i utdraget (L).
- **BOLK-1-OPPDRAG (spørsmål 5, haster: jobben er bestilt):** 3f («lagt fram av en annen identitet enn subjektet») fastlegger det punkt 1 lar stå åpent («hvem som legger det fram, er en del av svaret»), og strider mot dataflow kant 5, der eierens Mac legger fram kontrakten. Punkt 4 «og hva mangler?» forutsetter at noe mangler. Køprompten: «Ingen endring i CellScaffold» mot «Kjør `CellScaffold/scripts/haven_learn.py`» (S). Sitatet «A ja, B ja, C ja» er kuttet uten merke.

## De ni MÅ-rettelsene fra første kontroll (L)
1 tatt inn. 2 tatt inn (delen om svar A falt bort med «A ja»). 3 tatt inn. 4 tatt inn i ny form (hovedgrenen har flyttet seg). 5 tatt inn. 6 tatt inn, holdt mot lista i første rapport, ikke mot spesifikasjonen. 7 tatt inn. 8 tatt inn. 9 tatt inn.

## Stemmer (L)
Eierens svar ordrett, og A, B og C mot spørsmålene. Taggen kl. 15:04Z på eierens ja kl. 14:40Z. Bestillingen kl. 15:10Z, «ikke startet», «ikke kvittert». Tre nå og elleve senere er fjorten. Alle 19 arbeidspakker: «Trinn» og «Bolk» følger «Trinnene». Figuren har boks 0 til 9 og samme rekkefølge, hvem og ord som tabellen, bortsett fra boks 3. README: bare bolk 1 er åpnet; bolk 2 og 4 venter på G2 og bolk 1.

## Ikke kontrollert
- `DIFF-PLAN.txt` er ikke lest; hele `PLAN.md` slik den står, er lest i stedet.
- Stedene i «Endringer etter G1» (paragraf og rad) mot spesifikasjonen. «Forny, jeg bytter selv» står ordrett i spesifikasjonen linje 76 (L). Den andre trådens tekst om «Bad CPU type» er ikke blant kildene.
- Søkt etter «S1» til «S6» som bolk-navn i planen, dataflyten, `handoff/` og `contract/`: ingen funn (L). Figuren er sett på, ikke søkt i.
- Ikke åpnet: S6-dokumentet, G1-KORT, STATUS-etter-G1, KOORDINERING-utdraget, `Contract.swift`, malene, og det meste av GeneralCell-utdraget.
- Den fulle stien i meldingen, og om «ikke startet» gjelder når meldingen sendes.
- Utdataene fra tagg-jobben viser en annen hash hos GitHub enn commit-en. Det passer med en annotert tag (S), og er ikke målt.
- Om lesningen av punkt 5 er rett. Det kan bare eieren si.
