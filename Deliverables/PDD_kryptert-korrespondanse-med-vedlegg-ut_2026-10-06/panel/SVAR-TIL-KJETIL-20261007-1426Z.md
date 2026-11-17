**Ført nå:** G1 og bildene er godkjent (07.10), i `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/STATUS.md`. Bildene viser koden på seks sifre, så jeg leser det som ja til koden. Vegar og Victoria har fortsatt ikke fått noe nytt.

**Assistentidentiteten (punkt 2).** Uten den skriver agenten din med din korrespondanseidentitet, bare på ditt ja (en regel, ikke en lås), og Vegar kan ikke kontrollere kryptografisk om det er du eller agenten som har skrevet. Med den (Book 33 §4.3) får agenten egen identitet og nøkkel, og en fullmakt fra deg med formål og utløpsdato. Hver melding viser til fullmakten, så mottakeren kan kontrollere både hvem som skrev, og hvem som står bak. Du kan trekke fullmakten uten at historikken forsvinner. Du bestemte 01.09 at én slik identitet skal avløse en profil per motpart. Den fantes ikke i koden da jeg sjekket 06.10.

**Vedlegg og `main` (punkt 3).** Dårlig stilt av meg. Jeg mente koden som gjør vedlegg mulig, ikke vedleggene. Ingen vedlegg lagres i git: filene skal ligge kryptert på staging og fjernes ved utløp eller tilbakekall. Koden ligger på en egen gren. Den er testet lokalt, ikke gjennomgått, og lar ennå ikke deg sende vedlegg, bare den inviterte. En installerpakke kan bare bygges fra hovedgrenen (`main`). Vedleggs-PDD-en sier at Vegar og Victoria skal ha prøvd vedlegg før koden går dit, og de kan ikke prøve uten en pakke.

**Punkt 5, slik jeg leser det:** fornyelsen av den gamle kanalen sendes ikke til Vegar og Victoria. Du skrev «teste», ikke «fornye», så si fra i dag hvis jeg leser feil. Lesningen snur valget ditt 06.10 («Forny, jeg bytter selv») og punkt 7 i det du godkjente i dag. Følgen: Vegars tilgang der går ut i morgen, og Victorias er alt ute. Etter det har ingen av dem tilgang i korrespondansekanalen før den nye er ute, og jeg har ikke et tall for når det er. Varsel på skjermen, vedlegg som referanse eller hent ved behov, og sikkerhetskopi av nøkkelen blir ikke med i første pakke, slik spørsmål 5 sa.

**Tre ja eller nei fra deg:**

- **A.** Venter assistentidentiteten til etter første pakke? Anbefalt: ja. Pakketeksten sier da at det ikke kan etterprøves kryptografisk hvem som står bak en agent. Book 33 §10 krever den før en pakke sendes ut, så det trengs ditt ord. Nei betyr anslagsvis en til to uker mer og en egen gjennomgang (mitt anslag, ikke kontrollert).
- **B.** Kan koden for vedlegg slås sammen med hovedgrenen før Vegar og Victoria har prøvd, når funksjonsprøvene, en uavhengig gjennomgang (Fabel) og en lokal formålsprøve med to prøveidentiteter er grønne? Anbefalt: ja. Det må til for å holde valget ditt 06.10, «Kryptert og vedlegg samlet» (min slutning). Selve sammenslåingen får eget ja fra deg. Nei betyr to pakker: først uten vedlegg.
- **C.** Kan Codex starte første ledd nå, før planen er godkjent? Det er en liten prøve, lokalt: en avtale signert på én maskin slipper inn et medlem i en celle som kjører på en annen. Bestillingen sier at ingenting skal til hovedgrenen. Holder ikke prøven, kommer jeg tilbake til deg før noe annet bygges. Nei betyr at prøven venter til planen er godkjent.

Svar gjerne «A ja, B ja, C ja».

**Ett spørsmål til:** hvilke Macer har Vegar og Victoria (Intel eller Apple-prosessor, og macOS-versjon)? Det sto i meldingene som nå ikke sendes.

**Imens** skriver jeg planen (G2). Bestillingen til Codex gjelder først når du har sagt ja til C. Lest i koordineringsfila nå: kø-tråden venter på ditt ja til å merge PR #60 og #61 og tagge CellProtocol `2026.9.5`. Den utgivelsen har broen (#53), som den nye korrespondansen går over. Har du svart der, se bort fra det.

Lest mot kildene av en uavhengig leser (Claude Opus) før sending. Rettelsene etter kontrollen er ikke lest på nytt.
