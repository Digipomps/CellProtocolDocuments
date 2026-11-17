# Konferanse som felles kunnskapsrom — OIW som modell

Dato: 2026-10-02. Status: kildebasert vurdering og designforslag, ikke implementeringsgodkjenning eller releasebevis. Oppdragsgiver: Kjetil. Kilder og arbeidskopier ble lest denne datoen; produksjonstilstanden er ikke sertifisert.

## Konklusjon

Vi har en betydelig base: flere arrangører kan opprette og publisere arrangementer med egne medlemsrettigheter, konferanseceller har onboarding, tilgjengelighet og kontaktflyter, Binding har native nearby, og Swarm har en kjørbar arkitektur med administrasjons-API. Vi har ikke påvist en samlet løsning som oppfyller hele ønsket: paraplytilknytning, levende matching mellom alle aktører, frivillig felles kunnskapsbygging, gjensidig opptak/deling, portabel selskapsrepresentasjon og varig entitetsutvidelse mellom selvstendige scaffolds.

Anbefalingen er å bygge videre på disse delene, først med manuelt godkjente kunnskapsbidrag. Integrasjon mellom verter, faktisk rendererparitet og det felles opptaket får egne akseptansekrav. En lokal prototype kan prøves før disse er ferdige, men kan ikke kalles den ferdige konferanseløsningen.

## Hva vi har — og hva som mangler

| Område | Funnet i kode / tidligere bevis | Mangler før ønsket kan regnes som levert |
|---|---|---|
| Eget arrangement | EventPlatform: innlogget publisher-onboarding, utkast, redigering, publisering, arkivering og separate publiserte snapshots | Paraplymodell, tilknytningsforespørsel/godkjenning og sammenhengende deltakerreise; anonym selvbetjening er ikke påvist |
| Flere administratorer | Eksplisitte publisher-rettigheter, inkludert `publishEvent`, `editEvent`, `manageMembers`; vern av siste medlemsadministrator | Portabel selskapsfullmakt, verifisert representasjon, utløp og kontrollskifte/recovery; full medlemsrevokering må etterprøves |
| Formål og matching | Konferanseonboarding, formål, samtykkevalg og individuell tilgjengelighet | Anbefalingscellen bruker fortsatt fem faste kandidater; mangler felles levende indeks for personer, grupper og arrangementer, reell tidsavtale og forklaringer |
| DiMy-rådgivere | Formålsgrunnlag, GoalEvaluationCell og ClaimComposition er reelle byggesteiner | Ingen verifisert sammenhengende DiMy-tjeneste for denne konferansereisen; kildebundet rådgiver-UI, brukeraksept og provider-/kostnadsgrenser må kobles |
| Nearby | Binding/CellApple har scanning, invitasjoner og avgrensede utdrag | Faktisk konferansemyndighet, to-enhetsakseptanse og bro til delt møte er ikke dokumentert ferdig |
| Skeleton-paritet | Omfattende reparasjon og historiske tester i separat kandidat fra 30. september | Kandidaten er ikke vanlig installert/deployet checkout; konferansetema, faktiske møtestater, dark mode og iOS er ikke sertifisert |
| Opptak og transkripsjon | Native taleinput, TranscriptStore og konferansetråder finnes hver for seg | Felles møteplan, deltakergodkjenning, opptakstilstand, versjonskontroll, utvalgt deling og individuelle leveringskvitteringer |
| Entitetsutvidelse | EntityAnchor, signert scaffold-innmelding og lokal vedvarende grafprojeksjon | Full reise mellom selvstendige runtime-instaser; synk, tilbakekalling, konflikt/restart og støtte per faktisk scaffold må bevises |
| Felles konferanseinnsikt | Formål-/påstandsmodeller og innhold kan gjenbrukes | Samlet bidragsmodell med publikum, proveniens, rettelser, dissens og rettigheter; ingen automatisk deling av privat graf |
| Simulering | Swarm coordinator/workers, generiske brukeratferder, metrics og run-administrasjon | OIW-brukerreiser, semantiske forventninger, isolerte testidentiteter/data, opprydding og samlet operatørflate |

Dette er hovedsakelig kildefunn. Tester som finnes i repoet er ikke kjørt i denne vurderingen. Betydelige deler av arbeidskopiene er endret eller utrackede; HEAD alene gjenskaper ikke alt som ble undersøkt. Se [EVIDENCE.md](EVIDENCE.md) og rådgivervedleggene.

## Har Swarm en adminflate?

Tre forskjellige ting må skilles:

1. **Swarm har administrasjons-API i kode:** opprette, inspisere, pause, fortsette og stoppe kjøringer, se brukere/shards, feil og metrics. Det er gjenbruksbasen.
2. **Konferansen har en adminflate i kode** med syntetisk deltakerpopulasjon og inspeksjon/playback. Dette er ikke den komplette Swarm-operatørflaten. Reset fjerner heller ikke nødvendigvis alle vedvarende entiteter og aggregater.
3. **En samlet Swarm Workbench er designet**, og skissene ble godkjent 30. september. Implementerings- og akseptanseporter står fortsatt åpne i den leste statusfilen. OIW-scenarioet bør bli en utvidelse der, ikke en konkurrerende adminløsning.

Simuleringsfanen i den nye skissen er en interaktiv scenarioforhåndsvisning. Den starter ingen Swarm-kjøring og gir ingen målte backendresultater.

## Formål og produktretning

Kjetils føring: «Det gjennomgående formålet for alle i en konferanse bør være å bidra til å gjøre den felles bevisstheten arrangementet utgjør rikere, sekundært utvide egen entitet.»

Designet konkretiserer dette som et **frivillig felles kunnskapsrom**: spørsmål, erfaringer, kilder, argumenter, motargumenter, usikkerhet, neste forsøk og dokumenterte rettelser. Mer data er ikke i seg selv bedre forståelse. Ingen må gi fra seg private notater, hele transkripsjoner eller personlig profil for å delta. Et legitimt bidrag kan være et kritisk spørsmål eller en rettelse; felles forståelse krever ikke enighet.

Sekundært kan hver person velge hva som beriker egen Entity. Et selskap kan motta et godkjent bidrag gjennom sin egen fullmakt. Paraplyen skal ikke eie alle personenes eller selskapenes private grafer.

Foreslått rekkefølge:

1. Stabiliser kilde-/runtimegrunnlaget og prøv arrangement → frivillig bidrag → kildeforankret felles innsikt lokalt.
2. Fullfør en smal, reell to-scaffold-reise med identitetsbinding, avgrenset rettighet, lagring, read-back og tilbakekalling. Lag en støtteoversikt for hvert tilkoblet scaffold.
3. Koble levende formål/tilgjengelighet og DiMy-rådgivere; gjør selskapsroller tydelige og gjenbruk eksisterende publisher-administrasjon.
4. Gjenbruk Swarm for semantiske konferansescenarioer og feiltilfeller; gjennomfør en liten menneskepilot med valgfri deling.
5. Ta med nearby/opptak først etter faktisk rendererparitet og egen test med to enheter. Manuellt oppsummert møte er fullverdig alternativ.

Arbeidspakker, avhengigheter og akseptanse: [PLAN.md](PLAN.md). Datamodell, møtestater, selskaper og GUI: [DESIGN.md](DESIGN.md).

## OIW-rammen

OIW oppgir 19.–22. oktober 2026. Det er en paraply med uavhengige arrangører og separat registrering per arrangement, ikke én felles deltakerliste. I 2026 skiller OIW mellom kuratert hovedprogram og sideprogram. Den publiserte søknadsfristen for sideprogrammet var 13. september. Alle skal kunne lage et HAVEN-arrangement i vårt design; det innebærer ikke offisiell OIW-tilknytning. Ingen slik integrasjon, deltaker-API eller tillatelse er etablert i denne vurderingen. Kilde: [OIW FAQ](https://www.oiw.no/faq), lest 2. oktober 2026.

OIW brukes som referansemodell. Ingen pilotfrist eller avtale med OIW er lovet. Hvis en faktisk oktoberpilot velges, bør første omfang være lite og kunne fungere uten opptak og uten offisiell programintegrasjon.

## Leveranser og avgrensning

- Tre uavhengige kildevurderinger og en utfordret andre adjudikasjon ligger i `advisers/`.
- [analysis-contracts.json](analysis-contracts.json) inneholder analyseformål, mål, påstander, motargumenter og eide åpne spørsmål. Dette er manuell adjudikasjon, ikke et kjøreresultat fra DiMy.
- [EVIDENCE.md](EVIDENCE.md) viser kildeidentitet, primærkilder, begrensninger og kvalitetsdiagnostikk.
- [STATUS.md](STATUS.md) viser hva som faktisk er verifisert i designet.

Denne leveransen endrer ikke konferansens runtime, deploy, opptaksrettigheter eller Swarm-kjøringer. Designet er lagt frem for vurdering; eksisterende godkjenninger fra andre oppgaver utvides ikke til den nye løsningen.
