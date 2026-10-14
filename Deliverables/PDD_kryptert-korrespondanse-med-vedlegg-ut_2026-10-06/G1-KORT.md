# Kryptert korrespondanse med vedlegg, ut til Vegar og Victoria — kort til G1

Iterasjon 3, 07.10.2026, fra Claude-tråden i prosjektet «HavenAgentD» («korrespondanse-tråden»). Mappe: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Filnavnene under ligger i den mappen.

**Status:** Vegar og Victoria har ikke fått noe nytt, og ingen ny installerer er bygget. **Haster i dag:** send fornyelsen av den gamle kanalen til dem. Meldingene ligger klare i HAVEN-mappen, under `korrespondanse-privat-20261006/til-vegar/` og `korrespondanse-privat-20261006/til-victoria/`. Vegars tilgang går ut 08.10.

## Det jeg trenger fra deg nå

1. **G1:** er de sju punktene under det du vil ha? Et ja godkjenner punktene, ikke standardvalgene i `FORMAALSSPEC.md` (S1–S10).
2. **Venter delegering til etter første pakke?** Book 33 krever en delegert assistentidentitet før en pakke forlater huset. Den finnes ikke i koden, og jeg anslo en til to uker ekstra. Anbefalt: ja, den venter, og pakketeksten sier det.
3. **Kan vedlegg gå til `main` før Vegar og Victoria har prøvd dem?** Vedleggs-PDD-en sier at de skal prøve først, men en pakke kan bare bygges fra `main`. Anbefalt: ja, når funksjonsprøvene, en uavhengig gjennomgang og en lokal formålsprøve med to prøveidentiteter er grønne. Nei betyr to pakker: først tekst, så vedlegg.
4. **Bildene:** er `images/godkjenning-paa-macen-v1.png` og `images/mottaker-oppsett-v1.png` slik du vil ha det? De viser forslaget mitt om en kode på seks sifre. Uten koden har mottakeren ett håndgrep mindre, men da er lenken alene beviset.
5. **Ikke i første pakke**, hvis du ikke sier noe annet: varsel på skjermen ved ny post (du har bedt om det to ganger; klienten får posten uten å spørre, men varselet er ikke med), vedlegg som referanse eller hent ved behov (du svarte 28.09 at alle tre skal støttes; første pakke sender kopi), og sikkerhetskopi av nøkkelen på Macen.

Svar gjerne «1 ja, 2 ja, 3 ja, 4 ja, 5 ok», eller si hva som skal endres.

## De sju punktene

1. **Dere skriver til hverandre, kryptert.** Du og Vegar har én celle, du og Victoria en annen. Du eier dem og er med som deltaker. Begge parter sender og leser tekst og vedlegg, med samme klient. Jeg bygger på korrespondansecellen og gir den chat-cellens levering. Chat-cellen selv har klartekst og ingen vedlegg.
2. **Tjeneren kan ikke lese innholdet og ikke slippe inn noen.** Den ser numrene på dem som skriver, når og hvor mye, og om en melding har vedlegg. Nøklene dine ligger på Macen din.
3. **Posten kommer av seg selv.** Klienten abonnerer på cellen (Flow) og får ny post uten å spørre. Historikken hentes med `get state`.
4. **Bare du slipper inn,** på Macen, med Touch ID eller passordet ditt. Ingen agent og ingen tjener kan gjøre det. Agenten din sender og leser fortsatt på ditt ja, som i dag.
5. **Få håndgrep.** Mottakeren: installere én signert pakke, gi agenten sin én lenke, sende deg koden. Du, per person: lage lenken, sende pakken og lenken, sammenligne koden, godkjenne. Ingen adminside, ingen miljøfil og ingen omstart av staging, heller ikke ved fornyelse.
6. **Vedlegg i samme pakke,** begge veier. Installerpakken og budsjettet går som vedlegg.
7. **Den gamle kanalen står** til begge er over. Tilgangene der gjelder til 05.11. Er det nye ikke ute da, må den fornyes én gang til.

Prisen for punkt 2 og 4: Macen din må være på når du godkjenner, og mister du nøkkelen, må cellene opprettes på nytt.

## Det du får se før pakken sendes

Prøveparet: melding og vedlegg begge veier mot staging, med programmet fra pakken, og en utskrift fra staging uten innhold i klartekst, uten navn og uten nøkkel. Pakken: én fil, signert og notarisert, og et skjermopptak fra en ren Mac der håndgrepene er telt. Macen din på den nye klienten. Til slutt: Vegars og Victorias egne ord om at melding, installerpakke og budsjett kom fram.

## Hvem gjør hva

Codex: cellen i CellProtocol, ut i en utgivelse først, og klienten. Kortet på Macen og oppsettet hører til klienten, og pakken bygget Codex også sist. Si fra hvis du vil ha det annerledes. Denne tråden: staging og prøvene. Kø-tråden og bro-tråden: broen. Det Codex skriver, gjennomgås av Fabel. Det jeg skriver, gjennomgås av Astra. Figuren `figur/leddene-v3.png` viser leddene.

Første ledd er en liten prøve hos Codex av punkt 4, lokalt: en avtale signert på én maskin slipper inn et medlem i en celle som kjører på en annen. Holder den ikke, kommer jeg tilbake til deg før noe annet bygges. Tid: jeg har ikke et tall jeg kan stå for før den prøven er gjort. Anslaget fra 06.10 (fem til ni uker, tre til fem i to løp) gjaldt en annen modell og er ikke kontrollert.

## Det du gjør senere

Ja til planen, og til merge og utsetting når jeg ber om det. Installere pakken på Macen din. Per person: lage lenke, sende, sammenligne kode, godkjenne. Si hvilken installerpakke og budsjettfil som skal sendes, og hvem som skal ha budsjettet. Til slutt: si når de gamle tilgangene kan trekkes.
