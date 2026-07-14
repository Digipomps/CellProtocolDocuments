# DiMy/HAVEN ICP og persona-utvikling

Oppdatert: 2026-05-28

Status: arbeidsnotat for å utvikle Ideal Customer Profiles, proto-personaer, Jobs-to-Be-Done og story-scenarioer for DiMy/HAVEN. Dette er ikke validert markedskunnskap. Personaene under er hypoteser som må testes med ekte mennesker før de brukes som salgs-, produkt- eller investeringsbevis.

## Kort konklusjon

Vi bør ikke bare lage "personas". Vi bør lage en stabel:

```text
Segment / miljø
-> Ideal Customer Profile / Ideal Community Profile
-> buying / participation context
-> persona
-> job-to-be-done
-> trigger
-> current workaround
-> DiMy/HAVEN value hypothesis
-> proof needed
-> story scenario
-> validation plan
```

For DiMy/HAVEN er dette ekstra viktig fordi mange aktuelle brukere ikke bare "kjøper et verktøy". De prøver å skape relasjoner, koordinere prosjekter, dele kunnskap, publisere arbeid, beskytte autonomi og unngå plattformer de ikke stoler på. Det betyr at ICP må beskrive **miljøet og situasjonen**, mens persona beskriver **mennesket i et bestemt beslutningsøyeblikk**.

## Kilder sjekket

Sjekket 2026-05-28:

- Qualtrics beskriver ICP som en B2B/account-based profil av organisasjonen eller kontoen som passer best, og skiller ICP fra buyer persona: [Ideal Customer Profiles](https://www.qualtrics.com/articles/strategy-research/ideal-customer-profile/).
- Gartner beskriver ICP som en måte å fokusere B2B sales/marketing på de høyest passende kontoene; siden kunne ikke åpnes direkte på grunn av robots, men søketreffet ble brukt som sekundær bekreftelse: [Gartner ICP](https://www.gartner.com/en/digital-markets/insights/b2b-ideal-customer-profile).
- Harvard Business Review / Christensen m.fl. sin Jobs-to-Be-Done-artikkel vektlegger at man må forstå hvilken fremgang kunden prøver å få til i en konkret situasjon, ikke bare demografi: [Know Your Customers' Jobs to Be Done](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done).
- Interaction Design Foundation beskriver personaer som forskningsbaserte representasjoner som bør brukes sammen med scenarier, og peker på flere persona-tradisjoner: Cooper/goal-directed, role-based, engaging/story og fiction-based: [Personas](https://www.interaction-design.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/personas).
- Microsoft Research beskriver personaer som et supplement til andre usability-metoder, ikke en erstatning for dem: [Personas: Practice and Theory](https://www.microsoft.com/en-us/research/publication/personas-practice-theory/).
- IndieWeb/POSSE er relevant for kunst- og community-personaer fordi det beskriver "Publish on your Own Site, Syndicate Elsewhere" som en måte å redusere avhengighet av sosiale medie-siloer: [POSSE](https://indieweb.org/POSSE).
- European Commission beskriver open-source AI som relevant for innovasjon og digital sovereignty, og knytter åpenhet til lavere barrierer, gjenbruk, transparens og mindre avhengighet av proprietære systemer: [Europe's Open-Source AI Landscape](https://digital-strategy.ec.europa.eu/en/library/europes-open-source-ai-landscape-lever-innovation-and-sovereignty).
- Pådriv beskriver seg som et verktøy for mer handling, særlig der samarbeid på tvers trengs for bærekraftig stedsutvikling: [Pådriv](https://www.paadriv.no/).

## Begrepsmodell

| Begrep | Bruk hos oss | Hva det ikke er |
| --- | --- | --- |
| Segment | Et marked/miljø med lignende situasjon, f.eks. "uavhengige kunstmiljøer" eller "startup-konferanser". | Ikke en konkret kunde eller bruker. |
| ICP | Den typen organisasjon, miljø, arrangement eller fellesskap som passer spesielt godt for DiMy/HAVEN. | Ikke en menneskelig persona. |
| Persona | Et menneske i ICP-en med mål, frykt, beslutninger og språk. | Ikke demografisk pynt. |
| JTBD | Fremgangen personen prøver å få til i en bestemt situasjon. | Ikke en funksjonsliste. |
| Trigger | Hendelsen som gjør at behovet blir akutt. | Ikke en generell interesse. |
| Current workaround | Hva de bruker i dag selv om det er dårlig. | Ikke nødvendigvis konkurrent i snever forstand. |
| Red lines | Hva som gjør at de sier nei eller mister tillit. | Ikke bare "pain points". |
| Proof needed | Hva de må se før de tror på verdiforslaget. | Ikke salgsargument alene. |
| Story scenario | En konkret scene der personen må velge. | Ikke abstrakt pitch. |

## ICP-template

Bruk denne malen per miljø eller pilot:

```text
ICP-navn:
Miljø / account type:
Hvem har problemet:
Hvor problemet oppstår:
Trigger:
Nåværende workaround:
Hvorfor workaround ikke er god nok:
DiMy/HAVEN value hypothesis:
Betaler / sponsor / ressursgiver:
Brukere:
Gatekeepers:
Proof needed:
Red lines:
Payer clarity:
Adoption friction:
Trust sensitivity:
Validation questions:
First story scenario:
```

## Persona-template

Bruk denne malen per menneskelig persona:

```text
Navn:
Rolle:
Tilhører ICP:
Beslutning eller handling:
Job-to-be-done:
Trigger:
Current workaround:
Hvorfor ikke etablerte sosiale medier:
Hva de trenger fra DiMy/HAVEN:
Hva de ikke vil ha:
Proof needed:
Red lines:
Første historie:
Hva vi må validere:
```

## ICP 1: Startup-konferanse for samarbeid og investering

### Ideal Customer / Community Profile

Miljø: fagkonferanse, startup-event, demo day, investor-/founder-arena eller bransjekonferanse der nettverk er viktigere enn passiv innholdsstrømming.

Hvem har problemet:

- gründere som trenger samarbeidspartnere, pilotkunder og investorer,
- arrangører som vil bevise at eventet skaper relevante forbindelser,
- investorer som vil finne founder-signal uten å drukne i pitch-spam,
- sponsorer/partnere som vil ha kvalifisert oppfølging uten å hente rå deltakerdata.

Trigger:

- en founder skal på event med begrenset tid,
- investor-/partnerlisten er verdifull, men vanskelig å navigere,
- vanlige event-apper gir for mye støy og for lite tillit,
- oppfølging etter eventet mister kontekst.

DiMy/HAVEN value hypothesis:

> Gi gründeren en kontrollert måte å signalisere formål, finne relevante samarbeidspartnere og be om investor-/partnerdialog uten å gjøre hele profilen til et åpent lead-produkt.

Payer clarity: relativt høy hvis arrangør eller sponsor betaler for match/audit/reporting; founder kan være bruker, men ikke nødvendigvis betaler.

Trust sensitivity: høy, fordi founder deler tidlige ideer, kapitalbehov, teambehov og strategiske relasjoner.

Proof needed:

- god matching uten global reputation,
- tydelig visibility scope,
- møteforespørsler med formål,
- post-event relationship receipts,
- investor/sponsor får bare avtalt scope.

Anti-ICP:

- events der deltakerne bare vil konsumere innhold,
- rene masseleads-events der sponsor vil ha bred dataeksport,
- miljøer der arrangør ikke bryr seg om tillit eller post-event verdi.

### Persona A: Maja, startup-gründer på jakt etter samarbeidspartnere og investorer

Rolle: founder / CEO i tidlig fase.

Beslutning eller handling: om hun fyller inn startup-profil, signaliserer kapital-/partnerbehov, ber om møter og godkjenner oppfølging.

Job-to-be-done:

> Finne 3-5 relevante personer på konferansen som faktisk kan hjelpe startupen videre: én mulig pilotkunde, én teknisk/kommersiell samarbeidspartner og én investor som skjønner feltet.

Trigger: hun har to dager på konferansen, begrenset energi og trenger bedre filtrering enn LinkedIn-søk og tilfeldig mingling.

Current workaround:

- LinkedIn,
- Notion/Google Doc med target-liste,
- introer via venner,
- pitch-deck på e-post,
- fysisk mingling og tilfeldigheter.

Hvorfor ikke etablerte sosiale medier:

- for mye noise og performativ synlighet,
- uklar kontroll over hvem som ser strategiske signaler,
- algoritmisk feed er dårlig til tidsavgrenset, kontekstuell matching,
- DM-er mister kontekst etter eventet.

Hva hun trenger fra DiMy/HAVEN:

- formålsbasert profil for akkurat dette eventet,
- synlighet per kategori: investor, partner, deltaker, sponsor,
- møteforespørsel med eksplisitt purpose,
- receipts for hvem som fikk hva,
- post-event oppfølging uten permanent offentlig profil.

Hva hun ikke vil ha:

- global founder-score,
- at kapitalbehov blir synlig for alle,
- sponsorleads forkledd som investormatching,
- AI som skriver overdrevent pitchspråk på hennes vegne.

Proof needed:

- hun kan forhåndsvise egen visibility,
- hun ser hvorfor noen matcher,
- hun kan si ja/nei til investor/sponsor/partner scopes separat,
- hun kan eksportere sin egen relasjonshistorikk.

Første historie:

Maja står i kaffekøen mellom to sesjoner. I stedet for å scrolle LinkedIn ser hun tre foreslåtte møter: en investor som eksplisitt investerer i hennes fase, en industripartner som leter etter pilotprosjekter, og en annen founder med komplementær teknologi. Hver forespørsel viser hvorfor matchen finnes og hva som deles hvis hun sier ja.

Hva vi må validere:

- om founder vil fylle ut nok signaler,
- hvor følsomt kapital-/partnerbehov er,
- hvilke investorfelt som er nyttige uten å bli for private,
- om meeting intent gir bedre opplevelse enn vanlig event-app.

### Persona B: Erik, investor-scout med lav toleranse for pitch-spam

Rolle: angel/VC scout eller corporate venture-person.

Beslutning eller handling: om han bruker DiMy til å ta imot møteforespørsler og oppfølging.

Job-to-be-done:

> Finne founder-signal tidlig nok, uten å måtte lese 80 irrelevante pitchmeldinger.

Trigger: han deltar på et event med mange gründere, men har bare 8 åpne slots.

Current workaround: LinkedIn DMs, pitch-konkurranser, introer fra nettverk, Airtable/CRM.

DiMy/HAVEN value hypothesis:

> Investor kan motta forespørsler med tydelig purpose og selvvalgte kriterier, uten å få bred tilgang til founderdata eller skape en global investability-score.

Red lines:

- ranking av gründere som ser ut som objektiv kvalitet,
- skjult scoring fra deltakeratferd,
- at founder antar at matching betyr investeringsinteresse.

Proof needed:

- kriterier er eksplisitte,
- founder ser at dette bare er møteintensjon,
- avslag kan gis høflig og uten sosial skade,
- follow-up er tidsavgrenset.

## ICP 2: Uavhengig kunst- og kulturmiljø

### Ideal Customer / Community Profile

Miljø: kunstnere, kuratorer, atelierfellesskap, små gallerier, visningssteder, performance-/musikk-/tekstmiljøer og lokale kunstarrangører som vil publisere arbeid, avtale møter, invitere til arrangementer og bygge publikum uten å være avhengige av Instagram/Facebook/TikTok.

Hvem har problemet:

- kunstnere som trenger synlighet uten algoritmisk selvpromotering,
- kuratorer og arrangører som trenger ryddig kommunikasjon,
- små miljøer som trenger kalender, invitasjoner, arbeidsdeling og arkiv,
- publikum som vil følge miljøet uten etablerte sosiale medier.

Trigger:

- en kunstner skal lansere en serie arbeider,
- et visningssted skal koordinere åpning, atelierbesøk og dokumentasjon,
- et miljø er lei av at arrangementer og dokumentasjon forsvinner i feed/siloer,
- publikum finnes spredt på e-post, Instagram, Messenger, Signal og tilfeldige nettsider.

DiMy/HAVEN value hypothesis:

> Kunstmiljøet kan ha en egen, purpose-scoped publiserings- og arrangementsflate der kunstneren eier konteksten, avtaler visibility og kan møte publikum uten å gjøre arbeidet avhengig av en sosial medie-feed.

Payer clarity: middels/lav i tidlig fase. Kan være atelierfellesskap, galleri, støtteordning, medlemskap eller prosjektmidler. Bør ikke starte med individuell kunstnerbetaling som hovedcase.

Trust sensitivity: svært høy for kontroll over verk, kontekst, invitasjoner, rettigheter og sosial sårbarhet.

Proof needed:

- enkel publisering,
- egne canonical URLs / arkiv,
- eventinvitasjoner og RSVPs,
- møteavtaler,
- kontroll på hvem som ser uferdig arbeid,
- eksport/portabilitet.

Anti-ICP:

- kunstnere som først og fremst vil maksimere rekkevidde på etablerte plattformer,
- gallerier som bare trenger vanlig web/CMS,
- miljøer uten kapasitet til å drifte eller moderere egen digital flate.

### Persona C: Iben, uavhengig kunstner og arrangør

Rolle: billedkunstner / kurator i lite kunstmiljø.

Beslutning eller handling: om hun publiserer arbeid, inviterer til visning, avtaler møter og bygger kontaktliste i DiMy/HAVEN i stedet for Instagram/Facebook.

Job-to-be-done:

> Vise arbeid på egne premisser, invitere de riktige menneskene og holde kontakt med miljøet uten å måtte mate en algoritmisk feed.

Trigger: hun skal vise en ny serie arbeider, men vil ikke at kontekst, prosessbilder og invitasjoner skal leve på Instagram alene.

Current workaround:

- Instagram-post/story,
- e-postliste,
- Google Forms,
- Messenger/Signal,
- PDF-invitasjoner,
- manuell kalender.

Hvorfor ikke etablerte sosiale medier:

- arbeid reduseres til feed-objekt,
- algoritmen premierer feil type synlighet,
- publikum og arkiv eies av plattformen,
- DM/invitasjoner er rotete,
- det er uklart hva som skjer med bilder/data.

Hva hun trenger fra DiMy/HAVEN:

- portfolio/arbeidsflate med egne URLs,
- events med invitasjon, RSVP og møtebooking,
- publisering til egen flate først, eventuelt syndikering senere,
- grupper med forskjellig visibility: offentlig, samlere, kolleger, samarbeidspartnere,
- dokumentasjon og kunnskapsdeling mellom prosjekter.

Hva hun ikke vil ha:

- likes/follower-race,
- global reputation-score,
- AI som tolker eller markedsfører kunsten uten samtykke,
- at publikum blir leads for kommersiell utnyttelse.

Proof needed:

- kontroll på rettigheter og synlighet,
- enkel migrering/eksport,
- lav friksjon for publikum uten konto,
- god invitasjonsflyt,
- trygg moderering.

Første historie:

Iben legger ut tre nye arbeider på sin egen kunstflate, lager et atelierbesøk for 20 inviterte og åpner for fem én-til-én-møter med kuratorer. Hun kan dele offentlig dokumentasjon, men holde prosessnotater og uferdige verk for en mindre gruppe.

Hva vi må validere:

- om kunstnere vil bruke en ny flate uten eksisterende publikum,
- hvor viktig egen URL/arkiv er,
- betalingsvilje hos kunstner vs. visningssted,
- hvilke publiseringsfunksjoner som må finnes fra dag én.

### Persona D: Lukas, kurator/visningsstedskoordinator

Rolle: koordinator i et lite galleri, atelierfellesskap eller kunsthall.

Beslutning eller handling: om han bruker DiMy/HAVEN til program, invitasjoner, møter, dokumentasjon og intern koordinering.

Job-to-be-done:

> Samle program, kunstnere, publikum og dokumentasjon uten å spre alt over fem verktøy og tre sosiale medier.

Trigger: en gruppeutstilling krever kunstneravtaler, åpning, omvisninger, presse, dokumentasjon og etterarbeid.

Current workaround: e-post, Google Drive, Instagram, Facebook-event, Doodle, regneark.

DiMy/HAVEN value hypothesis:

> Visningsstedet får en lett arrangements- og dokumentasjonsflate der hvert prosjekt kan ha egne roller, avtaler, invitasjoner og arkiv.

Red lines:

- verktøyet blir for tungt for kunstnere,
- publikum må opprette konto for alt,
- rettigheter rundt bilder/tekst blir uklare.

Proof needed:

- ett fungerende prosjektrom,
- enkel invitasjon,
- rollebasert dokumentdeling,
- eksport til egen nettside eller arkiv.

## ICP 3: AI-miljø og digital uavhengighet

### Ideal Customer / Community Profile

Miljø: AI-byggere, open-source-/maker-miljøer, forskere, uavhengige utviklere, AI safety-/governance-folk, små produktteam og teknologer som liker ny teknologi, men ser økende risiko ved avhengighet av proprietære AI-/cloud-/social stacks.

Hvem har problemet:

- folk som eksperimenterer raskt med AI og agentic workflows,
- grupper som vil dele kunnskap uten å gi alt til etablerte plattformer,
- utviklere som ønsker audit, receipts, BYOK/BYOM og egne data boundaries,
- miljøer som vil snakke om digital uavhengighet uten å bli anti-teknologi.

Trigger:

- AI-verktøy blir mer kraftige og mer sentraliserte,
- teamet mister oversikt over hvor prompt/data flyter,
- open-source AI blir realistisk nok for flere use cases,
- personlige og kollektive kunnskapsbaser blir strategiske aktiva.

DiMy/HAVEN value hypothesis:

> AI-miljøet kan få en eksperimentell, transparent samarbeidsflate der AI-bruk, data, agreements, prompts, model/provider choices og knowledge sharing er eksplisitte og auditbare uten å bremse utforskning.

Payer clarity: middels. Early adopters kan være design partners, labs, små team eller communities; penger kommer trolig via hosted workspace, AI entitlement, support eller sponsor/partner.

Trust sensitivity: høy, men på teknisk måte: de vil se logs, control, portability, model/provider boundaries og mulighet for egen infra.

Proof needed:

- AI usage metering uten prompt leakage,
- BYOK/BYOM eller provider transparency,
- exportable knowledge base,
- role-scoped sharing,
- clear audit of what left the local/domain boundary.

Anti-ICP:

- rene AI-hype-miljøer som bare vil ha siste demo,
- enterprise buyers som krever full compliance før produktet finnes,
- folk som ikke bryr seg om data/control/independence.

### Persona E: Jonas, AI-utforsker som har blitt digital uavhengighets-bevisst

Rolle: uavhengig AI-utvikler, prototypebygger eller teknisk community-person.

Beslutning eller handling: om han bruker DiMy/HAVEN som arbeidsflate for eksperimenter, kunnskapsdeling, møter og digitale avtaler.

Job-to-be-done:

> Utforske ny AI-teknologi raskt sammen med andre, men samtidig forstå hvor data, prompts, kostnader og avhengigheter går.

Trigger: han har sett hvor fort AI-verktøy endres og hvor mye kunnskap som låses i proprietære chats, SaaS-kontoer og lukkede communities.

Current workaround:

- Discord/Slack,
- GitHub,
- Notion/Obsidian,
- ChatGPT/Claude/Gemini,
- Hugging Face,
- Google Drive,
- X/LinkedIn.

Hvorfor ikke etablerte sosiale medier:

- støy og hype gjør kvalitet vanskelig,
- kunnskap blir fragmentert,
- algoritmisk synlighet favoriserer demo fremfor forståelse,
- diskusjoner og relasjoner blir fanget i plattformer,
- data/prosjekter blandes med offentlig persona.

Hva han trenger fra DiMy/HAVEN:

- prosjektrom for AI-eksperimenter,
- knowledge sharing med source/provenance,
- model/provider receipts,
- AI cost/usage visibility,
- lokale eller domain-scoped identiteter,
- møte- og samarbeidsavtaler,
- digital independence som praktisk workflow, ikke manifest.

Hva han ikke vil ha:

- enterprise compliance-teater,
- sosial feed med reputation-score,
- AI som skjuler hvilke modeller/verktøy den bruker,
- lock-in til én provider.

Proof needed:

- kjørbar demo,
- export av data/prosjekt,
- audit av AI-kall,
- mulighet for bring-your-own-key/model senere,
- tydelig skille mellom public sharing og project-private work.

Første historie:

Jonas samler fem personer til en kveld om lokale AI-agenter. I DiMy/HAVEN lager han et prosjektrom, deler ressurser, avtaler to demoer, lar deltakerne legge inn egne interesser, og ser etterpå hvilke AI-verktøy og kostnader som faktisk ble brukt uten at råpromptene blir delt i rapporten.

Hva vi må validere:

- hvilke AI-communities som faktisk har dette problemet,
- om audit/receipts er verdifullt nok,
- hvor mye friksjon de tåler,
- hvilke providers/modeller som må støttes først.

### Persona F: Aisha, AI governance- og community bridge

Rolle: person som oversetter mellom teknologer, policy, civic actors og organisasjoner.

Beslutning eller handling: om hun bruker DiMy/HAVEN for å koordinere workshops, dele kunnskap og bygge ansvarlig AI-praksis på tvers.

Job-to-be-done:

> Få teknologer, samfunnsaktører og beslutningstakere til å lære av hverandre uten at alt reduseres til LinkedIn-poster eller lukkede Slack-kanaler.

Trigger: en workshop om AI i lokalsamfunn eller offentlig sektor trenger trygg dokumentasjon, deling og oppfølging.

Current workaround: Miro, Google Docs, Slack, LinkedIn, e-post, Zoom, arrangementssider.

DiMy/HAVEN value hypothesis:

> Hun kan drive AI-samtaler som er praktiske, sporbare og inkluderende, med tydelig scope for hva som deles og hva AI brukes til.

Red lines:

- AI-oppsummeringer uten samtykke,
- at teknologene får definere alt,
- at deltakerinnspill blir treningsdata eller markedsføring uten avtale.

Proof needed:

- consent for AI summaries,
- role-scoped workshop notes,
- exportable knowledge artifacts,
- low-friction participation for non-technical people.

## ICP 4: Ideell forening / Pådriv-lignende lokalmiljøprosjekter

### Ideal Customer / Community Profile

Miljø: ideelle foreninger, nabolagsprosjekter, Pådriv-lignende initiativer, byutviklingsnettverk, frivillige prosjekter, lokale arbeidsgrupper og samarbeidsarenaer mellom innbyggere, kommune, næringsliv og sivilsamfunn.

Hvem har problemet:

- prosjektkoordinatorer som må koble mennesker og grupper på tvers,
- frivillige som trenger oversikt uten å leve i Facebook-grupper,
- prosjektledere som vil dele kunnskap mellom prosjekter,
- lokale partnere som trenger møter, arrangementer, beslutninger og dokumentasjon,
- nye deltakere som vil bidra, men ikke vet hvor de passer inn.

Trigger:

- et lokalmiljøprosjekt skal mobilisere frivillige og partnere,
- flere grupper jobber parallelt med overlappende tema,
- kunnskap forsvinner mellom møter,
- etablerte sosiale medier er uegnet eller uønsket,
- man trenger arrangementer, møtebooking og prosjektdokumentasjon i samme flyt.

DiMy/HAVEN value hypothesis:

> En ideell lokal prosjektgruppe kan få et purpose-scoped samarbeidsrom der mennesker, prosjekter, steder, møter, arrangementer og kunnskap henger sammen uten global profilering eller plattformavhengig feed.

Payer clarity: lav/middels. Kan være prosjektmidler, kommune, stiftelse, medlemskap, samarbeidspartner eller DiMy/HAVEN pilot. Dette er sterk mission fit, men tregere kommersielt enn konferanse.

Trust sensitivity: høy. Deltakere kan være frivillige, naboer, aktivister, kommunale ansatte, lokale bedrifter og sårbare grupper. Må ha lave barrierer og tydelige grenser.

Proof needed:

- enkel onboarding,
- prosjekt- og gruppeoversikt,
- møte/arrangement,
- knowledge sharing,
- permissions som vanlige folk forstår,
- ingen global reputation,
- portabilitet og lokal eierskap.

Anti-ICP:

- grupper som egentlig bare trenger en enkel Facebook-gruppe,
- prosjekter uten koordinator eller vedlikeholdsevne,
- politisk konfliktfylte miljøer der verktøyet blir del av maktkamp før governance er tydelig.

### Persona G: Samira, prosjektkoordinator i Pådriv-lignende lokalmiljøprosjekt

Rolle: koordinator/fasilitator for lokale prosjekter i byen.

Beslutning eller handling: om hun samler kommunikasjon, møter, arrangementer og kunnskapsdeling i DiMy/HAVEN.

Job-to-be-done:

> Få mennesker fra ulike grupperinger til å finne hverandre, avtale arbeid, dele kunnskap og holde fremdrift uten at prosjektet blir en kaotisk miks av e-post, Facebook, Slack og tilfeldige dokumenter.

Trigger: et nabolagsprosjekt har mange involverte, men folk mister oversikt over hvem gjør hva, hvilke møter som gjelder og hva tidligere prosjekter har lært.

Current workaround:

- Facebook-gruppe,
- Messenger,
- e-postlister,
- Google Drive,
- Slack/Teams,
- kalenderinvitasjoner,
- manuelle referater.

Hvorfor ikke etablerte sosiale medier:

- noen deltakere vil ikke være der,
- samtaler blir rotete og søkbare på feil måte,
- kunnskap blir ikke strukturert mellom prosjekter,
- plattformen er bygget for feed/attention, ikke lokal handling,
- roller, samtykke og prosjektgrenser er uklare.

Hva hun trenger fra DiMy/HAVEN:

- project spaces med formål,
- people/place/project mapping,
- arrangementer og møtebooking,
- kunnskapsarkiv mellom prosjekter,
- rollebasert deling,
- lavterskel invitasjon for nye deltakere,
- mulighet for AI-fasilitator som hjelper å strukturere formål, ikke score folk.

Hva hun ikke vil ha:

- enda et tungt prosjektstyringssystem,
- global frivilligscore,
- offentlig feed som gjør intern usikkerhet synlig,
- AI som oppsummerer sensitive møter uten samtykke.

Proof needed:

- en fungerende prosjektrom-demo,
- møte- og arrangementsflyt,
- enkel permission-modell,
- export/arkiv,
- eksempler på kunnskapsdeling mellom prosjekter.

Første historie:

Samira skal samle en arbeidsgruppe om gjenbruk av et lokalt bygg. I stedet for å lage enda en Facebook-tråd oppretter hun et prosjektrom med formål, inviterer beboere, kommune, frivillige og lokale aktører med ulike scopes, setter opp et møte, og kobler inn tidligere erfaringer fra et annet nabolagsprosjekt.

Hva vi må validere:

- hvem som betaler,
- hvor lite friksjon frivillige tåler,
- hvilke roller som må finnes,
- om prosjektkunnskap faktisk deles mellom prosjekter,
- hvordan governance bør se ut.

### Persona H: Thomas, frivillig fagperson med lite tid

Rolle: lokal frivillig, fagperson eller nabo som bidrar i korte perioder.

Beslutning eller handling: om han blir med i prosjektrom, møter opp og deler kompetanse.

Job-to-be-done:

> Bidra med konkret kompetanse uten å måtte følge med på alt, lese lange tråder eller bli sittende med permanent ansvar.

Trigger: han blir invitert til å bidra i en arbeidsgruppe, men har lite tid.

Current workaround: e-post, Facebook, WhatsApp, dokumentlenker, møteinnkallinger uten kontekst.

DiMy/HAVEN value hypothesis:

> Thomas får en tydelig "hvor trengs jeg, hva er avtalt, hva er neste møte"-flate uten å måtte bli sosialt fanget i en feed.

Red lines:

- for mange varsler,
- uklart ansvar,
- offentlig synlighet han ikke har samtykket til,
- forventning om å bruke sosial profil.

Proof needed:

- kort oppgaveoversikt,
- møteagenda,
- tydelig exit,
- kontroll på notifications og visibility.

## Tverrgående personaer vi bør ha i tillegg

| Persona | Hvorfor den trengs | Første scenario |
| --- | --- | --- |
| Gatekeeper for personvern/digital rights | Tester om språket vårt tåler kritikk. | "Er dette bare ny sosial plattform med bedre ord?" |
| Sponsor/ressursgiver | Mange miljøer trenger penger eller støtte. | "Hva får jeg lov til å vite uten å hente ut persondata?" |
| Community moderator | Alle miljøer trenger normer og konfliktløsning. | "Hva gjør vi når noen misbruker møte-/publiseringsflaten?" |
| Low-digital-confidence participant | Hindrer at vi bygger for teknologer alene. | "Kan jeg delta uten å forstå CellProtocol?" |
| Archive/knowledge steward | Viktig for kunst, Pådriv og AI. | "Hvordan blir prosjektkunnskap gjenbrukt uten å bli overvåking?" |
| Venue/host | Kunst og lokalprosjekter trenger steder. | "Hvordan kobles arrangement, adgang, kapasitet og ansvar?" |

## Prioritert eksempelpersona-liste

P0 - bygg først:

1. `STARTUP_FOUNDER_CONNECTOR` - Maja, startup-gründer som søker samarbeidspartnere og investorer.
2. `INDEPENDENT_ARTIST_PUBLISHER` - Iben, kunstner som vil publisere og invitere uten etablerte sosiale medier.
3. `AI_INDEPENDENCE_EXPLORER` - Jonas, AI-utforsker som vil teste ny teknologi med digital uavhengighet.
4. `CIVIC_PROJECT_COORDINATOR` - Samira, Pådriv-lignende prosjektkoordinator for lokalmiljø.

P1 - bygg for å forstå kjøp, drift og governance:

5. `INVESTOR_SCOUT` - Erik, investor-scout med lav toleranse for pitch-spam.
6. `ART_SPACE_COORDINATOR` - Lukas, kurator/visningsstedskoordinator.
7. `AI_GOVERNANCE_BRIDGE` - Aisha, brobygger mellom AI, policy og community.
8. `LOCAL_VOLUNTEER_CONTRIBUTOR` - Thomas, frivillig fagperson med lite tid.

P2 - legg til før pilot:

9. `PRIVACY_RIGHTS_CRITIC` - kritisk digital-rettighetsstemme.
10. `COMMUNITY_MODERATOR` - moderator/governance-ansvarlig.
11. `PUBLIC_OR_FOUNDATION_FUNDER` - prosjektfinansierer/stiftelse/kommune.
12. `LOW_DIGITAL_CONFIDENCE_MEMBER` - deltaker som trenger enkelhet og trygghet.

## Hvordan disse personaene bør brukes i story-arbeid

Hver persona skal gi oss tre ting:

1. En sterkere historie: "Hvorfor bryr denne personen seg nå?"
2. En bedre produktbeslutning: "Hvilken funksjon må finnes for at historien er sann?"
3. En valideringstest: "Hva må vi spørre et ekte menneske om?"

Eksempel:

```text
Dårlig historie:
"DiMy gir kunstnere en desentralisert sosial plattform."

Bedre historie:
"Iben skal invitere 20 mennesker til atelierbesøk uten å gjøre prosessbildene sine til Instagram-innhold. Hun trenger en egen flate med invitasjon, møtebooking og kontroll på hvem som ser hva."
```

## Første valideringsplan

### P0 intervjuer

- 3 startup-founders som nylig har deltatt på konferanse/demo day.
- 2 investorer/scouts som får mange uønskede pitchmeldinger.
- 4 kunstnere/kuratorer som aktivt misliker etablerte sosiale medier.
- 3 personer i AI/open-source/digital sovereignty-miljøer.
- 3 lokale prosjektkoordinatorer eller Pådriv-lignende fasilitatorer.
- 3 frivillige/prosjektdeltakere med lav/moderat digital tålmodighet.

### Spørsmål som skal testes

- Hva er dagens workaround?
- Hvor gjør det vondt nok til å bytte?
- Hva er de røde linjene?
- Hvem betaler eller muliggjør bruken?
- Hvilke data/signaler er for sensitive?
- Hvilket første scenario ville gitt umiddelbar verdi?
- Hva må fungere uten at brukeren forstår HAVEN/CellProtocol?

### Hypoteser som ikke kan valideres syntetisk

- betalingsvilje,
- faktisk bytte fra etablerte sosiale medier,
- tillit til digital independence-språket,
- om kunstnere vil publisere på en ny flate uten eksisterende publikum,
- om frivillige tåler enda et verktøy,
- om AI-folk faktisk verdsetter audit mer enn fart,
- om founder/investor-matching oppleves trygg og nyttig.

## Anbefalt neste arbeid

1. Gjør de fire P0-personaene til egne story cards med ett konkret artefakt hver.
2. Lag intervjuguider for founder, kunstner, AI-miljø og Pådriv/lokalmiljø.
3. Kjør syntetisk story-kritikk bare for å finne hull før intervju.
4. Oppdater personaene med faktisk intervju-evidence og marker antakelser som bekreftet, avkreftet eller uklart.
5. Først etter dette: vurder om `PersonaCatalogCell` eller `StoryScenarioRunnerCell` gir nok nytte.

