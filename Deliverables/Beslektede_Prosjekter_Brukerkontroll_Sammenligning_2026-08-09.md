# Beslektede prosjekter målt mot brukerkontroll-kriteriene

Dato: 2026-08-09

Måler et utvalg prosjekter som sier de gir folk kontroll over egne data mot
kriteriesettet i `purpose://self-determination.data`
(se `Brukerkontroll_Kriterier_Til_Formaal_2026-08-04.md`), og argumentanalyserer
påstanden om at dette bare virker hvis det gir et mer produktivt økosystem enn
dagens silobaserte.

Kildene er åpne nettkilder hentet 2026-08-09 og er markert der de er svake.

## 1. Kriteriene som målestokk

Åtte dimensjoner, hver med Goal og verifikator:

| Kode | Formål | Kjernespørsmål |
| --- | --- | --- |
| Fml | `.use-purpose` | Til hvilket erklært formål? |
| Omf | `.scope` | Hvilke felt, hvilken presisjon, hvilken identifiserbarhet? |
| Sted | `.locality` | Hvor lagres og behandles det, hvor mange kopier? |
| Måte | `.manner` | Kobling, profilering, trening — og hvem eier det avledede? |
| Mott | `.recipients` | Navngitt mottaker, synlig videredelegering, default deny |
| Var | `.duration` | Hvor lenge, og virker tilbaketrekking nedstrøms? |
| Etter | `.verifiability` | Kan eier sjekke, eller må eier stole? |
| Utøv | `.exercisability` | Kan en vanlig person faktisk utøve dette på minutter? |

Skala under: `+` dekket og håndhevet, `~` delvis, ved grensen eller kun juridisk,
`–` ikke adressert. Skalaen måler *arkitektonisk dekning*, ikke modenhet.

## 2. Sammenligningen

| Prosjekt | Fml | Omf | Sted | Måte | Mott | Var | Etter | Utøv |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Solid / Inrupt | – | ~ | + | – | ~ | ~ | ~ | – |
| AT Protocol / Bluesky | – | – | ~ | – | – | – | ~ | ~ |
| Nostr | – | – | ~ | – | – | – | ~ | – |
| MyData / DGA-intermediærer | ~ | ~ | ~ | ~ | ~ | ~ | – | ~ |
| IDS / Gaia-X dataspaces | + | ~ | + | + | + | + | ~ | – |
| EUDI-lommebok / VC+DID | ~ | + | + | – | ~ | – | ~ | + |
| MCP / agent-stacken | – | – | – | – | – | – | – | ~ |
| HAVEN (design) | + | + | + | + | + | + | + | + |
| HAVEN (implementert) | + | ~ | ~ | ~ | + | ~ | ~ | ~ |

### Solid / Inrupt

Nærmest i intensjon: personlig pod, appene kommer til dataene i stedet for
omvendt. Tilgangskontroll (WAC/ACP) er ressurs- og agentbasert.

Sterk på `.locality` — valg av pod-leverandør er en reell stedskontroll og den
dimensjonen Solid gjør best av alle her. Svak på alt som gjelder *etter* at data
er lest: ingen formålsbinding i tilgangsmodellen, ingen kontroll over kobling,
profilering eller modelltrening, og tilbaketrekking virker framover mot poden,
ikke mot kopien mottakeren allerede har. Etterprøvbarhet er ikke en
førsteklasses egenskap: eier må stole på pod-operatør og app. Utøvbarhet er
svakest — WebID, valg av leverandør og ACL-redigering er ekspertoppgaver.

Økosystem: tyngdepunktet har flyttet seg fra forbruker til offentlig sektor og
B2B. Athumi i Flandern bygger datahvelv for 6,5 millioner innbyggere, med
utvidet Inrupt-partnerskap og bruksområder i bemanning, utdanning, energi og
helse, og støtte til fem nederlandske mediehus. Motsatt signal: OpenWallet
Foundations `solid-data-wallet`-lab ble arkivert i april 2026 på
vedlikeholdernes forespørsel — ett datapunkt, ikke en trend, men det peker mot at
forbrukerlommeboken ikke fant fotfeste.

### AT Protocol / Bluesky

Kontroll her betyr *exit*: portabel DID-identitet og et repo som kan flyttes til
en annen PDS. Alt annet er bevisst gitt opp — repoet er offentlig, firehosen er
åpen, og indeksering er poenget. Det gir null på formål, omfang, måte, mottakere
og varighet, og det er et designvalg, ikke en mangel.

Verdt å merke seg: dette er det klart mest produktive økosystemet blant
kontrollprosjektene (over 1 000 aktive tredjepartsapper ukentlig, ~20 mrd
offentlige records, 43,5 mill. brukere per april 2026) — og det er oppnådd ved å
levere den svakeste formen for kontroll. Samtidig kjører en forsvinnende liten
andel egen PDS (observatører anslo ~10 000 av 25 mill. brukere i 2025), så exit
er en rett som nesten ingen utøver.

### Nostr

Identitet er en nøkkel, publisering går til relays. Radikal sensurresistens, men
kontroll i vår forstand finnes ikke: ingen tilbaketrekking, ingen mottakerstyring,
ingen recovery. Utøvbarhet er dimensjonen det bryter hardest på — mister du
nøkkelen, mister du personen. Brukertall er små og omstridte; tall fra
enkeltrelay-statistikk bør ikke brukes som globale tall.

### MyData / DGA-intermediærer (digi.me, Meeco, polypoly, datanyttebedrifter)

Institusjonell løsning: en nøytral mellommann som ikke får utnytte dataene
kommersielt, med samtykkeforvaltning som produkt. Kriteriene dekkes juridisk,
ikke maskinhåndhevet — og settet vårt forkaster nettopp «tillit til
organisasjon» som kriterium, så `.verifiability` faller.

Den viktigste empirien i hele oversikten ligger her: digi.me klarte å få folk til
å laste opp data, men ikke å skaffe etterspørselssiden. I et dokumentert forsøk
lot det seg ikke gjøre å finne én app å dele dataene med. Tilbudssiden alene er
verdiløs.

### IDS / Gaia-X dataspaces

Mekanisk den nærmeste slektningen til HAVEN: ODRL-baserte bruksvilkår med
permissions, prohibitions og obligations, håndhevet av en connector *hos
mottakeren*. Formål, mottakere, varighet, sted og måte finnes som
førsteklasses policy-begreper.

To lærdommer. Positiv: HAVENs modell er ikke teknisk urealistisk — den finnes i
produksjonsnære B2B-implementasjoner. Negativ: prisen er et sertifiseringsregime.
Håndheving forutsetter at motparten kjører en godkjent connector, og feltet
sliter allerede med at implementasjoner definerer egne policy-språk ved siden av
ODRL, med tilhørende inkompatibilitet, og med dokumentasjon som forskere
beskriver som en reell hindring for utbredelse. Eier er dessuten en virksomhet,
ikke en person: `.exercisability` er ikke i mandatet.

### EUDI-lommebok / verifiserbare legitimasjoner

Sterkest på `.scope`: selektiv utlevering gir en reell gradering av
identifiserbarhet, bedre enn noe annet i tabellen. Sterk på `.exercisability` av
en grunn ingen andre kan kopiere — statlig distribusjon. Alle 27 medlemsstater
skal tilby en lommebok innen 24. desember 2026, privat sektor skal akseptere den
fra desember 2027, og EØS-land inkludert Norge har ett års utsettelse.

Men modellen er attributt-formet, ikke dataflyt-formet: når en attest er vist, er
den kopiert. `.duration` og `.manner` finnes ikke. Kontrollen slutter i det
øyeblikket verifikasjonen lykkes.

### MCP / agent-stacken

Ikke et brukerkontrollprosjekt, og tas med fordi det er den faktiske
konkurrenten om produktivitetsargumentet. Over 10 000 aktive offentlige servere,
overdratt til Agentic AI Foundation under Linux Foundation i desember 2025, og
undersøkelser som viser rundt 41 % av spurte utviklingsorganisasjoner i
produksjon i 2026. Kriteriedekning: null, bortsett fra en engangs
brukergodkjenning uten formål, varighet eller etterprøvbarhet.

MCP løser nøyaktig den friksjonen silomodellen påfører — og gjør det uten å gi
brukeren noe.

### HAVEN

Eneste i tabellen som har alle åtte dimensjonene som eksplisitte, testbare mål.
Det er en reell forskjell, men den er per i dag en forskjell i *kriteriesett*, og
kriteriesettet er ennå en `candidate`-gren i kunnskapsbasen.

Implementert side: avtalelivsløp med RWXS-form, betingelser, evidence,
enforcement og VC-evalueringskvitteringer (Book 04), resolver med default deny
(Book 06). Svakest der det betyr mest for differensieringen: nedstrøms
tilbaketrekking med kvittering per mottaker, komplett kopi-inventar per eier, og
brukerstier som holder utøvbarhetskriteriet. Ingen av disse bør omtales som
innfridd før verifikatorene i formålsgrenen faktisk kjører grønt.

## 3. Det strukturelle funnet

Sorter dimensjonene etter hvor de håndheves:

- **Ved eierens grense** (Sted, Omfang, Mottakere ved utlevering): kan håndheves
  ensidig. Solid og EUDI får disse til uten at noen andre er med.
- **Etter utlevering** (Formål, Måte, Varighet, Etterprøvbarhet): kan i prinsippet
  ikke håndheves ensidig. De krever at mottakeren kjører noe som respekterer
  vilkårene, eller at et regime tvinger det fram.

HAVENs differensierende dimensjoner ligger alle i den andre gruppen. Det betyr at
økosystemspørsmålet ikke bare er en vekststrategi for HAVEN — det er
*håndhevingsforutsetningen* for nettopp de kriteriene som skiller HAVEN fra
Solid. Solid kan levere sin (svakere) kontroll uten økosystem. HAVEN kan ikke.

Dette er også grunnen til at IDS/Gaia-X er den mest lærerike naboen: de har valgt
samme håndhevingsmodell og betaler prisen i form av sertifisering, connectorer
og policy-språkstyring.

## 4. Argumentanalyse av produktivitetspåstanden

### Anker

> **P1** «dette bare vil virke om det leder til et mer produktivt økosystem enn
> dagens silobaserte» (oppdrag, 2026-08-09)

P1 er en **nødvendig betingelse**, ikke tilstrekkelig. Tre ord er
underbestemte: *virke* (fungerer teknisk / blir tatt i bruk / leverer kontrollen
det lover), *produktivt* (samlet output / nytte per deltaker / utviklerhastighet
/ verdifangst), og *dagens silobaserte* (silomodellen er høyproduktiv på de
fleste marginer — sammenligningen må stedfestes).

### Restatements som ligger i nærheten, og retningen de kan brukes i

| ID | Omformulering | Relasjon til P1 | Lovlig retning |
| --- | --- | --- | --- |
| P1a | «hvis økosystemet blir mer produktivt, vil HAVEN virke» | omvendt implikasjon | ingen — bytter nødvendig mot tilstrekkelig |
| P1b | «HAVEN må slå silomodellen på produktivitet på alle områder» | sterkere | kun støtte, aldri gjendriving |
| P1c | «HAVEN må gi noen deltakere mer nytte enn silomodellen på minst én margin» | svakere | kun gjendriving, aldri støtte |
| P1d | «brukerkontroll er ikke nok i seg selv» | svakere | kun gjendriving |

Den vanligste feilen i denne typen argumentasjon er å bruke P1c eller P1d som
*støtte* for at P1 er innfridd («vi er jo mer produktive for utviklere, altså
virker det»). Det er en retningsovertredelse: en svakere påstand kan ikke bære en
sterkere konklusjon. Den nest vanligste er P1a — å behandle produktivitet som
tilstrekkelig, som er den feilen MCP-eksempelet gjør synlig.

### Holder P1?

**Støtte, i styrkerekkefølge:**

1. *Empirien for tilbudsside-alene er entydig negativ.* digi.me fylte lageret og
   fant ingen etterspørselsside. Personal Data Store-bølgen 2012–2022 etterlot
   ingen økosystem. GDPR art. 20 ga rettigheten uten interoperabilitet, og bruken
   forble lav — forskningen peker på manglende interoperabilitet og manglende
   bruksområder, ikke på manglende rettighet.
2. *Tosidig marked.* Et kontrollag er en plattform med klassisk
   høne-og-egg-problem. Brukersiden har null nytte uten tjenestesiden, og
   tjenestesiden bærer integrasjonskostnaden. Uten en produktivitetsgevinst er
   det ingen som betaler den kostnaden frivillig.
3. *Kontroll har egenkostnad.* Beslutningsbelastning, latens og
   utøvbarhetskravet koster. Vokser ikke kaken, er kontroll ren omfordeling — og
   motparten i omfordelingen eier integrasjonsflatene.

**Motargumenter og grenser:**

1. *Mandatveien er et reelt moteksempel.* UK Open Banking oppsto ikke fordi
   økosystemet var mer produktivt, men fordi CMA påla de ni største bankene en
   felles API-standard i 2016. Produktiviteten kom etterpå: 18,81 millioner
   brukerkoblinger i juni 2026 og 2,81 milliarder API-kall den måneden alene.
   EUDI-lommeboken følger samme mønster med frist 24. desember 2026. P1 er derfor
   for sterk som formulert: «bare om» ignorerer at et mandat kan erstatte
   produktivitetsbeviset i adopsjonsfasen.
2. *Aggregert produktivitet er ikke beslutningsvariabelen.* Ingen aktør velger ut
   fra økosystemets samlede produktivitet; de velger ut fra marginalnytten for
   sin egen neste oppgave. Standarder som var mer produktive i aggregat har tapt
   mot siloer gang på gang. Den operative formen er derfor per deltaker, ved
   første kontakt — i praksis det samme kriteriet som «de første 60 sekundene»
   fra Arendalsuka-beredskapen.
3. *Baselinen må stedfestes.* Siloer er svært produktive innenfor sitt eget
   domene. De er svake på nøyaktig tre marginer: sammensetning på tvers av
   tjenester, handling utført av agenter på vegne av en person, og bruk som
   krever dokumentert grunnlag. Det er der sammenligningen har mening; alle andre
   steder taper man den.

**Det avgjørende, og ubehagelige, forbeholdet:** selv om P1 er sann, er den ikke
en strategi, fordi *produktivitet ikke trenger kontroll*. MCP demonstrerer at
integrasjonsgevinsten kan hentes ut uten å gi brukeren en eneste av de åtte
dimensjonene — raskere, billigere og med færre parter å overtale. En generell
produktivitetsfordel selekterer altså ikke for HAVEN.

### Reformulering

> **P1′** HAVEN virker bare hvis det finnes minst én margin der en deltaker får
> høyere nytte enn i silomodellen *fordi* brukerkontrollen er der — ikke ved
> siden av den — eller hvis et mandat pålegger adopsjon før den marginen finnes.

P1′ er svakere enn P1 og kan derfor ikke brukes til å hevde at P1 er innfridd.
Den er brukbar i motsatt retning: klarer man ikke å utpeke marginen, faller også
P1.

Kandidatmarginer der produktiviteten er *avledet av* kontrollen:

- **Sammenstillinger som ellers er ulovlige.** Helse × arbeid × utdanning kan
  ofte bare kobles hos eieren. Der er eierens runtime den eneste lovlige
  koblingspunktet — Athumi-porteføljen peker i den retningen.
- **Lavere risikokostnad på etterspørselssiden.** Formålsbundet tilgang med
  kvittering gjør bruk billigere å forsvare enn samme bruk uten. Dette er DGA- og
  dataspace-tesen, og den er testbar mot faktisk betalingsvilje.
- **Agenter som får lov.** Den bindende skranken for agenter i produksjon er
  sjelden modellkvalitet; det er at ingen kan bevise hva agenten hadde lov til.
  Beviselig formålsbundet fullmakt er en produktivitetsegenskap som ikke kan
  kopieres av MCP uten å bygge det HAVEN allerede har.

### Selvkontroll av denne analysen

Konklusjonen i punkt 3 («økosystem er håndhevingsforutsetning, ikke bare
vekststrategi») er elegant nok til å utløse skillets egen advarsel. Kontroll:
den hviler ikke på en omformulering av P1, men på en egenskap ved kriteriesettet
som kan sjekkes uavhengig — hvilke av de åtte dimensjonene som kan håndheves
ensidig ved eierens grense. Den holder også om P1 forkastes.

Reformuleringen P1′ er svakere enn P1 og brukes ikke noe sted til å konkludere
at P1 er innfridd.

## 5. Åpne spørsmål

1. Hvilken av de tre kandidatmarginene skal måles først, og med hvilken
   verifikator? Ingen av dem har i dag et tall.
2. Hvor mange av de åtte dimensjonene kan HAVEN håndheve når *motparten ikke*
   kjører HAVEN? Svaret avgjør hva som kan hevdes offentlig i dag.
3. Er mandatveien (EUDI-tilslutning, norsk offentlig sektor) en snarvei eller en
   avsporing, gitt at EUDI-modellen mangler `.duration` og `.manner`?

## Kilder

- <https://solidproject.org/about>
- <https://www.inrupt.com/case-study/flanders-strengthens-trusted-data-economy>
- <https://www.inrupt.com/blog/athumi-inrupt-cronos-groep-extend-partnership>
- <https://athumi.be/en/technologies/solid>
- <https://github.com/openwallet-foundation-labs/solid-data-wallet>
- <https://dl.acm.org/doi/full/10.1145/3771554>
- <https://arxiv.org/pdf/2210.08270>
- <https://backlinko.com/bluesky-statistics>
- <https://dustycloud.org/blog/how-decentralized-is-bluesky/>
- <https://www.eff.org/deeplinks/2024/12/what-you-should-know-when-joining-bluesky>
- <https://bitcoinmagazine.com/technical/solving-nostr-key-management-issues>
- <https://eike-global.medium.com/how-can-we-make-mydata-principles-a-reality-72bd9c2ab087>
- <https://www.sciencedirect.com/science/article/pii/S0267364923000407>
- <https://petsymposium.org/popets/2021/popets-2021-0051.pdf>
- <https://arxiv.org/pdf/2309.11289>
- <https://ceur-ws.org/Vol-3606/paper41.pdf>
- <https://internationaldataspaces.org/idsa-data-space-connector-report/>
- <https://www.signicat.com/blog/eudi-wallets-only-one-year-to-launch>
- <https://www.namirial.com/en/blog/stories/status-check-eudi-wallet/>
- <https://www.openbanking.org.uk/insights/2-billion-api-calls-and-15-million-users-a-landmark-month-for-open-banking-in-the-uk/>
- <https://thepaymentsassociation.org/article/the-state-of-open-banking-payments-in-the-uk-in-2026/>
- <https://blog.modelcontextprotocol.io/posts/2026-07-28/>
- <https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol>
