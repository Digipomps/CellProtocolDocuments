# Formålsspesifikasjon — kryptert korrespondanse med vedlegg, ut til Vegar og Victoria

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/` · Opprettet 2026-10-06 · Iterasjon 3 (**G1-forslag, ikke godkjent**)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

Skrevet av Claude-tråden i prosjektet «HavenAgentD». Den heter «korrespondanse-tråden» i `_losen-queue/KOORDINERING.md`, og kalles det her. Kø-tråden er en annen tråd.

**Slik leser du dette.** Vil du bare ta stilling, les `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/G1-KORT.md`. Det er den korte versjonen: fem spørsmål, sju punkter som skal være sanne, det du får se, og hvem som gjør hva. Her i den fulle spesifikasjonen står det samme i «Kort sagt» under og i §6. §1 er formålene. §3 er det du kommer til å se. §0 og §2 er grunnlaget og grensene. §4 og de første radene i §5 er lagt inn av verktøyet. Alle stier er skrevet fra HAVEN-mappen. Fagord er forklart i ordlista under. Iterasjon 2, med de fem valgene, ligger i `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/iterasjon-2/`.

**Kort sagt (iterasjon 3).** Bygger på ordene dine 06.10 kl. 20:03Z og de to svarene dine 07.10 (§0).

1. **Dere skriver til hverandre, kryptert.** Du og Vegar har én celle, du og Victoria en annen. Du eier dem og er med som deltaker. Begge parter sender og leser tekst og vedlegg, med samme klient. Korrespondansecellen bygges ut og får chat-cellens levering. Chat-cellen selv har klartekst og ingen vedlegg (A20 i §0).
2. **Tjeneren kan ikke lese innholdet og ikke slippe inn noen.** Den ser numrene på dem som skriver, når og hvor mye, og om en melding har vedlegg. Nøklene dine ligger på Macen din.
3. **Posten kommer av seg selv.** Klienten abonnerer på cellen (Flow) og får ny post uten å spørre. Historikken hentes med `get state`.
4. **Bare du slipper inn,** på Macen, med Touch ID eller passordet ditt. Ingen agent og ingen tjener kan gjøre det. Agenten din sender og leser fortsatt på ditt ja, som i dag.
5. **Få håndgrep.** Mottakeren: installere én signert pakke, gi agenten sin én lenke, sende deg koden (koden er et forslag, spørsmål 4 i §6). Du, per person: lage lenken, sende pakken og lenken, sammenligne koden, godkjenne. Ingen adminside, ingen miljøfil og ingen omstart av staging, heller ikke ved fornyelse.
6. **Vedlegg i samme pakke.** Installerpakken og budsjettet går som vedlegg, og vedlegg går begge veier.
7. **Den gamle kanalen står** til begge er over. Tilgangene der gjelder til 05.11. Er det nye ikke ute da, må den fornyes én gang til. Til slutt trekkes de gamle tilgangene, på ditt ord.

Prisen for punkt 2 og 4: Macen din må være på når du godkjenner. Mister du nøkkelen på Macen, må cellene opprettes på nytt.

- Dette finnes: cellen som lagrer krypterte meldinger (i CellProtocol, i revisjonen staging kjører), en klient for den inviterte parten (på `main` i HavenAgentD), vedlegg (skrevet og testet lokalt, ikke gjennomgått, ikke på `main`), og adminvinduet til HAVEN Agent med «Trenger deg» (på en gren, bildene godkjent 10.09 og 12.09).
- Dette mangler: i cellen eieren som deltaker også for vedlegg, levering med Flow og `state`, og innslipp og invitasjon signert på eierens Mac (A8, A10 og A19–A22 i §0). I klienten: samme klient for eier og invitert, håndtrykk og abonnement over broen, oppsett fra én lenke, og kortet i adminvinduet. På staging: å huse cellene og vedleggene. Og pakken.
- Ikke i første pakke, hvis du ikke sier noe annet (spørsmål 5 i §6): varsel på skjermen ved ny post, vedlegg som referanse eller hent ved behov (bare kopi), og sikkerhetskopi av nøkkelen. Heller ikke gruppesamtaler og produksjon.
- To løp (ditt valg 07.10): Codex tar cellen i CellProtocol og klienten. Kortet på Macen og oppsettet hører til klienten, og pakken bygget Codex også sist; det er min lesning, ikke ditt valg. Korrespondanse-tråden tar staging og prøvene. Det Codex skriver, gjennomgås av Fabel. Det korrespondanse-tråden skriver, gjennomgås av Astra. Det som skal inn i CellProtocol, går inn der og ut i en utgivelse først (ordene dine til kø-tråden 07.10).
- Første ledd er en liten prøve hos Codex av punkt 4, lokalt: en avtale signert på én maskin slipper inn et medlem i en celle som kjører på en annen. Holder ikke den, kommer saken tilbake til deg før noe annet bygges.
- Tid: jeg har ikke et tall jeg kan stå for før den prøven er gjort (§3b).
- Dokumentet sier hva som skal være sant når Vegar og Victoria bruker det, og hva som teller som bevis for det. Det er ikke en plan. Planen kommer etter at du har godkjent formålene (G1) og bildene (G1-GUI).

Figuren `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/figur/leddene-v3.png` viser leddene, hvor hvert av dem står i dag, og hvor ordet ditt trengs.

**Ordliste.**

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
| Kortet | Flaten der du godkjenner eller avslår en forespørsel om tilgang. I den gamle kanalen: «Godkjenn meldingsadgang» under `/admin/funding` på staging. I det nye: et kort under «Trenger deg» i adminvinduet til HAVEN Agent på Macen din. |
| Flow | Strømmen av hendelser en celle sender til dem som abonnerer på den. I chat-cellen kommer hver melding slik. |
| `get state` | Kallet som henter cellens tilstand. I chat-cellen gir det de siste meldingene. |
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

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 06.10.2026 ca. kl. 10:10Z:

> Dette sier meg ingenting om hva status er eller hva jeg skal gjøre. Formålet er å få ut correnspondence til vegar og victoria, med støtte for vedleg og kryptert kommunikasjon. Hva gjenstår for å få testet med dem. De har ikke fått noen ny installerer pakke. Og det er altfor mye manuelle operasjoner.

Kjetils tre valg samme dag, ca. kl. 11:20Z:

| Spørsmål | Kjetils svar |
|---|---|
| «Tjenerdelen (punkt 2) har ingen eier. Hvem skal bygge den?» | «Denne tråden» |
| «Hva skal den første pakken til Vegar og Victoria bære?» | «Kryptert og vedlegg samlet» |
| «Vegars tilgang i den gamle kanalen går ut torsdag 08.10, og Victorias er alt ute. Hva gjør vi med den imens?» | «Forny, jeg bytter selv» |

Kjetil, 05.10.2026:

> Bygg en ny universal installerer om det trengs - men DET MÅ VIRKE! - før jeg sender dem en ny installerer

Kjetil, 06.10.2026 ca. kl. 20:03Z, etter å ha fått iterasjon 2 med de fem valgene:

> Jeg synes du har rotet det til. En chat celle må kunne brukes av eier også. Om det er vanskelig så er  det feil satt sammen. Mulig vi skal bruke chat celle funksjonaliteten vi har et annet sted hvor alle som ønsker å motta meldinger abonnerer på Flow og de kan alltids be om get state for å få litt chat historie. Hvordan er chat i korrespondansen skrudd sammen?

Kjetil, 07.10.2026 ca. kl. 10:00Z og ca. kl. 12:57Z: meldingen fra 06.10 kl. 10:10Z en gang til, ordrett, begge ganger.

Kjetils to svar 07.10.2026 (mellom kl. 10:25Z og 12:58Z):

| Spørsmål | Kjetils svar |
|---|---|
| «Hvor skal eierens nøkler ligge i den nye korrespondansen?» | «På Macen min». Valget var beskrevet slik: tjeneren kan verken lese meldingene eller slippe inn noen, og han godkjenner nye medlemmer på Macen. |
| «Skal Codex ta CellProtocol og klienten (punkt 1 og 3 i tabellen) mens jeg tar staging (punkt 4)?» | «Ja, to løp» |

Kjetil til kø-tråden 07.10.2026, slik kø-tråden gjengir det i `_losen-queue/KOORDINERING.md` (innlegget kl. 09:56Z):

> Vi kan ikke ha det slik at det tar en måned å få deployet fikser. Om det er noe som skal inn i CellProtocol for at noe i CellScaffold eller HAVEN app skal virke - SÅ MÅ DET INN i CellProtocol FØRST!

### Det som alt er bestemt, og som gjelder her

Dette er ikke åpent i denne spesifikasjonen. Det er tatt med fordi formålene bygger på det. Der formålene her avviker fra noe av det, står avviket i §6, som valg eller som standardvalg, og i endringsforslaget til Book 33 (§3 rad 4).

| Bestemt | Hvor det står |
|---|---|
| Fire egenskaper «each of which must be true before any package leaves the house»: meldingen er en verdi i en celle; cellen har bare chiffertekst, og den som drifter verten, kan ikke lese innhold; konvolutten er formålsbundet, minimal og utløper med innholdet; driften kan ikke koble en korrespondanseidentitet til en person ut fra det verten lagrer. | `CellProtocolDocuments/Book/33_Correspondence_First_Class.md`, innledningen (Kjetil er beslutningseier; 01.09) |
| Seks ting en pakke må vise før den forlater huset: (1) meldingen ligger som konvolutt, og en utskrift fra verten viser ingen klartekst; (2) avtalen har nøyaktig de fire handlingene, og et forsøk på å invitere andre blir avvist; (3) vertens tilstand har identitetsnumre og ingen navn; (4) utløp fjerner også ytterdelen; (5) en delegert assistentidentitet sender, og mottakeren verifiserer både assistenten og hvem som står bak; (6) klienten er signert, notarisert og går gjennom Gatekeeper. | Samme fil, §10 |
| Avtalen for en ekstern flate gir nøyaktig fire handlinger. Medlemskap, nøkkelpolicy og livsløp gis aldri til en ekstern flate; de hører til eieridentiteten, og til den som drifter verten bare der livsløpet krever det. | Samme fil, §3.4 |
| Kvitteringen kan i piloten være synlig for verten, hvis pakketeksten sier det rett ut. Når og hvor mye som sendes, skjules ikke, og ingen pakketekst skal antyde noe annet. | Samme fil, §5.3 og §4.2 |
| Tre beslutninger 01.09: konvoluttens ytterdel har sitt eget formål; en celle med to medlemmer lukkes når medlemslista endres, og en ny relasjon er en ny celle; én delegert identitet med flere motparter erstatter én profil per motpart. | Samme fil, §11 |
| Vedlegg: tre moduser, og valget følger av hva som faktisk er mulig («Alle tre må støttes»); avsenders celle lagrer og mottaker henter («Det gjør tilbakekall mulig»); vedlegget dør med meldingen; ingen størrelsesgrense; mottakeren ser navn, type og størrelse før henting; signert binding til melding og avtale. Avklart 29.09: sletting hos avsender gjelder bare kopimodus («var tenkt bare om den sendes som kopi via vedlegg»). At slettingen da er en overdragelse til mottakeren, er Losens lesning av svaret, ikke et eget vedtak. | `CellProtocolDocuments/Deliverables/PDD_vedlegg-korrespondanse_2026-09-28/BESLUTNINGER_KJETIL_2026-09-28.md` |
| Broen: «det å bevise identitet over bridge er helt nødvenig» (27.09). «Peer-beviset må være helt sikkert og robust - alle sårbarheter vi oppdager skal lukes ut.» (28.09). Åpne funn skal være lukket eller skriftlig godtatt før en utgivelse med broen pinnes. | `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/STATUS.md`; `_losen-queue/KOORDINERING.md` |
| Nye kapabiliteter i CellProtocol «skal være testet mot både funksjon og formål før implementasjonen pushes til main i CellProtocol … Er Claude i tvil om et valg, skal han spørre, og spørre tydelig» (18.09). | Kjetils stående regel |
| Varsel ved ny post, hendelsesbasert. G1, G1-GUI og G2 godkjent 12.09. Bygget for den gamle cellen. | `CellProtocolDocuments/Deliverables/PDD_correspondence-varsel-hendelsesbasert_2026-09-12/STATUS.md` |
| Agentene i dag: «Losen kvitterer selv på innkommende correspondence-post uten å spørre; sending av meldinger krever fortsatt eget ja.» | Kjetils stående regel |

### Påstandene intensjonen bygger på

«Hentet» betyr lest fra kilden, med sti og dato. Bare det som er hentet, bærer planen. A7–A10 er lest i dag i koden; hva den uavhengige kontrollen av dem sa, står i §7.

| Nr. | Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|---|
| A1 | «De har ikke fått noen ny installerer pakke» | hentet 06.10 | Det siste som er sendt, er `HAVENAgentD-0.3.2-universal2.pkg` fra 08.09 (Vegar) og en pilotpakke fra 30.08 (Victoria; fila er ikke funnet igjen). Forsøket 29.09 ga ingen pakke: `CellProtocolDocuments/Deliverables/INSTALLER_UNIVERSAL_2026-09-29.md`. |
| A2 | Det mottakerne har, er den gamle kanalen: tjeneren ser meldingene i klartekst, ingen vedlegg, 16 KiB per melding | hentet 06.10; for Victoria en slutning | CellScaffold `e5c3434`: `CellScaffold/Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift`. Vegars klient er den fra pakken 08.09. Hva Victoria har installert, er ikke målt (A15). |
| A3 | Det finnes en klient for kryptert korrespondanse på `main` | hentet 06.10 | HavenAgentD `ea558ba`: `HavenAgentD/Sources/HavenCorrespondenceMCP/`. Den forsegler konvolutter til en relasjonscelle og sender dem over broen. Den har ingen HTTP-reserve for meldinger. Den virker bare for den inviterte parten (A9). |
| A4 | Tjenerdelen finnes ikke | hentet 06.10 | CellScaffold `origin/main` er `e5c3434` (2026.9.5, på staging og prod). Den har bare rutene til den gamle kanalen, huser ingen relasjonscelle og har ingen innmelding for den nye klienten. Ingen oppgave under `HAVEN-Deploy/queue/tasks/` dekker det. |
| A5 | Byggesteinene ligger i CellProtocol-revisjonen staging kjører | hentet 06.10 | `/health/build` på staging oppgir `cellprotocol_revision` `81601a6…` (2026.9.4). Den har relasjonscellen, konvoluttene, avtalemalene og strømkryptoen for vedlegg (`AttachmentStreamV1`). |
| A6 | Vedlegg er skrevet og testet, men ligger ikke på `main` | hentet 06.10 | Lokale grener `codex/correspondence-attachments-20260930` (CellProtocol `9420e7d`, HavenAgentD `a6bd163`). 24 nye tester grønne lokalt. Ingen fjern-gren har commitene. Ikke prøvd: filer over 180 037 byte, to maskiner, full disk i virkeligheten. En overføring som blir avbrutt av en omstart, kan ikke fortsette; den må sendes på nytt. Det finnes ingen kvote. `CellProtocolDocuments/Deliverables/VEDLEGG_IMPL_3_2026-09-30.md`. |
| A7 | Cellen legger alltid eieren i medlemslista, og krever at hver konvolutt er kryptert til nøyaktig hele medlemslista | hentet 06.10, på `origin/main` | CellProtocol `1ec56d5`: `CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift`, `establishInitialMembership` (linje 198–204) og `envelopeRecipientsMatchCurrentMembership` (linje 479–483). Lest med jobben `b22`: `HAVEN-Deploy/_handoff/KORR-UT/maal/CP-MAIN-MOT-VEDLEGGSGRUNN-20261006.md`. Følge: eier tjeneren cellen, er tjeneren mottaker og kan lese. |
| A8 | Bare eieren kan gi en identitet en avtale. Eierens nøkkel må da bevise seg og signere i cellens prosess, med eierens nøkkellager, og den som får avtalen, må bevise sin nøkkel i samme kall | hentet 06.10, på `origin/main` | Samme revisjon: `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`, `addAgreement(_:for:authorizedBy:)` (fra linje 1334) og `admissionPolicyAllows` (linje 1431–1445). Fila er uendret fra `81601a6` til `1ec56d5` (samme jobb). Medlemslista kan også endres av en identitet som er lenket til eieren som samme entitet, og av en delegat som har fått eierens egen avtalemal; ingen av dem kan gi avtaler. Om eierens nøkkellager kan ligge på en annen maskin og svare over broen, viser ikke kildene. |
| A9 | Klienten på `main` virker bare for den inviterte parten i en celle med to medlemmer | hentet 06.10, på `origin/main` | HavenAgentD `ea558ba`: `HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceClient.swift`, linje 513–553. Klienten krever at den lokale identiteten er den avtalen er utstedt til, at utstederen er medlem, og at hvert medlems krypteringsnøkkel står i den signerte avtalen. Cellen fører bare eieren og den inviterte der (`GeneralCell.swift`, `agreementDerivedFromTemplate`). Eiersiden har ingen vei til klienten i produksjon: ingen kommando lager en eierprofil. Klientkoden godtar likevel en profil der eieren selv har signert den samme avtalen med seg selv som mottaker av den, og vedleggstestene bruker det for eieren som den som tar imot (`HavenAgentD/Tests/HavenCorrespondenceMCPTests/CorrespondenceAttachmentMCPTests.swift` linje 19–28, på vedleggsgrenen). Med en slik profil kan eieren etter koden også sende tekst; det er ikke testet. |
| A10 | Bare den inviterte parten kan sende vedlegg; eieren kan bare ta imot | hentet 06.10, på vedleggsgrenen | CellProtocol `9420e7d`: `CorrespondenceCell.swift`, `authorizeAttachment` og `performAttachment` (avsenderen må selv ha en avtale, og mottakernøklene tas fra avtalen). HavenAgentD `a6bd163`: `Sources/HavenCorrespondenceMCP/CorrespondenceAttachments.swift`, `sendAttachment`. Følge: eier du cellen, kan du ikke sende installerpakken til Vegar med koden som den står. |
| A11 | Delegeringen Book 33 §4.3 og §10 punkt 5 krever, finnes ikke | hentet 06.10, på `origin/main` og på vedleggsgrenen | `delegation` forekommer bare som avslagsgrunnen `delegationRevoked` (samme jobb `b22`). `HavenAgentD/Docs/CorrespondenceS6ChangeSetAndRollback.md` sier det samme under «Preconditions». |
| A12 | Broen er merget i CellProtocol, men ikke ute | hentet 06.10 | PR #53 merget 05.10 (`1ec56d5`). Ingen tagg inneholder den: den nyeste taggen er `2026.9.4`, som er `81601a6`. Funnene N32 og N36–N39 står åpne. CellScaffold mangler ruta (HD-0166, ikke påbegynt). N35 gjelder den delte forbindelsen den nye klienten bruker (HD-0161); om den er lukket i #53, vet jeg ikke. Etter #53 må klientene gjøre håndtrykket selv; korrespondanseklienten er ikke oppdatert for det. `_losen-queue/KOORDINERING.md`; `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/STATUS.md`. |
| A13 | «altfor mye manuelle operasjoner» | hentet 06.10 | For en mottaker i dag: pakke ut, lagre en invitasjonsfil, kjøre `setup`, sende en identitetsutskrift, kjøre `activate` og `doctor`, og registrere MCP for hånd. For deg ved hver fornyelse: nytt invitasjonssett, én linje i en root-eid fil på verten, omstart av staging, sammenligning av fem identitetsverdier, godkjenning og videresending. Det siste er målt i dag: `HAVEN-Deploy/_handoff/HD-0006/maal/HAVEN-DEPLOY-PAA-VERTEN-20261006.md`. |
| A14 | Ny post gir ikke varsel | hentet 06.10 | HD-0069, HD-0093 og HD-0072 står åpne. PDD-en for varsel har G2, ikke G3, og er bygget for den gamle cellen. |
| A15 | Hva Victoria har installert, og hvilke Macer mottakerne har | ikke tilgjengelig | Ingen kilde. Macen din har ikke Rosetta, så Intel-delen av en pakke kan ikke prøves her. |
| A16 | HavenAgentD `main` har ikke grønn CI | hentet 05.10 | Tre av tre løp sto til tidsgrensen. Codex' PR #28 har grønn CI og retter testskriptet. `_losen-queue/KOORDINERING.md`. |
| A17 | Det finnes en godkjenningsflate for den gamle kanalen | navnet hentet 06.10; innholdet ikke lest | `CellScaffold/Sources/App/Cells/Agent/CorrespondenceApprovalConfigurationFactory.swift` finnes på `origin/main`. To adminceller på staging («Admin Control Plane Overview» og «Drift») var røde 06.10 kl. 07:17–07:23Z («AdminScaffold er utilgjengelig», HD-0143). Om `/admin/funding`, der kortet ligger, er rammet, er ikke målt. |
| A18 | Vedlegg kan gå som referanse, hent ved behov eller kopi | hentet 06.10, på vedleggsgrenen | De to første krever at kilden er registrert i avsenders celle, og registreringen er et lokalt kall på maskinen der cellen kjører (`CorrespondenceCell.swift`: «This local integration API never accepts a path from an MCP peer»). Bare testene registrerer kilder; klienten kan vise til en registrert kilde, men kan ikke registrere en. For filer som ligger hos avsenderen, blir modusen mot en celle på staging derfor alltid kopi. |
| A19 | Korrespondansecellen leverer bare på forespørsel | hentet 06.10 kveld, på `main` i arbeidstreet | `CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift`: `inbox` gir bare ytterdata, `readMessage` gir én konvolutt. Cellen sender fem hendelser på Flow (`message.stored` og fire til), uten innhold. `GeneralCell.flow` krever rettigheten `feed`, og avtalemalen for den inviterte har den ikke (`CorrespondenceAgreementTemplates.swift`, linje 7–12). Flow lagres ikke, så en frakoblet klient mister hendelsen. Kontrollert av en uavhengig leser 06.10 (`panel/FABEL-CHATSVAR.md`). |
| A20 | Chat-cellen leverer over Flow og gir historikk med `get state`, men i klartekst | hentet 06.10 kveld | `CellProtocol/Sources/CellBase/Cells/Chat/ChatCell.swift`: hver melding sendes til alle abonnenter (`chat.message`), `state` gir inntil 200 meldinger, og eieren sender og leser som de andre. Teksten ligger i klartekst i cellen og på Flow; krypteringen er bare forberedt (`encryptionEnabled: false`). Ingen vedlegg, intet utløp. Cellen har invitasjonsbevis signert av eierens nøkkellager (`ChatInvitationProofUtility.swift`), men en godtatt invitasjon gir ikke tilgang i seg selv. |
| A21 | For de fire tekstoperasjonene behandler korrespondansecellen eier og invitert likt; det er innslippet som krever eierens nøkkel der cellen kjører | hentet 06.10 kveld | `CorrespondenceCell.swift`: de fire operasjonene sjekker bare medlemskap (linje 283, 299, 320, 391). `GeneralCell.swift`, `addAgreement`: avtalen signeres alltid av eierens nøkkel i cellens prosess (`contractSigningOwner`, linje 1396–1411 og 1546–1559), og standarden er `.ownerApprovalRequired` (linje 390 og 462). Det gjelder alle celler, chat-cellen også. Setningen «To agenter kan ikke skrive til hverandre i én celle slik koden står» i iterasjon 2 var for sterk for tekst. Den står for vedlegg (A10) og for innslipp. |
| A22 | Klienten avviser en avtale som ikke har nøyaktig de fire handlingene, og bruker bare `get` og `set` | hentet 06.10 kveld | `HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceClient.swift`, linje 521–533, og `CorrespondenceCellTransport.swift`, linje 49 og 54. Broen har kommandoen `feed` (`CellProtocol/Sources/CellBase/Cells/Bridging/BridgeCommand.swift`). Om et abonnement over broen virker fra en klient utenfor Binding, er ikke prøvd. |
| A23 | Broen 07.10: utgivelsen venter bare på Kjetils ja | hentet 07.10 kl. 13:00Z fra `_losen-queue/KOORDINERING.md` (kø-trådens innlegg kl. 10:15Z–12:32Z), ikke målt av denne tråden | CellProtocol `2026.9.5` = `main` med #53 og PR #60; alle CI-kjøringer grønne. N32 og N36–N38 ligger i Apple-skanneren og holder ikke serverutgivelsen tilbake. N35, som ligger på veien korrespondanseklienten bruker, var en testmangel og har fått en test (PR #61). Bro-tråden eier pinnbytte og adminbro-rute i CellScaffold (HD-0190). Om det dekker ruta korrespondansen trenger (HD-0166), står ikke der. |

**Hva A7–A10 betyr samlet.** Slik koden står, er en relasjon som virker, én eier og én invitert. Den inviterte siden har klienten og kan sende tekst og vedlegg. Eiersiden har ingen vei til klienten utenom testene, og kan ikke sende vedlegg. To inviterte i samme celle går ikke: klienten til den ene godtar ikke den andre som medlem. Eier tjeneren cellen, er tjeneren mottaker. Ingen av måtene gir det du har bedt om: at agenten din og Vegars agent skriver til hverandre, begge veier, med vedlegg, uten at tjeneren kan lese. Planen fra 09.09 pekte på den ene halvdelen (`CellProtocolDocuments/Deliverables/Correspondence_Uten_Agent_I_Runtime_Plan_2026-09-09.md`, §3.3: lagringsmyndighet må skilles fra hvem som er mottaker). Den sier ikke at klienten bare virker for den inviterte, eller at et vedlegg binder avsenderen til en avtale.

**Rettet i iterasjon 3.** Avsnittet over er for sterkt for tekst: cellen behandler eier og invitert likt i de fire tekstoperasjonene (A21). Det som mangler for at eieren skal bruke cellen som den andre parten, er en eierprofil i klienten (A9), vedlegg for eieren (A10), og en vei for innslipp når eierens nøkkel ikke ligger der cellen kjører (A8). Kjetil har valgt at han eier cellene og er part, med nøklene på Macen sin. Modellen der tjeneren eier, er ute.

## 1. Formålstre

Nye noder heter `purpose://candidate.kryptert-korrespondanse-med-vedlegg-ut.<navn>`. I tabellen står bare `<navn>`. Foreldrene er hentet fra `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json`. Formålene gir ingen rettigheter.

```text
R  Vegar og Victoria korresponderer med Kjetil, kryptert og med vedlegg
├── A  Kryptert fra avsender til mottaker, og driften er blind
│   ├── A1  Eieren og den inviterte skriver til hverandre i én celle, med samme klient
│   ├── A2  Staging huser én celle per relasjon, og cellen tar bare imot konvolutter
│   ├── A3  Tjeneren har ingen nøkkel: den kan verken lese, slippe inn eller koble identitet til person
│   ├── A4  Innmelding gir en smal avtale, ikke en bred
│   ├── A5  Meldingene går over den autentiserte broen, og ingen annen vei
│   ├── A6  Utløp fjerner hele meldingen, også når ingen leser
│   └── A7  Ny post kommer uten spørring (Flow), og historikken kan hentes (state)
├── B  Vedlegg i samme pakke
│   ├── B1  Vedleggskoden er gjennomgått og ligger på main
│   ├── B2  Staging bærer vedleggene og rydder etter seg
│   └── B3  Installerpakken og budsjettet kommer fram og kan brukes
├── C  Én pakke og få håndgrep
│   ├── C1  Mottakeren installerer én pakke og gjør høyst to håndgrep til
│   ├── C2  Kjetil slipper inn én person på Macen sin, og ser at det er rett person
│   ├── C3  Å invitere og å fornye krever ingen drift
│   ├── C4  Kjetils egen Mac bruker samme pakke og samme vei
│   └── C5  Overgangen er fullført: begge er over, og de gamle tilgangene er trukket
└── D  Dette skal ikke skje
    ├── D1  Den gamle kanalen brytes før begge er over
    ├── D2  Klartekst inn i de nye cellene, eller retur til klartekst
    ├── D3  En agent sender i Kjetils navn, eller slipper inn noen, uten hans ja
    └── D4  Nøkkel, kode eller meldingstekst i logger og bevis
```

R er oppnådd når A, B og C er oppnådd og ingenting under D har skjedd. En grønn test i skyen oppfyller ikke R: R krever at Vegar og Victoria selv har brukt det. En mottaker er «over» når T-R er grønn for den mottakeren.

Kolonnen «Hvem» sier hvem som gjør arbeidet. «Codex eller du» betyr at merge og utsetting utføres av Codex eller deg, på ditt ord; korrespondanse-tråden kan ikke merge eller sette ut.

| Id | purposeRef (`<navn>`) | Formål | Forelder | Mål som kan observeres | Test | Hvem | Status |
|---|---|---|---|---|---|---|---|
| R | `i-bruk-hos-mottakerne` | Vegar og Victoria korresponderer med Kjetil, kryptert og med vedlegg | `purpose://contact.communication` | Begge har, med den nye pakken, lest en melding, svart, hentet et vedlegg og sendt et vedlegg, og sier selv at det virket. | T-R | Vegar, Victoria og Kjetil | candidate |
| A | `kryptert-og-blind-drift` | Meldingene er kryptert fra avsender til mottaker, og den som drifter staging, kan verken lese dem eller se hvem som er hvem | R; `purpose://access.audit.privacy` | Punkt 1–4 i Book 33 §10 er vist på staging. | A1–A6 | — | candidate |
| A1 | `to-parter-i-en-celle` | Eieren og den inviterte skriver til hverandre i én relasjonscelle, med samme klient, tekst og vedlegg begge veier | A | Prøveparet, der den ene prøveidentiteten eier cellen og den andre er invitert, mot samme celle på staging og med binæren fra pakken: hver side leser, sender, kvitterer, sender et vedlegg og henter et vedlegg. Alle ti handlingene lykkes. Medlemslista har nøyaktig de to. | T-A1 | Codex skriver; Fabel gjennomgår; Codex eller du merger | candidate |
| A2 | `staging-huser-konvolutter` | Staging huser én relasjonscelle per godkjent relasjon, og cellen tar bare imot konvolutter | A | En melding sendt med klienten ligger lagret som konvolutt. Bytene staging har lagret for cellen, inneholder verken innholdet eller emnet, heller ikke i en annen koding. Klartekst sendt rett til cellen blir avvist. | T-A2 | Korrespondanse-tråden | candidate |
| A3 | `tjeneren-er-ikke-mottaker` | Tjeneren har ingen nøkkel som åpner en konvolutt eller slipper inn et medlem, og kan ikke koble en identitet til en person ut fra det den lagrer | A | Medlemslista i hver celle er de to partenes korrespondanseidentiteter og ingen andre, og hver lagret konvolutt er kryptert til nøyaktig de to. Eierens nøkler finnes ikke på staging. En avtale kan bare signeres på eierens Mac, og et forsøk på å slippe inn et medlem fra tjeneren blir avvist av cellen og av klientene. Det staging lagrer for korrespondansen, har verken visningsnavn, profilnavn, maskinnavn eller entitetsreferanse. | T-A3 | Codex (cellen og klienten); korrespondanse-tråden (staging) | candidate |
| A4 | `smal-avtale-ved-innmelding` | En godkjent identitet får cellens adresse, medlemmenes offentlige nøkler og en avtale signert av eieren, med nøyaktig de handlingene den skal ha | A | Avtalen har de fire handlingene (innboks, les, send, kvitter), retten til å abonnere på cellens hendelser og hente historikken (A7), og de ti vedleggshandlingene, og ikke flere. Et forsøk på å invitere andre med den blir avvist. En avtale uten vedleggshandlingene gir ingen vedleggstilgang. | T-A4 | Codex | candidate |
| A5 | `over-autentisert-bro` | Meldingene går over den autentiserte broen, og ingen annen vei | A | To prøveidentiteter sender hver sin melding mot staging over broen. En forbindelse uten håndtrykk når ikke cellen. En identitet med håndtrykk, men uten avtale, blir avvist av cellen. Klientbinæren inneholder ikke adressen til den gamle ruta. | T-A5 | Bro-tråden leverer ruta (HD-0166). Codex gjør klientens håndtrykk. Korrespondanse-tråden prøver | candidate |
| A6 | `utloep-fjerner-alt` | Når en melding utløper, forsvinner hele konvolutten, også ytterdelen, uten at noen må lese innboksen først | A | Senest én time etter utløp finnes meldingen ikke i det staging har lagret, selv om ingen har kalt cellen i mellomtiden. | T-A6 | Korrespondanse-tråden | candidate |
| A7 | `levering-uten-spoerring` | Ny post kommer til mottakerens klient uten at noen spør, og historikken kan hentes | A | En klient som abonnerer på cellen (Flow), har en ny konvolutt innen ti sekunder etter at den er lagret, uten å ha spurt. En klient som var frakoblet, henter de siste konvoluttene med `get state` når den kobler til igjen, og mangler ingen. En identitet uten avtale får verken hendelser eller historikk. Abonnentene får bare chiffertekst. | T-A7 | Codex | candidate |
| B | `vedlegg-i-samme-pakke` | Mottakeren får materialet arbeidet trenger, i samme pakke som den krypterte korrespondansen | R; `purpose://digital-work.coordinate` | F1–F7 i vedleggs-PDD-en, prøvd ute. | B1–B3 | — | candidate |
| B1 | `vedlegg-paa-main` | Vedleggskoden er gjennomgått av Astra og ligger på `main` i CellProtocol og HavenAgentD, og eieren kan sende vedlegg som den inviterte | B | En ren klone fra GitHub til en tom mappe bygger og består testene i begge repoene. Rapporten fra gjennomgangen ligger ved, og hvert funn er rettet eller skriftlig godtatt av deg. | T-B1 | Codex; Fabel gjennomgår; Codex eller du merger | candidate |
| B2 | `staging-baerer-vedlegg` | Staging lagrer avsenders krypterte vedlegg i en undercelle avsenderen eier, og rydder ved utløp og tilbakekall | B | Den faktiske installerpakken og en fil på 200 MB går hver vei med lik sjekksum hos mottakeren. Etter utløp og etter tilbakekall kan fila ikke hentes, og bytene er borte fra disken. Er det mindre ledig plass enn terskelen (§6, standardvalg), blir et nytt vedlegg avvist før en eneste filbyte er sendt. | T-B2 | Korrespondanse-tråden | candidate |
| B3 | `installerpakke-og-budsjett` | Installerpakken når Vegar og Victoria, og budsjettet når den du velger, som vedlegg | B | F2 og F3 i vedleggs-PDD-en: to av to får brukt pakken, og budsjettmottakeren åpner riktig versjon. | T-B3 | Vegar, Victoria og Kjetil | candidate |
| C | `en-pakke-faa-haandgrep` | Ingen gjør driftsarbeid for å korrespondere | R | C1–C5. | C1–C5 | — | candidate |
| C1 | `mottaker-en-pakke-ett-haandgrep` | Mottakeren installerer én signert pakke og gjør høyst to håndgrep til | C | På en Mac uten HAVEN: dobbeltklikk på pakken, gi agenten sin lenken, og send Kjetil koden på seks sifre. Ingen kommando skrives, ingen fil lagres eller redigeres for hånd, ingen advarsel fra macOS. Bestått er tre håndgrep eller færre, telt på et skjermopptak (macOS' egne dialoger under installasjonen teller som ett). Det virker oppå en eldre installasjon, og på Intel hvis en mottaker har det. Bildet er `images/mottaker-oppsett-v1.png`. | T-C1 | Codex bygger pakken og oppsettet; korrespondanse-tråden prøver | candidate |
| C2 | `en-godkjenning-per-person` | Kjetil slipper inn én person på Macen sin, og ser at forespørselen er fra rett person | C; `purpose://gui.quality.functional-accessible` | Per person gjør Kjetil fire ting: lager lenken, sender pakken og lenken, sammenligner koden, og godkjenner. Ett kort per person som ber om tilgang, under «Trenger deg» i adminvinduet til HAVEN Agent. Kortet viser navnet Kjetil selv ga lenken (lagret bare på Macen), en kode på seks sifre og sluttdatoen. Å lage lenken og å godkjenne krever Touch ID eller passordet hans. Koden er et forslag (spørsmål 4 i §6): uten den er lenken alene beviset. Avslag virker. En forespørsel laget med en annen nøkkel enn mottakerens, viser en annen kode enn den mottakeren ser. Lenken lages i samme vindu. Bildet er `images/godkjenning-paa-macen-v1.png`, og Kjetil godkjenner det før noe bygges (G1-GUI). | T-C2 | Codex | candidate |
| C3 | `tilgang-uten-driftsrunder` | Å invitere en ny person, og å fornye en tilgang, krever ingen drift | C | Kjetil lager en lenke på Macen, og mottakeren kommer inn uten at noen rører staging: ingen miljøfil, ingen omstart og ingen root, fra lenken lages til første melding er lest. Avtalen gjelder til sluttdatoen Kjetil satte, høyst ett år. Når den går ut, sier klienten det i klare ord. Kjetil fornyer med samme trykk som første gang, og klienten henter den nye avtalen selv. En lenke gjelder i sju dager og kan brukes én gang. Kjetil kan trekke en tilgang i samme vindu, og etter det blir mottakerens kall avvist. Ny nøkkel eller flere rettigheter krever en ny forespørsel. | T-C3 | Codex (cellen og klienten); korrespondanse-tråden (staging) | candidate |
| C4 | `kjetils-mac-samme-pakke` | Kjetils egen Mac bruker samme pakke og samme vei som mottakerne | C | For den nye korrespondansen er programfila agentene dine starter, pakkens (stien i oppsettet og sjekksummen stemmer med pakkens liste). En melding sendt med ferdighetene dine går fram med den nye klienten. Ferdighetene dine er oppdatert for den nye klienten, som velger relasjon på en annen måte enn den gamle. Den gamle klienten står ved siden av og virker til begge mottakerne er over (D1). | T-C4 | Korrespondanse-tråden; du installerer pakken | candidate |
| C5 | `overgangen-fullfoert` | Begge mottakerne er over, og de gamle tilgangene deres er trukket | C | T-R er grønn for både Vegar og Victoria. Etter ditt ord er de to gamle tilgangene trukket, og et sendeforsøk til dem i den gamle kanalen blir avvist. De gamle meldingene ligger urørt til de utløper. | T-C5 | Korrespondanse-tråden; ditt ord | candidate |
| D | `det-som-virker-staar` | Det som virker i dag, står, og det som aldri skal skje, skjer ikke | R; `purpose://self-determination.data.verifiability` | D1–D4. | D1–D4 | — | candidate |
| D1 | `gammel-kanal-staar` | Skal ikke: den gamle kanalen brytes før begge mottakerne er over | D | Før og etter hver utsetting til staging sender prøveparet en melding hver vei i den gamle kanalen og leser den. | T-D1 | Korrespondanse-tråden | candidate |
| D2 | `ingen-klartekst` | Skal ikke: gamle meldinger flyttes inn i de nye cellene, eller den nye klienten faller tilbake til klartekst | D | De nye cellene er tomme før første nye melding. Når broen er sperret, feiler klienten med en klar melding og sender ingenting. | T-D2 | Korrespondanse-tråden | candidate |
| D3 | `ingen-agent-uten-ja` | Skal ikke: en agent sender i Kjetils navn, eller slipper inn noen, uten hans ja | D | I prøven finnes ingen sending fra Kjetils identitet som han ikke har sagt ja til. Å slippe inn et medlem krever Touch ID eller passordet hans på Macen: et forsøk fra agentens prosess, uten det, blir avvist. Avtalen en invitert holder, gir bare handlingene i A4. Vernet mot at en agent sender i hans navn, er fortsatt hans ja og den stående regelen, ikke en lås (§2). | T-D3 | Codex; korrespondanse-tråden prøver | candidate |
| D4 | `ingen-verdi-i-logg` | Skal ikke: nøkler, engangskoder eller meldingstekst havner i logger, utskrifter eller bevis | D | Søk i alle bevisfiler og logger fra prøven etter prøvenøkler, prøvekoder og prøvetekst gir null treff, og det samme søket finner en merkelapp som er lagt inn med vilje. | T-D4 | Korrespondanse-tråden | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål har en test i §5.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en menneskeklient i Binding (W5 i planen fra 09.09). Den første pakken er agentens klient, som i dag.
- Ikke jobbadministrasjon uten agent (W1 og W2 i samme plan).
- Ikke skillet mellom agenter og identiteter (W0 og porten G0 i samme plan). I den første pakken bruker agentene dine korrespondansenøkkelen din, som i dag, og Vegars og Victorias agenter bruker deres. Vernet mot at en agent sender i ditt navn, er ditt ja og den stående regelen, ikke en lås. Det er spørsmål 2 i §6.
- Ikke delegering (Book 33 §4.3 og §10 punkt 5). Også spørsmål 2 i §6.
- Ikke produksjon. Prøven går mot staging, som den gamle piloten.
- Ikke celler som deltakerne huser selv (Book 33 §7.2). Derfor går vedlegg som kopi i første pakke (A18 i §0).
- Ikke gruppekorrespondanse, og ikke skjuling av når og hvor mye som sendes. Pakketeksten sier det.
- Ikke vern mot en drift som med vilje bytter nøkler under innmeldingen eller kjører endret kode. Book 33 lover at driften ikke kan lese eller koble ut fra det verten lagrer; det er det som prøves her.
- Ikke varsel på skjermen ved ny post, hvis du ikke sier noe annet (spørsmål 5 i §6). Klienten får ny post uten å spørre (A7).
- Ikke sikkerhetskopi av eierens nøkkel, hvis du ikke sier noe annet (spørsmål 5 i §6). Mister du nøkkelen på Macen, må cellene opprettes på nytt.
- Ikke Losens egen entitet (Book 33 §4A). Ingen nøkkel lages for Losen.
- Ikke flytting av gamle meldinger. De blir i den gamle kanalen til de utløper.
- Ikke en ny utgave av vedleggsformålene. F1–F7 og svarene dine står i vedleggs-PDD-en og gjelder som de er.

Kapabiliteter og avhengigheter oppgaven bygger på:

| Nr. | Kapabilitet | Kilde | Avgrensning | Må virke før test? | Eier |
|---|---|---|---|---|---|
| 1 | Utgivelse av CellProtocol med broen (#53) | `_losen-queue/KOORDINERING.md`, kø-trådens innlegg 07.10 (A23 i §0) | `2026.9.5` = `main` med #53 og PR #60 venter per 07.10 kl. 12:32Z bare på ditt ja til merge og tag. Korrespondansens egne endringer rekker ikke den utgivelsen. De trenger en utgivelse til, etter nr. 4 og 5. | Ja | Kø-tråden og bro-tråden; ditt ord |
| 2 | Autentisert bro-rute i CellScaffold (`/bridgehead/<publisher>/<broId>`, også for delt forbindelse), og en bro-del i `/health/ready` | HD-0166; `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/PLAN.md`, AP5 og AP6 | Ikke påbegynt. Uten den når ingen klient cellene. N35 gjelder den delte forbindelsen klienten bruker. | Ja, før A5 og alt som bygger på A5 | Codex (bro-tråden) |
| 3 | Korrespondanseklienten gjør håndtrykket og abonnerer over broen | `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/PLAN.md`, AP7; A22 i §0 | Klienten på `main` i HavenAgentD er ikke endret siden før #53, og bruker bare `get` og `set`. Om et abonnement over broen virker fra en klient utenfor Binding, er ikke prøvd. | Ja, før A5 og A7 | Codex (Kjetils valg 07.10) |
| 4 | Relasjonsmodellen gjort ferdig i CellProtocol og klienten | A7–A10 og A19–A22 i §0 | Mangler: eieren som deltaker også for vedlegg, levering med Flow og `state`, og innslipp og invitasjon signert på eierens Mac. Planen (G2) starter med en liten prøve av innslippet, lokalt, før noe annet bygges på det. | Ja, før A1–A4 og A7 | Codex skriver; Fabel gjennomgår; Codex eller du merger |
| 5 | Vedleggsgrenen oppå ny `main`, tilpasset punkt 4, gjennomgått | A6 og A10 i §0 | Lokal gren. HavenAgentD får ikke pinne en CellProtocol-revisjon som ikke ligger på CellProtocols `main` (spørsmål 3 i §6). | Ja, før B | Codex; Fabel gjennomgår |
| 6 | HavenAgentD `main` grønn | A16 i §0 | Rød i dag. PR #28 først, så PR #30 og vedleggene. | Ja, før pakken bygges | Codex (#28); korrespondanse-tråden (#30 og vedlegg) |
| 7 | Signering og notarisering av hele pakken | `HavenAgentD/Packaging/build_pkg.sh` og `HavenAgentD/Packaging/notarize_pkg.sh`; HD-0107 | HD-0107 er åpen (pakken mangler ressurser og riktige sjekksummer). Det lille pilotskriptet signerer ikke, og brukes ikke. | Ja, før C1 | Codex; nøklene ligger på Macen din |
| 8 | Utsetting til staging | `haven-deploy` på verten | Tjenerdelen må ut i en utgivelse av CellScaffold, helst den samme som bro-ruta. | Ja | Codex eller du utfører, på ditt ord; kø-tråden sier når |
| 9 | Sikkerhetskopi av korrespondansetilstanden før tjenerendringen | `HavenAgentD/Docs/CorrespondenceS6ChangeSetAndRollback.md`, «Preconditions» | Ikke tatt. De gamle meldingene skal ikke flyttes, bare kunne gjenopprettes. | Ja, før første utsetting | Den som setter ut |
| 10 | Godkjenningen på Macen | HavenAgentD, grenen `pdd/agent-menylinje-og-varsler`: adminvinduet med «Trenger deg» (`CellProtocolDocuments/Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/`, G1-GUI godkjent 10.09) | Adminvinduet ligger på en gren som ikke er på `main`. Kortet for korrespondanse er nytt, og krever bilde før det bygges. Adminsiden på staging brukes ikke for den nye korrespondansen. | Ja, før C2 | Codex |
| 11 | Touch ID eller passord på Macen din | — | Bare du kan godkjenne, og Macen må være på. | Ja, for C2 og for hver godkjenning | Kjetil |
| 12 | Plass til vedlegg på staging | Ikke målt | Hvor mye ledig plass datadisken har, og om vedleggene kommer med i sikkerhetskopien, måles i planen. | Ja, før B2 | Korrespondanse-tråden måler |
| 13 | Prøveparets tilgang i den gamle kanalen | `HAVEN-Deploy/_handoff/HD-0006/` | Går ut 08.10 kl. 13:03Z. Fornyes i prøven som pågår (HD-0006). Uten den kan T-D1 ikke kjøres. | Ja, for D1 | Korrespondanse-tråden; ditt ord om root |
| 14 | Mottakernes maskiner | A15 i §0 | Ukjent. | Avgjør om Intel må prøves | Du spør dem |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.

| Nr. | Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|---|
| 1 | Godkjenningen på Macen: kortet under «Trenger deg», lenken som lages, og tilstandene venter, godkjent, avslått og feil | bilde | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/images/godkjenning-paa-macen-v1.png` | Lagt fram 07.10 sammen med G1. Du godkjenner bildet (G1-GUI). | nei |
| 2 | Det mottakeren ser under oppsettet: pakken installert, lenken gitt til agenten, ferdig, og feil | bilde | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/images/mottaker-oppsett-v1.png` | Lagt fram 07.10 sammen med G1. Du godkjenner bildet (G1-GUI). | nei |
| 3 | Pakketeksten: meldingen du videresender, og veiledningen i pakken. Den sier hva tjeneren kan se (at en celle finnes, når og hvor mye som sendes, og at en melding er kvittert), hva den ikke kan se, og at hvem som står bak en agent, ikke kan etterprøves kryptografisk ennå | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/TIL-VEGAR.md` og `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/TIL-VICTORIA.md` (lenkene selv ligger privat) | Book 33 §4.2 og §5.3. Du godkjenner teksten. | nei |
| 4 | Forslag til endringer i Book 33: vedlegg er ikke lenger et ikke-mål; avtalen har de fire handlingene, abonnement og historikk, og de ti vedleggshandlingene; eieren er selv part og slipper inn fra sin egen maskin; ytterdelen av konvolutten har ett felt til (S10) | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/BOOK-33-ENDRINGSFORSLAG.md` | Boka endres ikke uten ditt ord. | nei |
| 5 | Rapporten fra Astras gjennomgang av relasjonsmodellen og vedleggene, med ett utfall per funn | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/evidence/ASTRA-GJENNOMGANG.md` | T-A1, T-B1 | nei |
| 6 | Utskrift fra staging av en relasjonscelle etter en prøvemelding: ikke innhold i klartekst, ingen navn, ingen nøkkel, to medlemmer | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/evidence/celle-utskrift-staging.txt` | T-A2, T-A3 | nei |
| 7 | Prøveparet: melding og vedlegg begge veier mot staging, med binæren fra pakken | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#proevepar` | T-A1, T-A5, T-B2 | nei |
| 8 | Pakken: én fil, signert og notarisert | fil | `HAVEN-Deploy/_handoff/VEGAR/` (navnet settes i planen), med utskriften fra Gatekeeper-kontrollen ved siden av | T-C1 | nei |
| 9 | Skjermopptak av oppsettet på en Mac uten HAVEN, med håndgrepene telt | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/evidence/oppsett-ren-mac.mov` | T-C1 | nei |
| 10 | En tilgang som går ut, og som fornyes uten drift | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#fornyelse` | T-C3 | nei |
| 11 | Macen din på den nye klienten | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#kjetils-mac` | T-C4 | nei |
| 12 | Vegars og Victorias egne ord om at melding, installerpakke og budsjett kom fram og kunne brukes | deres svar | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/ACCEPT.md#mottakerne` | T-R, T-B3 | nei |
| 13 | Den gamle kanalen før og etter hver utsetting, og de gamle tilgangene trukket til slutt | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#gammel-kanal` og `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#overgang` | T-D1, T-C5 | nei |

## 3b. Hvem gjør hva, hva du må gjøre, og hvor lang tid det tar

To løp, etter Kjetils valg 07.10. Det som skal inn i CellProtocol, går inn der og ut i en utgivelse først.

| Ledd | Hvem | Venter på |
|---|---|---|
| 1. En liten prøve av innslippet, lokalt: en avtale signert på én maskin slipper inn et medlem i en celle som kjører på en annen | Codex | G1 |
| 2. Cellen i CellProtocol: eieren som deltaker også for vedlegg, levering med Flow og `state`, innslipp og invitasjon fra eierens Mac, vedlegg til `main` | Codex; Fabel gjennomgår | Ledd 1, G2 |
| 3. Utgivelser av CellProtocol: `2026.9.5` med broen, og en til med ledd 2 | Kø-tråden; ditt ord | `2026.9.5`: bare ditt ja. Den neste: ledd 2 |
| 4. Bro-ruta i CellScaffold (HD-0166, HD-0190) | Bro-tråden | `2026.9.5` |
| 5. Klienten: samme klient for eier og invitert, håndtrykk og abonnement over broen, oppsett fra én lenke, kortet i adminvinduet | Codex | Ledd 2; bildene |
| 6. Staging: huse cellene, lagre vedlegg, rydde ved utløp | Korrespondanse-tråden; Astra gjennomgår | G1, G2; kan skrives mot et lokalt bygg av ledd 2, men settes ikke ut før ledd 3 |
| 7. Pakken: bygg, signering, notarisering | Codex | Ledd 3 og 5 |
| 8. Prøveparet mot staging, og pakken på en ren Mac | Korrespondanse-tråden | Ledd 4, 6 og 7 |
| 9. Macen din over på den nye klienten | Korrespondanse-tråden; du installerer | Grønt prøvepar |
| 10. Vegar og Victoria | Dem og deg | Ledd 9 |

**Tid.** Jeg har ikke et tall jeg kan stå for før ledd 1 er gjort. Anslaget i iterasjon 2 var fem til ni uker for korrespondanse-trådens ledd etter hverandre, tre til fem i to løp, og fire til sju arbeidsdager til for en eiernøkkel på Macen. Det er ikke kontrollert. Det er uten gjennomgangsrunder, broen, pakken og utgivelsene, og levering over Flow og invitasjon fra Macen er ikke med i det. Nytt anslag kommer med planen.

**Følge for den gamle kanalen.** Fornyelsen er prøvd på prøveparet (grønn 07.10 kl. 10:01Z, `HAVEN-Deploy/_handoff/HD-0006/maal/PROEVE-9-AKTIVER-20261006.md`), og Kjetil sender den til Vegar og Victoria. Tilgangene de får, gjelder til 05.11. Er det nye ikke ute da, må den gamle kanalen fornyes én gang til.

**Det du selv må gjøre.**

Nå:
1. Sende fornyelsen av den gamle kanalen til Vegar og Victoria (meldingene ligger klare under `korrespondanse-privat-20261006/`), og godkjenne forespørslene deres. Vegars tilgang går ut 08.10.
2. Svare på de fem spørsmålene i §6 (G1, delegering, vedlegg til `main`, bildene med koden, og det som ikke er med i første pakke).
3. Si ja eller nei til merge og tag av CellProtocol `2026.9.5` (kø-tråden har spurt).

Senere, samlet i så få runder som mulig:
4. Godkjenne planen (G2).
5. Si «merge» for hver PR, og ja til hver utsetting til staging. Si ja eller nei til endringsforslaget til Book 33.
6. Installere pakken på din egen Mac, og svare «Tillat alltid» når macOS spør om nøkkelringen. Den gamle klienten blir stående ved siden av til begge mottakerne er over.
7. Godkjenne pakketeksten.
8. Per person (én prøveidentitet først, så Vegar og Victoria): lage lenken i vinduet, sende pakken og lenken, sammenligne koden, og godkjenne.
9. Si hvilken installerpakke og hvilken budsjettfil som skal sendes som vedlegg, og hvem som skal ha budsjettet.
10. Når begge har bekreftet: si at de gamle tilgangene kan trekkes (C5), og om G3 er godkjent.

Hvilken Mac og macOS Vegar og Victoria har, er spurt om i meldingene om fornyelsen 07.10.

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

**Lærdommene som har formet §1–§3** (hele registeret står under, slik verktøyet la det inn):

- `lesson.plan-instead-of-delivery`: «Et dokument om leveransen teller aldri som leveransen.» Derfor er R ikke oppnådd før Vegar og Victoria har brukt det (T-R).
- `lesson.read-origin-main-before-writing-a-mechanism`: les det som ligger på `origin/main`, før en mekanisme bygges. Derfor er A7–A9 lest på `origin/main` i dag, og derfor starter planen med en liten prøve av relasjonsmodellen (§2 nr. 4).
- `lesson.stand-in-kept-less-than-the-server-keeps`, og funnet 06.10 i HD-0006 (byttet av invitasjoner var prøvd grønt mot en etterligning som ikke kjente fila verten setter lista fra). A7–A10 er samme slag: testene av klienten er grønne mot en oppstilling der motparten eier cellen, og ingen test lar to inviterte skrive til hverandre. Derfor går T-A1 og T-B2 mot staging selv, med binæren fra pakken, og begge parter bruker klienten.
- `lesson.ciphertext-field-held-plaintext-hash`: «En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet.» Derfor leser T-A2 og T-A3 bytene staging har lagret, i flere kodinger.
- `lesson.location-is-not-ownership`: du sa at en celle i skyen som du eier, er innenfor din entitet. Det taler for valg 1b. Det står i valget.
- `lesson.corr-approval-surfaces-timed-out`: avhengigheter føres som egne rader med eier. Derfor står broen, utgivelsene, signeringen og adminflatene i §2.
- `lesson.corr-grant-expired-without-renewal-path`: «En tilgang eller et bevis med utløpstid tas ikke i bruk før fornyelsesveien er testet ende til ende» Derfor er fornyelsen (C3) med i første pakke, og prøves på prøveparet før noen får pakken.
- `lesson.what-a-recipient-has-was-read-off-our-own-disk`: derfor står mottakernes maskiner som ukjent (A15), og du må spørre dem.
- `lesson.linux-green-and-a-read-through-were-not-a-run-on-macos`: derfor prøves pakken på en Mac, i en ren bruker, før noen får den (T-C1).
- `lesson.text-ux-is-not-design`: derfor godkjenner du bildene av kortet og av mottakerens oppsett, ikke en beskrivelse av dem.
- `lesson.host-mutation-without-reading-the-coordination-file`: hver utsetting går gjennom køen med egen claim.
- `lesson.estimate-assumed-one-attack-round`: derfor er anslagene i §3b per ledd, med runder i tillegg.
- `lesson.new-cell-must-declare-its-provisioning-mode` og `lesson.cellscaffold-two-holes`: en ny lagret celle i CellScaffold må si hvordan den opprettes, og tilgang skal prøves på nøkkelstien. Planen (G2) må svare på begge for relasjonscellen.


## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra. Er bildet en mockup i stedet for Porthole-preview, kreves i stedet en renderingserklæring i images/README.md som lister hva skjelettet ikke kan rendre.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.

## Lærdommer du må lese før dekomponering
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.stop-rule-too-wide-stops-the-job** (2026-09-09, minor): En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.
    - forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pkill-pattern-killed-the-queue-job** (2026-09-10, major): En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.
    - forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.
- **lesson.queue-job-file-before-prompt** (2026-09-10, minor): Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.
    - forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.readonly-git-is-not-all-git** (2026-09-24, minor): Et `git status` fra device_bash i CellProtocolDocuments etterlot .git/index.lock (0 byte) som ikke kunne fjernes fra VM-en, selv om git show/grep/log/rev-parse i samme økt ikke gjorde det.
    - forebygging: Fra device_bash bare objektlesende git mot en revisjon (git show/grep/log/cat-file <rev>); aldri status, diff mot arbeidstreet, add eller commit. Finnes en lås likevel: flytt den til _to_delete/ (mv virker, rm gjør ikke).
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.jxa-objc-method-without-arguments-is-a-property** (2026-09-24, minor): `a.terminate()` i JXA ga `TypeError: a.terminate is not a function`, men appene avsluttet likevel.
    - forebygging: Skriv `a.terminate` (uten parentes) og sjekk etterpå med `pgrep` at prosessen er borte før du går videre.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.sketch-assumed-a-renderer-it-did-not-have** (2026-09-25, major): Skissen v2 (HTML) var venstrestilt, men «Utvid entiteten» i HAVEN viste all tekst sentrert, også etter at hAlignment «leading» var satt.
    - forebygging: Før en skisse godkjennes: finn CellProtocol-committen HAVEN-bygget bruker, les hvordan Text/VStack/HStack rendres der, og list i §3 hva den ikke kan (her: venstrestilt tekst). Et HTML-bilde er ikke bevis for at rendreren kan det samme.
- **lesson.maxwidthinfinity-also-stretches-height** (2026-09-25, minor): En tekst i en listerad ble kuttet med «…» etter fem linjer når en HStack med wrap og maxWidthInfinity sto i samme rad; uten maxWidthInfinity ble teksten hel.
    - forebygging: Ikke sett maxWidthInfinity på elementer i listerader. Se etter «…» i skjermbildet av hver rad med lang tekst, i et smalt vindu.
- **lesson.wrap-gives-each-item-its-ideal-width** (2026-09-25, minor): Knappen «Par agenten med denne HAVEN-en» gikk ut over kortet og ble klippet i et smalt vindu.
    - forebygging: Knapper i vanlig HStack, som kan krympe og bryte teksten; wrap bare for korte merkelapper. Se på flaten i et smalt vindu før den vises fram.
- **lesson.empty-list-keeps-its-slot** (2026-09-25, minor): Tomme lister og tomme tekster ga store hull i «Utvid entiteten».
    - forebygging: Én liste per kort, der cellen bestemmer radene (`kind`) og en rad med en kort linje står der det ellers ville vært tomt. Ingen faste høyder på lister, og ingen tekst på toppnivå som kan bli tom.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.text-field-sends-a-string** (2026-09-25, major): Adressefeltet i «Utvid entiteten» kunne aldri starte en forespørsel: Enter ga alltid «Si hvilket scaffold dette gjelder — `audience` …».
    - forebygging: For hvert tekstfelt: en kontraktstest som sender feltets egen payload (.string) til targetKeypath og venter et svar som ikke er feil.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.placeholder-example-leaks-into-judgement** (2026-09-28, minor): I «Dommerbenken — chat» v2 var plassholderen i fritekstfeltet «f.eks. «status på prosjektet»». Kjetil skrev nøyaktig «status på prosjektet» som sin egen tolkning i to av tretti saker («hvor står vi nå på prosjektet», «hva står igjen»). Eksempelet var hentet fra meningen til en sak i settet.
    - forebygging: Eksempler, plassholdere og hjelpetekst i en dommerflate skal hentes fra et domene som ikke finnes i settet, og testes: ingen sak i settet skal ha gold hvis tittel eller alias overlapper eksempelteksten. Rapporter saker der dommerens fritekst er lik eksempelet som svakere.
- **lesson.corr-grant-expired-without-renewal-path** (2026-09-30, major): 30.09 fikk Vegar `recipient_not_allowed` da han sendte til `kjetil-vegar-codex-d`, Kjetils klient avviste sitt eget bevis, og meldingen til Victoria ble avvist på samme måte; korrespondansen sto stille i over ett døgn.
    - forebygging: En tilgang eller et bevis med utløpstid tas ikke i bruk før fornyelsesveien er testet ende til ende (utløpt tilgang → fersk invitasjon → eiergodkjenning → ny frist → sending virker), og fristen står i pilotens STATUS med en påminnelse minst sju dager før.
- **lesson.renewal-invite-must-carry-device-id** (2026-09-30, major): Gjennomgangen av korrespondanseklienten 30.09 viste at `setup` gjenbruker `identity.json`, men tar enhets-ID-en fra invitasjonen (`invite.deviceID ?? tilfeldig`); en fornyelsesinvitasjon uten profilens `deviceID` ville gitt ny enhet og `principal_already_enrolled` i stedet for fornyelse.
    - forebygging: En fornyelsesinvitasjon lages bare med `deviceID` hentet fra deltakergrafen eller profilen (`haven-correspondence-mcp identity`), og generatoren nekter uten; test: fornyelsesinvitasjonens `deviceID` er lik profilens, og `setup` gir `pending_approval` med `renewsGrantID`.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.md5-differs-for-images-written-from-the-cloud** (2026-10-02, minor): Etter at seks PNG-filer ble skrevet fra en Cowork-økt til Macen, stemte ikke md5 mot originalene, mens alle tekstfilene stemte. Det så ut som feilen der en gammel utgave blir skrevet.
    - forebygging: Kontroller tekstfiler med md5. Kontroller bilder ved å sammenligne `IDAT`-dataene eller størrelsen minus `caBX`-blokken, ikke md5 av hele fila. Test: kontrollskriptet for overførte filer skiller de to tilfellene.
- **lesson.deployed-after-the-attack-was-known** (2026-10-03, major): To utgaver av en vakt ble satt ut etter at angrepet mot dem var målt; den første ble lagt i køen 5 minutter og 28 sekunder etter at målingen viste 20 av 40 publisert.
    - forebygging: Et frosset angrep måles mot en utgave før den pushes, og skriptet som pusher og setter ut, startes først når målingen er lest. Test: tidspunktet for angrepsmålingen i TESTRESULT.md er før tidspunktet for push.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.container-log-dies-with-the-container** (2026-10-03, major): Loggene til to utgaver gikk tapt ved neste utsetting, så ingen kan si hva gjester fikk i de periodene; ved det tredje byttet skulle kjeden lese 24 timer av en logg på 25 timer og 18 minutter.
    - forebygging: Rett før en container byttes, leses loggen fra containeren startet, med et vindu som er lengre enn oppetiden, og beviset sier hvor lenge før byttet den ble lest. Test: bevisfilen har containerens starttid, lesetidspunkt og linjetall, og vinduet er lengre enn oppetiden.
- **lesson.red-check-rerun-because-the-cause-looked-like-the-network** (2026-10-03, major): Deployens egen kontroll ble rød på én av 25 rader (kode 000, kallet kom ikke fram). Tråden kjørte de samme kontrollene om igjen, fikk grønt og gikk videre, mot planens stopp-regel.
    - forebygging: En rød kontroll stopper kjeden uansett årsak. Rapporten sier hvilke rader som er kall som ikke kom fram, og kontrollen kjøres ikke om igjen uten eierens ord. Test: kjedeskriptet avslutter ved første røde kontroll og har ikke noe nytt forsøk på en hel kontroll.
- **lesson.status-reader-gave-up-at-the-first-network-error** (2026-10-03, major): Skriptet som ventet på CI for en utgave, ga opp ved første nettfeil. Utgaven lå bygget, men ikke satt ut, i tre timer, mens den forrige sto på nett med hull et angrep hadde vist.
    - forebygging: Lesing av et utfall som ligger et annet sted, prøves på nytt når ingen svar kom, og skriptet sier hvor mange ganger; et rødt utfall stopper. Det er lesing, ikke en kontroll som er blitt rød (se lesson.red-check-rerun-because-the-cause-looked-like-the-network). Test: venteren kjørt uten nett leser igjen og skriver antall forsøk.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.failure-named-by-a-guess** (2026-10-03, minor): En kjede leste CI-utfallet tjue ganger uten nett og meldte «gh er ikke logget inn» hver gang; innloggingen var i orden.
    - forebygging: Et skript skriver ut det kommandoen sa, eller prøver nettet før innloggingen. Test: skriptet kjørt uten nett melder at det ikke fikk kontakt.
- **lesson.claim-on-another-resource-does-not-stop-a-deploy** (2026-10-03, major): En annen tråd tok claim på host-disk på verten og tømte systemlogger der mens en utsetting med claim på palazzo-staging-app pågikk. Utsettingen kjørte tre forsøk til, og ingen ble stoppet eller varslet.
    - forebygging: Aktive claims for verten leses rett før hvert forsøk på utsetting (`hd coord status`), og enhver claim på samme vert stopper forsøket, uansett ressurs. Dette er strengere enn lesson.host-mutation-without-reading-the-coordination-file, som sier «på samme tjeneste». Test: jobbloggen for hvert forsøk viser lesingen av claims, og ingen andre sto.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.linux-green-and-a-read-through-were-not-a-run-on-macos** (2026-10-05, major): Fila mottakerne skulle kjøre, var grønn i 52 tester på Linux under tre skall og gjennomgått for macOS av en uavhengig kontroll, og var rød i de to første kjøringene på Macen: den kunne velge en eldre invitasjonsfil, og seks feilmeldinger ble til «unbound variable» i Terminal.
    - forebygging: Et skript som mennesker skal kjøre på en Mac, kjøres på Macen før det kalles ferdig: med /bin/bash, én runde uten språkinnstilling og én med UTF-8, mot en stedfortreder i en midlertidig mappe. Test: selvtesten skriver to runder og er rød på en maskin uten UTF-8, jobbnummeret for den grønne kjøringen står i LES-MEG, og en test nekter en variabel uten klammer rett foran et tegn utenfor ASCII.
- **lesson.stand-in-kept-less-than-the-server-keeps** (2026-10-05, major): Skriptet for fornyelse kunne si «Tilgangen er på plass» med et bevis tjeneren avviser (profilen lagt tilbake fra kopi, så godkjenning, så aktivering), og alle testene var grønne; en uavhengig kontroll fant det ved å lese tjenerens kilde.
    - forebygging: En stedfortreder fører hver post den ekte tjenesten fører, og endrer dem bare der kilden gjør det. Tilstanden en test starter fra, bygges ved å kjøre stedfortrederens egne steg, ikke ved å skrive den for hånd. Test: én test går gjennom rekkefølgen kontrollen fant, og krever at skriptet sier «IKKE I ORDEN».
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.what-a-recipient-has-was-read-off-our-own-disk** (2026-10-05, minor): Formålsspesifikasjonen og koordineringsfila sa at begge mottakerne har pakken HAVENAgentD-0.3.2-universal2.pkg; den ene fikk en usignert pilotpakke, og fila hun fikk, er ikke funnet.
    - forebygging: Hva en mottaker har, leses av det som ble sendt til den mottakeren: pakkemappen og meldingen, én rad per mottaker. Finnes det ikke spor, står det «ukjent», og det som bygges, må tåle begge. Test: påstandstabellen har én rad per mottaker med fila som belegger den, og skriptet finner klienten både der pakken og der pilotpakken legger den.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://questionnaire.delivery.consent [active] — Questionnaire delivery and consent
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | ./<skript>.sh (uten --go) | TESTRESULT.md#dry-run | venter |
| T-R | `i-bruk-hos-mottakerne` | Vegar og Victoria gjør hver sin runde med den nye pakken: les en melding, svar, hent et vedlegg, send et vedlegg. Svarene deres føres ordrett, sammen med cellens egne tall for relasjonen (antall meldinger og hentede vedlegg). «Sendt» alene består ikke. | ACCEPT.md#mottakerne | venter |
| T-A1 | `to-parter-i-en-celle` | Prøveparet mot samme celle på staging, med binæren fra pakken (sjekksum føres). Den ene prøveidentiteten eier cellen, den andre er invitert. Hver side leser, sender, kvitterer, sender et vedlegg og henter et vedlegg. Ti handlinger, ti utfall. Medlemslista leses: nøyaktig to. Før dette, i planens første steg: samme ti handlinger lokalt mot en celle i en testprosess. | TESTRESULT.md#proevepar | venter |
| T-A2 | `staging-huser-konvolutter` | Send en prøvemelding der emne og innhold har hver sin tilfeldige merkelapp. Les bytene staging har lagret for cellen, og søk etter merkelappene som de står, og i base64, base64url, heksadesimalt og UTF-16. Null treff. Kontroll på at søket virker: mottakeren åpner samme melding og finner begge merkelappene. Send klartekst rett til cellen: skal avvises. | TESTRESULT.md#celle, evidence/celle-utskrift-staging.txt | venter |
| T-A3 | `tjeneren-er-ikke-mottaker` | Les medlemslista: de to prøveidentitetenes numre og ingen andre. Les mottakerlista i hodet på den lagrede konvolutten: nøyaktig de samme to. Søk i alt staging har lagret, og i miljøet til prosessen, etter prøveeierens private nøkler: null treff. Kontroll: samme søk finner dem på prøveeierens maskin. Prøv å gi en tredje identitet en avtale fra tjeneren, uten eierens signatur: cellen avviser, og en klient som får en slik avtale, avviser den. Søk i det staging har lagret for korrespondansen etter prøveidentitetenes visningsnavn, profilnavn og maskinnavn, i de samme kodingene som i T-A2. Null treff. Kontroll: de samme ordene finnes i klientens egen profilfil. | TESTRESULT.md#blind | venter |
| T-A4 | `smal-avtale-ved-innmelding` | Over broen, med prøveidentitetene: les avtalen klienten fikk, og tell handlingene (de fire, abonnement og historikk, og de ti vedleggshandlingene). Kall `audience.inviteIdentities` med den: skal gi `grantNotHeld`. Kall en vedleggshandling med en avtale uten vedleggshandlingene: skal avvises. | TESTRESULT.md#avtale | venter |
| T-A5 | `over-autentisert-bro` | To prøveidentiteter mot staging over broen, én melding hver vei. En forbindelse uten håndtrykk: skal stenges før cellen. En identitet med håndtrykk, uten avtale: `grantNotHeld`. `strings` på klientbinæren i pakken gir null treff på `assistant-correspondence/v1`; kontroll: samme søk gir treff i den gamle binæren fra pakken 08.09. | TESTRESULT.md#bro | venter (avhenger av HD-0166) |
| T-A6 | `utloep-fjerner-alt` | En prøvemelding med ti minutters levetid. Ingen kaller cellen etterpå. Før utløp finnes meldingsnummeret i det staging har lagret (kontroll). Sytti minutter etter utløp finnes det ikke, verken i ytterdel eller innerdel. | TESTRESULT.md#utloep | venter |
| T-A7 | `levering-uten-spoerring` | To prøveidentiteter mot staging over broen. Mottakeren abonnerer. Avsenderen sender en melding med en tilfeldig merkelapp. Mottakerens klient har konvolutten innen ti sekunder uten å ha kalt `inbox` eller `readMessage` (klientens logg over utgående kall viser det), åpner den og finner merkelappen. Koble mottakeren fra, send tre meldinger, koble til: `get state` gir alle tre. En identitet med håndtrykk, men uten avtale, abonnerer: den får ingen hendelser, og `state` blir avvist. Det abonnenten fikk over Flow, leses: søk etter merkelappen gir null treff i det som ikke er åpnet. | TESTRESULT.md#levering | venter |
| T-B1 | `vedlegg-paa-main` | Ren klone fra GitHub til en tom mappe; bygg og test begge repoene. Rapporten fra Astras gjennomgang ligger ved, med ett utfall per funn: rettet, eller skriftlig godtatt av Kjetil. | TESTRESULT.md#vedlegg-main, evidence/ASTRA-GJENNOMGANG.md | venter |
| T-B2 | `staging-baerer-vedlegg` | Den faktiske installerpakken og en fil på 200 MB, hver vei mot staging; sjekksum hos mottakeren, og minnetopp hos klient og tjener føres. Hent etter utløp og etter tilbakekall: skal avvises, og mappen på disken listes før og etter. Omstart av staging midt i en opplasting: klar feil, og en ny sending lykkes. Med mindre ledig plass enn terskelen (prøvd ved å sette terskelen over det som er ledig): avvist, og null filbyte sendt. | TESTRESULT.md#vedlegg-staging | venter |
| T-B3 | `installerpakke-og-budsjett` | T2 og T3 i vedleggs-PDD-en, med pakken og budsjettfila Kjetil navngir. | ACCEPT.md#mottakerne | venter |
| T-C1 | `mottaker-en-pakke-ett-haandgrep` | En ren bruker på en Mac uten HAVEN: installer, gi agenten lenken, send koden, med skjermopptak. Tell håndgrepene: høyst tre (pakken, lenken, koden). Gjenta oppå 0.3.2. `spctl --assess --type install` på pakken skal si «accepted», `codesign --verify --deep --strict` på det installerte skal gå gjennom, og `lipo -archs` skal vise begge arkitekturer. Intel prøves bare hvis en mottaker har det, og da på en Intel-Mac; ellers sier pakketeksten at Intel ikke er prøvd. | TESTRESULT.md#pakke, evidence/oppsett-ren-mac.mov | venter |
| T-C2 | `en-godkjenning-per-person` | Du lager en lenke i vinduet og godkjenner en prøveidentitet der. Håndgrepene dine telles: fire per person (lage lenke, sende, sammenligne kode, godkjenne). Uten Touch ID eller passord: verken lenke eller godkjenning. Det godkjente bildet står ved siden av et skjermbilde av den ferdige flaten, i samme størrelse. Avslag prøves. Én forespørsel lages med en annen nøkkel enn den prøvemottakeren viser: koden på kortet skal da ikke stemme med den prøvemottakeren ser. Kortet leses for navn: bare navnet du selv ga lenken, og det finnes ikke i det staging har lagret. | ACCEPT.md#kort | venter |
| T-C3 | `tilgang-uten-driftsrunder` | Fra en lenke lages på Macen til prøvemottakeren har lest sin første melding: journalen på verten viser ingen `haven-deploy`, ingen endring under `/etc/haven` og ingen innlogging som root i det tidsrommet. En prøveidentitet får en avtale på femten minutter. Etter utløp: klienten sier i klare ord at tilgangen er utløpt, og hva som må gjøres. Du fornyer med ett trykk. Klienten henter den nye avtalen og virker igjen, uten ny installasjon. En lenke brukes to ganger: den andre gangen blir avvist. En lenke som er eldre enn sju dager, blir avvist. Trekk tilgangen i vinduet: prøvemottakerens neste kall blir avvist. Bytt nøkkel på prøveidentiteten: det kreves en ny forespørsel. | TESTRESULT.md#fornyelse | venter |
| T-C4 | `kjetils-mac-samme-pakke` | Les oppsettet agentene dine bruker for den nye korrespondansen: hvilken programfil starter de? Sjekksummen av den fila er lik den i pakkens liste over sjekksummer (`release-manifest.json`, som bygget legger ved siden av pakken). En melding sendt med ferdighetene dine kommer fram hos prøvemottakeren. Oppsettet for den gamle kanalen leses også: det peker fortsatt på den gamle klienten, og T-D1 er grønn etterpå. | TESTRESULT.md#kjetils-mac | venter |
| T-C5 | `overgangen-fullfoert` | T-R er grønn for begge. Etter ditt ord: de to gamle tilgangene står som trukket på adminsiden, og et sendeforsøk til hver av dem fra prøveparet i den gamle kanalen blir avvist. Antall gamle meldinger er det samme før og etter. | TESTRESULT.md#overgang | venter |
| T-D1 | `gammel-kanal-staar` | Før og etter hver utsetting til staging: prøveparet sender én melding hver vei i den gamle kanalen og leser den. Fire utfall per utsetting. | TESTRESULT.md#gammel-kanal | venter (krever at prøveparets tilgang er fornyet, HD-0006) |
| T-D2 | `ingen-klartekst` | Tell meldinger i de nye cellene før første nye melding: null. Sperr broen i en prøve og send: klienten skal feile med en klar melding, og den lokale loggen over utgående kall viser ingen sending. Statisk kontroll som i T-A5: binæren har ikke adressen til den gamle ruta. | TESTRESULT.md#ingen-klartekst | venter |
| T-D3 | `ingen-agent-uten-ja` | Les verktøylista og avtalen agentens klient holder. List sendingene fra din identitet i prøven, og hold dem mot det du har sagt ja til. Prøv å slippe inn en prøveidentitet fra agentens prosess, uten Touch ID eller passord: skal avvises. Prøv det samme fra tjeneren: skal avvises (T-A3). At en agent sender i ditt navn, hindres fortsatt av regelen din og ikke av en lås. Det føres som det er, ikke som bestått. | ACCEPT.md#agent | venter |
| T-D4 | `ingen-verdi-i-logg` | Legg en merkelapp i én bevisfil med vilje, og søk i alle bevisfiler og logger fra prøven etter prøvenøkler, prøvekoder, prøvetekst og merkelappen. Bare merkelappen skal gi treff. | TESTRESULT.md#ingen-verdier | venter |

Radene som begynner med `test.`, er lagt inn av verktøyet. Radene som begynner med `T-`, hører til bladformålene i §1. `TESTRESULT.md`, `ACCEPT.md`, `evidence/` og `images/` ligger i oppgavemappen, `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Hver `T-`-test er skrevet slik at den blir rød hvis målet ikke er nådd. Der et søk skal gi null treff, står det også hva som viser at søket kan finne noe.

## 6. Åpne spørsmål til Kjetil

Fem spørsmål, de samme som i `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/G1-KORT.md`. Anbefalingen min står i hvert.

1. **G1:** er de sju punktene i «Kort sagt» det du vil ha? Et ja godkjenner punktene, ikke standardvalgene under (S1–S10).
2. **Venter delegering til etter første pakke?** Book 33 §10 punkt 5 sier at en pakke ikke forlater huset før en delegert assistentidentitet sender, og mottakeren verifiserer både assistenten og hvem som står bak. Det finnes ikke i koden (A11 i §0). Anbefalt: ja, den venter. Agentene bruker identitetene som i dag, og pakketeksten sier rett ut at hvem som står bak en agent, ikke kan etterprøves kryptografisk ennå. Det krever ditt uttrykkelige ord, for boka sier at alle seks punktene skal være vist først. Sier du nei, bygges delegeringen først: anslagsvis en til to uker mer, og en egen gjennomgang.
3. **Kan vedleggene gå til `main` før Vegar og Victoria har prøvd dem?** Vedleggs-PDD-en sier: «Funksjonsprøvene og de to mottakeroppgavene må begge bestå før noe foreslås mot main.» Regelen din fra 18.09 sier det samme om nye kapabiliteter. Men en pakke bygges fra `main`, og et skript i CI håndhever det (`HavenAgentD/Scripts/assert_dependencies_are_on_their_main.sh`). Anbefalt: ja, når funksjonsprøvene, en uavhengig gjennomgang og en lokal formålsprøve med to prøveidentiteter er grønne. Mottakerprøven er første ekte bruk, og den avgjør G3. Sier du nei, blir det to pakker: først kryptert tekst, så vedlegg. De andre endringene i cellen (ledd 2 i §3b) følger regelen din fra 18.09 som den står: testet mot funksjon og formål, lokalt, før `main`.
4. **Bildene (G1-GUI):** er `images/godkjenning-paa-macen-v1.png` og `images/mottaker-oppsett-v1.png` slik du vil ha det? De viser forslaget mitt om en kode på seks sifre: mottakeren ser seks sifre, regnet ut av nøkkelen sin, og sender dem til deg, og kortet ditt viser de samme. Uten koden har mottakeren ett håndgrep mindre, men da er lenken alene beviset, og den som får tak i lenken først, kan be om tilgang som mottakeren.
5. **Ikke i første pakke**, hvis du ikke sier noe annet: varsel på skjermen ved ny post (du har bedt om det to ganger, HD-0069 og HD-0093; klienten får posten uten å spørre, men varselet til deg er ikke med), vedlegg som referanse eller hent ved behov (du svarte 28.09 «Alle tre må støttes»; første pakke sender kopi, S1), og sikkerhetskopi av nøkkelen på Macen.

### Avgjort siden iterasjon 2

| Var | Avgjort | Grunnlag |
|---|---|---|
| Valg 1: hvem som slipper inn medlemmer | Kjetil eier cellene og er selv part. Nøklene hans ligger på Macen hans, og han slipper inn derfra. Modellen der tjeneren eier, er ute. | Kjetil 06.10 kl. 20:03Z og 07.10 («På Macen min») |
| Valg 2: hvordan han ser at en forespørsel er fra rett person | Ikke avgjort: forslaget er en kode på seks sifre, vist i vinduet på Macen og hos mottakeren (spørsmål 4). Navnet på lenken ligger bare på Macen. | Valget med navnet i nettleseren (2c) falt bort med valg 1 |
| Valg 5: invitere uten drift | Er et formål (C3): lenken lages på Macen, og staging røres ikke. | Følger av valg 1, og av «altfor mye manuelle operasjoner» |
| S2: varsel ved ny post | Levering uten spørring er med (A7), etter forslaget hans 06.10 om Flow og `get state`. Varsel på skjermen er ikke avgjort: spørsmål 5. | |
| S9: hvem som gjør CellProtocol og klienten | Codex. Korrespondanse-tråden tar staging og prøvene. | Kjetil 07.10 («Ja, to løp») |

### Standardvalg

S1 og S2 gjelder noe du har sagt eller bedt om før. Resten trenger du bare å lese hvis du vil ha noe annerledes.

| Nr. | Hva | Standard jeg har valgt | Følge | Si fra hvis |
|---|---|---|---|---|
| S1 | Hvordan vedlegg overføres. **Avviker fra svaret ditt 28.09 («Alle tre må støttes»).** | Som kopi i første pakke. | Avsenders krypterte kopi ligger på staging til meldingen utløper, til den kalles tilbake, eller til den er overdratt til mottakeren. «Referanse» og «hent ved behov» finnes i koden, men kan ikke nås mot en celle på staging (A18 i §0): de krever at avsenders celle kjører der filene ligger. For en installerpakke og et budsjett som ligger som filer hos deg, er kopi uansett modusen svaret ditt gir. | de to andre må virke mot Vegar og Victoria i første pakke. Det krever celler som kjører hos dere, og er et eget arbeid. |
| S2 | Varsel ved ny post | Levering uten spørring er med (A7). Varsel på skjermen: spørsmål 5 over. | | |
| S3 | Rydding ved utløp | En jobb på staging fjerner utløpte meldinger og vedlegg hver time. | A6 kan prøves uten at noen leser. I koden i dag fjernes en utløpt melding først neste gang noen kaller cellen. | det holder at de fjernes ved neste kall. Da endres A6 og T-A6. |
| S4 | Levetid for en melding | 30 dager når avsenderen ikke sier noe, høyst 90, som i koden. | Book 33 §5.2 sier at standarden for kontakt bør være lang, og at eieren skal kunne sette den per relasjon. Det siste er ikke bygget. | du vil ha andre tall i første pakke. |
| S5 | Hvor lenge en tilgang varer | Til sluttdatoen du setter når du godkjenner. Setter du ingen, ett år, som er det lengste koden tillater (`Contract.maximumDuration`). | Ingen fornyelse før den datoen. | standarden skal være kortere. |
| S6 | Plass til vedlegg | Ingen grense per fil (svaret ditt 28.09). Staging avviser et nytt vedlegg når datadisken har mindre enn 10 GB ledig. | Tallet er et forslag. Ledig plass måles i planen. | du vil ha en annen terskel. |
| S7 | Hvem som legger klienten inn hos mottakerens agent | Mottakerens agent gjør det selv, når mottakeren gir den lenken. | Installereren rører fortsatt ikke oppsettet til Claude eller Codex. Slik er det i dag: pakken skriver ut hva mottakeren selv må kjøre i Terminal, og det lille pilotskriptet lar med vilje oppsettet være (`HavenAgentD/Packaging/README.md`). | installereren skal gjøre det. |
| S8 | Hvilken pakke | Hele pakken, signert og notarisert. | Book 33 §10 punkt 6, og ordene dine 05.10. Ikke åpent; står her for at det skal være sagt. Det lille, usignerte pilotskriptet brukes ikke. | — |
| S9 | Hvem som gjør relasjonsmodellen ferdig i CellProtocol og klienten | Avgjort i iterasjon 3, se tabellen over. | | |
| S10 | Et nytt felt i klartekst | Ytterdelen av konvolutten har på vedleggsgrenen fått nummeret på avtalen vedlegget er bundet til. Feltet står. | Driften kan se at en melding har vedlegg. Book 33 §5.1 lister ikke feltet. Det samme nummeret står uansett i klartekst i kallet som sender meldingen, i vedleggshandlingene og i lagerets register, så å flytte feltet inn i den krypterte delen skjuler ingenting. Det legges inn i endringsforslaget til boka, og Astra får det som eget punkt. | du vil at det ikke skal synes for driften at en melding har vedlegg. Det er et større arbeid enn å flytte ett felt. |

### Det jeg ikke vet

- Om en avtale signert på eierens Mac kan slippe inn et medlem i en celle som kjører på staging, og hva som må endres for det. Det er første ledd (§3b).
- Om et abonnement over broen virker fra en klient utenfor Binding.
- Om bro-ruta bro-tråden gjør klar (HD-0190), dekker ruta korrespondansen trenger (HD-0166).
- Hva #53 gir en klient å bygge på for håndtrykket.
- Om adminvinduet fra grenen `pdd/agent-menylinje-og-varsler` kan bære kortet, og hva som gjenstår for å få den grenen til `main`.
- Hvilke Macer Vegar og Victoria har, og hva Victoria har installert. Spurt om i meldingene 07.10.
- Hvor mye ledig plass datadisken på staging har.
- Hvor mange runder gjennomgangene tar, og dermed tiden.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-06 | Opprettet | Losen |
| 1 | 2026-10-06 | Første utkast. Ikke lagt fram for Kjetil. En uavhengig kontroll (Fabel) sa: «Nei, ikke slik den står. Ja etter rettelsene 1–8». Rapporten: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/FABEL-G1-RUNDE-1.md`. | Korrespondanse-tråden |
| 2 | 2026-10-06 | Rettet etter kontrollen, og etter et funn gjort mens rettelsene ble etterprøvd i koden: koden dekker én eier og én invitert, klienten har bare en vei for den inviterte, og eieren kan ikke sende vedlegg (A7–A10). Treet har fått A1 (to parter i én celle) og C5 (overgangen). Varsel er tatt ut av treet og ført som standardvalg. Valgene er nå fem: hvem som slipper inn medlemmer, hvordan en forespørsel knyttes til en person, delegering, vedlegg til `main` før mottakerprøven, og invitasjon uten drift. Pakkevalget er ikke lenger et valg. Tidsanslaget er summen av leddene. Testene har fått kontroller som gjør at de ikke kan bli grønne uten at målet er nådd. Figuren er tegnet på nytt. To uavhengige kontroller (Fabel) leste utgaven før de siste rettelsene. Den ene leste koden bak A7–A10 og valg 1 og sa: «Ja, etter navngitte rettelser». Kjernen holder, men «eiersiden har ingen klient» var for sterkt sagt (vedleggstestene gir eieren en klient), og 1b og 1c var for enkelt beskrevet. Den andre leste hele spesifikasjonen og sa: «Ja etter rettelsene 1–5». Alle de navngitte rettelsene er tatt inn. Rettelsene selv er ikke lest av en kontrollør. Rapportene: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/FABEL-G1-RUNDE-2-MODELL.md` og `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/FABEL-G1-RUNDE-2-SPEC.md`. | Korrespondanse-tråden |
| 3 | 2026-10-07 | Skrevet om etter Kjetils ord 06.10 kl. 20:03Z («Jeg synes du har rotet det til. En chat celle må kunne brukes av eier også …») og de to svarene hans 07.10 («På Macen min», «Ja, to løp»). Kjetil eier cellene og er part, nøklene ligger på Macen hans, og han slipper inn derfra (A3, C2, D3). Levering over Flow og historikk med `state` er nytt formål (A7). Å invitere og fornye uten drift er formål (C3). Codex tar cellen, klienten og pakken; korrespondanse-tråden tar staging. De fem valgene er blitt fem korte spørsmål, og tre av de gamle valgene er avgjort eller falt bort. `G1-KORT.md` er skrevet om og er kort. To bilder er lagt fram for G1-GUI. Svaret Kjetil fikk 06.10 om hvordan cellene er skrudd sammen, ble kontrollert av en uavhengig leser før det ble sendt (`panel/FABEL-CHATSVAR.md`). Utkastet til denne iterasjonen ble kontrollert av en uavhengig leser (Claude Opus; Fabel hadde brukt opp kvoten): «Nei, ikke som den står», med sju ting som måtte endres (`panel/KONTROLL-G1-ITERASJON-3.md`). De er endret. Endringene er ikke kontrollert på nytt. | Korrespondanse-tråden |
