# Vedlegg i korrespondansen — formål før implementasjon

Dato: 2026-09-28. **G1-forslag til Kjetil. Ikke godkjent for implementasjon.**

Formålet er at mottakeren får det materialet som trengs for å gjøre arbeidet: motta og kunne bruke installerpakken, og motta og kunne bruke budsjettet. At korrespondansen har en vedleggsfunksjon er et eget, nødvendig delmål. Det beviser ikke at disse oppgavene blir løst.

**Anbefaling til vurdering:** Første versjon leverer én bestemt filversjon per melding. Meldingen inneholder en signert, kryptert beskrivelse av filen; bytene overføres separat som en kryptert strøm. Midlertidige leveringskopier følger meldingens utløp. Mottakeren kan beholde en egen kopi bare gjennom et uttrykkelig lagringsvalg som avtalen tillater. Dette er en anbefaling, ikke en eksisterende kapabilitet.

Les formålstreet og eiervalgene nedenfor. Målinger, kildehenvisninger og usikkerheter står i [STATUS.md](STATUS.md). Oppdraget gjengis ordrett til slutt, slik at formålet kommer først.

## §1 Formålstreet og hva som teller som oppnådd

```text
R: Mottakeren får brukt materialet til avtalt arbeid
├── A: Vedlegg finnes i korrespondansen
│   └── F1: En melding kan levere én navngitt fil
├── B: De konkrete leveransene kan fullføres
│   ├── F2: Vegar og LilleRobot får brukt installerpakken
│   └── F3: Budsjettmottakeren får brukt riktig budsjettversjon
└── C: Partene beholder oversikt og kontroll
    ├── F4: Det er tydelig hvilken kilde og versjon filen kommer fra
    ├── F5: Lagring, utløp og opprydding har en ansvarlig
    ├── F6: Partene kan ta et informert valg før filoverføring
    └── F7: Filen kan verifiseres mot avsender, melding og avtale
```

F-numrene er lokale navn i dette forslaget. De oppretter ingen nye `purpose://`-referanser. R/A/B forankres i eksisterende `purpose://digital-work.coordinate` og `purpose://contact.communication`; C i `purpose://access.audit.privacy`. Testene forankres i `purpose://test.acceptance`. Dette endrer ikke det kanoniske formålsregisteret og gir ingen rettigheter.

| Formål | Hva det innebærer | Målt utgangspunkt | Foreslått målbart resultat | Verifikasjon og frist |
|---|---|---|---|---|
| F1 — Vedlegg finnes | Filen henger på én melding, med en synlig beskrivelse og eksplisitt henting. | 0 vedleggstreff i 8 MCP-kildefiler; ingen slik verktøyflate funnet. Ingen funksjonstest kjørt. | 1 melding med 1 fil kan sendes, leses og hentes; mottatt hash er lik valgt kildeversjon. | T1, før G3 og før noe går mot main. |
| F2 — Installerleveransen lykkes | Hver tiltenkt mottaker får riktig pakke og kan bruke den. Nedlasting starter aldri installasjon automatisk. | Stoppet leveranse er opplyst av eieren; antall forsøk og pakkestørrelse er ikke målt her. | 2 av 2 mottakere får verifisert pakke uten alternativ filkanal og kan starte avtalt installasjonsløp etter eget valg. | T2, med Kjetils valgte pakke og mottakere før G3. Installasjonstest krever egen autorisasjon. |
| F3 — Budsjettleveransen lykkes | Mottakeren kan bruke riktig budsjett til det arbeidet eieren faktisk mener. | Stoppet sending er opplyst av eieren; bruk, mottaker og filformat er ikke fastlagt her. | 1 av 1 mottakere åpner riktig versjon i avtalt program og bekrefter at den kan brukes til valgt oppgave. | T3, før G3. Kjetil velger lesing/beslutningsgrunnlag eller videre redigering ved G1. |
| F4 — Én autoritativ kilde er tydelig | En leveringskopi blir ikke en konkurrerende original. | Kilde og versjon for de to leveransene er ikke undersøkt. | 100 % av testleveransene har kilde/versjon eller eksplisitt «lokal fil», hash og begrunnelse for kopiering. Ingen ny redigerbar original opprettes automatisk. | T4, før G3. |
| F5 — Lagring og utløp kan etterprøves | Det er kjent hvem som oppbevarer hva, og hvem som rydder. | Meldingsutløp finnes i kildekoden; vedleggslivsløp finnes ikke i undersøkt integrasjon. | 0 vellykkede hentinger etter utløp; alle administrerte kopier slettes innen avtalt frist. Bevarte kopier har separat lagringsvalg og ansvarlig. | T5, med styrt klokke, avbrudd og omstart før G3. |
| F6 — Valget tas før bytene sendes | Avsender får tidlige størrelsesfeil; mottaker ser hva som tilbys. | Ingen vedleggsmetadata eller vedleggskvote i undersøkt flate. | Alle kjente størrelses-/kvoteavslag skjer med 0 overførte filbyte. Navn, oppgitt type, størrelse, hash og utløp vises med 0 hentede filbyte. | T6, før G3; metadataoverføring telles separat. |
| F7 — Riktig fil, riktig sammenheng | Autentiserte chunks må også høre til denne meldingen og avtalen. | Chunk-autentisering finnes; korrespondansebinding for vedlegg mangler. | Alle planlagte negative tilfeller i T7 avvises; ingen ufullstendig eller feilbundet fil presenteres som verifisert. | T7, før G3. |

A er oppnådd når F1 er oppnådd; B krever både F2 og F3; C krever alle F4–F7. R krever A, B og C. En grønn kryptotest alene oppfyller derfor ikke R. Produktmålene er **ikke testet**, og videre gjennomføring avventer eierens valg. Denne jobbens mål er et kontrollerbart G1-grunnlag, målt ved D0 i §5.

## §2 De seks valgene som bestemmer løsningen

### 1. Hva er et vedlegg? — D1

**Anbefalt: en uforanderlig filversjon.** En referanse i meldingen identifiserer leveringsobjektet; strømmen er måten bytene fraktes på. En strøm uten kjent slutt og størrelse er ikke omfattet av første versjon.

| Alternativ | Hva du får | Hva du må akseptere |
|---|---|---|
| Filversjon, anbefalt for disse leveransene | Mottakeren får nøyaktig pakken eller budsjettversjonen som ble sendt, også når avsenders maskin er frakoblet etter levering. | Det lages kopier. Kopieringen må ha formål, levetid og opprinnelse. |
| Referanse til eksisterende kilde | Materialet blir hos sin nåværende eier; passer et budsjett som fortsatt skal redigeres sammen. | Kilden må gi mottakeren tilgang og tilstrekkelig tilgjengelighet. En levende referanse kan vise andre byte neste gang. En versjonslåst referanse krever at kilden faktisk støtter det. |
| Åpen strøm | Materiale kan produseres mens det sendes. | Full størrelse og hash kan ikke vises på forhånd. Det trenger en annen kontrakt og er utenfor anbefalt første versjon. |

**Én source of truth:** Dersom filen allerede bor i en celle eller et arkiv, er denne kilden fortsatt autoritativ for dokumentet eller utgivelsen. Leveringsobjektet er et datert, uforanderlig eksemplar med kildehenvisning, versjon hvis tilgjengelig og hash. En ny budsjettendring skjer i originalkilden, ikke i leveringsobjektet. Originale lokale filstier skal ikke røpes til mottakeren.

Dette er fortsatt duplisering av byte. Begrunnelsen som foreslås er «mottakeren trenger en fast versjon som kan hentes uten at avsender er tilkoblet». Hvis eksisterende kildetilgang allerede løser dette, bør den brukes, og kopieringen kan falle bort. Det er ikke undersøkt for de aktuelle filene.

**Kjetil avgjør:** Er en fast leveringskopi riktig for begge leveransene, og er denne kopieringsgrunnen god nok? Hvis budsjettet skal være et felles, levende dokument, må F3 og løsningen endres før implementasjon.

### 2. Hvem lagrer bytene? — D2

**Anbefalt: kryptert leveringslager under den eksisterende relasjonscellens ansvar.** Kildekoden bruker en felles `CorrespondenceCell` for relasjonen, ikke en dokumentert overlevering mellom en avsendercelle og en mottakercelle. Valget her er derfor å la verten for denne cellen oppbevare den krypterte leveringskopien. Et slikt vedleggslager er nytt arbeid, ikke noe kildekoden allerede tilbyr.

| Sted | Hva lagres | Hvem rydder og når — foreslått regel |
|---|---|---|
| Avsenders kilde | Den opprinnelige filen. | Kildeeieren etter kildens regler. Sending endrer eller sletter aldri originalen. |
| Avsenders lokale klient | Midlertidig, frosset kildeversjon ved behov og krypterte opplastingsdata. | Klienten etter bekreftet lagring eller avbrudd; senest ved kladdens frist. |
| Relasjonscellens vert | Én kryptert leveringskopi per vedlegg; ingen klartekstnøkkel. | Vertens vedleggslager etter meldingens utløp. Ufullførte opplastinger har egen kladdefrist. |
| Mottakers klient | Privat, administrert arbeidskopi under henting og verifikasjon. | Klienten ved feil/avbrudd; ellers ved meldingens utløp, eller tidligere etter lagring/bruk. |
| Mottakers valgte filområde | Bare en uttrykkelig bevart kopi, dersom avtalen tillater det. | Mottakeren etter eget, synlig lagringsvalg, jf. D3. |

Forslag til frister: kladd/reservasjon utløper etter **1 time**, uten automatisk forlengelse. Etter utløp sperres tilgang straks; sletting av administrerte data skjer innen **24 timer på en kjørende vert/klient**, og innen **5 minutter etter neste oppstart** hvis den var avslått. Døde prosesser og frakoblede maskiner kan ikke love sletting på klokkeslettet. Aktiv lagring, midlertidige filer og eventuelle sikkerhetskopier må inngå i lagringsplanen; et ukjent backup-regime er et åpent hull, ikke dokumentert sletting.

Alternativet «avsender beholder alt til mottaker henter» reduserer serverlagring, men gjør levering avhengig av avsenders tilgjengelighet. Automatisk varig lagring hos begge gir flere kopier og uklart ansvar. Ingen av delene anbefales som standard.

**Kjetil avgjør:** Kan relasjonscellens vert få dette lagringsansvaret, og er fristene akseptable? Verten, diskbudsjettet og backup-reglene må navngis i neste plan.

### 3. Hva betyr `retentionSeconds`? — D3

**Anbefalt: Vedleggets administrerte leveringskopier får samme absolutte `expiresAt` som meldingen.** Ingen egen vedleggsteller forlenger dette. Tiden regnes fra publisering av meldingen, ikke fra påbegynt opplasting. `ack_message` er en meldingskvittering; den betyr verken «alle vedlegg er hentet» eller «slett dem nå».

Pågående henting stoppes ved utløp, og arbeidskopien ryddes. Et bevaringsvalg må være fullført mens filen og tilgangen fortsatt er gyldige. Tilgang og avtale kontrolleres på nytt ved publisering og henting; en vellykket forberedelse er ikke et varig tilgangsbevis.

Kildekodens standard for meldinger er 30 dager, med maksimum 90 dager. Dette er en måling av standardpolicyen, ikke en bekreftelse på innstillingene i den kjørende tjenesten. Et kortere tillatt tidsrom skal gjelde også for vedlegget.

Mottakeren må kunne velge **«Behold en egen kopi»** for å bruke for eksempel installerpakken etter at korrespondansen utløper. Anbefalingen er å tillate dette for de to bestilte leveransene gjennom en uttrykkelig avtale. Bevaring er et eget valg, med egen mottakerstyrt plassering og kilde-/versjonsopplysning. Den bevarte kopien overlever meldingens utløp; originalkilden forblir originalkilden.

Hvis avtalen ikke tillater bevaring, skal verktøyet avvise slik lagring. Teknisk kan man ikke tilbakekalle klartekst som en mottaker allerede har kopiert utenfor klienten. Løftet gjelder derfor de administrerte kopiene, ikke alle mulige eksemplarer i verden.

**Kjetil avgjør:** Skal mottakeren få beholde filen etter utløp? Anbefalt ja for disse leveransene, ved uttrykkelig valg. Hvis nei, må vi prøve om installer- og budsjettformålet fortsatt kan oppnås.

### 4. Hvor går grensen? — D4

**Anbefalt utgangspunkt til måling:** én fil per melding, høyst **100 MiB = 104 857 600 klartekstbyte**, og høyst **1 GiB = 1 073 741 824 byte med reservert/lagret vedleggsdata per relasjon**. Relasjonskvoten må regnes på faktisk lagringsformat, inkludert kryptering og innramming. Vertens samlede diskgrense kommer i tillegg. Tallene er foreslåtte produktgrenser, ikke målte kapasiteter.

Før en filbyte sendes, kontrollerer klienten den valgte, faste kildeversjonens faktiske størrelse. Tjenesten kontrollerer støtte, avtale, levetid og ledig kvote og reserverer nødvendig plass. Et størrelsesavslag skal oppgi faktisk størrelse, tillatt størrelse og at **ingen filbyte er sendt**. Manglende støtte hos mottakeren skal også oppdages her; filen skal ikke smugles inn som base64 i `content`.

Ved sendekallet må også tekst, manifest og samsvar med forberedelsen valideres før opplastingen starter. En gyldig fil skal ikke lastes opp først for deretter å bli avvist på grunn av en på forhånd kjent tekst- eller metadatafeil.

En ukjent størrelse eller en kilde som endres under forberedelsen avvises før opplasting; den må først gjøres til en stabil filversjon. Kilden hashes lokalt før overføring. Underveis håndheves også faktisk byteantall. Nettbrudd, tilbakekalt tilgang eller feilaktig avsender kan fortsatt føre til avbrudd etter start; det må gi en tydelig feil og opprydding, aldri en halv fil markert som levert.

Den oppgitte **16 KiB-grensen for `content` er ikke gjenfunnet i den undersøkte kodeveien**. Den beholdes som krav/premiss for tekst i forslaget, separat fra vedleggsgrensen. Hvilken kjørende komponent som håndhever den må avklares. Metadata trenger dessuten et eget, begrenset budsjett; forslag: maksimalt 8 KiB for vedleggsbeskrivelsen, målt i det avtalte byteformatet før sending.

**Kjetil avgjør:** Er én fil per melding nok i første versjon? 100 MiB er bare en kandidat inntil de faktiske pakkene og budsjettet er størrelsesmålt. Hvis en bestilt fil er større, kan dette forslaget ikke sies å løse bestillingen. Dagens `open` holder hele klarteksten i minnet; grensen kan ikke godkjennes som driftskapasitet uten minnemåling eller særskilt godkjent arbeid med filbasert dekryptering.

### 5. Hva får mottakeren vite før nedlasting? — D5

**Anbefalt:** Etter eksplisitt lesing av meldingen vises avsender og signaturstatus, visningsnavn, oppgitt medietype, eksakt klartekststørrelse, SHA-256, kilde/versjon når tilgjengelig, utløp og om egen kopi er tillatt. Ingen filbyte hentes for å vise dette. En vedleggsbeskrivelse kalles her et **manifest**.

Manifestet ligger inne i den signerte og krypterte meldingen. Filnavn og hash skal ikke legges i en offentlig URL, serverlogg eller ukryptert innboksliste. Verten vil fortsatt kunne se nødvendig ruting og kryptert størrelse; forslaget lover ikke å skjule trafikkmønsteret.

Medietype og navn er avsenderopplysninger, ikke en attest på trygt innhold. En verifisert signatur beviser avsenderbinding, ikke at en installer er ufarlig. Klienten henter, åpner, pakker ut eller kjører ingenting automatisk. Filnavn brukes til visning; mottakerens uttrykkelige lagringsvalg bestemmer filstien.

**Kjetil avgjør:** Er metadata etter «les melding», men før «hent fil», riktig nivå? Anbefalt ja. Metadata allerede i innbokslisten vil kreve et annet personvernvalg.

### 6. Hva binder filen til akkurat denne meldingen og avtalen? — D6

**Anbefalt: signert manifest i den krypterte meldingen, med hemmelig strømnøkkel der inne.** `AttachmentStreamV1` gjenbrukes for chunk-kryptering og autentisert slutt. Den har ikke felter for melding eller avtale og distribuerer ikke nøkkelen selv.

Manifestet må binde sammen:

- reservert endelig `messageID`, `clientMessageID` og unikt `attachmentID`;
- `cellID`, medlemsfingeravtrykk og fingeravtrykk av den nøyaktige, signerte avtaleversjonen;
- avsenders domeneidentitet og signeringsnøkkel, formål, avtalte lagringsrettigheter og absolutt utløp;
- navn, type, eksakt størrelse, klarteksthash og hash av den komplette krypterte strømmen, inkludert header og avsluttende chunk;
- strømmens header og en ny hemmelig innholdsnøkkel for akkurat denne strømmen.

Alle feltene må omfattes av avsenderens signatur og den indre krypteringen. Hashene må beregnes over et fast, versjonert byteformat. En løs hash ved siden av meldingen gir ikke denne bindingen. Den hemmelige nøkkelen skal aldri returneres til språkmodellen eller legges i logger. Mottakernøklene må fortsatt kontrolleres mot signert avtale.

**Et konkret gap:** I dag lager cellen `messageID` først når den mottar den ferdig krypterte meldingen. Forslaget krever at cellen reserverer endelig ID før forsegling. Når opplastingen er komplett, fastsetter cellen publiseringstid og utløp i en kort sluttreservasjon. Klienten signerer disse verdiene i manifestet; cellen publiserer bare den tilhørende reservasjonen. Hvis sluttreservasjonen utløper, må sluttforseglingen gjøres på nytt før publisering. Dette er foreslått kontraktsarbeid, ikke implementert atferd.

Mottakeren verifiserer signatur, ID-er, celle, avtaleversjon og utløp før henting. Etter henting kontrolleres kryptert hash, alle chunks og autentisert slutt, eksakt lengde og klarteksthash. Bytte til en annen melding eller avtale skal feile selv om bytene og strømnøkkelen ellers er gyldige. Gjentatt samme sending skal finne samme resultat; endret innhold med samme idempotens-ID skal avvises. Historisk avtaleversjon dokumenterer hva som ble sendt; gjeldende tilgang må i tillegg kontrolleres ved hver henting.

**Kjetil avgjør:** Godtas denne ekstra meldings-/avtalebindingen og ID-reservasjonen som nødvendig del av kapabiliteten? Anbefalt ja. Den kryptografiske byggesteinen alene beviser ikke F7.

## §3 Verktøyflate og forventet brukerforløp

Dette er lesbare **forslag til signaturer**, ikke Swift, JSON-skjema eller tilgjengelige verktøy. `ID`, `String` og `Int` angir tekst og heltall; `?` betyr valgfritt. Filreferansene nedenfor er lokale, uttrykkelig godkjente filvalg som klienten må kunne løse opp. Et eksisterende slikt filvalgs-API er ikke påvist. Støtte for det er en avhengighet, ikke en antakelse om fri tilgang til filsystemet.

Anbefalt kobling: **nytt valgfritt felt `preparedAttachmentID` på `correspondence_send_message`.** Forberedelse gir ingen synlig melding. Publisering knytter tekst og ferdig vedlegg sammen i én operasjon. Å legge til et vedlegg i etterkant av en publisert `messageID` ville endre det mottakeren allerede har fått; det velges derfor bort. Rettelse sendes som ny melding.

| Verktøy og foreslått signatur | Resultat og virkning |
|---|---|
| `correspondence_prepare_attachment(relationshipID: ID, sourceFileRef: ID, clientMessageID: ID, copyReason: String, purposeRef: String?, retentionSeconds: Int?)` | Kontrollerer filvalg, fast versjon, størrelse, hash, avtale, støtte og kvote før nettverksopplasting. Returnerer `preparationID`, `preparedAttachmentID`, `reservedMessageID`, metadata, effektive grenser og `reservationExpiresAt`. Reserverer plass og lokal kladd; sender ingen filbyte til mottakertjenesten. |
| `correspondence_send_message(relationshipID: ID, content: String, subject: String?, purposeRef: String?, clientMessageID: ID?, retentionSeconds: Int?, preparedAttachmentID: ID?)` | Med vedlegg kreves samme `clientMessageID`, relasjon, formål og levetid som forberedelsen. Starter kryptert opplasting og publiserer først etter komplett lagring og sluttforsegling. Returnerer `operationID` og status; `messageID` og `expiresAt` blir endelige ved `stored`. Vanlig tekstsending beholdes. |
| `correspondence_fetch_attachment(relationshipID: ID, messageID: ID, attachmentID: ID, clientTransferID: ID)` | Henter på mottakerens uttrykkelige valg til privat, administrert klientlager. Returnerer `operationID`; først etter full verifikasjon returneres `verifiedFileRef`, størrelse og hash. Ingen base64-fil i MCP-svaret. |
| `correspondence_save_attachment(verifiedFileRef: ID, destinationFileRef: ID, clientSaveID: ID)` | Beholder verifisert fil på mottakerens valgte sted hvis avtalen tillater det. Returnerer lagringskvittering med kilde/versjon og beskjed om at denne kopien har eget livsløp. Verken overskriving eller installasjon følger automatisk. |
| `correspondence_attachment_status(operationID: ID)` | Returnerer status, bytefremdrift, feil og eventuelt endelig meldings-/filreferanse, bare til autorisert part. Skiller `prepared`, `uploading`, `stored`, `downloading`, `verified`, `failed`, `cancelled` og `expired`. |
| `correspondence_cancel_attachment(operationID: ID)` | Avbryter egen ufullført forberedelse/overføring og frigjør reservasjon og midlertidige data. Trekker ikke tilbake en publisert melding eller mottakerens bevarte kopi. |

`preparationID` er også status-/avbruddshåndtak for forberedelsen. Lange operasjoner må gi håndtak og kunne følges etter tidsavbrudd i MCP; gjentatt kall med samme klient-ID og samme innhold skal returnere eksisterende operasjon, ikke ny levering. Gjenopptak bruker allerede forseglet ciphertext; ny kryptering betyr ny strøm og ny nøkkel. Flytting av store filer må ikke kreve ett MCP-kall per chunk.

Eksisterende `correspondence_read_message(relationshipID, messageID)` foreslås utvidet til å returnere den verifiserte vedleggsbeskrivelsen uten filbyte eller nøkkel. `list_inbox` og meldingskvitteringen får ingen skjult nedlasting. Tekst, vedleggsmanifest og faktisk byteoverføring har separate grenser.

**Navneavvik som må løses:** Den tilkoblede verktøydeklarasjonen bruker `recipientID`; undersøkt HavenAgentD-kilde bruker `relationshipID`. Forslaget følger kildekodens relasjonsscope. Ingen automatisk oversettelse antas: valgt klientversjon og eventuell kompatibilitetsregel må dokumenteres før implementasjon.

Verktøyenes navn gir ingen tilgang. Dagens klient krever nøyaktig fire avtalte cellehandlinger. Nye opplastings-/hentehandlinger og eventuell varig bevaring trenger en uttrykkelig, versjonert tilgangskontrakt, håndhevet i resolver/celle. Gamle avtaler utvides ikke automatisk. Verken en filreferanse, et `operationID` eller `purposeRef` er et tilgangsbevis.

For avsender blir forløpet: velg fil → se kildeversjon, størrelse, mottaker og levetid → send → få bekreftelse på lagret melding. For mottaker: les melding og manifest → velg henting → få verifisert fil → velg eventuell bevaring → åpne eller installer etter eget valg. Dette er funksjonelt forløp, ikke et godkjent GUI-design.

**Leveranser i denne jobben:** [FORMAALSSPEC.md](FORMAALSSPEC.md) er beslutningsgrunnlaget; [STATUS.md](STATUS.md) viser evidens og begrensninger. Ingen kjørende flate, ny kontraktfil, kildekode, commit eller push inngår.

## §4 Avgrensning, avhengigheter og relevante lærdommer

Første forslag omfatter én fil per melding i eksisterende, autorisert relasjon. Gruppeutsending, levende dokumentredigering, åpne strømmer, forhåndsvisning av filinnhold og automatisk installasjon inngår ikke. Et nytt GUI må eventuelt få eget G1-GUI-grunnlag. Denne jobben oppretter ingen skjemaer eller kanoniske formålsnoder.

| Avhengighet | Hva er funnet / hva mangler | Hva må verifiseres før gjennomføring |
|---|---|---|
| Kryptering | Strømkrypto og meldingskrypto finnes, men ingen integrert vedleggsbinding. | T7 og gjennomgang av nøkkeldistribusjon; minne-/kapasitetsmåling i T6. |
| Riktig kjørende klient | Kilde og tilkoblet deklarasjon har ulike selektorer. Utsjekket og main har ulike avhengighetspinner. | Valgt binær, verktøyskjema og CellProtocol-revisjon må navngis; gammel mottaker må avvises før opplasting. |
| Relasjon og rettigheter | Dagens fire handlinger og signerte medlemsnøkler er kildekontrollert. Vedleggslagring og bevaring er ikke hjemlet som nye handlinger. | Ny avtaleversjon med avgrensede rettigheter; positiv og negativ tilgang gjennom faktisk resolvervei. |
| Lagringsvert | Meldingscellen lagrer konvolutter. Vedleggslager, kvoter og tidsstyrt rydding er ikke påvist. | Navngitt vert og ansvarlig, disk-/backup-policy og T5. |
| Lokale filvalg | Ingen filinngang/-utgang finnes i undersøkt MCP-flate. | Autorisert lokal filtilgang, trygg målplassering og ingen filbyte/nøkler i modellkontekst eller logger. |
| De faktiske leveransene | Bestillingen er kjent; filene og bruken er ikke undersøkt. | Eier velger kildeversjoner, størrelse, budsjettbruk og passende mottakertest. Ingen privat filleting eller prøvesending er gjort her. |

PDD-oppslaget festet `pkg.std.everything-works`, `pkg.std.cell-contract`, `pkg.std.cell-combination` og `pkg.std.codex-handoff`. I G1 brukes kravene til synlig status, kildekontroll og avledede tester. Bygg/regresjon, kontrakt-fixtures, dataflytartefakt og kjørbar overlevering hører til en senere autorisert fase. De er ikke utført eller levert her.

Lærdommene som konkret påvirker forslaget:

- «G1 godkjenner formål, ikke arbeid» (`lesson.plan-instead-of-delivery`): denne bestillingen er nettopp G1-materiale; en senere levering må oppfylle F2/F3.
- «Planlagt oppførsel merkes eksplisitt» (`lesson.planned-documented-as-implemented`): alle nye verktøy, kvoter og frister er forslag.
- «Brief-audit skal si HVILKEN revisjon noe ble lest fra» (`lesson.read-origin-main-before-writing-a-mechanism`): STATUS skiller main, arbeidskopi og kjørende deklarasjon.
- «Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en» (`lesson.purpose-never-grants-rights`): gamle avtaler gir ingen automatisk vedleggstilgang.
- `lesson.corr-approval-surfaces-timed-out` og `lesson.tested-a-different-path-than-production`: relasjon, klient og autorisasjon må virke før reell mottakertest; simulert kryptotest er utilstrekkelig.

## §5 Plan for å prøve funksjon og formål

Dette er en prøveplan til G1, ikke en igangsatt implementeringsplan. Alle T-testene **venter**. Først fastsettes D1–D8. Deretter utarbeides en G2-plan med kontrakter og arbeidsrekkefølge, og først etter særskilt autorisasjon kan noe implementeres. Funksjonsprøvene og de to mottakeroppgavene må begge bestå før noe foreslås mot main.

| Test / formål | Hvordan det senere skal prøves | Evidens som må foreligge |
|---|---|---|
| D0 — Denne dokumentjobben | Kontroller to filer, formål/mål, alle seks spørsmål, signaturer, åpne eiervalg og skille mellom målt og antatt. Kontroller lokale lenker og PDD-portstatus. | Faktisk dokumentkontroll i STATUS. |
| T1 — F1 | Send én godkjent testfil via faktisk klient/celle/MCP-vei; les metadata, hent og sammenlign hash. Prøv også ren tekst med gammel klient. | Senere `TESTRESULT.md`, med revisjoner og overføringsresultat. |
| T2 — F2 | For hver av de to mottakerne: finn meldingen, forstå vedlegget, hent, verifiser og start avtalt installasjonsløp under separat tillatelse. Registrer fullføring og behov for hjelp/annen kanal. | Senere `ACCEPT.md`: 2 av 2 konkrete mottakerresultater. «Sendt» alene er ikke bestått. |
| T3 — F3 | Bruk eierens faktiske, valgte budsjettversjon i avtalt program. Mottakeren utfører den oppgaven eieren valgte ved G1. Hvis videre redigering krever en annen kilde, registreres det som formålsgap. | Senere `ACCEPT.md`: 1 av 1 oppgaver fullført, versjon og resultat. |
| T4 — F4 | Send fra eksisterende kilde og fra lokal fil. Endre originalen etterpå. Bekreft at leveringsversjonen er uendret, har proveniens og ikke utgir seg for å være ny original. | Senere `TESTRESULT.md`: kilde, versjon, kopieringsgrunn og begge hasher. |
| T5 — F5 | Prøv uhentet, hentet, bevart, avbrutt og foreldreløs opplasting. Flytt klokken over utløp, start klient/vert på nytt og trekk tilgang tilbake. Kontroller også at ack ikke sletter filen. | Senere `TESTRESULT.md`: tilgangsavslag og inventar av alle administrerte lagringssteder før/etter frist. Backup-grensen må fremgå. |
| T6 — F6 | Mål faktiske bestillingsfiler, minnetopp og diskbruk. Prøv 0 byte, grensen og grensen + 1 byte, full kvote, to samtidige reservasjoner, endret kilde og gammel klient. Les manifest uten å hente fil. | Senere `TESTRESULT.md`: faktisk byteantall før avslag (0), synlige metadata, minne og tidsbruk. Tom fil kan leveres, men består ikke F2/F3. |
| T7 — F7 | Prøv endret chunk/header/manifest, manglende slutt, feil hash/lengde, hel strøm fra annen melding, annen avtale med samme medlemmer, feil celle/identitet, utløpt/tilbakekalt grant og gjenbruk av klient-ID med endret innhold. | Senere `TESTRESULT.md`: hvert tilfelle avvist på faktisk tilgangs-/hentevei, ingen fil vist som verifisert; sjekk av logger for nøkkel/filinnhold. |

Eksisterende kryptotester kan gjenbrukes som regresjonsgrunnlag, men er ikke kjørt i denne jobben. T2/T3 må prøves med eierens konkrete materiale og godkjente mottakere; syntetiske småfiler beviser ikke at bestillingen er løst.

## §6 Det Kjetil må ta stilling til før implementasjon

| Valg | Anbefalingen du tar stilling til | Hva et annet svar endrer |
|---|---|---|
| D1 — Fast fil eller kildereferanse | Fast filversjon; begrunnet, tidsavgrenset leveringskopi. | Levende referanse krever kildeautorisasjon og andre tilgjengelighets-/versjonsmål. |
| D2 — Ansvar for bytene | Relasjonscellens vert lagrer kryptert; klienter har midlertidige kopier. Foreslåtte ryddefrister i §2. | Avsenderlagring gjør mottak avhengig av avsenders tilgjengelighet. |
| D3 — Liv etter meldingen | Samme utløp for administrert vedlegg; uttrykkelig tillatt bevaring hos mottaker for disse leveransene. | Forbud mot bevaring kan hindre normal bruk av installer og budsjett. |
| D4 — Omfang og grenser | Én fil per melding; 100 MiB/fil og 1 GiB/relasjon som kandidater. | Må endres hvis filstørrelser, minne eller vertskvote ikke støtter målene. Tall må verifiseres før de låses. |
| D5 — Innsyn før henting | Manifest ved lesing av meldingen; ingen filbyte eller offentlig metadata. | Synlig navn/hash i innboksen endrer personverngrensen. |
| D6 — Bevis og avtale | Signert manifest, avtaleversjon, reservert messageID og ingen automatisk utvidelse av gamle avtaler. | En svakere binding oppfyller ikke F7 slik det er formulert. |
| D7 — Meldingskobling og verktøy | Forbered → send med `preparedAttachmentID`; ingen ettermontering på publisert melding. Egen bevaringsoperasjon. | Ettermontering krever regler for endring, signering og hva en tidligere mottaker faktisk så. |
| D8 — Prøven som avgjør nytten | Navngi pakkene og budsjettfilen, og fastsett budsjettoppgaven. Godta kriteriene F2/F3 eller juster dem. | Hvis oppgavene er annerledes, må formålstreet endres før det blir en G2-plan. |

Ubesvarte valg blir stående som åpne, med Kjetil som beslutningseier. Særlig D1, D3 og D8 kan endre selve formålet. Et G1-ja er godkjenning av formålsgrunnlaget; denne jobben gir ingen implementasjons-, commit- eller push-autorisasjon.

## §7 Revisjonslogg

| Iterasjon | Dato | Endring | Ansvar |
|---|---|---|---|
| 1 | 2026-09-28 | Første G1-forslag. Skiller funksjon fra nytte; synliggjør selector-avvik, ubekreftet tekstgrense, minnebegrensning og manglende meldings-/avtalebinding. Ingen eiervalg registrert som godkjent. | Codex utarbeider; Kjetil avgjør. |

## §0 Oppdraget ordrett og kontroll av premissene

Faktapåstandene er kontrollert og klassifisert i [STATUS.md](STATUS.md). Eierens erfaring med stoppede leveranser behandles som opplyst behov, ikke som en test kjørt av Codex.

<details>
<summary>Vis den opprinnelige bestillingen</summary>

Vedlegg i korrespondansen. **Dette er første steg: formål og plan, ikke implementasjon.**
Ingen kode skal skrives i denne jobben. Ingen commit, ingen push.

Grunnen til at det stopper her: dette er en ny kapabilitet, og eieren krever at nye
kapabiliteter er prøvd mot både funksjon og formål før noe går mot main. Vi bommer oftere på
formålet enn på koden.

## Bakgrunnen, målt

- `Sources/HavenCorrespondenceMCP/` i HavenAgentD har **null** treff på «attachment» i alle åtte
  filene. Verktøyet `correspondence_send_message` tar bare `recipientID`, `subject`, `content`,
  `purposeRef`, `clientMessageID`, `retentionSeconds`. `content` er tekst med tak på 16 KiB.
- Krypteringen finnes allerede: `CorrespondenceEnvelopeClient` forsegler indre payload, signerer
  og verifiserer, og mottakernøkler hentes fra den signerte avtalen.
- `Sources/CellBase/Crypto/AttachmentStreamV1.swift` ligger på `origin/main` i CellProtocol:
  `AttachmentStreamHeader`, `AttachmentStreamChunk`, `EncryptedAttachmentStream`,
  `SealedAttachmentStream`, `sealChunk(_:)`, `finish()`. Autentiserte chunks med avslutning.

Byggeklossen finnes altså. Koblingen inn i korrespondansen finnes ikke.

Dette har stoppet to konkrete leveranser på fem dager: installerpakken til Vegar og LilleRobot,
og et budsjettvedlegg eieren ville sende. Det er bestillingen, ikke en øvelse.

## Skriv formålet først

Følg PDD. Formålstreet skal skille:

- at vedlegg skal finnes — ett formål
- hva vedlegg skal løse — andre formål, hver med et målbart resultat

Minst disse spørsmålene skal treet svare på, og de er ekte:

1. **Hva er et vedlegg her?** En fil, en strøm, eller en referanse til noe som ligger et annet
   sted? De tre gir helt ulike kontrakter. Husk eierens regel om én source of truth: et vedlegg
   som *kopierer* noe som allerede bor et sted, er en duplisering som må begrunnes.
2. **Hvem lagrer byten?** Avsenders celle til mottaker henter, mottakers celle etter levering,
   eller begge midlertidig? Hvem rydder, og når?
3. **Hva skjer med `retentionSeconds`?** Meldinger utløper. Utløper vedlegget med meldingen,
   eller lever det videre? Hvis videre — hvor, og hvem eier det da?
4. **Hva er grensen?** 16 KiB-taket gjelder `content`. Hva er taket for et vedlegg, og hva skjer
   når noen sprenger det? En feil som kommer etter at halve filen er sendt er en dårlig feil.
5. **Hva ser mottakeren før nedlasting?** Navn, type, størrelse, hash? Å måtte laste ned for å
   vite hva noe er, er et personvernproblem og et sikkerhetsproblem.
6. **Hva beviser at vedlegget er det avsenderen sendte?** `AttachmentStreamV1` autentiserer
   chunks. Hva binder strømmen til *denne* meldingen og *denne* avtalen?

Ikke svar på disse i prompten hvis du er usikker — skriv dem som åpne valg med det du mener er
riktig og hvorfor. Eieren avgjør.

## Verktøyflaten

Foreslå de MCP-verktøyene som trengs, med signaturer. Sannsynligvis noe som ligner
`correspondence_send_attachment` og `correspondence_fetch_attachment`, men navn og deling er
en del av forslaget, ikke gitt.

Vis hvordan et vedlegg henger på en melding: nytt felt i send-verktøyet, eller en egen
operasjon som refererer til `messageID`. Si hva du velger og hvorfor.

## Hva som ikke skal gjøres

Ingen Swift. Ingen skjemaendringer. Ingen commit. Dette er G1-materiale.

## Leveranse

`CellProtocolDocuments/Deliverables/PDD_vedlegg-korrespondanse_2026-09-28/FORMAALSSPEC.md`:
formålstreet med målbare mål, de seks spørsmålene med anbefaling og begrunnelse, forslag til
verktøyflate, og hva som må avgjøres av eieren før implementasjon.

Legg ved `STATUS.md` med hva som er målt og hva som er antatt, hver for seg.

Hold det forståelig. Eieren har sagt at formålsforslag ofte er vanskelige å lese — skriv hva
hvert punkt innebærer og hva han selv må ta stilling til.

</details>
