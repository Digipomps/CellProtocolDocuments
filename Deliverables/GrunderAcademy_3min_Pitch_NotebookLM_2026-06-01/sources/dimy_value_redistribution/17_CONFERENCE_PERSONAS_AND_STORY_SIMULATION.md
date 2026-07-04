# DiMy konferanseprodukt: personas, story-test og swarm-simulering

Oppdatert: 2026-05-22

Status: proto-persona- og simuleringsnotat for kommunikasjon, produktprioritering og story-kritikk. Dette er ikke validert brukerinnsikt, juridisk vurdering eller markedsbevis. Personaene under skal brukes til å skjerpe hypoteser og finne hull før reelle intervjuer, demoer og pilotavtaler.

## Kort konklusjon

Det er en god ide å definere personaer for DiMy-konferanseproduktet, men bare hvis de brukes som **scenario- og beslutningsmodeller**, ikke som dekorative fiktive profiler.

Swarm-simulering er også nyttig, men med en tydelig etikett:

> Syntetiske personaer kan hjelpe oss å generere innvendinger, alternative historier og testbare hypoteser. De kan ikke validere betalingsvilje, samtykkerate, juridisk aksept eller faktisk brukeradferd.

Den beste bruken nå er:

- test av pitch mot ulike roller,
- red-team av personvern, consent og value-return-språk,
- prioritering av hvilke bevis vi mangler,
- trening av Arthur Scott-style historier før vi viser dem til mennesker,
- generering av intervjuguider og demo-scenarioer.

## Kilder sjekket

Sjekket 2026-05-22:

- Interaction Design Foundation beskriver personaer som fiktive, men forskningsbaserte representasjoner av brukergrupper, og understreker at personaer ikke har verdi alene før de brukes i scenarier: [Personas - A Simple Introduction](https://ixdf.org/literature/article/personas-why-and-how-you-should-use-them).
- Interaction Design Foundation beskriver user scenarios som historier som forklarer motivasjon, kontekst, pain points og forventede interaksjoner, ikke bare tekniske use cases: [What are User Scenarios?](https://ixdf.org/literature/topics/user-scenarios).
- Atlassian sin persona-mal peker på mål, utfordringer, motivatorer og informasjonskilder som praktiske felt i persona-arbeid: [User persona template](https://www.atlassian.com/software/confluence/templates/persona).
- En 2025/2026-artikkel om interactive virtual personas finner at LLM-baserte personaer kan gi rask, brukerlik feedback, men at designere advarer mot bias, overoptimisme og manglende autentisitet uten ekte stakeholders: ["She was useful, but a bit too optimistic"](https://arxiv.org/abs/2508.19463).
- UXAtlas sin 2026-oppsummering av synthetic users anbefaler dem særlig til hypotesegenerering og pre-test av researchopplegg, men advarer mot å behandle dem som ekte research: [Synthetic Users: What the Evidence Actually Shows](https://www.uxatlas.io/articles/synthetic-users-evidence).

Jeg fant ikke en relevant offentlig metodekilde for navnet "Arthur Scott" i denne konteksten. I dette notatet behandles Arthur Scott som deres interne/eksterne story-praksis: en måte å skrive konkrete verdiforslag fra mottakerens situasjon, konflikt og bevisbehov.

## Persona-format

DiMy-personaene bør holdes rolle- og beslutningsnære. Ikke start med alder, hobby og generisk livsstil. Start med hva personen kan akseptere, avvise, kjøpe, blokkere eller anbefale.

Anbefalt feltsett:

| Felt | Hvorfor |
| --- | --- |
| Rolle i verdikjeden | Avklarer om personen er bruker, kjøper, betaler, gatekeeper, kritiker eller beneficiary. |
| Beslutning personen påvirker | Gjør personaen operativ i pitch og produktvalg. |
| Job-to-be-done | Holder fokuset på situasjonen, ikke demografi. |
| Dagens workaround | Viser hva DiMy konkurrerer med i praksis. |
| Frykt og rode linjer | Avdekker hva som dreper tillit eller salg. |
| Bevis som trengs | Binder kommunikasjon til demo, rapport, audit, pris eller juridisk underlag. |
| DiMy-krok | Hvilken del av verdiforslaget som faktisk treffer. |
| Story-moment | En konkret scene der personen må velge. |
| Swarm-knobs | Parametre som kan varieres i simulering. |
| Real validation needed | Hva som må sjekkes med ekte mennesker. |

## Persona-katalog

### P1. Konferansedeltaker: Nora, faglig nettverksbygger

Rolle: deltaker og potensiell beneficiary.

Beslutning: om hun fyller ut profil, godkjenner sponsorinteresse, bruker møte-/matchingflyt og stoler på plattformen etter eventet.

Job-to-be-done: finne relevante folk, sesjoner og oppfølging uten å bli gjort til et skjult lead-produkt.

Dagens workaround: LinkedIn, QR-koder, badge scans, tilfeldig mingling, manuelle notater og etterarbeid.

Frykt og rode linjer:

- at samtykke blir pakket inn som "bedre opplevelse",
- at profilen brukes bredere enn hun skjønte,
- at sponsoroppfølging blir spam,
- at value-return brukes som lokkemiddel for datadeling.

Bevis hun trenger:

- enkel forklaring av hvem som spør, hvorfor, hva som deles og hvor lenge,
- receipt for consent,
- revoke/reclaim som faktisk gjør noe,
- rollebegrenset innsyn i hva som skjedde.

DiMy-krok:

> Du bestemmer hva som deles, hvorfor det deles, og kan se når egen deltakelse skaper kommersiell verdi.

Story-moment: Nora får en sponsorforespørsel etter en sesjon. Hun ser at matchen skyldes eksplisitte interesser hun selv la inn, at sponsoren bare får avtalt scope, og at hun kan trekke samtykket senere.

Swarm-knobs: privacy sensitivity, networking urgency, sponsor trust, time pressure, clarity tolerance.

Real validation needed: consent copy, receipt UX, revoke-forståelse og faktisk vilje til å godkjenne sponsoroppfølging.

### P2. Personvern- og digitale-rettigheter-persona: Elias, kritisk tillitsvakt

Rolle: ekstern kritiker, mulig alliert, community-stemme og red-team.

Beslutning: om DiMy-historien oppleves som ansvarlig eller som "lead harvesting med penere ord".

Job-to-be-done: beskytte deltakere mot skjult profilering, uklare samtykker, global identitet og kommersialisering av persondata.

Dagens workaround: kritisk offentlig debatt, personvernpolicy-gjennomgang, klager, friksjon mot eventplattformer.

Frykt og rode linjer:

- global reputation,
- global identity eller skjult cross-domain linkage,
- samtykke som ikke er spesifikt, frivillig og reverserbart,
- "credits" som blir money-like uten avklaring,
- at sponsorverdi fremstilles som deltakerfordel uten reell kontroll.

Bevis han trenger:

- dataminimeringskart,
- purpose/interest-modell uten ranking/profilscore,
- audit som ikke eksponerer private payloads,
- eksplisitt v0-grense: ingen transferability, cash-out, P2P eller multi-vendor credit network.

DiMy-krok:

> Sponsorverdi kan gjøres målbar uten at deltakerdata blir en svart boks.

Story-moment: Elias leser pitch decket og markerer hvert sted der ordene "value return", "trust", "credit" eller "lead" kan misforstås.

Swarm-knobs: suspicion level, legal literacy, technical literacy, tolerance for commercial sponsor models.

Real validation needed: språk for samtykke, claim-safety, personvernkonsekvens og om kritiske aktører oppfatter modellen som legitim.

### P3. Arrangør: Ingrid, partner- og inntektsansvarlig

Rolle: kjøper, budsjetteier eller sterk intern sponsor hos arrangør.

Beslutning: om DiMy får pilot, betalt event eller anbefaling inn i neste års sponsorprogram.

Job-to-be-done: skape sponsorinntekt og god deltakeropplevelse med mindre manuelt rapportarbeid og lavere tillitsrisiko.

Dagens workaround: sponsorlogoer, badge scans, manuelle rapporter, CRM-eksport, spørreskjema og magefølelse.

Frykt og rode linjer:

- at løsningen blir teknisk tung å forklare,
- at sponsorer ikke betaler for unlocks,
- at deltakere reagerer negativt,
- at rapporten ikke kan brukes i neste sponsorfornyelse.

Bevis hun trenger:

- demo av deltaker-, sponsor- og arrangørflyt,
- pris med synlig kostgrunnlag,
- eksempelrapport for styre/sponsor,
- klare roller, supportmodell og databehandlergrunnlag.

DiMy-krok:

> Selg bedre sponsorverdi uten å miste deltakernes tillit.

Story-moment: Ingrid sitter etter eventet og skal forklare til hovedsponsor hvorfor de bør fornye. DiMy-rapporten viser consent-rate, qualified leads, unlocks, reclaims, ressurskost og rollebegrenset audit.

Swarm-knobs: sponsor pressure, admin capacity, privacy concern, budget size, event maturity.

Real validation needed: arrangørens kjøpsprosess, budsjettlinje, betalingsvilje for transparency pack og supportbehov.

### P4. Sponsor: Markus, B2B marketing lead

Rolle: betaler for sponsor-/leadprodukt.

Beslutning: om han kjøper sponsor package, unlock pack eller forlenger avtalen.

Job-to-be-done: dokumentere pipeline-verdi fra eventbudsjettet uten å bruke tid på ubrukelige leads.

Dagens workaround: logo, stand, badge scanning, konkurranser, LinkedIn outreach, usikker CRM-import.

Frykt og rode linjer:

- betale for leads som ikke er kvalifiserte,
- få for lite data til å følge opp,
- få data som legal/CRM ikke kan bruke,
- uklare reclaim/refund-regler.

Bevis han trenger:

- qualification criteria,
- consent proof,
- eksempel på role-scoped export,
- ROI dashboard og regler for revoke/reclaim.

DiMy-krok:

> Betal for kvalifiserte, samtykkede relasjoner med audit trail, ikke bare logoeksponering.

Story-moment: Markus ser et aggregert, consent-safe lead-potensial før kjøp. Han kjøper unlock pack, bruker credit på ett lead og får umiddelbart lovlig follow-up-scope.

Swarm-knobs: ROI pressure, data hunger, compliance maturity, sales cycle length, patience for consent friction.

Real validation needed: betalingsvilje per unlock, minimum datafelter, CRM-krav og sponsorens faktiske alternativkost.

### P5. Utstiller: Sara, stand- og salgsansvarlig på gulvet

Rolle: daglig operatør for sponsorverdi.

Beslutning: om hun faktisk bruker flyten i hektiske minutter mellom samtaler.

Job-to-be-done: fange relevante samtaler raskt, booke oppfølging og slippe å rydde kaos etterpå.

Dagens workaround: visittkort, QR-scan, notater, Excel, etterregistrering i CRM.

Frykt og rode linjer:

- for mange steg på stand,
- uklart hvorfor en lead er locked/unlocked,
- at hun ikke rekker å forklare samtykke,
- at data forsvinner inn i arrangørens system.

Bevis hun trenger:

- ultraenkel standflyt,
- klar status: candidate, consent pending, qualified, unlocked, reclaimed,
- follow-up CTA som ikke bryter scope.

DiMy-krok:

> Gjør gode samtaler om til ryddig oppfølging uten manuelt rot.

Story-moment: Sara har fem minutter mellom foredrag. Hun ser hvilke tre leads som er klare for unlock, hvem som venter på samtykke, og hvem som ikke kan kontaktes.

Swarm-knobs: time pressure, UI patience, sales urgency, number of conversations, CRM dependency.

Real validation needed: operativ brukbarhet på stand og hvor lite friksjon som kreves for at dette brukes i praksis.

### P6. DPO / IT-gatekeeper: Amalie, ansvarlig for datarisiko

Rolle: kan blokkere eller akselerere avtalen.

Beslutning: om arrangør eller sponsor får lov til å bruke DiMy i et reelt event.

Job-to-be-done: sikre at databehandling, roller, rettigheter og leverandøransvar er forståelig og forsvarlig.

Dagens workaround: DPIA, databehandleravtaler, vendor questionnaires, sikkerhetsvedlegg, manuelle avklaringer.

Frykt og rode linjer:

- uavklart behandlingsgrunnlag,
- uklare controllership/processor-roller,
- lagring av private payloads i audit/kosteventer,
- utilstrekkelig sletting, revoke eller eksportkontroll,
- AI eller CRM-eksport uten scope.

Bevis hun trenger:

- data flow map,
- role/capability matrix,
- retention og deletion policy,
- subprocessor-/providerliste,
- audit manifest som utelater hemmeligheter og rå private data.

DiMy-krok:

> Hver kommersiell handling kan knyttes til purpose, contract, consent og audit uten global profilering.

Story-moment: Amalie får en one-pager og spør: "Vis meg nøyaktig hvilken data sponsoren får etter et unlock, og hva som skjer hvis samtykket trekkes tilbake."

Swarm-knobs: compliance strictness, public sector requirements, AI policy strictness, vendor risk tolerance.

Real validation needed: DPA/DPIA-krav, sikkerhetsspørsmål, AI/subprocessor policy og juridisk vurdering.

### P7. Speaker / faglig bidragsyter: Jonas, foredragsholder

Rolle: innholdsleverandør, tillitsbærer og mulig lead-kilde.

Beslutning: om han deler materiale, godtar opptak/AI-oppsummering og bruker oppfølgingsflater.

Job-to-be-done: nå riktig publikum, få relevante spørsmål og oppfølging uten at innholdet misbrukes.

Dagens workaround: slides på e-post, LinkedIn-post, manuell Q&A, arrangørstatistikk.

Frykt og rode linjer:

- at opptak/transkripsjon brukes til mer enn avtalt,
- at publikumsspørsmål eller interesse blir sponsor-signaler uten tydelig scope,
- at han mister kontroll over materiale.

Bevis han trenger:

- material rights scope,
- AI/transcription opt-in,
- hvem som ser session insights,
- content takedown/revocation path.

DiMy-krok:

> Foredraget kan skape bedre faglig oppfølging uten at innhold og publikumssignaler flyter fritt.

Story-moment: Jonas ser at deltakere ønsker oppfølging etter foredraget, men bare innen et avgrenset topic og uten at råspørsmål deles med sponsor.

Swarm-knobs: reputation sensitivity, content IP concern, desire for audience reach, AI concern.

Real validation needed: speaker-kontrakter, opptaks-/AI-samtykke og hva foredragsholdere faktisk vil ha i rapport.

### P8. Investor / Innovasjon Norge-vurderer: Ragnhild, bevisorientert ekstern leser

Rolle: vurderer innovasjonshøyde, marked, ansvarlighet og gjennomføringsevne.

Beslutning: om prosjektet får støtte, investering, videre møte eller krav om mer bevis.

Job-to-be-done: skille et ansvarlig, testbart produktløp fra en stor uvalidert visjon.

Dagens workaround: pitch deck, roadmap, markedsintervjuer, teknisk due diligence, finansmodell.

Frykt og rode linjer:

- at DiMy høres ut som generisk konferanseapp,
- at value redistribution overpåstås,
- at regulatorisk risiko underkommuniseres,
- at betalingsvillig marked ikke er bevist.

Bevis hun trenger:

- avgrenset wedge,
- demo og teknisk roadmap,
- sponsor/arrangørintervjuer,
- claim-safe regulatorisk grense,
- marginmodell og bevisplan.

DiMy-krok:

> Konferanser er en avgrenset kommersiell wedge for å teste etterprøvbar verdiflyt, consent og sponsorverdi.

Story-moment: Ragnhild leser 60-sekundershistorien og spør: "Hva er bevist, hva er simulert, og hva må piloten avklare?"

Swarm-knobs: technical skepticism, funding criteria strictness, commercial risk tolerance, regulatory concern.

Real validation needed: investor/IN-respons, finansieringskriterier, krav til pilotkunde og dokumentasjon.

### P9. DiMy operator / support: Mikkel, ansvarlig for drift og margin

Rolle: intern operatør, support og marginvakt.

Beslutning: om produktet kan leveres uten at support, media, AI eller audit-kost spiser marginen.

Job-to-be-done: sette opp event, overvåke kost, håndtere unntak og forklare rapporter.

Dagens workaround: manuelle dashboards, cloud-kost, supportlogg, regneark, incident-notater.

Frykt og rode linjer:

- skjulte resource costs,
- uforutsigbar AI/media-bruk,
- sponsor-/deltakerkonflikter uten audit,
- manuell avstemming etter eventet.

Bevis han trenger:

- ResourceMeterEvent og ValueFlowEvent i runtime,
- idempotency og ledger truth,
- support playbook,
- policy warnings og export manifest.

DiMy-krok:

> Ingen betalt funksjon skal ha påslag før kostnadsgrunnlaget er synlig.

Story-moment: Mikkel ser en sponsorreclaim og kan forklare ledger event, consent revoke, unlock reversal og policykonsekvens uten å lete i fem systemer.

Swarm-knobs: incident load, media cost volatility, support staffing, audit strictness.

Real validation needed: faktisk driftstid, supporttid, ressursmåling og avstemmingsarbeid.

### P10. Procurement / økonomisk kjøper: Henrik, innkjøps- og budsjettansvarlig

Rolle: formell kjøper eller budsjettkontroll hos arrangør/sponsor.

Beslutning: om tilbudet kan godkjennes som event-tech, sponsorprodukt, SaaS eller konsulent-/driftspakke.

Job-to-be-done: forstå pris, risiko, avtaleomfang, leveranse og exit før kjøp.

Dagens workaround: tilbud fra eventplattform, CRM, streaming, byrå og manuell sponsorrapportering.

Frykt og rode linjer:

- uklar prismodell,
- lock-in,
- uforståelige overage-kostnader,
- uklar ansvarsmatrise mellom DiMy, arrangør, sponsor og underleverandører.

Bevis han trenger:

- quote med basepris, inkludert kvote, overage og audit/support,
- leveransebeskrivelse,
- exit/export-plan,
- sammenligning mot status quo.

DiMy-krok:

> Betal for en avgrenset konferanseflate med forklarbar pris og rapporterbar sponsorverdi.

Story-moment: Henrik vurderer om DiMy er dyrere enn dagens miks av eventplattform, badge scan og manuell rapport. DiMy må vise hva som blir mindre risikabelt og mer målbart.

Swarm-knobs: budget strictness, procurement bureaucracy, vendor risk tolerance, price sensitivity.

Real validation needed: kjøpskategori, godkjenningsnivå, prisanker og kontraktskrav.

### P11. Non-consenter / reclaimer: Lea, aktivt nei-takk-deltaker

Rolle: deltaker som enten nekter sponsorconsent fra start eller trekker samtykke tilbake etterpå.

Beslutning: om DiMy fortsatt oppleves frivillig og brukbart uten sponsorconsent.

Job-to-be-done: delta fullt på konferansen uten å bli straffet, nedprioritert eller indirekte presset til datadeling.

Dagens workaround: gi minst mulig informasjon, bruke anonym e-post, droppe app, unngå sponsorflater.

Frykt og rode linjer:

- at "frivillig" samtykke i praksis blir nødvendig for god opplevelse,
- at hun mister matching, agenda eller nettverk hvis hun sier nei,
- at revoke ikke stopper praktisk oppfølging,
- at sponsor allerede har eksportert data.

Bevis hun trenger:

- appen fungerer uten sponsorconsent,
- tydelig "nei takk" uten mørke mønstre,
- revoke viser konkret konsekvens,
- reclaim/audit forklarer hva sponsor ikke lenger kan gjøre.

DiMy-krok:

> Nei skal være et fullt gyldig valg, ikke en dårligere konferanseopplevelse.

Story-moment: Lea nekter all sponsoroppfølging på dag 1 og bruker fortsatt agenda, sesjonslagring og nettverksfunksjoner som ikke krever sponsorgrant. På dag 2 trekker hun tilbake ett tidligere samtykke og ser konkret hva som endres.

Swarm-knobs: refusal strictness, digital literacy, trust baseline, prior bad experience, need for networking.

Real validation needed: non-consenter usability, dark-pattern review, revoke comprehension og faktisk stopp i follow-up.

### P12. Skeptisk arrangør: Karin, merkevare- og omdømmeansvarlig

Rolle: intern arrangørkritiker som kan stoppe sponsorproduktet selv om inntektsansvarlig liker det.

Beslutning: om sponsorverdi-flyten er verdt omdømmerisikoen.

Job-to-be-done: beskytte konferansens tillit, faglige integritet og deltakeropplevelse.

Dagens workaround: holde sponsoraktivering enkel, begrense datafangst og akseptere svakere sponsorrapportering.

Frykt og rode linjer:

- at konferansen oppleves som en salgsarena forkledd som fag,
- at kritiske deltakere reagerer offentlig,
- at arrangøren mister kontroll over sponsoradferd,
- at DiMy sitt språk blir for teknisk til å berolige styre eller programkomite.

Bevis hun trenger:

- deltakeropplevelse uten sponsorpress,
- sponsor policy og enforcement,
- tydelig avgrensing mellom faglig matching og kommersielt unlock,
- krise-/kommunikasjonsplan for revoke eller klage.

DiMy-krok:

> Arrangøren kan si ja til sponsorverdi uten å gi sponsorene fri tilgang til deltakerne.

Story-moment: Karin spør hva som skjer hvis en deltaker skriver offentlig at konferansen selger persondata til sponsorer. DiMy-historien må være enkel, sann og dokumenterbar.

Swarm-knobs: reputational risk tolerance, public criticism sensitivity, sponsor dependency, board pressure.

Real validation needed: arrangørens reelle omdømmerisiko, kommunikasjonsbehov og terskel for sponsoraktivering.

### P13. Sponsor compliance: Victor, juridisk bevisst sponsorrepresentant

Rolle: sponsorens legal/compliance-gatekeeper.

Beslutning: om sponsor kan kjøpe og bruke unlock-produktet uten å skape GDPR-/CRM-/salgsrisiko.

Job-to-be-done: sikre at markeds- og salgsteamet bare får data de faktisk kan bruke, med dokumenterbart grunnlag.

Dagens workaround: stoppe uklare leadlister, kreve DPA, begrense import til CRM, slette usikre eventleads.

Frykt og rode linjer:

- qualification er uklart eller manipulerbart,
- samtykke dekker ikke sponsorens faktiske follow-up,
- eksporten inneholder for mye,
- revoke kommer etter at data er distribuert internt.

Bevis han trenger:

- qualification-kriterier,
- samtykkeformulering og scope,
- eksportfelt og retention,
- audit trail for unlock og revoke,
- intern sponsorrollemodell.

DiMy-krok:

> Sponsor får færre, ryddigere og mer brukbare leads fordi hvert unlock har consent, qualification og scope.

Story-moment: Victor nekter å signere før han ser nøyaktig hva "qualified" betyr, hvilke felt som eksporteres, og hvordan sponsor må reagere på revoke.

Swarm-knobs: legal strictness, CRM governance, sales pressure, tolerance for missing fields.

Real validation needed: sponsorens DPA-krav, CRM governance, lovlig follow-up-scope og qualification-definisjon.

## Arthur Scott-style story lens

For hver persona bør historien skrives som en konkret beslutningsscene:

```text
Personaen står i en virkelig situasjon.
Det finnes et press eller en konflikt.
Dagens løsning er utilstrekkelig eller risikabel.
DiMy gir en ny mulig handling.
Personaen får et konkret bevis.
Historien ender med en beslutning, innvending eller neste test.
```

Unngå historier som starter med teknologi:

```text
Dårlig start:
"DiMy bruker HAVEN/CellProtocol til domain-scoped identity og audit."

Bedre start:
"Ingrid må forklare hovedsponsor hva de fikk igjen for 180 000 kroner, uten å vise rå deltakerdata."
```

Teknologien skal komme inn som bevis, ikke som åpning.

## Scenarioer som bør simuleres

### S1. Arrangør får transparent event-quote

Primærpersonas: Ingrid, Henrik, Mikkel.

Spørsmål: Forstår arrangøren hva hun kjøper, hva som er inkludert, hvilke kostdrivere som finnes, og hva som skjer ved overage?

God swarm-output:

- uklare prisord,
- manglende bevis,
- hva procurement vil spørre om,
- hvor storyen må forenkles.

Må valideres ekte: betalingsvilje, budsjettlinje, akseptabel prisstruktur.

### S2. Sponsor vurderer unlock pack

Primærpersonas: Markus, Sara, Amalie.

Spørsmål: Er "qualified, consented lead unlock" tydelig nok til at sponsor ser merverdi over badge scans?

God swarm-output:

- dataminimum sponsor krever,
- compliance-friksjon,
- hva som gjør ROI dashboard troverdig,
- hvor reclaim/refund-regler må være synlige.

Må valideres ekte: sponsor WTP, CRM-krav, salgsprosess.

### S3. Deltaker får sponsorforespørsel

Primærpersonas: Nora, Elias, Amalie.

Spørsmål: Føles dette som kontroll og relevans, eller som penere pakket lead capture?

God swarm-output:

- samtykketekst som kan misforstås,
- røde flagg i value-return-språk,
- hva receipt må vise,
- hva revoke må forklare.

Må valideres ekte: comprehension test, samtykkevilje, tillitsreaksjon.

### S4. Revoke -> reclaim etter unlock

Primærpersonas: Nora, Markus, Ingrid, Mikkel, Amalie.

Spørsmål: Tåler produktfortellingen den vanskeligste hendelsen: deltaker trekker tilbake etter at sponsor har betalt/unlocket?

God swarm-output:

- hvem blir sint og hvorfor,
- hvilke audit events må finnes,
- hvilken supporttekst trengs,
- hva som er claim-risk.

Må valideres ekte: juridisk håndtering, sponsoraksept, supportkost.

### S5. DPO/IT preflight

Primærpersonas: Amalie, Elias, Henrik.

Spørsmål: Er dokumentasjonspakken nok til å ikke bli stoppet før demo?

God swarm-output:

- vendor questionnaire gaps,
- data flow gaps,
- AI/subprocessor-spørsmål,
- retention/deletion-uklarheter.

Må valideres ekte: DPA/DPIA-krav, sikkerhetskrav, databehandlerrolle.

### S6. Post-event value report

Primærpersonas: Ingrid, Markus, Ragnhild, Mikkel.

Spørsmål: Forteller rapporten en historie som kan selge neste event og samtidig tåle kritikk?

God swarm-output:

- hvilke KPI-er som er nyttige,
- hvilke tall som kan overpåstås,
- hva som bør skjules/aggregere,
- hva investor/IN vil tolke som bevis versus simulering.

Må valideres ekte: rapportnytte, sponsorfornyelse, investorrespons.

### S7. Speaker content and AI summary

Primærpersonas: Jonas, Nora, Amalie.

Spørsmål: Kan opptak, transkripsjon og AI-oppsummering brukes uten å undergrave tillit til konferansen?

God swarm-output:

- innholdsscope,
- AI-opt-in,
- publikumsdata som ikke bør deles,
- kontraktstekst som må tydeliggjøres.

Må valideres ekte: speaker-avtaler, AI-policy, innholdsrettigheter.

### S8. Investor/Innovasjon Norge pitch

Primærpersonas: Ragnhild, Ingrid, Markus, Elias.

Spørsmål: Er DiMy tydelig som ansvarlig event-tech kontrollplan, ikke generisk konferanseapp eller uvalidert økonomisk visjon?

God swarm-output:

- claims som er for sterke,
- bevis som mangler,
- første pilotspørsmål,
- pitch-rewrite per publikum.

Må valideres ekte: investor/IN-møter, pilotkundeintervjuer, regulatorisk rådgivning.

### S9. Non-consenter bruker hele konferansen

Primærpersonas: Lea, Nora, Karin, Amalie.

Spørsmål: Er samtykke faktisk frivillig hvis deltakeren sier nei til all sponsoroppfølging?

God swarm-output:

- funksjoner som fortsatt må virke,
- steder der UI kan presse brukeren,
- om "nei takk" er respektfullt nok,
- hvilke sponsor-/arrangør-KPI-er som ikke må skape straff for non-consent.

Må valideres ekte: usability for non-consenters, dark-pattern review og deltakeropplevelse uten sponsorgrant.

### S10. Sponsor prøver å omgå qualification

Primærpersonas: Markus, Victor, Sara, Elias, Mikkel.

Spørsmål: Hva blokkerer hvis en sponsor vil kjøpe alle leads uavhengig av samtykke eller kvalifisering?

God swarm-output:

- enforcement gaps,
- qualification-kriterier som må formaliseres,
- access-control krav,
- audit events for rejected unlock attempts.

Må valideres ekte: faktisk runtime enforcement, sponsorreaksjon og juridisk aksept for qualification-logikk.

### S11. Masse-revoke på dag 2

Primærpersonas: Lea, Ingrid, Karin, Markus, Victor, Mikkel, Amalie.

Spørsmål: Hva skjer hvis mange deltakere trekker samtykke etter at sponsor allerede har brukt credits?

God swarm-output:

- konfliktkart mellom deltaker, sponsor og arrangør,
- refund/reclaim policy gaps,
- support- og kommunikasjonsbehov,
- ledger/audit events som må finnes.

Må valideres ekte: juridisk håndtering, sponsoravtale, supportkost og teknisk ledger reconciliation.

### S12. Arrangør prøver full deltakerprofil-eksport

Primærpersonas: Ingrid, Karin, Amalie, Elias, Mikkel.

Spørsmål: Stopper role-scoped access arrangøren fra å hente mer data enn avtalt?

God swarm-output:

- hvilke exports som skal avvises,
- hvordan avvisning forklares,
- audit for denied requests,
- hva arrangøren legitimt kan få aggregert.

Må valideres ekte: capability enforcement, data export policy og arrangørens rapportbehov.

### S13. Post-event query lease seks måneder senere

Primærpersonas: Nora, Lea, Markus, Ingrid, Amalie.

Spørsmål: Oppleves tidsavgrenset follow-up som et nytt frivillig grant, eller som et evig nyhetsbrev i forkledning?

God swarm-output:

- copy for tidsavgrensing,
- hva som er nytt formål versus opprinnelig conference consent,
- expiry/revoke-forventninger,
- sponsorens minimumsverdi.

Må valideres ekte: deltakerforståelse, sponsorverdi og juridisk vurdering av nytt formål.

## Swarm-strategi

Start med en enkel swarm, ikke nye runtime-celler.

Minimum input til en simulering:

- scenario,
- artefakt under test: pitch, one-pager, consent copy, report, dashboard, quote,
- 3-5 personaer,
- v0-guardrails,
- hva simuleringen skal produsere.

Minimum output:

- personaens umiddelbare reaksjon,
- topp 5 innvendinger,
- uklare ord eller claims,
- bevis som mangler,
- endret story i personaens språk,
- hva som må valideres med ekte mennesker,
- claim classification: safe, safe with caveat, aspirational, unsupported, forbidden.

Ikke la swarmen produsere:

- estimerte consent-rates som beslutningsgrunnlag,
- "markedet vil betale" uten ekte intervju,
- juridiske konklusjoner,
- global reputation-funksjoner,
- transferable credits, cash-out eller P2P-value i v0.

## Når bør dette bli egne Celler?

Ikke bygg egne Celler før opplegget gjentas nok til at strukturert state og replay gir verdi. Første steg bør være dokument + JSON-fixture + prompt.

Mulige Celler senere:

| Celle | Nyttig når | Ansvar |
| --- | --- | --- |
| `PersonaCatalogCell` | personaene endres ofte og må versjoneres | holder proto-personaer, kilder og valideringsstatus |
| `StoryScenarioRunnerCell` | dere kjører mange story-tester mot samme artefakter | kjører scenario mot persona-sett og lagrer output |
| `ClaimSafetyReviewCell` | pitch copy endres ofte | klassifiserer claims mot canon/maturity |
| `EvidenceNeedCell` | dere vil koble innvendinger til faktisk research backlog | lager evidence gaps og intervjuspørsmål |
| `InterviewSynthesisCell` | ekte intervjuer begynner å komme inn | oppdaterer personaer fra menneskelig data, ikke syntetiske antakelser |

Anbefalt nå:

1. Bruk `fixtures/conference_personas_and_story_scenarios.v0.json` som første swarm-input.
2. Bruk `Prompts/conference_persona_story_swarm.md` til story-kritikk.
3. Ikke bygg egne AI-assistent-celler før dere har kjørt minst 5-10 manuelle/syntetiske story-tester og vet hvilke outputs som faktisk blir gjenbrukt.

## Prioritert valideringsplan

P0:

- 3 arrangørintervjuer om sponsorverdi, pris og rapport.
- 5 deltaker-comprehension tests av sponsorforespørsel og consent receipt.
- 3 sponsorintervjuer om unlock pack, dataminimum og betalingsvilje.
- 2 DPO/IT-gjennomganger av data flow, revoke og audit.

P1:

- 2 speaker-intervjuer om opptak, AI-oppsummering og session insights.
- 2 procurement-/økonomikjøper-samtaler om quote og kontrakt.
- 2 investor/IN-lesninger av 60-sekundershistorien og bevisplan.

P2:

- live pilot med måling av consent comprehension, unlock conversion, supporttid, reclaims og sponsorfornyelsesintensjon.

## Claim-safe formuleringer

Trygge:

- "DiMy designer en konferanseflyt der sponsor-unlock krever samtykke, kvalifisering og audit."
- "V0 bruker event-domain scoped entitlements og simulerer eventuell deltakerfordel som ikke-overførbar benefit."
- "Swarm-simulering brukes til hypoteser og story-kritikk, ikke som erstatning for brukerintervjuer."

Med caveat:

- "Deltakere kan få verdi tilbake" -> "V0 kan simulere en ikke-overførbar deltakerfordel; ekte fordel krever juridisk og regnskapsmessig vurdering."
- "Sponsorer får bedre leads" -> "Hypotesen er at kvalifiserte, samtykkede leads kan gi høyere sponsorverdi; dette må valideres i pilot."
- "Audit gjør dette tryggere" -> "Role-scoped audit kan gjøre hendelser mer etterprøvbare; runtime events og eksport må implementeres og testes."

Unngå:

- "Dette er regulatorisk avklart."
- "Dette er ikke e-money."
- "Deltakerne får betalt."
- "Dette løser problemet med kommersialisering av persondata."
- "Synthetic personas validerer markedet."
