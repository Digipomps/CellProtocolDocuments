# Formålsspesifikasjon — kryptert korrespondanse med vedlegg, ut til Vegar og Victoria

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/` · Opprettet 2026-10-06 · Iterasjon 2 (**G1-forslag, ikke godkjent**)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

Skrevet av Claude-tråden i prosjektet «HavenAgentD». Den heter «korrespondanse-tråden» i `_losen-queue/KOORDINERING.md`, og kalles det her. Kø-tråden er en annen tråd.

**Slik leser du dette.** Vil du bare ta stilling, les utdraget `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/G1-KORT.md`. Det har «Kort sagt», de fem valgene og lista over det du selv må gjøre, og ingenting annet. Her i den fulle spesifikasjonen står det samme i «Kort sagt» under, i §6 og i §3b. §1 er formålene. §3 er det du kommer til å se. §0 og §2 er grunnlaget og grensene. §4 og de første radene i §5 er lagt inn av verktøyet. Alle stier er skrevet fra HAVEN-mappen. Fagord er forklart i ordlista under.

**Kort sagt.**

- Det Vegar og Victoria har i dag, er den gamle kanalen. Der ser tjeneren meldingene i klartekst, og vedlegg finnes ikke.
- Dette finnes for den nye, krypterte korrespondansen: cellen som lagrer meldingene (i CellProtocol, i revisjonen staging kjører), en klient for den parten som blir invitert (på `main` i HavenAgentD), og vedlegg (skrevet og testet lokalt, ikke gjennomgått, ikke på `main`).
- Dette mangler:
  1. **To agenter kan ikke skrive til hverandre i én celle slik koden står.** Koden regner med at den ene parten eier cellen. Eieren er mottaker av alt, har ingen vei til klienten utenom testene, og kan ikke sende vedlegg. Se A7–A10 i §0.
  2. Staging kan ikke huse de nye cellene, og kan ikke melde noen inn i dem.
  3. Broen meldingene skal gå over, er merget i CellProtocol, men ikke utgitt, og ruta mangler i CellScaffold.
  4. Ingen pakke med den nye klienten er bygget.
- Punkt 1 betyr at «tjenerdelen» er mer enn å sette cellen på staging. Reglene for hvem som er med i en celle, må gjøres ferdige først. Det er valg 1 i §6, og det avgjør hvor du godkjenner og hvor lang tid dette tar.
- Første pakke har ikke dette, slik forslaget står: varsel ved ny post, som du har bedt om to ganger (S2 i §6); vedlegg som referanse eller hent ved behov, bare som kopi (S1 i §6); og delegering (valg 3). Si fra hvis noe av det må inn.
- Tid: leddene korrespondanse-tråden har, er fem til ni uker når de tas etter hverandre, og tre til fem hvis Codex tar en del samtidig. Bro-leddene har jeg ikke tall for. Ingen dato er lovet (§3b).
- Dokumentet sier hva som skal være sant når Vegar og Victoria bruker det, og hva som teller som bevis for det. Det er ikke en plan. Planen kommer etter at du har godkjent formålene (G1) og bildene (G1-GUI).

Figuren `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/figur/leddene-v2.svg` viser leddene, hvor hvert av dem står i dag, og hvor ordet ditt trengs.

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

**Hva A7–A10 betyr samlet.** Slik koden står, er en relasjon som virker, én eier og én invitert. Den inviterte siden har klienten og kan sende tekst og vedlegg. Eiersiden har ingen vei til klienten utenom testene, og kan ikke sende vedlegg. To inviterte i samme celle går ikke: klienten til den ene godtar ikke den andre som medlem. Eier tjeneren cellen, er tjeneren mottaker. Ingen av måtene gir det du har bedt om: at agenten din og Vegars agent skriver til hverandre, begge veier, med vedlegg, uten at tjeneren kan lese. Planen fra 09.09 pekte på den ene halvdelen (`CellProtocolDocuments/Deliverables/Correspondence_Uten_Agent_I_Runtime_Plan_2026-09-09.md`, §3.3: lagringsmyndighet må skilles fra hvem som er mottaker). Den sier ikke at klienten bare virker for den inviterte, eller at et vedlegg binder avsenderen til en avtale.

## 1. Formålstre

Nye noder heter `purpose://candidate.kryptert-korrespondanse-med-vedlegg-ut.<navn>`. I tabellen står bare `<navn>`. Foreldrene er hentet fra `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json`. Formålene gir ingen rettigheter.

```text
R  Vegar og Victoria korresponderer med Kjetil, kryptert og med vedlegg
├── A  Kryptert fra avsender til mottaker, og driften er blind
│   ├── A1  To parter skriver til hverandre i én celle, hver med klienten fra pakken
│   ├── A2  Staging huser én celle per relasjon, og cellen tar bare imot konvolutter
│   ├── A3  Tjeneren er ikke mottaker og kan ikke koble identitet til person
│   ├── A4  Innmelding gir en smal avtale, ikke en bred
│   ├── A5  Meldingene går over den autentiserte broen, og ingen annen vei
│   └── A6  Utløp fjerner hele meldingen, også når ingen leser
├── B  Vedlegg i samme pakke
│   ├── B1  Vedleggskoden er gjennomgått og ligger på main
│   ├── B2  Staging bærer vedleggene og rydder etter seg
│   └── B3  Installerpakken og budsjettet kommer fram og kan brukes
├── C  Én pakke og få håndgrep
│   ├── C1  Mottakeren installerer én pakke og gjør ett håndgrep til
│   ├── C2  Kjetil godkjenner én forespørsel per person, og ser at den er fra rett person
│   ├── C3  Tilgangen varer til en sluttdato, og fornyes uten drift
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
| A1 | `to-parter-i-en-celle` | To parter skriver til hverandre i én relasjonscelle, hver med klienten fra pakken | A | Prøveparet, mot samme celle på staging og med binæren fra pakken: hver side leser, sender, kvitterer, sender et vedlegg og henter et vedlegg. Alle ti handlingene lykkes. Medlemslista har nøyaktig de to. | T-A1 | Korrespondanse-tråden skriver; Astra gjennomgår; Codex eller du merger | candidate |
| A2 | `staging-huser-konvolutter` | Staging huser én relasjonscelle per godkjent relasjon, og cellen tar bare imot konvolutter | A | En melding sendt med klienten ligger lagret som konvolutt. Bytene staging har lagret for cellen, inneholder verken innholdet eller emnet, heller ikke i en annen koding. Klartekst sendt rett til cellen blir avvist. | T-A2 | Korrespondanse-tråden | candidate |
| A3 | `tjeneren-er-ikke-mottaker` | Tjeneren er ikke mottaker, har ingen nøkkel som åpner en konvolutt, og kan ikke koble en identitet til en person ut fra det den lagrer | A | Medlemslista i hver celle er de to partenes korrespondanseidentiteter og ingen andre, og hver lagret konvolutt er kryptert til nøyaktig de to. Det staging lagrer for korrespondansen (cellene, forespørslene om tilgang og invitasjonene), har verken visningsnavn, profilnavn, maskinnavn eller entitetsreferanse. Hvordan dette oppnås, følger av valg 1 i §6. | T-A3 | Korrespondanse-tråden | candidate |
| A4 | `smal-avtale-ved-innmelding` | En godkjent identitet får cellens adresse, medlemmenes offentlige nøkler og en signert avtale med nøyaktig de handlingene den skal ha | A | Avtalen har de fire handlingene (innboks, les, send, kvitter) og de ti vedleggshandlingene, og ikke flere. Et forsøk på å invitere andre med den blir avvist. En avtale med bare de fire gir ingen vedleggstilgang. | T-A4 | Korrespondanse-tråden | candidate |
| A5 | `over-autentisert-bro` | Meldingene går over den autentiserte broen, og ingen annen vei | A | To prøveidentiteter sender hver sin melding mot staging over broen. En forbindelse uten håndtrykk når ikke cellen. En identitet med håndtrykk, men uten avtale, blir avvist av cellen. Klientbinæren inneholder ikke adressen til den gamle ruta. | T-A5 | Codex leverer ruta (HD-0166). Klientens håndtrykk: se §2 nr. 3. Korrespondanse-tråden prøver | candidate |
| A6 | `utloep-fjerner-alt` | Når en melding utløper, forsvinner hele konvolutten, også ytterdelen, uten at noen må lese innboksen først | A | Senest én time etter utløp finnes meldingen ikke i det staging har lagret, selv om ingen har kalt cellen i mellomtiden. | T-A6 | Korrespondanse-tråden | candidate |
| B | `vedlegg-i-samme-pakke` | Mottakeren får materialet arbeidet trenger, i samme pakke som den krypterte korrespondansen | R; `purpose://digital-work.coordinate` | F1–F7 i vedleggs-PDD-en, prøvd ute. | B1–B3 | — | candidate |
| B1 | `vedlegg-paa-main` | Vedleggskoden er gjennomgått av Astra og ligger på `main` i CellProtocol og HavenAgentD | B | En ren klone fra GitHub til en tom mappe bygger og består testene i begge repoene. Rapporten fra gjennomgangen ligger ved, og hvert funn er rettet eller skriftlig godtatt av deg. | T-B1 | Korrespondanse-tråden; Astra; Codex eller du merger | candidate |
| B2 | `staging-baerer-vedlegg` | Staging lagrer avsenders krypterte vedlegg i en undercelle avsenderen eier, og rydder ved utløp og tilbakekall | B | Den faktiske installerpakken og en fil på 200 MB går hver vei med lik sjekksum hos mottakeren. Etter utløp og etter tilbakekall kan fila ikke hentes, og bytene er borte fra disken. Er det mindre ledig plass enn terskelen (§6, standardvalg), blir et nytt vedlegg avvist før en eneste filbyte er sendt. | T-B2 | Korrespondanse-tråden | candidate |
| B3 | `installerpakke-og-budsjett` | Installerpakken når Vegar og Victoria, og budsjettet når den du velger, som vedlegg | B | F2 og F3 i vedleggs-PDD-en: to av to får brukt pakken, og budsjettmottakeren åpner riktig versjon. | T-B3 | Vegar, Victoria og Kjetil | candidate |
| C | `en-pakke-faa-haandgrep` | Ingen gjør driftsarbeid for å korrespondere | R | C1–C5. | C1–C5 | — | candidate |
| C1 | `mottaker-en-pakke-ett-haandgrep` | Mottakeren installerer én signert pakke og gjør ett håndgrep til | C | På en Mac uten HAVEN: dobbeltklikk på pakken, og så ett håndgrep (åpne lenken eller gi den til agenten sin; bildet du godkjenner, avgjør hvilket). Med valg 2a kommer én ting til: sende deg en kode på seks sifre. Ingen kommando skrives, ingen fil lagres eller redigeres for hånd, ingen advarsel fra macOS. Bestått er tre håndgrep eller færre, telt på et skjermopptak: installere pakken (macOS' egne dialoger teller som ett), gjøre oppsettet, og med valg 2a sende koden. Det virker oppå en eldre installasjon, og på Intel hvis en mottaker har det. | T-C1 | Codex bygger pakken; korrespondanse-tråden bygger oppsettet og prøver | candidate |
| C2 | `en-godkjenning-per-person` | Kjetil godkjenner én forespørsel per person, og ser at den er fra rett person | C; `purpose://gui.quality.functional-accessible` | Ett kort per person som ber om tilgang. Kortet viser det valg 2 bestemmer, og ingen navn hentet fra tjeneren. Ett trykk godkjenner. Avslag virker. En forespørsel laget med en annen nøkkel enn mottakerens, viser en annen kode enn den mottakeren ser. Bildet er godkjent av deg før noe bygges (G1-GUI). Hvor kortet ligger, følger av valg 1: på adminsiden (1a) eller i et vindu på Macen din (1b). Med 1c finnes ikke kortet; da sier du ja til agenten. | T-C2 | Korrespondanse-tråden | candidate |
| C3 | `tilgang-uten-driftsrunder` | Tilgangen varer til en sluttdato du setter, og fornyes uten drift | C | Avtalen gjelder til sluttdatoen du satte da du godkjente, høyst ett år. Når den går ut, sier klienten det i klare ord. Du fornyer med samme håndgrep som første gang, og klienten henter den nye avtalen selv. Ingen miljøfil, ingen omstart av staging og ingen root er i bruk ved fornyelsen. Ny nøkkel eller flere rettigheter krever en ny forespørsel. Om det å invitere en ny person også skal gå uten drift i første pakke, er valg 5. | T-C3 | Korrespondanse-tråden | candidate |
| C4 | `kjetils-mac-samme-pakke` | Kjetils egen Mac bruker samme pakke og samme vei som mottakerne | C | For den nye korrespondansen er programfila agentene dine starter, pakkens (stien i oppsettet og sjekksummen stemmer med pakkens liste). En melding sendt med ferdighetene dine går fram med den nye klienten. Ferdighetene dine er oppdatert for den nye klienten, som velger relasjon på en annen måte enn den gamle. Den gamle klienten står ved siden av og virker til begge mottakerne er over (D1). | T-C4 | Korrespondanse-tråden; du installerer pakken | candidate |
| C5 | `overgangen-fullfoert` | Begge mottakerne er over, og de gamle tilgangene deres er trukket | C | T-R er grønn for både Vegar og Victoria. Etter ditt ord er de to gamle tilgangene trukket, og et sendeforsøk til dem i den gamle kanalen blir avvist. De gamle meldingene ligger urørt til de utløper. | T-C5 | Korrespondanse-tråden; ditt ord | candidate |
| D | `det-som-virker-staar` | Det som virker i dag, står, og det som aldri skal skje, skjer ikke | R; `purpose://self-determination.data.verifiability` | D1–D4. | D1–D4 | — | candidate |
| D1 | `gammel-kanal-staar` | Skal ikke: den gamle kanalen brytes før begge mottakerne er over | D | Før og etter hver utsetting til staging sender prøveparet en melding hver vei i den gamle kanalen og leser den. | T-D1 | Korrespondanse-tråden | candidate |
| D2 | `ingen-klartekst` | Skal ikke: gamle meldinger flyttes inn i de nye cellene, eller den nye klienten faller tilbake til klartekst | D | De nye cellene er tomme før første nye melding. Når broen er sperret, feiler klienten med en klar melding og sender ingenting. | T-D2 | Korrespondanse-tråden | candidate |
| D3 | `ingen-agent-uten-ja` | Skal ikke: en agent sender i Kjetils navn, eller slipper inn noen, uten hans ja | D | I prøven finnes ingen sending fra din identitet som du ikke har sagt ja til. Avtalen agentens klient holder, gir bare handlingene i A4, og et forsøk på å godkjenne en forespørsel med agentens korrespondanseidentitet blir avvist. Hva som ellers hindrer en agent i å slippe inn noen, følger av valg 1: med 1a regelen din og innloggingen på adminsiden, ikke en lås; med 1b en lås (Touch ID); med 1c ingenting, for da holder agenten nøkkelen. | T-D3 | Korrespondanse-tråden | candidate |
| D4 | `ingen-verdi-i-logg` | Skal ikke: nøkler, engangskoder eller meldingstekst havner i logger, utskrifter eller bevis | D | Søk i alle bevisfiler og logger fra prøven etter prøvenøkler, prøvekoder og prøvetekst gir null treff, og det samme søket finner en merkelapp som er lagt inn med vilje. | T-D4 | Korrespondanse-tråden | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål har en test i §5.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en menneskeklient i Binding (W5 i planen fra 09.09). Den første pakken er agentens klient, som i dag.
- Ikke jobbadministrasjon uten agent (W1 og W2 i samme plan).
- Ikke skillet mellom agenter og identiteter (W0 og porten G0 i samme plan). I den første pakken bruker agentene dine korrespondansenøkkelen din, som i dag, og Vegars og Victorias agenter bruker deres. Vernet mot at en agent sender i ditt navn, er ditt ja og den stående regelen, ikke en lås. Det er valg 3 i §6.
- Ikke delegering (Book 33 §4.3 og §10 punkt 5). Også valg 3.
- Ikke produksjon. Prøven går mot staging, som den gamle piloten.
- Ikke celler som deltakerne huser selv (Book 33 §7.2). Derfor går vedlegg som kopi i første pakke (A18 i §0).
- Ikke gruppekorrespondanse, og ikke skjuling av når og hvor mye som sendes. Pakketeksten sier det.
- Ikke vern mot en drift som med vilje bytter nøkler under innmeldingen eller kjører endret kode. Book 33 lover at driften ikke kan lese eller koble ut fra det verten lagrer; det er det som prøves her.
- Ikke varsel ved ny post. Se standardvalgene i §6.
- Ikke Losens egen entitet (Book 33 §4A). Ingen nøkkel lages for Losen.
- Ikke flytting av gamle meldinger. De blir i den gamle kanalen til de utløper.
- Ikke en ny utgave av vedleggsformålene. F1–F7 og svarene dine står i vedleggs-PDD-en og gjelder som de er.

Kapabiliteter og avhengigheter oppgaven bygger på:

| Nr. | Kapabilitet | Kilde | Avgrensning | Må virke før test? | Eier |
|---|---|---|---|---|---|
| 1 | Utgivelse av CellProtocol med broen (#53) | CellProtocol `origin/main` `1ec56d5`; `_losen-queue/KOORDINERING.md` | Ingen utgivelse. N32 og N36–N39 må være rettet, eller skriftlig godtatt av deg, først. | Ja | Codex (bro-tråden); ditt ord |
| 2 | Autentisert bro-rute i CellScaffold (`/bridgehead/<publisher>/<broId>`, også for delt forbindelse), og en bro-del i `/health/ready` | HD-0166; `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/PLAN.md`, AP5 og AP6 | Ikke påbegynt. Uten den når ingen klient cellene. N35 gjelder den delte forbindelsen klienten bruker. | Ja, før A5 og alt som bygger på A5 | Codex (bro-tråden) |
| 3 | Korrespondanseklienten gjør håndtrykket | Samme plan, AP7; `CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/STATUS.md` («HavenAgentD må komponere porten») | Tittelen på #53 sier at AP7 er med; hva det dekker for korrespondanseklienten, har jeg ikke lest. Klienten på `main` i HavenAgentD er ikke endret siden før #53. I bro-planen ligger AP7 hos Codex. De samme filene endres av nr. 4 og 5, så jeg foreslår at korrespondanse-tråden tar klientdelen. Det avtales med bro-tråden i `_losen-queue/KOORDINERING.md`. | Ja, før A5 | Foreslått: korrespondanse-tråden. I dag: Codex (AP7) |
| 4 | Relasjonsmodellen gjort ferdig i CellProtocol og klienten | A7–A10 i §0; valg 1 i §6 | Mangler. Planen (G2) starter med en liten prøve som viser den valgte måten med to prøveidentiteter, før noe annet bygges på den. | Ja, før A1–A4 | Korrespondanse-tråden skriver; Astra gjennomgår; Codex eller du merger |
| 5 | Vedleggsgrenen oppå ny `main`, tilpasset punkt 4, gjennomgått | A6 og A10 i §0 | Lokal gren. HavenAgentD får ikke pinne en CellProtocol-revisjon som ikke ligger på CellProtocols `main` (se valg 4). | Ja, før B | Korrespondanse-tråden; Astra |
| 6 | HavenAgentD `main` grønn | A16 i §0 | Rød i dag. PR #28 først, så PR #30 og vedleggene. | Ja, før pakken bygges | Codex (#28); korrespondanse-tråden (#30 og vedlegg) |
| 7 | Signering og notarisering av hele pakken | `HavenAgentD/Packaging/build_pkg.sh` og `HavenAgentD/Packaging/notarize_pkg.sh`; HD-0107 | HD-0107 er åpen (pakken mangler ressurser og riktige sjekksummer). Det lille pilotskriptet signerer ikke, og brukes ikke. | Ja, før C1 | Codex; nøklene ligger på Macen din |
| 8 | Utsetting til staging | `haven-deploy` på verten | Tjenerdelen må ut i en utgivelse av CellScaffold, helst den samme som bro-ruta. | Ja | Codex eller du utfører, på ditt ord; kø-tråden sier når |
| 9 | Sikkerhetskopi av korrespondansetilstanden før tjenerendringen | `HavenAgentD/Docs/CorrespondenceS6ChangeSetAndRollback.md`, «Preconditions» | Ikke tatt. De gamle meldingene skal ikke flyttes, bare kunne gjenopprettes. | Ja, før første utsetting | Den som setter ut |
| 10 | Godkjenningsflaten på adminsiden | A17 i §0 | Finnes for den gamle kanalen. To adminceller var røde på staging 06.10 (HD-0143); om `/admin/funding` er rammet, er ikke målt. Kortet er GUI, og krever bilde før det bygges. | Ja, før C2 | Kortet: korrespondanse-tråden. HD-0143: konferanse-Codex |
| 11 | Innlogging på staging som admin | `_losen-queue/KOORDINERING.md` | Bare du kan logge inn. | Ja, for C2 og for godkjenningene | Kjetil |
| 12 | Plass til vedlegg på staging | Ikke målt | Hvor mye ledig plass datadisken har, og om vedleggene kommer med i sikkerhetskopien, måles i planen. | Ja, før B2 | Korrespondanse-tråden måler |
| 13 | Prøveparets tilgang i den gamle kanalen | `HAVEN-Deploy/_handoff/HD-0006/` | Går ut 08.10 kl. 13:03Z. Fornyes i prøven som pågår (HD-0006). Uten den kan T-D1 ikke kjøres. | Ja, for D1 | Korrespondanse-tråden; ditt ord om root |
| 14 | Mottakernes maskiner | A15 i §0 | Ukjent. | Avgjør om Intel må prøves | Du spør dem |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.

| Nr. | Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|---|
| 1 | Kortet for en relasjon, i fire tilstander: venter, godkjent, avslått, feil | bilde | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/images/kort-relasjon-<tilstand>-v1.png` | Lages når valg 1 og 2 er besvart, før G2. Du godkjenner bildet (G1-GUI). | nei |
| 2 | Det mottakeren ser under oppsettet: før, underveis, ferdig, feil | bilde | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/images/mottaker-oppsett-<tilstand>-v1.png` | Lages før G2. Du godkjenner bildet (G1-GUI). | nei |
| 3 | Pakketeksten: meldingen du videresender, og veiledningen i pakken. Den sier hva tjeneren kan se (at en celle finnes, når og hvor mye som sendes, og at en melding er kvittert), hva den ikke kan se, og at hvem som står bak en agent, ikke kan etterprøves kryptografisk ennå | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/TIL-VEGAR.md` og `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/TIL-VICTORIA.md` (lenkene selv ligger privat) | Book 33 §4.2 og §5.3. Du godkjenner teksten. | nei |
| 4 | Forslag til endringer i Book 33: vedlegg er ikke lenger et ikke-mål, avtalen har fjorten handlinger, ytterdelen av konvolutten har ett felt til (S10), og det som følger av valg 1 | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/BOOK-33-ENDRINGSFORSLAG.md` | Boka endres ikke uten ditt ord. | nei |
| 5 | Rapporten fra Astras gjennomgang av relasjonsmodellen og vedleggene, med ett utfall per funn | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/evidence/ASTRA-GJENNOMGANG.md` | T-A1, T-B1 | nei |
| 6 | Utskrift fra staging av en relasjonscelle etter en prøvemelding: ingen klartekst, ingen navn, to medlemmer | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/evidence/celle-utskrift-staging.txt` | T-A2, T-A3 | nei |
| 7 | Prøveparet: melding og vedlegg begge veier mot staging, med binæren fra pakken | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#proevepar` | T-A1, T-A5, T-B2 | nei |
| 8 | Pakken: én fil, signert og notarisert | fil | `HAVEN-Deploy/_handoff/VEGAR/` (navnet settes i planen), med utskriften fra Gatekeeper-kontrollen ved siden av | T-C1 | nei |
| 9 | Skjermopptak av oppsettet på en Mac uten HAVEN, med håndgrepene telt | fil | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/evidence/oppsett-ren-mac.mov` | T-C1 | nei |
| 10 | En tilgang som går ut, og som fornyes uten drift | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#fornyelse` | T-C3 | nei |
| 11 | Macen din på den nye klienten | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#kjetils-mac` | T-C4 | nei |
| 12 | Vegars og Victorias egne ord om at melding, installerpakke og budsjett kom fram og kunne brukes | deres svar | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/ACCEPT.md#mottakerne` | T-R, T-B3 | nei |
| 13 | Den gamle kanalen før og etter hver utsetting, og de gamle tilgangene trukket til slutt | testutdata | `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#gammel-kanal` og `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/TESTRESULT.md#overgang` | T-D1, T-C5 | nei |

## 3b. Hvem gjør hva, hva du må gjøre, og hvor lang tid det tar

Tallene er arbeidsdager for leddet, ikke kalenderdager, og de er anslag. «Runder» er gjennomganger der Astra finner noe som må rettes: én til to dager per runde. Broen trengte åtte runder. Jeg vet ikke hvor mange det blir her.

| Ledd | Hvem | Anslag | Venter på |
|---|---|---|---|
| 1. Broen: funnene N32 og N36–N39, og utgivelse av CellProtocol | Codex (bro-tråden) | Bro-tråden må si det. Jeg har ikke grunnlag for et tall. | At funnene rettes, eller at du godtar dem skriftlig |
| 2. Bro-ruta i CellScaffold (HD-0166) | Codex (bro-tråden) | Samme. | Ledd 1 |
| 3. En liten prøve av den valgte relasjonsmodellen, lokalt, før noe annet bygges | Korrespondanse-tråden | 1–2 | G1 og valg 1 |
| 4. Relasjonsmodellen i CellProtocol og klienten | Korrespondanse-tråden; Astra | 5–8, pluss runder | Ledd 3, G2 |
| 5. Vedlegg: oppå ny `main`, tilpasset ledd 4, gjennomgang, PR | Korrespondanse-tråden; Astra | 3–5, pluss runder | Ledd 4; valg 4 |
| 6. Klienten gjør håndtrykket på broen | Foreslått: korrespondanse-tråden (§2 nr. 3). I bro-planen: Codex | 2–4, pluss runder. Usikkert: tittelen på #53 sier at AP7 er med, og jeg har ikke lest hva det dekker. | Avtale med bro-tråden |
| 7. Tjenerdelen: huse cellene, innmelding, kortet, rydding ved utløp, lager for vedlegg | Korrespondanse-tråden | 8–12, pluss runder. Planen fra 09.09 sier 8–12 for å huse cellene alene (W4). | G1, bildene, G2, og ledd 3 og 4. Kan skrives mot et lokalt bygg av ledd 4, men kan ikke settes ut før CellProtocol er gitt ut (ledd 11) |
| 8. Fornyelse uten drift (C3). Med valg 5b også invitasjon fra adminsiden | Korrespondanse-tråden | 2–3. Med 5b: 6–9 til (W3 i planen fra 09.09). | Valg 5 |
| 9. Oppsett fra lenke hos mottakeren, og registrering av klienten hos agenten | Korrespondanse-tråden | 3–5 | Bildene |
| 10. Pakken: PR #28, HD-0107, bygg, signering, notarisering, prøve på en ren Mac | Codex; korrespondanse-tråden prøver | 2–4 | Utgivelse av CellProtocol; ledd 4–6 og 9 |
| 11. Utgivelser: CellProtocol én gang, CellScaffold til staging én gang | Codex eller du, på ditt ord | 1 per utgivelse | Leddene over |
| 12. Prøvepar mot staging | Korrespondanse-tråden | 1–2 | Pakke og utsetting |
| 13. Macen din over på den nye klienten | Korrespondanse-tråden; du installerer | 1–2 | Grønt prøvepar |
| 14. Vegar og Victoria | Dem og deg | Deres tid | Ledd 13 |

**Samlet.** Leddene korrespondanse-tråden har (3–9, 12 og 13), er 26–43 arbeidsdager når de tas etter hverandre. Det er fem til ni uker, før runder. Tar Codex ledd 4–6 mens korrespondanse-tråden tar ledd 7–9, går to løp samtidig, og tre til fem uker er mulig. Jeg lover ingen dato. Bro-leddene (1 og 2) har jeg ikke tall for.

**Følge for den gamle kanalen.** Når fornyelsen som pågår, er gjennomført, har Vegar og Victoria tilgang der til 05.11. Etter anslaget over er det nye neppe ute før den datoen. Da må den gamle kanalen fornyes én gang til i november, med skriptet som blir ferdig nå.

**Det du selv må gjøre, i rekkefølge:**

Haster, fordi Vegars tilgang i den gamle kanalen går ut 08.10:
1. Svare ja eller nei på spørsmålet jeg stilte 06.10 kl. 12:01Z: kan jeg bruke root på staging-verten til å bytte den ene linja med invitasjoner i `/etc/haven/staging-correspondence-invites.env`? Uten det kan fornyelsen ikke kjøres av meg. Etter byttet: godkjenne to kort for prøveparet, videresende én melding til Vegar og én til Victoria, og godkjenne kortene deres.

Nå, for det nye:
2. Svare på de fem valgene i §6, lese S1 og S2 samme sted, og si om G1 er godkjent.
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
| T-A1 | `to-parter-i-en-celle` | Prøveparet mot samme celle på staging, med binæren fra pakken (sjekksum føres): hver side leser, sender, kvitterer, sender et vedlegg og henter et vedlegg. Ti handlinger, ti utfall. Medlemslista leses: nøyaktig to. Før dette, i planens første steg: samme ti handlinger lokalt mot en celle i en testprosess. | TESTRESULT.md#proevepar | venter |
| T-A2 | `staging-huser-konvolutter` | Send en prøvemelding der emne og innhold har hver sin tilfeldige merkelapp. Les bytene staging har lagret for cellen, og søk etter merkelappene som de står, og i base64, base64url, heksadesimalt og UTF-16. Null treff. Kontroll på at søket virker: mottakeren åpner samme melding og finner begge merkelappene. Send klartekst rett til cellen: skal avvises. | TESTRESULT.md#celle, evidence/celle-utskrift-staging.txt | venter |
| T-A3 | `tjeneren-er-ikke-mottaker` | Les medlemslista: de to prøveidentitetenes numre og ingen andre; eierens nummer står der ikke (valg 1a og 1b). Les mottakerlista i hodet på den lagrede konvolutten: nøyaktig de samme to. Søk i det staging har lagret for korrespondansen (cellene, forespørslene, invitasjonene) etter prøveidentitetenes visningsnavn, profilnavn og maskinnavn, i de samme kodingene som i T-A2. Null treff. Kontroll: de samme ordene finnes i klientens egen profilfil. | TESTRESULT.md#blind | venter |
| T-A4 | `smal-avtale-ved-innmelding` | Over broen, med prøveidentitetene: les avtalen klienten fikk, og tell handlingene (fjorten). Kall `audience.inviteIdentities` med den: skal gi `grantNotHeld`. Kall en vedleggshandling med en avtale som bare har de fire: skal avvises. | TESTRESULT.md#avtale | venter |
| T-A5 | `over-autentisert-bro` | To prøveidentiteter mot staging over broen, én melding hver vei. En forbindelse uten håndtrykk: skal stenges før cellen. En identitet med håndtrykk, uten avtale: `grantNotHeld`. `strings` på klientbinæren i pakken gir null treff på `assistant-correspondence/v1`; kontroll: samme søk gir treff i den gamle binæren fra pakken 08.09. | TESTRESULT.md#bro | venter (avhenger av HD-0166) |
| T-A6 | `utloep-fjerner-alt` | En prøvemelding med ti minutters levetid. Ingen kaller cellen etterpå. Før utløp finnes meldingsnummeret i det staging har lagret (kontroll). Sytti minutter etter utløp finnes det ikke, verken i ytterdel eller innerdel. | TESTRESULT.md#utloep | venter |
| T-B1 | `vedlegg-paa-main` | Ren klone fra GitHub til en tom mappe; bygg og test begge repoene. Rapporten fra Astras gjennomgang ligger ved, med ett utfall per funn: rettet, eller skriftlig godtatt av Kjetil. | TESTRESULT.md#vedlegg-main, evidence/ASTRA-GJENNOMGANG.md | venter |
| T-B2 | `staging-baerer-vedlegg` | Den faktiske installerpakken og en fil på 200 MB, hver vei mot staging; sjekksum hos mottakeren, og minnetopp hos klient og tjener føres. Hent etter utløp og etter tilbakekall: skal avvises, og mappen på disken listes før og etter. Omstart av staging midt i en opplasting: klar feil, og en ny sending lykkes. Med mindre ledig plass enn terskelen (prøvd ved å sette terskelen over det som er ledig): avvist, og null filbyte sendt. | TESTRESULT.md#vedlegg-staging | venter |
| T-B3 | `installerpakke-og-budsjett` | T2 og T3 i vedleggs-PDD-en, med pakken og budsjettfila Kjetil navngir. | ACCEPT.md#mottakerne | venter |
| T-C1 | `mottaker-en-pakke-ett-haandgrep` | En ren bruker på en Mac uten HAVEN: installer, gjør oppsettet, med skjermopptak. Tell håndgrepene: høyst tre (pakken, oppsettet, koden). Gjenta oppå 0.3.2. `spctl --assess --type install` på pakken skal si «accepted», `codesign --verify --deep --strict` på det installerte skal gå gjennom, og `lipo -archs` skal vise begge arkitekturer. Intel prøves bare hvis en mottaker har det, og da på en Intel-Mac; ellers sier pakketeksten at Intel ikke er prøvd. | TESTRESULT.md#pakke, evidence/oppsett-ren-mac.mov | venter |
| T-C2 | `en-godkjenning-per-person` | Du godkjenner prøveparet på flaten valg 1 gir (adminsiden med 1a, vinduet på Macen med 1b). Det godkjente bildet står ved siden av et skjermbilde av den ferdige flaten, i samme størrelse. Avslag prøves. Én forespørsel lages med en annen nøkkel enn den prøvemottakeren viser: koden på kortet skal da ikke stemme med den prøvemottakeren ser. Kortet leses for navn: ingen hentet fra tjeneren. | ACCEPT.md#kort | venter |
| T-C3 | `tilgang-uten-driftsrunder` | En prøveidentitet får en avtale på femten minutter. Etter utløp: klienten sier i klare ord at tilgangen er utløpt, og hva som må gjøres. Du fornyer med ett trykk. Klienten henter den nye avtalen og virker igjen, uten ny installasjon. Journalen på verten viser ingen `haven-deploy` fra start til slutt. Bytt nøkkel på prøveidentiteten: det kreves en ny forespørsel. | TESTRESULT.md#fornyelse | venter |
| T-C4 | `kjetils-mac-samme-pakke` | Les oppsettet agentene dine bruker for den nye korrespondansen: hvilken programfil starter de? Sjekksummen av den fila er lik den i pakkens liste over sjekksummer (`release-manifest.json`, som bygget legger ved siden av pakken). En melding sendt med ferdighetene dine kommer fram hos prøvemottakeren. Oppsettet for den gamle kanalen leses også: det peker fortsatt på den gamle klienten, og T-D1 er grønn etterpå. | TESTRESULT.md#kjetils-mac | venter |
| T-C5 | `overgangen-fullfoert` | T-R er grønn for begge. Etter ditt ord: de to gamle tilgangene står som trukket på adminsiden, og et sendeforsøk til hver av dem fra prøveparet i den gamle kanalen blir avvist. Antall gamle meldinger er det samme før og etter. | TESTRESULT.md#overgang | venter |
| T-D1 | `gammel-kanal-staar` | Før og etter hver utsetting til staging: prøveparet sender én melding hver vei i den gamle kanalen og leser den. Fire utfall per utsetting. | TESTRESULT.md#gammel-kanal | venter (krever at prøveparets tilgang er fornyet, HD-0006) |
| T-D2 | `ingen-klartekst` | Tell meldinger i de nye cellene før første nye melding: null. Sperr broen i en prøve og send: klienten skal feile med en klar melding, og den lokale loggen over utgående kall viser ingen sending. Statisk kontroll som i T-A5: binæren har ikke adressen til den gamle ruta. | TESTRESULT.md#ingen-klartekst | venter |
| T-D3 | `ingen-agent-uten-ja` | Les verktøylista og avtalen agentens klient holder. List sendingene fra din identitet i prøven, og hold dem mot det du har sagt ja til. Prøv å godkjenne en prøveforespørsel med agentens korrespondanseidentitet: skal avvises. Med 1b: prøv å godkjenne uten Touch ID: skal avvises. Med 1a prøves ikke veien gjennom nettleseren din: en agent som styrer nettleseren mens du er innlogget, kan trykke, og vernet der er regelen din. Det føres som det er, ikke som bestått. | ACCEPT.md#agent | venter |
| T-D4 | `ingen-verdi-i-logg` | Legg en merkelapp i én bevisfil med vilje, og søk i alle bevisfiler og logger fra prøven etter prøvenøkler, prøvekoder, prøvetekst og merkelappen. Bare merkelappen skal gi treff. | TESTRESULT.md#ingen-verdier | venter |

Radene som begynner med `test.`, er lagt inn av verktøyet. Radene som begynner med `T-`, hører til bladformålene i §1. `TESTRESULT.md`, `ACCEPT.md`, `evidence/` og `images/` ligger i oppgavemappen, `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Hver `T-`-test er skrevet slik at den blir rød hvis målet ikke er nådd. Der et søk skal gi null treff, står det også hva som viser at søket kan finne noe.

## 6. Åpne spørsmål til Kjetil

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

### Standardvalg

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

### Det jeg ikke vet

- Om N35 er lukket i #53, og hvor mye som gjenstår på bro-leddene.
- Hva #53 gir en klient å bygge på for håndtrykket; tittelen sier at AP7 er med, og jeg har ikke lest det.
- Hvordan en invitert identitet skal bevise nøkkelen sin i innmeldingen når den er koblet til over broen (valg 1).
- Om `/admin/funding` er rammet av feilen i adminflatene (HD-0143).
- Hvilke Macer Vegar og Victoria har, og hva Victoria har installert.
- Hvor mye ledig plass datadisken på staging har.
- Hva godkjenningsflaten for den gamle kanalen inneholder; jeg har sett at fila finnes, ikke lest den.
- Hvor mange runder gjennomgangene tar.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-06 | Opprettet | Losen |
| 1 | 2026-10-06 | Første utkast. Ikke lagt fram for Kjetil. En uavhengig kontroll (Fabel) sa: «Nei, ikke slik den står. Ja etter rettelsene 1–8». Rapporten: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/FABEL-G1-RUNDE-1.md`. | Korrespondanse-tråden |
| 2 | 2026-10-06 | Rettet etter kontrollen, og etter et funn gjort mens rettelsene ble etterprøvd i koden: koden dekker én eier og én invitert, klienten har bare en vei for den inviterte, og eieren kan ikke sende vedlegg (A7–A10). Treet har fått A1 (to parter i én celle) og C5 (overgangen). Varsel er tatt ut av treet og ført som standardvalg. Valgene er nå fem: hvem som slipper inn medlemmer, hvordan en forespørsel knyttes til en person, delegering, vedlegg til `main` før mottakerprøven, og invitasjon uten drift. Pakkevalget er ikke lenger et valg. Tidsanslaget er summen av leddene. Testene har fått kontroller som gjør at de ikke kan bli grønne uten at målet er nådd. Figuren er tegnet på nytt. To uavhengige kontroller (Fabel) leste utgaven før de siste rettelsene. Den ene leste koden bak A7–A10 og valg 1 og sa: «Ja, etter navngitte rettelser». Kjernen holder, men «eiersiden har ingen klient» var for sterkt sagt (vedleggstestene gir eieren en klient), og 1b og 1c var for enkelt beskrevet. Den andre leste hele spesifikasjonen og sa: «Ja etter rettelsene 1–5». Alle de navngitte rettelsene er tatt inn. Rettelsene selv er ikke lest av en kontrollør. Rapportene: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/FABEL-G1-RUNDE-2-MODELL.md` og `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/panel/FABEL-G1-RUNDE-2-SPEC.md`. | Korrespondanse-tråden |
