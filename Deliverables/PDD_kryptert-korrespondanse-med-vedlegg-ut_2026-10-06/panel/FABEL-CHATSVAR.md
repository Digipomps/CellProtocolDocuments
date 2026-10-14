# RAPPORT — kontroll av UTKAST.md mot kildene (06.10.2026)

Forkortelser: AC = arbeidstre/CellScaffold/AssistantCorrespondenceCell.swift · CC = main/CellProtocol/CorrespondenceCell.swift · GC = main/CellProtocol/GeneralCell.swift · ChC = main/CellProtocol/ChatCell.swift · CAT = main/CellProtocol/CorrespondenceAgreementTemplates.swift · CE = main/CellProtocol/CorrespondenceEnvelope.swift · BC = main/CellProtocol/BridgeCommand.swift · CCl = main/HavenAgentD/CorrespondenceClient.swift · CCT = main/HavenAgentD/CorrespondenceCellTransport.swift · Main = main/HavenAgentD/HavenCorrespondenceMCPMain.swift · CIV = main/HavenAgentD/CorrespondenceIdentityVault.swift · VCC = vedleggsgren/CellProtocol/CorrespondenceCell.swift · G1 = pdd/G1-KORT.md · FS = pdd/FORMAALSSPEC.md

## Dom
**Nei, ikke som det står.** Tabellen og de tre hindrene holder i det store (20 av 23 enkeltpåstander stemmer), men tre setninger er for sterke og må endres før sending: linje 18 («ligger rundt cellen og ikke i den» — innslipp, eier-som-mottaker og vedleggsregelen ligger i cellen), linje 28 («valg 1 faller bort: du eier cellene dine» — det er valg 1c, med ulempene fra G1 ubesvart) og linje 24 («de tre variantene av valg 1 fulgte av det» — 1c fulgte ikke av setningen; 1c er det utkastet nå foreslår). I tillegg kan «Utløp: Ikke lest» erstattes med det koden sier, og U1 blander to nøkler.

## MÅ endres i utkastet
1. **Linje 18.** Si: for de fire tekstoperasjonene behandler cellen eier og invitert likt, men innslipp (GC:1358–1403 med `.ownerApprovalRequired` satt av cellen selv, CC:143/195), eier-alltid-mottaker (CC:198–204, 479–483) og vedleggsregelen (VCC:806–811, 872–874) ligger i cellen. Som den står, strider setningen mot A8 og A10 i FS:104/106.
2. **Linje 24.** 1a og 1b følger av premisset «noen andre enn de to må være eier» (G1:27); 1c gjør det ikke (G1:39). Skriv at den tilbakekalte setningen var for sterk for tekst, men står for vedlegg (P2) og for innslipp.
3. **Linje 28, «valg 1 faller bort».** Forslag A *besvarer* valg 1 med 1c (eller 1b), det fjerner det ikke. G1:39 nevner tre ulemper ved 1c som utkastet ikke svarer på: eieren kan ikke sende vedlegg (= P2), eierens nøkkel må signere der cellen kjører (staging) eller gå veien i 1b, og agenten holder nøkkelen som slipper inn folk (D3 uten lås, FS:175; S6-dokumentet). Utkastets eget «det jeg ikke vet» (linje 31) er nettopp valget 1b mot 1c. Si hvilken nøkkel som skal eie cellen.
4. **Linje 28, «varselet … kommer med av seg selv».** For sterkt: klienten bruker bare `get`/`set` (CCT:49, 54), må lære `feed` over broen (ikke prøvd, utkastet sier det selv) og få hendelsen fram til agenten.
5. **Linje 14, «Utløp: Ikke lest».** Koden sier: meldinger utløper (AC:1334–1340, 1361; purge 861, 1434–1443; filtrert 1272/1294/1387) og tilganger utløper på datoen fra invitasjonen (AC:589–592, 682, 949, 1411). Standard og tak står i `AssistantCorrespondenceContracts`, som ikke er i kildene.
6. **Linje 31 (U1).** Skill signeringsnøkkelen (må bevise seg i cellens prosess for innslipp: GC:1350–1403, 2255–2287) fra nøkkelutvekslingsnøkkelen (den som åpner konvolutter: CE:233–244; to roller i CIV:263–267). Staging kan lese bare hvis den *siste* ligger der; innslipp krever den *første*.
7. **Linje 1, «vanlig medlem».** Eieren står i medlemslista (CC:198–204), men autoriseres ved eierbevis, ikke avtale (GC:2066, 2083–2085), og klienten krever en avtale med eieren som mottaker av sin egen avtale (CCl:513–520), som bare testene lager (FS:105). Skriv «medlem».

## Påstandene
| Nr | Dom | Belegg |
|---|---|---|
| T1 | stemmer | én celle, alle mottakere: AC:32, 1270–1273. «Staging» er fra G1:141 og FS:100 (dokument, ikke kode) |
| T2 | stemmer | signert forespørsel verifiseres: AC:825–859 (852–855) |
| T3 | stemmer | `inbox.list`, `message.read`, `message.ack`: AC:863–870, 1265–1303, 1377–1405 |
| T4 | stemmer | lokal celle-eier: AC:375–382; godkjenning krever eierens identitet: AC:468–474, 977–985 |
| T5 | stemmer | klartekst lagret AC:1358, returnert 1301/1715; emne i klartekst også i liste og Flow (1706); Flow fjerner bare `content` (1723–1725) |
| T6 | stemmer | ingen treff på «attachment» i AC |
| T7 | stemmer ikke (utkastet sier «ikke lest») | se MÅ 5: både meldinger og tilganger utløper |
| K1 | stemmer | 730 linjer (wc); relasjonsceller CC:45–47 |
| K2 | stemmer | CC:235–248, 318–347 |
| K3 | stemmer | CC:213, 286–289 (`.outer`); 298–316 |
| K4 | stemmer | CC:281–316; ingen paging; hvert les gir `message.read` (311) |
| K5 | stemmer | CC:198–204; 479–483 |
| K6 | stemmer | CC:323–326, 565 (forbudte felt); 479–483 |
| K7 | stemmer (i kildemappene) | 0 treff «attachment» under main/; vedlegg bare under vedleggsgren/ |
| K8 | stemmer | CC:26–32, 348–354 |
| C1 | stemmer | 4529 linjer (wc); deltakere ChC:533, 1024 |
| C2 | stemmer | ChC:966–970, 2255–2260 |
| C3 | stemmer | `feed` i malen ChC:528; `chat.message` 2748–2757; `flow` GC:1273–1287 |
| C4 | stemmer | ChC:406, 606–615, 1033, 2286–2287 |
| C5 | stemmer | samme sjekk for alle (ChC:608, 968); eier via eierbevis GC:2036–2039 |
| C6 | stemmer | ChC:1248–1252; lager 2285; Flow 2752–2757. At innholdet er med i Flow-objektet, er slutning (`ChatMessage.messageObject` er ikke i kildene; «plaintextOnly» 1615 støtter det) |
| C7 | stemmer | 0 treff «attachment» i ChC |
| C8 | stemmer, med presisering | ingen tidsutløp (treff på «expir» gjelder invitasjoner: 209, 1809, 2473), men bare de 200 siste beholdes (2286–2287) |
| P1 | stemmer | kommandoene Main:25–61; `setup` krever invitasjon CCl:173–256. «Kan sende tekst etter koden» er slutning fra CCl:513–520 + CC:320–347, ikke belagt med test i kildene |
| P2 | stemmer | VCC:806–811 (avsender må holde avtalen), 842–844, 872–874 (mottakernøkler = avtalens medsignatarer minus avsender; tom for eieren) |
| P3 | stemmer | fem hendelser: CC:311, 374, 405, 440, 466; bare ytterdata 374–381; mal uten `feed` CAT:7–12; `flow` krever `feed` r--- GC:1275. «Eieren får abonnere» er slutning (`CellAuthorizationPolicy` er ikke i kildene) og forutsetter eierbevis fra cellens prosess (GC:2255–2287) |
| Q1 | ordrett: ja | G1:10 (og FS:17). Valg 1 = «Hvem slipper inn medlemmer i en relasjonscelle?» (G1:25–41): 1a tjeneren eier, ikke mottaker; 1b egen eiernøkkel på Macen bak Touch ID; 1c eieren eier med agentens nøkkel. Bare 1a og 1b følger av setningen. De fire andre: 2 hvordan se at forespørselen er fra rett person (2a–c); 3 delegering nå/senere; 4 vedlegg til `main` før prøvd; 5 invitere uten drift |
| A1 | stemmer | `feed`/`stopFeed` BC:13–14 (stream-felt 83–85); klienten bare `get`/`set` CCT:49, 54 |
| A2 | for sterkt | se MÅ 3 |
| A3 | stemmer, dokumentert | FS:22; FS:110 (A14); FS:622 (S2: to oppgavenumre); G1:15, 77. Oppgavene selv er ikke i kildene |
| B1 | stemmer | ChC:1246–1252 («bootstrap», `encryptionEnabled: false`, `bootstrapOnly: true`), 1248 |
| U1 | for sterkt / upresis | eier alltid mottaker (CC:198–204, 479–483) → eierens nøkkelutvekslingsnøkkel åpner alt (CE:233–244). Innslipp krever signeringsnøkkelen (GC:1350–1403). «Nøkkelen» i entall blander dem (CIV:263–267) |

## Spørsmål 1 — «ligger rundt cellen og ikke i den»
Holder ikke som den står. **Lest:** de fire tekstoperasjonene sjekker bare medlemskap (CC:283, 299, 320, 391), så eier og invitert bruker samme operasjoner — den delen stemmer. Men (a) innslipp: bare eierens nøkkel kan gi avtale, den må bevise seg og signere i cellens prosess (GC:1358–1361, 1374–1384, 1391–1403; bevis krever `identityVault` 2255–2287), og det er cellen selv som velger `.ownerApprovalRequired` (CC:143, 195); en lenket same-entity-identitet kan endre medlemslista, men ikke gi avtaler (GC:1358, 2043–2060); (b) eier-som-mottaker er i cellen (CC:198–204, 479–483) og er grunnen til nøkkelspørsmålet; (c) vedleggsregelen som stenger eieren ute, er i cellen på grenen (VCC:798–817, 865–876). Hvor cellen kjører: klienten krever `cell://<host>/…`, ikke localhost (CCT:64–84), så begge må nå samme vert over broen. **A8, A9, A10 stemmer med koden** (A8: GC:1334–1446; A9: CCl:513–553, Main:25–61; A10: VCC:806–811, 842–848, 872–874). Utkastets linje 18 strider mot A8 og A10. **Slutning:** for eieren som *tekst*sender mangler klient og nøkkelplassering (rundt cellen); for vedlegg og innslipp er det cellen.

## Spørsmål 2 — Forslag A
- `feed` kan stå i en avtale (ChatCell gjør det: ChC:528; GC:1476 sjekker ønsket grant mot malen) — men korrespondansemalen mangler den (CAT:7–12), så CellProtocol må endres, og klienten avviser enhver avtale som ikke er nøyaktig de fire (CCl:528–533; CorrespondenceContracts.swift:17–18). Ingen av de to endringene står i utkastet.
- `neverGrantedKeypaths` (CAT:24–38) nevner ikke `feed` og brukes ikke i kildenes cellekode; hindrer ikke.
- Abonnenter utenfor medlemslista: `flow(requester:)` krever `feed` r--- og revalideres ved medlemsendring (GC:1275–1283, 1943, 1957); i tillegg eieren og lenkede same-entity-identiteter (GC:2043–2060). Vertsprosessen leser Flow uten autorisasjon (`getFeedPublisher`, GC:1265–1270) — for konvolutter bare chiffertekst, som i lageret. Risikoen er en ekstra nøkkel i medlemslista, ikke Flow i seg selv.
- Flow lagres ikke (PassthroughSubject GC:366); frakoblet klient mister hendelsen, derfor trengs `state`-nøkkelen, som ikke finnes (CC:206–279). En `state` med konvolutter omgår «deliberate read»-registreringen (CC:228, 311) — bør sies.
- Om klientens Resolver kan abonnere på en fjern celle over WSS, står ikke i kildene (`CellResolver` mangler) → **kan ikke avgjøres**. Eierens abonnement krever eierbevis fra cellens prosess (GC:2255–2287) — samme spørsmål som innslipp.
- Konvolutten må fortsatt signeres og stemme med medlemsavtrykket (CC:330–347); Flow-levering endrer ikke det.

## Lest mot sluttet
Lest: alle fil:linje over. Sluttet: at eieren får abonnere og sende (policy-klassen, `ChatMessage.messageObject`, `CellResolver` og `AssistantCorrespondenceContracts` er ikke i kildene); at den gamle cellen står på staging (dokument, ikke kode). Ingen kode er kjørt.
